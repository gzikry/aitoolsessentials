#!/usr/bin/env python3
"""Re-resolve the two crossed-but-sendable reply routes against the live pages, today.

Raconteur: the byline address is assembled by the site's own JS from data-part1/2/3 on
/contributors/<slug>. The older /author/<slug>/ URL 404s and must not be cited. Control author
/contributors/tom-dennis must still carry tom.dennis/raconteur/net or the triplet read is suspect.
Speciality Food: the masthead address is read off specialityfoodmagazine.com/contact.
"""
import re
import subprocess

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def curl(url, timeout=45):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


def parts(raw):
    return {k: (re.search(r'data-part' + k + r'="([^"]*)"', raw) or [None, None])[1]
            for k in ("1", "2", "3")}


for label, url in [
    ("Raconteur Simon Chandler (live byline)", "https://www.raconteur.net/contributors/simon-chandler"),
    ("Raconteur control Tom Dennis", "https://www.raconteur.net/contributors/tom-dennis"),
    ("Raconteur LEGACY /author/simon-chandler/ (must 404)", "https://www.raconteur.net/author/simon-chandler/"),
    ("Speciality Food contact page", "https://www.specialityfoodmagazine.com/contact"),
]:
    code, raw = curl(url)
    p = parts(raw)
    emails = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)))
    print(f"{code:>4} {len(raw):>8}  {label}")
    if any(p.values()):
        print(f"      parts: {p}")
    if emails and "speciality" in url:
        print(f"      addresses on page: {emails}")
    print()
