#!/usr/bin/env python3
"""Re-resolve the Raconteur byline route.

The 2026-09-19 run reconstructed simon.chandler@raconteur.net from a data-part1/2/3 triple on
https://www.raconteur.net/author/simon-chandler/. That URL now returns 404, so this re-checks
whether the route still has a live source before a draft cites it.
"""
import re
import subprocess

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def get(url):
    r = subprocess.run(["curl", "-sL", "-m", "35", "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


code, raw = get("https://www.raconteur.net/author-sitemap.xml")
print(f"author-sitemap.xml http={code} bytes={len(raw)}")
locs = re.findall(r"<loc>([^<]+)</loc>", raw)
print("locs:", len(locs))
for l in locs[:15]:
    print("  ", l)

code, raw = get("https://www.raconteur.net/?s=simon+chandler")
print(f"\nsearch page http={code} bytes={len(raw)}")
for pat in (r'data-part[0-9]="[^"]*"', r'href="[^"]*author[^"]*"', r'href="[^"]*simon[^"]*"'):
    hits = sorted(set(re.findall(pat, raw)))[:8]
    print(f"  {pat} -> {hits}")

# Any article by him carries a byline link; find one and read its author page.
arts = sorted(set(re.findall(r"https://www\.raconteur\.net/[a-z0-9\-]+/[a-z0-9\-]+/", raw)))[:10]
print("\n  candidate article URLs on the search page:", arts[:6])
for a in arts[:3]:
    c, r2 = get(a)
    parts = re.findall(r'data-part([123])=["\\]?([^"\\>\s]+)', r2)
    links = sorted(set(re.findall(r'href="(https://www\.raconteur\.net/author/[^"]*)"', r2)))
    print(f"   {c} {a}  author-links={links}  parts={parts[:6]}")
