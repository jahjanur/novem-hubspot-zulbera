/*  Hero v2 — scroll-driven video scrubbing (v3, simplified for HubSpot)
    Strategy: set playbackRate to 0 once the video can render a frame,
    keep it "playing" (which avoids autoplay/pause tug-of-war), and update
    currentTime directly on every scroll event. This is the pattern used
    by Apple/Stripe/Linear product pages.
*/
(function () {
  'use strict';

  function init() {
    var hero  = document.getElementById('heroV2');
    var video = document.getElementById('heroV2Video');
    var progressEl = document.getElementById('heroV2Progress');
    var cueEl = document.getElementById('heroV2Cue');
    if (!hero || !video) {
      // Soft retry in case the element comes in later (HubSpot hydration).
      setTimeout(init, 400);
      return;
    }

    // ── Defensive video setup ──
    video.muted = true;
    video.playsInline = true;
    video.setAttribute('playsinline', '');
    video.setAttribute('webkit-playsinline', '');
    video.preload = 'auto';

    var ready = false;

    function freezeVideo() {
      try { video.playbackRate = 0; } catch (e) {}
    }

    function attemptPlay() {
      var p;
      try { p = video.play(); } catch (e) { return; }
      if (p && typeof p.then === 'function') {
        p.then(function () { freezeVideo(); ready = true; })
         .catch(function () {
           // Autoplay blocked — wait for first interaction or canplay
         });
      } else {
        freezeVideo();
        ready = true;
      }
    }

    // Try to start as soon as we can
    if (video.readyState >= 2) attemptPlay();
    video.addEventListener('loadedmetadata', attemptPlay, { once: true });
    video.addEventListener('canplay', attemptPlay, { once: true });

    // Fallback: any user interaction triggers play (recovers from autoplay block)
    var primeEvents = ['scroll', 'click', 'touchstart', 'wheel', 'keydown', 'pointerdown'];
    function userPrime() {
      attemptPlay();
      primeEvents.forEach(function (ev) {
        window.removeEventListener(ev, userPrime);
      });
    }
    primeEvents.forEach(function (ev) {
      window.addEventListener(ev, userPrime, { once: true, passive: true });
    });

    // ── Progress dots ──
    var STEPS = 4;
    if (progressEl && !progressEl.children.length) {
      for (var i = 0; i < STEPS; i++) {
        var dot = document.createElement('button');
        dot.className = 'hero-v2-progress-dot' + (i === 0 ? ' active' : '');
        dot.dataset.step = i;
        dot.setAttribute('aria-label', 'Jump to step ' + (i + 1));
        (function (idx) {
          dot.addEventListener('click', function () {
            var heroTop = hero.offsetTop;
            var heroH = hero.offsetHeight - window.innerHeight;
            var target = heroTop + (heroH * (idx / (STEPS - 1)));
            window.scrollTo({ top: target, behavior: 'smooth' });
          });
        })(i);
        progressEl.appendChild(dot);
      }
    }

    // ── Scroll-driven currentTime ──
    function computePct() {
      var heroTop = hero.offsetTop;
      var heroH = Math.max(1, hero.offsetHeight - window.innerHeight);
      var pct = (window.pageYOffset - heroTop) / heroH;
      if (pct < 0) pct = 0;
      if (pct > 1) pct = 1;
      return pct;
    }

    function updateVideo() {
      // Always re-freeze in case anything reset the rate
      freezeVideo();
      var dur = video.duration;
      if (!dur || !isFinite(dur)) return;
      var pct = computePct();
      var t = pct * (dur - 0.01);
      // Apply scroll-driven currentTime directly. Browsers handle the seek.
      try { video.currentTime = t; } catch (e) {}

      // Progress dots
      if (progressEl) {
        var step = Math.min(STEPS - 1, Math.floor(pct * STEPS));
        var dots = progressEl.querySelectorAll('.hero-v2-progress-dot');
        for (var i = 0; i < dots.length; i++) {
          dots[i].classList.toggle('active', i === step);
        }
      }
      if (cueEl) cueEl.style.opacity = pct > 0.04 ? '0' : '';
    }

    // Throttle to animation frame so we don't fire seeks faster than the
    // browser can paint.
    var rafScheduled = false;
    function onScroll() {
      if (rafScheduled) return;
      rafScheduled = true;
      requestAnimationFrame(function () {
        rafScheduled = false;
        updateVideo();
      });
    }
    window.addEventListener('scroll',  onScroll, { passive: true });
    window.addEventListener('resize',  onScroll);
    window.addEventListener('load',    onScroll);
    document.addEventListener('readystatechange', onScroll);

    // Initial paint
    onScroll();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
