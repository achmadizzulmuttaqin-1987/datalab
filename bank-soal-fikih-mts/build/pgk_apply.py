# -*- coding: utf-8 -*-
"""Terapkan teks opsi benar yang telah diringkas pada soal PGK.

Berkas masukan berupa JSON:
  {"slug": "k7/jujur",
   "items": [{"n": 1, "opsi": {"1": "teks baru opsi indeks 1"}}]}

Nomor `n` adalah nomor soal PGK 1-based dalam berkas tipe bab tersebut.
Kunci "opsi" adalah indeks opsi (0-3) dan HANYA boleh indeks yang menjadi
kunci benar (`answers`). Kunci jawaban, opsi salah, penjelasan, dan struktur
berkas tidak berubah.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datafile  # noqa: E402
import jsobj  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TYPES = ROOT / "data" / "types"
COMMENT_RE = "window.BSAddTypes"


def words(s: str) -> int:
    return len(re.findall(r"\S+", s or ""))


def header_comment(text: str) -> str:
    i = text.find(COMMENT_RE)
    return text[:i].rstrip() if i > 0 else ""


def main() -> int:
    if len(sys.argv) < 2:
        print("pakai: python3 build/pgk_apply.py <berkas-json> [...]")
        return 2
    ringkasan = []
    for arg in sys.argv[1:]:
        data = json.loads(Path(arg).read_text(encoding="utf-8"))
        slug = data["slug"]
        path = TYPES / ("%s.js" % slug)
        text = path.read_text(encoding="utf-8")
        bab = jsobj.extract_addtypes(text)
        head = header_comment(text)
        pgk = bab.get("pgk") or []
        berubah = 0
        for it in data["items"]:
            n = int(it["n"])
            q = pgk[n - 1]
            ans = list(q["answers"])
            opts = list(q["options"])
            for k, v in it["opsi"].items():
                idx = int(k)
                baru = str(v).strip()
                if idx not in ans:
                    raise SystemExit("GAGAL %s #%d: indeks %d bukan kunci benar %s"
                                     % (slug, n, idx, ans))
                if "'" in baru:
                    raise SystemExit("GAGAL %s #%d: mengandung apostrof" % (slug, n))
                lama = opts[idx]
                if baru.lower() == lama.strip().lower():
                    raise SystemExit("GAGAL %s #%d: teks tidak berubah" % (slug, n))
                if any(baru.lower() == o.strip().lower() for j, o in enumerate(opts) if j != idx):
                    raise SystemExit("GAGAL %s #%d: teks sama dengan opsi lain" % (slug, n))
                opts[idx] = baru
                berubah += 1
            q["options"] = opts
            wc = [words(o) for o in opts]
            benar = [wc[j] for j in ans]
            salah = [wc[j] for j in range(4) if j not in ans]
            rb, rs = sum(benar) / 2, sum(salah) / 2
            status = "OK" if rb <= rs + 1 else "MASIH-TIMPANG (%+0.1f)" % (rb - rs)
            ringkasan.append("%s #%-3d rata benar %4.1f vs salah %4.1f | %s"
                             % (slug, n, rb, rs, status))
        datafile.write_types(path, bab, head)
        back = jsobj.extract_addtypes(path.read_text(encoding="utf-8"))
        if [q.get("answers") for q in back.get("pgk", [])] != [q.get("answers") for q in pgk]:
            raise SystemExit("GAGAL %s: kunci berubah setelah tulis ulang" % slug)
        print("ditulis: data/types/%s.js — %d opsi benar diringkas" % (slug, berubah))
    print("\n".join(ringkasan))
    buruk = [r for r in ringkasan if not r.endswith("OK")]
    print("\npgk: %d butir diperbarui, %d masih perlu perhatian" % (len(ringkasan), len(buruk)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
