import subprocess, re, json
D = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
def field(raw, key):
    m = re.search(r'\\"'+key+r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw) \
        or re.search(r'"'+key+r'":"((?:[^"\\]|\\.)*?)"', raw)
    if not m: return None
    return m.group(1).replace("\\n","\n").replace('\\"','"').strip()
slugs = ["ai-content-moderation-experts-techcrunch-sameday",
         "ai-researchers-or-cybersecurity-experts-on-moltbook-privacy-techcrunch",
         "people-managers-no-founders-and-entrepreneurs-ai-and-working-motherhood",
         "us-dealer-principals-gms-and-group-leaders-ai-dealership-ops",
         "ai-and-mobile-tech-experts-journalist-story-on-emerging-tech",
         "technology-expert-tech-industry-commentary-daily-mirror"]
out = {}
for sl in slugs:
    raw = subprocess.run(["curl","-sL","-m","30","-A",UA,f"https://www.sourcee.app/journo-request/{sl}"],capture_output=True,text=True).stdout
    hl, desc, dp = field(raw,"headline"), field(raw,"description"), field(raw,"datePublished")
    spend = bool(re.search(r'(\$\s?\d|\/\s?month|per\s+seat|pricing|subscription|cost|budget|spend|credit|licen[cs]e)', (desc or ""), re.I))
    out[sl] = {"bytes": len(raw), "headline": hl, "datePublished": dp, "body": desc, "spend": spend}
    print(f"\n### {sl}\n  bytes={len(raw)} dp={dp} spend_lang={spend}\n  HL: {hl}\n  BODY: {(desc or '')[:900]}")
json.dump(out, open(f"{D}/_extra_0915.json","w"), indent=1)
