"""Pustaka untuk membaca, mengubah, dan menulis ulang file data soal.

Menjaga format asli berkas (kunci tanpa tanda kutip, string kutip tunggal)
sehapa diff tetap terbaca dan tidak ada apostrof yang merusak string JS.
"""
from __future__ import annotations

import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jsobj  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ESCAPE = {"\\": "\\\\", "'": "\\'", "\n": "\\n", "\r": "\\r", "\t": "\\t"}


def esc(s: str) -> str:
    out = []
    for ch in s:
        out.append(ESCAPE.get(ch, ch))
    return "".join(out)


def dumps(v) -> str:
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, str):
        return "'" + esc(v) + "'"
    if isinstance(v, list):
        return "[" + ",".join(dumps(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ",".join(dumps(k) + ":" + dumps(x) for k, x in v.items()) + "}"
    raise TypeError(f"tipe tak didukung: {type(v)}")


def dumps_question(q: dict) -> str:
    """Serialisasi satu soal, kunci ditulis tanpa tanda kutip seperti aslinya."""
    parts = [f"{k}:{dumps(v)}" for k, v in q.items()]
    return "{" + ",".join(parts) + "}"


HEADER = re.compile(r"\A(?P<head>.*?window\.BSRegister\(\{.*?'questions':\[)", re.S)

# Dua gaya penutup pernah dipakai: "]  \n});" (proyek Fikih) dan "\n]});" (Akidah).
FOOTERS = ("\n]\n});\n", "\n]});\n")


def read_topic(name: str) -> tuple[dict, str, str]:
    """Kembalikan (objek topik, kepala berkas, gaya penutup berkas)."""
    path = DATA / name
    text = path.read_text(encoding="utf-8")
    m = HEADER.match(text)
    if not m:
        raise ValueError(f"{name}: pola kepala tidak dikenali")
    head = m.group("head")
    body = text[len(head):]
    for footer in FOOTERS:
        if body.endswith(footer):
            obj = jsobj.extract_register(text)
            return obj, head, footer
    raise ValueError(f"{name}: pola penutup tidak dikenali ({body[-12:]!r})")


def write_topic(name: str, head: str, questions: list[dict], footer: str = "\n]});\n") -> None:
    body = "\n".join(dumps_question(q) + "," for q in questions)
    body = body[:-1]  # buang koma terakhir
    (DATA / name).write_text(head + body + footer, encoding="utf-8")


def balanced_keys(n: int) -> list[int]:
    """Kunci jawaban yang terbagi rata di antara opsi 0..3 untuk n soal."""
    base = [i % 4 for i in range(n)]
    rng = random.Random(20260929)
    rng.shuffle(base)
    return base


def reorder_options(q: dict, target: int, rng: random.Random) -> dict:
    """Susun ulang opsi sehingga kunci berada di indeks `target`."""
    opts = list(q["options"])
    a = q["answer"]
    if not (isinstance(a, int) and 0 <= a < len(opts)):
        raise ValueError(f"kunci tidak valid: {a}")
    rest = [o for i, o in enumerate(opts) if i != a]
    rng.shuffle(rest)
    new_opts = rest[:target] + [opts[a]] + rest[target:]
    out = dict(q)
    out["options"] = new_opts
    out["answer"] = new_opts.index(opts[a])
    return out


def stem_key(text: str, n: int = 70) -> str:
    return re.sub(r"\s+", " ", text or "").strip()[:n]


# ---------- berkas tipe soal tambahan (window.BSAddTypes) ----------
HEADER_TYPES = re.compile(
    r"\A(?P<head>.*?window\.BSAddTypes\(\{.*?'essay':\[)", re.S
)
TYPE_ORDER = ("pgk", "bs", "singkat", "essay")


def dumps_types(bab: dict) -> str:
    """Serialisasi satu berkas tipe soal, menjaga format kutip tunggal."""
    parts = [f"'id':{dumps(bab['id'])}"]
    for k in TYPE_ORDER:
        arr = bab.get(k, []) or []
        body = ",\n".join(dumps_question(q) for q in arr)
        parts.append(f"'{k}':[\n{body}\n]")
    return "window.BSAddTypes({\n" + ",\n".join(parts) + "\n});\n"


def write_types(path: Path, bab: dict, header_comment: str = "") -> None:
    text = (header_comment + "\n" if header_comment else "") + dumps_types(bab)
    path.write_text(text, encoding="utf-8")
