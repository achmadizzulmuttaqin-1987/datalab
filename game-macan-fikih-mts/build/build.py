"""Bangun game standalone Jejak Cilik (satu berkas HTML).

Sumber:
  build/shell.html      kerangka + markup
  build/game.css        gaya antarmuka
  build/js/*.js         mesin 3D + alur permainan (digabung berurutan)
  build/questions.json  1.500 soal dari bank-soal-fikih-mts
  build/three.min.js    three.js r160 (MIT) disematkan agar offline

Keluaran:
  index.html            game mandiri ±2 MB, tanpa permintaan jaringan
  Jejak-Cilik-Fikih-MTs-1file.html  salinan nama sesuai konvensi repo

Jalankan: python3 build/build.py
"""
from __future__ import annotations

import datetime
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "index.html"
OUT_ALT = ROOT / "Jejak-Cilik-Fikih-MTs-1file.html"

JS_ORDER = ["00-core.js", "10-world.js", "20-game.js", "30-ui.js"]


def main() -> int:
    shell = (HERE / "shell.html").read_text(encoding="utf-8")
    css = (HERE / "game.css").read_text(encoding="utf-8")
    questions = (HERE / "questions.json").read_text(encoding="utf-8")
    three = (HERE / "three.min.js").read_text(encoding="utf-8")

    js_parts = []
    for name in JS_ORDER:
        js_parts.append(f"/* ---- {name} ---- */\n" + (HERE / "js" / name).read_text(encoding="utf-8"))
    game_js = "\n".join(js_parts)

    # Pemeriksaan pengaman: jangan sampai penutup tag skrip muncul di dalam data.
    if "</script" in three.lower():
        raise SystemExit("three.min.js mengandung </script>")
    if "</script" in game_js.lower():
        raise SystemExit("game.js mengandung </script>")

    meta = json.loads(questions)["meta"]
    stamp = datetime.date.today().isoformat()
    banner = (
        "<!--\n"
        f"  Jejak Cilik — Petualangan 3D Fikih MTs ({stamp})\n"
        f"  {meta['nBabs']} bab · {meta['nCaves']} goa · {meta['nQuestions']} soal pilihan ganda\n"
        "  Sumber soal: bank-soal-fikih-mts (Kelas 7-9, KMA 183/2019)\n"
        "  Mesin 3D: three.js r160 (MIT License, https://threejs.org)\n"
        "  Seluruh berkas ini mandiri: tidak ada permintaan jaringan, data, atau aset luar.\n"
        "-->\n"
    )

    html = shell
    html = html.replace("/*__CSS__*/", css)
    html = html.replace("__DATA__", questions)
    html = html.replace("/*__THREE__*/", three)
    html = html.replace(
        "/*__GAME_JS__*/",
        "(function(){\n'use strict';\n" + game_js + "\n})();",
    )
    html = banner + html
    OUT.write_text(html, encoding="utf-8")
    OUT_ALT.write_text(html, encoding="utf-8")

    size_mb = OUT.stat().st_size / (1024 * 1024)
    print(f"OK  {OUT}  ({size_mb:.2f} MB)")
    print(f"OK  {OUT_ALT.name}  (salinan)")
    print(f"    bab={meta['nBabs']} goa={meta['nCaves']} soal={meta['nQuestions']}")
    print(f"    css={len(css)/1024:.0f} KB  js={len(game_js)/1024:.0f} KB  three={len(three)/1024:.0f} KB  data={len(questions)/1024:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
