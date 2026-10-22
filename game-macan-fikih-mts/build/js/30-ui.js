/* =====================================================================
   30 · Mulai aplikasi & jembatan UI terakhir
   ===================================================================== */
function toggleFullscreen() {
  const d = document.documentElement;
  try {
    if (!document.fullscreenElement) {
      if (d.requestFullscreen) d.requestFullscreen().catch(() => {});
    } else if (document.exitFullscreen) {
      document.exitFullscreen();
    }
  } catch (e) { /* tidak didukung */ }
  AudioFX.click();
}

function boot() {
  initGameFlow();
  document.body.classList.add('intro-open');
  document.body.classList.remove('modal-open');
  $('#intro').classList.remove('hidden');
  $('#quiz').classList.add('hidden');
  $('#result').classList.add('hidden');
  $('#review').classList.add('hidden');
  $('#map').classList.add('hidden');
  $('#settings').classList.add('hidden');
  $('#finale').classList.add('hidden');
  if (!document.fullscreenEnabled) $('#btn-full').style.display = 'none';
  if (!state.sound) {
    $('#sound-icon').setAttribute('href', '#i-mute');
    $('#btn-sound').classList.remove('on');
  }

  const fill = $('#load-fill');
  if (fill) fill.style.width = '18%';

  setTimeout(() => {
    if (fill) fill.style.width = '52%';
    let ok = false;
    try {
      ok = startWorld();
    } catch (e) {
      console.error('Dunia 3D gagal dimulai:', e);
      $('#stage').classList.add('no-webgl');
      WORLD.ok = false;
    }
    if (fill) fill.style.width = '100%';
    setTimeout(() => {
      const loader = $('#scene-loader');
      if (loader) {
        loader.classList.add('done');
        setTimeout(() => loader.remove(), 700);
      }
      if (!ok) {
        showToast('Mode 3D tidak tersedia. Kamu tetap bisa memainkan seluruh soal.', 4200);
      }
      // Sapa pemain baru sekali
      try {
        if (!localStorage.getItem('jejak-cilik-sapa')) {
          localStorage.setItem('jejak-cilik-sapa', '1');
          setTimeout(() => {
            showToast('Tips: buka <b>Pengaturan</b> untuk mencoba 4 tampilan Cilik dan 4 suasana bukit.', 4600);
          }, 1600);
        }
      } catch (e) {}
    }, 420);
  }, 90);

  // Ekspos untuk pengujian & pratinjau otomatis
  window.__CILIK = {
    WORLD, CAM, state, CAVES, BABS, SKINS, BIOMES, TIGER_ANIM,
    beginAdventure, travelTo, openQuiz, chooseAnswer, nextQuestion, closeQuiz,
    openMap, openSettings, startFinale, applyStyle, applyBiome, placeTigerAt, snapCamera, overviewGoal,
    getSession: () => session,
    getTravel: () => travelAnim,
    getStars: () => totalStars(),
  };

  // Simpan ketika tab disembunyikan/ditutup
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') saveNow();
  });
  window.addEventListener('beforeunload', saveNow);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}
