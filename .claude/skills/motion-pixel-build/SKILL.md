---
name: motion-pixel-build
description: "A word or logo assembles out of hundreds of square pixels that fly in from a scattered cloud and snap into place column by column, then a shine sweeps across. Use for 'building' and 'creating' metaphors, logo reveals, game/retro titles, digital transformation, assembly and data-to-insight moments."
---

# Pixel Build

A cloud of small squares hangs scattered and dim. In a left-to-right wave they fly to their target positions (eased, with slight rotation that settles to 0), turning from blue to accent as they land, until the word is complete. A diagonal highlight band sweeps across the finished word.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: scattered pixels fade in, drifting slowly.
- 0.6–3.0 s: pixels fly to targets; delay by target x plus a seeded jitter.
- 3.2–4.0 s: shine band sweeps left to right.
- 4.0–6.0 s: hold; pixels breathe ±1 px on a sine for life.

## How it's built

Render the word once to an offscreen canvas, sample it on a grid (every 14 px) and keep cells whose alpha > 128: those are the targets. Each target gets a seeded start position and rotation. Position is `lerp(start, target, E.expo(k))` with `k` from a delay proportional to target x. Colour mixes blue → accent with `k`. The shine adds brightness where `x + y·0.5` is near a moving line.

## Knobs

- Word or logo (any canvas-drawable text/image).
- Pixel size and gap (14 px cell, 11 px square).
- Wave direction and spread of the start cloud.
- Shine on/off and colour.

## Pitfalls

- Wait for the font before sampling the offscreen text or you build the fallback font.
- More than ~3,000 pixels gets slow in canvas preview; increase the cell size.
- Expo ease makes pixels arrive crisply; linear looks floaty.

## Pairs well with

`motion-tile-grids`, `motion-logo-land`, `motion-particle-sphere`, `motion-scramble-decode`
