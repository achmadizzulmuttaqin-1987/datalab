#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to build standalone slide decks for:
- Akidah Akhlak MTs Kelas VIII (Bab 1 - 10 + index.html)
- Akidah Akhlak MTs Kelas IX (Bab 1 - 8 + index.html)
Curriculum: KMA 183 Tahun 2019 Kemenag RI
Design: Dark Mode, Min font size 22pt, Arabic 32pt, Responsive, Interactive Drawer & Quiz.
"""

import os
import json

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{full_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Scheherazade+New:wght@400;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-canvas: #070d19;
      --bg-card: #0f192c;
      --bg-card-subtle: #16243d;
      --text-main: #ffffff;
      --text-muted: #e2e8f0;
      --text-light: #cbd5e1;
      --primary: {theme_color};
      --primary-light: {theme_light};
      --primary-subtle: {theme_subtle};
      --accent: #facc15;
      --border-card: #273e66;
      --shadow-card: 0 25px 60px -10px rgba(0, 0, 0, 0.85);
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-arabic: 'Amiri', 'Scheherazade New', serif;
      --radius-card: 24px;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background: radial-gradient(circle at 50% 15%, {radial_color} 0%, var(--bg-canvas) 85%);
      color: var(--text-main);
      font-family: var(--font-sans);
      font-size: 22pt;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      user-select: none;
    }}

    .deck-topbar {{
      position: fixed;
      top: 0; left: 0; right: 0;
      height: 70px; padding: 0 32px;
      display: flex; align-items: center; justify-content: space-between;
      z-index: 100;
      background: rgba(7, 13, 25, 0.92);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.14);
      color: #ffffff;
    }}

    .brand-group {{ display: flex; align-items: center; gap: 16px; font-size: 20pt; font-weight: 700; }}
    .brand-badge {{
      background: linear-gradient(135deg, {badge_gradient});
      color: #041326; padding: 6px 16px; border-radius: 999px;
      font-size: 15pt; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px;
    }}
    .brand-title {{ color: #ffffff; font-weight: 700; }}

    .status-group {{ display: flex; align-items: center; gap: 18px; }}
    .slide-counter {{
      background: rgba(255, 255, 255, 0.08); padding: 8px 18px; border-radius: 12px;
      font-size: 17pt; font-weight: 700; color: var(--primary-light);
      border: 1px solid rgba(255, 255, 255, 0.12);
    }}
    .slide-current-title {{
      font-size: 17pt; font-weight: 600; color: #ffffff;
      max-width: 480px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }}

    .top-actions {{ display: flex; align-items: center; gap: 10px; }}
    .icon-btn {{
      background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.16);
      color: #ffffff; width: 44px; height: 44px; border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
      cursor: pointer; font-size: 18pt; transition: all 0.2s ease;
      text-decoration: none;
    }}
    .icon-btn:hover {{ background: var(--primary); color: #041326; transform: translateY(-2px); }}

    .deck-bottombar {{
      position: fixed;
      bottom: 0; left: 0; right: 0;
      height: 72px; padding: 0 32px;
      display: flex; align-items: center; justify-content: space-between;
      z-index: 100;
      background: rgba(7, 13, 25, 0.94);
      backdrop-filter: blur(14px);
      border-top: 1px solid rgba(255, 255, 255, 0.14);
    }}

    .nav-btn-group {{ display: flex; align-items: center; gap: 12px; }}
    .nav-btn {{
      background: #1e293b; color: #ffffff;
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 10px 22px; border-radius: 14px;
      font-size: 16pt; font-weight: 700; cursor: pointer;
      display: flex; align-items: center; gap: 8px; transition: all 0.2s ease;
    }}
    .nav-btn:hover:not(:disabled) {{ background: var(--primary); color: #041326; border-color: var(--primary); }}
    .nav-btn:disabled {{ opacity: 0.35; cursor: not-allowed; }}
    .nav-btn-primary {{ background: var(--primary); color: #041326; border-color: var(--primary); }}
    .nav-btn-primary:hover:not(:disabled) {{ background: var(--primary-light); }}

    .progress-container {{
      flex: 1; max-width: 520px; height: 10px;
      background: rgba(255, 255, 255, 0.1); border-radius: 999px;
      overflow: hidden; margin: 0 24px; position: relative;
    }}
    .progress-fill {{
      height: 100%; width: 0%;
      background: linear-gradient(90deg, {theme_color}, {theme_light});
      transition: width 0.3s ease;
    }}

    .shortcut-hint {{ font-size: 14pt; color: #94a3b8; display: flex; gap: 14px; }}
    .shortcut-hint kbd {{
      background: #1e293b; padding: 3px 8px; border-radius: 6px;
      border: 1px solid #334155; color: #e2e8f0; font-size: 12pt;
    }}

    .slide-viewport {{
      width: 100vw; height: 100vh;
      display: flex; align-items: center; justify-content: center;
      padding: 85px 32px;
    }}

    .slide-stage {{
      width: 100%; max-width: 1420px; height: 100%; max-height: 840px;
      position: relative; perspective: 1200px;
    }}

    .slide {{
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      background: var(--bg-card);
      border: 1px solid var(--border-card);
      border-radius: var(--radius-card);
      box-shadow: var(--shadow-card);
      padding: 44px 56px;
      display: flex; flex-direction: column; justify-content: flex-start;
      opacity: 0; visibility: hidden; pointer-events: none;
      transform: translateY(20px) scale(0.98);
      transition: opacity 0.35s ease, transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.35s;
      overflow-y: auto;
    }}

    .slide.active {{
      opacity: 1; visibility: visible; pointer-events: auto;
      transform: translateY(0) scale(1);
    }}

    .slide-header {{
      display: flex; align-items: center; justify-content: space-between;
      border-bottom: 2px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 16px; margin-bottom: 24px;
    }}
    .slide-topic-badge {{
      display: inline-flex; align-items: center; gap: 8px;
      background: var(--primary-subtle); color: var(--primary-light);
      padding: 6px 16px; border-radius: 999px;
      font-size: 15pt; font-weight: 700; letter-spacing: 0.5px;
    }}
    .slide-title {{
      font-size: 32pt; font-weight: 800; color: #ffffff;
      line-height: 1.25; margin-top: 6px;
    }}
    .slide-subtitle {{ font-size: 20pt; color: #cbd5e1; margin-top: 4px; }}

    .arabic-box {{
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(250, 204, 21, 0.35);
      border-left: 6px solid var(--accent);
      padding: 22px 28px; border-radius: 16px;
      margin: 18px 0; text-align: right;
    }}
    .arabic-text {{
      font-family: var(--font-arabic);
      font-size: 32pt; line-height: 1.8;
      color: #fef08a; font-weight: 700;
      direction: rtl;
    }}
    .arabic-trans {{
      font-size: 20pt; font-style: italic; color: #e2e8f0;
      margin-top: 10px; line-height: 1.5; text-align: left;
    }}

    .content-grid-2 {{
      display: grid; grid-template-columns: 1fr 1fr;
      gap: 24px; align-items: stretch; margin-top: 10px;
    }}
    .content-grid-3 {{
      display: grid; grid-template-columns: repeat(3, 1fr);
      gap: 20px; align-items: stretch; margin-top: 10px;
    }}
    .content-grid-4 {{
      display: grid; grid-template-columns: repeat(4, 1fr);
      gap: 16px; align-items: stretch; margin-top: 10px;
    }}

    .card-box {{
      background: var(--bg-card-subtle);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 18px; padding: 24px 26px;
      display: flex; flex-direction: column; justify-content: flex-start;
      gap: 12px;
    }}
    .card-box-accent {{
      border-color: rgba(56, 189, 248, 0.4);
      background: linear-gradient(145deg, #112240, #152c52);
    }}
    .card-title {{
      font-size: 23pt; font-weight: 800; color: var(--primary-light);
      display: flex; align-items: center; gap: 10px;
    }}
    .card-desc {{
      font-size: 21pt; color: #f1f5f9; line-height: 1.5;
    }}

    .bullet-list {{
      list-style: none; display: flex; flex-direction: column; gap: 14px; margin-top: 8px;
    }}
    .bullet-item {{
      display: flex; align-items: flex-start; gap: 14px;
      font-size: 21pt; line-height: 1.45; color: #f8fafc;
    }}
    .bullet-icon {{
      background: var(--primary-subtle); color: var(--primary-light);
      min-width: 32px; height: 32px; border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
      font-size: 16pt; font-weight: 800; margin-top: 4px;
    }}

    .table-modern {{
      width: 100%; border-collapse: collapse; margin-top: 14px;
      background: rgba(15, 23, 42, 0.6); border-radius: 14px; overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.12);
    }}
    .table-modern th {{
      background: #1e293b; color: var(--primary-light);
      padding: 14px 18px; text-align: left; font-size: 21pt; font-weight: 800;
      border-bottom: 2px solid rgba(255, 255, 255, 0.15);
    }}
    .table-modern td {{
      padding: 14px 18px; font-size: 20pt; color: #f1f5f9;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08); vertical-align: top;
    }}
    .table-modern tr:last-child td {{ border-bottom: none; }}
    .table-modern tr:nth-child(even) {{ background: rgba(255, 255, 255, 0.02); }}

    .quiz-container {{ display: flex; flex-direction: column; gap: 16px; margin-top: 10px; }}
    .quiz-question {{
      font-size: 23pt; font-weight: 700; color: #ffffff;
      background: rgba(255, 255, 255, 0.05); padding: 18px 24px; border-radius: 14px;
      border-left: 5px solid var(--accent);
    }}
    .quiz-options {{ display: flex; flex-direction: column; gap: 10px; }}
    .quiz-opt {{
      background: #16243d; border: 1px solid rgba(255, 255, 255, 0.14);
      padding: 14px 20px; border-radius: 12px; cursor: pointer;
      display: flex; align-items: center; gap: 14px;
      font-size: 21pt; color: #f1f5f9; transition: all 0.2s ease;
    }}
    .quiz-opt:hover {{ background: #1e3357; border-color: var(--primary-light); }}
    .quiz-opt.correct {{ background: #064e3b !important; border-color: #10b981 !important; color: #a7f3d0 !important; }}
    .quiz-opt.wrong {{ background: #7f1d1d !important; border-color: #ef4444 !important; color: #fecaca !important; }}
    .quiz-feedback {{
      display: none; padding: 14px 18px; border-radius: 12px;
      font-size: 20pt; line-height: 1.5; margin-top: 6px;
    }}
    .quiz-feedback.show {{ display: block; }}
    .quiz-feedback.correct-fb {{ background: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; color: #ecfdf5; }}
    .quiz-feedback.wrong-fb {{ background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #fff1f2; }}

    .drawer-overlay {{
      position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(0, 0, 0, 0.75); backdrop-filter: blur(8px);
      z-index: 200; opacity: 0; visibility: hidden; transition: all 0.25s ease;
      display: flex; justify-content: flex-end;
    }}
    .drawer-overlay.open {{ opacity: 1; visibility: visible; }}
    .drawer-panel {{
      width: 440px; height: 100%; background: #0c1524;
      border-left: 1px solid rgba(255, 255, 255, 0.16);
      display: flex; flex-direction: column; padding: 24px 28px;
      transform: translateX(100%); transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: -15px 0 40px rgba(0, 0, 0, 0.8);
    }}
    .drawer-overlay.open .drawer-panel {{ transform: translateX(0); }}
    .drawer-header {{
      display: flex; align-items: center; justify-content: space-between;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12); padding-bottom: 16px; margin-bottom: 20px;
    }}
    .drawer-title {{ font-size: 22pt; font-weight: 800; color: #ffffff; }}
    .drawer-close {{
      background: transparent; border: none; color: #94a3b8; font-size: 24pt;
      cursor: pointer; line-height: 1;
    }}
    .drawer-close:hover {{ color: #ffffff; }}
    .drawer-list {{
      display: flex; flex-direction: column; gap: 10px; overflow-y: auto; flex: 1;
    }}
    .drawer-item {{
      background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.08);
      padding: 12px 16px; border-radius: 12px; cursor: pointer;
      display: flex; align-items: center; gap: 12px; font-size: 18pt;
      color: #e2e8f0; transition: all 0.15s ease;
    }}
    .drawer-item:hover {{ background: rgba(56, 189, 248, 0.15); border-color: var(--primary); }}
    .drawer-item.active {{ background: var(--primary); color: #041326; font-weight: 700; }}

    @media print {{
      body {{ overflow: visible; background: #000000; color: #ffffff; }}
      .deck-topbar, .deck-bottombar, .drawer-overlay {{ display: none !important; }}
      .slide-viewport {{ padding: 0; width: 100%; height: auto; }}
      .slide-stage {{ max-height: none; height: auto; }}
      .slide {{
        position: relative !important; opacity: 1 !important; visibility: visible !important;
        page-break-after: always; transform: none !important; margin-bottom: 40px;
      }}
    }}
  </style>
</head>
<body>

  <!-- TOP BAR -->
  <header class="deck-topbar">
    <div class="brand-group">
      <span class="brand-badge">{badge_text}</span>
      <span class="brand-title">{chapter_label}</span>
    </div>
    <div class="status-group">
      <div class="slide-counter" id="slide-counter">Slide 01 / {total_slides_pad}</div>
      <div class="slide-current-title" id="slide-current-title">{first_slide_title}</div>
    </div>
    <div class="top-actions">
      <button class="icon-btn" id="btn-drawer" title="Daftar Slide (M)">📑</button>
      <button class="icon-btn" id="btn-fullscreen" title="Layar Penuh (F)">⛶</button>
      <button class="icon-btn" id="btn-print" title="Cetak / Simpan PDF">🖨️</button>
      <a href="index.html" class="icon-btn" title="Kembali ke Beranda">🏠</a>
    </div>
  </header>

  <!-- VIEWPORT & SLIDES -->
  <main class="slide-viewport">
    <div class="slide-stage" id="slide-stage">
      {slides_html}
    </div>
  </main>

  <!-- BOTTOM BAR -->
  <footer class="deck-bottombar">
    <div class="nav-btn-group">
      <button class="nav-btn" id="btn-first" title="Slide Pertama (Home)">⏮ Awal</button>
      <button class="nav-btn" id="btn-prev" title="Slide Sebelumnya (Panah Kiri)">◀ Sebelumnya</button>
    </div>

    <div class="progress-container">
      <div class="progress-fill" id="progress-fill"></div>
    </div>

    <div class="nav-btn-group">
      <button class="nav-btn nav-btn-primary" id="btn-next" title="Slide Selanjutnya (Panah Kanan)">Selanjutnya ▶</button>
      <button class="nav-btn" id="btn-last" title="Slide Terakhir (End)">Akhir ⏭</button>
    </div>
  </footer>

  <!-- DRAWER OVERLAY -->
  <aside class="drawer-overlay" id="drawer-overlay">
    <div class="drawer-panel">
      <div class="drawer-header">
        <h3 class="drawer-title">Daftar Slide Bab</h3>
        <button class="drawer-close" id="btn-close-drawer">&times;</button>
      </div>
      <div class="drawer-list" id="drawer-grid">
        {drawer_items_html}
      </div>
    </div>
  </aside>

  <script>
    (function () {{
      const slides = Array.from(document.querySelectorAll('.slide'));
      const totalSlides = slides.length;
      let currentIndex = 0;

      const slideCounterDisplay = document.getElementById('slide-counter');
      const slideTitleDisplay = document.getElementById('slide-current-title');
      const progressFill = document.getElementById('progress-fill');
      const btnPrev = document.getElementById('btn-prev');
      const btnNext = document.getElementById('btn-next');
      const btnFirst = document.getElementById('btn-first');
      const btnLast = document.getElementById('btn-last');
      const btnDrawer = document.getElementById('btn-drawer');
      const btnCloseDrawer = document.getElementById('btn-close-drawer');
      const drawerOverlay = document.getElementById('drawer-overlay');
      const drawerGrid = document.getElementById('drawer-grid');
      const btnFullscreen = document.getElementById('btn-fullscreen');
      const btnPrint = document.getElementById('btn-print');

      function updateSlide(newIndex) {{
        if (newIndex < 0 || newIndex >= totalSlides) return;
        slides[currentIndex].classList.remove('active');
        slides[newIndex].classList.add('active');
        currentIndex = newIndex;

        const currNum = String(currentIndex + 1).padStart(2, '0');
        const totalNum = String(totalSlides).padStart(2, '0');
        slideCounterDisplay.textContent = `Slide ${{currNum}} / ${{totalNum}}`;
        slideTitleDisplay.textContent = slides[currentIndex].dataset.title || `Slide ${{currNum}}`;

        const pct = ((currentIndex + 1) / totalSlides) * 100;
        progressFill.style.width = pct + '%';

        btnPrev.disabled = currentIndex === 0;
        btnNext.disabled = currentIndex === totalSlides - 1;

        const drawerItems = drawerGrid.querySelectorAll('.drawer-item');
        drawerItems.forEach((dItem, idx) => {{
          dItem.classList.toggle('active', idx === currentIndex);
        }});
      }}

      function goToSlide(index) {{ updateSlide(index); }}
      function nextSlide() {{ if (currentIndex < totalSlides - 1) updateSlide(currentIndex + 1); }}
      function prevSlide() {{ if (currentIndex > 0) updateSlide(currentIndex - 1); }}
      function openDrawer() {{ drawerOverlay.classList.add('open'); }}
      function closeDrawer() {{ drawerOverlay.classList.remove('open'); }}

      btnNext.addEventListener('click', nextSlide);
      btnPrev.addEventListener('click', prevSlide);
      btnFirst.addEventListener('click', () => goToSlide(0));
      btnLast.addEventListener('click', () => goToSlide(totalSlides - 1));

      btnDrawer.addEventListener('click', openDrawer);
      btnCloseDrawer.addEventListener('click', closeDrawer);
      drawerOverlay.addEventListener('click', (e) => {{
        if (e.target === drawerOverlay) closeDrawer();
      }});

      window.addEventListener('keydown', (e) => {{
        if (drawerOverlay.classList.contains('open')) {{
          if (e.key === 'Escape') closeDrawer();
          return;
        }}
        if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
          e.preventDefault(); nextSlide();
        }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp' || e.key === 'Backspace') {{
          e.preventDefault(); prevSlide();
        }} else if (e.key === 'Home') {{
          e.preventDefault(); goToSlide(0);
        }} else if (e.key === 'End') {{
          e.preventDefault(); goToSlide(totalSlides - 1);
        }} else if (e.key === 'f' || e.key === 'F') {{
          toggleFullscreen();
        }} else if (e.key === 'm' || e.key === 'M') {{
          openDrawer();
        }}
      }});

      let touchStartX = 0, touchEndX = 0;
      const stage = document.getElementById('slide-stage');
      stage.addEventListener('touchstart', (e) => {{ touchStartX = e.changedTouches[0].screenX; }}, {{ passive: true }});
      stage.addEventListener('touchend', (e) => {{
        touchEndX = e.changedTouches[0].screenX;
        const threshold = 50;
        if (touchEndX < touchStartX - threshold) nextSlide();
        else if (touchEndX > touchStartX + threshold) prevSlide();
      }}, {{ passive: true }});

      function toggleFullscreen() {{
        if (!document.fullscreenElement) {{
          document.documentElement.requestFullscreen().catch(() => {{}});
        }} else {{
          document.exitFullscreen().catch(() => {{}});
        }}
      }}
      btnFullscreen.addEventListener('click', toggleFullscreen);
      btnPrint.addEventListener('click', () => {{ window.print(); }});

      // Handle interactive quiz options
      document.querySelectorAll('.quiz-container').forEach(container => {{
        const options = container.querySelectorAll('.quiz-opt');
        const feedback = container.querySelector('.quiz-feedback');
        options.forEach(opt => {{
          opt.addEventListener('click', () => {{
            const isCorrect = opt.dataset.correct === 'true';
            options.forEach(o => {{
              o.style.pointerEvents = 'none';
              if (o.dataset.correct === 'true') o.classList.add('correct');
              else if (o === opt) o.classList.add('wrong');
            }});
            if (feedback) {{
              feedback.classList.add('show');
              feedback.classList.add(isCorrect ? 'correct-fb' : 'wrong-fb');
            }}
          }});
        }});
      }});

      // Drawer navigation click
      document.querySelectorAll('.drawer-item').forEach((item, idx) => {{
        item.addEventListener('click', () => {{
          goToSlide(idx);
          closeDrawer();
        }});
      }});

      updateSlide(0);
    }})();
  </script>
</body>
</html>
"""

print("Template ready.")
