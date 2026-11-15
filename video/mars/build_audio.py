"""Cold open of the Mars video: narration (Kokoro 'am_fenrir', speed 0.975), space sound design and score.
Writes out/audio_mix.wav and timings.json (line starts, word marks, effect cues)."""
import json, os, wave
import numpy as np
from kokoro_onnx import Kokoro

SR = 48000; GAP = 0.32; LEAD = 1.6; TAIL = 2.4
K = Kokoro("/tmp/kokoro/kokoro-v1.0.onnx", "/tmp/kokoro/voices-v1.0.bin")
rng = np.random.default_rng(7)
script = json.load(open("script.json"))

def synth(text):
    x, sr = K.create(text, voice="am_fenrir", speed=0.975, lang="en-us")
    x = np.asarray(x, dtype=np.float32); n = int(len(x) * SR / sr)
    a = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
    nz = np.where(np.abs(a) > 0.01)[0]
    return a[max(0, nz[0] - 480): nz[-1] + 2400] if len(nz) else a

t = 0.0; chunks = []; scenes = []; events = []
for sc in script:
    s0 = t; t += LEAD; lines = []
    for ln in sc["lines"]:
        a = synth(ln["t"]); chunks.append((t, a)); d = len(a) / SR
        marks = {k: round(len(synth(v)) / SR, 3) for k, v in ln.get("marks", {}).items()}
        lines.append({"text": ln["t"], "start": round(t - s0, 3), "end": round(t - s0 + d, 3), "marks": marks})
        for name, off in ln.get("sfx", []): events.append({"name": name, "t": round(t + off, 3)})
        t += d + GAP + ln.get("pause", 0)
    t += TAIL
    scenes.append({"id": sc["id"], "start": round(s0, 3), "dur": round(t - s0, 3), "lines": lines})
total = t; N = int(total * SR) + SR; tt = np.arange(N) / SR
voice = np.zeros(N, np.float32)
for st, a in chunks: voice[int(st * SR): int(st * SR) + len(a)] += a
voice /= np.abs(voice).max() / 0.9

def lpf(x, k):
    if k <= 1: return x
    c = np.cumsum(np.concatenate([[0.0], x]).astype(np.float64)); return np.pad((c[k:] - c[:-k]) / k, (k - 1, 0)).astype(np.float32)
def noise(n): return rng.standard_normal(n).astype(np.float32)
def place(buf, at, x, g=1.0):
    i = int(at * SR); j = min(len(buf), i + len(x)); buf[i:j] += x[: j - i] * g
def thump(f0, f1, d, g=1.0):
    n = int(d * SR); k = np.arange(n) / SR; f = f1 + (f0 - f1) * np.exp(-k * 9); return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-k * 4) * g).astype(np.float32)
def env(n, a, r): e = np.ones(n, np.float32); A, R = int(a * SR), int(r * SR); e[:A] = np.linspace(0, 1, A) if A else 1; e[n - R:] *= np.linspace(1, 0, R) if R else 1; return e
L = scenes[0]["lines"]; at = lambda i, off=0.0: L[i]["start"] + off

# ---- sound design
sfx = np.zeros(N, np.float32)
drone = lpf(noise(N), 400) * 6 + np.sin(2 * np.pi * 41.2 * tt) * 0.25 + np.sin(2 * np.pi * 61.7 * tt) * 0.12
sfx += drone * 0.35 * np.clip(tt / 3, 0, 1)
b0, b1 = at(2, 2.6), at(4, 2.2)                                  # the engine burn: from "fire its engine" to "forever"
burn = lpf(noise(N), 18) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * tt)) * 1.4
sfx += burn * np.clip((tt - b0) / 0.6, 0, 1) * np.clip((b1 - tt) / 0.4, 0, 1)
for i in range(6):                                                # radio blips crossing the gap
    k = at(3, 0.3) + i * 0.55; n = int(0.09 * SR); place(sfx, k, (np.sin(2 * np.pi * 1760 * np.arange(n) / SR) * env(n, 0.005, 0.04) * 0.10).astype(np.float32))
for e in events:
    if e["name"] == "success":
        for f, dt in ((523.25, 0), (659.25, 0.12), (783.99, 0.24), (1046.5, 0.38)):
            n = int(2.2 * SR); k = np.arange(n) / SR; place(sfx, e["t"] + dt, (np.sin(2 * np.pi * f * k) * np.exp(-k * 1.5) * env(n, 0.01, 0.4) * 0.07).astype(np.float32))
    if e["name"] == "hit": place(sfx, e["t"], thump(70, 30, 2.0, 1.0)); place(sfx, e["t"], lpf(noise(int(1.5 * SR)), 40) * np.exp(-np.arange(int(1.5 * SR)) / SR * 4) * 0.4)

# ---- score: low strings that tense up during the burn and open into a major chord when it works
mus = np.zeros(N, np.float32)
def pad(fs, a, b, g):
    n = int((b - a) * SR); k = np.arange(n) / SR; x = np.zeros(n, np.float32)
    for f in fs:
        for det in (-0.004, 0.0, 0.005):
            for m in range(1, 6): x += np.sin(2 * np.pi * f * (1 + det) * m * k + m) / m
    place(mus, a, lpf(x, 24) * env(n, 1.5, 1.5) * g)
win = at(5)
pad([55.0, 82.4, 110.0, 130.8], 0.5, b0 + 0.5, 0.010)              # A minor, patient
pad([51.9, 77.8, 103.8, 123.5], b0, win - 0.3, 0.013)              # tension during the burn (G# diminished colour)
pad([65.4, 98.0, 130.8, 164.8, 196.0], win, total, 0.014)          # C major: it worked
hush = np.clip((tt - (at(4, 2.4))) / 0.3, 0, 1) * np.clip((win - tt) / 0.2, 0, 1)   # near silence before "It works."

envv = lpf(np.abs(voice), SR // 4); sp = np.clip(envv * 12, 0, 1)
vr = np.sqrt(np.mean(voice[np.abs(voice) > 0.02] ** 2))
def level(x, rel): e_ = np.sqrt(lpf(x * x, SR // 2) + 1e-12); return x * (vr * 10 ** (rel / 20) / np.percentile(e_, 95))
mix = voice + level(sfx, -10) * (1 - 0.5 * sp) * (1 - 0.85 * hush) + level(mus, -12) * (1 - 0.55 * sp) * (1 - 0.95 * hush)
mix = np.tanh(mix * 1.2) / 1.2; mix *= 0.89 / np.abs(mix).max()
st = np.clip(np.stack([mix, mix], 1)[: int(total * SR)], -1, 1); os.makedirs("out", exist_ok=True)
w = wave.open("out/audio_mix.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
json.dump({"total": round(total, 3), "scenes": scenes, "events": events, "burn": [round(b0, 3), round(b1, 3)]}, open("timings.json", "w"), indent=1)
print("total", round(total, 2), [(l["start"], l["end"]) for l in L])
