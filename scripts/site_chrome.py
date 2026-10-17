#!/usr/bin/env python3
"""One primary nav for every public page."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_scope import is_public_rel

# Same box the header-search pass injects, so a later pass does not stack a second form.
_FORM = (
    "<!-- AIT HEADER SEARCH START -->"
    '<form class="ait-hs" id="ait-hs" role="search" action="/search/" method="get" autocomplete="off">'
    '<span class="ait-hs-ico" aria-hidden="true">\u2315</span>'
    '<input class="ait-hs-input" id="ait-hs-input" type="search" name="q" '
    'placeholder="Search tools, guides\u2026" aria-label="Search AIToolsEssentials" '
    'role="combobox" aria-expanded="false" aria-controls="ait-hs-list" aria-autocomplete="list" '
    'autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search">'
    '<ul class="ait-hs-list" id="ait-hs-list" role="listbox" aria-label="Search suggestions" hidden></ul>'
    "</form>"
    "<!-- AIT HEADER SEARCH END -->"
)

CANONICAL_HEADER = (
    '<header class="global-nav">'
    '<a class="brand" href="/"><span class="brand-glyph">\u2726</span><span>AIToolsEssentials</span></a>'
    '<nav class="nav-links">'
    '<a href="/tools/">Tools</a>'
    '<a href="/search/">Search</a>'
    '<a href="/comparisons/best-ai-tools.html">Best AI tools</a>'
    '<a href="/categories/">Categories</a>'
    '<a href="/articles/">Guides</a>'
    '<a href="/benchmarks/">Benchmarks</a>'
    '<a href="/articles/learn.html">Learn</a>'
    '<a href="/guides/switch-guides/">Switching</a>'
    '<!-- AIT SPONSOR NAV START --><a href="/sponsor/" rel="nofollow">Sponsor us</a><!-- AIT SPONSOR NAV END -->'
    "</nav>"
    + _FORM
    + '<a class="nav-cta" href="/legal/affiliate-disclosure.html">Disclosure</a>'
    "</header>"
)

_HEADER_RE = re.compile(
    r'<header class="(?:global-nav|site-header)"[^>]*>.*?</header>',
    re.S,
)
_LABELS = (
    'href="/tools/">Tools</a>',
    'href="/search/">Search</a>',
    'href="/comparisons/best-ai-tools.html">Best AI tools</a>',
    'href="/categories/">Categories</a>',
    'href="/articles/">Guides</a>',
    'href="/benchmarks/">Benchmarks</a>',
    'href="/articles/learn.html">Learn</a>',
    'href="/guides/switch-guides/">Switching</a>',
    'href="/sponsor/" rel="nofollow">Sponsor us</a>',
    'href="/legal/affiliate-disclosure.html">Disclosure</a>',
)


def canonical_header(contained: bool = False) -> str:
    if not contained:
        return CANONICAL_HEADER
    return CANONICAL_HEADER.replace(
        '<header class="global-nav">',
        '<header class="global-nav" data-nav="contained">',
        1,
    )


def unify_headers(root: Path) -> int:
    """Replace every public header with the same nav. Redirect stubs are left alone."""
    changed = 0
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if not is_public_rel(rel):
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if 'http-equiv="refresh"' in html:
            continue
        match = _HEADER_RE.search(html)
        if not match:
            continue
        contained = 'data-nav="contained"' in match.group(0) or rel.as_posix() == "sponsor/index.html"
        updated = _HEADER_RE.sub(canonical_header(contained), html, count=1)
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def header_label_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if not is_public_rel(rel):
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if 'http-equiv="refresh"' in html:
            continue
        if 'class="site-header"' in html:
            errors.append(f"{rel.as_posix()} still uses site-header")
            continue
        if "<header" not in html:
            continue
        missing = [label for label in _LABELS if label not in html]
        if missing:
            errors.append(f"{rel.as_posix()} nav missing {missing[0]}")
    return errors
