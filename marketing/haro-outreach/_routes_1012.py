#!/usr/bin/env python3
"""2026-10-12 route re-verification: the sendable row's route and dead ends, plus the carried
Raconteur / Speciality Food / OPE+ routes that build_pitch_queue.py's DRAFTS prose names.

Writes marketing/haro-outreach/route-checks-2026-10-12.json in the DICT shape that
scripts/build_pitch_queue.py's _route_evidence() reads. The 2026-10-11 probe wrote the same file
as a LIST of {row, route, ...}, which crashed the queue build this morning with
`'list' object has no attribute 'get'`; the reader now accepts both shapes (see the
monitor_defects_fixed_this_run note in digest-2026-10-12.json), and this probe stays on the shape
every probe before yesterday used.
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
    # The one live route in the whole queue: the sendable row's LinkedIn DM.
    ("linkedin.com/in/christopher-mims-club/", "Mims LinkedIn byline page",
     "https://www.linkedin.com/in/christopher-mims-club/"),
    # Dead ends, re-checked so they stay recorded as dead rather than re-tried as routes.
    ("muckrack.com/christopher-mims", "Mims Muck Rack profile (recorded dead end)",
     "https://www.muckrack.com/christopher-mims"),
    ("wsj.com/news/author/christopher-mims", "Mims WSJ author page (recorded dead end)",
     "https://www.wsj.com/news/author/christopher-mims"),
    # Routes named in the DRAFTS prose for carried rows that are cold but not dropped.
    ("raconteur.net/contributors/simon-chandler", "Raconteur simon.chandler contributor",
     "https://raconteur.net/contributors/simon-chandler"),
    ("raconteur.net/contributors/tom-dennis", "Raconteur tom.dennis control",
     "https://raconteur.net/contributors/tom-dennis"),
    ("raconteur.net/author/simon-chandler/", "Raconteur legacy /author/simon-chandler/",
     "https://raconteur.net/author/simon-chandler/"),
    ("specialityfoodmagazine.com/contact", "Speciality Food contact",
     "https://www.specialityfoodmagazine.com/contact"),
]

out = {"checked": "2026-10-12", "routes": {}}
for key, label, url in TARGETS:
    code, raw = curl(url)
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    rec = {"label": label, "url": url, "http": code, "bytes": len(raw),
           "title": (title.group(1).strip()[:90] if title else "")}
    if "simon-chandler" in url or "tom-dennis" in url:
        parts = [re.findall(rf'data-part{i}="([^"]*)"', raw)[:4] for i in (1, 2, 3)]
        if parts[0]:
            rec["triple"] = "+".join(p[0] for p in parts if p)
    if "specialityfoodmagazine" in url:
        rec["emails"] = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)))[:12]
    out["routes"][key] = rec
    print(f"{code:>4}  {len(raw):>8} bytes  {label}  {rec.get('triple', '')}  {rec['title'][:50]}")

(D / "route-checks-2026-10-12.json").write_text(json.dumps(out, indent=1))
print("wrote route-checks-2026-10-12.json")
