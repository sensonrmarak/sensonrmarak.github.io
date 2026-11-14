---
name: motion-logo-land
description: "An end-card logo landing: the mark drops in with squash and stretch, hits with a shockwave ring and particle burst, then the wordmark letters pop in one by one and a tagline fades up. Use for end cards, brand sign-offs, intros, product logo reveals, CTAs and the final beat of promos and showreels."
---

# Logo Land

A bold round mark falls from above, stretched tall while falling, squashes wide on impact, rebounds and settles. A thin accent ring shoots out from the impact and a dozen small particles spray outward. Wordmark letters rise in a quick stagger beside it; a mono tagline and URL fade in last.

Working example: `example.html` in this folder (5 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.2–0.7 s: mark falls (ease-in), stretched 0.8×1.25.
- 0.7 s: impact: squash 1.3×0.7, shockwave ring and particles start.
- 0.7–1.3 s: rebound and settle (elastic).
- 1.1–1.7 s: wordmark letters pop in, 0.05 s apart (back ease).
- 1.9–2.5 s: tagline fades up; hold to the end.

## How it's built

The fall is `y = lerp(-700, 0, E.in(k))`; while falling, scaleY 1.25 and scaleX 0.8 (stretch along the motion). At impact, a short squash curve (`sin` over 0.12 s) then `E.elastic` back to 1. The ring is a circle scaling 0 → 4 with fading opacity; particles are seeded angles moving out with `E.out`, falling slightly with gravity. Letters are spans with per-letter delays.

## Knobs

- Mark (swap the SVG for your logo) and wordmark text.
- Fall height and impact time; squash amount.
- Ring and particle colours/count.
- Tagline and URL.

## Pitfalls

- Squash and stretch must preserve area (scaleX ≈ 1/scaleY) or it looks rubbery.
- Transform origin at the bottom of the mark so it squashes onto the ground.
- Don't over-bounce a logo: one rebound is premium, three is cartoon.

## Pairs well with

`motion-seal-spin`, `motion-pixel-build`, `motion-shape-morph`, `motion-extrude-type`
