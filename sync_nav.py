#!/usr/bin/env python3
"""
Sync the unified navigation across every preview/*/index.html page.

Structure (locked):
  Home | About | Platform v | Resources v | Contact

Platform v   -> How It Works, TCRO Framework, Industries
Resources v  -> Case Studies, Insights & Blog, Press & Whitepapers,
                Partners, Careers
"""
import re
import pathlib

CARET_SVG = ('<svg class="nav-caret" width="10" height="10" viewBox="0 0 24 24" '
             'fill="none" stroke="currentColor" stroke-width="2.5" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<polyline points="6 9 12 15 18 9"/></svg>')

MOB_CARET = ('<svg class="mob-caret" width="14" height="14" viewBox="0 0 24 24" '
             'fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<polyline points="6 9 12 15 18 9"/></svg>')

DESKTOP_NAV_INNER = f'''<div class="nav-item"><a href="/">Home</a></div>
        <div class="nav-item"><a href="/about/">About</a></div>
        <div class="nav-item has-dropdown" data-dropdown="platform">
          <a href="/how-it-works/" class="nav-dd-trigger">Platform {CARET_SVG}</a>
          <div class="nav-dropdown" role="menu" aria-label="Platform">
            <a href="/how-it-works/" class="nav-dd-item" role="menuitem">
              <span class="nav-dd-title">How It Works</span>
              <span class="nav-dd-desc">Platform architecture &amp; data flow</span>
            </a>
            <a href="/tcro/" class="nav-dd-item" role="menuitem">
              <span class="nav-dd-title">TCRO Framework</span>
              <span class="nav-dd-desc">Total Cost of Risk Ownership</span>
            </a>
            <a href="/industries/" class="nav-dd-item" role="menuitem">
              <span class="nav-dd-title">Industries</span>
              <span class="nav-dd-desc">Sectors we serve</span>
            </a>
          </div>
        </div>
        <div class="nav-item has-dropdown" data-dropdown="resources">
          <a href="/resources/" class="nav-dd-trigger">Resources {CARET_SVG}</a>
          <div class="nav-dropdown" role="menu" aria-label="Resources">
            <a href="/resources/" class="nav-dd-item" role="menuitem">
              <span class="nav-dd-title">Case Studies</span>
              <span class="nav-dd-desc">Real portfolio outcomes</span>
            </a>
            <a href="/resources/" class="nav-dd-item" role="menuitem">
              <span class="nav-dd-title">Insights &amp; Blog</span>
              <span class="nav-dd-desc">Research &amp; industry analysis</span>
            </a>
            <a href="/resources/" class="nav-dd-item" role="menuitem">
              <span class="nav-dd-title">Press &amp; Whitepapers</span>
              <span class="nav-dd-desc">Announcements and research</span>
            </a>
            <a href="/partners/" class="nav-dd-item" role="menuitem">
              <span class="nav-dd-title">Partners</span>
              <span class="nav-dd-desc">Ecosystem &amp; integrations</span>
            </a>
            <a href="/careers/" class="nav-dd-item" role="menuitem">
              <span class="nav-dd-title">Careers</span>
              <span class="nav-dd-desc">Join the team</span>
            </a>
          </div>
        </div>
        <div class="nav-item"><a href="/contact/">Contact</a></div>'''

# Canonical desktop block uses a <div> wrapper to match the modern pages.
DESKTOP_BLOCK_DIV = (
    '<div class="nav-links" id="desktopNav">\n        '
    + DESKTOP_NAV_INNER + '\n      </div>'
)

# For pages whose desktop wrapper is <nav class="nav-links"> (pr-* pages),
# keep the <nav> wrapper but use the same items.
DESKTOP_BLOCK_NAV = (
    '<nav class="nav-links" id="desktopNav" aria-label="Site links">\n        '
    + DESKTOP_NAV_INNER + '\n      </nav>'
)

# Canonical mobile drawer
MOBILE_NAV = f'''<div class="mobile-nav-list">
    <div class="mobile-nav-item">
      <a href="/" class="mobile-nav-trigger" data-mobile-link>Home</a>
    </div>
    <div class="mobile-nav-item">
      <a href="/about/" class="mobile-nav-trigger" data-mobile-link>About</a>
    </div>
    <div class="mobile-nav-item has-submenu" data-submenu="platform">
      <button class="mobile-nav-trigger" type="button" aria-expanded="false">
        Platform {MOB_CARET}
      </button>
      <div class="mobile-submenu">
        <a href="/how-it-works/" class="mobile-sub-item" data-mobile-link>How It Works</a>
        <a href="/tcro/" class="mobile-sub-item" data-mobile-link>TCRO Framework</a>
        <a href="/industries/" class="mobile-sub-item" data-mobile-link>Industries</a>
      </div>
    </div>
    <div class="mobile-nav-item has-submenu" data-submenu="resources">
      <button class="mobile-nav-trigger" type="button" aria-expanded="false">
        Resources {MOB_CARET}
      </button>
      <div class="mobile-submenu">
        <a href="/resources/" class="mobile-sub-item" data-mobile-link>Case Studies</a>
        <a href="/resources/" class="mobile-sub-item" data-mobile-link>Insights &amp; Blog</a>
        <a href="/resources/" class="mobile-sub-item" data-mobile-link>Press &amp; Whitepapers</a>
        <a href="/partners/" class="mobile-sub-item" data-mobile-link>Partners</a>
        <a href="/careers/" class="mobile-sub-item" data-mobile-link>Careers</a>
      </div>
    </div>
    <div class="mobile-nav-item">
      <a href="/contact/" class="mobile-nav-trigger" data-mobile-link>Contact</a>
    </div>
  </div>'''

PREVIEW = pathlib.Path('preview')

# Match the entire desktop links block, whether it's <div ...> or <nav ...>.
DESKTOP_DIV_RE = re.compile(
    r'<div class="nav-links"[^>]*>.*?</div>(?=\s*(?:<!--|<div class="nav-right"|<nav class="nav-right"|<button class="nav-hamburger"))',
    re.DOTALL,
)
DESKTOP_NAV_RE = re.compile(
    r'<nav class="nav-links"[^>]*>.*?</nav>',
    re.DOTALL,
)

# Mobile drawer block match (try several end markers)
MOBILE_RE = re.compile(
    r'<div class="mobile-nav-list">.*?</div>\s*(?=<!--\s*/mobile-nav-list\s*-->|\s*<div class="mobile-bottom"|<button|<div class="mobile-menu-footer)',
    re.DOTALL,
)

def update_page(path):
    txt = path.read_text(encoding='utf-8')
    changed = False

    # Desktop block: prefer <div ... id="desktopNav">; if not, try <nav class="nav-links">.
    if DESKTOP_DIV_RE.search(txt):
        new_txt = DESKTOP_DIV_RE.sub(DESKTOP_BLOCK_DIV, txt, count=1)
        if new_txt != txt:
            txt = new_txt
            changed = True
    elif DESKTOP_NAV_RE.search(txt):
        new_txt = DESKTOP_NAV_RE.sub(DESKTOP_BLOCK_NAV, txt, count=1)
        if new_txt != txt:
            txt = new_txt
            changed = True

    # Mobile drawer
    if MOBILE_RE.search(txt):
        new_txt = MOBILE_RE.sub(MOBILE_NAV + '\n  ', txt, count=1)
        if new_txt != txt:
            txt = new_txt
            changed = True

    # Inject home-nav.js (idempotent)
    if '/home-nav.js' not in txt:
        txt = txt.replace(
            '</body>',
            '<script src="/home-nav.js" defer></script>\n</body>',
            1,
        )
        changed = True

    if changed:
        path.write_text(txt, encoding='utf-8')
        return True
    return False


for page in sorted(PREVIEW.glob('**/index.html')):
    if update_page(page):
        print(f"OK Updated {page.relative_to(PREVIEW)}")
    else:
        print(f"   Unchanged {page.relative_to(PREVIEW)}")
