"""Siapkan data soal Fikih MTs untuk game 3D "Jejak Cilik".

Sumber : ../bank-soal-fikih-mts/data/k7..k9/*.js (1.500 soal pilihan ganda)
Keluaran: build/questions.json

Setiap bab (50 soal) dipecah menjadi 5 goa x 10 soal. Urutan soal dipertahankan
agar goa 1-5 memuat soal bab 1 secara berurutan, goa 6-10 memuat soal bab 2,
dan seterusnya.

Penjelasan (explanation) dibersihkan dari rujukan huruf pilihan ("Pilihan B
salah...") karena urutan opsi sudah diacak oleh balance_answers.py di repo
sumber, sehingga rujukan huruf lama bisa menyesatkan.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent
SRC = REPO / "bank-soal-fikih-mts" / "data"
OUT = HERE / "questions.json"

sys.path.insert(0, str(REPO / "bank-soal-fikih-mts" / "build"))
import jsobj  # noqa: E402


def clean_explanation(text: str) -> str:
    """Buang kalimat yang merujuk huruf opsi karena opsi telah diacak."""
    if not text:
        return ""
    # Pisahkan kalimat tanpa merusak singkatan/desimal.
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(])", text.strip())
    kept = []
    for part in parts:
        if re.search(r"\b(?:Pilihan|Opsi|pilihan|opsi)\s+[A-E]\b", part):
            continue
        if re.search(r"\b[A-D]\s+(?:salah|benar|keliru|tepat|kurang|lebih)\b", part):
            continue
        kept.append(part)
    out = " ".join(kept).strip()
    if len(out) < 40:
        # Jangan sampai pembahasan kosong; ambil kalimat pertama saja.
        out = text.strip()
    return out


def main() -> int:
    index = jsobj.extract_index((SRC / "index.js").read_text(encoding="utf-8"))
    if len(index) != 30:
        raise SystemExit(f"Jumlah bab tidak sesuai: {len(index)}")

    babs = []
    total = 0
    for order, meta in enumerate(index, 1):
        obj = jsobj.extract_register((SRC / meta["file"]).read_text(encoding="utf-8"))
        qs = obj["questions"]
        if len(qs) != 50:
            raise SystemExit(f"{meta['file']}: {len(qs)} soal, seharusnya 50")

        caves = []
        for c in range(5):
            chunk = qs[c * 10:(c + 1) * 10]
            packed = []
            for q in chunk:
                opts = q["options"]
                a = q["answer"]
                if not (0 <= a < len(opts)):
                    raise SystemExit(f"{meta['file']}: kunci tidak valid")
                item = {
                    "q": q["text"],
                    "o": opts,
                    "a": a,
                    "e": clean_explanation(q.get("explanation", "")),
                }
                if q.get("stimulus"):
                    item["st"] = q["stimulus"]
                if q.get("stimulusAr"):
                    item["ar"] = q["stimulusAr"]
                packed.append(item)
            caves.append(packed)
            total += len(packed)

        babs.append({
            "id": obj["id"],
            "g": obj["grade"],
            "s": obj["semester"],
            "o": order,
            "t": obj["title"],
            "d": obj.get("desc", ""),
            "caves": caves,
        })

    payload = {
        "meta": {
            "title": "Jejak Cilik",
            "subtitle": "Petualangan Fikih MTs",
            "source": "bank-soal-fikih-mts",
            "nBabs": len(babs),
            "nCaves": len(babs) * 5,
            "nQuestions": total,
            "perCave": 10,
            "perBab": 50,
        },
        "babs": babs,
    }
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    if "</" in raw:
        raw = raw.replace("</", "<\\/")
    OUT.write_text(raw, encoding="utf-8")

    # Ringkasan
    per_grade = {}
    for b in babs:
        per_grade.setdefault(b["g"], [0, 0])
        per_grade[b["g"]][0] += 1
        per_grade[b["g"]][1] += 50 * 5
    print(f"Berkas  : {OUT}  ({OUT.stat().st_size / 1024:.0f} KB)")
    print(f"Bab     : {len(babs)} | Goa: {len(babs) * 5} | Soal: {total}")
    for g in sorted(per_grade):
        print(f"Kelas {g} : {per_grade[g][0]} bab, {per_grade[g][0] * 5} goa, {per_grade[g][0] * 50} soal")
    print("Contoh goa 1 soal 1:", babs[0]["caves"][0][0]["q"][:70], "...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
