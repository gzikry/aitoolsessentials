from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal

__all__ = [
    "POSTAL_ADDRESS",
    "SENDING_DOMAIN",
    "SUBSCRIBE_ENDPOINT",
    "UNSUBSCRIBE_HREF",
    "Held",
    "compliance_footer",
    "hold",
    "subscribe_form",
]

_ON = frozenset({"1", "true", "yes", "on"})

POSTAL_ADDRESS = "1090 West Foothill, Claremont, CA 91711"
SENDING_DOMAIN = "news.aitoolsessentials.com"
SUBSCRIBE_ENDPOINT = "https://subscribe.news.aitoolsessentials.com/"
UNSUBSCRIBE_HREF = (
    "mailto:aitoolsessentials@gmail.com?subject=Unsubscribe%20Keep%2FCut%20Weekly"
)


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


def subscribe_form() -> str:
    return (
        '<form id="keep-cut-subscribe" method="post" action="'
        + SUBSCRIBE_ENDPOINT
        + '">'
        "<p>One email a week. We send a confirm link first. The list stays empty until you click it.</p>"
        '<p><label>Email <input type="email" name="email" autocomplete="email" required></label></p>'
        '<p class="subscribe-honeypot"><label>Company website <input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></p>'
        '<p><button class="button button-blue" type="submit">Get the free email</button></p>'
        "</form>"
        "<p>" + compliance_footer() + "</p>"
    )
