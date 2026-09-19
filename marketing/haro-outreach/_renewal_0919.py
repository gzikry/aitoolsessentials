#!/usr/bin/env python3
"""Cross-reference verified request ages against the sitemap lastmod.

Purpose: distinguish a request that is merely OLD from one that is old and unrenewed. Sourcee
refreshes a request's lastmod when the poster edits/renews it; if lastmod == datePublished the
page has not been touched since it was posted. The queue's STALE_DAYS rule treats all >10-day
requests as cold regardless, so this adds the one signal it lacks.
"""
import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
raw = Path("/tmp/sitemap_journo_0919.xml").read_text(errors="ignore")
pairs = re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", raw)
m = {}
for loc, lm in pairs:
    s = re.search(r"/journo-request/([a-z0-9\-]{5,160})", loc)
    if s:
        m.setdefault(s.group(1), []).append(lm)
m = {k: max(v) for k, v in m.items()}
v = json.load(open(D / "verified-requests.json"))
print(f"{'slug':<62} {'published':<12} {'lastmod':<12} renewed")
n_ref = 0
for slug, r in sorted(v.items(), key=lambda x: x[1].get("days_old") if x[1].get("days_old") is not None else 999):
    dp = (r.get("datePublished") or "")[:10]
    lm = m.get(slug, "MISSING")[:10]
    ref = lm != dp
    if ref:
        n_ref += 1
    print(f"{slug:<62} {dp:<12} {lm:<12} {'YES' if ref else 'no'}")
print("\nrenewed since posting:", n_ref, "of", len(v))
json.dump({s: {"published": (r.get("datePublished") or "")[:10], "lastmod": m.get(s),
               "renewed": m.get(s, "")[:10] != (r.get("datePublished") or "")[:10]}
           for s, r in v.items()},
          open(D / "_renewal_0919.json", "w"), indent=1)
