/*  Homepage — THREE OUTCOMES section
    Sticky-scroll storytelling. Section is 320vh tall; an inner viewport
    pins to 100vh while user scrolls. We compute scroll progress through
    the section and switch which of 3 outcome states is active (and which
    of 3 SVG visualizations is shown). Dot indicator + bar-chart animations.
*/
(function () {
  'use strict';

  const section = document.querySelector('.sec--outcomes-v2');
  if (!section) return;

  const track = section.querySelector('.oc-track');
  const contentStates = section.querySelectorAll('.oc-state');
  const visStates = section.querySelectorAll('.oc-vis-state');
  const dots = section.querySelectorAll('.oc-dot');
  const cornerNum = section.querySelector('.oc-corner-num');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const STATES = 3;
  let currentState = -1;
  let ticking = false;

  /* ─── Initialize VIS-3 bar widths from data-width attribute ─── */
  section.querySelectorAll('.oc-bar-fill').forEach((bar) => {
    const w = bar.getAttribute('data-width');
    if (w) {
      bar.setAttribute('width', '0');     // SVG attribute, not CSS
      bar.dataset.targetWidth = w;
    }
  });

  function setBars(state) {
    section.querySelectorAll('[data-state="2"] .oc-bar-fill').forEach((bar, i) => {
      const target = bar.dataset.targetWidth || '0';
      // animate width attribute via JS over 800ms
      if (state === 2) {
        animateAttr(bar, 'width', 0, parseFloat(target), 900 + i * 80, i * 100);
      } else {
        // reset for next time
        bar.setAttribute('width', '0');
      }
    });
  }

  function animateAttr(el, attr, from, to, duration, delay) {
    delay = delay || 0;
    setTimeout(() => {
      const start = performance.now();
      function frame(now) {
        const t = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - t, 3);
        el.setAttribute(attr, from + (to - from) * eased);
        if (t < 1) requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    }, delay);
  }

  /* ─── State switcher ───────────────────────────────────────── */
  function applyState(idx) {
    if (idx === currentState) return;
    currentState = idx;

    contentStates.forEach((el, i) => {
      el.classList.toggle('oc-state--active', i === idx);
    });
    visStates.forEach((el, i) => {
      el.classList.toggle('oc-vis-state--active', i === idx);
    });
    dots.forEach((d, i) => {
      d.classList.toggle('oc-dot--active', i === idx);
    });
    if (cornerNum) cornerNum.textContent = String(idx + 1).padStart(2, '0');

    setBars(idx);
  }

  /* ─── Scroll-based progress ────────────────────────────────── */
  function update() {
    const trackTop = track.getBoundingClientRect().top + window.scrollY;
    const trackHeight = track.offsetHeight - window.innerHeight;
    let progress = (window.scrollY - trackTop) / trackHeight;
    progress = Math.max(0, Math.min(1, progress));

    // Map progress to state (0, 1, 2)
    // First state: 0 - 0.33, Second: 0.33 - 0.66, Third: 0.66 - 1
    const state = progress >= 0.6633 ? 2 : progress >= 0.3333 ? 1 : 0;
    applyState(state);

    ticking = false;
  }

  function onScroll() {
    if (!ticking) {
      requestAnimationFrame(update);
      ticking = true;
    }
  }

  /* ─── Dot click — smooth scroll to that state ─────────────── */
  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      const trackTop = track.getBoundingClientRect().top + window.scrollY;
      const trackHeight = track.offsetHeight - window.innerHeight;
      const target = trackTop + (trackHeight * (i / (STATES - 1)));
      window.scrollTo({ top: target, behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  /* ─── Boot ─────────────────────────────────────────────────── */
  if (window.matchMedia('(min-width: 901px)').matches) {
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
  } else {
    // Mobile: just activate all states for static stacked view
    contentStates.forEach((el) => el.classList.add('oc-state--active'));
    visStates.forEach((el) => el.classList.add('oc-vis-state--active'));
    section.querySelectorAll('.oc-bar-fill').forEach((bar) => {
      bar.setAttribute('width', bar.dataset.targetWidth || '0');
    });
  }
})();
