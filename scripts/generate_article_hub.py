#!/usr/bin/env python3
"""Generate the complete searchable guides hub from published article files."""
from __future__ import annotations

import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://aitoolsessentials.com"


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title_parts: list[str] = []
        self.description = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "meta" and (data.get("name") or "").lower() == "description":
            self.description = data.get("content") or ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def classify(filename: str, title: str) -> str:
    text = f"{filename} {title}".lower()
    if filename == "learn.html":
        return "Start here"
    if filename.startswith("best-ai-tools-for-") or "best ai tools for" in text:
        return "Buyer guides by role"
    if any(token in text for token in ["-vs-", " vs ", "which-to-pay", "pick-one", "compare-"]):
        return "Comparisons & choose-one guides"
    if filename.startswith("how-to-") or title.lower().startswith("how to "):
        return "How-to guides"
    if filename.startswith(("is-", "does-", "can-", "what-")) or title.lower().startswith(("is ", "does ", "can ", "what ")):
        return "Questions answered"
    if any(token in text for token in ["stack", "subscription", "renewal", "pricing", "cost", "audit"]):
        return "Cost, renewals & stack control"
    return "Workflow & evaluation guides"


def collect(root: Path) -> list[dict]:
    pages = []
    for path in sorted((root / "articles").glob("*.html")):
        if path.name == "index.html":
            continue
        parser = HeadParser()
        parser.feed(path.read_text())
        title = clean("".join(parser.title_parts)) or path.stem.replace("-", " ").title()
        title = re.sub(r"\s+[—|-]\s+AIToolsEssentials.*$", "", title).strip()
        description = clean(parser.description) or "A practical AIToolsEssentials guide for evaluating AI tools and workflows."
        pages.append(
            {
                "filename": path.name,
                "title": title,
                "description": description,
                "group": classify(path.name, title),
            }
        )
    return pages


def generate(root: Path = ROOT) -> Path:
    pages = collect(root)
    order = [
        "Start here",
        "Comparisons & choose-one guides",
        "Buyer guides by role",
        "Cost, renewals & stack control",
        "How-to guides",
        "Questions answered",
        "Workflow & evaluation guides",
    ]
    grouped: dict[str, list[dict]] = {}
    for page in pages:
        grouped.setdefault(page["group"], []).append(page)

    sections = []
    for group in order:
        items = sorted(grouped.get(group, []), key=lambda item: item["title"].lower())
        if not items:
            continue
        cards = "".join(
            f'''<article class="content-hub-card" data-guide-card data-search="{esc((item['title'] + ' ' + item['description']).lower())}">
<span>{esc(group)}</span><h3><a href="{esc(item['filename'])}">{esc(item['title'])}</a></h3>
<p>{esc(item['description'])}</p><a class="text-link" href="{esc(item['filename'])}">Read guide →</a>
</article>'''
            for item in items
        )
        sections.append(
            f'''<section class="scene scene-light content-hub guide-hub-group" data-guide-group>
<div class="article-shell wide"><p class="kicker light" data-group-count data-total="{len(items)}">{len(items)} guides</p><h2>{esc(group)}</h2>
<div class="content-hub-grid">{cards}</div></div></section>'''
        )

    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "AIToolsEssentials AI tool guides",
        "numberOfItems": len(pages),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": page["title"],
                "url": f"{DOMAIN}/articles/{page['filename']}",
            }
            for index, page in enumerate(pages, start=1)
        ],
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": f"{DOMAIN}/articles/"},
        ],
    }

    document = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Search {len(pages)} practical AI tool buyer guides, comparisons, workflow evaluations, cost-control playbooks, and role-specific recommendations.">
<title>AI Tool Guides — {len(pages)} Practical Buyer Guides | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/articles/">
<link rel="stylesheet" href="../css/styles.css"><link rel="stylesheet" href="../css/share.css">
<link rel="icon" href="../assets/aitools-bot-mark.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="../assets/aitools-bot-logo-256.png">
<meta property="og:site_name" content="AIToolsEssentials"><meta property="og:type" content="website">
<meta property="og:title" content="AI Tool Guides — {len(pages)} Practical Buyer Guides">
<meta property="og:description" content="Practical AI tool comparisons, buyer guides, cost-control playbooks, and workflow evaluations.">
<meta property="og:url" content="{DOMAIN}/articles/"><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<script type="application/ld+json">{json.dumps(item_list, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False)}</script>
<link rel="manifest" href="/site.webmanifest"><link rel="alternate" type="application/rss+xml" title="AIToolsEssentials updates" href="/feed.xml"><script src="/js/discovery.js" defer></script>
</head><body>
<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a>
<nav class="nav-links"><a href="../tools/">Tools</a><a href="../comparisons/best-ai-tools.html">Best AI tools</a><a href="../categories/">Categories</a><a href="./">Guides</a><a href="../benchmarks/">Benchmarks</a><a href="learn.html">Learn</a><a href="../guides/switch-guides/">Switching</a></nav>
<a class="nav-cta" href="../newsletter/">Free newsletter</a></header>
<main>
<section class="scene scene-dark hero compact-hero"><div class="hero-copy"><p class="kicker">Practical AI buyer guides</p>
<h1>Find the guide for the decision in front of you.</h1>
<p class="subhead">Search {len(pages)} guides covering tool overlap, pricing, real workflows, role-specific stacks, cancellation decisions, and evaluation methods.</p>
<div class="actions"><a class="button button-blue" href="learn.html">Start with the learning path</a><a class="button button-dark" href="../tool-finder.html">Find a tool</a><a class="button button-dark" href="../pricing-watch/" style="margin-left:8px">Pricing Watch</a></div>
</div></section>
<section class="scene scene-light"><div class="article-shell wide">
<p class="kicker light">Search the library</p><h2>What are you deciding?</h2>
<label for="guide-filter">Filter by tool, role, workflow, or question</label>
<input id="guide-filter" type="search" placeholder="Try Cursor, small business, cancel, research…" style="width:100%;max-width:760px;padding:14px 16px;border:1px solid #c7c7cc;border-radius:12px;font:inherit">
<p id="guide-count" class="last-updated">Showing all {len(pages)} guides.</p>
</div></section>
{''.join(sections)}
<section class="score-card related-next-steps"><span>Free decision tools</span><h2>Turn a guide into a repeatable evaluation.</h2>
<p><a class="button button-blue" href="../compare-shortlist.html">Compare shortlist</a><a class="button button-blue" href="../cost-calculator.html" style="margin-left:8px">Estimate cost</a><a class="button button-dark" href="../downloads/ai-tool-evaluation-scorecard.html" style="margin-left:8px">Open scorecard</a></p>
<p><a href="../press/">Press / cite us</a> · <a href="../methodology/">Methodology</a> · <a href="../evidence/">Evidence ledger</a> · <a href="../newsletter/">Keep/Cut Weekly</a></p></section>
<section class="newsletter-panel"><div><span>Keep/Cut Weekly</span><h2>One tool to keep. One to cut. One worth testing.</h2>
<p>Get a concise weekly decision brief with pricing changes, overlap warnings, and one practical job to test.</p></div><div class="newsletter-actions"><a class="button button-blue" href="../newsletter/">Read the newsletter</a><a class="button button-dark" href="../premium/">Explore Premium</a></div></section>
<p class="affiliate-inline">Editorial recommendations are independent. Affiliate participation and paid placement never change rankings or conclusions. <a href="../legal/affiliate-disclosure.html">Disclosure</a>.</p>
</main><div id="share-row" hidden></div>
<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="../advertise/" rel="nofollow">Advertise</a><a href="../submit-tool.html" rel="nofollow">Submit a tool</a><a href="../legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:contact@aitoolsessentials.com">Contact</a><a href="../legal/about.html">About</a><a href="../legal/privacy.html">Privacy</a><a href="../legal/terms.html">Terms</a></footer>
<script>
(function() {{
  const input = document.getElementById('guide-filter');
  const cards = Array.from(document.querySelectorAll('[data-guide-card]'));
  const groups = Array.from(document.querySelectorAll('[data-guide-group]'));
  const count = document.getElementById('guide-count');
  if (!input) return;
  input.addEventListener('input', function() {{
    const query = input.value.trim().toLowerCase();
    let visible = 0;
    cards.forEach(function(card) {{
      const show = !query || card.dataset.search.includes(query) || card.textContent.toLowerCase().includes(query);
      card.hidden = !show;
      if (show) visible += 1;
    }});
    groups.forEach(function(group) {{
      const groupCards = Array.from(group.querySelectorAll('[data-guide-card]'));
      const groupVisible = groupCards.filter(function(card) {{ return !card.hidden; }}).length;
      group.hidden = groupVisible === 0;
      const groupCount = group.querySelector('[data-group-count]');
      if (groupCount) {{
        const total = groupCount.dataset.total;
        groupCount.textContent = query ? groupVisible + (groupVisible === 1 ? ' guide' : ' guides') : total + ' guides';
      }}
    }});
    count.textContent = query ? 'Showing ' + visible + ' matching guides.' : 'Showing all {len(pages)} guides.';
  }});
}})();
</script>
<script src="../js/site.js" defer></script><script src="../js/analytics.js" defer></script>
</body></html>'''

    output = root / "articles" / "index.html"
    output.write_text(document)
    print(f"Generated article hub: {len(pages)} guides")
    return output


if __name__ == "__main__":
    generate()
