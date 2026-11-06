"""Normalisasi dan penyeimbangan berkas tipe soal tambahan (window.BSAddTypes).

Yang dilakukan untuk setiap bab:
  * pgk     : posisi opsi benar diacak mengikuti pola seimbang sehingga enam
              kombinasi posisi kunci (A-B, A-C, A-D, B-C, B-D, C-D) terbagi
              rata dan tidak ada kombinasi yang menumpuk. Isi opsi tidak
              diubah, hanya urutannya.
  * bs      : urutan soal diacak. Komposisi kunci harus 5 Benar dan 5 Salah;
              bila tidak seimbang skrip hanya melaporkan karena membetulkannya
              berarti mengubah isi pernyataan.
  * singkat : urutan soal diacak (tidak ada posisi kunci).
  * essay   : urutan soal diacak (tidak ada posisi kunci).

Skrip bersifat idempoten dan aman dijalankan berulang.

Jalankan:
    python3 build/balance_types.py              # seluruh bab
    python3 build/balance_types.py --bab k7/dalil-naqli-aqli
    python3 build/balance_types.py --check      # periksa saja, jangan menulis
"""
from __future__ import annotations

import argparse
import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datafile  # noqa: E402
import jsobj  # noqa: E402
import typecheck  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TYPES = DATA / "types"
PAIRS = typecheck.PAIRS
COMMENT_RE = "window.BSAddTypes"


def header_comment(text: str) -> str:
    """Ambil komentar pembuka berkas agar tidak hilang saat ditulis ulang."""
    i = text.find(COMMENT_RE)
    return text[:i].rstrip() if i > 0 else ""


def targets(n: int, seed: int) -> list[tuple[int, int]]:
    """Pola seimbang pasangan posisi kunci untuk n soal pgk, urutannya diacak."""
    base = [PAIRS[i % len(PAIRS)] for i in range(n)]
    random.Random(seed).shuffle(base)
    return base


def rearrange_pgk(q: dict, tgt: tuple[int, int], rng: random.Random) -> None:
    """Susun ulang opsi sehingga dua opsi benar menempati posisi tgt."""
    opts = list(q["options"])
    ans = sorted(q["answers"])
    if len(opts) != 4 or len(ans) != 2:
        raise ValueError(f"pgk tidak sah: {len(opts)} opsi, answers={ans}")
    correct = [opts[i] for i in ans]
    wrong = [o for i, o in enumerate(opts) if i not in ans]
    rng.shuffle(correct)
    rng.shuffle(wrong)
    new_opts: list = [None] * 4
    for pos, c in zip(tgt, correct):
        new_opts[pos] = c
    wi = 0
    for i in range(4):
        if new_opts[i] is None:
            new_opts[i] = wrong[wi]
            wi += 1
    if any(o is None for o in new_opts) or sorted(new_opts) != sorted(opts):
        raise ValueError("gagal menyusun ulang opsi pgk tanpa mengubah isinya")
    q["options"] = new_opts
    q["answers"] = sorted(tgt)


def process(path: Path, check_only: bool) -> tuple[list[str], Counter]:
    text = path.read_text(encoding="utf-8")
    bab = jsobj.extract_addtypes(text)
    head = header_comment(text)
    seed = abs(hash(bab.get("id", path.stem))) % (2 ** 31)
    rng = random.Random(seed)
    notes: list[str] = []

    # acak urutan soal dalam tiap tipe
    for k in typecheck.TYPE_KEYS:
        arr = bab.get(k) or []
        rng.shuffle(arr)
        bab[k] = arr

    # seimbangkan posisi kunci pgk
    pgk = bab.get("pgk") or []
    if pgk:
        tgts = targets(len(pgk), seed)
        for q, tgt in zip(pgk, tgts):
            try:
                rearrange_pgk(q, tgt, rng)
            except ValueError as exc:
                notes.append(f"{path.name}: {exc}")

    # periksa komposisi benar/salah
    bs = bab.get("bs") or []
    vals = [q.get("answer") for q in bs if isinstance(q.get("answer"), bool)]
    if len(bs) == typecheck.N_TYPE["bs"] and vals.count(True) != 5:
        notes.append(
            f"{path.name}: bs {vals.count(True)} Benar / {vals.count(False)} Salah "
            f"(harus 5/5) — perlu perbaikan isi pernyataan"
        )

    counts = Counter({k: len(bab.get(k) or []) for k in typecheck.TYPE_KEYS})

    if not check_only and not any("tidak sah" in n or "gagal" in n for n in notes):
        datafile.write_types(path, bab, head)
        # verifikasi hasil tulis
        back = jsobj.extract_addtypes(path.read_text(encoding="utf-8"))
        if sorted(sum([[tuple(q["answers"]) for q in back.get("pgk", [])]], [])) != \
           sorted([tuple(q["answers"]) for q in bab.get("pgk", [])]):
            notes.append(f"{path.name}: hasil tulis tidak sesuai")
    return notes, counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bab", help="slug materi, contoh: k7/dalil-naqli-aqli")
    ap.add_argument("--check", action="store_true", help="periksa saja, jangan menulis")
    args = ap.parse_args()

    if not TYPES.exists():
        print("Belum ada folder data/types/")
        return 0

    files = sorted(TYPES.rglob("*.js"))
    if args.bab:
        files = [f for f in files if f.with_suffix("").as_posix().endswith(args.bab)]
    if not files:
        print("Tidak ada berkas tipe yang cocok.")
        return 0

    all_notes: list[str] = []
    grand = Counter()
    pair_grand = Counter()
    for f in files:
        notes, counts = process(f, args.check)
        all_notes.extend(notes)
        grand.update(counts)
        bab = jsobj.extract_addtypes(f.read_text(encoding="utf-8"))
        for q in bab.get("pgk", []) or []:
            pair_grand[tuple(q["answers"])] += 1
        rel = f.relative_to(TYPES).as_posix()
        print(f"{rel:<34} " + " ".join(f"{k}:{counts[k]}" for k in typecheck.TYPE_KEYS))

    print(f"\nBerkas diproses : {len(files)}{' (mode periksa)' if args.check else ''}")
    print("Total per tipe  : " + " · ".join(f"{k} {grand[k]}" for k in typecheck.TYPE_KEYS))
    print("Pasangan pgk    : " + " ".join(
        f"{chr(65+a)}{chr(65+b)}:{n}" for (a, b), n in sorted(pair_grand.items())
    ))
    if all_notes:
        print(f"\nCATATAN ({len(all_notes)}):")
        for n in all_notes[:40]:
            print("  -", n)
    return 1 if any("tidak sah" in n or "gagal" in n or "tidak sesuai" in n for n in all_notes) else 0


if __name__ == "__main__":
    sys.exit(main())
