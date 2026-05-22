/*  Homepage — PROBLEM section animations
    - Card entrance reveal with stagger (IntersectionObserver)
    - SVG line draw (cost-spike chart)
    - SVG cell + question-mark stagger reveal (data void)
    - SVG iceberg parts reveal + $ amount count-up
    - 3D card tilt on cursor hover
*/
(function () {
  'use strict';

  const root = document.querySelector('.sec--problem-v4');
  if (!root) return;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ────────── 1. CARD ENTRANCE on scroll-into-view ────────── */
  const cards = root.querySelectorAll('.prob-v4-card');
  cards.forEach((c, i) => {
    c.style.setProperty('--idx', i);
  });

  const cardObs = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('pv4-in');
        cardObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.18, rootMargin: '0px 0px -8% 0px' });

  cards.forEach((c) => cardObs.observe(c));

  /* ────────── 2. SVG ENTER animations when card visible ────── */
  function animateCard(card, idx) {
    if (reduce) return;

    // Card 1 — line draw
    if (idx === 0) {
      const line = card.querySelector('.pv4-spike-line');
      if (line) {
        try {
          const len = line.getTotalLength();
          line.style.strokeDasharray = len;
          line.style.strokeDashoffset = len;
          line.style.transition = 'stroke-dashoffset 1.5s cubic-bezier(.16, 1, .3, 1)';
          // force reflow then set offset to 0
          // eslint-disable-next-line no-unused-expressions
          line.getBoundingClientRect();
          requestAnimationFrame(() => { line.style.strokeDashoffset = '0'; });
        } catch (e) {}
      }
      const area = card.querySelector('.pv4-spike-area');
      if (area) {
        area.style.opacity = '0';
        area.style.transition = 'opacity 1s ease 0.5s';
        requestAnimationFrame(() => { area.style.opacity = '1'; });
      }
      // dots fade in after line draws
      card.querySelectorAll('.pv4-spike-dot').forEach((dot, i) => {
        dot.style.opacity = '0';
        dot.style.transition = 'opacity .4s ease ' + (1.2 + i * 0.15) + 's';
        requestAnimationFrame(() => { dot.style.opacity = '1'; });
      });

      // Count-up for +$2.8M total
      const total = card.querySelector('.pv4-total-num');
      if (total) countUp(total, '+$2.8M');
    }

    // Card 2 — cells stagger in + question marks
    if (idx === 1) {
      card.querySelectorAll('.pv4-cell').forEach((cell, i) => {
        cell.style.opacity = '0';
        cell.style.transform = 'scale(.92)';
        cell.style.transformOrigin = 'center';
        cell.style.transformBox = 'fill-box';
        cell.style.transition = 'opacity .5s ease, transform .6s cubic-bezier(.16,1,.3,1)';
        cell.style.transitionDelay = (0.1 + i * 0.08) + 's';
        requestAnimationFrame(() => {
          cell.style.opacity = '1';
          cell.style.transform = 'scale(1)';
        });
      });
      card.querySelectorAll('.pv4-q').forEach((q, i) => {
        q.style.opacity = '0';
        q.style.transition = 'opacity .4s ease ' + (0.4 + i * 0.08) + 's';
        requestAnimationFrame(() => { q.style.opacity = '1'; });
      });
    }

    // Card 3 — iceberg parts + count-up
    if (idx === 2) {
      const top = card.querySelector('.pv4-ice-top');
      if (top) {
        top.style.opacity = '0';
        top.style.transform = 'translateY(-12px)';
        top.style.transformBox = 'fill-box';
        top.style.transition = 'opacity .6s ease, transform .8s cubic-bezier(.16,1,.3,1)';
        requestAnimationFrame(() => {
          top.style.opacity = '1';
          top.style.transform = 'translateY(0)';
        });
      }
      const line = card.querySelector('.pv4-pl-line');
      if (line) {
        line.style.opacity = '0';
        line.style.transition = 'opacity .5s ease .4s';
        requestAnimationFrame(() => { line.style.opacity = '1'; });
      }
      const bot = card.querySelector('.pv4-ice-bottom');
      if (bot) {
        bot.style.opacity = '0';
        bot.style.transform = 'translateY(20px) scaleY(.6)';
        bot.style.transformOrigin = 'center top';
        bot.style.transformBox = 'fill-box';
        bot.style.transition = 'opacity .8s ease .7s, transform 1.1s cubic-bezier(.16,1,.3,1) .7s';
        requestAnimationFrame(() => {
          bot.style.opacity = '1';
          bot.style.transform = 'translateY(0) scaleY(1)';
        });
      }
      const burdenNum = card.querySelector('.pv4-burden-num');
      if (burdenNum) setTimeout(() => countUp(burdenNum, '$10.8M'), 1200);
    }
  }

  cards.forEach((card, i) => {
    const triggerObs = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          animateCard(card, i);
          triggerObs.unobserve(card);
        }
      });
    }, { threshold: 0.4 });
    triggerObs.observe(card);
  });

  /* ────────── 3. COUNT-UP utility (handles $ and M/K) ────────── */
  function countUp(el, finalText) {
    const m = finalText.match(/^([^\d-]*)(-?[\d.,]+)([^\d]*)$/);
    if (!m) return;
    const prefix = m[1] || '';
    const numStr = m[2];
    const suffix = m[3] || '';
    const target = parseFloat(numStr.replace(/,/g, ''));
    if (isNaN(target)) return;
    const decimals = numStr.includes('.') ? numStr.split('.')[1].length : 0;
    const dur = 1100;
    const start = performance.now();
    function frame(now) {
      const t = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = prefix + (target * eased).toFixed(decimals) + suffix;
      if (t < 1) requestAnimationFrame(frame);
      else el.textContent = finalText;
    }
    el.textContent = prefix + '0' + (decimals ? '.' + '0'.repeat(decimals) : '') + suffix;
    requestAnimationFrame(frame);
  }

  /* ────────── 4. 3D CARD TILT on hover ────────── */
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches && !reduce) {
    const TILT = 4; // max degrees
    cards.forEach((card) => {
      const inner = card;
      let raf;
      let target = { rx: 0, ry: 0 };
      let current = { rx: 0, ry: 0 };

      let lift = 0;
      let targetLift = 0;

      function loop() {
        current.rx += (target.rx - current.rx) * 0.12;
        current.ry += (target.ry - current.ry) * 0.12;
        lift += (targetLift - lift) * 0.14;
        inner.style.transform =
          'perspective(1200px) translateY(' + lift + 'px) rotateX(' + current.rx + 'deg) rotateY(' + current.ry + 'deg)';
        if (Math.abs(target.rx - current.rx) > 0.05 ||
            Math.abs(target.ry - current.ry) > 0.05 ||
            Math.abs(targetLift - lift) > 0.1) {
          raf = requestAnimationFrame(loop);
        } else {
          cancelAnimationFrame(raf);
        }
      }

      card.addEventListener('mouseenter', () => { targetLift = -6; cancelAnimationFrame(raf); raf = requestAnimationFrame(loop); });
      card.addEventListener('mousemove', (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width;
        const y = (e.clientY - r.top) / r.height;
        target.ry = (x - 0.5) * TILT * 2;
        target.rx = -(y - 0.5) * TILT * 2;
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(loop);
      });
      card.addEventListener('mouseleave', () => {
        target = { rx: 0, ry: 0 };
        targetLift = 0;
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(loop);
      });
    });
  }

  /* ────────── 5. SHIMMER sweep across card on intersect ────────── */
  cards.forEach((card) => {
    const intObs = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          card.classList.add('pv4-shimmer');
          setTimeout(() => card.classList.remove('pv4-shimmer'), 1600);
          intObs.unobserve(card);
        }
      });
    }, { threshold: 0.3 });
    intObs.observe(card);
  });
})();
