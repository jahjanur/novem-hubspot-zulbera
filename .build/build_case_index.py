#!/usr/bin/env python3
"""Build consolidated anonymized case-studies index from pre-extracted JSON.

The pre-extracted JSON files in .build/json/CASE__*.json were parsed from the
"Anon - *.docx" files in /Users/zulbearijahjanur/Downloads/CASE STUDIES/.
This script verifies anonymization and emits .build/case-studies-index.json.
"""
import json
import re
from pathlib import Path

BUILD = Path("/Users/zulbearijahjanur/Downloads/Novem_HubSpot_Zulbera/.build")
JSON_DIR = BUILD / "json"
OUT = BUILD / "case-studies-index.json"

# Real client names that must NOT appear anywhere in the output
FORBIDDEN = [
    "Bethany", "Riverview",
    "LHRG", "LRHG", "Pioneer Lodge", "Hayes",
    "PNE", "Pacific Coliseum", "Pacific National Exhibition",
    "TELUS", "Telus Garden", "Westbank",
    "Heights Collection", "The Heights",
]

# Map source JSON file -> anonymized slug + industry
# Hand-curated hero-stat overrides. Used when the auto-extracted stats are
# awkward (long phrases, missing a 3rd item, or a non-numeric lede).
STAT_OVERRIDES = {
    "dementia-care-continuous-commissioning": {
        "stat1_num": "$200K+",
        "stat1_lbl": "Annual value unlocked",
        "stat2_num": "$109K",
        "stat2_lbl": "Annual operating savings",
        "stat3_num": "$93K",
        "stat3_lbl": "Wrap-up liability reduction",
    },
    "mixed-use-office-tower-commissioning": {
        "stat1_num": "32 mo",
        "stat1_lbl": "Commissioning time saved (36 to 4 months)",
        "stat2_num": "$10.1M",
        "stat2_lbl": "10-year energy savings forecast",
        "stat3_num": "900+",
        "stat3_lbl": "Building issues found and resolved",
    },
    "events-campus-claim-prevention": {
        "stat1_num": "$5M",
        "stat1_lbl": "Claim prevented",
        "stat2_num": "0%",
        "stat2_lbl": "Annual premium growth",
        "stat3_num": "$400K/yr",
        "stat3_lbl": "Natural gas losses recovered",
    },
    "seniors-living-outbreak-prevention": {
        "stat1_num": "65%",
        "stat1_lbl": "Fewer outbreak weeks",
        "stat2_num": "34%",
        "stat2_lbl": "PPE spend reduction over 3 years",
        "stat3_num": "0",
        "stat3_lbl": "Respiratory outbreaks in 12 months",
    },
    "seniors-housing-insurance-savings": {
        "stat1_num": "10%",
        "stat1_lbl": "Insurance cost reduction",
        "stat2_num": "30%",
        "stat2_lbl": "Digital infrastructure savings",
        "stat3_num": "1%",
        "stat3_lbl": "Total construction cost reduction",
    },
}

ENTRIES = [
    {
        "source": "CASE__Bethany Riverview.json",
        "slug": "dementia-care-continuous-commissioning",
        "industry": "seniors-living",
    },
    {
        "source": "CASE__LHRG Pioneer Lodge.json",
        "slug": "seniors-living-outbreak-prevention",
        "industry": "seniors-living",
    },
    {
        "source": "CASE__PNE Pacific Coliseum.json",
        "slug": "events-campus-claim-prevention",
        "industry": "events-venues",
    },
    {
        "source": "CASE__TELUS Garden.json",
        "slug": "mixed-use-office-tower-commissioning",
        "industry": "mixed-use",
    },
    {
        "source": "CASE__The Heights Collection.json",
        "slug": "seniors-housing-insurance-savings",
        "industry": "seniors-living",
    },
]


def blocks_to_html(blocks):
    """Render the parsed-block JSON (after dropping title + subtitle + metaline)
    into clean HTML with <h2>, <p>, and <ul><li> grouping."""
    out = []
    list_buf = []

    def flush_list():
        nonlocal list_buf
        if list_buf:
            out.append("<ul>")
            out.extend(f"  <li>{li}</li>" for li in list_buf)
            out.append("</ul>")
            list_buf = []

    for b in blocks:
        t = b.get("type")
        html = b.get("html", "").strip()
        if not html:
            continue
        if t == "li":
            list_buf.append(html)
        else:
            flush_list()
            if t == "h2":
                out.append(f"<h2>{html}</h2>")
            else:
                out.append(f"<p>{html}</p>")
    flush_list()
    return "\n".join(out)


def extract_stats(blocks):
    """Find the 'BY THE NUMBERS' section and pull the first 3 stats as
    (num, label) tuples by splitting each list-item on the first natural
    break (em-dash / colon / 'in' / 'reduction' / 'of' phrasing)."""
    in_section = False
    items = []
    for b in blocks:
        t = b.get("type")
        text = b.get("text", "").strip()
        if t == "h2":
            in_section = text.upper().startswith("BY THE NUMBERS")
            if not in_section and items:
                break
            continue
        if in_section and t == "li":
            items.append(text)
    return items[:3]


def parse_stat(line):
    """Best-effort split: pull leading numeric/currency phrase as num,
    rest as label."""
    # Patterns like "$5M ...", "65% ...", "Up to $5M ...", "Zero respiratory..."
    m = re.match(
        r"^(?:Up to\s+|Approximately\s+|More than\s+|Over\s+)?"
        r"([\$\d][\d,\.]*\s*[KMB%]?(?:\s*(?:per year|months?|years?|liters?|weeks?))?)"
        r"\s+(.*)$",
        line,
    )
    if m:
        num = m.group(1).strip()
        lbl = m.group(2).strip().rstrip(".")
        # Trim label to a punchy ~6 words if it's long.
        words = lbl.split()
        if len(words) > 10:
            lbl = " ".join(words[:10]) + "..."
        return num, lbl
    # Fallback for things starting with "Zero"
    m2 = re.match(r"^(Zero\s+\S+)\s+(.*)$", line)
    if m2:
        return m2.group(1), m2.group(2).rstrip(".")
    return line, ""


def derive_summary(blocks):
    """Use the subtitle paragraph (immediately after the title) as summary.
    Trim to ~30 words."""
    # Find first non-empty paragraph after the title (skip metaline starting
    # with 'Solution Provider').
    seen_title = False
    for b in blocks:
        t = b.get("type")
        text = b.get("text", "").strip()
        if not text:
            continue
        if t in ("h1", "h2", "p") and not seen_title:
            seen_title = True
            continue
        if t == "p":
            if text.lower().startswith("solution provider"):
                continue
            words = text.split()
            if len(words) > 35:
                return " ".join(words[:32]).rstrip(",.;:") + "..."
            return text
    return ""


def derive_title(blocks):
    for b in blocks:
        text = b.get("text", "").strip()
        if text:
            return text
    return ""


def check_anonymized(payload):
    """Scan the payload for any forbidden client name."""
    blob = json.dumps(payload, ensure_ascii=False)
    hits = [name for name in FORBIDDEN if re.search(rf"\b{re.escape(name)}\b", blob, re.IGNORECASE)]
    return hits


def main():
    index = []
    for entry in ENTRIES:
        src = JSON_DIR / entry["source"]
        blocks = json.loads(src.read_text(encoding="utf-8"))

        title = derive_title(blocks)
        summary = derive_summary(blocks)
        body_html = blocks_to_html(blocks)
        stats_raw = extract_stats(blocks)
        parsed = [parse_stat(s) for s in stats_raw]
        while len(parsed) < 3:
            parsed.append(("", ""))

        row = {
            "slug": entry["slug"],
            "title": title,
            "summary": summary,
            "industry": entry["industry"],
            "body_html": body_html,
            "stat1_num": parsed[0][0],
            "stat1_lbl": parsed[0][1],
            "stat2_num": parsed[1][0],
            "stat2_lbl": parsed[1][1],
            "stat3_num": parsed[2][0],
            "stat3_lbl": parsed[2][1],
        }
        # Hand-curated hero stats for entries where the auto-split is awkward
        # or the source list is short on numeric ledes.
        overrides = STAT_OVERRIDES.get(entry["slug"])
        if overrides:
            for k, v in overrides.items():
                row[k] = v
        hits = check_anonymized(row)
        if hits:
            raise RuntimeError(f"Anonymization failed for {entry['slug']}: {hits}")
        index.append(row)

    OUT.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(index)} case studies to {OUT}")
    for r in index:
        print(f"  {r['slug']}  ::  {r['title']}")


if __name__ == "__main__":
    main()
