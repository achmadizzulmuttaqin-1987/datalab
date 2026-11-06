"""Perbarui build/PROGRESS.md sesuai berkas tipe yang sudah selesai ditulis.

Jalankan dari direktori proyek: python3 build/progress.py
Bagian "Status" ditulis ulang dari data/index.js + isi data/types/, sehingga
jumlah bab yang tercentang selalu mengikuti keadaan berkas yang sebenarnya.
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jsobj import extract_index  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    idx = extract_index((ROOT / "data" / "index.js").read_text(encoding="utf-8"))
    types_dir = ROOT / "data" / "types"
    have = {p.stem for p in types_dir.glob("k*/*.js")}

    def slug(entry: dict) -> str:
        return entry["file"][:-3].split("/")[-1]

    lines = []
    done = 0
    for e in idx:
        ok = slug(e) in have
        done += 1 if ok else 0
        lines.append(f"[{'x' if ok else ' '}] {e['file'][:-3]} — {e.get('title', e['id'])}")

    p = ROOT / "build" / "PROGRESS.md"
    s = p.read_text(encoding="utf-8")
    a = s.index("## Status — Fikih MTs (30 bab)")
    b = s.index("## Kemajuan terakhir")
    s = s[:a] + "## Status — Fikih MTs (30 bab)\n\n" + "\n".join(lines) + "\n\n" + s[b:]
    p.write_text(s, encoding="utf-8")
    print(f"bab selesai: {done} / {len(idx)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
