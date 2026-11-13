import { Composition } from "remotion";
import { Main } from "./Main";
import { StyleScene } from "./Styles";
import { CastTest } from "./moss/CastTest";
import { MossVideo, MOSS_FRAMES } from "./moss/MossVideo";
import { MossAIEdit } from "./moss/MossAIEdit";
import { ZonesLesson, ZONES_FRAMES, ZONES_FPS } from "./zones/ZonesLesson";
import { UpscBranded, brandedFrames } from "./brand/UpscBrand";
import { MonsoonLesson, MONSOON_FRAMES, MONSOON_FPS } from "./monsoon/MonsoonLesson";
import { MonsoonStatics } from "./monsoon/Statics";
import { SeasonsLesson, SEASONS_FRAMES, SEASONS_FPS } from "./seasons2/SeasonsLesson";
import { SeasonsStatics } from "./seasons2/Statics";
import { ThumbSeasons, ThumbMonsoon } from "./thumbs/Thumbs";
import { WbLesson, WB_FRAMES, WB_FPS } from "./wb/WbLesson";
const WbBranded = () => <UpscBranded contentFrames={WB_FRAMES} variant="ink" corner="bottom-right" opacity={0.35}><WbLesson /></UpscBranded>;
const SeasonsBranded = () => <UpscBranded contentFrames={SEASONS_FRAMES} variant="ink" corner="bottom-right"><SeasonsLesson /></UpscBranded>;
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
  <Composition id="SeasonsLesson" component={SeasonsLesson} durationInFrames={SEASONS_FRAMES} fps={SEASONS_FPS} width={2560} height={1440} />
  <Composition id="UpscSeasons" component={SeasonsBranded} durationInFrames={brandedFrames(SEASONS_FRAMES, SEASONS_FPS)} fps={SEASONS_FPS} width={2560} height={1440} />
  <Composition id="SeasonsStatics" component={SeasonsStatics} durationInFrames={1} fps={30} width={2560} height={1440} defaultProps={{ layer: "world0" }} />
  <Composition id="ThumbSeasons" component={ThumbSeasons} durationInFrames={1} fps={30} width={1920} height={1080} />
  <Composition id="ThumbMonsoon" component={ThumbMonsoon} durationInFrames={1} fps={30} width={1920} height={1080} />
  <Composition id="WbLesson" component={WbLesson} durationInFrames={WB_FRAMES} fps={WB_FPS} width={3840} height={2160} />
  <Composition id="UpscWbMonsoon" component={WbBranded} durationInFrames={brandedFrames(WB_FRAMES, WB_FPS)} fps={WB_FPS} width={3840} height={2160} />
  <Composition id="MonsoonStatics" component={MonsoonStatics} durationInFrames={1} fps={30} width={2560} height={1440} defaultProps={{ layer: "paper" }} />
  </>
);
