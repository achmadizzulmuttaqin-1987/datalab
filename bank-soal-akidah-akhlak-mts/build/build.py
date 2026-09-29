"""Gabungkan index.html + app.js + seluruh data/*.js menjadi satu file HTML mandiri.

Jalankan: python3 build/build.py
Output : Bank-Soal-Akidah-Akhlak-MTs-1file.html
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jsobj  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Bank-Soal-Akidah-Akhlak-MTs-1file.html"
REQ_TOPIC = {"id", "grade", "semester", "order", "title", "questions"}
REQ_Q = {"options", "answer", "text"}
MARKER = "<script>\nwindow.__BS"


def read_index() -> list:
    return jsobj.extract_index((ROOT / "data" / "index.js").read_text(encoding="utf-8"))


def read_topic(path: Path) -> dict:
    return jsobj.extract_register(path.read_text(encoding="utf-8"))


def main() -> int:
    index = read_index()
    chunks, total, problems, missing = [], 0, [], []
    per_topic = []

    for meta in index:
        p = ROOT / "data" / meta["file"]
        if not p.exists():
            missing.append(meta["file"])
            continue
        try:
            obj = read_topic(p)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{meta['file']}: {exc}")
            continue

        for k in REQ_TOPIC - set(obj):
            problems.append(f"{meta['file']}: field '{k}' hilang")
        if obj.get("id") != meta["id"]:
            problems.append(f"{meta['file']}: id tidak cocok ({obj.get('id')} vs {meta['id']})")
        if obj.get("grade") != meta["grade"]:
            problems.append(f"{meta['file']}: grade tidak cocok")
        if obj.get("semester") != meta["semester"]:
            problems.append(f"{meta['file']}: semester tidak cocok")

        qs = obj.get("questions", [])
        seen = {}
        for i, q in enumerate(qs, 1):
            tag = f"{meta['file']} #{i}"
            for k in REQ_Q - set(q):
                problems.append(f"{tag}: field '{k}' hilang")
            if not q.get("explanation"):
                problems.append(f"{tag}: tidak ada pembahasan")
            opts = q.get("options", [])
            if not 4 <= len(opts) <= 5:
                problems.append(f"{tag}: jumlah opsi {len(opts)}")
            if any(not o for o in opts):
                problems.append(f"{tag}: ada opsi kosong")
            a = q.get("answer")
            ok_ans = isinstance(a, int) and not isinstance(a, bool) and 0 <= a < len(opts)
            if not ok_ans:
                problems.append(f"{tag}: answer tidak valid ({a})")
            if q.get("level") not in ("HOTS", "MOTS", "LOTS"):
                problems.append(f"{tag}: level tidak valid ({q.get('level')})")
            key = re.sub(r"\s+", " ", (q.get("text") or "")).strip()[:90]
            if key in seen:
                problems.append(f"{tag}: soal duplikat dengan #{seen[key]}")
            seen[key] = i
            if ok_ans:
                for j, o in enumerate(opts):
                    if o and j != a and o == opts[a]:
                        problems.append(f"{tag}: opsi {j} duplikat dengan kunci")

        total += len(qs)
        per_topic.append((meta["id"], len(qs)))
        chunks.append(
            "window.BSRegister("
            + json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            + ");"
        )

    if problems:
        print(f"MASALAH ({len(problems)}):")
        for x in problems[:80]:
            print("  -", x)
    if missing:
        print(f"BELUM ADA ({len(missing)}):")
        for x in missing:
            print("  -", x)

    idx_html = (ROOT / "index.html").read_text(encoding="utf-8")
    app_js = (ROOT / "app.js").read_text(encoding="utf-8")
    inline = (
        "<script>\nwindow.__BS = window.__BS || {topics:{}, index:[]};\n"
        "window.BSRegister = function(o){ window.__BS.topics[o.id] = o; };\n"
        "window.__BS.index = " + json.dumps(index, ensure_ascii=False) + ";\n"
        + "\n".join(chunks)
        + "\n</script>\n<script>\n" + app_js + "\n</script>\n"
        "<script>App.start(null);</script>\n"
    )
    start = idx_html.index(MARKER)
    end = idx_html.index("</body>")
    OUT.write_text(idx_html[:start] + inline + idx_html[end:], encoding="utf-8")

    bad_count = [t for t, n in per_topic if n != 50]
    print(f"\nTopik valid : {len(chunks)}/{len(index)}")
    print(f"Total soal  : {total}")
    if bad_count:
        print("Topik bukan 50 soal:", bad_count)
    print(f"Output      : {OUT.name} ({OUT.stat().st_size/1024:.0f} KB)")
    return 1 if problems or missing else 0


if __name__ == "__main__":
    sys.exit(main())
