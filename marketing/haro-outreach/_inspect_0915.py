import json, glob, re, os
D = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"
bodies = json.load(open(f"{D}/_bodies_0915.json"))

print("=== NEW STRONG / NOTABLE BODIES ===")
for sl in ["frontier-lab-researchers-archives-teaching-models",
           "global-innovators-scifi-tech-and-futuristic-locations",
           "ai-startups-workplace-fraud-detection-expenses-time-theft",
           "parents-who-bought-ai-toys-nonanonymous-experiences-and-fee-offered",
           "employees-hiding-knowledge-workplace-ai-data-compensation",
           "anthropic-users-and-business-owners-customer-service-experiences",
           "enterprise-ai-leaders-value-creation-ownership-and-governance"]:
    v = bodies.get(sl)
    if not v:
        print("!! not fetched:", sl); continue
    print("\n----", sl, "|", v["datePublished"], "| strong", v["strong"], "| hits", v["spend_hits"])
    print(v["headline"])
    print((v["body"] or "")[:1400])

print("\n=== APPEARANCE COUNTS ACROSS DIGESTS ===")
digests = sorted(glob.glob(f"{D}/digest-*.json"))
cands = ["anthropic-users-and-business-owners-customer-service-experiences",
         "edtech-product-managers-lms-audit-does-product-manage-learning",
         "business-and-technology-leaders-tech-budget-priorities-amid-volatility",
         "finops-professionals-agentic-ai-cost-overruns",
         "enterprise-ai-leaders-ai-governance-and-agent-sprawl",
         "scientists-phd-students-and-postdocs-paying-for-ai-subscriptions",
         "amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot",
         "ceos-ai-impact-on-ops-culture-and-commercial-strategy",
         "frontier-lab-researchers-archives-teaching-models",
         "us-dealer-principals-gms-and-group-leaders-ai-dealership-ops",
         "project-delivery-innovators-tech-leadership-and-procurement-ideas",
         "individual-contributors-managing-ai-agents-without-title-or-pay"]
for c in cands:
    hits = []
    for d in digests:
        t = open(d, errors="ignore").read()
        if c in t:
            hits.append(os.path.basename(d).replace("digest-","").replace(".json",""))
    print(f"{c}: {len(hits)} -> {hits}")

print("\n=== WINDOW CHECK: are prior-queue slugs still in sitemap window? ===")
scan = json.load(open(f"{D}/_scan_0915.json"))
slugs_all = set(scan["ai"]) | set(scan["strict"]) | set(scan["third_ai"])
for c in cands:
    print(c, "in 2026-09-02+ window:", c in slugs_all, "| lastmod:", scan["ai"].get(c) or scan["strict"].get(c) or scan["third_ai"].get(c))
