# -*- coding: utf-8 -*-
"""Terapkan teks opsi jawaban benar yang telah diringkas pada soal PG.

Berkas masukan berupa JSON:
  {"slug": "k7/adab-berpakaian",
   "items": [{"n": 1, "text": "opsi benar yang baru"}]}

Nomor `n` adalah nomor soal 1-based dalam berkas register.
Skrip ini hanya mengganti teks opsi yang menjadi kunci (`answer`);
indeks kunci, opsi lain, penjelasan, dan struktur berkas tidak berubah.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datafile  # noqa: E402


def words(s: str) -> int:
    return len(re.findall(r"\S+", s or ""))


def main() -> int:
    if len(sys.argv) < 2:
        print("pakai: python3 build/shorten_apply.py <berkas-json> [...]")
        return 2
    ringkasan = []
    for arg in sys.argv[1:]:
        data = json.loads(Path(arg).read_text(encoding="utf-8"))
        slug = data["slug"]
        obj, head, footer = datafile.read_topic("%s.js" % slug)
        qs = obj["questions"]
        berubah = 0
        for it in data["items"]:
            n = int(it["n"])
            baru = it["text"].strip()
            q = qs[n - 1]
            a = q["answer"]
            opts = list(q["options"])
            if "'" in baru:
                raise SystemExit("GAGAL %s #%d: mengandung apostrof" % (slug, n))
            lain = [o for j, o in enumerate(opts) if j != a]
            if any(baru.strip().lower() == o.strip().lower() for o in lain):
                raise SystemExit("GAGAL %s #%d: teks sama dengan opsi lain" % (slug, n))
            lama = opts[a]
            wb, ws = words(baru), max(words(o) for o in lain)
            rata = sum(words(o) for o in lain) / len(lain)
            opts[a] = baru
            q["options"] = opts
            berubah += 1
            status = "OK"
            if wb > ws:
                status = "MASIH-LEBIH-PANJANG (%d>%d)" % (wb, ws)
            elif wb > rata + 4:
                status = "AGAK-PANJANG (%d vs rata %0.1f)" % (wb, rata)
            ringkasan.append("%s #%-3d %3d kata -> %2d kata | distraktor maks %2d rata %4.1f | %s"
                             % (slug, n, words(lama), wb, ws, rata, status))
        datafile.write_topic("%s.js" % slug, head, qs, footer)
        print("ditulis: data/%s.js — %d opsi jawaban benar diringkas" % (slug, berubah))
    print("\n".join(ringkasan))
    buruk = [r for r in ringkasan if not r.endswith("OK")]
    print("\nringkas: %d butir diperbarui, %d masih perlu perhatian"
          % (len(ringkasan), len(buruk)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
