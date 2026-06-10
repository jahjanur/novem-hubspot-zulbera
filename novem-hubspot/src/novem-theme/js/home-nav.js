/*  Nav — active page indicator + dropdown behavior
    - Highlights the current page in desktop pill + mobile drawer
    - Highlights a dropdown parent if any of its children match the current route
    - Mobile submenu expand/collapse via accordion click
    - Click-outside closes desktop dropdowns
*/
(function () {
  'use strict';

  function normalize(path) {
    if (!path) return '/';
    path = path.split('#')[0].split('?')[0];
    if (path !== '/' && !path.endsWith('/')) path += '/';
    return path;
  }

  function hrefOf(a) {
    if (!a || !a.getAttribute('href')) return '';
    try {
      return normalize(new URL(a.href, location.origin).pathname);
    } catch (e) {
      return '';
    }
  }

  function markActive() {
    const current = normalize(location.pathname);

    // Desktop nav items
    document.querySelectorAll('nav.nav .nav-item').forEach((item) => {
      // For has-dropdown: active if ANY child link matches current route
      let isActive = false;
      if (item.classList.contains('has-dropdown')) {
        const childLinks = item.querySelectorAll('.nav-dropdown a');
        for (const a of childLinks) {
          if (hrefOf(a) === current) { isActive = true; break; }
        }
        // Also check the trigger link itself
        const trigger = item.querySelector('.nav-dd-trigger');
        if (!isActive && trigger && hrefOf(trigger) === current) isActive = true;
      } else {
        const a = item.querySelector('a');
        if (a && hrefOf(a) === current) isActive = true;
      }
      item.classList.toggle('nav-item--active', isActive);
      const directLink = item.querySelector(':scope > a');
      if (directLink) {
        if (isActive) directLink.setAttribute('aria-current', 'page');
        else directLink.removeAttribute('aria-current');
      }
    });

    // Mobile drawer: active state on direct triggers + sub-items, and auto-open
    // submenus whose child matches the current route.
    document.querySelectorAll('.mobile-nav-item').forEach((item) => {
      const direct = item.querySelector(':scope > .mobile-nav-trigger[href]');
      if (direct) {
        const isActive = hrefOf(direct) === current;
        direct.classList.toggle('mobile-nav-trigger--active', isActive);
        if (isActive) direct.setAttribute('aria-current', 'page');
      }
      if (item.classList.contains('has-submenu')) {
        const subs = item.querySelectorAll('.mobile-sub-item');
        let childActive = false;
        subs.forEach((a) => {
          const isActive = hrefOf(a) === current;
          if (isActive) {
            a.setAttribute('aria-current', 'page');
            childActive = true;
          }
        });
        if (childActive) item.classList.add('open');
      }
    });
  }

  function wireMobileSubmenus() {
    document.querySelectorAll('.mobile-nav-item.has-submenu > .mobile-nav-trigger')
      .forEach((trigger) => {
        trigger.addEventListener('click', (e) => {
          e.preventDefault();
          const item = trigger.closest('.mobile-nav-item');
          if (!item) return;
          const wasOpen = item.classList.contains('open');
          // Close all sibling submenus first (accordion)
          item.parentElement
            .querySelectorAll('.mobile-nav-item.has-submenu.open')
            .forEach((sib) => { if (sib !== item) sib.classList.remove('open'); });
          item.classList.toggle('open', !wasOpen);
          trigger.setAttribute('aria-expanded', String(!wasOpen));
        });
      });
  }

  function wireDesktopDropdownClickOutside() {
    // Hover already opens via CSS; this lets touch/keyboard users tap to open
    // and click outside to close.
    document.querySelectorAll('nav.nav .nav-item.has-dropdown > .nav-dd-trigger')
      .forEach((trigger) => {
        trigger.addEventListener('click', (e) => {
          // Only intercept when keyboard/touch — let normal hover navigation work too.
          // If primary link target matches an item already, allow navigation.
          // We toggle the .open class on first click; second click (or actual link tap)
          // performs navigation. To keep things simple, just navigate as normal —
          // hover/focus-within handles open. So this is a no-op safety net.
        });
      });
    document.addEventListener('click', (e) => {
      if (!e.target.closest('nav.nav .nav-item.has-dropdown')) {
        document.querySelectorAll('nav.nav .nav-item.has-dropdown.open')
          .forEach((it) => it.classList.remove('open'));
      }
    });
  }

  function init() {
    markActive();
    wireMobileSubmenus();
    wireDesktopDropdownClickOutside();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
