---
name: motion-donut-ring
description: "An animated donut chart whose segments sweep in one after another with gaps and rounded ends, a centre number counting up and a legend that ticks in. Use for market share, budgets, survey results, time splits, portfolio allocation, percentages and any part-of-a-whole data."
---

# Donut Ring

A thick ring on paper. Segments draw clockwise from 12 o'clock one at a time, each in its own colour with a small gap between them. The centre shows the hero percentage counting up from 0; legend rows slide in beside the ring as each segment lands.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: faint track ring fades in.
- 0.6–3.2 s: segments sweep in sequence (each ~0.7 s, overlapping 0.15 s).
- 0.6–3.0 s: centre number counts up to the hero value.
- Each segment's legend row slides in when its sweep ends.
- 3.6–4.2 s: hero segment pops outward 14 px; hold.

## How it's built

SVG circles with `stroke-dasharray = "len gap"` where `len = value·C` (C = circumference). Rotation offsets each segment to start where the previous ended (`rotate(start·360 - 90)`). To sweep, scale `len` by `E.inOut(k)`. The hero pop is a translate along the segment's mid-angle. Numbers use `Math.round(lerp(0, v, E.out(k)))` with tabular figures so they don't jitter.

## Knobs

- Data (values sum to 1), colours, labels.
- Ring radius, thickness and gap size.
- Sweep order and speed.
- Hero segment and centre label.

## Pitfalls

- Account for the gap in each segment's length or segments overlap at the ends.
- Round linecaps extend past the dash; subtract stroke-width from each length.
- Use `font-variant-numeric: tabular-nums` for counting numbers.

## Pairs well with

`motion-count-up`, `motion-bars-3d`, `motion-radar-morph`, `motion-swiss-grid`
