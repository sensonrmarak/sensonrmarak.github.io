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
# marks: the time a word ends inside a line = length of that line's prefix synthesised on its own
_mk = {}
def mark_time(prefix):
    if prefix not in _mk: _mk[prefix] = len(synth(prefix)) / SR
    return _mk[prefix]
t = 0.0; chunks = []; scenes = []; events = []; hush = []
for sc in script:
    s0 = t; t += 0.45 if sc["id"] == "hook" else LEAD; lines = []
    if sc["id"] == "hook": t += 1.2            # engines spool before the first word
    if sc.get("card"): t += 0.6                # room for the phase title card
    for ln in sc["lines"]:
        if ln.get("pre"): hush.append((t - 0.5, t + ln["pre"])); t += ln["pre"]   # a beat of near-silence before a payoff
        a = synth(ln["t"]); chunks.append((t, a)); d = len(a) / SR
        marks = {k: round(mark_time(v), 3) for k, v in ln.get("marks", {}).items()}
        lines.append({"text": ln["t"], "start": round(t - s0, 3), "end": round(t - s0 + d, 3), "marks": marks})
        for name, off in ln.get("sfx", []): events.append({"name": name, "t": round(t + (marks[off[1:]] if isinstance(off, str) else off), 3), "scene": sc["id"]})
        t += d + GAP + ln.get("pause", 0)
    t += TAIL - GAP
    post0 = t; t += sc.get("post", 0)
    for name, off in sc.get("post_sfx", []): events.append({"name": name, "t": round(post0 + off, 3), "scene": sc["id"]})
    if sc["id"] == "end": t += 6.0
    if sc["id"] not in ("hook",) and not sc.get("card"): events.append({"name": "whoosh_in", "t": round(s0, 3), "scene": sc["id"]})
    if sc.get("card"): events.append({"name": "card", "t": round(s0, 3), "scene": sc["id"]})
    stops = []
    for kind, li, off, label in sc.get("stops", []):
        L = lines[li]; at = L["end"] + 0.1 if off == "end" else L["start"] + (L["marks"][off[1:]] if isinstance(off, str) else off)
        stops.append({"kind": kind, "t": round(at, 3), "label": label}); events.append({"name": kind, "t": round(s0 + at, 3), "scene": sc["id"]})
    scenes.append({"id": sc["id"], "title": sc["title"], "phase": sc.get("phase", ""), "card": sc.get("card", ""), "start": round(s0, 3), "dur": round(t - s0, 3), "post": round(post0 - s0, 3), "lines": lines, "stops": stops})
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
# recorded aircraft (InspectorJ, CC BY 4.0): approach-and-pass flyby, peak about 14 s into the file
def loadwav(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; return x
FLY = loadwav("sfx/lib/flyby.wav"); FLY /= np.abs(FLY).max()
def clip(a, b): return FLY[int(a * SR): int(b * SR)].copy()
def loop(x, n, xf=SR):
    out = np.zeros(n + len(x), np.float32); pos = 0; fade = np.linspace(0, 1, xf, dtype=np.float32)
    while pos < n:
        y = x.copy(); y[:xf] *= fade; y[-xf:] *= fade[::-1]; out[pos: pos + len(y)] += y; pos += len(x) - xf
    return out[:n]
def window(x, at, a, b, fi=1.0, fo=1.0):     # place x so that its sample 0 lands at time `at`, audible only between a and b (absolute times)
    n0, n1 = int(max(0, a) * SR), int(min(total, b) * SR); y = np.zeros(N, np.float32); i0 = int(at * SR)
    for n in (n0,):
        src0 = n0 - i0; L = n1 - n0
        if src0 < 0: n0 -= src0; L += src0; src0 = 0
        L = max(0, min(L, len(x) - src0)); y[n0: n0 + L] = x[src0: src0 + L]
    e = np.clip((tt - a) / max(fi, 1e-3), 0, 1) * np.clip((b - tt) / max(fo, 1e-3), 0, 1); return y * e
bed = np.zeros(N, np.float32)
h = sc_by["hook"]; Lf_abs = h["start"] + h["lines"][3]["start"] - 1.7; Fz = h["start"] + h["stops"][0]["t"] if h["stops"] else h["start"] + h["dur"] - 1
bed += window(FLY, Lf_abs - 14.0, h["start"] + 0.8, Fz, fi=2.0, fo=0.12)                     # takeoff roll: the flyby's own crescendo peaks at liftoff, cut dead on the freeze
e = sc_by["equation"]; l3 = e["start"] + e["lines"][3]["start"]
bed += 0.9 * window(FLY, l3 + 5.0 - 14.0, l3 - 0.8, e["start"] + e["dur"], fi=1.2, fo=0.6)  # the takeoff replay in the lift-equation scene
ROAR = loop(clip(13, 22), N); ROAR /= np.abs(ROAR).max(); CABIN = lpf(ROAR, 48); CABIN /= np.abs(CABIN).max()
def span(sid, g0, sig, fi=1.0, fo=0.8, a=None, b=None):
    s_ = sc_by[sid]; A = s_["start"] if a is None else a; B = s_["start"] + s_["dur"] if b is None else b
    return g0 * sig * np.clip((tt - A) / fi, 0, 1) * np.clip((B - tt) / fo, 0, 1)
bed += span("engine", 0.45, lpf(ROAR, 3))
for sid in ("cruise", "drag", "controls", "parts"): bed += span(sid, 0.5, CABIN)
ld = sc_by["landing"]; td = ld["start"] + ld["lines"][2]["start"]; rv = ld["start"] + ld["lines"][4]["start"]; post0 = ld["start"] + ld["post"]
bed += span("stall", 0.3, lpf(ROAR, 6)); bed += span("landing", 0.3, lpf(ROAR, 6), b=td + 0.6, fo=0.5)
bed += 0.85 * window(clip(13, 19), rv, rv, rv + 5.5, fi=0.35, fo=2.2)                          # reverse thrust
tail = clip(22, 44); r = np.cumsum(np.linspace(1.0, 0.55, len(tail))); tail = np.interp(np.clip(r, 0, len(tail) - 1), np.arange(len(tail)), tail).astype(np.float32)
bed += 0.6 * window(tail, post0 - 0.4, post0 - 0.4, post0 + 6.0, fi=0.5, fo=2.5)                 # spool-down at the gate, pitch sliding down
# whine for "Full thrust" and a whisper of wind with airspeed
ph = 2 * np.pi * np.cumsum(180 + 900 * thrust) / SR
whine = (np.sin(ph) * 0.12 + np.sin(ph * 2.03) * 0.05).astype(np.float32) * thrust * (tt < Fz)
wind = lpf(noise(N), 6) * speed * 0.05
# runway seams: thumps that accelerate with speed during both takeoff rolls
for a, b in [(roll0, min(rot, Lf_abs)), (l3, l3 + 5.0)]:
    x = a
    while x < b:
        k = (x - a) / (b - a); place(sfx, x, thump(70, 40, 0.18, 0.15 + 0.12 * k)); x += 0.55 - 0.42 * k

# ---------------------------------------------------------------- one-shot effects
def add(name, at):
    if name == "hit": place(sfx, at, ov(thump(70, 28, 1.2, 0.9), click(0.05, 3) * 0.6))
    elif name == "stamp": place(sfx, at, ov(thump(90, 40, 0.5, 0.8), click(0.08, 2) * 0.8))
    elif name in ("pop",): place(sfx, at, ov(tone(520, 0.25, 14, (1, 0.4)) * 0.18, click(0.03, 4) * 0.3))
    elif name == "tick": place(sfx, at, tone(1318, 0.9, 4, (1, 0.25)) * 0.16); place(sfx, at + 0.12, tone(1760, 0.9, 4, (1, 0.25)) * 0.12)
    elif name == "chime":
        for f0, dt in ((1046.5, 0.0), (830.6, 0.6)):
            n = int(2.4 * SR); k = np.arange(n) / SR; x = sum(a_ * np.sin(2 * np.pi * f0 * m * k) * np.exp(-k * d_) for m, a_, d_ in ((1, 1, 1.6), (2.76, 0.35, 3.5), (5.4, 0.12, 6)))
            place(sfx, at + dt, (x * env(n, 0.003, 0.3) * 0.16).astype(np.float32))
    elif name in ("whoosh", "whoosh_in", "slice"):
        g = {"whoosh": 0.5, "whoosh_in": 0.3, "slice": 0.6}[name]; place(sfx, at - 0.35, sweep_noise(0.7, 40, 3, g) * 1.4)
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
    elif name == "rewind":
        n = int(0.75 * SR); k = np.arange(n) / SR; f = 2400 * np.exp(-k * 3.2) + 260; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 38 * k)))
        place(sfx, at, (x * env(n, 0.01, 0.15) * 0.07).astype(np.float32) + lpf(noise(n), 2) * env(n, 0.01, 0.2) * 0.05)
    elif name == "pause":
        place(sfx, at - 0.3, sweep_noise(0.6, 40, 3, 0.5)); n = int(0.45 * SR); k = np.arange(n) / SR; f = 520 * np.exp(-k * 4); place(sfx, at, (np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.005, 0.2) * 0.07).astype(np.float32)); place(sfx, at, thump(110, 50, 0.35, 0.45))
    elif name == "resume": place(sfx, at - 0.25, sweep_noise(0.55, 3, 40, 0.45)); place(sfx, at, click(0.03, 3) * 0.4)
    elif name == "card": place(sfx, at - 0.9, sweep_noise(1.0, 60, 2, 0.35) * np.linspace(0.2, 1, int(1.0 * SR))); place(sfx, at + 0.1, thump(52, 28, 1.8, 0.8))
    elif name == "spooldown": pass   # the recorded tail in the bed
    elif name in ("spool", "roll", "freeze"): pass   # beds, or the pause event at the same moment
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
PL = {}
def pluck(f, d=1.4):        # Karplus-Strong plucked string, cached per pitch
    key = round(f, 1)
    if key not in PL:
        n = int(d * SR); p = max(2, int(SR / f)); buf = rng.uniform(-1, 1, p).astype(np.float32); out = np.zeros(n, np.float32)
        for i in range(0, n, p):
            m = min(p, n - i); out[i: i + m] = buf[:m]; buf = 0.996 * 0.5 * (buf + np.roll(buf, -1))
        PL[key] = lpf(out, 3) * env(n, 0.002, 0.25)
    return PL[key]
def pad_note(f, n):          # detuned additive saw, darkened: reads as soft strings
    k = np.arange(n) / SR; x = np.zeros(n, np.float32)
    for det in (-0.004, 0.0, 0.005):
        for m in range(1, 7): x += np.sin(2 * np.pi * f * (1 + det) * m * k + m) / m
    return lpf(x, 24) * (1 + 0.04 * np.sin(2 * np.pi * 5.1 * k))
ARP = {"calm": (2, [0, 2, 1, 3]), "curious": (2, [0, 3, 1, 4, 2, 3]), "build": (4, [0, 2, 3, 4]), "drive": (4, [0, 1, 2, 3, 4, 3, 2, 1]), "tense": (4, [0, 1, 0, 2]), "resolve": (2, [0, 2, 4, 3])}
for s_ in scenes:
    a0, a1 = int(s_["start"] * SR), int(min(total, s_["start"] + s_["dur"]) * SR); n = a1 - a0; k = np.arange(n) / SR; inten, mood = MOOD[s_["id"]]; chords = PROG[mood]
    seg = np.zeros(n + 2 * SR, np.float32); per, pat = ARP[mood]
    for ci in range(int(np.ceil(s_["dur"] / (bar * 2))) + 1):
        ch = chords[ci % 4]; c0 = ci * bar * 2; L = int((bar * 2 + 0.8) * SR); i0 = int(c0 * SR)
        if i0 >= n: break
        e = env(L, 0.9, 0.8); pd = sum(pad_note(f, L) for f in ch[:3]) * e * 0.010
        seg[i0: i0 + L] += pd[: len(seg) - i0]
        step = beat / per
        for j in range(int(bar * 2 / step)):
            t0 = int((c0 + j * step) * SR); f = ch[pat[j % len(pat)] % len(ch)] * (2 if mood in ("drive", "build") else 1); x = pluck(f) * (0.07 if j % per == 0 else 0.045)
            seg[t0: t0 + len(x)] += x[: max(0, len(seg) - t0)]
        if mood in ("drive", "tense", "build"):   # soft low pulse on each beat
            for j in range(int(bar * 2 / beat)):
                t0 = int((c0 + j * beat) * SR); x = thump(ch[0] / 2 + 20, ch[0] / 2, 0.5, 0.10 * inten); seg[t0: t0 + len(x)] += x[: max(0, len(seg) - t0)]
    seg = seg[:n]
    if s_["id"] == "hook":   # rising build into liftoff, then silence for the liftoff itself
        lift = s_["lines"][3]["start"] - 1.7; seg *= np.clip(k / lift, 0.3, 1) * (1 - np.clip((k - lift + 0.1) / 0.2, 0, 1) * (k < lift + 1.6))
    fade = np.clip(k / 0.8, 0, 1) * np.clip((s_["dur"] - k) / 0.6, 0, 1); music[a0:a1] += seg * fade * (0.6 + 0.6 * inten)
# recorded score (CC BY tracks, when downloaded): one track per act, crossfaded at act changes, intensity per scene
ACTS = [("legends", ["hook"]), ("windswept", ["forces", "wing", "myth", "equation"]), ("unity", ["engine"]), ("stratosphere", ["cruise", "drag", "controls", "parts"]), ("windswept", ["stall"]), ("legends", ["landing"]), ("unity", ["recap", "end"])]
if all(os.path.exists(f"sfx/lib/music_{n}.wav") for n, _ in ACTS):
    TR = {n: loadwav(f"sfx/lib/music_{n}.wav") for n, _ in ACTS}; used = {n: 0.0 for n in TR}; rec = np.zeros(N, np.float32)
    for name, ids in ACTS:
        A = sc_by[ids[0]]["start"]; B = sc_by[ids[-1]]["start"] + sc_by[ids[-1]]["dur"]; x = TR[name]; x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9)
        off = used[name]; L = int((B - A + 3) * SR); src = loop(np.roll(x, -int(off * SR)), L, xf=2 * SR); used[name] = (off + B - A + 3) % (len(x) / SR)
        rec += window(src, A - 1.5, A - 1.5, B + 1.5, fi=1.5, fo=1.5)
    inten = np.zeros(N, np.float32)
    for s_ in scenes: inten[int(s_["start"] * SR): int((s_["start"] + s_["dur"]) * SR)] = 0.6 + 0.6 * MOOD[s_["id"]][0]
    hk = sc_by["hook"]; lift = hk["start"] + hk["lines"][3]["start"] - 1.7
    drop = 1 - np.clip((tt - lift + 0.1) / 0.2, 0, 1) * np.clip((lift + 1.7 - tt) / 0.3, 0, 1)                 # silence at the moment of liftoff
    gate = 1 - 0.9 * np.clip((tt - post0) / 1.0, 0, 1) * np.clip((post0 + ld["dur"] - ld["post"] - tt + 0.01) / 1.0, 0, 1)   # quiet at the gate
    music = lpf(inten, SR) * rec * drop * gate; MUSIC_SRC = "recorded"
else: MUSIC_SRC = "synth"
for name in ("hit",):        # timpani under the payoff hits
    for e_ in events:
        if e_["name"] == name: place(music, e_["t"], thump(68, 44, 1.6, 0.5) + lpf(noise(int(1.6 * SR)), 30) * np.exp(-np.arange(int(1.6 * SR)) / SR * 6) * 0.25)
music *= np.clip(tt / 1.5, 0, 1) * np.clip((total - tt) / 3, 0, 1)

# ---------------------------------------------------------------- mix: the voice always on top
envv = lpf(np.abs(voice), SR // 4); sp_ = np.clip(envv * 12, 0, 1)
hushv = np.zeros(N, np.float32)
for a_, b_ in hush: hushv = np.maximum(hushv, np.clip((tt - a_) / 0.3, 0, 1) * np.clip((b_ + 0.05 - tt) / 0.15, 0, 1))
vr = np.sqrt(np.mean(voice[np.abs(voice) > 0.02] ** 2))                    # speech RMS
def level(x, rel):            # scale x so its loud passages sit `rel` dB below speech
    e_ = np.sqrt(lpf(x * x, SR // 2) + 1e-12); p = np.percentile(e_[e_ > 1e-4], 95) if (e_ > 1e-4).any() else 1; return x * (vr * 10 ** (rel / 20) / p)
bed_l = level(bed, -9.0) + whine * 0.25 + wind
bed_mix = bed_l * (1 - 0.55 * sp_) * (1 - 0.85 * hushv)
mus_mix = level(music, -13.0) * (1 - 0.6 * sp_) * (1 - 0.92 * hushv)
sfx_mix = level(sfx, -4.0) * (1 - 0.3 * sp_)
mix = voice + bed_mix + mus_mix + sfx_mix
mix = np.tanh(mix * 1.2) / 1.2; mix *= 0.89 / np.abs(mix).max()   # soft limiter
def wr(name, x):
    st = np.clip(np.stack([x, x], 1)[: int(total * SR)], -1, 1); w = wave.open(name, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
os.makedirs("out", exist_ok=True); wr("out/audio_mix.wav", mix); wr("out/narration.wav", voice)
json.dump({"total": round(total, 3), "scenes": scenes, "events": events}, open("timings.json", "w"), indent=1)
print("music:", MUSIC_SRC); print("total", round(total, 1), "s;", " ".join(f"{s['id']}={s['dur']:.1f}" for s in scenes), "| events", len(events))
