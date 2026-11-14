---
name: motion-terrain-mesh
description: "A wireframe landscape of noise-driven hills that the camera glides over, lines tinted by height, synthwave or topographic. Use for data landscapes, exploration, 'the road ahead', synthwave/retro scenes, Joy-Division ridgelines, AI/latent-space visuals and ambient backgrounds."
---

# Terrain Mesh

A perspective grid of lines stretches to a horizon. Hills rise and fall as the camera flies forward; low ground is ink-blue, peaks glow accent orange. A sun disc with scanline cuts sits on the horizon for the synthwave variant.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–1.0 s: terrain amplitude grows from flat to full.
- Continuous: camera moves forward 1.2 grid rows per second.
- 2.5–6.0 s: horizon sun rises slightly; slow camera bob.

## How it's built

Grid `cols × rows` in world space. Height `h = noise(x*0.12, (z + travel)*0.12)` from a seeded 2D value noise (smooth interpolated lattice), so moving `travel` scrolls the hills toward the camera with no popping. Project with a simple pinhole: `sx = cx + x*f/z`, `sy = horizon + (camY - h)*f/z`. Draw rows back to front, each as a polyline filled with background below it (`fill` then `stroke`) so nearer ridges hide farther ones: that hidden-line trick is what makes it read as solid.

## Knobs

- Noise scale (0.12) and amplitude (hill height).
- Rows/cols density (line count vs. speed).
- Colour ramp low→high; sun on/off.
- Fill under each row on (solid, Joy Division) or off (pure wireframe).

## Pitfalls

- Use a lattice noise keyed on integer world coordinates; re-seeding per frame flickers.
- Draw strictly back to front or the occlusion breaks.
- Clip rows with z ≤ near plane to avoid huge projected values.

## Pairs well with

`motion-wave-dots`, `motion-tunnel-grid`, `motion-flow-line`, `motion-halftone-wave`
