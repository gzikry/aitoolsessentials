#!/usr/bin/env python3
"""Read the two spend-token slugs from the last 3 days that are not already recorded.

Both matched a spend token but carry no AI token, so they are the class of request the slug filter
routinely misses. Fetching them is the only way to know whether they are on-beat.
"""
import json
import re
import subprocess
import time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = D / "_bodies_0921.json"

CANDS = [
    "sales-enablement-saas-tools-proposal-and-deck-engagement-tracking",
    "companies-that-stopped-emailing-pdfs-new-tools-and-transition",
]


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
            "datePublished": field(raw, "datePublished"), "badge": badge.group(1) if badge else None,
            "domain": field(raw, "domain"), "author": field(raw, "name"),
            "email_redacted": bool(re.search(r"email redacted", core, re.I)),
            "emails_on_page": sorted(set(e for e in re.findall(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core) if "sourcee" not in e.lower())),
            "links": sorted(set(u for u in re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,150}", raw)
                                if not any(c in u for c in ("sourcee.app", "vercel", "sentry", "schema.org",
                                                            "w3.org", "gstatic", "supabase.co", "nextjs.org"))))[:8],
            "core": core[:2600]}


bodies = json.loads(OUT.read_text()) if OUT.exists() else {}
for i, sl in enumerate(CANDS):
    if (bodies.get(sl) or {}).get("core"):
        continue
    rec = probe(sl)
    bodies[sl] = rec
    OUT.write_text(json.dumps(bodies, indent=1))
    print(f"\n=== [{i}] {rec['http']} {rec['badge']} | {rec['datePublished']} | domain={rec['domain']} "
          f"| author={rec['author']}")
    print("HEADLINE:", rec["headline"])
    print("EMAILS:", rec["emails_on_page"], "| redacted:", rec["email_redacted"])
    print("LINKS:", rec["links"])
    print("BODY:", rec["core"][:1400])
    time.sleep(1)
