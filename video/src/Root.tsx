import { Composition } from "remotion";
import { Main } from "./Main";
import { StyleScene } from "./Styles";

export const RemotionRoot = () => (
  <>
  <Composition id="Main" component={Main} durationInFrames={150} fps={30} width={1920} height={1080} />
  {(["lowpoly","diorama","paper","toon","night"] as const).map((s) => (
    <Composition key={s} id={"Style-" + s} component={StyleScene} defaultProps={{ style: s }} durationInFrames={150} fps={30} width={1280} height={720} />
  ))}
  </>
);
