import subprocess, re, json, time

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
D = "/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach"

slugs = [
    "finops-professionals-agentic-ai-cost-overruns",
    "amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot",
    "employees-hiding-knowledge-from-workplace-ai-want-pay-for-ai-data",
    "individual-contributors-managing-ai-agents-without-title-or-pay",
    "enterprise-ai-leaders-ai-governance-and-agent-sprawl",
    "cybersecurity-companies-and-experts-ai-scams-and-consumer-safety",
    "us-founders-calls-to-slow-ai-development-impact-on-companies",
    "ai-startups-workplace-fraud-detection-expenses-time-theft",
]

out = {}
for sl in slugs:
    url = f"https://www.sourcee.app/journo-request/{sl}"
    raw = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url], capture_output=True, text=True).stdout
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"\s+", " ", txt).strip()
    # cut the Sourcee chrome: keep from the headline marker to the "Brought to you by Sourcee" footer
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    core = m.group(1).strip() if m else txt
    out[sl] = {"url": url, "core": core, "badge": (re.search(r"(Posted [^<]{0,30})", txt) or [None])[0] if False else None}
    print("=" * 100)
    print(sl)
    print(core[:1800])
    print()
    time.sleep(1)

json.dump(out, open(f"{D}/_bodies_visible_0916.json", "w"), indent=1)
