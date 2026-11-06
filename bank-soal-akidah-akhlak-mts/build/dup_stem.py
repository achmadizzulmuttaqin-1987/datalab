"""Cari batang soal tipe baru yang berbagi awalan (bawaan 40 karakter) antarbab.

Jalankan: python3 build/dup_stem.py [panjang_awalan]
Pemeriksaan ini melampaui validate.py yang hanya mencari duplikat teks penuh,
karena batang yang berbeda isi namun berbagi awalan umum (mis. "Perhatikan
empat pernyataan berikut ...") akan terjaring pemeriksaan duplikat batang.
"""
from __future__ import annotations
import re, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from jsobj import extract_addtypes

ROOT = Path(__file__).resolve().parent.parent
KEYS = ("pgk", "bs", "singkat", "essay")


def norm(t: str) -> str:
    return re.sub(r"\s+", " ", t or "").strip()


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    groups = defaultdict(list)
    for f in sorted((ROOT / "data" / "types").glob("k*/*.js")):
        d = extract_addtypes(f.read_text(encoding="utf-8"))
        for k in KEYS:
            for i, q in enumerate(d.get(k, []) or [], 1):
                t = norm(q.get("text", ""))
                if t:
                    groups[t[:n]].append(f"{f.parent.name}/{f.stem} {k}#{i}")
    dups = {k: v for k, v in groups.items() if len(v) > 1}
    if not dups:
        print(f"Tidak ada batang soal yang berbagi {n} karakter awalan.")
        return 0
    print(f"DUPLIKAT AWALAN {n} KARAKTER ({len(dups)} kelompok):")
    for k, v in sorted(dups.items()):
        print(f"\n  '{k}...'")
        for tag in v:
            print(f"    - {tag}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
