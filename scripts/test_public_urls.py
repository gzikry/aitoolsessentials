#!/usr/bin/env python3
"""Public URL and footer checks for the QA fixes."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from newsletter_hold import public_colophon_html
from premium_copy import homepage_footer_html
from validate_site import (
    ROOT,
    double_slash_external_hrefs,
    external_path_has_double_slash,
    unresolved_canonicals,
)

ADDRESS = "Keep/Cut Weekly by AIToolsEssentials, 1090 West Foothill, Claremont, CA 91711"
UNSUBSCRIBE = "Every email has an unsubscribe link."


def test_double_slash_is_the_path() -> None:
    if not external_path_has_double_slash("https://speechify.com//docs/"):
        raise AssertionError("speechify docs path")
    if not external_path_has_double_slash("https://rows.com//privacy"):
        raise AssertionError("rows privacy path")
    if not external_path_has_double_slash("https://www.shortwave.com//privacy/"):
        raise AssertionError("shortwave privacy path")
    if not external_path_has_double_slash("https://www.browse.ai//terms"):
        raise AssertionError("browse terms path")
    if external_path_has_double_slash("https://speechify.com/docs/"):
        raise AssertionError("a single path slash is fine")
    if external_path_has_double_slash("https://docs.speechify.com/guide"):
        raise AssertionError("a docs host is fine")


def test_published_urls_and_canonicals() -> None:
    slashes = double_slash_external_hrefs(ROOT)
    if slashes:
        raise AssertionError("double slash\n" + "\n".join(slashes[:8]))
    misses = unresolved_canonicals(ROOT)
    if misses:
        raise AssertionError("canonical\n" + "\n".join(misses))
    reports = (ROOT / "community" / "reports.html").read_text(encoding="utf-8")
    real = "https://aitoolsessentials.com/community/reports.html"
    if f'href="{real}"' not in reports:
        raise AssertionError("reports canonical")
    if "https://aitoolsessentials.com/community/reports/" in reports:
        raise AssertionError("reports still publishes the directory URL")


def test_footer_colophon() -> None:
    colophon = public_colophon_html()
    if ADDRESS not in colophon or UNSUBSCRIBE not in colophon:
        raise AssertionError(colophon)
    footer = homepage_footer_html()
    if ADDRESS not in footer or UNSUBSCRIBE not in footer:
        raise AssertionError("homepage generator dropped the colophon")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    hub = (ROOT / "newsletter" / "index.html").read_text(encoding="utf-8")
    if ADDRESS not in home or UNSUBSCRIBE not in home:
        raise AssertionError("homepage footer")
    if ADDRESS not in hub or UNSUBSCRIBE not in hub:
        raise AssertionError("newsletter index footer")


def test_sponsor_page_uses_the_container() -> None:
    page = (ROOT / "sponsor" / "index.html").read_text(encoding="utf-8")
    if "article-shell wide" not in page:
        raise AssertionError("sponsor page has no article shell")
    if 'data-nav="contained"' not in page or 'sponsor-offer' not in page:
        raise AssertionError("sponsor nav is not contained")


if __name__ == "__main__":
    test_double_slash_is_the_path()
    test_published_urls_and_canonicals()
    test_footer_colophon()
    test_sponsor_page_uses_the_container()
    print("ok")
