---
name: motion-chat-thread
description: "A messaging conversation that plays out: typing-indicator dots, bubbles springing in on alternating sides, timestamps and the thread scrolling up as it grows. Use for AI assistant demos, customer support, testimonials as chats, dialogue-driven explainers, texting stories and 'ask it anything' product moments."
---

# Chat Thread

A phone-sized chat column centred in frame. Incoming messages (white, left) are preceded by a three-dot typing bubble that bounces; outgoing (blue, right) pop straight in. Each bubble springs from its tail corner. As the thread fills, older messages slide up smoothly.

Working example: `example.html` in this folder (7 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.3 s: message 1 (them) after 0.6 s of typing dots.
- 1.6 s: reply (me).
- 2.4–3.4 s: typing, then a longer answer.
- 4.2 s: reply; 5.0–5.8 s typing, then final message with an emoji-free punchline.
- Thread scrolls to keep the newest bubble in view.

## How it's built

A script list `[{who, text, at, typing}]`. For each message, visibility and spring scale come from `t - at` (`E.back` over 0.35 s, origin at the tail corner). The typing bubble shows during `[at - typing, at)` with three dots bouncing via phase-offset `sin`. Scroll: sum the heights of visible messages after measuring once, and ease the column's translateY to keep the latest bottom at a fixed line.

## Knobs

- Script: who, text, times, typing durations.
- Bubble colours, corner radius, max width.
- Spring strength; scroll anchor line.
- Show/hide avatars and timestamps.

## Pitfalls

- Measure bubble heights once after fonts load; never measure inside renderAt.
- Typing time should scale with message length (~25 ms/char) to feel real.
- Keep messages short; a chat is skimmed, not read.

## Pairs well with

`motion-typewriter`, `motion-command-palette`, `motion-notifications`, `motion-cursor-tour`
