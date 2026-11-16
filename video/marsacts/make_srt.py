"""Captions for the full video: cold open (mars3d) followed by the main film (marsacts)."""
import json, re, subprocess
def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))
OFF = dur("../mars3d/out/mars-cold-open-3d-final-1080p.mp4")
cues = []
for path, off in (("../mars3d/timings.json", 0.0), ("timings.json", OFF)):
    for sc in json.load(open(path))["scenes"]:
        for ln in sc["lines"]:
            a, b = off + sc["start"] + ln["start"], off + sc["start"] + ln["end"]
            parts = re.split(r"(?<=[.?!,])\s+", ln["text"]) if len(ln["text"]) > 84 else [ln["text"]]
            chunks, cur = [], ""
            for p in parts:
                if cur and len(cur) + len(p) > 84: chunks.append(cur); cur = p
                else: cur = (cur + " " + p).strip()
            chunks.append(cur); tot = sum(len(c) for c in chunks); t = a
            for c in chunks: e = t + (b - a) * len(c) / tot; cues.append((t, e, c)); t = e
f = lambda s: f"{int(s // 3600):02}:{int(s % 3600 // 60):02}:{int(s % 60):02},{int(s * 1000 % 1000):03}"
open("out/captions.srt", "w").write("\n".join(f"{i}\n{f(a)} --> {f(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues, 1)))
print(len(cues), "cues; offset", OFF)
