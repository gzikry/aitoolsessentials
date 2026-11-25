#!/usr/bin/env python3
"""The homepage body: four plain sections and one email ask.

Runs after every other pass that touches index.html, so the injections those
passes add to the homepage do not pile back up. The <head> and the shared
header and footer are left as the earlier passes wrote them.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

_MAIN_RE = re.compile(r"<main\b[^>]*>.*?</main>", re.S)
_DATE_RE = re.compile(r"^(\d{1,2}) ([A-Z][a-z]{2}) (\d{4})$")
_MONTHS = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}

# Pages people open most often. Each line says who the page is for, in plain words.
POPULAR = (
    ("/comparisons/chatgpt-vs-claude.html", "ChatGPT vs Claude", "Two general assistants. Which one to pay for if you only want one."),
    ("/articles/cursor-vs-github-copilot-deep-comparison.html", "Cursor vs GitHub Copilot", "An editor that writes code with you, or completions inside the editor you already use."),
    ("/comparisons/v0-vs-lovable.html", "v0 vs Lovable", "Two app builders for people who want a working prototype this week."),
    ("/comparisons/fathom-vs-fireflies.html", "Fathom vs Fireflies", "Meeting notes and recordings for sales and client calls."),
    ("/articles/make-vs-n8n.html", "Make vs n8n", "Automation with a visual builder, or one you can host yourself."),
    ("/comparisons/heygen-vs-synthesia.html", "HeyGen vs Synthesia", "AI presenter videos for training and marketing."),
)


def _sort_key(checked: str) -> tuple[int, int, int]:
    m = _DATE_RE.match(checked.strip())
    if not m:
        return (0, 0, 0)
    return (int(m.group(3)), _MONTHS.get(m.group(2), 0), int(m.group(1)))


def _latest_changes(limit: int = 4) -> list[tuple[str, str, str, str]]:
    from generate_price_changes import ROWS

    rows = sorted(ROWS, key=lambda r: _sort_key(r[2]), reverse=True)
    out = []
    for name, href, checked, price, _trap in rows[:limit]:
        first = price.split(". ")[0].rstrip(".") + "."
        out.append((name, href, checked, first))
    return out


def body(root: Path) -> str:
    from inject_price_alerts import signup_block

    cards = "".join(
        f'<li><a href="{href}"><strong>{html.escape(title)}</strong><span>{html.escape(line)}</span></a></li>'
        for href, title, line in POPULAR
    )
    changes = _latest_changes()
    newest = changes[0][2] if changes else ""
    change_items = "".join(
        f'<li><a href="{href}">{html.escape(name)}</a> <span class="home-date">checked {html.escape(checked)}</span>'
        f"<p>{html.escape(first)}</p></li>"
        for name, href, checked, first in changes
    )
    signup = signup_block(root, source="index.html")
    return (
        '<main class="home-simple">'
        '<section class="home-section home-intro">'
        "<h1>Plain reviews of the AI tools people pay for.</h1>"
        "<p>We read the pricing pages, compare the plans, and write down what we found and when we checked. "
        "Some links are partner links. They never change a review.</p>"
        '<form class="home-search" role="search" action="/search/" method="get">'
        '<label for="home-search-input">Search tools and comparisons</label>'
        '<span><input id="home-search-input" type="search" name="q" placeholder="ChatGPT, Cursor, Fireflies\u2026">'
        '<button class="button" type="submit">Search</button></span>'
        "</form>"
        '<p class="home-intro-links"><a href="/tools/">Browse all tools</a> \u00b7 '
        '<a href="/stack-audit.html">Check what you already pay for</a></p>'
        "</section>"
        '<section class="home-section" aria-labelledby="home-popular">'
        '<h2 id="home-popular">Popular comparisons</h2>'
        f'<ul class="home-cards">{cards}</ul>'
        '<p><a href="/comparisons/">See all comparisons</a></p>'
        "</section>"
        '<section class="home-section" id="price-alerts" aria-labelledby="home-changes">'
        '<h2 id="home-changes">Recent price changes</h2>'
        + (f'<p class="home-date">Newest note: {html.escape(newest)}. Each one links to the vendor page we checked.</p>' if newest else "")
        + f'<ul class="home-changes">{change_items}</ul>'
        '<p><a href="/price-changes/">All price changes</a></p>'
        '<div class="home-signup"><h3>Get an email when a price changes</h3>'
        f"{signup}</div>"
        "</section>"
        '<section class="home-section home-founders" aria-labelledby="home-founders">'
        '<h2 id="home-founders">Launching an AI tool?</h2>'
        "<p>Send it through the free queue, which takes about 14 days, or pay $79 for the Verified fast lane "
        "and get a written decision in one working day. Paying never changes a score.</p>"
        '<p><a class="button" href="/founders/">See launch options</a> '
        '<a href="/submit/">Use the free queue</a> \u00b7 <a href="/sponsor/" rel="nofollow">Sponsor the site</a></p>'
        "</section>"
        "</main>"
    )


def generate(root: Path) -> bool:
    page = root / "index.html"
    text = page.read_text(encoding="utf-8")
    updated = _MAIN_RE.sub(lambda _m: body(root), text, count=1)
    # The old sections' critical CSS and the bill-slasher script only served the old body.
    updated = re.sub(r"<!-- AIT HOME CRITICAL START -->.*?<!-- AIT HOME CRITICAL END -->", "", updated, flags=re.S)
    updated = re.sub(r'<script src="/js/homepage-bill-slasher\.js[^"]*" defer></script>', "", updated)
    if updated != text:
        page.write_text(updated, encoding="utf-8")
        return True
    return False


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parents[1]))
