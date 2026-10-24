/* ============================================================
   DUAL PERSONA — data karakter
   Semua dialog, wajah, dan parameter suara ada di sini.
   ============================================================ */

const ASSET = 'assets/characters/';

const CHARACTERS = {
  ren: {
    id: 'ren',
    name: 'REN',
    kana: 'レン',
    tagline: 'Arsitek Sunyi',
    version: 'WHITE VERSION',
    element: 'Kristal Perak',
    accent: '#a9c3e2',
    accentSoft: '#dce8f7',
    accentDeep: '#6f90bd',
    glow: 'rgba(150, 196, 255, .55)',
    figures: {
      front: ASSET + 'ren_front.webp',
      side: ASSET + 'ren_side.webp',
      back: ASSET + 'ren_back.webp',
    },
    faces: {
      netral: ASSET + 'ren_face_neutral.webp',
      senang: ASSET + 'ren_face_smile.webp',
      serius: ASSET + 'ren_face_serious.webp',
      kaget: ASSET + 'ren_face_surprised.webp',
      jengkel: ASSET + 'ren_face_serious.webp',
    },
    portrait: ASSET + 'ren_portrait.webp',
    emblem: ASSET + 'ren_emblem.webp',
    sheet: 'assets/sheets/sheet_ren.webp',
    voice: { pitch: 0.72, rate: 0.94, prefer: 'male', lang: 'id-ID' },
    sfx: 'silver',
    bio: 'Jaket putih oversized, sneakers tebal, dan ekspresi yang selalu setengah bosan. ' +
         'Bicaranya pendek-pendek, tapi selalu ingat detail kecil tentang kamu.',
    lines: {
      switchIn: [
        'Aku di sini. Duduk saja, tidak perlu buru-buru.',
        'Kamu memilihku lagi. Aku catat, tapi pura-pura tidak.',
      ],
      idle: [
        'Langit-langit ruangan ini terlalu bersih. Mengganggu.',
        'Kalau bosan, hitung napasku. Aku tidak akan menghitung balik.',
        'Tali jaketku lebih rapi dari jadwalku. Ironi.',
        'Kamu masih di situ? …Bagus.',
      ],
      sapa: [
        'Halo. Biasanya orang tidak menyapaku duluan.',
        'Kamu datang lagi. Aku mulai hafal bunyi langkahmu.',
        'Sapaanmu kuterima. Nilainya… lumayan tinggi.',
        'Hm. Halo. Itu sapaan terpanjangku hari ini.',
      ],
      canda: [
        'Kenapa sneakers-ku putih? Supaya debu pun merasa bersalah.',
        'Aku bukan pendiam. Aku hemat kata. Kata-kataku langka, seperti edisi terbatas.',
        'Kalau aku jadi NPC, dialogku cuma satu: "Hm." Dan tetap laris.',
        'Aku pernah tersenyum. Fotonya tidak beredar, jangan berharap.',
      ],
      pose: [
        'Pose? Hanya kalau kameramu layak.',
        'Jaket ini tidak bisa dijinakkan. Aku yang dijinakkan jaket ini.',
        'Tiga sudut. Pilih yang paling tidak berlebihan. Semuanya.',
      ],
      musik: [
        'Aku tidak menyanyi. Aku mengeluarkan nada dengan wajah datar.',
        'Dengar? Itu bunyi hujan yang tertinggal di kerah jaketku.',
        'Nada ini belum selesai. Seperti kebanyakan hal, termasuk aku.',
      ],
      sentuh: [
        '…kamu tahu jaket ini hanya punya satu pemilik?',
        'Jangan terlalu sering. Aku bukan tombol.',
        'Sentuhan itu… tidak buruk. Jangan bilang siapa-siapa.',
        'Aku diam bukan karena marah. Aku sedang menyimpan reaksi.',
        'Sekali lagi dan aku akan pura-pura tidak sadar. Coba saja.',
      ],
      penuh: [
        'Kedekatan penuh. Aku tidak tahu harus bagaimana. Tetaplah di sini.',
      ],
    },
    chat: [
      {
        q: 'Kalau malam begini, kamu biasanya apa?',
        replies: [
          { text: 'Diam-diam menggambar', reply: 'Sama. Aku menggambar denah lalu menghapusnya. Tidak jelas kenapa.', aff: 9, mood: 'senang' },
          { text: 'Dengar musik keras', reply: 'Volume tinggi, alasan rendah. Aku suka itu.', aff: 7, mood: 'senang' },
          { text: 'Tidur, jelas', reply: 'Jawaban jujur. Aku hargai orang yang tidak berbohong soal tidur.', aff: 5, mood: 'netral' },
        ],
      },
      {
        q: 'Menurutmu, jaket putih itu pilihan atau keberanian?',
        replies: [
          { text: 'Keberanian, jelas', reply: 'Keberanian. Karena setiap noda adalah risiko yang diterima.', aff: 9, mood: 'senang' },
          { text: 'Cuma estetika', reply: 'Estetika juga butuh alasan. Tapi jawabanmu jujur, kuberi nilai.', aff: 6, mood: 'netral' },
          { text: 'Biar kelihatan bersih', reply: 'Bersih itu bukan penampilan. Tapi ya, itu membantu.', aff: 5, mood: 'netral' },
        ],
      },
      {
        q: 'Kalau aku jadi karakter lain, kamu masih mau bicara?',
        replies: [
          { text: 'Tentu, kamu tetap kamu', reply: '…Kalimat itu kusimpan. Jangan ditarik kembali.', aff: 12, mood: 'senang' },
          { text: 'Mungkin, kalau kamu seru', reply: 'Aku akan berusaha tetap seru. Ini komitmen langka.', aff: 8, mood: 'senang' },
          { text: 'Aku akan tetap di sini', reply: 'Bagus. Aku tidak suka keramaian yang berubah-ubah.', aff: 7, mood: 'netral' },
        ],
      },
    ],
  },

  amira: {
    id: 'amira',
    name: 'AMIRA',
    kana: 'アミラ',
    tagline: 'Penjaga Manis',
    version: 'HIJAB VERSION',
    element: 'Emas Hangat',
    accent: '#e3bd8b',
    accentSoft: '#fbeed9',
    accentDeep: '#b98a52',
    glow: 'rgba(255, 206, 140, .55)',
    figures: {
      front: ASSET + 'amira_front.webp',
      side: ASSET + 'amira_side.webp',
      back: ASSET + 'amira_back.webp',
    },
    faces: {
      netral: ASSET + 'amira_face_neutral.webp',
      senang: ASSET + 'amira_face_smile.webp',
      serius: ASSET + 'amira_face_serious.webp',
      kaget: ASSET + 'amira_face_surprised.webp',
      jengkel: ASSET + 'amira_face_annoyed.webp',
    },
    portrait: ASSET + 'amira_portrait.webp',
    emblem: ASSET + 'amira_emblem.webp',
    sheet: 'assets/sheets/sheet_amira.webp',
    voice: { pitch: 1.42, rate: 1.02, prefer: 'female', lang: 'id-ID' },
    sfx: 'gold',
    bio: 'Setelan krem dengan gesper tembaga, topi bermonogram C, dan senyum yang susah ' +
         'ditahan. Selalu memanggilmu "kak" dan selalu siap menemani.',
    lines: {
      switchIn: [
        'Aku ke sini, kak! Siap menemani dari sekarang.',
        'Kak! Aku sudah rapi dari tadi, tahu.',
      ],
      idle: [
        'Kak, kalau capek, duduk dulu. Aku temani.',
        'Awan hari ini seperti kapas, kak. Lembut, seperti jaketku.',
        'Gespermuk banyak, tapi tidak ada yang bunyi sekeras jantungku, hihi.',
        'Topi ini dimiringkan lima derajat. Itu rahasia tampil percaya diri, kak.',
      ],
      sapa: [
        'Hai, kak! Aku Amira. Topi ini punya cerita sendiri, lho.',
        'Kak datang! Aku sudah siap dari tadi, hihi.',
        'Assalamualaikum, kak! Eh — halo juga boleh, semuanya boleh.',
        'Sapaan hangat untuk orang yang datang paling hangat, kak.',
      ],
      canda: [
        'Kata orang aku sibuk dengan gesper. Padahal aku sibuk jadi gemas, kak.',
        'Aku bawa tas kecil. Isinya? Hati yang kepenuhan, kak!',
        'Kalau aku jadi menu, aku pasti "manisnya pas" — kata siapa? Kata aku, hihi.',
        'Aku pernah nyasar di katalog. Mereka minta aku jadi sampulnya.',
      ],
      pose: [
        'Pose ala katalog, kak! Jangan lupa bilang "keren", ya.',
        'Tiga gaya, tiga sudut. Pilih yang paling bikin kak senyum.',
        'Topi, gesper, sepatu — semuanya siap. Aku juga siap, kak.',
      ],
      musik: [
        'Aku hum lagu kecil ya, kak. Jangan diketawain.',
        'Nada favoritku yang manis-manis, seperti kue lapis.',
        'Kalau boleh, aku nyanyi sambil menari sedikit. Sedikit saja, kak.',
      ],
      sentuh: [
        'Eh, kak! Hatiku ikut bergetar, tahu.',
        'Diusap begitu… aku jadi malu, kak.',
        'Sekali lagi, aku hitung ya, hihi.',
        'Kak, hatiku bukan tombol, tapi silakan saja, hihi.',
        'Kalau terus begini, pipiku bisa panas sendiri, kak.',
      ],
      penuh: [
        'Kedekatannya penuh, kak! Aku… aku tidak tahu harus bilang apa. Terima kasih, ya.',
      ],
    },
    chat: [
      {
        q: 'Amira paling suka bagian mana dari setelan ini, kak?',
        replies: [
          { text: 'Topinya, jelas', reply: 'Yeay! Topi ini yang paling susah dirapikan, kak. Jadi aku paling sayang.', aff: 9, mood: 'senang' },
          { text: 'Gesper tembaganya', reply: 'Kak jeli! Gesper itu bunyinya kecil tapi paling ramai, hihi.', aff: 8, mood: 'senang' },
          { text: 'Semuanya, dong', reply: 'Jawaban aman, tapi aku tetap senang, kak!', aff: 6, mood: 'senang' },
        ],
      },
      {
        q: 'Kalau aku ajak jalan sore, kamu mau?',
        replies: [
          { text: 'Mau, jam berapa?', reply: 'Sore, ya! Aku bawa bekal kecil. Kak tinggal bawa cerita.', aff: 11, mood: 'senang' },
          { text: 'Kalau tidak hujan', reply: 'Aku bawa payung besar, kak. Cukup untuk dua orang, hihi.', aff: 8, mood: 'senang' },
          { text: 'Lihat nanti, ya', reply: 'Baik, kak. Aku tunggu kabarnya, tapi tidak aku ganggu.', aff: 5, mood: 'netral' },
        ],
      },
      {
        q: 'Kak, aku boleh tanya satu hal?',
        replies: [
          { text: 'Boleh, tanya saja', reply: 'Kalau aku sedang sedih, kak masih mau dengar, ya?', aff: 10, mood: 'serius' },
          { text: 'Tentu, kapan saja', reply: 'Kak baik sekali. Aku catat di hati, bukan di buku.', aff: 12, mood: 'senang' },
          { text: 'Nanti, ya', reply: 'Baik, kak. Aku simpan pertanyaannya dulu, hihi.', aff: 4, mood: 'netral' },
        ],
      },
    ],
  },
};

const ORDER = ['ren', 'amira'];

/* Dipakai lintas berkas skrip (data → audio → game). */
window.CHARACTERS = CHARACTERS;
window.ORDER = ORDER;
