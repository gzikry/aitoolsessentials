#!/usr/bin/env python3
"""2026-09-19 candidate fetch: sitemap slugs newly indexed since the 2026-09-18 marker.

The slug filter cannot see a spend angle that only appears in the body, so every slug carrying
any AI token inside the recent window gets fetched and read. Two are the strongest new
candidates this run and had never been read: fulltime-employees-shadow-ai-use-and-paying-
outofpocket and speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech.
"""
import json
import re
import subprocess
import time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = D / "_bodies_0919.json"
SPEND = re.compile(r"(\$\s?\d|\u00a3\s?\d|\d+\s?(?:usd|dollars?|bucks)|/\s?month|per\s+month|per\s+seat|"
                   r"per\s+user|a\s+month|monthly|pricing|price[sd]?\b|cost|costs|subscri|budget|credit[s]?\b|"
                   r"spend|spending|billing|invoice|renewal|overlap|consolidat|licen[cs]e|seat[s]?\b|tier|"
                   r"reimburse|expense|paywall|fee[s]?\b|expensive|cheaper|afford|out.of.pocket|"
                   r"procurement|vendor|renew|waste|duplicate|stack|subscription|paying|pay for)", re.I)

SLUGS = """
fulltime-employees-shadow-ai-use-and-paying-outofpocket
speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
managers-and-tech-leaders-at-small-software-firms-ai-adoption
companies-that-stopped-emailing-pdfs-new-tools-and-transition
ai-safety-community-leaders-group-photo-publication
african-tech-practitioners-and-founders-technology-impact-on-africa
women-in-stem-onstage-representation-in-water-tech
real-estate-agents-3d-tour-vs-standard-packet-criteria
frontier-ai-and-national-security-experts-governing-ai-without-trust
legal-experts-in-australia-ai-coercive-control
eyeopener-students-against-ai-privacy-jobs-disinfo-and-bias
ukraine-tech-builders-and-global-observers-commercial-tech-adaptation
laidoff-tech-employees-personal-stories-on-industry-layoffs
book-publishers-and-authors-publisher-use-of-ai
ecommerce-engineering-leaders-peak-traffic-resilience-and-ai
adults-who-had-childhood-visions-ai-and-lunar-age-politics
ai-safety-researchers-and-practitioners-how-ai-could-eliminate-humanity
current-and-former-federal-employees-government-use-of-ai
ukrainian-founders-and-ceos-international-expansion-and-marketing-and-ai
dating-app-users-using-chatgpt-to-craft-messages-success
north-texas-parents-and-students-school-ai-policy-views
alpha-school-teachers-parents-and-alumni-ai-school-experiences
london-tech-telecoms-and-banking-veterans-navigating-change
people-experiencing-ai-synchronicities-firsthand-stories
""".split()


def field(raw, key):
    for pat in (r'"' + key + r'":\s*"((?:[^"\\]|\\.)*?)"',
                r'\\+"' + key + r'\\+":\\+"((?:[^"\\]|\\.)*?)\\+"'):
        m = re.search(pat, raw)
        if m:
            v = m.group(1)
            for _ in range(3):
                n = v.replace("\\n", " ").replace("\\u0026", "&").replace("\\/", "/")
                n = re.sub(r"\\(.)", r"\1", n)
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
prev = {}
for f in ("_bodies_0918b.json", "_bodies_0918.json"):
    p = D / f
    if p.exists():
        prev.update(json.loads(p.read_text()))

for i, sl in enumerate(SLUGS):
    if (bodies.get(sl) or {}).get("core"):
        continue
    if (prev.get(sl) or {}).get("core"):
        bodies[sl] = prev[sl]
        continue
    url = f"https://www.sourcee.app/journo-request/{sl}"
    code, raw = curl(url)
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    core = m.group(1).strip() if m else ""
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
    rec = {"slug": sl, "url": url, "http": code, "headline": field(raw, "headline"),
           "datePublished": field(raw, "datePublished"),
           "badge": badge.group(1) if badge else None, "author": field(raw, "name"),
           "domain": field(raw, "domain"),
           "email_redacted": bool(re.search(r"email redacted", core, re.I)),
           "emails_on_page": sorted(set(e for e in re.findall(
               r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core) if "sourcee" not in e.lower())),
           "core": core[:3000],
           "spend_tokens": sorted(set(x.group(0).lower().strip() for x in SPEND.finditer(core)))}
    bodies[sl] = rec
    OUT.write_text(json.dumps(bodies, indent=1))
    print(f"[{i}] {code} {str(rec['badge']):<21} tok={len(rec['spend_tokens']):<2} "
          f"{str(rec['domain'])[:22]:<24} {str(rec['headline'])[:56]}", flush=True)
    time.sleep(1)

print("\nfetched", len(bodies))
