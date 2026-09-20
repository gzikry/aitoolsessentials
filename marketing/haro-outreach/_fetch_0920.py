#!/usr/bin/env python3
"""2026-09-20 candidate fetch + broader spend-token sweep of the recent sitemap window.

The slug filter can only see tokens in the slug, so it missed the shadow-AI and Raconteur
requests on previous runs. This run does both: read every new AI-token slug, and read every
slug from the last 3 days carrying any spend token even without an AI token.
"""
import json
import re
import subprocess
import time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = D / "_bodies_0920.json"

SPEND = re.compile(r"(\$\s?\d|\u00a3\s?\d|\d+\s?(?:usd|dollars?|bucks)|/\s?month|per\s+month|per\s+seat|"
                   r"per\s+user|a\s+month|monthly|pricing|price[sd]?\b|cost|costs|subscri|budget|credit[s]?\b|"
                   r"spend|spending|billing|invoice|renewal|overlap|consolidat|licen[cs]e|seat[s]?\b|tier|"
                   r"reimburse|expense|paywall|fee[s]?\b|expensive|cheaper|afford|out.of.pocket|"
                   r"procurement|vendor|renew|waste|duplicate|stack|subscription|paying|pay for)", re.I)
AI = re.compile(r"(?<![a-z])(ai|llm|chatgpt|claude|copilot|agentic|artificial.intelligence)(?![a-z])", re.I)


def field(raw, key):
    for pat in (r'"' + key + r'":\s*"((?:[^"\\]|\\.)*?)"',
                r'\\+"' + key + r'\\+":\\+"((?:[^"\\]|\\.)*?)\\+"'):
        m = re.search(pat, raw)
        if m:
            v = m.group(1)
            for _ in range(3):
                n = v.replace("\\n", " ").replace("\\u0026", "&").replace("\\/", "/")
                n = re.sub(r"\\(.)", r"\1", n)
                if n == v:
                    break
                v = n
            return v.strip()
    return None


def curl(url):
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


def probe(sl):
    url = f"https://www.sourcee.app/journo-request/{sl}"
    code, raw = curl(url)
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    core = m.group(1).strip() if m else ""
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
    return {"slug": sl, "url": url, "http": code, "headline": field(raw, "headline"),
            "datePublished": field(raw, "datePublished"),
            "badge": badge.group(1) if badge else None, "author": field(raw, "name"),
            "domain": field(raw, "domain"),
            "email_redacted": bool(re.search(r"email redacted", core, re.I)),
            "emails_on_page": sorted(set(e for e in re.findall(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core) if "sourcee" not in e.lower())),
            "links": sorted(set(u for u in re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,140}", raw)
                                if not any(c in u for c in ("sourcee.app", "vercel", "sentry", "schema.org",
                                                            "w3.org", "gstatic", "supabase.co", "nextjs.org"))))[:8],
            "core": core[:3000],
            "spend_tokens": sorted(set(x.group(0).lower().strip() for x in SPEND.finditer(core)))}


sw = json.loads((D / "_window_0920.json").read_text())
cands = [s for s, _ in sw["ai"]]
# broader sweep: anything in the whole 3-day window carrying a spend token
for s, lm in sw["window"]:
    if lm > "2026-09-17T04:00:00" and SPEND.search(s.replace("-", " ")) and s not in cands:
        cands.append(s)
print(f"candidates: {len(cands)}")

bodies = json.loads(OUT.read_text()) if OUT.exists() else {}
for i, sl in enumerate(cands):
    if (bodies.get(sl) or {}).get("core"):
        continue
    rec = probe(sl)
    bodies[sl] = rec
    OUT.write_text(json.dumps(bodies, indent=1))
    print(f"[{i}] {rec['http']} {str(rec['badge']):<21} tok={len(rec['spend_tokens']):<2} "
          f"ai={'Y' if AI.search(rec['core']) else 'n'} {str(rec['domain'])[:20]:<22} "
          f"{str(rec['headline'])[:52]}", flush=True)
    time.sleep(1)

print(f"\nfetched {len(bodies)}")
for sl, r in bodies.items():
    if r["spend_tokens"]:
        print(f"\n=== {sl} [{r['datePublished']}] {r['domain']} tok={len(r['spend_tokens'])}")
        print("   ", " ".join(r["spend_tokens"][:25]))
