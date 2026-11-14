---
name: motion-carousel-ring
description: "Cards arranged on a 3D ring that rotates in confident steps, bringing each card to the front where it scales up and sharpens while the rest recede. Use for portfolios, product lineups, case studies, testimonials, templates, galleries and 'browse the collection' moments."
---

# Carousel Ring

Eight image cards stand on an invisible circular track seen slightly from above. The ring turns one card at a time with an ease-in-out and a tiny settle; the front card is full-size and bright, side cards angle away and dim, back cards are small and faint. A caption under the front card updates each step.

Working example: `example.html` in this folder (7 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.8 s: ring scales up from 0.8 and fades in.
- 1.0, 2.2, 3.4, 4.6 s: step rotations of 45° (0.7 s each, in-out).
- Caption swaps at each step midpoint.
- 5.8–7.0 s: hold on the final card with a slow 3° drift.

## How it's built

Cards are children of a `preserve-3d` ring: `rotateY(i·45°) translateZ(R)`. The ring's `rotateY` is a step function: the sum over steps of `45°·E.inOut(seg(t, step_k, step_k + 0.7))`. Per card, the facing angle `cos(θ_i + ring)` drives opacity and brightness (computed, not via backface). The caption text is chosen by the current step index.

## Knobs

- Card count, ring radius, camera tilt (rotateX on the stage).
- Step times and duration; continuous spin as an alternative.
- Card art (images), caption list.
- Dim strength for side/back cards.

## Pitfalls

- Cards facing away show mirrored; dim them heavily or hide when `cos < -0.2`.
- Use step rotation for content, continuous only for ambience.
- Large radius plus strong perspective distorts the side cards; keep perspective ≥ 2000 px.

## Pairs well with

`motion-card-fan`, `motion-type-ring`, `motion-phone-trio`, `motion-marquee-brands`
