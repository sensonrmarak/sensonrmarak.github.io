---
name: motion-count-up
description: "A big number that counts up on a rolling odometer, every digit column spinning and carrying like a mechanical counter, with a label and a sparkline drawing underneath. Use for milestones, revenue, users, downloads, raised funding, stats, KPIs, records and any 'big number' moment."
---

# Count Up

A huge tabular number in heavy display type. Each digit sits in its own masked column and rolls vertically; the ones column spins fast, higher columns tick over only when the column to their right wraps, exactly like an odometer. Thousands separators stay put. A small accent sparkline draws below and a label slides in.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.2–3.2 s: value rolls from 0 to 2,481,903 (expo out: fast then settling).
- 0.6–3.2 s: sparkline draws left to right in sync.
- 3.2 s: final digits land with a 1.04 scale pop; label slides up.
- 3.5–6.0 s: hold.

## How it's built

Value `v = target·E.expo(k)`. For digit column `j` (10^j), the strip position is `floor(v / 10^j) mod 10` plus a carry fraction: when the lower part `v mod 10^j` is in its last 10 %, add `(fraction - 0.9)/0.1` so the column rolls over just as the column to its right wraps. The ones column rolls continuously. Each column is a strip `0…9,0` translated by `-pos × digitHeight`.

## Knobs

- Target value, prefix/suffix ($, %, K, +).
- Duration and ease (expo for drama, inOut for calm).
- Separator style; digit font size.
- Sparkline data or off.

## Pitfalls

- Use tabular figures (or fixed-width columns) or digits jitter sideways.
- Don't count for more than ~3 s; viewers only read the final number.
- Round the displayed final value exactly to the target at the end.

## Pairs well with

`motion-donut-ring`, `motion-bars-3d`, `motion-split-flap`, `motion-kinetic-type`
