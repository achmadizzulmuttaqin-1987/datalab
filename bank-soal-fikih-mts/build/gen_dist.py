"""Pembangkit distribusi kunci jawaban untuk tipe soal baru.

Untuk `pgk` (pilihan ganda kompleks, 2 benar dari 4 opsi) ada enam kombinasi
posisi kunci: (0,1) (0,2) (0,3) (1,2) (1,3) (2,3). Untuk 10 soal per bab,
setiap kombinasi dipakai merata lalu sisanya diacak, dan urutannya diacak.

Untuk `bs` (benar/salah) dihasilkan tepat 5 Benar dan 5 Salah dengan urutan
yang diacak.

Jalankan:
    python3 build/gen_dist.py            # cetak rencana untuk seluruh bab
    python3 build/gen_dist.py --bab k9/muslim-sejati
    python3 build/gen_dist.py --json     # keluaran JSON
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jsobj  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
N_PGK = 10
N_BS = 10
N_SINGKAT = 10
N_ESSAY = 5


def pgk_plan(n: int, seed: int) -> list[tuple[int, int]]:
    """Susunan pasangan posisi kunci untuk n soal pgk, merata lalu diacak."""
    base = [PAIRS[i % len(PAIRS)] for i in range(n)]
    # untuk n=10: 6 kombinasi muncul sekali, 4 sisanya mengulang kombinasi awal
    rng = random.Random(seed)
    rng.shuffle(base)
    return base


def bs_plan(n: int, seed: int) -> list[bool]:
    """Susunan kunci benar/salah untuk n soal, seimbang lalu diacak."""
    half = n // 2
    base = [True] * half + [False] * (n - half)
    rng = random.Random(seed + 1)
    rng.shuffle(base)
    return base


def plan_for(topic_id: str) -> dict:
    seed = abs(hash(topic_id)) % (2 ** 31)
    return {
        "id": topic_id,
        "seed": seed,
        "pgk_pairs": [list(p) for p in pgk_plan(N_PGK, seed)],
        "bs_keys": bs_plan(N_BS, seed),
        "counts": {"pgk": N_PGK, "bs": N_BS, "singkat": N_SINGKAT, "essay": N_ESSAY},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bab", help="slug materi, contoh: k9/muslim-sejati")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    index = jsobj.extract_index((ROOT / "data" / "index.js").read_text(encoding="utf-8"))
    rows = []
    for meta in index:
        slug = meta["file"][:-3]
        if args.bab and slug != args.bab:
            continue
        rows.append(plan_for(meta["id"]))

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return 0

    for r in rows:
        pairs = " ".join(f"{chr(65+a)}{chr(65+b)}" for a, b in r["pgk_pairs"])
        bs = "".join("B" if x else "S" for x in r["bs_keys"])
        print(f"{r['id']:<28} pgk: {pairs}   bs: {bs}")
    if not rows:
        print("tidak ada bab yang cocok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
