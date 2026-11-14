---
name: motion-scramble-decode
description: "Text that resolves out of cycling random glyphs, left to right, like a decrypting terminal or hacker reveal, with the settled letters locking in colour. Use for secrets/security, AI 'thinking', product names, codes and passwords, glitchy tech intros, subtitles and data reveals."
---

# Scramble Decode

A headline and a mono subtitle. Each character cycles through random glyphs (A–Z, 0–9, symbols) at 20 fps, then locks to its final letter in a wave from left to right. Unlocked characters are dim accent; locked ones are paper white with a one-frame flash.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.4 s: the full line appears as random glyphs.
- 0.4–2.4 s: headline locks left to right (each char ~0.05 s after the previous, plus seeded jitter).
- 2.0–3.6 s: subtitle locks, faster.
- 4.6–5.4 s: optional re-scramble of one word (shows it's live), relocks.

## How it's built

For each character: `lockAt = start + i·step + jitter_i`. Before `lockAt`, show a glyph chosen by `rng(seed + i·997 + floor(t·20))`, which changes 20 times a second and is identical on every render of the same frame. At `lockAt` show the real character; for one frame after, flash it accent. Spaces lock immediately.

## Knobs

- Glyph set (letters, katakana, binary, box-drawing).
- Cycle rate (20 fps) and lock step per char.
- Lock order: left-to-right, random, centre-out.
- Colours for scrambling vs. locked.

## Pitfalls

- Seed by `floor(t·rate)`, never `Math.random()`, or scrubbing shows different glyphs.
- Use a monospace face or the line width jumps every frame.
- Keep scrambling short per char (< 1.5 s) or it becomes unreadable noise.

## Pairs well with

`motion-typewriter`, `motion-split-flap`, `motion-kinetic-type`, `motion-command-palette`
