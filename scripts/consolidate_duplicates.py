#!/usr/bin/env python3
"""Fold duplicate H1 pairs onto one page and leave a noindex redirect stub."""
from __future__ import annotations

import os
import re
import sys
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


def _is_real_stub(html: str) -> bool:
    """A redirect stub is noindex and a meta refresh. Indexable pages are not exempt."""
    return _is_stub(html) and "noindex" in html.casefold()


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


# Same check as main (5f737e6 / cf0689c): a case-insensitive substring anywhere
# in the file. With no data-moved-ok marker the scan is that substring, so it
# cannot miss a phrase main would catch, including JSON-LD name/headline,
# og/twitter, alt, and aria-label. A data-moved-ok element drops its own
# subtree before the substring. The allowlist drops a whole page.
_MOVED_PHRASE = "has moved"
_MOVED_MARK = "(moved)"
_OPT_OUT = "data-moved-ok"
_ALLOWLIST_NAME = Path("scripts/moved_phrase_allowlist.txt")
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


def _split_tag(folded: str, i: int) -> tuple[int, str, bool, bool, bool]:
    """Read one tag at '<'. One forward pass. Returns end, name, is_end, opt_out, self_closing."""
    n = len(folded)
    j = i + 1
    is_end = False
    if j < n and folded[j] == "/":
        is_end = True
        j += 1
    while j < n and folded[j].isspace():
        j += 1
    start = j
    while j < n and (folded[j].isalnum() or folded[j] in ":-"):
        j += 1
    name = folded[start:j]
    opt_out = False
    quote = ""
    self_closing = False
    while j < n:
        char = folded[j]
        if quote:
            if char == quote:
                quote = ""
            j += 1
            continue
        if char in "\"'":
            quote = char
            j += 1
            continue
        if char == ">":
            j += 1
            break
        if char == "/":
            if j + 1 < n and folded[j + 1] == ">":
                self_closing = True
                j += 2
                break
            j += 1
            continue
        if char.isspace():
            j += 1
            continue
        attr_start = j
        while j < n and not folded[j].isspace() and folded[j] not in "=>/\"'":
            j += 1
        if folded[attr_start:j] == _OPT_OUT:
            opt_out = True
        while j < n and folded[j].isspace():
            j += 1
        if j < n and folded[j] == "=":
            j += 1
            while j < n and folded[j].isspace():
                j += 1
            if j < n and folded[j] in "\"'":
                quote = folded[j]
                j += 1
            else:
                while j < n and not folded[j].isspace() and folded[j] != ">":
                    j += 1
    return j, name, is_end, opt_out, self_closing


def _without_moved_opt_outs(folded: str) -> str:
    """Drop each data-moved-ok element, including descendants. Linear in the HTML."""
    parts: list[str] = []
    n = len(folded)
    i = 0
    skip_name = ""
    depth = 0
    while i < n:
        if folded[i] != "<":
            nxt = folded.find("<", i)
            if nxt < 0:
                nxt = n
            if depth == 0:
                parts.append(folded[i:nxt])
            i = nxt
            continue
        if folded.startswith("<!--", i):
            end = folded.find("-->", i + 4)
            end = n if end < 0 else end + 3
            if depth == 0:
                parts.append(folded[i:end])
            i = end
            continue
        if i + 1 < n and folded[i + 1] in "!?":
            end = folded.find(">", i + 2)
            end = n if end < 0 else end + 1
            if depth == 0:
                parts.append(folded[i:end])
            i = end
            continue
        end, name, is_end, opt_out, self_closing = _split_tag(folded, i)
        if end <= i:
            if depth == 0:
                parts.append(folded[i])
            i += 1
            continue
        if depth:
            if name == skip_name and not is_end and not self_closing and name not in _VOID_TAGS:
                depth += 1
            elif is_end and name == skip_name:
                depth -= 1
            i = end
            continue
        if opt_out and not is_end:
            if self_closing or not name or name in _VOID_TAGS:
                i = end
                continue
            skip_name = name
            depth = 1
            i = end
            continue
        parts.append(folded[i:end])
        i = end
    return "".join(parts)


def _phrase_errors(label: str, text: str, *, html: bool) -> list[str]:
    """Main's substring check. HTML may drop data-moved-ok subtrees first."""
    folded = text.casefold()
    if html and _OPT_OUT in folded:
        folded = _without_moved_opt_outs(folded)
    errors: list[str] = []
    if _MOVED_MARK in folded:
        errors.append(f"{label} still says (moved)")
    if _MOVED_PHRASE in folded:
        errors.append(f"{label} still says has moved")
    return errors


def _moved_allowlist(root: Path) -> set[str]:
    path = root / _ALLOWLIST_NAME
    if not path.is_file():
        return set()
    found: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        entry = line.split("#", 1)[0].strip().lstrip("/")
        if entry:
            found.add(entry)
    return found


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
    allowed = _moved_allowlist(root)
    errors: list[str] = []
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if is_working_rel(rel) or not is_public_rel(rel):
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if _is_real_stub(html):
            continue
        if rel.as_posix() not in allowed:
            errors.extend(_phrase_errors(rel.as_posix(), html, html=True))
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
        if "llms.txt" not in allowed:
            errors.extend(_phrase_errors("llms.txt", text, html=False))
        for href in _MD_LINK.findall(text):
            target = _resolve_href(Path("llms.txt"), href)
            if target in stubs:
                errors.append(f"llms.txt links to stub {target}")
    return errors
