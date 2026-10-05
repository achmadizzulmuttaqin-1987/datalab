# Pelacak Pengerjaan Soal Tipe Baru (PGK - B/S - Singkat - Esai) — Fikih MTs

Target: 35 soal HOTS per bab = 10 PGK + 10 Benar/Salah + 10 Jawaban Singkat + 5 Esai.
Jumlah bab Fikih MTs: 30 -> 1.050 soal tipe baru.

Infrastruktur telah disalin dari proyek Akidah Akhlak: engine multi-tipe pada
`app.js`, pemuat berkas tipe pada `index.html`, serta `build/typecheck.py`,
`build/lint_types.py`, `build/balance_types.py`, `build/validate.py`,
`build/gen_dist.py`, `build/build.py`, `build/jsobj.py`, `build/datafile.py`.

## Aturan yang wajib dipatuhi setiap bab

| Aturan | Ketentuan |
|---|---|
| PGK | 4 opsi, tepat 2 benar (`answers` terurut naik) |
| Pasangan kunci PGK | 6 kombinasi (AB, AC, AD, BC, BD, CD) terbagi rata, masing-masing maksimal 2 per bab |
| Benar/Salah | tepat 5 Benar dan 5 Salah |
| Jawaban singkat | 1-4 kata, sertakan `accepted` (varian ejaan/sinonim) |
| Esai | wajib `key`, `rubric` minimal 2 butir; tidak dinilai otomatis |
| Level | seluruh soal `HOTS` |
| Stem | tidak boleh duplikat, termasuk terhadap 50 soal PG yang sudah ada |
| Tanda kutip | jangan memakai apostrof; tulis "Al-Quran" |

## Alur kerja per bab

1. Baca `data/<kelas>/<slug>.js` untuk mengetahui judul, KD, deskripsi, dan indikator soal PG (agar stem tidak duplikat).
2. Tulis `data/types/<kelas>/<slug>.js` mengikuti format bab yang sudah selesai.
3. `python3 build/lint_types.py <slug>`
4. `node --check data/types/<kelas>/<slug>.js`
5. `python3 build/balance_types.py --bab <kelas>/<slug>`
6. `python3 build/validate.py` -> harus "Semua pemeriksaan lulus".
7. Ulangi untuk bab berikutnya; jalankan `python3 build/build.py` setelah beberapa bab selesai.

## Status — Fikih MTs (30 bab)

[x] k7/thaharah — Thaharah (Bersuci)
[x] k7/salat-fardu — Salat Fardu, Adzan & Iqamah
[x] k7/salat-sunnah — Salat Sunnah Muakkad & Ghairu Muakkad
[x] k7/salat-berjamaah — Salat Berjamaah & Munfarid
[x] k7/salat-darurat — Salat dalam Keadaan Darurat
[x] k7/salat-jumat — Salat Jumat
[x] k7/salat-jamak — Salat Jama', Qasar, & Khauf
[x] k7/salat-idain — Salat Idain (Idulfitri & Iduladha)
[x] k7/salat-sunah-lain — Salat Sunah Berjamaah & Munfarid Lainnya
[x] k7/adab-masjid — Adab Masuk Masjid & Zikir
[x] k8/sujud — Sujud Sahwi, Tilawah & Syukur
[x] k8/puasa — Puasa Wajib dan Puasa Sunah
[x] k8/zakat — Zakat Fitrah & Zakat Mal
[x] k8/haji — Haji dan Umrah
[x] k8/makanan — Makanan & Minuman Halal-Haram
[x] k8/qurban — Qurban dan Akikah
[x] k8/muamalah — Muamalah (Jual Beli, Khiyar, Qirad)
[x] k8/riba — Riba, Bank & Rahn
[x] k8/waris — Hukum Waris dalam Islam
[x] k8/hikmah-ibadah — Hikmah Ibadah Mahdah & Ghairu Mahdah
[x] k9/sembelihan — Penyembelihan Hewan
[x] k9/qurban-akikah — Qurban dan Akikah (Pendalaman)
[x] k9/haji-umrah — Haji & Umrah (Pendalaman Manasik)
[x] k9/muamalah-modern — Muamalah: Jual Beli Terlarang & Kontemporer
[x] k9/riba-bank — Riba, Bank, Rahn & Hutang Piutang
[x] k9/asuransi — Asuransi Syariah (Takaful)
[x] k9/koperasi — Koperasi Syariah & Mudharabah
[x] k9/waris-hitung — Perhitungan Waris (Ilmu Faraid)
[x] k9/nikah — Pernikahan dalam Islam
[x] k9/hikmah-syariat — Hikmah & Implementasi Syariat

## Kemajuan terakhir

- Infrastruktur multi-tipe selesai disalin dan diuji: `validate.py` lulus
  (1.500 soal PG, 30 materi) dan `build.py` menghasilkan
  `Bank-Soal-Fikih-MTs-1file.html` yang termuat benar pada uji asap Node.
- Satu batang soal PG duplikat antarbab diperbaiki: `k9/qurban-akikah.js` #4
  ditulis ulang menjadi soal analisis ketentuan jumlah dan waktu akikah.
- Pemeriksaan duplikat batang PG kini menggabungkan `stimulus` dengan batang
  soal, karena soal berstimulus (kutipan dalil, tabel, kasus) sah memakai
  batang yang sama selama stimulusnya berbeda. Perbaikan yang sama diterapkan
  pada proyek Akidah Akhlak.
- Soal tipe baru: **1.050 dari 1.050 — SELESAI (30/30 bab)**.
  Rinciannya 300 PGK (4 opsi, tepat 2 jawaban benar; pasangan kunci
  AB/AC/AD/BC/BD/CD terbagi rata), 300 Benar/Salah (tepat 150 Benar dan
  150 Salah), 300 jawaban singkat (1-4 kata, dilengkapi `accepted`), serta
  150 esai (kunci, rubrik minimal 2 butir, penjelasan; tidak dinilai otomatis).
- Total isi `Bank-Soal-Fikih-MTs-1file.html` kini 2.550 soal
  (1.500 pilihan ganda + 1.050 tipe baru).
- Setiap bab melewati `lint_types.py`, `balance_types.py --bab`, `validate.py`,
  `dup_check.py` (A-E nol), `dup_stem.py`, lalu `build.py` dan
  `build/smoke_built.mjs` (SEMUA PEMERIKSAAN LULUS).

## Pemerataan panjang opsi jawaban (Fikih) — SELESAI
- Latar: pada soal PG dan PGK, teks opsi jawaban benar rata-rata lebih panjang
  daripada distraktor sehingga kunci mudah ditebak tanpa menguasai materi.
- Tindakan: hanya teks opsi jawaban benar yang diringkas — kunci/indeks
  (`answer`/`answers`), distraktor, penjelasan, stimulus, serta soal
  singkat/Benar-Salah/esai sama sekali tidak diubah.
- Hasil: dari 1.269 PG dan 184 PGK yang timpang, kini **0 butir timpang**
  (ambang 4 kata) untuk PG 1.500 butir maupun PGK 300 butir.
- PGK: rata-rata panjang opsi benar 20,4 kata vs opsi salah 23,3 kata;
  selisih >= 2 kata tinggal 65 butir (21,7%), >= 3 kata 34 butir (11,3%),
  >= 4 kata 0 butir.
- Alat kerja (salinan identik dari proyek Akidah Akhlak):
  `len_check.py`, `len_dump.py`, `len_sample.py`, `shorten_apply.py` (PG)
  dan `pgk_len.py`, `pgk_apply.py` (PGK); patch per bab disimpan di
  `/home/user/patches/fikih-<kelas>-<slug>.json` dan `fikih-pgk-...json`.
- Verifikasi akhir: `lint_types.py`, `validate.py` (2.550 soal),
  `dup_check.py` (nol soal kembar), `balance_types.py --check`
  (pgk 300, bs 300 = 150 B/150 S, pasangan kunci 60/60/60/60/30/30,
  batang unik 2.550), `build.py`, dan `build/smoke_built.mjs` — semua lulus.
- Output akhir: `Bank-Soal-Fikih-MTs-1file.html` (2.550 soal, ±3,7 MB).
