---
name: motion-flow-line
description: "A curved process line that draws through a sequence of step nodes, each node lighting up and labelling as the head passes, then dashes keep flowing along the path. Use for processes and workflows, user journeys, pipelines, roadmaps, timelines, 'how it works' steps and onboarding flows."
---

# Flow Line

A smooth S-curve snakes across the frame through four circular nodes. The line draws from the first node; as the head reaches each node, the node fills accent with a pop and a numbered label rises beside it. Once complete, small dashes march along the line forever, showing flow direction.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.2–3.4 s: line draws through the path (in-out).
- Each node pops when the head reaches its path length.
- Labels rise 0.15 s after their node.
- 3.6 s →: marching dashes flow along the path (offset −t·120).

## How it's built

One SVG path for the route. Node positions are chosen as fractions of the path length (`getPointAtLength`), so they're exactly on the line and their trigger time is just `fraction ↔ progress`. The draw uses the dashoffset technique; the flow is a second copy of the path with a short dash pattern (`14 22`) and `stroke-dashoffset = -t·120`, faded in after the draw.

## Knobs

- Path shape and node fractions.
- Step labels; node size; colours.
- Draw duration; flow speed and dash pattern.
- Direction (reverse the path for right-to-left).

## Pitfalls

- Place nodes by path length, not by guessing coordinates, or they float off the line.
- Labels must not collide with the curve; alternate them above/below.
- Marching dashes faster than ~200 px/s strobe in video.

## Pairs well with

`motion-line-draw`, `motion-agent-swarm`, `motion-ribbon-twist`, `motion-blueprint-draw`
