import React from "react";
import { Arrow, C, Card, CARD, Cloud, FONT, FONT_SC, Host, Label, cue, fmtDate, interp, lerp, segOf, sm } from "./kit";
const mixHex = (a: string, b: string, k: number) => "#" + [1, 3, 5].map((i) => Math.round(parseInt(a.slice(i, i + 2), 16) * (1 - k) + parseInt(b.slice(i, i + 2), 16) * k).toString(16).padStart(2, "0")).join("");
import { IndiaClip, MapView, P, PP, Ranges, SeaLabels, View, X, Y } from "./map";

type SP = { T: number };
const INDIA: View = { lon0: 63, lon1: 99, lat0: 5, lat1: 37.6 };
const MAPBOX = { left: 34, top: 92, w: 740, h: 700 };
const PANEL = { left: 800, top: 120, w: 560 };

/* text lines in the card's side panel */
const Line = ({ T, at, y, children, size = 40, color = C.ink, x = PANEL.left, sc = false, w = PANEL.w }:
  { T: number; at: number; y: number; children: React.ReactNode; size?: number; color?: string; x?: number; sc?: boolean; w?: number }) => {
  const o = sm(at - 0.15, at + 0.35, T);
  return <div style={{ position: "absolute", left: x, top: y, width: Math.min(w, CARD.w - x - 40), fontFamily: sc ? FONT_SC : FONT, fontSize: size, lineHeight: 1.15, color, opacity: o, transform: `translateY(${(1 - o) * 14}px)` }}>{children}</div>;
};
const Big = ({ T, at, y, children, color = C.red, size = 120, x = PANEL.left }: { T: number; at: number; y: number; children: React.ReactNode; color?: string; size?: number; x?: number }) => {
  const o = sm(at - 0.1, at + 0.3, T), s = 0.7 + 0.3 * o + 0.08 * Math.sin(Math.min(1, Math.max(0, (T - at) / 0.4)) * Math.PI);
  return <div style={{ position: "absolute", left: x, top: y, fontFamily: FONT, fontSize: size, color, opacity: o, transform: `scale(${s})`, transformOrigin: "0% 50%", lineHeight: 1 }}>{children}</div>;
};
const hostMood = (T: number, a: number, b: number) => T > a && T < b;

/* =========================================================== intro */
export const Intro = ({ T }: SP) => {
  const s = segOf("intro"), t = T - s.start;
  return (
    <>
      <Host t={t} T={T} mood="umbrella" />
      <Card title="The Indian Monsoon" t={T} appear={s.start - 0.2}>
        <MapView {...MAPBOX} view={INDIA}>{(u) => (
          <>
            <Ranges u={u} ghats={0.9} himalaya={0.9} /><SeaLabels u={u} />
            {[[70, 18], [77, 24], [86, 23], [80, 13]].map(([lo, la], i) => <Cloud key={i} x={X(lo + Math.sin(T * 0.4 + i) * 1.2)} y={Y(la)} s={46} u={u} T={T + i} rain={0.9} />)}
          </>)}
        </MapView>
        <Line T={T} at={cue("intro", "two")} y={PANEL.top + 60} size={52}>1 · Two phases</Line>
        <Line T={T} at={cue("intro", "drives")} y={PANEL.top + 170} size={52}>2 · Core drivers</Line>
        <Line T={T} at={cue("intro", "changing")} y={PANEL.top + 280} size={52}>3 · Recent shifts</Line>
      </Card>
    </>
  );
};

/* =========================================================== part cards */
export const PartCard = ({ T, id, n, title, icon }: SP & { id: string; n: number; title: string; icon: React.ReactNode }) => {
  const s = segOf(id);
  return (
    <>
      <Host t={T - s.start} T={T} mood="wave" />
      <Card title={`Part ${n}`} t={T} appear={s.start - 0.3}>
        <div style={{ position: "absolute", left: 0, right: 0, top: 260, textAlign: "center", fontFamily: FONT, fontSize: 110, color: C.ink }}>{title}</div>
        <div style={{ position: "absolute", left: 0, right: 0, top: 440, display: "flex", justifyContent: "center" }}>{icon}</div>
      </Card>
    </>
  );
};

/* =========================================================== 1a southwest monsoon: onset sweep */
// IMD normal onset dates (revised 2020); front position as "effective latitude" lat - 0.35 (lon - 77)
const ONSET = [{ name: "Kerala", lon: 76.95, lat: 8.5, doy: 151, lab: "1 Jun" }, { name: "Kolkata", lon: 88.36, lat: 22.57, doy: 160, lab: "10 Jun" },
  { name: "Mumbai", lon: 72.88, lat: 19.08, doy: 161, lab: "11 Jun" }, { name: "Delhi", lon: 77.21, lat: 28.61, doy: 177, lab: "27 Jun" }];
const frontLat = (doy: number) => interp(doy, [146, 151, 160, 161, 177, 188], [6, 9.5, 18.6, 20.4, 28.6, 38.5]);
export const SouthWest = ({ T }: SP) => {
  const s = segOf("sw"), a = cue("sw", "reach"), b = cue("sw", "eighth") + 0.6;
  const doy = interp(T, [a - 0.6, b], [146, 188]), E = frontLat(doy);
  const front = (lo: number) => [lo, E + 0.35 * (lo - 77)];
  return (
    <>
      <Host t={T - s.start} T={T} mood={T > b ? "wow" : "point"} />
      <Card title="Southwest monsoon · June to September" t={T} appear={s.start - 0.3}>
        <MapView {...MAPBOX} view={INDIA}>{(u) => (
          <>
            <defs><IndiaClip id="clipSW" /></defs>
            <g clipPath="url(#clipSW)">
              <path d={"M" + PP([front(55), front(105), [105, -5], [55, -5]]).map((p) => p.join(" ")).join("L") + "Z"} fill={C.greenLight} opacity={0.85} />
            </g>
            {E > 7 && E < 36 && <g clipPath="url(#clipSW)"><path d={"M" + PP([front(60), front(100)]).map((p) => p.join(" ")).join("L")} stroke={C.rain} strokeWidth={7 * u} strokeDasharray={`${16 * u} ${10 * u}`} fill="none" /></g>}
            <Ranges u={u} ghats={0.8} himalaya={0.8} /><SeaLabels u={u} />
            {[0, 1, 2].map((i) => <Arrow key={i} pts={PP([[60 + i * 3, 0 + i * 1.2], [68 + i * 2, 5 + i], [74.5 + i * 1.5, 9 + i * 0.6]])} k={sm(cue("sw", "moist") + i * 0.2, cue("sw", "kerala"), T)} color={C.rain} u={u} w={10} />)}
            {ONSET.map((c) => { const on = doy >= c.doy; const [x, y] = P(c.lon, c.lat); return (
              <g key={c.name} opacity={on ? 1 : 0.0}>
                <circle cx={x} cy={y} r={9 * u} fill={C.red} stroke={C.ink} strokeWidth={3 * u} />
                <Label x={x + 14 * u} y={y - 10 * u} size={30 * u} anchor="start">{`${c.name} · ${c.lab}`}</Label>
              </g>); })}
          </>)}
        </MapView>
        <Line T={T} at={a} y={PANEL.top + 10} size={36} color={C.soft} sc>Monsoon reaches</Line>
        <div style={{ position: "absolute", left: PANEL.left, top: PANEL.top + 60, fontFamily: FONT, fontSize: 150, color: doy >= 188 ? C.red : C.ink, opacity: sm(a - 0.5, a, T), lineHeight: 1 }}>{fmtDate(doy)}</div>
        <Line T={T} at={cue("sw", "whole")} y={PANEL.top + 270} size={40}>Whole country covered by about 8 July</Line>
        <Line T={T} at={a + 0.4} y={PANEL.top + 420} size={30} color={C.soft}>IMD normal onset dates</Line>
      </Card>
    </>
  );
};

/* =========================================================== 1b share of rain */
export const Share = ({ T }: SP) => {
  const s = segOf("share"), k = sm(cue("share", "nearly") - 0.3, cue("share", "rainfall") + 0.3, T), pct = Math.round(75 * k);
  const R = 230, cx = 360, cy = 450, ang = (p: number) => -Math.PI / 2 + 2 * Math.PI * p;
  const arc = (p: number) => { const a = ang(p); return `M ${cx} ${cy} L ${cx} ${cy - R} A ${R} ${R} 0 ${p > 0.5 ? 1 : 0} 1 ${cx + R * Math.cos(a)} ${cy + R * Math.sin(a)} Z`; };
  const months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"];
  return (
    <>
      <Host t={T - s.start} T={T} mood={k > 0.9 ? "wow" : "idle"} />
      <Card title="Share of India's annual rainfall" t={T} appear={s.start - 0.3}>
        <svg width={CARD.w} height={CARD.h} style={{ position: "absolute", inset: 0 }}>
          <g filter="url(#wob)">
            <circle cx={cx} cy={cy} r={R} fill="#efe6d2" stroke={C.ink} strokeWidth={5} />
            {k > 0.01 && <path d={arc(0.75 * k)} fill={C.rain} stroke={C.ink} strokeWidth={5} strokeLinejoin="round" />}
          </g>
          {months.map((m, i) => { const on = i >= 5 && i <= 8; return (
            <g key={i} filter="url(#wob)">
              <rect x={720 + i * 52} y={560} width={44} height={60} rx={8} fill={on ? C.rain : C.card} stroke={C.ink} strokeWidth={3.5} opacity={on ? sm(s.start, s.start + 0.6, T) * 0.9 + 0.1 : 1} />
              <text x={742 + i * 52} y={602} fontFamily={FONT} fontSize={30} textAnchor="middle" fill={on ? "#fff" : C.ink}>{m}</text>
            </g>); })}
          <text x={1032} y={668} fontFamily={FONT} fontSize={32} textAnchor="middle" fill={C.soft}>June to September</text>
        </svg>
        <div style={{ position: "absolute", left: 720, top: 210, fontFamily: FONT, fontSize: 190, color: C.red, lineHeight: 1 }}>{`≈${pct}%`}</div>
        <Line T={T} at={s.start + 0.3} x={720} y={430} size={40}>of the year's rain falls in one season</Line>
      </Card>
    </>
  );
};

/* =========================================================== 1c Arabian Sea branch */
export const Arabian = ({ T }: SP) => {
  const s = segOf("arabian"), a = cue("arabian", "arabian"), g = cue("arabian", "western"), d = cue("arabian", "deccan");
  return (
    <>
      <Host t={T - s.start} T={T} mood="umbrella" />
      <Card title="Two branches · the Arabian Sea branch" t={T} appear={s.start - 0.3}>
        <MapView {...MAPBOX} view={INDIA}>{(u) => (
          <>
            <defs><IndiaClip id="clipAR" /></defs>
            <g clipPath="url(#clipAR)" opacity={sm(d - 0.2, d + 0.6, T)}>
              <path d={"M" + PP([[75.3, 21], [79.5, 21], [80.5, 14], [76.6, 12.4], [75.4, 14.5]]).map((p) => p.join(" ")).join("L") + "Z"} fill="#d8b98a" opacity={0.75} />
              {Array.from({ length: 14 }, (_, i) => { const [x, y] = P(75.6 + (i % 7) * 0.65, 14.2 + Math.floor(i / 7) * 3.2); return <path key={i} d={`M${x} ${y} l ${30 * u} ${-30 * u}`} stroke="#a7834f" strokeWidth={4 * u} />; })}
            </g>
            <Ranges u={u} ghats={1} himalaya={0.6} /><SeaLabels u={u} />
            {[[[58, 7], [66, 10.5], [72.6, 13.6]], [[57, 11], [65, 14.5], [71.8, 17.6]], [[57, 15], [64, 18.5], [70.5, 21.2], [73.5, 25.5]]].map((pts, i) =>
              <Arrow key={i} pts={PP(pts)} k={sm(a + i * 0.25, a + 1.6 + i * 0.25, T)} color={C.rain} u={u} w={11} />)}
            {[[74.4, 18.6], [74.9, 15.6], [75.6, 12.6], [76.5, 10.4]].map(([lo, la], i) =>
              <Cloud key={i} x={X(lo)} y={Y(la) - 20 * u} s={40} u={u} T={T + i} rain={sm(g, g + 0.6, T)} dark o={sm(g - 0.3 + i * 0.1, g + 0.3 + i * 0.1, T)} />)}
            <g opacity={sm(d, d + 0.5, T)}><Label x={X(79.2)} y={Y(17.6)} size={32 * u} color="#7a5a2e" sc>Rain shadow</Label><Label x={X(79.2)} y={Y(16.5)} size={26 * u} color="#7a5a2e">Deccan Plateau</Label></g>
          </>)}
        </MapView>
        <Line T={T} at={g} y={PANEL.top + 30} size={44} color={C.rain}>Windward slopes</Line>
        <Line T={T} at={g + 0.2} y={PANEL.top + 86} size={36}>of the Western Ghats get drenched</Line>
        <Line T={T} at={d} y={PANEL.top + 230} size={44} color="#9a6b2f">Leeward Deccan</Line>
        <Line T={T} at={d + 0.2} y={PANEL.top + 286} size={36}>lies in a rain shadow: much drier</Line>
      </Card>
    </>
  );
};

/* =========================================================== 1d Bay of Bengal branch */
export const Bengal = ({ T }: SP) => {
  const s = segOf("bengal"), a = s.start, w = cue("bengal", "west");
  return (
    <>
      <Host t={T - s.start} T={T} mood="umbrella" />
      <Card title="Two branches · the Bay of Bengal branch" t={T} appear={s.start - 0.3}>
        <MapView {...MAPBOX} view={INDIA}>{(u) => (
          <>
            <Ranges u={u} ghats={0.6} himalaya={1} /><SeaLabels u={u} />
            <Arrow pts={PP([[86.5, 6.5], [88.5, 13], [90.3, 19.5], [91.4, 24.6]])} k={sm(a, a + 2.2, T)} color={C.rain} u={u} w={12} />
            <Cloud x={X(91.7)} y={Y(25.6)} s={46} u={u} T={T} rain={sm(a + 1.6, a + 2.2, T)} dark o={sm(a + 1.4, a + 2, T)} />
            <g opacity={sm(a + 2, a + 2.4, T)}><circle cx={X(91.58)} cy={Y(25.3)} r={7 * u} fill={C.red} stroke={C.ink} strokeWidth={3 * u} /><Label x={X(91.58) + 12 * u} y={Y(25.3) + 34 * u} size={26 * u} anchor="start">Mawsynram</Label></g>
            <Arrow pts={PP([[91.2, 26.3], [88.0, 26.6], [84.5, 27.1], [81.0, 28.2], [77.6, 29.8]])} k={sm(w - 0.2, w + 2.2, T)} color={C.rain} u={u} w={12} />
            {[[86.5, 25.6], [82.6, 26.6], [79.2, 28.1]].map(([lo, la], i) => <Cloud key={i} x={X(lo)} y={Y(la) - 6 * u} s={34} u={u} T={T + i} rain={sm(w + 0.6 + i * 0.4, w + 1 + i * 0.4, T)} o={sm(w + 0.4 + i * 0.4, w + 0.8 + i * 0.4, T)} />)}
            <g opacity={sm(cue("bengal", "ganga"), cue("bengal", "ganga") + 0.4, T)}><Label x={X(82.0)} y={Y(24.4)} size={30 * u} sc>Ganga plains</Label></g>
          </>)}
        </MapView>
        <Line T={T} at={a + 0.6} y={PANEL.top + 30} size={44} color={C.rain}>Soaks the northeast</Line>
        <Line T={T} at={a + 1.0} y={PANEL.top + 86} size={36}>Mawsynram, Meghalaya: among the wettest places on Earth</Line>
        <Line T={T} at={w} y={PANEL.top + 250} size={44} color={C.rain}>Turns west</Line>
        <Line T={T} at={w + 0.3} y={PANEL.top + 306} size={36}>guided by the Himalayas, across the Ganga plains</Line>
      </Card>
    </>
  );
};

/* =========================================================== 1e NE / retreating monsoon */
export const NorthEast = ({ T }: SP) => {
  const s = segOf("ne"), r = cue("ne", "reverse");
  const arrows = [[[93, 29], [88, 26.5], [82, 23.5], [76.5, 20.5]], [[89, 31.5], [83, 29], [77, 26.5], [71.5, 24]], [[95, 22], [91, 18.5], [86.5, 14.5], [82, 11.5]]];
  return (
    <>
      <Host t={T - s.start} T={T} mood="think" />
      <Card title="Northeast (retreating) monsoon · October to December" t={T} appear={s.start - 0.3}>
        <MapView {...MAPBOX} view={INDIA}>{(u) => (
          <>
            <Ranges u={u} ghats={0.6} himalaya={0.9} /><SeaLabels u={u} />
            {arrows.map((pts, i) => <Arrow key={i} pts={PP(pts)} k={sm(r + i * 0.3, r + 1.8 + i * 0.3, T)} color={i === 2 ? C.rain : "#c9a46a"} u={u} w={11} />)}
          </>)}
        </MapView>
        <Line T={T} at={s.start + 0.6} y={PANEL.top + 20} size={44}>Winds reverse</Line>
        <Line T={T} at={cue("ne", "land")} y={PANEL.top + 90} size={60} color="#9a6b2f">Land → Sea</Line>
        <Line T={T} at={cue("ne", "land") + 0.4} y={PANEL.top + 180} size={36}>cool, dry winds blow from the northeast</Line>
      </Card>
    </>
  );
};
export const TamilNadu = ({ T }: SP) => {
  const s = segOf("tn"), c = cue("tn", "crossing"), h = cue("tn", "half");
  return (
    <>
      <Host t={T - s.start} T={T} mood={T > h ? "umbrella" : "idle"} />
      <Card title="Northeast monsoon · rain for Tamil Nadu" t={T} appear={s.start - 0.3}>
        <MapView {...MAPBOX} view={INDIA}>{(u) => (
          <>
            <Ranges u={u} ghats={0.6} himalaya={0.6} /><SeaLabels u={u} />
            <Arrow pts={PP([[95, 22], [91, 18.5], [86.5, 14.5], [81.4, 11.6]])} k={sm(s.start, c + 1.2, T)} color={C.rain} u={u} w={12} />
            {[[79.6, 12.6], [79.2, 10.3]].map(([lo, la], i) => <Cloud key={i} x={X(lo)} y={Y(la)} s={40} u={u} T={T + i} rain={sm(c + 1, c + 1.5, T)} dark o={sm(c + 0.8, c + 1.2, T)} />)}
            <g opacity={sm(c + 1, c + 1.4, T)}><circle cx={X(80.27)} cy={Y(13.08)} r={7 * u} fill={C.red} stroke={C.ink} strokeWidth={3 * u} /><Label x={X(80.27) + 14 * u} y={Y(13.08) - 8 * u} size={28 * u} anchor="start">Chennai</Label>
              <Label x={X(80.9)} y={Y(9.6)} size={26 * u} anchor="start" sc>Coromandel coast</Label></g>
          </>)}
        </MapView>
        <Line T={T} at={c} y={PANEL.top + 20} size={40}>Picks up moisture over the Bay of Bengal</Line>
        <Line T={T} at={h - 0.6} y={PANEL.top + 170} size={36} color={C.soft} sc>Tamil Nadu's yearly rain from Oct to Dec</Line>
        <Big T={T} at={h} y={PANEL.top + 230}>≈ 50%</Big>
      </Card>
    </>
  );
};

/* =========================================================== 2a differential heating (cross-section) */
export const Heating = ({ T }: SP) => {
  const s = segOf("heat"), l = cue("heat", "land"), lo = cue("heat", "low"), hi = cue("heat", "high"), ru = cue("heat", "rushes");
  const landT = sm(l, l + 2.2, T), seaT = sm(l, l + 2.2, T) * 0.35;
  const flow = (T * 0.6) % 1;
  return (
    <>
      <Host t={T - s.start} T={T} mood="hot" />
      <Card title="Driver 1 · Differential heating" t={T} appear={s.start - 0.3}>
        <svg width={CARD.w} height={CARD.h} style={{ position: "absolute", inset: 0 }}>
          <g filter="url(#wob)">
            <rect x={60} y={560} width={620} height={180} fill="#9fd0e0" stroke={C.ink} strokeWidth={5} />
            <path d="M 680 560 L 1330 560 L 1330 740 L 680 740 Z" fill="#d9b27a" stroke={C.ink} strokeWidth={5} />
            {[0, 1, 2, 3, 4, 5].map((i) => <path key={i} d={`M ${90 + i * 100} ${600 + (i % 2) * 40} q 20 -12 40 0 t 40 0`} fill="none" stroke="#5f9fb3" strokeWidth={4} />)}
            <circle cx={1180} cy={190} r={60} fill={C.sun} stroke={C.ink} strokeWidth={5} />
            {Array.from({ length: 10 }, (_, i) => { const a = (i / 10) * Math.PI * 2; return <line key={i} x1={1180 + Math.cos(a) * 78} y1={190 + Math.sin(a) * 78} x2={1180 + Math.cos(a) * 98} y2={190 + Math.sin(a) * 98} stroke={C.sunDark} strokeWidth={5} strokeLinecap="round" />; })}
          </g>
          <text x={370} y={780} fontFamily={FONT_SC} fontSize={38} textAnchor="middle" fill={C.ink}>Indian Ocean · cooler</text>
          <text x={1005} y={780} fontFamily={FONT_SC} fontSize={38} textAnchor="middle" fill={C.ink}>Land (NW India) · hotter</text>
          {/* thermometers */}
          {[[200, seaT, C.cold], [1180, landT, C.hot]].map(([x, k, col], i) => (
            <g key={i} filter="url(#wob)"><rect x={(x as number) - 16} y={330} width={32} height={190} rx={16} fill="#fff" stroke={C.ink} strokeWidth={4} />
              <rect x={(x as number) - 9} y={330 + 180 - 160 * (k as number) - 10} width={18} height={160 * (k as number) + 10} rx={9} fill={col as string} />
              <circle cx={x as number} cy={530} r={26} fill={col as string} stroke={C.ink} strokeWidth={4} /></g>
          ))}
          {/* pressure letters */}
          <g opacity={sm(lo, lo + 0.4, T)}><text x={930} y={470} fontFamily={FONT} fontSize={130} textAnchor="middle" fill={C.red}>L</text><text x={930} y={515} fontFamily={FONT} fontSize={30} textAnchor="middle" fill={C.red}>Low pressure</text></g>
          <g opacity={sm(hi, hi + 0.4, T)}><text x={400} y={470} fontFamily={FONT} fontSize={130} textAnchor="middle" fill={C.cold}>H</text><text x={400} y={515} fontFamily={FONT} fontSize={30} textAnchor="middle" fill={C.cold}>High pressure</text></g>
        </svg>
        <svg width={CARD.w} height={CARD.h} style={{ position: "absolute", inset: 0 }}>
          <Arrow pts={[[300, 545], [520, 540], [760, 540], [930, 545]]} k={sm(ru - 0.2, ru + 0.9, T)} color={C.rain} w={14} head={34} />
          <Arrow pts={[[1130, 520], [1135, 400], [1125, 270]]} k={sm(ru + 0.3, ru + 1.1, T)} color="#e9a07a" w={9} head={26} o={0.9} />
          <Arrow pts={[[1090, 230], [760, 200], [470, 205], [400, 240]]} k={sm(ru + 0.6, ru + 1.5, T)} color="#e9a07a" w={7} head={22} dash="16 12" o={0.85} />
          <Arrow pts={[[400, 250], [395, 330], [400, 380]]} k={sm(ru + 1.0, ru + 1.7, T)} color={C.rainLight} w={7} head={22} o={0.85} />
          {T > ru + 1 && [0, 1, 2].map((i) => { const p = (flow + i / 3) % 1; return <circle key={i} cx={320 + p * 600} cy={540} r={7} fill="#fff" stroke={C.ink} strokeWidth={2} />; })}
        </svg>
        <div style={{ position: "absolute", left: 0, right: 0, top: 96, textAlign: "center", fontFamily: FONT, fontSize: 40, color: C.ink, opacity: sm(ru, ru + 0.4, T) }}>Moist air rushes from sea to land</div>
      </Card>
    </>
  );
};

/* =========================================================== 2b Coriolis */
const WIDE: View = { lon0: 52, lon1: 102, lat0: -20, lat1: 32 };
const WIDEBOX = { left: 34, top: 92, w: 900, h: 700 };
export const Coriolis = ({ T }: SP) => {
  const s = segOf("coriolis"), tr = cue("coriolis", "southeast"), cr = cue("coriolis", "cross"), df = cue("coriolis", "deflected"), sw = cue("coriolis", "southwest");
  return (
    <>
      <Host t={T - s.start} T={T} mood="point" />
      <Card title="Driver 2 · The Coriolis force" t={T} appear={s.start - 0.3}>
        <MapView {...WIDEBOX} view={WIDE} landO={0.9}>{(u) => (
          <>
            <path d={`M${X(52)} ${Y(0)} L${X(102)} ${Y(0)}`} stroke={C.ink} strokeWidth={4 * u} strokeDasharray={`${18 * u} ${12 * u}`} />
            <Label x={X(53.5)} y={Y(0) - 12 * u} size={30 * u} anchor="start" sc>Equator</Label>
            <Label x={X(80)} y={Y(-16)} size={30 * u} sc>Southern Hemisphere</Label>
            {[0, 1].map((i) => <Arrow key={i} pts={PP([[96 - i * 6, -15 + i * 2], [86 - i * 6, -8 + i * 2], [77 - i * 6, -2.5 + i * 2], [71 - i * 6, 0.5 + i * 2]])} k={sm(tr + i * 0.3, cr + 0.6 + i * 0.3, T)} color="#7fb4e4" u={u} w={11} />)}
            {[0, 1].map((i) => <Arrow key={"n" + i} pts={PP([[71 - i * 6, 0.5 + i * 2], [68.6 - i * 6, 4 + i * 2], [70 - i * 5, 8.5 + i * 2], [75.3 - i * 4, 12 + i * 1.8]])} k={sm(df + i * 0.3, sw + 0.8 + i * 0.3, T)} color={C.rain} u={u} w={11} />)}
            <g opacity={sm(tr, tr + 0.4, T)}><Label x={X(91)} y={Y(-10.5)} size={32 * u} color="#3d6ea5" sc>SE trades</Label></g>
            <g opacity={sm(sw, sw + 0.4, T)}><Label x={X(62)} y={Y(13.5)} size={32 * u} color={C.rain} sc>SW monsoon</Label></g>
          </>)}
        </MapView>
        <Line T={T} at={cr} x={960} y={PANEL.top + 30} w={400} size={36}>Crossing the equator...</Line>
        <Line T={T} at={df} x={960} y={PANEL.top + 110} w={400} size={36} color={C.red}>deflected to the right</Line>
        <Line T={T} at={df + 0.4} x={960} y={PANEL.top + 190} w={400} size={34}>(Earth's spin bends winds rightward in the Northern Hemisphere)</Line>
        <Line T={T} at={sw} x={960} y={PANEL.top + 360} w={400} size={36} color={C.rain}>SE trades → SW monsoon</Line>
      </Card>
    </>
  );
};

/* =========================================================== 2c ITCZ */
const ITCZ_VIEW: View = { lon0: 55, lon1: 100, lat0: -14, lat1: 36 };
const JAN = [[55, -6], [65, -7], [75, -8], [85, -9], [95, -8], [100, -8]];
const JUL = [[55, 19], [62, 22], [70, 26.5], [76, 27.5], [82, 25], [88, 22], [95, 21], [100, 20.5]];
export const Itcz = ({ T }: SP) => {
  const s = segOf("itcz"), a = cue("itcz", "july") - 0.3, b = cue("itcz", "north") + 1.2, tr = cue("itcz", "trough");
  const k = sm(a, b, T), line = JAN.map((p, i) => [lerp(p[0], JUL[Math.min(i, JUL.length - 1)][0], 0), 0]).length ? null : null;
  const pts = JUL.map((q, i) => { const p = JAN[Math.min(i, JAN.length - 1)]; return [q[0], lerp(p[1] + (i >= JAN.length ? 0 : 0), q[1], k)]; });
  const month = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL"][Math.min(6, Math.floor(k * 6.999))];
  void line;
  return (
    <>
      <Host t={T - s.start} T={T} mood="point" />
      <Card title="Driver 3 · The shifting ITCZ" t={T} appear={s.start - 0.3}>
        <MapView {...WIDEBOX} view={ITCZ_VIEW}>{(u) => (
          <>
            <path d={`M${X(55)} ${Y(0)} L${X(100)} ${Y(0)}`} stroke={C.ink} strokeWidth={3 * u} strokeDasharray={`${14 * u} ${10 * u}`} opacity={0.6} />
            <Label x={X(56)} y={Y(0) - 10 * u} size={26 * u} anchor="start" color={C.soft} sc>Equator</Label>
            <Ranges u={u} ghats={0.5} himalaya={0.8} />
            <path d={"M" + PP(pts).map((p) => p.join(" ")).join("L")} fill="none" stroke={C.red} strokeWidth={9 * u} strokeDasharray={`${22 * u} ${12 * u}`} strokeLinecap="round" filter="url(#wob)" />
            <g opacity={sm(s.start + 0.6, s.start + 1, T)}><Label x={X(66)} y={Y(pts[2][1]) - 22 * u} size={32 * u} color={C.red} sc>ITCZ</Label></g>
            <g opacity={sm(tr, tr + 0.4, T)}><Label x={X(80)} y={Y(23.5)} size={30 * u} color={C.red}>Monsoon trough</Label></g>
          </>)}
        </MapView>
        <Line T={T} at={s.start + 0.8} x={960} y={PANEL.top + 10} w={400} size={34} color={C.soft} sc>Inter-Tropical Convergence Zone</Line>
        <div style={{ position: "absolute", left: 960, top: PANEL.top + 80, fontFamily: FONT, fontSize: 140, color: k > 0.99 ? C.red : C.ink, opacity: sm(a - 0.5, a, T), lineHeight: 1 }}>{month}</div>
        <Line T={T} at={cue("itcz", "north")} x={960} y={PANEL.top + 270} w={400} size={36}>moves north over the Ganga plains</Line>
        <Line T={T} at={tr} x={960} y={PANEL.top + 380} w={400} size={36}>Low pressure here pulls the monsoon winds in</Line>
      </Card>
    </>
  );
};

/* =========================================================== 2d jet streams + Tibet */
const JET_VIEW: View = { lon0: 55, lon1: 105, lat0: 4, lat1: 45 };
export const Jets = ({ T }: SP) => {
  const s = segOf("jet"), he = cue("jet", "heated"), pu = cue("jet", "push"), ea = cue("jet", "easterly"), bu = cue("jet", "burst");
  const k = sm(pu, pu + 2.2, T);
  const west = [[55, lerp(29, 40, k)], [68, lerp(28.5, 41.5, k)], [82, lerp(27.8, 41.5, k)], [96, lerp(28.2, 40.5, k)], [104, lerp(29, 40, k)]];
  const tib = [[79, 35.5], [84, 36], [90, 36.2], [96, 34.8], [99, 32], [95, 30], [89, 29.4], [83, 30.2], [79.5, 32.3]];
  return (
    <>
      <Host t={T - s.start} T={T} mood={T > bu ? "umbrella" : "hot"} />
      <Card title="Driver 4 · Jet streams and the Tibetan Plateau" t={T} appear={s.start - 0.3}>
        <MapView {...WIDEBOX} view={JET_VIEW}>{(u) => (
          <>
            <path d={"M" + PP(tib).map((p) => p.join(" ")).join("L") + "Z"} fill="#d6b58a" stroke={C.ink} strokeWidth={4 * u} opacity={0.9} filter="url(#wob)" />
            <Label x={X(89)} y={Y(33.4)} size={30 * u} sc>Tibetan Plateau</Label>
            <Ranges u={u} ghats={0.5} himalaya={1} />
            {T > he && [0, 1, 2].map((i) => { const ph = ((T - he) * 0.8 + i / 3) % 1; const [x, y] = P(84 + i * 4, 31.5); return <path key={i} d={`M${x} ${y - ph * 60 * u} q ${8 * u} ${-10 * u} 0 ${-20 * u} q ${-8 * u} ${-10 * u} 0 ${-20 * u}`} fill="none" stroke={C.hot} strokeWidth={5 * u} opacity={1 - ph} />; })}
            <Arrow pts={PP(west)} k={sm(s.start + 1, s.start + 2.5, T)} color="#8a7cc8" u={u} w={12} />
            <Label x={X(62)} y={Y(west[1][1]) - 16 * u} size={28 * u} color="#5d4fa0" anchor="start" sc>Westerly jet</Label>
            <Arrow pts={PP([[102, 15], [92, 14.2], [82, 13.6], [72, 13], [60, 12.4]])} k={sm(ea, ea + 1.6, T)} color={C.sun} u={u} w={12} />
            <g opacity={sm(ea + 0.6, ea + 1, T)}><Label x={X(88)} y={Y(15.6)} size={28 * u} color={C.sunDark} sc>Tropical easterly jet</Label></g>
            {[[74.6, 14.5], [76.2, 10.6]].map(([lo, la], i) => <Cloud key={i} x={X(lo)} y={Y(la)} s={38} u={u} T={T + i} rain={sm(bu, bu + 0.5, T)} dark o={sm(bu - 0.2, bu + 0.3, T)} />)}
          </>)}
        </MapView>
        <Line T={T} at={he} x={960} y={PANEL.top + 10} w={400} size={36}>The plateau heats up in summer...</Line>
        <Line T={T} at={pu + 0.5} x={960} y={PANEL.top + 100} w={400} size={36} color="#5d4fa0">westerly jet shifts north of the Himalayas</Line>
        <Line T={T} at={ea + 0.3} x={960} y={PANEL.top + 230} w={400} size={36} color={C.sunDark}>an easterly jet forms over the peninsula</Line>
        <Big T={T} at={bu} x={960} y={PANEL.top + 380} size={110}>Burst!</Big>
      </Card>
    </>
  );
};

/* =========================================================== 2e oceans */
const Wave = ({ x, y, w, col }: { x: number; y: number; w: number; col: string }) => (
  <g filter="url(#wob)"><path d={`M${x} ${y} q ${w / 8} -26 ${w / 4} 0 t ${w / 4} 0 t ${w / 4} 0 t ${w / 4} 0 L ${x + w} ${y + 110} L ${x} ${y + 110} Z`} fill={col} stroke={C.ink} strokeWidth={5} /></g>
);
export const Oceans = ({ T }: SP) => {
  const s = segOf("ocean"), cards = [
    { at: cue("ocean", "el"), title: "El Niño", sea: "#f0a27a", sub: "warm east Pacific", up: false, eff: "weakens" },
    { at: cue("ocean", "la"), title: "La Niña", sea: "#7fb4e4", sub: "cool east Pacific", up: true, eff: "strengthens" },
    { at: cue("ocean", "positive"), title: "+ Indian Ocean Dipole", sea: "", sub: "warm west, cool east", up: true, eff: "can help" }];
  return (
    <>
      <Host t={T - s.start} T={T} mood="think" />
      <Card title="Driver 5 · The oceans" t={T} appear={s.start - 0.3}>
        {cards.map((c, i) => { const o = sm(c.at - 0.2, c.at + 0.3, T), x = 50 + i * 445; return (
          <div key={i} style={{ position: "absolute", left: x, top: 120, width: 420, height: 640, opacity: o, transform: `translateY(${(1 - o) * 20}px)` }}>
            <svg width={420} height={640} style={{ position: "absolute", inset: 0 }}>
              <g filter="url(#wob)"><rect x={6} y={6} width={408} height={628} rx={18} fill="#fffaf0" stroke={C.ink} strokeWidth={4} /></g>
              {c.sea ? <Wave x={40} y={250} w={340} col={c.sea} /> : <><Wave x={40} y={250} w={165} col="#f0a27a" /><Wave x={215} y={250} w={165} col="#7fb4e4" /></>}
              <Arrow pts={c.up ? [[210, 560], [210, 440]] : [[210, 440], [210, 560]]} k={sm(c.at + 0.3, c.at + 0.9, T)} color={c.up ? C.green : C.red} w={16} head={40} smooth={false} />
            </svg>
            <div style={{ position: "absolute", left: 0, right: 0, top: 40, textAlign: "center", fontFamily: FONT_SC, fontSize: 46, color: C.ink }}>{c.title}</div>
            <div style={{ position: "absolute", left: 0, right: 0, top: 110, textAlign: "center", fontFamily: FONT, fontSize: 32, color: C.soft }}>{c.sub}</div>
            <div style={{ position: "absolute", left: 0, right: 0, top: 380, textAlign: "center", fontFamily: FONT, fontSize: 34, color: C.ink }}>Monsoon</div>
            <div style={{ position: "absolute", left: 0, right: 0, top: 580, textAlign: "center", fontFamily: FONT, fontSize: 40, color: c.up ? C.green : C.red }}>{c.eff}</div>
          </div>); })}
      </Card>
    </>
  );
};

/* =========================================================== 3a long period average */
export const Lpa = ({ T }: SP) => {
  const s = segOf("lpa"), a = cue("lpa", "long"), k = sm(a - 0.2, cue("lpa", "87") + 0.4, T);
  const top = 180, bot = 700, cm = (v: number) => bot - ((bot - top) * v) / 110;
  return (
    <>
      <Host t={T - s.start} T={T} mood="idle" />
      <Card title="Long Period Average (LPA)" t={T} appear={s.start - 0.3}>
        <svg width={CARD.w} height={CARD.h} style={{ position: "absolute", inset: 0 }}>
          <g filter="url(#wob)">
            <rect x={260} y={top} width={200} height={bot - top} rx={14} fill="#fff" stroke={C.ink} strokeWidth={5} />
            <rect x={268} y={cm(87 * k)} width={184} height={bot - cm(87 * k) - 6} rx={8} fill={C.rainLight} />
            <rect x={262} y={cm(90.5)} width={196} height={cm(83.5) - cm(90.5)} fill={C.green} opacity={0.35 * sm(a + 1, a + 1.5, T)} />
          </g>
          {[0, 20, 40, 60, 80, 100].map((v) => <g key={v}><line x1={460} y1={cm(v)} x2={490} y2={cm(v)} stroke={C.ink} strokeWidth={3} /><text x={500} y={cm(v) + 10} fontFamily={FONT} fontSize={28} fill={C.soft}>{v}</text></g>)}
          <line x1={240} y1={cm(87)} x2={720} y2={cm(87)} stroke={C.red} strokeWidth={5} strokeDasharray="16 10" opacity={sm(a, a + 0.4, T)} />
          <text x={360} y={bot + 50} fontFamily={FONT_SC} fontSize={32} textAnchor="middle" fill={C.ink}>Rain gauge (cm)</text>
        </svg>
        <Big T={T} at={cue("lpa", "87")} x={760} y={230} size={150}>87 cm</Big>
        <Line T={T} at={a + 0.3} x={760} y={420} size={36}>June to September average, 1971 to 2020</Line>
        <Line T={T} at={a + 1.2} x={760} y={500} size={34} color={C.green}>"Normal" year: 96 to 104% of LPA</Line>
        <Line T={T} at={cue("lpa", "but")} x={760} y={600} size={40} color={C.red}>...but how the rain falls is changing</Line>
      </Card>
    </>
  );
};

/* =========================================================== 3b fewer moderate days, more extremes (illustrative) */
const EARLIER = "mmlmm.mmlm.mmlmm.mlmmm.mmlmm.m".split("");
const NOW = "...H......l....HH.......l..H..".split("");
export const Extremes = ({ T }: SP) => {
  const s = segOf("extreme"), f = cue("extreme", "fewer"), e = cue("extreme", "extreme"), d = cue("extreme", "dry");
  const row = (days: string[], y: number, at: number, hl: boolean) => days.map((c, i) => {
    const o = sm(at + i * 0.03, at + 0.3 + i * 0.03, T), x = 70 + i * 42;
    const fill = c === "H" ? C.rain : c === "m" ? C.rainLight : c === "l" ? "#cfe3f5" : (hl && T > d ? "#f0d9b0" : "#fbf6ea");
    return (<g key={i} opacity={o}><rect x={x} y={y} width={36} height={36} rx={6} fill={fill} stroke={C.ink} strokeWidth={2.5} />
      {c === "H" && T > e && <Cloud x={x + 18} y={y - 30} s={22} T={T + i} rain={1} dark />}</g>);
  });
  return (
    <>
      <Host t={T - s.start} T={T} mood={T > e ? "umbrella" : "think"} />
      <Card title="Fewer rainy days, more extreme downpours" t={T} appear={s.start - 0.3}>
        <svg width={CARD.w} height={CARD.h} style={{ position: "absolute", inset: 0, overflow: "visible" }}>
          <text x={70} y={210} fontFamily={FONT_SC} fontSize={34} fill={C.soft}>Earlier pattern</text>
          {row(EARLIER, 235, s.start, false)}
          <text x={70} y={450} fontFamily={FONT_SC} fontSize={34} fill={C.soft}>Recent pattern</text>
          {row(NOW, 520, f, true)}
          <g opacity={sm(d, d + 0.4, T)}><path d="M 238 580 l 0 20 l 250 0 l 0 -20" fill="none" stroke={C.red} strokeWidth={4} /><text x={363} y={640} fontFamily={FONT} fontSize={32} textAnchor="middle" fill={C.red}>long dry break</text></g>
          <g opacity={sm(e, e + 0.4, T)}><text x={1330} y={455} fontFamily={FONT} fontSize={34} textAnchor="end" fill={C.rain}>extreme downpours</text></g>
          <text x={1330} y={760} fontFamily={FONT} fontSize={26} textAnchor="end" fill={C.soft}>Illustrative pattern of one monsoon month (each square = a day)</text>
        </svg>
        <div style={{ position: "absolute", left: 70, top: 680, fontFamily: FONT, fontSize: 34, color: C.ink, opacity: sm(e, e + 0.4, T) }}>Strongest rise in extreme rain: central India</div>
      </Card>
    </>
  );
};

/* =========================================================== 3c erratic onset / late withdrawal */
export const Erratic = ({ T }: SP) => {
  const s = segOf("erratic"), w = cue("erratic", "late");
  const months = ["MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV"], x0 = 120, mw = 175, dx = (doy: number) => x0 + ((doy - 121) / 30.5) * mw;
  const jit = Math.sin(T * 5) * 6 * sm(s.start, s.start + 0.6, T), late = sm(w - 0.4, w + 1, T) * 22;
  return (
    <>
      <Host t={T - s.start} T={T} mood="think" />
      <Card title="Onset and withdrawal: more erratic" t={T} appear={s.start - 0.3}>
        <svg width={CARD.w} height={CARD.h} style={{ position: "absolute", inset: 0 }}>
          {months.map((m, i) => <g key={i}><rect x={x0 + i * mw} y={420} width={mw} height={70} fill={i >= 1 && i <= 4 ? "#dcebd2" : "#fbf6ea"} stroke={C.ink} strokeWidth={3} /><text x={x0 + i * mw + mw / 2} y={468} fontFamily={FONT_SC} fontSize={34} textAnchor="middle" fill={C.ink}>{m}</text></g>)}
          <g transform={`translate(${dx(152) + jit - dx(152) + dx(152)} 0)`}>
            <line x1={0} y1={300} x2={0} y2={420} stroke={C.green} strokeWidth={6} />
            <text x={0} y={285} fontFamily={FONT} fontSize={36} textAnchor="middle" fill={C.green}>Onset</text>
          </g>
          <rect x={dx(140)} y={505} width={dx(164) - dx(140)} height={14} rx={7} fill={C.green} opacity={0.4} />
          <g transform={`translate(${dx(260) + late * (mw / 30.5)} 0)`}>
            <line x1={0} y1={300} x2={0} y2={420} stroke={C.red} strokeWidth={6} />
            <text x={0} y={250} fontFamily={FONT} fontSize={36} textAnchor="middle" fill={C.red}>Withdrawal</text>
          </g>
          <line x1={dx(260)} y1={320} x2={dx(260)} y2={420} stroke={C.red} strokeWidth={3} strokeDasharray="8 8" opacity={0.6} />
          <text x={dx(260)} y={560} fontFamily={FONT} fontSize={28} textAnchor="middle" fill={C.soft}>normal start ~17 Sep</text>
          <Arrow pts={[[dx(262), 395], [dx(262) + late * (mw / 30.5) - 16, 395]]} k={late > 1 ? 1 : 0} color={C.red} w={8} head={24} smooth={false} />
        </svg>
        <Line T={T} at={w} x={120} y={640} w={1200} size={42} color={C.red}>Withdrawal is often late, stretching rain into October</Line>
      </Card>
    </>
  );
};

/* =========================================================== 3d Arabian Sea cyclones */
const AS_VIEW: View = { lon0: 52, lon1: 82, lat0: 4, lat1: 28 };
export const Cyclones = ({ T }: SP) => {
  const s = segOf("cyclone"), wm = cue("cyclone", "warming"), cy = cue("cyclone", "cyclones");
  const warm = sm(wm, wm + 1.5, T);
  const spots = [[63, 15], [67, 19.5], [60, 11], [69, 13], [64.5, 21.5]];
  return (
    <>
      <Host t={T - s.start} T={T} mood="wow" />
      <Card title="A warming Arabian Sea" t={T} appear={s.start - 0.3}>
        <MapView {...WIDEBOX} view={AS_VIEW} seaColor={mixHex("#d9e8ea", "#f3c6a4", warm)}>{(u) => (
          <>
            {spots.map(([lo, la], i) => { const at = cy - 1.6 + i * 0.4, o = sm(at, at + 0.3, T); const [x, y] = P(lo, la); return (
              <g key={i} opacity={o} transform={`rotate(${-(T * 120 + i * 50) % 360} ${x} ${y})`}>
                {[0, 1, 2].map((j) => <path key={j} d={`M${x} ${y} q ${30 * u} ${-8 * u} ${40 * u} ${18 * u}`} fill="none" stroke={C.ink} strokeWidth={6 * u} transform={`rotate(${j * 120} ${x} ${y})`} />)}
                <circle cx={x} cy={y} r={8 * u} fill={C.card} stroke={C.ink} strokeWidth={4 * u} />
              </g>); })}
            <Label x={X(62)} y={Y(7)} size={30 * u} color="#4d7d86" sc>Arabian Sea</Label>
          </>)}
        </MapView>
        <Line T={T} at={wm} x={960} y={PANEL.top + 20} w={400} size={36} color={C.hot}>Sea surface warming</Line>
        <Line T={T} at={cy - 0.6} x={960} y={PANEL.top + 120} w={400} size={36}>more frequent cyclones</Line>
        <Line T={T} at={cy} x={960} y={PANEL.top + 190} w={400} size={36} color={C.red}>and more intense ones</Line>
      </Card>
    </>
  );
};

/* =========================================================== 3e impacts */
export const Impacts = ({ T }: SP) => {
  const s = segOf("impact"), fl = cue("impact", "floods"), dr = cue("impact", "droughts");
  const items = [{ at: cue("impact", "farmers"), t: "Farmers" }, { at: cue("impact", "cities"), t: "Cities" }, { at: cue("impact", "reservoirs"), t: "Reservoirs" }];
  return (
    <>
      <Host t={T - s.start} T={T} mood={T > dr ? "hot" : "umbrella"} />
      <Card title="What it means on the ground" t={T} appear={s.start - 0.3}>
        <svg width={CARD.w} height={CARD.h} style={{ position: "absolute", inset: 0, overflow: "visible" }}>
          {items.map((it, i) => { const o = sm(it.at - 0.2, it.at + 0.3, T), x = 90 + i * 430; return (
            <g key={i} opacity={o} filter="url(#wob)">
              <rect x={x} y={150} width={380} height={420} rx={18} fill="#fffaf0" stroke={C.ink} strokeWidth={4} />
              {i === 0 && <>{[0, 1, 2, 3, 4].map((j) => <path key={j} d={`M${x + 70 + j * 60} 470 l -10 -110 M${x + 70 + j * 60} 420 l -24 -20 M${x + 66 + j * 60} 395 l 20 -22`} stroke="#b79a4a" strokeWidth={6} fill="none" />)}
                <path d={`M${x + 40} 480 l 300 0`} stroke="#9a7b4f" strokeWidth={8} />{T > dr && <path d={`M${x + 80} 500 l 30 30 l -10 20 M${x + 220} 500 l -20 26 l 18 22`} stroke={C.ink} strokeWidth={4} fill="none" />}</>}
              {i === 1 && <>{[0, 1, 2, 3].map((j) => <rect key={j} x={x + 60 + j * 70} y={300 - (j % 2) * 70} width={56} height={200 + (j % 2) * 70} fill="#d9cdb8" stroke={C.ink} strokeWidth={4} />)}
                <rect x={x + 30} y={500 - 80 * sm(fl, fl + 0.8, T)} width={320} height={80 * sm(fl, fl + 0.8, T)} fill={C.rain} opacity={0.75} /></>}
              {i === 2 && <><path d={`M${x + 50} 300 L${x + 330} 300 L${x + 300} 520 L${x + 80} 520 Z`} fill="#e6dccb" stroke={C.ink} strokeWidth={4} />
                <path d={`M${x + 70} ${520 - 160 * (0.5 + 0.45 * Math.sin(T * 1.6))} L${x + 310} ${520 - 160 * (0.5 + 0.45 * Math.sin(T * 1.6))} L${x + 300} 520 L${x + 80} 520 Z`} fill={C.rainLight} /></>}
            </g>); })}
          {items.map((it, i) => <text key={i} x={280 + i * 430} y={630} fontFamily={FONT_SC} fontSize={44} textAnchor="middle" fill={C.ink} opacity={sm(it.at - 0.2, it.at + 0.3, T)}>{it.t}</text>)}
        </svg>
        <Line T={T} at={fl} x={90} y={690} size={46} color={C.rain}>More floods</Line>
        <Line T={T} at={dr} x={480} y={690} size={46} color={C.hot}>and more droughts</Line>
        <Line T={T} at={cue("impact", "same")} x={900} y={698} size={36} color={C.red}>sometimes in the same season</Line>
      </Card>
    </>
  );
};

/* =========================================================== outro */
export const Outro = ({ T }: SP) => {
  const s = segOf("outro");
  return (
    <>
      <Host t={T - s.start} T={T} mood="wave" />
      <Card title="Remember" t={T} appear={s.start - 0.3}>
        <Line T={T} at={cue("outro", "seasonal")} x={120} w={1200} y={200} size={64}>A seasonal reversal of winds</Line>
        <Line T={T} at={cue("outro", "driven")} x={120} w={1200} y={330} size={54} color={C.soft}>driven by heat, by Earth's spin, and by the oceans</Line>
        <Line T={T} at={cue("outro", "warming")} x={120} w={1200} y={500} size={64} color={C.red}>A warming climate makes it more extreme</Line>
      </Card>
    </>
  );
};

/* every map base drawn in the video (pre-rendered to PNG by MonsoonStatics) */
export const MAP_BASES = [{ view: INDIA, box: MAPBOX }, { view: WIDE, box: WIDEBOX }, { view: ITCZ_VIEW, box: WIDEBOX }, { view: JET_VIEW, box: WIDEBOX }, { view: AS_VIEW, box: WIDEBOX }];
