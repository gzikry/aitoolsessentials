import subprocess, re, json, os
D = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"

s = open("/tmp/sitemap_0915.xml", errors="ignore").read()
pairs = re.findall(r'<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>', s)
allslugs = {}
for loc, lm in pairs:
    m = re.search(r'/journo-request/([a-z0-9\-]{5,160})', loc)
    if m and (m.group(1) not in allslugs or lm > allslugs[m.group(1)]):
        allslugs[m.group(1)] = lm

def field(raw, key):
    m = re.search(r'\\"'+key+r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw) \
        or re.search(r'"'+key+r'":"((?:[^"\\]|\\.)*?)"', raw)
    if not m: return None
    return m.group(1).replace("\\n","\n").replace('\\"','"').strip()

def get(url, timeout=30):
    return subprocess.run(["curl","-sL","-m",str(timeout),"-A",UA,url], capture_output=True, text=True).stdout

CARRY = {
 "anthropic-users-and-business-owners-customer-service-experiences": "pitch-now-or-drop (#1)",
 "edtech-product-managers-lms-audit-does-product-manage-learning": "#2 EdTech adjacent",
 "business-and-technology-leaders-tech-budget-priorities-amid-volatility": "#3 Forbes hold",
}
out = {"carry_checks": {}, "outlets": {}}
print("=== CARRY ITEM CHECKS ===")
for sl, label in CARRY.items():
    lm = allslugs.get(sl)
    raw = get(f"https://www.sourcee.app/journo-request/{sl}")
    hl, desc, dp = field(raw,"headline"), field(raw,"description"), field(raw,"datePublished")
    rec = {"label": label, "sitemap_lastmod": lm, "http_bytes": len(raw), "headline": hl,
           "datePublished": dp, "body_len": len(desc or ""), "body": desc,
           "removed": hl is None, "url": f"https://www.sourcee.app/journo-request/{sl}"}
    out["carry_checks"][sl] = rec
    print(f"{sl}\n   lastmod={lm} bytes={len(raw)} removed={rec['removed']} datePublished={dp} bodylen={rec['body_len']}")
    print("   headline:", hl)

print("\n=== OUTLET PAGES ===")
for o in ["forbes", "financial-times", "techcrunch"]:
    url = f"https://www.sourcee.app/media-outlets/{o}/journo-requests"
    raw = get(url, 40)
    slugs = sorted(set(re.findall(r'/journo-request/([a-z0-9\-]{8,140})', raw)))
    titles = []
    for sl in slugs:
        m = re.search(r'\\"headline\\":\\"((?:[^"\\]|\\.)*?)\\"', raw)
        titles.append(sl)
    ai = [x for x in slugs if re.search(r'\bai\b|artificial|llm|agent|chatgpt|claude|copilot|model', x)]
    out["outlets"][o] = {"bytes": len(raw), "count": len(slugs), "slugs": slugs, "ai_slugs": ai}
    print(f"\n{o}: {len(raw)}B, {len(slugs)} listings; AI-ish: {ai}")
    for sl in slugs: print("   -", sl)

json.dump(out, open(f"{D}/_carry_outlets_0915.json","w"), indent=1)
