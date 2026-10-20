#!/usr/bin/env python3
"""Publish /submit/ as the same tool form submit-tool.html already serves.

GitHub Pages returns 200 for /submit/ only when submit/index.html exists.
Relative links on the root form would 404 from that directory, so the copy
uses root-absolute URLs. The page stays noindex and keeps the canonical on
submit-tool.html. ?verified=1 is the script already on the form page.
"""
from __future__ import annotations

import re
from pathlib import Path

_ATTR = re.compile(
    r"""(?P<attr>href|src)(?P<eq>\s*=\s*)(?P<q>["'])(?P<url>[^"']+)(?P=q)""",
    re.I,
)
_HEAD = re.compile(r"<head\b[^>]*>", re.I)
_ROBOTS = '<meta name="robots" content="noindex,follow">'
_SOURCE = Path("submit-tool.html")
_DEST = Path("submit") / "index.html"


def _root_url(url: str) -> str:
    if not url or url.startswith(
        ("/", "#", "?", "http://", "https://", "mailto:", "javascript:", "data:", "//")
    ):
        return url
    return "/" + url


def render(html: str) -> str:
    """Root-absolute copy of the submit form, hidden from the index."""

    def repl(match: re.Match[str]) -> str:
        url = match.group("url")
        rooted = _root_url(url)
        if rooted == url:
            return match.group(0)
        return (
            match.group("attr")
            + match.group("eq")
            + match.group("q")
            + rooted
            + match.group("q")
        )

    page = _ATTR.sub(repl, html)
    if 'name="robots" content="noindex' in page:
        return page
    head = _HEAD.search(page)
    if head is None:
        raise RuntimeError("submit-tool.html has no head")
    return page[: head.end()] + _ROBOTS + page[head.end() :]


def publish(root: Path) -> Path:
    source = root / _SOURCE
    dest = root / _DEST
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(render(source.read_text(encoding="utf-8")), encoding="utf-8")
    return dest


if __name__ == "__main__":
    written = publish(Path(__file__).resolve().parents[1])
    print("Published " + written.as_posix())
