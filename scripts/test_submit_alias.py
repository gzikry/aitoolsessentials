#!/usr/bin/env python3
""" /submit/ hosts the existing tool form and the verified-listing thank-you."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from publish_submit_page import render

REPO = Path(__file__).resolve().parents[1]
VERIFIED = "https://buy.stripe.com/7sY6oG3Ed2SF7JZ3eD0x205"
FORM = 'id="tool-submission"'
THANKS = 'id="verified-thanks"'


def _fail(message: str) -> None:
    raise AssertionError(message)


def test_render_roots_links_and_hides_the_alias() -> None:
    page = render(
        "<!doctype html><html><head>"
        '<link rel="stylesheet" href="css/styles.css">'
        "</head><body>"
        '<a href="tools/">Tools</a>'
        '<a href="/sponsor/#verified-listing">Verified</a>'
        '<a href="https://buy.stripe.com/example">Pay</a>'
        "</body></html>"
    )
    if page.count('name="robots" content="noindex,follow"') != 1:
        _fail("alias robots meta count")
    if 'href="/css/styles.css"' not in page or 'href="css/styles.css"' in page:
        _fail("stylesheet was not rooted: " + page)
    if 'href="/tools/"' not in page:
        _fail("directory link was not rooted")
    if 'href="/sponsor/#verified-listing"' not in page:
        _fail("root-absolute link changed")
    if 'href="https://buy.stripe.com/example"' not in page:
        _fail("external link changed")
    again = render(page)
    if again != page:
        _fail("rendering the alias twice changed it")


def test_repo_submit_alias_hosts_the_form() -> None:
    source = (REPO / "submit-tool.html").read_text(encoding="utf-8")
    alias_path = REPO / "submit" / "index.html"
    if not alias_path.is_file():
        _fail("submit/index.html is missing")
    alias = alias_path.read_text(encoding="utf-8")
    if alias != render(source):
        _fail("submit/index.html drifted from submit-tool.html")
    for label, page in (("source", source), ("alias", alias)):
        if FORM not in page:
            _fail(label + " is missing the submission form")
        if THANKS not in page:
            _fail(label + " is missing the verified thank-you")
        if VERIFIED not in page:
            _fail(label + " is missing the verified listing link")
        if "get('verified')==='1'" not in page:
            _fail(label + " does not show the thank-you for verified=1")
    if 'name="robots" content="noindex,follow"' not in alias:
        _fail("submit/index.html is indexable")
    if 'href="css/' in alias or 'src="js/' in alias:
        _fail("submit/index.html still has directory-relative assets")
    if "The submission form is on" in alias:
        _fail("submit/index.html still points away from the form")
    if 'rel="canonical" href="https://aitoolsessentials.com/submit-tool.html"' not in alias:
        _fail("submit alias lost the submit-tool canonical")


if __name__ == "__main__":
    test_render_roots_links_and_hides_the_alias()
    test_repo_submit_alias_hosts_the_form()
    print("submit alias ok")
