#!/usr/bin/env python3
"""Seimbangkan sebaran kunci jawaban secara deterministik.

- PG : memindahkan opsi benar ke posisi A/B/C/D yang jumlahnya merata.
- PGK: memindahkan pasangan opsi benar ke kombinasi AB/AC/AD/BC/BD/CD yang merata.
Isi opsi, batang soal, dan pembahasan tidak diubah; hanya urutan opsi dan indeks kunci.
"""
import glob
import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "build", "data")
LETTERS = ["A", "B", "C", "D"]
SEED = 20241001


def load_all():
    files = []
    for path in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        name = os.path.basename(path)
        if name in ("kisi-kisi.json", "rangkuman.json"):
            continue
        with open(path, encoding="utf-8") as fh:
            obj = json.load(fh)
        files.append((path, obj))
    return files


def main():
    rng = random.Random(SEED)
    files = load_all()

    pg_items = [it for _, obj in files for it in obj["items"] if it["tipe"] == "pg"]
    pgk_items = [it for _, obj in files for it in obj["items"] if it["tipe"] == "pgk"]

    # --- PG: sasaran posisi merata ---
    n = len(pg_items)
    base, rem = divmod(n, 4)
    pool = []
    for i, L in enumerate(LETTERS):
        pool += [L] * (base + (1 if i < rem else 0))
    rng.shuffle(pool)
    for it, target in zip(pg_items, pool):
        correct = it["opsi"][it["kunci"]]
        rest = [op for op in it["opsi"] if op != correct]
        pos = LETTERS.index(target)
        new = rest[:pos] + [correct] + rest[pos:]
        it["opsi"] = new
        it["kunci"] = pos

    # --- PGK: sasaran pasangan merata ---
    combos = ["AB", "AC", "AD", "BC", "BD", "CD"]
    m = len(pgk_items)
    b, r = divmod(m, 6)
    cpool = []
    for i, c in enumerate(combos):
        cpool += [c] * (b + (1 if i < r else 0))
    rng.shuffle(cpool)
    for it, combo in zip(pgk_items, cpool):
        correct = [it["opsi"][k] for k in sorted(it["kunci"])]
        rest = [op for op in it["opsi"] if op not in correct]
        new = [None, None, None, None]
        for pos, txt in zip([LETTERS.index(ch) for ch in combo], correct):
            new[pos] = txt
        ri = 0
        for i in range(4):
            if new[i] is None:
                new[i] = rest[ri]
                ri += 1
        it["opsi"] = new
        it["kunci"] = sorted([LETTERS.index(ch) for ch in combo])

    for path, obj in files:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=2)
            fh.write("\n")

    dist = {L: sum(1 for it in pg_items if it["kunci"] == i) for i, L in enumerate(LETTERS)}
    pair = {}
    for it in pgk_items:
        k = "".join(sorted(LETTERS[i] for i in it["kunci"]))
        pair[k] = pair.get(k, 0) + 1
    print("Sebaran kunci PG  :", dist)
    print("Pasangan kunci PGK:", dict(sorted(pair.items())))
    print("Selesai: %d soal PG dan %d soal PGK diseimbangkan." % (len(pg_items), len(pgk_items)))


if __name__ == "__main__":
    main()
