import React from "react";
import { C, FONT, FONT_SC, sm } from "./kit";

/* WHAT / WHY / HOW question badge, drawn in the empty paper above the host (x 36-448, y 96-~430),
   never over the card (x >= 470) or the caption strip (y >= 905). */
export type Tag = "WHAT" | "WHY" | "HOW";
export type QA = { tag: Tag; q: string; src?: string };
export const TAGCOL: Record<Tag, string> = { WHAT: "#2f6d9a", WHY: "#b8432f", HOW: "#2f7d3a" };

export const QBadge = ({ T, start, end, qa }: { T: number; start: number; end: number; qa?: QA }) => {
  if (!qa) return null;
  const k = sm(start - 0.25, start + 0.35, T) * (1 - sm(end - 0.1, end + 0.25, T)), col = TAGCOL[qa.tag];
  return (
    <div style={{ position: "absolute", left: 36, top: 96, width: 412, opacity: k, transform: `translateY(${(1 - k) * 14}px)` }}>
      <div style={{ display: "inline-block", fontFamily: FONT_SC, fontSize: 46, lineHeight: 1.1, color: "#fff", background: col, border: `3px solid ${C.ink}`, borderRadius: 16, padding: "2px 24px 4px", transform: "rotate(-2deg)" }}>{qa.tag}?</div>
      <div style={{ fontFamily: FONT, fontSize: 40, lineHeight: 1.12, color: C.ink, marginTop: 16 }}>{qa.q}</div>
      {qa.src && <div style={{ display: "inline-block", marginTop: 18, fontFamily: FONT, fontSize: 25, lineHeight: 1.15, color: C.soft, border: `2px dashed ${C.soft}`, borderRadius: 10, padding: "4px 12px" }}>Source: {qa.src}</div>}
    </div>
  );
};

export const MONSOON_QA: Record<string, QA> = {
  sw: { tag: "WHAT", q: "What is the southwest monsoon?", src: "IMD normal onset dates (2020)" },
  share: { tag: "WHY", q: "Why does it matter so much?", src: "IMD rainfall statistics" },
  arabian: { tag: "HOW", q: "How does it spread across India?", src: "IMD · NCERT Geography" },
  bengal: { tag: "HOW", q: "How does it spread across India?", src: "IMD · NCERT Geography" },
  ne: { tag: "WHAT", q: "What is the northeast monsoon?", src: "IMD" },
  tn: { tag: "WHY", q: "Why does Tamil Nadu get rain in winter?", src: "IMD Chennai (RMC)" },
  heat: { tag: "WHY", q: "Why do winds blow from sea to land?", src: "IMD · NCERT Geography" },
  coriolis: { tag: "HOW", q: "How do the winds turn southwest?", src: "NCERT Geography" },
  itcz: { tag: "WHAT", q: "What is the monsoon trough?", src: "IMD" },
  jet: { tag: "HOW", q: "How does the monsoon burst?", src: "NCERT Geography" },
  ocean: { tag: "HOW", q: "How do the oceans change it?", src: "IMD ENSO / IOD bulletins" },
  lpa: { tag: "WHAT", q: "What counts as a normal monsoon?", src: "IMD, LPA 1971–2020" },
  extreme: { tag: "HOW", q: "How is the rain changing?", src: "IITM Pune, Roxy et al. (2017)" },
  erratic: { tag: "WHAT", q: "What about its timing?", src: "IMD normal withdrawal dates" },
  cyclone: { tag: "WHY", q: "Why more storms over the Arabian Sea?", src: "IITM Pune, Deshpande et al. (2021)" },
  track: { tag: "HOW", q: "How does India track the monsoon?", src: "IMD · ISRO" },
  impact: { tag: "WHY", q: "Why does this matter?", src: "IMD" },
};

export const SEASONS_QA: Record<string, QA> = {
  lat: { tag: "WHAT", q: "What is latitude?", src: "NCERT · Survey of India" },
  lon: { tag: "WHAT", q: "What is longitude?", src: "NCERT · Survey of India" },
  equator: { tag: "WHAT", q: "What makes the Equator special?", src: "NASA Earth Fact Sheet" },
  parallels: { tag: "WHY", q: "Why are some parallels special?", src: "NASA" },
  india: { tag: "WHAT", q: "Where does the Tropic of Cancer cross India?", src: "Survey of India" },
  time: { tag: "HOW", q: "How does longitude set our clocks?", src: "CSIR-National Physical Laboratory" },
  tilt: { tag: "WHAT", q: "What is Earth's tilt?", src: "NASA" },
  orbit: { tag: "HOW", q: "How does the orbit create seasons?", src: "NASA" },
  distance: { tag: "WHY", q: "Why is it not about distance?", src: "NASA (perihelion / aphelion)" },
  june: { tag: "WHAT", q: "What happens at the summer solstice?", src: "NASA · IMD sunrise-sunset data" },
  dec: { tag: "WHAT", q: "What happens at the winter solstice?", src: "NASA · IMD sunrise-sunset data" },
  equinox: { tag: "WHAT", q: "What is an equinox?", src: "NASA" },
  noon: { tag: "HOW", q: "How do solstices change the heat we feel?", src: "Sun angle = 90° − latitude ± 23.44°" },
  eqzone: { tag: "WHY", q: "Why is the Equator hot and wet all year?", src: "NCERT · NASA Earth Observatory" },
  rainforest: { tag: "HOW", q: "How does this shape the forests?", src: "NCERT · Forest Survey of India" },
  tropics: { tag: "WHY", q: "Why do deserts lie near the tropics?", src: "NASA Earth Observatory" },
  desert: { tag: "HOW", q: "How do desert plants survive?", src: "NCERT Geography" },
  india2: { tag: "WHAT", q: "What forests does India have?", src: "Forest Survey of India, ISFR 2023" },
  poles: { tag: "HOW", q: "How does vegetation change towards the poles?", src: "NCERT Geography" },
};
