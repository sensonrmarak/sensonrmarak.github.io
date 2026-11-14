---
name: motion-bars-3d
description: "An isometric 3D bar chart whose prisms grow from the floor with staggered back-eases, value labels counting up on top and the winning bar highlighted. Use for revenue/growth, comparisons, rankings, survey results, KPIs and any 'numbers going up' data story."
---

# 3D Bars

Seven isometric prisms on a light floor grid, three-tone shaded. They grow upward left to right with a slight overshoot; a value label rides each bar's top and counts up. The tallest bar switches to the accent palette and gets a pointer label.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: floor grid fades in.
- 0.5–2.9 s: bars grow, 0.2 s stagger, 0.9 s each (back ease).
- Labels count with their bar.
- 3.2–3.8 s: top bar turns accent, callout drops in; others fade to 70 %.

## How it's built

Same isometric math as `motion-cube-stack` but each bar is one box with continuous height `h·E.back(k)`. Draw order: by x+y (back to front), then within a bar left face, right face, top. The label is canvas text placed at the projected top-centre. Highlight is a colour `mix()` driven by its own eased progress.

## Knobs

- Data values and category labels.
- Bar footprint, spacing and max height.
- Growth stagger and ease.
- Highlight rule (max, latest, chosen index).

## Pitfalls

- Overshoot pushes labels above the frame for tall bars; leave headroom.
- Iso bars exaggerate differences visually; label exact values.
- Don't rotate a 3D chart during the data reveal; viewers lose the comparison.

## Pairs well with

`motion-cube-stack`, `motion-count-up`, `motion-donut-ring`, `motion-iso-city`
