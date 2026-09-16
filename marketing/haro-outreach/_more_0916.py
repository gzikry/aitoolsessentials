import subprocess, re, json, time
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")

SLUGS = ["ai-agents-making-money-2026-sales-and-leadgen-workflow-ops",
         "uk-managers-cracked-down-on-gen-z-ai-overuse",
         "marketing-and-content-leaders-aiassisted-work-review-process",
         "earlystage-founders-building-saas-and-ai-tools-built-from-scratch",
         "tech-policy-experts-california-ai-audit-bills-impact-cios",
         "anthropic-users-and-business-owners-customer-service-experiences"]

for sl in SLUGS:
    url = f"https://www.sourcee.app/journo-request/{sl}"
    raw = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url], capture_output=True, text=True).stdout
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"\s+", " ", txt).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    core = m.group(1).strip() if m else ""
    dom = re.search(r'\\"domain\\":\\"([^"\\]+)', raw)
    links = [u for u in sorted(set(re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,140}", raw)))
             if not any(s in u for s in ("sourcee", "vercel", "sentry", "nextjs", "schema.org", "w3.org",
                                         "gstatic", "google.com/s2", "supabase", "redditstatic",
                                         "andrewsmith313", "andy_cb_smith"))]
    print("=" * 100)
    print(sl, "| domain:", dom.group(1) if dom else None)
    print("links:", links[:6])
    print(core[:900])
    print()
    time.sleep(1)
