#!/usr/bin/env python3
"""Generate viral/shareable growth utilities for AIToolsEssentials."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

DOMAIN = 'https://aitoolsessentials.com'
EMAIL = 'contact@aitoolsessentials.com'

HEADER = '''<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/stack-builder.html">Stack builder</a><a href="/tool-finder.html">Tool finder</a><a href="/free-ai-tools.html">Free AI tools</a><a href="/alternatives/">Alternatives</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/articles/index.html">Guides</a></nav><a class="nav-cta" href="/pricing/">Premium</a></header>'''
FOOTER = f'''<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/advertise/index.html" rel="nofollow">Advertise</a><a href="/submit-tool.html" rel="nofollow">Submit a tool</a><a href="/community/test-report.html" rel="nofollow">Report your results</a><a href="/badges/">Badges</a><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a></footer>'''

def esc(s):
    return (str(s or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;'))

def head(title, desc, canonical):
    return f'''<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{esc(desc)}"><title>{esc(title)}</title><link rel="canonical" href="{canonical}"><link rel="stylesheet" href="/css/styles.css"></head>'''

def scripts(extra=''):
    return extra + '<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>'

def tool_card(t):
    return f'''<article class="content-hub-card"><span>{esc(t['category'])} · {esc(t.get('price',''))}</span><h3><a href="/tools/{t['slug']}/">{esc(t['name'])}</a></h3><p>{esc(t.get('summary',''))}</p><p><strong>Best for:</strong> {esc(t.get('best_for',''))}</p><a class="button button-blue small" href="/tools/{t['slug']}/">Read review</a></article>'''

def pick_stack(tools, role, budget, vibe):
    by = {t['slug']: t for t in tools}
    stacks = {
        'freelancer': ['chatgpt','perplexity','make','canva-ai','otter-ai'],
        'agency': ['jasper','copy-ai','canva-ai','make','descript'],
        'developer': ['cursor','github-copilot','claude','replit-ai','v0'],
        'teacher': ['chatgpt','gamma','canva-ai','perplexity','otter-ai'],
        'creator': ['descript','elevenlabs','canva-ai','midjourney','allvideoai'],
        'small-business': ['chatgpt','make','zapier-ai','airtable-ai','microsoft-copilot'],
        'researcher': ['perplexity','claude','you-com','gemini','notion-ai'],
    }
    slugs = stacks.get(role, stacks['freelancer'])
    if budget == 'free':
        slugs = [s for s in slugs if s in by and 'free' in by[s].get('price','').lower()] + [s for s in ['chatgpt','claude','gemini','perplexity','canva-ai','n8n'] if s in by]
    if vibe == 'technical':
        slugs = ['n8n','cursor','github-copilot','claude','airtable-ai'] + slugs
    if vibe == 'low-friction':
        slugs = ['chatgpt','canva-ai','zapier-ai','perplexity','otter-ai'] + slugs
    seen=[]
    for s in slugs:
        if s in by and s not in seen: seen.append(s)
    return [by[s] for s in seen[:5]]

def generate_stack_builder(root, tools):
    payload = json.dumps([{k:t.get(k) for k in ['slug','name','category','best_for','price','rating','summary']} for t in tools], separators=(',',':'))
    default_stack = pick_stack(tools, 'freelancer', 'free', 'low-friction')
    default_cards = ''.join(tool_card(t) for t in default_stack)
    default_result = f'<span>Your shareable stack</span><h2>freelancer · free · low-friction</h2><div class="content-hub-grid">{default_cards}</div><p><button class="button button-blue" id="shareNative">Share stack</button><a class="button button-blue" href="/cost-calculator.html" style="margin-left:8px">Estimate cost</a></p>'
    page = f'''<!doctype html><html lang="en">{head('AI Stack Builder — Generate Your Shareable AI Stack | AIToolsEssentials','Generate a personalized AI tools stack for your role, budget, and workflow. Share your stack with a link and compare full reviews.',DOMAIN+'/stack-builder.html')}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:880px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Shareable AI stack generator</p><h1>Generate the AI stack you would actually use.</h1><p class="subhead">Pick your role, budget, and workflow style. Get a clean stack you can copy, save, or share.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card viral-control"><span>Build your stack</span><div class="viral-controls"><label>Role<select id="role"><option value="freelancer">Freelancer / consultant</option><option value="agency">Agency / marketer</option><option value="developer">Developer / builder</option><option value="teacher">Teacher / educator</option><option value="creator">Creator / YouTuber</option><option value="small-business">Small business / ops</option><option value="researcher">Researcher / analyst</option></select></label><label>Budget<select id="budget"><option value="free">Free-first</option><option value="balanced">Balanced</option><option value="premium">Premium OK</option></select></label><label>Style<select id="vibe"><option value="low-friction">Low-friction</option><option value="technical">Technical/control</option><option value="creative">Creative-heavy</option></select></label></div><div class="actions" style="margin-top:18px"><button class="button button-blue" id="generateStack">Generate stack</button><button class="button button-blue" id="copyStack">Copy share link</button></div></div><div id="stackResult" class="viral-result-card">{default_result}</div></div></section></main>{FOOTER}{scripts('<script>const TOOLS='+payload+';</script><script src="/js/viral.js" defer></script>')}</body></html>'''
    (root/'stack-builder.html').write_text(page)

def generate_stack_gallery(root, tools):
    seed = [
        ('Solo consultant admin stack','freelancer','Free-first tools for drafting, research, automation, visuals, and meeting notes.'),
        ('Teacher free-tier classroom stack','teacher','A practical stack for lesson planning, slides, research, visuals, and meeting notes.'),
        ('Creator repurposing stack','creator','Voice, video, short clips, visuals, and script support for creators.'),
        ('Developer shipping stack','developer','Coding assistant, app builder, pair-programming, and UI generation stack.'),
        ('Small business operations stack','small-business','Lightweight tools for admin, CRM, automation, internal docs, and client workflows.'),
        ('Research analyst stack','researcher','Source-backed search, long-document synthesis, notes, and writing support.'),
    ]
    sections=''
    for title, role, desc in seed:
        items=pick_stack(tools, role, 'free' if 'free' in title.lower() else 'balanced', 'low-friction')
        sections += f'''<section class="stack-gallery-block"><div><h2>{esc(title)}</h2><p>{esc(desc)}</p><p><a class="button button-blue small" href="/stack-builder.html">Build a similar stack</a></p></div><div class="content-hub-grid">{''.join(tool_card(t) for t in items[:3])}</div></section>'''
    page=f'''<!doctype html><html lang="en">{head('AI Stack Gallery — Copy Practical AI Tool Stacks | AIToolsEssentials','Browse practical AI stacks for consultants, teachers, creators, developers, small businesses, and researchers.',DOMAIN+'/stacks/')}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:880px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">AI stack gallery</p><h1>Copy a stack. Then make it yours.</h1><p class="subhead">Seed stacks for common roles — designed to be shared, debated, and improved.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Community loop</span><p>Have a better real-world stack? Submit it through the community report form and we can publish verified examples as buyer evidence.</p><p><a class="button button-blue" href="/community/test-report.html">Submit real results</a></p></div>{sections}</div></section></main>{FOOTER}{scripts()}</body></html>'''
    out=root/'stacks'/'index.html'; out.parent.mkdir(exist_ok=True); out.write_text(page)

def generate_badges(root, tools):
    top = sorted(tools, key=lambda t: float(t.get('rating',0) or 0), reverse=True)[:12]
    badges=''.join(f'''<article class="content-hub-card"><span>{esc(t['category'])}</span><h3>{esc(t['name'])}</h3><div class="vendor-badge-preview"><strong>Reviewed on AIToolsEssentials</strong><small>{esc(t.get('rating'))}/5 editorial score</small></div><textarea readonly>&lt;a href="{DOMAIN}/tools/{t['slug']}/" rel="noopener"&gt;&lt;img alt="Reviewed on AIToolsEssentials" src="{DOMAIN}/badges/{t['slug']}.svg"&gt;&lt;/a&gt;</textarea><a class="button button-blue small" href="/tools/{t['slug']}/">Review page</a></article>''' for t in top)
    page=f'''<!doctype html><html lang="en">{head('AIToolsEssentials Vendor Badges — Reviewed AI Tool Badges','Vendors can link to their AIToolsEssentials review with transparent, editorially-labeled badges.',DOMAIN+'/badges/')}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:880px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Vendor badges</p><h1>Give reviewed tools a reason to link back.</h1><p class="subhead">Transparent badges for vendors who want to point buyers to independent review pages. No paid ranking implied.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Editorial rules</span><p>Badges link to review pages and may not imply endorsement beyond the exact text shown. Sponsored placements remain separately labeled.</p></div><div class="content-hub-grid">{badges}</div></div></section></main>{FOOTER}{scripts()}</body></html>'''
    out=root/'badges'/'index.html'; out.parent.mkdir(exist_ok=True); out.write_text(page)

def generate_cost_calculator(root, tools):
    payload=json.dumps([{k:t.get(k) for k in ['slug','name','category','price','summary','rating']} for t in tools], separators=(',',':'))
    cost_cards=''.join(f'<article class="content-hub-card"><span>{esc(t["category"])} · {esc(t.get("price",""))}</span><h3>{esc(t["name"])}</h3><p>{esc(t.get("summary",""))}</p><label><input type="checkbox" data-cost value="{t["slug"]}"> Add to estimate</label></article>' for t in tools)
    default_summary='<span>Estimated monthly stack cost</span><h2>$0/mo</h2><p>Select tools above to estimate your monthly stack. Verify current vendor pricing before paying.</p>'
    page=f'''<!doctype html><html lang="en">{head('AI Tool Cost Calculator — Estimate Your Stack Cost | AIToolsEssentials','Estimate your AI stack cost by choosing tools and team size. Compare free-first and paid-plan risk before subscribing.',DOMAIN+'/cost-calculator.html')}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:880px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">AI tool cost calculator</p><h1>Know the monthly cost before the stack sprawls.</h1><p class="subhead">Select tools, set team size, and see rough monthly budget risk. Official pricing changes often — use this as a planning estimate.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Estimate</span><label>Team size <input id="teamSize" type="number" min="1" value="1"></label><p class="muted-small">Planning assumptions: free/self-hosted = $0, free+paid = $20/user/mo, paid = $35/user/mo unless official pages say otherwise. Use reviews for current pricing.</p></div><div id="costSummary" class="viral-result-card">{default_summary}</div><div id="costToolList" class="content-hub-grid">{cost_cards}</div></div></section></main>{FOOTER}{scripts('<script>const COST_TOOLS='+payload+';</script><script src="/js/viral.js" defer></script>')}</body></html>'''
    (root/'cost-calculator.html').write_text(page)

def generate_weekly(root, tools, today):
    top = sorted(tools, key=lambda t: float(t.get('rating',0) or 0), reverse=True)[:5]
    free = [t for t in tools if 'free' in t.get('price','').lower()][:5]
    auto = [t for t in tools if 'automation' in t.get('category','').lower() or 'workflow' in t.get('best_for','').lower()][:4]
    page=f'''<!doctype html><html lang="en">{head('AI Tools Worth Testing This Week | AIToolsEssentials','A weekly public shortlist of AI tools worth testing, pricing notes, workflow ideas, and tools to compare before paying.',DOMAIN+'/weekly/')}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:880px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Weekly shortlist · Updated {today}</p><h1>AI tools worth testing this week.</h1><p class="subhead">A repeat-visit page for practical tools, free-tier picks, and workflow stacks worth trying.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><h2>Five tools worth testing</h2><div class="content-hub-grid">{''.join(tool_card(t) for t in top)}</div><h2>Free-tier picks to try before paying</h2><div class="content-hub-grid">{''.join(tool_card(t) for t in free)}</div><h2>Workflow stack of the week</h2><p>Automate lead intake, first response, and follow-up reminders with a free-first operations stack.</p><div class="content-hub-grid">{''.join(tool_card(t) for t in auto)}</div><p><a class="button button-blue" href="/stack-builder.html">Generate your stack</a><a class="button button-blue" href="/cost-calculator.html" style="margin-left:8px">Estimate cost</a></p></div></section></main>{FOOTER}{scripts()}</body></html>'''
    out=root/'weekly'/'index.html'; out.parent.mkdir(exist_ok=True); out.write_text(page)

def generate_js(root):
    js = r'''
(function(){
function params(){return new URLSearchParams(location.search)}
function find(slug){return (window.TOOLS||[]).find(t=>t.slug===slug)}
function stacks(role,budget,vibe){
 const base={freelancer:['chatgpt','perplexity','make','canva-ai','otter-ai'],agency:['jasper','copy-ai','canva-ai','make','descript'],developer:['cursor','github-copilot','claude','replit-ai','v0'],teacher:['chatgpt','gamma','canva-ai','perplexity','otter-ai'],creator:['descript','elevenlabs','canva-ai','midjourney','allvideoai'],'small-business':['chatgpt','make','zapier-ai','airtable-ai','microsoft-copilot'],researcher:['perplexity','claude','you-com','gemini','notion-ai']};
 let slugs=(base[role]||base.freelancer).slice();
 if(budget==='free') slugs=slugs.filter(s=>{let t=find(s); return t && /free/i.test(t.price||'')}).concat(['chatgpt','claude','gemini','perplexity','canva-ai','n8n']);
 if(vibe==='technical') slugs=['n8n','cursor','github-copilot','claude','airtable-ai'].concat(slugs);
 if(vibe==='low-friction') slugs=['chatgpt','canva-ai','zapier-ai','perplexity','otter-ai'].concat(slugs);
 const seen=[]; return slugs.filter(s=>find(s)&&!seen.includes(s)&&seen.push(s)).slice(0,5).map(find);
}
function card(t){return `<article class="content-hub-card"><span>${t.category} · ${t.price||''}</span><h3><a href="/tools/${t.slug}/">${t.name}</a></h3><p>${t.summary||''}</p><p><strong>Best for:</strong> ${t.best_for||''}</p><a class="button button-blue small" href="/tools/${t.slug}/">Read review</a></article>`}
function renderStack(){
 if(!window.TOOLS||!document.getElementById('stackResult')) return;
 const p=params(); ['role','budget','vibe'].forEach(id=>{if(p.get(id)&&document.getElementById(id)) document.getElementById(id).value=p.get(id)});
 const role=document.getElementById('role').value,budget=document.getElementById('budget').value,vibe=document.getElementById('vibe').value;
 const result=stacks(role,budget,vibe); const url=new URL(location.href); url.search=`?role=${role}&budget=${budget}&vibe=${vibe}`; history.replaceState(null,'',url);
 document.getElementById('stackResult').innerHTML=`<span>Your shareable stack</span><h2>${role.replace('-',' ')} · ${budget} · ${vibe}</h2><div class="content-hub-grid">${result.map(card).join('')}</div><p><button class="button button-blue" id="shareNative">Share stack</button><a class="button button-blue" href="/cost-calculator.html" style="margin-left:8px">Estimate cost</a></p>`;
 const share=document.getElementById('shareNative'); if(share) share.onclick=()=>{navigator.share?navigator.share({title:document.title,url:location.href}):navigator.clipboard.writeText(location.href).then(()=>share.textContent='Copied ✓')};
}
function renderCost(){
 if(!window.COST_TOOLS||!document.getElementById('costToolList')) return;
 const list=document.getElementById('costToolList'), summary=document.getElementById('costSummary'), team=document.getElementById('teamSize');
 function est(t){let p=(t.price||'').toLowerCase(); if(p.includes('free self-hosted')) return 0; if(p.includes('free')) return 20; return 35}
 function update(){let selected=[...document.querySelectorAll('[data-cost]:checked')].map(i=>COST_TOOLS.find(t=>t.slug===i.value)); let seats=Math.max(1,Number(team.value||1)); let monthly=selected.reduce((a,t)=>a+est(t)*seats,0); summary.innerHTML=`<span>Estimated monthly stack cost</span><h2>$${monthly}/mo</h2><p>${selected.length} tools · ${seats} seat${seats===1?'':'s'} · rough planning estimate. Verify current vendor pricing before paying.</p>`}
 list.innerHTML=COST_TOOLS.map(t=>`<article class="content-hub-card"><span>${t.category} · ${t.price||''}</span><h3>${t.name}</h3><p>${t.summary||''}</p><label><input type="checkbox" data-cost value="${t.slug}"> Add to estimate</label></article>`).join('');
 list.addEventListener('change',update); team.addEventListener('input',update); update();
}
document.addEventListener('DOMContentLoaded',function(){document.getElementById('generateStack')?.addEventListener('click',renderStack);document.getElementById('copyStack')?.addEventListener('click',()=>navigator.clipboard.writeText(location.href));renderStack();renderCost();});
})();
'''
    (root/'js'/'viral.js').write_text(js)

def generate_css(root):
    p=root/'css'/'styles.css'; css=p.read_text()
    if '.viral-controls' not in css:
        css += '''

/* Viral/share utility surfaces */
.viral-controls { display:grid; grid-template-columns:repeat(3,minmax(180px,1fr)); gap:14px; margin-top:14px; }
.viral-controls label, .viral-control label { display:flex; flex-direction:column; gap:7px; font-size:13px; font-weight:700; color:rgba(0,0,0,.62); }
.viral-controls select, .viral-control input { border:1px solid rgba(94,106,210,.22); border-radius:10px; padding:12px; font:inherit; background:#fff; }
.viral-result-card { margin-top:28px; padding:28px; border-radius:22px; border:1px solid rgba(94,106,210,.18); background:linear-gradient(180deg,#fff,rgba(94,106,210,.06)); box-shadow:0 24px 70px rgba(8,9,10,.08); }
.viral-result-card > span, .stack-gallery-block > div > p:first-child { text-transform:uppercase; letter-spacing:.12em; font-size:12px; font-weight:800; color:#5e6ad2; }
.stack-gallery-block { display:grid; grid-template-columns:minmax(240px,.55fr) 1fr; gap:28px; align-items:start; margin:58px 0; }
.vendor-badge-preview { display:inline-flex; flex-direction:column; gap:2px; border:1px solid rgba(94,106,210,.28); border-radius:14px; padding:12px 14px; background:linear-gradient(135deg,#08090a,#151626); color:#fff; box-shadow:0 18px 42px rgba(94,106,210,.18); }
.vendor-badge-preview small { color:rgba(255,255,255,.72); }
.content-hub-card textarea { width:100%; min-height:84px; border:1px solid rgba(0,0,0,.12); border-radius:10px; padding:10px; font-size:12px; background:#f8f8fb; }
@media (max-width: 800px) { .viral-controls, .stack-gallery-block { grid-template-columns:1fr; } }
'''
        p.write_text(css)

def generate(root: Path, tools: list | None = None, today: str | None = None):
    tools = tools or json.loads((root/'data/tools.json').read_text())
    today = today or datetime.today().strftime('%Y-%m-%d')
    generate_stack_builder(root, tools)
    generate_stack_gallery(root, tools)
    generate_badges(root, tools)
    generate_cost_calculator(root, tools)
    generate_weekly(root, tools, today)
    generate_js(root)
    generate_css(root)
    return 5

if __name__ == '__main__':
    root = Path(__file__).resolve().parent.parent
    print(generate(root))
