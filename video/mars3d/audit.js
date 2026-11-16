// node audit.js [step] : samples the 3D cold open and reports overlaps and crops
const { chromium } = require('playwright');
(async () => { const step = +process.argv[2] || 0.1; const b = await chromium.launch({ args: ['--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'] }); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await pg.goto('http://localhost:8765/mars3d/film.html?raw&mb=1&pr=1'); await pg.waitForFunction('window.READY', null, { timeout: 180000 }); const dur = await pg.evaluate(() => DUR);
  const res = await pg.evaluate(({ step, dur }) => { const out = [], W = 1920, H = 1080;
    const vis = e => { let op = 1; for (let n = e; n && n.id !== 'root'; n = n.parentElement) { const cs = getComputedStyle(n); if (cs.display === 'none' || cs.visibility === 'hidden') return 0; op *= +cs.opacity; } return op; };
    for (let t = 0; t < dur; t += step) { renderAt(t); const A = AUDIT3D(t), dom = [];
      const add = (e, n) => { if (vis(e) < 0.15) return; const r = e.getBoundingClientRect(); if (r.width < 4 || r.height < 4) return; dom.push({ n, x0: r.left, y0: r.top, x1: r.right, y1: r.bottom, el: e }); };
      document.querySelectorAll('.t').forEach(e => add(e, '#' + e.id)); add(document.querySelector('#hud'), '#hud'); add(document.querySelector('#src'), '#src'); add(document.querySelector('#logo'), '#logo');
      if (A.split) document.querySelectorAll('#split span').forEach((e, i) => add(e, '#split-label-' + i));
      const ov = (p, q, pad = 0) => Math.min(p.x1, q.x1) - Math.max(p.x0, q.x0) + pad > 6 && Math.min(p.y1, q.y1) - Math.max(p.y0, q.y0) + pad > 6;
      for (let i = 0; i < dom.length; i++) for (let j = i + 1; j < dom.length; j++) if (ov(dom[i], dom[j], dom[i].n === '#logo' || dom[j].n === '#logo' ? 14 : 0)) out.push([t, dom[i].n + ' × ' + dom[j].n]);
      for (const d of dom) { if (d.n !== '#logo' && (d.x0 < 6 || d.y0 < 4 || d.x1 > W - 6 || d.y1 > H - 6)) out.push([t, d.n + ' × frame edge']);
        if (d.el.scrollWidth > d.el.clientWidth + 2) out.push([t, d.n + ' text cut off inside its box']);
        if (A.split && d.n !== '#logo' && d.x0 < 960 && d.x1 > 960) out.push([t, d.n + ' × split divider']);
        for (const s of A.boxes) if (ov(d, s, d.n === '#logo' ? 14 : 0)) out.push([t, d.n + ' × ' + s.n]); }
      for (const s of A.boxes) if (s.x1 - s.x0 > 30 && (s.x0 < s.panel[0] + 4 || s.x1 > s.panel[1] - 4 || s.y0 < 4 || s.y1 > H - 4)) out.push([t, s.n + ' cropped by ' + (A.split ? 'its panel' : 'the frame')]);
    }
    return out; }, { step, dur });
  const g = new Map(); for (const [t, p] of res) { const x = g.get(p); if (x && t - x.t1 <= step * 1.6) x.t1 = t; else if (!x) g.set(p, { t0: t, t1: t }); else g.set(p + '@' + t, { t0: t, t1: t, p }); }
  [...g.entries()].sort((a, b) => a[1].t0 - b[1].t0).forEach(([p, r]) => console.log(`${r.t0.toFixed(2)}-${r.t1.toFixed(2)}s  ${r.p || p}`)); console.log(g.size + ' problems'); await b.close(); })();
