"""Validasi seluruh berkas data soal tanpa membangun output.

Memeriksa berkas materi (pilihan ganda) dan berkas tipe soal tambahan
(PG kompleks, benar/salah, jawaban singkat, uraian): jumlah soal per tipe,
kunci jawaban, distribusi kunci, pembahasan, apostrof yang dapat merusak
string JS, dan duplikasi batang soal.

Jalankan: python3 build/validate.py
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jsobj  # noqa: E402
import typecheck  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
# Apostrof tak ter-escape di antara huruf akan memutus string kutip tunggal.
APOS = re.compile(r"[A-Za-z]'[A-Za-z]")


def check_apostrophes(path: Path, label: str, errors: list) -> None:
    text = path.read_text(encoding="utf-8")
    # apostrof yang di-escape (\') aman; sisakan yang tidak ter-escape
    stripped = text.replace("\\'", "")
    hits = APOS.findall(stripped)
    if hits:
        errors.append(f"{label}: apostrof tak ter-escape {hits[:3]}")


def main() -> int:
    index = jsobj.extract_index((DATA / "index.js").read_text(encoding="utf-8"))
    errors = []
    rows = []
    total_pg = 0
    total_type = Counter()
    seen_global = {}
    n_type_files = 0

    for meta in index:
        p = DATA / meta["file"]
        check_apostrophes(p, meta["file"], errors)
        obj = jsobj.extract_register(p.read_text(encoding="utf-8"))
        qs = obj.get("questions", [])
        total_pg += len(qs)
        stem = Counter()
        dist = Counter()

        for i, q in enumerate(qs, 1):
            tag = f"{meta['file']} #{i}"
            opts = q.get("options", [])
            a = q.get("answer")
            if len(opts) != 4:
                errors.append(f"{tag}: jumlah opsi {len(opts)}")
            if not (isinstance(a, int) and not isinstance(a, bool) and 0 <= a < len(opts)):
                errors.append(f"{tag}: answer tidak valid ({a})")
            else:
                dist[a] += 1
            if not q.get("explanation"):
                errors.append(f"{tag}: pembahasan kosong")
            if q.get("level") not in ("HOTS", "MOTS", "LOTS"):
                errors.append(f"{tag}: level tidak valid")
            txt = re.sub(r"\s+", " ", (q.get("text") or "")).strip()
            if not txt:
                errors.append(f"{tag}: teks soal kosong")
            stem[txt[:40]] += 1
            # Soal berstimulus (kutipan dalil, tabel, kasus) sah memakai batang
            # yang sama selama stimulusnya berbeda, jadi kunci duplikat PG
            # menggabungkan stimulus dengan batang soal.
            stim = re.sub(r"\s+", " ", (q.get("stimulus") or "")).strip()
            key = (stim + "\u0001" + txt) if stim else txt
            if key in seen_global:
                errors.append(f"{tag}: batang soal sama dengan {seen_global[key]}")
            seen_global[key] = tag

        # ---- tipe soal tambahan ----
        tp = DATA / "types" / (meta["file"][:-3] + ".js")
        tc = Counter()
        if tp.exists():
            n_type_files += 1
            label = f"types/{tp.name}"
            check_apostrophes(tp, label, errors)
            try:
                tobj = jsobj.extract_addtypes(tp.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{label}: gagal dibaca ({exc})")
                tobj = None
            if tobj is not None:
                if tobj.get("id") != meta["id"]:
                    errors.append(f"{label}: id tidak cocok ({tobj.get('id')} vs {meta['id']})")
                for k in typecheck.TYPE_KEYS:
                    for i, q in enumerate(tobj.get(k, []) or [], 1):
                        tag = f"{label} {k}#{i}"
                        typecheck.check_common(q, tag, errors, seen_global)
                        typecheck.CHECKERS[k](q, tag, errors)
                tc = typecheck.check_balance(tobj, label, errors)
                total_type.update(tc)

        rows.append((meta["id"], obj.get("grade"), obj.get("semester"), len(qs), tc))

    # berkas yang tidak terdaftar di indeks
    disk = {str(x.relative_to(DATA)) for x in DATA.glob("k*/*.js")}
    listed = {m["file"] for m in index}
    for f in sorted(listed - disk):
        errors.append(f"indeks menunjuk berkas yang tidak ada: {f}")
    for f in sorted(disk - listed):
        errors.append(f"berkas tidak terdaftar di indeks: {f}")
    disk_t = {x.name for x in (DATA / "types").glob("*.js")} if (DATA / "types").exists() else set()
    listed_t = {m["file"][:-3] + ".js" for m in index}
    for f in sorted(disk_t - listed_t):
        errors.append(f"berkas tipe tidak cocok dengan materi mana pun: types/{f}")

    print(f"{'materi':<26}{'kl':>3}{'sm':>3}{'PG':>5}{'PGK':>5}{'B/S':>5}{'Sgkt':>6}{'Esai':>6}")
    for r in rows:
        tc = r[4]
        print(f"{r[0]:<26}{r[1]:>3}{r[2]:>3}{r[3]:>5}{tc['pgk']:>5}{tc['bs']:>5}"
              f"{tc['singkat']:>6}{tc['essay']:>6}")

    grand = total_pg + sum(total_type.values())
    print(f"\nMateri        : {len(rows)}")
    print(f"Berkas tipe   : {n_type_files}/{len(rows)} bab")
    print(f"Soal PG       : {total_pg}")
    print(f"Soal tipe lain: " + " · ".join(f"{k} {total_type[k]}" for k in typecheck.TYPE_KEYS))
    print(f"Total soal    : {grand}")

    if errors:
        print(f"\nERROR ({len(errors)}):")
        for e in errors[:60]:
            print("  -", e)
        if len(errors) > 60:
            print(f"  ... dan {len(errors) - 60} lainnya")
        return 1
    print("\nSemua pemeriksaan lulus.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
