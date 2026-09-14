#!/usr/bin/env python3
"""Second-pass sweep for cost/spend tokens the primary filter may have missed."""
import json, re

BASE = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/"
data = json.load(open(BASE + "_scan2.json"))

EXTRA = ["cfo", "finance", "financial", "billing", "invoice", "license", "licence",
         "seat", "procure", "procurement", "vendor", "saving", "efficien", "waste",
         "audit", "sprawl", "tooling", "platform", "license", "renew", "churn",
         "retention", "budget", "spend", "cost", "price", "subscription"]

seen, rows = set(), []
for entry in data["broad"]:
    url, lm = entry["url"], entry["lastmod"]
    slug = url.rstrip("/").split("/journo-request/")[-1]
    if slug in seen:
        continue
    seen.add(slug)
    parts = set(slug.split("-"))
    hits = sorted(p for p in EXTRA if p in parts)
    if hits:
        rows.append({"slug": slug, "lastmod": lm, "kw": hits})

rows.sort(key=lambda r: r["lastmod"], reverse=True)
print(f"SECOND-PASS cost/spend token matches since {data['cutoff']}: {len(rows)}")
for r in rows:
    print(f"[{r['lastmod'][:16]}] {r['slug'][:95]} | {','.join(r['kw'])}")

# also show any slug mentioning AI AND any spend token in the whole sitemap-recent set
print("\n--- AI + spend co-occurrence (any position) ---")
for r in rows:
    s = r["slug"]
    if re.search(r"(^|-)ai(-|$)", s) or "artificial-intelligence" in s:
        print(f"[{r['lastmod'][:16]}] {s} | {','.join(r['kw'])}")
