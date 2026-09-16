import subprocess, re, json, sys, time
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")

SLUGS = [
    "finops-professionals-agentic-ai-cost-overruns",
    "amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot",
    "enterprise-ai-leaders-ai-governance-and-agent-sprawl",
    "scientists-phd-students-and-postdocs-paying-for-ai-subscriptions",
    "ceos-ai-impact-on-ops-culture-and-commercial-strategy",
    "enterprise-ai-leaders-value-creation-ownership-and-governance",
    "edtech-product-managers-lms-audit-does-product-manage-learning",
    "employees-hiding-knowledge-from-workplace-ai-want-pay-for-ai-data",
    "individual-contributors-managing-ai-agents-without-title-or-pay",
    "us-founders-calls-to-slow-ai-development-impact-on-companies",
    "cybersecurity-companies-and-experts-ai-scams-and-consumer-safety",
    "ukraine-tech-builders-and-global-observers-commercial-tech-adaptation",
    "ai-saas-users-in-production-integrations-and-autonomous-workflows",
    "sme-owners-operational-challenges-for-ai-solutions-case-study",
    "earlystage-founders-building-saas-and-ai-tools-built-from-scratch",
    "ai-agents-making-money-2026-sales-and-leadgen-workflow-ops",
    "msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends",
    "uk-finance-risk-and-regulatory-leaders-ai-explainability-risks",
]

# The single request's own record sits in the RSC payload as an object containing "headline"
# and "domain"/"platforms"/"is_live". Isolate the object that owns the headline we fetched.
OBJ_RE = re.compile(r'\{[^{}]*?"headline"[^{}]*?\}')


def unesc(s):
    return (s.replace('\\\\"', '"').replace('\\"', '"').replace("\\n", " ")
             .replace("\\u0026", "&").replace("\\/", "/").strip())


def get(raw, key):
    for pat in (r'\\"' + key + r'\\":\\"((?:[^"\\]|\\.)*?)\\"', r'"' + key + r'":"((?:[^"\\]|\\.)*?)"'):
        m = re.search(pat, raw)
        if m:
            return unesc(m.group(1))
    return None


def get_bool(raw, key):
    for pat in (r'\\"' + key + r'\\":(true|false)', r'"' + key + r'":(true|false)'):
        m = re.search(pat, raw)
        if m:
            return m.group(1) == "true"
    return None


out = {}
for sl in SLUGS:
    url = f"https://www.sourcee.app/journo-request/{sl}"
    raw = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url], capture_output=True, text=True).stdout
    rec = {
        "url": url,
        "headline": get(raw, "headline"),
        "datePublished": get(raw, "datePublished"),
        "domain": get(raw, "domain"),
        "is_live": get_bool(raw, "is_live"),
    }
    # Find the platforms array nearest the headline occurrence.
    idx = raw.find(unesc(rec["headline"])[:40]) if rec["headline"] else -1
    seg = raw[max(0, idx - 6000): idx + 6000] if idx > 0 else raw
    plats = re.findall(r'\\"display_name\\":\\"([^\\"]{2,40})\\"', seg)
    rec["platforms_near"] = sorted(set(plats))[:12]
    out[sl] = rec
    print(f"{sl[:60]:<62} live={rec['is_live']} domain={rec['domain']!r} pub={rec['datePublished']}")
    if rec["platforms_near"]:
        print("     platforms:", rec["platforms_near"])
    time.sleep(1)

(D / "_meta_0916.json").write_text(json.dumps(out, indent=1))
