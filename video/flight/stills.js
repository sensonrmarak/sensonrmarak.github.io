const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'] }); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 4 / 3 });
  await pg.goto('http://localhost:8765/flight/film.html?raw&pr=2'); await pg.waitForFunction('window.READY');
  const shots = { '01-hook': 12.5, '02-four-forces': 41, '03-airfoil-lift': 79, '04-myth': 101, '05-lift-equation': 131, '06-stall': 149, '07-turbofan': 172, '08-drag-winglet': 203, '09-controls': 232, '10-parts-exploded': 262, '11-cruise': 340, '12-mind-map': 396, '13-end-card': 405 };
  fs.mkdirSync(path.join(__dirname, 'out/stills'), { recursive: true });
  for (const [n, t] of Object.entries(shots)) { await pg.evaluate(t => renderAt(t), t); await pg.screenshot({ path: path.join(__dirname, 'out/stills', n + '.png'), type: 'png' }); }
  await b.close(); })();
