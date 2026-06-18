# -*- coding: utf-8 -*-
import re,html,pickle,sys
ROOT="/Users/zulbearijahjanur/Downloads/Novem_HubSpot_Zulbera"
rows=pickle.load(open(f"{ROOT}/.build/rows.pkl","rb"))
def esc(s): return html.escape(s,quote=True)
def excerpt(s,n=165):
    s=re.sub(r'\s+',' ',s).strip()
    return s if len(s)<=n else s[:n].rsplit(' ',1)[0].rstrip('.,;:')+'…'
ARROW='<svg width="13" height="13" viewBox="0 0 14 14" fill="none"><path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def thumb(a): return f'background:radial-gradient(130% 130% at 75% 12%,{a}33 0%,transparent 55%),linear-gradient(150deg,#0c1419 0%,#162a33 55%,#0c1419 100%);'

cases=[r for r in rows if r['type']=='case-study']
blogs=[r for r in rows if r['type']=='blog']
prs  =[r for r in rows if r['type']=='press-release']

def case_card(r):
    st=r['stats']; (n1,l1),(n2,l2)=st[0],st[1]
    return f'''      <a class="rcard rev" data-type="case-study" href="/resources/{r['slug']}/" target="_blank" rel="noopener noreferrer">
        <div class="rcard-img" style="{thumb('#7BFAB5')}">
          <span class="rcard-badge rcard-badge--cs">Case Study</span>
        </div>
        <div class="rcard-body">
          <div class="rcard-meta"><span class="rcard-industry">{esc(r['industry'])}</span></div>
          <h3 class="rcard-title">{esc(r['title'])}</h3>
          <p class="rcard-excerpt">{esc(excerpt(r['summary']))}</p>
          <div class="rcard-stats">
            <div><div class="rcard-stat-num">{esc(n1)}</div><div class="rcard-stat-lbl">{esc(l1)}</div></div>
            <div><div class="rcard-stat-num">{esc(n2)}</div><div class="rcard-stat-lbl">{esc(l2)}</div></div>
          </div>
          <span class="rcard-link">Read case study {ARROW}</span>
        </div>
      </a>'''
def blog_card(r):
    meta=f'<span class="rcard-industry" style="color:var(--bl);">{esc(r["industry"])}</span>'
    if r.get('read'): meta+=f'<span class="rcard-dot"></span><span class="rcard-date">{r["read"]} min read</span>'
    return f'''      <a class="rcard rev" data-type="blog" href="/resources/{r['slug']}/" target="_blank" rel="noopener noreferrer">
        <div class="rcard-img" style="{thumb('#B8A0E8')}">
          <span class="rcard-badge" style="background:color-mix(in srgb,var(--bl,#B8A0E8) 80%,#000);color:#fff;">Blog</span>
        </div>
        <div class="rcard-body">
          <div class="rcard-meta">{meta}</div>
          <h3 class="rcard-title">{esc(r['title'])}</h3>
          <p class="rcard-excerpt">{esc(excerpt(r['summary']))}</p>
          <span class="rcard-link" style="margin-top:auto;">Read article {ARROW}</span>
        </div>
      </a>'''
def pr_card(r):
    return f'''      <a class="rcard rev" data-type="press-release" href="/resources/{r['slug']}/" target="_blank" rel="noopener noreferrer">
        <div class="rcard-img" style="{thumb('#60BCD6')}">
          <span class="rcard-badge rcard-badge--pr">Press Release</span>
        </div>
        <div class="rcard-body">
          <div class="rcard-meta"><span class="rcard-industry" style="color:var(--pr);">Customer Outcome</span><span class="rcard-dot"></span><span class="rcard-date">June 25, 2025</span></div>
          <h3 class="rcard-title">{esc(r['title'])}</h3>
          <p class="rcard-excerpt">{esc(excerpt(r['summary']))}</p>
          <span class="rcard-link" style="margin-top:auto;">Read press release {ARROW}</span>
        </div>
      </a>'''
wp_card='''      <div class="rcard rcard--soon rev" data-type="white-paper">
        <div class="rcard-img" style="%s">
          <span class="rcard-badge rcard-badge--wp">White Paper</span>
        </div>
        <div class="rcard-body">
          <div class="rcard-meta"><span class="rcard-industry" style="color:var(--wp);">TCRO Framework</span></div>
          <h3 class="rcard-title">The Total Cost of Risk Ownership White Paper</h3>
          <p class="rcard-excerpt">The full TCRO framework — define, quantify, and defend the complete cost of building risk across an institutional portfolio. In production; publishing soon.</p>
          <span class="rcard-coming">Coming Soon</span>
        </div>
      </div>'''%thumb('#60BCD6')

def grid(label,dtype,cards,mt=False):
    st=' style="margin-top:1rem;"' if mt else ''
    dd='cs' if dtype=='case-study' else dtype[:2]
    return (f'    <!-- ── {label.upper()} ── -->\n'
            f'    <div class="section-divider section-divider--{dd} content-section" data-section="{dtype}"{st}>\n'
            f'      <span class="section-divider-label">{label}</span>\n'
            f'      <span class="section-divider-line"></span>\n    </div>\n\n'
            f'    <div class="resource-grid content-section" data-section="{dtype}">\n\n'
            + ''.join(c+'\n\n' for c in cards) + '    </div>')

new_lib='\n'.join([
    grid('Case Studies','case-study',[case_card(r) for r in cases]),'',
    grid('White Papers','white-paper',[wp_card],mt=True),'',
    grid('Blog','blog',[blog_card(r) for r in blogs],mt=True),'',
    grid('Press Releases','press-release',[pr_card(r) for r in prs],mt=True),
])

# ---- head builders (anonymized) ----
KW=('institutional real estate case studies, building risk white paper, TCRO framework, '
    'Total Cost of Risk Ownership, predictive commissioning, automated continuous commissioning, '
    'commercial real estate risk intelligence, seniors living risk management, events campus risk, '
    'building failure prevention, insurance claim reduction, predictive building intelligence')
ARTS=[
 ("dementia-care-continuous-commissioning","Automated Continuous Commissioning Unlocks $200K+ at a Specialized Dementia Care Facility",
  "At a specialized dementia and long-term care facility in Western Canada, automated continuous commissioning cut wrap-up liability and delivered six-figure annual savings.",
  ["dementia & long-term care","automated continuous commissioning","building handover","HVAC failure detection"]),
 ("seniors-living-outbreak-reduction","65% Fewer Outbreak Weeks at a Regional Seniors Living Operator",
  "At a regional seniors living operator, continuous air quality monitoring cut outbreak weeks from 19 to 3 and reduced outbreak-related wage premiums and PPE spend.",
  ["seniors living risk management","air quality monitoring","infection control","respiratory outbreak prevention"]),
 ("events-campus-claim-prevention","Preventing a $5M Claim at a Major Western Canadian Events Campus",
  "At a major Western Canadian events and entertainment campus, predictive operations on 50-year-old infrastructure prevented a $5M claim, held premiums flat, and recovered over $400K per year in utility losses.",
  ["events & entertainment","insurance claim prevention","predictive maintenance","aging infrastructure"]),
 ("mixed-use-office-accelerated-commissioning","From 36 to 4 Months: Accelerated Commissioning at a Landmark Mixed-Use Office Tower",
  "At a landmark mixed-use office tower, an integrated digital risk platform compressed commissioning from 36 months to roughly 4, reduced capital spend, and set a 10-year, $10.1M energy savings forecast.",
  ["mixed-use office","automated continuous commissioning","building commissioning","energy savings"]),
 ("seniors-housing-insurance-savings","10% Insurance Savings and 30% Digital Infrastructure Savings for an Independent Seniors Housing Developer",
  "For an independent seniors housing developer, a lower Total Cost of Risk Ownership delivered 10% insurance savings and 30% lower digital infrastructure capital spend on a new community.",
  ["seniors housing","insurance savings","digital infrastructure","new development"]),
]
def art(slug,head,desc,about):
    ab=", ".join('"%s"'%a for a in about)
    return ('          {\n            "@type": "Article",\n'
            f'            "@id": "https://novemdigital.com/resources/{slug}",\n'
            f'            "url": "https://novemdigital.com/resources/{slug}",\n'
            f'            "headline": "{head.replace(chr(34),chr(92)+chr(34))}",\n'
            f'            "description": "{desc.replace(chr(34),chr(92)+chr(34))}",\n'
            '            "author": { "@id": "https://novemdigital.com/#org" },\n'
            '            "publisher": { "@id": "https://novemdigital.com/#org" },\n'
            f'            "about": [{ab}]\n          }}')
TCRO=('          {\n            "@type": "TechArticle",\n'
      '            "@id": "https://novemdigital.com/tcro",\n'
      '            "url": "https://novemdigital.com/tcro",\n'
      '            "headline": "The TCRO Framework: Total Cost of Risk Ownership for Institutional Real Estate",\n'
      '            "description": "The financial standard for measuring the complete cost of building risk across institutional real estate portfolios. A single number finance and operations leaders use to defend capital allocation and insurance decisions.",\n'
      '            "author": { "@id": "https://novemdigital.com/#org" },\n'
      '            "publisher": { "@id": "https://novemdigital.com/#org" }\n          }')
NEW_HASPART='"hasPart": [\n'+',\n'.join([art(*a) for a in ARTS]+[TCRO])+'\n        ]'
FAQ_NEW='Yes. Novem Digital has deployed air quality monitoring and predictive risk intelligence at seniors living and long-term care facilities. Anonymized case studies include a regional seniors living operator where outbreak weeks dropped 65%, and a specialized dementia care facility where critical HVAC failures were caught before residents moved in.'

def patch(path):
    s=open(path,encoding='utf-8').read(); orig=s
    s=re.sub(r'(<meta name="keywords" content=")[^"]*("\s*/?>)', lambda m:m.group(1)+KW+m.group(2), s, count=1)
    s=re.sub(r'"hasPart":\s*\[.*?\n        \]', lambda m:NEW_HASPART, s, count=1, flags=re.S)
    s=re.sub(r'Yes\. Novem Digital has deployed air quality monitoring.*?before residents moved in\.', lambda m:FAQ_NEW, s, flags=re.S)
    # card grid splice (markers identical in preview + theme)
    pat=re.compile(r'<!-- ── CASE STUDIES ──.*?\n\n(  </div>\n</section>\n\n<!-- ═══ FAQ)', re.S)
    if pat.search(s):
        s=pat.sub(lambda m:new_lib+'\n\n'+m.group(1), s, count=1)
    else:
        print("  WARN: grid markers not found in",path)
    open(path,'w',encoding='utf-8').write(s)
    return s!=orig

for p in sys.argv[1:]:
    ch=patch(p); print(("patched " if ch else "nochange ")+p)
