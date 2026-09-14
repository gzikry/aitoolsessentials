#!/usr/bin/env python3
"""Fetch specific Sourcee journo-request pages and print JSON-LD fields."""
import re, json, subprocess, sys, time

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
BASE = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/"


def curl(url, timeout=35):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                       capture_output=True, text=True)
    return r.stdout


def field(raw, key):
    m = re.search(r'\\"' + key + r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw) \
        or re.search(r'"' + key + r'":"((?:[^"\\]|\\.)*?)"', raw)
    if not m:
        return None
    v = m.group(1)
    v = v.replace("\\u003c", "<").replace("\\u003e", ">").replace("\\/", "/")
    v = v.replace("\\n", "\n").replace('\\"', '"').replace("\\'", "'")
    return v.strip()


SLUGS = sys.argv[1].split(",")
out = []
for s in SLUGS:
    url = "https://www.sourcee.app/journo-request/" + s
    raw = curl(url)
    rec = {
        "slug": s,
        "url": url,
        "bytes": len(raw),
        "headline": field(raw, "headline"),
        "datePublished": field(raw, "datePublished"),
        "description": field(raw, "description"),
    }
    out.append(rec)
    print("\n" + "=" * 90)
    print("SLUG:", s)
    print("BYTES:", len(raw), "| HEADLINE:", rec["headline"])
    print("DATE:", rec["datePublished"])
    if not rec["headline"]:
        print(">>> NO HEADLINE - page may be removed")
    print("BODY:\n" + (rec["description"] or "(none)")[:1500])
    time.sleep(1.2)   # respect crawl-delay

json.dump(out, open(BASE + "_fetched2.json", "w"), indent=1)
print("\n\nsaved", len(out), "records")
