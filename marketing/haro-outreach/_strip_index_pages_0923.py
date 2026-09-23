#!/usr/bin/env python3
"""Strip index/browse pages out of the historical digests.

The 2026-09-23 run's brief names this explicitly: /media-outlets/<outlet>/journo-requests and
/topics/<topic>/journo-requests are browse pages with no deadline and no reply route, and counting
them inflated the queue. build_pitch_queue.py already filters them at read time, so the QUEUE is
correct - but eleven of them are still sitting in digest-2026-09-07 through digest-2026-09-09 as if
they were opportunities, and any other reader of those files (or a future rewrite of the builder)
would re-inflate the count from them.

This removes only records whose url is not a /journo-request/<slug> page, records what was removed in
the digest's own `index_pages_removed` field rather than deleting the evidence silently, and leaves
every real request untouched. Idempotent: a second run removes nothing.
"""
from __future__ import annotations

import glob
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
total = 0

for f in sorted(glob.glob(str(OUT / "digest-*.json"))):
    p = Path(f)
    d = json.loads(p.read_text())
    ops = d.get("opportunities")
    if not isinstance(ops, list):
        continue
    keep, drop = [], []
    for o in ops:
        u = (o.get("url") or "").strip()
        if u and "/journo-request/" in u and "/media-outlets/" not in u and "/topics/" not in u:
            keep.append(o)
        else:
            drop.append(u or "(no url)")
    if not drop:
        continue
    d["opportunities"] = keep
    d.setdefault("index_pages_removed", [])
    d["index_pages_removed"] += [
        f"{u} - browse/index page, not a request: no deadline, no reply route, no journalist"
        for u in drop
    ]
    p.write_text(json.dumps(d, indent=1), encoding="utf-8")
    total += len(drop)
    print(f"{p.name}: removed {len(drop)}, kept {len(keep)}")

print(f"\ntotal index-page records removed: {total}")

# Verify: nothing non-request remains in any digest.
left = []
for f in sorted(glob.glob(str(OUT / "digest-*.json"))):
    d = json.loads(Path(f).read_text())
    for o in d.get("opportunities") or []:
        u = o.get("url") or ""
        if "/journo-request/" not in u or "/media-outlets/" in u or "/topics/" in u:
            left.append((Path(f).name, u))
print("non-request records still present:", len(left))
for x in left:
    print("  ", x)
