#!/usr/bin/env python3
"""
Sync the unified v2 footer across every preview/*/index.html page.

Replaces any legacy <footer class="foot">...</footer> block with the
canonical v2 footer (brand band + 5-col grid + bottom strip with
Zulbera attribution) and ensures /footer-v2.css is loaded.

Idempotent — re-running keeps things consistent.
"""
import re
import pathlib

FOOTER_V2 = '''<footer class="foot foot-v2">
  <div class="w">

    <!-- BRAND BAND: tagline + CTA -->
    <div class="foot-v2-brand">
      <div class="foot-v2-brand-left">
        <p class="foot-v2-tagline">Ready to see what surfaces in <span class="accent">your portfolio?</span></p>
      </div>
      <a href="/get-a-demo/" class="foot-v2-cta">Get a Demo <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
    </div>

    <!-- MAIN 5-COL GRID -->
    <div class="foot-v2-g">

      <div>
        <a href="/" class="logo" aria-label="Novem Digital home">
          <img src="/logo.png" style="height:26px;width:auto;" alt=""/>
          <span style="font-family:'Titillium Web','Arial Narrow',sans-serif;font-weight:700;font-size:14px;letter-spacing:1.5px;color:#E8F4F0;white-space:nowrap;margin-left:6px;">NOVEM</span>
          <span style="font-family:'Titillium Web','Arial Narrow',sans-serif;font-weight:400;font-size:14px;letter-spacing:1.5px;color:#7BFAB5;opacity:.9;white-space:nowrap;">DIGITAL</span>
        </a>
        <p class="foot-v2-desc">A global digital risk platform making building failure predictable for institutional real estate. Headquartered in Vancouver, BC, Canada.</p>
        <div class="foot-v2-contacts">
          <a href="tel:+18336683647" aria-label="Call Novem Digital">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            +1 (833) 668-3647
          </a>
          <a href="mailto:connect@novemdigital.com" aria-label="Email Novem Digital">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            connect@novemdigital.com
          </a>
          <a href="https://www.linkedin.com/company/novem-digital/" target="_blank" rel="noopener noreferrer" aria-label="Novem Digital on LinkedIn">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
            LinkedIn
          </a>
        </div>
      </div>

      <div>
        <div class="foot-v2-ct">Industries</div>
        <ul class="foot-v2-links">
          <li><a href="/industries/#commercial-mixed-use">Commercial &amp; Mixed Use</a></li>
          <li><a href="/industries/#seniors-wellness">Seniors &amp; Wellness</a></li>
          <li><a href="/industries/#data-centers">Data Centers</a></li>
          <li><a href="/industries/#recreational-venues">Recreational &amp; Venues</a></li>
        </ul>
      </div>

      <div>
        <div class="foot-v2-ct">Platform</div>
        <ul class="foot-v2-links">
          <li><a href="/how-it-works/">How It Works</a></li>
          <li><a href="/tcro/">TCRO Framework</a></li>
          <li><a href="/partners/">Partners</a></li>
        </ul>
      </div>

      <div>
        <div class="foot-v2-ct">Resources</div>
        <ul class="foot-v2-links">
          <li><a href="/resources/">Case Studies</a></li>
          <li><a href="/resources/">Insights &amp; Blog</a></li>
          <li><a href="/resources/">Press &amp; Whitepapers</a></li>
        </ul>
      </div>

      <div>
        <div class="foot-v2-ct">Company</div>
        <ul class="foot-v2-links">
          <li><a href="/about/">About</a></li>
          <li><a href="/careers/">Careers</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>

    </div>

    <!-- BOTTOM strip: copyright + zulbera attribution -->
    <div class="foot-v2-bot">
      <div class="foot-v2-legal">
        <span>&copy; 2026 Novem Digital. All rights reserved.</span>
        <span>Failure is Predictable.</span>
      </div>
      <a class="foot-v2-made" href="https://zulbera.com" target="_blank" rel="noopener noreferrer" aria-label="Made by Zulbera">
        Made with <span class="foot-v2-made-heart">&hearts;</span> by <span class="foot-v2-made-brand">Zulbera</span>
      </a>
    </div>

  </div>
</footer>'''

PREVIEW = pathlib.Path('preview')

# Match any <footer ...>...</footer> block — covers <footer class="foot">,
# <footer class="foot foot-v2">, and bare <footer> shapes used across the
# preview pages. We always overwrite so the canonical content stays in sync.
FOOTER_RE = re.compile(
    r'<footer(?:\s[^>]*)?>.*?</footer>',
    re.DOTALL,
)

# Inject footer-v2.css link after redesign.css if not already present
def ensure_footer_css(txt):
    if '/footer-v2.css' in txt:
        return txt, False
    # Insert after the redesign.css link, falling back to before </head>
    if 'redesign.css' in txt:
        return re.sub(
            r'(<link rel="stylesheet" href="/redesign\.css"[^>]*>)',
            r'\1\n<link rel="stylesheet" href="/footer-v2.css">',
            txt, count=1,
        ), True
    return txt.replace('</head>', '<link rel="stylesheet" href="/footer-v2.css">\n</head>', 1), True


def update_page(path):
    txt = path.read_text(encoding='utf-8')
    original = txt
    changed = False

    # Replace footer
    if FOOTER_RE.search(txt):
        new_txt = FOOTER_RE.sub(FOOTER_V2, txt, count=1)
        if new_txt != txt:
            txt = new_txt
            changed = True

    # Ensure footer-v2.css link
    txt, css_added = ensure_footer_css(txt)
    changed = changed or css_added

    if changed:
        path.write_text(txt, encoding='utf-8')
        return True
    return False


for page in sorted(PREVIEW.glob('**/index.html')):
    if update_page(page):
        print(f"OK Updated {page.relative_to(PREVIEW)}")
    else:
        print(f"   Unchanged {page.relative_to(PREVIEW)}")
