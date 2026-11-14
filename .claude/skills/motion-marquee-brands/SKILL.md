---
name: motion-marquee-brands
description: "Rows of logo wordmarks scrolling endlessly in opposite directions with soft edge fades, a seamless 'trusted by' strip. Use for client logos, partners, integrations, press mentions, sponsors, tech stacks and social-proof sections of promos and showreels."
---

# Marquee Brands

Three rows of wordmarks in mixed type styles (bold sans, serif italic, mono, rounded) glide horizontally: top and bottom rows left, middle row right, at slightly different speeds. The edges fade to the background so logos appear and disappear softly. A small 'TRUSTED BY' label sits above.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: rows fade/slide in from slight offsets.
- Continuous: rows scroll at 120, 90 and 150 px/s; loops seamlessly.
- 3.0 s: middle row's centre logo turns accent for emphasis (optional).

## How it's built

Each row contains its logo list twice in a flex track. Offset `x = -((t·speed) mod trackWidth)`, where `trackWidth` is the width of one copy (measured once after fonts load). Because the second copy follows the first exactly, the wrap is invisible. Edge fades are a `mask-image: linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent)` on the row.

## Knobs

- Logo list per row (use SVG logos you have rights to, or wordmarks).
- Speeds and directions.
- Gap between logos; row count.
- Fade width.

## Pitfalls

- Measure one copy's width after fonts load or the loop jumps.
- Use real client logos only with permission; placeholders here are invented names.
- Keep logos visually equal in weight; one huge logo breaks the strip.

## Pairs well with

`motion-type-ring`, `motion-count-up`, `motion-notifications`, `motion-swiss-grid`
