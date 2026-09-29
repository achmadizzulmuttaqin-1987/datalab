"""Validasi seluruh file data soal tanpa membangun output.

Periksa: jumlah soal per materi, kunci jawaban, jumlah opsi, pembahasan,
apostrof yang merusak string JS, dan duplikasi batang soal.
Jalankan: python3 build/validate.py
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jsobj  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
APOS = re.compile(r"[A-Za-z]'[A-Za-z]")


def main() -> int:
    index = jsobj.extract_index((ROOT / "data" / "index.js").read_text(encoding="utf-8"))
    errors = []
    rows = []
    total = 0
    seen_global = {}

    for meta in index:
        p = ROOT / "data" / meta["file"]
        t = p.read_text(encoding="utf-8")
        if APOS.search(t):
            errors.append(f"{meta['file']}: apostrof di dalam string ({APOS.findall(t)[:3]})")
        obj = jsobj.extract_register(t)
        qs = obj.get("questions", [])
        total += len(qs)
        stem = Counter()
        dist = Counter()
        for i, q in enumerate(qs, 1):
            tag = f"{meta['file']} #{i}"
            opts = q.get("options", [])
            a = q.get("answer")
            if len(opts) != 4:
                errors.append(f"{tag}: jumlah opsi {len(opts)}")
            if not (isinstance(a, int) and not isinstance(a, bool) and 0 <= a < len(opts)):
                errors.append(f"{tag}: answer tidak valid ({a})")
            else:
                dist[a] += 1
            if not q.get("explanation"):
                errors.append(f"{tag}: pembahasan kosong")
            if q.get("level") not in ("HOTS", "MOTS", "LOTS"):
                errors.append(f"{tag}: level tidak valid")
            txt = (q.get("text") or "").strip()
            if not txt:
                errors.append(f"{tag}: teks soal kosong")
            stem[txt[:40]] += 1
            g = re.sub(r"\s+", " ", txt)[:70]
            if g in seen_global:
                errors.append(f"{tag}: batang soal sama dengan {seen_global[g]}")
            seen_global[g] = tag
        dup = {k: v for k, v in stem.items() if v > 1}
        if dup:
            errors.append(f"{meta['file']}: batang soal mirip {dup}")
        if len(qs) != 50:
            errors.append(f"{meta['file']}: {len(qs)} soal (harus 50)")
        rows.append((meta["id"], obj.get("grade"), obj.get("semester"), len(qs),
                     dict(sorted(dist.items()))))

    disk = {str(p.relative_to(ROOT / "data")) for p in (ROOT / "data").glob("k*/*.js")}
    listed = {m["file"] for m in index}
    for f in sorted(listed - disk):
        errors.append(f"index menunjuk file yang tidak ada: {f}")
    for f in sorted(disk - listed):
        errors.append(f"file tidak terdaftar di index: {f}")

    print(f"{'materi':<26}{'kl':>3}{'sm':>3}{'soal':>6}   distribusi kunci")
    for r in rows:
        print(f"{r[0]:<26}{r[1]:>3}{r[2]:>3}{r[3]:>6}   {r[4]}")
    print(f"\nMateri: {len(rows)}   Total soal: {total}")
    if errors:
        print(f"\nERROR ({len(errors)}):")
        for e in errors[:60]:
            print("  -", e)
        return 1
    print("\nSemua pemeriksaan lulus.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
