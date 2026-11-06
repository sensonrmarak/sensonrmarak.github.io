import { Composition } from "remotion";
import { Main } from "./Main";
import { StyleScene } from "./Styles";
import { CastTest } from "./moss/CastTest";
import { MossVideo, MOSS_FRAMES } from "./moss/MossVideo";

export const RemotionRoot = () => (
  <>
  <Composition id="Main" component={Main} durationInFrames={150} fps={30} width={1920} height={1080} />
  {(["lowpoly","diorama","paper","toon","night","autumn","winter","clay","pastel","sunset"] as const).map((s) => (
    <Composition key={s} id={"Style-" + s} component={StyleScene} defaultProps={{ style: s }} durationInFrames={150} fps={30} width={1280} height={720} />
  ))}
  <Composition id="MossCast" component={CastTest} durationInFrames={1} fps={24} width={1080} height={1080} />
  <Composition id="MossSilverTrail" component={MossVideo} durationInFrames={MOSS_FRAMES} fps={24} width={1080} height={1920} />
  </>
);
