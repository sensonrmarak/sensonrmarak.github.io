import * as THREE from "three";
import { buildAircraft, explode, setControls, glow, matsOf, loft, COL } from "./model.js";

const W = 1920, H = 1080, Q = new URLSearchParams(location.search);
const TM = await (await fetch("timings.json")).json();
const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x), lerp = (a, b, k) => a + (b - a) * k;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const E = { out: x => 1 - (1 - x) ** 3, in: x => x ** 3, io: x => (x < 0.5 ? 4 * x ** 3 : 1 - (-2 * x + 2) ** 3 / 2), expo: x => (x >= 1 ? 1 : 1 - 2 ** (-10 * x)),
  back: x => { const c = 1.70158; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2; } };
const pop = (t, a, d = 0.45) => E.back(seg(t, a, a + d)), fin = (t, a, d = 0.4) => E.out(seg(t, a, a + d));
function rng(seed) { let s = seed >>> 0; return () => { s = (s + 0x6d2b79f5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const $ = s => document.querySelector(s);
const V = (x, y, z) => new THREE.Vector3(x, y, z);

// ------------------------------------------------------------------ renderer, world
const renderer = new THREE.WebGLRenderer({ canvas: $("#gl"), antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(parseFloat(Q.get("pr")) || 1); renderer.setSize(W, H, false);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(35, W / H, 0.5, 6000);
const sky = new THREE.Mesh(new THREE.SphereGeometry(3000, 32, 16), new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false,
  uniforms: { top: { value: new THREE.Color(0x0b2f7a) }, mid: { value: new THREE.Color(0x6fb1ee) }, bot: { value: new THREE.Color(0xdff0ff) } },
  vertexShader: "varying float h; void main(){ h = normalize(position).y; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }",
  fragmentShader: "uniform vec3 top; uniform vec3 mid; uniform vec3 bot; varying float h; void main(){ vec3 c = h > 0.0 ? mix(mid, top, pow(h, 0.55)) : mix(mid, bot, pow(-h, 0.4)); gl_FragColor = vec4(c, 1.0); }" }));
scene.add(sky);
const hemi = new THREE.HemisphereLight(0xdfeaff, 0x8b98b5, 1.25), sun = new THREE.DirectionalLight(0xfff2dc, 2.6), fill = new THREE.DirectionalLight(0xbcd4ff, 0.7);
sun.position.set(40, 80, 60); fill.position.set(-60, -20, -40); scene.add(hemi, sun, fill);
function skyCol(top, mid, bot) { const u = sky.material.uniforms; u.top.value.setHex(top); u.mid.value.setHex(mid); u.bot.value.setHex(bot); }

const dotTex = (() => { const c = document.createElement("canvas"); c.width = c.height = 64; const g = c.getContext("2d"), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.55, "rgba(255,255,255,.9)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c); })();
const puffTex = (() => { const c = document.createElement("canvas"); c.width = c.height = 128; const g = c.getContext("2d"), gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  gr.addColorStop(0, "rgba(255,255,255,.95)"); gr.addColorStop(0.5, "rgba(255,255,255,.55)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c); })();
// clouds
const clouds = new THREE.Group(); scene.add(clouds); const CL = [];
{ const r = rng(11); for (let i = 0; i < 46; i++) { const base = V((r() - 0.5) * 700, r() < 0.8 ? -18 - r() * 70 : 26 + r() * 40, (r() - 0.5) * 420), n = 3 + Math.floor(r() * 3);
  for (let j = 0; j < n; j++) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: puffTex, transparent: true, opacity: 0.4, depthWrite: false })); const sc = 34 + r() * 40; s.scale.set(sc * 1.5, sc, 1);
    const off = V((r() - 0.5) * 50, (r() - 0.5) * 10, (r() - 0.5) * 30); clouds.add(s); CL.push({ s, base, off, jx: r() * 1500, jy: 95 + r() * 80, jz: -320 + r() * 420 }); } } }
function cloudsFly(tg, speed = 55) { CL.forEach(c => { const x = ((c.base.x - tg * speed) % 700 + 1050) % 700 - 350; c.s.position.set(x + c.off.x, c.base.y + c.off.y, c.base.z + c.off.z); }); }
function cloudsWorld() { CL.forEach(c => c.s.position.set(c.jx + c.off.x, c.jy + c.off.y, c.jz + c.off.z)); }

// aircraft
const A = buildAircraft(); A.rotation.order = "YZX"; scene.add(A); const P = A.userData.P;
const MATS = { nose: matsOf(P.nose), fuselage: matsOf(P.fuselage), engines: matsOf(P.engines), tail: matsOf(P.tail), gear: matsOf(P.gear), fuel: matsOf(P.fuel), systems: matsOf(P.systems), movables: P.movMats };
MATS.wings = matsOf(P.wings).filter(m => !P.movMats.includes(m));
const ALLM = matsOf(A); ALLM.forEach(m => { m.userData.e0 = m.emissive.getHex(); m.userData.i0 = m.emissiveIntensity; });
function resetGlow() { ALLM.forEach(m => { m.emissive.setHex(m.userData.e0); m.emissiveIntensity = m.userData.i0; }); }
const ailM = P.mov.ail.map(a => a.userData.piv.children[0].material), flapM = P.mov.flaps.map(a => a.userData.piv.children[0].material), slatM = P.mov.slats.map(a => a.userData.piv.children[0].material), spoilM = P.mov.spoil.map(a => a.userData.piv.children[0].material);

// arrows
function mkArrow(color) { const g = new THREE.Group(), m = new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 0.45, roughness: 0.4 });
  const sh = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 1, 16), m), hd = new THREE.Mesh(new THREE.ConeGeometry(1.5, 2.6, 20), m); g.add(sh, hd); g.userData = { sh, hd }; scene.add(g); g.visible = false; return g; }
function setArrow(a, o, dir, len, s = 1) { a.visible = len > 0.05; if (!a.visible) return; const d = dir.clone().normalize(); a.position.copy(o); a.quaternion.setFromUnitVectors(V(0, 1, 0), d); a.scale.setScalar(s);
  const L = len / s, body = Math.max(0.01, L - 2.6); a.userData.sh.scale.y = body; a.userData.sh.position.y = body / 2; a.userData.hd.position.y = body + 1.3; }
const AR = { lift: mkArrow(0xffb11f), weight: mkArrow(0x4f7dff), thrust: mkArrow(0x7ddc3a), drag: mkArrow(0xff5f8a), down: mkArrow(0x59c8ff) };

// point clouds helper
function mkPoints(n, size, opacity = 1) { const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(new Float32Array(n * 3), 3)); g.setAttribute("color", new THREE.Float32BufferAttribute(new Float32Array(n * 3).fill(1), 3));
  const p = new THREE.Points(g, new THREE.PointsMaterial({ size, map: dotTex, vertexColors: true, transparent: true, opacity, depthWrite: false, sizeAttenuation: true })); p.frustumCulled = false; p.visible = false; scene.add(p); return p; }
const setP = (p, i, x, y, z) => p.geometry.attributes.position.setXYZ(i, x, y, z), setC = (p, i, r, g, b) => p.geometry.attributes.color.setXYZ(i, r, g, b);
const upd = p => { p.geometry.attributes.position.needsUpdate = true; p.geometry.attributes.color.needsUpdate = true; };

// ---- airfoil rig
const RIG = new THREE.Group(); scene.add(RIG); const foil = new THREE.Group(); RIG.add(foil);
const afSec = z => ({ le: [5, 0, z], chord: 10, t: 0.13, m: 0.04 });
foil.add(new THREE.Mesh(loft([afSec(-6), afSec(6)]), new THREE.MeshStandardMaterial({ color: 0xeef1f5, metalness: 0.3, roughness: 0.35, side: THREE.DoubleSide })));
foil.add(new THREE.Mesh(loft([afSec(6), afSec(6.06)]), new THREE.MeshStandardMaterial({ color: COL.gold, metalness: 0.5, roughness: 0.35, side: THREE.DoubleSide, emissive: 0x6b4a00, emissiveIntensity: 0.5 })));
const SY0 = [0.4, 0.9, 1.5, 2.2, 3.0, 3.9, 4.9, 6.0], NPL = 90, flow = mkPoints(SY0.length * 2 * NPL, 0.5, 0.95);
const afU = u => { const yt = 5 * 0.13 * (0.2969 * Math.sqrt(u) - 0.126 * u - 0.3516 * u * u + 0.2843 * u ** 3 - 0.1036 * u ** 4), yc = 4 * 0.04 * u * (1 - u); return [(yc + yt) * 10, (yc - yt) * 10]; };
function surfY(x, al) { const u = (5 - x) / 10; if (u <= 0 || u >= 1) return [x * Math.sin(al) * (u <= 0 ? Math.exp(-(-u) * 6) : Math.exp(-(u - 1) * 6)), x * Math.sin(al) * (u <= 0 ? Math.exp(-(-u) * 6) : Math.exp(-(u - 1) * 6))]; const [a, b] = afU(u); return [x * Math.sin(al) + a * Math.cos(al), x * Math.sin(al) + b * Math.cos(al)]; }
function streamY(x, y0, al, t) { const deg = al * 57.3, liftK = deg < 15 ? deg / 15 : Math.max(0.2, 1 - (deg - 15) / 4), [su, sl] = surfY(x, al), a = Math.abs(y0);
  let y = y0 > 0 ? y0 + su * Math.exp(-a / 3.2) + 0.25 * Math.exp(-a) * (x < 5 && x > -5 ? 1 : 0) : y0 + sl * Math.exp(-a / 3.2) - 0.2 * Math.exp(-a) * (x < 5 && x > -5 ? 1 : 0);
  y += -0.7 * liftK * Math.exp(-(((x - 9) / 4) ** 2)) * Math.exp(-a / 6);                       // upwash ahead of the wing
  if (x < -4) y -= 0.2 * liftK * (1 - Math.exp(-(-4 - x) / 5)) * 5 * Math.exp(-a / 7);        // downwash behind it
  const sepK = clamp((deg - 13.5) / 3.5); if (sepK > 0 && y0 > 0 && y0 < 4) { const xs = 5 - 10 * (1 - 0.8 * sepK); if (x < xs) { const d = xs - x; y += sepK * Math.exp(-y0 / 2.5) * (d * 0.3 + Math.sin(x * 2.3 + t * 9 + y0 * 4) * 0.45 * Math.min(1, d / 2)); } }
  return y; }
function drawFlow(t, al, on = 1, hi = 0) { flow.visible = on > 0.01; flow.material.opacity = 0.95 * on; let i = 0;
  for (const s of [1, -1]) SY0.forEach((y0a, li) => { if (s < 0 && li > 5) { for (let k = 0; k < NPL; k++, i++) setP(flow, i, 0, -999, 0); return; } const y0 = s * y0a, v = s > 0 ? 9.5 + 3 * Math.exp(-y0a / 2) : 8 - 1.2 * Math.exp(-y0a / 2);
    for (let k = 0; k < NPL; k++, i++) { const x = 17 - (((k / NPL) * 34 + t * v + li * 1.7) % 34), y = streamY(x, y0, al, t), z = 6.5 + ((li * 37 + k * 13) % 5) * 0.12;
      setP(flow, i, x, y, z); const near = Math.exp(-y0a / 2.2) * hi; s > 0 ? setC(flow, i, lerp(0.75, 0.3, near), lerp(0.92, 0.75, near), 1) : setC(flow, i, 1, lerp(0.95, 0.55, near), lerp(0.9, 0.4, near)); } });
  upd(flow); }
const mkBall = c => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.42, 20, 14), new THREE.MeshStandardMaterial({ color: c, emissive: c, emissiveIntensity: 0.7 })); m.visible = false; scene.add(m); return m; };
const ballT = mkBall(0xff4a3a), ballB = mkBall(0x3aa0ff);
const glowS = (c) => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: puffTex, color: c, transparent: true, opacity: 0, depthWrite: false })); scene.add(s); return s; };
const loP = glowS(0x3aa0ff), hiP = glowS(0xff5a3a);

// ---- engine rig (flow goes toward -x)
const ENG = new THREE.Group(); scene.add(ENG); const EM = {};
{ const lathe = (pts, c, o = {}) => { const g = new THREE.LatheGeometry(pts.map(p => new THREE.Vector2(p[1], p[0])), 48, 0, Math.PI); g.rotateZ(-Math.PI / 2); g.rotateX(Math.PI / 2); const m = new THREE.MeshStandardMaterial({ color: c, side: THREE.DoubleSide, metalness: 0.5, roughness: 0.4, ...o }); const me = new THREE.Mesh(g, m); ENG.add(me); return me; };
  lathe([[5.6, 2.55], [6.0, 2.75], [5.4, 2.98], [2, 3.05], [-1.5, 2.8], [-2.6, 2.5], [-2.6, 2.38], [-1.5, 2.6], [2, 2.7], [5.2, 2.6], [5.6, 2.55]], 0xdde3ec, { metalness: 0.35, roughness: 0.45 });
  lathe([[3.2, 1.0], [3.0, 1.25], [0.5, 1.25], [-3.2, 1.3], [-4.2, 0.95]], 0xaeb6c2, { transparent: true, opacity: 0.38 });
  const disc = (x, r, c, key, th = 0.16) => { const m = new THREE.MeshStandardMaterial({ color: c, metalness: 0.7, roughness: 0.35 }); const d = new THREE.Mesh(new THREE.CylinderGeometry(r, r, th, 40), m); d.rotation.z = Math.PI / 2; d.position.x = x; ENG.add(d); (EM[key] ||= []).push(m); return d; };
  EM.fanG = new THREE.Group(); EM.fanG.position.x = 4.4; ENG.add(EM.fanG); const fm = new THREE.MeshStandardMaterial({ color: 0x2c313a, metalness: 0.7, roughness: 0.3 }); EM.fan = [fm];
  for (let i = 0; i < 20; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.1, 1.95, 0.42), fm), a = i / 20 * Math.PI * 2; b.position.set(0, Math.cos(a) * 1.4, Math.sin(a) * 1.4); b.rotation.x = a; b.rotation.y = 0.55; EM.fanG.add(b); }
  const sp = new THREE.Mesh(new THREE.ConeGeometry(0.55, 1.2, 24), new THREE.MeshStandardMaterial({ color: 0xe6e9ee })); sp.rotation.z = -Math.PI / 2; sp.position.x = 0.5; EM.fanG.add(sp);
  for (let i = 0; i < 7; i++) disc(2.7 - i * 0.36, 1.12 - i * 0.07, 0x7f95b8, "comp");
  const cm = new THREE.MeshStandardMaterial({ color: 0xff7a1a, emissive: 0xff5a00, emissiveIntensity: 1.2, transparent: true, opacity: 0.9 }); const cb = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 0.85, 1.25, 40), cm); cb.rotation.z = Math.PI / 2; cb.position.x = -0.55; ENG.add(cb); EM.comb = [cm];
  for (let i = 0; i < 4; i++) disc(-1.6 - i * 0.42, 0.85 + i * 0.09, 0xc79a3a, "turb");
  const nz = new THREE.Mesh(new THREE.ConeGeometry(0.75, 2.0, 30), new THREE.MeshStandardMaterial({ color: 0x8d939c, metalness: 0.8, roughness: 0.3 })); nz.rotation.z = Math.PI / 2; nz.position.x = -4.3; ENG.add(nz);
  const shf = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 8.2, 16), new THREE.MeshStandardMaterial({ color: 0xd0d5dc, metalness: 0.9, roughness: 0.2 })); shf.rotation.z = Math.PI / 2; shf.position.x = 0.4; ENG.add(shf); }
const NEP = 900, epart = mkPoints(NEP, 0.2, 0.95), er = rng(5), EP = Array.from({ length: NEP }, (_, i) => ({ core: i % 9 === 0 ? 1 : (i % 3 === 0 ? 1 : 0), a: er() * Math.PI, rr: er(), ph: er() }));
function drawEngine(t, on, hiBy = 0) { epart.visible = on > 0.01; epart.material.opacity = on; EP.forEach((p, i) => { const sp = p.core ? 0.22 : 0.3, u = (p.ph + t * sp) % 1, x = 9 - u * 19; let r, cr, cg, cb;
    if (p.core) { const sq = x > 3 ? 1 : x > 0.2 ? lerp(0.55, 1, (x - 0.2) / 2.8) : 0.55 + clamp((-x - 1) / 4) * 0.3; r = (0.25 + p.rr * 0.85) * sq * (x > 3.4 ? 1.9 : 1);
      const hot = clamp((0.4 - x) / 1.2); cr = lerp(0.55, 1, hot); cg = lerp(0.8, x < -1.4 ? 0.35 : 0.6, hot); cb = lerp(1, 0.1, hot); const dim = 1 - 0.6 * hiBy; cr *= dim; cg *= dim; cb *= dim; }
    else { r = x > 3.4 ? 0.3 + p.rr * 2.3 : 1.5 + p.rr * 0.95; cr = lerp(0.55, 0.45, hiBy); cg = lerp(0.8, 1, hiBy); cb = 1; }
    const a = p.a + Math.PI; setP(epart, i, x, Math.cos(a) * r * (p.i2 ?? 1), -Math.abs(Math.sin(a)) * r * 0.98 + 0.0); setC(epart, i, cr, cg, cb); }); upd(epart); }

// ---- wind streaks + tip vortices (drag scene), jet stream (journey)
const NW = 500, wind = mkPoints(NW, 0.35, 0.8), wr = rng(21), WP = Array.from({ length: NW }, () => ({ y: (wr() - 0.5) * 30, z: (wr() - 0.5) * 60, ph: wr(), v: 0.5 + wr() * 0.5 }));
const NVX = 400, vort = mkPoints(NVX, 0.3, 0.9);
const jet = mkPoints(600, 1.6, 0.9), jr = rng(31), JP = Array.from({ length: 600 }, () => ({ y: (jr() - 0.5) * 26, z: (jr() - 0.5) * 120, ph: jr(), v: 0.6 + jr() * 0.6 }));

// ---- journey world
const WORLD = new THREE.Group(); scene.add(WORLD);
{ const c = document.createElement("canvas"); c.width = c.height = 512; const g = c.getContext("2d"), r = rng(3); g.fillStyle = "#6f8f5a"; g.fillRect(0, 0, 512, 512);
  const cols = ["#7fa062", "#8aa56b", "#9a9a62", "#5f8250", "#b0a676", "#6b8a58", "#84996a"]; for (let i = 0; i < 90; i++) { g.fillStyle = cols[Math.floor(r() * cols.length)]; g.fillRect(Math.floor(r() * 8) * 64, Math.floor(r() * 8) * 64, 64 * (1 + Math.floor(r() * 2)), 64); }
  g.strokeStyle = "rgba(60,80,50,.5)"; g.lineWidth = 2; for (let i = 0; i <= 8; i++) { g.beginPath(); g.moveTo(i * 64, 0); g.lineTo(i * 64, 512); g.moveTo(0, i * 64); g.lineTo(512, i * 64); g.stroke(); }
  const tex = new THREE.CanvasTexture(c); tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(14, 14); tex.anisotropy = 8;
  const gr = new THREE.Mesh(new THREE.PlaneGeometry(9000, 9000), new THREE.MeshStandardMaterial({ map: tex, roughness: 1 })); gr.rotation.x = -Math.PI / 2; gr.position.set(700, -4.3, 0); WORLD.add(gr);
  const rc = document.createElement("canvas"); rc.width = 512; rc.height = 128; const rg = rc.getContext("2d"); rg.fillStyle = "#3a3d44"; rg.fillRect(0, 0, 512, 128); rg.fillStyle = "#e9e9e9"; rg.fillRect(60, 58, 240, 12); rg.fillRect(0, 6, 512, 5); rg.fillRect(0, 117, 512, 5);
  const rtex = new THREE.CanvasTexture(rc); rtex.wrapS = THREE.RepeatWrapping; rtex.repeat.set(30, 1); rtex.anisotropy = 8; WORLD.userData.rtex = rtex;
  [[250, 1100], [1350, 1100]].forEach(([x, L]) => { const rw = new THREE.Mesh(new THREE.PlaneGeometry(L, 46), new THREE.MeshStandardMaterial({ map: rtex, roughness: 0.9 })); rw.rotation.x = -Math.PI / 2; rw.position.set(x, -4.22, 0); WORLD.add(rw); }); }
const SAT = new THREE.Group(); scene.add(SAT);
{ const b = new THREE.Mesh(new THREE.BoxGeometry(5, 5, 7), new THREE.MeshStandardMaterial({ color: COL.gold, metalness: 0.7, roughness: 0.3, emissive: 0x5a3d00 })); SAT.add(b);
  [-1, 1].forEach(s => { const p = new THREE.Mesh(new THREE.BoxGeometry(16, 0.3, 6), new THREE.MeshStandardMaterial({ color: 0x1c3f9a, metalness: 0.6, roughness: 0.3, emissive: 0x0a1a55 })); p.position.x = s * 11; SAT.add(p); });
  const d = new THREE.Mesh(new THREE.ConeGeometry(2.6, 2.2, 20, 1, true), new THREE.MeshStandardMaterial({ color: 0xeeeeee, side: THREE.DoubleSide })); d.position.y = -3.6; SAT.add(d); }
const beam = mkPoints(80, 1.5, 0.9);

// ------------------------------------------------------------------ overlay helpers
const labels = $("#labels"), lines = $("#lines"), LAB = {};
function project(v) { const p = v.clone().project(camera); return [(p.x * 0.5 + 0.5) * W, (-p.y * 0.5 + 0.5) * H, p.z]; }
function lab(key, html, at, o = {}) { let L = LAB[key]; if (!L) { const d = document.createElement("div"); d.className = "lab"; labels.appendChild(d); const ln = document.createElementNS("http://www.w3.org/2000/svg", "line"); ln.setAttribute("stroke", "#d9a93a"); ln.setAttribute("stroke-width", 3); lines.appendChild(ln);
    const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle"); dot.setAttribute("r", 7); dot.setAttribute("fill", "#d9a93a"); lines.appendChild(dot); L = LAB[key] = { d, ln, dot, html: "" }; }
  const op = clamp(o.op ?? 1); L.used = true; if (L.html !== html) { L.d.innerHTML = html; L.html = html; } L.d.className = "lab " + (o.cls || "");
  const [sx, sy] = Array.isArray(at) ? at : project(at), dx = o.dx ?? 0, dy = o.dy ?? 0, w = L.d.offsetWidth, h = L.d.offsetHeight;
  let bx = sx + dx - (dx < 0 ? w : dx === 0 ? w / 2 : 0), by = sy + dy - (dy < 0 ? h : dy === 0 ? h / 2 : 0);
  bx = clamp(bx, 20, W - w - 20); by = clamp(by, 96, 900 - h);
  L.d.style.opacity = op; L.d.style.transform = `translate(${bx.toFixed(1)}px,${by.toFixed(1)}px) scale(${(0.9 + 0.1 * op).toFixed(3)})`;
  const noLine = o.line === false || (dx === 0 && dy === 0), ax = clamp(sx, bx, bx + w), ay = clamp(sy, by, by + h);
  L.ln.setAttribute("x1", sx); L.ln.setAttribute("y1", sy); L.ln.setAttribute("x2", ax); L.ln.setAttribute("y2", ay); L.ln.setAttribute("opacity", noLine ? 0 : op); L.dot.setAttribute("cx", sx); L.dot.setAttribute("cy", sy); L.dot.setAttribute("opacity", noLine ? 0 : op); }
function labelsBegin() { for (const k in LAB) LAB[k].used = false; }
function labelsEnd() { for (const k in LAB) if (!LAB[k].used) { LAB[k].d.style.opacity = 0; LAB[k].ln.setAttribute("opacity", 0); LAB[k].dot.setAttribute("opacity", 0); } }
const OV = {}; function ov(id, html) { const d = document.createElement("div"); d.className = "ov"; d.id = "ov-" + id; d.innerHTML = html; $("#ovs").appendChild(d); OV[id] = d; return d; }
const st = (sel, o) => { const e = typeof sel === "string" ? $(sel) : sel; if (!e) return; if (o.op !== undefined) e.style.opacity = clamp(o.op); if (o.tf !== undefined) e.style.transform = o.tf; };
const rise = (sel, k, dy = 40) => st(sel, { op: k, tf: `translateY(${((1 - k) * dy).toFixed(1)}px)` });
function cam(pos, tgt, fov = 35, shift = 0) { camera.fov = fov; camera.position.copy(pos); camera.up.set(0, 1, 0); camera.lookAt(tgt); if (shift) camera.setViewOffset(W, H, -shift, 0, W, H); else camera.clearViewOffset(); camera.updateProjectionMatrix(); camera.updateMatrixWorld(); }
const orbit = (r, ang, h) => V(Math.cos(ang) * r, h, Math.sin(ang) * r);

// subtitles: split each narration line into chunks, timed by character share
const SUBS = []; TM.scenes.forEach(sc => sc.lines.forEach(l => { const words = l.text.split(" "), chunks = []; let cur = "";
  words.forEach(w => { if ((cur + " " + w).trim().length > 60 || (cur.length > 30 && /[.,?]$/.test(cur))) { chunks.push(cur); cur = w; } else cur = (cur + " " + w).trim(); }); if (cur) chunks.push(cur);
  const tot = chunks.reduce((a, c) => a + c.length, 0); let acc = 0; chunks.forEach(c => { const a = sc.start + l.start + (l.end - l.start) * acc / tot; acc += c.length; SUBS.push({ a, b: sc.start + l.start + (l.end - l.start) * acc / tot + 0.25, text: c }); }); }));
const CH = TM.scenes.filter(s => s.title); $("#dots").innerHTML = CH.map(() => "<i></i>").join("");
const SRC = { hook: "Sources: Airbus (A320neo) · IATA 2026 outlook", forces: "Source: NASA Glenn Research Center", wing: "Source: NASA Glenn Research Center", myth: "Source: NASA Glenn, “Incorrect Lift Theory”", equation: "Source: NASA Glenn, lift equation",
  stall: "Source: NASA Glenn · FAA Pilot's Handbook", engine: "Sources: NASA · CFM International", drag: "Sources: NASA Glenn · Airbus", controls: "Source: NASA Glenn Research Center", parts: "Sources: Airbus · Boeing · CFM International",
  journey: "Sources: ICAO Standard Atmosphere · IMD · ISRO / AAI", recap: "", end: "" };

// ------------------------------------------------------------------ overlays (static markup per scene)
ov("hook", `<div class="huge" id="h1" style="top:150px">79 TONNES</div>
  <div id="h2" style="position:absolute;left:78px;top:310px;font:400 64px var(--disp)">≈ 13 ELEPHANTS<div id="h2d" style="display:flex;gap:10px;margin-top:16px"></div><div class="k" style="margin-top:14px;color:#fff">AIRBUS A320neo · MAX TAKEOFF WEIGHT 79 t · ELEPHANT ≈ 6 t</div></div>
  <div class="huge" id="h3" style="top:150px;font-size:118px">NOTHING<br>HOLDS IT UP.</div>
  <div class="huge" id="h4" style="top:150px;font-size:118px;color:var(--gold)">SO WHY<br>DOESN'T<br>IT FALL?</div>
  <div class="card" id="h5" style="left:70px;top:560px;width:640px"><div class="k">IATA OUTLOOK · 2026</div><h3 style="font-size:60px;margin-top:6px">≈ 5 BILLION</h3><p>passengers expected to fly this year</p></div>`);
$("#h2d").innerHTML = Array.from({ length: 13 }, () => `<i style="width:34px;height:34px;border-radius:9px 9px 14px 14px;background:var(--gold);display:inline-block"></i>`).join("");
ov("forces", `<div class="card" id="f1" style="left:1280px;top:150px;width:580px"><div class="k">BALANCED FLIGHT</div><h3>LIFT = WEIGHT</h3><h3>THRUST = DRAG</h3><p>→ steady, level cruise</p></div>
  <div class="card" id="f2" style="left:1280px;top:420px;width:580px"><div class="k">TO MANOEUVRE</div><p><b>Lift &gt; weight</b> → climb</p><p><b>Thrust &gt; drag</b> → speed up</p><p><b>Tilt the lift</b> → turn</p></div>`);
ov("wing", `<div class="card" id="w1" style="left:60px;top:120px;width:560px"><div class="k">CROSS-SECTION OF A WING</div><h3>THE AIRFOIL</h3><p>Curved top · flatter bottom<br>Rounded front · sharp back</p></div>
  <div class="card" id="w2" style="left:1250px;top:120px;width:610px"><div class="k">NEWTON'S THIRD LAW</div><h3>AIR DOWN → WING UP</h3><p>Every action has an equal and opposite reaction.</p></div>
  <div class="card" id="w3" style="left:560px;top:110px;width:800px;text-align:center"><h3 style="font-size:38px;margin:0">THE WING TURNS THE AIR.<br>THE AIR LIFTS THE WING.</h3></div>`);
ov("myth", `<div class="card" id="m1" style="left:60px;top:120px;width:640px"><div class="k">THE "EQUAL TRANSIT TIME" MYTH</div><h3 id="m1h">"Top air must catch up with bottom air"</h3></div>
  <div id="m2" style="position:absolute;left:1180px;top:140px;transform-origin:50% 50%;border:8px solid #ff4a3a;color:#ff4a3a;border-radius:16px;padding:12px 28px;font:400 60px var(--disp);background:rgba(11,16,32,.8)">INCORRECT<div style="font:700 24px var(--mono);letter-spacing:3px">— NASA GLENN RESEARCH CENTER</div></div>
  <div class="card" id="m3" style="left:1180px;top:340px;width:680px"><div class="k">WHAT REALLY HAPPENS</div><p>Air over the top moves <b>much faster</b> and reaches the trailing edge <b>first</b>.</p><p>The two streams never rejoin.</p></div>`);
ov("equation", `<div id="eq">L = <span id="e4">C<sub style="font-size:.5em">L</sub></span> × <span id="e1">½ρ</span> <span id="e2">V²</span> × <span id="e3">A</span></div><div id="eqcap"></div>
  <div class="card" id="q2" style="left:70px;top:330px;width:560px;height:470px"><div class="k">SPEED IS SQUARED</div>
    <div style="position:absolute;left:60px;right:60px;bottom:86px;height:300px"><div class="bar" id="b1" style="left:30px;background:#9fb0d8"></div><div class="bar" id="b2" style="left:270px"></div></div>
    <p style="position:absolute;left:54px;bottom:20px;width:170px;text-align:center">1× speed<br><b>1× lift</b></p><p style="position:absolute;left:294px;bottom:20px;width:170px;text-align:center">2× speed<br><b>4× lift</b></p></div>
  <div class="card" id="q3" style="left:1340px;top:330px;width:520px"><div class="k">GROUND SPEED</div><h3 style="font-size:110px;margin:0;line-height:1"><span id="spd">0</span></h3><p>km/h &nbsp;·&nbsp; liftoff ≈ <b>270 km/h</b><br>(typical A320-class airliner)</p><p id="q3s" class="pill" style="margin-top:10px">ROTATE</p></div>`);
ov("stall", `<div class="card" id="s1" style="left:1260px;top:120px;width:600px;height:500px"><div class="k">LIFT vs ANGLE OF ATTACK</div>
    <svg viewBox="0 0 600 500" style="position:absolute;inset:0"><line x1="70" y1="420" x2="560" y2="420" stroke="#8fa0c8" stroke-width="3"/><line x1="70" y1="420" x2="70" y2="90" stroke="#8fa0c8" stroke-width="3"/>
    <path id="clp" fill="none" stroke="#d9a93a" stroke-width="6"/><line x1="0" y1="90" x2="0" y2="420" id="cll" stroke="#ff4a3a" stroke-width="3" stroke-dasharray="8 8"/><circle id="cld" r="13" fill="#fff"/>
    <text x="330" y="470" fill="#cfd6e6" font-family="JetBrains Mono" font-size="22" text-anchor="middle">ANGLE OF ATTACK →</text><text x="250" y="80" fill="#ff8a7d" font-family="JetBrains Mono" font-size="22" id="clt">≈ 15° critical angle</text></svg></div>
  <div class="card" id="s2" style="left:60px;top:120px;width:470px"><div class="k">ANGLE OF ATTACK</div><h3 style="font-size:90px;margin:0;line-height:1"><span id="aoa">5</span>°</h3></div>
  <div id="s3" style="position:absolute;left:60px;top:330px;font:400 130px var(--disp);color:#ff4a3a;text-shadow:0 4px 24px rgba(0,0,0,.6)">STALL</div>`);
ov("engine", `<div class="card" id="g1" style="left:60px;top:110px;width:760px"><div class="k">THE SURPRISE</div><h3>MOST AIR NEVER BURNS</h3><p>Fan-driven <b>bypass air</b> generates the <b>bulk of the thrust</b> (NASA).</p><p>Bypass ratio ≈ <b>11 : 1</b> on the CFM LEAP-1A.</p></div>`);
ov("drag", `<div class="card" id="d1" style="left:60px;top:120px;width:560px"><div class="k">STREAMLINING</div><h3>LESS DRAG = LESS FUEL</h3><p>Every surface is shaped so air slides past instead of piling up.</p></div>
  <div class="card" id="d2" style="left:60px;top:400px;width:560px"><div class="k">WINGTIP DEVICES</div><p>Airbus “Sharklets” cut fuel burn by <b>up to 4%</b>.</p></div>`);
ov("controls", `<div class="card" id="c1" style="left:60px;top:120px;width:520px"><div class="k" id="c1k">AXIS</div><h3 id="c1h" style="font-size:64px"></h3><p id="c1p"></p></div>`);
ov("parts", `<div class="card big" id="p1" style="left:50px;top:110px;width:660px"><div class="k" id="pk"></div><h3 id="ph" style="font-size:42px"></h3><div id="pb"></div></div>`);
ov("journey", `<div class="card" id="j0" style="left:48px;top:110px;width:330px"><div class="k" id="jph">PHASE</div><h3 id="jp" style="font-size:44px;margin:4px 0"></h3><div class="k" style="color:#cfd6e6;margin-top:10px">ALTITUDE</div><h3 style="font-size:54px;margin:0;color:#fff"><span id="jalt">0</span><span style="font-size:26px"> ft</span></h3>
    <div style="height:14px;border-radius:8px;background:rgba(255,255,255,.18);margin-top:10px"><div id="jbar" style="height:14px;border-radius:8px;background:var(--gold);width:0"></div></div></div>
  <div class="card jc" id="j1" style="left:1290px;top:110px;width:580px"><div class="k">CRUISE ALTITUDE</div><h3>35,000 ft ≈ 10.7 km</h3><p>Higher than Mount Everest (8.85 km)</p></div>
  <div class="card jc" id="j2" style="left:1290px;top:300px;width:580px"><div class="k">AIR DENSITY · ICAO STANDARD ATMOSPHERE</div><h3>≈ 31% of sea level</h3><div style="height:16px;border-radius:8px;background:rgba(255,255,255,.2)"><div style="height:16px;border-radius:8px;background:var(--gold);width:31%"></div></div><p>Thinner air → less drag → less fuel</p></div>
  <div class="card jc" id="j3" style="left:1290px;top:560px;width:580px"><div class="k">OUTSIDE TEMPERATURE</div><h3>≈ −54 °C</h3><p>Cabin is pressurised and heated</p></div>
  <div class="card jc" id="j4" style="left:1290px;top:110px;width:580px"><div class="k">JET STREAM · IMD, 4 JAN 2026</div><h3>≈ 150 knots</h3><p>(≈ 280 km/h) core winds at <b>12.6 km</b> above northwest India</p><p>Tailwind → shorter flight, less fuel</p></div>
  <div class="card jc" id="j5" style="left:1290px;top:430px;width:580px"><div class="k">NAVIGATION · ISRO + AAI</div><h3>GAGAN</h3><p>GPS-Aided GEO Augmented Navigation: satellite corrections for precise approaches</p><p>Certified for <b>APV-1</b> approaches in 2015</p></div>`);
ov("recap", `<svg viewBox="0 0 1920 1080" id="mm"></svg>
  <div class="node navy" id="n1" style="left:240px;top:290px">ENGINES<small>suck · squeeze · bang · blow</small></div>
  <div class="node" id="n2" style="left:660px;top:290px">THRUST<small>beats drag</small></div>
  <div class="node" id="n3" style="left:1040px;top:290px">SPEED<small>≈ 270 km/h to lift off</small></div>
  <div class="node navy" id="n4" style="left:1450px;top:290px">WINGS<small>turn the air downward</small></div>
  <div class="node" id="n5" style="left:1450px;top:510px;background:var(--gold)">LIFT<small>L = C<sub>L</sub> · ½ρV² · A</small></div>
  <div class="node" id="n6" style="left:1040px;top:510px">&gt; WEIGHT<small>79 tonnes</small></div>
  <div class="node navy" id="n7" style="left:600px;top:510px;font-size:60px">FLIGHT</div>
  <div class="node" id="n8" style="left:300px;top:730px">CONTROL<small>ailerons · elevator · rudder</small></div>
  <div class="node" id="n9" style="left:900px;top:730px">DRAG<small>streamlining · winglets</small></div>
  <div id="n10" style="position:absolute;left:0;right:0;top:110px;text-align:center;font:400 64px var(--disp);text-shadow:0 4px 24px rgba(0,0,30,.7)">NO MAGIC. JUST <span style="color:var(--gold)">AIR</span> AND <span style="color:var(--gold)">PHYSICS</span>.</div>`);
ov("end", `<div id="x0" style="position:absolute;inset:0;background:linear-gradient(#fbf5e9,#f3e7cf)"></div>
  <img id="x1" src="assets/banner.png" style="position:absolute;left:440px;top:56px;width:1040px;height:588px;object-fit:cover;border-radius:20px;box-shadow:0 20px 60px rgba(60,40,0,.3)">
  <div class="btn" id="x2" style="left:560px;top:680px;width:330px;background:var(--navy)"><svg viewBox="0 0 24 24" style="position:static;width:50px;height:50px;vertical-align:-8px;margin-right:12px"><path fill="#fff" d="M2 10h4v11H2zM8 10l4-8c1.7 0 3 1.3 3 3v4h5.2c1.3 0 2.2 1.2 1.9 2.4l-1.7 7.1c-.3 1.4-1.6 2.5-3 2.5H8z"/></svg>LIKE</div>
  <div class="btn" id="x3" style="left:930px;top:680px;width:430px;background:#e02020">SUBSCRIBE</div>
  <div id="x4" style="position:absolute;left:300px;right:300px;top:800px;text-align:center;font:400 19px/1.5 var(--mono);color:#3a3320">SOURCES: NASA Glenn Research Center (Beginner's Guide to Aeronautics) · ICAO Standard Atmosphere · India Meteorological Department (press release, 4 Jan 2026) · ISRO / Airports Authority of India (GAGAN) · IATA 2026 outlook · Airbus · Boeing · CFM International</div>`);
// stall curve
{ let d = ""; for (let a = 0; a <= 20; a += 0.5) { const cl = a <= 15 ? a / 15 : Math.max(0.35, 1 - (a - 15) / 5 * 0.85), x = 70 + a / 20 * 490, y = 420 - cl * 300; d += (a ? "L" : "M") + x + " " + y; } $("#clp").setAttribute("d", d); $("#cll").setAttribute("x1", 70 + 15 / 20 * 490); $("#cll").setAttribute("x2", 70 + 15 / 20 * 490); }

const PARTS = [
  ["nose", "01 · NOSE & COCKPIT", "Radome · weather radar · windshield (6 panes) · flight deck · pitot probes", "Rounded, pointed cone", "White skin · dark tinted glass", "Glass-fibre composite radome (radar passes through) · laminated glass and acrylic windshield"],
  ["fuselage", "02 · FUSELAGE", "Pressure cabin · doors · windows · cargo hold · frames and stringers", "Long tube ≈ 4 m wide, tapering to a tail cone", "White, gold cheatline", "Aluminium alloy (A320) · carbon-fibre composite (787, A350)"],
  ["wings", "03 · WINGS", "Wing box · spars · ribs · skin panels · winglets", "Swept back ≈ 25°, tapered, airfoil section, tips turned up", "Light grey · gold winglets", "Aluminium alloy; carbon-fibre composite on newer jets"],
  ["movables", "04 · MOVING SURFACES", "Slats (front) · flaps (rear) · ailerons (outer) · spoilers (top)", "Thin hinged panels along both wing edges", "Mid grey", "Mostly carbon-fibre composite"],
  ["engines", "05 · ENGINES", "Nacelle · fan · compressor · combustor · turbine · nozzle · pylon", "Barrel; fan ≈ 2 m across (LEAP-1A)", "Navy cowl · silver lip · dark fan", "Carbon-composite fan blades with titanium edges · nickel superalloy turbine"],
  ["tail", "06 · TAIL (EMPENNAGE)", "Vertical fin · rudder · horizontal stabiliser · elevators · APU in tail cone", "Swept fins, like small wings", "Navy fin · gold rudder", "Carbon-fibre composite"],
  ["gear", "07 · LANDING GEAR", "Nose gear (2 wheels) · main gear (2 × 2 wheels) · shock struts · brakes", "Telescopic struts with wheels; folds into the belly", "Silver steel · black tyres", "High-strength steel and titanium · carbon brakes · rubber tyres"],
  ["fuel", "08 · FUEL TANKS", "Left and right wing tanks · centre tank · pumps and pipes", "The hollow inside of the wing itself", "Shown in blue", "Sealed aluminium wing structure · Jet A-1 kerosene, ≈ 24,000 litres (A320)"],
  ["systems", "09 · HIDDEN SYSTEMS", "Hydraulics (3 circuits) · electrical generators · avionics · fly-by-wire computers · air conditioning", "Pipes, cables and boxes under the floor", "Shown in gold, blue and green", "Titanium and steel pipes · copper and aluminium wiring"]];

// ------------------------------------------------------------------ scenes
function baseFly(tg, bob = 1) { A.visible = true; A.position.set(0, Math.sin(tg * 0.9) * 0.35 * bob, 0); A.rotation.set(Math.sin(tg * 0.6) * 0.02 * bob, 0, Math.sin(tg * 0.7) * 0.012 * bob); explode(A, 0); setControls(A, {}); P.fuel.visible = P.systems.visible = false; cloudsFly(tg); P.fans.forEach(f => f.rotation.x = tg * 30); }
const S = {};
S.hook = (t, c, d, tg) => { baseFly(tg); const k = E.io(seg(t, 0, d)); cam(V(lerp(50, 18, k), lerp(-7, 4, k), lerp(34, 62, k)), V(0, 0, 0), 35, 300);
  const o1 = fin(t, 0.3) * (1 - fin(t, c[2] - 0.3)); rise("#h1", E.expo(seg(t, 0.3, 0.9)) * (1 - fin(t, c[2] - 0.3)), 60); rise("#h2", fin(t, c[1]) * (1 - fin(t, c[2] - 0.3)));
  [...$("#h2d").children].forEach((e, i) => e.style.transform = `scale(${pop(t, c[1] + 0.25 + i * 0.07, 0.3)})`);
  rise("#h3", E.expo(seg(t, c[2], c[2] + 0.6)) * (1 - fin(t, c[3] - 0.25)), 60); rise("#h4", E.expo(seg(t, c[3], c[3] + 0.6)) * (1 - fin(t, c[4] - 0.2)), 60); rise("#h5", pop(t, c[4] + 0.3)); $("#h5").style.top = "170px"; };
S.forces = (t, c, d, tg) => { baseFly(tg, 0.5); const un = E.io(seg(t, c[6], c[6] + 2.5)); A.rotation.z += 0.12 * un; A.position.y += 3 * un;
  cam(orbit(82, 1.05 - 0.25 * E.io(seg(t, 0, d)), 16), V(0, 1, 0), 35, -150); const o = A.position.clone();
  const L = (key, cue, org, dir, len, txt, sub, dx, dy) => { const k = E.back(seg(t, cue, cue + 0.6)); setArrow(AR[key], o.clone().add(org), dir, len * k); if (k > 0.3) lab("f" + key, `${txt}<small>${sub}</small>`, o.clone().add(org).addScaledVector(dir.clone().normalize(), len * k), { dx, dy, op: fin(t, cue + 0.2), cls: "big" }); };
  L("weight", c[1], V(0, -2.6, 0), V(0, -1, 0), 15, "WEIGHT", "gravity pulls down", 30, 10); L("lift", c[2], V(0, 2.4, 0), V(0, 1, 0), 15 + 5 * un, "LIFT", "wings push up", 30, -10);
  L("thrust", c[3], V(19.5, 0, 0), V(1, 0, 0), 14, "THRUST", "engines push forward", 20, -40); L("drag", c[4], V(-19.5, 1.5, 0), V(-1, 0, 0), 14, "DRAG", "air resists", -20, -40);
  rise("#f1", pop(t, c[5] + 0.3)); rise("#f2", pop(t, c[6] + 0.3)); };
function rigScene(t, al, flowOn, hi = 0) { A.visible = false; clouds.visible = false; RIG.visible = true; foil.rotation.z = al; drawFlow(t, al, flowOn, hi); skyCol(0x071a48, 0x15306e, 0x2a4a8c); }
S.wing = (t, c, d, tg) => { if (t < c[1]) { baseFly(tg); const k = E.io(seg(t, 0, c[1])); cam(V(lerp(30, 6, k), lerp(16, 7, k), lerp(70, 34, k)), V(lerp(0, -1, k), 0, lerp(0, 9, k))); glow(MATS.wings, 0xc9992e, 0.5 * fin(t, c[0]));
    lab("wg", "THE WING", V(-1.5, 0.2, 10), { dx: 60, dy: -90, op: fin(t, c[0] + 0.3), cls: "big" }); ["#w1", "#w2", "#w3"].forEach(e => rise(e, 0)); return; }
  const al = 0.1; rigScene(t, al, fin(t, c[3] - 0.4, 0.8), fin(t, c[5]));
  const k = E.io(seg(t, c[1], d)); cam(V(lerp(10, 2, k), lerp(4, 2, k), lerp(34, 30, k)), V(-1, -1.6, 0), 38); st("#flash", { op: 1 - seg(t, c[1], c[1] + 0.35) });
  rise("#w1", pop(t, c[1] + 0.4) * (1 - fin(t, c[4] - 0.3)));
  if (t > c[2]) { const o = fin(t, c[2] + 1.6) * (1 - fin(t, c[4])); lab("aoa", "ANGLE OF ATTACK<small>the wing's tilt against the oncoming air</small>", V(5, 0.4, 6), { dx: 40, dy: 120, op: o }); lab("top", "CURVED TOP", V(1.5, 1.35, 6), { dx: -40, dy: -110, op: fin(t, c[2] + 0.3) * (1 - fin(t, c[4])) }); }
  if (t > c[3] && t < c[5]) lab("dw", "AIR IS BENT DOWNWARD<small>this is called downwash</small>", V(-10, -1.6, 0), { dx: -30, dy: 150, op: fin(t, c[3] + 1.2) * (1 - fin(t, c[5] - 0.4)) });
  const n3 = seg(t, c[4], c[4] + 0.8) * (1 - fin(t, c[5] + 0.2)); setArrow(AR.down, V(-9, -1.2, 6.8), V(-0.25, -1, 0), 4.5 * E.back(seg(t, c[4] + 1.6, c[4] + 2.2)) * (t < c[5] + 0.5 ? 1 : 0), 0.5); setArrow(AR.lift, V(0.5, 1.6, 6.8), V(0.05, 1, 0), 5 * E.back(seg(t, c[4] + 3.4, c[4] + 4)), 0.5);
  rise("#w2", pop(t, c[4] + 0.3) * (1 - fin(t, c[5] - 0.2)));
  const pk = fin(t, c[5] + 0.5, 0.8); loP.position.set(0.5, 3.4, 6.2); hiP.position.set(1, -2.6, 6.2); loP.scale.set(15, 5.5, 1); hiP.scale.set(14, 4.5, 1); loP.material.opacity = 0.5 * pk; hiP.material.opacity = 0.45 * pk;
  if (t > c[5]) { lab("lp", "FASTER AIR · LOWER PRESSURE", V(0.5, 3.6, 6.2), { dx: 0, dy: -150, op: fin(t, c[5] + 1.5) * (1 - fin(t, c[6] + 3)) }); lab("hp", "SLOWER AIR · HIGHER PRESSURE", V(1, -2.8, 6.2), { dx: 0, dy: 120, op: fin(t, c[5] + 5.5) * (1 - fin(t, c[6] + 3)) }); lab("lf", "LIFT", V(0.8, 6.8, 6.8), { dx: 40, dy: 0, op: fin(t, c[4] + 3.8), cls: "big" }); }
  rise("#w3", pop(t, c[6] + 2.6)); };
S.myth = (t, c, d) => { const al = 0.09; rigScene(t, al, 0.55); cam(V(3, 2, 31), V(-1, -1.4, 0), 38); rise("#m1", pop(t, 0.3));
  const cyc = t < c[1] ? seg(t, c[0] + 3, c[1] - 0.3) : t < c[2] ? 0 : ((t - c[2]) % 4.2) / 3.6, show = (t > c[0] + 2.6 && t < c[1]) || t > c[2];
  ballT.visible = ballB.visible = show; const myth = t < c[1], uT = clamp(cyc * (myth ? 1 : 1.45)), uB = clamp(cyc * (myth ? 1 : 0.92)), pos = (u, top) => { const x = 5 - 10 * u, ys = afU(clamp(u, 0.001, 0.999)); const y = x * Math.sin(al) + (top ? ys[0] + 0.55 : ys[1] - 0.55) * Math.cos(al); return V(x - (u >= 1 && !myth ? (cyc * 1.45 - 1) * 10 : 0), y, 6.6); };
  ballT.position.copy(pos(uT, 1)); ballB.position.copy(pos(uB, 0)); if (show) { lab("bt", "TOP AIR", ballT.position, { dx: 20, dy: -70 }); lab("bb", "BOTTOM AIR", ballB.position, { dx: 20, dy: 70 }); }
  const sk = seg(t, c[1] + 0.9, c[1] + 1.25); st("#m2", { op: sk > 0 ? 1 : 0, tf: `rotate(-6deg) scale(${lerp(2.2, 1, E.out(sk))})` }); $("#m1h").style.textDecoration = t > c[1] + 1 ? "line-through" : "none"; $("#m1h").style.textDecorationColor = "#ff4a3a"; rise("#m3", pop(t, c[2] + 0.3)); };
S.equation = (t, c, d, tg) => { A.visible = true; clouds.visible = false; explode(A, 0); WORLD.visible = true; skyCol(0x2a6fd0, 0x9fd0f5, 0xe6f3ff);
  const tr = c[3] + 6.2, sp = 270 * E.in(seg(t, 0.5, tr)) ** 0.75, vK = seg(t, 0.5, tr), dist = (() => { let s = 0; const n = 60; for (let i = 0; i < n; i++) { const x = (i + 0.5) / n * t; s += 75 * (E.in(seg(x, 0.5, tr)) ** 0.75 || 0) * (t / n); } return s; })();
  const air = E.io(seg(t, tr, tr + 5)), rot = E.io(seg(t, tr - 0.8, tr + 1.4)); A.position.set(-250 + dist, 55 * air, 0); A.rotation.set(0, 0, 0.19 * rot - 0.05 * air); setControls(A, { flaps: 0.55, gear: 1 - 0.0 * air, elevator: 0.25 * rot * (1 - air) }); P.fans.forEach(f => f.rotation.x = tg * 40); P.fuel.visible = P.systems.visible = false;
  cam(V(A.position.x + lerp(46, 30, vK), lerp(1, 6, vK) + A.position.y * 0.5, 74), V(A.position.x + 4, A.position.y * 0.75 + 1, 0), 35, 0);
  const l1 = TM.scenes.find(s => s.id === "equation").lines[1], f = seg(t, l1.start, l1.end), term = t < c[1] ? 0 : f < 0.34 ? 0 : f < 0.5 ? 1 : f < 0.66 ? 2 : f < 0.8 ? 3 : 4;
  rise("#eq", E.expo(seg(t, c[0] + 0.3, c[0] + 1))); [1, 2, 3, 4].forEach(i => $("#e" + i).classList.toggle("on", term === i && t < c[2]));
  $("#eqcap").textContent = t < c[1] || t > c[2] ? "LIFT EQUATION · NASA GLENN RESEARCH CENTER" : ["L = lift force", "ρ (rho) = AIR DENSITY", "V = SPEED, squared", "A = WING AREA", "C L = LIFT COEFFICIENT (shape + angle)"][term]; st("#eqcap", { op: fin(t, c[0] + 1) });
  rise("#q2", pop(t, c[2] + 0.2) * (1 - fin(t, c[3] + 1.5))); $("#b1").style.height = 75 * E.out(seg(t, c[2] + 0.8, c[2] + 1.4)) + "px"; $("#b2").style.height = 300 * E.out(seg(t, c[2] + 2.2, c[2] + 3.2)) + "px";
  rise("#q3", pop(t, c[3] + 0.3)); $("#spd").textContent = Math.round(sp); st("#q3s", { op: t > tr - 0.6 ? 1 : 0.15 }); };
S.stall = (t, c, d) => { const deg = lerp(5, 18.5, E.io(seg(t, c[1] + 0.5, c[1] + 6.5))), al = deg / 57.3; rigScene(t, al, 1, 0); cam(V(3, 2, 32), V(-1, -1.2, 0), 38, -160);
  const cl = deg <= 15 ? deg / 15 : Math.max(0.35, 1 - (deg - 15) / 5 * 0.85); setArrow(AR.lift, V(0.5, 1.8 + deg * 0.05, 6.8), V(0.05, 1, 0), 1.5 + 4.5 * cl, 0.5);
  rise("#s1", pop(t, 0.3)); rise("#s2", pop(t, 0.5)); $("#aoa").textContent = deg.toFixed(0); $("#cld").setAttribute("cx", 70 + deg / 20 * 490); $("#cld").setAttribute("cy", 420 - cl * 300); st("#clt", { op: fin(t, c[1] + 2) });
  const sk = seg(t, c[2] + 0.4, c[2] + 0.75); st("#s3", { op: sk > 0 ? (0.75 + 0.25 * Math.sin(t * 9)) : 0, tf: `scale(${lerp(1.8, 1, E.out(sk))})` }); if (deg > 15) lab("sep", "AIRFLOW SEPARATES", V(-2, 3.2, 6), { dx: 30, dy: -120, cls: "red", op: fin(t, c[1] + 5.5) }); };
S.engine = (t, c, d) => { A.visible = false; clouds.visible = false; ENG.visible = true; skyCol(0x071a48, 0x15306e, 0x2a4a8c); EM.fanG.rotation.x = t * 7; const hb = fin(t, c[5] + 0.5, 1);
  drawEngine(t, fin(t, 0.4, 1), hb); cam(orbit(17.5, 1.42 - 0.22 * E.io(seg(t, 0, d)), 4.2).add(V(0.3, 0, 0)), V(0.3, -0.9, 0), 36);
  const stg = [["fan", c[1], "1 · SUCK", "the fan pulls air in", V(4.4, 2.4, 0), -1], ["comp", c[2], "2 · SQUEEZE", "compressor packs it tight", V(1.6, 1.1, 0), -1], ["comb", c[3], "3 · BANG", "fuel burns at 1,000 °C+", V(-0.55, 0.95, 0), -1], ["turb", c[4], "4 · BLOW", "hot gas spins the turbine", V(-2.3, 1.0, 0), -1]];
  stg.forEach(([key, cue, a, b, p, s], i) => { const act = t >= cue && (i === 3 ? t < c[5] : t < stg[i + 1][1]); EM[key].forEach(m => { if (key !== "comb") { m.emissive.setHex(0xffb11f); m.emissiveIntensity = act ? 0.75 : 0; } else m.emissiveIntensity = act ? 2.2 : 1.0 + 0.2 * Math.sin(t * 12); });
    if (act) lab("estage", `${a}<small>${b}</small>`, p, { dx: 0, dy: -170, op: fin(t, cue + 0.1, 0.25), cls: "big" }); });
  if (t > c[5]) { lab("by", "BYPASS AIR (cool)", V(1, -2.0, -1.0), { dx: 60, dy: 110, op: fin(t, c[5] + 1) }); lab("co", "CORE AIR (hot)", V(-5.6, 0.2, 0), { dx: -20, dy: 130, op: fin(t, c[5] + 1.6) }); }
  rise("#g1", pop(t, c[5] + 2.2)); };
S.drag = (t, c, d, tg) => { baseFly(tg); const k = E.io(seg(t, c[2] - 0.6, c[2] + 2)); cam(V(lerp(62, -40, k), lerp(8, 10, k), lerp(46, 40, k)), V(lerp(0, -6, k), lerp(0, 2, k), lerp(0, 15, k)), 35, lerp(220, 240, k));
  wind.visible = true; WP.forEach((p, i) => { const x = 60 - ((p.ph * 130 + tg * 70 * p.v) % 130); const rr = Math.hypot(p.y, p.z); const push = rr < 6 && Math.abs(x) < 22 ? 6 / Math.max(rr, 1.5) : 1; setP(wind, i, x, p.y * push, p.z * (rr < 6 ? push : 1)); setC(wind, i, 1, 0.86, 0.45); }); upd(wind);
  rise("#d1", pop(t, 0.4)); const o1 = fin(t, c[1] + 0.2) * (1 - fin(t, c[2] - 0.5));
  if (t > c[1] && t < c[2]) { lab("dn", "ROUNDED NOSE", V(18.6, -0.3, 0), { dx: -40, dy: -130, op: o1 }); lab("ds", "SMOOTH SKIN", V(6, 1.9, 0.6), { dx: 30, dy: -160, op: fin(t, c[1] + 1.3) * (1 - fin(t, c[2] - 0.5)) }); lab("dw", "SWEPT WINGS ≈ 25°", V(-2.5, 0.2, 12), { dx: 60, dy: 130, op: fin(t, c[1] + 2.4) * (1 - fin(t, c[2] - 0.5)) }); }
  const vk = fin(t, c[2] + 1, 1.2); vort.visible = vk > 0; vort.material.opacity = 0.9 * vk; for (let i = 0; i < NVX; i++) { const s = i % 2 ? 1 : -1, u = ((i / NVX) + tg * 0.35) % 1, a = u * 40 + i, r = 0.3 + u * 2.6; setP(vort, i, -6 - u * 55, 2.2 + Math.cos(a) * r, s * (17.6 + Math.sin(a) * r)); setC(vort, i, 1, 0.8, 0.35); } upd(vort);
  if (t > c[2]) { glow([P.wingR.children[1].material], 0xffb11f, 0.6 * fin(t, c[2] + 0.5)); lab("wl", "WINGLET<small>weakens the tip vortex</small>", V(-5.4, 2.6, 17.5), { dx: -50, dy: -120, op: fin(t, c[2] + 1.2), cls: "big" }); lab("vx", "WINGTIP VORTEX", V(-20, 2.4, 18), { dx: 40, dy: 130, op: fin(t, c[2] + 2.6) }); rise("#d2", pop(t, c[2] + 3.2)); } else rise("#d2", 0); };
S.controls = (t, c, d, tg) => { baseFly(tg, 0.3); const ph = t < c[1] ? 0 : t < c[2] ? 1 : t < c[3] ? 2 : t < c[4] ? 3 : t < c[5] ? 4 : 5, wob = (a, b) => Math.sin(seg(t, a + 0.6, b) * Math.PI * 2) * E.out(seg(t, a + 0.3, a + 1));
  const roll = ph === 1 ? wob(c[1], c[2]) : 0, pit = ph === 2 ? wob(c[2], c[3]) : 0, yaw = ph === 3 ? wob(c[3], c[4]) : 0, fl = E.io(seg(t, c[4] + 0.6, c[4] + 3.5)), spk = E.io(seg(t, c[5] + 1.2, c[5] + 2.2));
  A.rotation.x += roll * 0.32; A.rotation.z += pit * 0.2; A.rotation.y += yaw * 0.22; setControls(A, { aileron: roll * 0.42, elevator: pit * 0.42, rudder: -yaw * 0.45, flaps: fl, spoilers: spk });
  const wk = E.io(seg(t, c[4] - 0.3, c[4] + 1.6)); cam(V(lerp(-62, -34, wk), lerp(24, 15, wk), lerp(34, 46, wk)), V(lerp(0, -1, wk), 0, lerp(0, 8, wk)), 35, lerp(230, 280, wk));
  glow(ailM, 0xffb11f, ph === 1 ? 0.9 : 0); glow(P.tailMats, 0xffb11f, ph === 2 ? 0.9 : 0); glow([P.rudMat], 0xffb11f, ph === 3 ? 0.8 : 0); glow(flapM.concat(slatM), 0xffb11f, ph === 4 ? 0.7 : 0); glow(spoilM, 0xff5a1f, ph === 5 ? 0.9 * spk : 0);
  const info = [["", "CONTROL SURFACES", "Hinged panels on the wings and tail"], ["LONGITUDINAL AXIS", "ROLL", "Ailerons move in opposite directions: one wing gains lift, the other loses it"], ["LATERAL AXIS", "PITCH", "The elevator pushes the tail down or up, raising or lowering the nose"], ["VERTICAL AXIS", "YAW", "The rudder pushes the tail sideways, swinging the nose left or right"],
    ["HIGH-LIFT DEVICES", "FLAPS + SLATS", "A bigger, more curved wing: more lift at low speed for takeoff and landing"], ["AFTER TOUCHDOWN", "SPOILERS", "Panels rise from the wing top to dump lift and put weight on the wheels"]][ph];
  $("#c1k").textContent = info[0] || "STEERING"; $("#c1h").textContent = info[1]; $("#c1p").textContent = info[2]; rise("#c1", pop(t, c[ph] + 0.2, 0.35));
  if (ph === 1) lab("ca", "AILERON", V(-5.6, 0.6, 14.5), { dx: 60, dy: 110 }); if (ph === 2) lab("ce", "ELEVATOR", V(-17.3, 1.3, 3.6), { dx: -40, dy: 120 }); if (ph === 3) lab("cr", "RUDDER", V(-17.4, 5.5, 0), { dx: -60, dy: -90 });
  if (ph === 4) { lab("cf", "FLAPS", V(-4.6, -0.6, 8), { dx: -40, dy: 130, op: fl }); lab("cs", "SLATS", V(-0.5, 0.1, 10), { dx: 70, dy: -120, op: fl }); } if (ph === 5) lab("cp", "SPOILERS", V(-2.6, 0.9, 9.3), { dx: 60, dy: -130, op: spk }); };
S.parts = (t, c, d, tg) => { A.visible = true; A.position.set(0, 0, 0); A.rotation.set(0, 0, 0); clouds.visible = false; skyCol(0x071a48, 0x15306e, 0x2a4a8c); const ex = E.io(seg(t, 0.4, 3.2)); explode(A, ex); P.fuel.visible = P.systems.visible = ex > 0.5; setControls(A, { gear: 1, flaps: 0.3 }); P.fans.forEach(f => f.rotation.x = tg * 6);
  cam(orbit(84, 0.85 + 0.55 * seg(t, 0, d), 36), V(0, 0.5, 0), 35, 330);
  let idx = -1; for (let i = 1; i <= 9; i++) if (t >= c[i]) idx = i - 1; const last = t >= c[10];
  if (idx >= 0 && !last) { const p = PARTS[idx], k = fin(t, c[idx + 1], 0.5); glow(MATS[p[0]], p[0] === "fuel" ? 0x3a8cff : 0xd9a93a, (p[0] === "systems" ? 1.6 : 0.85) * k);
    $("#pk").textContent = "SECTION " + p[1].slice(0, 2) + " OF 09"; $("#ph").textContent = p[1].slice(5);
    $("#pb").innerHTML = `<p class="k" style="margin-top:14px">PARTS</p><p>${p[2]}</p><p class="k" style="margin-top:14px">SHAPE</p><p>${p[3]}</p><p class="k" style="margin-top:14px">COLOUR</p><p>${p[4]}</p><p class="k" style="margin-top:14px">MATERIAL</p><p>${p[5]}</p>`; rise("#p1", pop(t, c[idx + 1], 0.35)); }
  else if (last) { $("#pk").textContent = "MATERIALS · BOEING 787 AIRFRAME, BY WEIGHT"; $("#ph").textContent = "HALF IS CARBON FIBRE"; const rows = [["Carbon-fibre composite", 50, "#d9a93a"], ["Aluminium", 20, "#b9c0c9"], ["Titanium", 15, "#8fa0c8"], ["Steel", 10, "#6f7a8c"], ["Other", 5, "#4a5468"]];
    $("#pb").innerHTML = rows.map(([n, v, col], i) => `<p style="margin-top:20px">${n} <b style="float:right">${v}%</b></p><div style="height:22px;border-radius:8px;background:rgba(255,255,255,.14)"><div style="height:22px;border-radius:8px;background:${col};width:${v * 2 * E.out(seg(t, c[10] + 0.5 + i * 0.25, c[10] + 1.3 + i * 0.25))}%"></div></div>`).join(""); rise("#p1", 1); }
  else { $("#pk").textContent = "EXPLODED VIEW"; $("#ph").textContent = "9 SECTIONS"; $("#pb").innerHTML = "<p>Every visible part of an airliner, grouped by what it does.</p>"; rise("#p1", pop(t, 0.6)); } };
S.journey = (t, c, d, tg) => { A.visible = true; explode(A, 0); P.fuel.visible = P.systems.visible = false; WORLD.visible = true; cloudsWorld(); P.fans.forEach(f => f.rotation.x = tg * 40);
  const tLift = c[1] + 0.62 * (c[2] - c[1]), tTop = c[3] + 2.5, tDes = c[8] + 0.6, tTd = c[9] + 0.5 * (d - c[9]), TDX = 1320;
  let X, Y; if (t < tLift) { X = 150 * E.in(seg(t, c[1] + 0.8, tLift)) ** 0.8; Y = 0; } else if (t < tTop) { const k = seg(t, tLift, tTop); X = 150 + 400 * k; Y = 220 * E.io(k); } else if (t < tDes) { X = 550 + 330 * seg(t, tTop, tDes); Y = 220; }
  else if (t < tTd) { const k = seg(t, tDes, tTd); X = 880 + (TDX - 880) * k; Y = 220 * (1 - E.io(k)); } else { X = TDX + 190 * E.out(seg(t, tTd, d + 1.5)); Y = 0; }
  const e = 0.05, slope = (() => { const f = tt => { if (tt < tLift) return 0; if (tt < tTop) { const k = seg(tt, tLift, tTop); return 220 * E.io(k) / 1; } if (tt < tDes) return 220; if (tt < tTd) return 220 * (1 - E.io(seg(tt, tDes, tTd))); return 0; }; return (f(t + e) - f(t - e)) / (2 * e); })();
  const rot = E.io(seg(t, tLift - 1.2, tLift + 0.6)) * (1 - seg(t, tLift + 0.6, tLift + 5)), flare = Math.sin(seg(t, tTd - 2.2, tTd + 0.8) * Math.PI) * 0.09;
  A.position.set(X, Y, 0); A.rotation.set(0, 0, clamp(slope * 0.012, -0.12, 0.2) + rot * 0.14 + flare);
  const gearK = t < tLift + 2 ? 1 : t < tDes ? 1 - seg(t, tLift + 2, tLift + 5) : seg(t, tTd - 9, tTd - 6), flK = t < tLift + 4 ? 0.55 : t < tDes ? 0.55 * (1 - seg(t, tLift + 4, tLift + 9)) : seg(t, tDes + 2, tTd - 4);
  setControls(A, { flaps: flK, gear: gearK, spoilers: E.out(seg(t, tTd + 0.6, tTd + 1.4)) });
  const altK = Y / 220; skyCol(altK > 0.5 ? 0x08245f : 0x2a6fd0, altK > 0.5 ? 0x5ea4e8 : 0x9fd0f5, 0xe6f3ff);
  const far = E.io(seg(t, tLift + 1, tTop)) * (1 - E.io(seg(t, tDes + 4, tTd - 2))); cam(V(X + lerp(26, 14, far), Y + lerp(3, 10, far), lerp(74, 104, far)), V(X + lerp(2, 4, far), Y + lerp(3, 3, far), 0), 35, lerp(0, 90, far));
  const phase = t < c[1] ? "READY" : t < tLift + 1.5 ? "TAKEOFF" : t < tTop ? "CLIMB" : t < tDes ? "CRUISE" : t < tTd - 6 ? "DESCENT" : "LANDING"; $("#jp").textContent = phase; $("#jalt").textContent = (Math.round(altK * 350) * 100).toLocaleString("en-US"); $("#jbar").style.width = altK * 100 + "%"; rise("#j0", pop(t, 0.4));
  const off = 1 - fin(t, c[5] - 0.5); rise("#j1", pop(t, c[2] + 2.2) * off); rise("#j2", pop(t, c[3] + 2.4) * off); rise("#j3", pop(t, c[4] + 0.6) * off);
  const off2 = 1 - fin(t, c[8] - 0.2); rise("#j4", pop(t, c[5] + 1.4) * off2); rise("#j5", pop(t, c[7] + 0.6) * off2);
  const jk = fin(t, c[5] + 0.3, 1) * (1 - fin(t, c[7] - 0.3, 1)); jet.visible = jk > 0; jet.material.opacity = 0.85 * jk; JP.forEach((p, i) => { const x = X - 170 + ((p.ph * 340 + tg * 150 * p.v) % 340); setP(jet, i, x, Y + 10 + p.y, p.z - 20); setC(jet, i, 1, 0.82, 0.35); }); upd(jet);
  if (jk > 0.5) lab("js", "JET STREAM →", V(X + 6, Y + 20, -20), { dx: 0, dy: -40, op: jk, cls: "big", line: false });
  const sk = fin(t, c[7] + 0.2, 0.8) * (1 - fin(t, c[8] - 0.2)); SAT.visible = sk > 0; SAT.position.set(X + 2, Y + 30, -30); SAT.rotation.set(0.3, tg * 0.2, 0.2); SAT.scale.setScalar(sk); beam.visible = sk > 0.5;
  for (let i = 0; i < 80; i++) { const u = ((i / 80) + tg * 0.5) % 1; setP(beam, i, lerp(SAT.position.x, X, u), lerp(SAT.position.y - 4, Y + 2, u), lerp(-30, 0, u)); setC(beam, i, 0.5, 1, 0.6); } upd(beam);
  if (sk > 0.5) lab("gs", "GAGAN SATELLITE", SAT.position, { dx: -60, dy: -50, op: sk });
  if (phase === "TAKEOFF" && t > tLift - 1.5) lab("jr", "LIFT > WEIGHT", V(X, Y + 6, 0), { dx: 60, dy: -110, op: fin(t, tLift - 1), cls: "big" });
  if (phase === "LANDING" && t > tTd + 0.6) lab("jl", "SPOILERS UP · REVERSE THRUST · BRAKES", V(X - 4, Y + 2, 6), { dx: 40, dy: -150, op: fin(t, tTd + 0.8) }); };
S.recap = (t, c, d, tg) => { baseFly(tg); cam(V(34, 9, 78), V(0, 0, 0), 35, 0); st("#veil", { op: 0.62 * fin(t, 0.2, 0.8) });
  const cue = [c[1], c[1] + 1.1, c[1] + 2.3, c[2] + 0.9, c[2] + 1.9, c[3] + 0.6, c[3] + 1.8, c[4] + 0.2, c[4] + 0.6]; cue.forEach((q, i) => st("#n" + (i + 1), { op: seg(t, q, q + 0.2), tf: `translate(-50%,-50%) scale(${pop(t, q, 0.4)})` })); rise("#n10", pop(t, c[4] + 0.2));
  const N = [[240, 290], [660, 290], [1040, 290], [1450, 290], [1450, 510], [1040, 510], [600, 510], [300, 730], [900, 730]], links = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [7, 6], [8, 6]];
  $("#mm").innerHTML = links.map(([a, b], i) => { const k = E.io(seg(t, cue[Math.max(a, b)] - 0.5, cue[Math.max(a, b)])); const [x1, y1] = N[a], [x2, y2] = N[b]; return `<line x1="${x1}" y1="${y1}" x2="${lerp(x1, x2, k)}" y2="${lerp(y1, y2, k)}" stroke="#d9a93a" stroke-width="7" stroke-linecap="round" opacity="${k > 0 ? 1 : 0}"/>`; }).join(""); };
S.end = (t, c, d, tg) => { baseFly(tg); cam(V(34, 9, 78), V(0, 0, 0)); st("#x0", { op: fin(t, 0, 0.6) }); st("#x1", { op: fin(t, 0.4), tf: `scale(${lerp(0.9, 1, E.out(seg(t, 0.4, 1.4)))})` });
  const pr = (a) => 1 - 0.1 * Math.sin(seg(t, a, a + 0.35) * Math.PI); st("#x2", { op: 1, tf: `scale(${pop(t, c[0] + 1.6) * pr(c[0] + 3)})` }); st("#x3", { op: 1, tf: `scale(${pop(t, c[0] + 2.4) * pr(c[0] + 4.2) * (1 + 0.03 * Math.sin(t * 5) * seg(t, 6, 7))})` });
  $("#x2").style.background = t > c[0] + 3.15 ? "#1f6fff" : "#0f2557"; $("#x3").textContent = t > c[0] + 4.4 ? "SUBSCRIBED ✓" : "SUBSCRIBE"; $("#x3").style.background = t > c[0] + 4.4 ? "#555" : "#e02020"; rise("#x4", fin(t, 2)); };

// ------------------------------------------------------------------ frame
window.DUR = TM.total;
window.renderAt = function (tg) { tg = clamp(tg, 0, TM.total - 0.001); let sc = TM.scenes[0]; for (const s of TM.scenes) if (tg >= s.start) sc = s; const t = tg - sc.start, c = sc.lines.map(l => l.start);
  // reset shared state
  clouds.visible = true; RIG.visible = ENG.visible = WORLD.visible = SAT.visible = false; [flow, epart, wind, vort, jet, beam].forEach(p => p.visible = false); ballT.visible = ballB.visible = false; loP.material.opacity = hiP.material.opacity = 0;
  for (const k in AR) AR[k].visible = false; resetGlow(); skyCol(0x0b2f7a, 0x6fb1ee, 0xdff0ff); st("#veil", { op: 0 }); st("#flash", { op: 0 }); labelsBegin();
  for (const id in OV) OV[id].style.display = id === sc.id ? "block" : "none";
  S[sc.id](t, c, sc.dur, tg);
  labelsEnd();
  // chrome
  const ci = CH.indexOf(sc); $("#chip").style.opacity = sc.title ? fin(t, 0.15) : 0; if (sc.title) { $("#chip b").textContent = String(ci + 1).padStart(2, "0"); $("#chip span").textContent = sc.title.toUpperCase(); }
  $("#src").textContent = SRC[sc.id] || ""; $("#src").style.opacity = SRC[sc.id] ? fin(t, 0.6) : 0; $("#prog").style.width = (tg / TM.total * 100) + "%"; [...$("#dots").children].forEach((e, i) => e.classList.toggle("on", ci >= 0 ? i <= ci : sc.id === "end"));
  $("#dots").style.opacity = sc.id === "hook" || sc.id === "end" ? 0 : 1; $("#chip span").style.color = $("#src").style.color = "";
  const su = SUBS.find(s => tg >= s.a && tg < s.b), el = $("#sub span"); if (su) { if (el.textContent !== su.text) el.textContent = su.text; el.style.opacity = 1; } else el.style.opacity = 0;
  // transition flash between scenes
  const edge = Math.min(t, sc.dur - t); if (edge < 0.18 && tg > 0.2 && sc.id !== "end") st("#flash", { op: Math.max(parseFloat($("#flash").style.opacity) || 0, (1 - edge / 0.18) * 0.85) });
  renderer.render(scene, camera);
};
const fit = () => { const k = Math.min(innerWidth / W, innerHeight / H); $("#root").style.transform = k < 1 ? `scale(${k})` : ""; $("#root").style.transformOrigin = "0 0"; };
if (!Q.has("raw")) { fit(); addEventListener("resize", fit); }
await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => 0)));
renderAt(parseFloat(Q.get("t")) || 0); window.READY = true;
if (Q.has("play")) { const s0 = performance.now(), t0 = parseFloat(Q.get("t")) || 0; const loop = () => { renderAt((t0 + (performance.now() - s0) / 1000) % TM.total); requestAnimationFrame(loop); }; loop(); }
