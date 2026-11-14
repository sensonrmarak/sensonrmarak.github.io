---
name: motion-seal-spin
description: "A circular badge seal with text running around its edge that stamps in with a punch, then spins slowly forever, with a scalloped border and a centre icon. Use for 'certified', 'new', 'limited edition', guarantees, awards, launch stickers, end cards, CTAs and premium brand marks."
---

# Seal Spin

A scalloped sticker seal in ink with paper text running around the rim ('• LIMITED EDITION • MADE WITH CODE'). It slams in from 2.5× scale with a slight rotation and a shockwave ring, settles, then the text ring keeps rotating slowly while the centre star stays still.

Working example: `example.html` in this folder (5 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.2–0.65 s: seal punches in (scale 2.5 → 1 with back ease, rotation −30° → 0).
- 0.45–1.1 s: shockwave ring expands and fades.
- Continuous after 0.6 s: text ring rotates 30°/s; scallop edge rotates −10°/s.
- 1.0–1.5 s: centre star pops in.

## How it's built

SVG: a scalloped polygon (radius alternating with a sine of angle·n), a `<textPath>` on a circle path for the rim text, and a centre star. Group transforms: whole seal for the punch; inner groups for the counter-rotations. The rim text length should fill the circle exactly: set `textLength` to the path length so the start and end meet.

## Knobs

- Rim text and font size; number of scallops.
- Rotation speeds (text vs. edge).
- Punch scale/rotation; shockwave on/off.
- Centre icon (star, logo, number).

## Pitfalls

- Set `textLength` to the circumference or there's a gap or overlap at the seam.
- Spin slowly (≤ 40°/s); fast spinning text is unreadable and strobes in video.
- Keep the seal's centre still while the rim spins: it anchors the eye.

## Pairs well with

`motion-logo-land`, `motion-shape-morph`, `motion-kinetic-type`, `motion-swiss-grid`
