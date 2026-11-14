// node snap.js "t1,t2,..." out.jpg [pr]  -> contact sheet of frames
const { chromium } = require('playwright'); const { execSync } = require('child_process'); const fs = require('fs');
(async () => { const ts = process.argv[2].split(',').map(Number), out = process.argv[3], pr = process.argv[4] || 1;
  const b = await chromium.launch({ args: ['--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'] }); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto(`http://localhost:8765/flight/film.html?raw&pr=${pr}`); await pg.waitForFunction('window.READY', null, { timeout: 60000 }).catch(() => {});
  const files = []; for (const t of ts) { const t0 = Date.now(); await pg.evaluate(t => { try { renderAt(t); } catch (e) { console.error('renderAt ' + t + ': ' + e.message + ' ' + (e.stack || '').split('\n')[1]); } }, t); const f = `/tmp/snap_${t}.jpg`; await pg.screenshot({ path: f, type: 'jpeg', quality: 85 }); files.push(f); if (process.argv[5]) console.log(t, Date.now() - t0, 'ms'); }
  if (errs.length) console.log('ERRORS:\n' + [...new Set(errs)].slice(0, 8).join('\n'));
  const cols = Math.min(3, files.length), rows = Math.ceil(files.length / cols);
  execSync(`ffmpeg -v error -y ${files.map(f => '-i ' + f).join(' ')} -filter_complex "${files.map((_, i) => `[${i}:v]scale=800:-1[v${i}]`).join(';')};${files.map((_, i) => `[v${i}]`).join('')}xstack=inputs=${files.length}:layout=${files.map((_, i) => `${(i % cols) * 800}_${Math.floor(i / cols) * 450}`).join('|')}:fill=black" -q:v 3 ${out}`);
  await b.close(); })();
