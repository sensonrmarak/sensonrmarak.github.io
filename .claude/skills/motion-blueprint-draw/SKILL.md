---
name: motion-blueprint-draw
description: "A technical drawing that draws itself line by line on blueprint paper: construction grid, outlines, dimension lines and handwritten-style labels. Use for engineering, architecture, product design, 'how it's made', planning, hardware and build-process scenes."
---

# Blueprint Draw

Deep blueprint blue with a fine white grid. A part (a flanged bearing housing) draws in white strokes, outlines first, then centre lines (dashed), then dimension lines with arrowheads and monospaced callouts that type on. A title block sits bottom right.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: grid fades in.
- 0.4–2.8 s: outlines draw, each path over 0.7 s, staggered 0.18 s.
- 2.4–3.6 s: dashed centre lines draw.
- 3.2–4.8 s: dimension lines draw, then their labels fade/slide in.
- 4.6–5.4 s: title block draws; hold.

## How it's built

Inline SVG. On load, measure each path once with `getTotalLength()` and set `stroke-dasharray = L`. Per frame `stroke-dashoffset = L * (1 - E.inOut(k))`. Dashed centre lines can't use dasharray for the draw, so they're revealed through an animated `clipPath` rect instead. Labels are SVG `<text>` with opacity and a small x offset. Order the reveal by importance: silhouette, then construction, then annotation.

## Knobs

- Paper colour (#173a8c classic, #0f2f6b deep) and grid spacing.
- Per-path duration/stagger and draw order.
- Swap the drawing: any SVG paths work; keep strokes 2–4 px.
- Label text and units.

## Pitfalls

- Measure lengths once at setup, never inside renderAt.
- `vector-effect: non-scaling-stroke` breaks dash lengths if the SVG is scaled; keep 1:1.
- Too many simultaneous paths turns into noise: keep 2–3 drawing at once.

## Pairs well with

`motion-line-draw`, `motion-layer-explode`, `motion-iso-city`, `motion-swiss-grid`
