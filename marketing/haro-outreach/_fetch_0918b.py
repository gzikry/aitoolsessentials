#!/usr/bin/env python3
"""Second-pass fetch: remaining AI-token candidates from the 2026-09-16/17 window.

These are the sitemap candidates that carry an AI token but no pricing/cost token in the slug —
the slug filter cannot see a spend angle that only appears in the body, and every on-beat request
this monitor has ever found was found by reading the body, not the slug.
"""
import json
import re
import subprocess
import time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = D / "_bodies_0918b.json"
SPEND = re.compile(r"(\$\s?\d|\u00a3\s?\d|\d+\s?(?:usd|dollars?|bucks)|/\s?month|per\s+month|per\s+seat|"
                   r"per\s+user|a\s+month|monthly|pricing|price[sd]?\b|cost|costs|subscri|budget|credit[s]?\b|"
                   r"spend|spending|billing|invoice|renewal|overlap|consolidat|licen[cs]e|seat[s]?\b|tier|"
                   r"reimburse|expense|paywall|fee[s]?\b|expensive|cheaper|afford|out.of.pocket|"
                   r"procurement|vendor|renew|waste|duplicate|stack|subscription|paying|pay for)", re.I)

SLUGS = """
ai-training-ops-robotics-and-physical-ai-data-collection
canadians-views-on-ai-in-newsrooms
mechanical-and-mfg-engineers-ai-limits-in-cadtomanufacture
neurips-attendees-in-vancouver-where-ai-is-headed
dating-app-users-using-ai-profile-creation-and-message-replies
women-ai-experts-in-china-development-regulation-and-power-shifts
futurists-ai-researchers-and-tech-builders-visions-tradeoffs-ethics
mri-engineers-and-clinicians-imaging-tech-procurement-and-patient-impact
uk-talent-tech-founders-ai-hiring-and-workforce-design-cnbc
project-delivery-innovators-tech-leadership-and-procurement-ideas
ecommerce-marketers-transparency-in-ai-recommendations-and-conversion
gen-z-ai-data-annotators-work-experience-and-income-impact
tech-founders-and-clevel-executives-podcast-feature-slots
brightonseo-san-diego-search-pros-aeo-geo-seo-and-ai-podcast
customer-experience-and-automation-leads-data-integration-and-safe-ai
machine-identity-vendors-ai-agent-delegation-solutions
employees-who-replaced-boss-with-ai-workplace-leadership-change
parents-and-partners-ai-replacing-parent-or-causing-friction
hr-leaders-ensuring-female-employees-access-ai-career-opportunities
sydney-creativeindustry-workers-and-students-ai-impact-creative-work
psychologists-studying-generative-ai-impact-on-thinking
hr-practitioners-strategic-workforce-planning-tools-and-ai
builders-using-ai-aidriven-knowledge-work-transformation
retail-tech-leaders-holiday-ai-impact-plain-language
us-manufacturing-plant-managers-ai-and-tech-trends
fulltime-employees-shadow-ai-use-and-paying-outofpocket
speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
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
cached = json.loads((D / "_bodies_0918.json").read_text())

for i, sl in enumerate(SLUGS):
    if sl in cached:
        bodies[sl] = cached[sl]
        continue
    if (bodies.get(sl) or {}).get("core"):
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
          f"{str(rec['domain'])[:24]:<26} {str(rec['headline'])[:58]}", flush=True)
    time.sleep(1)

print("\nfetched", len(bodies))
