from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal

__all__ = [
    "POSTAL_ADDRESS",
    "SENDING_DOMAIN",
    "UNSUBSCRIBE_HREF",
    "Held",
    "compliance_footer",
    "hold",
    "public_colophon_html",
    "subscribe_endpoint",
    "subscribe_form",
]

_ON = frozenset({"1", "true", "yes", "on"})

POSTAL_ADDRESS = "1090 West Foothill, Claremont, CA 91711"
SENDING_DOMAIN = "news.aitoolsessentials.com"
UNSUBSCRIBE_HREF = (
    "mailto:aitoolsessentials@gmail.com?subject=Unsubscribe%20Keep%2FCut%20Weekly"
)
_SIGNUP_MAIL = "mailto:aitoolsessentials@gmail.com"


@dataclass(frozen=True, slots=True)
class Held:
    reason: Literal["disabled", "needs_approval", "no_transport"]

    def __post_init__(self) -> None:
        if self.reason not in ("disabled", "needs_approval", "no_transport"):
            raise ValueError("unknown hold reason")


def hold(env: Mapping[str, str] | None = None, *, approved: bool = False) -> Held:
    source = os.environ if env is None else env
    raw = source.get("NEWSLETTER_SEND_ENABLED", "")
    if not isinstance(raw, str) or raw.strip().casefold() not in _ON:
        return Held("disabled")
    if approved is not True:
        return Held("needs_approval")
    return Held("no_transport")


def compliance_footer() -> str:
    return (
        "AIToolsEssentials, "
        + POSTAL_ADDRESS
        + '. <a href="'
        + UNSUBSCRIBE_HREF
        + '">Unsubscribe</a>'
    )


def public_colophon_html() -> str:
    """Postal line for the homepage and the newsletter index. Emails carry the unsubscribe link."""
    return (
        '<span class="footer-colophon">Keep/Cut Weekly by AIToolsEssentials, '
        + POSTAL_ADDRESS
        + "</span>"
        '<span class="footer-colophon">Every email has an unsubscribe link.</span>'
    )


def subscribe_endpoint(value: object) -> str:
    """Accept only the workers.dev URL copied from Wrangler. Anything else stays closed."""
    if not isinstance(value, str):
        return ""
    raw = value.strip()
    if not raw.startswith("https://") or any(ch in raw for ch in " \t\r\n"):
        return ""
    host = raw[len("https://") :].split("/", 1)[0].split(":", 1)[0].lower()
    if "@" in host or not host.endswith(".workers.dev") or host == "workers.dev":
        return ""
    return raw


def subscribe_form(endpoint: str = "") -> str:
    action = subscribe_endpoint(endpoint)
    footer = "<p>" + compliance_footer() + "</p>"
    if not action:
        return (
            '<p id="keep-cut-subscribe">Signups open soon. Email '
            '<a href="' + _SIGNUP_MAIL + '">aitoolsessentials@gmail.com</a>.</p>'
            + footer
        )
    return (
        '<form id="keep-cut-subscribe" method="post" action="'
        + action
        + '">'
        "<p>One email a week. We send a confirm link first. The list stays empty until you click it.</p>"
        '<p><label>Email <input type="email" name="email" autocomplete="email" required></label></p>'
        '<p class="subscribe-honeypot"><label>Company website <input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></p>'
        '<p><button class="button button-blue" type="submit">Get the free email</button></p>'
        "</form>"
        + footer
    )
