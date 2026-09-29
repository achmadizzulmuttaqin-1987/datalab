/* ============================================================
   Bank Soal Akidah Akhlak MTs — app.js
   Aplikasi standalone (vanilla JS, tanpa dependensi eksternal)
   ============================================================ */
var App = (function () {
  'use strict';

  /* ---------- Konstanta ---------- */
  var LS_KEY = 'banksoal_akidah_akhlak_mts_v1';
  var GRADE_LABEL = { 7: 'Kelas VII', 8: 'Kelas VIII', 9: 'Kelas IX' };
  var LEVEL_LABEL = { HOTS: 'HOTS', MOTS: 'MOTS', LOTS: 'LOTS' };
  var LETTERS = ['A', 'B', 'C', 'D', 'E'];

  /* ---------- State ---------- */
  var S = {
    tab: 'bank',            // bank | browse | stats
    grade: 0,               // 0 = semua
    setup: null,            // topik yang sedang dikonfigurasi
    quiz: null,             // sesi latihan aktif
    browse: null,           // {id, page, filter, showKey}
    missing: null
  };

  var store = { history: [], mastery: {}, weak: {} };

  function loadStore() {
    try {
      var raw = localStorage.getItem(LS_KEY);
      if (raw) {
        var o = JSON.parse(raw);
        store.history = o.history || [];
        store.mastery = o.mastery || {};
        store.weak = o.weak || {};
      }
    } catch (e) { /* storage tidak tersedia */ }
  }
  function saveStore() {
    try { localStorage.setItem(LS_KEY, JSON.stringify(store)); } catch (e) {}
  }

  /* ---------- Data helper ---------- */
  function topics() {
    var t = window.__BS && window.__BS.topics ? window.__BS.topics : {};
    return Object.keys(t).map(function (k) { return t[k]; }).sort(function (a, b) {
      return (a.grade - b.grade) || (a.order - b.order);
    });
  }
  function byGrade(g) { return topics().filter(function (t) { return !g || t.grade === g; }); }
  function countQ(list) { return list.reduce(function (n, t) { return n + (t.questions ? t.questions.length : 0); }, 0); }
  function topicById(id) { return (window.__BS.topics || {})[id] || null; }
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function shuffle(a) {
    var arr = a.slice();
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }
  function pad(n) { return n < 10 ? '0' + n : '' + n; }
  function fmtDur(sec) {
    sec = Math.max(0, Math.round(sec));
    var h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
    return (h ? h + ':' : '') + pad(m) + ':' + pad(s);
  }
  function fmtDate(ts) {
    var d = new Date(ts);
    return pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear() + ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes());
  }

  /* ---------- UI kecil ---------- */
  var $view = null;
  function toast(msg) {
    var t = document.getElementById('toast');
    t.textContent = msg; t.classList.add('on');
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('on'); }, 2200);
  }
  function modal(html, onMount) {
    var m = document.getElementById('modal'), b = document.getElementById('mbox');
    b.innerHTML = html; m.classList.add('on');
    if (onMount) onMount(b);
    b.querySelectorAll('[data-close]').forEach(function (el) {
      el.onclick = function () { m.classList.remove('on'); };
    });
  }
  function closeModal() { document.getElementById('modal').classList.remove('on'); }
  function ring(pct, label) {
    var c = pct >= 80 ? '#1a8f5a' : pct >= 60 ? '#c9962b' : '#c0392b';
    return '<div class="ring" style="--p:' + pct + ';--rc:' + c + '"><div class="in"><div><b>' + Math.round(pct) + '</b><span>' + (label || 'Nilai') + '</span></div></div></div>';
  }
  function progressOf(id) {
    var h = store.history.filter(function (x) { return x.id === id; });
    if (!h.length) return { best: null, tries: 0, pct: 0 };
    var best = h.reduce(function (a, b) { return b.score > a.score ? b : a; });
    return { best: best, tries: h.length, pct: best.score };
  }

  /* ============================================================
     VIEW: BANK SOAL (beranda)
     ============================================================ */
  function viewBank() {
    var all = topics();
    var list = byGrade(S.grade);
    var totalQ = countQ(all);
    var done = store.history.length;
    var avg = done ? Math.round(store.history.reduce(function (a, b) { return a + b.score; }, 0) / done) : 0;

    var html = '';
    html += '<div class="hero">' +
      '<h2>Bank Soal Akidah Akhlak Madrasah Tsanawiyah</h2>' +
      '<p>Kumpulan soal pilihan ganda berorientasi <b>HOTS</b> yang disusun per materi untuk kelas VII, VIII, dan IX sesuai ruang lingkup KMA 183 Tahun 2019. Setiap soal dilengkapi kunci jawaban dan pembahasan untuk belajar mandiri maupun latihan ulangan, PTS, PAS, dan persiapan Asesmen Madrasah.</p>' +
      '<div class="stat-row">' +
        stat(totalQ, 'Total Soal') +
        stat(all.length, 'Materi / Topik') +
        stat(3, 'Kelas') +
        stat(done, 'Latihan Selesai') +
        stat(avg, 'Rata-rata Nilai') +
      '</div></div>';

    html += '<div class="gradebar">' +
      gchip(0, 'Semua Kelas', all.length) +
      gchip(7, 'Kelas VII', byGrade(7).length) +
      gchip(8, 'Kelas VIII', byGrade(8).length) +
      gchip(9, 'Kelas IX', byGrade(9).length) +
    '</div>';

    if (S.missing && S.missing.length) {
      html += '<div class="empty" style="margin-bottom:14px;border-color:#f2cfcb;background:#fdeceb"><b>Sebagian berkas soal gagal dimuat</b>' +
        esc(S.missing.join(', ')) +
        '<div style="margin-top:10px;font-size:13px">Jika Anda membuka berkas <code>index.html</code> langsung dari folder (double-click), beberapa browser memblokir pemuatan berkas terpisah. Gunakan versi <b>satu berkas</b> (<code>Bank-Soal-Akidah-Akhlak-MTs-1file.html</code>) atau jalankan lewat server lokal.</div></div>';
    }

    // kelompokkan per semester
    var groups = {};
    list.forEach(function (t) {
      var k = t.grade + '|' + t.semester;
      (groups[k] = groups[k] || []).push(t);
    });
    Object.keys(groups).sort().forEach(function (k) {
      var g = groups[k][0];
      html += '<h3 style="margin:22px 0 10px;font-size:15px;color:var(--ink-2);text-transform:uppercase;letter-spacing:.5px">' +
        GRADE_LABEL[g.grade] + ' &middot; Semester ' + g.semester +
        ' <span style="color:var(--muted);font-weight:600;text-transform:none;letter-spacing:0">(' + countQ(groups[k]) + ' soal)</span></h3>';
      html += '<div class="grid">' + groups[k].map(cardTopic).join('') + '</div>';
    });

    if (!list.length) html += '<div class="empty"><b>Belum ada materi</b>Data soal belum termuat.</div>';

    render(html);
    bindBank();
  }
  function stat(v, l) { return '<div class="stat"><b>' + v + '</b><span>' + l + '</span></div>'; }
  function gchip(g, label, n) {
    return '<button class="chip' + (S.grade === g ? ' on' : '') + '" data-grade="' + g + '">' + label + ' <span class="n">' + n + '</span></button>';
  }
  function cardTopic(t) {
    var p = progressOf(t.id);
    var nq = t.questions ? t.questions.length : 0;
    var hots = t.questions ? t.questions.filter(function (q) { return q.level === 'HOTS'; }).length : 0;
    return '<div class="card">' +
      '<div class="sem">Smt ' + t.semester + '</div>' +
      '<h3>' + esc(t.title) + '</h3>' +
      (t.desc ? '<p class="desc">' + esc(t.desc) + '</p>' : '') +
      '<div class="meta"><span class="tag">' + nq + ' Soal</span>' +
        '<span class="tag g">' + hots + ' HOTS</span>' +
        (t.kd ? '<span class="tag b" title="' + esc(t.kd) + '">' + esc(t.kd.length > 22 ? t.kd.slice(0, 22) + '…' : t.kd) + '</span>' : '') +
      '</div>' +
      '<div class="prog"><i style="width:' + p.pct + '%"></i></div>' +
      '<div class="row" style="font-size:12px;color:var(--muted)">' +
        (p.tries ? '<span>Nilai terbaik <b style="color:var(--green-d)">' + p.pct + '</b> · ' + p.tries + '× latihan</span>' : '<span>Belum pernah dilatih</span>') +
      '</div>' +
      '<div class="row" style="margin-top:2px">' +
        '<button class="btn grow" data-start="' + t.id + '">▶ Latihan Soal</button>' +
        '<button class="btn ghost" data-browse="' + t.id + '" title="Lihat semua soal">📖</button>' +
      '</div></div>';
  }
  function bindBank() {
    document.querySelectorAll('[data-grade]').forEach(function (b) {
      b.onclick = function () { S.grade = +b.dataset.grade; viewBank(); };
    });
    document.querySelectorAll('[data-start]').forEach(function (b) {
      b.onclick = function () { openSetup(b.dataset.start); };
    });
    document.querySelectorAll('[data-browse]').forEach(function (b) {
      b.onclick = function () { S.tab = 'browse'; S.browse = { id: b.dataset.browse, filter: 'all', showKey: false }; renderShell(); };
    });
  }

  /* ============================================================
     VIEW: SETUP LATIHAN
     ============================================================ */
  function openSetup(id) {
    var t = topicById(id); if (!t) return;
    S.setup = {
      id: id, n: Math.min(50, t.questions.length), mode: 'belajar',
      shuffle: true, timer: 0, level: 'all'
    };
    viewSetup();
  }
  function viewSetup() {
    var t = topicById(S.setup.id); if (!t) { S.tab = 'bank'; return viewBank(); }
    var qs = t.questions || [];
    var nH = qs.filter(function (q) { return q.level === 'HOTS'; }).length;
    var maxN = S.setup.level === 'all' ? qs.length : nH;
    if (S.setup.n > maxN) S.setup.n = maxN;

    var html = '<div class="sheet">' +
      '<div style="display:flex;gap:8px;align-items:center;margin-bottom:6px;flex-wrap:wrap">' +
        '<span class="tag">' + GRADE_LABEL[t.grade] + '</span><span class="tag g">Semester ' + t.semester + '</span>' +
        (t.kd ? '<span class="tag b">' + esc(t.kd) + '</span>' : '') +
      '</div>' +
      '<h3>' + esc(t.title) + '</h3>' +
      '<p class="sub">' + esc(t.desc || '') + '</p>' +
      '<div style="height:1px;background:var(--line);margin:0 0 16px"></div>' +

      fld('Mode Latihan', '<div class="opts">' +
        opt('mode', 'belajar', '📚 Belajar', 'Jawaban &amp; pembahasan langsung muncul') +
        opt('mode', 'ujian', '📝 Simulasi Ujian', 'Pembahasan di akhir, ada navigasi soal') +
        opt('mode', 'cepat', '⚡ Cepat', 'Tanpa pembahasan, hanya skor') +
      '</div>') +

      fld('Jumlah Soal <span style="text-transform:none;font-weight:600;color:var(--muted)">(tersedia ' + maxN + ')</span>',
        '<div class="opts">' +
        [10, 20, 30, 40, 50].filter(function (n) { return n <= maxN; }).map(function (n) {
          return opt('n', n, n + ' Soal');
        }).join('') +
        opt('n', maxN, 'Semua (' + maxN + ')') +
      '</div>') +

      fld('Tingkat Kesulitan', '<div class="opts">' +
        opt('level', 'all', 'Semua (' + qs.length + ')') +
        opt('level', 'hots', 'HOTS saja (' + nH + ')') +
      '</div>') +

      fld('Acak Urutan Soal', '<div class="opts">' +
        opt('shuffle', true, '🔀 Diacak') + opt('shuffle', false, '📑 Sesuai urutan materi') +
      '</div>') +

      fld('Batas Waktu', '<div class="opts">' +
        opt('timer', 0, 'Tanpa batas') + opt('timer', 30, '30 menit') + opt('timer', 60, '60 menit') + opt('timer', 90, '90 menit') +
      '</div><div class="hint">Waktu habis = latihan otomatis dinilai.</div>') +

      '<div style="display:flex;gap:9px;margin-top:20px;flex-wrap:wrap">' +
        '<button class="btn big grow" id="goQuiz">Mulai Latihan →</button>' +
        '<button class="btn ghost big" id="goBrowse">📖 Lihat Semua Soal</button>' +
        '<button class="btn ghost big" id="goBack">← Kembali</button>' +
      '</div></div>';

    render(html);

    document.querySelectorAll('.opt').forEach(function (b) {
      b.onclick = function () {
        var k = b.dataset.k, v = b.dataset.v;
        v = (v === 'true') ? true : (v === 'false') ? false : (isNaN(+v) ? v : +v);
        S.setup[k] = v; viewSetup();
      };
    });
    document.getElementById('goQuiz').onclick = startQuiz;
    document.getElementById('goBrowse').onclick = function () { S.tab = 'browse'; S.browse = { id: t.id, filter: 'all', showKey: false }; renderShell(); };
    document.getElementById('goBack').onclick = function () { S.tab = 'bank'; S.setup = null; renderShell(); };
  }
  function fld(label, inner) { return '<div class="field"><label>' + label + '</label>' + inner + '</div>'; }
  function opt(k, v, label, sub) {
    var on = String(S.setup[k]) === String(v);
    return '<button class="opt' + (on ? ' on' : '') + '" data-k="' + k + '" data-v="' + v + '">' + label +
      (sub ? '<div style="font-size:11.3px;font-weight:500;opacity:.72;margin-top:1px">' + sub + '</div>' : '') + '</button>';
  }

  /* ============================================================
     QUIZ ENGINE
     ============================================================ */
  function startQuiz() {
    var t = topicById(S.setup.id);
    var pool = (t.questions || []).slice();
    if (S.setup.level === 'hots') pool = pool.filter(function (q) { return q.level === 'HOTS'; });
    if (!pool.length) return toast('Tidak ada soal pada filter ini.');
    if (S.setup.shuffle) pool = shuffle(pool);
    pool = pool.slice(0, S.setup.n);

    // siapkan opsi (acak posisi opsi bila mode acak)
    var items = pool.map(function (q, i) {
      var correctIdx = q.answer;
      var opts = q.options.map(function (txt, oi) { return { txt: txt, orig: oi }; });
      if (S.setup.shuffle) opts = shuffle(opts);
      var newCorrect = 0;
      opts.forEach(function (o, ni) { if (o.orig === correctIdx) newCorrect = ni; });
      return {
        n: i + 1, q: q, opts: opts.map(function (o) { return o.txt; }),
        answer: newCorrect, pick: -1, flagged: false, revealed: false
      };
    });

    S.quiz = {
      topic: t, items: items, cur: 0, mode: S.setup.mode,
      t0: Date.now(), limit: S.setup.timer * 60, left: S.setup.timer * 60,
      finished: false, timerId: null, order: items.map(function (_, i) { return i; })
    };
    document.body.classList.add('in-quiz');
    if (S.quiz.limit) {
      S.quiz.timerId = setInterval(function () {
        S.quiz.left--;
        var el = document.getElementById('qtime');
        if (el) {
          el.textContent = '⏱ ' + fmtDur(S.quiz.left);
          el.classList.toggle('warn', S.quiz.left <= 60);
        }
        if (S.quiz.left <= 0) { clearInterval(S.quiz.timerId); finish(true); }
      }, 1000);
    }
    viewQuiz();
  }

  function viewQuiz() {
    var Q = S.quiz; if (!Q) return;
    var it = Q.items[Q.cur];
    var answered = Q.items.filter(function (x) { return x.pick >= 0; }).length;
    var done = Q.items.filter(function (x) { return x.revealed; }).length;
    var pct = Math.round((Q.cur + 1) / Q.items.length * 100);

    var html = '<div class="qbar">' +
      '<div class="ttl">' + esc(Q.topic.title) + '</div>' +
      '<span class="pill">' + GRADE_LABEL[Q.topic.grade] + '</span>' +
      (Q.limit ? '<span class="pill time" id="qtime">⏱ ' + fmtDur(Q.left) + '</span>' : '') +
      '<span class="pill">Soal ' + (Q.cur + 1) + '/' + Q.items.length + '</span>' +
      '<span class="pill" style="background:#eef1f6;color:#4b5b70;border-color:#dde3ec">Terjawab ' + answered + '</span>' +
      '<button class="btn gold sm" id="btnFinish">Selesai &amp; Nilai ✓</button>' +
      '<div class="qtrack" style="flex-basis:100%"><i style="width:' + pct + '%"></i></div>' +
    '</div>';

    html += '<div class="qcard" id="qcard">' + questionHtml(it, Q) + '</div>';

    html += '<div class="palette">' +
      '<h4>Navigasi Soal</h4><div class="pgrid">' +
      Q.items.map(function (x, i) {
        var c = 'pcell';
        if (Q.mode === 'belajar' && x.revealed) c += x.pick === x.answer ? ' right' : ' wr';
        else if (x.pick >= 0) c += ' ans-d';
        if (i === Q.cur) c += ' cur';
        if (x.flagged) c += ' flag';
        return '<button class="' + c + '" data-jump="' + i + '">' + (i + 1) + '</button>';
      }).join('') +
      '</div>' +
      '<div class="legend">' +
        '<span><i style="background:#eef2f0"></i>Belum dijawab</span>' +
        '<span><i style="background:var(--green-l);border-color:#bfe0d3"></i>Sudah dijawab</span>' +
        '<span><i style="background:var(--ok-l);border-color:#bfe4cf"></i>Benar</span>' +
        '<span><i style="background:var(--bad-l);border-color:#f2cfcb"></i>Salah</span>' +
        '<span><i style="background:var(--gold)"></i>Ditandai</span>' +
      '</div></div>';

    render(html, true);
    bindQuiz(it, Q);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function questionHtml(it, Q) {
    var q = it.q;
    var locked = (Q.mode === 'belajar' && it.revealed);
    var lvl = q.level || 'HOTS';
    var h = '<div class="qhead">' +
      '<span class="qnum">No. ' + it.n + '</span>' +
      '<span class="badge ' + lvl.toLowerCase() + '">' + (LEVEL_LABEL[lvl] || lvl) + '</span>' +
      (q.indicator ? '<span class="badge ind">' + esc(q.indicator) + '</span>' : '') +
    '</div>';

    if (q.stimulus) {
      var st = q.stimulus;
      if (q.stimulusAr) st = '<span class="arab">' + esc(q.stimulusAr) + '</span>' + esc(st);
      h += '<div class="qstim">' + st + '</div>';
    }
    h += '<div class="qtext">' + esc(q.text) + '</div>';
    h += '<div class="answers">';
    it.opts.forEach(function (o, i) {
      var cls = 'ans';
      if (locked) {
        cls += i === it.answer ? ' correct' : (i === it.pick ? ' wrong' : '');
      } else if (it.pick === i) cls += ' on';
      h += '<button class="' + cls + '" data-pick="' + i + '"' + (locked ? ' disabled' : '') + '>' +
        '<span class="k">' + LETTERS[i] + '</span><span class="t">' + esc(o) + '</span></button>';
    });
    h += '</div>';

    if (locked) {
      var ok = it.pick === it.answer;
      h += '<div class="fb ' + (ok ? 'ok' : 'no') + '"><b>' + (ok ? '✓ Jawaban benar!' : '✕ Jawaban kurang tepat.') + '</b>' +
        (ok ? '' : 'Kunci jawaban: <b>' + LETTERS[it.answer] + '. ' + esc(it.opts[it.answer]) + '</b>') + '</div>';
      if (q.explanation) h += '<div class="exp"><b style="color:var(--green-d)">💡 Pembahasan</b><br>' + esc(q.explanation) + '</div>';
    }

    h += '<div class="qnav">' +
      '<button class="btn ghost" id="prevQ"' + (Q.cur === 0 ? ' disabled' : '') + '>← Sebelumnya</button>' +
      '<button class="btn ghost" id="flagQ">' + (it.flagged ? '🚩 Hapus Tanda' : '🏳 Tandai Ragu') + '</button>' +
      '<span class="grow"></span>' +
      (Q.mode === 'belajar' && !it.revealed
        ? '<button class="btn" id="checkQ">Periksa Jawaban ✓</button>'
        : '<button class="btn" id="nextQ">' + (Q.cur === Q.items.length - 1 ? 'Lihat Hasil →' : 'Selanjutnya →') + '</button>') +
    '</div>';
    return h;
  }

  function bindQuiz(it, Q) {
    document.querySelectorAll('[data-pick]').forEach(function (b) {
      b.onclick = function () {
        it.pick = +b.dataset.pick;
        if (Q.mode !== 'belajar') { renderQuizOnly(); }
        else { viewQuiz(); }
      };
    });
    var j = document.querySelectorAll('[data-jump]');
    j.forEach(function (b) { b.onclick = function () { Q.cur = +b.dataset.jump; viewQuiz(); }; });
    var p = document.getElementById('prevQ'); if (p) p.onclick = function () { if (Q.cur > 0) { Q.cur--; viewQuiz(); } };
    var n = document.getElementById('nextQ'); if (n) n.onclick = function () {
      if (Q.cur < Q.items.length - 1) { Q.cur++; viewQuiz(); } else confirmFinish();
    };
    var c = document.getElementById('checkQ'); if (c) c.onclick = function () {
      if (it.pick < 0) return toast('Pilih salah satu jawaban terlebih dahulu.');
      it.revealed = true;
      recordAnswer(Q, it);
      viewQuiz();
    };
    var f = document.getElementById('flagQ'); if (f) f.onclick = function () { it.flagged = !it.flagged; renderQuizOnly(); };
    document.getElementById('btnFinish').onclick = confirmFinish;
  }
  function renderQuizOnly() {
    var Q = S.quiz;
    var card = document.getElementById('qcard');
    if (card) {
      card.innerHTML = questionHtml(Q.items[Q.cur], Q);
      bindQuiz(Q.items[Q.cur], Q);
    }
    document.querySelectorAll('[data-jump]').forEach(function (b, i) {
      var x = Q.items[i], c = 'pcell';
      if (Q.mode === 'belajar' && x.revealed) c += x.pick === x.answer ? ' right' : ' wr';
      else if (x.pick >= 0) c += ' ans-d';
      if (i === Q.cur) c += ' cur';
      if (x.flagged) c += ' flag';
      b.className = c;
    });
  }

  function recordAnswer(Q, it) {
    var id = Q.topic.id;
    var m = store.mastery[id] || (store.mastery[id] = { c: 0, t: 0 });
    m.t++; if (it.pick === it.answer) m.c++;
    if (it.pick !== it.answer) {
      var w = store.weak[id] || (store.weak[id] = {});
      var key = it.q.indicator || 'umum';
      w[key] = (w[key] || 0) + 1;
    }
    saveStore();
  }

  function confirmFinish() {
    var Q = S.quiz;
    var un = Q.items.filter(function (x) { return x.pick < 0; }).length;
    var wrong = Q.items.filter(function (x) { return x.pick >= 0 && (Q.mode !== 'belajar' ? false : x.pick !== x.answer); }).length;
    modal('<h3>Selesaikan latihan?</h3>' +
      '<p>' + (un ? 'Masih ada <b>' + un + ' soal belum dijawab</b>. ' : '') +
      (Q.mode === 'belajar' && wrong ? 'Sudah ada <b>' + wrong + ' jawaban salah</b>. ' : '') +
      'Soal yang belum dijawab akan dihitung salah dalam penilaian.</p>' +
      '<div class="mrow"><button class="btn ghost" data-close>Batal</button>' +
      '<button class="btn danger" id="doFinish">Ya, Nilai Sekarang</button></div>',
      function (b) { b.querySelector('#doFinish').onclick = function () { closeModal(); finish(false); }; });
  }

  function finish(auto) {
    var Q = S.quiz; if (!Q || Q.finished) return;
    Q.finished = true;
    if (Q.timerId) clearInterval(Q.timerId);
    var secs = (Date.now() - Q.t0) / 1000;
    var benar = 0;
    Q.items.forEach(function (it) {
      if (Q.mode !== 'belajar' && !it.revealed) it.revealed = true;
      if (it.pick === it.answer) benar++;
    });
    var score = Math.round(benar / Q.items.length * 100);
    Q.result = { benar: benar, salah: Q.items.length - benar, score: score, secs: secs, auto: auto };

    store.history.unshift({
      id: Q.topic.id, title: Q.topic.title, grade: Q.topic.grade,
      score: score, benar: benar, total: Q.items.length,
      mode: Q.mode, ts: Date.now(), dur: Math.round(secs)
    });
    if (store.history.length > 300) store.history.length = 300;
    saveStore();
    viewResult();
    if (auto) toast('Waktu habis — latihan otomatis dinilai.');
  }

  function viewResult() {
    var Q = S.quiz, R = Q.result;
    var p = progressOf(Q.topic.id);
    var html = '<div class="score-hero">' +
      ring(R.score) +
      '<div class="verdict"><b>' + verdictText(R.score) + '</b><br>' +
        esc(Q.topic.title) + ' · ' + GRADE_LABEL[Q.topic.grade] + '</div>' +
      '<div class="res-grid">' +
        '<div class="res-cell ok"><b>' + R.benar + '</b><span>Benar</span></div>' +
        '<div class="res-cell bad"><b>' + R.salah + '</b><span>Salah / Kosong</span></div>' +
        '<div class="res-cell mut"><b>' + R.total + '</b><span>Total Soal</span></div>' +
        '<div class="res-cell mut"><b>' + fmtDur(R.secs) + '</b><span>Waktu</span></div>' +
        '<div class="res-cell mut"><b>' + p.pct + '</b><span>Nilai Terbaik</span></div>' +
      '</div>' +
      '<div style="display:flex;gap:9px;justify-content:center;margin-top:20px;flex-wrap:wrap">' +
        '<button class="btn" id="rReview">🔍 Bahas Jawaban</button>' +
        '<button class="btn ghost" id="rRetry">↻ Ulangi Latihan</button>' +
        '<button class="btn ghost" id="rWrong">✕ Bahas yang Salah Saja</button>' +
        '<button class="btn ghost" id="rPrint">🖨 Cetak / PDF</button>' +
        '<button class="btn ghost" id="rHome">🏠 Beranda</button>' +
      '</div></div>' +
      '<div id="reviewBox"></div>';
    render(html, true);
    document.getElementById('rReview').onclick = function () { showReview(Q, 'all'); };
    document.getElementById('rWrong').onclick = function () { showReview(Q, 'wrong'); };
    document.getElementById('rRetry').onclick = function () {
      var cfg = { id: Q.topic.id, n: Q.items.length, mode: Q.mode, shuffle: true, timer: Q.limit / 60 | 0, level: S.setup ? S.setup.level : 'all' };
      S.setup = cfg; document.body.classList.remove('in-quiz'); startQuiz();
    };
    document.getElementById('rPrint').onclick = function () { showReview(Q, 'all'); setTimeout(function () { window.print(); }, 250); };
    document.getElementById('rHome').onclick = exitQuiz;
  }
  function verdictText(s) {
    if (s >= 95) return 'Masyaallah, sempurna! 🏆';
    if (s >= 85) return 'Sangat baik, pertahankan! ⭐';
    if (s >= 75) return 'Baik, sudah di atas KKM. 👍';
    if (s >= 60) return 'Cukup, perkuat lagi pembahasannya.';
    return 'Perlu pendalaman materi. Jangan menyerah! 💪';
  }
  function showReview(Q, filter) {
    var box = document.getElementById('reviewBox'); if (!box) return;
    var items = Q.items.filter(function (it) { return filter === 'all' || it.pick !== it.answer; });
    box.innerHTML = '<div class="review">' +
      '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">' +
        '<h3 style="margin:0;font-size:16px">Pembahasan ' + (filter === 'all' ? 'Seluruh Soal' : 'Soal yang Salah') + ' (' + items.length + ')</h3>' +
        '<button class="btn ghost sm" id="closeRev">Tutup</button></div>' +
      items.map(reviewItem).join('') + '</div>';
    document.getElementById('closeRev').onclick = function () { box.innerHTML = ''; };
    box.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  function reviewItem(it) {
    var ok = it.pick === it.answer, cls = it.pick < 0 ? 'sk' : (ok ? 'ok' : 'no');
    var h = '<div class="ritem ' + cls + '">' +
      '<div class="rh"><span class="qnum">No. ' + it.n + '</span>' +
      '<span class="badge ' + (it.q.level || 'HOTS').toLowerCase() + '">' + (LEVEL_LABEL[it.q.level || 'HOTS']) + '</span>' +
      (it.q.indicator ? '<span class="badge ind">' + esc(it.q.indicator) + '</span>' : '') +
      '<span class="pillsm ' + (it.pick < 0 ? 'no' : ok ? 'ok' : 'no') + '">' + (it.pick < 0 ? 'Tidak dijawab' : ok ? 'Benar' : 'Salah') + '</span></div>';
    if (it.q.stimulus) h += '<div class="qstim">' + (it.q.stimulusAr ? '<span class="arab">' + esc(it.q.stimulusAr) + '</span>' : '') + esc(it.q.stimulus) + '</div>';
    h += '<div class="qtext">' + esc(it.q.text) + '</div>';
    it.opts.forEach(function (o, i) {
      var c = 'ans-line';
      if (i === it.answer) c = 'ans-line';
      var mark = i === it.answer ? ' ✅' : (i === it.pick ? ' ❌' : '');
      h += '<div class="' + c + '" style="' + (i === it.answer ? 'color:var(--ok)' : i === it.pick ? 'color:var(--bad)' : 'color:var(--ink-2)') + '">' +
        '<b>' + LETTERS[i] + '.</b> ' + esc(o) + mark + '</div>';
    });
    if (it.pick >= 0 && !ok) h += '<div class="ans-line" style="margin-top:6px;color:var(--bad)">Jawabanmu: <b>' + LETTERS[it.pick] + '</b> · Kunci: <b>' + LETTERS[it.answer] + '</b></div>';
    if (it.q.explanation) h += '<div class="exp"><b style="color:var(--green-d)">💡 Pembahasan</b><br>' + esc(it.q.explanation) + '</div>';
    return h + '</div>';
  }

  function exitQuiz() {
    if (S.quiz && !S.quiz.finished && S.quiz.items.some(function (x) { return x.pick >= 0; })) {
      modal('<h3>Keluar dari latihan?</h3><p>Progres latihan ini belum dinilai dan akan hilang.</p>' +
        '<div class="mrow"><button class="btn ghost" data-close>Lanjut Latihan</button>' +
        '<button class="btn danger" id="doExit">Keluar</button></div>',
        function (b) { b.querySelector('#doExit').onclick = function () { closeModal(); reallyExit(); }; });
    } else reallyExit();
  }
  function reallyExit() {
    if (S.quiz && S.quiz.timerId) clearInterval(S.quiz.timerId);
    S.quiz = null; S.setup = null; S.tab = 'bank';
    document.body.classList.remove('in-quiz');
    renderShell();
  }

  /* ============================================================
     VIEW: JELAJAH / BACA SOAL
     ============================================================ */
  function viewBrowse() {
    var b = S.browse;
    var t = topicById(b.id);
    if (!t) { S.tab = 'bank'; return viewBank(); }
    var qs = (t.questions || []).map(function (q, i) { return { q: q, i: i }; });
    var f = b.filter;
    if (f === 'hots') qs = qs.filter(function (x) { return x.q.level === 'HOTS'; });
    if (f === 'unseen') {
      var m = store.mastery[t.id];
      qs = qs.filter(function () { return !m; });
    }
    var term = (b.term || '').toLowerCase().trim();
    if (term) qs = qs.filter(function (x) {
      return (x.q.text + ' ' + (x.q.stimulus || '') + ' ' + x.q.options.join(' ') + ' ' + (x.q.explanation || '')).toLowerCase().indexOf(term) >= 0;
    });

    var perPage = 20, pages = Math.max(1, Math.ceil(qs.length / perPage));
    b.page = Math.min(b.page || 1, pages);
    var slice = qs.slice((b.page - 1) * perPage, b.page * perPage);

    var html = '<div class="sheet" style="margin-bottom:14px">' +
      '<div style="display:flex;gap:8px;align-items:center;margin-bottom:6px;flex-wrap:wrap">' +
        '<span class="tag">' + GRADE_LABEL[t.grade] + '</span><span class="tag g">Semester ' + t.semester + '</span>' +
        '<span class="tag b">' + (t.questions || []).length + ' soal</span></div>' +
      '<h3 style="margin-bottom:2px">📖 ' + esc(t.title) + '</h3>' +
      '<p class="sub" style="margin-bottom:12px">' + esc(t.desc || '') + '</p>' +
      '<div class="filters">' +
        '<input class="search" id="bsearch" placeholder="Cari kata kunci soal / pembahasan…" value="' + esc(b.term || '') + '">' +
        '<div class="opts">' +
          bropt('all', 'Semua') + bropt('hots', 'HOTS saja') +
        '</div>' +
        '<button class="btn ghost sm" id="bkey">' + (b.showKey ? '🙈 Sembunyikan Kunci' : '👁 Tampilkan Kunci') + '</button>' +
        '<button class="btn sm" id="bstart">▶ Latihan</button>' +
      '</div></div>';

    html += '<div class="review">' + slice.map(function (x) { return browseItem(x.q, x.i + 1, b.showKey); }).join('') + '</div>';
    if (!slice.length) html += '<div class="empty" style="margin-top:12px"><b>Tidak ada soal yang cocok</b>Coba kata kunci lain.</div>';

    html += '<div style="display:flex;gap:8px;justify-content:center;align-items:center;margin-top:16px;flex-wrap:wrap">' +
      '<button class="btn ghost sm" id="bprev"' + (b.page <= 1 ? ' disabled' : '') + '>← Sebelumnya</button>' +
      '<span style="font-size:13px;color:var(--muted);font-weight:600">Halaman ' + b.page + ' / ' + pages + '</span>' +
      '<button class="btn ghost sm" id="bnext"' + (b.page >= pages ? ' disabled' : '') + '>Selanjutnya →</button>' +
      '<button class="btn ghost sm" id="bprint">🖨 Cetak</button></div>';

    render(html);
    function bropt(v, l) { return '<button class="opt' + (b.filter === v ? ' on' : '') + '" data-f="' + v + '">' + l + '</button>'; }
    document.querySelectorAll('[data-f]').forEach(function (el) {
      el.onclick = function () { b.filter = el.dataset.f; b.page = 1; viewBrowse(); };
    });
    var si = document.getElementById('bsearch');
    si.oninput = function () { b.term = si.value; b.page = 1; clearTimeout(si._t); si._t = setTimeout(function () { viewBrowse(); var e = document.getElementById('bsearch'); if (e) { e.focus(); e.setSelectionRange(e.value.length, e.value.length); } }, 320); };
    document.getElementById('bkey').onclick = function () { b.showKey = !b.showKey; viewBrowse(); };
    document.getElementById('bstart').onclick = function () { openSetup(t.id); };
    document.getElementById('bprev').onclick = function () { b.page--; viewBrowse(); window.scrollTo({ top: 0, behavior: 'smooth' }); };
    document.getElementById('bnext').onclick = function () { b.page++; viewBrowse(); window.scrollTo({ top: 0, behavior: 'smooth' }); };
    document.getElementById('bprint').onclick = function () { b.showKey = true; viewBrowse(); setTimeout(function () { window.print(); }, 250); };
  }
  function browseItem(q, n, showKey) {
    var h = '<div class="ritem ' + (showKey ? '' : '') + '">' +
      '<div class="rh"><span class="qnum">No. ' + n + '</span>' +
      '<span class="badge ' + (q.level || 'HOTS').toLowerCase() + '">' + (LEVEL_LABEL[q.level || 'HOTS']) + '</span>' +
      (q.indicator ? '<span class="badge ind">' + esc(q.indicator) + '</span>' : '') + '</div>';
    if (q.stimulus) h += '<div class="qstim">' + (q.stimulusAr ? '<span class="arab">' + esc(q.stimulusAr) + '</span>' : '') + esc(q.stimulus) + '</div>';
    h += '<div class="qtext">' + esc(q.text) + '</div>';
    q.options.forEach(function (o, i) {
      var mark = showKey && i === q.answer ? ' ✅ <b style="color:var(--ok)">(Kunci)</b>' : '';
      h += '<div class="ans-line" style="color:' + (showKey && i === q.answer ? 'var(--ok)' : 'var(--ink-2)') + '"><b>' + LETTERS[i] + '.</b> ' + esc(o) + mark + '</div>';
    });
    if (showKey && q.explanation) h += '<div class="exp"><b style="color:var(--green-d)">💡 Pembahasan</b><br>' + esc(q.explanation) + '</div>';
    return h + '</div>';
  }

  /* ============================================================
     VIEW: PROGRES & RIWAYAT
     ============================================================ */
  function viewStats() {
    var all = topics();
    var h = store.history;
    var avg = h.length ? Math.round(h.reduce(function (a, b) { return a + b.score; }, 0) / h.length) : 0;
    var totalSoalDikerjakan = h.reduce(function (a, b) { return a + b.total; }, 0);
    var totalBenar = h.reduce(function (a, b) { return a + b.benar; }, 0);

    var html = '<div class="hero"><h2>📊 Progres &amp; Riwayat Belajar</h2>' +
      '<p>Data tersimpan otomatis di peramban perangkat ini (localStorage). Tidak ada data yang dikirim ke internet.</p>' +
      '<div class="stat-row">' +
        stat(h.length, 'Sesi Latihan') + stat(totalSoalDikerjakan, 'Soal Dikerjakan') +
        stat(totalBenar, 'Jawaban Benar') + stat(totalSoalDikerjakan ? Math.round(totalBenar / totalSoalDikerjakan * 100) : 0, 'Akurasi') +
        stat(avg, 'Rata-rata Nilai') +
      '</div></div>';

    // Penguasaan per materi
    html += '<h3 style="margin:20px 0 10px;font-size:15px;text-transform:uppercase;letter-spacing:.5px;color:var(--ink-2)">Penguasaan per Materi</h3>';
    var rows = all.map(function (t) {
      var m = store.mastery[t.id] || { c: 0, t: 0 };
      var p = progressOf(t.id);
      var pct = m.t ? Math.round(m.c / m.t * 100) : 0;
      return { t: t, m: m, pct: pct, best: p.pct, tries: p.tries };
    }).filter(function (r) { return r.m.t > 0; }).sort(function (a, b) { return a.pct - b.pct; });

    if (rows.length) {
      html += '<div style="display:flex;flex-direction:column;gap:8px;margin-bottom:22px">' + rows.map(function (r) {
        var c = r.pct >= 80 ? 'var(--ok)' : r.pct >= 60 ? 'var(--gold)' : 'var(--bad)';
        return '<div class="sheet" style="padding:12px 14px;display:flex;gap:12px;align-items:center;flex-wrap:wrap">' +
          '<div style="flex:1;min-width:190px"><b style="font-size:14px">' + esc(r.t.title) + '</b>' +
          '<div style="font-size:12px;color:var(--muted)">' + GRADE_LABEL[r.t.grade] + ' · ' + r.m.c + ' benar dari ' + r.m.t + ' soal · ' + r.tries + ' sesi</div></div>' +
          '<div class="prog" style="flex:2;min-width:130px"><i style="width:' + r.pct + '%;background:' + c + '"></i></div>' +
          '<b style="color:' + c + ';font-size:16px;min-width:44px;text-align:right">' + r.pct + '%</b>' +
          '</div>';
      }).join('') + '</div>';

      var weak = {};
      Object.keys(store.weak).forEach(function (id) {
        Object.keys(store.weak[id]).forEach(function (k) { weak[k] = (weak[k] || 0) + store.weak[id][k]; });
      });
      var wl = Object.keys(weak).map(function (k) { return { k: k, v: weak[k] }; }).sort(function (a, b) { return b.v - a.v; }).slice(0, 8);
      if (wl.length) {
        html += '<div class="sheet" style="margin-bottom:22px"><h3 style="margin-bottom:8px">🎯 Indikator yang Paling Sering Salah</h3>' +
          '<div class="meta">' + wl.map(function (w) { return '<span class="tag g" style="font-size:12px">' + esc(w.k) + ' · ' + w.v + '×</span>'; }).join('') + '</div>' +
          '<div class="hint">Fokuskan belajar pada indikator di atas, lalu ulangi latihan materinya.</div></div>';
      }
    } else {
      html += '<div class="empty"><b>Belum ada data penguasaan</b>Mulai latihan soal untuk melihat perkembanganmu di sini.</div>';
    }

    html += '<h3 style="margin:20px 0 10px;font-size:15px;text-transform:uppercase;letter-spacing:.5px;color:var(--ink-2)">Riwayat Latihan</h3>';
    if (h.length) {
      html += '<div style="overflow-x:auto"><table class="hist"><thead><tr><th>Waktu</th><th>Materi</th><th>Kelas</th><th>Mode</th><th>Benar</th><th>Waktu</th><th>Nilai</th></tr></thead><tbody>' +
        h.slice(0, 60).map(function (x) {
          var c = x.score >= 80 ? 'ok' : x.score >= 60 ? '' : 'no';
          return '<tr><td style="white-space:nowrap">' + fmtDate(x.ts) + '</td><td><b>' + esc(x.title) + '</b></td>' +
            '<td>' + GRADE_LABEL[x.grade] + '</td><td style="text-transform:capitalize">' + x.mode + '</td>' +
            '<td>' + x.benar + '/' + x.total + '</td><td>' + fmtDur(x.dur) + '</td>' +
            '<td><span class="pillsm ' + c + '" style="background:' + (c === 'ok' ? 'var(--ok-l)' : c === 'no' ? 'var(--bad-l)' : 'var(--gold-l)') + ';color:' + (c === 'ok' ? 'var(--ok)' : c === 'no' ? 'var(--bad)' : '#8a6516') + '">' + x.score + '</span></td></tr>';
        }).join('') + '</tbody></table></div>';
      html += '<div style="display:flex;gap:8px;margin-top:14px;flex-wrap:wrap">' +
        '<button class="btn ghost sm" id="expJson">⬇ Ekspor Riwayat (JSON)</button>' +
        '<button class="btn ghost sm" id="clrHist">🗑 Hapus Semua Data</button></div>';
    } else {
      html += '<div class="empty"><b>Riwayat masih kosong</b>Setiap latihan yang kamu selesaikan akan tercatat di sini.</div>';
    }

    render(html);
    var ej = document.getElementById('expJson');
    if (ej) ej.onclick = function () {
      var blob = new Blob([JSON.stringify(store, null, 2)], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'progres-bank-soal-fikih.json'; a.click();
      toast('Riwayat diunduh.');
    };
    var ch = document.getElementById('clrHist');
    if (ch) ch.onclick = function () {
      modal('<h3>Hapus semua data?</h3><p>Riwayat latihan dan statistik penguasaan akan dihapus permanen dari perangkat ini.</p>' +
        '<div class="mrow"><button class="btn ghost" data-close>Batal</button><button class="btn danger" id="doClr">Hapus</button></div>',
        function (b) { b.querySelector('#doClr').onclick = function () {
          store = { history: [], mastery: {}, weak: {} }; saveStore(); closeModal(); viewStats(); toast('Data dihapus.');
        }; });
    };
  }

  /* ============================================================
     SHELL / ROUTER
     ============================================================ */
  function render(html, keepQuiz) {
    if (!$view) $view = document.getElementById('view');
    $view.innerHTML = html;
  }
  function renderShell() {
    setTabs();
    if (S.quiz) return viewQuiz();
    if (S.setup) return viewSetup();
    if (S.tab === 'browse' && S.browse) return viewBrowse();
    if (S.tab === 'stats') return viewStats();
    S.tab = 'bank'; return viewBank();
  }
  function setTabs() {
    var t = document.getElementById('tabsBar');
    if (t) t.remove();
    if (S.quiz) return;
    var bar = document.createElement('div');
    bar.className = 'tabs'; bar.id = 'tabsBar';
    bar.innerHTML =
      tab('bank', '🗂 Bank Soal') + tab('browse', '📖 Jelajah Soal') + tab('stats', '📊 Progres');
    document.querySelector('.wrap').insertBefore(bar, document.getElementById('view'));
    bar.querySelectorAll('button').forEach(function (b) {
      b.onclick = function () {
        if (b.dataset.tab === 'browse') {
          var first = topics()[0];
          S.browse = S.browse || { id: first.id, filter: 'all', showKey: false, page: 1 };
          if (!topicById(S.browse.id)) S.browse.id = first.id;
        }
        S.tab = b.dataset.tab; S.setup = null; renderShell();
      };
    });
    function tab(id, l) { return '<button data-tab="' + id + '"' + (S.tab === id && !S.setup ? ' class="on"' : '') + '>' + l + '</button>'; }
  }

  function about() {
    var all = topics();
    modal('<h3>Tentang Aplikasi Ini</h3>' +
      '<p><b>Bank Soal Akidah Akhlak MTs</b> — aplikasi HTML standalone untuk latihan soal Akidah Akhlak kelas VII, VIII, dan IX.</p>' +
      '<p style="margin-bottom:10px">Isi: <b>' + countQ(all) + ' soal</b> pilihan ganda pada <b>' + all.length + ' materi</b>, disusun berorientasi HOTS (analisis kasus, tabel, kutipan dalil, dan penilaian sikap) mengikuti ruang lingkup kurikulum Akidah Akhlak MTs (KMA 183 Tahun 2019).</p>' +
      '<p style="margin-bottom:10px">Seluruh soal merupakan <b>karya orisinal</b> yang ditulis untuk aplikasi ini — bukan salinan dari buku atau situs tertentu — sehingga bebas digunakan, dimodifikasi, dan dibagikan untuk keperluan pembelajaran.</p>' +
      '<p style="margin-bottom:16px">Fitur: mode belajar/ujian/cepat, pengacakan soal &amp; opsi, timer, pembahasan, navigasi nomor, statistik penguasaan, riwayat tersimpan otomatis di perangkat, serta cetak/ekspor PDF.</p>' +
      '<div class="mrow"><button class="btn" data-close>Tutup</button></div>');
  }

  function bootError(msg) {
    document.getElementById('view').innerHTML = '<div class="empty" style="margin-top:30px"><b>Gagal memuat data soal</b>' + esc(msg) + '</div>';
  }

  /* ---------- Init ---------- */
  function start(missing) {
    S.missing = missing;
    loadStore();
    $view = document.getElementById('view');
    document.getElementById('btnHome').onclick = function () { if (S.quiz) exitQuiz(); else { S.tab = 'bank'; S.setup = null; renderShell(); } };
    document.getElementById('btnBack').onclick = exitQuiz;
    document.getElementById('btnStats').onclick = function () { S.tab = 'stats'; S.setup = null; renderShell(); };
    document.getElementById('btnAbout').onclick = about;
    document.getElementById('modal').addEventListener('click', function (e) { if (e.target === this) closeModal(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeModal();
      if (!S.quiz || S.quiz.finished) return;
      var tag = (e.target.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea') return;
      if (e.key === 'ArrowRight') { var n = document.getElementById('nextQ'); if (n) n.click(); else { S.quiz.cur = Math.min(S.quiz.items.length - 1, S.quiz.cur + 1); viewQuiz(); } }
      if (e.key === 'ArrowLeft') { var p = document.getElementById('prevQ'); if (p && !p.disabled) p.click(); }
      if (/^[1-5]$/.test(e.key)) {
        var b = document.querySelector('[data-pick="' + (+e.key - 1) + '"]');
        if (b && !b.disabled) b.click();
      }
    });

    var all = topics();
    document.getElementById('foot').innerHTML =
      'Bank Soal Akidah Akhlak MTs · ' + all.length + ' materi · ' + countQ(all) + ' soal pilihan ganda HOTS<br>' +
      'Soal ditulis orisinal mengikuti ruang lingkup KMA 183/2019 · Berjalan sepenuhnya offline, tanpa server &amp; tanpa pelacak.';

    renderShell();
  }

  return { start: start, bootError: bootError };
})();
