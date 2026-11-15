import { Clay, Eye, Glow } from "./clay";

type V3 = [number, number, number];
export type Pose = {
  position?: V3;
  rotY?: number;
  hop?: number; // vertical offset
  squash?: number; // -1..1 (positive = squashed)
  lean?: number; // forward lean (rad)
  headYaw?: number;
  headTilt?: number;
  blink?: number; // 0 open .. 1 closed
  mouth?: number; // 0 smile .. 1 open "o"
  cheeks?: number; // pink blush 0..1
  scale?: number;
};

const Mouth = ({ open = 0, w = 0.05, y = 0, z = 0 }: { open?: number; w?: number; y?: number; z?: number }) =>
  open > 0.15 ? (
    <mesh position={[0, y, z]} scale={[1, 0.6 + open * 0.8, 1]}>
      <sphereGeometry args={[w * 0.55, 16, 12]} />
      <meshStandardMaterial color="#4a1c18" roughness={0.5} />
    </mesh>
  ) : (
    <mesh position={[0, y + w * 0.35, z]} rotation={[0, 0, Math.PI]}>
      <torusGeometry args={[w, w * 0.18, 8, 20, Math.PI]} />
      <meshStandardMaterial color="#3a1a14" roughness={0.6} />
    </mesh>
  );

const Cheeks = ({ amt, x, y, z, r = 0.045 }: { amt: number; x: number; y: number; z: number; r?: number }) =>
  amt > 0.02 ? (
    <>
      {[-1, 1].map((s) => (
        <mesh key={s} position={[s * x, y, z]} scale={[1, 0.7, 0.4]}>
          <sphereGeometry args={[r, 12, 10]} />
          <meshStandardMaterial color="#ff7a8a" transparent opacity={amt * 0.85} roughness={0.8} />
        </mesh>
      ))}
    </>
  ) : null;

const Body = ({ p, children }: { p: Pose; children: React.ReactNode }) => {
  const sq = p.squash ?? 0;
  return (
    <group position={p.position ?? [0, 0, 0]} rotation={[0, p.rotY ?? 0, 0]} scale={p.scale ?? 1}>
      <group position={[0, p.hop ?? 0, 0]} rotation={[p.lean ?? 0, 0, 0]} scale={[1 + sq * 0.15, 1 - sq * 0.2, 1 + sq * 0.15]}>
        {children}
      </group>
    </group>
  );
};

/* ------------------------------------------------------------------ Moss the snail */
export const Moss = (p: Pose & { lantern?: number; stretch?: number }) => {
  const body = "#c8e29a", shell = "#6d9440", swirl = "#4d6f2b";
  const st = p.stretch ?? 0;
  return (
    <Body p={p}>
      {/* foot */}
      <mesh position={[0, 0.11, 0.02]} rotation={[Math.PI / 2, 0, 0]} scale={[1, 1 + st * 0.12, 0.75]} castShadow>
        <capsuleGeometry args={[0.15, 0.62, 8, 20]} />
        <Clay color={body} />
      </mesh>
      {/* neck + head */}
      <mesh position={[0, 0.3, 0.36]} rotation={[0.35, 0, 0]} castShadow>
        <capsuleGeometry args={[0.13, 0.22, 8, 16]} />
        <Clay color={body} />
      </mesh>
      <group position={[0, 0.5, 0.44]} rotation={[p.headTilt ?? 0, p.headYaw ?? 0, 0]}>
        <mesh castShadow><sphereGeometry args={[0.17, 28, 22]} /><Clay color={body} /></mesh>
        {[-1, 1].map((s) => (
          <group key={s}>
            <mesh position={[s * 0.07, 0.04, 0.135]} scale={[1, 1 - (p.blink ?? 0) * 0.9, 1]}><Eye r={0.06} /></mesh>
            <mesh position={[s * 0.06, 0.22, -0.02]} rotation={[-0.2, 0, s * -0.3]}>
              <capsuleGeometry args={[0.018, 0.16, 4, 8]} /><Clay color={body} />
            </mesh>
            <mesh position={[s * 0.088, 0.31, -0.04]}><sphereGeometry args={[0.035, 12, 10]} /><Clay color={body} /></mesh>
          </group>
        ))}
        <Mouth open={p.mouth ?? 0} w={0.045} y={-0.06} z={0.15} />
        <Cheeks amt={p.cheeks ?? 0} x={0.11} y={-0.03} z={0.12} r={0.035} />
      </group>
      {/* shell with swirl */}
      <group position={[0, 0.4, -0.12]}>
        <mesh scale={[0.72, 1, 1]} castShadow><sphereGeometry args={[0.3, 28, 22]} /><Clay color={shell} /></mesh>
        {[-1, 1].map((s) => (
          <group key={s} position={[s * 0.2, 0, 0]} rotation={[0, Math.PI / 2, 0]}>
            <mesh><torusGeometry args={[0.17, 0.035, 10, 32]} /><Clay color={swirl} /></mesh>
            <mesh position={[0.02, 0.02, s * 0.02]}><torusGeometry args={[0.085, 0.03, 10, 24]} /><Clay color={swirl} /></mesh>
          </group>
        ))}
        {[[0.08, 0.25, 0.08], [-0.1, 0.22, -0.1], [0.02, 0.27, -0.03], [-0.05, 0.2, 0.15]].map((q, i) => (
          <mesh key={i} position={q as V3}><sphereGeometry args={[0.05, 10, 8]} /><Clay color="#8fb85a" /></mesh>
        ))}
        {/* tiny mushroom lantern */}
        <group position={[0, 0.3, 0]}>
          <mesh position={[0, 0.05, 0]}><cylinderGeometry args={[0.025, 0.03, 0.1, 10]} /><Clay color="#f3e7cf" /></mesh>
          <mesh position={[0, 0.11, 0]} scale={[1, 0.6, 1]}>
            <sphereGeometry args={[0.08, 18, 14]} />
            <Glow color="#ff9a2e" intensity={0.4 + (p.lantern ?? 1) * 1.6} />
          </mesh>
          {(p.lantern ?? 0) > 0.05 && <pointLight position={[0, 0.2, 0.1]} color="#ffb347" intensity={(p.lantern ?? 0) * 2.5} distance={2.5} decay={1.6} />}
        </group>
      </group>
    </Body>
  );
};

/* ------------------------------------------------------------------ Juniper the squirrel */
export const Juniper = (p: Pose & { tail?: number; reach?: number }) => {
  const fur = "#b4492a", cream = "#f1dcb5", scarf = "#d9a330";
  const tw = p.tail ?? 0;
  const tailPts: [number, number, number, number][] = [
    [0, 0.2, -0.24, 0.12], [0, 0.36, -0.36, 0.16], [0, 0.56, -0.44, 0.19], [0, 0.78, -0.44, 0.2],
    [0, 0.96, -0.36, 0.19], [0, 1.06, -0.22, 0.16], [0, 1.04, -0.1, 0.12],
  ];
  const reach = p.reach ?? 0;
  return (
    <Body p={p}>
      <mesh position={[0, 0.32, 0]} scale={[1, 1.15, 0.95]} castShadow><sphereGeometry args={[0.25, 28, 22]} /><Clay color={fur} /></mesh>
      <mesh position={[0, 0.3, 0.155]} scale={[0.8, 1.05, 0.5]}><sphereGeometry args={[0.2, 24, 18]} /><Clay color={cream} /></mesh>
      {/* feet */}
      {[-1, 1].map((s) => (
        <mesh key={s} position={[s * 0.12, 0.05, 0.08]} scale={[1, 0.6, 1.4]} castShadow><sphereGeometry args={[0.08, 14, 10]} /><Clay color={fur} /></mesh>
      ))}
      {/* arms (right arm can reach out) */}
      <mesh position={[-0.23, 0.34, 0.06]} rotation={[-0.2, 0, -0.35]}><capsuleGeometry args={[0.05, 0.14, 6, 10]} /><Clay color={fur} /></mesh>
      <mesh position={[0.23 + reach * 0.05, 0.34 + reach * 0.04, 0.06 + reach * 0.14]} rotation={[-0.2 - reach * 1.3, 0, 0.35 - reach * 0.15]}>
        <capsuleGeometry args={[0.05, 0.14 + reach * 0.08, 6, 10]} /><Clay color={fur} />
      </mesh>
      {/* tail */}
      <group rotation={[tw * 0.15, 0, tw * 0.12]}>
        {tailPts.map(([x, y, z, r], i) => (
          <mesh key={i} position={[x + Math.sin(i * 0.9 + tw * 3) * 0.02 * i * tw, y, z]} castShadow>
            <sphereGeometry args={[r, 20, 16]} /><Clay color={i % 2 ? "#c2552f" : fur} />
          </mesh>
        ))}
      </group>
      {/* scarf */}
      <mesh position={[0, 0.54, 0]} rotation={[Math.PI / 2 - 0.1, 0, 0]}><torusGeometry args={[0.16, 0.055, 12, 28]} /><Clay color={scarf} /></mesh>
      <mesh position={[0.09, 0.44, 0.16]} rotation={[0.2, 0, -0.25]} castShadow><boxGeometry args={[0.08, 0.2, 0.04]} /><Clay color={scarf} /></mesh>
      {/* head */}
      <group position={[0, 0.72, 0.02]} rotation={[p.headTilt ?? 0, p.headYaw ?? 0, 0]}>
        <mesh castShadow><sphereGeometry args={[0.21, 28, 22]} /><Clay color={fur} /></mesh>
        <mesh position={[0, -0.06, 0.15]} scale={[1, 0.8, 0.8]}><sphereGeometry args={[0.1, 18, 14]} /><Clay color={cream} /></mesh>
        <mesh position={[0, -0.02, 0.24]}><sphereGeometry args={[0.03, 10, 8]} /><meshStandardMaterial color="#2a1510" roughness={0.3} /></mesh>
        {[-1, 1].map((s) => (
          <group key={s}>
            <mesh position={[s * 0.085, 0.03, 0.17]} scale={[1, 1 - (p.blink ?? 0) * 0.9, 1]}><Eye r={0.055} /></mesh>
            <mesh position={[s * 0.12, 0.2, -0.02]} rotation={[0, 0, s * -0.25]} castShadow>
              <coneGeometry args={[0.065, 0.17, 14]} /><Clay color={fur} />
            </mesh>
            <mesh position={[s * 0.13, 0.3, -0.02]} rotation={[0, 0, s * -0.4]}><coneGeometry args={[0.025, 0.08, 8]} /><Clay color="#7d2e18" /></mesh>
          </group>
        ))}
        <Mouth open={p.mouth ?? 0} w={0.04} y={-0.11} z={0.2} />
        <Cheeks amt={p.cheeks ?? 0} x={0.13} y={-0.05} z={0.15} />
      </group>
    </Body>
  );
};

/* ------------------------------------------------------------------ Pebble the rabbit */
export const Pebble = (p: Pose & { droop?: number; worry?: number }) => {
  const grey = "#a9a7ae", light = "#dcd9df", blue = "#4a7cc4";
  const d = p.droop ?? 0, w = p.worry ?? 0;
  return (
    <Body p={p}>
      <mesh position={[0, 0.3, 0]} scale={[1, 1, 0.95]} castShadow><sphereGeometry args={[0.27, 28, 22]} /><Clay color={grey} /></mesh>
      <mesh position={[0, 0.27, 0.17]} scale={[0.75, 0.9, 0.5]}><sphereGeometry args={[0.2, 24, 18]} /><Clay color={light} /></mesh>
      <mesh position={[0, 0.22, -0.27]}><sphereGeometry args={[0.08, 14, 10]} /><Clay color="#f4f2f5" /></mesh>
      {[-1, 1].map((s) => (
        <mesh key={s} position={[s * 0.13, 0.05, 0.1]} scale={[1, 0.6, 1.6]} castShadow><sphereGeometry args={[0.085, 14, 10]} /><Clay color={grey} /></mesh>
      ))}
      {[-1, 1].map((s) => (
        <mesh key={s} position={[s * 0.23, 0.33, 0.1]} rotation={[0.5, 0, s * 0.4]}><capsuleGeometry args={[0.05, 0.1, 6, 10]} /><Clay color={grey} /></mesh>
      ))}
      {/* satchel + strap */}
      <mesh position={[0.21, 0.2, 0.14]} rotation={[0, 0.5, 0]} castShadow><boxGeometry args={[0.15, 0.13, 0.07]} /><Clay color={blue} /></mesh>
      <mesh position={[0.21, 0.25, 0.18]} rotation={[0, 0.5, 0]}><boxGeometry args={[0.15, 0.04, 0.03]} /><Clay color="#365f9e" /></mesh>
      <mesh position={[0, 0.36, 0]} rotation={[Math.PI / 2 + 0.05, 0.6, 0]}><torusGeometry args={[0.27, 0.018, 8, 36]} /><Clay color={blue} /></mesh>
      {/* head */}
      <group position={[0, 0.68, 0.02]} rotation={[(p.headTilt ?? 0) + d * 0.15, p.headYaw ?? 0, 0]}>
        <mesh castShadow><sphereGeometry args={[0.22, 28, 22]} /><Clay color={grey} /></mesh>
        {[-1, 1].map((s) => (
          <mesh key={s} position={[s * 0.05, -0.08, 0.17]}><sphereGeometry args={[0.055, 14, 10]} /><Clay color={light} /></mesh>
        ))}
        <mesh position={[0, -0.04, 0.21]} scale={[1.2, 0.8, 1]}><sphereGeometry args={[0.025, 10, 8]} /><meshStandardMaterial color="#e8879a" roughness={0.5} /></mesh>
        {[-1, 1].map((s) => (
          <group key={s}>
            <mesh position={[s * 0.085, 0.04, 0.17]} scale={[1, 1 - (p.blink ?? 0) * 0.9, 1]}><Eye r={0.055} /></mesh>
            {/* worried brows */}
            <mesh position={[s * 0.085, 0.115 + w * 0.01, 0.19]} rotation={[0, 0, Math.PI / 2 - s * (0.08 + w * 0.4)]}>
              <capsuleGeometry args={[0.009, 0.05, 4, 6]} /><meshStandardMaterial color="#5e5a63" />
            </mesh>
          </group>
        ))}
        <Mouth open={p.mouth ?? 0} w={0.03} y={-0.12} z={0.19} />
        <Cheeks amt={p.cheeks ?? 0} x={0.13} y={-0.05} z={0.15} />
        {/* ears: right upright, left floppy */}
        <group position={[0.08, 0.17, -0.02]} rotation={[-0.1 - d * 0.9, 0, -0.12 - d * 0.5]}>
          <mesh position={[0, 0.17, 0]} scale={[1, 1, 0.55]} castShadow><capsuleGeometry args={[0.055, 0.26, 8, 14]} /><Clay color={grey} /></mesh>
          <mesh position={[0, 0.17, 0.03]} scale={[0.55, 0.85, 0.3]}><capsuleGeometry args={[0.05, 0.24, 8, 10]} /><Clay color="#e9b6c0" /></mesh>
        </group>
        <group position={[-0.1, 0.15, -0.02]} rotation={[-0.1 - d * 0.4, 0, 1.0 + d * 0.5]}>
          <mesh position={[0, 0.16, 0]} scale={[1, 1, 0.55]} castShadow><capsuleGeometry args={[0.055, 0.24, 8, 14]} /><Clay color={grey} /></mesh>
        </group>
      </group>
    </Body>
  );
};
