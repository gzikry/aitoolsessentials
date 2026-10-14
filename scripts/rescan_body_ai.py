#!/usr/bin/env python3
"""Re-scan already-fetched request bodies for prose-level AI tokens.

Why this exists: the body-level AI scan in `marketing/haro-outreach/_bodies_*.py` used
`sourcee_terms.AI`, which is written for slugs and requires a hyphen on each side of a token.
In prose there are no hyphens, so the scan reported ZERO AI hits on windows whose bodies plainly
say "AI" — a false zero, and one the digests recorded as an unfixed limitation for several runs
rather than citing the regex as evidence.

The bodies are already on disk, so the fix costs no network calls: this script re-reads a stored
`_bodies_*.json` (default: the newest one), matches every stored `core` with `AI_PROSE`, and
prints both the AI hits and the AI+spend rows that the slug filter could not have found.

Usage:
    python3 scripts/rescan_body_ai.py                 # newest bodies file
    python3 scripts/rescan_body_ai.py 1014            # a specific one (MMDD)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
OUT = SITE_ROOT / "marketing" / "haro-outreach"
sys.path.insert(0, str(SITE_ROOT / "scripts"))
from sourcee_terms import AI_PROSE, REAL_SPEND, prose_ai  # noqa: E402


def newest() -> Path:
    return max(OUT.glob("_bodies_*.json"), key=lambda p: p.stat().st_mtime)


def main() -> None:
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        path = OUT / f"_bodies_{sys.argv[1]}.json"
    else:
        path = newest()
    bodies = json.loads(path.read_text())

    ai_rows, ai_spend_rows = [], []
    for slug, rec in bodies.items():
        toks = prose_ai(rec.get("core") or "")
        if not toks:
            continue
        ai_rows.append((slug, toks))
        if REAL_SPEND.search(rec.get("core") or ""):
            ai_spend_rows.append((slug, toks))

    print(f"{path.name}: {len(bodies)} bodies re-scanned with AI_PROSE")
    print(f"body-level AI hits: {len(ai_rows)}  (the old slug-tuned AI regex reported 0)")
    for slug, toks in sorted(ai_rows):
        print(f"   {slug}  tokens={toks[:8]}")
    print(f"body-level AI + REAL_SPEND: {len(ai_spend_rows)}")
    for slug, toks in sorted(ai_spend_rows):
        print(f"   {slug}  tokens={toks[:8]}")

    # A sanity check on the matcher itself: prose that must not match, and prose that must.
    assert not AI_PROSE.search("The rain in Spain stays mainly in the plain."), "false positive on prose"
    assert AI_PROSE.search("we use AI at work"), "missed plain 'AI'"
    assert AI_PROSE.search("Claude and Gemini seat costs"), "missed vendor names"
    print("matcher self-check: 3/3 assertions passed")


if __name__ == "__main__":
    main()
