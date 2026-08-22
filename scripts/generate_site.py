#!/usr/bin/env python3
"""Regenerate AIToolsEssentials directory, review, comparison, and category pages.

Source of truth: data/tools.json
Run from repo root:
    python3 scripts/generate_site.py
"""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
TOOLS = json.loads((ROOT / "data" / "tools.json").read_text())


def e(value):
    return html.escape(str(value), quote=True)


def site_header(prefix=""):
    return (
        f'<header class="global-nav"><a class="brand" href="{prefix}index.html">'
        '<span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a>'
        f'<nav class="nav-links"><a href="{prefix}tools/index.html">Tools</a>'
        f'<a href="{prefix}comparisons/best-ai-tools.html">Best AI tools</a>'
        f'<a href="{prefix}categories/index.html">Categories</a>'
        f'<a href="{prefix}articles/top-ai-tools-2026.html">Guide</a></nav>'
        f'<a class="nav-cta" href="{prefix}legal/affiliate-disclosure.html">Disclosure</a></header>'
    )


def footer(prefix=""):
    return (
        '<footer class="footer"><span>© 2026 AIToolsEssentials</span>'
        f'<a href="{prefix}legal/affiliate-disclosure.html">Affiliate disclosure</a>'
        f'<a href="{prefix}tools/index.html">Tools</a>'
        f'<a href="{prefix}comparisons/best-ai-tools.html">Best AI tools</a></footer>'
    )


def render_directory():
    cards = []
    for t in sorted(TOOLS, key=lambda item: (item["category"], item["name"])):
        cards.append(
            f'<article class="directory-card" data-category="{e(t["category"])}" '
            f'data-name="{e(t["name"].lower())}" data-use="{e(" ".join(t["use_cases"]).lower())}">'
            f'<div><span class="category-pill">{e(t["category"])}</span><h3>{e(t["name"])}</h3><p>{e(t["summary"])}</p></div>'
            f'<dl><dt>Best for</dt><dd>{e(t["best_for"])}</dd><dt>Price</dt><dd>{e(t["price"])}</dd><dt>Rating</dt><dd>{e(t["rating"])}/5</dd></dl>'
            f'<div class="card-actions"><a class="text-link" href="{e(t["slug"])}.html">Review ›</a>'
            f'<a class="button button-blue small" href="{e(t["official"])}" rel="sponsored nofollow" target="_blank">Visit site</a></div></article>'
        )
    (ROOT / "tools" / "index.html").write_text(
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="description" content="Browse curated AI tools by category, use case, price, and workflow fit.">'
        '<title>AI Tools Directory — AIToolsEssentials</title><link rel="stylesheet" href="../css/styles.css"></head>'
        f'<body>{site_header("../")}<main><section class="scene scene-dark hero compact-hero"><div class="hero-copy">'
        f'<p class="kicker">AI tools directory</p><h1>{len(TOOLS)} AI tools organized by real workflows.</h1>'
        '<p class="subhead">A continuously maintained shortlist for AI assistants, search, creative production, automation, development, productivity, meetings, audio, and video.</p>'
        '</div></section><section class="scene scene-light directory-section"><div class="directory-toolbar">'
        '<label for="toolSearch">Search tools</label><input id="toolSearch" type="search" placeholder="Try: Grok, research, video, coding, meetings…">'
        '<p class="monetization-note">This is a living directory, not a claim that the market is finite. Some outbound links may become affiliate links; recommendations are organized by workflow fit first.</p>'
        f'</div><div class="directory-grid" id="toolGrid">{"".join(cards)}</div></section></main>{footer("../")}<script src="../js/directory.js"></script></body></html>'
    )


def render_reviews():
    for old in (ROOT / "tools").glob("*.html"):
        if old.name != "index.html":
            old.unlink()
    for t in TOOLS:
        uses = "".join(f"<li>{e(u)}</li>" for u in t["use_cases"])
        pros = "".join(f"<li>{e(p)}</li>" for p in t["pros"])
        cons = "".join(f"<li>{e(c)}</li>" for c in t["cons"])
        (ROOT / "tools" / f"{t['slug']}.html").write_text(
            f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<meta name="description" content="{e(t["name"])} review: best use cases, pricing notes, pros, cons, and workflow fit.">'
            f'<title>{e(t["name"])} Review — AIToolsEssentials</title><link rel="stylesheet" href="../css/styles.css"></head><body>{site_header("../")}'
            f'<main><section class="scene scene-light review-hero"><p class="kicker light">{e(t["category"])}</p><h1>{e(t["name"])} review</h1><p>{e(t["summary"])}</p>'
            f'<div class="actions"><a class="button button-blue" href="{e(t["official"])}" rel="sponsored nofollow" target="_blank">Visit {e(t["name"])}</a><a class="button button-dark" href="index.html">Back to directory</a></div>'
            '<p class="affiliate-inline">Disclosure: outbound partner links may earn AIToolsEssentials a commission at no extra cost to you.</p></section>'
            f'<section class="scene scene-light review-layout"><article class="review-content"><h2>Best for</h2><p>{e(t["best_for"])}</p><h2>Use cases</h2><ul>{uses}</ul><h2>Pros</h2><ul>{pros}</ul><h2>Cons</h2><ul>{cons}</ul><h2>Verdict</h2><p>{e(t["name"])} is worth testing when your workflow matches the use cases above. Run three real examples, measure output quality after review, and compare the time saved against the monthly cost.</p></article>'
            f'<aside class="review-aside"><div class="score-card"><span>AIToolsEssentials score</span><strong>{e(t["rating"])}/5</strong><p>{e(t["price"])}</p><a class="button button-blue" href="{e(t["official"])}" rel="sponsored nofollow" target="_blank">Visit site</a></div></aside></section></main>{footer("../")}</body></html>'
        )


def render_comparison():
    rows = "".join(
        f'<tr><td><a href="../tools/{e(t["slug"])}.html">{e(t["name"])}</a></td><td>{e(t["category"])}</td><td>{e(t["best_for"])}</td><td>{e(t["rating"])}/5</td></tr>'
        for t in sorted(TOOLS, key=lambda item: -item["rating"])
    )
    (ROOT / "comparisons" / "best-ai-tools.html").write_text(
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="The best AI tools organized by category, workflow fit, and practical use case."><title>Best AI Tools — AIToolsEssentials</title><link rel="stylesheet" href="../css/styles.css"></head><body>{site_header("../")}<main><section class="scene scene-dark hero compact-hero"><div class="hero-copy"><p class="kicker">Best AI tools</p><h1>The practical AI shortlist for 2026.</h1><p class="subhead">A revenue-ready comparison page covering {len(TOOLS)} important AI products across assistants, search, creative, coding, automation, meetings, and productivity.</p></div></section><section class="scene scene-light comparison-section"><div class="article-shell wide"><h2>Best AI tools by category</h2><p>This is a living shortlist, not a claim that the AI market is finite. AIToolsEssentials will keep expanding and pruning tools based on adoption, buyer intent, practical usefulness, and monetization fit.</p><div class="table-wrap"><table><thead><tr><th>Tool</th><th>Category</th><th>Best for</th><th>Score</th></tr></thead><tbody>{rows}</tbody></table></div><h2>How this page can produce revenue</h2><ul><li><strong>Affiliate links:</strong> outbound “Visit site” buttons are already marked <code>rel="sponsored nofollow"</code>.</li><li><strong>High-intent SEO:</strong> comparison pages target searches like “best AI tools for research” and “best AI writing tools”.</li><li><strong>Lead capture:</strong> the homepage CTA can become a newsletter or buyer-guide signup.</li><li><strong>Sponsorships:</strong> category pages can sell clearly labeled featured placements without changing editorial reviews.</li></ul></div></section></main>{footer("../")}</body></html>'
    )


def render_categories():
    categories = {}
    for t in TOOLS:
        categories.setdefault(t["category"], []).append(t)
    tiles = []
    for category, items in sorted(categories.items()):
        links = " ".join(
            f'<a class="text-link" href="../tools/{e(t["slug"])}.html">{e(t["name"])} ›</a>'
            for t in sorted(items, key=lambda item: -item["rating"])[:4]
        )
        category_id = category.lower().replace(" ", "-").replace("&", "and")
        tiles.append(
            f'<article id="{e(category_id)}" class="product-tile tile-light category-list-tile"><div class="tile-text"><p class="eyebrow">{len(items)} tools</p><h3>{e(category)}</h3><p>Compare the strongest options in {e(category.lower())} and choose based on workflow fit, pricing, and review needs.</p><div class="mini-links">{links}</div></div></article>'
        )
    (ROOT / "categories" / "index.html").write_text(
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Browse AI tool categories for assistants, writing, creative work, automation, development, productivity, meetings, and research."><title>Categories — AIToolsEssentials</title><link rel="stylesheet" href="../css/styles.css"></head><body>{site_header("../")}<main><section class="scene scene-dark hero compact-hero"><div class="hero-copy"><p class="kicker">Category map</p><h1>Start with the work, then pick the tool.</h1><p class="subhead">AIToolsEssentials organizes {len(TOOLS)} AI tools around outcomes: assistants, research, writing, creative production, automation, coding, meetings, and productivity.</p></div></section><section class="scene scene-light product-grid-section"><div class="product-grid">{"".join(tiles)}</div></section></main>{footer("../")}</body></html>'
    )


def main():
    render_directory()
    render_reviews()
    render_comparison()
    render_categories()
    print(f"Regenerated {len(TOOLS)} tools and {len(list((ROOT / 'tools').glob('*.html'))) - 1} review pages")


if __name__ == "__main__":
    main()
