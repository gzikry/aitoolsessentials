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
    '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>'
    '<nav class="nav-links" id="site-nav">'
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

# Homepage keeps the short nav from main: Stack Audit, Premium, Subscribe.
HOMEPAGE_HEADER = (
    '<header class="global-nav" aria-label="Primary navigation" data-nav="slim">'
    '<a class="brand home-appear" data-appear="0" href="/" aria-label="AIToolsEssentials home">'
    '<span class="brand-glyph">\u2726</span><span>AIToolsEssentials</span></a>'
    '<nav class="nav-links home-appear" data-appear="1">'
    '<a href="/tools/">Tools</a>'
    '<a href="/search/">Search</a>'
    '<a href="/stack-audit.html">Stack Audit</a>'
    '<a href="/premium/">Premium</a>'
    '<a href="/subscribe/">Subscribe</a>'
    '<!-- AIT SPONSOR NAV START --><a href="/sponsor/" rel="nofollow">Sponsor us</a><!-- AIT SPONSOR NAV END -->'
    "</nav>"
    + _FORM
    + '<a class="nav-cta home-appear" data-appear="1" href="/stack-audit.html">Free Stack Audit</a>'
    "</header>"
)

# Former site-header pages carried Sponsor us in the footer. The shared nav
# also has it; the footer link stays. Redirect stubs are not in this list.
FOOTER_SPONSOR_PAGES = (
    "articles/airtable-ai-vs-smartsuite.html",
    "articles/claude-vs-chatgpt.html",
    "articles/durable-ai-vs-wix-adi.html",
    "articles/elevenlabs-vs-playht.html",
    "articles/gamma-vs-beautiful-ai.html",
    "articles/grammarly-vs-prowritingaid.html",
    "articles/grok-vs-chatgpt.html",
    "articles/hootsuite-vs-buffer-ai.html",
    "articles/hubspot-vs-zoho-crm-ai.html",
    "articles/jasper-vs-copy-ai.html",
    "articles/make-vs-n8n.html",
    "articles/midjourney-vs-dalle.html",
    "articles/notion-ai-vs-mem.html",
    "articles/otter-vs-fireflies.html",
    "articles/zapier-vs-make.html",
    "comparisons/gemini-vs-claude.html",
    "guides/official/apple-intelligence/index.html",
    "guides/official/cohere/index.html",
    "guides/official/deepseek/index.html",
    "guides/official/index.html",
    "guides/official/qwen/index.html",
    "services/audit-intake.html",
    "services/audit-standard.html",
    "services/intake-received.html",
    "services/paid-audit.html",
    "services/sample-audit.html",
)
_FOOTER_SPONSOR = '<a href="/sponsor/" rel="nofollow">Sponsor us</a>'

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
    'class="nav-toggle"',
)
_HOME_LABELS = (
    'data-nav="slim"',
    'href="/tools/">Tools</a>',
    'href="/search/">Search</a>',
    'href="/stack-audit.html">Stack Audit</a>',
    'href="/premium/">Premium</a>',
    'href="/subscribe/">Subscribe</a>',
    'href="/sponsor/" rel="nofollow">Sponsor us</a>',
    'href="/stack-audit.html">Free Stack Audit</a>',
)


def canonical_header(contained: bool = False) -> str:
    if not contained:
        return CANONICAL_HEADER
    return CANONICAL_HEADER.replace(
        '<header class="global-nav">',
        '<header class="global-nav" data-nav="contained">',
        1,
    )


def homepage_header() -> str:
    return HOMEPAGE_HEADER


def _restore_footer_sponsor(html: str) -> str:
    match = re.search(r"<footer\b[^>]*>.*?</footer>", html, re.S)
    if not match:
        return html
    footer = match.group(0)
    if 'href="/sponsor/"' in footer and "Sponsor us" in footer:
        return html
    updated = footer.replace("</footer>", _FOOTER_SPONSOR + "</footer>", 1)
    return html[: match.start()] + updated + html[match.end() :]


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
            updated = html
        else:
            if rel.as_posix() == "index.html":
                replacement = HOMEPAGE_HEADER
            else:
                contained = 'data-nav="contained"' in match.group(0) or rel.as_posix() == "sponsor/index.html"
                replacement = canonical_header(contained)
            updated = _HEADER_RE.sub(replacement, html, count=1)
        if rel.as_posix() in FOOTER_SPONSOR_PAGES:
            updated = _restore_footer_sponsor(updated)
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
        labels = _HOME_LABELS if rel.as_posix() == "index.html" else _LABELS
        missing = [label for label in labels if label not in html]
        if missing:
            errors.append(f"{rel.as_posix()} nav missing {missing[0]}")
        if rel.as_posix() in FOOTER_SPONSOR_PAGES:
            footer = html[html.rfind("<footer") :]
            if 'href="/sponsor/"' not in footer or "Sponsor us" not in footer:
                errors.append(f"{rel.as_posix()} footer is missing Sponsor us")
    return errors
