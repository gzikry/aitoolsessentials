#!/usr/bin/env python3
"""Generate discovery, browser metadata, and trust/navigation surfaces."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
HEADER = '<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/stack-builder.html">Stack builder</a><a href="/tool-finder.html">Tool finder</a><a href="/free-ai-tools.html">Free AI tools</a><a href="/alternatives/">Alternatives</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/articles/index.html">Guides</a><a href="/deals/">Deals</a></nav><a class="nav-cta" href="/pricing/">Premium</a></header>'
FOOTER = f'<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/advertise/index.html" rel="nofollow">Advertise</a><a href="/submit-tool.html" rel="nofollow">Submit a tool</a><a href="/community/test-report.html" rel="nofollow">Report your results</a><a href="/badges/">Badges</a><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a></footer>'


def esc(s: Any) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def head(title: str, desc: str, canonical: str) -> str:
    return f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{esc(desc)}"><title>{esc(title)}</title><link rel="canonical" href="{canonical}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/css/styles.css"></head>'


def scripts() -> str:
    return '<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>'


def generate_manifest(root: Path) -> None:
    manifest = {
        "name": "AIToolsEssentials",
        "short_name": "AI Tools",
        "description": "Find, compare, shortlist, and estimate the cost of practical AI tools.",
        "start_url": "/?source=pwa",
        "scope": "/",
        "display": "standalone",
        "background_color": "#08090a",
        "theme_color": "#5e6ad2",
        "categories": ["productivity", "business", "education"],
        "icons": [
            {"src": "/assets/aitools-bot-mark.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"},
            {"src": "/favicon.ico", "sizes": "16x16 32x32 48x48", "type": "image/x-icon"},
        ],
        "shortcuts": [
            {"name": "Stack Builder", "url": "/stack-builder.html", "description": "Generate a practical AI stack."},
            {"name": "Tool Finder", "url": "/tool-finder.html", "description": "Filter AI tools by job, budget, and buyer."},
            {"name": "Cost Calculator", "url": "/cost-calculator.html", "description": "Estimate monthly AI stack cost."},
            {"name": "Free AI Tools", "url": "/free-ai-tools.html", "description": "Browse free and freemium AI tools."},
        ],
    }
    (root / "site.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n")


def generate_opensearch(root: Path) -> None:
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
  <ShortName>AIToolsEssentials</ShortName>
  <Description>Search AIToolsEssentials AI tool reviews, stacks, alternatives, and guides.</Description>
  <InputEncoding>UTF-8</InputEncoding>
  <Image height="16" width="16" type="image/x-icon">{DOMAIN}/favicon.ico</Image>
  <Url type="text/html" template="{DOMAIN}/tools/index.html?q={{searchTerms}}"/>
</OpenSearchDescription>
'''
    (root / "opensearch.xml").write_text(xml)


def generate_human_sitemap(root: Path, tools: list[dict[str, Any]]) -> None:
    groups = [
        ("Find tools", [("All tools", "/tools/index.html"), ("Tool Finder", "/tool-finder.html"), ("Fit Interview", "/fit-interview/"), ("Confidence Check", "/confidence-check/"), ("Free AI tools", "/free-ai-tools.html"), ("Best AI tools", "/comparisons/best-ai-tools.html")]),
        ("Decide", [("Stack Builder", "/stack-builder.html"), ("Cost Calculator", "/cost-calculator.html"), ("Compare Shortlist", "/compare-shortlist.html"), ("Alternatives", "/alternatives/")]),
        ("Trust", [("Changelog", "/changelog/"), ("Community reports", "/community/test-report.html"), ("Get reviewed", "/get-reviewed/"), ("Affiliate disclosure", "/legal/affiliate-disclosure.html")]),
        ("Distribution", [("Launch Kit", "/launch-kit/"), ("Vendor Badges", "/badges/"), ("Weekly", "/weekly/"), ("RSS feed", "/feed.xml")]),
    ]
    cards = "".join(f'<article class="content-hub-card"><h3>{esc(title)}</h3><ul>' + "".join(f'<li><a href="{href}">{esc(label)}</a></li>' for label, href in links) + "</ul></article>" for title, links in groups)
    top_tools = "".join(f'<li><a href="/tools/{esc(t["slug"])}/">{esc(t["name"])}</a></li>' for t in tools[:40])
    page = f'<!doctype html><html lang="en">{head("AIToolsEssentials Site Map", "A human-readable map of AIToolsEssentials tools, stack utilities, alternatives, guides, feeds, and trust pages.", DOMAIN+"/site-map/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Site map</p><h1>Everything useful on AIToolsEssentials.</h1><p class="subhead">Jump to reviews, stack utilities, comparison pages, trust policies, launch assets, and update feeds.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{cards}</div><h2>Tool reviews</h2><div class="score-card"><ul class="directory-list">{top_tools}</ul></div></div></section></main>{FOOTER}{scripts()}</body></html>'
    out = root / "site-map" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)


def generate_start_here(root: Path) -> None:
    steps = [
        ("I need a tool now", "Use Tool Finder to narrow the list by workflow, budget, and buyer type.", "/tool-finder.html", "Open Tool Finder"),
        ("I need a full stack", "Use Stack Builder to generate a shareable role-specific stack.", "/stack-builder.html", "Build my stack"),
        ("I need to control cost", "Use the Cost Calculator before subscriptions sprawl.", "/cost-calculator.html", "Estimate cost"),
        ("I am replacing a tool", "Open the Alternatives hub and compare before switching.", "/alternatives/", "Compare alternatives"),
        ("I am a vendor", "Use Get Reviewed for editorial submission and correction rules.", "/get-reviewed/", "Get reviewed"),
    ]
    cards = "".join(f'<article class="content-hub-card"><span>Start here</span><h3>{esc(title)}</h3><p>{esc(text)}</p><a class="button button-blue small" href="{href}">{esc(cta)}</a></article>' for title, text, href, cta in steps)
    page = f'<!doctype html><html lang="en">{head("Start Here | AIToolsEssentials", "A guided first-visit page for choosing AI tools, building stacks, estimating cost, comparing alternatives, or submitting a vendor review.", DOMAIN+"/start-here/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Start here</p><h1>Choose the shortest path to a better AI stack.</h1><p class="subhead">Skip the directory maze. Pick the job you need done and jump to the right utility.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{cards}</div></div></section></main>{FOOTER}{scripts()}</body></html>'
    out = root / "start-here" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)


def generate_status(root: Path, tools: list[dict[str, Any]], today: str) -> None:
    html_count = len(list(root.rglob("*.html")))
    data = {
        "site": "AIToolsEssentials",
        "domain": DOMAIN,
        "last_generated": today,
        "tools_tracked": len(tools),
        "html_pages": html_count,
        "feeds": ["/feed.xml", "/weekly/feed.xml", "/changelog/feed.xml"],
        "core_utilities": ["/stack-builder.html", "/tool-finder.html", "/fit-interview/", "/confidence-check/", "/cost-calculator.html", "/compare-shortlist.html"],
        "editorial_boundaries": "Affiliate/sponsor relationships do not change editorial scoring; corrections are verified against official sources before publication.",
    }
    (root / "site-status.json").write_text(json.dumps(data, indent=2) + "\n")
    page = f'<!doctype html><html lang="en">{head("AIToolsEssentials Site Status", "Machine-readable and human-readable status snapshot for AIToolsEssentials coverage, feeds, utilities, and editorial boundaries.", DOMAIN+"/status/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Site status</p><h1>Coverage and freshness snapshot.</h1><p class="subhead">A transparent status page for what the site tracks and how to verify updates.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell"><div class="score-card"><span>Generated {esc(today)}</span><h2>{len(tools)} tools · {html_count} HTML pages</h2><p>Feeds, sitemap, stack utilities, alternatives pages, and correction modules are generated through the static pipeline.</p><p><a class="button button-blue" href="/site-status.json">View JSON status</a><a class="button button-blue" href="/changelog/" style="margin-left:8px">View changelog</a></p></div></div></section></main>{FOOTER}{scripts()}</body></html>'
    out = root / "status" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)


def generate_js(root: Path) -> None:
    js = r'''
(function(){
function initCopy(){document.querySelectorAll('[data-copy-current-url]').forEach(btn=>btn.addEventListener('click',()=>navigator.clipboard?.writeText(location.href).then(()=>{const old=btn.textContent;btn.textContent='Copied ✓';setTimeout(()=>btn.textContent=old,1400)})))}
document.addEventListener('DOMContentLoaded',initCopy);
})();
'''
    (root / "js" / "discovery.js").write_text(js)


def ensure_robots(root: Path) -> None:
    p = root / "robots.txt"
    text = p.read_text() if p.exists() else "User-agent: *\nAllow: /\n"
    additions = [
        f"Sitemap: {DOMAIN}/sitemap.xml",
        f"Sitemap: {DOMAIN}/feed.xml",
    ]
    for line in additions:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    p.write_text(text)


def postprocess_head_links(root: Path) -> None:
    marker = "<!-- AIT DISCOVERY LINKS -->"
    links = marker + '<link rel="manifest" href="/site.webmanifest"><link rel="alternate" type="application/rss+xml" title="AIToolsEssentials updates" href="/feed.xml"><link rel="search" type="application/opensearchdescription+xml" title="AIToolsEssentials" href="/opensearch.xml"><meta name="theme-color" content="#5e6ad2"><script src="/js/discovery.js" defer></script>'
    for p in root.rglob("*.html"):
        if any(part.startswith(".") for part in p.relative_to(root).parts):
            continue
        html = p.read_text()
        html = re.sub(r"\s*<!-- AIT DISCOVERY LINKS -->.*?<script src=\"/js/discovery\.js\" defer></script>", "", html, flags=re.S)
        if "</head>" in html:
            html = html.replace("</head>", links + "</head>", 1)
        p.write_text(html)


def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    if tools is None:
        tools = json.loads((root / "data/tools.json").read_text())
    today = today or datetime.today().strftime("%Y-%m-%d")
    generate_manifest(root)
    generate_opensearch(root)
    generate_human_sitemap(root, tools)
    generate_start_here(root)
    generate_js(root)
    ensure_robots(root)
    return 6


def postprocess(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> None:
    if tools is None:
        tools = json.loads((root / "data/tools.json").read_text())
    today = today or datetime.today().strftime("%Y-%m-%d")
    generate_status(root, tools, today)
    postprocess_head_links(root)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    tools = json.loads((root / "data/tools.json").read_text())
    print(generate(root, tools))
    postprocess(root, tools)
