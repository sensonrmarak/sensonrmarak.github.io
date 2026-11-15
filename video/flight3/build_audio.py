"""Narration (same Kokoro 'am_fenrir' voice, speed 0.975), procedural sound design and adaptive score.
Writes out/audio_mix.wav, out/narration.wav and timings.json (scene/line times + every SFX event)."""
import json, os, wave
import numpy as np
from kokoro_onnx import Kokoro

SR = 48000; GAP = 0.22; LEAD = 0.75; TAIL = 0.75
K = Kokoro("/tmp/kokoro/kokoro-v1.0.onnx", "/tmp/kokoro/voices-v1.0.bin")
rng = np.random.default_rng(11)
script = json.load(open("script.json"))

def synth(text):
    x, sr = K.create(text, voice="am_fenrir", speed=0.975, lang="en-us")
    x = np.asarray(x, dtype=np.float32); n = int(len(x) * SR / sr)
    a = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
    nz = np.where(np.abs(a) > 0.01)[0]
    return a[max(0, nz[0] - 480): nz[-1] + 2400] if len(nz) else a

# ---------------------------------------------------------------- narration + timings
t = 0.0; chunks = []; scenes = []; events = []
for sc in script:
    s0 = t; t += 0.45 if sc["id"] == "hook" else LEAD; lines = []
    if sc["id"] == "hook": t += 1.2            # engines spool before the first word
    for ln in sc["lines"]:
        a = synth(ln["t"]); chunks.append((t, a)); d = len(a) / SR
        lines.append({"text": ln["t"], "start": round(t - s0, 3), "end": round(t - s0 + d, 3)})
        for name, off in ln.get("sfx", []): events.append({"name": name, "t": round(t + off, 3), "scene": sc["id"]})
        t += d + GAP + ln.get("pause", 0)
    t += TAIL - GAP
    if sc["id"] == "end": t += 6.0
    if sc["id"] != "hook": events.append({"name": "whoosh_in", "t": round(s0, 3), "scene": sc["id"]})
    scenes.append({"id": sc["id"], "title": sc["title"], "phase": sc.get("phase", ""), "start": round(s0, 3), "dur": round(t - s0, 3), "lines": lines})
total = t; N = int(total * SR) + SR; tt = np.arange(N) / SR
voice = np.zeros(N, np.float32)
for st, a in chunks: voice[int(st * SR): int(st * SR) + len(a)] += a
voice /= np.abs(voice).max() / 0.9

# ---------------------------------------------------------------- DSP helpers
def lpf(x, k):           # cheap FIR low-pass (moving average of k samples), vectorised
    if k <= 1: return x
    c = np.cumsum(np.concatenate([[0.0], x]).astype(np.float64)); return np.pad((c[k:] - c[:-k]) / k, (k - 1, 0)).astype(np.float32)
def ov(*xs):             # sum signals of different lengths
    n = max(len(x) for x in xs); y = np.zeros(n, np.float32)
    for x in xs: y[:len(x)] += x
    return y
def noise(n): return rng.standard_normal(n).astype(np.float32)
def env(n, a, r): e = np.ones(n, np.float32); A = int(a * SR); R = int(r * SR); e[:A] = np.linspace(0, 1, A) if A else 1; e[-R:] *= np.linspace(1, 0, R) if R else 1; return e
def place(buf, at, x, g=1.0):
    i = int(at * SR);
    if i < 0: x = x[-i:]; i = 0
    j = min(len(buf), i + len(x)); buf[i:j] += x[: j - i] * g
def thump(f0=60, f1=32, d=0.6, g=1.0):
    n = int(d * SR); k = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-k * 9); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-k * 7) * g).astype(np.float32)
def click(d=0.05, k=6): n = int(d * SR); return (lpf(noise(n), k) * np.exp(-np.arange(n) / SR * 60)).astype(np.float32)
def tone(f, d, dec=3.0, h=(1, 0.3, 0.1)):
    n = int(d * SR); k = np.arange(n) / SR; x = sum(a * np.sin(2 * np.pi * f * (i + 1) * k) for i, a in enumerate(h))
    return (x * np.exp(-k * dec) * env(n, 0.005, 0.05)).astype(np.float32)
def sweep_noise(d, k0, k1, g=1.0):   # filtered noise whose darkness moves from k0 to k1 taps
    n = int(d * SR); x = noise(n); out = np.zeros(n, np.float32); steps = 24
    for s in range(steps):
        a, b = s * n // steps, (s + 1) * n // steps; k = int(k0 + (k1 - k0) * s / (steps - 1)); out[a:b] = lpf(x, max(1, k))[a:b]
    return out * np.sin(np.linspace(0, np.pi, n)) ** 2 * g

# ---------------------------------------------------------------- engine & wind beds driven by flight phase
sfx = np.zeros(N, np.float32)
def S(name): return [e["t"] for e in events if e["name"] == name]
def scene_t(i): return scenes[i]["start"]
sc_by = {s["id"]: s for s in scenes}
# thrust curve (0..1) and airspeed (0..1) over the film, piecewise from scene times
def ramp(x, a, b): return np.clip((x - a) / max(1e-6, b - a), 0, 1)
h = sc_by["hook"]; spool0 = h["start"] + 0.2; roll0 = h["start"] + h["lines"][1]["start"]; rot = h["start"] + h["lines"][2]["start"] + 2.2
thrust = np.zeros(N, np.float32); speed = np.zeros(N, np.float32)
thrust += 0.9 * ramp(tt, spool0, spool0 + 2.4) * (1 - ramp(tt, sc_by["forces"]["start"] - 0.2, sc_by["forces"]["start"] + 0.2))  # hook full thrust, cut on freeze
speed += ramp(tt, roll0, rot) * (1 - ramp(tt, sc_by["forces"]["start"] - 0.2, sc_by["forces"]["start"] + 0.2))
for sid, th, spd in [("equation", 0.0, 0.0), ("engine", 0.75, 0.6), ("cruise", 0.45, 0.8), ("drag", 0.45, 0.8), ("controls", 0.45, 0.8), ("parts", 0.4, 0.75), ("stall", 0.25, 0.45), ("landing", 0.3, 0.4)]:
    s = sc_by[sid]; m = ramp(tt, s["start"], s["start"] + 1.2) * (1 - ramp(tt, s["start"] + s["dur"] - 0.6, s["start"] + s["dur"]))
    thrust += th * m; speed += spd * m
# equation scene replays the takeoff roll in its last line
e = sc_by["equation"]; l3 = e["start"] + e["lines"][3]["start"]; m = ramp(tt, l3, l3 + 5.0) * (1 - ramp(tt, e["start"] + e["dur"] - 0.6, e["start"] + e["dur"]))
thrust += 0.8 * ramp(tt, l3 - 0.5, l3 + 1.0) * (1 - ramp(tt, e["start"] + e["dur"] - 0.6, e["start"] + e["dur"])); speed += m
# landing: touchdown and reverse thrust
ld = sc_by["landing"]; td = ld["start"] + ld["lines"][2]["start"]; rv = ld["start"] + ld["lines"][4]["start"]
speed *= 1 - 0.6 * ramp(tt, td, rv + 3)
thrust += 0.7 * ramp(tt, rv, rv + 0.6) * (1 - ramp(tt, rv + 2.8, rv + 4.2))
thrust = lpf(thrust, 2400); speed = lpf(speed, 2400)
# engine: rumble + whine whose pitch follows thrust
rumble = lpf(noise(N), 60) * 3.0
ph = 2 * np.pi * np.cumsum(180 + 900 * thrust) / SR
whine = (np.sin(ph) * 0.12 + np.sin(ph * 2.03) * 0.05 + np.sin(ph * 3.1) * 0.02).astype(np.float32)
engine = (rumble * (0.25 + 0.75 * thrust) + whine * thrust) * thrust * 0.3
wind = lpf(noise(N), 6) * speed * 0.16
sfx += engine + wind
# runway seams: thumps that accelerate with speed during both takeoff rolls
for a, b in [(roll0, rot), (l3, l3 + 5.0)]:
    x = a
    while x < b:
        k = (x - a) / (b - a); place(sfx, x, thump(70, 40, 0.18, 0.25 + 0.2 * k)); x += 0.55 - 0.42 * k

# ---------------------------------------------------------------- one-shot effects
def add(name, at):
    if name == "hit": place(sfx, at, ov(thump(70, 28, 1.2, 0.9), click(0.05, 3) * 0.6))
    elif name == "stamp": place(sfx, at, ov(thump(90, 40, 0.5, 0.8), click(0.08, 2) * 0.8))
    elif name in ("pop",): place(sfx, at, ov(tone(520, 0.25, 14, (1, 0.4)) * 0.18, click(0.03, 4) * 0.3))
    elif name == "tick": place(sfx, at, tone(1318, 0.9, 4, (1, 0.25)) * 0.16); place(sfx, at + 0.12, tone(1760, 0.9, 4, (1, 0.25)) * 0.12)
    elif name == "chime": place(sfx, at, tone(1046.5, 1.6, 2.2, (1, 0.2, 0.05)) * 0.22); place(sfx, at + 0.55, tone(784, 2.0, 1.8, (1, 0.2, 0.05)) * 0.22)
    elif name in ("whoosh", "whoosh_in", "slice", "freeze"):
        g = {"whoosh": 0.5, "whoosh_in": 0.35, "slice": 0.6, "freeze": 0.55}[name]; place(sfx, at - 0.35, sweep_noise(0.7, 40, 3, g) * 1.4)
        if name == "freeze": place(sfx, at, thump(110, 50, 0.35, 0.5))
    elif name == "riser": place(sfx, at, sweep_noise(1.3, 60, 2, 0.5) * np.linspace(0.2, 1.3, int(1.3 * SR)))
    elif name == "rotate": place(sfx, at, sweep_noise(1.6, 30, 4, 0.4))
    elif name == "liftoff": place(sfx, at, sweep_noise(2.4, 8, 30, 0.5))     # rumble falls away as the wheels leave the ground
    elif name == "clunk": place(sfx, at, ov(thump(130, 60, 0.3, 0.7), click(0.04, 2)))
    elif name == "gear": place(sfx, at, thump(55, 30, 0.8, 1.0)); place(sfx, at + 0.05, lpf(noise(int(0.6 * SR)), 3) * np.exp(-np.arange(int(0.6 * SR)) / SR * 8) * 0.25)
    elif name == "touchdown":
        n = int(0.35 * SR); ch = lpf(noise(n), 2) * np.exp(-np.arange(n) / SR * 10) * 0.5; place(sfx, at, ch); place(sfx, at + 0.02, thump(60, 30, 0.9, 1.1))
    elif name == "flaps":
        n = int(2.2 * SR); k = np.arange(n) / SR; f = 330 + 140 * np.minimum(k / 1.6, 1); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 31 * k))
        place(sfx, at, (x * env(n, 0.15, 0.3) * 0.07).astype(np.float32)); place(sfx, at + 2.1, thump(90, 50, 0.25, 0.4))
    elif name == "servo":
        n = int(0.6 * SR); k = np.arange(n) / SR; x = np.sin(2 * np.pi * np.cumsum(500 + 200 * k) / SR); place(sfx, at, (x * env(n, 0.05, 0.2) * 0.05).astype(np.float32))
    elif name == "explode": place(sfx, at, sweep_noise(1.0, 2, 30, 0.5)); place(sfx, at, thump(80, 35, 0.8, 0.6))
    elif name in ("suck", "squeeze", "bang", "blow"):
        if name == "bang": place(sfx, at, thump(75, 30, 1.0, 1.0)); place(sfx, at, lpf(noise(int(0.8 * SR)), 2) * np.exp(-np.arange(int(0.8 * SR)) / SR * 5) * 0.4)
        else: place(sfx, at, sweep_noise(0.9, {"suck": 30, "squeeze": 12, "blow": 4}[name], {"suck": 4, "squeeze": 3, "blow": 30}[name], 0.45))
    elif name == "alarm":
        for i in range(4): place(sfx, at + i * 0.32, tone(880 if i % 2 == 0 else 660, 0.28, 2, (1, 0.5, 0.25)) * 0.13)
    elif name == "reverse": place(sfx, at, sweep_noise(3.0, 20, 3, 0.4))
    elif name in ("spool", "roll"): pass   # handled by the engine/wind beds
for e in events: add(e["name"], e["t"])

# ---------------------------------------------------------------- adaptive score
music = np.zeros(N, np.float32)
MOOD = {"hook": (0.9, "build"), "forces": (0.45, "calm"), "wing": (0.55, "calm"), "myth": (0.5, "curious"), "equation": (0.6, "build"), "engine": (0.75, "drive"),
        "cruise": (0.4, "calm"), "drag": (0.45, "calm"), "controls": (0.5, "drive"), "parts": (0.5, "curious"), "stall": (0.7, "tense"), "landing": (0.75, "drive"), "recap": (0.7, "resolve"), "end": (0.6, "resolve")}
PROG = {"calm": [[110, 164.8, 220, 261.6, 329.6], [87.3, 130.8, 174.6, 220, 329.6], [130.8, 196, 261.6, 329.6, 392], [98, 146.8, 196, 246.9, 293.7]],
        "curious": [[110, 164.8, 220, 246.9, 329.6], [98, 146.8, 196, 246.9, 349.2], [87.3, 130.8, 174.6, 261.6, 329.6], [82.4, 123.5, 164.8, 246.9, 329.6]],
        "build": [[110, 164.8, 220, 261.6, 329.6], [130.8, 196, 261.6, 329.6, 392], [98, 146.8, 196, 246.9, 293.7], [87.3, 130.8, 174.6, 220, 329.6]],
        "drive": [[110, 164.8, 220, 261.6, 329.6], [98, 146.8, 196, 246.9, 293.7], [87.3, 130.8, 174.6, 220, 261.6], [98, 146.8, 196, 246.9, 293.7]],
        "tense": [[110, 155.6, 220, 261.6, 311.1], [103.8, 155.6, 207.7, 246.9, 311.1], [110, 164.8, 233.1, 261.6, 349.2], [103.8, 146.8, 207.7, 261.6, 293.7]],
        "resolve": [[87.3, 130.8, 174.6, 220, 349.2], [98, 146.8, 196, 246.9, 392], [130.8, 196, 261.6, 329.6, 392], [130.8, 196, 261.6, 329.6, 523.3]]}
BPM = 100; beat = 60 / BPM; bar = beat * 4
for s in scenes:
    a0, a1 = int(s["start"] * SR), int(min(total, s["start"] + s["dur"]) * SR); n = a1 - a0; k = np.arange(n) / SR; inten, mood = MOOD[s["id"]]; chords = PROG[mood]
    seg = np.zeros(n, np.float32)
    for ci in range(int(np.ceil(s["dur"] / (bar * 2))) + 1):
        ch = chords[ci % 4]; c0 = ci * bar * 2; m = (k >= c0) & (k < c0 + bar * 2 + 0.6)
        if not m.any(): continue
        kk = k[m] - c0; e = np.clip(kk / 0.8, 0, 1) * np.clip((bar * 2 + 0.6 - kk) / 0.6, 0, 1)
        for f in ch: seg[m] += (np.sin(2 * np.pi * f * k[m]) + 0.3 * np.sin(2 * np.pi * f * 2.001 * k[m]) + 0.12 * np.sin(2 * np.pi * f * 3 * k[m])) * e * 0.022
        if mood in ("drive", "build", "tense", "resolve"):   # pulsing bass on the beat
            b = ch[0] / 2; ph = (kk % beat) / beat; seg[m] += np.sin(2 * np.pi * b * k[m]) * np.exp(-ph * 5) * 0.09 * inten
        if mood in ("drive", "tense"):                       # soft kick on beats 1 and 3, hat on the offbeat
            ph2 = (kk % (beat * 2)); seg[m] += np.sin(2 * np.pi * (50 + 60 * np.exp(-ph2 * 30)) * ph2) * np.exp(-ph2 * 12) * 0.12 * inten
    if s["id"] == "hook":   # rising build into liftoff, then silence for the cut to black
        lift = s["lines"][2]["start"] + 2.2; seg *= np.clip(k / lift, 0.3, 1) * (1 - np.clip((k - lift) / 0.2, 0, 1) * (k < lift + 1.6))
    fade = np.clip(k / 0.8, 0, 1) * np.clip((s["dur"] - k) / 0.6, 0, 1); music[a0:a1] += seg * fade * (0.6 + 0.6 * inten)
music *= np.clip(tt / 1.5, 0, 1) * np.clip((total - tt) / 3, 0, 1)

# ---------------------------------------------------------------- mix: duck music and beds under the voice
envv = lpf(np.abs(voice), SR // 4); duck = 1 - 0.6 * np.clip(envv * 12, 0, 1); duck_s = 1 - 0.35 * np.clip(envv * 12, 0, 1)
mix = voice * 0.95 + music * duck * 1.25 + sfx * duck_s * 0.7
mix = np.tanh(mix * 1.3) / 1.3; mix *= 0.93 / np.abs(mix).max()   # soft limiter, peak -0.6 dBFS
def wr(name, x):
    st = np.clip(np.stack([x, x], 1)[: int(total * SR)], -1, 1); w = wave.open(name, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
os.makedirs("out", exist_ok=True); wr("out/audio_mix.wav", mix); wr("out/narration.wav", voice)
json.dump({"total": round(total, 3), "scenes": scenes, "events": events}, open("timings.json", "w"), indent=1)
print("total", round(total, 1), "s;", " ".join(f"{s['id']}={s['dur']:.1f}" for s in scenes), "| events", len(events))
