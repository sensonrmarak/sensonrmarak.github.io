---
name: motion-card-fan
description: "A stack of cards fans out like a hand of playing cards from a shared pivot, then one card lifts out and flips forward to the camera. Use for plan/pricing tiers, feature lists, portfolios, team members, product options, credit cards and 'pick one' choice moments."
---

# Card Fan

Five rounded cards start as a neat stack. They rotate around a pivot below the stack into a fan (−30° to +30°) with a slight stagger, like a dealer's spread. The middle card then rises, straightens and scales up while the others dim and drop back.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: stack drops in with a back ease.
- 0.8–2.0 s: cards fan out, 0.06 s stagger from the centre outward.
- 2.6–3.6 s: middle card lifts and scales to 1.1 (the low pivot adds lift); others dim to 60 % and sink.
- 3.6–6.0 s: hold with a slow float on the hero card.

## How it's built

Every card has `transform-origin: 50% 160%` (a pivot well below the card) so `rotate()` produces an arc, not a spin. Fan angle `θ_i = (i - mid)·15°·k`. The hero card's extra transform is layered after the fan rotation. Dimming is opacity plus a darker background mix, not a filter.

## Knobs

- Card count, fan spread (15° step), pivot depth (origin y).
- Which card becomes the hero and how far it lifts.
- Card designs (pricing, photos, credit cards).
- Stagger direction (centre-out or left-to-right).

## Pitfalls

- Pivot at the card centre makes a pinwheel, not a fan; push the origin down.
- Set z-index so the hero card is above the others once it lifts.
- Keep the card text horizontal-ish on the final frame (hero at 0°).

## Pairs well with

`motion-card-flip`, `motion-carousel-ring`, `motion-phone-trio`, `motion-count-up`
