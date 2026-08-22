#!/usr/bin/env python3
"""Polished category buyer-guide page generator. Matches the review-page design system."""
import json
import re
from pathlib import Path

DOMAIN = 'https://aitoolsessentials.com'
EMAIL = 'contact@aitoolsessentials.com'


def generate_category_page(root: Path, cat: str, cat_tools: list, tools: list, today: str) -> Path:
    cat_dir = root / 'categories' / cat
    cat_dir.mkdir(parents=True, exist_ok=True)
    n = len(cat_tools)

    import json as _json
    schema = _json.dumps({
        "@context": "https://schema.org", "@type": "ItemList",
        "name": f"Best {cat} AI Tools",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1,
             "url": f"{DOMAIN}/tools/{t['slug']}/"}
            for i, t in enumerate(sorted(cat_tools, key=lambda x: -x.get('rating', 0))[:12])
        ]
    })

    # Cards for each tool in this category (ranked by rating)
    cards_html = ''
    for i, t in enumerate(sorted(cat_tools, key=lambda x: -x.get('rating', 0))[:12], start=1):
        stars = '★' * int(round(t.get('rating', 0)))
        best = t.get('best_for', t.get('summary', ''))[:110].rstrip()
        cards_html += f'''
        <article class="directory-card">
          <div>
            <span class="category-pill">#{i} · {t.get('rating','')}/5</span>
            <h3><a href="../tools/{t['slug']}/">{t['name']}</a></h3>
            <p>{best}</p>
            <span style="color:#f5a623;letter-spacing:2px">{stars}</span>
          </div>
          <div class="card-actions">
            <a class="text-link" href="../tools/{t['slug']}/">Read review</a>
            <a class="button button-blue small" href="{t.get('official','')}" rel="sponsored noopener nofollow" target="_blank">Visit site</a>
          </div>
        </article>'''

    # Related categories (share at least one tool slug overlap or sibling naming)
    other_cats = sorted({t2['category'] for t2 in tools if t2['category'] != cat})
    pills = ''.join(f'<a class="guide-pill" href="../articles/best-ai-tools.html">{c}</a>' for c in other_cats[:8])

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="The {n} best {cat} AI tools, ranked and reviewed: pricing notes, strengths, trade-offs, and who each tool is actually for.">
<title>Best {cat} AI Tools ({today[:4]}) — Ranked &amp; Reviewed | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/categories/{cat}/">
<link rel="stylesheet" href="../css/styles.css">
<link rel="stylesheet" href="../css/share.css">
<script type="application/ld+json">{schema}</script>
</head>
<body>
<header class="global-nav">
<a class="brand" href="../index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a>
<nav class="nav-links">
<a href="../tools/index.html">Tools</a>
<a href="../comparisons/best-ai-tools.html">Best AI tools</a>
<a href="../categories/index.html">Categories</a>
<a href="../articles/index.html">Guides</a>
</nav>
<a class="nav-cta" href="../legal/affiliate-disclosure.html">Disclosure</a>
</header>

<section class="review-hero scene scene-light">
<p class="kicker light">{cat}</p>
<h1>Best {cat} AI tools</h1>
<p>{n} tools ranked by our evaluation rubric: job fit, output quality, and operational cost. Every entry links to a full hands-on review.</p>
<p class="last-updated">Independently ranked · Updated {today}</p>
</section>

<section class="directory-section scene scene-light">
<div class="directory-grid">
{cards_html}
</div>
</section>

<section class="scene scene-light guide-strip">
<div>
<p class="kicker light">Choosing between tools?</p>
<h2>Compare before you commit.</h2>
<p>Run any two or three candidates through the free evaluation scorecard — real tasks, scored side by side, in under an hour.</p>
<div class="actions" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:10px">
<a class="button button-blue" href="../downloads/ai-tool-evaluation-scorecard.html">Get the free scorecard</a>
<a class="button button-dark" href="../comparisons/index.html">Browse comparisons</a>
</div>
</div>
</section>

<footer class="footer">
<span>© {today[:4]} AIToolsEssentials</span>
<a href="../advertise/index.html" rel="nofollow">Advertise</a>
<a href="../submit-tool.html" rel="nofollow">Submit a tool</a>
<a href="../legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
<a href="mailto:{EMAIL}">Contact</a>
</footer>
<script src="../js/site.js" defer></script>
<script src="../js/analytics.js" defer></script>
</body>
</html>'''


    out = cat_dir / 'index.html'
    out.write_text(html)
    return out


def generate_all(root: Path, tools: list, today: str) -> int:
    cats = sorted({t['category'] for t in tools})
    for cat in cats:
        cat_tools = [t for t in tools if cat in t.get('category', '')]
        generate_category_page(root, cat, cat_tools, tools, today)
        print(f'Generated category buyer: {cat}')
    return len(cats)


if __name__ == '__main__':
    from datetime import datetime
    root = Path('/Users/georgezikry/aitoolessentials/site')
    tools = json.loads((root / 'data/tools.json').read_text())
    generate_all(root, tools, datetime.today().strftime('%Y-%m-%d'))
