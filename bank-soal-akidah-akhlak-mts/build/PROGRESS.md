# Pelacak Pengerjaan Soal Tipe Baru (PGK · B/S · Singkat · Esai)

Target: 35 soal HOTS per bab = 10 PGK + 10 Benar/Salah + 10 Jawaban Singkat + 5 Esai.
Jumlah bab: 32 (Akidah Akhlak) + 30 (Fikih) = 62 bab → 2.170 soal.

## Aturan yang wajib dipatuhi setiap bab

| Aturan | Ketentuan |
|---|---|
| PGK | 4 opsi, tepat 2 benar (`answers` terurut naik) |
| Pasangan kunci PGK | 6 kombinasi (AB, AC, AD, BC, BD, CD) terbagi rata, masing-masing maksimal 2 per bab |
| Benar/Salah | tepat 5 Benar dan 5 Salah |
| Jawaban singkat | 1–4 kata, sertakan `accepted` (varian ejaan/sinonim) |
| Esai | wajib `key`, `rubric` minimal 2 butir; tidak dinilai otomatis |
| Level | seluruh soal `HOTS` |
| Stem | tidak boleh duplikat, termasuk terhadap 50 soal PG yang sudah ada |
| Tanda kutip | jangan memakai apostrof; tulis "Al-Quran" |

## Alur kerja per bab

1. Baca `data/<kelas>/<slug>.js` untuk mengetahui judul, KD, deskripsi, dan indikator soal PG (agar stem tidak duplikat).
2. Tulis `data/types/<kelas>/<slug>.js` mengikuti format yang sama dengan bab yang sudah selesai.
3. `node --check data/types/<kelas>/<slug>.js`
4. `python3 build/balance_types.py --bab <kelas>/<slug>` → meratakan pasangan kunci PGK dan mengacak urutan soal.
5. `python3 build/validate.py` → harus "Semua pemeriksaan lulus".
6. Ulangi untuk bab berikutnya; jalankan `python3 build/build.py` setelah beberapa bab selesai.

## Status — Akidah Akhlak MTs (32 bab)

[x] k7/dalil-naqli-aqli — Dalil Naqli & Aqli tentang Allah
[x] k7/allah-asmaul-husna — Allah, Asmaul Husna & Sifat Wajib
[x] k7/iman-malaikat — Iman kepada Malaikat
[x] k7/syukur — Syukur Nikmat & Hidup Sederhana
[x] k7/jujur — Hidup Jujur
[x] k7/hormat-taat — Hormat & Taat kepada Orang Tua dan Guru
[x] k7/riya-nifaq — Menghindari Riya, Nifaq & Takabur
[x] k7/adab-berpakaian — Adab Berpakaian & Berhias
[x] k7/adab-makan-minum — Adab Makan, Minum & Perjalanan
[x] k7/kisah-sabar — Kisah Ketabahan Nabi Ayyub & Keluarga Nabi Yakub
[x] k7/asmaul-husna-2 — Asmaul Husna (al-Karim, al-Mumin, al-Wakil, al-Matin)
[x] k8/tawakal-ikhtiar — Iman kepada Takdir, Ikhtiar, Doa & Tawakal
[x] k8/tawadu-ta-at-qanaah — Tawadu, Taat & Qanaah
[x] k8/hasad-ghibah-fitnah — Menghindari Hasad, Ghibah & Fitnah
[x] k8/adab-ibadah — Adab Beribadah & Membaca Al-Quran
[x] k8/adab-silaturahmi — Adab Menjenguk, Melawat & Silaturahmi
[x] k8/kisah-ulul-azmi — Kisah Ketabahan Nabi Ulul Azmi
[x] k8/asmaul-husna-3 — Asmaul Husna (al-Waliy, al-Hamid, asy-Syakur, al-Aliyy)
[x] k8/hormat-guru — Adab terhadap Guru & Orang Tua
[x] k8/akhlak-tercela-2 — Menghindari Minuman Keras, Narkoba & Judi
[x] k8/adab-muamalah — Adab Muamalah & Etos Kerja
[x] k8/kisah-sahabat — Kisah Kesungguhan Ibadah Para Sahabat
[x] k9/mengharap-ridha — Mengharap Ridha Allah & Ikhlas Beramal
[x] k9/tauhid-syirik — Tauhid, Syirik, Murtad & Tahayul
[x] k9/qadha-qadar — Qadha, Qadar & Sikap terhadap Takdir
[x] k9/surga-neraka — Iman kepada Hari Akhir, Surga & Neraka
[x] k9/akhlak-terpuji-9 — Akhlak Terpuji: Sabar, Syukur, Istiqamah & Husnuzan
[x] k9/akhlak-tercela-9 — Akhlak Tercela: Namimah, Su uzan, Takabur & Ananiah
[x] k9/adab-medsos — Adab Menggunakan Media Sosial
[x] k9/islam-seni-budaya — Islam, Seni, Budaya & Teknologi
[x] k9/kisah-dakwah-nabi — Kisah Perjuangan Dakwah Nabi & Sahabat
[x] k9/muslim-sejati — Ciri Muslim Sejati & Akhlakul Karimah

## Status — Fikih MTs (30 bab)

Belum dimulai. Infrastruktur (engine `app.js`, CSS dan pemuat `index.html`,
`build/typecheck.py`, `build/build.py`, `build/validate.py`, `build/jsobj.py`,
`build/datafile.py`, `build/balance_types.py`) perlu disalin lebih dahulu dari
proyek Akidah Akhlak, lalu 30 berkas `data/types/<kelas>/<slug>.js` ditulis.

Catatan khusus Fikih: footer berkas data berbunyi `"\n]\n});\n"` dan berkas lama
memakai escape `\'`; berkas tipe baru tetap memakai footer `window.BSAddTypes({...});`
dan harus bebas apostrof.

## Kemajuan terakhir

- Akidah Akhlak: **32 dari 32 bab selesai** — 1.120 soal tipe baru
  (320 PGK + 320 Benar/Salah + 320 Jawaban Singkat + 160 Esai).
- Total berkas Akidah Akhlak: **2.720 soal** (1.600 PG + 1.120 tipe baru),
  seluruh batang soal unik, kunci PGK rata per bab (maks. 2 per kombinasi),
  Benar/Salah tepat 5 Benar dan 5 Salah per bab.
- Output: `Bank-Soal-Akidah-Akhlak-MTs-1file.html` (±5,4 MB) — `validate.py`
  dan uji asap Node atas HTML jadi keduanya lulus.
- Fikih: **30 dari 30 bab selesai** — 1.050 soal tipe baru (300 PGK, 300
  Benar/Salah, 300 jawaban singkat, 150 esai) sehingga total isi
  `Bank-Soal-Fikih-MTs-1file.html` menjadi 2.550 soal. Seluruh pemeriksaan
  lulus di kedua proyek.
