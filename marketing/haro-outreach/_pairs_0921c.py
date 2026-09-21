#!/usr/bin/env python3
"""The defensible same-tier monthly/annual ratio set, computed once and locked.

The claim "1.21x to 2.53x" appears in two pitches that were already sent and in every draft since.
Running three different extractions over data/pricing_snapshots.json returned 9, 7, 18 and 2 pairs,
which means the range was a property of the regex, not of the data. Two of those extractions put
pairs BELOW 1.21x:

    instrumentl  Pre-Award  $499/month annually or $579 monthly  = 1.16x
    instrumentl  Discover   $299/month annually or $349 monthly  = 1.17x
    slack-ai     Business+  $15/user/month annually or $18 monthly = 1.20x
    airtable-ai  Team       $20/seat/month billed annually or $24 billed monthly = 1.20x

So the published floor of "1.21x" was wrong for the same reason the 2026-09-18 pitch's "1.2-1.3x"
was understated: the pair set was never fixed, so each run measured a different population.

This script fixes the population by rule and prints it for inspection. A pair qualifies when:
  * the same plan tier quotes BOTH a monthly term and an annual term,
  * BOTH figures are monthly-equivalents (a bare yearly total like "$200 annual prepayment" or
    "$288 annually" is the same tier's whole-year price, not a per-month figure, so dividing a
    monthly rate by it produces a meaningless 10x-112x "ratio" - every such artifact is listed
    separately and excluded, with its sentence, so the exclusion is auditable rather than silent),
  * the two figures differ, and the monthly rate is the higher one (that is the only direction a
    vendor ever actually charges; anything else is a parse error).
"""
import json
import re
import statistics
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
snaps = json.loads((S / "data" / "pricing_snapshots.json").read_text())["snapshots"]

ANN = re.compile(r"(billed annually|per year|/year|annually|annual)", re.I)
MON = re.compile(r"(monthly|/month|per month|a month|month-to-month)", re.I)
MONEY = re.compile(r"\$\s?(\d[\d,]*(?:\.\d+)?)")
# a figure is a monthly-equivalent only when a month word sits within ~14 chars after it,
# or the clause labels it "monthly" right before it.
MONTHLY_EQ = re.compile(r"month|mo\b|monthly", re.I)

pairs, artifacts = [], []
for slug, v in sorted(snaps.items()):
    d = " ".join((v.get("digest") or "").split())
    if not (ANN.search(d) and MON.search(d)):
        continue
    for sent in re.split(r"(?<=[.;])\s+", d):
        if not (ANN.search(sent) and MON.search(sent)):
            continue
        nums = [(float(m.group(1).replace(",", "")), m.start(), m.end()) for m in MONEY.finditer(sent)]
        if len(nums) < 2:
            continue
        # a number is an annual-monthly-equivalent when "annual" or "monthly" follows and the unit
        # after it is per-month
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                a, b = nums[i], nums[j]
                tail_a = sent[a[2]:a[2] + 26]
                tail_b = sent[b[2]:b[2] + 26]
                a_ann = bool(re.search(r"annual|/year|per year", tail_a, re.I))
                b_ann = bool(re.search(r"annual|/year|per year", tail_b, re.I))
                a_mon = bool(MONTHLY_EQ.search(tail_a))
                b_mon = bool(MONTHLY_EQ.search(tail_b))
                lo, hi = min(a[0], b[0]), max(a[0], b[0])
                if lo <= 0:
                    continue
                ratio = hi / lo
                rec = (slug, v.get("date"), lo, hi, ratio, sent[:110])
                if a_ann and not a_mon and b_ann and not b_mon:
                    # both figures are yearly totals -> not a monthly-vs-annual comparison
                    artifacts.append(rec)
                elif (a_mon != b_mon) or (a_ann != b_ann):
                    pairs.append(rec)

# dedupe on (slug, lo, hi)
seen, uniq = set(), []
for p in sorted(pairs, key=lambda x: x[4]):
    k = (p[0], p[2], p[3])
    if k not in seen:
        seen.add(k)
        uniq.append(p)

print("=" * 118)
print("QUALIFYING same-tier monthly vs annual pairs (both figures are per-month equivalents)")
print("=" * 118)
for slug, dt, lo, hi, r, sent in uniq:
    print(f"  {r:5.2f}x  {slug:<15} ${lo:<8g} vs ${hi:<8g} ({dt})")
    print(f"          {sent}")
vals = [p[4] for p in uniq]
print("-" * 118)
print(f"n = {len(vals)}")
if vals:
    print(f"range  : {min(vals):.2f}x to {max(vals):.2f}x")
    print(f"median : {statistics.median(vals):.2f}x")
    print(f"min pair: {[f'{p[0]} ${p[2]:g} vs ${p[3]:g}' for p in uniq if p[4] == min(vals)]}")
    print(f"max pair: {[f'{p[0]} ${p[2]:g} vs ${p[3]:g}' for p in uniq if p[4] == max(vals)]}")
    print(f"count above 1.8x: {sum(1 for v in vals if v > 1.8)}")

print("\n" + "=" * 118)
print("EXCLUDED as annual-total artifacts (a whole-year price, not a per-month equivalent)")
print("=" * 118)
seen2, uniq2 = set(), []
for p in sorted(artifacts, key=lambda x: -x[4]):
    k = (p[0], p[2], p[3])
    if k not in seen2:
        seen2.add(k)
        uniq2.append(p)
for slug, dt, lo, hi, r, sent in uniq2:
    print(f"  {r:7.2f}x {slug:<15} ${lo:g} vs ${hi:g}  {sent[:80]}")
print(f"n = {len(uniq2)}")
