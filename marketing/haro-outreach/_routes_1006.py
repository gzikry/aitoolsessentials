#!/usr/bin/env python3
"""2026-10-06 route resolution: check the reply routes the drafts will cite, by fetching them."""
import re
import subprocess

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

TARGETS = [
    ("ZDNET lnkd.in route (Ritoban Mukherjee Qwoted post)", "https://lnkd.in/dVu9JK4C"),
    ("Raconteur /contributors/simon-chandler", "https://www.raconteur.net/contributors/simon-chandler"),
    ("Raconteur control /contributors/tom-dennis", "https://www.raconteur.net/contributors/tom-dennis"),
    ("Raconteur legacy /author/simon-chandler/", "https://www.raconteur.net/author/simon-chandler/"),
    ("Speciality Food /contact", "https://www.specialityfoodmagazine.com/contact"),
    ("Grist author page /staff/jake-bittle", "https://grist.org/staff/jake-bittle/"),
]


def curl(url, timeout=40):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA,
                        "-w", "\n__HTTP__%{http_code}__|%{url_effective}", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\|(\S*)\s*$", raw)
    return (m.group(1) if m else "000"), (m.group(2) if m else ""), (raw[:raw.rfind("__HTTP__")] if m else raw)


for label, url in TARGETS:
    code, eff, raw = curl(url)
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    emails = sorted(set(e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)
                        if not any(x in e.lower() for x in ("sentry", "wixpress", "example", ".png", ".jpg"))))[:8]
    print("=" * 100)
    print(f"{label}\n  {url}\n  HTTP {code} | {len(raw)} bytes | effective {eff}")
    print(f"  title: {title.group(1).strip()[:110] if title else ''}")
    print(f"  emails: {emails}")
