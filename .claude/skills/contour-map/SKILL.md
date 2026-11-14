---
name: contour-map
description: Your numbers as a 3D topographic mountain. Use when the user types /contour-map or asks for a contour map style animation. Writes a single HTML file.
---

# /contour-map

Turn the user's metric (default: monthly revenue, example data) into a growing 3D terrain.
- Beige paper look (#D9CFBF to #EFE8DC), a heightfield peak drawn as 20 to 30 contour lines (marching squares on a noise-plus-gaussian field), tilted in perspective.
- The peak height maps to the metric and grows over the loop from the first value to the last.
- A vertical ruler on the right with tick labels; an orange marker and a value chip that tick up with the peak.
- Thin dark lines, soft shading between contours, light fog at the bottom.

## Output rules (all styles)
- One self-contained `index.html`: inline CSS and JS, no external assets, no libraries unless the user asks.
- Draw with `<canvas>` (2D, or WebGL only if needed). Size to the window, handle devicePixelRatio and resize.
- Default canvas 1080x1920 (vertical, for reels) unless the user names another size; ask nothing else first.
- Animation loops seamlessly (8 to 12 s) and is driven by one `render(t)` function from requestAnimationFrame, so a frame at any time t is reproducible.
- Respect `prefers-reduced-motion`: show one still frame.
- Put every number and label the user gives into the scene. Mark made-up numbers "example data".
- When done, open the file (or tell the user the path) and list the 3 knobs they can change at the top of the script (colours, speed, text).
