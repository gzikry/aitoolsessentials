#!/usr/bin/env python3
"""2026-09-20 platform probe: record per-platform status, then pull the Sourcee sitemap.

Cheap and non-repeating: HARO/Connectively are expected to return a Vercel checkpoint and are
probed exactly once each. The real work is the sitemap diff — new slugs indexed since the
2026-09-19 marker, filtered for AI tokens.
"""
import json
import re
import subprocess
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def curl(url, timeout=45):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


PROBES = {
    "HARO": "https://www.helpareporter.com/",
    "Connectively": "https://www.connectively.us/",
    "Source of Sources": "https://sourceofsources.com/requests",
    "Qwoted": "https://app.qwoted.com/requests",
    "MentionMatch": "https://mentionmatch.com/",
    "Medialyst MCP": "https://medialyst.ai/api/mcp",
    "ResponseSource": "https://www.responsesource.com/",
    "Sourcee": "https://www.sourcee.app/",
}

out = {}
for name, url in PROBES.items():
    code, raw = curl(url, 30)
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    out[name] = {"url": url, "http": code, "bytes": len(raw),
                 "title": (title.group(1).strip()[:80] if title else "")}
    print(f"{name:<18} {code} {len(raw):>7}B  {out[name]['title']}", flush=True)

(D / "_probe_0920.json").write_text(json.dumps(out, indent=1))

# --- Sourcee sitemap: the only accessible source ---
code, raw = curl("https://www.sourcee.app/sitemap-journo-requests.xml", 90)
pairs = re.findall(r"<loc>https://www\.sourcee\.app/journo-request/([a-z0-9\-]+)</loc>\s*<lastmod>([^<]+)</lastmod>", raw)
if not pairs:
    pairs = list(zip(re.findall(r"/journo-request/([a-z0-9\-]+)", raw), re.findall(r"<lastmod>([^<]+)</lastmod>", raw)))
newest = max((p[1] for p in pairs), default="")
print(f"\nsitemap: http={code} bytes={len(raw)} pairs={len(pairs)} newest_lastmod={newest}")
(D / "_sitemap_0920.json").write_text(json.dumps({"http": code, "bytes": len(raw),
                                                  "count": len(pairs), "newest": newest,
                                                  "pairs": pairs}, indent=0))

AI = re.compile(r"(?<![a-z])(ai|a\.i\.|artificial.intelligence|llm|chatgpt|claude|copilot|agentic)(?![a-z])", re.I)
STRICT = re.compile(r"(\$\s?\d|£\s?\d|pricing|price[sd]?\b|cost|costs|budget|spend|spending|subscription|"
                    r"overlap|consolidat|procurement|invoice|billing|renewal|credit[s]?|paywall|licen[cs]e|tier|"
                    r"fee[s]?|expensive|cheaper|afford|out.of.pocket|saas|software spend)", re.I)

# Marker: the 2026-09-19 run reported 578 slugs inside the 2026-09-11+ window and newest
# lastmod 2026-09-19T02:27:03Z. Cut everything at or below that stamp as already seen.
MARK = "2026-09-19T02:27:03"
window, ai_slug, both = [], [], []
for slug, lm in pairs:
    if lm > MARK:
        window.append((slug, lm))
        if AI.search(slug.replace("-", " ")):
            ai_slug.append((slug, lm))
            if STRICT.search(slug.replace("-", " ")):
                both.append((slug, lm))
print(f"new since marker {MARK}: {len(window)} slugs; with AI token: {len(ai_slug)}; with strict spend token too: {len(both)}")
for s, lm in sorted(both, key=lambda x: x[1], reverse=True):
    print(f"  STRICT {lm} {s}")
for s, lm in sorted((x for x in ai_slug if x not in both), key=lambda x: x[1], reverse=True)[:20]:
    print(f"  ai     {lm} {s}")
(D / "_window_0920.json").write_text(json.dumps({"mark": MARK, "window": window,
                                                 "ai": ai_slug, "strict": both}, indent=1))
