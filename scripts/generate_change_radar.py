#!/usr/bin/env python3
"""Generate a public, evidence-first AI Tool Change Radar."""
from __future__ import annotations
from datetime import date
from html import escape
import json
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"

def esc(v: object) -> str:
    return escape(str(v or ""), quote=True)

def load(path: Path):
    return json.loads(path.read_text())

def generate(root: Path) -> Path:
    tools = load(root / "data/tools.json")
    sources = {x["slug"]: x for x in load(root / "data/tool_sources.json")["tools"]}
    prices = load(root / "data/pricing_snapshots.json").get("snapshots", {})
    lineups = load(root / "data/model_lineups.json")
    rows=[]; dates=[]
    for t in tools:
        slug=t["slug"]; src=sources.get(slug,{}) ; snap=prices.get(slug,{})
        pricing_date=src.get("pricing_checked_date") or snap.get("date") or ""
        lineup=lineups.get(slug,{})
        model_date=lineup.get("as_of","")
        for d in (pricing_date,model_date):
            if d: dates.append(d)
        latest=max([d for d in (pricing_date,model_date) if d] or [""])
        kinds=[]
        if pricing_date: kinds.append("pricing")
        if model_date: kinds.append("models")
        unresolved=len(src.get("unresolved_claims",[]))
        status="Freshly checked" if latest and latest==max(dates or [latest]) else "Needs recheck"
        rows.append({"slug":slug,"name":t.get("name",slug),"category":t.get("category",""),"pricing_date":pricing_date,"model_date":model_date,"latest":latest,"status":status,"kinds":kinds,"unresolved":unresolved})
    latest=max(dates or [str(date.today())])
    rows.sort(key=lambda r:(r["latest"] != latest, r["latest"], r["name"]))
    tool_count = len(tools)
    watches_path = root / "data/vendor_watches.json"
    watch_cards = []
    if watches_path.exists():
        watch_data = load(watches_path)
        for w in watch_data.get("watches", []):
            src = w.get("source_url") or ""
            src_link = (
                f'<a href="{esc(src)}" rel="external nofollow" target="_blank">{esc(w.get("source_title") or src)}</a>'
                if src else "Official source not recorded"
            )
            watch_cards.append(f'''<article class="score-card vendor-watch">
<span class="evidence-label">Unlisted launch · {esc(w.get("status", "watch"))}</span>
<h2>{esc(w.get("name"))}</h2>
<p>Checked <strong>{esc(w.get("checked_at"))}</strong> against {src_link}.</p>
<p>{esc(w.get("summary"))}</p>
<p><strong>Pricing:</strong> {esc(w.get("pricing_note") or "No public self-serve pricing recorded.")}</p>
<p class="radar-links"><a href="/updates/">Monthly digest →</a><a href="/model-lineups/">Model lineups →</a><a href="/pricing-watch/">Pricing Watch →</a></p>
</article>''')
    watch_section = ""
    if watch_cards:
        watch_section = (
            '<section class="score-card" style="margin:0 0 28px;border-left:4px solid #d97706">'
            '<span>Vendor launches · not directory SKUs</span>'
            '<h2>Recorded launches without public self-serve pricing.</h2>'
            '<p>These are dated official-source watches. They are not tools.json listings, have no invented plan prices, and do not get a review page until public pricing exists.</p>'
            f'{"".join(watch_cards)}</section>'
        )
    cards=[]
    for r in rows:
        tags=''.join(f'<span class="radar-tag">{esc(k.title())}</span>' for k in r['kinds'])
        unresolved=f'<span class="radar-note">{r["unresolved"]} unresolved claim(s)</span>' if r['unresolved'] else '<span class="radar-note">No unresolved claims recorded</span>'
        cards.append(f'''<article class="radar-row" data-search="{esc((r['name']+' '+r['category']+' '+' '.join(r['kinds'])).lower())}" data-status="{esc(r['status'])}">
<div class="radar-main"><div><span class="evidence-label">{esc(r['category'])}</span><h2><a href="/tools/{esc(r['slug'])}/">{esc(r['name'])}</a></h2></div><span class="radar-status">{esc(r['status'])}</span></div>
<div class="radar-meta">{tags}<span>Latest recorded check: <strong>{esc(r['latest'])}</strong></span>{unresolved}</div>
<p>Pricing: {esc(r['pricing_date'] or 'not recorded')} · Model lineup: {esc(r['model_date'] or 'not recorded')}</p>
<p class="radar-links"><a href="/tools/{esc(r['slug'])}/">Review →</a><a href="/evidence/#evidence-{esc(r['slug'])}">Evidence row →</a><a href="/pricing-watch/">Pricing Watch →</a></p>
</article>''')
    schema=json.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":"AI Tool Change Radar","url":f"{DOMAIN}/change-radar/","description":"Recorded pricing and model-lineup freshness for the AI tools directory.","dateModified":latest},separators=(",",":"))
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="AI Tool Change Radar: see the latest recorded pricing and model-lineup checks, unresolved claims, and evidence links for {tool_count} AI tools."><title>AI Tool Change Radar — Pricing &amp; Model Freshness</title><link rel="canonical" href="{DOMAIN}/change-radar/"><meta property="og:title" content="AI Tool Change Radar — AIToolsEssentials"><meta property="og:description" content="Track recorded pricing and model-lineup freshness before you decide."><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg"><link rel="stylesheet" href="/css/styles.css"><script type="application/ld+json">{schema}</script></head><body><header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/fit-interview/">Fit interview</a><a href="/confidence-check/">Confidence check</a><a href="/pricing-watch/">Pricing Watch</a><a href="/evidence/">Evidence</a><a href="/guides/switch-guides/">Switching</a></nav><a class="nav-cta" href="/premium/">Premium</a></header><main><section class="scene scene-dark"><div class="radar-hero"><p class="kicker">Trust layer · return before you buy</p><h1>What changed since the last check?</h1><p class="subhead">A transparent radar for recorded pricing and model-lineup freshness. It is not a vendor API or a guarantee of real-time change detection—always verify the official source before purchase.</p><div class="radar-hero-actions"><a class="button button-blue" href="/pricing-watch/">Open Pricing Watch</a><a class="button button-dark" href="/evidence/">Inspect Evidence Ledger</a><a class="button button-ghost-dark" href="/newsletter/" style="margin-left:8px">Keep/Cut Weekly</a></div></div></section><section class="scene scene-light"><div class="article-shell wide"><div class="radar-principles"><div><strong>Recorded, not implied</strong><span>Dates show when the source was last checked.</span></div><div><strong>Models move too</strong><span>Lineup checks are separate from pricing checks.</span></div><div><strong>Unresolved stays visible</strong><span>Missing evidence is a buying signal, not a hidden footnote.</span></div></div>{watch_section}<div class="radar-controls"><label for="radar-search">Find a tool</label><input id="radar-search" type="search" placeholder="Search by tool, category, or check type"><label class="radar-check"><input id="radar-attention" type="checkbox"> Show only items needing attention</label><span id="radar-count">{len(rows)} tools shown</span></div><div class="radar-list">{''.join(cards)}</div><section class="score-card radar-next"><span>Next decision step</span><h2>Do not buy from a stale snapshot.</h2><p>Use the radar to find the right record, then run the Fit Interview, inspect the evidence row, and test the tool with one real task before subscribing.</p><p><a class="button button-blue" href="/fit-interview/">Run Fit Interview</a><a class="button button-dark" href="/decision-brief.html">Create Decision Brief</a></p></section></div></section></main><footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/methodology/">Methodology</a><a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a></footer><script>
(function(){{var input=document.getElementById('radar-search'), attention=document.getElementById('radar-attention'), rows=[].slice.call(document.querySelectorAll('.radar-row')), count=document.getElementById('radar-count'); function apply(){{var q=(input.value||'').toLowerCase().trim(), n=0; rows.forEach(function(row){{var ok=(!q||row.dataset.search.indexOf(q)>-1)&&(!attention.checked||row.dataset.status==='Needs recheck'); row.hidden=!ok;if(ok)n++;}});count.textContent=n+' tool'+(n===1?'':'s')+' shown';}} input.addEventListener('input',apply);attention.addEventListener('change',apply);}})();</script></body></html>'''
    out=root/'change-radar'/'index.html'; out.parent.mkdir(exist_ok=True); out.write_text(page); return out

def main():
    import sys
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
    print(generate(root))
if __name__=='__main__': main()
