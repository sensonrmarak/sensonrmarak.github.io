// Mars video, cold open in 3D, VFX pass 2. renderAt(t) poses everything from t; motion blur averages sub-frames inside the shutter.
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
const TM = await (await fetch("timings.json")).json(), L = TM.scenes[0].lines, c = L.map(l => l.start), [B0, B1] = TM.burn, WIN = c[5], SPLIT = c[3] + (L[3].marks.twelve ?? 2.8) - 0.4, SPLIT_END = WIN + 2.4;
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
const mirror = new Reflector(new THREE.PlaneGeometry(60, 60), { textureWidth: 512 * PR, textureHeight: 512 * PR, color: 0x555566 }); mirror.rotation.x = -Math.PI / 2; BAR.add(mirror);
const floorVeil = new THREE.Mesh(new THREE.CircleGeometry(30, 64), new THREE.MeshBasicMaterial({ color: 0x05060a, transparent: true, opacity: 0.72 })); floorVeil.rotation.x = -Math.PI / 2; floorVeil.position.y = 0.01; BAR.add(floorVeil);
const barLight = new THREE.SpotLight(0xffffff, 0, 80, 0.6, 0.6); barLight.position.set(-6, 22, 14); barLight.target.position.set(0, 3, 0); BAR.add(barLight, barLight.target);
const reel = new THREE.Group(); { const disc = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 0.22, 48), new THREE.MeshStandardMaterial({ color: 0x2a2d36, metalness: 0.7, roughness: 0.3, envMap: envTex })); disc.rotation.x = Math.PI / 2; reel.add(disc);
  for (let i = 0; i < 6; i++) { const h = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.26, 24), new THREE.MeshBasicMaterial({ color: 0x0b0c12 })); h.rotation.x = Math.PI / 2; h.position.set(Math.cos(i * 1.047) * 0.52, Math.sin(i * 1.047) * 0.52, 0); reel.add(h); } } BAR.add(reel);
const skipIdx = new Set([plumeCore, plumeGlow, sparks, flash, ...rcs].map(o => craft.children.indexOf(o)).filter(i => i >= 0)), mini = craft.clone(true); mini.children = mini.children.filter((_, i) => !skipIdx.has(i));

// ---------------------------------------------------------------- mission control, Bengaluru (stylised): desks, screens, people who wait and then cheer
const room = new THREE.Scene(), roomCam = new THREE.PerspectiveCamera(44, W / H, 0.1, 200); room.add(new THREE.AmbientLight(0x6070a0, 1.3), new THREE.HemisphereLight(0xbfd4ff, 0x202a40, 1.2)); [-3, 0, 3].forEach(x => { const pl = new THREE.PointLight(0x8fc4ff, 6, 10, 2); pl.position.set(x, 1.6, -0.5); room.add(pl); });
const roomKey = new THREE.SpotLight(0xbfd4ff, 40, 60, 0.9, 0.7); roomKey.position.set(0, 9, 6); room.add(roomKey, roomKey.target);
const screenTex = (msg, col) => { const cv = document.createElement("canvas"); cv.width = 1024; cv.height = 400; const x = cv.getContext("2d"); x.fillStyle = "#06101f"; x.fillRect(0, 0, 1024, 400); x.strokeStyle = "rgba(90,170,255,.35)"; for (let i = 0; i < 1024; i += 64) { x.beginPath(); x.moveTo(i, 0); x.lineTo(i, 400); x.stroke(); }
  x.fillStyle = "#8fc4ff"; x.font = "700 44px Body, Arial"; x.fillText("MARS ORBITER MISSION · ORBIT INSERTION", 40, 80); x.fillStyle = col; x.font = "900 96px Body, Arial"; x.fillText(msg, 40, 230); x.strokeStyle = "#ff9a5a"; x.lineWidth = 4; x.beginPath(); for (let i = 0; i < 900; i += 6) x.lineTo(40 + i, 330 - Math.sin(i * 0.03) * 22 - i * 0.02); x.stroke();
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
const look = (pos, tgt, fov = 35, roll = 0, w = 0, t = 0) => { camera.position.copy(pos).add(wob(t, w)); camera.up.set(Math.sin(roll), Math.cos(roll), 0); camera.lookAt(tgt.clone().add(wob(t + 3.7, w * 0.6))); camera.fov = fov; camera.updateProjectionMatrix(); camera.updateMatrixWorld(); };
$("#src").textContent = "Sources: ISRO · The Planetary Society · NASA";

// ---------------------------------------------------------------- one pose of the whole world at time t
function pose(t) {
  const burnK = seg(t, B0, B0 + 0.5) * (1 - seg(t, B1 - 0.3, B1)), heat = t < B0 ? 0 : t < B1 ? seg(t, B0, B0 + 3) : Math.exp(-(t - B1) * 0.35), orbitK = E.io(seg(t, WIN - 0.1, WIN + 2.4));
  const eclipse = seg(t, B0 - 0.8, B0 + 0.2) * (1 - seg(t, B1 + 0.2, B1 + 1.2));            // the real burn ran in Mars's shadow
  mars.rotation.y = -2.2 + t * 0.006; earth.rotation.y = t * 0.05; clouds.rotation.y = t * 0.065;
  phobos.position.set(Math.cos(t * 0.09 + 1) * 277, Math.sin(t * 0.09 + 1) * 30, Math.sin(t * 0.09 + 1) * 277 * 0.8); phobos.rotation.set(t * 0.1, t * 0.09, 0); deimos.position.set(Math.cos(t * 0.03 + 4) * 690, 60, Math.sin(t * 0.03 + 4) * 690); deimos.rotation.y = t * 0.05;
  [orbit, inbound, ghost, ...rings, BAR].forEach(o => o.visible = false); craft.visible = true; mars.visible = marsAtmo.visible = marsHaze.visible = true;
  if (t < c[3]) { inbound.visible = true; inbound.material.uniforms.p.value = 1; inbound.material.uniforms.o.value = 0.3; inbound.material.uniforms.head.value = 0; }
  const capture = Math.PI * 0.92, inU = seg(t, 0, c[4] + 1.0), onIn = INB[Math.min(199, Math.floor(E.out(inU) * 199))], th = t < WIN ? capture : capture + (t - WIN) * 0.16;
  const cpos = t < c[4] + 1.0 ? onIn.clone() : orbitPt(t < WIN ? capture : th); craft.position.copy(cpos);
  const vel = t < WIN ? INB[199].clone().sub(INB[150]).normalize() : orbitPt(th + 0.01).sub(orbitPt(th)).normalize(), turn = E.io(seg(t, c[2] + 0.6, B0 - 0.1));
  craft.quaternion.setFromUnitVectors(V(1, 0, 0), vel); craft.rotateY(turn * Math.PI); craft.rotateX(0.25 + Math.sin(t * 0.3) * 0.04); if (t >= WIN) craft.rotateY(Math.PI);
  plumeCore.material.uniforms.k.value = plumeGlow.material.uniforms.k.value = burnK; plumeCore.material.uniforms.t.value = plumeGlow.material.uniforms.t.value = t; plumeCore.visible = plumeGlow.visible = burnK > 0.01;
  { const P = spG.attributes.position.array; for (let i = 0; i < SPARK; i++) { const [ph, a, b, sp] = SPR[i], age = (t * sp * 1.4 + ph) % 1; P[i * 3] = -1.3 - age * 5 * burnK; P[i * 3 + 1] = a * age * 0.7; P[i * 3 + 2] = b * age * 0.7; } spG.attributes.position.needsUpdate = true; sparks.material.opacity = burnK * 0.6; sparks.visible = burnK > 0.01; }
  heatMat.emissiveIntensity = heat * 2.2;
  const puff = Math.max(Math.exp(-(((t - (c[2] + 0.65)) / 0.12) ** 2)), Math.exp(-(((t - (B0 - 0.15)) / 0.12) ** 2))); rcs.forEach((s, i) => { s.material.opacity = puff; s.visible = puff > 0.02; s.scale.setScalar(0.4 + puff * 0.6); });
  const nz = V(-1.35, 0, 0).applyQuaternion(craft.quaternion).add(cpos); flash.position.copy(nz); flash.intensity = burnK * 9 + Math.exp(-(((t - B0) / 0.15) ** 2)) * 45;
  sun.intensity = 2.7; const dimK = 1 - 0.9 * eclipse; CRAFT_MATS.forEach(([m, base, env]) => { m.color.copy(base).multiplyScalar(dimK); if (m.envMapIntensity !== undefined) m.envMapIntensity = env * dimK; }); sun.position.copy(cpos.clone().add(SUN.clone().multiplyScalar(40))); sun.target.position.copy(cpos);
  const toCraft = cpos.clone().normalize(); bounce.position.copy(toCraft.clone().multiplyScalar(-1).add(cpos)); bounce.target.position.copy(cpos); bounce.intensity = 0.35 * (1 - 0.5 * eclipse);
  return { burnK, eclipse, orbitK, cpos, vel };
}
function shoot(t) {   // camera for time t; returns post settings
  const { burnK, cpos, vel, orbitK } = pose(t); let fov = 35, exp = 1.0, aper = 0.00012, focus = camera.position.distanceTo(cpos), flare = 1, split = t >= SPLIT && t < SPLIT_END;
  if (t < c[1]) { const k = seg(t, 0, c[1]); look(cpos.clone().add(V(lerp(-9, 5, k), lerp(2, 0.8, k), lerp(16, 13, k))), cpos.clone().add(V(lerp(30, 4, E.io(k)), 0, -20 * (1 - k))), 32, 0, 0.25, t); aper = 0.00025; }
  else if (t < c[2]) { const k = E.io(seg(t, c[1], c[2])), back = vel.clone().multiplyScalar(-lerp(15, 11, k)), side = V(0, 1, 0).cross(vel).normalize().multiplyScalar(lerp(6, 9, k));
    look(cpos.clone().add(back).add(side).add(V(0, lerp(1.6, 0.6, k), 0)), cpos.clone().add(vel.clone().multiplyScalar(9)), lerp(36, 32, k), lerp(0.04, -0.03, k), 0.3, t); exp = 0.68; flare = 0; aper = 0.0002; }
  else if (t < c[3]) { const k = E.io(seg(t, c[2], c[3])), side = V(0, 1, 0).cross(vel).normalize();
    look(cpos.clone().add(side.clone().multiplyScalar(lerp(14, 11, k))).add(vel.clone().multiplyScalar(lerp(-3, 4, k))).add(V(0, lerp(-2.4, -1, k), 0)), cpos.clone().add(V(0, 0.3, 0)).add(vel.clone().multiplyScalar(-2)), 32, 0.05, 0.2, t); aper = 0.0004; exp = lerp(1.0, 1.1, seg(t, B0 - 0.8, B0 + 0.4)); }
  else if (t < SPLIT) { const k = E.io(seg(t, c[3], SPLIT)); look(V(lerp(-150, -120, k), lerp(210, 190, k), lerp(640, 600, k)), V(-290, 15, -430), 42, 0, 1.5, t); aper = 0;
    rings.forEach((m, i) => { const u = ((t - c[3]) * 0.045 + i * 0.05) % 1; m.visible = true; m.position.lerpVectors(EARTH, V(0, 0, 0), 0.07 + u * 0.5); m.lookAt(V(0, 0, 0)); m.scale.setScalar(1 + u * 1.5); m.material.opacity = Math.max(0, 0.9 - u * 1.6); }); craft.scale.setScalar(7); }
  else if (t < WIN) { const k = E.io(seg(t, SPLIT, WIN)); ghost.visible = true; ghost.material.uniforms.p.value = fin(t, c[4] + 0.3, 1.8); ghost.material.uniforms.o.value = fin(t, c[4] + 0.3, 1) * (1 - fin(t, WIN - 0.5, 0.4));
    look(cpos.clone().add(V(lerp(-14, -18, k), lerp(-3, -4, k), lerp(16, 22, k))), cpos.clone().add(V(20, -8, -30)), 36, -0.08, 0.25, t); aper = 0.0002; exp = 1.25; }
  else if (t < c[7]) { const k = E.io(seg(t, WIN, WIN + 3)); orbit.visible = true; orbit.material.uniforms.p.value = lerp(0.1, 1, orbitK); orbit.material.uniforms.head.value = 1 - seg(t, WIN + 2.2, WIN + 2.6);
    const wide = V(lerp(cpos.x - 30, 160, k), lerp(cpos.y + 10, 260, k), lerp(cpos.z + 60, 560, k)), ride = cpos.clone().add(V(-10, 6, 18)), r2 = E.io(seg(t, c[6] + 3, c[7]));
    look(t < c[6] ? wide : wide.lerp(ride, r2), t < c[6] ? V(lerp(cpos.x, 0, k), 0, lerp(cpos.z, 0, k)) : V(0, 0, 0).lerp(cpos, r2), 36, 0, 1.2 * (1 - r2) + 0.2, t); aper = r2 * 0.0002; }
  else if (t < c[8]) { const k = E.io(seg(t, c[7], c[8])); look(cpos.clone().add(V(lerp(-10, -7, k), lerp(5, 3, k), lerp(16, 11, k))), cpos.clone().add(V(0, 0.4, 0)), 32, 0, 0.18, t); aper = 0.0005; }
  else if (t < c[9] - 0.15) { BAR.visible = true; mars.visible = marsAtmo.visible = marsHaze.visible = false; craft.visible = false; barLight.intensity = 40; const kg = E.out(seg(t, c[8] + 0.1, c[8] + 1.2)), km = E.out(seg(t, c[8] + 0.6, c[8] + 1.7)), Hm = 9;
    barG.scale.set(2.6, Math.max(0.01, Hm * kg), 2.6); barG.position.set(-2.4, Hm * kg / 2, 0); barM.scale.set(2.6, Math.max(0.01, Hm * 0.74 * km), 2.6); barM.position.set(2.4, Hm * 0.74 * km / 2, 0);
    reel.position.set(-2.4, Hm * kg + 1.4, 0); reel.rotation.z = t * 1.5; if (!mini.parent) BAR.add(mini); mini.scale.setScalar(0.32); mini.position.set(2.4, Hm * 0.74 * km + 1.3, 0); mini.rotation.y = t * 0.8;
    const k = seg(t, c[8], c[9]); look(BO.clone().add(V(lerp(-6, 4, k), lerp(5, 7, k), lerp(26, 23, k))), BO.clone().add(V(0, 4.8, 0)), 38, 0, 0.15, t); focus = 25; aper = 0.0002; flare = 0; }
  else { craft.visible = false; const k = E.io(seg(t, c[9] - 0.15, TM.total)), cam = V(-20, 108, 52).normalize().multiplyScalar(lerp(118, 124, k)), cd = cam.clone().negate().normalize(), T = SUN.clone().sub(cd.clone().multiplyScalar(SUN.dot(cd))).normalize(), a = lerp(0.36, 0.3, k);
    look(cam, cam.clone().add(T.clone().multiplyScalar(Math.cos(a)).add(cd.clone().multiplyScalar(Math.sin(a))).multiplyScalar(100)), 46, 0, 0.1, t); aper = 0; flare = 1.3; }
  if (t < c[3] || t >= SPLIT) craft.scale.setScalar(1); if (t >= c[8] && t < c[9] - 0.15) {} else barLight.intensity = 0;
  if (split) camera.setViewOffset(W, H, W * 0.25, 0, W, H); else camera.clearViewOffset(); camera.updateProjectionMatrix();
  const shake = burnK * 0.035; camera.position.add(V(Math.sin(t * 61) * shake, Math.cos(t * 53) * shake, 0)); camera.updateMatrixWorld();
  sunFlare.intensity = flare; renderer.toneMappingExposure = exp; bokeh.uniforms.focus.value = focus; bokeh.uniforms.aperture.value = aper; bokeh.enabled = aper > 0;
  bloom.strength = (t >= c[8] && t < c[9] - 0.15 ? 0.2 : 0.5) + 0.45 * burnK + 0.6 * (t > WIN && t < WIN + 1 ? 1 - seg(t, WIN, WIN + 1) : 0);
  return { split, cpos };
}
function room_pose(t) {   // mission control: waiting, then the cheer
  const cheer = seg(t, WIN + 0.15, WIN + 0.6); wall.material.map = t < WIN + 0.1 ? waitTex : okTex; wall.material.needsUpdate = true;
  people.forEach(({ p, arms, d, jump }, i) => { const k = seg(t, WIN + 0.15 + d, WIN + 0.5 + d); arms.forEach((a, s) => { a.rotation.z = (s ? 1 : -1) * lerp(0.25, 2.7, E.back(k)) + Math.sin(t * 9 + i) * 0.15 * k; }); p.position.y = (Math.floor(i / 6) * 0.25) + Math.abs(Math.sin(t * 7 + jump * 6)) * 0.18 * k; p.rotation.y = Math.sin(t * 0.7 + i) * 0.1; });
  const k = seg(t, SPLIT, SPLIT_END); roomCam.position.set(lerp(-1.2, 1.0, k), lerp(3.6, 3.3, k), lerp(15.5, 14, k)); roomCam.lookAt(0, 2.9, -2); roomCam.updateMatrixWorld(); roomKey.target.position.set(0, 1, -1);
}

// ---------------------------------------------------------------- frame = motion-blurred average of sub-frames; split screen composited on the 2D canvas
window.renderAt = function (tg) {
  const t0 = clamp(tg, 0, TM.total - 0.001), shutter = 0.5 / FPS; ax.setTransform(1, 0, 0, 1, 0, 0); ax.globalCompositeOperation = "source-over"; let info;
  for (let i = 0; i < MB; i++) { const t = MB > 1 ? clamp(t0 - shutter / 2 + shutter * (i + 0.5) / MB, 0, TM.total - 0.001) : t0;
    info = shoot(t); lens.uniforms.seed.value = Math.floor(t0 * FPS) * 1.37 + i; rpass.scene = scene; rpass.camera = camera; bokeh.scene = scene; bokeh.camera = camera; composer.render();
    ax.globalAlpha = 1 / (i + 1);
    if (info.split) { ax.drawImage(glc, 0, 0, glc.width / 2, glc.height, 0, 0, acc.width / 2, acc.height);
      if (i === 0) { room_pose(t0); rpass.scene = room; rpass.camera = roomCam; bokeh.enabled = false; composer.render(); ROOMC.width = glc.width / 2; ROOMC.height = glc.height; ROOMC.getContext('2d').drawImage(glc, glc.width / 4, 0, glc.width / 2, glc.height, 0, 0, glc.width / 2, glc.height); }
      ax.drawImage(ROOMC, acc.width / 2, 0, acc.width / 2, acc.height);
      ax.globalAlpha = 1; ax.fillStyle = "rgba(255,255,255,.85)"; ax.fillRect(acc.width / 2 - 2 * PR, 0, 4 * PR, acc.height); }
    else ax.drawImage(glc, 0, 0); }
  overlays(t0, info);
};
function overlays(t, { split, cpos }) {
  const tp = toScreen(cpos.clone().add(V(0, -1.8, 0)));
  show("#date", fin(t, 0.6, 0.8) * (1 - fin(t, c[1] - 0.2, 0.4)));
  show("#dist", fin(t, c[1] + 0.3) * (1 - fin(t, c[2] - 0.2, 0.3))); show("#dist2", fin(t, c[1] + 0.8) * (1 - fin(t, c[2] - 0.2, 0.3)));
  { const k = fin(t, c[1] + 4.0) * (1 - fin(t, c[2] - 0.2, 0.3)); $("#scale").style.left = tp[0] - 160 + "px"; $("#scale").style.top = tp[1] + 30 + "px"; show("#scale", k); }
  show("#burn", fin(t, c[2] + 1.5) * (1 - fin(t, c[3] - 0.2, 0.3)));
  { const e = $("#clock"), e2 = $("#clock2"); e.style.left = e2.style.left = split ? "960px" : "0px"; e.style.width = e2.style.width = split ? "960px" : "1920px"; e.style.top = split ? "880px" : "150px"; e2.style.top = split ? "985px" : "258px"; const left = Math.max(0, 12.5 * 60 * (1 - seg(t, SPLIT, WIN))), mm = Math.floor(left / 60), ss = Math.floor(left % 60);
    e.innerHTML = split ? `${String(mm).padStart(2, "0")}:${String(ss).padStart(2, "0")}` : '12.5 <span style="font-size:56px">MIN</span>'; e2.textContent = split ? (t < WIN ? "until Earth hears back (time-lapse)" : "signal received") : "one way, at the speed of light";
    show("#clock", fin(t, c[3] + 2.2) * (1 - fin(t, SPLIT_END - 0.3, 0.3))); show("#clock2", fin(t, c[3] + 2.6) * (1 - fin(t, SPLIT_END - 0.3, 0.3))); }
  show("#miss", fin(t, c[4] + 0.5) * (1 - fin(t, WIN - 0.6, 0.4)));
  { const k = pop(t, WIN + 0.05, 0.45); $("#works").style.opacity = clamp(k * 2) * (1 - fin(t, c[6] - 0.2, 0.3)); $("#works").style.transform = `scale(${(0.6 + 0.4 * k).toFixed(3)})`; $("#works").style.top = split ? "170px" : "150px"; $("#works").style.width = split ? "960px" : "1920px"; }
  show("#first1", fin(t, c[6] + 1.0) * (1 - fin(t, c[7] - 0.3, 0.3))); show("#first2", fin(t, c[6] + 4.0) * (1 - fin(t, c[7] - 0.3, 0.3)));
  if (t >= c[7] && t < c[8]) { const [sx, sy] = toScreen(cpos.clone().add(V(0, 2.6, 0))), e = $("#price"), pk = pop(t, c[7] + 1.2, 0.5); e.style.left = sx - 170 + "px"; e.style.top = sy - 110 + "px"; e.style.opacity = clamp(pk * 3); e.style.transform = `scale(${pk.toFixed(3)}) rotate(-4deg)`; const e2 = $("#price2"); e2.style.left = sx - 110 + "px"; e2.style.top = sy - 28 + "px"; e2.style.opacity = fin(t, c[7] + 1.6); }
  else { $("#price").style.opacity = 0; $("#price2").style.opacity = 0; }
  if (t >= c[8] && t < c[9] - 0.15) { const kg = E.out(seg(t, c[8] + 0.1, c[8] + 1.2)), km = E.out(seg(t, c[8] + 0.6, c[8] + 1.7));
    [["#barG", `<b>$${Math.round(100 * kg)}M</b><br>GRAVITY<br><small>Hollywood film, 2013</small>`, -2.4], ["#barM", `<b>$${Math.round(74 * km)}M</b><br>MARS ORBITER MISSION<br><small>ISRO, 2013–14</small>`, 2.4]].forEach(([id, h, x]) => { const [sx, sy] = toScreen(BO.clone().add(V(x, -1.4, 0))), e = $(id); e.style.left = sx - 200 + "px"; e.style.top = sy + "px"; e.style.opacity = fin(t, c[8] + 0.6); e.innerHTML = h; }); }
  else { $("#barG").style.opacity = 0; $("#barM").style.opacity = 0; }
  show("#title", fin(t, c[9] - 0.1, 0.5), 40);
  // telemetry: what the spacecraft is doing, live
  const hk = fin(t, c[1] + 1.0) * (1 - fin(t, WIN + 3.2, 0.5)), burnT = clamp((t - B0) / (B1 - B0)) * 24, dv = Math.round(1099 * E.io(clamp((t - B0) / (B1 - B0))));
  const status = t < c[2] + 0.6 ? "CRUISE · APPROACHING MARS" : t < B0 ? "TURNING ENGINE TO FACE FORWARD" : t < B1 ? "MAIN ENGINE FIRING · IN MARS'S SHADOW · AUTONOMOUS" : t < WIN ? "BURN COMPLETE · WAITING FOR CONFIRMATION" : "CAPTURED · IN MARS ORBIT";
  $("#hud").style.opacity = hk; $("#hud").style.left = "60px"; $("#hst").textContent = status; $("#hst").style.color = t >= B0 && t < B1 ? "#ffb35c" : t >= WIN ? "#7dffa0" : "#cfe3ff";
  $("#hburn").textContent = `${String(Math.floor(burnT)).padStart(2, "0")}:${String(Math.floor((burnT % 1) * 60)).padStart(2, "0")}`; $("#hdv").textContent = `${dv.toLocaleString("en-US")} m/s`;
  $("#flash").style.opacity = (t > WIN && t < WIN + 0.5 ? 0.25 * (1 - seg(t, WIN, WIN + 0.5)) : 0) + (t > c[9] && t < c[9] + 0.3 ? 0.2 * (1 - seg(t, c[9], c[9] + 0.3)) : 0);
  $("#src").style.opacity = fin(t, 1.0) * (t < c[9] && !split ? 1 : 0); $("#split").style.opacity = split ? 1 : 0;
}
window.DUR = TM.total;
await document.fonts.ready; renderAt(parseFloat(Q.get("t")) || 0); window.READY = true;
