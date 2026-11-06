import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { continueRender, delayRender } from "remotion";
import { Shot1, Shot2, Shot3, Shot4, Shot5, Shot6, Shot7, Shot8 } from "./shots";
import { TL, shotEnd, shotStart, smooth, wt } from "./util";

// Fonts are bundled locally (public/fonts) so rendering needs no network access. Both are OFL licensed (Google Fonts).
const FRED = "Fredoka", LORA = "Lora";
if (typeof document !== "undefined") {
  const handle = delayRender("Loading fonts");
  Promise.all([
    new FontFace(FRED, `url(${staticFile("fonts/Fredoka.woff2")})`, { weight: "300 700" }).load(),
    new FontFace(LORA, `url(${staticFile("fonts/Lora-Italic.woff2")})`, { weight: "400 700", style: "italic" }).load(),
  ]).then((faces) => { faces.forEach((f) => document.fonts.add(f)); continueRender(handle); });
}

const SHOTS = [Shot1, Shot2, Shot3, Shot4, Shot5, Shot6, Shot7, Shot8];

/* ---------------------------------------------------------------- captions */
type Word = { text: string; start: number; end: number };
const PAGES: { words: Word[]; start: number; end: number }[] = [];
TL.segments.forEach((seg, si) => {
  if (si === 8) return; // the moral card carries the last line
  let cur: Word[] = [];
  const flush = () => {
    if (cur.length) PAGES.push({ words: cur, start: cur[0].start, end: cur[cur.length - 1].end });
    cur = [];
  };
  seg.words.forEach((w) => {
    cur.push(w);
    const len = cur.reduce((a, x) => a + x.text.length + 1, 0);
    if (/[.!?]"?$|\.\.\.$/.test(w.text) || (/[,:]"?$/.test(w.text) && len > 14) || cur.length >= 5) flush();
  });
  flush();
});

const Captions = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const T = f / fps;
  const page = PAGES.find((p, i) => T >= p.start - 0.05 && T < Math.min(p.end + 0.45, PAGES[i + 1]?.start ?? 1e9));
  if (!page) return null;
  const pop = interpolate(T - page.start, [0, 0.12], [0.85, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", top: 1330 }}>
      <div style={{
        transform: `scale(${pop})`, maxWidth: 900, textAlign: "center", fontFamily: FRED, fontWeight: 700, fontSize: 74,
        lineHeight: 1.15, color: "white", WebkitTextStroke: "14px #2b1d14", paintOrder: "stroke fill",
        textShadow: "0 6px 14px rgba(0,0,0,0.35)",
      }}>
        {page.words.map((w, i) => {
          const on = T >= w.start && T < (page.words[i + 1]?.start ?? page.end + 0.45);
          return (
            <span key={i} style={{ color: on ? "#ffd166" : "white", display: "inline-block", margin: "0 10px",
              transform: on ? "translateY(-4px)" : undefined }}>{w.text.replace(/^"|"$/g, (m) => m)}</span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/* ---------------------------------------------------------------- title + moral card */
const LanternDot = ({ size = 34 }: { size?: number }) => (
  <span style={{ display: "inline-block", width: size, height: size * 1.15, borderRadius: "45% 45% 50% 50%", verticalAlign: "middle",
    background: "radial-gradient(circle at 50% 40%, #fff2c2, #ffb347 55%, #e0742a)", boxShadow: "0 0 28px 8px rgba(255,179,71,0.55)",
    margin: "0 16px" }} />
);

const Title = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const T = f / fps;
  const o = smooth(0.4, 1.3, T) * (1 - smooth(5.4, 6.4, T));
  return (
    <AbsoluteFill style={{ alignItems: "center", top: 210, opacity: o }}>
      <div style={{ fontFamily: FRED, fontWeight: 600, fontSize: 46, letterSpacing: 10, color: "#fff7e6",
        textShadow: "0 3px 10px rgba(80,40,10,0.6)", textTransform: "uppercase" }}>
        <LanternDot size={28} />Oakenvale Tales<LanternDot size={28} />
      </div>
      <div style={{ fontFamily: LORA, fontStyle: "italic", fontWeight: 600, fontSize: 92, color: "white", marginTop: 18, textAlign: "center",
        lineHeight: 1.05, textShadow: "0 4px 18px rgba(80,40,10,0.65)", transform: `translateY(${(1 - smooth(0.4, 1.4, T)) * 20}px)` }}>
        Moss and the<br />Silver Trail
      </div>
    </AbsoluteFill>
  );
};

const MoralCard = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const T = f / fps;
  const seg = TL.segments[8];
  const a = smooth(seg.start - 0.3, seg.start + 0.4, T);
  const l1 = smooth(wt(8, "slow") - 0.15, wt(8, "slow") + 0.3, T);
  const l2 = smooth(wt(8, "Every") - 0.15, wt(8, "Every") + 0.3, T);
  const logo = smooth(seg.end + 0.2, seg.end + 0.9, T);
  return (
    <AbsoluteFill style={{ opacity: a }}>
      <AbsoluteFill style={{ background: "linear-gradient(rgba(10,14,35,0.55), rgba(10,14,35,0.15) 55%, rgba(10,14,35,0))" }} />
      <AbsoluteFill style={{ alignItems: "center", top: 250 }}>
        <div style={{ width: 900, padding: "56px 40px", borderRadius: 48, background: "rgba(20,28,58,0.72)", border: "4px solid #e8c36a",
          boxShadow: "0 0 60px rgba(255,190,90,0.35)", textAlign: "center", transform: `scale(${0.92 + a * 0.08})` }}>
          <div style={{ fontFamily: FRED, fontWeight: 600, fontSize: 40, letterSpacing: 6, color: "#e8c36a", textTransform: "uppercase" }}>
            Remember, little friends
          </div>
          <div style={{ fontFamily: FRED, fontWeight: 700, fontSize: 96, color: "white", marginTop: 26, opacity: l1,
            transform: `translateY(${(1 - l1) * 18}px)` }}>Slow is not small.</div>
          <div style={{ fontFamily: LORA, fontStyle: "italic", fontWeight: 600, fontSize: 64, color: "#ffe3a3", marginTop: 22, lineHeight: 1.2,
            opacity: l2, transform: `translateY(${(1 - l2) * 18}px)` }}>Every gift can light<br />someone's way.</div>
        </div>
        <div style={{ marginTop: 60, opacity: logo, fontFamily: FRED, fontWeight: 600, fontSize: 54, letterSpacing: 8, color: "#fff7e6",
          textTransform: "uppercase", textShadow: "0 0 24px rgba(255,190,90,0.6)" }}>
          <LanternDot />Oakenvale Tales<LanternDot />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ---------------------------------------------------------------- main */
export const MossVideo = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const f = useCurrentFrame();
  const fade = Math.min(interpolate(f, [0, 12], [1, 0], { extrapolateRight: "clamp" }),
    1) + interpolate(f, [durationInFrames - 30, durationInFrames - 1], [0, 1], { extrapolateLeft: "clamp" });
  return (
    <AbsoluteFill style={{ background: "black" }}>
      {SHOTS.map((S, i) => {
        const from = Math.round(shotStart(i) * fps), to = Math.round(shotEnd(i) * fps);
        return <Sequence key={i} from={from} durationInFrames={to - from} name={`Shot ${i + 1}`}><S /></Sequence>;
      })}
      <Sequence durationInFrames={Math.round(7 * fps)} name="Title"><Title /></Sequence>
      <Captions />
      <MoralCard />
      <AbsoluteFill style={{ background: "black", opacity: Math.min(1, fade) }} />
      <Audio src={staticFile("moss/soundtrack.wav")} />
    </AbsoluteFill>
  );
};

export const MOSS_FRAMES = Math.ceil(TL.total * TL.fps);
