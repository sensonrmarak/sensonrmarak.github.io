// node thumb.js  -> out/thumbnail-4k.png (3840x2160) + out/thumbnail-1280.jpg (YouTube upload, < 2 MB)
const { chromium } = require('playwright'); const { execSync } = require('child_process'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  await pg.goto('http://localhost:8765/flight2/thumb.html?raw&pr=2'); await pg.waitForFunction('window.READY', null, { timeout: 60000 });
  await pg.evaluate(() => {
    renderAt(1);
    ['#ovs', '#labels', '#lines', '#chip', '#src', '#dots', '#prog', '#veil', '#flash'].forEach(q => document.querySelector(q).style.display = 'none');
    const cv = document.querySelector('#gl'); cv.style.transform = 'none';
    const { g, planeSide, arrow, circ, line, rng, PR, C } = window.FX, W = 1920, H = 1080;
    g.setTransform(PR, 0, 0, PR, 0, 0); g.globalAlpha = 1; g.shadowBlur = 0;
    // background: black with a deep glow behind the aircraft
    g.fillStyle = '#000'; g.fillRect(0, 0, W, H);
    const rg = g.createRadialGradient(1290, 540, 40, 1290, 540, 760); rg.addColorStop(0, 'rgba(42,79,196,.55)'); rg.addColorStop(0.55, 'rgba(20,30,80,.25)'); rg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = rg; g.fillRect(0, 0, W, H);
    // airflow streamlines bending around the plane (cyan above = fast, orange below = slow)
    const r = rng(9);
    for (let i = 0; i < 9; i++) { const up = i < 5, y0 = up ? 250 + i * 48 : 690 + (i - 5) * 58;
      for (let k = 0; k < 64; k++) { const x = 720 + k * 19; if (up && x > 1640 && y0 < 330) continue; const d = (x - 1290) / 520, bend = Math.exp(-d * d * 1.6) * (up ? -70 + i * 10 : 38 - (i - 5) * 6) - (x > 1500 ? (x - 1500) * 0.05 : 0);
        circ(x, y0 + bend + (r() - 0.5) * 2, 4.2, up ? 'rgba(79,209,255,.75)' : 'rgba(255,150,80,.65)'); } }
    // the aircraft, climbing, with contrails and lights
    const o = { x: 1300, y: 560, s: 1.72, rot: -0.15, gear: 0, t: 0.02, trail: 0.85 }; planeSide(o);
    // forces: a big golden LIFT arrow up, WEIGHT down
    arrow(1290, 445, -Math.PI / 2, 300, C.gold, 58); arrow(1290, 690, Math.PI / 2, 190, '#3b82ff', 40);
    // overlay text
    const root = document.querySelector('#root'), add = (html, css) => { const d = document.createElement('div'); d.innerHTML = html; d.style.cssText = 'position:absolute;white-space:nowrap;' + css; root.appendChild(d); return d; };
    const t1 = add('WHY', 'left:70px;top:150px;font:900 190px/0.95 "Disp";color:#fbf5e9;text-shadow:0 8px 40px rgba(0,0,0,.8)');
    const t2 = add("DOESN'T IT", 'left:74px;top:350px;font:900 104px/1 "Disp";color:#fbf5e9;text-shadow:0 8px 40px rgba(0,0,0,.8)');
    const t3 = add('FALL?', 'left:66px;top:470px;font:900 230px/0.95 "Disp";color:#e8b548;text-shadow:0 8px 50px rgba(232,181,72,.35)');
    const fit = el => { const w = el.getBoundingClientRect().width; if (w > 640) el.style.fontSize = parseFloat(getComputedStyle(el).fontSize) * 640 / w + 'px'; };
    [t1, t2, t3].forEach(fit);
    add('79 TONNES', 'left:1040px;top:860px;font:900 64px/1 "Disp";color:#fff;background:#e0201f;padding:18px 34px 14px;border-radius:16px;transform:rotate(-4deg);box-shadow:0 12px 40px rgba(0,0,0,.6)');
    add('LIFT', 'left:1342px;top:160px;font:900 54px/1 "Disp";color:#e8b548;letter-spacing:2px;background:#000;padding:10px 16px;border-radius:10px');
    const lg = document.querySelector('#logo'); lg.style.cssText += ';left:auto;right:44px;top:40px;bottom:auto;width:150px;height:150px';
  });
  const out = path.join(__dirname, 'out'); await pg.screenshot({ path: path.join(out, 'thumbnail-4k.png') });
  execSync(`ffmpeg -v error -y -i ${out}/thumbnail-4k.png -vf scale=1280:720:flags=lanczos -q:v 2 ${out}/thumbnail-1280.jpg`);
  await b.close();
})();
