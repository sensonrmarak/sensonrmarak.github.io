---
name: motion-torus-wire
description: "A wireframe torus (donut) tumbling in 3D with depth-shaded lines that twists and breathes, drawn in pure canvas with no 3D library. Use for tech/sci-fi scenes, 'dimension' or 'depth' chapters in a showreel, loading states, abstract 3D brand moments and math visuals."
---

# Torus Wire

A torus built from rings of lines tumbles slowly on two axes. Lines near the camera are bright and thick, far lines thin and dim, so it reads as 3D without lighting. Mid-clip the tube twists (a phase offset around the ring), turning the wireframe into a spiralling knot-like form before relaxing.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–1.0 s: torus draws on ring by ring.
- Continuous: rotation 0.5 rad/s on X, 0.8 rad/s on Y.
- 2.0–4.0 s: twist rises to a full turn, then relaxes by 5.0 s.
- 5.0–6.0 s: tube radius breathes in slightly; hold.

## How it's built

Parametric torus `p(u,v) = ((R + r·cos v)·cos u, r·sin v, (R + r·cos v)·sin u)`, with a twist term `v + twist·u`. Draw `U` rings (constant u) and `V` rings (constant v) as polylines. For each segment, depth from the rotated z sets `lineWidth` and alpha: no z-buffer needed for lines. Rotate with `rot()` and project with `proj()` from the kit.

## Knobs

- Major/minor radius (R, r) and ring counts (U, V).
- Twist amount and timing.
- Rotation speeds; colour (single accent or gradient by u).
- Line width range (near vs. far).

## Pitfalls

- Sort isn't needed for additive-looking wires, but heavy alpha on many lines muddies: keep far lines under 0.15 alpha.
- Ring counts above ~60×30 slow canvas preview.
- Keep twist an integer number of turns at rest, or the mesh won't close.

## Pairs well with

`motion-particle-sphere`, `motion-helix`, `motion-orbit-rings`, `motion-tunnel-grid`
