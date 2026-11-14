// usage: node test.js <skillsDir> [slug...]  -> renders frames, reports console errors, writes contact sheets
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const dir = process.argv[2], only = process.argv.slice(3), out = path.join(__dirname, 'shots'); fs.mkdirSync(out, { recursive: true });
  const slugs = fs.readdirSync(dir).filter(d => d.startsWith('motion-') && d !== 'motion-core' && (!only.length || only.includes(d.slice(7))));
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  let bad = 0;
  for (const s of slugs) {
    const errs = []; pg.removeAllListeners('pageerror'); pg.removeAllListeners('console');
    pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    const f = 'file://' + path.join(dir, s, 'example.html');
    try {
    await pg.goto(f + '?t=0'); await pg.evaluate(() => document.fonts.ready); const dur = await pg.evaluate(() => DUR);
    const ts = [0.15, 0.3, 0.5, 0.7, 0.95].map(k => +(dur * k).toFixed(2)); const files = [];
    for (const t of ts) { await pg.evaluate(t => renderAt(t), t); const fn = path.join(out, `${s}-${t}.png`);
      await pg.screenshot({ path: fn }); files.push(fn); }
    // determinism: DOM + canvas pixels must match after reaching t by different paths
    const snap = () => pg.evaluate(() => document.getElementById('root').outerHTML + [...document.querySelectorAll('canvas')].map(c => c.toDataURL()).join(''));
    await pg.evaluate(() => renderAt(DUR * 0.5)); const a1 = await snap();
    await pg.evaluate(() => { renderAt(DUR * 0.9); renderAt(DUR * 0.1); renderAt(DUR * 0.5); }); const a2 = await snap();
    const det = a1 === a2;
    if (errs.length || !det) bad++;
    console.log(`${s.padEnd(26)} ${errs.length ? 'ERR ' + errs.slice(0, 2).join(' | ') : 'ok'}${det ? '' : '  NONDETERMINISTIC'}`);
    fs.writeFileSync(path.join(out, s + '.list'), files.join('\n'));
    } catch (e) { bad++; console.log(`${s.padEnd(26)} CRASH ${e.message.split('\n')[0]} ${errs.join(' | ')}`); }
  }
  await b.close(); console.log(bad ? `${bad} with problems` : 'all clean');
})();
