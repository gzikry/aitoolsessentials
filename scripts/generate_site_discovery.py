#!/usr/bin/env python3
"""Generate discovery, browser metadata, and trust/navigation surfaces."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from affiliate_util import inject_nous_referral_module

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
HEADER = '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/stack-builder.html">Stack builder</a><a href="/tool-finder.html">Tool finder</a><a href="/free-ai-tools.html">Free AI tools</a><a href="/alternatives/">Alternatives</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/articles/index.html">Guides</a><a href="/deals/">Deals</a></nav><a class="nav-cta" href="/pricing/">Paid Premium</a></header>'
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
            {"name": "Stack Audit", "url": "/stack-audit.html", "description": "Audit the tools you already pay for."},
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
        ("Find tools", [("All tools", "/tools/index.html"), ("Tool Finder", "/tool-finder.html"), ("Fit Interview", "/fit-interview/"), ("Workflow guides", "/workflows/"), ("Local AI Planner", "/local-ai-planner/"), ("Confidence Check", "/confidence-check/"), ("Free AI tools", "/free-ai-tools.html"), ("Best AI tools", "/comparisons/best-ai-tools.html"), ("Best-for roles", "/best-for/"), ("Stack gallery", "/stacks/"), ("Glossary", "/glossary/")]),
        ("Decide", [("Stack Builder", "/stack-builder.html"), ("Cost Calculator", "/cost-calculator.html"), ("Free Stack Audit", "/stack-audit.html"), ("Automation Billing Decoder", "/automation-cost-decoder/"), ("Compare Shortlist", "/compare-shortlist.html"), ("Alternatives", "/alternatives/"), ("Pricing Watch", "/pricing-watch/"), ("Keep/Cut Weekly", "/newsletter/"), ("Paid Premium", "/premium/"), ("Premium preview", "/premium/library/")]),
        ("Trust", [("Changelog", "/changelog/"), ("Change Radar", "/change-radar/"), ("Model lineups", "/model-lineups/"), ("How-to library", "/how-to/"), ("Hardware guide", "/hardware/"), ("Evidence ledger", "/evidence/"), ("Methodology", "/methodology/"), ("Community reports", "/community/test-report.html"), ("Get reviewed", "/get-reviewed/"), ("Affiliate disclosure", "/legal/affiliate-disclosure.html")]),
        ("Distribution", [("Launch Kit", "/launch-kit/"), ("Vendor Badges", "/badges/"), ("Press / cite us", "/press/"), ("Weekly", "/weekly/"), ("Site status", "/status/"), ("RSS feed", "/feed.xml")]),
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
        ("I need to control cost", "Use the Cost Calculator before subscriptions sprawl, or decode automation billing units for Zapier, Make, and n8n.", "/automation-cost-decoder/", "Decode automation cost"),
        ("I am paying for overlapping AI tools", "Run the free instant Stack Audit first. Keep/Cut Weekly is the free email. Premium is a separate $12/month Whop membership.", "/stack-audit.html", "Free Stack Audit"),
        ("I am replacing a tool", "Open the Alternatives hub and compare before switching.", "/alternatives/", "Compare alternatives"),
        ("I want the $12/month membership", "Premium is $12/month on Whop: dated keep/cut research, monthly CSV, weekly checklist, alerts, and a written reply. Code LAUNCH50 for 50% off the first paid month.", "/premium/", "See what $12 buys"),
        ("I need dated prices", "Open Pricing Watch for official snapshots with checked dates. No invented history.", "/pricing-watch/", "Open Pricing Watch"),
        ("I want to cite this site", "Use the press page, methodology, and evidence ledger. Do not invent traffic or rankings.", "/press/", "Press / cite us"),
        ("I am a vendor", "Use Get Reviewed for editorial submission and correction rules.", "/get-reviewed/", "Get reviewed"),
    ]
    cards = "".join(f'<article class="content-hub-card"><span>Start here</span><h3>{esc(title)}</h3><p>{esc(text)}</p><a class="button button-blue small" href="{href}">{esc(cta)}</a></article>' for title, text, href, cta in steps)
    page = f'<!doctype html><html lang="en">{head("Start Here | AIToolsEssentials", "Pick the job you need done: find a tool, cut overlap, check cost, or join Paid Premium.", DOMAIN+"/start-here/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Start here</p><h1>Pick the job. Then open the page that does it.</h1><p class="subhead">Skip the directory maze. Start with what you need to decide this week.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{cards}</div></div></section></main>{FOOTER}{scripts()}</body></html>'
    page = inject_nous_referral_module(page)
    out = root / "start-here" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)


def generate_status(root: Path, tools: list[dict[str, Any]], today: str) -> None:
    html_count = len(list(root.rglob("*.html")))
    source_data = json.loads((root / "data/tool_sources.json").read_text())
    source_records = source_data.get("tools", [])
    if not isinstance(source_records, list):
        raise ValueError("data/tool_sources.json tools must be a list")
    valid_pricing_dates = []
    undated_or_invalid = 0
    for record in source_records:
        if not isinstance(record, dict):
            raise ValueError("data/tool_sources.json tools entries must be objects")
        value = str(record.get("pricing_checked_date", ""))
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                raise ValueError
            datetime.strptime(value, "%Y-%m-%d")
            valid_pricing_dates.append(value)
        except ValueError:
            undated_or_invalid += 1
    pricing_dates = sorted(set(valid_pricing_dates))
    latest_pricing = pricing_dates[-1] if pricing_dates else None
    pricing_checked = sum(1 for x in source_records if x.get("pricing_checked_date") == latest_pricing) if latest_pricing else 0
    hardware_data = root / "data/hardware.json"
    if hardware_data.exists():
        hardware_payload = json.loads(hardware_data.read_text())
        if isinstance(hardware_payload, list):
            hardware_records = len(hardware_payload)
        elif isinstance(hardware_payload, dict) and isinstance(hardware_payload.get("hardware"), list):
            hardware_records = len(hardware_payload["hardware"])
        else:
            raise ValueError("data/hardware.json must be a list or an object with a hardware list")
    else:
        hardware_records = 0
    data = {
        "site": "AIToolsEssentials",
        "domain": DOMAIN,
        "last_generated": today,
        "tools_tracked": len(tools),
        "html_pages": html_count,
        "evidence_freshness": {
            "pricing_records": len(source_records),
            "latest_pricing_checked": latest_pricing,
            "pricing_checked_on_latest_date": pricing_checked,
            "pricing_older_than_latest": max(0, len(source_records) - pricing_checked - undated_or_invalid),
            "pricing_undated_or_invalid": undated_or_invalid,
        },
        "hardware_records": hardware_records,
        "feeds": ["/feed.xml", "/weekly/feed.xml", "/changelog/feed.xml"],
        "core_utilities": ["/stack-builder.html", "/tool-finder.html", "/fit-interview/", "/workflows/", "/local-ai-planner/", "/confidence-check/", "/change-radar/", "/model-lineups/", "/how-to/", "/hardware/", "/cost-calculator.html", "/compare-shortlist.html", "/stack-audit.html"],
        "editorial_boundaries": "Affiliate/sponsor relationships do not change editorial scoring; corrections are verified against official sources before publication.",
    }
    (root / "site-status.json").write_text(json.dumps(data, indent=2) + "\n")
    latest_label = latest_pricing or "no recorded date"
    status_path = root / "status" / "index.html"
    existing_status = status_path.read_text() if status_path.exists() else ""
    preserved_head_blocks = []
    for pattern in (r'<!-- AIT DISCOVERY LINKS -->.*?<script src="/js/discovery\.js" defer></script>', r'<!-- AIT KNOWLEDGE SCHEMA START -->.*?<!-- AIT KNOWLEDGE SCHEMA END -->', r'<!-- AIT STRUCTURED DATA START -->.*?<!-- AIT STRUCTURED DATA END -->'):
        preserved_head_blocks.extend(re.findall(pattern, existing_status, flags=re.S))
    page = f'<!doctype html><html lang="en">{head("AIToolsEssentials Site Status", "Machine-readable and human-readable status snapshot for AIToolsEssentials coverage, feeds, utilities, and editorial boundaries.", DOMAIN+"/status/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Site status</p><h1>Coverage and freshness snapshot.</h1><p class="subhead">A transparent status page for what the site tracks and how to verify updates.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell"><div class="score-card"><span>Generated {esc(today)}</span><h2>{len(tools)} tools · {html_count} HTML pages</h2><p>Feeds, sitemap, stack utilities, alternatives pages, and correction modules are generated through the static pipeline.</p><p><span style="font-weight:700">Evidence freshness:</span> {pricing_checked}/{len(source_records)} pricing records checked on {esc(latest_label)} · {max(0, len(source_records) - pricing_checked - undated_or_invalid)} older records · {undated_or_invalid} undated/invalid · {hardware_records} hardware records.</p><p><a class="button button-blue" href="/site-status.json">View JSON status</a><a class="button button-blue" href="/changelog/" style="margin-left:8px">View changelog</a></p></div></div></section></main>{FOOTER}{scripts()}</body></html>'
    if preserved_head_blocks:
        page = page.replace('</head>', '\n'.join(preserved_head_blocks) + '</head>', 1)
    out = status_path
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
        rel_parts = p.relative_to(root).parts
        if any(part.startswith(".") for part in rel_parts) or "go" in rel_parts:
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
