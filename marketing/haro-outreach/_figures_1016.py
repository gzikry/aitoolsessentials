"""Recompute every figure today's drafts will cite, from our own data files (2026-10-08 run)."""
import json
import re
import statistics
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
tools = json.loads((S / "data/tools.json").read_text())
snapf = json.loads((S / "data/pricing_snapshots.json").read_text())
snaps = snapf["snapshots"]

print("pricing_snapshots.updated:", snapf.get("updated"))
print("tools.json entries:", len(tools), "| snapshots:", len(snaps))

MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid = {}
for k, v in snaps.items():
    d = " ".join((v.get("digest") or "").split())
    vals = [float(x) for x in MONTH.findall(d) if float(x) > 0]
    if vals:
        paid[k] = (min(vals), v.get("date"))
print(f"\ntools quoting a non-zero monthly price: {len(paid)} of {len(snaps)}")
print(f"    cheapest paid monthly tier <= $25: {sum(1 for v in paid.values() if v[0] <= 25)}")
print(f"    median cheapest paid monthly tier: ${statistics.median(v[0] for v in paid.values()):.2f}")
lo = min(v[0] for v in paid.values())
print(f"    min ${lo:.2f} ({[k for k, v in paid.items() if v[0] == lo]})")

pairs = json.loads((S / "data/monthly_annual_pairs.json").read_text())
print(f"\nmonthly/annual pairs: n={pairs.get('n')} range {pairs.get('range_low')}x to "
      f"{pairs.get('range_high')}x median {pairs.get('median')}x  built {pairs.get('built')}")

# the two sentences a draft may stand behind today
print("\nA)", f"We track {len(snaps)} AI tools; {len(paid)} publish a monthly price, "
      f"{sum(1 for v in paid.values() if v[0] <= 25)} at or under $25/month, median "
      f"${statistics.median(v[0] for v in paid.values()):.2f} (snapshots re-checked {snapf.get('updated')}).")
print("B)", f"Across {pairs.get('n')} tiers quoting both monthly and annual-billed monthly, the monthly "
      f"payer pays {pairs.get('range_low')}x to {pairs.get('range_high')}x more, median {pairs.get('median')}x.")
