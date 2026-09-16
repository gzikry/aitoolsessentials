import subprocess, re, json, time
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")

SLUGS = [
    "finops-professionals-agentic-ai-cost-overruns",
    "amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot",
    "enterprise-ai-leaders-ai-governance-and-agent-sprawl",
    "employees-hiding-knowledge-from-workplace-ai-want-pay-for-ai-data",
    "individual-contributors-managing-ai-agents-without-title-or-pay",
    "us-founders-calls-to-slow-ai-development-impact-on-companies",
    "enterprise-ai-leaders-value-creation-ownership-and-governance",
    "ai-startups-workplace-fraud-detection-expenses-time-theft",
    "scientists-phd-students-and-postdocs-paying-for-ai-subscriptions",
    "ceos-ai-impact-on-ops-culture-and-commercial-strategy",
]

for sl in SLUGS:
    url = f"https://www.sourcee.app/journo-request/{sl}"
    raw = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url], capture_output=True, text=True).stdout
    # Un-escape the whole RSC payload into plain JSON text, then find the request object.
    flat = raw.replace('\\"', '"').replace("\\\\", "\\")
    # find the object that has BOTH headline and (platforms or source_url or url)
    best = None
    for m in re.finditer(r'\{[^{}]{0,4000}?"headline"[^{}]{0,4000}?\}', flat):
        seg = m.group(0)
        if sl[:25] in seg or "headline" in seg:
            best = seg
            break
    print("=" * 100)
    print(sl)
    if best:
        # print only non-body fields of interest
        for key in ("headline", "datePublished", "domain", "is_live", "platforms", "platform",
                    "source_url", "source", "url", "author", "publication", "deadline",
                    "display_name", "link", "permalink", "origin"):
            for mm in re.finditer(r'"' + key + r'"\s*:\s*("(?:[^"\\]|\\.)*"|\[[^\]]{0,400}\]|true|false|null|\d+)', best):
                v = mm.group(1)
                print(f"   {key} = {v[:300]}")
    else:
        print("   no object matched; dumping platform-ish context")
        for mm in re.finditer(r'"platforms"\s*:\s*(\[[^\]]{0,600}\])', flat):
            print("   platforms:", mm.group(1)[:400])
    time.sleep(1)
