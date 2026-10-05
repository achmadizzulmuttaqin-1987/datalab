# Latihan AKG Akidah Akhlak MTs

Aplikasi web **satu berkas** untuk latihan mandiri menghadapi Asesmen Kompetensi Guru (AKG) madrasah, khusus mata pelajaran Akidah Akhlak jenjang MTs. Berkas hasil bangun dapat dibuka langsung dari HP, laptop, atau komputer tanpa internet dan tanpa pemasangan apa pun.

## Catatan penting tentang keaslian soal

- Naskah asli AKG **tidak dipublikasikan** oleh Kementerian Agama, sehingga tidak ada soal resmi tahun lalu yang dapat disalin atau diunduh. Bank soal ini **bukan** salinan soal ujian.
- Seluruh **300 soal** pada aplikasi ini adalah **soal latihan yang ditulis orisinal**, disusun mengikuti format, komposisi, dan kisi-kisi resmi AKG madrasah. Aplikasi ini bukan produk resmi Kementerian Agama.
- Dasar penyusunan: juknis dan kisi-kisi AKG Direktorat Jenderal Pendidikan Islam (kompetensi pedagogik dan profesional, 60 butir per paket), Permendiknas Nomor 16 Tahun 2007, KMA Nomor 183 Tahun 2019, dan KMA Nomor 347 Tahun 2022.

## Isi bank soal

| Bagian | Jumlah | Keterangan |
| --- | --- | --- |
| Pedagogik | 150 butir | karakteristik peserta didik, teori belajar, kurikulum, desain pembelajaran, potensi peserta didik, komunikasi, penilaian, PTK, teknologi, profesi dan etika guru, serta bimbingan dan konseling |
| Profesional Akidah Akhlak | 150 butir | akidah, asmaul husna, malaikat-kitab-rasul, hari akhir dan qadha qadar, ilmu kalam, akhlak dan tasawuf, adab kontemporer, kisah teladan, serta pembelajaran Akidah Akhlak |
| **Total** | **300 butir** | 266 pilihan ganda dan 34 pilihan ganda kompleks (dua jawaban benar) |

Perbandingan pedagogik dan profesional dibuat 1 banding 1 agar kedua ranah terlatih seimbang. Komposisi resmi AKG jenjang MTs sendiri memuat 20 butir pedagogik dan 40 butir profesional pada setiap paket soal.

Setiap butir memuat kunci jawaban dan pembahasan. Aplikasi juga memuat **kisi-kisi AKG** dan **rangkuman materi 10 seksi** sebagai bekal belajar.

## Fitur aplikasi

- Latihan per kategori (pedagogik, profesional) atau per topik, dengan opsi pengacakan urutan soal.
- Umpan balik langsung untuk setiap jawaban: benar atau belum tepat, kunci, dan pembahasan.
- Tombol **Latih soal yang salah** untuk menuntaskan butir yang belum tepat.
- Progres jawaban tersimpan otomatis di peramban (tanpa internet) dan dapat dihapus.
- Tab **Kunci dan Pembahasan** memuat seluruh soal dengan pencarian.
- Tombol **Cetak / Simpan PDF**: seluruh rangkuman dan kunci dapat dicetak ke PDF dari peramban.
- Berkas tunggal: CSS, JavaScript, data soal, dan seluruh aset tertanam (sekitar 214 KB).

## Cara memakai

1. Buka berkas `Bank-Soal-AKG-Akidah-Akhlak-MTs-1file.html` dengan peramban apa pun (kembar klik).
2. Pada perangkat seluler, berkas dapat dipindahkan melalui pesan atau penyimpanan lalu dibuka dari aplikasi berkas.
3. Ikuti urutan tab: Petunjuk, Kisi-Kisi AKG, Rangkuman Materi, Latihan Soal, lalu Kunci dan Pembahasan.

## Struktur berkas

```
bank-soal-akg-akidah-akhlak-mts/
  Bank-Soal-AKG-Akidah-Akhlak-MTs-1file.html   <-- hasil bangun (berkas tunggal)
  README.md
  build/
    app.css, app.js             antarmuka dan logika aplikasi
    build_app.py                menyatukan semua aset menjadi satu HTML
    validate_app.py             pemeriksaan mutu bank soal
    smoke_app.mjs               uji asap berkas HTML hasil bangun
    rebalance_keys.py           penyeimbang sebaran kunci jawaban
    apply_opsi_patch.py         penerap tambalan teks opsi
    patch/patch-opsi-1.json     tambalan penyeimbang panjang opsi
    patch/patch-opsi-2.json     tambalan penyeimbang panjang opsi tahap kedua
    data/                       bank soal, kisi-kisi, dan rangkuman
    PROGRESS.md                 catatan pembangunan
```

## Membangun ulang

```bash
cd bank-soal-akg-akidah-akhlak-mts
python3 build/validate_app.py                              # periksa mutu data
node --check build/app.js                                  # periksa sintaks skrip
python3 build/build_app.py                                 # bangun berkas HTML
node build/smoke_app.mjs Bank-Soal-AKG-Akidah-Akhlak-MTs-1file.html   # uji asap
```

## Mutu yang dijaga

- Semua butir memuat empat opsi, opsi tidak kembar, dan kunci sesuai tipe soal.
- Sebaran kunci pilihan ganda merata: A=67, B=67, C=66, D=66.
- Pasangan kunci pilihan ganda kompleks merata pada enam kombinasi: AB=6, AC=6, AD=6, BC=6, BD=5, CD=5.
- Panjang opsi jawaban benar tidak menyolok dibandingkan distraktor (0 butir timpang pada ambang 4 kata).
- Batang soal unik dan setiap butir memiliki pembahasan.
