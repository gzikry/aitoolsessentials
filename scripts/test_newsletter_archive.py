#!/usr/bin/env python3

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from newsletter_archive import sync_archive
from premium_copy import homepage_footer_html

REPO = Path(__file__).resolve().parent.parent


def main() -> None:
    errors: list[str] = []
    root = Path(tempfile.mkdtemp())
    shutil.copytree(REPO / "admin" / "newsletter", root / "admin" / "newsletter")
    shutil.copytree(REPO / "newsletter", root / "newsletter")
    before = (root / "newsletter" / "2026-w35.html").read_text(encoding="utf-8")
    (root / "newsletter" / "2026-w42.html").unlink()
    (root / "newsletter" / "2026-w38.html").unlink()
    sync_archive(root)
    page = (root / "newsletter" / "2026-w42.html").read_text(encoding="utf-8")
    if "<h1 class=\"newsletter-subject\">ChatGPT Go is $8 a month</h1>" not in page:
        errors.append("w42 title missing")
    if "newsletter-letter" not in page or "letter-rule--gold" not in page:
        errors.append("w42 missing the paper letter")
    if "Morning." in page:
        errors.append("w42 copied the issue 1 opening")
    if "george" in page.casefold():
        errors.append("w42 uses a personal name")
    if "1090 West Foothill, Claremont, CA 91711" not in page:
        errors.append("w42 missing the postal address")
    if "not reliably exposed" in page:
        errors.append("w42 kept issue 1's price note")
    if "newsletter-pager-prev" not in page or "Issue 4 · Sonaopus is $99 once" not in page:
        errors.append("w42 missing the previous issue")
    if "newsletter-pager-next" in page:
        errors.append("w42 invented a next issue")
    if 'href="/subscribe/">Get the free email' not in page:
        errors.append("w42 missing the subscribe CTA")
    w38_page = (root / "newsletter" / "2026-w38.html").read_text(encoding="utf-8")
    if "newsletter-pager-prev" not in w38_page or "newsletter-pager-next" not in w38_page:
        errors.append("w38 missing prev and next")
    if 'href="/subscribe/">Get the free email' not in w38_page:
        errors.append("w38 missing the subscribe CTA")
    sitemap = (REPO / "sitemap.xml").read_text(encoding="utf-8")
    for slug in ("2026-w42.html", "2026-w38.html", "2026-w35.html"):
        if f"https://aitoolsessentials.com/newsletter/{slug}" not in sitemap:
            errors.append(f"sitemap missing {slug}")
    if (root / "newsletter" / "2026-w35.html").read_text(encoding="utf-8") != before:
        errors.append("issue 1 page changed")
    if "Morning." not in before:
        errors.append("issue 1 fixture lost Morning.")
    hub = (root / "newsletter" / "index.html").read_text(encoding="utf-8")
    w42 = hub.find("/newsletter/2026-w42.html")
    w38 = hub.find("/newsletter/2026-w38.html")
    w35 = hub.find("/newsletter/2026-w35.html")
    if not (0 <= w42 < w38 < w35):
        errors.append(f"archive order is {w42}, {w38}, {w35}")
    if "Sonaopus is $99 once" not in hub or "The AI bill you forgot to cancel" not in hub:
        errors.append("archive index dropped an issue")
    first = (root / "newsletter" / "2026-w42.html").read_bytes()
    sync_archive(root)
    if (root / "newsletter" / "2026-w42.html").read_bytes() != first:
        errors.append("second publish changed w42")
    if (root / "newsletter" / "index.html").read_text(encoding="utf-8") != hub:
        errors.append("second publish changed the index")
    footer = homepage_footer_html()
    link = '<a href="/newsletter/">Keep, Test, Cut</a>'
    if link not in footer:
        errors.append("homepage generator dropped the archive link")
    if link not in (REPO / "index.html").read_text(encoding="utf-8"):
        errors.append("homepage footer missing the archive link")
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
