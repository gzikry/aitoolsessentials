#!/usr/bin/env python3
"""Recompute every figure today's drafts cite, against data files as they stand 2026-09-23.

pricing_snapshots.json carries `updated: 2026-09-23`, so nothing the 2026-09-22 drafts cite can be
carried on trust. Same discipline as _figures_0921.py, narrowed to the claims the two live drafts make.
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
print(f"snapshot dates in file    : {sorted({v.get('date') for v in snaps.values()})}")

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

pairs = json.loads((S / "data" / "monthly_annual_pairs.json").read_text())
pr = [p["ratio"] for p in pairs["pairs"]]
print(f"\n2. pairs file built {pairs['built']}: n={len(pr)} tiers across "
      f"{len({p['slug'] for p in pairs['pairs']})} tools, "
      f"{min(pr):.2f}x to {max(pr):.2f}x, median {statistics.median(pr):.2f}x")
print(f"   widest : {max(pairs['pairs'], key=lambda x: x['ratio'])['slug']} "
      f"${max(pairs['pairs'], key=lambda x: x['ratio'])['monthly_usd']:g} vs "
      f"${max(pairs['pairs'], key=lambda x: x['ratio'])['annual_billed_monthly_usd']:g}")
print(f"   pair dates: {sorted({p['snapshot_date'] for p in pairs['pairs']})}")

print("\n3. Claude / Anthropic tiers (draft 2 figure, now cold — recorded not drafted)")
c_s, c_t = snaps.get("claude", {}), ts.get("claude", {})
print(f"   snapshot date {c_s.get('date')} / tool_sources checked {c_t.get('pricing_checked_date')}")
summ = " ".join((c_t.get("pricing_summary") or "").split())
for needle in ("$17", "$20", "$100", "$200", "Premium"):
    print(f"   tool_sources contains {needle!r}: {needle in summ}")
print(f"   snapshot digest contains 'Premium': {'Premium' in (c_s.get('digest') or '')}")
