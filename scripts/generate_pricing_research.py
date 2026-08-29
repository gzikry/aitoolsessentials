#!/usr/bin/env python3
"""Generate the current State of AI Tool Pricing research page."""
from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path
from typing import Any

DOMAIN = "https://aitoolsessentials.com"


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> Path:
    if tools is None:
        tools = json.loads((root / "data" / "tools.json").read_text())
    pricing = json.loads((root / "data" / "pricing_snapshots.json").read_text())
    snapshots = pricing.get("snapshots", {})
    today = today or date.today().isoformat()
    current = [tool for tool in tools if tool.get("slug") in snapshots]
    current.sort(key=lambda tool: tool.get("name", "").lower())
    total = len(current)
    free_count = sum("free" in str(tool.get("price", "")).lower() for tool in current)
    paid_count = total - free_count
    free_pct = round((free_count / total) * 100) if total else 0
    dates = [rec.get("date", "") for rec in snapshots.values() if rec.get("date")]
    latest = max(dates) if dates else today

    rows = []
    for tool in current:
        slug = tool["slug"]
        rec = snapshots[slug]
        free = "free" in str(tool.get("price", "")).lower()
        model = "Free tier available" if free else "Paid / sales-led"
        rows.append(
            '<tr>'
            f'<td><strong><a href="/tools/{esc(slug)}/">{esc(tool.get("name"))}</a></strong></td>'
            f'<td>{esc(tool.get("category"))}</td>'
            f'<td><span class="category-pill">{model}</span></td>'
            f'<td>{esc(rec.get("digest"))}</td>'
            f'<td>{esc(rec.get("date"))}</td>'
            '</tr>'
        )

    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "State of AI Tool Pricing 2026",
        "description": f"Dated official-pricing snapshots for {total} AI tools tracked by AIToolsEssentials.",
        "url": f"{DOMAIN}/research/ai-tool-pricing-2026.html",
        "dateModified": latest,
        "creator": {"@type": "Organization", "name": "AIToolsEssentials", "url": DOMAIN},
        "measurementTechnique": "Manual verification against official vendor pricing pages",
        "variableMeasured": ["Plan availability", "Price", "Billing cadence", "Usage limits", "Checked date"],
    }, separators=(",", ":"))

    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Official-pricing snapshots for {total} AI tools, including free-tier availability, plan details, usage limits, and checked dates.">
<title>State of AI Tool Pricing 2026 — {total} Tools Tracked | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/research/ai-tool-pricing-2026.html"><link rel="stylesheet" href="../css/styles.css"><link rel="stylesheet" href="../css/share.css">
<script type="application/ld+json">{schema}</script></head><body>
<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/pricing-watch/">Pricing Watch</a><a href="/pricing-report/">Pricing report</a><a href="/change-radar/">Change radar</a><a href="/evidence/">Evidence</a><a href="/articles/">Guides</a></nav><a class="nav-cta" href="/premium/">Premium</a></header>
<main><section class="scene scene-dark"><div class="hero-copy" style="max-width:820px;margin:0 auto;padding:90px 28px 70px;text-align:center;justify-self:center"><p class="kicker">Original research · latest source check {esc(latest)}</p><h1>State of AI Tool Pricing 2026</h1><p class="subhead">A current, source-led view of how {total} tracked AI tools charge: free-tier availability, paid-plan structure, usage limits, and the date each official pricing page was checked.</p><p><a class="button button-blue" href="/pricing-watch/">Open Pricing Watch</a><a class="button button-ghost-dark" href="/newsletter/" style="margin-left:8px">Get Keep/Cut Weekly</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
<div class="content-hub-grid"><article class="content-hub-card"><span>Coverage</span><h2>{total}</h2><p>Current directory tools with dated pricing snapshots.</p></article><article class="content-hub-card"><span>Free access</span><h2>{free_count} of {total}</h2><p>{free_pct}% are labeled with a free tier or free/self-hosted path in the directory.</p></article><article class="content-hub-card"><span>Paid first</span><h2>{paid_count}</h2><p>Tools without a free-path label; some use sales-led pricing.</p></article><article class="content-hub-card"><span>Latest check</span><h2>{esc(latest)}</h2><p>Newest official-pricing verification date in the dataset.</p></article></div>
<h2>What this dataset can—and cannot—tell you</h2><p><strong>Free access is common, but limits are the product.</strong> Message caps, credits, minutes, renders, operations, seats, and storage determine whether a nominally free tool fits a real weekly workflow.</p><p><strong>Billing units are not directly comparable.</strong> A seat, credit, operation, token, minute, or generated second creates different cost risk. Compare the unit against your own task volume before buying annually.</p><p><strong>This is a directory snapshot, not the whole AI market.</strong> Coverage reflects the tools tracked by AIToolsEssentials. Prices and limits can change after the recorded check date; follow the review's official source before purchase.</p>
<h2>Current pricing dataset</h2><div class="table-wrap"><table><thead><tr><th>Tool</th><th>Category</th><th>Access model</th><th>Official-pricing snapshot</th><th>Checked</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<section class="score-card"><span>Use the data</span><h2>Check changes before the renewal date.</h2><p>Pricing Watch shows the source snapshots; the change radar surfaces records that need another look. Keep/Cut Weekly turns verified changes into one practical decision each week.</p><p><a class="button button-blue" href="/pricing-watch/">Inspect snapshots</a><a class="button button-dark" href="/change-radar/" style="margin-left:8px">Open change radar</a><a class="button button-dark" href="/newsletter/" style="margin-left:8px">Read Keep/Cut Weekly</a></p></section>
<h2>Methodology</h2><ul><li>Each row is tied to the current tool inventory and a dated pricing snapshot.</li><li>Snapshot text records plan names, published prices, cadence, and meaningful limits where available.</li><li>Free-tier classification uses the current directory pricing label; it is not a claim that the free tier is sufficient.</li><li>Promotions do not change rankings. Affiliate participation does not change inclusion, scores, or conclusions.</li></ul>
</div></section></main><div id="share-row" hidden></div>
<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/pricing-watch/">Pricing Watch</a><a href="/evidence/">Evidence</a><a href="/legal/editorial-methodology.html">Methodology</a><a href="/submit-tool.html" rel="nofollow">Submit corrections</a><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a></footer><script src="../js/site.js" defer></script><script src="../js/analytics.js" defer></script></body></html>'''
    out = root / "research" / "ai-tool-pricing-2026.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)

    home = root / "index.html"
    if home.exists():
        text = home.read_text()
        import re
        text = re.sub(r'\d+ tools\. Pricing verified from official pages\.', f'{total} tools. Pricing verified from official pages.', text, count=1)
        home.write_text(text)
    llms = root / "llms.txt"
    if llms.exists():
        text = llms.read_text()
        import re
        text = re.sub(r'verified snapshots for \d+ tools', f'verified snapshots for {total} tools', text)
        llms.write_text(text)
    return out


if __name__ == "__main__":
    project = Path(__file__).resolve().parents[1]
    print(generate(project))
