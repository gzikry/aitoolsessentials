#!/usr/bin/env python3
"""Verify today's drafts: every figure traced to its own data file, signature rule, word counts,
and the superseded-value guard.

Note on style: this file previously used `(cond and ok(msg)) or fail(msg)`. Because the helper
returned None, BOTH branches ran and every check printed as OK and FAIL at once — a verifier that
cannot fail is worse than no verifier. Every check below is an explicit if/else.
"""
import json
import re
import statistics
import sys
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing" / "haro-outreach"
MD = (D / "pitch-drafts-2026-09-29.md").read_text()

oks: list[str] = []
fails: list[str] = []


def check(cond: bool, msg: str) -> bool:
    (oks if cond else fails).append(msg)
    return bool(cond)


# ---------------------------------------------------------------- figures, recomputed
tools = json.loads((S / "data/tools.json").read_text())
snapf = json.loads((S / "data/pricing_snapshots.json").read_text())
snaps = snapf["snapshots"]
pairs = json.loads((S / "data/monthly_annual_pairs.json").read_text())

print("=== figure traceability ===")
check(len(tools) == 76 and "76 tools" in MD, f"76 tools (tools.json has {len(tools)})")
check(len(snaps) == 76, f"76 snapshot records ({len(snaps)})")

MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid: dict[str, float] = {}
for k, v in snaps.items():
    d = " ".join((v.get("digest") or "").split())
    vals = [float(x) for x in MONTH.findall(d) if float(x) > 0]
    if vals:
        paid[k] = min(vals)
check(len(paid) == 40, f"40 tools with a non-zero monthly price ({len(paid)})")
check(sum(1 for v in paid.values() if v <= 25) == 31,
      f"31 of those at/under $25 ({sum(1 for v in paid.values() if v <= 25)})")
med = statistics.median(paid.values())
check(abs(med - 16.50) < 0.01, f"median cheapest paid tier $16.50 (${med:.2f})")
check(min(paid.values()) == 4.0, f"$4 Khanmigo in the data (min ${min(paid.values()):.2f})")

check(round(pairs["range_low"], 2) == 1.11, f"1.11x floor ({pairs['range_low']})")
check(round(pairs["range_high"], 2) == 2.53, f"2.53x ceiling ({pairs['range_high']})")
check(round(pairs["median"], 2) == 1.25, f"median 1.25x ({pairs['median']})")
check(pairs["n"] == 19, f"19 tiers ({pairs['n']})")
check(len({p["slug"] for p in pairs["pairs"]}) == 14,
      f"14 tools ({len({p['slug'] for p in pairs['pairs']})})")
snap_dates = sorted({p["snapshot_date"] for p in pairs["pairs"]})
check(snap_dates == ["2026-09-18", "2026-09-21"], f"pair snapshot dates {snap_dates}")
browse = [p for p in pairs["pairs"] if p["slug"] == "browse-ai" and p["plan"] == "Personal"][0]
check(browse["monthly_usd"] == 48 and browse["annual_billed_monthly_usd"] == 19,
      f"Browse AI ${browse['monthly_usd']:.0f} vs ${browse['annual_billed_monthly_usd']:.0f}")
rep = [p for p in pairs["pairs"] if p["slug"] == "replit-ai" and p["plan"] == "Core"][0]
check(rep["monthly_usd"] == 20 and rep["annual_billed_monthly_usd"] == 18,
      f"replit-ai ${rep['monthly_usd']:.0f} vs ${rep['annual_billed_monthly_usd']:.0f} (narrowest)")

print(f"  pairs built: {pairs['built']} | snapshots updated: {snapf.get('updated')}")
check(pairs["built"] == "2026-09-29", f"pairs built today ({pairs['built']})")
check(snapf.get("updated") == "2026-09-29", f"snapshot updated today ({snapf.get('updated')})")

for route in ("simon.chandler@raconteur.net", "holly.shackleton@artichokehq.com",
              "1.11x", "2.53x", "1.25x", "nineteen" if False else "19 tiers", "14 tools"):
    check(route in MD, f"cited in the drafts: {route}")

# ---------------------------------------------------------------- quote bodies only
blocks = re.findall(r"^> Subject:.*(?:\n>.*)*", MD, re.M)
body_text = "\n".join(blocks)

print("\n=== superseded figures (inside pitch bodies only) ===")
hits_121 = body_text.count("1.21x-2.53x")
check(hits_121 <= 1, f"the superseded 1.21x range appears at most once in a body ({hits_121})")
check("That was wrong" in body_text, "where 1.21x does appear, it is flagged as wrong")
check("1.16x" not in body_text, f"no superseded 1.16x floor in a body ({body_text.count('1.16x')})")
check("median 1.33x" in body_text, "the correction quotes the 1.33x it is correcting")

print("\n=== signing ===")
check(not re.search(r"\bGeorge\b", body_text), "no 'George' inside any pitch body")
check(body_text.count("AIToolsEssentials") >= 3,
      f"AIToolsEssentials signature in each body ({body_text.count('AIToolsEssentials')})")
lane_hits = re.findall(r"George's lane\. Not automatable", MD)
check(len(lane_hits) >= 2, f"'George's lane. Not automatable' on each drafted pitch ({len(lane_hits)})")
check("Nothing here has been sent" in MD, "unsent header present")

print("\n=== word counts (body incl. subject + signature, under 200 each) ===")
for i, b in enumerate(blocks, 1):
    words = len(re.sub(r"^> ?", "", b, flags=re.M).split())
    print(f"  block {i}: {words} words")
    if i <= 2:
        check(words < 200, f"pitch body {i} under 200 words ({words})")

print("\n=== this run's defect, named where a reader will see it ===")
q = (D / "pitch-queue.md").read_text()
check("0 sendable" in q, "queue headline reads 0 sendable")
check("chrome filter" in q, "the chrome-filter defect is named in the queue")
check("chrome filter" in MD, "the chrome-filter defect is named in the drafts")

print()
for m in oks:
    print("  OK   ", m)
for m in fails:
    print("  FAIL ", m)
print(f"\n{len(oks)} checks passed, {len(fails)} failed")
print(f"file: marketing/haro-outreach/pitch-drafts-2026-09-29.md ({len(MD):,} chars)")
sys.exit(1 if fails else 0)
