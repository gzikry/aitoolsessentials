#!/usr/bin/env python3
"""Measure the word count of each paste-ready draft in a pitch-drafts file.

The drafts carry a claimed word count in italics ("176 words including the signature — measured on
this file"). Before this script that number was produced by a one-off command per run, so a draft
could be edited and the claim left standing. This extracts each `> ` blockquote, strips the marker,
counts whitespace-separated tokens, and prints both the measurement and the claim found in the file.

Usage:
    python3 scripts/verify_drafts.py marketing/haro-outreach/pitch-drafts-2026-10-18.md
Exit code is 1 when a draft exceeds 200 words or a claimed count differs from the measured one.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LIMIT = 200


def main() -> int:
    path = Path(sys.argv[1])
    text = path.read_text()
    blocks, cur = [], []
    for line in text.splitlines():
        if line.startswith(">"):
            cur.append(re.sub(r"^>\s?", "", line))
        elif cur:
            blocks.append("\n".join(cur).strip())
            cur = []
    if cur:
        blocks.append("\n".join(cur).strip())

    claims = [int(m) for m in re.findall(r"(\d+) words including the signature", text)]
    rc = 0
    for i, b in enumerate(blocks, 1):
        words = len(b.split())
        claim = claims[i - 1] if i - 1 < len(claims) else None
        status = "OK" if words <= LIMIT else f"OVER {LIMIT}"
        match = "" if claim is None else (" claim matches" if claim == words else f" CLAIM {claim} != {words}")
        if words > LIMIT or (claim is not None and claim != words):
            rc = 1
        print(f"draft {i}: {words} words — {status}{match}")
        if "AIToolsEssentials" not in b:
            print(f"draft {i}: MISSING AIToolsEssentials signature")
            rc = 1
        if re.search(r"\bGeorge\b", b):
            print(f"draft {i}: CONTAINS 'George' — outbound mail is signed AIToolsEssentials only")
            rc = 1
    print(f"{len(blocks)} draft(s) in {path.name}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
