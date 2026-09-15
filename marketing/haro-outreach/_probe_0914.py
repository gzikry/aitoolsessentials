#!/usr/bin/env python3
"""Probe every non-Sourcee journalist-request platform for the 2026-09-14 run."""
import subprocess, json

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def probe(url, extra=None):
    cmd = ["curl","-sL","-m","30","-A",UA,"-o","/tmp/probe_body.html","-w",
           "%{http_code}|%{size_download}|%{url_effective}"]
    if extra: cmd += extra
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True)
    body = ""
    try: body = open("/tmp/probe_body.html", errors="ignore").read()
    except Exception: pass
    t = ""
    m = body.lower().find("<title>")
    if m >= 0:
        e = body.lower().find("</title>", m)
        t = body[m+7:e].strip()[:120] if e > 0 else body[m+7:m+150].strip()[:120]
    return {"url": url, "status": r.stdout.strip(), "title": t,
            "checkpoint": "Vercel Security Checkpoint" in body or "vercel" in body[:3000].lower() and "checkpoint" in body.lower(),
            "journo_request_refs": body.lower().count("journo-request")}

TARGETS = [
    "https://www.helpareporter.com/",
    "https://www.helpareporter.com/view-queries",
    "https://www.connectively.us/",
    "https://www.connectively.us/queries",
    "https://www.sourceofsources.com/",
    "https://www.sourceofsources.com/requests",
    "https://app.qwoted.com/requests",
    "https://mentionmatch.com/",
    "https://www.mentionmatch.com/",
    "https://medialyst.ai/api/mcp",
    "https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns",
]

res = []
for u in TARGETS:
    try:
        res.append(probe(u))
    except Exception as ex:
        res.append({"url": u, "error": str(ex)})
    print(res[-1])

json.dump(res, open("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/_probe_0914.json","w"), indent=2)
print("wrote _probe_0914.json")
