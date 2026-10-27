"""Shared receipt footer for the calculators. Live Stripe URLs stay in premium_copy."""
from __future__ import annotations

from premium_copy import STRIPE_AUDIT_URL

DISCLOSURE = (
    "Independent math: our Keep/Test/Cut formulas are open-source in the page JS. "
    "Some outbound switch links may earn a partner commission at no cost to you."
)

AUDIT_LABEL = "Running a 5+ seat team? Get a Custom AI Stack & Seat Audit"
SPONSOR_LABEL = "Building an AI tool with transparent pricing? Book a Sponsored Category Audit slot"


def receipt_footer_html() -> str:
    return (
        '<div class="ledger-foot">'
        f"<p>{DISCLOSURE} "
        '<a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</p>'
        f'<p><a href="{STRIPE_AUDIT_URL}" rel="external noopener nofollow">{AUDIT_LABEL}</a>'
        ' · <a href="/pricing/">See it on the pricing page</a></p>'
        f'<aside class="ledger-sponsor"><p><a href="/sponsor/">{SPONSOR_LABEL}</a></p></aside>'
        "</div>"
    )
