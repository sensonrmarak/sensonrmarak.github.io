RECIPES = [
# ---------------------------------------------------------------- kinetic-type
dict(slug="kinetic-type", title="Kinetic Type", dur=6, bg="var(--paper)",
desc="Giant display words that slam in through masks with skew and motion blur, then the background flips colour on the hit word. Use for kinetic typography, title cards, 'MAKE IT MOVE' style openers, bold statement scenes, hooks and manifesto lines in a motion reel, promo or explainer.",
look="Huge heavy grotesque words fill the frame edge to edge. Each word rises out of an invisible mask with a hard expo ease, skewed and blurred while fast and crisp when it lands. On the key word the whole background snaps to the accent colour and the type inverts.",
beats=["0.2–1.6 s: words enter one by one, 0.18 s apart, each over 0.6 s (expo out).",
       "2.4 s: background cuts from paper to accent; the type turns paper-white; a slow 1.00→1.06 push starts.",
       "5.0–5.8 s: words exit upward in the same order (expo in), leaving a clean frame."],
build="""
Each line is a block with `overflow:hidden`, so a word translated 110 % down is invisible: that is the mask. Per word, `k = E.expo(seg(t, start, start + 0.6))` drives `translateY((1-k)*110%)`, `skewY((1-k)*-14deg)` and a blur of `(1-k)*14px`, which fakes motion blur because blur is largest exactly when speed is largest. The colour flip is a hard cut, not a fade: hard cuts read as rhythm.
""",
knobs=["Stagger (0.18 s) and per-word duration (0.6 s): shorter feels aggressive, longer feels editorial.",
       "Skew amount (−14°): 0 for calm, up to −25° for violent.",
       "Flip word index and accent colour.",
       "Font size: aim for the longest line at ~90 % of frame width."],
pitfalls=["Blur on huge text is expensive in a browser preview; it renders fine frame by frame.",
          "Never fade text in on top of the mask; the mask is the reveal. Mixing both looks soft.",
          "Measure line widths with the real font loaded, or the edge-to-edge fit breaks."],
pairs=["scramble-decode", "marker-draw", "count-up", "swiss-grid"],
css="""
.stack { position:absolute; left:80px; top:150px; }
.line { overflow:hidden; height:390px; display:flex; gap:40px; align-items:flex-end; }
.line span { display:inline-block; font-size:400px; line-height:0.86; letter-spacing:-12px; will-change:transform; }
.dot { color: var(--accent); }
#label { position:absolute; left:80px; bottom:60px; font:600 28px var(--mono); letter-spacing:2px; }
""",
html="""
<div class="stack" id="stack">
  <div class="line"><span>MAKE</span><span>IT</span></div>
  <div class="line"><span>MOVE</span><span class="dot">.</span></div>
</div>
<div id="label">02 — TYPE</div>
""",
js="""
const words = $$(".line span"), root = $("#root"), stack = $("#stack"), label = $("#label");
function renderAt(t) {
  const flip = t >= 2.4;
  root.style.background = flip ? C.accent : C.paper;
  words.forEach((w, i) => {
    const a = 0.2 + i * 0.18;
    const kin = E.expo(seg(t, a, a + 0.6));
    const kout = E.in(seg(t, 5.0 + i * 0.1, 5.5 + i * 0.1));
    const y = (1 - kin) * 110 - kout * 110;
    const sk = (1 - kin) * -14 + kout * 14;
    const speed = Math.max(1 - kin, kout);
    w.style.transform = `translateY(${y}%) skewY(${sk}deg)`;
    w.style.filter = speed > 0.01 ? `blur(${speed * 14}px)` : "none";
    w.style.color = w.classList.contains("dot") ? (flip ? C.ink : C.accent) : (flip ? C.paper : C.ink);
  });
  stack.style.transform = `scale(${1 + 0.06 * E.inOut(seg(t, 2.4, 6))})`;
  label.style.color = flip ? C.paper : C.ink;
}
"""),

# ---------------------------------------------------------------- phone-orbit
dict(slug="phone-orbit", title="Phone Orbit", dur=6, bg="var(--blue)",
desc="A 3D phone mockup turns in space while feature cards orbit around it on an ellipse, passing in front of and behind the device. Use for app launches, product promos, feature highlights, mobile UI showcases and 'here is the app' hero shots.",
look="A rounded phone with a live-looking UI screen sits centre frame, slowly yawing in 3D. Three small cards (stat, avatar, chart) circle it on a tilted ellipse; they shrink and dim when behind the phone and grow when in front, so depth reads without a 3D engine.",
beats=["0.0–0.8 s: phone rises from below with a back-ease, already turning.",
       "0.4–1.4 s: cards pop in at their orbit positions (scale 0→1, staggered).",
       "0.8–5.4 s: phone yaws −28°→+28°, cards complete about 1.2 orbits.",
       "5.4–6.0 s: everything settles; phone faces camera for the end frame."],
build="""
CSS 3D: the phone is a div with `transform-style: preserve-3d` under a `perspective` parent; `rotateY` comes from `lerp(-28, 28, E.inOut(...))`. Cards are 2D: each sits at angle `θ = base + t*speed` on an ellipse `x = R·cosθ, y = r·sinθ`. Depth `z = sinθ` sets `scale`, `opacity` and `z-index` (in front when `sinθ > 0`). The screen is plain HTML so it can be swapped for a real screenshot (`<img>`).
""",
knobs=["Orbit radii (R 620 px, r 120 px) and tilt (the r/R ratio).",
       "Orbit speed (turns per clip).",
       "Phone yaw range; keep under ±35° or the screen becomes unreadable.",
       "Replace `.screen` content with a real UI screenshot."],
pitfalls=["Swap z-index exactly when sinθ crosses 0, or a card pops through the phone.",
          "Don't rotate the phone more than ±35°: the screen is the product.",
          "Keep cards out of the phone's silhouette at the end frame."],
pairs=["phone-trio", "phone-scroll", "notifications", "count-up"],
css="""
.scene { position:absolute; inset:0; perspective:2200px; }
.phone { position:absolute; left:50%; top:50%; width:430px; height:880px; margin:-440px 0 0 -215px;
  border-radius:68px; background:#0b0b0b; box-shadow:0 60px 120px rgba(0,0,0,.45); transform-style:preserve-3d; }
.screen { position:absolute; inset:16px; border-radius:54px; overflow:hidden; background:var(--paper); }
.notch { position:absolute; top:22px; left:50%; width:120px; height:34px; margin-left:-60px; border-radius:20px; background:#0b0b0b; }
.hero { margin:90px 28px 0; height:300px; border-radius:30px; background:var(--accent); }
.row { margin:22px 28px 0; height:70px; border-radius:20px; background:#fff; }
.row.s { width:60%; }
.card { position:absolute; left:50%; top:50%; width:260px; height:150px; margin:-75px 0 0 -130px; border-radius:28px;
  background:#fff; box-shadow:0 30px 60px rgba(0,0,0,.25); padding:24px; box-sizing:border-box; font:700 22px var(--mono); }
.card b { display:block; font:400 64px var(--display); margin-top:8px; }
.c2 { background:var(--yellow); } .c3 { background:var(--pink); }
""",
html="""
<div class="scene">
  <div class="phone" id="phone"><div class="screen"><div class="hero"></div><div class="row"></div><div class="row"></div><div class="row s"></div></div><div class="notch"></div></div>
  <div class="card c1" id="c1">USERS<b>48K</b></div>
  <div class="card c2" id="c2">RATING<b>4.9</b></div>
  <div class="card c3" id="c3">GROWTH<b>+312%</b></div>
</div>
""",
js="""
const phone = $("#phone"), cards = [$("#c1"), $("#c2"), $("#c3")];
function renderAt(t) {
  const rise = E.back(seg(t, 0, 0.8));
  const settle = E.inOut(seg(t, 5.4, 6));
  const yaw = lerp(lerp(-28, 28, E.inOut(seg(t, 0.8, 5.4))), 0, settle);
  phone.style.transform = `translateY(${(1 - rise) * 900}px) rotateY(${yaw}deg) rotateX(${4 * Math.sin(t * 1.3)}deg)`;
  cards.forEach((c, i) => {
    const th = i * 2.0944 + t * 1.25 - 1.2;
    const z = Math.sin(th);
    const pop = E.back(seg(t, 0.4 + i * 0.2, 0.9 + i * 0.2));
    const s = (0.78 + 0.22 * (z + 1) / 2) * pop;
    c.style.transform = `translate(${620 * Math.cos(th)}px, ${120 * z}px) scale(${s})`;
    c.style.opacity = (0.55 + 0.45 * (z + 1) / 2).toFixed(3);
    c.style.zIndex = z > 0 ? 3 : 0;
  });
  phone.style.zIndex = 1;
}
"""),

# ---------------------------------------------------------------- globe-arcs
dict(slug="globe-arcs", title="Globe Arcs", dur=6, bg="var(--ink)",
desc="A rotating dotted globe with glowing great-circle arcs that draw between cities and pulse at each end. Use for global reach, network, shipping, payments, users-worldwide, distributed systems and 'connected everywhere' scenes.",
look="Thousands of small dots form a sphere on black; back-facing dots are dimmed so the globe reads round. Bright accent arcs lift off the surface between city pairs, draw from start to end, leave a fading tail and ring the landing city with an expanding pulse.",
beats=["0.0–1.0 s: globe scales up from 0.6 with dots fading in from the centre.",
       "1.0–4.6 s: six arcs launch 0.45 s apart, each drawing over 1.1 s.",
       "Continuous: globe rotates 0.35 rad/s around Y with a fixed 0.35 rad tilt.",
       "4.6–6.0 s: arcs hold, tails fade, pulses settle."],
build="""
Dots: a Fibonacci sphere (`N = 1800` evenly spread points). Each frame rotates them with `rot()` and projects with `proj()`; dots with `z > 0` (facing away) draw at low alpha. Arcs: cities are lat/lon → unit vectors; points along the arc are a normalised slerp between the two, pushed outward by `1 + h·sin(πu)` so the arc lifts. Draw the sub-range `[tail, head]` where `head = E.inOut(progress)`. Everything rotates with the globe, so arcs stick to their cities.
""",
knobs=["City list and arc pairs (lat, lon in degrees).",
       "Arc height `h` (0.25 for long hauls, 0.1 for short).",
       "Dot count and size; rotation speed and tilt.",
       "Accent colour and glow (`shadowBlur`)."],
pitfalls=["Hide arc segments when they pass behind the globe (z > 0 and inside the disc) or they show through.",
          "Use real lat/lon if the scene names real places; viewers check.",
          "Keep `shadowBlur` modest: it's the slowest call in canvas 2D."],
pairs=["orbit-rings", "flow-line", "count-up", "radar-morph"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv");
const N = 2200, R = 430, pts = [];
for (let i = 0; i < N; i++) { const y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), th = i * 2.39996;
  pts.push([Math.cos(th) * r, y, Math.sin(th) * r]); }
const ll = (lat, lon) => { const a = lat * Math.PI / 180, b = lon * Math.PI / 180; return [Math.cos(a) * Math.sin(b), -Math.sin(a), Math.cos(a) * Math.cos(b)]; };
const city = { ny: ll(40.7, -74), ldn: ll(51.5, -0.1), tok: ll(35.7, 139.7), syd: ll(-33.9, 151.2), sp: ll(-23.5, -46.6), dxb: ll(25.2, 55.3), sf: ll(37.8, -122.4), sg: ll(1.35, 103.8) };
const arcs = [["sf", "ldn"], ["ny", "sp"], ["ldn", "dxb"], ["dxb", "sg"], ["sg", "syd"], ["tok", "sf"]];
function slerp(a, b, u) { const d = Math.acos(clamp(a[0] * b[0] + a[1] * b[1] + a[2] * b[2], -1, 1)), s = Math.sin(d) || 1;
  const ka = Math.sin((1 - u) * d) / s, kb = Math.sin(u * d) / s; return [a[0] * ka + b[0] * kb, a[1] * ka + b[1] * kb, a[2] * ka + b[2] * kb]; }
function renderAt(t) {
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  const sc = lerp(0.6, 1, E.out(seg(t, 0, 1))), ay = t * 0.35 - 0.6, ax = 0.35, Rr = R * sc;
  const P = v => { const q = rot(v, ax, ay); return [W / 2 + q[0] * Rr, H / 2 + q[1] * Rr, q[2]]; };
  const fade = E.out(seg(t, 0, 1));
  for (const p of pts) { const [x, y, z] = P(p);
    g.fillStyle = z < 0 ? `rgba(239,233,223,${0.85 * fade})` : `rgba(239,233,223,${0.13 * fade})`;
    g.fillRect(x - 1.6, y - 1.6, z < 0 ? 3.2 : 2.4, z < 0 ? 3.2 : 2.4); }
  arcs.forEach(([a, b], i) => {
    const p = seg(t, 1 + i * 0.45, 2.1 + i * 0.45); if (p <= 0) return;
    const head = E.inOut(p), tail = Math.max(0, head - 0.5);
    const A = city[a], B = city[b], steps = 60;
    g.lineWidth = 4; g.lineCap = "round"; g.strokeStyle = C.accent; g.shadowColor = C.accent; g.shadowBlur = 14;
    g.beginPath(); let started = false;
    for (let s = 0; s <= steps; s++) { const u = s / steps; if (u < tail || u > head) continue;
      const v = slerp(A, B, u), h = 1 + 0.28 * Math.sin(Math.PI * u), [x, y, z] = P([v[0] * h, v[1] * h, v[2] * h]);
      const hidden = z > 0 && Math.hypot(x - W / 2, y - H / 2) < Rr;
      if (hidden) { started = false; continue; }
      if (!started) { g.moveTo(x, y); started = true; } else g.lineTo(x, y); }
    g.stroke(); g.shadowBlur = 0;
    [[A, 0], [B, 1]].forEach(([v, end]) => { const [x, y, z] = P(v); if (z > 0) return;
      const k = end ? seg(t, 2.1 + i * 0.45, 2.9 + i * 0.45) : seg(t, 1 + i * 0.45, 1.6 + i * 0.45); if (k <= 0) return;
      g.fillStyle = C.accent; g.beginPath(); g.arc(x, y, 7, 0, 7); g.fill();
      g.strokeStyle = `rgba(255,74,28,${1 - k})`; g.lineWidth = 3; g.beginPath(); g.arc(x, y, 7 + 40 * E.out(k), 0, 7); g.stroke(); });
  });
}
"""),

# ---------------------------------------------------------------- blueprint-draw
dict(slug="blueprint-draw", title="Blueprint Draw", dur=6, bg="#173a8c",
desc="A technical drawing that draws itself line by line on blueprint paper: construction grid, outlines, dimension lines and handwritten-style labels. Use for engineering, architecture, product design, 'how it's made', planning, hardware and build-process scenes.",
look="Deep blueprint blue with a fine white grid. A part (a flanged bearing housing) draws in white strokes, outlines first, then centre lines (dashed), then dimension lines with arrowheads and monospaced callouts that type on. A title block sits bottom right.",
beats=["0.0–0.6 s: grid fades in.",
       "0.4–2.8 s: outlines draw, each path over 0.7 s, staggered 0.18 s.",
       "2.4–3.6 s: dashed centre lines draw.",
       "3.2–4.8 s: dimension lines draw, then their labels fade/slide in.",
       "4.6–5.4 s: title block draws; hold."],
build="""
Inline SVG. On load, measure each path once with `getTotalLength()` and set `stroke-dasharray = L`. Per frame `stroke-dashoffset = L * (1 - E.inOut(k))`. Dashed centre lines can't use dasharray for the draw, so they're revealed through an animated `clipPath` rect instead. Labels are SVG `<text>` with opacity and a small x offset. Order the reveal by importance: silhouette, then construction, then annotation.
""",
knobs=["Paper colour (#173a8c classic, #0f2f6b deep) and grid spacing.",
       "Per-path duration/stagger and draw order.",
       "Swap the drawing: any SVG paths work; keep strokes 2–4 px.",
       "Label text and units."],
pitfalls=["Measure lengths once at setup, never inside renderAt.",
          "`vector-effect: non-scaling-stroke` breaks dash lengths if the SVG is scaled; keep 1:1.",
          "Too many simultaneous paths turns into noise: keep 2–3 drawing at once."],
pairs=["line-draw", "layer-explode", "iso-city", "swiss-grid"],
css="""
svg { position:absolute; inset:0; }
.o { fill:none; stroke:#eef3ff; stroke-width:4; stroke-linecap:round; stroke-linejoin:round; }
.c { fill:none; stroke:#9fb7ff; stroke-width:2; stroke-dasharray:18 8 4 8; }
.d { fill:none; stroke:#cfe0ff; stroke-width:2; }
.lab { fill:#eef3ff; font:600 26px var(--mono); letter-spacing:1px; }
""",
html="""
<svg viewBox="0 0 1920 1080" id="svg">
  <defs>
    <pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="1"/></pattern>
    <pattern id="g2" width="200" height="200" patternUnits="userSpaceOnUse"><path d="M200 0H0V200" fill="none" stroke="rgba(255,255,255,.22)" stroke-width="1.5"/></pattern>
    <clipPath id="cc"><rect id="ccr" x="0" y="0" width="0" height="1080"/></clipPath>
    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#cfe0ff"/></marker>
  </defs>
  <g id="grid"><rect width="1920" height="1080" fill="url(#g)"/><rect width="1920" height="1080" fill="url(#g2)"/></g>
  <g class="draw">
    <path class="o" d="M560 300 H1160 V420 H1060 V700 H660 V420 H560 Z"/>
    <path class="o" d="M760 560 m-140 0 a140 140 0 1 0 280 0 a140 140 0 1 0 -280 0"/>
    <path class="o" d="M860 560 m-60 0 a60 60 0 1 0 120 0 a60 60 0 1 0 -120 0"/>
    <path class="o" d="M610 360 m-22 0 a22 22 0 1 0 44 0 a22 22 0 1 0 -44 0"/>
    <path class="o" d="M1110 360 m-22 0 a22 22 0 1 0 44 0 a22 22 0 1 0 -44 0"/>
    <path class="o" d="M1300 300 H1460 V700 H1300 Z M1300 420 H1460 M1340 300 V700 M1420 300 V700"/>
  </g>
  <g clip-path="url(#cc)"><path class="c" d="M500 560 H1220 M860 250 V760 M1380 250 V760"/></g>
  <g class="draw">
    <path class="d" d="M560 250 H1160" marker-start="url(#ar)" marker-end="url(#ar)"/>
    <path class="d" d="M1210 300 V700" marker-start="url(#ar)" marker-end="url(#ar)"/>
    <path class="d" d="M1300 760 H1460" marker-start="url(#ar)" marker-end="url(#ar)"/>
    <path class="d" d="M1480 820 H1840 V1000 H1480 Z M1480 880 H1840"/>
  </g>
  <text class="lab" id="l1" x="800" y="235">600.00</text>
  <text class="lab" id="l2" x="1225" y="510">400.00</text>
  <text class="lab" id="l3" x="1335" y="800">160</text>
  <text class="lab" id="l4" x="1500" y="862">HOUSING / A-02</text>
  <text class="lab" id="l5" x="1500" y="940" style="font-size:20px">SCALE 1:4   REV C</text>
</svg>
""",
js="""
const paths = $$(".draw path"), lens = paths.map(p => p.getTotalLength());
paths.forEach((p, i) => { p.style.strokeDasharray = lens[i]; });
const nOut = 6, labels = ["#l1", "#l2", "#l3", "#l4", "#l5"].map($);
function renderAt(t) {
  $("#grid").style.opacity = E.out(seg(t, 0, 0.6));
  paths.forEach((p, i) => {
    const a = i < nOut ? 0.4 + i * 0.18 : 3.2 + (i - nOut) * 0.3 + (i === paths.length - 1 ? 1.2 : 0);
    const k = E.inOut(seg(t, a, a + 0.7));
    p.style.strokeDashoffset = lens[i] * (1 - k);
    p.style.opacity = k > 0 ? 1 : 0;
  });
  $("#ccr").setAttribute("width", 1920 * E.inOut(seg(t, 2.4, 3.6)));
  labels.forEach((l, i) => { const k = E.out(seg(t, 3.7 + i * 0.25, 4.2 + i * 0.25));
    l.style.opacity = k; l.setAttribute("transform", `translate(${(1 - k) * -16},0)`); });
}
"""),

# ---------------------------------------------------------------- terrain-mesh
dict(slug="terrain-mesh", title="Terrain Mesh", dur=6, bg="var(--ink)",
desc="A wireframe landscape of noise-driven hills that the camera glides over, lines tinted by height, synthwave or topographic. Use for data landscapes, exploration, 'the road ahead', synthwave/retro scenes, Joy-Division ridgelines, AI/latent-space visuals and ambient backgrounds.",
look="A perspective grid of lines stretches to a horizon. Hills rise and fall as the camera flies forward; low ground is ink-blue, peaks glow accent orange. A sun disc with scanline cuts sits on the horizon for the synthwave variant.",
beats=["0.0–1.0 s: terrain amplitude grows from flat to full.",
       "Continuous: camera moves forward 1.2 grid rows per second.",
       "2.5–6.0 s: horizon sun rises slightly; slow camera bob."],
build="""
Grid `cols × rows` in world space. Height `h = noise(x*0.12, (z + travel)*0.12)` from a seeded 2D value noise (smooth interpolated lattice), so moving `travel` scrolls the hills toward the camera with no popping. Project with a simple pinhole: `sx = cx + x*f/z`, `sy = horizon + (camY - h)*f/z`. Draw rows back to front, each as a polyline filled with background below it (`fill` then `stroke`) so nearer ridges hide farther ones: that hidden-line trick is what makes it read as solid.
""",
knobs=["Noise scale (0.12) and amplitude (hill height).",
       "Rows/cols density (line count vs. speed).",
       "Colour ramp low→high; sun on/off.",
       "Fill under each row on (solid, Joy Division) or off (pure wireframe)."],
pitfalls=["Use a lattice noise keyed on integer world coordinates; re-seeding per frame flickers.",
          "Draw strictly back to front or the occlusion breaks.",
          "Clip rows with z ≤ near plane to avoid huge projected values."],
pairs=["wave-dots", "tunnel-grid", "flow-line", "halftone-wave"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), r0 = rng(7), LAT = 64, lat = Array.from({ length: LAT * LAT }, () => r0());
const sm = x => x * x * (3 - 2 * x);
function vn(x, y) { const xi = Math.floor(x), yi = Math.floor(y), xf = sm(x - xi), yf = sm(y - yi);
  const L = (i, j) => lat[((j % LAT + LAT) % LAT) * LAT + ((i % LAT + LAT) % LAT)];
  return lerp(lerp(L(xi, yi), L(xi + 1, yi), xf), lerp(L(xi, yi + 1), L(xi + 1, yi + 1), xf), yf); }
const noise = (x, y) => vn(x, y) * 0.65 + vn(x * 2.1, y * 2.1) * 0.35;
function renderAt(t) {
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  const horizon = 430, f = 900, camY = 260 + 18 * Math.sin(t * 0.9), amp = 420 * E.out(seg(t, 0, 1));
  const sunY = horizon - 40 - 60 * E.inOut(seg(t, 2.5, 6));
  const sg = g.createLinearGradient(0, sunY - 220, 0, sunY + 220); sg.addColorStop(0, C.yellow); sg.addColorStop(1, C.accent);
  g.fillStyle = sg; g.beginPath(); g.arc(W / 2, sunY, 220, 0, 7); g.fill();
  g.fillStyle = C.ink; for (let i = 0; i < 7; i++) g.fillRect(W / 2 - 230, sunY + 30 + i * 28, 460, 4 + i * 2);
  const travel = t * 1.2, rows = 46, cols = 60, step = 70, z0 = travel % 1;
  for (let r = rows; r >= 1; r--) {
    const zw = (r - z0) * step + 40, zi = r + Math.floor(travel);
    g.beginPath();
    for (let c = 0; c <= cols; c++) { const xw = (c - cols / 2) * step;
      const h = noise(c * 0.16, zi * 0.16) ** 1.6 * amp * clamp(Math.abs(c - cols / 2) / 6, 0.25, 1);
      const sx = W / 2 + xw * f / zw, sy = horizon + (camY - h) * f / zw;
      c ? g.lineTo(sx, sy) : g.moveTo(sx, sy); }
    g.lineTo(W * 2, H * 2); g.lineTo(-W, H * 2); g.closePath();
    g.fillStyle = C.ink; g.fill();
    const near = 1 - r / rows;
    g.strokeStyle = mix("#3340a0", C.accent, near ** 0.7); g.lineWidth = 1 + near * 2.2; g.stroke();
  }
}
"""),

# ---------------------------------------------------------------- paper-collage
dict(slug="paper-collage", title="Paper Collage", dur=6, bg="#e9e2d3",
desc="Torn paper cutouts, halftone photo scraps, tape and a stamped headline slap onto a textured board in stop-motion steps. Use for Vox-style explainers, editorial and documentary scenes, zines, history, culture, scrapbook and handmade-feel motion.",
look="A warm paper board with fibre texture. Pieces arrive with a 'slap': slight overshoot rotation, a drop shadow that tightens as they land, and a brief squash. Everything moves on 12 fps steps so it feels hand-animated. Torn edges come from jagged clip-paths; photos are halftone dots; strips of masking tape pin the corners.",
beats=["0.0–0.4 s: board fades up.",
       "0.3–2.6 s: five pieces slap in 0.4 s apart (back ease, quantised to 12 fps).",
       "2.8–3.6 s: headline label stamps in with a scale overshoot; tape strips drop.",
       "Continuous: everything 'boils', tiny 12 fps jitter of ±0.6°."],
build="""
Quantise time first: `tq = Math.floor(t * 12) / 12`, then compute every tween from `tq`, which gives the stop-motion cadence for free. Each piece is a div with a generated jagged `clip-path: polygon(...)` (seeded, so it's stable), a `radial-gradient` halftone or flat colour, and a `drop-shadow` filter whose offset shrinks as the piece lands (it reads as height). The boil is a seeded per-frame rotation: `rng(seed + frameIndex)`.
""",
knobs=["Frame cadence (12 fps; 8 for cruder, 24 for smoother).",
       "Overshoot rotation per piece and landing order.",
       "Halftone dot size/colour; swap in real photos with `mix-blend-mode:multiply`.",
       "Boil amplitude (0.6°)."],
pitfalls=["Quantise everything from the same `tq`, or smooth and stepped motion mix and look like a bug.",
          "Generate torn edges once (seeded), not per frame, unless you want the edge itself to boil.",
          "Keep the palette to 3–4 inks plus paper or it stops reading as print."],
pairs=["halftone-wave", "marker-draw", "kinetic-type", "typewriter"],
css="""
#root { background-image: radial-gradient(rgba(0,0,0,.035) 1px, transparent 1.4px); background-size: 7px 7px; }
.pc { position:absolute; will-change:transform; }
.ht { background: radial-gradient(circle, #1a1a1a 38%, transparent 42%) 0 0/16px 16px, var(--pink); }
.ht2 { background: radial-gradient(circle, #1a1a1a 30%, transparent 34%) 0 0/12px 12px, var(--yellow); }
.tape { position:absolute; width:150px; height:46px; background:rgba(240,228,190,.82); }
#head { position:absolute; left:640px; top:430px; padding:26px 46px; background:var(--accent); color:var(--paper);
  font-size:110px; letter-spacing:-3px; line-height:1; }
#sub { position:absolute; left:690px; top:600px; padding:10px 20px; background:var(--ink); color:var(--paper); font:700 30px var(--mono); }
""",
html="""
<div class="pc ht" id="p1" style="left:180px;top:140px;width:520px;height:380px"></div>
<div class="pc" id="p2" style="left:1180px;top:110px;width:560px;height:420px;background:var(--blue)"></div>
<div class="pc ht2" id="p3" style="left:300px;top:600px;width:460px;height:340px"></div>
<div class="pc" id="p4" style="left:1240px;top:580px;width:480px;height:360px;background:#2b2b2b"></div>
<div class="pc" id="p5" style="left:860px;top:220px;width:300px;height:300px;background:var(--paper);border:3px solid var(--ink)"></div>
<div class="tape" id="t1" style="left:230px;top:118px"></div>
<div class="tape" id="t2" style="left:1560px;top:90px"></div>
<div class="pc" id="head">CUT &amp; PASTE</div>
<div class="pc" id="sub">THE HISTORY OF COLLAGE</div>
""",
js="""
function torn(seed, n = 34, amp = 2.2) { const r = rng(seed), pts = [];
  const edge = (x0, y0, x1, y1) => { for (let i = 0; i < n; i++) { const u = i / n;
    pts.push(`${(lerp(x0, x1, u) + (r() - 0.5) * amp * (y0 === y1 ? 0 : 1)).toFixed(2)}% ${(lerp(y0, y1, u) + (r() - 0.5) * amp * (x0 === x1 ? 0 : 1)).toFixed(2)}%`); } };
  edge(1, 1, 99, 1); edge(99, 1, 99, 99); edge(99, 99, 1, 99); edge(1, 99, 1, 1); return `polygon(${pts.join(",")})`; }
const pieces = ["#p1", "#p2", "#p3", "#p4", "#p5"].map($);
pieces.forEach((p, i) => p.style.clipPath = torn(11 + i));
const rots = [-4, 3, 5, -3, 8];
function renderAt(t) {
  const tq = Math.floor(t * 12) / 12, fi = Math.floor(t * 12);
  $("#root").style.opacity = E.out(seg(tq, 0, 0.4));
  pieces.forEach((p, i) => { const a = 0.3 + i * 0.4, k = seg(tq, a, a + 0.4), kb = E.back(k);
    const boil = (rng(fi * 31 + i)() - 0.5) * 1.2;
    const lift = (1 - E.out(k)) * 26;
    p.style.opacity = k > 0 ? 1 : 0;
    p.style.transform = `translateY(${(1 - kb) * -60}px) rotate(${rots[i] * (2 - kb) + boil}deg) scale(${lerp(1.25, 1, kb)})`;
    p.style.filter = `drop-shadow(${6 + lift}px ${10 + lift}px ${4 + lift}px rgba(0,0,0,.28))`; });
  [["#t1", 2.9, -8], ["#t2", 3.05, 12]].forEach(([id, a, r]) => { const k = seg(tq, a, a + 0.25);
    $(id).style.opacity = k > 0 ? 1 : 0; $(id).style.transform = `rotate(${r}deg) scale(${lerp(1.4, 1, E.out(k))})`; });
  [["#head", 2.8], ["#sub", 3.2]].forEach(([id, a]) => { const k = seg(tq, a, a + 0.35), boil = (rng(fi * 7 + a * 10)() - 0.5) * 1.2;
    $(id).style.opacity = k > 0 ? 1 : 0; $(id).style.transform = `rotate(${-2 + boil}deg) scale(${lerp(1.8, 1, E.back(k))})`; });
}
"""),

# ---------------------------------------------------------------- type-ring
dict(slug="type-ring", title="Type Ring", dur=6, bg="var(--ink)",
desc="Rows of text wrapped around an invisible 3D cylinder that spin in alternating directions, a rotating marquee tower of words. Use for skill lists, taglines, services, 'kinetic type' showreel moments, brand values and looping text sculptures.",
look="Three stacked rings of uppercase words orbit a vertical axis. Front-facing letters are bright paper, back-facing ones fade to a dim outline so the cylinder reads round. Alternate rows spin opposite ways; the whole tower tilts slightly toward camera.",
beats=["0.0–0.9 s: rings fade/scale in from the centre row outward.",
       "Continuous: rows rotate ±40°/s in alternating directions.",
       "2.5–4.5 s: tower tilt eases from 18° to −10°.",
       "4.5–6.0 s: middle row's accent word swings to the front and holds."],
build="""
Per row, split the string into characters and place each on the cylinder: angle `a = i/n · 360°`, `transform: rotateY(a) translateZ(R)`, inside a `preserve-3d` row container whose `rotateY` is driven by `t`. Front/back is known analytically: `cos(a + rowAngle) > 0` → front; set colour and opacity per char each frame (cheap, < 200 chars). Use a monospace or tracked display face so spacing around the ring is even.
""",
knobs=["Ring radius and characters per row (density).",
       "Row speeds and directions.",
       "Tilt range; text content per row.",
       "Back-face style: dim fill, outline (`-webkit-text-stroke`) or hidden."],
pitfalls=["Pad the string so the ring closes cleanly (no gap or overlap where it wraps).",
          "`backface-visibility:hidden` breaks the dim back-face look; compute front/back yourself.",
          "Too many chars per ring tanks DOM performance; 60–80 per row is plenty."],
pairs=["marquee-brands", "kinetic-type", "carousel-ring", "helix"],
css="""
.tower { position:absolute; left:50%; top:50%; transform-style:preserve-3d; perspective:2400px; }
.row { position:absolute; left:0; top:0; transform-style:preserve-3d; }
.ch { position:absolute; left:-28px; top:-55px; width:56px; height:110px; text-align:center; font-size:84px; line-height:110px; }
.stage { position:absolute; inset:0; perspective:2400px; }
""",
html="""<div class="stage"><div class="tower" id="tower"></div></div>""",
js="""
const rows = ["MOTION DESIGN · KINETIC TYPE · ", "EASE IN · EASE OUT · ", "LOOP FOREVER · MAKE IT MOVE · "];
const R = 520, tower = $("#tower"), rowEls = [];
rows.forEach((txt, r) => { const row = document.createElement("div"); row.className = "row"; tower.appendChild(row);
  const n = txt.length * Math.max(1, Math.round(2 * Math.PI * R / 58 / txt.length)), chars = [];  // whole repeats: no seam
  for (let i = 0; i < n; i++) { const s = document.createElement("span"); s.className = "ch"; s.textContent = txt[i % txt.length];
    row.appendChild(s); chars.push({ s, a: (i / n) * 360 }); }
  rowEls.push({ row, chars, y: (r - 1) * 150, dir: r % 2 ? -1 : 1 }); });
function renderAt(t) {
  const tilt = lerp(18, -10, E.inOut(seg(t, 2.5, 4.5)));
  tower.style.transform = `rotateX(${tilt}deg)`;
  rowEls.forEach((R_, r) => {
    const k = E.out(seg(t, Math.abs(r - 1) * 0.3, 0.6 + Math.abs(r - 1) * 0.3));
    let ang = R_.dir * t * 40 + r * 25;
    if (r === 1) ang = lerp(ang, Math.round(ang / 360) * 360 + 360 - 15, E.inOut(seg(t, 4.5, 5.6)));
    R_.row.style.transform = `translateY(${R_.y}px) rotateY(${ang}deg) scale(${lerp(0.7, 1, k)})`;
    R_.row.style.opacity = k;
    R_.chars.forEach(c => { c.s.style.transform = `rotateY(${c.a}deg) translateZ(${R}px)`;
      const front = Math.cos((c.a + ang) * Math.PI / 180);
      c.s.style.color = front > 0 ? (r === 1 && t > 4.5 ? C.accent : C.paper) : "rgba(239,233,223,.16)"; });
  });
}
"""),

# ---------------------------------------------------------------- cursor-tour
dict(slug="cursor-tour", title="Cursor Tour", dur=7, bg="#dfe3ea",
desc="A cursor glides through a product UI on eased curves, hovers, clicks with a ripple and the camera follows and zooms into each action. Use for SaaS demos, product walkthroughs, feature tours, onboarding, 'how it works in 3 clicks' and launch videos.",
look="A clean app window floats on a soft background. A macOS-style cursor travels on curved paths (never straight lines), slows into each target, presses (cursor scales to 0.85), a ring ripples out, and the UI responds: a button fills, a toggle slides, a card highlights. The whole window gently zooms toward the action.",
beats=["0.0–0.6 s: window rises into place.",
       "0.8–2.0 s: cursor travels to 'New project', clicks at 2.0 s; button fills.",
       "2.4–3.6 s: cursor moves to the toggle, clicks at 3.6 s; toggle slides on.",
       "4.0–5.2 s: cursor moves to the card, clicks at 5.2 s; card lifts and outlines.",
       "Camera: scale 1→1.25 centred on each target during each move, back to 1 at 6.2 s."],
build="""
Waypoints `[{x,y,t}]`. Between two waypoints the cursor follows a quadratic Bézier whose control point is offset perpendicular to the segment, which gives the natural human curve, with `E.inOut` progress. A click is a 0.18 s window: cursor scale dips, a ring expands (scale 0→1, opacity 1→0), and the target's state switches at the click instant. The camera is a transform on the window wrapper: translate so the current target sits centre, scale up, all eased.
""",
knobs=["Waypoints and click times.",
       "Curve bend (perpendicular offset, ±80 px).",
       "Camera zoom per step (1.15–1.4).",
       "Swap the mock UI for a real screenshot with hotspots."],
pitfalls=["Straight-line cursor moves look robotic; always bend them.",
          "Change UI state exactly at the click frame, not before.",
          "Zooming and cursor moving at full speed together causes nausea: ease both."],
pairs=["command-palette", "chat-thread", "notifications", "before-after"],
css="""
#cam { position:absolute; inset:0; transform-origin:0 0; }
.win { position:absolute; left:260px; top:140px; width:1400px; height:800px; border-radius:22px; background:#fff;
  box-shadow:0 40px 100px rgba(20,30,60,.22); overflow:hidden; font-family: var(--mono); }
.bar { height:56px; background:#f3f4f7; display:flex; align-items:center; gap:10px; padding:0 22px; }
.bar i { width:14px; height:14px; border-radius:50%; background:#d5d8de; display:inline-block; }
.side { position:absolute; left:0; top:56px; bottom:0; width:280px; background:#f7f8fa; }
#btn { position:absolute; left:360px; top:110px; padding:22px 34px; border-radius:14px; border:3px solid var(--blue); color:var(--blue); font:700 26px var(--mono); }
.tg { position:absolute; left:360px; top:270px; width:120px; height:62px; border-radius:40px; background:#d9dce3; }
#knob { position:absolute; top:6px; left:6px; width:50px; height:50px; border-radius:50%; background:#fff; box-shadow:0 2px 6px rgba(0,0,0,.2); }
.tl { position:absolute; left:510px; top:283px; font:600 26px var(--mono); color:#444; }
.card { position:absolute; top:420px; width:300px; height:260px; border-radius:20px; background:#f2f3f6; }
#card2 { outline:0 solid var(--accent); }
#cursor { position:absolute; left:0; top:0; width:44px; height:44px; z-index:9; transform-origin:4px 4px; }
#ring { position:absolute; width:90px; height:90px; margin:-45px 0 0 -45px; border-radius:50%; border:4px solid var(--blue); z-index:8; }
""",
html="""
<div id="cam">
  <div class="win" id="win">
    <div class="bar"><i></i><i></i><i></i></div><div class="side"></div>
    <div id="btn">+ New project</div>
    <div class="tg" id="tg"><div id="knob"></div></div><div class="tl">Auto-publish</div>
    <div class="card" style="left:360px"></div><div class="card" id="card2" style="left:700px"></div><div class="card" style="left:1040px"></div>
  </div>
  <div id="ring"></div>
  <svg id="cursor" viewBox="0 0 24 24"><path d="M3 2l7 19 2.6-7.4L20 11z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>
</div>
""",
js="""
const WP = [{ x: 1500, y: 980, t: 0.8 }, { x: 760, y: 300, t: 2.0 }, { x: 680, y: 450, t: 3.6 }, { x: 960, y: 700, t: 5.2 }, { x: 1300, y: 900, t: 6.4 }];
const clicks = [2.0, 3.6, 5.2], targets = [[760, 300], [680, 450], [960, 700]];
function cursorAt(t) {
  if (t <= WP[0].t) return [WP[0].x, WP[0].y];
  for (let i = 0; i < WP.length - 1; i++) { const a = WP[i], b = WP[i + 1]; const t0 = a.t + 0.35;
    if (t < t0) return [a.x, a.y];
    if (t <= b.t) { const u = E.inOut(seg(t, t0, b.t)), dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy) || 1;
      const cx = (a.x + b.x) / 2 - dy / L * 90, cy = (a.y + b.y) / 2 + dx / L * 90;
      return [(1 - u) ** 2 * a.x + 2 * (1 - u) * u * cx + u * u * b.x, (1 - u) ** 2 * a.y + 2 * (1 - u) * u * cy + u * u * b.y]; } }
  const l = WP[WP.length - 1]; return [l.x, l.y]; }
function renderAt(t) {
  const rise = E.out(seg(t, 0, 0.6));
  $("#win").style.transform = `translateY(${(1 - rise) * 80}px)`; $("#win").style.opacity = rise;
  let zx = W / 2, zy = H / 2, z = 1;
  targets.forEach(([x, y], i) => { const a = i ? clicks[i - 1] + 0.3 : 0.8, k = E.inOut(seg(t, a, clicks[i]));
    if (t >= a) { zx = lerp(zx, x, k); zy = lerp(zy, y, k); z = lerp(z, 1.25, k); } });
  const back = E.inOut(seg(t, 5.6, 6.4)); zx = lerp(zx, W / 2, back); zy = lerp(zy, H / 2, back); z = lerp(z, 1, back);
  $("#cam").style.transform = `translate(${W / 2 - zx * z}px, ${H / 2 - zy * z}px) scale(${z})`;
  const [cx, cy] = cursorAt(t);
  let press = 1, ring = -1;
  clicks.forEach(c => { if (t >= c - 0.09 && t < c + 0.09) press = 0.85; if (t >= c && t < c + 0.5) ring = seg(t, c, c + 0.5); });
  $("#cursor").style.transform = `translate(${cx}px, ${cy}px) scale(${press})`;
  $("#ring").style.transform = `translate(${cx}px, ${cy}px) scale(${ring < 0 ? 0 : E.out(ring)})`;
  $("#ring").style.opacity = ring < 0 ? 0 : 1 - ring;
  const b = t >= clicks[0]; $("#btn").style.background = b ? C.blue : "transparent"; $("#btn").style.color = b ? "#fff" : C.blue;
  const tk = E.back(seg(t, clicks[1], clicks[1] + 0.3));
  $("#knob").style.transform = `translateX(${58 * tk}px)`; $("#tg").style.background = tk > 0.5 ? C.accent : "#d9dce3";
  const ck = E.back(seg(t, clicks[2], clicks[2] + 0.35));
  $("#card2").style.transform = `translateY(${-24 * ck}px)`; $("#card2").style.outlineWidth = `${6 * clamp(ck)}px`;
  $("#card2").style.boxShadow = `0 ${30 * ck}px ${60 * ck}px rgba(0,0,0,.15)`;
}
"""),

# ---------------------------------------------------------------- cube-stack
dict(slug="cube-stack", title="Cube Stack", dur=6, bg="var(--paper)",
desc="Isometric cubes drop from above and bounce into a stacked bar or staircase, each face shaded in three tones. Use for growth, building blocks, 'stacking up', progress, modular products, data as physical blocks and playful explainer moments.",
look="Clean isometric cubes in three-tone shading (top light, left mid, right dark) fall in a staggered wave and land with a small bounce and squash, stacking into rising columns. Final frame is a tidy 3D bar chart of blocks with a label.",
beats=["0.2–3.2 s: cubes drop column by column, bottom to top, 0.07 s apart.",
       "Each cube: 0.55 s fall with bounce ease, squash 0.85 on contact.",
       "3.4–4.2 s: the label slides in and the tallest column turns accent.",
       "4.4–6.0 s: hold with a gentle camera drift."],
build="""
Isometric projection: `sx = (x - y) * cos30 * s`, `sy = (x + y) * sin30 * s - z * s`. Each cube is three polygons (top, left, right) drawn in painter's order sorted by `x + y + z` ascending. Drop: `z = zFinal + (1 - E.bounce(k)) * 9`. Squash on landing: scale the cube's height by `0.85` for 0.08 s around contact. Columns are heights from a data array, so the stack is a real chart.
""",
knobs=["Data array (column heights) and grid layout.",
       "Cube size and gap.",
       "Drop stagger order (by column, by height, diagonal wave).",
       "Face colours (keep top lightest)."],
pitfalls=["Sort by x+y+z every frame: falling cubes change depth order.",
          "Draw faces with a 1 px overlap/stroke of the same colour to hide seams.",
          "Don't drop more than ~10 cubes at once or the eye can't follow."],
pairs=["bars-3d", "iso-city", "count-up", "tile-grids"],
html="""<canvas id="cv"></canvas><div id="lab" style="position:absolute;left:120px;top:110px;font-size:120px;letter-spacing:-4px;line-height:.9">STACK<br>IT UP.</div>""",
js="""
const g = ctx2d("cv"), heights = [2, 3, 3, 5, 4, 6, 8], s = 70, cos = Math.cos(Math.PI / 6), sin = 0.5;
const cubes = []; heights.forEach((h, x) => { for (let z = 0; z < h; z++) cubes.push({ x, y: 0, z }); });
cubes.forEach((c, i) => c.i = i);
const ox = 1060, oy = 820;
const iso = (x, y, z) => [ox + (x - y) * cos * s, oy + (x + y) * sin * s - z * s];
function face(pts, col) { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.closePath(); g.fillStyle = col; g.fill(); g.strokeStyle = col; g.lineWidth = 1; g.stroke(); }
function renderAt(t) {
  g.clearRect(0, 0, W, H);
  const drift = Math.sin(t * 0.6) * 6;
  const list = cubes.map(c => { const a = 0.2 + c.x * 0.32 + c.z * 0.07, k = seg(t, a, a + 0.55);
    const contact = k > 0.36 && k < 0.48 ? 0.85 : 1;
    return { ...c, k, zz: c.z + (1 - E.bounce(k)) * 9, sq: contact }; }).filter(c => c.k > 0);
  list.sort((a, b) => (a.x + a.y + a.zz) - (b.x + b.y + b.zz));
  const tall = heights.indexOf(Math.max(...heights)), hl = E.inOut(seg(t, 3.4, 4.0));
  for (const c of list) { const x = c.x * 1.18, y = c.y, z = c.zz, hgt = c.sq;
    const P = (dx, dy, dz) => { const p = iso(x + dx, y + dy, z + dz * hgt); return [p[0] + drift, p[1]]; };
    const top = c.x === tall ? mix("#ffd2c4", "#ffb39c", hl) : "#ffffff", L = c.x === tall ? mix("#c9c3b8", C.accent, hl) : "#c9c3b8", Rr = c.x === tall ? mix("#8f897f", "#b8300f", hl) : "#8f897f";
    face([P(0, 0, 1), P(1, 0, 1), P(1, 1, 1), P(0, 1, 1)], c.x === tall ? mix("#ffffff", "#ffc9b8", hl) : top);
    face([P(0, 1, 1), P(1, 1, 1), P(1, 1, 0), P(0, 1, 0)], L);
    face([P(1, 0, 1), P(1, 1, 1), P(1, 1, 0), P(1, 0, 0)], Rr); }
  const lk = E.out(seg(t, 3.4, 4.2)); $("#lab").style.opacity = lk; $("#lab").style.transform = `translateX(${(1 - lk) * -60}px)`;
}
"""),

# ---------------------------------------------------------------- split-flap
dict(slug="split-flap", title="Split Flap", dur=6, bg="#111111",
desc="An airport/train departure board whose characters flip mechanically through the alphabet until they land on the message. Use for announcements, destinations, launches, countdowns, 'now boarding' moments, headlines, dates and retro-mechanical reveals.",
look="A grid of dark flap cells with a hairline split. Each cell flips through characters (top half folds down over the bottom), with every cell running its own number of flips so the message resolves in a ripple from left to right. Accent-coloured cells mark the key word.",
beats=["0.0–0.4 s: board fades up showing random characters.",
       "0.4–3.2 s: cells flip, 60 ms per flip, each cell 8–22 flips, resolving left to right.",
       "3.4–5.5 s: the second row flips to the gate and time; hold to the end."],
build="""
Each cell has four layers: static top (next char), static bottom (current char), and two moving flaps, the top flap showing the current char rotating `rotateX(0 → -90deg)` in the first half of a flip and the bottom flap showing the next char rotating `90deg → 0` in the second half. For time `t`, flip index `f = floor((t - start)/0.06)` and phase `p = frac(...)` give everything, so it scrubs exactly. Each half is a 60 px window with `overflow:hidden`; the glyph inside is 120 px tall and offset so halves line up.
""",
knobs=["Flip duration (60 ms) and per-cell flip counts (min/max).",
       "Character set (A–Z 0–9 or custom).",
       "Board size; accent cells.",
       "Click sound per flip (add audio ticks at flip times)."],
pitfalls=["Compute everything from t; never accumulate flips frame to frame.",
          "Rotating halves need `backface-visibility:hidden` and a `perspective` on the cell.",
          "Monospace glyphs only, or halves misalign."],
pairs=["count-up", "scramble-decode", "typewriter", "marquee-brands"],
css="""
.board { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); display:grid; gap:12px; }
.r { display:flex; gap:10px; }
.cell { position:relative; width:96px; height:140px; perspective:500px; font:800 104px/140px var(--mono); color:#f4efe6; text-align:center; }
.h { position:absolute; left:0; width:100%; height:70px; overflow:hidden; background:#262626; }
.h span { position:absolute; left:0; width:100%; height:140px; }
.top { top:0; border-radius:10px 10px 0 0; } .top span { top:0; }
.bot { top:70px; border-radius:0 0 10px 10px; } .bot span { top:-70px; }
.ft { transform-origin:50% 100%; backface-visibility:hidden; z-index:2; }
.fb { transform-origin:50% 0%; backface-visibility:hidden; z-index:2; }
.cell:after { content:""; position:absolute; left:0; right:0; top:69px; height:2px; background:#0a0a0a; z-index:3; }
.acc .h { background:var(--accent); }
""",
html="""<div class="board" id="board"></div>""",
js="""
const CH = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:.";
const msg = ["NOW BOARDING", "GATE 26 14:05"], board = $("#board"), cells = [];
msg.forEach((line, r) => { const row = document.createElement("div"); row.className = "r"; board.appendChild(row);
  [...line.padEnd(13)].forEach((ch, i) => { const c = document.createElement("div"); c.className = "cell" + (r === 0 && i < 3 ? " acc" : "");
    c.innerHTML = '<div class="h top"><span></span></div><div class="h bot"><span></span></div><div class="h top ft"><span></span></div><div class="h bot fb"><span></span></div>';
    row.appendChild(c); const rr = rng(r * 100 + i), n = 8 + Math.floor(rr() * 14), tgt = CH.indexOf(ch);
    cells.push({ el: c, sp: [...c.querySelectorAll("span")], n, tgt, start: (r ? 3.4 : 0.4) + i * (r ? 0.05 : 0.08), from: (tgt - n + CH.length * 4) % CH.length }); }); });
function renderAt(t) {
  board.style.opacity = E.out(seg(t, 0, 0.4));
  cells.forEach(c => { const el = (t - c.start) / 0.06; let f = Math.floor(el), p = el - f;
    if (f < 0) { f = 0; p = 0; } if (f >= c.n) { f = c.n; p = 0; }
    const cur = CH[(c.from + f) % CH.length], nxt = CH[(c.from + Math.min(f + 1, c.n)) % CH.length];
    const [top, bot, ft, fb] = c.sp;
    top.textContent = p > 0 ? nxt : cur; bot.textContent = cur; ft.textContent = cur; fb.textContent = nxt;
    const ftEl = ft.parentNode, fbEl = fb.parentNode;
    ftEl.style.transform = `rotateX(${p < 0.5 ? -180 * p : -90}deg)`; ftEl.style.visibility = p > 0 && p < 0.5 ? "visible" : "hidden";
    fbEl.style.transform = `rotateX(${p >= 0.5 ? 180 * (1 - p) : 90}deg)`; fbEl.style.visibility = p >= 0.5 ? "visible" : "hidden";
    if (p >= 0.5) bot.textContent = cur; });
}
"""),
]
