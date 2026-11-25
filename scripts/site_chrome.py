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
    'placeholder="Search\u2026" aria-label="Search AIToolsEssentials" '
    'role="combobox" aria-expanded="false" aria-controls="ait-hs-list" aria-autocomplete="list" '
    'autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search">'
    '<ul class="ait-hs-list" id="ait-hs-list" role="listbox" aria-label="Search suggestions" hidden></ul>'
    "</form>"
    "<!-- AIT HEADER SEARCH END -->"
)

# One header on every page, the homepage included: six plain links and the search box.
NAV_LINKS = (
    ("/tools/", "Tools", ""),
    ("/comparisons/", "Compare", ""),
    ("/price-changes/", "Price alerts", ""),
    ("/newsletter/", "Newsletter", ""),
    ("/founders/", "For founders", ""),
    ("/sponsor/", "Sponsor", ' rel="nofollow"'),
)


def _nav_html() -> str:
    links = []
    for href, label, extra in NAV_LINKS:
        link = f'<a href="{href}"{extra}>{label}</a>'
        if href == "/sponsor/":
            link = "<!-- AIT SPONSOR NAV START -->" + link + "<!-- AIT SPONSOR NAV END -->"
        links.append(link)
    return "".join(links)


CANONICAL_HEADER = (
    '<header class="global-nav">'
    '<a class="brand" href="/"><span class="brand-glyph">ATE</span><span>AIToolsEssentials</span></a>'
    '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>'
    '<nav class="nav-links" id="site-nav">'
    + _nav_html()
    + "</nav>"
    + _FORM
    + "</header>"
)

# The homepage uses the same header. It keeps its aria label so screen readers hear "Primary navigation".
HOMEPAGE_HEADER = CANONICAL_HEADER.replace(
    '<header class="global-nav">',
    '<header class="global-nav" aria-label="Primary navigation">',
    1,
)

# One footer on every page that uses the shared chrome.
CANONICAL_FOOTER = (
    '<footer class="footer" data-footer="site">'
    '<nav class="footer-row" aria-label="Site">'
    '<a href="/tools/">Tools</a>'
    '<a href="/comparisons/">Compare</a>'
    '<a href="/price-changes/">Price alerts</a>'
    '<a href="/newsletter/">Newsletter</a>'
    '<a href="/founders/">For founders</a>'
    '<a href="/sponsor/" rel="nofollow">Sponsor us</a>'
    '<a href="/submit/">Submit a tool</a>'
    "</nav>"
    '<nav class="footer-row footer-row-small" aria-label="About">'
    '<a href="/legal/about.html">About</a>'
    '<a href="/search/">Search</a>'
    '<a href="/methodology/">How we review</a>'
    '<a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>'
    '<a href="/legal/corrections.html">Corrections</a>'
    '<a href="mailto:contact@aitoolsessentials.com">Contact</a>'
    '<a href="/legal/privacy.html">Privacy</a>'
    '<a href="/legal/terms.html">Terms</a>'
    '<a href="/embeds/">Embeds</a>'
    "</nav>"
    '<p class="footer-colophon">\u00a9 2026 AIToolsEssentials. '
    "Keep, Test, Cut by AIToolsEssentials, 1090 West Foothill, Claremont, CA 91711. "
    "Every email has an unsubscribe link.</p>"
    "</footer>"
)
_FOOTER_RE = re.compile(r'<footer class="footer"[^>]*>.*?</footer>', re.S)


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
    "services/audit-thanks/index.html",
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
_LABELS = tuple(f'href="{href}"{extra}>{label}</a>' for href, label, extra in NAV_LINKS) + (
    'class="nav-toggle"',
    'data-footer="site"',
)
_HOME_LABELS = _LABELS


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
        updated = _FOOTER_RE.sub(lambda _m: CANONICAL_FOOTER, updated, count=1)
        if rel.as_posix() in FOOTER_SPONSOR_PAGES:
            updated = _restore_footer_sponsor(updated)
        updated = _ensure_newsletter_footer(updated)
        updated = _ensure_embeds_footer(updated)
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
        if '<footer class="footer"' not in html:
            labels_needed = [label for label in _LABELS if label != 'data-footer="site"']
        else:
            labels_needed = list(_LABELS)
        missing = [label for label in labels_needed if label not in html]
        if missing:
            errors.append(f"{rel.as_posix()} nav missing {missing[0]}")
        if "<footer" in html and 'href="/newsletter/">Newsletter</a>' not in html:
            errors.append(f"{rel.as_posix()} footer is missing Newsletter")
        if rel.as_posix() in FOOTER_SPONSOR_PAGES:
            footer = html[html.rfind("<footer") :]
            if 'href="/sponsor/"' not in footer or "Sponsor us" not in footer:
                errors.append(f"{rel.as_posix()} footer is missing Sponsor us")
    return errors


_NEWSLETTER_FOOTER = '<a href="/newsletter/">Newsletter</a>'


def _ensure_newsletter_footer(html: str) -> str:
    if _NEWSLETTER_FOOTER in html or "<footer" not in html:
        return html
    return html.replace("</footer>", _NEWSLETTER_FOOTER + "</footer>", 1)


_EMBEDS_FOOTER = '<a href="/embeds/">Embeds</a>'


def _ensure_embeds_footer(html: str) -> str:
    if _EMBEDS_FOOTER in html or "<footer" not in html:
        return html
    return html.replace("</footer>", _EMBEDS_FOOTER + "</footer>", 1)
