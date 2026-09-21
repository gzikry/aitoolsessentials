#!/usr/bin/env python3
"""Deterministic same-tier monthly/annual pair extraction, printed in full for hand-inspection.

The range "1.21x-2.53x" has been cited in two pitches and appears in the queue. Three different
regexes over the same file produce 9, 7 and 2 pairs, which means the range is a property of the
pattern rather than of the data. Any figure going into a pitch has to survive that, so this prints
every tool whose snapshot digest mentions both a monthly and an annual term, with the sentence, so
the pairs can be counted off the text rather than inferred from a match count.
"""
import json
import re
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
snaps = json.loads((S / "data" / "pricing_snapshots.json").read_text())["snapshots"]

ANN = re.compile(r"(billed annually|per year|/year|annually|annual)", re.I)
MON = re.compile(r"(monthly|/month|per month|a month)", re.I)
MONEY = re.compile(r"\$\s?(\d[\d,]*(?:\.\d+)?)")

print("tool           date        monthly$   annual$   ratio   sentence")
print("-" * 118)
hits = []
for slug, v in sorted(snaps.items()):
    d = " ".join((v.get("digest") or "").split())
    if not (ANN.search(d) and MON.search(d)):
        continue
    # every sentence that carries BOTH terms is a candidate pair sentence
    for sent in re.split(r"(?<=[.;])\s+", d):
        if not (ANN.search(sent) and MON.search(sent)):
            continue
        nums = [float(m.group(1).replace(",", "")) for m in MONEY.finditer(sent)]
        if len(nums) < 2:
            continue
        lo, hi = min(nums), max(nums)
        ratio = hi / lo if lo > 0 else 0
        print(f"{slug:<14} {v.get('date'):<11} {lo:<10g} {hi:<9g} {ratio:<7.2f} {sent[:70]}")
        hits.append((slug, v.get("date"), lo, hi, ratio, sent))

print("-" * 118)
ratios = sorted({round(h[4], 2) for h in hits if h[0] > 0})
print(f"distinct ratios across candidate sentences: {ratios}")
print(f"count of candidate sentences: {len(hits)}")

# the only defensible way to state it: pairs where BOTH terms are quoted in one clause
print("\n--- strict one-clause, both terms with own figure ---")
STRICT = re.findall(
    r"\$\s?(\d[\d,]*(?:\.\d+)?)\s*(?:/\s*(?:user|seat|member|person|editor)\s*)?(?:/\s*month|per month|monthly)"
    r"[^.$;]{0,50}?\$\s?(\d[\d,]*(?:\.\d+)?)\s*(?:/\s*(?:user|seat|member|person|editor)\s*)?"
    r"(?:/\s*month|per month|monthly)?\s*(?:billed\s+)?annual", " ".join(
        " ".join((v.get("digest") or "").split()) for v in snaps.values()), re.I)
out = []
for a, b in STRICT:
    x, y = float(a.replace(",", "")), float(b.replace(",", ""))
    if y > 0 and x != y:
        out.append((max(x, y) / min(x, y), min(x, y), max(x, y)))
out.sort()
print(f"n = {len(out)}")
for r, lo, hi in out:
    print(f"  {r:.2f}x  ${lo:g} vs ${hi:g}")
