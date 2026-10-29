#!/usr/bin/env python3
"""Generate discovery, browser metadata, and trust/navigation surfaces."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from affiliate_util import inject_nous_referral_module
from site_scope import is_email_draft, is_public_rel, is_working_rel

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
HEADER = '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">ATE</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/stack-builder.html">Stack builder</a><a href="/tool-finder.html">Tool finder</a><a href="/free-ai-tools.html">Free AI tools</a><a href="/alternatives/">Alternatives</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/articles/index.html">Guides</a><a href="/deals/">Deals</a></nav><a class="nav-cta" href="/pricing/">Paid Premium</a></header>'
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
        "background_color": "#FAF8F5",
        "theme_color": "#FAF8F5",
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
  <Url type="text/html" template="{DOMAIN}/search/?q={{searchTerms}}"/>
</OpenSearchDescription>
'''
    (root / "opensearch.xml").write_text(xml)


def generate_human_sitemap(root: Path, tools: list[dict[str, Any]]) -> None:
    groups = [
        ("Find tools", [("All tools", "/tools/index.html"), ("Tool Finder", "/tool-finder.html"), ("Fit Interview", "/fit-interview/"), ("Workflow guides", "/workflows/"), ("Local AI Planner", "/local-ai-planner/"), ("Confidence Check", "/confidence-check/"), ("Free AI tools", "/free-ai-tools.html"), ("Best AI tools", "/comparisons/best-ai-tools.html"), ("Best-for roles", "/best-for/"), ("Stack gallery", "/stacks/"), ("Glossary", "/glossary/")]),
        ("Decide", [("Stack Builder", "/stack-builder.html"), ("Cost Calculator", "/cost-calculator.html"), ("Free Stack Audit", "/stack-audit.html"), ("Automation Billing Decoder", "/automation-cost-decoder/"), ("Compare Shortlist", "/compare-shortlist.html"), ("Alternatives", "/alternatives/"), ("Pricing Watch", "/pricing-watch/"), ("Keep, Test, Cut", "/newsletter/"), ("Paid Premium", "/premium/"), ("Premium preview", "/premium/library/")]),
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
        ("I am paying for overlapping AI tools", "Run the free instant Stack Audit first. Keep, Test, Cut is the free email. Premium is a separate $12/month membership, secure checkout by Stripe.", "/stack-audit.html", "Free Stack Audit"),
        ("I am replacing a tool", "Open the Alternatives hub and compare before switching.", "/alternatives/", "Compare alternatives"),
        ("I want the $12/month membership", "Run the free Stack Audit first. Premium is optional: dated keep/cut pack and a 48-hour written reply in Whop. $12/month — cheaper than one overlapping seat. Code LAUNCH50 for 50% off the first paid month.", "/premium/", "See Premium keep/cut pack"),
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
    # The public status page states a page count as a coverage claim, so it must
    # count public pages only: scratch captures under marketing/ are not pages.
    html_count = sum(
        1 for p in root.rglob("*.html")
        if is_public_rel(p.relative_to(root)) and p.name != "404.html"
        and 'name="robots" content="noindex' not in p.read_text()
    )
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
    for pattern in (r'<!-- AIT DISCOVERY LINKS -->[^\n]*?(?:<meta name="theme-color" content="#(?:5e6ad2|FAF8F5)">|<script src="/js/discovery\.js(?:\?[^"]*)?" defer></script>)', r'<!-- AIT KNOWLEDGE SCHEMA START -->.*?<!-- AIT KNOWLEDGE SCHEMA END -->', r'<!-- AIT STRUCTURED DATA START -->.*?<!-- AIT STRUCTURED DATA END -->'):
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
    links = marker + '<link rel="manifest" href="/site.webmanifest"><link rel="alternate" type="application/rss+xml" title="AIToolsEssentials updates" href="/feed.xml"><link rel="search" type="application/opensearchdescription+xml" title="AIToolsEssentials" href="/opensearch.xml"><meta name="theme-color" content="#FAF8F5"><script src="/js/discovery.js" defer></script>'
    # The content-hash pass rewrites this to `/js/discovery.js?v=<hash>`, so both patterns must
    # tolerate an optional query string. Matching the block only as far as the theme-color meta
    # (same line) keeps the match from running into unrelated markup, and the separate script
    # sweep then removes the stamped script the block left behind. Strip block -> strip stray
    # script -> insert one canonical block is idempotent for both the clean and the
    # double-inserted state.
    block_re = re.compile(
        r'[ \t]*<!-- AIT DISCOVERY LINKS -->[^\n]*?<meta name="theme-color" content="#(?:5e6ad2|FAF8F5)">'
    )
    script_re = re.compile(r'[ \t]*<script src="/js/discovery\.js(?:\?[^"]*)?" defer></script>')
    for p in root.rglob("*.html"):
        rel_parts = p.relative_to(root).parts
        if any(part.startswith(".") for part in rel_parts) or "go" in rel_parts:
            continue
        rel = p.relative_to(root)
        if is_working_rel(rel) or is_email_draft(rel):
            continue
        html = p.read_text()
        html = re.sub(
            r'(<meta\s+name="theme-color"\s+content=")#5e6ad2(")',
            r"\1#FAF8F5\2",
            html,
            flags=re.I,
        )
        html = block_re.sub("", html)
        html = script_re.sub("", html)
        if "</head>" in html:
            html = html.replace("</head>", links + "</head>", 1)
        p.write_text(html)


def postprocess_nav_search(root: Path) -> int:
    """Put a Search link in the header nav of every page.

    Search existed but was effectively unfindable: `/search/` was linked from 7 pages of 761 and
    absent from the homepage nav, so the site had a working search nobody could reach. There are
    58 distinct header-nav variants across the generators, which makes editing each template both
    large and easy to do half-way, so this inserts the link once, sitewide, after the Tools anchor
    that every variant already carries.

    Absolute `/search/` is used because the nav's own links are depth-relative in five different
    forms (`../tools/`, `../../tools/`, `/tools/`, ...) while an absolute path resolves correctly
    from any directory - the footer already relies on that.

    Idempotent: a page that already links /search/ from its header is left untouched.
    """
    link = '<a href="/search/">Search</a>'
    changed = 0
    tool_link = re.compile(r'<a[^>]*href="[^"]*tools/(?:index\.html)?"[^>]*>Tools</a>')
    for p in sorted(root.rglob('*.html')):
        rel = p.relative_to(root)
        if is_working_rel(rel) or not is_public_rel(rel):
            continue
        html = p.read_text(errors='ignore')
        # Match the class as a prefix, not an exact attribute: several generators emit
        # `class="nav-links home-appear"` with animation classes, and requiring the exact
        # `class="nav-links"` silently skipped them (the services pages and
        # automation-cost-decoder kept no Search link while 717 others got one).
        if not re.search(r'<nav[^>]*class="nav-links', html):
            continue
        head = html.split('</header>', 1)[0]
        if re.search(r'href="/search/"', head):
            continue
        m = tool_link.search(html)
        if m:
            html = html[: m.end()] + link + html[m.end():]
        else:
            # A few pages build a task-specific nav with no Tools anchor at all
            # (automation-cost-decoder/index.html links straight to Zapier/Make/n8n). Put the
            # link first there rather than skipping the page and leaving it without search.
            nav = re.search(r'<nav[^>]*class="nav-links[^>]*>', html)
            if not nav:
                continue
            html = html[: nav.end()] + link + html[nav.end():]
        p.write_text(html)
        changed += 1
    return changed


def postprocess_search_action(root: Path) -> int:
    """Normalise the schema.org SearchAction target to the page that actually applies ?q=.

    Every page advertised `/tools/index.html?q={search_term_string}`, but the tools page ignored
    the query string entirely, so Google's sitelinks search box and the OpenSearch provider both
    landed on an unfiltered directory. The generators now emit `/search/?q=`, and this pass exists
    because three pages (`contact.html`, `faq.html`, `services/ai-stack-audit.html`) are
    hand-maintained with no generator at all - a fix applied only to the generators would leave
    them wrong forever, with nothing to regenerate them.

    Idempotent: once replaced there is no remaining match.
    """
    stale = f'{DOMAIN}/tools/index.html?q={{search_term_string}}'
    fixed = f'{DOMAIN}/search/?q={{search_term_string}}'
    changed = 0
    for p in sorted(root.rglob('*.html')):
        rel = p.relative_to(root)
        if is_working_rel(rel) or not is_public_rel(rel):
            continue
        html = p.read_text(errors='ignore')
        if stale not in html:
            continue
        p.write_text(html.replace(stale, fixed))
        changed += 1
    return changed


HS_MARK_START = "<!-- AIT HEADER SEARCH START -->"
HS_MARK_END = "<!-- AIT HEADER SEARCH END -->"
HS_SCRIPTS_MARK = "<!-- AIT HEADER SEARCH SCRIPTS -->"
HS_STYLE_MARK = "<!-- AIT HEADER SEARCH STYLE -->"

HS_FORM = (
    HS_MARK_START
    + '<form class="ait-hs" id="ait-hs" role="search" action="/search/" method="get" autocomplete="off">'
    + '<span class="ait-hs-ico" aria-hidden="true">\u2315</span>'
    + '<input class="ait-hs-input" id="ait-hs-input" type="search" name="q" '
    + 'placeholder="Search\u2026" aria-label="Search AIToolsEssentials" '
    + 'role="combobox" aria-expanded="false" aria-controls="ait-hs-list" aria-autocomplete="list" '
    + 'autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search">'
    + '<ul class="ait-hs-list" id="ait-hs-list" role="listbox" aria-label="Search suggestions" hidden></ul>'
    + "</form>"
    + HS_MARK_END
)

# Inline so the widget looks identical on all 58 header-nav variants without depending on each
# page's cached stylesheet version. Scoped under .ait-hs so it cannot touch existing layout.
HS_CSS = (
    ".ait-hs{position:relative;display:flex;align-items:center;margin-left:6px}"
    ".ait-hs-ico{position:absolute;left:8px;font-size:14px;line-height:1;color:#111315;pointer-events:none}"
    ".ait-hs-input{width:186px;padding:6px 8px 6px 24px;border-radius:0;border:0;border-bottom:1px solid #111315;"
    "background:transparent;color:#111315;font:inherit;font-size:13px}"
    ".ait-hs-input::placeholder{color:rgba(17,19,21,.55)}"
    ".ait-hs-input:focus{outline:2px solid #8C2F2B;outline-offset:2px;border-color:#111315}"
    ".ait-hs-list{position:absolute;top:calc(100% + 6px);right:0;width:340px;max-width:86vw;z-index:60;"
    "margin:0;padding:6px;list-style:none;background:#FAF8F5;border:1px solid #111315;border-radius:0;"
    "box-shadow:none;max-height:60vh;overflow:auto}"
    ".ait-hs-list[hidden]{display:none}"
    ".ait-hs-item,.ait-hs-all,.ait-hs-note{display:block;padding:8px 10px;border-radius:0;"
    "text-decoration:none;color:#111315;cursor:pointer}"
    ".ait-hs-item:hover,.ait-hs-item.ait-hs-active,.ait-hs-all:hover,.ait-hs-all.ait-hs-active{background:#F7F5F0}"
    ".ait-hs-type{display:block;font-size:10px;font-weight:700;text-transform:uppercase;"
    "letter-spacing:.06em;color:#8C2F2B}"
    ".ait-hs-name{display:block;font-size:14px;font-weight:600;line-height:1.3}"
    ".ait-hs-name mark{background:#fff2a8;color:inherit;border-radius:2px;padding:0 1px}"
    ".ait-hs-all{margin-top:4px;border-top:1px solid #D8D2C5;font-size:12px;color:#8C2F2B;font-weight:600}"
    ".ait-hs-note{font-size:13px;color:rgba(17,19,21,.72)}"
    "@media (max-width:1100px){.ait-hs-input{width:132px}}"
    "@media (max-width:900px){.ait-hs{display:none}}"
)


def postprocess_header_search(root: Path) -> int:
    """Add a predictive search box to the header of every page.

    The /search/ page ranks well but a reader has to navigate to it before anything happens, so
    this starts suggesting on the first keystroke from any page. It reuses `js/search-core.js`,
    the same ranking engine the full page uses - two surfaces that order results differently would
    be a bug, because a reader who searched the same term twice would get two different answers.

    Degrades without JavaScript: the widget is a real `<form action="/search/" method="get">` with
    a named `q` input, so submitting lands on `/search/?q=` and that page renders it server-lessly.
    JS only adds the dropdown.

    Marker-delimited and rebuilt each run rather than appended, so it is idempotent; the script
    URLs carry a content hash so a changed JS file busts the browser cache (the previous search
    change did not, which is why a reader could keep seeing the old page).
    """
    core = root / "js" / "search-core.js"
    head = root / "js" / "header-search.js"
    if not core.exists() or not head.exists():
        return 0
    core_v = hashlib.sha256(core.read_bytes()).hexdigest()[:12]
    head_v = hashlib.sha256(head.read_bytes()).hexdigest()[:12]
    scripts = (
        f'{HS_SCRIPTS_MARK}<script src="/js/search-core.js?v={core_v}" defer></script>'
        f'<script src="/js/header-search.js?v={head_v}" defer></script>'
    )
    style = f"{HS_STYLE_MARK}<style>{HS_CSS}</style>"

    changed = 0
    for p in sorted(root.rglob("*.html")):
        rel = p.relative_to(root)
        if is_working_rel(rel) or not is_public_rel(rel):
            continue
        html = p.read_text(errors="ignore")
        original = html

        # Remove any previous injection first, so a rerun rebuilds rather than stacks.
        html = re.sub(re.escape(HS_MARK_START) + r".*?" + re.escape(HS_MARK_END), "", html, flags=re.S)
        html = re.sub(re.escape(HS_SCRIPTS_MARK) + r".*?header-search\.js[^>]*></script>", "", html, flags=re.S)
        html = re.sub(re.escape(HS_STYLE_MARK) + r"<style>.*?</style>", "", html, flags=re.S)

        if "</header>" not in html or "</body>" not in html:
            if html != original:
                p.write_text(html)
                changed += 1
            continue

        # Place the box before the header CTA when there is one, so it sits with the nav rather
        # than after the primary button.
        cta = re.search(r'<a[^>]*class="[^"]*nav-cta', html)
        if cta:
            html = html[: cta.start()] + HS_FORM + html[cta.start():]
        else:
            html = html.replace("</header>", HS_FORM + "</header>", 1)

        html = html.replace("</head>", style + "</head>", 1)
        html = html.replace("</body>", scripts + "</body>", 1)

        # Version the search assets wherever the page references them directly. The /search/ page
        # loads /js/search.js itself, and without a version a returning reader keeps running the
        # cached copy after an update — which is exactly why the previous search change could be
        # deployed and still not be visible.
        for name, ver in (("search-core.js", core_v), ("search.js", core_v)):
            html = re.sub(
                rf'src="/js/{re.escape(name)}(?:\?v=[^"]*)?"',
                f'src="/js/{name}?v={ver}"',
                html,
            )

        if html != original:
            p.write_text(html)
            changed += 1
    return changed


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
    nav_added = postprocess_nav_search(root)
    if nav_added:
        print(f"Search nav link added to {nav_added} pages")
    action_fixed = postprocess_search_action(root)
    if action_fixed:
        print(f"SearchAction target normalised on {action_fixed} pages")
    hs = postprocess_header_search(root)
    if hs:
        print(f"Predictive header search added to {hs} pages")


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    tools = json.loads((root / "data/tools.json").read_text())
    print(generate(root, tools))
    postprocess(root, tools)
