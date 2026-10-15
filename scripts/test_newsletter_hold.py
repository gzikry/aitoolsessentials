#!/usr/bin/env python3
"""NEWSLETTER_SEND_ENABLED only produces a hold."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from newsletter_hold import Held, hold  # noqa: E402


def main() -> None:
    errors: list[str] = []
    if hold({}) != Held("disabled"):
        errors.append('hold({}) is not Held("disabled")')
    if hold({"NEWSLETTER_SEND_ENABLED": "false"}) != Held("disabled"):
        errors.append("false is not disabled")
    if hold({"NEWSLETTER_SEND_ENABLED": ""}) != Held("disabled"):
        errors.append("empty is not disabled")
    if hold({"NEWSLETTER_SEND_ENABLED": "0"}) != Held("disabled"):
        errors.append("0 is not disabled")
    if hold({"NEWSLETTER_SEND_ENABLED": "no"}) != Held("disabled"):
        errors.append("no is not disabled")
    if hold({"NEWSLETTER_SEND_ENABLED": "off"}) != Held("disabled"):
        errors.append("off is not disabled")
    if hold({"NEWSLETTER_SEND_ENABLED": "true"}) != Held("no_transport"):
        errors.append('true is not Held("no_transport")')
    if hold({"NEWSLETTER_SEND_ENABLED": "YES"}) != Held("no_transport"):
        errors.append("YES is not no_transport")
    if hold({"NEWSLETTER_SEND_ENABLED": " on "}) != Held("no_transport"):
        errors.append("padded on is not no_transport")
    if hold({"NEWSLETTER_SEND_ENABLED": "1"}) != Held("no_transport"):
        errors.append("1 is not no_transport")

    source = Path(__file__).resolve().with_name("newsletter_hold.py").read_text().lower()
    for word in ("beehiiv", "formsubmit", "requests", "urllib", "smtplib"):
        if word in source:
            errors.append("newsletter_hold.py contains " + word)
    chrome = Path(__file__).resolve().with_name("sponsor_chrome.py").read_text()
    if "newsletter_hold" in chrome or "sponsor_chrome" in source:
        errors.append("sponsor_chrome and newsletter_hold import each other")

    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
