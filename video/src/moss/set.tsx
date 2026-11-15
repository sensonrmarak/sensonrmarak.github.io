import { useMemo } from "react";
import * as THREE from "three";
import { Clay, Glow, softTex } from "./clay";
import { rand } from "./util";

type V3 = [number, number, number];

/* ---------------------------------------------------------------- path through Oakenvale */
export const PATH = new THREE.CatmullRomCurve3(
  [[0, 0, 8], [0.5, 0, 3], [-0.5, 0, -1], [0.6, 0, -6], [-0.4, 0, -11], [0.3, 0, -16], [0, 0, -21], [0, 0, -27.5]].map(
    (p) => new THREE.Vector3(...(p as V3)),
  ),
);
/** Path parameter u for a given z (path runs monotonically toward -z). */
export const uAtZ = (z: number) => {
  let lo = 0, hi = 1;
  for (let i = 0; i < 30; i++) {
    const m = (lo + hi) / 2;
    if (PATH.getPoint(m).z > z) lo = m; else hi = m;
  }
  return (lo + hi) / 2;
};
export const pathAt = (z: number): V3 => {
  const p = PATH.getPoint(uAtZ(z));
  return [p.x, 0, p.z];
};
/** Heading (rotY) of a walker moving toward -z along the path at z. */
export const pathHeading = (z: number) => {
  const t = PATH.getTangent(uAtZ(z));
  return Math.atan2(t.x, t.z);
};

const ribbonGeo = (curve: THREE.Curve<THREE.Vector3>, u0: number, u1: number, width: number, y: number, segs = 160, wobble = 0) => {
  const pos: number[] = [], idx: number[] = [], uv: number[] = [];
  const n = Math.max(2, Math.round(segs * (u1 - u0)));
  for (let i = 0; i <= n; i++) {
    const u = u0 + ((u1 - u0) * i) / n;
    const p = curve.getPoint(u), t = curve.getTangent(u);
    const side = new THREE.Vector3(-t.z, 0, t.x).normalize();
    const w = width * (1 + wobble * Math.sin(u * 90) * 0.3);
    pos.push(p.x + side.x * w / 2, y, p.z + side.z * w / 2, p.x - side.x * w / 2, y, p.z - side.z * w / 2);
    uv.push(0, i / n, 1, i / n);
    if (i < n) idx.push(i * 2, i * 2 + 1, i * 2 + 2, i * 2 + 1, i * 2 + 3, i * 2 + 2);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(idx);
  g.computeVertexNormals();
  return g;
};

export const Ground = ({ color = "#7f9f4e" }: { color?: string }) => (
  <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
    <planeGeometry args={[160, 160]} />
    <Clay color={color} bump={1.5} />
  </mesh>
);

export const Path = () => {
  const g = useMemo(() => ribbonGeo(PATH, 0, 1, 1.0, 0.012, 200, 1), []);
  return <mesh geometry={g} receiveShadow><Clay color="#c9a26a" bump={2} /></mesh>;
};

/** The glowing silver trail, drawn from u0 up to u1 along the path (or any curve). */
export const Trail = ({ u0 = 0, u1 = 1, glow = 0.5, curve = PATH, offset = 0.18, width = 0.07 }:
  { u0?: number; u1?: number; glow?: number; curve?: THREE.Curve<THREE.Vector3>; offset?: number; width?: number }) => {
  const g = useMemo(() => {
    if (u1 - u0 < 0.002) return null;
    const shifted = new THREE.CatmullRomCurve3(
      Array.from({ length: 80 }, (_, i) => {
        const u = i / 79; const p = curve.getPoint(u); const t = curve.getTangent(u);
        return new THREE.Vector3(p.x - t.z * offset, p.y, p.z + t.x * offset);
      }),
    );
    return ribbonGeo(shifted, u0, u1, width, 0.03, 400);
  }, [u0, u1, curve, offset, width]);
  if (!g) return null;
  return (
    <mesh geometry={g}>
      <meshStandardMaterial color="#dfe8ff" emissive="#cfe0ff" emissiveIntensity={0.3 + glow * 2.6} roughness={0.2} metalness={0.4}
        transparent opacity={0.55 + glow * 0.45} />
    </mesh>
  );
};

/* ---------------------------------------------------------------- trees */
const LEAF = ["#7c9a3a", "#c9862f", "#b4542b", "#9aa23e", "#d9a441"];
export const Oak = ({ position, s = 1, seed = 0, colors }: { position: V3; s?: number; seed?: number; colors?: string[] }) => {
  const pal = colors ?? LEAF;
  return (
    <group position={position} scale={s} rotation={[0, rand(seed) * 6, 0]}>
      <mesh position={[0, 0.8, 0]} castShadow><cylinderGeometry args={[0.16, 0.26, 1.6, 10]} /><Clay color="#6b4429" /></mesh>
      {[0, 1, 2, 3, 4].map((k) => {
        const a = k * 1.4 + seed, r = k === 0 ? 0 : 0.5;
        return (
          <mesh key={k} position={[Math.cos(a) * r, 2.0 + (k === 0 ? 0.35 : rand(seed + k) * 0.3), Math.sin(a) * r]} castShadow>
            <sphereGeometry args={[k === 0 ? 0.85 : 0.6 + rand(seed * 3 + k) * 0.2, 18, 14]} />
            <Clay color={pal[Math.floor(rand(seed * 7 + k) * pal.length)]} />
          </mesh>
        );
      })}
    </group>
  );
};

/** Trees lining the path; skips spots near the houses and the path itself. */
export const VillageTrees = ({ zMin = -30, zMax = 12 }: { zMin?: number; zMax?: number }) => {
  const trees = useMemo(() => {
    const out: { p: V3; s: number; seed: number }[] = [];
    let i = 0;
    for (let z = 12; z > -30; z -= 1.9) {
      for (const side of [-1, 1]) {
        i++;
        const cx = pathAt(z)[0];
        const x = cx + side * (2.6 + rand(i) * 4.5);
        if (z > -3 && z < 6 && Math.abs(x - cx) < 4.2) continue; // houses
        out.push({ p: [x, 0, z + rand(i + 50) * 1.2], s: 0.85 + rand(i + 9) * 0.5, seed: i });
        if (rand(i + 77) > 0.5) out.push({ p: [cx + side * (8 + rand(i + 3) * 6), 0, z], s: 1 + rand(i + 4) * 0.4, seed: i + 300 });
      }
    }
    return out.filter((t) => t.p[2] > zMin && t.p[2] < zMax);
  }, [zMin, zMax]);
  return <>{trees.map((t, k) => <Oak key={k} position={t.p} s={t.s} seed={t.seed} />)}</>;
};

/* ---------------------------------------------------------------- toadstool houses */
export const Toadstool = ({ position, rotY = 0, s = 1, windows = 0.3 }: { position: V3; rotY?: number; s?: number; windows?: number }) => (
  <group position={position} rotation={[0, rotY, 0]} scale={s}>
    <mesh position={[0, 0.5, 0]} castShadow receiveShadow><cylinderGeometry args={[0.42, 0.5, 1.0, 20]} /><Clay color="#efe2c6" /></mesh>
    <mesh position={[0, 0.27, 0.47]} scale={[1, 1.4, 0.3]}><sphereGeometry args={[0.15, 14, 12]} /><Clay color="#7a4a2a" /></mesh>
    <mesh position={[0.24, 0.66, 0.41]}><circleGeometry args={[0.09, 16]} /><Glow color="#ffc861" intensity={windows * 2} /></mesh>
    <mesh position={[0, 1.1, 0]} scale={[1, 0.55, 1]} castShadow><sphereGeometry args={[0.85, 28, 20]} /><Clay color="#c4432d" /></mesh>
    {[0, 1, 2, 3, 4, 5].map((k) => {
      const a = k * 1.05, r = 0.45 + (k % 2) * 0.15;
      return <mesh key={k} position={[Math.cos(a) * r, 1.32 - r * 0.25, Math.sin(a) * r]}><sphereGeometry args={[0.07, 10, 8]} /><Clay color="#fbf5e8" /></mesh>;
    })}
    <mesh position={[0, 1.55, 0]}><sphereGeometry args={[0.08, 10, 8]} /><Clay color="#fbf5e8" /></mesh>
  </group>
);

export const Village = ({ windows = 0.3 }: { windows?: number }) => (
  <>
    <Toadstool position={[-2.3, 0, 3.4]} rotY={0.6} windows={windows} />
    <Toadstool position={[2.5, 0, 1.6]} rotY={-0.8} s={1.15} windows={windows} />
    <Toadstool position={[-2.6, 0, -1.2]} rotY={0.9} s={0.9} windows={windows} />
    <Toadstool position={[2.2, 0, 5.2]} rotY={-0.4} s={0.85} windows={windows} />
    <Toadstool position={[3.4, 0, -2.6]} rotY={-1.1} s={0.8} windows={windows} />
  </>
);

/* ---------------------------------------------------------------- lanterns, gate, hill fair */
const LANTERN = ["#ff9a3c", "#ffd166", "#ff6b5b", "#ffb347"];
export const Lantern = ({ position, c = 0, s = 1, glow = 1 }: { position: V3; c?: number; s?: number; glow?: number }) => (
  <mesh position={position} scale={[s, s * 1.2, s]}>
    <sphereGeometry args={[0.09, 14, 12]} />
    <Glow color={LANTERN[c % LANTERN.length]} intensity={0.8 + glow * 1.8} />
  </mesh>
);

export const Gate = ({ glow = 1, twinkle = 0 }: { glow?: number; twinkle?: number }) => (
  <group position={[0, 0, -27.6]}>
    {[-1, 1].map((s) => (
      <mesh key={s} position={[s * 0.95, 0.85, 0]} castShadow><boxGeometry args={[0.16, 1.7, 0.16]} /><Clay color="#7a5232" /></mesh>
    ))}
    <mesh position={[0, 1.7, 0]}><torusGeometry args={[0.95, 0.07, 10, 32, Math.PI]} /><Clay color="#7a5232" /></mesh>
    <mesh position={[0, 2.68, 0.05]}><boxGeometry args={[0.9, 0.26, 0.05]} /><Clay color="#e8d3a8" /></mesh>
    {Array.from({ length: 7 }, (_, k) => {
      const a = (k / 6) * Math.PI;
      const tw = 0.75 + 0.25 * Math.sin(twinkle * 6 + k * 2);
      return <Lantern key={k} position={[Math.cos(a) * 0.95, 1.7 + Math.sin(a) * 0.95 - 0.16, 0.04]} c={k} glow={glow * tw} />;
    })}
    {[-1, 1].map((s) =>
      Array.from({ length: 5 }, (_, k) => (
        <Lantern key={`${s}${k}`} position={[s * (1.2 + k * 0.5), 1.55 - Math.sin((k / 4) * Math.PI) * 0.25, 0.1]} c={k + 1} s={0.8} glow={glow} />
      )),
    )}
    {glow > 0.05 && <pointLight position={[0, 1.8, 0.8]} color="#ffb25e" intensity={glow * 4} distance={7} decay={1.5} />}
  </group>
);

export const Tent = ({ position, color = "#d9534f", s = 1 }: { position: V3; color?: string; s?: number }) => (
  <group position={position} scale={s}>
    <mesh position={[0, 0.4, 0]} castShadow><cylinderGeometry args={[0.6, 0.6, 0.8, 16]} /><Clay color="#f4ead6" /></mesh>
    <mesh position={[0, 1.05, 0]} castShadow><coneGeometry args={[0.75, 0.6, 16]} /><Clay color={color} /></mesh>
    <mesh position={[0, 1.45, 0]}><sphereGeometry args={[0.05, 8, 6]} /><Clay color="#ffd166" /></mesh>
  </group>
);

export const HillFair = ({ glow = 1 }: { glow?: number }) => {
  const lanterns = useMemo(() => {
    const out: { p: V3; c: number }[] = [];
    for (let k = 0; k < 70; k++) {
      const x = (rand(k) - 0.5) * 14, z = -36 - rand(k + 40) * 14;
      const dz = (z + 46) / 18, dx = x / 18;
      const y = -3 + 6.3 * Math.sqrt(Math.max(0, 1 - dz * dz - dx * dx)) + 0.6 + rand(k + 80) * 0.6;
      out.push({ p: [x, y, z], c: k });
    }
    return out;
  }, []);
  return (
    <group>
      <mesh position={[0, -3, -46]} scale={[1.1, 0.35, 1]} receiveShadow><sphereGeometry args={[18, 48, 32]} /><Clay color="#728f42" bump={2} /></mesh>
      {lanterns.map((l, k) => <Lantern key={k} position={l.p} c={l.c} s={2} glow={glow} />)}
      <Tent position={[-3, 2.6, -40]} s={1.4} />
      <Tent position={[2.5, 2.8, -41]} color="#5b8bd9" s={1.5} />
      <Tent position={[0, 3.1, -44]} color="#e0a43a" s={1.7} />
      <Tent position={[-1.8, 0.05, -30.4]} color="#d9534f" s={0.9} />
      <Tent position={[2.2, 0.05, -30.8]} color="#5b8bd9" s={0.9} />
    </group>
  );
};

/* ---------------------------------------------------------------- atmosphere */
export const FogPuffs = ({ t, amount, color = "#c9ced6", center = [0, 0.6, 0] as V3, spread = [10, 1.2, 8] as V3, count = 18 }:
  { t: number; amount: number; color?: string; center?: V3; spread?: V3; count?: number }) => {
  if (amount <= 0.01) return null;
  return (
    <>
      {Array.from({ length: count }, (_, i) => {
        const x = center[0] + ((rand(i) - 0.5) * spread[0] + t * (0.25 + rand(i + 5) * 0.3) * (i % 2 ? 1 : -1)) % spread[0];
        const y = center[1] + rand(i + 9) * spread[1];
        const z = center[2] + (rand(i + 17) - 0.5) * spread[2];
        const s = 2.5 + rand(i + 3) * 3;
        return (
          <sprite key={i} position={[x, y, z]} scale={[s * 1.8, s, 1]}>
            <spriteMaterial map={softTex()} color={color} transparent opacity={amount * (0.35 + rand(i + 2) * 0.3)} depthWrite={false} fog={false} />
          </sprite>
        );
      })}
    </>
  );
};

export const Stars = ({ amount = 1 }: { amount?: number }) =>
  amount > 0.01 ? (
    <>
      {Array.from({ length: 140 }, (_, i) => (
        <mesh key={i} position={[(rand(i) - 0.5) * 120, 12 + rand(i + 1) * 40, -60 - rand(i + 2) * 10]}>
          <sphereGeometry args={[0.08 + rand(i + 3) * 0.08, 6, 4]} />
          <meshBasicMaterial color="#fff8e0" transparent opacity={amount * (0.5 + rand(i + 4) * 0.5)} fog={false} />
        </mesh>
      ))}
    </>
  ) : null;

export const Moon = ({ position = [-14, 18, -55] as V3, amount = 1 }: { position?: V3; amount?: number }) =>
  amount > 0.01 ? (
    <group position={position}>
      <mesh><sphereGeometry args={[2.2, 32, 24]} /><meshBasicMaterial color="#fff4d6" transparent opacity={amount} fog={false} /></mesh>
      <sprite scale={[14, 14, 1]}><spriteMaterial map={softTex()} color="#a9c1ff" transparent opacity={amount * 0.35} depthWrite={false} fog={false} /></sprite>
    </group>
  ) : null;

export const FallingLeaves = ({ t, center, amount = 1, count = 40 }: { t: number; center: V3; amount?: number; count?: number }) =>
  amount > 0.01 ? (
    <>
      {Array.from({ length: count }, (_, i) => {
        const fall = ((t * (0.35 + rand(i) * 0.25) + rand(i + 1) * 4) % 4);
        const y = center[1] + 3.2 - fall;
        const x = center[0] + (rand(i + 2) - 0.5) * 5 + Math.sin(t * 1.5 + i) * 0.3;
        const z = center[2] + (rand(i + 3) - 0.5) * 3;
        return (
          <mesh key={i} position={[x, y, z]} rotation={[t * 2 + i, t * 1.3 + i * 2, i]} scale={amount}>
            <circleGeometry args={[0.07, 5]} />
            <meshStandardMaterial color={LEAF[i % LEAF.length]} side={THREE.DoubleSide} roughness={0.9} />
          </mesh>
        );
      })}
    </>
  ) : null;

/** Grove of identical, grey-green trees for the lost-in-the-fog shot. */
export const SameTrees = () => (
  <>
    {Array.from({ length: 46 }, (_, i) => {
      const ring = i < 12 ? 3.2 : i < 26 ? 6 : 9.5;
      const a = i * 2.39996;
      const x = Math.cos(a) * ring, z = Math.sin(a) * ring - 1;
      if (z > -0.3 && Math.abs(x) < 2.4 + z * 0.55) return null; // keep the camera's side open
      return <Oak key={i} position={[x, 0, z]} s={1} seed={4} colors={["#6f7d55"]} />;
    })}
  </>
);
