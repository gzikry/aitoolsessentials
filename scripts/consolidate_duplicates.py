#!/usr/bin/env python3
"""Fold duplicate H1 pairs onto one page and leave a noindex redirect stub."""
from __future__ import annotations

import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_scope import is_public_rel, is_working_rel

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


def is_redirect_stub(html: str) -> bool:
    return _is_stub(html)


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
        f'<p><a class="button button-blue stub-fallback" href="{dest}">Open the current page</a></p>'
        '</div></section></main>'
        '<script src="/js/analytics.js" defer></script>'
        "</body></html>\n"
    )


def _rewrite(html: str) -> str:
    for loser, winner, _title in PAIRS:
        html = html.replace(loser, winner)
    return html


def _href_from(page: Path, target: str) -> str:
    start = page.parent.as_posix()
    return os.path.relpath(target, start if start != "." else ".").replace("\\", "/")


def _rewrite_page(html: str, page: Path) -> str:
    """Point full paths and same-directory hrefs at the winner."""
    html = _rewrite(html)
    for loser, winner, _title in PAIRS:
        loser_path = Path(loser)
        if loser_path.parent != page.parent:
            continue
        href = _href_from(page, winner)
        html = re.sub(
            rf'(href=["\'])(?:\./)?{re.escape(loser_path.name)}(?=["\'?#])',
            rf"\1{href}",
            html,
        )
    return html


def _resolve_href(page: Path, href: str) -> str | None:
    href = href.split("#", 1)[0].split("?", 1)[0].strip()
    if not href or href.startswith(("mailto:", "javascript:", "tel:")):
        return None
    if href.startswith(("http://", "https://")):
        prefix = DOMAIN + "/"
        if not href.startswith(prefix):
            return None
        href = href[len(prefix) :]
    elif href.startswith("/"):
        href = href[1:]
    else:
        base = page.parent.as_posix()
        href = href if base == "." else base + "/" + href
    parts: list[str] = []
    for part in href.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


# One run of trailing punctuation, then the end or a separator. Nested repeats
# on that punctuation are exponential, so this stays linear. A period ends the
# segment even when another sentence follows. A hyphen does not: "moved-on",
# "moved-in", and "moved - here's" keep going. A spaced hyphen before a capital
# brand ("moved - AIToolsEssentials") is still a separator.
_MOVED_ENDS = re.compile(
    r"(?i:\bhas moved)[\s,!?…:;)\]]*(?:$|[|–—:·.]|-(?=\s+[A-Z]))",
)
_THIS_MOVED = re.compile(r"\bthis (?:page|guide|article) has moved\b", re.I)
_SHORT_COPY_LIMIT = 180
_HEADING_TAGS = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
_BLOCK_TAGS = _HEADING_TAGS | frozenset({
    "p", "div", "li", "section", "article", "main", "blockquote",
    "td", "th", "figcaption", "dd", "dt", "aside", "header", "footer", "address",
})
_VOID_TAGS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "source", "track", "wbr",
})
_LINK = re.compile(r"""href=["']([^"']+)["']""", re.I)
_MD_LINK = re.compile(r"\((https://aitoolsessentials\.com/[^)\s]+)\)")
_JSONLD = re.compile(
    r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
_JSON_URL = re.compile(r'"url"\s*:\s*"([^"]+)"')


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
        updated = _rewrite_page(html, rel)
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            written += 1
    for name in ("llms.txt",):
        path = root / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        updated = _rewrite(text)
        if updated != text:
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


def _norm_copy(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _moved_ends_segment(text: str) -> bool:
    """True when 'has moved' ends at punctuation, the end of the text, or a separator."""
    plain = _norm_copy(text)
    return bool(plain) and _MOVED_ENDS.search(plain) is not None


def _short_stub_body(text: str) -> bool:
    """True for a short block that says this page, guide, or article has moved."""
    plain = _norm_copy(text)
    if not plain or len(plain) > _SHORT_COPY_LIMIT:
        return False
    return _THIS_MOVED.search(plain) is not None


class _StubCopyParser(HTMLParser):
    """Collect title, heading, and short-block text, including nested spans."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[list] = []
        self.titles: list[str] = []
        self.headings: list[str] = []
        self.blocks: list[str] = []
        self.descriptions: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        tag = tag.lower()
        if tag == "meta":
            attr = {key.lower(): value or "" for key, value in attrs}
            if attr.get("name", "").lower() == "description" and attr.get("content"):
                self.descriptions.append(attr["content"])
            return
        if tag in _VOID_TAGS:
            return
        if tag in {"title"} | _BLOCK_TAGS or self.stack:
            self.stack.append([tag, []])

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in _VOID_TAGS or not self.stack:
            return
        while self.stack:
            open_tag, parts = self.stack.pop()
            text = "".join(parts)
            if open_tag == "title":
                self.titles.append(text)
            elif open_tag in _HEADING_TAGS:
                self.headings.append(text)
            elif open_tag in _BLOCK_TAGS:
                self.blocks.append(text)
            if self.stack:
                self.stack[-1][1].append(text)
            if open_tag == tag:
                break

    def handle_data(self, data: str) -> None:
        if self.stack:
            self.stack[-1][1].append(data)


def _page_has_stub_moved_copy(html: str) -> bool:
    parser = _StubCopyParser()
    parser.feed(html)
    parser.close()
    for text in parser.titles + parser.headings + parser.descriptions:
        if _moved_ends_segment(text):
            return True
    return any(_short_stub_body(text) for text in parser.blocks)


def stub_link_errors(root: Path) -> list[str]:
    """Indexable pages must not link to a redirect stub or repeat its moved title."""
    stubs: set[str] = set()
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if is_working_rel(rel) or not path.is_file():
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if _is_stub(html):
            stubs.add(rel.as_posix())
    errors: list[str] = []
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if is_working_rel(rel) or not is_public_rel(rel):
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if _is_stub(html):
            continue
        folded = html.casefold()
        if "(moved)" in folded:
            errors.append(f"{rel.as_posix()} still says (moved)")
        if _page_has_stub_moved_copy(html):
            errors.append(f"{rel.as_posix()} still says has moved")
        for href in _LINK.findall(html):
            target = _resolve_href(rel, href)
            if target in stubs:
                errors.append(f"{rel.as_posix()} links to stub {target}")
        for raw in _JSON_URL.findall("\n".join(_JSONLD.findall(html))):
            target = _resolve_href(rel, raw)
            if target in stubs:
                errors.append(f"{rel.as_posix()} JSON-LD url points at stub {target}")
    llms = root / "llms.txt"
    if llms.is_file():
        text = llms.read_text(encoding="utf-8", errors="ignore")
        folded = text.casefold()
        if "(moved)" in folded:
            errors.append("llms.txt still says (moved)")
        if any(_moved_ends_segment(line) or _short_stub_body(line) for line in text.splitlines()):
            errors.append("llms.txt still says has moved")
        for href in _MD_LINK.findall(text):
            target = _resolve_href(Path("llms.txt"), href)
            if target in stubs:
                errors.append(f"llms.txt links to stub {target}")
    return errors
