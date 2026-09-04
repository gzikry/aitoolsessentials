#!/usr/bin/env python3
"""Generate the free, no-login Stack Audit page and catalog contract."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from premium_copy import BUY_PAGE_LABEL, post_audit_upgrade_html
from stack_audit_lib import build_catalog, catalog_index

DOMAIN = "https://aitoolsessentials.com"
HEADER = (
    '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span>'
    '<span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a>'
    '<a href="/stack-builder.html">Stack builder</a><a href="/cost-calculator.html">Cost calculator</a>'
    '<a href="/decision-brief.html">Decision brief</a><a href="/stack-audit.html" aria-current="page">Stack audit</a>'
    '</nav><a class="nav-cta" href="/pricing/">Paid Premium</a></header>'
)
FOOTER = (
    '<footer class="footer"><span>© 2026 AIToolsEssentials</span>'
    '<a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a>'
    '<a href="/legal/terms.html">Terms</a><a href="/legal/affiliate-disclosure.html">Disclosure</a>'
    '<a href="mailto:contact@aitoolsessentials.com">Contact</a></footer>'
)
LINK_MARK = "<!-- AIT STACK AUDIT LINK -->"


def esc(value: Any) -> str:
    return (
        str(value or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def generate_page(root: Path, catalog: dict[str, Any]) -> Path:
    today = catalog.get("generated_at") or date.today().isoformat()
    count = len(catalog.get("tools", []))
    desc = (
        "Free, no-login AI stack audit. Enter the tools you already pay for, "
        "see overlap, keep/cut advice, and a personal efficiency score. "
        "Nothing is submitted to a server."
    )
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "AI Stack Audit",
        "applicationCategory": "UtilityApplication",
        "operatingSystem": "Web",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "url": f"{DOMAIN}/stack-audit.html",
        "dateModified": today,
        "description": desc,
        "publisher": {"@type": "Organization", "name": "AIToolsEssentials"},
    }, separators=(",", ":"))
    payload = json.dumps({
        "generated_at": catalog["generated_at"],
        "policy": catalog["policy"],
        "rules": catalog["rules"],
        "tools": [
            {
                "slug": item["slug"],
                "name": item["name"],
                "category": item["category"],
                "official_url": item["official_url"],
                "review_url": item["review_url"],
                "price_label": item["price_label"],
                "pricing_summary": item["pricing_summary"],
                "pricing_url": item["pricing_url"],
                "pricing_checked_date": item["pricing_checked_date"],
                "price_confidence": item["price_confidence"],
                "promotion_mentioned": item["promotion_mentioned"],
                "suggested_use_cases": item["suggested_use_cases"],
                "capability_confidence": item["capability_confidence"],
                "capabilities_known": item["capabilities_known"],
            }
            for item in catalog["tools"]
        ],
    }, ensure_ascii=False).replace("</", "<\\/")

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(desc)}">
<title>AI Stack Audit — Keep, cut, or review your tools</title>
<link rel="canonical" href="{DOMAIN}/stack-audit.html">
<meta property="og:title" content="AI Stack Audit">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/css/styles.css">
<link rel="stylesheet" href="/css/stack-audit.css">
<script type="application/ld+json">{schema}</script>
</head>
<body>
{HEADER}
<main>
<section class="scene scene-dark">
  <div style="max-width:920px;margin:0 auto;padding:88px 28px 64px;text-align:center">
    <p class="kicker">Free stack audit · no login · stays on your device</p>
    <h1>See what you actually pay for.</h1>
    <p class="subhead">This is the free instant scorecard — not Keep/Cut Weekly and not paid Premium. Pick the tools you already use. Enter what you pay — or mark spend unknown. See keep/cut advice, tools that do the same job, and how efficiently you spend. Affiliate status never changes the result.</p>
    <p><a class="button button-blue" href="#sa-app">Start the free audit</a>
       <a class="button button-ghost-dark" href="/premium/" style="margin-left:8px">{BUY_PAGE_LABEL}</a></p>
  </div>
</section>
<section class="scene scene-light content-hub" id="sa-app">
  <div class="article-shell wide sa-wrap">
    <p class="sa-note">All {count} directory tools are selectable. Official pricing notes are dated source text, not auto-filled bills. The cost calculator’s $20 / $35 planning heuristic is not used here.</p>
    <div class="sa-progress" aria-label="Audit steps">
      <div class="sa-progress-step" data-step="1">1. Select tools</div>
      <div class="sa-progress-step" data-step="2">2. Spend &amp; use</div>
      <div class="sa-progress-step" data-step="3">3. Results</div>
    </div>
    <p id="sa-error" class="sa-error" role="alert"></p>
    <p id="sa-live" class="sa-status vis-hidden" aria-live="polite"></p>

    <section class="score-card sa-panel" id="sa-step-1">
      <h2>Select the tools you already have</h2>
      <p>Search the directory or add a custom tool. Limit {catalog["rules"]["max_tools"]} tools so share links stay short.</p>
      <label class="sa-field" for="sa-search">Search tools</label>
      <input class="sa-search" id="sa-search" type="search" placeholder="Search by name or category" autocomplete="off">
      <div id="sa-chips" class="sa-chips" aria-label="Selected tools"></div>
      <div id="sa-tool-grid" class="sa-tool-grid"></div>
      <div class="sa-custom">
        <label class="vis-hidden" for="sa-custom-name">Custom tool name</label>
        <input id="sa-custom-name" type="text" maxlength="40" placeholder="Custom tool name">
        <button class="button button-blue" type="button" id="sa-add-custom">Add custom tool</button>
      </div>
      <div class="sa-actions">
        <button class="button button-blue" type="button" id="sa-to-step-2">Continue to spend &amp; use cases</button>
      </div>
    </section>

    <section class="sa-panel" id="sa-step-2" hidden>
      <h2 id="sa-config-heading" tabindex="-1">Enter spend and how you use each tool</h2>
      <p>Actual spend is whatever you type. “Free + paid” in the directory is not treated as a paid bill.</p>
      <div id="sa-config-cards"></div>
      <div class="sa-actions">
        <button class="button button-dark" type="button" id="sa-back-1">Back</button>
        <button class="button button-blue" type="button" id="sa-run">See my audit</button>
      </div>
    </section>

    <section class="sa-results" id="sa-results" hidden>
      <h2 id="sa-results-heading" tabindex="-1">Your audit</h2>
      <div id="sa-result-body"></div>
      <section class="score-card sa-policy">
        <span>Editorial policy</span>
        <h3>Money and affiliation do not buy a recommendation.</h3>
        <p>Affiliate or sponsor status never changes the score, inclusion, tools that do the same job, badges, or Keep / Cut / Replace / Review / Trial first advice.</p>
      </section>
      <section class="score-card">
        <span>Share &amp; export</span>
        <h3>Private by default</h3>
        <p>Share links live in the URL fragment and stay in the browser. Exact spend is omitted unless you opt in. Session memory is automatic; lasting local save requires the button below. Nothing is posted to AIToolsEssentials.</p>
        <label><input type="checkbox" id="sa-share-spend"> Include exact spend in the public share link</label>
        <div class="sa-actions">
          <button class="button button-blue" type="button" id="sa-copy-link">Copy share link</button>
          <button class="button button-dark" type="button" id="sa-print">Print / PDF</button>
          <button class="button button-dark" type="button" id="sa-json">Download JSON</button>
          <button class="button button-dark" type="button" id="sa-csv">Download CSV</button>
          <button class="button button-dark" type="button" id="sa-text">Download text</button>
          <button class="button button-dark" type="button" id="sa-save-local">Save on this device</button>
          <button class="button button-dark" type="button" id="sa-load-local">Load local save</button>
        </div>
      </section>
      {post_audit_upgrade_html()}
      <div id="sa-premium-panel"></div>
      <div class="sa-actions">
        <button class="button button-dark" type="button" id="sa-back-2">Edit answers</button>
        <button class="button button-blue" type="button" id="sa-restart">Start over</button>
        <a class="button button-ghost-dark" data-sa-cta href="/newsletter/">Free Keep/Cut Weekly</a>
        <a class="button button-ghost-dark" data-sa-cta href="/premium/">{BUY_PAGE_LABEL}</a>
      </div>
    </section>
  </div>
</section>
</main>
{FOOTER}
<script type="application/json" id="sa-catalog">{payload}</script>
<script src="/js/stack-audit.js" defer></script>
<script src="/js/site.js" defer></script>
<script src="/js/analytics.js" defer></script>
</body>
</html>
'''
    out = root / "stack-audit.html"
    out.write_text(html)
    return out


def write_catalog(root: Path, catalog: dict[str, Any]) -> Path:
    path = root / "data" / "stack_audit_catalog.json"
    path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
    return path


def upsert_sitemap(root: Path, today: str) -> None:
    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        return
    loc = f"{DOMAIN}/stack-audit.html"
    text = sitemap.read_text()
    if loc in text:
        return
    entry = f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'
    text = text.replace("</urlset>", entry + "</urlset>")
    sitemap.write_text(text)


def inject_link(path: Path, html: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text()
    if "stack-audit.html" in text and LINK_MARK in text:
        return False
    if LINK_MARK in text:
        return False
    if "</main>" not in text:
        return False
    updated = text.replace("</main>", html + "\n</main>", 1)
    if updated == text:
        return False
    path.write_text(updated)
    return True


def postprocess(root: Path) -> int:
    changed = 0
    scoped = (
        f'{LINK_MARK}<p class="sa-crosslink" style="text-align:center;margin-top:18px">'
        '<a class="button button-ghost-dark" href="/stack-audit.html">'
        "Already paying for tools? Run a free Stack Audit →</a></p>"
    )
    for rel in ("stack-builder.html", "cost-calculator.html", "decision-brief.html"):
        if inject_link(root / rel, scoped):
            changed += 1
    return changed


def generate(root: Path, today: str | None = None) -> dict[str, Any]:
    today = today or date.today().isoformat()
    catalog = build_catalog(root, today)
    write_catalog(root, catalog)
    generate_page(root, catalog)
    upsert_sitemap(root, today)
    catalog_index(catalog)
    return catalog


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    catalog = generate(root)
    print(f"Generated stack audit for {len(catalog['tools'])} tools")
    print("Crosslinks:", postprocess(root))
