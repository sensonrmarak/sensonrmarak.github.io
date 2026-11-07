import { AbsoluteFill, Audio, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import timeline from "./timeline.json";

/* "Seasons and Heat Zones" lesson video: screen recordings of the two Colorfigures models (recorded in time with Lily's
   narration), gentle zooms on the key moments, section labels, captions, title and closing cards. */
type Word = { text: string; start: number; end: number };
const TL = timeline as { total: number; segments: { start: number; end: number; text: string; words: Word[] }[] };
export const ZONES_FPS = 30;
export const ZONES_FRAMES = Math.round(127.5 * ZONES_FPS);
const CUT = TL.segments[5].start;            // recording 2 (heat zones model) starts here

const INK = "#231e16", PAPER = "#f2efe7", SUN = "#f4b829";
const FRED = "Fredoka", MONO = "ui-monospace, Menlo, monospace";
if (typeof document !== "undefined") {
  const h = delayRender("fonts");
  new FontFace(FRED, `url(${staticFile("fonts/Fredoka.woff2")})`, { weight: "300 700" }).load()
    .then((f) => { document.fonts.add(f); continueRender(h); });
}
const sm = (a: number, b: number, t: number) => interpolate(t, [a, b], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: (x) => x * x * (3 - 2 * x) });

/* zoom-ins: [start, end, scale, originX%, originY%] in narration seconds */
const ZOOMS: [number, number, number, number, number][] = [
  [26.2, 34.5, 1.3, 58, 30], [37.2, 46.8, 1.3, 64, 32],
  [89.0, 94.0, 1.28, 60, 28], [103.3, 118.4, 1.25, 64, 30],
];
const BASE = 1.1;                             // the 2K footage is framed a little tighter than the page
const Footage = () => {
  const { fps } = useVideoConfig();
  const T = useCurrentFrame() / fps;
  let s = BASE, ox = 55, oy = 42;
  for (const [a, b, k, x, y] of ZOOMS) {
    const w = sm(a, a + 1.2, T) * (1 - sm(b - 1.2, b, T));
    if (w > 0) { s = BASE + (k - BASE) * w; ox = 55 + (x - 55) * w; oy = 42 + (y - 42) * w; }
  }
  const v: React.CSSProperties = { width: "100%", height: "100%", objectFit: "cover" };
  return (
    <AbsoluteFill style={{ transform: `scale(${s})`, transformOrigin: `${ox}% ${oy}%` }}>
      <OffthreadVideo src={staticFile("zones/footage_2k.mp4")} style={v} muted />
    </AbsoluteFill>
  );
};

/* section chip, top centre (the figure's own buttons sit top-left and top-right) */
const SECTIONS: [number, string][] = [[TL.segments[1].start, "Lesson 1 · Why Earth's tilt causes seasons"],
  [CUT, "Lesson 2 · The three heat zones"], [TL.segments[8].start, "Lesson 3 · Which zone is a city in?"]];
const Section = () => {
  const T = useCurrentFrame() / useVideoConfig().fps;
  const cur = [...SECTIONS].reverse().find(([t]) => T >= t - 0.2);
  if (!cur || T > cur[0] + 3.4) return null;                 // shown briefly so it never covers the graphics for long
  const o = sm(cur[0] - 0.2, cur[0] + 0.4, T) * (1 - sm(cur[0] + 2.8, cur[0] + 3.4, T));
  return (
    <AbsoluteFill style={{ alignItems: "center", top: 26, opacity: o }}>
      <div style={{ fontFamily: FRED, fontWeight: 600, fontSize: 30, color: PAPER, background: INK, padding: "10px 26px", borderRadius: 999 }}>{cur[1]}</div>
    </AbsoluteFill>
  );
};

/* captions: a few words at a time, the spoken word highlighted */
const PAGES: { words: Word[]; start: number; end: number }[] = [];
TL.segments.forEach((seg, si) => {
  if (si === 0 || si === 9) return;            // title and closing cards carry these lines
  let cur: Word[] = [];
  const flush = () => { if (cur.length) PAGES.push({ words: cur, start: cur[0].start, end: cur[cur.length - 1].end }); cur = []; };
  seg.words.forEach((w) => { cur.push(w); if (/[.!?:]$/.test(w.text) || (/,$/.test(w.text) && cur.length > 3) || cur.length >= 8) flush(); });
  flush();
});
const Captions = () => {
  const T = useCurrentFrame() / useVideoConfig().fps;
  const i = PAGES.findIndex((p, k) => T >= p.start - 0.05 && T < Math.min(p.end + 0.5, PAGES[k + 1]?.start ?? 1e9));
  if (i < 0) return null;
  const p = PAGES[i];
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 70 }}>
      <div style={{ maxWidth: 1500, textAlign: "center", fontFamily: FRED, fontWeight: 600, fontSize: 52, lineHeight: 1.35, color: INK,
        background: "rgba(251,249,243,0.92)", border: `3px solid ${INK}`, borderRadius: 22, padding: "14px 30px" }}>
        {p.words.map((w, k) => {
          const on = T >= w.start && T < (p.words[k + 1]?.start ?? p.end + 0.5);
          return <span key={k} style={{ background: on ? SUN : "transparent", borderRadius: 10, padding: "0 6px", margin: "0 1px" }}>{w.text}</span>;
        })}
      </div>
    </AbsoluteFill>
  );
};

const Card = ({ from, to, children }: { from: number; to: number; children: React.ReactNode }) => {
  const T = useCurrentFrame() / useVideoConfig().fps;
  const o = sm(from, from + 0.8, T) * (1 - sm(to - 0.8, to, T));
  if (o <= 0) return null;
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 80, opacity: o }}>
      <div style={{ textAlign: "center", fontFamily: FRED, color: INK, background: "rgba(251,249,243,0.95)", border: `3px solid ${INK}`,
        borderRadius: 28, padding: "26px 56px", transform: `translateY(${(1 - o) * 20}px)` }}>{children}</div>
    </AbsoluteFill>
  );
};

export const ZonesLesson = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const f = useCurrentFrame();
  const fade = interpolate(f, [0, 15], [1, 0], { extrapolateRight: "clamp" }) + interpolate(f, [durationInFrames - 40, durationInFrames - 1], [0, 1], { extrapolateLeft: "clamp" });
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <Footage />
      <Section />
      <Captions />
      <Card from={0.4} to={TL.segments[0].end + 0.4}>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: 4, textTransform: "uppercase", opacity: 0.7 }}>A lesson in three parts</div>
        <div style={{ fontWeight: 700, fontSize: 84, lineHeight: 1.05, marginTop: 8 }}>Seasons and Heat Zones</div>
        <div style={{ fontWeight: 500, fontSize: 38, marginTop: 10 }}>Why Earth has seasons, and why some places are hot all year</div>
      </Card>
      <Card from={TL.segments[9].start - 0.2} to={127.5}>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: 4, textTransform: "uppercase", opacity: 0.7 }}>Remember</div>
        <div style={{ fontWeight: 700, fontSize: 66, lineHeight: 1.15, marginTop: 8 }}>The <span style={{ background: SUN, borderRadius: 12, padding: "0 10px" }}>tilt</span> makes the seasons.</div>
        <div style={{ fontWeight: 700, fontSize: 66, lineHeight: 1.15 }}><span style={{ background: "#a8d66f", borderRadius: 12, padding: "0 10px" }}>Latitude</span> decides your heat zone.</div>
      </Card>
      <AbsoluteFill style={{ background: PAPER, opacity: Math.min(1, fade) }} />
      <Audio src={staticFile("zones/soundtrack.wav")} />
    </AbsoluteFill>
  );
};
