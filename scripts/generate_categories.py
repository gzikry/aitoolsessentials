#!/usr/bin/env python3
"""Polished category buyer-guide page generator. Matches the review-page design system."""
import json
import re
from html import escape as htmlesc
from pathlib import Path
from urllib.parse import quote

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
    compact_card = ' style="min-height:260px"' if len(cat_tools) < 3 else ''
    for i, t in enumerate(sorted(cat_tools, key=lambda x: -x.get('rating', 0))[:12], start=1):
        stars = '★' * int(round(t.get('rating', 0)))
        score_label = f"{t['rating']}/5" if t.get('rating') else 'Editorial score in review'
        best = ', '.join(t.get('best_for', t.get('summary', ''))) if isinstance(t.get('best_for', t.get('summary', '')), list) else t.get('best_for', t.get('summary', ''))
        best = best[:110].rstrip()
        cards_html += f'''
        <article class="directory-card"{compact_card}>
          <div>
            <span class="category-pill">#{i} · {score_label}</span>
            <h3><a href="../../tools/{t['slug']}/">{t['name']}</a></h3>
            <p>{best}</p>
            <span style="color:#f5a623;letter-spacing:2px">{stars}</span>
          </div>
          <div class="card-actions">
            <a class="text-link" href="../../tools/{t['slug']}/">Read review</a>
            <a class="button button-blue small" href="{t.get('official','')}" rel="sponsored noopener nofollow" target="_blank">Visit site</a>
          </div>
        </article>'''

    from urllib.parse import quote
    other_cats = sorted({t2['category'] for t2 in tools if t2['category'] != cat})
    pills = ''.join(f'<a class="guide-pill" href="../{quote(c, safe="")}/">{c}</a>' for c in other_cats[:8])
    related_categories = f'<div class="category-related"><p class="kicker light">Explore related categories</p><div class="guide-pills">{pills}</div></div>'

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="The {n} best {cat} AI tools, ranked and reviewed: pricing notes, strengths, trade-offs, and who each tool is actually for.">
<title>Best {cat} AI tools ({today[:4]}) | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/categories/{cat}/">
<link rel="stylesheet" href="../../css/styles.css">
<link rel="stylesheet" href="../../css/share.css">
<script type="application/ld+json">{schema}</script>
</head>
<body>
<header class="global-nav">
<a class="brand" href="../../index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a>
<nav class="nav-links">
<a href="../../tools/index.html">Tools</a>
<a href="../../comparisons/best-ai-tools.html">Best AI tools</a>
<a href="../../categories/index.html">Categories</a>
<a href="../../articles/index.html">Guides</a>
</nav>
<a class="nav-cta" href="../../legal/affiliate-disclosure.html">Disclosure</a>
</header>

<main>

<section class="review-hero scene scene-light">
<p class="kicker light">{cat}</p>
<h1>Best {cat} AI tools</h1>
<p>{n} tools ranked by our evaluation rubric: job fit, output quality, and operational cost. Every entry links to a full hands-on review.</p>
<p class="last-updated">Independently ranked · Updated {today}</p>
</section>

<section class="directory-section scene scene-light">
<div class="directory-grid"{' style="max-width:760px"' if n < 3 else ''}>
{cards_html}
</div>
</section>

<section class="scene scene-light category-related-section">
<div class="article-shell wide">{related_categories}</div>
</section>

<section class="scene scene-light guide-strip">
<div>
<p class="kicker light">Choosing between tools?</p>
<h2>Compare before you commit.</h2>
<p>Run any two or three candidates through the free evaluation scorecard — real tasks, scored side by side, in under an hour.</p>
<div class="actions" style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:10px">
<a class="button button-blue" href="../../downloads/ai-tool-evaluation-scorecard.html">Get the free scorecard</a>
<a class="button button-dark" href="../../comparisons/index.html">Browse comparisons</a>
<a class="button button-blue" href="../../newsletter/" style="margin-left:8px">Read the newsletter</a>
<a class="button button-dark" href="../../pricing-watch/" style="margin-left:8px">Pricing Watch</a>
<a class="button button-dark" href="../../methodology/" style="margin-left:8px">Methodology</a>
<a class="button button-dark" href="../../press/" style="margin-left:8px">Press / cite us</a>
<a class="button button-dark" href="../../evidence/" style="margin-left:8px">Evidence ledger</a>
<a class="button button-dark" href="../../premium/" style="margin-left:8px">Premium research membership</a>
</div>
</div>
</section>

</main>

<footer class="footer">
<span>© {today[:4]} AIToolsEssentials</span>
<a href="../../advertise/index.html" rel="nofollow">Advertise</a>
<a href="../../submit-tool.html" rel="nofollow">Submit a tool</a>
<a href="../../legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
<a href="mailto:{EMAIL}">Contact</a>
</footer>
<script src="../../js/site.js" defer></script>
<script src="../../js/analytics.js" defer></script>
</body>
</html>'''


    out = cat_dir / 'index.html'
    out.write_text(html)
    return out


def _cat_id(cat: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', cat.lower().replace('&', 'and')).strip('-')


def generate_category_hub(root: Path, tools: list, today: str) -> Path:
    """Rebuild categories/index.html so the leftover truncated hub cannot stay in the sitemap."""
    by_cat: dict[str, list] = {}
    for t in tools:
        by_cat.setdefault(t.get('category', 'Uncategorized'), []).append(t)
    cats = sorted(by_cat, key=lambda c: (-len(by_cat[c]), c))
    tiles = []
    cards = []
    item_list = []
    for i, cat in enumerate(cats, start=1):
        cat_tools = sorted(by_cat[cat], key=lambda x: -x.get('rating', 0))
        n = len(cat_tools)
        href = quote(cat, safe='') + '/'
        mini = ''.join(
            f'<a class="text-link" href="../tools/{t["slug"]}/">{htmlesc(t["name"])} ›</a>'
            for t in cat_tools[:3]
        )
        tiles.append(
            f'<article id="{_cat_id(cat)}" class="product-tile tile-light category-list-tile"><div class="tile-text">'
            f'<p class="eyebrow">{n} tool{"s" if n != 1 else ""}</p>'
            f'<h3>{htmlesc(cat)}</h3>'
            f'<p>Compare the strongest options in {htmlesc(cat.lower())} and choose based on workflow fit, pricing, and review needs.</p>'
            f'<div class="mini-links">{mini}</div></div></article>'
        )
        label = 'Browse 1 tool' if n == 1 else f'Browse {n} tools'
        cards.append(
            f'<article class="content-hub-card"><h3><a href="{href}">{htmlesc(cat)}</a></h3>'
            f'<a class="text-link" href="{href}">{label}</a></article>'
        )
        item_list.append({
            '@type': 'ListItem',
            'position': i,
            'name': cat,
            'url': f'{DOMAIN}/categories/{quote(cat, safe="")}/',
        })
    schema = json.dumps({'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'AI tool categories', 'itemListElement': item_list}, ensure_ascii=False)
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Browse AI tool categories for assistants, writing, creative work, automation, development, productivity, meetings, and research.">
<title>Categories — AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/categories/">
<link rel="stylesheet" href="../css/styles.css">
<link rel="stylesheet" href="../css/share.css">
<link rel="icon" href="../assets/aitools-bot-mark.svg" type="image/svg+xml">
<meta property="og:title" content="Categories — AIToolsEssentials">
<meta property="og:description" content="Browse AI tool categories for assistants, writing, creative work, automation, development, productivity, meetings, and research.">
<meta property="og:url" content="{DOMAIN}/categories/">
<meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{schema}</script>
</head>
<body>
<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a>
<nav class="nav-links"><a href="../tools/">Tools</a><a href="../comparisons/best-ai-tools.html">Best AI tools</a><a href="./">Categories</a><a href="../articles/">Guides</a><a href="../benchmarks/">Benchmarks</a><a href="../guides/switch-guides/">Switching</a></nav>
<a class="nav-cta" href="../newsletter/">Free newsletter</a></header>
<main>
<section class="scene scene-dark hero compact-hero"><div class="hero-copy"><p class="kicker">Category map</p>
<h1>Start with the work, then pick the tool.</h1>
<p class="subhead">AIToolsEssentials organizes {len(tools)} AI tools around outcomes: assistants, research, writing, creative production, automation, coding, meetings, and productivity.</p>
<div class="actions"><a class="button button-blue" href="../pricing-watch/">Pricing Watch</a>
<a class="button button-dark" href="../press/">Press / cite us</a>
<a class="button button-dark" href="../methodology/">Methodology</a></div>
</div></section>
<section class="scene scene-light product-grid-section"><div class="product-grid">{''.join(tiles)}</div></section>
<section class="scene scene-light content-hub"><h2>Browse by category</h2><div class="content-hub-grid">{''.join(cards)}</div></section>
<!-- AIT SOURCE CITE START --><section class="score-card related-next-steps"><span>Cite and verify</span>
<h2>Source pages Google can quote.</h2>
<p><a href="/pricing-watch/">Pricing Watch</a> · <a href="/newsletter/">Keep/Cut Weekly</a> · <a href="/press/">Press / cite us</a> · <a href="/evidence/">Evidence ledger</a> · <a href="/methodology/">Methodology</a></p>
</section><!-- AIT SOURCE CITE END -->
</main>
<div id="share-row" hidden></div>
<footer class="footer"><span>© {today[:4]} AIToolsEssentials</span><a href="../advertise/" rel="nofollow">Advertise</a><a href="../submit-tool.html" rel="nofollow">Submit a tool</a><a href="../legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="../legal/about.html">About</a><a href="../legal/privacy.html">Privacy</a><a href="../legal/terms.html">Terms</a></footer>
<script src="../js/site.js" defer></script>
<script src="../js/analytics.js" defer></script>
</body>
</html>
'''
    out = root / 'categories' / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return out


def generate_all(root: Path, tools: list, today: str) -> int:
    cats = sorted({t['category'] for t in tools})
    for cat in cats:
        cat_tools = [t for t in tools if cat in t.get('category', '')]
        generate_category_page(root, cat, cat_tools, tools, today)
        print(f'Generated category buyer: {cat}')
    generate_category_hub(root, tools, today)
    print('Generated category hub')
    return len(cats)


if __name__ == '__main__':
    from datetime import datetime
    root = Path(__file__).resolve().parents[1]
    tools = json.loads((root / 'data/tools.json').read_text())
    generate_all(root, tools, datetime.today().strftime('%Y-%m-%d'))
