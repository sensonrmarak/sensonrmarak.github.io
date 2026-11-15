import { useMemo } from "react";
import * as THREE from "three";
import { AbsoluteFill, useVideoConfig } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { useThree } from "@react-three/fiber";
import { Juniper, Moss, Pebble } from "./characters";
import {
  FallingLeaves, FogPuffs, Gate, Ground, HillFair, Moon, PATH, Path, SameTrees, Stars, Trail, Village, VillageTrees,
  pathAt, pathHeading, uAtZ,
} from "./set";
import { softTex } from "./clay";
import { blink, lerp, mix3, rand, shotStart, smooth, useStepTime, wt } from "./util";

type V3 = [number, number, number];

/* ---------------------------------------------------------------- stage helpers */
const CamRig = ({ pos, look, fov }: { pos: V3; look: V3; fov: number }) => {
  const { camera } = useThree();
  const cam = camera as THREE.PerspectiveCamera;
  cam.position.set(...pos);
  if (cam.fov !== fov) { cam.fov = fov; cam.updateProjectionMatrix(); }
  cam.lookAt(...look);
  return null;
};

const Sun = ({ target, dir, color, intensity, size = 10 }: { target: V3; dir: V3; color: string; intensity: number; size?: number }) => {
  const obj = useMemo(() => new THREE.Object3D(), []);
  obj.position.set(...target);
  obj.updateMatrixWorld();
  return (
    <>
      <primitive object={obj} />
      <directionalLight target={obj} position={[target[0] + dir[0], target[1] + dir[1], target[2] + dir[2]]} color={color} intensity={intensity}
        castShadow shadow-mapSize={[2048, 2048]} shadow-bias={-0.0004} shadow-normalBias={0.02}
        shadow-camera-left={-size} shadow-camera-right={size} shadow-camera-top={size} shadow-camera-bottom={-size}
        shadow-camera-near={0.5} shadow-camera-far={80} />
    </>
  );
};

const Stage = ({ sky, fog, cam, look, fov = 40, children }:
  { sky: [string, string]; fog: [string, number, number]; cam: V3; look: V3; fov?: number; children: React.ReactNode }) => {
  const { width, height } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: `linear-gradient(${sky[0]} 0%, ${sky[1]} 52%, ${fog[0]} 70%)` }}>
      <ThreeCanvas width={width} height={height} shadows gl={{ antialias: true }} camera={{ fov, near: 0.05, far: 200 }}>
        <CamRig pos={cam} look={look} fov={fov} />
        <fog attach="fog" args={[fog[0], fog[1], fog[2]]} />
        {children}
      </ThreeCanvas>
    </AbsoluteFill>
  );
};

const hex = (c: number[]) => "#" + c.map((v) => Math.round(Math.min(255, Math.max(0, v))).toString(16).padStart(2, "0")).join("");
const rgb = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
const mixc = (a: string, b: string, t: number) => hex(mix3(rgb(a), rgb(b), t));

/** Mouth movement while a line is being spoken. */
const talk = (T: number, a: number, b: number, amt = 0.7) => (T > a && T < b ? 0.25 + amt * Math.abs(Math.sin(T * 13)) * (Math.sin(T * 5.3) > -0.6 ? 1 : 0.2) : 0);
/** Little hop arc for a hop that starts at h and lasts d. */
const hopArc = (T: number, h: number, d: number, height: number) => (T > h && T < h + d ? Math.sin(((T - h) / d) * Math.PI) * height : 0);
const walkBob = (T: number, speed = 8, amt = 0.05) => Math.abs(Math.sin(T * speed)) * amt;

const Sparkles = ({ points, t, amount }: { points: V3[]; t: number; amount: number }) =>
  amount > 0.01 ? (
    <>
      {points.map((p, i) => {
        const tw = Math.max(0, Math.sin(t * 5 + i * 2.1));
        return (
          <sprite key={i} position={[p[0], p[1] + 0.05 + rand(i) * 0.12, p[2]]} scale={[0.12 * tw + 0.02, 0.12 * tw + 0.02, 1]}>
            <spriteMaterial map={softTex()} color="#eef4ff" transparent opacity={amount * tw} depthWrite={false} fog={false} />
          </sprite>
        );
      })}
    </>
  ) : null;

const DAY_LIGHTS = (target: V3, size = 10) => (
  <>
    <hemisphereLight args={["#ffe7c2", "#5d6b2f", 0.9]} />
    <Sun target={target} dir={[-7, 6, 8]} color="#ffd59a" intensity={2.4} size={size} />
  </>
);

/** Soft frontal fill so characters stay readable at night (light travels from `from` toward `to`). */
const NightFill = ({ from, to = [0, 0.5, 0], k = 1 }: { from: V3; to?: V3; k?: number }) => {
  const obj = useMemo(() => new THREE.Object3D(), []);
  obj.position.set(...to);
  obj.updateMatrixWorld();
  return (<><primitive object={obj} /><directionalLight target={obj} position={from} intensity={1.1 * k} color="#c9d4ff" /></>);
};

/* ================================================================ SHOT 1: establishing */
export const Shot1 = () => {
  const t = useStepTime();
  const k = smooth(0, 6.9, t);
  return (
    <Stage sky={["#8fbfe6", "#ffd9a3"]} fog={["#f4d3a2", 18, 85]} fov={42}
      cam={mix3([0.8, 3.6, 16], [0.4, 2.7, 11.5], k)} look={[0, 1.3, -10]}>
      {DAY_LIGHTS([0, 0, 0], 16)}
      <Ground /><Path /><Village windows={0.3} /><VillageTrees /><HillFair glow={0.7} /><Gate glow={0.7} twinkle={t} />
    </Stage>
  );
};

/* ================================================================ SHOT 2: Juniper zips, Pebble hops */
export const Shot2 = () => {
  const t = useStepTime();
  const T = shotStart(1) + t;
  const B = pathAt(3.2);
  const zip = wt(1, "zipped");
  const hops = [wt(1, "hopped"), wt(1, "Hop,"), wt(1, "hop...")];
  const head = pathHeading(2);

  // Juniper: talks + laughs, then turns and dashes away along the path
  const jRun = Math.max(0, T - zip - 0.15);
  const jz = 3.2 - (jRun > 0 ? jRun * 9 + jRun * jRun * 6 : 0);
  const jTurn = smooth(zip - 0.1, zip + 0.15, T);
  const jPos: V3 = [lerp(B[0] - 0.3, pathAt(jz)[0] - 0.1, smooth(0, 0.3, jRun)), 0, jz];
  // Pebble: three hops after her, then keeps bounding off
  let pz = 3.45, ph = 0;
  hops.forEach((h, i) => {
    const d = Math.min(0.42, (hops[i + 1] ?? h + 0.42) - h);
    pz -= smooth(h, h + d, T) * (i === 2 ? 1.6 : 1.1);
    ph += hopArc(T, h, d, 0.35);
  });
  const gone = hops[2] + 0.42;
  if (T > gone) { const r = T - gone; pz -= r * 7; ph += Math.abs(Math.sin(r * 9)) * 0.3; }
  const pTurn = smooth(hops[0] - 0.2, hops[0], T);

  return (
    <Stage sky={["#9cc7ea", "#ffd9a3"]} fog={["#f4d3a2", 10, 60]} fov={32}
      cam={mix3([B[0] + 1.2, 1.15, 7.9], [B[0] + 1.0, 1.05, 7.3], smooth(0, 10, t))} look={[B[0] + 0.05, 0.38, 3.0]}>
      {DAY_LIGHTS([B[0], 0, 2], 8)}
      <Ground /><Path /><Village windows={0.2} /><VillageTrees zMin={-20} /><HillFair glow={0.5} />
      <Juniper position={jPos} rotY={lerp(0.55, head, jTurn)} lean={jRun > 0 ? 0.35 : 0}
        hop={jRun > 0 ? Math.abs(Math.sin(jRun * 22)) * 0.12 : hopArc(T % 0.9, 0, 0.3, T < zip - 0.4 ? 0.06 : 0)}
        squash={T > 8.8 && T < zip ? Math.sin(T * 16) * 0.25 : 0}
        mouth={T < zip ? talk(T, 7.13, 8.75, 0.8) + (T > 8.8 && T < 10.6 ? 0.6 : 0) : 0}
        tail={Math.sin(T * 6)} blink={blink(T, 0.3)} headTilt={T > 8.8 && T < 10.6 ? Math.sin(T * 16) * 0.12 : 0} />
      <Pebble position={[B[0] + 0.32 - smooth(hops[0], hops[0] + 0.4, T) * 0.3, 0, pz]} rotY={lerp(-0.35, head, pTurn)} hop={ph}
        squash={ph > 0 ? -0.3 : 0} headYaw={T < zip + 0.4 ? -0.3 : 0.3 * (1 - pTurn)} blink={blink(T, 1.2)} mouth={T > zip && T < zip + 1 ? 0.6 : 0} />
      <Moss position={[B[0] + 0.62, 0, 2.75]} rotY={0.1} lantern={0.6} headYaw={T > zip ? -0.45 : 0.2} blink={blink(T, 2)}
        headTilt={T > gone ? 0.15 : 0} />
    </Stage>
  );
};

/* ================================================================ SHOT 3: Moss, slow and steady */
export const Shot3 = () => {
  const t = useStepTime();
  const T = shotStart(2) + t;
  const z0 = 4.15, z = z0 - t * 0.13;
  const P = pathAt(z);
  const stretch = Math.sin(t * 3.2);
  const smile = wt(2, "smiled");
  const u0 = uAtZ(z0 + 1.6), u1 = uAtZ(z + 0.32);
  const sparkPts = useMemo(() => Array.from({ length: 16 }, (_, i) => PATH.getPoint(u0 + (i / 16) * 0.05)), [u0]);
  const pts = sparkPts.filter((p) => p.z > z + 0.3).map((p) => [p.x, 0.02, p.z] as V3);
  return (
    <Stage sky={["#a7cbe8", "#ffd09a"]} fog={["#f2cf9c", 6, 40]} fov={34}
      cam={[P[0] + 1.35 - smooth(0, 8.7, t) * 0.15, 0.6, z - 2.05]} look={[P[0] + 0.05, 0.36, z - 0.05]}>
      {DAY_LIGHTS([P[0], 0, z], 6)}
      <pointLight position={[P[0] + 0.6, 0.6, z - 0.9]} color="#ffe2b5" intensity={1.2} distance={4} />
      <Ground /><Path /><Village windows={0.3} /><VillageTrees zMin={-14} /><HillFair glow={0.5} />
      <Trail u0={u0} u1={u1} glow={0.25 + 0.15 * Math.sin(t * 4)} offset={0} />
      <Sparkles points={pts} t={t} amount={smooth(wt(2, "silvery") - 1, wt(2, "silvery"), T) * 0.9} />
      <Moss position={P} rotY={pathHeading(z) - 0.25} stretch={stretch} lantern={0.8 + 0.2 * Math.sin(t * 2)}
        headTilt={T > smile ? 0.12 * smooth(smile, smile + 0.5, T) : 0} headYaw={0.25} blink={blink(T, 0.8)}
        cheeks={0.3 * smooth(smile, smile + 0.6, T)} />
    </Stage>
  );
};

/* ================================================================ SHOT 4: sunset, fog rolls in, lost */
export const Shot4 = () => {
  const t = useStepTime();
  const T = shotStart(3) + t;
  const jStop = wt(3, "Juniper"), pStop = wt(3, "Pebble"), same = wt(3, "Every");
  const dusk = smooth(0.3, 5.5, t), fogK = smooth(1.5, same - shotStart(3), t);
  const look = T > same - 0.3 ? Math.sign(Math.sin((T - same) * 4.2)) * 0.7 : 0;
  const jx = lerp(-4.5, -0.38, smooth(jStop - 1.5, jStop, T));
  const px = lerp(-5, 0.38, smooth(pStop - 1.6, pStop, T));
  const jMoving = T < jStop && T > jStop - 1.5, pMoving = T < pStop && T > pStop - 1.6;
  const fogC = mixc("#f0b582", "#8e96a6", dusk);
  return (
    <Stage sky={[mixc("#f59a62", "#46516e", dusk), mixc("#ffc48a", "#8e96a6", dusk)]} fog={[fogC, lerp(14, 3, fogK), lerp(60, 17, fogK)]} fov={38}
      cam={mix3([0, 1.55, 6.4], [0, 1.25, 4.9], smooth(0, 11, t))} look={[0, 0.65, 0]}>
      <hemisphereLight args={[mixc("#ffd2a0", "#8d9ab8", dusk), "#4b5530", lerp(0.8, 0.7, dusk)]} />
      <Sun target={[0, 0, 0]} dir={[-9, lerp(4, 2, dusk), -6]} color={mixc("#ff9a52", "#7f8db8", dusk)} intensity={lerp(2.4, 0.6, dusk)} size={7} />
      <directionalLight position={[2, 3, 6]} intensity={0.5} color="#c6d0ea" />
      <Ground color="#73914a" /><SameTrees />
      <FogPuffs t={t} amount={fogK * 0.75} color={fogC} center={[0, 0.4, -1.5]} spread={[14, 1.6, 7]} count={22} />
      <Juniper position={[jx, 0, 0.3]} rotY={jMoving ? Math.PI / 2 : look * 0.4} headYaw={look} lean={jMoving ? 0.3 : 0}
        hop={jMoving ? Math.abs(Math.sin(T * 18)) * 0.1 : 0} tail={Math.sin(T * 4) * 0.5} blink={blink(T, 0.5)} mouth={T > same + 1.5 ? 0.3 : 0} />
      <Pebble position={[px, 0, 0.55]} rotY={pMoving ? Math.PI / 2 : -look * 0.4} headYaw={-look} hop={pMoving ? Math.abs(Math.sin(T * 9)) * 0.25 : 0}
        droop={smooth(same, same + 3, T) * 0.5} worry={smooth(same, same + 2, T)} blink={blink(T, 1.7)} />
    </Stage>
  );
};

/* ================================================================ SHOT 5: "Which way is the Fair?" */
export const Shot5 = () => {
  const t = useStepTime();
  const T = shotStart(4) + t;
  const s = TL5();
  return (
    <Stage sky={["#3e4864", "#6d7891"]} fog={["#6d7891", 1.4, 7]} fov={30}
      cam={mix3([0.5, 0.82, 2.85], [0.45, 0.8, 2.6], smooth(0, 3.1, t))} look={[0.12, 0.55, 0.4]}>
      <hemisphereLight args={["#9aa8cc", "#30364a", 0.9]} />
      <Sun target={[0, 0, 0]} dir={[-4, 5, 4]} color="#a9b6dd" intensity={0.9} size={4} />
      <directionalLight position={[1, 1.2, 3]} intensity={0.6} color="#d9def0" />
      <Ground color="#56693d" /><SameTrees />
      <FogPuffs t={t + 11} amount={0.8} color="#7c869e" center={[0, 0.5, -1]} spread={[8, 1.2, 4]} count={14} />
      <Pebble position={[0.3, 0, 0.5]} rotY={0.15} droop={0.5 + 0.5 * smooth(0, 1.2, t)} worry={1} mouth={talk(T, s.a, s.b, 0.35)} blink={blink(T, 2.2)}
        headTilt={0.1} />
      <Juniper position={[-0.3, 0, 0.35]} rotY={0.6} headYaw={0.35} reach={smooth(0.8, 2.0, t)} blink={blink(T, 0.4)} tail={Math.sin(T) * 0.3} />
    </Stage>
  );
};
const TL5 = () => ({ a: wt(4, "Which"), b: wt(4, "whispered", "end") });

/* ================================================================ SHOT 6: the silver line appears */
const TRAIL6 = new THREE.CatmullRomCurve3([[-1.6, 0, 2.6], [-0.6, 0, 1.6], [0.1, 0, 0.6], [0.2, 0, -1.5], [-0.4, 0, -4.5], [0.2, 0, -9]].map(
  (p) => new THREE.Vector3(...(p as V3))));
export const Shot6 = () => {
  const t = useStepTime();
  const T = shotStart(5) + t;
  const sh = wt(5, "shimmered"), its = wt(5, "It's");
  const prog = smooth(sh - 0.3, sh + 2.6, T);
  const pts = useMemo(() => Array.from({ length: 30 }, (_, i) => TRAIL6.getPoint(i / 30)), []);
  const vis = pts.filter((_, i) => i / 30 < prog).map((p) => [p.x, 0.02, p.z] as V3);
  const lit = smooth(sh, sh + 2, T);
  const gasp = T > its - 0.1;
  return (
    <Stage sky={["#0f1733", "#3a4870"]} fog={["#3d4a6e", lerp(2.5, 4, lit), lerp(13, 20, lit)]} fov={38}
      cam={mix3([0.2, 1.45, 4.7], [0.15, 1.25, 4.2], smooth(0, 7.9, t))} look={[0.05, 0.3, 0.3]}>
      <hemisphereLight args={["#5d6fa8", "#1d2236", 0.7]} />
      <Sun target={[0, 0, 0]} dir={[-6, 9, -5]} color="#9fb6ff" intensity={1.1} size={5} />
      <directionalLight position={[0.5, 2, 4]} intensity={0.45} color="#b8c6f0" />
      <pointLight position={[0.1, 0.7, 1.3]} color="#d7e4ff" intensity={lit * 1.2} distance={3} />
      <NightFill from={[0.5, 2, 6]} k={0.8} />
      <Ground color="#46593a" /><SameTrees /><Moon amount={0.9} /><Stars amount={0.5} />
      <FogPuffs t={t + 20} amount={0.6} color="#55628a" center={[0, 0.5, -2]} spread={[10, 1.4, 6]} count={14} />
      <Trail curve={TRAIL6} u0={0} u1={Math.max(0.003, prog)} glow={0.8 + 0.2 * Math.sin(t * 5)} offset={0} width={0.17} />
      <Sparkles points={vis} t={t} amount={smooth(sh - 0.2, sh + 0.5, T)} />
      <Juniper position={[-0.42, 0, 0.6]} rotY={0.45} headTilt={gasp ? -0.05 : 0.3 * lit} headYaw={gasp ? 0.4 : 0.2}
        mouth={gasp ? (T < wt(5, "trail", "end") + 0.2 ? talk(T, its, wt(5, "trail", "end") + 0.1, 0.9) : 0.7) : lit > 0.3 ? 0.5 : 0}
        hop={hopArc(T, its, 0.35, 0.12)} tail={Math.sin(T * 5) * (gasp ? 1 : 0.2)} blink={blink(T, 0.9)} />
      <Pebble position={[0.48, 0, 0.45]} rotY={-0.45} headTilt={0.3 * lit} headYaw={gasp ? -0.4 : -0.15} droop={0.8 * (1 - smooth(its, its + 0.6, T))}
        worry={1 - lit} mouth={lit > 0.3 && !gasp ? 0.6 : 0} hop={hopArc(T, its + 0.1, 0.35, 0.14)} blink={blink(T, 2.5)} />
    </Stage>
  );
};

/* ================================================================ SHOT 7: following the trail to the gate */
export const Shot7 = () => {
  const t = useStepTime();
  const T = shotStart(6) + t;
  const melt = smooth(wt(6, "until") - 0.5, wt(6, "away", "end") + 0.8, T);
  const moss = wt(6, "Moss,");
  const arrive = moss - 0.2;
  const k = smooth(shotStart(6) + 0.2, arrive, T);
  const z = lerp(-15.8, -24.9, k);
  const walking = T < arrive;
  const P = pathAt(z), h = pathHeading(z);
  const camEnd = smooth(arrive - 0.6, arrive + 1.4, T);
  const camA: V3 = [P[0] + 1.1, 1.75, z + 4.6], lookA: V3 = [P[0], 0.45, z - 2.2];
  const fogC = mixc("#46557d", "#27335a", melt);
  return (
    <Stage sky={["#141c3a", mixc("#46557d", "#33416a", melt)]} fog={[fogC, lerp(2.2, 14, melt), lerp(10, 70, melt)]} fov={38}
      cam={mix3(camA, [0.1, 1.75, -22.6], camEnd)} look={mix3(lookA, [0.05, 0.35, -26.4], camEnd)}>
      <hemisphereLight args={["#5f71ac", "#1c2234", 0.75]} />
      <Sun target={[0, 0, z]} dir={[-6, 9, -2]} color="#9fb6ff" intensity={1.0} size={7} />
      <NightFill from={[2, 4, z + 8]} to={[0, 0.5, z - 1]} />
      <Ground color="#4d6340" /><Path /><VillageTrees zMin={-32} zMax={-8} /><HillFair glow={0.4 + melt} />
      <Gate glow={0.3 + 0.9 * melt} twinkle={t} /><Moon amount={0.9} /><Stars amount={0.4 + 0.6 * melt} />
      <FogPuffs t={t} amount={1 - melt} color="#5a6890" center={[0, 0.5, z - 3]} spread={[10, 1.5, 9]} count={18} />
      <Trail u0={uAtZ(-12)} u1={uAtZ(-26.3)} glow={0.85 + 0.15 * Math.sin(t * 4)} offset={0} />
      <Juniper position={[P[0] - 0.32, 0, z]} rotY={h} hop={walking ? walkBob(T, 9, 0.06) : 0} tail={Math.sin(T * 3) * 0.6} blink={blink(T, 0.6)}
        headYaw={walking ? 0 : 0.0} mouth={T > moss ? 0.5 : 0} />
      <Pebble position={[P[0] + 0.32, 0, z + 0.1]} rotY={h} hop={walking ? walkBob(T + 0.3, 9, 0.08) : 0} droop={0.3 * (1 - melt)} blink={blink(T, 1.4)}
        mouth={T > moss ? 0.5 : 0} />
      <Moss position={[0.05, 0, -26.5]} rotY={0} lantern={0.85 + 0.15 * Math.sin(t * 6)} blink={blink(T, 1.1)} cheeks={0.2} />
    </Stage>
  );
};

/* ================================================================ SHOT 8: "You're the one who lit the way" + moral */
export const Shot8 = () => {
  const t = useStepTime();
  const T = shotStart(7) + t;
  const dlg0 = TLs(7).start, dlg1 = TLs(7).end, moral = TLs(8).start;
  const hug = wt(7, "lit") - 0.2;
  const hugK = smooth(hug, hug + 0.5, T) * (1 - smooth(dlg1 + 0.9, dlg1 + 1.4, T));
  const go = dlg1 + 1.3;
  const walk = Math.max(0, T - go);
  const dz = -walk * 0.42;
  const turn = smooth(go - 0.5, go + 0.3, T);
  const app = smooth(dlg0, dlg0 + 1.2, T);
  const wide = smooth(go - 0.6, go + 4.5, T);
  const jFace = lerp(lerp(Math.PI, 1.2, smooth(dlg0 + 0.7, dlg0 + 1.4, T)), Math.PI, turn);
  return (
    <Stage sky={["#141c3a", "#33416a"]} fog={["#27335a", 16, 75]} fov={lerp(34, 42, wide)}
      cam={mix3([1.25, 0.95, -23.6], [0.2, 2.5, -20.2], wide)} look={mix3([-0.15, 0.42, -26.3], [0, 1.25, -28.4], wide)}>
      <hemisphereLight args={["#6576b3", "#1c2234", 0.75]} />
      <Sun target={[0, 0, -26]} dir={[-6, 9, -2]} color="#9fb6ff" intensity={0.9} size={6} />
      <directionalLight position={[3, 2.5, -20]} intensity={0.9} color="#ffd9a8" />
      <NightFill from={[2, 3, -18]} to={[0, 0.5, -26.5]} k={0.7} />
      <Ground color="#4d6340" /><Path /><VillageTrees zMin={-36} zMax={-14} /><HillFair glow={1.4} />
      <Gate glow={1.3} twinkle={t} /><Moon amount={0.9} /><Stars amount={1} />
      <Trail u0={uAtZ(-16)} u1={uAtZ(-26.3)} glow={0.6} offset={0} />
      <FallingLeaves t={t} center={[0, 0.2, -26.6]} amount={smooth(go - 1, go + 1, T)} count={46} />
      <Juniper position={[lerp(-0.32, -0.38, app) + hugK * 0.2, 0, lerp(-24.9, -26.1, app) + dz]} rotY={jFace} lean={hugK * 0.35}
        reach={hugK} cheeks={smooth(dlg0 - 0.3, dlg0 + 0.6, T)} mouth={talk(T, dlg0, dlg1, 0.7)}
        hop={walk > 0 ? walkBob(T, 5, 0.04) : app > 0 && app < 1 ? walkBob(T, 9, 0.06) : hopArc(T, dlg1 + 0.2, 0.35, 0.08)}
        tail={Math.sin(T * 3) * 0.6} blink={blink(T, 0.6)} headTilt={hugK * 0.25} />
      <Pebble position={[lerp(-0.8, -0.75, turn), 0, -26.75 + dz]} rotY={lerp(0.9, Math.PI, turn)} cheeks={0.5} mouth={T > hug && T < go ? 0.3 : 0}
        hop={walk > 0 ? walkBob(T + 0.4, 5, 0.06) : hopArc(T, dlg1 + 0.35, 0.35, 0.12)} blink={blink(T, 1.4)} />
      <Moss position={[0.2, 0, -26.4 + dz]} rotY={lerp(-0.4, Math.PI, turn)} lantern={1} cheeks={0.4 + hugK * 0.4}
        stretch={walk > 0 ? Math.sin(T * 3) : 0} headTilt={hugK * -0.15} blink={blink(T, 1.1)} headYaw={T < moral ? -0.2 : 0} />
    </Stage>
  );
};
import { TL } from "./util";
const TLs = (i: number) => TL.segments[i];
