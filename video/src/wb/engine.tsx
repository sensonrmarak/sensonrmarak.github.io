import React from "react";
import narration from "./narration.json";
import { FONT } from "../monsoon/kit";

/* Whiteboard engine: a marker writes text and draws paths on a 1800x860 board, one item after another,
   timed to narration cues. A camera (view rectangle) follows the area being drawn. */
export type Word = { text: string; start: number; end: number };
export type Seg = { id: string; text: string; start: number; end: number; words: Word[] };
export const NAR = narration as unknown as { total: number; segments: Seg[] };
export const BW = 1800, BH = 860;
export const FOLLOW_CAM = false;
export const K = "#23201d", B = "#2456c4", R = "#d23b2e", G = "#1f8a4c";

export type Item =
  | { k: "t"; at: number; dur: number; x: number; y: number; s: string; size: number; c: string; anchor: "start" | "middle" | "end" }
  | { k: "p"; at: number; dur: number; d: string; c: string; w: number; fill?: string; fo?: number; dash?: string };
export type Cam = { at: number; x: number; y: number; w: number };
export type Board = { id: string; items: Item[]; cams: Cam[] };

/* ---------- deterministic wobble so lines look hand-drawn ---------- */
let seed = 7;
const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647 - 0.5; };
const f1 = (v: number) => v.toFixed(1);
export const lineD = (x1: number, y1: number, x2: number, y2: number, wob = 1) => {
  const L = Math.hypot(x2 - x1, y2 - y1), k = Math.min(6, L * 0.03) * wob, nx = -(y2 - y1) / (L || 1), ny = (x2 - x1) / (L || 1), o = rnd() * 2 * k;
  return `M${f1(x1)} ${f1(y1)} Q${f1((x1 + x2) / 2 + nx * o)} ${f1((y1 + y2) / 2 + ny * o)} ${f1(x2)} ${f1(y2)}`;
};
export const headD = (x1: number, y1: number, x2: number, y2: number, h = 16) => {
  const a = Math.atan2(y2 - y1, x2 - x1);
  return ` M${f1(x2 - h * Math.cos(a - 0.45))} ${f1(y2 - h * Math.sin(a - 0.45))} L${f1(x2)} ${f1(y2)} L${f1(x2 - h * Math.cos(a + 0.45))} ${f1(y2 - h * Math.sin(a + 0.45))}`;
};
/** smooth curve through points (Catmull-Rom to cubic) */
export const curveD = (pts: number[][], closed = false) => {
  const p = closed ? [pts[pts.length - 1], ...pts, pts[0], pts[1]] : [pts[0], ...pts, pts[pts.length - 1]];
  let d = `M${f1(p[1][0])} ${f1(p[1][1])}`;
  for (let i = 1; i < p.length - 2; i++) {
    const [a, b, c, e] = [p[i - 1], p[i], p[i + 1], p[i + 2]];
    d += ` C${f1(b[0] + (c[0] - a[0]) / 6)} ${f1(b[1] + (c[1] - a[1]) / 6)} ${f1(c[0] - (e[0] - b[0]) / 6)} ${f1(c[1] - (e[1] - b[1]) / 6)} ${f1(c[0])} ${f1(c[1])}`;
  }
  return d + (closed ? " Z" : "");
};
export const polyD = (pts: number[][], closed = false) => pts.map((p, i) => `${i ? "L" : "M"}${f1(p[0])} ${f1(p[1])}`).join(" ") + (closed ? " Z" : "");
export const circD = (cx: number, cy: number, r: number, ry = r) => {
  const n = 14, pts = Array.from({ length: n }, (_, i) => { const a = -Math.PI / 2 + (i / n) * Math.PI * 2, j = 1 + rnd() * 0.05; return [cx + Math.cos(a) * r * j, cy + Math.sin(a) * ry * j]; });
  return curveD(pts, true);
};
export const rectD = (x: number, y: number, w: number, h: number) => {
  const j = () => rnd() * 4;
  return `M${f1(x + j())} ${f1(y + j())} L${f1(x + w + j())} ${f1(y + j())} L${f1(x + w + j())} ${f1(y + h + j())} L${f1(x + j())} ${f1(y + h + j())} Z`;
};
export const cloudD = (x: number, y: number, s: number) =>
  `M${f1(x - s)} ${f1(y + s * 0.35)} q${f1(-s * 0.45)} ${f1(-s * 0.05)} ${f1(-s * 0.3)} ${f1(-s * 0.42)} q${f1(-s * 0.05)} ${f1(-s * 0.5)} ${f1(s * 0.5)} ${f1(-s * 0.42)} q${f1(s * 0.25)} ${f1(-s * 0.55)} ${f1(s * 0.8)} ${f1(-s * 0.15)} q${f1(s * 0.6)} ${f1(-s * 0.2)} ${f1(s * 0.65)} ${f1(s * 0.4)} q${f1(s * 0.5)} ${f1(s * 0.1)} ${f1(s * 0.3)} ${f1(s * 0.5)} q${f1(-s * 0.1)} ${f1(s * 0.12)} ${f1(-s * 0.3)} ${f1(s * 0.09)} Z`;
export const dropsD = (x: number, y: number, s: number, n = 5) =>
  Array.from({ length: n }, (_, i) => { const dx = x - s * 0.8 + (i * s * 1.6) / (n - 1), dy = y + (i % 2) * s * 0.25; return `M${f1(dx)} ${f1(dy)} l${f1(-s * 0.12)} ${f1(s * 0.4)}`; }).join(" ");
export const sunD = (x: number, y: number, r: number) =>
  circD(x, y, r) + Array.from({ length: 10 }, (_, i) => { const a = (i / 10) * Math.PI * 2; return ` M${f1(x + Math.cos(a) * r * 1.3)} ${f1(y + Math.sin(a) * r * 1.3)} L${f1(x + Math.cos(a) * r * 1.75)} ${f1(y + Math.sin(a) * r * 1.75)}`; }).join("");
export const peaksD = (x: number, y: number, w: number, h: number, n: number) => {
  let d = `M${f1(x)} ${f1(y)}`;
  for (let i = 0; i < n; i++) d += ` L${f1(x + ((i + 0.5) * w) / n)} ${f1(y - h * (0.7 + ((i * 37) % 10) / 30))} L${f1(x + ((i + 1) * w) / n)} ${f1(y)}`;
  return d;
};

/* ---------- simplified India outline (lon, lat), sketched like a teacher would ---------- */
const INDIA: number[][] = [[74.5, 37.0], [78.0, 35.6], [80.2, 35.4], [79.5, 34.0], [78.7, 32.5], [79.5, 31.0], [81.1, 30.2], [80.1, 28.8], [83.3, 27.4], [88.1, 27.9], [88.8, 27.2], [89.8, 26.7], [92.1, 26.9], [92.0, 27.8], [94.5, 29.3], [96.1, 29.4], [97.3, 28.2], [96.2, 27.2], [95.2, 26.0], [94.6, 24.7], [93.3, 24.0], [93.3, 22.2], [92.3, 23.0], [91.3, 23.7], [92.2, 25.1], [89.8, 25.3], [88.8, 26.2], [88.2, 25.6], [88.9, 24.6], [88.6, 23.6], [89.0, 22.0], [87.0, 21.5], [86.4, 20.0], [85.1, 19.4], [84.0, 18.3], [82.3, 16.6], [81.3, 16.3], [80.3, 15.5], [80.1, 13.5], [79.8, 11.5], [79.3, 10.3], [78.9, 9.3], [78.2, 8.9], [77.5, 8.1], [76.6, 8.9], [76.2, 10.0], [75.3, 11.9], [74.8, 13.0], [74.4, 14.6], [73.5, 16.0], [73.0, 18.0], [72.8, 19.2], [72.7, 20.8], [72.9, 21.5], [72.1, 21.2], [71.0, 20.7], [70.2, 21.0], [69.0, 22.3], [70.4, 23.0], [68.8, 23.2], [68.2, 23.7], [70.9, 24.4], [70.1, 25.7], [69.5, 26.8], [70.4, 28.0], [71.9, 27.9], [72.9, 29.0], [73.4, 29.9], [74.5, 31.1], [74.6, 31.9], [75.3, 32.3], [74.4, 32.8], [73.6, 33.8], [73.2, 34.8], [73.0, 36.0]];
export type MapP = { x: number; y: number; s: number };
export const geo = (m: MapP) => (lon: number, lat: number) => [m.x + (lon - 68) * m.s * 0.93, m.y + (37.2 - lat) * m.s];
export const indiaD = (m: MapP) => curveD(INDIA.map(([lo, la]) => geo(m)(lo, la)), true);

/* ---------- builder: items are placed on a timeline; an item never starts before the previous one ends ---------- */
export const makeBoard = (id: string, build: (b: Builder) => void): Board => {
  const seg = NAR.segments.find((s) => s.id === id);
  if (!seg) throw new Error("no segment " + id);
  seed = 7 + id.length * 131 + id.charCodeAt(0);
  const items: Item[] = [], cams: Cam[] = [];
  const req: number[] = [];
  const norm = (w: string) => w.toLowerCase().replace(/[^a-z0-9.]/g, "");
  const q = (w: string, n = 0) => { const m = seg.words.filter((x) => norm(x.text).startsWith(norm(w))); if (!m[n]) throw new Error(`cue ${id}:${w}:${n}`); return m[n].start; };
  const when = (at: number | string | null) => { const r = at === null ? 0 : typeof at === "string" ? q(at) : at; req.push(r); return r; };
  const b: Builder = {
    q, start: seg.start, end: seg.end,
    t: (at, x, y, s, o = {}) => { const a = when(at), size = o.size ?? 34, dur = o.dur ?? Math.max(0.35, s.length * 0.042); items.push({ k: "t", at: a, dur, x, y, s, size, c: o.c ?? K, anchor: o.anchor ?? "start" }); },
    p: (at, d, o = {}) => { const a = when(at), dur = o.dur ?? 0.55; items.push({ k: "p", at: a, dur, d, c: o.c ?? K, w: o.w ?? 4, fill: o.fill, fo: o.fo, dash: o.dash }); },
    ln: (at, x1, y1, x2, y2, o = {}) => b.p(at, lineD(x1, y1, x2, y2), { dur: 0.35, ...o }),
    ar: (at, x1, y1, x2, y2, o = {}) => b.p(at, lineD(x1, y1, x2, y2) + headD(x1, y1, x2, y2, o.head ?? 16), { dur: 0.5, ...o }),
    ul: (at, x, y, w, o = {}) => b.p(at, lineD(x, y, x + w, y + 2, 0.5), { dur: 0.3, w: 5, ...o }),
    box: (at, x, y, w, h, o = {}) => b.p(at, rectD(x, y, w, h), { dur: 0.6, ...o }),
    circ: (at, x, y, r, o = {}) => b.p(at, circD(x, y, r, o.ry ?? r), { dur: 0.45, ...o }),
    num: (at, x, y, n, c = G) => { b.p(at, circD(x, y, 20), { dur: 0.3, c, w: 3.5 }); b.t(null, x, y + 11, String(n), { size: 30, c, anchor: "middle", dur: 0.15 }); },
    cam: (at, x, y, w) => { cams.push({ at: typeof at === "string" ? q(at) : at, x, y, w }); },
    wait: () => undefined,
  };
  build(b);
  // schedule: an item never starts before the previous one ends; if the page runs past the narration, write faster
  const d0 = items.map((it) => it.dur);
  for (let f = 1; f > 0.25; f *= 0.9) {
    let last = seg.start - 0.3;
    items.forEach((it, i) => { it.at = Math.max(last + 0.06 * f, req[i]); it.dur = d0[i] * f; last = it.at + it.dur; });
    if (last <= seg.end + 0.15) break;
  }
  return { id, items, cams: cams.sort((a, c) => a.at - c.at) };
};
type PO = { c?: string; w?: number; dur?: number; fill?: string; fo?: number; dash?: string; head?: number; ry?: number };
type At = number | string | null;
export type Builder = {
  q: (w: string, n?: number) => number; start: number; end: number;
  t: (at: At, x: number, y: number, s: string, o?: { size?: number; c?: string; dur?: number; anchor?: "start" | "middle" | "end" }) => void;
  p: (at: At, d: string, o?: PO) => void;
  ln: (at: At, x1: number, y1: number, x2: number, y2: number, o?: PO) => void;
  ar: (at: At, x1: number, y1: number, x2: number, y2: number, o?: PO) => void;
  ul: (at: At, x: number, y: number, w: number, o?: PO) => void;
  box: (at: At, x: number, y: number, w: number, h: number, o?: PO) => void;
  circ: (at: At, x: number, y: number, r: number, o?: PO) => void;
  num: (at: At, x: number, y: number, n: number | string, c?: string) => void;
  cam: (at: number | string, x: number, y: number, w: number) => void;
  wait: (s: number) => void;
};

/* ---------- measuring (browser only) ---------- */
const wCache = new Map<string, number>(), pCache = new Map<string, SVGPathElement>();
let ctx: CanvasRenderingContext2D | null = null;
const textW = (s: string, size: number) => {
  const key = size + "|" + s; let w = wCache.get(key);
  if (w === undefined) {
    if (typeof document === "undefined") return s.length * size * 0.42;
    ctx = ctx ?? document.createElement("canvas").getContext("2d")!;
    ctx.font = `${size}px "${FONT}"`; w = ctx.measureText(s).width; wCache.set(key, w);
  }
  return w;
};
const pathEl = (d: string) => {
  let el = pCache.get(d);
  if (!el) { el = document.createElementNS("http://www.w3.org/2000/svg", "path"); el.setAttribute("d", d); pCache.set(d, el); }
  return el;
};
const ease = (x: number) => { const t = Math.max(0, Math.min(1, x)); return t * t * (3 - 2 * t); };
const prog = (it: Item, T: number) => Math.max(0, Math.min(1, (T - it.at) / it.dur));
const tipOf = (it: Item, p: number): [number, number] => {
  if (it.k === "t") { const w = textW(it.s, it.size), x0 = it.anchor === "middle" ? it.x - w / 2 : it.anchor === "end" ? it.x - w : it.x; return [x0 + w * p, it.y - it.size * 0.3 + Math.sin(p * it.s.length * 2.2) * it.size * 0.16]; }
  if (typeof document === "undefined") return [0, 0];
  const el = pathEl(it.d), pt = el.getPointAtLength(el.getTotalLength() * p); return [pt.x, pt.y];
};

/* ---------- the marker pen ---------- */
const Pen = ({ x, y, c, s }: { x: number; y: number; c: string; s: number }) => (
  <g transform={`translate(${x} ${y}) scale(${s}) rotate(38)`}>
    <path d="M0 0 L-5 -12 L5 -12 Z" fill={c} />
    <rect x={-7} y={-22} width={14} height={11} rx={2} fill="#3a3a3a" />
    <rect x={-9} y={-92} width={18} height={71} rx={5} fill="#f4f4f2" stroke="#2c2c2c" strokeWidth={2} />
    <rect x={-9} y={-50} width={18} height={14} fill={c} />
    <rect x={-9} y={-104} width={18} height={14} rx={4} fill={c} stroke="#2c2c2c" strokeWidth={2} />
  </g>
);

/* ---------- one board at time T ---------- */
export const BoardView = ({ board, T }: { board: Board; T: number }) => {
  const { items, cams } = board;
  // camera
  let v = { x: 0, y: 0, w: BW };
  // FOLLOW_CAM off: the whole board stays in view for the entire video, so nothing is ever cropped
  if (FOLLOW_CAM) for (const c of cams) { const k = ease((T - c.at) / 1.3); v = { x: v.x + (c.x - v.x) * k, y: v.y + (c.y - v.y) * k, w: v.w + (c.w - v.w) * k }; }
  v.x = Math.max(0, Math.min(BW - v.w, v.x)); v.y = Math.max(0, Math.min(BH - (v.w * BH) / BW, v.y));
  const z = BW / v.w;
  // pen
  let cur = -1; for (let i = 0; i < items.length; i++) if (items[i].at <= T) cur = i;
  let pen: [number, number] | null = null, pc = K;
  if (cur >= 0) {
    const it = items[cur], p = prog(it, T); pen = tipOf(it, p); pc = it.c;
    const nx = items[cur + 1];
    if (p >= 1 && nx) { const k = ease((T - (nx.at - 0.4)) / 0.4), n0 = tipOf(nx, 0); pen = [pen[0] + (n0[0] - pen[0]) * k, pen[1] + (n0[1] - pen[1]) * k]; if (k > 0.5) pc = nx.c; }
  } else if (items[0]) { pen = tipOf(items[0], 0); pc = items[0].c; }
  return (
    <svg width={BW} height={BH} viewBox={`${v.x} ${v.y} ${v.w} ${(v.w * BH) / BW}`} style={{ position: "absolute", inset: 0 }}>
      {items.map((it, i) => {
        if (it.at > T) return null;
        const p = prog(it, T);
        if (it.k === "t") {
          const w = textW(it.s, it.size), x0 = it.anchor === "middle" ? it.x - w / 2 : it.anchor === "end" ? it.x - w : it.x;
          return (<g key={i}>
            {p < 1 && <clipPath id={`c${i}`}><rect x={x0 - 4} y={it.y - it.size * 1.1} width={(w + 8) * p} height={it.size * 1.6} /></clipPath>}
            <text x={x0} y={it.y} fontFamily={FONT} fontSize={it.size} fill={it.c} clipPath={p < 1 ? `url(#c${i})` : undefined}>{it.s}</text>
          </g>);
        }
        return (<g key={i}>
          {it.fill && <path d={it.d} fill={it.fill} opacity={(it.fo ?? 0.25) * ease((T - it.at - it.dur) / 0.4)} stroke="none" />}
          <path d={it.d} fill="none" stroke={it.c} strokeWidth={it.w} strokeLinecap="round" strokeLinejoin="round"
            {...(p < 1 ? { pathLength: 1, strokeDasharray: "1 1", strokeDashoffset: 1 - p } : it.dash ? { strokeDasharray: it.dash } : {})} />
        </g>);
      })}
      {pen && <Pen x={pen[0]} y={pen[1]} c={pc} s={1.15 / z + 0.25} />}
    </svg>
  );
};
