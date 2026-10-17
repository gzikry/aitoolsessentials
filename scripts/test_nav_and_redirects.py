#!/usr/bin/env python3
"""The shared nav and the duplicate-page redirects stay put."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from consolidate_duplicates import PAIRS, duplicate_errors, redirect_stub, stub_link_errors
from site_chrome import CANONICAL_HEADER, header_label_errors

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    errors: list[str] = []
    if 'class="nav-toggle"' not in CANONICAL_HEADER or 'id="site-nav"' not in CANONICAL_HEADER:
        errors.append("shared nav has no menu button")
    if 'href="/tools/">Tools</a>' not in CANONICAL_HEADER:
        errors.append("shared nav dropped Tools")
    if 'href="/legal/affiliate-disclosure.html">Disclosure</a>' not in CANONICAL_HEADER:
        errors.append("shared nav dropped Disclosure")
    if CANONICAL_HEADER.count(">Sponsor us</a>") != 1:
        errors.append("shared nav must have one Sponsor us link")
    sample = redirect_stub("Suno vs Udio", "comparisons/suno-vs-udio.html")
    if 'url=/comparisons/suno-vs-udio.html' not in sample or "noindex" not in sample:
        errors.append("redirect stub is not a noindex refresh")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    header = home.split("</header>", 1)[0]
    if 'data-nav="slim"' not in header:
        errors.append("homepage nav is not the short nav")
    for label in ("Stack Audit", "Premium", "Subscribe"):
        if f">{label}</a>" not in header:
            errors.append(f"homepage nav lost {label}")
    if 'class="button home-cta-primary" href="/stack-audit.html"' not in home:
        errors.append("homepage hero lost Free Stack Audit")
    claude = (ROOT / "articles/claude-vs-chatgpt.html").read_text(encoding="utf-8")
    footer = claude[claude.rfind("<footer") :]
    if 'href="/sponsor/" rel="nofollow">Sponsor us</a>' not in footer:
        errors.append("claude vs chatgpt footer lost Sponsor us")
    errors.extend(stub_link_errors(ROOT)[:8])
    errors.extend(header_label_errors(ROOT)[:8])
    errors.extend(duplicate_errors(ROOT)[:8])
    for loser, winner, _title in PAIRS:
        if loser in (ROOT / "index.html").read_text(encoding="utf-8"):
            errors.append(f"homepage still links {loser}")
        winner_html = (ROOT / winner).read_text(encoding="utf-8")
        if "This page has moved." in winner_html:
            errors.append(f"{winner} absorbed the redirect stub")
        if "affiliate" in (ROOT / loser).read_text(encoding="utf-8").casefold() and "affiliate" not in winner_html.casefold():
            errors.append(f"{winner} lost the affiliate disclosure that {loser} carried")
    site_js = (ROOT / "js/site.js").read_text(encoding="utf-8")
    if "event.key !== 'Escape'" not in site_js or "button.focus()" not in site_js:
        errors.append("Escape does not close the menu and return focus to the button")
    errors.extend(_stub_phrase_and_jsonld())
    if errors:
        raise SystemExit("\n".join(errors))


def _doc(head: str, body: str) -> str:
    return f"<!doctype html><html><head>{head}</head><body>{body}</body></html>"


def _stub_phrase_and_jsonld() -> list[str]:
    """Stub titles and short stub bodies fail. Ordinary 'has moved' sentences pass."""
    misses: list[str] = []
    failures = {
        "title-pipe.html": _doc("<title>Runway vs Pika has moved | AIToolsEssentials</title>", "<p>Current page.</p>"),
        "title-bare.html": _doc("<title>Runway vs Pika has moved</title>", "<p>Current page.</p>"),
        "h1.html": _doc("<title>Compare</title>", "<h1>Runway vs Pika has moved</h1>"),
        "h1-span.html": _doc("<title>Compare</title>", "<h1><span>Runway vs Pika has moved</span></h1>"),
        "h2.html": _doc("<title>Compare</title>", "<h2>X has moved.</h2>"),
        "div.html": _doc("<title>Compare</title>", "<div>This page has moved.</div>"),
        "guide.html": _doc("<title>Compare</title>", "<p>This guide has moved.</p>"),
    }
    passes = {
        "prose.html": _doc("<title>Pricing notes</title>", "<p>its pricing page has moved behind a login</p>"),
        "export.html": _doc("<title>Export</title>", "<p>The export button has moved to the Pro plan.</p>"),
        "comma.html": _doc("<title>pricing has moved, so…</title>", "<h1>pricing has moved, so…</h1>"),
    }
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "articles").mkdir()
        (root / "articles" / "suno-vs-udio.html").write_text(
            redirect_stub("Suno vs Udio", "comparisons/suno-vs-udio.html"),
            encoding="utf-8",
        )
        (root / "index.html").write_text(
            "<!doctype html><html><head>"
            '<script type="application/ld+json">'
            '{"url":"https://aitoolsessentials.com/articles/suno-vs-udio.html"}'
            "</script></head><body><p>Still here.</p></body></html>",
            encoding="utf-8",
        )
        for name, html in {**failures, **passes}.items():
            (root / name).write_text(html, encoding="utf-8")
        found = "\n".join(stub_link_errors(root))
        for name in failures:
            if f"{name} still says has moved" not in found:
                misses.append(f"validator missed {name}: {found}")
        for name in passes:
            if name in found:
                misses.append(f"validator flagged {name}: {found}")
        if "index.html JSON-LD url points at stub articles/suno-vs-udio.html" not in found:
            misses.append(f"validator missed JSON-LD stub url: {found}")
        if "articles/suno-vs-udio.html still says" in found:
            misses.append("validator flagged the redirect stub itself")
    return misses


if __name__ == "__main__":
    main()
