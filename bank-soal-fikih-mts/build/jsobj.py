#!/usr/bin/env python3
"""Parser literal objek JavaScript -> objek Python.

Dirancang untuk berkas data bank soal yang seluruh string-nya memakai kutip
tunggal. Parser bersifat string-aware sehingga tanda kutip, titik dua, dan
koma di dalam teks soal tidak merusak proses parsing.
"""
import re

IDENT = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")
KEYWORD = {
    "true": True, "false": False, "null": None, "undefined": None,
}


def strip_comments(src):
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


class Parser:
    def __init__(self, src, start=0, cleaned=None):
        """cleaned: teks yang sudah dibuang komentarnya (bila start dihitung
        dari teks asli, teks ini WAJIB dilewatkan agar indeks tidak bergeser)."""
        self.s = cleaned if cleaned is not None else src
        self.i = start
        self.n = len(self.s)

    # ---------- util ----------
    def ws(self):
        while self.i < self.n and self.s[self.i] in " \t\r\n":
            self.i += 1

    def peek(self):
        self.ws()
        return self.s[self.i] if self.i < self.n else ""

    def eat(self, ch):
        self.ws()
        if self.i < self.n and self.s[self.i] == ch:
            self.i += 1
            return True
        return False

    def expect(self, ch):
        if not self.eat(ch):
            raise ValueError("diharapkan %r pada posisi %d, ditemukan %r"
                             % (ch, self.i, self.s[self.i:self.i + 40]))

    # ---------- nilai ----------
    def parse(self):
        v = self.value()
        return v

    def value(self):
        c = self.peek()
        if c == "{":
            return self.obj()
        if c == "[":
            return self.arr()
        if c in "\"'":
            return self.string()
        return self.scalar()

    def obj(self):
        self.expect("{")
        d = {}
        if self.eat("}"):
            return d
        while True:
            key = self.key()
            self.expect(":")
            d[key] = self.value()
            if self.eat(","):
                if self.peek() == "}":
                    self.i += 1
                    break
                continue
            self.expect("}")
            break
        return d

    def key(self):
        c = self.peek()
        if c in "\"'":
            return self.string()
        m = IDENT.match(self.s, self.i)
        if not m:
            raise ValueError("kunci objek tidak valid pada posisi %d: %r"
                             % (self.i, self.s[self.i:self.i + 40]))
        k = m.end()
        while k < self.n and self.s[k] in " \t\r\n":
            k += 1
        if k < self.n and self.s[k] == ":":
            self.i = m.end()
            return m.group(0)
        if m.group(0) in KEYWORD:
            self.i = m.end()
            return m.group(0)
        raise ValueError("kunci objek tidak valid pada posisi %d: %r"
                         % (self.i, self.s[self.i:self.i + 40]))

    def arr(self):
        self.expect("[")
        a = []
        if self.eat("]"):
            return a
        while True:
            a.append(self.value())
            if self.eat(","):
                if self.peek() == "]":
                    self.i += 1
                    break
                continue
            self.expect("]")
            break
        return a

    def string(self):
        self.ws()
        q = self.s[self.i]
        i = self.i + 1
        res = []
        while i < self.n:
            ch = self.s[i]
            if ch == "\\" and i + 1 < self.n:
                nxt = self.s[i + 1]
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
                elif nxt == "0":
                    res.append("\0")
                elif nxt == "u" and i + 5 < self.n:
                    res.append(chr(int(self.s[i + 2:i + 6], 16)))
                    i += 6
                    continue
                elif nxt == "x" and i + 3 < self.n:
                    res.append(chr(int(self.s[i + 2:i + 4], 16)))
                    i += 4
                    continue
                else:
                    res.append(nxt)
                i += 2
                continue
            if ch == q:
                i += 1
                break
            res.append(ch)
            i += 1
        self.i = i
        return "".join(res)

    def scalar(self):
        self.ws()
        m = re.match(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", self.s[self.i:])
        if m:
            self.i += m.end()
            t = m.group(0)
            return float(t) if ("." in t or "e" in t or "E" in t) else int(t)
        m = IDENT.match(self.s, self.i)
        if m and m.group(0) in KEYWORD:
            self.i = m.end()
            return KEYWORD[m.group(0)]
        raise ValueError("nilai tidak dikenal pada posisi %d: %r"
                         % (self.i, self.s[self.i:self.i + 40]))


def loads(src):
    return Parser(strip_comments(src)).parse()


def extract_register(src):
    """Ambil objek pada window.BSRegister({...});"""
    cleaned = strip_comments(src)
    ms = list(re.finditer(r"window\.BSRegister\s*\(", cleaned))
    if not ms:
        raise ValueError("pola window.BSRegister( tidak ditemukan")
    return Parser(cleaned, ms[-1].end()).parse()


def extract_index(src):
    """Ambil array pada window.__BS.index = [...]; (pencocokan terakhir)."""
    cleaned = strip_comments(src)
    ms = list(re.finditer(r"window\.__BS\.index(?=\s*=[^=])", cleaned))
    if not ms:
        raise ValueError("pola window.__BS.index tidak ditemukan")
    m = ms[-1]
    i = m.end()
    while i < len(cleaned) and cleaned[i] in " \t\r\n=":
        i += 1
    return Parser(cleaned, i).parse()
