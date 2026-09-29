#!/usr/bin/env python3
"""Compare yesterday's ages with today's page-read ages; name every row that crossed."""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
prev = json.loads((D / "digest-2026-09-28.json").read_text())
led = json.loads((D / "pitch-ledger.json").read_text())
done = {u.rstrip("/").split("/journo-request/")[-1] for u in
        list(led.get("pitched", {})) + list(led.get("skipped", {}))}

today = {}
for r in json.loads((D / "_reverify_0929.json").read_text()):
    today[r["url"].rstrip("/").split("/journo-request/")[-1]] = r


def days_from_badge(badge, pub):
    import re
    if badge:
        m = re.search(r"(\d+)\s*days?", badge)
        if m:
            return int(m.group(1))
        if "last 7 days" in badge:
            return 3
        if badge == "today":
            return 0
        if badge == "yesterday":
            return 1
    return None


rows = []
for o in prev["opportunities"]:
    slug = o["url"].rstrip("/").split("/journo-request/")[-1]
    t = today.get(slug, {})
    old = o.get("_days_old")
    new = days_from_badge(t.get("badge"), t.get("datePublished"))
    rows.append((slug, old, new, slug in done, o.get("relevance")))

live_prev = [r for r in rows if (r[1] or 99) <= 10 and not r[3]]
live_now = [r for r in rows if (r[2] if r[2] is not None else 99) <= 10 and not r[3]]
print(f"prev digest rows: {len(rows)}  live&unpitched yesterday: {len(live_prev)}  live&unpitched today: {len(live_now)}")
print("\n--- live & unpitched TODAY (<=10d) ---")
for s, o, n, d, rel in live_now:
    print(f"  {n:>3}d (was {o}d) rel={rel:<8} {s}")
print("\n--- crossed the line in this run (was live, now >10d) ---")
for s, o, n, d, rel in rows:
    if (o or 99) <= 10 and (n or 0) > 10 and not d:
        print(f"  was {o}d -> now {n}d rel={rel:<8} {s}")
print("\n--- badge not parseable (no 'Posted ... ago' text) ---")
for s, o, n, d, rel in rows:
    if n is None:
        print(f"  prev {o}d  {s}")
