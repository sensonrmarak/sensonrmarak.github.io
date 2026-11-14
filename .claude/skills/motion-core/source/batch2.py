RECIPES = [
# ---------------------------------------------------------------- liquid-blob
dict(slug="liquid-blob", title="Liquid Blob", dur=6, bg="var(--ink)",
desc="Glossy liquid metaballs that drift, merge and split like lava-lamp goo, with a gradient fill and highlight. Use for fluid/organic brand moments, AI or 'thinking' states, transitions, abstract backgrounds, merging ideas, and soft playful showreel beats.",
look="Five or six soft circles orbit and breathe; where they meet they fuse with a smooth neck instead of overlapping, then pinch apart again. The fused shape is filled with a pink→accent gradient and a soft specular highlight so it reads like glossy liquid.",
beats=["0.0–1.0 s: blobs grow from the centre and spread.",
       "1.0–4.0 s: orbits cross: blobs merge into one mass around 2.6 s, then separate.",
       "4.0–5.2 s: all blobs pull into one big drop.",
       "5.2–6.0 s: drop holds and wobbles."],
build="""
SVG 'goo' filter: blur the group (`feGaussianBlur stdDeviation=28`), then crank alpha contrast with `feColorMatrix values='… 0 0 0 38 -16'`. Overlapping blurred circles become one shape with smooth necks. Circle centres are sums of sines of `t` (Lissajous orbits), so they're deterministic. The gradient and a white highlight blob sit inside the filtered group so they're clipped to the goo shape.
""",
knobs=["Blur (stdDeviation 20–40) and alpha contrast (38/−16): higher = tighter edges.",
       "Number of blobs, radii and orbit speeds.",
       "Gradient colours; highlight on/off.",
       "Merge moment: when orbit radii shrink toward 0."],
pitfalls=["The filter region must be large (`x=-50% width=200%`) or edges clip.",
          "Filters are per-frame expensive in preview; keep blobs under ~12.",
          "Text can't go inside the filtered group: it will melt. Put it on top."],
pairs=["shape-morph", "particle-sphere", "ribbon-twist", "dot-wipe"],
css="""svg { position:absolute; inset:0; }""",
html="""
<svg viewBox="0 0 1920 1080">
  <defs>
    <filter id="goo" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="28" result="b"/>
      <feColorMatrix in="b" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 38 -16"/>
    </filter>
    <linearGradient id="gr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4a7c4"/><stop offset=".55" stop-color="#ff4a1c"/><stop offset="1" stop-color="#2433ff"/></linearGradient>
    <mask id="m"><g id="mg" filter="url(#goo)" fill="#fff"></g></mask>
  </defs>
  <rect width="1920" height="1080" fill="url(#gr)" mask="url(#m)"/>
  <g mask="url(#m)"><ellipse id="hi" cx="860" cy="430" rx="110" ry="60" fill="#fff" opacity=".35"/></g>
</svg>
""",
js="""
const mg = $("#mg"), NB = 6, blobs = [];
for (let i = 0; i < NB; i++) { const c = document.createElementNS("http://www.w3.org/2000/svg", "circle"); mg.appendChild(c); blobs.push(c); }
const R = [150, 120, 110, 95, 130, 85];
function renderAt(t) {
  const grow = E.back(seg(t, 0, 1)), gather = E.inOut(seg(t, 4.0, 5.2));
  const spread = 380 * (0.75 + 0.25 * Math.cos(t * 1.1)) * (1 - gather);
  let sx = 0, sy = 0;
  blobs.forEach((c, i) => {
    const a = i * 1.047 + t * (0.6 + i * 0.07) * (i % 2 ? -1 : 1);
    const x = 960 + Math.cos(a) * spread * (0.6 + 0.4 * Math.sin(t * 0.7 + i));
    const y = 540 + Math.sin(a * 1.3) * spread * 0.55;
    const wob = 1 + 0.06 * Math.sin(t * 6 + i) * seg(t, 5.2, 5.4);
    const r = R[i] * grow * lerp(1, 1.25, gather) * wob;
    c.setAttribute("cx", x.toFixed(1)); c.setAttribute("cy", y.toFixed(1)); c.setAttribute("r", Math.max(0, r).toFixed(1));
    sx += x; sy += y; });
  $("#hi").setAttribute("cx", (sx / NB - 70).toFixed(1)); $("#hi").setAttribute("cy", (sy / NB - 90).toFixed(1));
  $("#hi").setAttribute("opacity", (0.35 * grow).toFixed(2));
}
"""),

# ---------------------------------------------------------------- iso-city
dict(slug="iso-city", title="Iso City", dur=6, bg="#e8eef7",
desc="An isometric city grid whose buildings rise out of the ground in a wave from the centre, with lit windows and roads. Use for smart cities, real estate, infrastructure, growth, platforms 'building' something, SimCity-style worlds and data-as-skyline scenes.",
look="A diamond-shaped isometric block of land with a road grid. Buildings of varied heights extrude upward from the centre outward with a soft back-ease overshoot. Faces are three-tone (light top, mid left, dark right); window rows light up warm yellow after each building lands.",
beats=["0.0–0.5 s: ground plate and roads fade in.",
       "0.4–3.4 s: buildings rise in a radial wave (delay ∝ distance from centre), 0.7 s each.",
       "2.0–4.5 s: windows switch on in a random-but-seeded order.",
       "Continuous: slow camera drift upward 30 px."],
build="""
Grid of plots; each has a seeded height. Isometric projection as in `motion-cube-stack`; a building is a box from z=0 to z=h·k where `k = E.back(seg(t, d·0.12, d·0.12 + 0.7))` and `d` is the plot's distance from centre. Painter's order: sort plots by `x + y` (constant, so sort once). Windows: rows of small parallelograms on the left and right faces, each with a seeded switch-on time.
""",
knobs=["Grid size, plot spacing, road width.",
       "Height distribution (seeded) and hero tower.",
       "Wave origin (centre, corner) and speed.",
       "Palette: day (light) or night (navy ground, glowing windows)."],
pitfalls=["Draw a building's faces in order left, right, top or the top is hidden.",
          "Back-ease overshoot can poke through neighbours mid-rise; keep overshoot small.",
          "Too many windows is noise: 2–4 columns per face."],
pairs=["cube-stack", "bars-3d", "blueprint-draw", "globe-arcs"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), N = 9, s = 64, cs = Math.cos(Math.PI / 6), r0 = rng(21), plots = [];
for (let x = 0; x < N; x++) for (let y = 0; y < N; y++) { if (x % 3 === 1 && y % 3 === 1) continue;
  const road = x % 4 === 3 || y % 4 === 3; if (road) continue;
  const d = Math.hypot(x - N / 2 + 0.5, y - N / 2 + 0.5);
  plots.push({ x, y, h: 1 + r0() * 4 + (d < 1.6 ? 3 : 0), d, win: Array.from({ length: 24 }, () => 2 + r0() * 2.5) }); }
plots.sort((a, b) => (a.x + a.y) - (b.x + b.y));
function renderAt(t) {
  g.clearRect(0, 0, W, H);
  const ox = 960, oy = 300 - 30 * E.inOut(seg(t, 0, 6)), fade = E.out(seg(t, 0, 0.5));
  const P = (x, y, z) => [ox + (x - y) * cs * s, oy + (x + y) * 0.5 * s - z * s];
  const poly = (pts, col) => { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.closePath(); g.fillStyle = col; g.fill(); g.strokeStyle = col; g.stroke(); };
  g.globalAlpha = fade;
  poly([P(-0.3, -0.3, 0), P(N + 0.3, -0.3, 0), P(N + 0.3, N + 0.3, 0), P(-0.3, N + 0.3, 0)], "#c9d3e3");
  for (let i = 0; i <= N; i++) { if (i % 4 !== 3) continue;
    poly([P(i, 0, 0), P(i + 1, 0, 0), P(i + 1, N, 0), P(i, N, 0)], "#9aa6bb"); poly([P(0, i, 0), P(N, i, 0), P(N, i + 1, 0), P(0, i + 1, 0)], "#9aa6bb"); }
  g.globalAlpha = 1;
  for (const p of plots) { const k = E.back(seg(t, 0.4 + p.d * 0.45, 1.1 + p.d * 0.45)); if (k <= 0) continue;
    const h = p.h * k * 0.9, x0 = p.x + 0.12, y0 = p.y + 0.12, w = 0.76;
    poly([P(x0, y0 + w, h), P(x0 + w, y0 + w, h), P(x0 + w, y0 + w, 0), P(x0, y0 + w, 0)], "#7f8fb0");
    poly([P(x0 + w, y0, h), P(x0 + w, y0 + w, h), P(x0 + w, y0 + w, 0), P(x0 + w, y0, 0)], "#55658a");
    poly([P(x0, y0, h), P(x0 + w, y0, h), P(x0 + w, y0 + w, h), P(x0, y0 + w, h)], p.d < 1.6 ? C.accent : "#f4f6fb");
    const rows = Math.floor(h / 0.5);
    for (let rI = 0; rI < Math.min(rows, 12); rI++) for (let c = 0; c < 2; c++) { const on = t > p.win[(rI * 2 + c) % 24] + p.d * 0.2;
      const z0 = 0.25 + rI * 0.5, u0 = 0.15 + c * 0.35;
      poly([P(x0 + u0 * w, y0 + w, z0 + 0.25), P(x0 + (u0 + 0.22) * w, y0 + w, z0 + 0.25), P(x0 + (u0 + 0.22) * w, y0 + w, z0), P(x0 + u0 * w, y0 + w, z0)], on ? C.yellow : "#6d7c9c");
      poly([P(x0 + w, y0 + u0 * w, z0 + 0.25), P(x0 + w, y0 + (u0 + 0.22) * w, z0 + 0.25), P(x0 + w, y0 + (u0 + 0.22) * w, z0), P(x0 + w, y0 + u0 * w, z0)], on ? "#e0a800" : "#46557a"); } }
}
"""),

# ---------------------------------------------------------------- line-draw
dict(slug="line-draw", title="Line Draw", dur=6, bg="var(--paper)",
desc="A single continuous one-line illustration draws itself with a visible pen nib leading the stroke, then a label writes in. Use for minimalist explainers, ideas and inspiration, hand-drawn icons, signature moments, onboarding illustrations and elegant 'one stroke' reveals.",
look="One unbroken ink line wanders, loops and resolves into a lightbulb with a little flourish. A small accent dot (the pen nib) rides the head of the stroke. When the line finishes, the bulb's glow fills behind it and a word fades up beneath.",
beats=["0.2–3.8 s: line draws with an ease-in-out, nib leading.",
       "3.8–4.4 s: nib shrinks away; soft yellow glow scales up behind the bulb.",
       "4.2–5.0 s: caption slides up.",
       "5.0–6.0 s: hold."],
build="""
One SVG `<path>`, `stroke-dasharray = L`, `stroke-dashoffset = L·(1-k)`. The nib position is `path.getPointAtLength(L·k)`. Calling that per frame is fine for a single path. Draw speed matters more than duration: ease-in-out makes it feel hand-drawn (slow start, confident middle, careful finish).
""",
knobs=["The path (any single-stroke SVG: draw in Figma/Illustrator with one path).",
       "Stroke width (5–8 px) and linecap round.",
       "Draw duration and easing.",
       "Glow colour; caption text."],
pitfalls=["Multiple sub-paths (`M` in the middle) jump; join them into one path for the one-line look.",
          "`getTotalLength` once at setup; `getPointAtLength` per frame is OK for one path.",
          "Hide the nib when k = 0 or 1, or it sits as a stray dot."],
pairs=["blueprint-draw", "marker-draw", "flow-line", "typewriter"],
css="""svg { position:absolute; inset:0; } #cap { position:absolute; left:0; right:0; top:860px; text-align:center; font-size:72px; letter-spacing:-2px; }""",
html="""
<svg viewBox="0 0 1920 1080">
  <circle id="glow" cx="960" cy="420" r="230" fill="#ffc21a" opacity=".55"/>
  <path id="ln" fill="none" stroke="#0e0e0e" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"
    d="M380 760 C520 760 560 640 660 650 C760 660 720 780 820 770 C880 764 890 700 880 640 C860 560 780 520 780 420 C780 300 860 220 960 220 C1060 220 1140 300 1140 420 C1140 520 1060 560 1040 640 C1030 700 1040 764 1100 770 C1180 776 1170 700 1100 690 L880 690 L880 640 L1040 640 L1040 690 L1020 730 L900 730 C1060 730 1060 770 1020 770 L900 770 C860 770 860 810 900 810 L1020 810 C1100 810 1120 760 1240 760 C1340 760 1400 700 1540 700"/>
  <circle id="nib" r="13" fill="#ff4a1c"/>
</svg>
<div id="cap">One idea. One line.</div>
""",
js="""
const ln = $("#ln"), L = ln.getTotalLength(); ln.style.strokeDasharray = L;
function renderAt(t) {
  const k = E.inOut(seg(t, 0.2, 3.8));
  ln.style.strokeDashoffset = L * (1 - k);
  const p = ln.getPointAtLength(L * k), nk = k > 0 && k < 1 ? 1 : 1 - E.in(seg(t, 3.8, 4.1));
  $("#nib").setAttribute("cx", p.x); $("#nib").setAttribute("cy", p.y);
  $("#nib").setAttribute("r", (13 * (k > 0 ? nk : 0)).toFixed(2));
  const gk = E.back(seg(t, 3.8, 4.4)); $("#glow").setAttribute("r", (230 * gk).toFixed(1));
  const ck = E.out(seg(t, 4.2, 5.0)); $("#cap").style.opacity = ck; $("#cap").style.transform = `translateY(${(1 - ck) * 40}px)`;
}
"""),

# ---------------------------------------------------------------- phone-trio
dict(slug="phone-trio", title="Phone Trio", dur=6, bg="var(--paper)",
desc="Three phone mockups rise in staggered and splay into a fan, side phones angled in 3D, centre phone scrolling its screen. Use for app store screenshots in motion, multi-screen feature overviews, app launch hero shots and 'three key screens' explainers.",
look="Three phones slide up from below one after another. The outer two rotate outward in 3D (±22°) and sit slightly behind; the centre phone is larger and its screen content scrolls up. Each phone has a different accent screen colour.",
beats=["0.0–1.2 s: phones rise 0.15 s apart (back ease).",
       "1.0–2.0 s: side phones rotate out and slide apart.",
       "2.0–5.0 s: centre screen scrolls; side screens tick their own small motion.",
       "5.0–6.0 s: slight push-in, hold."],
build="""
Three absolutely positioned phones under one `perspective` parent. Each frame computes `translate`, `rotateY` and `scale` from `t`. The centre screen is a tall inner column translated upward (`translateY(-scroll)`) with `overflow:hidden` on the screen. Swap the screen divs for real screenshots (`<img>` of a tall capture) to use it for a real app.
""",
knobs=["Splay angle (±22°) and spacing.",
       "Rise stagger; centre phone scale (1.1).",
       "Scroll distance and timing.",
       "Screen images."],
pitfalls=["Put the centre phone on top (z-index) or the side phones clip it when rotated.",
          "Scrolling + rotating + pushing together is too much: one motion at a time.",
          "Use real screenshots at ≥2× for crisp UI."],
pairs=["phone-orbit", "phone-scroll", "notifications", "card-fan"],
css="""
.stage { position:absolute; inset:0; perspective:2400px; }
.ph { position:absolute; left:50%; top:50%; width:360px; height:740px; margin:-370px 0 0 -180px; border-radius:58px; background:#0b0b0b;
  box-shadow:0 50px 100px rgba(0,0,0,.3); }
.sc { position:absolute; inset:14px; border-radius:46px; overflow:hidden; }
.col { position:absolute; left:0; right:0; top:0; }
.blk { margin:22px; height:150px; border-radius:24px; background:rgba(255,255,255,.85); }
.blk.h { height:260px; background:rgba(0,0,0,.18); margin-top:80px; }
""",
html="""
<div class="stage">
  <div class="ph" id="p0"><div class="sc" style="background:var(--yellow)"><div class="col" id="k0"><div class="blk h"></div><div class="blk"></div><div class="blk"></div></div></div></div>
  <div class="ph" id="p2"><div class="sc" style="background:var(--blue)"><div class="col" id="k2"><div class="blk h"></div><div class="blk"></div><div class="blk"></div></div></div></div>
  <div class="ph" id="p1"><div class="sc" style="background:var(--accent)"><div class="col" id="k1"><div class="blk h"></div><div class="blk"></div><div class="blk"></div><div class="blk"></div><div class="blk"></div><div class="blk"></div><div class="blk"></div></div></div></div>
</div>
""",
js="""
const P = [$("#p0"), $("#p1"), $("#p2")];
function renderAt(t) {
  const sp = E.inOut(seg(t, 1.0, 2.0)), push = 1 + 0.05 * E.inOut(seg(t, 5, 6));
  [-1, 0, 1].forEach((side, i) => {
    const order = [0, 1, 2][i], rise = E.back(seg(t, order * 0.15, order * 0.15 + 1.0));
    const x = side * 470 * sp, ry = -side * 22 * sp, z = side ? -160 * sp : 0, s = (side ? 1 : 1.1) * push;
    P[i].style.transform = `translate3d(${x}px, ${(1 - rise) * 1100}px, ${z}px) rotateY(${ry}deg) scale(${s})`;
    P[i].style.zIndex = side ? 1 : 2; });
  $("#k1").style.transform = `translateY(${-560 * E.inOut(seg(t, 2.0, 5.0))}px)`;
  $("#k0").style.transform = `translateY(${-60 * E.inOut(seg(t, 2.6, 3.6))}px)`;
  $("#k2").style.transform = `translateY(${-90 * E.inOut(seg(t, 3.2, 4.4))}px)`;
}
"""),

# ---------------------------------------------------------------- marker-draw
dict(slug="marker-draw", title="Marker Draw", dur=6, bg="var(--paper)",
desc="Hand-drawn annotations on top of text: a highlighter swipe behind a key word, a scribbled circle around another and a wobbly underline, drawn on in sequence. Use for emphasis in explainers, editorial and Vox-style scenes, quotes, key takeaways, headlines and 'pay attention to this' moments.",
look="A big two-line headline in heavy ink. A translucent yellow highlighter bar sweeps left-to-right behind one word with a slight skew. A red marker loop circles a second word, overshooting its start like a real hand. A squiggly underline finishes the sentence.",
beats=["0.0–1.0 s: the three headline lines slide up into place.",
       "1.0–1.6 s: highlighter sweeps behind 'never'.",
       "1.8–2.6 s: red loop draws around 'twice'.",
       "2.8–3.4 s: underline squiggle draws under the last line.",
       "3.4–6.0 s: hold."],
build="""
Text is HTML; annotations are an SVG overlay in the same coordinate space. The highlighter is a rect with `mix-blend-mode: multiply`, revealed by animating its `scaleX` from a left origin. The loop and underline are paths drawn with the dashoffset technique (`motion-line-draw`). Hand-feel comes from the paths themselves: slightly off-ellipse, overlapping ends, and a 2–3° rotation.
""",
knobs=["Which words get which mark; marker colours.",
       "Stroke width (10–14 px) and roughness of the paths.",
       "Draw durations (0.5–0.8 s each).",
       "Highlighter opacity (0.6–0.8)."],
pitfalls=["Measure word positions after fonts load, then place the SVG marks; hard-coded positions break with a new font.",
          "Highlighter must sit behind the ink (multiply or lower z-index) or it greys the text.",
          "One mark at a time; simultaneous scribbles look chaotic."],
pairs=["kinetic-type", "paper-collage", "typewriter", "line-draw"],
css="""
#txt { position:absolute; left:150px; top:170px; font-size:170px; line-height:1.08; letter-spacing:-5px; z-index:2; }
.ln { overflow:hidden; } .ln span { display:inline-block; }
svg { position:absolute; inset:0; z-index:3; }
#hl { mix-blend-mode:multiply; }
""",
html="""
<svg viewBox="0 0 1920 1080" style="z-index:1"><rect id="hl" x="0" y="0" width="0" height="0" fill="#ffc21a" opacity=".85"/></svg>
<div id="txt"><div class="ln"><span id="a1">Good design is</span></div><div class="ln"><span id="a2">never <b id="w2" style="font-weight:inherit">twice</b></span></div><div class="ln"><span id="a3">the same.</span></div></div>
<svg viewBox="0 0 1920 1080"><path id="loop" fill="none" stroke="#ff4a1c" stroke-width="12" stroke-linecap="round"/><path id="und" fill="none" stroke="#2433ff" stroke-width="11" stroke-linecap="round"/></svg>
""",
js="""
function wordBox(el, frac0 = 0, frac1 = 1) { const r = el.getBoundingClientRect(), R = $("#root").getBoundingClientRect(), k = R.width / W;
  return { x: (r.left - R.left) / k, y: (r.top - R.top) / k, w: r.width / k, h: r.height / k }; }
let geo = null;
function layout() {
  const ids = ["#a1", "#a2", "#a3"], keep = ids.map(i => $(i).style.transform);
  ids.forEach(i => $(i).style.transform = "none");   // measure the resting layout, not a mid-tween one
  const a2 = $("#a2"), b = wordBox($("#a3")), w2 = wordBox($("#w2"));
  const range = document.createRange(); range.setStart(a2.firstChild, 0); range.setEnd(a2.firstChild, 5);
  const rr = range.getBoundingClientRect(), R = $("#root").getBoundingClientRect(), k = R.width / W;
  const nv = { x: (rr.left - R.left) / k, y: (rr.top - R.top) / k, w: rr.width / k, h: rr.height / k };
  const cx = w2.x + w2.w / 2, cy = w2.y + w2.h / 2 + 8, rx = w2.w / 2 + 40, ry = w2.h / 2 + 10;
  $("#loop").setAttribute("d", `M${cx - rx * 0.2} ${cy - ry * 1.05} C${cx + rx * 0.9} ${cy - ry * 1.15} ${cx + rx * 1.1} ${cy + ry * 0.9} ${cx} ${cy + ry} C${cx - rx * 1.15} ${cy + ry * 1.05} ${cx - rx * 1.05} ${cy - ry * 0.9} ${cx + rx * 0.25} ${cy - ry * 1.12}`);
  const uy = b.y + b.h - 6; let d = `M${b.x} ${uy}`;
  for (let x = b.x; x < b.x + b.w; x += 60) d += ` q30 ${x % 120 ? 14 : -14} 60 0`;
  $("#und").setAttribute("d", d);
  geo = { nv, L1: $("#loop").getTotalLength(), L2: $("#und").getTotalLength() };
  ids.forEach((i, n) => $(i).style.transform = keep[n]);
  $("#loop").style.strokeDasharray = geo.L1; $("#und").style.strokeDasharray = geo.L2;
}
function renderAt(t) {
  if (!geo || !renderAt.ready) { layout(); renderAt.ready = document.fonts.status === "loaded"; }
  [["#a1", 0], ["#a2", 0.12], ["#a3", 0.24]].forEach(([id, d]) => { const k = E.expo(seg(t, d, d + 0.8)); $(id).style.transform = `translateY(${(1 - k) * 110}%)`; });
  const hk = E.inOut(seg(t, 1.0, 1.6)), nv = geo.nv;
  const hl = $("#hl"); hl.setAttribute("x", nv.x - 14); hl.setAttribute("y", nv.y + nv.h * 0.3); hl.setAttribute("height", nv.h * 0.6);
  hl.setAttribute("width", (nv.w + 28) * hk); hl.setAttribute("transform", `rotate(-1.5 ${nv.x} ${nv.y})`);
  $("#loop").style.strokeDashoffset = geo.L1 * (1 - E.inOut(seg(t, 1.8, 2.6)));
  $("#und").style.strokeDashoffset = geo.L2 * (1 - E.inOut(seg(t, 2.8, 3.4)));
}
"""),

# ---------------------------------------------------------------- card-fan
dict(slug="card-fan", title="Card Fan", dur=6, bg="var(--blue)",
desc="A stack of cards fans out like a hand of playing cards from a shared pivot, then one card lifts out and flips forward to the camera. Use for plan/pricing tiers, feature lists, portfolios, team members, product options, credit cards and 'pick one' choice moments.",
look="Five rounded cards start as a neat stack. They rotate around a pivot below the stack into a fan (−30° to +30°) with a slight stagger, like a dealer's spread. The middle card then rises, straightens and scales up while the others dim and drop back.",
beats=["0.0–0.6 s: stack drops in with a back ease.",
       "0.8–2.0 s: cards fan out, 0.06 s stagger from the centre outward.",
       "2.6–3.6 s: middle card lifts and scales to 1.1 (the low pivot adds lift); others dim to 60 % and sink.",
       "3.6–6.0 s: hold with a slow float on the hero card."],
build="""
Every card has `transform-origin: 50% 160%` (a pivot well below the card) so `rotate()` produces an arc, not a spin. Fan angle `θ_i = (i - mid)·15°·k`. The hero card's extra transform is layered after the fan rotation. Dimming is opacity plus a darker background mix, not a filter.
""",
knobs=["Card count, fan spread (15° step), pivot depth (origin y).",
       "Which card becomes the hero and how far it lifts.",
       "Card designs (pricing, photos, credit cards).",
       "Stagger direction (centre-out or left-to-right)."],
pitfalls=["Pivot at the card centre makes a pinwheel, not a fan; push the origin down.",
          "Set z-index so the hero card is above the others once it lifts.",
          "Keep the card text horizontal-ish on the final frame (hero at 0°)."],
pairs=["card-flip", "carousel-ring", "phone-trio", "count-up"],
css="""
.card { position:absolute; left:50%; top:50%; width:360px; height:500px; margin:-250px 0 0 -180px; border-radius:30px;
  transform-origin:50% 160%; box-shadow:0 30px 70px rgba(0,0,0,.3); padding:34px; box-sizing:border-box; font:700 24px var(--mono); }
.card b { display:block; font:400 92px var(--display); margin-top:150px; letter-spacing:-3px; }
""",
html="""
<div class="card" style="background:#fff">BASIC<b>$9</b></div>
<div class="card" style="background:var(--pink)">TEAM<b>$29</b></div>
<div class="card" style="background:var(--accent);color:#fff">PRO<b>$49</b></div>
<div class="card" style="background:var(--yellow)">SCALE<b>$99</b></div>
<div class="card" style="background:var(--ink);color:#fff">CUSTOM<b>—</b></div>
""",
js="""
const cards = $$(".card"), mid = 2;
function renderAt(t) {
  const drop = E.back(seg(t, 0, 0.6)), hero = E.inOut(seg(t, 2.6, 3.6));
  cards.forEach((c, i) => {
    const off = i - mid, k = E.back(seg(t, 0.8 + Math.abs(off) * 0.06, 1.8 + Math.abs(off) * 0.06));
    let ang = off * 15 * k, y = (1 - drop) * -900, s = 1, op = 1;
    if (i === mid) { y -= 70 * hero; s = lerp(1, 1.1, hero); y += Math.sin(t * 1.6) * 8 * seg(t, 3.6, 4); }
    else { y += 60 * hero; op = lerp(1, 0.6, hero); s = lerp(1, 0.94, hero); }
    c.style.transform = `translateY(${y}px) rotate(${ang}deg) scale(${s})`;
    c.style.opacity = op; c.style.zIndex = i === mid ? 9 : 5 - Math.abs(off);
  });
}
"""),

# ---------------------------------------------------------------- torus-wire
dict(slug="torus-wire", title="Torus Wire", dur=6, bg="var(--ink)",
desc="A wireframe torus (donut) tumbling in 3D with depth-shaded lines that twists and breathes, drawn in pure canvas with no 3D library. Use for tech/sci-fi scenes, 'dimension' or 'depth' chapters in a showreel, loading states, abstract 3D brand moments and math visuals.",
look="A torus built from rings of lines tumbles slowly on two axes. Lines near the camera are bright and thick, far lines thin and dim, so it reads as 3D without lighting. Mid-clip the tube twists (a phase offset around the ring), turning the wireframe into a spiralling knot-like form before relaxing.",
beats=["0.0–1.0 s: torus draws on ring by ring.",
       "Continuous: rotation 0.5 rad/s on X, 0.8 rad/s on Y.",
       "2.0–4.0 s: twist rises to a full turn, then relaxes by 5.0 s.",
       "5.0–6.0 s: tube radius breathes in slightly; hold."],
build="""
Parametric torus `p(u,v) = ((R + r·cos v)·cos u, r·sin v, (R + r·cos v)·sin u)`, with a twist term `v + twist·u`. Draw `U` rings (constant u) and `V` rings (constant v) as polylines. For each segment, depth from the rotated z sets `lineWidth` and alpha: no z-buffer needed for lines. Rotate with `rot()` and project with `proj()` from the kit.
""",
knobs=["Major/minor radius (R, r) and ring counts (U, V).",
       "Twist amount and timing.",
       "Rotation speeds; colour (single accent or gradient by u).",
       "Line width range (near vs. far)."],
pitfalls=["Sort isn't needed for additive-looking wires, but heavy alpha on many lines muddies: keep far lines under 0.15 alpha.",
          "Ring counts above ~60×30 slow canvas preview.",
          "Keep twist an integer number of turns at rest, or the mesh won't close."],
pairs=["particle-sphere", "helix", "orbit-rings", "tunnel-grid"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), U = 56, V = 22;
function renderAt(t) {
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  const R = 300, r = 120 * (1 - 0.12 * E.inOut(seg(t, 5, 6))), ax = 0.6 + t * 0.5, ay = t * 0.8;
  const tw = 1 * E.inOut(seg(t, 2, 4)) * (1 - E.inOut(seg(t, 4, 5))), draw = E.out(seg(t, 0, 1));
  const pt = (u, v) => { const vv = v + tw * u, c = Math.cos(vv);
    return proj(rot([(R + r * c) * Math.cos(u), r * Math.sin(vv), (R + r * c) * Math.sin(u)], ax, ay), 1300); };
  const seg2 = (a, b, hue) => { const z = (a[2] + b[2]) / 2, near = clamp((z - 0.75) / 0.6);
    g.strokeStyle = hue ? `rgba(255,74,28,${0.12 + 0.88 * near})` : `rgba(239,233,223,${0.08 + 0.7 * near})`;
    g.lineWidth = 0.8 + 3.2 * near; g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke(); };
  const Ud = Math.ceil(U * draw);
  for (let i = 0; i < Ud; i++) { const u = i / U * 2 * Math.PI;
    for (let j = 0; j < V; j++) seg2(pt(u, j / V * 2 * Math.PI), pt(u, (j + 1) / V * 2 * Math.PI), 0); }
  for (let j = 0; j < V; j++) { const v = j / V * 2 * Math.PI;
    for (let i = 0; i < Ud; i++) seg2(pt(i / U * 2 * Math.PI, v), pt((i + 1) / U * 2 * Math.PI, v), 1); }
}
"""),

# ---------------------------------------------------------------- typewriter
dict(slug="typewriter", title="Typewriter", dur=7, bg="var(--paper)",
desc="Text types itself character by character with human rhythm, a blinking caret, a realistic typo that gets backspaced and corrected, and each letter popping in. Use for terminal/command intros, chat-style reveals, quotes, prompts, hooks, 'what if…' questions and code or AI-generated-text scenes.",
look="A monospace line appears letter by letter with uneven timing (faster within words, pauses at spaces and punctuation). A wrong letter is typed, the caret pauses, two backspaces remove it and the correct text continues. A solid block caret blinks only when idle.",
beats=["0.3 s: caret appears and blinks.",
       "0.8–5.4 s: typing; a typo at ~2.6 s is backspaced at ~3.1 s.",
       "5.4–7.0 s: caret blinks at the end; the last word turns accent at 5.8 s."],
build="""
Precompute a keystroke list once: `[{t, op:'type'|'back', ch}]` with seeded jitter (base 55 ms per char, +180 ms after spaces, +350 ms after punctuation, ±25 ms noise). `renderAt(t)` replays all keystrokes with `time ≤ t` into a string: pure and scrub-safe. Each character is a span; the newest one gets a tiny scale pop based on its age. The caret blinks with `floor(t·2) % 2` only when the last keystroke is older than 0.4 s.
""",
knobs=["Text, typo position and wrong letters.",
       "Base speed and pause lengths.",
       "Caret style (block, bar, underscore).",
       "Sound: a key click at each keystroke time (export the list)."],
pitfalls=["Never type with setInterval; scrubbing breaks. Replay from the keystroke list.",
          "Monospace keeps the caret from jittering horizontally.",
          "Keep lines under ~40 characters at this size or wrap deliberately."],
pairs=["scramble-decode", "chat-thread", "command-palette", "split-flap"],
css="""
#line { position:absolute; left:160px; top:420px; right:160px; font:700 92px/1.25 var(--mono); letter-spacing:-2px; white-space:pre-wrap; }
#line .w { font-weight:inherit; white-space:nowrap; } #line span { display:inline-block; }
#car { display:inline-block; width:52px; height:100px; margin-left:4px; background:var(--accent); vertical-align:-14px; }
#pr { position:absolute; left:160px; top:330px; font:600 30px var(--mono); color:#8a857c; }
""",
html="""<div id="pr">~/ideas $</div><div id="line"></div>""",
js="""
const TEXT = "What if every frame was written in code?", TYPO_AT = 18, TYPO = "wr";
const keys = []; (function build() { const r = rng(5); let tt = 0.8;
  const push = (op, ch, gap) => { tt += gap + (r() - 0.5) * 0.05; keys.push({ t: tt, op, ch }); };
  for (let i = 0; i < TEXT.length; i++) {
    if (i === TYPO_AT) { for (const c of TYPO) push("type", c, 0.06); tt += 0.35; for (const c of TYPO) push("back", "", 0.09); tt += 0.12; }
    const prev = TEXT[i - 1] || ""; push("type", TEXT[i], prev === " " ? 0.16 : /[?,.]/.test(prev) ? 0.3 : 0.055); } })();
const line = $("#line");
function renderAt(t) {
  const out = []; let last = -1;
  for (const k of keys) { if (k.t > t) break; if (k.op === "type") out.push({ ch: k.ch, t: k.t }); else out.pop(); last = k.t; }
  const idle = last < 0 || t - last > 0.4, blink = !idle || Math.floor(t * 2) % 2 === 0, hot = t > 5.8;
  const lastWord = TEXT.lastIndexOf(" ") + 1;
  let html = "<b class=w>";
  out.forEach((o, i) => { const age = t - o.t, s = 1 + 0.25 * (1 - clamp(age / 0.08));
    const col = hot && i >= lastWord && out.length === TEXT.length ? `color:${C.accent}` : "";
    if (o.ch === " ") { html += "</b> <b class=w>"; return; }
    html += `<span style="transform:scale(${s.toFixed(3)});${col}">${o.ch.replace("<", "&lt;")}</span>`; });
  line.innerHTML = html + `<i id="car" style="opacity:${t > 0.3 && blink ? 1 : 0}"></i></b>`;
}
"""),

# ---------------------------------------------------------------- wave-dots
dict(slug="wave-dots", title="Wave Dots", dur=6, bg="var(--ink)",
desc="A full-frame grid of dots that ripples with radial and travelling sine waves, dots growing, shifting and changing colour with the wave height. Use for audio/voice visualisation, data pulses, rhythm/beat sections, ambient tech backgrounds, 'signal' and 'ripple effect' metaphors.",
look="A dense, even grid of round dots. A ripple expands from the centre, so dots swell and lift as the crest passes, coloured from blue at rest to accent at the peak. A second, slower diagonal wave interferes, so the pattern never looks mechanical.",
beats=["0.0–0.8 s: dots fade in from the centre outward.",
       "0.6 s, 2.4 s, 4.2 s: three ripples launch from the centre.",
       "Continuous: diagonal swell wave travelling left to right.",
       "5.2–6.0 s: amplitude eases down to calm."],
build="""
For every grid point, wave height `h = Σ ripple_k + swell`. A ripple is a Gaussian ring: `exp(-((d - c·(t - t_k))/w)²) · decay`, where `d` is distance from the centre. Swell is `sin(x·0.012 + y·0.006 - t·2)`. Dot radius, vertical offset and colour all come from `h`. Pure function of `(x, y, t)`, so it scrubs and loops cleanly.
""",
knobs=["Grid spacing (36 px) and dot size range.",
       "Ripple times, speed `c` and width `w`.",
       "Colour ramp (rest → crest).",
       "Swap the centre for a moving source (e.g. follow a cursor path)."],
pitfalls=["~1,500 dots is fine in canvas; DOM dots that many will crawl.",
          "Clamp radius ≥ 0.5 px or dots vanish and the grid looks broken.",
          "Align ripple launches to the beat if there's music."],
pairs=["halftone-wave", "radar-morph", "terrain-mesh", "dot-wipe"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), SP = 36, rip = [0.6, 2.4, 4.2];
function renderAt(t) {
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  const calm = 1 - E.inOut(seg(t, 5.2, 6));
  for (let y = SP / 2; y < H; y += SP) for (let x = SP / 2; x < W; x += SP) {
    const d = Math.hypot(x - W / 2, y - H / 2), on = E.out(seg(t, d / 1400 * 0.8, d / 1400 * 0.8 + 0.3));
    if (on <= 0) continue;
    let h = 0.35 * Math.sin(x * 0.012 + y * 0.006 - t * 2);
    for (const r0 of rip) { if (t < r0) continue; const c = (t - r0) * 700;
      h += Math.exp(-(((d - c) / 90) ** 2)) * Math.exp(-(t - r0) * 0.5) * 1.4; }
    h *= calm; const k = clamp((h + 0.4) / 1.6);
    g.fillStyle = k > 0.55 ? mix(C.blue, C.accent, (k - 0.55) / 0.45) : mix("#1c2470", C.blue, k / 0.55);
    g.beginPath(); g.arc(x, y - h * 10, Math.max(0.6, (3 + 9 * k) * on), 0, 6.283); g.fill(); }
}
"""),

# ---------------------------------------------------------------- before-after
dict(slug="before-after", title="Before After", dur=6, bg="#151515",
desc="A before/after comparison with a draggable-style divider that wipes across, revealing the improved version, labelled and with a handle. Use for redesigns, product upgrades, photo/edit results, AI enhancement, cleanup, makeovers, A/B outcomes and 'old way vs new way' scenes.",
look="Two versions of the same layout sit exactly on top of each other: a grey, cluttered 'before' and a clean, colourful 'after'. A white vertical divider with a round handle sweeps from left to right with an overshoot, then back to centre. 'BEFORE' and 'AFTER' pills sit in the corners of each side.",
beats=["0.0–0.6 s: frame fades up showing BEFORE fully.",
       "0.8–2.4 s: divider sweeps to 85 % (in-out).",
       "2.6–3.6 s: divider returns to 50 % with a back ease and holds.",
       "3.6–6.0 s: a tiny handle nudge (±12 px) at 4.4 s to invite the eye."],
build="""
Both panels fill the same box; the AFTER panel is clipped with `clip-path: inset(0 0 0 X%)` where X follows the divider. The divider is a 4 px bar plus a round handle with arrow glyphs, translated to the same X. Use real screenshots or photos in the two panels for an actual comparison; keep them pixel-aligned.
""",
knobs=["Divider path (keyframes of X over time).",
       "Orientation (vertical or horizontal wipe).",
       "Panel content: images, UI or video.",
       "Labels and handle style."],
pitfalls=["The two images must be the same size and registration or the wipe shows a jump.",
          "Clip the AFTER layer, don't resize it; resizing distorts.",
          "Don't park the divider at the exact centre of a face or product."],
pairs=["cursor-tour", "card-flip", "count-up", "dot-wipe"],
css="""
.pn { position:absolute; left:160px; top:110px; width:1600px; height:860px; border-radius:26px; overflow:hidden; }
#bef { background:#cfcfcf; } #aft { background:var(--paper); }
.pill { position:absolute; top:28px; padding:10px 22px; border-radius:30px; font:700 24px var(--mono); }
.b1 { position:absolute; border-radius:12px; }
#div { position:absolute; top:110px; width:4px; height:860px; margin-left:-2px; background:#fff; z-index:5; }
#hd { position:absolute; top:50%; left:50%; width:84px; height:84px; margin:-42px 0 0 -42px; border-radius:50%; background:#fff;
  box-shadow:0 10px 30px rgba(0,0,0,.35); font:700 30px/84px var(--mono); text-align:center; color:#111; }
""",
html="""
<div class="pn" id="bef">
  <div class="b1" style="left:60px;top:120px;width:700px;height:60px;background:#9a9a9a"></div>
  <div class="b1" style="left:60px;top:210px;width:520px;height:40px;background:#b0b0b0"></div>
  <div class="b1" style="left:60px;top:300px;width:1480px;height:480px;background:#bdbdbd"></div>
  <div class="b1" style="left:900px;top:110px;width:600px;height:150px;background:#a8a8a8"></div>
  <div class="pill" style="left:28px;background:#888;color:#fff">BEFORE</div>
</div>
<div class="pn" id="aft">
  <div class="b1" style="left:60px;top:110px;font:400 110px var(--display);letter-spacing:-4px;color:var(--ink)">Clean.</div>
  <div class="b1" style="left:60px;top:300px;width:700px;height:480px;background:var(--accent)"></div>
  <div class="b1" style="left:800px;top:300px;width:740px;height:220px;background:var(--blue)"></div>
  <div class="b1" style="left:800px;top:560px;width:740px;height:220px;background:var(--yellow)"></div>
  <div class="pill" style="right:28px;background:var(--ink);color:#fff">AFTER</div>
</div>
<div id="div"><div id="hd">‹ ›</div></div>
""",
js="""
function renderAt(t) {
  $("#root").style.opacity = E.out(seg(t, 0, 0.6));
  let x = lerp(0.02, 0.85, E.inOut(seg(t, 0.8, 2.4)));
  x = lerp(x, 0.5, E.back(seg(t, 2.6, 3.6)));
  x += Math.sin(seg(t, 4.4, 5.0) * Math.PI * 2) * 12 / 1600;
  $("#aft").style.clipPath = `inset(0 0 0 ${(x * 100).toFixed(3)}%)`;
  $("#div").style.left = `${160 + 1600 * x}px`;
}
"""),
]
