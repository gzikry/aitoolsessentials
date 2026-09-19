import json
import re
import subprocess
import time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = D / "_bodies_0919b.json"
SPEND = re.compile(r"(\$\s?\d|\u00a3\s?\d|\d+\s?(?:usd|dollars?|bucks)|/\s?month|per\s+month|per\s+seat|"
                   r"per\s+user|a\s+month|monthly|pricing|price[sd]?\b|cost|costs|subscri|budget|credit[s]?\b|"
                   r"spend|spending|billing|invoice|renewal|overlap|consolidat|licen[cs]e|seat[s]?\b|tier|"
                   r"reimburse|expense|paywall|fee[s]?\b|expensive|cheaper|afford|out.of.pocket|"
                   r"procurement|vendor|renew|waste|duplicate|stack|subscription|paying|pay for)", re.I)

SLUGS = ["travelers-and-agents-top-cruise-and-caribbean-pick-travel-leisure",
         "health-tech-leaders-and-designers-narrative-medicine-podcast",
         "uk-adults-80-lifetime-tech-economic-and-social-change",
         "cornell-ar-program-participants-ai-academic-integrity-experiences",
         "sports-event-managers-and-infrastructure-experts-morocco-hosting-model",
         "parents-of-schoolaged-kids-teaching-ai-skills-and-home-ai-use",
         "independent-medicare-agents-plan-switching-before-open-enrollment",
         "medicare-insurance-agents-preopen-enrollment-switches-and-commissions"]

bodies = json.loads(OUT.read_text()) if OUT.exists() else {}
for sl in SLUGS:
    if (bodies.get(sl) or {}).get("core"):
        continue
    url = f"https://www.sourcee.app/journo-request/{sl}"
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url], capture_output=True, text=True)
    raw = r.stdout
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    core = m.group(1).strip() if m else ""
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
    bodies[sl] = {
        "slug": sl, "url": url, "core": core[:2600],
        "badge": badge.group(1) if badge else None,
        "spend_tokens": sorted(set(x.group(0).lower().strip() for x in SPEND.finditer(core))),
    }
    OUT.write_text(json.dumps(bodies, indent=1))
    print(f"{str(bodies[sl]['badge']):<21} tok={len(bodies[sl]['spend_tokens']):<2} {sl[:64]}", flush=True)
    time.sleep(1)

print()
for sl, v in bodies.items():
    print("=" * 92)
    print(sl, "| tokens:", v["spend_tokens"][:12])
    print("   ", v["core"][:330])
