---
name: motion-particle-sphere
description: "Thousands of particles swirl in from chaos and assemble into a rotating sphere that breathes with noise, then morph into a torus ring. Use for AI/neural visuals, data and 'big picture' moments, global community, energy/science scenes, logo-adjacent 3D beats and showreel particle chapters."
---

# Particle Sphere

Particles start scattered across the frame. They converge onto a Fibonacci sphere, which rotates slowly; each point is pushed in and out by a travelling wave so the surface ripples. Near particles are larger and paper-white, far ones small and accent-tinted. Late in the clip the sphere flows into a torus.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.5 s: scattered cloud fades in.
- 0.5–2.2 s: particles converge to the sphere (staggered by index).
- 2.2–4.2 s: sphere rotates; surface ripple.
- 4.2–5.4 s: morph sphere → torus.
- 5.4–6.0 s: torus holds and spins.

## How it's built

Precompute per particle: a seeded chaos position, its Fibonacci-sphere point and its torus point (same index → stable morph). Position = chaos → sphere (`E.inOut` with index stagger), then sphere → torus. Apply ripple `1 + 0.06·sin(4·lat + t·3)` radially, rotate with `rot()`, project with `proj()`, then sort by depth and draw squares sized by the projected scale.

## Knobs

- Particle count (2,000–5,000).
- Target shapes (sphere, torus, text sampled to 3D points).
- Ripple amplitude and speed; rotation speed.
- Colour by depth or by index.

## Pitfalls

- Depth-sort every frame or near/far particles overlap wrongly.
- Use squares (`fillRect`), not arcs, for thousands of particles: much faster.
- Give every particle a stable target index so morphs don't shuffle.

## Pairs well with

`motion-torus-wire`, `motion-helix`, `motion-orbit-rings`, `motion-pixel-build`
