#!/usr/bin/env python3
"""Removed public URLs redirect, and the sitemap lists only canonical indexable URLs."""
from __future__ import annotations

import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from legacy_redirects import LEGACY
from site_health import run as health_run
from site_scope import is_public_rel
from validate_site import site_urls

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://aitoolsessentials.com"


def main() -> None:
    errors: list[str] = []
    known = site_urls(ROOT)
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    for line in ("Disallow: /admin/", "Disallow: /checkout/", "Disallow: /go/", "Disallow: /xmlrpc.php", "Disallow: /wp-login.php"):
        if line not in robots:
            errors.append(f"robots.txt missing {line}")
    if "Allow: /" not in robots:
        errors.append("robots.txt no longer allows the public site")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    for loser, winner, _title in LEGACY:
        page = ROOT / loser
        if not page.is_file():
            errors.append(f"missing redirect stub {loser}")
            continue
        html = page.read_text(encoding="utf-8")
        dest = DOMAIN + "/" + winner
        if f'href="{dest}"' not in html:
            errors.append(f"{loser} canonical is not {dest}")
        if 'http-equiv="refresh"' not in html or f"url=/{winner}" not in html:
            errors.append(f"{loser} is not a refresh redirect")
        if 'name="robots" content="noindex' not in html:
            errors.append(f"{loser} is indexable")
        if dest not in known:
            errors.append(f"{loser} points at a URL the site does not serve: {dest}")
        banned = []
        for form in _public_forms(loser):
            banned.append(form)
            banned.append(quote(form, safe="/"))
        if any(form in loc for loc in locs for form in banned):
            errors.append(f"sitemap still lists {loser}")
    indexable = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if not is_public_rel(rel) or path.name == "404.html":
            continue
        html = path.read_text(encoding="utf-8", errors="ignore")
        if 'name="robots" content="noindex' in html or 'http-equiv="refresh"' in html:
            continue
        url = _page_url(rel)
        canon = re.search(r'rel="canonical" href="([^"]+)"', html)
        if canon:
            target = unescape(unquote(urlparse(canon.group(1)).path))
            if target.rstrip("/") != url.rstrip("/"):
                errors.append(f"{rel} is indexable but canonical is {canon.group(1)}")
        loc = DOMAIN + quote(url, safe="/")
        if loc not in locs:
            errors.append(f"sitemap missing indexable {loc}")
        indexable += 1
    if indexable != len(locs):
        errors.append(f"sitemap has {len(locs)} URLs and {indexable} indexable pages")
    for loc in locs:
        path = unescape(unquote(urlparse(loc).path))
        if path in ("/", ""):
            rel = Path("index.html")
        elif path.endswith("/"):
            rel = Path(path.strip("/")) / "index.html"
        else:
            rel = Path(path.lstrip("/"))
        page = ROOT / rel
        if not page.is_file():
            errors.append(f"sitemap URL has no file: {loc}")
            continue
        html = page.read_text(encoding="utf-8", errors="ignore")
        if 'name="robots" content="noindex' in html or 'http-equiv="refresh"' in html:
            errors.append(f"sitemap lists a non-indexable page: {loc}")
    coverage = health_run(ROOT)["checks"]["coverage"]
    if not coverage["ok"]:
        errors.append(
            f"health coverage treats redirect stubs as reviews: {coverage['orphan_reviews']}"
        )
    if errors:
        raise SystemExit("\n".join(errors))


def _page_url(rel: Path) -> str:
    if rel.name == "index.html":
        parent = rel.parent.as_posix()
        return "/" if parent == "." else f"/{parent}/"
    return "/" + rel.as_posix()


def _public_forms(loser: str) -> list[str]:
    forms = [loser]
    if loser.endswith("/index.html"):
        forms.append(loser[: -len("index.html")])
    return forms


if __name__ == "__main__":
    main()
