#!/usr/bin/env python3

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from newsletter_archive import parse_draft, sync_archive
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
    if 'href="/newsletter/2026-w43.html"' not in page or "Next · Issue 6 ·" not in page:
        errors.append("w42 missing the next issue")
    w43_page = (root / "newsletter" / "2026-w43.html").read_text(encoding="utf-8")
    if 'href="/newsletter/2026-w44.html"' not in w43_page or "Next · Issue 7 ·" not in w43_page:
        errors.append("w43 missing the next issue")
    if "Previous · Issue 5 · ChatGPT Go is $8 a month" not in w43_page:
        errors.append("w43 missing the previous issue")
    if "Issue 6 · 20 Oct 2026" not in w43_page or "Cursor’s $20 Pro is off the page" not in w43_page:
        errors.append("w43 missing the issue line or headline")
    w44_page = (root / "newsletter" / "2026-w44.html").read_text(encoding="utf-8")
    if "newsletter-pager-next" in w44_page:
        errors.append("w44 invented a newer issue")
    if "Previous · Issue 6 · Cursor’s $20 Pro is off the page" not in w44_page:
        errors.append("w44 missing the previous issue")
    if "Issue 7 · 27 Oct 2026" not in w44_page or "v0’s $20 tier is closed to new signups" not in w44_page:
        errors.append("w44 missing the issue line or headline")
    if 'href="/compare/ai-app-builders/"' not in w44_page:
        errors.append("w44 missing the app-builder calculator")
    if "Premium $20/mo closed to new signups" not in w44_page or "Starter tier from our 21 Aug check is off the page" not in w44_page:
        errors.append("w44 missing the verified pricing copy")
    if "george" in w43_page.casefold():
        errors.append("w43 uses a personal name")
    if "1090 West Foothill, Claremont, CA 91711" not in w43_page:
        errors.append("w43 missing the postal address")
    if 'href="/subscribe/">Get the free email' not in page:
        errors.append("w42 missing the subscribe CTA")
    w38_page = (root / "newsletter" / "2026-w38.html").read_text(encoding="utf-8")
    if "newsletter-pager-prev" not in w38_page or "newsletter-pager-next" not in w38_page:
        errors.append("w38 missing prev and next")
    if 'href="/subscribe/">Get the free email' not in w38_page:
        errors.append("w38 missing the subscribe CTA")
    sitemap = (REPO / "sitemap.xml").read_text(encoding="utf-8")
    for slug in ("2026-w44.html", "2026-w43.html", "2026-w42.html", "2026-w38.html", "2026-w35.html"):
        if f"https://aitoolsessentials.com/newsletter/{slug}" not in sitemap:
            errors.append(f"sitemap missing {slug}")
    if (root / "newsletter" / "2026-w35.html").read_text(encoding="utf-8") != before:
        errors.append("issue 1 page changed")
    if "Morning." not in before:
        errors.append("issue 1 fixture lost Morning.")
    hub = (root / "newsletter" / "index.html").read_text(encoding="utf-8")
    w44 = hub.find("/newsletter/2026-w44.html")
    w43 = hub.find("/newsletter/2026-w43.html")
    w42 = hub.find("/newsletter/2026-w42.html")
    w38 = hub.find("/newsletter/2026-w38.html")
    w35 = hub.find("/newsletter/2026-w35.html")
    if not (0 <= w44 < w43 < w42 < w38 < w35):
        errors.append(f"archive order is {w44}, {w43}, {w42}, {w38}, {w35}")
    if "Cursor now sells one five-rung ladder. If you already pay for a plan, nothing forces you to move." not in hub:
        errors.append("archive index dropped the issue 6 dek")
    if "which coding subscription to keep" in hub:
        errors.append("archive index kept issue 1's second sentence")
    parsed = parse_draft((REPO / "admin" / "newsletter" / "2026-w43-draft.html").read_text(encoding="utf-8"), "2026-w43")
    if parsed.when != "Tue 20 Oct 2026" or parsed.issue != 6:
        errors.append(f"w43 draft parsed as issue {parsed.issue} {parsed.when!r}")
    parsed44 = parse_draft((REPO / "admin" / "newsletter" / "2026-w44-draft.html").read_text(encoding="utf-8"), "2026-w44")
    if parsed44.when != "27 Oct 2026" or parsed44.issue != 7:
        errors.append(f"w44 draft parsed as issue {parsed44.issue} {parsed44.when!r}")
    if parsed44.title != "v0’s $20 tier is closed to new signups":
        errors.append(f"w44 title parsed as {parsed44.title!r}")
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
