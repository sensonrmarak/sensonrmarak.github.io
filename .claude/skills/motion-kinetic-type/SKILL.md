---
name: motion-kinetic-type
description: "Giant display words that slam in through masks with skew and motion blur, then the background flips colour on the hit word. Use for kinetic typography, title cards, 'MAKE IT MOVE' style openers, bold statement scenes, hooks and manifesto lines in a motion reel, promo or explainer."
---

# Kinetic Type

Huge heavy grotesque words fill the frame edge to edge. Each word rises out of an invisible mask with a hard expo ease, skewed and blurred while fast and crisp when it lands. On the key word the whole background snaps to the accent colour and the type inverts.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.2–1.6 s: words enter one by one, 0.18 s apart, each over 0.6 s (expo out).
- 2.4 s: background cuts from paper to accent; the type turns paper-white; a slow 1.00→1.06 push starts.
- 5.0–5.8 s: words exit upward in the same order (expo in), leaving a clean frame.

## How it's built

Each line is a block with `overflow:hidden`, so a word translated 110 % down is invisible: that is the mask. Per word, `k = E.expo(seg(t, start, start + 0.6))` drives `translateY((1-k)*110%)`, `skewY((1-k)*-14deg)` and a blur of `(1-k)*14px`, which fakes motion blur because blur is largest exactly when speed is largest. The colour flip is a hard cut, not a fade: hard cuts read as rhythm.

## Knobs

- Stagger (0.18 s) and per-word duration (0.6 s): shorter feels aggressive, longer feels editorial.
- Skew amount (−14°): 0 for calm, up to −25° for violent.
- Flip word index and accent colour.
- Font size: aim for the longest line at ~90 % of frame width.

## Pitfalls

- Blur on huge text is expensive in a browser preview; it renders fine frame by frame.
- Never fade text in on top of the mask; the mask is the reveal. Mixing both looks soft.
- Measure line widths with the real font loaded, or the edge-to-edge fit breaks.

## Pairs well with

`motion-scramble-decode`, `motion-marker-draw`, `motion-count-up`, `motion-swiss-grid`
