import React, { useContext } from "react";
import { Img, staticFile } from "remotion";
import narration from "./narration.json";
import world from "./world.json";
import { C, FONT, FONT_SC, CARD, sm } from "../monsoon/kit";
import { StaticMode, baseKey } from "../monsoon/map";

/* ---------- narration timing ---------- */
export type Word = { text: string; start: number; end: number };
export type Seg = { id: string; text: string; start: number; end: number; words: Word[] };
export const NAR = narration as unknown as { total: number; segments: Seg[] };
export const segOf = (id: string) => NAR.segments.find((s) => s.id === id)!;
export const cue = (id: string, w: string, n = 0) => {
  const m = segOf(id).words.filter((x) => x.text.toLowerCase().replace(/[^a-z0-9.]/g, "").startsWith(w.toLowerCase().replace(/[^a-z0-9.]/g, "")));
  if (!m[n]) throw new Error(`cue ${id}:${w}:${n}`);
  return m[n].start;
};

/* ---------- side-panel text ---------- */
export const PANEL = { left: 800, top: 120, w: 540 };
export const Line = ({ T, at, y, children, size = 40, color = C.ink, x = PANEL.left, sc = false, w = PANEL.w }:
  { T: number; at: number; y: number; children: React.ReactNode; size?: number; color?: string; x?: number; sc?: boolean; w?: number }) => {
  const o = sm(at - 0.15, at + 0.35, T);
  return <div style={{ position: "absolute", left: x, top: y, width: Math.min(w, CARD.w - x - 40), fontFamily: sc ? FONT_SC : FONT, fontSize: size, lineHeight: 1.15, color, opacity: o, transform: `translateY(${(1 - o) * 14}px)` }}>{children}</div>;
};
export const Big = ({ T, at, y, children, color = C.red, size = 120, x = PANEL.left }: { T: number; at: number; y: number; children: React.ReactNode; color?: string; size?: number; x?: number }) => {
  const o = sm(at - 0.1, at + 0.3, T), s = 0.7 + 0.3 * o + 0.08 * Math.sin(Math.min(1, Math.max(0, (T - at) / 0.4)) * Math.PI);
  return <div style={{ position: "absolute", left: x, top: y, fontFamily: FONT, fontSize: size, color, opacity: o, transform: `scale(${s})`, transformOrigin: "0% 50%", lineHeight: 1, whiteSpace: "nowrap" }}>{children}</div>;
};
export const txt = (x: number, y: number, s: string, size: number, color = C.ink, anchor: "start" | "middle" | "end" = "middle", o = 1, sc = false) => (
  <text x={x} y={y} fontSize={size} fontFamily={sc ? FONT_SC : FONT} fill={color} textAnchor={anchor} opacity={o} stroke={C.card} strokeWidth={size * 0.25} paintOrder="stroke">{s}</text>
);

/* ---------- the globe: tilted axis, parallels, meridians, night side, overhead Sun ---------- */
export type LatLine = { lat: number; color?: string; w?: number; dash?: string; o?: number };
export const Globe = ({ cx, cy, r, tilt = 0, sunAngle = null, lats = [], meridians = 0, spin = 0, prime = false, axis = true, o = 1, glowLat = null, landTint = true }:
  { cx: number; cy: number; r: number; tilt?: number; sunAngle?: number | null; lats?: LatLine[]; meridians?: number; spin?: number; prime?: boolean; axis?: boolean; o?: number; glowLat?: number | null; landTint?: boolean }) => {
  const th = (tilt * Math.PI) / 180;
  const proj = (lat: number, lon: number) => {
    const p = (lat * Math.PI) / 180, l = (lon * Math.PI) / 180;
    const x = Math.cos(p) * Math.sin(l), y = Math.sin(p), z = Math.cos(p) * Math.cos(l);
    return { X: cx + r * (x * Math.cos(th) + y * Math.sin(th)), Y: cy - r * (-x * Math.sin(th) + y * Math.cos(th)), z };
  };
  const curve = (pts: { X: number; Y: number; z: number }[]) => {
    let d = "", on = false;
    for (const q of pts) { if (q.z > 0) { d += (on ? "L" : "M") + q.X.toFixed(1) + " " + q.Y.toFixed(1); on = true; } else on = false; }
    return d;
  };
  const latPath = (lat: number) => curve(Array.from({ length: 121 }, (_, i) => proj(lat, -180 + i * 3)));
  const lonPath = (lon: number) => curve(Array.from({ length: 61 }, (_, i) => proj(-90 + i * 3, lon)));
  const ax = [Math.sin(th), Math.cos(th)];
  return (
    <g opacity={o}>
      <circle cx={cx} cy={cy} r={r} fill="#8ec5e6" stroke={C.ink} strokeWidth={5} />
      {landTint && <path d={`M${cx - r * 0.55} ${cy - r * 0.25} q ${r * 0.25} ${-r * 0.35} ${r * 0.55} ${-r * 0.1} q ${r * 0.1} ${r * 0.35} ${-r * 0.15} ${r * 0.6} q ${-r * 0.35} ${r * 0.05} ${-r * 0.4} ${-r * 0.5} Z M${cx + r * 0.15} ${cy + r * 0.05} q ${r * 0.35} ${-r * 0.1} ${r * 0.45} ${r * 0.25} q ${-r * 0.05} ${r * 0.35} ${-r * 0.3} ${r * 0.4} q ${-r * 0.2} ${-r * 0.3} ${-r * 0.15} ${-r * 0.65} Z`} fill="#9fd08a" opacity={0.75} />}
      {glowLat !== null && <path d={latPath(glowLat)} fill="none" stroke="#ffe08a" strokeWidth={16} opacity={0.8} strokeLinecap="round" />}
      {Array.from({ length: meridians }, (_, i) => <path key={"m" + i} d={lonPath(spin + (i * 360) / meridians)} fill="none" stroke="#3d6f93" strokeWidth={2} opacity={0.55} />)}
      {prime && <path d={lonPath(spin)} fill="none" stroke={C.red} strokeWidth={5} />}
      {lats.map((l, i) => <path key={i} d={latPath(l.lat)} fill="none" stroke={l.color ?? "#3d6f93"} strokeWidth={l.w ?? 2.5} strokeDasharray={l.dash} opacity={l.o ?? 1} strokeLinecap="round" />)}
      {sunAngle !== null && (() => { const a = sunAngle + Math.PI, x1 = cx + r * Math.cos(a - Math.PI / 2), y1 = cy + r * Math.sin(a - Math.PI / 2), x2 = cx + r * Math.cos(a + Math.PI / 2), y2 = cy + r * Math.sin(a + Math.PI / 2);
        return <path d={`M${x1} ${y1} A ${r} ${r} 0 0 1 ${x2} ${y2} Z`} fill="#1d2440" opacity={0.42} transform={`rotate(0)`} />; })()}
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={C.ink} strokeWidth={5} />
      {axis && <line x1={cx - ax[0] * r * 1.28} y1={cy + ax[1] * r * 1.28} x2={cx + ax[0] * r * 1.28} y2={cy - ax[1] * r * 1.28} stroke={C.ink} strokeWidth={5} strokeLinecap="round" />}
      {axis && <circle cx={cx + ax[0] * r * 1.28} cy={cy - ax[1] * r * 1.28} r={8} fill={C.red} stroke={C.ink} strokeWidth={3} />}
    </g>
  );
};
/** screen point of (lat, lon) on a Globe with the same cx, cy, r, tilt (front side when z > 0) */
export const gpt = (cx: number, cy: number, r: number, tilt: number, lat: number, lon = 0) => {
  const th = (tilt * Math.PI) / 180, p = (lat * Math.PI) / 180, l = (lon * Math.PI) / 180;
  const x = Math.cos(p) * Math.sin(l), y = Math.sin(p);
  return [cx + r * (x * Math.cos(th) + y * Math.sin(th)), cy - r * (-x * Math.sin(th) + y * Math.cos(th))];
};
export const SunIcon = ({ x, y, r, T = 0, o = 1 }: { x: number; y: number; r: number; T?: number; o?: number }) => (
  <g opacity={o}>
    <circle cx={x} cy={y} r={r * 1.5} fill="#ffd66b" opacity={0.25} />
    {Array.from({ length: 12 }, (_, i) => { const a = (i / 12) * Math.PI * 2 + T * 0.3; return <line key={i} x1={x + Math.cos(a) * r * 1.15} y1={y + Math.sin(a) * r * 1.15} x2={x + Math.cos(a) * r * 1.4} y2={y + Math.sin(a) * r * 1.4} stroke={C.sunDark} strokeWidth={5} strokeLinecap="round" />; })}
    <circle cx={x} cy={y} r={r} fill={C.sun} stroke={C.ink} strokeWidth={5} />
  </g>
);

/* ---------- world map (plate carree, x = 10 lon, y = -10 lat); land pre-rendered to PNG ---------- */
export type WView = { lon0: number; lon1: number; lat0: number; lat1: number };
export const WORLD_VIEW: WView = { lon0: -100, lon1: 160, lat0: -45, lat1: 45 };
export const WORLD_BOX = { left: 34, top: 92, w: 1322, h: 640 };
export const W = (lon: number, lat: number) => [lon * 10, -lat * 10];
export const WorldView = ({ left, top, w, h, view, children }: { left: number; top: number; w: number; h: number; view: WView; children?: (u: number) => React.ReactNode }) => {
  const isStatic = useContext(StaticMode);
  const x0 = view.lon0 * 10, y0 = -view.lat1 * 10, vw = (view.lon1 - view.lon0) * 10, vh = (view.lat1 - view.lat0) * 10, u = Math.max(vw / w, vh / h), vb = `${x0} ${y0} ${vw} ${vh}`;
  const box: React.CSSProperties = { position: "absolute", left, top, width: w, height: h, overflow: "hidden", borderRadius: 14 };
  const land = (
    <svg width={w} height={h} viewBox={vb} preserveAspectRatio="xMidYMid meet" style={{ position: "absolute", inset: 0 }}>
      <g filter="url(#wob)">{(world as string[]).map((d, i) => <path key={i} d={d} fill={C.land} stroke="#8f7f63" strokeWidth={2.4 * u} strokeLinejoin="round" />)}</g>
    </svg>);
  if (isStatic) return <div style={box}>{land}</div>;
  return (
    <div style={box}>
      <svg width={w} height={h} viewBox={vb} preserveAspectRatio="xMidYMid meet" style={{ position: "absolute", inset: 0 }}><rect x={x0 - 100} y={y0 - 100} width={vw + 200} height={vh + 200} fill={C.sea} /></svg>
      <Img src={staticFile(`seasons2/static/world_${baseKey(view, w, h)}.png`)} style={{ position: "absolute", inset: 0, width: w, height: h }} />
      <svg width={w} height={h} viewBox={vb} preserveAspectRatio="xMidYMid meet" style={{ position: "absolute", inset: 0, overflow: "hidden" }}>{children && children(u)}</svg>
    </div>
  );
};

/* ---------- tree / plant icons (x, y = base centre; s = scale) ---------- */
export const Tree = ({ kind, x, y, s = 1, o = 1, bare = 0 }: { kind: "rain" | "decid" | "conifer" | "cactus" | "acacia" | "tundra" | "teak"; x: number; y: number; s?: number; o?: number; bare?: number }) => {
  const S = (v: number) => v * s, st = { stroke: C.ink, strokeWidth: 4, strokeLinejoin: "round" as const };
  return (
    <g opacity={o} filter="url(#wob)">
      {kind === "rain" && <><rect x={x - S(9)} y={y - S(230)} width={S(18)} height={S(230)} fill="#7a5233" {...st} />
        {[[-40, -235, 52], [30, -250, 58], [-5, -285, 60], [-55, -170, 40], [50, -175, 42], [0, -130, 38]].map(([dx, dy, rr], i) => <circle key={i} cx={x + S(dx)} cy={y + S(dy)} r={S(rr)} fill={i < 3 ? "#2f7d3a" : "#4f9d45"} {...st} />)}</>}
      {(kind === "decid" || kind === "teak") && <><rect x={x - S(8)} y={y - S(120)} width={S(16)} height={S(120)} fill="#7a5233" {...st} />
        <path d={`M${x} ${y - S(110)} l ${S(-40)} ${S(-40)} M${x} ${y - S(95)} l ${S(38)} ${S(-45)}`} stroke="#7a5233" strokeWidth={S(8)} />
        <ellipse cx={x} cy={y - S(160)} rx={S(78)} ry={S(58)} fill={kind === "teak" ? "#86b04a" : "#7dbb5a"} opacity={1 - bare} {...st} /></>}
      {kind === "conifer" && <><rect x={x - S(7)} y={y - S(40)} width={S(14)} height={S(40)} fill="#7a5233" {...st} />
        {[0, 1, 2].map((i) => <path key={i} d={`M${x - S(55 - i * 12)} ${y - S(35 + i * 45)} L${x} ${y - S(110 + i * 45)} L${x + S(55 - i * 12)} ${y - S(35 + i * 45)} Z`} fill="#2f6b4a" {...st} />)}</>}
      {kind === "cactus" && <path d={`M${x - S(14)} ${y} L${x - S(14)} ${y - S(150)} Q${x} ${y - S(170)} ${x + S(14)} ${y - S(150)} L${x + S(14)} ${y} Z M${x - S(14)} ${y - S(80)} L${x - S(45)} ${y - S(80)} L${x - S(45)} ${y - S(120)} M${x + S(14)} ${y - S(60)} L${x + S(42)} ${y - S(60)} L${x + S(42)} ${y - S(105)}`} fill="#78a85a" stroke={C.ink} strokeWidth={4} strokeLinecap="round" />}
      {kind === "acacia" && <><path d={`M${x} ${y} L${x} ${y - S(90)} L${x - S(45)} ${y - S(140)} M${x} ${y - S(90)} L${x + S(50)} ${y - S(135)}`} stroke="#7a5233" strokeWidth={S(12)} fill="none" strokeLinecap="round" />
        <ellipse cx={x} cy={y - S(150)} rx={S(110)} ry={S(26)} fill="#9aae55" {...st} /></>}
      {kind === "tundra" && [[-40, 0], [0, -6], [40, 0]].map(([dx, dy], i) => <path key={i} d={`M${x + S(dx - 28)} ${y + S(dy)} q ${S(28)} ${S(-40)} ${S(56)} 0 Z`} fill={i === 1 ? "#b9c98a" : "#a7b77e"} {...st} />)}
    </g>
  );
};
