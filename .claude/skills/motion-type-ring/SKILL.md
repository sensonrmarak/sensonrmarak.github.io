---
name: motion-type-ring
description: "Rows of text wrapped around an invisible 3D cylinder that spin in alternating directions, a rotating marquee tower of words. Use for skill lists, taglines, services, 'kinetic type' showreel moments, brand values and looping text sculptures."
---

# Type Ring

Three stacked rings of uppercase words orbit a vertical axis. Front-facing letters are bright paper, back-facing ones fade to a dim outline so the cylinder reads round. Alternate rows spin opposite ways; the whole tower tilts slightly toward camera.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.9 s: rings fade/scale in from the centre row outward.
- Continuous: rows rotate ±40°/s in alternating directions.
- 2.5–4.5 s: tower tilt eases from 18° to −10°.
- 4.5–6.0 s: middle row's accent word swings to the front and holds.

## How it's built

Per row, split the string into characters and place each on the cylinder: angle `a = i/n · 360°`, `transform: rotateY(a) translateZ(R)`, inside a `preserve-3d` row container whose `rotateY` is driven by `t`. Front/back is known analytically: `cos(a + rowAngle) > 0` → front; set colour and opacity per char each frame (cheap, < 200 chars). Use a monospace or tracked display face so spacing around the ring is even.

## Knobs

- Ring radius and characters per row (density).
- Row speeds and directions.
- Tilt range; text content per row.
- Back-face style: dim fill, outline (`-webkit-text-stroke`) or hidden.

## Pitfalls

- Pad the string so the ring closes cleanly (no gap or overlap where it wraps).
- `backface-visibility:hidden` breaks the dim back-face look; compute front/back yourself.
- Too many chars per ring tanks DOM performance; 60–80 per row is plenty.

## Pairs well with

`motion-marquee-brands`, `motion-kinetic-type`, `motion-carousel-ring`, `motion-helix`
