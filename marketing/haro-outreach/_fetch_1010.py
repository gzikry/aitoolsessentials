#!/usr/bin/env python3
"""2026-10-10 candidate fetch: read the body of EVERY slug in today's new sitemap window.

The slug-level AI/spend regex returned zero hits this run, so slug matching alone cannot
support the "clean window" claim: a request about Anthropic pricing would carry no AI token
in its slug. Every window slug is therefore fetched and its rendered body scanned for AI and
spend tokens, which is the only check that can back a zero.
"""
import json
import re
import subprocess
import time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = D / "_bodies_1010.json"


def field(raw, key):
    for pat in (r'"' + key + r'":\s*"((?:[^"\\]|\\.)*?)"',
                r'\\+"' + key + r'\\+":\\+"((?:[^"\\]|\\.)*?)\\+"'):
        m = re.search(pat, raw)
        if m:
            v = m.group(1)
            for _ in range(3):
                n = v.replace("\\n", " ").replace("\\u0026", "&").replace("\\/", "/")
                n = re.sub(r'\\(.)', r'\1', n)
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


win = json.loads((D / "_window_1010.json").read_text())
SLUGS = [s for s, _lm in win["window"]]

bodies = json.loads(OUT.read_text()) if OUT.exists() else {}

for i, sl in enumerate(SLUGS):
    if (bodies.get(sl) or {}).get("core"):
        continue
    url = f"https://www.sourcee.app/journo-request/{sl}"
    code, raw = curl(url)
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    core = m.group(1).strip() if m else ""
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
    links = [u for u in sorted(set(re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,160}", raw)))
             if not any(c in u for c in ("sourcee.app", "vercel", "sentry", "nextjs.org", "schema.org",
                                         "w3.org", "gstatic", "google.com/s2", "supabase.co"))]
    rec = {"slug": sl, "url": url, "http": code, "headline": field(raw, "headline"),
           "datePublished": field(raw, "datePublished"),
           "badge": badge.group(1) if badge else None, "author": field(raw, "name"),
           "domain": field(raw, "domain"),
           "email_redacted": bool(re.search(r"email redacted", core, re.I)),
           "emails_on_page": sorted(set(e for e in re.findall(
               r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core) if "sourcee" not in e.lower())),
           "published_links": links[:6],
           "core": core[:4000]}
    bodies[sl] = rec
    OUT.write_text(json.dumps(bodies, indent=1))
    print(f"[{i}] {code} {str(rec['badge']):<21} mail={len(rec['emails_on_page'])} "
          f"{str(rec['domain'])[:24]:<26} {str(rec['headline'])[:60]}", flush=True)
    time.sleep(1)

print("\nfetched", len(bodies), "of", len(SLUGS))
