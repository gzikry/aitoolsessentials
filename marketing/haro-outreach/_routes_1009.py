#!/usr/bin/env python3
"""2026-10-09 route re-verification for the draft rows + the carried sendable row.

Writes marketing/haro-outreach/route-checks-2026-10-09.json, which
scripts/build_pitch_queue.py reads (newest route-checks-*.json) for its DRAFTS prose.
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
    ("raconteur.net/contributors/simon-chandler", "Raconteur simon.chandler contributor",
     "https://raconteur.net/contributors/simon-chandler"),
    ("raconteur.net/contributors/tom-dennis", "Raconteur tom.dennis control",
     "https://raconteur.net/contributors/tom-dennis"),
    ("raconteur.net/author/simon-chandler/", "Raconteur legacy /author/simon-chandler/",
     "https://raconteur.net/author/simon-chandler/"),
    ("specialityfoodmagazine.com/contact", "Speciality Food contact",
     "https://www.specialityfoodmagazine.com/contact"),
]

out = {"checked": "2026-10-09", "routes": {}}
for key, label, url in TARGETS:
    code, raw = curl(url)
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    rec = {"label": label, "url": url, "http": code, "bytes": len(raw),
           "title": (title.group(1).strip()[:90] if title else "")}
    if "simon-chandler" in url and "author" not in url:
        parts = [re.findall(rf'data-part{i}="([^"]*)"', raw)[:4] for i in (1, 2, 3)]
        if parts[0]:
            rec["triple"] = "+".join(p[0] for p in parts if p)
    if "tom-dennis" in url:
        parts = [re.findall(rf'data-part{i}="([^"]*)"', raw)[:4] for i in (1, 2, 3)]
        if parts[0]:
            rec["triple"] = "+".join(p[0] for p in parts if p)
    if "specialityfoodmagazine" in url:
        rec["emails"] = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)))[:12]
    out["routes"][key] = rec
    print(f"{code:>4}  {len(raw):>8} bytes  {label}  {rec.get('triple','')}  {rec['title'][:50]}")

(D / "route-checks-2026-10-09.json").write_text(json.dumps(out, indent=1))
print("wrote route-checks-2026-10-09.json")
