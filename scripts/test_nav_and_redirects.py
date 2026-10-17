#!/usr/bin/env python3
"""The shared nav and the duplicate-page redirects stay put."""
from __future__ import annotations

import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from consolidate_duplicates import (
    PAIRS,
    _phrase_errors,
    duplicate_errors,
    redirect_stub,
    stub_link_errors,
)
from site_chrome import CANONICAL_HEADER, header_label_errors

ROOT = Path(__file__).resolve().parents[1]
_PROSE = "The export button has moved to the Pro plan."


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


def _meta(attr: str, content: str) -> str:
    return _doc(f'{attr} content="{content}"><title>Compare</title>', "<p>Current page.</p>")


def _stub_phrase_and_jsonld() -> list[str]:
    """Substring check, plus an explicit opt-out. Cases are written in this file."""
    misses: list[str] = []
    compare = "<title>Compare</title>"
    safe = "<p>Current page.</p>"
    failures = {
        # T / Z. Titles fail on the phrase anywhere, including hyphen tails.
        "t6.html": _doc("<title>X has moved. See the current page</title>", safe),
        "t-mark.html": _doc("<title>Runway vs Pika (moved)</title>", safe),
        "z1.html": _doc("<title>Runway vs Pika has moved -</title>", safe),
        "z2.html": _doc("<title>has moved -- AIToolsEssentials</title>", safe),
        "z3.html": _doc("<title>has moved - aitoolsessentials.com</title>", safe),
        "z4.html": _doc("<title>has moved -AIToolsEssentials</title>", safe),
        # G. Body, blocks, span, and bare text.
        "g1.html": _doc(compare, "<p>This page has moved.</p>"),
        "g2.html": _doc(compare, "<div>This guide has moved.</div>"),
        "g3.html": _doc(compare, "<li>This article has moved</li>"),
        "g6.html": _doc(compare, "<section>This guide has moved.</section>"),
        "g-span.html": _doc(compare, "<span>This page has moved.</span>"),
        "g-bare.html": _doc(compare, "This page has moved."),
        "g-td.html": _doc(compare, "<table><tr><td>This page has moved.</td></tr></table>"),
        "g-article.html": _doc(compare, "<article>This article has moved.</article>"),
        "g-bq.html": _doc(compare, "<blockquote>This guide has moved.</blockquote>"),
        "g-main.html": _doc(compare, "<main>This page has moved.</main>"),
        "g-fig.html": _doc(compare, "<figure><figcaption>This article has moved.</figcaption></figure>"),
        "g-aside.html": _doc(compare, "<aside>This guide has moved.</aside>"),
        # K / V / D. Social tags and descriptions.
        "k3.html": _meta('<meta property="og:title"', "Runway vs Pika has moved"),
        "k5.html": _meta('<meta name="twitter:title"', "X (moved)"),
        "k-og-desc.html": _meta('<meta property="og:description"', "X has moved. See the current page"),
        "k-tw-desc.html": _meta('<meta name="twitter:description"', "X has moved? Open the new guide"),
        "v1.html": _meta('<meta name="description"', "Runway vs Pika has moved - AIToolsEssentials"),
        "v2.html": _meta('<meta name="description"', "has moved -- AIToolsEssentials"),
        "v3.html": _meta('<meta name="description"', "has moved - aitoolsessentials.com"),
        "v4.html": _meta('<meta name="description"', "has moved -AIToolsEssentials"),
        "v13.html": _meta('<meta name="description"', "X has moved. See the current page"),
        "v14.html": _meta('<meta name="description"', "X has moved. See the new guide"),
        "v15.html": _meta('<meta property="og:description"', "X has moved! Open the current page"),
        "v16.html": _meta('<meta name="twitter:description"', "X has moved? Open the new guide"),
        "d1.html": _meta('<meta name="description"', _PROSE),
        # J / W / C. JSON-LD, alt, aria-label, and a comment. Raw text, not a tag guess.
        "j-name.html": _doc(
            compare + '<script type="application/ld+json">{"name":"X has moved"}</script>',
            safe,
        ),
        "j-headline.html": _doc(
            compare + '<script type="application/ld+json">{"headline":"Runway vs Pika (moved)"}</script>',
            safe,
        ),
        "w-alt.html": _doc(compare, '<img alt="Runway vs Pika has moved">'),
        "w-aria.html": _doc(compare, '<button aria-label="Pricing has moved">Open</button>'),
        "c1.html": _doc(compare, "<!-- This page has moved. --><p>Current page.</p>"),
        # Prose fails until an element or ancestor opts out. A lookalike attribute does not.
        "export.html": _doc(compare, f"<p>{_PROSE}</p>"),
        "lookalike.html": _doc(compare, f'<p data-moved-okay>{_PROSE}</p>'),
        "opt-sibling.html": _doc(
            compare,
            f'<p data-moved-ok>{_PROSE}</p><p>This page has moved.</p>',
        ),
        "refresh-open.html": _doc(
            '<meta http-equiv="refresh" content="0; url=/elsewhere.html"><title>Elsewhere</title>',
            "<p>This page has moved.</p>",
        ),
        "img-then-bad.html": _doc(
            compare,
            '<img data-moved-ok alt="has moved"><p>This page has moved.</p>',
        ),
    }
    passes = {
        "export-ok.html": _doc(compare, f'<p data-moved-ok>{_PROSE}</p>'),
        "export-ancestor.html": _doc(compare, f'<section data-moved-ok><p>{_PROSE}</p></section>'),
        "export-case.html": _doc(compare, f'<p DATA-MOVED-OK>{_PROSE}</p>'),
        "nested-ok.html": _doc(
            compare,
            f'<div data-moved-ok><div>{_PROSE}</div></div><p>Current page.</p>',
        ),
        "img-ok.html": _doc(compare, '<img data-moved-ok alt="a>b has moved"><p>Current page.</p>'),
        "clean.html": _doc(compare, safe),
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
        found_lines = stub_link_errors(root)
        for name, html in failures.items():
            folded = html.casefold()
            if "has moved" in folded and not any(
                line.startswith(f"{name} still says has moved") for line in found_lines
            ):
                misses.append(f"validator missed has moved in {name}")
            if "(moved)" in folded and not any(
                line.startswith(f"{name} still says (moved)") for line in found_lines
            ):
                misses.append(f"validator missed (moved) in {name}")
        for name in passes:
            if any(line.startswith(f"{name} ") for line in found_lines):
                misses.append(f"validator flagged {name}")
        if "index.html JSON-LD url points at stub articles/suno-vs-udio.html" not in "\n".join(found_lines):
            misses.append("validator missed JSON-LD stub url")
        if any(line.startswith("articles/suno-vs-udio.html still says") for line in found_lines):
            misses.append("validator flagged the redirect stub itself")
    misses.extend(_allowlist_and_llms())
    misses.extend(_span_budget())
    misses.extend(_allowlist_file_is_empty())
    return misses


def _allowlist_and_llms() -> list[str]:
    misses: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "scripts").mkdir()
        (root / "scripts" / "moved_phrase_allowlist.txt").write_text(
            "# kept on purpose\nexport-allow.html\n/nested/ok.html\n",
            encoding="utf-8",
        )
        (root / "nested").mkdir()
        prose = _doc("<title>Compare</title>", f"<p>{_PROSE}</p>")
        (root / "export-allow.html").write_text(prose, encoding="utf-8")
        (root / "nested" / "ok.html").write_text(prose, encoding="utf-8")
        (root / "still-bad.html").write_text(prose, encoding="utf-8")
        (root / "llms.txt").write_text(_PROSE + "\n", encoding="utf-8")
        found = stub_link_errors(root)
        if any(line.startswith("export-allow.html ") or line.startswith("nested/ok.html ") for line in found):
            misses.append(f"allowlist page was flagged: {found}")
        if not any(line.startswith("still-bad.html still says has moved") for line in found):
            misses.append("allowlist hid a page that is not listed")
        if not any(line.startswith("llms.txt still says has moved") for line in found):
            misses.append("llms line was not flagged")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "llms.txt").write_text("X (moved)\n", encoding="utf-8")
        found = stub_link_errors(root)
        if not any(line.startswith("llms.txt still says (moved)") for line in found):
            misses.append("llms (moved) was not flagged")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "llms.txt").write_text("Current comparison of Runway and Pika.\n", encoding="utf-8")
        found = stub_link_errors(root)
        if found:
            misses.append(f"llms line without the phrase was flagged: {found}")
    return misses


def _span_budget() -> list[str]:
    """Unclosed spans stay linear. The opt-out path has to run, not the fast skip."""
    misses: list[str] = []
    spans = "<span>" * 20000
    cases = (
        ("open spans", spans + "has moved", True),
        ("opt-out spans", '<span data-moved-ok>' + spans + "has moved", False),
        ("phrase then spans", "has moved" + '<div data-moved-ok>' + spans, True),
    )
    for label, html, expect in cases:
        started = time.perf_counter()
        found = _phrase_errors("spans.html", html, html=True)
        elapsed = time.perf_counter() - started
        flagged = any("has moved" in line for line in found)
        if flagged != expect:
            misses.append(f"{label} flagged={flagged}")
        if elapsed > 1:
            misses.append(f"{label} took {elapsed:.3f}s")
    return misses


def _allowlist_file_is_empty() -> list[str]:
    misses: list[str] = []
    text = (ROOT / "scripts" / "moved_phrase_allowlist.txt").read_text(encoding="utf-8")
    paths = [line.split("#", 1)[0].strip() for line in text.splitlines()]
    paths = [entry for entry in paths if entry]
    if paths:
        misses.append(f"moved phrase allowlist is not empty: {paths}")
    return misses


if __name__ == "__main__":
    main()
