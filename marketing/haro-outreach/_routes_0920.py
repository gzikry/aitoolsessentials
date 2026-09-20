#!/usr/bin/env python3
"""2026-09-20 route re-verification.

Three routes were resolved by hand across earlier runs. A route that was right on 2026-09-19 is
not evidence it is right today, and a draft is only paste-ready if the address still exists. Each
route is re-fetched from the page that published it, and the MX is re-checked against DNS.
"""
import re
import subprocess

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def curl(url, timeout=30):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, "-w", "\n__HTTP__%{http_code}__", url],
                       capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


print("=" * 90)
print("1. RACONTEUR — simon.chandler@raconteur.net (obfuscated data-part triple on byline page)")
for u in ("https://www.raconteur.net/author/simon-chandler/",
          "https://www.raconteur.net/author/ian-deering/"):
    code, raw = curl(u)
    triples = re.findall(r'data-part1="([^"]*)"\s+data-part2="([^"]*)"\s+data-part3="([^"]*)"', raw)
    triples += re.findall(r'data-part1=\\?"([^"\\]*)\\?"[^>]{0,80}?data-part2=\\?"([^"\\]*)\\?"'
                          r'[^>]{0,80}?data-part3=\\?"([^"\\]*)\\?"', raw)
    parts = re.findall(r'data-part([123])=["\\]?([^"\\>\s]+)', raw)
    print(f"  {code} {u}  bytes={len(raw)}  triples={triples}  parts={parts[:9]}")

print()
print("=" * 90)
print("2. SPECIALITY FOOD — holly.shackleton@artichokehq.com (named on /contact)")
for u in ("https://www.specialityfoodmagazine.com/contact", "https://www.artichokehq.com/contact"):
    code, raw = curl(u)
    txt = re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I))
    txt = re.sub(r"\s+", " ", txt)
    emails = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", txt)))
    hit = re.search(r".{120}holly\.shackleton.{160}", txt, re.I)
    print(f"  {code} {u}  bytes={len(raw)}  emails={emails[:12]}")
    if hit:
        print("   context:", hit.group(0).strip()[:290])

print()
print("=" * 90)
print("3. ANTHROPIC REQUEST — Signal handle re-read off the live request page")
code, raw = curl("https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences")
body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
core = m.group(1).strip() if m else ""
sig = re.findall(r"Signal\s+([A-Za-z0-9._\-]{3,40})", core)
print(f"  {code} bytes={len(raw)}  signal={sig}")
print("   core:", core[:420])

print()
print("=" * 90)
print("4. MX re-check")
for dom in ("raconteur.net", "artichokehq.com", "forbes.com"):
    out = subprocess.run(["dig", "+short", "MX", dom], capture_output=True, text=True).stdout.strip()
    print(f"  {dom:<18} {out.splitlines()[:3]}")
