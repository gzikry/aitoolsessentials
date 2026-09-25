#!/usr/bin/env python3
"""Fetch and read every AI-token / spend-token slug in today's window, in full."""
import json
import re
import subprocess
import time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

win = json.loads((D / "_window_0925.json").read_text())
seen = []
for s, _ in win["ai"]:
    seen.append(s)
for s, _ in win["spend_any"]:
    if s not in seen:
        seen.append(s)


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
for s in seen:
    url = f"https://www.sourcee.app/journo-request/{s}"
    code, raw = curl(url)
    core = visible(raw)
    dp = re.search(r'"datePublished":\s*"([^"]+)"', raw)
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
    emails = sorted(set(e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core)
                        if "sourcee" not in e.lower()))
    links = sorted(set(u for u in re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,160}", raw)
                       if not any(c in u for c in ("sourcee.app", "vercel", "sentry", "nextjs", "schema.org",
                                                   "w3.org", "gstatic", "google.com/s2", "supabase"))))
    bodies[s] = {"url": url, "http": code, "datePublished": dp.group(1) if dp else None,
                 "badge": badge.group(1) if badge else None, "body": core,
                 "emails": emails, "redacted": bool(re.search(r"email redacted", core, re.I)),
                 "links": links[:6], "headline": (re.search(r'"headline":\s*"([^"]+)"', raw) or [None, ""])[1]}
    print(f"\n=== {s}  HTTP {code}  {bodies[s]['datePublished']}  {bodies[s]['badge']}")
    print(core[:1500])
    time.sleep(1)

(D / "_newbodies_0925.json").write_text(json.dumps(bodies, indent=1))
print(f"\nwrote _newbodies_0925.json with {len(bodies)} bodies")
