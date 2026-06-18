#!/usr/bin/env python3
"""
Build the resource center artifacts:
  1. /novem-hubspot/hubdb/resources_rows.csv
  2. /novem-hubspot/hubdb/resources_rows.json
  3. /novem-hubspot/src/novem-theme/templates/resources.html (rebuilt cards section)
  4. /novem-hubspot/src/novem-theme/templates/resources/<slug>.html (per resource)
  5. /novem-hubspot/src/novem-theme/templates/resources/README.md

Sources of truth:
  - .build/blog-index.json (17 blog posts)
  - .build/case-studies-index.json (5 anonymized case studies)
  - .build/press-releases-index.json (currently empty; broken source docx)
  - Existing preview PR page for pr-accelerated-commissioning-office-tower (1 PR)
  - White paper text composed from TCRO framework sections per Nicole's brief

NOTE: The user instructions said 8 press releases, but the press-releases-index.json
is empty (the source Press-Releases-v1.3.docx is a corrupted MS sign-in HTML page).
Only the single press release with real body content (extracted from the existing
preview page) is included. The instructions also implied the white paper text was
inline in the prompt — only a stub was provided, so it was composed using the
canonical TCRO framework sections explicitly enumerated in the brief plus the
existing TCRO blog corpus.
"""
import csv
import json
import os
import re
import html as html_lib
from pathlib import Path
from datetime import datetime

ROOT = Path("/Users/zulbearijahjanur/Downloads/Novem_HubSpot_Zulbera")
BUILD = ROOT / ".build"
HUBDB_DIR = ROOT / "novem-hubspot" / "hubdb"
TPL_DIR = ROOT / "novem-hubspot" / "src" / "novem-theme" / "templates"
RES_DIR = TPL_DIR / "resources"
RES_DIR.mkdir(parents=True, exist_ok=True)

# ── Industries / client labels per case-study slug ────────────────────────────
CASE_CLIENT = {
    "dementia-care-continuous-commissioning": "A specialized dementia and long-term care facility",
    "seniors-living-outbreak-prevention":     "A regional seniors living operator (120-resident)",
    "events-campus-claim-prevention":         "A major Western Canadian events and entertainment campus",
    "mixed-use-office-tower-commissioning":   "A landmark mixed-use office tower",
    "seniors-housing-insurance-savings":      "A Western Canadian independent seniors housing developer",
}

# ── Industry tags for blog posts (display-friendly slugs) ─────────────────────
BLOG_INDUSTRY = {
    "tcro-vs-cost-of-risk":               "tcro",
    "data-governance-financial-control":  "data-governance",
    "reactive-to-predictive-maintenance": "predictive-operations",
    "7-criteria-digital-risk-platform":   "digital-risk-platform",
    "insurance-no-longer-fixed-line-item":"insurance",
    "make-data-pay":                      "building-data",
    "tcro-capital-planning":              "capital-planning",
    "tcro-in-the-real-world":             "tcro",
    "tcro-dashboard-for-boards":          "tcro",
    "esg-to-tcro":                        "esg",
    "hidden-wage-cost-of-invisible-risk": "labor-cost",
    "ai-in-the-built-environment":        "ai",
    "tcro-implementation-checklist-cfos": "implementation",
    "best-digital-risk-platforms-2026":   "digital-risk-platform",
    "tcro-roi-seniors-housing":           "seniors-living",
    "tcro-roi-events-entertainment":      "events-venues",
    "tcro-roi-office-mixed-use":          "mixed-use",
}

INDUSTRY_LABEL = {
    "tcro": "TCRO",
    "data-governance": "Data Governance",
    "predictive-operations": "Predictive Operations",
    "digital-risk-platform": "Digital Risk Platform",
    "insurance": "Insurance",
    "building-data": "Building Data",
    "capital-planning": "Capital Planning",
    "esg": "ESG",
    "labor-cost": "Labor Cost",
    "ai": "AI",
    "implementation": "Implementation",
    "seniors-living": "Seniors Living",
    "events-venues": "Events & Entertainment",
    "mixed-use": "Mixed-Use Office",
    "commercial-office": "Commercial Office",
    "white-paper": "TCRO Framework",
    "press-release": "Customer Outcome",
}

CASE_INDUSTRY_LABEL = {
    "seniors-living": "Seniors Living",
    "events-venues": "Events & Entertainment",
    "mixed-use": "Mixed-Use Office",
    "commercial-office": "Commercial Office",
}

# ── Load source indices ───────────────────────────────────────────────────────
with (BUILD / "blog-index.json").open() as f:
    BLOGS = json.load(f)
with (BUILD / "case-studies-index.json").open() as f:
    CASES = json.load(f)

# Single real press release — extracted from existing preview page body
PR_BODY = """<p style="font-size:clamp(1.1rem,1rem + .35vw,1.3rem);color:#D4E8EE;font-style:italic;margin-bottom:2rem;">Novem helps institutional real estate owners identify which building systems are likely to fail, what that failure could cost, and what to fix first to protect cash flow.</p>
<p><strong>VANCOUVER, British Columbia, June 25, 2025</strong> &mdash; Novem Digital helps institutional real estate owners make building failure predictable. The company combines live building data with historical loss data to identify early signs of equipment and system risk, so owners can reduce surprise failures, avoid emergency spend, and make better capital and insurance decisions. Today, Novem Digital announced that its work at a landmark mixed-use office tower helped cut the building&rsquo;s systems startup and stabilization timeline from 36 months to 4 months.</p>
<p>Building systems startup is the process of testing, tuning, and verifying that a building&rsquo;s critical systems &mdash; including HVAC, electrical, controls, and life safety &mdash; are working properly before and after full operations begin. When that process drags on, owners can face delayed stabilization, extended carrying costs, tenant frustration, and hidden performance issues that become expensive later.</p>
<blockquote>For owners and investors, readiness matters because cash flow depends on reliable building performance. Compressing a startup and stabilization timeline from 36 months to 4 months changes the economics of the asset. It improves operational confidence and helps protect asset value.<cite>&mdash; David Crawford, CFO and Head of Capital Planning, Novem Digital</cite></blockquote>
<p>Novem Digital is defining a new category in the market: a Digital Risk Platform for institutional real estate and insurance. In plain terms, that means helping owners move from reactive building management to predictive operations. Instead of waiting for a system to fail, Novem gives leaders earlier visibility into what is at risk, what action matters most, and how to defend those decisions with audit-ready data.</p>
<p>Industry research has found that commissioning can deliver median whole-building energy savings of 13% in new construction and 16% in existing buildings, showing why faster and more effective building startup matters financially, not just operationally. Other industry estimates put delayed occupancy costs for commercial properties at $0.50 to $2.00 per square foot per month in lost revenue, which can quickly turn startup delays into a material cash flow issue.</p>
<p>For owners and investors, that matters because the financial burden of building risk goes well beyond one repair. It includes claims, downtime, emergency repair premiums, insurance volatility, wasted labor, and capital deployed too late. Novem refers to that broader burden as Total Cost of Risk Ownership.</p>
<p>At this mixed-use office tower, Novem Digital helped move the asset from fragmented testing and handover activity to a more continuous, structured, and financially visible process. That shortened the path to dependable building performance and reduced the period where system underperformance could put revenue readiness and asset value at risk.</p>
<blockquote>In institutional real estate, a long building startup cycle is not just an engineering issue. It is a financial issue. When a building takes years to stabilize, owners absorb delay, uncertainty, and avoidable cost. Novem helps make that risk visible early enough to act on it.<cite>&mdash; Clint Undseth, CEO, Novem Digital</cite></blockquote>
<p>The result strengthens Novem Digital&rsquo;s position in mixed-use office, institutional commercial real estate, and complex urban developments where leaders need more confidence in capital timing, operational readiness, and the financial consequences of underperformance. It also reinforces the company&rsquo;s belief that risk should never be invisible &mdash; because what owners cannot see often becomes what they end up paying for.</p>
<p>Novem Digital is headquartered in Vancouver, Canada.</p>
<h2>Notes to Editors</h2>
<p>Customer outcome data referenced in this release &mdash; including the reduction in building systems startup timeline from 36 months to 4 months &mdash; is Novem Digital proprietary client data. External statistics are sourced as follows:</p>
<ul>
  <li>Building commissioning energy savings benchmark (13% new construction / 16% existing buildings) &mdash; Lawrence Berkeley National Laboratory, &ldquo;Building Commissioning Costs and Savings Across Three Decades and 1,500 North American Buildings.&rdquo;</li>
  <li>Delayed occupancy cost range ($0.50&ndash;$2.00 per sq ft per month) &mdash; PingCx, &ldquo;The Hidden Costs of Manual Commissioning in Today&rsquo;s Complex Buildings&rdquo; (May 2025).</li>
</ul>
<h2>About Novem Digital</h2>
<p>Novem Digital is an AI-powered digital risk platform that makes building failure predictable for institutional real estate portfolios. Novem predicts and prevents equipment failures before they happen by combining real-time monitoring with historical insurance claims data from millions of buildings. Customers reduce Total Cost of Risk Ownership, protect cash flow, and manage risk-related costs with confidence across operations, capital planning, and insurance.</p>"""

PRESS_RELEASES = [{
    "slug": "pr-accelerated-commissioning-office-tower",
    "title": "From 36 Months to 4 Months: Novem Digital Helps Landmark Mixed-Use Office Tower Accelerate Building Systems Startup by Nearly 89%",
    "summary": "Novem helps institutional real estate owners identify which building systems are likely to fail, what that failure could cost, and what to fix first to protect cash flow.",
    "publish_date": "2025-06-25",
    "body_html": PR_BODY,
    "pr_dateline": "VANCOUVER, British Columbia — June 25, 2025",
    "industry": "press-release",
}]

# White paper — composed from the framework sections enumerated in the brief
# (Executive Summary, Key Findings, The Problem Is Structural, From Cost of Risk
# to TCRO, The TCRO Framework, Financial Case for a CFO, Make Data Pay, Proof,
# What Adoption Looks Like, Conclusion) plus three case-study excerpts.
WP_BODY = """<h2>Executive Summary</h2>
<p>Institutional real estate is at an inflection point. Insurance markets are harder, emergency repair costs are higher, and boards, lenders, and regulators all want more proof that risk is being managed, not just absorbed. The financial standard most organizations still use to think about risk — Cost of Risk — was built for insurers. It is too narrow for owners.</p>
<p>Total Cost of Risk Ownership (TCRO) is the wider lens. It follows the money through losses, downtime, premiums, operating inefficiency, and governance overhead. Backed by live building data and a common data environment, TCRO turns risk from a report you defend into a number you can move.</p>
<p>This paper defines TCRO, explains why the shift is happening now, and shows what adoption looks like in practice — with three anonymized case studies where owners turned risk visibility into measurable financial outcomes.</p>

<h2>Key Findings</h2>
<ul>
  <li>One avoidable major equipment failure can carry several times its direct repair cost once downtime, emergency work, premium spend, and reputational impact are included. Most of that bill never appears in Cost of Risk.</li>
  <li>Portfolios with continuous monitoring on critical systems can hold property insurance premium growth at <strong>0% in a hard market</strong> by giving underwriters evidence of active control.</li>
  <li>A digital risk platform layered on existing building systems can compress commissioning timelines from a typical <strong>36-month cycle to roughly 4 months</strong>, while avoiding ~2% of infrastructure capital spend.</li>
  <li>In care environments, predictive air-quality and ventilation control can produce <strong>65% fewer outbreak weeks</strong> and a <strong>34% reduction in PPE spending</strong> over three years.</li>
</ul>

<h2>The Problem Is Structural, Not Occasional</h2>
<p>Most owners experience risk as a series of bad days: a chiller fails, an outbreak hits a community, a leak ruins a tenant space. The instinct is to treat each as an isolated event. The reality is that these events are the visible surface of a structural problem.</p>
<p>That structural problem has three drivers:</p>
<ul>
  <li>Building data is fragmented across BMS, CMMS, sensors, spreadsheets, and PDFs — so failure patterns are invisible until they break the surface.</li>
  <li>Risk is reported in a vocabulary insurers built for themselves (Cost of Risk) — narrow, backward-looking, and indifferent to most of what failures actually cost an owner.</li>
  <li>Capital planning still runs on asset age, not on risk-weighted economics — so capital is deployed too early in some places and far too late in others.</li>
</ul>
<p>The cost of this structural problem is rarely a single line item. It is the sum of small inefficiencies, surprise failures, emergency premiums, and avoidable wage costs that erode NOI and weaken the story you can tell at the board and at renewal.</p>

<h2>From Cost of Risk to Total Cost of Risk Ownership</h2>
<p>Cost of Risk measures what risk costs the insurer — premiums, broker fees, retained claims, and loss-control spend. TCRO measures what risk costs the owner.</p>
<p>For an institutional real estate portfolio, that broader number includes:</p>
<ul>
  <li><strong>Losses and claims</strong> — direct incident and claim costs.</li>
  <li><strong>Downtime and business interruption</strong> — revenue and service impact when systems are down.</li>
  <li><strong>Premiums and retentions</strong> — insurance spend and retained risk.</li>
  <li><strong>Operating and maintenance inefficiency</strong> — reactive work, wasted labor, emergency premiums.</li>
  <li><strong>Compliance and reporting burden</strong> — the time and cost of proving control.</li>
  <li><strong>Indirect reputational and governance costs</strong> — the trust hit when things go wrong.</li>
</ul>
<p>Cost of Risk is a slice. TCRO is the bill.</p>

<h2>The TCRO Framework</h2>
<p>TCRO is built on four practical elements:</p>
<h3>1. A common data environment</h3>
<p>One source of truth for what you own, what is at risk, and what failure costs. That means a complete, risk-aware asset inventory, normalized definitions across finance, operations, and risk, and traceable lineage from raw signals to board-level KPIs.</p>
<h3>2. Continuous risk signal</h3>
<p>Monitoring on the systems and conditions where failures hurt most — vibration on critical motors, leak and flow detection on high-risk water lines, air-quality and environmental data in care environments, gas detection on aging infrastructure.</p>
<h3>3. Closed-loop workflows</h3>
<p>Every signal triggers a clear, prioritized intervention. Every intervention is logged. Every outcome — failure prevented, claim avoided, hours saved — feeds back into the model. Without this loop, you have alerts, not risk management.</p>
<h3>4. A financial vocabulary</h3>
<p>Every alert, every project, every renewal is expressed in TCRO terms: what risk is being addressed, what it would cost if untreated, what intervention costs, and what the net impact is. This is the language CFOs, boards, brokers, and underwriters share.</p>

<h2>The Financial Case for a CFO</h2>
<p>TCRO changes three financial conversations:</p>
<ul>
  <li><strong>Capital planning</strong> moves from age-based replacement to risk-weighted investment. Capital flows to assets where the TCRO reduction per dollar is highest.</li>
  <li><strong>Insurance</strong> stops being a fixed line item. Continuous evidence of control becomes the basis for performance-based program design and pricing.</li>
  <li><strong>Board reporting</strong> shifts from defending failures to allocating against a forward TCRO plan. Directors see a small, stable set of metrics — TCRO level, trend, drivers, avoided losses, capital alignment — that connect today's decisions to tomorrow's outcomes.</li>
</ul>
<p>For a finance leader, that is the difference between absorbing risk-related costs and engineering them down.</p>

<h2>Make Data Pay</h2>
<p>Most portfolios already have the raw material — building systems, work orders, sensors, claims, inspections. The asset is stranded because it sits in silos, with no common definitions and no clear financial frame.</p>
<p>When data is governed and connected to TCRO, three categories of return appear:</p>
<ul>
  <li><strong>Cost avoidance</strong> — claims that never occur, emergency callouts that never get booked, outbreaks that never happen.</li>
  <li><strong>Cost reduction</strong> — lower utility bills through leak detection and better controls, lower insurance premiums over time, less maintenance waste.</li>
  <li><strong>Value protection and upside</strong> — more predictable NOI, stronger ESG and resilience stories for lenders and investors, higher confidence in capital plans.</li>
</ul>
<p>This is what "make data pay" means in TCRO terms: the same building data that supports operations also lowers risk-related costs and supports stronger capital and insurance outcomes.</p>

<h2>Proof</h2>
<p>TCRO is not theoretical. Three anonymized client examples illustrate what adoption looks like in practice.</p>

<blockquote>
  <strong>Specialized dementia and long-term care facility.</strong> Automated continuous commissioning on the Digital Risk Platform identified uncommissioned drives, misconfigured rooftop units, and under-performing heat exchangers. The result: <strong>$93K reduction in handover costs</strong> (lower wrap-up liability exposure) and <strong>$109,326 in annual operating savings</strong> — six figures unlocked from data the building was already producing.
</blockquote>

<blockquote>
  <strong>Major Western Canadian events and entertainment campus.</strong> Layering monitoring on pumps, motors, gas, water, and environmental conditions across a 50-year-old multi-building campus prevented a <strong>maximum probable loss of up to $5M</strong> from a single vibration alert on a critical motor. The program also uncovered a previously invisible <strong>natural gas leak worth over $400K per year</strong> and held <strong>property insurance premium growth at 0%</strong> in a rising market.
</blockquote>

<blockquote>
  <strong>Landmark mixed-use office tower.</strong> Automated continuous commissioning reduced startup from the typical <strong>36-month cycle to approximately 4 months</strong>, eliminated infrastructure redundancies (saving ~2% of capital), and delivered a <strong>10-year forecast energy savings of $10.1M</strong> — over 900 building issues identified and resolved to 10 with clear repair paths.
</blockquote>

<p>The common pattern: invisible risk is made visible, signals are tied to financial outcomes, and Total Cost of Risk Ownership is engineered down — not absorbed.</p>

<h2>What Adoption Looks Like</h2>
<p>Adopting TCRO is a sequence, not a switch.</p>
<ul>
  <li><strong>Scope and target.</strong> Choose one flagship asset, one campus, or one asset class. Define what TCRO target you are pursuing.</li>
  <li><strong>Baseline.</strong> Build a first-pass TCRO model with your own assumptions for losses, downtime, premiums, operating inefficiency, and governance overhead. Even rough numbers reveal where to focus.</li>
  <li><strong>Govern.</strong> Assign data owners. Standardize definitions for incidents, failures, outages, and interventions. Put a common data environment in place — even a simple one.</li>
  <li><strong>Instrument.</strong> Deploy targeted monitoring on the systems where a single failure could move TCRO meaningfully. Integrate signals with work orders so alerts trigger real action.</li>
  <li><strong>Close the loop.</strong> Track avoided losses and prevented failures in financial terms. Recalculate TCRO periodically. Use the evidence in capital planning and insurance renewals.</li>
  <li><strong>Scale.</strong> Extend to more assets, more asset classes, and more risk domains. Make TCRO part of how the portfolio is run, not a one-off model.</li>
</ul>

<h2>Conclusion</h2>
<p>The built environment is moving from "how fast do we recover from failures" to "how precisely do we price and prevent them." TCRO is the financial standard for that shift. It gives owners a number they can defend, a number they can move, and a number that connects directly to the people who live, work, and spend time in their buildings.</p>
<p>Behind every avoided failure is a resident who does not lose heat in winter, a care team that does not work a crisis shift, a visitor whose event is not cancelled. TCRO is how that human impact shows up in the financials.</p>
<p>Failures are predictable. What changes is whether you are positioned to act on them first.</p>

<h2>About Novem Digital</h2>
<p>Novem Digital is an AI-powered digital risk platform that transforms operational data from real estate into measurable financial returns. Novem predicts and prevents equipment failures before they happen so leaders can reduce Total Cost of Risk Ownership, protect cash flow, and manage risk-related costs with confidence. Headquartered in Vancouver, Canada. Serving institutional real estate portfolios globally.</p>"""

WHITE_PAPERS = [{
    "slug": "total-cost-of-risk-ownership-white-paper",
    "title": "Total Cost of Risk Ownership",
    "subtitle": "The financial standard for institutional real estate, and the framework that turns building data into a strategic asset.",
    "summary": "The TCRO framework — define, quantify, and defend the complete cost of building risk across an institutional portfolio.",
    "publish_date": "2026-06-01",
    "body_html": WP_BODY,
    "industry": "white-paper",
}]

# ── Industry assignment for case studies (from source) ────────────────────────
CASE_INDUSTRY = {c["slug"]: c.get("industry", "") for c in CASES}

# ── Build canonical row list ──────────────────────────────────────────────────
def make_blog_row(b):
    slug = b["slug"]
    ind = BLOG_INDUSTRY.get(slug, "tcro")
    return {
        "title": b["title"],
        "slug": slug,
        "type": "blog",
        "client": "",
        "industry": ind,
        "publish_date": b["publish_date"],
        "summary": b["summary"],
        "body": b["body_html"],
        "results": "",
        "hero_image": "",
        "stat1_num": "", "stat1_label": "",
        "stat2_num": "", "stat2_label": "",
        "stat3_num": "", "stat3_label": "",
        "seo_title": b["title"],
        "seo_description": b["summary"],
        "og_image": "",
    }

def make_case_row(c):
    slug = c["slug"]
    return {
        "title": c["title"],
        "slug": slug,
        "type": "case-study",
        "client": CASE_CLIENT.get(slug, ""),
        "industry": c.get("industry", ""),
        "publish_date": "2026-06-11",
        "summary": c["summary"],
        "body": c["body_html"],
        "results": "",
        "hero_image": "",
        "stat1_num": c.get("stat1_num", ""), "stat1_label": c.get("stat1_lbl", ""),
        "stat2_num": c.get("stat2_num", ""), "stat2_label": c.get("stat2_lbl", ""),
        "stat3_num": c.get("stat3_num", ""), "stat3_label": c.get("stat3_lbl", ""),
        "seo_title": c["title"],
        "seo_description": c["summary"],
        "og_image": "",
    }

def make_pr_row(p):
    return {
        "title": p["title"],
        "slug": p["slug"],
        "type": "press-release",
        "client": "",
        "industry": "mixed-use",
        "publish_date": p["publish_date"],
        "summary": p["summary"],
        "body": p["body_html"],
        "results": "",
        "hero_image": "",
        "stat1_num": "", "stat1_label": "",
        "stat2_num": "", "stat2_label": "",
        "stat3_num": "", "stat3_label": "",
        "seo_title": p["title"],
        "seo_description": p["summary"],
        "og_image": "",
    }

def make_wp_row(w):
    return {
        "title": w["title"],
        "slug": w["slug"],
        "type": "white-paper",
        "client": "",
        "industry": "white-paper",
        "publish_date": w["publish_date"],
        "summary": w["summary"],
        "body": w["body_html"],
        "results": "",
        "hero_image": "",
        "stat1_num": "", "stat1_label": "",
        "stat2_num": "", "stat2_label": "",
        "stat3_num": "", "stat3_label": "",
        "seo_title": w["title"],
        "seo_description": w["summary"],
        "og_image": "",
    }

rows = []
rows += [make_wp_row(w)   for w in WHITE_PAPERS]
rows += [make_case_row(c) for c in CASES]
rows += [make_blog_row(b) for b in BLOGS]
rows += [make_pr_row(p)   for p in PRESS_RELEASES]

# ── ARTIFACT 1: CSV ───────────────────────────────────────────────────────────
COLUMNS = ["title","slug","type","client","industry","publish_date","summary","body","results","hero_image",
           "stat1_num","stat1_label","stat2_num","stat2_label","stat3_num","stat3_label",
           "seo_title","seo_description","og_image"]
csv_path = HUBDB_DIR / "resources_rows.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLUMNS, quoting=csv.QUOTE_ALL)
    w.writeheader()
    for r in rows:
        w.writerow(r)

# ── ARTIFACT 2: JSON (HubDB Rows API shape) ───────────────────────────────────
def to_api_row(r):
    return {
        "path": r["slug"],
        "name": r["title"],
        "values": {k: v for k, v in r.items() if v != ""},
    }
api_rows = [to_api_row(r) for r in rows]
json_path = HUBDB_DIR / "resources_rows.json"
with json_path.open("w", encoding="utf-8") as f:
    json.dump(api_rows, f, indent=2, ensure_ascii=False)

# ── ARTIFACT 3: Rebuild resources.html cards ──────────────────────────────────
RES_HTML = TPL_DIR / "resources.html"
src = RES_HTML.read_text(encoding="utf-8")

# Find the region: from the first <!-- ── CASE STUDIES ── --> comment to the
# closing </div> just before <!-- ═══ FAQ ═══ -->. We rebuild everything inside.
start_marker = "        <!-- ── CASE STUDIES ── -->"
end_marker   = "  </div>\n</section>\n\n<!-- ═══ FAQ ═══ -->"
i = src.find(start_marker)
j = src.find(end_marker)
if i < 0 or j < 0:
    raise SystemExit(f"Could not find card region markers in resources.html (i={i} j={j})")

def card_link_label(t):
    return {"case-study":"Read case study","white-paper":"Read white paper",
            "blog":"Read article","press-release":"Read press release"}.get(t, "Read")

def card_badge_class(t):
    return {"case-study":"rcard-badge--cs","white-paper":"rcard-badge--wp",
            "blog":"rcard-badge--bl","press-release":"rcard-badge--pr"}[t]

def card_industry_color(t):
    return {"case-study":"","white-paper":"var(--wp)","blog":"var(--bl)","press-release":"var(--pr)"}[t]

def card_bg(t):
    color = {"case-study":"#7BFAB533","white-paper":"#60BCD633",
             "blog":"#B8A0E833","press-release":"#60BCD633"}[t]
    return f"background:radial-gradient(130% 130% at 75% 12%,{color} 0%,transparent 55%),linear-gradient(150deg,#0c1419 0%,#162a33 55%,#0c1419 100%);"

def render_industry_label(r):
    t = r["type"]
    ind_key = r["industry"] or ""
    if t == "case-study":
        return CASE_INDUSTRY_LABEL.get(ind_key, ind_key.replace("-"," ").title() or "Institutional Real Estate")
    if t == "blog":
        return INDUSTRY_LABEL.get(ind_key, ind_key.replace("-"," ").title())
    if t == "white-paper":
        return "TCRO Framework"
    if t == "press-release":
        return "Customer Outcome"
    return "Resource"

def card_html(r):
    t = r["type"]
    badge_class = card_badge_class(t)
    badge_label = {"case-study":"Case Study","white-paper":"White Paper",
                   "blog":"Blog","press-release":"Press Release"}[t]
    industry_color = card_industry_color(t)
    industry_style = f' style="color:{industry_color};"' if industry_color else ""
    industry_label_html = html_lib.escape(render_industry_label(r))

    # Meta row varies by type
    meta_parts = [f'<span class="rcard-industry"{industry_style}>{industry_label_html}</span>']
    if t == "blog":
        meta_parts.append('<span class="rcard-dot"></span>')
        meta_parts.append('<span class="rcard-date">5 min read</span>')
    elif t == "press-release" and r.get("publish_date"):
        try:
            d = datetime.strptime(r["publish_date"], "%Y-%m-%d")
            meta_parts.append('<span class="rcard-dot"></span>')
            meta_parts.append(f'<span class="rcard-date">{d.strftime("%B %d, %Y")}</span>')
        except Exception:
            pass

    # Stats strip — only case studies have these
    stats_html = ""
    if t == "case-study":
        items = []
        for n, l in [(r.get("stat1_num"), r.get("stat1_label")),
                     (r.get("stat2_num"), r.get("stat2_label"))]:
            if n and l:
                items.append(f'<div><div class="rcard-stat-num">{html_lib.escape(n)}</div><div class="rcard-stat-lbl">{html_lib.escape(l)}</div></div>')
        if items:
            stats_html = f'\n          <div class="rcard-stats">\n            {"".join(items)}\n          </div>'

    # Badge — case-study and white-paper use rcard-badge classes; blog/PR use color override style
    if t in ("case-study", "white-paper", "press-release"):
        badge_html = f'<span class="rcard-badge {badge_class}">{badge_label}</span>'
    else:  # blog gets violet override
        badge_html = '<span class="rcard-badge" style="background:color-mix(in srgb,var(--bl,#B8A0E8) 80%,#000);color:#fff;">Blog</span>'

    link_label = card_link_label(t)
    link_style = ' style="margin-top:auto;"' if t in ("blog","press-release","white-paper") else ""

    return f'''      <a class="rcard rev" data-type="{t}" href="/resources/{r["slug"]}/" target="_blank" rel="noopener noreferrer">
        <div class="rcard-img" style="{card_bg(t)}">
          {badge_html}
        </div>
        <div class="rcard-body">
          <div class="rcard-meta">{"".join(meta_parts)}</div>
          <h3 class="rcard-title">{html_lib.escape(r["title"])}</h3>
          <p class="rcard-excerpt">{html_lib.escape(r["summary"])}</p>{stats_html}
          <span class="rcard-link"{link_style}>{link_label} <svg width="13" height="13" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
        </div>
      </a>'''

def section_block(label, divider_class, type_value, items_html):
    return f'''        <!-- ── {label.upper()} ── -->
    <div class="section-divider {divider_class} content-section" data-section="{type_value}"{' style="margin-top:1rem;"' if type_value != "white-paper" else ' style="margin-top:1rem;"'}>
      <span class="section-divider-label">{label}</span>
      <span class="section-divider-line"></span>
    </div>

    <div class="resource-grid content-section" data-section="{type_value}">

{items_html}

    </div>
'''

wp_rows = [r for r in rows if r["type"] == "white-paper"]
cs_rows = [r for r in rows if r["type"] == "case-study"]
bl_rows = [r for r in rows if r["type"] == "blog"]
pr_rows = [r for r in rows if r["type"] == "press-release"]

def join_cards(lst):
    return "\n\n".join(card_html(r) for r in lst)

new_region_parts = []
# White paper first
new_region_parts.append(section_block("White Papers", "section-divider--wp", "white-paper", join_cards(wp_rows)))
# Case studies
new_region_parts.append(section_block("Case Studies", "section-divider--cs", "case-study", join_cards(cs_rows)))
# Blog
new_region_parts.append(section_block("Blog", "section-divider--bl", "blog", join_cards(bl_rows)))
# Press releases
new_region_parts.append(section_block("Press Releases", "section-divider--pr", "press-release", join_cards(pr_rows)))

# Fix the first section's leading indentation: the existing markup begins each
# block with eight spaces before the divider comment. We've matched that.
new_region = "".join(new_region_parts).rstrip() + "\n\n  </div>\n</section>\n\n<!-- ═══ FAQ ═══ -->"

new_src = src[:i] + new_region + src[j + len(end_marker):]
RES_HTML.write_text(new_src, encoding="utf-8")

# ── ARTIFACT 4: Per-resource sub-templates ────────────────────────────────────
BLOG_TPL  = (TPL_DIR / "resource-blog.html").read_text(encoding="utf-8")
CASE_TPL  = (TPL_DIR / "resource-case-study.html").read_text(encoding="utf-8")
PR_TPL    = (TPL_DIR / "resource-press-release.html").read_text(encoding="utf-8")
WP_TPL    = (TPL_DIR / "resource-whitepaper.html").read_text(encoding="utf-8")

def upgrade_cdn(s):
    return s.replace("NovemZulbera_24", "NovemZulbera_25")

def replace_templatetype_header(s, type_label, title):
    """Replace the leading templateType comment with label + isAvailableForNewContent: false."""
    new = f'''<!--
  templateType: page
  label: "{type_label}: {title}"
  isAvailableForNewContent: false
-->'''
    return re.sub(r"<!--\s*templateType:.*?-->", new, s, count=1, flags=re.DOTALL)

def replace_meta(s, title, summary, slug, publish_date):
    """Replace <title>, og:*, twitter:*, canonical and article:published_time."""
    esc_title = html_lib.escape(title, quote=True)
    esc_summary = html_lib.escape(summary, quote=True)
    s = re.sub(r"<title>.*?</title>", f"<title>{esc_title} | Novem Digital</title>", s, count=1, flags=re.DOTALL)
    s = re.sub(r'<meta name="description" content="[^"]*"',
               f'<meta name="description" content="{esc_summary}"', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*"',
               f'<meta property="og:title" content="{esc_title}"', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*"',
               f'<meta property="og:description" content="{esc_summary}"', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*"',
               f'<meta property="og:url" content="https://novemdigital.com/resources/{slug}/"', s, count=1)
    s = re.sub(r'<meta name="twitter:title" content="[^"]*"',
               f'<meta name="twitter:title" content="{esc_title}"', s, count=1)
    s = re.sub(r'<meta name="twitter:description" content="[^"]*"',
               f'<meta name="twitter:description" content="{esc_summary}"', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*"',
               f'<link rel="canonical" href="/resources/{slug}/"', s, count=1)
    if publish_date:
        s = re.sub(r'<meta property="article:published_time" content="[^"]*"',
                   f'<meta property="article:published_time" content="{publish_date}"', s, count=1)
    return s

def replace_body_section(s, body_pattern, replacement):
    return re.sub(body_pattern, replacement, s, count=1, flags=re.DOTALL)

# ── BLOG template builder ────────────────────────────────────────────────────
def build_blog_template(r):
    s = BLOG_TPL
    s = upgrade_cdn(s)
    s = replace_templatetype_header(s, "Blog", r["title"])
    s = replace_meta(s, r["title"], r["summary"], r["slug"], r["publish_date"])

    # Replace the hero <h1>
    s = re.sub(r'<h1 class="h1" style="max-width:18ch;">[^<]*(?:<[^>]+>[^<]*)*</h1>',
               f'<h1 class="h1" style="max-width:24ch;">{html_lib.escape(r["title"])}</h1>',
               s, count=1, flags=re.DOTALL)

    # Replace the meta bar (pr-meta block) — keep structure, just update date
    try:
        d = datetime.strptime(r["publish_date"], "%Y-%m-%d")
        date_str = d.strftime("%B %-d, %Y")
    except Exception:
        date_str = "June 2026"
    s = re.sub(
        r'<div class="pr-meta">\s*<span class="pr-badge badge--blog">Blog</span>\s*<span class="pr-date">[^<]*</span>\s*<span class="pr-read">[^<]*</span>\s*<span class="pr-author">[^<]*</span>\s*</div>',
        f'<div class="pr-meta">\n      <span class="pr-badge badge--blog">Blog</span>\n      <span class="pr-date">{date_str}</span>\n      <span class="pr-read">6 min read</span>\n      <span class="pr-author">By Novem Digital</span>\n    </div>',
        s, count=1, flags=re.DOTALL)

    # Replace the tag-strip — use the industry label
    ind = INDUSTRY_LABEL.get(r["industry"], "TCRO")
    s = re.sub(
        r'<div class="tag-strip">.*?</div>',
        f'<div class="tag-strip"><span class="tag">{html_lib.escape(ind)}</span><span class="tag">Institutional Real Estate</span><span class="tag">TCRO</span></div>',
        s, count=1, flags=re.DOTALL)

    # Replace the entire <div class="art-body"> ... </div> block
    body_inner = f'      <h2 style="margin-top:0;">{html_lib.escape(r["title"])}</h2>\n      <p style="font-size:clamp(1.1rem,1rem + .35vw,1.3rem);color:#D4E8EE;font-style:italic;margin-bottom:2rem;">{html_lib.escape(r["summary"])}</p>\n\n      {r["body"]}'
    s = re.sub(r'<div class="art-body">.*?</div>\s*\n\s*<!-- CTA Box -->',
               f'<div class="art-body">\n{body_inner}\n    </div>\n\n    <!-- CTA Box -->',
               s, count=1, flags=re.DOTALL)
    return s

# ── CASE-STUDY template builder ──────────────────────────────────────────────
def build_case_template(r):
    s = CASE_TPL
    s = upgrade_cdn(s)
    s = replace_templatetype_header(s, "Case Study", r["title"])
    s = replace_meta(s, r["title"], r["summary"], r["slug"], r["publish_date"])

    # Replace the hero <h1>
    s = re.sub(r'<h1 style="font-family:var\(--font-h\)[^"]*"[^>]*>.*?</h1>',
               f'<h1 style="font-family:var(--font-h);font-size:clamp(2.4rem,1.4rem + 4.5vw,4.5rem);font-weight:700;line-height:1.05;color:var(--text);max-width:22ch;">{html_lib.escape(r["title"])}</h1>',
               s, count=1, flags=re.DOTALL)

    # Replace art-meta
    industry_label = CASE_INDUSTRY_LABEL.get(r["industry"], r["industry"].replace("-"," ").title())
    client = r["client"] or "Institutional Real Estate Portfolio"
    s = re.sub(
        r'<div class="art-meta">.*?</div>',
        f'<div class="art-meta">\n      <span class="badge badge--cs">Case Study</span>\n      <span class="art-date">{html_lib.escape(industry_label)}</span>\n      <span class="art-location">{html_lib.escape(client)}</span>\n      <span class="art-read">6 min read</span>\n    </div>',
        s, count=1, flags=re.DOTALL)

    # Build stats strip from row stats
    stat_cells = []
    for n, l in [(r.get("stat1_num"), r.get("stat1_label")),
                 (r.get("stat2_num"), r.get("stat2_label")),
                 (r.get("stat3_num"), r.get("stat3_label"))]:
        if n and l:
            stat_cells.append(f'      <div class="stat-cell">\n        <div class="stat-num">{html_lib.escape(n)}</div>\n        <div class="stat-lbl">{html_lib.escape(l)}</div>\n      </div>')
    new_stats = '<div class="stats-strip">\n' + "\n".join(stat_cells) + '\n    </div>'

    # Replace existing stats-strip
    s = re.sub(r'<div class="stats-strip">.*?</div>\s*\n\s*<div class="art-body">',
               f'{new_stats}\n\n    <div class="art-body">',
               s, count=1, flags=re.DOTALL)

    # Replace the FIRST art-body intro block
    intro = f'      <p class="lg" style="color:#D4E8EE;margin-bottom:2rem;"><em>{html_lib.escape(r["summary"])}</em></p>'
    s = re.sub(r'<div class="art-body">\s*<h2>[^<]+</h2>\s*<p class="lg"[^>]*>.*?</p>.*?</div>\s*\n\s*<!-- Stats strip -->',
               f'<div class="art-body">\n{intro}\n    </div>\n\n    <!-- Stats strip -->',
               s, count=1, flags=re.DOTALL)

    # Replace the SECOND art-body (the long body section)
    s = re.sub(r'<div class="art-body">\s*<h2>The Challenge</h2>.*?</div>\s*\n\s*<div class="cta-box">',
               f'<div class="art-body">\n{r["body"]}\n    </div>\n\n    <div class="cta-box">',
               s, count=1, flags=re.DOTALL)
    return s

# ── PRESS-RELEASE template builder ───────────────────────────────────────────
def build_pr_template(r):
    s = PR_TPL
    s = upgrade_cdn(s)
    s = replace_templatetype_header(s, "Press Release", r["title"])
    s = replace_meta(s, r["title"], r["summary"], r["slug"], r["publish_date"])

    # Hero h1
    s = re.sub(r'<h1 class="h1" style="max-width:14ch;">[^<]*(?:<[^>]+>[^<]*)*</h1>',
               f'<h1 class="h1" style="max-width:24ch;">{html_lib.escape(r["title"])}</h1>',
               s, count=1, flags=re.DOTALL)

    # Meta bar
    try:
        d = datetime.strptime(r["publish_date"], "%Y-%m-%d")
        date_str = d.strftime("%B %-d, %Y")
    except Exception:
        date_str = r["publish_date"] or ""
    s = re.sub(
        r'<div class="pr-meta">\s*<span class="pr-badge">Press Release</span>\s*<span class="pr-date">[^<]*</span>\s*<span class="pr-location">[^<]*</span>\s*</div>',
        f'<div class="pr-meta">\n      <span class="pr-badge">Press Release</span>\n      <span class="pr-date">{date_str}</span>\n      <span class="pr-location">Vancouver, BC, Canada</span>\n    </div>',
        s, count=1, flags=re.DOTALL)

    # Replace the pr-body
    s = re.sub(r'<div class="pr-body">.*?</div>\s*\n\s*<!-- CTA -->',
               f'<div class="pr-body">\n{r["body"]}\n    </div>\n\n    <!-- CTA -->',
               s, count=1, flags=re.DOTALL)
    return s

# ── WHITE-PAPER template builder ─────────────────────────────────────────────
def build_wp_template(r):
    s = WP_TPL
    s = upgrade_cdn(s)
    s = replace_templatetype_header(s, "White Paper", r["title"])
    s = replace_meta(s, r["title"], r["summary"], r["slug"], r["publish_date"])

    # Hero h1
    s = re.sub(r'<h1 class="h1" style="max-width:16ch;">[^<]*(?:<[^>]+>[^<]*)*</h1>',
               f'<h1 class="h1" style="max-width:22ch;">{html_lib.escape(r["title"])}</h1>',
               s, count=1, flags=re.DOTALL)

    # Meta bar (white paper)
    try:
        d = datetime.strptime(r["publish_date"], "%Y-%m-%d")
        date_str = d.strftime("%B %Y")
    except Exception:
        date_str = "June 2026"
    s = re.sub(
        r'<div class="pr-meta">\s*<span class="pr-badge badge--wp">White Paper</span>\s*<span class="pr-date">[^<]*</span>\s*<span class="pr-pages">[^<]*</span>\s*</div>',
        f'<div class="pr-meta">\n      <span class="pr-badge badge--wp">White Paper</span>\n      <span class="pr-date">{date_str}</span>\n      <span class="pr-pages">White Paper</span>\n    </div>',
        s, count=1, flags=re.DOTALL)

    # Title block
    s = re.sub(
        r'<div style="margin-bottom:3rem;">\s*<h2 style="font-family:var\(--font-h\)[^"]*"[^>]*>.*?</h2>\s*<p style="[^"]*">.*?</p>\s*</div>',
        f'<div style="margin-bottom:3rem;">\n      <h2 style="font-family:var(--font-h);font-size:clamp(1.6rem,1.2rem + 2vw,2.6rem);font-weight:700;color:var(--text);line-height:1.15;margin-bottom:1rem;">{html_lib.escape(r["title"])}</h2>\n      <p style="font-size:clamp(1.1rem,1rem + .35vw,1.3rem);color:var(--muted);line-height:1.6;max-width:56ch;">{html_lib.escape(WHITE_PAPERS[0]["subtitle"])}</p>\n    </div>',
        s, count=1, flags=re.DOTALL)

    # Replace art-body — drop exec summary card, findings grid, sec-rule
    # Match from <div class="exec-summary"> through the </div> right before <!-- CTA Box -->
    s = re.sub(
        r'<div class="exec-summary">.*?</div>\s*</div>\s*\n\s*<!-- CTA Box -->',
        f'<div class="art-body">\n{r["body"]}\n    </div>\n\n    <!-- CTA Box -->',
        s, count=1, flags=re.DOTALL)
    return s

generated = []
issues = []

for r in rows:
    out = RES_DIR / f'{r["slug"]}.html'
    try:
        if r["type"] == "blog":
            html_out = build_blog_template(r)
        elif r["type"] == "case-study":
            html_out = build_case_template(r)
        elif r["type"] == "press-release":
            html_out = build_pr_template(r)
        elif r["type"] == "white-paper":
            html_out = build_wp_template(r)
        else:
            issues.append(f"Unknown type for {r['slug']}: {r['type']}")
            continue
        out.write_text(html_out, encoding="utf-8")
        generated.append(str(out))
    except Exception as e:
        issues.append(f"FAIL {r['slug']}: {e}")

# ── ARTIFACT 5: README for marketing team ────────────────────────────────────
readme_lines = [
    "# Resource Center Sub-Templates",
    "",
    "Each file in this directory is a HubSpot page template for a single resource",
    "(blog post, case study, press release, or the TCRO white paper). The marketing",
    "team creates one HubSpot Website Page per resource using these templates.",
    "",
    "## How to activate a resource in HubSpot",
    "",
    "1. Go to **Marketing → Website → Website Pages → Create → Website page**.",
    "2. In the template picker, search for the template by its label (e.g. ",
    "   `Blog: Total Cost of Risk Ownership vs Cost of Risk`).",
    "3. Set the page URL to `/resources/<slug>/` (the slug column below).",
    "4. Publish.",
    "",
    "Templates have `isAvailableForNewContent: false` because each is bound to",
    "exactly one resource — they should not be picked accidentally for unrelated",
    "pages. If you want to reuse a layout for a different resource, duplicate the",
    "template file, change its label, and update the title/meta/body in place.",
    "",
    "## Template index",
    "",
    "| Template file | URL slug | Type |",
    "|---|---|---|",
]
order = ["white-paper", "case-study", "blog", "press-release"]
for t in order:
    for r in [x for x in rows if x["type"] == t]:
        readme_lines.append(f"| `resources/{r['slug']}.html` | `/resources/{r['slug']}/` | {t} |")
readme_lines.append("")
readme_lines.append(f"_{len(rows)} templates total — generated from `.build/build_resources_v2.py`._")

(RES_DIR / "README.md").write_text("\n".join(readme_lines), encoding="utf-8")

# ── Report ───────────────────────────────────────────────────────────────────
print(f"\n=== Generation summary ===")
print(f"CSV rows:       {len(rows)}  → {csv_path}")
print(f"JSON entries:   {len(api_rows)}  → {json_path}")
print(f"Sub-templates:  {len(generated)}  → {RES_DIR}/<slug>.html")
print(f"README:         {RES_DIR}/README.md")
print(f"Issues:         {len(issues)}")
for i in issues:
    print(" -", i)

# Counts by type
from collections import Counter
print("\nBy type:")
for t, n in Counter(r["type"] for r in rows).items():
    print(f"  {t:14s}  {n}")
