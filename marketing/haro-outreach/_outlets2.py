#!/usr/bin/env python3
"""Read Sourcee outlet pages: list jurmo-request slugs + titles."""
import re, json, subprocess, sys, time

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def curl(url, timeout=35):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                       capture_output=True, text=True)
    return r.stdout


def field(raw, key):
    m = re.search(r'\\"' + key + r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw) \
        or re.search(r'"' + key + r'":"((?:[^"\\]|\\.)*?)"', raw)
    if not m:
        return None
    return m.group(1).replace("\\n", "\n").replace('\\"', '"').strip()


OUTLETS = ["forbes", "financial-times", "techcrunch"]
res = {}
for o in OUTLETS:
    url = f"https://www.sourcee.app/media-outlets/{o}/journo-requests"
    raw = curl(url)
    slugs = sorted(set(re.findall(r"/journo-request/([a-z0-9\-]{8,140})", raw)))
    res[o] = {"url": url, "bytes": len(raw), "count": len(slugs), "slugs": slugs}
    print("\n" + "=" * 80)
    print(f"OUTLET {o} | bytes {len(raw)} | {len(slugs)} listings")
    for s in slugs:
        print("  -", s)
    time.sleep(1.2)

json.dump(res, open("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/_outlets2.json", "w"), indent=1)
