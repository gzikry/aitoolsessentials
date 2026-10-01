import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
v = json.loads((D / "verified-requests.json").read_text())
prev = json.loads((D / "digest-2026-09-30.json").read_text())
prevset = {o["url"].rstrip("/").split("/journo-request/")[-1]: o.get("_days_old")
           for o in prev["opportunities"]}
print("cached:", len(v))
rows = sorted(((r.get("days_old"), k, r.get("live"), r.get("http"), r.get("badge"))
               for k, r in v.items()), key=lambda x: (x[0] is None, x[0]))
for a, k, l, h, b in rows:
    print(f"{a:>4}d live={l} {h} {b} {k[:60]}")

print("\n--- crossed today (was <=10, now 11) ---")
for k, r in v.items():
    d, p = r.get("days_old"), prevset.get(k)
    if d is not None and d == 11 and p is not None and p <= 10:
        print(f"  {p}d -> {d}d  {k}")
print("--- at 10d today (crosses tomorrow) ---")
for k, r in v.items():
    if r.get("days_old") == 10:
        print(f"  {k}")
print("--- carried rows missing from cache ---")
for k in prevset:
    if k not in v:
        print("  MISSING", k)
print("--- in cache but not carried before (NEW) ---")
for k in v:
    if k not in prevset:
        print("  NEW", k)

pairs = json.loads(Path("/Users/georgezikry/aitoolessentials/site/data/monthly_annual_pairs.json").read_text())
print("\npairs keys:", list(pairs.keys()))
print("n:", pairs.get("n"), "range:", pairs.get("range_low"), pairs.get("range_high"),
      "median:", pairs.get("median"), "built:", pairs.get("built"))
