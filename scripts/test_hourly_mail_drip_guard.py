#!/usr/bin/env python3
"""Prove the two mail-monitor false-positive defects, and that the fix holds.

Defect 1: our own outbound mail sent from the site's forwarder alias
          (contact@aitoolsessentials.com) is classified as *incoming* and alerts.
Defect 2: the seen fingerprint includes folder + IMAP id, so the same message
          re-alerts whenever Gmail refiles it or the sequence id shifts. The
          seen set is also replaced by the current 100-message window each run,
          so mail that scrolls out of the window and back in re-alerts too.

Each case asserts the exact disposition, not just "no crash" — a guard that
never fires is indistinguishable from no guard.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hourly_mail_alert as h  # noqa: E402

CASES = [
    # (description, message, expected_actionable)
    (
        "DEFECT 1: our own verification send from the forwarder alias",
        {"from": {"addr": "contact@aitoolsessentials.com"},
         "subject": "Image Describer submission — verification needed",
         "date": "2026-09-07 22:14-07:00", "id": "104", "_folder": "[Gmail]/All Mail"},
        False,
    ),
    (
        "DEFECT 1: forwarder alias, mixed case",
        {"from": {"addr": "Contact@AIToolsEssentials.com"},
         "subject": "Sharpniq / Unblur Image submission — verification needed",
         "date": "x", "id": "1", "_folder": "[Gmail]/All Mail"},
        False,
    ),
    (
        "our own primary inbox address is still never actionable",
        {"from": {"addr": "aitoolsessentials@gmail.com"}, "subject": "Re: anything",
         "date": "x", "id": "2", "_folder": "[Gmail]/All Mail"},
        False,
    ),
    (
        "DEFECT 2: stable key survives a folder refile (same mail, moved to Trash)",
        {"from": {"addr": "submissions@formsubmit.co"},
         "subject": "New AI tool submission — editorial review",
         "date": "2026-09-12 12:21+00:00", "id": "88", "_folder": "[Gmail]/Trash"},
        True,
    ),
    (
        "MUST STILL FIRE: a genuine new vendor submission",
        {"from": {"addr": "submissions@formsubmit.co"},
         "subject": "New AI tool submission — editorial review",
         "date": "2026-09-18 09:00+00:00", "id": "240", "_folder": "[Gmail]/All Mail"},
        True,
    ),
    (
        "MUST STILL FIRE: a DSN failure",
        {"from": {"addr": "mailer-daemon@googlemail.com"},
         "subject": "Delivery Status Notification (Failure)",
         "date": "x", "id": "5", "_folder": "[Gmail]/Spam"},
        True,
    ),
    (
        "MUST STILL FIRE: unknown human sender",
        {"from": {"addr": "someone@example.com"}, "subject": "Hello",
         "date": "x", "id": "7", "_folder": "[Gmail]/All Mail"},
        True,
    ),
    (
        "MUST STILL FIRE: a human replying to a drip",
        {"from": {"addr": "community@connectively.us"}, "subject": "Re: Checking in",
         "date": "x", "id": "9", "_folder": "[Gmail]/All Mail"},
        True,
    ),
    (
        "Connectively lifecycle drip stays silent",
        {"from": {"addr": "community@connectively.us"}, "subject": "Checking in",
         "date": "x", "id": "11", "_folder": "[Gmail]/All Mail"},
        False,
    ),
]

failures = 0
for description, message, expected in CASES:
    got, reason = h.disposition(message)
    ok = got == expected
    failures += 0 if ok else 1
    print(f"{'PASS' if ok else 'FAIL'}  actionable={got!s:5} expected={expected!s:5}  {description}")
    if not ok:
        print(f"        reason returned: {reason!r}")

# Defect 2, part two: the fingerprint must be folder- and id-independent, so a
# message that Gmail refiles or renumbers maps to the SAME key.
moved = {"from": {"addr": "submissions@formsubmit.co"},
         "subject": "New AI tool submission — editorial review",
         "date": "2026-09-12 12:21+00:00", "id": "88", "_folder": "[Gmail]/Trash"}
renumbered = dict(moved, id="120", _folder="[Gmail]/All Mail")
same = h.fingerprint(moved) == h.fingerprint(renumbered)
failures += 0 if same else 1
print(f"{'PASS' if same else 'FAIL'}  fingerprint stable across folder move + renumber")
if not same:
    print(f"        {h.fingerprint(moved)!r} != {h.fingerprint(renumbered)!r}")

# ...while two genuinely different messages must stay distinct.
a = {"from": {"addr": "submissions@formsubmit.co"}, "subject": "New AI tool submission — editorial review",
     "date": "2026-09-18 09:00+00:00", "id": "240", "_folder": "[Gmail]/All Mail"}
b = dict(a, date="2026-09-18 10:00+00:00")
distinct = h.fingerprint(a) != h.fingerprint(b)
failures += 0 if distinct else 1
print(f"{'PASS' if distinct else 'FAIL'}  genuinely different messages stay distinct")

print()
print(f"{len(CASES) + 2 - failures}/{len(CASES) + 2} passed")
sys.exit(1 if failures else 0)
