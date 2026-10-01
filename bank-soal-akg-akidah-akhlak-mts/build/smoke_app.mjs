// Uji asap berkas HTML hasil bangun: memastikan data tertanam, JSON valid,
// jumlah soal benar, dan semua id unik. Jalankan: node build/smoke_app.mjs <berkas.html>
import { readFileSync } from "node:fs";

const file = process.argv[2];
if (!file) {
  console.error("Pemakaian: node build/smoke_app.mjs <berkas.html>");
  process.exit(2);
}
const html = readFileSync(file, "utf8");

let fail = 0;
function check(label, cond, extra) {
  console.log((cond ? "OK   " : "GAGAL") + "  " + label + (extra ? "  (" + extra + ")" : ""));
  if (!cond) fail++;
}

check("berkas memuat blok data akg-data", html.includes('id="akg-data"'));
check("berkas memuat script aplikasi", html.includes("__AKG_DATA__"));
check("berkas memuat CSS tertanam", html.includes("--brand"));

const m = html.match(/<script id="akg-data" type="application\/json">([\s\S]*?)<\/script>/);
check("blok data dapat diekstrak", !!m);
let DATA = null;
if (m) {
  try {
    DATA = JSON.parse(m[1]);
    check("JSON data valid", true);
  } catch (e) {
    check("JSON data valid", false, e.message);
  }
}

if (DATA) {
  const soal = DATA.soal || [];
  const ped = soal.filter((s) => s.kategori === "pedagogik").length;
  const pro = soal.filter((s) => s.kategori === "profesional").length;
  check("jumlah soal = 150", soal.length === 150, String(soal.length));
  check("pedagogik = 50", ped === 50, String(ped));
  check("profesional = 100", pro === 100, String(pro));

  const ids = new Set();
  let dup = 0, badKey = 0, badOpt = 0, noBahasan = 0, badTipe = 0;
  for (const s of soal) {
    if (ids.has(s.id)) dup++;
    ids.add(s.id);
    if (!s.bahasan) noBahasan++;
    if (!Array.isArray(s.opsi) || s.opsi.length !== 4) badOpt++;
    if (s.tipe === "pg") {
      if (!Number.isInteger(s.kunci) || s.kunci < 0 || s.kunci > 3) badKey++;
    } else if (s.tipe === "pgk") {
      if (!Array.isArray(s.kunci) || s.kunci.length !== 2) badKey++;
    } else {
      badTipe++;
    }
  }
  check("id unik", dup === 0, dup + " duplikat");
  check("kunci sesuai tipe", badKey === 0, String(badKey));
  check("semua soal punya 4 opsi", badOpt === 0, String(badOpt));
  check("semua soal punya pembahasan", noBahasan === 0, String(noBahasan));
  check("tipe hanya pg/pgk", badTipe === 0, String(badTipe));

  const pgk = soal.filter((s) => s.tipe === "pgk").length;
  const bs = soal.filter((s) => s.tipe === "bs").length;
  check("tidak ada sisa tipe bs", bs === 0, String(bs));
  console.log("Info: " + soal.length + " soal, " + pgk + " PGK, " + DATA.kisi.aspekPedagogik.length + " aspek pedagogik, " + DATA.rangkuman.seksi.length + " seksi rangkuman");
}

console.log(fail ? "\nUJI ASAP GAGAL (" + fail + ")" : "\nSEMUA UJI ASAP LULUS");
process.exit(fail ? 1 : 0);
