"""Recompute every figure today's drafts will cite, from our own data files (2026-10-07 run)."""
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

cats = {}
for t in tools:
    cats[t["category"]] = cats.get(t["category"], 0) + 1
three_plus = {k: v for k, v in cats.items() if v >= 3}
print(f"\n[1] categories: {len(cats)} | holding >=3: {len(three_plus)} | tools in them: {sum(three_plus.values())}")

MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid = {}
for k, v in snaps.items():
    d = " ".join((v.get("digest") or "").split())
    vals = [float(x) for x in MONTH.findall(d) if float(x) > 0]
    if vals:
        paid[k] = (min(vals), v.get("date"))
print(f"\n[2] tools quoting a non-zero monthly price: {len(paid)} of {len(snaps)}")
print(f"    cheapest paid monthly tier <= $25: {sum(1 for v in paid.values() if v[0] <= 25)}")
print(f"    median cheapest paid monthly tier: ${statistics.median(v[0] for v in paid.values()):.2f}")
lo = min(v[0] for v in paid.values())
print(f"    min ${lo:.2f} ({[k for k, v in paid.items() if v[0] == lo]})")
print(f"    max ${max(v[0] for v in paid.values()):.2f}")

both = [k for k, v in snaps.items()
        if re.search(r"(monthly|/month|month-to-month)", v.get("digest", ""), re.I)
        and re.search(r"(annual|/year|yearly)", v.get("digest", ""), re.I)]
print(f"\n[3] tools quoting BOTH a monthly and an annual rate: {len(both)} of {len(snaps)}")

pairs = json.loads((S / "data/monthly_annual_pairs.json").read_text())
print(f"\n[4] monthly/annual pairs: n={pairs.get('n')} range {pairs.get('range_low')}x to "
      f"{pairs.get('range_high')}x median {pairs.get('median')}x")
print(f"    built: {pairs.get('built')}  source: {pairs.get('source')}")
ts = sorted({p.get("slug") for p in (pairs.get("pairs") or []) if p.get("slug")})
print(f"    distinct tools: {len(ts)}")

print("\n[5] the two sentences a draft may stand behind today")
print(f'    A) "We track {len(snaps)} AI tools and their published list prices; {len(paid)} of them '
      f'publish a monthly price, {sum(1 for v in paid.values() if v[0] <= 25)} of those at or under '
      f'$25/month, median ${statistics.median(v[0] for v in paid.values()):.2f} '
      f'(snapshots re-checked {snapf.get("updated")})."')
print(f'    B) "Across {pairs.get("n")} tiers where the same tier quotes both a monthly price and an '
      f'annual-billed monthly price, the monthly payer always pays more: {pairs.get("range_low")}x to '
      f'{pairs.get("range_high")}x, median {pairs.get("median")}x."')
