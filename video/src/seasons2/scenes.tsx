import { TAGCOL } from "../monsoon/qa";
import React from "react";
import { Arrow, C, CARD, Card, Cloud, FONT, FONT_SC, Host, Label, lerp, sm } from "../monsoon/kit";
import { MapView, P, X, Y } from "../monsoon/map";
import { Big, Globe, Line, PANEL, SunIcon, Tree, W, WORLD_BOX, WORLD_VIEW, WorldView, cue, gpt, segOf, txt } from "./parts";

type SP = { T: number };
const Svg = ({ children }: { children: React.ReactNode }) => <svg width={CARD.w} height={CARD.h} style={{ position: "absolute", inset: 0, overflow: "visible" }}>{children}</svg>;
const GX = 380, GY = 450, GR = 270;   // globe placement inside the card
const KEY_LATS = (k = 1) => [
  { lat: 66.5, color: "#3f86d6", w: 4, dash: "12 9", o: k }, { lat: 23.5, color: C.sunDark, w: 4.5, dash: "14 9", o: k }, { lat: 0, color: C.red, w: 5, o: k },
  { lat: -23.5, color: C.sunDark, w: 4.5, dash: "14 9", o: k }, { lat: -66.5, color: "#3f86d6", w: 4, dash: "12 9", o: k }];

/* =========================================================== intro + part cards */
export const Intro = ({ T }: SP) => {
  const s = segOf("intro"), t = T - s.start;
  return (
    <>
      <Host t={t} T={T} mood="wave" />
      <Card title="Seasons, Solstices and Heat Zones" t={T} appear={s.start - 0.2}>
        <Svg><SunIcon x={1180} y={190} r={60} T={T} /><Globe cx={GX} cy={GY} r={GR} tilt={23.5} sunAngle={0} meridians={10} spin={T * 12} lats={KEY_LATS()} /></Svg>
        {([["WHAT", "are the imaginary lines, solstices and equinoxes?", "what"], ["WHY", "do we have seasons, and different climates?", "why"], ["HOW", "do they shape weather and forests?", "how"]] as const).map(([tg, x, w], i) =>
          <Line key={i} T={T} at={cue("intro", w)} y={PANEL.top + 170 + i * 130} size={44} color={TAGCOL[tg]}>{`${tg} ${x}`}</Line>)}
      </Card>
    </>
  );
};
export const PartCard = ({ T, id, n, title, icon }: SP & { id: string; n: number; title: string; icon: React.ReactNode }) => {
  const s = segOf(id);
  return (
    <>
      <Host t={T - s.start} T={T} mood="wave" />
      <Card title={`Part ${n}`} t={T} appear={s.start - 0.3}>
        <div style={{ position: "absolute", left: 0, right: 0, top: 240, textAlign: "center", fontFamily: FONT, fontSize: 84, color: C.ink }}>{title}</div>
        <div style={{ position: "absolute", left: 0, right: 0, top: 420, display: "flex", justifyContent: "center" }}>{icon}</div>
      </Card>
    </>
  );
};

/* =========================================================== part 1: lines */
export const Latitude = ({ T }: SP) => {
  const s = segOf("lat"), a = cue("lat", "latitude", 1), m = cue("lat", "measured");
  const lats = [0, 30, 60, -30, -60].map((lat, i) => ({ lat, color: lat === 0 ? C.red : "#2f6d9a", w: lat === 0 ? 5 : 3.5, o: sm(a + i * 0.35, a + 0.4 + i * 0.35, T) }));
  return (
    <>
      <Host t={T - s.start} T={T} mood="point" />
      <Card title="Latitude: the parallels" t={T} appear={s.start - 0.3}>
        <Svg>
          <Globe cx={GX} cy={GY} r={GR} lats={lats} axis={false} />
          {[[0, "0° Equator"], [30, "30° N"], [60, "60° N"], [-30, "30° S"], [-60, "60° S"]].map(([lat, l], i) => { const [x, y] = gpt(GX, GY, GR, 0, lat as number, 90); return <g key={i} opacity={sm(m + i * 0.25, m + 0.4 + i * 0.25, T)}>{txt(x + 16, y + 10, l as string, 32, lat === 0 ? C.red : C.ink, "start")}</g>; })}
          <g opacity={sm(m + 1.5, m + 2, T)}>{txt(GX, GY - GR - 24, "90° N (North Pole)", 32)}{txt(GX, GY + GR + 48, "90° S (South Pole)", 32)}</g>
        </Svg>
        <Line T={T} at={a} y={PANEL.top + 40} size={46}>Run east to west</Line>
        <Line T={T} at={a + 0.6} y={PANEL.top + 110} size={36} color={C.soft}>parallel to the Equator, never meeting</Line>
        <Line T={T} at={m} y={PANEL.top + 170} size={46} color={C.red}>0° to 90° N and S</Line>
        <Line T={T} at={m + 0.6} y={PANEL.top + 240} size={36} color={C.soft}>angle north or south of the Equator</Line>
      </Card>
    </>
  );
};
export const Longitude = ({ T }: SP) => {
  const s = segOf("lon"), a = cue("lon", "longitude", 1), g = cue("lon", "greenwich"), e = cue("lon", "east");
  return (
    <>
      <Host t={T - s.start} T={T} mood="point" />
      <Card title="Longitude: the meridians" t={T} appear={s.start - 0.3}>
        <Svg>
          <Globe cx={GX} cy={GY} r={GR} meridians={Math.round(12 * sm(a, a + 2, T))} spin={-20} prime={T > g} lats={[{ lat: 0, color: C.red, w: 3, o: 0.5 }]} axis={false} />
          <g opacity={sm(g, g + 0.4, T)}>{(() => { const [x, y] = gpt(GX, GY, GR, 0, 30, -20); return <>{txt(x - 10, y - 20, "0° Prime Meridian", 32, C.red, "end")}{txt(x - 10, y + 16, "(Greenwich)", 28, C.red, "end")}</>; })()}</g>
          <g opacity={sm(e, e + 0.4, T)}>{txt(GX + GR + 30, GY - 30, "→ 180° E", 32, C.ink, "start")}{txt(GX - GR - 30, GY - 30, "180° W ←", 32, C.ink, "end")}</g>
        </Svg>
        <Line T={T} at={a} y={PANEL.top + 40} size={46}>Run pole to pole</Line>
        <Line T={T} at={a + 0.6} y={PANEL.top + 110} size={36} color={C.soft}>all meet at the North and South Poles</Line>
        <Line T={T} at={g} y={PANEL.top + 230} size={46} color={C.red}>0° at Greenwich</Line>
        <Line T={T} at={e} y={PANEL.top + 300} size={40}>to 180° east and west</Line>
      </Card>
    </>
  );
};
export const Equator = ({ T }: SP) => {
  const s = segOf("equator"), l = cue("equator", "longest"), d = cue("equator", "divides");
  return (
    <>
      <Host t={T - s.start} T={T} mood="wow" />
      <Card title="The Equator: 0°" t={T} appear={s.start - 0.3}>
        <Svg>
          <Globe cx={GX} cy={GY} r={GR} glowLat={T > l ? 0 : null} lats={[{ lat: 0, color: C.red, w: 6 }]} axis={false} />
          <g opacity={sm(d, d + 0.4, T)}>{txt(GX, GY - 110, "Northern Hemisphere", 38, C.ink, "middle", 1, true)}{txt(GX, GY + 140, "Southern Hemisphere", 38, C.ink, "middle", 1, true)}</g>
        </Svg>
        <Line T={T} at={l} y={PANEL.top + 40} size={40}>The longest parallel</Line>
        <Big T={T} at={l + 0.5} y={PANEL.top + 110}>40,075 km</Big>
        <Line T={T} at={l + 0.8} y={PANEL.top + 250} size={34} color={C.soft}>Earth's equatorial circumference</Line>
        <Line T={T} at={d} y={PANEL.top + 360} size={40}>Divides Earth into two hemispheres</Line>
      </Card>
    </>
  );
};
export const Parallels = ({ T }: SP) => {
  const s = segOf("parallels"), c = cue("parallels", "cancer"), cp = cue("parallels", "capricorn"), ar = cue("parallels", "arctic"), ti = cue("parallels", "tilt");
  const items = [{ lat: 66.5, l: "66.5° N  Arctic Circle", at: ar, col: "#3f86d6" }, { lat: 23.5, l: "23.5° N  Tropic of Cancer", at: c, col: C.sunDark }, { lat: 0, l: "0°  Equator", at: s.start, col: C.red },
    { lat: -23.5, l: "23.5° S  Tropic of Capricorn", at: cp, col: C.sunDark }, { lat: -66.5, l: "66.5° S  Antarctic Circle", at: ar + 0.4, col: "#3f86d6" }];
  return (
    <>
      <Host t={T - s.start} T={T} mood="point" />
      <Card title="The five key parallels" t={T} appear={s.start - 0.3}>
        <Svg>
          <Globe cx={GX} cy={GY} r={GR} lats={items.map((it, i) => ({ ...KEY_LATS()[i], o: sm(it.at - 0.1, it.at + 0.3, T) }))} axis={false} />
          {items.map((it, i) => { const [x, y] = gpt(GX, GY, GR, 0, it.lat, 88), ly = 160 + i * 130; return (
            <g key={i} opacity={sm(it.at - 0.1, it.at + 0.3, T)}>
              <path d={`M${x} ${y} L${GX + GR + 60} ${ly - 10}`} stroke={C.ink} strokeWidth={2} fill="none" /><circle cx={x} cy={y} r={6} fill={C.ink} />
              {txt(GX + GR + 70, ly, it.l, 40, it.col, "start")}</g>); })}
        </Svg>
        <div style={{ position: "absolute", left: 700, top: 740, fontFamily: FONT, fontSize: 34, color: C.ink, opacity: sm(ti, ti + 0.4, T) }}>Positions set by Earth's 23.5° tilt (precisely 23° 26′)</div>
      </Card>
    </>
  );
};
const TOC_STATES: [string, number, number][] = [["Gujarat", 70.4, -1], ["Rajasthan", 74.2, 1], ["Madhya Pradesh", 78.2, -1], ["Chhattisgarh", 82.3, 1], ["Jharkhand", 85.5, -1], ["West Bengal", 88.0, 1], ["Tripura", 91.5, -1], ["Mizoram", 92.9, 1]];
export const IndiaToc = ({ T }: SP) => {
  const s = segOf("india"), e = cue("india", "eight");
  const names = TOC_STATES.map(([n]) => n.split(" ")[0].toLowerCase());
  const at = names.map((n) => { try { return cue("india", n); } catch { return e + 1; } });
  const shown = at.filter((a) => T > a).length;
  return (
    <>
      <Host t={T - s.start} T={T} mood="point" />
      <Card title="Tropic of Cancer across India" t={T} appear={s.start - 0.3}>
        <MapView left={34} top={92} w={740} h={700} view={{ lon0: 63, lon1: 99, lat0: 5, lat1: 37.6 }}>{(u) => (
          <>
            <path d={`M${X(63)} ${Y(23.44)} L${X(99)} ${Y(23.44)}`} stroke={C.sunDark} strokeWidth={7 * u} strokeDasharray={`${18 * u} ${11 * u}`} opacity={sm(s.start, s.start + 0.6, T)} />
            <Label x={X(64)} y={Y(23.44) - 16 * u} size={28 * u} anchor="start" color={C.sunDark} sc>23.5° N</Label>
            {TOC_STATES.map(([n, lo, side], i) => { const [x, y] = P(lo, 23.44), o = sm(at[i] - 0.1, at[i] + 0.3, T); return (
              <g key={n} opacity={o}><circle cx={x} cy={y} r={10 * u} fill={C.red} stroke={C.ink} strokeWidth={3 * u} />
                <Label x={x} y={y + (side < 0 ? -26 : 46) * u} size={24 * u}>{`${i + 1}`}</Label></g>); })}
          </>)}
        </MapView>
        <Big T={T} at={e} y={PANEL.top - 10} x={800} size={110}>{`${Math.max(shown, T > e ? 1 : 0) ? shown || 8 : 8} states`}</Big>
        {TOC_STATES.map(([n], i) => <Line key={n} T={T} at={at[i]} x={800 + (i % 2) * 270} y={PANEL.top + 150 + Math.floor(i / 2) * 64} size={36} w={270}>{`${i + 1}. ${n}`}</Line>)}
        <Line T={T} at={e + 0.5} x={800} y={PANEL.top + 430} size={30} color={C.soft}>west to east</Line>
      </Card>
    </>
  );
};
export const TimeScene = ({ T }: SP) => {
  const s = segOf("time"), f = cue("time", "15"), ist = cue("time", "indian");
  const x0 = 120, dx = 12.6, xl = (lon: number) => x0 + lon * dx;
  const hand = (cx: number, cy: number, h: number, m: number, k: number) => {
    const ah = ((h % 12) + m / 60) / 12 * Math.PI * 2 - Math.PI / 2, am = m / 60 * Math.PI * 2 - Math.PI / 2;
    return <g opacity={k}><circle cx={cx} cy={cy} r={62} fill="#fffaf0" stroke={C.ink} strokeWidth={5} />
      <line x1={cx} y1={cy} x2={cx + Math.cos(ah) * 34} y2={cy + Math.sin(ah) * 34} stroke={C.ink} strokeWidth={7} strokeLinecap="round" />
      <line x1={cx} y1={cy} x2={cx + Math.cos(am) * 50} y2={cy + Math.sin(am) * 50} stroke={C.ink} strokeWidth={4} strokeLinecap="round" /></g>;
  };
  return (
    <>
      <Host t={T - s.start} T={T} mood="think" />
      <Card title="Longitude and time" t={T} appear={s.start - 0.3}>
        <Svg>
          <line x1={xl(0)} y1={430} x2={xl(90)} y2={430} stroke={C.ink} strokeWidth={5} />
          {[0, 15, 30, 45, 60, 75, 90].map((lon, i) => <g key={lon} opacity={sm(f + i * 0.2, f + 0.3 + i * 0.2, T)}>
            <line x1={xl(lon)} y1={410} x2={xl(lon)} y2={450} stroke={C.ink} strokeWidth={4} />{txt(xl(lon), 490, `${lon}° E`, 30)}{txt(xl(lon), 395, `+${i} h`, 30, C.rain)}</g>)}
          {hand(xl(0), 280, 12, 0, sm(s.start + 0.5, s.start + 1, T))}{txt(xl(0), 190, "Greenwich 12:00", 30, C.ink, "middle", sm(s.start + 0.5, s.start + 1, T))}
          <g opacity={sm(ist, ist + 0.4, T)}>
            <line x1={xl(82.5)} y1={330} x2={xl(82.5)} y2={560} stroke={C.red} strokeWidth={6} strokeDasharray="14 9" />
            {hand(xl(82.5), 640, 17, 30, 1)}{txt(xl(82.5) - 80, 650, "17:30", 40, C.red, "end")}{txt(xl(82.5), 600 - 30, "82.5° E  IST", 32, C.red)}
          </g>
        </Svg>
        <Line T={T} at={f} x={760} y={90} size={40} w={560}>360° in 24 h = 15° per hour</Line>
        <Line T={T} at={cue("time", "1", 1)} x={760} y={145} size={40} w={560} color={C.rain}>1° = 4 minutes</Line>
        <Line T={T} at={ist} x={120} y={700} size={34} w={560} color={C.soft}>IST meridian passes near Mirzapur (UP)</Line>
        <Big T={T} at={cue("time", "5")} x={760} y={205} size={90}>GMT + 5:30</Big>
      </Card>
    </>
  );
};

/* =========================================================== part 2: tilt and orbit */
export const Tilt = ({ T }: SP) => {
  const s = segOf("tilt"), a = cue("tilt", "tilt", 1), b = cue("tilt", "66.5"), p = cue("tilt", "pole");
  const tl = 23.5 * sm(a - 0.5, a + 0.6, T), r = 195, cx = 420, cy = 470, th = tl * Math.PI / 180;
  const arc = (R: number, a0: number, a1: number) => `M ${cx + R * Math.sin(a0)} ${cy - R * Math.cos(a0)} A ${R} ${R} 0 0 1 ${cx + R * Math.sin(a1)} ${cy - R * Math.cos(a1)}`;
  return (
    <>
      <Host t={T - s.start} T={T} mood="point" />
      <Card title="Earth's tilted axis" t={T} appear={s.start - 0.3}>
        <Svg>
          <line x1={cx - 380} y1={cy} x2={cx + 380} y2={cy} stroke={C.soft} strokeWidth={3} strokeDasharray="14 10" />
          {txt(cx + 380, cy + 40, "orbital plane", 28, C.soft, "end")}
          <Globe cx={cx} cy={cy} r={r} tilt={tl} sunAngle={0} lats={KEY_LATS(0.8)} meridians={8} spin={T * 10} />
          <line x1={cx} y1={cy - r * 1.4} x2={cx} y2={cy + r * 1.4} stroke={C.ink} strokeWidth={3} strokeDasharray="10 8" opacity={0.6} />
          <g opacity={sm(a, a + 0.5, T)}><path d={arc(r * 1.32, 0, th)} fill="none" stroke={C.red} strokeWidth={5} />{txt(cx - 16, cy - r * 1.42, "23.5°", 40, C.red, "end")}</g>
          <g opacity={sm(b, b + 0.5, T)}><path d={arc(r * 0.45, th, Math.PI / 2)} fill="none" stroke={C.rain} strokeWidth={5} />{txt(cx + 165, cy - 70, "66.5°", 36, C.rain, "start")}</g>
          <g opacity={sm(p, p + 0.5, T)}><path d={`M ${cx + Math.sin(th) * r * 1.62} ${cy - Math.cos(th) * r * 1.62 - 26} l 8 20 l 22 0 l -18 13 l 7 21 l -19 -13 l -19 13 l 7 -21 l -18 -13 l 22 0 Z`} fill="#ffd66b" stroke={C.ink} strokeWidth={3} />
            {txt(cx + Math.sin(th) * r * 1.62 + 40, cy - Math.cos(th) * r * 1.62, "Pole Star (Polaris)", 30, C.ink, "start")}</g>
        </Svg>
        <Line T={T} at={a} x={860} y={PANEL.top + 60} w={480} size={44} color={C.red}>23.5° from the vertical</Line>
        <Line T={T} at={b} x={860} y={PANEL.top + 170} w={480} size={40} color={C.rain}>66.5° with the orbital plane</Line>
        <Line T={T} at={p} x={860} y={PANEL.top + 300} w={480} size={38}>always points to the Pole Star</Line>
      </Card>
    </>
  );
};
const OrbitScene = ({ T, id, title, mode }: SP & { id: string; title: string; mode: "orbit" | "distance" }) => {
  const s = segOf(id), cx = 660, cy = 400, A = 470, B = 200, ex = mode === "distance" ? 70 : 0;
  const ang = mode === "orbit" ? (T - s.start) * 0.55 : Math.PI * 0.0 + Math.sin((T - s.start) * 0.5) * 0.15;
  const pos = (a: number) => [cx + A * Math.cos(a), cy + B * Math.sin(a)];
  const months = [[0, "June"], [Math.PI / 2, "September"], [Math.PI, "December"], [-Math.PI / 2, "March"]] as [number, string][];
  const earth = (a: number, k = 1) => { const [x, y] = pos(a); return <Globe key={a} cx={x} cy={y} r={52} tilt={23.5} sunAngle={Math.atan2(cy - y, cx + ex - x)} axis o={k} landTint={false} lats={[{ lat: 0, color: C.red, w: 2 }]} />; };
  const near = mode === "distance" ? cue(id, "closest") : 0, far = mode === "distance" ? cue(id, "farthest") : 0;
  return (
    <>
      <Host t={T - s.start} T={T} mood={mode === "distance" ? "think" : "point"} />
      <Card title={title} t={T} appear={s.start - 0.3}>
        <Svg>
          <ellipse cx={cx} cy={cy} rx={A} ry={B} fill="none" stroke={C.ink} strokeWidth={3} strokeDasharray="12 10" />
          <SunIcon x={cx + ex} y={cy} r={62} T={T} />
          {mode === "orbit" ? <>{months.map(([a, m]) => { const [x, y] = pos(a); return <g key={m}>{txt(x, y + (y > cy ? 100 : -78), m, 32, C.soft)}</g>; })}{earth(ang)}</> : <>
            {(() => { const [x1, y1] = [cx + ex + 62, cy], [x2] = pos(0), [x3] = pos(Math.PI); return <>
              <g opacity={sm(near, near + 0.4, T)}>{earth(Math.PI)}<line x1={cx + ex - 62} y1={cy} x2={x3 + 52} y2={cy} stroke={C.red} strokeWidth={4} />{txt((cx + ex + x3) / 2, cy - 18, "147 million km", 32, C.red)}{txt(x3, cy + 100, "early January (perihelion)", 28)}</g>
              <g opacity={sm(far, far + 0.4, T)}>{earth(0)}<line x1={x1} y1={y1} x2={x2 - 52} y2={cy} stroke={C.rain} strokeWidth={4} />{txt((x1 + x2) / 2, cy - 18, "152 million km", 32, C.rain)}{txt(x2, cy + 100, "early July (aphelion)", 28)}</g></>; })()}
          </>}
        </Svg>
        {mode === "orbit" && <><Line T={T} at={cue(id, "365")} x={70} y={735} w={600} size={38}>One orbit ≈ 365¼ days</Line><Line T={T} at={cue(id, "seasons")} x={700} y={735} w={640} size={38} color={C.red}>hemispheres take turns leaning sunward</Line></>}
        {mode === "distance" && <Line T={T} at={cue(id, "yet")} x={70} y={735} w={1200} size={42} color={C.red}>Yet January is winter in India: distance is not the cause</Line>}
      </Card>
    </>
  );
};
export const Orbit = ({ T }: SP) => <OrbitScene T={T} id="orbit" title="Revolution around the Sun" mode="orbit" />;
export const Distance = ({ T }: SP) => <OrbitScene T={T} id="distance" title="Not distance: perihelion and aphelion" mode="distance" />;

/* =========================================================== part 3: solstices */
const SolsticeScene = ({ T, id, title, tilt, rows }: SP & { id: string; title: string; tilt: number; rows: { at: number; t: string; c?: string; s?: number }[] }) => {
  // Sun on the LEFT so its rays never cross the text panel on the right; positive "tilt" = north pole leaning toward the Sun
  const s = segOf(id), sub = tilt > 0 ? 23.5 : tilt < 0 ? -23.5 : 0, gx = 560, gr = 240, gt = -tilt;
  const rays = [-0.32, -0.16, 0, 0.16, 0.32];
  const [sx, sy] = gpt(gx, GY, gr, gt, sub, -90);
  return (
    <>
      <Host t={T - s.start} T={T} mood={tilt >= 0 ? "hot" : "think"} />
      <Card title={title} t={T} appear={s.start - 0.3}>
        <Svg>
          <SunIcon x={95} y={GY} r={54} T={T} o={0.95} />
          {rays.map((k, i) => <Arrow key={i} pts={[[165, GY + k * 260], [gx - gr - 22, GY + k * 260]]} k={sm(s.start + 0.2 + i * 0.08, s.start + 1.2 + i * 0.08, T)} color="#ffcf4d" w={7} head={20} smooth={false} />)}
          <Globe cx={gx} cy={GY} r={gr} tilt={gt} sunAngle={Math.PI} lats={KEY_LATS(0.9)} meridians={8} spin={T * 10} glowLat={sub} />
          <circle cx={sx} cy={sy} r={14} fill="#ffd66b" stroke={C.ink} strokeWidth={4} />
          {txt(sx + 28, sy + 46, "Sun overhead", 30, C.ink, "start")}
        </Svg>
        {rows.map((r, i) => <Line key={i} T={T} at={r.at} x={850} y={PANEL.top - 20 + i * 104} w={500} size={r.s ?? 38} color={r.c ?? C.ink}>{r.t}</Line>)}
      </Card>
    </>
  );
};
export const June = ({ T }: SP) => <SolsticeScene T={T} id="june" title="Summer solstice · around 21 June" tilt={23.5} rows={[
  { at: cue("june", "summer"), t: "Summer solstice", s: 46 }, { at: cue("june", "overhead"), t: "Sun overhead: Tropic of Cancer (23.5° N)", c: C.sunDark },
  { at: cue("june", "longest"), t: "Longest day, Northern Hemisphere" }, { at: cue("june", "delhi"), t: "Delhi ≈ 14 h daylight", c: C.red, s: 44 },
  { at: cue("june", "arctic"), t: "Arctic Circle: the Sun never sets", c: C.rain }]} />;
export const Dec = ({ T }: SP) => <SolsticeScene T={T} id="dec" title="Winter solstice · around 22 December" tilt={-23.5} rows={[
  { at: cue("dec", "winter"), t: "Winter solstice", s: 46 }, { at: cue("dec", "overhead"), t: "Sun overhead: Tropic of Capricorn (23.5° S)", c: C.sunDark },
  { at: cue("dec", "delhi"), t: "Delhi ≈ 10 h daylight", c: C.red, s: 44 }, { at: cue("dec", "arctic"), t: "Arctic: polar night", c: C.rain },
  { at: cue("dec", "southern"), t: "Southern Hemisphere: summer" }]} />;
export const Equinox = ({ T }: SP) => <SolsticeScene T={T} id="equinox" title="Equinoxes · 21 March and 23 September" tilt={0} rows={[
  { at: cue("equinox", "21st"), t: "21 March · 23 September", s: 44 }, { at: cue("equinox", "overhead"), t: "Sun overhead: the Equator", c: C.red },
  { at: cue("equinox", "equinoxes"), t: "Equinox = 'equal night'" }, { at: cue("equinox", "day"), t: "Day ≈ night ≈ 12 h everywhere", c: C.rain, s: 42 }]} />;
export const Noon = ({ T }: SP) => {
  const s = segOf("noon"), j = cue("noon", "85"), d = cue("noon", "38"), sp = cue("noon", "spreads");
  const panel = (x: number, deg: number, at: number, label: string, col: string) => {
    const g = 600, a = deg * Math.PI / 180, bw = 70 / Math.sin(a), o = sm(at - 0.2, at + 0.4, T);
    const dir = [-Math.cos(a), -Math.sin(a)], L = 330, cx = x + 300;
    return (<g opacity={o}>
      <path d={`M ${cx - bw / 2} ${g} L ${cx + bw / 2} ${g} L ${cx + bw / 2 + dir[0] * -L} ${g + dir[1] * L} L ${cx - bw / 2 + dir[0] * -L} ${g + dir[1] * L} Z`} fill="#ffd66b" opacity={0.6} stroke={C.sunDark} strokeWidth={3} />
      <line x1={x + 40} y1={g} x2={x + 560} y2={g} stroke={C.ink} strokeWidth={6} />
      <rect x={cx - bw / 2} y={g - 6} width={bw} height={12} fill={col} />
      <path d={`M ${cx + 110} ${g} A 110 110 0 0 0 ${cx + 110 * Math.cos(a)} ${g - 110 * Math.sin(a)}`} fill="none" stroke={col} strokeWidth={5} />
      {txt(cx + 150, g - 40, `${deg}°`, 54, col, "start")}{txt(x + 300, g + 60, label, 34)}
    </g>);
  };
  return (
    <>
      <Host t={T - s.start} T={T} mood="point" />
      <Card title="Noon Sun over Delhi (28.6° N)" t={T} appear={s.start - 0.3}>
        <Svg>{panel(60, 85, j, "21 June · high Sun", C.red)}{panel(700, 38, d, "22 December · low Sun", C.rain)}</Svg>
        <Line T={T} at={sp} x={80} y={700} w={1240} size={40} color={C.red}>Low Sun: the same light spreads over more ground and heats it less</Line>
      </Card>
    </>
  );
};

/* =========================================================== part 4: climates and forests */
export const EqZone = ({ T }: SP) => {
  const s = segOf("eqzone"), r = cue("eqzone", "rises"), c = cue("eqzone", "convectional"), tc = cue("eqzone", "27"), mm = cue("eqzone", "2,000");
  return (
    <>
      <Host t={T - s.start} T={T} mood="umbrella" />
      <Card title="At the Equator: hot and wet all year" t={T} appear={s.start - 0.3}>
        <Svg>
          <SunIcon x={360} y={170} r={52} T={T} />
          <rect x={60} y={600} width={620} height={110} fill="#8cc06a" stroke={C.ink} strokeWidth={5} />
          {[0, 1, 2, 3, 4, 5].map((i) => <Tree key={i} kind="rain" x={110 + i * 105} y={600} s={0.42} />)}
          {[0, 1, 2].map((i) => <Arrow key={i} pts={[[180 + i * 180, 560], [190 + i * 180, 440], [180 + i * 180, 330]]} k={sm(r + i * 0.2, r + 1 + i * 0.2, T)} color="#f0a27a" w={9} head={26} />)}
          <g opacity={sm(c - 0.3, c + 0.3, T)}><Cloud x={300} y={300} s={95} T={T} rain={sm(c, c + 0.5, T)} dark /><Cloud x={500} y={290} s={80} T={T + 1} rain={sm(c, c + 0.5, T)} dark /></g>
          {txt(370, 760, "Equatorial belt (about 10° N to 10° S)", 30, C.soft)}
        </Svg>
        <Line T={T} at={s.start + 1} x={760} y={PANEL.top - 10} w={560} size={40}>Sun high all year · ~12 h days</Line>
        <Line T={T} at={c} x={760} y={PANEL.top + 70} w={560} size={40} color={C.rain}>Convectional rain, almost daily</Line>
        <Big T={T} at={tc} x={760} y={PANEL.top + 190} size={100}>≈ 27 °C</Big>
        <Line T={T} at={tc + 0.3} x={760} y={PANEL.top + 300} w={560} size={32} color={C.soft}>average temperature, little seasonal change</Line>
        <Big T={T} at={mm} x={760} y={PANEL.top + 400} size={100} color={C.rain}>&gt; 2,000 mm</Big>
        <Line T={T} at={mm + 0.3} x={760} y={PANEL.top + 510} w={560} size={32} color={C.soft}>rainfall a year</Line>
      </Card>
    </>
  );
};
const FORESTS = [{ n: "Amazon", lo: -62, la: -4, dx: 0, dy: -34 }, { n: "Congo basin", lo: 22, la: 0, dx: 0, dy: -34 }, { n: "SE Asia", lo: 112, la: 1, dx: 0, dy: 58 },
  { n: "Western Ghats", lo: 75, la: 12, dx: -20, dy: 56 }, { n: "Andaman & Nicobar", lo: 92.7, la: 10, dx: -14, dy: -44 }];
export const Rainforest = ({ T }: SP) => {
  const s = segOf("rainforest"), at = [cue("rainforest", "amazon"), cue("rainforest", "congo"), cue("rainforest", "western") - 0.6, cue("rainforest", "western"), cue("rainforest", "andaman")];
  return (
    <>
      <Host t={T - s.start} T={T} mood="umbrella" />
      <Card title="Tropical evergreen rainforests" t={T} appear={s.start - 0.3}>
        <WorldView left={34} top={92} w={900} h={560} view={{ lon0: -90, lon1: 130, lat0: -35, lat1: 35 }}>{(u) => (
          <>
            {[0].map((la) => <path key={la} d={`M${-900} ${-la * 10} L${1300} ${-la * 10}`} stroke={C.red} strokeWidth={4 * u} strokeDasharray={`${14 * u} ${9 * u}`} />)}
            {[23.5, -23.5].map((la) => <path key={la} d={`M${-900} ${-la * 10} L${1300} ${-la * 10}`} stroke={C.sunDark} strokeWidth={3 * u} strokeDasharray={`${12 * u} ${9 * u}`} opacity={0.7} />)}
            {FORESTS.map((f, i) => { const [x, y] = W(f.lo, f.la), o = sm(at[i] - 0.2, at[i] + 0.3, T); return (
              <g key={f.n} opacity={o}><circle cx={x} cy={y} r={(i < 3 ? 26 : 12) * u} fill="#2f7d3a" opacity={0.7} stroke={C.ink} strokeWidth={3 * u} />
                <Label x={x + f.dx * u} y={y + f.dy * u} size={24 * u} anchor={i === 3 || i === 4 ? "end" : "middle"}>{f.n}</Label></g>); })}
          </>)}
        </WorldView>
        <Svg>
          <Tree kind="rain" x={1150} y={640} s={1.15} o={sm(s.start + 0.3, s.start + 0.8, T)} />
          <g opacity={sm(cue("rainforest", "multi"), cue("rainforest", "multi") + 0.4, T)}>{txt(1150, 230, "emergent", 26, C.soft)}{txt(1260, 330, "canopy", 26, C.soft, "start")}{txt(1250, 470, "understorey", 26, C.soft, "start")}</g>
        </Svg>
        <Line T={T} at={cue("rainforest", "mahogany")} x={60} y={680} w={880} size={38}>Mahogany · ebony · rosewood: hardwoods, never leafless</Line>
      </Card>
    </>
  );
};
const DESERTS = [{ n: "Sahara", lo: 13, la: 23 }, { n: "Arabian", lo: 47, la: 22 }, { n: "Thar", lo: 71.5, la: 27 }, { n: "Kalahari", lo: 22, la: -23 }, { n: "Atacama", lo: -69.5, la: -24 }, { n: "Australian", lo: 130, la: -25 }];
export const Tropics = ({ T }: SP) => {
  const s = segOf("tropics"), sk = cue("tropics", "sinks"), dr = cue("tropics", "dry");
  const at = ["sahara", "arabian", "thar", "kalahari", "atacama", "australian"].map((n) => cue("tropics", n));
  return (
    <>
      <Host t={T - s.start} T={T} mood="hot" />
      <Card title="Near the tropics: sinking dry air and deserts" t={T} appear={s.start - 0.3}>
        <WorldView {...WORLD_BOX} view={WORLD_VIEW}>{(u) => (
          <>
            <path d={`M-1100 0 L1700 0`} stroke={C.red} strokeWidth={4 * u} strokeDasharray={`${14 * u} ${9 * u}`} />
            {[23.5, -23.5].map((la) => <path key={la} d={`M-1100 ${-la * 10} L1700 ${-la * 10}`} stroke={C.sunDark} strokeWidth={5 * u} strokeDasharray={`${16 * u} ${10 * u}`} />)}
            <Label x={-980} y={-245} size={26 * u} anchor="start" color={C.sunDark} sc>Tropic of Cancer 23.5° N</Label>
            <Label x={-560} y={285} size={26 * u} anchor="start" color={C.sunDark} sc>Tropic of Capricorn 23.5° S</Label>
            <Label x={-980} y={-12} size={26 * u} anchor="start" color={C.red} sc>Equator</Label>
            {/* Hadley circulation over Africa: rise at the equator, sink near the tropics */}
            {[1, -1].map((h) => <Arrow key={h} pts={[[200, 0], [210, -60 * h], [250, -150 * h], [300, -240 * h], [330, -200 * h]]} k={sm(s.start + 0.4, sk + 0.6, T)} color="#f0a27a" u={u} w={9} />)}
            {DESERTS.map((d, i) => { const [x, y] = W(d.lo, d.la), o = sm(at[i] - 0.2, at[i] + 0.3, T); return (
              <g key={d.n} opacity={o}><ellipse cx={x} cy={y} rx={60 * u} ry={26 * u} fill="#e6b65c" opacity={0.85} stroke={C.ink} strokeWidth={3 * u} />
                <Label x={x} y={y + 8 * u} size={26 * u}>{d.n}</Label></g>); })}
          </>)}
        </WorldView>
        <Line T={T} at={sk} x={60} y={740} w={640} size={36} color="#c46a3a">Air rising at the Equator sinks near the tropics</Line>
        <Line T={T} at={dr} x={720} y={740} w={640} size={36} color={C.red}>Sinking air is dry: few clouds, little rain</Line>
      </Card>
    </>
  );
};
export const Desert = ({ T }: SP) => {
  const s = segOf("desert");
  const plants = [{ k: "acacia" as const, n: "Acacia", at: cue("desert", "acacia") }, { k: "cactus" as const, n: "Cactus", at: cue("desert", "cactus") }, { k: "acacia" as const, n: "Khejri", at: cue("desert", "khejri") }, { k: "acacia" as const, n: "Babool", at: cue("desert", "babool") }];
  return (
    <>
      <Host t={T - s.start} T={T} mood="hot" />
      <Card title="Desert plants: built to save water" t={T} appear={s.start - 0.3}>
        <Svg>
          <rect x={60} y={520} width={1270} height={70} fill="#e8c98a" stroke={C.ink} strokeWidth={4} />
          {plants.map((p, i) => <g key={p.n}><Tree kind={p.k} x={220 + i * 310} y={520} s={i === 1 ? 1.4 : 1.1} o={sm(p.at - 0.2, p.at + 0.3, T)} />{txt(220 + i * 310, 250, p.n, 40, C.ink, "middle", sm(p.at - 0.2, p.at + 0.3, T))}</g>)}
          {[220, 530, 840, 1150].map((x, i) => <path key={i} d={`M${x} 590 q -30 40 -10 80 M${x} 590 q 25 45 10 95`} stroke="#7a5233" strokeWidth={4} fill="none" opacity={sm(cue("desert", "long"), cue("desert", "long") + 0.5, T)} />)}
        </Svg>
        <Line T={T} at={cue("desert", "long")} x={60} y={715} w={420} size={36}>Long roots reach deep water</Line>
        <Line T={T} at={cue("desert", "small")} x={500} y={715} w={420} size={36}>Small, waxy leaves</Line>
        <Line T={T} at={cue("desert", "thorny")} x={920} y={715} w={420} size={36}>Thorns instead of leaves</Line>
      </Card>
    </>
  );
};
export const India2 = ({ T }: SP) => {
  const s = segOf("india2"), dc = cue("india2", "deciduous"), sh = cue("india2", "shed"), fr = cue("india2", "21.76%");
  const bare = sm(sh, sh + 1, T) * (1 - sm(sh + 2.5, sh + 3.5, T));
  return (
    <>
      <Host t={T - s.start} T={T} mood="idle" />
      <Card title="India: monsoon (tropical deciduous) forests" t={T} appear={s.start - 0.3}>
        <MapView left={34} top={92} w={740} h={700} view={{ lon0: 63, lon1: 99, lat0: 5, lat1: 37.6 }}>{(u) => (
          <>
            <path d={`M${X(63)} ${Y(23.44)} L${X(99)} ${Y(23.44)}`} stroke={C.sunDark} strokeWidth={6 * u} strokeDasharray={`${16 * u} ${10 * u}`} />
            <Label x={X(64)} y={Y(23.44) - 14 * u} size={26 * u} anchor="start" color={C.sunDark} sc>Tropic of Cancer</Label>
            {[[80, 22], [82, 20], [85, 23], [77, 15], [74, 19], [84, 21.5], [79, 24.5]].map(([lo, la], i) => { const [x, y] = P(lo, la); return <circle key={i} cx={x} cy={y} r={14 * u} fill="#5e9b45" opacity={0.75 * sm(dc + i * 0.15, dc + 0.4 + i * 0.15, T)} stroke={C.ink} strokeWidth={2 * u} />; })}
          </>)}
        </MapView>
        <Svg>
          <Tree kind="teak" x={930} y={470} s={1} bare={bare} o={sm(dc - 0.2, dc + 0.3, T)} /><Tree kind="decid" x={1170} y={470} s={1} bare={bare} o={sm(dc, dc + 0.4, T)} />
          {txt(930, 520, "Teak", 36, C.ink, "middle", sm(cue("india2", "teak"), cue("india2", "teak") + 0.3, T))}{txt(1170, 520, "Sal", 36, C.ink, "middle", sm(cue("india2", "sal"), cue("india2", "sal") + 0.3, T))}
        </Svg>
        <Line T={T} at={sh} x={800} y={130} w={560} size={34} color={C.soft}>leaves fall in the dry season to save water</Line>
        <Big T={T} at={fr} x={800} y={560} size={100}>21.76%</Big>
        <Line T={T} at={fr + 0.3} x={800} y={680} w={560} size={30} color={C.soft}>forest cover, ISFR 2023 · forest + tree cover 25.17%</Line>
      </Card>
    </>
  );
};
export const Poles = ({ T }: SP) => {
  const s = segOf("poles"), te = cue("poles", "temperate"), fr = cue("poles", "frigid");
  const zones = [{ n: "Equatorial · rainforest", k: "rain" as const, lat: "0°", hl: false }, { n: "Tropical · deciduous / thorn", k: "acacia" as const, lat: "10–30°", hl: false },
    { n: "Temperate · oak, pine, deodar", k: "conifer" as const, lat: "30–66.5°", hl: true, at: te }, { n: "Frigid · tundra", k: "tundra" as const, lat: "66.5–90°", hl: true, at: fr }];
  return (
    <>
      <Host t={T - s.start} T={T} mood="think" />
      <Card title="Vegetation changes with latitude" t={T} appear={s.start - 0.3}>
        <Svg>
          {zones.map((z, i) => { const x = 70 + i * 315, on = z.at ? sm(z.at - 0.2, z.at + 0.3, T) : 0.4 + 0.6 * sm(s.start, s.start + 0.5, T);
            return (<g key={i} opacity={0.35 + 0.65 * on}>
              <rect x={x} y={110} width={295} height={560} rx={16} fill={z.hl && on > 0.5 ? "#fff6dc" : "#fffaf0"} stroke={C.ink} strokeWidth={4} />
              <Tree kind={z.k} x={x + 148} y={530} s={z.k === "rain" ? 0.85 : 1} />
              {txt(x + 148, 170, z.lat, 40, C.red)}{txt(x + 148, 610, z.n.split(" · ")[0], 36, C.ink, "middle", 1, true)}{txt(x + 148, 652, z.n.split(" · ")[1], 26, C.soft)}
            </g>); })}
          <Arrow pts={[[90, 705], [1290, 705]]} k={sm(s.start + 0.3, s.start + 1.3, T)} color={C.rain} w={6} head={20} smooth={false} />
          {txt(690, 752, "away from the Equator → lower Sun → cooler", 28, C.soft)}
        </Svg>
      </Card>
    </>
  );
};
export const Outro = ({ T }: SP) => {
  const s = segOf("outro");
  return (
    <>
      <Host t={T - s.start} T={T} mood="wave" />
      <Card title="Remember" t={T} appear={s.start - 0.3}>
        <Line T={T} at={cue("outro", "imaginary")} x={110} y={170} w={1200} size={54}>WHAT · imaginary lines locate places and set time</Line>
        <Line T={T} at={cue("outro", "tilt")} x={110} y={320} w={1200} size={54} color={TAGCOL.WHY}>WHY · Earth's 23.5° tilt creates solstices and seasons</Line>
        <Line T={T} at={cue("outro", "latitude")} x={110} y={470} w={1200} size={54} color={TAGCOL.HOW}>HOW · latitude (Sun angle + air movement) decides climate and forests</Line>
      </Card>
    </>
  );
};
export { lerp, FONT_SC };
