import subprocess, re, json, sys, time, os

D = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"

scan = json.load(open(f"{D}/_scan_0916.json"))
pool = {}
for grp in ("tight_since_0915_ai", "ai", "strict", "third_ai", "strict_ai"):
    pass
# union: everything lastmod >= 2026-09-02 that matched ANY filter, plus the tight window
sel = {}
for key in ("ai", "strict", "strict_ai", "third_ai"):
    for k, v in (scan.get(key) or {}).items():
        sel[k] = v
# add tight window (need it stored) - rebuild from sitemap
s = open("/tmp/sitemap_0916.xml", errors="ignore").read()
pairs = re.findall(r'<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>', s)
for loc, lm in pairs:
    m = re.search(r'/journo-request/([a-z0-9\-]{5,160})', loc)
    if m and lm >= "2026-09-15T16:00:00":
        sel[m.group(1)] = lm

out_path = f"{D}/_bodies_0916.json"
bodies = json.load(open(out_path)) if os.path.exists(out_path) else {}

def field(raw, key):
    m = re.search(r'\\"' + key + r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw) \
        or re.search(r'"' + key + r'":"((?:[^"\\]|\\.)*?)"', raw)
    if not m:
        return None
    return m.group(1).replace("\\n", "\n").replace('\\"', '"').replace("\\u0026", "&").strip()

SPEND = re.compile(r'(\$\s?\d|\d+\s?(?:usd|dollars?|bucks)|\/\s?month|per\s+month|per\s+seat|per\s+user|a\s+month|monthly\s+(?:fee|cost|bill|price|plan)|pricing|price[sd]?\b|cost|costs|subscri|budget|credit[s]?\b|spend|spending|billing|invoice|renewal|overlap|consolidat|licen[cs]e|seat[s]?\b|tier|reimburse|expense|paywall|fee[s]?\b|expensive|cheaper|afford)', re.I)

slugs = sorted(sel, key=lambda k: sel[k], reverse=True)
todo = [sl for sl in slugs if not (bodies.get(sl) or {}).get("headline")]
print("pool", len(slugs), "todo", len(todo), flush=True)

for i, sl in enumerate(todo):
    url = f"https://www.sourcee.app/journo-request/{sl}"
    raw = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url], capture_output=True, text=True).stdout
    hl, desc, dp = field(raw, "headline"), field(raw, "description"), field(raw, "datePublished")
    rec = {"slug": sl, "url": url, "lastmod": sel[sl], "bytes": len(raw),
           "headline": hl, "datePublished": dp, "body": desc}
    if desc:
        hits = sorted(set(m.group(0).lower().strip() for m in SPEND.finditer(desc)))
        rec["spend_hits"] = hits
        rec["spend_tokens"] = len(hits)
        money = bool(re.search(r'\$\s?\d|\d+\s?(?:usd|dollars?|bucks)', desc))
        permo = bool(re.search(r'(?:\/\s?month|per\s+month|per\s+seat|per\s+user|a\s+month)', desc, re.I))
        rec["strong"] = bool(money or permo or len(hits) >= 2)
    else:
        rec["spend_hits"], rec["spend_tokens"], rec["strong"] = [], 0, False
    bodies[sl] = rec
    json.dump(bodies, open(out_path, "w"), indent=1)
    print(f"[{i}] {len(raw)}B strong={rec['strong']} tok={rec['spend_tokens']} {sl}", flush=True)
    time.sleep(1)

print("\nfetched total", len(bodies), "with headline", sum(1 for v in bodies.values() if v.get("headline")))
strong = [k for k, v in bodies.items() if v.get("strong") and (v.get("lastmod") or "") >= "2026-09-02"]
print("STRONG spend signal in window:", len(strong))
for k in sorted(strong, key=lambda k: bodies[k]["lastmod"], reverse=True):
    b = bodies[k]
    print("  ", b["lastmod"], "|", (b["headline"] or "")[:95], "|tok", b["spend_tokens"], "|", k)
