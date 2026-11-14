RECIPES = [
# ---------------------------------------------------------------- orbit-rings
dict(slug="orbit-rings", title="Orbit Rings", dur=6, bg="var(--ink)",
desc="Tilted 3D orbit rings around a central core with satellites riding each ring, passing behind and in front of the core with correct depth. Use for ecosystems, integrations around a platform, solar-system metaphors, 'everything revolves around X', networks, atoms and space-themed openers.",
look="A glowing sphere in the centre. Four thin elliptical rings at different tilts draw on one after another; a coloured satellite rides each ring at its own speed. Where a ring passes behind the sphere it is hidden, so the system reads in 3D. Labels can ride with the satellites.",
beats=["0.0–0.6 s: core scales in with a soft halo.",
       "0.4–2.0 s: rings draw on (each sweeps its full angle in 0.6 s, staggered 0.25 s).",
       "1.0 s →: satellites launch, each at its own angular speed.",
       "Continuous: the whole system yaws slowly (0.15 rad/s)."],
build="""
Each ring is a circle of radius `r` in the XZ plane, tilted by `rot(p, tiltX, yaw, tiltZ)` and projected with `proj()`. Ring segments and satellites with `z > 0` (behind the centre plane) that fall inside the core's screen disc are skipped, which is all the occlusion needed. Draw order: back halves of rings, core, then front halves and satellites.
""",
knobs=["Ring radii and tilts.",
       "Satellite speeds, colours, sizes; labels.",
       "Yaw speed; ring draw order.",
       "Core: plain sphere, logo or photo."],
pitfalls=["Draw back halves before the core and front halves after, or rings cut across it.",
          "Give rings clearly different tilts; similar tilts read as a mess of lines.",
          "Keep satellite speeds incommensurate so they don't line up in a loop."],
pairs=["globe-arcs", "particle-sphere", "agent-swarm", "torus-wire"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), rings = [{ r: 260, tx: 1.15, tz: 0.2, sp: 1.3, c: C.accent }, { r: 360, tx: 1.35, tz: -0.5, sp: -0.9, c: C.yellow }, { r: 460, tx: 1.0, tz: 0.7, sp: 0.6, c: C.blue }, { r: 560, tx: 1.45, tz: -0.15, sp: -0.45, c: C.pink }];
function renderAt(t) {
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  const core = E.back(seg(t, 0, 0.6)), CR = 150 * core, yaw = t * 0.15;
  const pt = (R, a) => proj(rot([Math.cos(a) * R.r, 0, Math.sin(a) * R.r], R.tx, yaw, R.tz), 1800);
  const hidden = p => p[2] < 1 && Math.hypot(p[0] - W / 2, p[1] - H / 2) < CR;
  const drawRing = (R, i, front) => { const k = E.inOut(seg(t, 0.4 + i * 0.25, 1.0 + i * 0.25)); if (k <= 0) return;
    g.strokeStyle = "rgba(239,233,223,.45)"; g.lineWidth = 2; g.beginPath(); let on = false;
    for (let s = 0; s <= 180 * k; s++) { const p = pt(R, s / 180 * Math.PI * 2), isF = p[2] >= 1;
      if (isF !== front || hidden(p)) { on = false; continue; } on ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1]); on = true; } g.stroke(); };
  const drawSat = (R, i, front) => { if (t < 1.0 + i * 0.25) return; const p = pt(R, (t - 1) * R.sp + i * 1.7), isF = p[2] >= 1;
    if (isF !== front || hidden(p)) return; const sz = 18 * p[2] ** 2 * E.back(seg(t, 1 + i * 0.25, 1.4 + i * 0.25));
    g.fillStyle = R.c; g.beginPath(); g.arc(p[0], p[1], Math.max(0, sz), 0, 7); g.fill(); };
  rings.forEach((R, i) => { drawRing(R, i, false); drawSat(R, i, false); });
  const hg = g.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, CR * 2); hg.addColorStop(0, "rgba(255,74,28,.35)"); hg.addColorStop(1, "rgba(255,74,28,0)");
  g.fillStyle = hg; g.beginPath(); g.arc(W / 2, H / 2, CR * 2, 0, 7); g.fill();
  const sg = g.createRadialGradient(W / 2 - CR * 0.35, H / 2 - CR * 0.35, CR * 0.1, W / 2, H / 2, CR); sg.addColorStop(0, "#ffb08f"); sg.addColorStop(1, C.accent);
  g.fillStyle = sg; g.beginPath(); g.arc(W / 2, H / 2, Math.max(0, CR), 0, 7); g.fill();
  rings.forEach((R, i) => { drawRing(R, i, true); drawSat(R, i, true); });
}
"""),

# ---------------------------------------------------------------- halftone-wave
dict(slug="halftone-wave", title="Halftone Wave", dur=6, bg="var(--ink)",
desc="A printed-halftone dot field that renders a lit 3D ring and ripples, dot size driven by shading, with red accent dots in the shadows. Use for 'systems' chapters, retro-print and newspaper looks, editorial tech, Vox-style backgrounds, audio pulses and abstract showreel beats.",
look="A regular grid of dots on black. Dot size encodes brightness of an underlying image: a softly lit torus ring that rotates its light, plus a ripple that passes through. Bright areas are big white dots; the background dots stay tiny and some turn accent red in a checker of the darker zones, like a two-ink print.",
beats=["0.0–1.0 s: dots grow in from size 0, centre first.",
       "Continuous: the light direction on the ring orbits once over the clip.",
       "2.0–3.5 s: a ripple crosses outward from the centre, inflating dots.",
       "4.5–6.0 s: the ring slowly 'breathes' its radius."],
build="""
Sample a brightness function `b(x, y, t)` at each grid cell and draw a dot of radius `maxR·√b` (area ∝ brightness, like real halftone). The ring is a 2D torus field: distance to a circle `|d - R|` gives the tube; a fake normal from that and a rotating light vector gives Lambert shading. Add a Gaussian ripple ring to `b`. Accent dots: where `b` is low and `(i + j)` is even, draw red at a fixed small size.
""",
knobs=["Cell size (18–30 px) and max dot radius.",
       "The image function: swap the ring for text masks, a face (from an image) or a logo.",
       "Light orbit speed; ripple timing.",
       "Two-ink colours."],
pitfalls=["Radius ∝ √brightness, not brightness, or mid-tones look too dark.",
          "Cell sizes below ~14 px at 1080p moiré in compressed video.",
          "Keep the dot grid fixed; moving the grid itself shimmers."],
pairs=["wave-dots", "paper-collage", "tile-grids", "dot-wipe"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), CS = 26;
function renderAt(t) {
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  const la = t * Math.PI * 2 / 6, L = [Math.cos(la) * 0.7, Math.sin(la) * 0.7, 0.7];
  const RR = 300 * (1 + 0.06 * Math.sin(seg(t, 4.5, 6) * Math.PI * 2)), TR = 120;
  for (let j = 0, y = CS / 2; y < H; y += CS, j++) for (let i = 0, x = CS / 2; x < W; x += CS, i++) {
    const dx = x - W / 2, dy = y - H / 2, d = Math.hypot(dx, dy) || 1, on = E.out(seg(t, d / 1100, d / 1100 + 0.6));
    const q = (d - RR) / TR; let b = 0;
    if (Math.abs(q) < 1) { const nz = Math.sqrt(1 - q * q), nx = dx / d * q, ny = dy / d * q;
      b = clamp(nx * L[0] + ny * L[1] + nz * L[2]) * 0.9 + 0.1; }
    const c = (t - 2) * 650; if (t > 2 && t < 3.6) b += Math.exp(-(((d - c) / 70) ** 2)) * 0.5;
    b = clamp(b);
    if (b > 0.06) { g.fillStyle = C.paper; g.beginPath(); g.arc(x, y, CS * 0.48 * Math.sqrt(b) * on, 0, 7); g.fill(); }
    else if ((i + j) % 2 === 0) { g.fillStyle = (i * 7 + j * 3) % 5 === 0 ? C.accent : "#3a3a3a"; g.beginPath(); g.arc(x, y, 2.6 * on, 0, 7); g.fill(); }
  }
}
"""),

# ---------------------------------------------------------------- scramble-decode
dict(slug="scramble-decode", title="Scramble Decode", dur=6, bg="var(--ink)",
desc="Text that resolves out of cycling random glyphs, left to right, like a decrypting terminal or hacker reveal, with the settled letters locking in colour. Use for secrets/security, AI 'thinking', product names, codes and passwords, glitchy tech intros, subtitles and data reveals.",
look="A headline and a mono subtitle. Each character cycles through random glyphs (A–Z, 0–9, symbols) at 20 fps, then locks to its final letter in a wave from left to right. Unlocked characters are dim accent; locked ones are paper white with a one-frame flash.",
beats=["0.0–0.4 s: the full line appears as random glyphs.",
       "0.4–2.4 s: headline locks left to right (each char ~0.05 s after the previous, plus seeded jitter).",
       "2.0–3.6 s: subtitle locks, faster.",
       "4.6–5.4 s: optional re-scramble of one word (shows it's live), relocks."],
build="""
For each character: `lockAt = start + i·step + jitter_i`. Before `lockAt`, show a glyph chosen by `rng(seed + i·997 + floor(t·20))`, which changes 20 times a second and is identical on every render of the same frame. At `lockAt` show the real character; for one frame after, flash it accent. Spaces lock immediately.
""",
knobs=["Glyph set (letters, katakana, binary, box-drawing).",
       "Cycle rate (20 fps) and lock step per char.",
       "Lock order: left-to-right, random, centre-out.",
       "Colours for scrambling vs. locked."],
pitfalls=["Seed by `floor(t·rate)`, never `Math.random()`, or scrubbing shows different glyphs.",
          "Use a monospace face or the line width jumps every frame.",
          "Keep scrambling short per char (< 1.5 s) or it becomes unreadable noise."],
pairs=["typewriter", "split-flap", "kinetic-type", "command-palette"],
css="""
#h { position:absolute; left:140px; top:330px; font:800 150px var(--mono); letter-spacing:-4px; white-space:pre; }
#s { position:absolute; left:146px; top:560px; font:600 40px var(--mono); white-space:pre; }
#tag { position:absolute; left:146px; top:250px; font:700 24px var(--mono); color:#777; letter-spacing:4px; }
""",
html="""<div id="tag">// ACCESS GRANTED</div><div id="h"></div><div id="s"></div>""",
js="""
const GL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&@$*+=<>/\\\\";
const lines = [{ el: $("#h"), txt: "DECRYPTED.", start: 0.4, step: 0.17, seed: 1 }, { el: $("#s"), txt: "Every frame is a function of time.", start: 2.0, step: 0.04, seed: 2 }];
lines.forEach(L => { const r = rng(L.seed); L.lock = [...L.txt].map((c, i) => c === " " ? 0 : L.start + i * L.step + r() * 0.15); });
function renderAt(t) {
  const fr = Math.floor(t * 20);
  lines.forEach((L, li) => { let html = "";
    [...L.txt].forEach((c, i) => {
      if (c === " ") { html += " "; return; }
      // headline re-scrambles its first word at 4.6 s and relocks left to right
      const relock = li === 0 && i < 9 && t > 4.6 ? 4.9 + i * 0.06 : null;
      const lockT = relock ?? L.lock[i], locked = t >= lockT;
      if (!locked) { const gch = GL[Math.floor(rng(L.seed * 7919 + i * 997 + fr)() * GL.length)];
        html += `<span style="color:${C.accent};opacity:.75">${gch === "<" ? "&lt;" : gch}</span>`; }
      else html += `<span style="color:${t - lockT < 0.05 ? C.accent : C.paper}">${c}</span>`; });
    L.el.innerHTML = html; });
  $("#tag").style.opacity = E.out(seg(t, 2.4, 2.8));
}
"""),

# ---------------------------------------------------------------- carousel-ring
dict(slug="carousel-ring", title="Carousel Ring", dur=7, bg="var(--paper)",
desc="Cards arranged on a 3D ring that rotates in confident steps, bringing each card to the front where it scales up and sharpens while the rest recede. Use for portfolios, product lineups, case studies, testimonials, templates, galleries and 'browse the collection' moments.",
look="Eight image cards stand on an invisible circular track seen slightly from above. The ring turns one card at a time with an ease-in-out and a tiny settle; the front card is full-size and bright, side cards angle away and dim, back cards are small and faint. A caption under the front card updates each step.",
beats=["0.0–0.8 s: ring scales up from 0.8 and fades in.",
       "1.0, 2.2, 3.4, 4.6 s: step rotations of 45° (0.7 s each, in-out).",
       "Caption swaps at each step midpoint.",
       "5.8–7.0 s: hold on the final card with a slow 3° drift."],
build="""
Cards are children of a `preserve-3d` ring: `rotateY(i·45°) translateZ(R)`. The ring's `rotateY` is a step function: the sum over steps of `45°·E.inOut(seg(t, step_k, step_k + 0.7))`. Per card, the facing angle `cos(θ_i + ring)` drives opacity and brightness (computed, not via backface). The caption text is chosen by the current step index.
""",
knobs=["Card count, ring radius, camera tilt (rotateX on the stage).",
       "Step times and duration; continuous spin as an alternative.",
       "Card art (images), caption list.",
       "Dim strength for side/back cards."],
pitfalls=["Cards facing away show mirrored; dim them heavily or hide when `cos < -0.2`.",
          "Use step rotation for content, continuous only for ambience.",
          "Large radius plus strong perspective distorts the side cards; keep perspective ≥ 2000 px."],
pairs=["card-fan", "type-ring", "phone-trio", "marquee-brands"],
css="""
.stage { position:absolute; inset:0; perspective:2400px; }
#ring { position:absolute; left:50%; top:46%; transform-style:preserve-3d; }
.cd { position:absolute; left:-200px; top:-260px; width:400px; height:520px; border-radius:28px; box-shadow:0 30px 60px rgba(0,0,0,.25); }
.cd b { position:absolute; left:30px; bottom:26px; font:400 54px var(--display); color:#fff; letter-spacing:-2px; }
#cap { position:absolute; left:0; right:0; top:900px; text-align:center; font:700 30px var(--mono); letter-spacing:3px; }
""",
html="""<div class="stage"><div id="ring"></div></div><div id="cap"></div>""",
js="""
const COLS = [C.accent, C.blue, C.yellow, C.ink, C.pink, "#1f8a5b", "#8b5cf6", "#e85d9e"], NAMES = ["Atlas", "Nimbus", "Solace", "Onyx", "Petal", "Fern", "Iris", "Bloom"];
const N = 8, R = 640, ring = $("#ring"), cards = [], steps = [1.0, 2.2, 3.4, 4.6];
COLS.forEach((c, i) => { const d = document.createElement("div"); d.className = "cd"; d.style.background = `linear-gradient(160deg, ${c}, ${mix(c, "#000000", 0.35)})`;
  d.innerHTML = `<b>${NAMES[i]}</b>`; ring.appendChild(d); cards.push(d); });
function renderAt(t) {
  const intro = E.out(seg(t, 0, 0.8));
  let ang = 0, idx = 0; steps.forEach((s, k) => { const p = E.inOut(seg(t, s, s + 0.7)); ang -= 45 * p; if (p > 0.5) idx = k + 1; });
  ang += 3 * Math.sin(seg(t, 5.8, 7) * Math.PI);
  ring.style.transform = `translateZ(-${R}px) rotateX(-8deg) rotateY(${ang}deg) scale(${lerp(0.8, 1, intro)})`; ring.style.opacity = intro;
  cards.forEach((c, i) => { const f = Math.cos((i * 45 + ang) * Math.PI / 180);
    c.style.transform = `rotateY(${i * 45}deg) translateZ(${R}px) scale(${0.85 + 0.15 * clamp(f)})`;
    c.style.opacity = f < -0.2 ? 0 : (0.25 + 0.75 * clamp((f + 0.2) / 1.2)).toFixed(3);
    c.style.filter = `brightness(${(0.6 + 0.4 * clamp(f)).toFixed(3)})`; });
  $("#cap").textContent = `${String(idx + 1).padStart(2, "0")} / ${NAMES[idx % N].toUpperCase()}`;
}
"""),

# ---------------------------------------------------------------- chat-thread
dict(slug="chat-thread", title="Chat Thread", dur=7, bg="#e9ecf2",
desc="A messaging conversation that plays out: typing-indicator dots, bubbles springing in on alternating sides, timestamps and the thread scrolling up as it grows. Use for AI assistant demos, customer support, testimonials as chats, dialogue-driven explainers, texting stories and 'ask it anything' product moments.",
look="A phone-sized chat column centred in frame. Incoming messages (white, left) are preceded by a three-dot typing bubble that bounces; outgoing (blue, right) pop straight in. Each bubble springs from its tail corner. As the thread fills, older messages slide up smoothly.",
beats=["0.3 s: message 1 (them) after 0.6 s of typing dots.",
       "1.6 s: reply (me).",
       "2.4–3.4 s: typing, then a longer answer.",
       "4.2 s: reply; 5.0–5.8 s typing, then final message with an emoji-free punchline.",
       "Thread scrolls to keep the newest bubble in view."],
build="""
A script list `[{who, text, at, typing}]`. For each message, visibility and spring scale come from `t - at` (`E.back` over 0.35 s, origin at the tail corner). The typing bubble shows during `[at - typing, at)` with three dots bouncing via phase-offset `sin`. Scroll: sum the heights of visible messages after measuring once, and ease the column's translateY to keep the latest bottom at a fixed line.
""",
knobs=["Script: who, text, times, typing durations.",
       "Bubble colours, corner radius, max width.",
       "Spring strength; scroll anchor line.",
       "Show/hide avatars and timestamps."],
pitfalls=["Measure bubble heights once after fonts load; never measure inside renderAt.",
          "Typing time should scale with message length (~25 ms/char) to feel real.",
          "Keep messages short; a chat is skimmed, not read."],
pairs=["typewriter", "command-palette", "notifications", "cursor-tour"],
css="""
.wrap { position:absolute; left:50%; top:90px; width:860px; height:900px; margin-left:-430px; overflow:hidden; border-radius:40px; background:#f7f8fb; box-shadow:0 40px 90px rgba(20,30,60,.18); }
.hdr { position:absolute; left:0; right:0; top:0; height:110px; background:#fff; display:flex; align-items:center; gap:22px; padding:0 34px; z-index:3; font:700 30px var(--mono); }
.hdr i { width:60px; height:60px; border-radius:50%; background:var(--accent); }
#col { position:absolute; left:0; right:0; top:130px; }
.m { position:absolute; max-width:600px; padding:24px 30px; border-radius:34px; font:500 30px/1.35 var(--mono); }
.them { left:34px; background:#fff; color:#111; border-bottom-left-radius:8px; transform-origin:0 100%; box-shadow:0 4px 12px rgba(0,0,0,.05); }
.me { right:34px; background:var(--blue); color:#fff; border-bottom-right-radius:8px; transform-origin:100% 100%; }
.typing { left:34px; width:120px; height:74px; padding:0; background:#fff; border-bottom-left-radius:8px; transform-origin:0 100%; }
.typing span { position:absolute; top:30px; width:14px; height:14px; border-radius:50%; background:#9aa0ab; }
""",
html="""<div class="wrap"><div class="hdr"><i></i>Studio Assistant</div><div id="col"></div></div>""",
js="""
const SCRIPT = [["them", "Hey! Want to make a launch video today?", 0.9, 0.6], ["me", "Yes. 15 seconds, bold type.", 1.6, 0],
  ["them", "Done. I wrote it as code, so every frame renders exactly the same.", 3.4, 1.0], ["me", "Can you make the logo land harder?", 4.2, 0],
  ["them", "Added a squash and a shockwave ring.", 5.8, 0.8]];
const col = $("#col"), msgs = [];
SCRIPT.forEach(([who, text, at, typ]) => { const d = document.createElement("div"); d.className = "m " + who; d.textContent = text; col.appendChild(d);
  let ty = null; if (typ) { ty = document.createElement("div"); ty.className = "m typing"; ty.innerHTML = "<span style='left:26px'></span><span style='left:53px'></span><span style='left:80px'></span>"; col.appendChild(ty); }
  msgs.push({ d, ty, at, typ, who }); });
let lay = null;
function layout() { let y = 0; lay = msgs.map(m => { const h = m.d.offsetHeight; const r = { y, h }; y += h + 22; return r; }); }
function renderAt(t) {
  if (!lay || document.fonts.status !== "loaded") layout();
  let bottom = 0;
  msgs.forEach((m, i) => { const L = lay[i], k = E.back(seg(t, m.at, m.at + 0.35)), vis = t >= m.at;
    m.d.style.top = `${L.y}px`; m.d.style.opacity = vis ? 1 : 0; m.d.style.transform = `scale(${vis ? k : 0})`;
    if (vis) bottom = L.y + L.h;
    if (m.ty) { const on = t >= m.at - m.typ && t < m.at; m.ty.style.top = `${L.y}px`; m.ty.style.opacity = on ? 1 : 0;
      m.ty.style.transform = `scale(${on ? E.back(seg(t, m.at - m.typ, m.at - m.typ + 0.25)) : 0})`;
      [...m.ty.children].forEach((s, j) => s.style.transform = `translateY(${-8 * Math.max(0, Math.sin(t * 9 - j * 0.9))}px)`);
      if (on) bottom = Math.max(bottom, L.y + 74); } });
  const target = Math.max(0, bottom - 700);
  col.style.transform = `translateY(${-target}px)`;
}
"""),

# ---------------------------------------------------------------- dot-wipe
dict(slug="dot-wipe", title="Dot Wipe", dur=4, bg="var(--paper)",
desc="A transition where a grid of dots swells from one point until it covers the screen, the scene switches underneath, and the dots shrink away to reveal the next scene. Use for scene and chapter transitions, before/after switches, brand-colour wipes, playful cuts and pattern-based reveals.",
look="Scene A (paper, ink headline) is overtaken by a wave of ink dots growing outward from the lower-left; they grow until they merge into solid ink. Behind the cover the scene changes; the dots then shrink in the same wave order, revealing Scene B (accent background, paper headline).",
beats=["0.0–0.6 s: Scene A holds.",
       "0.6–1.7 s: dots grow in a wave from the origin until full cover.",
       "1.7 s: scene swap (hidden).",
       "1.8–2.9 s: dots shrink in the same order, revealing Scene B.",
       "2.9–4.0 s: Scene B holds."],
build="""
Canvas overlay above two DOM scenes. Each dot's growth phase is `seg(t, a + d·k, a + d·k + 0.45)` where `d` is its distance to the origin. Radius goes to `cell·0.75` (≥ √2/2 of the cell, so neighbours overlap into full cover). Swap scene visibility at the instant every dot is fully grown. The shrink uses the same delays, so the wave reads as one gesture.
""",
knobs=["Origin point (corner, centre, a button's position).",
       "Cell size (bigger = chunkier, more graphic).",
       "Wave speed and per-dot growth time.",
       "Cover colour (ink, accent, or the next scene's colour)."],
pitfalls=["Max radius must be ≥ 0.71 × cell or gaps remain at full cover.",
          "Swap scenes only when the last dot is fully grown, or the swap flashes through.",
          "Use the same order for grow and shrink; reversing it looks like a rewind."],
pairs=["tile-grids", "halftone-wave", "before-after", "kinetic-type"],
css="""
.sc { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:210px; letter-spacing:-8px; }
#A { background:var(--paper); color:var(--ink); } #B { background:var(--accent); color:var(--paper); }
canvas { z-index:5; }
""",
html="""<div class="sc" id="A">Chapter one.</div><div class="sc" id="B">Chapter two.</div><canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), CELL = 80, ox = 0, oy = H, MAXD = Math.hypot(W, H), WAVE = 0.6, GROW = 0.45;
function renderAt(t) {
  g.clearRect(0, 0, W, H);
  const swapped = t >= 0.6 + WAVE + GROW;
  $("#A").style.visibility = swapped ? "hidden" : "visible"; $("#B").style.visibility = swapped ? "visible" : "hidden";
  g.fillStyle = C.ink;
  for (let y = CELL / 2; y < H + CELL; y += CELL) for (let x = CELL / 2; x < W + CELL; x += CELL) {
    const d = Math.hypot(x - ox, y - oy) / MAXD;
    const grow = E.inOut(seg(t, 0.6 + d * WAVE, 0.6 + d * WAVE + GROW)), shrink = E.inOut(seg(t, 1.8 + d * WAVE, 1.8 + d * WAVE + GROW));
    const r = CELL * 0.75 * grow * (1 - shrink); if (r <= 0.3) continue;
    g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
}
"""),

# ---------------------------------------------------------------- ribbon-twist
dict(slug="ribbon-twist", title="Ribbon Twist", dur=6, bg="var(--ink)",
desc="A two-sided 3D ribbon that flows across the frame along a wavy path, twisting so its front and back colours flip, drawn with depth-sorted quads on canvas. Use for flow and journey metaphors, brand ribbons, festive or premium openers, 'connecting the dots', transitions and elegant abstract showreel moments.",
look="A wide band snakes in from the left, following a sine-like path that drifts. Along its length it twists around its own centreline: one face is accent orange, the other is pale pink, so each half-twist flips the colour. Shading darkens faces turned away from the light. It draws on from the tail, then keeps flowing.",
beats=["0.0–1.8 s: ribbon draws on from the left edge (head advances along the path).",
       "Continuous: path phase flows; twist rate 2.5 turns across the ribbon.",
       "3.0–4.5 s: twist accelerates, then relaxes.",
       "Continuous: slight camera roll."],
build="""
Sample the centreline `c(u)` (u from 0 to 1) in 3D. At each sample, build a frame: tangent `T` (finite difference), a reference up vector, normal `N = up × T`, then rotate `N` around `T` by `twist(u, t)`. Edges are `c ± w·N`. Each quad between samples gets a face normal; its sign toward the camera picks the colour (front vs back) and its magnitude the shade. Sort quads by depth and fill back to front.
""",
knobs=["Path shape (amplitude, frequency, drift), ribbon width.",
       "Twist turns and acceleration.",
       "Front/back colours; shading strength.",
       "Draw-on speed."],
pitfalls=["Use a stable up vector (not parallel to the tangent) or the ribbon flips randomly.",
          "Depth-sort quads every frame; twisting changes order.",
          "Add a 1 px stroke in the fill colour to hide hairline seams between quads."],
pairs=["flow-line", "liquid-blob", "helix", "line-draw"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), NS = 160;
function renderAt(t) {
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  const head = E.inOut(seg(t, 0, 1.8)), tw = 2.5 + 1.5 * Math.sin(seg(t, 3, 4.5) * Math.PI), wdt = 70, roll = 0.06 * Math.sin(t * 0.7);
  const C3 = u => [(u - 0.5) * 2100, 260 * Math.sin(u * 7 + t * 1.3) + 80 * Math.sin(u * 3 - t), 220 * Math.cos(u * 5 + t * 0.9)];
  const pts = [];
  for (let s = 0; s <= NS; s++) { const u = s / NS; if (u > head) break;
    const c = C3(u), c2 = C3(u + 0.002), T = [c2[0] - c[0], c2[1] - c[1], c2[2] - c[2]], tl = Math.hypot(...T); T[0] /= tl; T[1] /= tl; T[2] /= tl;
    let N = [-T[1], T[0], 0], nl = Math.hypot(...N) || 1; N = N.map(v => v / nl); const B = [T[1] * N[2] - T[2] * N[1], T[2] * N[0] - T[0] * N[2], T[0] * N[1] - T[1] * N[0]];
    const a = u * tw * Math.PI * 2 + t * 1.5, ca = Math.cos(a), sa = Math.sin(a), D = [N[0] * ca + B[0] * sa, N[1] * ca + B[1] * sa, N[2] * ca + B[2] * sa];
    const e1 = [c[0] + D[0] * wdt, c[1] + D[1] * wdt, c[2] + D[2] * wdt], e2 = [c[0] - D[0] * wdt, c[1] - D[1] * wdt, c[2] - D[2] * wdt];
    pts.push([proj(rot(e1, 0, 0, roll), 1600), proj(rot(e2, 0, 0, roll), 1600)]); }
  const quads = [];
  for (let i = 0; i < pts.length - 1; i++) { const [a, b] = pts[i], [c, d] = pts[i + 1];
    const cross = (c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0]);
    quads.push({ z: a[2] + b[2] + c[2] + d[2], pts: [a, c, d, b], front: cross > 0, sh: clamp(Math.abs(cross) / 9000, 0.25, 1) }); }
  quads.sort((p, q) => p.z - q.z);
  for (const q of quads) { const col = q.front ? mix("#5a1406", C.accent, q.sh) : mix("#5b3a46", C.pink, q.sh);
    g.fillStyle = col; g.strokeStyle = col; g.lineWidth = 1; g.beginPath(); q.pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.closePath(); g.fill(); g.stroke(); }
}
"""),

# ---------------------------------------------------------------- seal-spin
dict(slug="seal-spin", title="Seal Spin", dur=5, bg="var(--yellow)",
desc="A circular badge seal with text running around its edge that stamps in with a punch, then spins slowly forever, with a scalloped border and a centre icon. Use for 'certified', 'new', 'limited edition', guarantees, awards, launch stickers, end cards, CTAs and premium brand marks.",
look="A scalloped sticker seal in ink with paper text running around the rim ('• LIMITED EDITION • MADE WITH CODE'). It slams in from 2.5× scale with a slight rotation and a shockwave ring, settles, then the text ring keeps rotating slowly while the centre star stays still.",
beats=["0.2–0.65 s: seal punches in (scale 2.5 → 1 with back ease, rotation −30° → 0).",
       "0.45–1.1 s: shockwave ring expands and fades.",
       "Continuous after 0.6 s: text ring rotates 30°/s; scallop edge rotates −10°/s.",
       "1.0–1.5 s: centre star pops in."],
build="""
SVG: a scalloped polygon (radius alternating with a sine of angle·n), a `<textPath>` on a circle path for the rim text, and a centre star. Group transforms: whole seal for the punch; inner groups for the counter-rotations. The rim text length should fill the circle exactly: set `textLength` to the path length so the start and end meet.
""",
knobs=["Rim text and font size; number of scallops.",
       "Rotation speeds (text vs. edge).",
       "Punch scale/rotation; shockwave on/off.",
       "Centre icon (star, logo, number)."],
pitfalls=["Set `textLength` to the circumference or there's a gap or overlap at the seam.",
          "Spin slowly (≤ 40°/s); fast spinning text is unreadable and strobes in video.",
          "Keep the seal's centre still while the rim spins: it anchors the eye."],
pairs=["logo-land", "shape-morph", "kinetic-type", "swiss-grid"],
css="""svg { position:absolute; inset:0; } .rim { font:700 40px var(--mono); letter-spacing:6px; fill:var(--paper); }""",
html="""
<svg viewBox="0 0 1920 1080">
  <circle id="shock" cx="960" cy="540" r="300" fill="none" stroke="#0e0e0e" stroke-width="10"/>
  <g id="seal" transform="translate(960 540)">
    <g id="edge"><path id="scal" fill="#0e0e0e"/></g>
    <g id="txt"><path id="cp" fill="none" d="M0,-250 a250,250 0 1,1 0,500 a250,250 0 1,1 0,-500"/>
      <text class="rim"><textPath href="#cp" id="tp">• LIMITED EDITION • MADE WITH CODE • EST. 2026 </textPath></text></g>
    <circle r="190" fill="none" stroke="#efe9df" stroke-width="3"/>
    <path id="star" fill="#ff4a1c"/>
  </g>
</svg>
""",
js="""
let d = ""; for (let i = 0; i <= 360; i++) { const a = i / 360 * Math.PI * 2, r = 320 + 14 * Math.cos(a * 24); d += (i ? "L" : "M") + (Math.cos(a) * r).toFixed(1) + "," + (Math.sin(a) * r).toFixed(1); }
$("#scal").setAttribute("d", d + "Z");
let s = ""; for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, r = i % 2 ? 62 : 150; s += (i ? "L" : "M") + (Math.cos(a) * r).toFixed(1) + "," + (Math.sin(a) * r).toFixed(1); }
$("#star").setAttribute("d", s + "Z");
$("#tp").setAttribute("textLength", (2 * Math.PI * 250 - 4).toFixed(1));
function renderAt(t) {
  const k = seg(t, 0.2, 0.65), sc = lerp(2.5, 1, E.back(k)), rotA = lerp(-30, 0, E.out(k));
  $("#seal").setAttribute("transform", `translate(960 540) rotate(${rotA}) scale(${k > 0 ? sc : 0})`);
  const sp = Math.max(0, t - 0.6);
  $("#txt").setAttribute("transform", `rotate(${sp * 30})`); $("#edge").setAttribute("transform", `rotate(${-sp * 10})`);
  const sk = seg(t, 0.45, 1.1); $("#shock").setAttribute("r", (300 + 380 * E.out(sk)).toFixed(1)); $("#shock").setAttribute("opacity", sk > 0 ? (1 - sk).toFixed(3) : 0);
  const st = E.back(seg(t, 1.0, 1.5)); $("#star").setAttribute("transform", `scale(${st}) rotate(${(1 - st) * -90})`);
}
"""),

# ---------------------------------------------------------------- command-palette
dict(slug="command-palette", title="Command Palette", dur=7, bg="#1b1d22",
desc="A ⌘K command palette opens over a blurred app, a query types in, results filter live, the highlight moves down with arrow presses and Enter fires the action with a toast. Use for developer tools, productivity apps, keyboard-first products, AI command bars, search features and power-user demos.",
look="A dimmed, blurred app UI in the background. A centred palette springs open with a search field; key caps '⌘' and 'K' flash at the bottom. Letters type in, the result list narrows with items collapsing, a highlight bar slides between results, then Enter: the palette closes and a success toast slides up.",
beats=["0.3 s: key caps ⌘ K flash; backdrop blurs and dims.",
       "0.5–0.9 s: palette scales from 0.96 and fades in.",
       "1.2–2.4 s: query 'depl' types; list filters from 6 to 2 items as letters arrive.",
       "2.8 s: highlight moves down to 'Deploy preview'; 3.3 s: back up to 'Deploy to production'.",
       "3.9 s: Enter: palette closes; 4.1–4.6 s toast slides up 'Deployed to production'."],
build="""
DOM. All results exist; each has a `match` time (when the typed query stops matching it). After that time it collapses (height and opacity to 0 over 0.2 s). The query string at time `t` is the prefix of 'depl' by keystroke times. The highlight's y is the eased position of the selected index among the visible rows. Backdrop blur is a CSS `filter: blur()` on the app layer (fine here: it's static UI, not footage).
""",
knobs=["Command list and query.",
       "Keystroke times; arrow presses; selected action.",
       "Theme (dark/light), accent colour.",
       "Toast text and position."],
pitfalls=["Filter results at the exact keystroke frames; lagging lists look broken.",
          "Animate list height changes; jumping rows lose the eye.",
          "Show key caps for keyboard actions, since viewers can't see a keyboard."],
pairs=["cursor-tour", "typewriter", "chat-thread", "scramble-decode"],
css="""
#app { position:absolute; inset:0; background:linear-gradient(135deg,#2a2e36,#1b1d22); }
#app i { position:absolute; border-radius:16px; background:#343944; }
#pal { position:absolute; left:50%; top:200px; width:960px; margin-left:-480px; border-radius:26px; background:#262a32; box-shadow:0 50px 120px rgba(0,0,0,.6);
  overflow:hidden; font-family:var(--mono); color:#e6e8ec; border:1px solid #3a3f4a; }
#q { height:110px; display:flex; align-items:center; padding:0 40px; font:500 40px var(--mono); border-bottom:1px solid #3a3f4a; }
#q span { color:#7d8494; } #car { width:3px; height:46px; background:var(--accent); margin-left:3px; }
.it { position:relative; height:90px; display:flex; align-items:center; gap:24px; padding:0 40px; font:500 32px var(--mono); overflow:hidden; z-index:1; }
.it b { width:44px; height:44px; border-radius:12px; background:#3a3f4a; flex:none; }
#hl { position:absolute; left:14px; right:14px; height:76px; border-radius:16px; background:rgba(255,74,28,.22); border:2px solid var(--accent); z-index:0; }
.kc { position:absolute; bottom:90px; width:110px; height:110px; border-radius:22px; background:#2f333c; border:2px solid #4a505d; color:#fff; font:700 54px/106px var(--mono); text-align:center; }
#toast { position:absolute; left:50%; bottom:80px; width:640px; margin-left:-320px; padding:30px 40px; border-radius:22px; background:#e9fbe0; color:#173b08; font:700 32px var(--mono); box-sizing:border-box; }
""",
html="""
<div id="app"><i style="left:60px;top:60px;width:340px;height:960px"></i><i style="left:440px;top:60px;width:1420px;height:140px"></i><i style="left:440px;top:240px;width:680px;height:400px"></i><i style="left:1160px;top:240px;width:700px;height:400px"></i><i style="left:440px;top:680px;width:1420px;height:340px"></i></div>
<div id="pal"><div id="q"><span id="qt"></span><i id="car"></i></div><div id="list" style="position:relative;padding:12px 0"><div id="hl"></div></div></div>
<div class="kc" id="k1" style="left:780px">⌘</div><div class="kc" id="k2" style="left:920px">K</div><div class="kc" id="k3" style="left:1060px;width:180px;font-size:34px">ENTER</div>
<div id="toast">✓ Deployed to production</div>
""",
js="""
const ITEMS = [["Deploy to production", 99], ["Deploy preview", 99], ["Open settings", 1.2], ["Duplicate project", 1.6], ["Invite teammate", 1.2], ["Export video", 1.85]];
const KEYS = [[1.2, "d"], [1.6, "e"], [1.85, "p"], [2.15, "l"]], list = $("#list"), rows = [];
ITEMS.forEach(([name, gone]) => { const d = document.createElement("div"); d.className = "it"; d.innerHTML = `<b></b>${name}`; list.appendChild(d); rows.push({ d, gone }); });
function renderAt(t) {
  const open = E.out(seg(t, 0.5, 0.9)), close = E.in(seg(t, 3.9, 4.15)), vis = open * (1 - close);
  $("#app").style.filter = `blur(${8 * E.out(seg(t, 0.3, 0.8))}px) brightness(${1 - 0.4 * E.out(seg(t, 0.3, 0.8))})`;
  $("#pal").style.opacity = vis; $("#pal").style.transform = `scale(${lerp(0.96, 1, open) * lerp(1, 0.97, close)})`;
  const q = KEYS.filter(k => t >= k[0]).map(k => k[1]).join(""); $("#qt").innerHTML = q || "<span>Type a command…</span>";
  $("#car").style.opacity = Math.floor(t * 2.5) % 2 || t < 2.4 ? 1 : 0;
  rows.forEach(r => { const k = E.inOut(seg(t, r.gone, r.gone + 0.2)); r.d.style.height = `${90 * (1 - k)}px`; r.d.style.opacity = 1 - k; });
  const row = E.inOut(seg(t, 2.8, 3.0)) - E.inOut(seg(t, 3.3, 3.5)), y = 12 + 7 + 90 * row;  // down to row 2, back up to row 1
  $("#hl").style.top = `${y}px`; $("#hl").style.opacity = t > 1.0 ? 1 : 0;
  const kp = (a, b) => { const k = seg(t, a, b); return k > 0 && k < 1 ? 1 - 0.1 * Math.sin(k * Math.PI) : 1; };
  [["#k1", 0.3], ["#k2", 0.35], ["#k3", 3.9]].forEach(([id, a]) => { const on = seg(t, a - 0.1, a + 0.5); $(id).style.opacity = on > 0 && on < 1 ? 1 : 0;
    $(id).style.transform = `scale(${kp(a, a + 0.18)})`; $(id).style.background = t > a && t < a + 0.2 ? C.accent : "#2f333c"; });
  const tk = E.back(seg(t, 4.1, 4.6)); $("#toast").style.transform = `translateY(${(1 - tk) * 200}px)`; $("#toast").style.opacity = clamp(tk);
}
"""),

# ---------------------------------------------------------------- tunnel-grid
dict(slug="tunnel-grid", title="Tunnel Grid", dur=6, bg="var(--ink)",
desc="An endless square tunnel of glowing grid lines rushing toward the camera, with rings, depth fog and a twist, like flying through a data corridor. Use for speed and momentum, 'deep dive', hyperspace/warp moments, transitions into a new section, tech openers and music-driven intense beats.",
look="Concentric square frames recede to a vanishing point, joined by longitudinal lines along the walls. They stream toward the viewer; near frames are bright accent and thick, far ones fade into the black. The tunnel slowly rotates and bends (vanishing point drifts), and the speed surges mid-clip.",
beats=["0.0–0.8 s: tunnel fades up from black, slow.",
       "0.8–2.5 s: speed ramps up.",
       "2.5–3.5 s: surge: fastest, twist increases.",
       "3.5–6.0 s: eases to a cruise; vanishing point drifts in a slow ellipse."],
build="""
Frames sit at `z = (i - travel) mod span`, so they recycle seamlessly; `travel` is the integral of speed over time (computed analytically from the speed curve, or as a sum of eased segments) so scrubbing is exact. Each frame is a square of half-size `s` at depth z projected with `f/z`, rotated by `twist·z + t·0.2`. The vanishing point offset is a function of z (bend). Longitudinal lines connect corresponding corners and midpoints across frames.
""",
knobs=["Tunnel shape (square, hexagon, circle) and frame spacing.",
       "Speed curve (cruise, surge) and twist.",
       "Bend amount (vanishing point drift).",
       "Colours and fog distance."],
pitfalls=["Derive travel from a closed-form integral of the speed curve, not from frame-to-frame accumulation.",
          "Skip frames with z below the near plane; they explode to infinity.",
          "High speed + many lines strobes in 30 fps video; render at 60 fps or reduce line count."],
pairs=["terrain-mesh", "torus-wire", "wave-dots", "kinetic-type"],
html="""<canvas id="cv"></canvas>""",
js="""
const g = ctx2d("cv"), SPAN = 30, NF = 30;
// speed(t) = 2 + 10*ramp + 14*surge ; travel = ∫ speed dt, integrated numerically from 0 with a fixed step (deterministic)
function travelAt(t) { let s = 0; const dt = 1 / 240; for (let x = 0; x < t; x += dt) { const sp = 2 + 8 * E.inOut(seg(x, 0.8, 2.5)) + 12 * Math.sin(Math.PI * seg(x, 2.5, 3.8)) - 4 * E.inOut(seg(x, 3.5, 6)); s += sp * Math.min(dt, t - x); } return s; }
function renderAt(t) {
  g.fillStyle = C.ink; g.fillRect(0, 0, W, H);
  const tr = travelAt(t), fade = E.out(seg(t, 0, 0.8)), twist = 0.02 + 0.03 * Math.sin(Math.PI * seg(t, 2.5, 3.8)), f = 700;
  const frames = [];
  for (let i = 0; i < NF; i++) { const z = ((i - tr) % SPAN + SPAN) % SPAN + 0.6;
    const bx = Math.cos(t * 0.5) * 18 * z, by = Math.sin(t * 0.4) * 12 * z, a = twist * z + t * 0.2, s = 380;
    const corners = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]].map(([cx, cy]) => { const x = cx * s, y = cy * s;
      const rx = x * Math.cos(a) - y * Math.sin(a), ry = x * Math.sin(a) + y * Math.cos(a); return [W / 2 + (rx + bx) * f / (z * 100), H / 2 + (ry + by) * f / (z * 100)]; });
    frames.push({ z, corners }); }
  frames.sort((a, b) => b.z - a.z);
  for (let i = 1; i < frames.length; i++) { const A = frames[i - 1], B = frames[i]; if (B.z > A.z) continue; const near = clamp(1 - B.z / SPAN);
    g.strokeStyle = `rgba(239,233,223,${0.25 * near ** 2 * fade})`; g.lineWidth = 1;
    for (let k = 0; k < 8; k++) { g.beginPath(); g.moveTo(...A.corners[k]); g.lineTo(...B.corners[k]); g.stroke(); } }
  for (const F of frames) { const near = clamp(1 - F.z / SPAN);
    g.strokeStyle = near > 0.8 ? `rgba(255,74,28,${fade})` : `rgba(255,74,28,${near ** 2 * fade})`; g.lineWidth = 1 + 5 * near ** 3;
    g.beginPath(); [0, 2, 4, 6].forEach((k, j) => j ? g.lineTo(...F.corners[k]) : g.moveTo(...F.corners[k])); g.closePath(); g.stroke(); }
}
"""),
]
