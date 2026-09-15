#!/usr/bin/env python3
"""Second-pass token sweep (pay/cancel/stack/sprawl etc.) + outlet page re-check."""
import json, re, subprocess, time

OUT = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
d = json.load(open(f"{OUT}/_scan_0914.json"))
recent = d["all_recent"]

SECOND = {"pay","paying","paid","cancel","cancelling","canceled","cancelled",
          "unsubscribe","stack","stacks","sprawl","duplicate","duplicates",
          "waste","wasted","overspend","overspending","tooling","saas","software"}

def toks(s): return set(s.split("-"))
print("=== SECOND-PASS TOKEN HITS ===")
hits = []
for k, v in sorted(recent.items(), key=lambda x: x[1], reverse=True):
    if toks(k) & SECOND:
        ai = "*AI*" if "ai" in toks(k) else "    "
        new = "NEW " if v > "2026-09-12T23:59:59" else "    "
        print(f"  {new}{ai} {v} {k}")
        hits.append((k, v, "ai" in toks(k)))

print(f"\nsecond-pass hits: {len(hits)}; of which AI co-occur: {sum(1 for h in hits if h[2])}")

def fetch(u):
    return subprocess.run(["curl","-sL","-m","40","-A",UA,u], capture_output=True, text=True).stdout

def field(raw, key):
    m = re.search(r'\\"'+key+r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw) or re.search(r'"'+key+r'":"((?:[^"\\]|\\.)*?)"', raw)
    return m.group(1).replace("\\n","\n").replace('\\"','"').strip() if m else None

# AI-token slugs in second pass that we have not assessed yet
already = set(json.load(open(f"{OUT}/_fetched_0914.json")).keys()) | set(json.load(open(f"{OUT}/_extra_0914.json")).keys())
todo = [k for k, v, isai in hits if isai and k not in already]
print("\nAI second-pass slugs not yet assessed:", todo)
res = {}
for s in todo:
    raw = fetch(f"https://www.sourcee.app/journo-request/{s}")
    h, dp, de = field(raw,"headline"), field(raw,"datePublished"), field(raw,"description")
    res[s] = {"headline":h,"datePublished":dp,"description":de,"bytes":len(raw)}
    print(f"\n--- {s}\n  bytes={len(raw)} date={dp}\n  headline={h}\n  desc={(de or '')[:700]!r}")
    time.sleep(1.0)
json.dump(res, open(f"{OUT}/_second_0914.json","w"), indent=2)

# outlet pages: re-check Forbes + TechCrunch listings
for slug in ["forbes", "techcrunch", "financial-times"]:
    u = f"https://www.sourcee.app/media-outlets/{slug}/journo-requests"
    raw = fetch(u)
    refs = re.findall(r'/journo-request/([a-z0-9\-]{8,120})', raw)
    uniq = sorted(set(refs))
    print(f"\n=== OUTLET {slug}: {len(raw)} bytes, {len(uniq)} listings")
    for s in uniq:
        print("   ", s)
    # titles
    js = json.load(open(f"{OUT}/_scan_0914.json"))["all_recent"]
    json.dump({"slug":slug,"bytes":len(raw),"listings":uniq}, open(f"{OUT}/_outlet_{slug}_0914.json","w"), indent=2)
    time.sleep(1.0)
