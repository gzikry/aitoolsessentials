import subprocess, re, json
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
OUT = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach/platforms_0916.json")

targets = [
    ("HARO", "https://www.helpareporter.com/issues/"),
    ("HARO home", "https://www.helpareporter.com/"),
    ("Connectively", "https://www.connectively.us/"),
    ("Connectively queries", "https://www.connectively.us/queries"),
    ("Qwoted app", "https://app.qwoted.com/requests"),
    ("Qwoted www", "https://www.qwoted.com/"),
    ("Source of Sources", "https://www.sourceofsources.com/"),
    ("Source of Sources requests", "https://www.sourceofsources.com/requests"),
    ("MentionMatch", "https://mentionmatch.com/"),
    ("MentionMatch www", "https://www.mentionmatch.com/"),
    ("Medialyst MCP", "https://medialyst.ai/api/mcp"),
    ("Sourcee AI topic", "https://www.sourcee.app/topics/ai/journo-requests"),
    ("Sourcee sitemap", "https://www.sourcee.app/sitemap-journo-requests.xml"),
]

res = {}
for name, url in targets:
    r = subprocess.run(["curl", "-sL", "-m", "25", "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    code = m.group(1) if m else "000"
    body = raw[:raw.rfind("__HTTP__")] if m else raw
    title = re.search(r"<title>(.*?)</title>", body, re.S)
    res[name] = {
        "url": url, "http": code, "bytes": len(body),
        "title": title.group(1).strip()[:90] if title else None,
        "checkpoint": bool(re.search(r"Security Checkpoint|Vercel", body, re.I)),
        "has_feed": bool(re.search(r"journo-request|query|request", body, re.I)),
    }
    print(f"{code:<4} {len(body):>8}B {name:<26} {str(res[name]['title'])[:60]}"
          f"{' [CHECKPOINT]' if res[name]['checkpoint'] else ''}")

# X credits via the platform's own signal is not reachable from cron; record prior state.
OUT.write_text(json.dumps(res, indent=1))
print("\nwrote", OUT)
