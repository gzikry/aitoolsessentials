#!/usr/bin/env python3
"""Probe access status for each journalist-request platform."""
import subprocess, re, json

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

TARGETS = [
    ("HARO root", "https://www.helpareporter.com/"),
    ("HARO queries", "https://www.helpareporter.com/view-queries"),
    ("Connectively root", "https://www.connectively.us/"),
    ("Connectively queries", "https://www.connectively.us/queries"),
    ("Source of Sources root", "https://www.sourceofsources.com/"),
    ("Source of Sources reqs", "https://www.sourceofsources.com/requests"),
    ("Qwoted requests", "https://app.qwoted.com/requests"),
    ("MentionMatch root", "https://www.mentionmatch.com/"),
    ("MentionMatch reqs", "https://www.mentionmatch.com/requests"),
    ("Medialyst MCP", "https://medialyst.ai/api/mcp"),
    ("Sourcee health", "https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns"),
]


def probe(name, url):
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, "-o", "/tmp/p.html",
                        "-w", "%{http_code}|%{size_download}|%{time_total}", url],
                       capture_output=True, text=True)
    meta = r.stdout.strip()
    body = ""
    try:
        body = open("/tmp/p.html", encoding="utf-8", errors="replace").read()
    except Exception as e:
        body = "READFAIL " + str(e)
    low = body.lower()
    flags = []
    if "vercel security checkpoint" in low:
        flags.append("VERCEL_CHECKPOINT")
    if "just a moment" in low or "cf-chl" in low or "cloudflare" in low:
        flags.append("CLOUDFLARE?")
    if "invalid_token" in low:
        flags.append("OAUTH_401")
    if "edit with" in low and "lovable" in low:
        flags.append("LOVABLE_SHELL")
    if "page not found" in low and "404" in meta:
        flags.append("404")
    m = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
    title = re.sub(r"\s+", " ", m.group(1)).strip()[:70] if m else ""
    return {"platform": name, "url": url, "code_size_time": meta,
            "title": title, "flags": flags, "bytes": len(body)}


out = []
for n, u in TARGETS:
    try:
        out.append(probe(n, u))
    except Exception as e:
        out.append({"platform": n, "url": u, "error": str(e)})

for o in out:
    print(json.dumps(o))
json.dump(out, open("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/_probe2.json", "w"), indent=1)
