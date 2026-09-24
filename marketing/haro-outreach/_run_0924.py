#!/usr/bin/env python3
"""2026-09-24 platform probes + fresh sitemap pull, same method as the 09-23 run.

Records per-platform status first (the task requires the status of each platform to be recorded),
then pulls /sitemap-journo-requests.xml fresh and computes the new-slug window against the newest
lastmod the 2026-09-23 run saw (2026-09-23T02:13:14.000Z).
"""
import json
import re
import subprocess
import time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
SITEMAP = "https://www.sourcee.app/sitemap-journo-requests.xml"
MARK = "2026-09-23T02:13:14"          # newest lastmod seen by the 2026-09-23 run

AI = re.compile(r"(?<![a-z])(ai|llm|chatgpt|claude|copilot|agentic|artificial.intelligence)(?![a-z])", re.I)
STRICT = re.compile(r"(pricing|price|subscription|cost|costs|spend|budget|credit|seat|licen[cs]e|"
                    r"renewal|procurement|invoice|billing|expense|reimburse|vendor|per.seat|per.user|"
                    r"monthly|overlap|consolidat|waste|stack|tier|saas|software|tool)", re.I)

PLATFORMS = [
    ("Sourcee (sourcee.app)", "https://www.sourcee.app/"),
    ("HARO (helpareporter.com)", "https://www.helpareporter.com/"),
    ("Connectively (connectively.us)", "https://www.connectively.us/"),
    ("Source of Sources (sourceofsources.com)", "https://www.sourceofsources.com/requests"),
    ("Qwoted (qwoted.com)", "https://app.qwoted.com/requests"),
    ("MentionMatch (mentionmatch.com)", "https://mentionmatch.com/"),
    ("Medialyst MCP (medialyst.ai)", "https://medialyst.ai/api/mcp"),
    ("ResponseSource (responsesource.com)", "https://www.responsesource.com/"),
]


def curl(url, timeout=30):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


plat = []
for name, url in PLATFORMS:
    code, raw = curl(url)
    title = re.search(r"<title[^>]*>([^<]{0,140})", raw)
    plat.append({"platform": name, "url": url, "http": code, "bytes": len(raw),
                 "title": (title.group(1).strip() if title else None),
                 "checkpoint": "Vercel Security Checkpoint" in raw})
    print(f"{code}  {len(raw):>9,}b  {name:<42} {(title.group(1)[:60] if title else '')}")

# AI topic feed window (rolling recency window, not persistence)
fcode, fraw = curl("https://www.sourcee.app/topics/ai/journo-requests", 40)
feed_slugs = []
for s in re.findall(r"/journo-request/([a-z0-9\-]{5,160})", fraw):
    if s not in feed_slugs:
        feed_slugs.append(s)
(D / "ai-topic-feed.json").write_text(json.dumps(
    {"captured": "2026-09-24", "http": fcode, "count": len(feed_slugs), "slugs": feed_slugs}, indent=1))
print(f"\nAI topic feed: HTTP {fcode}, {len(feed_slugs)} slugs")

code, xml = curl(SITEMAP, 90)
pairs = re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", xml)
slugs = [(u.rstrip("/").split("/journo-request/")[-1], lm) for u, lm in pairs]
slugs = [(s, lm) for s, lm in slugs if s and "/" not in s]
slugs.sort(key=lambda x: x[1], reverse=True)

window = [p for p in slugs if p[1] > MARK]
ai = [p for p in window if AI.search(p[0].replace("-", " "))]
strict = [p for p in ai if STRICT.search(p[0].replace("-", " "))]
spend_any = [p for p in window if STRICT.search(p[0].replace("-", " "))]

out = {"http": code, "bytes": len(xml), "count": len(slugs),
       "newest": slugs[0][1] if slugs else None, "mark": MARK,
       "window": window, "ai": ai, "ai_strict": strict, "spend_any": spend_any,
       "feed_count": len(feed_slugs), "feed_http": fcode,
       "feed_overlap_with_window": len(set(s for s, _ in window) & set(feed_slugs)),
       "platforms": plat}
(D / "_window_0924.json").write_text(json.dumps(out, indent=1))
(D / "_sitemap_0924.json").write_text(json.dumps(out, indent=1))

print(f"\nHTTP {code}  {len(xml):,} bytes  {len(slugs):,} loc/lastmod pairs")
print(f"newest lastmod: {out['newest']}   mark: {MARK}")
print(f"newer than mark: {len(window)}   with AI token: {len(ai)}   AI+strict: {len(strict)}")
print(f"feed overlap with window: {out['feed_overlap_with_window']} of {len(feed_slugs)}")
print("\n-- new slugs with an AI token --")
for s, lm in ai:
    print(f"  {lm}  {'STRICT' if STRICT.search(s.replace('-', ' ')) else '      '}  {s}")
print("\n-- other new slugs carrying any spend token --")
for s, lm in spend_any:
    if s not in [a[0] for a in ai]:
        print(f"  {lm}  {s}")
