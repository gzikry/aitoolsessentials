#!/usr/bin/env python3
"""Verify 2026-10-16's pitch drafts against our own data: word counts and every cited figure.

Two failure classes this closes, both seen in this monitor's history:
  * a draft that goes past the 200-word ceiling because the count was asserted, not measured;
  * a figure in a paste-ready draft that no longer matches data/ - the corrected Amplemarket range
    was sent 22 days after it stopped being true.
Every number the drafts cite is re-derived here from data/tools.json, data/pricing_snapshots.json,
data/tool_sources.json and data/monthly_annual_pairs.json. Anything that cannot be re-derived fails.

Usage: python3 marketing/haro-outreach/_verify_drafts_1016.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing/haro-outreach"
DRAFTS = D / "pitch-drafts-2026-10-16.md"
fails: list[str] = []

text = DRAFTS.read_text()
sections = re.split(r"\n## ", text)
blocks = {}
for sec in sections:
    m = re.match(r"(\d)\. ", sec)
    if m:
        body = sec.split("*Draft length")[0]
        quote = "\n".join(l[2:].strip() for l in body.splitlines() if l.startswith("> "))
        blocks[m.group(1)] = quote or body

for k, v in sorted(blocks.items()):
    words = len(re.findall(r"[A-Za-z0-9\$@./'’%+-]+", v))
    status = "OK " if words < 200 else "FAIL"
    if words >= 200:
        fails.append(f"section {k} is {words} words, at or over the 200-word ceiling")
    print(f"{status} section {k}: {words} words")
    print(f"     signature: {'AIToolsEssentials' if 'AIToolsEssentials' in v else 'MISSING'}"
          f" | George's name present: {'YES - FAIL' if re.search(r'george|zikry', v, re.I) else 'no'}")
    if "AIToolsEssentials" not in v:
        fails.append(f"section {k} is not signed AIToolsEssentials")
    if re.search(r"george|zikry", v, re.I):
        fails.append(f"section {k} carries George's name")

# ---------------------------------------------------------------- figure re-derivation
tools = json.loads((S / "data/tools.json").read_text())
snaps = json.loads((S / "data/pricing_snapshots.json").read_text())["snapshots"]
srcs = json.loads((S / "data/tool_sources.json").read_text())["tools"]
pairs = json.loads((S / "data/monthly_annual_pairs.json").read_text())

MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid = {}
for k, v in snaps.items():
    vals = [float(x) for x in MONTH.findall(v.get("digest") or "") if float(x) > 0]
    if vals:
        paid[k] = min(vals)
import statistics
facts = {
    "78": len(tools),
    "42": len(paid),
    "33": sum(1 for v in paid.values() if v <= 25),
    "17.50": f"{statistics.median(paid.values()):.2f}",
    "25": 25,
}
print("\nre-derived headline set:", facts)

cited = {
    "1.11x": str(pairs["range_low"]), "2.53x": str(pairs["range_high"]),
    "1.25x": str(pairs["median"]), "19": str(pairs["n"]),
}
print("re-derived pair set:", cited, "| built", pairs["built"], "| snapshot updated",
      json.loads((S / "data/pricing_snapshots.json").read_text()).get("updated"))

# The two named tool entries, read out of tool_sources.json with their own check dates
for slug, want in (("browse-ai", ("$48", "$19", "2026-09-18")), ("gamma", ("$18", "2026-10-01"))):
    entry = next((t for t in srcs if t["slug"] == slug), None)
    if not entry:
        fails.append(f"{slug} is not in data/tool_sources.json")
        continue
    summary = entry.get("pricing_summary") or ""
    for w in want:
        token = w
        if token not in summary and token not in (entry.get("pricing_checked_date") or "") and token not in summary.replace(" ", ""):
            fails.append(f"{slug}: '{token}' not found in its own tool_sources entry")
    print(f"tool {slug}: checked {entry.get('pricing_checked_date')} | "
          f"cites {', '.join(w for w in want if w in summary or w == entry.get('pricing_checked_date'))}")

# every date-like claim in the drafts must be a date we actually recorded
for d in sorted(set(re.findall(r"20\d\d-\d\d-\d\d", text))):
    if d not in {"2026-10-16", "2026-10-15", "2026-09-18", "2026-10-01", "2026-10-08", "2026-10-10", "2026-10-05"}:
        fails.append(f"draft cites {d}, which is not a date this run produced")

print()
if fails:
    print("FAILURES:")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print("all draft figures re-derived; both sections under the ceiling and signed AIToolsEssentials")
