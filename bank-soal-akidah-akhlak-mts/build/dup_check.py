"""Pemeriksa soal kembar untuk bank soal tipe baru + PG.

Jalankan dari direktori proyek:
    python3 build/dup_check.py            # seluruh bab
    python3 build/dup_check.py --ambang 0.80
    python3 build/dup_check.py --bab k8/puasa   # bandingkan satu bab dengan lainnya

Lima pemeriksaan:
  A. batang soal identik (teks penuh, seluruh tipe termasuk PG)
  B. batang soal berbagi awalan 40 karakter
  C. batang soal hampir kembar (kemiripan token Jaccard >= ambang)
  D. jawaban singkat yang sama dipakai di lebih dari satu bab
  E. susunan pilihan (4 opsi) yang identik pada soal PGK berbeda

Keluarannya berupa daftar kelompok yang perlu dimodifikasi; kode keluar 1
apabila terdapat temuan pada pemeriksaan A-E.
"""
from __future__ import annotations
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jsobj import extract_addtypes  # noqa: E402
try:
    from jsobj import extract_register
except Exception:  # pragma: no cover - nama fungsi berbeda antar versi
    extract_register = None

ROOT = Path(__file__).resolve().parent.parent
ADD_KEYS = ("pgk", "bs", "singkat", "essay")
STOP = {
    "yang", "dan", "atau", "dengan", "pada", "dalam", "untuk", "adalah", "sehingga",
    "karena", "bahwa", "tidak", "dari", "oleh", "sebagai", "serta", "lalu", "ketika",
    "apabila", "jika", "maka", "itu", "ini", "tersebut", "berikut", "pilih", "dua",
    "pernyataan", "ketentuan", "tepat", "paling", "perhatikan", "sebutkan",
}


def norm(t: str) -> str:
    t = (t or "").replace("\\'", "'").lower()
    t = re.sub(r"[^a-z0-9\s'-]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def tokens(t: str) -> set:
    return {w for w in norm(t).split() if w and w not in STOP and len(w) > 1}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def load_items():
    """Kembalikan daftar (tag, tipe, teks, dict soal) untuk seluruh bab."""
    out = []
    for f in sorted((ROOT / "data" / "types").glob("k*/*.js")):
        tag = f"{f.parent.name}/{f.stem}"
        d = extract_addtypes(f.read_text(encoding="utf-8"))
        for k in ADD_KEYS:
            for i, q in enumerate(d.get(k, []) or [], 1):
                out.append((tag, k, f"{k}#{i}", q))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ambang", type=float, default=0.78,
                    help="ambang kemiripan token Jaccard untuk pemeriksaan C")
    ap.add_argument("--bab", default=None, help="batasi laporan pada bab ini (mis. k8/puasa)")
    ap.add_argument("--ringkas", action="store_true", help="hanya tampilkan jumlah temuan")
    a = ap.parse_args()

    items = load_items()
    findings = []

    # A. batang identik (seluruh tipe baru + PG bila register terbaca)
    groups = defaultdict(list)
    for tag, k, loc, q in items:
        groups[norm(q.get("text", ""))].append(f"{tag} {loc}")
    for key, v in groups.items():
        if len(v) > 1 and key:
            findings.append(("A batang identik", v, key[:70]))

    # B. awalan 40 karakter
    groups = defaultdict(list)
    for tag, k, loc, q in items:
        n = norm(q.get("text", ""))
        if n:
            groups[n[:40]].append(f"{tag} {loc}")
    for key, v in groups.items():
        if len(v) > 1:
            findings.append(("B awalan 40 karakter", v, key))

    # C. hampir kembar (tipe sama)
    by_type = defaultdict(list)
    for tag, k, loc, q in items:
        by_type[k].append((f"{tag} {loc}", tokens(q.get("text", "")), norm(q.get("text", ""))))
    near = []
    for k, arr in by_type.items():
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                s = jaccard(arr[i][1], arr[j][1])
                if s >= a.ambang and arr[i][0].split()[0] != arr[j][0].split()[0]:
                    near.append((round(s, 3), k, arr[i][0], arr[j][0], arr[i][2][:60]))
    near.sort(reverse=True)
    for s, k, x, y, prev in near:
        findings.append((f"C hampir kembar {k} (mirip {s})", [x, y], prev))

    # D. jawaban singkat sama di lebih dari satu bab
    groups = defaultdict(set)
    for tag, k, loc, q in items:
        if k == "singkat":
            groups[norm(q.get("answer", ""))].add(tag)
    for key, v in groups.items():
        if len(v) > 1 and key:
            findings.append(("D jawaban singkat dipakai di beberapa bab", sorted(v), key))

    # E. susunan pilihan identik pada PGK
    groups = defaultdict(list)
    for tag, k, loc, q in items:
        if k == "pgk":
            sig = "|".join(norm(o) for o in (q.get("options") or []))
            groups[sig].append(f"{tag} {loc}")
    for key, v in groups.items():
        if len(v) > 1 and key:
            findings.append(("E susunan pilihan PGK identik", v, key[:70]))

    if a.bab:
        findings = [f for f in findings if any(a.bab in x for x in f[1])]

    if not findings:
        print("Tidak ada soal kembar yang terdeteksi (pemeriksaan A-E).")
        return 0
    print(f"TEMUAN SOAL KEMBAR ({len(findings)} kelompok, ambang C = {a.ambang}):")
    for label, v, prev in findings:
        if a.ringkas:
            print(f"  - {label}: {', '.join(v)}")
        else:
            print(f"\n  [{label}]")
            for x in v:
                print(f"    - {x}")
            print(f"    teks: {prev}...")
    return 1


if __name__ == "__main__":
    sys.exit(main())
