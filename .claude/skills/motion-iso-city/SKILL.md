---
name: motion-iso-city
description: "An isometric city grid whose buildings rise out of the ground in a wave from the centre, with lit windows and roads. Use for smart cities, real estate, infrastructure, growth, platforms 'building' something, SimCity-style worlds and data-as-skyline scenes."
---

# Iso City

A diamond-shaped isometric block of land with a road grid. Buildings of varied heights extrude upward from the centre outward with a soft back-ease overshoot. Faces are three-tone (light top, mid left, dark right); window rows light up warm yellow after each building lands.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.5 s: ground plate and roads fade in.
- 0.4–3.4 s: buildings rise in a radial wave (delay ∝ distance from centre), 0.7 s each.
- 2.0–4.5 s: windows switch on in a random-but-seeded order.
- Continuous: slow camera drift upward 30 px.

## How it's built

Grid of plots; each has a seeded height. Isometric projection as in `motion-cube-stack`; a building is a box from z=0 to z=h·k where `k = E.back(seg(t, d·0.12, d·0.12 + 0.7))` and `d` is the plot's distance from centre. Painter's order: sort plots by `x + y` (constant, so sort once). Windows: rows of small parallelograms on the left and right faces, each with a seeded switch-on time.

## Knobs

- Grid size, plot spacing, road width.
- Height distribution (seeded) and hero tower.
- Wave origin (centre, corner) and speed.
- Palette: day (light) or night (navy ground, glowing windows).

## Pitfalls

- Draw a building's faces in order left, right, top or the top is hidden.
- Back-ease overshoot can poke through neighbours mid-rise; keep overshoot small.
- Too many windows is noise: 2–4 columns per face.

## Pairs well with

`motion-cube-stack`, `motion-bars-3d`, `motion-blueprint-draw`, `motion-globe-arcs`
