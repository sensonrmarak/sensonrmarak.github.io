---
name: motion-tile-grids
description: "A full-screen grid of square tiles that ripple in a diagonal colour wave (lime → orange → red), flip and scale, then settle into a pixel picture or word. Use for transitions, chapter openers, 'systems' or 'grid' moments, pixel/mosaic reveals, brand patterns and rhythmic beat sections."
---

# Tile Grids

Small rounded squares fill the frame. A wave sweeps diagonally from the top-left: tiles pop larger, rotate 90° and shift colour from lime through orange to red as the crest passes. A second wave from the centre leaves behind a picture: tiles inside a bitmap heart stay accent, the rest drop back to dark.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–2.2 s: diagonal wave crosses the grid (tile scale and colour).
- 2.4–4.0 s: radial wave from the centre; tiles in the bitmap settle accent.
- 4.0–6.0 s: picture holds; tiles breathe ±4 % on a slow sine.

## How it's built

Each tile `(c, r)` has two wave phases: `p1 = seg(t, 0.2 + (c + r)·0.035, …)` for the diagonal wave and `p2` from its distance to the centre. Crest strength is `sin(π·p)`; scale, rotation and a 3-stop colour ramp come from it. The final state comes from a small bitmap (rows of 0/1 strings) mapped to the grid; tiles in the shape take the accent once `p2` passes 0.5.

## Knobs

- Tile size/gap and grid dimensions.
- Wave directions, speeds, colour ramp.
- Bitmap picture (heart, letter, logo mark).
- Rotation on crest (0° to 180°).

## Pitfalls

- Canvas, not DOM: a full 1080p grid is ~1,000+ tiles.
- Design the bitmap at the grid's resolution; scaling it blurs the picture.
- Use the crest curve (sin πp) so tiles return to rest, or the frame ends noisy.

## Pairs well with

`motion-pixel-build`, `motion-dot-wipe`, `motion-wave-dots`, `motion-halftone-wave`
