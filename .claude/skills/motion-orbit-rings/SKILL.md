---
name: motion-orbit-rings
description: "Tilted 3D orbit rings around a central core with satellites riding each ring, passing behind and in front of the core with correct depth. Use for ecosystems, integrations around a platform, solar-system metaphors, 'everything revolves around X', networks, atoms and space-themed openers."
---

# Orbit Rings

A glowing sphere in the centre. Four thin elliptical rings at different tilts draw on one after another; a coloured satellite rides each ring at its own speed. Where a ring passes behind the sphere it is hidden, so the system reads in 3D. Labels can ride with the satellites.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: core scales in with a soft halo.
- 0.4–2.0 s: rings draw on (each sweeps its full angle in 0.6 s, staggered 0.25 s).
- 1.0 s →: satellites launch, each at its own angular speed.
- Continuous: the whole system yaws slowly (0.15 rad/s).

## How it's built

Each ring is a circle of radius `r` in the XZ plane, tilted by `rot(p, tiltX, yaw, tiltZ)` and projected with `proj()`. Ring segments and satellites with `z > 0` (behind the centre plane) that fall inside the core's screen disc are skipped, which is all the occlusion needed. Draw order: back halves of rings, core, then front halves and satellites.

## Knobs

- Ring radii and tilts.
- Satellite speeds, colours, sizes; labels.
- Yaw speed; ring draw order.
- Core: plain sphere, logo or photo.

## Pitfalls

- Draw back halves before the core and front halves after, or rings cut across it.
- Give rings clearly different tilts; similar tilts read as a mess of lines.
- Keep satellite speeds incommensurate so they don't line up in a loop.

## Pairs well with

`motion-globe-arcs`, `motion-particle-sphere`, `motion-agent-swarm`, `motion-torus-wire`
