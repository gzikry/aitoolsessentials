#!/usr/bin/env python3
"""Cross-check every tracked request against today's full sitemap: present? edited today?"""
import json, re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
prev = json.loads((D / "digest-2026-09-28.json").read_text())
tracked = {o["url"].rstrip("/").split("/journo-request/")[-1] for o in prev["opportunities"]}
xml = (D / "_sitemap_0929.xml").read_text(errors="ignore")
pairs = re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", xml)
sitemap = {l.rstrip("/").split("/journo-request/")[-1]: lm for l, lm in pairs if "/journo-request/" in l}
print("tracked:", len(tracked), "in sitemap:", sum(1 for t in tracked if t in sitemap))
print("MISSING from sitemap:", sorted(t for t in tracked if t not in sitemap))
MARK = "2026-09-28T03:31:57.000Z"
renewed = {t: sitemap[t] for t in tracked if t in sitemap and sitemap[t] > MARK}
print("carrying a lastmod inside today's new window:", renewed)
