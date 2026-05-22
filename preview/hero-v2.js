/*  Hero v2 — scroll-driven video scrubbing (cross-browser robust)
    Strategy:
    1. Force video to autoplay muted (allowed everywhere)
    2. Intercept EVERY play() and immediately pause — keeps it paused
    3. Try to set currentTime every animation frame; ignore failures
    4. Smoothly lerp the displayed time toward the scroll-target
*/
(function () {
  'use strict';

  function init() {
    const hero = document.getElementById('heroV2');
    const video = document.getElementById('heroV2Video');
    const progressEl = document.getElementById('heroV2Progress');
    const cueEl = document.getElementById('heroV2Cue');
    if (!hero || !video) return;

    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) return;

    // ── Progress dots ──
    const STEPS = 4;
    if (progressEl && !progressEl.children.length) {
      for (let i = 0; i < STEPS; i++) {
        const dot = document.createElement('button');
        dot.className = 'hero-v2-progress-dot' + (i === 0 ? ' active' : '');
        dot.dataset.step = i;
        dot.setAttribute('aria-label', 'Jump to step ' + (i + 1));
        dot.addEventListener('click', () => {
          const heroTop = hero.offsetTop;
          const heroH = hero.offsetHeight - window.innerHeight;
          const target = heroTop + (heroH * (i / (STEPS - 1)));
          window.scrollTo({ top: target, behavior: 'smooth' });
        });
        progressEl.appendChild(dot);
      }
    }

    // ── INTERCEPT PLAY: keep the video paused at all times ──
    // We need play() to be called at least once so the browser warms the
    // decoder, but then we want it paused so currentTime seeking works.
    video.addEventListener('play', () => {
      // Let it actually render 1 frame, then pause
      requestAnimationFrame(() => requestAnimationFrame(() => {
        try { video.pause(); } catch (e) {}
      }));
    });

    // Try to play (muted) so the decoder warms up — fine if it fails
    const tryPlay = () => {
      const p = video.play();
      if (p && p.catch) p.catch(() => {});
    };
    if (video.readyState >= 2) tryPlay();
    else video.addEventListener('loadeddata', tryPlay, { once: true });
    // Fallback: if autoplay was blocked, prime on first user interaction
    const firstInteract = () => {
      tryPlay();
      ['scroll', 'click', 'touchstart', 'wheel', 'keydown'].forEach((ev) =>
        window.removeEventListener(ev, firstInteract));
    };
    ['scroll', 'click', 'touchstart', 'wheel', 'keydown'].forEach((ev) =>
      window.addEventListener(ev, firstInteract, { once: true, passive: true }));

    // ── SCROLL → target time ──
    let targetTime = 0;
    let displayTime = 0;

    function computePct() {
      const heroTop = hero.offsetTop;
      const heroH = hero.offsetHeight - window.innerHeight;
      let pct = (window.scrollY - heroTop) / heroH;
      return Math.max(0, Math.min(1, pct));
    }

    function onScroll() {
      const pct = computePct();
      if (video.duration && !isNaN(video.duration) && video.duration > 0) {
        targetTime = pct * video.duration;
      }
      if (progressEl) {
        const step = Math.min(STEPS - 1, Math.floor(pct * STEPS));
        progressEl.querySelectorAll('.hero-v2-progress-dot').forEach((d, i) => {
          d.classList.toggle('active', i === step);
        });
      }
      if (cueEl) cueEl.style.opacity = pct > 0.04 ? '0' : '';
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);

    // ── rAF: try to seek every frame, ignore failures silently ──
    function tick() {
      if (video.duration && !isNaN(video.duration)) {
        const diff = targetTime - displayTime;
        if (Math.abs(diff) > 0.01) {
          displayTime += diff * 0.18; // smoothing factor (Apple-style)
          try {
            // Pause if it's still playing somehow
            if (!video.paused) video.pause();
            video.currentTime = displayTime;
          } catch (e) {
            // swallow — try again next frame
          }
        }
      }
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);

    onScroll();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
