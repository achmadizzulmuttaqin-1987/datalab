"""Pemeriksa cepat berkas tipe soal sebelum validasi penuh.

Memeriksa hal yang paling sering keliru saat menulis berkas secara manual:
  1. array 'options' yang tidak ditutup dengan benar  ->  "}',answers':" atau "}',answers':"
  2. jumlah opsi bukan empat
  3. kunci pgk tidak tepat dua atau tidak terurut
  4. bs bukan 5 Benar dan 5 Salah
  5. tanda kutip tunggal di dalam string (apostrof)
"""
from __future__ import annotations
import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jsobj  # noqa: E402
import typecheck  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TYPES = ROOT / "data" / "types"
BAD_CLOSE = re.compile(r"\}'answers':")


def _check_options_close(path: Path, src: str) -> list[str]:
    """Cari array options yang ditutup dengan }} bukan ] (keliru tulis yang sering terjadi)."""
    err: list[str] = []
    for i, line in enumerate(src.split("\n"), 1):
        if "'options'" not in line:
            continue
        seg = line[line.index("'options'"):]
        stop = seg.find(",'answers'")
        if stop < 0:
            continue
        arr = seg[:stop]
        if arr.count("[") != 1 or not arr.endswith("]"):
            err.append(f"{path.name}:{i}: array options tidak ditutup dengan benar -> {arr[-45:]!r}")
    return err


def scan(path: Path) -> list[str]:
    src = path.read_text(encoding="utf-8")
    err: list[str] = []
    for m in BAD_CLOSE.finditer(src):
        line = src[:m.start()].count("\n") + 1
        err.append(f"{path.name}:{line}: array options tidak ditutup dengan benar (ditemukan \"}}'answers':\")")
    err.extend(_check_options_close(path, src))
    if err:
        return err
    try:
        bab = jsobj.extract_addtypes(src)
    except Exception as exc:  # noqa: BLE001
        err.append(f"{path.name}: gagal dibaca ({exc})")
        return err
    for i, q in enumerate(bab.get("pgk") or []):
        if len(q.get("options") or []) != 4:
            err.append(f"{path.name} pgk#{i}: opsi berjumlah {len(q.get('options') or [])}, seharusnya 4")
        a = q.get("answers")
        if not isinstance(a, list) or len(a) != 2 or a != sorted(a):
            err.append(f"{path.name} pgk#{i}: answers={a}, seharusnya 2 indeks terurut naik")
    bs = bab.get("bs") or []
    vals = [q.get("answer") for q in bs]
    if len(bs) == typecheck.N_TYPE["bs"] and vals.count(True) != 5:
        err.append(f"{path.name}: bs {vals.count(True)} Benar / {vals.count(False)} Salah (harus 5/5)")
    for k in typecheck.TYPE_KEYS:
        for i, q in enumerate(bab.get(k) or []):
            for field in ("text", "explanation", "key"):
                if "'" in str(q.get(field, "")):
                    err.append(f"{path.name} {k}#{i}: tanda kutip tunggal di dalam '{field}'")
    return err


def main() -> int:
    files = sorted(TYPES.rglob("*.js")) if TYPES.exists() else []
    if len(sys.argv) > 1:
        files = [f for f in files if sys.argv[1] in f.as_posix()]
    errs: list[str] = []
    for f in files:
        errs.extend(scan(f))
    print(f"Berkas diperiksa : {len(files)}")
    if errs:
        print(f"KELIRU ({len(errs)}):")
        for e in errs:
            print("  -", e)
        return 1
    print("Tidak ada keliru struktur yang terdeteksi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
