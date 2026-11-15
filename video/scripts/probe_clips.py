"""Record the length of each AI clip in public/moss/clips (shot1.mp4 ... shot8.mp4) for the edit."""
import json, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
clips = {}
for i in range(1, 9):
    f = os.path.join(ROOT, "public/moss/clips", f"shot{i}.mp4")
    if os.path.exists(f):
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                           capture_output=True, text=True, check=True).stdout.strip()
        clips[str(i)] = round(float(d), 3)
json.dump(clips, open(os.path.join(ROOT, "src/moss/clips.json"), "w"), indent=1)
print(clips)
