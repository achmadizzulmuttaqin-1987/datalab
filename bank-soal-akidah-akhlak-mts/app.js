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
  var TYPE_LABEL = {
    pg: 'Pilihan Ganda',
    pgk: 'PG Kompleks · 2 Jawaban Benar',
    bs: 'Benar / Salah',
    singkat: 'Jawaban Singkat',
    essay: 'Essay / Uraian'
  };
  var TYPE_SHORT = { pg: 'PG', pgk: 'PGK', bs: 'B/S', singkat: 'Singkat', essay: 'Essay' };
  /* Tipe yang dinilai otomatis. Essay disajikan dengan kunci + rubrik untuk
     penilaian mandiri sehingga tidak masuk perhitungan skor. */
  var SCORED = { pg: 1, pgk: 1, bs: 1, singkat: 1 };
  var TYPE_KEYS = ['pg', 'pgk', 'bs', 'singkat', 'essay'];

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
  /* Semua soal satu materi: pilihan ganda + 4 tipe tambahan. */
  function allQ(t) {
    if (!t) return [];
    if (t.all && t.all.length) return t.all;
    return (t.questions || []).concat(t.pgk || [], t.bs || [], t.singkat || [], t.essay || []);
  }
  function countQ(list) { return list.reduce(function (n, t) { return n + allQ(t).length; }, 0); }
  function countPg(t) { return t && t.questions ? t.questions.length : 0; }
  function countByType(list) {
    var c = { pg: 0, pgk: 0, bs: 0, singkat: 0, essay: 0 };
    list.forEach(function (t) {
      c.pg += countPg(t);
      c.pgk += (t.pgk || []).length;
      c.bs += (t.bs || []).length;
      c.singkat += (t.singkat || []).length;
      c.essay += (t.essay || []).length;
    });
    c.total = c.pg + c.pgk + c.bs + c.singkat + c.essay;
    return c;
  }
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
    var c = countByType(all);
    var done = store.history.length;
    var avg = done ? Math.round(store.history.reduce(function (a, b) { return a + b.score; }, 0) / done) : 0;
    var nTypes = TYPE_KEYS.filter(function (k) { return c[k] > 0; }).length;

    var html = '';
    html += '<div class="hero">' +
      '<h2>Bank Soal Akidah Akhlak Madrasah Tsanawiyah</h2>' +
      '<p>Kumpulan soal berorientasi <b>HOTS</b> yang disusun per materi untuk kelas VII, VIII, dan IX sesuai ruang lingkup KMA 183 Tahun 2019. ' +
      'Tersedia <b>lima tipe soal</b>: pilihan ganda, pilihan ganda kompleks (dua jawaban benar), benar/salah, jawaban singkat, dan uraian — ' +
      'seluruhnya dilengkapi kunci jawaban, pembahasan, serta rubrik penilaian untuk soal uraian.</p>' +
      '<div class="stat-row">' +
        stat(c.total, 'Total Soal') +
        stat(all.length, 'Materi / Topik') +
        stat(nTypes, 'Tipe Soal') +
        stat(done, 'Latihan Selesai') +
        stat(avg, 'Rata-rata Nilai') +
      '</div>' +
      '<div class="typerow">' +
        TYPE_KEYS.filter(function (k) { return c[k] > 0; }).map(function (k) {
          return '<button class="typechip t-' + k + '" data-gotype="' + k + '">' +
            '<b>' + c[k] + '</b><span>' + TYPE_LABEL[k] + '</span></button>';
        }).join('') +
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
    var c = countByType([t]);
    var hots = allQ(t).filter(function (q) { return q.level === 'HOTS'; }).length;
    var types = TYPE_KEYS.filter(function (k) { return typeCount(t, k) > 0; });
    var breakdown = types.map(function (k) {
      return '<span class="tag t" title="' + esc(TYPE_LABEL[k]) + '">' + TYPE_SHORT[k] + ' ' + typeCount(t, k) + '</span>';
    }).join('');
    return '<div class="card">' +
      '<div class="sem">Smt ' + t.semester + '</div>' +
      '<h3>' + esc(t.title) + '</h3>' +
      (t.desc ? '<p class="desc">' + esc(t.desc) + '</p>' : '') +
      '<div class="meta"><span class="tag">' + c.total + ' Soal</span>' +
        '<span class="tag g">' + hots + ' HOTS</span>' +
        (t.kd ? '<span class="tag b" title="' + esc(t.kd) + '">' + esc(t.kd.length > 22 ? t.kd.slice(0, 22) + '…' : t.kd) + '</span>' : '') +
      '</div>' +
      '<div class="meta tbreak">' + breakdown + '</div>' +
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
      b.onclick = function () {
        S.tab = 'browse';
        S.browse = { id: b.dataset.browse, filter: 'all', showKey: false, type: 'all' };
        renderShell();
      };
    });
    /* Chip ringkasan tipe soal: buka materi pertama yang punya tipe itu. */
    document.querySelectorAll('[data-gotype]').forEach(function (b) {
      b.onclick = function () {
        var k = b.dataset.gotype;
        var t = topics().filter(function (x) { return typeCount(x, k) > 0; })[0];
        if (!t) return toast('Tipe soal ini belum tersedia.');
        S.tab = 'browse';
        S.browse = { id: t.id, filter: 'all', showKey: false, type: k, page: 1 };
        renderShell();
      };
    });
  }

  /* ============================================================
     VIEW: SETUP LATIHAN
     ============================================================ */
  function openSetup(id) {
    var t = topicById(id); if (!t) return;
    var avail = allQ(t).length;
    S.setup = {
      id: id, n: Math.min(50, avail), mode: 'belajar',
      shuffle: true, timer: 0, level: 'all',
      types: TYPE_KEYS.filter(function (k) { return typeCount(t, k) > 0; })
    };
    viewSetup();
  }
  function typeCount(t, k) { return (k === 'pg' ? (t.questions || []) : (t[k] || [])).length; }

  function viewSetup() {
    var t = topicById(S.setup.id); if (!t) { S.tab = 'bank'; return viewBank(); }
    if (!S.setup.types || !S.setup.types.length) {
      S.setup.types = TYPE_KEYS.filter(function (k) { return typeCount(t, k) > 0; });
    }
    var pool = poolFor(t, { types: S.setup.types, level: 'all' });
    var poolH = poolFor(t, { types: S.setup.types, level: 'hots' });
    var maxN = S.setup.level === 'all' ? pool.length : poolH.length;
    if (S.setup.n > maxN) S.setup.n = maxN;
    if (maxN && S.setup.n <= 0) S.setup.n = maxN;

    /* Pemilih tipe soal: boleh memilih lebih dari satu tipe. */
    var typeChips = TYPE_KEYS.filter(function (k) { return typeCount(t, k) > 0; }).map(function (k) {
      var on = S.setup.types.indexOf(k) >= 0;
      return '<button class="opt tchip' + (on ? ' on' : '') + '" data-type="' + k + '">' +
        '<b>' + TYPE_LABEL[k] + '</b><span class="tn">' + typeCount(t, k) + ' soal</span></button>';
    }).join('');

    var html = '<div class="sheet">' +
      '<div style="display:flex;gap:8px;align-items:center;margin-bottom:6px;flex-wrap:wrap">' +
        '<span class="tag">' + GRADE_LABEL[t.grade] + '</span><span class="tag g">Semester ' + t.semester + '</span>' +
        '<span class="tag b">' + allQ(t).length + ' soal · ' + TYPE_KEYS.filter(function (k) { return typeCount(t, k) > 0; }).length + ' tipe</span>' +
        (t.kd ? '<span class="tag b">' + esc(t.kd) + '</span>' : '') +
      '</div>' +
      '<h3>' + esc(t.title) + '</h3>' +
      '<p class="sub">' + esc(t.desc || '') + '</p>' +
      '<div style="height:1px;background:var(--line);margin:0 0 16px"></div>' +

      fld('Tipe Soal <span style="text-transform:none;font-weight:600;color:var(--muted)">(boleh pilih lebih dari satu)</span>',
        '<div class="opts types">' + typeChips + '</div>' +
        '<div class="hint">PG Kompleks = centang 2 jawaban benar · Benar/Salah = nilai pernyataan · ' +
        'Jawaban Singkat = 1–4 kata, dinilai otomatis · Essay = kunci &amp; rubrik untuk penilaian mandiri.</div>') +

      fld('Mode Latihan', '<div class="opts">' +
        opt('mode', 'belajar', '📚 Belajar', 'Jawaban &amp; pembahasan langsung muncul') +
        opt('mode', 'ujian', '📝 Simulasi Ujian', 'Pembahasan di akhir, ada navigasi soal') +
        opt('mode', 'cepat', '⚡ Cepat', 'Tanpa pembahasan, hanya skor') +
      '</div>') +

      fld('Jumlah Soal <span style="text-transform:none;font-weight:600;color:var(--muted)">(tersedia ' + maxN + ')</span>',
        '<div class="opts">' +
        [10, 20, 30, 35, 40, 50].filter(function (n) { return n <= maxN; }).map(function (n) {
          return opt('n', n, n + ' Soal');
        }).join('') +
        opt('n', maxN, 'Semua (' + maxN + ')') +
      '</div>') +

      fld('Tingkat Kesulitan', '<div class="opts">' +
        opt('level', 'all', 'Semua (' + pool.length + ')') +
        opt('level', 'hots', 'HOTS saja (' + poolH.length + ')') +
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

    document.querySelectorAll('.opt[data-k]').forEach(function (b) {
      b.onclick = function () {
        var k = b.dataset.k, v = b.dataset.v;
        v = (v === 'true') ? true : (v === 'false') ? false : (isNaN(+v) ? v : +v);
        S.setup[k] = v; viewSetup();
      };
    });
    document.querySelectorAll('[data-type]').forEach(function (b) {
      b.onclick = function () {
        var k = b.dataset.type, arr = S.setup.types, at = arr.indexOf(k);
        if (at >= 0) {
          if (arr.length <= 1) return toast('Pilih minimal satu tipe soal.');
          arr.splice(at, 1);
        } else arr.push(k);
        S.setup.n = Math.min(S.setup.n, 50);
        viewSetup();
      };
    });
    document.getElementById('goQuiz').onclick = startQuiz;
    document.getElementById('goBrowse').onclick = function () { S.tab = 'browse'; S.browse = { id: t.id, filter: 'all', showKey: false, type: 'all' }; renderShell(); };
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
  /* ============================================================
     PENILAIAN PER TIPE SOAL
     pg      : 1 jawaban benar dari 4 opsi (sudah ada)
     pgk     : 2 jawaban benar dari 4 opsi — nilai penuh bila keduanya tepat
     bs      : pernyataan Benar / Salah
     singkat : isian 1-4 kata, dinilai otomatis dengan toleransi ejaan
     essay   : uraian, tidak dinilai otomatis; kunci + rubrik untuk pembanding
     ============================================================ */
  function qType(q) { return (q && q.type) || 'pg'; }
  function isScored(it) { return !!SCORED[qType(it.q)]; }

  /* Normalisasi isian singkat: huruf kecil, buang tanda baca & spasi berlebih,
     samakan beberapa varian ejaan yang lazim. */
  function normText(s) {
    return String(s == null ? '' : s)
      .toLowerCase()
      .replace(/[\u2018\u2019\u201C\u201D]/g, "'")
      .replace(/[^a-z0-9'\s-]/g, ' ')
      .replace(/['-]+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }
  function normLoose(s) {
    return normText(s)
      .replace(/\b(al|as|an|ar|at|az|ad|az|asy|ash)\b/g, 'al')   // sandang "al-"
      .replace(/(^|\s)al\s+/g, '$1al')
      .replace(/[^a-z0-9]/g, '');
  }
  function sameSet(a, b) {
    if (!a || !b || a.length !== b.length) return false;
    var x = a.slice().sort(), y = b.slice().sort();
    for (var i = 0; i < x.length; i++) if (x[i] !== y[i]) return false;
    return true;
  }
  /* Periksa isian singkat terhadap kunci dan varian yang diterima. */
  function checkShort(it, raw) {
    var q = it.q;
    var keys = [q.answer].concat(q.accepted || []);
    var n = normText(raw), l = normLoose(raw);
    for (var i = 0; i < keys.length; i++) {
      if (!keys[i]) continue;
      if (n === normText(keys[i]) || l === normLoose(keys[i])) return true;
    }
    return false;
  }

  function isAnswered(it) {
    switch (qType(it.q)) {
      case 'pgk': return (it.picks || []).length > 0;
      case 'bs': return it.pickB === true || it.pickB === false;
      case 'singkat': return !!(it.text && String(it.text).trim());
      case 'essay': return !!(it.text && String(it.text).trim());
      default: return it.pick >= 0;
    }
  }
  function isCorrect(it) {
    switch (qType(it.q)) {
      case 'pgk': return sameSet(it.picks || [], it.answers || []);
      case 'bs': return it.pickB === it.answerB;
      case 'singkat': return it.shortOk === true;
      default: return it.pick === it.answer;
    }
  }
  function keyLetters(it) {
    return (it.answers || []).map(function (i) { return LETTERS[i]; }).join(' & ');
  }
  function pickLetters(it) {
    return (it.picks || []).slice().sort().map(function (i) { return LETTERS[i]; }).join(' & ');
  }

  function startQuiz() {
    var t = topicById(S.setup.id);
    var pool = poolFor(t, S.setup);
    if (!pool.length) return toast('Tidak ada soal pada filter ini.');
    if (S.setup.shuffle) pool = shuffle(pool);
    pool = pool.slice(0, S.setup.n);

    // siapkan item; opsi diacak hanya untuk tipe berbasis opsi (pg & pgk)
    var items = pool.map(function (q, i) {
      var type = qType(q);
      var it = {
        n: i + 1, q: q, type: type, flagged: false, revealed: false,
        pick: -1, picks: [], pickB: null, text: '', shortOk: false
      };

      if (type === 'pg' || type === 'pgk') {
        var opts = q.options.map(function (txt, oi) { return { txt: txt, orig: oi }; });
        if (S.setup.shuffle) opts = shuffle(opts);
        it.opts = opts.map(function (o) { return o.txt; });
        if (type === 'pg') {
          it.answer = 0;
          opts.forEach(function (o, ni) { if (o.orig === q.answer) it.answer = ni; });
        } else {
          it.answers = [];
          opts.forEach(function (o, ni) { if ((q.answers || []).indexOf(o.orig) >= 0) it.answers.push(ni); });
          it.answers.sort(function (a, b) { return a - b; });
        }
      } else if (type === 'bs') {
        it.answerB = q.answer === true;
      }
      return it;
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

  /* Kumpulan soal satu materi sesuai filter tipe & tingkat kesulitan. */
  function poolFor(t, cfg) {
    if (!t) return [];
    var want = cfg && cfg.types && cfg.types.length ? cfg.types : TYPE_KEYS;
    var pool = [];
    TYPE_KEYS.forEach(function (k) {
      if (want.indexOf(k) < 0) return;
      var arr = k === 'pg' ? (t.questions || []) : (t[k] || []);
      arr.forEach(function (q) {
        if (!q.type) q.type = k;
        pool.push(q);
      });
    });
    if (cfg && cfg.level === 'hots') pool = pool.filter(function (q) { return q.level === 'HOTS'; });
    return pool;
  }

  function viewQuiz() {
    var Q = S.quiz; if (!Q) return;
    var it = Q.items[Q.cur];
    var answered = Q.items.filter(isAnswered).length;
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
        return '<button class="' + cellClass(x, i, Q.cur, Q.mode) + '" data-jump="' + i + '" title="' +
          (TYPE_LABEL[x.type] || '') + '">' + (i + 1) + '</button>';
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

  function typeBadge(t) {
    return '<span class="badge type t-' + t + '">' + (TYPE_SHORT[t] || t) + '</span>';
  }

  function questionHtml(it, Q) {
    var q = it.q, type = it.type;
    var locked = (Q.mode === 'belajar' && it.revealed);
    var lvl = q.level || 'HOTS';
    var h = '<div class="qhead">' +
      '<span class="qnum">No. ' + it.n + '</span>' +
      typeBadge(type) +
      '<span class="badge ' + lvl.toLowerCase() + '">' + (LEVEL_LABEL[lvl] || lvl) + '</span>' +
      (q.indicator ? '<span class="badge ind">' + esc(q.indicator) + '</span>' : '') +
    '</div>';

    if (q.stimulus) {
      var st = q.stimulus;
      if (q.stimulusAr) st = '<span class="arab">' + esc(q.stimulusAr) + '</span>' + esc(st);
      h += '<div class="qstim">' + st + '</div>';
    }
    h += '<div class="qtext">' + esc(q.text) + '</div>';

    if (type === 'pg') h += htmlPg(it, locked);
    else if (type === 'pgk') h += htmlPgk(it, locked);
    else if (type === 'bs') h += htmlBs(it, locked);
    else if (type === 'singkat') h += htmlSingkat(it, locked);
    else h += htmlEssay(it, locked);

    if (locked) h += feedbackHtml(it);

    h += '<div class="qnav">' +
      '<button class="btn ghost" id="prevQ"' + (Q.cur === 0 ? ' disabled' : '') + '>← Sebelumnya</button>' +
      '<button class="btn ghost" id="flagQ">' + (it.flagged ? '🚩 Hapus Tanda' : '🏳 Tandai Ragu') + '</button>' +
      '<span class="grow"></span>' +
      (Q.mode === 'belajar' && !it.revealed
        ? '<button class="btn" id="checkQ">' + (type === 'essay' ? 'Lihat Kunci &amp; Rubrik ✓' : 'Periksa Jawaban ✓') + '</button>'
        : '<button class="btn" id="nextQ">' + (Q.cur === Q.items.length - 1 ? 'Lihat Hasil →' : 'Selanjutnya →') + '</button>') +
    '</div>';
    return h;
  }

  /* --- Pilihan ganda: satu jawaban benar --- */
  function htmlPg(it, locked) {
    var h = '<div class="answers">';
    it.opts.forEach(function (o, i) {
      var cls = 'ans';
      if (locked) cls += i === it.answer ? ' correct' : (i === it.pick ? ' wrong' : '');
      else if (it.pick === i) cls += ' on';
      h += '<button class="' + cls + '" data-pick="' + i + '"' + (locked ? ' disabled' : '') + '>' +
        '<span class="k">' + LETTERS[i] + '</span><span class="t">' + esc(o) + '</span></button>';
    });
    return h + '</div>';
  }

  /* --- PG kompleks: tepat dua jawaban benar --- */
  function htmlPgk(it, locked) {
    var picks = it.picks || [];
    var h = '<div class="typehint">Centang <b>dua</b> jawaban yang benar · terpilih <b id="pgkCount">' + picks.length + '</b>/2</div>';
    h += '<div class="answers pgk">';
    it.opts.forEach(function (o, i) {
      var isKey = (it.answers || []).indexOf(i) >= 0;
      var chosen = picks.indexOf(i) >= 0;
      var cls = 'ans multi';
      if (locked) cls += isKey ? ' correct' : (chosen ? ' wrong' : '');
      else if (chosen) cls += ' on';
      h += '<button class="' + cls + '" data-pick="' + i + '"' + (locked ? ' disabled' : '') + '>' +
        '<span class="k box">' + (locked && isKey ? '✓' : chosen ? '✓' : '') + '</span>' +
        '<span class="let">' + LETTERS[i] + '</span><span class="t">' + esc(o) + '</span></button>';
    });
    return h + '</div>';
  }

  /* --- Benar / Salah --- */
  function htmlBs(it, locked) {
    var h = '<div class="answers bs">';
    [[true, '✓ Benar'], [false, '✕ Salah']].forEach(function (p) {
      var v = p[0], chosen = it.pickB === v, isKey = it.answerB === v;
      var cls = 'ans bsbtn';
      if (locked) cls += isKey ? ' correct' : (chosen ? ' wrong' : '');
      else if (chosen) cls += ' on';
      h += '<button class="' + cls + '" data-bs="' + v + '"' + (locked ? ' disabled' : '') + '>' +
        '<span class="t">' + p[1] + '</span></button>';
    });
    return h + '</div>';
  }

  /* --- Jawaban singkat 1-4 kata --- */
  function htmlSingkat(it, locked) {
    var h = '<div class="typehint">Jawaban singkat, <b>1–4 kata</b>. Dinilai otomatis dengan toleransi ejaan.</div>';
    h += '<input class="tinput" id="shortIn" type="text" autocomplete="off" spellcheck="false" ' +
      'placeholder="Ketik jawabanmu di sini…" value="' + esc(it.text || '') + '"' + (locked ? ' disabled' : '') + '>';
    if (locked) {
      var keys = [it.q.answer].concat(it.q.accepted || []).filter(Boolean);
      h += '<div class="keylist"><b>Jawaban diterima:</b> ' + keys.map(function (k) { return '<code>' + esc(k) + '</code>'; }).join(' ') + '</div>';
    }
    return h;
  }

  /* --- Essay: tidak dinilai otomatis, kunci + rubrik sebagai pembanding --- */
  function htmlEssay(it, locked) {
    var h = '<div class="typehint">Soal uraian. <b>Tidak dinilai otomatis</b> — tulis jawabanmu, lalu bandingkan dengan kunci dan rubrik.</div>';
    h += '<textarea class="tarea" id="essayIn" rows="6" placeholder="Tulis jawaban uraianmu di sini…"' +
      (locked ? ' disabled' : '') + '>' + esc(it.text || '') + '</textarea>';
    if (locked) {
      if (it.q.key) h += '<div class="keybox"><b>🔑 Kunci Jawaban</b><div>' + esc(it.q.key) + '</div></div>';
      if (it.q.rubric && it.q.rubric.length) {
        h += '<div class="rubric"><b>📋 Rubrik Penilaian</b><ol>' +
          it.q.rubric.map(function (r) { return '<li>' + esc(r) + '</li>'; }).join('') + '</ol></div>';
      }
    }
    return h;
  }

  /* --- Umpan balik setelah diperiksa --- */
  function feedbackHtml(it) {
    var type = it.type, q = it.q;
    if (type === 'essay') {
      return '<div class="fb info"><b>📝 Bandingkan jawabanmu dengan kunci di atas.</b>' +
        'Gunakan rubrik untuk menilai sendiri berapa poin yang kamu peroleh.</div>' +
        expBlock(q);
    }
    var ok = isCorrect(it), h;
    if (type === 'pgk') {
      h = '<div class="fb ' + (ok ? 'ok' : 'no') + '"><b>' + (ok ? '✓ Tepat! Kedua jawaban benar.' : '✕ Belum tepat.') + '</b>' +
        'Kunci: <b>' + keyLetters(it) + '</b>' +
        (ok ? '' : ' · Jawabanmu: <b>' + (pickLetters(it) || '—') + '</b>') + '</div>';
    } else if (type === 'bs') {
      h = '<div class="fb ' + (ok ? 'ok' : 'no') + '"><b>' + (ok ? '✓ Jawaban benar!' : '✕ Jawaban kurang tepat.') + '</b>' +
        'Kunci: <b>' + (it.answerB ? 'Benar' : 'Salah') + '</b>' +
        (ok ? '' : ' · Jawabanmu: <b>' + (it.pickB === null ? '—' : it.pickB ? 'Benar' : 'Salah') + '</b>') + '</div>';
    } else if (type === 'singkat') {
      h = '<div class="fb ' + (ok ? 'ok' : 'no') + '"><b>' + (ok ? '✓ Jawaban benar!' : '✕ Jawaban kurang tepat.') + '</b>' +
        'Kunci: <b>' + esc(q.answer) + '</b>' +
        (ok ? '' : ' · Jawabanmu: <b>' + esc(it.text || '—') + '</b>') + '</div>';
    } else {
      h = '<div class="fb ' + (ok ? 'ok' : 'no') + '"><b>' + (ok ? '✓ Jawaban benar!' : '✕ Jawaban kurang tepat.') + '</b>' +
        (ok ? '' : 'Kunci jawaban: <b>' + LETTERS[it.answer] + '. ' + esc(it.opts[it.answer]) + '</b>') + '</div>';
    }
    return h + expBlock(q);
  }
  function expBlock(q) {
    return q.explanation
      ? '<div class="exp"><b style="color:var(--green-d)">💡 Pembahasan</b><br>' + esc(q.explanation) + '</div>'
      : '';
  }

  function bindQuiz(it, Q) {
    /* Pilihan ganda: satu jawaban benar */
    if (it.type === 'pg') {
      document.querySelectorAll('[data-pick]').forEach(function (b) {
        b.onclick = function () {
          it.pick = +b.dataset.pick;
          if (Q.mode !== 'belajar') renderQuizOnly(); else viewQuiz();
        };
      });
    }

    /* PG kompleks: tepat dua jawaban benar, klik untuk mencentang / melepas */
    if (it.type === 'pgk') {
      document.querySelectorAll('[data-pick]').forEach(function (b) {
        b.onclick = function () {
          var i = +b.dataset.pick;
          it.picks = it.picks || [];
          var at = it.picks.indexOf(i);
          if (at >= 0) it.picks.splice(at, 1);
          else {
            if (it.picks.length >= 2) return toast('Hanya dua jawaban yang boleh dicentang. Lepaskan satu centang terlebih dahulu.');
            it.picks.push(i);
          }
          if (Q.mode !== 'belajar') renderQuizOnly(); else viewQuiz();
        };
      });
    }

    /* Benar / Salah */
    document.querySelectorAll('[data-bs]').forEach(function (b) {
      b.onclick = function () {
        it.pickB = (b.dataset.bs === 'true');
        if (Q.mode !== 'belajar') renderQuizOnly(); else viewQuiz();
      };
    });

    /* Isian singkat & uraian: simpan ke state tanpa merender ulang
       agar kursor dan fokus tidak hilang saat mengetik. */
    var si = document.getElementById('shortIn');
    if (si) {
      si.oninput = function () { it.text = si.value; };
      si.onkeydown = function (e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          var c = document.getElementById('checkQ'); if (c) c.click();
        }
      };
    }
    var ei = document.getElementById('essayIn');
    if (ei) ei.oninput = function () { it.text = ei.value; };

    var j = document.querySelectorAll('[data-jump]');
    j.forEach(function (b) { b.onclick = function () { Q.cur = +b.dataset.jump; viewQuiz(); }; });
    var p = document.getElementById('prevQ'); if (p) p.onclick = function () { if (Q.cur > 0) { Q.cur--; viewQuiz(); } };
    var n = document.getElementById('nextQ'); if (n) n.onclick = function () {
      if (Q.cur < Q.items.length - 1) { Q.cur++; viewQuiz(); } else confirmFinish();
    };
    var c = document.getElementById('checkQ'); if (c) c.onclick = function () {
      var msg = needAnswerMsg(it);
      if (msg) return toast(msg);
      if (it.type === 'singkat') it.shortOk = checkShort(it, it.text);
      it.revealed = true;
      recordAnswer(Q, it);
      viewQuiz();
    };
    var f = document.getElementById('flagQ'); if (f) f.onclick = function () { it.flagged = !it.flagged; renderQuizOnly(); };
    document.getElementById('btnFinish').onclick = confirmFinish;
  }

  /* Pesan bila soal belum dijawab; null berarti sudah terisi. */
  function needAnswerMsg(it) {
    switch (it.type) {
      case 'pgk':
        if ((it.picks || []).length === 0) return 'Centang dua jawaban terlebih dahulu.';
        if ((it.picks || []).length < 2) return 'Masih satu centang. Soal ini meminta dua jawaban benar.';
        return null;
      case 'bs':
        return (it.pickB === true || it.pickB === false) ? null : 'Pilih Benar atau Salah terlebih dahulu.';
      case 'singkat':
        return (it.text && it.text.trim()) ? null : 'Tulis jawabanmu terlebih dahulu.';
      case 'essay':
        return (it.text && it.text.trim()) ? null : 'Tulis jawaban uraianmu terlebih dahulu.';
      default:
        return it.pick >= 0 ? null : 'Pilih salah satu jawaban terlebih dahulu.';
    }
  }

  function cellClass(x, i, cur, mode) {
    var c = 'pcell';
    if (mode === 'belajar' && x.revealed) {
      if (x.type === 'essay') c += ' ess';
      else c += isCorrect(x) ? ' right' : ' wr';
    } else if (isAnswered(x)) c += ' ans-d';
    if (i === cur) c += ' cur';
    if (x.flagged) c += ' flag';
    return c;
  }

  function renderQuizOnly() {
    var Q = S.quiz;
    var card = document.getElementById('qcard');
    if (card) {
      card.innerHTML = questionHtml(Q.items[Q.cur], Q);
      bindQuiz(Q.items[Q.cur], Q);
    }
    document.querySelectorAll('[data-jump]').forEach(function (b, i) {
      b.className = cellClass(Q.items[i], i, Q.cur, Q.mode);
    });
  }

  function recordAnswer(Q, it) {
    var id = Q.topic.id;
    var m = store.mastery[id] || (store.mastery[id] = { c: 0, t: 0 });
    if (isScored(it)) {
      m.t++;
      if (isCorrect(it)) m.c++;
      else {
        var w = store.weak[id] || (store.weak[id] = {});
        var key = it.q.indicator || 'umum';
        w[key] = (w[key] || 0) + 1;
      }
    }
    saveStore();
  }

  function confirmFinish() {
    var Q = S.quiz;
    var un = Q.items.filter(function (x) { return !isAnswered(x); }).length;
    var wrong = Q.items.filter(function (x) {
      return Q.mode === 'belajar' && isScored(x) && isAnswered(x) && !isCorrect(x);
    }).length;
    var nEssay = Q.items.filter(function (x) { return x.type === 'essay'; }).length;
    modal('<h3>Selesaikan latihan?</h3>' +
      '<p>' + (un ? 'Masih ada <b>' + un + ' soal belum dijawab</b>. ' : '') +
      (Q.mode === 'belajar' && wrong ? 'Sudah ada <b>' + wrong + ' jawaban salah</b>. ' : '') +
      'Soal yang belum dijawab akan dihitung salah dalam penilaian.' +
      (nEssay ? '<br><span style="font-size:13px;color:var(--muted)">' + nEssay +
        ' soal uraian tidak dinilai otomatis — kunci dan rubriknya ditampilkan untuk penilaian mandiri.</span>' : '') +
      '</p>' +
      '<div class="mrow"><button class="btn ghost" data-close>Batal</button>' +
      '<button class="btn danger" id="doFinish">Ya, Nilai Sekarang</button></div>',
      function (b) { b.querySelector('#doFinish').onclick = function () { closeModal(); finish(false); }; });
  }

  function finish(auto) {
    var Q = S.quiz; if (!Q || Q.finished) return;
    Q.finished = true;
    if (Q.timerId) clearInterval(Q.timerId);
    var secs = (Date.now() - Q.t0) / 1000;

    /* Nilai otomatis hanya untuk tipe yang dapat dinilai; uraian disajikan
       beserta kunci dan rubrik untuk penilaian mandiri. */
    var scored = Q.items.filter(isScored);
    var essays = Q.items.filter(function (x) { return !isScored(x); });
    var benar = 0;
    Q.items.forEach(function (it) {
      if (Q.mode !== 'belajar' && !it.revealed) it.revealed = true;
      if (it.type === 'singkat' && !it.revealed) it.shortOk = checkShort(it, it.text);
      if (isScored(it) && isCorrect(it)) benar++;
    });
    var denom = scored.length || 1;
    var score = scored.length ? Math.round(benar / denom * 100) : 0;
    Q.result = {
      benar: benar, salah: scored.length - benar, score: score, secs: secs, auto: auto,
      total: scored.length, essay: essays.length
    };

    store.history.unshift({
      id: Q.topic.id, title: Q.topic.title, grade: Q.topic.grade,
      score: score, benar: benar, total: scored.length, essay: essays.length,
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
        '<div class="res-cell mut"><b>' + R.total + '</b><span>Soal Dinilai</span></div>' +
        (R.essay ? '<div class="res-cell mut"><b>' + R.essay + '</b><span>Uraian (mandiri)</span></div>' : '') +
        '<div class="res-cell mut"><b>' + fmtDur(R.secs) + '</b><span>Waktu</span></div>' +
        '<div class="res-cell mut"><b>' + p.pct + '</b><span>Nilai Terbaik</span></div>' +
      '</div>' +
      (R.essay ? '<div class="hint" style="max-width:520px;margin:12px auto 0">Nilai di atas dihitung dari ' + R.total +
        ' soal yang dapat dinilai otomatis. ' + R.essay + ' soal uraian dinilai mandiri dengan membandingkan jawabanmu terhadap kunci dan rubrik.</div>' : '') +
      '<div style="display:flex;gap:9px;justify-content:center;margin-top:20px;flex-wrap:wrap">' +
        '<button class="btn" id="rReview">🔍 Bahas Jawaban</button>' +
        '<button class="btn ghost" id="rRetry">↻ Ulangi Latihan</button>' +
        '<button class="btn ghost" id="rWrong">✕ Bahas yang Salah Saja</button>' +
        '<button class="btn ghost" id="rEssay">📝 Kunci Uraian</button>' +
        '<button class="btn ghost" id="rPrint">🖨 Cetak / PDF</button>' +
        '<button class="btn ghost" id="rHome">🏠 Beranda</button>' +
      '</div></div>' +
      '<div id="reviewBox"></div>';
    render(html, true);
    document.getElementById('rReview').onclick = function () { showReview(Q, 'all'); };
    document.getElementById('rWrong').onclick = function () { showReview(Q, 'wrong'); };
    document.getElementById('rEssay').onclick = function () { showReview(Q, 'essay'); };
    document.getElementById('rRetry').onclick = function () {
      var cfg = {
        id: Q.topic.id, n: Q.items.length, mode: Q.mode, shuffle: true,
        timer: Q.limit / 60 | 0, level: S.setup ? S.setup.level : 'all',
        types: S.setup ? S.setup.types : TYPE_KEYS.slice()
      };
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
    var items = Q.items.filter(function (it) {
      if (filter === 'all') return true;
      if (filter === 'wrong') return isScored(it) && !isCorrect(it);
      if (filter === 'essay') return it.type === 'essay';
      return true;
    });
    var label = filter === 'all' ? 'Seluruh Soal' : filter === 'wrong' ? 'Soal yang Salah' : 'Soal Uraian + Kunci';
    box.innerHTML = '<div class="review">' +
      '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">' +
        '<h3 style="margin:0;font-size:16px">Pembahasan ' + label + ' (' + items.length + ')</h3>' +
        '<button class="btn ghost sm" id="closeRev">Tutup</button></div>' +
      (items.length ? items.map(reviewItem).join('') : '<div class="empty" style="margin-top:10px"><b>Tidak ada soal pada saringan ini</b></div>') +
      '</div>';
    document.getElementById('closeRev').onclick = function () { box.innerHTML = ''; };
    box.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  function reviewItem(it) {
    var type = it.type || 'pg', q = it.q;
    var scored = isScored(it);
    var ok = scored ? isCorrect(it) : false;
    var answered = isAnswered(it);
    var cls = type === 'essay' ? 'ess' : (!answered ? 'sk' : ok ? 'ok' : 'no');
    var pill = type === 'essay' ? 'Nilai mandiri' : (!answered ? 'Tidak dijawab' : ok ? 'Benar' : 'Salah');
    var pillCls = type === 'essay' ? 'mut' : (!answered || !ok ? 'no' : 'ok');

    var h = '<div class="ritem ' + cls + '">' +
      '<div class="rh"><span class="qnum">No. ' + it.n + '</span>' +
      typeBadge(type) +
      '<span class="badge ' + (q.level || 'HOTS').toLowerCase() + '">' + (LEVEL_LABEL[q.level || 'HOTS']) + '</span>' +
      (q.indicator ? '<span class="badge ind">' + esc(q.indicator) + '</span>' : '') +
      '<span class="pillsm ' + pillCls + '">' + pill + '</span></div>';

    if (q.stimulus) h += '<div class="qstim">' + (q.stimulusAr ? '<span class="arab">' + esc(q.stimulusAr) + '</span>' : '') + esc(q.stimulus) + '</div>';
    h += '<div class="qtext">' + esc(q.text) + '</div>';

    if (type === 'pg' || type === 'pgk') {
      var keys = type === 'pgk' ? (it.answers || []) : [it.answer];
      it.opts.forEach(function (o, i) {
        var isKey = keys.indexOf(i) >= 0;
        var chosen = type === 'pgk' ? (it.picks || []).indexOf(i) >= 0 : it.pick === i;
        var mark = isKey ? ' ✅' : (chosen ? ' ❌' : '');
        h += '<div class="ans-line" style="color:' + (isKey ? 'var(--ok)' : chosen ? 'var(--bad)' : 'var(--ink-2)') + '">' +
          '<b>' + LETTERS[i] + '.</b> ' + esc(o) + mark + '</div>';
      });
      if (type === 'pgk') {
        h += '<div class="ans-line" style="margin-top:6px;color:' + (ok ? 'var(--ok)' : 'var(--bad)') + '">Kunci: <b>' +
          keyLetters(it) + '</b> · Centangmu: <b>' + (pickLetters(it) || '—') + '</b></div>';
      } else if (answered && !ok) {
        h += '<div class="ans-line" style="margin-top:6px;color:var(--bad)">Jawabanmu: <b>' +
          LETTERS[it.pick] + '</b> · Kunci: <b>' + LETTERS[it.answer] + '</b></div>';
      }
    } else if (type === 'bs') {
      h += '<div class="ans-line" style="color:' + (ok ? 'var(--ok)' : 'var(--bad)') + '">Kunci: <b>' +
        (it.answerB ? 'Benar ✅' : 'Salah ✅') + '</b> · Jawabanmu: <b>' +
        (it.pickB === null || it.pickB === undefined ? '—' : it.pickB ? 'Benar' : 'Salah') + '</b></div>';
    } else if (type === 'singkat') {
      var keys2 = [q.answer].concat(q.accepted || []).filter(Boolean);
      h += '<div class="ans-line" style="color:' + (ok ? 'var(--ok)' : 'var(--bad)') + '">Jawabanmu: <b>' +
        esc((it.text || '').trim() || '—') + '</b></div>' +
        '<div class="ans-line" style="color:var(--ok)">Kunci: <b>' + esc(q.answer) + '</b>' +
        (keys2.length > 1 ? ' · Varian diterima: ' + keys2.slice(1).map(function (k) { return '<code>' + esc(k) + '</code>'; }).join(' ') : '') + '</div>';
    } else {
      if ((it.text || '').trim()) {
        h += '<div class="keybox"><b>✍️ Jawabanmu</b><div>' + esc(it.text) + '</div></div>';
      } else {
        h += '<div class="ans-line" style="color:var(--muted)">Jawabanmu: <b>—</b> (tidak diisi)</div>';
      }
      if (q.key) h += '<div class="keybox"><b>🔑 Kunci Jawaban</b><div>' + esc(q.key) + '</div></div>';
      if (q.rubric && q.rubric.length) {
        h += '<div class="rubric"><b>📋 Rubrik Penilaian</b><ol>' +
          q.rubric.map(function (r) { return '<li>' + esc(r) + '</li>'; }).join('') + '</ol></div>';
      }
    }

    h += expBlock(q);
    return h + '</div>';
  }

  function exitQuiz() {
    if (S.quiz && !S.quiz.finished && S.quiz.items.some(isAnswered)) {
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
  /* Gabungan teks satu soal untuk pencarian, mencakup seluruh tipe. */
  function qBlob(q) {
    var parts = [q.text || '', q.stimulus || '', q.explanation || '', q.indicator || ''];
    if (q.options) parts.push(q.options.join(' '));
    if (q.key) parts.push(q.key);
    if (q.rubric) parts.push(q.rubric.join(' '));
    if (q.answer != null && typeof q.answer !== 'boolean') parts.push(String(q.answer));
    if (q.accepted) parts.push(q.accepted.join(' '));
    return parts.join(' ').toLowerCase();
  }

  function viewBrowse() {
    var b = S.browse;
    var t = topicById(b.id);
    if (!t) { S.tab = 'bank'; return viewBank(); }
    if (!b.type) b.type = 'all';

    var qs = allQ(t).map(function (q, i) { return { q: q, i: i }; });
    var f = b.filter;
    if (f === 'hots') qs = qs.filter(function (x) { return x.q.level === 'HOTS'; });
    if (f === 'unseen') {
      var m = store.mastery[t.id];
      qs = qs.filter(function () { return !m; });
    }
    if (b.type !== 'all') qs = qs.filter(function (x) { return qType(x.q) === b.type; });

    var term = (b.term || '').toLowerCase().trim();
    if (term) qs = qs.filter(function (x) { return qBlob(x.q).indexOf(term) >= 0; });

    var perPage = 20, pages = Math.max(1, Math.ceil(qs.length / perPage));
    b.page = Math.min(b.page || 1, pages);
    var slice = qs.slice((b.page - 1) * perPage, b.page * perPage);
    var c = countByType([t]);

    var html = '<div class="sheet" style="margin-bottom:14px">' +
      '<div style="display:flex;gap:8px;align-items:center;margin-bottom:6px;flex-wrap:wrap">' +
        '<span class="tag">' + GRADE_LABEL[t.grade] + '</span><span class="tag g">Semester ' + t.semester + '</span>' +
        '<span class="tag b">' + c.total + ' soal</span>' +
        '<span class="tag">' + c.pg + ' PG</span><span class="tag">' + c.pgk + ' PGK</span>' +
        '<span class="tag">' + c.bs + ' B/S</span><span class="tag">' + c.singkat + ' Singkat</span>' +
        '<span class="tag">' + c.essay + ' Essay</span></div>' +
      '<h3 style="margin-bottom:2px">📖 ' + esc(t.title) + '</h3>' +
      '<p class="sub" style="margin-bottom:12px">' + esc(t.desc || '') + '</p>' +
      '<div class="filters">' +
        '<input class="search" id="bsearch" placeholder="Cari kata kunci soal / pembahasan…" value="' + esc(b.term || '') + '">' +
        '<div class="opts">' +
          bropt('all', 'Semua') + bropt('hots', 'HOTS saja') +
        '</div>' +
        '<div class="opts">' + btype('all', 'Semua Tipe', c.total) +
          TYPE_KEYS.filter(function (k) { return typeCount(t, k) > 0; })
            .map(function (k) { return btype(k, TYPE_SHORT[k], typeCount(t, k)); }).join('') +
        '</div>' +
        '<button class="btn ghost sm" id="bkey">' + (b.showKey ? '🙈 Sembunyikan Kunci' : '👁 Tampilkan Kunci') + '</button>' +
        '<button class="btn sm" id="bstart">▶ Latihan</button>' +
      '</div></div>';

    html += '<div class="review">' + slice.map(function (x) { return browseItem(x.q, x.i + 1, b.showKey); }).join('') + '</div>';
    if (!slice.length) html += '<div class="empty" style="margin-top:12px"><b>Tidak ada soal yang cocok</b>Coba kata kunci atau tipe lain.</div>';

    html += '<div style="display:flex;gap:8px;justify-content:center;align-items:center;margin-top:16px;flex-wrap:wrap">' +
      '<button class="btn ghost sm" id="bprev"' + (b.page <= 1 ? ' disabled' : '') + '>← Sebelumnya</button>' +
      '<span style="font-size:13px;color:var(--muted);font-weight:600">Halaman ' + b.page + ' / ' + pages + '</span>' +
      '<button class="btn ghost sm" id="bnext"' + (b.page >= pages ? ' disabled' : '') + '>Selanjutnya →</button>' +
      '<button class="btn ghost sm" id="bprint">🖨 Cetak</button></div>';

    render(html);
    function bropt(v, l) { return '<button class="opt' + (b.filter === v ? ' on' : '') + '" data-f="' + v + '">' + l + '</button>'; }
    function btype(v, l, n) {
      return '<button class="opt' + (b.type === v ? ' on' : '') + '" data-t="' + v + '">' + l +
        ' <span style="opacity:.7;font-weight:600">' + n + '</span></button>';
    }
    document.querySelectorAll('[data-f]').forEach(function (el) {
      el.onclick = function () { b.filter = el.dataset.f; b.page = 1; viewBrowse(); };
    });
    document.querySelectorAll('[data-t]').forEach(function (el) {
      el.onclick = function () { b.type = el.dataset.t; b.page = 1; viewBrowse(); };
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
    var type = qType(q);
    var h = '<div class="ritem">' +
      '<div class="rh"><span class="qnum">No. ' + n + '</span>' +
      typeBadge(type) +
      '<span class="badge ' + (q.level || 'HOTS').toLowerCase() + '">' + (LEVEL_LABEL[q.level || 'HOTS']) + '</span>' +
      (q.indicator ? '<span class="badge ind">' + esc(q.indicator) + '</span>' : '') + '</div>';
    if (q.stimulus) h += '<div class="qstim">' + (q.stimulusAr ? '<span class="arab">' + esc(q.stimulusAr) + '</span>' : '') + esc(q.stimulus) + '</div>';
    h += '<div class="qtext">' + esc(q.text) + '</div>';

    if (type === 'pg') {
      q.options.forEach(function (o, i) {
        var isKey = showKey && i === q.answer;
        h += '<div class="ans-line" style="color:' + (isKey ? 'var(--ok)' : 'var(--ink-2)') + '"><b>' + LETTERS[i] + '.</b> ' + esc(o) +
          (isKey ? ' ✅ <b>(Kunci)</b>' : '') + '</div>';
      });
    } else if (type === 'pgk') {
      var keys = q.answers || [];
      h += '<div class="typehint">Pilihan ganda kompleks — <b>dua</b> jawaban benar.</div>';
      q.options.forEach(function (o, i) {
        var isKey = showKey && keys.indexOf(i) >= 0;
        h += '<div class="ans-line" style="color:' + (isKey ? 'var(--ok)' : 'var(--ink-2)') + '"><b>' + LETTERS[i] + '.</b> ' + esc(o) +
          (isKey ? ' ✅ <b>(Kunci)</b>' : '') + '</div>';
      });
      if (showKey) h += '<div class="ans-line" style="color:var(--ok);margin-top:5px">Kunci: <b>' +
        keys.map(function (i) { return LETTERS[i]; }).join(' &amp; ') + '</b></div>';
    } else if (type === 'bs') {
      h += '<div class="ans-line" style="color:var(--ink-2)"><b>Pernyataan di atas:</b> Benar / Salah</div>';
      if (showKey) h += '<div class="ans-line" style="color:var(--ok);margin-top:5px">Kunci: <b>' +
        (q.answer === true ? 'Benar ✅' : 'Salah ✅') + '</b></div>';
    } else if (type === 'singkat') {
      h += '<div class="ans-line" style="color:var(--ink-2)"><b>Jawaban singkat</b> (1–4 kata)</div>';
      if (showKey) {
        var variants = (q.accepted || []).filter(Boolean);
        h += '<div class="ans-line" style="color:var(--ok);margin-top:5px">Kunci: <b>' + esc(q.answer) + '</b>' +
          (variants.length ? ' · Varian diterima: ' + variants.map(function (k) { return '<code>' + esc(k) + '</code>'; }).join(' ') : '') + '</div>';
      }
    } else {
      h += '<div class="ans-line" style="color:var(--ink-2)"><b>Soal uraian</b> — jawab dengan kalimat lengkap</div>';
      if (showKey) {
        if (q.key) h += '<div class="keybox"><b>🔑 Kunci Jawaban</b><div>' + esc(q.key) + '</div></div>';
        if (q.rubric && q.rubric.length) {
          h += '<div class="rubric"><b>📋 Rubrik Penilaian</b><ol>' +
            q.rubric.map(function (r) { return '<li>' + esc(r) + '</li>'; }).join('') + '</ol></div>';
        }
      }
    }

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
    var c = countByType(all);
    modal('<h3>Tentang Aplikasi Ini</h3>' +
      '<p><b>Bank Soal Akidah Akhlak MTs</b> — aplikasi HTML standalone untuk latihan soal Akidah Akhlak kelas VII, VIII, dan IX.</p>' +
      '<p style="margin-bottom:10px">Isi: <b>' + c.total + ' soal</b> pada <b>' + all.length + ' materi</b>, disusun berorientasi HOTS (analisis kasus, tabel, kutipan dalil, dan penilaian sikap) mengikuti ruang lingkup kurikulum Akidah Akhlak MTs (KMA 183 Tahun 2019).</p>' +
      '<div class="typelist">' +
        TYPE_KEYS.filter(function (k) { return c[k] > 0; }).map(function (k) {
          return '<div class="typerow-i"><span class="badge type t-' + k + '">' + TYPE_SHORT[k] + '</span>' +
            '<b>' + TYPE_LABEL[k] + '</b><span class="tn">' + c[k] + ' soal</span></div>';
        }).join('') +
      '</div>' +
      '<p style="margin:10px 0">Setiap soal dilengkapi kunci jawaban dan pembahasan. Soal uraian disertai <b>kunci jawaban dan rubrik penilaian</b> untuk penilaian mandiri karena tidak dinilai otomatis.</p>' +
      '<p style="margin-bottom:10px">Seluruh soal merupakan <b>karya orisinal</b> yang ditulis untuk aplikasi ini — bukan salinan dari buku atau situs tertentu — sehingga bebas digunakan, dimodifikasi, dan dibagikan untuk keperluan pembelajaran.</p>' +
      '<p style="margin-bottom:16px">Fitur: mode belajar/ujian/cepat, pemilih tipe soal, pengacakan soal &amp; opsi, timer, pembahasan, navigasi nomor, statistik penguasaan, riwayat tersimpan otomatis di perangkat, serta cetak/ekspor PDF.</p>' +
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
    var c = countByType(all);
    document.getElementById('foot').innerHTML =
      'Bank Soal Akidah Akhlak MTs · ' + all.length + ' materi · ' + c.total + ' soal HOTS dalam ' +
      TYPE_KEYS.filter(function (k) { return c[k] > 0; }).length + ' tipe<br>' +
      TYPE_KEYS.filter(function (k) { return c[k] > 0; }).map(function (k) {
        return TYPE_SHORT[k] + ' ' + c[k];
      }).join(' · ') + '<br>' +
      'Soal ditulis orisinal mengikuti ruang lingkup KMA 183/2019 · Berjalan sepenuhnya offline, tanpa server &amp; tanpa pelacak.';

    renderShell();
  }

  return { start: start, bootError: bootError };
})();
