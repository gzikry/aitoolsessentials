#!/usr/bin/env python3
"""Fetch and read the new AI-token slugs from today's window, in full."""
import json
import re
import subprocess
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

win = json.loads((D / "_window_0924.json").read_text())
slugs = [s for s, _ in win["ai"]] + [s for s, _ in win["spend_any"] if s not in [a[0] for a in win["ai"]]]

import time


def curl(url, timeout=30):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


def visible(raw):
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"\s+", " ", txt).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    return (m.group(1).strip() if m else "")


bodies = {}
for s in slugs:
    url = f"https://www.sourcee.app/journo-request/{s}"
    code, raw = curl(url)
    core = visible(raw)
    dp = re.search(r'"datePublished":\s*"([^"]+)"', raw)
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
    bodies[s] = {"url": url, "http": code, "datePublished": dp.group(1) if dp else None,
                 "badge": badge.group(1) if badge else None, "body": core}
    print(f"\n=== {s}  HTTP {code}  {dp.group(1) if dp else '?'}  {badge.group(1) if badge else ''}")
    print(core[:1400])
    time.sleep(1)

(D / "_newbodies_0924.json").write_text(json.dumps(bodies, indent=1))
print(f"\nwrote _newbodies_0924.json with {len(bodies)} bodies")
