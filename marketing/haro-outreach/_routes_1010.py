#!/usr/bin/env python3
"""2026-10-10 route re-verification for the draft rows, the carried sendable row, and the
NEWLY RESOLVED Glenn Hansen route.

Writes marketing/haro-outreach/route-checks-2026-10-10.json, which
scripts/build_pitch_queue.py reads (newest route-checks-*.json) for its DRAFTS prose.

New this run: the Glenn Hansen route.  The request page publishes no route, but the author
names himself in the page's own author field and states he reports on power equipment
manufacturing.  That identifies him as Glenn Hansen, editor of OPE+ (EPG Brand Acceleration),
and OPE+ publishes his address on its own site: 'Glenn Hansen, Editor - ghansen@epgacceleration.com'
on /2024/02/13/announcing-ope/19236, with the same editorial domain named on /contact-us.
"""
import json
import re
import subprocess
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")


def curl(url, timeout=40):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


TARGETS = [
    ("linkedin.com/in/christopher-mims-club/", "Mims LinkedIn byline page",
     "https://www.linkedin.com/in/christopher-mims-club/"),
    ("ope-plus.com/2024/02/13/announcing-ope/19236", "OPE+ 'Announcing OPE+' - carries the editor's address",
     "https://ope-plus.com/2024/02/13/announcing-ope/19236"),
    ("ope-plus.com/contact-us", "OPE+ contact page - editorial domain",
     "https://ope-plus.com/contact-us"),
    ("raconteur.net/contributors/simon-chandler", "Raconteur simon.chandler contributor",
     "https://raconteur.net/contributors/simon-chandler"),
    ("raconteur.net/contributors/tom-dennis", "Raconteur tom.dennis control",
     "https://raconteur.net/contributors/tom-dennis"),
    ("raconteur.net/author/simon-chandler/", "Raconteur legacy /author/simon-chandler/",
     "https://raconteur.net/author/simon-chandler/"),
    ("specialityfoodmagazine.com/contact", "Speciality Food contact",
     "https://www.specialityfoodmagazine.com/contact"),
]

out = {"checked": "2026-10-10", "routes": {}}
for key, label, url in TARGETS:
    code, raw = curl(url)
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    rec = {"label": label, "url": url, "http": code, "bytes": len(raw),
           "title": (title.group(1).strip()[:90] if title else "")}
    if "simon-chandler" in url or "tom-dennis" in url:
        parts = [re.findall(rf'data-part{i}="([^"]*)"', raw)[:4] for i in (1, 2, 3)]
        if parts[0]:
            rec["triple"] = "+".join(p[0] for p in parts if p)
    if "ope-plus.com" in url:
        rec["emails"] = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)))[:12]
        rec["ghansen_present"] = "ghansen@epgacceleration.com" in raw
    if "specialityfoodmagazine" in url:
        rec["emails"] = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)))[:12]
    out["routes"][key] = rec
    print(f"{code:>4}  {len(raw):>8} bytes  {label}  {rec.get('triple', '')}  "
          f"ghansen={rec.get('ghansen_present')}  {rec['title'][:50]}")

(D / "route-checks-2026-10-10.json").write_text(json.dumps(out, indent=1))
print("wrote route-checks-2026-10-10.json")
