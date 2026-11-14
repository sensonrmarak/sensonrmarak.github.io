---
name: motion-layer-explode
description: "An exploded axonometric view: a UI or product separates into stacked layers floating apart in 3D, each labelled with a leader line, then compresses back together. Use for architecture of an app or system, design anatomy, 'what's inside', tech stacks, product teardowns and layered-explanation scenes."
---

# Layer Explode

A screen seen in isometric (rotateX 55°, rotateZ −40°). Its four layers (background, layout grid, content cards, floating UI) lift apart vertically with a staggered back-ease, revealing each plane. Thin leader lines with mono labels extend to the right of each layer. Finally they settle back into one flat screen.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: flat composite screen fades in, already isometric.
- 0.8–2.0 s: layers separate upward (stagger 0.12 s).
- 1.8–2.8 s: labels and leader lines draw in per layer.
- 4.2–5.2 s: layers collapse back together; labels fade.
- 5.2–6.0 s: hold on the composite.

## How it's built

CSS 3D: a container with `rotateX(55deg) rotateZ(-40deg)` and `preserve-3d`; each layer is an absolutely positioned plane with `translateZ(gap·i·k)`. Labels are 2D elements outside the 3D container. Their anchor points are computed by projecting each layer's right-edge midpoint with the same matrix (here a small JS iso projection) so leader lines meet the layer edges.

## Knobs

- Layer contents and count.
- Gap between layers and the iso angle.
- Label text and side.
- Explode/collapse timing.

## Pitfalls

- `transform-style: preserve-3d` must be set on every ancestor between the layers and the rotated container.
- Semi-transparent layers help depth read; fully opaque top layers hide the rest.
- Keep the leader lines horizontal; diagonal leaders look messy.

## Pairs well with

`motion-blueprint-draw`, `motion-iso-city`, `motion-cube-fold`, `motion-swiss-grid`
