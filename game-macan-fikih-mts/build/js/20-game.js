/* =====================================================================
   20 · Alur permainan: kuis, bintang, perpindahan, akhir cerita
   ===================================================================== */
const UI = {
  introOpen: true,
  stack: [],
  lastReview: null,
  lastResult: null,
  returnAfterFinale: null,
};
let session = null;
let quizLocked = false;
let bannerTimer = 0;
let toastTimer = 0;

/* ---------- Util UI ---------- */
function showToast(msg, ms) {
  const el = $('#toast');
  if (!el) return;
  el.innerHTML = msg;
  el.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('show'), ms || 2600);
}
function showBanner(kicker, title, sub, ms) {
  $('#banner-k').textContent = kicker;
  $('#banner-t').textContent = title;
  $('#banner-s').textContent = sub || '';
  const el = $('#banner');
  el.classList.add('show');
  clearTimeout(bannerTimer);
  bannerTimer = setTimeout(() => el.classList.remove('show'), ms || 3400);
}
function showScreen(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.remove('hidden');
  if (!UI.stack.includes(id)) UI.stack.push(id);
  document.body.classList.add('modal-open');
}
function hideScreen(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.add('hidden');
  UI.stack = UI.stack.filter(x => x !== id);
  if (!UI.stack.length) document.body.classList.remove('modal-open');
}
function topScreen() { return UI.stack[UI.stack.length - 1] || null; }
function closeAllScreens(except) {
  UI.stack.slice().forEach(id => { if (id !== except) hideScreen(id); });
}
function openIntro() {
  if (topScreen()) return;
  UI.introOpen = true;
  document.body.classList.add('intro-open');
  $('#intro').classList.remove('hidden');
  CAM.mode = 'intro';
  refreshIntro();
}
function closeIntro() {
  UI.introOpen = false;
  document.body.classList.remove('intro-open');
  $('#intro').classList.add('hidden');
}

/* ---------- HUD & kartu goa ---------- */
function syncHud() {
  const c = caveInfo(state.cave);
  $('#hud-bab').textContent = gradeLabel(c.bab.g) + ' · Bab ' + c.bab.o;
  $('#hud-cave').textContent = c.no;
  $('#hud-stars').textContent = totalStars();
  const snd = $('#btn-sound');
  snd.classList.toggle('on', state.sound);
  const icon = $('#sound-icon');
  if (icon) icon.setAttribute('href', state.sound ? '#i-sound' : '#i-mute');
  const card = $('#cave-card');
  card.classList.toggle('traveling', !!travelAnim);
}
function updateCaveCard() {
  const c = caveInfo(state.cave);
  const stars = state.stars[state.cave] || 0;
  const passed = isPassed(state.cave);
  $('#card-cave').textContent = c.no;
  $('#card-grade').textContent = gradeLabel(c.bab.g);
  $('#card-sem').textContent = c.bab.s;
  $('#card-bab-no').textContent = c.bab.o;
  $('#card-title').textContent = c.bab.t;
  $('#card-cave-pos').textContent = 'Goa ' + (c.k + 1) + ' dari 5 di bab ini';
  $('#card-stars').innerHTML = starRow(stars, 3);
  $('#card-stars').setAttribute('aria-label', stars + ' dari 3 bintang');
  $('#card-passed').innerHTML = passed
    ? '<span style="color:#fbbf24;font-weight:800;font-size:11.5px">✓ Sudah dilewati</span>'
    : (state.cave < state.frontier
      ? '<span style="color:#9fd8ca;font-size:11.5px">Tinjau ulang · terdepan goa ' + (state.frontier + 1) + '</span>'
      : '');
  const btn = $('#btn-enter');
  const label = btn.querySelector('span');
  if (travelAnim) {
    label.textContent = 'Cilik sedang mendaki…';
    btn.disabled = true;
  } else {
    btn.disabled = false;
    if (session && session.cave === state.cave && !session.done) label.textContent = 'Lanjutkan Goa';
    else if (passed) label.textContent = 'Ulangi Goa';
    else label.textContent = 'Masuk Goa';
  }
  const icon = btn.querySelector('use');
  if (icon) icon.setAttribute('href', passed ? '#i-refresh' : '#i-play');
  syncHud();
}
function setTraveling(v) {
  $('#cave-card').classList.toggle('traveling', v);
  $('#btn-enter').disabled = v;
  if (v) {
    const l = $('#btn-enter').querySelector('span');
    if (l) l.textContent = 'Cilik sedang mendaki…';
  }
}

/* ---------- Layar pembuka ---------- */
function refreshIntro() {
  const any = hasAnyProgress();
  $('#btn-resume').classList.toggle('hidden', !any);
  $('#btn-start').classList.toggle('hidden', any);
  const save = $('#intro-save');
  save.classList.toggle('hidden', !any);
  if (any) {
    const pct = Math.round(totalStars() / (N_CAVES * 3) * 100);
    $('#intro-bar').style.width = pct + '%';
    const c = caveInfo(state.cave);
    $('#intro-save-text').innerHTML = 'Tersimpan: <b>Goa ' + c.no + '</b> · ' + totalStars() + '/450 bintang · ' +
      passedCount() + '/150 goa';
    $('#btn-resume').innerHTML = '<svg><use href="#i-mountain"/></svg> Lanjutkan dari Goa ' + c.no;
  }
  if (state.finished) {
    $('#btn-resume').innerHTML = '<svg><use href="#i-star"/></svg> Lihat Puncak (Selesai)';
  }
}

function beginAdventure() {
  AudioFX.unlock();
  closeIntro();
  const c = caveInfo(state.cave);
  CAM.mode = 'follow';
  CAM.yaw = 0.2;
  CAM.pitch = 0.17;
  CAM.dist = 7.7;
  CAM.zoom = 1;
  if (WORLD.ok) {
    WORLD.finaleMode = false;
    WORLD.tigerRoot.visible = true;
    TIGER_ANIM.mode = 'idle';
  }
  updateCaveCard();
  showBanner(
    state.finished ? 'Perjalanan selesai' : 'Cilik siap mendaki',
    'Goa ' + c.no + ' · ' + c.bab.t,
    gradeLabel(c.bab.g) + ' · Bab ' + c.bab.o + ' · ' + (c.k + 1) + '/5',
    3200
  );
  AudioFX.whoosh();
}

/* ---------- Perpindahan ---------- */
function canTravel(i) { return i >= 0 && i < N_CAVES && i <= state.frontier; }

function travelTo(target, opts) {
  opts = opts || {};
  if (travelAnim || !WORLD.ok) { if (!WORLD.ok) { state.cave = target; updateCaveCard(); } return; }
  if (target < 0 || target >= N_CAVES) return;
  if (target === state.cave) { closeAllScreens(); updateCaveCard(); return; }
  if (!canTravel(target) && !opts.force) { showToast('Goa itu masih terkunci.'); return; }
  closeAllScreens();
  const from = state.cave;
  const p1 = cavePose(from), p2 = cavePose(target);
  const adjacent = target === from + 1;
  if (opts.instant || !adjacent || !state.cinema) { fadeTeleport(target); return; }
  const climb = p1.b !== p2.b;
  TIGER_ANIM.mode = climb ? 'climb' : 'walk';
  travelAnim = {
    from, to: target, t: 0,
    t0: WORLD.clock.elapsedTime,
    dur: climb ? 2.4 : 1.7,
    climb, p1, p2,
    arrived: false,
  };
  setTraveling(true);
  AudioFX.whoosh();
}

function updateTravel(dt, time) {
  if (!travelAnim) return;
  const a = travelAnim;
  a.t += dt;
  // progres memakai waktu nyata (bukan akumulasi dt yang dibatasi)
  let k = clamp((time - a.t0) / a.dur, 0, 1);
  const e = easeInOut(k);
  const p1 = a.p1, p2 = a.p2;
  if (a.climb) {
    const rr = lerp(p1.r + 1.08, p2.r + 1.08, e);
    const th = lerp(p1.th, p2.th + Math.PI * 2 * (p2.th < p1.th ? 1 : 0), e);
    const hop = Math.abs(Math.sin(e * Math.PI * 2.2)) * 0.55;
    const y = lerp(p1.y, p2.y, e) + hop;
    WORLD.tigerRoot.position.set(Math.sin(th) * rr, y + 0.02, Math.cos(th) * rr);
    const dir = new THREE.Vector3(Math.sin(th) * (p2.r - p1.r), 0, Math.cos(th) * (p2.r - p1.r))
      .add(new THREE.Vector3(Math.cos(th), 0, -Math.sin(th)).multiplyScalar(1));
    WORLD.tigerRoot.rotation.y = Math.atan2(dir.x, dir.z);
    if (k > 0.5 && !a.hopped) { a.hopped = true; AudioFX.hop(); }
  } else {
    const th = lerp(p1.th, p2.th, e);
    const rr = p1.r + 1.08;
    WORLD.tigerRoot.position.set(Math.sin(th) * rr, p1.y + 0.02, Math.cos(th) * rr);
    WORLD.tigerRoot.rotation.y = Math.atan2(Math.cos(th), -Math.sin(th));
  }
  if (k >= 1 && !a.arrived) {
    a.arrived = true;
    travelAnim = null;
    state.cave = a.to;
    saveState();
    placeTigerAt(a.to, true);
    snapCamera();
    TIGER_ANIM.mode = 'idle';
    setTraveling(false);
    updateCaveCard();
    refreshCaveColors();
    AudioFX.hop();
    announceCave(a.to);
  }
}

function announceCave(i) {
  const c = caveInfo(i);
  if (c.k === 0) {
    const gradeChanged = i > 0 && caveInfo(i - 1).bab.g !== c.bab.g;
    showBanner(
      gradeChanged ? 'Naik ke ' + gradeLabel(c.bab.g) : 'Bab baru',
      'Bab ' + c.bab.o + ' · ' + c.bab.t,
      gradeLabel(c.bab.g) + ' · Semester ' + c.bab.s + ' · Goa ' + c.no + '–' + (c.no + 4),
      3800
    );
    if (gradeChanged) showToast('Cilik naik ke tingkat <b>' + gradeLabel(c.bab.g) + '</b>. Bab baru dimulai!', 3400);
  } else if (c.k === 4) {
    showBanner('Tanjakan berikutnya', 'Puncak tanjakan bab ' + c.bab.o + ' hampir tiba', 'Goa ' + c.no + ' · siapkan 2 bintang untuk memanjat', 2600);
  }
}

function fadeTeleport(target) {
  let fade = $('#fade');
  if (!fade) {
    fade = document.createElement('div');
    fade.id = 'fade';
    document.body.appendChild(fade);
  }
  fade.classList.add('on');
  AudioFX.whoosh();
  setTraveling(true);
  setTimeout(() => {
    travelAnim = null;
    state.cave = clamp(target, 0, N_CAVES - 1);
    state.frontier = Math.max(state.frontier, state.cave);
    saveState();
    placeTigerAt(state.cave, true);
    TIGER_ANIM.mode = 'idle';
    updateCaveCard();
    refreshCaveColors();
    CAM.yaw = 0.2; CAM.pitch = 0.17;
    snapCamera();
    updateMarker();
    fade.classList.remove('on');
    setTraveling(false);
    announceCave(state.cave);
  }, REDUCED ? 40 : 300);
}

/* ---------- Masuk goa & kuis ---------- */
function enterCave() {
  AudioFX.unlock();
  if (!WORLD.ok) { openQuiz(state.cave); return; }
  const passed = isPassed(state.cave);
  AudioFX.click();
  CAM.dist = 7.2;
  setTimeout(() => openQuiz(state.cave), 180);
}

function openQuiz(idx) {
  const c = caveInfo(idx);
  if (!session || session.cave !== idx || session.done) {
    session = {
      cave: idx,
      qi: 0,
      answers: new Array(10).fill(null),
      done: false,
      startedAt: Date.now(),
    };
  }
  showScreen('quiz');
  quizLocked = false;
  $('#q-badge').textContent = 'GOA ' + c.no;
  $('#q-title').innerHTML = esc(c.bab.t) + '<span id="q-sub">' +
    gradeLabel(c.bab.g) + ' · Bab ' + c.bab.o + ' · Semester ' + c.bab.s + '</span>';
  renderQuiz();
  document.body.classList.add('modal-open');
}

function renderQuiz() {
  const c = caveInfo(session.cave);
  const q = c.qs[session.qi];
  const answered = session.answers[session.qi] != null;
  const letters = ['A', 'B', 'C', 'D', 'E'];
  let html = '';
  html += '<div class="q-topic"><span class="sq">' + (session.qi + 1) + '</span> Fikih · ' + esc(c.bab.t) + '</div>';
  if (q.ar) {
    html += '<div class="arabic" dir="rtl" lang="ar">' + esc(q.ar) + '</div>';
  }
  if (q.st) {
    html += '<div class="stimulus"><span class="lbl">Stimulus</span>' + esc(q.st) + '</div>';
  }
  html += '<p class="q-text">' + esc(q.q) + '</p>';
  html += '<div class="options" id="opts">';
  q.o.forEach((opt, i) => {
    html += '<button class="option" data-k="' + i + '" type="button">' +
      '<span class="key">' + letters[i] + '</span><span class="txt">' + esc(opt) + '</span><span class="mark"></span></button>';
  });
  html += '</div>';
  if (answered) {
    const chosen = session.answers[session.qi];
    const ok = chosen === q.a;
    html += '<div class="feedback ' + (ok ? 'ok' : 'bad') + '">' +
      '<div class="fb-head"><span class="ic">' + (ok ? '✓' : '✕') + '</span>' + (ok ? 'Benar sekali!' : 'Belum tepat') + '</div>' +
      '<p>' + esc(q.e) + '</p></div>';
  }
  $('#q-body').innerHTML = html;
  $('#q-body').scrollTop = 0;

  $('#q-dots').innerHTML = session.answers.map((a, i) => {
    let cls = '';
    if (a != null) cls = a === c.qs[i].a ? 'done-ok' : 'done-bad';
    else if (i === session.qi) cls = 'current';
    return '<span class="dot ' + cls + '"></span>';
  }).join('');
  $('#q-count').textContent = 'Soal ' + (session.qi + 1) + ' / 10';

  const nextBtn = $('#q-next');
  const nextLabel = nextBtn.querySelector('span');
  if (answered) {
    nextBtn.disabled = false;
    nextLabel.textContent = session.qi === 9 ? 'Lihat Hasil' : 'Soal Berikutnya';
    $('#q-hint').innerHTML = 'Baca pembahasannya, lalu lanjut. Tekan <b>Enter</b>.';
    applyAnswerClasses();
  } else {
    nextBtn.disabled = true;
    nextLabel.textContent = 'Pilih jawaban';
    $('#q-hint').innerHTML = state.keys
      ? 'Pilih satu jawaban yang paling tepat. Gunakan tombol <b>1–4</b> di papan ketik.'
      : 'Pilih satu jawaban yang paling tepat.';
  }
  $$('#opts .option').forEach(btn => {
    btn.addEventListener('click', () => chooseAnswer(Number(btn.dataset.k)));
  });
  if (!answered) {
    // tidak auto-scroll; jawaban dipilih pengguna
  }
}

function chooseAnswer(k) {
  if (quizLocked) return;
  if (session.answers[session.qi] != null) return;
  const c = caveInfo(session.cave);
  const q = c.qs[session.qi];
  if (k < 0 || k >= q.o.length) return;
  quizLocked = true;
  session.answers[session.qi] = k;
  const ok = k === q.a;
  if (ok) AudioFX.correct(); else AudioFX.wrong();
  applyAnswerClasses();
  const qEl = $('#opts');
  if (qEl) {
    const chosen = qEl.querySelector('[data-k="' + k + '"]');
    if (chosen && !ok) {
      chosen.style.animation = 'shake .35s';
      setTimeout(() => { chosen.style.animation = ''; }, 400);
    }
  }
  const feedback = document.createElement('div');
  feedback.className = 'feedback ' + (ok ? 'ok' : 'bad');
  feedback.innerHTML = '<div class="fb-head"><span class="ic">' + (ok ? '✓' : '✕') + '</span>' +
    (ok ? 'Benar sekali!' : 'Belum tepat') + '</div><p>' + esc(q.e) + '</p>';
  $('#q-body').appendChild(feedback);
  const nextBtn = $('#q-next');
  nextBtn.disabled = false;
  nextBtn.querySelector('span').textContent = session.qi === 9 ? 'Lihat Hasil' : 'Soal Berikutnya';
  $('#q-hint').innerHTML = 'Baca pembahasannya, lalu lanjut. Tekan <b>Enter</b>.';
  $('#q-dots').innerHTML = session.answers.map((a, i) => {
    let cls = '';
    if (a != null) cls = a === c.qs[i].a ? 'done-ok' : 'done-bad';
    else if (i === session.qi) cls = 'current';
    return '<span class="dot ' + cls + '"></span>';
  }).join('');
  setTimeout(() => { quizLocked = false; }, 250);
}

function applyAnswerClasses() {
  const c = caveInfo(session.cave);
  const q = c.qs[session.qi];
  const chosen = session.answers[session.qi];
  $$('#opts .option').forEach(btn => {
    const k = Number(btn.dataset.k);
    btn.classList.add('dim');
    btn.disabled = true;
    if (k === q.a) {
      btn.classList.remove('dim'); btn.classList.add('correct');
      btn.querySelector('.mark').textContent = '✓';
    }
    if (chosen != null && k === chosen && k !== q.a) {
      btn.classList.remove('dim'); btn.classList.add('wrong');
      btn.querySelector('.mark').textContent = '✕';
    }
  });
}

function nextQuestion() {
  if (!session) return;
  if (session.answers[session.qi] == null) return;
  if (session.qi < 9) {
    session.qi++;
    AudioFX.select();
    renderQuiz();
    $('#q-body').scrollTop = 0;
  } else {
    finishQuiz();
  }
}

function closeQuiz() {
  hideScreen('quiz');
  const c = caveInfo(state.cave);
  $('#q-hint').innerHTML = 'Pilih satu jawaban yang paling tepat.';
  if (session && !session.done && session.answers.some(a => a != null)) {
    showToast('Progres goa disimpan sementara. Klik <b>Lanjutkan Goa</b> untuk melanjutkan.', 3000);
  } else {
    session = null;
  }
  updateCaveCard();
}

function finishQuiz() {
  const c = caveInfo(session.cave);
  const idx = session.cave;
  let correct = 0;
  session.answers.forEach((a, i) => { if (a === c.qs[i].a) correct++; });
  const stars = starsFor(correct);
  const prevStars = state.stars[idx] || 0;
  const prevBest = state.best[idx];
  state.best[idx] = Math.max(prevBest, correct);
  const newBest = correct > prevBest;
  state.stars[idx] = Math.max(prevStars, stars);
  state.visits[idx] = (state.visits[idx] || 0) + 1;
  const pass = stars >= 2;
  if (pass && idx === state.frontier && idx < N_CAVES - 1) {
    state.frontier = idx + 1;
  }
  if (pass && idx === N_CAVES - 1) {
    state.frontier = N_CAVES - 1;
    state.finished = true;
  }
  session.done = true;
  session.correct = correct;
  session.stars = stars;
  UI.lastReview = { cave: idx, answers: session.answers.slice(), correct, stars };
  UI.lastResult = { cave: idx, correct, stars, pass, prevStars, newBest };
  saveState();
  refreshCaveColors();
  syncHud();
  updateCaveCard();
  hideScreen('quiz');
  showResult(UI.lastResult);
  if (stars === 3) AudioFX.star();
  else if (pass) AudioFX.pass();
  else AudioFX.fail();
}

/* ---------- Kartu hasil ---------- */
function resultMessage(correct, stars, pass) {
  if (correct === 10) return 'Sempurna! Semua jawaban benar. Cilik melompat riang dan langit di atas bukit seakan ikut bersinar.';
  if (correct >= 8) return 'Hebat! Cilik berhasil mengumpulkan ' + stars + ' bintang. Jalan menuju tanjakan berikutnya terbuka.';
  if (correct === 7) return 'Hampir sempurna! Cilik mendapat 1 bintang. Butuh <b>minimal 2 bintang</b> untuk memanjat—pelajari pembahasannya, lalu coba lagi.';
  return 'Cilik belum mendapat bintang kali ini. Tidak apa-apa! Pelajari pembahasan tiap soal, lalu ulangi goa ini. Jawaban benar 10 soal akan memberi 3 bintang.';
}
function starRowHTML(n, cls) {
  let s = '';
  for (let i = 0; i < 3; i++) s += '<span class="star ' + (i < n ? 'on' : '') + ' ' + (cls || '') + '">' +
    '<svg viewBox="0 0 24 24"><use href="#i-star"/></svg></span>';
  return s;
}
function confettiHTML(n) {
  const colors = ['#fbbf24', '#f59e0b', '#2dd4bf', '#34d399', '#fb7185', '#fcd34d', '#a78bfa'];
  let h = '<div class="confetti">';
  for (let i = 0; i < n; i++) {
    const left = Math.random() * 100;
    const delay = Math.random() * 1.8;
    const dur = 2.4 + Math.random() * 2.2;
    const col = colors[i % colors.length];
    const w = 5 + Math.random() * 7;
    h += '<i style="left:' + left + '%;background:' + col + ';animation-delay:' + delay + 's;animation-duration:' + dur + 's;width:' + w + 'px"></i>';
  }
  return h + '</div>';
}

function showResult(r) {
  const c = caveInfo(r.cave);
  const stars = r.stars;
  const pass = r.pass;
  const finalCave = r.cave === N_CAVES - 1;
  const title = correctTitle(r.correct);
  let actions = '';
  if (pass) {
    if (finalCave) {
      actions += '<button class="btn btn-gold btn-lg btn-block" id="res-primary"><span>Temui Induk di Puncak</span></button>';
    } else {
      actions += '<button class="btn btn-primary btn-lg btn-block" id="res-primary"><span>Naik ke Goa ' + (r.cave + 2) + '</span><svg><use href="#i-arrow"/></svg></button>';
    }
    actions += '<div class="row"><button class="btn btn-soft" id="res-review"><svg><use href="#i-book"/></svg> Lihat Pembahasan</button>' +
      '<button class="btn btn-soft" id="res-close">Tutup</button></div>';
  } else {
    actions += '<button class="btn btn-primary btn-lg btn-block" id="res-primary"><svg><use href="#i-refresh"/></svg> Coba Lagi Goa Ini</button>';
    actions += '<div class="row"><button class="btn btn-soft" id="res-review"><svg><use href="#i-book"/></svg> Lihat Pembahasan</button>' +
      '<button class="btn btn-soft" id="res-close">Tutup</button></div>';
  }
  const html =
    (stars >= 2 ? confettiHTML(isMobile ? 24 : 46) : '') +
    '<div class="result-kicker">Goa ' + c.no + ' · ' + gradeLabel(c.bab.g) + '</div>' +
    '<div class="result-title" id="res-title">' + title + '</div>' +
    '<p class="result-sub">' + esc(c.bab.t) + '</p>' +
    '<div class="result-stars" id="res-stars">' + starRowHTML(0, 'huge') + '</div>' +
    '<div class="result-score">' +
      '<div class="score-box good"><b>' + r.correct + '/10</b><span>Benar</span></div>' +
      '<div class="score-box bad"><b>' + (10 - r.correct) + '</b><span>Salah</span></div>' +
      '<div class="score-box"><b>' + stars + '</b><span>Bintang</span></div>' +
    '</div>' +
    '<p class="result-msg">' + resultMessage(r.correct, stars, pass) + '</p>' +
    (r.newBest && r.prevStars >= 0 ? '<div class="stars-note">Rekor terbaikmu untuk goa ini: <b>' + state.best[r.cave] + '/10 benar</b>.</div>' : '') +
    '<div class="result-actions">' + actions + '</div>' +
    '<div class="stars-note">' +
      (pass
        ? (finalCave ? 'Ini goa terakhir—induk Cilik menunggu di puncak!' : 'Goa berikutnya terbuka. Kamu tetap boleh kembali untuk mengejar 3 bintang.')
        : 'Aturan: benar <b>7</b> = 1 bintang · <b>8–9</b> = 2 bintang · <b>10</b> = 3 bintang. Minimal <b>2 bintang</b> untuk naik.')
    + '</div>';
  $('#result-card').innerHTML = html;
  showScreen('result');
  $$('#res-stars .star').forEach((el, i) => {
    if (i < stars) setTimeout(() => el.classList.add('on'), 220 + i * 220);
  });
  const primary = $('#res-primary');
  if (primary) {
    primary.addEventListener('click', () => {
      AudioFX.click();
      hideScreen('result');
      if (pass) {
        if (finalCave) startFinale();
        else travelTo(r.cave + 1);
      } else {
        session = null;
        openQuiz(r.cave);
      }
    });
  }
  $('#res-review').addEventListener('click', () => {
    AudioFX.click();
    openReview();
  });
  $('#res-close').addEventListener('click', () => {
    AudioFX.click();
    hideScreen('result');
    session = null;
    updateCaveCard();
  });
}

function correctTitle(correct) {
  if (correct === 10) return 'Sempurna!';
  if (correct >= 8) return 'Luar biasa!';
  if (correct === 7) return 'Hampir sampai!';
  if (correct >= 4) return 'Terus semangat!';
  return 'Jangan menyerah!';
}

/* ---------- Pembahasan ---------- */
function openReview() {
  const rev = UI.lastReview;
  if (!rev) return;
  const c = caveInfo(rev.cave);
  $('#rev-title').textContent = 'Pembahasan Goa ' + c.no;
  $('#rev-sub').textContent = gradeLabel(c.bab.g) + ' · Bab ' + c.bab.o + ' · ' + c.bab.t + ' — benar ' + rev.correct + '/10';
  let html = '';
  c.qs.forEach((q, i) => {
    const chosen = rev.answers[i];
    const ok = chosen === q.a;
    const letters = ['A', 'B', 'C', 'D', 'E'];
    html += '<details class="review-item"' + (i === 0 ? ' open' : '') + '>' +
      '<summary><span class="st ' + (ok ? 'ok' : 'bad') + '">' + (ok ? '✓' : '✕') + '</span>' +
      '<span class="qt">' + (i + 1) + '. ' + esc(q.q) + '</span><span class="chev">▶</span></summary>' +
      '<div class="rev-body">' +
      (q.st ? '<div class="rev-expl" style="margin-bottom:10px">' + esc(q.st) + '</div>' : '') +
      (chosen != null && !ok ? '<div class="rev-line wrong-answer"><span class="lab bad">Jawabanmu</span><span class="val">' + letters[chosen] + '. ' + esc(q.o[chosen]) + '</span></div>' : '') +
      (chosen == null ? '<div class="rev-line wrong-answer"><span class="lab bad">Jawabanmu</span><span class="val">Tidak dijawab</span></div>' : '') +
      '<div class="rev-line correct-answer"><span class="lab ok">Kunci</span><span class="val">' + letters[q.a] + '. ' + esc(q.o[q.a]) + '</span></div>' +
      '<div class="rev-line"><span class="lab ex">Pembahasan</span><span class="val">' + esc(q.e) + '</span></div>' +
      '</div></details>';
  });
  $('#rev-body').innerHTML = html;
  showScreen('review');
}

/* ---------- Peta ---------- */
function openMap() {
  if (topScreen() === 'result') { /* tetap */ }
  const t = $('#toast'); if (t) { clearTimeout(toastTimer); t.classList.remove('show'); }
  renderMap();
  showScreen('map');
}
function renderMap() {
  $('#map-progress').innerHTML =
    '<div class="mp-box"><b>' + totalStars() + '/450</b><span>Bintang</span></div>' +
    '<div class="mp-box"><b>' + passedCount() + '/150</b><span>Goa dilewati</span></div>' +
    '<div class="mp-box"><b>Goa ' + (state.frontier + 1) + '</b><span>Goa terdepan</span></div>' +
    '<div class="mp-box"><b>' + gradeLabel(caveInfo(state.frontier).bab.g) + '</b><span>Tingkat sekarang</span></div>';

  const grades = [7, 8, 9];
  let html = '';
  grades.forEach(g => {
    const babs = BABS.filter(b => b.g === g);
    html += '<div class="grade-block"><h3><span class="g-badge">Kelas ' + romanGrade(g) + '</span> ' +
      (g === 7 ? 'Fikih dasar: bersuci & shalat' : g === 8 ? 'Ibadah & muamalah' : 'Muamalah lanjut & waris') +
      '<span style="margin-left:auto;font-weight:600;letter-spacing:0;text-transform:none;color:#9a8c72">' +
      babs.length + ' bab · ' + babs.length * 5 + ' goa</span></h3>';
    babs.forEach(bab => {
      const start = babStartCave(bab.o - 1);
      const isCurrentBab = caveInfo(state.cave).bab === bab;
      html += '<div class="bab-row' + (isCurrentBab ? ' current' : '') + '">' +
        '<div class="bt"><b>Bab ' + bab.o + ' · ' + esc(bab.t) + '</b>' +
        '<span>Semester ' + bab.s + ' · goa ' + (start + 1) + '–' + (start + 5) + '</span></div>' +
        '<div class="cave-chips">';
      for (let k = 0; k < 5; k++) {
        const i = start + k;
        const st = state.stars[i] || 0;
        const passed = st >= 2;
        const unlocked = i <= state.frontier;
        const current = i === state.cave;
        let cls = 'cave-chip';
        if (passed) cls += ' passed';
        if (!unlocked) cls += ' locked';
        if (current) cls += ' current';
        const title = 'Goa ' + (i + 1) + (unlocked ? ' · buka' : ' · terkunci');
        html += '<button class="' + cls + '" data-cave="' + i + '" ' + (!unlocked ? 'disabled' : '') +
          ' title="' + title + '" aria-label="' + title + '">' +
          '<span class="cno">' + (k + 1) + '</span>' +
          '<span class="mini-stars">' +
          [0, 1, 2].map(x => '<span class="' + (x < st ? 'on' : '') + '">★</span>').join('') +
          '</span></button>';
      }
      html += '</div></div>';
    });
    html += '</div>';
  });
  $('#map-wrap').innerHTML = html;
  $$('#map-wrap .cave-chip:not(.locked)').forEach(btn => {
    btn.addEventListener('click', () => {
      const i = Number(btn.dataset.cave);
      AudioFX.click();
      hideScreen('map');
      if (i === state.cave) { updateCaveCard(); return; }
      travelTo(i, { instant: true });
    });
  });
  const frontier = state.frontier;
  $('#map-go-frontier').disabled = frontier === state.cave;
}

/* ---------- Pengaturan ---------- */
function renderSettings() {
  const skins = Object.values(SKINS);
  $('#skin-grid').innerHTML = skins.map(s =>
    '<button class="skin' + (s.key === state.style ? ' on' : '') + '" data-skin="' + s.key + '">' +
      '<span class="skin-swatch ' + (s.key === 'chibi' ? 'plain' : '') + '" style="background:' + s.swatch + '"><span>' +
      '' + '</span></span>' +
      '<span class="skin-txt"><b>' + s.name + '</b><span>' + s.short + '</span></span>' +
    '</button>'
  ).join('');
  const biomes = Object.values(BIOMES);
  $('#biome-grid').innerHTML = biomes.map(b =>
    '<button class="biome' + (b.key === state.biome ? ' on' : '') + '" data-biome="' + b.key + '">' +
      biomeCss(b) +
      '<span class="biome-txt"><b>' + b.name + '</b><span>' + b.short + '</span></span>' +
    '</button>'
  ).join('');
  $$('#skin-grid .skin').forEach(btn => {
    btn.addEventListener('click', () => {
      state.style = btn.dataset.skin;
      AudioFX.select();
      applyStyle(state.style);
      renderSettings();
      saveState();
    });
  });
  $$('#biome-grid .biome').forEach(btn => {
    btn.addEventListener('click', () => {
      state.biome = btn.dataset.biome;
      AudioFX.select();
      applyBiome(state.biome);
      renderSettings();
      saveState();
    });
  });
  $('#set-sound').classList.toggle('on', state.sound);
  $('#set-sound').setAttribute('aria-pressed', state.sound ? 'true' : 'false');
  $('#set-cinema').classList.toggle('on', state.cinema);
  $('#set-cinema').setAttribute('aria-pressed', state.cinema ? 'true' : 'false');
  $('#set-keys').classList.toggle('on', state.keys);
  $('#set-keys').setAttribute('aria-pressed', state.keys ? 'true' : 'false');
  $('#btn-sound').classList.toggle('on', state.sound);
  $('#sound-icon').setAttribute('href', state.sound ? '#i-sound' : '#i-mute');
}
function openSettings() {
  renderSettings();
  showScreen('settings');
}
function toggleSound(force) {
  state.sound = force == null ? !state.sound : !!force;
  saveState();
  if (state.sound) { AudioFX.unlock(); AudioFX.select(); }
  $('#btn-sound').classList.toggle('on', state.sound);
  $('#sound-icon').setAttribute('href', state.sound ? '#i-sound' : '#i-mute');
  $('#set-sound').classList.toggle('on', state.sound);
  $('#set-sound').setAttribute('aria-pressed', state.sound ? 'true' : 'false');
  showToast(state.sound ? 'Efek suara dinyalakan' : 'Efek suara dimatikan', 1600);
}

/* ---------- Akhir cerita ---------- */
function startFinale() {
  closeAllScreens();
  UI.introOpen = false;
  document.body.classList.remove('intro-open');
  $('#intro').classList.add('hidden');
  document.body.classList.add('modal-open');
  $('#scene-ui').style.opacity = '0';
  $('#hud').style.opacity = '0';
  AudioFX.finale();
  WORLD.finaleMode = true;
  WORLD.hearts.forEach(h => { h.visible = true; h.position.y = 0.6 + Math.random() * 5; });
  TIGER_ANIM.mode = 'happy';

  const sy = summitY();
  const p = cavePose(state.cave);
  // Kamera terbang ke puncak
  CAM.mode = 'finale';
  CAM.posGoal.set(3.4, sy + 3.4, 11.6);
  CAM.targetGoal.set(0, sy + 1.85, 1.6);
  setTimeout(() => {
    if (!WORLD.ok) { showFinaleCard(); return; }
    WORLD.tigerRoot.position.set(-1.5, sy + 0.02, 2.9);
    WORLD.tigerRoot.rotation.y = 0.34;
    WORLD.tigerShadow.position.set(0, 0.03, 0);
    WORLD.tigerHolder.scale.setScalar(0.82);
    placeCameraFinale();
    setTimeout(() => {
      WORLD.tigerRoot.position.z = 2.35;
      TIGER_ANIM.mode = 'happy';
      WORLD.pointLight.position.set(0, sy + 3.4, 6.5);
      WORLD.pointLight.color.set('#ffdf9e');
      WORLD.pointLight.intensity = 34;
    }, 900);
    setTimeout(showFinaleCard, 2600);
  }, 900);
  if (!WORLD.ok) setTimeout(showFinaleCard, 500);
}
function placeCameraFinale() {
  CAM.posGoal.set(3.4, summitY() + 3.4, 11.6);
  CAM.targetGoal.set(0, summitY() + 1.85, 1.6);
  // posisi kamera diatur oleh updateCamera (mode finale) dengan lerp
}

function showFinaleCard() {
  const el = $('#finale');
  const stars = totalStars();
  const best = state.best.reduce((a, b) => a + Math.max(0, b), 0);
  $('#finale-card').innerHTML =
    '<div class="k">Puncak Bukit Fikih</div>' +
    '<h2>Cilik menemukan induknya!</h2>' +
    '<p>Dengan <b>' + stars + ' bintang</b> dari 150 goa, Cilik berhasil menaklukkan 30 tanjakan dan menuntaskan 1.500 soal Fikih kelas 7–9. Induknya bangga—dan Cilik siap menjelajah lagi.</p>' +
    '<div class="finale-stats">' +
      '<div class="final-stat"><b>' + stars + '/450</b><span>Bintang</span></div>' +
      '<div class="final-stat"><b>150/150</b><span>Goa</span></div>' +
      '<div class="final-stat"><b>30</b><span>Bab</span></div>' +
      '<div class="final-stat"><b>' + best + '/1500</b><span>Jawaban benar</span></div>' +
    '</div>' +
    '<button class="btn btn-gold btn-lg" id="fin-map"><svg><use href="#i-map"/></svg> Lihat Peta Bintang</button>' +
    '<button class="btn btn-ghost btn-lg" id="fin-close">Kembali ke Goa</button>' +
    '<div style="font-size:11px;color:#a8c6bb;margin-top:12px">Terima kasih telah menemani Cilik. Ilmu fikih terbaik adalah yang dipraktikkan.</div>';
  el.classList.remove('hidden');
  $('#fin-map').addEventListener('click', () => {
    AudioFX.click();
    hideFinale();
    openMap();
  });
  $('#fin-close').addEventListener('click', () => {
    AudioFX.click();
    hideFinale();
  });
}
function hideFinale() {
  $('#finale').classList.add('hidden');
  WORLD.finaleMode = false;
  WORLD.hearts.forEach(h => { h.visible = false; });
  $('#scene-ui').style.opacity = '';
  $('#hud').style.opacity = '';
  document.body.classList.remove('modal-open');
  if (WORLD.pointLight) {
    WORLD.pointLight.intensity = 26;
    WORLD.pointLight.color.set(BIOMES[state.biome].glow);
  }
  returnToCaveAfterFinale();
}
function returnToCaveAfterFinale() {
  if (!WORLD.ok) { openIntro(); return; }
  document.body.classList.remove('modal-open');
  CAM.mode = 'follow';
  CAM.override = null;
  CAM.yaw = 0.2;
  placeTigerAt(state.cave, true);
  TIGER_ANIM.mode = 'idle';
  updateCaveCard();
}

/* ---------- Inisialisasi alur ---------- */
function initGameFlow() {
  // Tombol utama
  $('#btn-start').addEventListener('click', beginAdventure);
  $('#btn-resume').addEventListener('click', () => {
    if (state.finished) {
      startFinale();
    } else {
      beginAdventure();
    }
  });
  $('#btn-enter').addEventListener('click', enterCave);
  $('#btn-map').addEventListener('click', () => { AudioFX.click(); openMap(); });
  $('#btn-map-2').addEventListener('click', () => { AudioFX.click(); openMap(); });
  $('#btn-intro-map').addEventListener('click', () => { AudioFX.click(); openMap(); });
  $('#btn-settings').addEventListener('click', () => { AudioFX.click(); openSettings(); });
  $('#btn-intro-settings').addEventListener('click', () => { AudioFX.click(); openSettings(); });
  $('#btn-sound').addEventListener('click', () => toggleSound());
  $('#brand-home').addEventListener('click', () => {
    if (topScreen()) return;
    openIntro();
  });
  $('#btn-full').addEventListener('click', toggleFullscreen);
  $('#q-close').addEventListener('click', () => { AudioFX.click(); closeQuiz(); });
  $('#q-next').addEventListener('click', () => { AudioFX.click(); nextQuestion(); });
  $('#map-close').addEventListener('click', () => { AudioFX.click(); hideScreen('map'); });
  $('#map-go-frontier').addEventListener('click', () => {
    AudioFX.click();
    hideScreen('map');
    travelTo(state.frontier, { instant: true });
  });
  $('#rev-close').addEventListener('click', () => { AudioFX.click(); hideScreen('review'); });
  $('#rev-back').addEventListener('click', () => { AudioFX.click(); hideScreen('review'); });
  $('#set-close').addEventListener('click', () => { AudioFX.click(); hideScreen('settings'); });
  $('#set-done').addEventListener('click', () => { AudioFX.click(); hideScreen('settings'); });
  $('#set-sound').addEventListener('click', () => toggleSound());
  $('#set-cinema').addEventListener('click', () => {
    state.cinema = !state.cinema;
    saveState();
    $('#set-cinema').classList.toggle('on', state.cinema);
    $('#set-cinema').setAttribute('aria-pressed', state.cinema ? 'true' : 'false');
    AudioFX.select();
  });
  $('#set-keys').addEventListener('click', () => {
    state.keys = !state.keys;
    saveState();
    $('#set-keys').classList.toggle('on', state.keys);
    $('#set-keys').setAttribute('aria-pressed', state.keys ? 'true' : 'false');
    AudioFX.select();
  });
  $('#set-reset').addEventListener('click', () => {
    if (!confirm('Mulai ulang perjalanan? Semua bintang dan progres akan dihapus.')) return;
    if (!confirm('Yakin? Tindakan ini tidak bisa dibatalkan.')) return;
    try { localStorage.removeItem(SAVE_KEY); } catch (e) {}
    state = defaultState();
    session = null;
    location.reload();
  });

  // Pintasan papan ketik
  document.addEventListener('keydown', e => {
    const tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea') return;
    const top = topScreen();
    if (e.key === 'Escape') {
      if (top === 'review') { hideScreen('review'); return; }
      if (top === 'map') { hideScreen('map'); return; }
      if (top === 'settings') { hideScreen('settings'); return; }
      if (top === 'result') { $('#res-close') && $('#res-close').click(); return; }
      if (top === 'quiz') { closeQuiz(); return; }
      return;
    }
    if (top === 'quiz') {
      if (state.keys && /^[1-4]$/.test(e.key)) {
        e.preventDefault();
        const k = Number(e.key) - 1;
        const q = caveInfo(session.cave).qs[session.qi];
        if (k < q.o.length) chooseAnswer(k);
      }
      if (e.key === 'Enter' && !$('#q-next').disabled) { e.preventDefault(); nextQuestion(); }
      return;
    }
    if (top) return;
    if (e.key === 'm' || e.key === 'M') { openMap(); }
    if (e.key === 'p' || e.key === 'P') { openSettings(); }
  });

  window.addEventListener('resize', () => {
    if (UI.stack.includes('map')) { /* biarkan */ }
  });

  // Intro & kartu awal
  refreshIntro();
  updateCaveCard();
  syncHud();
}
