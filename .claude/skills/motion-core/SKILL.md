---
name: motion-core
description: "Shared conventions and index for the 50 motion-* recipe skills (kinetic type, phone orbit, globe arcs, split flap, particle sphere, logo land and more): palette, easing, bundled fonts, the deterministic renderAt(t) pattern, and how to drop a recipe into HyperFrames or Remotion. Read this first when building a motion reel, showreel, promo or explainer from several motion recipes, or when choosing which motion recipe fits a scene."
---

# Motion core

Fifty motion-design recipes live next to this skill as `motion-<name>/`. Each has a `SKILL.md` (look, beat timing, how it's built, knobs, pitfalls) and a working `example.html`: 1920×1080, no dependencies, pure function of time. This file holds what they share.

## The contract every recipe follows

- **One pure function draws a frame:** `renderAt(t)`, where `t` is seconds. Everything visible is computed from `t` alone: no `Date.now()`, no `requestAnimationFrame` clock, no accumulated state, no unseeded `Math.random()`. Randomness comes from `rng(seed)`, and per-frame randomness from `rng(seed + Math.floor(t * fps))`. That's what makes a recipe scrub, loop and render frame-exactly.
- **Setup runs once:** measuring text, `getTotalLength()`, sampling bitmaps and building DOM happen once, outside `renderAt`. Anything that depends on font metrics is re-measured once fonts have loaded (`document.fonts`).
- **HyperFrames hook:** when GSAP is on the page, the example registers one paused timeline holding a single tween whose `onUpdate` calls `renderAt(tl.time())`. HyperFrames seeks each scene's timeline in that scene's local time, so a recipe starting at 5 s still sees t = 0 at its first frame. (An `hf-seek` listener receives film time, which is wrong for a scene that doesn't start at 0, so the examples don't use one.)
- **Preview:** open `example.html` in a browser. `?play` loops it in real time, `?t=2.5` freezes one frame, and no parameter shows t = 0.

## Shared kit (inlined at the top of every example)

| Helper | What it does |
|---|---|
| `seg(t, a, b)` | 0→1 progress of `t` through `[a, b]`, clamped. The backbone of every timeline. |
| `E.out / in / inOut / expo / back / elastic / bounce` | Easing curves; wrap a `seg()` in one. |
| `lerp(a, b, k)`, `clamp(x)`, `mix(hexA, hexB, k)` | Interpolate numbers and colours. |
| `rng(seed)` | Seeded PRNG (mulberry32); same seed, same sequence. |
| `rot(p, ax, ay, az)`, `proj(p, f)` | Rotate a 3D point; perspective-project it to the 1920×1080 frame. Enough for wireframes and particles without a 3D library. |
| `ctx2d(id)` | Sizes a canvas to 1920×1080 and returns its 2D context. |
| `C.ink / paper / accent / blue / pink / yellow / lime` | The palette (also the CSS variables `--ink`, `--paper`, …). |

## Look

- **Palette:** ink `#0e0e0e`, paper `#efe9df`, accent `#ff4a1c`, cobalt `#2433ff`, pink `#f4a7c4`, yellow `#ffc21a`, lime `#c6ff3d`. Use one accent per scene. Swap the palette per brand by editing the CSS variables and `C`.
- **Type:** Archivo Black (display), JetBrains Mono (labels, data) and Playfair Display Italic (serif accents). The bundled files in `fonts/` are under the SIL Open Font License, see `fonts/OFL-LICENSE.txt`. Examples load them from `../motion-core/fonts/`, so keep the folders side by side.
- **Motion:** expo-out for arrivals, back for playful pops, in-out for camera and morphs, hard cuts for colour changes. Land moves on beats; don't spread them evenly.

## Using a recipe in HyperFrames

Tested: two recipes ported this way rendered correctly as a 10 s film with `npx hyperframes render`.

1. Make a scene file `compositions/<id>.html` with everything inside `<template>`: copy the example's `<style>`, the `#root` markup and the `<script>`. Set `data-composition-id="<id>"` on `#root` (and use the same id on the host in `index.html`).
2. In the style, replace `#root { position:relative; width:1920px; height:1080px; …` with `#root { position:absolute; inset:0; …` and drop the `html, body` rule.
3. In the script, delete the boot block at the bottom and add the timeline yourself:
   ```js
   const tl = gsap.timeline({ paused: true });
   tl.to({ p: 0 }, { p: 1, duration: DUR, ease: "none", onUpdate: () => renderAt(tl.time()) }, 0);
   renderAt(0);
   window.__timelines["<id>"] = tl;
   ```
4. Load GSAP in `index.html`. If the CDN is unreachable, `npm i gsap` and use a local copy: `<script src="lib/gsap.min.js"></script>`.
5. Copy `fonts/*.woff2` into `assets/fonts/` and change the `@font-face` URLs from `../motion-core/fonts/` to `assets/fonts/`.
6. Run `npx hyperframes check --json`, then `npx hyperframes render`. The check also runs design rules worth knowing about:
   - Text must be at least 28 px, so raise small mono labels.
   - Paper text on the accent orange is 2.8:1 contrast. Use ink on accent, or a darker accent, for text that must be read.
   - Masked reveals (kinetic type lines, marker-draw lines) overflow their boxes on purpose; mark those elements with `data-layout-allow-overflow`.

## Using a recipe in Remotion

Put the example's markup in JSX with a `ref`, run the setup once in `useLayoutEffect(() => { … }, [])`, then call `renderAt(frame / fps)` in `useLayoutEffect(() => renderAt(frame / fps), [frame])`, using `useCurrentFrame()` and `useVideoConfig()`. Scope the `$` helpers to the ref if more than one recipe is on screen. Canvas recipes port best: the drawing code is unchanged.

## Chaining recipes into a reel

Every recipe starts and ends on a clean frame, so they cut together. A 15 s showreel is typically 6–8 recipes of 1.5–2.5 s each, trimmed by offsetting `t`: play `renderAt(t + inPoint)` for the slice you want. Match transitions with `motion-dot-wipe` or `motion-tile-grids`, put kinetic type between visual beats, and end on `motion-logo-land` or `motion-seal-spin`. The Vox and HyperFrames skills in this project cover narration, captions and sound.

## All recipes

| Recipe | Skill | Length | Typical use |
|---|---|---|---|
| 3D Bars | `motion-bars-3d` | 6 s | revenue/growth, comparisons, rankings |
| Agent Swarm | `motion-agent-swarm` | 7 s | multi-agent AI, automation pipelines, distributed work |
| Before After | `motion-before-after` | 6 s | redesigns, product upgrades, photo/edit results |
| Blueprint Draw | `motion-blueprint-draw` | 6 s | engineering, architecture, product design |
| Card Fan | `motion-card-fan` | 6 s | plan/pricing tiers, feature lists, portfolios |
| Card Flip | `motion-card-flip` | 6 s | reveals, quiz answers, myths vs facts |
| Carousel Ring | `motion-carousel-ring` | 7 s | portfolios, product lineups, case studies |
| Chat Thread | `motion-chat-thread` | 7 s | AI assistant demos, customer support, testimonials as chats |
| Command Palette | `motion-command-palette` | 7 s | developer tools, productivity apps, keyboard-first products |
| Count Up | `motion-count-up` | 6 s | milestones, revenue, users |
| Cube Fold | `motion-cube-fold` | 6 s | packaging, 'it all comes together', product boxes |
| Cube Stack | `motion-cube-stack` | 6 s | growth, building blocks, 'stacking up' |
| Cursor Tour | `motion-cursor-tour` | 7 s | SaaS demos, product walkthroughs, feature tours |
| Donut Ring | `motion-donut-ring` | 6 s | market share, budgets, survey results |
| Dot Wipe | `motion-dot-wipe` | 4 s | scene and chapter transitions, before/after switches, brand-colour wipes |
| Extrude Type | `motion-extrude-type` | 6 s | retro and bold titles, logo-like wordmarks, game and music titles |
| Flow Line | `motion-flow-line` | 6 s | processes and workflows, user journeys, pipelines |
| Globe Arcs | `motion-globe-arcs` | 6 s | global reach, network, shipping |
| Halftone Wave | `motion-halftone-wave` | 6 s | 'systems' chapters, retro-print and newspaper looks, editorial tech |
| Helix | `motion-helix` | 6 s | biotech, health, genetics |
| Iso City | `motion-iso-city` | 6 s | smart cities, real estate, infrastructure |
| Kinetic Type | `motion-kinetic-type` | 6 s | kinetic typography, title cards, 'MAKE IT MOVE' style openers |
| Layer Explode | `motion-layer-explode` | 6 s | architecture of an app or system, design anatomy, 'what's inside' |
| Line Draw | `motion-line-draw` | 6 s | minimalist explainers, ideas and inspiration, hand-drawn icons |
| Liquid Blob | `motion-liquid-blob` | 6 s | fluid/organic brand moments, AI or 'thinking' states, transitions |
| Logo Land | `motion-logo-land` | 5 s | end cards, brand sign-offs, intros |
| Marker Draw | `motion-marker-draw` | 6 s | emphasis in explainers, editorial and Vox-style scenes, quotes |
| Marquee Brands | `motion-marquee-brands` | 6 s | client logos, partners, integrations |
| Notifications | `motion-notifications` | 6 s | social proof, 'your phone is blowing up', sales/order alerts |
| Orbit Rings | `motion-orbit-rings` | 6 s | ecosystems, integrations around a platform, solar-system metaphors |
| Paper Collage | `motion-paper-collage` | 6 s | Vox-style explainers, editorial and documentary scenes, zines |
| Particle Sphere | `motion-particle-sphere` | 6 s | AI/neural visuals, data and 'big picture' moments, global community |
| Phone Orbit | `motion-phone-orbit` | 6 s | app launches, product promos, feature highlights |
| Phone Scroll | `motion-phone-scroll` | 6 s | social apps, content feeds, e-commerce browsing |
| Phone Trio | `motion-phone-trio` | 6 s | app store screenshots in motion, multi-screen feature overviews, app launch hero shots and 'three key screens' explainers. |
| Pixel Build | `motion-pixel-build` | 6 s | 'building' and 'creating' metaphors, logo reveals, game/retro titles |
| Radar Morph | `motion-radar-morph` | 6 s | skill profiles, product comparisons, competitive analysis |
| Ribbon Twist | `motion-ribbon-twist` | 6 s | flow and journey metaphors, brand ribbons, festive or premium openers |
| Scramble Decode | `motion-scramble-decode` | 6 s | secrets/security, AI 'thinking', product names |
| Seal Spin | `motion-seal-spin` | 5 s | 'certified', 'new', 'limited edition' |
| Shape Morph | `motion-shape-morph` | 6 s | 'transform/adapt' metaphors, logo builds, chapter transitions |
| Split Flap | `motion-split-flap` | 6 s | announcements, destinations, launches |
| Swiss Grid | `motion-swiss-grid` | 6 s | editorial and design-forward scenes, chapter cards, data headlines |
| Terrain Mesh | `motion-terrain-mesh` | 6 s | data landscapes, exploration, 'the road ahead' |
| Tile Grids | `motion-tile-grids` | 6 s | transitions, chapter openers, 'systems' or 'grid' moments |
| Torus Wire | `motion-torus-wire` | 6 s | tech/sci-fi scenes, 'dimension' or 'depth' chapters in a showreel, loading states |
| Tunnel Grid | `motion-tunnel-grid` | 6 s | speed and momentum, 'deep dive', hyperspace/warp moments |
| Type Ring | `motion-type-ring` | 6 s | skill lists, taglines, services |
| Typewriter | `motion-typewriter` | 7 s | terminal/command intros, chat-style reveals, quotes |
| Wave Dots | `motion-wave-dots` | 6 s | audio/voice visualisation, data pulses, rhythm/beat sections |

## Editing or adding recipes

The 50 recipe folders are generated. Each recipe's text and code live in `source/batch*.py`, and `source/gen.py` writes every `motion-*/SKILL.md` and `example.html` from them. To change a recipe, edit its entry and run `python3 source/gen.py <path-to>/.claude/skills`. Then check it with `node source/test.js <path-to>/.claude/skills <slug>`, which renders sample frames in Chromium and fails on console errors or non-deterministic frames. Editing a generated file directly works too, but the next regeneration overwrites it.
