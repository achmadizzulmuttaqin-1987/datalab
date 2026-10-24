/* ============================================================
   DUAL PERSONA — mesin suara
   Web Audio untuk efek & melodi, Web Speech untuk suara karakter.
   Tidak ada berkas audio eksternal, jadi tetap ringan & offline-ready.
   ============================================================ */

const Sound = (() => {
  let ctx = null;
  let master = null;
  let enabled = true;
  let voiceEnabled = true;
  let voices = [];

  function ensure() {
    if (!ctx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return null;
      ctx = new AC();
      master = ctx.createGain();
      master.gain.value = 0.35;
      master.connect(ctx.destination);
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  function loadVoices() {
    if (!('speechSynthesis' in window)) return;
    voices = window.speechSynthesis.getVoices() || [];
  }
  if ('speechSynthesis' in window) {
    loadVoices();
    window.speechSynthesis.onvoiceschanged = loadVoices;
  }

  /* ---------- primitif ---------- */
  function tone({ freq = 440, type = 'sine', dur = 0.2, gain = 0.3, delay = 0,
                  slide = 0, attack = 0.01, pan = 0 } = {}) {
    const c = ensure();
    if (!c || !enabled) return;
    const t0 = c.currentTime + delay;
    const osc = c.createOscillator();
    const g = c.createGain();
    const p = c.createStereoPanner ? c.createStereoPanner() : null;

    osc.type = type;
    osc.frequency.setValueAtTime(freq, t0);
    if (slide) osc.frequency.exponentialRampToValueAtTime(Math.max(30, freq + slide), t0 + dur);

    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(Math.max(gain, 0.0002), t0 + attack);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);

    osc.connect(g);
    if (p) { p.pan.value = pan; g.connect(p); p.connect(master); }
    else g.connect(master);

    osc.start(t0);
    osc.stop(t0 + dur + 0.05);
  }

  function noiseBurst({ dur = 0.16, gain = 0.18, delay = 0, hp = 900 } = {}) {
    const c = ensure();
    if (!c || !enabled) return;
    const t0 = c.currentTime + delay;
    const frames = Math.floor(c.sampleRate * dur);
    const buf = c.createBuffer(1, frames, c.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < frames; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / frames, 2.2);
    }
    const src = c.createBufferSource();
    src.buffer = buf;
    const filter = c.createBiquadFilter();
    filter.type = 'highpass';
    filter.frequency.value = hp;
    const g = c.createGain();
    g.gain.value = gain;
    src.connect(filter); filter.connect(g); g.connect(master);
    src.start(t0);
  }

  /* ---------- karakter ---------- */
  const PALETTE = {
    ren:   { notes: [523.25, 659.25, 783.99, 1046.5], type: 'sine', tail: 'triangle' },
    amira: { notes: [587.33, 739.99, 880.0, 1174.66], type: 'triangle', tail: 'sine' },
  };
  const ALIAS = { silver: 'ren', gold: 'amira' };
  const paletteOf = (who) => PALETTE[ALIAS[who] || who] || PALETTE.ren;

  function tap(who = 'ren') {
    const p = paletteOf(who);
    const base = p.notes[Math.floor(Math.random() * p.notes.length)];
    tone({ freq: base, type: p.type, dur: 0.18, gain: 0.22, slide: who === 'amira' ? 90 : -60 });
    tone({ freq: base * 2, type: p.tail, dur: 0.5, gain: 0.07, delay: 0.03 });
    noiseBurst({ dur: 0.1, gain: 0.05, hp: 2400 });
  }

  function chime(who = 'ren', step = 0) {
    const p = paletteOf(who);
    const note = p.notes[step % p.notes.length];
    tone({ freq: note, type: p.tail, dur: 0.5, gain: 0.14 });
    tone({ freq: note * 1.5, type: 'sine', dur: 0.4, gain: 0.06, delay: 0.06 });
  }

  function whoosh() {
    noiseBurst({ dur: 0.42, gain: 0.12, hp: 380 });
    tone({ freq: 220, type: 'sine', dur: 0.35, gain: 0.05, slide: 180 });
  }

  function flash() {
    noiseBurst({ dur: 0.09, gain: 0.14, hp: 3000 });
    tone({ freq: 1200, type: 'square', dur: 0.05, gain: 0.04 });
  }

  function heart() {
    tone({ freq: 880, type: 'sine', dur: 0.14, gain: 0.12 });
    tone({ freq: 1174.66, type: 'sine', dur: 0.3, gain: 0.09, delay: 0.09 });
  }

  function deny() {
    tone({ freq: 180, type: 'sawtooth', dur: 0.14, gain: 0.07, slide: -50 });
  }

  /* Melodi "humming" singkat, berbeda per karakter. */
  const MELODIES = {
    ren:   [392.0, 440.0, 523.25, 466.16, 392.0, 349.23, 392.0],
    amira: [523.25, 587.33, 659.25, 587.33, 523.25, 659.25, 783.99],
  };

  function hum(who = 'ren', onNote) {
    const seq = MELODIES[ALIAS[who] || who] || MELODIES.ren;
    const p = paletteOf(who);
    const beat = who === 'amira' ? 0.26 : 0.32;
    seq.forEach((f, i) => {
      const delay = i * beat;
      tone({ freq: f, type: p.type, dur: beat * 1.5, gain: 0.16, delay });
      tone({ freq: f * 2, type: 'sine', dur: beat * 1.2, gain: 0.04, delay: delay + 0.02 });
      if (onNote) window.setTimeout(() => onNote(i, seq.length), delay * 1000);
    });
    return seq.length * beat;
  }

  function fanfare(who = 'ren') {
    const p = paletteOf(who);
    [0, 2, 3, 4].forEach((n, i) => {
      tone({ freq: p.notes[n % p.notes.length], type: p.tail, dur: 0.45, gain: 0.13, delay: i * 0.12 });
    });
  }

  /* ---------- suara manusia ---------- */
  function speak(text, char) {
    if (!voiceEnabled || !enabled || !('speechSynthesis' in window) || !text) return;
    try {
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      const cfg = (char && char.voice) || { pitch: 1, rate: 1, lang: 'id-ID' };
      u.lang = cfg.lang || 'id-ID';
      u.pitch = cfg.pitch;
      u.rate = cfg.rate;
      u.volume = 0.95;

      const ind = voices.filter(v => /^id/i.test(v.lang) || /indone/i.test(v.name));
      if (ind.length) {
        const byGender = ind.filter(v => new RegExp(cfg.prefer, 'i').test(v.name));
        u.voice = (byGender[0] || ind[0]);
      }
      window.speechSynthesis.speak(u);
    } catch (err) { /* diam saja, teks tetap tampil */ }
  }

  function stopSpeech() {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  }

  return {
    unlock: ensure,
    tone, chime, tap, whoosh, flash, heart, deny, hum, fanfare, speak, stopSpeech,
    get enabled() { return enabled; },
    set enabled(v) {
      enabled = v;
      if (!v) stopSpeech();
      if (master) master.gain.value = v ? 0.35 : 0;
    },
    get voiceEnabled() { return voiceEnabled; },
    set voiceEnabled(v) {
      voiceEnabled = v;
      if (!v) stopSpeech();
    },
    get hasSpeech() { return 'speechSynthesis' in window; },
  };
})();

window.Sound = Sound;
