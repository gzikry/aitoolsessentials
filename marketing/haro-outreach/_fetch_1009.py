#!/usr/bin/env python3
"""2026-10-09 candidate fetch: read the bodies of every AI-token window slug plus the
spend-any slugs that could carry an AI+spend angle. Same extraction as _fetch_1008.py.
"""
import json
import re
import subprocess
import time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = D / "_bodies_1009.json"

SLUGS = """
sales-reps-who-cold-call-and-email-how-ai-changed-outreach
enterprise-ai-leaders-and-builders-realworld-deployment-and-strategy
voters-who-used-ai-to-navigate-ballot-voting-experience
hotel-and-fandb-supervisors-and-managers-customer-expectations-vs-ai
researchers-founders-and-funders-ai-transforming-scientific-research
facebook-marketplace-sellers-ai-listing-photos-and-selling-experience
economists-and-technologists-bank-runs-from-ai-markets-and-social-media
consumers-using-ai-finance-agents-experiences-managing-money
people-who-paid-irish-citizenship-firms-misled-and-still-waiting
seattle-friends-and-family-pairs-therapistled-political-conversation
omaha-commuters-and-residents-parkomaha-paid-parking-expansion
grocery-shoppers-who-return-food-time-effort-and-costs
nj-policy-experts-ways-mikie-sherrill-can-cut-costs-now
brit-who-stayed-with-partner-costofliving-relationship-tradeoffs
spouses-whose-partner-left-with-coworker-paid-fee
""".split()


def field(raw, key):
    for pat in (r'"' + key + r'":\s*"((?:[^"\\]|\\.)*?)"',
                r'\\+"' + key + r'\\+":\\+"((?:[^"\\]|\\.)*?)\\+"'):
        m = re.search(pat, raw)
        if m:
            v = m.group(1)
            for _ in range(3):
                n = v.replace("\\n", " ").replace("\\u0026", "&").replace("\\/", "/")
                n = re.sub(r'\\(.)', r'\1', n)
                if n == v:
                    break
                v = n
            return v.strip()
    return None


def curl(url):
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


bodies = json.loads(OUT.read_text()) if OUT.exists() else {}

for i, sl in enumerate(SLUGS):
    if (bodies.get(sl) or {}).get("core"):
        continue
    url = f"https://www.sourcee.app/journo-request/{sl}"
    code, raw = curl(url)
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    core = m.group(1).strip() if m else ""
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
    links = [u for u in sorted(set(re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,160}", raw)))
             if not any(c in u for c in ("sourcee.app", "vercel", "sentry", "nextjs.org", "schema.org",
                                         "w3.org", "gstatic", "google.com/s2", "supabase.co"))]
    rec = {"slug": sl, "url": url, "http": code, "headline": field(raw, "headline"),
           "datePublished": field(raw, "datePublished"),
           "badge": badge.group(1) if badge else None, "author": field(raw, "name"),
           "domain": field(raw, "domain"),
           "email_redacted": bool(re.search(r"email redacted", core, re.I)),
           "emails_on_page": sorted(set(e for e in re.findall(
               r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core) if "sourcee" not in e.lower())),
           "published_links": links[:6],
           "core": core[:4000]}
    bodies[sl] = rec
    OUT.write_text(json.dumps(bodies, indent=1))
    print(f"[{i}] {code} {str(rec['badge']):<21} link={len(links):<2} "
          f"{str(rec['domain'])[:24]:<26} {str(rec['headline'])[:64]}", flush=True)
    time.sleep(1)

print("\nfetched", len(bodies))
