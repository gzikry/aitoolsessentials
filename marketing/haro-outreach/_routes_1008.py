#!/usr/bin/env python3
"""2026-10-08 route re-verification for the draft rows + the new Google/Claude row's prospects."""
import re
import subprocess

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def curl(url, timeout=40):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


TARGETS = [
    ("Mims LinkedIn", "https://www.linkedin.com/in/christopher-mims-club/"),
    ("Raconteur simon.chandler contributor", "https://raconteur.net/contributors/simon-chandler"),
    ("Raconteur tom.dennis control", "https://raconteur.net/contributors/tom-dennis"),
    ("Raconteur legacy /author/simon-chandler/", "https://raconteur.net/author/simon-chandler/"),
    ("Speciality Food contact", "https://www.specialityfoodmagazine.com/contact"),
]
for name, url in TARGETS:
    code, raw = curl(url)
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    print(f"{code:>4}  {len(raw):>8} bytes  {name}")
    print(f"       title: {(title.group(1).strip()[:90] if title else '')}")
    if "simon-chandler" in url:
        for i in (1, 2, 3):
            m = re.findall(rf'data-part{i}="([^"]*)"', raw)
            print(f"       data-part{i}: {m[:4]}")
        print("       'simon.chandler' present:", "simon.chandler" in raw)
    if "tom-dennis" in url:
        print("       'tom.dennis' present:", "tom.dennis" in raw)
    if "specialityfoodmagazine" in url:
        emails = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)))
        print("       emails:", emails[:12])
