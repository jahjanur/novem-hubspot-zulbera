#!/usr/bin/env python3
"""Parse Press-Releases-v1.3.docx (actually HTML) into structured JSON."""
import re
import json
import os
from html import unescape
from datetime import datetime

SRC = "/Users/zulbearijahjanur/Downloads/Novem_HubSpot_Zulbera/Press-Releases-v1.3.docx"
OUT = "/Users/zulbearijahjanur/Downloads/Novem_HubSpot_Zulbera/.build/press-releases-index.json"
DEBUG_DIR = "/Users/zulbearijahjanur/Downloads/Novem_HubSpot_Zulbera/.build/pr_debug"
os.makedirs(DEBUG_DIR, exist_ok=True)

with open(SRC, "r", encoding="utf-8", errors="replace") as f:
    raw = f.read()

# Strip head, style, script, comments
raw = re.sub(r"<head\b[^>]*>.*?</head>", "", raw, flags=re.DOTALL | re.IGNORECASE)
raw = re.sub(r"<style\b[^>]*>.*?</style>", "", raw, flags=re.DOTALL | re.IGNORECASE)
raw = re.sub(r"<script\b[^>]*>.*?</script>", "", raw, flags=re.DOTALL | re.IGNORECASE)
raw = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
# Word-specific XML
raw = re.sub(r"<\?xml[^>]*\?>", "", raw)
raw = re.sub(r"<o:p\b[^>]*>.*?</o:p>", "", raw, flags=re.DOTALL | re.IGNORECASE)
raw = re.sub(r"<o:p\b[^>]*/>", "", raw, flags=re.IGNORECASE)

# Remove Word-specific tags but keep content
def strip_vendor_attrs(html: str) -> str:
    # Remove class, style, lang, dir, align, mso-* attributes
    html = re.sub(r'\s+(?:class|style|lang|dir|align|width|height|valign|cellspacing|cellpadding|border|bgcolor|nowrap)="[^"]*"', "", html, flags=re.IGNORECASE)
    html = re.sub(r"\s+(?:class|style|lang|dir|align|width|height|valign|cellspacing|cellpadding|border|bgcolor|nowrap)='[^']*'", "", html, flags=re.IGNORECASE)
    # remove name attribute on a tags (anchors)
    html = re.sub(r'\s+name="[^"]*"', "", html, flags=re.IGNORECASE)
    # collapse empty span/font tags
    html = re.sub(r"<span\s*>([\s\S]*?)</span>", r"\1", html, flags=re.IGNORECASE)
    html = re.sub(r"<font\s*>([\s\S]*?)</font>", r"\1", html, flags=re.IGNORECASE)
    html = re.sub(r"<span\b[^>]*>", "<span>", html, flags=re.IGNORECASE)
    # collapse repeated spaces
    return html

# Extract body
body_m = re.search(r"<body\b[^>]*>(.*)</body>", raw, flags=re.DOTALL | re.IGNORECASE)
body = body_m.group(1) if body_m else raw

# Save cleaned for debugging
with open(os.path.join(DEBUG_DIR, "01_body.html"), "w") as f:
    f.write(body)

cleaned = strip_vendor_attrs(body)
# Repeated cleaning
for _ in range(3):
    new = strip_vendor_attrs(cleaned)
    if new == cleaned:
        break
    cleaned = new

with open(os.path.join(DEBUG_DIR, "02_cleaned.html"), "w") as f:
    f.write(cleaned)


def tag_text(html: str) -> str:
    """Strip all HTML tags, decode entities, collapse whitespace."""
    text = re.sub(r"<[^>]+>", " ", html)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Find press release boundaries. Look for "FOR IMMEDIATE RELEASE" markers.
# First, find all positions of that string in the cleaned HTML.
markers = [m.start() for m in re.finditer(r"FOR\s+IMMEDIATE\s+RELEASE", cleaned, flags=re.IGNORECASE)]
print(f"Found {len(markers)} 'FOR IMMEDIATE RELEASE' markers")

if len(markers) < 2:
    # Fallback: look for city datelines
    markers = [m.start() for m in re.finditer(r"(Vancouver|Toronto|Calgary|Ottawa|Montreal|New\s+York|Seattle|Boston),?\s+(?:BC|ON|AB|QC|NY|WA|MA)\b", cleaned, flags=re.IGNORECASE)]
    print(f"Fallback: found {len(markers)} city dateline markers")

# Slice into chunks
chunks = []
for i, start in enumerate(markers):
    end = markers[i + 1] if i + 1 < len(markers) else len(cleaned)
    # Back up to include nearest preceding heading (h1/h2/h3) that's within ~3000 chars
    look_back = max(0, start - 4000)
    pre = cleaned[look_back:start]
    # Find last heading tag opening
    headings = list(re.finditer(r"<(h[1-3])\b", pre, flags=re.IGNORECASE))
    if headings:
        # Use absolute position
        chunk_start = look_back + headings[-1].start()
    else:
        # try last <p> with bold inside
        chunk_start = start
    chunks.append((chunk_start, end))

print(f"Built {len(chunks)} chunks")


def slugify(text: str, max_len: int = 60) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s[:max_len].rstrip("-")


def extract_title(chunk_html: str) -> str:
    # Try h1/h2/h3
    for tag in ("h1", "h2", "h3"):
        m = re.search(rf"<{tag}\b[^>]*>(.*?)</{tag}>", chunk_html, flags=re.DOTALL | re.IGNORECASE)
        if m:
            t = tag_text(m.group(1))
            if t and len(t) > 5 and "FOR IMMEDIATE RELEASE" not in t.upper():
                return t
    # Try bold paragraphs
    for m in re.finditer(r"<p\b[^>]*>\s*<(?:b|strong)\b[^>]*>(.*?)</(?:b|strong)>\s*</p>", chunk_html, flags=re.DOTALL | re.IGNORECASE):
        t = tag_text(m.group(1))
        if t and len(t) > 10 and "FOR IMMEDIATE RELEASE" not in t.upper() and not re.match(r"^[A-Z][a-z]+,?\s+(BC|ON|AB)", t):
            return t
    # Try any bold
    for m in re.finditer(r"<(?:b|strong)\b[^>]*>(.*?)</(?:b|strong)>", chunk_html, flags=re.DOTALL | re.IGNORECASE):
        t = tag_text(m.group(1))
        if t and len(t) > 15 and "FOR IMMEDIATE RELEASE" not in t.upper() and not re.match(r"^[A-Z][a-z]+,?\s+(BC|ON|AB)", t):
            return t
    return ""


MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"

def extract_dateline_and_date(chunk_html: str):
    text = tag_text(chunk_html)
    # Find "City, ST — Month Day, Year" or with hyphens
    pat = rf"([A-Z][A-Za-z\.\s]+,\s*[A-Z]{{2,}}(?:\s*,\s*[A-Z][a-z]+)?)\s*[–—\-]+\s*({MONTHS})\s+(\d{{1,2}}),?\s+(\d{{4}})"
    m = re.search(pat, text)
    if m:
        city = m.group(1).strip()
        month = m.group(2)
        day = m.group(3)
        year = m.group(4)
        dateline = f"{city} — {month} {int(day)}, {year}"
        try:
            iso = datetime.strptime(f"{month} {day} {year}", "%B %d %Y").date().isoformat()
        except ValueError:
            iso = ""
        return dateline, iso
    # Fallback: just find a date
    m = re.search(rf"({MONTHS})\s+(\d{{1,2}}),?\s+(\d{{4}})", text)
    if m:
        month, day, year = m.group(1), m.group(2), m.group(3)
        try:
            iso = datetime.strptime(f"{month} {day} {year}", "%B %d %Y").date().isoformat()
        except ValueError:
            iso = ""
        return f"{month} {int(day)}, {year}", iso
    return "", ""


def extract_summary(body_text: str) -> str:
    # First sentence(s) up to ~25 words
    sentences = re.split(r"(?<=[\.!?])\s+", body_text)
    words = []
    for s in sentences:
        for w in s.split():
            words.append(w)
            if len(words) >= 28:
                break
        if len(words) >= 22:
            break
    summary = " ".join(words[:28])
    # Trim to nearest end-of-sentence if reasonable
    if not summary.endswith((".", "!", "?")):
        summary = summary.rstrip(",;:") + "."
    return summary


def clean_body_html(chunk_html: str) -> str:
    h = chunk_html
    # Replace headings into h2
    h = re.sub(r"<h[1-3]\b[^>]*>", "<h2>", h, flags=re.IGNORECASE)
    h = re.sub(r"</h[1-3]>", "</h2>", h, flags=re.IGNORECASE)
    # Remove span/font wrappers
    h = re.sub(r"</?span\b[^>]*>", "", h, flags=re.IGNORECASE)
    h = re.sub(r"</?font\b[^>]*>", "", h, flags=re.IGNORECASE)
    h = re.sub(r"</?div\b[^>]*>", "", h, flags=re.IGNORECASE)
    # Word artifacts: empty paragraphs
    h = re.sub(r"<p\b[^>]*>\s*(?:&nbsp;|\s)*</p>", "", h, flags=re.IGNORECASE)
    # Normalize p tags - strip attrs
    h = re.sub(r"<p\b[^>]*>", "<p>", h, flags=re.IGNORECASE)
    # Strip a-tag attrs except href
    def clean_a(m):
        attrs = m.group(1)
        href = re.search(r'href="([^"]*)"', attrs, flags=re.IGNORECASE)
        if href:
            return f'<a href="{href.group(1)}">'
        return "<a>"
    h = re.sub(r"<a\b([^>]*)>", clean_a, h, flags=re.IGNORECASE)
    # Strip img tags attrs except src/alt
    def clean_img(m):
        attrs = m.group(1)
        src = re.search(r'src="([^"]*)"', attrs, flags=re.IGNORECASE)
        alt = re.search(r'alt="([^"]*)"', attrs, flags=re.IGNORECASE)
        bits = []
        if src:
            bits.append(f'src="{src.group(1)}"')
        if alt:
            bits.append(f'alt="{alt.group(1)}"')
        return "<img " + " ".join(bits) + " />"
    h = re.sub(r"<img\b([^>]*)/?>", clean_img, h, flags=re.IGNORECASE)
    # Strip table attrs
    h = re.sub(r"<(table|tr|td|th|thead|tbody|ul|ol|li)\b[^>]*>", r"<\1>", h, flags=re.IGNORECASE)
    # Strip empty bold/italic
    h = re.sub(r"<(b|strong|i|em)>\s*</\1>", "", h, flags=re.IGNORECASE)
    # Decode/normalize whitespace
    h = re.sub(r"\s+", " ", h)
    h = re.sub(r">\s+<", "><", h)
    # Re-add line breaks for readability
    h = re.sub(r"</(p|h2|li|ul|ol|table|tr)>", r"</\1>\n", h, flags=re.IGNORECASE)
    return h.strip()


# Now strip out the "FOR IMMEDIATE RELEASE" line and dateline paragraph from body
def strip_release_header(html: str) -> str:
    # Remove any paragraph containing FOR IMMEDIATE RELEASE
    html = re.sub(r"<p\b[^>]*>[^<]*FOR\s+IMMEDIATE\s+RELEASE[^<]*</p>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"FOR\s+IMMEDIATE\s+RELEASE", "", html, flags=re.IGNORECASE)
    return html


results = []
for i, (cs, ce) in enumerate(chunks):
    chunk = cleaned[cs:ce]
    with open(os.path.join(DEBUG_DIR, f"chunk_{i+1:02d}.html"), "w") as f:
        f.write(chunk)

    title = extract_title(chunk)
    dateline, iso_date = extract_dateline_and_date(chunk)
    text_only = tag_text(chunk)
    # Remove title and "FOR IMMEDIATE RELEASE" from text for summary
    summary_source = text_only
    if title:
        summary_source = summary_source.replace(title, "", 1)
    summary_source = re.sub(r"FOR\s+IMMEDIATE\s+RELEASE", "", summary_source, flags=re.IGNORECASE)
    # remove dateline-ish prefix
    summary_source = re.sub(rf"^\s*[A-Z][A-Za-z\.\s]+,\s*[A-Z]{{2,}}\s*[–—\-]+\s*(?:{MONTHS})\s+\d{{1,2}},?\s+\d{{4}}\s*[–—\-:\.\s]*", "", summary_source)
    summary = extract_summary(summary_source.strip())

    body_html = clean_body_html(chunk)
    body_html = strip_release_header(body_html)
    # remove the title heading from body to avoid duplication
    if title:
        body_html = re.sub(r"<h2>\s*" + re.escape(title) + r"\s*</h2>", "", body_html, flags=re.IGNORECASE)

    slug = slugify(title) if title else f"press-release-{i+1}"

    results.append({
        "slug": slug,
        "title": title,
        "summary": summary,
        "publish_date": iso_date,
        "body_html": body_html,
        "pr_dateline": dateline,
    })

with open(OUT, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nWrote {len(results)} releases to {OUT}")
for r in results:
    print(f"  - {r['publish_date']}  {r['title'][:80]}")
