import React from "react";
import { AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { C, Defs, FONT, FONT_SC, Paper, sm } from "../monsoon/kit";
import { NAR } from "./parts";
import * as S from "./scenes";
import { QBadge, SEASONS_QA } from "../monsoon/qa";

/* UPSC Animated · Seasons, solstices and heat zones. Same layout as the monsoon lesson:
   card y 74-880 (graphics), caption strip y 905-1060 (nothing else drawn there), chapter label top-left. */
export const SEASONS_FPS = 24;
export const SEASONS_FRAMES = Math.ceil(NAR.total * SEASONS_FPS);

const Icon = ({ kind }: { kind: "grid" | "orbit" | "sun" | "tree" }) => (
  <svg width={260} height={220} viewBox="0 0 260 220">
    <g filter="url(#wob)" fill={C.card} stroke={C.ink} strokeWidth={6} strokeLinejoin="round">
      {kind === "grid" && <><circle cx={130} cy={110} r={90} fill={C.rainLight} /><ellipse cx={130} cy={110} rx={90} ry={26} fill="none" /><ellipse cx={130} cy={110} rx={36} ry={90} fill="none" /><line x1={40} y1={110} x2={220} y2={110} stroke={C.red} /></>}
      {kind === "orbit" && <><ellipse cx={130} cy={110} rx={110} ry={50} fill="none" strokeDasharray="12 9" /><circle cx={130} cy={110} r={30} fill={C.sun} /><circle cx={232} cy={118} r={18} fill={C.rainLight} /></>}
      {kind === "sun" && <><circle cx={130} cy={110} r={50} fill={C.sun} />{Array.from({ length: 8 }, (_, i) => { const a = i * Math.PI / 4; return <line key={i} x1={130 + 66 * Math.cos(a)} y1={110 + 66 * Math.sin(a)} x2={130 + 96 * Math.cos(a)} y2={110 + 96 * Math.sin(a)} />; })}</>}
      {kind === "tree" && <><rect x={118} y={120} width={24} height={80} fill="#7a5233" /><circle cx={130} cy={90} r={64} fill="#5e9b45" /></>}
    </g>
  </svg>
);

const SCENES: Record<string, (p: { T: number }) => React.ReactElement> = {
  intro: S.Intro,
  p1: ({ T }) => <S.PartCard T={T} id="p1" n={1} title="What are the imaginary lines?" icon={<Icon kind="grid" />} />,
  lat: S.Latitude, lon: S.Longitude, equator: S.Equator, parallels: S.Parallels, india: S.IndiaToc, time: S.TimeScene,
  p2: ({ T }) => <S.PartCard T={T} id="p2" n={2} title="Why do we have seasons?" icon={<Icon kind="orbit" />} />,
  tilt: S.Tilt, orbit: S.Orbit, distance: S.Distance,
  p3: ({ T }) => <S.PartCard T={T} id="p3" n={3} title="What are solstices and equinoxes?" icon={<Icon kind="sun" />} />,
  june: S.June, dec: S.Dec, equinox: S.Equinox, noon: S.Noon,
  p4: ({ T }) => <S.PartCard T={T} id="p4" n={4} title="Why do climates and forests differ?" icon={<Icon kind="tree" />} />,
  eqzone: S.EqZone, rainforest: S.Rainforest, tropics: S.Tropics, desert: S.Desert, india2: S.India2, poles: S.Poles, outro: S.Outro,
};
const GROUPS: [string, string[]][] = [["Part 1 · What are the imaginary lines?", ["p1", "lat", "lon", "equator", "parallels", "india", "time"]],
  ["Part 2 · Why do we have seasons?", ["p2", "tilt", "orbit", "distance"]], ["Part 3 · What are solstices and equinoxes?", ["p3", "june", "dec", "equinox", "noon"]],
  ["Part 4 · Why do climates differ?", ["p4", "eqzone", "rainforest", "tropics", "desert", "india2", "poles"]], ["Summary", ["outro"]]];
const PART = (id: string) => GROUPS.find(([, ids]) => ids.includes(id))?.[0] ?? "";

/* captions: a few words at a time in the strip below the card; the spoken word underlined in marker yellow */
type W = { text: string; start: number; end: number };
const PAGES: { words: W[]; start: number; end: number }[] = [];
NAR.segments.forEach((s) => {
  let cur: W[] = [];
  const flush = () => { if (cur.length) PAGES.push({ words: cur, start: cur[0].start, end: cur[cur.length - 1].end }); cur = []; };
  s.words.forEach((w) => { cur.push(w); const len = cur.reduce((a, x) => a + x.text.length + 1, 0);
    if (/[.!?:]$/.test(w.text) || (/,$/.test(w.text) && len > 26) || len > 52) flush(); });
  flush();
});
const Captions = ({ T }: { T: number }) => {
  const i = PAGES.findIndex((p, k) => T >= p.start - 0.08 && T < Math.min(p.end + 0.45, PAGES[k + 1]?.start ?? 1e9));
  if (i < 0) return null;
  const p = PAGES[i];
  return (
    <div style={{ position: "absolute", left: 160, right: 260, top: 930, height: 110, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center",
      fontFamily: FONT, fontSize: 50, lineHeight: 1.15, color: C.ink }}>
      <div>{p.words.map((w, k) => { const on = T >= w.start - 0.03 && T < (p.words[k + 1]?.start ?? p.end + 0.45);
        return <span key={k} style={{ padding: "0 5px", borderRadius: 8, background: on ? C.marker : "transparent" }}>{w.text} </span>; })}</div>
    </div>
  );
};

const Inner = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const f = useCurrentFrame(), T = f / fps;
  const idx = Math.max(0, NAR.segments.findIndex((s, i) => T < (NAR.segments[i + 1]?.start ?? 1e9) - 0.35));
  const seg = NAR.segments[idx], Scene = SCENES[seg.id];
  const fade = interpolate(f, [0, 12], [1, 0], { extrapolateRight: "clamp" }) + interpolate(f, [durationInFrames - 18, durationInFrames - 1], [0, 1], { extrapolateLeft: "clamp" });
  const part = PART(seg.id);
  return (
    <AbsoluteFill>
      <Defs />
      <Paper />
      <Scene T={T} />
      <QBadge T={T} start={seg.start} end={NAR.segments[idx + 1]?.start ?? 1e9} qa={SEASONS_QA[seg.id]} />
      <div style={{ position: "absolute", left: 40, top: 20, fontFamily: FONT_SC, fontSize: 30, color: C.soft, letterSpacing: 1, opacity: part ? 1 : 0 }}>Seasons and Heat Zones · {part}</div>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
        <path d="M 120 908 Q 960 902 1800 908" fill="none" stroke={C.ink} strokeWidth={2.5} strokeDasharray="10 9" opacity={0.35} />
      </svg>
      <Captions T={T} />
      <AbsoluteFill style={{ background: C.paper, opacity: Math.min(1, fade) * sm(-1, 0, 0) + Math.min(1, fade) }} />
      <Audio src={staticFile("seasons2/soundtrack.wav")} />
    </AbsoluteFill>
  );
};

export const SeasonsLesson = () => (
  <AbsoluteFill style={{ background: C.paper }}>
    <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, transform: "scale(1.3333333)", transformOrigin: "0 0" }}>
      <Inner />
    </div>
  </AbsoluteFill>
);
