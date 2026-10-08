#!/usr/bin/env python3
"""Measure the word counts of each draft body in pitch-drafts-2026-10-08.md and flag any figure
that is not in our verified data. Asserts, rather than trusting the prose."""
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
txt = (D / "pitch-drafts-2026-10-08.md").read_text()

blocks = re.split(r"\n---\n", txt)
for i, b in enumerate(blocks):
    if "> Subject:" not in b:
        continue
    # the quoted draft body: lines starting with '>'
    body = "\n".join(l[2:] if l.startswith("> ") else l[1:] if l.startswith(">") else ""
                     for l in b.splitlines() if l.lstrip().startswith(">"))
    body = re.sub(r"^--$", "", body, flags=re.M).strip()
    words = len(re.findall(r"\S+", body))
    subj = re.search(r"> Subject: (.+)", b)
    print(f"§{i}  words={words}  subject={subj.group(1) if subj else '?'}")

# figure sanity: every $ figure cited must appear somewhere in our data files
import json
data = ((D.parent.parent / "data" / "pricing_snapshots.json").read_text()
        + (D.parent.parent / "data" / "tool_sources.json").read_text())
for fig in ("$20", "$100", "$8.40", "$7", "$26.40", "$22", "$19", "$39", "$17.50", "$25", "$4", "$48"):
    print(f"  {fig:<8} in data: {fig in data}")
