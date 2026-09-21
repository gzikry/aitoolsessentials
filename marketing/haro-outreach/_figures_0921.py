#!/usr/bin/env python3
"""Recompute every figure the outgoing drafts cite, against the data files as they stand today.

Run before writing any draft. The 2026-09-15 pitch went out citing a count that had drifted and the
2026-09-18 one cited two wrong claims; both were published to a recipient. data/pricing_snapshots.json
carries `updated: 2026-09-21`, so the numbers the 2026-09-20 drafts were built on must be re-derived
rather than carried.
"""
import json
import re
import statistics
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
tools = json.loads((S / "data" / "tools.json").read_text())
ps = json.loads((S / "data" / "pricing_snapshots.json").read_text())
snaps = ps["snapshots"]
srcs = json.loads((S / "data" / "tool_sources.json").read_text())
ts = {t["slug"]: t for t in srcs["tools"]}

print(f"pricing_snapshots updated : {ps.get('updated')}")
print(f"tools.json records        : {len(tools)}")
print(f"snapshot records          : {len(snaps)}")
dates = sorted({v.get("date") for v in snaps.values()})
print(f"snapshot dates in file    : {dates}")

MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid = {}
for k, v in snaps.items():
    vals = [float(x) for x in MONTH.findall(" ".join((v.get("digest") or "").split())) if float(x) > 0]
    if vals:
        paid[k] = (min(vals), v.get("date"))
print(f"\n1. tools with a non-zero monthly price : {len(paid)}")
print(f"   of those at or under $25            : {sum(1 for v in paid.values() if v[0] <= 25)}")
print(f"   median cheapest paid tier           : ${round(statistics.median(v[0] for v in paid.values()), 2)}")
low = min(paid.items(), key=lambda kv: kv[1][0])
print(f"   lowest                              : {low[0]} ${low[1][0]} (date {low[1][1]})")

PAIR = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(user|seat|member|person)?\s*/?\s*month[^.;$]{0,60}?"
                  r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(user|seat|member|person)?\s*/?\s*month\s*(?:billed\s+)?annual", re.I)
ratios = []
for k, v in snaps.items():
    d = " ".join((v.get("digest") or "").split())
    for m in PAIR.finditer(d):
        mo, an = float(m.group(1)), float(m.group(3))
        if an > 0 and mo > an and (m.group(2) or "") == (m.group(4) or ""):
            ratios.append((mo / an, k, mo, an, v.get("date")))
ratios.sort()
print(f"\n2. same-tier monthly/annual pairs       : {len(ratios)}")
for r in ratios:
    print(f"   {r[0]:.2f}x  {r[1]:<18} ${r[2]:g} vs ${r[3]:g} annual  ({r[4]})")
if ratios:
    print(f"   range: {ratios[0][0]:.2f}x ({ratios[0][1]}) to {ratios[-1][0]:.2f}x ({ratios[-1][1]})")
    print(f"   pair dates: {sorted({r[4] for r in ratios})}")

print("\n3. Claude / Anthropic tiers (draft 2)")
c_s = snaps.get("claude", {})
c_t = ts.get("claude", {})
print(f"   snapshot date {c_s.get('date')} / tool_sources checked {c_t.get('pricing_checked_date')}")
summ = " ".join((c_t.get("pricing_summary") or "").split())
for needle in ("$17 per month", "$200 annual prepayment", "$20 month-to-month",
               "Max starts at $100 per month", "Standard seats at $20 per seat per month",
               "Premium seats at $100 per seat per month"):
    print(f"   {'OK ' if needle in summ else 'MISS'}  {needle}")
print(f"   snapshot digest carries Premium seats: {'yes' if 'Premium seats' in (c_s.get('digest') or '') else 'no'}")

print("\n4. monthly/annual claims in the Claude source summary")
print("   ", [s for s in re.findall(r"[^.]*annual[^.]*", summ)][:3])
