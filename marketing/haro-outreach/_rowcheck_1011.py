#!/usr/bin/env python3
"""2026-10-11 page check for the two rows the report turns on, read off the pages themselves."""
import re
import subprocess
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
ROWS = {
    "mims": "https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks",
    "finops": "https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns",
    "anthro": "https://www.sourcee.app/journo-request/anthropic-gtm-leaders-scaling-300k-b2b-clients",
    "hrjobs": "https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring",
    "cyber": "https://www.sourcee.app/journo-request/ai-cybersecurity-iot-and-web3-founders-and-operators-news-submissions",
}

for name, url in ROWS.items():
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, url], capture_output=True, text=True)
    raw = r.stdout
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    flat = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    core = re.search(r"Start free trial (.*?)Brought to you by Sourcee", flat, re.S)
    txt = core.group(1).strip() if core else ""
    dp = re.search(r'"datePublished":"([^"]+)"', raw)
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", txt)
    author = re.search(r'"name":"([^"]{2,60})"', raw)
    print(f"=== {name} {url}")
    print(f"    http_code_ok={len(raw)>20000} bytes={len(raw)} datePublished={dp.group(1) if dp else None}")
    print(f"    badge={badge.group(1) if badge else None} author={author.group(1) if author else None}")
    print(f"    text={txt[:520]}")
    Path(f"/tmp/row_{name}.txt").write_text(txt)
    print()
