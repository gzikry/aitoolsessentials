#!/usr/bin/env python3
"""Robust same-tier monthly/annual pair extraction from data/pricing_snapshots.json.

Why: the range "1.21x-2.53x" is about to be cited in a pitch that a journalist will read. A strict
one-directional regex finds 7 pairs; the 2026-09-18 ledger recorded 9. Both cannot be right, and a
range whose lower bound moves with the regex is not a figure worth publishing. This handles both
phrasings ("X billed annually or Y billed monthly" and "$A/month or $B/month billed annually") and
prints every pair with its plan context so each end of the range can be read off a page.
"""
import json
import re
import statistics
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
snaps = json.loads((S / "data" / "pricing_snapshots.json").read_text())["snapshots"]

# a money figure with an optional unit suffix, then a term word
NUM = r"\$\s?(\d[\d,]*(?:\.\d+)?)\s*(?:USD\s*)?(?:/\s*(?:user|seat|member|person|editor|month|mo)\s*)*"
ANN = r"(?:billed\s+)?annual|per\s+year|/\s*year|annually"
MON = r"monthly|/\s*month|per\s+month|a\s+month"

pairs = []
for slug, v in snaps.items():
    d = " ".join((v.get("digest") or "").split())
    # split into clause-ish chunks on . ; so plan context stays near its numbers
    for chunk in re.split(r"(?<=[.;])\s+", d):
        if not re.search(ANN, chunk, re.I):
            continue
        nums = [(float(m.group(1).replace(",", "")), m.start(), m.group(0)) for m in re.finditer(NUM, chunk)]
        if len(nums) < 2:
            continue
        # find an annual-tagged figure and a monthly-tagged figure in the same clause
        ann = [n for n in nums if re.search(ANN, chunk[max(0, n[1] - 40):n[1] + 60], re.I)
               and not re.search(MON, chunk[n[1] + len(n[2]):n[1] + len(n[2]) + 12], re.I)]
        mon = [n for n in nums if re.search(MON, chunk[max(0, n[1] - 40):n[1] + 60], re.I)
               and not re.search(ANN, chunk[n[1] + len(n[2]):n[1] + len(n[2]) + 12], re.I)]
        if len(ann) == 1 and len(mon) == 1:
            a, m = ann[0][0], mon[0][0]
            if a > 0 and m > 0 and m != a:
                lo, hi = min(a, m), max(a, m)
                pairs.append((hi / lo, slug, lo, hi, chunk[:150], v.get("date")))

pairs.sort()
print(f"candidate pairs: {len(pairs)}\n")
for r, slug, lo, hi, ctx, dt in pairs:
    print(f"{r:5.2f}x  {slug:<16} ${lo:g} vs ${hi:g}  ({dt})")
    print(f"        {ctx}")

vals = [p[0] for p in pairs if p[0] > 1.0]
if vals:
    print(f"\npairs with a real gap (>1.0x): {len(vals)}")
    print(f"range : {min(vals):.2f}x ({pairs[[p[0] for p in pairs].index(min([v for v in vals]))][1]}) "
          f"to {max(vals):.2f}x")
    print(f"median: {statistics.median(vals):.2f}x")
    print(f"above 1.8x: {sum(1 for v in vals if v > 1.8)}")
