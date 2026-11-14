---
name: motion-split-flap
description: "An airport/train departure board whose characters flip mechanically through the alphabet until they land on the message. Use for announcements, destinations, launches, countdowns, 'now boarding' moments, headlines, dates and retro-mechanical reveals."
---

# Split Flap

A grid of dark flap cells with a hairline split. Each cell flips through characters (top half folds down over the bottom), with every cell running its own number of flips so the message resolves in a ripple from left to right. Accent-coloured cells mark the key word.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.4 s: board fades up showing random characters.
- 0.4–3.2 s: cells flip, 60 ms per flip, each cell 8–22 flips, resolving left to right.
- 3.4–5.5 s: the second row flips to the gate and time; hold to the end.

## How it's built

Each cell has four layers: static top (next char), static bottom (current char), and two moving flaps, the top flap showing the current char rotating `rotateX(0 → -90deg)` in the first half of a flip and the bottom flap showing the next char rotating `90deg → 0` in the second half. For time `t`, flip index `f = floor((t - start)/0.06)` and phase `p = frac(...)` give everything, so it scrubs exactly. Each half is a 60 px window with `overflow:hidden`; the glyph inside is 120 px tall and offset so halves line up.

## Knobs

- Flip duration (60 ms) and per-cell flip counts (min/max).
- Character set (A–Z 0–9 or custom).
- Board size; accent cells.
- Click sound per flip (add audio ticks at flip times).

## Pitfalls

- Compute everything from t; never accumulate flips frame to frame.
- Rotating halves need `backface-visibility:hidden` and a `perspective` on the cell.
- Monospace glyphs only, or halves misalign.

## Pairs well with

`motion-count-up`, `motion-scramble-decode`, `motion-typewriter`, `motion-marquee-brands`
