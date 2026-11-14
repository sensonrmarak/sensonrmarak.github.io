RECIPES = [
# ---------------------------------------------------------------- shape-morph
dict(slug="shape-morph", title="Shape Morph", dur=6, bg="var(--paper)",
desc="A single solid shape that morphs smoothly circle → triangle → square → star, rotating and changing colour at each stage. Use for 'transform/adapt' metaphors, logo builds, chapter transitions, Bauhaus/geometric motion, loading states and showreel 'morph' moments.",
look="One flat shape centre frame. It holds briefly as a circle, then flows into a triangle, a square and finally a five-point star, each transition with an in-out ease and a quarter turn of rotation. The fill steps through accent, blue, yellow and ink on each arrival, and a thin outline echo trails one beat behind.",
beats=["0.0–0.6 s: circle scales up from 0 (back ease).",
       "1.0–1.8 s: circle → triangle (fill to blue).",
       "2.3–3.1 s: triangle → square (fill to yellow).",
       "3.6–4.4 s: square → star (fill to accent).",
       "4.4–6.0 s: star holds and slowly spins; outline echo catches up."],
build="""
Every shape is resampled to the same number of points (`N = 180`) evenly spaced along its perimeter, starting at the top. Morphing is then just `lerp` between matching points. A polygon with `k` vertices (and an inner radius for stars) is sampled by walking its edges by arc length; the circle is sampled by angle. The echo is the same morph evaluated at `t - 0.25`, stroked instead of filled.
""",
knobs=["Shape sequence (any polygon/star; add custom paths by resampling them).",
       "Point count N (more = smoother curves).",
       "Rotation per stage; colours.",
       "Echo delay or off."],
pitfalls=["Start every shape's sampling at the same angle (top) or the morph twists inside out.",
          "Equal point spacing by arc length, not by vertex index, or corners bunch up.",
          "Hold each shape long enough (≥0.4 s) to be recognised."],
pairs=["liquid-blob", "logo-land", "seal-spin", "swiss-grid"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), N = 180;
function poly(k, rIn = 1, rot0 = -Math.PI / 2) { const vs = [];
  for (let i = 0; i < k * (rIn < 1 ? 2 : 1); i++) { const r = rIn < 1 && i % 2 ? rIn : 1, a = rot0 + i * Math.PI * 2 / (k * (rIn < 1 ? 2 : 1)); vs.push([Math.cos(a) * r, Math.sin(a) * r]); }
  const segL = vs.map((v, i) => Math.hypot(vs[(i + 1) % vs.length][0] - v[0], vs[(i + 1) % vs.length][1] - v[1])), tot = segL.reduce((a, b) => a + b, 0), out = [];
  for (let n = 0; n < N; n++) { let d = n / N * tot, i = 0; while (d > segL[i]) { d -= segL[i]; i++; }
    const a = vs[i], b = vs[(i + 1) % vs.length], u = d / segL[i]; out.push([lerp(a[0], b[0], u), lerp(a[1], b[1], u)]); }
  return out; }
const circle = Array.from({ length: N }, (_, n) => { const a = -Math.PI / 2 + n / N * Math.PI * 2; return [Math.cos(a), Math.sin(a)]; });
const shapes = [circle, poly(3), poly(4, 1, -Math.PI / 2), poly(5, 0.45)], cols = [C.ink, C.blue, C.yellow, C.accent];
const T = [[1.0, 1.8], [2.3, 3.1], [3.6, 4.4]];
function stateAt(t) { let pts = shapes[0], col = cols[0], rot = 0;
  T.forEach(([a, b], i) => { const k = E.inOut(seg(t, a, b)); if (k > 0) { pts = pts.map((p, j) => [lerp(p[0], shapes[i + 1][j][0], k), lerp(p[1], shapes[i + 1][j][1], k)]);
    col = mix(cols[i], cols[i + 1], k); rot += k * Math.PI / 2; } });
  return { pts, col, rot: rot + Math.max(0, t - 4.4) * 0.4 }; }
function draw(st, sc, fill) { g.save(); g.translate(W / 2, H / 2); g.rotate(st.rot); g.beginPath();
  st.pts.forEach((p, i) => i ? g.lineTo(p[0] * sc, p[1] * sc) : g.moveTo(p[0] * sc, p[1] * sc)); g.closePath();
  if (fill) { g.fillStyle = st.col; g.fill(); } else { g.strokeStyle = st.col; g.lineWidth = 4; g.stroke(); } g.restore(); }
function renderAt(t) {
  g.clearRect(0, 0, W, H);
  const sc = 330 * E.back(seg(t, 0, 0.6));
  if (t > 0.9) draw(stateAt(t - 0.25), sc * 1.12, false);
  draw(stateAt(t), sc, true);
}
"""),

# ---------------------------------------------------------------- card-flip
dict(slug="card-flip", title="Card Flip", dur=6, bg="var(--ink)",
desc="A row of cards that flip over in 3D one after another, lifting toward the camera mid-flip, to reveal answers, stats or the new version on the back. Use for reveals, quiz answers, myths vs facts, old vs new, features, flashcards and 'turn the card' storytelling.",
look="Three tall cards face-down with a question or 'before' label. One by one they flip around the vertical axis: lifting (scale 1.08) and casting a bigger shadow at 90°, then settling with a small overshoot on the back face, which is a saturated colour with a big number.",
beats=["0.0–0.6 s: cards slide up into place.",
       "1.0–1.9 s: card 1 flips (back ease); 1.6–2.5 s card 2; 2.2–3.1 s card 3.",
       "3.4–6.0 s: hold; a subtle 2° parallax tilt follows a slow sine."],
build="""
Each card has `transform-style: preserve-3d` with two faces; the back face starts at `rotateY(180deg)` and both faces use `backface-visibility: hidden`. The card's `rotateY = 180·E.back(k)`. Lift is `1 + 0.08·sin(π·k)`, so it's highest exactly edge-on, which hides the moment the faces swap. The shadow grows with the same curve.
""",
knobs=["Card count, size and gap.",
       "Flip axis (Y for left-right, X for top-bottom).",
       "Stagger and overshoot strength.",
       "Front/back content."],
pitfalls=["The back face must be pre-rotated 180° or its content renders mirrored.",
          "Never put `filter` or `opacity < 1` on the 3D card itself: both flatten `preserve-3d` and the back face never shows. Shadow the faces instead.",
          "Perspective on the parent, not each card, so all cards share a vanishing point.",
          "Overshoot past 180° briefly shows the front edge; keep it small (back ease 1.2–1.7)."],
pairs=["card-fan", "count-up", "before-after", "swiss-grid"],
css="""
.row { position:absolute; inset:0; perspective:2000px; display:flex; justify-content:center; align-items:center; gap:60px; }
.card { position:relative; width:440px; height:620px; transform-style:preserve-3d; }
.f { position:absolute; inset:0; border-radius:30px; backface-visibility:hidden; padding:40px; box-sizing:border-box; }
.front { background:#262626; color:#bdb7ad; font:700 30px var(--mono); }
.front b { display:block; margin-top:300px; font:400 64px var(--display); color:#f1ece3; letter-spacing:-2px; line-height:1; }
.back { transform:rotateY(180deg); font:700 28px var(--mono); }
.back b { display:block; margin-top:250px; font:400 150px var(--display); letter-spacing:-6px; line-height:1; }
""",
html="""
<div class="row">
  <div class="card" id="c0"><div class="f front">01<b>Render time?</b></div><div class="f back" style="background:var(--accent);color:#fff">RENDER<b>12s</b></div></div>
  <div class="card" id="c1"><div class="f front">02<b>Frame rate?</b></div><div class="f back" style="background:var(--yellow)">FPS<b>60</b></div></div>
  <div class="card" id="c2"><div class="f front">03<b>Lines of code?</b></div><div class="f back" style="background:var(--blue);color:#fff">LOC<b>240</b></div></div>
</div>
""",
js="""
const cards = [$("#c0"), $("#c1"), $("#c2")];
function renderAt(t) {
  cards.forEach((c, i) => {
    const up = E.out(seg(t, i * 0.1, 0.6 + i * 0.1)), k = seg(t, 1.0 + i * 0.6, 1.9 + i * 0.6);
    const ry = 180 * E.back(k), lift = 1 + 0.08 * Math.sin(Math.PI * k), tilt = 2 * Math.sin(t * 1.2 + i) * seg(t, 3.4, 4);
    c.style.transform = `translateY(${(1 - up) * 700}px) rotateY(${ry + tilt}deg) scale(${lift})`;
    const sh = Math.sin(Math.PI * k);  // box-shadow on faces: a filter on the card would flatten its 3D
    c.querySelectorAll(".f").forEach(f => f.style.boxShadow = `0 ${20 + 50 * sh}px ${30 + 40 * sh}px rgba(0,0,0,.5)`);
  });
}
"""),

# ---------------------------------------------------------------- donut-ring
dict(slug="donut-ring", title="Donut Ring", dur=6, bg="var(--paper)",
desc="An animated donut chart whose segments sweep in one after another with gaps and rounded ends, a centre number counting up and a legend that ticks in. Use for market share, budgets, survey results, time splits, portfolio allocation, percentages and any part-of-a-whole data.",
look="A thick ring on paper. Segments draw clockwise from 12 o'clock one at a time, each in its own colour with a small gap between them. The centre shows the hero percentage counting up from 0; legend rows slide in beside the ring as each segment lands.",
beats=["0.0–0.6 s: faint track ring fades in.",
       "0.6–3.2 s: segments sweep in sequence (each ~0.7 s, overlapping 0.15 s).",
       "0.6–3.0 s: centre number counts up to the hero value.",
       "Each segment's legend row slides in when its sweep ends.",
       "3.6–4.2 s: hero segment pops outward 14 px; hold."],
build="""
SVG circles with `stroke-dasharray = "len gap"` where `len = value·C` (C = circumference). Rotation offsets each segment to start where the previous ended (`rotate(start·360 - 90)`). To sweep, scale `len` by `E.inOut(k)`. The hero pop is a translate along the segment's mid-angle. Numbers use `Math.round(lerp(0, v, E.out(k)))` with tabular figures so they don't jitter.
""",
knobs=["Data (values sum to 1), colours, labels.",
       "Ring radius, thickness and gap size.",
       "Sweep order and speed.",
       "Hero segment and centre label."],
pitfalls=["Account for the gap in each segment's length or segments overlap at the ends.",
          "Round linecaps extend past the dash; subtract stroke-width from each length.",
          "Use `font-variant-numeric: tabular-nums` for counting numbers."],
pairs=["count-up", "bars-3d", "radar-morph", "swiss-grid"],
css="""
svg { position:absolute; left:220px; top:140px; width:800px; height:800px; }
#num { position:absolute; left:220px; top:440px; width:800px; text-align:center; font-size:150px; letter-spacing:-5px; font-variant-numeric:tabular-nums; }
#cap { position:absolute; left:220px; top:620px; width:800px; text-align:center; font:700 26px var(--mono); }
.lg { position:absolute; left:1160px; font:700 34px var(--mono); display:flex; align-items:center; gap:24px; }
.lg i { width:34px; height:34px; border-radius:50%; display:inline-block; }
.lg b { font:400 64px var(--display); width:180px; letter-spacing:-2px; }
""",
html="""
<svg viewBox="-400 -400 800 800"><circle r="300" fill="none" stroke="#ddd6ca" stroke-width="90" id="track"/><g id="segs"></g></svg>
<div id="num">0%</div><div id="cap">MOBILE SHARE</div>
<div id="legend"></div>
""",
js="""
const data = [[0.46, C.accent, "Mobile"], [0.27, C.blue, "Desktop"], [0.17, C.yellow, "Tablet"], [0.10, C.ink, "Other"]];
const R = 300, CIRC = 2 * Math.PI * R, GAP = 26, SW = 90, segs = [], legs = [];
let acc = 0;
data.forEach(([v, col, name], i) => { const c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  c.setAttribute("r", R); c.setAttribute("fill", "none"); c.setAttribute("stroke", col); c.setAttribute("stroke-width", SW); c.setAttribute("stroke-linecap", "butt");
  $("#segs").appendChild(c); segs.push({ c, v, start: acc }); acc += v;
  const l = document.createElement("div"); l.className = "lg"; l.style.top = `${330 + i * 110}px`;
  l.innerHTML = `<i style="background:${col}"></i><b>${Math.round(v * 100)}%</b>${name}`; $("#legend").appendChild(l); legs.push(l); });
function renderAt(t) {
  $("#track").style.opacity = E.out(seg(t, 0, 0.6));
  segs.forEach((s, i) => { const a = 0.6 + i * 0.55, k = E.inOut(seg(t, a, a + 0.7));
    const len = Math.max(0, s.v * CIRC - GAP) * k;
    s.c.setAttribute("stroke-dasharray", `${len} ${CIRC}`);
    const mid = (s.start + s.v / 2) * 2 * Math.PI - Math.PI / 2, pop = i === 0 ? 14 * E.back(seg(t, 3.6, 4.2)) : 0;
    s.c.setAttribute("transform", `translate(${Math.cos(mid) * pop} ${Math.sin(mid) * pop}) rotate(${s.start * 360 - 90 + (GAP / CIRC) * 180})`);
    const lk = E.out(seg(t, a + 0.5, a + 0.9)); legs[i].style.opacity = lk; legs[i].style.transform = `translateX(${(1 - lk) * 40}px)`; });
  $("#num").textContent = Math.round(46 * E.out(seg(t, 0.6, 3.0))) + "%";
}
"""),

# ---------------------------------------------------------------- swiss-grid
dict(slug="swiss-grid", title="Swiss Grid", dur=6, bg="var(--paper)",
desc="International Typographic Style layout in motion: a 12-column grid draws on, then blocks, a huge number, a red circle and text columns snap into the grid on hard beats. Use for editorial and design-forward scenes, chapter cards, data headlines, portfolio intros, poster-style title cards and timeline sections.",
look="Hairline grid lines rule across the frame, then elements land on the grid with hard, confident moves: a giant numeral, a red disc, a black bar, flush-left text columns and small metadata in mono. Strict alignment, asymmetric composition, lots of white space.",
beats=["0.0–0.8 s: vertical then horizontal grid lines draw (stagger 30 ms).",
       "0.9 s: giant '26' slides in from the left edge (expo).",
       "1.3 s: red circle scales in on its grid cell (back).",
       "1.6 s: black bar wipes across 6 columns.",
       "2.0–2.6 s: three text blocks rise in, column by column.",
       "4.6–5.2 s: grid lines fade to 40 %, layout holds."],
build="""
Positions come from a grid helper: `col(n) = margin + n·(colW + gutter)`, rows likewise, so every element snaps. Lines are divs whose `scaleX/scaleY` animate from 0 with origin at their start. Elements use `translate` from off-grid positions with expo/back eases, timed to land on beats (0.9, 1.3, 1.6, 2.0 s), not spread evenly.
""",
knobs=["Columns (12), margins and gutters.",
       "Element list, grid spans and land times (align to music beats).",
       "Accent colour (classic red #e3001b or the palette accent).",
       "Line weight and final opacity."],
pitfalls=["Everything must snap to the grid; one off-grid element breaks the style.",
          "Don't centre things; Swiss style is flush-left and asymmetric.",
          "Avoid soft fades for the main elements: hard moves and cuts."],
pairs=["kinetic-type", "count-up", "donut-ring", "blueprint-draw"],
css="""
.gl { position:absolute; background:rgba(14,14,14,.18); }
#big { position:absolute; font-size:560px; letter-spacing:-30px; line-height:.8; }
#disc { position:absolute; border-radius:50%; background:#e3001b; }
#bar { position:absolute; background:var(--ink); transform-origin:0 50%; }
.tx { position:absolute; font:600 24px/1.35 var(--mono); }
.tx b { display:block; font:400 40px/1 var(--display); margin-bottom:14px; letter-spacing:-1px; }
""",
html="""
<div id="lines"></div>
<div id="big">26</div><div id="disc"></div><div id="bar"></div>
<div class="tx" id="t0"><b>Form</b>Every element sits on the grid. Nothing floats.</div>
<div class="tx" id="t1"><b>Order</b>Flush left, ragged right, generous space.</div>
<div class="tx" id="t2"><b>Rhythm</b>Moves land on the beat, never between.</div>
""",
js="""
const M = 80, G = 24, COLS = 12, cw = (W - 2 * M - G * (COLS - 1)) / COLS, RH = (H - 2 * M) / 8;
const col = n => M + n * (cw + G), row = n => M + n * RH, lines = [];
for (let i = 0; i <= COLS; i++) { const d = document.createElement("div"); d.className = "gl"; Object.assign(d.style, { left: `${i < COLS ? col(i) : W - M}px`, top: `${M}px`, width: "1px", height: `${H - 2 * M}px`, transformOrigin: "50% 0" }); $("#lines").appendChild(d); lines.push([d, "Y", i]); }
for (let j = 0; j <= 8; j++) { const d = document.createElement("div"); d.className = "gl"; Object.assign(d.style, { left: `${M}px`, top: `${row(j)}px`, height: "1px", width: `${W - 2 * M}px`, transformOrigin: "0 50%" }); $("#lines").appendChild(d); lines.push([d, "X", j + COLS]); }
Object.assign($("#big").style, { left: `${col(0) - 20}px`, top: `${row(1)}px` });
const dsz = 3 * cw + 2 * G; Object.assign($("#disc").style, { left: `${col(8)}px`, top: `${row(1)}px`, width: `${dsz}px`, height: `${dsz}px` });
Object.assign($("#bar").style, { left: `${col(0)}px`, top: `${row(6)}px`, width: `${col(6) - col(0) - G}px`, height: "28px" });
[0, 1, 2].forEach(i => Object.assign($("#t" + i).style, { left: `${col(6 + i * 2)}px`, top: `${row(6) - 10}px`, width: `${2 * cw + G - 10}px` }));
function renderAt(t) {
  const fadeL = lerp(1, 0.4, E.inOut(seg(t, 4.6, 5.2)));
  lines.forEach(([d, ax, i]) => { const k = E.inOut(seg(t, i * 0.03, i * 0.03 + 0.5)); d.style.transform = `scale${ax}(${k})`; d.style.opacity = fadeL; });
  const bk = E.expo(seg(t, 0.9, 1.5)); $("#big").style.transform = `translateX(${(1 - bk) * -900}px)`;
  $("#disc").style.transform = `scale(${E.back(seg(t, 1.3, 1.8))})`;
  $("#bar").style.transform = `scaleX(${E.expo(seg(t, 1.6, 2.1))})`;
  [0, 1, 2].forEach(i => { const k = E.expo(seg(t, 2.0 + i * 0.15, 2.6 + i * 0.15)); const e = $("#t" + i);
    e.style.transform = `translateY(${(1 - k) * 60}px)`; e.style.opacity = k > 0 ? 1 : 0; e.style.clipPath = `inset(0 0 ${(1 - k) * 100}% 0)`; });
}
"""),

# ---------------------------------------------------------------- helix
dict(slug="helix", title="Helix", dur=6, bg="var(--ink)",
desc="A rotating DNA-style double helix of glowing dots joined by rungs, depth-shaded and drawn in 3D on canvas. Use for biotech, health, genetics, 'in our DNA' brand values, science explainers, growth/evolution metaphors and elegant looping tech backgrounds.",
look="Two strands of dots spiral around a horizontal axis, joined by thin rungs. The helix rotates continuously; near dots are large and bright (one strand accent, one blue), far dots small and dim. It builds from left to right at the start and the rungs flash white one by one like a scan.",
beats=["0.0–1.6 s: helix builds left to right (dots and rungs appear by x).",
       "Continuous: rotation 1.4 rad/s around the long axis.",
       "2.0–4.0 s: a white scan pulse runs along the rungs.",
       "4.0–6.0 s: camera tilts 15° so the helix angles into depth."],
build="""
For `i` in `0..N`, position along the axis `x = (i/N - 0.5)·L`, angle `a = i·0.32 + t·1.4`; strand A at `(x, R·cos a, R·sin a)`, strand B offset by π. Rotate the whole thing with a slow tilt via `rot()`, project with `proj()`. Sort all dots and rungs by depth (back to front) each frame (a few hundred items) and size/alpha them by projected scale `k`.
""",
knobs=["Turns (angle step 0.32), radius R and length L.",
       "Dot count; strand colours.",
       "Scan pulse colour/speed.",
       "Tilt (flat side view vs. into-depth)."],
pitfalls=["Depth sort every frame; rotating helices change order constantly.",
          "Rungs drawn after both dots will cover the near dot; draw rung at its mid-depth.",
          "Too many turns looks like a spring, not DNA: about 4–6 turns across the frame."],
pairs=["particle-sphere", "torus-wire", "orbit-rings", "wave-dots"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), N = 72, L = 1500, R = 170;
function renderAt(t) {
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  const tilt = 0.14 * E.inOut(seg(t, 4, 6)), build = seg(t, 0, 1.6), items = [];
  for (let i = 0; i < N; i++) { const u = i / (N - 1); if (u > build * 1.0001) break;
    const x = (u - 0.5) * L, a = i * 0.27 + t * 1.4;
    const A = proj(rot([x, R * Math.cos(a), R * Math.sin(a)], 0, tilt), 1500), B = proj(rot([x, -R * Math.cos(a), -R * Math.sin(a)], 0, tilt), 1500);
    const scan = Math.exp(-(((u - seg(t, 2, 4) * 1.2 + 0.1) / 0.04) ** 2));
    if (i % 2 === 0 || scan > 0.05) items.push({ z: (A[2] + B[2]) / 2, f: () => { g.strokeStyle = `rgba(${scan > 0.05 ? "255,255,255" : "239,233,223"},${0.15 + 0.7 * scan})`; g.lineWidth = 2 + 3 * scan; g.beginPath(); g.moveTo(A[0], A[1]); g.lineTo(B[0], B[1]); g.stroke(); } });
    items.push({ z: A[2], f: () => { g.fillStyle = C.accent; g.globalAlpha = clamp((A[2] - 0.75) / 0.5, 0.2, 1); g.beginPath(); g.arc(A[0], A[1], 11 * A[2] ** 2, 0, 7); g.fill(); g.globalAlpha = 1; } });
    items.push({ z: B[2], f: () => { g.fillStyle = "#4f5bff"; g.globalAlpha = clamp((B[2] - 0.75) / 0.5, 0.2, 1); g.beginPath(); g.arc(B[0], B[1], 11 * B[2] ** 2, 0, 7); g.fill(); g.globalAlpha = 1; } }); }
  items.sort((a, b) => a.z - b.z).forEach(it => it.f());
}
"""),

# ---------------------------------------------------------------- notifications
dict(slug="notifications", title="Notifications", dur=6, bg="var(--pink)",
desc="Phone-style notification banners drop in one after another with a spring, stacking and pushing older ones down and back, with app icons and a growing badge count. Use for social proof, 'your phone is blowing up', sales/order alerts, reminders, engagement and app-growth moments.",
look="Rounded frosted banners slide down from the top centre with a springy overshoot. Each new one lands on top; older banners shift down, shrink slightly and fade, forming a neat 3D stack. A red badge in the corner counts the notifications.",
beats=["0.4 s, 1.0 s, 1.5 s, 1.9 s, 2.25 s, 2.55 s: notifications arrive, accelerating like a pile-up.",
       "Each arrival: 0.5 s spring from −160 px; previous stack steps down.",
       "3.0–6.0 s: hold; the top banner gets a subtle highlight pulse at 3.4 s."],
build="""
Banner `i` arrives at `T[i]`. For a time `t`, count arrivals `n` so far; banner `i`'s depth in the stack is `n-1-i`. Its target y, scale and opacity are functions of depth (`y = depth·26`, `scale = 1 - depth·0.05`, `opacity = 1 - depth·0.18`). Transitions between depths are eased using the time since the latest arrival, so the stack 'steps' on each new banner. The badge number is just `n`.
""",
knobs=["Notification list (icon colour, app name, text) and arrival times.",
       "Stack depth visible (4) and step spacing.",
       "Spring strength (elastic vs. back ease).",
       "Badge on/off."],
pitfalls=["Accelerating arrival times sell 'blowing up'; even spacing feels like a slideshow.",
          "Keep text short: two lines per banner max.",
          "Use made-up app names unless you have rights to real logos."],
pairs=["phone-orbit", "chat-thread", "count-up", "phone-scroll"],
css="""
.stack { position:absolute; left:50%; top:200px; width:900px; margin-left:-450px; }
.n { position:absolute; left:0; top:0; width:900px; height:150px; border-radius:36px; background:rgba(255,255,255,.88);
  box-shadow:0 20px 50px rgba(0,0,0,.15); display:flex; align-items:center; gap:28px; padding:0 34px; box-sizing:border-box; transform-origin:50% 0; }
.n i { width:84px; height:84px; border-radius:22px; flex:none; }
.n div { font:600 26px/1.3 var(--mono); color:#333; } .n b { display:block; font:700 30px var(--mono); color:#111; }
#badge { position:absolute; left:1320px; top:150px; min-width:80px; height:80px; border-radius:40px; background:#ff2d2d; color:#fff;
  font:700 44px/80px var(--mono); text-align:center; padding:0 18px; box-sizing:border-box; z-index:20; }
#title { position:absolute; left:0; right:0; top:700px; text-align:center; font-size:110px; letter-spacing:-4px; }
""",
html="""
<div class="stack" id="stack"></div><div id="badge">0</div><div id="title">They noticed.</div>
""",
js="""
const notes = [[C.blue, "Orders", "New order #2041 — $129"], [C.accent, "Studio", "Mia liked your reel"], [C.yellow, "Mail", "Re: partnership next week?"],
  [C.ink, "Bank", "Payment received: $3,400"], [C.lime, "Shop", "You sold out in 12 minutes"], ["#8b5cf6", "Social", "+1,204 new followers"]];
const T = [0.4, 1.0, 1.5, 1.9, 2.25, 2.55], els = [];
notes.forEach(([c, app, txt]) => { const d = document.createElement("div"); d.className = "n";
  d.innerHTML = `<i style="background:${c}"></i><div><b>${app}</b>${txt}</div>`; $("#stack").appendChild(d); els.push(d); });
function renderAt(t) {
  const n = T.filter(x => t >= x).length;
  els.forEach((el, i) => {
    if (t < T[i]) { el.style.opacity = 0; return; }
    const kin = E.back(seg(t, T[i], T[i] + 0.5));
    const depthNow = n - 1 - i, since = n ? t - T[n - 1] : 0, step = E.out(clamp(since / 0.35));
    const depth = depthNow > 0 ? lerp(depthNow - 1, depthNow, step) : 0;
    const y = (1 - kin) * -220 + depth * 28, s = 1 - depth * 0.05, op = depth > 3.5 ? 0 : 1 - depth * 0.2;
    el.style.transform = `translateY(${y}px) scale(${s})`; el.style.opacity = clamp(op) * clamp(kin * 3); el.style.zIndex = 10 - depthNow;
    el.style.background = i === n - 1 && t > 3.4 ? `rgba(255,255,255,${0.88 + 0.12 * Math.sin(seg(t, 3.4, 4.0) * Math.PI)})` : "rgba(255,255,255,.88)"; });
  const b = $("#badge"); b.textContent = n; b.style.transform = `scale(${n ? 1 + 0.25 * (1 - E.out(clamp((t - T[n - 1]) / 0.25))) : 0})`;
  const tk = E.expo(seg(t, 3.0, 3.6)); $("#title").style.opacity = tk; $("#title").style.transform = `translateY(${(1 - tk) * 50}px)`;
}
"""),

# ---------------------------------------------------------------- marquee-brands
dict(slug="marquee-brands", title="Marquee Brands", dur=6, bg="var(--paper)",
desc="Rows of logo wordmarks scrolling endlessly in opposite directions with soft edge fades, a seamless 'trusted by' strip. Use for client logos, partners, integrations, press mentions, sponsors, tech stacks and social-proof sections of promos and showreels.",
look="Three rows of wordmarks in mixed type styles (bold sans, serif italic, mono, rounded) glide horizontally: top and bottom rows left, middle row right, at slightly different speeds. The edges fade to the background so logos appear and disappear softly. A small 'TRUSTED BY' label sits above.",
beats=["0.0–0.6 s: rows fade/slide in from slight offsets.",
       "Continuous: rows scroll at 120, 90 and 150 px/s; loops seamlessly.",
       "3.0 s: middle row's centre logo turns accent for emphasis (optional)."],
build="""
Each row contains its logo list twice in a flex track. Offset `x = -((t·speed) mod trackWidth)`, where `trackWidth` is the width of one copy (measured once after fonts load). Because the second copy follows the first exactly, the wrap is invisible. Edge fades are a `mask-image: linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent)` on the row.
""",
knobs=["Logo list per row (use SVG logos you have rights to, or wordmarks).",
       "Speeds and directions.",
       "Gap between logos; row count.",
       "Fade width."],
pitfalls=["Measure one copy's width after fonts load or the loop jumps.",
          "Use real client logos only with permission; placeholders here are invented names.",
          "Keep logos visually equal in weight; one huge logo breaks the strip."],
pairs=["type-ring", "count-up", "notifications", "swiss-grid"],
css="""
#lab { position:absolute; left:0; right:0; top:170px; text-align:center; font:700 26px var(--mono); letter-spacing:6px; color:#7b766e; }
.row { position:absolute; left:0; width:100%; overflow:hidden; -webkit-mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent); mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent); }
.tr { display:flex; gap:110px; white-space:nowrap; width:max-content; padding-right:110px; }
.lg { font-size:76px; color:#2a2a2a; letter-spacing:-2px; }
.s1 { font-family:var(--serif); font-style:italic; letter-spacing:0; } .s2 { font:700 64px var(--mono); letter-spacing:-3px; }
""",
html="""<div id="lab">TRUSTED BY TEAMS AT</div><div id="rows"></div>""",
js="""
const LOGOS = [["Northwind", ""], ["Halcyon", "s1"], ["QUBIT", "s2"], ["Lumen&Co", ""], ["Parallax", "s1"], ["orbit.io", "s2"], ["Fieldnote", ""], ["Marlowe", "s1"], ["KITE", "s2"]];
const rows = [{ y: 300, sp: 120, dir: -1, off: 0 }, { y: 470, sp: 90, dir: 1, off: 3 }, { y: 640, sp: 150, dir: -1, off: 6 }];
rows.forEach(r => { const row = document.createElement("div"); row.className = "row"; row.style.top = `${r.y}px`;
  const list = LOGOS.map((_, i) => LOGOS[(i + r.off) % LOGOS.length]);
  const one = list.map(([n, c]) => `<span class="lg ${c}">${n}</span>`).join("");
  row.innerHTML = `<div class="tr">${one}${one}</div>`; $("#rows").appendChild(row); r.tr = row.firstChild; r.spans = [...row.querySelectorAll(".lg")]; });
function renderAt(t) {
  rows.forEach((r, i) => { const wOne = r.tr.scrollWidth / 2, k = E.out(seg(t, i * 0.12, 0.6 + i * 0.12));
    let x = (t * r.sp) % wOne; x = r.dir < 0 ? -x : x - wOne;
    r.tr.style.transform = `translateX(${x + (1 - k) * 80 * r.dir}px)`; r.tr.parentNode.style.opacity = k;
    r.spans.forEach((s, j) => { s.style.color = i === 1 && j % LOGOS.length === 4 && t > 3 ? C.accent : "#2a2a2a"; }); });
  $("#lab").style.opacity = E.out(seg(t, 0, 0.6));
}
"""),

# ---------------------------------------------------------------- bars-3d
dict(slug="bars-3d", title="3D Bars", dur=6, bg="#f2f0ea",
desc="An isometric 3D bar chart whose prisms grow from the floor with staggered back-eases, value labels counting up on top and the winning bar highlighted. Use for revenue/growth, comparisons, rankings, survey results, KPIs and any 'numbers going up' data story.",
look="Seven isometric prisms on a light floor grid, three-tone shaded. They grow upward left to right with a slight overshoot; a value label rides each bar's top and counts up. The tallest bar switches to the accent palette and gets a pointer label.",
beats=["0.0–0.6 s: floor grid fades in.",
       "0.5–2.9 s: bars grow, 0.2 s stagger, 0.9 s each (back ease).",
       "Labels count with their bar.",
       "3.2–3.8 s: top bar turns accent, callout drops in; others fade to 70 %."],
build="""
Same isometric math as `motion-cube-stack` but each bar is one box with continuous height `h·E.back(k)`. Draw order: by x+y (back to front), then within a bar left face, right face, top. The label is canvas text placed at the projected top-centre. Highlight is a colour `mix()` driven by its own eased progress.
""",
knobs=["Data values and category labels.",
       "Bar footprint, spacing and max height.",
       "Growth stagger and ease.",
       "Highlight rule (max, latest, chosen index)."],
pitfalls=["Overshoot pushes labels above the frame for tall bars; leave headroom.",
          "Iso bars exaggerate differences visually; label exact values.",
          "Don't rotate a 3D chart during the data reveal; viewers lose the comparison."],
pairs=["cube-stack", "count-up", "donut-ring", "iso-city"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), vals = [32, 48, 41, 66, 58, 92, 74], labs = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"], s = 100, cs = Math.cos(Math.PI / 6);
const ox = 360, oy = 800, P = (x, y, z) => [ox + (x - y) * cs * s, oy + (x + y) * 0.5 * s - z * s];
const poly = (pts, col) => { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.closePath(); g.fillStyle = col; g.fill(); g.strokeStyle = col; g.lineWidth = 1; g.stroke(); };
function renderAt(t) {
  g.clearRect(0, 0, W, H);
  // floor band under the bars, which run along the screen-horizontal iso axis (x up, y down)
  g.globalAlpha = E.out(seg(t, 0, 0.6));
  poly([P(-0.2, 1.4, 0), P(8.2, -7.0, 0), P(10.0, -5.2, 0), P(1.6, 3.2, 0)], "#e3dfd4");
  g.strokeStyle = "#d0cbbf"; g.lineWidth = 1.5;
  for (let i = 0; i <= 8; i++) { g.beginPath(); g.moveTo(...P(-0.2 + i * 1.05, 1.4 - i * 1.05, 0)); g.lineTo(...P(1.6 + i * 1.05, 3.2 - i * 1.05, 0)); g.stroke(); }
  g.globalAlpha = 1;
  const top = vals.indexOf(Math.max(...vals)), hl = E.inOut(seg(t, 3.2, 3.8));
  vals.forEach((v, i) => { const k = seg(t, 0.5 + i * 0.2, 1.4 + i * 0.2); if (k <= 0) return;
    const h = v / 100 * 7.5 * E.back(k), x = 0.4 + i * 1.05, y = 0.8 - i * 1.05, w = 1.0, isT = i === top;
    g.globalAlpha = isT ? 1 : lerp(1, 0.7, hl);
    poly([P(x, y + w, h), P(x + w, y + w, h), P(x + w, y + w, 0), P(x, y + w, 0)], isT ? mix("#c9c3b8", C.accent, hl) : "#c9c3b8");
    poly([P(x + w, y, h), P(x + w, y + w, h), P(x + w, y + w, 0), P(x + w, y, 0)], isT ? mix("#8f897f", "#b8300f", hl) : "#8f897f");
    poly([P(x, y, h), P(x + w, y, h), P(x + w, y + w, h), P(x, y + w, h)], isT ? mix("#ffffff", "#ffb39c", hl) : "#ffffff");
    const [lx, ly] = P(x + w / 2, y + w / 2, h);
    g.fillStyle = C.ink; g.font = "400 56px 'Archivo Black', Arial Black, sans-serif"; g.textAlign = "center";
    g.fillText(Math.round(v * E.out(clamp(k * 1.2))), lx, ly - 30);
    const [bx, by] = P(x + w / 2, y + w + 0.6, 0); g.font = "700 22px 'JetBrains Mono', monospace"; g.fillStyle = "#6f6a61"; g.fillText(labs[i], bx, by + 20);
    g.globalAlpha = 1; });
  if (hl > 0) { const [cx, cy] = P(0.9 + top * 1.05, 1.3 - top * 1.05, vals[top] / 100 * 7.5);
    g.globalAlpha = hl; g.fillStyle = C.ink; g.beginPath(); g.roundRect(cx + 70, cy - 150 + (1 - hl) * -30, 300, 80, 40); g.fill();
    g.fillStyle = "#fff"; g.font = "700 30px 'JetBrains Mono', monospace"; g.textAlign = "left"; g.fillText("PEAK DAY ↑", cx + 105, cy - 98 + (1 - hl) * -30); g.globalAlpha = 1; }
}
"""),

# ---------------------------------------------------------------- agent-swarm
dict(slug="agent-swarm", title="Agent Swarm", dur=7, bg="var(--ink)",
desc="A central orchestrator node spawns AI agent nodes that fly out, connect with links, pass glowing task packets back and forth and tick off as done. Use for multi-agent AI, automation pipelines, distributed work, 'your team of AI agents', orchestration, workflows and parallel processing scenes.",
look="A glowing core node in the centre. Eight agent nodes burst outward on curved paths into a ring, each trailing a link back to the core. Bright packets travel out along the links, agents pulse while 'working' (a spinning arc), then flash to a check mark and send a packet back. Labels in mono under each agent.",
beats=["0.0–0.6 s: core scales in with a halo.",
       "0.6–1.8 s: agents spawn outward 0.1 s apart (back ease along a curved path).",
       "1.8–2.6 s: packets travel core → agents.",
       "2.4–4.8 s: agents work (spinner arcs), finishing at seeded times.",
       "On finish: check mark, colour flips to lime, packet returns to core.",
       "5.6–7.0 s: core pulses 'DONE', hold."],
build="""
Canvas. Agent `i` has a ring position at angle `2πi/8`; its spawn path is a quadratic curve from the core with a perpendicular bend. Each agent has seeded `start` and `finish` times. Packets are dots at `lerp(core, agent, E.inOut(p))` with a short fading trail (draw 6 copies at slightly earlier p). A spinner is an arc whose start angle is `t·6`. All state is derived from `t` and the per-agent times.
""",
knobs=["Agent count, ring radius, labels.",
       "Spawn stagger; per-agent work durations (seeded).",
       "Packet speed and colour; trail length.",
       "Done colour (lime) and the core's final label."],
pitfalls=["Spread finish times; agents finishing together looks fake.",
          "Too many simultaneous packets is noise; cap ~8 visible.",
          "Keep labels short (one word) at this size."],
pairs=["flow-line", "orbit-rings", "chat-thread", "command-palette"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), NA = 8, RR = 360, cx = W / 2, cy = H / 2, rr = rng(9);
const names = ["SEARCH", "CODE", "TEST", "REVIEW", "DESIGN", "WRITE", "DEPLOY", "MONITOR"];
const ag = names.map((n, i) => { const a = -Math.PI / 2 + i * 2 * Math.PI / NA; return { n, a, x: cx + Math.cos(a) * RR * 1.25, y: cy + Math.sin(a) * RR, sp: 0.6 + i * 0.1, fin: 3.0 + rr() * 1.8 }; });
const font = (w, s, f) => g.font = `${w} ${s}px ${f === "m" ? "'JetBrains Mono', monospace" : "'Archivo Black', Arial Black, sans-serif"}`;
function renderAt(t) {
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  const core = E.back(seg(t, 0, 0.6));
  ag.forEach(a => { const k = E.back(seg(t, a.sp, a.sp + 0.8)); if (k <= 0) return;
    const mx = (cx + a.x) / 2 - Math.sin(a.a) * 90, my = (cy + a.y) / 2 + Math.cos(a.a) * 90, u = clamp(k, 0, 1.2);
    a.px = (1 - u) ** 2 * cx + 2 * (1 - u) * u * mx + u * u * a.x; a.py = (1 - u) ** 2 * cy + 2 * (1 - u) * u * my + u * u * a.y;
    g.strokeStyle = "rgba(239,233,223,.18)"; g.lineWidth = 2; g.beginPath(); g.moveTo(cx, cy); g.quadraticCurveTo(mx, my, a.px, a.py); g.stroke(); a.mx = mx; a.my = my; });
  const packet = (a, p, col) => { for (let j = 0; j < 7; j++) { const q = clamp(p - j * 0.025); if (q <= 0 || q >= 1) continue; const u = E.inOut(q);
    const x = (1 - u) ** 2 * cx + 2 * (1 - u) * u * a.mx + u * u * a.x, y = (1 - u) ** 2 * cy + 2 * (1 - u) * u * a.my + u * u * a.y;
    g.fillStyle = col; g.globalAlpha = 1 - j / 7; g.beginPath(); g.arc(x, y, 9 - j, 0, 7); g.fill(); } g.globalAlpha = 1; };
  ag.forEach((a, i) => { if (t > a.sp + 0.8) { packet(a, seg(t, 1.8 + i * 0.08, 2.6 + i * 0.08), C.accent); }
    if (t > a.fin) { const back = seg(t, a.fin + 0.1, a.fin + 0.8); if (back > 0 && back < 1) { const u = 1 - back; packet(a, u, C.lime); } } });
  g.fillStyle = `rgba(255,74,28,${0.18 * core})`; g.beginPath(); g.arc(cx, cy, 120 * core + 10 * Math.sin(t * 3) * (t > 5.6 ? 1 : 0), 0, 7); g.fill();
  g.fillStyle = C.accent; g.beginPath(); g.arc(cx, cy, 70 * core, 0, 7); g.fill();
  g.fillStyle = C.ink; font(400, 30); g.textAlign = "center"; g.textBaseline = "middle"; g.globalAlpha = core; g.fillText(t > 5.6 ? "DONE" : "CORE", cx, cy); g.globalAlpha = 1;
  ag.forEach(a => { const k = E.back(seg(t, a.sp, a.sp + 0.8)); if (k <= 0) return; const done = t > a.fin, dk = E.back(seg(t, a.fin, a.fin + 0.3));
    g.fillStyle = done ? C.lime : "#262626"; g.strokeStyle = done ? C.lime : "#555"; g.lineWidth = 3;
    g.beginPath(); g.arc(a.px, a.py, 44 * Math.min(k, 1.1) * (done ? 1 + 0.15 * Math.sin(dk * Math.PI) : 1), 0, 7); g.fill(); g.stroke();
    if (!done && t > 2.4) { g.strokeStyle = C.accent; g.lineWidth = 5; g.beginPath(); g.arc(a.px, a.py, 56, t * 6, t * 6 + 1.8); g.stroke(); }
    if (done) { g.strokeStyle = C.ink; g.lineWidth = 7; g.lineCap = "round"; g.beginPath(); g.moveTo(a.px - 16, a.py + 2); g.lineTo(a.px - 4, a.py + 14); g.lineTo(a.px + 18, a.py - 12); g.stroke(); }
    g.fillStyle = "rgba(239,233,223,.8)"; font(700, 20, "m"); g.textAlign = "center"; g.fillText(a.n, a.px, a.py + 74); });
}
"""),

# ---------------------------------------------------------------- tile-grids
dict(slug="tile-grids", title="Tile Grids", dur=6, bg="var(--ink)",
desc="A full-screen grid of square tiles that ripple in a diagonal colour wave (lime → orange → red), flip and scale, then settle into a pixel picture or word. Use for transitions, chapter openers, 'systems' or 'grid' moments, pixel/mosaic reveals, brand patterns and rhythmic beat sections.",
look="Small rounded squares fill the frame. A wave sweeps diagonally from the top-left: tiles pop larger, rotate 90° and shift colour from lime through orange to red as the crest passes. A second wave from the centre leaves behind a picture: tiles inside a bitmap heart stay accent, the rest drop back to dark.",
beats=["0.0–2.2 s: diagonal wave crosses the grid (tile scale and colour).",
       "2.4–4.0 s: radial wave from the centre; tiles in the bitmap settle accent.",
       "4.0–6.0 s: picture holds; tiles breathe ±4 % on a slow sine."],
build="""
Each tile `(c, r)` has two wave phases: `p1 = seg(t, 0.2 + (c + r)·0.035, …)` for the diagonal wave and `p2` from its distance to the centre. Crest strength is `sin(π·p)`; scale, rotation and a 3-stop colour ramp come from it. The final state comes from a small bitmap (rows of 0/1 strings) mapped to the grid; tiles in the shape take the accent once `p2` passes 0.5.
""",
knobs=["Tile size/gap and grid dimensions.",
       "Wave directions, speeds, colour ramp.",
       "Bitmap picture (heart, letter, logo mark).",
       "Rotation on crest (0° to 180°)."],
pitfalls=["Canvas, not DOM: a full 1080p grid is ~1,000+ tiles.",
          "Design the bitmap at the grid's resolution; scaling it blurs the picture.",
          "Use the crest curve (sin πp) so tiles return to rest, or the frame ends noisy."],
pairs=["pixel-build", "dot-wipe", "wave-dots", "halftone-wave"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), TS = 60, COLS = Math.ceil(W / TS), ROWS = Math.ceil(H / TS);
const BMP = ["00110001100", "01111011110", "11111111111", "11111111111", "01111111110", "00111111100", "00011111000", "00001110000", "00000100000"];
const bw = BMP[0].length, bh = BMP.length, bx0 = Math.floor((COLS - bw) / 2), by0 = Math.floor((ROWS - bh) / 2);
const ramp = k => k < 0.5 ? mix(C.lime, C.yellow, k * 2) : mix(C.yellow, C.accent, (k - 0.5) * 2);
function renderAt(t) {
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
    const p1 = seg(t, 0.2 + (c + r) * 0.035, 0.9 + (c + r) * 0.035), crest1 = Math.sin(Math.PI * p1);
    const d = Math.hypot(c - COLS / 2, r - ROWS / 2), p2 = seg(t, 2.4 + d * 0.06, 3.1 + d * 0.06), crest2 = Math.sin(Math.PI * p2);
    const inPic = BMP[r - by0] && BMP[r - by0][c - bx0] === "1", settled = p2 > 0.5 && inPic;
    const crest = Math.max(crest1, crest2), breathe = settled ? 1 + 0.04 * Math.sin(t * 3 + c * 0.3) * seg(t, 4, 4.4) : 1;
    const sz = (TS - 10) * (0.55 + 0.45 * crest + (settled ? 0.4 : 0)) * breathe * 0.75;
    const col = crest > 0.02 ? ramp(crest) : settled ? C.accent : "#232323";
    g.save(); g.translate(c * TS + TS / 2, r * TS + TS / 2); g.rotate(crest * Math.PI / 2); g.fillStyle = col;
    g.beginPath(); g.roundRect(-sz / 2, -sz / 2, sz, sz, sz * 0.18); g.fill(); g.restore(); }
}
"""),
]
