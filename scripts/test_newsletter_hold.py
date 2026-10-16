#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from newsletter_hold import (
    POSTAL_ADDRESS,
    SENDING_DOMAIN,
    SUBSCRIBE_ENDPOINT,
    Held,
    compliance_footer,
    hold,
    subscribe_form,
)


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
    if hold({"NEWSLETTER_SEND_ENABLED": "true"}) != Held("needs_approval"):
        errors.append('true without approval is not Held("needs_approval")')
    if hold({"NEWSLETTER_SEND_ENABLED": "YES"}) != Held("needs_approval"):
        errors.append("YES without approval is not needs_approval")
    if hold({"NEWSLETTER_SEND_ENABLED": " on "}) != Held("needs_approval"):
        errors.append("padded on without approval is not needs_approval")
    if hold({"NEWSLETTER_SEND_ENABLED": "1"}) != Held("needs_approval"):
        errors.append("1 without approval is not needs_approval")
    if hold({"NEWSLETTER_SEND_ENABLED": "true"}, approved=True) != Held("no_transport"):
        errors.append("approved true is not no_transport")
    if hold({"NEWSLETTER_SEND_ENABLED": "false"}, approved=True) != Held("disabled"):
        errors.append("approval does not override a disabled flag")
    footer = compliance_footer()
    if POSTAL_ADDRESS not in footer or "Unsubscribe" not in footer:
        errors.append("compliance footer missing the address or unsubscribe link")
    if SENDING_DOMAIN != "news.aitoolsessentials.com":
        errors.append("sending domain is not news.aitoolsessentials.com")
    form = subscribe_form()
    if SUBSCRIBE_ENDPOINT not in form or 'name="company_website"' not in form:
        errors.append("subscribe form is missing the worker or the honeypot")
    if "disabled" in form.split("</form>", 1)[0]:
        errors.append("subscribe form still disables the email field")
    if "confirm link" not in form.casefold():
        errors.append("subscribe form does not describe the confirm link")
    if POSTAL_ADDRESS not in form or "Unsubscribe" not in form:
        errors.append("subscribe form missing the CAN-SPAM footer")
    if SUBSCRIBE_ENDPOINT != "https://subscribe.news.aitoolsessentials.com/":
        errors.append("subscribe endpoint is not the newsletter host")

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
