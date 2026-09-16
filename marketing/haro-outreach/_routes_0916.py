import subprocess, re, json, time
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")

SLUGS = [
    "finops-professionals-agentic-ai-cost-overruns",
    "enterprise-ai-leaders-ai-governance-and-agent-sprawl",
    "amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot",
    "individual-contributors-managing-ai-agents-without-title-or-pay",
    "employees-hiding-knowledge-from-workplace-ai-want-pay-for-ai-data",
    "us-founders-calls-to-slow-ai-development-impact-on-companies",
    "cybersecurity-companies-and-experts-ai-scams-and-consumer-safety",
    "ukraine-tech-builders-and-global-observers-commercial-tech-adaptation",
    "enterprise-ai-leaders-value-creation-ownership-and-governance",
]

SKIP = ("sourcee.app", "vercel", "sentry", "nextjs.org", "schema.org", "w3.org",
        "gstatic", "fonts.googleapis", "supabase.co", "redditstatic", "preview.redd.it",
        "linkedin.com/in/andrewsmith313", "x.com/andy_cb_smith")

out = {}
for sl in SLUGS:
    url = f"https://www.sourcee.app/journo-request/{sl}"
    raw = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url], capture_output=True, text=True).stdout
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"\s+", " ", txt).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    core = m.group(1).strip() if m else txt

    urls = sorted(set(re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,160}", raw)))
    links = [u for u in urls if not any(s in u for s in SKIP)]
    # short links and handles visible in the rendered body
    handles = sorted(set(re.findall(r"@[A-Za-z0-9_]{3,20}", core)))
    emails_core = [e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core) if "sourcee" not in e.lower()]
    redacted = bool(re.search(r"email redacted", core, re.I))
    out[sl] = {"url": url, "links": links, "handles": handles, "emails_in_body": emails_core,
               "email_redacted": redacted, "core": core[:1500]}
    print("=" * 100)
    print(sl)
    print("  links:", links[:8])
    print("  handles:", handles[:8], "| emails:", emails_core, "| redacted:", redacted)
    time.sleep(1)

(D / "_routes_0916.json").write_text(json.dumps(out, indent=1))
