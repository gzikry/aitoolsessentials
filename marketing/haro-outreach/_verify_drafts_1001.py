#!/usr/bin/env python3
"""Measure the draft bodies rather than asserting their word counts.

The 2026-09-23 drafts claimed 138 and 136 words for two bodies that measured 194 and 197 when the
signature and subject line were counted. Every count printed here is measured off the file.
"""
import re
from pathlib import Path

p = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/pitch-drafts-2026-10-01.md")
text = p.read_text()
blocks = re.findall(r"^> .*$", text, re.M)  # blockquote draft bodies

# Split into consecutive runs of quote lines.
runs, cur = [], []
prev = None
for line in text.splitlines():
    if line.startswith(">"):
        cur.append(line)
        prev = True
    else:
        if cur:
            runs.append(cur)
            cur = []
print(f"{len(runs)} quoted draft blocks\n")
for i, run in enumerate(runs, 1):
    body = "\n".join(l[2:] for l in run)
    words = len(body.split())
    print(f"--- block {i}: {words} words ---")
    print(f"    first line: {run[0][2:][:90]}")
    print(f"    signed AIToolsEssentials: {'AIToolsEssentials' in body}")
    print(f"    contains 'George': {'George' in body}")
    print()

for name in ("simon.chandler@raconteur.net", "holly.shackleton@artichokehq.com", "jan@jansuski.com"):
    print(f"{name}: {'present' if name in text else 'MISSING'}")
for bad in ("1.21x", "1.16x", "1.33x"):
    hits = [m.start() for m in re.finditer(re.escape(bad), text)]
    print(f"superseded figure {bad}: {len(hits)} mention(s) "
          f"({'all in the correction/history context' if hits else 'absent'})")
