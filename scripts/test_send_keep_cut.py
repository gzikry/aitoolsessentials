#!/usr/bin/env python3

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from newsletter_hold import POSTAL_ADDRESS, Held
from send_keep_cut import FROM_ADDRESS, Refused, email_html, send_issue

REPO = Path(__file__).resolve().parent.parent


def main() -> None:
    errors: list[str] = []
    root = Path(tempfile.mkdtemp())
    pack = root / "admin" / "newsletter"
    pack.mkdir(parents=True)
    shutil.copy(REPO / "admin" / "newsletter" / "2026-w42-draft.html", pack / "2026-w42-draft.html")
    shutil.copy(REPO / "admin" / "newsletter" / "2026-w42-subject.txt", pack / "2026-w42-subject.txt")
    calls: list[tuple[dict, str]] = []

    def post(payload: dict, key: str) -> dict:
        calls.append((payload, key))
        return {"id": "br_test"}

    held = send_issue(root, "2026-w42", {}, post=post)
    if held != Held("disabled") or calls:
        errors.append(f"flag off returned {held!r} with {calls!r}")
    held = send_issue(root, "2026-w42", {"NEWSLETTER_SEND_ENABLED": "true"}, post=post)
    if held != Held("needs_approval") or calls:
        errors.append(f"unapproved returned {held!r}")
    (pack / "2026-w42.approved").write_text("yes\n", encoding="utf-8")
    held = send_issue(root, "2026-w42", {"NEWSLETTER_SEND_ENABLED": "true"}, post=post)
    if held != Held("needs_approval") or calls:
        errors.append(f"wrong approval word returned {held!r}")
    (pack / "2026-w42.approved").write_text("approved\n", encoding="utf-8")
    held = send_issue(root, "2026-w42", {"NEWSLETTER_SEND_ENABLED": "true"}, post=post)
    if held != Held("no_transport") or calls:
        errors.append(f"missing key returned {held!r}")
    env = {
        "NEWSLETTER_SEND_ENABLED": "true",
        "RESEND_API_KEY": "test-key",
        "RESEND_SEGMENT_ID": "seg_test",
    }
    sent = send_issue(root, "2026-w42", env, post=post)
    if sent != {"id": "br_test"} or len(calls) != 1:
        errors.append(f"approved send returned {sent!r} calls={len(calls)}")
    else:
        payload, key = calls[0]
        if key != "test-key":
            errors.append(f"key was {key}")
        if payload["from"] != FROM_ADDRESS or payload["from"] != "Keep, Test, Cut <weekly@news.aitoolsessentials.com>":
            errors.append(f"from was {payload['from']}")
        if payload["subject"] != "ChatGPT Go is $8 a month":
            errors.append(f"subject was {payload['subject']}")
        if payload["segment_id"] != "seg_test" or payload["send"] is not True:
            errors.append(f"broadcast fields {payload['segment_id']!r} {payload['send']!r}")
        if payload["name"] != "Keep, Test, Cut 2026-w42":
            errors.append(f"name was {payload['name']}")
        html = payload["html"]
        if "{{{RESEND_UNSUBSCRIBE_URL}}}" not in html:
            errors.append("broadcast missing the Resend unsubscribe URL")
        if "mailto:aitoolsessentials@gmail.com?subject=Unsubscribe%20Keep%2C%20Test%2C%20Cut" in html:
            errors.append("broadcast still uses the mailto unsubscribe")
        if POSTAL_ADDRESS not in html or "\u2014 AIToolsEssentials" not in html:
            errors.append("broadcast missing the footer or the brand sign-off")
        if "george" in html.casefold():
            errors.append("broadcast uses a personal name")
    calls.clear()
    named = (pack / "2026-w42-draft.html").read_text(encoding="utf-8").replace("ChatGPT", "George")
    (pack / "2026-w99-draft.html").write_text(named, encoding="utf-8")
    (pack / "2026-w99-subject.txt").write_text("Nope\n", encoding="utf-8")
    (pack / "2026-w99.approved").write_text("approved\n", encoding="utf-8")
    refused = send_issue(root, "2026-w99", env, post=post)
    if refused != Refused("personal_name") or calls:
        errors.append(f"personal name returned {refused!r} calls={calls!r}")
    draft = (REPO / "admin" / "newsletter" / "2026-w43-draft.html").read_text(encoding="utf-8")
    try:
        html = email_html(draft)
    except ValueError as exc:
        errors.append(f"w43 draft refused: {exc}")
    else:
        if "{{{RESEND_UNSUBSCRIBE_URL}}}" not in html:
            errors.append("w43 broadcast missing the Resend unsubscribe URL")
        if POSTAL_ADDRESS not in html or "\u2014 AIToolsEssentials" not in html:
            errors.append("w43 broadcast missing the footer or the brand sign-off")
        if "george" in html.casefold():
            errors.append("w43 broadcast uses a personal name")
        if "mailto:aitoolsessentials@gmail.com?subject=Unsubscribe%20Keep%2C%20Test%2C%20Cut" in html:
            errors.append("w43 broadcast still uses the mailto unsubscribe")
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
