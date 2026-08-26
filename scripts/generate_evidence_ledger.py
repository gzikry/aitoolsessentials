#!/usr/bin/env python3
"""Generate a public evidence ledger for every reviewed tool."""
from __future__ import annotations
import html
import json
from datetime import datetime
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"

def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)

def source_link(url: str, label: str) -> str:
    if not url:
        return '<span class="muted">Not published</span>'
    return f'<a href="{esc(url)}" rel="external nofollow" target="_blank">{esc(label)} ↗</a>'

def generate(root: Path, today: str | None = None) -> Path:
    today = today or datetime.today().strftime("%Y-%m-%d")
    tools = {t["slug"]: t for t in json.loads((root / "data/tools.json").read_text())}
    records = {r["slug"]: r for r in json.loads((root / "data/tool_sources.json").read_text()).get("tools", [])}
    rows = []
    for slug, tool in sorted(tools.items(), key=lambda item: item[1].get("name", "")):
        rec = records.get(slug, {})
        unresolved = rec.get("unresolved_claims") or []
        unresolved_text = "; ".join(str(x) for x in unresolved) if unresolved else "None recorded"
        notes = rec.get("verification_notes") or "Official source links recorded in the site data ledger."
        rows.append(
            f'<tr id="evidence-{esc(slug)}"><td><strong><a href="/tools/{esc(slug)}/">{esc(tool.get("name", slug))}</a></strong><br><span class="muted">{esc(tool.get("category", ""))}</span></td>'
            f'<td><strong>{esc(rec.get("pricing_checked_date", "—"))}</strong><br>{source_link(rec.get("pricing_url", ""), "Pricing")}</td>'
            f'<td>{source_link(rec.get("docs_url", ""), "Docs")}<br>{source_link(rec.get("privacy_url", ""), "Privacy")}<br>{source_link(rec.get("rights_url", ""), "Rights")}</td>'
            f'<td>{esc(notes)}<br><span class="muted">Unresolved: {esc(unresolved_text)}</span></td></tr>'
        )
    schema = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "AIToolsEssentials Evidence Ledger", "url": f"{DOMAIN}/evidence/", "dateModified": today, "description": "Public source ledger for AI tool pricing, documentation, privacy, rights, and unresolved claims.", "publisher": {"@type": "Organization", "name": "AIToolsEssentials"}})
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Public evidence ledger for AIToolsEssentials: official pricing, documentation, privacy, rights sources, checked dates, verification notes, and unresolved claims for {len(tools)} AI tools."><title>Evidence Ledger — Sources, Dates &amp; Unresolved Claims | AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/evidence/"><meta property="og:title" content="Evidence Ledger — AIToolsEssentials"><meta property="og:description" content="Trace every AI tool claim to an official source and checked date."><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg"><link rel="stylesheet" href="/css/styles.css"><link rel="stylesheet" href="/css/share.css"><script type="application/ld+json">{schema}</script></head><body>
<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/categories/">Categories</a><a href="/guides/switch-guides/">Switching</a><a href="/pricing-watch/">Pricing Watch</a><a href="/benchmarks/">Benchmarks</a></nav><a class="nav-cta" href="/premium/">Premium</a></header><main>
<section class="scene scene-dark"><div class="evidence-hero"><p class="kicker">Trust layer · public source ledger</p><h1>Trace the claim before you trust it.</h1><p class="subhead">Every tool below has a public evidence row: official pricing, documentation, privacy and rights links where published, the last checked date, verification notes, and unresolved claims.</p><p><a class="button button-blue" href="/pricing-watch/">Open Pricing Watch</a><a class="button button-dark" href="/methodology/">Read our methodology</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="evidence-principles"><div><strong>Official first</strong><span>Vendor sources before summaries or third-party claims.</span></div><div><strong>Dated</strong><span>Pricing rows show the last verification date.</span></div><div><strong>Unresolved is visible</strong><span>Missing rights or policy pages are labeled, not guessed.</span></div></div><div class="evidence-table-hint">On mobile, swipe the evidence table horizontally to view all source columns.</div><div class="table-wrap evidence-table"><table><thead><tr><th>Tool</th><th>Pricing evidence</th><th>Policy &amp; rights</th><th>Verification notes</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div><p class="affiliate-inline">Methodology: source links are stored in <code>data/tool_sources.json</code> and regenerated into this public ledger. Editorial ratings are independent; affiliate relationships never determine scores. Prices and policies change — confirm the vendor source before purchasing.</p><section class="score-card evidence-next"><span>Use the evidence</span><h2>Now turn research into a decision.</h2><p><a class="button button-blue" href="/decision-brief.html">Generate a decision brief</a><a class="button button-dark" href="/compare-shortlist.html">Compare a shortlist</a></p></section></div></section></main><footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a><a href="/legal/corrections.html">Corrections</a><a href="mailto:contact@aitoolsessentials.com">Contact</a></footer><script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script></body></html>'''
    out = root / "evidence" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)
    return out


def postprocess_reviews(root: Path) -> int:
    """Add an exact source-ledger anchor to every generated review page."""
    marker = "<!-- AIT EVIDENCE LINK START -->"
    records = {r["slug"]: r for r in json.loads((root / "data" / "tool_sources.json").read_text()).get("tools", [])}
    block_template = '\n{marker}<p class="evidence-link"><span class="evidence-badge">Source check: {checked}</span><a href="/evidence/#evidence-{slug}">Trace this review\'s pricing, policy, and rights sources in the public Evidence Ledger →</a></p><!-- AIT EVIDENCE LINK END -->\n'
    changed = 0
    for page in sorted((root / "tools").glob("*/index.html")):
        slug = page.parent.name
        html_text = page.read_text()
        import re
        html_text = re.sub(re.escape(marker) + r".*?<!-- AIT EVIDENCE LINK END -->\n?", "\n", html_text, flags=re.S)
        block = block_template.format(marker=marker, slug=slug, checked=records.get(slug, {}).get("pricing_checked_date", "date unavailable"))
        if "</main>" in html_text:
            html_text = html_text.replace("</main>", block + "</main>", 1)
            page.write_text(html_text)
            changed += 1
    return changed


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    print(generate(root))
