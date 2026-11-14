---
name: motion-liquid-blob
description: "Glossy liquid metaballs that drift, merge and split like lava-lamp goo, with a gradient fill and highlight. Use for fluid/organic brand moments, AI or 'thinking' states, transitions, abstract backgrounds, merging ideas, and soft playful showreel beats."
---

# Liquid Blob

Five or six soft circles orbit and breathe; where they meet they fuse with a smooth neck instead of overlapping, then pinch apart again. The fused shape is filled with a pink→accent gradient and a soft specular highlight so it reads like glossy liquid.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–1.0 s: blobs grow from the centre and spread.
- 1.0–4.0 s: orbits cross: blobs merge into one mass around 2.6 s, then separate.
- 4.0–5.2 s: all blobs pull into one big drop.
- 5.2–6.0 s: drop holds and wobbles.

## How it's built

SVG 'goo' filter: blur the group (`feGaussianBlur stdDeviation=28`), then crank alpha contrast with `feColorMatrix values='… 0 0 0 38 -16'`. Overlapping blurred circles become one shape with smooth necks. Circle centres are sums of sines of `t` (Lissajous orbits), so they're deterministic. The gradient and a white highlight blob sit inside the filtered group so they're clipped to the goo shape.

## Knobs

- Blur (stdDeviation 20–40) and alpha contrast (38/−16): higher = tighter edges.
- Number of blobs, radii and orbit speeds.
- Gradient colours; highlight on/off.
- Merge moment: when orbit radii shrink toward 0.

## Pitfalls

- The filter region must be large (`x=-50% width=200%`) or edges clip.
- Filters are per-frame expensive in preview; keep blobs under ~12.
- Text can't go inside the filtered group: it will melt. Put it on top.

## Pairs well with

`motion-shape-morph`, `motion-particle-sphere`, `motion-ribbon-twist`, `motion-dot-wipe`
