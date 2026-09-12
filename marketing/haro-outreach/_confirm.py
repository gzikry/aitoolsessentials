#!/usr/bin/env python3
"""Look up sitemap lastmod for specific slugs to confirm they are still listed."""
import re, subprocess, json

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
raw = subprocess.run(["curl", "-sL", "-m", "90", "-A", UA,
                      "https://www.sourcee.app/sitemap-journo-requests.xml"],
                     capture_output=True, text=True).stdout
pairs = re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", raw)
m = {u.rsplit("/", 1)[-1]: (u, lm) for u, lm in pairs}
print("sitemap entries:", len(m))

WATCH = [
    "finops-professionals-agentic-ai-cost-overruns",
    "enterprise-ai-leaders-ai-governance-and-agent-sprawl",
    "scientists-phd-students-and-postdocs-paying-for-ai-subscriptions",
    "anthropic-users-and-business-owners-customer-service-experiences",
    "individual-contributors-managing-ai-agents-without-title-or-pay",
    "tech-policy-experts-california-ai-audit-bills-impact-cios",
    "employees-hiding-knowledge-workplace-ai-data-compensation",
    "amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot",
    "business-and-technology-leaders-tech-budget-priorities-amid-volatility",
    "ai-startups-workplace-fraud-detection-expenses-time-theft",
    "earlystage-founders-building-saas-and-ai-tools-built-from-scratch",
    "employees-and-executives-workplace-ai-writing-rules-and-stories",
    "ai-agents-making-money-2026-sales-and-leadgen-workflow-ops",
    "ceos-ai-impact-on-ops-culture-and-commercial-strategy",
    "companies-ditching-per-seat-pricing-ai",
    "software-budget-cuts-shadow-ai-spending",
]
for s in WATCH:
    v = m.get(s)
    print(f"{'FOUND' if v else 'ABSENT':6} {v[1][:19] if v else '-':20} {s}")
