"""Parser minimal untuk objek literal JS (kunci tanpa tanda kutip, string kutip tunggal).

Dipakai untuk membaca data/index.js dan data/k*/<materi>.js tanpa Node.js.
"""
from __future__ import annotations

KEY_OK = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$")


class ParseError(Exception):
    pass


class _Reader:
    __slots__ = ("s", "i", "n")

    def __init__(self, s: str):
        self.s = s
        self.i = 0
        self.n = len(s)

    def ws(self) -> None:
        s, n = self.s, self.n
        i = self.i
        while i < n:
            c = s[i]
            if c in " \t\r\n":
                i += 1
            elif c == "/" and i + 1 < n and s[i + 1] == "/":
                j = s.find("\n", i)
                i = n if j < 0 else j + 1
            elif c == "/" and i + 1 < n and s[i + 1] == "*":
                j = s.find("*/", i + 2)
                i = n if j < 0 else j + 2
            else:
                break
        self.i = i

    def peek(self) -> str:
        self.ws()
        return self.s[self.i] if self.i < self.n else ""

    def eat(self, ch: str) -> None:
        self.ws()
        if self.i >= self.n or self.s[self.i] != ch:
            got = self.s[self.i] if self.i < self.n else "EOF"
            raise ParseError(f"harapkan {ch!r} dapat {got!r} di offset {self.i}")
        self.i += 1

    def try_eat(self, ch: str) -> bool:
        self.ws()
        if self.i < self.n and self.s[self.i] == ch:
            self.i += 1
            return True
        return False

    def string(self) -> str:
        s, n = self.s, self.n
        q = s[self.i]
        if q not in "'\"":
            raise ParseError(f"bukan awal string di offset {self.i}")
        self.i += 1
        out = []
        while self.i < n:
            c = s[self.i]
            if c == "\\":
                self.i += 1
                if self.i >= n:
                    break
                e = s[self.i]
                out.append({"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f",
                            "v": "\v", "0": "\0", "\\": "\\", "'": "'", '"': '"',
                            "/": "/"}.get(e, e))
                self.i += 1
            elif c == q:
                self.i += 1
                return "".join(out)
            else:
                out.append(c)
                self.i += 1
        raise ParseError("string tidak ditutup")

    def key(self) -> str:
        s, n = self.s, self.n
        self.ws()
        if self.i < n and s[self.i] in "'\"":
            return self.string()
        j = self.i
        while j < n and s[j] in KEY_OK:
            j += 1
        if j == self.i:
            raise ParseError(f"bukan kunci di offset {self.i}")
        k = s[self.i:j]
        self.i = j
        return k

    def number(self):
        s, n = self.s, self.n
        self.ws()
        j = self.i
        if j < n and s[j] in "-+":
            j += 1
        k = j
        while k < n and (s[k].isdigit() or s[k] in ".eE+-"):
            if s[k] in "+-" and (k == j or s[k - 1] not in "eE"):
                break
            k += 1
        tok = s[self.i:k]
        if not tok:
            raise ParseError(f"bukan angka di offset {self.i}")
        self.i = k
        return float(tok) if any(c in tok for c in ".eE") else int(tok)

    def literal(self):
        for name, val in (("true", True), ("false", False), ("null", None)):
            if self.s.startswith(name, self.i):
                self.i += len(name)
                return val
        raise ParseError(f"literal tak dikenal di offset {self.i}: {self.s[self.i:self.i+12]!r}")


def parse_value(r: _Reader):
    c = r.peek()
    if c == "{":
        r.eat("{")
        d = {}
        if r.peek() == "}":
            r.eat("}")
            return d
        while True:
            k = r.key()
            r.eat(":")
            d[k] = parse_value(r)
            if r.try_eat(","):
                if r.peek() == "}":
                    r.eat("}")
                    return d
                continue
            r.eat("}")
            return d
    if c == "[":
        r.eat("[")
        a = []
        if r.peek() == "]":
            r.eat("]")
            return a
        while True:
            a.append(parse_value(r))
            if r.try_eat(","):
                if r.peek() == "]":
                    r.eat("]")
                    return a
                continue
            r.eat("]")
            return a
    if c in "'\"":
        r.ws()
        return r.string()
    if c == "-" or c.isdigit():
        return r.number()
    return r.literal()


def _slice_call(src: str, marker: str) -> str:
    a = src.find(marker)
    if a < 0:
        raise ParseError(f"penanda {marker!r} tidak ditemukan")
    a = src.index("(", a) + 1
    depth, i, n, in_str, q = 0, a, len(src), False, ""
    while i < n:
        c = src[i]
        if in_str:
            if c == "\\":
                i += 2
                continue
            if c == q:
                in_str = False
        elif c in "'\"":
            in_str, q = True, c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            if depth == 0:
                return src[a:i]
            depth -= 1
        i += 1
    raise ParseError("tanda kurung tidak seimbang")


def extract_register(src: str) -> dict:
    """Ambil objek pada window.BSRegister({...}) — satu topik/materi."""
    return parse_value(_Reader(_slice_call(src, "window.BSRegister")))


def extract_addtypes(src: str) -> dict:
    """Ambil objek pada window.BSAddTypes({...}) — tipe soal tambahan satu bab."""
    return parse_value(_Reader(_slice_call(src, "window.BSAddTypes")))


def extract_index(src: str) -> list:
    """Ambil array pada window.__BS.index = [...]."""
    a = src.find("window.__BS.index")
    if a < 0:
        raise ParseError("window.__BS.index tidak ditemukan")
    a = src.index("[", a)
    r = _Reader(src)
    r.i = a
    return parse_value(r)
