(function () {
  const root = document.documentElement;

  const themeBtn = document.querySelector('[data-theme-toggle]');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('novem-theme', next); } catch (e) {}
    });
  }
  try {
    const saved = localStorage.getItem('novem-theme');
    if (saved) root.setAttribute('data-theme', saved);
  } catch (e) {}

  const nav = document.getElementById('mainNav');
  if (nav) {
    addEventListener('scroll', () => {
      nav.classList.toggle('nav--scrolled', scrollY > 40);
    }, { passive: true });
  }

  const hamburger = document.getElementById('hamburgerBtn');
  const mobileClose = document.getElementById('mobileCloseBtn');
  const mobileOverlay = document.getElementById('mobileOverlay');
  const mobileMenu = document.getElementById('mobileMenu');

  function openMobile() {
    if (!mobileMenu || !mobileOverlay || !hamburger) return;
    mobileMenu.classList.add('open');
    mobileOverlay.classList.add('open');
    document.body.classList.add('no-scroll');
    hamburger.setAttribute('aria-expanded', 'true');
    mobileMenu.setAttribute('aria-hidden', 'false');
  }
  function closeMobile() {
    if (!mobileMenu || !mobileOverlay || !hamburger) return;
    mobileMenu.classList.remove('open');
    mobileOverlay.classList.remove('open');
    document.body.classList.remove('no-scroll');
    hamburger.setAttribute('aria-expanded', 'false');
    mobileMenu.setAttribute('aria-hidden', 'true');
  }
  if (hamburger) hamburger.addEventListener('click', openMobile);
  if (mobileClose) mobileClose.addEventListener('click', closeMobile);
  if (mobileOverlay) mobileOverlay.addEventListener('click', closeMobile);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMobile(); });
  document.querySelectorAll('[data-mobile-link]').forEach(l => l.addEventListener('click', closeMobile));

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.rev').forEach(el => obs.observe(el));

  document.querySelectorAll('[data-filter]').forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.getAttribute('data-filter');
      document.querySelectorAll('[data-filter]').forEach(b => b.classList.toggle('active', b === btn));
      document.querySelectorAll('[data-type]').forEach(card => {
        const show = type === 'all' || card.getAttribute('data-type') === type;
        card.style.display = show ? '' : 'none';
      });
    });
  });
})();
