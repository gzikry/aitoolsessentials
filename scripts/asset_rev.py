#!/usr/bin/env python3
"""Content-hash query strings for local stylesheets and scripts.

Porkbun caches an unversioned /css/styles.css response for 30 days. A query
string is a different cache key, so the hash has to change when the file
bytes change. The same 12-character SHA-256 prefix already used by the stack
audit and the header search is the version token.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from site_scope import is_public_rel

_HASH_LEN = 12
_ATTR = re.compile(
    r"""(?P<attr>href|src)(?P<eq>\s*=\s*)(?P<q>["'])(?P<url>[^"']+)(?P=q)""",
    re.I,
)
_ASSET_DIRS = frozenset({"css", "js"})


def _versioned_page(rel: Path) -> bool:
    """Public pages, plus the go/ redirect stubs that still load site CSS."""
    if is_public_rel(rel):
        return True
    return bool(rel.parts) and rel.parts[0] == "go"


def content_hash(path: Path, cache: dict[Path, str] | None = None) -> str:
    key = path.resolve()
    if cache is not None and key in cache:
        return cache[key]
    digest = hashlib.sha256(key.read_bytes()).hexdigest()[:_HASH_LEN]
    if cache is not None:
        cache[key] = digest
    return digest


def resolve_local_asset(root: Path, page: Path, url: str) -> Path | None:
    """Return the css or js file a page URL points at, when it is a real local file."""
    if url.startswith(("http://", "https://", "//", "data:", "mailto:", "javascript:")):
        return None
    bare = url.split("#", 1)[0].split("?", 1)[0]
    if not bare or bare.endswith("/"):
        return None
    if bare.startswith("/"):
        candidate = (root / bare.lstrip("/")).resolve()
    else:
        candidate = (page.parent / bare).resolve()
    try:
        rel = candidate.relative_to(root.resolve())
    except ValueError:
        return None
    if not rel.parts or rel.parts[0] not in _ASSET_DIRS:
        return None
    if candidate.suffix not in {".css", ".js"} or not candidate.is_file():
        return None
    return candidate


def versioned_ref(
    root: Path,
    page: Path,
    url: str,
    cache: dict[Path, str] | None = None,
) -> str | None:
    """Same URL spelling with ?v= set to the file hash. None when it is not a local asset."""
    asset = resolve_local_asset(root, page, url)
    if asset is None:
        return None
    fragment = ""
    path = url
    if "#" in path:
        path, frag = path.split("#", 1)
        fragment = "#" + frag
    bare = path.split("?", 1)[0]
    return f"{bare}?v={content_hash(asset, cache)}{fragment}"


_SCRIPT = re.compile(
    r"""<script\b(?=[^>]*\bsrc=(?P<q>["'])(?P<url>[^"']+)(?P=q))[^>]*>\s*</script>""",
    re.I,
)


def _dedupe_local_scripts(html: str, page: Path, root: Path) -> str:
    """Keep the first script tag for each local file. A second stamp must not put it back."""
    seen: set[Path] = set()

    def keep(match: re.Match[str]) -> str:
        asset = resolve_local_asset(root, page, match.group("url"))
        if asset is None:
            return match.group(0)
        if asset in seen:
            return ""
        seen.add(asset)
        return match.group(0)

    return _SCRIPT.sub(keep, html)


def stamp_html(html: str, page: Path, root: Path, cache: dict[Path, str] | None = None) -> str:
    """Rewrite local stylesheet and script URLs to the current file hash."""
    if cache is None:
        cache = {}

    def repl(match: re.Match[str]) -> str:
        url = match.group("url")
        versioned = versioned_ref(root, page, url, cache)
        if versioned is None or versioned == url:
            return match.group(0)
        return f"{match.group('attr')}{match.group('eq')}{match.group('q')}{versioned}{match.group('q')}"

    return _dedupe_local_scripts(_ATTR.sub(repl, html), page, root)


def stamp_tree(root: Path) -> int:
    """Stamp every public HTML page. Returns how many files changed."""
    root = Path(root)
    cache: dict[Path, str] = {}
    changed = 0
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if not _versioned_page(rel):
            continue
        original = path.read_text(errors="ignore")
        stamped = stamp_html(original, path, root, cache)
        if stamped != original:
            path.write_text(stamped)
            changed += 1
    return changed


def asset_link_errors(root: Path, limit: int = 8) -> list[str]:
    """Public pages whose local stylesheet or script URL is not the current hash."""
    root = Path(root)
    cache: dict[Path, str] = {}
    misses: list[str] = []
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if not _versioned_page(rel):
            continue
        html = path.read_text(errors="ignore")
        for match in _ATTR.finditer(html):
            url = match.group("url")
            asset = resolve_local_asset(root, path, url)
            if asset is None:
                continue
            expected = versioned_ref(root, path, url, cache)
            if expected != url:
                kind = "stylesheet" if asset.suffix == ".css" else "script"
                misses.append(f"{rel}: {kind} {url} should be {expected}")
    if len(misses) > limit:
        extra = len(misses) - limit
        return misses[:limit] + [f"{extra} more local stylesheet or script links are not on the current content hash"]
    return misses
