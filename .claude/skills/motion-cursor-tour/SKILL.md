---
name: motion-cursor-tour
description: "A cursor glides through a product UI on eased curves, hovers, clicks with a ripple and the camera follows and zooms into each action. Use for SaaS demos, product walkthroughs, feature tours, onboarding, 'how it works in 3 clicks' and launch videos."
---

# Cursor Tour

A clean app window floats on a soft background. A macOS-style cursor travels on curved paths (never straight lines), slows into each target, presses (cursor scales to 0.85), a ring ripples out, and the UI responds: a button fills, a toggle slides, a card highlights. The whole window gently zooms toward the action.

Working example: `example.html` in this folder (7 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: window rises into place.
- 0.8–2.0 s: cursor travels to 'New project', clicks at 2.0 s; button fills.
- 2.4–3.6 s: cursor moves to the toggle, clicks at 3.6 s; toggle slides on.
- 4.0–5.2 s: cursor moves to the card, clicks at 5.2 s; card lifts and outlines.
- Camera: scale 1→1.25 centred on each target during each move, back to 1 at 6.2 s.

## How it's built

Waypoints `[{x,y,t}]`. Between two waypoints the cursor follows a quadratic Bézier whose control point is offset perpendicular to the segment, which gives the natural human curve, with `E.inOut` progress. A click is a 0.18 s window: cursor scale dips, a ring expands (scale 0→1, opacity 1→0), and the target's state switches at the click instant. The camera is a transform on the window wrapper: translate so the current target sits centre, scale up, all eased.

## Knobs

- Waypoints and click times.
- Curve bend (perpendicular offset, ±80 px).
- Camera zoom per step (1.15–1.4).
- Swap the mock UI for a real screenshot with hotspots.

## Pitfalls

- Straight-line cursor moves look robotic; always bend them.
- Change UI state exactly at the click frame, not before.
- Zooming and cursor moving at full speed together causes nausea: ease both.

## Pairs well with

`motion-command-palette`, `motion-chat-thread`, `motion-notifications`, `motion-before-after`
