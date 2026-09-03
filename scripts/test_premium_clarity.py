#!/usr/bin/env python3
"""Checks that paid Premium, free newsletter, and free Stack Audit stay distinct."""
from __future__ import annotations

import json
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
    if "paid Premium" not in stack.lower() and "Paid Premium" not in stack:
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

    pricing = (ROOT / "pricing/index.html").read_text()
    if "Instant Stack Audit" not in pricing and "free instant" not in pricing.lower():
        errors.append("Pricing must show the free Stack Audit lane")
    if "Join Premium on Whop ($12/mo)" not in pricing:
        errors.append("Pricing missing labeled Premium checkout")

    banned = [
        "operationalize the best AI tools",
        "The essential AI tools directory",
        "Pay for the research layer.",
        "Join the research membership — not the free email.",
        "The member library keeps compounding.",
        "Jarvis-dry",
        "strategy services",
        "overlap clusters",
    ]
    priority = [
        ROOT / "index.html",
        ROOT / "stack-audit.html",
        ROOT / "newsletter/index.html",
        ROOT / "subscribe/index.html",
        ROOT / "premium/index.html",
        ROOT / "premium/roadmap.html",
        ROOT / "pricing/index.html",
        ROOT / "legal/terms.html",
        ROOT / "legal/privacy.html",
    ]
    for path in priority:
        text = path.read_text()
        for phrase in banned:
            if phrase in text:
                errors.append(f"{path.relative_to(ROOT)} still has {phrase!r}")

    home_head = home.split("</head>", 1)[0]
    if "Stop paying for tools you do not use" not in home_head:
        errors.append("Homepage head missing second-person title")
    if "See which subscriptions you should keep" not in home_head:
        errors.append("Homepage head missing second-person description")
    for needle, label in (
        ('property="og:title" content="AIToolsEssentials — Stop paying for tools you do not use"', "og:title"),
        ('property="og:description" content="See which subscriptions you should keep, which you can cancel, and what to test this week."', "og:description"),
        ('name="twitter:title" content="AIToolsEssentials — Stop paying for tools you do not use"', "twitter:title"),
        ('name="twitter:description" content="See which subscriptions you should keep, which you can cancel, and what to test this week."', "twitter:description"),
        ('"name": "AIToolsEssentials — Stop paying for tools you do not use"', "JSON-LD name"),
        ('"description": "See which subscriptions you should keep, which you can cancel, and what to test this week."', "JSON-LD description"),
    ):
        if needle not in home_head:
            errors.append(f"Homepage head missing {label}")

    from generate_premium_membership import apply_homepage_voice_meta, homepage_voice_meta

    stale = """<!doctype html><html><head>
<meta name="description" content="AIToolsEssentials helps you discover, compare, and operationalize the best AI tools for real work." />
<title>AIToolsEssentials — The essential AI tools directory</title>
<!-- AIT SEO START -->
<meta property="og:title" content="AIToolsEssentials — The essential AI tools directory">
<meta property="og:description" content="AIToolsEssentials helps you discover, compare, and operationalize the best AI tools for real work.">
<meta name="twitter:title" content="AIToolsEssentials — The essential AI tools directory">
<meta name="twitter:description" content="AIToolsEssentials helps you discover, compare, and operationalize the best AI tools for real work.">
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "WebPage", "name": "AIToolsEssentials — The essential AI tools directory", "description": "AIToolsEssentials helps you discover, compare, and operationalize the best AI tools for real work.", "url": "https://aitoolsessentials.com/"}</script>
<!-- AIT SEO END -->
</head><body><h2>Stop paying for tools you do not use</h2></body></html>"""
    voice_title, voice_desc = homepage_voice_meta(ROOT)
    rewritten = apply_homepage_voice_meta(stale, voice_title, voice_desc)
    if "operationalize" in rewritten:
        errors.append("apply_homepage_voice_meta left operationalize in homepage meta")
    if "The essential AI tools directory" in rewritten:
        errors.append("apply_homepage_voice_meta left The essential AI tools directory")
    if voice_title not in rewritten or voice_desc not in rewritten:
        errors.append("apply_homepage_voice_meta did not set voice title/description")

    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if "admin" in rel.parts or any(part.startswith(".") for part in rel.parts):
            continue
        if "operationalize" in path.read_text().lower():
            errors.append(f"{rel} still says operationalize")

    if errors:
        raise SystemExit("premium clarity failures:\n- " + "\n- ".join(errors))
    print("premium clarity ok")


if __name__ == "__main__":
    main()
