#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from generate_decks_k8_k9 import HTML_TEMPLATE

chapters_k9 = [
    {
        "filename": "bab-1-iman-kepada-hari-akhir.html",
        "full_title": "BAB I: Beriman kepada Hari Akhir — Akidah Akhlak Kelas IX MTs",
        "chapter_label": "BAB I: Beriman kepada Hari Akhir",
        "badge_text": "K9 • SEMESTER 1",
        "theme_color": "#f59e0b",
        "theme_light": "#fcd34d",
        "theme_subtle": "rgba(245, 158, 11, 0.16)",
        "badge_gradient": "#d97706, #f59e0b",
        "radial_color": "#78350f",
        "slides": [
            {
                "title": "Beriman kepada Hari Akhir (Hari Kiamat)",
                "badge": "PENGANTAR BAB I",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">⏳🌌</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #fcd34d; margin: 12px 0;">BAB I: IMAN KEPADA HARI AKHIR</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Rukun Iman kelima: Mengimani hancurnya seluruh alam semesta dan dimulainya fase kehidupan abadi pembalasan amal manusia.
                  </p>
                  <div class="content-grid-3" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">1. Kiamat Sugra & Kubra</div>
                      <div class="card-desc">Kematian individu, bencana alam, tanda-tanda kecil/besar kiamat, dan tiupan sangkakala Israfil.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">2. Tahapan Alam Gaib</div>
                      <div class="card-desc">Barzakh, Ba'ats, Mahsyar, Mizan, Hisab, Shirath, hingga pembalasan Surga dan Neraka.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">3. Dampak Amaliah</div>
                      <div class="card-desc">Membentuk pribadi mawas diri (*muhasabah*), gemar beramal saleh, dan takut berbuat dosa.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Pengertian dan Dalil Iman kepada Hari Akhir",
                "badge": "HAKIKAT IMAN",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Beriman kepada Hari Akhir</strong> adalah meyakini dengan sepenuh hati bahwa seluruh alam semesta beserta isinya suatu hari akan hancur lebur dan musnah, lalu manusia akan dibangkitkan dari kubur untuk mempertanggungjawabkan segala amalnya di hadapan Allah Swt.
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">يَٰٓأَيُّهَا ٱلنَّاسُ ٱتَّقُوا۟ رَبَّكُمْ ۚ إِنَّ زَلْزَلَةَ ٱلسَّاعَةِ شَىْءٌ عَظِيمٌ</div>
                  <div class="arabic-trans">"Wahai manusia! Bertakwalah kepada Tuhanmu; sesungguhnya guncangan hari kiamat itu adalah suatu kejadian yang sangat besar (dahsyat)." (QS. Al-Hajj: 1)</div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Kebenaran Mutlak Hari Akhir (QS. Al-Hajj: 7):</div>
                  <div class="card-desc" style="font-size: 21pt;">
                    <em>"Wa annas-saa'ata aatiyatul laa raiba fiihaa wa annallaaha yab'atsu man fil qubuur"</em> (Dan sungguh, hari kiamat itu pasti datang, tidak ada keraguan padanya; dan sungguh, Allah akan membangkitkan siapa pun yang di dalam kubur).
                  </div>
                </div>
                """
            },
            {
                "title": "Pembagian Kiamat: Sugra dan Kubra",
                "badge": "KLASIFIKASI KIAMAT",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">1. Kiamat Sugra (Kiamat Kecil)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Kematian tiap-tiap makhluk bernyawa atau kehancuran sebagian wilayah di muka bumi akibat bencana alam (gempa bumi, tsunami, banjir).
                    </div>
                    <ul class="bullet-list" style="margin-top: 8px; font-size: 19pt;">
                      <li><em>"Kullu nafsin dzaa'iqatul maut"</em> (Tiap-tiap jiwa akan merasakan mati — QS. Ali 'Imran: 185).</li>
                      <li>Kematian adalah kiamat kecil bagi orang yang mengalaminya karena terputusnya amal dunia.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">2. Kiamat Kubra (Kiamat Besar)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Kehancuran total seluruh tata surya dan jagat raya semesta saat Malaikat Israfil meniup sangkakala yang pertama (<em>Nafkhatush Sha'iq</em>).
                    </div>
                    <ul class="bullet-list" style="margin-top: 8px; font-size: 19pt;">
                      <li>Langit terbelah, bintang-bintang berjatuhan, lautan meluap menjadi api (QS. At-Takwir & Al-Infithar).</li>
                      <li>Gunung-gunung dihambur-hamburkan seperti bulu-bulu yang beterbangan (QS. Al-Qari'ah).</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Tanda-Tanda Datangnya Hari Kiamat",
                "badge": "TANDA-TANDA KIAMAT",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Tanda-Tanda Kecil (Shughra):</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Diutus dan wafatnya Nabi Muhammad Saw.</li>
                      <li>Ilmu agama diangkat dengan wafatnya para ulama saleh.</li>
                      <li>Banyak perzinaan, minuman keras diminum terang-terangan.</li>
                      <li>Orang-orang miskin berlomba-lomba meninggikan bangunan megah.</li>
                      <li>Zaman terasa berjalan sangat cepat.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Tanda-Tanda Besar (Kubra):</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Munculnya <strong>Dajjal</strong> pembawa fitnah terbesar.</li>
                      <li>Turunnya <strong>Nabi Isa As.</strong> menegakkan keadilan syariat Islam.</li>
                      <li>Keluarnya bangsa perusak <strong>Ya'juj dan Ma'juj</strong>.</li>
                      <li>Terbitnya matahari dari ufuk barat (*Thulu'usy Syamsi min Maghribiha*).</li>
                      <li>Munculnya binatang melata yang berbicara (*Dabbatul Ardh*).</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Kronologi Perjalanan Ruh di Alam Akhirat",
                "badge": "TAHAPAN ALAM GAIB",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th style="width: 25%;">Tahapan / Alam</th>
                      <th style="width: 35%;">Pengertian & Peristiwa</th>
                      <th>Kondisi Hamba Beriman</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Alam Barzakh</strong></td>
                      <td>Dinding pembatas antara dunia fana dan akhirat; kubur.</td>
                      <td>Mendapat nikmat kubur dan diterangi seluas pandangan mata.</td>
                    </tr>
                    <tr>
                      <td><strong>Yaumul Ba'ats</strong></td>
                      <td>Hari kebangkitan seluruh manusia dari kubur.</td>
                      <td>Bangkit dengan wajah berseri-seri penuh cahaya wudhu.</td>
                    </tr>
                    <tr>
                      <td><strong>Yaumul Mahsyar</strong></td>
                      <td>Pengumpulan di padang datar luas di bawah matahari sejengkal.</td>
                      <td>Mendapatkan naungan 'Arsy Allah dari sengatan dahsyat.</td>
                    </tr>
                    <tr>
                      <td><strong>Hisab & Mizan</strong></td>
                      <td>Perhitungan teliti dan penimbangan bobot timbangan amal.</td>
                      <td>Menerima buku catatan amal dengan tangan kanan (*hisaban yasira*).</td>
                    </tr>
                    <tr>
                      <td><strong>Shirath & Jaza'</strong></td>
                      <td>Jembatan di atas neraka menuju Surga pembalasan abadi.</td>
                      <td>Melintas secepat kilat menyambar dan kekal dalam kenikmatan surga.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            {
                "title": "Perilaku Cerminan Beriman kepada Hari Akhir",
                "badge": "IMPLEMENTASI AMAL",
                "content": """
                <ul class="bullet-list">
                  <li class="bullet-item">
                    <span class="bullet-icon">✦</span>
                    <div><strong>Senantiasa Mawas Diri (Muhasabah):</strong> Menyadari bahwa setiap bisikan hati, tatapan mata, dan gerak tangan dicatat oleh malaikat Raqib dan 'Atid serta disaksikan oleh bumi tempat berpijak.</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">✦</span>
                    <div><strong>Giat Memperbanyak Amal Jariyah:</strong> Tidak tertipu kemewahan dunia yang fana, melainkan menyisihkan harta, tenaga, dan ilmunya sebagai bekal kekal di akhirat kelak.</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">✦</span>
                    <div><strong>Teguh Memegang Kejujuran:</strong> Yakin bahwa kezaliman yang lolos dari hukuman pengadilan dunia pasti akan diadili di Mahkamah Adil Ilahi tanpa sedikit pun kezaliman.</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">✦</span>
                    <div><strong>Ikhlas Menerima Takdir dan Tabah:</strong> Menyadari penderitaan dunia hanya sementara dan akan diganti dengan kebahagiaan abadi di surga Jannatun Na'im.</div>
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
                    Peristiwa dibangkitkannya seluruh manusia dari dalam kubur sejak manusia pertama Nabi Adam as. hingga manusia terakhir dinamakan...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Yaumul Mahsyar</div>
                    <div class="quiz-opt" data-correct="true">B. Yaumul Ba'ats</div>
                    <div class="quiz-opt" data-correct="false">C. Yaumul Hisab</div>
                    <div class="quiz-opt" data-correct="false">D. Yaumul Jaza'</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). <em>Yaumul Ba'ats</em> (يَوْمُ البَعْثِ) secara harfiah adalah Hari Kebangkitan manusia dari alam kubur setelah tiupan sangkakala kedua Malaikat Israfil.
                  </div>
                </div>
                """
            },
            {
                "title": "Rangkuman Refleksi Keimanan Hari Akhir",
                "badge": "IKHTISAR BAB I",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">💡 Pesan Kehidupan Singkat (HR. Al-Bukhari):</div>
                  <blockquote style="font-size: 22pt; font-style: italic; color: #fef08a; margin: 14px 0; padding-left: 20px; border-left: 4px solid #f59e0b; line-height: 1.6;">
                    "Hiduplah engkau di dunia ini seakan-akan orang asing atau seorang pengembara yang sedang melintasi jalan!"
                  </blockquote>
                  <p style="font-size: 21pt; color: #cbd5e1; line-height: 1.5;">
                    Dunia adalah ladang tempat menanam bibit (*mazra'atul akhirah*), sedangkan akhirat adalah hari memanen buahnya. Tanamlah kebaikan hari ini agar memanen rida Allah di hari kemudian!
                  </p>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-2-akhlak-terpuji-diri-sendiri.html",
        "full_title": "BAB II: Akhlak Terpuji kepada Diri Sendiri — Akidah Akhlak Kelas IX MTs",
        "chapter_label": "BAB II: Akhlak Terpuji Diri Sendiri",
        "badge_text": "K9 • SEMESTER 1",
        "theme_color": "#10b981",
        "theme_light": "#6ee7b7",
        "theme_subtle": "rgba(16, 185, 129, 0.16)",
        "badge_gradient": "#059669, #10b981",
        "radial_color": "#064e3b",
        "slides": [
            {
                "title": "Akhlak Terpuji kepada Diri Sendiri",
                "badge": "PENGANTAR BAB II",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">🧠🚀</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #34d399; margin: 12px 0;">BAB II: AKHLAK KEPADA DIRI SENDIRI</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Membangun karakter unggul generasi muslim: <strong>Berilmu, Kerja Keras, Kreatif, Produktif,</strong> dan <strong>Inovatif</strong> demi menyongsong masa depan gemilang.
                  </p>
                  <div class="content-grid-3" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">1. Berilmu & Kerja Keras</div>
                      <div class="card-desc">Semangat haus ilmu (*tholabul 'ilmi*) dan ketekunan banting tulang pantang berpangku tangan.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">2. Kreatif & Inovatif</div>
                      <div class="card-desc">Daya cipta gagasan baru yang bermanfaat dan pembaharuan solusi atas berbagai tantangan zaman.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">3. Produktif</div>
                      <div class="card-desc">Memaksimalkan waktu untuk menghasilkan karya nyata yang bernilai faedah bagi umat.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Berilmu: Mahkota Kemuliaan Insan",
                "badge": "PILAR 1: BERILMU",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Berilmu</strong> adalah keadaan memiliki pemahaman mendalam tentang ajaran agama maupun ilmu pengetahuan umum, serta mengamalkannya dalam kehidupan.
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">يَرْفَعِ ٱللَّهُ ٱلَّذِينَ ءَامَنُوا۟ مِنكُمْ وَٱلَّذِينَ أُوتُوا۟ ٱلْعِلْمَ دَرَجَٰتٍ</div>
                  <div class="arabic-trans">"...niscaya Allah akan mengangkat (derajat) orang-orang yang beriman di antaramu dan orang-orang yang diberi ilmu beberapa derajat." (QS. Al-Mujadilah: 11)</div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Kewajiban Menuntut Ilmu (HR. Ibnu Majah):</div>
                  <div class="card-desc" style="font-size: 21pt;">
                    <em>"Thalabul 'ilmi fariidhatun 'ala kulli muslim"</em> (Menuntut ilmu itu hukumnya wajib bagi setiap orang muslim!). Orang berilmu tanpa amal ibarat pohon tak berbuah.
                  </div>
                </div>
                """
            },
            {
                "title": "Kerja Keras: Jihad Membangun Martabat",
                "badge": "PILAR 2: KERJA KERAS",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Kerja Keras</strong> adalah berusaha secara bersungguh-sungguh mengerahkan tenaga, waktu, dan pikiran demi mencapai target yang diridhai Allah, tanpa mudah menyerah atau malas.
                </p>
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Kemuliaan Bekerja Sendiri:</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Rasulullah Saw. bersabda: <em>"Tidak ada makanan yang lebih baik bagi seseorang selain makanan yang ia peroleh dari hasil keringat tangannya sendiri. Sesungguhnya Nabi Daud as. makan dari hasil usahanya sendiri."</em> (HR. Al-Bukhari).
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Ciri Mukmin Pekerja Keras:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Bangun pagi hari dan memulai aktivitas dengan basmalah.</li>
                      <li>Fokus menyelesaikan tugas sekolah tepat waktu.</li>
                      <li>Tidak mengharapkan belas kasihan atau meminta-minta kepada orang lain.</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Kreatif dan Inovatif: Pemimpin Perubahan",
                "badge": "PILAR 3 & 4",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box card-box-accent">
                    <div class="card-title">🎨 Kreatif (Daya Cipta)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Kemampuan berpikir di luar kebiasaan (*out of the box*) untuk melahirkan gagasan-gagasan baru, melihat peluang dari masalah, dan mendayagunakan potensi secara artistik dan fungsional.
                    </div>
                    <ul class="bullet-list" style="margin-top: 10px; font-size: 19pt;">
                      <li>Menemukan metode belajar cerdas yang menyenangkan.</li>
                      <li>Memanfaatkan barang bekas menjadi media belajar berguna.</li>
                    </ul>
                  </div>
                  <div class="card-box">
                    <div class="card-title">💡 Inovatif (Pembaruan)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Kemampuan merealisasikan ide baru ke dalam bentuk teknologi, sistem, atau produk nyata yang lebih efektif, efisien, dan memecahkan permasalahan umat.
                    </div>
                    <ul class="bullet-list" style="margin-top: 10px; font-size: 19pt;">
                      <li>Menciptakan aplikasi dakwah atau riset sains madrasah.</li>
                      <li>Mengembangkan teknik budidaya ramah lingkungan.</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Produktif: Memaksimalkan Nilai Tambah Waktu",
                "badge": "PILAR 5: PRODUKTIF",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  <strong>Produktif</strong> adalah sikap senantiasa memanfaatkan waktu, tenaga, dan karunia yang dimiliki untuk menghasilkan karya nyata (*output*) yang bernilai guna dan memberi maslahat.
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">فَإِذَا فَرَغْتَ فَٱنصَبْ ﴿٧﴾ وَإِلَىٰ رَبِّكَ فَٱرْغَب ﴿٨﴾</div>
                  <div class="arabic-trans">"Maka apabila engkau telah selesai (dari suatu urusan), tetaplah bekerja keras (untuk urusan yang lain), dan hanya kepada Tuhanmulah engkau berharap." (QS. Al-Insyirah: 7-8)</div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Manusia Terbaik di Sisi Rasulullah Saw.:</div>
                  <div class="card-desc" style="font-size: 21pt;">
                    <em>"Khairun-naasi anfa'uhum lin-naas"</em> (Sebaik-baik manusia adalah yang paling banyak memberi manfaat bagi sesama manusia!). (HR. Ath-Thabrani).
                  </div>
                </div>
                """
            },
            {
                "title": "Tabel Komparasi Profil Karakter Remaja Unggul",
                "badge": "MATRIKS KARAKTER",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th>Karakter Unggul</th>
                      <th>Ciri Perilaku Siswa MTs</th>
                      <th>Musuh / Kebiasaan Negatif yang Dikikis</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong style="color: #6ee7b7;">Berilmu</strong></td>
                      <td>Gemar membaca buku, aktif bertanya, menghormati guru.</td>
                      <td>Kebodohan, malas membaca (*low literacy*).</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #6ee7b7;">Kerja Keras</strong></td>
                      <td>Tekun mengerjakan proyek, pantang mengeluh tugas sulit.</td>
                      <td>Sikap manja, suka jalan pintas menyontek.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #6ee7b7;">Kreatif</strong></td>
                      <td>Mencari sudut pandang alternatif saat memecahkan masalah.</td>
                      <td>Pikiran kaku, suka meniru tanpa improvisasi.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #6ee7b7;">Produktif</strong></td>
                      <td>Menghasilkan tulisan artikel, karya seni, atau hafalan Qur'an.</td>
                      <td>Menghabiskan waktu main game online berjam-jam.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #6ee7b7;">Inovatif</strong></td>
                      <td>Menciptakan solusi baru bagi kegiatan musala/kelas.</td>
                      <td>Pasrah pada keadaan lama yang tertinggal.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab II",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    Surah Al-Insyirah ayat 7 yang berbunyi <em>"Fa-idza faraghta fanshab"</em> mengajarkan kepada setiap muslim untuk senantiasa memiliki sikap...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Tawadhu' dan tidak memamerkan prestasinya</div>
                    <div class="quiz-opt" data-correct="true">B. Produktif dan kerja keras, segera beralih melakukan karya bermanfaat berikutnya setelah menyelesaikan suatu tugas</div>
                    <div class="quiz-opt" data-correct="false">C. Qana'ah dengan beristirahat penuh tanpa memikirkan pekerjaan lain</div>
                    <div class="quiz-opt" data-correct="false">D. Menunggu perintah orang lain sebelum memulai sesuatu</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). Makna <em>"Fa-idza faraghta fanshab"</em> menuntun kita untuk tidak berdiam diri menganggur; begitu satu tugas tuntas, segera songsong karya amal kebajikan produktif berikutnya.
                  </div>
                </div>
                """
            },
            {
                "title": "Rangkuman Refleksi Sukses Generasi Emas Madrasah",
                "badge": "IKHTISAR BAB II",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">🚀 Rumus Sukses Pemuda Muslim:</div>
                  <p style="font-size: 22pt; line-height: 1.6; margin-top: 10px;">
                    Peradaban emas Islam di masa lalu dibangun oleh ilmuwan seperti Ibnu Sina, Al-Khawarizmi, dan Al-Biruni yang memadukan keimanan tauhid kokoh dengan etos <strong>ilmu, kerja keras, kreativitas, dan produktivitas</strong> tinggi.
                  </p>
                  <div style="margin-top: 16px; font-size: 21pt; color: #6ee7b7;">
                    Jadikan masa mudamu di MTs sebagai kawah candradimuka: Belajar tanpa lelah, berkarya tanpa batas, dan niatkan semuanya lillahi ta'ala!
                  </div>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-3-adab-kepada-saudara-teman-tetangga.html",
        "full_title": "BAB III: Adab kepada Saudara, Teman, dan Tetangga — Akidah Akhlak Kelas IX MTs",
        "chapter_label": "BAB III: Adab Saudara, Teman & Tetangga",
        "badge_text": "K9 • SEMESTER 1",
        "theme_color": "#0ea5e9",
        "theme_light": "#7dd3fc",
        "theme_subtle": "rgba(14, 165, 233, 0.16)",
        "badge_gradient": "#0284c7, #0ea5e9",
        "radial_color": "#075985",
        "slides": [
            {
                "title": "Adab kepada Saudara, Teman, dan Tetangga",
                "badge": "PENGANTAR BAB III",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">🏡🤝</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #38bdf8; margin: 12px 0;">BAB III: ADAB KEPADA SAUDARA, TEMAN & TETANGGA</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Membangun jalinan persaudaraan (*ukhuwah*) yang hangat, damai, dan penuh penghormatan dalam lingkaran sosial terdekat kita.
                  </p>
                  <div class="content-grid-3" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">1. Adab kepada Saudara</div>
                      <div class="card-desc">Kasih sayang kandung, menghormati kakak, menyayangi adik, dan menyambung tali rahim.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">2. Adab kepada Teman</div>
                      <div class="card-desc">Saling menasihati dalam kebenaran, menjaga rahasia, setia kawan, dan menolak perundungan.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">3. Adab kepada Tetangga</div>
                      <div class="card-desc">Hak tetangga dalam syariat, berbagi hidangan, tidak mengganggu, dan menjenguk saat sakit.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Dalil Perintah Menjaga Ukhuwah & Adab Bertetangga",
                "badge": "DALIL NAQLI",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Islam mengikat persaudaraan sesama mukmin layaknya satu bangunan kokoh yang saling menguatkan (QS. Al-Hujurat: 10):
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">إِنَّمَا ٱلْمُؤْمِنُونَ إِخْوَةٌ فَأَصْلِحُوا۟ بَيْنَ أَخَوَيْكُمْ ۚ وَٱتَّقُوا۟ ٱللَّهَ لَعَلَّكُمْ تُرْحَمُونَ</div>
                  <div class="arabic-trans">"Sesungguhnya orang-orang mukmin itu bersaudara, karena itu damaikanlah antara kedua saudaramu (yang berselisih) dan bertakwalah kepada Allah agar kamu mendapat rahmat." (QS. Al-Hujurat: 10)</div>
                </div>
                <div class="arabic-box" style="margin-top: 14px;">
                  <div class="arabic-text">مَنْ كَانَ يُؤْمِنُ بِاللَّهِ وَالْيَوْمِ الْآخِرِ فَلْيُكْرِمْ جَارَهُ</div>
                  <div class="arabic-trans">"Barangsiapa beriman kepada Allah dan hari akhir, hendaklah ia memuliakan tetangganya!" (HR. Al-Bukhari & Muslim)</div>
                </div>
                """
            },
            {
                "title": "Adab Islami kepada Saudara Kandung / Kerabat",
                "badge": "SILATURAHMI KELUARGA",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Adab kepada Kakak (Yang Lebih Tua):</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Menghormati pendapatnya dan bertutur kata sopan.</li>
                      <li>Meminta bimbingan dalam hal kebaikan dan mematuhi arahan positifnya.</li>
                      <li>Tidak memotong pembicaraan atau bersikap congkak di hadapannya.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Adab kepada Adik (Yang Lebih Muda):</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Menyayangi dengan tulus, mengayomi, dan memberikan teladan akhlak mulia.</li>
                      <li>Membantu kesulitan belajarnya dengan sabar tanpa membentak.</li>
                      <li>Rasulullah Saw.: <em>"Bukan golongan kami orang yang tidak menyayangi yang lebih muda dan tidak menghormati yang lebih tua."</em> (HR. At-Tirmidzi).</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Adab Bergaul dengan Teman Sebaya",
                "badge": "ETIKA PERTEMANAN",
                "content": """
                <ul class="bullet-list">
                  <li class="bullet-item">
                    <span class="bullet-icon">🤝</span>
                    <div><strong>Mengucapkan Salam dan Berwajah Ramah:</strong> Tersenyum di hadapan saudaramu adalah sedekah. Memulai salam saat bertemu di madrasah.</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">🤝</span>
                    <div><strong>Menjaga Aib dan Rahasia Sahabat:</strong> Tidak mengumbar kelemahan teman kepada orang lain, apalagi menjadikannya bahan lelucon publik.</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">🤝</span>
                    <div><strong>Saling Menasihati dalam Kebaikan & Kesabaran (*Tawashau bil Haq*):</strong> Menegur dengan penuh kasih tatkala melihat teman berbuat salah, dan menjaganya dari maksiat.</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">🤝</span>
                    <div><strong>Menghindari Panggilan Ejekan Buruk:</strong> Memanggil teman dengan nama yang disukainya, bukan dengan julukan fisik atau celaan merendahkan (QS. Al-Hujurat: 11).</div>
                  </li>
                </ul>
                """
            },
            {
                "title": "Adab Mulia terhadap Tetangga Sekitar Rumah",
                "badge": "HAK TETANGGA",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Malaikat Jibril as. begitu sering mewasiatkan hak tetangga kepada Nabi Muhammad Saw. hingga beliau mengira tetangga akan mendapatkan bagian hak waris!
                </p>
                <div class="content-grid-3">
                  <div class="card-box">
                    <div class="card-title">1. Tidak Mengganggu</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Tidak menyalakan musik keras-keras, tidak membuang sampah di depan halamannya, dan tidak memarkir kendaraan menghalangi jalan keluar tetangga.
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">2. Berbagi Makanan</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Nabi Saw. bersabda kepada Abu Dzar: <em>"Jika engkau memasak sayur berkuah, perbanyaklah airnya lalu perhatikanlah para tetanggamu (bagikanlah kepada mereka)!"</em> (HR. Muslim).
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">3. Tolong-Menolong</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Menjenguk tetangga saat jatuh sakit, membantu saat ada hajatan/kemalangan, serta menjaga rumahnya saat ia sedang bepergian ke luar kota.
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Tiga Kategori Tetangga dan Hak-Haknya dalam Islam",
                "badge": "KLASIFIKASI SYARIAT",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th>Kategori Tetangga</th>
                      <th>Jumlah Hak</th>
                      <th>Rincian Hak Syar'i</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong style="color: #38bdf8;">1. Tetangga Muslim yang masih Kerabat</strong></td>
                      <td><strong>3 Hak</strong></td>
                      <td>Hak sebagai sesama Muslim, hak tetangga sekitar, dan hak tali persaudaraan rahim keluarga.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #38bdf8;">2. Tetangga Muslim (bukan kerabat)</strong></td>
                      <td><strong>2 Hak</strong></td>
                      <td>Hak sebagai sesama Muslim (salam, jenazah, dll.) dan hak kehormatan bertetangga.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #38bdf8;">3. Tetangga Non-Muslim</strong></td>
                      <td><strong>1 Hak</strong></td>
                      <td>Hak perlindungan dan kenyamanan sebagai tetangga (tidak diganggu, berbuat adil, diberi bingkisan halal).</td>
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
                    Seorang tetangga beragama non-muslim yang tinggal bersebelahan dengan rumah kita sedang tertimpa musibah sakit. Sikap adab islami yang paling tepat adalah...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Membiarkannya karena berbeda keyakinan agama</div>
                    <div class="quiz-opt" data-correct="false">B. Menunggu hingga ia masuk Islam baru ditolong</div>
                    <div class="quiz-opt" data-correct="true">C. Menjenguknya, memberikan bantuan kemanusiaan, dan mendoakan kesembuhan fisiknya karena ia memiliki hak tetangga</div>
                    <div class="quiz-opt" data-correct="false">D. Mengajaknya berdebat teologi saat sedang terbaring lemah</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (C). Tetangga non-muslim tetap memiliki satu hak syar'i yaitu hak tetangga. Islam memerintahkan berbuat baik, menjenguk saat sakit, dan berbuat kebajikan sosial kepada mereka selama tidak memerangi agama kita.
                  </div>
                </div>
                """
            },
            {
                "title": "Rangkuman Hikmah Keberkahan Silaturahmi",
                "badge": "IKHTISAR BAB III",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">🌟 Janji Rasulullah Saw. (HR. Al-Bukhari & Muslim):</div>
                  <blockquote style="font-size: 22pt; font-style: italic; color: #bae6fd; margin: 14px 0; padding-left: 20px; border-left: 4px solid #0ea5e9; line-height: 1.6;">
                    "Barangsiapa yang ingin dilapangkan rezekinya dan dipanjangkan umurnya (diberkahi jejak hidupnya), hendaklah ia menyambung tali silaturahmi!"
                  </blockquote>
                  <p style="font-size: 21pt; color: #f1f5f9; line-height: 1.5;">
                    Rumah yang penuh dengan adab kepada tetangga, sahabat, dan keluarga akan senantiasa dinaungi rahmat dan dijauhkan dari petaka fitnah perpecahan!
                  </p>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-4-keteladanan-umar-bin-khattab-dan-sayyidah-aisyah.html",
        "full_title": "BAB IV: Keteladanan Umar bin Khattab Ra. & Sayyidah Aisyah Ra. — K9",
        "chapter_label": "BAB IV: Umar bin Khattab & Sayyidah Aisyah",
        "badge_text": "K9 • SEMESTER 1",
        "theme_color": "#ec4899",
        "theme_light": "#f472b6",
        "theme_subtle": "rgba(236, 72, 153, 0.16)",
        "badge_gradient": "#db2777, #ec4899",
        "radial_color": "#831843",
        "slides": [
            {
                "title": "Keteladanan Sahabat Umar bin Khattab Ra. & Sayyidah Aisyah Ra.",
                "badge": "PENGANTAR BAB IV",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">🗡️📜</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #f472b6; margin: 12px 0;">BAB IV: UMAR BIN KHATTAB & SAYYIDAH AISYAH</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Perpaduan ketegasan keadilan Khalifah kedua <em>Al-Faruq</em> dan kecerdasan keilmuan fiqih sang <em>Ummul Mu'minin</em> r.a.
                  </p>
                  <div class="content-grid-2" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">🗡️ Sahabat Umar bin Khattab Ra.</div>
                      <div class="card-desc">Gelar Al-Faruq (pembeda haq-bathil), ronda malam memanggul gandum untuk rakyat miskin, dan keberanian menegakkan hukum adil tanpa pandang bulu.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">📜 Sayyidah Aisyah Ra.</div>
                      <div class="card-desc">Gelar Al-Humaira, perawi ribuan hadits shahih, pakar ilmu faraidh & medis, serta teladan kezuhudan dan kedermawanan wanita muslimah.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Biografi & Kepribadian Umar bin Khattab Ra.",
                "badge": "SANG AL-FARUQ",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Umar bin Khattab ra. masuk Islam setelah mendengar adiknya Fatimah membaca surah Thaha. Masuk Islamnya Umar menjadi titik balik kejayaan dakwah hingga kaum muslimin berani shalat terang-terangan di Ka'bah. Nabi Saw. memberinya gelar <strong>Al-Faruq</strong> (pembeda kebenaran dan kebatilan).
                </p>
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Karisma Umar Ra. (HR. Al-Bukhari):</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Nabi Saw. bersabda: <em>"Demi Dzat yang jiwaku berada di tangan-Nya, tidaklah setan menjumpaimu mengambil suatu jalan, melainkan setan itu akan kabur mengambil jalan lain selain jalanmu!"</em>
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Gagasan Bersejarah:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Menetapkan awal Kalender Hijriyah dimulai dari peristiwa hijrah.</li>
                      <li>Mendirikan Baitul Mal, kantor pos, dan kepolisian pengaman kota.</li>
                      <li>Menginisiasi pengumpulan lembaran Al-Qur'an mushaf pertama.</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Keadilan & Kesederhanaan Khalifah Umar",
                "badge": "TELADAN PEMIMPIN",
                "content": """
                <div class="card-box card-box-accent" style="margin-bottom: 16px;">
                  <div class="card-title">Kisah Haru Memanggul Sendiri Karung Gandum:</div>
                  <div class="card-desc" style="font-size: 21pt; line-height: 1.6;">
                    Saat blusukan malam hari, Umar mendengar tangisan anak-anak kelaparan yang ibunya merebus batu demi menenangkan mereka. Mengetahui hal itu, Umar bergegas ke Baitul Mal dan memanggul sendiri karung gandum dan minyak di pundaknya. Ketika pembantunya (Aslam) ingin membawakan, Umar menjawab tegas: <em>"Apakah engkau mau memikul dosa pertanggungjawabanku di hari kiamat kelak?!"</em>
                  </div>
                </div>
                <div class="card-box">
                  <div class="card-title">Kezuhudan Seorang Penguasa Imperium Besar:</div>
                  <div class="card-desc" style="font-size: 21pt; line-height: 1.5;">
                    Meskipun menguasai Romawi dan Persia, jubah Umar memiliki belasan tambalan kain kasar, tidur beralaskan pelepah kurma di bawah pohon kurma, dan tak segan ditegur oleh rakyat biasa saat berkhotbah.
                  </div>
                </div>
                """
            },
            {
                "title": "Biografi & Kecerdasan Sayyidah Aisyah Ra.",
                "badge": "UMMUL MU'MININ",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Aisyah binti Abu Bakar Ash-Shiddiq ra. adalah istri Rasulullah Saw. yang paling cerdas, memiliki daya hafal tajam, dan pemahaman fiqih yang sangat mendalam. Nabi menggelarinya <em>Al-Humaira</em> (karena rona pipinya yang kemerahan).
                </p>
                <div class="content-grid-3">
                  <div class="card-box">
                    <div class="card-title">1. Rawi Hadits Terbesar</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Meriwayatkan lebih dari 2.210 hadits nabawi, terutama mengenai adab keluarga, shalat malam, dan etika privasi Rasulullah Saw.
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">2. Rujukan Fatwa Sahabat</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Abu Musa Al-Asy'ari ra. berkata: <em>"Tidaklah kami para sahabat menghadapi kesulitan hukum agama melainkan kami menanyakannya kepada Aisyah dan menemukan solusinya."</em>
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">3. Pembelaan Ilahiah</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Ketika difitnah oleh kaum munafik dalam peristiwa <em>Haditsul Ifki</em>, kesucian kehormatannya dibersihkan langsung oleh ayat Al-Qur'an (QS. An-Nur: 11-20).
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Kedermawanan & Kezuhudan Sayyidah Aisyah Ra.",
                "badge": "AKHLAK MULIA",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">Teladan Kedermawanan Luar Biasa:</div>
                  <div class="card-desc" style="font-size: 21pt; line-height: 1.6; margin-top: 10px;">
                    Suatu hari Sayyidah Aisyah ra. menerima kiriman uang 100.000 dirham dari keponakannya Abdullah bin Zubair. Beliau membagikan seluruh uang tersebut kepada kaum fakir miskin Madinah hingga tak tersisa sepeser pun.
                  </div>
                  <p style="font-size: 21pt; color: #fbcfe8; margin-top: 10px; line-height: 1.5;">
                    Ketika waktu berbuka puasa tiba, pelayannya berkata: <em>"Wahai Ummul Mu'minin, mengapa engkau tidak menyisakan satu dirham saja untuk membeli sepotong daging berbuka?"</em> Aisyah menjawab dengan tenang: <em>"Seandainya engkau tadi mengingatkanku, niscaya aku akan membelinya."</em> Beliau berbuka hanya dengan roti gandum kering dan zaitun!
                  </p>
                </div>
                """
            },
            {
                "title": "Tabel Komparasi Karakter Teladan Umar Ra. & Aisyah Ra.",
                "badge": "MATRIKS KETELADANAN",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th>Tokoh Sahabat</th>
                      <th>Gelar Kehormatan</th>
                      <th>Dimensi Keunggulan Karakter</th>
                      <th>Aplikasi bagi Siswa Remaja</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong style="color: #f472b6;">Umar bin Khattab Ra.</strong></td>
                      <td>Al-Faruq & Amirul Mukminin</td>
                      <td>Ketegasan memegang prinsip, keadilan tanpa pandang bulu, kepedulian sosial tinggi.</td>
                      <td>Berani menolak maksiat sebaya, jujur dalam ujian, membela teman tertindas.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #f472b6;">Sayyidah Aisyah Ra.</strong></td>
                      <td>Ummul Mu'minin & Al-Humaira</td>
                      <td>Kecerdasan intelektual, kepakaran sains & syariat, kezuhudan, dermawan.</td>
                      <td>Semangat menuntut ilmu tinggi, menjaga kesucian diri, giat bersedekah.</td>
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
                    Mengapa Khalifah Umar bin Khattab ra. bergegas memanggul sendiri karung gandum dari gudang Baitul Mal untuk diberikan kepada seorang ibu dan anak-anaknya yang kelaparan?
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Karena tidak ada pengawal yang bersedia membantunya malam itu</div>
                    <div class="quiz-opt" data-correct="true">B. Karena ia merasa sangat takut akan pertanggungjawaban hisabnya sebagai pemimpin di hadapan Allah Swt.</div>
                    <div class="quiz-opt" data-correct="false">C. Agar dipuji oleh masyarakat Madinah sebagai pemimpin dermawan</div>
                    <div class="quiz-opt" data-correct="false">D. Karena gandum tersebut merupakan harta milik pribadi keluarganya</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). Umar bin Khattab ra. memiliki rasa takut yang teramat tinggi kepada Allah (<em>Khauf</em>) dan menyadari bahwa setiap pemimpin akan dimintai pertanggungjawaban mutlak atas rakyat yang dipimpinnya.
                  </div>
                </div>
                """
            },
            {
                "title": "Refleksi Keteladanan Sahabat Nabi: Bab IV",
                "badge": "IKHTISAR BAB IV",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">🌟 Bintang Petunjuk Umat (HR. Al-Baihaqi):</div>
                  <p style="font-size: 22pt; line-height: 1.6; margin-top: 10px;">
                    <em>"Para sahabatku bagaikan bintang-gemintang di langit; dengan siapa pun di antara mereka engkau meneladani, niscaya engkau akan mendapatkan petunjuk jalan kebenaran."</em>
                  </p>
                  <div style="margin-top: 16px; font-size: 21pt; color: #f472b6;">
                    Tirulah keberanian dan kepedulian Umar dalam membela keadilan! Teladanilah kecerdasan dan kesucian Aisyah dalam menggapai mahkota ilmu dan kesalehan!
                  </div>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-5-iman-kepada-qadha-dan-qadar.html",
        "full_title": "BAB V: Beriman kepada Qadha' dan Qadar — Akidah Akhlak Kelas IX MTs",
        "chapter_label": "BAB V: Iman Qadha' & Qadar",
        "badge_text": "K9 • SEMESTER 2",
        "theme_color": "#6366f1",
        "theme_light": "#a5b4fc",
        "theme_subtle": "rgba(99, 102, 241, 0.16)",
        "badge_gradient": "#4f46e5, #6366f1",
        "radial_color": "#312e81",
        "slides": [
            {
                "title": "Beriman kepada Qadha' dan Qadar (Takdir Allah)",
                "badge": "PENGANTAR BAB V",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">⚖️🌌</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #a5b4fc; margin: 12px 0;">BAB V: IMAN KEPADA QADHA' & QADAR</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Rukun Iman keenam: Menghayati kebijaksanaan takdir ilahi, menyelaraskan ikhtiar dan doa, serta meraih ketenangan jiwa sejati.
                  </p>
                  <div class="content-grid-3" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">1. Hakikat Qadha & Qadar</div>
                      <div class="card-desc">Ketetapan azali Allah dalam ilmu-Nya dan perwujudan takdir sesuai ukuran hikmah-Nya.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">2. Mu'allaq & Mubram</div>
                      <div class="card-desc">Takdir yang terikat ikhtiar-doa manusia vs takdir paten yang tak dapat ditolak.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">3. Buah Ketenangan</div>
                      <div class="card-desc">Menghapus kesombongan saat berhasil dan mencegah keputusasaan saat gagal.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Pengertian dan Perbedaan Qadha' & Qadar",
                "badge": "HAKIKAT TAKDIR",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">1. Qadha' (الْقَضَاء)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Ketetapan, rencana, dan kehendak Allah Swt. tentang segala sesuatu pada zaman azali (sebelum segala makhluk diciptakan) yang tersimpan dalam Lauhul Mahfuzh.
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">2. Qadar / Takdir (الْقَدَر)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Perwujudan, pelaksanaan, atau realisasi ketetapan Allah atas makhluk-Nya dalam kenyataan hidup dengan kadar, ukuran, dan waktu tertentu.
                    </div>
                  </div>
                </div>
                <div class="arabic-box" style="margin-top: 14px;">
                  <div class="arabic-text">إِنَّا كُلَّ شَىْءٍ خَلَقْنَٰهُ بِقَدَرٍ</div>
                  <div class="arabic-trans">"Sesungguhnya Kami menciptakan segala sesuatu menurut ukuran (takdir)." (QS. Al-Qamar: 49)</div>
                </div>
                """
            },
            {
                "title": "Pembagian Takdir: Mu'allaq & Mubram",
                "badge": "KLASIFIKASI TAKDIR",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box card-box-accent">
                    <div class="card-title">1. Takdir Mu'allaq (تَقْدِير مُعَلَّق)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Ketetapan Allah yang masih digantungkan pada usaha sungguh-sungguh (*ikhtiar*) dan permohonan (*doa*) hamba-Nya.
                    </div>
                    <ul class="bullet-list" style="margin-top: 10px; font-size: 19pt;">
                      <li><strong>Kecerdasan:</strong> Tergantung pada ketekunan belajar siswa.</li>
                      <li><strong>Kesehatan:</strong> Terkait pola makan, olahraga, dan berobat.</li>
                      <li><strong>Kelapangan Rezeki:</strong> Terkait kerja keras dan silaturahmi.</li>
                    </ul>
                  </div>
                  <div class="card-box">
                    <div class="card-title">2. Takdir Mubram (تَقْدِير مُبْرَم)</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Ketetapan mutlak Allah yang sudah pasti terjadi dan tidak dapat diubah atau ditawar oleh ikhtiar manusia mana pun.
                    </div>
                    <ul class="bullet-list" style="margin-top: 10px; font-size: 19pt;">
                      <li><strong>Kematian (Ajal):</strong> Waktu dan tempat datangnya maut.</li>
                      <li><strong>Jenis Kelamin & Kelahiran:</strong> Lahir dari orang tua mana.</li>
                      <li><strong>Terjadinya Hari Kiamat:</strong> Akhir kehidupan semesta alam.</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Hubungan Segitiga: Ikhtiar, Doa, dan Tawakal",
                "badge": "MEKANISME TAKDIR",
                "content": """
                <div class="content-grid-3">
                  <div class="card-box">
                    <div class="card-title">1. Ikhtiar Maksimal</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Pintu pembuka hukum sebab-akibat (sunnatullah). Belajar tekun, berobat saat sakit, dan berikhtiar pantang bermalas-malasan.
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">2. Doa yang Tulus</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Senjata orang mukmin (*silahul mukmin*). Rasulullah Saw. bersabda: <em>"Tidak ada yang dapat menolak takdir kecuali doa."</em> (HR. At-Tirmidzi).
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">3. Tawakal & Ridha</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Menyerahkan hasil akhir kepada Allah. Apabila berhasil tidak ujub, apabila belum berhasil tidak menyalahkan takdir ilahi.
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Bahaya Paham Menyimpang: Jabariyah & Qadariyah",
                "badge": "LURUSKAN AKIDAH",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box" style="border-color: rgba(239, 68, 68, 0.4);">
                    <div class="card-title" style="color: #fca5a5;">Paham Jabariyah (Fatalisme Buta):</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Berpandangan bahwa manusia tidak memiliki kehendak sama sekali, ibarat wayang yang digerakkan dalang atau bulu yang diterbangkan angin. Menjadikan takdir alasan berbuat maksiat.
                    </div>
                  </div>
                  <div class="card-box" style="border-color: rgba(239, 68, 68, 0.4);">
                    <div class="card-title" style="color: #fca5a5;">Paham Qadariyah (Kebebasan Mutlak):</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Berpandangan bahwa manusia mandiri menentukan nasibnya sendiri tanpa campur tangan takdir dan kehendak Allah sama sekali. Sombong saat berhasil.
                    </div>
                  </div>
                </div>
                <div class="card-box card-box-accent" style="margin-top: 14px;">
                  <div class="card-title">Akidah Ahlus Sunnah wal Jama'ah (Wasathiyah):</div>
                  <div class="card-desc" style="font-size: 21pt;">
                    Manusia memiliki ikhtiar dan kehendak (*kasb*), namun kehendak manusia tetap berada di bawah kekuasaan dan takdir Allah Swt. (*Wa maa tasyaa'uuna illaa an yasyaa'allaah*).
                  </div>
                </div>
                """
            },
            {
                "title": "Hikmah Mengimani Qadha' dan Qadar",
                "badge": "BUAH KEIMANAN",
                "content": """
                <ul class="bullet-list">
                  <li class="bullet-item">
                    <span class="bullet-icon">✦</span>
                    <div><strong>Melatih Jiwa Sabar dan Tawakal:</strong> Tidak mudah depresi atau histeris saat mengalami musibah, karena menyadari semua telah tertulis dalam takdir Allah yang bijaksana.</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">✦</span>
                    <div><strong>Menjauhkan Diri dari Sifat Ujub dan Sombong:</strong> Tatkala meraih kesuksesan nilai tinggi atau kekayaan, ia sadar itu adalah karunia dan taufik Allah, bukan semata kepintarannya.</div>
                  </li>
                  <li class="bullet-item">
                    <span class="bullet-icon">✦</span>
                    <div><strong>Menumbuhkan Jiwa Pemberani dan Optimis:</strong> Yakin bahwa rezeki dan ajal sudah ditetapkan Allah, sehingga tidak takut menegakkan amar ma'ruf nahi munkar.</div>
                  </li>
                </ul>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab V",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    Seorang pasien menderita sakit tipus, lalu ia berobat ke dokter, meminum obat sesuai resep, beristirahat cukup, dan berdoa memohon kesembuhan hingga akhirnya sembuh. Kejadian kesembuhan pasien tersebut termasuk contoh dari...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Takdir Mubram karena kesehatan ditentukan langsung oleh takdir</div>
                    <div class="quiz-opt" data-correct="true">B. Takdir Mu'allaq karena terwujud melalui proses ikhtiar berobat dan berdoa</div>
                    <div class="quiz-opt" data-correct="false">C. Sihir pengobatan tradisional</div>
                    <div class="quiz-opt" data-correct="false">D. Keberuntungan semata tanpa campur tangan Allah</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). Kesembuhan yang diikhtiarkan dengan berobat dan pola hidup sehat adalah wujud nyata <em>Takdir Mu'allaq</em> (takdir yang melibatkan ikhtiar hamba).
                  </div>
                </div>
                """
            },
            {
                "title": "Refleksi Ketenangan Batin: Bab V",
                "badge": "IKHTISAR BAB V",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">🌸 Firman Allah Penenang Jiwa (QS. Al-Hadid: 22-23):</div>
                  <blockquote style="font-size: 21pt; font-style: italic; color: #c7d2fe; margin: 14px 0; padding-left: 20px; border-left: 4px solid #6366f1; line-height: 1.6;">
                    "Tiada suatu bencana pun yang menimpa di bumi dan (tidak pula) pada dirimu sendiri melainkan telah tertulis dalam kitab (Lauhul Mahfuzh) sebelum Kami menciptakannya... (agar) kamu tidak berputus asa terhadap apa yang luput darimu, dan tidak pula terlalu gembira (sombong) terhadap apa yang diberikan-Nya kepadamu."
                  </blockquote>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-6-menghindari-perilaku-menyimpang-remaja.html",
        "full_title": "BAB VI: Menghindari Perilaku Menyimpang Remaja — Akidah Akhlak Kelas IX MTs",
        "chapter_label": "BAB VI: Menghindari Perilaku Menyimpang Remaja",
        "badge_text": "K9 • SEMESTER 2",
        "theme_color": "#ef4444",
        "theme_light": "#fca5a5",
        "theme_subtle": "rgba(239, 68, 68, 0.16)",
        "badge_gradient": "#dc2626, #ef4444",
        "radial_color": "#7f1d1d",
        "slides": [
            {
                "title": "Menghindari Perilaku Menyimpang dalam Pergaulan Remaja",
                "badge": "PENGANTAR BAB VI",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">🚫🛡️</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #fca5a5; margin: 12px 0;">BAB VI: MENANGKAL PENYIMPANGAN REMAJA</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Membentengi diri generasi muda madrasah dari racun destruktif: <strong>Khamr, Judi, Pergaulan Bebas (Zina), Narkoba,</strong> dan <strong>Tawuran Pelajar</strong>.
                  </p>
                  <div class="content-grid-3" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">1. Khamr & Narkoba</div>
                      <div class="card-desc">Penghilang akal sehat, perusak syaraf otak, dan induk segala kejahatan kemaksiatan (*Ummul Khaba'its*).</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">2. Judi & Tawuran</div>
                      <div class="card-desc">Maysir/judi online penghancur masa depan ekonomi dan kekerasan fisik perenggut nyawa sia-sia.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">3. Pergaulan Bebas</div>
                      <div class="card-desc">Larangan mendekati zina, bahaya pacaran, menjaga pandangan mata, dan etika hijab syar'i.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Karakteristik Usia Remaja & Tantangannya",
                "badge": "FASE REMAJA",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Masa remaja (<em>marhalah al-muraahaqah</em>) adalah fase transisi peralihan dari masa kanak-kanak menuju dewasa (baligh). Ditandai dengan perkembangan fisik, gejolak emosi pencarian jati diri, dan pengaruh kuat lingkungan sebaya.
                </p>
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Tantangan Khas Remaja:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Rasa ingin tahu tinggi yang terkadang mencoba hal berbahaya.</li>
                      <li>Mudah terpengaruh tren sosial media dan tekanan teman sebaya (*peer pressure*).</li>
                      <li>Kecenderungan membangkang bila nasihat disampaikan secara kasar.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Tuntunan Islam Membina Masa Muda:</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Rasulullah Saw. menyebutkan salah satu dari 7 golongan yang mendapat naungan 'Arsy Allah di padang mahsyar adalah: <em>"Syabbun nasya'a fii 'ibaadatillah"</em> (Pemuda yang tumbuh dan menghabiskan masa mudanya dalam ketaatan beribadah kepada Allah!).
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Bahaya Khamr, Narkoba, dan Judi",
                "badge": "PERILAKU MERUSAK 1",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Allah Swt. secara tegas mengharamkan minuman keras, judi, dan perbuatan keji setan (QS. Al-Ma'idah [5]: 90):
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">يَٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوٓا۟ إِنَّمَا ٱلْخَمْرُ وَٱلْمَيْسِرُ وَٱلْأَنصَابُ وَٱلْأَزْلَٰمُ رِجْسٌ مِّنْ عَمَلِ ٱلشَّيْطَٰنِ فَٱجْتَنِبُوهُ لَعَلَّكُمْ تُفْلِحُونَ</div>
                  <div class="arabic-trans">"Wahai orang-orang yang beriman! Sesungguhnya minuman keras, berjudi, (berkurban untuk) berhala, dan mengundi nasib dengan anak panah, adalah perbuatan keji dan termasuk perbuatan setan. Maka jauhilah (perbuatan-perbuatan) itu agar kamu beruntung." (QS. Al-Ma'idah: 90)</div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Narkoba Sebagai Pembunuh Karakter:</div>
                  <div class="card-desc" style="font-size: 21pt;">
                    Narkoba (narkotika dan obat terlarang) hukumnya haram mutlak berdasarkan kaidah *Iskhar* (memabukkan) dan merusak jiwa raga. Menghancurkan cita-cita dan menjerumuskan pada kriminalitas.
                  </div>
                </div>
                """
            },
            {
                "title": "Larangan Mendekati Zina & Pergaulan Bebas",
                "badge": "PERILAKU MERUSAK 2",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Islam tidak hanya mengharamkan zina, melainkan mengharamkan seluruh pintu dan sarana yang dapat mengantarkan kepada perzinaan (QS. Al-Isra' [17]: 32):
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">وَلَا تَقْرَبُوا۟ ٱلزِّنَىٰٓ ۖ إِنَّهُۥ كَانَ فَٰحِشَةً وَسَآءَ سَبِيلًا</div>
                  <div class="arabic-trans">"Dan janganlah kamu mendekati zina; sesungguhnya zina itu adalah suatu perbuatan yang keji, dan suatu jalan yang buruk." (QS. Al-Isra': 32)</div>
                </div>
                <div class="content-grid-2" style="margin-top: 14px;">
                  <div class="card-box">
                    <div class="card-title">Pintu Mendekati Zina yang Wajib Dijauhi:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Budaya pacaran bebas dan berdua-duaan (*khalwat*).</li>
                      <li>Menonton video pornografi dan konten vulgar di internet.</li>
                      <li>Berpakaian ketat memperlihatkan lekuk tubuh atau membuka aurat.</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Benteng Syariat:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Menundukkan pandangan mata (*Ghadhdhul Bashar*).</li>
                      <li>Berpuasa sunnah Senin-Kamis untuk meredam syahwat.</li>
                      <li>Menjaga interaksi lawan jenis dalam koridor adab belajar.</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Tawuran Pelajar: Arogansi Bodoh yang Merenggut Nyawa",
                "badge": "PERILAKU MERUSAK 3",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">⚠️ Ancaman Keras Rasulullah Saw. bagi Pelaku Tawuran (HR. Al-Bukhari & Muslim):</div>
                  <blockquote style="font-size: 22pt; font-style: italic; color: #fecaca; margin: 14px 0; padding-left: 20px; border-left: 4px solid #ef4444; line-height: 1.6;">
                    "Apabila dua orang muslim saling berhadapan membawa pedang (senjata untuk saling membunuh), maka pembunuh dan yang dibunuh sama-sama berada di dalam neraka!"
                  </blockquote>
                  <p style="font-size: 21pt; color: #f1f5f9; line-height: 1.5;">
                    Para sahabat bertanya: <em>"Wahai Rasulullah, yang membunuh wajar disiksa, tetapi mengapa orang yang terbunuh juga masuk neraka?"</em> Nabi menjawab: <em>"Karena sesungguhnya ia pun sangat berambisi dan berusaha untuk membunuh saudaranya!"</em>
                  </p>
                </div>
                """
            },
            {
                "title": "Matriks Benteng Diri dari Godaan Menyimpang",
                "badge": "TABEL PREVENTIF",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th>Bentuk Penyimpangan</th>
                      <th>Dampak Buruk Dunia & Akhirat</th>
                      <th>Langkah Benteng Pencegahan</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong style="color: #fca5a5;">Khamr & Narkoba</strong></td>
                      <td>Kerusakan otak permanen, hilang akal, shalat ditolak 40 hari.</td>
                      <td>Tegas menolak rokok & miras, pilih kawan saleh di madrasah.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #fca5a5;">Judi / Slot Online</strong></td>
                      <td>Kecanduan mental, hutang menumpuk, mencuri uang ortu.</td>
                      <td>Hapus aplikasi game judi, cari rezeki halal dengan kerja keras.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #fca5a5;">Pergaulan Bebas</strong></td>
                      <td>Penyakit menular seksual, hamil luar nikah, masa depan suram.</td>
                      <td>Tundukkan pandangan (*ghaddul bashar*), jangan khalwat/pacaran.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #fca5a5;">Tawuran Pelajar</strong></td>
                      <td>Kematian sia-sia, cacat seumur hidup, pidana penjara.</td>
                      <td>Salurkan energi pada beladiri resmi, futsal, pramuka, dan PMR.</td>
                    </tr>
                  </tbody>
                </table>
                """
            },
            {
                "title": "Uji Pemahaman Formatif: Bab VI",
                "badge": "EVALUASI SISWA",
                "content": """
                <div class="quiz-container">
                  <div class="quiz-question">
                    Mengapa dalam Surah Al-Isra' ayat 32 Allah Swt. menggunakan redaksi <em>"Wa laa taqrabuz-zina"</em> (Dan janganlah kamu MENDEKATI zina), bukan sekadar melarang berbuat zina?
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Karena zina hanya dilarang bagi orang tua yang sudah berumah tangga</div>
                    <div class="quiz-opt" data-correct="true">B. Sebagai tindakan preventif (*saddudz-dzari'ah*), mengharamkan segala hal pengantar dan pemicu yang mengarahkan pada zina seperti pacaran dan khalwat</div>
                    <div class="quiz-opt" data-correct="false">C. Karena mendekati zina hukumnya makruh sedangkan berzina baru haram</div>
                    <div class="quiz-opt" data-correct="false">D. Agar manusia bebas berbuat apa saja asalkan tidak sampai berhubungan fisik</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). Larangan "mendekati" menunjukkan kaidah preventif syariat Islam yang menutup rapat seluruh pintu perantara (pandangan liar, khalwat, pacaran) demi melindungi kesucian kehormatan manusia.
                  </div>
                </div>
                """
            },
            {
                "title": "Refleksi Pemuda Idaman Surga: Bab VI",
                "badge": "IKHTISAR BAB VI",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">🛡️ Ikrar Remaja Muslim Berkualitas:</div>
                  <p style="font-size: 22pt; line-height: 1.6; margin-top: 10px;">
                    "Masa muda hanya datang sekali seumur hidup. Aku tolak narkoba, aku jauhi miras dan judi, aku jaga kehormatan dari pergaulan bebas, dan aku ukir prestasi untuk membanggakan orang tua serta mengharumkan agama Islam!"
                  </p>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-7-adab-berjalan-berpakaian-makan-minum.html",
        "full_title": "BAB VII: Adab Berjalan, Berpakaian, Makan, Minum — Akidah Akhlak Kelas IX MTs",
        "chapter_label": "BAB VII: Adab Berjalan, Berpakaian, Makan & Minum",
        "badge_text": "K9 • SEMESTER 2",
        "theme_color": "#14b8a6",
        "theme_light": "#5eead4",
        "theme_subtle": "rgba(20, 184, 166, 0.16)",
        "badge_gradient": "#0d9488, #14b8a6",
        "radial_color": "#134e4a",
        "slides": [
            {
                "title": "Adab Berjalan, Berpakaian, Makan, dan Minum",
                "badge": "PENGANTAR BAB VII",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">🚶👔🍲</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #5eead4; margin: 12px 0;">BAB VII: ADAB BERJALAN, PAKAIAN & KONSUMSI</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Keindahan tata krama syariat Islam yang mengatur gerak langkah, penampilan lahiriah bermartabat, serta etika hidangan makanan halal bergizi.
                  </p>
                  <div class="content-grid-3" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">1. Adab Berjalan</div>
                      <div class="card-desc">Langkah wajar, tenang, tidak sombong membenturkan kaki, dan santun menyapa orang.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">2. Adab Berpakaian</div>
                      <div class="card-desc">Menutup aurat syar'i, bersih rapi, tidak ketat/transparan, serta bebas dari sifat tabarruj.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">3. Makan & Minum</div>
                      <div class="card-desc">Halalan thayyiban, basmalah tangan kanan, duduk tenang, dan tidak berlebihan (*israf*).</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Adab Berjalan Menurut Tuntunan Islam",
                "badge": "LANGKAH BERADAB",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Cara seseorang berjalan mencerminkan karakter batiniahnya. Islam mengajarkan berjalan dengan wajar, tegap, namun senantiasa tawadhu' tanpa kesombongan (QS. Luqman [31]: 18-19):
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">وَلَا تَمْشِ فِى ٱلْأَرْضِ مَرَحًا ۖ إِنَّ ٱللَّهَ لَا يُحِبُّ كُلَّ مُخْتَالٍ فَخُورٍ ﴿١٨﴾ وَٱقْصِدْ فِى مَشْيِكَ وَٱغْضُضْ مِن صَوْتِكَ</div>
                  <div class="arabic-trans">"Dan janganlah engkau berjalan di bumi dengan angkuh; sesungguhnya Allah tidak menyukai orang-orang yang sombong lagi membanggakan diri. Dan sederhanakanlah langkahmu dan lunakkanlah suaramu..." (QS. Luqman: 18-19)</div>
                </div>
                """
            },
            {
                "title": "Adab Berpakaian Sesuai Syariat Islam",
                "badge": "BUSANA BERMARTABAT",
                "content": """
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Fungsi Utama Pakaian (QS. Al-A'raf: 26):</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li>Menutup aurat dari pandangan yang tidak halal.</li>
                      <li>Sebagai perhiasan (*zinah*) yang memperindah penampilan.</li>
                      <li>Pakaian terbaik adalah <strong>Pakaian Takwa</strong> (kesucian batin).</li>
                    </ul>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Kriteria Pakaian Syar'i:</div>
                    <ul class="bullet-list" style="font-size: 20pt;">
                      <li><strong>Bagi Laki-Laki:</strong> Menutup antara pusar hingga lutut, tidak memakai kain sutera murni atau perhiasan emas.</li>
                      <li><strong>Bagi Perempuan:</strong> Menutup seluruh tubuh kecuali wajah dan telapak tangan, longgar tidak membentuk lekuk tubuh, dan tidak transparan.</li>
                      <li>Tidak menyerupai pakaian lawan jenis (*tasyabbuh*).</li>
                    </ul>
                  </div>
                </div>
                """
            },
            {
                "title": "Adab Makan dan Minum Sesuai Sunnah Nabi",
                "badge": "ETIKA HIDANGAN",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Rasulullah Saw. menasihati Umar bin Abi Salamah ra. tentang tiga etika dasar makan (HR. Al-Bukhari & Muslim):
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">يَا غُلَامُ، سَمِّ اللَّهَ، وَكُلْ بِيَمِينِكَ، وَكُلْ مِمَّا يَلِيكَ</div>
                  <div class="arabic-trans">"Wahai anak muda! Sebutlah nama Allah (bacalah Bismillah), makanlah dengan tangan kananmu, dan makanlah makanan yang berada di dekatmu!"</div>
                </div>
                <div class="content-grid-3" style="margin-top: 14px;">
                  <div class="card-box">
                    <div class="card-title">1. Mencuci Tangan & Duduk</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Mencuci tangan sebelum makan, duduk sopan (tidak bersandar sombong atau makan sambil berdiri).
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">2. Tidak Mencela Makanan</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Nabi Saw. tidak pernah mencela hidangan makanan: bila suka beliau makan, bila tidak suka beliau tinggalkan tanpa menghina yang memasak.
                    </div>
                  </div>
                  <div class="card-box">
                    <div class="card-title">3. Prinsip Sepertiga</div>
                    <div class="card-desc" style="font-size: 20pt;">
                      Tidak makan kekenyangan: sepertiga lambung untuk makanan, sepertiga untuk air minum, dan sepertiga untuk bernafas.
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Adab Berinteraksi terhadap Lingkungan Hidup",
                "badge": "PELESTARIAN ALAM",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Manusia diciptakan sebagai khalifah di bumi untuk memelihara dan melestarikan alam, bukan merusaknya (QS. Al-A'raf [7]: 56):
                </p>
                <div class="arabic-box">
                  <div class="arabic-text">وَلَا تُفْسِدُوا۟ فِى ٱلْأَرْضِ بَعْدَ إِصْلَٰحِهَا وَٱدْعُوهُ خَوْفًا وَطَمَعًا ۚ إِنَّ رَحْمَتَ ٱللَّهِ قَرِيبٌ مِّنَ ٱلْمُحْسِنِينَ</div>
                  <div class="arabic-trans">"Dan janganlah kamu berbuat kerusakan di bumi setelah (diciptakan) dengan baik, dan berdoalah kepada-Nya dengan rasa takut dan penuh harap. Sesungguhnya rahmat Allah sangat dekat kepada orang-orang yang berbuat baik." (QS. Al-A'raf: 56)</div>
                </div>
                <div class="card-box" style="margin-top: 14px;">
                  <div class="card-title">Kasih Sayang Terhadap Satwa & Pohon:</div>
                  <div class="card-desc" style="font-size: 21pt;">
                    Nabi Saw. melarang menyiksa hewan atau mengurungnya tanpa makan, melarang menebang pohon sembarangan bahkan di medan pertempuran, serta menjanjikan sedekah bagi siapa yang menanam pohon yang buahnya dimakan manusia, burung, atau hewan liar.
                  </div>
                </div>
                """
            },
            {
                "title": "Tabel Ikhtisar Adab Ragam Keseharian",
                "badge": "PANDUAN PRAKTIS",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th>Aktivitas</th>
                      <th>Sunnah yang Dianjurkan</th>
                      <th>Larangan yang Dihindari</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong>Berjalan</strong></td>
                      <td>Tenang, tegap bersahaja, menyapa dengan salam.</td>
                      <td>Berjalan sombong, membusungkan dada, menghina orang lewat.</td>
                    </tr>
                    <tr>
                      <td><strong>Berpakaian</strong></td>
                      <td>Menutup aurat syar'i, rapi, mendahulukan bagian kanan.</td>
                      <td>Isbal sombong, pakaian ketat/transparan, tabarruj pamer aurat.</td>
                    </tr>
                    <tr>
                      <td><strong>Makan & Minum</strong></td>
                      <td>Basmalah, tangan kanan, posisi duduk, doa tahmid.</td>
                      <td>Makan berdiri tergesa, meniup hidangan panas, berlebihan (*israf*).</td>
                    </tr>
                    <tr>
                      <td><strong>Lingkungan</strong></td>
                      <td>Menanam pohon, memungut duri/sampah di jalanan.</td>
                      <td>Buang sampah di sungai, merusak tanaman, menyiksa binatang.</td>
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
                    Berdasarkan hadits Nabi Muhammad Saw., bagaimanakah sikap seorang muslim yang beradab apabila ia mendapati hidangan makanan yang disajikan tidak sesuai dengan selera lidahnya?
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Memarahinya dan membuang makanan tersebut ke tempat sampah</div>
                    <div class="quiz-opt" data-correct="false">B. Menceritakan keburukan rasa masakannya kepada tamu lain</div>
                    <div class="quiz-opt" data-correct="true">C. Tidak mencela makanan tersebut; jika berselera ia makan dan jika tidak suka ia meninggalkannya secara diam-diam</div>
                    <div class="quiz-opt" data-correct="false">D. Menuntut ganti rugi uang kepada pemilik warung atau tuan rumah</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (C). Dari Abu Hurairah ra.: <em>"Nabi Muhammad Saw. sekali-kali tidak pernah mencela makanan. Apabila beliau berselera beliau memakannya, dan apabila tidak suka beliau meninggalkannya tanpa mencela."</em> (HR. Al-Bukhari).
                  </div>
                </div>
                """
            },
            {
                "title": "Refleksi Pribadi Anggun & Beradab: Bab VII",
                "badge": "IKHTISAR BAB VII",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">🌸 Budi Pekerti Sempurna:</div>
                  <p style="font-size: 22pt; line-height: 1.6; margin-top: 10px;">
                    Islam bukan hanya ajaran shalat di mihrab musala, melainkan petunjuk komprehensif yang memancarkan pesona kesopanan di jalan raya, etika di meja makan, kerapian dalam berbusana, dan kelestarian cinta alam semesta!
                  </p>
                </div>
                """
            }
        ]
    },
    {
        "filename": "bab-8-keteladanan-utsman-bin-affan-dan-ali-bin-abi-thalib.html",
        "full_title": "BAB VIII: Keteladanan Sahabat Utsman bin Affan Ra. & Ali bin Abi Thalib Ra. — K9",
        "chapter_label": "BAB VIII: Utsman bin Affan & Ali bin Abi Thalib",
        "badge_text": "K9 • SEMESTER 2",
        "theme_color": "#eab308",
        "theme_light": "#fde047",
        "theme_subtle": "rgba(234, 179, 8, 0.16)",
        "badge_gradient": "#ca8a04, #eab308",
        "radial_color": "#713f12",
        "slides": [
            {
                "title": "Keteladanan Sahabat Utsman bin Affan Ra. & Ali bin Abi Thalib Ra.",
                "badge": "PENGANTAR BAB VIII",
                "content": """
                <div style="text-align: center; margin-top: 15px;">
                  <span style="font-size: 52pt;">👑📖🗡️</span>
                  <h1 style="font-size: 38pt; font-weight: 800; color: #fde047; margin: 12px 0;">BAB VIII: UTSMAN BIN AFFAN & ALI BIN ABI THALIB</h1>
                  <p style="font-size: 24pt; color: #e2e8f0; max-width: 1000px; margin: 0 auto; line-height: 1.5;">
                    Dua pilar agung Khulafaur Rasyidin: Sang pemilik dua cahaya (<em>Dzun Nurain</em>) yang dermawan dan pemalu, serta gerbang lautan ilmu (<em>Babul 'Ilm</em>) yang gagah perkasa.
                  </p>
                  <div class="content-grid-2" style="margin-top: 36px; text-align: left;">
                    <div class="card-box card-box-accent">
                      <div class="card-title">💎 Utsman bin Affan Ra.</div>
                      <div class="card-desc">Gelar Dzun Nurain, membeli sumur Rumah untuk umat, mendanai pasukan Usrah di Tabuk, kodifikasi Mushaf Utsmani, dan rasa malu yang dicintai malaikat.</div>
                    </div>
                    <div class="card-box card-box-accent">
                      <div class="card-title">⚔️ Ali bin Abi Thalib Ra.</div>
                      <div class="card-desc">Gelar Babul 'Ilm & Asadullah, menggantikan Rasulullah tidur di ranjang hijrah, pahlawan perang Khaibar, dan kecerdasan putusan hukum peradilan.</div>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Biografi & Kedermawanan Utsman bin Affan Ra.",
                "badge": "DZUN NURAIN",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Utsman bin Affan ra. dijuluki <strong>Dzun Nurain</strong> (pemilik dua cahaya) karena menikahi dua putri Rasulullah Saw., yaitu Ruqayyah dan setelah wafat menikahi Ummu Kultsum.
                </p>
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">1. Membeli Sumur Rumah:</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Saat Madinah dilanda krisis air bersih, sumur milik seorang Yahudi dijual dengan harga mencekik. Utsman membelinya dengan harga mahal dan mewakafkannya secara gratis untuk seluruh penduduk Madinah hingga kiamat.
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">2. Membiayai Pasukan Perang Tabuk:</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Menyumbangkan 950 ekor unta, 50 ekor kuda, dan 1.000 dinar emas tunai untuk membekali <em>Jaisyul 'Usrah</em> (pasukan kesukaran). Nabi Saw. bersabda: <em>"Tidak ada yang membahayakan Utsman setelah apa yang ia perbuat hari ini!"</em>
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Sifat Pemalu Utsman & Kodifikasi Mushaf Al-Qur'an",
                "badge": "JASA AKBAR UTSMAN",
                "content": """
                <div class="card-box card-box-accent" style="margin-bottom: 16px;">
                  <div class="card-title">Malaikat Pun Malu Kepada Utsman (HR. Muslim):</div>
                  <div class="card-desc" style="font-size: 21pt; line-height: 1.6;">
                    Rasulullah Saw. membetulkan pakaiannya saat Utsman masuk dan bersabda: <em>"Tidakkah aku merasa malu kepada seseorang yang malaikat pun merasa malu kepadanya?"</em> Utsman adalah pribadi yang sangat santun, lemah lembut, dan menjaga rasa malunya.
                  </div>
                </div>
                <div class="card-box">
                  <div class="card-title">Kodifikasi Mushaf Standar (Mushaf Utsmani):</div>
                  <div class="card-desc" style="font-size: 21pt; line-height: 1.5;">
                    Melihat perbedaan bacaan dialek Al-Qur'an yang memicu perselisihan di wilayah kekhalifahan yang meluas, Khalifah Utsman membentuk tim penghimpun di bawah Zaid bin Tsabit untuk menyatukan tulisan mushaf resmi (*Rasm Utsmani*) yang kini dibaca oleh seluruh umat Islam di dunia.
                  </div>
                </div>
                """
            },
            {
                "title": "Biografi & Keberanian Ali bin Abi Thalib Ra.",
                "badge": "SINGA ALLAH & BABUL 'ILM",
                "content": """
                <p style="font-size: 22pt; margin-bottom: 14px;">
                  Ali bin Abi Thalib Karramallahu Wajhah adalah sepupu sekaligus menantu Nabi Saw. yang menikahi Sayyidah Fatimah Az-Zahra. Ia adalah golongan anak-anak pertama yang memeluk Islam (*as-saabiquunal awwaluun*).
                </p>
                <div class="content-grid-2">
                  <div class="card-box">
                    <div class="card-title">Keberanian di Malam Hijrah:</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Dengan nyawa sebagai taruhan, Ali dengan tenang tidur di ranjang Rasulullah mengenakan selimut hijau beliau demi mengelabui para algojo kafir Quraisy yang mengepung rumah hendak membunuh Nabi.
                    </div>
                  </div>
                  <div class="card-box card-box-accent">
                    <div class="card-title">Pahlawan Benteng Khaibar:</div>
                    <div class="card-desc" style="font-size: 20pt; line-height: 1.5;">
                      Nabi Saw. menyerahkan panji komando perang: <em>"Besok akan kuserahkan bendera ini kepada seseorang yang mencintai Allah dan Rasul-Nya, serta dicintai oleh Allah dan Rasul-Nya."</em> Ali meruntuhkan pintu benteng Khaibar yang kokoh.
                    </div>
                  </div>
                </div>
                """
            },
            {
                "title": "Kecerdasan Keilmuan & Kebijaksanaan Ali Ra.",
                "badge": "GERBANG ILMU",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">Pintu Gerbang Kota Ilmu (HR. At-Tirmidzi):</div>
                  <blockquote style="font-size: 22pt; font-style: italic; color: #fef08a; margin: 14px 0; padding-left: 20px; border-left: 4px solid #eab308; line-height: 1.6;">
                    "Ana madiinatul 'ilmi wa 'Aliyyun baabuhaa" (Aku adalah kotanya ilmu dan Ali adalah pintu gerbangnya).
                  </blockquote>
                  <p style="font-size: 21pt; color: #f1f5f9; line-height: 1.5;">
                    Ali dikenal sangat cerdas dalam memecahkan sengketa rumit, menguasai tata bahasa Arab (beliau menginstruksikan Abul Aswad Ad-Du'ali meletakkan dasar kaidah ilmu Nahwu), serta hidup bersahaja memakan roti gandum kasar kendati menjabat sebagai Khalifah.
                  </p>
                </div>
                """
            },
            {
                "title": "Tabel Komparasi Keteladanan Utsman Ra. & Ali Ra.",
                "badge": "MATRIKS KETELADANAN",
                "content": """
                <table class="table-modern">
                  <thead>
                    <tr>
                      <th>Sahabat Nabi</th>
                      <th>Gelar Kemuliaan</th>
                      <th>Jasa Terbesar bagi Umat</th>
                      <th>Karakter Utama yang Diteladani</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><strong style="color: #fde047;">Utsman bin Affan Ra.</strong></td>
                      <td>Dzun Nurain</td>
                      <td>Kodifikasi Mushaf Utsmani, wakaf sumur Rumah, pembiayaan armada laut.</td>
                      <td>Kedermawanan harta (*al-jud*), rasa malu (*al-haya'*), kelembutan nurani.</td>
                    </tr>
                    <tr>
                      <td><strong style="color: #fde047;">Ali bin Abi Thalib Ra.</strong></td>
                      <td>Babul 'Ilm & Karramallahu Wajhah</td>
                      <td>Merintis kaidah ilmu Nahwu, keadilan fatwa hukum peradilan, keberanian jihad.</td>
                      <td>Keberanian bela kebenaran (*syaja'ah*), kecerdasan berpikir, kezuhudan hidup.</td>
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
                    Jasa monumental Khalifah Utsman bin Affan ra. yang dampaknya mempersatukan bacaan ayat suci Al-Qur'an bagi seluruh umat Islam di seluruh penjuru dunia hingga hari kiamat adalah...
                  </div>
                  <div class="quiz-options">
                    <div class="quiz-opt" data-correct="false">A. Membeli sumur Rumah dari tangan saudagar Yahudi</div>
                    <div class="quiz-opt" data-correct="true">B. Melakukan kodifikasi penyeragaman penulisan mushaf Al-Qur'an (Mushaf Utsmani)</div>
                    <div class="quiz-opt" data-correct="false">C. Menetapkan permulaan sistem kalender tahun Hijriyah</div>
                    <div class="quiz-opt" data-correct="false">D. Menaklukkan benteng pertahanan Khaibar</div>
                  </div>
                  <div class="quiz-feedback">
                    <strong>Kunci & Pembahasan:</strong> Benar (B). Penyeragaman dan pembukuan resmi mushaf Al-Qur'an yang dikirimkan ke berbagai wilayah metropolitan Islam dikenal sebagai <em>Mushaf Utsmani</em> yang menjadi acuan mushaf standar dunia Islam.
                  </div>
                </div>
                """
            },
            {
                "title": "Rangkuman Penutup: Mengibarkan Panji Sahabat",
                "badge": "IKHTISAR BAB VIII",
                "content": """
                <div class="card-box card-box-accent">
                  <div class="card-title">👑 Warisan Abadi Khulafaur Rasyidin:</div>
                  <p style="font-size: 22pt; line-height: 1.6; margin-top: 10px;">
                    Utsman mengajarkan bahwa kekayaan yang diridhai Allah adalah kekayaan yang disalurkan untuk wakaf dan kemaslahatan umat; sedangkan Ali mengajarkan bahwa kemuliaan sejati terletak pada mahkota ilmu dan keberanian moral menegakkan kebenaran.
                  </p>
                  <div style="margin-top: 16px; font-size: 21pt; color: #fde047;">
                    Selesaikan jenjang MTs dengan bekal akidah kokoh, keteladanan para sahabat, dan akhlakul karimah yang menghiasi setiap nafas kehidupanmu!
                  </div>
                </div>
                """
            }
        ]
    }
]

def build_k9():
    out_dir = "deck-akidah-akhlak-mts-k9"
    os.makedirs(out_dir, exist_ok=True)
    
    for ch in chapters_k9:
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
        print(f"Created K9: {filepath}")

    # Build index.html for K9
    build_k9_index(out_dir)

def build_k9_index(out_dir):
    cards_html = []
    
    chapter_metadata = [
        ("Bab I: Iman kepada Hari Akhir", "bab-1-iman-kepada-hari-akhir.html", "SEMESTER 1", "#fcd34d", "⏳", "Kiamat Sugra-Kubra, tanda-tanda hari akhir, Barzakh, Ba'ats, Mahsyar, Mizan, Shirath, Surga-Neraka."),
        ("Bab II: Akhlak Terpuji Diri Sendiri", "bab-2-akhlak-terpuji-diri-sendiri.html", "SEMESTER 1", "#34d399", "🧠", "Membangun pribadi unggul: Berilmu, Kerja Keras, Kreatif, Produktif, dan Inovatif penakluk masa depan."),
        ("Bab III: Adab Saudara, Teman & Tetangga", "bab-3-adab-kepada-saudara-teman-tetangga.html", "SEMESTER 1", "#38bdf8", "🏡", "Hak ukhuwah islami, memuliakan tetangga (3 hak syar'i), etika bergaul tanpa perundungan."),
        ("Bab IV: Umar bin Khattab & Sayyidah Aisyah", "bab-4-keteladanan-umar-bin-khattab-dan-sayyidah-aisyah.html", "SEMESTER 1", "#f472b6", "🗡️", "Ketegasan Al-Faruq memanggul gandum rakyat dan kecerdasan Ummul Mu'minin gudang hadits & fiqih."),
        ("Bab V: Iman Qadha' & Qadar", "bab-5-iman-kepada-qadha-dan-qadar.html", "SEMESTER 2", "#a5b4fc", "⚖️", "Takdir Mu'allaq & Mubram, integrasi ikhtiar-doa-tawakal, serta meluruskan Jabariyah-Qadariyah."),
        ("Bab VI: Menghindari Perilaku Menyimpang Remaja", "bab-6-menghindari-perilaku-menyimpang-remaja.html", "SEMESTER 2", "#fca5a5", "🚫", "Membentengi diri dari miras, judi online, narkoba, larangan mendekati zina, dan tawuran maut."),
        ("Bab VII: Adab Berjalan, Pakaian, Makan & Minum", "bab-7-adab-berjalan-berpakaian-makan-minum.html", "SEMESTER 2", "#5eead4", "🚶", "Etika langkah santun Luqman, busana syar'i penutup aurat, sunnah makan duduk, dan cinta alam."),
        ("Bab VIII: Utsman bin Affan & Ali bin Abi Thalib", "bab-8-keteladanan-utsman-bin-affan-dan-ali-bin-abi-thalib.html", "SEMESTER 2", "#fde047", "👑", "Kedermawanan Dzun Nurain kodifikasi mushaf dan kepahlawanan Babul 'Ilm pintu gerbang ilmu nabi.")
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
  <title>Slide Deck Akidah Akhlak MTs Kelas IX — KMA 183</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: radial-gradient(circle at 50% 10%, #1e1b4b 0%, #070d19 80%);
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
      background: linear-gradient(135deg, #6366f1, #a5b4fc);
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
      border-color: #a5b4fc;
      box-shadow: 0 20px 45px rgba(99, 102, 241, 0.25);
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
      background: #6366f1;
      color: #ffffff;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header class="header">
      <span class="badge-top">KEMENTERIAN AGAMA RI • KMA 183</span>
      <h1>Slide Deck Akidah Akhlak MTs Kelas IX</h1>
      <p class="subtitle">
        Modul Pembelajaran Multimedia Mandiri: 8 Bab Lengkap (Semester Ganjil & Genap) — Dark Mode Penuh, Tipografi 22pt+, Dilengkapi Dalil Al-Qur'an & Hadits Shahih, Tabel Analisis, dan Kuis Evaluasi Formatif.
      </p>
    </header>

    <main class="grid">
      {"".join(cards_html)}
    </main>

    <footer class="nav-cross">
      <h3>Akses Lintas Modul Deck Digital MTs</h3>
      <div class="nav-cross-links">
        <a href="../deck-akidah-akhlak-mts-k7/index.html" class="nav-cross-btn">📖 Akidah Akhlak Kelas VII</a>
        <a href="../deck-akidah-akhlak-mts-k8/index.html" class="nav-cross-btn">📖 Akidah Akhlak Kelas VIII</a>
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
    print(f"Created K9 Index: {os.path.join(out_dir, 'index.html')}")

if __name__ == "__main__":
    build_k9()
