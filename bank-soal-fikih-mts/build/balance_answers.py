"""Seimbangkan distribusi kunci jawaban di seluruh materi sebuah proyek bank soal.

Masalah yang diperbaiki: kunci jawaban menumpuk di satu opsi (pada draf awal
Akidah Akhlak 1514 dari 1600 soal berkunci opsi B, pada Fikih 1246 dari 1500),
sehingga kunci dapat ditebak tanpa membaca soal.

Skrip mengacak urutan opsi tiap soal lalu menempatkan kunci mengikuti pola
gilir merata. Isi soal, indikator, stimulus, dan pembahasan tidak diubah, dan
opsi yang benar tetap opsi yang sama — hanya posisinya yang berpindah.

Jalankan dari folder proyek:
    python3 build/balance_answers.py [--dry-run] [--seed N]
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="laporkan saja, jangan menulis")
    ap.add_argument("--seed", type=int, default=20260929)
    args = ap.parse_args()

    index = jsobj.extract_index((datafile.DATA / "index.js").read_text(encoding="utf-8"))
    rng = random.Random(args.seed)
    before_all, after_all = Counter(), Counter()
    written = 0
    failures = []

    for meta in index:
        name = meta["file"]
        obj, head, footer = datafile.read_topic(name)
        qs = obj["questions"]
        targets = datafile.balanced_keys(len(qs))
        new_qs = []

        for q, tgt in zip(qs, targets):
            if len(q["options"]) != 4:
                failures.append(f"{name}: jumlah opsi {len(q['options'])}, dilewati")
                new_qs.append(q)
                before_all.update([q["answer"]])
                after_all.update([q["answer"]])
                continue
            correct = q["options"][q["answer"]]
            before_all.update([q["answer"]])
            nq = datafile.reorder_options(q, tgt, rng)

            # verifikasi ketat: tidak ada isi yang berubah selain urutan opsi
            if sorted(nq["options"]) != sorted(q["options"]):
                failures.append(f"{name}: isi opsi berubah")
                return 1
            if nq["options"][nq["answer"]] != correct:
                failures.append(f"{name}: kunci bergeser dari jawaban benar")
                return 1
            if nq["answer"] != tgt:
                failures.append(f"{name}: target {tgt} tidak tercapai")
                return 1
            for k in q:
                if k not in ("options", "answer") and nq[k] != q[k]:
                    failures.append(f"{name}: field {k} berubah")
                    return 1
            after_all.update([nq["answer"]])
            new_qs.append(nq)

        if not args.dry_run:
            datafile.write_topic(name, head, new_qs, footer)
            written += 1

    # baca ulang dan pastikan berkas tetap sah
    if not args.dry_run:
        recheck = Counter()
        for meta in index:
            obj = jsobj.extract_register(
                (datafile.DATA / meta["file"]).read_text(encoding="utf-8")
            )
            if len(obj["questions"]) != 50:
                failures.append(f"{meta['file']}: {len(obj['questions'])} soal setelah tulis")
            for q in obj["questions"]:
                if len(q["options"]) != 4:
                    failures.append(f"{meta['file']}: opsi {len(q['options'])} setelah tulis")
                if q["answer"] not in (0, 1, 2, 3):
                    failures.append(f"{meta['file']}: kunci {q['answer']} setelah tulis")
                recheck.update([q["answer"]])
        print(f"Kunci baca ulang  : {dict(sorted(recheck.items()))}")

    print(f"Berkas ditulis    : {written}")
    print(f"Kunci SEBELUM     : {dict(sorted(before_all.items()))}")
    print(f"Kunci SESUDAH     : {dict(sorted(after_all.items()))}")
    if failures:
        print(f"\nMASALAH ({len(failures)}):")
        for f in failures[:20]:
            print("  -", f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
