#!/usr/bin/env python3
"""Enhance Article JSON-LD schema on all article pages.

Some article generators emit Article schema without image or datePublished.
Google requires image for Article rich results, and datePublished/dateModified
help search engines understand freshness. This post-processor ensures all
Article schemas have these required/recommended fields.

Called from daily_content_update.py after all article generators run.
"""
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"
OG_IMAGE = f"{DOMAIN}/assets/og-ai-tools.jpg"
MARKER_START = "<!-- article-schema-enhance -->"
MARKER_END = "<!-- /article-schema-enhance -->"
ARTICLE_TYPES = ("Article", "NewsArticle", "TechArticle")


def first_add_dates(root: Path) -> dict:
    """Map article filename -> the date git first added it.

    Used only as a fallback publication date when a page carries no date at all.
    Without it the stamp falls back to "today", which silently rewrites the
    publication date every morning on every page it touches.
    """
    try:
        result = subprocess.run(
            ["git", "log", "--diff-filter=A", "--name-only", "--format=AITDATE:%as", "--", "articles/*.html"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except Exception:
        return {}

    dates = {}
    current = None
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("AITDATE:"):
            current = line.split(":", 1)[1].strip()
        elif line.startswith("articles/") and current:
            name = Path(line).name
            previous = dates.get(name)
            if previous is None or current < previous:
                dates[name] = current
    return dates


def existing_article_dates(html: str):
    """Return (earliest datePublished, latest dateModified) already on the page."""
    published, modified = [], []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            data = json.loads(block)
        except Exception:
            continue
        if isinstance(data, dict) and data.get("@type") in ARTICLE_TYPES:
            if data.get("datePublished"):
                published.append(str(data["datePublished"]))
            if data.get("dateModified"):
                modified.append(str(data["dateModified"]))
    published = [d for d in published if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d)]
    modified = [d for d in modified if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d)]
    return (min(published) if published else None, max(modified) if modified else None)


def enhance_article_schema(root: Path) -> int:
    articles_dir = root / "articles"
    if not articles_dir.exists():
        return 0

    today = datetime.today().strftime("%Y-%m-%d")
    added = first_add_dates(root)
    enhanced = 0

    for f in sorted(articles_dir.glob("*.html")):
        if f.name in ("index.html", "learn.html"):
            continue

        html = f.read_text()

        # Find all JSON-LD blocks and check if any Article schema needs enhancement
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        
        # Extract title and description for fallback
        title_match = re.search(r"<title>(.*?)</title>", html)
        title = title_match.group(1).replace(" — AIToolsEssentials", "").replace(" | AIToolsEssentials", "") if title_match else f.stem.replace("-", " ").title()
        desc_match = re.search(r'<meta name="description" content="([^"]*)"', html)
        desc = desc_match.group(1) if desc_match else title

        needs_enhancement = False
        has_article = False
        for b in blocks:
            try:
                d = json.loads(b)
                if isinstance(d, dict) and d.get("@type") in ("Article", "NewsArticle", "TechArticle"):
                    has_article = True
                    missing = []
                    if not d.get("image"):
                        missing.append("image")
                    if not d.get("datePublished"):
                        missing.append("datePublished")
                    if not d.get("dateModified"):
                        missing.append("dateModified")
                    if missing:
                        needs_enhancement = True
            except Exception:
                pass

        # Also check if no Article schema exists at all
        if not has_article:
            needs_enhancement = True

        if not needs_enhancement:
            continue

        # Keep the dates the page already carries. Rebuilding with "today" on every
        # run rewrote datePublished daily across every article page, which reads as
        # manufactured freshness and contradicts the visible editorial dates.
        prior_published, prior_modified = existing_article_dates(html)
        date_published = prior_published or added.get(f.name) or today
        date_modified = prior_modified or date_published
        if date_modified < date_published:
            date_modified = date_published

        # Build the enhanced schema
        article_schema = json.dumps({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": desc,
            "image": OG_IMAGE,
            "datePublished": date_published,
            "dateModified": date_modified,
            "url": f"{DOMAIN}/articles/{f.name}",
            "author": {"@type": "Organization", "name": "AIToolsEssentials"},
            "publisher": {"@type": "Organization", "name": "AIToolsEssentials", "url": DOMAIN},
        })

        schema_block = f'{MARKER_START}\n<script type="application/ld+json">{article_schema}</script>\n{MARKER_END}'

        # Remove any existing enhanced block (idempotent)
        stripped = re.sub(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END) + r"\n?",
            "",
            html,
            flags=re.S,
        )

        # Remove any existing injected block from previous version
        stripped = re.sub(
            r"<!-- article-schema-inject -->.*?<!-- /article-schema-inject -->\n?",
            "",
            stripped,
            flags=re.S,
        )

        # Insert before </head>
        updated = stripped.replace("</head>", schema_block + "\n</head>", 1)

        if updated != html:
            f.write_text(updated)
            enhanced += 1

    if enhanced:
        print(f"Article schema enhanced on {enhanced} article pages")
    return enhanced


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    enhance_article_schema(root)