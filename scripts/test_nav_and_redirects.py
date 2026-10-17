#!/usr/bin/env python3
"""The shared nav and the duplicate-page redirects stay put."""
from __future__ import annotations

import sys
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
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
