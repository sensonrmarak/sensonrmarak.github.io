import { useCurrentFrame, useVideoConfig } from "remotion";
import timeline from "./timeline.json";

export const TL = timeline as {
  fps: number;
  total: number;
  shots: number[];
  segments: { start: number; end: number; text: string; words: { text: string; start: number; end: number }[] }[];
};

/** Absolute time (s) of the first word in a segment containing `word`. */
export const wt = (seg: number, word: string, which: "start" | "end" = "start") => {
  const w = TL.segments[seg].words.find((x) => x.text.toLowerCase().includes(word.toLowerCase()));
  if (!w) throw new Error(`word ${word} not in segment ${seg}`);
  return w[which];
};

export const shotStart = (i: number) => TL.shots[i];
export const shotEnd = (i: number) => (i + 1 < TL.shots.length ? TL.shots[i + 1] : TL.total);

/** Shot-local time in seconds, quantised "on twos" for a stop-motion feel. */
export const useStepTime = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (Math.floor(f / 2) * 2) / fps;
};

export const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
export const smooth = (a: number, b: number, t: number) => {
  const x = clamp01((t - a) / (b - a));
  return x * x * (3 - 2 * x);
};
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const mix3 = (a: number[], b: number[], t: number) => a.map((v, i) => lerp(v, b[i], t)) as [number, number, number];

/** Deterministic pseudo random in [0,1). */
export const rand = (i: number) => {
  const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

/** Blink: closed briefly every few seconds (0 open, 1 closed). */
export const blink = (t: number, offset = 0) => {
  const p = (t + offset) % 3.3;
  return p > 3.1 ? 1 : 0;
};
