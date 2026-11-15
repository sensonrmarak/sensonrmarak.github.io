import { AbsoluteFill, useVideoConfig } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { useThree } from "@react-three/fiber";
import { Moss, Juniper, Pebble } from "./characters";
import { Clay } from "./clay";

const Cam = () => { const { camera } = useThree(); camera.position.set(0.3, 0.9, 3.2); camera.lookAt(0, 0.45, 0); return null; };
export const CastTest = () => {
  const { width, height } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: "linear-gradient(#f6e6c8,#e8c99a)" }}>
      <ThreeCanvas width={width} height={height} shadows camera={{ fov: 35 }}>
        <Cam />
        <hemisphereLight args={["#fff1d6", "#6b7a3a", 0.9]} />
        <directionalLight position={[3, 5, 4]} intensity={2.2} color="#ffe0b0" castShadow shadow-mapSize={[2048, 2048]} />
        <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><circleGeometry args={[6, 48]} /><Clay color="#86a956" /></mesh>
        <Juniper position={[-0.75, 0, 0]} rotY={0.35} cheeks={0.6} tail={0.5} />
        <Moss position={[0.05, 0, 0.25]} rotY={0.5} lantern={1} />
        <Pebble position={[0.85, 0, 0]} rotY={-0.35} worry={0.5} />
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
