---
name: motion-line-draw
description: "A single continuous one-line illustration draws itself with a visible pen nib leading the stroke, then a label writes in. Use for minimalist explainers, ideas and inspiration, hand-drawn icons, signature moments, onboarding illustrations and elegant 'one stroke' reveals."
---

# Line Draw

One unbroken ink line wanders, loops and resolves into a lightbulb with a little flourish. A small accent dot (the pen nib) rides the head of the stroke. When the line finishes, the bulb's glow fills behind it and a word fades up beneath.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.2–3.8 s: line draws with an ease-in-out, nib leading.
- 3.8–4.4 s: nib shrinks away; soft yellow glow scales up behind the bulb.
- 4.2–5.0 s: caption slides up.
- 5.0–6.0 s: hold.

## How it's built

One SVG `<path>`, `stroke-dasharray = L`, `stroke-dashoffset = L·(1-k)`. The nib position is `path.getPointAtLength(L·k)`. Calling that per frame is fine for a single path. Draw speed matters more than duration: ease-in-out makes it feel hand-drawn (slow start, confident middle, careful finish).

## Knobs

- The path (any single-stroke SVG: draw in Figma/Illustrator with one path).
- Stroke width (5–8 px) and linecap round.
- Draw duration and easing.
- Glow colour; caption text.

## Pitfalls

- Multiple sub-paths (`M` in the middle) jump; join them into one path for the one-line look.
- `getTotalLength` once at setup; `getPointAtLength` per frame is OK for one path.
- Hide the nib when k = 0 or 1, or it sits as a stray dot.

## Pairs well with

`motion-blueprint-draw`, `motion-marker-draw`, `motion-flow-line`, `motion-typewriter`
