---
name: motion-globe-arcs
description: "A rotating dotted globe with glowing great-circle arcs that draw between cities and pulse at each end. Use for global reach, network, shipping, payments, users-worldwide, distributed systems and 'connected everywhere' scenes."
---

# Globe Arcs

Thousands of small dots form a sphere on black; back-facing dots are dimmed so the globe reads round. Bright accent arcs lift off the surface between city pairs, draw from start to end, leave a fading tail and ring the landing city with an expanding pulse.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–1.0 s: globe scales up from 0.6 with dots fading in from the centre.
- 1.0–4.6 s: six arcs launch 0.45 s apart, each drawing over 1.1 s.
- Continuous: globe rotates 0.35 rad/s around Y with a fixed 0.35 rad tilt.
- 4.6–6.0 s: arcs hold, tails fade, pulses settle.

## How it's built

Dots: a Fibonacci sphere (`N = 1800` evenly spread points). Each frame rotates them with `rot()` and projects with `proj()`; dots with `z > 0` (facing away) draw at low alpha. Arcs: cities are lat/lon → unit vectors; points along the arc are a normalised slerp between the two, pushed outward by `1 + h·sin(πu)` so the arc lifts. Draw the sub-range `[tail, head]` where `head = E.inOut(progress)`. Everything rotates with the globe, so arcs stick to their cities.

## Knobs

- City list and arc pairs (lat, lon in degrees).
- Arc height `h` (0.25 for long hauls, 0.1 for short).
- Dot count and size; rotation speed and tilt.
- Accent colour and glow (`shadowBlur`).

## Pitfalls

- Hide arc segments when they pass behind the globe (z > 0 and inside the disc) or they show through.
- Use real lat/lon if the scene names real places; viewers check.
- Keep `shadowBlur` modest: it's the slowest call in canvas 2D.

## Pairs well with

`motion-orbit-rings`, `motion-flow-line`, `motion-count-up`, `motion-radar-morph`
