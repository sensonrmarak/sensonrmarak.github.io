---
name: motion-dot-wipe
description: "A transition where a grid of dots swells from one point until it covers the screen, the scene switches underneath, and the dots shrink away to reveal the next scene. Use for scene and chapter transitions, before/after switches, brand-colour wipes, playful cuts and pattern-based reveals."
---

# Dot Wipe

Scene A (paper, ink headline) is overtaken by a wave of ink dots growing outward from the lower-left; they grow until they merge into solid ink. Behind the cover the scene changes; the dots then shrink in the same wave order, revealing Scene B (accent background, paper headline).

Working example: `example.html` in this folder (4 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: Scene A holds.
- 0.6–1.7 s: dots grow in a wave from the origin until full cover.
- 1.7 s: scene swap (hidden).
- 1.8–2.9 s: dots shrink in the same order, revealing Scene B.
- 2.9–4.0 s: Scene B holds.

## How it's built

Canvas overlay above two DOM scenes. Each dot's growth phase is `seg(t, a + d·k, a + d·k + 0.45)` where `d` is its distance to the origin. Radius goes to `cell·0.75` (≥ √2/2 of the cell, so neighbours overlap into full cover). Swap scene visibility at the instant every dot is fully grown. The shrink uses the same delays, so the wave reads as one gesture.

## Knobs

- Origin point (corner, centre, a button's position).
- Cell size (bigger = chunkier, more graphic).
- Wave speed and per-dot growth time.
- Cover colour (ink, accent, or the next scene's colour).

## Pitfalls

- Max radius must be ≥ 0.71 × cell or gaps remain at full cover.
- Swap scenes only when the last dot is fully grown, or the swap flashes through.
- Use the same order for grow and shrink; reversing it looks like a rewind.

## Pairs well with

`motion-tile-grids`, `motion-halftone-wave`, `motion-before-after`, `motion-kinetic-type`
