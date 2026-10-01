#!/usr/bin/env python3
"""Migrasi satu-kali: seragamkan berkas data topik menjadi literal objek JS
dengan SELURUH string memakai kutip tunggal (single-quoted), sehingga bebas
ambiguitas dan pasti dapat diparsing.

Jalankan sekali:  python3 build/normalize_data.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDENT = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")


def strip_comments(src: str) -> str:
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c in "\"'":
            q, j = c, i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == q:
                    j += 1
                    break
                j += 1
            out.append(src[i:j])
            i = j
            continue
        if src.startswith("/*", i):
            k = src.find("*/", i + 2)
            i = (k + 2) if k != -1 else n
            continue
        if src.startswith("//", i):
            k = src.find("\n", i)
            i = k if k != -1 else n
            continue
        out.append(c)
        i += 1
    return "".join(out)


def decode_js_string(raw: str) -> str:
    """raw = teks lengkap termasuk kutip pembuka/penutup -> isi string asli."""
    q = raw[0]
    body = raw[1:-1]
    res, i = [], 0
    while i < len(body):
        ch = body[i]
        if ch == "\\" and i + 1 < len(body):
            nxt = body[i + 1]
            if nxt == "n":
                res.append("\n")
            elif nxt == "t":
                res.append("\t")
            elif nxt == "r":
                res.append("\r")
            elif nxt == "b":
                res.append("\b")
            elif nxt == "f":
                res.append("\f")
            elif nxt == "u" and i + 5 < len(body):
                res.append(chr(int(body[i + 2:i + 6], 16)))
                i += 6
                continue
            else:
                res.append(nxt)
            i += 2
            continue
        res.append(ch)
        i += 1
    return "".join(res)


def encode_sq(text: str) -> str:
    """Encode teks menjadi string kutip tunggal JS yang valid."""
    res = []
    for ch in text:
        if ch == "\\":
            res.append("\\\\")
        elif ch == "'":
            res.append("\\'")
        elif ch == "\n":
            res.append("\\n")
        elif ch == "\r":
            continue
        elif ch == "\t":
            res.append("\\t")
        else:
            res.append(ch)
    return "'" + "".join(res) + "'"


def tokenize(src: str):
    """Ubah teks JS menjadi daftar token: ('str', nilai) | ('raw', teks)."""
    toks, i, n, buf = [], 0, len(src), []

    def flush():
        if buf:
            toks.append(("raw", "".join(buf)))
            buf.clear()

    while i < n:
        c = src[i]
        if c in "\"'":
            q, j = c, i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == q:
                    j += 1
                    break
                j += 1
            flush()
            toks.append(("str", decode_js_string(src[i:j])))
            i = j
            continue
        buf.append(c)
        i += 1
    flush()
    return toks


def render(toks) -> str:
    """Render token: string -> kutip tunggal; raw -> kunci objek diberi kutip."""
    out = []
    pending = ""
    for kind, val in toks:
        if kind == "str":
            out.append(pending)
            pending = ""
            out.append(encode_sq(val))
        else:
            pending += val
    out.append(pending)
    text = "".join(out)

    # beri kutip pada kunci objek yang belum berkutip
    def quote_key(m):
        return m.group(1) + "'" + m.group(2) + "'" + m.group(3)

    text = re.sub(r"([{,]\s*)([A-Za-z_$][A-Za-z0-9_$]*)(\s*:)", quote_key, text)
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    return text


def main():
    files = sorted((ROOT / "data").rglob("*.js"))
    for p in files:
        if p.name == "index.js":
            continue
        src = p.read_text(encoding="utf-8")
        head = ""
        m = re.match(r"(/\*[\s\S]*?\*/\s*)", src)
        if m:
            head = m.group(1)
        body = src[len(head):]
        try:
            new = head + render(tokenize(strip_comments(body)))
        except Exception as exc:
            print(f"GAGAL {p.name}: {exc}")
            continue
        if new != src:
            p.write_text(new, encoding="utf-8")
            print(f"OK  {p.relative_to(ROOT)}")
        else:
            print(f"--  {p.relative_to(ROOT)} (sudah seragam)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
