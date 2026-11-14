import * as THREE from "three";
export const COL = { navy: 0x0f2557, gold: 0xc9992e, cream: 0xfbf5e9, white: 0xf4f5f7, grey: 0xb9c0c9, dark: 0x1b1f27, glass: 0x10151d, accent: 0xff5a1f };
const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, metalness: 0.25, roughness: 0.5, side: THREE.DoubleSide, ...o });

// ---- airfoil outline (unit chord, LE at 0, TE at 1), n points per surface
export function airfoil(t = 0.12, m = 0.02, n = 18) {
  const up = [], lo = [];
  for (let i = 0; i <= n; i++) { const x = 0.5 * (1 - Math.cos(Math.PI * i / n));
    const yt = 5 * t * (0.2969 * Math.sqrt(x) - 0.126 * x - 0.3516 * x * x + 0.2843 * x ** 3 - 0.1036 * x ** 4), yc = 4 * m * x * (1 - x);
    up.push([x, yc + yt]); lo.push([x, yc - yt]); }
  return up.concat(lo.reverse().slice(1, -1));   // closed loop: LE → TE over top, back under
}
// ---- loft airfoil sections: {le:[x,y,z], chord, t, up:[x,y,z], m}; chord runs toward -x
export function loft(secs) {
  const pos = [], idx = []; let N = 0;
  secs.forEach(s => { const pts = airfoil(s.t ?? 0.12, s.m ?? 0.02); N = pts.length; const u = s.up ?? [0, 1, 0];
    pts.forEach(([x, y]) => pos.push(s.le[0] - x * s.chord + u[0] * y * s.chord, s.le[1] + u[1] * y * s.chord, s.le[2] + u[2] * y * s.chord)); });
  for (let k = 0; k < secs.length - 1; k++) for (let i = 0; i < N; i++) { const a = k * N + i, b = k * N + (i + 1) % N, c = a + N, d = b + N; idx.push(a, c, b, b, c, d); }
  [0, secs.length - 1].forEach(k => { for (let i = 1; i < N - 1; i++) idx.push(k * N, k * N + i, k * N + i + 1); });
  const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals(); return g;
}
// ---- body of revolution about the x axis from a radius function
function revolve(rf, x0, x1, n = 40, seg = 40, phiStart = 0, phiLen = Math.PI * 2, droop = null) {
  const pts = []; for (let i = 0; i <= n; i++) { const x = x0 + (x1 - x0) * i / n; pts.push(new THREE.Vector2(Math.max(0.0001, rf(x)), x)); }
  const g = new THREE.LatheGeometry(pts, seg, phiStart, phiLen); g.rotateZ(-Math.PI / 2);   // lathe axis y → x
  if (droop) { const p = g.attributes.position; for (let i = 0; i < p.count; i++) p.setY(i, p.getY(i) + droop(p.getX(i))); g.computeVertexNormals(); }
  return g;
}
const FR = 1.98;
export const fuseR = x => x > 13.2 ? FR * Math.sqrt(Math.max(0, 1 - ((x - 13.2) / 5.6) ** 2.1)) : x > -5 ? FR : FR * (1 - 0.86 * ((-5 - x) / 13.8) ** 1.5);
const droop = x => x < -5 ? ((-5 - x) / 13.8) ** 1.6 * 1.25 : x > 13.2 ? -(((x - 13.2) / 5.6) ** 2) * 0.45 : 0;

// ---- hinged plate: hinge from p0 to p1, plate extends "aft" by chord
function surface(p0, p1, chord, thick, mat, aft = new THREE.Vector3(-1, 0, 0)) {
  const a = new THREE.Vector3(...p0), b = new THREE.Vector3(...p1), z = b.clone().sub(a), len = z.length(); z.normalize();
  const x = aft.clone().sub(z.clone().multiplyScalar(aft.dot(z))).normalize(), y = new THREE.Vector3().crossVectors(z, x);
  const g = new THREE.Group(); g.position.copy(a).add(b).multiplyScalar(0.5); g.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, y, z));
  const piv = new THREE.Group(); g.add(piv); const m = new THREE.Mesh(new THREE.BoxGeometry(chord, thick, len), mat); m.position.x = chord / 2; piv.add(m);
  g.userData.piv = piv; return g;
}
// wing planform helpers (right wing, +z)
const WS = [{ z: 1.6, le: 3.6, c: 7.0 }, { z: 6.0, le: 0.7, c: 4.2 }, { z: 17.0, le: -4.5, c: 1.6 }];
const wy = z => -0.95 + (z - 1.6) / 15.4 * 1.35;
function wat(z) { const k = z < 6 ? 0 : 1, a = WS[k], b = WS[k + 1], u = (z - a.z) / (b.z - a.z); return { le: a.le + (b.le - a.le) * u, c: a.c + (b.c - a.c) * u, y: wy(z) }; }
const wpt = (z, f, dy = 0) => { const w = wat(z); return [w.le - w.c * f, w.y + dy, z]; };

export function buildAircraft() {
  const A = new THREE.Group(), P = {};   // P: named parts
  const grp = (name, ex) => { const g = new THREE.Group(); g.name = name; g.userData.ex = new THREE.Vector3(...ex); A.add(g); P[name] = g; return g; };
  const M = { skin: () => std(COL.white, { metalness: 0.15, roughness: 0.42 }), wing: () => std(0xd5dae1, { metalness: 0.35, roughness: 0.4 }), mov: () => std(0x9aa3ae, { metalness: 0.3 }),
    navy: () => std(COL.navy, { roughness: 0.38 }), gold: () => std(COL.gold, { metalness: 0.6, roughness: 0.35 }), dark: () => std(COL.dark, { roughness: 0.7 }), glass: () => std(COL.glass, { metalness: 0.8, roughness: 0.15 }) };

  // 1 nose & cockpit
  const nose = grp("nose", [7, 0, 0]);
  nose.add(new THREE.Mesh(revolve(fuseR, 13.2, 18.8, 30, 48, 0, Math.PI * 2, droop), M.skin()));
  const radome = new THREE.Mesh(revolve(x => fuseR(x) * 1.004, 17.3, 18.8, 12, 48, 0, Math.PI * 2, droop), std(0xdfe3e8, { roughness: 0.6 })); nose.add(radome);
  const glass = new THREE.Mesh(revolve(x => fuseR(x) * 1.012, 15.5, 16.75, 8, 24, Math.PI / 2 - 1.15, 2.3, droop), M.glass()); nose.add(glass);
  [-1, 0, 1].forEach(k => { if (!k) return; const post = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.09, 0.09), M.skin()); post.position.set(16.1, 1.36, k * 0.42); post.rotation.z = -0.5; nose.add(post); });
  // 2 fuselage
  const fuse = grp("fuselage", [0, 0, 0]);
  fuse.add(new THREE.Mesh(revolve(fuseR, -18.8, 13.2, 60, 48, 0, Math.PI * 2, droop), M.skin()));
  const stripe = new THREE.Mesh(revolve(x => fuseR(x) * 1.003, -17.5, 13.2, 50, 12, Math.PI / 2 + 1.75, 0.16, droop), M.gold()); fuse.add(stripe);
  const stripe2 = stripe.clone(); stripe2.scale.z = -1; fuse.add(stripe2);
  const wn = []; for (let x = 12; x > -11; x -= 0.56) if (Math.abs(x - 6.2) > 0.5 && Math.abs(x + 3) > 0.5) wn.push(x);
  const win = new THREE.InstancedMesh(new THREE.BoxGeometry(0.26, 0.36, 0.06), M.glass(), wn.length * 2), mt = new THREE.Matrix4();
  wn.forEach((x, i) => { mt.makeRotationX(-0.2).setPosition(x, 0.42, 1.93); win.setMatrixAt(i * 2, mt); mt.makeRotationX(0.2).setPosition(x, 0.42, -1.93); win.setMatrixAt(i * 2 + 1, mt); }); fuse.add(win);
  [[12.6, 1.9], [-9.6, 1.9]].forEach(([x, h]) => [-1, 1].forEach(s => { const d = new THREE.Mesh(new THREE.BoxGeometry(0.85, h, 0.05), std(0xe3e6ea)); d.position.set(x, 0.1, s * 1.96); d.rotation.x = -s * 0.1; fuse.add(d); }));
  const belly = new THREE.Mesh(new THREE.SphereGeometry(1, 32, 16), M.skin()); belly.scale.set(5.6, 1.05, 2.5); belly.position.set(0.6, -1.5, 0); fuse.add(belly);
  // 3 wings (+ winglets)
  const wings = grp("wings", [0, 0, 0]); P.wingR = new THREE.Group(); P.wingL = new THREE.Group(); P.wingR.userData.ex = new THREE.Vector3(0, 0, 9); P.wingL.userData.ex = new THREE.Vector3(0, 0, -9); wings.add(P.wingR, P.wingL);
  const wingGeo = loft(WS.map((s, i) => ({ le: [s.le, wy(s.z), s.z], chord: s.c, t: [0.14, 0.12, 0.10][i], m: 0.025 })));
  const wl = loft([{ le: [-4.5, wy(17), 17], chord: 1.6, t: 0.1, up: [0, 0, 1], m: 0 }, { le: [-5.0, wy(17) + 0.9, 17.35], chord: 1.25, t: 0.09, up: [0, 0, 1], m: 0 }, { le: [-6.0, wy(17) + 2.5, 17.6], chord: 0.7, t: 0.09, up: [0, 0, 1], m: 0 }]);
  const wm = M.wing(), gm = M.gold();
  P.wingR.add(new THREE.Mesh(wingGeo, wm), new THREE.Mesh(wl, gm));
  const wgl = new THREE.Mesh(wingGeo, wm), wll = new THREE.Mesh(wl, gm); wgl.scale.z = wll.scale.z = -1; P.wingL.add(wgl, wll);
  // 4 moving surfaces (children of each wing so they explode with it, plus their own offset)
  const mov = { flaps: [], slats: [], ail: [], spoil: [] }; P.mov = mov; P.movMats = [];
  [1, -1].forEach(s => { const host = new THREE.Group(); host.scale.z = s; host.userData.ex = new THREE.Vector3(-4, 1.2, 0); host.name = "movables"; (s > 0 ? P.wingR : P.wingL).add(host); (P.movHosts ||= []).push(host);
    const mk = () => { const m = M.mov(); P.movMats.push(m); return m; };
    [[2.1, 5.8], [6.3, 12.0]].forEach(([a, b]) => { const f = surface(wpt(a, 0.8, -0.02), wpt(b, 0.8, -0.02), wat((a + b) / 2).c * 0.24, 0.16, mk()); host.add(f); mov.flaps.push(f); });
    const al = surface(wpt(12.4, 0.78), wpt(16.6, 0.78), 0.62, 0.12, mk()); host.add(al); al.userData.side = s; mov.ail.push(al);
    [[2.4, 5.8], [6.3, 16.4]].forEach(([a, b]) => { const sl = surface(wpt(a, 0.0, 0.03), wpt(b, 0.0, 0.03), 0.55, 0.2, mk(), new THREE.Vector3(1, 0, 0)); sl.userData.piv.children[0].position.x = -0.1; host.add(sl); mov.slats.push(sl); });
    const sp = surface(wpt(6.6, 0.62, 0.28), wpt(12.0, 0.62, 0.16), 0.75, 0.07, mk()); host.add(sp); mov.spoil.push(sp); });
  // 5 engines
  const engines = grp("engines", [3, -5.5, 0]); P.fans = [];
  [1, -1].forEach(s => { const e = new THREE.Group(); e.position.set(5.2, -2.25, s * 5.75); engines.add(e);
    const nr = x => 1.02 + 0.2 * Math.sin(Math.PI * Math.min(1, (2.3 - x) / 4.2) ** 0.7) ;
    e.add(new THREE.Mesh(revolve(nr, -1.9, 2.3, 24, 40), M.navy()));
    const lip = new THREE.Mesh(new THREE.TorusGeometry(1.03, 0.07, 10, 40), std(0xd9dde2, { metalness: 0.9, roughness: 0.2 })); lip.rotation.y = Math.PI / 2; lip.position.x = 2.3; e.add(lip);
    const inner = new THREE.Mesh(new THREE.CylinderGeometry(0.98, 0.98, 1.2, 32, 1, true), M.dark()); inner.rotation.z = Math.PI / 2; inner.position.x = 1.7; e.add(inner);
    const fan = new THREE.Group(); fan.position.x = 1.45; e.add(fan); P.fans.push(fan);
    for (let i = 0; i < 18; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.9, 0.2), std(0x30353e, { metalness: 0.7, roughness: 0.3 })); const a = i / 18 * Math.PI * 2; b.position.set(0, Math.cos(a) * 0.5, Math.sin(a) * 0.5); b.rotation.x = a; b.rotation.y = 0.5; fan.add(b); }
    const spin = new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.6, 20), std(0xdfe3e8)); spin.rotation.z = -Math.PI / 2; spin.position.x = 0.3; fan.add(spin);
    const noz = new THREE.Mesh(revolve(x => 0.62 - 0.45 * ((-1.6 - x) / 1.5), -3.1, -1.6, 8, 28), std(0x8d939c, { metalness: 0.8, roughness: 0.3 })); e.add(noz);
    const py = new THREE.Mesh(new THREE.BoxGeometry(3.6, 1.3, 0.28), M.skin()); py.position.set(-0.7, 1.35, 0); py.rotation.z = -0.12; e.add(py); });
  // 6 tail
  const tail = grp("tail", [-7, 2, 0]);
  const fy = x => droop(x);
  tail.add(new THREE.Mesh(loft([{ le: [-10.6, 1.75, 0], chord: 6.4, t: 0.1, up: [0, 0, 1], m: 0 }, { le: [-16.0, 8.4, 0], chord: 2.3, t: 0.09, up: [0, 0, 1], m: 0 }]), M.navy()));
  const finBand = new THREE.Mesh(loft([{ le: [-12.2, 3.7, 0], chord: 5.75, t: 0.104, up: [0, 0, 1], m: 0 }, { le: [-12.7, 4.3, 0], chord: 5.4, t: 0.104, up: [0, 0, 1], m: 0 }]), M.gold()); tail.add(finBand);
  const sg = loft([{ le: [-13.2, 1.0, 0.7], chord: 3.9, t: 0.1, m: 0 }, { le: [-16.6, 1.5, 6.3], chord: 1.5, t: 0.09, m: 0 }]);
  const sR = new THREE.Mesh(sg, M.wing()), sL = new THREE.Mesh(sg, M.wing()); sL.scale.z = -1; tail.add(sR, sL);
  P.elev = []; P.tailMats = [];
  [1, -1].forEach(s => { const h = new THREE.Group(); h.scale.z = s; tail.add(h); const m = M.mov(); P.tailMats.push(m); const el = surface([-16.25, 1.03, 0.9], [-17.75, 1.5, 6.2], 0.95, 0.1, m); h.add(el); P.elev.push(el); });
  const rm = M.gold(); P.rudMat = rm; P.rudder = surface([-15.75, 2.3, 0], [-17.75, 8.3, 0], 1.25, 0.14, rm); tail.add(P.rudder);
  // 7 landing gear
  const gear = grp("gear", [0, -7, 0]);
  const strut = (x, z, len, wr, pair) => { const g = new THREE.Group(); g.position.set(x, -1.7, z); const st = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.16, len, 12), std(0xaab1ba, { metalness: 0.8, roughness: 0.3 })); st.position.y = -len / 2; g.add(st);
    [-1, 1].forEach(k => { const w = new THREE.Mesh(new THREE.CylinderGeometry(wr, wr, 0.34, 24), std(0x16181c, { roughness: 0.9 })); w.rotation.x = Math.PI / 2; w.position.set(0, -len, k * pair); g.add(w);
      const hub = new THREE.Mesh(new THREE.CylinderGeometry(wr * 0.45, wr * 0.45, 0.36, 16), std(0xc5cad1, { metalness: 0.8 })); hub.rotation.x = Math.PI / 2; hub.position.copy(w.position); g.add(hub); }); gear.add(g); };
  strut(13.6, 0, 1.75, 0.42, 0.3); strut(-1.2, 3.6, 1.9, 0.58, 0.42); strut(-1.2, -3.6, 1.9, 0.58, 0.42);
  // 8 fuel tanks (inside wings; shown in the parts scene)
  const fuel = grp("fuel", [0, 6, 0]); const fm = new THREE.MeshStandardMaterial({ color: 0x2f7bff, transparent: true, opacity: 0.75, emissive: 0x0a2a88, roughness: 0.3 });
  const tg = loft([{ le: [2.2, wy(1.8), 1.8], chord: 3.6, t: 0.1, m: 0 }, { le: [-0.2, wy(6), 6], chord: 2.2, t: 0.09, m: 0 }, { le: [-3.3, wy(13), 13], chord: 1.2, t: 0.07, m: 0 }]);
  const tR = new THREE.Mesh(tg, fm), tL = new THREE.Mesh(tg, fm); tL.scale.z = -1; const ctr = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.7, 3.4), fm); ctr.position.set(0.4, -1.0, 0); fuel.add(tR, tL, ctr);
  // 9 systems (schematic runs)
  const sys = grp("systems", [0, 7.5, 0]); const sm = c => new THREE.MeshStandardMaterial({ color: c, emissive: c, emissiveIntensity: 0.6 });
  const run = (pts, c, r = 0.07) => sys.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(...p))), 60, r, 8), sm(c)));
  run([[16, 0, 0.4], [6, -0.6, 0.5], [0, -0.9, 0.6], [-10, -0.2, 0.4], [-17, 1.4, 0.2]], 0xc9992e); run([[0, -0.9, 0.6], [-1.5, -0.7, 6], [-4.5, 0.1, 14]], 0xc9992e); run([[0, -0.9, -0.6], [-1.5, -0.7, -6], [-4.5, 0.1, -14]], 0xc9992e);
  run([[16.5, 0.3, -0.4], [5, 0.2, -0.6], [-12, 0.4, -0.5]], 0x39c0ff); run([[5, -1.2, 0], [5.2, -2, 5.6]], 0x39c0ff); run([[5, -1.2, 0], [5.2, -2, -5.6]], 0x39c0ff);
  run([[16.8, 0.9, 0], [15.2, 0.9, 0.5], [14.4, 0.6, 0]], 0x7dff8a, 0.1);
  [[16.2, 0.5, 0], [14.4, 0.2, 0.6], [-17.3, 1.3, 0]].forEach(p => { const b = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.5, 0.6), sm(0x7dff8a)); b.position.set(...p); sys.add(b); });
  fuel.visible = sys.visible = false;
  A.userData.P = P; return A;
}
// set every explodable group's offset: k in 0..1
export function explode(A, k) { A.traverse(o => { if (o.userData.ex) { o.userData.base ??= o.position.clone(); o.position.copy(o.userData.base).addScaledVector(o.userData.ex, k); } }); }
// control deflections in radians / 0..1
export function setControls(A, c = {}) { const P = A.userData.P, m = P.mov;
  const fl = c.flaps ?? 0, sl = c.slats ?? fl, sp = c.spoilers ?? 0, ai = c.aileron ?? 0;
  m.flaps.forEach(f => { f.userData.piv.rotation.z = -0.62 * fl; f.userData.piv.position.x = 0.9 * fl; f.userData.piv.position.y = -0.25 * fl; });
  m.slats.forEach(s => { s.userData.piv.position.x = 0.5 * sl; s.userData.piv.position.y = -0.22 * sl; s.userData.piv.rotation.z = 0.35 * sl; });
  m.spoil.forEach(s => { s.userData.piv.rotation.z = 0.85 * sp; });
  m.ail.forEach(a => { a.userData.piv.rotation.z = -ai * a.userData.side; });
  P.elev.forEach(e => { e.userData.piv.rotation.z = -(c.elevator ?? 0); });
  P.rudder.userData.piv.rotation.z = c.rudder ?? 0;
  P.gear.visible = (c.gear ?? 0) > 0.02; P.gear.scale.y = Math.max(0.05, c.gear ?? 0); P.gear.position.y = (P.gear.userData.base?.y ?? 0) + (1 - (c.gear ?? 0)) * -1.2 * 0;
}
export function glow(mats, color, k) { mats.forEach(m => { m.emissive.setHex(color); m.emissiveIntensity = k; }); }
export function matsOf(obj) { const s = new Set(); obj.traverse(o => { if (o.material) s.add(o.material); }); return [...s]; }
