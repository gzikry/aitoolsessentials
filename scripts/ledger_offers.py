"""Shared receipt footer for the calculators. Live Stripe URLs stay in premium_copy."""
from __future__ import annotations

DISCLOSURE = (
    "Independent math: our Keep/Test/Cut formulas are open-source in the page JS. "
    "Some outbound switch links may earn a partner commission at no cost to you."
)

# The $497 written audit is parked off the front door (2026-11-24). Its page stays live.
ALERT_LABEL = "Get an email when these prices change"
SPONSOR_LABEL = "Building an AI tool with transparent pricing? Book a Sponsored Category Audit slot"


def receipt_footer_html() -> str:
    return (
        '<div class="ledger-foot">'
        f"<p>{DISCLOSURE} "
        '<a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</p>'
        f'<p><a href="/price-changes/#price-alert">{ALERT_LABEL}</a>'
        ' · <a href="/pricing-watch/">Pricing watch</a></p>'
        f'<aside class="ledger-sponsor"><p><a href="/sponsor/">{SPONSOR_LABEL}</a></p></aside>'
        "</div>"
    )
