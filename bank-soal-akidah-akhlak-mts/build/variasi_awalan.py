"""Meragamkan awalan batang soal yang berulang (temuan tipe B pada dup_check).

Isi dan kunci soal tidak diubah; hanya kalimat pembuka yang diberi variasi agar
tidak ada dua soal yang berbagi 40 karakter awalan. Anggota pertama setiap
kelompok dibiarkan tetap, anggota berikutnya diberi pembuka yang berbeda.

Strategi:
  * soal pgk / bs / essay  -> ditambah kalimat pengantar (lead-in) yang cocok
    untuk soal berbasis pernyataan atau uraian;
  * soal jawaban singkat   -> kepala definisinya diparafrase (mis. "Nama Allah
    yang menunjukkan bahwa Allah ..." -> "Asma Allah yang menunjukkan bahwa
    Allah ...") supaya tetap terbaca sebagai soal definisi.

Jalankan dari direktori proyek:  python3 build/variasi_awalan.py
"""
import sys, collections, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'build'))
from jsobj import extract_addtypes
import datafile

BASE = ROOT / 'data' / 'types'

IMPERATIF = re.compile(r'^(perhatikan|cermati|bacalah|pahami|simaklah|telitilah)\b', re.I)

# kalimat pengantar utuh (untuk batang soal yang bukan kalimat perintah)
KALIMAT = [
    'Perhatikan keterangan berikut. ',
    'Cermati uraian berikut ini. ',
    'Bacalah keterangan berikut. ',
    'Perhatikan pernyataan berikut. ',
    'Cermati beberapa pernyataan berikut. ',
    'Simak uraian berikut ini. ',
    'Perhatikan cuplikan diskusi berikut. ',
    'Cermati cuplikan bacaan berikut. ',
    'Perhatikan hasil diskusi berikut. ',
    'Bacalah cuplikan berikut. ',
    'Cermati pernyataan seorang guru berikut. ',
    'Perhatikan tulisan berikut ini. ',
    'Simak pernyataan dalam forum berikut. ',
    'Cermati catatan seorang murid berikut. ',
    'Perhatikan pengumuman berikut. ',
    'Cermati kutipan bacaan berikut. ',
    'Perhatikan ringkasan materi berikut. ',
    'Simak hasil pengamatan berikut. ',
    'Cermati situasi yang diuraikan berikut. ',
    'Perhatikan laporan kegiatan berikut. ',
    'Bacalah kutipan berikut ini. ',
    'Cermati dialog singkat berikut. ',
    'Perhatikan catatan kegiatan berikut. ',
    'Simak penjelasan seorang ustaz berikut. ',
    'Perhatikan lembar kegiatan murid berikut. ',
    'Cermati rangkuman pembelajaran berikut. ',
    'Perhatikan hasil wawancara berikut. ',
]
# anak kalimat pengantar (untuk batang soal yang diawali kata perintah)
ANAK = [
    'Dalam diskusi kelas, ',
    'Pada kegiatan pembelajaran, ',
    'Dalam sebuah kajian, ',
    'Saat diskusi kelompok, ',
    'Dalam majelis taklim, ',
    'Pada pesantren kilat, ',
    'Ketika mengikuti kajian, ',
    'Dalam forum remaja masjid, ',
    'Saat kegiatan mentoring, ',
    'Pada kegiatan literasi, ',
    'Dalam kegiatan keagamaan, ',
    'Saat menjadi panitia kegiatan, ',
    'Pada peringatan hari besar Islam, ',
    'Ketika mendampingi adik kelas, ',
    'Dalam sebuah pelatihan, ',
    'Saat mengikuti pengajian, ',
    'Pada kegiatan bakti sosial, ',
    'Dalam rapat pengurus kelas, ',
    'Saat berkunjung ke panti asuhan, ',
    'Pada kegiatan ramadan di madrasah, ',
    'Dalam pelatihan kepemimpinan pelajar, ',
    'Saat mengikuti kegiatan pramuka, ',
    'Pada dialog antarumat di kampungnya, ',
]
# parafrase kepala definisi untuk soal jawaban singkat dan kepala soal pgk
HEADS = [
    (r'^Dua pernyataan yang tepat tentang ', [
        'Dua pernyataan berikut yang tepat mengenai ',
        'Dua keterangan yang tepat tentang ',
        'Dua pernyataan yang benar tentang ',
        'Dua simpulan yang tepat tentang ',
        'Dua pernyataan yang tepat mengenai ',
        'Dua penilaian yang tepat tentang ',
        'Dua pernyataan yang sesuai tentang ',
        'Dua pernyataan berikut yang benar mengenai ',
        'Dua simpulan berikut yang tepat mengenai ',
        'Dua keterangan berikut yang benar tentang ',
    ]),
    (r'^Nama Allah yang menunjukkan bahwa Allah ', [
        'Asma Allah yang menunjukkan bahwa Allah ',
        'Nama Allah yang bermakna bahwa Allah ',
        'Salah satu nama Allah yang menunjukkan bahwa Allah ',
        'Nama Allah yang memiliki arti bahwa Allah ',
        'Nama Allah yang mengandung makna bahwa Allah ',
        'Asmaul Husna yang menunjukkan bahwa Allah ',
        'Nama Allah yang menjadi petunjuk bahwa Allah ',
        'Nama Allah yang menegaskan bahwa Allah ',
    ]),
    (r'^Nama Allah yang menunjukkan ', [
        'Asma Allah yang menunjukkan ',
        'Nama Allah yang menegaskan ',
        'Salah satu nama Allah yang menunjukkan ',
    ]),
    (r'^Sifat wajib bagi Allah yang berarti ', [
        'Sifat wajib Allah yang berarti ',
        'Salah satu sifat wajib bagi Allah yang berarti ',
        'Sifat wajib bagi Allah yang bermakna ',
    ]),
    (r'^Bacaan yang diucapkan oleh seorang muslim ', [
        'Lafal yang diucapkan oleh seorang muslim ',
        'Ucapan yang dilafalkan oleh seorang muslim ',
        'Kalimat yang diucapkan oleh seorang muslim ',
    ]),
    (r'^Kebaikan dan manfaat yang terus berlangsung ', [
        'Kebaikan serta manfaat yang terus berlangsung ',
        'Manfaat dan kebaikan yang terus berlangsung ',
    ]),
    (r'^Sebutan bagi penduduk Madinah yang ', [
        'Sebutan untuk penduduk Madinah yang ',
        'Julukan bagi penduduk Madinah yang ',
    ]),
]


def lower_first(s):
    return s[:1].lower() + s[1:]


def kandidat(asli, tipe):
    """Hasilkan calon batang soal baru, diurutkan dari yang paling cocok."""
    out = []
    for pola, varian in HEADS:
        m = re.match(pola, asli)
        if m:
            sisa = asli[m.end():]
            out.extend(v + sisa for v in varian)
            break
    if tipe != 'singkat':
        if IMPERATIF.match(asli):
            out.extend(p + lower_first(asli) for p in ANAK)
        else:
            out.extend(p + asli for p in KALIMAT)
            out.extend(p + lower_first(asli) for p in ANAK)
    else:
        if not IMPERATIF.match(asli):
            out.extend(p + asli for p in KALIMAT[:3])
    return out


def main(contoh_max=8):
    data = {}
    for f in sorted(BASE.rglob('*.js')):
        src = f.read_text(encoding='utf-8')
        data[f] = (src.split('window.BSAddTypes')[0], extract_addtypes(src))

    kel = collections.defaultdict(list)
    for f, (head, d) in data.items():
        for k in ('pgk', 'bs', 'singkat', 'essay'):
            for i, q in enumerate(d[k]):
                kel[q['text'].strip().lower()[:40]].append((f, k, i))

    dipakai = set(kel.keys())

    ubah, gagal, contoh = 0, [], []
    for awalan, anggota in sorted(kel.items(), key=lambda x: -len(x[1])):
        if len(anggota) < 2:
            continue
        for f, k, i in anggota[1:]:
            q = data[f][1][k][i]
            asli = q['text'].strip()
            baru = None
            for calon in kandidat(asli, k):
                pre = calon.strip().lower()[:40]
                if pre in dipakai or pre == awalan:
                    continue
                baru = calon
                dipakai.add(pre)
                break
            if baru is None:
                gagal.append((str(f.relative_to(BASE)), k, i + 1, asli[:60]))
                continue
            q['text'] = baru
            ubah += 1
            if len(contoh) < contoh_max:
                contoh.append((str(f.relative_to(BASE))[:-3], k, i + 1, asli[:60], baru[:95]))

    for f, (head, d) in data.items():
        datafile.write_types(f, d, header_comment=head)

    print('batang soal diragamkan:', ubah, '| gagal:', len(gagal))
    for g in gagal:
        print('  GAGAL', g)
    for c in contoh:
        print('  %s %s#%d\n    lama: %s\n    baru: %s' % c)


if __name__ == '__main__':
    main()
