#!/usr/bin/env python3
"""Read the three slugs from the 2026-09-20/21 sitemap window that are adjacent but carry no AI
token, so the "no AI-token slug" count is not mistaken for "nothing worth reading"."""
import json
import re
import subprocess
import time
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = D / "_bodies_0921b.json"
CANDS = ["founders-and-leaders-mindsets-and-milestones",
         "ml-researchers-continuous-learning-fast-weights-and-adapters",
         "founders-55-latelife-entrepreneurship-series-1",
         "founders-and-entrepreneurs-and-musicians-podcast-guests"]


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
            "core": core[:1200]}


bodies = json.loads(OUT.read_text()) if OUT.exists() else {}
for sl in CANDS:
    if (bodies.get(sl) or {}).get("core"):
        continue
    rec = probe(sl)
    bodies[sl] = rec
    OUT.write_text(json.dumps(bodies, indent=1))
    print(f"\n=== {rec['http']} | {rec['badge']} | {rec['datePublished']} | {rec['author']} "
          f"| {rec['domain']} | emails={rec['emails_on_page']}")
    print(rec["core"][:750])
    time.sleep(1)
