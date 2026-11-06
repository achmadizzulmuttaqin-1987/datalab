# -*- coding: utf-8 -*-
"""Uji ketimpangan panjang opsi: jawaban benar vs distraktor pada soal PG.

Memindai berkas register (data/k*/*.js). Melaporkan:
 - jumlah soal PG yang jawabannya lebih panjang dari distraktor terpanjang
 - ambang selisih kata yang dapat diatur (--ambang)
 - daftar butir yang perlu diringkas (--daftar)
"""
from __future__ import annotations

import argparse
import glob
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jsobj import extract_register  # noqa: E402


def words(s: str) -> int:
    return len(re.findall(r"\S+", s or ""))


def scan(root: Path, ambang: int):
    baris = []
    for f in sorted(glob.glob(str(root / "data" / "k*" / "*.js"))):
        d = extract_register(Path(f).read_text(encoding="utf-8"))
        rel = str(Path(f).relative_to(root))
        for i, q in enumerate(d.get("questions", [])):
            opts = q.get("options")
            a = q.get("answer")
            if not opts or not isinstance(a, int):
                continue
            wc = words(opts[a])
            wd = [words(o) for j, o in enumerate(opts) if j != a]
            sel = wc - max(wd)
            baris.append(dict(selisih=sel, benar=wc, maks=max(wd),
                              rata=sum(wd) / len(wd), berkas=rel, nomor=i + 1,
                              teks=opts[a]))
    return baris


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ambang", type=int, default=4,
                    help="selisih kata minimal agar butir dilaporkan (bawaan 4)")
    ap.add_argument("--daftar", action="store_true", help="cetak daftar butir")
    ap.add_argument("--berkas", default="", help="batasi pada satu berkas register")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    baris = scan(root, args.ambang)
    if args.berkas:
        baris = [b for b in baris if b["berkas"].endswith(args.berkas)]
    total = len(baris)
    timpang = [b for b in baris if b["selisih"] >= args.ambang]
    for amb in (2, 3, 4, 5, 8, 12):
        n = sum(1 for b in baris if b["selisih"] >= amb)
        print("  selisih >= %2d kata : %4d butir (%0.1f%%)" % (amb, n, 100.0 * n / total))
    print("total soal PG dipindai : %d" % total)
    print("perlu diringkas (ambang %d) : %d" % (args.ambang, len(timpang)))
    if args.daftar:
        timpang.sort(key=lambda b: -b["selisih"])
        for b in timpang:
            print("  %+3d | benar %2d maks %2d | %s #%d | %s"
                  % (b["selisih"], b["benar"], b["maks"], b["berkas"], b["nomor"],
                     b["teks"]))
    return 1 if timpang else 0


if __name__ == "__main__":
    raise SystemExit(main())
