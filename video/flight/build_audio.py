import json, subprocess, wave, os, sys
import numpy as np
VOICE = sys.argv[1] if len(sys.argv) > 1 else "/tmp/piper/en_GB-alan-medium.onnx"
SR = 48000; GAP = 0.32; LEAD = 0.9; TAIL = 0.9
script = json.load(open("script.json"))
def synth(text, path):
    subprocess.run(["piper", "-m", VOICE, "-f", path, "--length-scale", "1.06", "--sentence-silence", "0.22", "--", text], check=True, capture_output=True)
    tmp = path + ".48.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ar", str(SR), "-ac", "1", tmp], check=True)
    w = wave.open(tmp); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768; w.close(); os.remove(tmp)
    # trim leading/trailing silence
    nz = np.where(np.abs(a) > 0.01)[0]
    return a[max(0, nz[0] - 480): nz[-1] + 2400] if len(nz) else a
t = 0.0; chunks = []; timings = []
for sc in script:
    s0 = t; t += LEAD if sc["id"] != "hook" else 0.5; lines = []
    for i, line in enumerate(sc["lines"]):
        a = synth(line, f"audio/{sc['id']}_{i}.wav")
        chunks.append((t, a)); d = len(a) / SR
        lines.append({"text": line, "start": round(t - s0, 3), "end": round(t - s0 + d, 3)}); t += d + GAP
    t += TAIL - GAP
    if sc["id"] == "end": t += 6.0
    timings.append({"id": sc["id"], "title": sc["title"], "start": round(s0, 3), "dur": round(t - s0, 3), "lines": lines})
total = t; voice = np.zeros(int(total * SR) + SR, dtype=np.float32)
for st, a in chunks: voice[int(st * SR): int(st * SR) + len(a)] += a
voice /= max(1e-6, np.abs(voice).max()) / 0.9
# ---- music bed: slow evolving pad (A minor 9 / F maj 7 / C / G) + soft pulse
n = len(voice); tt = np.arange(n) / SR; rng = np.random.default_rng(7)
def tone(f, ph=0): return np.sin(2 * np.pi * f * tt + ph) + 0.35 * np.sin(2 * np.pi * f * 2 * tt + ph) * 0.5
chords = [[110, 164.81, 220, 261.63, 329.63], [87.31, 130.81, 174.61, 220, 329.63], [130.81, 196, 261.63, 329.63, 392], [98, 146.83, 196, 246.94, 293.66]]
bar = 8.0; pad = np.zeros(n, dtype=np.float32)
for ci, ch in enumerate(chords):
    env = np.clip(1 - np.abs(((tt / bar - ci) % 4) - 0.5) / 0.75, 0, 1) ** 1.5
    for f in ch: pad += (tone(f, rng.random() * 6) * env * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * tt + f))).astype(np.float32)
pad *= 0.05
pulse = (np.sin(2 * np.pi * 55 * tt) * np.exp(-((tt % 1.0)) * 6) * 0.05).astype(np.float32)
music = pad + pulse
# whoosh at scene changes
for sc in timings[1:]:
    c = int(sc["start"] * SR); L = int(1.0 * SR); x = rng.standard_normal(L).astype(np.float32)
    k = np.linspace(0, 1, L); x = np.convolve(x, np.ones(40) / 40, "same") * np.sin(np.pi * k) ** 2 * 0.22
    a0 = max(0, c - L // 2); music[a0:a0 + L] += x[: len(music[a0:a0 + L])]
fade = np.clip(tt / 2, 0, 1) * np.clip((total - tt) / 3, 0, 1); music *= fade
# duck music under voice
envv = np.convolve(np.abs(voice), np.ones(SR // 4) / (SR // 4), "same"); duck = 1 - 0.55 * np.clip(envv * 12, 0, 1)
mix = voice * 0.95 + music * duck * 1.6
st = np.stack([mix, mix], 1); st = np.clip(st, -1, 1)
for name, arr in [("out/audio_mix.wav", st), ("out/narration.wav", np.stack([voice, voice], 1))]:
    w = wave.open(name, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((arr[: int(total * SR)] * 32767).astype(np.int16).tobytes()); w.close()
json.dump({"total": round(total, 3), "scenes": timings}, open("timings.json", "w"), indent=1)
print("total", round(total, 1), "s;", " ".join(f"{s['id']}={s['dur']:.1f}" for s in timings))
