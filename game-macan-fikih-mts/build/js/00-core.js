/* =====================================================================
   00 · Inti: utilitas, data, penyimpanan, audio, konfigurasi tampilan
   ===================================================================== */
const $ = (sel, root) => (root || document).querySelector(sel);
const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const easeInOut = t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const easeOut = t => 1 - Math.pow(1 - t, 3);
const isMobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent) ||
  (window.matchMedia && window.matchMedia('(max-width: 820px)').matches);
const REDUCED = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}
function romanGrade(g) { return g === 7 ? 'VII' : g === 8 ? 'VIII' : 'IX'; }
function gradeLabel(g) { return 'Kelas ' + romanGrade(g); }
function starSVG(cls) {
  return '<span class="star ' + (cls || '') + '"><svg viewBox="0 0 24 24"><use href="#i-star"/></svg></span>';
}
function starRow(n, total, big) {
  let h = '';
  for (let i = 0; i < (total || 3); i++) h += starSVG(i < n ? 'on' : '');
  return h;
}
function formatNumber(n) { return new Intl.NumberFormat('id-ID').format(n); }

/* ---------- Data ---------- */
const DATA = JSON.parse($('#game-data').textContent);
const BABS = DATA.babs;
const N_CAVES = BABS.length * 5;
const CAVES = [];
BABS.forEach((bab, bi) => {
  bab.caves.forEach((qs, k) => {
    CAVES.push({
      idx: CAVES.length,            // 0-based
      no: CAVES.length + 1,         // 1-based untuk tampilan
      bi, bab, k, qs,
    });
  });
});
if (CAVES.length !== 150) console.warn('Jumlah goa tidak 150:', CAVES.length);

function caveInfo(i) { return CAVES[clamp(i, 0, N_CAVES - 1)]; }
function babStartCave(bi) { return bi * 5; }

/* ---------- Simpanan ---------- */
const SAVE_KEY = 'jejak-cilik-fikih-v1';
function defaultState() {
  return {
    v: 1,
    frontier: 0,
    cave: 0,
    stars: new Array(N_CAVES).fill(0),
    best: new Array(N_CAVES).fill(-1),
    style: 'sumatera',
    biome: 'starlight',
    sound: true,
    cinema: true,
    keys: true,
    visits: new Array(N_CAVES).fill(0),
    finished: false,
  };
}
function loadState() {
  const d = defaultState();
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    if (!raw) return d;
    const saved = JSON.parse(raw);
    const out = { ...d, ...saved };
    out.frontier = clamp(Number(saved.frontier) || 0, 0, N_CAVES - 1);
    out.cave = clamp(Number(saved.cave) || 0, 0, out.frontier);
    out.stars = Array.from({ length: N_CAVES }, (_, i) => clamp(Number((saved.stars || [])[i]) || 0, 0, 3));
    out.best = Array.from({ length: N_CAVES }, (_, i) => {
      const b = Number((saved.best || [])[i]);
      return Number.isFinite(b) ? clamp(b, -1, 10) : -1;
    });
    out.visits = Array.from({ length: N_CAVES }, (_, i) => Number((saved.visits || [])[i]) || 0);
    if (!SKINS[out.style]) out.style = d.style;
    if (!BIOMES[out.biome]) out.biome = d.biome;
    out.sound = out.sound !== false;
    out.cinema = out.cinema !== false;
    out.keys = out.keys !== false;
    out.finished = !!saved.finished;
    return out;
  } catch (e) {
    console.warn('Gagal memuat progres:', e);
    return d;
  }
}
let state = loadState();
let saveTimer = 0;
function saveState() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    try {
      localStorage.setItem(SAVE_KEY, JSON.stringify(state));
    } catch (e) { /* mode privat / kuota penuh */ }
  }, 120);
}
function saveNow() {
  clearTimeout(saveTimer);
  try { localStorage.setItem(SAVE_KEY, JSON.stringify(state)); } catch (e) {}
}
function starsFor(correct) {
  if (correct >= 10) return 3;
  if (correct >= 8) return 2;
  if (correct === 7) return 1;
  return 0;
}
function totalStars() { return state.stars.reduce((a, b) => a + b, 0); }
function passedCount() { return state.stars.filter(s => s >= 2).length; }
function isPassed(i) { return (state.stars[i] || 0) >= 2; }
function hasAnyProgress() {
  return state.frontier > 0 || state.cave > 0 || state.stars.some(s => s > 0) ||
    state.best.some(b => b >= 0);
}

/* ---------- Konfigurasi tampilan ---------- */
const SKINS = {
  sumatera: {
    key: 'sumatera', name: 'Si Belang Sumatera', short: 'Oranye klasik',
    desc: 'Bulu oranye hangat, belang hitam tegas, syal petualang zamrud.',
    swatch: '#f97316',
    fur: '#f97316', furDark: '#c2410c', stripe: '#1c1917', belly: '#fff7ed',
    eye: '#34d399', nose: '#fb7185', cheek: '#fda4af', inner: '#fda4af',
    scarf: '#059669', hat: null, vest: null, pack: null, head: 1.0, body: 1.0, chibi: false,
  },
  white: {
    key: 'white', name: 'Si Salju Benggala', short: 'Putih salju',
    desc: 'Macan putih keperakan, mata biru safir, topi petualang emas.',
    swatch: '#e2e8f0',
    fur: '#f1f5f9', furDark: '#cbd5e1', stripe: '#64748b', belly: '#ffffff',
    eye: '#38bdf8', nose: '#fb7185', cheek: '#f9a8d4', inner: '#fbcfe8',
    scarf: null, hat: '#f59e0b', vest: null, pack: null, head: 1.02, body: 1.0, chibi: false,
  },
  royal: {
    key: 'royal', name: 'Si Raja Rimba Cilik', short: 'Emas & ransel',
    desc: 'Bulu emas madu, rompi petualang hijau, ransel bintang ilmu.',
    swatch: '#fbbf24',
    fur: '#fbbf24', furDark: '#d97706', stripe: '#451a03', belly: '#fef3c7',
    eye: '#d97706', nose: '#fb7185', cheek: '#fda4af', inner: '#fda4af',
    scarf: null, hat: null, vest: '#065f46', pack: '#b45309', head: 1.0, body: 1.0, chibi: false,
  },
  chibi: {
    key: 'chibi', name: 'Si Chibi Gembul', short: 'Kartun kepala besar',
    desc: 'Kepala super bulat, pipi gembul, telapak pink, syal merah.',
    swatch: '#fb923c',
    fur: '#fb923c', furDark: '#ea580c', stripe: '#292524', belly: '#ffedd5',
    eye: '#34d399', nose: '#f43f5e', cheek: '#fb7185', inner: '#fb7185',
    scarf: '#e11d48', hat: null, vest: null, pack: null, head: 1.34, body: 0.9, chibi: true,
  },
};

const BIOMES = {
  starlight: {
    key: 'starlight', name: 'Bukit Malam Berbintang', short: 'Malam aurora',
    desc: 'Langit biru malam, bulan sabit, aurora ungu-toska, jamur bercahaya.',
    skyTop: '#060d20', skyMid: '#1d1c46', skyBot: '#4a3175',
    fog: '#1e2a44', fogDensity: 0.0024,
    grass: '#2f7d6c', grass2: '#276b5c', cliff: '#44596e', cliff2: '#5c7288',
    rock: '#5a7186', caveRock: '#39495b', portal: '#04070d', glow: '#fbbf24',
    crystal: '#a78bfa', tree: '#12655c', tree2: '#167066', trunk: '#4a3728',
    light: '#c9d6ff', hemiSky: '#7b8fe0', hemiGround: '#0d1626', amb: 1.35, sun: 1.85,
    stars: 1, moon: true, aurora: true, clouds: 0, fireflies: true, rainbow: false, emissive: 0.5,
    swatch: 'linear-gradient(180deg,#040a18 0%,#141335 55%,#3b2360 100%)',
    swatchHill: '#1c4d48',
  },
  emerald: {
    key: 'emerald', name: 'Bukit Zamrud Tropis', short: 'Siang hijau',
    desc: 'Siang cerah, terasering hijau, air terjun, kristal emas di goa.',
    skyTop: '#3d9ee8', skyMid: '#8ed0f4', skyBot: '#e7f6ec',
    fog: '#a8dcc4', fogDensity: 0.0022,
    grass: '#2fa96b', grass2: '#25915a', cliff: '#6b6a55', cliff2: '#8a8267',
    rock: '#8a7a62', caveRock: '#6b5d49', portal: '#06120d', glow: '#fbbf24',
    crystal: '#fbbf24', tree: '#1e7a4b', tree2: '#2b8f59', trunk: '#6b4426',
    light: '#fff5d6', hemiSky: '#cdeeff', hemiGround: '#294b38', amb: 0.7, sun: 1.55,
    stars: 0, moon: false, aurora: false, clouds: 1, fireflies: false, rainbow: false, emissive: 0.05,
    swatch: 'linear-gradient(180deg,#3d9ee8 0%,#9bd8f7 62%,#e7f6ec 100%)',
    swatchHill: '#2f9e63',
  },
  sunset: {
    key: 'sunset', name: 'Pegunungan Senja Emas', short: 'Sore keemasan',
    desc: 'Langit jingga-ungu, lentera hangat, kristal amber di mulut goa.',
    skyTop: '#3b2a6b', skyMid: '#d75a55', skyBot: '#f6b26b',
    fog: '#c07a68', fogDensity: 0.0024,
    grass: '#a8622f', grass2: '#8d4f26', cliff: '#5b4038', cliff2: '#6b4b3e',
    rock: '#6d4a3c', caveRock: '#4a332c', portal: '#120705', glow: '#fbbf24',
    crystal: '#f97316', tree: '#8a3d1e', tree2: '#9a4724', trunk: '#4a2a1c',
    light: '#ffd7a8', hemiSky: '#ffbe8a', hemiGround: '#3a1c1c', amb: 0.62, sun: 1.3,
    stars: 0.22, moon: false, aurora: false, clouds: 0.7, fireflies: true, rainbow: false, emissive: 0.12,
    swatch: 'linear-gradient(180deg,#3b2a6b 0%,#d75a55 58%,#f6b26b 100%)',
    swatchHill: '#a8622f',
  },
  misty: {
    key: 'misty', name: 'Lembah Pinus & Pelangi', short: 'Pagi berkabut',
    desc: 'Pagi sejuk, hutan pinus kebiruan, pelangi, goa kristal biru.',
    skyTop: '#6ba7c9', skyMid: '#b9dce8', skyBot: '#eef7f4',
    fog: '#cfe7e2', fogDensity: 0.0034,
    grass: '#4c9a80', grass2: '#3c8570', cliff: '#4c5f70', cliff2: '#657a8c',
    rock: '#74838d', caveRock: '#4f5e69', portal: '#07141a', glow: '#7dd3fc',
    crystal: '#7dd3fc', tree: '#1f5e58', tree2: '#286b63', trunk: '#4c3a2c',
    light: '#eafaff', hemiSky: '#d8f1ff', hemiGround: '#1f3e3c', amb: 0.78, sun: 1.0,
    stars: 0, moon: false, aurora: false, clouds: 1, fireflies: false, rainbow: true, emissive: 0.08,
    swatch: 'linear-gradient(180deg,#6ba7c9 0%,#b9dce8 60%,#eef7f4 100%)',
    swatchHill: '#357d6c',
  },
};

function biomeCss(b) {
  return `<span class="biome-sky" style="background:${b.swatch}">
      <span class="orb" style="background:${b.moon ? '#fef3c7' : '#fff7d6'};${b.moon ? 'box-shadow:0 0 10px 3px rgba(254,243,199,.55);' : ''}"></span>
      <span class="hill" style="background:${b.swatchHill}"></span>
    </span>`;
}

/* ---------- Audio ringan (WebAudio) ---------- */
const AudioFX = (() => {
  let ctx = null;
  let master = null;
  function ensure() {
    if (!state.sound) return null;
    if (!ctx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return null;
      ctx = new AC();
      master = ctx.createGain();
      master.gain.value = 0.20;
      master.connect(ctx.destination);
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }
  function tone(freq, dur, type, delay, gain, glide) {
    const c = ensure();
    if (!c) return;
    const t0 = c.currentTime + (delay || 0);
    const o = c.createOscillator();
    const g = c.createGain();
    o.type = type || 'sine';
    o.frequency.setValueAtTime(freq, t0);
    if (glide) o.frequency.exponentialRampToValueAtTime(Math.max(40, glide), t0 + dur);
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(gain == null ? 0.5 : gain, t0 + 0.015);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    o.connect(g); g.connect(master);
    o.start(t0); o.stop(t0 + dur + 0.03);
  }
  function noise(dur, gain) {
    const c = ensure();
    if (!c) return;
    const n = c.sampleRate * dur;
    const buf = c.createBuffer(1, n, c.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 2.4);
    const src = c.createBufferSource();
    src.buffer = buf;
    const g = c.createGain();
    g.gain.value = gain == null ? 0.16 : gain;
    const f = c.createBiquadFilter();
    f.type = 'lowpass'; f.frequency.value = 1200;
    src.connect(f); f.connect(g); g.connect(master);
    src.start();
  }
  return {
    unlock() { ensure(); },
    click() { tone(520, 0.07, 'triangle', 0, 0.18, 460); },
    select() { tone(660, 0.08, 'sine', 0, 0.22, 720); },
    correct() {
      tone(660, 0.14, 'sine', 0, 0.28); tone(880, 0.18, 'sine', 0.09, 0.26);
      tone(1320, 0.25, 'sine', 0.19, 0.16);
    },
    wrong() { tone(200, 0.22, 'sawtooth', 0, 0.13, 120); noise(0.22, 0.05); },
    star() { [523, 659, 784, 1046].forEach((f, i) => tone(f, 0.3, 'triangle', i * 0.09, 0.2)); },
    pass() { [392, 523, 659, 784, 1046].forEach((f, i) => tone(f, 0.4, 'sine', i * 0.11, 0.18)); },
    fail() { [330, 294, 247].forEach((f, i) => tone(f, 0.32, 'triangle', i * 0.14, 0.16)); },
    hop() { tone(500, 0.12, 'sine', 0, 0.16, 760); },
    whoosh() { noise(0.4, 0.12); },
    finale() {
      [523, 659, 784, 1046, 1318, 1568].forEach((f, i) => tone(f, 0.6, 'sine', i * 0.14, 0.16));
    },
  };
})();
