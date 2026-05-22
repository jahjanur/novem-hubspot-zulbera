#!/usr/bin/env bash
# Converts each unzipped source HTML page into a HubSpot HubL page template.
# - Strips the original <nav> and <footer> (those are partials now)
# - Keeps the page's <style> block but strips the global tokens that already live in main.css
# - Wraps in {% extends "../layouts/base.html" %} + {% block body %} / {% block extra_head %}
# - Fixes obvious placeholder hrefs
set -euo pipefail

SRC="/Users/zulbearijahjanur/Downloads/Novem_HubSpot_Zulbera/unzipped"
OUT="/Users/zulbearijahjanur/Downloads/Novem_HubSpot_Zulbera/novem-hubspot/src/novem-theme/templates"

convert () {
  local src_file="$1"
  local out_file="$2"
  local label="$3"
  local screenshot="${4:-}"

  python3 - "$src_file" "$out_file" "$label" <<'PY'
import sys, re, pathlib
src_path, out_path, label = sys.argv[1], sys.argv[2], sys.argv[3]
html = pathlib.Path(src_path).read_text(encoding='utf-8', errors='replace')

# Body content: from <main ...> to </main>, exclusive of the tag itself
m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
body = m.group(1) if m else ''

# Page-specific CSS: take the FIRST <style>...</style>, then drop the global tokens
s = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
css = s.group(1) if s else ''

# Remove the global blocks we already pushed to main.css: BRAND TOKENS / RESET / UTILITIES /
# BUTTONS / NAVIGATION / FOOTER / FAQ / CTA / REVEAL / body.no-scroll
def strip_global(css):
    # remove :root and [data-theme="light"] declarations
    css = re.sub(r':root\s*\{[^}]*\}', '', css, flags=re.DOTALL)
    css = re.sub(r'\[data-theme="light"\]\s*\{[^}]*\}', '', css, flags=re.DOTALL)
    # remove reset/utility/btn/nav/footer/faq/cta/reveal selector blocks
    patterns_to_drop = [
        r'\*\s*,\s*\*::before\s*,\s*\*::after\s*\{[^}]*\}',
        r'html\s*\{[^}]*\}',
        r'body\s*\{[^}]*\}',
        r'img\s*\{[^}]*\}',
        r'ul\s*\{[^}]*\}',
        r'button\s*\{[^}]*\}',
        r'a\s*\{[^}]*\}',
        r':focus-visible\s*\{[^}]*\}',
        r'\.sr-only\s*\{[^}]*\}',
        r'\.w\s*\{[^}]*\}',
        r'\.wm\s*\{[^}]*\}',
        r'\.eye\s*\{[^}]*\}',
        r'\.eye-dot\s*\{[^}]*\}',
        r'@keyframes\s+blink\s*\{[^}]*\}',
        r'\.h1\s*\{[^}]*\}',
        r'\.h2\s*\{[^}]*\}',
        r'\.h3\s*\{[^}]*\}',
        r'\.accent\s*\{[^}]*\}',
        r'\.lg\s*\{[^}]*\}',
        r'\.sm\s*\{[^}]*\}',
        r'\.sec\s*\{[^}]*\}',
        r'\.sec--alt\s*\{[^}]*\}',
        r'\.sec--gun\s*\{[^}]*\}',
        r'sup\s*\{[^}]*\}',
        r'\.btn\s*\{[^}]*\}',
        r'\.btn:hover\s*\{[^}]*\}',
        r'\.btn-p\s*\{[^}]*\}',
        r'\.btn-p:hover\s*\{[^}]*\}',
        r'\.btn-g\s*\{[^}]*\}',
        r'\.btn-g:hover\s*\{[^}]*\}',
        r'\.btn-ghost\s*\{[^}]*\}',
        r'\.btn-ghost:hover\s*\{[^}]*\}',
        r'\.btn-s\s*\{[^}]*\}',
        r'\.btn-s:hover\s*\{[^}]*\}',
        r'\.btn-gs\s*\{[^}]*\}',
        r'\.btn-gs:hover\s*\{[^}]*\}',
        r'\.btn-ol\s*\{[^}]*\}',
        r'\.btn-ol:hover\s*\{[^}]*\}',
        r'\[data-theme="light"\] \.btn-ghost\s*\{[^}]*\}',
        r'\[data-theme="light"\] \.btn-ghost:hover\s*\{[^}]*\}',
        r'\.nav[^\{]*\{[^}]*\}',
        r'\.mobile-[a-z\-]*[^\{]*\{[^}]*\}',
        r'\[data-theme="light"\] \.mobile-[a-z\-]*[^\{]*\{[^}]*\}',
        r'\[data-theme="light"\] \.nav[^\{]*\{[^}]*\}',
        r'\.tbtn\s*\{[^}]*\}',
        r'\.tbtn:hover\s*\{[^}]*\}',
        r'\.logo\s*\{[^}]*\}',
        r'\.foot[^\{]*\{[^}]*\}',
        r'\.rev\s*\{[^}]*\}',
        r'\.rev\.in\s*\{[^}]*\}',
        r'\.d1\s*\{[^}]*\}',
        r'\.d2\s*\{[^}]*\}',
        r'\.d3\s*\{[^}]*\}',
        r'\.d1\s*,\s*\.d2\s*,\s*\.d3[^{]*\{[^}]*\}',
        r'body\.no-scroll\s*\{[^}]*\}',
        r'@media[^\{]*\{\s*\.nav[^}]*\}[^}]*\}',
        r'@media[^\{]*\{\s*\.foot[^}]*\}[^}]*\}',
        r'@media\(prefers-reduced-motion[^\{]*\{[^}]*\}',
        r'@media[^{]*\{\s*\.rev[^}]*\}\s*\}',
    ]
    for p in patterns_to_drop:
        css = re.sub(p, '', css, flags=re.IGNORECASE)
    return css

css = strip_global(css)
# Clean up double newlines
css = re.sub(r'\n\s*\n\s*\n+', '\n\n', css).strip()

# Drop the dev-only Perplexity inline-edit injection if present in body
body = re.sub(r'<script data-pplx-inline-edit>.*?</script>', '', body, flags=re.DOTALL)

# Fix obvious placeholder hrefs in body
body = body.replace('href="#"', 'href="/get-a-demo/"')

# Extract meta from source for the template "label" doc
title_m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
desc_m  = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html, re.DOTALL)
title = title_m.group(1).strip() if title_m else label
desc  = desc_m.group(1).strip() if desc_m else ''

out = []
out.append('<!--')
out.append('  templateType: page')
out.append(f'  label: "{label}"')
out.append('  isAvailableForNewContent: true')
out.append(f'  -->')
out.append('{% extends "../layouts/base.html" %}')
out.append('')
out.append(f"{{# Suggested page settings — title: {title} #}}")
if desc:
    out.append(f"{{# meta description: {desc} #}}")
out.append('')
if css:
    out.append('{% block extra_head %}')
    out.append('<style>')
    out.append(css)
    out.append('</style>')
    out.append('{% endblock %}')
    out.append('')
out.append('{% block body %}')
out.append(body.strip())
out.append('{% endblock %}')

pathlib.Path(out_path).write_text('\n'.join(out), encoding='utf-8')
print(f"Wrote {out_path}")
PY
}

mkdir -p "$OUT"

convert "$SRC/01-Homepage/01-Homepage/index.html"             "$OUT/home.html"              "Home"
convert "$SRC/02-Platform/02-Platform/index.html"             "$OUT/platform.html"          "Platform"
convert "$SRC/03-Industries/03-Industries/index.html"         "$OUT/industries.html"        "Industries"
convert "$SRC/04-TCRO/04-TCRO/index.html"                     "$OUT/tcro.html"              "TCRO"
convert "$SRC/05-Partners/05-Partners/index.html"             "$OUT/partners.html"          "Partners"
convert "$SRC/07-About/07-About/index.html"                   "$OUT/about.html"             "About"
convert "$SRC/08-Careers/08-Careers/index.html"               "$OUT/careers.html"           "Careers"
convert "$SRC/09-404/09-404/index.html"                       "$OUT/system/error_page.html" "404 Error"
convert "$SRC/10-Form-Get-a-Demo/10-Form-Get-a-Demo/index.html" "$OUT/get-a-demo.html"      "Get a Demo (form)"
convert "$SRC/11-Form-Partner/11-Form-Partner/index.html"     "$OUT/become-a-partner.html"  "Become a Partner (form)"
convert "$SRC/12-Form-Careers-Apply/12-Form-Careers-Apply/index.html" "$OUT/careers-apply.html" "Careers Apply (form)"
convert "$SRC/06-Resources/06-Resources/index.html"           "$OUT/resources.html"         "Resources (listing)"
convert "$SRC/13-Template-Case-Study/13-Template-Case-Study/index.html"     "$OUT/resource-case-study.html"     "Resource: Case Study (HubDB)"
convert "$SRC/14-Template-Whitepaper/14-Template-Whitepaper/index.html"     "$OUT/resource-whitepaper.html"     "Resource: White Paper (HubDB)"
convert "$SRC/15-Template-Blog/15-Template-Blog/index.html"                 "$OUT/resource-blog.html"           "Resource: Blog (HubDB)"
convert "$SRC/16-Template-Press-Release/16-Template-Press-Release/index.html" "$OUT/resource-press-release.html" "Resource: Press Release (HubDB)"
