#!/usr/bin/env python3
"""Fold duplicate H1 pairs onto one page and leave a noindex redirect stub."""
from __future__ import annotations

import os
import re
import sys
from html import unescape
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


def _is_real_stub(html: str, header_noindex: bool = False) -> bool:
    """A redirect stub is a meta refresh plus a real noindex directive.

    The word noindex in prose, a comment, or a script does not count. A real
    directive is a robots or googlebot meta, an X-Robots-Tag meta, or an
    X-Robots-Tag rule in the site header config.
    """
    return _is_stub(html) and (header_noindex or _document_noindex(html))


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


# Main's check is a case-insensitive substring of the raw file. The same phrases
# are also checked after entities are decoded in their original spelling, zero-width
# characters are removed, and Unicode whitespace is collapsed. A real stub or an
# allowlisted path is the only exemption.
_MOVED_PHRASE = "has moved"
_MOVED_MARK = "(moved)"
_ALLOWLIST_NAME = Path("scripts/moved_phrase_allowlist.txt")
_ZERO_WIDTH = re.compile(
    "[\u00ad\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]"
)
_WS_RUN = re.compile(r"\s+")
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


def _read_tag_attrs(html: str, i: int) -> tuple[int, dict[str, str]]:
    """Read one start tag at '<'. One forward pass. Attribute names are lowercased."""
    n = len(html)
    j = i + 1
    while j < n and html[j] not in " \t\r\n/>":
        j += 1
    attrs: dict[str, str] = {}
    while j < n:
        char = html[j]
        if char == ">":
            return j + 1, attrs
        if char == "/" and j + 1 < n and html[j + 1] == ">":
            return j + 2, attrs
        if char.isspace() or char == "/":
            j += 1
            continue
        start = j
        while j < n and not html[j].isspace() and html[j] not in "=>/\"'":
            j += 1
        key = html[start:j].casefold()
        while j < n and html[j].isspace():
            j += 1
        value = ""
        if j < n and html[j] == "=":
            j += 1
            while j < n and html[j].isspace():
                j += 1
            if j < n and html[j] in "\"'":
                quote = html[j]
                j += 1
                value_start = j
                while j < n and html[j] != quote:
                    j += 1
                value = html[value_start:j]
                if j < n:
                    j += 1
            else:
                value_start = j
                while j < n and not html[j].isspace() and html[j] not in ">/":
                    j += 1
                value = html[value_start:j]
        if key:
            attrs[key] = value
    return n, attrs


def _tag_boundary(text: str, i: int, name: str) -> bool:
    end = i + 1 + len(name)
    return end >= len(text) or text[end] in " \t\r\n/>"


def _document_noindex(html: str) -> bool:
    """True for a robots/googlebot meta or an X-Robots-Tag meta whose content says noindex."""
    folded = html.casefold()
    n = len(html)
    i = 0
    while i < n:
        start = folded.find("<", i)
        if start < 0:
            return False
        if folded.startswith("<!--", start):
            end = folded.find("-->", start + 4)
            i = n if end < 0 else end + 3
            continue
        if folded.startswith("<script", start) and _tag_boundary(folded, start, "script"):
            end = folded.find("</script", start + 7)
            i = n if end < 0 else end + 9
            continue
        if folded.startswith("<style", start) and _tag_boundary(folded, start, "style"):
            end = folded.find("</style", start + 6)
            i = n if end < 0 else end + 8
            continue
        if folded.startswith("<meta", start) and _tag_boundary(folded, start, "meta"):
            end, attrs = _read_tag_attrs(html, start)
            name = attrs.get("name", "").strip().casefold()
            http_equiv = attrs.get("http-equiv", "").strip().casefold()
            content = attrs.get("content", "").casefold()
            if "noindex" in content and (
                name in {"robots", "googlebot"} or http_equiv == "x-robots-tag"
            ):
                return True
            i = end
            continue
        i = start + 1
    return False


def _x_robots_header_rules(root: Path) -> list[tuple[str, bool]]:
    """Path rules from a `_headers` file. Indented X-Robots-Tag lines belong to the path above."""
    path = root / "_headers"
    if not path.is_file():
        return []
    rules: list[tuple[str, bool]] = []
    current = ""
    noindex = False

    def flush() -> None:
        nonlocal current, noindex
        if current:
            rules.append((current, noindex))
        current = ""
        noindex = False

    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[:1].isspace():
            key, _, value = raw.strip().partition(":")
            if key.casefold() == "x-robots-tag" and "noindex" in value.casefold():
                noindex = True
            continue
        flush()
        current = raw.strip()
        noindex = False
    flush()
    return rules


def _header_noindex(rules: list[tuple[str, bool]], rel: str) -> bool:
    rel = rel.lstrip("/")
    for pattern, noindex in rules:
        if not noindex:
            continue
        pattern = pattern.strip().lstrip("/")
        if pattern in ("*", "/*"):
            return True
        if pattern.endswith("/*") and rel.startswith(pattern[:-1]):
            return True
        if rel == pattern:
            return True
    return False


def _normalized_phrase_text(text: str) -> str:
    """Decode entities in their original spelling, then fold case and whitespace."""
    decoded = unescape(text)
    stripped = _ZERO_WIDTH.sub("", decoded)
    return _WS_RUN.sub(" ", stripped).casefold()


def _phrase_errors(label: str, text: str) -> list[str]:
    """Main's raw substring, and the same phrases after entity and whitespace normalization."""
    raw = text.casefold()
    normalized = _normalized_phrase_text(text)
    errors: list[str] = []
    if _MOVED_MARK in raw or _MOVED_MARK in normalized:
        errors.append(f"{label} still says (moved)")
    if _MOVED_PHRASE in raw or _MOVED_PHRASE in normalized:
        errors.append(f"{label} still says has moved")
    return errors


def _moved_allowlist(root: Path) -> set[str]:
    """One public path per line. Blank lines and # comments are ignored."""
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
    header_rules = _x_robots_header_rules(root)
    errors: list[str] = []
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if is_working_rel(rel) or not is_public_rel(rel):
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if _is_real_stub(html, _header_noindex(header_rules, rel.as_posix())):
            continue
        if rel.as_posix() in allowed:
            print(f"allowlist skip {rel.as_posix()}")
        else:
            errors.extend(_phrase_errors(rel.as_posix(), html))
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
        if "llms.txt" in allowed:
            print("allowlist skip llms.txt")
        else:
            errors.extend(_phrase_errors("llms.txt", text))
        for href in _MD_LINK.findall(text):
            target = _resolve_href(Path("llms.txt"), href)
            if target in stubs:
                errors.append(f"llms.txt links to stub {target}")
    return errors
