#!/usr/bin/env python3
"""2026-10-06: resolve the Christopher Mims route off his own byline pages (not the request page)."""
import re
import subprocess

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

TARGETS = [
    ("Muck Rack - Christopher Mims", "https://muckrack.com/christopher-mims"),
    ("WSJ author page /news/author/christopher-mims", "https://www.wsj.com/news/author/christopher-mims"),
    ("LinkedIn handle (may 999)", "https://www.linkedin.com/in/christopher-mims-club/"),
    ("WSJ contact /help/contact-us", "https://www.wsj.com/help/contact-us"),
    ("Grist staff index", "https://grist.org/staff/"),
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
                        if not any(x in e.lower() for x in ("sentry", "wixpress", "example", ".png", ".jpg",
                                                            "schema.org"))))[:10]
    mims = [l for l in re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,120}", raw)
            if "mims" in l.lower()][:6]
    print("=" * 100)
    print(f"{label}\n  {url}\n  HTTP {code} | {len(raw)} bytes | effective {eff}")
    print(f"  title: {title.group(1).strip()[:110] if title else ''}")
    print(f"  emails: {emails}")
    if mims:
        print(f"  mims-links: {mims}")
