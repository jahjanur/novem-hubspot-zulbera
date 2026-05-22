/*  Homepage — TCRO interactive radial diagram
    Click a satellite → highlight it, dim others, light its connection line,
    update the detail panel with category info + count-up the dollar amount.
    Subtle parallax tilt on cursor movement.
*/
(function () {
  'use strict';

  const stage = document.getElementById('tcroV2Stage');
  const detail = document.getElementById('tcroV2Detail');
  if (!stage || !detail) return;

  /* ─── Category data ─────────────────────────────────────── */
  const CATEGORIES = {
    losses: {
      name: 'Losses & Claims',
      pct: 22,
      amount: 1.43,
      body: 'Direct insurance claims, deductibles and retentions paid out across the portfolio. The visible tip of TCRO — and the only piece most frameworks capture.',
    },
    downtime: {
      name: 'Downtime',
      pct: 18,
      amount: 1.17,
      body: 'Revenue lost while a system is out, occupants are displaced, or a building is partially offline. Compounds quickly in income-producing assets.',
    },
    premiums: {
      name: 'Insurance Premiums',
      pct: 15,
      amount: 0.98,
      body: 'Year-over-year premium creep driven by claims history and unverifiable risk profile. Without continuous data, you renew on the insurer\'s terms.',
    },
    maintenance: {
      name: 'Maintenance',
      pct: 12,
      amount: 0.78,
      body: 'Reactive service contracts, emergency callouts, and premium replacement parts. The "planned" maintenance line item that quietly absorbs unplanned work.',
    },
    compliance: {
      name: 'Compliance',
      pct: 9,
      amount: 0.59,
      body: 'Inspections, certifications, regulatory documentation and the staff overhead required to prove your portfolio is operating within code.',
    },
    overhead: {
      name: 'Overhead',
      pct: 14,
      amount: 0.91,
      body: 'Internal staff time spent chasing failures, reconciling vendor invoices, preparing risk reports, and gathering evidence after the fact.',
    },
    governance: {
      name: 'Governance',
      pct: 10,
      amount: 0.65,
      body: 'Board-level risk oversight, internal-audit cycles, lender requirements and the documentation overhead that comes with institutional capital.',
    },
  };

  const TOTAL = {
    name: 'TCRO · Full Portfolio',
    pct: 100,
    amount: 6.51,
    body: 'The full financial burden of building risk — direct claims plus every cost that hits your P&L before it makes the risk register. Click any category to see its share.',
  };

  const sats = stage.querySelectorAll('.tcro-sat');
  const lines = stage.querySelectorAll('.tcro-line');
  const centerAmt = stage.querySelector('.tcro-center-amount');
  let activeCat = null;
  let amountAnim = null;

  /* ─── Count-up utility ─── */
  function countUp(el, fromVal, toVal, dur, formatter) {
    if (amountAnim) cancelAnimationFrame(amountAnim);
    const start = performance.now();
    function frame(now) {
      const t = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      const v = fromVal + (toVal - fromVal) * eased;
      el.textContent = formatter(v);
      if (t < 1) amountAnim = requestAnimationFrame(frame);
    }
    amountAnim = requestAnimationFrame(frame);
  }

  function formatMoney(v) {
    return '$' + v.toFixed(2).replace(/\.?0+$/, '') + 'M';
  }

  /* ─── Apply state (with crossfade transition) ─── */
  let changeTimer = null;
  function applyCategory(catKey) {
    const data = catKey ? CATEGORIES[catKey] : TOTAL;
    if (!data) return;

    // Highlight active sat + line, dim others (these transition smoothly via CSS)
    sats.forEach((s) => {
      s.classList.toggle('tcro-sat--active', s.dataset.cat === catKey);
      s.classList.toggle('tcro-sat--dim', catKey && s.dataset.cat !== catKey);
    });
    lines.forEach((l) => {
      l.classList.toggle('tcro-line--active', l.dataset.cat === catKey);
      l.classList.toggle('tcro-line--dim', catKey && l.dataset.cat !== catKey);
    });

    // Crossfade detail panel text — fade out, swap, fade in
    if (changeTimer) clearTimeout(changeTimer);
    detail.classList.add('is-changing');

    changeTimer = setTimeout(() => {
      detail.querySelector('[data-field="name"]').textContent = data.name;
      detail.querySelector('[data-field="pct"]').textContent = data.pct + '%';
      detail.querySelector('[data-field="body"]').textContent = data.body;

      // Count-up dollar amount (parallel with fade-in)
      const amountEl = detail.querySelector('[data-field="amount"]');
      const fromValMatch = (amountEl.textContent || '').match(/[\d.]+/);
      const fromVal = fromValMatch ? parseFloat(fromValMatch[0]) : data.amount;
      countUp(amountEl, fromVal, data.amount, 700, formatMoney);

      // Center label count-up (faster so it leads)
      if (centerAmt) {
        const fromCenter = parseFloat((centerAmt.textContent || '').match(/[\d.]+/)?.[0] || data.amount);
        countUp(centerAmt, fromCenter, data.amount, 700, formatMoney);
      }

      detail.classList.remove('is-changing');
    }, 260);

    activeCat = catKey;
  }

  /* ─── Click handlers ─── */
  sats.forEach((sat) => {
    sat.addEventListener('click', (e) => {
      e.stopPropagation();
      const cat = sat.dataset.cat;
      // Toggle: click again to deselect
      applyCategory(activeCat === cat ? null : cat);
    });

    // Keyboard accessibility
    sat.setAttribute('tabindex', '0');
    sat.setAttribute('role', 'button');
    sat.setAttribute('aria-label', 'View ' + sat.dataset.cat);
    sat.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        sat.click();
      }
    });
  });

  // Click outside satellites resets to TOTAL
  stage.addEventListener('click', () => {
    if (activeCat) applyCategory(null);
  });

  /* ─── AUTO-CYCLE every 2 seconds when section is visible ─────
     Cycles: total → losses → downtime → premiums → maintenance →
             compliance → overhead → governance → (back to total)
     Pauses if the user clicks a satellite (returns control to them).
     Resumes 6 seconds after their last interaction. */
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce) {
    const sequence = [null, 'losses', 'downtime', 'premiums', 'maintenance', 'compliance', 'overhead', 'governance'];
    let seqIdx = 0;
    let cycleTimer = null;
    let pauseUntil = 0;
    let visible = false;

    function tick() {
      if (!visible) return;
      if (Date.now() < pauseUntil) return;          // user just interacted — wait
      seqIdx = (seqIdx + 1) % sequence.length;
      applyCategory(sequence[seqIdx]);
    }

    function startCycle() {
      if (cycleTimer) return;
      cycleTimer = setInterval(tick, 2000);
    }
    function stopCycle() {
      if (!cycleTimer) return;
      clearInterval(cycleTimer);
      cycleTimer = null;
    }

    // Only run when section is on-screen (saves CPU)
    const visObs = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        visible = e.isIntersecting;
        if (visible) startCycle();
        else stopCycle();
      });
    }, { threshold: 0.25 });
    visObs.observe(stage);

    // Pause auto-cycle for 6 seconds when user clicks a satellite
    sats.forEach((sat) => {
      sat.addEventListener('click', () => {
        pauseUntil = Date.now() + 6000;
        // Sync seqIdx so resume continues from where the user is
        const idx = sequence.indexOf(sat.dataset.cat);
        if (idx >= 0) seqIdx = idx;
      });
    });
    stage.addEventListener('click', (e) => {
      if (e.target.closest('.tcro-sat')) return;
      pauseUntil = Date.now() + 6000;
      seqIdx = 0; // back to total
    });
  }
})();
