---
name: motion-tunnel-grid
description: "An endless square tunnel of glowing grid lines rushing toward the camera, with rings, depth fog and a twist, like flying through a data corridor. Use for speed and momentum, 'deep dive', hyperspace/warp moments, transitions into a new section, tech openers and music-driven intense beats."
---

# Tunnel Grid

Concentric square frames recede to a vanishing point, joined by longitudinal lines along the walls. They stream toward the viewer; near frames are bright accent and thick, far ones fade into the black. The tunnel slowly rotates and bends (vanishing point drifts), and the speed surges mid-clip.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.8 s: tunnel fades up from black, slow.
- 0.8–2.5 s: speed ramps up.
- 2.5–3.5 s: surge: fastest, twist increases.
- 3.5–6.0 s: eases to a cruise; vanishing point drifts in a slow ellipse.

## How it's built

Frames sit at `z = (i - travel) mod span`, so they recycle seamlessly; `travel` is the integral of speed over time (computed analytically from the speed curve, or as a sum of eased segments) so scrubbing is exact. Each frame is a square of half-size `s` at depth z projected with `f/z`, rotated by `twist·z + t·0.2`. The vanishing point offset is a function of z (bend). Longitudinal lines connect corresponding corners and midpoints across frames.

## Knobs

- Tunnel shape (square, hexagon, circle) and frame spacing.
- Speed curve (cruise, surge) and twist.
- Bend amount (vanishing point drift).
- Colours and fog distance.

## Pitfalls

- Derive travel from a closed-form integral of the speed curve, not from frame-to-frame accumulation.
- Skip frames with z below the near plane; they explode to infinity.
- High speed + many lines strobes in 30 fps video; render at 60 fps or reduce line count.

## Pairs well with

`motion-terrain-mesh`, `motion-torus-wire`, `motion-wave-dots`, `motion-kinetic-type`
