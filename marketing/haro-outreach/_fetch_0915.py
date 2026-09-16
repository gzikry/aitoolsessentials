import subprocess, re, json, sys, time, os

D = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"

scan = json.load(open(f"{D}/_scan_0915.json"))
ai = scan["ai"]                      # slug -> lastmod
slugs = sorted(ai, key=lambda k: ai[k], reverse=True)

start = int(sys.argv[1]); end = int(sys.argv[2])
chunk = slugs[start:end]

out_path = f"{D}/_bodies_0915.json"
bodies = json.load(open(out_path)) if os.path.exists(out_path) else {}

def field(raw, key):
    m = re.search(r'\\"'+key+r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw) \
        or re.search(r'"'+key+r'":"((?:[^"\\]|\\.)*?)"', raw)
    if not m: return None
    return m.group(1).replace("\\n","\n").replace('\\"','"').replace("\\u0026","&").strip()

SPEND = re.compile(r'(\$\s?\d|\d+\s?(?:usd|dollars?|bucks)|\/\s?month|per\s+month|per\s+seat|per\s+user|a\s+month|monthly\s+(?:fee|cost|bill|price|plan)|pricing|price[sd]?\b|cost|costs|subscri|budget|credit[s]?\b|spend|spending|billing|invoice|renewal|overlap|consolidat|licen[cs]e|seat[s]?\b|tier|reimburse|expense|paywall|fee[s]?\b|expensive|cheaper|afford)', re.I)

for i, sl in enumerate(chunk):
    url = f"https://www.sourcee.app/journo-request/{sl}"
    if sl in bodies and bodies[sl].get("headline"):
        continue
    raw = subprocess.run(["curl","-sL","-m","30","-A",UA,url], capture_output=True, text=True).stdout
    hl, desc, dp = field(raw,"headline"), field(raw,"description"), field(raw,"datePublished")
    rec = {"slug": sl, "url": url, "lastmod": ai[sl], "bytes": len(raw),
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
    json.dump(bodies, open(out_path,"w"), indent=1)
    print(f"[{start+i}] {len(raw)}B strong={rec['strong']} tok={rec['spend_tokens']} {sl}", flush=True)
    time.sleep(1)   # robots crawl-delay 1

print("\nfetched total", len(bodies), "with headline", sum(1 for v in bodies.values() if v.get("headline")), "missing", sum(1 for v in bodies.values() if not v.get("headline")))
strong = [k for k,v in bodies.items() if v.get("strong")]
print("STRONG spend signal:", len(strong))
for k in strong:
    print("  ", bodies[k]["datePublished"], "|", bodies[k]["headline"], "|tok", bodies[k]["spend_tokens"], "|", k)
