# Jejak Cilik — Petualangan Fikih MTs

Game 3D **satu berkas HTML** (offline, tanpa server) untuk siswa MTs kelas 7–9.
Seekor anak macan bernama **Cilik** kehilangan jejak induknya. Induk menunggu di
puncak bukit, di balik **150 goa** yang masing-masing menyimpan **10 soal Fikih**.
Temani Cilik mendaki **30 tanjakan** (30 bab) dan kumpulkan minimal **2 bintang**
di setiap goa agar jalan ke atas terbuka.

```
index.html  (≈ 2,0 MB, berdiri sendiri)
```

---

## Cara membuka

1. Unduh/salin `index.html` ke komputer, laptop, atau HP.
2. Klik dua kali berkas itu (atau buka dengan Chrome/Edge/Firefox/Safari).
3. Tidak perlu internet, tidak perlu instalasi apa pun.

Berkas `Jejak-Cilik-Fikih-MTs-1file.html` adalah **salinan persis** dari
`index.html` — gunakan salah satu.

> Jika peramban menonaktifkan WebGL, pemandangan 3D diganti pesan ramah dan
> seluruh soal tetap bisa dimainkan (mode 2D).

## Kontrol

| Aksi | Cara |
|---|---|
| Memutar pandangan | seret tetikus / satu jari |
| Zoom | gulir tetikus / cubit dua jari |
| Naik-turun sudut | seret vertikal / tombol panah |
| Masuk goa | tombol **Masuk Goa** (atau `Enter`) |
| Peta bintang | tombol peta di kanan atas |
| Pengaturan | tombol roda gigi (ganti macan & suasana) |
| Suara / layar penuh | tombol speaker & tombol layar penuh |

## Aturan main

- Setiap **goa = 10 soal** pilihan ganda.
- **5 goa = 1 bab** (50 soal per bab). Total **30 bab = 150 goa = 1.500 soal**.
  - Goa 1–5 → Bab 1, goa 6–10 → Bab 2, … goa 146–150 → Bab 30.
  - Di dalam satu bab, goa ke‑n memakai 10 soal ke‑((n−1)×10+1) sampai +10.
- Bintang per goa:

  | Jawaban benar | Bintang |
  |---|---|
  | 10 | ★★★ |
  | 8–9 | ★★ |
  | 7 | ★ |
  | ≤ 6 | ☆ (tidak lulus) |

- **Minimal 2 bintang (8 benar)** untuk membuka goa berikutnya.
  Gagal? Goa yang sama bisa diulang sebanyak yang dibutuhkan.
- Bab terakhir (Bab 30) selesai → adegan puncak: Cilik bertemu induknya.

Progres (bintang, goa terdepan, pilihan tampilan) disimpan otomatis di
`localStorage` peramban. Ada tombol untuk mengulang dari awal di pengaturan.

## Isi dan variasi

**4 tampilan Cilik** (bisa diganti kapan saja):

| Nama | Ciri |
|---|---|
| Si Belang Sumatera | oranye klasik, belang toska, syal merah — *bawaan* |
| Si Salju Benggala | putih salju, peci emas |
| Si Raja Rimba Cilik | hijau zamrud, peci & rompi emas |
| Si Chibi Gembul | kepala besar, kuncir emas |

**4 suasana bukit**:

| Nama | Ciri |
|---|---|
| Bukit Malam Berbintang | langit malam, bulan, aurora, kunang-kunang — *bawaan* |
| Bukit Zamrud Tropis | siang hijau, terasering, kabut tipis |
| Pegunungan Senja Emas | langit jingga-ungu, lentera hangat |
| Lembah Pinus & Pelangi | pagi berkabut, hutan pinus, pelangi |

## Sumber soal

Seluruh 1.500 soal diambil dari bank soal pada repo
[`bank-soal-fikih-mts`](../bank-soal-fikih-mts) (30 bab, kelas VII–IX,
semester 1–2), lalu divalidasi dan dikemas oleh `build/prep_data.py`.
Tidak ada soal yang dikarang. Stimulus, dalil (Arab/terjemah), dan pembahasan
ikut ditampilkan bila tersedia di bank soal.

## Isi folder

```
index.html                        ← game siap pakai (satu berkas)
Jejak-Cilik-Fikih-MTs-1file.html  ← salinan identik
pratinjau/                        ← tangkapan layar 4 tampilan Cilik + 4 suasana
build/
  build.py            ← penggabung shell + CSS + JS + three.js + data soal
  shell.html          ← markup + sprite SVG (logo, bintang)
  game.css            ← seluruh gaya antarmuka
  js/00-core.js       ← data, simpanan, audio, 4 tampilan, 4 suasana
  js/10-world.js      ← dunia three.js: bukit 30 teras, 150 goa, model Cilik, kamera
  js/20-game.js       ← alur permainan, kuis, peta, pengaturan, adegan puncak
  js/30-ui.js         ← tombol global, boot, jembatan debug
  three.min.js        ← three.js r160 (disematkan, tanpa CDN)
  questions.json      ← muatan soal tervalidasi (30 bab / 150 goa / 1.500 soal)
  prep_data.py        ← pengubah bank soal → questions.json
```

## Membangun ulang

```bash
cd game-macan-fikih-mts
python3 build/prep_data.py     # (opsional) segarkan questions.json dari bank soal
python3 build/build.py         # hasil: index.html + salinan 1file
```

Keluaran build: `bab=30 goa=150 soal=1500`.

## Catatan teknis

- three.js r160 disematkan **di dalam** HTML; tidak ada permintaan jaringan
  (tidak ada CDN, font, atau gambar eksternal).
- Huruf memakai tumpukan font sistem; ikon memakai sprite SVG, bukan emoji,
  agar tampil sama di semua perangkat.
- Seluruh UI berbahasa Indonesia dan responsif (ponsel potret, tablet, desktop).
- Denah bukit: 30 teras melingkar, rasio radius `outerR(b) = RTOP + (R0−RTOP)·(1−b/29)^0.78`,
  tinggi teras 3 satuan, goa ditempatkan di kaki tebing tiap teras
  (6 goa per teras, 30 × 5 = 150 goa).
- Aksesibilitas: kontras teks tinggi, tombol besar, bunyi dapat dimatikan,
  animasi kamera dapat dilewati lewat pengaturan "sinematik".

## Lisensi & kredit

- Soal: **Bank Soal Fikih MTs** (repo `bank-soal-fikih-mts`).
- Kode game, model 3D, dan antarmuka dibuat khusus untuk proyek ini.
- three.js © three.js authors, lisensi MIT.
