---
name: motion-swiss-grid
description: "International Typographic Style layout in motion: a 12-column grid draws on, then blocks, a huge number, a red circle and text columns snap into the grid on hard beats. Use for editorial and design-forward scenes, chapter cards, data headlines, portfolio intros, poster-style title cards and timeline sections."
---

# Swiss Grid

Hairline grid lines rule across the frame, then elements land on the grid with hard, confident moves: a giant numeral, a red disc, a black bar, flush-left text columns and small metadata in mono. Strict alignment, asymmetric composition, lots of white space.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.8 s: vertical then horizontal grid lines draw (stagger 30 ms).
- 0.9 s: giant '26' slides in from the left edge (expo).
- 1.3 s: red circle scales in on its grid cell (back).
- 1.6 s: black bar wipes across 6 columns.
- 2.0–2.6 s: three text blocks rise in, column by column.
- 4.6–5.2 s: grid lines fade to 40 %, layout holds.

## How it's built

Positions come from a grid helper: `col(n) = margin + n·(colW + gutter)`, rows likewise, so every element snaps. Lines are divs whose `scaleX/scaleY` animate from 0 with origin at their start. Elements use `translate` from off-grid positions with expo/back eases, timed to land on beats (0.9, 1.3, 1.6, 2.0 s), not spread evenly.

## Knobs

- Columns (12), margins and gutters.
- Element list, grid spans and land times (align to music beats).
- Accent colour (classic red #e3001b or the palette accent).
- Line weight and final opacity.

## Pitfalls

- Everything must snap to the grid; one off-grid element breaks the style.
- Don't centre things; Swiss style is flush-left and asymmetric.
- Avoid soft fades for the main elements: hard moves and cuts.

## Pairs well with

`motion-kinetic-type`, `motion-count-up`, `motion-donut-ring`, `motion-blueprint-draw`
