#!/usr/bin/env python3
"""Audit outbound outreach recipients for deliverability.

Checks every September+ outbound message (Sent Mail and Trash, since Gmail files
some sends there) and reports recipient domains with no MX record. A no-MX domain
cannot receive mail and will never generate a bounce, so this is the only way to
catch it.

Usage:
    python3 scripts/audit_recipient_mx.py            # report only
    python3 scripts/audit_recipient_mx.py --since 2026-09
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict

SELF_ADDR = "aitoolsessentials@gmail.com"
# Outbound mail can live in more than one folder; Trash is the one that gets missed.
OUTBOUND_FOLDERS = ("[Gmail]/Sent Mail", "[Gmail]/Trash", "[Gmail]/All Mail")


def himalaya_envelopes(folder: str, page_size: int = 400) -> list[dict]:
    result = subprocess.run(
        ["himalaya", "envelope", "list", "--folder", folder,
         "--page-size", str(page_size), "--output", "json"],
        capture_output=True, text=True, timeout=300,
    )
    start = result.stdout.find("[")
    if start == -1:
        return []
    try:
        return json.JSONDecoder().raw_decode(result.stdout[start:])[0]
    except json.JSONDecodeError:
        return []


def has_mx(domain: str) -> bool:
    result = subprocess.run(
        ["dig", "+short", "MX", domain], capture_output=True, text=True, timeout=30
    )
    return bool(result.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", default="2026-09", help="Only messages on/after this YYYY-MM prefix")
    parser.add_argument("--quiet", action="store_true", help="Print nothing when clean")
    args = parser.parse_args()

    outbound: dict[tuple, dict] = {}
    for folder in OUTBOUND_FOLDERS:
        for message in himalaya_envelopes(folder):
            if ((message.get("from") or {}).get("addr") or "").lower() != SELF_ADDR:
                continue
            if not (message.get("date") or "").startswith(args.since):
                continue
            recipient = ((message.get("to") or {}).get("addr") or "").lower()
            # Same send can appear in several folders; key on the send itself.
            key = ((message.get("date") or "")[:19], message.get("subject") or "", recipient)
            outbound.setdefault(key, {**message, "_folder": folder})
    messages = list(outbound.values())

    by_domain: dict[str, set[str]] = defaultdict(set)
    for message in messages:
        recipient = ((message.get("to") or {}).get("addr") or "").lower()
        if "@" in recipient:
            by_domain[recipient.rsplit("@", 1)[1]].add(recipient)

    dead = {d: addrs for d, addrs in by_domain.items() if not has_mx(d)}

    if not args.quiet:
        print(f"Outbound since {args.since}: {len(messages)} sends")
        print(f"Recipient domains: {len(by_domain)}")
        print(f"Domains with MX: {len(by_domain) - len(dead)}")
        print(f"Domains WITHOUT MX: {len(dead)}")

    if dead:
        print("\nUNDELIVERABLE RECIPIENT DOMAINS (no MX — mail cannot arrive):")
        for domain in sorted(dead):
            print(f"  {domain}  ->  {sorted(dead[domain])}")
        print("\nRemove these from outreach lists; a no-MX domain never bounces, so it")
        print("fails silently and is invisible to bounce-driven detection.")
        return 1

    if not args.quiet:
        print("\nAll recipient domains can receive mail.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
