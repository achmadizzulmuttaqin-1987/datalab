/* ============================================================
   DUAL PERSONA — logika permainan
   ============================================================ */

(() => {
  'use strict';

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- elemen ---------------- */
  const el = {
    html: document.documentElement,
    figure: $('#figureWrap'),
    img: $('#figureImg'),
    bubble: $('#bubble'),
    bubbleName: $('#bubbleName'),
    bubbleText: $('#bubbleText'),
    reaction: $('#reactionCard'),
    reactionImg: $('#reactionImg'),
    reactionLabel: $('#reactionLabel'),
    rings: $('#touchRings'),
    combo: $('#comboLayer'),
    chatTray: $('#chatTray'),
    affinity: $('#affinityValue'),
    interactions: $('#interactionCount'),
    mood: $('#moodChip'),
    hint: $('#hint'),
    picks: { ren: $('#pickRen'), amira: $('#pickAmira') },
    hearts: {
      ren: $('[data-hearts="ren"]'),
      amira: $('[data-hearts="amira"]'),
    },
    states: {
      ren: $('[data-state="ren"]'),
      amira: $('[data-state="amira"]'),
    },
    flash: $('#flash'),
    modal: $('#sheetModal'),
    dock: $('.dock'),
  };

  /* ---------------- state ---------------- */
  const STORE_KEY = 'dual-persona-v1';
  const state = {
    active: 'ren',
    sound: true,
    voice: true,
    aff: { ren: 0, amira: 0 },
    taps: { ren: 0, amira: 0 },
    pose: { ren: 0, amira: 0 },
    last: {},          // baris terakhir per karakter+aksi
    combo: 0,
    comboAt: 0,
    busy: false,
    started: false,
    celebrated: { ren: false, amira: false },
  };

  const POSE_ORDER = ['front', 'side', 'back'];

  /* ---------------- persist ---------------- */
  function load() {
    try {
      const raw = localStorage.getItem(STORE_KEY);
      if (!raw) return;
      const saved = JSON.parse(raw);
      state.aff = { ...state.aff, ...(saved.aff || {}) };
      state.taps = { ...state.taps, ...(saved.taps || {}) };
      if (saved.active && CHARACTERS[saved.active]) state.active = saved.active;
      if (typeof saved.sound === 'boolean') state.sound = saved.sound;
      if (typeof saved.voice === 'boolean') state.voice = saved.voice;
    } catch (e) { /* penyimpanan tidak tersedia */ }
  }

  function save() {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify({
        aff: state.aff, taps: state.taps, active: state.active,
        sound: state.sound, voice: state.voice,
      }));
    } catch (e) { /* abaikan */ }
  }

  const char = () => CHARACTERS[state.active];

  /* ============================================================
     PARTIKEL
     ============================================================ */
  const FX = (() => {
    const canvas = $('#fx');
    const ctx = canvas.getContext && canvas.getContext('2d');
    if (!ctx) return { spawn() {}, resize() {} };
    let dpr = Math.min(window.devicePixelRatio || 1, 2);
    let parts = [];
    let raf = 0;
    let last = 0;

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.floor(window.innerWidth * dpr);
      canvas.height = Math.floor(window.innerHeight * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    const shapes = {
      spark(x, y, s, rot, color, alpha) {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rot);
        ctx.globalAlpha = alpha;
        ctx.fillStyle = color;
        ctx.beginPath();
        for (let i = 0; i < 4; i++) {
          const a = (Math.PI / 2) * i;
          ctx.lineTo(Math.cos(a) * s, Math.sin(a) * s);
          ctx.lineTo(Math.cos(a + Math.PI / 4) * s * 0.32, Math.sin(a + Math.PI / 4) * s * 0.32);
        }
        ctx.closePath();
        ctx.fill();
        ctx.restore();
      },
      dot(x, y, s, rot, color, alpha) {
        ctx.globalAlpha = alpha;
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x, y, s, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
      },
      heart(x, y, s, rot, color, alpha) {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rot);
        ctx.scale(s / 16, s / 16);
        ctx.globalAlpha = alpha;
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(0, 5);
        ctx.bezierCurveTo(-9, -3, -6, -13, 0, -7);
        ctx.bezierCurveTo(6, -13, 9, -3, 0, 5);
        ctx.fill();
        ctx.restore();
        ctx.globalAlpha = 1;
      },
      note(x, y, s, rot, color, alpha) {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rot);
        ctx.scale(s / 14, s / 14);
        ctx.globalAlpha = alpha;
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.ellipse(-3, 8, 4.6, 3.4, -0.4, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillRect(0.6, -9, 2, 17);
        ctx.beginPath();
        ctx.moveTo(2.6, -9);
        ctx.quadraticCurveTo(10, -6, 9, 1);
        ctx.quadraticCurveTo(9, -3, 2.6, -3);
        ctx.fill();
        ctx.restore();
        ctx.globalAlpha = 1;
      },
      confetti(x, y, s, rot, color, alpha) {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rot);
        ctx.globalAlpha = alpha;
        ctx.fillStyle = color;
        ctx.fillRect(-s / 2, -s / 4, s, s / 2);
        ctx.restore();
        ctx.globalAlpha = 1;
      },
    };

    function spawn(list) {
      if (reducedMotion) list = list.slice(0, Math.min(6, list.length));
      parts.push(...list);
      if (!raf) {
        last = performance.now();
        raf = requestAnimationFrame(frame);
      }
    }

    function frame(now) {
      const dt = Math.min((now - last) / 16.67, 3);
      last = now;
      ctx.clearRect(0, 0, canvas.width / dpr, canvas.height / dpr);

      parts = parts.filter((p) => p.life > 0);
      for (const p of parts) {
        p.life -= dt;
        p.vy += p.g * dt;
        p.vx *= 0.995;
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        p.rot += p.vr * dt;
        const alpha = clamp(p.life / p.fade, 0, 1);
        (shapes[p.shape] || shapes.dot)(p.x, p.y, p.size, p.rot, p.color, alpha * p.opacity);
      }

      if (parts.length) {
        raf = requestAnimationFrame(frame);
      } else {
        raf = 0;
        ctx.clearRect(0, 0, canvas.width / dpr, canvas.height / dpr);
      }
    }

    return { spawn, resize };
  })();

  function bodyAnchor() {
    const rect = el.figure.getBoundingClientRect();
    return {
      x: rect.left + rect.width / 2,
      y: rect.top + rect.height * 0.42,
      w: rect.width,
      h: rect.height,
    };
  }

  function burst(anchor, { count = 20, colors, shapes: kinds = ['spark', 'dot'], speed = 4.5, up = 2 } = {}) {
    const palette = colors || [char().accent, char().accentSoft, '#ffffff'];
    const list = [];
    for (let i = 0; i < count; i++) {
      const a = Math.random() * Math.PI * 2;
      const sp = speed * (0.35 + Math.random() * 0.9);
      list.push({
        x: anchor.x + (Math.random() - 0.5) * anchor.w * 0.7,
        y: anchor.y + (Math.random() - 0.5) * anchor.h * 0.5,
        vx: Math.cos(a) * sp,
        vy: Math.sin(a) * sp - up,
        g: 0.055,
        life: 34 + Math.random() * 30,
        fade: 46,
        size: 2 + Math.random() * 6,
        color: pick(palette),
        shape: pick(kinds),
        rot: Math.random() * Math.PI,
        vr: (Math.random() - 0.5) * 0.28,
        opacity: 0.65 + Math.random() * 0.35,
      });
    }
    FX.spawn(list);
  }

  function noteBurst(anchor, count = 7) {
    const palette = [char().accent, char().accentSoft, '#ffffff'];
    const list = [];
    for (let i = 0; i < count; i++) {
      list.push({
        x: anchor.x + (Math.random() - 0.5) * anchor.w * 0.5,
        y: anchor.y + anchor.h * 0.1,
        vx: (Math.random() - 0.5) * 1.1,
        vy: -1.5 - Math.random() * 1.4,
        g: -0.004,
        life: 60 + Math.random() * 25,
        fade: 70,
        size: 11 + Math.random() * 9,
        color: pick(palette),
        shape: 'note',
        rot: (Math.random() - 0.5) * 0.4,
        vr: (Math.random() - 0.5) * 0.04,
        opacity: 0.85,
      });
    }
    FX.spawn(list);
  }

  function heartsBurst(anchor, count = 8) {
    const list = [];
    for (let i = 0; i < count; i++) {
      list.push({
        x: anchor.x + (Math.random() - 0.5) * anchor.w * 0.8,
        y: anchor.y + (Math.random() - 0.2) * anchor.h * 0.4,
        vx: (Math.random() - 0.5) * 1.4,
        vy: -1.6 - Math.random() * 1.5,
        g: -0.002,
        life: 55 + Math.random() * 25,
        fade: 66,
        size: 10 + Math.random() * 10,
        color: pick([char().accent, '#ffd9e2', '#ffffff']),
        shape: 'heart',
        rot: (Math.random() - 0.5) * 0.5,
        vr: (Math.random() - 0.5) * 0.05,
        opacity: 0.9,
      });
    }
    FX.spawn(list);
  }

  function confetti() {
    const palette = ['#a9c3e2', '#e3bd8b', '#ffffff', '#8fb6ff', '#ffd9a0'];
    const list = [];
    for (let i = 0; i < 90; i++) {
      list.push({
        x: Math.random() * window.innerWidth,
        y: -20 - Math.random() * 200,
        vx: (Math.random() - 0.5) * 2,
        vy: 1.6 + Math.random() * 2.6,
        g: 0.02,
        life: 150 + Math.random() * 90,
        fade: 200,
        size: 5 + Math.random() * 7,
        color: pick(palette),
        shape: 'confetti',
        rot: Math.random() * Math.PI,
        vr: (Math.random() - 0.5) * 0.3,
        opacity: 0.95,
      });
    }
    FX.spawn(list);
  }

  /* ============================================================
     TAMPILAN
     ============================================================ */
  function renderCharacter({ entering = false } = {}) {
    const c = char();
    const other = state.active === 'ren' ? 'amira' : 'ren';

    el.html.dataset.char = state.active;
    document.title = `DUAL PERSONA — ${c.name}`;
    el.img.src = c.figures[POSE_ORDER[state.pose[state.active]]];
    el.img.alt = `${c.name}, karakter versi ${c.version.toLowerCase()}`;

    // kartu pemilih
    for (const id of ORDER) {
      const card = el.picks[id];
      const on = id === state.active;
      card.classList.toggle('is-active', on);
      card.setAttribute('aria-pressed', String(on));
      el.states[id].textContent = on ? 'AKTIF' : 'PILIH';
    }

    renderAffinity();
    el.reaction.classList.remove('is-on');
    el.mood.textContent = 'netral';
    el.chatTray.dataset.open = 'false';

    if (entering) {
      el.figure.classList.remove('is-entering');
      void el.figure.offsetWidth;
      el.figure.classList.add('is-entering');
      clearTimeout(renderCharacter._t);
      renderCharacter._t = setTimeout(() => el.figure.classList.remove('is-entering'), 900);
      if (!reducedMotion) burst(bodyAnchor(), { count: 26, speed: 5.5 });
    }
    save();
  }

  function renderAffinity() {
    for (const id of ORDER) {
      const value = state.aff[id];
      const full = Math.round(value / 20);
      el.hearts[id].innerHTML = Array.from({ length: 5 }, (_, i) =>
        `<i class="${i < full ? 'is-on' : ''}"></i>`).join('');
    }
    el.affinity.textContent = `${Math.round(state.aff[state.active])}%`;
    const total = state.taps.ren + state.taps.amira;
    el.interactions.textContent = `${total} interaksi`;
  }

  let typeTimer = 0;
  function say(text, { face = null, mood = null, speak = true, showCard = true } = {}) {
    const c = char();
    el.bubbleName.textContent = c.name;
    el.bubble.dataset.show = 'true';

    const target = text;
    clearInterval(typeTimer);
    if (reducedMotion) {
      el.bubbleText.textContent = target;
    } else {
      let i = 0;
      el.bubbleText.textContent = '';
      typeTimer = setInterval(() => {
        i += 1;
        el.bubbleText.textContent = target.slice(0, i);
        if (i >= target.length) clearInterval(typeTimer);
      }, 16);
    }

    if (showCard && mood) showReaction(mood, face);
    el.mood.textContent = mood || 'netral';
    if (speak) Sound.speak(text, c);
  }

  function showReaction(mood, faceSrc) {
    const c = char();
    const src = faceSrc || c.faces[mood] || c.faces.netral;
    el.reactionImg.src = src;
    el.reactionLabel.textContent = mood;
    el.reaction.classList.remove('is-on');
    void el.reaction.offsetWidth;
    el.reaction.classList.add('is-on');
    clearTimeout(showReaction._t);
    showReaction._t = setTimeout(() => el.reaction.classList.remove('is-on'), 3200);
  }

  function floatCombo(text, { big = false, at = null } = {}) {
    const b = document.createElement('b');
    b.textContent = text;
    if (big) b.classList.add('is-big');
    const a = at || bodyAnchor();
    b.style.left = `${a.x}px`;
    b.style.top = `${a.y + a.h * 0.18}px`;
    b.style.position = 'fixed';
    el.combo.appendChild(b);
    setTimeout(() => b.remove(), 1200);
  }

  function animate(kind) {
    if (reducedMotion) return;
    const cls = `anim-${kind}`;
    el.img.classList.remove('anim-hop', 'anim-sway', 'anim-tilt', 'anim-shake',
      'anim-squash', 'anim-spin', 'anim-step');
    void el.img.offsetWidth;
    el.img.classList.add(cls);
    clearTimeout(animate._t);
    animate._t = setTimeout(() => el.img.classList.remove(cls), 1400);
  }

  function touchRings(clientX, clientY) {
    const rect = el.figure.getBoundingClientRect();
    const s = document.createElement('span');
    s.style.left = `${clientX - rect.left}px`;
    s.style.top = `${clientY - rect.top}px`;
    el.rings.appendChild(s);
    setTimeout(() => s.remove(), 800);
  }

  function flashScreen() {
    el.flash.classList.remove('is-on');
    void el.flash.offsetWidth;
    el.flash.classList.add('is-on');
  }

  /* ---------------- baris dialog ---------------- */
  function nextLine(kind) {
    const c = char();
    const pool = c.lines[kind] || c.lines.sentuh;
    const key = `${state.active}:${kind}`;
    let idx = Math.floor(Math.random() * pool.length);
    if (pool.length > 1 && idx === state.last[key]) idx = (idx + 1) % pool.length;
    state.last[key] = idx;
    return pool[idx];
  }

  /* ---------------- kedekatan ---------------- */
  function gain(amount, anchor) {
    const id = state.active;
    const before = state.aff[id];
    state.aff[id] = clamp(before + amount, 0, 100);
    const got = state.aff[id] - before;
    if (got > 0) {
      renderAffinity();
      const a = anchor || bodyAnchor();
      floatCombo(`+${Math.round(got)}`, { at: a });
      if (Math.round(state.aff[id] / 20) > Math.round(before / 20)) Sound.chime(id, 2);
    }
    if (state.aff[id] >= 100 && !state.celebrated[id]) {
      state.celebrated[id] = true;
      setTimeout(() => {
        say(pick(char().lines.penuh), { mood: 'senang' });
        heartsBurst(bodyAnchor(), 20);
        confetti();
        Sound.fanfare(id);
      }, 900);
    }
    save();
  }

  function bumpCombo(anchor) {
    const now = performance.now();
    state.combo = now - state.comboAt < 1700 ? state.combo + 1 : 1;
    state.comboAt = now;
    if (state.combo >= 3) {
      const a = anchor || bodyAnchor();
      floatCombo(`${state.combo}× COMBO`, { big: true, at: { ...a, y: a.y + a.h * 0.1 } });
    }
    return state.combo;
  }

  /* ============================================================
     AKSI
     ============================================================ */
  const ACTIONS = {
    sapa(anchor) {
      animate(pick(['sway', 'tilt']));
      gain(4, anchor);
      say(nextLine('sapa'), { mood: 'senang' });
      burst(anchor, { count: 16, shapes: ['spark', 'dot'] });
      Sound.tap(state.active);
      Sound.chime(state.active, 1);
    },

    canda(anchor) {
      animate('hop');
      gain(6, anchor);
      setTimeout(() => say(nextLine('canda'), { mood: 'senang' }), 220);
      burst(anchor, { count: 24, shapes: ['spark', 'heart'], speed: 5.2 });
      Sound.tap(state.active);
      Sound.chime(state.active, 2);
    },

    pose(anchor) {
      state.pose[state.active] = (state.pose[state.active] + 1) % POSE_ORDER.length;
      const shown = POSE_ORDER[state.pose[state.active]];
      flashScreen();
      Sound.flash();
      animate('spin');
      el.img.src = char().figures[shown];
      gain(5, anchor);
      const line = shown === 'back'
        ? (state.active === 'ren'
          ? 'Belakang juga boleh. Jaket ini adil di semua sudut.'
          : 'Dari belakang pun tetap rapi, kak! Lihat syalnya, hihi.')
        : nextLine('pose');
      say(line, { mood: 'senang' });
      burst(anchor, { count: 20, shapes: ['spark'], speed: 6 });
    },

    musik(anchor) {
      animate('sway');
      gain(5, anchor);
      say(nextLine('musik'), { mood: 'senang' });
      Sound.tap(state.active);
      Sound.hum(state.active, (i) => {
        const a = bodyAnchor();
        noteBurst(a, 2);
      });
    },

    sentuh(anchor, point) {
      const roll = Math.random();
      const kind = roll < 0.34 ? 'hop' : roll < 0.62 ? 'shake' : roll < 0.84 ? 'squash' : 'tilt';
      const moods = state.active === 'amira'
        ? ['kaget', 'senang', 'senang', 'jengkel']
        : ['kaget', 'serius', 'senang', 'jengkel'];
      const mood = pick(moods);
      animate(kind);
      gain(3, anchor);
      say(nextLine('sentuh'), { mood });
      burst(anchor, { count: 14, shapes: ['spark', 'heart'], speed: 3.8 });
      Sound.tap(state.active);
      Sound.heart();
      if (point) touchRings(point.x, point.y);
    },

    obrolan(anchor) {
      if (el.chatTray.dataset.open === 'true') {
        closeChat();
        return;
      }
      animate('tilt');
      Sound.tap(state.active);
      gain(2, anchor);
      openChat();
      say(nextLine('sapa'), { mood: 'serius' });
    },
  };

  function runAction(action, event) {
    const anchor = bodyAnchor();
    let point = null;
    if (event && typeof event.clientX === 'number' && event.clientX > 0) {
      point = { x: event.clientX, y: event.clientY };
    }
    state.taps[state.active] += 1;
    bumpCombo(anchor);
    if (!state.started) {
      state.started = true;
      el.hint.classList.add('is-dim');
    }
    el.figure.classList.add('is-hot');
    clearTimeout(runAction._hot);
    runAction._hot = setTimeout(() => el.figure.classList.remove('is-hot'), 900);

    const fn = ACTIONS[action] || ACTIONS.sentuh;
    fn(anchor, point);
    renderAffinity();
    resetIdle();
  }

  function openChat() {
    const c = char();
    const topic = pick(c.chat);
    el.chatTray.innerHTML = '';
    const q = document.createElement('p');
    q.className = 'chat-tray__q';
    q.id = 'chatQuestion';
    q.textContent = `“${topic.q}”`;
    el.chatTray.appendChild(q);

    topic.replies.forEach((reply) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'chat-reply';
      btn.textContent = reply.text;
      btn.addEventListener('click', (ev) => {
        ev.stopPropagation();
        closeChat();
        animate(reply.mood === 'serius' ? 'tilt' : 'hop');
        gain(reply.aff, bodyAnchor());
        say(reply.reply, { mood: reply.mood });
        burst(bodyAnchor(), {
          count: 18,
          shapes: reply.mood === 'senang' ? ['heart', 'spark'] : ['dot', 'spark'],
        });
        Sound.tap(state.active);
        if (reply.mood === 'senang') Sound.heart();
      });
      el.chatTray.appendChild(btn);
    });
    el.chatTray.dataset.open = 'true';
  }

  function closeChat() {
    el.chatTray.dataset.open = 'false';
  }

  /* ============================================================
     GANTI KARAKTER
     ============================================================ */
  function switchTo(id, { silent = false } = {}) {
    if (!CHARACTERS[id] || id === state.active) {
      if (id === state.active) {
        animate('squash');
        Sound.deny();
        floatCombo(`${CHARACTERS[id].name} sudah aktif`, { at: bodyAnchor() });
      }
      return;
    }
    if (state.busy) return;
    state.busy = true;
    Sound.whoosh();
    Sound.stopSpeech();
    closeChat();

    el.figure.classList.add('is-hidden');
    const anchor = bodyAnchor();
    burst(anchor, { count: 30, speed: 6.5, shapes: ['spark', 'dot'] });

    setTimeout(() => {
      state.active = id;
      state.pose[id] = 0;
      renderCharacter({ entering: true });
      el.figure.classList.remove('is-hidden');
      el.picks[id].classList.remove('is-picked');
      void el.picks[id].offsetWidth;
      el.picks[id].classList.add('is-picked');

      const c = char();
      el.bubble.dataset.show = 'false';
      setTimeout(() => {
        say(pick(c.lines.switchIn), { mood: 'senang', speak: !silent });
        Sound.chime(id, 1);
      }, 260);
      state.busy = false;
    }, 220);
  }

  /* ============================================================
     IKATAN
     ============================================================ */
  function bind() {
    // pemilih karakter
    for (const id of ORDER) {
      el.picks[id].addEventListener('click', () => switchTo(id));
    }

    // sentuh / geser karakter
    let ptr = null;
    el.figure.addEventListener('pointerdown', (e) => {
      if (e.button !== undefined && e.button > 0) return;
      ptr = { x: e.clientX, y: e.clientY, t: performance.now() };
    });
    el.figure.addEventListener('pointercancel', () => { ptr = null; });
    el.figure.addEventListener('pointerup', (e) => {
      if (!ptr) return;
      const dx = e.clientX - ptr.x;
      const dy = e.clientY - ptr.y;
      const dt = performance.now() - ptr.t;
      ptr = null;
      // geser mendatar = berganti karakter, selain itu = sentuhan biasa
      if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.3 && dt < 700) {
        switchTo(state.active === 'ren' ? 'amira' : 'ren');
        return;
      }
      if (el.chatTray.dataset.open === 'true') closeChat();
      Sound.unlock();
      runAction('sentuh', e);
    });

    // tombol aksi
    el.dock.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      Sound.unlock();
      runAction(btn.dataset.action, { clientX: 0, clientY: 0 });
    });

    // kontrol atas
    const btnSound = $('#btnSound');
    const btnVoice = $('#btnVoice');
    btnSound.addEventListener('click', () => {
      state.sound = !state.sound;
      Sound.enabled = state.sound;
      btnSound.setAttribute('aria-pressed', String(state.sound));
      if (state.sound) Sound.unlock();
      save();
    });
    btnVoice.addEventListener('click', () => {
      state.voice = !state.voice;
      Sound.voiceEnabled = state.voice;
      btnVoice.setAttribute('aria-pressed', String(state.voice));
      if (!state.voice) Sound.stopSpeech();
      save();
    });

    // modal lembar karakter
    const openSheet = () => { el.modal.dataset.open = 'true'; };
    const closeSheet = () => { el.modal.dataset.open = 'false'; };
    $('#btnSheet').addEventListener('click', openSheet);
    $$('[data-close]').forEach((n) => n.addEventListener('click', closeSheet));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeSheet();
    });

    // ganti karakter
    $('#btnSwitch').addEventListener('click', () => {
      switchTo(state.active === 'ren' ? 'amira' : 'ren');
    });

    // keyboard
    const KEYS = ['sapa', 'canda', 'pose', 'musik', 'obrolan', 'sentuh'];
    document.addEventListener('keydown', (e) => {
      if (e.target && e.target.matches && e.target.matches('input, textarea')) return;
      if (e.key === 'Tab') {
        e.preventDefault();
        switchTo(state.active === 'ren' ? 'amira' : 'ren');
        return;
      }
      if (e.key === '1' || e.key === '2') {
        switchTo(e.key === '1' ? 'ren' : 'amira');
        return;
      }
      const n = parseInt(e.key, 10);
      if (n >= 3 && n <= 8) {
        runAction(KEYS[n - 3], { clientX: 0, clientY: 0 });
      }
    });

    // klik di luar tray menutup obrolan
    document.addEventListener('click', (e) => {
      if (el.chatTray.dataset.open !== 'true') return;
      if (e.target.closest('#chatTray') || e.target.closest('[data-action="obrolan"]')) return;
      closeChat();
    });

    // suara latar dari interaksi pertama (kebijakan autoplay peramban)
    window.addEventListener('pointerdown', function unlockOnce() {
      Sound.unlock();
      window.removeEventListener('pointerdown', unlockOnce);
    }, { once: true });
  }

  /* ============================================================
     IDLE CHATTER
     ============================================================ */
  let idleTimer = 0;
  function resetIdle() {
    clearTimeout(idleTimer);
    idleTimer = setTimeout(() => {
      if (el.chatTray.dataset.open === 'true') { resetIdle(); return; }
      const c = char();
      say(pick(c.lines.idle), { mood: Math.random() < 0.4 ? 'senang' : 'netral' });
      animate('tilt');
      resetIdle();
    }, 23000);
  }

  /* ============================================================
     MULAI
     ============================================================ */
  function boot() {
    load();
    Sound.enabled = state.sound;
    Sound.voiceEnabled = state.voice;
    $('#btnSound').setAttribute('aria-pressed', String(state.sound));
    $('#btnVoice').setAttribute('aria-pressed', String(state.voice));

    renderCharacter({ entering: true });
    bind();

    // sapaan pembuka (tanpa suara sampai pengguna menyentuh)
    setTimeout(() => {
      const c = char();
      say(`Halo. Aku ${c.name}. Sentuh aku, atau pilih aksi di bawah.`,
        { mood: 'senang', speak: false });
    }, 700);

    resetIdle();
    window.addEventListener('resize', () => FX.resize(), { passive: true });
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) Sound.stopSpeech();
      else resetIdle();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
