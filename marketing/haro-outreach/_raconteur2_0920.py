#!/usr/bin/env python3
"""Fetch Raconteur's real contributor page and re-read the obfuscated address triple."""
import re
import subprocess

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def get(url):
    r = subprocess.run(["curl", "-sL", "-m", "35", "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


for u in ("https://www.raconteur.net/contributors/Simon%20Chandler",
          "https://www.raconteur.net/contributors/Simon+Chandler",
          "https://www.raconteur.net/contributors/tom-dennis"):
    code, raw = get(u)
    parts = re.findall(r'data-part([123])=["\\]?([^"\\>\s]+)', raw)
    mailto = sorted(set(re.findall(r"mailto:[^\"'<> ]+", raw)))
    emails = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@raconteur\.net", raw)))
    print(f"{code} {u} bytes={len(raw)}")
    print(f"   parts={parts[:9]}")
    print(f"   mailto={mailto[:5]} emails={emails[:5]}")
    if parts:
        d = {}
        for k, v in parts:
            d.setdefault(k, v)
        if len(d) >= 3:
            print(f"   RECONSTRUCTED = {d['1']}@{d['2']}.{d['3']}")
    # also look for the JS assembler and any inline triple
    js = re.findall(r"(part1[^;]{0,120})", raw)[:3]
    if js:
        print("   js:", js)
    print()
