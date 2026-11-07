"""Word-level caption sync: aligns a narration MP3 to its known script with PocketSphinx (offline, model built in).
Setup:  uv venv psx && uv pip install --python psx/bin/python pocketsphinx numpy
Usage:  psx/bin/python scripts/align_words.py src/zones/timeline.json narration.mp3
Segments that will not align as a whole are aligned sentence by sentence; a sentence that still fails is timed
inside its measured start and end. NOTE: the second pass compares against an estimate file at
/tmp/claude-0/zl_timeline_est.json (a copy of the timeline before alignment); keep that copy when re-running."""
import json, re, subprocess, sys
from pocketsphinx import Decoder, get_model_path
import os
tl_path, mp3 = sys.argv[1], sys.argv[2]
tl = json.load(open(tl_path))
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
SR = 16000
mp = get_model_path()
dec = Decoder(hmm=os.path.join(mp, "en-us/en-us"), dict=os.path.join(mp, "en-us/cmudict-en-us.dict"), loglevel="FATAL", beam=1e-80, wbeam=1e-60, pbeam=1e-80)
EXTRA = {"longyearbyen": "L AO NG Y IH R B IY AH N", "orrery": "AO R ER IY", "earth's": "ER TH S", "axis": "AE K S AH S"}
def norm(tok):  # original caption token -> list of dictionary words
    t = tok.lower().strip('".,!?:;')
    return [p for p in re.split(r"[-]", t) if p]
missing = set()
for seg in tl["segments"]:
    for w in seg["words"]:
        for p in norm(w["text"]):
            if not dec.lookup_word(p):
                missing.add(p)
for w in missing:
    if w in EXTRA: dec.add_word(w, EXTRA[w], True)
    else: print("MISSING", w)
for seg in tl["segments"]:
    toks = seg["words"]; parts = [norm(w["text"]) for w in toks]
    flat = [p for ps in parts for p in ps]
    words = None
    for pad in (0.25, 0.45, 0.1, 0.7):
        s0 = max(0.0, seg["start"] - pad); s1 = seg["end"] + pad
        chunk = raw[int(s0 * SR) * 2: int(s1 * SR) * 2]
        dec.set_align_text(" ".join(flat))
        dec.start_utt(); dec.process_raw(chunk, full_utt=True); dec.end_utt()
        sg = dec.seg()
        if sg is not None:
            words = [(x.word, x.start_frame / 100 + s0, (x.end_frame + 1) / 100 + s0) for x in sg]; break
    if words is None:
        print("FAILED", seg["text"][:40]); continue
    words = [w for w in words if w[0] not in ("<s>", "</s>", "<sil>", "(NULL)")]
    words = [(re.sub(r"\(\d+\)$", "", a), b, c) for a, b, c in words]
    if [w[0] for w in words] != flat:
        print("ALIGN MISMATCH in segment:", seg["text"][:40], len(words), len(flat)); continue
    i = 0
    for tok, ps in zip(toks, parts):
        tok["start"] = round(words[i][1], 3); tok["end"] = round(words[i + len(ps) - 1][2], 3); i += len(ps)
    print("ok", seg["text"][:40], [(t["text"], t["start"]) for t in toks[:3]])
json.dump(tl, open(tl_path, "w"), indent=1)

# ---- second pass: align failed segments sentence by sentence, cutting at the pauses between sentences
import numpy as np
x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
win = 160; nW = len(x) // win
rms = np.sqrt((x[: nW * win].reshape(nW, win) ** 2).mean(1) + 1e-12); db = 20 * np.log10(rms / rms.max())
def quiet_runs(a, b, min_len=0.12):
    runs, st = [], None
    for i in range(int(a * 100), int(b * 100)):
        q = db[i] < -35
        if q and st is None: st = i
        if not q and st is not None:
            if (i - st) / 100 >= min_len: runs.append(((st + i) / 200))
            st = None
    return runs
def align_piece(toks, a, b):
    parts = [norm(w["text"]) for w in toks]; flat = [p for ps in parts for p in ps]
    for pad in (0.15, 0.3, 0.05):
        s0 = max(0.0, a - pad); s1 = b + pad
        dec.set_align_text(" ".join(flat)); dec.start_utt(); dec.process_raw(raw[int(s0 * SR) * 2: int(s1 * SR) * 2], full_utt=True); dec.end_utt()
        sg = dec.seg()
        if sg is None: continue
        words = [(re.sub(r"\(\d+\)$", "", w.word), w.start_frame / 100 + s0, (w.end_frame + 1) / 100 + s0) for w in sg]
        words = [w for w in words if w[0] not in ("<s>", "</s>", "<sil>", "(NULL)")]
        if [w[0] for w in words] != flat: continue
        i = 0
        for tok, ps in zip(toks, parts):
            tok["start"] = round(words[i][1], 3); tok["end"] = round(words[i + len(ps) - 1][2], 3); i += len(ps)
        return True
    return False
def spread(toks, a, b):
    # fallback: spread the sentence's words over its voiced span (bounds come from the measured pauses)
    i0, i1 = int(a * 100), int(b * 100)
    v = [i for i in range(i0, i1) if db[i] > -35]
    va, vb = (v[0] / 100, (v[-1] + 1) / 100) if v else (a, b)
    wts = [len(t["text"].strip('".,!?:')) + 1.5 for t in toks]; tot = sum(wts); c = va
    for t, w in zip(toks, wts):
        t["start"] = round(c, 3); c += (vb - va) * w / tot; t["end"] = round(c, 3)
    print("   fallback:", " ".join(t["text"] for t in toks)[:60], round(va, 2), round(vb, 2))
est = json.load(open("/tmp/claude-0/zl_timeline_est.json"))
for si, seg in enumerate(tl["segments"]):
    if seg["words"][0]["start"] != est["segments"][si]["words"][0]["start"]: continue   # already aligned
    toks = seg["words"]
    sents, cur = [], []
    for k, w in enumerate(toks):
        cur.append(k)
        if re.search(r'[.!?]"?$', w["text"]): sents.append(cur); cur = []
    if cur: sents.append(cur)
    pauses = quiet_runs(seg["start"], seg["end"])
    bounds = [seg["start"]]
    for sent in sents[:-1]:
        e = est["segments"][si]["words"][sent[-1]]["end"]
        c = min(pauses, key=lambda p: abs(p - e)) if pauses else e
        bounds.append(c)
    bounds.append(seg["end"])
    res = [align_piece([toks[k] for k in sent], bounds[j], bounds[j + 1]) for j, sent in enumerate(sents)]
    for j, sent in enumerate(sents):
        if res[j]: continue
        a = toks[sents[j - 1][-1]]["end"] if j > 0 and res[j - 1] else bounds[j]
        b = toks[sents[j + 1][0]]["start"] if j + 1 < len(sents) and res[j + 1] else bounds[j + 1]
        spread([toks[k] for k in sent], a, b)
    ok = all(res)
    print("pass2", "ok" if ok else "PARTIAL", seg["text"][:40], [(toks[s[0]]["text"], toks[s[0]]["start"]) for s in sents])
json.dump(tl, open(tl_path, "w"), indent=1)
