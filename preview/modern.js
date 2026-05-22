/*  Novem Digital — modern interactions (refined)
    Scroll reveal, animated counters, subtle hover lift.
    Cursor glow + magnetic buttons removed (clashed with redesign).
*/
(function () {
  'use strict';

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;

  /* ─── REVEAL ON SCROLL ─────────────────────────────── */
  const revObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        revObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

  function tagReveals() {
    const candidates = document.querySelectorAll(
      'section .h2, section .h3, section .lg, section p.sm, ' +
      '.pil, .prob-card, .seg, .rcard, .part, .lead-card, .insight-card, ' +
      '.hero-stat, .stat-b, .step, .proof-cust-card, .tcro-diagram-wrap, .lead-bar'
    );
    candidates.forEach((el) => {
      if (!el.classList.contains('rev')) el.classList.add('rev');
      const idx = Array.from(el.parentNode.children).indexOf(el);
      if (idx > 0 && idx < 6) el.classList.add('d' + Math.min(idx, 4));
      revObserver.observe(el);
    });
  }
  tagReveals();

  /* ─── ANIMATED NUMBER COUNTERS ─────────────────────── */
  function animateCounter(el) {
    const raw = el.textContent.trim();
    const match = raw.match(/^([^\d\-]*)([\d,.]+)([^\d]*)$/);
    if (!match) return;
    const prefix = match[1] || '';
    const numStr = match[2];
    const suffix = match[3] || '';
    const target = parseFloat(numStr.replace(/,/g, ''));
    if (isNaN(target)) return;
    const hasDecimal = numStr.includes('.');
    const decimals = hasDecimal ? numStr.split('.')[1].length : 0;
    const duration = 1400;
    const start = performance.now();

    function frame(now) {
      const t = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      const current = target * eased;
      el.textContent = prefix + current.toFixed(decimals) + suffix;
      if (t < 1) requestAnimationFrame(frame);
      else el.textContent = raw;
    }
    requestAnimationFrame(frame);
  }

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll(
    '.hero-stat-num, .stat-b-num, .proof-v, .rcard-stat-num, .insight-stat, .rd-stat-num'
  ).forEach((el) => counterObserver.observe(el));

  /* ─── PARALLAX HERO BG (subtle) ────────────────────── */
  const heroBgs = document.querySelectorAll('.hero-bg img, .resources-hero-bg img');
  if (heroBgs.length) {
    let ticking = false;
    function updateParallax() {
      const y = window.scrollY;
      heroBgs.forEach((img) => {
        const speed = 0.3;
        img.style.transform = `translate3d(0, ${y * speed}px, 0)`;
      });
      ticking = false;
    }
    window.addEventListener('scroll', () => {
      if (!ticking) { requestAnimationFrame(updateParallax); ticking = true; }
    }, { passive: true });
  }

  /* ─── ACTIVE NAV STATE ─────────────────────────────── */
  const path = location.pathname.replace(/\/+$/, '') || '/';
  document.querySelectorAll('.nav-item > a, .mobile-nav-trigger').forEach((a) => {
    const href = (a.getAttribute('href') || '').replace(/\/+$/, '') || '/';
    if (href === path && href !== '/') a.style.color = 'var(--acc-g, #7BFAB5)';
  });

  /* ─── SMOOTH ANCHOR SCROLLING ──────────────────────── */
  document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach((a) => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      const target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        history.pushState(null, '', id);
      }
    });
  });

  /* ─── THEME PERSISTENCE ────────────────────────────── */
  try {
    const saved = localStorage.getItem('novem-theme');
    if (saved) document.documentElement.setAttribute('data-theme', saved);
  } catch (e) {}
  document.querySelectorAll('[data-theme-toggle]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('novem-theme', next); } catch (e) {}
    });
  });

  /* ─── REMOVE LEGACY CURSOR GLOW (cleanup if previously injected) ── */
  document.querySelectorAll('.cursor-glow').forEach((el) => el.remove());
})();
