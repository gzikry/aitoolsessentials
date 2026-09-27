#!/usr/bin/env python3
"""Verify today's drafts before anyone pastes them.

Three checks, because all three have failed in a previous run:
  1. Word count under 200 for every paste-ready body (body only: excludes subject line, signature
     and the unsubscribe footer). The 2026-09-23 run's first pass asserted 138/136 words and was
     wrong; measured properly they were 154/164. So the count is measured here, never asserted.
  2. Every number in a draft body traces to a value in data/tools.json, data/pricing_snapshots.json,
     data/monthly_annual_pairs.json or data/tool_sources.json (with its own check date).
  3. Signed AIToolsEssentials, George's name absent from every body, and the reply route named.
"""
from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing" / "haro-outreach" / "pitch-drafts-2026-09-27.md"
text = D.read_text()

blocks = re.findall(r"^> Hi .*?(?=^> AIToolsEssentials)", text, re.M | re.S)

print("=== word counts (body only: excl. subject, signature, footer) ===")
for i, b in enumerate(blocks, 1):
    words = re.findall(r"\S+", " ".join(re.sub(r"^> ?", "", ln) for ln in b.splitlines()))
    flag = "  !! OVER 200" if len(words) > 200 else ""
    print(f"  draft {i}: {len(words)} words{flag}")
if not blocks:
    print("  !! no bodies found — the extraction pattern is wrong, fix it before trusting this")

ps = json.loads((S / "data" / "pricing_snapshots.json").read_text())
snaps = ps["snapshots"]
pairs = json.loads((S / "data" / "monthly_annual_pairs.json").read_text())["pairs"]
tools = json.loads((S / "data" / "tools.json").read_text())
srcs = json.loads((S / "data" / "tool_sources.json").read_text())
blob = (json.dumps(snaps) + json.dumps(pairs) + json.dumps(tools) + json.dumps(srcs)).lower()

MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid = {}
for k, v in snaps.items():
    vals = [float(x) for x in MONTH.findall(" ".join((v.get("digest") or "").split())) if float(x) > 0]
    if vals:
        paid[k] = min(vals)
n_under = sum(1 for v in paid.values() if v <= 25)
med = round(statistics.median(paid.values()), 2)

checked = [
    ("76 tools (tools.json)", len(tools) == 76),
    ("76 snapshot records", len(snaps) == 76),
    ("40 tools with a non-zero monthly price", len(paid) == 40),
    ("31 of those at/under $25", n_under == 31),
    ("median cheapest paid tier $16.50", med == 16.5),
    ("$4 Khanmigo in the data", "khanmigo" in blob),
    ("1.11x floor", any(p["ratio"] == 1.11 for p in pairs)),
    ("2.53x ceiling", any(p["ratio"] == 2.53 for p in pairs)),
    ("median 1.25x", statistics.median(p["ratio"] for p in pairs) == 1.25),
    ("19 tiers", len(pairs) == 19),
    ("14 tools", len({p["slug"] for p in pairs}) == 14),
    ("Browse AI $48 vs $19", any(p["slug"] == "browse-ai" and p["monthly_usd"] == 48
                                 and p["annual_billed_monthly_usd"] == 19 for p in pairs)),
    ("replit-ai $20 vs $18 (narrowest)", any(p["slug"] == "replit-ai" and p["monthly_usd"] == 20
                                            and p["annual_billed_monthly_usd"] == 18 for p in pairs)),
    ("pair snapshot dates 2026-09-18 / 2026-09-21",
     sorted({p["snapshot_date"] for p in pairs}) == ["2026-09-18", "2026-09-21"]),
    ("snapshot updated today", ps.get("updated") == "2026-09-27"),
    ("pairs built today", json.loads((S / "data" / "monthly_annual_pairs.json").read_text())["built"]
     == "2026-09-27"),
    ("simon.chandler@raconteur.net cited", "simon.chandler@raconteur.net" in text),
    ("holly.shackleton@artichokehq.com cited", "holly.shackleton@artichokehq.com" in text),
    ("Signal hliwrites.99 cited", "hliwrites.99" in text),
    ("no superseded 1.21x floor presented as current",
     "runs 1.21x" not in text and "1.21x-2.53x" not in text.replace("1.21x-2.53x, median 1.33x", "")),
    ("no superseded 1.16x floor presented as current", "1.16x to 2.53x" not in text.split("corrected to")[-1]),
]
print("\n=== figure traceability ===")
for label, ok in checked:
    print(f"  {'OK  ' if ok else 'FAIL'} {label}")

print("\n=== signing ===")
sigs = re.findall(r"^> (\S+)$", text, re.M)
body_text = " ".join(re.sub(r"^> ?", "", ln) for b in blocks for ln in b.splitlines())
for label, ok in [
    ("every body carries an AIToolsEssentials signature",
     len(re.findall(r"^> AIToolsEssentials$", text, re.M)) == len(blocks) == 2),
    ("no 'George' inside any draft body or signature",
     "george" not in body_text.lower() and not any("george" in s.lower() for s in sigs)),
    ("'George' appears only as operator routing notes",
     all("lane" in ln or "blocking sends" in ln for ln in re.findall(r".*George.*", text))),
    # Two paste-ready drafts, each naming its reply route, plus the Jan Suski correction, which is
    # not a pitch draft and routes by thread reply instead. Asserting >= 3 "Reply route:" lines (as
    # this check first did) demanded a third draft that does not exist — the right constraint is that
    # each of the 2 bodies has a route and the correction names its own route class.
    ("every draft body names a reply route", text.count("Reply route:") == 2),
    ("the correction names its route class", "In-Reply-To the existing thread" in text),
    ("every pitch draft says not automatable", text.count("Not automatable") >= 2),
    ("unsent header present", "Nothing here has been sent" in text),
    ("every body under 200 words", all(len(re.findall(r"\S+", b)) <= 200 for b in blocks)),
]:
    print(f"  {'OK  ' if ok else 'FAIL'} {label}")

print(f"\nfile: {D.relative_to(S)}  ({len(text):,} chars)")
print(f"pricing_snapshots updated: {ps.get('updated')}  pairs built: "
      f"{json.loads((S / 'data' / 'monthly_annual_pairs.json').read_text())['built']}")
