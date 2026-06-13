/*  Novem Digital — Redesign layer interactions
    Injects: scroll progress bar, sticky CTA, hero floating widget,
    pre-footer marquee. Refined, no aggressive cursor effects.
*/
(function () {
  'use strict';
  if (window.__novemRedesignLoaded) return;
  window.__novemRedesignLoaded = true;

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ─── SCROLL PROGRESS BAR ────────────────────────────── */
  if (!document.querySelector('.scroll-progress')) {
    const bar = document.createElement('div');
    bar.className = 'scroll-progress';
    document.body.appendChild(bar);
    let ticking = false;
    function update() {
      const scrolled = window.scrollY;
      const max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = max > 0 ? (scrolled / max) * 100 + '%' : '0';
      ticking = false;
    }
    window.addEventListener('scroll', () => {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  /* ─── STICKY CTA BAR ────────────────────────────────── */
  const path = location.pathname;
  const isFormPage = /\/(get-a-demo|become-a-partner|careers\/apply|careers-apply)\/?$/.test(path);
  const is404 = /\/404\/?$/.test(path);

  if (!isFormPage && !is404 && !document.querySelector('.sticky-cta')) {
    const cta = document.createElement('div');
    cta.className = 'sticky-cta';
    cta.innerHTML =
      '<div class="sticky-cta-text"><strong>Failure is predictable.</strong> See what surfaces in your portfolio.</div>' +
      '<a href="/get-a-demo/">Get a Demo →</a>' +
      '<button class="close-x" aria-label="Close">✕</button>';
    document.body.appendChild(cta);

    let dismissed = false;
    try { dismissed = sessionStorage.getItem('novem-cta-dismissed') === '1'; } catch (e) {}
    cta.querySelector('.close-x').addEventListener('click', () => {
      cta.classList.remove('in');
      try { sessionStorage.setItem('novem-cta-dismissed', '1'); } catch (e) {}
      dismissed = true;
    });

    function evalCta() {
      if (dismissed) return;
      const hero = document.querySelector('.hero, .resources-hero, section:first-of-type');
      const heroBottom = hero ? hero.getBoundingClientRect().bottom : 200;
      const footer = document.querySelector('.foot');
      const footerTop = footer ? footer.getBoundingClientRect().top : Infinity;
      const inWindow = heroBottom < 0 && footerTop > window.innerHeight - 100;
      cta.classList.toggle('in', inWindow);
    }
    window.addEventListener('scroll', evalCta, { passive: true });
    evalCta();
  }

  /* ─── HERO RESTRUCTURE — scroll-driven video + 4-step storytelling ───
     The hero becomes 250vh tall. Inside, a sticky 100vh viewport is pinned.
     The Novem video plays scrubbed by scroll position (frame 1 → frame end).
     Foreground content cycles through 4 narrative steps as you scroll. */
  const isHomepage = path === '/' || path === '/index.html';
  const hero = document.querySelector('.hero');

  const ICONS = {
    buildings: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="9" y1="6" x2="9" y2="6"/><line x1="15" y1="6" x2="15" y2="6"/><line x1="9" y1="10" x2="9" y2="10"/><line x1="15" y1="10" x2="15" y2="10"/><line x1="9" y1="14" x2="9" y2="14"/><line x1="15" y1="14" x2="15" y2="14"/><line x1="9" y1="18" x2="15" y2="18"/></svg>',
    trending: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
    clock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    shield: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    alert: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><circle cx="12" cy="17" r=".5" fill="currentColor"/></svg>',
    bolt: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    eye: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
  };

  // Homepage hero is now the static 2-column layout (per client direction).
  // Dynamic video injection + scroll-pin treatment intentionally disabled.
  const heroV2 = document.getElementById('heroV2');
  if (false && hero && isHomepage && !heroV2) {
    // ═══ STEP 1: wrap existing hero contents in a sticky pinned viewport ═══
    if (!hero.querySelector('.hero-pin')) {
      const pin = document.createElement('div');
      pin.className = 'hero-pin';
      // Move all current children of .hero into the pin
      while (hero.firstChild) pin.appendChild(hero.firstChild);
      hero.appendChild(pin);
    }
    const pin = hero.querySelector('.hero-pin');

    // ═══ STEP 2: replace hero-bg <img> with the Novem video ═══
    const heroBg = pin.querySelector('.hero-bg');
    if (heroBg && !heroBg.querySelector('video')) {
      const oldImg = heroBg.querySelector('img');
      const video = document.createElement('video');
      video.className = 'hero-video';
      video.muted = true;
      video.playsInline = true;
      video.preload = 'auto';
      video.setAttribute('aria-hidden', 'true');
      video.poster = '/images/hero-poster.jpg';
      video.innerHTML =
        '<source src="/images/hero.webm" type="video/webm">' +
        '<source src="/images/hero.mp4" type="video/mp4">';
      // Replace the img with the video (keep img as fallback off-screen)
      if (oldImg) oldImg.style.display = 'none';
      heroBg.appendChild(video);
    }
    const video = heroBg ? heroBg.querySelector('video') : null;

    // ═══ STEP 3: progress dots indicating scroll step ═══
    const STEPS = 4; // 4 narrative beats through the video
    if (!pin.querySelector('.hero-progress')) {
      const prog = document.createElement('div');
      prog.className = 'hero-progress';
      for (let i = 0; i < STEPS; i++) {
        const dot = document.createElement('button');
        dot.className = 'hero-progress-dot';
        dot.setAttribute('aria-label', 'Go to step ' + (i + 1));
        dot.dataset.step = i;
        prog.appendChild(dot);
      }
      pin.appendChild(prog);
    }

    // Click on dot scrolls to that step
    pin.querySelectorAll('.hero-progress-dot').forEach((dot) => {
      dot.addEventListener('click', () => {
        const i = parseInt(dot.dataset.step, 10);
        const heroTop = hero.offsetTop;
        const heroH = hero.offsetHeight - window.innerHeight;
        const target = heroTop + (heroH * (i / (STEPS - 1)));
        window.scrollTo({ top: target, behavior: 'smooth' });
      });
    });

    // ═══ STEP 4: ambient orbs (kept) ═══
    if (!pin.querySelector('.hero-orb-1')) {
      const orb1 = document.createElement('div');
      orb1.className = 'hero-orb hero-orb-1';
      const orb2 = document.createElement('div');
      orb2.className = 'hero-orb hero-orb-2';
      pin.appendChild(orb1);
      pin.appendChild(orb2);
    }

    // ═══ STEP 5: scroll cue (only at first step) ═══
    if (!pin.querySelector('.hero-scroll-cue')) {
      const cue = document.createElement('div');
      cue.className = 'hero-scroll-cue';
      cue.innerHTML = '<span>Scroll to explore</span>';
      pin.appendChild(cue);
    }

    // ═══ STEP 6: SCROLL-DRIVEN VIDEO + STEP TRANSITIONS ═══
    // Wait for video metadata to know its duration
    function setupScrollDrive() {
      if (!video || !video.duration || isNaN(video.duration)) {
        setTimeout(setupScrollDrive, 100);
        return;
      }
      const duration = video.duration;
      let ticking = false;

      function update() {
        const heroTop = hero.offsetTop;
        const heroH = hero.offsetHeight - window.innerHeight;
        const scrolled = window.scrollY - heroTop;
        let progress = scrolled / heroH;
        progress = Math.max(0, Math.min(1, progress));

        // Drive video time
        if (video.readyState >= 2) {
          try {
            video.currentTime = progress * duration;
          } catch (e) {}
        }

        // Drive step indicator + content step
        const step = Math.min(STEPS - 1, Math.floor(progress * STEPS));
        pin.querySelectorAll('.hero-progress-dot').forEach((dot, i) => {
          dot.classList.toggle('active', i === step);
        });
        pin.querySelectorAll('.hero-step').forEach((el) => {
          el.classList.toggle('in', parseInt(el.dataset.step, 10) === step);
        });

        // Scroll cue fades out once we leave step 0
        const cue = pin.querySelector('.hero-scroll-cue');
        if (cue) cue.style.opacity = progress > 0.05 ? 0 : '';

        ticking = false;
      }

      window.addEventListener('scroll', () => {
        if (!ticking) { requestAnimationFrame(update); ticking = true; }
      }, { passive: true });
      window.addEventListener('resize', update);
      update();
    }

    if (video) {
      // iOS Safari needs play() called once to allow currentTime scrubbing
      const kickPlay = () => {
        video.play().catch(() => {});
        setTimeout(() => video.pause(), 50);
      };
      if (video.readyState >= 1) { kickPlay(); setupScrollDrive(); }
      else video.addEventListener('loadedmetadata', () => { kickPlay(); setupScrollDrive(); }, { once: true });
    }
  }
  // Non-homepage heroes get NO injected ornaments — keep them clean.
  // (Scroll cue + orbs only appear on the homepage .hero-v2 scroll-driven hero.)

  if (hero && isHomepage && !heroV2) {

    // PRODUCT MOCKUP — inject into hero-right (replaces hidden stats)
    const heroRight = hero.querySelector('.hero-right');
    if (heroRight && !heroRight.querySelector('.hero-mockup') && !reduce) {
      const mockup = document.createElement('div');
      mockup.className = 'hero-mockup-wrap rev';
      mockup.innerHTML =
        '<div class="hero-mockup-chip hero-mockup-chip--top">' + ICONS.bolt + '<span>Predicting in real time</span></div>' +
        '<div class="hero-mockup">' +
          '<div class="mk-header">' +
            '<div class="mk-title">Risk Overview · Portfolio</div>' +
            '<div class="mk-live">Live</div>' +
          '</div>' +
          '<div class="mk-grid">' +
            '<div class="mk-tile mk-tile--healthy">' +
              '<div class="mk-tile-name">Tower A</div>' +
              '<div class="mk-tile-score">12%</div>' +
              '<div class="mk-tile-status">Healthy</div>' +
              '<div class="mk-tile-bar"></div>' +
            '</div>' +
            '<div class="mk-tile mk-tile--risk">' +
              '<div class="mk-tile-name">Tower B</div>' +
              '<div class="mk-tile-score">87%</div>' +
              '<div class="mk-tile-status">At-risk</div>' +
              '<div class="mk-tile-bar"></div>' +
            '</div>' +
            '<div class="mk-tile mk-tile--watch">' +
              '<div class="mk-tile-name">Campus E</div>' +
              '<div class="mk-tile-score">34%</div>' +
              '<div class="mk-tile-status">Watch</div>' +
              '<div class="mk-tile-bar"></div>' +
            '</div>' +
            '<div class="mk-tile mk-tile--healthy">' +
              '<div class="mk-tile-name">Plant W</div>' +
              '<div class="mk-tile-score">8%</div>' +
              '<div class="mk-tile-status">Healthy</div>' +
              '<div class="mk-tile-bar"></div>' +
            '</div>' +
          '</div>' +
          '<div class="mk-chart">' +
            '<div class="mk-chart-header">' +
              '<span class="mk-chart-title">Failure prediction · 30d</span>' +
              '<span class="mk-chart-value">+34% accuracy</span>' +
            '</div>' +
            '<svg class="mk-chart-svg" viewBox="0 0 200 50" preserveAspectRatio="none">' +
              '<defs><linearGradient id="mk-grad" x1="0" y1="0" x2="0" y2="1">' +
                '<stop offset="0%" stop-color="#7BFAB5" stop-opacity=".6"/>' +
                '<stop offset="100%" stop-color="#7BFAB5" stop-opacity="0"/>' +
              '</linearGradient></defs>' +
              '<path class="mk-chart-area" d="M0,40 L20,32 L40,36 L60,24 L80,28 L100,18 L120,22 L140,14 L160,18 L180,10 L200,12 L200,50 L0,50 Z"/>' +
              '<path class="mk-chart-line" d="M0,40 L20,32 L40,36 L60,24 L80,28 L100,18 L120,22 L140,14 L160,18 L180,10 L200,12"/>' +
              '<circle class="mk-chart-dot" cx="200" cy="12" r="3"/>' +
            '</svg>' +
          '</div>' +
          '<div class="mk-alert">' +
            '<div class="mk-alert-icon">' + ICONS.alert + '</div>' +
            '<div class="mk-alert-text"><strong>Action required</strong> · HVAC chiller, Tower B — 87% likely failure within 14 days, est $42K avoidable</div>' +
          '</div>' +
        '</div>' +
        '<div class="hero-mockup-chip hero-mockup-chip--bottom">' + ICONS.eye + '<span>4 buildings monitored</span></div>';
      heroRight.appendChild(mockup);
    }

    // Trust strip below CTAs
    const heroLeft = hero.querySelector('.hero-left');
    const heroActs = hero.querySelector('.hero-acts');
    if (heroLeft && heroActs && !heroLeft.querySelector('.hero-trust')) {
      const trust = document.createElement('div');
      trust.className = 'hero-trust rev';
      trust.innerHTML =
        '<div class="hero-trust-label">Trusted across</div>' +
        '<div class="hero-trust-stats">' +
          '<div class="hero-trust-stat">' + ICONS.shield + '<span><strong>4</strong> asset classes</span></div>' +
          '<div class="hero-trust-stat">' + ICONS.buildings + '<span><strong>North America</strong> coverage</span></div>' +
          '<div class="hero-trust-stat">' + ICONS.trending + '<span><strong>34%</strong> avg cost cut</span></div>' +
        '</div>';
      heroActs.after(trust);
    }

    // HORIZONTAL STAT STRIP — insert section right after the hero
    if (!document.querySelector('.hero-strip')) {
      const strip = document.createElement('section');
      strip.className = 'hero-strip';
      strip.innerHTML =
        '<div class="hero-strip-row">' +
          '<div class="hero-strip-item">' +
            '<div class="hero-strip-icon">' + ICONS.buildings + '</div>' +
            '<div class="hero-strip-text"><div class="hero-strip-num">7.2M</div><div class="hero-strip-lbl">Buildings analyzed</div></div>' +
          '</div>' +
          '<div class="hero-strip-item">' +
            '<div class="hero-strip-icon">' + ICONS.trending + '</div>' +
            '<div class="hero-strip-text"><div class="hero-strip-num">30%</div><div class="hero-strip-lbl">Better capital IRR</div></div>' +
          '</div>' +
          '<div class="hero-strip-item">' +
            '<div class="hero-strip-icon">' + ICONS.clock + '</div>' +
            '<div class="hero-strip-text"><div class="hero-strip-num">1–3yr</div><div class="hero-strip-lbl">Payback period</div></div>' +
          '</div>' +
          '<div class="hero-strip-item">' +
            '<div class="hero-strip-icon">' + ICONS.shield + '</div>' +
            '<div class="hero-strip-text"><div class="hero-strip-num">4</div><div class="hero-strip-lbl">Asset classes covered</div></div>' +
          '</div>' +
        '</div>';
      hero.after(strip);
    }
  }

  /* ─── PRE-FOOTER MARQUEE ────────────────────────────── */
  const foot = document.querySelector('.foot');
  if (foot && !document.querySelector('.marquee-strip')) {
    const phrases = [
      'Failures are Predictable',
      'Total Cost of Risk Ownership',
      'Digital Risk Platform',
      'Audit-ready monitoring',
      'Reduce emergency spend by 34%',
      'Defend every capital decision',
      'Predictive intelligence at scale',
      'Insurance outcomes, controlled'
    ];
    const items = [...phrases, ...phrases].map(p => '<div class="marquee-item">' + p + '</div>').join('');
    const marquee = document.createElement('section');
    marquee.className = 'marquee-strip';
    marquee.setAttribute('aria-hidden', 'true');
    marquee.innerHTML = '<div class="marquee-track">' + items + '</div>';
    foot.parentNode.insertBefore(marquee, foot);
  }

  /* ─── REMOVE LEGACY TILT (cleanup) ─────────────────── */
  document.querySelectorAll('.pil, .seg, .rcard, .insight-card, .hero-stat, .lead-card').forEach((card) => {
    if (card.__tiltBound) return;
    card.__tiltBound = true;
    card.style.transform = '';
    // Don't bind tilt — keep cards static for cleaner aesthetic
  });
})();
