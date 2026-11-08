import React from "react";
import { AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { C, Defs, FONT, FONT_SC, NAR, Paper, sm } from "./kit";
import * as S from "./scenes";
import { QBadge, MONSOON_QA } from "./qa";

/* UPSC Animated · Indian Monsoon. Designed at 1920x1080 and drawn at 2560x1440 (vectors scaled 4/3).
   Layout: card y 74-880 (graphics), caption strip y 905-1060 (nothing else drawn there), chapter label top-left. */
export const MONSOON_FPS = 24;
export const MONSOON_FRAMES = Math.ceil(NAR.total * MONSOON_FPS);

const Icon = ({ kind }: { kind: "calendar" | "gears" | "thermo" }) => (
  <svg width={260} height={220} viewBox="0 0 260 220">
    <g filter="url(#wob)" fill={C.card} stroke={C.ink} strokeWidth={6} strokeLinejoin="round">
      {kind === "calendar" && <><rect x={40} y={40} width={180} height={160} rx={14} /><rect x={40} y={40} width={180} height={40} rx={14} fill={C.rain} />
        {[0, 1, 2].map((r) => [0, 1, 2, 3].map((c) => <rect key={`${r}${c}`} x={58 + c * 40} y={98 + r * 32} width={26} height={20} rx={4} fill={c + r * 4 >= 5 && c + r * 4 <= 8 ? C.rainLight : C.card} strokeWidth={3} />))}</>}
      {kind === "gears" && <><circle cx={100} cy={120} r={60} fill={C.sun} /><circle cx={100} cy={120} r={20} /><circle cx={185} cy={70} r={38} fill={C.rainLight} /><circle cx={185} cy={70} r={12} /></>}
      {kind === "thermo" && <><rect x={110} y={20} width={40} height={140} rx={20} /><rect x={120} y={60} width={20} height={110} rx={10} fill={C.hot} strokeWidth={0} /><circle cx={130} cy={175} r={32} fill={C.hot} /></>}
    </g>
  </svg>
);

const SCENES: Record<string, (p: { T: number }) => React.ReactElement> = {
  intro: S.Intro,
  p1: ({ T }) => <S.PartCard T={T} id="p1" n={1} title="What is the monsoon?" icon={<Icon kind="calendar" />} />,
  sw: S.SouthWest, share: S.Share, arabian: S.Arabian, bengal: S.Bengal, ne: S.NorthEast, tn: S.TamilNadu,
  p2: ({ T }) => <S.PartCard T={T} id="p2" n={2} title="Why does it happen?" icon={<Icon kind="gears" />} />,
  heat: S.Heating, coriolis: S.Coriolis, itcz: S.Itcz, jet: S.Jets, ocean: S.Oceans,
  p3: ({ T }) => <S.PartCard T={T} id="p3" n={3} title="How is it changing?" icon={<Icon kind="thermo" />} />,
  lpa: S.Lpa, extreme: S.Extremes, erratic: S.Erratic, cyclone: S.Cyclones, track: S.Track, impact: S.Impacts, outro: S.Outro,
};
const PART = (id: string) => ["p1", "sw", "share", "arabian", "bengal", "ne", "tn"].includes(id) ? "Part 1 · What is the monsoon?"
  : ["p2", "heat", "coriolis", "itcz", "jet", "ocean"].includes(id) ? "Part 2 · Why does it happen?" : ["intro"].includes(id) ? "" : id === "outro" ? "Summary" : "Part 3 · How is it changing?";

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
      <QBadge T={T} start={seg.start} end={NAR.segments[idx + 1]?.start ?? 1e9} qa={MONSOON_QA[seg.id]} />
      <div style={{ position: "absolute", left: 40, top: 20, fontFamily: FONT_SC, fontSize: 30, color: C.soft, letterSpacing: 1, opacity: part ? 1 : 0 }}>Indian Monsoon · {part}</div>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
        <path d="M 120 908 Q 960 902 1800 908" fill="none" stroke={C.ink} strokeWidth={2.5} strokeDasharray="10 9" opacity={0.35} />
      </svg>
      <Captions T={T} />
      <AbsoluteFill style={{ background: C.paper, opacity: Math.min(1, fade) * sm(-1, 0, 0) + Math.min(1, fade) }} />
      <Audio src={staticFile("monsoon/soundtrack.wav")} />
    </AbsoluteFill>
  );
};

export const MonsoonLesson = () => (
  <AbsoluteFill style={{ background: C.paper }}>
    <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, transform: "scale(1.3333333)", transformOrigin: "0 0" }}>
      <Inner />
    </div>
  </AbsoluteFill>
);
