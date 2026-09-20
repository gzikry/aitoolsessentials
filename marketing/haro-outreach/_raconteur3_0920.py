#!/usr/bin/env python3
"""Find Simon Chandler's live contributor URL by trying the sitemap's exact strings and variants."""
import re
import subprocess
import urllib.parse

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def get(url):
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


code, raw = get("https://www.raconteur.net/author-sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", raw)
ch = [l for l in locs if "chandler" in l.lower()]
print("sitemap entries matching chandler:", ch)

cands = list(ch)
for c in ch:
    cands.append(c.replace("%20", "-").lower())
    cands.append(c.replace("%20", "").lower())
    cands.append(c + "/")
seen = []
for u in cands:
    if u in seen:
        continue
    seen.append(u)
    code, raw2 = get(u)
    parts = re.findall(r'data-part([123])=["\\]?([^"\\>\s]+)', raw2)
    d = {}
    for k, v in parts:
        d.setdefault(k, v)
    recon = f"{d['1']}@{d['2']}.{d['3']}" if len(d) >= 3 else None
    print(f"  {code} {u}  recon={recon}")
