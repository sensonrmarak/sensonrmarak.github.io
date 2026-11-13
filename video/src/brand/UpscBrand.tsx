import { AbsoluteFill, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

/* UPSC Animated channel branding, reusable in every video.
   <UpscBranded fps={30} endSeconds={4}> ...video... </UpscBranded> adds:
     - a faint logo watermark in a bottom corner for the whole video
     - an end card (the channel banner) after the video's last frame
   Logos: brand/upsc_logo_chalk.png (white chalk, for dark videos), brand/upsc_logo_ink.png (dark ink, for light videos). */

export type Corner = "bottom-right" | "bottom-left";
export type LogoVariant = "chalk" | "ink" | "seal";   // "seal" = the full-colour Modus & Raison roundel

export const Watermark = ({ corner = "bottom-right", variant = "ink", opacity = 0.2, size = 0.075 }:
  { corner?: Corner; variant?: LogoVariant; opacity?: number; size?: number }) => {
  const { width, height } = useVideoConfig();
  const f = useCurrentFrame();
  const px = Math.round(Math.min(width, height) * size * 1.45);   // about 11% of the short side
  const margin = Math.round(Math.min(width, height) * 0.03);
  const fadeIn = interpolate(f, [15, 45], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <Img src={staticFile(variant === "seal" ? "brand/modus_raison_seal.png" : `brand/upsc_logo_${variant}.png`)} style={{
        position: "absolute", width: px, height: px, bottom: margin,
        [corner === "bottom-right" ? "right" : "left"]: margin, opacity: opacity * fadeIn, objectFit: "contain",
      }} />
    </AbsoluteFill>
  );
};

export const EndCard = () => {
  const f = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const a = interpolate(f, [0, fps * 0.8], [0, 1], { extrapolateRight: "clamp" });
  const out = interpolate(f, [durationInFrames - fps * 0.6, durationInFrames - 1], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const zoom = interpolate(f, [0, durationInFrames], [1.0, 1.05]);
  return (
    <AbsoluteFill style={{ background: "black" }}>
      <Img src={staticFile("brand/upsc_banner.png")} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${zoom})`, opacity: a * out }} />
    </AbsoluteFill>
  );
};

/** End card for the Modus & Raison channel: the roundel on its own cream ground, with a subscribe line. */
export const SealEndCard = () => {
  const f = useCurrentFrame();
  const { fps, durationInFrames, height } = useVideoConfig();
  const a = interpolate(f, [0, fps * 0.8], [0, 1], { extrapolateRight: "clamp" });
  const out = interpolate(f, [durationInFrames - fps * 0.6, durationInFrames - 1], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const zoom = interpolate(f, [0, durationInFrames], [0.97, 1.02]);
  return (
    <AbsoluteFill style={{ background: "#fdf7ec", alignItems: "center", justifyContent: "center" }}>
      <div style={{ opacity: a * out, display: "flex", flexDirection: "column", alignItems: "center", transform: `scale(${zoom})` }}>
        <Img src={staticFile("brand/modus_raison_full.png")} style={{ width: height * 0.74, height: height * 0.74 }} />
        <div style={{ fontFamily: "Georgia, 'Times New Roman', serif", fontSize: height * 0.045, color: "#14233f", letterSpacing: height * 0.006, marginTop: height * 0.01 }}>SUBSCRIBE FOR MORE</div>
      </div>
    </AbsoluteFill>
  );
};

/** Wrap a video: its own frames first, then the end card; the watermark sits over the video (not the end card). */
export const UpscBranded = ({ children, contentFrames, endSeconds = 4, corner = "bottom-right", variant = "ink", opacity = 0.2, size }:
  { children: React.ReactNode; contentFrames: number; endSeconds?: number; corner?: Corner; variant?: LogoVariant; opacity?: number; size?: number }) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: "black" }}>
      <Sequence durationInFrames={contentFrames}>
        {children}
        <Watermark corner={corner} variant={variant} opacity={opacity} size={size} />
      </Sequence>
      <Sequence from={contentFrames} durationInFrames={Math.round(endSeconds * fps)}>{variant === "seal" ? <SealEndCard /> : <EndCard />}</Sequence>
    </AbsoluteFill>
  );
};
export const brandedFrames = (contentFrames: number, fps: number, endSeconds = 4) => contentFrames + Math.round(endSeconds * fps);
