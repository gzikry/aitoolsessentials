#!/usr/bin/env python3
"""Checks that paid Premium, free newsletter, and free Stack Audit stay distinct."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WHOP = "https://whop.com/checkout/ch_DKm5yxA1OBXoDru/"
PRODUCT = "https://whop.com/aitoolsessentials/aitoolsessentials-premium/"


def main() -> None:
    errors: list[str] = []
    cfg = json.loads((ROOT / "data" / "integrations.json").read_text())["whop"]
    if cfg["checkout_url"] != WHOP:
        errors.append("integrations.json checkout_url drifted from the live Premium checkout")
    if cfg["product_url"] != PRODUCT:
        errors.append("integrations.json product_url drifted from AIToolsEssentials Premium")
    if int(cfg["price_usd_month"]) != 12:
        errors.append("Do not invent a new Premium price")
    if cfg.get("plan_id") != "plan_FNXWs3suBFwDN":
        errors.append("Do not invent a new Whop plan id")

    home = (ROOT / "index.html").read_text()
    if WHOP not in home:
        errors.append("Homepage missing existing Whop Premium checkout")
    if "Join Premium on Whop ($12/mo)" not in home:
        errors.append("Homepage paid CTA is not labeled Join Premium on Whop ($12/mo)")
    subscribe = home[home.find('id="subscribe"'): home.find('id="subscribe"') + 1200]
    if WHOP in subscribe:
        errors.append("Homepage #subscribe still contains Whop checkout")

    checkout = (ROOT / "checkout/complete/index.html").read_text()
    if "Payment confirmed" in checkout:
        errors.append("Checkout complete still claims Payment confirmed")
    if "If Whop shows payment succeeded" not in checkout:
        errors.append("Checkout complete missing honest Whop wording")

    stack = (ROOT / "stack-audit.html").read_text()
    if "paid Premium" not in stack.lower() and "Paid Premium" not in stack and "See what $12 buys" not in stack:
        errors.append("Free Stack Audit page must label paid Premium separately")
    if "Keep/Cut Weekly" not in stack:
        errors.append("Free Stack Audit page must label the free newsletter")

    library = ROOT / "premium/library"
    for name in (
        "index.html",
        "research-brief.html",
        "decision-matrix.html",
        "stack-audit-template.html",
        "weekly-checklist.html",
        "tool-change-alerts.html",
        "roi-worksheet.html",
        "how-to-access.html",
    ):
        if not (library / name).exists():
            errors.append(f"Missing {name}")
    brief = (library / "research-brief.html").read_text()
    if "invented" not in brief.lower() and "No case studies" not in brief:
        errors.append("Research brief must refuse invented savings/case studies")
    if "Catch" not in brief and "Lily" not in brief:
        errors.append("Research brief must use dated digest tools, not invented ones")

    library_hub = (library / "index.html").read_text()
    if "public preview" not in library_hub.lower() and "not gated" not in library_hub.lower():
        errors.append("Library hub must say it is a public preview / not gated")
    if "delivered in Whop" not in library_hub and "delivered in Whop" not in library_hub.replace("\n", " "):
        if "lives in Whop" not in library_hub and "inside Whop" not in library_hub:
            errors.append("Library hub must say Premium is delivered in Whop")
    if "This is the $12/month Whop membership library" in library_hub:
        errors.append("Library hub still sells public HTML as the paid membership")
    if "George" in library_hub:
        errors.append("Library hub must not name George")

    access = (library / "how-to-access.html").read_text()
    if "George" in access:
        errors.append("how-to-access.html must not name George")

    pricing = (ROOT / "pricing/index.html").read_text()
    if "Instant Stack Audit" not in pricing and "free instant" not in pricing.lower():
        errors.append("Pricing must show the free Stack Audit lane")
    if "Join Premium on Whop ($12/mo)" not in pricing:
        errors.append("Pricing missing labeled Premium checkout")
    if "not a second product" not in pricing.lower() and "not a second paid" not in pricing.lower():
        errors.append("Pricing must say the written reply is not a second product")
    if WHOP not in pricing:
        errors.append("Pricing missing existing Whop checkout URL")

    sys.path.insert(0, str(ROOT / "scripts"))
    from generate_premium_membership import update_pricing_page

    tools = json.loads((ROOT / "data/tools.json").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        (tmp_root / "pricing").mkdir()
        (tmp_root / "pricing" / "index.html").write_text(pricing)
        update_pricing_page(tmp_root, tools)
        first = (tmp_root / "pricing" / "index.html").read_text()
        update_pricing_page(tmp_root, tools)
        second = (tmp_root / "pricing" / "index.html").read_text()
        if first != second:
            errors.append("update_pricing_page is not idempotent (Delivery/Scope spacing drifted)")
        if first.count("<strong>Scope:") != 1:
            errors.append("pricing page Scope label was lost or duplicated")

    premium = (ROOT / "premium/index.html").read_text()
    for heading in (
        "What you buy for $12/mo",
        "What you get this week",
        "What stays free",
        "What is not included",
    ):
        if heading not in premium:
            errors.append(f"premium/index.html missing heading {heading!r}")
    if "You are paying for overlapping AI tools" not in premium:
        errors.append("premium/index.html must lead with overlapping-tool money pain")
    if "Join Premium on Whop ($12/mo)" not in premium:
        errors.append("premium/index.html missing labeled Premium checkout")
    if "George" in premium:
        errors.append("premium/index.html must not name George")

    banned = [
        "operationalize the best AI tools",
        "Pay for the worksheets. Not the newsletter.",
        "Join the research membership — not the free email.",
        "The member library keeps compounding.",
        "Jarvis-dry",
        "strategy services",
        "overlap clusters",
        "A real member library from day one.",
        "Public member library",
        "This is the $12/month Whop membership library",
        "curated for outcomes",
        "member library as product",
    ]
    priority = [
        ROOT / "index.html",
        ROOT / "stack-audit.html",
        ROOT / "newsletter/index.html",
        ROOT / "subscribe/index.html",
        ROOT / "premium/index.html",
        ROOT / "premium/roadmap.html",
        ROOT / "premium/faq.html",
        ROOT / "premium/welcome/index.html",
        ROOT / "premium/archive.html",
        ROOT / "premium/library/index.html",
        ROOT / "premium/library/how-to-access.html",
        ROOT / "pricing/index.html",
        ROOT / "legal/terms.html",
        ROOT / "legal/privacy.html",
    ]
    for path in priority:
        if not path.exists():
            errors.append(f"Missing {path.relative_to(ROOT)}")
            continue
        text = path.read_text()
        for phrase in banned:
            if phrase in text:
                errors.append(f"{path.relative_to(ROOT)} still has {phrase!r}")
        if path.name != "integrations.json" and "George" in text and "premium" in str(path):
            errors.append(f"{path.relative_to(ROOT)} names George in public copy")

    if errors:
        raise SystemExit("premium clarity failures:\n- " + "\n- ".join(errors))
    print("premium clarity ok")


if __name__ == "__main__":
    main()
