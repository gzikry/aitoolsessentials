#!/usr/bin/env python3
"""Measure the paste-ready body of each draft in pitch-drafts-2026-10-07.md (subject + body + sig)."""
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
txt = (D / "pitch-drafts-2026-10-07.md").read_text()

# blocks are the lines starting with "> "
blocks = []
cur = []
for line in txt.splitlines():
    if line.startswith(">"):
        cur.append(line.lstrip("> ").rstrip())
    else:
        if cur:
            blocks.append("\n".join(cur))
            cur = []
if cur:
    blocks.append("\n".join(cur))

for i, b in enumerate(blocks, 1):
    words = len(re.findall(r"\S+", b))
    print(f"draft {i}: {words} words  (lines {b.count(chr(10)) + 1})  first line: {b.splitlines()[0][:60]}")
