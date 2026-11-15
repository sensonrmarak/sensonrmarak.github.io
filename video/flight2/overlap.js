// Overlap audit: node overlap.js [step=0.25] [from=0] [to=end]
// Samples the film, collects the on-screen box of every visible element (DOM cards, labels, titles, chrome, logo
// and canvas objects registered by the drawing helpers), and reports every overlapping pair, anything inside the
// logo safe zone and any text box leaving the frame. Exits 0 with "0 problems" when the layout is clean.
const { chromium } = require('playwright');
(async () => {
  const step = +process.argv[2] || 0.25, from = +process.argv[3] || 0;
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await pg.goto('http://localhost:8765/flight2/film.html?raw&pr=1'); await pg.waitForFunction('window.READY', null, { timeout: 60000 });
  const to = +process.argv[4] || await pg.evaluate(() => DUR);
  const res = await pg.evaluate(({ step, from, to }) => {
    const W = 1920, H = 1080, out = [];
    const vis = e => { let op = 1; for (let n = e; n && n.id !== 'root'; n = n.parentElement) { const cs = getComputedStyle(n); if (cs.display === 'none' || cs.visibility === 'hidden') return 0; op *= +cs.opacity; } return op; };
    const nameOf = e => (e.id ? '#' + e.id : '.' + [...e.classList].join('.')) + ' "' + (e.innerText || e.getAttribute('src') || '').replace(/\s+/g, ' ').trim().slice(0, 26) + '"';
    for (let tg = from; tg < to; tg += step) {
      renderAt(tg); const cam = window.CAM, boxes = [];
      const add = (e, kind) => { if (vis(e) < 0.15) return; const r = e.getBoundingClientRect(); if (r.width < 4 || r.height < 4) return; boxes.push({ n: nameOf(e), kind, x0: r.left, y0: r.top, x1: r.right, y1: r.bottom }); };
      document.querySelectorAll('.ov').forEach(o => { if (getComputedStyle(o).display === 'none') return; [...o.children].forEach(ch => { if (ch.tagName === 'svg') return; if (ch.id === 'eqr') [...ch.children].forEach(cc => add(cc, 'dom')); else add(ch, 'dom'); }); });
      document.querySelectorAll('#labels .lab').forEach(e => add(e, 'label'));
      ['#chip', '#src', '#dots', '#logo'].forEach(q => add(document.querySelector(q), q === '#logo' ? 'logo' : 'chrome'));
      for (const r of window.REG()) { const m = (x, y) => [960 + (x - 960) * cam.cz + cam.cxp, 560 + (y - 560) * cam.cz + cam.cyp], a = m(r.x0, r.y0), c = m(r.x1, r.y1); boxes.push({ n: '[' + r.name + ']', kind: 'canvas', x0: a[0], y0: a[1], x1: c[0], y1: c[1] }); }
      const veil = +getComputedStyle(document.getElementById('veil')).opacity;
      const fam = n => n.startsWith('[part:') ? 'part' : n.startsWith('[plane') ? 'plane' : n.startsWith('[elephant') ? 'eleph' : n;
      for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
        const A = boxes[i], B = boxes[j];
        if (A.kind === 'canvas' && B.kind === 'canvas') { const fa = fam(A.n), fb = fam(B.n); if (fa === fb || [fa, fb].includes('[arrow]') && ([fa, fb].includes('plane') || [fa, fb].includes('[airfoil]'))) continue; }
        if ((A.n.startsWith('#chip') || B.n.startsWith('#chip')) && veil > 0.3) continue;
        const pad = (A.kind === 'logo' || B.kind === 'logo') ? 14 : 0;
        const ox = Math.min(A.x1 + pad, B.x1 + pad) - Math.max(A.x0 - pad, B.x0 - pad), oy = Math.min(A.y1 + pad, B.y1 + pad) - Math.max(A.y0 - pad, B.y0 - pad);
        if (ox > 6 && oy > 6) out.push({ t: +tg.toFixed(2), s: cam.scene, p: A.n + '  ×  ' + B.n, a: Math.round(ox * oy) });
      }
      for (const A of boxes) if (A.kind !== 'canvas' && A.kind !== 'logo' && (A.x0 < 6 || A.y0 < 4 || A.x1 > W - 6 || A.y1 > H - 6)) out.push({ t: +tg.toFixed(2), s: cam.scene, p: A.n + '  ×  [frame edge]', a: 0 });
    }
    return out;
  }, { step, from, to });
  // group consecutive samples of the same pair into time ranges
  const groups = new Map(); for (const r of res) { const k = r.s + '|' + r.p; const g = groups.get(k); if (g && r.t - g.t1 <= step * 1.5) { g.t1 = r.t; g.a = Math.max(g.a, r.a); } else if (!g) groups.set(k, { s: r.s, p: r.p, t0: r.t, t1: r.t, a: r.a, n: 1 }); else { groups.set(k + '#' + r.t, { s: r.s, p: r.p, t0: r.t, t1: r.t, a: r.a }); } }
  const list = [...groups.values()].sort((a, b) => a.t0 - b.t0);
  list.forEach(g => console.log(`${g.s.padEnd(9)} ${g.t0.toFixed(2)}-${g.t1.toFixed(2)}s  ${g.p}${g.a ? '  (' + g.a + ' px²)' : ''}`));
  console.log(`${list.length} problems`); await b.close();
})();
