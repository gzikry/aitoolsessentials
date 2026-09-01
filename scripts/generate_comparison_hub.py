#!/usr/bin/env python3
"""Generate the comparison hub from every published comparison page."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://aitoolsessentials.com"
EXCLUDED = {"index.html"}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def extract(pattern: str, source: str, fallback: str = "") -> str:
    match = re.search(pattern, source, flags=re.I | re.S)
    return html.unescape(re.sub(r"\s+", " ", match.group(1)).strip()) if match else fallback


def classify(filename: str) -> str:
    name = filename.lower()
    groups = [
        ("Coding", ("cursor", "copilot", "github")),
        ("Automation", ("zapier", "make-vs", "n8n")),
        ("Creative & video", ("midjourney", "canva", "runway", "pika", "heygen", "synthesia")),
        ("Marketing & writing", ("jasper", "copy-ai")),
        ("Assistants & research", ("chatgpt", "claude", "gemini", "grok", "perplexity", "deepseek")),
    ]
    for label, tokens in groups:
        if any(token in name for token in tokens):
            return label
    return "Other comparisons"


def collect_pages(root: Path) -> list[dict]:
    pages = []
    for path in sorted((root / "comparisons").glob("*.html")):
        if path.name in EXCLUDED:
            continue
        source = path.read_text()
        title = extract(r"<title>(.*?)</title>", source, path.stem.replace("-", " ").title())
        title = re.sub(r"\s+[—|-]\s+AIToolsEssentials.*$", "", title).strip()
        description = extract(
            r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
            source,
            "Compare workflow fit, pricing, evidence, and practical trade-offs.",
        )
        pages.append(
            {
                "filename": path.name,
                "title": title,
                "description": description,
                "group": "Best-of shortlist" if path.name == "best-ai-tools.html" else classify(path.name),
            }
        )
    return pages


def generate(root: Path = ROOT) -> Path:
    pages = collect_pages(root)
    groups: dict[str, list[dict]] = {}
    order = ["Best-of shortlist", "Assistants & research", "Coding", "Creative & video", "Automation", "Marketing & writing", "Other comparisons"]
    for page in pages:
        groups.setdefault(page["group"], []).append(page)

    sections = []
    for group in order:
        entries = sorted(groups.get(group, []), key=lambda item: item["title"].lower())
        if not entries:
            continue
        cards = "".join(
            f'''<article class="content-hub-card" data-comparison-card data-search="{esc(item['title'].lower())}">
<h3><a href="{esc(item['filename'])}">{esc(item['title'])}</a></h3>
<p>{esc(item['description'])}</p>
<a class="text-link" href="{esc(item['filename'])}">Compare →</a>
</article>'''
            for item in entries
        )
        sections.append(
            f'''<section class="scene scene-light content-hub comparison-hub-group">
<div class="article-shell wide"><p class="kicker light">{esc(group)}</p><h2>{esc(group)}</h2>
<div class="content-hub-grid">{cards}</div></div></section>'''
        )

    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "AIToolsEssentials AI tool comparisons",
        "numberOfItems": len(pages),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": page["title"],
                "url": f"{DOMAIN}/comparisons/{page['filename']}",
            }
            for index, page in enumerate(pages, start=1)
        ],
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": "Comparisons", "item": f"{DOMAIN}/comparisons/"},
        ],
    }

    document = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Browse {len(pages)} independent AI tool comparisons with pricing, evidence, workflow-fit guidance, and practical trial checklists.">
<title>AI Tool Comparisons — {len(pages)} Buyer Matchups | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/comparisons/">
<link rel="stylesheet" href="../css/styles.css"><link rel="stylesheet" href="../css/share.css">
<link rel="icon" href="../assets/aitools-bot-mark.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../assets/aitools-bot-logo-256.png">
<meta property="og:site_name" content="AIToolsEssentials"><meta property="og:type" content="website">
<meta property="og:title" content="AI Tool Comparisons — {len(pages)} Buyer Matchups">
<meta property="og:description" content="Independent AI tool comparisons grounded in current pricing, official sources, and real workflow decisions.">
<meta property="og:url" content="{DOMAIN}/comparisons/"><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<script type="application/ld+json">{json.dumps(item_list, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False)}</script>
<link rel="manifest" href="/site.webmanifest"><link rel="alternate" type="application/rss+xml" title="AIToolsEssentials updates" href="/feed.xml">
<script src="/js/discovery.js" defer></script>
</head><body>
<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a>
<nav class="nav-links"><a href="../tools/">Tools</a><a href="best-ai-tools.html">Best AI tools</a><a href="../categories/">Categories</a><a href="../articles/">Guides</a><a href="../benchmarks/">Benchmarks</a><a href="../guides/switch-guides/">Switching</a></nav>
<a class="nav-cta" href="../newsletter/">Free newsletter</a></header>
<main>
<section class="scene scene-dark hero compact-hero"><div class="hero-copy"><p class="kicker">Comparison library</p>
<h1>Choose the right AI tool before you pay.</h1>
<p class="subhead">Browse {len(pages)} buyer matchups organized by job. Each comparison connects current pricing, official evidence, workflow fit, and a repeatable trial checklist.</p>
<div class="actions"><a class="button button-blue" href="../compare-shortlist.html">Compare your shortlist</a><a class="button button-dark" href="../downloads/ai-tool-evaluation-scorecard.html">Open free scorecard</a><a class="button button-dark" href="../pricing-watch/" style="margin-left:8px">Pricing Watch</a></div>
</div></section>
<section class="scene scene-light"><div class="article-shell wide">
<p class="kicker light">Find a matchup</p><h2>Search the comparison library</h2>
<label for="comparison-filter">Filter by tool or matchup</label>
<input id="comparison-filter" type="search" placeholder="Try ChatGPT, Cursor, automation…" style="width:100%;max-width:720px;padding:14px 16px;border:1px solid #c7c7cc;border-radius:12px;font:inherit">
<p id="comparison-count" class="last-updated">Showing all {len(pages)} comparisons.</p>
</div></section>
{''.join(sections)}
<section class="score-card related-next-steps"><span>Decision workflow</span><h2>Turn reading into a documented choice.</h2>
<p>Save the finalists, estimate the full stack cost, then run the same real task in each tool before subscribing.</p>
<p><a class="button button-blue" href="../compare-shortlist.html">Compare shortlist</a><a class="button button-blue" href="../cost-calculator.html" style="margin-left:8px">Estimate cost</a><a class="button button-dark" href="../decision-brief.html" style="margin-left:8px">Create decision brief</a></p>
<p><a href="../press/">Press / cite us</a> · <a href="../methodology/">Methodology</a> · <a href="../evidence/">Evidence ledger</a> · <a href="../newsletter/">Keep/Cut Weekly</a></p></section>
<section class="newsletter-panel"><div><span>Keep/Cut Weekly</span><h2>One tool to keep. One to cut. One worth testing.</h2>
<p>Get a concise weekly decision brief with pricing changes and practical tool choices.</p></div><div class="newsletter-actions"><a class="button button-blue" href="../newsletter/">Read the newsletter</a><a class="button button-dark" href="../premium/">Explore Premium</a></div></section>
<p class="affiliate-inline">Editorial rankings and recommendations are independent. Affiliate participation and paid placement never change scores or ordering. <a href="../legal/affiliate-disclosure.html">Disclosure</a>.</p>
</main>
<div id="share-row" hidden></div>
<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="../advertise/" rel="nofollow">Advertise</a><a href="../submit-tool.html" rel="nofollow">Submit a tool</a><a href="../legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:contact@aitoolsessentials.com">Contact</a><a href="../legal/about.html">About</a><a href="../legal/privacy.html">Privacy</a><a href="../legal/terms.html">Terms</a></footer>
<script>
(function() {{
  const input = document.getElementById('comparison-filter');
  const cards = Array.from(document.querySelectorAll('[data-comparison-card]'));
  const count = document.getElementById('comparison-count');
  if (!input) return;
  input.addEventListener('input', function() {{
    const query = input.value.trim().toLowerCase();
    let visible = 0;
    cards.forEach(function(card) {{
      const show = !query || card.dataset.search.includes(query) || card.textContent.toLowerCase().includes(query);
      card.hidden = !show;
      if (show) visible += 1;
    }});
    count.textContent = query ? 'Showing ' + visible + ' matching comparisons.' : 'Showing all {len(pages)} comparisons.';
  }});
}})();
</script>
<script src="../js/site.js" defer></script><script src="../js/analytics.js" defer></script>
</body></html>'''

    output = root / "comparisons" / "index.html"
    output.write_text(document)
    print(f"Generated comparison hub: {len(pages)} pages")
    return output


if __name__ == "__main__":
    generate()
