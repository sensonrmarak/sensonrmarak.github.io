import { Composition } from "remotion";
import { Main } from "./Main";
import { StyleScene } from "./Styles";
import { CastTest } from "./moss/CastTest";
import { MossVideo, MOSS_FRAMES } from "./moss/MossVideo";
import { MossAIEdit } from "./moss/MossAIEdit";
import { ZonesLesson, ZONES_FRAMES, ZONES_FPS } from "./zones/ZonesLesson";
import { UpscBranded, brandedFrames } from "./brand/UpscBrand";
import { MonsoonLesson, MONSOON_FRAMES, MONSOON_FPS } from "./monsoon/MonsoonLesson";
const MonsoonBranded = () => <UpscBranded contentFrames={MONSOON_FRAMES} variant="ink" corner="bottom-right"><MonsoonLesson /></UpscBranded>;
const ZonesLessonBranded = () => <UpscBranded contentFrames={ZONES_FRAMES} variant="ink" corner="bottom-right"><ZonesLesson /></UpscBranded>;

export const RemotionRoot = () => (
  <>
  <Composition id="Main" component={Main} durationInFrames={150} fps={30} width={1920} height={1080} />
  {(["lowpoly","diorama","paper","toon","night","autumn","winter","clay","pastel","sunset"] as const).map((s) => (
    <Composition key={s} id={"Style-" + s} component={StyleScene} defaultProps={{ style: s }} durationInFrames={150} fps={30} width={1280} height={720} />
  ))}
  <Composition id="MossCast" component={CastTest} durationInFrames={1} fps={24} width={1080} height={1080} />
  <Composition id="MossSilverTrail" component={MossVideo} durationInFrames={MOSS_FRAMES} fps={24} width={1080} height={1920} />
  <Composition id="MossAIEdit" component={MossAIEdit} durationInFrames={MOSS_FRAMES} fps={24} width={1080} height={1920} />
  <Composition id="ZonesLesson" component={ZonesLesson} durationInFrames={ZONES_FRAMES} fps={ZONES_FPS} width={2560} height={1440} />
  <Composition id="ZonesLessonBranded" component={ZonesLessonBranded} durationInFrames={brandedFrames(ZONES_FRAMES, ZONES_FPS)} fps={ZONES_FPS} width={2560} height={1440} />
  <Composition id="MonsoonLesson" component={MonsoonLesson} durationInFrames={MONSOON_FRAMES} fps={MONSOON_FPS} width={2560} height={1440} />
  <Composition id="UpscMonsoon" component={MonsoonBranded} durationInFrames={brandedFrames(MONSOON_FRAMES, MONSOON_FPS)} fps={MONSOON_FPS} width={2560} height={1440} />
  </>
);
