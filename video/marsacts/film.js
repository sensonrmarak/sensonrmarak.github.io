// Mars video, main film after the cold open: eleven 3D scenes timed to the narration. renderAt(t) poses everything from t.
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { BokehPass } from "three/addons/postprocessing/BokehPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { Lensflare, LensflareElement } from "three/addons/objects/Lensflare.js";
import { Reflector } from "three/addons/objects/Reflector.js";


const W = 1920, H = 1080, Q = new URLSearchParams(location.search), PR = parseFloat(Q.get("pr")) || 1, FPS = parseFloat(Q.get("fps")) || 30, MB = parseInt(Q.get("mb") || "1");
await Promise.all(["900 120px Body", "700 30px Body", "700 44px Body", "900 96px Body"].map(f => document.fonts.load(f)));
const TM = await (await fetch("timings.json")).json();
const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x), lerp = (a, b, k) => a + (b - a) * k, seg = (t, a, b) => clamp((t - a) / (b - a));
const E = { out: x => 1 - (1 - x) ** 3, in: x => x ** 3, io: x => (x < 0.5 ? 4 * x ** 3 : 1 - (-2 * x + 2) ** 3 / 2), back: x => { const k = 1.70158; return 1 + (k + 1) * (x - 1) ** 3 + k * (x - 1) ** 2; } };
const fin = (t, a, d = 0.5) => E.out(seg(t, a, a + d)), pop = (t, a, d = 0.5) => E.back(seg(t, a, a + d));
function rng(seed) { let s = seed >>> 0; return () => { s = (s + 0x6d2b79f5) | 0; let x = Math.imul(s ^ (s >>> 15), 1 | s); x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x; return ((x ^ (x >>> 14)) >>> 0) / 4294967296; }; }
const $ = s => document.querySelector(s), V = (x, y, z) => new THREE.Vector3(x, y, z), D2R = Math.PI / 180;

// ---------------------------------------------------------------- noise
const PERM = (() => { const r = rng(42), p = Array.from({ length: 256 }, (_, i) => i); for (let i = 255; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [p[i], p[j]] = [p[j], p[i]]; } return Uint8Array.from([...p, ...p]); })();
const fade = t => t * t * (3 - 2 * t), hash = (x, y, z) => PERM[(PERM[(PERM[x & 255] + y) & 255] + z) & 255] / 255;
function vnoise(x, y, z) { const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), xf = fade(x - xi), yf = fade(y - yi), zf = fade(z - zi), l = (a, b, k) => a + (b - a) * k, h = (dx, dy, dz) => hash(xi + dx, yi + dy, zi + dz);
  return l(l(l(h(0, 0, 0), h(1, 0, 0), xf), l(h(0, 1, 0), h(1, 1, 0), xf), yf), l(l(h(0, 0, 1), h(1, 0, 1), xf), l(h(0, 1, 1), h(1, 1, 1), xf), yf), zf); }
function fbm(x, y, z, oct = 6) { let s = 0, a = 0.5, f = 1; for (let i = 0; i < oct; i++) { s += a * vnoise(x * f, y * f, z * f); f *= 2.03; a *= 0.5; } return s; }
const unit = (latD, lonD) => [Math.cos(latD * D2R) * Math.cos(lonD * D2R), Math.sin(latD * D2R), Math.cos(latD * D2R) * Math.sin(lonD * D2R)];
const angd = (x, y, z, u) => Math.acos(clamp(x * u[0] + y * u[1] + z * u[2], -1, 1));

// ---------------------------------------------------------------- equirectangular texture builder
function equi(w, h, shade, maps = 2) { const cvs = Array.from({ length: maps }, () => { const cv = document.createElement("canvas"); cv.width = w; cv.height = h; return cv; }), ids = cvs.map(cv => cv.getContext("2d").createImageData(w, h));
  for (let j = 0; j < h; j++) { const lat = (0.5 - j / h) * Math.PI, cl = Math.cos(lat), sl = Math.sin(lat);
    for (let i = 0; i < w; i++) { const lon = (i / w) * 2 * Math.PI, x = cl * Math.cos(lon), y = sl, z = cl * Math.sin(lon), out = shade(x, y, z, lat, lon), k = (j * w + i) * 4;
      for (let m = 0; m < maps; m++) { const o = out[m]; ids[m].data[k] = o[0]; ids[m].data[k + 1] = o[1]; ids[m].data[k + 2] = o[2]; ids[m].data[k + 3] = o[3] ?? 255; } } }
  return cvs.map((cv, m) => { cv.getContext("2d").putImageData(ids[m], 0, 0); const t = new THREE.CanvasTexture(cv); t.anisotropy = 8; return t; }); }

// ---------------------------------------------------------------- Mars with its real landmarks at their real positions (planetocentric latitude, east longitude)
const F = { olym: unit(18.65, 226.2), arsia: unit(-8.3, 239.1), pavo: unit(1.5, 247.0), ascr: unit(11.9, 255.9), thar: unit(1, 252), hellas: unit(-42.4, 70.5), syrtis: unit(8.4, 69.5), acid: unit(46, 330), argyre: unit(-49.7, 316) };
const VM = Array.from({ length: 40 }, (_, i) => { const u = i / 39; return unit(-7 - 6 * u + Math.sin(u * 9) * 0.8, 262 + 58 * u); });   // Valles Marineris polyline
const CRT = (() => { const r = rng(9), list = []; for (let i = 0; i < 420; i++) { const u = r() * 2 - 1, lat = Math.asin(u) / D2R, lon = r() * 360; if (lat > 25 && r() < 0.75) continue; list.push([...unit(lat, lon), 0.006 + r() ** 3 * 0.06]); } return list; })();
const GRID = new Map(); CRT.forEach((cr, i) => { const lat = Math.asin(cr[1]) / D2R, lon = (Math.atan2(cr[2], cr[0]) / D2R + 360) % 360; const k = Math.floor((lat + 90) / 10) * 100 + Math.floor(lon / 10); if (!GRID.has(k)) GRID.set(k, []); GRID.get(k).push(i); });
function marsShade(x, y, z, lat, lon) {
  const latD = lat / D2R, lonD = lon / D2R, n = fbm(x * 2.4 + 7, y * 2.4, z * 2.4, 6), d = fbm(x * 9 + 3, y * 9, z * 9, 4);
  const north = clamp((latD - 18 + (n - 0.5) * 30) / 14);                                                   // smooth northern lowlands
  let hgt = 0.55 - north * 0.25 + (n - 0.5) * 0.3, alb = 0.55 + (n - 0.5) * 0.5 - north * 0.12;
  const tharsis = Math.exp(-((angd(x, y, z, F.thar) / 0.45) ** 2)); hgt += tharsis * 0.25; alb += tharsis * 0.1;
  for (const [u, r, h] of [[F.olym, 0.1, 0.55], [F.arsia, 0.045, 0.35], [F.pavo, 0.04, 0.33], [F.ascr, 0.045, 0.35]]) { const a = angd(x, y, z, u) / r; if (a < 1.6) { hgt += h * Math.exp(-a * a * 1.2); alb += 0.12 * Math.exp(-a * a); if (a < 0.22) hgt -= 0.15 * (1 - a / 0.22), alb -= 0.15; if (Math.abs(a - 1.05) < 0.08) alb -= 0.12; } }
  let vm = 9; for (let i = 0; i < VM.length - 1; i += 1) vm = Math.min(vm, angd(x, y, z, VM[i])); const canyon = Math.exp(-((vm / 0.018) ** 2)) + 0.4 * Math.exp(-((vm / 0.045) ** 2)) * (fbm(x * 30, y * 30, z * 30, 2) > 0.5 ? 1 : 0.4); hgt -= canyon * 0.35; alb -= canyon * 0.25;
  const hel = angd(x, y, z, F.hellas) / 0.34; if (hel < 1.3) { hgt -= 0.35 * Math.exp(-hel * hel * 2); alb += 0.18 * Math.exp(-hel * hel * 1.5); }
  const arg = angd(x, y, z, F.argyre) / 0.15; if (arg < 1.4) { hgt -= 0.25 * Math.exp(-arg * arg * 2); alb += 0.1 * Math.exp(-arg * arg); }
  const syr = Math.exp(-((angd(x, y, z, F.syrtis) / 0.16) ** 2) * (1 + (d - 0.5))), aci = Math.exp(-((angd(x, y, z, F.acid) / 0.25) ** 2)); alb -= syr * 0.35 + aci * 0.2;
  let cr = 0; { const k0 = Math.floor((latD + 90) / 10), k1 = Math.floor(((lonD % 360) + 360) % 360 / 10); for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) { const list = GRID.get((k0 + a) * 100 + ((k1 + b + 36) % 36)); if (!list) continue;
      for (const i of list) { const [cx, cy, cz, s] = CRT[i], dd = Math.hypot(x - cx, y - cy, z - cz); if (dd < s * 1.7) { const q = dd / s; cr += q < 1 ? -0.55 * (1 - q * q) : 0.4 * Math.exp(-((q - 1.12) ** 2) * 20); } } } }
  hgt += cr * 0.25; alb += cr * 0.08 + (d - 0.5) * 0.18;
  let r = lerp(96, 222, alb), g = lerp(42, 120, alb), b = lerp(28, 74, alb);
  const ncap = clamp((latD - 79 + (fbm(x * 9, y * 9, z * 9, 3) - 0.5) * 9) / 2.5), scap = clamp((-latD - 84 + (fbm(x * 9 + 5, y * 9, z * 9, 3) - 0.5) * 6) / 2), cap = Math.max(ncap, scap);
  r = lerp(r, 246, cap); g = lerp(g, 240, cap); b = lerp(b, 236, cap);
  const H8 = clamp(128 + (hgt - 0.5) * 220, 0, 255); return [[clamp(r, 0, 255), clamp(g, 0, 255), clamp(b, 0, 255)], [H8, H8, H8]]; }
function earthShade(x, y, z, lat) { const n = fbm(x * 1.7 + 2, y * 1.7, z * 1.7, 7), land = n > 0.53, latD = Math.abs(lat / D2R), m = fbm(x * 6, y * 6, z * 6, 4);
  let day, night = [0, 0, 0];
  if (latD > 72) day = [236, 240, 246]; else if (!land) { const dp = clamp((0.53 - n) * 5); day = [lerp(28, 8, dp), lerp(86, 32, dp), lerp(156, 96, dp)]; }
  else { const desert = latD < 35 && latD > 12 && m > 0.45; day = desert ? [196, 166, 112] : [lerp(44, 104, m), lerp(96, 124, m), lerp(46, 66, m)];
    const city = fbm(x * 60, y * 60, z * 60, 2); if (city > 0.62 && latD < 60) { const v = (city - 0.62) * 900; night = [Math.min(255, v), Math.min(255, v * 0.78), Math.min(255, v * 0.45)]; } }
  return [day, night]; }
const cloudShade = (x, y, z) => { const n = fbm(x * 3 + 11, y * 3.6, z * 3, 7), v = clamp((n - 0.5) * 3.4) * 255; return [[255, 255, 255, v]]; };
// spacecraft surfaces: crinkled foil with seams and tape (colour + normal), solar cells, ribbed dish
function foilMaps(base, seam) { const N = 512, hc = document.createElement("canvas"); hc.width = hc.height = N; const hx = hc.getContext("2d"), r = rng(31);
  hx.fillStyle = "#808080"; hx.fillRect(0, 0, N, N); hx.globalAlpha = 0.18; for (let i = 0; i < 900; i++) { const x = r() * N, y = r() * N, a = r() * 3.14, l = 20 + r() * 90; hx.strokeStyle = r() < 0.5 ? "#fff" : "#000"; hx.lineWidth = 1 + r() * 3; hx.beginPath(); hx.moveTo(x, y); hx.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); hx.stroke(); }
  hx.globalAlpha = 1; const hd = hx.getImageData(0, 0, N, N).data, cc = document.createElement("canvas"), nc = document.createElement("canvas"); cc.width = cc.height = nc.width = nc.height = N; const cx = cc.getContext("2d"), cd = cx.createImageData(N, N), nd = nc.getContext("2d").createImageData(N, N);
  const Hh = (i, j) => hd[(((j + N) % N) * N + ((i + N) % N)) * 4] / 255;
  for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) { const k = (j * N + i) * 4, dx = (Hh(i + 1, j) - Hh(i - 1, j)) * 3, dy = (Hh(i, j + 1) - Hh(i, j - 1)) * 3, s = 1 / Math.hypot(dx, dy, 1);
    nd.data[k] = 128 - dx * s * 127; nd.data[k + 1] = 128 - dy * s * 127; nd.data[k + 2] = s * 255; nd.data[k + 3] = 255; const v = 0.82 + Hh(i, j) * 0.36, sm = (i % 171 < 4 || j % 171 < 4) ? 1 : 0, tape = (Math.abs((i % 171) - 9) < 4 || Math.abs((j % 171) - 9) < 4) ? 1 : 0;
    const col = sm ? seam : tape ? base.map(c => Math.min(255, c * 1.15)) : base; cd.data[k] = col[0] * v; cd.data[k + 1] = col[1] * v; cd.data[k + 2] = col[2] * v; cd.data[k + 3] = 255; }
  cx.putImageData(cd, 0, 0); nc.getContext("2d").putImageData(nd, 0, 0); const ct = new THREE.CanvasTexture(cc), nt = new THREE.CanvasTexture(nc); ct.colorSpace = THREE.SRGBColorSpace; return [ct, nt]; }
function cellMap() { const cv = document.createElement("canvas"); cv.width = 512; cv.height = 640; const x = cv.getContext("2d"); x.fillStyle = "#c8ccd4"; x.fillRect(0, 0, 512, 640);
  for (let i = 0; i < 8; i++) for (let j = 0; j < 10; j++) { const gr = x.createLinearGradient(i * 64, j * 64, i * 64 + 64, j * 64 + 64); gr.addColorStop(0, "#22378f"); gr.addColorStop(1, "#101d58"); x.fillStyle = gr; x.fillRect(i * 64 + 3, j * 64 + 3, 58, 58); x.fillStyle = "rgba(200,210,230,.55)"; for (let k = 1; k < 4; k++) x.fillRect(i * 64 + 3, j * 64 + 3 + k * 14.5, 58, 1.2); }
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; }

// ---------------------------------------------------------------- renderer, post chain: render → bokeh → bloom → output → lens (fringe, vignette, grain)
const glc = $("#gl"), renderer = new THREE.WebGLRenderer({ canvas: glc, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(PR); renderer.setSize(W, H, false); renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(35, W / H, 0.05, 20000), envTex = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
const composer = new EffectComposer(renderer); composer.setPixelRatio(PR); composer.setSize(W, H); const rpass = new RenderPass(scene, camera); composer.addPass(rpass);
const bokeh = new BokehPass(scene, camera, { focus: 10, aperture: 0.0002, maxblur: 0.008 }); composer.addPass(bokeh);
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), 0.55, 0.5, 0.9); composer.addPass(bloom); composer.addPass(new OutputPass());
const lens = new ShaderPass({ uniforms: { tDiffuse: { value: null }, seed: { value: 0 }, ca: { value: 0.0016 }, vig: { value: 0.32 }, grain: { value: 0.035 } }, vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }",
  fragmentShader: "uniform sampler2D tDiffuse; uniform float seed, ca, vig, grain; varying vec2 vUv; float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898,78.233)) + seed) * 43758.5453); } void main(){ vec2 d = vUv - .5; float r2 = dot(d,d); vec2 o = d * ca * r2 * 4.; vec3 col = vec3(texture2D(tDiffuse, vUv + o).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - o).b); col *= 1. - vig * smoothstep(.15, .75, r2 * 2.2); col += (h(vUv * 1000.) - .5) * grain; gl_FragColor = vec4(col, 1.); }" });
composer.addPass(lens);
const ROOMC = document.createElement("canvas"), acc = $("#acc"); acc.width = W * PR; acc.height = H * PR; const ax = acc.getContext("2d");

// ---------------------------------------------------------------- lights: Sun with shadows, Mars bounce fill, cool rim, ignition flash
const SUN = V(-1, 0.35, 0.6).normalize(), sun = new THREE.DirectionalLight(0xfff2e0, 2.7); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -9, right: 9, top: 9, bottom: -9, near: 1, far: 80 }); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.02;
scene.add(sun, sun.target, new THREE.AmbientLight(0x2a3a66, 0.1)); const bounce = new THREE.DirectionalLight(0xff8a5a, 0.0), rim = new THREE.DirectionalLight(0xa8c8ff, 0.0); scene.add(bounce, bounce.target, rim, rim.target);
const flash = new THREE.PointLight(0xffa860, 0, 30, 2); scene.add(flash);
const sunFlare = new THREE.PointLight(0xffffff, 0); sunFlare.position.copy(SUN.clone().multiplyScalar(8000)); scene.add(sunFlare);
{ const tex = (draw) => { const cv = document.createElement("canvas"); cv.width = cv.height = 256; draw(cv.getContext("2d")); return new THREE.CanvasTexture(cv); };
  const disc = tex(x => { const gr = x.createRadialGradient(128, 128, 0, 128, 128, 128); gr.addColorStop(0, "rgba(255,255,245,1)"); gr.addColorStop(0.08, "rgba(255,236,200,.9)"); gr.addColorStop(0.3, "rgba(255,190,140,.25)"); gr.addColorStop(1, "rgba(255,160,100,0)"); x.fillStyle = gr; x.fillRect(0, 0, 256, 256); });
  const ring = tex(x => { x.strokeStyle = "rgba(160,200,255,.35)"; x.lineWidth = 10; x.beginPath(); x.arc(128, 128, 100, 0, 6.28); x.stroke(); });
  const hexa = tex(x => { x.fillStyle = "rgba(255,210,160,.22)"; x.beginPath(); for (let i = 0; i < 6; i++) x.lineTo(128 + Math.cos(i * 1.047) * 90, 128 + Math.sin(i * 1.047) * 90); x.fill(); });
  const lf = new Lensflare(); lf.addElement(new LensflareElement(disc, 520, 0)); lf.addElement(new LensflareElement(hexa, 70, 0.45)); lf.addElement(new LensflareElement(ring, 150, 0.7)); lf.addElement(new LensflareElement(hexa, 110, 0.95)); sunFlare.add(lf); }

// ---------------------------------------------------------------- sky: stars and a faint Milky Way
{ const r = rng(5), n = 9000, pos = new Float32Array(n * 3), col = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) { const u = r() * 2 - 1, th = r() * 6.2832, s = Math.sqrt(1 - u * u), band = r() < 0.45, R = 9000, uu = band ? (r() - 0.5) * 0.25 : u; pos.set([Math.sqrt(1 - uu * uu) * Math.cos(th) * R, uu * R, Math.sqrt(1 - uu * uu) * Math.sin(th) * R], i * 3);
    const k = 0.35 + r() ** 3 * 1.7, tint = r(); col.set([k * (tint < 0.2 ? 1 : 0.86), k * 0.9, k * (tint > 0.7 ? 1.1 : 0.9)], i * 3); }
  const gm = new THREE.BufferGeometry(); gm.setAttribute("position", new THREE.BufferAttribute(pos, 3)); gm.setAttribute("color", new THREE.BufferAttribute(col, 3));
  const stars = new THREE.Points(gm, new THREE.PointsMaterial({ size: 1.6 * PR, sizeAttenuation: false, vertexColors: true, depthWrite: false })); stars.rotation.z = 0.5; scene.add(stars);
  const [mw] = equi(1024, 512, (x, y, z, lat) => { const band = Math.exp(-((lat / 0.18) ** 2)), n = fbm(x * 4, y * 4, z * 4, 6), v = band * clamp(n * 1.6 - 0.35) * 70; return [[v * 0.9, v * 0.85, v]]; }, 1);
  mw.colorSpace = THREE.SRGBColorSpace; const sky = new THREE.Mesh(new THREE.SphereGeometry(8800, 64, 32), new THREE.MeshBasicMaterial({ map: mw, side: THREE.BackSide, depthWrite: false, transparent: true, opacity: 0.6 })); sky.rotation.z = 0.5; scene.add(sky); }

// ---------------------------------------------------------------- planets
const atmo = (color, power, k, night = 0.12) => new THREE.ShaderMaterial({ transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.BackSide, uniforms: { c: { value: new THREE.Color(color) }, sun: { value: SUN } },
  vertexShader: "varying vec3 n; varying vec3 v; void main(){ n = normalize(mat3(modelMatrix)*normal); vec4 w = modelMatrix*vec4(position,1.); v = normalize(cameraPosition - w.xyz); gl_Position = projectionMatrix*viewMatrix*w; }",
  fragmentShader: `uniform vec3 c; uniform vec3 sun; varying vec3 n; varying vec3 v; void main(){ float f = pow(1. - abs(dot(n, v)), ${power.toFixed(1)}); float lit = smoothstep(-.4, .5, dot(-n, sun) * -1.); gl_FragColor = vec4(c * f * ${k.toFixed(2)} * (${night.toFixed(2)} + lit), f); }` });
const [mCol, mBump] = equi(2048, 1024, marsShade); mCol.colorSpace = THREE.SRGBColorSpace;
const mars = new THREE.Mesh(new THREE.SphereGeometry(100, 256, 160), new THREE.MeshStandardMaterial({ map: mCol, bumpMap: mBump, bumpScale: 3.0, roughness: 0.95 })); mars.rotation.y = -2.2; scene.add(mars);
const marsHaze = new THREE.Mesh(new THREE.SphereGeometry(102.2, 128, 64), atmo(0xffb38a, 2.2, 0.9, 0.08)); const marsAtmo = new THREE.Mesh(new THREE.SphereGeometry(104.5, 96, 64), atmo(0xff9a6a, 3.2, 1.5)); scene.add(marsHaze, marsAtmo);
const moonGeo = (seed, r) => { const gm = new THREE.IcosahedronGeometry(r, 5), p = gm.attributes.position; for (let i = 0; i < p.count; i++) { const v = V(p.getX(i), p.getY(i), p.getZ(i)), k = 1 + (fbm(v.x / r * 1.5 + seed, v.y / r * 1.5, v.z / r * 1.5, 4) - 0.5) * 0.7; v.multiplyScalar(k); v.x *= 1.35; p.setXYZ(i, v.x, v.y, v.z); } gm.computeVertexNormals(); return gm; };
const rockMat = new THREE.MeshStandardMaterial({ color: 0x6d6158, roughness: 1, flatShading: false }), phobos = new THREE.Mesh(moonGeo(3, 3.2), rockMat), deimos = new THREE.Mesh(moonGeo(8, 1.8), rockMat); scene.add(phobos, deimos);
const EARTH = V(-560, 40, -900), [eDay, eNight] = equi(1024, 512, earthShade); eDay.colorSpace = THREE.SRGBColorSpace; eNight.colorSpace = THREE.SRGBColorSpace;
const earth = new THREE.Mesh(new THREE.SphereGeometry(28, 128, 64), new THREE.ShaderMaterial({ uniforms: { day: { value: eDay }, night: { value: eNight }, sun: { value: SUN } },
  vertexShader: "varying vec2 vUv; varying vec3 n; void main(){ vUv = uv; n = normalize(mat3(modelMatrix)*normal); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }",
  fragmentShader: "uniform sampler2D day, night; uniform vec3 sun; varying vec2 vUv; varying vec3 n; void main(){ float l = dot(n, sun); vec3 d = texture2D(day, vUv).rgb * (max(l, 0.) * 1.6 + .02); vec3 c = texture2D(night, vUv).rgb * smoothstep(.15, -.25, l) * 2.2; gl_FragColor = vec4(d + c, 1.);\n#include <tonemapping_fragment>\n#include <colorspace_fragment>\n}" }));
earth.position.copy(EARTH); scene.add(earth);
const [cTex] = equi(1024, 512, cloudShade, 1); const clouds = new THREE.Mesh(new THREE.SphereGeometry(28.4, 96, 64), new THREE.MeshStandardMaterial({ color: 0xffffff, map: cTex, alphaMap: cTex, transparent: true, opacity: 0.85, depthWrite: false })); clouds.position.copy(EARTH); scene.add(clouds);
const earthAtmo = new THREE.Mesh(new THREE.SphereGeometry(30.5, 64, 48), atmo(0x5aa8ff, 2.4, 2.6, 0.05)); earthAtmo.position.copy(EARTH); scene.add(earthAtmo);

// ---------------------------------------------------------------- Mangalyaan, detailed (metres; main engine on -X, dish on +Y, solar wing on +Z)
const craft = new THREE.Group(); scene.add(craft); const parts = [], CRAFT_MATS_EXTRA = [];
const add = (m, to = craft) => { m.castShadow = m.receiveShadow = true; to.add(m); parts.push(m); return m; };
const [gc, gn] = foilMaps([214, 160, 64], [90, 60, 20]), [sc_, sn] = foilMaps([196, 200, 208], [80, 84, 92]);
const gold = new THREE.MeshStandardMaterial({ map: gc, normalMap: gn, normalScale: new THREE.Vector2(0.45, 0.45), metalness: 0.95, roughness: 0.38, envMap: envTex, envMapIntensity: 0.55 });
const silver = new THREE.MeshStandardMaterial({ map: sc_, normalMap: sn, normalScale: new THREE.Vector2(0.4, 0.4), metalness: 0.9, roughness: 0.32, envMap: envTex, envMapIntensity: 0.6 });
const white = new THREE.MeshStandardMaterial({ color: 0xe9e9e4, roughness: 0.55, metalness: 0.05, envMap: envTex, envMapIntensity: 0.35, side: THREE.DoubleSide });
const grey = new THREE.MeshStandardMaterial({ color: 0x8a8f99, roughness: 0.38, metalness: 0.85, envMap: envTex, envMapIntensity: 0.8 }), black = new THREE.MeshStandardMaterial({ color: 0x0c0d10, roughness: 0.25, metalness: 0.5 });
add(new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.4, 1.55), [gold, gold, gold, gold, gold, silver]));
[[0.76, 0.3, 0.3, 0.18, 0.16, 0.2], [0.76, -0.25, -0.35, 0.14, 0.2, 0.26], [0.2, 0.71, -0.55, 0.3, 0.1, 0.2]].forEach(([x, y, z, a, b, cc]) => add(new THREE.Mesh(new THREE.BoxGeometry(a, b, cc), black)).position.set(x, y, z));   // instruments
[[0.78, 0.3, 0.3], [0.78, -0.25, -0.35]].forEach(([x, y, z]) => { const l = add(new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.06, 0.06, 20), grey)); l.rotation.z = Math.PI / 2; l.position.set(x + 0.08, y, z); });
for (const sx of [1, -1]) for (const sz of [1, -1]) { const th = add(new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.12, 16, 1, true), grey)); th.rotation.z = Math.PI / 2; th.position.set(-0.78, sx * 0.6, sz * 0.66); }   // 22 N thrusters
{ const pts = []; for (let i = 0; i <= 28; i++) { const r = 1.1 * i / 28; pts.push(new THREE.Vector2(r, r * r * 0.3)); } const dish = new THREE.Group(); dish.position.set(0.1, 1.0, 0); dish.rotation.z = -0.35; craft.add(dish);
  add(new THREE.Mesh(new THREE.LatheGeometry(pts, 72), white), dish);
  for (let i = 0; i < 10; i++) { const rib = add(new THREE.Mesh(new THREE.BoxGeometry(1.08, 0.025, 0.035), grey), dish); const a = i / 10 * 6.2832; rib.position.set(Math.cos(a) * 0.54, 0.085 - 0.02, Math.sin(a) * 0.54); rib.rotation.y = -a; rib.rotation.z = 0.16; }
  for (let i = 0; i < 3; i++) { const a = i / 3 * 6.2832, top = V(0, 0.75, 0), base = V(Math.cos(a) * 1.0, 0.3, Math.sin(a) * 1.0), mid = top.clone().add(base).multiplyScalar(0.5), len = top.distanceTo(base), st = add(new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, len, 6), grey), dish); st.position.copy(mid); st.quaternion.setFromUnitVectors(V(0, 1, 0), top.clone().sub(base).normalize()); }
  add(new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.18, 20), grey), dish).position.set(0, 0.72, 0); const mast = add(new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.32), grey)); mast.position.set(0.05, 0.82, 0); }
{ const yoke = add(new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.0), grey)); yoke.rotation.x = Math.PI / 2; yoke.position.set(0, 0, 1.25); const cells = new THREE.MeshStandardMaterial({ map: cellMap(), metalness: 0.5, roughness: 0.3, envMap: envTex, envMapIntensity: 1.0 }), back = new THREE.MeshStandardMaterial({ color: 0xb8bcc6, roughness: 0.7 }); CRAFT_MATS_EXTRA.push(cells, back);
  for (let i = 0; i < 3; i++) { const z = 2.65 + i * 1.88; add(new THREE.Mesh(new THREE.BoxGeometry(1.44, 0.06, 1.84), [grey, grey, cells, back, grey, grey])).position.set(0, 0, z);
    if (i < 2) { const hg = add(new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.5, 12), grey)); hg.rotation.z = Math.PI / 2; hg.position.set(0, 0, z + 0.94); } } }
[[0.5, -0.71, 0.5, 0.5], [-0.5, 0.71, -0.62, 0.35]].forEach(([x, y, z, l]) => { const a = add(new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, l), grey)); a.position.set(x, y + Math.sign(y) * l / 2, z); add(new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.02, 20), white)).position.set(x, y + Math.sign(y) * l, z); });
const CRAFT_MATS = []; const heatMat = new THREE.MeshStandardMaterial({ color: 0x8a8f99, roughness: 0.35, metalness: 0.85, envMap: envTex, emissive: 0xff5a1a, emissiveIntensity: 0, side: THREE.DoubleSide });
{ const pts = []; for (let i = 0; i <= 16; i++) { const u = i / 16; pts.push(new THREE.Vector2(0.09 + 0.2 * u ** 1.6, -u * 0.55)); } const bell = add(new THREE.Mesh(new THREE.LatheGeometry(pts, 40), heatMat)); bell.rotation.z = -Math.PI / 2; bell.position.set(-0.75, 0, 0); }
// plume: soft-edged, rippling, mostly transparent (vacuum exhaust), a white-blue core with mach diamonds, and a faint warm envelope
[gold, silver, white, grey, black, heatMat, ...CRAFT_MATS_EXTRA].forEach(m => CRAFT_MATS.push([m, m.color.clone(), m.envMapIntensity ?? 1]));
const plumeShader = (core) => new THREE.ShaderMaterial({ transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, uniforms: { k: { value: 0 }, t: { value: 0 } },
  vertexShader: "varying vec2 u; varying vec3 n; varying vec3 v; void main(){ u = uv; n = normalize(normalMatrix*normal); vec4 mv = modelViewMatrix*vec4(position,1.); v = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }",
  fragmentShader: `uniform float k, t; varying vec2 u; varying vec3 n; varying vec3 v; float h(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7))) * 43758.5); } float ns(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.-2.*f); return mix(mix(h(i), h(i+vec2(1,0)), f.x), mix(h(i+vec2(0,1)), h(i+vec2(1,1)), f.x), f.y); }
    void main(){ float a = 1. - u.y; float edge = pow(abs(dot(n, v)), 1.4); float rip = .75 + .5 * ns(vec2(u.x * 10., u.y * 14. - t * 9.));
      ${core ? "float dia = .7 + .3 * pow(abs(sin(u.y * 26.)), 6.); vec3 col = mix(vec3(.55,.75,1.), vec3(1.), a); float al = pow(a, 2.2) * edge * rip * dia * k * 1.2;" : "vec3 col = vec3(1., .72, .5); float al = pow(a, 1.6) * edge * rip * k * .32;"}
      gl_FragColor = vec4(col * al, al); }` });
const plumeCore = new THREE.Mesh(new THREE.ConeGeometry(0.2, 2.2, 40, 24, true), plumeShader(true)), plumeGlow = new THREE.Mesh(new THREE.ConeGeometry(0.85, 6.5, 40, 24, true), plumeShader(false));
plumeCore.rotation.z = Math.PI / 2; plumeCore.position.set(-1.4, 0, 0); plumeGlow.rotation.z = Math.PI / 2; plumeGlow.position.set(-3.6, 0, 0); craft.add(plumeCore, plumeGlow);
const SPARK = 90, spG = new THREE.BufferGeometry(); spG.setAttribute("position", new THREE.BufferAttribute(new Float32Array(SPARK * 3), 3));
const sparks = new THREE.Points(spG, new THREE.PointsMaterial({ color: 0xffd2a0, size: 0.035, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false })); craft.add(sparks);
const SPR = (() => { const r = rng(17); return Array.from({ length: SPARK }, () => [r(), r() * 2 - 1, r() * 2 - 1, 0.7 + r() * 0.6]); })();
const puffTex = (() => { const cv = document.createElement("canvas"); cv.width = cv.height = 128; const x = cv.getContext("2d"), gr = x.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, "rgba(255,255,255,.9)"); gr.addColorStop(1, "rgba(255,255,255,0)"); x.fillStyle = gr; x.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(cv); })();
const rcs = [V(-0.86, 0.6, 0.66), V(-0.86, -0.6, -0.66)].map(p => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: puffTex, color: 0xdfeeff, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true })); s.position.copy(p); craft.add(s); return s; });

// ---------------------------------------------------------------- paths as glowing ribbons that draw themselves with a bright head
const ORB = { a: 230, b: 150, tilt: 0.22 }, orbitPt = th => V(Math.cos(th) * ORB.a + 40, Math.sin(th) * ORB.b * Math.sin(ORB.tilt), Math.sin(th) * ORB.b * Math.cos(ORB.tilt));
const ribbon = (pts, closed, color, rad) => { const curve = new THREE.CatmullRomCurve3(pts, closed), m = new THREE.ShaderMaterial({ transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, uniforms: { p: { value: 1 }, c: { value: new THREE.Color(color) }, o: { value: 1 }, head: { value: 1 } },
    vertexShader: "varying float s; void main(){ s = uv.x; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }",
    fragmentShader: "uniform float p, o, head; uniform vec3 c; varying float s; void main(){ if (s > p) discard; float tail = smoothstep(p - .45, p, s); float hd = smoothstep(p - .015, p, s) * head; float a = (.35 + .65 * tail) * o; gl_FragColor = vec4(c * a + vec3(1.) * hd * 1.4, a); }" });
  const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, closed ? 600 : 300, rad, 8, closed), m); scene.add(mesh); return mesh; };
const orbit = ribbon(Array.from({ length: 120 }, (_, i) => orbitPt(i / 120 * 6.2832)), true, 0xffc65a, 0.55);
const INB = Array.from({ length: 200 }, (_, i) => { const u = i / 199, e = orbitPt(Math.PI * 0.92); return V(lerp(-700, e.x, u), lerp(140, e.y, u) + Math.sin(u * Math.PI) * 30, lerp(520, e.z, u)); });
const inbound = ribbon(INB.filter((_, i) => i % 10 === 0).concat([INB[199]]), false, 0xbcd4ff, 0.18);
const ghost = ribbon(Array.from({ length: 40 }, (_, i) => { const th = Math.PI * 0.92 + i / 39 * 1.4, r = 1 + i / 39 * 1.8, p = orbitPt(th); return V(p.x * r, p.y * r + i * 2, p.z * r + i * 6); }), false, 0xff5a46, 0.45);
const rings = Array.from({ length: 5 }, () => { const m = new THREE.Mesh(new THREE.TorusGeometry(26, 1.1, 8, 64), new THREE.MeshBasicMaterial({ color: 0x8fdcff, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false })); scene.add(m); return m; });

// ---------------------------------------------------------------- comparison set: pillars on a reflective floor
const BAR = new THREE.Group(), BO = V(2600, 0, 0); BAR.position.copy(BO); scene.add(BAR);
const barMat = col => new THREE.MeshPhysicalMaterial({ color: col, metalness: 0.2, roughness: 0.25, clearcoat: 1, clearcoatRoughness: 0.15, envMap: envTex, envMapIntensity: 0.9 });
const barG = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), barMat(0x5b4bd6)), barM = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), barMat(0xd29a34)); BAR.add(barG, barM);
const mirror = new Reflector(new THREE.PlaneGeometry(60, 60), { textureWidth: 512 * PR, textureHeight: 512 * PR, color: 0x2a2a36 }); mirror.rotation.x = -Math.PI / 2; BAR.add(mirror);
const floorVeil = new THREE.Mesh(new THREE.CircleGeometry(30, 64), new THREE.MeshBasicMaterial({ color: 0x05060a, transparent: true, opacity: 0.84 })); floorVeil.rotation.x = -Math.PI / 2; floorVeil.position.y = 0.01; BAR.add(floorVeil);
const barLight = new THREE.SpotLight(0xffffff, 0, 80, 0.6, 0.6); barLight.position.set(-6, 22, 14); barLight.target.position.set(0, 3, 0); BAR.add(barLight, barLight.target);
const reel = new THREE.Group(); { const disc = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 0.22, 48), new THREE.MeshStandardMaterial({ color: 0x2a2d36, metalness: 0.7, roughness: 0.3, envMap: envTex })); disc.rotation.x = Math.PI / 2; reel.add(disc);
  for (let i = 0; i < 6; i++) { const h = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.26, 24), new THREE.MeshBasicMaterial({ color: 0x0b0c12 })); h.rotation.x = Math.PI / 2; h.position.set(Math.cos(i * 1.047) * 0.52, Math.sin(i * 1.047) * 0.52, 0); reel.add(h); } } BAR.add(reel);
const skipIdx = new Set([plumeCore, plumeGlow, sparks, flash, ...rcs].map(o => craft.children.indexOf(o)).filter(i => i >= 0)), mini = craft.clone(true); mini.children = mini.children.filter((_, i) => !skipIdx.has(i));

// ---------------------------------------------------------------- mission control, Bengaluru (stylised): desks, screens, people who wait and then cheer
const room = new THREE.Scene(), roomCam = new THREE.PerspectiveCamera(44, W / H, 0.1, 200); room.add(new THREE.AmbientLight(0x6070a0, 1.3), new THREE.HemisphereLight(0xbfd4ff, 0x202a40, 1.2)); [-3, 0, 3].forEach(x => { const pl = new THREE.PointLight(0x8fc4ff, 6, 10, 2); pl.position.set(x, 1.6, -0.5); room.add(pl); });
const roomKey = new THREE.SpotLight(0xbfd4ff, 40, 60, 0.9, 0.7); roomKey.position.set(0, 9, 6); room.add(roomKey, roomKey.target);
const screenTex = (msg, col) => { const cv = document.createElement("canvas"); cv.width = 1024; cv.height = 400; const x = cv.getContext("2d"); x.fillStyle = "#06101f"; x.fillRect(0, 0, 1024, 400); x.strokeStyle = "rgba(90,170,255,.35)"; for (let i = 0; i < 1024; i += 64) { x.beginPath(); x.moveTo(i, 0); x.lineTo(i, 400); x.stroke(); }
  const fitText = (txt, wt, size, y, colr) => { x.font = `${wt} ${size}px Body, Arial`; const w = x.measureText(txt).width, sz = w > 944 ? size * 944 / w : size; x.font = `${wt} ${sz}px Body, Arial`; x.fillStyle = colr; x.fillText(txt, 40, y); };   // shrink to fit the 944 px safe width
  fitText("MARS ORBITER MISSION · ORBIT INSERTION", 700, 44, 80, "#8fc4ff"); fitText(msg, 900, 96, 230, col); x.strokeStyle = "#ff9a5a"; x.lineWidth = 4; x.beginPath(); for (let i = 0; i < 900; i += 6) x.lineTo(40 + i, 330 - Math.sin(i * 0.03) * 22 - i * 0.02); x.stroke();
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; };
const waitTex = screenTex("AWAITING SIGNAL", "#ffd36b"), okTex = screenTex("MOI SUCCESSFUL", "#7dffa0");
const wall = new THREE.Mesh(new THREE.PlaneGeometry(11, 4.3), new THREE.MeshBasicMaterial({ map: waitTex })); wall.position.set(0, 4.2, -6); room.add(wall);
{ const fl = new THREE.Mesh(new THREE.PlaneGeometry(40, 30), new THREE.MeshStandardMaterial({ color: 0x0d1220, roughness: 0.9 })); fl.rotation.x = -Math.PI / 2; room.add(fl); }
const backWall = new THREE.Mesh(new THREE.PlaneGeometry(40, 14), new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 1 })); backWall.position.set(0, 7, -6.2); room.add(backWall);
const people = [], skin = [0x8d5a3b, 0xa86f4c, 0x6e4430, 0xc08a63], shirts = [0xe8e6df, 0x9fb6d8, 0xd9c9a3, 0x7f8fa8, 0xf0f0f0];
{ const r = rng(77); for (let row = 0; row < 3; row++) { const z = -1.8 + row * 2.3, y0 = row * 0.25;
    const desk = new THREE.Mesh(new THREE.BoxGeometry(9.5, 0.12, 0.9), new THREE.MeshStandardMaterial({ color: 0x2a3142, roughness: 0.6 })); desk.position.set(0, 0.95 + y0, z - 0.55); room.add(desk);
    for (let i = 0; i < 6; i++) { const x = -4 + i * 1.6; const scr = new THREE.Mesh(new THREE.PlaneGeometry(0.62, 0.38), new THREE.MeshBasicMaterial({ color: [0x2c8cff, 0x35d0a0, 0xffb347][(i + row) % 3] })); scr.position.set(x, 1.32 + y0, z - 0.8); scr.rotation.x = -0.15; room.add(scr);
      if (r() < 0.82) { const p = new THREE.Group(), body = new THREE.Mesh(new THREE.CapsuleGeometry(0.22, 0.45, 6, 12), new THREE.MeshStandardMaterial({ color: shirts[Math.floor(r() * 5)], roughness: 0.8 })), head = new THREE.Mesh(new THREE.SphereGeometry(0.16, 20, 14), new THREE.MeshStandardMaterial({ color: skin[Math.floor(r() * 4)], roughness: 0.7 }));
        body.position.y = 0.75; head.position.y = 1.28; p.add(body, head); const arms = [-1, 1].map(s => { const a = new THREE.Group(), m = new THREE.Mesh(new THREE.CapsuleGeometry(0.06, 0.42, 4, 8), body.material); m.position.y = -0.24; a.add(m); a.position.set(s * 0.27, 1.02, 0); a.rotation.z = s * 0.25; p.add(a); return a; });
        p.position.set(x + (r() - 0.5) * 0.3, y0, z); room.add(p); people.push({ p, arms, d: r() * 0.4, jump: r() }); } } } }

// ---------------------------------------------------------------- helpers
const toScreen = (v, cam = camera) => { const p = v.clone().project(cam); return [(p.x + 1) / 2 * W, (1 - p.y) / 2 * H, p.z]; };
const show = (id, k, dy = 30, extra = "") => { const e = $(id); e.style.opacity = clamp(k); e.style.transform = `translateY(${((1 - clamp(k)) * dy).toFixed(1)}px) ${extra}`; };
const wob = (t, a) => V(Math.sin(t * 0.83) * 0.6 + Math.sin(t * 2.1 + 1) * 0.25, Math.sin(t * 0.67 + 2) * 0.5 + Math.sin(t * 1.9) * 0.2, Math.sin(t * 0.71 + 4) * 0.4).multiplyScalar(a);
let FOCUS = 10, APER = 0.0001;
const CR_R = 5.2;   // radius of the spacecraft including the solar wing (m)
const fitD = (fov, fill) => CR_R / Math.tan(fov / 2 * D2R) / fill;   // distance at which the craft fills `fill` of the frame height
const ctrOf = (cpos) => cpos.clone().add(V(0, 0, 1).applyQuaternion(craft.quaternion).multiplyScalar(3.4));
const look = (pos, tgt, fov = 35, roll = 0, w = 0, t = 0) => { camera.position.copy(pos).add(wob(t, w)); camera.up.set(Math.sin(roll), Math.cos(roll), 0); camera.lookAt(tgt.clone().add(wob(t + 3.7, w * 0.6))); camera.fov = fov; camera.updateProjectionMatrix(); camera.updateMatrixWorld(); };
$("#src").textContent = "Sources: ISRO · The Planetary Society · NASA";

// ================================================================ MAIN FILM: scene builders, cameras and overlays (appended after the shared library)
const SC = Object.fromEntries(TM.scenes.map(s => [s.id, s]));
[orbit, inbound, ghost, ...rings, BAR].forEach(o => { o.visible = false; });
const hideAll = () => { [mars, marsAtmo, marsHaze, phobos, deimos, earth, clouds, earthAtmo, craft, orbit, inbound, ghost, ...rings, BAR, ...GROUPS].forEach(o => { o.visible = false; }); STARS.visible = SKY.visible = true; craft.scale.setScalar(1); };
const GROUPS = [];
const group = () => { const g = new THREE.Group(); g.visible = false; scene.add(g); GROUPS.push(g); return g; };
const STARS = scene.children.find(o => o.isPoints), SKY = scene.children.find(o => o.isMesh && o.geometry.parameters && o.geometry.parameters.radius === 8800);
const std = (o) => new THREE.MeshStandardMaterial(Object.assign({ roughness: 0.6, metalness: 0.1, envMap: envTex, envMapIntensity: 0.5 }, o));
const glowSprite = (col, s) => { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: puffTex, color: col, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true })); sp.scale.setScalar(s); return sp; };
const line3 = (pts, col, op = 1) => { const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: col, transparent: true, opacity: op, depthWrite: false })); return l; };

// ---------------------------------------------------------------- 1 · solar system (Sun at the origin; orbit radii in the real 1 : 1.524 ratio)
const SYS = group(), ER = 260, MR = ER * 1.524, AU = 149.6;
const sunBall = new THREE.Mesh(new THREE.SphereGeometry(16, 48, 32), new THREE.MeshBasicMaterial({ color: 0xffe6a8 })); SYS.add(sunBall, glowSprite(0xffc070, 120), glowSprite(0xffffff, 46));
const sunLamp = new THREE.PointLight(0xfff0d8, 3.2, 0, 0); SYS.add(sunLamp);
const eSmall = new THREE.Mesh(new THREE.SphereGeometry(13, 48, 32), std({ map: eDay, roughness: 0.8 })), mSmall = new THREE.Mesh(new THREE.SphereGeometry(10, 48, 32), std({ map: mCol, roughness: 0.95 })); SYS.add(eSmall, mSmall);
const moonSmall = new THREE.Mesh(new THREE.SphereGeometry(1.9, 32, 20), std({ color: 0xb8b4ac, roughness: 1 })); SYS.add(moonSmall);
const circle = (r, n = 240) => Array.from({ length: n }, (_, i) => V(Math.cos(i / n * 6.2832) * r, 0, Math.sin(i / n * 6.2832) * r));
const eOrbit = ribbon(circle(ER), true, 0x5aa8ff, 0.7), mOrbit = ribbon(circle(MR), true, 0xff8a5a, 0.7); scene.remove(eOrbit, mOrbit); SYS.add(eOrbit, mOrbit);
const TH0 = -1.9, hoh = (u) => { const a = (ER + MR) / 2, e = (MR - ER) / (MR + ER), th = TH0 + Math.PI * u, f = Math.PI * u, r = a * (1 - e * e) / (1 + e * Math.cos(f)); return V(Math.cos(th) * r, 0, Math.sin(th) * r); };
const hohRib = ribbon(Array.from({ length: 120 }, (_, i) => hoh(i / 119)), false, 0xffd36b, 1.1); scene.remove(hohRib); SYS.add(hohRib);
const probe = glowSprite(0xffd890, 9); SYS.add(probe);
const failRibs = [[0.62, 1.12], [0.85, 0.9], [0.5, 1.3]].map(([k, s], i) => { const pts = Array.from({ length: 80 }, (_, j) => { const u = j / 79, th = TH0 + 0.3 * i + Math.PI * u * k * 1.3, r = lerp(ER, MR * s, u); return V(Math.cos(th) * r, (i - 1) * 6 * u, Math.sin(th) * r); }); const rb = ribbon(pts, false, 0xff4a3a, 0.9); scene.remove(rb); SYS.add(rb); return rb; });
const distLine = line3([V(0, 0, 0), V(1, 0, 0)], 0xffffff, 0.75); SYS.add(distLine);

// ---------------------------------------------------------------- 3 · timeline bar (Aug 2012 → Nov 2013)
const TL = group(), TLW = 150;
const tlBase = new THREE.Mesh(new THREE.BoxGeometry(TLW, 1.2, 1.2), std({ color: 0x2a3550, emissive: 0x0a1020 })); TL.add(tlBase);
const tlFill = new THREE.Mesh(new THREE.BoxGeometry(1, 1.6, 1.6), std({ color: 0xffc65a, emissive: 0xffa020, emissiveIntensity: 0.9 })); TL.add(tlFill);
const ticks = Array.from({ length: 16 }, (_, i) => { const m = new THREE.Mesh(new THREE.BoxGeometry(0.5, 5, 0.5), std({ color: 0x8fa8d8, emissive: 0x000000 })); m.position.set(-TLW / 2 + i * TLW / 15, 0, 0); TL.add(m); return m; });
const tlHead = glowSprite(0xffd890, 14); TL.add(tlHead);

// ---------------------------------------------------------------- 4 · rockets on the pad, launch, Earth orbit raising
const ROCK = group(), white2 = std({ color: 0xeeeeea, roughness: 0.45 }), greyR = std({ color: 0x5a5f69, roughness: 0.5 }), dark = std({ color: 0x1b1d22, roughness: 0.5 }), orangeR = std({ color: 0xd9822b, roughness: 0.5 });
function rocket(kind) { const g = new THREE.Group(), cyl = (r0, r1, h, y, m) => { const c = new THREE.Mesh(new THREE.CylinderGeometry(r1, r0, h, 40), m); c.position.y = y + h / 2; c.castShadow = c.receiveShadow = true; g.add(c); return c; };
  if (kind === "pslv") { cyl(1.4, 1.4, 20, 0, white2); cyl(1.4, 1.4, 1.2, 20, dark); cyl(1.4, 1.4, 12, 21.2, white2); cyl(1.0, 1.0, 4, 33.2, greyR); cyl(1.6, 1.6, 6, 37.2, white2); cyl(1.6, 0.05, 4.2, 43.2, white2);
    for (let i = 0; i < 6; i++) { const a = i / 6 * 6.2832, b = new THREE.Group(), c = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 12, 24), i % 2 ? white2 : orangeR), n = new THREE.Mesh(new THREE.ConeGeometry(0.5, 1.4, 24), white2); c.position.y = 6; n.position.y = 12.7; b.add(c, n); b.position.set(Math.cos(a) * 1.95, 0, Math.sin(a) * 1.95); g.add(b); } }
  else { cyl(1.4, 1.4, 21, 0, white2); for (let k = 0; k < 6; k++) cyl(1.41, 1.41, 1.4, 2 + k * 3, k % 2 ? dark : white2); cyl(1.4, 1.4, 12, 21, white2); cyl(1.4, 1.4, 8.6, 33, greyR); cyl(1.7, 1.7, 5, 41.6, white2); cyl(1.7, 0.05, 3.6, 46.6, white2);
    for (let i = 0; i < 4; i++) { const a = i / 4 * 6.2832 + 0.78, b = new THREE.Group(), c = new THREE.Mesh(new THREE.CylinderGeometry(1.0, 1.0, 19.7, 28), white2), n = new THREE.Mesh(new THREE.ConeGeometry(1.0, 2.6, 28), white2); c.position.y = 9.85; n.position.y = 21; b.add(c, n); b.position.set(Math.cos(a) * 2.5, 0, Math.sin(a) * 2.5); g.add(b); } }
  return g; }
const pslv = rocket("pslv"), gslv = rocket("gslv"); ROCK.add(pslv, gslv);
const pad = new THREE.Mesh(new THREE.CircleGeometry(160, 64), std({ color: 0x24262c, roughness: 0.95 })); pad.rotation.x = -Math.PI / 2; pad.receiveShadow = true; ROCK.add(pad);
const tower = new THREE.Group(); for (let i = 0; i < 4; i++) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.4, 52, 0.4), greyR); p.position.set((i % 2 ? 1 : -1) * 1.6, 26, (i < 2 ? 1 : -1) * 1.6); tower.add(p); } for (let y = 4; y < 52; y += 4) { const r = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.25, 3.6), greyR); r.position.y = y; tower.add(r); } ROCK.add(tower);
const skyDome = new THREE.Mesh(new THREE.SphereGeometry(5000, 48, 24), new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false, uniforms: { alt: { value: 0 } }, vertexShader: "varying vec3 p; void main(){ p = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }",
  fragmentShader: "uniform float alt; varying vec3 p; void main(){ float h = clamp(p.y, -.2, 1.); vec3 lo = mix(vec3(.36,.5,.68), vec3(.02,.03,.08), alt); vec3 hi = mix(vec3(.08,.2,.45), vec3(0.), alt); gl_FragColor = vec4(mix(lo, hi, smoothstep(0., .6, h)), 1.); }" })); ROCK.add(skyDome);
const daySun = new THREE.DirectionalLight(0xfff4e0, 2.4); daySun.position.set(-60, 120, 80); daySun.castShadow = true; Object.assign(daySun.shadow.camera, { left: -60, right: 60, top: 80, bottom: -10, near: 1, far: 400 }); daySun.shadow.mapSize.set(2048, 2048); ROCK.add(daySun, daySun.target);
const exhaust = new THREE.Mesh(new THREE.ConeGeometry(2.2, 26, 40, 24, true), plumeShader(true)), exGlow = new THREE.Mesh(new THREE.ConeGeometry(5, 34, 40, 24, true), plumeShader(false)); exhaust.rotation.x = Math.PI; exGlow.rotation.x = Math.PI; pslv.add(exhaust, exGlow); exhaust.position.y = -13; exGlow.position.y = -17;
const SMOKE = Array.from({ length: 70 }, (_, i) => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: puffTex, color: 0xd8d4cc, transparent: true, depthWrite: false })); ROCK.add(s); return { s, a: (i * 2.399) % 6.2832, sp: 0.5 + (i * 0.61803) % 1 }; });
// big Earth for orbit raising (radius 60 = 6,371 km; orbit sizes compressed with a square root so they fit: labelled "not to scale")
const EAR = group(), EARTH_R = 60, bigEarth = new THREE.Mesh(new THREE.SphereGeometry(EARTH_R, 160, 96), earth.material.clone()); bigEarth.material.uniforms = THREE.UniformsUtils.clone(earth.material.uniforms); bigEarth.material.uniforms.day.value = eDay; bigEarth.material.uniforms.night.value = eNight; EAR.add(bigEarth);
const bigClouds = new THREE.Mesh(new THREE.SphereGeometry(EARTH_R * 1.012, 128, 64), clouds.material), bigAtmo = new THREE.Mesh(new THREE.SphereGeometry(EARTH_R * 1.07, 96, 48), atmo(0x5aa8ff, 2.4, 2.4, 0.05)); EAR.add(bigClouds, bigAtmo);
const apoU = km => EARTH_R + 4.2 * Math.sqrt(km / 100), PER_U = EARTH_R + 4;
const ellPts = (apoKm, n = 200) => { const ra = apoU(apoKm), rp = PER_U, a = (ra + rp) / 2, c = (ra - rp) / 2, b = Math.sqrt(ra * rp); return Array.from({ length: n }, (_, i) => { const th = i / n * 6.2832; return V(Math.cos(th) * a - c, Math.sin(th) * b * 0.25, Math.sin(th) * b); }); };
const APO = [23550, 28825, 40186, 71623, 118642, 192874], ORBS = APO.map((km, i) => { const r = ribbon(ellPts(km), true, i === APO.length - 1 ? 0xffd36b : 0x8fc4ff, 0.45); scene.remove(r); EAR.add(r); return r; });
const tmi = (() => { const pts = Array.from({ length: 90 }, (_, i) => { const u = i / 89, th = Math.PI + u * 2.6, r = PER_U + u * u * 900; return V(Math.cos(th) * r, u * 60, Math.sin(th) * r * 0.9); }); const r = ribbon(pts, false, 0xffd36b, 0.8); scene.remove(r); EAR.add(r); return r; })();
const periMark = glowSprite(0xffb070, 12); EAR.add(periMark);

// ---------------------------------------------------------------- 5 · Chandrayaan-1 silhouette, 8 · MAVEN, 9 · banknote and auto-rickshaw, 10 · Moon and Chandrayaan-3
const ch1 = new THREE.Group(); { const b = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.5, 1.5), gold); ch1.add(b); const p = new THREE.Mesh(new THREE.BoxGeometry(0.05, 2.1, 2.6), std({ color: 0x1b2a6a, metalness: 0.5, roughness: 0.3 })); p.position.set(0, 0, 2.4); ch1.add(p); const boom = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.0), grey); boom.rotation.x = Math.PI / 2; boom.position.set(0, 0, 1.2); ch1.add(boom); } scene.add(ch1); ch1.visible = false; GROUPS.push(ch1);
const maven = new THREE.Group(); { maven.add(new THREE.Mesh(new THREE.BoxGeometry(2.3, 2.3, 2.0), silver)); for (const s of [1, -1]) { const w = new THREE.Group(), pnl = new THREE.Mesh(new THREE.BoxGeometry(0.06, 1.8, 5.2), std({ map: cellMap(), metalness: 0.5, roughness: 0.3 })); pnl.position.z = s * 3.6; w.add(pnl); const outer = pnl.clone(); outer.position.z = s * 8.6; outer.position.y = 0; w.add(outer); w.rotation.x = s * -0.35; maven.add(w); }
  const dish = new THREE.Mesh(new THREE.CircleGeometry(1.0, 40), white); dish.position.set(1.2, 0.2, 0); dish.rotation.y = Math.PI / 2; maven.add(dish); const boom = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 4.5), grey); boom.position.set(-0.4, 2.8, 0); maven.add(boom); } scene.add(maven); maven.visible = false; GROUPS.push(maven);
const note = (() => { const cv = document.createElement("canvas"); cv.width = 1024; cv.height = 460; const x = cv.getContext("2d"), gr = x.createLinearGradient(0, 0, 1024, 460); gr.addColorStop(0, "#c0397f"); gr.addColorStop(1, "#7a2a8a"); x.fillStyle = gr; x.fillRect(0, 0, 1024, 460);
  x.strokeStyle = "rgba(255,255,255,.25)"; for (let i = 0; i < 40; i++) { x.beginPath(); x.arc(780, 230, 30 + i * 9, 0, 6.28); x.stroke(); } x.fillStyle = "#fff"; x.font = "900 120px Body, Arial"; x.fillText("₹2000", 60, 150); x.font = "700 30px Body, Arial"; x.fillText("ILLUSTRATION · MANGALYAAN MOTIF", 60, 410);
  x.fillStyle = "#f2c26a"; x.fillRect(720, 195, 90, 70); x.fillStyle = "#2a3c8a"; x.fillRect(810, 215, 140, 30); x.fillStyle = "#eee"; x.beginPath(); x.ellipse(760, 185, 50, 16, -0.3, 0, 6.28); x.fill();
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; const m = new THREE.Mesh(new THREE.PlaneGeometry(15.6, 7), new THREE.MeshStandardMaterial({ map: t, roughness: 0.55, side: THREE.DoubleSide })); scene.add(m); m.visible = false; GROUPS.push(m); return m; })();
const auto = new THREE.Group(); { const body = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.3, 1.4), std({ color: 0x2f9a4a, roughness: 0.4 })); body.position.y = 1.0; const top = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.9, 1.45), std({ color: 0xf2c218, roughness: 0.4 })); top.position.set(-0.1, 2.05, 0); const roof = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.12, 1.55), dark); roof.position.set(-0.1, 2.55, 0);
  auto.add(body, top, roof); [[1.1, 0], [-0.9, 0.62], [-0.9, -0.62]].forEach(([x, z]) => { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.3, 24), dark); w.rotation.x = Math.PI / 2; w.position.set(x, 0.42, z); auto.add(w); }); } scene.add(auto); auto.visible = false; GROUPS.push(auto);
const MOON = group(), moonBig = new THREE.Mesh(new THREE.SphereGeometry(60, 160, 96), std({ color: 0xa9a6a0, roughness: 1, bumpMap: mBump, bumpScale: 1.6 })); MOON.add(moonBig);
const lander = new THREE.Group(); { lander.add(new THREE.Mesh(new THREE.BoxGeometry(2, 1.2, 2), gold)); for (let i = 0; i < 4; i++) { const l = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.6), grey); l.position.set((i % 2 ? 1 : -1) * 1.1, -0.6, (i < 2 ? 1 : -1) * 1.1); l.rotation.z = (i % 2 ? -1 : 1) * 0.35; lander.add(l); } const p = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.05, 1.0), std({ color: 0x1b2a6a })); p.position.set(0, 0.65, 0); lander.add(p); }
lander.scale.setScalar(1.0); lander.position.set(0, -60.9, 0); lander.rotation.x = Math.PI; MOON.add(lander);

// ---------------------------------------------------------------- overlays: one generic card system; every box is measured by the audit
const OV = {}; const ovl = $("#ovl");
function card(id, html, o) { let e = OV[id]; if (!e) { e = document.createElement("div"); e.className = "card " + (o.cls || ""); e.id = id; ovl.appendChild(e); OV[id] = e; }
  if (e._h !== html) { e.innerHTML = html; e._h = html; } const k = clamp(o.k); e.style.opacity = k; e.style.left = o.x + "px"; e.style.top = o.y + "px"; if (o.w) e.style.width = o.w + "px"; e.style.transform = `translateY(${((1 - k) * 20).toFixed(1)}px)`; e._used = true; }
const CHIP = $("#chip"), SRC = $("#src");
const SOURCES = { hard: "Sources: NASA · ISRO", first: "Sources: NASA · JAXA · ISRO", clock: "Source: ISRO", rocket: "Sources: ISRO · The Planetary Society", small: "Source: ISRO", people: "Source: ISRO", nearly: "Sources: ISRO · Spaceflight Now · The Planetary Society", maven: "Sources: NASA · ISRO", payoff: "Sources: ISRO · RBI · PTI", meaning: "Sources: ISRO", end: "" };
const kmFmt = v => Math.round(v).toLocaleString("en-US");
let SUBJ = [];   // [{n, objs, cam, panel}] 3D subjects of this frame, for the audit

// ---------------------------------------------------------------- shots
function shot(tg) {
  let sc = TM.scenes[0]; for (const s of TM.scenes) if (tg >= s.start) sc = s; const t = tg - sc.start, c = sc.lines.map(l => l.start), d = sc.dur;
  hideAll(); SUBJ = []; rpass.scene = scene; let cam = camera, exp = 1.0, aper = 0, focus = 30, flare = 0, useRoom = false, bloomK = 0.5; camera.clearViewOffset(); camera.updateProjectionMatrix();
  const isk = (a, b) => E.io(seg(t, a, b));
  renderer.toneMappingExposure = 1; sun.intensity = 2.7; heatMat.emissiveIntensity = 0; plumeCore.visible = plumeGlow.visible = sparks.visible = false; rcs.forEach(s => s.visible = false); flash.intensity = 0;
  CRAFT_MATS.forEach(([m, base, env]) => { m.color.copy(base); m.envMapIntensity = env; });
  const craftAt = (p, yaw = 0, pitch = 0.2) => { craft.visible = true; craft.position.copy(p); craft.rotation.set(pitch, yaw, 0); sun.position.copy(p.clone().add(SUN.clone().multiplyScalar(40))); sun.target.position.copy(p); bounce.intensity = 0; };
  const burnFx = (k, tt) => { plumeCore.visible = plumeGlow.visible = sparks.visible = k > 0.01; plumeCore.material.uniforms.k.value = plumeGlow.material.uniforms.k.value = k; plumeCore.material.uniforms.t.value = plumeGlow.material.uniforms.t.value = tt; heatMat.emissiveIntensity = k * 2;
    const P = spG.attributes.position.array; for (let i = 0; i < SPARK; i++) { const [ph, a, b, sp] = SPR[i], age = (tt * sp * 1.4 + ph) % 1; P[i * 3] = -1.3 - age * 5 * k; P[i * 3 + 1] = a * age * 0.7; P[i * 3 + 2] = b * age * 0.7; } spG.attributes.position.needsUpdate = true; sparks.material.opacity = k * 0.6; };
  const fitCraft = (dir, fill, fov = 34, up = 0) => { const ctr = craft.position.clone().add(V(0, 0, 1).applyQuaternion(craft.quaternion).multiplyScalar(3.4)); look(ctr.clone().add(dir.clone().normalize().multiplyScalar(5.2 / Math.tan(fov / 2 * D2R) / fill)), ctr.clone().add(V(0, up, 0)), fov, 0, 0.15, tg); SUBJ.push({ n: "[spacecraft]", objs: parts }); return ctr; };
  const id = sc.id;
  if (id === "hard") {   // the solar system: changing distance, the transfer orbit, the window, failures, then Earth and its Moon
    SYS.visible = true; const warp = t < c[1] ? 0 : t < c[2] ? (t - c[1]) * 0.12 : t < c[4] ? 0.12 * (c[2] - c[1]) : 0.12 * (c[2] - c[1]) + (t - c[4]) * 0.03;
    const thE = 0.6 + warp * 6.2832, thM = 0.6 + warp * 6.2832 / 1.881, transfer = t >= c[2] && t < c[5];
    const u = transfer ? isk(c[2] + 0.4, c[4] - 0.2) : 0, thE2 = transfer ? TH0 + u * Math.PI * 0.95 : thE, thM2 = transfer ? TH0 + 0.77 + u * (Math.PI - 0.77) : thM;
    eSmall.position.set(Math.cos(thE2) * ER, 0, Math.sin(thE2) * ER); mSmall.position.set(Math.cos(thM2) * MR, 0, Math.sin(thM2) * MR); eSmall.rotation.y = tg * 0.5; mSmall.rotation.y = tg * 0.5;
    moonSmall.position.copy(eSmall.position).add(V(Math.cos(tg * 0.8) * 34, 2, Math.sin(tg * 0.8) * 34));
    eOrbit.visible = mOrbit.visible = true; eOrbit.material.uniforms.p.value = mOrbit.material.uniforms.p.value = fin(t, 0.4, 2.0); eOrbit.material.uniforms.head.value = mOrbit.material.uniforms.head.value = 0; eOrbit.material.uniforms.o.value = mOrbit.material.uniforms.o.value = 0.55;
    hohRib.visible = transfer; hohRib.material.uniforms.p.value = u; probe.visible = transfer; probe.position.copy(hoh(u)).add(V(0, 3, 0));
    distLine.visible = t >= c[1] && t < c[2] + 0.3; distLine.geometry.setFromPoints([eSmall.position, mSmall.position]);
    failRibs.forEach((r, i) => { r.visible = t >= c[5]; r.material.uniforms.p.value = fin(t, c[5] + 0.6 + i * 0.9, 1.2); r.material.uniforms.head.value = 1; });
    const moonK = isk(c[6] - 0.3, c[6] + 2.2), top = V(0, 470, 330), near = eSmall.position.clone().add(V(-46, 34, 92)); if (moonK > 0.25) { eOrbit.visible = mOrbit.visible = false; failRibs.forEach(r => r.visible = false); }
    look(top.clone().lerp(near, moonK), V(0, 0, 0).lerp(eSmall.position, moonK), 40, 0, 0.4 * (1 - moonK), tg); exp = 1.0;
    if (t >= c[1] && t < c[2] + 0.3) { const dkm = eSmall.position.distanceTo(mSmall.position) / ER * AU; card("dist", `<b>${Math.round(dkm)}</b> million km<br><small>Earth–Mars distance, right now</small>`, { x: 1400, y: 150, w: 420, k: fin(t, c[1] + 0.6) * (1 - fin(t, c[2] - 0.1, 0.3)), cls: "big" }); }
    card("range", "≈ 55 million km at closest<br>≈ 400 million km at farthest", { x: 1400, y: 330, w: 420, k: fin(t, c[1] + 4.5) * (1 - fin(t, c[2] - 0.1, 0.3)) });
    card("months", "<b>≈ 10</b> months<br><small>Mangalyaan's journey</small>", { x: 1400, y: 150, w: 420, k: fin(t, c[3] + 1.5) * (1 - fin(t, c[4] - 0.2, 0.3)), cls: "big" });
    card("window", "<b>26</b> months<br><small>between launch windows</small>", { x: 1400, y: 150, w: 420, k: fin(t, c[4] + 1.5) * (1 - fin(t, c[5] - 0.2, 0.3)), cls: "big" });
    card("failed", "Many missions to Mars<br><b class='red'>have failed</b>", { x: 1400, y: 150, w: 420, k: fin(t, c[5] + 1.0) * (1 - fin(t, c[6] - 0.3, 0.3)), cls: "big" });
    card("moon", "CHANDRAYAAN-1 · 2008<br><small>India's farthest trip so far: the Moon</small>", { x: 1350, y: 170, w: 480, k: fin(t, c[6] + 1.8) });
    if (moonK > 0.5) SUBJ.push({ n: "[Earth]", objs: [eSmall] });
  }
  else if (id === "first") {   // four early attempts, against a slowly turning Mars
    mars.visible = marsAtmo.visible = marsHaze.visible = true; mars.rotation.y = -2.2 + tg * 0.01; look(V(-330, 120, 330), V(0, 0, 0), 34, 0, 0.6, tg); camera.setViewOffset(W, H, -W * 0.2, 0, W, H); camera.updateProjectionMatrix();
    const C = [["USSR · 1960", "First two Mars probes", "never reached orbit"], ["USA · 1964", "Mariner 3", "protective cover failed to open"], ["JAPAN · 2003", "Nozomi", "could not enter Mars orbit"], ["CHINA · 2011", "Yinghuo-1", "lost with the Russian probe carrying it"]];
    C.forEach(([a, b, x], i) => card("f" + i, `<span class="k">${a}</span><b>${b}</b><br><span class="red">✕</span> ${x}`, { x: 80 + (i % 2) * 450, y: 150 + Math.floor(i / 2) * 230, w: 420, k: fin(t, c[Math.min(4, i + 1)] + (i === 3 ? 3.4 : 0.6)) * (1 - fin(t, c[4] - 0.4, 0.3)) }));
    card("rare", "Reaching Mars on the <b>first</b> try:<br><b class='gold'>almost unheard of</b>", { x: 80, y: 150, w: 600, k: fin(t, c[4] + 0.3), cls: "big" });
  }
  else if (id === "clock") {   // fifteen months
    TL.visible = true; const k = isk(c[1] - 0.5, c[2] + 3.0); tlFill.scale.x = Math.max(0.01, TLW * k); tlFill.position.x = -TLW / 2 + TLW * k / 2; ticks.forEach((m, i) => { m.material.emissive.setHex(i / 15 <= k ? 0xffa020 : 0x000000); }); tlHead.position.set(-TLW / 2 + TLW * k, 0, 0);
    look(V(lerp(-10, 10, k), 30, 168), V(0, -8, 0), 40, 0, 0.3, tg);
    card("ap", "<span class='k'>APPROVED</span><b>3 Aug 2012</b>", { x: 140, y: 690, w: 330, k: fin(t, c[0] + 2.4) });
    card("lw", "<span class='k'>LAUNCH WINDOW</span><b>Nov 2013</b>", { x: 1440, y: 690, w: 330, k: fin(t, c[1] + 0.6) });
    card("m15", `<b class="huge">${Math.round(15 * k)}</b><br>months`, { x: 760, y: 150, w: 400, k: fin(t, c[1] + 2.0), cls: "center" });
    SUBJ.push({ n: "[timeline]", objs: [tlBase] });
  }
  else if (id === "rocket") {
    const L2 = c[2], L3 = c[3];
    if (t < L2) {   // GSLV vs PSLV on the pad
      ROCK.visible = true; STARS.visible = SKY.visible = false; skyDome.material.uniforms.alt.value = 0; pslv.position.set(8, 0, 0); gslv.position.set(-8, 0, 0); exhaust.visible = exGlow.visible = false; tower.position.set(30, 0, -10); SMOKE.forEach(m => m.s.visible = false);
      look(V(lerp(-14, 14, isk(0, L2)), 22, 112), V(0, 24, 0), 40, 0, 0.3, tg); exp = 0.72; bloomK = 0.15;
      const [gx, gy] = toScreen(V(-12.5, 28, 0)), [px, py] = toScreen(V(13.5, 28, 0));
      card("gslv", "<span class='k'>GSLV</span>more powerful<br><span class='red'>failed twice in 2010</span>", { x: gx - 320, y: gy - 50, w: 300, k: fin(t, c[1] + 0.8) });
      card("pslvl", "<span class='k'>PSLV</span>smaller<br><span class='green'>reliable</span>", { x: px + 20, y: py - 50, w: 300, k: fin(t, c[1] + 4.0) });
      SUBJ.push({ n: "[GSLV]", objs: [gslv] }, { n: "[PSLV]", objs: [pslv] });
    } else if (t < L3) {   // launch from Sriharikota
      ROCK.visible = true; STARS.visible = SKY.visible = false; gslv.visible = false; const lt = Math.max(0, t - L2 - 0.6), yR = 0.9 * lt * lt; pslv.position.set(0, yR, 0); tower.position.set(6, 0, 0);
      skyDome.material.uniforms.alt.value = clamp(yR / 900); exhaust.visible = exGlow.visible = t > L2 + 0.2; exhaust.material.uniforms.k.value = exGlow.material.uniforms.k.value = fin(t, L2 + 0.2, 0.4); exhaust.material.uniforms.t.value = exGlow.material.uniforms.t.value = tg;
      SMOKE.forEach(({ s, a, sp }, i) => { const age = clamp((t - L2 - 0.2) * sp * 0.6 - i * 0.008); s.visible = age > 0; s.position.set(Math.cos(a) * age * 40, 2 + age * 6, Math.sin(a) * age * 40); s.scale.setScalar(6 + age * 30); s.material.opacity = 0.75 * (1 - age); });
      look(V(-52, 20 + yR, 104), V(0, 24 + yR, 0), 40, 0, 0.4, tg); exp = 0.72; bloomK = 0.2;
      card("shar", "<span class='k'>5 NOVEMBER 2013</span><b>Sriharikota</b>", { x: 80, y: 150, w: 380, k: fin(t, L2 + 1.2) * (1 - fin(t, L3 - 0.4, 0.3)) });
      SUBJ.push({ n: "[PSLV]", objs: pslv.children.filter(o => o !== exhaust && o !== exGlow) });
    } else {   // around Earth: orbit raising, then the departure burn
      EAR.visible = true; bigEarth.rotation.y = tg * 0.02; bigClouds.rotation.y = tg * 0.026; const stepT = [c[4] + 2.5, c[4] + 3.8, c[5] + 1.5, c[6] - 1.0, c[6] + 0.5], nOrb = 1 + stepT.filter(x => t >= x).length;
      ORBS.forEach((r, i) => { r.visible = i < nOrb; r.material.uniforms.p.value = i < nOrb - 1 ? 1 : fin(t, i ? stepT[i - 1] : L3 + 1, 1.0); r.material.uniforms.o.value = i < nOrb - 1 ? 0.3 : 1; r.material.uniforms.head.value = i < nOrb - 1 ? 0 : 1; });
      periMark.position.set(-PER_U - 0.5, 0, 0); periMark.visible = t > c[4] + 1.5 && t < c[7] + 0.5; periMark.material.opacity = 0.5 + 0.5 * Math.sin(tg * 6);
      const departing = t >= c[7] + 1.5; tmi.visible = departing; tmi.material.uniforms.p.value = fin(t, c[7] + 1.5, 2.4);
      const camK = isk(L3, c[4] + 1), camOut = isk(c[7] + 1.0, d - 0.5); look(V(lerp(-210, -120, camK), lerp(180, 300, camK) + camOut * 260, lerp(340, 420, camK) + camOut * 500), V(lerp(0, 60, camK), 0, 0), 42, 0, 0.3, tg);
      card("apo", `<span class='k'>HIGHEST POINT OF ORBIT</span><b>${kmFmt(APO[Math.min(APO.length - 1, nOrb - 1)])} km</b><br><small>orbit sizes not to scale</small>`, { x: 80, y: 150, w: 420, k: fin(t, L3 + 1.2) * (1 - fin(t, c[7] + 1.2, 0.3)) });
      card("ober", "<span class='k'>OBERTH EFFECT</span>Push where you're fastest<br>for the biggest boost", { x: 80, y: 150, w: 420, k: 0 });
      card("tmi", "<span class='k'>1 DECEMBER 2013</span><b>Trans-Mars injection</b>", { x: 80, y: 150, w: 420, k: fin(t, c[7] + 1.4) });
      card("peri", "closest point:<br>engine fires here", { x: 0, y: 0, w: 260, k: 0 });
      if (t > c[4] + 1.5 && t < c[7]) { const [sx, sy] = toScreen(V(-PER_U, 0, 0)); const eb = projBox([bigEarth], camera); card("peri", "closest point · engine fires here", { x: Math.max(40, (eb ? eb.x0 : sx) - 330), y: Math.min(880, (eb ? eb.y1 : sy) + 16), w: 300, k: fin(t, c[4] + 1.8) * (1 - fin(t, c[7] - 0.3, 0.3)) }); }
      if (t > c[5] && t < c[6] + 0.5) card("ober", "<span class='k'>OBERTH EFFECT</span>Push where you're fastest<br>for the biggest boost", { x: 1440, y: 150, w: 420, k: fin(t, c[5] + 0.6) * (1 - fin(t, c[6] + 0.2, 0.3)) });
      SUBJ.push({ n: "[Earth]", objs: [bigEarth] });
    }
  }
  else if (id === "small") {   // the spacecraft up close: mass, five instruments, Chandrayaan-1
    craftAt(V(0, 0, 0), tg * 0.18 + 0.4, 0.15); const ch = t >= c[4] + 4.0; if (ch) { ch1.visible = true; ch1.position.set(16, 0, 0); ch1.rotation.y = tg * 0.18; }
    const ctr = fitCraft(V(-0.55, 0.25, 0.8), ch ? 0.36 : 0.6, 34, 0); if (ch) { look(ctr.clone().lerp(V(16, 0, 0), 0.5).add(V(-14, 6, 44)), ctr.clone().lerp(V(16, 0, 0), 0.5), 34, 0, 0.15, tg); SUBJ.push({ n: "[Chandrayaan-1]", objs: [ch1] }); }
    const fuelK = fin(t, c[1] + 1.0, 1.2);
    card("mass", `<span class='k'>LAUNCH MASS</span><b>≈ 1,340 kg</b><div class="bar"><i style="width:${(63.6 * fuelK).toFixed(1)}%;background:#4fa3ff"></i><i style="width:${(36.4 * fuelK).toFixed(1)}%;background:#9aa3b5"></i></div><small>blue ≈ 850 kg of fuel · grey: the spacecraft</small>`, { x: 1380, y: 150, w: 460, k: fin(t, c[1] + 0.4) * (1 - fin(t, c[2] - 0.3, 0.3)) });
    card("inst", "<span class='k'>FIVE INSTRUMENTS</span><b>≈ 15 kg</b> in total", { x: 1380, y: 150, w: 460, k: fin(t, c[2] + 0.4) * (1 - fin(t, c[4] - 0.3, 0.3)) });
    card("ilist", "Mars Colour Camera<br>Methane Sensor for Mars<br>Thermal Infrared Imaging Spectrometer<br>Lyman Alpha Photometer<br>Exospheric Neutral Composition Analyser", { x: 1380, y: 330, w: 460, k: fin(t, c[3] + 0.4) * (1 - fin(t, c[4] - 0.3, 0.3)), cls: "list" });
    card("chand", "<span class='k'>SIMILAR STRUCTURE &amp; ENGINES</span>Mangalyaan <small>(left)</small> · Chandrayaan-1 <small>(right, 2008)</small>", { x: 560, y: 150, w: 800, k: fin(t, c[4] + 4.2), cls: "center" });
  }
  else if (id === "people") {   // mission control, full frame
    useRoom = true; people.forEach(({ arms }, i) => arms.forEach((a, s) => { a.rotation.z = (s ? 1 : -1) * 0.25; })); wall.material.map = waitTex;
    const k = isk(0, d); roomCam.position.set(lerp(-3, 3, k), lerp(4.2, 3.8, k), lerp(16.5, 14.5, k)); roomCam.lookAt(0, 2.6, -2); roomCam.updateMatrixWorld(); cam = roomCam;
    card("sal", "<span class='k'>SALARIES</span>Engineers in India earn a fraction<br>of US or European pay", { x: 80, y: 150, w: 520, k: fin(t, c[1] + 1.0) * (1 - fin(t, c[3] - 0.4, 0.3)) });
    card("built", "<span class='k'>BUILT AT HOME</span>Designed and built in India", { x: 1320, y: 150, w: 520, k: fin(t, c[2] + 0.6) * (1 - fin(t, c[3] - 0.4, 0.3)) });
    card("team", "Small team · tight schedule · no extras", { x: 560, y: 150, w: 800, k: fin(t, c[3] + 0.3), cls: "center big" });
    SUBJ.push({ n: "[wall screen]", objs: [wall], cam: roomCam });
  }
  else if (id === "nearly") {
    if (t < c[3]) {   // the shortfall and the make-up burn, around Earth
      EAR.visible = true; bigEarth.rotation.y = tg * 0.02; ORBS.forEach((r, i) => { r.visible = i === 3; r.material.uniforms.p.value = 1; r.material.uniforms.o.value = 0.6; r.material.uniforms.head.value = 0; });
      const pc = V(-PER_U - 1, 0, 0); craftAt(pc, Math.PI, 0.2); craft.scale.setScalar(1);
      const b1 = c[1] + 1.2, cut = c[1] + 4.0, b2 = c[2] + 1.0, k1 = seg(t, b1, b1 + 0.4) * (t < cut ? 1 : Math.max(0, 1 - (t - cut) * 6)) * (t > cut - 0.6 ? 0.5 + 0.5 * Math.sin(t * 40) : 1), k2 = seg(t, b2, b2 + 0.4) * (1 - seg(t, b2 + 3.0, b2 + 3.4));
      burnFx(Math.max(k1, k2), tg); const ctr = fitCraft(V(-0.3, 0.3, 1), 0.5, 34, 1.5); focus = camera.position.distanceTo(ctr); aper = 0.0002;
      const apo = t < cut ? lerp(71623, 78276, seg(t, b1, cut)) : t < b2 ? 78276 : lerp(78276, 118642, seg(t, b2, b2 + 3.2));
      card("hud", `<span class='k'>ORBIT-RAISING BURN 4 · 11 NOV 2013</span><b>${kmFmt(apo)} km</b> <small>target 100,000 km</small><br>${t > cut && t < b2 ? "<span class='red'>ENGINE CUT OFF EARLY · VALVE FAULT</span>" : t >= b2 ? "<span class='green'>EXTRA BURN · BACK ON TRACK</span>" : "MAIN ENGINE FIRING"}`, { x: 80, y: 760, w: 600, k: fin(t, c[1] + 0.3) });
    } else if (t < c[6]) {   // the long cruise, the restart test
      craftAt(V(0, 0, 0), tg * 0.05 + 0.6, 0.18); const ctr = fitCraft(V(-0.5, 0.2, 0.85), 0.6, 34, 1.0); const cold = fin(t, c[3], 1.5) * (1 - fin(t, c[5], 1)); CRAFT_MATS.forEach(([m, base]) => { m.color.copy(base).lerp(new THREE.Color(0x9fc8ff), 0.35 * cold); });
      const tf = c[5] + 4.4; burnFx(seg(t, tf, tf + 0.15) * (1 - seg(t, tf + 0.5, tf + 0.7)), tg);
      card("days", `<span class='k'>MAIN ENGINE IDLE</span><b>${Math.round(300 * seg(t, c[3] + 0.5, c[4] + 1.5))}</b> days`, { x: 80, y: 760, w: 420, k: fin(t, c[3] + 0.4) * (1 - fin(t, c[5] + 2.0, 0.3)) });
      card("test", `<span class='k'>22 SEPTEMBER 2014 · TEST FIRE</span><b>${t > tf ? "3.968 s" : "…"}</b> ${t > tf + 1.2 ? "<span class='green'>✓ IT WORKS</span>" : ""}`, { x: 80, y: 760, w: 500, k: fin(t, c[5] + 2.2) });
    } else {   // two days later: the capture burn, in Mars's shadow
      mars.visible = marsAtmo.visible = marsHaze.visible = true; const p = V(-140, 40, 160); craftAt(p, -0.8, 0.2); CRAFT_MATS.forEach(([m, base, env]) => { m.color.copy(base).multiplyScalar(0.12); m.envMapIntensity = env * 0.12; }); burnFx(1, tg); flash.position.copy(p); flash.intensity = 8;
      const ctr = fitCraft(V(-0.6, -0.1, 0.8), 0.42, 36, 1.0); exp = 1.1;
      card("moi", "<span class='k'>24 SEPTEMBER 2014</span><b>24 minutes</b> · in Mars's shadow · autonomous", { x: 80, y: 760, w: 640, k: fin(t, c[6] + 0.8) });
    }
  }
  else if (id === "maven") {   // two orbiters, one week
    mars.visible = marsAtmo.visible = marsHaze.visible = true; const a1 = 2.4 + tg * 0.05, a2 = a1 + 0.5; craftAt(V(Math.cos(a1) * 150, 30, Math.sin(a1) * 150), -a1, 0.2); craft.scale.setScalar(5); maven.visible = true; maven.scale.setScalar(4); maven.position.set(Math.cos(a2) * 165, 55, Math.sin(a2) * 165); maven.rotation.set(0.1, -a2, 0);
    const mid = craft.position.clone().lerp(maven.position, 0.5), out = mid.clone().setY(0).normalize(); look(mid.clone().add(out.multiplyScalar(210)).add(V(0, 50, 0)), mid.clone().add(V(0, -14, 0)), 40, 0, 0.3, tg); SUBJ.push({ n: "[Mangalyaan]", objs: parts }, { n: "[MAVEN]", objs: [maven] });
    const [mx, my] = toScreen(craft.position), [vx, vy] = toScreen(maven.position);
    const bm = projBox(parts, camera), bv = projBox([maven], camera);
    if (bm) card("lm", "<span class='k'>MANGALYAAN · ISRO</span>≈ $74 million", { x: (bm.x0 + bm.x1) / 2 - 160, y: Math.min(880, bm.y1 + 16), w: 320, k: fin(t, c[1] + 0.4), cls: "center" });
    if (bv) card("lv", "<span class='k'>MAVEN · NASA</span>several hundred<br>million dollars", { x: (bv.x0 + bv.x1) / 2 - 170, y: Math.min(880, bv.y1 + 16), w: 340, k: fin(t, c[1] + 1.4), cls: "center" });
    card("both", "Both worked. <b class='gold'>One cost a fraction of the other.</b>", { x: 410, y: 900, w: 1100, k: fin(t, c[2] + 0.2), cls: "center big" });
  }
  else if (id === "payoff") {
    mars.visible = marsAtmo.visible = marsHaze.visible = phobos.visible = true; const a = 1.8 + tg * 0.06, p = V(Math.cos(a) * 160, 40, Math.sin(a) * 160);
    if (t < c[3]) { craftAt(p, -a, 0.2); look(V(160, 260, 520), V(0, 0, 0), 38, 0, 0.6, tg); phobos.position.set(-210, 20, 120);
      card("life", `<span class='k'>DESIGN LIFE</span><b>6 months</b>${t > c[1] ? " → <b class='gold'>≈ 8 years</b>" : ""}`, { x: 80, y: 150, w: 520, k: fin(t, c[0] + 0.6) * (1 - fin(t, c[3] - 0.3, 0.3)) });
      if (t > c[2]) { card("photo", "Full-planet photographs · Phobos · the Martian atmosphere", { x: 410, y: 900, w: 1100, k: fin(t, c[2] + 0.5) * (1 - fin(t, c[3] - 0.3, 0.3)), cls: "center" }); flash.position.copy(p); flash.intensity = Math.max(0, Math.sin((t - c[2]) * 2.2)) ** 30 * 60; } }
    else if (t < c[4]) {   // the banknote
      note.visible = true; note.position.set(0, 0, 0); note.rotation.set(-0.15 + 0.05 * Math.sin(tg * 0.5), 0.3 * Math.sin(tg * 0.3), 0.04); STARS.visible = true; mars.visible = marsAtmo.visible = marsHaze.visible = phobos.visible = false;
      look(V(0, 2, lerp(26, 21, isk(c[3], c[4]))), V(0, 0, 0), 38, 0, 0.1, tg); SUBJ.push({ n: "[banknote]", objs: [note] });
      card("noteL", "₹2,000 banknote, 2016 · Mangalyaan motif<br><small>illustration, not a replica</small>", { x: 560, y: 860, w: 800, k: fin(t, c[3] + 0.6), cls: "center" });
    } else if (t < c[5]) {   // contact lost
      craftAt(p, -a, 0.2); const k = fin(t, c[4] + 0.8, 2.5); CRAFT_MATS.forEach(([m, base, env]) => { m.color.copy(base).multiplyScalar(1 - 0.7 * k); m.envMapIntensity = env * (1 - 0.7 * k); }); fitCraft(V(-0.6, 0.2, 0.8), 0.5, 34, 1.0);
      card("lost", `<span class='k'>2022</span><b class='red'>SIGNAL LOST</b><br><small>fuel exhausted · batteries drained</small>`, { x: 80, y: 760, w: 420, k: fin(t, c[4] + 0.6) });
    } else {   // seven rupees per kilometre, and an auto-rickshaw
      STARS.visible = true; mars.visible = marsAtmo.visible = marsHaze.visible = phobos.visible = false; auto.visible = true; auto.position.set(0, 0, 0); auto.rotation.y = 0.6 + tg * 0.2; craftAt(V(-9, 2.5, -2), tg * 0.2, 0.2); craft.scale.setScalar(0.55);
      look(V(-3, 5, 22), V(-3, 1.6, 0), 36, 0, 0.12, tg); SUBJ.push({ n: "[auto-rickshaw]", objs: [auto] }, { n: "[spacecraft]", objs: parts });
      card("km", `<span class='k'>JOURNEY</span><b>≈ ${Math.round(650 * fin(t, c[5] + 0.3, 2.5))} million km</b>`, { x: 80, y: 150, w: 460, k: fin(t, c[5] + 0.3) });
      card("rs", "<b class='gold'>≈ ₹7 per km</b><br><small>Prime Minister Modi, 2014</small>", { x: 1380, y: 150, w: 460, k: fin(t, c[5] + 3.0) });
      card("autoL", "Ahmedabad auto-rickshaw: <b>≈ ₹10 per km</b> <small>(2014)</small>", { x: 480, y: 900, w: 960, k: fin(t, c[6] + 0.2), cls: "center" });
    }
  }
  else if (id === "meaning") {
    if (t < c[2]) { mars.visible = marsAtmo.visible = marsHaze.visible = true; craftAt(V(-130, 50, 150), -0.8, 0.2); look(V(-260, 160, 520), V(-40, 0, 0), 38, 0, 0.5, tg); SUBJ.push({ n: "[spacecraft]", objs: parts });
      card("m1", "Cheap ≠ careless", { x: 560, y: 150, w: 800, k: fin(t, c[0] + 0.3) * (1 - fin(t, c[2] - 0.3, 0.3)), cls: "center big" });
      card("m2", "Simple, proven solutions · let physics do the work", { x: 410, y: 900, w: 1100, k: fin(t, c[1] + 0.5) * (1 - fin(t, c[2] - 0.3, 0.3)), cls: "center" }); }
    else if (t < c[3]) { MOON.visible = true; moonBig.rotation.y = tg * 0.01; const k = isk(c[2], c[3]); MOON.rotation.x = Math.PI; lander.scale.setScalar(2.2); look(V(lerp(-20, -12, k), lerp(66, 64.5, k), lerp(26, 18, k)), V(0, 61.6, 0), 36, 0, 0.1, tg); SUBJ.push({ n: "[Chandrayaan-3 lander]", objs: [lander] });
      card("c3", "<span class='k'>23 AUGUST 2023</span><b>Chandrayaan-3</b><br>first landing near the Moon's south pole", { x: 80, y: 150, w: 560, k: fin(t, c[2] + 0.8) }); }
    else { mars.visible = marsAtmo.visible = marsHaze.visible = true; craftAt(V(150, 40, 120), 2.2, 0.2); const k = isk(c[3], d); look(V(lerp(300, 420, k), lerp(150, 220, k), lerp(420, 640, k)), V(40, 0, 0), 38, 0, 0.4, tg); flare = 1;
      card("final", "Less than a movie.<br><b class='gold'>Mars, on the first try.</b>", { x: 410, y: 150, w: 1100, k: fin(t, c[2] + 6.0), cls: "center big" }); }
  }
  else {   // end card
    mars.visible = marsAtmo.visible = marsHaze.visible = true; look(V(0, 60, 420), V(0, 0, 0), 38, 0, 0.3, tg);
    card("banner", "<img src='assets/banner.png' alt='Modus & Raison banner'>", { x: 460, y: 110, w: 1000, k: fin(t, 0.3, 0.6), cls: "banner" });
    card("like", "👍 LIKE", { x: 610, y: 720, w: 300, k: fin(t, c[0] + 1.2, 0.4), cls: "btn blue" }); card("sub", "SUBSCRIBE", { x: 1010, y: 720, w: 300, k: fin(t, c[0] + 1.8, 0.4), cls: "btn red" });
    card("credits", "Aircraft-engine recording used in the launch: InspectorJ (freesound.org), CC BY 4.0 · Sources: ISRO, NASA, JAXA, RBI, The Planetary Society, Spaceflight Now", { x: 260, y: 880, w: 1400, k: fin(t, 1.0), cls: "center tiny" });
  }
  const shake = 0; renderer.toneMappingExposure = exp; bloom.strength = bloomK; bokeh.uniforms.focus.value = focus; bokeh.uniforms.aperture.value = aper; bokeh.enabled = aper > 0; sunFlare.intensity = flare;
  CHIP.textContent = sc.title ? sc.title.toUpperCase() : ""; CHIP.style.opacity = sc.title ? fin(t, 0.3, 0.4) * (1 - fin(t, d - 0.5, 0.4)) : 0; SRC.textContent = SOURCES[id] || ""; SRC.style.opacity = SOURCES[id] ? fin(t, 0.8) : 0;
  return { cam, useRoom, sc, t };
}

// ---------------------------------------------------------------- frame: motion-blurred average of sub-frames
window.renderAt = function (tg) {
  const t0 = clamp(tg, 0, TM.total - 0.001), shutter = 0.5 / FPS; let info;
  for (const k in OV) OV[k]._used = false;
  for (let i = 0; i < MB; i++) { const t = MB > 1 ? clamp(t0 - shutter / 2 + shutter * (i + 0.5) / MB, 0, TM.total - 0.001) : t0;
    info = shot(t); rpass.scene = info.useRoom ? room : scene; rpass.camera = info.cam; bokeh.scene = rpass.scene; bokeh.camera = info.cam; lens.uniforms.seed.value = Math.floor(t0 * FPS) * 1.37 + i; composer.render(); ax.globalAlpha = 1 / (i + 1); ax.drawImage(glc, 0, 0); }
  for (const k in OV) if (!OV[k]._used) OV[k].style.opacity = 0;
  const sc = info.sc, fade = Math.min(fin(info.t, 0, 0.35), 1 - fin(info.t, sc.dur - 0.35, 0.35)); $("#veil").style.opacity = sc === TM.scenes[0] ? 1 - fin(info.t, 0, 0.6) : 1 - Math.max(0, fade);
};
window.AUDIT3D = function () { const out = []; for (const s of SUBJ) { const b = projBox(s.objs, s.cam || camera); if (b) out.push({ n: s.n, ...b, subject: true, panel: [0, 1920] }); } return { split: false, boxes: out }; };
function projBox(objs, cam, dx = 0) { const b = new THREE.Box3(); objs.forEach(o => { if (!o.visible) return; o.updateMatrixWorld(true); o.traverseVisible(ch => { if ((ch.isMesh || ch.isPoints) && ch.geometry) { if (!ch.geometry.boundingBox) ch.geometry.computeBoundingBox(); b.union(ch.geometry.boundingBox.clone().applyMatrix4(ch.matrixWorld)); } }); }); if (b.isEmpty()) return null; let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  for (let i = 0; i < 8; i++) { const p = V(i & 1 ? b.max.x : b.min.x, i & 2 ? b.max.y : b.min.y, i & 4 ? b.max.z : b.min.z).project(cam); if (p.z > 1) return null; const x = (p.x + 1) / 2 * W + dx, y = (1 - p.y) / 2 * H; x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); } return { x0, y0, x1, y1 }; }
window.DUR = TM.total;
await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => 0))); renderAt(parseFloat(Q.get("t")) || 0); window.READY = true;
