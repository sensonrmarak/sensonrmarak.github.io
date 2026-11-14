---
name: motion-phone-trio
description: "Three phone mockups rise in staggered and splay into a fan, side phones angled in 3D, centre phone scrolling its screen. Use for app store screenshots in motion, multi-screen feature overviews, app launch hero shots and 'three key screens' explainers."
---

# Phone Trio

Three phones slide up from below one after another. The outer two rotate outward in 3D (±22°) and sit slightly behind; the centre phone is larger and its screen content scrolls up. Each phone has a different accent screen colour.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–1.2 s: phones rise 0.15 s apart (back ease).
- 1.0–2.0 s: side phones rotate out and slide apart.
- 2.0–5.0 s: centre screen scrolls; side screens tick their own small motion.
- 5.0–6.0 s: slight push-in, hold.

## How it's built

Three absolutely positioned phones under one `perspective` parent. Each frame computes `translate`, `rotateY` and `scale` from `t`. The centre screen is a tall inner column translated upward (`translateY(-scroll)`) with `overflow:hidden` on the screen. Swap the screen divs for real screenshots (`<img>` of a tall capture) to use it for a real app.

## Knobs

- Splay angle (±22°) and spacing.
- Rise stagger; centre phone scale (1.1).
- Scroll distance and timing.
- Screen images.

## Pitfalls

- Put the centre phone on top (z-index) or the side phones clip it when rotated.
- Scrolling + rotating + pushing together is too much: one motion at a time.
- Use real screenshots at ≥2× for crisp UI.

## Pairs well with

`motion-phone-orbit`, `motion-phone-scroll`, `motion-notifications`, `motion-card-fan`
