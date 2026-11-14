---
name: motion-extrude-type
description: "Bold 3D extruded lettering whose depth grows out of flat type, then swings so the extrusion sweeps around, with a bright front face and shaded sides. Use for retro and bold titles, logo-like wordmarks, game and music titles, punchy end cards, '3D type' showreel moments and loud announcements."
---

# Extrude Type

A heavy word in paper-white sits flat. Its extrusion grows backward into a long, solid side in deep accent shades, as if pushed out of the screen. The light/camera then swings so the extrusion direction rotates from down-right to down-left, the side faces sliding around the letters. A hard drop shadow follows.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: flat word pops in (scale overshoot).
- 0.6–1.8 s: extrusion depth grows 0 → 60 layers.
- 2.0–4.4 s: extrusion angle swings from 35° to 145°.
- 4.6–6.0 s: hold; front face gets a slow shine sweep.

## How it's built

Canvas 'layer stack' extrusion: draw the word `n` times, offset 1.4 px further along the extrusion vector each time, from the back layer to the front, darkening as layers go back; then draw the front face on top. The extrusion vector `(cos a, sin a)` rotates over time. Cheap, crisp, no 3D engine. The shine is a gradient clipped to the front text (`globalCompositeOperation = 'source-atop'`).

## Knobs

- Word, font, size.
- Depth (layers × step) and extrusion colours.
- Swing angles and timing.
- Shadow and shine.

## Pitfalls

- Draw back-to-front; front-to-back hides the front face under the sides.
- 60–100 layers is enough; more just costs time.
- Wait for the font before drawing or the extrusion bakes the fallback.

## Pairs well with

`motion-kinetic-type`, `motion-logo-land`, `motion-seal-spin`, `motion-count-up`
