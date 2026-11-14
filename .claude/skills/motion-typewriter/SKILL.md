---
name: motion-typewriter
description: "Text types itself character by character with human rhythm, a blinking caret, a realistic typo that gets backspaced and corrected, and each letter popping in. Use for terminal/command intros, chat-style reveals, quotes, prompts, hooks, 'what if…' questions and code or AI-generated-text scenes."
---

# Typewriter

A monospace line appears letter by letter with uneven timing (faster within words, pauses at spaces and punctuation). A wrong letter is typed, the caret pauses, two backspaces remove it and the correct text continues. A solid block caret blinks only when idle.

Working example: `example.html` in this folder (7 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.3 s: caret appears and blinks.
- 0.8–5.4 s: typing; a typo at ~2.6 s is backspaced at ~3.1 s.
- 5.4–7.0 s: caret blinks at the end; the last word turns accent at 5.8 s.

## How it's built

Precompute a keystroke list once: `[{t, op:'type'|'back', ch}]` with seeded jitter (base 55 ms per char, +180 ms after spaces, +350 ms after punctuation, ±25 ms noise). `renderAt(t)` replays all keystrokes with `time ≤ t` into a string: pure and scrub-safe. Each character is a span; the newest one gets a tiny scale pop based on its age. The caret blinks with `floor(t·2) % 2` only when the last keystroke is older than 0.4 s.

## Knobs

- Text, typo position and wrong letters.
- Base speed and pause lengths.
- Caret style (block, bar, underscore).
- Sound: a key click at each keystroke time (export the list).

## Pitfalls

- Never type with setInterval; scrubbing breaks. Replay from the keystroke list.
- Monospace keeps the caret from jittering horizontally.
- Keep lines under ~40 characters at this size or wrap deliberately.

## Pairs well with

`motion-scramble-decode`, `motion-chat-thread`, `motion-command-palette`, `motion-split-flap`
