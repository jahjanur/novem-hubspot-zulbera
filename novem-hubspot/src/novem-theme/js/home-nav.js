/*  Nav — active page indicator
    Marks the current page's link in both the desktop pill nav and
    the mobile drawer. Compares window.location.pathname against each
    link's href (normalized to trailing slash form).
*/
(function () {
  'use strict';

  function normalize(path) {
    if (!path) return '/';
    // Strip query + hash
    path = path.split('#')[0].split('?')[0];
    // Ensure trailing slash for non-root paths
    if (path !== '/' && !path.endsWith('/')) path += '/';
    return path;
  }

  function markActive() {
    const current = normalize(location.pathname);

    document.querySelectorAll('nav.nav .nav-item').forEach((item) => {
      const a = item.querySelector('a');
      if (!a) return;
      const href = normalize(new URL(a.href, location.origin).pathname);
      const isActive = href === current;
      item.classList.toggle('nav-item--active', isActive);
      if (isActive) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });

    document.querySelectorAll('.mobile-nav-trigger').forEach((a) => {
      const href = normalize(new URL(a.href, location.origin).pathname);
      const isActive = href === current;
      a.classList.toggle('mobile-nav-trigger--active', isActive);
      if (isActive) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', markActive);
  } else {
    markActive();
  }
})();
