"""Recompute every figure today's drafts will cite, from our own data files.

Nothing is trusted from an earlier draft: the Amplemarket send used a count (60) that had drifted
to 70, and two opacity claims were flatly wrong. Every number below is recomputed against
data/tools.json, data/pricing_snapshots.json and data/tool_sources.json as they stand today.
"""
import json
import re
import statistics
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
tools = json.loads((S / "data/tools.json").read_text())
snapf = json.loads((S / "data/pricing_snapshots.json").read_text())
snaps = snapf["snapshots"]
srcs = json.loads((S / "data/tool_sources.json").read_text())

print("pricing_snapshots.updated:", snapf.get("updated"))
print("tools:", len(tools), "snapshots:", len(snaps))

cats = {}
for t in tools:
    cats[t["category"]] = cats.get(t["category"], 0) + 1
three_plus = {k: v for k, v in cats.items() if v >= 3}
print("\n[1] categories:", len(cats), "| holding >=3:", len(three_plus),
      "| tools in them:", sum(three_plus.values()))

MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid = {}
for k, v in snaps.items():
    d = " ".join((v.get("digest") or "").split())
    vals = [float(x) for x in MONTH.findall(d) if float(x) > 0]
    if vals:
        paid[k] = (min(vals), v.get("date"))
print(f"\n[2] tools quoting a non-zero monthly price: {len(paid)} of {len(tools)}")
print(f"    cheapest paid monthly tier <= $25: {sum(1 for v in paid.values() if v[0] <= 25)}")
print(f"    median cheapest paid monthly tier: ${statistics.median(v[0] for v in paid.values()):.2f}")
print(f"    min ${min(v[0] for v in paid.values()):.2f} "
      f"({[k for k, v in paid.items() if v[0] == min(x[0] for x in paid.values())]})")
low = sorted((v[0], k, v[1]) for k, v in paid.items() if v[0] <= 25)
print("    sub-$25 set:", [(f"${a:.2f}", b, c) for a, b, c in low])

both = [k for k, v in snaps.items()
        if re.search(r"(monthly|/month|month-to-month)", v.get("digest", ""), re.I)
        and re.search(r"(annual|/year|yearly)", v.get("digest", ""), re.I)]
print(f"\n[3] tools quoting BOTH a monthly and an annual rate: {len(both)} of {len(tools)}")

NOPRICE = re.compile(r"(does not publish a self-serve|did not publish a self-serve|"
                     r"No official USD seat price is reported|No official USD seat or credit price is reported|"
                     r"No official paid consumer|no public pricing page|do not publish)", re.I)
nop = sorted((k, v.get("date")) for k, v in snaps.items()
             if NOPRICE.search(v.get("digest", "")) and "free and unlimited" not in v.get("digest", ""))
print(f"\n[5] tools publishing no paid-tier price: {len(nop)}")
for k, d in nop:
    print(f"    {k:<22} checked {d}")

print("\n[6] shadow-AI draft figures re-checked")
print(f"    tools tracked: {len(tools)}")
print(f"    priced tools: {len(paid)}; of those <= $25/mo: {sum(1 for v in paid.values() if v[0] <= 25)}; "
      f"median ${statistics.median(v[0] for v in paid.values()):.2f}; "
      f"lowest ${min(v[0] for v in paid.values()):.2f} "
      f"({[k for k, v in paid.items() if v[0] == min(x[0] for x in paid.values())]})")
pairs = json.loads((S / "data/monthly_annual_pairs.json").read_text())
print("    monthly/annual pairs file keys:", list(pairs)[:8])
