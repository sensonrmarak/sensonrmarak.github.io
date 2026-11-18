"""Main film after the cold open: narration (Kokoro 'am_fenrir', speed 0.975), sound design and score.
Writes out/audio_mix.wav and timings.json (scene and line starts, word marks, effect cues)."""
import json, os, wave
import numpy as np
from kokoro_onnx import Kokoro

SR = 48000; GAP = 0.34; LEAD = 1.9; TAIL = 1.6
K = Kokoro("/tmp/kokoro/kokoro-v1.0.onnx", "/tmp/kokoro/voices-v1.0.bin")
rng = np.random.default_rng(23)
script = json.load(open("script.json"))

def synth(text):
    x, sr = K.create(text, voice="am_fenrir", speed=0.975, lang="en-us")
    x = np.asarray(x, dtype=np.float32); n = int(len(x) * SR / sr)
    a = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
    nz = np.where(np.abs(a) > 0.01)[0]
    return a[max(0, nz[0] - 480): nz[-1] + 2400] if len(nz) else a

t = 0.6; chunks = []; scenes = []; events = []
for sc in script:
    s0 = t; t += LEAD; lines = []
    for ln in sc["lines"]:
        a = synth(ln["t"]); chunks.append((t, a)); d = len(a) / SR
        marks = {k: round(len(synth(v)) / SR, 3) for k, v in ln.get("marks", {}).items()}
        lines.append({"text": ln["t"], "start": round(t - s0, 3), "end": round(t - s0 + d, 3), "marks": marks})
        for name, off in ln.get("sfx", []): events.append({"name": name, "t": round(t + off, 3), "scene": sc["id"]})
        t += d + GAP + ln.get("pause", 0)
    t += TAIL + (5.5 if sc["id"] == "end" else 0)
    events.append({"name": "whoosh_in", "t": round(s0, 3), "scene": sc["id"]})
    scenes.append({"id": sc["id"], "title": sc["title"], "start": round(s0, 3), "dur": round(t - s0, 3), "lines": lines})
total = t; N = int(total * SR) + SR; tt = np.arange(N) / SR
voice = np.zeros(N, np.float32)
for st, a in chunks: voice[int(st * SR): int(st * SR) + len(a)] += a
voice /= np.abs(voice).max() / 0.9

def lpf(x, k):
    if k <= 1: return x
    c = np.cumsum(np.concatenate([[0.0], x]).astype(np.float64)); return np.pad((c[k:] - c[:-k]) / k, (k - 1, 0)).astype(np.float32)
def noise(n): return rng.standard_normal(n).astype(np.float32)
def place(buf, at, x, g=1.0):
    i = int(at * SR)
    if i < 0: x = x[-i:]; i = 0
    j = min(len(buf), i + len(x)); buf[i:j] += x[: j - i] * g
def env(n, a, r): e = np.ones(n, np.float32); A, R = int(a * SR), int(r * SR); e[:A] = np.linspace(0, 1, A) if A else 1; e[n - R:] *= np.linspace(1, 0, R) if R else 1; return e
def thump(f0, f1, d, g=1.0):
    n = int(d * SR); k = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-k * 9); return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-k * 4) * g).astype(np.float32)
def tone(f, d, dec=3.0): n = int(d * SR); k = np.arange(n) / SR; return (np.sin(2 * np.pi * f * k) * np.exp(-k * dec) * env(n, 0.005, 0.05)).astype(np.float32)
def sweep(d, k0, k1, g):
    n = int(d * SR); x = noise(n); out = np.zeros(n, np.float32)
    for s in range(20): a, b = s * n // 20, (s + 1) * n // 20; out[a:b] = lpf(x, max(1, int(k0 + (k1 - k0) * s / 19)))[a:b]
    return out * np.sin(np.linspace(0, np.pi, n)) ** 2 * g
def loadwav(p): w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
FLY = loadwav("../flight4/sfx/lib/flyby.wav"); FLY /= np.abs(FLY).max()   # InspectorJ, CC BY 4.0 (credited)

sfx = np.zeros(N, np.float32)
sfx += (lpf(noise(N), 500) * 6 + np.sin(2 * np.pi * 41.2 * tt) * 0.2) * 0.25                      # deep-space bed
for e in events:
    n_, at = e["name"], e["t"]
    if n_ == "whoosh_in": place(sfx, at - 0.3, sweep(0.7, 40, 3, 0.35))
    elif n_ == "whoosh": place(sfx, at - 0.4, sweep(1.2, 50, 2, 0.6))
    elif n_ == "stamp": place(sfx, at, thump(90, 40, 0.5, 0.8))
    elif n_ == "clunk": place(sfx, at, thump(130, 60, 0.35, 0.6))
    elif n_ == "tick":
        for i in range(8): place(sfx, at + i * 0.5, tone(1800 if i % 2 else 1400, 0.06, 40) * 0.12)
    elif n_ == "fail":
        for i in range(3): place(sfx, at + i * 0.9, thump(60, 30, 1.0, 0.7)); place(sfx, at + i * 0.9, lpf(noise(int(0.8 * SR)), 3) * np.exp(-np.arange(int(0.8 * SR)) / SR * 5) * 0.3)
    elif n_ == "launch":
        seg = FLY[int(9 * SR): int(24 * SR)].copy(); seg = lpf(seg, 3) * 1.4; place(sfx, at - 0.5, seg * env(len(seg), 1.0, 4.0))
        place(sfx, at, thump(45, 25, 3.0, 1.0))
    elif n_ == "burn":
        n = int(3.5 * SR); b = lpf(noise(n), 16) * (0.7 + 0.3 * np.sin(2 * np.pi * 7 * np.arange(n) / SR)) * env(n, 0.3, 0.8) * 0.9; place(sfx, at, b)
    elif n_ == "alarm":
        for i in range(4): place(sfx, at + i * 0.34, tone(880 if i % 2 == 0 else 660, 0.3, 2) * 0.14)
    elif n_ == "success":
        for f, dt in ((523.25, 0), (659.25, 0.12), (783.99, 0.24), (1046.5, 0.38)): place(sfx, at + dt, tone(f, 2.0, 1.5) * 0.08)
    elif n_ == "hit": place(sfx, at, thump(70, 30, 2.0, 1.0)); place(sfx, at, lpf(noise(int(1.4 * SR)), 40) * np.exp(-np.arange(int(1.4 * SR)) / SR * 4) * 0.35)
    elif n_ == "click":
        n = int(0.05 * SR); k = np.arange(n) / SR; place(sfx, at, (lpf(noise(n), 2) * np.exp(-k * 160) * 0.5 + np.sin(2 * np.pi * 2400 * k) * np.exp(-k * 220) * 0.25).astype(np.float32))
    elif n_ == "pop":
        n = int(0.18 * SR); k = np.arange(n) / SR; f = 500 + 900 * (1 - np.exp(-k * 30)); place(sfx, at, (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-k * 18) * 0.22).astype(np.float32))
    elif n_ == "bell":
        for f, g in ((1318.5, 0.10), (1975.5, 0.05), (2637.0, 0.03)):
            for i in range(3): place(sfx, at + i * 0.16, tone(f, 1.6, 2.6) * g * (1 - i * 0.25))
    elif n_ == "horn":
        for dt in (0, 0.32):
            n = int(0.24 * SR); k = np.arange(n) / SR; x = (np.sign(np.sin(2 * np.pi * 420 * k)) * 0.5 + np.sign(np.sin(2 * np.pi * 530 * k)) * 0.5) * env(n, 0.01, 0.04); place(sfx, at + dt, lpf(x.astype(np.float32), 6) * 0.10)

# score: soft strings whose colour follows the story
mus = np.zeros(N, np.float32)
CH = {"curious": [55.0, 82.4, 110.0, 130.8], "drive": [65.4, 98.0, 130.8, 164.8], "tense": [51.9, 77.8, 103.8, 123.5], "warm": [73.4, 110.0, 146.8, 185.0], "bright": [65.4, 98.0, 130.8, 164.8, 196.0]}
MOOD = {"hard": "curious", "first": "tense", "clock": "tense", "rocket": "drive", "small": "curious", "people": "warm", "nearly": "tense", "maven": "curious", "payoff": "bright", "meaning": "warm", "end": "bright"}
def pad(fs, a, b, g):
    n = int((b - a) * SR); k = np.arange(n) / SR; x = np.zeros(n, np.float32)
    for f in fs:
        for det in (-0.004, 0.0, 0.005):
            for m in range(1, 6): x += np.sin(2 * np.pi * f * (1 + det) * m * k + m) / m
    place(mus, a, lpf(x, 24) * env(n, 1.5, 1.5) * g)
for s in scenes: pad(CH[MOOD[s["id"]]], max(0, s["start"] - 0.8), s["start"] + s["dur"] + 0.8, 0.011)

envv = lpf(np.abs(voice), SR // 4); sp = np.clip(envv * 12, 0, 1)
vr = np.sqrt(np.mean(voice[np.abs(voice) > 0.02] ** 2))
def level(x, rel): e_ = np.sqrt(lpf(x * x, SR // 2) + 1e-12); return x * (vr * 10 ** (rel / 20) / np.percentile(e_, 95))
mix = voice + level(sfx, -10) * (1 - 0.5 * sp) + level(mus, -12) * (1 - 0.55 * sp)
mix = np.tanh(mix * 1.2) / 1.2; mix *= 0.89 / np.abs(mix).max()
st = np.clip(np.stack([mix, mix], 1)[: int(total * SR)], -1, 1); os.makedirs("out", exist_ok=True)
w = wave.open("out/audio_mix.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
json.dump({"total": round(total, 3), "scenes": scenes, "events": events}, open("timings.json", "w"), indent=1)
print("total", round(total, 1), "s;", " ".join(f"{s['id']}={s['dur']:.1f}" for s in scenes))
