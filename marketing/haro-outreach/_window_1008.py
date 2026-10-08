#!/usr/bin/env python3
"""2026-10-08 window probe: pull today's sitemap, measure the new-slug window since the
2026-10-07 run, and probe every platform once.

Same measurement as _window_1007.py. Mark = newest lastmod of the 2026-10-07 pull
(2026-10-07T03:00:43.149Z).
"""
import json
import re
import subprocess
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

MARK = "2026-10-07T03:00:43.149Z"
TODAY = "2026-10-08"
AI = re.compile(r"(^|[-/])(ai|a-i|llm|gpt|chatgpt|claude|gemini|copilot|agents?|machine-learning|automation|ml)([-/]|$)", re.I)
SPEND = re.compile(r"(pricing|prices?|price|cost|costs|spend|spending|budget|budgets|subscription|subscriptions|"
                   r"saas|licen[cs]e|seat|seats|billing|invoice|credits|procurement|roi|pay|paid|afford)", re.I)
REAL_SPEND = re.compile(r"(?<![a-z])(pricing|prices?|costs?|spend(?:ing)?|budgets?|subscriptions?|saas|"
                        r"licen[cs]es?|seats?|billing|invoices?|credits|procurement|roi|afford)(?![a-z])",
                        re.I)


def curl(url, timeout=90):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


code, xml = curl("https://www.sourcee.app/sitemap-journo-requests.xml")
(D / f"_sitemap_{TODAY.replace('-', '')[4:]}.xml").write_text(xml)
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
FP = [(s, toks) for s, _lm, toks in ai_strict if not REAL_SPEND.search(s)]

feed_code, feed_raw = curl("https://www.sourcee.app/topics/ai/journo-requests")
feed_slugs = []
for s in re.findall(r"/journo-request/([a-z0-9\-]{5,160})", feed_raw):
    if s not in feed_slugs:
        feed_slugs.append(s)
win_set = {s for s, _ in window}

out = {
    "today": TODAY,
    "sitemap_http": code, "bytes": len(xml), "count": len(slugs), "newest": newest, "mark": MARK,
    "window": window, "ai": ai, "ai_strict": ai_strict, "spend_any": spend_any,
    "ai_strict_false_positives": FP,
    "feed_count": len(feed_slugs), "feed_http": feed_code, "feed_bytes": len(feed_raw),
    "feed_overlap_with_window": len([s for s in feed_slugs if s in win_set]),
    "feed_slugs": feed_slugs,
}

PLATFORMS = [
    ("Sourcee (sourcee.app)", "https://www.sourcee.app/"),
    ("Sourcee AI topic feed", "https://www.sourcee.app/topics/ai/journo-requests"),
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
    pcode, raw = curl(url, 40)
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    plats.append({"platform": name, "url": url, "http": pcode, "bytes": len(raw),
                  "title": (title.group(1).strip()[:120] if title else ""),
                  "checkpoint": "Vercel Security Checkpoint" in raw})
out["platforms"] = plats

(D / f"_window_{TODAY.replace('-', '')[4:]}.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: (len(v) if isinstance(v, list) and k not in ("feed_slugs",) else v)
                  for k, v in out.items() if k not in ("platforms", "feed_slugs")}, indent=1))
print("--- AI-Token window slugs ---")
for s, lm in ai:
    print(f"  {lm}  {s}")
print("--- AI+spend (with matched tokens) ---")
for s, lm, toks in ai_strict:
    print(f"  {lm}  {s}   tokens={toks}")
print("--- strict hits judged false positives ---")
for s, toks in FP:
    print(f"  {s}   tokens={toks}")
print("--- spend-any window slugs ---")
for s, lm in spend_any:
    print(f"  {s}   {lm}")
print("--- platforms ---")
for p in plats:
    print(f"  {p['http']:>4} {p['bytes']:>8} {p['platform']:<40} {p['title'][:60]}  ckpt={p['checkpoint']}")
print("--- feed ---")
print(f"  {len(feed_slugs)} slugs; overlap with window {out['feed_overlap_with_window']}")
