#!/usr/bin/env python3
"""Generate the public Model Lineups index — a source-dated ledger of what each
tracked product actually ships, so comparisons stay about real models, not
marketing names.

Data-driven from data/model_lineups.json. The per-comparison panels are
injected by scripts/generate_model_lineups.py; this generator owns the hub
page at /model-lineups/.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from html import escape
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"


def esc(v: object) -> str:
    return escape(str(v or ""), quote=True)


def strict_date(value: object) -> str:
    """Return a validated YYYY-MM-DD date string or an empty string."""
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        return ""
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return ""
    return value


def generate(root: Path) -> Path:
    lineups = json.loads((root / "data/model_lineups.json").read_text())
    tools = {x["slug"]: x for x in json.loads((root / "data/tools.json").read_text())}
    today = datetime.now().strftime("%Y-%m-%d")

    unknown_slugs = sorted(
        k for k, lu in lineups.items()
        if k not in tools and lu.get("listed") is not False
    )
    if unknown_slugs:
        raise ValueError(f"data/model_lineups.json references unknown tool slugs: {unknown_slugs}")

    def lineup_name(slug: str, lu: dict) -> str:
        if lu.get("listed") is False:
            return str(lu.get("name") or slug)
        return str(tools[slug].get("name", slug))

    cards = []
    dates = []
    for slug, lu in sorted(lineups.items(), key=lambda kv: lineup_name(kv[0], kv[1]).lower()):
        unlisted = lu.get("listed") is False
        if unlisted:
            name = lineup_name(slug, lu)
            category = lu.get("category", "Research watch")
            official = lu.get("official") or lu.get("source_url") or ""
            if not official:
                raise ValueError(f"unlisted model lineup {slug} is missing an official source URL")
        else:
            name = tools[slug].get("name", slug)
            category = tools[slug].get("category", "")
            official = ""
        as_of = strict_date(lu.get("as_of", ""))
        if not as_of:
            raise ValueError(f"model lineup for {slug} has a missing or invalid as_of date")
        dates.append(as_of)
        models = lu.get("models", [])
        if not isinstance(models, list) or not models:
            raise ValueError(f"model lineup for {slug} has no models list")
        rows = "".join(
            f'<tr><td><strong>{esc(m.get("model",""))}</strong></td><td>{esc(m.get("role",""))}</td>'
            f'<td>{esc(m.get("context","-"))}</td><td>{esc(m.get("pricing","-"))}</td></tr>'
            for m in models
        )
        notes = "".join(f"<li>{esc(n)}</li>" for n in lu.get("notes", []))
        if unlisted:
            products_badge = '<span class="evidence-label">Research watch</span>'
            heading = f'<h2><a href="{esc(official)}" rel="external nofollow" target="_blank">{esc(name)}</a></h2>'
            links = (
                f'<p class="radar-links"><a href="{esc(official)}" rel="external nofollow" target="_blank">Official source →</a>'
                f'<a href="/change-radar/">Change Radar →</a><a href="/updates/">Monthly digest →</a></p>'
            )
        else:
            products_badge = '<span class="evidence-label">Products &amp; plans</span>' if lu.get("products") else '<span class="evidence-label">Model lineup</span>'
            heading = f'<h2><a href="/tools/{esc(slug)}/">{esc(name)}</a></h2>'
            links = (
                f'<p class="radar-links"><a href="/tools/{esc(slug)}/">Full review →</a>'
                f'<a href="/evidence/#evidence-{esc(slug)}">Evidence row →</a>'
                f'<a href="/change-radar/">Change Radar →</a></p>'
            )
        cards.append(f'''<article class="radar-row" id="lineup-{esc(slug)}" data-search="{esc((name + ' ' + category).lower())}">
<div class="radar-main"><div>{products_badge}<span class="evidence-label">{esc(category)}</span>{heading}</div><span class="radar-status">Checked {esc(as_of)}</span></div>
<div class="table-wrap"><table><thead><tr><th>Model / product</th><th>Role</th><th>Context</th><th>Pricing</th></tr></thead><tbody>{rows}</tbody></table></div>
{f'<ul class="lineup-notes">{notes}</ul>' if notes else ''}
{links}
</article>''')

    latest = max(dates) if dates else today
    count = len(lineups)
    listed_count = sum(1 for lu in lineups.values() if lu.get("listed") is not False)
    unlisted_count = count - listed_count
    tool_count = len(tools)
    coverage = (
        f"{listed_count} of {tool_count} tracked tools"
        + (f", plus {unlisted_count} research watch" + ("es" if unlisted_count != 1 else "") + " without public pricing" if unlisted_count else "")
    )
    schema = json.dumps({
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": "AI Model Lineups — source-dated coverage",
        "url": f"{DOMAIN}/model-lineups/",
        "description": f"Source-dated model and product lineups for {coverage}.",
        "dateModified": latest,
    }, separators=(",", ":"))

    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Source-dated model and product lineups for {esc(coverage)}: current shipping models, roles, context, and pricing notes with checked dates."><title>AI Model Lineups — Source-Dated Coverage · AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/model-lineups/"><meta property="og:title" content="AI Model Lineups — AIToolsEssentials"><meta property="og:description" content="What each AI product actually ships today, with checked dates."><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg"><link rel="stylesheet" href="/css/styles.css"><script type="application/ld+json">{schema}</script></head><body><header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/fit-interview/">Fit interview</a><a href="/confidence-check/">Confidence check</a><a href="/pricing-watch/">Pricing Watch</a><a href="/change-radar/">Change Radar</a><a href="/evidence/">Evidence</a></nav><a class="nav-cta" href="/premium/">Premium</a></header><main><section class="scene scene-dark"><div class="radar-hero"><p class="kicker">Trust layer · updated {esc(today)}</p><h1>What's actually shipping, dated.</h1><p class="subhead">Model names and prices move fast. This ledger tracks the current model or product lineup for {esc(coverage)} — with the date each lineup was checked against official vendor sources. Research watches are not directory SKUs.</p><div class="radar-hero-actions"><a class="button button-blue" href="/change-radar/">Open Change Radar</a><a class="button button-dark" href="/comparisons/">See comparisons</a><a class="button button-ghost-dark" href="/newsletter/" style="margin-left:8px">Keep/Cut Weekly</a></div></div></section><section class="scene scene-light"><div class="article-shell wide"><div class="radar-principles"><div><strong>Source-dated</strong><span>Every lineup names its check date; lineups are verified against official vendor pages, never inferred from marketing.</span></div><div><strong>Models vs products</strong><span>Some tools ship named models; others sell products and plans. The badge on each card distinguishes them.</span></div><div><strong>Fed into comparisons</strong><span>These same records power the current-lineup panels on head-to-head comparison pages.</span></div></div><div class="radar-toolbar"><input id="lineup-search" type="search" placeholder="Search {count} lineups" aria-label="Search lineups"><span id="lineup-count" class="radar-count">{count} shown</span></div>{''.join(cards)}</div></section></main><footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/advertise/index.html" rel="nofollow">Advertise</a><a href="/submit-tool.html" rel="nofollow">Submit a tool</a><a href="/community/test-report.html" rel="nofollow">Report your results</a><a href="/badges/">Badges</a><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a></footer><script>
(function(){{var input=document.getElementById('lineup-search'),cards=[].slice.call(document.querySelectorAll('.radar-row')),count=document.getElementById('lineup-count');function apply(){{var q=(input.value||'').toLowerCase().trim(),n=0;cards.forEach(function(c){{var ok=!q||c.dataset.search.indexOf(q)>-1;c.hidden=!ok;if(ok)n++;}});count.textContent=n+' shown';}}input.addEventListener('input',apply);}})();
</script><script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script></body></html>'''
    out = root / "model-lineups" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)
    return out


def main():
    import sys
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    print(generate(root))


if __name__ == "__main__":
    main()
