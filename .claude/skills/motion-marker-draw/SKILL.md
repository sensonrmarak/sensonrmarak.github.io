---
name: motion-marker-draw
description: "Hand-drawn annotations on top of text: a highlighter swipe behind a key word, a scribbled circle around another and a wobbly underline, drawn on in sequence. Use for emphasis in explainers, editorial and Vox-style scenes, quotes, key takeaways, headlines and 'pay attention to this' moments."
---

# Marker Draw

A big two-line headline in heavy ink. A translucent yellow highlighter bar sweeps left-to-right behind one word with a slight skew. A red marker loop circles a second word, overshooting its start like a real hand. A squiggly underline finishes the sentence.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–1.0 s: the three headline lines slide up into place.
- 1.0–1.6 s: highlighter sweeps behind 'never'.
- 1.8–2.6 s: red loop draws around 'twice'.
- 2.8–3.4 s: underline squiggle draws under the last line.
- 3.4–6.0 s: hold.

## How it's built

Text is HTML; annotations are an SVG overlay in the same coordinate space. The highlighter is a rect with `mix-blend-mode: multiply`, revealed by animating its `scaleX` from a left origin. The loop and underline are paths drawn with the dashoffset technique (`motion-line-draw`). Hand-feel comes from the paths themselves: slightly off-ellipse, overlapping ends, and a 2–3° rotation.

## Knobs

- Which words get which mark; marker colours.
- Stroke width (10–14 px) and roughness of the paths.
- Draw durations (0.5–0.8 s each).
- Highlighter opacity (0.6–0.8).

## Pitfalls

- Measure word positions after fonts load, then place the SVG marks; hard-coded positions break with a new font.
- Highlighter must sit behind the ink (multiply or lower z-index) or it greys the text.
- One mark at a time; simultaneous scribbles look chaotic.

## Pairs well with

`motion-kinetic-type`, `motion-paper-collage`, `motion-typewriter`, `motion-line-draw`
