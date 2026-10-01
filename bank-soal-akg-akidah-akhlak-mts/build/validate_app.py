#!/usr/bin/env python3
"""Periksa mutu bank soal AKG Akidah Akhlak MTs sebelum dibangun."""
import json
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "build", "data")

def main():
    errors = []
    items = []
    seen_ids = set()
    seen_stems = {}
    for path in sorted(glob.glob(os.path.join(DATA, "*.json"))):
        name = os.path.basename(path)
        if name in ("kisi-kisi.json", "rangkuman.json"):
            continue
        with open(path, encoding="utf-8") as fh:
            obj = json.load(fh)
        for it in obj["items"]:
            it.setdefault("kategori", obj["kategori"])
            iid = it["id"]
            if iid in seen_ids:
                errors.append("%s: id ganda %s" % (name, iid))
            seen_ids.add(iid)
            for field in ("kategori", "topik", "tipe", "teks", "opsi", "kunci", "bahasan"):
                if field not in it:
                    errors.append("%s %s: field %s hilang" % (name, iid, field))
            if it.get("kategori") not in ("pedagogik", "profesional"):
                errors.append("%s %s: kategori tidak dikenal" % (name, iid))
            opsi = it.get("opsi", [])
            if len(opsi) != 4:
                errors.append("%s %s: jumlah opsi %d (harus 4)" % (name, iid, len(opsi)))
            if len(set(opsi)) != len(opsi):
                errors.append("%s %s: ada opsi kembar" % (name, iid))
            for op in opsi:
                if not isinstance(op, str) or not op.strip():
                    errors.append("%s %s: opsi kosong" % (name, iid))
                if "'" in op or '"' in op:
                    errors.append("%s %s: opsi memuat tanda apostrof/kutip" % (name, iid))
            if not it.get("bahasan"):
                errors.append("%s %s: bahasan kosong" % (name, iid))
            if len(it.get("teks", "").strip()) < 20:
                errors.append("%s %s: teks soal terlalu pendek" % (name, iid))
            key = " ".join(it["teks"].split()).lower()
            if key in seen_stems:
                errors.append("%s %s: batang soal kembar dengan %s" % (name, iid, seen_stems[key]))
            seen_stems[key] = iid
            if it["tipe"] == "pg":
                k = it["kunci"]
                if not isinstance(k, int) or isinstance(k, bool) or not 0 <= k < len(opsi):
                    errors.append("%s %s: kunci PG tidak valid" % (name, iid))
            elif it["tipe"] == "pgk":
                k = it["kunci"]
                if (not isinstance(k, list) or len(k) != 2
                        or len(set(k)) != 2 or not all(isinstance(x, int) and 0 <= x < len(opsi) for x in k)):
                    errors.append("%s %s: kunci PGK harus dua indeks berbeda" % (name, iid))
            else:
                errors.append("%s %s: tipe tidak dikenal" % (name, iid))
            items.append(it)

    ped = [i for i in items if i["kategori"] == "pedagogik"]
    pro = [i for i in items if i["kategori"] == "profesional"]
    pgk = [i for i in items if i["tipe"] == "pgk"]

    # sebaran kunci PG
    dist = [0, 0, 0, 0]
    for i in items:
        if i["tipe"] == "pg":
            dist[i["kunci"]] += 1

    # panjang opsi: kunci tidak boleh jauh lebih panjang dari distraktor
    tilt = 0
    for i in items:
        lens = [len(o.split()) for o in i["opsi"]]
        ks = [i["kunci"]] if i["tipe"] == "pg" else i["kunci"]
        mean_k = sum(lens[k] for k in ks) / len(ks)
        others = [lens[j] for j in range(len(lens)) if j not in ks]
        mean_o = sum(others) / len(others)
        if mean_k - mean_o >= 4:
            tilt += 1
            errors.append("%s: opsi kunci rata-rata %.1f kata lebih panjang dari distraktor %.1f"
                          % (i["id"], mean_k, mean_o))

    # pasangan kunci PGK seimbang
    pair = {}
    for i in items:
        if i["tipe"] == "pgk":
            key = "".join(sorted("ABCD"[k] for k in i["kunci"]))
            pair[key] = pair.get(key, 0) + 1

    # keseimbangan sebaran kunci
    if sum(dist):
        mn, mx = min(dist), max(dist)
        if mn == 0 or mx > 1.8 * mn:
            errors.append("sebaran kunci PG tidak seimbang: A=%d B=%d C=%d D=%d" % tuple(dist))
    if pgk:
        mx = max(pair.values())
        if mx > max(3, 0.35 * len(pgk)):
            errors.append("sebaran pasangan kunci PGK tidak seimbang: %s" % dict(sorted(pair.items())))

    print("Total soal          :", len(items))
    print("Pedagogik           :", len(ped))
    print("Profesional         :", len(pro))
    print("PG kompleks (PGK)   :", len(pgk))
    print("Sebaran kunci PG    : A=%d B=%d C=%d D=%d" % tuple(dist))
    print("Pasangan kunci PGK  :", dict(sorted(pair.items())))
    print("Soal opsi timpang   :", tilt)
    if errors:
        print("\nMASALAH DITEMUKAN:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("\nSEMUA PEMERIKSAAN LULUS")

if __name__ == "__main__":
    main()
