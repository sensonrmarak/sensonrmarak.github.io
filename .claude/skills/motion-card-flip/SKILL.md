---
name: motion-card-flip
description: "A row of cards that flip over in 3D one after another, lifting toward the camera mid-flip, to reveal answers, stats or the new version on the back. Use for reveals, quiz answers, myths vs facts, old vs new, features, flashcards and 'turn the card' storytelling."
---

# Card Flip

Three tall cards face-down with a question or 'before' label. One by one they flip around the vertical axis: lifting (scale 1.08) and casting a bigger shadow at 90°, then settling with a small overshoot on the back face, which is a saturated colour with a big number.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: cards slide up into place.
- 1.0–1.9 s: card 1 flips (back ease); 1.6–2.5 s card 2; 2.2–3.1 s card 3.
- 3.4–6.0 s: hold; a subtle 2° parallax tilt follows a slow sine.

## How it's built

Each card has `transform-style: preserve-3d` with two faces; the back face starts at `rotateY(180deg)` and both faces use `backface-visibility: hidden`. The card's `rotateY = 180·E.back(k)`. Lift is `1 + 0.08·sin(π·k)`, so it's highest exactly edge-on, which hides the moment the faces swap. The shadow grows with the same curve.

## Knobs

- Card count, size and gap.
- Flip axis (Y for left-right, X for top-bottom).
- Stagger and overshoot strength.
- Front/back content.

## Pitfalls

- The back face must be pre-rotated 180° or its content renders mirrored.
- Never put `filter` or `opacity < 1` on the 3D card itself: both flatten `preserve-3d` and the back face never shows. Shadow the faces instead.
- Perspective on the parent, not each card, so all cards share a vanishing point.
- Overshoot past 180° briefly shows the front edge; keep it small (back ease 1.2–1.7).

## Pairs well with

`motion-card-fan`, `motion-count-up`, `motion-before-after`, `motion-swiss-grid`
