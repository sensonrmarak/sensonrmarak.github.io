---
name: motion-cube-fold
description: "A flat cube net (six squares in a cross) folds itself up into a 3D cube along its hinges, then the cube turns to show its faces. Use for packaging, 'it all comes together', product boxes, modular systems, origami/unboxing moments, assembling features into one product and playful 3D reveals."
---

# Cube Fold

Six coloured squares lie flat in a cross shape, tilted toward the camera. The side flaps rotate up around their shared edges one after another, the last flap closing like a lid, forming a crisp cube. The finished cube then rotates a quarter turn on two axes so three faces show, each with a big glyph.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: flat net drops in.
- 0.8–2.6 s: flaps fold, 0.25 s stagger (in-out), the lid last.
- 2.8–4.6 s: cube tumbles to a three-quarter view.
- 4.6–6.0 s: hold with a slow drift.

## How it's built

Nested CSS 3D: the centre face is the root; four faces are its children positioned on each edge with `transform-origin` on the shared edge, folding with `rotateX/rotateY(±90°·k)`. The lid is a child of one side face, hinged on that face's far edge, so it rides along and folds last. Every element needs `transform-style: preserve-3d`. The tumble rotates the root container.

## Knobs

- Face colours/content (logos, icons, photos).
- Fold order and stagger.
- Final view angles.
- Cube size.

## Pitfalls

- Every face in the chain needs `preserve-3d`, or children flatten into their parent.
- Never reuse the id `root` inside a scene: it is the composition root's id in HyperFrames and in these examples.
- Fold all flaps toward the same side (same sign relative to their hinge) or the cube turns inside out.
- Don't put `filter` or `overflow:hidden` on any face: both flatten 3D.
- No borders on faces: children are positioned from the padding box, so a border shifts every hinge. Use an inset box-shadow for edges.

## Pairs well with

`motion-layer-explode`, `motion-cube-stack`, `motion-card-flip`, `motion-logo-land`
