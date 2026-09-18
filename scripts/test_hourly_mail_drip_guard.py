#!/usr/bin/env python3
"""Prove the lifecycle-drip guard fires, and that it cannot suppress a real query.

A guard that never fires is indistinguishable from no guard, so each case asserts
the exact disposition (actionable True/False) rather than just "no crash".
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import hourly_mail_alert as h  # noqa: E402

CASES = [
    # (description, message, expected_actionable)
    (
        "the actual alert: Connectively 'Checking in' drip",
        {"from": {"addr": "community@connectively.us"}, "subject": "Checking in",
         "date": "2026-09-18 14:04+00:00", "id": "229", "_folder": "[Gmail]/All Mail"},
        False,
    ),
    (
        "Connectively 'Checking IN' cased differently",
        {"from": {"addr": "Community@Connectively.US"}, "subject": "CHECKING IN",
         "date": "x", "id": "1", "_folder": "[Gmail]/All Mail"},
        False,
    ),
    (
        "MUST STILL FIRE: an unrecognised Connectively subject (a possible query alert)",
        {"from": {"addr": "community@connectively.us"},
         "subject": "Query: AI subscription costs for a piece due Friday",
         "date": "x", "id": "2", "_folder": "[Gmail]/All Mail"},
        True,
    ),
    (
        "MUST STILL FIRE: a human replying as Re: to the drip",
        {"from": {"addr": "community@connectively.us"}, "subject": "Re: Checking in",
         "date": "x", "id": "3", "_folder": "[Gmail]/All Mail"},
        True,
    ),
    (
        "MUST STILL FIRE: a genuine FormSubmit vendor submission is untouched",
        {"from": {"addr": "submissions@formsubmit.co"},
         "subject": "New AI tool submission — editorial review",
         "date": "x", "id": "4", "_folder": "[Gmail]/All Mail"},
        True,
    ),
    (
        "MUST STILL FIRE: a DSN failure is untouched",
        {"from": {"addr": "mailer-daemon@googlemail.com"},
         "subject": "Delivery Status Notification (Failure)",
         "date": "x", "id": "5", "_folder": "[Gmail]/Spam"},
        True,
    ),
    (
        "connectively support 'Verify Your Email' drip",
        {"from": {"addr": "support@connectively.us"},
         "subject": "Verify Your Email on Connectively",
         "date": "x", "id": "6", "_folder": "[Gmail]/Trash"},
        False,
    ),
    (
        "MUST STILL FIRE: an unknown human sender",
        {"from": {"addr": "someone@example.com"}, "subject": "Hello",
         "date": "x", "id": "7", "_folder": "[Gmail]/All Mail"},
        True,
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

print()
print(f"{len(CASES) - failures}/{len(CASES)} passed")
sys.exit(1 if failures else 0)
