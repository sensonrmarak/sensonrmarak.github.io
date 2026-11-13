// Pre-renders the seasons video's world-land layers to PNG (2x) into public/seasons2/static/.
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
const browserExecutable = process.env.REMOTION_BROWSER || null;
const out = path.resolve("public/seasons2/static"); fs.mkdirSync(out, { recursive: true });
const tmp = "/tmp/claude-0/statics2"; fs.mkdirSync(tmp, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const CARD = { x: 470, y: 74 };
const g = v => String(v).replace(/-/g, "m");
const bases = [{ view: [-100, 160, -45, 45], box: [34, 92, 1322, 640] }, { view: [-90, 130, -35, 35], box: [34, 92, 900, 560] }];
for (const [i, b] of bases.entries()) {
  const layer = "world" + i, inputProps = { layer };
  const composition = await selectComposition({ serveUrl, id: "SeasonsStatics", inputProps, browserExecutable });
  const raw = `${tmp}/${layer}.png`;
  await renderStill({ composition, serveUrl, output: raw, inputProps, scale: 2, imageFormat: "png", browserExecutable });
  const k = (4 / 3) * 2, [x, y, w, h] = [CARD.x + b.box[0], CARD.y + b.box[1], b.box[2], b.box[3]].map(v => Math.round(v * k));
  const name = `world_${b.view.map(g).join("_")}_${b.box[2]}x${b.box[3]}.png`;
  execFileSync("python3", ["-c", `from PIL import Image; Image.open("${raw}").crop((${x},${y},${x + w},${y + h})).save("${out}/${name}")`]);
  console.log("wrote", name);
}
