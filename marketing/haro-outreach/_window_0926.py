#!/usr/bin/env python3
"""Build today's new-slug window from the freshly pulled sitemap, and probe the platforms.

Same measurement the 2026-09-20..2026-09-25 runs used:
  * window = slugs whose lastmod is newer than the previous run's mark
  * ai      = window slugs carrying an AI token
  * ai_strict = window slugs carrying an AI token AND a spend token
  * spend_any = window slugs carrying any spend-adjacent token
  * feed    = Sourcee's own /topics/ai/journo-requests listing, measured for overlap
"""
import json
import re
import subprocess
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

MARK = "2026-09-25T03:40:59.000Z"          # newest lastmod of the 2026-09-25 pull
AI = re.compile(r"(^|[-/])(ai|a-i|llm|gpt|chatgpt|claude|gemini|copilot|agents?|machine-learning|automation|ml)([-/]|$)", re.I)
SPEND = re.compile(r"(pricing|prices?|price|cost|costs|spend|spending|budget|budgets|subscription|subscriptions|"
                   r"saas|licen[cs]e|seat|seats|billing|invoice|credits|procurement|roi|pay|paid|afford)", re.I)


def curl(url, timeout=40):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


xml = (D / "_sitemap_0926.xml").read_text(errors="ignore")
pairs = re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", xml)
slugs = []
for loc, lm in pairs:
    if "/journo-request/" in loc:
        slugs.append((loc.rstrip("/").split("/journo-request/")[-1], lm))
newest = max(lm for _, lm in slugs)
window = [(s, lm) for s, lm in slugs if lm > MARK]
ai = [(s, lm) for s, lm in window if AI.search(s)]
ai_strict = [(s, lm, [t for t in SPEND.findall(s)]) for s, lm in ai if SPEND.search(s)]
spend_any = [(s, lm) for s, lm in window if SPEND.search(s)]

feed_code, feed_raw = curl("https://www.sourcee.app/topics/ai/journo-requests")
feed_slugs = []
for s in re.findall(r"/journo-request/([a-z0-9\-]{5,160})", feed_raw):
    if s not in feed_slugs:
        feed_slugs.append(s)
win_set = {s for s, _ in window}

out = {
    "http": "200", "bytes": len(xml), "count": len(slugs), "newest": newest, "mark": MARK,
    "window": window, "ai": ai, "ai_strict": ai_strict, "spend_any": spend_any,
    "feed_count": len(feed_slugs), "feed_http": feed_code,
    "feed_overlap_with_window": len([s for s in feed_slugs if s in win_set]),
}

# Platform probes — one attempt each, no retries.
PLATFORMS = [
    ("Sourcee (sourcee.app)", "https://www.sourcee.app/"),
    ("HARO (helpareporter.com)", "https://www.helpareporter.com/"),
    ("Connectively (connectively.us)", "https://www.connectively.us/"),
    ("Source of Sources (sourceofsources.com)", "https://sourceofsources.com/requests"),
    ("Qwoted (qwoted.com)", "https://app.qwoted.com/requests"),
    ("MentionMatch (mentionmatch.com)", "https://mentionmatch.com/"),
    ("Medialyst MCP (medialyst.ai/api/mcp)", "https://medialyst.ai/api/mcp"),
    ("ResponseSource (responsesource.com)", "https://www.responsesource.com/"),
]
plats = []
for name, url in PLATFORMS:
    code, raw = curl(url)
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    plats.append({"platform": name, "url": url, "http": code, "bytes": len(raw),
                  "title": (title.group(1).strip()[:120] if title else ""),
                  "checkpoint": "Vercel Security Checkpoint" in raw})
out["platforms"] = plats

(D / "_window_0926.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in out.items() if k != "platforms"}, indent=1))
print("--- AI-Token window slugs ---")
for s, lm in ai:
    print(f"  {lm}  {s}")
print("--- AI+spend (with matched tokens) ---")
for s, lm, toks in ai_strict:
    print(f"  {lm}  {s}   tokens={toks}")
print("--- spend-any window slugs ---")
for s, lm in spend_any:
    print(f"  {lm}  {s}")
print("--- platforms ---")
for p in plats:
    print(f"  {p['http']:>4} {p['bytes']:>8} {p['platform']:<40} {p['title'][:60]}")
