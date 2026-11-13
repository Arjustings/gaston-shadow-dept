// Records scripted gameplay for the trailer: props glide from their parked spots to the solution,
// Ready is pressed, the reveal and the Gazette review play out. Real game, real renders.
//   node trailer/record.mjs <out-name> <level> [miss]    (miss = stop short so the crowd boos)
// Frames come from a CDP screencast (real timestamps), stitched to 30 fps by ffmpeg.
import { createRequire } from 'module';
import { mkdirSync, writeFileSync, rmSync } from 'fs';
import { execFileSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
const require = createRequire(import.meta.url)  // npm i playwright-core;
const { chromium } = require('playwright-core');

const [name = 'play', lvl = '2', miss] = process.argv.slice(2);
const OUT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), 'gameplay');
const FR = path.join(OUT, name + '_frames');
rmSync(FR, { recursive: true, force: true }); mkdirSync(FR, { recursive: true });

const browser = await chromium.launch({ headless: false, executablePath: process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  args: ['--window-size=1920,1080', '--autoplay-policy=no-user-gesture-required', '--hide-scrollbars'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await page.addInitScript(() => { try { localStorage.setItem('sd-story', '1'); localStorage.setItem('sd-opts', JSON.stringify({ music: false, sfx: false, flash: true })) } catch (e) {} });
await page.goto(`http://localhost:8821/stage/index.html?lvl=${+lvl + 1}`);
await page.waitForFunction(() => window.__g && window.__g.props.length > 0, null, { timeout: 60000 });
await page.waitForTimeout(2500);

const cdp = await page.context().newCDPSession(page);
const frames = [];
cdp.on('Page.screencastFrame', async f => {
  frames.push({ t: f.metadata.timestamp, d: f.data });
  cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(() => {});
});
await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 92, maxWidth: 1920, maxHeight: 1080, everyNthFrame: 1 });

await page.waitForTimeout(1800);                              // Gaston's line on screen
await page.evaluate(() => window.__g.start());                // "To work!": curtain parts, camera glides to the lamp
await page.waitForTimeout(3600);

// glide each prop in turn from where it sits to its solved pose (eased), like a quick player
await page.evaluate(async (miss) => {
  const g = window.__g, ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const list = g.props.map(p => ({ p, a: { ...p.s }, b: { ...p.sol } }));
  if (miss) list.forEach((o, i) => { o.b = { ...o.b, x: o.b.x + (i % 2 ? 3.2 : -3.0), y: o.b.y + (i % 3 - 1) * 1.4, roll: o.b.roll + (i % 2 ? 1.6 : -1.3) }; });
  for (const o of list) {
    const dur = 900, t0 = performance.now();
    for (;;) {
      const k = Math.min(1, (performance.now() - t0) / dur), e = ease(k), s = {};
      for (const key of ['x', 'y', 'roll', 'yaw']) if (o.a[key] !== undefined && o.b[key] !== undefined) s[key] = o.a[key] + (o.b[key] - o.a[key]) * e;
      g.setState(o.p, s);
      if (k >= 1) break;
      await new Promise(r => requestAnimationFrame(r));
    }
    await sleep(150);
  }
}, !!miss);
await page.waitForTimeout(700);
await page.click('#ready');                                  // lamp on, camera swings to the audience, review unrolls
await page.waitForTimeout(miss ? 11000 : 10000);
await cdp.send('Page.stopScreencast');
await browser.close();

// write frames + an ffconcat list with the real gaps between them
let list = 'ffconcat version 1.0\n';
frames.forEach((f, i) => {
  const fn = `f${String(i).padStart(5, '0')}.jpg`;
  writeFileSync(path.join(FR, fn), Buffer.from(f.d, 'base64'));
  const dur = i < frames.length - 1 ? Math.max(0.001, frames[i + 1].t - f.t) : 0.04;
  list += `file ${fn}\nduration ${dur.toFixed(4)}\n`;
});
writeFileSync(path.join(FR, 'list.txt'), list);
const mp4 = path.join(OUT, name + '.mp4');
execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', path.join(FR, 'list.txt'), '-vf', 'fps=30,scale=1920:1080:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', mp4]);
console.log(name, frames.length, 'frames', ((frames.at(-1).t - frames[0].t)).toFixed(1) + 's ->', mp4);
