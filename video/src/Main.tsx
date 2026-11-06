import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { createTikTokStyleCaptions, Caption } from "@remotion/captions";
// To add audio: put a file in public/ and use <Audio src={staticFile("music.mp3")} /> from "remotion".

const captions: Caption[] = [
  { text: "Hello", startMs: 0, endMs: 1500, timestampMs: 750, confidence: 1 },
  { text: " from", startMs: 1500, endMs: 3000, timestampMs: 2250, confidence: 1 },
  { text: " Three.js!", startMs: 3000, endMs: 5000, timestampMs: 4000, confidence: 1 },
];
const { pages } = createTikTokStyleCaptions({ captions, combineTokensWithinMilliseconds: 1200 });

const Cube = () => {
  const frame = useCurrentFrame(); // drive animation from frame, never Date/requestAnimationFrame
  return (
    <mesh rotation={[frame * 0.02, frame * 0.03, 0]}>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color="#4f8cff" />
    </mesh>
  );
};

export const Main = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const ms = (frame / fps) * 1000;
  const page = pages.find((p) => ms >= p.startMs && ms < p.startMs + p.durationMs);
  return (
    <AbsoluteFill style={{ backgroundColor: "#111" }}>
      <ThreeCanvas width={width} height={height} camera={{ position: [0, 0, 6] }}>
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 5, 5]} />
        <Cube />
      </ThreeCanvas>
      {page && (
        <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 100 }}>
          <div style={{ color: "white", fontSize: 80, fontFamily: "sans-serif", fontWeight: 800,
            opacity: interpolate(ms - page.startMs, [0, 200], [0, 1], { extrapolateRight: "clamp" }) }}>
            {page.text}
          </div>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
