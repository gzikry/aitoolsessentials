#!/usr/bin/env python3
"""Fetch + assess Sourcee request bodies for the 2026-09-14 run."""
import re, json, subprocess, time, html

OUT = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def fetch(url):
    return subprocess.run(["curl", "-sL", "-m", "40", "-A", UA, url],
                          capture_output=True, text=True).stdout

def field(raw, key):
    m = re.search(r'\\"' + key + r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw) \
        or re.search(r'"' + key + r'":"((?:[^"\\]|\\.)*?)"', raw)
    if not m:
        return None
    v = m.group(1).replace("\\n", "\n").replace('\\"', '"').replace("\\u0026", "&")
    return v.strip()

TARGETS = [
    # health check (known-live, per skill)
    "finops-professionals-agentic-ai-cost-overruns",
    # carried items
    "anthropic-users-and-business-owners-customer-service-experiences",
    "amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot",
    "business-and-technology-leaders-tech-budget-priorities-amid-volatility",
    "ceos-ai-impact-on-ops-culture-and-commercial-strategy",
    # new since last run (AI-token)
    "brightonseo-san-diego-search-pros-aeo-geo-seo-and-ai-podcast",
    "customer-experience-and-automation-leads-data-integration-and-safe-ai",
    "alpha-school-teachers-parents-and-alumni-ai-school-experiences",
    # untested candidates
    "current-and-former-federal-employees-government-use-of-ai",
    "ukrainian-founders-and-ceos-international-expansion-and-marketing-and-ai",
    "psychologists-studying-generative-ai-impact-on-thinking",
    "sydney-creativeindustry-workers-and-students-ai-impact-creative-work",
    "parents-of-schoolaged-kids-teaching-ai-skills-and-home-ai-use",
    "ai-ethics-scholars-ethical-use-of-ai-in-research-and-writing",
    "employees-and-executives-workplace-ai-writing-rules-and-stories",
    "technology-leaders-educators-students-percent-of-role-ai-could-do",
    "ai-experts-and-creators-us-govt-backing-openai-on-copyrighted-training",
    "ai-agents-making-money-2026-sales-and-leadgen-workflow-ops",
    "supply-chain-ai-experts-research-and-industry-impact",
    "pharma-marketing-leaders-ai-impact-and-industry-restructures",
]

res = {}
for slug in TARGETS:
    url = f"https://www.sourcee.app/journo-request/{slug}"
    raw = fetch(url)
    rec = {
        "url": url,
        "bytes": len(raw),
        "headline": field(raw, "headline"),
        "datePublished": field(raw, "datePublished"),
        "description": field(raw, "description"),
    }
    res[slug] = rec
    print(f"--- {slug}\n  bytes={rec['bytes']} date={rec['datePublished']}")
    print(f"  headline={rec['headline']}")
    d = rec["description"] or ""
    print(f"  desc({len(d)})={d[:1400]!r}\n")
    time.sleep(1.2)

json.dump(res, open(f"{OUT}/_fetched_0914.json", "w"), indent=2)
print("wrote _fetched_0914.json", len(res))
