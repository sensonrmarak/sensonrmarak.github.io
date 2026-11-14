---
name: motion-before-after
description: "A before/after comparison with a draggable-style divider that wipes across, revealing the improved version, labelled and with a handle. Use for redesigns, product upgrades, photo/edit results, AI enhancement, cleanup, makeovers, A/B outcomes and 'old way vs new way' scenes."
---

# Before After

Two versions of the same layout sit exactly on top of each other: a grey, cluttered 'before' and a clean, colourful 'after'. A white vertical divider with a round handle sweeps from left to right with an overshoot, then back to centre. 'BEFORE' and 'AFTER' pills sit in the corners of each side.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: frame fades up showing BEFORE fully.
- 0.8–2.4 s: divider sweeps to 85 % (in-out).
- 2.6–3.6 s: divider returns to 50 % with a back ease and holds.
- 3.6–6.0 s: a tiny handle nudge (±12 px) at 4.4 s to invite the eye.

## How it's built

Both panels fill the same box; the AFTER panel is clipped with `clip-path: inset(0 0 0 X%)` where X follows the divider. The divider is a 4 px bar plus a round handle with arrow glyphs, translated to the same X. Use real screenshots or photos in the two panels for an actual comparison; keep them pixel-aligned.

## Knobs

- Divider path (keyframes of X over time).
- Orientation (vertical or horizontal wipe).
- Panel content: images, UI or video.
- Labels and handle style.

## Pitfalls

- The two images must be the same size and registration or the wipe shows a jump.
- Clip the AFTER layer, don't resize it; resizing distorts.
- Don't park the divider at the exact centre of a face or product.

## Pairs well with

`motion-cursor-tour`, `motion-card-flip`, `motion-count-up`, `motion-dot-wipe`
