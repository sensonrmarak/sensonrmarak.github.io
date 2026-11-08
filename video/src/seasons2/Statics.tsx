import { AbsoluteFill } from "remotion";
import { CARD, Defs } from "../monsoon/kit";
import { StaticMode } from "../monsoon/map";
import { WorldView, WORLD_BOX, WORLD_VIEW } from "./parts";

/* static world-land layers for the seasons video (rendered at --scale=2 and cropped by scripts/seasons2_statics.mjs) */
export const WORLD_BASES = [
  { box: WORLD_BOX, view: WORLD_VIEW },
  { box: { left: 34, top: 92, w: 900, h: 560 }, view: { lon0: -90, lon1: 130, lat0: -35, lat1: 35 } },
];
export const SeasonsStatics = ({ layer }: { layer: string }) => (
  <StaticMode.Provider value={true}>
    <AbsoluteFill style={{ background: "transparent" }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, transform: "scale(1.3333333)", transformOrigin: "0 0" }}>
        <Defs />
        {(() => { const b = WORLD_BASES[+layer.slice(5)]; return (
          <div style={{ position: "absolute", left: CARD.x, top: CARD.y, width: CARD.w, height: CARD.h }}><WorldView {...b.box} view={b.view} /></div>); })()}
      </div>
    </AbsoluteFill>
  </StaticMode.Provider>
);
