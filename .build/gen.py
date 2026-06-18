# -*- coding: utf-8 -*-
import json, re, os, math, html, shutil, csv

ROOT="/Users/zulbearijahjanur/Downloads/Novem_HubSpot_Zulbera"
JSON=f"{ROOT}/.build/json"
PREV=f"{ROOT}/preview/resources"
BASE=f"{ROOT}/.build/base_template.html"

# ---------- base chrome ----------
base=open(BASE,encoding='utf-8').read()
pre, _, rest = base.partition("<!-- HERO -->")
_mid, _, post = rest.partition("<!-- FOOTER -->")
POST="<!-- FOOTER -->"+post   # footer + scripts (shared)

# Inject badge colors for case-study / white-paper / press-release (base only defines blog)
extra_badges=(".badge--cs{background:color-mix(in srgb,#60BCD6 12%,transparent);color:#60BCD6;border:1px solid color-mix(in srgb,#60BCD6 30%,transparent);}"
              ".badge--wp{background:color-mix(in srgb,#B8A0E8 12%,transparent);color:#B8A0E8;border:1px solid color-mix(in srgb,#B8A0E8 30%,transparent);}"
              ".badge--pr{background:color-mix(in srgb,#7BFAB5 12%,transparent);color:#7BFAB5;border:1px solid color-mix(in srgb,#7BFAB5 30%,transparent);}")
pre=re.sub(r'(\.badge--blog\{[^}]*\})', r'\1'+extra_badges, pre, count=1)

# badge/accent per type
TYPE_META={
 'blog':            {'label':'Blog','eye':'Blog','badge':'badge--blog','accent':'#7BFAB5'},
 'case-study':      {'label':'Case Study','eye':'Case Study','badge':'badge--cs','accent':'#60BCD6'},
 'press-release':   {'label':'Press Release','eye':'Press Release','badge':'badge--pr','accent':'#7BFAB5'},
 'white-paper':     {'label':'White Paper','eye':'White Paper','badge':'badge--wp','accent':'#B8A0E8'},
}

def esc(s): return html.escape(s,quote=True)
def words(blocks): return sum(len(re.sub('<[^>]+>','',b['html']).split()) for b in blocks)
def readtime(n): return max(2,math.ceil(n/220))

# ---------- registry ----------
# key = json filename stem ; meta drives everything
BLOGS=[
 # json-stem, slug, title, tags
 ("BLOG__Post 1 - Total Cost of Risk Ownership vs Cost of Risk","tcro-vs-cost-of-risk",
  "Total Cost of Risk Ownership vs Cost of Risk",["TCRO","Cost of Risk","CFO","Risk Strategy"]),
 ("BLOG__Post 2 - Data Governance Is Not an IT Project. It Is the Operating System of Financial Control.","data-governance-financial-control",
  "Data Governance Is Not an IT Project. It Is the Operating System of Financial Control.",["Data Governance","Financial Control","CIO","TCRO"]),
 ("BLOG__Post 3 - From Reactive to Predictive Maintenance as a Finance Strategy","reactive-to-predictive-maintenance",
  "From Reactive to Predictive: Why Your Maintenance Model Is Now a Finance Strategy",["Predictive Operations","Maintenance","Finance Strategy","Downtime"]),
 ("BLOG__Post 4 - 7 Non Negotiable Criteria for a Digital Risk Platform","7-criteria-digital-risk-platform",
  "7 Non-Negotiable Criteria for a Digital Risk Platform That Actually Lowers TCRO",["Digital Risk Platform","Vendor Evaluation","TCRO","Procurement"]),
 ("BLOG__Post 5 - Insurance Is No Longer a Fixed Line Item","insurance-no-longer-fixed-line-item",
  "Insurance Is No Longer a Fixed Line Item",["Insurance","Underwriting","Risk Data","CFO"]),
 ("BLOG__Post 6 - Make Data Pay Turning Building Risk Data into a Financial Asset","make-data-pay",
  "Make Data Pay: Turning Building Risk Data into a Financial Asset",["Building Data","Financial Asset","ROI","Data Strategy"]),
 ("BLOG__Post 7 - How TCRO Changes Capital Planning From Age Based Replacement to Risk Weighted Investment","tcro-capital-planning",
  "How TCRO Changes Capital Planning: From Age-Based Replacement to Risk-Weighted Investment",["Capital Planning","TCRO","CapEx","Asset Management"]),
 ("BLOG__Post 8 - TCRO in the Real World - Seniors, Office, and Mixed Use Portfolios","tcro-in-the-real-world",
  "TCRO in the Real World: Seniors, Office, and Mixed-Use Portfolios",["TCRO","Seniors Housing","Mixed-Use","Portfolio"]),
 ("BLOG__Post 9 - The TCRO Dashboard - What Your Board Needs to See, and What It Does Not","tcro-dashboard-for-boards",
  "The TCRO Dashboard: What Your Board Needs to See, and What It Does Not",["TCRO","Board Reporting","Governance","Dashboards"]),
 ("BLOG__Post 10 - From ESG Reporting to TCRO - Turning Sustainability Data into Financial and Risk Advantage","esg-to-tcro",
  "From ESG Reporting to TCRO: Turning Sustainability Data into Financial and Risk Advantage",["ESG","Sustainability","TCRO","ROI"]),
 ("BLOG__Post 11 - The Hidden Wage Cost of Invisible Risk","hidden-wage-cost-of-invisible-risk",
  "The Hidden Wage Cost of Invisible Risk",["Labor Cost","Overtime","Risk","CHRO"]),
 ("BLOG__Post 12 - AI in the Built Environment - Why You Need TCRO and Data Governance Before You Buy Another Model","ai-in-the-built-environment",
  "AI in the Built Environment: Why You Need TCRO and Data Governance Before You Buy Another Model",["AI","Data Governance","TCRO","Technology Strategy"]),
 ("BLOG__Post 13 - TCRO Implementation Checklist for CFOs","tcro-implementation-checklist-cfos",
  "TCRO Implementation Checklist for CFOs",["TCRO","Implementation","CFO","Checklist"]),
 ("BLOG__Post 14 - Best Digital Risk Platforms for Institutional Real Estate in 2026","best-digital-risk-platforms-2026",
  "Best Digital Risk Platforms for Institutional Real Estate in 2026",["Digital Risk Platform","Buyer Guide","Institutional Real Estate","2026"]),
 ("BLOG__Blog 15 - TCRO ROI Snapshot - Seniors Housing","tcro-roi-seniors-housing",
  "What TCRO Really Looks Like in Seniors Housing (And Where the ROI Comes From)",["TCRO ROI","Seniors Housing","Outbreaks","Wage Cost"]),
 ("BLOG__Blog 16 - TCRO ROI Snapshot - Events and Entertainment Campus","tcro-roi-events-entertainment",
  "TCRO ROI in Events and Entertainment Campuses: Preventing the Expensive Failure",["TCRO ROI","Events & Venues","Utilities","Resilience"]),
 ("BLOG__Blog 17 - TCRO ROI Snapshot - Mixed Use and Office","tcro-roi-office-mixed-use",
  "TCRO ROI in Office and Mixed-Use Portfolios: Outages, Utilities, and Insurance",["TCRO ROI","Office","Mixed-Use","Insurance"]),
]
# manual ledes for posts whose doc opens on a heading (no intro paragraph)
LEDE_OVERRIDE={
 "tcro-roi-seniors-housing":"In seniors housing, the biggest swings in Total Cost of Risk Ownership come from outbreaks, environmental failures, and wage premiums — not just property damage. Here is what TCRO looks like in practice, and where the ROI shows up.",
 "tcro-roi-events-entertainment":"For events and entertainment campuses, TCRO is dominated by large, high-visibility failures — utilities, aging infrastructure, and the cost of a cancelled event. Here is where predictive operations pays back.",
 "tcro-roi-office-mixed-use":"In office and mixed-use portfolios, Total Cost of Risk Ownership is driven by outages, utility waste, and insurance friction. Here is how making failure predictable changes the numbers.",
}

CASES=[
 # json-stem, slug, title, industry, descriptor, [ (num,label) x3 ]
 ("CASE__Bethany Riverview","dementia-care-continuous-commissioning",
  "Automated Continuous Commissioning Unlocks $200K+ at a Specialized Dementia Care Facility",
  "Dementia & Long-Term Care","A specialized dementia and long-term care facility in Western Canada",
  [("$200K+","Total value unlocked"),("$93K","Handover cost reduction"),("$109K","Annual operating savings")]),
 ("CASE__LHRG Pioneer Lodge","seniors-living-outbreak-reduction",
  "65% Fewer Outbreak Weeks at a Regional Seniors Living Operator",
  "Seniors Living","A regional seniors living operator with a 120-resident supportive living community",
  [("65%","Fewer outbreak weeks"),("19→3","Lockdown weeks"),("34%","Less PPE spend")]),
 ("CASE__PNE Pacific Coliseum","events-campus-claim-prevention",
  "Preventing a $5M Claim at a Major Western Canadian Events Campus",
  "Events & Entertainment","A major Western Canadian events and entertainment campus with multi-building, aging infrastructure",
  [("$5M","Max claim prevented"),("$400K/yr","Gas leak recovered"),("0%","Premium increase")]),
 ("CASE__TELUS Garden","mixed-use-office-accelerated-commissioning",
  "From 36 to 4 Months: Accelerated Commissioning at a Landmark Mixed-Use Office Tower",
  "Mixed-Use Office","A landmark mixed-use office tower in a major Canadian city",
  [("36→4 mo","Commissioning time"),("$10.1M","10-year savings forecast"),("~2%","Capital spend avoided")]),
 ("CASE__The Heights Collection","seniors-housing-insurance-savings",
  "10% Insurance Savings and 30% Digital Infrastructure Savings for an Independent Seniors Housing Developer",
  "Seniors Housing","A Western Canadian independent seniors housing developer",
  [("10%","Insurance savings"),("30%","Digital infrastructure savings"),("1%","Total construction cost cut")]),
]

# ---------- body rendering ----------
def render_blocks(blocks, type, skip_idx=None, case=False):
    out=[]; i=0
    ul=[]
    def flush_ul():
        if ul:
            out.append('<ul>'+''.join(f'<li>{x}</li>' for x in ul)+'</ul>'); ul.clear()
    for idx,b in enumerate(blocks):
        if skip_idx is not None and idx==skip_idx: continue
        t=b['type']; h=b['html']
        if t=='li': ul.append(h); continue
        flush_ul()
        if t in('h2','h3'):
            txt=re.sub('<[^>]+>','',h)
            tag=t
            if case:
                up=sum(1 for c in txt if c.isupper()); low=sum(1 for c in txt if c.islower())
                tag='h2' if (':' in txt or up>=low) else 'h3'
            out.append(f'<{tag}>{txt}</{tag}>')
        elif t=='quote':
            out.append(f'<blockquote>{h}</blockquote>')
        else:
            out.append(f'<p>{h}</p>')
    flush_ul()
    return '\n      '.join(out)

def stat_strip(stats):
    items=''.join(f'<div class="pull-stat-item"><div class="pull-stat-num">{esc(n)}</div><div class="pull-stat-label">{esc(l)}</div></div>' for n,l in stats)
    return f'<div class="pull-stat">{items}</div>'

# ---------- head patch ----------
def patch_head(pre, title, desc, slug, type, date=None):
    p=pre
    p=re.sub(r'<title>.*?</title>', f'<title>{esc(title)} | Novem Digital</title>', p, flags=re.S)
    p=re.sub(r'(<meta name="description" content=").*?("/>)', lambda m:m.group(1)+esc(desc)+m.group(2), p, flags=re.S)
    p=re.sub(r'(<link rel="canonical" href=").*?("/>)', lambda m:m.group(1)+f'/resources/{slug}/'+m.group(2), p)
    p=re.sub(r'(<meta property="og:title" content=").*?("/>)', lambda m:m.group(1)+esc(title)+m.group(2), p, flags=re.S)
    p=re.sub(r'(<meta property="og:description" content=").*?("/>)', lambda m:m.group(1)+esc(desc)+m.group(2), p, flags=re.S)
    p=re.sub(r'(<meta property="og:url" content=").*?("/>)', lambda m:m.group(1)+f'https://novemdigital.com/resources/{slug}'+m.group(2), p)
    p=re.sub(r'(<meta name="twitter:title" content=").*?("/>)', lambda m:m.group(1)+esc(title)+m.group(2), p, flags=re.S)
    p=re.sub(r'(<meta name="twitter:description" content=").*?("/>)', lambda m:m.group(1)+esc(desc)+m.group(2), p, flags=re.S)
    # replace JSON-LD with a clean Article graph
    schema_type={'blog':'BlogPosting','case-study':'Article','press-release':'NewsArticle','white-paper':'Article'}[type]
    ld={"@context":"https://schema.org","@type":schema_type,
        "headline":title,"description":desc,"author":{"@type":"Organization","name":"Novem Digital"},
        "publisher":{"@type":"Organization","name":"Novem Digital","url":"https://novemdigital.com"},
        "url":f"https://novemdigital.com/resources/{slug}"}
    if date: ld["datePublished"]=date
    ld_str=json.dumps(ld,ensure_ascii=False,indent=2)
    p=re.sub(r'<script type="application/ld\+json">.*?</script>',
             '<script type="application/ld+json">\n'+ld_str+'\n  </script>', p, flags=re.S)
    return p

# ---------- page assembly ----------
def build_page(type, slug, title, desc, tags, content_html, hero_title, date=None, read=None):
    tm=TYPE_META[type]
    pre2=patch_head(pre, title, desc, slug, type, date)
    meta_spans=[f'<span class="pr-badge {tm["badge"]}">{tm["label"]}</span>']
    if date: meta_spans.append(f'<span class="pr-date">{esc(date)}</span>')
    if read: meta_spans.append(f'<span class="pr-read">{read} min read</span>')
    meta_spans.append('<span class="pr-author">By Novem Digital</span>')
    tagstrip=''.join(f'<span class="tag">{esc(t)}</span>' for t in tags)
    hero=f'''<!-- HERO -->
<section class="hero" aria-label="{tm['label']} hero">
  <div class="hero-bg" style="background:radial-gradient(120% 120% at 80% 0%,{tm['accent']}22 0%,transparent 55%),linear-gradient(160deg,#0c1419 0%,#14242c 55%,#0c1419 100%);"></div>
  <div class="hero-content w" style="padding-top:7rem;">
    <div class="eye"><span class="eye-dot"></span>{tm['eye']}</div>
    <h1 class="h1" style="max-width:24ch;">{hero_title}</h1>
  </div>
</section>

<main id="main">
<section style="padding-block:clamp(3.5rem,7vw,6rem);">
  <div class="wm">
    <div class="pr-meta">
      {''.join(meta_spans)}
    </div>
    <div class="tag-strip">{tagstrip}</div>
    <div class="action-bar">
      <button class="action-btn action-btn--share" id="shareBtn" title="Copy link to clipboard">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
        <span id="shareBtnLabel">Share</span>
      </button>
      <button class="action-btn action-btn--download" id="downloadBtn" title="Print / Save as PDF">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        Download
      </button>
    </div>
    <div class="art-body">
      {content_html}
    </div>
    <div style="margin-top:4rem;padding:2.5rem;background:var(--surf);border:1px solid var(--border2);border-radius:var(--rxl);display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1.5rem;">
      <div>
        <div class="h3" style="margin-bottom:.5rem;">See it in your portfolio.</div>
        <p style="font-size:clamp(1rem,.95rem + .25vw,1.125rem);color:var(--muted);max-width:44ch;">See how Novem Digital turns building data into a lower Total Cost of Risk Ownership — before failure becomes a claim.</p>
      </div>
      <a href="/get-a-demo/" class="btn btn-p">Get a Demo</a>
    </div>
  </div>
</section>
</main>

'''
    return pre2+hero+POST

def write_page(slug, html_str):
    d=f"{PREV}/{slug}"; os.makedirs(d,exist_ok=True)
    open(f"{d}/index.html","w",encoding='utf-8').write(html_str)
    shutil.copyfile(f"{PREV}/logo.png", f"{d}/logo.png")

# ---------- run ----------
rows=[]  # hubdb rows

def first_p_index(blocks):
    for i,b in enumerate(blocks[:2]):
        if b['type']=='p': return i
    return None

# BLOGS
for stem,slug,title,tags in BLOGS:
    blocks=json.load(open(f"{JSON}/{stem}.json",encoding='utf-8'))
    fp=first_p_index(blocks)
    if slug in LEDE_OVERRIDE:
        lede=LEDE_OVERRIDE[slug]; skip=None
    else:
        lede=re.sub('<[^>]+>','',blocks[fp]['html']) if fp is not None else title
        skip=fp
    body=render_blocks(blocks,'blog',skip_idx=skip)
    lede_html=f'<p style="font-size:clamp(1.1rem,1rem + .35vw,1.3rem);color:#D4E8EE;font-style:italic;margin-bottom:2rem;">{esc(lede)}</p>\n      '
    content=lede_html+body
    n=words(blocks); rt=readtime(n)
    page=build_page('blog',slug,title,lede,tags,content,esc(title),date=None,read=rt)
    write_page(slug,page)
    rows.append(dict(slug=slug,type='blog',title=title,client='',industry=tags[0],publish_date='',summary=lede,read=rt,body=body,results='',stats=[]))
    print(f"blog  {slug:42} {rt}min {n}w")

# CASES
for stem,slug,title,industry,descriptor,stats in CASES:
    blocks=json.load(open(f"{JSON}/{stem}.json",encoding='utf-8'))
    # block0 title, block1 lede, block2 meta line -> render rest
    lede=blocks[1]['html'] if blocks[1]['type']=='p' else ''
    lede_txt=re.sub('<[^>]+>','',lede)
    # body = blocks from index 2 onward, but turn block2 (Solution Provider...) into a fact strip
    body_blocks=blocks[3:] if (len(blocks)>3 and blocks[2]['text'].startswith('Solution Provider')) else blocks[2:]
    factline = blocks[2]['html'] if blocks[2]['text'].startswith('Solution Provider') else ''
    body=render_blocks(body_blocks,'case-study',case=True)
    parts=[]
    parts.append(f'<p style="font-size:clamp(1.1rem,1rem + .35vw,1.3rem);color:#D4E8EE;font-style:italic;margin-bottom:1.5rem;">{esc(lede_txt)}</p>')
    if factline:
        parts.append(f'<p style="font-size:.9rem;color:var(--muted);border-left:3px solid var(--border2);padding-left:1rem;margin-bottom:2rem;">{factline}</p>')
    parts.append(stat_strip(stats))
    parts.append(body)
    content='\n      '.join(parts)
    tags=[industry,"Case Study","Predictive Operations","TCRO"]
    page=build_page('case-study',slug,title,lede_txt,tags,content,esc(title),date=None,read=None)
    write_page(slug,page)
    rows.append(dict(slug=slug,type='case-study',title=title,client=descriptor,industry=industry,publish_date='',summary=lede_txt,read='',body=body,results='',stats=stats))
    print(f"case  {slug:42} stats={[s[0] for s in stats]}")

# PRESS RELEASE (real content provided by client; replaces placeholder Whetsel/Jay PRs)
pr_slug="pr-accelerated-commissioning-office-tower"
pr_title="From 36 Months to 4 Months: Novem Digital Helps Landmark Mixed-Use Office Tower Accelerate Building Systems Startup by Nearly 89%"
pr_lede="Novem helps institutional real estate owners identify which building systems are likely to fail, what that failure could cost, and what to fix first to protect cash flow."
def q(text,cite):
    return f'<blockquote>{esc(text)}<cite>— {esc(cite)}</cite></blockquote>'
pr_body=f'''<p style="font-size:clamp(1.1rem,1rem + .35vw,1.3rem);color:#D4E8EE;font-style:italic;margin-bottom:2rem;">{esc(pr_lede)}</p>
      <p><strong>VANCOUVER, British Columbia, June 25, 2025</strong> &mdash; Novem Digital helps institutional real estate owners make building failure predictable. The company combines live building data with historical loss data to identify early signs of equipment and system risk, so owners can reduce surprise failures, avoid emergency spend, and make better capital and insurance decisions. Today, Novem Digital announced that its work at a landmark mixed-use office tower helped cut the building&rsquo;s systems startup and stabilization timeline from 36 months to 4 months.</p>
      <p>Building systems startup is the process of testing, tuning, and verifying that a building&rsquo;s critical systems &mdash; including HVAC, electrical, controls, and life safety &mdash; are working properly before and after full operations begin. When that process drags on, owners can face delayed stabilization, extended carrying costs, tenant frustration, and hidden performance issues that become expensive later.</p>
      {q("For owners and investors, readiness matters because cash flow depends on reliable building performance. Compressing a startup and stabilization timeline from 36 months to 4 months changes the economics of the asset. It improves operational confidence and helps protect asset value.","David Crawford, CFO and Head of Capital Planning, Novem Digital")}
      <p>Novem Digital is defining a new category in the market: a Digital Risk Platform for institutional real estate and insurance. In plain terms, that means helping owners move from reactive building management to predictive operations. Instead of waiting for a system to fail, Novem gives leaders earlier visibility into what is at risk, what action matters most, and how to defend those decisions with audit-ready data.</p>
      <p>Industry research has found that commissioning can deliver median whole-building energy savings of 13% in new construction and 16% in existing buildings, showing why faster and more effective building startup matters financially, not just operationally. Other industry estimates put delayed occupancy costs for commercial properties at $0.50 to $2.00 per square foot per month in lost revenue, which can quickly turn startup delays into a material cash flow issue.</p>
      <p>For owners and investors, that matters because the financial burden of building risk goes well beyond one repair. It includes claims, downtime, emergency repair premiums, insurance volatility, wasted labor, and capital deployed too late. Novem refers to that broader burden as Total Cost of Risk Ownership.</p>
      <p>At this mixed-use office tower, Novem Digital helped move the asset from fragmented testing and handover activity to a more continuous, structured, and financially visible process. That shortened the path to dependable building performance and reduced the period where system underperformance could put revenue readiness and asset value at risk.</p>
      {q("In institutional real estate, a long building startup cycle is not just an engineering issue. It is a financial issue. When a building takes years to stabilize, owners absorb delay, uncertainty, and avoidable cost. Novem helps make that risk visible early enough to act on it.","Clint Undseth, CEO, Novem Digital")}
      <p>The result strengthens Novem Digital&rsquo;s position in mixed-use office, institutional commercial real estate, and complex urban developments where leaders need more confidence in capital timing, operational readiness, and the financial consequences of underperformance. It also reinforces the company&rsquo;s belief that risk should never be invisible &mdash; because what owners cannot see often becomes what they end up paying for.</p>
      <p>Novem Digital is headquartered in Vancouver, Canada.</p>
      <h2>Notes to Editors</h2>
      <p>Customer outcome data referenced in this release &mdash; including the reduction in building systems startup timeline from 36 months to 4 months &mdash; is Novem Digital proprietary client data. External statistics are sourced as follows:</p>
      <ul>
        <li>Building commissioning energy savings benchmark (13% new construction / 16% existing buildings) &mdash; Lawrence Berkeley National Laboratory, &ldquo;Building Commissioning Costs and Savings Across Three Decades and 1,500 North American Buildings.&rdquo; <a href="https://eta-publications.lbl.gov/publications/building-commissioning-costs-and" target="_blank" rel="noopener">Source</a></li>
        <li>Delayed occupancy cost range ($0.50&ndash;$2.00 per sq ft per month) &mdash; PingCx, &ldquo;The Hidden Costs of Manual Commissioning in Today&rsquo;s Complex Buildings&rdquo; (May 2025). <a href="https://www.pingcx.com/blog/the-hidden-costs-of-manual-commissioning-in-todays-complex-buildings" target="_blank" rel="noopener">Source</a></li>
      </ul>
      <h2>About Novem Digital</h2>
      <p>Novem Digital is an AI-powered digital risk platform that makes building failure predictable for institutional real estate portfolios. Novem predicts and prevents equipment failures before they happen by combining real-time monitoring with historical insurance claims data from millions of buildings. Customers reduce Total Cost of Risk Ownership, protect cash flow, and manage risk-related costs with confidence across operations, capital planning, and insurance.</p>
      <p style="font-size:.9rem;color:var(--muted);margin-top:2rem;">Media contact: <a href="mailto:pr@novemdigital.com">pr@novemdigital.com</a></p>'''
pr_hero='From 36 Months to <span class="accent">4 Months.</span>'
pr_tags=["Announcement","Mixed-Use Office","Commissioning","Vancouver"]
page=build_page('press-release',pr_slug,pr_title,pr_lede,pr_tags,pr_body,pr_hero,date="June 25, 2025",read=None)
write_page(pr_slug,page)
pr_body_csv=re.sub(r'^<p style="font-size:clamp\(1.1rem.*?</p>\s*','',pr_body,count=1,flags=re.S)
rows.append(dict(slug=pr_slug,type='press-release',title=pr_title,client='',industry='Customer Outcome',publish_date='2025-06-25',summary=pr_lede,read='',body=pr_body_csv,results='',stats=[]))
print(f"pr    {pr_slug:42} (press release)")

# ============ REBUILD LISTING (preview/resources/index.html) ============
summary_map={r['slug']:r['summary'] for r in rows}
read_map={r['slug']:r.get('read') for r in rows}

def excerpt(s,n=165):
    s=re.sub(r'\s+',' ',s).strip()
    if len(s)<=n: return s
    cut=s[:n].rsplit(' ',1)[0]
    return cut.rstrip('.,;:')+'…'

ARROW='<svg width="13" height="13" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def thumb(accent):
    return f'background:radial-gradient(130% 130% at 75% 12%,{accent}33 0%,transparent 55%),linear-gradient(150deg,#0c1419 0%,#162a33 55%,#0c1419 100%);'

# ---- Case study cards ----
cs_cards=[]
for stem,slug,title,industry,descriptor,stats in CASES:
    n1,l1=stats[0]; n2,l2=stats[1]
    cs_cards.append(f'''      <a class="rcard rev" data-type="case-study" href="/resources/{slug}/" target="_blank" rel="noopener noreferrer">
        <div class="rcard-img" style="{thumb('#7BFAB5')}">
          <span class="rcard-badge rcard-badge--cs">Case Study</span>
        </div>
        <div class="rcard-body">
          <div class="rcard-meta"><span class="rcard-industry">{esc(industry)}</span></div>
          <h3 class="rcard-title">{esc(title)}</h3>
          <p class="rcard-excerpt">{esc(excerpt(summary_map[slug]))}</p>
          <div class="rcard-stats">
            <div><div class="rcard-stat-num">{esc(n1)}</div><div class="rcard-stat-lbl">{esc(l1)}</div></div>
            <div><div class="rcard-stat-num">{esc(n2)}</div><div class="rcard-stat-lbl">{esc(l2)}</div></div>
          </div>
          <span class="rcard-link">Read case study {ARROW}</span>
        </div>
      </a>''')

# ---- White paper section: single honest "coming soon" (real WP pending from client) ----
wp_cards=[f'''      <div class="rcard rcard--soon rev" data-type="white-paper">
        <div class="rcard-img" style="{thumb('#60BCD6')}">
          <span class="rcard-badge rcard-badge--wp">White Paper</span>
        </div>
        <div class="rcard-body">
          <div class="rcard-meta"><span class="rcard-industry" style="color:var(--wp);">TCRO Framework</span></div>
          <h3 class="rcard-title">The Total Cost of Risk Ownership White Paper</h3>
          <p class="rcard-excerpt">The full TCRO framework — define, quantify, and defend the complete cost of building risk across an institutional portfolio. In production; publishing soon.</p>
          <span class="rcard-coming">Coming Soon</span>
        </div>
      </div>''']

# ---- Blog cards ----
bl_cards=[]
for stem,slug,title,tags in BLOGS:
    cat=tags[0]; rt=read_map.get(slug)
    meta=f'<span class="rcard-industry" style="color:var(--bl);">{esc(cat)}</span>'
    if rt: meta+=f'<span class="rcard-dot"></span><span class="rcard-date">{rt} min read</span>'
    bl_cards.append(f'''      <a class="rcard rev" data-type="blog" href="/resources/{slug}/" target="_blank" rel="noopener noreferrer">
        <div class="rcard-img" style="{thumb('#B8A0E8')}">
          <span class="rcard-badge" style="background:color-mix(in srgb,var(--bl,#B8A0E8) 80%,#000);color:#fff;">Blog</span>
        </div>
        <div class="rcard-body">
          <div class="rcard-meta">{meta}</div>
          <h3 class="rcard-title">{esc(title)}</h3>
          <p class="rcard-excerpt">{esc(excerpt(summary_map[slug]))}</p>
          <span class="rcard-link" style="margin-top:auto;">Read article {ARROW}</span>
        </div>
      </a>''')

# ---- Press release card (real) ----
pr_cards=[f'''      <a class="rcard rev" data-type="press-release" href="/resources/{pr_slug}/" target="_blank" rel="noopener noreferrer">
        <div class="rcard-img" style="{thumb('#60BCD6')}">
          <span class="rcard-badge rcard-badge--pr">Press Release</span>
        </div>
        <div class="rcard-body">
          <div class="rcard-meta"><span class="rcard-industry" style="color:var(--pr);">Customer Outcome</span><span class="rcard-dot"></span><span class="rcard-date">June 25, 2025</span></div>
          <h3 class="rcard-title">{esc(pr_title)}</h3>
          <p class="rcard-excerpt">{esc(excerpt(pr_lede))}</p>
          <span class="rcard-link" style="margin-top:auto;">Read press release {ARROW}</span>
        </div>
      </a>''']

def grid(label, dtype, cards, mt=False):
    style=' style="margin-top:1rem;"' if mt else ''
    return (f'''    <!-- ── {label.upper()} ── -->
    <div class="section-divider section-divider--{dtype[:2] if dtype!='case-study' else 'cs'} content-section" data-section="{dtype}"{style}>
      <span class="section-divider-label">{label}</span>
      <span class="section-divider-line"></span>
    </div>

    <div class="resource-grid content-section" data-section="{dtype}">

{chr(10).join(c+chr(10) for c in cards)}    </div>''')

new_lib='\n'.join([
    grid('Case Studies','case-study',cs_cards),
    '',
    grid('White Papers','white-paper',wp_cards,mt=True),
    '',
    grid('Blog','blog',bl_cards,mt=True),
    '',
    grid('Press Releases','press-release',pr_cards,mt=True),
])

LIST=f"{PREV}/index.html"
li=open(LIST,encoding='utf-8').read()
pat=re.compile(r'<!-- ── CASE STUDIES ──.*?\n\n(  </div>\n</section>\n\n<!-- ═══ FAQ)', re.S)
assert pat.search(li), "listing splice markers not found"
li2=pat.sub(lambda m: new_lib+'\n\n'+m.group(1), li)
open(LIST,'w',encoding='utf-8').write(li2)
print("Listing rebuilt: %d case, %d wp(soon), %d blog, %d pr"%(len(cs_cards),len(wp_cards),len(bl_cards),len(pr_cards)))

# ============ HubDB IMPORT FILES (novem-hubspot/hubdb/) ============
HUBDB=f"{ROOT}/novem-hubspot/hubdb"
COLS=["title","slug","type","client","industry","publish_date","summary","body","results",
      "stat1_num","stat1_label","stat2_num","stat2_label","stat3_num","stat3_label",
      "seo_title","seo_description"]
def row_record(r):
    st=r.get('stats') or []
    def s(i,j):
        return st[i][j] if i < len(st) else ""
    return {
      "title":r['title'],"slug":r['slug'],"type":r['type'],"client":r.get('client',''),
      "industry":r.get('industry',''),"publish_date":r.get('publish_date',''),
      "summary":r['summary'],"body":r.get('body',''),"results":r.get('results',''),
      "stat1_num":s(0,0),"stat1_label":s(0,1),"stat2_num":s(1,0),"stat2_label":s(1,1),
      "stat3_num":s(2,0),"stat3_label":s(2,1),
      "seo_title":f"{r['title']} | Novem Digital","seo_description":excerpt(r['summary'],155),
    }
records=[row_record(r) for r in rows]
# order: case studies, blog, press-release (white paper pending)
order={'case-study':0,'white-paper':1,'blog':2,'press-release':3}
records.sort(key=lambda x:(order.get(x['type'],9), x['title']))
# CSV
with open(f"{HUBDB}/resources_rows.csv","w",newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=COLS); w.writeheader()
    for rec in records: w.writerow(rec)
# JSON (HubDB rows API shape: {"path","name","values":{...}})
api_rows=[{"path":rec["slug"],"name":rec["title"],
           "values":{k:v for k,v in rec.items() if v!=""}} for rec in records]
json.dump(api_rows, open(f"{HUBDB}/resources_rows.json","w",encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"HubDB import: {len(records)} rows -> resources_rows.csv + resources_rows.json")

import pickle
pickle.dump(rows, open(f"{ROOT}/.build/rows.pkl","wb"))
print("\nTOTAL pages:",len(rows))
