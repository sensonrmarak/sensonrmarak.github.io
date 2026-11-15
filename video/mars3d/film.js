// Mars video, cold open in 3D (three.js). Every frame is a pure function of time: renderAt(t) poses the scene, then renders it.
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const W = 1920, H = 1080, Q = new URLSearchParams(location.search), PR = parseFloat(Q.get("pr")) || 1;
const TM = await (await fetch("timings.json")).json(), L = TM.scenes[0].lines, c = L.map(l => l.start), [B0, B1] = TM.burn, WIN = c[5];
const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x), lerp = (a, b, k) => a + (b - a) * k, seg = (t, a, b) => clamp((t - a) / (b - a));
const E = { out: x => 1 - (1 - x) ** 3, in: x => x ** 3, io: x => (x < 0.5 ? 4 * x ** 3 : 1 - (-2 * x + 2) ** 3 / 2), back: x => { const k = 1.70158; return 1 + (k + 1) * (x - 1) ** 3 + k * (x - 1) ** 2; } };
const fin = (t, a, d = 0.5) => E.out(seg(t, a, a + d)), pop = (t, a, d = 0.5) => E.back(seg(t, a, a + d));
function rng(seed) { let s = seed >>> 0; return () => { s = (s + 0x6d2b79f5) | 0; let x = Math.imul(s ^ (s >>> 15), 1 | s); x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x; return ((x ^ (x >>> 14)) >>> 0) / 4294967296; }; }
const $ = s => document.querySelector(s), V = (x, y, z) => new THREE.Vector3(x, y, z);

// ---------------------------------------------------------------- 3D value noise (seamless on a sphere), fbm
const PERM = (() => { const r = rng(42), p = Array.from({ length: 256 }, (_, i) => i); for (let i = 255; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [p[i], p[j]] = [p[j], p[i]]; } return Uint8Array.from([...p, ...p]); })();
const fade = t => t * t * (3 - 2 * t), hash = (x, y, z) => PERM[(PERM[(PERM[x & 255] + y) & 255] + z) & 255] / 255;
function vnoise(x, y, z) { const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), xf = fade(x - xi), yf = fade(y - yi), zf = fade(z - zi);
  const l = (a, b, k) => a + (b - a) * k, h = (dx, dy, dz) => hash(xi + dx, yi + dy, zi + dz);
  return l(l(l(h(0, 0, 0), h(1, 0, 0), xf), l(h(0, 1, 0), h(1, 1, 0), xf), yf), l(l(h(0, 0, 1), h(1, 0, 1), xf), l(h(0, 1, 1), h(1, 1, 1), xf), yf), zf); }
function fbm(x, y, z, oct = 6) { let s = 0, a = 0.5, f = 1; for (let i = 0; i < oct; i++) { s += a * vnoise(x * f, y * f, z * f); f *= 2.03; a *= 0.5; } return s; }

// ---------------------------------------------------------------- procedural planet textures (equirectangular)
function planetMaps(w, h, shade) { const col = document.createElement("canvas"), bmp = document.createElement("canvas"); col.width = bmp.width = w; col.height = bmp.height = h;
  const ci = col.getContext("2d").createImageData(w, h), bi = bmp.getContext("2d").createImageData(w, h);
  for (let j = 0; j < h; j++) { const lat = (0.5 - j / h) * Math.PI, cl = Math.cos(lat), sl = Math.sin(lat);
    for (let i = 0; i < w; i++) { const lon = (i / w) * 2 * Math.PI, x = cl * Math.cos(lon), y = sl, z = cl * Math.sin(lon), [r, g, b, hgt] = shade(x, y, z, lat, lon), k = (j * w + i) * 4;
      ci.data[k] = r; ci.data[k + 1] = g; ci.data[k + 2] = b; ci.data[k + 3] = 255; bi.data[k] = bi.data[k + 1] = bi.data[k + 2] = hgt; bi.data[k + 3] = 255; } }
  col.getContext("2d").putImageData(ci, 0, 0); bmp.getContext("2d").putImageData(bi, 0, 0);
  const T = cvs => { const t = new THREE.CanvasTexture(cvs); t.anisotropy = 8; return t; }, a = T(col); a.colorSpace = THREE.SRGBColorSpace; return [a, T(bmp)]; }
const CR = (() => { const r = rng(9); return Array.from({ length: 140 }, () => { const u = r() * 2 - 1, th = r() * 6.2832, s = Math.sqrt(1 - u * u); return [s * Math.cos(th), u, s * Math.sin(th), 0.008 + r() ** 3 * 0.07]; }); })();
const marsShade = (x, y, z, lat, lon) => {
  const n = fbm(x * 2.2 + 7, y * 2.2, z * 2.2, 6), d = fbm(x * 6 + 3, y * 6, z * 6, 4), hi = clamp((n - 0.42) * 3.2);   // highlands vs dark plains
  let cr = 0; for (const [cx, cy, cz, s] of CR) { const dd = Math.hypot(x - cx, y - cy, z - cz); if (dd < s * 1.6) { const q = dd / s; cr += q < 1 ? -0.5 * (1 - q * q) : 0.35 * Math.exp(-((q - 1.15) ** 2) * 18); } }
  const canyon = Math.exp(-((((lat + 0.12) - 0.08 * Math.sin(lon * 3)) / 0.025) ** 2)) * (lon > 4.2 && lon < 5.4 ? 1 : 0);
  let r = lerp(118, 205, hi) + d * 40, g = lerp(52, 108, hi) + d * 22, b = lerp(34, 66, hi) + d * 12; const dk = 1 + cr * 0.35 - canyon * 0.45; r *= dk; g *= dk; b *= dk;
  const cap = clamp((Math.abs(lat) - 1.25 + (fbm(x * 8, y * 8, z * 8, 3) - 0.5) * 0.25) * 9); r = lerp(r, 245, cap); g = lerp(g, 238, cap); b = lerp(b, 232, cap);
  return [clamp(r, 0, 255), clamp(g, 0, 255), clamp(b, 0, 255), clamp(110 + (n - 0.5) * 160 + d * 40 + cr * 120 - canyon * 90, 0, 255)]; };
const earthShade = (x, y, z, lat) => { const n = fbm(x * 1.8 + 2, y * 1.8, z * 1.8, 6), land = n > 0.52, ice = Math.abs(lat) > 1.2;
  if (ice) return [235, 240, 245, 200]; if (!land) { const dp = clamp((0.52 - n) * 4); return [lerp(30, 12, dp), lerp(90, 40, dp), lerp(170, 110, dp), 60]; }
  const m = fbm(x * 5, y * 5, z * 5, 4); return Math.abs(lat) < 0.45 && m > 0.5 ? [182, 150, 96, 150] : [lerp(50, 110, m), lerp(110, 130, m), lerp(50, 70, m), 140]; };
const cloudShade = (x, y, z) => { const n = fbm(x * 3 + 11, y * 3, z * 3, 6), v = clamp((n - 0.5) * 3.2) * 255; return [255, 255, 255, v]; };
function foilMap() { const cv = document.createElement("canvas"); cv.width = cv.height = 512; const x = cv.getContext("2d"), id = x.createImageData(512, 512);   // crinkled multilayer insulation, as a normal map
  for (let j = 0; j < 512; j++) for (let i = 0; i < 512; i++) { const a = fbm(i / 40, j / 40, 1.3, 4), b = fbm(i / 40 + 9, j / 40, 2.1, 4), k = (j * 512 + i) * 4; id.data[k] = 128 + (a - 0.5) * 300; id.data[k + 1] = 128 + (b - 0.5) * 300; id.data[k + 2] = 255; id.data[k + 3] = 255; }
  x.putImageData(id, 0, 0); const t = new THREE.CanvasTexture(cv); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; }
function cellMap() { const cv = document.createElement("canvas"); cv.width = 512; cv.height = 256; const x = cv.getContext("2d"); x.fillStyle = "#0d1a4a"; x.fillRect(0, 0, 512, 256);
  for (let i = 0; i < 16; i++) for (let j = 0; j < 8; j++) { const gr = x.createLinearGradient(i * 32, j * 32, i * 32 + 32, j * 32 + 32); gr.addColorStop(0, "#1f3a9a"); gr.addColorStop(1, "#14256c"); x.fillStyle = gr; x.fillRect(i * 32 + 2, j * 32 + 2, 28, 28); }
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; return t; }

// ---------------------------------------------------------------- renderer, post-processing
const canvas = $("#gl"), renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(PR); renderer.setSize(W, H, false); renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05; renderer.outputColorSpace = THREE.SRGBColorSpace;
const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(35, W / H, 0.05, 20000);
const pm = new THREE.PMREMGenerator(renderer), envTex = pm.fromScene(new RoomEnvironment(), 0.04).texture;
const composer = new EffectComposer(renderer); composer.setPixelRatio(PR); composer.setSize(W, H); composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), 0.6, 0.5, 0.9); composer.addPass(bloom); composer.addPass(new OutputPass());

// ---------------------------------------------------------------- lights and sky
const SUN = V(-1, 0.35, 0.6).normalize(), sun = new THREE.DirectionalLight(0xfff2e0, 2.7); sun.position.copy(SUN.clone().multiplyScalar(500)); scene.add(sun, new THREE.AmbientLight(0x223355, 0.08));
{ const r = rng(5), n = 9000, pos = new Float32Array(n * 3), col = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) { const u = r() * 2 - 1, th = r() * 6.2832, s = Math.sqrt(1 - u * u), band = Math.abs(u - 0.15) < 0.12 && r() < 0.6, R = 9000; pos.set([s * Math.cos(th) * R, (band ? u * 0.4 + 0.06 : u) * R, s * Math.sin(th) * R], i * 3);
    const k = 0.4 + r() ** 3 * 1.6, tint = r(); col.set([k * (tint < 0.2 ? 1 : 0.85), k * 0.9, k * (tint > 0.7 ? 1.1 : 0.9)], i * 3); }
  const gm = new THREE.BufferGeometry(); gm.setAttribute("position", new THREE.BufferAttribute(pos, 3)); gm.setAttribute("color", new THREE.BufferAttribute(col, 3));
  scene.add(new THREE.Points(gm, new THREE.PointsMaterial({ size: 1.7 * PR, sizeAttenuation: false, vertexColors: true, depthWrite: false }))); }
const sunGlow = new THREE.Sprite(new THREE.SpriteMaterial({ map: (() => { const cv = document.createElement("canvas"); cv.width = cv.height = 256; const x = cv.getContext("2d"), gr = x.createRadialGradient(128, 128, 0, 128, 128, 128); gr.addColorStop(0, "rgba(255,255,240,1)"); gr.addColorStop(0.1, "rgba(255,230,180,.8)"); gr.addColorStop(1, "rgba(255,180,120,0)"); x.fillStyle = gr; x.fillRect(0, 0, 256, 256); return new THREE.CanvasTexture(cv); })(), blending: THREE.AdditiveBlending, depthWrite: false }));
sunGlow.position.copy(SUN.clone().multiplyScalar(8000)); sunGlow.scale.set(700, 700, 1); scene.add(sunGlow);

// ---------------------------------------------------------------- planets (cinematic scale: Mars radius 100 at the origin)
const atmo = (color, power, k) => new THREE.ShaderMaterial({ transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.BackSide, uniforms: { c: { value: new THREE.Color(color) }, sun: { value: SUN } },
  vertexShader: "varying vec3 n; varying vec3 v; void main(){ n = normalize(mat3(modelMatrix)*normal); vec4 w = modelMatrix*vec4(position,1.); v = normalize(cameraPosition - w.xyz); gl_Position = projectionMatrix*viewMatrix*w; }",
  fragmentShader: `uniform vec3 c; uniform vec3 sun; varying vec3 n; varying vec3 v; void main(){ float f = pow(1. - abs(dot(n, v)), ${power.toFixed(1)}); float lit = smoothstep(-.35, .45, dot(-n, sun) * -1.); gl_FragColor = vec4(c * f * ${k.toFixed(2)} * (0.25 + lit), f); }` });
const [mCol, mBump] = planetMaps(2048, 1024, marsShade);
const mars = new THREE.Mesh(new THREE.SphereGeometry(100, 192, 128), new THREE.MeshStandardMaterial({ map: mCol, bumpMap: mBump, bumpScale: 2.2, roughness: 0.96, metalness: 0 })); scene.add(mars);
const marsAtmo = new THREE.Mesh(new THREE.SphereGeometry(103.5, 96, 64), atmo(0xff9a6a, 3.0, 1.6)); scene.add(marsAtmo);
const EARTH = V(-560, 40, -900), [eCol, eBump] = planetMaps(1024, 512, earthShade), [cCol] = planetMaps(1024, 512, cloudShade);
const earth = new THREE.Mesh(new THREE.SphereGeometry(28, 96, 64), new THREE.MeshStandardMaterial({ map: eCol, bumpMap: eBump, bumpScale: 0.6, roughness: 0.75 })); earth.position.copy(EARTH); scene.add(earth);
cCol.colorSpace = THREE.NoColorSpace; const clouds = new THREE.Mesh(new THREE.SphereGeometry(28.4, 96, 64), new THREE.MeshStandardMaterial({ color: 0xffffff, alphaMap: cCol, transparent: true, opacity: 0.7, depthWrite: false })); clouds.position.copy(EARTH); scene.add(clouds);
const earthAtmo = new THREE.Mesh(new THREE.SphereGeometry(30, 64, 48), atmo(0x5aa8ff, 2.6, 2.0)); earthAtmo.position.copy(EARTH); scene.add(earthAtmo);

// ---------------------------------------------------------------- Mangalyaan (units: metres; engine on the -X face, dish on +Y, solar wing along +Z)
const craft = new THREE.Group(); scene.add(craft);
const foil = new THREE.MeshStandardMaterial({ color: 0xd9a441, metalness: 1, roughness: 0.42, normalMap: foilMap(), normalScale: new THREE.Vector2(0.35, 0.35), envMap: envTex, envMapIntensity: 0.6 });
craft.add(new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.4, 1.55), foil));
const white = new THREE.MeshStandardMaterial({ color: 0xeeeeea, roughness: 0.5, metalness: 0.1, envMap: envTex, envMapIntensity: 0.4 }), grey = new THREE.MeshStandardMaterial({ color: 0x8a8f99, roughness: 0.4, metalness: 0.8, envMap: envTex });
{ const pts = []; for (let i = 0; i <= 24; i++) { const r = 1.1 * i / 24; pts.push(new THREE.Vector2(r, r * r * 0.32)); } const dish = new THREE.Mesh(new THREE.LatheGeometry(pts, 64), white); dish.material.side = THREE.DoubleSide; dish.position.set(0.1, 1.05, 0); dish.rotation.z = -0.35; craft.add(dish);
  const strut = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.5), grey); strut.position.set(0.05, 0.85, 0); craft.add(strut); const feed = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.1, 0.4), grey); feed.position.set(0.25, 1.55, 0); feed.rotation.z = -0.35; craft.add(feed); }
{ const boom = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.9), grey); boom.rotation.x = Math.PI / 2; boom.position.set(0, 0, 1.2); craft.add(boom);
  const cells = new THREE.MeshStandardMaterial({ map: cellMap(), metalness: 0.55, roughness: 0.28, envMap: envTex, envMapIntensity: 1.1 });
  for (let i = 0; i < 3; i++) { const p = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.03, 1.8), [grey, grey, cells, grey, grey, grey]); p.position.set(0, 0, 2.6 + i * 1.86); craft.add(p); } }
const nozzle = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.26, 0.5, 32, 1, true), grey); nozzle.material.side = THREE.DoubleSide; nozzle.rotation.z = Math.PI / 2; nozzle.position.set(-1.0, 0, 0); craft.add(nozzle);
const plumeMat = new THREE.ShaderMaterial({ transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, uniforms: { k: { value: 0 }, t: { value: 0 } },
  vertexShader: "varying vec2 u; void main(){ u = uv; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }",
  fragmentShader: "uniform float k; uniform float t; varying vec2 u; void main(){ float a = (1.-u.y); float fl = .85 + .15*sin(t*60. + u.y*30.); vec3 col = mix(vec3(1.,.45,.12), vec3(1.,.95,.75), pow(a, 3.)); gl_FragColor = vec4(col * k * fl * 1.15, a * a * k * .85); }" });
const plume = new THREE.Mesh(new THREE.ConeGeometry(0.42, 4.2, 32, 1, true), plumeMat); plume.rotation.z = Math.PI / 2; plume.position.set(-3.35, 0, 0); craft.add(plume);
const SPARK = 260, spG = new THREE.BufferGeometry(); spG.setAttribute("position", new THREE.BufferAttribute(new Float32Array(SPARK * 3), 3));
const sparks = new THREE.Points(spG, new THREE.PointsMaterial({ color: 0xffb070, size: 0.09, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false })); craft.add(sparks);
const SPR = (() => { const r = rng(17); return Array.from({ length: SPARK }, () => [r(), r() * 2 - 1, r() * 2 - 1, 0.6 + r() * 0.8]); })();
const rcs = [V(0.78, 0.6, -0.7), V(0.78, -0.6, 0.7)].map(p => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: sunGlow.material.map, color: 0xcfe6ff, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true })); s.position.copy(p); s.scale.set(0.8, 0.8, 1); craft.add(s); return s; });

// ---------------------------------------------------------------- paths and props
const ORB = { a: 230, b: 150, tilt: 0.22 }, orbitPt = th => V(Math.cos(th) * ORB.a + 40, Math.sin(th) * ORB.b * Math.sin(ORB.tilt), Math.sin(th) * ORB.b * Math.cos(ORB.tilt));
const lineOf = (pts, color, dash, gap, op = 1) => { const gm = new THREE.BufferGeometry().setFromPoints(pts), m = new THREE.LineDashedMaterial({ color, dashSize: dash, gapSize: gap, transparent: true, opacity: op, depthWrite: false }); const l = new THREE.Line(gm, m); l.computeLineDistances(); scene.add(l); return l; };
const orbit = lineOf(Array.from({ length: 361 }, (_, i) => orbitPt(i / 360 * 6.2832)), 0xffd36b, 5, 4);
const INB = Array.from({ length: 200 }, (_, i) => { const u = i / 199; return V(lerp(-700, orbitPt(Math.PI * 0.92).x, u), lerp(140, orbitPt(Math.PI * 0.92).y, u) + Math.sin(u * Math.PI) * 30, lerp(520, orbitPt(Math.PI * 0.92).z, u)); });
const inbound = lineOf(INB, 0xffffff, 4, 6, 0.45);
const ghost = lineOf(Array.from({ length: 200 }, (_, i) => { const th = Math.PI * 0.92 + i / 199 * 1.4, r = 1 + i / 199 * 1.8; const p = orbitPt(th); return V(p.x * r, p.y * r + i * 0.4, p.z * r + i * 1.2); }), 0xff6a55, 6, 6);
const rings = Array.from({ length: 5 }, () => { const m = new THREE.Mesh(new THREE.TorusGeometry(26, 1.1, 8, 64), new THREE.MeshBasicMaterial({ color: 0x8fdcff, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false })); scene.add(m); return m; });
const BARS = new THREE.Group(); scene.add(BARS);
const barMat = (col, em) => new THREE.MeshStandardMaterial({ color: col, emissive: em, emissiveIntensity: 0.06, metalness: 0.3, roughness: 0.35, envMap: envTex });
const barG = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), barMat(0x5a4ad0, 0x2a1d70)), barM = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), barMat(0xc98f2c, 0x5a3a08)); BARS.add(barG, barM);
const reel = new THREE.Group(); { const disc = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 0.22, 48), new THREE.MeshStandardMaterial({ color: 0x2a2d36, metalness: 0.7, roughness: 0.3, envMap: envTex })); disc.rotation.x = Math.PI / 2; reel.add(disc);
  for (let i = 0; i < 6; i++) { const h = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.26, 24), new THREE.MeshBasicMaterial({ color: 0x0b0c12 })); h.rotation.x = Math.PI / 2; h.position.set(Math.cos(i * 1.047) * 0.52, Math.sin(i * 1.047) * 0.52, 0); reel.add(h); } }
BARS.add(reel); const mini = craft.clone(true); mini.children = mini.children.filter(o => o !== plume && o !== sparks && !rcs.includes(o)); mini.scale.setScalar(0.32); BARS.add(mini); BARS.position.set(0, 0, 0);
const BAR_ORIGIN = V(2600, 0, 0);

// ---------------------------------------------------------------- helpers: project to screen for DOM labels
const toScreen = v => { const p = v.clone().project(camera); return [(p.x + 1) / 2 * W, (1 - p.y) / 2 * H, p.z]; };
const show = (id, k, dy = 30, extra = "") => { const e = $(id); e.style.opacity = clamp(k); e.style.transform = `translateY(${((1 - clamp(k)) * dy).toFixed(1)}px) ${extra}`; };
$("#src").textContent = "Sources: ISRO · The Planetary Society · NASA";
const look = (pos, tgt, fov = 35, roll = 0) => { camera.position.copy(pos); camera.up.set(Math.sin(roll), Math.cos(roll), 0); camera.lookAt(tgt); camera.fov = fov; camera.updateProjectionMatrix(); camera.updateMatrixWorld(); };

window.renderAt = function (tg) {
  const t = clamp(tg, 0, TM.total - 0.001), burnK = seg(t, B0, B0 + 0.5) * (1 - seg(t, B1 - 0.3, B1)), orbitK = E.io(seg(t, WIN - 0.1, WIN + 2.4));
  mars.rotation.y = 0.6 + t * 0.008; earth.rotation.y = t * 0.05; clouds.rotation.y = t * 0.065;
  [orbit, inbound, ghost, ...rings, BARS].forEach(o => o.visible = false); craft.visible = true; mars.visible = marsAtmo.visible = true;
  // craft position along its path: inbound cruise, then the arc around Mars after capture
  const capture = Math.PI * 0.92, inU = seg(t, 0, c[4] + 1.0), onIn = INB[Math.min(199, Math.floor(E.out(inU) * 199))];
  const th = t < WIN ? capture : capture + (t - WIN) * 0.16, cpos = t < c[4] + 1.0 ? onIn.clone() : orbitPt(th);
  if (t >= c[4] + 1.0 && t < WIN) cpos.copy(orbitPt(capture));
  craft.position.copy(cpos); const vel = t < WIN ? INB[199].clone().sub(INB[150]).normalize() : orbitPt(th + 0.01).sub(orbitPt(th)).normalize();
  const turn = E.io(seg(t, c[2] + 0.6, B0 - 0.1)), fwd = vel.clone().multiplyScalar(turn > 0.5 ? -1 : 1), q = new THREE.Quaternion().setFromUnitVectors(V(1, 0, 0), vel);
  craft.quaternion.copy(q); craft.rotateY(turn * Math.PI); craft.rotateX(0.25 + Math.sin(t * 0.3) * 0.04); if (t >= WIN) craft.rotateY(Math.PI);
  plumeMat.uniforms.k.value = burnK; plumeMat.uniforms.t.value = t; plume.scale.set(1, 0.8 + 0.2 * Math.sin(t * 50), 1); plume.visible = burnK > 0.01;
  { const P = spG.attributes.position.array; for (let i = 0; i < SPARK; i++) { const [ph, a, b, sp] = SPR[i], age = ((t * sp * 1.6 + ph) % 1); P[i * 3] = -1.2 - age * 6 * burnK; P[i * 3 + 1] = a * age * 0.9; P[i * 3 + 2] = b * age * 0.9; } spG.attributes.position.needsUpdate = true; sparks.material.opacity = burnK * 0.9; sparks.visible = burnK > 0.01; }
  const puff = Math.max(Math.exp(-(((t - (c[2] + 0.65)) / 0.12) ** 2)), Math.exp(-(((t - (B0 - 0.15)) / 0.12) ** 2))); rcs.forEach(s => { s.material.opacity = puff; s.visible = puff > 0.02; });
  let fov = 35;
  if (t < c[1]) {   // establishing: deep space, Mars a bright disc far ahead, the spacecraft sweeps past the lens
    const k = seg(t, 0, c[1]); look(cpos.clone().add(V(lerp(-9, 5, k), lerp(2, 0.8, k), lerp(16, 13, k))), cpos.clone().add(V(lerp(30, 4, E.io(k)), 0, -20 * (1 - k))), 32);
  } else if (t < c[2]) {   // chase: behind and beside the craft, Mars swelling ahead
    const k = E.io(seg(t, c[1], c[2])), back = vel.clone().multiplyScalar(-lerp(15, 11, k)), side = V(0, 1, 0).cross(vel).normalize().multiplyScalar(lerp(6, 9, k));
    look(cpos.clone().add(back).add(side).add(V(0, lerp(1.6, 0.6, k), 0)), cpos.clone().add(vel.clone().multiplyScalar(9)), lerp(36, 32, k), lerp(0.04, -0.03, k));
  } else if (t < c[3]) {   // the turn and ignition, close and low against the planet
    const k = E.io(seg(t, c[2], c[3])), side = V(0, 1, 0).cross(vel).normalize();
    look(cpos.clone().add(side.clone().multiplyScalar(lerp(14, 11, k))).add(vel.clone().multiplyScalar(lerp(-3, 4, k))).add(V(0, lerp(-2.4, -1, k), 0)), cpos.clone().add(V(0, 0.3, 0)).add(vel.clone().multiplyScalar(-2)), 32, 0.05);
  } else if (t < c[4]) {   // wide: Earth, Mars and the radio signal crawling between them
    const k = E.io(seg(t, c[3], c[4])); look(V(lerp(-150, -120, k), lerp(210, 190, k), lerp(640, 600, k)), V(-290, 15, -430), 42);
    rings.forEach((m, i) => { const u = ((t - c[3]) * 0.045 + i * 0.05) % 1; m.visible = true; m.position.lerpVectors(EARTH, V(0, 0, 0), 0.07 + u * 0.5); m.lookAt(V(0, 0, 0)); m.scale.setScalar(1 + u * 1.5); m.material.opacity = Math.max(0, 0.9 - u * 1.6); });
    craft.scale.setScalar(7);
  } else if (t < WIN) {   // the burn continues; the path that misses is shown in red; hush before the result
    const k = E.io(seg(t, c[4], WIN)); ghost.visible = true; ghost.material.opacity = fin(t, c[4] + 0.4, 1) * (1 - fin(t, WIN - 0.5, 0.4)); ghost.geometry.setDrawRange(0, Math.floor(fin(t, c[4] + 0.4, 1.8) * 200));
    look(cpos.clone().add(V(lerp(-14, -18, k), lerp(-3, -4, k), lerp(16, 22, k))), cpos.clone().add(V(20, -8, -30)), 36, -0.08);
  } else if (t < c[7]) {   // capture: the orbit closes around Mars, the camera pulls back, then rides along
    const k = E.io(seg(t, WIN, WIN + 3)); orbit.visible = true; orbit.material.opacity = 0.35 + 0.65 * orbitK; orbit.geometry.setDrawRange(0, Math.floor(lerp(40, 361, orbitK)));
    const wide = V(lerp(cpos.x - 30, 160, k), lerp(cpos.y + 10, 260, k), lerp(cpos.z + 60, 560, k)), ride = cpos.clone().add(V(-10, 6, 18));
    look(t < c[6] ? wide : wide.lerp(ride, E.io(seg(t, c[6] + 3, c[7]))), t < c[6] ? V(lerp(cpos.x, 0, k), 0, lerp(cpos.z, 0, k)) : V(0, 0, 0).lerp(cpos, E.io(seg(t, c[6] + 3, c[7]))), 36);
  } else if (t < c[8]) {   // close on the spacecraft for the price
    orbit.visible = true; orbit.material.opacity = 0.7; const k = E.io(seg(t, c[7], c[8])); look(cpos.clone().add(V(lerp(-10, -7, k), lerp(5, 3, k), lerp(16, 11, k))), cpos.clone().add(V(0, 0.4, 0)), 32);
    const [sx, sy] = toScreen(cpos.clone().add(V(0, 2.6, 0))), e = $("#price"), pk = pop(t, c[7] + 1.2, 0.5); e.style.left = sx - 170 + "px"; e.style.top = sy - 110 + "px"; e.style.opacity = clamp(pk * 3); e.style.transform = `scale(${pk.toFixed(3)}) rotate(-4deg)`;
    const e2 = $("#price2"); e2.style.left = sx - 110 + "px"; e2.style.top = sy - 28 + "px"; e2.style.opacity = fin(t, c[7] + 1.6);
  } else if (t < c[9] - 0.15) {   // the comparison: two lit pillars in space
    BARS.visible = true; mars.visible = marsAtmo.visible = false; craft.visible = false; BARS.position.copy(BAR_ORIGIN);
    const kg = E.out(seg(t, c[8] + 0.1, c[8] + 1.2)), km = E.out(seg(t, c[8] + 0.6, c[8] + 1.7)), Hm = 9;
    barG.scale.set(2.6, Math.max(0.01, Hm * kg), 2.6); barG.position.set(-2.4, Hm * kg / 2, 0); barM.scale.set(2.6, Math.max(0.01, Hm * 0.74 * km), 2.6); barM.position.set(2.4, Hm * 0.74 * km / 2, 0);
    reel.position.set(-2.4, Hm * kg + 1.4, 0); reel.rotation.z = t * 1.5; mini.position.set(2.4, Hm * 0.74 * km + 1.3, 0); mini.rotation.y = t * 0.8;
    const k = seg(t, c[8], c[9]); look(BAR_ORIGIN.clone().add(V(lerp(-6, 4, k), lerp(5, 7, k), lerp(26, 23, k))), BAR_ORIGIN.clone().add(V(0, 4.8, 0)), 38);
    const lab = (id, v, val, x) => { const [sx, sy] = toScreen(BAR_ORIGIN.clone().add(V(x, -1.4, 0))); const e = $(id); e.style.left = sx - 200 + "px"; e.style.top = sy + "px"; e.style.opacity = fin(t, c[8] + 0.6); e.innerHTML = v; };
    lab("#barG", `<b>$${Math.round(100 * kg)}M</b><br>GRAVITY<br><small>Hollywood film, 2013</small>`, 0, -2.4); lab("#barM", `<b>$${Math.round(74 * km)}M</b><br>MARS ORBITER MISSION<br><small>ISRO, 2013–14</small>`, 0, 2.4);
  } else {   // title: rising over the Martian horizon with the Sun breaking past the limb
    craft.visible = false; const k = E.io(seg(t, c[9] - 0.15, TM.total)), cam = V(-20, 108, 52).normalize().multiplyScalar(lerp(118, 124, k)), cd = cam.clone().negate().normalize(), T = SUN.clone().sub(cd.clone().multiplyScalar(SUN.dot(cd))).normalize(), a = lerp(0.36, 0.3, k), dir = T.clone().multiplyScalar(Math.cos(a)).add(cd.clone().multiplyScalar(Math.sin(a))); look(cam, cam.clone().add(dir.multiplyScalar(100)), 46);
  }
  if (t < c[3] || t >= c[4]) craft.scale.setScalar(1);
  if (!(t >= c[7] && t < c[8])) { $("#price").style.opacity = 0; $("#price2").style.opacity = 0; }
  if (!(t >= c[8] && t < c[9] - 0.15)) { $("#barG").style.opacity = 0; $("#barM").style.opacity = 0; }
  const shake = burnK * 0.04; camera.position.add(V(Math.sin(t * 61) * shake, Math.cos(t * 53) * shake, 0));
  bloom.strength = 0.65 + 0.5 * burnK + 0.6 * (t > WIN && t < WIN + 1 ? 1 - seg(t, WIN, WIN + 1) : 0);
  composer.render();
  // DOM text cues (same timing as the 2D cut)
  show("#date", fin(t, 0.6, 0.8) * (1 - fin(t, c[1] - 0.2, 0.4)));
  show("#dist", fin(t, c[1] + 0.3) * (1 - fin(t, c[2] - 0.2, 0.3))); show("#dist2", fin(t, c[1] + 0.8) * (1 - fin(t, c[2] - 0.2, 0.3)));
  { const k = fin(t, c[1] + 4.0) * (1 - fin(t, c[2] - 0.2, 0.3)), [sx, sy] = toScreen(cpos.clone().add(V(0, -1.8, 0))); $("#scale").style.left = sx - 160 + "px"; $("#scale").style.top = sy + 30 + "px"; show("#scale", k); }
  show("#burn", fin(t, c[2] + 1.5) * (1 - fin(t, c[3] - 0.2, 0.3)));
  show("#clock", fin(t, c[3] + 2.2) * (1 - fin(t, c[4] - 0.2, 0.3))); show("#clock2", fin(t, c[3] + 2.6) * (1 - fin(t, c[4] - 0.2, 0.3)));
  show("#miss", fin(t, c[4] + 0.5) * (1 - fin(t, WIN - 0.6, 0.4)));
  { const k = pop(t, WIN + 0.05, 0.45); $("#works").style.opacity = clamp(k * 2) * (1 - fin(t, c[6] - 0.2, 0.3)); $("#works").style.transform = `scale(${(0.6 + 0.4 * k).toFixed(3)})`; }
  show("#first1", fin(t, c[6] + 1.0) * (1 - fin(t, c[7] - 0.3, 0.3))); show("#first2", fin(t, c[6] + 4.0) * (1 - fin(t, c[7] - 0.3, 0.3)));
  show("#title", fin(t, c[9] - 0.1, 0.5), 40);
  $("#flash").style.opacity = (t > WIN && t < WIN + 0.5 ? 0.3 * (1 - seg(t, WIN, WIN + 0.5)) : 0) + (t > c[9] && t < c[9] + 0.3 ? 0.2 * (1 - seg(t, c[9], c[9] + 0.3)) : 0);
  $("#src").style.opacity = fin(t, 1.0) * (t < c[9] ? 1 : 0);
};
window.DUR = TM.total;
await document.fonts.ready; renderAt(parseFloat(Q.get("t")) || 0); window.READY = true;
if (Q.has("play")) { const s0 = performance.now(); const loop = () => { renderAt(((performance.now() - s0) / 1000) % TM.total); requestAnimationFrame(loop); }; loop(); }
