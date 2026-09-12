#!/usr/bin/env python3
"""Fetch full text of the shortlisted Sourcee requests."""
import re, json, subprocess, html, time, os

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
OUT = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/_requests.json"

SLUGS = [
    "builders-using-ai-aidriven-knowledge-work-transformation",
    "anthropic-users-and-business-owners-customer-service-experiences",
    "individual-contributors-managing-ai-agents-without-title-or-pay",
    "technology-expert-tech-industry-commentary-daily-mirror",
    "users-receiving-paid-agent-requests-aggressive-spam-and-no-optout",
    "ai-and-mobile-tech-experts-journalist-story-on-emerging-tech",
    "tech-policy-experts-california-ai-audit-bills-impact-cios",
    "ai-agents-making-money-2026-sales-and-leadgen-workflow-ops",
    "ai-startup-founder-newsletter-feature-builds-and-tech-challenges",
    "small-charities-with-ai-products-and-funders-scaling-support",
    "ai-experts-anthropic-researcher-resignation",
    "eam-professionals-apac-and-anz-platform-usage-industry-report",
    "ceos-ai-impact-on-ops-culture-and-commercial-strategy",
    "business-leaders-practical-ai-amplifying-human-connection",
    # carried-forward / previously reported
    "finops-professionals-agentic-ai-cost-overruns",
    "enterprise-ai-leaders-ai-governance-and-agent-sprawl",
    "scientists-phd-students-and-postdocs-paying-for-ai-subscriptions",
    "ai-startups-workplace-fraud-detection-expenses-time-theft",
    "earlystage-founders-building-saas-and-ai-tools-built-from-scratch",
    "amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot",
    "employees-and-executives-workplace-ai-writing-rules-and-stories",
    "employees-hiding-knowledge-workplace-ai-data-compensation",
    "managers-who-scaled-startups-preventing-organizational-drift",
]

res = {}
if os.path.exists(OUT):
    res = json.load(open(OUT))

for slug in SLUGS:
    if slug in res and res[slug].get("text"):
        continue
    url = f"https://www.sourcee.app/journo-request/{slug}"
    raw = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url],
                         capture_output=True, text=True).stdout
    m = re.search(r"(?is)<main.*?</main>", raw)
    body = ""
    if m:
        s = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", m.group(0))
        s = re.sub(r"(?s)<[^>]+>", "\n", s)
        s = html.unescape(s)
        s = s.split("We find journo requests from across the web")[0]
        lines = [l.strip() for l in s.split("\n") if l.strip()]
        body = "\n".join(lines)
    res[slug] = {"url": url, "text": body[:3500], "len": len(body)}
    print(f"--- {slug} ({len(body)} chars) ---")
    print(body[:1800])
    print()
    time.sleep(1.2)

json.dump(res, open(OUT, "w"), indent=1)
print("saved", OUT, "| entries:", len(res))
