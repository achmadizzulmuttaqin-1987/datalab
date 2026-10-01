# Catatan Pembangunan — Latihan AKG Akidah Akhlak MTs

## Ruang lingkup

- Permintaan: bahan belajar menghadapi AKG Akidah Akhlak, dalam bentuk aplikasi web luring satu berkas.
- Keputusan pengguna (via pilihan): jenjang **MTs**, cakupan **pedagogik + profesional**.
- Permintaan lanjutan: perbanyak soal menjadi **300 butir (150 pedagogik, 150 profesional)**, tanpa soal kembar, dengan **distribusi kunci merata**.
- Kebijakan keaslian: naskah AKG tidak dipublikasikan, sehingga tidak ada soal resmi yang dapat disalin. Seluruh soal ditulis orisinal mengikuti format dan kisi-kisi resmi. Aplikasi **bukan** produk resmi Kementerian Agama.

## Bank soal (kondisi akhir: 300 butir)

| Bagian | Butir | Rincian topik |
| --- | --- | --- |
| Pedagogik | 150 | 11 topik: penilaian dan evaluasi (20), desain dan pelaksanaan pembelajaran (18), kurikulum dan perencanaan (17), karakteristik peserta didik (15), teori belajar dan prinsip pembelajaran (15), refleksi dan PTK (12), pemanfaatan teknologi (11), profesi dan etika guru (11), bimbingan dan konseling (11), pengembangan potensi peserta didik (10), komunikasi dengan peserta didik (10) |
| Profesional | 150 | 13 topik: akhlak terpuji dan tercela (26), iman kepada Allah (21), malaikat-kitab-rasul (19), kisah teladan (17), hari akhir dan qadha qadar (13), akhlak dan tasawuf (12), asmaul husna (8), adab dalam kehidupan (7), pembelajaran Akidah Akhlak (7), ilmu kalam dan tokoh pemikir (6), ilmu kalam dan aliran (5), adab kontemporer (5), hakikat dan ruang lingkup (4) |
| Total | 300 | 266 pilihan ganda (130 pedagogik + 136 profesional) + 34 pilihan ganda kompleks (20 pedagogik + 14 profesional) |

Perbandingan pedagogik dan profesional dibuat 1 banding 1 sesuai permintaan. Komposisi resmi AKG jenjang MTs sendiri memuat 20 butir pedagogik dan 40 butir profesional pada setiap paket.

Setiap butir memuat: id, topik, kategori, tipe, batang soal, empat opsi, kunci, dan pembahasan. Tambahan bahan: `kisi-kisi.json` (struktur resmi AKG yang diringkas) dan `rangkuman.json` (10 seksi materi).

## Alur kerja

1. `validate_app.py` memeriksa struktur: id unik, empat opsi, opsi tidak kembar, kunci sesuai tipe, batang unik (anti kembar), pembahasan ada, tanpa tanda apostrof pada opsi, panjang opsi kunci tidak menyolok, serta keseimbangan sebaran kunci.
2. Tahap pertama (150 butir) menemukan dua masalah pada draf awal:
   - sebaran kunci PG sangat timpang (A=58, B=64, C=15, D=2) dan seluruh PGK berkunci AB;
   - 43 butir memiliki opsi kunci jauh lebih panjang daripada distraktor.
3. Perbaikan panjang opsi melalui tambalan terverifikasi (`apply_opsi_patch.py`):
   - `patch-opsi-1.json`: 23 butir pada ambang 6 kata;
   - `patch-opsi-2.json`: 20 butir pada ambang 4 kata.
   Tidak ada kunci, batang soal, atau pembahasan yang diubah pada tahap ini.
4. Tahap perluasan (150 butir baru: `PED-051` sampai `PED-150` dan `PRO-101` sampai `PRO-150`) menghasilkan 0 butir opsi timpang sejak awal karena gaya penulisan opsi sudah setara panjangnya.
5. `rebalance_keys.py` (deterministik, benih tetap) memindahkan opsi benar sehingga sebaran kunci merata:
   - sebaran akhir kunci PG: A=67, B=67, C=66, D=66;
   - pasangan kunci PGK: AB=6, AC=6, AD=6, BC=6, BD=5, CD=5.
6. `build_app.py` menyatukan CSS, JavaScript, dan seluruh data menjadi satu berkas HTML mandiri.
7. `smoke_app.mjs` memeriksa berkas hasil: blok data dapat diekstrak dan valid, jumlah soal 300 (150 pedagogik, 150 profesional), id unik, kunci sesuai tipe, semua butir beropsi empat dan berpembahasan.
8. `test_app.mjs` (jsdom) memeriksa antarmuka: 15 pemeriksaan, seluruhnya lulus pada berkas 300 butir.

## Hasil akhir

- Berkas: `Bank-Soal-AKG-Akidah-Akhlak-MTs-1file.html`, sekitar 214 KB, dibuka luring tanpa berkas pendamping.
- Pemeriksaan: `validate_app.py` lulus (0 butir opsi timpang, kunci merata), `node --check` lulus, `smoke_app.mjs` lulus, `test_app.mjs` lulus.
- Fitur: latihan per kategori/topik, pengacakan, umpan balik dan pembahasan langsung, latih ulang soal salah, penyimpanan progres di peramban, tab kunci dengan pencarian, serta cetak/simpan PDF.

## Catatan operasional

- Workspace sandbox sempat ter-reset beberapa kali. Prosedur pemulihan yang terbukti aman: `git fetch origin`, `git reset --mixed origin/arena/01a0ec50-datalab`, lalu `git ls-files --deleted -z | xargs -0 git checkout --`. Berkas baru yang belum ter-commit tetap utuh di disk dan tidak tertimpa.
- Seluruh perubahan dibangun ulang dan diverifikasi setelah pemulihan sebelum di-commit dan di-push.

## Batas dan tanggung jawab

- Soal disusun sebagai bahan latihan mandiri; tidak mewakili naskah, penilaian, atau kebijakan resmi pihak mana pun.
- Jadwal dan ketentuan resmi AKG mengikuti pengumuman Kementerian Agama dan kantor wilayah masing-masing.
- Kisah teladan disajikan secara ringkas berdasarkan riwayat yang masyhur; rincian sanad tidak dibahas dalam bank soal latihan.

## Uji antarmuka

- `build/test_app.mjs` (jsdom, opsional) memeriksa 15 hal: lima tab, tabel kisi-kisi, sepuluh seksi rangkuman, 300 butir pada tab kunci, alur latihan (soal tampil, empat opsi, umpan balik dan kunci muncul, navigasi), penyimpanan progres di localStorage, kotak pencarian, dan data 34 soal PGK.
- Hasil: seluruh 15 pemeriksaan lulus pada berkas 300 butir.
