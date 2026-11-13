"""Re-record only the last (outro) segment of the whiteboard narration and splice it onto the existing audio.
   /tmp/claude-0/kvenv/bin/python scripts/wb_reoutro.py"""
import json, os, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); K = "/tmp/claude-0/kokoro"
P = os.path.join(ROOT, "src/wb/narration.json"); WAV = os.path.join(ROOT, "public/wb/narration.wav")
RAW = "So here is the whole map in your mind. What: a seasonal reversal of winds, in two phases. Why: heating, the {I T C Z|ITCZ}, and the Himalayas. How it arrives: two branches, on a timetable, declared by three tests. Why it matters: crops, prices, and markets. And how we respond: store the rain, and prepare for a more extreme monsoon. If this helped, subscribe to Modus {and Rayzon|& Raison}."
speak = re.sub(r"\{([^|}]*)\|([^}]*)\}", r"\1", RAW); cap = re.sub(r"\{([^|}]*)\|([^}]*)\}", r"\2", RAW)
tl = json.load(open(P)); o = tl["segments"][-1]; assert o["id"] == "outro"
audio, sr = sf.read(WAV, dtype="float32"); i0 = int(o["start"] * sr); old = audio[i0:int(o["end"] * sr)]
a, sr2 = Kokoro(f"{K}/model.onnx", f"{K}/voices.npz").create(speak, voice=tl["voice"], speed=0.84, lang="en-gb", sentence_pause=0.55, clause_pause=0.18)
assert sr2 == sr; a = a.astype(np.float32); a *= np.sqrt((old ** 2).mean() / (a ** 2).mean())
out = np.concatenate([audio[:i0], a, np.zeros(int(1.8 * sr), np.float32)]); sf.write(WAV, out, sr)
o.update(speak=speak, text=cap, end=round(o["start"] + len(a) / sr, 3)); o.pop("words", None)
tl["total"] = round(len(out) / sr, 3); json.dump(tl, open(P, "w"), indent=1); print("outro", o["start"], o["end"], "total", tl["total"])
