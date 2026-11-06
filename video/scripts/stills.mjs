// Render several stills from one bundle: node scripts/stills.mjs <compId> <outDir> <frame> [frame...]
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";
const [comp, out, ...frames] = process.argv.slice(2);
const browserExecutable = process.env.REMOTION_BROWSER || null;
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const composition = await selectComposition({ serveUrl, id: comp, browserExecutable, chromiumOptions: { gl: "swangle" } });
for (const f of frames) {
  const t = Date.now();
  await renderStill({ composition, serveUrl, frame: Number(f), output: `${out}/f${f}.png`, browserExecutable, chromiumOptions: { gl: "swangle" }, scale: 0.5 });
  console.log("frame", f, Date.now() - t, "ms");
}
