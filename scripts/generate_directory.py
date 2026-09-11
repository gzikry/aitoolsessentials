#!/usr/bin/env python3
"""Generate the /tools/ directory index from data/tools.json.

The directory page must list every tracked tool. It previously drifted to a
39-tool subset because no generator owned the file. This generator is the
single source of truth for /tools/index.html.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

from affiliate_util import approved_programs

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"

HEADER = (
    '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span>'
    '<span>AIToolsEssentials</span></a><nav class="nav-links">'
    '<a href="/tools/index.html" aria-current="page">Tools</a>'
    '<a href="/comparisons/best-ai-tools.html">Best AI tools</a>'
    '<a href="/categories/index.html">Categories</a>'
    '<a href="/articles/index.html">Guides</a>'
    '<a href="/benchmarks/">Benchmarks</a>'
    '<a href="/articles/learn.html">Learn</a>'
    '<a href="/guides/switch-guides/">Switching</a>'
    '</nav><a class="nav-cta" href="/premium/">Paid Premium</a></header>'
)

FOOTER = (
    '<div id="share-row" hidden></div>\n'
    '<footer class="footer"><span>© 2026 AIToolsEssentials</span>'
    '<a href="/advertise/index.html" rel="nofollow">Advertise</a>'
    '<a href="/submit-tool.html" rel="nofollow">Submit a tool</a>'
    '<a href="/community/test-report.html" rel="nofollow">Report your results</a>'
    '<a href="/badges/">Badges</a>'
    '<a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>'
    '<a href="/legal/about.html">About</a>'
    '<a href="/legal/privacy.html">Privacy</a>'
    '<a href="/legal/terms.html">Terms</a>'
    f'<a href="mailto:{EMAIL}">Contact</a></footer>'
)


def esc(value: object) -> str:
    return (
        str(value or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def search_terms(tool: dict) -> str:
    """Searchable haystack for the client-side filter (data-use)."""
    parts: list[str] = []
    for key in ("best_for", "summary", "description", "price"):
        value = tool.get(key)
        if isinstance(value, str):
            parts.append(value)
    for key in ("use_cases", "key_features", "features"):
        value = tool.get(key)
        if isinstance(value, list):
            parts.extend(str(v) for v in value)
        elif isinstance(value, str):
            parts.append(value)
    haystack = " ".join(parts).lower()
    words = [w.strip(".,()/") for w in haystack.split()]
    seen: list[str] = []
    for word in words:
        if len(word) > 2 and word not in seen:
            seen.append(word)
    return " ".join(seen)


def visit_link(tool: dict, programs: dict) -> tuple[str, str, str]:
    """Return (href, rel, label) for the outbound control on a card.

    Path A keeps affiliate placement limited to disclosed audit replace links, so
    the directory links to the official site with an external-relationship rel.
    """
    _ = programs
    return tool.get("official") or tool.get("url") or "", "external noopener nofollow", "Visit site"


def tool_card(tool: dict, programs: dict) -> str:
    rating = tool.get("rating")
    rating_text = f"{rating}/5" if rating else "Not yet scored"
    href, rel, label = visit_link(tool, programs)
    visit = (
        f'<a class="button button-blue small" href="{esc(href)}" rel="{rel}" '
        f'target="_blank" data-outbound="true">{esc(label)}</a>'
        if href
        else ""
    )
    return (
        f'<article class="directory-card" data-category="{esc(tool.get("category"))}" '
        f'data-name="{esc(tool["slug"])}" data-use="{esc(search_terms(tool))}">'
        f'<div><span class="category-pill">{esc(tool.get("category"))}</span>'
        f'<h3><a href="/tools/{esc(tool["slug"])}/">{esc(tool.get("name"))}</a></h3>'
        f'<p>{esc(tool.get("summary") or tool.get("description"))}</p></div>'
        f'<dl><dt>Best for</dt><dd>{esc(tool.get("best_for"))}</dd>'
        f'<dt>Price</dt><dd>{esc(tool.get("price"))}</dd>'
        f'<dt>Rating</dt><dd>{esc(rating_text)}</dd></dl>'
        f'<div class="card-actions">'
        f'<a class="text-link" href="/tools/{esc(tool["slug"])}/">Read review ›</a>'
        f'{visit}</div></article>'
    )


def generate(root: Path, tools: list[dict] | None = None, today: str | None = None) -> Path:
    loaded: list[dict] = tools if tools is not None else json.loads((root / "data/tools.json").read_text())
    today = today or __import__("datetime").date.today().isoformat()
    try:
        programs = approved_programs(root)
    except Exception:
        programs = {}

    count = len(loaded)
    categories = sorted({t.get("category", "") for t in loaded})
    pills = "".join(
        f'<a class="guide-pill" href="/categories/{quote(cat, safe="")}/">{esc(cat)}</a>'
        for cat in categories
    )
    cards = "\n".join(
        tool_card(t, programs)
        for t in sorted(loaded, key=lambda x: (x.get("category", ""), x.get("name", "")))
    )

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Browse all {count} AI tools we track by category, use case, price, and workflow fit. Every entry links to a full review with dated pricing evidence.">
<title>AI Tools Directory — {count} Reviewed Tools | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/tools/">
<link rel="stylesheet" href="../css/styles.css">
<link rel="stylesheet" href="../css/share.css">
<meta property="og:title" content="AI Tools Directory — AIToolsEssentials">
<meta property="og:description" content="Browse all {count} AI tools we track by category, use case, price, and workflow fit.">
<meta property="og:url" content="{DOMAIN}/tools/">
<meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<meta name="twitter:card" content="summary_large_image">
</head>
<body>
{HEADER}
<main>
<section class="scene scene-dark hero compact-hero"><div class="hero-copy"><p class="kicker">AI tools directory</p>
<h1>{count} AI tools organized by real workflows.</h1>
<p class="subhead">A continuously maintained shortlist for AI assistants, search, creative production, automation, development, productivity, meetings, audio, and video. Every listing links to a dated review.</p>
<p class="hero-secondary-links">Not sure where to start? <a href="/stack-audit.html">Run the free Stack Audit</a> · <a href="/tool-finder.html">Use the tool finder</a></p>
</div></section>
<section class="scene scene-light directory-section">
<div class="directory-toolbar">
<label for="toolSearch">Search tools</label>
<input id="toolSearch" type="search" placeholder="Try: Grok, research, video, coding, meetings…">
<p class="monetization-note">This is a living directory, not a claim that the market is finite. Affiliate status never changes ranking or inclusion; recommendations are organized by workflow fit first. <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</p>
</div>
<div class="category-related"><div class="guide-pills">{pills}</div></div>
<div class="directory-grid" id="toolGrid">
{cards}
</div>
<p class="directory-count" id="toolCount">{count} of {count} tools shown</p>
</section>
</main>
{FOOTER}
<script src="../js/directory.js"></script>
<script src="../js/tracking.js"></script>
<script src="../js/site.js" defer></script>
<script src="../js/cookie-consent.js" defer></script>
<script src="../js/analytics.js" defer></script>
</body>
</html>
'''
    out = root / "tools" / "index.html"
    out.write_text(html)
    return out


if __name__ == "__main__":
    from datetime import date

    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "data/tools.json").read_text())
    path = generate(root, data, date.today().isoformat())
    print(f"Generated tool directory: {path}")
