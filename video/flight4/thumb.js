// node thumb.js  -> out/thumbnail-4k.png (3840x2160) + out/thumbnail-1280.jpg (YouTube upload, < 2 MB)
const { chromium } = require('playwright'); const { execSync } = require('child_process'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  pg.on('pageerror', e => console.log('ERR', e.message));
  await pg.goto('http://localhost:8766/flight4/thumb.html?raw&pr=2'); await pg.waitForFunction('window.READY', null, { timeout: 60000 });
  await pg.evaluate(() => {
    renderAt(1);
    ['#ovs', '#labels', '#lines', '#chip', '#src', '#hud', '#prog', '#veil', '#iris', '#pz', '#card', '#rw', '#frz', '#grain'].forEach(q => { const e = document.querySelector(q); if (e) e.style.display = 'none'; });
    const cv = document.querySelector('#gl'); cv.style.transform = 'none'; cv.style.filter = 'none';
    const { g, plane3D, p3, arrow, circ, line, rng, PR, C } = window.FX, W = 1920, H = 1080;
    g.setTransform(PR, 0, 0, PR, 0, 0); g.globalAlpha = 1; g.shadowBlur = 0; g.fillStyle = '#000'; g.fillRect(0, 0, W, H);
    // dawn: warm horizon low in frame, faint stars above
    const hz = 900, sg = g.createLinearGradient(0, hz - 520, 0, hz); sg.addColorStop(0, 'rgba(0,0,0,0)'); sg.addColorStop(0.7, 'rgba(255,110,40,.22)'); sg.addColorStop(1, 'rgba(255,170,90,.55)'); g.fillStyle = sg; g.fillRect(0, hz - 520, W, 520);
    const r = rng(5); for (let i = 0; i < 120; i++) circ(r() * W, r() * 420, 0.6 + r() * 1.4, `rgba(255,255,255,${0.15 + 0.35 * r()})`);
    g.fillStyle = '#07080b'; g.fillRect(0, hz, W, H - hz); line(0, hz, W, hz, 'rgba(255,180,100,.7)', 3);
    g.shadowColor = '#ffcf70'; g.shadowBlur = 14; for (let i = 0; i < 12; i++) { const x = i * 180 - 40; line(x, hz + 24, x + 120, hz + 24, 'rgba(255,225,150,.95)', 7); } for (let i = 0; i < 6; i++) { const x = i * 360 - 100; line(x, hz + 90, x + 260, hz + 90, 'rgba(255,255,255,.4)', 14); } g.shadowBlur = 0;
    // speed streaks behind the aircraft
    const rs = rng(9); for (let i = 0; i < 46; i++) { const y = 200 + rs() * 640, x = 700 + rs() * 1300, L = 80 + rs() * 260; line(x, y, x + L, y, `rgba(255,255,255,${0.06 + 0.12 * rs()})`, 3); }
    // the aircraft lifting off, seen from below at a front three-quarter angle
    const o = { x: 1300, y: 600, s: 1.55, yaw: 0.45, elev: -0.12, pitch: 0.17, gear: 0.7, t: 0.05 }; plane3D(o);
    // lift (gold) and weight (blue)
    const top = p3(o, [-40, 0, 40]), bot = p3(o, [-40, 0, -60]);
    arrow(top[0], top[1] - 10, -Math.PI / 2, 300, C.gold, 62); arrow(bot[0], bot[1] + 30, Math.PI / 2, 150, '#3b82ff', 40);
    // type
    const root = document.querySelector('#root'), add = (html, css) => { const d = document.createElement('div'); d.innerHTML = html; d.style.cssText = 'position:absolute;white-space:nowrap;' + css; root.appendChild(d); return d; };
    const t1 = add('WHY', 'left:70px;top:120px;font:900 196px/0.95 "Disp";color:#fbf5e9;text-shadow:0 8px 40px rgba(0,0,0,.85)');
    const t2 = add("DOESN'T IT", 'left:76px;top:326px;font:900 104px/1 "Disp";color:#fbf5e9;text-shadow:0 8px 40px rgba(0,0,0,.85)');
    const t3 = add('FALL?', 'left:66px;top:446px;font:900 236px/0.95 "Disp";color:#e8b548;text-shadow:0 8px 50px rgba(232,181,72,.35)');
    const fit = el => { const w = el.getBoundingClientRect().width; if (w > 660) el.style.fontSize = parseFloat(getComputedStyle(el).fontSize) * 660 / w + 'px'; }; [t1, t2, t3].forEach(fit);
    add('79 TONNES', 'left:84px;top:760px;font:900 66px/1 "Disp";color:#fff;background:#e0201f;padding:18px 34px 14px;border-radius:16px;transform:rotate(-4deg);box-shadow:0 12px 40px rgba(0,0,0,.6)');
    add('LIFT', `left:${top[0] + 54}px;top:${top[1] - 300}px;font:900 56px/1 "Disp";color:#e8b548;letter-spacing:2px;background:rgba(0,0,0,.8);padding:10px 16px;border-radius:10px`);
    const lg = document.querySelector('#logo'); lg.style.cssText += ';left:auto;right:44px;top:40px;bottom:auto;width:150px;height:150px';
  });
  const out = path.join(__dirname, 'out'); await pg.screenshot({ path: path.join(out, 'thumbnail-4k.png') });
  execSync(`ffmpeg -v error -y -i ${out}/thumbnail-4k.png -vf scale=1280:720:flags=lanczos -q:v 2 ${out}/thumbnail-1280.jpg`);
  await b.close();
})();
