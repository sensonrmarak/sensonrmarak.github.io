---
name: motion-cube-stack
description: "Isometric cubes drop from above and bounce into a stacked bar or staircase, each face shaded in three tones. Use for growth, building blocks, 'stacking up', progress, modular products, data as physical blocks and playful explainer moments."
---

# Cube Stack

Clean isometric cubes in three-tone shading (top light, left mid, right dark) fall in a staggered wave and land with a small bounce and squash, stacking into rising columns. Final frame is a tidy 3D bar chart of blocks with a label.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.2–3.2 s: cubes drop column by column, bottom to top, 0.07 s apart.
- Each cube: 0.55 s fall with bounce ease, squash 0.85 on contact.
- 3.4–4.2 s: the label slides in and the tallest column turns accent.
- 4.4–6.0 s: hold with a gentle camera drift.

## How it's built

Isometric projection: `sx = (x - y) * cos30 * s`, `sy = (x + y) * sin30 * s - z * s`. Each cube is three polygons (top, left, right) drawn in painter's order sorted by `x + y + z` ascending. Drop: `z = zFinal + (1 - E.bounce(k)) * 9`. Squash on landing: scale the cube's height by `0.85` for 0.08 s around contact. Columns are heights from a data array, so the stack is a real chart.

## Knobs

- Data array (column heights) and grid layout.
- Cube size and gap.
- Drop stagger order (by column, by height, diagonal wave).
- Face colours (keep top lightest).

## Pitfalls

- Sort by x+y+z every frame: falling cubes change depth order.
- Draw faces with a 1 px overlap/stroke of the same colour to hide seams.
- Don't drop more than ~10 cubes at once or the eye can't follow.

## Pairs well with

`motion-bars-3d`, `motion-iso-city`, `motion-count-up`, `motion-tile-grids`
