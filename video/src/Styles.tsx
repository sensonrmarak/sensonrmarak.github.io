import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import * as THREE from "three";

type S = "lowpoly" | "diorama" | "paper" | "toon" | "night";
const pal = {
  lowpoly: { sky: "#bfe3f2", ground: "#8ccf7e", roof: "#e07a5f", wall: "#f4e1c1", tree: "#4f9d69", trunk: "#8d5a3b" },
  diorama: { sky: "#f6efe4", ground: "#7fbf6a", roof: "#c9584a", wall: "#fff3dc", tree: "#3f8f5a", trunk: "#7a4e30" },
  paper: { sky: "#f3e6cf", ground: "#a7c97a", roof: "#d96c4f", wall: "#fbf2e0", tree: "#6aa86a", trunk: "#9a6a44" },
  toon: { sky: "#7fd3ff", ground: "#6ee06e", roof: "#ff5a5a", wall: "#fff1b8", tree: "#22b04a", trunk: "#a0522d" },
  night: { sky: "#0d1633", ground: "#2c5450", roof: "#5a3550", wall: "#3b3f5c", tree: "#173a33", trunk: "#3a2a22" },
};

const Mat = ({ s, color, flat = true }: { s: S; color: string; flat?: boolean }) =>
  s === "toon" ? <meshToonMaterial color={color} /> :
  <meshStandardMaterial color={color} flatShading={flat} roughness={s === "paper" ? 1 : 0.8} />;

const Outline = ({ s, children }: { s: S; children: React.ReactNode }) => <>{children}</>;

const House = ({ s, p, x, z, r = 0 }: { s: S; p: any; x: number; z: number; r?: number }) => (
  <group position={[x, 0, z]} rotation={[0, r, 0]}>
    <mesh position={[0, 0.5, 0]} castShadow><boxGeometry args={[1, 1, 1]} /><Mat s={s} color={p.wall} /></mesh>
    <mesh position={[0, 1.35, 0]} rotation={[0, Math.PI / 4, 0]} castShadow><coneGeometry args={[0.95, 0.8, 4]} /><Mat s={s} color={p.roof} /></mesh>
    {s === "night" && <mesh position={[0, 0.5, 0.51]}><planeGeometry args={[0.3, 0.3]} /><meshBasicMaterial color="#ffd27a" /></mesh>}
    {s === "night" && <pointLight position={[0, 0.5, 0.9]} color="#ffb84d" intensity={6} distance={4} />}
  </group>
);
const Tree = ({ s, p, x, z, h = 1 }: { s: S; p: any; x: number; z: number; h?: number }) => (
  <group position={[x, 0, z]} scale={h}>
    <mesh position={[0, 0.3, 0]} castShadow><cylinderGeometry args={[0.08, 0.1, 0.6, 6]} /><Mat s={s} color={p.trunk} /></mesh>
    <mesh position={[0, 0.9, 0]} castShadow>{s === "paper" ? <coneGeometry args={[0.45, 1, 3]} /> : <icosahedronGeometry args={[0.5, 0]} />}<Mat s={s} color={p.tree} /></mesh>
  </group>
);

const Village = ({ s }: { s: S }) => {
  const p = pal[s];
  const ground = s === "diorama"
    ? <mesh position={[0, -0.6, 0]} receiveShadow><cylinderGeometry args={[4, 3.2, 1.2, 10]} /><Mat s={s} color={p.ground} /></mesh>
    : <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><circleGeometry args={[30, 24]} /><Mat s={s} color={p.ground} /></mesh>;
  return (
    <group>
      {ground}
      {s === "diorama" && <mesh position={[0, -1.6, 0]}><coneGeometry args={[3.2, 2, 10]} /><Mat s={s} color="#8a6a4a" /></mesh>}
      <House s={s} p={p} x={-1.2} z={0} r={0.3} />
      <House s={s} p={p} x={1.1} z={-0.6} r={-0.4} />
      <House s={s} p={p} x={0.2} z={1.4} r={0.1} />
      {[[-2.5, -1.5, 1.2], [2.6, 1, 1], [-2.2, 1.8, 0.9], [2.2, -2.2, 1.3], [0, -2.4, 1.1], [-0.6, -1, 0.7]].map(([x, z, h], i) =>
        <Tree key={i} s={s} p={p} x={x} z={z} h={h} />)}
    </group>
  );
};

const Stars = () => {
  const pts = Array.from({ length: 120 }, (_, i) => [Math.sin(i * 12.9898) * 20, 4 + Math.abs(Math.cos(i * 78.233)) * 10, -12 + Math.sin(i * 3.1) * 4]);
  return <>{pts.map((q, i) => <mesh key={i} position={q as any}><sphereGeometry args={[0.05, 4, 4]} /><meshBasicMaterial color="#fff" /></mesh>)}
    <mesh position={[6, 9, -14]}><sphereGeometry args={[1, 16, 16]} /><meshBasicMaterial color="#fff6d5" /></mesh></>;
};
const Fireflies = ({ f }: { f: number }) => <>{Array.from({ length: 25 }, (_, i) =>
  <mesh key={i} position={[Math.sin(i * 1.7 + f * 0.03) * 3, 0.5 + Math.abs(Math.sin(i + f * 0.05)) * 1.5, Math.cos(i * 2.3 + f * 0.02) * 3]}>
    <sphereGeometry args={[0.04, 6, 6]} /><meshBasicMaterial color="#fff27a" /></mesh>)}</>;

export const StyleScene = ({ style }: { style: S }) => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const a = f * 0.008 + 0.6;
  const d = style === "diorama" ? 9 : 7.5;
  const cam = new THREE.Vector3(Math.sin(a) * d, style === "diorama" ? 5.5 : 3.2, Math.cos(a) * d);
  const titles: Record<S, string> = { lowpoly: "1 · Low-poly storybook", diorama: "2 · Diorama / tiny world", paper: "3 · Paper pop-up book", toon: "4 · Toon-shaded", night: "5 · Cosy night magic" };
  return (
    <AbsoluteFill style={{ background: style === "diorama" ? "radial-gradient(#fffaf0,#e9dcc6)" : pal[style].sky }}>
      <ThreeCanvas width={width} height={height} shadows
        camera={{ position: cam.toArray() as any, fov: 40 }}
        onCreated={({ camera }) => camera.lookAt(0, 0.6, 0)}>
        <CamLook pos={cam} />
        {style === "night" ? <><ambientLight intensity={1.1} color="#6a7bd6" /><directionalLight position={[6, 9, -14]} intensity={1.2} color="#9fb4ff" /><Stars /><Fireflies f={f} /></>
          : <><ambientLight intensity={style === "toon" ? 0.6 : 0.55} /><directionalLight position={[5, 8, 4]} intensity={style === "paper" ? 1.2 : 1.6} castShadow shadow-mapSize={[2048, 2048]} /></>}
        {style !== "diorama" && style !== "night" && <fog attach="fog" args={[pal[style].sky, 12, 30]} />}
        <Village s={style} />
      </ThreeCanvas>
      {style === "paper" && <AbsoluteFill style={{ background: "repeating-linear-gradient(45deg,rgba(120,90,50,.05) 0 2px,transparent 2px 6px)", mixBlendMode: "multiply" }} />}
      {style === "diorama" && <AbsoluteFill style={{ backdropFilter: "blur(0px)", background: "linear-gradient(rgba(255,255,255,.35),transparent 25%,transparent 75%,rgba(255,255,255,.35))" }} />}
      <div style={{ position: "absolute", left: 40, top: 30, fontFamily: "sans-serif", fontWeight: 800, fontSize: 56, color: style === "night" ? "#ffe9a8" : "#2b2b2b", textShadow: "0 2px 8px rgba(0,0,0,.25)" }}>{titles[style]}</div>
      <div style={{ position: "absolute", right: 40, bottom: 30, fontFamily: "Georgia,serif", fontStyle: "italic", fontSize: 40, color: style === "night" ? "#ffe9a8" : "#3b2a1a" }}>Oakenvale Tales</div>
    </AbsoluteFill>
  );
};

import { useThree } from "@react-three/fiber";
const CamLook = ({ pos }: { pos: THREE.Vector3 }) => { const { camera } = useThree(); camera.position.copy(pos); camera.lookAt(0, 0.6, 0); return null; };
