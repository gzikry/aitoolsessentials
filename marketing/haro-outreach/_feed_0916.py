import subprocess, re, json, time
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")

feed = []
seen = set()
h = (D / "_feed_ai_topic.html")
if not h.exists():
    raw = subprocess.run(["curl", "-sL", "-m", "40", "-A", UA, "https://www.sourcee.app/topics/ai/journo-requests"],
                         capture_output=True, text=True).stdout
    h.write_text(raw)
raw = h.read_text(errors="ignore")
for s in re.findall(r"/journo-request/([a-z0-9\-]{5,160})", raw):
    if s not in seen:
        seen.add(s)
        feed.append(s)
print("AI topic feed slugs:", len(feed))

SPEND = re.compile(r'(\$\s?\d|\d+\s?(?:usd|dollars?|bucks)|per\s+month|per\s+seat|per\s+user|a\s+month|pricing|price[sd]?\b|cost|subscri|budget|credit[s]?\b|spend|billing|invoice|renewal|overlap|consolidat|licen[cs]e|seat[s]?\b|expense|fee[s]?\b|expensive|cheaper)', re.I)

out = {}
for i, sl in enumerate(feed):
    url = f"https://www.sourcee.app/journo-request/{sl}"
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url], capture_output=True, text=True).stdout
    body = re.sub(r"<script.*?</script>", " ", r, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"\s+", " ", txt).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    core = m.group(1).strip() if m else ""
    badge = re.search(r"(Posted[^ ]{0,3}(?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
    hl = re.search(r'\\"headline\\":\\"((?:[^"\\]|\\.)*?)\\"', r)
    hl = hl.group(1) if hl else None
    dom = re.search(r'\\"domain\\":\\"([^"\\]+)', r)
    tokens = sorted(set(x.group(0).lower().strip() for x in SPEND.finditer(core)))
    rec = {"slug": sl, "url": url, "headline": hl, "badge": badge.group(1) if badge else None,
           "domain": dom.group(1) if dom else None, "spend_tokens": tokens,
           "core": core[:1200]}
    out[sl] = rec
    flag = "*** SPEND" if len(tokens) >= 2 else ""
    print(f"{i+1:>3} {str(rec['badge']):<24} tok={len(tokens):<2} {str(hl)[:64]:<66} {flag}", flush=True)
    time.sleep(1)

(D / "_feed_0916.json").write_text(json.dumps(out, indent=1))
print("\n--- any request with 2+ spend tokens in the live feed ---")
for sl, rec in out.items():
    if len(rec["spend_tokens"]) >= 2:
        print("=" * 90)
        print(sl, "|", rec["badge"], "|", rec["domain"])
        print("TOKENS:", rec["spend_tokens"])
        print(rec["core"][:900])
