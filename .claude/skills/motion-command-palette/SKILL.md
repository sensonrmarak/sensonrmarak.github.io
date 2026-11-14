---
name: motion-command-palette
description: "A ⌘K command palette opens over a blurred app, a query types in, results filter live, the highlight moves down with arrow presses and Enter fires the action with a toast. Use for developer tools, productivity apps, keyboard-first products, AI command bars, search features and power-user demos."
---

# Command Palette

A dimmed, blurred app UI in the background. A centred palette springs open with a search field; key caps '⌘' and 'K' flash at the bottom. Letters type in, the result list narrows with items collapsing, a highlight bar slides between results, then Enter: the palette closes and a success toast slides up.

Working example: `example.html` in this folder (7 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.3 s: key caps ⌘ K flash; backdrop blurs and dims.
- 0.5–0.9 s: palette scales from 0.96 and fades in.
- 1.2–2.4 s: query 'depl' types; list filters from 6 to 2 items as letters arrive.
- 2.8 s: highlight moves down to 'Deploy preview'; 3.3 s: back up to 'Deploy to production'.
- 3.9 s: Enter: palette closes; 4.1–4.6 s toast slides up 'Deployed to production'.

## How it's built

DOM. All results exist; each has a `match` time (when the typed query stops matching it). After that time it collapses (height and opacity to 0 over 0.2 s). The query string at time `t` is the prefix of 'depl' by keystroke times. The highlight's y is the eased position of the selected index among the visible rows. Backdrop blur is a CSS `filter: blur()` on the app layer (fine here: it's static UI, not footage).

## Knobs

- Command list and query.
- Keystroke times; arrow presses; selected action.
- Theme (dark/light), accent colour.
- Toast text and position.

## Pitfalls

- Filter results at the exact keystroke frames; lagging lists look broken.
- Animate list height changes; jumping rows lose the eye.
- Show key caps for keyboard actions, since viewers can't see a keyboard.

## Pairs well with

`motion-cursor-tour`, `motion-typewriter`, `motion-chat-thread`, `motion-scramble-decode`
