import React from "react";
import { AbsoluteFill } from "remotion";
import { Arrow, C, Cloud, Defs, FONT, FONT_SC, Host } from "../monsoon/kit";
import { MapView, P, PP, X, Y } from "../monsoon/map";
import { Globe, SunIcon } from "../seasons2/parts";

/* YouTube thumbnails, designed at 1920x1080 and saved at 1280x720.
   Rules: max 3-4 words, huge high-contrast type, one focal image, the host as a "face",
   nothing important in the bottom-right corner (YouTube's duration badge sits there). */
const Big = ({ children, size, color, x, y, rot = 0, stroke = 12 }: { children: React.ReactNode; size: number; color: string; x: number; y: number; rot?: number; stroke?: number }) => (
  <div style={{ position: "absolute", left: x, top: y, fontFamily: FONT, fontSize: size, lineHeight: 0.92, color, transform: `rotate(${rot}deg)`,
    WebkitTextStroke: `${stroke}px ${C.ink}`, paintOrder: "stroke fill", textShadow: `0 10px 0 rgba(0,0,0,0.35)`, letterSpacing: 2, whiteSpace: "nowrap" }}>{children}</div>
);
const Chip = ({ children, bg, x, y, size = 58, rot = 0 }: { children: React.ReactNode; bg: string; x: number; y: number; size?: number; rot?: number }) => (
  <div style={{ position: "absolute", left: x, top: y, fontFamily: FONT_SC, fontSize: size, lineHeight: 1.05, color: "#fff", background: bg, border: `6px solid ${C.ink}`,
    borderRadius: 22, padding: "4px 26px 8px", transform: `rotate(${rot}deg)`, boxShadow: "0 8px 0 rgba(0,0,0,0.3)", whiteSpace: "nowrap" }}>{children}</div>
);

export const ThumbSeasons = () => {
  const gx = 1390, gy = 590, gr = 330;
  return (
    <AbsoluteFill style={{ background: "radial-gradient(circle at 78% 28%, #3b5f9c 0%, #1d2f55 45%, #0f1a33 100%)" }}>
      <Defs />
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        {/* sunbeams onto the globe */}
        <circle cx={1760} cy={150} r={260} fill="#ffd66b" opacity={0.18} />
        {[-0.5, -0.25, 0, 0.25].map((k, i) => <path key={i} d={`M ${1700 - k * 120} ${200 + k * 160} L ${gx + 120 - k * 200} ${gy - 150 + k * 260}`} stroke="#ffd66b" strokeWidth={14} opacity={0.55} strokeLinecap="round" />)}
        <SunIcon x={1760} y={150} r={110} T={0.4} />
        <Globe cx={gx} cy={gy} r={gr} tilt={23.5} sunAngle={-0.6} meridians={10} spin={8} glowLat={23.5}
          lats={[{ lat: 66.5, color: "#7fb8ff", w: 6, dash: "16 10" }, { lat: 23.5, color: "#ffb340", w: 8, dash: "20 12" }, { lat: 0, color: "#ff5a3c", w: 8 }, { lat: -23.5, color: "#ffb340", w: 8, dash: "20 12" }]} />
        <path d={`M ${gx} ${gy - gr * 1.28} A ${gr * 1.28} ${gr * 1.28} 0 0 1 ${gx + Math.sin(0.41) * gr * 1.28} ${gy - Math.cos(0.41) * gr * 1.28}`} fill="none" stroke="#ffd66b" strokeWidth={9} />
        <line x1={gx} y1={gy - gr * 1.45} x2={gx} y2={gy - gr} stroke="#ffd66b" strokeWidth={5} strokeDasharray="14 10" />
        <text x={gx - 40} y={gy - gr * 1.33} fontFamily={FONT} fontSize={78} fill="#ffd66b" stroke={C.ink} strokeWidth={8} paintOrder="stroke" textAnchor="end">23.5°</text>
      </svg>
      <Chip bg="#c2402b" x={80} y={70} size={52} rot={-2}>UPSC GEOGRAPHY</Chip>
      <Big size={250} color="#ffd23f" x={70} y={190} rot={-3}>WHY</Big>
      <Big size={210} color="#ffffff" x={70} y={420} rot={-3}>SEASONS?</Big>
      <Chip bg="#2f6d9a" x={90} y={680} size={50} rot={-2}>Solstice · Tropics · Climate</Chip>
      <Host t={0.4} T={0.4} mood="wow" x={210} y={900} />
    </AbsoluteFill>
  );
};

export const ThumbMonsoon = () => (
  <AbsoluteFill style={{ background: "radial-gradient(circle at 75% 40%, #2a86a8 0%, #135570 50%, #0a2c3d 100%)" }}>
    <Defs />
    <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
      {Array.from({ length: 70 }, (_, i) => { const x = (i * 137) % 1920, y = (i * 263) % 1080; return <line key={i} x1={x} y1={y} x2={x - 18} y2={y + 60} stroke="#bfe3ff" strokeWidth={4} opacity={0.25} strokeLinecap="round" />; })}
    </svg>
    <div style={{ position: "absolute", left: 1060, top: 150, width: 760, height: 720, borderRadius: 28, border: `8px solid ${C.ink}`, overflow: "hidden", boxShadow: "0 16px 0 rgba(0,0,0,0.35)" }}>
      <MapView left={-6} top={4} w={740} h={700} view={{ lon0: 63, lon1: 99, lat0: 5, lat1: 37.6 }}>{(u) => (
        <>
          {[[[57, 6], [64, 10], [70.5, 14.5], [73.5, 17]], [[58, 3], [66, 6.5], [72, 10.5], [75, 12.5]], [[86, 4], [88, 11], [89.5, 18], [90.5, 24]]].map((pts, i) =>
            <Arrow key={i} pts={PP(pts)} k={1} color={C.rain} u={u} w={16} head={34} />)}
          {[[73.6, 17.5], [76, 12], [90.5, 25.5], [84, 25.5], [79, 23]].map(([lo, la], i) => <Cloud key={i} x={X(lo)} y={Y(la)} s={58} u={u} T={i * 1.3} rain={1} dark={i < 3} />)}
          <circle cx={P(76.95, 8.5)[0]} cy={P(76.95, 8.5)[1]} r={12 * u} fill={C.red} stroke={C.ink} strokeWidth={4 * u} />
        </>)}
      </MapView>
    </div>
    <Chip bg="#c2402b" x={80} y={70} size={52} rot={-2}>UPSC GEOGRAPHY</Chip>
    <Big size={150} color="#ffffff" x={74} y={185} rot={-3}>INDIAN</Big>
    <Big size={235} color="#ffd23f" x={60} y={330} rot={-3}>MONSOON</Big>
    <Chip bg="#2f6d9a" x={90} y={630} size={66} rot={-4}>WHAT?</Chip>
    <Chip bg="#b8432f" x={390} y={620} size={66} rot={2}>WHY?</Chip>
    <Chip bg="#2f7d3a" x={640} y={632} size={66} rot={-3}>HOW?</Chip>
    <Host t={0.4} T={0.4} mood="umbrella" x={190} y={900} />
  </AbsoluteFill>
);
