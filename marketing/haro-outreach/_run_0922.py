#!/usr/bin/env python3
"""2026-09-22 platform probes + fresh sitemap pull, same method as the 09-21 run.

Records per-platform status first (the task requires the status of each platform to be recorded),
then pulls /sitemap-journo-requests.xml fresh and computes the new-slug window against the newest
lastmod the 2026-09-21 run saw (2026-09-21T03:04:50).
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
MARK = "2026-09-21T03:04:50"          # newest lastmod seen by the 2026-09-21 run

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
]


def curl(url, timeout=30):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


def title(raw):
    m = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    return re.sub(r"\s+", " ", m.group(1)).strip()[:110] if m else ""


probes = []
for name, url in PLATFORMS:
    code, raw = curl(url)
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    flags = []
    low = txt.lower()
    if "security checkpoint" in low or "vercel" in low and code == "429":
        flags.append("Vercel Security Checkpoint")
    if "429" == code:
        flags.append("rate-limited")
    if "page not found" in low or "404" in title(raw):
        flags.append("genuine 404 (feed path does not exist)")
    if "email redacted" in low:
        flags.append("email redacted")
    rec = {"platform": name, "url": url, "http": code, "bytes": len(raw),
           "title": title(raw), "flags": flags, "text_head": txt[:300]}
    probes.append(rec)
    print(f"{code:<4} {len(raw):>8,}  {name:<42} {title(raw)[:60]}")
    for f in flags:
        print(f"        - {f}")
    time.sleep(0.7)

(D / "_platforms_0922.json").write_text(json.dumps(probes, indent=1))

print("\n--- sitemap ---")
code, xml = curl(SITEMAP, 120)
pairs = re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", xml)
slugs = [(u.rstrip("/").split("/journo-request/")[-1], lm) for u, lm in pairs]
slugs = [(s, lm) for s, lm in slugs if s and "/" not in s]
slugs.sort(key=lambda x: x[1], reverse=True)

window = [p for p in slugs if p[1] > MARK]
ai = [p for p in window if AI.search(p[0].replace("-", " "))]
strict = [p for p in ai if STRICT.search(p[0].replace("-", " "))]
spend_only = [p for p in window if p not in ai and STRICT.search(p[0].replace("-", " "))]

out = {"http": code, "bytes": len(xml), "count": len(slugs),
       "newest": slugs[0][1] if slugs else None, "mark": MARK,
       "pairs": slugs[:150], "window": window, "ai": ai, "strict": strict,
       "spend_only": spend_only,
       "ai_all_3day": [p for p in slugs[:500] if AI.search(p[0].replace("-", " "))][:40]}
(D / "_sitemap_0922.json").write_text(json.dumps(out, indent=1))

print(f"HTTP {code}  {len(xml):,} bytes  {len(slugs):,} loc/lastmod pairs")
print(f"newest lastmod: {out['newest']}   mark: {MARK}")
print(f"newer than mark: {len(window)}   with AI token: {len(ai)}   AI+strict: {len(strict)}")
print("\n-- new slugs with an AI token --")
for s, lm in ai:
    print(f"  {lm}  {'STRICT' if STRICT.search(s.replace('-', ' ')) else '      '}  {s}")
print("\n-- other new slugs carrying a spend/software token --")
for s, lm in spend_only[:60]:
    print(f"  {lm}  {s}")
