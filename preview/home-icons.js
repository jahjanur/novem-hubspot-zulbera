/*  Homepage icons — injects line-style SVGs into:
    - Problem cards (3): expensive surprises, running blind, hidden financial burden
    - Platform pillars (3): see everything, predict, prove & improve
    Brand-matched, 1.75 stroke, currentColor (so theme toggle works).
*/
(function () {
  'use strict';

  const ICON = {
    // Problem 1 — Expensive surprises (alert triangle with bolt)
    surprises:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>' +
        '<path d="m13 9-3 5h4l-3 5"/>' +
      '</svg>',

    // Problem 2 — Running blind (eye-off)
    blind:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>' +
        '<path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 11 7 11 7a13.16 13.16 0 0 1-1.67 2.68"/>' +
        '<path d="M6.61 6.61A13.526 13.526 0 0 0 1 12s4 7 11 7a9.74 9.74 0 0 0 5.39-1.61"/>' +
        '<line x1="2" y1="2" x2="22" y2="22"/>' +
      '</svg>',

    // Problem 3 — Hidden financial burden (iceberg/hidden cost)
    hidden:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M12 2 4 9l8 5 8-5z"/>' +
        '<line x1="2" y1="14" x2="22" y2="14" stroke-dasharray="2 2"/>' +
        '<path d="M3 14 12 22 21 14" opacity=".55"/>' +
      '</svg>',

    // Platform 1 — See everything (eye with portfolio cells)
    see:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12z"/>' +
        '<circle cx="12" cy="12" r="3"/>' +
        '<circle cx="12" cy="12" r="1" fill="currentColor"/>' +
      '</svg>',

    // Platform 2 — Predict (forecast/trend line)
    predict:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<polyline points="3 17 9 11 13 15 21 6"/>' +
        '<polyline points="14 6 21 6 21 13"/>' +
        '<circle cx="9" cy="11" r="1.5" fill="currentColor"/>' +
        '<circle cx="13" cy="15" r="1.5" fill="currentColor"/>' +
      '</svg>',

    // Platform 3 — Prove and improve (shield + check)
    prove:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>' +
        '<polyline points="8.5 11.5 11 14 15.5 9.5"/>' +
      '</svg>',
  };

  function tile(svgString) {
    return '<div class="hc-icon-tile" aria-hidden="true">' + svgString + '</div>';
  }

  function init() {
    // (Problem cards now use inline SVGs in their HTML — no JS injection needed.)

    // (Platform pillar 3D renders now live directly in the Product section
    //  HTML — see .prod-row blocks in index.html. No JS injection needed.)
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
