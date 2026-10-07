#!/usr/bin/env python3
"""Final audit of the 2026-10-07 artifacts: stale figures, JSON validity, counts."""
import json, re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
files = ["digest-2026-10-07.json", "pitch-queue.md", "pitch-drafts-2026-10-07.md",
         "pitch-ledger.json", "route-checks-2026-10-07.json"]
STALE = [r"40 of 76", r"median \$16\.50", r"\b1\.16x\b", r"1\.21x-2\.53x", r"630,514 bytes",
         r"pitch-drafts-2026-10-0[1-6]\.md", r"updated: 2026-10-0[1-6]"]
for f in files:
    t = (D / f).read_text()
    hits = []
    for pat in STALE:
        for m in re.finditer(pat, t):
            hits.append(m.group(0))
    print(f"{f}: {len(hits)} stale-figure hits" + (f" -> {hits[:6]}" if hits else ""))

d = json.loads((D / "digest-2026-10-07.json").read_text())
print("\ndigest date:", d["date"], "| opportunities:", len(d["opportunities"]),
      "| platforms:", len(d["platforms_checked"]))
print("monitor_health:", json.dumps(d["monitor_health"]))
led = json.loads((D / "pitch-ledger.json").read_text())
print("ledger reply_status_checked:", led["reply_status_checked"], "| pitched:", len(led["pitched"]),
      "| skipped:", len(led["skipped"]))
q = (D / "pitch-queue.md").read_text().splitlines()[2]
print("queue header:", q)
