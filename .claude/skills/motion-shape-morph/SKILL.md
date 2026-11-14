---
name: motion-shape-morph
description: "A single solid shape that morphs smoothly circle → triangle → square → star, rotating and changing colour at each stage. Use for 'transform/adapt' metaphors, logo builds, chapter transitions, Bauhaus/geometric motion, loading states and showreel 'morph' moments."
---

# Shape Morph

One flat shape centre frame. It holds briefly as a circle, then flows into a triangle, a square and finally a five-point star, each transition with an in-out ease and a quarter turn of rotation. The fill steps through accent, blue, yellow and ink on each arrival, and a thin outline echo trails one beat behind.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: circle scales up from 0 (back ease).
- 1.0–1.8 s: circle → triangle (fill to blue).
- 2.3–3.1 s: triangle → square (fill to yellow).
- 3.6–4.4 s: square → star (fill to accent).
- 4.4–6.0 s: star holds and slowly spins; outline echo catches up.

## How it's built

Every shape is resampled to the same number of points (`N = 180`) evenly spaced along its perimeter, starting at the top. Morphing is then just `lerp` between matching points. A polygon with `k` vertices (and an inner radius for stars) is sampled by walking its edges by arc length; the circle is sampled by angle. The echo is the same morph evaluated at `t - 0.25`, stroked instead of filled.

## Knobs

- Shape sequence (any polygon/star; add custom paths by resampling them).
- Point count N (more = smoother curves).
- Rotation per stage; colours.
- Echo delay or off.

## Pitfalls

- Start every shape's sampling at the same angle (top) or the morph twists inside out.
- Equal point spacing by arc length, not by vertex index, or corners bunch up.
- Hold each shape long enough (≥0.4 s) to be recognised.

## Pairs well with

`motion-liquid-blob`, `motion-logo-land`, `motion-seal-spin`, `motion-swiss-grid`
