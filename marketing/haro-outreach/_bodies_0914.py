#!/usr/bin/env python3
"""Fetch remaining AI-token candidate bodies and scan the TEXT for spend language."""
import json, re, subprocess, time, os

OUT = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
scan = json.load(open(f"{OUT}/_scan_0914.json"))
pool = scan["candidate_pool"]

done = {}
for f in ["_fetched_0914.json", "_extra_0914.json", "_second_0914.json"]:
    p = f"{OUT}/{f}"
    if os.path.exists(p):
        done.update(json.load(open(p)))
print("already fetched:", len(done))

def field(raw, key):
    m = re.search(r'\\"'+key+r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw) or re.search(r'"'+key+r'":"((?:[^"\\]|\\.)*?)"', raw)
    return m.group(1).replace("\\n","\n").replace('\\"','"').strip() if m else None

todo = [s for s in pool if s not in done]
print("to fetch:", len(todo))
res = dict(done)
for i, s in enumerate(todo):
    raw = subprocess.run(["curl","-sL","-m","40","-A",UA,
                          f"https://www.sourcee.app/journo-request/{s}"],
                         capture_output=True, text=True).stdout
    res[s] = {"headline": field(raw,"headline"), "datePublished": field(raw,"datePublished"),
              "description": field(raw,"description"), "bytes": len(raw)}
    time.sleep(1.0)
    if i % 10 == 9:
        json.dump(res, open(f"{OUT}/_bodies_0914.json","w"), indent=2)
        print("  checkpoint", i+1)

json.dump(res, open(f"{OUT}/_bodies_0914.json","w"), indent=2)
print("fetched total:", len(res))
missing = [s for s in pool if not res.get(s, {}).get("headline")]
print("no-headline (removed/unreadable):", missing)
