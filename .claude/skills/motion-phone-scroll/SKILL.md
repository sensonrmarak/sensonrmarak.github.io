---
name: motion-phone-scroll
description: "A phone whose feed scrolls with real momentum (a fling that decelerates), cards parallaxing, a thumb-tap that likes a post with a heart burst, beside a headline. Use for social apps, content feeds, e-commerce browsing, 'endless scroll' commentary, app demos and creator-economy explainers."
---

# Phone Scroll

A phone on the right third of the frame, tilted 6°. Its feed flings upward quickly then decelerates like iOS momentum scrolling, overshoots slightly and settles. A translucent thumb circle taps a post; a heart pops and bursts into small particles. A bold headline sits left.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: phone slides in from the right; headline rises.
- 0.8–2.6 s: fling: fast start, exponential decay.
- 2.6–3.0 s: small rubber-band settle.
- 3.4 s: tap indicator; 3.5–4.1 s heart pop and burst.
- 4.4–5.8 s: a second, gentler scroll; hold.

## How it's built

Momentum is `y = v0·τ·(1 - e^(-t/τ))`, the closed form of exponential friction, so it scrubs perfectly. A short settle uses a damped sine. Image tiles inside cards translate at 0.9× the feed speed for parallax. The heart is an SVG path scaled with an elastic ease; burst particles are 10 dots on radial lines with seeded angles.

## Knobs

- Fling velocity v0 and friction τ.
- Feed content (swap blocks for real screenshots).
- Tap time/position; like colour.
- Phone tilt and headline copy.

## Pitfalls

- Linear scroll looks like a slideshow; always use the exponential decay curve.
- Keep the tapped post fully visible at the tap moment.
- Don't scroll and zoom the phone at the same time.

## Pairs well with

`motion-phone-orbit`, `motion-phone-trio`, `motion-notifications`, `motion-chat-thread`
