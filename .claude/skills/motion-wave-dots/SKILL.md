---
name: motion-wave-dots
description: "A full-frame grid of dots that ripples with radial and travelling sine waves, dots growing, shifting and changing colour with the wave height. Use for audio/voice visualisation, data pulses, rhythm/beat sections, ambient tech backgrounds, 'signal' and 'ripple effect' metaphors."
---

# Wave Dots

A dense, even grid of round dots. A ripple expands from the centre, so dots swell and lift as the crest passes, coloured from blue at rest to accent at the peak. A second, slower diagonal wave interferes, so the pattern never looks mechanical.

Working example: `example.html` in this folder (6 s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

- 0.0–0.8 s: dots fade in from the centre outward.
- 0.6 s, 2.4 s, 4.2 s: three ripples launch from the centre.
- Continuous: diagonal swell wave travelling left to right.
- 5.2–6.0 s: amplitude eases down to calm.

## How it's built

For every grid point, wave height `h = Σ ripple_k + swell`. A ripple is a Gaussian ring: `exp(-((d - c·(t - t_k))/w)²) · decay`, where `d` is distance from the centre. Swell is `sin(x·0.012 + y·0.006 - t·2)`. Dot radius, vertical offset and colour all come from `h`. Pure function of `(x, y, t)`, so it scrubs and loops cleanly.

## Knobs

- Grid spacing (36 px) and dot size range.
- Ripple times, speed `c` and width `w`.
- Colour ramp (rest → crest).
- Swap the centre for a moving source (e.g. follow a cursor path).

## Pitfalls

- ~1,500 dots is fine in canvas; DOM dots that many will crawl.
- Clamp radius ≥ 0.5 px or dots vanish and the grid looks broken.
- Align ripple launches to the beat if there's music.

## Pairs well with

`motion-halftone-wave`, `motion-radar-morph`, `motion-terrain-mesh`, `motion-dot-wipe`
