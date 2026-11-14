---
name: motion-phone-orbit
description: "A 3D phone mockup turns in space while feature cards orbit around it on an ellipse, passing in front of and behind the device. Use for app launches, product promos, feature highlights, mobile UI showcases and 'here is the app' hero shots."
---

# Phone Orbit

A rounded phone with a live-looking UI screen sits centre frame, slowly yawing in 3D. Three small cards (stat, avatar, chart) circle it on a tilted ellipse; they shrink and dim when behind the phone and grow when in front, so depth reads without a 3D engine.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.8 s: phone rises from below with a back-ease, already turning.
- 0.4–1.4 s: cards pop in at their orbit positions (scale 0→1, staggered).
- 0.8–5.4 s: phone yaws −28°→+28°, cards complete about 1.2 orbits.
- 5.4–6.0 s: everything settles; phone faces camera for the end frame.

## How it's built

CSS 3D: the phone is a div with `transform-style: preserve-3d` under a `perspective` parent; `rotateY` comes from `lerp(-28, 28, E.inOut(...))`. Cards are 2D: each sits at angle `θ = base + t*speed` on an ellipse `x = R·cosθ, y = r·sinθ`. Depth `z = sinθ` sets `scale`, `opacity` and `z-index` (in front when `sinθ > 0`). The screen is plain HTML so it can be swapped for a real screenshot (`<img>`).

## Knobs

- Orbit radii (R 620 px, r 120 px) and tilt (the r/R ratio).
- Orbit speed (turns per clip).
- Phone yaw range; keep under ±35° or the screen becomes unreadable.
- Replace `.screen` content with a real UI screenshot.

## Pitfalls

- Swap z-index exactly when sinθ crosses 0, or a card pops through the phone.
- Don't rotate the phone more than ±35°: the screen is the product.
- Keep cards out of the phone's silhouette at the end frame.

## Pairs well with

`motion-phone-trio`, `motion-phone-scroll`, `motion-notifications`, `motion-count-up`
