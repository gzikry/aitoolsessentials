#!/usr/bin/env python3
"""Read every slug in today's new-sitemap window that carries an AI token or a spend token.

Purpose: the digest's "0 new on-beat" claim must not rest on slug tokens alone. Each candidate is
fetched and its rendered body read in full, so a request with an on-beat *subject* under a
non-matching slug is caught, and every false positive (e.g. 'seat' inside 'Seattle') is visible
rather than only appearing as a missing count.
"""
import json
import re
import subprocess
import time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = D / "_newbodies_0926.json"
win = json.loads((D / "_window_0926.json").read_text())
CANDS = []
for s, _lm in win["ai"] + win["spend_any"]:
    if s not in CANDS:
        CANDS.append(s)


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


def probe(sl):
    url = f"https://www.sourcee.app/journo-request/{sl}"
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    code = m.group(1) if m else "000"
    raw = raw[:raw.rfind("__HTTP__")] if m else raw
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    mm = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    core = mm.group(1).strip() if mm else ""
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
    return {"slug": sl, "url": url, "http": code, "badge": badge.group(1) if badge else None,
            "datePublished": field(raw, "datePublished"), "domain": field(raw, "domain"),
            "author": field(raw, "name"), "email_redacted": bool(re.search(r"email redacted", core, re.I)),
            "emails_on_page": sorted(set(e for e in re.findall(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core) if "sourcee" not in e.lower())),
            "core": core[:1600]}


bodies = json.loads(OUT.read_text()) if OUT.exists() else {}
for sl in CANDS:
    if (bodies.get(sl) or {}).get("core"):
        continue
    rec = probe(sl)
    bodies[sl] = rec
    OUT.write_text(json.dumps(bodies, indent=1))
    print(f"\n=== {rec['http']} | {rec['badge']} | {rec['datePublished']} | {rec['author']} "
          f"| {rec['domain']} | emails={rec['emails_on_page']}")
    print(rec["core"][:900])
    time.sleep(1)
