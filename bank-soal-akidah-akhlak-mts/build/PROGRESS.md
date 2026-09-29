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

[x] k7/adab-berpakaian — Adab Berpakaian & Berhias
[x] k7/adab-makan-minum — Adab Makan, Minum & Perjalanan
[x] k7/allah-asmaul-husna — Allah, Asmaul Husna & Sifat Wajib
[x] k7/asmaul-husna-2 — Asmaul Husna: al-Karim, al-Mumin, al-Wakil, al-Matin
[x] k7/dalil-naqli-aqli — Dalil Naqli & Aqli tentang Allah
[x] k7/hormat-taat — Hormat & Taat kepada Orang Tua dan Guru
[x] k7/iman-malaikat — Iman kepada Malaikat
[x] k7/jujur — Hidup Jujur
[x] k7/kisah-sabar — Kisah Ketabahan Nabi Ayyub & Keluarga Nabi Yakub
[x] k7/riya-nifaq — Menghindari Riya, Nifaq & Takabur
[x] k7/syukur — Syukur Nikmat & Hidup Sederhana
[ ] k8/adab-ibadah — Adab dalam Beribadah
[x] k8/adab-muamalah — Adab Muamalah & Etos Kerja
[x] k8/adab-silaturahmi — Adab Silaturahmi
[ ] k8/akhlak-tercela-2 — Menghindari Minuman Keras, Narkoba & Judi
[ ] k8/asmaul-husna-3 — Asmaul Husna (al-Waliy, al-Hamid, asy-Syakur, al-Aliyy)
[x] k8/hasad-ghibah-fitnah — Menghindari Hasad, Ghibah & Fitnah
[ ] k8/hormat-guru — Hormat dan Taat kepada Guru
[ ] k8/kisah-sahabat — Kisah Kesungguhan Ibadah Para Sahabat
[ ] k8/kisah-ulul-azmi — Kisah Keteladanan Rasul Ulul Azmi
[x] k8/tawadu-ta-at-qanaah — Tawadu, Taat & Qanaah
[ ] k8/tawakal-ikhtiar — Iman kepada Takdir, Ikhtiar, Doa & Tawakal
[ ] k9/adab-medsos — Adab Menggunakan Media Sosial
[ ] k9/akhlak-tercela-9 — Akhlak Tercela: Namimah, Su uzan, Takabur & Ananiah
[ ] k9/akhlak-terpuji-9 — Akhlak Terpuji: Sabar, Syukur, Istiqamah & Husnuzan
[ ] k9/islam-seni-budaya — Islam, Seni, Budaya & Teknologi
[ ] k9/kisah-dakwah-nabi — Kisah Perjuangan Dakwah Nabi & Sahabat
[ ] k9/mengharap-ridha — Mengharap Ridha Allah & Ikhlas Beramal
[ ] k9/muslim-sejati — Muslim Sejati
[ ] k9/qadha-qadar — Iman kepada Qadha & Qadar
[ ] k9/surga-neraka — Surga & Neraka
[ ] k9/tauhid-syirik — Tauhid & Syirik

## Status — Fikih MTs (30 bab)

Belum dimulai. Infrastruktur (engine `app.js`, CSS dan pemuat `index.html`,
`build/typecheck.py`, `build/build.py`, `build/validate.py`, `build/jsobj.py`,
`build/datafile.py`, `build/balance_types.py`) perlu disalin lebih dahulu dari
proyek Akidah Akhlak, lalu 30 berkas `data/types/<kelas>/<slug>.js` ditulis.

Catatan khusus Fikih: footer berkas data berbunyi `"\n]\n});\n"` dan berkas lama
memakai escape `\'`; berkas tipe baru tetap memakai footer `window.BSAddTypes({...});`
dan harus bebas apostrof.

## Kemajuan terakhir

- Akidah Akhlak: 15 dari 32 bab selesai (525 soal tipe baru), total berkas 2125 soal.
- Rincian: Kelas VII 11/11 bab selesai, Kelas VIII 4/11 bab, Kelas IX 0/10 bab.
- Fikih: 0 dari 30 bab, infrastruktur belum disalin.
