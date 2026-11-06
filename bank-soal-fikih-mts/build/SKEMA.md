# Skema Data Soal — Bank Soal MTs

Dokumen ini menjelaskan format berkas data yang dipakai oleh kedua proyek
(`bank-soal-akidah-akhlak-mts` dan `bank-soal-fikih-mts`).

## 1. Berkas materi (sudah ada)

Satu berkas per bab di `data/k7/`, `data/k8/`, `data/k9/`:

```js
window.BSRegister({
  'id':'k9-muslim-sejati', 'grade':9, 'semester':2, 'order':21,
  'title':'Muslim Sejati', 'desc':'...', 'kd':'...',
  'questions':[ /* 50 soal pilihan ganda, type 'pg' implisit */ ]
});
```

## 2. Berkas tipe soal tambahan (baru)

Satu berkas per bab di `data/types/<slug>.js`. Slug = nama berkas materi tanpa
`.js`. Berkas ini memanggil `window.BSAddTypes` dan **tidak** boleh mengubah
berkas materi.

```js
window.BSAddTypes({
  'id':'k9-muslim-sejati',
  'pgk':[ ... ],      // 10 soal pilihan ganda kompleks (2 benar dari 4 opsi)
  'bs':[ ... ],       // 10 soal benar/salah
  'singkat':[ ... ],  // 10 soal jawaban singkat (1-4 kata)
  'essay':[ ... ]     //  5 soal essay + kunci + rubrik
});
```

Semua soal wajib `level:'HOTS'` dan memiliki `indicator`, `text`, serta
`explanation`. String memakai kutip tunggal; **hindari apostrof** di dalam teks
(gunakan `Al-Quran`, bukan `Al-Qur'an`).

### 2.1 `pgk` — pilihan ganda kompleks

Empat opsi, **tepat dua** di antaranya benar. Siswa mencentang dua kotak;
nilai penuh hanya jika keduanya tepat.

```js
{'level':'HOTS','indicator':'...',
 'text':'...',
 'options':['...','...','...','...'],
 'answers':[0,2],            // indeks opsi benar, terurut naik, panjang 2
 'explanation':'...'}
```

Aturan distribusi: enam kombinasi pasangan posisi kunci (0-1, 0-2, 0-3, 1-2,
1-3, 2-3) harus terbagi merata dalam 10 soal per bab. Gunakan
`build/pgk_pairs.py` untuk memperoleh urutan pasangan yang sudah diacak.

### 2.2 `bs` — benar/salah

```js
{'level':'HOTS','indicator':'...',
 'text':'Pernyataan: ...',
 'answer':true,              // true = Benar, false = Salah
 'explanation':'...'}
```

Aturan distribusi: tepat **5 Benar dan 5 Salah** per bab, urutan diacak.

### 2.3 `singkat` — jawaban singkat 1-4 kata

```js
{'level':'HOTS','indicator':'...',
 'text':'...',
 'answer':'tawakal',                    // jawaban utama, 1-4 kata
 'accepted':['tawakkal','tawakul'],     // varian ejaan/sinonim, opsional
 'explanation':'...'}
```

Penilaian otomatis menormalkan huruf besar/kecil, tanda baca, dan spasi, lalu
membandingkan dengan `answer` dan seluruh `accepted`. Karena itu setiap soal
wajib mencantumkan varian ejaan yang wajar. Panjang `answer` maksimal 4 kata.

### 2.4 `essay` — uraian

```js
{'level':'HOTS','indicator':'...',
 'text':'...',
 'key':'Kunci jawaban berupa uraian ...',
 'rubric':['Poin 1: ...','Poin 2: ...','Poin 3: ...'],
 'explanation':'...'}
```

Essay **tidak dinilai otomatis**. Setelah latihan dinilai, kunci dan rubrik
ditampilkan sebagai pembanding untuk penilaian mandiri.

## 3. Cara kerja aplikasi

`window.__BS.topics[id]` mendapat empat array tambahan (`pgk`, `bs`, `singkat`,
`essay`) hasil gabungan `BSRegister` + `BSAddTypes`. Soal pilihan ganda tetap
berada di `questions` agar kompatibel dengan data lama.

Di layar persiapan latihan, siswa memilih tipe soal yang ingin dilatih. Skor
hanya dihitung dari soal yang dinilai otomatis (`pg`, `pgk`, `bs`, `singkat`);
essay disajikan terpisah beserta kunci dan rubriknya.

## 4. Verifikasi

```bash
python3 build/validate.py     # periksa seluruh berkas, termasuk tipe baru
python3 build/build.py        # bangun HTML satu berkas
```
