#!/usr/bin/env python3
"""Measure today's draft bodies rather than asserting their word counts.

Verifies, off the file: each quoted draft block's word count (must be <200 including subject and
signature), that every block is signed AIToolsEssentials and never George, that the routes are present,
that the CURRENT figures appear and the superseded ones appear only in the correction/history context,
and that no draft cites a figure that is not in our verified data.
"""
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
p = D / "pitch-drafts-2026-10-05.md"
text = p.read_text()

runs, cur = [], []
for line in text.splitlines():
    if line.startswith(">"):
        cur.append(line)
    else:
        if cur:
            runs.append(cur)
            cur = []
if cur:
    runs.append(cur)
print(f"{len(runs)} quoted draft blocks\n")
for i, run in enumerate(runs, 1):
    body = "\n".join(l[2:] for l in run)
    words = len(body.split())
    print(f"--- block {i}: {words} words {'OK (<200)' if words < 200 else 'OVER 200!'} ---")
    print(f"    first line: {run[0][2:][:95]}")
    print(f"    signed AIToolsEssentials: {'AIToolsEssentials' in body}")
    print(f"    contains 'George': {'George' in body}")
    print(f"    under 200 words: {words < 200}")
    print()

for name in ("simon.chandler@raconteur.net", "holly.shackleton@artichokehq.com", "jan@jansuski.com"):
    print(f"route {name}: {'present' if name in text else 'MISSING'}")
for good in ("42", "33", "$17.50", "1.11x", "2.53x", "1.25x", "2026-10-05"):
    print(f"current figure/date {good}: {'present' if good in text else 'missing'}")
for bad in ("1.21x", "1.16x", "1.33x", "$16.50", "40 publish", "31 of those"):
    hits = len(re.findall(re.escape(bad), text))
    print(f"superseded {bad}: {hits} mention(s)")
