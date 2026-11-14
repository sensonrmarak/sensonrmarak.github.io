---
name: motion-halftone-wave
description: "A printed-halftone dot field that renders a lit 3D ring and ripples, dot size driven by shading, with red accent dots in the shadows. Use for 'systems' chapters, retro-print and newspaper looks, editorial tech, Vox-style backgrounds, audio pulses and abstract showreel beats."
---

# Halftone Wave

A regular grid of dots on black. Dot size encodes brightness of an underlying image: a softly lit torus ring that rotates its light, plus a ripple that passes through. Bright areas are big white dots; the background dots stay tiny and some turn accent red in a checker of the darker zones, like a two-ink print.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–1.0 s: dots grow in from size 0, centre first.
- Continuous: the light direction on the ring orbits once over the clip.
- 2.0–3.5 s: a ripple crosses outward from the centre, inflating dots.
- 4.5–6.0 s: the ring slowly 'breathes' its radius.

## How it's built

Sample a brightness function `b(x, y, t)` at each grid cell and draw a dot of radius `maxR·√b` (area ∝ brightness, like real halftone). The ring is a 2D torus field: distance to a circle `|d - R|` gives the tube; a fake normal from that and a rotating light vector gives Lambert shading. Add a Gaussian ripple ring to `b`. Accent dots: where `b` is low and `(i + j)` is even, draw red at a fixed small size.

## Knobs

- Cell size (18–30 px) and max dot radius.
- The image function: swap the ring for text masks, a face (from an image) or a logo.
- Light orbit speed; ripple timing.
- Two-ink colours.

## Pitfalls

- Radius ∝ √brightness, not brightness, or mid-tones look too dark.
- Cell sizes below ~14 px at 1080p moiré in compressed video.
- Keep the dot grid fixed; moving the grid itself shimmers.

## Pairs well with

`motion-wave-dots`, `motion-paper-collage`, `motion-tile-grids`, `motion-dot-wipe`
