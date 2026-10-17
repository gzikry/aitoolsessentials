#!/usr/bin/env python3
"""Re-probe every reply route this monitor has ever recorded, and write today's route-checks file.

Why this exists: the per-run route probe (marketing/haro-outreach/_routes_*.py) was produced each
day by copying the previous day's file and editing its URL list by hand. On the 2026-10-12 run that
copy-step silently dropped the two OPE+ routes (ope-plus.com/2024/02/13/announcing-ope/19236 and
ope-plus.com/contact-us) that the 2026-10-10 probe had verified: the newest file simply did not
mention them, and only build_pitch_queue.py's file-MERGING kept their evidence alive. A route list
maintained by hand is the same defect class as the hardcoded draft filename and the hand-typed
live-row count already fixed elsewhere in this monitor.

This script takes the UNION of the route keys in every route-checks-*.json on disk, re-probes each
one once, and writes a file in the dict shape keyed by scheme-stripped route key:

    {"checked": "YYYY-MM-DD", "routes": {"<host/path/": {"label", "url", "http", "bytes", "title"}}}

Nothing is deleted from the union by this script; a route can only leave the set by being removed
from every historical file on purpose. Probe only - it never sends anything.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
OUT = SITE_ROOT / "marketing" / "haro-outreach"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def _key(u: str) -> str:
    return re.sub(r"^https?://(?:www\.)?", "", (u or "").strip()).rstrip("/").lower() + "/"


def _looks_like_route(k: str) -> bool:
    """A route key must look like a host/path, not a prose description.

    The 2026-10-11 file wrote `routes` as a list and used the prose string
    "six byline pages (muckrack.com/tobi-amure, ...)" as the route field for the dead-end row.
    Treating that as a URL produced a probe of "https://six byline pages (...)" returning HTTP 000.
    Prose is recorded on the row, not probed as a route.
    """
    return bool(re.match(r"^[a-z0-9][a-z0-9.\-]*\.[a-z]{2,}(?:/|$)", k))


def _load_union() -> dict:
    """Every route ever probed, newest file winning on conflicts."""
    union: dict = {}
    for p in sorted(OUT.glob("route-checks-*.json")):
        try:
            d = json.loads(p.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        routes = d.get("routes")
        if isinstance(routes, dict):
            items = [(k, v) for k, v in routes.items() if isinstance(v, dict)]
        elif isinstance(routes, list):  # the 2026-10-11 shape
            items = [(r.get("route") or r.get("url") or "", r) for r in routes if isinstance(r, dict)]
        else:
            continue
        for k, v in items:
            if k and _looks_like_route(_key(k)):
                union[_key(k)] = v
    return union


def curl(url: str, timeout: int = 30) -> tuple[str, str]:
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA,
                        "-w", "\n__HTTP__%{http_code}__", url], capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    return (m.group(1) if m else "000"), (raw[:raw.rfind("__HTTP__")] if m else raw)


def main() -> None:
    union = _load_union()
    # --add <url> [<url> ...] seeds the union from the command line, so a newly resolved route can be
    # brought into the probed set deliberately instead of by hand-editing a route-checks file. Seeded
    # routes are probed once and then live in the union like any other.
    adds = [a for a in sys.argv[sys.argv.index("--add") + 1:]] if "--add" in sys.argv else []
    for a in adds:
        url = a if a.startswith("http") else f"https://{a}"
        union.setdefault(_key(url), {"label": f"added {date.today().isoformat()}", "url": url})
    today = date.today().isoformat()
    routes: dict = {}
    for k, prev in sorted(union.items()):
        url = prev.get("url") or f"https://{k.rstrip('/')}"
        code, raw = curl(url)
        title = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
        rec = {"label": prev.get("label") or k, "url": url, "http": code, "bytes": len(raw),
               "title": (title.group(1).strip()[:120] if title else "")}
        # How many times each address appears on the page. A reply route published on a
        # journalist's own site is only evidence if it is still there, and "verbatim N times"
        # was a number measured by hand each run until now - the digest that cited it could not
        # tell a moved address from a re-worded page. Counting it here makes it a measurement.
        _emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)
        _counts = {e: raw.count(e) for e in sorted(set(_emails))}
        if _counts:
            rec["emails_on_page"] = _counts
        if prev.get("triple"):
            # A byline address assembled from data-part1/2/3 is only evidence if the parts are still
            # on the page; re-read them rather than carrying yesterday's triple forward.
            parts = re.findall(r'data-part[123]="([^"]*)"', raw)
            rec["triple"] = "+".join(parts[:3]) if len(parts) >= 3 else None
        routes[k] = rec
        print(f"  {code:>4} {len(raw):>9,}  {k}  {rec['title'][:52]}", flush=True)

    (OUT / f"route-checks-{today}.json").write_text(
        json.dumps({"checked": today, "routes": routes}, indent=1))
    print(f"\nprobed {len(routes)} route(s) -> route-checks-{today}.json")


if __name__ == "__main__":
    main()
