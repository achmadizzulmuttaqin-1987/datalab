#!/usr/bin/env python3
"""Bangun aplikasi latihan AKG Akidah Akhlak MTs menjadi satu berkas HTML mandiri.

Seluruh aset (CSS, JavaScript, data soal, kisi-kisi, rangkuman) disatukan sehingga
hasil dapat dibuka secara luring tanpa koneksi internet dan tanpa berkas pendamping.
"""
import json
import glob
import os
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")
DATA = os.path.join(BUILD, "data")
OUT = os.path.join(ROOT, "Bank-Soal-AKG-Akidah-Akhlak-MTs-1file.html")

TEMPLATE = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Latihan AKG Akidah Akhlak MTs</title>
<meta name="description" content="Aplikasi latihan mandiri AKG Akidah Akhlak MTs: soal pedagogik dan profesional, kunci, pembahasan, serta rangkuman materi. Berkas tunggal, dapat dipakai luring.">
<style>
{css}
</style>
</head>
<body>
<header class="hero">
  <div class="wrap">
    <h1>Latihan AKG &middot; Akidah Akhlak MTs</h1>
    <p class="sub">{sub}</p>
    <div class="badges">
      <span class="badge">{n_soal} soal latihan</span>
      <span class="badge">{n_ped} pedagogik</span>
      <span class="badge">{n_pro} profesional</span>
      <span class="badge">kunci + pembahasan</span>
      <span class="badge">rangkuman materi</span>
      <span class="badge">berkas tunggal, luring</span>
    </div>
    <div class="disclaimer"><strong>Catatan penting.</strong> Naskah asli AKG tidak dipublikasikan sehingga tidak ada soal resmi tahun lalu yang dapat disalin. Seluruh soal di aplikasi ini adalah <em>soal latihan yang ditulis orisinal</em> mengikuti format, komposisi, dan kisi-kisi resmi AKG madrasah. Aplikasi ini bukan produk resmi Kementerian Agama.</div>
  </div>
</header>
<nav class="tabs" aria-label="Menu utama">
  <div class="wrap" role="tablist">
    <button class="tab" id="btn-tab-petunjuk" aria-selected="true" role="tab">Petunjuk</button>
    <button class="tab" id="btn-tab-kisi" aria-selected="false" role="tab">Kisi-Kisi AKG</button>
    <button class="tab" id="btn-tab-materi" aria-selected="false" role="tab">Rangkuman Materi</button>
    <button class="tab" id="btn-tab-latihan" aria-selected="false" role="tab">Latihan Soal</button>
    <button class="tab" id="btn-tab-kunci" aria-selected="false" role="tab">Kunci &amp; Pembahasan</button>
  </div>
</nav>
<main>
  <section id="tab-petunjuk">
    <div class="card">
      <h2 class="sec">Selamat belajar, Bapak/Ibu Guru</h2>
      <p class="lead" id="meta-stat"></p>
      <ol>
        <li>Baca <strong>Kisi-Kisi AKG</strong> untuk memahami komposisi dan aspek yang diuji.</li>
        <li>Pelajari <strong>Rangkuman Materi</strong> sebagai bekal konsep dasar.</li>
        <li>Kerjakan <strong>Latihan Soal</strong> per kategori atau per topik. Setiap jawaban langsung diberi umpan balik dan pembahasan.</li>
        <li>Gunakan tombol <strong>Latih soal yang salah</strong> untuk menuntaskan soal yang belum tepat.</li>
        <li>Periksa <strong>Kunci &amp; Pembahasan</strong> untuk meninjau ulang seluruh soal, dan tekan cetak untuk menyimpannya sebagai PDF.</li>
      </ol>
      <p class="small muted">Progres jawaban tersimpan otomatis di peramban ini (tanpa internet). Tombol <em>Hapus riwayat</em> pada halaman latihan akan mengosongkannya.</p>
    </div>
    <div class="card">
      <h2 class="sec">Sumber dan dasar penyusunan</h2>
      <ul class="clean small">
        <li>Struktur dan komposisi AKG madrasah mengacu pada juknis serta kisi-kisi Direktorat Jenderal Pendidikan Islam Kementerian Agama: kompetensi pedagogik dan profesional, 60 butir per paket, 120 menit (jenjang MTs/MA: 20 butir pedagogik dan 40 butir profesional).</li>
        <li>Aspek kompetensi pedagogik mengacu pada Permendiknas Nomor 16 Tahun 2007 tentang Standar Kualifikasi Akademik dan Kompetensi Guru.</li>
        <li>Kurikulum madrasah mengacu pada KMA Nomor 183 Tahun 2019 tentang Kurikulum PAI dan Bahasa Arab serta KMA Nomor 347 Tahun 2022 tentang Pedoman Implementasi Kurikulum Merdeka pada Madrasah.</li>
        <li>Materi Akidah Akhlak mencakup akidah, akhlak, adab, kisah teladan, serta ilmu kalam pada jenjang MTs.</li>
      </ul>
      <p class="small muted">Soal disusun sebagai bahan latihan mandiri dan tidak mewakili naskah, kebijakan, atau penilaian resmi pihak mana pun. Untuk jadwal dan ketentuan resmi AKG, silakan merujuk pada pengumuman Kementerian Agama dan kantor wilayah masing-masing.</p>
    </div>
  </section>
  <section id="tab-kisi" hidden>
    <div class="card"><h2 class="sec">Kisi-Kisi dan Struktur AKG</h2><div id="kisi-body"></div></div>
  </section>
  <section id="tab-materi" hidden>
    <div class="card"><h2 class="sec">Rangkuman Materi</h2><div id="materi-body"></div></div>
  </section>
  <section id="tab-latihan" hidden>
    <div class="card">
      <h2 class="sec">Latihan Soal</h2>
      <div id="quiz-setup">
        <p class="lead">Pilih cakupan latihan, lalu mulai mengerjakan. Soal ditampilkan satu per satu dengan umpan balik langsung.</p>
        <div class="quizbar">
          <label class="field">Kategori
            <select id="sel-kat">
              <option value="semua">Semua kategori</option>
              <option value="pedagogik">Pedagogik</option>
              <option value="profesional">Profesional Akidah Akhlak</option>
            </select>
          </label>
          <label class="field">Topik
            <select id="sel-topik"></select>
          </label>
          <label class="field" style="flex-direction:row;align-items:center;gap:8px">
            <input type="checkbox" id="chk-acak" checked> Acak urutan soal
          </label>
          <button class="btn" id="btn-mulai">Mulai Latihan</button>
          <button class="btn ghost" id="btn-salah">Latih soal yang salah</button>
          <button class="btn ghost" id="btn-reset">Hapus riwayat</button>
        </div>
        <p class="small muted" id="prog-chip"></p>
      </div>
      <div id="quiz-area" hidden></div>
      <div id="quiz-result" hidden></div>
    </div>
  </section>
  <section id="tab-kunci" hidden>
    <div class="card"><h2 class="sec">Kunci Jawaban dan Pembahasan</h2><div id="kunci-body"></div></div>
  </section>
</main>
<footer>
  <p>Disusun untuk latihan mandiri guru madrasah. Seluruh soal merupakan karya orisinal; dilarang memperjualbelikan tanpa izin penyusun. Dibangun {tanggal}.</p>
  <p class="noprint">Tips: tekan Ctrl+P (atau tombol cetak pada halaman rangkuman/kunci) untuk menyimpan bagian mana pun sebagai PDF.</p>
</footer>
<script id="akg-data" type="application/json">
{data}
</script>
<script>
window.__AKG_DATA__ = JSON.parse(document.getElementById('akg-data').textContent);
</script>
<script>
{js}
</script>
</body>
</html>
"""


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    # muat soal
    items = []
    for path in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        name = os.path.basename(path)
        if name in ("kisi-kisi.json", "rangkuman.json"):
            continue
        obj = load_json(path)
        for it in obj["items"]:
            it.setdefault("kategori", obj["kategori"])
        items.extend(obj["items"])
    n_ped = sum(1 for i in items if i["kategori"] == "pedagogik")
    n_pro = sum(1 for i in items if i["kategori"] == "profesional")

    kisi = load_json(os.path.join(DATA, "kisi-kisi.json"))
    rangkuman = load_json(os.path.join(DATA, "rangkuman.json"))

    meta = {
        "judul": "Latihan AKG Akidah Akhlak MTs",
        "jumlah": len(items),
        "pedagogik": n_ped,
        "profesional": n_pro,
        "dibangun": datetime.date.today().isoformat(),
    }
    data = {"meta": meta, "kisi": kisi, "rangkuman": rangkuman, "soal": items}
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    data_json = data_json.replace("</", "<\\/")

    with open(os.path.join(BUILD, "app.css"), encoding="utf-8") as fh:
        css = fh.read()
    with open(os.path.join(BUILD, "app.js"), encoding="utf-8") as fh:
        js = fh.read()

    sub = ("%d soal latihan bergaya AKG (%d pedagogik dan %d profesional) beserta kunci, "
           "pembahasan, dan rangkuman materi untuk guru Akidah Akhlak MTs."
           % (len(items), n_ped, n_pro))

    html = TEMPLATE.format(
        css=css,
        js=js,
        data=data_json,
        sub=sub,
        n_soal=len(items),
        n_ped=n_ped,
        n_pro=n_pro,
        tanggal=datetime.date.today().strftime("%d-%m-%Y"),
    )

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)

    size_kb = os.path.getsize(OUT) / 1024
    print("Tersimpan :", os.path.relpath(OUT, ROOT))
    print("Ukuran    : %.1f KB" % size_kb)
    print("Jumlah    : %d soal (%d pedagogik + %d profesional)" % (len(items), n_ped, n_pro))


if __name__ == "__main__":
    main()
