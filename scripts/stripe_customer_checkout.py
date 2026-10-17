#!/usr/bin/env python3
"""Rewrite committed customer pages from Whop checkout to the live Stripe links.

Idempotent. Admin packs and Whop CLI review pages are left alone.
"""
from __future__ import annotations

import re
from pathlib import Path

from premium_copy import (
    ACCESS_COPY,
    ACCESS_EMAIL,
    CANCEL_COPY,
    STRIPE_AUDIT_URL,
    STRIPE_PREMIUM_URL,
    audit_buy_html,
    upsell_module_html,
)

EXEMPT = {
    "tools/whop-cli/index.html",
    "comparisons/whop-cli-vs-zapier-ai.html",
    "comparisons/n8n-vs-whop-cli.html",
    "comparisons/make-vs-whop-cli.html",
    "comparisons/browse-ai-vs-whop-cli.html",
}

_CHECKOUT = re.compile(r"https://whop\.com/checkout/[^\"'\s<]*")
_MODULE = re.compile(
    r"<!-- AIT PREMIUM MODULE START -->.*?<!-- AIT PREMIUM MODULE END -->",
    re.S,
)
_AUDIT_TEXT = re.compile(r">([^<]*\$497[^<]*)</([a-zA-Z0-9]+)>")

_PHRASES = (
    ("Join Premium on Whop — 7-day trial · LAUNCH50", "Join Premium — 7-day trial · use code LAUNCH50 at checkout"),
    ("Join Premium on Whop ($12/mo)", "Join Premium — 7-day trial · use code LAUNCH50 at checkout"),
    ("Checkout without promo code", "use code LAUNCH50 at checkout"),
    ("https://whop.com/joined/aitoolsessentials-premium/", "mailto:" + ACCESS_EMAIL),
    ("If Whop shows you are in, open the Premium hub.", "You are in. Access arrives by email."),
    ("Open your Whop member hub — that is where Premium is delivered.", ACCESS_COPY + "."),
    ("How to join Premium on Whop", "How to join Premium"),
    ("Whop is checkout. These pages are a public preview.", "Stripe is checkout. These pages are a public preview."),
    ("The pack, alerts, written reply, and priority research slots are delivered in Whop.", ACCESS_COPY + "."),
    ("Premium on Whop", "Premium"),
    ("Subscribe on Whop", "Join Premium"),
    ("Cancel anytime from your Whop account", CANCEL_COPY),
    ("Cancel from your Whop account", CANCEL_COPY),
    ("Cancel anytime from Whop", CANCEL_COPY),
    ("Cancel in Whop", CANCEL_COPY),
    ("cancel in Whop", "cancel anytime from the link in your Stripe receipt email"),
    ("Optional Premium · $12/mo via Whop", "Optional Premium · $12/mo, secure checkout by Stripe"),
    ("$12/mo via Whop", "$12/mo, secure checkout by Stripe"),
    ("$12/month on Whop", "$12/month, secure checkout by Stripe"),
    ("$12/month via Whop", "$12/month, secure checkout by Stripe"),
    ("$12/month Whop membership", "$12/month membership"),
    ("Keep/cut research on Whop", "Keep/cut research, secure checkout by Stripe"),
    ("Paid · Whop", "Paid · Stripe"),
    ("48-hour written reply in Whop", "48-hour written reply by email"),
    ("written reply in Whop", "written reply by email"),
    ("reply in Whop", "reply by email"),
    ("Premium is delivered in Whop", ACCESS_COPY),
    ("delivered in Whop", "delivered by email from " + ACCESS_EMAIL + " within 24 hours"),
    ("Delivered in Whop", "Delivered by email"),
    ("lives in Whop", "arrives by email"),
    ("inside Whop", "by email"),
    ("Live in Whop", "Emailed"),
    ("What shows up in Whop", "What shows up by email"),
    ("Paid in Whop", "Paid access"),
    ("Whop members", "Premium members"),
    ("Whop membership", "Premium membership"),
    ("Whop charge", "Premium charge"),
    ("Whop checkout", "Premium checkout"),
    ("Whop returns you", "Stripe returns you"),
    ("Trust the Whop receipt", "Trust the Stripe receipt email"),
    ("If Whop shows", "If Stripe shows"),
    ("Open your AIToolsEssentials Premium hub", "Check the access email from " + ACCESS_EMAIL),
    ("Open AIToolsEssentials Premium hub", "Email " + ACCESS_EMAIL),
    ("AIToolsEssentials Premium hub", "access email"),
    ("handled by Whop", "handled by Stripe"),
    ("through Whop", "through Stripe"),
    ("via Whop", "secure checkout by Stripe"),
    ("from Whop", "from the access email"),
    ("in Whop", "by email"),
)


def _offer() -> dict:
    return {
        "price_usd_month": 12,
        "trial_period_days": 7,
        "promo_code": "LAUNCH50",
        "plan_id": "plan_FNXWs3suBFwDN",
    }


def _insert_audit_buttons(html: str) -> str:
    head, sep, body = html.partition("</head>")
    if not sep:
        head, body = "", html
    else:
        head = head + sep
    pieces: list[str] = []
    last = 0
    for match in _AUDIT_TEXT.finditer(body):
        pieces.append(body[last:match.end()])
        tag = match.group(2).lower()
        tail = "".join(pieces)[-800:]
        window = body[match.end(): match.end() + 800]
        if tag not in {"script", "style", "title"} and STRIPE_AUDIT_URL not in tail and STRIPE_AUDIT_URL not in window:
            pieces.append(" " + audit_buy_html())
        last = match.end()
    pieces.append(body[last:])
    return head + "".join(pieces)


def rewrite_customer_markup(text: str) -> str:
    module = upsell_module_html(_offer())
    text = _MODULE.sub(module, text)
    text = _CHECKOUT.sub(STRIPE_PREMIUM_URL, text)
    for old, new in _PHRASES:
        text = text.replace(old, new)
    return _insert_audit_buttons(text)


def exempt(rel: str) -> bool:
    return rel.startswith("admin/") or rel in EXEMPT or rel.startswith("tools/whop-cli/")


def apply(root: Path) -> int:
    changed = 0
    for path in sorted(root.rglob("*")):
        if path.suffix not in {".html", ".js"}:
            continue
        rel = path.relative_to(root).as_posix()
        if exempt(rel):
            continue
        original = path.read_text(errors="ignore")
        updated = rewrite_customer_markup(original)
        if updated != original:
            path.write_text(updated)
            changed += 1
    return changed


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    print("rewrote", apply(root))
