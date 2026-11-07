import { AbsoluteFill } from "remotion";
import { CARD, CardFrame, Defs, Paper } from "./kit";
import { MapView, StaticMode } from "./map";
import { MAP_BASES } from "./scenes";

/* Pre-renders the static layers of the monsoon video (drawn at 2560x1440, rendered with --scale=2):
   layer "paper" | "card" | "map<i>". scripts/monsoon_statics.sh crops them to public/monsoon/static/. */
export const MonsoonStatics = ({ layer }: { layer: string }) => (
  <StaticMode.Provider value={true}>
    <AbsoluteFill style={{ background: "transparent" }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, transform: "scale(1.3333333)", transformOrigin: "0 0" }}>
        <Defs />
        {layer === "paper" && <Paper />}
        {layer === "card" && <div style={{ position: "absolute", left: CARD.x, top: CARD.y, width: CARD.w, height: CARD.h }}><CardFrame /></div>}
        {layer.startsWith("map") && (() => { const b = MAP_BASES[+layer.slice(3)]; return (
          <div style={{ position: "absolute", left: CARD.x, top: CARD.y, width: CARD.w, height: CARD.h }}><MapView {...b.box} view={b.view} /></div>); })()}
      </div>
    </AbsoluteFill>
  </StaticMode.Provider>
);
