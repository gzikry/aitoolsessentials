#!/usr/bin/env python3
"""Assert today's draft file is sendable-clean: word counts, superseded figures, names, signatures.

Measures rather than asserts, in the same spirit as _verify_drafts_1009.py.
"""
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
P = D / "pitch-drafts-2026-10-10.md"
text = P.read_text()
fails = []

# 1. Each pitch body sits between a "> Subject:" line and the trailing "> --" terminator.
bodies = re.findall(r"> Subject:.*?\n>\s*--", text, re.S)
print(f"draft bodies found: {len(bodies)}")
for i, b in enumerate(bodies, 1):
    words = len(re.findall(r"\S+", b.replace(">", " ")))
    flag = "OK " if words < 200 else "OVER"
    print(f"  §{i}: {words} words  {flag}")
    if words >= 200:
        fails.append(f"§{i} is {words} words (>= 200)")

# 2. A pitch must lead with a number/fact, and must not contain superseded figures.
for b in bodies:
    for bad in ("42 of 76", "of 76 tools", "40/31", "$16.50", "1.21x", "1.16x", "median 1.33x"):
        if bad in b:
            fails.append(f"superseded figure present in a draft body: {bad!r}")

# 3. Never George's name, always the brand signature.
for b in bodies:
    for bad in ("George", "Zikry", "georgezikry"):
        if bad in b:
            fails.append(f"personal name present in a draft body: {bad!r}")
for b in bodies:
    if "AIToolsEssentials" not in b:
        fails.append("a draft body is missing the AIToolsEssentials signature")

# 4. The sendable row's route must appear with today's verification.
if "ghansen@epgacceleration.com" not in text:
    fails.append("Glenn Hansen route missing from the draft file")
if "route-checks" in text:
    fails.append("stale probe wording present")

# 5. Every cited seat figure must carry its check date.
for figure, date in (("Claude Team", "2026-09-18"), ("$20/seat/month", "2026-09-18"),
                     ("GitHub Copilot", "2026-10-01"), ("$39 per user/month", "2026-10-01")):
    if figure in text and date not in text:
        fails.append(f"figure {figure!r} cited without its check date {date}")

print()
print("FAILS:" if fails else "all checks passed")
for f in fails:
    print("  -", f)
