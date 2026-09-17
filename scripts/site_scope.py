#!/usr/bin/env python3
"""Single source of truth for what counts as a site page.

`refresh_sitemap()` has always excluded working directories from the sitemap,
but the page-walking code in the generators and the validator did not share that
definition. So a raw third-party scrape saved under `marketing/` (the daily
Sourcee journo-request feed, `_feed_ai_topic.html`) was treated as a public
page: the generators injected site head markup into it, and the validator then
failed on its external logins, its `/_next/...` asset paths, and its
`/#features` fragments — 111 errors, none of them about our own site.

Two scopes are needed, because `admin/` is deliberately treated differently by
different checks (it is live but internal, and several checks already exempt it
while others still cover it):

- WORKING_DIRS: scratch/working artifacts. Never site pages, never published.
  Nothing that walks "the site" may touch these.
- NON_PUBLIC_DIRS: what the sitemap already excludes — WORKING_DIRS plus the
  internal `admin/` paste packs and the `go/` redirect stubs.

Use `iter_working_html` to *remove* scratch files from a walk without changing
how `admin/` is handled, and `is_public_rel` where the full public definition is
what is meant.
"""
from __future__ import annotations

from pathlib import Path

# Working/scratch artifacts. Never published, never part of the site.
WORKING_DIRS = frozenset({
    'marketing',
    'scripts',
    'content_briefs',
    'audit_reports',
})

# What the sitemap excludes: working dirs, internal admin tools, redirect stubs.
NON_PUBLIC_DIRS = WORKING_DIRS | {'admin', 'go'}


def is_working_rel(rel: Path) -> bool:
    """True for scratch/working paths that are never site pages."""
    parts = rel.parts
    if any(part.startswith('.') for part in parts):
        return True
    return bool(WORKING_DIRS.intersection(parts))


def is_public_rel(rel: Path) -> bool:
    """True when a root-relative path is a public, crawlable site page."""
    parts = rel.parts
    if any(part.startswith('.') for part in parts):
        return False
    return not NON_PUBLIC_DIRS.intersection(parts)


def is_public_site_html(root: Path, path: Path) -> bool:
    """True when `path` is a public site page under `root`."""
    return is_public_rel(path.relative_to(root))


def iter_working_html(root):
    """Yield (path, rel_path) for site HTML, skipping scratch dirs.

    `admin/` and `go/` are still yielded so existing per-check exemptions for
    those directories keep working unchanged.
    """
    root = Path(root)
    for path in sorted(root.rglob('*.html')):
        rel = path.relative_to(root)
        if is_working_rel(rel):
            continue
        yield path, rel
