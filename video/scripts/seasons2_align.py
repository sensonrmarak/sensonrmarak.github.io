"""Word timings for the seasons narration: align the spoken text with PocketSphinx, then map the times onto the
caption text (numbers written as digits) with a token diff.  /tmp/claude-0/psx/bin/python scripts/seasons2_align.py"""
import json, os, re, subprocess, difflib
from pocketsphinx import Decoder, get_model_path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, os.environ.get("NAR_JSON", "src/seasons2/narration.json"))
tl = json.load(open(P)); SR = 16000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(ROOT, os.environ.get("NAR_WAV", "public/seasons2/narration.wav")), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
mp = get_model_path()
dec = Decoder(hmm=os.path.join(mp, "en-us/en-us"), dict=os.path.join(mp, "en-us/cmudict-en-us.dict"), loglevel="FATAL", beam=1e-80, wbeam=1e-60, pbeam=1e-80)
EXTRA = {"mirzapur": "M IH R Z AA P UH R", "chhattisgarh": "CH AH T IY S G AA R", "jharkhand": "JH AA R K AA N D", "mizoram": "M IH Z AO R AE M",
         "tripura": "T R IH P UH R AH", "khejri": "K EH JH R IY", "babool": "B AH B UW L", "deodar": "D IY OW D AA R", "kalahari": "K AA L AH HH AA R IY",
         "atacama": "AE T AH K AA M AH", "nicobar": "N IH K OW B AA R", "andaman": "AE N D AH M AE N", "ghats": "G AA T S", "convectional": "K AH N V EH K SH AH N AH L", "meridians": "M ER IH D IY AH N Z", "hemispheres": "HH EH M IH S F IH R Z", "rajasthan": "R AA JH AH S T AA N", "madhya": "M AH D Y AH", "equinoxes": "IY K W AH N AA K S IH Z", "canopies": "K AE N AH P IY Z", "csir": "S IY EH S AY AA R", "insat": "IH N S AE T", "iitm": "AY AY T IY EH M", "pune": "P UW N EY", "itcz": "AY T IY S IY Z EH D", "deccan": "D EH K AH N", "coriolis": "K AO R IY OW L IH S", "nino": "N IY N Y OW", "nina": "N IY N Y AH", "kerala": "K EH R AH L AH", "ganga": "G AH NG G AA", "tibetan": "T IH B EH T AH N", "coromandel": "K AO R AH M AE N D AH L", "isro": "IH S R OW", "isro's": "IH S R OW Z", "nadu": "N AA D UW"}
norm = lambda tok: [p.strip("'.") for p in re.split(r"-", tok.lower().strip('".,!?:;')) if p.strip("'.")]
for s in tl["segments"]:
    for t in s["speak"].split():
        for p in norm(t):
            if not dec.lookup_word(p):
                if p in EXTRA: dec.add_word(p, EXTRA[p], True)
                else: print("MISSING", p)
key = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
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
    spoken = []
    if words:
        i = 0
        for t, ps in zip(toks, parts): spoken.append((t, words[i][1], words[i + len(ps) - 1][2])); i += len(ps)
    else:
        print("FALLBACK", s["id"]); wts = [len(t) + 1.5 for t in toks]; tot = sum(wts); c = s["start"]
        for t, wt in zip(toks, wts): d = (s["end"] - s["start"]) * wt / tot; spoken.append((t, c, c + d)); c += d
    cap = s["text"].split()
    sm = difflib.SequenceMatcher(a=[key(x[0]) for x in spoken], b=[key(c) for c in cap], autojunk=False)
    timed = []
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == "equal":
            for k in range(a2 - a1): timed.append({"text": cap[b1 + k], "start": round(spoken[a1 + k][1], 3), "end": round(spoken[a1 + k][2], 3)})
        elif b2 > b1:
            st = spoken[a1][1] if a2 > a1 else (timed[-1]["end"] if timed else s["start"])
            en = spoken[a2 - 1][2] if a2 > a1 else st + 0.3
            for k in range(b2 - b1):
                timed.append({"text": cap[b1 + k], "start": round(st + (en - st) * k / (b2 - b1), 3), "end": round(st + (en - st) * (k + 1) / (b2 - b1), 3)})
    s["words"] = timed
    assert " ".join(x["text"] for x in timed) == s["text"], s["id"]
    print("ok", s["id"])
json.dump(tl, open(P, "w"), indent=1)
