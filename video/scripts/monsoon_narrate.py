"""Narration for the UPSC Animated monsoon video with the free Kokoro voice (bf_emma), one segment per scene.
   /tmp/claude-0/kvenv/bin/python scripts/monsoon_narrate.py   (model files in /tmp/claude-0/kokoro)
Writes public/monsoon/narration.wav and src/monsoon/narration.json (segment id, text, caption text, start, end)."""
import json, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = "/tmp/claude-0/kokoro"
# (id, spoken text, caption text if different, pause before in seconds)
SEG = [
 ("intro", "The Indian monsoon, in three parts: its two phases, what drives it, and how it is changing.", None, 0.8),
 ("p1", "Part one: the two phases.", None, 1.0),
 ("sw", "The first is the southwest monsoon, from June to September. Moist winds from the Indian Ocean reach Kerala around the first of June, and cover the whole country by about the eighth of July.", None, 0.5),
 ("share", "This one season brings nearly three quarters of India's annual rainfall.", None, 0.5),
 ("arabian", "It arrives in two branches. The Arabian Sea branch strikes the Western Ghats, drenching the windward slopes, while the Deccan beyond lies in a rain shadow.", None, 0.6),
 ("bengal", "The Bay of Bengal branch soaks the northeast, then turns west along the Himalayas, across the Ganga plains.", None, 0.5),
 ("ne", "The second phase is the northeast, or retreating, monsoon, from October to December. The winds reverse, and blow from land to sea.", None, 0.7),
 ("tn", "They are mostly dry, but after crossing the Bay of Bengal they bring rain to the Tamil Nadu coast, which gets about half of its yearly rain in this season.", None, 0.5),
 ("p2", "Part two: the core drivers.", None, 1.1),
 ("heat", "First, differential heating. In summer, the land heats up faster than the sea. Low pressure forms over northwest India, and high pressure over the Indian Ocean, so air rushes from sea to land.", None, 0.6),
 ("coriolis", "Second, the Coriolis force. The southeast trade winds cross the equator, and are deflected to the right, turning into the southwest monsoon winds.", None, 0.6),
 ("itcz", "Third, the shifting I. T. C. Z. By July, the Inter-Tropical Convergence Zone moves north over the Ganga plains, as the monsoon trough.",
  "Third, the shifting ITCZ. By July, the Inter-Tropical Convergence Zone moves north over the Ganga plains, as the monsoon trough.", 0.6),
 ("jet", "Fourth, the jet streams and the Tibetan Plateau. The heated plateau helps push the westerly jet north of the Himalayas, and a tropical easterly jet sets up over the peninsula, triggering the burst of the monsoon.", None, 0.6),
 ("ocean", "And fifth, the oceans. El Nino tends to weaken the monsoon, La Nina tends to strengthen it, and a positive Indian Ocean Dipole can help.",
  "And fifth, the oceans. El Niño tends to weaken the monsoon, La Niña tends to strengthen it, and a positive Indian Ocean Dipole can help.", 0.6),
 ("p3", "Part three: recent shifts and climate change.", None, 1.1),
 ("lpa", "Season totals still swing around a long period average of eighty-seven centimetres, but the way the rain falls is changing.",
  "Season totals still swing around a long period average of 87 cm, but the way the rain falls is changing.", 0.5),
 ("extreme", "Studies show fewer days of moderate rain, and a sharp rise in extreme downpours over central India, with longer dry breaks in between.", None, 0.5),
 ("erratic", "Onset and withdrawal have become more erratic, and withdrawal is often late.", None, 0.5),
 ("cyclone", "And a warming Arabian Sea is fuelling more frequent and more intense cyclones.", None, 0.5),
 ("impact", "For farmers, cities and reservoirs, this means more floods, and more droughts, sometimes in the same season.", None, 0.5),
 ("outro", "Remember: the monsoon is a seasonal reversal of winds, driven by heat, by Earth's spin, and by the oceans. And a warming climate is making it more extreme.", None, 0.9),
]
VOICE, SPEED = os.environ.get("VOICE", "bf_emma"), float(os.environ.get("SPEED", "0.84"))
EXTRA_PAUSE = float(os.environ.get("EXTRA_PAUSE", "0.7"))   # added breathing room between scenes
k = Kokoro(f"{K}/model.onnx", f"{K}/voices.npz")
sr, parts, meta, t = 24000, [], [], 0.0
for sid, text, cap, pause in SEG:
    pause += EXTRA_PAUSE * (1.6 if sid in ("p1", "p2", "p3") else 1.0)
    parts.append(np.zeros(int(pause * sr), np.float32)); t += pause
    a, sr = k.create(text, voice=VOICE, speed=SPEED, lang="en-gb", sentence_pause=0.55, clause_pause=0.18)
    parts.append(a.astype(np.float32))
    meta.append({"id": sid, "speak": text, "text": cap or text, "start": round(t, 3), "end": round(t + len(a) / sr, 3)})
    t += len(a) / sr
    print(f"{sid:9s} {meta[-1]['start']:7.2f} {meta[-1]['end']:7.2f}")
parts.append(np.zeros(int(1.8 * sr), np.float32)); t += 1.8
audio = np.concatenate(parts); audio = audio / np.abs(audio).max() * 0.9
sf.write(os.path.join(ROOT, "public/monsoon/narration.wav"), audio, sr)
json.dump({"total": round(t, 3), "voice": VOICE, "segments": meta}, open(os.path.join(ROOT, "src/monsoon/narration.json"), "w"), indent=1)
print("total", round(t, 2))
