#!/usr/bin/env python3
"""Print only new actionable AIToolsEssentials mail; otherwise print nothing."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ACCOUNT = "aitools"
SPAM = "[Gmail]/Spam"
TRASH = "[Gmail]/Trash"
# All Mail covers the inbox; Spam catches misfiled form submissions; Trash matters
# because Gmail files some outbound mail and bounce replies there, which otherwise
# hides dead recipient domains indefinitely.
FOLDERS = ["[Gmail]/All Mail", SPAM, TRASH]
SELF = "aitoolsessentials@gmail.com"
# Every address we send *as*. Verification requests go out from the site's
# forwarder alias, and Gmail files a copy of each in All Mail; without this the
# monitor treats our own outbound mail as incoming and re-alerts on it.
SELF_ALIASES = {SELF, "contact@aitoolsessentials.com"}
STATE = Path.home() / ".local" / "state" / "aitoolsessentials" / "hourly-mail.json"

# Platform lifecycle/marketing drips that are never actionable on their own. Matched on the
# exact sender AND subject, deliberately — NOT by sender alone. Connectively sends its actual
# keyword/opportunity alerts from `community@connectively.us`, which is the one feed the
# journalist monitor exists to catch, so silencing the sender would blind the monitor.
# Observed onboarding drips 2026-09-03 → 2026-09-18: "Welcome to Connectively!" (Trash),
# "Verify Your Email on Connectively" (Trash, support@), "Create your Profile + best
# practices" (Trash), "Answer questions, get featured" (Trash), "Monitor Every Press
# Opportunity in One Place" (Trash), and "Checking in" (INBOX) — the last one raised this
# alert. Four of the six were already auto-filed to Trash. An unrecognised new subject still
# alerts, which is correct: a real query must never be suppressed, and an unknown drip costs
# one line of review to add here.
LIFECYCLE_DRIP_SUBJECTS = {
    ("community@connectively.us", "checking in"),
    ("community@connectively.us", "welcome to connectively!"),
    ("community@connectively.us", "create your profile + best practices"),
    ("community@connectively.us", "answer questions, get featured"),
    ("community@connectively.us", "monitor every press opportunity in one place"),
    ("support@connectively.us", "verify your email on connectively"),
}


def himalaya(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["himalaya", *args],
        capture_output=True,
        text=True,
        timeout=90,
    )


def list_messages(folder: str) -> list[dict]:
    result = himalaya(
        "envelope", "list", "--account", ACCOUNT,
        "--folder", folder, "--page", "1", "--page-size", "100",
        "--output", "json",
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "himalaya envelope list failed")
    messages = json.loads(result.stdout)
    for message in messages:
        message["_folder"] = folder
    return messages


def fingerprint(message: dict) -> str:
    """Stable identity for a message: sender + subject + date.

    Deliberately excludes the folder and the IMAP sequence id. Both are unstable
    for the *same* message: Gmail refiles mail between folders (a bounce can sit in
    Trash while its original lives in All Mail), and IMAP ids are per-folder UIDs,
    so one message has a different id in every folder it appears in. Including
    either made already-handled mail re-alert — the failure that produced a run of
    21 stale "actionable" items.

    Known and accepted limitation: two *distinct* messages that share a sender, a
    subject and the same minute collapse to one key, because himalaya's envelope
    date has minute resolution and carries no Message-ID. That is safe here — an
    alert is a notification aid, not the source of truth: every run re-lists the
    whole mailbox and dedupes against the hold ledger, so a collapsed duplicate
    cannot cause a missed action.
    """
    sender = (message.get("from") or {}).get("addr", "").lower()
    return "|".join([
        sender,
        (message.get("subject") or "").strip(),
        message.get("date") or "",
    ])


def bounce_detail(folder: str, message_id: str) -> str:
    """Extract the failed recipient and delivery status from a DSN.

    The bounced address is not in the envelope ``To:`` — it lives inside the
    attached ``message/delivery-status`` / ``message/rfc822`` parts, so the
    message has to be exported and parsed rather than grepped.
    """
    try:
        result = himalaya(
            "message", "export", str(message_id),
            "--account", ACCOUNT, "--folder", folder, "--full",
        )
        if result.returncode:
            return ""
        import email
        from email import policy
        msg = email.message_from_string(result.stdout, policy=policy.default)
        recipients: list[str] = []
        actions: list[str] = []
        statuses: list[str] = []
        for part in msg.walk():
            if part.get_content_type() == "message/delivery-status":
                payload = part.get_payload()
                if not isinstance(payload, list):
                    continue
                for sub in payload:
                    if not hasattr(sub, "get"):
                        continue
                    recipient = sub.get("Final-Recipient") or sub.get("Original-Recipient")
                    if recipient:
                        recipients.append(str(recipient).split(";")[-1].strip())
                    if sub.get("Action"):
                        actions.append(str(sub.get("Action")))
                    if sub.get("Status"):
                        statuses.append(str(sub.get("Status")))
        if not recipients:
            body = msg.get_body(preferencelist=("plain",))
            text = body.get_content() if body else ""
            for line in text.splitlines():
                if "delivering your message to" in line:
                    recipients.append(line.split("delivering your message to")[-1].strip().rstrip("."))
                    break
        fields = []
        if recipients:
            fields.append("Recipient: " + ", ".join(dict.fromkeys(recipients)))
        if actions:
            fields.append("Action: " + ", ".join(dict.fromkeys(actions)))
        if statuses:
            fields.append("Status: " + ", ".join(dict.fromkeys(statuses)))
        return " ".join(fields)
    except Exception:
        return ""


def disposition(message: dict) -> tuple[bool, str]:
    sender = (message.get("from") or {}).get("addr", "").lower()
    subject = (message.get("subject") or "").strip()
    lower = subject.lower()

    # Outbound mail we sent is never actionable, whichever address we sent it as.
    if sender in SELF_ALIASES:
        return False, ""
    # Bounces and delivery delays matter whatever folder Gmail filed them to.
    if sender in {"mailer-daemon@googlemail.com", "mailer-daemon@gmail.com"}:
        detail = bounce_detail(message.get("_folder") or FOLDERS[0], message.get("id"))
        if "delay" in lower:
            # A Delay is a retry notice, not a verdict: it becomes a Failure
            # later if the recipient is genuinely unreachable. Worth diagnosing,
            # never worth declaring a recipient dead on its own.
            reason = (
                "Delivery DELAY (not final — a Failure may follow). "
                "Resolve MX for the recipient domain before concluding anything."
            )
        else:
            reason = (
                "Delivery FAILURE (final). Inspect the recipient and error; "
                "do not retry unless a working address exists."
            )
        return True, f"{reason} {detail}".strip()
    if sender == "submissions@formsubmit.co":
        if "audit" in lower or "intake" in lower:
            return True, "New AI Stack Audit intake — review and respond within 24 hours."
        if "tool" in lower:
            return True, "New vendor submission — verify the product before publishing."
        if "test" in lower or "report" in lower:
            return True, "New community test report — verify before publishing."
        return True, "New website form submission — review the details."

    # Mail in Spam or Trash is only actionable from senders we already trust, or
    # when it is a real reply. Plain junk must stay silent or the monitor becomes noise.
    folder = message.get("_folder")
    if folder in (SPAM, TRASH):
        if lower.startswith("re:") or lower.startswith("fw:"):
            return True, "A correspondent replied — read the full thread and respond if needed."
        return False, ""

    if lower.startswith("re:") or lower.startswith("fw:"):
        return True, "A correspondent replied — read the full thread and respond if needed."
    if (sender, lower) in LIFECYCLE_DRIP_SUBJECTS:
        return False, ""
    if message.get("has_attachment"):
        return True, "New incoming attachment — inspect before taking action."

    # Unknown incoming human mail is actionable; common machine-only senders are silent.
    machine_markers = ("noreply", "no-reply", "notifications@", "newsletter", "updates@")
    if any(marker in sender for marker in machine_markers):
        return False, ""
    return True, "New incoming message — review and classify."


# Bump when the fingerprint shape changes: state written by an older shape can
# never match the new keys, so it is re-seeded instead of firing every message in
# the window as "new" on the first run after a code change.
STATE_VERSION = 2
# How many fingerprints to retain. The mailbox window is 100/folder, but retaining
# more than the live window means mail that scrolls out of view and back in later
# (a reply thread Gmail re-lists) still never re-alerts.
STATE_LIMIT = 5000


def load_seen() -> tuple[set[str], bool]:
    """Return (fingerprints, is_current_shape)."""
    try:
        payload = json.loads(STATE.read_text())
        if payload.get("version") != STATE_VERSION:
            return set(), False
        return set(payload.get("seen", [])), True
    except Exception:
        return set(), False


def save_seen(fingerprints: set[str]) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    kept = sorted(fingerprints)[-STATE_LIMIT:]
    STATE.write_text(
        json.dumps({"version": STATE_VERSION, "seen": kept}, indent=2) + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--initialize", action="store_true")
    args = parser.parse_args()

    try:
        messages = []
        for folder in FOLDERS:
            messages.extend(list_messages(folder))
        current = {fingerprint(message) for message in messages}
        seen, shape_current = load_seen()
        # A missing state file, --initialize, or a fingerprint-shape change all mean
        # "seed now, alert on nothing": we cannot tell old mail from new without a
        # baseline, and firing the whole window would bury a real alert in noise.
        if args.initialize or not shape_current:
            save_seen(current | seen)
            return 0

        alerts = []
        alerted: set[str] = set()
        for message in reversed(messages):
            key = fingerprint(message)
            # Skip mail already handled, and skip the second copy of a message that
            # Gmail exposes in more than one folder, so one mail alerts once.
            if key in seen or key in alerted:
                continue
            actionable, reason = disposition(message)
            if actionable:
                alerted.add(key)
                sender = (message.get("from") or {}).get("addr", "unknown sender")
                alerts.append(
                    f"ACTIONABLE EMAIL\n"
                    f"From: {sender}\n"
                    f"Subject: {message.get('subject') or '(no subject)'}\n"
                    f"Date: {message.get('date') or 'unknown'}\n"
                    f"Next: {reason}"
                )
        # Merge rather than replace: fingerprints outside the live window must
        # survive, or that mail re-alerts when Gmail lists it again.
        save_seen(seen | current)
        if alerts:
            print("\n\n".join(alerts))
        return 0
    except Exception as exc:
        print(f"MAIL MONITOR ERROR\nHourly email check failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
