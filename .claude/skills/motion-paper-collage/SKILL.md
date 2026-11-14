---
name: motion-paper-collage
description: "Torn paper cutouts, halftone photo scraps, tape and a stamped headline slap onto a textured board in stop-motion steps. Use for Vox-style explainers, editorial and documentary scenes, zines, history, culture, scrapbook and handmade-feel motion."
---

# Paper Collage

A warm paper board with fibre texture. Pieces arrive with a 'slap': slight overshoot rotation, a drop shadow that tightens as they land, and a brief squash. Everything moves on 12 fps steps so it feels hand-animated. Torn edges come from jagged clip-paths; photos are halftone dots; strips of masking tape pin the corners.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.4 s: board fades up.
- 0.3–2.6 s: five pieces slap in 0.4 s apart (back ease, quantised to 12 fps).
- 2.8–3.6 s: headline label stamps in with a scale overshoot; tape strips drop.
- Continuous: everything 'boils', tiny 12 fps jitter of ±0.6°.

## How it's built

Quantise time first: `tq = Math.floor(t * 12) / 12`, then compute every tween from `tq`, which gives the stop-motion cadence for free. Each piece is a div with a generated jagged `clip-path: polygon(...)` (seeded, so it's stable), a `radial-gradient` halftone or flat colour, and a `drop-shadow` filter whose offset shrinks as the piece lands (it reads as height). The boil is a seeded per-frame rotation: `rng(seed + frameIndex)`.

## Knobs

- Frame cadence (12 fps; 8 for cruder, 24 for smoother).
- Overshoot rotation per piece and landing order.
- Halftone dot size/colour; swap in real photos with `mix-blend-mode:multiply`.
- Boil amplitude (0.6°).

## Pitfalls

- Quantise everything from the same `tq`, or smooth and stepped motion mix and look like a bug.
- Generate torn edges once (seeded), not per frame, unless you want the edge itself to boil.
- Keep the palette to 3–4 inks plus paper or it stops reading as print.

## Pairs well with

`motion-halftone-wave`, `motion-marker-draw`, `motion-kinetic-type`, `motion-typewriter`
