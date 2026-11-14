"""Generate motion-* skills (SKILL.md + example.html) from recipe batches."""
import importlib.util, os, sys, glob, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]

KIT = r"""
// ---- motion kit (inlined so the file stands alone) ----
const W = 1920, H = 1080;
const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x);
const seg = (t, a, b) => clamp((t - a) / (b - a));          // 0..1 progress of t through [a,b]
const lerp = (a, b, k) => a + (b - a) * k;
const E = {
  lin: x => x,
  in: x => x * x * x,
  out: x => 1 - (1 - x) ** 3,
  inOut: x => (x < 0.5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2),
  expo: x => (x >= 1 ? 1 : 1 - 2 ** (-10 * x)),
  back: x => { const c = 1.70158; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2; },
  elastic: x => (x <= 0 ? 0 : x >= 1 ? 1 : 2 ** (-10 * x) * Math.sin((x * 10 - 0.75) * 2.0944) + 1),
  bounce: x => { const n = 7.5625, d = 2.75;
    if (x < 1 / d) return n * x * x; if (x < 2 / d) return n * (x -= 1.5 / d) * x + 0.75;
    if (x < 2.5 / d) return n * (x -= 2.25 / d) * x + 0.9375; return n * (x -= 2.625 / d) * x + 0.984375; },
};
function rng(seed) { let s = seed >>> 0; return () => { s = (s + 0x6d2b79f5) | 0;
  let t = Math.imul(s ^ (s >>> 15), 1 | s); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
function ctx2d(id) { const c = document.getElementById(id); c.width = W; c.height = H; return c.getContext("2d"); }
function rot(p, ax, ay, az = 0) { let [x, y, z] = p, c, s;
  c = Math.cos(ax); s = Math.sin(ax); [y, z] = [y * c - z * s, y * s + z * c];
  c = Math.cos(ay); s = Math.sin(ay); [x, z] = [x * c + z * s, -x * s + z * c];
  c = Math.cos(az); s = Math.sin(az); [x, y] = [x * c - y * s, x * s + y * c];
  return [x, y, z]; }
function proj(p, f = 1400, cx = W / 2, cy = H / 2) { const k = f / (f + p[2]); return [cx + p[0] * k, cy + p[1] * k, k]; }
function mix(c1, c2, k) { const a = parseInt(c1.slice(1), 16), b = parseInt(c2.slice(1), 16);
  const ch = sh => Math.round(lerp((a >> sh) & 255, (b >> sh) & 255, k));
  return `rgb(${ch(16)},${ch(8)},${ch(0)})`; }
const C = { ink: "#0e0e0e", paper: "#efe9df", accent: "#ff4a1c", blue: "#2433ff",
  pink: "#f4a7c4", yellow: "#ffc21a", lime: "#c6ff3d", white: "#ffffff" };
// ---- end kit ----
"""

BOOT = r"""
// ---- boot: HyperFrames timeline + browser preview ----
(function () {
  const root = document.getElementById("root");
  const fit = () => { const k = Math.min(innerWidth / W, innerHeight / H); root.style.transform = k < 1 ? `scale(${k})` : ""; };
  fit(); addEventListener("resize", fit);
  // In HyperFrames (GSAP loaded): one paused timeline whose tween calls renderAt with the scene's local time.
  if (window.gsap) { const id = root.dataset.compositionId, tl = gsap.timeline({ paused: true });
    tl.to({ p: 0 }, { p: 1, duration: DUR, ease: "none", onUpdate: () => renderAt(tl.time()) }, 0);
    window.__timelines = window.__timelines || {}; window.__timelines[id] = tl; }
  const q = new URLSearchParams(location.search);
  const start = () => {
    if (q.has("play")) { const s0 = performance.now();
      const loop = () => { renderAt(((performance.now() - s0) / 1000) % DUR); requestAnimationFrame(loop); }; loop(); }
    else renderAt(parseFloat(q.get("t")) || 0);
  };
  renderAt(parseFloat(q.get("t")) || 0);
  document.fonts.ready.then(start);  // re-render once the bundled fonts are in
})();
"""

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
@font-face {{ font-family:"Archivo Black"; src:url("../motion-core/fonts/archivo-black.woff2") format("woff2"); font-weight:400 900; }}
@font-face {{ font-family:"JetBrains Mono"; src:url("../motion-core/fonts/jetbrains-mono-400.woff2") format("woff2"); font-weight:400; }}
@font-face {{ font-family:"JetBrains Mono"; src:url("../motion-core/fonts/jetbrains-mono-700.woff2") format("woff2"); font-weight:500 900; }}
@font-face {{ font-family:"Playfair Display"; src:url("../motion-core/fonts/playfair-display-italic.woff2") format("woff2"); font-style:italic; }}
:root {{ --ink:#0e0e0e; --paper:#efe9df; --accent:#ff4a1c; --blue:#2433ff; --pink:#f4a7c4; --yellow:#ffc21a; --lime:#c6ff3d;
  --display: "Archivo Black","Arial Black","Helvetica Neue",Arial,sans-serif; --mono: "JetBrains Mono",ui-monospace,Menlo,monospace;
  --serif: "Playfair Display",Georgia,"Times New Roman",serif; }}
html, body {{ margin:0; background:#111; overflow:hidden; }}
#root {{ position:relative; width:1920px; height:1080px; overflow:hidden; background:{bg}; transform-origin:0 0;
  font-family: var(--display); color: var(--ink); }}
canvas {{ position:absolute; inset:0; width:100%; height:100%; display:block; }}
{css}
</style>
</head>
<body>
<div id="root" data-composition-id="{slug}" data-width="1920" data-height="1080" data-duration="{dur}">
{html}
</div>
<script>
{kit}
const DUR = {dur};
{js}
{boot}
</script>
</body>
</html>
"""

def bullets(items):
    return "\n".join(f"- {i}" for i in items)

SKILL = """---
name: motion-{slug}
description: "{desc}"
---

# {title}

{look}

Working example: `example.html` in this folder ({dur} s, 1920×1080, no dependencies). Open it with `?play` to loop it in a browser, or `?t=2.5` to freeze one frame. Read `../motion-core/SKILL.md` once for the shared palette, easing and the HyperFrames / Remotion porting steps.

## Beats

{beats}

## How it's built

{build}

## Knobs

{knobs}

## Pitfalls

{pitfalls}

## Pairs well with

{pairs}
"""

def load_batches():
    recipes = []
    for path in sorted(glob.glob(os.path.join(HERE, "batch*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        recipes.extend(mod.RECIPES)
    return recipes

def main():
    recipes = load_batches()
    seen = set()
    for r in recipes:
        assert r["slug"] not in seen, r["slug"]; seen.add(r["slug"])
        d = os.path.join(OUT, "motion-" + r["slug"]); os.makedirs(d, exist_ok=True)
        desc = r["desc"].replace('"', "'")
        with open(os.path.join(d, "SKILL.md"), "w") as f:
            f.write(SKILL.format(slug=r["slug"], title=r["title"], desc=desc, look=r["look"].strip(), dur=r["dur"],
                beats=bullets(r["beats"]), build=textwrap.dedent(r["build"]).strip(), knobs=bullets(r["knobs"]),
                pitfalls=bullets(r["pitfalls"]), pairs=", ".join(f"`motion-{p}`" for p in r["pairs"])))
        with open(os.path.join(d, "example.html"), "w") as f:
            f.write(HTML.format(title=r["title"], slug="motion-" + r["slug"], bg=r.get("bg", "var(--paper)"), dur=r["dur"],
                css=textwrap.dedent(r.get("css", "")).strip(), html=textwrap.dedent(r.get("html", "")).strip(),
                kit=KIT.strip(), js=textwrap.dedent(r["js"]).strip(), boot=BOOT.strip()))
    print(len(recipes), "recipes written")

if __name__ == "__main__":
    main()
