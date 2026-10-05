#!/usr/bin/env python3
"""2026-10-05: try to resolve a reply route for the best live requests off the PUBLICATION's
own site, and re-verify the two carried routes. One attempt each, no retries.
"""
import re
import subprocess
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def curl(url, timeout=40):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


TARGETS = [
    ("CNBC author Lindsay Dodgson", "https://www.cnbc.com/lindsay-dodgson/"),
    ("CNBC author alt", "https://www.cnbc.com/author/lindsay-dodgson/"),
    ("CIPD people Katie Jacobs", "https://www.cipd.org/uk/about/people/katie-jacobs/"),
    ("CIPD contact", "https://www.cipd.org/uk/about/contact-us/"),
    ("Raconteur contributors simon-chandler", "https://www.raconteur.net/contributors/simon-chandler"),
    ("Raconteur control tom-dennis", "https://www.raconteur.net/contributors/tom-dennis"),
    ("Speciality Food contact", "https://www.specialityfoodmagazine.com/contact"),
]
for name, url in TARGETS:
    code, raw = curl(url)
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    emails = sorted(set(e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)
                        if "sourcee" not in e.lower()))
    triples = re.findall(r'data-part1=\\?"([^"\\]+)\\?"[^>]*data-part2=\\?"([^"\\]+)\\?"[^>]*data-part3=\\?"([^"\\]+)\\?"', raw)
    if not triples:
        triples = re.findall(r'data-part1="([^"]+)"[^>]*data-part2="([^"]+)"[^>]*data-part3="([^"]+)"', raw)
    title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    print("=" * 90)
    print(f"{name}\n  url: {url}\n  HTTP {code}  bytes {len(raw)}  title: {(title.group(1).strip()[:90] if title else '')}")
    print(f"  emails: {emails[:12]}")
    print(f"  data-part triples: {triples}")
    # pull any 'contact' contexts
    for m in re.finditer(r"(.{60}(?:contact|email|reach|press|journalist).{60})", txt, re.I):
        s = m.group(1).strip()
        print("   ctx:", s[:180])
