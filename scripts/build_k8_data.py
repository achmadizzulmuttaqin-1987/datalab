#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from generate_decks_k8_k9 import HTML_TEMPLATE

chapters_k8 = [
    {
        "filename": "bab-1-al-quran-dan-keistimewaannya.html",
        "full_title": "BAB I: Al-Qur'an dan Keistimewaannya — Akidah Akhlak Kelas VIII MTs",
        "chapter_label": "BAB I: Al-Qur'an dan Keistimewaannya",
        "badge_text": "K8 • SEMESTER 1",
        "theme_color": "#38bdf8",
        "theme_light": "#7dd3fc",
        "theme_subtle": "rgba(56, 189, 248, 0.16)",
        "badge_gradient": "#0284c7, #38bdf8",
        "radial_color": "#0c2d54",
        "slides": [
            {
                "title": "Al-Qur'an dan Keistimewaannya",
                "badge": "PENGANTAR BAB I",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">📖✨</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #38bdf8; margin: 12px 0;">BAB I: AL-QUR'AN DAN KEISTIMEWAANNYA</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Kalamullah yang abadi, mukjizat terbesar sepanjang zaman, dan pedoman hidup utama umat manusia hingga akhir hayat.
                  </p>
                  <div class="content-grid-3" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">📌 Hakikat & Pengertian</div>
                      <div class="card-desc">Definisi syar'i wahyu Allah, sejarah diturunkannya secara berangsur-angsur (*tanjim*).</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">🌟 Keistimewaan Mukjizat</div>
                      <div class="card-desc">Terpelihara dari kepalsuan, tata bahasa indah tak tertandingi, dan mukjizat ilmiah.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">🛡️ Fungsi & Pengamalan</div>
                      <div class="card-desc">Sebagai *Asy-Syifa'*, *Al-Huda*, *Al-Furqan*, serta adab menghafal & mentadabburinya.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Pengertian dan Hakikat Al-Qur'an",
                "badge": "KONSEP DASAR",
                "content": """
                <p style="font-size: 22pt; line-height: 1.6; margin-bottom: 20px;">
                  Secara bahasa (etimologi), kata <strong>Al-Qur'an</strong> berakar dari kata <em>qara'a - yaqra'u - qur'anan</em> (قَرَأَ - يَقْرَأُ - قُرْآنًا) yang berarti bacaan atau apa yang dibaca berulang-ulang.
                </p>
                <div class="card-box card-box-accent" style="margin-bottom: 20px;">
                  <div class="card-title">📖 Definisi Syar'i (Istilah Para Ulama Ushul Fiqih):</div>
                  <div class="card-desc" style="font-size: 22pt; line-height: 1.6;">
                    <em>"Kalam Allah yang diturunkan kepada Nabi Muhammad Saw. melalui perantaraan Malaikat Jibril as. dengan lafaz dan makna berbahasa Arab, dinukilkan secara mutawatir, termaktub dalam mushaf, membacanya bernilai ibadah, diawali dengan surah Al-Fatihah dan diakhiri dengan surah An-Nas."</em>
                  </div>
                </div>
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">1. Turun Secara Berangsur</div>
                    <div class="card-desc">Diturunkan selama kurun waktu 22 tahun 2 bulan 22 hari (sekitar 23 tahun) untuk meneguhkan hati Rasulullah dan menjawab peristiwa kehidupan umat.</div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">2. Mutawatir & Bernilai Ibadah</div>
                    <div class="card-desc">Diriwayatkan oleh banyak perawi pada tiap generasi sehingga mustahil bersepakat dusta. Setiap satu huruf yang dibaca diganjar sepuluh kebaikan.</div>
                  </div>
                </div>
                """
            },
            {
                "title": "Dalil Al-Qur'an dan Jaminan Keasliannya",
                "badge": "DALIL NAQLI",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">Allah Swt. sendiri yang menjamin pemeliharaan dan keaslian Al-Qur'an hingga hari kiamat (QS. Al-Hijr [15]: 9):</p>
                <div class="arabic-box">
                  <div class="arabic-text">إِنَّا نَحْنُ نَزَّلْنَا ٱلذِّكْرَ وَإِنَّا لَهُۥ لَحَٰفِظُونَ</div>
                  <div class="arabic-trans">"Sesungguhnya Kamilah yang menurunkan Al-Qur'an, dan sesungguhnya Kami benar-benar memeliharanya." (QS. Al-Hijr: 9)</div>
                </div>
                <div class="arabic-box" style="margin-top: 14px;">
                  <div class="arabic-text">قُل لَّئِنِ ٱجْتَمَعَتِ ٱلْإِنسُ وَٱلْجِنُّ عَلَىٰٓ أَن يَأْتُوا۟ بِمِثْلِ هَٰذَا ٱلْقُرْءَانِ لَا يَأْتُونَ بِمِثْلِهِۦ وَلَوْ كَانَ بَعْضُهُمْ لِبَعْضٍ ظَهِيرًا</div>
                  <div class="arabic-trans">"Katakanlah: 'Sesungguhnya jika manusia dan jin berkumpul untuk membuat yang serupa Al-Qur'an ini, niscaya mereka tidak akan dapat membuat yang serupa dengannya, sekalipun sebagian mereka menjadi pembantu bagi sebagian yang lain'." (QS. Al-Isra': 88)</div>
                </div>
                """
            },
            {
                "title": "Isi Pokok Kandungan Al-Qur'an",
                "badge": "SUBSTANSI WAHYU",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 16px;">Al-Qur'an mencakup seluruh pokok pedoman kehidupan manusia yang dirangkum ke dalam 6 dimensi utama:</p>
                <div class="content-grid-3">
                  <div class="card-box">
                    <div class="card-title">1. Akidah (Tauhid)</div>
                    <div class="card-desc">Keyakinan mutlak kepada Allah, Malaikat, Kitab-Kitab, Rasul, Hari Akhir, dan Qadha-Qadar.</div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">2. Ibadah & Syariah</div>
                    <div class="card-desc">Tata cara penghambaan vertikal (mahdhah) seperti shalat, zakat, puasa, dan haji.</div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">3. Akhlak (Moral)</div>
                    <div class="card-desc">Panduan budi pekerti luhur kepada Allah, sesama manusia, dan alam semesta.</div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">4. Muamalah</div>
                    <div class="card-desc">Hukum hubungan sosial sesama manusia, perniagaan, keadilan ekonomi, dan hukum waris.</div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">5. Kisah Umat Terdahulu</div>
                    <div class="card-desc">Ibrah (pelajaran) sejarah keteladanan para nabi dan kehancuran bangsa pembangkang.</div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">6. Sains & Isyarat Ilmiah</div>
                    <div class="card-desc">Isyarat tentang penciptaan alam semesta, embriologi manusia, tata surya, dan siklus air.</div>
                  </div>
                </div>
                """
            },
            {
                "title": "Nama-Nama Lain Al-Qur'an dan Fungsinya",
                "badge": "KHAZANAH NAMA",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th style="width: 25%;">Nama Lain</th>
                      <th style="width: 30%;">Arti & Makna</th>
                      <th>Dasar Dalil & Fungsi Utama</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Al-Kitab</strong> (ٱلْكِتَاب)</td>
                      <td>Sesuatu yang dituliskan</td>
                      <td><em>"Dzalikal kitabu la raiba fiih..."</em> (QS. Al-Baqarah: 2). Terbukukan rapi dalam mushaf terpelihara.</td>
                    </tr>
                    <tr>
                      <td><strong>Al-Furqan</strong> (ٱلْفُرْقَان)</td>
                      <td>Pembeda hak & batil</td>
                      <td><em>"Tabarakalladzi nazzalal furqana..."</em> (QS. Al-Furqan: 1). Menjadi barometer kebenaran vs kesesatan.</td>
                    </tr>
                    <tr>
                      <td><strong>Adz-Dzikr</strong> (ٱلذِّكْر)</td>
                      <td>Pemberi peringatan</td>
                      <td><em>"Inna nahnu nazzalnadz-dzikra..."</em> (QS. Al-Hijr: 9). Menyadarkan nurani manusia dari kelalaian.</td>
                    </tr>
                    <tr>
                      <td><strong>Al-Huda</strong> (ٱلْهُدَى)</td>
                      <td>Petunjuk hidup</td>
                      <td><em>"Hudan lin-naasi wa bayyinatin minal huda..."</em> (QS. Al-Baqarah: 185). Kompas keselamatan dunia dan akhirat.</td>
                    </tr>
                    <tr>
                      <td><strong>Asy-Syifa'</strong> (ٱلشِّفَاء)</td>
                      <td>Penyembuh/Penawar</td>
                      <td><em>"Wa nunazzilu minal qur'ani ma huwa syifa'un..."</em> (QS. Al-Isra': 82). Obat penenteram hati dan jiwa manusia.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            {
                "title": "Keistimewaan Al-Qur'an Dibanding Kitab Samawi Lainnya",
                "badge": "KEISTIMEWAAN MUKJIZAT",
                "content": """
                <ul class="bullet-list">
                  <li class="bullet-item">
                    <span class="bullet-icon">✦</span>
                    <div><strong>Keaslian yang Terjamin Langsung oleh Allah:</strong> Kitab terdahulu dipercayakan penjagaannya kepada umatnya sehingga rentan tahrif (perubahan), sedangkan Al-Qur'an dijaga oleh qudrat Allah hingga akhir zaman.</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">✦</span>
                    <div><strong>Berlaku Universal untuk Seluruh Umat dan Sepanjang Zaman:</strong> Taurat dan Injil diutus khusus bagi Bani Israil pada kurun waktu tertentu, sedangkan Al-Qur'an bersifat lintas masa dan bangsa (rahmatan lil 'alamin).</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">✦</span>
                    <div><strong>Mudah Dihafal dan Menggetarkan Jiwa:</strong> Satu-satunya kitab suci tebal di dunia yang dihafal jutaan orang dari berbagai ras, usia anak-anak hingga lansia dengan pelafalan harakat yang presisi (QS. Al-Qamar: 17).</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">✦</span>
                    <div><strong>Menyempurnakan dan Mengoreksi Kitab Terdahulu (*Muhaiminan*):</strong> Menghapus hukum kitab sebelumnya yang sifatnya lokal temporer serta mengukuhkan tauhid murni yang pernah diajarkan semua rasul.</div>
                  </li>
                </ul>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab I",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    1. Mengapa Al-Qur'an dijuluki sebagai "Al-Furqan" dalam Surah Al-Furqan ayat 1?
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Karena diturunkan pada malam Lailatul Qadar</div>
                    <div class="quiz-opt" data-correct="true">B. Karena berfungsi sebagai pembeda antara yang hak (kebenaran) dan yang batil (kesesatan)</div>
                    <div class="quiz-opt" data-correct="false">C. Karena dibaca secara berangsur-angsur selama 23 tahun</div>
                    <div class="quiz-opt" data-correct="false">D. Karena memuat kisah-kisah peradaban umat terdahulu</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). <em>Al-Furqan</em> berakar dari kata <em>faraqa</em> (memisahkan/membedakan), merujuk pada fungsi Al-Qur'an sebagai pembeda mutlak antara jalan tauhid dan syirik, keadilan dan kezaliman.
                  </div>
                </div>
                """
            },
            {
                "title": "Rangkuman & Refleksi Berinteraksi dengan Al-Qur'an",
                "badge": "IKHTISAR BAB I",
                "content": """
                <div class="content-grid-2" style="margin-top: 10px;">
                  <div class="card-box card-box-accent">
                    <div class="card-title">📌 Ikhtisar Pokok Pembelajaran</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Al-Qur'an adalah mukjizat abadi Nabi Muhammad Saw. yang mutawatir dan terjaga orisinalitasnya.</li>
                      <li>Berfungsi sebagai pedoman universal (hudan), penyembuh jiwa (syifa'), dan pembeda hak-batil (furqan).</li>
                      <li>Memuat 6 pilar utama: Akidah, Ibadah, Akhlak, Muamalah, Kisah Tauladan, dan Sains Ilmiah.</li>
                    </ul>
                  </div>
                  <div class="card-box">
                    <div class="card-title">🌟 Komitmen Amaliah Remaja MTs</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Membaca Al-Qur'an secara rutin (tilawah) minimal 1 ruku'/halaman setiap hari ba'da Maghrib/Subuh.</li>
                      <li>Mempelajari tajwid, makharijul huruf, dan berusaha memahami terjemahan maknanya.</li>
                      <li>Menjadikan Al-Qur'an sebagai penuntun akhlak mulia dalam tutur kata dan tindak-tanduk pergaulan.</li>
                    </ul>
                  </div>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-2-mukjizat-dan-kejadian-luar-biasa.html",
        "full_title": "BAB II: Mukjizat dan Kejadian Luar Biasa Lainnya — Akidah Akhlak Kelas VIII MTs",
        "chapter_label": "BAB II: Mukjizat & Kejadian Luar Biasa",
        "badge_text": "K8 • SEMESTER 1",
        "theme_color": "#10b981",
        "theme_light": "#6ee7b7",
        "theme_subtle": "rgba(16, 185, 129, 0.16)",
        "badge_gradient": "#059669, #10b981",
        "radial_color": "#064e3b",
        "slides": [
            {
                "title": "Mukjizat dan Kejadian Luar Biasa Lainnya",
                "badge": "PENGANTAR BAB II",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">⚡🛡️</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #34d399; margin: 12px 0;">BAB II: MUKJIZAT & KEJADIAN LUAR BIASA LAINNYA</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Mengenal tanda-tanda kebesaran dan kekuasaan mutlak Allah Swt. yang melampaui hukum sebab-akibat fisika alam semesta.
                  </p>
                  <div class="content-grid-4" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">✨ Mukjizat</div>
                      <div class="card-desc" style="font-size: 19pt;">Bukti kenabian bagi para Rasul untuk melemahkan musuh.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">💎 Karamah</div>
                      <div class="card-desc" style="font-size: 19pt;">Kemuliaan luar biasa yang dianugerahkan kepada wali Allah.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">🤝 Ma'unah</div>
                      <div class="card-desc" style="font-size: 19pt;">Pertolongan Allah bagi orang mukmin biasa saat kesulitan.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">🌟 Irhash</div>
                      <div class="card-desc" style="font-size: 19pt;">Pertanda keistimewaan calon nabi sebelum masa kerasulan.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Pengertian & Syarat-Syarat Mukjizat",
                "badge": "HAKIKAT MUKJIZAT",
                "content": """
                <p style="font-size: 22pt; line-height: 1.6; margin-bottom: 16px;">
                  Secara bahasa, <strong>Mukjizat</strong> berasal dari kata <em>a'jaza - yu'jizu</em> (أَعْجَزَ - يُعْجِزُ) yang artinya melemahkan atau menjadikan tidak mampu. Menurut istilah syariat, mukjizat adalah kejadian luar biasa (*amrun khariqun lil 'adah*) yang terjadi pada diri seorang Nabi atau Rasul Allah untuk membuktikan kebenaran risalahnya di hadapan penentangnya.
                </p>
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">4 Syarat Sah Suatu Mukjizat:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Merupakan hal luar biasa yang menyalahi adat kebiasaan alamiah.</li>
                      <li>Hanya terjadi pada seorang Nabi atau Rasul Allah yang resmi diutus.</li>
                      <li>Terjadi beriringan dengan tantangan (*tahaddi*) dari kaum penentang.</li>
                      <li>Tidak ada seorang manusia pun yang mampu menandingi atau menirunya.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Tujuan Utama Mukjizat:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Membungkam keraguan kaum kafir terhadap wahyu samawi.</li>
                      <li>Memperkokoh keimanan para sahabat dan pengikut setia rasul.</li>
                      <li>Menunjukkan bahwa kekuasaan Allah Swt. berdiri di atas seluruh hukum alam ciptaan-Nya.</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Pembagian Mukjizat: Hissiyah & Maknawiyah",
                "badge": "KLASIFIKASI",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">1. Mukjizat Hissiyah (Kauniyah)</div>
                    <div class="card-desc" style="font-size: 21pt;">
                      Mukjizat fisik yang dapat diindera langsung (dilihat, didengar, atau disentuh oleh mata kepala manusia) pada masa itu, namun bersifat material dan temporer.
                    </div>
                    <ul class="bullet-list" style="margin-top: 10px; font-size: 20pt;">
                      <li>Tongkat Nabi Musa as. membelah Laut Merah dan menjadi ular besar.</li>
                      <li>Nabi Isa as. menghidupkan orang mati dan menyembuhkan penyakit kusta atas izin Allah.</li>
                      <li>Keluarnya air memancar dari sela-sela jemari Rasulullah Saw.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">2. Mukjizat Maknawiyah (Aqliyah)</div>
                    <div class="card-desc" style="font-size: 21pt;">
                      Mukjizat non-fisik yang hanya dapat dipahami dan dihayati melalui akal pikiran, kecerdasan nurani, dan perenungan mendalam, serta bersifat abadi sepanjang zaman.
                    </div>
                    <ul class="bullet-list" style="margin-top: 10px; font-size: 20pt;">
                      <li><strong>Al-Qur'an Al-Karim:</strong> Mukjizat terbesar Nabi Muhammad Saw. Keagungan sastranya, nubuat masa depannya, dan keselarasan ilmiahnya tetap eksis hingga kiamat.</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Karamah, Ma'unah, dan Irhash",
                "badge": "KEJADIAN LUAR BIASA",
                "content": """
                <div class="content-grid-3">
                  <div class="card-box">
                    <div class="card-title">💎 Karamah</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Kejadian luar biasa dari Allah yang diberikan kepada <em>waliyullah</em> (hamba saleh yang bertakwa dan istiqamah tanpa menuntut pengakuan kenabian).
                    </div>
                    <div style="font-size: 19pt; color: #cbd5e1; margin-top: 8px;">
                      <strong>Contoh:</strong> Kisah pemuda Ashabul Kahfi yang tertidur 309 tahun di gua (QS. Al-Kahfi) dan Maryam binti Imran yang memperoleh buah-buahan surga di mihrabnya (QS. Ali 'Imran: 37).
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">🤝 Ma'unah</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Pertolongan ajaib dari Allah yang datang kepada orang mukmin biasa saat menghadapi marabahaya yang sangat genting dan di luar nalar.
                    </div>
                    <div style="font-size: 19pt; color: #cbd5e1; margin-top: 8px;">
                      <strong>Contoh:</strong> Seorang mukmin yang selamat tanpa luka sedikit pun saat gedung runtuh akibat gempa bumi dahsyat, atau korban selamat kecelakaan maut secara ajaib.
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">🌟 Irhash</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Tanda atau peristiwa luar biasa yang dialami oleh calon Nabi/Rasul pada masa sebelum diangkat resmi menjadi rasul (*qablal bi'tsah*).
                    </div>
                    <div style="font-size: 19pt; color: #cbd5e1; margin-top: 8px;">
                      <strong>Contoh:</strong> Awan yang memayungi perjalanan dagang Nabi Muhammad Saw. ke Syam saat bersama pamannya Abu Thalib, serta terbelahnya dada beliau saat diasuh Halimah As-Sa'diyah.
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Tabel Komparasi Perbedaan Kejadian Luar Biasa",
                "badge": "MATRIKS KOMPARATIF",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th>Jenis Fenomena</th>
                      <th>Penerima / Pelaku</th>
                      <th>Waktu Kejadian</th>
                      <th>Tujuan & Sifat Kejadian</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong style="color: #6ee7b7;">Mukjizat</strong></td>
                      <td>Nabi & Rasul Allah</td>
                      <td>Setelah diangkat kerasulan</td>
                      <td>Membuktikan risalah, melemahkan musuh kafir (*tahaddi*).</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #6ee7b7;">Karamah</strong></td>
                      <td>Wali Allah (hamba bertakwa)</td>
                      <td>Sepanjang masa ketakwaannya</td>
                      <td>Memuliakan wali dan menguatkan istiqamah ibadah.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #6ee7b7;">Ma'unah</strong></td>
                      <td>Orang mukmin biasa</td>
                      <td>Saat musibah/kritis mendesak</td>
                      <td>Menyelamatkan hamba beriman dari bahaya maut.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #6ee7b7;">Irhash</strong></td>
                      <td>Calon Nabi / Rasul</td>
                      <td>Sebelum masa kenabian</td>
                      <td>Menjadi tanda persiapan ilahiah calon pembawa wahyu.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #f87171;">Sihir / Istidraj</strong></td>
                      <td>Orang kafir / fasik / durhaka</td>
                      <td>Kapan saja tipu daya setan</td>
                      <td>Kesesatan, menjerumuskan manusia, bantuan jin jahat.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            {
                "title": "Membedakan Karunia Ilahi vs Sihir / Istidraj",
                "badge": "BENTENG AKIDAH",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box card-box-accent">
                    <div class="card-title">Ciri Karunia Allah (Mukjizat, Karamah, Ma'unah):</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Datang semata-mata atas izin Allah tanpa mantra atau ritual kesyirikan.</li>
                      <li>Penerimanya adalah pribadi yang semakin taat, rendah hati (*tawadhu'*), dan menjauhi maksiat.</li>
                      <li>Membimbing manusia kepada tauhid, amal saleh, dan perbaikan akhlak.</li>
                    </ul>
                  </div>
                  <div class="card-box" style="border-color: rgba(239, 68, 68, 0.4);">
                    <div class="card-title" style="color: #fca5a5;">Ciri Tipu Daya (Sihir & Istidraj):</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Sihir dipelajari melalui persekutuan dengan bangsa jin kafir dan sesajen haram.</li>
                      <li>Istidraj: kelapangan materi/kekuatan semu bagi pendosa agar makin tenggelam dalam laknat Allah.</li>
                      <li>Menimbulkan kesombongan, riya', ketakutan, dan perpecahan di masyarakat.</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab II",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    Peristiwa awan yang senantiasa menaungi perjalanan Nabi Muhammad Saw. sewaktu masih remaja berdagang ke negeri Syam bersama Abu Thalib diklasifikasikan sebagai...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Mukjizat Kauniyah karena disaksikan oleh pendeta Buhaira</div>
                    <div class="quiz-opt" data-correct="false">B. Karamah karena terjadi pada orang saleh keturunan Quraisy</div>
                    <div class="quiz-opt" data-correct="true">C. Irhash karena terjadi pada calon rasul sebelum resmi diutus Allah</div>
                    <div class="quiz-opt" data-correct="false">D. Ma'unah karena menyelamatkan dari terik panas padang pasir</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (C). <em>Irhash</em> adalah kejadian luar biasa yang menyertai calon nabi sebelum masa kenabian (sebelum menerima wahyu pertama di Gua Hira).
                  </div>
                </div>
                """
            },
            {
                "title": "Hikmah Mempercayai Mukjizat & Kejadian Luar Biasa",
                "badge": "REFLEKSI AKIDAH",
                "content": """
                <div class="card-box card-box-accent" style="margin-bottom: 20px;">
                  <div class="card-title">🌟 Hikmah dalam Kehidupan Seorang Mukmin:</div>
                  <ul class="bullet-list" style="font-size: 21pt;">
                    <li><strong>Mempertebal Tauhid:</strong> Meyakini tiada daya dan kekuatan melainkan milik Allah Swt. (*La hawla wa la quwwata illa billah*).</li>
                    <li><strong>Membenarkan Kerasulan:</strong> Yakin sepenuhnya bahwa ajaran para Rasul adalah haq dan wahyu murni dari langit.</li>
                    <li><strong>Optimisme dalam Berikhtiar:</strong> Selalu berprasangka baik bahwa Allah senantiasa mendengar doa dan mampu menurunkan pertolongan-Nya (*ma'unah*) di saat yang tak terduga.</li>
                    <li><strong>Terhindar dari Kesyirikan:</strong> Tidak mudah tertipu oleh atraksi dukun, paranormal, atau sulap sihir berkedok karamah.</li>
                  </ul>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-3-akhlak-terpuji-ikhtiar-tawakkal-sabar-syukur-qanaah.html",
        "full_title": "BAB III: Akhlak Terpuji (Ikhtiar, Tawakkal, Sabar, Syukur, Qana'ah) — Akidah Akhlak K8",
        "chapter_label": "BAB III: Ikhtiar, Tawakkal, Sabar, Syukur, Qana'ah",
        "badge_text": "K8 • SEMESTER 1",
        "theme_color": "#f59e0b",
        "theme_light": "#fcd34d",
        "theme_subtle": "rgba(245, 158, 11, 0.16)",
        "badge_gradient": "#d97706, #f59e0b",
        "radial_color": "#78350f",
        "slides": [
            {
                "title": "Membiasakan Akhlak Terpuji: 5 Pilar Kehidupan",
                "badge": "PENGANTAR BAB III",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">💎🤲</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #fcd34d; margin: 12px 0;">BAB III: MEMBIASAKAN AKHLAK TERPUJI</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Lima pondasi mental spiritual mukmin sejati: <strong>Ikhtiar, Tawakkal, Sabar, Syukur,</strong> dan <strong>Qana'ah</strong> dalam menghadapi dinamika takdir kehidupan.
                  </p>
                  <div class="content-grid-3" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">1. Ikhtiar & Tawakkal</div>
                      <div class="card-desc">Kerja keras maksimal mengerahkan seluruh potensi akal dan raga, disempurnakan dengan penyerahan diri bulat kepada Allah.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">2. Sabar & Syukur</div>
                      <div class="card-desc">Dua sayap burung keimanan: tabah menghadapi ujian duka dan mensyukuri nikmat suka dengan ketaatan.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">3. Qana'ah</div>
                      <div class="card-desc">Merasa cukup dan rela menerima ketetapan rezeki dari Allah, membebaskan jiwa dari ketamakan duniawi.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Ikhtiar: Hakikat Berusaha Sungguh-Sungguh",
                "badge": "PILAR 1: IKHTIAR",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Ikhtiar</strong> adalah usaha sungguh-sungguh seorang hamba dalam mengerahkan segenap tenaga, pikiran, dan keterampilan demi menggapai cita-cita yang diridhai Allah Swt.
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">إِنَّ ٱللَّهَ لَا يُغَيِّرُ مَا بِقَوْمٍ حَتَّىٰ يُغَيِّرُوا۟ مَا بِأَنفُسِهِمْ</div>
                  <div class="arabic-trans">"Sesungguhnya Allah tidak akan mengubah keadaan suatu kaum sebelum mereka mengubah keadaan diri mereka sendiri." (QS. Ar-Ra'd: 11)</div>
                </div>
                <div class="content-grid-2" style="margin-top: 14px;">
                  <div class="card-box">
                    <div class="card-title">Ciri Mukmin Berikhtiar:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Memiliki rencana matang, disiplin, dan etos kerja tinggi.</li>
                      <li>Tidak pasrah buta pada nasib tanpa aksi nyata.</li>
                      <li>Memilih cara-cara halal dan menjauhi jalan pintas yang curang.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Dampak Positif:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Menumbuhkan kemandirian dan rasa percaya diri yang kokoh.</li>
                      <li>Terhindar dari sikap malas, meminta-minta, dan kehinaan diri.</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Tawakkal: Menyandarkan Hasil Hanya kepada Allah",
                "badge": "PILAR 2: TAWAKKAL",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Tawakkal</strong> adalah menyandarkan seluruh urusan dan hasil ikhtiar kepada Allah Swt. disertai keyakinan bahwa apa pun ketetapan-Nya adalah yang terbaik bagi hamba-Nya.
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">فَإِذَا عَزَمْتَ فَتَوَكَّلْ عَلَى ٱللَّهِ ۚ إِنَّ ٱللَّهَ يُحِبُّ ٱلْمُتَوَكِّلِينَ</div>
                  <div class="arabic-trans">"Kemudian, apabila engkau telah membulatkan tekad, maka bertawakallah kepada Allah. Sesungguhnya Allah mencintai orang-orang yang bertawakal." (QS. Ali 'Imran: 159)</div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Prinsip Tawakkal yang Benar (Bukan Fatalisme):</div>
                  <div class="card-desc" style="font-size: 21pt;">
                    Rasulullah Saw. menegur seorang Arab badui yang melepas untanya tanpa diikat dengan sabda: <em>"I'qilha wa tawakkal"</em> (Ikatlah untamu terlebih dahulu, baru kemudian bertawakallah kepada Allah!). Tawakkal hadir setelah ikhtiar optimal dilakukan, bukan sebagai alasan untuk bermalas-malasan.
                  </div>
                </div>
                """
            },
            {
                "title": "Sabar: Keteguhan Hati Menghadapi Ujian",
                "badge": "PILAR 3: SABAR",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Sabar</strong> adalah menahan diri dari keluh kesah, kemarahan, dan keputusasaan ketika diuji, serta menahan hawa nafsu dari maksiat.
                </p>
                <div class="content-grid-3">
                  <div class="card-box card-box-accent">
                    <div class="card-title">1. Sabar dalam Taat</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Istiqamah mendirikan shalat subuh tepat waktu, berpuasa di cuaca terik, dan konsisten menuntut ilmu meskipun lelah.
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">2. Sabar dari Maksiat</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Menjaga pandangan, menolak ajakan miras, judi online, pornografi, dan tawuran remaja meskipun tren sebaya menuntutnya.
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">3. Sabar atas Musibah</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Mengucapkan istirja' (<em>Inna lillahi wa inna ilaihi raji'un</em>) saat tertimpa sakit, kehilangan harta benda, atau duka kematian keluarga.
                    </div>
                  </div>
                </div>
                <div class="arabic-box" style="margin-top: 14px;">
                  <div class="arabic-text">إِنَّمَا يُوَفَّى ٱلصَّٰبِرُونَ أَجْرَهُم بِغَيْرِ حِسَابٍ</div>
                  <div class="arabic-trans">"Sesungguhnya hanya orang-orang yang bersabarlah yang disempurnakan pahalanya tanpa batas." (QS. Az-Zumar: 10)</div>
                </div>
                """
            },
            {
                "title": "Syukur dan Qana'ah: Kunci Kebahagiaan Jiwa",
                "badge": "PILAR 4 & 5",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">🌟 Syukur (Pemberian Pengakuan)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Mengakui bahwa seluruh karunia berasal dari Allah dan menggunakannya untuk beribadah kepada-Nya.
                    </div>
                    <ul class="bullet-list" style="font-size: 19pt; margin-top: 8px;">
                      <li><strong>Syukur Hati:</strong> Meyakini nikmat dari Allah.</li>
                      <li><strong>Syukur Lisan:</strong> Memperbanyak tahmid (Alhamdulillah).</li>
                      <li><strong>Syukur Anggota Tubuh:</strong> Memanfaatkan kesehatan, ilmu, dan harta demi kebajikan umat.</li>
                    </ul>
                    <div style="font-size: 19pt; color: #fcd34d; margin-top: 10px;">
                      <em>"La-in syakartum la-aziidannakum..."</em> (QS. Ibrahim: 7).
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">🌾 Qana'ah (Merasa Cukup)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Sikap rela menerima apa yang ada (*ridha bi qadha'illah*), tidak iri melihat nikmat orang lain, dan hidup bersahaja.
                    </div>
                    <ul class="bullet-list" style="font-size: 19pt; margin-top: 8px;">
                      <li>Menjauhkan diri dari sifat tamak dan serakah.</li>
                      <li>Hidup tenang tanpa beban gengsi sosial.</li>
                      <li>Selalu melihat ke bawah dalam urusan harta dunia, dan melihat ke atas dalam urusan amal akhirat.</li>
                    </ul>
                    <div style="font-size: 19pt; color: #fcd34d; margin-top: 10px;">
                      Rasulullah Saw.: <em>"Kekayaan sejati bukanlah banyaknya harta, melainkan kekayaan jiwa (hati)."</em> (HR. Al-Bukhari).
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Harmoni Hubungan 5 Pilar Karakter Mukmin",
                "badge": "INTEGRASI SIKAP",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th>Situasi Hidup</th>
                      <th>Respon Akhlak Terpuji</th>
                      <th>Buah / Dampak Kejiwaan</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Sedang menghadapi tugas belajar / cita-cita</td>
                      <td><strong>Ikhtiar Maksimal + Doa</strong></td>
                      <td>Etos belajar gigih, terencana, dan tidak malas.</td>
                    </tr>
                    <tr>
                      <td>Menanti hasil pengumuman ujian / perlombaan</td>
                      <td><strong>Tawakkal Mutlak</strong></td>
                      <td>Bebas dari kecemasan berlebih, damai lahir batin.</td>
                    </tr>
                    <tr>
                      <td>Mendapat hasil nilai tinggi / juara lomba</td>
                      <td><strong>Syukur Nikmat</strong></td>
                      <td>Tidak sombong (ujub), makin rendah hati dan dermawan.</td>
                    </tr>
                    <tr>
                      <td>Menghadapi kegagalan / musibah duka</td>
                      <td><strong>Sabar & Tabah</strong></td>
                      <td>Tidak menyalahkan takdir, lekas bangkit mengevaluasi diri.</td>
                    </tr>
                    <tr>
                      <td>Melihat kemewahan fasilitas teman lain</td>
                      <td><strong>Qana'ah di Hati</strong></td>
                      <td>Bersyukur atas rezeki keluarga, terhindar dari hasad & gengsi.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab III",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    Ahmad belajar tekun siang dan malam untuk menghadapi ujian madrasah. Menjelang ujian, ia berdoa memohon kelulusan dan menyerahkan hasilnya kepada kehendak Allah. Sikap penyerahan hasil kepada Allah yang dilakukan Ahmad dinamakan...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Qana'ah karena merasa cukup dengan ilmunya</div>
                    <div class="quiz-opt" data-correct="false">B. Ikhtiar karena telah belajar tanpa henti</div>
                    <div class="quiz-opt" data-correct="true">C. Tawakkal karena menyandarkan hasil kepada Allah setelah berikhtiar</div>
                    <div class="quiz-opt" data-correct="false">D. Sabar karena tabah menghadapi soal-soal sulit</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (C). Ikhtiar adalah proses belajarnya, sedangkan menyandarkan keputusan hasil akhir kepada kekuasaan dan takdir Allah Swt. disebut <em>Tawakkal</em>.
                  </div>
                </div>
                """
            },
            {
                "title": "Rangkuman Refleksi Hati Nurani",
                "badge": "IKHTISAR BAB III",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">💡 Renungan Keimanan:</div>
                  <p style="font-size: 22pt; line-height: 1.6; color: #f1f5f9;">
                    "Sungguh mengagumkan perkara orang mukmin, semua urusannya adalah kebaikan baginya. Jika mendapatkan kelapangan nikmat, ia <strong>bersyukur</strong> maka itu baik baginya; dan jika ditimpa musibah kesempitan, ia <strong>bersabar</strong> maka itu pun mendatangkan pahala kebaikan baginya." (HR. Muslim).
                  </p>
                  <div style="margin-top: 20px; font-size: 21pt; color: #fcd34d;">
                    Jadikan Ikhtiar sebagai tanganmu, Tawakkal sebagai bentengmu, Sabar dan Syukur sebagai sayapmu, serta Qana'ah sebagai mahkota ketenteraman jiwamu!
                  </div>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-4-akhlak-tercela-ananiyah-putus-asa-ghadhab-tamak.html",
        "full_title": "BAB IV: Menghindari Akhlak Tercela (Ananiyah, Putus Asa, Ghadhab, Tamak) — Akidah Akhlak K8",
        "chapter_label": "BAB IV: Ananiyah, Putus Asa, Ghadhab, Tamak",
        "badge_text": "K8 • SEMESTER 1",
        "theme_color": "#f43f5e",
        "theme_light": "#fda4af",
        "theme_subtle": "rgba(244, 63, 94, 0.16)",
        "badge_gradient": "#e11d48, #f43f5e",
        "radial_color": "#881337",
        "slides": [
            {
                "title": "Menghindari Akhlak Tercela: Penyakit Hati",
                "badge": "PENGANTAR BAB IV",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">⚠️🔥</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #fb7185; margin: 12px 0;">BAB IV: MENGHINDARI AKHLAK TERCELA</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Mendeteksi dan membersihkan hati dari racun moral: <strong>Ananiyah (Egois), Putus Asa (Al-Ya'su), Ghadhab (Pemarah),</strong> dan <strong>Tamak (Serakah)</strong>.
                  </p>
                  <div class="content-grid-4" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">1. Ananiyah</div>
                      <div class="card-desc" style="font-size: 19pt;">Egoisme akut, mementingkan diri sendiri dan mengabaikan hak sesama.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">2. Putus Asa</div>
                      <div class="card-desc" style="font-size: 19pt;">Hilang harapan dari rahmat Allah ketika menghadapi kegagalan.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">3. Ghadhab</div>
                      <div class="card-desc" style="font-size: 19pt;">Emosi meledak-ledak yang merusak akal sehat dan silaturahmi.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">4. Tamak</div>
                      <div class="card-desc" style="font-size: 19pt;">Kerakusan duniawi tanpa batas, tidak pernah merasa puas.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Ananiyah (Egois): Gejala & Bahayanya",
                "badge": "PENYAKIT 1: ANANIYAH",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Ananiyah</strong> berasal dari kata <em>Ana</em> (أَنَا - saya/aku). Ananiyah adalah sikap mementingkan diri sendiri, merasa diri paling benar dan paling berhak, tanpa mempedulikan nasib, hak, maupun perasaan orang lain.
                </p>
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Ciri-Ciri Orang Bersikap Ananiyah:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Hanya memikirkan keuntungan pribadi dalam pertemanan.</li>
                      <li>Enggan mengalah dan tidak mau menerima masukan atau kritik orang lain.</li>
                      <li>Kikir dan tidak memiliki empati terhadap kesulitan sesama.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Dampak Negatif & Bahaya:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Dijauhi dan dibenci dalam pergaulan lingkungan sosial.</li>
                      <li>Menumbuhkan kesombongan dan merusak tali persaudaraan (ukhuwah).</li>
                      <li>Rasulullah Saw.: <em>"Tidak beriman salah seorang di antara kalian hingga ia mencintai saudaranya seperti mencintai dirinya sendiri."</em> (HR. Al-Bukhari).</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Putus Asa (Al-Ya'su): Menutup Pintu Rahmat",
                "badge": "PENYAKIT 2: PUTUS ASA",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Putus Asa</strong> adalah sikap merasa bahwa segala harapan telah punah dan menganggap Allah tidak lagi menolongnya saat tertimpa ujian atau kegagalan berulang.
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">وَلَا تَا۟يْـَٔسُوا۟ مِن رَّوْحِ ٱللَّهِ ۖ إِنَّهُۥ لَا يَا۟يْـَٔسُ مِن رَّوْحِ ٱللَّهِ إِلَّا ٱلْقَوْمُ ٱلْكَٰفِرُونَ</div>
                  <div class="arabic-trans">"...dan janganlah kamu berputus asa dari rahmat Allah. Sesungguhnya tiada yang berputus asa dari rahmat Allah melainkan kaum yang kafir." (QS. Yusuf: 87)</div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Cara Mengobati Keputusasaan:</div>
                  <ul class="bullet-list" style="font-size: 20pt;">
                    <li>Meyakini bahwa di balik setiap kesulitan pasti terdapat kemudahan berlipat (QS. Al-Insyirah: 5-6).</li>
                    <li>Menjadikan kegagalan sebagai bahan evaluasi dan sarana mematangkan kualitas diri.</li>
                    <li>Memperbanyak istighfar dan bergaul dengan sahabat-sahabat yang positif serta saleh.</li>
                  </ul>
                </div>
                """
            },
            {
                "title": "Ghadhab (Pemarah): Api Gejolak Iblis",
                "badge": "PENYAKIT 3: GHADHAB",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Ghadhab</strong> adalah luapan emosi amarah yang tak terkendali akibat gejolak darah yang dipicu oleh bisikan setan untuk merusak hubungan sesama hamba Allah.
                </p>
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Bahaya Ghadhab bagi Kehidupan:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Menyebabkan tindakan kekerasan fisik, tawuran, caci maki, dan penyesalan seumur hidup.</li>
                      <li>Memicu gangguan kesehatan (hipertensi, serangan jantung, dan stroke).</li>
                      <li>Mengikis pahala amal kebaikan yang telah dikumpulkan.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Petunjuk Nabi Meredam Marah:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Membaca ta'awudz (<em>A'udzu billahi minasy syaithanir rajim</em>).</li>
                      <li>Bila sedang berdiri, hendaknya duduk; bila belum reda, hendaknya berbaring.</li>
                      <li>Bersegera mengambil air wudhu (karena air memadamkan api marah).</li>
                      <li>Nabi Saw.: <em>"Orang kuat bukanlah yang menang gulat, melainkan yang mampu menguasai dirinya saat marah."</em> (HR. Al-Bukhari).</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Tamak: Kerakusan yang Menghancurkan Nurani",
                "badge": "PENYAKIT 4: TAMAK",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Tamak</strong> (rakus/loba) adalah cinta duniawi berlebihan (*hubbud dunya*) yang mendorong seseorang menghalalkan segala cara demi menumpuk kekayaan atau jabatan tanpa rasa syukur.
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">أَلْهَىٰكُمُ ٱلتَّكَاثُرُ ﴿١﴾ حَتَّىٰ زُرْتُمُ ٱلْمَقَابِرَ ﴿٢﴾</div>
                  <div class="arabic-trans">"Bermegah-megahan telah melalaikan kamu, sampai kamu masuk ke dalam kubur." (QS. At-Takatsur: 1-2)</div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Penawar Sifat Tamak:</div>
                  <div class="card-desc" style="font-size: 21pt;">
                    Menumbuhkan sifat <strong>Qana'ah</strong> (merasa cukup), rajin berinfak dan sedekah, mengingat kematian yang memutuskan segala kenikmatan, serta menyadari bahwa kafan mayat tidak memiliki saku untuk membawa harta simpanan.
                  </div>
                </div>
                """
            },
            {
                "title": "Matriks Solusi Penawar Akhlak Tercela",
                "badge": "TABEL MUJAHADAH",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th>Penyakit Tercela</th>
                      <th>Akar Penyebab Utama</th>
                      <th>Penawar Terpuji Penyeimbangnya</th>
                      <th>Tindakan Nyata Keseharian</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong style="color: #fb7185;">Ananiyah</strong> (Egois)</td>
                      <td>Ujub & ketiadaan empati</td>
                      <td><strong>Itsar</strong> & <strong>Tawadhu'</strong></td>
                      <td>Mendengarkan pendapat orang lain, gemar menolong teman.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #fb7185;">Putus Asa</strong></td>
                      <td>Su'udzan kepada takdir Allah</td>
                      <td><strong>Raja'</strong> & <strong>Husnuzzan</strong></td>
                      <td>Segera bangkit evaluasi diri, meyakini hikmah di balik duka.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #fb7185;">Ghadhab</strong> (Marah)</td>
                      <td>Hawa nafsu & hasutan setan</td>
                      <td><strong>Hilim</strong> & <strong>Pemaaf</strong></td>
                      <td>Diam, berwudhu, menarik nafas panjang, dan memaafkan.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #fb7185;">Tamak</strong> (Serakah)</td>
                      <td>Hubbud dunya (cinta dunia)</td>
                      <td><strong>Qana'ah</strong> & <strong>Zuhud</strong></td>
                      <td>Bersyukur atas rezeki halal, aktif sedekah dan zakat.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab IV",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    Seorang siswa mengalami kegagalan seleksi beasiswa, kemudian ia mengurung diri di kamar, menolak makan, dan menuduh Allah tidak adil kepadanya. Perilaku siswa tersebut mencerminkan akhlak tercela...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Ananiyah karena mementingkan perasaan pribadinya</div>
                    <div class="quiz-opt" data-correct="true">B. Putus asa karena meragukan kasih sayang dan rahmat Allah Swt.</div>
                    <div class="quiz-opt" data-correct="false">C. Tamak karena menginginkan beasiswa yang menjadi hak orang lain</div>
                    <div class="quiz-opt" data-correct="false">D. Ghadhab karena memarahi pihak panitia penyelenggara beasiswa</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). Menganggap doa tidak berguna dan berprasangka buruk kepada Allah saat gagal adalah manifestasi dari keputusasaan (<em>Al-Ya'su</em>) yang dilarang keras dalam QS. Yusuf ayat 87.
                  </div>
                </div>
                """
            },
            {
                "title": "Refleksi Tazkiyatun Nafs: Bab IV",
                "badge": "IKHTISAR BAB IV",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">🛡️ Menjaga Kesucian Qalbu:</div>
                  <p style="font-size: 22pt; line-height: 1.6;">
                    Hati manusia ibarat cermin bening. Setiap dosa egois, marah, putus asa, dan tamak akan meninggalkan bintik hitam pekat di atasnya.
                  </p>
                  <ul class="bullet-list" style="margin-top: 14px; font-size: 20pt;">
                    <li>Gantilah <em>ananiyah</em> dengan kepedulian sosial yang tulus.</li>
                    <li>Usir kabut <em>putus asa</em> dengan keyakinan bahwa rahmat Allah meluas meliputi segala sesuatu.</li>
                    <li>Padamkan api <em>ghadhab</em> dengan kesejukan wudhu dan kelapangan hati memaafkan.</li>
                    <li>Kikis <em>tamak</em> dengan kekayaan jiwa qana'ah yang penuh syukur.</li>
                  </ul>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-5-adab-kepada-orang-tua-dan-guru.html",
        "full_title": "BAB V: Adab Seorang Muslim terhadap Orang Tua dan Guru — Akidah Akhlak K8",
        "chapter_label": "BAB V: Adab kepada Orang Tua & Guru",
        "badge_text": "K8 • SEMESTER 1",
        "theme_color": "#a855f7",
        "theme_light": "#d8b4fe",
        "theme_subtle": "rgba(168, 85, 247, 0.16)",
        "badge_gradient": "#9333ea, #a855f7",
        "radial_color": "#581c87",
        "slides": [
            {
                "title": "Adab Seorang Muslim kepada Orang Tua dan Guru",
                "badge": "PENGANTAR BAB V",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">👵👨‍🏫</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #c084fc; margin: 12px 0;">BAB V: ADAB KEPADA ORANG TUA & GURU</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Kunci utama terbukanya pintu ridha ilahi, barakah umur, dan kemudahan dalam menuntut ilmu dunia dan akhirat.
                  </p>
                  <div class="content-grid-2" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">🌸 Birrul Walidain (Berbakti Orang Tua)</div>
                      <div class="card-desc">Kedudukan istimewa orang tua dalam Al-Qur'an, adab berbakti saat hidup maupun setelah wafat, serta bahaya uququl walidain.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">📚 Ta'dzim lil Asatidz (Hormat Guru)</div>
                      <div class="card-desc">Guru sebagai orang tua rohani yang mendidik akal budi, adab mendengarkan pelajaran, dan etika menyapa penuh takzim.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Kedudukan Istimewa Berbakti kepada Orang Tua",
                "badge": "BIRRUL WALIDAIN",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Allah Swt. menggandengkan perintah beribadah kepada-Nya dengan perintah berbakti kepada kedua orang tua (QS. Al-Isra' [17]: 23):
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">۞ وَقَضَىٰ رَبُّكَ أَلَّا تَعْبُدُوٓا۟ إِلَّآ إِيَّاهُ وَبِٱلْوَٰلِدَيْنِ إِحْسَٰنًا ۚ إِمَّا يَبْلُغَنَّ عِندَكَ ٱلْكِبَرَ أَحَدُهُمَآ أَوْ كِلَاهُمَا فَلَا تَقُل لَّهُمَآ أُفٍّ وَلَا تَنْهَرْهُمَا وَقُل لَّهُمَا قَوْلًا كَرِيمًا</div>
                  <div class="arabic-trans">"Dan Tuhanmu telah memerintahkan agar kamu jangan menyembah selain Dia dan hendaklah berbuat baik kepada ibu bapak. Jika salah seorang di antara keduanya atau kedua-duanya sampai berusia lanjut dalam pemeliharaanmu, maka sekali-kali janganlah engkau mengatakan kepada keduanya perkataan 'ah' dan janganlah engkau membentak keduanya, dan ucapkanlah kepada keduanya perkataan yang mulia." (QS. Al-Isra': 23)</div>
                </div>
                """
            },
            {
                "title": "Bentuk Nyata Berbakti kepada Orang Tua",
                "badge": "AMALIAH NYATA",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Saat Orang Tua Masih Hidup:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Berbicara dengan tutur kata yang santun, lembut, dan tidak menyela perkataan mereka.</li>
                      <li>Mentaati perintah keduanya selama tidak dalam kemaksiatan kepada Allah.</li>
                      <li>Membantu pekerjaan rumah tangga dan merawat mereka dengan ikhlas saat sakit/uzur.</li>
                      <li>Meminta restu dan doa sebelum melangkah dalam urusan penting.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Setelah Orang Tua Wafat:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Mendoakan ampunan dan rahmat bagi mereka setiap selesai shalat fardhu.</li>
                      <li>Menunaikan wasiat, nadzar, atau hutang-piutang yang belum selesai.</li>
                      <li>Menyambung silaturahmi dengan kerabat dan sahabat-sahabat dekat kedua orang tua.</li>
                      <li>Bersedekah atas nama kedua orang tua (*amal jariyah*).</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Uququl Walidain: Bahaya Durhaka kepada Orang Tua",
                "badge": "PERINGATAN KERAS",
                "content": """
                <div class="card-box card-box-accent" style="margin-bottom: 20px;">
                  <div class="card-title">⚠️ Dosa Besar Paling Cepat Dibalas di Dunia:</div>
                  <p style="font-size: 22pt; line-height: 1.6;">
                    Durhaka kepada orang tua (<em>'Uququl Walidain</em>) adalah salah satu dosa besar yang ancamannya tidak ditunda hanya di akhirat, melainkan dipercepat balasannya sejak hidup di dunia.
                  </p>
                </div>
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Sabda Rasulullah Saw. (HR. Al-Hakim):</div>
                    <div class="card-desc" style="font-size: 21pt;">
                      <em>"Setiap dosa akan ditunda hukumannya oleh Allah sampai hari kiamat sesuai kehendak-Nya, kecuali dosa durhaka kepada kedua orang tua; sesungguhnya Allah mempercepat siksanya bagi pelakunya dalam kehidupan di dunia sebelum wafatnya."</em>
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">Puncak Ridha Ilahi:</div>
                    <div class="card-desc" style="font-size: 21pt;">
                      <em>"Ridhallahi fii ridhal walidain, wa sukhtullahi fii sukhtil walidain"</em> (Ridha Allah terletak pada ridha kedua orang tua, dan murka Allah terletak pada murka kedua orang tua). (HR. At-Tirmidzi).
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Adab Menghormati Guru (Pewaris Para Nabi)",
                "badge": "TA'DZIM GURU",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Guru adalah orang tua rohani kita yang membimbing akal dari kebodohan dan menyalakan lentera tauhid dalam dada. Ulama salaf mengatakan: <em>"Bila orang tua jasmani menghidupkan raga di dunia fana, maka guru menghidupkan jiwa untuk keselamatan akhirat baka."</em>
                </p>
                <div class="content-grid-3">
                  <div class="card-box">
                    <div class="card-title">1. Sikap Menuntut Ilmu</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Hadir tepat waktu di kelas, memperhatikan penjelasan guru dengan fokus, dan tidak bermain gadget saat pelajaran.
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">2. Bertanya Sopan</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Mengangkat tangan dengan sopan, memilih kata santun, dan tidak memotong penjelasan guru sebelum dipersilakan.
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">3. Bertegur Sapa</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Mengucapkan salam dan mencium tangan guru saat berpapasan di madrasah maupun di jalan raya dengan penuh rasa hormat.
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Kisah Teladan Imam Asy-Syafi'i Memuliakan Guru",
                "badge": "KETELADANAN SALAF",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">📖 Penghormatan Luar Biasa Ulama Terhadap Gurunya:</div>
                  <p style="font-size: 22pt; line-height: 1.6; margin-top: 10px;">
                    Imam Asy-Syafi'i rahimahullah meriwayatkan ketawadhu'annya di majelis gurunya, Imam Malik:
                  </p>
                  <blockquote style="font-size: 21pt; font-style: italic; color: #f3e8ff; margin: 14px 0; padding-left: 20px; border-left: 4px solid #c084fc; line-height: 1.6;">
                    "Aku membalik lembaran kertas kitabku dengan sangat perlahan dan sangat hati-hati di hadapan Imam Malik karena rasa hormatku kepadanya, agar beliau tidak terganggu oleh desiran bunyi kertas tersebut."
                  </blockquote>
                  <p style="font-size: 21pt; color: #cbd5e1; line-height: 1.5;">
                    Barakah ilmu seorang murid sangat ditentukan oleh sejauh mana keikhlasan doa dan keridhaan gurunya. Ilmu tanpa adab akan hilang keberkahannya.
                  </p>
                </div>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab V",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    Manakah di antara pernyataan berikut yang merupakan adab berbakti kepada orang tua yang telah meninggal dunia?
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Meminta doa restu kelulusan sekolah secara langsung di hadapan pusaranya</div>
                    <div class="quiz-opt" data-correct="true">B. Mendoakan ampunan, menuntaskan wasiat/hutangnya, dan menyambung silaturahmi dengan sahabat karibnya</div>
                    <div class="quiz-opt" data-correct="false">C. Menggelar pesta peringatan mewah setiap tahun dengan dana hutang</div>
                    <div class="quiz-opt" data-correct="false">D. Menyimpan pakaian dan perabotannya tanpa boleh dipakai oleh siapa pun</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). Sebagaimana hadits riwayat Abu Dawud, cara berbakti setelah orang tua wafat adalah mendoakannya, memohonkan ampunan, menepati janjinya, memuliakan teman-temannya, dan menyambung tali silaturahmi keluarganya.
                  </div>
                </div>
                """
            },
            {
                "title": "Rangkuman Hikmah Menghormati Orang Tua & Guru",
                "badge": "IKHTISAR BAB V",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box card-box-accent">
                    <div class="card-title">🌟 Keberkahan Berbakti Orang Tua:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Mendapat garansi surga Allah Swt.</li>
                      <li>Dipanjangkan umur dalam ketaatan dan dilapangkan pintu rezekinya.</li>
                      <li>Kelak anak keturunannya akan berbakti serupa kepadanya.</li>
                    </ul>
                  </div>
                  <div class="card-box">
                    <div class="card-title">📚 Keberkahan Menghormati Guru:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Ilmu yang dipelajari menjadi mudah dipahami dan berbuah amal saleh.</li>
                      <li>Memperoleh kemudahan derajat martabat yang tinggi di mata manusia dan Allah.</li>
                      <li>Didoakan para malaikat penuntut ilmu di segenap penjuru langit dan bumi.</li>
                    </ul>
                  </div>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-6-keteladanan-nabi-musa-as.html",
        "full_title": "BAB VI: Kisah Keteladanan Nabi Musa As. — Akidah Akhlak Kelas VIII MTs",
        "chapter_label": "BAB VI: Keteladanan Nabi Musa As.",
        "badge_text": "K8 • SEMESTER 1",
        "theme_color": "#06b6d4",
        "theme_light": "#67e8f9",
        "theme_subtle": "rgba(6, 182, 212, 0.16)",
        "badge_gradient": "#0891b2, #06b6d4",
        "radial_color": "#164e63",
        "slides": [
            {
                "title": "Kisah Keteladanan Nabi Musa As.",
                "badge": "PENGANTAR BAB VI",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">🌊🦯</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #22d3ee; margin: 12px 0;">BAB VI: KETELADANAN NABI MUSA AS.</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Sang <em>Kalimullah</em> yang pemberani menentang tirani Fir'aun, pembebas Bani Israil, dan teladan kesabaran dalam menegakkan tauhid sejati.
                  </p>
                  <div class="content-grid-3" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">1. Bayi di Peti Nil</div>
                      <div class="card-desc">Pertolongan Allah menyelamatkan Musa bayi di sarang istana tirani Fir'aun.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">2. Menentang Fir'aun</div>
                      <div class="card-desc">Dakwah santun namun tegas didampingi Nabi Harun as. serta mukjizat tongkat pembelah laut.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">3. Sabar Mengasuh Kaum</div>
                      <div class="card-desc">Ketabahan menghadapi kedegilan Bani Israil dan pengkhianatan patung anak sapi Samiri.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Kelahiran dan Penyelamatan Menakjubkan",
                "badge": "FASE AWAL KEHIDUPAN",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Musa lahir di masa tirani Fir'aun yang mengeluarkan dekrit keji membunuh setiap bayi laki-laki Bani Israil karena ramalan mimpinya. Allah mengilhamkan kepada ibunda Musa untuk menghanyutkan peti bayinya ke Sungai Nil.
                </p>
                <div class="card-box card-box-accent" style="margin-bottom: 16px;">
                  <div class="card-title">Skenario Ilahi di Istana Fir'aun:</div>
                  <div class="card-desc" style="font-size: 21pt; line-height: 1.6;">
                    Peti tersebut ditemukan oleh istri Fir'aun, <strong>Asiyah</strong> binti Muzahim, yang hatinya diliputi kasih sayang. Allah mengharamkan semua ibu susuan bagi Musa hingga saudari perempuannya menawarkan ibu kandung Musa sendiri sebagai perawatnya. Musa dibesarkan di istana musuh yang kelak ia runtuhkan tirani kesyirikannya.
                  </div>
                </div>
                <div class="arabic-box">
                  <div class="arabic-text">فَرَدَدْنَٰهُ إِلَىٰٓ أُمِّهِۦ كَىْ تَقَرَّ عَيْنُهَا وَلَا تَحْزَنَ وَلِتَعْلَمَ أَنَّ وَعْدَ ٱللَّهِ حَقٌّ</div>
                  <div class="arabic-trans">"Maka Kami kembalikan dia (Musa) kepada ibunya, agar senang hatinya dan tidak bersedih hati, dan agar dia mengetahui bahwa janji Allah itu benar..." (QS. Al-Qashas: 13)</div>
                </div>
                """
            },
            {
                "title": "Menerima Risalah di Lembah Thuwa & Menghadapi Fir'aun",
                "badge": "DAKWAH TAUHID",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Wahyu di Bukit Sinai:</div>
                    <div class="card-desc" style="font-size: 21pt; line-height: 1.5;">
                      Di Lembah Thuwa, Allah berfirman langsung kepada Musa as. (sehingga bergelar <em>Kalimullah</em>) dan menganugerahkan dua mukjizat utama: tongkat yang berubah menjadi ular besar dan tangan yang memancarkan cahaya putih tanpa cela.
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Perintah Berdakwah Santun (QS. Thaha: 43-44):</div>
                    <div class="card-desc" style="font-size: 21pt; line-height: 1.5;">
                      <em>"Pergilah kamu berdua kepada Fir'aun, sesungguhnya dia telah melampaui batas; maka berbicaralah kamu berdua kepadanya dengan kata-kata yang lemah lembut, mudah-mudahan dia ingat atau takut."</em>
                    </div>
                  </div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Kekalahan Ahli Sihir Istana:</div>
                  <div class="card-desc" style="font-size: 21pt;">
                    Ketika para ahli sihir Fir'aun melemparkan tali-temali tipu dayanya, tongkat Nabi Musa menelan seluruh muslihat mereka. Para penyihir tersebut langsung bersujud dan beriman kepada Tuhannya Musa dan Harun, rela mati syahid di bawah siksaan Fir'aun.
                  </div>
                </div>
                """
            },
            {
                "title": "Eksodus Bani Israil & Tenggelamnya Pasukan Fir'aun",
                "badge": "MUKJIZAT LAUT MERAH",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Ketika Musa memimpin Bani Israil keluar dari Mesir, pasukan Fir'aun mengejar dengan kekuatan penuh hingga menjepit mereka di tepi Laut Merah. Kaumnya panik dan berkata: <em>"Inna lamudrakuun"</em> (Sesungguhnya kita benar-benar akan tertangkap!).
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">قَالَ كَلَّآ ۖ إِنَّ مَعِىَ رَبِّى سَيَهْدِينِ ﴿٦٢﴾ فَأَوْحَيْنَآ إِلَىٰ مُوسَىٰٓ أَنِ ٱضْرِب بِّعَصَاكَ ٱلْبَحْرَ ۖ فَٱنفَلَقَ فَكَانَ كُلُّ فِرْقٍ كَٱلطَّوْدِ ٱلْعَظِيمِ ﴿٦٣﴾</div>
                  <div class="arabic-trans">"Musa menjawab: 'Sekali-kali tidak! Sesungguhnya Tuhanku bersamaku, Dia akan memberi petunjuk kepadaku.' Lalu Kami wahyukan kepada Musa: 'Pukullah lautan itu dengan tongkatmu.' Maka terbelahlah lautan itu, dan setiap belahan seperti gunung yang besar." (QS. Asy-Syu'ara: 62-63)</div>
                </div>
                """
            },
            {
                "title": "Kesabaran Menghadapi Pembangkangan Bani Israil",
                "badge": "UJIAN DAKWAH",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">Ketabahan Nabi Musa diuji luar biasa setelah Bani Israil selamat melintasi lautan:</p>
                <div class="content-grid-3">
                  <div class="card-box">
                    <div class="card-title">1. Patung Samiri</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Saat Musa bermunajat 40 malam menerima Kitab Taurat, Samiri menghasut kaumnya membuat patung anak sapi emas bersuara untuk disembah.
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">2. Menuntut Lihat Allah</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Kaumnya lancang menolak beriman sebelum melihat Allah secara kasat mata, hingga mereka disambar halilintar lalu dihidupkan kembali.
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">3. Menolak Masuk Palestina</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Kaumnya membangkang berperang: <em>"Pergilah engkau bersama Tuhanmu dan berperanglah berdua, kami duduk menanti di sini"</em> (QS. Al-Maidah: 24).
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Berguru kepada Nabi Khidir As. (Adab Menuntut Ilmu)",
                "badge": "HIKMAH ILMU",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">Tiga Peristiwa Penuh Hikmah Gaib (QS. Al-Kahfi):</div>
                  <div class="card-desc" style="font-size: 21pt; line-height: 1.6; margin-top: 10px;">
                    Musa as. menempuh perjalanan jauh demi berguru kepada hamba saleh pilihan Allah (Khidir as.) untuk belajar kerendahan hati:
                  </div>
                  <ul class="bullet-list" style="margin-top: 10px; font-size: 20pt;">
                    <li><strong>Melubangi Perahu Nelayan:</strong> Menyelamatkan perahu warga miskin dari rampasan raja zalim yang menyita perahu bagus.</li>
                    <li><strong>Membunuh Anak Muda:</strong> Mencegah anak tersebut menjerumuskan kedua orang tuanya yang beriman ke dalam kekafiran saat dewasa.</li>
                    <li><strong>Memperbaiki Dinding Rumah Roboh:</strong> Menjaga harta karun peninggalan orang tua saleh bagi dua anak yatim hingga dewasa.</li>
                  </ul>
                  <div style="font-size: 20pt; color: #22d3ee; margin-top: 12px;">
                    <em>Pelajaran: Keterbatasan pandangan lahiriah manusia harus tunduk di bawah kebijaksanaan takdir ilahi.</em>
                  </div>
                </div>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab VI",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    Pelajaran utama yang dipetik dari dialog antara Nabi Musa as. dan Nabi Khidir as. dalam Surah Al-Kahfi adalah...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Membuktikan bahwa ilmu sihir Mesir lebih unggul dari ilmu wahyu</div>
                    <div class="quiz-opt" data-correct="true">B. Keharusan bersabar dalam menuntut ilmu dan kerendahan hati bahwa di atas orang berilmu ada Yang Maha Tahu</div>
                    <div class="quiz-opt" data-correct="false">C. Pembenaran merusak barang milik orang lain tanpa alasan syar'i</div>
                    <div class="quiz-opt" data-correct="false">D. Larangan bertanya kepada guru dalam majelis ilmu madrasah</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). Kisah Nabi Musa dan Khidir menegaskan etika tawadhu' dalam menuntut ilmu dan kesadaran bahwa ilmu manusia sangat terbatas di hadapan rahasia hikmah Allah.
                  </div>
                </div>
                """
            },
            {
                "title": "Rangkuman Butir Keteladanan Nabi Musa As.",
                "badge": "IKHTISAR BAB VI",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box card-box-accent">
                    <div class="card-title">🛡️ Karakter Kepemimpinan Nabi Musa As.:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li><strong>Keberanian Luar Biasa:</strong> Teguh membela kaum tertindas dan tidak gentar menghadapi penguasa tiran berdarah dingin.</li>
                      <li><strong>Ketulusan Tawakkal:</strong> Yakin mutlak akan pertolongan Allah saat terpojok di depan lautan luas.</li>
                    </ul>
                  </div>
                  <div class="card-box">
                    <div class="card-title">🌾 Refleksi bagi Siswa MTs:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Berani menegakkan kebenaran dan menolak perundungan (*bullying*) di lingkungan pergaulan.</li>
                      <li>Berbicara santun (*qaulan layyinan*) sekalipun kepada orang yang berbuat salah.</li>
                      <li>Memiliki etos sabar yang tak kunjung padam dalam menuntut ilmu.</li>
                    </ul>
                  </div>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-7-keteladanan-rasul-ulul-azmi.html",
        "full_title": "BAB VII: Kisah Keteladanan Rasul Ulul Azmi — Akidah Akhlak Kelas VIII MTs",
        "chapter_label": "BAB VII: Rasul Ulul Azmi",
        "badge_text": "K8 • SEMESTER 2",
        "theme_color": "#14b8a6",
        "theme_light": "#5eead4",
        "theme_subtle": "rgba(20, 184, 166, 0.16)",
        "badge_gradient": "#0d9488, #14b8a6",
        "radial_color": "#134e4a",
        "slides": [
            {
                "title": "Kisah Keteladanan Rasul Ulul Azmi",
                "badge": "PENGANTAR BAB VII",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">👑⛰️</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #5eead4; margin: 12px 0;">BAB VII: KETELADANAN RASUL ULUL AZMI</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Lima nabi dan rasul istimewa pemegang keteguhan tekad baja, kesabaran tanpa batas, dan ketabahan luar biasa dalam mengemban amanah risalah ilahiah.
                  </p>
                  <div class="content-grid-4" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">🚢 Nabi Nuh As.</div>
                      <div class="card-desc" style="font-size: 19pt;">Dakwah 950 tahun penuh kesabaran dan bahtera penyelamat banjir bandang.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">🔥 Nabi Ibrahim As.</div>
                      <div class="card-desc" style="font-size: 19pt;">Bapak ketauhidan, dinginnya api Namrud, dan keikhlasan qurban agung.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">🦯 Nabi Musa As.</div>
                      <div class="card-desc" style="font-size: 19pt;">Keberanian menumpas Fir'aun dan pembawa Kitab Taurat suci.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">🕊️ Nabi Isa As. & Saw.</div>
                      <div class="card-desc" style="font-size: 19pt;">Kasih sayang, mukjizat penyembuh, dan penyempurna Muhammad Saw.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Pengertian & Syarat Gelar Ulul Azmi",
                "badge": "HAKIKAT ULUL AZMI",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Secara bahasa, <strong>Ulu</strong> (أُولُو) berarti mempunyai/memiliki, dan <strong>Al-'Azmi</strong> (العَزْم) berarti tekad bulat, kemauan kokoh, atau keteguhan hati. Menurut istilah syar'i, <strong>Ulul Azmi</strong> adalah gelar kehormatan bagi para rasul yang memiliki ketabahan luar biasa, keteguhan hati pantang menyerah, dan kesabaran tiada tara dalam menghadapi rintangan dakwah tauhid.
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">فَٱصْبِرْ كَمَا صَبَرَ أُو۟لُوا۟ ٱلْعَزْمِ مِنَ ٱلرُّسُلِ وَلَا تَسْتَعْجِل لَّهُمْ</div>
                  <div class="arabic-trans">"Maka bersabarlah engkau (Muhammad) sebagaimana kesabaran rasul-rasul yang memiliki keteguhan hati (Ulul Azmi), dan janganlah engkau meminta agar azab disegerakan untuk mereka..." (QS. Al-Ahqaf: 35)</div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Kriteria Khusus Rasul Ulul Azmi:</div>
                  <ul class="bullet-list" style="font-size: 20pt;">
                    <li>Memiliki ketabahan luar biasa tatkala diintimidasi, diusir, bahkan diancam dibunuh oleh kaumnya.</li>
                    <li>Senantiasa mendoakan hidayah dan kebaikan bagi umatnya, bukan meminta kehancuran lekas.</li>
                    <li>Memiliki tekad baja (*azam*) yang tak tergoyahkan oleh bujuk rayu harta, tahta, maupun derita fisik.</li>
                  </ul>
                </div>
                """
            },
            {
                "title": "Kisah Nabi Nuh As. & Nabi Ibrahim As.",
                "badge": "RASUL 1 & 2",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">🚢 1. Nabi Nuh As. (Sabar 950 Tahun)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Berdakwah selama sembilan setengah abad siang dan malam, namun hanya segelintir pengikut yang beriman. Bahkan istri dan putranya sendiri (Kan'an) membangkang dan tenggelam dalam air bah. Nuh tetap tabah membuat bahtera di atas bukit meski dihujani cemoohan.
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">🔥 2. Nabi Ibrahim As. (Bapak Tauhid)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Diuji menghadapi ayahnya si pembuat berhala (Azar) dan Raja Namrud. Ketika dilempar ke kobaran api unggun raksasa, Allah memerintahkan: <em>"Wahai api, jadilah dingin dan penyelamat bagi Ibrahim!"</em> (QS. Al-Anbiya: 69). Diuji pula menyembelih putra tercintanya Ismail as. yang ia laksanakan dengan kepasrahan mutlak.
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Kisah Nabi Musa As. & Nabi Isa As.",
                "badge": "RASUL 3 & 4",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">🦯 3. Nabi Musa As. (Menghadapi Kedegilan)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Menghadapi raja paling tiran dalam sejarah (Fir'aun) yang mengaku tuhan. Disertai ujian berat membimbing Bani Israil yang berulang kali membangkang, menyembah anak sapi Samiri, dan menuntut mukjizat materi tiada henti.
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">🕊️ 4. Nabi Isa As. (Kasih & Zuhud)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Lahir tanpa ayah atas kekuasaan kalimat Allah melalui Maryam binti Imran. Sejak bayi mampu berbicara membela kesucian ibundanya. Menyembuhkan orang buta, kusta, dan menghidupkan orang mati atas izin Allah. Ditolak oleh pemuka Yahudi munafik hingga diselamatkan dan diangkat Allah ke langit.
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Nabi Muhammad Saw. (Penutup Para Nabi / Khatamul Anbiya)",
                "badge": "PENGHULU ULUL AZMI",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">🌟 Sayyidul Awwalin wal Akhirin (Rahmatan Lil 'Alamin):</div>
                  <p style="font-size: 22pt; line-height: 1.6; margin-top: 10px;">
                    Mendapat cobaan paling komprehensif sejak yatim piatu, diboikot 3 tahun di Syi'ib Abi Thalib hingga kelaparan, dilempari batu berdarah-darah di Thaif, namun beliau menolak tawaran Malaikat Jibril untuk menimpakan gunung, seraya berdoa:
                  </p>
                  <blockquote style="font-size: 22pt; font-style: italic; color: #a7f3d0; margin: 14px 0; padding-left: 20px; border-left: 4px solid #14b8a6;">
                    "Ya Allah, ampunilah kaumku, sesungguhnya mereka tidak mengetahui!"
                  </blockquote>
                  <p style="font-size: 21pt; color: #cbd5e1; line-height: 1.5;">
                    Puncak mukjizat beliau adalah Al-Qur'an Al-Karim dan peristiwa Isra' Mi'raj menerima perintah shalat lima waktu, serta akhlak budi pekerti yang menjadi cerminan Al-Qur'an berjalan.
                  </p>
                </div>
                """
            },
            {
                "title": "Tabel Ikhtisar 5 Rasul Ulul Azmi & Kitab Samawi",
                "badge": "MATRIKS MUKJIZAT",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th>Nama Rasul</th>
                      <th>Kitab Suci</th>
                      <th>Kaum / Musuh Utama</th>
                      <th>Mukjizat Terbesar</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Nuh As.</strong></td>
                      <td>Shuhuf</td>
                      <td>Bani Rasib pembangkang</td>
                      <td>Bahtera raksasa penyelamat banjir bandang global.</td>
                    </tr>
                    <tr>
                      <td><strong>Ibrahim As.</strong></td>
                      <td>Shuhuf Ibrahim</td>
                      <td>Raja Namrud & Babilonia</td>
                      <td>Api dingin yang menyelamatkan, pembangunan Ka'bah.</td>
                    </tr>
                    <tr>
                      <td><strong>Musa As.</strong></td>
                      <td>Kitab Taurat</td>
                      <td>Raja Fir'aun Mesir</td>
                      <td>Tongkat membelah Laut Merah, tangan bersinar.</td>
                    </tr>
                    <tr>
                      <td><strong>Isa As.</strong></td>
                      <td>Kitab Injil</td>
                      <td>Bani Israil / Romawi</td>
                      <td>Lahir tanpa ayah, berbicara saat bayi, menyembuhkan kusta.</td>
                    </tr>
                    <tr>
                      <td><strong>Muhammad Saw.</strong></td>
                      <td>Al-Qur'an Al-Karim</td>
                      <td>Kafir Quraisy & Seluruh Alam</td>
                      <td>Al-Qur'an abadi, Isra' Mi'raj, membelah bulan.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab VII",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    Di antara 25 nabi dan rasul yang wajib diimani, terdapat lima orang yang mendapat gelar kehormatan "Ulul Azmi". Singkatan akronim populer untuk mengingat urutan kelima rasul tersebut adalah...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. ADAM (Adam, Daud, Ayub, Musa)</div>
                    <div class="quiz-opt" data-correct="true">B. NIMIM (Nuh, Ibrahim, Musa, Isa, Muhammad Saw.)</div>
                    <div class="quiz-opt" data-correct="false">C. ISMA (Ibrahim, Sulaiman, Musa, Adam)</div>
                    <div class="quiz-opt" data-correct="false">D. YASIN (Yusuf, Ayub, Syuaib, Idris, Nuh)</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). Akronim <em>NIMIM</em> mempermudah mengingat lima Rasul Ulul Azmi: <strong>N</strong>uh As., <strong>I</strong>brahim As., <strong>M</strong>usa As., <strong>I</strong>sa As., dan <strong>M</strong>uhammad Saw.
                  </div>
                </div>
                """
            },
            {
                "title": "Keteladanan Hidup Siswa Madrasah dari Ulul Azmi",
                "badge": "IKHTISAR BAB VII",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">🌟 Mutiara Hikmah untuk Generasi Remaja:</div>
                  <ul class="bullet-list" style="font-size: 21pt; margin-top: 10px;">
                    <li><strong>Memiliki Ketahanan Mental (*Grit*):</strong> Tidak mudah mengeluh ketika tugas sekolah menumpuk atau menghadapi ulangan yang sulit.</li>
                    <li><strong>Pemaaf dan Pengasih:</strong> Membalas ejekan atau keburukan orang lain dengan senyuman dan doa kebaikan, meneladani Rasulullah di Thaif.</li>
                    <li><strong>Istiqamah Menegakkan Kebenaran:</strong> Teguh menolak pergaulan yang merusak moral meski dijauhi oleh kelompok sebaya.</li>
                  </ul>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-8-akhlak-terpuji-husnuzzan-tawadhu-tasamuh-taawun.html",
        "full_title": "BAB VIII: Akhlak Terpuji (Husnuzzan, Tawadhu', Tasamuh, Ta'awun) — Akidah Akhlak K8",
        "chapter_label": "BAB VIII: Husnuzzan, Tawadhu', Tasamuh, Ta'awun",
        "badge_text": "K8 • SEMESTER 2",
        "theme_color": "#3b82f6",
        "theme_light": "#93c5fd",
        "theme_subtle": "rgba(59, 130, 246, 0.16)",
        "badge_gradient": "#2563eb, #3b82f6",
        "radial_color": "#1e3a8a",
        "slides": [
            {
                "title": "Membiasakan Akhlak Terpuji Sosial",
                "badge": "PENGANTAR BAB VIII",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">🤝🌸</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #93c5fd; margin: 12px 0;">BAB VIII: AKHLAK SOSIAL TERPUJI</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Empat pilar keharmonisan hidup bermasyarakat: <strong>Husnuzzan</strong> (Berbaik Sangka), <strong>Tawadhu'</strong> (Rendah Hati), <strong>Tasamuh</strong> (Toleransi), dan <strong>Ta'awun</strong> (Tolong-Menolong).
                  </p>
                  <div class="content-grid-4" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">1. Husnuzzan</div>
                      <div class="card-desc" style="font-size: 19pt;">Beningnya prasangka kepada Allah, diri sendiri, dan sesama insan.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">2. Tawadhu'</div>
                      <div class="card-desc" style="font-size: 19pt;">Kerendahan hati tanpa merasa lebih mulia dari hamba lainnya.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">3. Tasamuh</div>
                      <div class="card-desc" style="font-size: 19pt;">Toleransi lapang dada menghargai perbedaan ragam latar belakang.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title" style="font-size: 21pt;">4. Ta'awun</div>
                      <div class="card-desc" style="font-size: 19pt;">Gotong royong saling membantu dalam kebajikan dan ketakwaan.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Husnuzzan: Membersihkan Prasangka Pikiran",
                "badge": "PILAR 1: HUSNUZZAN",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Husnuzzan</strong> (حُسْنُ الظَّنِّ) berarti berbaik sangka atau memandang segala sesuatu dengan kacamata positif. Lawan katanya adalah <em>su'udzan</em> (berburuk sangka).
                </p>
                <div class="content-grid-3">
                  <div class="card-box">
                    <div class="card-title">1. Kepada Allah</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Yakin bahwa semua ketetapan Allah penuh hikmah kebaikan, dan doa pasti dikabulkan pada saat yang paling tepat. Hadits Qudsi: <em>"Aku sesuai prasangka hamba-Ku kepada-Ku."</em>
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">2. Kepada Diri Sendiri</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Optimis dan percaya diri atas potensi karunia Allah dalam diri, pantang menyerah dan terus mengembangkan bakat.
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">3. Kepada Sesama Manusia</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Mengedepankan klarifikasi (*tabayyun*) dan tidak terburu-buru menuduh motif buruk atas perkataan atau perbuatan teman (QS. Al-Hujurat: 12).
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Tawadhu': Kemuliaan dalam Kerendahan Hati",
                "badge": "PILAR 2: TAWADHU'",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Tawadhu'</strong> adalah sikap rendah hati, menerima kebenaran dari siapa pun yang mengucapkannya, dan tidak memandang remeh orang lain sekalipun ia miskin atau berpangkat rendah.
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">وَعِبَادُ ٱلرَّحْمَٰنِ ٱلَّذِينَ يَمْشُونَ عَلَى ٱلْأَرْضِ هَوْنًا وَإِذَا خَاطَبَهُمُ ٱلْجَٰهِلُونَ قَالُوا۟ سَلَٰمًا</div>
                  <div class="arabic-trans">"Adapun hamba-hamba Tuhan Yang Maha Pengasih itu adalah orang-orang yang berjalan di bumi dengan rendah hati dan apabila orang-orang bodoh menyapa mereka (dengan kata-kata menghina), mereka mengucapkan 'salam'." (QS. Al-Furqan: 63)</div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Janji Kemuliaan Bagi Orang Tawadhu' (HR. Muslim):</div>
                  <div class="card-desc" style="font-size: 21pt;">
                    <em>"Wa maa tawadha'a ahadun lillahi illaa rafa'ahullah"</em> (Tidaklah seseorang merendahkan hatinya karena Allah, melainkan Allah akan mengangkat derajat martabatnya!).
                  </div>
                </div>
                """
            },
            {
                "title": "Tasamuh: Toleransi Islami yang Berkeadaban",
                "badge": "PILAR 3: TASAMUH",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Tasamuh</strong> adalah sikap lapang dada, tenggang rasa, dan menghargai perbedaan keyakinan, suku, budaya, serta sudut pandang fikih furu'iyah tanpa mengorbankan akidah tauhid.
                </p>
                <div class="content-grid-2">
                  <div class="card-box card-box-accent">
                    <div class="card-title">Batasan Toleransi dalam Islam:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li><strong>Dalam Urusan Sosial (Muamalah):</strong> Sangat dianjurkan saling tolong-menolong, bekerja sama menjaga keamanan, dan berbuat adil kepada siapa pun (QS. Al-Mumtahanah: 8).</li>
                      <li><strong>Dalam Urusan Akidah & Ibadah:</strong> Tegas memegang prinsip: <em>"Lakum diinukum wa liya diin"</em> (Bagimu agamamu, dan bagiku agamaku). Tidak boleh mencampuradukkan ritual peribadatan (QS. Al-Kafirun: 6).</li>
                    </ul>
                  </div>
                  <div class="card-box">
                    <div class="card-title">Contoh Tasamuh dalam Fikih:</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Saling menghormati sesama muslim saat berbeda amalan cabang (furu'), seperti qunut subuh, jumlah rakaat tarawih, atau lafal niat shalat tanpa saling menuduh sesat atau membid'ahkan.
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Ta'awun: Tolong-Menolong dalam Kebaikan",
                "badge": "PILAR 4: TA'AWUN",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Ta'awun</strong> adalah sikap saling membantu, gotong royong, dan bersinergi dalam mewujudkan kemaslahatan bersama serta mencegah kezaliman.
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">وَتَعَاوَنُوا۟ عَلَى ٱلْبِرِّ وَٱلتَّقْوَىٰ ۖ وَلَا تَعَاوَنُوا۟ عَلَى ٱلْإِثْمِ وَٱلْعُدْوَٰنِ ۚ وَٱتَّقُوا۟ ٱللَّهَ ۖ إِنَّ ٱللَّهَ شَدِيدُ ٱلْعِقَابِ</div>
                  <div class="arabic-trans">"...Dan tolong-menolonglah kamu dalam (mengerjakan) kebajikan dan takwa, dan jangan tolong-menolong dalam berbuat dosa dan permusuhan. Bertakwalah kepada Allah, sesungguhnya Allah sangat berat siksaan-Nya." (QS. Al-Ma'idah: 2)</div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Praktek Ta'awun di Madrasah:</div>
                  <div class="card-desc" style="font-size: 21pt;">
                    Membantu teman yang kesulitan memahami pelajaran, menggalang dana sosial bagi teman yang tertimpa musibah duka, membersihkan musala bersama, dan menolak tegas ajakan menyontek massal atau tawuran pelajar.
                  </div>
                </div>
                """
            },
            {
                "title": "Sinergi 4 Pilar Membangun Masyarakat Madani",
                "badge": "INTEGRASI SOSIAL",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th>Sikap Mulia</th>
                      <th>Perwujudan Keseharian</th>
                      <th>Dampak bagi Harmoni Bangsa</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong style="color: #93c5fd;">Husnuzzan</strong></td>
                      <td>Tabayyun terhadap berita, tidak menyebarkan gosip.</td>
                      <td>Mencegah fitnah dan polarisasi permusuhan di medsos.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #93c5fd;">Tawadhu'</strong></td>
                      <td>Suka berbaur tanpa membedakan kaya-miskin.</td>
                      <td>Menghilangkan sekat kasta sosial dan arogansi kekuasaan.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #93c5fd;">Tasamuh</strong></td>
                      <td>Menghargai tradisi damai dan keragaman suku.</td>
                      <td>Memperkokoh persatuan NKRI dan kedamaian antarumat beragama.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #93c5fd;">Ta'awun</strong></td>
                      <td>Aktif kegiatan bakti sosial dan ronda lingkungan.</td>
                      <td>Mempercepat penuntasan kemiskinan dan bencana alam.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab VIII",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    Roni diajak oleh teman sekelasnya untuk bersama-sama membuat contekan ujian semester agar seluruh kelas lulus. Berdasarkan Surah Al-Ma'idah ayat 2, sikap yang tepat bagi Roni adalah...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Menerimanya sebagai bentuk ta'awun solidaritas setia kawan</div>
                    <div class="quiz-opt" data-correct="true">B. Menolaknya dengan tegas karena Islam melarang tolong-menolong dalam perbuatan dosa (*al-itsmi wal 'udwan*)</div>
                    <div class="quiz-opt" data-correct="false">C. Ikut menyontek asalkan tidak ketahuan oleh guru pengawas</div>
                    <div class="quiz-opt" data-correct="false">D. Menerapkannya atas dasar tasamuh menghargai kesepakatan kelompok</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). Tolong-menolong hanya diperintahkan dalam kebajikan dan ketakwaan (<em>al-birri wat-taqwa</em>), sedangkan menyontek adalah kebohongan dan dosa yang dilarang dijadikan objek ta'awun.
                  </div>
                </div>
                """
            },
            {
                "title": "Refleksi Akhlakul Karimah: Bab VIII",
                "badge": "IKHTISAR BAB VIII",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">💎 Pesan Luhur Rasulullah Saw. (HR. Al-Bukhari & Muslim):</div>
                  <p style="font-size: 22pt; line-height: 1.6; margin-top: 10px;">
                    <em>"Perumpamaan orang-orang mukmin dalam hal saling mencintai, saling mengasihi, dan saling menyayangi bagaikan satu tubuh; apabila satu anggota tubuh merasa sakit, maka seluruh anggota tubuh yang lain ikut merasakan demam dan tidak dapat tidur."</em>
                  </p>
                  <div style="margin-top: 16px; font-size: 21pt; color: #93c5fd;">
                    Jadikan dirimu pembawa kedamaian, bukan pemantik perselisihan; tebarkan prasangka baik, hiasi diri dengan tawadhu', lapangkan dada dengan tasamuh, dan ulurkan tangan dengan ta'awun!
                  </div>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-9-akhlak-tercela-hasad-dendam-ghibah-fitnah-namimah.html",
        "full_title": "BAB IX: Menghindari Akhlak Tercela (Hasad, Dendam, Ghibah, Fitnah, Namimah) — K8",
        "chapter_label": "BAB IX: Hasad, Dendam, Ghibah, Fitnah, Namimah",
        "badge_text": "K8 • SEMESTER 2",
        "theme_color": "#e11d48",
        "theme_light": "#fda4af",
        "theme_subtle": "rgba(225, 29, 72, 0.16)",
        "badge_gradient": "#be123c, #e11d48",
        "radial_color": "#881337",
        "slides": [
            {
                "title": "Menghindari Akhlak Tercela Pergaulan",
                "badge": "PENGANTAR BAB IX",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">☠️🔥</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #fda4af; margin: 12px 0;">BAB IX: PENGHANCUR PERSAUDARAAN</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Lima racun pergaulan yang merusak kedamaian masyarakat: <strong>Hasad</strong> (Dengki), <strong>Dendam</strong>, <strong>Ghibah</strong> (Gosip), <strong>Fitnah</strong>, dan <strong>Namimah</strong> (Adu Domba).
                  </p>
                  <div class="content-grid-3" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">1. Hasad & Dendam</div>
                      <div class="card-desc">Benci melihat orang lain bahagia dan menyimpan niat jahat membalas dendam kesumat.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">2. Ghibah & Fitnah</div>
                      <div class="card-desc">Membicarakan aib orang lain di belakangnya dan menyebarkan tuduhan dusta tanpa bukti.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">3. Namimah</div>
                      <div class="card-desc">Provokasi mengadu domba dua pihak agar saling bermusuhan dan putus silaturahmi.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Hasad (Dengki): Pemakan Amal Kebaikan",
                "badge": "PENYAKIT 1: HASAD",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Hasad</strong> adalah rasa benci, tidak senang, atau gelisah di hati ketika melihat orang lain mendapatkan nikmat dari Allah, disertai harapan agar nikmat tersebut segera lenyap dari orang itu.
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">إِيَّاكُمْ وَالْحَسَدَ فَإِنَّ الْحَسَدَ يَأْكُلُ الْحَسَنَاتِ كَمَا تَأْكُلُ النَّارُ الْحَطَبَ</div>
                  <div class="arabic-trans">"Jauhilah olehmu sifat hasad (dengki), karena sesungguhnya hasad itu memakan kebaikan-kebaikan sebagaimana api memakan kayu bakar." (HR. Abu Dawud)</div>
                </div>
                <div class="content-grid-2" style="margin-top: 14px;">
                  <div class="card-box">
                    <div class="card-title">Bahaya Hasad:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Menentang qadha dan pembagian rezeki Allah Swt.</li>
                      <li>Hatinya selalu menderita dan gelisah melihat keberhasilan orang lain.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Ghibthah (Iri yang Dibolehkan):</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Iri positif ingin meniru kebaikan orang lain tanpa mengharap nikmatnya hilang, misalnya ingin hafal Qur'an seperti temannya atau dermawan seperti pengusaha saleh.
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Dendam (Al-Hiqd): Bara Api Kebencian",
                "badge": "PENYAKIT 2: DENDAM",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Dendam</strong> adalah menyimpan perasaan sakit hati dan kebencian mendalam di dada, disertai tekad membara untuk membalas perbuatan buruk orang lain dengan keburukan yang serupa atau lebih parah.
                </p>
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Ciri Pribadi Pendendam:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Sulit memaafkan kesalahan teman kendati orang itu telah meminta maaf.</li>
                      <li>Selalu menunggu momen kelemahan musuh untuk mempermalukannya.</li>
                      <li>Wajahnya masam dan hatinya kaku dari sifat kasih sayang.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Kemuliaan Membuka Pintu Maaf:</div>
                    <div class="card-desc" style="font-size: 21pt; line-height: 1.5;">
                      <em>"Dan orang-orang yang menahan amarahnya dan memaafkan (kesalahan) orang lain. Dan Allah mencintai orang-orang yang berbuat kebajikan."</em> (QS. Ali 'Imran: 134). Memaafkan membebaskan jiwa dari racun kepahitan.
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Ghibah (Menggunjing): Memakan Bangkai Saudara",
                "badge": "PENYAKIT 3: GHIBAH",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Nabi Saw. mendefinisikan <strong>Ghibah</strong>: <em>"Engkau menceritakan saudaramu tentang sesuatu yang tidak disukainya."</em> Meskipun apa yang diceritakan itu memang benar adanya faktanya! (Bila ceritanya bohong, maka itu dinamakan <strong>Fitnah / Buhtan</strong>).
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">وَلَا يَغْتَب بَّعْضُكُم بَعْضًا ۚ أَيُحِبُّ أَحَدُكُمْ أَن يَأْكُلَ لَحْمَ أَخِيهِ مَيْتًا فَكَرِهْتُمُوهُ ۚ وَٱتَّقُوا۟ ٱللَّهَ</div>
                  <div class="arabic-trans">"...dan janganlah sebagian kamu menggunjing sebagian yang lain. Sukakah salah seorang di antara kamu memakan daging saudaranya yang sudah mati? Maka tentulah kamu merasa jijik kepadanya. Dan bertakwalah kepada Allah..." (QS. Al-Hujurat: 12)</div>
                </div>
                """
            },
            {
                "title": "Fitnah dan Namimah: Pemutus Ikatan Ukhuwah",
                "badge": "PENYAKIT 4 & 5",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box card-box-accent">
                    <div class="card-title">⚠️ Fitnah (Menuduh Dusta)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Menyebarkan kabar bohong atau menuduhkan aib yang tidak pernah dilakukan seseorang demi merusak nama baiknya.
                    </div>
                    <div style="font-size: 20pt; color: #fda4af; margin-top: 10px;">
                      <em>"Al-fitnatu asyaddu minal qatl"</em> (Fitnah itu dosanya lebih besar dan kejam daripada pembunuhan biasa!) (QS. Al-Baqarah: 191).
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">🐍 Namimah (Adu Domba)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Menukil omongan orang lain dengan tujuan memicu permusuhan dan membakar amarah dua pihak yang sebelumnya rukun.
                    </div>
                    <div style="font-size: 20pt; color: #fda4af; margin-top: 10px;">
                      Rasulullah Saw.: <em>"Laa yadkhulul jannata qattaatun (nam-maam)"</em> (Tidak akan masuk surga orang yang suka mengadu domba!). (HR. Al-Bukhari & Muslim).
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Strategi Menangkis Ghibah & Namimah di Era Digital",
                "badge": "BENTENG DIRI",
                "content": """
                <ul class="bullet-list">
                  <li class="bullet-item">
                    <span class="bullet-icon">🛡️</span>
                    <div><strong>Budaya Tabayyun (Klarifikasi):</strong> Jangan langsung percaya atau membagikan berita viral sebelum mengecek fakta kebenarannya (QS. Al-Hujurat: 6).</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">🛡️</span>
                    <div><strong>Tegas Menolak Masuk Majelis Gosip:</strong> Apabila ada teman yang mulai menggunjingkan orang lain, ingatkan dengan sopan atau segera alihkan pembicaraan / tinggalkan obrolan tersebut.</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">🛡️</span>
                    <div><strong>Menjaga Lidah & Jemari (Hifzhul Lisan):</strong> Mengingat hisab akhirat bahwa setiap kata dan ketikan postingan akan dipertanggungjawabkan di hadapan Allah (QS. Qaf: 18).</div>
                  </li>
                </ul>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab IX",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    Zaid mendengar Hasan menceritakan kejelekan Umar. Kemudian Zaid mendatangi Umar dan menceritakan kembali perkataan Hasan dengan sengaja agar Umar marah dan membenci Hasan. Tindakan yang dilakukan Zaid dinamakan...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Ghibah karena menceritakan aib teman secara jujur</div>
                    <div class="quiz-opt" data-correct="true">B. Namimah (adu domba) karena memindahkan perkataan demi memicu permusuhan</div>
                    <div class="quiz-opt" data-correct="false">C. Fitnah karena membuat berita palsu yang belum tentu terjadi</div>
                    <div class="quiz-opt" data-correct="false">D. Hasad karena menginginkan nikmat Hasan berpindah padanya</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). Memindahkan omongan atau informasi kepada pihak lain dengan motif merusak hubungan persahabatan dan menyalakan api kebencian adalah definisi persis dari <em>Namimah</em>.
                  </div>
                </div>
                """
            },
            {
                "title": "Rangkuman Refleksi Hati Nurani: Bab IX",
                "badge": "IKHTISAR BAB IX",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">🌟 Kunci Keselamatan Lidah (HR. Al-Bukhari & Muslim):</div>
                  <blockquote style="font-size: 22pt; font-style: italic; color: #fecdd3; margin: 14px 0; padding-left: 20px; border-left: 4px solid #e11d48; line-height: 1.6;">
                    "Barangsiapa beriman kepada Allah dan hari akhir, hendaklah ia berkata yang baik atau diam!"
                  </blockquote>
                  <p style="font-size: 21pt; color: #f1f5f9; line-height: 1.5;">
                    Sibukkan diri dengan memperbaiki kekurangan dan aib diri sendiri, sehingga tidak ada waktu lagi untuk mengintai cela orang lain atau menyulut api perpecahan!
                  </p>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-10-adab-bersosial-media-dalam-islam.html",
        "full_title": "BAB X: Adab Bersosial Media dalam Pandangan Islam — Akidah Akhlak K8",
        "chapter_label": "BAB X: Adab Bersosial Media dalam Islam",
        "badge_text": "K8 • SEMESTER 2",
        "theme_color": "#8b5cf6",
        "theme_light": "#c4b5fd",
        "theme_subtle": "rgba(139, 92, 246, 0.16)",
        "badge_gradient": "#7c3aed, #8b5cf6",
        "radial_color": "#4c1d95",
        "slides": [
            {
                "title": "Adab Bersosial Media dalam Pandangan Islam",
                "badge": "PENGANTAR BAB X",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">📱🌐</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #c4b5fd; margin: 12px 0;">BAB X: ADAB BERSOSIAL MEDIA DALAM ISLAM</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Menjadikan teknologi digital dan media sosial sebagai ladang dakwah, sarana silaturahmi, dan sumber pahala jariyah bagi generasi muslim modern.
                  </p>
                  <div class="content-grid-3" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">1. Panduan Syar'i Digital</div>
                      <div class="card-desc">Etika berkomunikasi di dunia maya, menjaga privasi aurat, dan saring sebelum sharing.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">2. Menangkal Hoaks & Bullying</div>
                      <div class="card-desc">Menerapkan prinsip tabayyun, menolak cyberbullying, dan menjaga jejak digital bersih.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">3. Dakwah Kreatif</div>
                      <div class="card-desc">Mengisi ruang maya dengan konten inspiratif, video edukatif, dan amar ma'ruf nahi munkar.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Urgensi Etika Bermedsos di Era Digital",
                "badge": "TANTANGAN MODERN",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Media sosial (WhatsApp, Instagram, TikTok, YouTube, X/Twitter) adalah ruang publik baru umat manusia. Dalam timbangan akidah Islam, setiap ketikan jemari, komentar, dan video unggahan memiliki hisab pertanggungjawaban yang setara dengan perkataan lisan secara langsung.
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">مَّا يَلْفِظُ مِن قَوْلٍ إِلَّا لَدَيْهِ رَقِيبٌ عَتِيدٌ</div>
                  <div class="arabic-trans">"Tiada suatu ucapan pun yang diucapkannya melainkan ada di dekatnya malaikat pengawas yang selalu hadir (Raqib dan 'Atid)." (QS. Qaf: 18)</div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Prinsip Emas: "Jemari adalah Cermin Akhlak"</div>
                  <div class="card-desc" style="font-size: 21pt;">
                    Seorang muslim tidak mengenal istilah anonimitas di hadapan Allah Swt. Akun palsu sekalipun tetap berada dalam pantauan CCTV ilahi yang Maha Mengetahui gerak-gerik hati nurani.
                  </div>
                </div>
                """
            },
            {
                "title": "Prinsip Tabayyun: Saring Sebelum Sharing",
                "badge": "VERIFIKASI INFORMASI",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Islam mewajibkan umatnya memverifikasi setiap kabar atau berita yang beredar agar terhindar dari penyebaran hoaks (*kadzib*) yang mencelakai masyarakat (QS. Al-Hujurat [49]: 6):
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">يَٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوٓا۟ إِن جَآءَكُمْ فَاسِقٌۢ بِنَبَإٍ فَتَبَيَّنُوٓا۟ أَن تُصِيبُوا۟ قَوْمًۢا بِجَهَٰلَةٍ فَتُصْبِحُوا۟ عَلَىٰ مَا فَعَلْتُمْ نَٰدِمِينَ</div>
                  <div class="arabic-trans">"Wahai orang-orang yang beriman! Jika seseorang yang fasik datang kepadamu membawa suatu berita, maka telitilah kebenarannya, agar kamu tidak mencelakakan suatu kaum karena kebodohan (kecerobohan), yang akhirnya kamu menyesali perbuatanmu itu." (QS. Al-Hujurat: 6)</div>
                </div>
                """
            },
            {
                "title": "6 Adab Islami Bermedia Sosial",
                "badge": "PEDOMAN AMALIAH",
                "content": """
                <div class="content-grid-3">
                  <div class="card-box">
                    <div class="card-title">1. Niat Kebaikan</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Meniatkan medsos untuk menyambung silaturahmi, belajar ilmu bermanfaat, dan menebar inspirasi kebaikan.
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">2. Qaulan Sadidan</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Bertutur kata benar, sopan, menjauhi caci maki, sarkasme merendahkan, dan ujaran kebencian.
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">3. Menjaga Aurat & Privasi</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Tidak mengunggah foto/video membuka aurat, pose tidak senonoh, atau menyebarkan data pribadi orang lain (*doxxing*).
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">4. Tolak Cyberbullying</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Tidak melakukan perundungan siber, berkomentar merusak mental orang, atau ikut-ikutan menghujat massal.
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">5. Menghargai Hak Cipta</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Mencantumkan sumber orisinil, tidak melakukan plagiarisme karya cipta digital tanpa izin.
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">6. Manajemen Waktu</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Membatasi screen time, tidak melalaikan kewajiban shalat fardhu, belajar, dan berbakti kepada orang tua.
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Bahaya Dosa Jariyah di Media Sosial",
                "badge": "PERINGATAN DIGITAL",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">⚠️ Mengalirnya Dosa Tanpa Disadari (*Sayyi'ah Jariyah*):</div>
                  <p style="font-size: 22pt; line-height: 1.6; margin-top: 10px;">
                    Sebagaimana kebaikan bisa menjadi <strong>sedekah jariyah</strong> yang pahalanya terus mengalir pasca kematian, perbuatan dosa di media sosial (seperti mengunggah konten maksiat, menyebarkan fitnah, atau musik keji) yang ditonton dan ditiru oleh ribuan orang dapat menjadi <strong>dosa jariyah</strong> yang terus menumpuk di alam kubur!
                  </p>
                  <blockquote style="font-size: 21pt; font-style: italic; color: #ddd6fe; margin: 14px 0; padding-left: 20px; border-left: 4px solid #8b5cf6; line-height: 1.6;">
                    "Barangsiapa mengajak kepada keburukan/kesesatan, maka ia memikul dosanya beserta dosa orang-orang yang mengikutinya tanpa dikurangi sedikit pun dari dosa-dosa mereka." (HR. Muslim).
                  </blockquote>
                </div>
                """
            },
            {
                "title": "Medsos Sebagai Ladang Dakwah Kreatif",
                "badge": "OPTIMALISASI MEDSOS",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Peluang Emas Remaja Madrasah:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Membuat infografis kutipan hadits dan ayat Al-Qur'an dengan desain estetik.</li>
                      <li>Berbagi video tilawah merdu atau tips menghafal Al-Qur'an.</li>
                      <li>Membuat konten edukasi sains Islam, adab islami, dan motivasi belajar berprestasi.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Dampak Positif:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Mendapatkan pahala jariyah setiap kali konten tersebut ditonton dan diamalkan.</li>
                      <li>Menyeimbangkan algoritma ruang maya dari banjir konten unfaedah dan maksiat.</li>
                      <li>Mengharumkan citra madrasah dan generasi muda Islam yang cerdas beradab.</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab X",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    Fatimah menerima sebuah pesan berantai di grup WhatsApp tentang skandal seorang tokoh agama tanpa sumber yang jelas. Tindakan yang paling sesuai dengan ajaran Islam adalah...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Langsung meneruskannya (forward) ke seluruh grup keluarga agar waspada</div>
                    <div class="quiz-opt" data-correct="true">B. Melakukan tabayyun (meneliti kebenaran) dan tidak ikut menyebarkannya jika kabar tersebut tidak valid atau mengandung aib</div>
                    <div class="quiz-opt" data-correct="false">C. Menambahkan komentar pedas lalu mengunggahnya ke status WhatsApp</div>
                    <div class="quiz-opt" data-correct="false">D. Menghasut anggota grup lain untuk memboikot tokoh agama tersebut</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). Berdasarkan QS. Al-Hujurat ayat 6, sikap wajib seorang mukmin terhadap berita yang belum pasti adalah melakukan <em>tabayyun</em> (klarifikasi) serta menahan diri dari menyebarkan gosip/fitnah.
                  </div>
                </div>
                """
            },
            {
                "title": "Refleksi Akhir Semester: Generasi Digital Berakhlak",
                "badge": "IKHTISAR BAB X",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">🌐 Resolusi Mukmin Cerdas di Dunia Maya:</div>
                  <p style="font-size: 22pt; line-height: 1.6; margin-top: 10px;">
                    Jadikan smartphone dan akun mediamu sebagai saksi pembela di yaumil hisab, bukan penuntut yang memberatkan siksa!
                  </p>
                  <ul class="bullet-list" style="margin-top: 14px; font-size: 20pt;">
                    <li><strong>Sebelum Mengetik:</strong> Tanya hati, apakah kata-kata ini diridhai Allah?</li>
                    <li><strong>Sebelum Mengunggah:</strong> Tanya hati, apakah gambar/video ini menutup aurat dan bermartabat?</li>
                    <li><strong>Sebelum Meneruskan (Share):</strong> Tanya hati, apakah berita ini sudah pasti benar dan bermanfaat bagi umat?</li>
                  </ul>
                </div>
                """
            }
        ]
    }
]

def build_k8():
    out_dir = "deck-akidah-akhlak-mts-k8"
    os.makedirs(out_dir, exist_ok=True)
    
    for ch in chapters_k8:
        slides = ch["slides"]
        total_slides = len(slides)
        total_slides_pad = f"{total_slides:02d}"
        first_slide_title = slides[0]["title"]
        
        slides_html_parts = []
        drawer_items_parts = []
        
        for idx, s in enumerate(slides):
            active_class = " active" if idx == 0 else ""
            slide_num_str = f"{idx+1:02d}"
            
            # drawer item
            drawer_items_parts.append(f"""
            <div class="drawer-item{' active' if idx == 0 else ''}" data-index="{idx}">
              <span style="font-weight: 800; color: var(--primary);">{slide_num_str}.</span>
              <span>{s['title']}</span>
            </div>
            """)
            
            # slide card
            slides_html_parts.append(f"""
            <section class="slide{active_class}" data-index="{idx}" data-title="{s['title']}">
              <div class="slide-header">
                <div>
                  <span class="slide-topic-badge">{s['badge']}</span>
                  <h2 class="slide-title">{s['title']}</h2>
                </div>
                <div style="font-size: 16pt; color: #94a3b8; font-weight: 700;">
                  SLIDE {slide_num_str} / {total_slides_pad}
                </div>
              </div>
              <div class="slide-body">
                {s['content']}
              </div>
            </section>
            """)
            
        full_html = HTML_TEMPLATE.format(
            full_title=ch["full_title"],
            chapter_label=ch["chapter_label"],
            badge_text=ch["badge_text"],
            theme_color=ch["theme_color"],
            theme_light=ch["theme_light"],
            theme_subtle=ch["theme_subtle"],
            badge_gradient=ch["badge_gradient"],
            radial_color=ch["radial_color"],
            total_slides_pad=total_slides_pad,
            first_slide_title=first_slide_title,
            slides_html="\n".join(slides_html_parts),
            drawer_items_html="\n".join(drawer_items_parts)
        )
        
        filepath = os.path.join(out_dir, ch["filename"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"Created K8: {filepath}")

    # Build index.html for K8
    build_k8_index(out_dir)

def build_k8_index(out_dir):
    cards_html = []
    
    chapter_metadata = [
        ("Bab I: Al-Qur'an dan Keistimewaannya", "bab-1-al-quran-dan-keistimewaannya.html", "SEMESTER 1", "#38bdf8", "📖", "Kalamullah abadi, sejarah penurunan berangsur, mukjizat ilmiah sastra, dan 6 kandungan utama."),
        ("Bab II: Mukjizat & Kejadian Luar Biasa", "bab-2-mukjizat-dan-kejadian-luar-biasa.html", "SEMESTER 1", "#34d399", "⚡", "Mukjizat hissiyah-maknawiyah, karamah wali, ma'unah mukmin, irhash rasul vs sihir/istidraj."),
        ("Bab III: Ikhtiar, Tawakkal, Sabar, Syukur, Qana'ah", "bab-3-akhlak-terpuji-ikhtiar-tawakkal-sabar-syukur-qanaah.html", "SEMESTER 1", "#fcd34d", "💎", "Lima pilar pembangun mental spiritual tangguh menghadapi takdir dan dinamika kehidupan."),
        ("Bab IV: Ananiyah, Putus Asa, Ghadhab, Tamak", "bab-4-akhlak-tercela-ananiyah-putus-asa-ghadhab-tamak.html", "SEMESTER 1", "#fb7185", "⚠️", "Mendeteksi dan membersihkan hati dari penyakit egois, putus asa, pemarah, dan serakah dunia."),
        ("Bab V: Adab kepada Orang Tua dan Guru", "bab-5-adab-kepada-orang-tua-dan-guru.html", "SEMESTER 1", "#c084fc", "👵", "Birrul walidain, kunci ridha ilahi, adab ta'dzim memuliakan guru pewaris para nabi."),
        ("Bab VI: Keteladanan Nabi Musa As.", "bab-6-keteladanan-nabi-musa-as.html", "SEMESTER 1", "#22d3ee", "🦯", "Keberanian Kalimullah menentang tirani Fir'aun, mukjizat Laut Merah, dan kesabaran membina kaum."),
        ("Bab VII: Keteladanan Rasul Ulul Azmi", "bab-7-keteladanan-rasul-ulul-azmi.html", "SEMESTER 2", "#5eead4", "👑", "Keteguhan tekad baja lima nabi pilihan: Nuh, Ibrahim, Musa, Isa, dan Muhammad Saw."),
        ("Bab VIII: Husnuzzan, Tawadhu', Tasamuh, Ta'awun", "bab-8-akhlak-terpuji-husnuzzan-tawadhu-tasamuh-taawun.html", "SEMESTER 2", "#93c5fd", "🤝", "Harmoni masyarakat madani: prasangka baik, rendah hati, toleransi luhur, dan gotong royong taqwa."),
        ("Bab IX: Hasad, Dendam, Ghibah, Fitnah, Namimah", "bab-9-akhlak-tercela-hasad-dendam-ghibah-fitnah-namimah.html", "SEMESTER 2", "#fda4af", "☠️", "Bahaya racun pergaulan: dengki pemakan amal, dendam kesumat, gosip bangkai, dan adu domba."),
        ("Bab X: Adab Bersosial Media dalam Islam", "bab-10-adab-bersosial-media-dalam-islam.html", "SEMESTER 2", "#c4b5fd", "📱", "Panduan etika digital syar'i, saring sebelum sharing (tabayyun), dan dakwah kreatif remaja.")
    ]
    
    for title, link, sem, col, icon, desc in chapter_metadata:
        cards_html.append(f"""
        <a href="{link}" class="card-item">
          <div class="card-badge" style="background: {col}; color: #041326;">{sem}</div>
          <div class="card-icon">{icon}</div>
          <h2 class="card-title">{title}</h2>
          <p class="card-desc">{desc}</p>
          <div class="card-link" style="color: {col};">Buka Presentasi Bab &rarr;</div>
        </a>
        """)
        
    index_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide Deck Akidah Akhlak MTs Kelas VIII — KMA 183</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: radial-gradient(circle at 50% 10%, #0f2b48 0%, #070d19 80%);
      color: #ffffff;
      font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
      font-size: 22pt;
      min-height: 100vh;
      padding: 60px 40px;
    }}
    .container {{
      max-width: 1400px;
      margin: 0 auto;
    }}
    .header {{
      text-align: center;
      margin-bottom: 50px;
    }}
    .badge-top {{
      display: inline-block;
      background: linear-gradient(135deg, #0284c7, #38bdf8);
      color: #041326;
      font-size: 16pt;
      font-weight: 800;
      padding: 8px 24px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 16px;
    }}
    h1 {{
      font-size: 42pt;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 16px;
    }}
    .subtitle {{
      font-size: 24pt;
      color: #94a3b8;
      max-width: 900px;
      margin: 0 auto 30px auto;
      line-height: 1.5;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
      gap: 28px;
    }}
    .card-item {{
      background: #0f192c;
      border: 1px solid #273e66;
      border-radius: 20px;
      padding: 32px;
      text-decoration: none;
      color: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    }}
    .card-item:hover {{
      transform: translateY(-6px);
      border-color: #38bdf8;
      box-shadow: 0 20px 45px rgba(56, 189, 248, 0.2);
    }}
    .card-badge {{
      align-self: flex-start;
      font-size: 14pt;
      font-weight: 800;
      padding: 4px 14px;
      border-radius: 999px;
      margin-bottom: 16px;
    }}
    .card-icon {{
      font-size: 40pt;
      margin-bottom: 14px;
    }}
    .card-title {{
      font-size: 24pt;
      font-weight: 800;
      margin-bottom: 12px;
      line-height: 1.35;
      color: #f8fafc;
    }}
    .card-desc {{
      font-size: 19pt;
      color: #cbd5e1;
      line-height: 1.5;
      margin-bottom: 24px;
      flex: 1;
    }}
    .card-link {{
      font-size: 20pt;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .nav-cross {{
      margin-top: 60px;
      background: #111d33;
      border: 1px solid #223759;
      border-radius: 20px;
      padding: 30px;
      text-align: center;
    }}
    .nav-cross h3 {{ font-size: 24pt; margin-bottom: 16px; }}
    .nav-cross-links {{
      display: flex;
      justify-content: center;
      gap: 20px;
      flex-wrap: wrap;
    }}
    .nav-cross-btn {{
      background: #1e293b;
      color: #e2e8f0;
      border: 1px solid #334155;
      padding: 10px 24px;
      border-radius: 12px;
      font-size: 18pt;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .nav-cross-btn:hover {{
      background: #38bdf8;
      color: #041326;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header class="header">
      <span class="badge-top">KEMENTERIAN AGAMA RI • KMA 183</span>
      <h1>Slide Deck Akidah Akhlak MTs Kelas VIII</h1>
      <p class="subtitle">
        Modul Pembelajaran Multimedia Mandiri: 10 Bab Lengkap (Semester Ganjil & Genap) — Dark Mode Penuh, Tipografi 22pt+, Dilengkapi Dalil Al-Qur'an & Hadits Shahih, Tabel Analisis, dan Kuis Evaluasi Formatif.
      </p>
    </header>

    <main class="grid">
      {"".join(cards_html)}
    </main>

    <footer class="nav-cross">
      <h3>Akses Lintas Modul Deck Digital MTs</h3>
      <div class="nav-cross-links">
        <a href="../deck-akidah-akhlak-mts-k7/index.html" class="nav-cross-btn">📖 Akidah Akhlak Kelas VII</a>
        <a href="../deck-akidah-akhlak-mts-k9/index.html" class="nav-cross-btn">📖 Akidah Akhlak Kelas IX</a>
        <a href="../deck-fikih-mts-k7/index.html" class="nav-cross-btn">⚖️ Fikih Kelas VII</a>
        <a href="../deck-fikih-mts-k8/index.html" class="nav-cross-btn">⚖️ Fikih Kelas VIII</a>
        <a href="../deck-fikih-mts-k9/index.html" class="nav-cross-btn">⚖️ Fikih Kelas IX</a>
      </div>
    </footer>
  </div>
</body>
</html>
"""
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_content)
    print(f"Created K8 Index: {os.path.join(out_dir, 'index.html')}")

if __name__ == "__main__":
    build_k8()
