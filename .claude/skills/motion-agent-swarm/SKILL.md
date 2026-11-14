---
name: motion-agent-swarm
description: "A central orchestrator node spawns AI agent nodes that fly out, connect with links, pass glowing task packets back and forth and tick off as done. Use for multi-agent AI, automation pipelines, distributed work, 'your team of AI agents', orchestration, workflows and parallel processing scenes."
---

# Agent Swarm

A glowing core node in the centre. Eight agent nodes burst outward on curved paths into a ring, each trailing a link back to the core. Bright packets travel out along the links, agents pulse while 'working' (a spinning arc), then flash to a check mark and send a packet back. Labels in mono under each agent.

Working example: `example.html` in this folder (7 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.6 s: core scales in with a halo.
- 0.6–1.8 s: agents spawn outward 0.1 s apart (back ease along a curved path).
- 1.8–2.6 s: packets travel core → agents.
- 2.4–4.8 s: agents work (spinner arcs), finishing at seeded times.
- On finish: check mark, colour flips to lime, packet returns to core.
- 5.6–7.0 s: core pulses 'DONE', hold.

## How it's built

Canvas. Agent `i` has a ring position at angle `2πi/8`; its spawn path is a quadratic curve from the core with a perpendicular bend. Each agent has seeded `start` and `finish` times. Packets are dots at `lerp(core, agent, E.inOut(p))` with a short fading trail (draw 6 copies at slightly earlier p). A spinner is an arc whose start angle is `t·6`. All state is derived from `t` and the per-agent times.

## Knobs

- Agent count, ring radius, labels.
- Spawn stagger; per-agent work durations (seeded).
- Packet speed and colour; trail length.
- Done colour (lime) and the core's final label.

## Pitfalls

- Spread finish times; agents finishing together looks fake.
- Too many simultaneous packets is noise; cap ~8 visible.
- Keep labels short (one word) at this size.

## Pairs well with

`motion-flow-line`, `motion-orbit-rings`, `motion-chat-thread`, `motion-command-palette`
