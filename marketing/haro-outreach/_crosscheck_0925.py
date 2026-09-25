#!/usr/bin/env python3
"""Cross-check: are all tracked slugs still in the sitemap, and which aged past the cold line today?"""
import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
xml = (D / "_sitemap_0925.xml").read_text(errors="ignore")
pairs = dict(re.findall(r"<loc>[^<]*?/journo-request/([^<]+?)</loc>\s*<lastmod>([^<]+)</lastmod>", xml))
verified = json.loads((D / "verified-requests.json").read_text())
ledger = json.loads((D / "pitch-ledger.json").read_text())
win = json.loads((D / "_window_0925.json").read_text())
MARK = win["mark"]

tracked = set(verified)
print(f"tracked: {len(tracked)}  sitemap slugs: {len(pairs)}")
missing = [s for s in tracked if s not in pairs]
print(f"tracked slugs MISSING from today's sitemap: {len(missing)} {missing}")
edited = [(s, pairs[s]) for s in tracked if s in pairs and pairs[s] > MARK]
print(f"tracked slugs with a lastmod inside today's window (i.e. edited/renewed): {len(edited)} {edited}")

print("\nages today (page datePublished) vs yesterday's digest:")
for s, r in sorted(verified.items(), key=lambda kv: kv[1].get("days_old") or 0):
    print(f"  {str(r.get('days_old')):>5}d {r.get('http')} live={str(r.get('live')):<5} {s[:66]}")
