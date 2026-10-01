// Uji antarmuka aplikasi di DOM sungguhan memakai jsdom.
// Prasyarat: npm install jsdom (di luar folder ini, misalnya /tmp).
// Jalankan: node build/test_app.mjs Bank-Soal-AKG-Akidah-Akhlak-MTs-1file.html
import { readFileSync } from "node:fs";
import { JSDOM, VirtualConsole } from "jsdom";

const html = readFileSync(process.argv[2], "utf8");
const dom = new JSDOM(html, {
  runScripts: "dangerously",
  pretendToBeVisual: true,
  url: "https://contoh.test/",
  virtualConsole: new VirtualConsole(),
});
await new Promise((r) => setTimeout(r, 400));
const w = dom.window;
const d = w.document;
let fail = 0;
const ok = (label, cond, extra) => {
  console.log((cond ? "OK   " : "GAGAL") + "  " + label + (extra ? "  (" + extra + ")" : ""));
  if (!cond) fail++;
};

// --- struktur halaman ---
ok("5 tab tersedia", d.querySelectorAll(".tab").length === 5);
ok("tabel kisi-kisi terisi", d.querySelectorAll("#kisi-body tbody tr").length === 2);
ok("rangkuman 10 seksi", d.querySelectorAll("#materi-body details").length === 10);
ok("kunci memuat 150 butir", d.querySelectorAll("#kunci-body .kunciitem").length === 150);
ok("chip statistik terisi", (d.getElementById("meta-stat").textContent || "").includes("150"));

// --- latihan ---
d.getElementById("btn-tab-latihan").click();
d.getElementById("chk-acak").checked = false;
d.getElementById("btn-mulai").click();
const q1 = d.querySelector(".qtext")?.textContent || "";
ok("soal pertama tampil", q1.length > 20, q1.slice(0, 40) + "...");
ok("empat opsi dirender", d.querySelectorAll(".opt").length === 4);
ok("label topik terisi", (d.querySelector(".chip.gray")?.textContent || "").length > 3);

d.querySelectorAll(".opt")[0].click();
ok("umpan balik muncul setelah menjawab", !!d.querySelector("#quiz-area .feedback"));
ok("kunci tampil di umpan balik", (d.querySelector(".feedback")?.textContent || "").includes("Kunci jawaban"));

const next = [...d.querySelectorAll("#quiz-area .btn")].find((b) => b.textContent.includes("Berikutnya"));
next.click();
const q2 = d.querySelector(".qtext")?.textContent || "";
ok("soal kedua berbeda", q2 !== q1 && q2.length > 20);
ok("navigasi Sebelumnya aktif", ![...d.querySelectorAll("#quiz-area .btn")].find((b) => b.textContent.includes("Sebelumnya")).disabled);

// --- penyimpanan dan data ---
ok("progres tersimpan di localStorage", (w.localStorage.getItem("akg-akidah-akhlak-mts-v1") || "").length > 20);
ok("kotak pencarian kunci ada", !!d.querySelector("#kunci-body input"));
const data = JSON.parse(html.match(/<script id="akg-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
ok("11 soal PGK terdata", data.soal.filter((s) => s.tipe === "pgk").length === 11);

console.log(fail ? "\nUJI ANTARMUKA GAGAL (" + fail + ")" : "\nSEMUA UJI ANTARMUKA LULUS");
process.exit(fail ? 1 : 0);
