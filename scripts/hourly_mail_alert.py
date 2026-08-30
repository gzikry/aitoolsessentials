#!/usr/bin/env python3
"""Print only new actionable AIToolsEssentials mail; otherwise print nothing."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ACCOUNT = "aitools"
FOLDER = "[Gmail]/All Mail"
SELF = "aitoolsessentials@gmail.com"
STATE = Path.home() / ".local" / "state" / "aitoolsessentials" / "hourly-mail.json"


def himalaya(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["himalaya", *args],
        capture_output=True,
        text=True,
        timeout=90,
    )


def list_messages() -> list[dict]:
    result = himalaya(
        "envelope", "list", "--account", ACCOUNT,
        "--folder", FOLDER, "--page", "1", "--page-size", "100",
        "--output", "json",
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "himalaya envelope list failed")
    return json.loads(result.stdout)


def fingerprint(message: dict) -> str:
    sender = (message.get("from") or {}).get("addr", "").lower()
    return "|".join([
        sender,
        message.get("subject") or "",
        message.get("date") or "",
        str(message.get("id") or ""),
    ])


def disposition(message: dict) -> tuple[bool, str]:
    sender = (message.get("from") or {}).get("addr", "").lower()
    subject = (message.get("subject") or "").strip()
    lower = subject.lower()

    if sender == SELF:
        return False, ""
    if sender in {"mailer-daemon@googlemail.com", "mailer-daemon@gmail.com"}:
        return True, "Delivery failure — inspect the bounced recipient and error."
    if sender == "submissions@formsubmit.co":
        if "audit" in lower or "intake" in lower:
            return True, "New AI Stack Audit intake — review and respond within 24 hours."
        if "tool" in lower:
            return True, "New vendor submission — verify the product before publishing."
        if "test" in lower or "report" in lower:
            return True, "New community test report — verify before publishing."
        return True, "New website form submission — review the details."
    if lower.startswith("re:") or lower.startswith("fw:"):
        return True, "A correspondent replied — read the full thread and respond if needed."
    if message.get("has_attachment"):
        return True, "New incoming attachment — inspect before taking action."

    # Unknown incoming human mail is actionable; common machine-only senders are silent.
    machine_markers = ("noreply", "no-reply", "notifications@", "newsletter", "updates@")
    if any(marker in sender for marker in machine_markers):
        return False, ""
    return True, "New incoming message — review and classify."


def load_seen() -> set[str]:
    try:
        return set(json.loads(STATE.read_text()).get("seen", []))
    except Exception:
        return set()


def save_seen(fingerprints: set[str]) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    # The current 100-message window is enough to prevent repeat alerts while bounding state.
    STATE.write_text(json.dumps({"seen": sorted(fingerprints)}, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--initialize", action="store_true")
    args = parser.parse_args()

    try:
        messages = list_messages()
        current = {fingerprint(message) for message in messages}
        seen = load_seen()
        if args.initialize or not seen:
            save_seen(current)
            return 0

        alerts = []
        for message in reversed(messages):
            key = fingerprint(message)
            if key in seen:
                continue
            actionable, reason = disposition(message)
            if actionable:
                sender = (message.get("from") or {}).get("addr", "unknown sender")
                alerts.append(
                    f"ACTIONABLE EMAIL\n"
                    f"From: {sender}\n"
                    f"Subject: {message.get('subject') or '(no subject)'}\n"
                    f"Date: {message.get('date') or 'unknown'}\n"
                    f"Next: {reason}"
                )
        save_seen(current)
        if alerts:
            print("\n\n".join(alerts))
        return 0
    except Exception as exc:
        print(f"MAIL MONITOR ERROR\nHourly email check failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
