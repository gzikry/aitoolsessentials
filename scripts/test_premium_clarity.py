#!/usr/bin/env python3
"""Checks that paid Premium, free newsletter, and free Stack Audit stay distinct."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WHOP = "https://whop.com/checkout/ch_DKm5yxA1OBXoDru/"
WHOP_PROMO = "https://whop.com/checkout/ch_DKm5yxA1OBXoDru/?promo=LAUNCH50"
PRODUCT = "https://whop.com/aitoolsessentials/aitoolsessentials-premium/"
HUB = "https://whop.com/joined/aitoolsessentials-premium/"
JOIN_LABEL = "Join Premium on Whop — 7-day trial · LAUNCH50"


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
    if WHOP_PROMO not in home:
        errors.append("Homepage missing LAUNCH50 promo checkout on the upgrade path")
    if "$12" not in home:
        errors.append("Homepage must keep $12/mo visible near Premium upgrade copy")
    if home.count(JOIN_LABEL) > 2:
        errors.append("Homepage repeats Join more than mid-page upgrade + footer")
    subscribe = home[home.find('id="subscribe"'): home.find('id="subscribe"') + 1200]
    if WHOP in subscribe or WHOP_PROMO in subscribe:
        errors.append("Homepage #subscribe still contains Whop checkout")
    hero = home[home.find('class="hero '): home.find("hero-device")]
    if 'href="/stack-audit.html">Free Stack Audit</a>' not in hero and 'href="/stack-audit.html">Free Stack Audit' not in hero:
        errors.append("Homepage hero primary CTA must be Free Stack Audit")
    if "Join Premium" in hero:
        errors.append("Homepage hero must not sell Join Premium as a primary CTA")
    if '<a class="button' in hero and "Build a starter list" in hero:
        starter = hero.find("Build a starter list")
        if starter != -1 and '<a class="button' in hero[max(0, starter - 80): starter]:
            errors.append("Homepage hero still promotes Build a starter list as a primary button")
    if "pay $12 to stop paying" in home.lower() or "Premium is $12/month to decide which ones to keep" in home:
        errors.append("Homepage still sells Premium as pay $12 to stop paying for AI")
    if "Three paths" in home or "Essential categories" in home or "AIT LEAD MAGNET" in home:
        errors.append("Homepage is still the fat pre-slim page")
    if home.count("AIT HOMEPAGE PREMIUM BAND START") != 1:
        errors.append("Homepage must keep exactly one Premium band")
    if home.count('id="subscribe"') != 1:
        errors.append("Homepage must keep exactly one #subscribe panel")

    checkout = (ROOT / "checkout/complete/index.html").read_text()
    if "Payment confirmed" in checkout or "You're in" in checkout:
        errors.append("Checkout complete still claims payment confirmation")
    if 'http-equiv="refresh"' not in checkout or "/premium/welcome/" not in checkout:
        errors.append("Checkout complete must redirect to /premium/welcome/")
    if "cannot verify a charge" not in checkout.lower() and "If Whop shows payment succeeded" not in checkout:
        errors.append("Checkout complete missing honest Whop wording")

    welcome = (ROOT / "premium/welcome/index.html").read_text()
    if HUB not in welcome:
        errors.append("Welcome page missing product hub deep link")
    if "https://whop.com/hub\"" in welcome or "https://whop.com/hub'" in welcome:
        errors.append("Welcome page still uses generic whop.com/hub")
    if "cannot verify a charge" not in welcome.lower():
        errors.append("Welcome page must say this page cannot verify a charge")

    stack = (ROOT / "stack-audit.html").read_text()
    if "paid Premium" not in stack.lower() and "Paid Premium" not in stack and "keep/cut pack" not in stack.lower() and "See Premium keep/cut pack" not in stack:
        errors.append("Free Stack Audit page must label paid Premium separately")
    if WHOP_PROMO not in stack:
        errors.append("Stack Audit post-result upgrade must use the LAUNCH50 checkout")
    if "You could save" in stack:
        errors.append("Stack Audit must not invent savings in the Premium upgrade CTA")
    if "200 audit" in stack.lower():
        errors.append("Do not invent audit-count metrics")
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
    if "public premium preview" not in library_hub.lower():
        errors.append("Library hub must be labeled Public Premium preview")
    if "public preview" not in library_hub.lower() and "not gated" not in library_hub.lower():
        errors.append("Library hub must say it is a public preview / not gated")
    if "format only" not in library_hub.lower():
        errors.append("Library hub must contrast preview format vs paid Whop pack")
    if HUB not in library_hub and HUB not in (library / "how-to-access.html").read_text():
        errors.append("Library must use the product hub deep link")
    if WHOP_PROMO not in library_hub:
        errors.append("Library hub missing LAUNCH50 promo checkout")
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
    if HUB not in access:
        errors.append("how-to-access.html missing product hub deep link")
    if "/premium/welcome/" not in access:
        errors.append("how-to-access.html must point post-purchase to /premium/welcome/")
    if "You're in" in access or "Payment confirmed" in access:
        errors.append("how-to-access.html has confirmation tone")

    pricing = (ROOT / "pricing/index.html").read_text()
    if "Instant Stack Audit" not in pricing and "free instant" not in pricing.lower():
        errors.append("Pricing must show the free Stack Audit lane")
    if JOIN_LABEL not in pricing:
        errors.append("Pricing missing labeled Premium checkout")
    if "not a second product" not in pricing.lower() and "not a second paid" not in pricing.lower():
        errors.append("Pricing must say the written reply is not a second product")
    if WHOP_PROMO not in pricing:
        errors.append("Pricing missing LAUNCH50 promo checkout URL")
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

    from generate_premium_membership import enhance_homepage
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        (tmp_root / "index.html").write_text(home)
        (tmp_root / "data").mkdir()
        (tmp_root / "data" / "voice_rewrites.json").write_text(
            (ROOT / "data" / "voice_rewrites.json").read_text()
        )
        (tmp_root / "data" / "newsletter.json").write_text(
            (ROOT / "data" / "newsletter.json").read_text()
        )
        (tmp_root / "data" / "integrations.json").write_text(
            (ROOT / "data" / "integrations.json").read_text()
        )
        enhance_homepage(tmp_root)
        first_home = (tmp_root / "index.html").read_text()
        enhance_homepage(tmp_root)
        second_home = (tmp_root / "index.html").read_text()
        if first_home != second_home:
            errors.append("enhance_homepage is not idempotent (second generate changed index.html)")
        if "Three paths" in first_home or "AIT LEAD MAGNET" in first_home:
            errors.append("enhance_homepage still emits the fat homepage")
        if 'href="/stack-audit.html">Free Stack Audit' not in first_home:
            errors.append("enhance_homepage dropped the Free Stack Audit CTA")

    premium = (ROOT / "premium/index.html").read_text()
    for heading in (
        "What you buy for $12/mo",
        "What you get this week",
        "What stays free",
        "What is not included",
    ):
        if heading not in premium:
            errors.append(f"premium/index.html missing heading {heading!r}")
    if "The free audit finds the waste" not in premium:
        errors.append("premium/index.html must lead with Path A: free audit finds waste")
    if "cheaper than one overlapping seat" not in premium.lower():
        errors.append("premium/index.html must use one-time-feeling value, not another AI subscription")
    if "Premium is $12/month to decide which ones to keep" in premium:
        errors.append("premium/index.html still sells pay $12 to stop paying")
    if JOIN_LABEL not in premium:
        errors.append("premium/index.html missing labeled Premium checkout")
    if WHOP_PROMO not in premium:
        errors.append("premium/index.html missing LAUNCH50 promo checkout")
    if "George" in premium:
        errors.append("premium/index.html must not name George")

    faq = (ROOT / "premium/faq.html").read_text()
    if HUB not in faq:
        errors.append("premium/faq.html missing product hub deep link")
    if "/premium/welcome/" not in faq:
        errors.append("premium/faq.html must point post-purchase to welcome")
    if "You're in" in faq or "Payment confirmed" in faq:
        errors.append("premium/faq.html has confirmation tone")
    if JOIN_LABEL not in faq:
        errors.append("premium/faq.html missing labeled Premium checkout")

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
        "Premium is $12/month to decide which ones to keep",
        "pay $12 to stop paying",
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
