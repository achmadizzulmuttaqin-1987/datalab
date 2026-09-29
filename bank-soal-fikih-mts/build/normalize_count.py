#!/usr/bin/env python3
"""Rapikan berkas data: hapus soal duplikat dan samakan jumlah soal menjadi tepat 50
per topik (hanya memangkas yang berlebih, tidak menambah).

Format keluaran diseragamkan: satu soal per baris, seluruh string kutip tunggal.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jsobj  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TARGET = 50
KEY_ORDER = ["level", "indicator", "stimulusAr", "stimulus", "text",
             "options", "answer", "explanation"]


def esc(t):
    out = []
    for ch in str(t):
        if ch == "\\":
            out.append("\\\\")
        elif ch == "'":
            out.append("\\'")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            continue
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    return "'" + "".join(out) + "'"


def val(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, list):
        return "[" + ",".join(val(x) for x in v) + "]"
    return esc(v)


def dump_q(q):
    keys = [k for k in KEY_ORDER if k in q] + [k for k in q if k not in KEY_ORDER]
    return "{" + ",".join("'%s':%s" % (k, val(q[k])) for k in keys) + "}"


def main():
    for p in sorted(ROOT.glob("data/k*/*.js")):
        src = p.read_text(encoding="utf-8")
        head = ""
        m = re.match(r"(/\*[\s\S]*?\*/\s*)", src)
        if m:
            head = m.group(1)
        obj = jsobj.extract_register(src)
        qs = obj["questions"]

        # buang duplikat (berdasarkan teks soal yang dinormalkan)
        seen, uniq = set(), []
        for q in qs:
            key = re.sub(r"\s+", " ", str(q.get("text", ""))).strip()
            if key in seen:
                continue
            seen.add(key)
            uniq.append(q)

        removed = len(qs) - len(uniq)
        if len(uniq) > TARGET:
            uniq = uniq[:TARGET]
        trimmed = len(qs) - len(uniq)

        head_obj = {k: obj[k] for k in obj if k != "questions"}
        parts = []
        for k in ["id", "grade", "semester", "order", "title", "desc", "kd"]:
            if k in head_obj:
                parts.append("'%s':%s" % (k, val(head_obj.pop(k))))
        for k, v in head_obj.items():
            parts.append("'%s':%s" % (k, val(v)))
        parts.append("'questions':[\n" + ",\n".join(dump_q(q) for q in uniq) + "\n]")

        p.write_text(head + "window.BSRegister({\n" + ",\n".join(parts) + "\n});\n",
                     encoding="utf-8")
        if trimmed:
            print(f"{p.name}: {len(qs)} -> {len(uniq)} soal (duplikat {removed}, dipangkas {trimmed - removed})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
