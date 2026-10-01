/* Aplikasi Latihan AKG Akidah Akhlak MTs - logika antarmuka (vanilla JS) */
(function () {
  'use strict';
  var DATA = window.__AKG_DATA__ || { meta: {}, soal: [], kisi: {}, rangkuman: {} };
  var SOAL = DATA.soal || [];
  var LETTERS = ['A', 'B', 'C', 'D', 'E'];
  var LS_KEY = 'akg-akidah-akhlak-mts-v1';
  var STORE = { picked: {}, ok: {}, ts: 0 };
  try {
    var raw = localStorage.getItem(LS_KEY);
    if (raw) { var p = JSON.parse(raw); if (p && p.picked) { STORE = p; } }
  } catch (e) { /* localStorage tidak tersedia, lanjut tanpa simpan */ }
  function save() { STORE.ts = Date.now(); try { localStorage.setItem(LS_KEY, JSON.stringify(STORE)); } catch (e) {} }

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (txt != null) { e.textContent = txt; } return e; }
  function letter(i) { return LETTERS[i] || '?'; }
  function catName(k) { return k === 'pedagogik' ? 'Pedagogik' : 'Profesional'; }
  function kunciText(it) {
    if (it.tipe === 'pg') { return letter(it.kunci); }
    return it.kunci.map(letter).join(' dan ');
  }
  function isCorrect(it, picked) {
    if (!picked || !picked.length) { return false; }
    if (it.tipe === 'pg') { return picked.length === 1 && picked[0] === it.kunci; }
    var k = it.kunci.slice().sort().join(',');
    var q = picked.slice().sort().join(',');
    return k === q;
  }
  function topikList(kat) {
    var seen = {}, out = [];
    SOAL.forEach(function (it) {
      if (kat && kat !== 'semua' && it.kategori !== kat) { return; }
      if (!seen[it.topik]) { seen[it.topik] = 1; out.push(it.topik); }
    });
    return out;
  }
  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  /* ---------------- Tab ---------------- */
  var TABS = ['petunjuk', 'kisi', 'materi', 'latihan', 'kunci'];
  function showTab(name) {
    TABS.forEach(function (t) {
      var sec = document.getElementById('tab-' + t);
      var btn = document.getElementById('btn-tab-' + t);
      if (!sec || !btn) { return; }
      var on = t === name;
      sec.hidden = !on;
      btn.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  /* ---------------- Kisi-kisi ---------------- */
  function renderKisi() {
    var box = $('#kisi-body');
    if (!box) { return; }
    var k = DATA.kisi || {};
    var wrap = el('div');
    wrap.appendChild(el('p', 'lead', k.catatan || ''));
    var t = el('table');
    var thead = el('thead'); var tr = el('tr');
    ['Jenjang', 'Pedagogik', 'Profesional', 'Jumlah', 'Waktu', 'Keterangan'].forEach(function (h) { tr.appendChild(el('th', null, h)); });
    thead.appendChild(tr); t.appendChild(thead);
    var tb = el('tbody');
    (k.komposisi || []).forEach(function (r) {
      var row = el('tr');
      [r.jenjang, r.pedagogik, r.profesional, r.total, r.waktu, r.keterangan].forEach(function (v) { row.appendChild(el('td', null, String(v))); });
      tb.appendChild(row);
    });
    t.appendChild(tb); wrap.appendChild(t); wrap.appendChild(el('h3', null, 'Aspek kompetensi pedagogik yang diuji'));
    var ul = el('ul', 'clean');
    (k.aspekPedagogik || []).forEach(function (x) { ul.appendChild(el('li', null, x)); });
    wrap.appendChild(ul); wrap.appendChild(el('h3', null, 'Aspek kompetensi profesional Akidah Akhlak'));
    var ul2 = el('ul', 'clean');
    (k.aspekProfesional || []).forEach(function (x) { ul2.appendChild(el('li', null, x)); });
    wrap.appendChild(ul2); wrap.appendChild(el('h3', null, 'Lingkup materi'));
    var grid = el('div', 'grid c2');
    (k.lingkupMateri || []).forEach(function (m) {
      var c = el('div', 'card');
      c.appendChild(el('h4', null, m.nama));
      c.appendChild(el('p', 'small muted', m.poin));
      grid.appendChild(c);
    });
    wrap.appendChild(grid); wrap.appendChild(el('h3', null, 'Tips belajar'));
    var ul3 = el('ul', 'clean');
    (k.tipsBelajar || []).forEach(function (x) { ul3.appendChild(el('li', null, x)); });
    wrap.appendChild(ul3);
    box.appendChild(wrap);
  }

  /* ---------------- Materi ---------------- */
  function renderMateri() {
    var box = $('#materi-body');
    if (!box) { return; }
    var r = DATA.rangkuman || {};
    box.appendChild(el('p', 'lead', 'Ringkasan padat sebagai bekal mengerjakan soal. Klik judul untuk membuka atau menutup.'));
    (r.seksi || []).forEach(function (s, i) {
      var d = el('details', 'acc'); if (i === 0) { d.open = true; }
      d.appendChild(el('summary', null, s.judul));
      var b = el('div', 'body');
      var ul = el('ul', 'clean');
      s.poin.forEach(function (p) { ul.appendChild(el('li', null, p)); });
      b.appendChild(ul); d.appendChild(b); box.appendChild(d);
    });
    var btn = el('button', 'btn ghost', '🖨 Cetak / Simpan PDF');
    btn.onclick = function () {
      document.querySelectorAll('#materi-body details, #kunci-body details').forEach(function (d) { d.open = true; });
      window.print();
    };
    var row = el('div', 'btnrow'); row.appendChild(btn); box.appendChild(row);
  }

  /* ---------------- Kunci jawaban ---------------- */
  function renderKunci() {
    var box = $('#kunci-body');
    if (!box) { return; }
    box.appendChild(el('p', 'lead', 'Seluruh ' + SOAL.length + ' soal beserta kunci dan pembahasan. Gunakan kolom pencarian untuk menyaring topik atau soal tertentu.'));
    var row = el('div', 'quizbar');
    var lab = el('label', 'field'); lab.appendChild(document.createTextNode('Cari soal'));
    var inp = el('input'); inp.type = 'text'; inp.placeholder = 'contoh: malaikat, qadha, asesmen';
    lab.appendChild(inp); row.appendChild(lab);
    var stat = el('span', 'chip gray'); row.appendChild(stat);
    box.appendChild(row);
    var list = el('div'); box.appendChild(list);

    function draw(q) {
      list.innerHTML = '';
      var n = 0;
      ['pedagogik', 'profesional'].forEach(function (kat) {
        var items = SOAL.filter(function (it) { return it.kategori === kat; }).filter(function (it) {
          if (!q) { return true; }
          var blob = (it.id + ' ' + it.topik + ' ' + it.teks + ' ' + it.opsi.join(' ')).toLowerCase();
          return blob.indexOf(q.toLowerCase()) >= 0;
        });
        if (!items.length) { return; }
        n += items.length;
        var d = el('details', 'acc');
        d.appendChild(el('summary', null, catName(kat) + ' · ' + items.length + ' soal'));
        var b = el('div', 'body');
        items.forEach(function (it) {
          var item = el('div', 'kunciitem');
          item.appendChild(el('div', 'kn', it.id + ' · ' + it.topik + ' · ' + it.tipe.toUpperCase()));
          item.appendChild(el('div', 'kt', it.teks));
          it.opsi.forEach(function (op, i) {
            var ok = it.tipe === 'pg' ? (i === it.kunci) : (it.kunci.indexOf(i) >= 0);
            var line = el('div', 'opt-line' + (ok ? ' correct' : ''));
            line.appendChild(el('span', 'k', letter(i) + '.'));
            line.appendChild(el('span', null, op));
            item.appendChild(line);
          });
          item.appendChild(el('div', 'answerline', 'Kunci: ' + kunciText(it)));
          if (it.bahasan) { item.appendChild(el('div', 'bahasan', it.bahasan)); }
          b.appendChild(item);
        });
        d.appendChild(b); list.appendChild(d);
      });
      stat.textContent = q ? (n + ' soal cocok') : (SOAL.length + ' soal');
    }
    inp.addEventListener('input', function () { draw(inp.value.trim()); });
    draw('');
  }

  /* ---------------- Latihan ---------------- */
  var quiz = { list: [], idx: 0, picked: {}, checked: {}, label: '' };

  function answeredCount() {
    var n = 0;
    Object.keys(STORE.ok || {}).forEach(function (k) { if (STORE.ok[k] !== undefined) { n++; } });
    return n;
  }
  function benarCount() {
    var n = 0;
    Object.keys(STORE.ok || {}).forEach(function (k) { if (STORE.ok[k] === true) { n++; } });
    return n;
  }
  function updateChip() {
    var chip = $('#prog-chip');
    if (!chip) { return; }
    chip.textContent = 'Progres tersimpan: ' + answeredCount() + ' soal dikerjakan · ' + benarCount() + ' benar';
  }

  function initLatihan() {
    var katSel = $('#sel-kat'), topSel = $('#sel-topik');
    if (!katSel || !topSel) { return; }
    function fillTopics() {
      var kat = katSel.value;
      topSel.innerHTML = '';
      var optAll = el('option', null, kat === 'semua' ? 'Semua topik' : 'Semua topik pada kategori ini');
      optAll.value = 'all'; topSel.appendChild(optAll);
      topikList(kat).forEach(function (t) {
        var o = el('option', null, t); o.value = t; topSel.appendChild(o);
      });
    }
    katSel.addEventListener('change', fillTopics);
    fillTopics();
    updateChip();
    $('#btn-mulai').onclick = function () {
      var kat = katSel.value, top = topSel.value;
      var list = SOAL.filter(function (it) {
        if (kat !== 'semua' && it.kategori !== kat) { return false; }
        if (top !== 'all' && it.topik !== top) { return false; }
        return true;
      });
      if ($('#chk-acak').checked) { list = shuffle(list.slice()); }
      if (!list.length) { return; }
      quiz.list = list; quiz.idx = 0; quiz.picked = {}; quiz.checked = {};
      quiz.label = (kat === 'semua' ? 'Semua kategori' : catName(kat)) + (top === 'all' ? '' : ' · ' + top);
      $('#quiz-setup').hidden = true;
      $('#quiz-area').hidden = false;
      $('#quiz-result').hidden = true;
      renderQ();
    };
    $('#btn-salah').onclick = function () {
      var wrongIds = Object.keys(STORE.ok).filter(function (k) { return STORE.ok[k] === false; });
      var list = SOAL.filter(function (it) { return wrongIds.indexOf(it.id) >= 0; });
      if (!list.length) { return; }
      list = shuffle(list.slice());
      quiz.list = list; quiz.idx = 0; quiz.picked = {}; quiz.checked = {};
      quiz.label = 'Ulangi soal yang salah';
      $('#quiz-setup').hidden = true;
      $('#quiz-area').hidden = false;
      $('#quiz-result').hidden = true;
      renderQ();
    };
    $('#btn-reset').onclick = function () {
      if (!window.confirm('Hapus seluruh riwayat jawaban yang tersimpan di peramban ini?')) { return; }
      STORE = { picked: {}, ok: {}, ts: 0 }; save(); updateChip();
      $('#quiz-area').hidden = true; $('#quiz-result').hidden = true; $('#quiz-setup').hidden = false;
    };
  }

  function currentItem() { return quiz.list[quiz.idx]; }

  function renderQ() {
    var it = currentItem();
    var area = $('#quiz-area');
    area.innerHTML = '';
    var bar = el('div', 'qhead');
    var meta = el('div', 'qmeta');
    meta.appendChild(el('span', 'chip', catName(it.kategori)));
    meta.appendChild(el('span', 'chip gray', it.tipe === 'pg' ? 'Pilihan Ganda · 1 jawaban' : 'PG Kompleks · 2 jawaban benar'));
    meta.appendChild(el('span', 'chip gray', it.topik));
    bar.appendChild(meta);
    var pos = el('div', 'small muted', 'Soal ' + (quiz.idx + 1) + ' dari ' + quiz.list.length);
    bar.appendChild(pos);
    area.appendChild(bar);
    var pr = el('div', 'progress'); var fill = el('i');
    fill.style.width = (100 * (quiz.idx) / quiz.list.length) + '%';
    pr.appendChild(fill); area.appendChild(pr);
    area.appendChild(el('div', 'small muted', quiz.label));
    area.appendChild(el('div', 'qtext', it.teks));

    var opts = el('div', 'opts');
    var done = quiz.checked[it.id] ? quiz.picked[it.id] || [] : null;
    it.opsi.forEach(function (op, i) {
      var b = el('button', 'opt'); b.type = 'button';
      var k = el('span', 'key', letter(i)); b.appendChild(k);
      b.appendChild(el('span', null, op));
      if (done) {
        b.disabled = true;
        var correct = it.tipe === 'pg' ? i === it.kunci : it.kunci.indexOf(i) >= 0;
        var chosen = done.indexOf(i) >= 0;
        if (correct && chosen) { b.className = 'opt ok'; }
        else if (!correct && chosen) { b.className = 'opt bad'; }
        else if (correct && !chosen) { b.className = 'opt miss'; }
      } else {
        var sel = (quiz.picked[it.id] || []).slice();
        if (it.tipe === 'pg') {
          if (sel.indexOf(i) >= 0) { b.className = 'opt sel'; }
        } else if (sel.indexOf(i) >= 0) { b.className = 'opt sel'; }
        b.onclick = function () { pickOption(it, i); };
      }
      opts.appendChild(b);
    });
    area.appendChild(opts);

    if (it.tipe === 'pgk' && !done) {
      var row = el('div', 'btnrow');
      var cek = el('button', 'btn', 'Periksa Jawaban');
      cek.disabled = !(quiz.picked[it.id] || []).length;
      cek.onclick = function () { checkAnswer(it); };
      row.appendChild(cek);
      row.appendChild(el('span', 'small muted', 'Pilih dua opsi, lalu tekan Periksa Jawaban.'));
      area.appendChild(row);
    }
    if (done) {
      var ok = isCorrect(it, done);
      var fb = el('div', 'feedback ' + (ok ? 'ok' : 'bad'));
      fb.appendChild(el('div', 'ftitle', ok ? '✔ Jawaban benar' : '✘ Belum tepat'));
      fb.appendChild(el('div', 'small', 'Kunci jawaban: ' + kunciText(it)));
      if (it.bahasan) { fb.appendChild(el('div', 'bahasan', it.bahasan)); }
      area.appendChild(fb);
    }

    var nav = el('div', 'btnrow');
    var prev = el('button', 'btn ghost', '← Sebelumnya');
    prev.disabled = quiz.idx === 0;
    prev.onclick = function () { if (quiz.idx > 0) { quiz.idx--; renderQ(); } };
    nav.appendChild(prev);
    var next = el('button', 'btn', quiz.idx === quiz.list.length - 1 ? 'Lihat Hasil' : 'Berikutnya →');
    next.onclick = function () {
      if (quiz.idx < quiz.list.length - 1) { quiz.idx++; renderQ(); }
      else { showResult(); }
    };
    nav.appendChild(next);
    var back = el('button', 'btn ghost', 'Keluar');
    back.onclick = function () {
      $('#quiz-area').hidden = true; $('#quiz-result').hidden = true; $('#quiz-setup').hidden = false;
      updateChip();
    };
    nav.appendChild(back);
    area.appendChild(nav);
    updateChip();
  }

  function pickOption(it, i) {
    var sel = (quiz.picked[it.id] || []).slice();
    if (it.tipe === 'pg') {
      sel = [i];
      quiz.picked[it.id] = sel;
      checkAnswer(it);
      return;
    }
    var at = sel.indexOf(i);
    if (at >= 0) { sel.splice(at, 1); } else { sel.push(i); }
    quiz.picked[it.id] = sel;
    renderQ();
  }

  function checkAnswer(it) {
    var sel = quiz.picked[it.id] || [];
    if (!sel.length) { return; }
    quiz.checked[it.id] = true;
    STORE.picked[it.id] = sel.slice();
    STORE.ok[it.id] = isCorrect(it, sel);
    save();
    renderQ();
  }

  function showResult() {
    var area = $('#quiz-area'); area.hidden = true;
    var box = $('#quiz-result'); box.hidden = false; box.innerHTML = '';
    var ok = 0, bad = 0, wrong = [];
    quiz.list.forEach(function (it) {
      var picked = quiz.checked[it.id] ? quiz.picked[it.id] : (STORE.ok[it.id] !== undefined ? STORE.picked[it.id] : null);
      if (picked && isCorrect(it, picked)) { ok++; } else { bad++; wrong.push(it); }
    });
    var total = quiz.list.length;
    var pct = total ? Math.round(100 * ok / total) : 0;
    var c = el('div', 'result');
    c.appendChild(el('div', 'score', pct + '%'));
    c.appendChild(el('div', 'muted', ok + ' benar · ' + bad + ' belum tepat dari ' + total + ' soal'));
    c.appendChild(el('div', 'small muted', pct >= 80 ? 'Sangat baik, pertahankan dan ulangi soal yang salah.' : pct >= 60 ? 'Baik, tingkatkan lagi dengan mengulang soal yang salah.' : 'Jangan menyerah, baca rangkuman materi lalu ulangi soal yang salah.'));
    if (wrong.length) {
      var wl = el('ul', 'clean wronglist');
      wrong.slice(0, 30).forEach(function (it) {
        wl.appendChild(el('li', null, it.id + ' · ' + it.topik + ' · kunci ' + kunciText(it)));
      });
      c.appendChild(el('h4', null, 'Soal yang perlu diulang (' + wrong.length + ')'));
      c.appendChild(wl);
    }
    var row = el('div', 'btnrow');
    var again = el('button', 'btn', 'Ulangi set ini');
    again.onclick = function () { quiz.idx = 0; quiz.picked = {}; quiz.checked = {}; $('#quiz-result').hidden = true; $('#quiz-area').hidden = false; renderQ(); };
    row.appendChild(again);
    var ws = el('button', 'btn ghost', 'Latih soal yang salah');
    ws.onclick = function () { $('#btn-salah').click(); };
    row.appendChild(ws);
    var back = el('button', 'btn ghost', 'Pilih set lain');
    back.onclick = function () { box.hidden = true; $('#quiz-setup').hidden = false; updateChip(); };
    row.appendChild(back);
    c.appendChild(row);
    box.appendChild(c);
    updateChip();
  }

  /* ---------------- Start ---------------- */
  document.addEventListener('DOMContentLoaded', function () {
    TABS.forEach(function (t) {
      var btn = document.getElementById('btn-tab-' + t);
      if (btn) { btn.addEventListener('click', function () { showTab(t); }); }
    });
    renderKisi(); renderMateri(); renderKunci();
    var stat = $('#meta-stat');
    if (stat) {
      var np = SOAL.filter(function (i) { return i.kategori === 'pedagogik'; }).length;
      var nr = SOAL.filter(function (i) { return i.kategori === 'profesional'; }).length;
      stat.textContent = SOAL.length + ' soal latihan · ' + np + ' pedagogik · ' + nr + ' profesional';
    }
    initLatihan();
  });
})();
