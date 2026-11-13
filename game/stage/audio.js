/* Gaston Grandiose's Shadow Dept. — all music and sound effects are synthesised here (no audio files, no licences needed). */
const AU = (() => {
  let ctx = null, master, musicBus, sfxBus, verb, musicOn = true, sfxOn = true, playing = false, timer = null, nextT = 0, step = 0, duck = 1;
  const BEAT = 0.34;                       // quarter note (3/4 waltz ~176 bpm)
  const mtof = m => 440 * Math.pow(2, (m - 69) / 12);

  function init() {
    if (ctx) return;
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    master = ctx.createGain(); master.gain.value = .9; master.connect(ctx.destination);
    // small hall reverb from a generated impulse
    verb = ctx.createConvolver(); const len = ctx.sampleRate * 2.2, ir = ctx.createBuffer(2, len, ctx.sampleRate);
    for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 3.2); }
    verb.buffer = ir; const vg = ctx.createGain(); vg.gain.value = .22; verb.connect(vg); vg.connect(master);
    musicBus = ctx.createGain(); musicBus.gain.value = 0; musicBus.connect(master); musicBus.connect(verb);
    sfxBus = ctx.createGain(); sfxBus.gain.value = 1; sfxBus.connect(master); sfxBus.connect(verb);
  }
  function unlock() { init(); loadAll(); if (ctx.state === 'suspended') ctx.resume(); if (musicOn && !playing) startMusic(); }
  const now = () => ctx.currentTime;
  const noiseBuf = (() => { let b = null; return () => { if (b) return b; const n = ctx.sampleRate * 2; b = ctx.createBuffer(1, n, ctx.sampleRate); const d = b.getChannelData(0); for (let i = 0; i < n; i++) d[i] = Math.random() * 2 - 1; return b; }; })();
  function noise(t, dur, { type = 'bandpass', f = 1000, q = 1, f2 = null, g = .5, a = .005, rel = null, bus = sfxBus } = {}) {
    const s = ctx.createBufferSource(); s.buffer = noiseBuf(); s.loop = true;
    const fl = ctx.createBiquadFilter(); fl.type = type; fl.frequency.setValueAtTime(f, t); fl.Q.value = q; if (f2) fl.frequency.exponentialRampToValueAtTime(f2, t + dur);
    const e = ctx.createGain(); e.gain.setValueAtTime(0, t); e.gain.linearRampToValueAtTime(g, t + a); e.gain.exponentialRampToValueAtTime(.0001, t + (rel || dur));
    s.connect(fl); fl.connect(e); e.connect(bus); s.start(t, Math.random()); s.stop(t + (rel || dur) + .05);
  }
  function tone(t, freq, dur, { type = 'sine', g = .3, a = .005, bus = sfxBus, f2 = null } = {}) {
    const o = ctx.createOscillator(); o.type = type; o.frequency.setValueAtTime(freq, t); if (f2) o.frequency.exponentialRampToValueAtTime(f2, t + dur);
    const e = ctx.createGain(); e.gain.setValueAtTime(0, t); e.gain.linearRampToValueAtTime(g, t + a); e.gain.exponentialRampToValueAtTime(.0001, t + dur);
    o.connect(e); e.connect(bus); o.start(t); o.stop(t + dur + .05);
  }

  /* ---------- music: an original fairground waltz on a calliope ---------- */
  // melody [midi, beats]; 16 bars of 3/4 = 48 beats
  const MEL = [[67,1],[72,1],[76,1],[79,2],[76,1],[77,1],[76,1],[74,1],[72,2],[67,1],
               [69,1],[72,1],[77,1],[81,2],[77,1],[79,1],[77,1],[76,1],[74,3],
               [67,1],[71,1],[74,1],[77,2],[74,1],[76,1],[74,1],[72,1],[71,2],[67,1],
               [72,1],[76,1],[79,1],[84,2],[83,.5],[81,.5],[79,1],[76,1],[74,1],[72,3]];
  const ROOT = [48,48,43,48,41,41,48,43, 43,43,48,43,48,45,43,48];          // bass roots per bar
  const CH = { 48:[60,64,67], 43:[59,62,67], 41:[60,65,69], 45:[60,64,69] };   // chord voicings
  const events = []; { let b = 0; for (const [m, d] of MEL) { events.push({ b, m, d }); b += d; } }
  function calliope(t, freq, dur, g) {
    const out = ctx.createGain(); out.gain.setValueAtTime(0, t); out.gain.linearRampToValueAtTime(g, t + .015);
    out.gain.setValueAtTime(g * .8, t + dur * .7); out.gain.exponentialRampToValueAtTime(.0001, t + dur * .98);
    const trem = ctx.createOscillator(), tg = ctx.createGain(); trem.frequency.value = 6.2; tg.gain.value = g * .25; trem.connect(tg); tg.connect(out.gain);
    for (const [mult, type, lv] of [[1, 'square', .28], [2, 'triangle', .5], [1.003, 'sawtooth', .12]]) {
      const o = ctx.createOscillator(); o.type = type; o.frequency.value = freq * mult; const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 3200;
      const og = ctx.createGain(); og.gain.value = lv; o.connect(lp); lp.connect(og); og.connect(out); o.start(t); o.stop(t + dur + .05);
    }
    trem.start(t); trem.stop(t + dur + .05); out.connect(musicBus);
  }
  function scheduleBeat(t, beatIdx) {
    const bar = Math.floor(beatIdx / 3) % 16, inBar = beatIdx % 3, beat48 = beatIdx % 48;
    if (inBar === 0) { tone(t, mtof(ROOT[bar] - 12), BEAT * .9, { type: 'triangle', g: .5, bus: musicBus }); tone(t, mtof(ROOT[bar]), BEAT * .7, { type: 'square', g: .07, bus: musicBus }); noise(t, .05, { f: 180, q: .8, g: .25, bus: musicBus }); }
    else for (const m of CH[ROOT[bar]]) tone(t, mtof(m - 12), BEAT * .45, { type: 'square', g: .035, bus: musicBus });
    for (const ev of events) if (ev.b >= beat48 && ev.b < beat48 + 1) calliope(t + (ev.b - beat48) * BEAT, mtof(ev.m), ev.d * BEAT, .11);
  }
  function startMusic() {
    if (!ctx || playing) return; playing = true; nextT = now() + .1; step = 0;
    musicBus.gain.cancelScheduledValues(now()); musicBus.gain.setTargetAtTime(.55 * duck, now(), .4);
    timer = setInterval(() => { while (nextT < now() + .25) { scheduleBeat(nextT, step); nextT += BEAT; step++; } }, 60);
  }
  function stopMusic() { if (!playing) return; playing = false; clearInterval(timer); musicBus.gain.setTargetAtTime(0, now(), .15); }
  function setDuck(v) { duck = v; if (ctx && playing) musicBus.gain.setTargetAtTime(.55 * v, now(), .5); }

  /* ---------- sound effects: recorded clips (Pixabay, Pixabay Content Licence) ---------- */
  const NAMES = ['boo','cry','crickets','hmm','applause','cheer','screams','laugh','laughbig','tick','drumroll','crash','lamp','curtain','splat','whoosh','ding','click'];
  const BUF = {}; let loading = false;
  function loadAll() { if (loading) return; loading = true;
    for (const n of NAMES) fetch('../assets/sfx/' + n + '.mp3').then(r => r.arrayBuffer()).then(b => ctx.decodeAudioData(b)).then(d => BUF[n] = d).catch(() => {}); }
  function clip(n, { g = 1, rate = 1, delay = 0 } = {}) { const b = BUF[n]; if (!b) return;
    const s = ctx.createBufferSource(); s.buffer = b; s.playbackRate.value = rate; const v = ctx.createGain(); v.gain.value = g; s.connect(v); v.connect(sfxBus); s.start(now() + delay); }
  const fx = {
    click() { clip('click', { g: .7 }); },
    swish() { clip('curtain', { g: .9 }); },
    clunk() { clip('lamp', { g: 1 }); },
    drumroll() { clip('drumroll', { g: .9 }); },
    crash() { clip('crash', { g: .8 }); },
    ding(i = 0) { clip('ding', { g: .7, rate: 1 + i * .12 }); },
    applause(level = 1) { clip('applause', { g: .85 }); if (level > .8) clip('cheer', { g: level > 1.2 ? 1 : .7, delay: .15 }); },
    booLoud() { clip('boo', { g: 1.25 }); clip('boo', { g: .8, rate: .94, delay: .35 }); },
    boo() { clip('boo', { g: 1 }); },
    crickets() { clip('crickets', { g: .9 }); },
    murmur() { clip('crickets', { g: .7 }); },
    hmm() { clip('hmm', { g: 1 }); },
    laugh(level = 1) { clip(level > 1 ? 'laughbig' : 'laugh', { g: 1 }); },
    sob() { clip('cry', { g: 1 }); },
    screams() { clip('screams', { g: .55 }); },
    whoosh() { clip('whoosh', { g: .6, rate: .9 + Math.random() * .25 }); },
    splat() { clip('splat', { g: .9, rate: .85 + Math.random() * .3 }); },
    tick(v = 0) { clip('tick', { g: .55, rate: (v ? 1.18 : 1) * (.94 + Math.random() * .12) }); },
  };
  const play = (name, ...a) => { if (!ctx || !sfxOn) return; try { fx[name](...a); } catch (e) { } };
  return {
    unlock, play, setDuck, _test(n, ...a) { init(); loadAll(); return fx[n](...a); }, _loaded() { return Object.keys(BUF); },
    setMusic(on) { musicOn = on; if (!ctx) return; on ? startMusic() : stopMusic(); },
    setSfx(on) { sfxOn = on; },
  };
})();
window.AU = AU;
