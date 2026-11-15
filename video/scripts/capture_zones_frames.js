// Captures the lesson's figure footage frame by frame as 2560x1440 PNGs, with every state change cued to the
// word-aligned narration (src/zones/cues.json), then encodes each chunk losslessly-close to MP4.
//   node scripts/capture_zones_frames.js <workerIndex> <workers> <outDir>
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const ROOT = path.resolve(__dirname, '..');
const cue = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/zones/cues.json'), 'utf8'));
const TL = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/zones/timeline.json'), 'utf8'));
const FIG = { A: path.resolve(ROOT, '../colorfigures/seasons_orrery.html'), B: path.resolve(ROOT, '../colorfigures/heat_zones_orrery.html') };
const FPS = 30, TOTAL = 127.5, CUT = TL.segments[5].start, W = 2560, H = 1440;
const clamp = x => Math.max(0, Math.min(1, x)), ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
const ramp = (t, a, b) => ease(clamp((t - a) / (b - a)));                // 0 -> 1 between a and b
const win = (t, a, b, f = .6) => ramp(t, a, a + f) * (1 - ramp(t, b - f, b));  // fade in at a, out by b
const twenty2 = TL.segments[2].words.filter(w => w.text.toLowerCase().startsWith('twenty'))[1].start;

function director(t){
  const YAW0 = 45;
  if (t < CUT){                                                         // ---- figure A: seasons orrery
    let yaw = YAW0 + 360 * ramp(t, 0.3, 16.8);
    let th = 180 + 180 * ramp(t, cue.six, cue.six + 1.7);
    if (t > cue.watch) th = 360 + (t - cue.watch) * 40;
    return { fig: 'A', yaw, th, xr: ramp(t, cue.inside, cue.inside + 0.9), labels: t > cue.belt,
      deg: ramp(t, cue.tilted - 0.2, cue.tilted + 0.5), degLat: win(t, twenty2 - 0.4, cue.six - 0.1) };
  }
  let th = 180;                                                         // ---- figure B: heat zones orrery
  const orb0 = cue.temperate + 0.2, orb1 = TL.segments[6].end + 0.2;   // a year back to June while "four strong seasons" is said
  if (t > orb0) th = 180 + 360 * ramp(t, orb0, orb1);
  if (t > cue.winter7 - 1.3) th = 540 + 180 * ramp(t, cue.winter7 - 1.3, cue.winter7 + 0.1);
  if (t > cue.which) th = 720 + 180 * ramp(t, cue.which, cue.which + 1.5);
  let city = -1;
  if (t > cue.singapore - 0.15) city = 0;
  if (t > cue.london - 0.15) city = 10;
  if (t > cue.longyearbyen - 0.15) city = 14;
  const degLat = Math.max(win(t, cue.between - 0.5, cue.temperate - 0.1), win(t, cue.beyond - 0.3, cue.winter7 - 1.4));
  const yaw = t > cue.remember ? YAW0 + (t - cue.remember) * 14 : YAW0;
  return { fig: 'B', yaw, th, zones: true, city, labels: true, xr: 0, deg: 1 - ramp(t, cue.which, cue.which + 0.6), degLat };
}

(async () => {
  const [wi, wn, out] = [+process.argv[2], +process.argv[3], path.resolve(process.argv[4])];
  const N = Math.round(TOTAL * FPS), per = Math.ceil(N / wn), f0 = wi * per, f1 = Math.min(N, f0 + per);
  const dir = path.join(out, `w${wi}`); fs.mkdirSync(dir, { recursive: true });
  const b = await chromium.launch(), pages = {};
  const pageFor = async fig => {
    if (pages[fig]) return pages[fig];
    const p = await b.newPage({ viewport: { width: W / 2, height: H / 2 }, deviceScaleFactor: 2 });
    await p.goto('file://' + FIG[fig]);
    await p.addStyleTag({ content: 'body>header,.controls,.made-with,.zchip,.toast{display:none!important} #btns,.actions,.vset,#lblctl{visibility:hidden!important} body{padding-top:14px!important}' });
    await p.waitForTimeout(1500);
    return (pages[fig] = p);
  };
  const only = process.env.TEST_FRAMES ? process.env.TEST_FRAMES.split(',').map(Number) : null;
  for (let fr = f0; fr < f1; fr++){
    if (only && !only.includes(fr)) continue;
    const s = director(fr / FPS), p = await pageFor(s.fig);
    await p.evaluate(s => new Promise(res => {
      const st = window.__st; for (const k of ['th', 'xr', 'deg', 'degLat', 'city', 'zones']) if (s[k] !== undefined) st[k] = s[k];
      st.rays = true; st.moving = false; st.run = false;
      setCam(s.yaw, PITCH0);
      document.documentElement.classList.toggle('nolabels', !s.labels);
      ui.render(); requestAnimationFrame(() => requestAnimationFrame(res));
    }), s);
    await p.screenshot({ path: path.join(dir, (only ? 'f' + fr : String(fr - f0).padStart(5, '0')) + '.png') });
    if ((fr - f0) % 200 === 0) console.log(`w${wi} ${fr - f0}/${f1 - f0}`);
  }
  await b.close();
  if (only) { console.log('test frames written to', dir); return; }
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', path.join(dir, '%05d.png'), '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p', path.join(out, `chunk${wi}.mp4`)]);
  fs.rmSync(dir, { recursive: true });
  console.log(`w${wi} done`);
})();
