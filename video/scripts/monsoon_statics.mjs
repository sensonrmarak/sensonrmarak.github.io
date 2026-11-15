// Pre-renders the monsoon video's static layers to PNG (2x) and crops them into public/monsoon/static/.
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
const browserExecutable = process.env.REMOTION_BROWSER || null;
const out = path.resolve("public/monsoon/static"); fs.mkdirSync(out, { recursive: true });
const tmp = "/tmp/claude-0/statics"; fs.mkdirSync(tmp, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const CARD = { x: 470, y: 74, w: 1390, h: 806 };
const g = v => String(v).replace(/-/g, "m");
const bases = [
  { view: [63, 99, 5, 37.6], box: [34, 92, 740, 700] }, { view: [52, 102, -20, 32], box: [34, 92, 900, 700] },
  { view: [55, 100, -14, 36], box: [34, 92, 900, 700] }, { view: [55, 105, 4, 45], box: [34, 92, 900, 700] },
  { view: [52, 82, 4, 28], box: [34, 92, 900, 700] }];
const jobs = [{ layer: "paper", scale: 1, crop: null, name: "paper.png" },
  { layer: "card", scale: 2, crop: [CARD.x - 20, CARD.y - 20, CARD.w + 40, CARD.h + 40], name: "card.png" },
  ...bases.map((b, i) => ({ layer: "map" + i, scale: 2, crop: [CARD.x + b.box[0], CARD.y + b.box[1], b.box[2], b.box[3]],
    name: `map_${b.view.map(g).join("_")}_${b.box[2]}x${b.box[3]}.png` }))];
for (const j of jobs) {
  const composition = await selectComposition({ serveUrl, id: "MonsoonStatics", inputProps: { layer: j.layer }, browserExecutable });
  const raw = `${tmp}/${j.layer}.png`;
  await renderStill({ composition, serveUrl, output: raw, inputProps: { layer: j.layer }, scale: j.scale, imageFormat: "png", browserExecutable });
  if (!j.crop) { fs.copyFileSync(raw, `${out}/${j.name}`); }
  else {
    const k = (4 / 3) * j.scale, [x, y, w, h] = j.crop.map(v => Math.round(v * k));
    execFileSync("python3", ["-c", `from PIL import Image; Image.open("${raw}").crop((${x},${y},${x + w},${y + h})).save("${out}/${j.name}")`]);
  }
  console.log("wrote", j.name);
}
