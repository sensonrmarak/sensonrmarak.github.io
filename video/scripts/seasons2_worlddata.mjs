// World land (Natural Earth 50m via world-atlas) in plate carree units: x = 10*lon, y = -10*lat  -> src/seasons2/world.json
import fs from "node:fs";
import { feature } from "topojson-client";
const topo = JSON.parse(fs.readFileSync("node_modules/world-atlas/land-50m.json", "utf8"));
const land = feature(topo, topo.objects.land), out = [];
for (const f of land.features) for (const poly of (f.geometry.type === "Polygon" ? [f.geometry.coordinates] : f.geometry.coordinates)) {
  const ring = poly[0]; if (ring.length < 8) continue;
  let d = "", prev = null;
  for (const [lo, la] of ring) { if (prev && Math.abs(lo - prev) > 180) d += "Z"; d += (d === "" || d.endsWith("Z") ? "M" : "L") + (lo * 10).toFixed(0) + " " + (-la * 10).toFixed(0); prev = lo; }
  out.push(d + "Z");
}
fs.writeFileSync("src/seasons2/world.json", JSON.stringify(out)); console.log(out.length, "rings");
