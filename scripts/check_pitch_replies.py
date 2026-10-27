#!/usr/bin/env python3
"""Check the mailbox for replies to pitches we actually sent — with a positive control.

Why this exists: the 2026-10-27 run swept nine recipient domains and got zero for every one of
them, including jansuski.com, which the ledger records as having replied twice. The sweep was
wrong, not the mailbox: the query had been passed as a single quoted string (`-q "from <domain>"`)
and himalaya v1 matches `from` as a pattern over the From header, not as a free-text search, so
every sender returned nothing. That is a silent zero — the one failure mode this monitor cannot
afford, because "no replies" is the sentence George acts on.

Two defences are built in:

  * a POSITIVE CONTROL is run first and must return at least one message from a sender we know has
    written to us (jan@jansuski.com, ledger reply_status 2026-09-18 and 2026-10-11). If the control
    returns nothing, the script exits non-zero and prints BROKEN rather than "no replies";
  * the folder is named explicitly ([Gmail]/All Mail by default), because a sweep of INBOX alone
    misses any reply that was filed, archived or read on a phone.

Usage:
    python3 scripts/check_pitch_replies.py
    python3 scripts/check_pitch_replies.py --folder INBOX --control jansuski.com
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
LEDGER = SITE_ROOT / "marketing" / "haro-outreach" / "pitch-ledger.json"

# Every domain a pitch has ever gone to from this monitor. Derived entries from the ledger are added
# on top of these, so a new send does not need this list edited — but the hand-kept list is what
# makes the sweep cover sends made before the ledger recorded a `to` field.
KNOWN = [
    "jansuski.com",            # control: replied 2026-09-18 and 2026-10-11
    "marketintelligencetools.com",
    "foxandspindle.com",
    "sherwood.news",
    "epgacceleration.com",
    "artichokehq.com",
    "raconteur.net",           # dead mailbox recorded: simon.chandler@ returns 550
    "businessinsider.com",
    "tobiamure.com",
    "linkedin.com",            # DMs, never email — kept so a notification email is not missed
]


def envelopes(folder: str, pattern: str, size: int = 20) -> list[str]:
    """Envelope rows from `himalaya envelope list`, one string per message.

    The query is passed as SEPARATE argv entries (`from`, `<pattern>`). Joined into one string it is
    matched as a literal and silently returns nothing — the defect this script exists to prevent.
    """
    r = subprocess.run(["himalaya", "envelope", "list", "-f", folder, "-s", str(size),
                        "from", pattern], capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        return []
    rows = []
    for line in r.stdout.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        # A data row's first cell is the envelope id. The header and the |----| separator both fail
        # that test; matching merely on "starts with |" counted the separator as a message and
        # reported one inbound from every domain on the first run of this script.
        if cells and cells[0].isdigit():
            rows.append(line)
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", default="[Gmail]/All Mail")
    ap.add_argument("--control", default="jansuski.com")
    a = ap.parse_args()

    ctl = envelopes(a.folder, a.control, size=5)
    print(f"positive control ({a.control}) in {a.folder}: {len(ctl)} message(s)")
    if not ctl:
        print("BROKEN: the control sender returned nothing, so every zero below is meaningless.")
        print("Check the folder name and the query shape before reading any result as 'no replies'.")
        return 2
    for row in ctl:
        print("   ", row)

    domains = list(dict.fromkeys(KNOWN))
    try:
        led = json.loads(LEDGER.read_text())
    except (OSError, json.JSONDecodeError):
        led = {}
    for entry in (led.get("log") or []):
        to = (entry.get("to") or "").strip()
        m = re.search(r"@([A-Za-z0-9.-]+\.[A-Za-z]{2,})", to)
        if m and m.group(1).lower() not in domains:
            domains.append(m.group(1).lower())

    print(f"\nsweeping {len(domains)} recipient domain(s) in {a.folder}")
    total = 0
    for d in domains:
        rows = envelopes(a.folder, d, size=20)
        hit = len(rows) if d != a.control else len(rows)
        total += 0 if d == a.control else hit
        label = f"{hit} message(s)" if hit else "no messages"
        print(f"  {d:<32} {label}")
        if hit and d != a.control:
            for row in rows:
                print("        ", row)

    print(f"\nnon-control inbound found: {total}")
    if total == 0:
        print("ZERO REPLIES — measured against a working control, so this is a real zero and not a "
              "broken query.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
