---
name: motion-radar-morph
description: "A radar/spider chart with a sweeping scan line whose data polygon grows from the centre, then morphs from a 'before' profile to an 'after' profile with values updating. Use for skill profiles, product comparisons, competitive analysis, performance metrics, player stats, improvement over time and multi-axis data."
---

# Radar Morph

A hexagonal web of concentric rings and six spokes with mono labels at each tip. A bright sweep line rotates once, and the data polygon grows from the centre behind it in translucent blue. Then it morphs to a larger, differently shaped accent polygon ('after'), vertex dots riding along, numbers at each tip counting to new values.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.8 s: web rings and spokes draw on.
- 0.6–2.0 s: sweep line rotates 360°; 'before' polygon grows in its wake.
- 2.6–3.8 s: morph before → after (in-out), colour blue → accent.
- Values at each axis count during the morph.
- 4.0–6.0 s: hold; a faint 'before' outline remains for comparison.

## How it's built

SVG. Axis `i` is at angle `-90° + i·60°`; a value `v ∈ [0,1]` maps to `(cos·R·v, sin·R·v)`. The polygon's points are recomputed each frame from `lerp(before_i, after_i, E.inOut(k))`. The grow-in multiplies by the sweep reveal: each vertex appears when the sweep angle passes its axis. Numbers use rounded `lerp` of the real values.

## Knobs

- Axes (names, count) and the two datasets.
- Ring count and radius.
- Sweep on/off, colours.
- Keep or drop the 'before' ghost outline.

## Pitfalls

- Use the same axis order for both datasets, or the morph twists.
- Radar charts exaggerate area; label actual values.
- Six to eight axes max; more turns into a circle.

## Pairs well with

`motion-donut-ring`, `motion-wave-dots`, `motion-count-up`, `motion-orbit-rings`
