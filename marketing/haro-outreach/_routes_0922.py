#!/usr/bin/env python3
"""2026-09-22 route + figure re-verification for the three sendable rows.

Re-verifies, from the live pages rather than from yesterday's notes:
  1. Raconteur byline triple for simon.chandler (data-part1/2/3) + a control author.
  2. Speciality Food contact page for holly.shackleton@artichokehq.com + the named masthead.
  3. The Anthropic request page's own words on the Signal handle.
  4. MX records for the two resolved mail domains.
  5. The figures each draft cites, recomputed from data/tools.json and
     data/pricing_snapshots.json with each value's own snapshot date.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

SITE = Path("/Users/georgezikry/aitoolessentials/site")
D = SITE / "marketing" / "haro-outreach"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def curl(url, timeout=40):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA,
                        "-w", "\n__HTTP__%{http_code}__", url], capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


print("=" * 78)
print("1. RACONTEUR BYLINE ROUTE  (simon.chandler@raconteur.net)")
print("=" * 78)
for slug, who in (("simon-chandler", "target"), ("tom-dennis", "control")):
    code, raw = curl(f"https://www.raconteur.net/contributors/{slug}")
    trip = re.findall(r'data-part1="([^"]*)"\s+data-part2="([^"]*)"\s+data-part3="([^"]*)"', raw)
    print(f"{slug:<16} HTTP {code}  {len(raw):>8,} bytes  triple={trip}")
    if trip:
        a, b, c = trip[0]
        print(f"                 -> {a}@{b}.{c}")
    print(f"                 old /author/{slug}/ = HTTP {curl(f'https://www.raconteur.net/author/{slug}/')[0]}")

print()
print("=" * 78)
print("2. SPECIALITY FOOD CONTACT ROUTE  (holly.shackleton@artichokehq.com)")
print("=" * 78)
code, raw = curl("https://www.specialityfoodmagazine.com/contact")
body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
emails = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", txt)))
print(f"HTTP {code}  {len(raw):,} bytes")
print("masthead addresses:", emails)
print("holly present:", any("shackleton" in e.lower() for e in emails))
i = txt.lower().find("shackleton")
print("context:", txt[max(0, i - 120):i + 90] if i >= 0 else "NOT FOUND")

print()
print("=" * 78)
print("3. ANTHROPIC REQUEST PAGE — the Signal handle, in the page's own words")
print("=" * 78)
code, raw = curl("https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences")
body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
core = m.group(1).strip() if m else ""
print(f"HTTP {code}")
print("BODY:", core[:900])
print("signal token present:", "hliwrites" in core.lower())

print()
print("=" * 78)
print("4. MX RECORDS")
print("=" * 78)
for dom in ("raconteur.net", "artichokehq.com"):
    r = subprocess.run(["dig", "+short", "MX", dom], capture_output=True, text=True)
    print(f"{dom:<18} {r.stdout.strip().replace(chr(10), ' | ')}")

print()
print("=" * 78)
print("5. FIGURES CITED BY THE DRAFTS")
print("=" * 78)
tools = json.loads((SITE / "data" / "tools.json").read_text())
print("tools.json records:", len(tools))

snap = json.loads((SITE / "data" / "pricing_snapshots.json").read_text())
print("pricing_snapshots.json keys:", len(snap), "| sample:", list(snap)[:3])
k0 = list(snap)[0]
print("sample record:", json.dumps(snap[k0], indent=1)[:500])
