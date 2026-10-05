#!/usr/bin/env python3
"""Terapkan tambalan teks opsi tanpa mengubah kunci.

Pemakaian: python3 build/apply_opsi_patch.py build/patch/patch-opsi-1.json
Aturan keselamatan: soal dan indeks kunci tidak diubah, jumlah opsi wajib sama,
teks tidak boleh memuat apostrof atau tanda kutip, dan teks harus benar-benar berubah.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "build", "data")


def main():
    if len(sys.argv) < 2:
        print("Pemakaian: python3 build/apply_opsi_patch.py <berkas-patch.json>")
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as fh:
        patch = json.load(fh)

    files = {}
    for entry in patch["items"]:
        name = entry["file"]
        files.setdefault(name, {})[entry["id"]] = entry["opsi"]

    total = 0
    for name, changes in sorted(files.items()):
        path = os.path.join(DATA, name + ".json")
        with open(path, encoding="utf-8") as fh:
            obj = json.load(fh)
        for it in obj["items"]:
            if it["id"] not in changes:
                continue
            new = changes[it["id"]]
            if len(new) != len(it["opsi"]):
                print("DITOLAK", it["id"], "jumlah opsi berbeda")
                sys.exit(1)
            for op in new:
                if not op.strip():
                    print("DITOLAK", it["id"], "opsi kosong")
                    sys.exit(1)
                if "'" in op or '"' in op:
                    print("DITOLAK", it["id"], "opsi memuat apostrof/kutip")
                    sys.exit(1)
            if new == it["opsi"]:
                print("DITOLAK", it["id"], "teks tidak berubah")
                sys.exit(1)
            it["opsi"] = new
            total += 1
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    print("Tambalan diterapkan: %d soal pada %d berkas." % (total, len(files)))


if __name__ == "__main__":
    main()
