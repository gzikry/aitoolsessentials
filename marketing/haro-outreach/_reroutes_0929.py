#!/usr/bin/env python3
"""Re-resolve every hand-resolved reply route against the live page today (one attempt each)."""
import re, subprocess
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def curl(url, timeout=45):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


# 1. Raconteur byline address, assembled from data-part1/2/3 by the site's own JS.
for url in ("https://www.raconteur.net/contributors/simon-chandler",
            "https://www.raconteur.net/contributors/tom-dennis",
            "https://www.raconteur.net/author/simon-chandler/"):
    code, raw = curl(url)
    parts = re.findall(r'data-part[123]="([^"]+)"', raw)
    print(f"{code} {len(raw):>8} {url}  parts={parts[:4]}")

# 2. Speciality Food masthead contact page.
code, raw = curl("https://www.specialityfoodmagazine.com/contact")
emails = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)))
print(f"\n{code} {len(raw):>8} specialityfoodmagazine.com/contact")
print("  emails:", [e for e in emails if "specialityfood" in e or "artichoke" in e][:12])

# 3. The Anthropic request's published Signal / DM route, re-read verbatim off its own page.
code, raw = curl("https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences")
body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
txt = re.sub(r"<[^>]+>", " ", body)
txt = re.sub(r"\s+", " ", txt).strip()
m = re.search(r"Start free trial(.*?)Brought to you by Sourcee", txt, re.S)
core = m.group(1).strip() if m else txt
print(f"\n{code} {len(raw):>8} anthropic request")
print("  signal/handles:", re.findall(r"[Ss]ignal[^.]{0,60}|hliwrites[.\w]*|linkedin\.com/in/[A-Za-z0-9\-]+", core)[:6])

# 4. The FinOps LinkedIn DM route.
code, raw = curl("https://www.linkedin.com/in/niloy-ghosh")
print(f"\n{code} {len(raw):>8} linkedin.com/in/niloy-ghosh")
code2, raw2 = curl("https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns")
b2 = re.sub(r"<script.*?</script>", " ", raw2, flags=re.S | re.I)
t2 = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", b2)).strip()
m2 = re.search(r"Start free trial(.*?)Brought to you by Sourcee", t2, re.S)
c2 = m2.group(1).strip() if m2 else t2
print(f"{code2} {len(raw2):>8} finops request")
print("  linkedin/dm hints:", re.findall(r"linkedin\.com/in/[A-Za-z0-9\-]+|DM[^.]{0,40}|Comment[^.]{0,40}", c2)[:8])
