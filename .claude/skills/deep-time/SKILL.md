---
name: deep-time
description: Space-scale scenes: black holes, galaxies, star fields. Use when the user types /deep-time or asks for a deep time style animation. Writes a single HTML file.
---

# /deep-time

Render a cinematic space scene (default: a black hole).
- Black hole: dark event horizon circle, an orange-gold accretion disk of thousands of particle streaks orbiting (faster near the centre), and the lensed ring arching over the top and under the bottom of the shadow.
- Deep background star field with 3 parallax layers and slow twinkle; a few drifting dust particles.
- Warm palette #FF8A3D, #FFD27A on near-black; bloom by drawing glow layers with 'lighter' compositing.
- Optional halftone dot frame around the scene. Very slow camera push in over the loop.

## Output rules (all styles)
- One self-contained `index.html`: inline CSS and JS, no external assets, no libraries unless the user asks.
- Draw with `<canvas>` (2D, or WebGL only if needed). Size to the window, handle devicePixelRatio and resize.
- Default canvas 1080x1920 (vertical, for reels) unless the user names another size; ask nothing else first.
- Animation loops seamlessly (8 to 12 s) and is driven by one `render(t)` function from requestAnimationFrame, so a frame at any time t is reproducible.
- Respect `prefers-reduced-motion`: show one still frame.
- Put every number and label the user gives into the scene. Mark made-up numbers "example data".
- When done, open the file (or tell the user the path) and list the 3 knobs they can change at the top of the script (colours, speed, text).
