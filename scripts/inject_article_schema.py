#!/usr/bin/env python3
"""Inject Article JSON-LD schema into article pages that are missing it.

Some article generators emit FAQPage and BreadcrumbList but not Article.
This post-processor reads the page title and description and injects a
minimal Article schema so Google can identify these as articles.

Called from daily_content_update.py after all article generators run.
"""
import json
import re
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"
MARKER_START = "<!-- article-schema-inject -->"
MARKER_END = "<!-- /article-schema-inject -->"


def inject_article_schema(root: Path) -> int:
    articles_dir = root / "articles"
    if not articles_dir.exists():
        return 0

    injected = 0
    for f in sorted(articles_dir.glob("*.html")):
        if f.name in ("index.html", "learn.html"):
            continue

        html = f.read_text()

        # Check if Article schema already exists
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        has_article = False
        for b in blocks:
            try:
                d = json.loads(b)
                if isinstance(d, dict) and d.get("@type") in ("Article", "NewsArticle", "TechArticle"):
                    has_article = True
                    break
            except Exception:
                pass

        if has_article:
            continue

        # Extract title and description
        title_match = re.search(r"<title>(.*?)</title>", html)
        title = title_match.group(1).replace(" — AIToolsEssentials", "").replace(" | AIToolsEssentials", "") if title_match else f.stem.replace("-", " ").title()
        desc_match = re.search(r'<meta name="description" content="([^"]*)"', html)
        desc = desc_match.group(1) if desc_match else title

        article_schema = json.dumps({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": desc,
            "url": f"{DOMAIN}/articles/{f.name}",
            "author": {"@type": "Organization", "name": "AIToolsEssentials"},
            "publisher": {"@type": "Organization", "name": "AIToolsEssentials", "url": DOMAIN},
        })

        schema_block = f'{MARKER_START}\n<script type="application/ld+json">{article_schema}</script>\n{MARKER_END}'

        # Remove any existing injected block (idempotent)
        stripped = re.sub(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END) + r"\n?",
            "",
            html,
            flags=re.S,
        )

        # Insert before </head>
        updated = stripped.replace("</head>", schema_block + "\n</head>", 1)

        if updated != html:
            f.write_text(updated)
            injected += 1

    if injected:
        print(f"Article schema injected into {injected} article pages")
    return injected


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    inject_article_schema(root)