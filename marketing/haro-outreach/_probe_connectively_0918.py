#!/usr/bin/env python3
"""Probe current Connectively access state (gated vs public feed)."""
import subprocess, re, sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

def fetch(url, extra=None):
    cmd = ["curl", "-sL", "-m", "25", "-A", UA, "-w", "\n__HTTP__%{http_code}__SIZE__%{size_download}", url]
    if extra:
        cmd[1:1] = extra
    r = subprocess.run(cmd, capture_output=True, text=True)
    body = r.stdout
    m = re.search(r"__HTTP__(\d+)__SIZE__(\d+)$", body)
    code, size = (m.group(1), m.group(2)) if m else ("?", "?")
    body = re.sub(r"\n__HTTP__.*$", "", body)
    return code, size, body

urls = [
    "https://connectively.us/",
    "https://connectively.us/queries",
    "https://connectively.us/requests",
    "https://connectively.us/signup",
    "https://connectively.us/login",
]
for u in urls:
    code, size, body = fetch(u)
    low = body.lower()
    signals = []
    for k in ["vercel security checkpoint", "just a moment", "cloudflare", "captcha",
              "sign in", "log in", "subscribe", "journalist", "request"]:
        if k in low:
            signals.append(k)
    title = re.search(r"<title>(.*?)</title>", body, re.S)
    print(f"{u}\n  HTTP {code} size={size} title={title.group(1).strip()[:80] if title else None}")
    print(f"  signals: {signals}")
    print()
