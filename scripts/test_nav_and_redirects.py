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
    _short_stub_copy,
    duplicate_errors,
    redirect_stub,
    stub_link_errors,
)
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
    """Titles and headings fail on the phrase. Short stub lines fail. Prose passes.

    'Pricing has moved. Here's what changed' and 'Runway has moved - Pika has not'
    fail when they are the title. The same sentences pass in body prose. That split
    is intentional: a real title never needs the phrase.
    """
    misses: list[str] = []
    failures = {
        # Z1–Z4. Hyphen tails used to slip through the separator regex.
        "z1.html": _doc("<title>Runway vs Pika has moved -</title>", "<p>Current page.</p>"),
        "z2.html": _doc("<title>has moved -- AIToolsEssentials</title>", "<p>Current page.</p>"),
        "z3.html": _doc("<title>has moved - aitoolsessentials.com</title>", "<p>Current page.</p>"),
        "z4.html": _doc("<title>has moved -AIToolsEssentials</title>", "<p>Current page.</p>"),
        # T6. A title that continues after the phrase still fails.
        "t6.html": _doc("<title>X has moved. See the current page</title>", "<p>Current page.</p>"),
        "title-bang.html": _doc("<title>X has moved! See the new guide.</title>", "<p>Current page.</p>"),
        "title-pipe.html": _doc("<title>Runway vs Pika has moved | AIToolsEssentials</title>", "<p>Current page.</p>"),
        "title-bare.html": _doc("<title>Runway vs Pika has moved</title>", "<p>Current page.</p>"),
        "h1.html": _doc("<title>Compare</title>", "<h1>Runway vs Pika has moved</h1>"),
        "h1-span.html": _doc("<title>Compare</title>", "<h1><span>Runway vs Pika has moved</span></h1>"),
        "h1-paren.html": _doc("<title>Compare</title>", "<h1>X (has moved)</h1>"),
        "title-moved-mark.html": _doc("<title>Runway vs Pika (moved)</title>", "<p>Current page.</p>"),
        # Comma cases. A comma does not save a title or heading.
        "title-comma-ellipsis.html": _doc("<title>Runway vs Pika has moved, …</title>", "<p>Current page.</p>"),
        "h1-comma.html": _doc("<title>Compare</title>", "<h1>Runway vs Pika has moved,</h1>"),
        "title-comma-pipe.html": _doc("<title>Runway vs Pika has moved, | AIToolsEssentials</title>", "<p>Current page.</p>"),
        # These two are the body sentences below. As titles they fail on purpose.
        "title-pricing-changed.html": _doc(
            "<title>Pricing has moved. Here's what changed</title>",
            "<p>Current page.</p>",
        ),
        "title-runway-pika.html": _doc(
            "<title>Runway has moved - Pika has not</title>",
            "<p>Current page.</p>",
        ),
        # G1–G7. Stub sentence, or the whole short block is '<X> has moved' plus punctuation.
        "g1.html": _doc("<title>Compare</title>", "<p>This page has moved.</p>"),
        "g2.html": _doc("<title>Compare</title>", "<div>This guide has moved.</div>"),
        "g3.html": _doc("<title>Compare</title>", "<li>This article has moved</li>"),
        "g4.html": _doc("<title>Compare</title>", "<p>Runway vs Pika has moved.</p>"),
        "g5.html": _doc("<title>Compare</title>", "<li>Runway vs Pika has moved,</li>"),
        "g6.html": _doc("<title>Compare</title>", "<div>Runway vs Pika has moved…</div>"),
        "g7.html": _doc("<title>Compare</title>", "<h2>X has moved.</h2>"),
    }
    passes = {
        "comma.html": _doc("<title>Pricing notes</title>", "<p>pricing has moved, so…</p>"),
        "export.html": _doc("<title>Export</title>", "<p>The export button has moved to the Pro plan.</p>"),
        "login.html": _doc("<title>Pricing</title>", "<li>its pricing page has moved behind a login</li>"),
        "pricing-prose.html": _doc("<title>Pricing</title>", "<p>Pricing has moved. Here's what changed</p>"),
        "runway-prose.html": _doc("<title>Compare</title>", "<div>Runway has moved - Pika has not</div>"),
        "hyphen-on.html": _doc("<title>Plans</title>", "<p>The team has moved-on to the new plan.</p>"),
        "hyphen-in.html": _doc("<title>Layout</title>", "<p>The control has moved-in from the sidebar.</p>"),
        "meta-prose.html": _doc(
            '<meta name="description" content="X has moved. See the current page"><title>Compare</title>',
            "<p>Current page.</p>",
        ),
        "z2-body.html": _doc("<title>Compare</title>", "<p>has moved -- AIToolsEssentials</p>"),
        "z3-body.html": _doc("<title>Compare</title>", "<p>has moved - aitoolsessentials.com</p>"),
        "z4-body.html": _doc("<title>Compare</title>", "<div>has moved -AIToolsEssentials</div>"),
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
        found = "\n".join(found_lines)
        for name in failures:
            if not any(line.startswith(f"{name} still says has moved") for line in found_lines):
                misses.append(f"validator missed {name}: {found}")
        for name in passes:
            if any(line.startswith(f"{name} ") for line in found_lines):
                misses.append(f"validator flagged {name}: {found}")
        if "index.html JSON-LD url points at stub articles/suno-vs-udio.html" not in found:
            misses.append(f"validator missed JSON-LD stub url: {found}")
        if "articles/suno-vs-udio.html still says" in found:
            misses.append("validator flagged the redirect stub itself")
    stub = "This page has moved. "
    exact = stub + ("x" * (180 - len(stub)))
    over = stub + ("x" * (181 - len(stub)))
    if len(exact) != 180 or not _short_stub_copy(exact):
        misses.append("a 180-character stub sentence was not flagged")
    if len(over) != 181 or _short_stub_copy(over):
        misses.append("a stub sentence longer than 180 characters was flagged")
    long_copy = "Pricing notes has moved" + (", " * 20000) + "so the plan changed"
    started = time.perf_counter()
    flagged = _short_stub_copy(long_copy)
    elapsed = time.perf_counter() - started
    if flagged:
        misses.append("a long punctuation run was treated as a stub")
    if elapsed > 0.2:
        misses.append(f"a long punctuation run took {elapsed:.3f}s")
    return misses


if __name__ == "__main__":
    main()
