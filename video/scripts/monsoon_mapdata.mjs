// Builds src/monsoon/mapdata.json: India's outline (state paths from @svg-maps/india, CC BY 4.0) and the surrounding
// land (Natural Earth 50m via world-atlas), in one Mercator projection calibrated to the India SVG:
//   x = K * rad(lon - 68.17),  y = K * (M(37.10) - M(lat)),  K = 1199.55,  M(p) = ln tan(45deg + p/2)
import fs from "node:fs";
import { feature } from "topojson-client";
const K = 1199.55, LON0 = 68.17, LAT0 = 37.10;
const M = p => Math.log(Math.tan(Math.PI / 4 + p * Math.PI / 360));
const X = lon => K * (lon - LON0) * Math.PI / 180, Y = lat => K * (M(LAT0) - M(lat));
const svg = fs.readFileSync(process.argv[2], "utf8");
const india = [...svg.matchAll(/id="([a-z]+)"[\s\S]*?d="([^"]+)"/g)].map(m => ({ id: m[1], d: m[2] }));
const topo = JSON.parse(fs.readFileSync("node_modules/world-atlas/land-50m.json", "utf8"));
const land = feature(topo, topo.objects.land);
const BB = [45, -25, 115, 48];   // lon/lat window kept
const paths = [];
for (const f of land.features) {
  const polys = f.geometry.type === "Polygon" ? [f.geometry.coordinates] : f.geometry.coordinates;
  for (const poly of polys) {
    const ring = poly[0];
    if (!ring.some(([lo, la]) => lo > BB[0] && lo < BB[2] && la > BB[1] && la < BB[3])) continue;
    const pts = ring.map(([lo, la]) => [Math.max(BB[0] - 5, Math.min(BB[2] + 5, lo)), Math.max(BB[1] - 5, Math.min(BB[3] + 5, la))]);
    paths.push("M" + pts.map(([lo, la]) => `${X(lo).toFixed(1)} ${Y(la).toFixed(1)}`).join("L") + "Z");
  }
}
fs.writeFileSync("src/monsoon/mapdata.json", JSON.stringify({ K, LON0, LAT0, india, land: paths }));
console.log("india paths", india.length, "land rings", paths.length);
