---
name: motion-notifications
description: "Phone-style notification banners drop in one after another with a spring, stacking and pushing older ones down and back, with app icons and a growing badge count. Use for social proof, 'your phone is blowing up', sales/order alerts, reminders, engagement and app-growth moments."
---

# Notifications

Rounded frosted banners slide down from the top centre with a springy overshoot. Each new one lands on top; older banners shift down, shrink slightly and fade, forming a neat 3D stack. A red badge in the corner counts the notifications.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.4 s, 1.0 s, 1.5 s, 1.9 s, 2.25 s, 2.55 s: notifications arrive, accelerating like a pile-up.
- Each arrival: 0.5 s spring from −160 px; previous stack steps down.
- 3.0–6.0 s: hold; the top banner gets a subtle highlight pulse at 3.4 s.

## How it's built

Banner `i` arrives at `T[i]`. For a time `t`, count arrivals `n` so far; banner `i`'s depth in the stack is `n-1-i`. Its target y, scale and opacity are functions of depth (`y = depth·26`, `scale = 1 - depth·0.05`, `opacity = 1 - depth·0.18`). Transitions between depths are eased using the time since the latest arrival, so the stack 'steps' on each new banner. The badge number is just `n`.

## Knobs

- Notification list (icon colour, app name, text) and arrival times.
- Stack depth visible (4) and step spacing.
- Spring strength (elastic vs. back ease).
- Badge on/off.

## Pitfalls

- Accelerating arrival times sell 'blowing up'; even spacing feels like a slideshow.
- Keep text short: two lines per banner max.
- Use made-up app names unless you have rights to real logos.

## Pairs well with

`motion-phone-orbit`, `motion-chat-thread`, `motion-count-up`, `motion-phone-scroll`
