import React from "react";
import mapdata from "./mapdata.json";
import { C, Label, Peaks } from "./kit";

/* Mercator projection calibrated to India's official outline (see scripts/monsoon_mapdata.mjs) */
const MD = mapdata as unknown as { K: number; LON0: number; LAT0: number; india: { id: string; d: string }[]; land: string[] };
const M = (p: number) => Math.log(Math.tan(Math.PI / 4 + (p * Math.PI) / 360));
export const X = (lon: number) => MD.K * ((lon - MD.LON0) * Math.PI) / 180;
export const Y = (lat: number) => MD.K * (M(MD.LAT0) - M(lat));
export const P = (lon: number, lat: number) => [X(lon), Y(lat)];
export const PP = (pts: number[][]) => pts.map(([lo, la]) => P(lo, la));

export type View = { lon0: number; lon1: number; lat0: number; lat1: number };
/** A map placed at (left, top, w, h) in card px; children get the projection and `u` (svg units per screen px). */
export const MapView = ({ left, top, w, h, view, children, landO = 1, indiaFill = C.india, seaColor = C.sea }:
  { left: number; top: number; w: number; h: number; view: View; children?: (u: number) => React.ReactNode; landO?: number; indiaFill?: string; seaColor?: string }) => {
  const x0 = X(view.lon0), x1 = X(view.lon1), y0 = Y(view.lat1), y1 = Y(view.lat0);
  const vw = x1 - x0, vh = y1 - y0, u = Math.max(vw / w, vh / h);
  return (
    <svg width={w} height={h} viewBox={`${x0} ${y0} ${vw} ${vh}`} preserveAspectRatio="xMidYMid meet" style={{ position: "absolute", left, top, overflow: "hidden", borderRadius: 14 }}>
      <rect x={x0 - 50} y={y0 - 50} width={vw + 100} height={vh + 100} fill={seaColor} />
      {/* sea texture: faint wave strokes */}
      {Array.from({ length: 26 }, (_, i) => {
        const yy = y0 + (vh * (i + 0.5)) / 26, xx = x0 + ((i * 97) % 9) * vw / 9;
        return <path key={i} d={`M${xx} ${yy} q ${12 * u} ${-7 * u} ${24 * u} 0 t ${24 * u} 0`} fill="none" stroke="#b8d2d6" strokeWidth={3 * u} opacity={0.8} />;
      })}
      <g opacity={landO}>{MD.land.map((d, i) => <path key={i} d={d} fill={C.land} stroke="#b9a988" strokeWidth={2.2 * u} strokeLinejoin="round" />)}</g>
      {/* India: inked outline drawn first, fills on top hide the internal (state) edges */}
      <g filter="url(#wob)">
        {MD.india.map((p) => <path key={"s" + p.id} d={p.d} fill="none" stroke={C.ink} strokeWidth={7 * u} strokeLinejoin="round" />)}
        {MD.india.map((p) => <path key={"f" + p.id} d={p.d} fill={indiaFill} stroke={indiaFill} strokeWidth={0.6 * u} />)}
      </g>
      {children && children(u)}
    </svg>
  );
};

/* India's outline as a clip (for washes such as monsoon cover) */
export const IndiaClip = ({ id }: { id: string }) => (
  <clipPath id={id}>{MD.india.map((p) => <path key={p.id} d={p.d} />)}</clipPath>
);

/* the Western Ghats and the Himalaya as rows of little peaks */
export const GHATS = [[74.0, 20.8], [73.7, 19.6], [73.7, 18.4], [73.9, 17.2], [74.1, 16.0], [74.5, 14.8], [75.0, 13.6], [75.5, 12.4], [76.1, 11.3], [76.8, 10.2], [77.2, 9.0]];
export const HIMALAYA = [[74.5, 34.4], [76.0, 33.4], [77.6, 32.4], [79.0, 31.0], [80.5, 29.9], [82.2, 29.0], [84.0, 28.3], [85.8, 27.9], [87.6, 27.7], [89.4, 27.9], [91.2, 27.9], [93.0, 28.1], [94.8, 28.3]];
export const Ranges = ({ u, ghats = 1, himalaya = 1 }: { u: number; ghats?: number; himalaya?: number }) => (
  <>
    {ghats > 0 && <Peaks pts={PP(GHATS)} size={16} u={u} color="#9fb37a" o={ghats} />}
    {himalaya > 0 && <Peaks pts={PP(HIMALAYA)} size={22} u={u} color="#c9b48d" o={himalaya} />}
  </>
);
export const SeaLabels = ({ u, o = 1 }: { u: number; o?: number }) => (
  <g opacity={o}>
    <Label x={X(64.5)} y={Y(15.5)} size={26 * u} color="#4d7d86" sc>Arabian Sea</Label>
    <Label x={X(88.5)} y={Y(15.0)} size={26 * u} color="#4d7d86" sc>Bay of Bengal</Label>
  </g>
);
