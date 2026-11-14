---
name: motion-ribbon-twist
description: "A two-sided 3D ribbon that flows across the frame along a wavy path, twisting so its front and back colours flip, drawn with depth-sorted quads on canvas. Use for flow and journey metaphors, brand ribbons, festive or premium openers, 'connecting the dots', transitions and elegant abstract showreel moments."
---

# Ribbon Twist

A wide band snakes in from the left, following a sine-like path that drifts. Along its length it twists around its own centreline: one face is accent orange, the other is pale pink, so each half-twist flips the colour. Shading darkens faces turned away from the light. It draws on from the tail, then keeps flowing.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–1.8 s: ribbon draws on from the left edge (head advances along the path).
- Continuous: path phase flows; twist rate 2.5 turns across the ribbon.
- 3.0–4.5 s: twist accelerates, then relaxes.
- Continuous: slight camera roll.

## How it's built

Sample the centreline `c(u)` (u from 0 to 1) in 3D. At each sample, build a frame: tangent `T` (finite difference), a reference up vector, normal `N = up × T`, then rotate `N` around `T` by `twist(u, t)`. Edges are `c ± w·N`. Each quad between samples gets a face normal; its sign toward the camera picks the colour (front vs back) and its magnitude the shade. Sort quads by depth and fill back to front.

## Knobs

- Path shape (amplitude, frequency, drift), ribbon width.
- Twist turns and acceleration.
- Front/back colours; shading strength.
- Draw-on speed.

## Pitfalls

- Use a stable up vector (not parallel to the tangent) or the ribbon flips randomly.
- Depth-sort quads every frame; twisting changes order.
- Add a 1 px stroke in the fill colour to hide hairline seams between quads.

## Pairs well with

`motion-flow-line`, `motion-liquid-blob`, `motion-helix`, `motion-line-draw`
