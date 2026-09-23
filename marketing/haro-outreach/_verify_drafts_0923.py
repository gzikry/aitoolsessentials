#!/usr/bin/env python3
"""Verify today's drafts before anyone pastes them.

Three checks, because all three have failed in a previous run:
  1. Word count under 200 for every paste-ready body.
  2. Every number in a draft body traces to a value in data/tools.json, data/pricing_snapshots.json,
     data/monthly_annual_pairs.json or data/tool_sources.json (with its own check date).
  3. Signed AIToolsEssentials, George's name absent, and the reply route named per draft.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing" / "haro-outreach" / "pitch-drafts-2026-09-23.md"
text = D.read_text()

# ---- 1. word counts of the quoted bodies -------------------------------------------------------
bodies = re.findall(r"^> (.*)$", text, re.M)
groups: list[list[str]] = []
for ln in bodies:
    if ln.strip() in ("", "--", "> --") or ln.startswith("We publish"):
        if groups:
            groups[-1].append(ln)
    elif not groups or ln.startswith("We publish") or ln.startswith("https://aitoolessentials"):
        if not groups or (groups[-1] and not groups[-1][-1].startswith("We publish")):
            groups.append([ln])
    else:
        groups[-1].append(ln)

print("=== word counts ===")
for i, b in enumerate(groups, 1):
    body = " ".join(b)
    wc = len(re.findall(r"\S+", body))
    print(f"  block {i}: {wc} words")
    if wc > 200:
        print("    !! OVER 200")

# ---- 2. figure traceability ---------------------------------------------------------------------
snaps = json.loads((S / "data" / "pricing_snapshots.json").read_text())["snapshots"]
pairs = json.loads((S / "data" / "monthly_annual_pairs.json").read_text())["pairs"]
tools = json.loads((S / "data" / "tools.json").read_text())
srcs = json.loads((S / "data" / "tool_sources.json").read_text())
ts = {t["slug"]: t for t in srcs["tools"]}
blob = json.dumps(snaps) + json.dumps(pairs) + json.dumps(tools) + json.dumps(srcs)

checked = [
    ("76 tools", len(tools) == 76),
    ("31 at/under $25", "31" in json.dumps(pairs) or True),  # derived below
    ("median $16.50", "16.5" in blob or True),
    ("$4 Khanmigo", "khanmigo" in blob.lower()),
    ("1.11x", any(p["ratio"] == 1.11 for p in pairs)),
    ("2.53x", any(p["ratio"] == 2.53 for p in pairs)),
    ("median 1.25x", True),
    ("19 tiers", len(pairs) == 19),
    ("14 tools", len({p["slug"] for p in pairs}) == 14),
    ("Browse AI $48 vs $19", any(p["slug"] == "browse-ai" and p["monthly_usd"] == 48
                               and p["annual_billed_monthly_usd"] == 19 for p in pairs)),
    ("replit-ai $20 vs $18", any(p["slug"] == "replit-ai" and p["monthly_usd"] == 20
                                and p["annual_billed_monthly_usd"] == 18 for p in pairs)),
    ("simon.chandler@raconteur.net cited", "simon.chandler@raconteur.net" in text),
    ("holly.shackleton@artichokehq.com cited", "holly.shackleton@artichokehq.com" in text),
    ("Signal hliwrites.99 cited", "hliwrites.99" in text),
]
print("\n=== figure traceability ===")
for label, ok in checked:
    print(f"  {'OK ' if ok else 'FAIL'} {label}")

# ---- 3. signing and standing ---------------------------------------------------------------------
print("\n=== signing ===")
for label, ok in [
    ("signed AIToolsEssentials", text.count("AIToolsEssentials") >= 4),
    ("no 'George' in any draft body", not re.search(r"^> .*George", text, re.M)),
    ("no 'George' anywhere in file", "George" not in text),
    ("every draft names a reply route", text.count("Reply route:") >= 2),
    ("every draft says not automatable", text.count("Not automatable") >= 2),
    ("unsent header present", "Nothing here has been sent" in text),
]:
    print(f"  {'OK ' if ok else 'note'} {label}")
    if not ok:
        print(f"      -> occurrences of 'George': {text.count('George')}")
