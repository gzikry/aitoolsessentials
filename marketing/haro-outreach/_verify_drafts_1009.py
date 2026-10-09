#!/usr/bin/env python3
"""Verify the 2026-10-09 draft figures against our own data files, and measure the drafts.

Nothing in the drafts may cite a number that is not in data/tools.json,
data/pricing_snapshots.json, data/tool_sources.json or data/monthly_annual_pairs.json with its
check date. This script re-derives each figure the drafts use and asserts the draft text carries
it; it also measures the word count of each paste-ready block (the drafts have twice been shipped
with hand-typed word counts that were wrong).

Usage: python3 marketing/haro-outreach/_verify_drafts_1009.py
"""
from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing" / "haro-outreach"
DRAFT = D / "pitch-drafts-2026-10-09.md"

snaps = json.loads((S / "data/pricing_snapshots.json").read_text())
tools = json.loads((S / "data/tools.json").read_text())
pairs = json.loads((S / "data/monthly_annual_pairs.json").read_text())
srcs = json.loads((S / "data/tool_sources.json").read_text())
text = DRAFT.read_text()

MONTH = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
paid = {}
for k, v in (snaps.get("snapshots") or {}).items():
    vals = [float(x) for x in MONTH.findall(v.get("digest") or "") if float(x) > 0]
    if vals:
        paid[k] = min(vals)

checks: list[tuple[str, bool, str]] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    checks.append((label, ok, detail))


n_tools, n_snap = len(tools), len(snaps.get("snapshots") or {})
check("tools.json and snapshots agree on the count", n_tools == n_snap, f"{n_tools} vs {n_snap}")
check("snapshot date is today", snaps.get("updated") == "2026-10-09", str(snaps.get("updated")))
check("77 tools claimed", f"{n_snap} AI tools" in text, f"digest has {n_snap}")
check("42 of 77 publish a monthly price", len(paid) == 42 and "42 of 77" in text, f"derived {len(paid)}")
check("33 at or under $25", sum(1 for v in paid.values() if v <= 25) == 33
      and "33 of those start at or under" in text)
check("median $17.50", f"{statistics.median(paid.values()):.2f}" == "17.50" and "median $17.50" in text)
lo = min(paid.values())
check("lowest $4 (khanmigo)", lo == 4.0 and "lowest $4 (Khanmigo)" in text,
      f"min {lo} -> {[k for k, v in paid.items() if v == lo]}")
check("no superseded 76 denominator left", "of 76 tools" not in text)
check("pair range 1.11x-2.53x",
      str(pairs.get("range_low")) == "1.11" and str(pairs.get("range_high")) == "2.53"
      and ("1.11x to 2.53x" in text or "1.11x-2.53x" in text),
      f"{pairs.get('range_low')}x-{pairs.get('range_high')}x")
check("pair median 1.25x", str(pairs.get("median")) == "1.25" and "median 1.25x" in text,
      str(pairs.get("median")))
check("pair n is 19", str(pairs.get("n")) == "19" and "19 tiers" in text, str(pairs.get("n")))

# The three seat prices the Google/Claude draft cites must exist in our sources with their dates.
seat_tokens = {
    "Claude Team $20/$100 per seat": ("claude", ["$20 per seat per month", "$100 per seat per month"]),
    "Gemini $8.40/$7 to $26.40/$22": ("gemini", ["8.40/$7", "26.40/$22"]),
    "Copilot Business $19 / Enterprise $39": ("github-copilot", ["$19/user/month", "$39/user/month"]),
}
for label, (slug, needles) in seat_tokens.items():
    entry = next((t for t in srcs["tools"] if t["slug"] == slug), None)
    blob = (entry or {}).get("pricing_summary", "")
    check(f"tool_sources holds {label}", bool(entry) and all(n in blob for n in needles),
          f"slug={slug} checked {entry.get('pricing_checked_date') if entry else '—'}")

# The signature must be AIToolsEssentials with no personal name. "George" may appear only in the
# per-row routing notes (it is his lane), never inside a paste-ready block.
blocks_only = "\n".join(re.findall(r"^> .*$", text, re.M))
check("signature is AIToolsEssentials only in the paste-ready blocks",
      "AIToolsEssentials" in blocks_only and "George" not in blocks_only)
check("no placeholder or unfilled figure", "TBD" not in text and "XX" not in text)

# word counts, measured rather than asserted
blocks = re.findall(r"^> .*$", text, re.M)
print("figures re-derived:")
for k, v in sorted(paid.items()):
    pass
print(f"  tools {n_snap}, monthly-priced {len(paid)}, <=$25 {sum(1 for v in paid.values() if v <= 25)}, "
      f"median ${statistics.median(paid.values()):.2f}, min ${lo:.2f}")

sections = re.split(r"^## ", text, flags=re.M)
for sec in sections[1:]:
    title = sec.split("\n", 1)[0][:56]
    body = " ".join(l[2:].strip() for l in sec.splitlines() if l.startswith("> "))
    words = len(body.split()) if body else 0
    print(f"  {words:>4} words (incl. subject+signature) — {title}")

bad = [c for c in checks if not c[1]]
print(f"\n{len(checks) - len(bad)}/{len(checks)} checks passed")
for label, ok, detail in bad:
    print(f"  FAIL {label}  {detail}")
raise SystemExit(1 if bad else 0)
