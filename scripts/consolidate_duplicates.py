#!/usr/bin/env python3
"""Fold duplicate H1 pairs onto one page and leave a noindex redirect stub."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_scope import is_working_rel

DOMAIN = "https://aitoolsessentials.com"

# Loser path, winner path, visible title. The winner is the longer or more dated page.
PAIRS = (
    (
        "articles/ai-invoicing-admin-stack-consultants.html",
        "articles/ai-invoicing-admin-stack-solo-consultants.html",
        "AI invoicing and admin stack for solo consultants",
    ),
    (
        "alternatives/chatgpt-alternatives.html",
        "articles/chatgpt-alternatives.html",
        "Best ChatGPT alternatives",
    ),
    (
        "alternatives/claude-alternatives.html",
        "articles/claude-alternatives.html",
        "Best Claude alternatives",
    ),
    (
        "alternatives/grok-alternatives.html",
        "articles/grok-alternatives.html",
        "Best Grok alternatives",
    ),
    (
        "alternatives/jasper-alternatives.html",
        "articles/jasper-alternatives.html",
        "Best Jasper alternatives",
    ),
    (
        "alternatives/perplexity-alternatives.html",
        "articles/perplexity-alternatives.html",
        "Best Perplexity alternatives",
    ),
    (
        "articles/claude-code-vs-copilot-vs-cursor.html",
        "articles/claude-code-vs-cursor-vs-copilot.html",
        "Claude Code vs Cursor vs Copilot",
    ),
    (
        "articles/gemini-vs-claude.html",
        "comparisons/gemini-vs-claude.html",
        "Gemini vs Claude",
    ),
    (
        "articles/perplexity-vs-gemini.html",
        "comparisons/perplexity-vs-gemini.html",
        "Perplexity vs Gemini",
    ),
    (
        "articles/runway-vs-pika.html",
        "comparisons/runway-vs-pika.html",
        "Runway vs Pika",
    ),
    (
        "articles/suno-vs-udio.html",
        "comparisons/suno-vs-udio.html",
        "Suno vs Udio",
    ),
)

_BLOCK = re.compile(r"<(p|li)\b[^>]*>.*?</\1>", re.S | re.I)
_DATE = re.compile(
    r"20\d\d-\d\d-\d\d|"
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b[^<]{0,40}20\d\d"
)
_MAIN = re.compile(r"<main\b[^>]*>(.*)</main>", re.S | re.I)
_NOTE = re.compile(
    r"\n?<!-- consolidated-from:.*?-->"
    r'<section class="score-card consolidated-note">.*?</section>\n*',
    re.S,
)
_MOVED = "This page has moved."


def _plain(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = (
        text.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
        .replace("&apos;", "'")
    )
    return re.sub(r"\s+", " ", text).strip()


def _is_stub(html: str) -> bool:
    return 'http-equiv="refresh"' in html


def _strip_notes(html: str) -> str:
    return _NOTE.sub("", html)


def _worth_keeping(text: str) -> bool:
    if _MOVED in text:
        return False
    if "affiliate" in text.casefold():
        return True
    return _DATE.search(text) is not None


def _unique_blocks(loser_html: str, winner_html: str) -> list[str]:
    loser_main = _MAIN.search(loser_html)
    source = loser_main.group(1) if loser_main else loser_html
    winner_text = _plain(winner_html)
    kept: list[str] = []
    seen: set[str] = set()
    for match in _BLOCK.finditer(source):
        fragment = match.group(0)
        text = _plain(fragment)
        if len(text) < 40 or text in seen or not _worth_keeping(text):
            continue
        if text in winner_text:
            continue
        seen.add(text)
        kept.append(fragment)
        if len(kept) == 8:
            break
    return kept


def _fold(winner_html: str, loser: str, blocks: list[str]) -> str:
    marker = f"<!-- consolidated-from:{loser} -->"
    if not blocks or marker in winner_html:
        return winner_html
    section = (
        marker
        + '<section class="score-card consolidated-note"><h2>Also recorded</h2>'
        + "".join(blocks)
        + "</section>"
    )
    if "<!-- AIT RELATED NEXT STEPS START -->" in winner_html:
        return winner_html.replace("<!-- AIT RELATED NEXT STEPS START -->", section + "<!-- AIT RELATED NEXT STEPS START -->", 1)
    if "</main>" in winner_html:
        return winner_html.replace("</main>", section + "</main>", 1)
    return winner_html + section


def redirect_stub(title: str, winner: str) -> str:
    dest = "/" + winner
    safe_title = (
        title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    return (
        "<!doctype html><html lang=\"en\"><head>"
        '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<meta name="description" content="{safe_title} has moved.">'
        f"<title>{safe_title} (moved) | AIToolsEssentials</title>"
        f'<link rel="canonical" href="{DOMAIN}{dest}">'
        f'<meta http-equiv="refresh" content="0; url={dest}">'
        '<meta name="robots" content="noindex,follow">'
        '<link rel="stylesheet" href="/css/styles.css">'
        "</head><body><main><section class=\"scene scene-light\"><div class=\"article-shell\">"
        f"<h1>{safe_title}</h1>"
        "<p>This page has moved. The current page keeps the dated evidence and the affiliate disclosure.</p>"
        f'<p><a class="button button-blue" href="{dest}">Open the current page</a></p>'
        '</div></section></main>'
        '<script src="/js/analytics.js" defer></script>'
        "</body></html>\n"
    )


def _rewrite(html: str) -> str:
    for loser, winner, _title in PAIRS:
        html = html.replace(loser, winner)
    return html


def consolidate(root: Path) -> int:
    """Fold unique dated or affiliate lines into the winner, then stub the loser."""
    written = 0
    # Read every loser before any rewrite, so a shared pass cannot eat the source.
    sources = {
        loser: (root / loser).read_text(encoding="utf-8", errors="ignore")
        for loser, _winner, _title in PAIRS
        if (root / loser).is_file()
    }
    # Point internal links at the winner before the attribution marker is inserted.
    # A later replace would rewrite consolidated-from:LOSER into the winner path.
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if is_working_rel(rel):
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        updated = _rewrite(html)
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            written += 1
    for loser, winner, _title in PAIRS:
        winner_path = root / winner
        if not winner_path.is_file():
            continue
        current = _strip_notes(winner_path.read_text(encoding="utf-8", errors="ignore"))
        source = sources.get(loser, "")
        blocks = [] if not source or _is_stub(source) else _unique_blocks(source, current)
        folded = _fold(current, loser, blocks)
        if folded != winner_path.read_text(encoding="utf-8", errors="ignore"):
            winner_path.write_text(folded, encoding="utf-8")
            written += 1
    for loser, winner, title in PAIRS:
        loser_path = root / loser
        loser_path.parent.mkdir(parents=True, exist_ok=True)
        stub = redirect_stub(title, winner)
        if not loser_path.is_file() or loser_path.read_text(encoding="utf-8", errors="ignore") != stub:
            loser_path.write_text(stub, encoding="utf-8")
            written += 1
    return written


def duplicate_errors(root: Path) -> list[str]:
    errors: list[str] = []
    sitemap = (root / "sitemap.xml").read_text(encoding="utf-8") if (root / "sitemap.xml").is_file() else ""
    for loser, winner, title in PAIRS:
        loser_html = (root / loser).read_text(encoding="utf-8", errors="ignore") if (root / loser).is_file() else ""
        winner_html = (root / winner).read_text(encoding="utf-8", errors="ignore") if (root / winner).is_file() else ""
        if 'http-equiv="refresh"' not in loser_html or f"url=/{winner}" not in loser_html:
            errors.append(f"{loser} is not a redirect to {winner}")
        if 'name="robots" content="noindex' not in loser_html:
            errors.append(f"{loser} is still indexable")
        if f'href="{DOMAIN}/{winner}"' not in loser_html and f'href="https://aitoolsessentials.com/{winner}"' not in loser_html:
            errors.append(f"{loser} canonical does not point at {winner}")
        if title not in winner_html:
            errors.append(f"{winner} dropped the shared title")
        if f"https://aitoolsessentials.com/{loser}" in sitemap:
            errors.append(f"sitemap still lists {loser}")
        if f"https://aitoolsessentials.com/{winner}" not in sitemap:
            errors.append(f"sitemap dropped {winner}")
    return errors
