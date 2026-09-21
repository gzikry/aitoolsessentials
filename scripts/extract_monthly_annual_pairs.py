#!/usr/bin/env python3
"""THE authoritative same-tier monthly-vs-annual pair set. Curated, then asserted against the source.

Why curated: four regex extractions over data/pricing_snapshots.json returned 2, 7, 9 and 18 pairs,
so "1.21x to 2.53x" was a property of the pattern, not of the data. Each pair below was read off its
own sentence by hand. The script re-finds that sentence in the snapshot file and fails loudly if it
is no longer there, so the set cannot silently drift when the snapshots are refreshed.

FOUND 2026-09-21: the floor published in the 2026-09-18 pitch and repeated in the ledger and every
draft since is WRONG. Three same-tier pairs sit below 1.21x:

    instrumentl Pre-Award  $579 monthly vs $499/month annually = 1.16x
    instrumentl Discover   $349 monthly vs $299/month annually = 1.17x
    airtable-ai Team       $24 monthly  vs $20/seat/month annually = 1.20x
    slack-ai    Business+  $18 monthly  vs $15/user/month annually = 1.20x

The true range across same-tier per-month pairs is 1.16x to 2.53x, and the median is not 1.33x.
"""
import json
import statistics
import sys
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
snaps = json.loads((S / "data" / "pricing_snapshots.json").read_text())["snapshots"]

# (slug, plan label, monthly USD, annual-billed monthly-equivalent USD, must-appear substring)
PAIRS = [
    ("instrumentl",     "Discover",   349.0,  299.0, "$299/month paid upfront annually or $349 paid monthly"),
    ("instrumentl",     "Pre-Award",  579.0,  499.0, "$499/month annually or $579 monthly"),
    ("airtable-ai",     "Team",        24.0,   20.0, "$20/seat/month billed annually or $24 billed monthly"),
    ("slack-ai",        "Business+",   18.0,   15.0, "$15/user/month annually or $18 monthly"),
    ("slack-ai",        "Pro",          8.75,   7.25, "$7.25/user/month when paid annually or $8.75 when paid monthly"),
    ("heygen",          "Creator",     29.0,   24.0, "Creator is $29/month or $24/month billed annually"),
    ("fathom",          "premium",     20.0,   16.0, "$20/user/month monthly or $16/user/month billed annually"),
    ("replit-ai",       "Core",        25.0,   20.0, "Core is $25 monthly or $20/month billed annually"),
    ("runway",          "Standard",    15.0,   12.0, "Standard $15 monthly or $12/month billed annually"),
    ("runway",          "Pro",         35.0,   28.0, "Pro $35 monthly or $28/month billed annually"),
    ("browse-ai",       "Professional", 87.0,   69.0, "$87/month or $69/month billed annually"),
    ("browse-ai",       "Personal",     48.0,   19.0, "$48/month or $19/month billed annually"),
    ("rows",            "Plus",         8.0,    6.0, "$8/month per user billed monthly or $6/month billed annually"),
    ("descript",        "Hobbyist",    24.0,   16.0, "$24/month or $16/person/month billed annually"),
    ("magicschool",     "Plus",        12.99,   8.33, "$8.33 USD/user/month billed annually or $12.99 USD/month billed monthly"),
    ("fireflies",       "pro",         18.0,   10.0, "$18/seat/month monthly or $10/seat/month billed annually"),
    ("otter-ai",        "pro",         16.99,   8.33, "$16.99/user/month monthly or $8.33/user/month billed annually"),
    ("synthesia",       "Starter",     29.0,   18.0, "$29/month with 1,200 credits/month, or $18/month"),
]

fails = []
rows = []
for slug, plan, mon, ann, needle in PAIRS:
    d = " ".join((snaps.get(slug, {}).get("digest") or "").split())
    present = needle in d
    if not present:
        fails.append(f"{slug} {plan}: sentence no longer found — {needle!r}")
    if not (mon > ann > 0):
        fails.append(f"{slug} {plan}: monthly {mon} not above annual {ann}")
    rows.append((slug, plan, mon, ann, mon / ann, snaps.get(slug, {}).get("date"), present))

rows.sort(key=lambda r: r[4])
print("=" * 112)
print("CURATED same-tier monthly vs annual-monthly pairs — both figures are per-month prices")
print("=" * 112)
print(f"{'slug':<15}{'plan':<14}{'monthly$':>10}{'annual$':>10}{'ratio':>8}  {'date':<11}sent")
for slug, plan, mon, ann, r, dt, ok in rows:
    print(f"{slug:<15}{plan:<14}{mon:>10g}{ann:>10g}{r:>8.2f}  {dt:<11}{'yes' if ok else 'MISSING'}")

vals = [r[4] for r in rows]
print("-" * 112)
print(f"n                  : {len(vals)}")
print(f"range              : {min(vals):.2f}x  to  {max(vals):.2f}x")
print(f"median             : {statistics.median(vals):.2f}x")
print(f"count above 1.8x   : {sum(1 for v in vals if v > 1.8)}")
print(f"count at/below 1.21x: {sum(1 for v in vals if v <= 1.21)}")
lo = [r for r in rows if r[4] == min(vals)]
hi = [r for r in rows if r[4] == max(vals)]
print(f"lowest pair        : {lo[0][0]} {lo[0][1]} ${lo[0][2]:g} vs ${lo[0][3]:g}")
print(f"highest pair       : {hi[0][0]} {hi[0][1]} ${hi[0][2]:g} vs ${hi[0][3]:g}")
print(f"\nPUBLISHABLE SENTENCE: across {len(vals)} tools where the same tier quotes both a monthly "
      f"price and an annual-billed monthly price ({min(vals):.2f}x to {max(vals):.2f}x), the monthly "
      f"payer always pays more; median {statistics.median(vals):.2f}x.")
print(f"all pair dates: {sorted({r[5] for r in rows})}")

# machine-readable, so drafts and the verifier read one source
out = {"built": "2026-09-21", "source": "data/pricing_snapshots.json",
       "method": "curated by hand from each pair's own sentence; sentence re-asserted on every run",
       "pairs": [{"slug": s, "plan": p, "monthly_usd": m, "annual_billed_monthly_usd": a,
                  "ratio": round(r, 2), "snapshot_date": dt} for s, p, m, a, r, dt, _ in rows],
       "range_low": round(min(vals), 2), "range_high": round(max(vals), 2),
       "median": round(statistics.median(vals), 2), "n": len(vals),
       "supersedes": "the 1.21x-2.53x / median 1.33x claim published 2026-09-18 (it measured a "
                     "regex-dependent population of 9 pairs and omitted four pairs below 1.21x)"}
(S / "data" / "monthly_annual_pairs.json").write_text(json.dumps(out, indent=2))
print(f"\nwrote data/monthly_annual_pairs.json")
if fails:
    print("\nFAILURES:")
    for f in fails:
        print("  ", f)
sys.exit(1 if fails else 0)
