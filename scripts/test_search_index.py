#!/usr/bin/env python3
"""Guard the site search index against the failure that hid it for six weeks.

`data/search_index.json` had no generator and no test, so it was last built 2026-09-03 and had
drifted to 74 tools and 438 entries against a 78-tool, 748-page site. Nothing failed, because
nothing watched it — search just quietly returned a subset of the site, which reads to a visitor
as "this site does not have that".

These assertions make that specific regression loud:
  1. every catalog tool has an entry (the drift that actually happened)
  2. coverage of public pages stays above a floor (catches a partial or truncated build)
  3. every indexed URL resolves to a file that exists (catches dead links in results)
  4. no duplicate URLs, and the site-name suffix is stripped from result titles
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from site_scope import is_public_rel  # noqa: E402

INDEX = ROOT / "data" / "search_index.json"
# Floor, not a target: the index must not silently shed most of the site. Current coverage is
# ~100% of public HTML; 0.85 leaves room for deliberate exclusions without allowing a stub.
MIN_COVERAGE = 0.85
SITE_NAME = "AIToolsEssentials"


def main() -> None:
    errors: list[str] = []

    if not INDEX.exists():
        raise SystemExit("search index missing: data/search_index.json")
    try:
        payload = json.loads(INDEX.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"search index is not valid JSON: {exc}")

    entries = payload.get("entries") if isinstance(payload, dict) else payload
    if not isinstance(entries, list) or not entries:
        raise SystemExit("search index has no entries")

    # 1. Every catalog tool is findable. This is the drift that actually occurred.
    tools = json.loads((ROOT / "data" / "tools.json").read_text())
    indexed_tool_slugs = {e.get("slug") for e in entries if e.get("type") == "tool"}
    for tool in tools:
        if tool["slug"] not in indexed_tool_slugs:
            errors.append(f"catalog tool not searchable: {tool['slug']}")
    extra = {s for s in indexed_tool_slugs if s} - {t["slug"] for t in tools}
    if extra:
        errors.append(f"index claims tools that are not in the catalog: {sorted(extra)[:5]}")

    # 2. Coverage floor over public pages.
    public_pages = [
        p for p in ROOT.rglob("*.html")
        if is_public_rel(p.relative_to(ROOT))
        and not any(part in p.parts for part in ("go",))
    ]
    coverage = len(entries) / max(1, len(public_pages))
    if coverage < MIN_COVERAGE:
        errors.append(
            f"search index covers {len(entries)} of {len(public_pages)} public pages "
            f"({coverage:.0%}) — below the {MIN_COVERAGE:.0%} floor; the index looks stale or partial"
        )

    # 3. Every indexed URL resolves to a real file. A result that 404s is worse than no result.
    seen: set[str] = set()
    for e in entries:
        url = e.get("url") or ""
        if not url:
            errors.append(f"entry without a url: {e.get('name')!r}")
            continue
        if url in seen:
            errors.append(f"duplicate url in index: {url}")
        seen.add(url)
        rel = url.strip("/")
        if not rel:
            continue
        candidates = [ROOT / rel] if rel.endswith(".html") else [ROOT / rel / "index.html", ROOT / rel]
        if not any(c.exists() for c in candidates):
            errors.append(f"indexed url has no file: {url}")

    # 4. Titles are display-ready: the site name is stripped from the result name.
    for e in entries:
        name = e.get("name") or ""
        if name.endswith(f"| {SITE_NAME}") or name.endswith(f"— {SITE_NAME}"):
            errors.append(f"result title still carries the site name: {name[:70]!r}")

    if errors:
        raise SystemExit("search index guard failures:\n- " + "\n- ".join(errors[:25]))

    print(
        f"search index ok: {len(entries)} entries "
        f"({len(indexed_tool_slugs)} tools, {coverage:.0%} of {len(public_pages)} public pages)"
    )


if __name__ == "__main__":
    main()
