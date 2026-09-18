#!/usr/bin/env python3
"""Fetch candidate request bodies for the 2026-09-18 run.

Only /journo-request/<slug> pages are fetched. The sitemap candidate list for this run is
_scan_0918.json; bodies are cached so a re-run does not re-pay for anything already read.
"""
import json
import re
import subprocess
import time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = D / "_bodies_0918.json"
SPEND = re.compile(r"(\$\s?\d|\d+\s?(?:usd|dollars?|bucks)|/\s?month|per\s+month|per\s+seat|per\s+user|"
                   r"a\s+month|monthly\s+(?:fee|cost|bill|price|plan)|pricing|price[sd]?\b|cost|costs|"
                   r"subscri|budget|credit[s]?\b|spend|spending|billing|invoice|renewal|overlap|"
                   r"consolidat|licen[cs]e|seat[s]?\b|tier|reimburse|expense|paywall|fee[s]?\b|"
                   r"expensive|cheaper|afford|out.of.pocket)", re.I)

CANDIDATES = [
    "fulltime-employees-shadow-ai-use-and-paying-outofpocket",
    "hr-practitioners-strategic-workforce-planning-tools-and-ai",
    "builders-using-ai-aidriven-knowledge-work-transformation",
    "speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech",
    "ai-automation-experts-speakers-on-marketing-sales-operations-gains",
    "retail-tech-leaders-holiday-ai-impact-plain-language",
    "us-manufacturing-plant-managers-ai-and-tech-trends",
    "marketing-and-content-leaders-aiassisted-work-review-process",
    "ai-agents-making-money-2026-sales-and-leadgen-workflow-ops",
    "individual-contributors-managing-ai-agents-without-title-or-pay",
    "anthropic-users-and-business-owners-customer-service-experiences",
    "earlystage-founders-building-saas-and-ai-tools-built-from-scratch",
    "scientists-phd-students-and-postdocs-paying-for-ai-subscriptions",
    "ai-startups-workplace-fraud-detection-expenses-time-theft",
    "finops-professionals-agentic-ai-cost-overruns",
    "amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot",
]


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
    code = m.group(1) if m else "000"
    return code, (raw[:raw.rfind("__HTTP__")] if m else raw)


def visible(raw):
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"\s+", " ", txt).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    return m.group(1).strip() if m else ""


bodies = json.loads(OUT.read_text()) if OUT.exists() else {}
for i, sl in enumerate(CANDIDATES):
    if (bodies.get(sl) or {}).get("core"):
        print(f"[{i}] cached {sl}", flush=True)
        continue
    url = f"https://www.sourcee.app/journo-request/{sl}"
    code, raw = curl(url)
    core = visible(raw)
    desc = field(raw, "description") or ""
    dp = field(raw, "datePublished")
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
    emails = sorted(set(e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core)
                        if "sourcee" not in e.lower()))
    rec = {"slug": sl, "url": url, "http": code, "headline": field(raw, "headline"),
           "datePublished": dp, "badge": badge.group(1) if badge else None,
           "domain": field(raw, "domain"), "emails_on_page": emails,
           "email_redacted": bool(re.search(r"email redacted", core, re.I)),
           "core": core[:2500], "desc": desc[:2500],
           "spend_tokens": sorted(set(m.group(0).lower().strip() for m in SPEND.finditer(core + " " + desc)))}
    bodies[sl] = rec
    OUT.write_text(json.dumps(bodies, indent=1))
    print(f"[{i}] {code} {str(rec['badge']):<22} tok={len(rec['spend_tokens']):<2} "
          f"{str(rec['headline'])[:60]} | {sl}", flush=True)
    time.sleep(1)
print("\nfetched", len(bodies))
