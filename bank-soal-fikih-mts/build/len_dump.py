# -*- coding: utf-8 -*-
"""Cetak ringkas soal PG: nomor, panjang distraktor, batang, dan opsi jawaban benar.

Pakai: python3 build/len_dump.py <bagian-slug> <jumlah> <mulai>
Contoh: python3 build/len_dump.py k7/hormat-taat 25 0
"""
import sys
import glob
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jsobj import extract_register  # noqa: E402


def words(s):
    return len(re.findall(r"\S+", s or ""))


root = Path(__file__).resolve().parent.parent
slug = sys.argv[1] if len(sys.argv) > 1 else ""
jumlah = int(sys.argv[2]) if len(sys.argv) > 2 else 25
mulai = int(sys.argv[3]) if len(sys.argv) > 3 else 0

semua = sorted(glob.glob(str(root / "data" / "k*" / "*.js")))
if slug:
    semua = [f for f in semua if slug in f]

n = 0
for f in semua:
    d = extract_register(Path(f).read_text(encoding="utf-8"))
    for i, q in enumerate(d.get("questions", [])):
        if i < mulai:
            continue
        opts = q.get("options")
        a = q.get("answer")
        if not opts or not isinstance(a, int):
            continue
        wd = [words(o) for j, o in enumerate(opts) if j != a]
        wc = words(opts[a])
        if wc - max(wd) < 4:
            continue  # sudah setara, tidak perlu diringkas
        t = re.sub(r"\s+", " ", q.get("text", "")).strip()
        st = re.sub(r"\s+", " ", str(q.get("stimulus") or "")).strip()
        print("#%d [maks %d] T: %s%s" % (i + 1, max(wd), ("S: " + st[:80] + " | ") if st else "", t[:150]))
        print("   B(%d): %s" % (wc, opts[a]))
        n += 1
        if n >= jumlah:
            raise SystemExit(0)
