import React from "react";
import { AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { FONT } from "../monsoon/kit";
import { BH, BW, BoardView, K, NAR } from "./engine";
import { BOARDS } from "./boards";

/* UPSC Animated · Indian Monsoon, whiteboard edition. Designed at 1920x1080, rendered at 3840x2160 (vectors x2).
   Layout: whiteboard x 60-1860, y 30-890 (drawing only); caption strip y 915-1065 (captions only); logo bottom-right. */
export const WB_FPS = 24;
export const WB_FRAMES = Math.ceil(NAR.total * WB_FPS);

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
    <div style={{ position: "absolute", left: 160, right: 260, top: 925, height: 130, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center",
      fontFamily: FONT, fontSize: 52, lineHeight: 1.15, color: K }}>
      <div>{p.words.map((w, k) => { const on = T >= w.start - 0.03 && T < (p.words[k + 1]?.start ?? p.end + 0.45);
        return <span key={k} style={{ padding: "0 5px", borderRadius: 8, background: on ? "#f6d36b" : "transparent" }}>{w.text} </span>; })}</div>
    </div>
  );
};

const Inner = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const f = useCurrentFrame(), T = f / fps;
  const idx = Math.max(0, NAR.segments.findIndex((s, i) => T < (NAR.segments[i + 1]?.start ?? 1e9) - 0.45));
  const seg = NAR.segments[idx], board = BOARDS.find((b) => b.id === seg.id)!;
  const wipe = idx === 0 ? 1 : interpolate(T, [seg.start - 0.45, seg.start - 0.1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const fade = interpolate(f, [0, 10], [1, 0], { extrapolateRight: "clamp" }) + interpolate(f, [durationInFrames - 16, durationInFrames - 1], [0, 1], { extrapolateLeft: "clamp" });
  return (
    <AbsoluteFill style={{ background: "linear-gradient(180deg, #d8d3c6 0%, #cfc9ba 100%)" }}>
      {/* whiteboard */}
      <div style={{ position: "absolute", left: 60, top: 30, width: BW, height: BH, background: "linear-gradient(160deg, #ffffff 0%, #f6f6f3 100%)", borderRadius: 10,
        border: "5px solid #b9b9b4", boxShadow: "0 10px 26px rgba(40,35,25,0.28)", overflow: "hidden" }}>
        <div style={{ position: "absolute", inset: 0, opacity: wipe }}><BoardView board={board} T={T} /></div>
      </div>
      {/* marker tray */}
      <div style={{ position: "absolute", left: 660, top: 893, width: 600, height: 12, background: "#a9a9a3", borderRadius: 4, boxShadow: "0 3px 6px rgba(0,0,0,0.25)" }} />
      {["#23201d", "#2456c4", "#d23b2e", "#1f8a4c"].map((c, i) => <div key={i} style={{ position: "absolute", left: 900 + i * 78, top: 884, width: 62, height: 10, background: c, borderRadius: 5 }} />)}
      <Captions T={T} />
      <AbsoluteFill style={{ background: "#d8d3c6", opacity: Math.min(1, fade) }} />
      <Audio src={staticFile("wb/soundtrack.wav")} />
    </AbsoluteFill>
  );
};

export const WbLesson = () => (
  <AbsoluteFill style={{ background: "#d8d3c6" }}>
    <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, transform: "scale(2)", transformOrigin: "0 0" }}>
      <Inner />
    </div>
  </AbsoluteFill>
);
