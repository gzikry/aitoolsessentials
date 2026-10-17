#!/usr/bin/env python3
"""Live Stripe checkout for Premium and the written audit."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

PREMIUM_URL = "https://buy.stripe.com/bJe4gya2Bctf1lB02r0x203"
AUDIT_URL = "https://buy.stripe.com/cNi00ideNbpb8O32az0x204"
JOIN_LABEL = "Join Premium — 7-day trial · use code LAUNCH50 at checkout"
ACCESS_EMAIL = "aitoolsessentials@gmail.com"
CANCEL = "Cancel anytime from the link in your Stripe receipt email"

CHECKOUT_PAGES = (
    "premium/index.html",
    "index.html",
    "services/ai-stack-audit.html",
    "stack-audit.html",
    "js/stack-audit.js",
    "pricing/index.html",
    "start-here/index.html",
    "resources/index.html",
    "weekly/index.html",
    "tools/whop-cli/index.html",
    "comparisons/whop-cli-vs-zapier-ai.html",
    "comparisons/n8n-vs-whop-cli.html",
    "comparisons/make-vs-whop-cli.html",
    "comparisons/browse-ai-vs-whop-cli.html",
)

AUDIT_PAGES = (
    "premium/index.html",
    "services/ai-stack-audit.html",
    "services/paid-audit.html",
    "services/intake-questionnaire.html",
    "stack-audit.html",
    "pricing/index.html",
    "index.html",
)


def main() -> None:
    errors: list[str] = []
    try:
        from premium_copy import (
            STRIPE_AUDIT_URL,
            STRIPE_PREMIUM_URL,
            join_label,
            primary_checkout_url,
        )
    except ImportError:
        errors.append("premium_copy is missing STRIPE_PREMIUM_URL and STRIPE_AUDIT_URL")
        STRIPE_PREMIUM_URL = ""
        STRIPE_AUDIT_URL = ""
        join_label = None
        primary_checkout_url = None

    if STRIPE_PREMIUM_URL != PREMIUM_URL:
        errors.append("Premium checkout must be the live Stripe URL")
    if STRIPE_AUDIT_URL != AUDIT_URL:
        errors.append("Written audit checkout must be the live Stripe URL")
    if primary_checkout_url is not None:
        legacy = {"checkout_promo_url": "https://whop.com/checkout/ch_DKm5yxA1OBXoDru/?promo=LAUNCH50"}
        got = primary_checkout_url(legacy)
        if got != PREMIUM_URL:
            errors.append("primary checkout must ignore the legacy Whop promo URL")
        if "promo=" in got:
            errors.append("Premium checkout must not prefill a promo code")
    if join_label is not None and join_label(12, trial_days=7, promo="LAUNCH50") != JOIN_LABEL:
        errors.append("Join label must say use code LAUNCH50 at checkout")

    for rel in CHECKOUT_PAGES:
        text = (ROOT / rel).read_text()
        if PREMIUM_URL not in text:
            errors.append(rel + " missing the live Premium URL")
        if "whop.com/checkout" in text:
            errors.append(rel + " still links to whop.com/checkout")
        if "promo=LAUNCH50" in text:
            errors.append(rel + " still prefills LAUNCH50")
        if rel.startswith(("tools/whop-cli/", "comparisons/")) and JOIN_LABEL not in text:
            errors.append(rel + " missing the Stripe join label")

    tool_review = (ROOT / "tools/whop-cli/index.html").read_text()
    if "Is the Whop CLI free?" not in tool_review:
        errors.append("tools/whop-cli/index.html lost the product review copy")

    for rel in AUDIT_PAGES:
        text = (ROOT / rel).read_text()
        if "$497" in text and AUDIT_URL not in text:
            errors.append(rel + " mentions the $497 audit without the live buy link")

    welcome = (ROOT / "premium/welcome/index.html").read_text()
    access = (ROOT / "premium/library/how-to-access.html").read_text()
    for label, text in (("premium/welcome/index.html", welcome), ("premium/library/how-to-access.html", access)):
        if ACCESS_EMAIL not in text or "24 hours" not in text:
            errors.append(label + " must say access is emailed within 24 hours")
        if "whop.com" in text.lower():
            errors.append(label + " still points at Whop")
        if CANCEL not in text:
            errors.append(label + " missing the Stripe cancel sentence")

    for path in ROOT.rglob("*"):
        if path.suffix not in {".html", ".js"}:
            continue
        rel = path.relative_to(ROOT)
        if "admin" in rel.parts:
            continue
        if "whop.com/checkout" in path.read_text(errors="ignore"):
            errors.append(rel.as_posix() + " still links to whop.com/checkout")

    if errors:
        raise SystemExit("stripe premium failures:\n- " + "\n- ".join(errors))
    print("stripe premium ok")


if __name__ == "__main__":
    main()
