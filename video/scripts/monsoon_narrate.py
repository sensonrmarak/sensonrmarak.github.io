"""Narration for the UPSC Animated monsoon video with the free Kokoro voice (bf_emma), one segment per scene.
   /tmp/claude-0/kvenv/bin/python scripts/monsoon_narrate.py   (model files in /tmp/claude-0/kokoro)
Writes public/monsoon/narration.wav and src/monsoon/narration.json (segment id, text, caption text, start, end)."""
import json, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = "/tmp/claude-0/kokoro"
# (id, spoken text, caption text if different, pause before in seconds)
SEG = [
 ("intro", "This lesson answers three questions about the Indian monsoon. What is it? Why does it happen? And how is it changing? The facts come from the India Meteorological Department, ISRO, and the Indian Institute of Tropical Meteorology.", None, 0.8),
 ("p1", "Part one. What is the monsoon?", None, 1.0),
 ("sw", "What is the southwest monsoon? It is a seasonal reversal of winds, from June to September. On I M D's normal dates, moist winds from the Indian Ocean reach Kerala around the first of June, and cover the whole country by about the eighth of July.",
  "What is the southwest monsoon? It is a seasonal reversal of winds, from June to September. On IMD's normal dates, moist winds from the Indian Ocean reach Kerala around the first of June, and cover the whole country by about the eighth of July.", 0.5),
 ("share", "Why does it matter so much? I M D data show this one season brings nearly three quarters of India's annual rainfall.",
  "Why does it matter so much? IMD data show this one season brings nearly three quarters of India's annual rainfall.", 0.5),
 ("arabian", "How does it spread across India? It arrives in two branches. The Arabian Sea branch strikes the Western Ghats, drenching the windward slopes, while the Deccan beyond lies in a rain shadow.", None, 0.6),
 ("bengal", "The Bay of Bengal branch soaks the northeast, then turns west along the Himalayas, across the Ganga plains.", None, 0.5),
 ("ne", "What is the northeast monsoon? It is the retreating phase, from October to December. The winds reverse, and blow from land to sea.", None, 0.7),
 ("tn", "Why does Tamil Nadu get rain in winter? These winds are mostly dry, but after crossing the Bay of Bengal they pick up moisture. I M D data show Tamil Nadu gets about forty-eight percent of its yearly rain in this season.",
  "Why does Tamil Nadu get rain in winter? These winds are mostly dry, but after crossing the Bay of Bengal they pick up moisture. IMD data show Tamil Nadu gets about 48% of its yearly rain in this season.", 0.5),
 ("p2", "Part two. Why does the monsoon happen?", None, 1.1),
 ("heat", "Why do the winds blow from sea to land? First, differential heating. In summer, the land heats up faster than the sea. Low pressure forms over northwest India, and high pressure over the Indian Ocean, so air rushes from sea to land.", None, 0.6),
 ("coriolis", "How do they turn southwest? Second, the Coriolis force. The southeast trade winds cross the equator, and are deflected to the right, turning into the southwest monsoon winds.", None, 0.6),
 ("itcz", "What is the monsoon trough? Third, the shifting I. T. C. Z. By July, the Inter-Tropical Convergence Zone moves north over the Ganga plains, as the monsoon trough.",
  "What is the monsoon trough? Third, the shifting ITCZ. By July, the Inter-Tropical Convergence Zone moves north over the Ganga plains, as the monsoon trough.", 0.6),
 ("jet", "How does the monsoon burst? Fourth, the jet streams and the Tibetan Plateau. The heated plateau helps push the westerly jet north of the Himalayas, and a tropical easterly jet sets up over the peninsula, triggering the burst of the monsoon.", None, 0.6),
 ("ocean", "How do the oceans change it? And fifth, the oceans. I M D tracks them closely. El Nino tends to weaken the monsoon, La Nina tends to strengthen it, and a positive Indian Ocean Dipole can help.",
  "How do the oceans change it? And fifth, the oceans. IMD tracks them closely. El Niño tends to weaken the monsoon, La Niña tends to strengthen it, and a positive Indian Ocean Dipole can help.", 0.6),
 ("p3", "Part three. How is the monsoon changing?", None, 1.1),
 ("lpa", "What counts as a normal monsoon? I M D compares each season with a long period average of eighty-seven centimetres, for nineteen seventy-one to twenty twenty. Totals still swing around it, but the way the rain falls is changing.",
  "What counts as a normal monsoon? IMD compares each season with a long period average of 87 cm, for 1971 to 2020. Totals still swing around it, but the way the rain falls is changing.", 0.5),
 ("extreme", "How is the rain changing? A study led by I I T M Pune found a threefold rise in widespread extreme rain events over central India from nineteen fifty to twenty fifteen, with fewer days of moderate rain, and longer dry breaks in between.",
  "How is the rain changing? A study led by IITM Pune found a threefold rise in widespread extreme rain events over central India from 1950 to 2015, with fewer days of moderate rain, and longer dry breaks in between.", 0.5),
 ("erratic", "What about its timing? Onset and withdrawal have become more erratic. I M D's normal date for withdrawal to begin is the seventeenth of September, but it is often late.",
  "What about its timing? Onset and withdrawal have become more erratic. IMD's normal date for withdrawal to begin is the 17th of September, but it is often late.", 0.5),
 ("cyclone", "Why are there more storms over the Arabian Sea? Because it is warming. An I I T M Pune study found that cyclones there rose by about fifty-two percent in two thousand one to twenty nineteen, compared with the previous two decades.",
  "Why are there more storms over the Arabian Sea? Because it is warming. An IITM Pune study found that cyclones there rose by about 52% in 2001 to 2019, compared with the previous two decades.", 0.5),
 ("track", "How does India track the monsoon? From space, I M D uses ISRO's weather satellites, insat three D, three D R, and the newest, three D S. On the ground, it uses Doppler weather radars and thousands of rain gauges. I M D issues its monsoon forecast in April, and updates it at the end of May.",
  "How does India track the monsoon? From space, IMD uses ISRO's weather satellites, INSAT-3D, 3DR, and the newest, 3DS. On the ground, it uses Doppler weather radars and thousands of rain gauges. IMD issues its monsoon forecast in April, and updates it at the end of May.", 0.5),
 ("impact", "Why does this matter? For farmers, cities and reservoirs, it means more floods, and more droughts, sometimes in the same season.", None, 0.5),
 ("outro", "So: what, why, and how. What: the monsoon is a seasonal reversal of winds. Why: it is driven by heat, by Earth's spin, and by the oceans. How it is changing: a warming climate is making it more extreme.", None, 0.9),
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
