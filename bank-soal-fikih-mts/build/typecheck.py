"""Aturan pemeriksaan untuk empat tipe soal tambahan.

Dipakai bersama oleh build.py dan validate.py agar tidak ada aturan yang
bercabang. Tipe soal:

  pgk      pilihan ganda kompleks, 4 opsi dengan tepat 2 jawaban benar
  bs       pernyataan benar/salah
  singkat  isian singkat 1-4 kata, dinilai otomatis
  essay    uraian, dilengkapi kunci jawaban dan rubrik penilaian
"""
from __future__ import annotations

import re
from collections import Counter

TYPE_KEYS = ("pgk", "bs", "singkat", "essay")
N_TYPE = {"pgk": 10, "bs": 10, "singkat": 10, "essay": 5}
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
MAX_SHORT_WORDS = 4


def check_pg(q: dict, tag: str, problems: list) -> None:
    opts = q.get("options", [])
    if len(opts) != 4:
        problems.append(f"{tag}: pgk harus punya 4 opsi, dapat {len(opts)}")
    if any(not isinstance(o, str) or not o.strip() for o in opts):
        problems.append(f"{tag}: pgk ada opsi kosong")
    ans = q.get("answers")
    if not isinstance(ans, list) or len(ans) != 2:
        problems.append(f"{tag}: pgk harus punya tepat 2 kunci (answers), dapat {ans!r}")
        return
    if sorted(ans) != ans or len(set(ans)) != 2:
        problems.append(f"{tag}: pgk answers harus unik dan terurut naik, dapat {ans}")
    if any(not isinstance(i, int) or isinstance(i, bool) or not 0 <= i < len(opts) for i in ans):
        problems.append(f"{tag}: pgk answers di luar rentang opsi ({ans})")


def check_bs(q: dict, tag: str, problems: list) -> None:
    if not isinstance(q.get("answer"), bool):
        problems.append(
            f"{tag}: bs answer harus boolean true/false, dapat {q.get('answer')!r}"
        )
    if q.get("options"):
        problems.append(f"{tag}: bs tidak perlu field options")


def check_singkat(q: dict, tag: str, problems: list) -> None:
    a = q.get("answer")
    if not isinstance(a, str) or not a.strip():
        problems.append(f"{tag}: singkat answer harus berupa teks")
        return
    words = a.strip().split()
    if len(words) > MAX_SHORT_WORDS:
        problems.append(f"{tag}: singkat answer {len(words)} kata (maks {MAX_SHORT_WORDS}): {a!r}")
    accepted = q.get("accepted", []) or []
    if not isinstance(accepted, list):
        problems.append(f"{tag}: singkat accepted harus berupa array")
        return
    for v in accepted:
        if not isinstance(v, str) or not v.strip():
            problems.append(f"{tag}: singkat accepted berisi nilai kosong")
        elif len(v.strip().split()) > MAX_SHORT_WORDS:
            problems.append(f"{tag}: singkat accepted {v!r} lebih dari {MAX_SHORT_WORDS} kata")


def check_essay(q: dict, tag: str, problems: list) -> None:
    if not q.get("key") or not str(q.get("key")).strip():
        problems.append(f"{tag}: essay wajib punya kunci jawaban (key)")
    rub = q.get("rubric")
    if not isinstance(rub, list) or len(rub) < 2:
        problems.append(f"{tag}: essay wajib punya rubric minimal 2 poin")
    elif any(not str(r).strip() for r in rub):
        problems.append(f"{tag}: essay rubric berisi poin kosong")


CHECKERS = {"pgk": check_pg, "bs": check_bs, "singkat": check_singkat, "essay": check_essay}


def check_common(q: dict, tag: str, problems: list, seen: dict) -> None:
    """Aturan yang berlaku untuk semua tipe: teks, pembahasan, level, duplikasi."""
    if not q.get("text") or not str(q.get("text")).strip():
        problems.append(f"{tag}: teks soal kosong")
    if not q.get("indicator") or not str(q.get("indicator")).strip():
        problems.append(f"{tag}: indikator kosong")
    if not q.get("explanation") or not str(q.get("explanation")).strip():
        problems.append(f"{tag}: tidak ada pembahasan")
    if q.get("level") not in ("HOTS", "MOTS", "LOTS"):
        problems.append(f"{tag}: level tidak valid ({q.get('level')})")
    key = re.sub(r"\s+", " ", str(q.get("text") or "")).strip()[:90]
    if key and key in seen:
        problems.append(f"{tag}: batang soal duplikat dengan {seen[key]}")
    if key:
        seen[key] = tag


def check_balance(bab: dict, label: str, problems: list) -> Counter:
    """Periksa jumlah per tipe dan keseimbangan distribusi kunci.

    Mengembalikan Counter jumlah soal per tipe.
    """
    counts = Counter()
    for k in TYPE_KEYS:
        arr = bab.get(k, []) or []
        counts[k] = len(arr)
        if len(arr) != N_TYPE[k]:
            problems.append(f"{label}: tipe {k} {len(arr)} soal (harus {N_TYPE[k]})")

    # PG kompleks: enam kombinasi posisi kunci terbagi rata dalam 10 soal,
    # sehingga tidak ada pasangan yang muncul lebih dari dua kali.
    pairs = [tuple(q.get("answers") or ()) for q in bab.get("pgk", []) or []]
    valid_pairs = [p for p in pairs if p in PAIRS]
    if counts["pgk"] == N_TYPE["pgk"] and len(valid_pairs) == N_TYPE["pgk"]:
        c = Counter(valid_pairs)
        if any(v > 2 for v in c.values()):
            problems.append(f"{label}: pgk pasangan kunci menumpuk {dict(c)}")
        if len(c) < 5:
            problems.append(
                f"{label}: pgk hanya {len(c)} kombinasi posisi kunci (harapkan >=5 dari 6)"
            )
    elif pairs and len(valid_pairs) != len(pairs):
        problems.append(f"{label}: pgk ada pasangan kunci tidak sah {[p for p in pairs if p not in PAIRS]}")

    # Benar/salah: tepat 5 Benar dan 5 Salah.
    bs = [q.get("answer") for q in bab.get("bs", []) or [] if isinstance(q.get("answer"), bool)]
    if counts["bs"] == N_TYPE["bs"] and len(bs) == N_TYPE["bs"]:
        if bs.count(True) != 5 or bs.count(False) != 5:
            problems.append(
                f"{label}: bs harus 5 Benar & 5 Salah, dapat {bs.count(True)} Benar / {bs.count(False)} Salah"
            )
    return counts
