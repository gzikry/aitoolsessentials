#!/usr/bin/env python3
"""Shared Premium purchase-story copy.

One offer: $12/month on Whop. Public /premium/library/ pages are a preview
of the format, not a gated member area. Import from generators only.
"""
from __future__ import annotations

from typing import Any

EMAIL = "contact@aitoolsessentials.com"
PREVIEW_LABEL = "See a public preview"
BUY_PAGE_LABEL = "See what $12 buys"
FREE_AUDIT_LABEL = "Free Stack Audit"
FREE_EMAIL_LABEL = "Free Keep/Cut Weekly"


def esc(s: Any) -> str:
    return (
        str(s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def join_label(price: int) -> str:
    return f"Join Premium on Whop (${int(price)}/mo)"


def lanes_note() -> str:
    return (
        '<p class="affiliate-inline">'
        "<strong>Keep/Cut Weekly</strong> is the free weekly email. "
        "The <strong>instant Stack Audit</strong> is free and stays on your device. "
        "<strong>Premium</strong> is $12/month on Whop."
        "</p>"
    )


def not_included_phrase() -> str:
    return (
        "implementation, setup, integrations, account access, credentials, "
        "or ongoing technical support"
    )


def what_you_buy_items(n_tools: int) -> list[str]:
    return [
        "Dated keep/cut research for the tools you already pay for",
        f"A monthly decision matrix CSV covering {n_tools} tracked tools",
        "A weekly 15-minute checklist",
        "Tool-change alerts when prices, plans, or model names move",
        "A stack-audit template plus a strategy-only written reply within 48 hours",
        "An ROI worksheet you fill with your own invoices and hours",
        "Priority research slots — first 5 complete requests each month",
    ]


def this_week_items() -> list[str]:
    return [
        "Open this week's keep/cut notes and the decision matrix CSV in Whop",
        "Run the 15-minute checklist on the tools you already pay for",
        "Fill the stack-audit template if you want a written keep/cut reply",
        "Reply in the request thread if you want a priority research slot",
    ]


def stays_free_items() -> list[str]:
    return [
        'The public directory of tool reviews and comparisons',
        'Keep/Cut Weekly — the free Beehiiv email at <a href="/subscribe/">/subscribe/</a>',
        'The instant Stack Audit at <a href="/stack-audit.html">/stack-audit.html</a> — no login, stays on your device',
    ]


def not_included_items() -> list[str]:
    return [
        "Implementation, setup, or integrations",
        "Account access, credentials, or API keys",
        "Ongoing technical support",
        "A login wall on this website — these HTML pages are a public preview",
        "Changes to public rankings, scores, or affiliate labels",
    ]


def preview_access_note(whop: dict[str, Any]) -> str:
    price = int(whop["price_usd_month"])
    trial = int(whop["trial_period_days"])
    promo = esc(whop["promo_code"])
    return (
        '<section class="score-card"><span>Public preview</span>'
        "<h2>These pages are not gated. Premium is delivered in Whop.</h2>"
        "<p>You can read this preview without paying. This site is static, so it cannot hide HTML. "
        f"What you buy for ${price}/month lives in Whop: dated keep/cut research, the monthly "
        "decision matrix CSV, the weekly checklist, tool-change alerts, a stack-audit template "
        "with a strategy-only reply within 48 hours, an ROI worksheet, and priority research slots.</p>"
        f"<p>{trial}-day free trial, then ${price}/month. Code <strong>{promo}</strong> is 50% off "
        "the first paid month for new users. Open the "
        '<a href="https://whop.com/hub" rel="external noopener">Whop member hub</a> '
        "with the email you used at checkout. The directory, Keep/Cut Weekly, and instant Stack Audit "
        f"stay free. Premium does not include {not_included_phrase()}.</p>"
        f'<p><a class="button button-blue" href="{esc(whop["checkout_url"])}" rel="external noopener">'
        f"{esc(join_label(price))}</a>"
        f'<a class="button button-dark" href="{esc(whop["checkout_promo_url"])}" rel="external noopener" style="margin-left:8px">'
        f"Use code {promo}</a>"
        f'<a class="button button-dark" href="/premium/" style="margin-left:8px">{BUY_PAGE_LABEL}</a>'
        f'<a class="button button-dark" href="/subscribe/" style="margin-left:8px">{FREE_EMAIL_LABEL}</a>'
        f'<a class="button button-dark" href="/stack-audit.html" style="margin-left:8px">{FREE_AUDIT_LABEL}</a></p>'
        "</section>"
    )


def buy_story_cards_html(n_tools: int) -> str:
    boxes = [
        ("What you buy for $12/mo", what_you_buy_items(n_tools), False),
        ("What you get this week", this_week_items(), False),
        ("What stays free", stays_free_items(), True),
        ("What is not included", not_included_items(), False),
    ]
    cards = []
    for title, items, allow_html in boxes:
        lis = "".join(
            f"<li>{item if allow_html else esc(item)}</li>" for item in items
        )
        cards.append(
            f'<article class="content-hub-card"><span>The purchase</span>'
            f"<h3>{esc(title)}</h3><ul>{lis}</ul></article>"
        )
    return f'<div class="content-hub-grid">{"".join(cards)}</div>'


def deliverable_cards_html(n_tools: int) -> str:
    cards = [
        ("Dated keep/cut research", "A dated brief on price, plan, and overlap changes for tools you already pay for. Delivered in Whop."),
        ("Monthly decision matrix CSV", f"One spreadsheet covering {n_tools} tracked tools: official price labels, category, and what each tool is for."),
        ("Weekly checklist", "Fifteen minutes. Check the tools on your bill. Make one keep, cut, or trial decision."),
        ("Tool-change alerts", "When a price, plan name, or model changes on a tool you pay for, the alert is in Whop."),
        ("Stack-audit template + written reply", "Fill the inventory. Send it. You get a strategy-only keep/cut/trial reply within 48 hours. No one logs into your accounts."),
        ("ROI worksheet", "You type your invoices and hours. The page does not invent savings."),
        ("Priority research slots", "The first 5 complete member requests each month become the next brief and CSV."),
    ]
    return "".join(
        f'<article class="content-hub-card"><span>Delivered in Whop</span>'
        f"<h3>{esc(title)}</h3><p>{esc(text)}</p></article>"
        for title, text in cards
    )


def checkout_buttons(
    whop: dict[str, Any],
    *,
    preview: bool = False,
    buy_page: bool = False,
    free_audit: bool = False,
    extra: str = "",
) -> str:
    price = int(whop["price_usd_month"])
    parts = [
        f'<a class="button button-blue" href="{esc(whop["checkout_url"])}" rel="external noopener" data-whop-checkout="{esc(whop["plan_id"])}">{esc(join_label(price))}</a>',
        f'<a class="button button-blue" href="{esc(whop["checkout_promo_url"])}" rel="external noopener" style="margin-left:8px">Use code {esc(whop["promo_code"])} — 50% off first paid month</a>',
    ]
    if buy_page:
        parts.append(
            f'<a class="button button-blue" href="/premium/" style="margin-left:8px">{BUY_PAGE_LABEL}</a>'
        )
    if preview:
        parts.append(
            f'<a class="button button-blue" href="/premium/library/" style="margin-left:8px">{PREVIEW_LABEL}</a>'
        )
    if free_audit:
        parts.append(
            f'<a class="button button-blue" href="/stack-audit.html" style="margin-left:8px">{FREE_AUDIT_LABEL}</a>'
        )
    if extra:
        parts.append(extra)
    return "".join(parts)


def billing_fine_print(whop: dict[str, Any]) -> str:
    price = int(whop["price_usd_month"])
    trial = int(whop["trial_period_days"])
    promo = esc(whop["promo_code"])
    return (
        f'<p class="affiliate-inline">{trial}-day free trial, then ${price}/month on the existing '
        f"AIToolsEssentials Premium checkout. Code <strong>{promo}</strong> is 50% off the first "
        "paid month for new users. Cancel in Whop. All sales are final — no refunds. "
        f"Premium is delivered in Whop. Research and strategy only — no {not_included_phrase()}. "
        "Affiliate or sponsor status never changes recommendations.</p>"
    )


def premium_nav_header() -> str:
    return (
        '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span>'
        "<span>AIToolsEssentials</span></a><nav class=\"nav-links\">"
        '<a href="/tools/index.html">Tools</a>'
        '<a href="/stack-audit.html">Free Stack Audit</a>'
        '<a href="/newsletter/">Keep/Cut Weekly</a>'
        '<a href="/premium/library/">Preview</a>'
        '<a href="/premium/">Premium</a>'
        "</nav>"
        '<a class="nav-cta" href="/pricing/">Paid Premium $12/mo</a></header>'
    )


def upsell_module_html(whop: dict[str, Any]) -> str:
    price = int(whop["price_usd_month"])
    trial = int(whop["trial_period_days"])
    promo = esc(whop["promo_code"])
    return (
        "<!-- AIT PREMIUM MODULE START -->\n"
        '<section class="newsletter-panel premium-conversion-panel"><div>'
        f"<span>Paid Premium · ${price}/mo via Whop</span>"
        "<h2>Paying for two tools that do the same job?</h2>"
        f"<p>Premium is ${price}/month on Whop. You get dated keep/cut research, a monthly "
        "decision matrix CSV, a weekly checklist, tool-change alerts, a written keep/cut reply, "
        "and priority research slots — delivered in Whop. The directory, Keep/Cut Weekly, and "
        "the instant Stack Audit stay free.</p>"
        f'<p class="affiliate-inline">{trial}-day free trial · then ${price}/month · code {promo} '
        "for 50% off first paid month · delivered in Whop · research and strategy only · "
        "affiliate status never changes recommendations.</p>"
        "</div><div class=\"newsletter-actions\">"
        f'<a class="button button-blue" href="{esc(whop["checkout_url"])}" rel="external noopener">'
        f"{esc(join_label(price))}</a>"
        f'<a class="button button-dark" href="/premium/">{BUY_PAGE_LABEL}</a>'
        '<a class="button button-dark" href="/premium/faq.html">FAQ</a>'
        "</div></section>\n"
        "<!-- AIT PREMIUM MODULE END -->"
    )


def homepage_band_html(whop: dict[str, Any]) -> str:
    price = int(whop["price_usd_month"])
    trial = int(whop["trial_period_days"])
    promo = esc(whop["promo_code"])
    return f"""<!-- AIT HOMEPAGE PREMIUM BAND START -->
<section class="scene scene-dark" style="padding:64px 28px">
<div style="max-width:1040px;margin:0 auto">
<p class="kicker light">Paid Premium · ${price}/month via Whop</p>
<h2 style="font-size:clamp(28px,4vw,42px)">You are paying for overlapping AI tools. Premium is ${price}/month to decide which ones to keep.</h2>
<p class="subhead">Join on Whop. You get dated keep/cut research, a monthly decision matrix CSV, a weekly checklist, tool-change alerts, a written keep/cut reply, and priority research slots. The directory, Keep/Cut Weekly, and the instant Stack Audit stay free.</p>
<ul style="max-width:740px;margin:20px 0 28px;line-height:1.6">
<li>{trial}-day free trial, then ${price}/month. Code <strong>{promo}</strong> = 50% off the first paid month (new users).</li>
<li>Free first: <a href="/stack-audit.html">run the instant Stack Audit</a> or <a href="/subscribe/">subscribe to Keep/Cut Weekly</a>.</li>
<li>Cancel in Whop. Research and strategy only — no {not_included_phrase()}. Affiliate status never changes recommendations.</li>
</ul>
<p><a class="button button-blue" href="{esc(whop["checkout_url"])}" rel="external noopener">{esc(join_label(price))}</a><a class="button button-ghost-dark" href="premium/" style="margin-left:8px">{BUY_PAGE_LABEL}</a><a class="button button-ghost-dark" href="pricing/" style="margin-left:8px">Free vs paid</a><a class="button button-ghost-dark" href="/stack-audit.html" style="margin-left:8px">{FREE_AUDIT_LABEL}</a></p>
</div></section>
<!-- AIT HOMEPAGE PREMIUM BAND END -->
"""
