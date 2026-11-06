/* Uji integritas HTML 1 file hasil build di node.
   Jalankan: node build/smoke_built.mjs [path-html]
   Memuat skrip data+bootstrap, memanggil BSMergeTypes(), lalu memeriksa jumlah
   soal per tipe, keseimbangan pasangan PGK, keseimbangan B/S, kelengkapan field,
   dan duplikat batang soal dengan kunci stimulus+teks (selaras validate.py). */
import fs from 'fs';

const file = process.argv[2] || 'Bank-Soal-Fikih-MTs-1file.html';
const h = fs.readFileSync(file, 'utf8');
const scripts = [...h.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
globalThis.window = globalThis;
for (let i = 0; i < 2; i++) {
  try { (0, eval)(scripts[i]); } catch (e) { console.log('ERR eval script', i, e.message.slice(0, 120)); }
}
globalThis.window.BSMergeTypes();
const T = globalThis.window.__BS.topics, idx = globalThis.window.__BS.index;
console.log('index materi:', idx.length, '| topics:', Object.keys(T).length);

let tot = { pgk: 0, bs: 0, singkat: 0, essay: 0, pg: 0 }, bad = [], pairs = {}, bsTF = { B: 0, S: 0 }, babTipe = 0;
const stems = new Map();
const key = q => ((q.stimulus || '').trim() + '\u0001' + (q.text || '').trim());

for (const id of Object.keys(T)) {
  const t = T[id];
  tot.pg += (t.questions || []).length;
  for (const q of (t.questions || [])) {
    const s = key(q);
    if (stems.has(s)) bad.push('DUP STEM PG ' + id + ' & ' + stems.get(s)); else stems.set(s, id);
    if (!(q.answer >= 0 && q.answer <= 3)) bad.push(id + ' pg answer');
    if (!q.options || q.options.length !== 4) bad.push(id + ' pg opsi');
  }
  const hasTypes = ['pgk', 'bs', 'singkat', 'essay'].some(k => (t[k] || []).length > 0);
  if (hasTypes) babTipe++;
  for (const k of ['pgk', 'bs', 'singkat', 'essay']) {
    const arr = t[k] || []; tot[k] += arr.length;
    if (hasTypes) {
      if (k !== 'essay' && arr.length !== 10) bad.push(id + ' ' + k + '=' + arr.length);
      if (k === 'essay' && arr.length !== 5) bad.push(id + ' essay=' + arr.length);
    }
    for (const q of arr) {
      const s = key(q);
      if (stems.has(s)) bad.push('DUP STEM ' + k + ' ' + id + ' & ' + stems.get(s)); else stems.set(s, id);
      if (q.type !== k) bad.push(id + ' ' + k + ' type tag');
      if (!q.indicator) bad.push(id + ' ' + k + ' indicator');
      if (!q.explanation) bad.push(id + ' ' + k + ' explanation');
      if (q.level !== 'HOTS') bad.push(id + ' ' + k + ' level');
      if (k === 'pgk') {
        if (!q.options || q.options.length !== 4) bad.push(id + ' pgk opsi');
        if (!Array.isArray(q.answers) || q.answers.length !== 2) bad.push(id + ' pgk answers');
        else { const p = [...q.answers].sort((a, b) => a - b).join(''); pairs[p] = (pairs[p] || 0) + 1; }
      }
      if (k === 'bs') { if (typeof q.answer !== 'boolean') bad.push(id + ' bs nonbool'); else bsTF[q.answer ? 'B' : 'S']++; }
      if (k === 'singkat') {
        const w = (q.answer || '').trim().split(/\s+/).length;
        if (w < 1 || w > 4) bad.push(id + ' singkat ' + w + ' kata: ' + q.answer);
        if (!q.accepted || !q.accepted.length) bad.push(id + ' singkat accepted');
        for (const a of (q.accepted || [])) if (a.trim().split(/\s+/).length > 4) bad.push(id + ' accepted >4 kata: ' + a);
      }
      if (k === 'essay') { if (!q.key) bad.push(id + ' essay key'); if (!q.rubric || q.rubric.length < 2) bad.push(id + ' essay rubric'); }
    }
  }
}
console.log('bab bertipe:', babTipe, '| soal PG:', tot.pg, '| tipe lain:', JSON.stringify({ pgk: tot.pgk, bs: tot.bs, singkat: tot.singkat, essay: tot.essay }));
console.log('TOTAL soal:', tot.pg + tot.pgk + tot.bs + tot.singkat + tot.essay);
console.log('pasangan pgk:', JSON.stringify(pairs));
console.log('bs Benar/Salah:', JSON.stringify(bsTF));
console.log('batang unik (stimulus+teks):', stems.size);
console.log(bad.length ? ('MASALAH(' + bad.length + '):\n' + bad.slice(0, 20).join('\n')) : 'SEMUA PEMERIKSAAN LULUS');
