import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
v = json.loads((D / "verified-requests.json").read_text())
prev = json.loads((D / "digest-2026-10-01.json").read_text())
prevset = {o["url"].rstrip("/").split("/journo-request/")[-1]: o.get("_days_old")
           for o in prev["opportunities"]}
print("cached:", len(v), "prev rows:", len(prevset))
print("all live:", all(r.get("live") for r in v.values()))
print("http codes:", sorted({r.get("http") for r in v.values()}))
print("expiry words:", [k for k, r in v.items() if r.get("live") is False])

print("\n--- crossed today (was <=10, now 11) ---")
for k, r in sorted(v.items()):
    d, p = r.get("days_old"), prevset.get(k)
    if d is not None and d == 11 and p is not None and p <= 10:
        print(f"  {p}d -> {d}d  {k}  [{r.get('badge')}]")
print("--- at 10d today (crosses tomorrow) ---")
for k, r in sorted(v.items()):
    if r.get("days_old") == 10:
        print(f"  {k}  [{r.get('badge')}] (was {prevset.get(k)}d)")
print("--- carried rows missing from cache ---")
for k in prevset:
    if k not in v:
        print("  MISSING", k)
print("--- in cache but not carried before (NEW) ---")
for k in sorted(v):
    if k not in prevset:
        print(f"  {v[k].get('days_old')}d NEW {k}")

pairs = json.loads(Path("/Users/georgezikry/aitoolessentials/site/data/monthly_annual_pairs.json").read_text())
print("\npairs:", pairs.get("n"), pairs.get("range_low"), pairs.get("range_high"),
      pairs.get("median"), "built:", pairs.get("built"))
sn = json.loads(Path("/Users/georgezikry/aitoolessentials/site/data/pricing_snapshots.json").read_text())
print("snapshots updated:", sn.get("updated"), "n:", len(sn.get("snapshots", {})))
live = [o for o in v.values() if (o.get("days_old") or 99) <= 10]
cold = [o for o in v.values() if (o.get("days_old") or 0) > 10]
print(f"live(<=10d): {len(live)}  cold(>10d): {len(cold)}")
