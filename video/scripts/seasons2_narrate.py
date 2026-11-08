"""Narration for the UPSC Animated monsoon video with the free Kokoro voice (bf_emma), one segment per scene.
   /tmp/claude-0/kvenv/bin/python scripts/monsoon_narrate.py   (model files in /tmp/claude-0/kokoro)
Writes public/monsoon/narration.wav and src/monsoon/narration.json (segment id, text, caption text, start, end)."""
import json, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = "/tmp/claude-0/kokoro"
# (id, spoken text, caption text if different, pause before in seconds)
SEG = [
 ("intro", "This lesson answers three questions. What are the imaginary lines, the solstices and the equinoxes? Why do we have seasons, and why do climates differ? And how do they shape our weather and forests? Let's build the answers, step by step.", None, 0.8),
 ("p1", "Part one. What are the imaginary lines?", None, 1.0),
 ("lat", "What is latitude? To locate any place on Earth, we use a grid of imaginary lines. Lines of latitude, or parallels, run east to west. They are measured from zero degrees at the Equator, to ninety degrees at each pole.", None, 0.5),
 ("lon", "What is longitude? Lines of longitude, or meridians, run from pole to pole. They are measured from zero degrees at Greenwich, the Prime Meridian, to one hundred and eighty degrees east and west.", None, 0.5),
 ("equator", "What makes the Equator special? It is the longest parallel. NASA puts Earth's equatorial circumference at about forty thousand and seventy-five kilometres. It divides Earth into the Northern and Southern Hemispheres.",
  "What makes the Equator special? It is the longest parallel. NASA puts Earth's equatorial circumference at about 40,075 km. It divides Earth into the Northern and Southern Hemispheres.", 0.5),
 ("parallels", "Why are some parallels special? The Tropic of Cancer lies at twenty-three and a half degrees north, and the Tropic of Capricorn at twenty-three and a half degrees south. They are the limits where the Sun can be directly overhead. The Arctic and Antarctic Circles, at sixty-six and a half degrees, are the limits of the midnight Sun. All four are fixed by Earth's tilt.",
  "Why are some parallels special? The Tropic of Cancer lies at 23.5° N, and the Tropic of Capricorn at 23.5° S. They are the limits where the Sun can be directly overhead. The Arctic and Antarctic Circles, at 66.5°, are the limits of the midnight Sun. All four are fixed by Earth's tilt.", 0.5),
 ("india", "Where does the Tropic of Cancer cross India? Survey of India maps show it passing through eight states: Gujarat, Rajasthan, Madhya Pradesh, Chhattisgarh, Jharkhand, West Bengal, Tripura, and Mizoram.", None, 0.5),
 ("time", "How does longitude set our clocks? Earth turns three hundred and sixty degrees in twenty-four hours: fifteen degrees every hour, or one degree every four minutes. Indian Standard Time, kept by the C S I R National Physical Laboratory, is taken from eighty-two and a half degrees east, near Mirzapur, five and a half hours ahead of Greenwich.",
  "How does longitude set our clocks? Earth turns 360° in 24 hours: 15° every hour, or 1° every 4 minutes. Indian Standard Time, kept by the CSIR National Physical Laboratory, is taken from 82.5° E, near Mirzapur, 5 and a half hours ahead of Greenwich.", 0.5),
 ("p2", "Part two. Why do we have seasons?", None, 1.0),
 ("tilt", "What is Earth's tilt? NASA gives the axis a tilt of about twenty-three and a half degrees from the vertical, so it makes an angle of sixty-six and a half degrees with the plane of its orbit. And it always points the same way, towards the Pole Star.",
  "What is Earth's tilt? NASA gives the axis a tilt of about 23.5° from the vertical, so it makes an angle of 66.5° with the plane of its orbit. And it always points the same way, towards the Pole Star.", 0.5),
 ("orbit", "How does the orbit create seasons? Earth goes round the Sun once in about three hundred and sixty-five and a quarter days. Because the axis keeps pointing the same way, first one hemisphere, and then the other, leans towards the Sun. That is what makes the seasons.",
  "How does the orbit create seasons? Earth goes round the Sun once in about 365 and a quarter days. Because the axis keeps pointing the same way, first one hemisphere, and then the other, leans towards the Sun. That is what makes the seasons.", 0.5),
 ("distance", "Why is it not about distance? NASA's data show Earth is closest to the Sun in early January, about one hundred and forty-seven million kilometres away, and farthest in early July, about one hundred and fifty-two million kilometres. Yet January is winter in India.",
  "Why is it not about distance? NASA's data show Earth is closest to the Sun in early January, about 147 million km away, and farthest in early July, about 152 million km. Yet January is winter in India.", 0.5),
 ("p3", "Part three. What are solstices and equinoxes, and how do they affect us?", None, 1.0),
 ("june", "What happens at the summer solstice? Around the twenty-first of June, the Sun is directly overhead at the Tropic of Cancer. It is the longest day in the Northern Hemisphere. Delhi gets about fourteen hours of daylight, and beyond the Arctic Circle, the Sun does not set at all.",
  "What happens at the summer solstice? Around the 21st of June, the Sun is directly overhead at the Tropic of Cancer. It is the longest day in the Northern Hemisphere. Delhi gets about 14 hours of daylight, and beyond the Arctic Circle, the Sun does not set at all.", 0.5),
 ("dec", "What happens at the winter solstice? Around the twenty-second of December, the Sun is overhead at the Tropic of Capricorn. Delhi's day shrinks to about ten hours, the Arctic has polar night, and the Southern Hemisphere has its summer.",
  "What happens at the winter solstice? Around the 22nd of December, the Sun is overhead at the Tropic of Capricorn. Delhi's day shrinks to about 10 hours, the Arctic has polar night, and the Southern Hemisphere has its summer.", 0.5),
 ("equinox", "And what is an equinox? Around the twenty-first of March and the twenty-third of September, the Sun is overhead at the Equator. These are the equinoxes, when day and night are nearly equal everywhere.",
  "And what is an equinox? Around the 21st of March and the 23rd of September, the Sun is overhead at the Equator. These are the equinoxes, when day and night are nearly equal everywhere.", 0.5),
 ("noon", "How do the solstices change the heat we feel? At noon on the June solstice, the Sun stands about eighty-five degrees high over Delhi. On the December solstice, it is only about thirty-eight degrees high. Low sunlight spreads over more ground, and heats it far less.",
  "How do the solstices change the heat we feel? At noon on the June solstice, the Sun stands about 85° high over Delhi. On the December solstice, it is only about 38° high. Low sunlight spreads over more ground, and heats it far less.", 0.5),
 ("p4", "Part four. Why do climates and forests differ?", None, 1.0),
 ("eqzone", "Why is the Equator hot and wet all year? Here the Sun is high in every season, and days stay close to twelve hours. Hot, moist air rises every afternoon, cools, and brings convectional rain almost daily. Temperatures stay around twenty-seven degrees Celsius, and rainfall often exceeds two thousand millimetres a year.",
  "Why is the Equator hot and wet all year? Here the Sun is high in every season, and days stay close to 12 hours. Hot, moist air rises every afternoon, cools, and brings convectional rain almost daily. Temperatures stay around 27 °C, and rainfall often exceeds 2,000 mm a year.", 0.5),
 ("rainforest", "How does this shape the forests? It supports tropical evergreen rainforests, with tall, multi-layered canopies of trees like mahogany, ebony and rosewood. Think of the Amazon, the Congo basin, and in India, the Western Ghats and the Andaman and Nicobar Islands.", None, 0.5),
 ("tropics", "Why do deserts lie near the tropics? The air that rose at the Equator flows away high up, and sinks back down near the Tropics of Cancer and Capricorn. Sinking air is dry, and stops clouds from forming. That is why the world's great hot deserts lie near the tropics: the Sahara, the Arabian, India's Thar, the Kalahari, the Atacama, and the Australian deserts.", None, 0.5),
 ("desert", "How do desert plants survive? They are thorny and drought-resistant: acacia, cactus, and in the Thar, khejri and babool, with long roots and small, waxy leaves to save water.", None, 0.5),
 ("india2", "What forests does India have? Most of India lies in between, where the monsoon brings seasonal rain. So its most widespread forests are tropical deciduous, with trees like teak and sal that shed their leaves in the dry season. The Forest Survey of India's latest report, for twenty twenty-three, puts forest cover at about twenty-one point seven six percent of India's area.",
  "What forests does India have? Most of India lies in between, where the monsoon brings seasonal rain. So its most widespread forests are tropical deciduous, with trees like teak and sal that shed their leaves in the dry season. The Forest Survey of India's latest report, for 2023, puts forest cover at about 21.76% of India's area.", 0.5),
 ("poles", "How does vegetation change towards the poles? Further from the Equator, the Sun sits lower. The temperate zones grow deciduous and coniferous forests, like oak, pine and deodar, and the frigid zones have only tundra: mosses and lichens.", None, 0.5),
 ("outro", "So: what, why, and how. What: imaginary lines locate places and set time. Why: Earth's tilt creates the solstices and the seasons. How: latitude, through the Sun's angle and the movement of air, decides climate and forests.", None, 0.9),
]
VOICE, SPEED = os.environ.get("VOICE", "bf_emma"), float(os.environ.get("SPEED", "0.84"))
EXTRA_PAUSE = float(os.environ.get("EXTRA_PAUSE", "0.7"))   # added breathing room between scenes
k = Kokoro(f"{K}/model.onnx", f"{K}/voices.npz")
sr, parts, meta, t = 24000, [], [], 0.0
for sid, text, cap, pause in SEG:
    pause += EXTRA_PAUSE * (1.6 if sid in ("p1", "p2", "p3", "p4") else 1.0)
    parts.append(np.zeros(int(pause * sr), np.float32)); t += pause
    a, sr = k.create(text, voice=VOICE, speed=SPEED, lang="en-gb", sentence_pause=0.55, clause_pause=0.18)
    parts.append(a.astype(np.float32))
    meta.append({"id": sid, "speak": text, "text": cap or text, "start": round(t, 3), "end": round(t + len(a) / sr, 3)})
    t += len(a) / sr
    print(f"{sid:9s} {meta[-1]['start']:7.2f} {meta[-1]['end']:7.2f}")
parts.append(np.zeros(int(1.8 * sr), np.float32)); t += 1.8
audio = np.concatenate(parts); audio = audio / np.abs(audio).max() * 0.9
sf.write(os.path.join(ROOT, "public/seasons2/narration.wav"), audio, sr)
json.dump({"total": round(t, 3), "voice": VOICE, "segments": meta}, open(os.path.join(ROOT, "src/seasons2/narration.json"), "w"), indent=1)
print("total", round(t, 2))
