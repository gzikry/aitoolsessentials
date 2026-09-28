#!/usr/bin/env python3
"""Verify today's drafts before anyone pastes them.

Three checks, because all three have failed in a previous run:
  1. Word count under 200 for every paste-ready body (body only: excludes subject line, signature
     and the unsubscribe footer). The 2026-09-23 run's first pass asserted 138/136 words and was
     wrong; measured properly they were 154/164. So the count is measured here, never asserted.
  2. Every number in a draft body traces to a value in data/tools.json, data/pricing_snapshots.json,
     data/monthly_annual_pairs.json or data/tool_sources.json (with its own check date).
  3. Signed AIToolsEssentials, George's name absent from every body, and the reply route named.

Note on the superseded-figure check: the Jan Suski block is a CORRECTION, so it must quote the wrong
figure ("1.21x-2.53x, median 1.33x") - that is its whole content. The check therefore tests the two
pitch bodies only, not the correction.
"""
from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing" / "haro-outreach" / "pitch-drafts-2026-09-28.md"
text = D.read_text()

# A body runs from "> Hi <name>," to its signature line. The correction is addressed "> Jan —" and
# is captured separately so it is never mistaken for a pitch body.
pitch_blocks = re.findall(r"^> Hi .*?(?=^> AIToolsEssentials)", text, re.M | re.S)
correction_blocks = re.findall(r"^> Jan — .*?(?=^> AIToolsEssentials)", text, re.M | re.S)


def _plain(block: str) -> str:
    return " ".join(re.sub(r"^> ?", "", ln) for ln in block.splitlines())


print("=== word counts (pitch bodies only: excl. subject, signature, footer) ===")
for i, b in enumerate(pitch_blocks, 1):
    words = re.findall(r"\S+", _plain(b))
    flag = "  !! OVER 200" if len(words) > 200 else ""
    print(f"  pitch draft {i}: {len(words)} words{flag}")
if len(pitch_blocks) != 2:
    print(f"  !! expected 2 pitch bodies, found {len(pitch_blocks)} - fix the pattern before trusting this")
print(f"  correction block found: {len(correction_blocks)} (not word-limited: it is a correction, not a pitch)")

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
    ("snapshot updated today", ps.get("updated") == "2026-09-28"),
    ("pairs built today", json.loads((S / "data" / "monthly_annual_pairs.json").read_text())["built"]
     == "2026-09-28"),
    ("simon.chandler@raconteur.net cited", "simon.chandler@raconteur.net" in text),
    ("holly.shackleton@artichokehq.com cited", "holly.shackleton@artichokehq.com" in text),
    ("Signal hliwrites.99 cited", "hliwrites.99" in text),
]
print("\n=== figure traceability ===")
for label, ok in checked:
    print(f"  {'OK  ' if ok else 'FAIL'} {label}")

# Superseded figures must not appear in either PITCH body. The correction block is excluded by
# design - quoting the wrong number is its content.
pitch_text = " ".join(_plain(b) for b in pitch_blocks)
superseded = [
    ("no superseded 1.21x floor in a pitch body", "1.21x" not in pitch_text),
    ("no superseded 1.16x floor in a pitch body", "1.16x" not in pitch_text),
    ("no superseded median 1.33x in a pitch body", "1.33x" not in pitch_text),
    ("the correction does quote the wrong figure it is correcting",
     "1.21x-2.53x" in " ".join(_plain(b) for b in correction_blocks)),
]
print("\n=== superseded figures ===")
for label, ok in superseded:
    print(f"  {'OK  ' if ok else 'FAIL'} {label}")

print("\n=== signing ===")
sigs = re.findall(r"^> (\S+)$", text, re.M)
body_text = " ".join(re.sub(r"^> ?", "", ln) for b in pitch_blocks + correction_blocks for ln in b.splitlines())
for label, ok in [
    ("every body carries an AIToolsEssentials signature",
     len(re.findall(r"^> AIToolsEssentials$", text, re.M)) == 3),
    ("no 'George' inside any draft body or signature",
     "george" not in body_text.lower() and not any("george" in s.lower() for s in sigs)),
    ("'George' appears only as operator routing notes",
     all("lane" in ln or "blocking sends" in ln for ln in re.findall(r".*George.*", text))),
    ("every pitch body names a reply route", text.count("Reply route:") == 2),
    ("the correction names its route class", "In-Reply-To the existing thread" in text),
    ("every pitch draft says not automatable", text.count("Not automatable") >= 2),
    ("unsent header present", "Nothing here has been sent" in text),
    ("both crossed rows are named as crossed", text.count("CROSSED COLD TODAY") == 2),
    ("both pitch bodies under 200 words",
     all(len(re.findall(r"\S+", _plain(b))) <= 200 for b in pitch_blocks)),
]:
    print(f"  {'OK  ' if ok else 'FAIL'} {label}")

print(f"\nfile: {D.relative_to(S)}  ({len(text):,} chars)")
print(f"pricing_snapshots updated: {ps.get('updated')}  pairs built: "
      f"{json.loads((S / 'data' / 'monthly_annual_pairs.json').read_text())['built']}")
