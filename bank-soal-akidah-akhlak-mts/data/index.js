/* ============================================================
   Bank Soal Akidah Akhlak MTs — manifes materi
   Ruang lingkup: KMA 183 Tahun 2019 (Akidah Akhlak MTs)
   32 materi × 50 soal = 1600 soal pilihan ganda HOTS
   ============================================================ */
window.__BS = window.__BS || {topics:{}, index:[]};
window.BSRegister = function(o){ window.__BS.topics[o.id] = o; };

window.__BS.index = [
  /* ===== KELAS VII — SEMESTER 1 ===== */
  { id:'k7-dalil-naqli-aqli',  file:'k7/dalil-naqli-aqli.js',  title:'Dalil Naqli & Aqli tentang Allah',        grade:7, semester:1 },
  { id:'k7-allah-asmaul-husna',file:'k7/allah-asmaul-husna.js',title:'Allah, Asmaul Husna & Sifat Wajib',       grade:7, semester:1 },
  { id:'k7-iman-malaikat',     file:'k7/iman-malaikat.js',     title:'Iman kepada Malaikat',                    grade:7, semester:1 },
  { id:'k7-syukur',            file:'k7/syukur.js',            title:'Syukur Nikmat & Hidup Sederhana',         grade:7, semester:1 },
  { id:'k7-jujur',             file:'k7/jujur.js',             title:'Hidup Jujur',                             grade:7, semester:1 },
  { id:'k7-hormat-taat',       file:'k7/hormat-taat.js',       title:'Hormat & Taat kepada Orang Tua dan Guru', grade:7, semester:1 },

  /* ===== KELAS VII — SEMESTER 2 ===== */
  { id:'k7-riya-nifaq',        file:'k7/riya-nifaq.js',        title:'Menghindari Riya, Nifaq & Takabur',       grade:7, semester:2 },
  { id:'k7-adab-berpakaian',   file:'k7/adab-berpakaian.js',   title:'Adab Berpakaian & Berhias',               grade:7, semester:2 },
  { id:'k7-adab-makan-minum',  file:'k7/adab-makan-minum.js',  title:'Adab Makan, Minum & Perjalanan',          grade:7, semester:2 },
  { id:'k7-kisah-sabar',       file:'k7/kisah-sabar.js',       title:'Kisah Ketabahan Nabi Ayyub & Keluarga Nabi Yakub', grade:7, semester:2 },
  { id:'k7-asmaul-husna-2',    file:'k7/asmaul-husna-2.js',    title:'Asmaul Husna (al-Karim, al-Mumin, al-Wakil, al-Matin)', grade:7, semester:2 },

  /* ===== KELAS VIII — SEMESTER 1 ===== */
  { id:'k8-tawakal-ikhtiar',   file:'k8/tawakal-ikhtiar.js',   title:'Iman kepada Takdir, Ikhtiar, Doa & Tawakal', grade:8, semester:1 },
  { id:'k8-tawadu-ta-at-qanaah',file:'k8/tawadu-ta-at-qanaah.js',title:'Tawadu, Taat & Qanaah',                grade:8, semester:1 },
  { id:'k8-hasad-ghibah-fitnah',file:'k8/hasad-ghibah-fitnah.js',title:'Menghindari Hasad, Ghibah & Fitnah',   grade:8, semester:1 },
  { id:'k8-adab-ibadah',       file:'k8/adab-ibadah.js',       title:'Adab Beribadah & Membaca Al-Quran',       grade:8, semester:1 },
  { id:'k8-adab-silaturahmi',  file:'k8/adab-silaturahmi.js',  title:'Adab Menjenguk, Melawat & Silaturahmi',   grade:8, semester:1 },
  { id:'k8-kisah-ulul-azmi',   file:'k8/kisah-ulul-azmi.js',   title:'Kisah Ketabahan Nabi Ulul Azmi',          grade:8, semester:1 },
  { id:'k8-asmaul-husna-3',    file:'k8/asmaul-husna-3.js',    title:'Asmaul Husna (al-Waliy, al-Hamid, asy-Syakur, al-Aliyy)', grade:8, semester:1 },

  /* ===== KELAS VIII — SEMESTER 2 ===== */
  { id:'k8-hormat-guru',       file:'k8/hormat-guru.js',       title:'Adab terhadap Guru & Orang Tua',          grade:8, semester:2 },
  { id:'k8-akhlak-tercela-2',  file:'k8/akhlak-tercela-2.js',  title:'Menghindari Minuman Keras, Narkoba & Judi', grade:8, semester:2 },
  { id:'k8-adab-muamalah',     file:'k8/adab-muamalah.js',     title:'Adab Muamalah & Etos Kerja',              grade:8, semester:2 },
  { id:'k8-kisah-sahabat',     file:'k8/kisah-sahabat.js',     title:'Kisah Kesungguhan Ibadah Para Sahabat',   grade:8, semester:2 },

  /* ===== KELAS IX — SEMESTER 1 ===== */
  { id:'k9-mengharap-ridha',   file:'k9/mengharap-ridha.js',   title:'Mengharap Ridha Allah & Ikhlas Beramal',  grade:9, semester:1 },
  { id:'k9-tauhid-syirik',     file:'k9/tauhid-syirik.js',     title:'Tauhid, Syirik, Murtad & Tahayul',        grade:9, semester:1 },
  { id:'k9-qadha-qadar',       file:'k9/qadha-qadar.js',       title:'Qadha, Qadar & Sikap terhadap Takdir',    grade:9, semester:1 },
  { id:'k9-surga-neraka',      file:'k9/surga-neraka.js',      title:'Iman kepada Hari Akhir, Surga & Neraka',  grade:9, semester:1 },
  { id:'k9-akhlak-terpuji-9',  file:'k9/akhlak-terpuji-9.js',  title:'Akhlak Terpuji: Sabar, Syukur, Istiqamah & Husnuzan', grade:9, semester:1 },
  { id:'k9-akhlak-tercela-9',  file:'k9/akhlak-tercela-9.js',  title:'Akhlak Tercela: Namimah, Su uzan, Takabur & Ananiah', grade:9, semester:1 },

  /* ===== KELAS IX — SEMESTER 2 ===== */
  { id:'k9-adab-medsos',       file:'k9/adab-medsos.js',       title:'Adab Menggunakan Media Sosial',           grade:9, semester:2 },
  { id:'k9-islam-seni-budaya', file:'k9/islam-seni-budaya.js', title:'Islam, Seni, Budaya & Teknologi',         grade:9, semester:2 },
  { id:'k9-kisah-dakwah-nabi', file:'k9/kisah-dakwah-nabi.js', title:'Kisah Perjuangan Dakwah Nabi & Sahabat',  grade:9, semester:2 },
  { id:'k9-muslim-sejati',     file:'k9/muslim-sejati.js',     title:'Ciri Muslim Sejati & Akhlakul Karimah',   grade:9, semester:2 }
];
