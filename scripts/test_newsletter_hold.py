#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from newsletter_hold import (
    POSTAL_ADDRESS,
    SENDING_DOMAIN,
    UNSUBSCRIBE_HREF,
    Held,
    compliance_footer,
    email_compliance_footer,
    hold,
    subscribe_endpoint,
    subscribe_form,
)

REPO = Path(__file__).resolve().parent.parent
WORKERS_DEV = "https://aitools-newsletter-subscribe.example.workers.dev/"
LIVE_ENDPOINT = "https://aitools-newsletter-subscribe.aitoolsessentials.workers.dev"


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
    if UNSUBSCRIBE_HREF not in footer:
        errors.append("public footer lost the mailto unsubscribe")
    emailed = email_compliance_footer()
    if "{{{RESEND_UNSUBSCRIBE_URL}}}" not in emailed or UNSUBSCRIBE_HREF in emailed:
        errors.append("email footer is not the Resend unsubscribe URL")
    if POSTAL_ADDRESS not in emailed:
        errors.append("email footer missing the postal address")
    if SENDING_DOMAIN != "news.aitoolsessentials.com":
        errors.append("sending domain is not news.aitoolsessentials.com")
    closed = subscribe_form("")
    if "Signups open soon." not in closed or "aitoolsessentials@gmail.com" not in closed:
        errors.append("closed subscribe form missing the soon message")
    if "<form" in closed or "subscribe.news" in closed:
        errors.append("closed subscribe form still posts")
    if POSTAL_ADDRESS not in closed or "Unsubscribe" not in closed:
        errors.append("subscribe form missing the CAN-SPAM footer")
    dead = subscribe_form("https://subscribe.news.aitoolsessentials.com/")
    if dead != closed:
        errors.append("the Porkbun host was accepted as a signup action")
    opened = subscribe_form(WORKERS_DEV)
    if f'action="{WORKERS_DEV}"' not in opened:
        errors.append("open form action is not the workers.dev config value")
    if 'name="company_website"' not in opened or "confirm link" not in opened.casefold():
        errors.append("open form missing the honeypot or the confirm copy")
    if subscribe_endpoint(WORKERS_DEV) != WORKERS_DEV:
        errors.append("workers.dev URL was rejected")
    cfg = json.loads((REPO / "data" / "newsletter.json").read_text(encoding="utf-8"))
    if cfg.get("subscribe_endpoint") != LIVE_ENDPOINT:
        errors.append("committed subscribe_endpoint is not the live workers.dev URL")
    if subscribe_endpoint(cfg.get("subscribe_endpoint")) != LIVE_ENDPOINT:
        errors.append("committed endpoint did not parse as the live workers.dev URL")
    if cfg.get("send_enabled") is not False:
        errors.append("send_enabled must stay false")
    page = (REPO / "subscribe" / "index.html").read_text(encoding="utf-8")
    if f'action="{LIVE_ENDPOINT}"' not in page:
        errors.append("subscribe page action is not the live workers.dev URL")
    if "Signups open soon." in page:
        errors.append("subscribe page still says signups open soon")
    if 'name="company_website"' not in page or "confirm link" not in page.casefold():
        errors.append("subscribe page is missing the honeypot or the confirm copy")
    if "subscribe.news.aitoolsessentials.com" in page:
        errors.append("subscribe page posts to the Porkbun host")
    home = (REPO / "index.html").read_text(encoding="utf-8")
    panel = home[home.find("AIT HOMEPAGE NEWSLETTER START"): home.find("AIT HOMEPAGE NEWSLETTER END")]
    if f'action="{LIVE_ENDPOINT}"' not in panel:
        errors.append("homepage subscribe panel action is not the live workers.dev URL")
    if "Signups open soon." in panel:
        errors.append("homepage subscribe panel still says signups open soon")
    if panel.count('href="/subscribe/">Subscribe free') != 1:
        errors.append("homepage subscribe panel must keep one Subscribe free link")

    source = Path(__file__).resolve().with_name("newsletter_hold.py").read_text().lower()
    for word in ("beehiiv", "formsubmit", "requests", "urllib", "smtplib"):
        if word in source:
            errors.append("newsletter_hold.py contains " + word)
    chrome_path = Path(__file__).resolve().with_name("sponsor_chrome.py")
    if chrome_path.exists() and (
        "newsletter_hold" in chrome_path.read_text(encoding="utf-8") or "sponsor_chrome" in source
    ):
        errors.append("sponsor_chrome and newsletter_hold import each other")

    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
