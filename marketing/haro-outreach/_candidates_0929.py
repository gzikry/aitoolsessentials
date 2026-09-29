#!/usr/bin/env python3
"""Fetch and read the 2026-09-29 candidate slugs in full (4 AI-token + 10 spend-any).

Read in full, because the AI+spend strict counter returned 0 and a zero has to be backed by
having read every row that could have been a hit.
"""
import json, re, subprocess
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

CANDIDATES = [
    # AI-token slugs
    "insurance-agents-ai-use-in-personal-lines",
    "data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity",
    "b2b-marketing-leaders-hyperspecialization-to-outcompete-ai",
    "ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes",
    # spend-any slugs
    "drivers-practicing-hypermiling-strategies-amid-rising-gas-prices",
    "young-adults-from-san-francisco-moved-to-more-affordable-areas",
    "parents-in-ireland-childcare-budget-priorities",
    "money-coaches-and-savings-experts-payday-hacks-christmas-twist",
    "washington-mystics-playoff-ticket-holders-ticket-price-impact",
    "1car-or-nocar-households-savings-vs-transit-costs",
    "nyc-energy-economist-fuel-cost-impact-ahead-of-heating-season",
    "gen-z-daters-1829-dating-budgets-and-financial-dealbreakers",
    "small-business-owners-faced-cashflow-crisis-and-budgeted-growth",
    "adults-living-with-exes-trapped-by-cost-of-living",
]

def curl(url, timeout=45):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)

out = {}
for slug in CANDIDATES:
    url = f"https://www.sourcee.app/journo-request/{slug}"
    code, raw = curl(url)
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    pub = re.search(r'datePublished"?\s*[:=]\s*"([^"]+)"', raw)
    out[slug] = {"url": url, "http": code, "bytes": len(raw),
                 "datePublished": (pub.group(1) if pub else None), "text": txt[:2600]}
    print("=" * 100)
    print(slug, "| HTTP", code, "|", len(raw), "bytes | datePublished:", out[slug]["datePublished"])
    print(txt[:1500])

(D / "_candidates_0929.json").write_text(json.dumps(out, indent=1))
