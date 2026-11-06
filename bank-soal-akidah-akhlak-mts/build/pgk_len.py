# -*- coding: utf-8 -*-
"""Uji ketimpangan panjang opsi pada soal PGK (pilihan ganda kompleks).

PGK memiliki dua opsi benar dan dua opsi salah. Yang diukur:
  rata benar = rata-rata jumlah kata kedua opsi benar
  rata salah = rata-rata jumlah kata kedua opsi salah
  selisih    = rata benar - rata salah

Butir disebut timpang apabila selisih >= ambang (bawaan 4 kata),
artinya opsi benar jauh lebih panjang sehingga dapat ditebak dari panjangnya.

Jalankan:
    python3 build/pgk_len.py                    # ringkasan seluruh bab
    python3 build/pgk_len.py --ambang 2         # ambang lain
    python3 build/pgk_len.py --daftar           # daftar butir timpang
    python3 build/pgk_len.py --dump k7/jujur    # rincian satu bab untuk diringkas
"""
from __future__ import annotations

import argparse
import glob
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jsobj import extract_addtypes  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TYPES = ROOT / "data" / "types"


def words(s: str) -> int:
    return len(re.findall(r"\S+", s or ""))


def slug_of(path: Path) -> str:
    return "%s/%s" % (path.parent.name, path.stem)


def scan(ambang: int):
    baris = []
    for f in sorted(glob.glob(str(TYPES / "k*" / "*.js"))):
        p = Path(f)
        bab = extract_addtypes(p.read_text(encoding="utf-8"))
        for i, q in enumerate(bab.get("pgk") or []):
            opts = q.get("options") or []
            ans = q.get("answers") or []
            if len(opts) != 4 or len(ans) != 2:
                continue
            wc = [words(opts[j]) for j in range(4)]
            benar = [wc[j] for j in ans]
            salah = [wc[j] for j in range(4) if j not in ans]
            rb = sum(benar) / len(benar)
            rs = sum(salah) / len(salah)
            baris.append(dict(slug=slug_of(p), nomor=i + 1, selisih=rb - rs,
                              rb=rb, rs=rs, maks_salah=max(salah),
                              opts=opts, answers=list(ans), wc=wc,
                              teks=q.get("text", "")))
    return baris


def dump(baris, slug: str, ambang: int = 4, hanya_timpang: bool = True) -> int:
    pilih = [b for b in baris if b["slug"] == slug]
    if not pilih:
        print("bab tidak ditemukan: %s" % slug)
        return 2
    total_bab = len(pilih)
    if hanya_timpang:
        pilih = [b for b in pilih if b["selisih"] >= ambang]
    for b in pilih:
        print("#%-2d [maks salah %d] T: %s" % (b["nomor"], b["maks_salah"],
                                               b["teks"][:110]))
        for j in b["answers"]:
            print("   B[%d](%2d): %s" % (j, b["wc"][j], b["opts"][j]))
        for j in range(4):
            if j not in b["answers"]:
                print("   S[%d](%2d): %s" % (j, b["wc"][j], b["opts"][j][:70]))
        print("   rata benar %0.1f vs rata salah %0.1f (selisih %+0.1f)"
              % (b["rb"], b["rs"], b["selisih"]))
    print("\n%d butir PGK di %s, %d timpang >= %d kata" % (total_bab, slug, len(pilih), ambang))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ambang", type=int, default=4)
    ap.add_argument("--daftar", action="store_true")
    ap.add_argument("--dump", default="")
    args = ap.parse_args()

    baris = scan(args.ambang)
    if args.dump:
        return dump(baris, args.dump, args.ambang)

    total = len(baris)
    rb = sum(b["rb"] for b in baris) / total
    rs = sum(b["rs"] for b in baris) / total
    print("total soal PGK dipindai       : %d" % total)
    print("rata-rata opsi benar          : %0.1f kata" % rb)
    print("rata-rata opsi salah          : %0.1f kata" % rs)
    for a in (2, 3, 4, 6, 10):
        n = sum(1 for b in baris if b["selisih"] >= a)
        print("  selisih >= %2d kata : %4d butir (%0.1f%%)" % (a, n, 100.0 * n / total))
    buruk = [b for b in baris if b["selisih"] >= args.ambang]
    print("perlu diringkas (ambang %d)   : %d" % (args.ambang, len(buruk)))
    if args.daftar:
        per_bab = {}
        for b in buruk:
            per_bab.setdefault(b["slug"], []).append(b["nomor"])
        for s in sorted(per_bab):
            print("  %-28s %s" % (s, ",".join(str(n) for n in per_bab[s])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
