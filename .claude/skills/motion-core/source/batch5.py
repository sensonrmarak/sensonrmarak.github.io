RECIPES = [
# ---------------------------------------------------------------- pixel-build
dict(slug="pixel-build", title="Pixel Build", dur=6, bg="var(--ink)",
desc="A word or logo assembles out of hundreds of square pixels that fly in from a scattered cloud and snap into place column by column, then a shine sweeps across. Use for 'building' and 'creating' metaphors, logo reveals, game/retro titles, digital transformation, assembly and data-to-insight moments.",
look="A cloud of small squares hangs scattered and dim. In a left-to-right wave they fly to their target positions (eased, with slight rotation that settles to 0), turning from blue to accent as they land, until the word is complete. A diagonal highlight band sweeps across the finished word.",
beats=["0.0–0.6 s: scattered pixels fade in, drifting slowly.",
       "0.6–3.0 s: pixels fly to targets; delay by target x plus a seeded jitter.",
       "3.2–4.0 s: shine band sweeps left to right.",
       "4.0–6.0 s: hold; pixels breathe ±1 px on a sine for life."],
build="""
Render the word once to an offscreen canvas, sample it on a grid (every 14 px) and keep cells whose alpha > 128: those are the targets. Each target gets a seeded start position and rotation. Position is `lerp(start, target, E.expo(k))` with `k` from a delay proportional to target x. Colour mixes blue → accent with `k`. The shine adds brightness where `x + y·0.5` is near a moving line.
""",
knobs=["Word or logo (any canvas-drawable text/image).",
       "Pixel size and gap (14 px cell, 11 px square).",
       "Wave direction and spread of the start cloud.",
       "Shine on/off and colour."],
pitfalls=["Wait for the font before sampling the offscreen text or you build the fallback font.",
          "More than ~3,000 pixels gets slow in canvas preview; increase the cell size.",
          "Expo ease makes pixels arrive crisply; linear looks floaty."],
pairs=["tile-grids", "logo-land", "particle-sphere", "scramble-decode"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), CELL = 14, SQ = 11; let PX = null;
function sample() { const o = document.createElement("canvas"); o.width = W; o.height = H; const c = o.getContext("2d");
  c.fillStyle = "#fff"; c.font = "400 330px 'Archivo Black', Arial Black, sans-serif"; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("BUILD.", W / 2, H / 2);
  const d = c.getImageData(0, 0, W, H).data, r = rng(3), out = [];
  for (let y = 0; y < H; y += CELL) for (let x = 0; x < W; x += CELL) if (d[(y * W + x) * 4 + 3] > 128)
    out.push({ x, y, sx: W / 2 + (r() - 0.5) * W * 1.3, sy: H / 2 + (r() - 0.5) * H * 1.4, rot: (r() - 0.5) * 3, j: r() * 0.35, ph: r() * 6 });
  return out; }
function renderAt(t) {
  if (!PX || (document.fonts.status === "loaded" && !PX.ok)) { PX = sample(); PX.ok = document.fonts.status === "loaded"; }
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  const fade = E.out(seg(t, 0, 0.6)), shine = seg(t, 3.2, 4.0) * (W + 900) - 300;
  for (const p of PX) { const k = E.expo(seg(t, 0.6 + p.x / W * 1.8 + p.j, 1.3 + p.x / W * 1.8 + p.j));
    const br = t > 4 ? Math.sin(t * 2 + p.ph) : 0, drift = (1 - k) * Math.sin(t + p.ph) * 12;
    const x = lerp(p.sx + drift, p.x, k) + br * 0.6, y = lerp(p.sy, p.y, k), a = p.rot * (1 - k);
    const sh = Math.max(0, 1 - Math.abs(p.x + p.y * 0.5 - shine) / 140);
    g.fillStyle = sh > 0 ? mix(C.accent, "#ffffff", sh) : mix("#2b37c8", C.accent, k);
    g.globalAlpha = fade * (0.35 + 0.65 * k);
    g.save(); g.translate(x + SQ / 2, y + SQ / 2); g.rotate(a); g.fillRect(-SQ / 2, -SQ / 2, SQ, SQ); g.restore(); }
  g.globalAlpha = 1;
}
"""),

# ---------------------------------------------------------------- count-up
dict(slug="count-up", title="Count Up", dur=6, bg="var(--paper)",
desc="A big number that counts up on a rolling odometer, every digit column spinning and carrying like a mechanical counter, with a label and a sparkline drawing underneath. Use for milestones, revenue, users, downloads, raised funding, stats, KPIs, records and any 'big number' moment.",
look="A huge tabular number in heavy display type. Each digit sits in its own masked column and rolls vertically; the ones column spins fast, higher columns tick over only when the column to their right wraps, exactly like an odometer. Thousands separators stay put. A small accent sparkline draws below and a label slides in.",
beats=["0.2–3.2 s: value rolls from 0 to 2,481,903 (expo out: fast then settling).",
       "0.6–3.2 s: sparkline draws left to right in sync.",
       "3.2 s: final digits land with a 1.04 scale pop; label slides up.",
       "3.5–6.0 s: hold."],
build="""
Value `v = target·E.expo(k)`. For digit column `j` (10^j), the strip position is `floor(v / 10^j) mod 10` plus a carry fraction: when the lower part `v mod 10^j` is in its last 10 %, add `(fraction - 0.9)/0.1` so the column rolls over just as the column to its right wraps. The ones column rolls continuously. Each column is a strip `0…9,0` translated by `-pos × digitHeight`.
""",
knobs=["Target value, prefix/suffix ($, %, K, +).",
       "Duration and ease (expo for drama, inOut for calm).",
       "Separator style; digit font size.",
       "Sparkline data or off."],
pitfalls=["Use tabular figures (or fixed-width columns) or digits jitter sideways.",
          "Don't count for more than ~3 s; viewers only read the final number.",
          "Round the displayed final value exactly to the target at the end."],
pairs=["donut-ring", "bars-3d", "split-flap", "kinetic-type"],
css="""
#num { position:absolute; left:50%; top:300px; transform-origin:50% 50%; display:flex; font-size:250px; line-height:1; letter-spacing:-6px; }
.dc { position:relative; height:250px; width:0.72em; overflow:hidden; }
.strip { position:absolute; left:0; top:0; width:100%; text-align:center; }
.strip div { height:250px; }
.sep { width:0.32em; text-align:center; }
#lab { position:absolute; left:0; right:0; top:620px; text-align:center; font:700 34px var(--mono); letter-spacing:6px; }
svg { position:absolute; left:560px; top:720px; width:800px; height:200px; }
""",
html="""<div id="num"></div><div id="lab">CREATORS ON THE PLATFORM</div><svg viewBox="0 0 800 200"><path id="sp" fill="none" stroke="#ff4a1c" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
js="""
const TARGET = 2481903, digits = String(TARGET).length, num = $("#num"), cols = [];
const fmt = String(TARGET).replace(/\\B(?=(\\d{3})+(?!\\d))/g, ",");
[...fmt].forEach(ch => { if (ch === ",") { const s = document.createElement("div"); s.className = "sep"; s.textContent = ","; num.appendChild(s); return; }
  const c = document.createElement("div"); c.className = "dc"; c.innerHTML = `<div class="strip">${[0,1,2,3,4,5,6,7,8,9,0].map(d => `<div>${d}</div>`).join("")}</div>`; num.appendChild(c); cols.push(c.firstChild); });
const pts = [12, 18, 15, 26, 30, 28, 44, 52, 49, 68, 80, 96].map((v, i, a) => [i / (a.length - 1) * 780 + 10, 190 - v * 1.8]);
$("#sp").setAttribute("d", pts.map((p, i) => (i ? "L" : "M") + p.join(" ")).join(" ")); const SL = $("#sp").getTotalLength(); $("#sp").style.strokeDasharray = SL;
function renderAt(t) {
  const k = seg(t, 0.2, 3.2), v = k >= 1 ? TARGET : TARGET * E.expo(k);
  cols.forEach((s, idx) => { const j = digits - 1 - idx, p10 = 10 ** j;
    let pos = Math.floor(v / p10) % 10;
    if (j === 0) pos = v % 10; else { const frac = (v % p10) / p10; if (frac > 0.9) pos += (frac - 0.9) / 0.1; }
    if (k >= 1) pos = Math.floor(TARGET / p10) % 10;
    s.style.transform = `translateY(${-pos * 250}px)`; });
  const pop = 1 + 0.04 * Math.sin(Math.PI * seg(t, 3.2, 3.5));
  num.style.transform = `translateX(-50%) scale(${pop})`;
  $("#sp").style.strokeDashoffset = SL * (1 - E.inOut(seg(t, 0.6, 3.2)));
  const lk = E.out(seg(t, 3.2, 3.8)); $("#lab").style.opacity = lk; $("#lab").style.transform = `translateY(${(1 - lk) * 30}px)`;
}
"""),

# ---------------------------------------------------------------- particle-sphere
dict(slug="particle-sphere", title="Particle Sphere", dur=6, bg="var(--ink)",
desc="Thousands of particles swirl in from chaos and assemble into a rotating sphere that breathes with noise, then morph into a torus ring. Use for AI/neural visuals, data and 'big picture' moments, global community, energy/science scenes, logo-adjacent 3D beats and showreel particle chapters.",
look="Particles start scattered across the frame. They converge onto a Fibonacci sphere, which rotates slowly; each point is pushed in and out by a travelling wave so the surface ripples. Near particles are larger and paper-white, far ones small and accent-tinted. Late in the clip the sphere flows into a torus.",
beats=["0.0–0.5 s: scattered cloud fades in.",
       "0.5–2.2 s: particles converge to the sphere (staggered by index).",
       "2.2–4.2 s: sphere rotates; surface ripple.",
       "4.2–5.4 s: morph sphere → torus.",
       "5.4–6.0 s: torus holds and spins."],
build="""
Precompute per particle: a seeded chaos position, its Fibonacci-sphere point and its torus point (same index → stable morph). Position = chaos → sphere (`E.inOut` with index stagger), then sphere → torus. Apply ripple `1 + 0.06·sin(4·lat + t·3)` radially, rotate with `rot()`, project with `proj()`, then sort by depth and draw squares sized by the projected scale.
""",
knobs=["Particle count (2,000–5,000).",
       "Target shapes (sphere, torus, text sampled to 3D points).",
       "Ripple amplitude and speed; rotation speed.",
       "Colour by depth or by index."],
pitfalls=["Depth-sort every frame or near/far particles overlap wrongly.",
          "Use squares (`fillRect`), not arcs, for thousands of particles: much faster.",
          "Give every particle a stable target index so morphs don't shuffle."],
pairs=["torus-wire", "helix", "orbit-rings", "pixel-build"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), N = 3200, r0 = rng(17), P = [];
for (let i = 0; i < N; i++) { const y = 1 - (i / (N - 1)) * 2, rr = Math.sqrt(1 - y * y), th = i * 2.39996;
  const u = (i / N) * Math.PI * 2 * 24, v = (i * 0.618034 % 1) * Math.PI * 2;
  P.push({ c: [(r0() - 0.5) * 2600, (r0() - 0.5) * 1600, (r0() - 0.5) * 1200], s: [Math.cos(th) * rr, y, Math.sin(th) * rr],
    o: [(1 + 0.38 * Math.cos(v)) * Math.cos(u) / 1.38, 0.38 * Math.sin(v) / 1.38, (1 + 0.38 * Math.cos(v)) * Math.sin(u) / 1.38], lat: Math.asin(y), d: r0() * 0.5 }); }
function renderAt(t) {
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  const R = 360, fade = E.out(seg(t, 0, 0.5)), mt = E.inOut(seg(t, 4.2, 5.4)), ay = t * 0.5, ax = 0.35 + 0.25 * mt, items = [];
  for (const p of P) { const k = E.inOut(seg(t, 0.5 + p.d, 1.7 + p.d)), rip = 1 + 0.06 * Math.sin(p.lat * 4 + t * 3) * seg(t, 2.2, 2.6);
    const tg = [lerp(p.s[0], p.o[0], mt) * R * rip, lerp(p.s[1], p.o[1], mt) * R * rip, lerp(p.s[2], p.o[2], mt) * R * rip];
    const q = rot([lerp(p.c[0], tg[0], k), lerp(p.c[1], tg[1], k), lerp(p.c[2], tg[2], k)], ax, ay); items.push(proj(q, 1400)); }
  items.sort((a, b) => a[2] - b[2]);
  for (const [x, y, s] of items) { const near = clamp((s - 0.7) / 0.6);
    g.fillStyle = near > 0.5 ? C.paper : mix(C.accent, C.paper, near * 2); g.globalAlpha = fade * (0.3 + 0.7 * near);
    const z = 1.2 + 3.6 * near; g.fillRect(x - z / 2, y - z / 2, z, z); }
  g.globalAlpha = 1;
}
"""),

# ---------------------------------------------------------------- flow-line
dict(slug="flow-line", title="Flow Line", dur=6, bg="var(--paper)",
desc="A curved process line that draws through a sequence of step nodes, each node lighting up and labelling as the head passes, then dashes keep flowing along the path. Use for processes and workflows, user journeys, pipelines, roadmaps, timelines, 'how it works' steps and onboarding flows.",
look="A smooth S-curve snakes across the frame through four circular nodes. The line draws from the first node; as the head reaches each node, the node fills accent with a pop and a numbered label rises beside it. Once complete, small dashes march along the line forever, showing flow direction.",
beats=["0.2–3.4 s: line draws through the path (in-out).",
       "Each node pops when the head reaches its path length.",
       "Labels rise 0.15 s after their node.",
       "3.6 s →: marching dashes flow along the path (offset −t·120)."],
build="""
One SVG path for the route. Node positions are chosen as fractions of the path length (`getPointAtLength`), so they're exactly on the line and their trigger time is just `fraction ↔ progress`. The draw uses the dashoffset technique; the flow is a second copy of the path with a short dash pattern (`14 22`) and `stroke-dashoffset = -t·120`, faded in after the draw.
""",
knobs=["Path shape and node fractions.",
       "Step labels; node size; colours.",
       "Draw duration; flow speed and dash pattern.",
       "Direction (reverse the path for right-to-left)."],
pitfalls=["Place nodes by path length, not by guessing coordinates, or they float off the line.",
          "Labels must not collide with the curve; alternate them above/below.",
          "Marching dashes faster than ~200 px/s strobe in video."],
pairs=["line-draw", "agent-swarm", "ribbon-twist", "blueprint-draw"],
css="""svg { position:absolute; inset:0; } .lb { font:700 26px var(--mono); fill:#6f6a61; } .lt { font:400 46px var(--display); fill:#0e0e0e; letter-spacing:-1px; }""",
html="""
<svg viewBox="0 0 1920 1080">
  <path id="base" fill="none" stroke="#0e0e0e" stroke-width="8" stroke-linecap="round" d="M180 760 C420 760 420 320 720 320 C1020 320 900 760 1200 760 C1500 760 1460 320 1740 320"/>
  <path id="flow" fill="none" stroke="#ff4a1c" stroke-width="8" stroke-linecap="round" stroke-dasharray="14 22" d="M180 760 C420 760 420 320 720 320 C1020 320 900 760 1200 760 C1500 760 1460 320 1740 320"/>
  <g id="nodes"></g>
</svg>
""",
js="""
const base = $("#base"), L = base.getTotalLength(); base.style.strokeDasharray = L;
const STEPS = [[0.0, "01", "Write"], [0.36, "02", "Render"], [0.64, "03", "Review"], [1.0, "04", "Ship"]], NS = "http://www.w3.org/2000/svg", nodes = [];
STEPS.forEach(([f, n, name], i) => { const p = base.getPointAtLength(L * f), gN = document.createElementNS(NS, "g"); gN.setAttribute("transform", `translate(${p.x} ${p.y})`);
  const up = i % 2 ? 1 : -1;
  gN.innerHTML = `<circle r="34" fill="#efe9df" stroke="#0e0e0e" stroke-width="8"/><g class="lab"><text class="lb" x="0" y="${up * 80 - (up < 0 ? 40 : 0)}" text-anchor="middle">${n}</text><text class="lt" x="0" y="${up * 80 + (up < 0 ? 4 : 44)}" text-anchor="middle">${name}</text></g>`;
  $("#nodes").appendChild(gN); nodes.push({ gN, f, c: gN.querySelector("circle"), lab: gN.querySelector(".lab") }); });
function renderAt(t) {
  const k = E.inOut(seg(t, 0.2, 3.4)); base.style.strokeDashoffset = L * (1 - k);
  nodes.forEach(n => { const at = n.f <= k + 1e-6 && t >= 0.2, tAt = 0.2 + 3.2 * invEase(n.f), pk = E.back(seg(t, tAt, tAt + 0.3));
    n.c.setAttribute("fill", at ? C.accent : C.paper); n.c.setAttribute("r", (34 * (0.6 + 0.4 * (at ? pk : 0))).toFixed(2));
    n.gN.style.opacity = t >= 0.2 ? 1 : 0;
    const lk = E.out(seg(t, tAt + 0.15, tAt + 0.55)); n.lab.style.opacity = lk; n.lab.setAttribute("transform", `translate(0 ${(1 - lk) * 20})`); });
  $("#flow").style.strokeDashoffset = -t * 120; $("#flow").style.opacity = E.out(seg(t, 3.4, 3.9));
}
function invEase(y) { let lo = 0, hi = 1; for (let i = 0; i < 30; i++) { const m = (lo + hi) / 2; E.inOut(m) < y ? lo = m : hi = m; } return (lo + hi) / 2; }
"""),

# ---------------------------------------------------------------- phone-scroll
dict(slug="phone-scroll", title="Phone Scroll", dur=6, bg="var(--yellow)",
desc="A phone whose feed scrolls with real momentum (a fling that decelerates), cards parallaxing, a thumb-tap that likes a post with a heart burst, beside a headline. Use for social apps, content feeds, e-commerce browsing, 'endless scroll' commentary, app demos and creator-economy explainers.",
look="A phone on the right third of the frame, tilted 6°. Its feed flings upward quickly then decelerates like iOS momentum scrolling, overshoots slightly and settles. A translucent thumb circle taps a post; a heart pops and bursts into small particles. A bold headline sits left.",
beats=["0.0–0.6 s: phone slides in from the right; headline rises.",
       "0.8–2.6 s: fling: fast start, exponential decay.",
       "2.6–3.0 s: small rubber-band settle.",
       "3.4 s: tap indicator; 3.5–4.1 s heart pop and burst.",
       "4.4–5.8 s: a second, gentler scroll; hold."],
build="""
Momentum is `y = v0·τ·(1 - e^(-t/τ))`, the closed form of exponential friction, so it scrubs perfectly. A short settle uses a damped sine. Image tiles inside cards translate at 0.9× the feed speed for parallax. The heart is an SVG path scaled with an elastic ease; burst particles are 10 dots on radial lines with seeded angles.
""",
knobs=["Fling velocity v0 and friction τ.",
       "Feed content (swap blocks for real screenshots).",
       "Tap time/position; like colour.",
       "Phone tilt and headline copy."],
pitfalls=["Linear scroll looks like a slideshow; always use the exponential decay curve.",
          "Keep the tapped post fully visible at the tap moment.",
          "Don't scroll and zoom the phone at the same time."],
pairs=["phone-orbit", "phone-trio", "notifications", "chat-thread"],
css="""
#hd { position:absolute; left:140px; top:330px; font-size:140px; line-height:.92; letter-spacing:-5px; }
.ph { position:absolute; left:1150px; top:90px; width:440px; height:900px; border-radius:66px; background:#0b0b0b; box-shadow:0 60px 120px rgba(0,0,0,.3); }
.sc { position:absolute; inset:16px; border-radius:52px; overflow:hidden; background:#fff; }
#feed { position:absolute; left:0; right:0; top:0; }
.post { margin:24px; height:420px; border-radius:30px; background:#f1f1f1; overflow:hidden; position:relative; }
.img { position:absolute; left:0; right:0; top:-40px; height:420px; }
#tap { position:absolute; width:90px; height:90px; margin:-45px 0 0 -45px; border-radius:50%; background:rgba(0,0,0,.25); z-index:5; }
#heart { position:absolute; left:220px; top:440px; width:160px; height:160px; margin:-80px 0 0 -80px; z-index:6; }
""",
html="""
<div id="hd">Scroll<br>less.<br>Make<br>more.</div>
<div class="ph" id="ph"><div class="sc"><div id="feed"></div><div id="tap"></div>
<svg id="heart" viewBox="-60 -60 120 120"><g id="burst"></g><path id="hp" fill="#ff2d55" d="M0 30 C-40 5 -45 -25 -22 -32 C-10 -36 -2 -28 0 -20 C2 -28 10 -36 22 -32 C45 -25 40 5 0 30Z"/></svg></div></div>
""",
js="""
const COLS = [C.accent, C.blue, C.pink, C.ink, C.lime, "#8b5cf6", C.yellow, C.accent, C.blue, C.pink, C.ink, C.lime];
COLS.forEach(c => { const d = document.createElement("div"); d.className = "post"; d.innerHTML = `<div class="img" style="background:linear-gradient(160deg,${c},${mix(c, "#000000", .3)})"></div>`; $("#feed").appendChild(d); });
const imgs = $$(".img"), br = rng(4);
for (let i = 0; i < 10; i++) { const a = i / 10 * Math.PI * 2 + br() * 0.3, c = document.createElementNS("http://www.w3.org/2000/svg", "circle"); c.setAttribute("r", 6); c.setAttribute("fill", i % 2 ? "#ff2d55" : "#ffc21a"); c.dataset.a = a; $("#burst").appendChild(c); }
function scrollAt(t) { const fl = t < 0.8 ? 0 : 2200 * 0.55 * (1 - Math.exp(-(t - 0.8) / 0.55));
  const settle = t > 2.6 ? -30 * Math.exp(-(t - 2.6) * 6) * Math.sin((t - 2.6) * 14) : 0;
  const s2 = t < 4.4 ? 0 : 700 * 0.4 * (1 - Math.exp(-(t - 4.4) / 0.4)); return fl + settle + s2; }
function renderAt(t) {
  const sin = E.out(seg(t, 0, 0.6)); $("#ph").style.transform = `translateX(${(1 - sin) * 700}px) rotate(6deg)`;
  $("#hd").style.opacity = sin; $("#hd").style.transform = `translateY(${(1 - sin) * 60}px)`;
  const y = scrollAt(t); $("#feed").style.transform = `translateY(${-y}px)`;
  imgs.forEach(im => im.style.transform = `translateY(${y * 0.1 % 40}px)`);
  const tk = seg(t, 3.3, 3.6); $("#tap").style.left = "220px"; $("#tap").style.top = "440px";
  $("#tap").style.opacity = tk > 0 && tk < 1 ? Math.sin(tk * Math.PI) : 0; $("#tap").style.transform = `scale(${0.6 + 0.6 * tk})`;
  const hk = seg(t, 3.5, 4.1); $("#hp").setAttribute("transform", `scale(${hk > 0 ? E.elastic(hk) * (1 - E.in(seg(t, 4.4, 4.7))) : 0})`);
  [...$("#burst").children].forEach(c => { const a = +c.dataset.a, d = 70 * E.out(seg(t, 3.6, 4.1)); c.setAttribute("cx", Math.cos(a) * d); c.setAttribute("cy", Math.sin(a) * d);
    c.setAttribute("opacity", t > 3.6 ? (1 - seg(t, 3.8, 4.2)).toFixed(2) : 0); });
}
"""),

# ---------------------------------------------------------------- layer-explode
dict(slug="layer-explode", title="Layer Explode", dur=6, bg="#e7e9ee",
desc="An exploded axonometric view: a UI or product separates into stacked layers floating apart in 3D, each labelled with a leader line, then compresses back together. Use for architecture of an app or system, design anatomy, 'what's inside', tech stacks, product teardowns and layered-explanation scenes.",
look="A screen seen in isometric (rotateX 55°, rotateZ −40°). Its four layers (background, layout grid, content cards, floating UI) lift apart vertically with a staggered back-ease, revealing each plane. Thin leader lines with mono labels extend to the right of each layer. Finally they settle back into one flat screen.",
beats=["0.0–0.6 s: flat composite screen fades in, already isometric.",
       "0.8–2.0 s: layers separate upward (stagger 0.12 s).",
       "1.8–2.8 s: labels and leader lines draw in per layer.",
       "4.2–5.2 s: layers collapse back together; labels fade.",
       "5.2–6.0 s: hold on the composite."],
build="""
CSS 3D: a container with `rotateX(55deg) rotateZ(-40deg)` and `preserve-3d`; each layer is an absolutely positioned plane with `translateZ(gap·i·k)`. Labels are 2D elements outside the 3D container. Their anchor points are computed by projecting each layer's right-edge midpoint with the same matrix (here a small JS iso projection) so leader lines meet the layer edges.
""",
knobs=["Layer contents and count.",
       "Gap between layers and the iso angle.",
       "Label text and side.",
       "Explode/collapse timing."],
pitfalls=["`transform-style: preserve-3d` must be set on every ancestor between the layers and the rotated container.",
          "Semi-transparent layers help depth read; fully opaque top layers hide the rest.",
          "Keep the leader lines horizontal; diagonal leaders look messy."],
pairs=["blueprint-draw", "iso-city", "cube-fold", "swiss-grid"],
css="""
.wrap { position:absolute; left:760px; top:680px; transform-style:preserve-3d; }
.iso { transform-style:preserve-3d; transform:rotateX(55deg) rotateZ(-40deg); }
.ly { position:absolute; left:-360px; top:-240px; width:720px; height:480px; border-radius:26px; box-shadow:0 30px 40px rgba(20,30,60,.12); }
.l0 { background:#fff; } .l1 { background:repeating-linear-gradient(90deg, rgba(36,51,255,.18) 0 50px, transparent 50px 66px), rgba(255,255,255,.55); }
.l2 { background:transparent; box-shadow:none; } .l2 i { position:absolute; border-radius:18px; }
.l3 { background:transparent; box-shadow:none; } .l3 i { position:absolute; border-radius:40px; background:var(--accent); }
.lab { position:absolute; left:1240px; font:700 26px var(--mono); color:#333; white-space:nowrap; }
.lab b { display:block; font:400 40px var(--display); color:#111; letter-spacing:-1px; }
svg { position:absolute; inset:0; }
""",
html="""
<svg viewBox="0 0 1920 1080" id="lines"></svg>
<div class="wrap"><div class="iso" id="iso">
  <div class="ly l0" id="L0"></div>
  <div class="ly l1" id="L1"></div>
  <div class="ly l2" id="L2"><i style="left:40px;top:40px;width:640px;height:90px;background:#0e0e0e"></i><i style="left:40px;top:160px;width:300px;height:280px;background:var(--blue)"></i><i style="left:380px;top:160px;width:300px;height:280px;background:var(--yellow)"></i></div>
  <div class="ly l3" id="L3"><i style="left:470px;top:380px;width:210px;height:70px"></i></div>
</div></div>
<div class="lab" id="T0"><b>Surface</b>01 / background</div><div class="lab" id="T1"><b>Grid</b>02 / 12 columns</div><div class="lab" id="T2"><b>Content</b>03 / cards</div><div class="lab" id="T3"><b>Actions</b>04 / floating UI</div>
""",
js="""
const GAP = 120, Ls = [0, 1, 2, 3].map(i => $("#L" + i)), Ts = [0, 1, 2, 3].map(i => $("#T" + i)), NS = "http://www.w3.org/2000/svg";
const lines = Ts.map(() => { const l = document.createElementNS(NS, "line"); l.setAttribute("stroke", "#333"); l.setAttribute("stroke-width", 2); $("#lines").appendChild(l); return l; });
// project a point on a layer (x, y in layer px from its centre, z height) with the same rotateX(55) rotateZ(-40) as CSS
function iso(x, y, z) { const a = -40 * Math.PI / 180, b = 55 * Math.PI / 180; const x1 = x * Math.cos(a) - y * Math.sin(a), y1 = x * Math.sin(a) + y * Math.cos(a);
  const y2 = y1 * Math.cos(b) - z * Math.sin(b); return [760 + x1, 680 + y2]; }
function renderAt(t) {
  $("#iso").parentNode.style.opacity = E.out(seg(t, 0, 0.6));
  const col = E.inOut(seg(t, 4.2, 5.2));
  Ls.forEach((l, i) => { const k = E.back(seg(t, 0.8 + i * 0.12, 1.6 + i * 0.12)) * (1 - col); l.style.transform = `translateZ(${i * GAP * k}px)`;
    const [ax, ay] = iso(360, 0, i * GAP * k), lk = E.out(seg(t, 1.8 + i * 0.15, 2.3 + i * 0.15)) * (1 - E.out(seg(t, 4.0, 4.4)));
    const ty = ay - 40 + i * 14; Ts[i].style.top = `${ty - 20}px`; Ts[i].style.opacity = lk; Ts[i].style.transform = `translateX(${(1 - lk) * 30}px)`;
    const ln = lines[i]; ln.setAttribute("x1", ax); ln.setAttribute("y1", ay); ln.setAttribute("x2", lerp(ax, 1225, lk)); ln.setAttribute("y2", lerp(ay, ty + 20, lk)); ln.setAttribute("opacity", lk); });
}
"""),

# ---------------------------------------------------------------- radar-morph
dict(slug="radar-morph", title="Radar Morph", dur=6, bg="var(--ink)",
desc="A radar/spider chart with a sweeping scan line whose data polygon grows from the centre, then morphs from a 'before' profile to an 'after' profile with values updating. Use for skill profiles, product comparisons, competitive analysis, performance metrics, player stats, improvement over time and multi-axis data.",
look="A hexagonal web of concentric rings and six spokes with mono labels at each tip. A bright sweep line rotates once, and the data polygon grows from the centre behind it in translucent blue. Then it morphs to a larger, differently shaped accent polygon ('after'), vertex dots riding along, numbers at each tip counting to new values.",
beats=["0.0–0.8 s: web rings and spokes draw on.",
       "0.6–2.0 s: sweep line rotates 360°; 'before' polygon grows in its wake.",
       "2.6–3.8 s: morph before → after (in-out), colour blue → accent.",
       "Values at each axis count during the morph.",
       "4.0–6.0 s: hold; a faint 'before' outline remains for comparison."],
build="""
SVG. Axis `i` is at angle `-90° + i·60°`; a value `v ∈ [0,1]` maps to `(cos·R·v, sin·R·v)`. The polygon's points are recomputed each frame from `lerp(before_i, after_i, E.inOut(k))`. The grow-in multiplies by the sweep reveal: each vertex appears when the sweep angle passes its axis. Numbers use rounded `lerp` of the real values.
""",
knobs=["Axes (names, count) and the two datasets.",
       "Ring count and radius.",
       "Sweep on/off, colours.",
       "Keep or drop the 'before' ghost outline."],
pitfalls=["Use the same axis order for both datasets, or the morph twists.",
          "Radar charts exaggerate area; label actual values.",
          "Six to eight axes max; more turns into a circle."],
pairs=["donut-ring", "wave-dots", "count-up", "orbit-rings"],
css="""svg { position:absolute; inset:0; } .ax { font:700 24px var(--mono); fill:#bdb7ad; } .vl { font:400 34px var(--display); fill:#efe9df; }""",
html="""<svg viewBox="0 0 1920 1080"><g id="web" transform="translate(960 560)"></g></svg>""",
js="""
const AX = ["SPEED", "QUALITY", "COST", "SCALE", "CONTROL", "REACH"], B = [0.35, 0.5, 0.7, 0.3, 0.45, 0.4], A = [0.85, 0.9, 0.55, 0.8, 0.95, 0.75];
const R = 330, NS = "http://www.w3.org/2000/svg", web = $("#web"), mk = (tag, at) => { const e = document.createElementNS(NS, tag); for (const k in at) e.setAttribute(k, at[k]); web.appendChild(e); return e; };
const ang = i => (-90 + i * 60) * Math.PI / 180, P = (i, v) => [Math.cos(ang(i)) * R * v, Math.sin(ang(i)) * R * v];
const rings = [1, 2, 3, 4].map(r => mk("polygon", { fill: "none", stroke: "#3a3a3a", "stroke-width": 2, points: AX.map((_, i) => P(i, r / 4).join(",")).join(" ") }));
const spokes = AX.map((_, i) => mk("line", { x1: 0, y1: 0, x2: P(i, 1)[0], y2: P(i, 1)[1], stroke: "#3a3a3a", "stroke-width": 2 }));
const ghost = mk("polygon", { fill: "none", stroke: "#4f5bff", "stroke-width": 3, "stroke-dasharray": "8 8" });
const poly = mk("polygon", { "stroke-width": 5, "stroke-linejoin": "round" });
const sweep = mk("line", { x1: 0, y1: 0, stroke: "#efe9df", "stroke-width": 3 });
const dots = AX.map(() => mk("circle", { r: 9 }));
const labs = AX.map((n, i) => { const [x, y] = P(i, 1.22); return mk("text", { x, y: y + 8, class: "ax", "text-anchor": "middle" }); });
const vals = AX.map((n, i) => { const [x, y] = P(i, 1.22); return mk("text", { x, y: y + 46, class: "vl", "text-anchor": "middle" }); });
function renderAt(t) {
  const wk = E.out(seg(t, 0, 0.8)); rings.forEach(r => r.setAttribute("opacity", wk)); spokes.forEach(s => s.setAttribute("opacity", wk));
  const sw = seg(t, 0.6, 2.0), sa = -Math.PI / 2 + sw * Math.PI * 2, mk2 = E.inOut(seg(t, 2.6, 3.8));
  sweep.setAttribute("x2", Math.cos(sa) * R); sweep.setAttribute("y2", Math.sin(sa) * R); sweep.setAttribute("opacity", sw > 0 && sw < 1 ? 1 : 0);
  const pts = AX.map((_, i) => { const reveal = E.back(clamp((sw * 6 - i) / 1.2)); return P(i, lerp(B[i], A[i], mk2) * reveal); });
  poly.setAttribute("points", pts.map(p => p.join(",")).join(" "));
  const col = mix("#4f5bff", C.accent, mk2); poly.setAttribute("fill", col); poly.setAttribute("fill-opacity", 0.35); poly.setAttribute("stroke", col);
  dots.forEach((d, i) => { d.setAttribute("cx", pts[i][0]); d.setAttribute("cy", pts[i][1]); d.setAttribute("fill", col); });
  ghost.setAttribute("points", AX.map((_, i) => P(i, B[i]).join(",")).join(" ")); ghost.setAttribute("opacity", 0.8 * E.out(seg(t, 3.8, 4.4)));
  labs.forEach((l, i) => { l.textContent = AX[i]; l.setAttribute("opacity", wk); });
  vals.forEach((v, i) => { v.textContent = Math.round(lerp(B[i], A[i], mk2) * 100); v.setAttribute("opacity", clamp((sw * 6 - i) / 1.2)); });
}
"""),

# ---------------------------------------------------------------- cube-fold
dict(slug="cube-fold", title="Cube Fold", dur=6, bg="var(--paper)",
desc="A flat cube net (six squares in a cross) folds itself up into a 3D cube along its hinges, then the cube turns to show its faces. Use for packaging, 'it all comes together', product boxes, modular systems, origami/unboxing moments, assembling features into one product and playful 3D reveals.",
look="Six coloured squares lie flat in a cross shape, tilted toward the camera. The side flaps rotate up around their shared edges one after another, the last flap closing like a lid, forming a crisp cube. The finished cube then rotates a quarter turn on two axes so three faces show, each with a big glyph.",
beats=["0.0–0.6 s: flat net drops in.",
       "0.8–2.6 s: flaps fold, 0.25 s stagger (in-out), the lid last.",
       "2.8–4.6 s: cube tumbles to a three-quarter view.",
       "4.6–6.0 s: hold with a slow drift."],
build="""
Nested CSS 3D: the centre face is the root; four faces are its children positioned on each edge with `transform-origin` on the shared edge, folding with `rotateX/rotateY(±90°·k)`. The lid is a child of one side face, hinged on that face's far edge, so it rides along and folds last. Every element needs `transform-style: preserve-3d`. The tumble rotates the root container.
""",
knobs=["Face colours/content (logos, icons, photos).",
       "Fold order and stagger.",
       "Final view angles.",
       "Cube size."],
pitfalls=["Every face in the chain needs `preserve-3d`, or children flatten into their parent.",
          "Never reuse the id `root` inside a scene: it is the composition root's id in HyperFrames and in these examples.",
          "Fold all flaps toward the same side (same sign relative to their hinge) or the cube turns inside out.",
          "Don't put `filter` or `overflow:hidden` on any face: both flatten 3D.",
          "No borders on faces: children are positioned from the padding box, so a border shifts every hinge. Use an inset box-shadow for edges."],
pairs=["layer-explode", "cube-stack", "card-flip", "logo-land"],
css="""
.stage { position:absolute; inset:0; perspective:2600px; }
#cube { position:absolute; left:50%; top:50%; width:260px; height:260px; margin:-130px 0 0 -130px; transform-style:preserve-3d; }
.f { position:absolute; width:260px; height:260px; transform-style:preserve-3d; box-shadow:inset 0 0 0 3px rgba(0,0,0,.14);
  font:400 140px/260px var(--display); text-align:center; color:#fff; }
""",
html="""
<div class="stage"><div id="cube">
  <div class="f" id="F" style="left:0;top:0;background:var(--accent)">C
    <div class="f" id="Lf" style="left:-260px;top:0;background:var(--blue);transform-origin:100% 50%">O</div>
    <div class="f" id="Rf" style="left:260px;top:0;background:var(--yellow);color:#0e0e0e;transform-origin:0 50%">D</div>
    <div class="f" id="Tf" style="left:0;top:-260px;background:var(--pink);color:#0e0e0e;transform-origin:50% 100%">E</div>
    <div class="f" id="Bf" style="left:0;top:260px;background:var(--ink);transform-origin:50% 0">★
      <div class="f" id="Kf" style="left:0;top:260px;background:var(--lime);color:#0e0e0e;transform-origin:50% 0">!</div>
    </div>
  </div>
</div></div>
""",
js="""
function renderAt(t) {
  const drop = E.back(seg(t, 0, 0.6)), f = i => E.inOut(seg(t, 0.8 + i * 0.25, 1.5 + i * 0.25));
  $("#Lf").style.transform = `rotateY(${90 * f(0)}deg)`; $("#Rf").style.transform = `rotateY(${-90 * f(1)}deg)`;
  $("#Tf").style.transform = `rotateX(${-90 * f(2)}deg)`; $("#Bf").style.transform = `rotateX(${90 * f(3)}deg)`; $("#Kf").style.transform = `rotateX(${90 * f(4)}deg)`;
  const tb = E.inOut(seg(t, 2.8, 4.6)), drift = 4 * Math.sin(seg(t, 4.6, 6) * Math.PI);
  $("#cube").style.transform = `translateY(${(1 - drop) * -700}px) rotateX(${lerp(48, -28, tb)}deg) rotateY(${lerp(0, 38, tb) + drift}deg) rotateZ(${lerp(0, 0, tb)}deg) scale(${lerp(1, 1.15, tb)})`;
}
"""),

# ---------------------------------------------------------------- extrude-type
dict(slug="extrude-type", title="Extrude Type", dur=6, bg="var(--blue)",
desc="Bold 3D extruded lettering whose depth grows out of flat type, then swings so the extrusion sweeps around, with a bright front face and shaded sides. Use for retro and bold titles, logo-like wordmarks, game and music titles, punchy end cards, '3D type' showreel moments and loud announcements.",
look="A heavy word in paper-white sits flat. Its extrusion grows backward into a long, solid side in deep accent shades, as if pushed out of the screen. The light/camera then swings so the extrusion direction rotates from down-right to down-left, the side faces sliding around the letters. A hard drop shadow follows.",
beats=["0.0–0.6 s: flat word pops in (scale overshoot).",
       "0.6–1.8 s: extrusion depth grows 0 → 60 layers.",
       "2.0–4.4 s: extrusion angle swings from 35° to 145°.",
       "4.6–6.0 s: hold; front face gets a slow shine sweep."],
build="""
Canvas 'layer stack' extrusion: draw the word `n` times, offset 1.4 px further along the extrusion vector each time, from the back layer to the front, darkening as layers go back; then draw the front face on top. The extrusion vector `(cos a, sin a)` rotates over time. Cheap, crisp, no 3D engine. The shine is a gradient clipped to the front text (`globalCompositeOperation = 'source-atop'`).
""",
knobs=["Word, font, size.",
       "Depth (layers × step) and extrusion colours.",
       "Swing angles and timing.",
       "Shadow and shine."],
pitfalls=["Draw back-to-front; front-to-back hides the front face under the sides.",
          "60–100 layers is enough; more just costs time.",
          "Wait for the font before drawing or the extrusion bakes the fallback."],
pairs=["kinetic-type", "logo-land", "seal-spin", "count-up"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), WORD = "LOUD!", FS = 300, FONT = `400 ${FS}px 'Archivo Black', Arial Black, sans-serif`;
const shine = document.createElement("canvas"); shine.width = W; shine.height = H; const sg = shine.getContext("2d");
function renderAt(t) {
  g.clearRect(0, 0, W, H);
  const pop = E.back(seg(t, 0, 0.6)), depth = Math.round(60 * E.out(seg(t, 0.6, 1.8))), a = (35 + 110 * E.inOut(seg(t, 2.0, 4.4))) * Math.PI / 180, step = 1.6;
  const dx = Math.cos(a) * step, dy = Math.sin(a) * step;
  g.save(); g.translate(W / 2 - dx * depth / 2, H / 2 - dy * depth / 2); g.scale(pop, pop);
  g.font = FONT; g.textAlign = "center"; g.textBaseline = "middle";
  g.fillStyle = "rgba(0,0,0,.25)"; g.fillText(WORD, dx * (depth + 30), dy * (depth + 30));
  for (let i = depth; i >= 1; i--) { g.fillStyle = mix("#7a1a05", C.accent, 1 - i / Math.max(depth, 1) * 0.8); g.fillText(WORD, dx * i, dy * i); }
  g.fillStyle = C.paper; g.fillText(WORD, 0, 0);
  g.restore();
  const sk = seg(t, 4.6, 5.6); if (sk > 0 && sk < 1) {
    sg.clearRect(0, 0, W, H); sg.save(); sg.translate(W / 2 - dx * depth / 2, H / 2 - dy * depth / 2); sg.font = FONT; sg.textAlign = "center"; sg.textBaseline = "middle"; sg.fillStyle = "#fff"; sg.fillText(WORD, 0, 0); sg.restore();
    sg.globalCompositeOperation = "source-atop"; const x = lerp(-400, W + 400, sk), gr = sg.createLinearGradient(x - 160, 0, x + 160, 0);
    gr.addColorStop(0, "rgba(255,194,26,0)"); gr.addColorStop(0.5, "rgba(255,194,26,.9)"); gr.addColorStop(1, "rgba(255,194,26,0)"); sg.fillStyle = gr; sg.fillRect(0, 0, W, H);
    sg.globalCompositeOperation = "source-over"; g.drawImage(shine, 0, 0); }
}
"""),

# ---------------------------------------------------------------- logo-land
dict(slug="logo-land", title="Logo Land", dur=5, bg="var(--paper)",
desc="An end-card logo landing: the mark drops in with squash and stretch, hits with a shockwave ring and particle burst, then the wordmark letters pop in one by one and a tagline fades up. Use for end cards, brand sign-offs, intros, product logo reveals, CTAs and the final beat of promos and showreels.",
look="A bold round mark falls from above, stretched tall while falling, squashes wide on impact, rebounds and settles. A thin accent ring shoots out from the impact and a dozen small particles spray outward. Wordmark letters rise in a quick stagger beside it; a mono tagline and URL fade in last.",
beats=["0.2–0.7 s: mark falls (ease-in), stretched 0.8×1.25.",
       "0.7 s: impact: squash 1.3×0.7, shockwave ring and particles start.",
       "0.7–1.3 s: rebound and settle (elastic).",
       "1.1–1.7 s: wordmark letters pop in, 0.05 s apart (back ease).",
       "1.9–2.5 s: tagline fades up; hold to the end."],
build="""
The fall is `y = lerp(-700, 0, E.in(k))`; while falling, scaleY 1.25 and scaleX 0.8 (stretch along the motion). At impact, a short squash curve (`sin` over 0.12 s) then `E.elastic` back to 1. The ring is a circle scaling 0 → 4 with fading opacity; particles are seeded angles moving out with `E.out`, falling slightly with gravity. Letters are spans with per-letter delays.
""",
knobs=["Mark (swap the SVG for your logo) and wordmark text.",
       "Fall height and impact time; squash amount.",
       "Ring and particle colours/count.",
       "Tagline and URL."],
pitfalls=["Squash and stretch must preserve area (scaleX ≈ 1/scaleY) or it looks rubbery.",
          "Transform origin at the bottom of the mark so it squashes onto the ground.",
          "Don't over-bounce a logo: one rebound is premium, three is cartoon."],
pairs=["seal-spin", "pixel-build", "shape-morph", "extrude-type"],
css="""
#mark { position:absolute; left:560px; top:330px; width:300px; height:300px; transform-origin:50% 100%; }
#ring { position:absolute; left:710px; top:630px; width:120px; height:40px; margin:-20px 0 0 -60px; border-radius:50%; border:6px solid var(--accent); }
#word { position:absolute; left:930px; top:375px; font-size:190px; letter-spacing:-7px; line-height:1; display:flex; overflow:hidden; padding-bottom:12px; }
#word span { display:inline-block; }
#tag { position:absolute; left:940px; top:600px; font:700 30px var(--mono); letter-spacing:3px; color:#6f6a61; }
canvas { z-index:1; }
""",
html="""
<canvas id="cv"></canvas><div id="ring"></div>
<svg id="mark" viewBox="0 0 300 300"><circle cx="150" cy="150" r="146" fill="#ff4a1c"/><path d="M95 95 h110 v40 h-70 v30 h55 v38 h-55 v62 h-40z" fill="#efe9df"/></svg>
<div id="word"></div><div id="tag">MOTION, WRITTEN IN CODE — FRAMEWORK.STUDIO</div>
""",
js="""
const g = ctx2d("cv"), WORD = "Frame.", r0 = rng(12), parts = Array.from({ length: 14 }, () => ({ a: -Math.PI * (0.05 + r0() * 0.9), v: 260 + r0() * 260, s: 5 + r0() * 7 }));
[...WORD].forEach(ch => { const s = document.createElement("span"); s.textContent = ch; if (ch === ".") s.style.color = C.accent; $("#word").appendChild(s); });
const letters = $$("#word span"), HIT = 0.7;
function renderAt(t) {
  const k = seg(t, 0.2, HIT), y = lerp(-760, 0, E.in(k));
  let sx = 1, sy = 1;
  if (t < HIT) { sx = lerp(1, 0.8, k); sy = lerp(1, 1.25, k); }
  else { const q = seg(t, HIT, HIT + 0.12); const sq = Math.sin(q * Math.PI);
    const el = E.elastic(seg(t, HIT + 0.06, HIT + 0.7)); sy = q < 1 ? lerp(1, 0.7, sq) : lerp(0.85, 1, el); sx = 1 / sy; }
  $("#mark").style.transform = `translateY(${y}px) scale(${sx}, ${sy})`; $("#mark").style.opacity = t >= 0.2 ? 1 : 0;
  const rk = seg(t, HIT, HIT + 0.7); $("#ring").style.transform = `scale(${1 + 5 * E.out(rk)})`; $("#ring").style.opacity = rk > 0 && rk < 1 ? 1 - rk : 0;
  g.clearRect(0, 0, W, H);
  const pk = seg(t, HIT, HIT + 0.9);
  if (pk > 0 && pk < 1) parts.forEach(p => { const d = p.v * E.out(pk), x = 710 + Math.cos(p.a) * d, yy = 630 + Math.sin(p.a) * d + 260 * pk * pk;
    g.fillStyle = C.accent; g.globalAlpha = 1 - pk; g.beginPath(); g.arc(x, yy, p.s * (1 - pk * 0.5), 0, 7); g.fill(); });
  g.globalAlpha = 1;
  letters.forEach((l, i) => { const lk = E.back(seg(t, 1.1 + i * 0.05, 1.5 + i * 0.05)); l.style.transform = `translateY(${(1 - lk) * 110}%)`; });
  const tk = E.out(seg(t, 1.9, 2.5)); $("#tag").style.opacity = tk; $("#tag").style.transform = `translateY(${(1 - tk) * 20}px)`;
}
"""),
]
