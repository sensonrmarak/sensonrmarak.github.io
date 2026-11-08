"""Soundtrack for the seasons video: Kokoro narration + soft music-box bed (ducked) + chimes at parts + light rain in rainy scenes.
   python3 scripts/build_monsoon_audio.py"""
import json, os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_moss_audio as b
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tl = json.load(open(os.path.join(ROOT, "src/seasons2/narration.json")))
TOTAL = tl["total"]; n = b.t2i(TOTAL)
narr = b.load_narration(os.path.join(ROOT, "public/seasons2/narration.wav"))
music = np.zeros((2, n)); sfx = np.zeros((2, n))
beat, prog = 60 / 80, [(50, [62, 65, 69]), (46, [58, 62, 65]), (53, [65, 69, 72]), (48, [60, 64, 67])]   # Dm Bb F C
k = 0
while k * beat < TOTAL - 1:
    t = k * beat; root, ch = prog[(k // 4) % 4]; pos = k % 4
    b.add(music, b.music_box(ch[pos % 3] + 12, 2.0), t, 0.13, -0.3 + 0.2 * pos)
    if pos == 0: b.add(music, b.pad([root] + ch, beat * 4 + 0.4), t, 0.2)
    k += 1
S = {s["id"]: s for s in tl["segments"]}
for sid in ("intro", "p1", "p2", "p3", "p4", "outro"): b.add(sfx, b.chime_run(), S[sid]["start"] - 0.5, 0.3)
def rain(dur):
    m = b.t2i(dur); x = b.bandpass(b.rng.standard_normal(m), 1500, 7000); t = np.arange(m) / b.SR
    e = np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.0)
    return x / np.abs(x).max() * np.clip(e, 0, 1)
for sid in ("eqzone", "rainforest"):
    s = S[sid]; b.add(sfx, rain(s["end"] - s["start"] + 1.0), s["start"] - 0.3, 0.05)
nt = np.zeros(n); nt[:min(n, len(narr))] = narr[:n]
env = np.convolve(np.abs(nt), np.ones(b.t2i(0.3)) / b.t2i(0.3), mode="same")
out = (music * (1 - 0.6 * np.clip(env / 0.04, 0, 1)) + sfx) * 0.8
out[0] += nt; out[1] += nt
out *= np.clip((TOTAL - np.arange(n) / b.SR) / 1.5, 0, 1)
out = out / max(1.0, np.abs(out).max() / 0.95)
with wave.open(os.path.join(ROOT, "public/seasons2/soundtrack.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(b.SR); w.writeframes((out.T * 32767).astype("<i2").tobytes())
print("ok", TOTAL)
