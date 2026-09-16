import subprocess, re, json
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")

for sl in ("finops-professionals-agentic-ai-cost-overruns", "us-founders-calls-to-slow-ai-development-impact-on-companies"):
    url = f"https://www.sourcee.app/journo-request/{sl}"
    raw = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url], capture_output=True, text=True).stdout
    Path(f"/tmp/raw_{sl[:20]}.txt").write_text(raw)
    print("=" * 100)
    print(sl, len(raw), "bytes ->", f"/tmp/raw_{sl[:20]}.txt")
    # every occurrence of 'domain' with surrounding context
    for m in re.finditer(r'.{260}domain.{260}', raw, re.S):
        print("---- DOMAIN CTX ----")
        print(m.group(0).replace("\n", " ")[:560])
        print()
