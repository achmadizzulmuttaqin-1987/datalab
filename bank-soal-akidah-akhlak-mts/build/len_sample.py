# -*- coding: utf-8 -*-
"""Cetak contoh soal PG beserta panjang setiap opsinya (untuk audit ketimpangan)."""
import sys
import glob
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jsobj import extract_register  # noqa: E402


def words(s):
    return len(re.findall(r"\S+", s or ""))


root = Path(__file__).resolve().parent.parent
berkas = sys.argv[1] if len(sys.argv) > 1 else ""
jumlah = int(sys.argv[2]) if len(sys.argv) > 2 else 3
mulai = int(sys.argv[3]) if len(sys.argv) > 3 else 0

semua = sorted(glob.glob(str(root / "data" / "k*" / "*.js")))
if berkas:
    semua = [f for f in semua if berkas in f]

cw = []
dw = []
for f in semua:
    d = extract_register(Path(f).read_text(encoding="utf-8"))
    for q in d.get("questions", []):
        opts = q.get("options")
        a = q.get("answer")
        if not opts or not isinstance(a, int):
            continue
        cw.append(words(opts[a]))
        dw += [words(o) for j, o in enumerate(opts) if j != a]

print("rata-rata panjang jawaban benar  : %0.1f kata (maks %d, min %d)"
      % (sum(cw) / len(cw), max(cw), min(cw)))
print("rata-rata panjang jawaban salah  : %0.1f kata (maks %d, min %d)"
      % (sum(dw) / len(dw), max(dw), min(dw)))

ditampilkan = 0
for f in semua:
    d = extract_register(Path(f).read_text(encoding="utf-8"))
    qs = d.get("questions", [])
    for i, q in enumerate(qs):
        if i < mulai:
            continue
        opts = q.get("options")
        a = q.get("answer")
        if not opts:
            continue
        print("\n=== %s #%d (%s) ===" % (f.split("/data/")[1][:-3], i + 1, d.get("title", "")))
        print("  T: %s" % q.get("text", "")[:220])
        if q.get("stimulus"):
            print("  S: %s" % str(q["stimulus"])[:120])
        for j, o in enumerate(opts):
            tanda = "BENAR" if j == a else "salah"
            print("  [%d %s %2d kata] %s" % (j, tanda, words(o), o))
        ditampilkan += 1
        if ditampilkan >= jumlah:
            raise SystemExit(0)
