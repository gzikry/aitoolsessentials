#!/usr/bin/env python3
"""Quick compare of the 0928 vs 0929 sitemap pulls (offline, no network)."""
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")


def load(name):
    xml = (D / name).read_text(errors="ignore")
    pairs = re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", xml)
    slugs = [(l.rstrip("/").split("/journo-request/")[-1], lm) for l, lm in pairs if "/journo-request/" in l]
    return xml, slugs


for name in ("_sitemap_0927.xml", "_sitemap_0928.xml", "_sitemap_0929.xml"):
    xml, slugs = load(name)
    print(f"{name}: {len(xml):,} bytes, {len(slugs):,} pairs, newest {max(lm for _, lm in slugs)}")
