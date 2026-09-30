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

[ ] k7/thaharah — Thaharah (Bersuci)
[ ] k7/salat-fardu — Salat Fardu, Adzan & Iqamah
[ ] k7/salat-sunnah — Salat Sunnah Muakkad & Ghairu Muakkad
[ ] k7/salat-berjamaah — Salat Berjamaah & Munfarid
[ ] k7/salat-darurat — Salat dalam Keadaan Darurat
[ ] k7/salat-jumat — Salat Jumat
[ ] k7/salat-jamak — Salat Jama', Qasar, & Khauf
[ ] k7/salat-idain — Salat Idain (Idulfitri & Iduladha)
[ ] k7/salat-sunah-lain — Salat Sunah Berjamaah & Munfarid Lainnya
[ ] k7/adab-masjid — Adab Masuk Masjid & Zikir
[ ] k8/sujud — Sujud Sahwi, Tilawah & Syukur
[ ] k8/puasa — Puasa Wajib dan Puasa Sunah
[ ] k8/zakat — Zakat Fitrah & Zakat Mal
[ ] k8/haji — Haji dan Umrah
[ ] k8/makanan — Makanan & Minuman Halal-Haram
[ ] k8/qurban — Qurban dan Akikah
[ ] k8/muamalah — Muamalah (Jual Beli, Khiyar, Qirad)
[ ] k8/riba — Riba, Bank & Rahn
[ ] k8/waris — Hukum Waris dalam Islam
[ ] k8/hikmah-ibadah — Hikmah Ibadah Mahdah & Ghairu Mahdah
[ ] k9/sembelihan — Penyembelihan Hewan
[ ] k9/qurban-akikah — Qurban dan Akikah (Pendalaman)
[ ] k9/haji-umrah — Haji & Umrah (Pendalaman Manasik)
[ ] k9/muamalah-modern — Muamalah: Jual Beli Terlarang & Kontemporer
[ ] k9/riba-bank — Riba, Bank, Rahn & Hutang Piutang
[ ] k9/asuransi — Asuransi Syariah (Takaful)
[ ] k9/koperasi — Koperasi Syariah & Mudharabah
[ ] k9/waris-hitung — Perhitungan Waris (Ilmu Faraid)
[ ] k9/nikah — Pernikahan dalam Islam
[ ] k9/hikmah-syariat — Hikmah & Implementasi Syariat

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
- Soal tipe baru: 0 dari 1.050.
