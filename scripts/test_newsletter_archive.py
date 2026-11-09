#!/usr/bin/env python3

from __future__ import annotations

import re
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
    if 'href="/newsletter/2026-w45.html"' not in w44_page or "Next · Issue 8 ·" not in w44_page:
        errors.append("w44 missing the next issue")
    if "Previous · Issue 6 · Cursor’s $20 Pro is off the page" not in w44_page:
        errors.append("w44 missing the previous issue")
    w45_page = (root / "newsletter" / "2026-w45.html").read_text(encoding="utf-8")
    if 'href="/newsletter/2026-w46.html"' not in w45_page or "Next · Issue 9 ·" not in w45_page:
        errors.append("w45 missing the next issue")
    if "Previous · Issue 7 · v0’s $20 tier is closed to new signups" not in w45_page:
        errors.append("w45 missing the previous issue")
    if "Issue 8 · 3 Nov 2026" not in w45_page or "Synthesia’s $9 Starter lasts one month" not in w45_page:
        errors.append("w45 missing the issue line or headline")
    if "{{{RESEND_UNSUBSCRIBE_URL}}}" in w45_page:
        errors.append("w45 published the send placeholder")
    w46_page = (root / "newsletter" / "2026-w46.html").read_text(encoding="utf-8")
    if "newsletter-pager-next" in w46_page:
        errors.append("w46 invented a newer issue")
    if "Previous · Issue 8 · Synthesia’s $9 Starter lasts one month" not in w46_page:
        errors.append("w46 missing the previous issue")
    if "Issue 9 · 10 Nov 2026" not in w46_page or "Otter’s monthly Pro costs twice the annual rate" not in w46_page:
        errors.append("w46 missing the issue line or headline")
    if "Tue 10 Nov 2026" in w46_page:
        errors.append("w46 public page kept the weekday")
    if "{{{RESEND_UNSUBSCRIBE_URL}}}" in w46_page:
        errors.append("w46 published the send placeholder")
    if "<strong>KEEP.</strong>" not in w46_page or "<strong>TEST FIRST.</strong>" not in w46_page or "<strong>CUT.</strong>" not in w46_page:
        errors.append("w46 missing keep/test/cut paragraphs")
    if "<table" in w46_page:
        errors.append("w46 public page kept an email table")
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
    for slug in ("2026-w46.html", "2026-w45.html", "2026-w44.html", "2026-w43.html", "2026-w42.html", "2026-w38.html", "2026-w35.html"):
        if f"https://aitoolsessentials.com/newsletter/{slug}" not in sitemap:
            errors.append(f"sitemap missing {slug}")
    issue1 = (root / "newsletter" / "2026-w35.html").read_text(encoding="utf-8")

    def _body(html: str) -> str:
        match = re.search(
            r'<div class="newsletter-body">(.*)</div>\s*<div class="newsletter-colophon">',
            html,
            flags=re.S,
        )
        return match.group(1) if match else ""

    if _body(issue1) != _body(before):
        errors.append("issue 1 body changed")
    if "Morning." not in issue1:
        errors.append("issue 1 fixture lost Morning.")
    if 'href="/newsletter/">← All past issues' not in issue1:
        errors.append("issue 1 missing the archive back-link")
    if 'href="/newsletter/">← All past issues' not in w44_page:
        errors.append("w44 missing the archive back-link")
    if 'href="/newsletter/">← All past issues' not in w45_page:
        errors.append("w45 missing the archive back-link")
    if 'href="/newsletter/">← All past issues' not in w46_page:
        errors.append("w46 missing the archive back-link")
    if "george" in w45_page.casefold():
        errors.append("w45 uses a personal name")
    if "1090 West Foothill, Claremont, CA 91711" not in w45_page:
        errors.append("w45 missing the postal address")
    hub = (root / "newsletter" / "index.html").read_text(encoding="utf-8")
    w46 = hub.find("/newsletter/2026-w46.html")
    w45 = hub.find("/newsletter/2026-w45.html")
    w44 = hub.find("/newsletter/2026-w44.html")
    w43 = hub.find("/newsletter/2026-w43.html")
    w42 = hub.find("/newsletter/2026-w42.html")
    w38 = hub.find("/newsletter/2026-w38.html")
    w35 = hub.find("/newsletter/2026-w35.html")
    if not (0 <= w46 < w45 < w44 < w43 < w42 < w38 < w35):
        errors.append(f"archive order is {w46}, {w45}, {w44}, {w43}, {w42}, {w38}, {w35}")
    if "Meeting note-takers charge monthly payers up to double. Fathom’s free plan records without a cap, so most people need one paid seat or none." not in hub:
        errors.append("archive index dropped the issue 9 dek")
    if "Synthesia cut its Starter renewal from $29 to $19 and put $9 on the first month. You still need only one AI avatar seat." not in hub:
        errors.append("archive index dropped the issue 8 dek")
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
    parsed45 = parse_draft((REPO / "admin" / "newsletter" / "2026-w45-draft.html").read_text(encoding="utf-8"), "2026-w45")
    if parsed45.when != "Tue 3 Nov 2026" or parsed45.issue != 8:
        errors.append(f"w45 draft parsed as issue {parsed45.issue} {parsed45.when!r}")
    if parsed45.title != "Synthesia’s $9 Starter lasts one month":
        errors.append(f"w45 title parsed as {parsed45.title!r}")
    parsed46 = parse_draft((REPO / "admin" / "newsletter" / "2026-w46-draft.html").read_text(encoding="utf-8"), "2026-w46")
    if parsed46.when != "Tue 10 Nov 2026" or parsed46.issue != 9:
        errors.append(f"w46 draft parsed as issue {parsed46.issue} {parsed46.when!r}")
    if parsed46.title != "Otter’s monthly Pro costs twice the annual rate":
        errors.append(f"w46 title parsed as {parsed46.title!r}")
    if "Sonaopus is $99 once" not in hub or "The AI bill you forgot to cancel" not in hub:
        errors.append("archive index dropped an issue")
    if "Issues 2 and 3 were not published." not in hub:
        errors.append("archive index skipped the unpublished gap")
    if "call-pill-keep" not in hub or "call-pill-test" not in hub or "call-pill-cut" not in hub:
        errors.append("archive index missing keep/test/cut pills")
    if 'href="/subscribe/"' not in hub:
        errors.append("archive index missing the subscribe page")
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
    if '<a href="/newsletter/">Newsletter</a>' not in footer:
        errors.append("homepage generator dropped the Newsletter link")
    if link not in (REPO / "index.html").read_text(encoding="utf-8"):
        errors.append("homepage footer missing the archive link")
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
