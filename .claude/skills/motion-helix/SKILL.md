---
name: motion-helix
description: "A rotating DNA-style double helix of glowing dots joined by rungs, depth-shaded and drawn in 3D on canvas. Use for biotech, health, genetics, 'in our DNA' brand values, science explainers, growth/evolution metaphors and elegant looping tech backgrounds."
---

# Helix

Two strands of dots spiral around a horizontal axis, joined by thin rungs. The helix rotates continuously; near dots are large and bright (one strand accent, one blue), far dots small and dim. It builds from left to right at the start and the rungs flash white one by one like a scan.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–1.6 s: helix builds left to right (dots and rungs appear by x).
- Continuous: rotation 1.4 rad/s around the long axis.
- 2.0–4.0 s: a white scan pulse runs along the rungs.
- 4.0–6.0 s: camera tilts 15° so the helix angles into depth.

## How it's built

For `i` in `0..N`, position along the axis `x = (i/N - 0.5)·L`, angle `a = i·0.32 + t·1.4`; strand A at `(x, R·cos a, R·sin a)`, strand B offset by π. Rotate the whole thing with a slow tilt via `rot()`, project with `proj()`. Sort all dots and rungs by depth (back to front) each frame (a few hundred items) and size/alpha them by projected scale `k`.

## Knobs

- Turns (angle step 0.32), radius R and length L.
- Dot count; strand colours.
- Scan pulse colour/speed.
- Tilt (flat side view vs. into-depth).

## Pitfalls

- Depth sort every frame; rotating helices change order constantly.
- Rungs drawn after both dots will cover the near dot; draw rung at its mid-depth.
- Too many turns looks like a spring, not DNA: about 4–6 turns across the frame.

## Pairs well with

`motion-particle-sphere`, `motion-torus-wire`, `motion-orbit-rings`, `motion-wave-dots`
