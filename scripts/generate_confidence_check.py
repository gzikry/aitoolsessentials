#!/usr/bin/env python3
"""Generate the public evidence-confidence utility."""
from __future__ import annotations
import html, json
from datetime import date
from pathlib import Path

DOMAIN='https://aitoolsessentials.com'

def esc(v): return html.escape(str(v or ''), quote=True)

def generate(root: Path, today: str) -> Path:
    tools=json.loads((root/'data/tools.json').read_text())
    source_data=json.loads((root/'data/tool_sources.json').read_text())
    sources={x['slug']:x for x in source_data.get('tools',[])}
    arena={x['tool_slug']:x for x in json.loads((root/'data/benchmarks.json').read_text()).get('arena_text_snapshot',[])}
    rows=[]
    for tool in sorted(tools,key=lambda x:x.get('name','')):
        slug=tool['slug']; src=sources.get(slug,{})
        checks=[bool(src.get('pricing_checked_date')),bool(src.get('pricing_url')),bool(src.get('docs_url')),bool(src.get('privacy_url')),bool(src.get('rights_url'))]
        unresolved=len(src.get('unresolved_claims') or [])
        points=sum(checks)*16
        if unresolved==0: points+=20
        elif unresolved<=2: points+=12
        elif unresolved<=4: points+=6
        if slug in arena: points+=0
        label='High' if points>=88 else 'Moderate' if points>=68 else 'Limited'
        row=f'''<article class="confidence-card" data-name="{esc(tool.get('name'))}" data-confidence="{points}"><div class="confidence-card-head"><div><span class="evidence-label">{esc(tool.get('category',''))}</span><h3><a href="/tools/{esc(slug)}/">{esc(tool.get('name',slug))}</a></h3></div><strong class="confidence-pill confidence-{label.lower()}">{label} confidence</strong></div><div class="confidence-meter"><span style="width:{min(points,100)}%"></span></div><p class="confidence-score"><strong>{points}/100</strong> evidence confidence</p><ul class="confidence-facts"><li>{'Pricing checked '+esc(src.get('pricing_checked_date')) if src.get('pricing_checked_date') else 'Pricing check date unavailable'}</li><li>{'Official pricing, docs, privacy, and rights links recorded' if sum(checks)>=5 else f'{sum(checks)}/5 core source links recorded'}</li><li>{'No unresolved claims recorded' if unresolved==0 else f'{unresolved} unresolved claim'+('s' if unresolved != 1 else '')} <a href="/evidence/#evidence-{esc(slug)}">View evidence →</a></li></ul></article>'''
        rows.append(row)
    schema=json.dumps({'@context':'https://schema.org','@type':'WebPage','name':'AI Tool Decision Confidence Check','url':f'{DOMAIN}/confidence-check/','dateModified':today,'description':'Transparent evidence-confidence scores for 40 AI tools.'})
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="See how much confidence to place in each AI tool review based on source freshness, official pricing, documentation, privacy, rights evidence, and unresolved claims."><title>AI Tool Decision Confidence Check — AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/confidence-check/"><meta property="og:title" content="AI Tool Decision Confidence Check"><meta property="og:description" content="Evidence confidence is separate from product quality. See what is known, dated, and unresolved."><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg"><link rel="stylesheet" href="/css/styles.css"><link rel="stylesheet" href="/css/share.css"><script type="application/ld+json">{schema}</script></head><body><header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/categories/">Categories</a><a href="/guides/switch-guides/">Switching</a><a href="/evidence/">Evidence</a><a href="/benchmarks/">Benchmarks</a></nav><a class="nav-cta" href="/premium/">Premium</a></header><main><section class="scene scene-dark"><div class="confidence-hero"><p class="kicker">Decision infrastructure · evidence quality</p><h1>Know how much confidence to place in the claim.</h1><p class="subhead">A product can be excellent and still have incomplete public evidence. This check separates evidence confidence from our editorial product score.</p><p><a class="button button-blue" href="/decision-brief.html">Build a decision brief</a><a class="button button-dark" href="/methodology/">Read the rules</a></p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="confidence-explainer"><div><strong>High</strong><span>Core source links are present and few unresolved claims remain.</span></div><div><strong>Moderate</strong><span>Useful evidence exists, but some policy, rights, or claim gaps remain.</span></div><div><strong>Limited</strong><span>Verify more directly before making a high-stakes purchase.</span></div></div><p class="confidence-note"><strong>Important:</strong> This is not a product-quality ranking. It measures the completeness and clarity of the public evidence record: pricing date, official pricing, documentation, privacy, rights, and unresolved-claim visibility.</p><label class="confidence-search">Find a tool <input id="confidence-search" type="search" placeholder="Search 40 tools" autocomplete="off"></label><div class="confidence-grid" id="confidence-grid">{"".join(rows)}</div><p id="confidence-empty" class="confidence-empty" hidden>No matching tool. Try another name.</p><section class="score-card confidence-next"><span>Use the confidence signal</span><h2>Still compare the fit, cost, and switching risk.</h2><p><a class="button button-blue" href="/compare-shortlist.html">Compare a shortlist</a><a class="button button-dark" href="/pricing-watch/">Check pricing freshness</a></p></section></div></section></main><footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/evidence/">Evidence ledger</a><a href="/methodology/">Methodology</a><a href="/legal/corrections.html">Corrections</a><a href="mailto:contact@aitoolsessentials.com">Contact</a></footer><script>const q=document.getElementById('confidence-search'),cards=[...document.querySelectorAll('.confidence-card')],empty=document.getElementById('confidence-empty');q.addEventListener('input',()=>{{const term=q.value.trim().toLowerCase();let shown=0;cards.forEach(c=>{{const yes=!term||c.dataset.name.toLowerCase().includes(term);c.hidden=!yes;if(yes)shown++;}});empty.hidden=shown!==0;}});</script><script src="/js/analytics.js" defer></script></body></html>'''
    out=root/'confidence-check'/'index.html'; out.parent.mkdir(exist_ok=True); out.write_text(page); return out

if __name__=='__main__':
    from datetime import date
    root=Path(__file__).resolve().parent.parent
    print(generate(root,date.today().isoformat()))
