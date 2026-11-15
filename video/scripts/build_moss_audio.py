"""Builds the soundtrack and caption timeline for "Moss and the Silver Trail".

Usage:  python3 scripts/build_moss_audio.py [narration.mp3]

- Splits the narration into the 9 script segments (using pauses in the audio),
  places each one at its slot from the script's timing table,
- synthesises an original music-box score and all sound effects,
- writes public/moss/soundtrack.wav and src/moss/timeline.json.

Without a narration file it writes a placeholder timeline (for previewing visuals).
"""
import json, os, subprocess, sys
import numpy as np

SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(7)

SEGMENTS = [
    "In Oakenvale, the Harvest Lantern Fair was glowing on the far side of Fernwhistle Hill.",
    "\"Last one there is a slowpoke!\" laughed Juniper the squirrel, and off she zipped. Pebble the rabbit hopped after her. Hop, hop... gone!",
    "Little Moss the snail just smiled, and kept to the path. Slow and steady, one silvery inch at a time.",
    "But as the sun slipped down, a thick fog came rolling in. Juniper stopped. Pebble stopped. Every tree looked the same.",
    "\"Which way is the Fair?\" Pebble whispered.",
    "Then, through the fog, something shimmered. A thin silver line, glowing in the moonlight. \"It's Moss's trail!\"",
    "They followed it, step by step, until the fog melted away, and there was Moss, waiting at the gate of the Fair.",
    "\"You're not slow, Moss,\" said Juniper. \"You're the one who lit the way.\"",
    "Remember, little friends: slow is not small. Every gift can light someone's way.",
]
SLOTS = [0.5, 6, 13, 20, 29, 33, 41, 50, 55.5]
SHOT_SEGS = [0, 1, 2, 3, 4, 5, 6, 7]  # shot i starts with segment SHOT_SEGS[i]; shot 8 also holds segment 9


# ---------------------------------------------------------------- helpers
def t2i(t):
    return int(round(t * SR))


def env_exp(n, decay):
    return np.exp(-np.arange(n) / SR / decay)


def attack(n, a=0.004):
    e = np.ones(n)
    k = min(n, max(1, t2i(a)))
    e[:k] = np.linspace(0, 1, k)
    return e


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def bandpass(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = 1 / (1 + (lo / np.maximum(f, 1)) ** 4) / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, len(x))


def add(buf, sig, t, gain=1.0, pan=0.0):
    i = t2i(t)
    if i >= buf.shape[1] or i + len(sig) <= 0:
        return
    if i < 0:
        sig, i = sig[-i:], 0
    sig = sig[: buf.shape[1] - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[0, i:i + len(sig)] += sig * gain * l * 1.414
    buf[1, i:i + len(sig)] += sig * gain * r * 1.414


# ---------------------------------------------------------------- instruments
def music_box(m, dur=1.6):
    n = t2i(dur); t = np.arange(n) / SR; f = mtof(m)
    s = np.sin(2 * np.pi * f * t) * env_exp(n, 0.9) + 0.25 * np.sin(2 * np.pi * 2 * f * t) * env_exp(n, 0.35)
    s += 0.12 * np.sin(2 * np.pi * 5.4 * f * t) * env_exp(n, 0.06)
    return s * attack(n, 0.002)


def glock(m, dur=2.2):
    n = t2i(dur); t = np.arange(n) / SR; f = mtof(m)
    s = np.sin(2 * np.pi * f * t) * env_exp(n, 1.1) + 0.3 * np.sin(2 * np.pi * 2.76 * f * t) * env_exp(n, 0.3)
    s += 0.12 * np.sin(2 * np.pi * 5.4 * f * t) * env_exp(n, 0.1)
    return s * attack(n, 0.001)


def pizz(m, dur=0.5):
    n = t2i(dur); t = np.arange(n) / SR; f = mtof(m)
    s = sum(np.sin(2 * np.pi * f * k * t) / k ** 1.3 for k in range(1, 6)) * env_exp(n, 0.12)
    return s * attack(n, 0.003) * 0.6


def pad(ms, dur):
    n = t2i(dur); t = np.arange(n) / SR; s = np.zeros(n)
    for m in ms:
        f = mtof(m)
        for d in (-0.15, 0.0, 0.15):
            s += np.sin(2 * np.pi * f * (1 + d / 100) * t) + 0.3 * np.sin(2 * np.pi * 2 * f * (1 + d / 100) * t)
    e = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.6)
    return s * np.clip(e, 0, 1) / (len(ms) * 4)


# ---------------------------------------------------------------- sound effects
def whoosh():
    n = t2i(0.7); x = rng.standard_normal(n)
    a = bandpass(x[: n // 2], 300, 1400); b = bandpass(x[n // 2:], 900, 4000)
    s = np.concatenate([a, b]); t = np.arange(n) / n
    return s * np.sin(np.pi * t) ** 2 * 0.5


def boing():
    n = t2i(0.4); t = np.arange(n) / SR
    f = 200 + 260 * (t / 0.4) ** 0.5 + 18 * np.sin(2 * np.pi * 22 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.13) * attack(n) * 0.5


def chime_run(notes=(84, 88, 91, 96), gap=0.09):
    out = np.zeros(t2i(gap * len(notes) + 2.4))
    for k, m in enumerate(notes):
        g = glock(m); i = t2i(k * gap); out[i:i + len(g)] += g * 0.5
    return out


def wind(dur):
    n = t2i(dur); x = bandpass(rng.standard_normal(n), 80, 650)
    t = np.arange(n) / SR
    am = 0.6 + 0.4 * np.sin(2 * np.pi * 0.17 * t) * np.sin(2 * np.pi * 0.07 * t + 1)
    e = np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 1.5)
    return x / np.abs(x).max() * am * np.clip(e, 0, 1)


def owl():
    out = np.zeros(t2i(1.3))
    for st, d in ((0.0, 0.3), (0.45, 0.65)):
        n = t2i(d); t = np.arange(n) / SR
        f = 390 - 30 * t / d
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 1.5
        s += 0.15 * bandpass(rng.standard_normal(n), 300, 900) * np.sin(np.pi * t / d)
        out[t2i(st):t2i(st) + n] += s
    return out * 0.45


def heartbeat():
    out = np.zeros(t2i(0.7))
    for st, g in ((0.0, 1.0), (0.26, 0.6)):
        n = t2i(0.25); t = np.arange(n) / SR
        s = np.sin(2 * np.pi * (60 - 20 * t / 0.25) * t) * env_exp(n, 0.07) * g
        out[t2i(st):t2i(st) + n] += s
    return out


def sparkle(dur=1.6, count=26):
    out = np.zeros(t2i(dur + 0.6))
    for k in range(count):
        st = dur * (k / count) ** 0.8; m = rng.integers(88, 103)
        g = glock(m, 0.5) * (0.15 + 0.15 * rng.random())
        i = t2i(st); out[i:i + len(g)] += g
    return out


def bell():
    n = t2i(2.0); t = np.arange(n) / SR; f = 1320
    s = sum(a * np.sin(2 * np.pi * f * p * t) * env_exp(n, d) for p, a, d in ((1, 1, 0.9), (2.4, 0.5, 0.5), (3.0, 0.3, 0.3), (4.5, 0.2, 0.2)))
    return s * attack(n, 0.001) * 0.35


def crickets(dur):
    out = np.zeros(t2i(dur)); t0 = 0.2
    while t0 < dur - 0.3:
        for c in range(3):
            n = t2i(0.045); t = np.arange(n) / SR
            s = np.sin(2 * np.pi * 4300 * t) * np.sin(np.pi * t / 0.045)
            i = t2i(t0 + c * 0.075); out[i:i + n] += s[: len(out) - i]
        t0 += 0.7 + rng.random() * 0.6
    return out * 0.05


def fair_ambience(dur):
    n = t2i(dur); t = np.arange(n) / SR
    x = bandpass(rng.standard_normal(n), 250, 1600)
    syll = np.clip(np.sin(2 * np.pi * 3.7 * t + 2 * np.sin(2 * np.pi * 0.6 * t)), 0, 1) * 0.5 + 0.5
    e = np.minimum(1, t / 2.5) * np.minimum(1, (dur - t) / 1.0)
    return x / np.abs(x).max() * syll * np.clip(e, 0, 1)


# ---------------------------------------------------------------- narration split + timeline
def load_narration(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def silences(x, min_len=0.22, win=0.01):
    w = t2i(win); n = len(x) // w
    rms = np.sqrt((x[: n * w].reshape(n, w) ** 2).mean(1) + 1e-12)
    db = 20 * np.log10(rms / rms.max())
    quiet = db < -38
    runs, s = [], None
    for i, q in enumerate(np.append(quiet, False)):
        if q and s is None:
            s = i
        elif not q and s is not None:
            if (i - s) * win >= min_len:
                runs.append((s * win, i * win))
            s = None
    return runs


def split_segments(x):
    runs = silences(x)
    dur = len(x) / SR
    speech_start = runs[0][1] if runs and runs[0][0] == 0 else 0.0
    speech_end = runs[-1][0] if runs and runs[-1][1] >= dur - 0.02 else dur
    inner = [r for r in runs if r[0] > speech_start + 0.1 and r[1] < speech_end - 0.1]
    lens = np.array([len(s) for s in SEGMENTS], float)
    cum = np.cumsum(lens)[:-1] / lens.sum()
    bounds, used = [], set()
    for c in cum:
        est = speech_start + c * (speech_end - speech_start)
        cands = [(abs((a + b) / 2 - est) - 0.6 * (b - a), k) for k, (a, b) in enumerate(inner)
                 if k not in used and (not bounds or (a + b) / 2 > bounds[-1][1])]
        _, k = min(cands)
        used.add(k); bounds.append(inner[k])
    segs = []
    starts = [speech_start] + [b for _, b in bounds]
    ends = [a for a, _ in bounds] + [speech_end]
    for s, e in zip(starts, ends):
        segs.append((max(0, s - 0.03), min(dur, e + 0.08)))
    return segs, runs


def word_times(text, start, end, pauses):
    """Spread words across [start, end], skipping internal pauses (absolute times)."""
    words = text.split()
    spans, cur = [], start
    for a, b in pauses:
        if start < a and b < end:
            spans.append((cur, a)); cur = b
    spans.append((cur, end))
    total = sum(b - a for a, b in spans)
    weights = np.array([len(w.strip('".,!?:')) + 1.5 for w in words], float)
    # assign words to spans by cumulative proportion of weight vs span time
    cumw = np.concatenate([[0], np.cumsum(weights)]) / weights.sum()
    span_cum = np.concatenate([[0], np.cumsum([b - a for a, b in spans])]) / total

    def at(p):
        k = min(np.searchsorted(span_cum, p, side="right") - 1, len(spans) - 1)
        a, b = spans[k]
        frac = (p - span_cum[k]) / max(1e-6, span_cum[k + 1] - span_cum[k])
        return a + frac * (b - a)

    return [{"text": w, "start": round(at(cumw[i]), 3), "end": round(at(cumw[i + 1]), 3)} for i, w in enumerate(words)]


def build(narr_path):
    timeline_segs = []
    narr_track = None
    if narr_path:
        x = load_narration(narr_path)
        x = x / np.abs(x).max() * 0.9
        segs, runs = split_segments(x)
        cur_end = 0.0
        placed = []
        for i, (s, e) in enumerate(segs):
            st = max(SLOTS[i], cur_end + (0.45 if i else 0))
            placed.append((st, s, e)); cur_end = st + (e - s)
        total = max(60.0, cur_end + 3.5)
        narr_track = np.zeros(t2i(total) + SR)
        for i, (st, s, e) in enumerate(placed):
            clip = x[t2i(s):t2i(e)]
            fade = np.minimum(1, np.minimum(np.arange(len(clip)), np.arange(len(clip))[::-1]) / t2i(0.01))
            narr_track[t2i(st):t2i(st) + len(clip)] += clip * fade
            pauses = [(a - s + st, b - s + st) for a, b in runs if s < a and b < e and b - a >= 0.22]
            timeline_segs.append({"start": round(st, 3), "end": round(st + e - s, 3), "text": SEGMENTS[i],
                                  "words": word_times(SEGMENTS[i], st, st + e - s, pauses)})
    else:
        total = 60.0
        for i, text in enumerate(SEGMENTS):
            st = SLOTS[i]; en = (SLOTS[i + 1] if i + 1 < len(SLOTS) else 60) - 0.6
            en = min(en, st + len(text.split()) * 0.36)
            timeline_segs.append({"start": st, "end": round(en, 3), "text": text, "words": word_times(text, st, en, [])})

    shots = [0.0] + [timeline_segs[k]["start"] - 0.25 for k in SHOT_SEGS[1:]]
    tl = {"fps": 24, "total": round(total, 3), "shots": [round(s, 3) for s in shots], "segments": timeline_segs}

    def wt(seg, word, which="start"):
        for w in tl["segments"][seg]["words"]:
            if word.lower() in w["text"].lower():
                return w[which]
        raise KeyError(word)

    # ------------------------------------------------ music
    n = t2i(total) + SR
    music = np.zeros((2, n)); sfx = np.zeros((2, n))
    S = [s["start"] for s in timeline_segs]
    sec = lambda t: max(i for i in range(len(S)) if S[i] - 0.3 <= t) if t >= S[0] - 0.3 else 0
    beat = 60 / 84
    prog = [(53, [65, 69, 72]), (50, [62, 65, 69]), (46, [58, 62, 65]), (48, [60, 64, 67])]  # F Dm Bb C
    minor = [(50, [62, 65, 69]), (43, [55, 58, 62]), (46, [58, 62, 65]), (45, [57, 61, 64])]  # Dm Gm Bb A
    melody = [(69, 2), (72, 1), (74, 2), (72, 1), (70, 1), (69, 1), (67, 1), (67, 2), (None, 1),
              (69, 2), (72, 1), (77, 2), (76, 1), (74, 1), (72, 1), (70, 1), (67, 1), (64, 1), (65, 1)]
    mel_beats = []
    for m, d in melody:
        mel_beats.append(m); mel_beats += [None] * (d - 1)
    b = 0
    while b * beat < total - 0.5:
        t = b * beat; s = sec(t); bar = b // 3; pos = b % 3
        root, ch = prog[bar % 4]
        mroot, mch = minor[bar % 4]
        mel = mel_beats[b % len(mel_beats)]
        if s == 0:  # gentle music box intro
            add(music, music_box(ch[pos] + 12), t, 0.22, -0.3)
            if mel: add(music, music_box(mel + 12), t, 0.3, 0.2)
        elif s == 1:  # playful pizzicato
            add(music, pizz(root if pos == 0 else ch[pos]), t, 0.5, -0.2)
            add(music, pizz(ch[(pos + 1) % 3] + 12), t + beat / 2, 0.35, 0.3)
        elif s == 2:  # music slows
            if pos == 0: add(music, music_box(ch[0] + 12, 2.5), t, 0.25)
            if mel and b % 2 == 0: add(music, music_box(mel + 12, 2.5), t, 0.25, 0.2)
        elif s in (3, 4):  # low and soft, then near silence
            if pos == 0 and s == 3: add(music, pad([mroot] + mch, beat * 3 + 0.4), t, 0.5)
            if pos == 0 and s == 4: add(music, pad([mroot, mch[0]], beat * 3 + 0.4), t, 0.18)
        elif s == 5:  # lift with warm glockenspiel
            if pos == 0: add(music, pad([root] + ch, beat * 3 + 0.4), t, 0.4)
            add(music, glock(ch[pos] + 24), t, 0.16, 0.3 - 0.3 * pos)
        elif s == 6:  # builds
            if pos == 0: add(music, pad([root] + ch, beat * 3 + 0.4), t, 0.45)
            add(music, pizz(root if pos == 0 else ch[pos]), t, 0.35, -0.3)
            add(music, music_box(ch[pos] + 12), t + beat / 2, 0.2, 0.3)
            if mel: add(music, glock(mel + 12), t, 0.18)
        elif s == 7:  # softens under dialogue
            if pos == 0: add(music, pad([root] + ch, beat * 3 + 0.4), t, 0.25)
            add(music, music_box(ch[pos] + 12), t, 0.15)
        else:  # full warm melody
            if pos == 0: add(music, pad([root] + ch, beat * 3 + 0.4), t, 0.45)
            add(music, music_box(ch[pos] + 12), t, 0.22, -0.3)
            add(music, pizz(root if pos == 0 else ch[pos]), t, 0.25, 0.3)
            if mel: add(music, music_box(mel + 12), t, 0.35, 0.1); add(music, glock(mel + 24), t, 0.08)
        b += 1

    # ------------------------------------------------ sound effects, synced to words
    add(sfx, crickets(S[1]), 0, 0.9, 0.4)
    add(sfx, whoosh(), wt(1, "zipped") + 0.05, 0.8, 0.5)
    for w in ("hopped", "Hop,", "hop..."):
        add(sfx, boing(), wt(1, w), 0.7, -0.2)
    add(sfx, chime_run(), wt(2, "silvery"), 0.5, 0.2)
    wd = S[5] - S[3] + 1
    add(sfx, wind(wd), S[3] - 0.3, 0.12, 0)
    add(sfx, owl(), tl["segments"][3]["end"] + 0.2, 0.6, -0.6)
    hb_t = S[4] - 0.1
    while hb_t < S[5] - 0.6:
        add(sfx, heartbeat(), hb_t, 0.9); hb_t += 1.05
    add(sfx, sparkle(), wt(5, "shimmered") - 0.1, 0.9, 0)
    add(sfx, fair_ambience(total - wt(6, "melted")), wt(6, "melted"), 0.05, 0)
    add(sfx, bell(), wt(6, "gate"), 0.7, 0.3)
    add(sfx, chime_run((77, 81, 84, 89, 93), 0.12), S[8] + 0.4, 0.7, 0)
    add(sfx, glock(89, 4) * 0.5, tl["segments"][8]["end"] + 0.3, 0.5, 0)

    # ------------------------------------------------ mix with ducking under narration
    out = music * 0.55 + sfx
    if narr_track is not None:
        nt = np.abs(narr_track[:n]) if len(narr_track) >= n else np.pad(np.abs(narr_track), (0, n - len(narr_track)))
        k = t2i(0.25); env = np.convolve(nt, np.ones(k) / k, mode="same")
        duck = 1 - 0.45 * np.clip(env / 0.05, 0, 1)
        out[0] *= duck; out[1] *= duck
        out[0] += nt * 0 + (narr_track[:n] if len(narr_track) >= n else np.pad(narr_track, (0, n - len(narr_track))))
        out[1] += (narr_track[:n] if len(narr_track) >= n else np.pad(narr_track, (0, n - len(narr_track))))
    fade = np.clip((total - np.arange(n) / SR) / 2.0, 0, 1)
    out *= fade
    out = out[:, : t2i(total)]
    out = out / max(1.0, np.abs(out).max() / 0.95)

    os.makedirs(os.path.join(ROOT, "public/moss"), exist_ok=True)
    pcm = (out.T * 32767).astype("<i2").tobytes()
    import wave
    with wave.open(os.path.join(ROOT, "public/moss/soundtrack.wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm)
    with open(os.path.join(ROOT, "src/moss/timeline.json"), "w") as f:
        json.dump(tl, f, indent=1)
    print("total", total, "segments", [(s["start"], s["end"]) for s in timeline_segs])


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else None)
