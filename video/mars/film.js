// Mars video, cold open: flat vector space illustration, every frame a pure function of time (renderAt).
const W = 1920, H = 1080, Q = new URLSearchParams(location.search), PR = parseFloat(Q.get("pr")) || 1;
const TM = await (await fetch("timings.json")).json(), L = TM.scenes[0].lines, c = L.map(l => l.start), [B0, B1] = TM.burn;
const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x), lerp = (a, b, k) => a + (b - a) * k, seg = (t, a, b) => clamp((t - a) / (b - a));
const E = { out: x => 1 - (1 - x) ** 3, in: x => x ** 3, io: x => (x < 0.5 ? 4 * x ** 3 : 1 - (-2 * x + 2) ** 3 / 2), back: x => { const k = 1.70158; return 1 + (k + 1) * (x - 1) ** 3 + k * (x - 1) ** 2; } };
const fin = (t, a, d = 0.5) => E.out(seg(t, a, a + d)), pop = (t, a, d = 0.5) => E.back(seg(t, a, a + d));
function rng(seed) { let s = seed >>> 0; return () => { s = (s + 0x6d2b79f5) | 0; let x = Math.imul(s ^ (s >>> 15), 1 | s); x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x; return ((x ^ (x >>> 14)) >>> 0) / 4294967296; }; }
const $ = s => document.querySelector(s), cv = $("#gl"); cv.width = W * PR; cv.height = H * PR; const g = cv.getContext("2d");
const circ = (x, y, r, f) => { g.beginPath(); g.arc(x, y, Math.max(0, r), 0, 6.2832); g.fillStyle = f; g.fill(); };
const rr = (x, y, w, h, r, f) => { g.beginPath(); g.roundRect(x, y, w, h, r); g.fillStyle = f; g.fill(); };
const poly = (p, f) => { g.beginPath(); p.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.closePath(); g.fillStyle = f; g.fill(); };
const glow = (x, y, r, col, a) => { const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, col.replace("A", a)); gr.addColorStop(1, col.replace("A", 0)); g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r); };

// ---------------------------------------------------------------- backdrop: gradient, drifting nebulae, three parallax star layers
const STARS = [0.15, 0.4, 1].map((z, li) => { const r = rng(10 + li); return Array.from({ length: [260, 130, 50][li] }, () => ({ x: r() * W * 1.4 - W * 0.2, y: r() * H * 1.4 - H * 0.2, s: (0.6 + r() * 1.4) * (0.6 + z), p: r() * 6, z })); }).flat();
function backdrop(tg, px, py, dim = 1) {
  const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, "#0a1030"); gr.addColorStop(0.65, "#1b1850"); gr.addColorStop(1, "#33215f"); g.fillStyle = gr; g.fillRect(0, 0, W, H);
  glow(380 + Math.sin(tg * 0.05) * 60 - px * 0.1, 260, 620, "rgba(120,70,200,A)", 0.22 * dim); glow(1500 - px * 0.1, 860, 700, "rgba(40,140,190,A)", 0.16 * dim);
  for (const s of STARS) { const x = ((s.x - px * s.z) % (W * 1.4) + W * 1.4) % (W * 1.4) - W * 0.2, y = s.y - py * s.z, tw = 0.55 + 0.45 * Math.sin(tg * 1.7 + s.p);
    if (s.z === 1) glow(x, y, s.s * 7, "rgba(190,210,255,A)", 0.25 * tw * dim); circ(x, y, s.s, `rgba(235,240,255,${(0.35 + 0.6 * tw * s.z) * dim})`); } }
// ---------------------------------------------------------------- planets
const CRATERS = (() => { const r = rng(3); return Array.from({ length: 14 }, () => ({ a: r() * 6.28, d: Math.sqrt(r()) * 0.82, s: 0.04 + r() * 0.1 })); })();
function mars(x, y, R, spin = 0) {
  glow(x, y, R * 1.45, "rgba(255,120,80,A)", 0.28);
  g.save(); g.beginPath(); g.arc(x, y, R, 0, 6.2832); g.clip();
  const base = g.createRadialGradient(x - R * 0.35, y - R * 0.4, R * 0.1, x, y, R * 1.05); base.addColorStop(0, "#ff8a5c"); base.addColorStop(0.55, "#e4583b"); base.addColorStop(1, "#a83a2c"); g.fillStyle = base; g.fillRect(x - R, y - R, 2 * R, 2 * R);
  for (let i = 0; i < 5; i++) { const yy = y - R + (i + 0.5) * (2 * R / 5), w = Math.sin(i * 1.7 + spin) * R * 0.08; poly([[x - R, yy - R * 0.05 + w], [x + R, yy + w], [x + R, yy + R * 0.06 + w], [x - R, yy + R * 0.09 + w]], "rgba(190,70,45,.28)"); }
  for (const k of CRATERS) { const a = k.a + spin, cx = x + Math.cos(a) * k.d * R, cy = y + Math.sin(a) * k.d * R * 0.9; circ(cx, cy, k.s * R, "rgba(160,52,36,.55)"); circ(cx - k.s * R * 0.18, cy - k.s * R * 0.18, k.s * R * 0.72, "rgba(208,82,58,.6)"); }
  g.beginPath(); g.ellipse(x - R * 0.08, y - R * 0.9, R * 0.3, R * 0.1, -0.08, 0, 6.2832); g.fillStyle = "rgba(255,238,228,.8)"; g.fill(); g.beginPath(); g.ellipse(x + R * 0.12, y - R * 0.84, R * 0.12, R * 0.04, 0, 0, 6.2832); g.fill();                                  // polar cap
  const sh = g.createRadialGradient(x - R * 0.55, y - R * 0.5, R * 0.6, x - R * 0.2, y - R * 0.2, R * 1.7); sh.addColorStop(0, "rgba(20,10,40,0)"); sh.addColorStop(1, "rgba(20,10,40,.72)"); g.fillStyle = sh; g.fillRect(x - R, y - R, 2 * R, 2 * R);
  g.restore(); g.beginPath(); g.arc(x, y, R - 2, 3.4, 4.9); g.strokeStyle = "rgba(255,200,170,.55)"; g.lineWidth = Math.max(2, R * 0.02); g.stroke(); }
function earth(x, y, R) {
  glow(x, y, R * 1.6, "rgba(90,170,255,A)", 0.3);
  g.save(); g.beginPath(); g.arc(x, y, R, 0, 6.2832); g.clip(); circ(x, y, R, "#2f78dc");
  poly([[x - R * 0.6, y - R * 0.3], [x - R * 0.1, y - R * 0.55], [x + R * 0.1, y - R * 0.1], [x - R * 0.2, y + R * 0.3], [x - R * 0.55, y + R * 0.15]], "#3fbf80");
  poly([[x + R * 0.25, y + R * 0.05], [x + R * 0.7, y - R * 0.05], [x + R * 0.6, y + R * 0.5], [x + R * 0.3, y + R * 0.6]], "#3fbf80");
  g.strokeStyle = "rgba(255,255,255,.8)"; g.lineWidth = R * 0.08; g.lineCap = "round"; g.beginPath(); g.arc(x, y, R * 0.75, 3.6, 4.4); g.stroke(); g.beginPath(); g.arc(x + R * 0.1, y, R * 0.55, 0.3, 1.1); g.stroke();
  const sh = g.createRadialGradient(x - R * 0.5, y - R * 0.5, R * 0.5, x, y, R * 1.6); sh.addColorStop(0, "rgba(10,10,40,0)"); sh.addColorStop(1, "rgba(10,10,40,.7)"); g.fillStyle = sh; g.fillRect(x - R, y - R, 2 * R, 2 * R); g.restore(); }
// ---------------------------------------------------------------- Mangalyaan: gold box, one solar wing, dish on top, engine at the back (local units, nose = +x)
function craft(x, y, s, rot, burn, tg) {
  g.save(); g.translate(x, y); g.rotate(rot); g.scale(s, s);
  if (burn > 0.01) { const f = 0.85 + 0.15 * Math.sin(tg * 40); glow(-46, 0, 120 * burn, "rgba(255,150,60,A)", 0.55 * burn);
    poly([[-34, -13], [-34 - 120 * burn * f, 0], [-34, 13]], "rgba(255,140,50,.9)"); poly([[-34, -8], [-34 - 70 * burn * f, 0], [-34, 8]], "rgba(255,226,140,.95)"); }
  rr(-38, -9, 10, 18, 3, "#7d8596");                                                                // nozzle
  g.lineWidth = 4; g.strokeStyle = "#c9cfdb"; g.beginPath(); g.moveTo(0, 26); g.lineTo(0, 62); g.stroke();   // boom to the wing
  rr(-46, 62, 92, 40, 5, "#2c4fc4"); g.strokeStyle = "rgba(160,190,255,.7)"; g.lineWidth = 2; for (let i = 1; i < 4; i++) { g.beginPath(); g.moveTo(-46 + i * 23, 62); g.lineTo(-46 + i * 23, 102); g.stroke(); } g.beginPath(); g.moveTo(-46, 82); g.lineTo(46, 82); g.stroke();
  rr(-28, -26, 56, 52, 8, "#f2b33d"); rr(-28, 6, 56, 20, 6, "#d58f27"); rr(-20, -18, 18, 12, 3, "rgba(255,240,190,.7)");   // gold body
  g.lineWidth = 4; g.strokeStyle = "#c9cfdb"; g.beginPath(); g.moveTo(6, -26); g.lineTo(10, -40); g.stroke();
  g.save(); g.translate(12, -50); g.rotate(-0.35); g.beginPath(); g.ellipse(0, 0, 30, 12, 0, 0, 6.2832); g.fillStyle = "#eef1f6"; g.fill(); g.beginPath(); g.ellipse(0, 3, 24, 7, 0, 0, 6.2832); g.fillStyle = "#c8cfdb"; g.fill(); g.restore();
  g.restore(); }
function person(x, y, h) { const u = h / 10; circ(x, y - 9 * u, u * 1.1, "#ffe1c4"); rr(x - u * 1.2, y - 7.8 * u, u * 2.4, u * 4, u, "#ff8f5a"); rr(x - u * 1.1, y - 4 * u, u * 0.9, u * 4, u * 0.4, "#2c3a7a"); rr(x + u * 0.2, y - 4 * u, u * 0.9, u * 4, u * 0.4, "#2c3a7a"); }
function dashArc(pts, col, w, dash, upto = 1) { const n = Math.max(2, Math.round(pts.length * upto)); g.beginPath(); pts.slice(0, n).forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.setLineDash(dash); g.strokeStyle = col; g.lineWidth = w; g.lineCap = "round"; g.stroke(); g.setLineDash([]); }
const ell = (cx, cy, rx, ry, tilt, a0 = 0, a1 = 6.2832, n = 160) => Array.from({ length: n + 1 }, (_, i) => { const a = lerp(a0, a1, i / n), x = Math.cos(a) * rx, y = Math.sin(a) * ry; return [cx + x * Math.cos(tilt) - y * Math.sin(tilt), cy + x * Math.sin(tilt) + y * Math.cos(tilt)]; });
function tx(s, x, y, size, col, align = "left", w = 800) { g.font = `${w} ${size}px Body, Arial`; g.fillStyle = col; g.textAlign = align; g.textBaseline = "middle"; g.fillText(s, x, y); }

// ---------------------------------------------------------------- DOM text
const show = (id, k, dy = 30, extra = "") => { const e = $(id); e.style.opacity = clamp(k); e.style.transform = `translateY(${((1 - clamp(k)) * dy).toFixed(1)}px) ${extra}`; };
$("#src").textContent = "Sources: ISRO · The Planetary Society · NASA";

window.renderAt = function (tg) {
  tg = clamp(tg, 0, TM.total - 0.001); const t = tg, burnK = seg(t, B0, B0 + 0.5) * (1 - seg(t, B1 - 0.3, B1)), win = c[5], orbitK = E.io(seg(t, win - 0.1, win + 2.2));
  g.setTransform(PR, 0, 0, PR, 0, 0);
  // camera: slow push while falling in, wide for the radio gap, push on "It works", settle for the comparison
  let cz = 1, fx = 960, fy = 540;
  if (t < c[3]) { cz = lerp(1, 1.1, E.io(seg(t, 0, c[3]))); fx = 1250; fy = 620; } else if (t >= c[4] && t < c[7]) { cz = 1 + 0.06 * fin(t, win, 1.2); fx = 1250; fy = 620; }
  const shake = burnK * 2.5; g.translate(fx * (1 - cz) + Math.sin(tg * 47) * shake, fy * (1 - cz) + Math.cos(tg * 53) * shake); g.scale(cz, cz);
  const px = tg * 14, py = 0; backdrop(tg, px, py, t > c[4] + 2.6 && t < win ? 0.55 : 1);

  if (t < c[3]) {   // falling in, then the burn begins
    const k = E.io(seg(t, c[1] - 0.5, c[3])), R = lerp(90, 330, k), mx = lerp(1500, 1340, k), my = lerp(600, 690, k); mars(mx, my, R, tg * 0.01);
    earth(lerp(260, 170, k), lerp(880, 940, k), lerp(12, 8, k));
    const path = ell(mx, my, R * 1.45, R * 0.55, -0.12, Math.PI * 0.95, Math.PI * 1.55, 120), inbound = Array.from({ length: 60 }, (_, i) => [lerp(380, path[0][0], i / 59), lerp(430, path[0][1], i / 59) - Math.sin(i / 59 * Math.PI) * 30]);
    const ap = seg(t, c[1], c[3]), cpos = ap < 0.7 ? inbound[Math.floor(ap / 0.7 * 59)] : path[Math.floor((ap - 0.7) / 0.3 * 119 * 0.35)];
    dashArc(inbound.concat(path), "rgba(255,255,255,.35)", 3, [6, 14], fin(t, c[1] + 0.3, 2.5));
    const rot = lerp(-0.1, Math.PI - 0.1, E.io(seg(t, c[2] + 0.8, B0))), s = lerp(0.55, 1.15, k);
    craft(cpos[0], cpos[1], s, rot, burnK, tg);
    const sk = fin(t, c[1] + 4.2) * (1 - fin(t, c[2] - 0.2, 0.3)); if (sk > 0) { g.globalAlpha = sk; person(cpos[0] + 95 * s, cpos[1] + 40 * s, 92 * s); g.globalAlpha = 1; const e = $("#scale"); e.style.left = (cpos[0] + 70 * s) * cz + fx * (1 - cz) + "px"; e.style.top = (cpos[1] + 60 * s) * cz + fy * (1 - cz) + "px"; }
    show("#scale", sk);
  } else if (t < c[4]) {   // pulled back: Earth, Mars, and a radio signal that cannot help in time
    const ex = 300, mx = 1580, y = 620; earth(ex, y, 70); mars(mx, y, 120, tg * 0.01); craft(mx - 170, y - 70, 0.45, Math.PI - 0.3, burnK, tg);
    for (let i = 0; i < 6; i++) { const u = ((t - c[3]) * 0.09 + i * 0.05) % 1, x = ex + 80 + u * 300; g.beginPath(); g.arc(x - 60, y, 70 + i * 6, -0.55, 0.55); g.strokeStyle = `rgba(150,220,255,${Math.max(0, 0.85 * (1 - u * 2.4))})`; g.lineWidth = 7; g.stroke(); }
    dashArc([[ex + 80, y + 120], [mx - 130, y + 120]], "rgba(255,255,255,.25)", 3, [6, 12]); tx("224 million km", (ex + mx) / 2, y + 160, 30, "rgba(220,226,255,.85)", "center", 700);
  } else if (t < c[7] + 0.0 || t < c[8]) {   // the burn, the miss we avoid, the capture, the records, the price
    const mx = 1250, my = 640, R = 300; mars(mx, my, R, tg * 0.01);
    const ghost = Array.from({ length: 80 }, (_, i) => { const u = i / 79; return [lerp(mx - 520, mx + 900, u), my - 330 + Math.sin(u * 2.4) * 120 - u * 260]; });
    const gk = fin(t, c[4] + 0.6, 1.2) * (1 - fin(t, win - 0.4, 0.4)); if (gk > 0) { g.globalAlpha = gk; dashArc(ghost, "rgba(255,120,100,.9)", 4, [10, 14], fin(t, c[4] + 0.6, 1.6)); g.globalAlpha = 1; }
    const orb = ell(mx, my, R * 1.55, R * 0.5, -0.12); g.save(); g.globalAlpha = 0.25 + 0.55 * orbitK; dashArc(orb, orbitK > 0.05 ? "#ffd36b" : "rgba(255,255,255,.5)", 4, [2, 12], t < win ? 0.28 : lerp(0.28, 1, orbitK)); g.restore();
    const a0 = Math.PI * 1.3, a = t < win ? a0 : a0 + (t - win) * 0.55, cp = [mx + Math.cos(a) * R * 1.55, my + Math.sin(a) * R * 0.5], tilt = -0.12, cpos = [mx + (cp[0] - mx) * Math.cos(tilt) - (cp[1] - my) * Math.sin(tilt), my + (cp[0] - mx) * Math.sin(tilt) + (cp[1] - my) * Math.cos(tilt)];
    const front = Math.sin(a) > 0; const draw = () => craft(cpos[0], cpos[1], 1.05, a + Math.PI / 2 + (t < win ? Math.PI : 0), burnK, tg);
    if (!front && t >= win) { draw(); } if (front || t < win) draw();
    if (t >= c[7]) { const e = $("#price"), k = pop(t, c[7] + 1.2, 0.5); e.style.left = (cpos[0] - 150) * cz + fx * (1 - cz) + "px"; e.style.top = (cpos[1] - 170) * cz + fy * (1 - cz) + "px"; e.style.opacity = clamp(k * 3); e.style.transform = `scale(${k.toFixed(3)}) rotate(-4deg)`;
      const e2 = $("#price2"); e2.style.left = (cpos[0] - 120) * cz + fx * (1 - cz) + "px"; e2.style.top = (cpos[1] - 92) * cz + fy * (1 - cz) + "px"; e2.style.opacity = fin(t, c[7] + 1.6) * (1 - fin(t, c[8] - 0.3, 0.3)); }
  } else if (t < c[9] - 0.2) {   // the comparison
    backdrop(tg, px, py, 0.9); const bx = 560, by = 860, maxH = 520, items = [["GRAVITY", "Hollywood film, 2013", 100, "#8a7cff"], ["MARS ORBITER MISSION", "ISRO, 2013–14", 74, "#ffd36b"]];
    items.forEach(([n, sub, v, col], i) => { const k = E.out(seg(t, c[8] + 0.2 + i * 0.5, c[8] + 1.2 + i * 0.5)), h = maxH * v / 100 * k, x = bx + i * 520;
      rr(x, by - h, 300, h, 22, col); tx(`$${Math.round(v * k)}M`, x + 150, by - h - 46, 64, "#fff", "center", 900); tx(n, x + 150, by + 50, 30, "#fff", "center", 800); tx(sub, x + 150, by + 92, 22, "rgba(220,226,255,.75)", "center", 600); });
    craft(bx + 520 + 150, by - maxH * 0.74 * E.out(seg(t, c[8] + 0.7, c[8] + 1.7)) + 70, 0.8, -0.2, 0, tg);
    g.save(); g.translate(bx + 150, by - maxH * E.out(seg(t, c[8] + 0.2, c[8] + 1.2)) + 80); rr(-70, -10, 140, 90, 10, "#2a2350"); g.rotate(-0.25); rr(-70, -40, 140, 30, 6, "#2a2350"); g.fillStyle = "#fff"; for (let i = 0; i < 4; i++) { g.beginPath(); g.moveTo(-60 + i * 36, -40); g.lineTo(-40 + i * 36, -40); g.lineTo(-52 + i * 36, -10); g.lineTo(-72 + i * 36, -10); g.closePath(); g.fill(); } g.restore();
  } else {   // title
    mars(700, 1500, 780, tg * 0.004);
  }
  // DOM text cues
  show("#date", fin(t, 0.6, 0.8) * (1 - fin(t, c[1] - 0.2, 0.4)));
  show("#dist", fin(t, c[1] + 0.3) * (1 - fin(t, c[2] - 0.2, 0.3))); show("#dist2", fin(t, c[1] + 0.8) * (1 - fin(t, c[2] - 0.2, 0.3)));
  show("#burn", fin(t, c[2] + 1.5) * (1 - fin(t, c[3] - 0.2, 0.3)));
  show("#clock", fin(t, c[3] + 2.2) * (1 - fin(t, c[4] - 0.2, 0.3))); show("#clock2", fin(t, c[3] + 2.6) * (1 - fin(t, c[4] - 0.2, 0.3)));
  show("#miss", fin(t, c[4] + 0.5) * (1 - fin(t, win - 0.6, 0.4)));
  { const k = pop(t, win + 0.05, 0.45); $("#works").style.opacity = clamp(k * 2) * (1 - fin(t, c[6] - 0.2, 0.3)); $("#works").style.transform = `scale(${(0.6 + 0.4 * k).toFixed(3)})`; }
  show("#first1", fin(t, c[6] + 1.0) * (1 - fin(t, c[7] - 0.3, 0.3))); show("#first2", fin(t, c[6] + 4.0) * (1 - fin(t, c[7] - 0.3, 0.3)));
  if (t < c[7] || t >= c[8] - 0.3) { $("#price").style.opacity = 0; $("#price2").style.opacity = 0; }
  show("#title", fin(t, c[9] - 0.1, 0.5), 40);
  $("#flash").style.opacity = (t > win && t < win + 0.5 ? 0.35 * (1 - seg(t, win, win + 0.5)) : 0) + (t > c[9] && t < c[9] + 0.3 ? 0.25 * (1 - seg(t, c[9], c[9] + 0.3)) : 0);
  $("#src").style.opacity = fin(t, 1.0) * (t < c[9] ? 1 : 0);
};
window.DUR = TM.total;
await document.fonts.ready; renderAt(parseFloat(Q.get("t")) || 0); window.READY = true;
if (Q.has("play")) { const s0 = performance.now(); const loop = () => { renderAt(((performance.now() - s0) / 1000) % TM.total); requestAnimationFrame(loop); }; loop(); }
