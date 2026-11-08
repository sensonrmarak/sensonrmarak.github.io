"""Word timings for the monsoon narration (PocketSphinx forced alignment, segment by segment).
   /tmp/claude-0/psx/bin/python scripts/monsoon_align.py  -> adds `words` (caption tokens with start/end) to src/monsoon/narration.json"""
import json, os, re, subprocess
from pocketsphinx import Decoder, get_model_path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, os.environ.get("NAR_JSON", "src/monsoon/narration.json"))
tl = json.load(open(P)); SR = 16000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, os.environ.get("NAR_WAV", "public/monsoon/narration.wav")), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
mp = get_model_path()
dec = Decoder(hmm=os.path.join(mp, "en-us/en-us"), dict=os.path.join(mp, "en-us/cmudict-en-us.dict"), loglevel="FATAL", beam=1e-80, wbeam=1e-60, pbeam=1e-80)
for w, ph in {"coriolis": "K AO R IY OW L IH S", "deccan": "D EH K AH N", "ganga": "G AA NG G AH", "ghats": "G AA T S", "nadu": "N AA D UW"}.items():
    dec.add_word(w, ph, True)
norm = lambda tok: [p.strip("'.") for p in re.split(r"-", tok.lower().strip('".,!?:;')) if p.strip("'.")]
# spoken token groups shown differently in the captions
REPL = __import__("json").loads(os.environ.get("REPL_JSON", "null")) or {"itcz": [(["I.", "T.", "C.", "Z."], "ITCZ.")], "lpa": [(["eighty-seven", "centimetres,"], "87 cm,")],
        "ocean": [(["Nino"], "Niño"), (["Nina"], "Niña")]}
for s in tl["segments"]:
    toks = s["speak"].split(); parts = [norm(t) for t in toks]; flat = [p for ps in parts for p in ps]
    words = None
    for pad in (0.15, 0.3, 0.05):
        a0 = max(0, s["start"] - pad); a1 = s["end"] + pad
        dec.set_align_text(" ".join(flat)); dec.start_utt(); dec.process_raw(raw[int(a0 * SR) * 2: int(a1 * SR) * 2], full_utt=True); dec.end_utt()
        sg = dec.seg()
        if sg is None: continue
        w = [(re.sub(r"\(\d+\)$", "", x.word), x.start_frame / 100 + a0, (x.end_frame + 1) / 100 + a0) for x in sg]
        w = [x for x in w if x[0] not in ("<s>", "</s>", "<sil>", "(NULL)")]
        if [x[0] for x in w] == flat: words = w; break
    timed = []
    if words:
        i = 0
        for t, ps in zip(toks, parts):
            timed.append({"text": t, "start": round(words[i][1], 3), "end": round(words[i + len(ps) - 1][2], 3)}); i += len(ps)
    else:  # fallback: spread over the segment by word length
        wts = [len(t) + 1.5 for t in toks]; tot = sum(wts); c = s["start"]
        for t, wt in zip(toks, wts): timed.append({"text": t, "start": round(c, 3), "end": round(c + (s["end"] - s["start"]) * wt / tot, 3)}); c += (s["end"] - s["start"]) * wt / tot
        print("FALLBACK", s["id"])
    for grp, rep in REPL.get(s["id"], []):
        for i in range(len(timed) - len(grp) + 1):
            if [x["text"] for x in timed[i:i + len(grp)]] == grp:
                timed[i:i + len(grp)] = [{"text": rep, "start": timed[i]["start"], "end": timed[i + len(grp) - 1]["end"]}]; break
    s["words"] = timed
    assert " ".join(x["text"] for x in timed) == s["text"], (s["id"], " ".join(x["text"] for x in timed))
    print("ok", s["id"], timed[0]["start"], timed[-1]["end"])
json.dump(tl, open(P, "w"), indent=1)
