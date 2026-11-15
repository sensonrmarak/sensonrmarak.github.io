import React, { useContext } from "react";
import { AbsoluteFill, Img, continueRender, delayRender, interpolate, staticFile } from "remotion";
import { StaticMode } from "./map";
import narration from "./narration.json";

/* ---------- Cartoon Explainer kit: parchment paper, inked card, the boxy host, arrows, clouds, rain ---------- */
export type Word = { text: string; start: number; end: number };
export type Seg = { id: string; text: string; start: number; end: number; words: Word[] };
export const NAR = narration as unknown as { total: number; segments: Seg[] };
export const segOf = (id: string) => NAR.segments.find((s) => s.id === id)!;
/** absolute time of the first word in segment `id` that starts with `w` (nth match) */
export const cue = (id: string, w: string, n = 0) => {
  const m = segOf(id).words.filter((x) => x.text.toLowerCase().replace(/[^a-z0-9ñ]/g, "").startsWith(w.toLowerCase()));
  if (!m[n]) throw new Error(`cue ${id}:${w}`);
  return m[n].start;
};

export const C = {
  paper: "#efe5cf", paper2: "#e3d5b6", card: "#fbf6ea", ink: "#2a2420", soft: "#6b5f52",
  brick: "#c8603e", brickDark: "#8e3f27", sun: "#f2a531", sunDark: "#d9822b", rain: "#3f86d6", rainLight: "#9cc5ef",
  red: "#c2402b", green: "#6fb65f", greenLight: "#bfe0a6", land: "#e8dcc1", sea: "#d9e8ea", india: "#f7ecd0", hot: "#e8643a", cold: "#4f8fd6",
  marker: "#f6d36b", grey: "#a69c8e",
};
export const FONT = "Patrick Hand", FONT_SC = "Patrick Hand SC";
if (typeof document !== "undefined") {
  const h = delayRender("monsoon fonts");
  Promise.all([
    new FontFace(FONT, `url(${staticFile("fonts/PatrickHand.woff2")})`).load(),
    new FontFace(FONT_SC, `url(${staticFile("fonts/PatrickHandSC.woff2")})`).load(),
  ]).then((fs) => { fs.forEach((f) => document.fonts.add(f)); continueRender(h); });
}

export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
export const ease = (x: number) => { const t = clamp01(x); return t * t * (3 - 2 * t); };
export const sm = (a: number, b: number, t: number) => ease((t - a) / (b - a));
export const win = (t: number, a: number, b: number, f = 0.4) => sm(a, a + f, t) * (1 - sm(b - f, b, t));
export const lerp = (a: number, b: number, k: number) => a + (b - a) * k;
export const pop = (t: number, a: number) => { const x = clamp01((t - a) / 0.35); return x <= 0 ? 0 : 1 + 0.12 * Math.sin(x * Math.PI) * (1 - x) + (x < 1 ? -0.0 : 0); };

/* hand-drawn wobble (static seed) + paper grain, defined once per frame */
export const Defs = () => (
  <svg width={0} height={0} style={{ position: "absolute" }}>
    <defs>
      <filter id="wob" x="-5%" y="-5%" width="110%" height="110%">
        <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves={2} seed={7} result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale={3.2} xChannelSelector="R" yChannelSelector="G" />
      </filter>
      <filter id="grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={3} seed={3} />
        <feColorMatrix values="0 0 0 0 0.35  0 0 0 0 0.28  0 0 0 0 0.2  0 0 0 0.09 0" />
      </filter>
      <filter id="soft"><feGaussianBlur stdDeviation="6" /></filter>
    </defs>
  </svg>
);

export const Paper = () => useContext(StaticMode) ? (
  <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 42%, #f6eedd 0%, ${C.paper} 55%, ${C.paper2} 100%)` }}>
    <svg width="100%" height="100%" style={{ position: "absolute", inset: 0 }}><rect width="100%" height="100%" filter="url(#grain)" /></svg>
  </AbsoluteFill>
) : <Img src={staticFile("monsoon/static/paper.png")} style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080 }} />;
export const CardFrame = () => (
  <svg width={CARD.w + 40} height={CARD.h + 40} style={{ position: "absolute", left: -20, top: -20, overflow: "visible" }}>
    <g transform="translate(20 20)">
      <rect x={8} y={10} width={CARD.w - 10} height={CARD.h - 10} rx={22} fill="rgba(60,40,20,0.10)" filter="url(#soft)" />
      <g filter="url(#wob)"><rect x={4} y={4} width={CARD.w - 8} height={CARD.h - 8} rx={20} fill={C.card} stroke={C.ink} strokeWidth={4.5} /></g>
    </g>
  </svg>
);

/* the inked card that holds each diagram (x, y, w, h in design px) */
export const CARD = { x: 470, y: 74, w: 1390, h: 806 };
export const Card = ({ title, t, children, appear = 0 }: { title: string; t: number; children?: React.ReactNode; appear?: number }) => {
  const o = sm(appear - 0.25, appear + 0.25, t), s = 0.96 + 0.04 * o;
  return (
    <div style={{ position: "absolute", left: CARD.x, top: CARD.y, width: CARD.w, height: CARD.h, opacity: o, transform: `scale(${s})`, transformOrigin: "50% 50%" }}>
      <Img src={staticFile("monsoon/static/card.png")} style={{ position: "absolute", left: -20, top: -20, width: CARD.w + 40, height: CARD.h + 40 }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 22, textAlign: "center", fontFamily: FONT_SC, fontSize: 46, color: C.ink, letterSpacing: 1 }}>{title}</div>
      {children}
    </div>
  );
};

/* the host: a boxy brick character (eyes blink, arms wave, legs shuffle; optional umbrella, sweat, pointing) */
export type Mood = "idle" | "talk" | "point" | "wow" | "umbrella" | "hot" | "wave" | "think";
export const Host = ({ t, T, mood = "idle", speaking = false, x = 120, y = 560 }: { t: number; T: number; mood?: Mood; speaking?: boolean; x?: number; y?: number }) => {
  const bob = Math.sin(T * 2.2) * 4, blink = (T % 3.3) > 3.15 ? 0.15 : 1;
  const W = 230, H = 165, armL = mood === "wave" ? -40 + Math.sin(T * 9) * 30 : -10 + Math.sin(T * 2.2) * 6;
  const armR = mood === "point" ? -58 : mood === "wave" ? 20 : 12 + Math.sin(T * 2.2 + 1) * 6;
  const mouthOpen = speaking ? (Math.sin(T * 17) > 0.1 ? 1 : 0.35) : 0;
  const eyeH = mood === "wow" ? 34 : 26;
  return (
    <svg width={420} height={380} style={{ position: "absolute", left: x - 80, top: y - 120, overflow: "visible" }} viewBox="-80 -120 420 380">
      <ellipse cx={W / 2} cy={H + 62} rx={W * 0.55} ry={12} fill="rgba(60,40,20,0.15)" />
      <g transform={`translate(0 ${bob})`} filter="url(#wob)">
        {[0, 1, 2, 3].map((i) => <rect key={i} x={28 + i * 50} y={H - 4} width={20} height={58 + (i % 2 ? Math.sin(T * 6) * 3 : 0)} rx={4} fill={C.brickDark} stroke={C.ink} strokeWidth={4} />)}
        <g transform={`rotate(${armL} 0 ${H * 0.45})`}><rect x={-46} y={H * 0.36} width={52} height={22} rx={6} fill={C.brick} stroke={C.ink} strokeWidth={4} /></g>
        <g transform={`rotate(${armR} ${W} ${H * 0.45})`}><rect x={W - 6} y={H * 0.36} width={52} height={22} rx={6} fill={C.brick} stroke={C.ink} strokeWidth={4} /></g>
        <rect x={0} y={0} width={W} height={H} rx={10} fill={C.brick} stroke={C.ink} strokeWidth={5} />
        <line x1={W / 2} y1={6} x2={W / 2} y2={H - 6} stroke={C.brickDark} strokeWidth={3} opacity={0.6} />
        <rect x={W * 0.3} y={H * 0.32} width={18} height={eyeH * blink} rx={6} fill={C.ink} />
        <rect x={W * 0.62} y={H * 0.32} width={18} height={eyeH * blink} rx={6} fill={C.ink} />
        {mouthOpen > 0 ? <ellipse cx={W / 2} cy={H * 0.7} rx={14} ry={4 + 9 * mouthOpen} fill={C.ink} />
          : <path d={`M${W / 2 - 14} ${H * 0.68} Q${W / 2} ${H * (mood === "wow" ? 0.62 : 0.74)} ${W / 2 + 14} ${H * 0.68}`} fill="none" stroke={C.ink} strokeWidth={4} strokeLinecap="round" />}
        {mood === "hot" && <path d={`M${W * 0.9} ${H * 0.12} q 10 18 0 26 q -10 -8 0 -26`} fill={C.rainLight} stroke={C.ink} strokeWidth={3} />}
        {mood === "umbrella" && (
          <g transform={`translate(${W + 30} -30)`}>
            <line x1={0} y1={0} x2={0} y2={150} stroke={C.ink} strokeWidth={6} />
            <path d="M -120 0 Q 0 -110 120 0 Q 90 -20 60 0 Q 30 -20 0 0 Q -30 -20 -60 0 Q -90 -20 -120 0 Z" fill={C.rain} stroke={C.ink} strokeWidth={5} />
          </g>
        )}
      </g>
      {mood === "think" && [0, 1, 2].map((i) => <circle key={i} cx={W * 0.78 + i * 18} cy={-22} r={6} fill={C.ink} opacity={((T * 2 + i * 0.33) % 1) > 0.4 ? 1 : 0.25} />)}
    </svg>
  );
};

/* text with a cream halo, for labels inside diagrams (svg units) */
export const Label = ({ x, y, size, children, color = C.ink, anchor = "middle", o = 1, sc = false, weight }:
  { x: number; y: number; size: number; children: React.ReactNode; color?: string; anchor?: "start" | "middle" | "end"; o?: number; sc?: boolean; weight?: number }) => (
  <text x={x} y={y} fontSize={size} fontFamily={sc ? FONT_SC : FONT} fill={color} textAnchor={anchor} opacity={o} fontWeight={weight}
    stroke={C.card} strokeWidth={size * 0.28} paintOrder="stroke" strokeLinejoin="round">{children}</text>
);

/* catmull-rom smooth polyline through points; returns sampled points */
export const smoothPts = (pts: number[][], n = 18) => {
  if (pts.length < 3) return pts;
  const out: number[][] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    for (let k = 0; k < n; k++) {
      const s = k / n, s2 = s * s, s3 = s2 * s;
      out.push([0, 1].map((j) => 0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * s + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * s2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * s3)));
    }
  }
  out.push(pts[pts.length - 1]);
  return out;
};
const lenOf = (p: number[][]) => p.slice(1).reduce((a, q, i) => a + Math.hypot(q[0] - p[i][0], q[1] - p[i][1]), 0);
/* an arrow that draws itself along `pts` (svg coords), with a head; u = svg units per screen px */
export const Arrow = ({ pts, k, color, w = 9, u = 1, head = 26, dash, o = 1, smooth = true }:
  { pts: number[][]; k: number; color: string; w?: number; u?: number; head?: number; dash?: string; o?: number; smooth?: boolean }) => {
  if (k <= 0.001) return null;
  const P = smooth ? smoothPts(pts) : pts, L = lenOf(P);
  let acc = 0; const cut: number[][] = [P[0]];
  for (let i = 1; i < P.length; i++) {
    const d = Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]);
    if (acc + d >= L * k) { const f = (L * k - acc) / d; cut.push([P[i - 1][0] + (P[i][0] - P[i - 1][0]) * f, P[i - 1][1] + (P[i][1] - P[i - 1][1]) * f]); break; }
    acc += d; cut.push(P[i]);
  }
  const a = cut[cut.length - 1], b = cut[Math.max(0, cut.length - 3)], ang = Math.atan2(a[1] - b[1], a[0] - b[0]), h = head * u;
  const tri = [[a[0] + Math.cos(ang) * h * 0.55, a[1] + Math.sin(ang) * h * 0.55], [a[0] + Math.cos(ang + 2.5) * h, a[1] + Math.sin(ang + 2.5) * h], [a[0] + Math.cos(ang - 2.5) * h, a[1] + Math.sin(ang - 2.5) * h]];
  const d = "M" + cut.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join("L");
  return (
    <g opacity={o} filter="url(#wob)">
      <path d={d} fill="none" stroke={C.ink} strokeWidth={(w + 6) * u} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dash} />
      <path d={d} fill="none" stroke={color} strokeWidth={w * u} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dash} />
      {k > 0.05 && <path d={"M" + tri.map((p) => p.join(" ")).join("L") + "Z"} fill={color} stroke={C.ink} strokeWidth={4 * u} strokeLinejoin="round" />}
    </g>
  );
};

/* a cartoon cloud with optional falling rain (centre x, y; size in px; u = svg units per px) */
export const Cloud = ({ x, y, s, u = 1, T = 0, rain = 0, dark = false, o = 1 }: { x: number; y: number; s: number; u?: number; T?: number; rain?: number; dark?: boolean; o?: number }) => {
  const r = s * u, fill = dark ? "#b9c3cc" : "#ffffff";
  const drops = rain > 0 ? Array.from({ length: 7 }, (_, i) => {
    const ph = ((T * 1.6 + i * 0.37) % 1), dx = (i - 3) * r * 0.32, dy = r * 0.55 + ph * r * 1.1;
    return <line key={i} x1={x + dx} y1={y + dy} x2={x + dx - r * 0.08} y2={y + dy + r * 0.28} stroke={C.rain} strokeWidth={4 * u} strokeLinecap="round" opacity={rain * (1 - ph * 0.6)} />;
  }) : null;
  return (
    <g opacity={o}>
      {drops}
      <g filter="url(#wob)">
        <path d={`M${x - r} ${y + r * 0.45} a ${r * 0.42} ${r * 0.42} 0 0 1 ${r * 0.18} ${-r * 0.78} a ${r * 0.55} ${r * 0.55} 0 0 1 ${r * 0.95} ${-r * 0.3} a ${r * 0.48} ${r * 0.48} 0 0 1 ${r * 0.82} ${r * 0.38} a ${r * 0.4} ${r * 0.4} 0 0 1 ${r * 0.05} ${r * 0.7} Z`}
          fill={fill} stroke={C.ink} strokeWidth={4 * u} strokeLinejoin="round" />
      </g>
    </g>
  );
};

/* a row of little mountain peaks along a polyline (svg coords) */
export const Peaks = ({ pts, size, u = 1, color = "#b9a07a", o = 1, step = 1 }: { pts: number[][]; size: number; u?: number; color?: string; o?: number; step?: number }) => (
  <g opacity={o} filter="url(#wob)">
    {pts.filter((_, i) => i % step === 0).map(([x, y], i) => {
      const h = size * u * (0.8 + 0.4 * ((i * 37) % 7) / 7);
      return <path key={i} d={`M${x - h * 0.7} ${y + h * 0.35} L${x} ${y - h * 0.65} L${x + h * 0.7} ${y + h * 0.35} Z`} fill={color} stroke={C.ink} strokeWidth={3 * u} strokeLinejoin="round" />;
    })}
  </g>
);

export const fmtDate = (d: number) => { // day of year (1 Jan = 0) -> "11 JUN"
  const m = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], dt = new Date(Date.UTC(2025, 0, 1) + Math.round(d) * 864e5);
  return `${dt.getUTCDate()} ${m[dt.getUTCMonth()]}`;
};
export const interp = (x: number, xs: number[], ys: number[]) => interpolate(x, xs, ys, { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
