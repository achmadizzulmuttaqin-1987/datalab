#!/usr/bin/env python3
"""Gabungkan soal tambahan dari build/topup/*.js ke berkas data yang bersangkutan."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOPUP = ROOT / "build" / "topup"


def rreplace(s, old, new):
    i = s.rindex(old)
    return s[:i] + new + s[i + len(old):]


def main():
    for p in sorted(TOPUP.glob("*.js")):
        target = ROOT / "data" / "k7" / p.name
        if not target.exists():
            target = ROOT / "data" / "k8" / p.name
        if not target.exists():
            target = ROOT / "data" / "k9" / p.name
        if not target.exists():
            print("target tidak ditemukan:", p.name)
            continue
        add = p.read_text(encoding="utf-8").strip()
        if not add:
            continue
        src = target.read_text(encoding="utf-8")
        marker = "\n]\n});"
        if marker not in src:
            print("marker tidak ditemukan:", p.name)
            continue
        new = rreplace(src, marker, ",\n" + add + marker)
        target.write_text(new, encoding="utf-8")
        n = add.count("{'level':")
        print(f"{p.name}: +{n} soal")
        p.unlink()
    return 0


if __name__ == "__main__":
    sys.exit(main())
