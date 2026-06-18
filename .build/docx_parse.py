import zipfile, re, sys, json, html
from xml.etree import ElementTree as ET

W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def run_text(r):
    """Walk run children in order: text, no-break hyphen, tab, break."""
    out=[]
    for ch in r:
        tag=ch.tag
        if tag==W+'t': out.append(ch.text or '')
        elif tag==W+'noBreakHyphen': out.append('-')
        elif tag==W+'softHyphen': out.append('')
        elif tag==W+'tab': out.append(' ')
        elif tag in (W+'br',W+'cr'): out.append(' ')
    return ''.join(out)

def runs_html(p):
    parts=[]
    for r in p.findall(W+'r'):
        txt=run_text(r)
        if txt=='' : continue
        rpr=r.find(W+'rPr')
        b=i=False
        if rpr is not None:
            bn=rpr.find(W+'b'); it=rpr.find(W+'i')
            b = bn is not None and bn.get(W+'val','true') not in ('false','0')
            i = it is not None and it.get(W+'val','true') not in ('false','0')
        esc=html.escape(txt)
        if esc.strip()=='' :
            parts.append(esc); continue
        if b: esc=f'<strong>{esc}</strong>'
        if i: esc=f'<em>{esc}</em>'
        parts.append(esc)
    s=''.join(parts)
    s=re.sub(r'</strong>(\s*)<strong>',r'\1',s)
    s=re.sub(r'</em>(\s*)<em>',r'\1',s)
    return s.strip()

def para_meta(p):
    ppr=p.find(W+'pPr')
    if ppr is None: return None,False,None
    ps=ppr.find(W+'pStyle'); style=ps.get(W+'val') if ps is not None else None
    is_list = ppr.find(W+'numPr') is not None
    jc=ppr.find(W+'jc'); align=jc.get(W+'val') if jc is not None else None
    return style,is_list,align

def parse(path):
    z=zipfile.ZipFile(path)
    root=ET.fromstring(z.read('word/document.xml'))
    body=root.find(W+'body')
    blocks=[]
    for p in body.findall(W+'p'):
        style,is_list,align = para_meta(p)
        h=runs_html(p); raw=re.sub(r'\s+',' ',(''.join(run_text(r) for r in p.findall(W+'r')))).strip()
        if not raw: continue
        sl=(style or '').lower()
        bt='p'
        if 'heading1' in sl or sl=='title': bt='h1'
        elif 'heading2' in sl: bt='h2'
        elif 'heading3' in sl or 'heading4' in sl: bt='h3'
        elif 'quote' in sl: bt='quote'
        elif is_list or 'listparagraph' in sl: bt='li'
        blocks.append({'type':bt,'html':h,'text':raw,'align':align})
    return blocks

# ---- Heuristic heading detection for prose docs (no Word heading styles) ----
def looks_like_heading(text):
    t=text.strip()
    if len(t)>95: return False
    if t.endswith('?'): return True
    if t.endswith((':','.',',',';','!','"','”')): return False
    words=t.split()
    if len(words)<2 or len(words)>14: return False
    # Title-ish: majority of significant words capitalized, OR short imperative phrase
    return True

def postprocess(blocks, drop_title=True):
    # drop the doc-title first line (e.g. "Post 1: ...")
    out=[]
    started=False
    for idx,b in enumerate(blocks):
        if drop_title and not started and idx==0:
            started=True
            # skip first block (document title)
            continue
        out.append(b)
    # promote question-style headings (only if currently 'p' and not a list lead-in)
    for k,b in enumerate(out):
        if b['type']=='p' and looks_like_heading(b['text']):
            # ensure next block exists and isn't a list lead-in colon
            b['type']='h2'
    return out

def clean_links(h):
    # remove editorial "[link to /path]" or "[link: ...]" markers
    h=re.sub(r'\s*\[link[^\]]*\]','',h, flags=re.I)
    h=re.sub(r'\s*\[[^\]]*/[^\]]*\]','',h)  # leftover bracketed paths
    return h

if __name__=='__main__':
    path=sys.argv[1]
    raw=parse(path)
    blocks=postprocess(raw, drop_title=('--keep-title' not in sys.argv))
    if '--json' in sys.argv:
        for b in blocks: b['html']=clean_links(b['html'])
        print(json.dumps(blocks,ensure_ascii=False,indent=1))
    else:
        for b in blocks:
            print(f"[{b['type']:5}] {clean_links(b['html'])[:120]}")
