#!/usr/bin/env python3
"""List strict/wide hits, then fetch any untested new candidates."""
import json, re, subprocess, time

OUT = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
d = json.load(open(f"{OUT}/_scan_0914.json"))
recent = d["all_recent"]
STRICT = {"pricing","price","prices","cost","costs","subscription","subscriptions",
          "spend","spending","credit","credits","renewal","renewals","overlap",
          "overlapping","consolidat","consolidation","finops","budget","budgets"}
WIDE = {"cfo","finance","procurement","licensing","license","seat","seats","audit",
        "audits","invoice","invoices","billing","expense","expenses","usage","tco",
        "roi","vendor","vendors","contract","contracts"}

def toks(s): return set(s.split("-"))

print("=== STRICT HITS (window since 09-02, lastmod desc) ===")
for k, v in sorted(recent.items(), key=lambda x: x[1], reverse=True):
    if toks(k) & STRICT:
        ai = "*AI*" if "ai" in toks(k) else "    "
        new = "NEW " if v > "2026-09-12T23:59:59" else "    "
        print(f"  {new}{ai} {v} {k}")

print("\n=== WIDE HITS ===")
for k, v in sorted(recent.items(), key=lambda x: x[1], reverse=True):
    if toks(k) & WIDE:
        ai = "*AI*" if "ai" in toks(k) else "    "
        new = "NEW " if v > "2026-09-12T23:59:59" else "    "
        print(f"  {new}{ai} {v} {k}")

# untested new candidates worth a body fetch (from the 39 new slugs)
extra = [s for s in d["new_since_last_run"] if any(t in s for t in
         ("data-center", "audit", "tech", "software", "saas", "cost", "spend",
          "pricing", "budget", "subscription", "tool", "startup", "founder"))]
extra = [s for s in extra if s not in d["candidate_pool"]]
print("\n=== EXTRA NEW SLUGS TO ASSESS ===")
for s in extra: print("  ", s)

def fetch(u):
    return subprocess.run(["curl","-sL","-m","40","-A",UA,u], capture_output=True, text=True).stdout

def field(raw, key):
    m = re.search(r'\\"'+key+r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw) or re.search(r'"'+key+r'":"((?:[^"\\]|\\.)*?)"', raw)
    return m.group(1).replace("\\n","\n").replace('\\"','"').strip() if m else None

out = {}
for s in extra:
    raw = fetch(f"https://www.sourcee.app/journo-request/{s}")
    h, dp, de = field(raw,"headline"), field(raw,"datePublished"), field(raw,"description")
    out[s] = {"headline":h,"datePublished":dp,"description":de,"bytes":len(raw)}
    print(f"\n--- {s}\n  bytes={len(raw)} date={dp}\n  headline={h}\n  desc={ (de or '')[:900]!r}")
    time.sleep(1.0)

json.dump(out, open(f"{OUT}/_extra_0914.json","w"), indent=2)
print("\nwrote _extra_0914.json", len(out))
