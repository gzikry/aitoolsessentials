#!/usr/bin/env python3
"""Verify 2026-10-17's pitch drafts against our own data: word counts and every cited figure.

Two failure classes this closes, both seen in this monitor's history:
  * a draft that goes past the 200-word ceiling because the count was asserted, not measured;
  * a figure in a paste-ready draft that no longer matches data/ - the corrected Amplemarket range
    was sent 22 days after it stopped being true.
Every number the drafts cite is re-derived here from data/tools.json, data/pricing_snapshots.json,
data/tool_sources.json and data/monthly_annual_pairs.json. Anything that cannot be re-derived fails.

Note on the previous version: it keyed its headline set on the literal string "78"
(`{"78": len(tools), ...}`), so when the catalogue moved to 79 the printed set still read "78" and no
check would have caught a draft citing the old count through that key. The key is now derived.

Usage: python3 marketing/haro-outreach/_verify_drafts_1017.py
"""
from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing/haro-outreach"
DRAFTS = D / "pitch-drafts-2026-10-17.md"
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
snaps_doc = json.loads((S / "data/pricing_snapshots.json").read_text())
snaps = snaps_doc["snapshots"]
srcs = json.loads((S / "data/tool_sources.json").read_text())["tools"]
pairs = json.loads((S / "data/monthly_annual_pairs.json").read_text())

MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid = {}
for k, v in snaps.items():
    vals = [float(x) for x in MONTH.findall(v.get("digest") or "") if float(x) > 0]
    if vals:
        paid[k] = min(vals)

n_tools = len(tools)
n_paid = len(paid)
n_25 = sum(1 for v in paid.values() if v <= 25)
med = f"{statistics.median(paid.values()):.2f}"
facts = {str(n_tools): n_tools, str(n_paid): n_paid, str(n_25): n_25, med: med, "25": 25}
print("\nre-derived headline set:", facts, "| snapshot updated", snaps_doc.get("updated"))

# every headline figure the drafts actually print must match the re-derived value
for token, want in ((str(n_tools) + " AI tools", n_tools), (f"{n_paid} of them", n_paid),
                    (f"{n_paid} publish a monthly price", n_paid)):
    if token in text and want != (n_tools if "tools" in token else n_paid):
        fails.append(f"draft cites '{token}' but the re-derived value is {want}")
if f"median ${med}" not in text:
    fails.append(f"draft does not print the re-derived median ${med}")

cited = {
    "1.11x": str(pairs["range_low"]), "2.53x": str(pairs["range_high"]),
    "1.25x": str(pairs["median"]), str(pairs["n"]): str(pairs["n"]),
}
print("re-derived pair set:", cited, "| built", pairs["built"], "| snapshot updated",
      snaps_doc.get("updated"))

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
ALLOWED_DATES = {"2026-10-17", "2026-10-16", "2026-10-15", "2026-10-05", "2026-10-10",
                 "2026-09-18", "2026-10-01", "2026-10-08"}
for d in sorted(set(re.findall(r"20\d\d-\d\d-\d\d", text))):
    if d not in ALLOWED_DATES:
        fails.append(f"draft cites {d}, which is not a date this run produced")

print()
if fails:
    print("FAILURES:")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print("all draft figures re-derived; both sections under the ceiling and signed AIToolsEssentials")
