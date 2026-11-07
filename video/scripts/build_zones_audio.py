"""Soundtrack for the Seasons and Heat Zones lesson video: Lily's narration over a soft music-box bed (ducked), chimes at sections.
    python3 scripts/build_zones_audio.py ../assets-src/zones_lesson_narration_lily.mp3"""
import json, os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_moss_audio as b

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOTAL = 127.5
tl = json.load(open(os.path.join(ROOT, "src/zones/timeline.json")))
narr = b.load_narration(sys.argv[1]); narr = narr / np.abs(narr).max() * 0.9
n = b.t2i(TOTAL)
music = np.zeros((2, n)); sfx = np.zeros((2, n))
beat, prog = 60 / 76, [(53, [65, 69, 72]), (50, [62, 65, 69]), (46, [58, 62, 65]), (48, [60, 64, 67])]
k = 0
while k * beat < TOTAL - 1:
    t = k * beat; root, ch = prog[(k // 3) % 4]; pos = k % 3
    b.add(music, b.music_box(ch[pos] + 12, 2.2), t, 0.16, -0.3 + 0.3 * pos)
    if pos == 0: b.add(music, b.pad([root] + ch, beat * 3 + 0.4), t, 0.22)
    k += 1
for t in (0.2, tl["segments"][5]["start"] - 0.4, tl["segments"][8]["start"] - 0.4):
    b.add(sfx, b.chime_run(), t, 0.35)
b.add(sfx, b.chime_run((77, 81, 84, 89, 93), 0.12), tl["segments"][9]["start"] - 0.3, 0.4)
nt = np.zeros(n); nt[:min(n, len(narr))] = narr[:n]
env = np.convolve(np.abs(nt), np.ones(b.t2i(0.3)) / b.t2i(0.3), mode="same")
duck = 1 - 0.6 * np.clip(env / 0.04, 0, 1)
out = (music * duck + sfx) * 0.8
out[0] += nt; out[1] += nt
out *= np.clip((TOTAL - np.arange(n) / b.SR) / 2.5, 0, 1)
out = out / max(1.0, np.abs(out).max() / 0.95)
os.makedirs(os.path.join(ROOT, "public/zones"), exist_ok=True)
with wave.open(os.path.join(ROOT, "public/zones/soundtrack.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(b.SR); w.writeframes((out.T * 32767).astype("<i2").tobytes())
print("ok", TOTAL)
