import { B, Board, Builder, G, K, MapP, R, circD, cloudD, curveD, dropsD, geo, indiaD, lineD, headD, makeBoard, peaksD, polyD, rectD, sunD } from "./engine";

/* One board per narration segment. Coordinates are board units (1800 x 860). */
const title = (b: Builder, s: string, x = 50, y = 78, size = 54) => { b.t(b.start - 0.2, x, y, s, { size }); b.ul(null, x, y + 16, Math.min(1500, s.length * size * 0.42), { c: K }); };
const full = (b: Builder) => b.cam(b.end - 1.5, 0, 0, 1800);
const dot = (b: Builder, at: number | string | null, p: number[], c = R, r = 9) => b.p(at, circD(p[0], p[1], r), { c, w: 4, dur: 0.25, fill: c, fo: 1 });
const cloud = (b: Builder, at: number | string | null, x: number, y: number, s: number, rain = true) => { b.p(at, cloudD(x, y, s), { c: K, w: 3.5, dur: 0.6 }); if (rain) b.p(null, dropsD(x - s * 0.1, y + s * 0.55, s), { c: B, w: 3.5, dur: 0.35 }); };
const arrowC = (pts: number[][]) => { const n = pts.length; return curveD(pts) + headD(pts[n - 2][0], pts[n - 2][1], pts[n - 1][0], pts[n - 1][1], 18); };

export const BOARDS: Board[] = [
  makeBoard("hook", (b) => {
    b.t(b.start, 60, 100, "One wind decides...", { size: 70 }); b.ul(null, 60, 120, 560);
    b.p("one", arrowC([[70, 330], [200, 250], [330, 330], [470, 270]]), { c: B, w: 6, dur: 0.7 });
    b.p(null, arrowC([[70, 420], [200, 340], [330, 420], [470, 360]]), { c: B, w: 6, dur: 0.6 });
    b.p(null, arrowC([[70, 510], [200, 430], [330, 510], [470, 450]]), { c: B, w: 6, dur: 0.6 });
    b.t("price", 560, 290, "₹  the price of your food", { size: 46, c: R });
    b.t("interest", 560, 380, "%  the interest on your loan", { size: 46, c: B });
    b.t("income", 560, 470, "the income of ~46% of India's workers", { size: 46, c: G });
    b.cam("calendar", 500, 120, 1300);
    b.box("calendar", 1330, 170, 380, 330, { w: 5 }); b.ln(null, 1330, 250, 1710, 250, { w: 5 });
    b.t("2025", 1520, 232, "MAY 2025", { size: 44, anchor: "middle" });
    b.t("24th", 1520, 400, "24", { size: 150, c: R, anchor: "middle", dur: 0.6 });
    b.t("earliest", 1330, 560, "Kerala onset: earliest", { size: 36 }); b.t(null, 1330, 606, "since 2009 (IMD)", { size: 36 });
    b.cam("monsoon", 0, 0, 1800);
    b.t("monsoon", 900, 730, "THE INDIAN MONSOON", { size: 104, c: B, anchor: "middle", dur: 1.2 }); b.ul(null, 470, 752, 860, { c: R, w: 7 });
    b.t("stay", 900, 825, "by the end: draw the whole system from memory", { size: 38, anchor: "middle" });
  }),

  makeBoard("intro", (b) => {
    title(b, "What is the monsoon?");
    b.cam("arabic", 0, 60, 1400);
    b.t("arabic", 60, 210, "mausim", { size: 80, c: B, dur: 0.8 }); b.t("meaning", 330, 205, '= "season of winds"  (Arabic)', { size: 40 });
    b.box("reversal", 80, 330, 330, 190, { c: R, w: 5 }); b.t(null, 245, 440, "LAND", { size: 46, c: R, anchor: "middle" });
    b.p(null, curveD([[520, 500], [580, 480], [640, 500], [700, 480], [760, 500], [820, 480], [880, 500]]), { c: B, w: 5 }); b.t(null, 700, 560, "OCEAN", { size: 46, c: B, anchor: "middle" });
    b.p(null, arrowC([[860, 400], [650, 360], [430, 400]]), { c: B, w: 6 }); b.t(null, 650, 345, "summer: sea → land", { size: 34, c: B, anchor: "middle" });
    b.p(null, arrowC([[430, 300], [650, 260], [860, 300]]), { c: R, w: 6 }); b.t(null, 650, 250, "winter: land → sea", { size: 34, c: R, anchor: "middle" });
    b.t("heated", 80, 590, "heats up fast", { size: 34, c: R }); b.t("cooler", 560, 620, "stays cooler", { size: 34, c: B });
    b.t("reversal", 80, 700, "= seasonal reversal of winds", { size: 44 });
    b.cam("75", 650, 120, 1150);
    b.t("75", 1080, 330, "≈ 75%", { size: 150, c: R, dur: 0.8 }); b.t(null, 1085, 400, "of India's annual rainfall (IMD)", { size: 38 });
    b.t("strong", 1085, 520, "strong → bumper crops, full reservoirs", { size: 38, c: G });
    b.t("weak", 1085, 600, "weak → drought", { size: 38, c: R });
    full(b);
  }),

  makeBoard("phases", (b) => {
    title(b, "Two phases");
    const m1: MapP = { x: 560, y: 240, s: 12 }, m2: MapP = { x: 1450, y: 240, s: 12 }, g1 = geo(m1), g2 = geo(m2);
    b.ln(null, 900, 130, 900, 800, { c: K, w: 3, dash: "10 10" });
    b.cam("phase", 0, 80, 1150);
    b.num("phase", 80, 200, 1, B); b.t(null, 115, 214, "Southwest monsoon  (wet)", { size: 46, c: B });
    b.p(null, indiaD(m1), { dur: 1.6, w: 3.5 });
    b.t("june", 60, 300, "June – September", { size: 40 });
    [[62, 9, 73, 15], [62, 14, 72.5, 19.5], [64, 5, 75.5, 10.5]].forEach(([a, c, d, e], i) => b.p(i ? null : "sea", arrowC([g1(a, c), g1((a + d) / 2, (c + e) / 2 - 1), g1(d, e)]), { c: B, w: 5, dur: 0.4 }));
    b.t(null, 60, 370, "winds: sea → land", { size: 38, c: B });
    b.t("three", 60, 440, "≈ 75% of the year's rain", { size: 38 });
    b.t("ghats", 60, 510, "most on: Western Ghats", { size: 38 }); b.t(null, 60, 560, "+ the Northeast", { size: 38 });
    cloud(b, null, g1(74, 15)[0] + 4, g1(74, 15)[1] - 30, 26); cloud(b, null, g1(92, 26)[0], g1(92, 26)[1] - 36, 26);
    b.cam(b.q("phase", 1), 650, 100, 1150);
    b.num(b.q("phase", 1), 960, 200, 2, R); b.t(null, 995, 214, "Northeast (retreating) monsoon", { size: 46, c: R });
    b.p(null, indiaD(m2), { dur: 1.6, w: 3.5 });
    b.t("october", 950, 300, "October – December", { size: 40 });
    [[90, 31, 80, 24], [94, 22, 84, 16], [86, 34, 76, 27]].forEach(([a, c, d, e], i) => b.p(i ? null : "land", arrowC([g2(a, c), g2((a + d) / 2, (c + e) / 2 + 1), g2(d, e)]), { c: R, w: 5, dur: 0.4 }));
    b.t(null, 950, 370, "winds: land → sea", { size: 38, c: R });
    b.t("dry", 950, 440, "mostly dry, but...", { size: 38 });
    b.t("48", 950, 510, "Tamil Nadu: ≈ 48% of its", { size: 38, c: B }); b.t(null, 950, 560, "annual rain (IMD)", { size: 38, c: B });
    cloud(b, null, g2(80, 11.5)[0], g2(80, 11.5)[1] - 28, 24);
    b.t("andhra", 950, 630, "+ coastal Andhra", { size: 38 });
    full(b);
  }),

  makeBoard("drivers", (b) => {
    const m: MapP = { x: 630, y: 110, s: 22 }, g = geo(m);
    title(b, "Why? A giant sea breeze", 40, 70, 50);
    b.p("breeze", indiaD(m), { dur: 2.4, w: 4 });
    b.cam("first", 0, 60, 1560);
    b.num("first", 60, 180, 1, R); b.t(null, 95, 194, "Differential heating", { size: 44, c: R });
    b.p("summer", sunD(480, 300, 34), { c: R, w: 4, dur: 0.8 });
    b.circ("low", g(72.5, 27)[0], g(72.5, 27)[1], 34, { c: R, w: 5 }); b.t(null, g(72.5, 27)[0], g(72.5, 27)[1] + 16, "L", { size: 50, c: R, anchor: "middle" });
    b.t("thar", 50, 300, "LOW pressure: Thar", { size: 38, c: R }); b.t(null, 50, 348, "Desert + northern plains", { size: 38, c: R });
    b.circ("high", g(66.5, 9)[0], g(66.5, 9)[1], 34, { c: B, w: 5 }); b.t(null, g(66.5, 9)[0], g(66.5, 9)[1] + 16, "H", { size: 50, c: B, anchor: "middle" });
    b.t(null, 50, 640, "HIGH pressure:", { size: 38, c: B }); b.t(null, 50, 688, "cooler Indian Ocean", { size: 38, c: B });
    b.p("rushes", arrowC([g(67.5, 11), g(68.5, 17), g(71.5, 24)]), { c: B, w: 6, dur: 0.7 }); b.p(null, arrowC([g(69, 9), g(75, 12), g(78, 20)]), { c: B, w: 6, dur: 0.6 });
    b.t(null, 50, 470, "air: HIGH → LOW,", { size: 38 }); b.t(null, 50, 518, "carrying moisture", { size: 38 });
    b.cam("second", 240, 100, 1560);
    b.num("second", 1250, 180, 2, G); b.t(null, 1285, 194, "ITCZ shifts north", { size: 44, c: G });
    b.p("belt", lineD(650, 812, 1170, 812), { c: G, w: 5, dash: "14 12", dur: 0.6 }); b.t(null, 1200, 824, "winter: near the Equator", { size: 34, c: G });
    b.p("shifts", arrowC([[1100, 795], [1120, 600], [g(86, 25.5)[0] + 30, g(86, 25.5)[1] + 40]]), { c: G, w: 5, dur: 0.7 });
    b.p(null, curveD([g(73, 28), g(78, 27.3), g(83, 25.8), g(88, 24.8)]), { c: G, w: 6, dash: "14 12", dur: 0.7 });
    b.t("ganga", 1240, 262, "July: over the Ganga plain,", { size: 36, c: G }); b.t(null, 1240, 308, "pulls the winds in", { size: 36, c: G });
    b.num("third", 1250, 420, 3, K); b.t(null, 1285, 434, "Himalayas = high wall", { size: 44 });
    b.p("wall", peaksD(g(75, 31)[0], g(75, 30.2)[1], g(96, 0)[0] - g(75, 0)[0], 34, 9), { w: 4.5, dur: 1.0 });
    b.t("escaping", 1240, 502, "blocks escape to Central Asia", { size: 36 });
    b.p("rise", arrowC([g(88, 24.5), g(89.5, 26.5), g(90, 29.5)]), { c: B, w: 5 }); cloud(b, null, g(92, 31.6)[0] + 30, g(92, 31.6)[1], 30);
    b.t(null, 1240, 570, "forces air to rise →", { size: 36, c: B }); b.t(null, 1240, 616, "orographic rain over India", { size: 36, c: B });
    full(b);
  }),

  makeBoard("branches", (b) => {
    const m: MapP = { x: 250, y: 110, s: 22 }, g = geo(m);
    title(b, "It splits into two branches", 900, 90, 50);
    b.p(b.start + 0.3, indiaD(m), { dur: 2.2, w: 4 });
    dot(b, "tip", g(76.9, 8.6)); b.t(null, g(76.9, 8.6)[0] + 20, g(76.9, 8.6)[1] + 34, "Kerala", { size: 32, c: R });
    b.num("arabian", 930, 220, 1, B); b.t(null, 965, 234, "Arabian Sea branch", { size: 46, c: B });
    [[61, 7, 73, 14.5], [61, 12, 72.5, 18.5], [63, 16.5, 72.3, 21]].forEach(([a, c, d, e]) => b.p(null, arrowC([g(a, c), g((a + d) / 2, (c + e) / 2 - 0.8), g(d, e)]), { c: B, w: 6, dur: 0.45 }));
    b.p("ghats", polyD([g(73.6, 20.5), g(74.5, 19.6), g(73.9, 18.6), g(74.8, 17.6), g(74.3, 16.6), g(75.3, 15.5), g(74.9, 14.4), g(75.9, 13.3), g(75.7, 12.2), g(76.8, 11.1), g(76.7, 10.1)]), { w: 4, dur: 0.8 });
    b.t(null, g(77.4, 16.5)[0], g(77.4, 16.5)[1], "W. Ghats", { size: 30 });
    cloud(b, "soaks", g(71.2, 16.5)[0], g(71.2, 16.5)[1], 30);
    b.t(null, 930, 300, "hits the Western Ghats,", { size: 38 }); b.t(null, 930, 348, "soaks the west coast", { size: 38 });
    b.num("bay", 930, 450, 2, G); b.t(null, 965, 464, "Bay of Bengal branch", { size: 46, c: G });
    b.p(null, arrowC([g(87, 7), g(89.5, 14), g(90.5, 20), g(91.5, 24.6)]), { c: G, w: 6, dur: 0.8 });
    b.p("turns", arrowC([g(90.5, 25.6), g(86, 26.2), g(81.5, 27.2), g(77.6, 28.6)]), { c: G, w: 6, dur: 0.9 });
    b.t("northeast", 930, 530, "up into the Northeast, then", { size: 38 }); b.t(null, 930, 578, "west along the Ganga plain", { size: 38 });
    b.circ("meet", g(76, 29.3)[0], g(76, 29.3)[1], 42, { c: R, w: 5 });
    b.t(null, 930, 690, "branches meet over NW India", { size: 40, c: R });
    full(b);
  }),

  makeBoard("shifts", (b) => {
    const m: MapP = { x: 700, y: 170, s: 17 }, g = geo(m);
    title(b, "Is it changing?  Yes.");
    b.cam("scientists", 0, 60, 1250);
    b.t("threefold", 60, 330, "3×", { size: 190, c: R, dur: 0.8 });
    b.t("widespread", 60, 420, "widespread extreme rain", { size: 38 }); b.t(null, 60, 468, "events, central India", { size: 38 });
    b.t("1950", 60, 536, "1950 → 2015", { size: 44, c: B });
    b.t(null, 60, 596, "IITM Pune (Roxy et al., 2017)", { size: 30 });
    b.p("depressions", indiaD(m), { dur: 1.6, w: 3.5 });
    b.p("peninsula", arrowC([g(81, 23.5), g(80.3, 19.5), g(78.3, 14.5)]), { c: B, w: 6, dur: 0.7 });
    b.t(null, g(84.5, 15)[0], g(84.5, 15)[1], "rain shifting", { size: 30, c: B }); b.t(null, g(84.5, 15)[0], g(84.5, 15)[1] + 38, "south", { size: 30, c: B });
    b.cam("marathwada", 550, 130, 1250);
    b.circ("marathwada", g(77, 19.6)[0], g(77, 19.6)[1], 30, { c: R, w: 5, fill: R, fo: 0.2 });
    b.ln(null, g(77, 19.6)[0] + 30, g(77, 19.6)[1] - 14, 1240, 250, { c: R, w: 3 });
    b.t(null, 1250, 240, "Marathwada + Vidarbha:", { size: 36, c: R }); b.t(null, 1250, 286, "repeated droughts", { size: 36, c: R });
    b.t("nino", 1250, 440, "El Niño", { size: 64, c: R });
    b.t("warming", 1250, 506, "warm Pacific →", { size: 36 }); b.t(null, 1250, 552, "weaker monsoon winds", { size: 36 });
    b.t("2023", 1250, 650, "2023: only 94%", { size: 48, c: B }); b.t(null, 1250, 700, "of normal rain (IMD)", { size: 36 });
    full(b);
  }),

  makeBoard("onset", (b) => {
    title(b, "How IMD declares the onset", 40, 70, 50);
    b.t("shower", 760, 70, "not the first shower!", { size: 40, c: R }); b.p(null, lineD(1090, 58, 760, 60), { c: R, w: 3, dur: 0.3 });
    b.t("10th", 1170, 70, "after 10 May: 3 tests, together", { size: 38, c: B });
    [40, 620, 1200].forEach((x) => b.box(null, x, 120, 560, 700, { w: 3, dur: 0.5 }));
    b.cam("one", 0, 105, 1500);
    b.num("one", 80, 172, 1, B); b.t(null, 115, 186, "Rainfall", { size: 46, c: B });
    for (let i = 0; i < 14; i++) b.p(i ? null : "stations", circD(100 + (i % 7) * 66, 270 + Math.floor(i / 7) * 66, 16), { c: i < 9 ? B : K, w: 3.5, dur: 0.12, fill: i < 9 ? B : undefined, fo: 0.9 });
    b.t("60", 70, 420, "≥ 60% of 14 stations", { size: 38 }); b.t(null, 70, 466, "(at least 9)", { size: 34 });
    b.t("2.5", 70, 550, "≥ 2.5 mm each,", { size: 40, c: B }); b.t("two", 70, 600, "2 days in a row", { size: 40, c: B });
    b.t("kerala", 70, 700, "Kerala · Lakshadweep ·", { size: 32 }); b.t(null, 70, 742, "coastal Karnataka", { size: 32 });
    b.cam(b.q("two", 1), 150, 105, 1500);
    b.num(b.q("two", 1), 660, 172, 2, G); b.t(null, 695, 186, "Wind", { size: 46, c: G });
    b.ar("deep", 700, 560, 700, 260, { c: K, w: 4 }); b.t(null, 670, 600, "height", { size: 28 });
    [300, 370, 440, 510].forEach((y, i) => b.ar(i ? null : "westerly", 740, y, 900 + i * 22, y, { c: G, w: 5, dur: 0.25 }));
    b.t("600", 960, 330, "westerlies", { size: 36, c: G }); b.t(null, 960, 376, "up to 600 hPa", { size: 36, c: G });
    b.t("15", 660, 690, "15 to 20 knots", { size: 44, c: G }); b.t(null, 660, 740, "near the surface (925 hPa)", { size: 32 });
    b.cam(b.q("three", 1), 300, 105, 1500);
    b.num(b.q("three", 1), 1240, 172, 3, R); b.t(null, 1275, 186, "Cloud (OLR)", { size: 46, c: R });
    b.p("outgoing", curveD([[1240, 560], [1400, 520], [1560, 520], [1720, 560]]), { w: 4 }); b.t(null, 1480, 600, "Earth", { size: 30, anchor: "middle" });
    [1300, 1380].forEach((x) => b.ar(null, x, 510, x, 300, { c: R, w: 4, dur: 0.3 })); b.t(null, 1255, 280, "heat escapes", { size: 28, c: R });
    cloud(b, null, 1590, 420, 62, false); [1540, 1610].forEach((x) => b.ar(null, x, 510, x, 462, { c: R, w: 4, dur: 0.2, head: 10 }));
    b.p("isro", rectD(1560, 200, 50, 34) + ` M1500 206 L1556 206 L1556 228 L1500 228 Z M1614 206 L1670 206 L1670 228 L1614 228 Z`, { w: 3.5, c: B, dur: 0.6 });
    b.t(null, 1500, 276, "INSAT-3D (ISRO)", { size: 30, c: B });
    b.t("200", 1240, 690, "OLR < 200 W/m²", { size: 46, c: R });
    b.t("thick", 1240, 742, "= thick, tall rain clouds", { size: 34 });
    full(b);
  }),

  makeBoard("agri", (b) => {
    title(b, "Monsoon runs farming: 2 crop seasons", 50, 76, 50);
    b.ln(null, 900, 130, 900, 640, { w: 3, dash: "10 10" });
    b.cam("kharif", 0, 60, 1050);
    b.t("kharif", 60, 200, "KHARIF", { size: 70, c: G }); b.t(null, 300, 196, "(monsoon crops)", { size: 34 });
    cloud(b, null, 720, 190, 44);
    b.t("sown", 60, 280, "sow:  June – July", { size: 40 }); b.t("harvested", 60, 340, "harvest:  Sept – Oct", { size: 40 });
    b.t("water", 60, 410, "water need:  HIGH", { size: 40, c: B });
    b.t("rice", 60, 490, "rice · maize · cotton", { size: 38, c: G }); b.t("soybean", 60, 540, "soybean · sugarcane · groundnut", { size: 38, c: G });
    b.cam("rabi", 750, 60, 1050);
    b.t("rabi", 950, 200, "RABI", { size: 70, c: R }); b.t(null, 1120, 196, "(winter crops)", { size: 34 });
    b.t(b.q("sown", 1), 950, 280, "sow:  Oct – Nov", { size: 40 }); b.t(b.q("harvested", 1), 950, 340, "harvest:  March – April", { size: 40 });
    b.t("moisture", 950, 410, "soil moisture + western disturbances", { size: 36, c: B });
    b.t("wheat", 950, 490, "wheat · barley · mustard", { size: 38, c: R }); b.t("gram", 950, 540, "gram · peas", { size: 38, c: R });
    b.cam("depends", 200, 190, 1400);
    b.p("depends", arrowC([[520, 600], [900, 680], [1280, 600]]), { c: B, w: 6, dur: 0.8 });
    b.t("fills", 900, 740, "monsoon fills reservoirs + groundwater → irrigates rabi", { size: 38, c: B, anchor: "middle" });
    b.t("spell", 900, 810, "a dry spell in July can wipe out kharif seedlings", { size: 38, c: R, anchor: "middle" });
    full(b);
  }),

  makeBoard("wettest", (b) => {
    title(b, "Where does it rain the most?");
    b.cam("meghalaya", 0, 150, 1100);
    b.p("khasi", polyD([[60, 620], [420, 620], [520, 560], [600, 440], [660, 330], [720, 300], [800, 330], [860, 420]]), { w: 5, dur: 1.0 });
    b.t(null, 700, 420, "Khasi Hills", { size: 34 }); b.t("funnel", 610, 470, "(a funnel)", { size: 30 });
    [[80, 520, 380, 520], [80, 580, 400, 580]].forEach(([x1, y1, x2, y2], i) => b.ar(i ? null : "bay", x1, y1, x2, y2, { c: B, w: 6, dur: 0.4 }));
    b.t(null, 80, 480, "Bay of Bengal winds", { size: 32, c: B });
    b.t("bangladesh", 120, 668, "plains of Bangladesh", { size: 32 });
    b.p("rise", arrowC([[430, 560], [520, 480], [590, 340], [640, 250]]), { c: B, w: 6, dur: 0.7 });
    b.t("orographic", 250, 300, "orographic lift", { size: 42, c: G });
    cloud(b, null, 700, 210, 60);
    b.cam("11,870", 0, 330, 1100);
    b.t("11,870", 60, 760, "Mawsynram ≈ 11,870 mm a year", { size: 50, c: R }); b.t("cherrapunji", 60, 818, "Cherrapunji close behind", { size: 36 });
    b.cam("western", 700, 160, 1100);
    b.t("western", 1000, 200, "Western Ghats", { size: 48, c: G }); b.ul(null, 1000, 214, 280, { c: G });
    const bar = (at: string, y: number, name: string, mm: number, c: string) => { b.t(at, 1000, y, name, { size: 36 }); b.p(null, rectD(1000, y + 14, mm * 0.058, 30), { c, w: 3.5, fill: c, fo: 0.35, dur: 0.5 }); b.t(null, 1010 + mm * 0.058, y + 40, `≈ ${mm.toLocaleString("en-US")} mm`, { size: 34, c }); };
    bar("amboli", 290, "Amboli (Maharashtra)", 7500, B); bar("agumbe", 410, "Agumbe (Karnataka): 'Cherrapunji of the south'", 7200, B); bar("mahabaleshwar", 530, "Mahabaleshwar: source of the Krishna", 5600, B);
    b.t(null, 1000, 640, "for scale:  Mawsynram", { size: 32, c: R }); b.p(null, rectD(1000, 652, 11870 * 0.058, 30), { c: R, w: 3.5, fill: R, fo: 0.35, dur: 0.5 });
    full(b);
  }),

  makeBoard("timetable", (b) => {
    const m: MapP = { x: 100, y: 100, s: 23 }, g = geo(m);
    title(b, "The monsoon timetable", 800, 80, 50); b.t(null, 1330, 80, "(IMD normal dates)", { size: 34, c: B });
    b.p(b.start + 0.2, indiaD(m), { dur: 2.0, w: 4 });
    const row = (at: string, y: number, date: string, place: string, c = B) => { b.t(at, 810, y, date, { size: 40, c }); b.t(null, 1010, y, place, { size: 38 }); };
    dot(b, "22nd", g(92.7, 11.7), B); row("22nd", 170, "22 May", "Andaman & Nicobar Islands");
    dot(b, "first", g(76.6, 9.6), B); row("first", 226, "1 June", "Kerala");
    dot(b, "11th", g(72.9, 19.1), B); dot(b, null, g(88.3, 22.6), B); row("11th", 282, "11 June", "Mumbai · Kolkata");
    b.p("20th", curveD([g(70.5, 21.5), g(76, 22.5), g(82, 24.5), g(87.5, 26.5)]), { c: B, w: 4, dash: "12 10", dur: 0.6 }); row("20th", 338, "20 June", "central India");
    dot(b, "delhi", g(77.2, 28.6), B); row("delhi", 394, "~27 June", "Delhi");
    b.p("8th", arrowC([g(76, 26), g(73.5, 27), g(70.8, 27.3)]), { c: B, w: 5 }); row("8th", 450, "8 July", "whole country covered", G);
    b.t("reverses", 810, 560, "Withdrawal", { size: 48, c: R }); b.ul(null, 810, 574, 210, { c: R });
    b.p("17th", arrowC([g(71, 27.8), g(75, 25.5), g(79.5, 21.5)]), { c: R, w: 6, dur: 0.7 }); row("17th", 636, "17 Sept", "begins: west Rajasthan", R);
    row("15th", 692, "15 Oct", "complete", R);
    b.p("crossing", arrowC([g(90, 19), g(86, 15.5), g(81, 12.5)]), { c: G, w: 6, dur: 0.7 });
    b.t("become", 810, 770, "→ over the Bay: Northeast monsoon", { size: 38, c: G });
    full(b);
  }),

  makeBoard("harvest", (b) => {
    title(b, "Storing the rain: 4 months of water for 12", 50, 76, 50);
    b.t("traditionally", 60, 160, "Traditional", { size: 42, c: G });
    // taanka
    b.p("taankas", polyD([[90, 290], [210, 210], [330, 290]]) + " " + rectD(110, 290, 200, 90), { w: 4, dur: 0.7 });
    b.p(null, polyD([[330, 290], [370, 290], [370, 400]]), { c: B, w: 4, dur: 0.3 }); b.p(null, rectD(340, 400, 150, 70), { c: B, w: 4, fill: B, fo: 0.25, dur: 0.5 });
    b.ln(null, 60, 392, 520, 392, { w: 3 });
    b.t(null, 60, 520, "Taanka (Rajasthan):", { size: 34 }); b.t("underground", 60, 562, "underground rooftop-rain tank", { size: 32 });
    // johad
    b.p("johads", curveD([[660, 250], [740, 300], [830, 290], [900, 340]]), { c: B, w: 5 }); b.p(null, curveD([[820, 420], [900, 370], [990, 370], [1070, 420]]), { w: 7, dur: 0.5 });
    b.p(null, curveD([[850, 400], [940, 350], [1040, 400]], true), { c: B, w: 3, fill: B, fo: 0.25, dur: 0.4 });
    [900, 950, 1000].forEach((x, i) => b.ar(i ? null : "recharge", x, 430, x, 470, { c: B, w: 3.5, dur: 0.2, head: 10 }));
    b.t(null, 660, 520, "Johad / check dam:", { size: 34 }); b.t(null, 660, 562, "holds runoff, recharges groundwater", { size: 32 });
    // bamboo
    b.p("bamboo", lineD(1260, 240, 1480, 300) + " " + lineD(1480, 300, 1700, 360), { c: G, w: 7, dur: 0.6 }); b.p(null, dropsD(1500, 330, 30, 3) + " " + dropsD(1690, 390, 30, 3), { c: B, w: 4, dur: 0.3 });
    b.p(null, peaksD(1240, 250, 120, 60, 2), { w: 3.5 });
    b.t(null, 1240, 520, "Bamboo drip (Northeast):", { size: 34 }); b.t("drop", 1240, 562, "spring water, drop by drop", { size: 32 });
    b.t("modern", 60, 650, "Modern cities", { size: 42, c: B });
    b.p(b.q("rooftop", 1), rectD(330, 620, 110, 150), { w: 4 }); b.p(null, polyD([[440, 630], [500, 630], [500, 720]]), { c: B, w: 4, dur: 0.3 }); b.p(null, rectD(480, 720, 44, 40), { c: R, w: 3.5, dur: 0.3 }); b.p(null, polyD([[502, 760], [502, 790], [560, 790]]), { c: B, w: 4, dur: 0.3 }); b.p(null, rectD(560, 760, 50, 60), { c: B, w: 3.5, fill: B, fo: 0.25, dur: 0.3 });
    b.t("filter", 640, 700, "Rooftop RWH:", { size: 34 }); b.t(null, 640, 742, "roof → filter → recharge well", { size: 32 });
    b.p("permeable", lineD(1150, 700, 1500, 700) + " " + [1190, 1260, 1330, 1400, 1470].map((x) => `M${x} 690 L${x} 710`).join(" "), { w: 4, dur: 0.5 }); [1220, 1300, 1380].forEach((x, i) => b.ar(i ? null : "lakes", x, 712, x, 760, { c: B, w: 3.5, dur: 0.2, head: 10 }));
    b.t("sponge", 1150, 820, "Permeable pavements + lakes = sponge city", { size: 32 });
  }),

  makeBoard("economy", (b) => {
    title(b, "Weak monsoon: the chain reaction");
    const bx = (at: string | number, x: number, y: number, l1: string, l2: string, c: string) => { b.box(at, x, y, 390, 150, { c, w: 4.5, dur: 0.45 }); b.t(null, x + 195, y + 62, l1, { size: 36, c, anchor: "middle" }); b.t(null, x + 195, y + 112, l2, { size: 30, anchor: "middle" }); };
    b.cam("follow", 0, 80, 1500);
    bx("90", 40, 190, "Deficient monsoon", "< 90% of the LPA", R);
    b.ar("kharif", 440, 265, 485, 265, { w: 5 }); bx("kharif", 495, 190, "Kharif sowing falls", "less rice, pulses, oilseeds", K);
    b.ar("food", 895, 265, 940, 265, { w: 5 }); bx("food", 950, 190, "Food prices rise", "pulses · rice · vegetables", R);
    b.cam("largest", 300, 80, 1500);
    b.ar("largest", 1350, 265, 1385, 265, { w: 5 }); bx("reserve", 1395, 190, "RBI keeps rates high", "food = largest part of CPI", B);
    b.ar("46", 1590, 345, 1590, 465, { w: 5 }); bx("46", 1395, 475, "Rural incomes fall", "≈ 46% of workers farm (PLFS)", R);
    b.ar("sales", 1385, 550, 1350, 550, { w: 5 }); bx("sales", 950, 475, "Sales slow down", "tractors · 2-wheelers · FMCG", K);
    b.cam("pump", 0, 140, 1500);
    b.ar("pump", 940, 550, 895, 550, { w: 5 }); bx("pump", 495, 475, "More groundwater pumping", "→ power demand rises", B);
    b.t("demand", 40, 760, "one bad season → farms → prices → interest rates → factories", { size: 40, c: G });
    full(b);
  }),

  makeBoard("climate", (b) => {
    const m: MapP = { x: 1180, y: 150, s: 19 }, g = geo(m);
    title(b, "Climate change: same total, new pattern", 50, 76, 50);
    b.cam("total", 0, 60, 1200);
    b.t("87", 60, 180, "LPA = 87 cm", { size: 56, c: B }); b.t(null, 400, 176, "(June–Sept, 1971–2020, IMD)", { size: 32 });
    b.t("pattern", 60, 270, "earlier: steady rain", { size: 34 });
    b.ln(null, 60, 400, 760, 400, { w: 3 }); for (let i = 0; i < 20; i++) b.p(null, lineD(80 + i * 34, 398, 80 + i * 34, 360 - ((i * 7) % 4) * 9, 0), { c: B, w: 9, dur: 0.05 });
    b.t("warmer", 60, 480, "+7% moisture per °C of warming", { size: 44, c: R });
    b.cam("so", 0, 290, 1200);
    b.t("so", 60, 560, "now:", { size: 34 }); b.ln(null, 60, 730, 760, 730, { w: 3 });
    [[2, 150], [9, 170], [10, 120], [17, 160]].forEach(([i, h], k) => b.p(k ? null : "bursts", lineD(80 + i * 34, 728, 80 + i * 34, 728 - h, 0), { c: R, w: 11, dur: 0.15 }));
    b.t("spells", 190, 700, "dry spell", { size: 30 }); b.t(null, 480, 700, "dry spell", { size: 30 });
    b.t("bursts", 60, 790, "long dry spells + short, extreme bursts", { size: 38, c: R });
    b.cam("shifting", 500, 110, 1300);
    b.p("shifting", indiaD(m), { dur: 1.6, w: 3.5 });
    [[80, 27.2], [85.5, 25.6], [88, 23.6]].forEach(([lo, la], i) => b.ar(i ? null : "falling", g(lo, la)[0], g(lo, la)[1] - 44, g(lo, la)[0], g(lo, la)[1], { c: R, w: 5, dur: 0.25 }));
    b.t("uttar", 860, 250, "less rain: Uttar", { size: 34, c: R }); b.t(null, 860, 292, "Pradesh · Bihar ·", { size: 34, c: R }); b.t(null, 860, 334, "West Bengal (IMD)", { size: 34, c: R });
    [[72.5, 22], [76.5, 14]].forEach(([lo, la], i) => b.ar(i ? null : "western", g(lo, la)[0], g(lo, la)[1] + 40, g(lo, la)[0], g(lo, la)[1] - 8, { c: B, w: 5, dur: 0.25 }));
    b.t("heavier", 860, 560, "heavier floods:", { size: 34, c: B }); b.t(null, 860, 602, "western India +", { size: 34, c: B }); b.t(null, 860, 644, "southern peninsula", { size: 34, c: B });
    full(b);
  }),

  makeBoard("markets", (b) => {
    title(b, "How do markets react?");
    b.box("april", 620, 150, 560, 110, { c: B, w: 5 }); b.t(null, 900, 222, "IMD forecast (mid-April)", { size: 44, c: B, anchor: "middle" });
    b.cam("above", 0, 100, 1300);
    b.ar("above", 700, 262, 420, 350, { c: G, w: 6 }); b.t(null, 60, 420, "Above normal rain", { size: 56, c: G });
    b.t("ease", 60, 500, "farm commodity prices ease", { size: 38 });
    b.t("shares", 60, 570, "shares tend to rise:", { size: 38, c: G }); b.t("tractor", 60, 620, "tractors · two-wheelers ·", { size: 36 }); b.t("fertiliser", 60, 666, "fertiliser · consumer goods", { size: 36 });
    b.cam("below", 500, 100, 1300);
    b.ar("below", 1100, 262, 1380, 350, { c: R, w: 6 }); b.t(null, 1000, 420, "Below normal rain", { size: 56, c: R });
    b.t("futures", 1000, 500, "futures prices tend to jump:", { size: 38, c: R }); b.t("pulses", 1000, 550, "pulses · soybean · mustard · guar", { size: 36 });
    b.t("rural", 1000, 630, "rural-demand stocks tend to fall", { size: 38 });
    b.cam("this", 0, 0, 1800);
    b.t("advice", 900, 790, "how markets behave: not investment advice", { size: 34, anchor: "middle" });
    full(b);
  }),

  makeBoard("tn", (b) => {
    title(b, "Case study: Tamil Nadu's rainwater law");
    b.cam("2003", 0, 80, 1150);
    b.t("2003", 60, 300, "2003", { size: 150, c: B, dur: 0.7 });
    b.t("first", 60, 380, "first state: rainwater harvesting", { size: 40 }); b.t("compulsory", 60, 430, "compulsory for every building", { size: 40 });
    b.box("strict", 60, 500, 760, 100, { c: R, w: 5 }); b.t(null, 440, 566, "no harvesting system → no water connection", { size: 36, c: R, anchor: "middle" });
    b.cam("roof", 400, 150, 1400);
    b.p("roof", polyD([[1000, 300], [1130, 210], [1260, 300]]) + " " + rectD(1020, 300, 220, 150), { w: 4.5, dur: 0.7 });
    b.p(null, polyD([[1260, 300], [1330, 300], [1330, 380]]), { c: B, w: 5, dur: 0.3 });
    b.box("filter", 1280, 380, 230, 190, { w: 4 });
    b.ln("sand", 1280, 444, 1510, 444, { w: 3 }); b.t(null, 1395, 426, "sand", { size: 32, anchor: "middle" });
    b.ln("gravel", 1280, 508, 1510, 508, { w: 3 }); b.t(null, 1395, 490, "gravel", { size: 32, anchor: "middle" });
    b.t("charcoal", 1395, 554, "charcoal", { size: 32, anchor: "middle" });
    b.p("well", polyD([[1395, 570], [1395, 620], [1600, 620], [1600, 640]]), { c: B, w: 5, dur: 0.4 }); b.p(null, rectD(1560, 640, 80, 150), { c: B, w: 4, fill: B, fo: 0.25, dur: 0.4 });
    b.t(null, 1660, 730, "recharge", { size: 30, c: B }); b.t(null, 1660, 766, "well", { size: 30, c: B });
    b.cam("chennai", 0, 143, 1500);
    b.t("chennai", 60, 690, "Chennai: water table rose by several metres", { size: 40, c: G });
    b.t("seawater", 60, 746, "seawater intrusion pushed back", { size: 38, c: G });
    b.t("cleaned", 60, 810, "clean the system before each northeast monsoon", { size: 36 });
    full(b);
  }),

  makeBoard("outro", (b) => {
    b.p(b.start, circD(900, 420, 250, 80), { c: B, w: 6, dur: 0.8 }); b.t(null, 900, 440, "INDIAN MONSOON", { size: 60, c: B, anchor: "middle", dur: 0.8 });
    const br = (at: string, x1: number, y1: number, x2: number, y2: number, tx: number, ty: number, head: string, l: string, c: string, anchor: "start" | "end" | "middle" = "start") => {
      b.p(at, lineD(x1, y1, x2, y2), { c, w: 5, dur: 0.35 }); b.t(null, tx, ty, head, { size: 50, c, anchor }); b.t(null, tx, ty + 50, l, { size: 34, anchor });
    };
    br("what", 700, 372, 520, 240, 80, 150, "WHAT", "wind reversal · 2 phases", B);
    br("heating", 1100, 372, 1280, 240, 1720, 150, "WHY", "heating · ITCZ · Himalayas", R, "end");
    br("arrives", 660, 440, 500, 470, 80, 440, "HOW", "2 branches · timetable · 3 tests", G);
    br("matters", 1140, 440, 1300, 470, 1720, 440, "IMPACT", "crops · prices · markets", R, "end");
    br("respond", 900, 500, 900, 600, 900, 660, "RESPONSE", "store the rain · prepare for extremes", B, "middle");
    b.t("subscribe", 900, 820, "Subscribe to UPSC Animated", { size: 44, c: R, anchor: "middle" });
  }),
];
