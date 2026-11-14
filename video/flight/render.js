// node render.js [workers=4] [fps=24]  -> out/seg_XXXX.mp4 (resumable), 3840x2160
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const fs = require('fs'); const path = require('path');
const NW = +process.argv[2] || 4, FPS = +process.argv[3] || 24, SEG = FPS * 10, OUT = path.join(__dirname, 'out');
const TM = JSON.parse(fs.readFileSync(path.join(__dirname, 'timings.json'))), TOTAL = Math.ceil(TM.total * FPS), NSEG = Math.ceil(TOTAL / SEG);
const queue = []; for (let i = 0; i < NSEG; i++) if (!fs.existsSync(path.join(OUT, `seg_${String(i).padStart(4, '0')}.mp4`))) queue.push(i);
console.log(`${TOTAL} frames, ${NSEG} segments, ${queue.length} to do, ${NW} workers`); const t0 = Date.now(); let done = 0;
async function worker(w) { const b = await chromium.launch({ args: ['--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'] }); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  await pg.goto('http://localhost:8765/flight/film.html?raw&pr=2'); await pg.waitForFunction('window.READY', null, { timeout: 120000 });
  while (queue.length) { const i = queue.shift(), name = path.join(OUT, `seg_${String(i).padStart(4, '0')}`), a = i * SEG, z = Math.min(TOTAL, a + SEG);
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'fast', '-crf', '15', '-pix_fmt', 'yuv420p', '-threads', '2', name + '.part.mp4'], { stdio: ['pipe', 'inherit', 'inherit'] });
    const closed = new Promise(r => ff.on('close', r));
    for (let f = a; f < z; f++) { await pg.evaluate(t => renderAt(t), f / FPS); const buf = await pg.screenshot({ type: 'jpeg', quality: 95 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); const code = await closed; if (code === 0) { fs.renameSync(name + '.part.mp4', name + '.mp4'); done++; const el = (Date.now() - t0) / 60000; console.log(`seg ${i} done (${done} this run, ${queue.length} queued) ${el.toFixed(1)} min`); } else console.log(`seg ${i} FAILED`); }
  await b.close(); }
Promise.all(Array.from({ length: NW }, (_, w) => worker(w))).then(() => console.log('ALL DONE'));
