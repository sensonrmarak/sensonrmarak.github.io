import { AbsoluteFill, Audio, Freeze, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Captions, MoralCard, Title } from "./MossVideo";
import clips from "./clips.json";
import { shotEnd, shotStart } from "./util";

/**
 * Final edit for AI-generated shots: drop shot1.mp4 ... shot8.mp4 into public/moss/clips,
 * run `python3 scripts/probe_clips.py`, then render the "MossAIEdit" composition.
 * Each clip is fitted to its narration slot (speed 0.8x-1.25x, then a hold on the last frame).
 */
const LABELS = [
  "Village establishing shot", "Juniper zips off, Pebble hops after", "Moss, slow and steady", "Sunset, fog rolls in",
  "Pebble: \"Which way is the Fair?\"", "The silver trail appears", "Following the trail to the gate", "The hug and the walk into the Fair",
];

const cover: React.CSSProperties = { width: "100%", height: "100%", objectFit: "cover" };

const Shot = ({ i, slotFrames }: { i: number; slotFrames: number }) => {
  const { fps } = useVideoConfig();
  const dur = (clips as Record<string, number>)[String(i + 1)];
  if (!dur) {
    return (
      <AbsoluteFill style={{ background: "linear-gradient(#26304f,#11162a)", justifyContent: "center", alignItems: "center",
        fontFamily: "Fredoka", color: "#e8c36a", textAlign: "center" }}>
        <div style={{ fontSize: 90, fontWeight: 700 }}>Shot {i + 1}</div>
        <div style={{ fontSize: 48, color: "#fff7e6", marginTop: 20, maxWidth: 800 }}>{LABELS[i]}</div>
        <div style={{ fontSize: 34, color: "#9aa6c8", marginTop: 30 }}>public/moss/clips/shot{i + 1}.mp4</div>
      </AbsoluteFill>
    );
  }
  const slot = slotFrames / fps;
  const rate = Math.min(1.25, Math.max(0.8, dur / slot));
  const playFrames = Math.min(slotFrames, Math.floor((dur / rate) * fps) - 1);
  const src = staticFile(`moss/clips/shot${i + 1}.mp4`);
  return (
    <AbsoluteFill>
      <Sequence durationInFrames={playFrames}><OffthreadVideo src={src} muted playbackRate={rate} style={cover} /></Sequence>
      {playFrames < slotFrames && (
        <Sequence from={playFrames}>
          <Freeze frame={playFrames - 1}><OffthreadVideo src={src} muted playbackRate={rate} style={cover} /></Freeze>
        </Sequence>
      )}
    </AbsoluteFill>
  );
};

export const MossAIEdit = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const f = useCurrentFrame();
  const fade = interpolate(f, [0, 12], [1, 0], { extrapolateRight: "clamp" }) +
    interpolate(f, [durationInFrames - 30, durationInFrames - 1], [0, 1], { extrapolateLeft: "clamp" });
  return (
    <AbsoluteFill style={{ background: "black" }}>
      {LABELS.map((_, i) => {
        const from = Math.round(shotStart(i) * fps), to = Math.round(shotEnd(i) * fps);
        return <Sequence key={i} from={from} durationInFrames={to - from} name={`Shot ${i + 1}`}><Shot i={i} slotFrames={to - from} /></Sequence>;
      })}
      <Sequence durationInFrames={Math.round(7 * fps)} name="Title"><Title /></Sequence>
      <Captions />
      <MoralCard />
      <AbsoluteFill style={{ background: "black", opacity: Math.min(1, fade) }} />
      <Audio src={staticFile("moss/soundtrack.wav")} />
    </AbsoluteFill>
  );
};
