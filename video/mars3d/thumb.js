// node thumb.js T -> ../marsacts/out/thumbnail-4k.png + thumbnail-1280.jpg (clean 3D frame from the cold open + thumbnail type)
const { chromium } = require('playwright'); const { execSync } = require('child_process'); const path = require('path');
(async () => { const T = +process.argv[2] || 12, out = path.join(__dirname, '../marsacts/out');
  const b = await chromium.launch({ args: ['--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'] }); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  pg.on('pageerror', e => console.log('ERR', e.message));
  await pg.goto('http://localhost:8765/mars3d/film.html?raw&pr=2&mb=4'); await pg.waitForFunction('window.READY', null, { timeout: 120000 });
  await pg.evaluate(T => { renderAt(T);
    document.querySelectorAll('#root > *').forEach(e => { if (!['gl', 'acc', 'vig', 'logo'].includes(e.id)) e.style.display = 'none'; });
    const root = document.querySelector('#root'), add = (h, css) => { const d = document.createElement('div'); d.innerHTML = h; d.style.cssText = 'position:absolute;white-space:nowrap;' + css; root.appendChild(d); return d; };
    const sh = 'text-shadow:0 6px 30px rgba(0,0,0,.9),0 0 4px rgba(0,0,0,.8)';
    add('INDIA REACHED MARS', `right:70px;top:90px;font:900 84px/1 "Body",Arial,sans-serif;color:#fff;letter-spacing:1px;${sh}`);
    add('FOR LESS THAN', `right:70px;top:186px;font:900 84px/1 "Body",Arial,sans-serif;color:#fff;${sh}`);
    add('A MOVIE', `right:66px;top:280px;font:900 170px/1 "Body",Arial,sans-serif;color:#ffb347;${sh}`);
    add('$74M', `left:90px;top:860px;font:900 92px/1 "Body",Arial,sans-serif;color:#fff;background:#e0201f;padding:16px 30px 10px;border-radius:16px;transform:rotate(-5deg);box-shadow:0 12px 40px rgba(0,0,0,.6)`);
    const lg = document.querySelector('#logo'); if (lg) lg.style.cssText += ';left:auto;right:44px;top:auto;bottom:40px;width:140px;height:140px';
  }, T);
  await pg.screenshot({ path: path.join(out, 'thumbnail-4k.png') });
  execSync(`ffmpeg -v error -y -i ${out}/thumbnail-4k.png -vf scale=1280:720:flags=lanczos -q:v 2 ${out}/thumbnail-1280.jpg`); await b.close(); })();
