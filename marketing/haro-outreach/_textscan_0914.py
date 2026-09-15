#!/usr/bin/env python3
"""Text-level spend scan across all fetched AI-token candidate bodies."""
import json, re

OUT = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
res = json.load(open(f"{OUT}/_bodies_0914.json"))

SPEND = ["pricing", "price", "cost", "costs", "subscription", "subscribe", "spend",
         "budget", "credit", "bill", "invoice", "renewal", "renew", "overlap",
         "consolidat", "cancel", "duplicate", "expensive", "afford", "seat",
         "license", "licence", "$", "per month", "/month", "per seat", "roi", "tco"]

rows = []
for slug, r in res.items():
    body = (r.get("description") or "")
    low = body.lower()
    hits = sorted({k for k in SPEND if k in low})
    # require a real spend signal: currency symbol, or >=2 distinct spend words
    strong = ("$" in body) or ("per month" in low) or ("month" in low and "cost" in low) or len(hits) >= 2
    rows.append((len(hits), slug, r.get("datePublished"), hits, strong, body[:200]))

rows.sort(reverse=True)
print(f"total AI-token candidate bodies: {len(rows)}\n")
print("=== bodies with any spend token ===")
n_any = 0
n_strong = 0
for n, slug, dp, hits, strong, prev in rows:
    if n:
        n_any += 1
        if strong: n_strong += 1
        print(f"  {'STRONG' if strong else '      '} n={n:2d} {dp} {slug}\n        tokens={hits}")
print(f"\nbodies with >=1 spend token: {n_any} / {len(rows)}")
print(f"bodies with a strong spend signal: {n_strong} / {len(rows)}")

json.dump({"with_spend_token": n_any, "strong": n_strong, "total": len(rows),
           "rows": [{"slug": s, "date": d, "tokens": t, "strong": st} for n, s, d, t, st, _ in rows]},
          open(f"{OUT}/_textscan_0914.json","w"), indent=2)
