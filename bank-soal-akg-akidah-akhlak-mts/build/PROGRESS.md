# Catatan Pembangunan — Latihan AKG Akidah Akhlak MTs

## Ruang lingkup

- Permintaan: bahan belajar menghadapi AKG Akidah Akhlak, dalam bentuk aplikasi web luring satu berkas.
- Keputusan pengguna (via pilihan): jenjang **MTs**, cakupan **pedagogik + profesional**.
- Kebijakan keaslian: naskah AKG tidak dipublikasikan, sehingga tidak ada soal resmi yang dapat disalin. Seluruh soal ditulis orisinal mengikuti format dan kisi-kisi resmi. Aplikasi **bukan** produk resmi Kementerian Agama.

## Bank soal

| Bagian | Butir | Rincian |
| --- | --- | --- |
| Pedagogik | 50 | 10 topik: karakteristik peserta didik, teori belajar, kurikulum, desain pembelajaran, potensi peserta didik, komunikasi, penilaian, PTK, teknologi |
| Profesional | 100 | iman kepada Allah (25), malaikat-kitab-rasul (15), hari akhir-qadha qadar-ilmu kalam (15), akhlak (25), adab (8), kisah teladan (10), pembelajaran Akidah Akhlak (12) |
| Total | 150 | 139 pilihan ganda + 11 pilihan ganda kompleks (dua jawaban benar) |

Komposisi pedagogik berbanding profesional 1 banding 2, mengikuti perbandingan AKG jenjang MTs (20 butir pedagogik berbanding 40 butir profesional per paket).

Setiap butir memuat: id, topik, kategori, tipe, batang soal, empat opsi, kunci, dan pembahasan. Tambahan bahan: `kisi-kisi.json` (struktur resmi AKG yang diringkas) dan `rangkuman.json` (10 seksi materi).

## Alur kerja

1. `validate_app.py` memeriksa struktur: id unik, empat opsi, opsi tidak kembar, kunci sesuai tipe, batang unik, pembahasan ada, tanpa tanda apostrof pada opsi.
2. Pemeriksaan sebaran kunci dan panjang opsi menemukan dua masalah pada draf awal:
   - sebaran kunci PG sangat timpang (A=58, B=64, C=15, D=2) dan seluruh PGK berkunci AB;
   - 43 butir memiliki opsi kunci jauh lebih panjang daripada distraktor.
3. Perbaikan panjang opsi melalui tambalan terverifikasi (`apply_opsi_patch.py`):
   - `patch-opsi-1.json`: 23 butir pada ambang 6 kata;
   - `patch-opsi-2.json`: 20 butir pada ambang 4 kata.
   Tidak ada kunci, batang soal, atau pembahasan yang diubah pada tahap ini.
4. `rebalance_keys.py` (deterministik, benih tetap) memindahkan opsi benar sehingga sebaran kunci merata: A=35, B=35, C=35, D=34; pasangan PGK AB=2, AC=2, AD=2, BC=2, BD=2, CD=1.
5. `build_app.py` menyatukan CSS, JavaScript, dan seluruh data menjadi satu berkas HTML mandiri.
6. `smoke_app.mjs` memeriksa berkas hasil: blok data dapat diekstrak dan valid, jumlah soal 150 (50 pedagogik, 100 profesional), id unik, kunci sesuai tipe, semua butir beropsi empat dan berpembahasan.

## Hasil akhir

- Berkas: `Bank-Soal-AKG-Akidah-Akhlak-MTs-1file.html`, sekitar 126 KB, dibuka luring tanpa berkas pendamping.
- Pemeriksaan: `validate_app.py` lulus (0 butir opsi timpang), `node --check` lulus, `smoke_app.mjs` lulus.
- Fitur: latihan per kategori/topik, pengacakan, umpan balik dan pembahasan langsung, latih ulang soal salah, penyimpanan progres di peramban, tab kunci dengan pencarian, serta cetak/simpan PDF.

## Batas dan tanggung jawab

- Soal disusun sebagai bahan latihan mandiri; tidak mewakili naskah, penilaian, atau kebijakan resmi pihak mana pun.
- Jadwal dan ketentuan resmi AKG mengikuti pengumuman Kementerian Agama dan kantor wilayah masing-masing.
- Kisah teladan disajikan secara ringkas berdasarkan riwayat yang masyhur; rincian sanad tidak dibahas dalam bank soal latihan.
