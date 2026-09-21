#!/usr/bin/env python3
"""2026-09-21 sitemap pull + new-slug window, same method as the 09-20 run.

Pulls /sitemap-journo-requests.xml fresh, records every loc/lastmod pair, and computes how many
slugs carry a lastmod newer than the previous run's newest. Reports how many of those carry an AI
token and how many carry both an AI token and a strict pricing/cost token - the two counts that
decide whether there is anything worth fetching.
"""
import json
import re
import subprocess
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
SITEMAP = "https://www.sourcee.app/sitemap-journo-requests.xml"
MARK = "2026-09-20T03:58:40"          # newest lastmod seen by the 2026-09-20 run

AI = re.compile(r"(?<![a-z])(ai|llm|chatgpt|claude|copilot|agentic|artificial.intelligence)(?![a-z])", re.I)
STRICT = re.compile(r"(pricing|price|subscription|cost|costs|spend|budget|credit|seat|licen[cs]e|"
                    r"renewal|procurement|invoice|billing|expense|reimburse|vendor|per.seat|per.user|"
                    r"monthly|overlap|consolidat|waste|stack|tier)", re.I)


def curl(url):
    r = subprocess.run(["curl", "-sL", "-m", "90", "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


code, xml = curl(SITEMAP)
pairs = re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", xml)
slugs = [(u.rstrip("/").split("/journo-request/")[-1], lm) for u, lm in pairs]
slugs = [(s, lm) for s, lm in slugs if s and "/" not in s]
slugs.sort(key=lambda x: x[1], reverse=True)

window = [p for p in slugs if p[1] > MARK]
ai = [p for p in window if AI.search(p[0].replace("-", " "))]
strict = [p for p in ai if STRICT.search(p[0].replace("-", " "))]

out = {"http": code, "bytes": len(xml), "count": len(slugs),
       "newest": slugs[0][1] if slugs else None, "mark": MARK,
       "pairs": slugs[:120], "window": window, "ai": ai, "strict": strict,
       "ai_all_3day": [p for p in slugs[:400] if AI.search(p[0].replace("-", " "))][:40]}
(D / "_sitemap_0921.json").write_text(json.dumps(out, indent=1))
(D / "_window_0921.json").write_text(json.dumps(out, indent=1))

print(f"HTTP {code}  {len(xml):,} bytes  {len(slugs):,} loc/lastmod pairs")
print(f"newest lastmod: {out['newest']}   mark: {MARK}")
print(f"newer than mark: {len(window)}   with AI token: {len(ai)}   AI+strict: {len(strict)}")
print("\n-- new slugs with an AI token --")
for s, lm in ai:
    print(f"  {lm}  {'STRICT' if STRICT.search(s.replace('-', ' ')) else '      '}  {s}")
print("\n-- any other new slug carrying a strict spend token --")
for s, lm in window:
    if STRICT.search(s.replace("-", " ")) and s not in [a[0] for a in ai]:
        print(f"  {lm}  {s}")
