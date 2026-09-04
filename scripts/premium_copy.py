#!/usr/bin/env python3
"""Shared Premium purchase-story copy.

Path A: the free Stack Audit finds the waste. Premium is optional —
dated keep/cut pack + a 48-hour written reply in Whop when you want
help deciding before renewals. $12/month, cheaper than one overlapping
seat — not another AI subscription.

Public /premium/library/ pages are a preview of the format, not a gated
member area. Upgrade checkout uses the existing LAUNCH50 promo URL.
Do not invent plans, prices, trial days, or member counts.
"""
from __future__ import annotations

from typing import Any

EMAIL = "contact@aitoolsessentials.com"
PREVIEW_LABEL = "See a public preview"
BUY_PAGE_LABEL = "See Premium keep/cut pack"
FREE_AUDIT_LABEL = "Free Stack Audit"
FREE_EMAIL_LABEL = "Free Keep/Cut Weekly"
DEFAULT_HUB_URL = "https://whop.com/joined/aitoolsessentials-premium/"
DEFAULT_CHECKOUT = "https://whop.com/checkout/ch_DKm5yxA1OBXoDru/"
DEFAULT_CHECKOUT_PROMO = "https://whop.com/checkout/ch_DKm5yxA1OBXoDru/?promo=LAUNCH50"
WELCOME_PATH = "/premium/welcome/"


def esc(s: Any) -> str:
    return (
        str(s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def join_label(price: int | None = None, *, trial_days: int = 7, promo: str = "LAUNCH50") -> str:
    """Upgrade CTA after the free audit. $12/mo stays visible in nearby copy."""
    _ = price
    return f"Join Premium on Whop — {int(trial_days)}-day trial · {promo}"


def hub_url(whop: dict[str, Any] | None = None) -> str:
    if whop and whop.get("hub_url"):
        return str(whop["hub_url"])
    return DEFAULT_HUB_URL


def primary_checkout_url(whop: dict[str, Any]) -> str:
    return str(whop.get("checkout_promo_url") or DEFAULT_CHECKOUT_PROMO)


def plain_checkout_url(whop: dict[str, Any]) -> str:
    return str(whop.get("checkout_url") or DEFAULT_CHECKOUT)


def plain_checkout_link(whop: dict[str, Any]) -> str:
    return (
        f'<a class="checkout-plain-link" href="{esc(plain_checkout_url(whop))}" '
        'rel="external noopener">Checkout without promo code</a>'
    )


def lanes_note() -> str:
    return (
        '<p class="affiliate-inline">'
        "The <strong>instant Stack Audit</strong> is free — that is how you find the waste. "
        "<strong>Keep/Cut Weekly</strong> is the free weekly email. "
        "<strong>Premium</strong> is optional: $12/month on Whop for the dated keep/cut pack "
        "and a 48-hour written reply when you want help before renewals. "
        "Cheaper than one overlapping seat. Not another AI subscription."
        "</p>"
    )


def path_a_pitch(price: int = 12) -> tuple[str, str, str]:
    """Premium page kicker, h1, subhead. Not “pay $12 to stop paying.”"""
    return (
        f"Optional Premium · ${int(price)}/month on Whop",
        "The free audit finds the waste. Premium is optional help before you renew.",
        "Run the instant Stack Audit first — no login. If you want a dated keep/cut pack "
        f"and a written reply within 48 hours, Premium is ${int(price)}/month on Whop. "
        "That is cheaper than one overlapping seat. It is not another AI subscription. "
        'The <a href="/stack-audit.html">instant Stack Audit</a>, the directory, and '
        '<a href="/newsletter/">Keep/Cut Weekly</a> stay free.',
    )


def post_audit_upgrade_html(whop: dict[str, Any] | None = None) -> str:
    """One paid upgrade after the free audit. No invented savings figures."""
    price = int((whop or {}).get("price_usd_month") or 12)
    trial = int((whop or {}).get("trial_period_days") or 7)
    promo = str((whop or {}).get("promo_code") or "LAUNCH50")
    href = esc(primary_checkout_url(whop or {"checkout_promo_url": DEFAULT_CHECKOUT_PROMO}))
    return (
        '<section class="score-card sa-premium-upsell">'
        "<span>Optional next step</span>"
        "<h3>Want a keep/cut pack and a written reply before you renew?</h3>"
        "<p>The scorecard above stays free. Premium is optional: dated keep/cut notes and a "
        "48-hour written reply in Whop when you want someone to decide with you. "
        f"${price}/month — cheaper than one overlapping seat, not another AI subscription.</p>"
        f'<p><a class="button button-blue" data-sa-cta href="{href}" rel="external noopener">'
        f"{esc(join_label(price, trial_days=trial, promo=promo))}</a></p>"
        f'<p class="sa-note">{trial}-day free trial, then ${price}/month. Code <strong>{esc(promo)}</strong> '
        "for 50% off the first paid month. We do not invent how much you will save. "
        "Use your own numbers from this audit.</p>"
        "</section>"
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


def preview_vs_paid_note() -> str:
    return (
        '<section class="score-card"><span>Public Premium preview</span>'
        "<h2>Preview = format only. Paid in Whop = the dated pack.</h2>"
        "<p><strong>Preview</strong> on this site is the format: sample brief, matrix, "
        "checklist, alerts, and worksheets. Pages are not gated. This static site cannot hide HTML.</p>"
        "<p><strong>Paid in Whop</strong> is the dated pack, tool-change alerts, a written keep/cut reply, "
        "and priority research slots. After checkout, Whop returns you to "
        f'<a href="{WELCOME_PATH}">{WELCOME_PATH}</a>. Open the '
        f'<a href="{esc(DEFAULT_HUB_URL)}" rel="external noopener">AIToolsEssentials Premium hub</a> '
        "with the email you used at checkout.</p>"
        "</section>"
    )


def preview_access_note(whop: dict[str, Any]) -> str:
    price = int(whop["price_usd_month"])
    trial = int(whop["trial_period_days"])
    promo = esc(whop["promo_code"])
    hub = esc(hub_url(whop))
    return (
        '<section class="score-card"><span>Public Premium preview</span>'
        "<h2>These pages are not gated. Premium is delivered in Whop.</h2>"
        "<p>You can read this preview without paying. This site is static, so it cannot hide HTML. "
        f"What you buy for ${price}/month lives in Whop: dated keep/cut research, the monthly "
        "decision matrix CSV, the weekly checklist, tool-change alerts, a stack-audit template "
        "with a strategy-only reply within 48 hours, an ROI worksheet, and priority research slots.</p>"
        f"<p>{trial}-day free trial, then ${price}/month. Code <strong>{promo}</strong> is 50% off "
        "the first paid month for new users. After checkout, open "
        f'<a href="{WELCOME_PATH}">{WELCOME_PATH}</a>, then the '
        f'<a href="{hub}" rel="external noopener">AIToolsEssentials Premium hub</a> '
        "with the email you used at checkout. The directory, Keep/Cut Weekly, and instant Stack Audit "
        f"stay free. Premium does not include {not_included_phrase()}.</p>"
        f'<p><a class="button button-blue" href="{esc(primary_checkout_url(whop))}" rel="external noopener">'
        f"{esc(join_label(price, trial_days=trial, promo=whop['promo_code']))}</a>"
        f'<a class="button button-dark" href="/premium/" style="margin-left:8px">{BUY_PAGE_LABEL}</a>'
        f'<a class="button button-dark" href="/subscribe/" style="margin-left:8px">{FREE_EMAIL_LABEL}</a>'
        f'<a class="button button-dark" href="/stack-audit.html" style="margin-left:8px">{FREE_AUDIT_LABEL}</a></p>'
        f'<p class="muted-small">Then ${price}/mo · {plain_checkout_link(whop)}</p>'
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
    trial = int(whop["trial_period_days"])
    promo = str(whop["promo_code"])
    parts = [
        f'<a class="button button-blue" href="{esc(primary_checkout_url(whop))}" rel="external noopener" data-whop-checkout="{esc(whop["plan_id"])}">{esc(join_label(price, trial_days=trial, promo=promo))}</a>',
    ]
    if buy_page:
        parts.append(
            f'<a class="button button-ghost-dark" href="/premium/" style="margin-left:8px">{BUY_PAGE_LABEL}</a>'
        )
    if preview:
        parts.append(
            f'<a class="button button-ghost-dark" href="/premium/library/" style="margin-left:8px">{PREVIEW_LABEL}</a>'
        )
    if free_audit:
        parts.append(
            f'<a class="button button-ghost-dark" href="/stack-audit.html" style="margin-left:8px">{FREE_AUDIT_LABEL}</a>'
        )
    if extra:
        parts.append(extra)
    parts.append(
        f'<span class="muted-small" style="display:block;margin-top:10px">Then ${price}/mo · {plain_checkout_link(whop)}</span>'
    )
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
        f"<span>Optional Premium · ${price}/mo via Whop</span>"
        "<h2>Want someone to decide with you before a renewal?</h2>"
        f"<p>The free Stack Audit finds the waste. Premium is optional: a dated keep/cut pack, "
        "alerts, and a 48-hour written reply in Whop — ${price}/month, cheaper than one overlapping "
        "seat, not another AI subscription. The directory, Keep/Cut Weekly, and the instant Stack "
        "Audit stay free.</p>"
        f'<p class="affiliate-inline">{trial}-day free trial · then ${price}/month · code {promo} '
        "for 50% off first paid month · delivered in Whop · research and strategy only · "
        "affiliate status never changes recommendations.</p>"
        "</div><div class=\"newsletter-actions\">"
        f'<a class="button button-blue" href="{esc(primary_checkout_url(whop))}" rel="external noopener">'
        f"{esc(join_label(price, trial_days=trial, promo=whop['promo_code']))}</a>"
        f'<a class="button button-dark" href="/premium/">{BUY_PAGE_LABEL}</a>'
        '<a class="button button-dark" href="/premium/faq.html">FAQ</a>'
        "</div></section>\n"
        "<!-- AIT PREMIUM MODULE END -->"
    )


def homepage_hero_actions_html(whop: dict[str, Any]) -> str:
    _ = whop
    return (
        '<div class="actions">'
        f'<a class="button button-blue" href="/stack-audit.html">{FREE_AUDIT_LABEL}</a>'
        "</div>"
        '<p class="hero-secondary-links">'
        f'Optional: <a href="/premium/">{BUY_PAGE_LABEL}</a> when you want help before renewals.'
        "</p>"
    )


def homepage_hero_html(whop: dict[str, Any]) -> str:
    """Homepage hero only: overlap/cancel H1, Stack Audit primary, Premium secondary line."""
    actions = homepage_hero_actions_html(whop)
    return f'''    <section class="hero scene scene-dark">
      <div class="hero-copy">
        <p class="kicker">You are paying for overlapping AI tools.</p>
        <h1>Find overlapping AI subscriptions — and what to cancel.</h1>
        <p class="subhead">Run a free Stack Audit on this device. Keep one tool per job. Cancel the rest before renewal.</p>
        {actions}
      </div>
      <div class="hero-device" aria-hidden="true">
        <div class="device-window">
          <div class="window-bar"><span></span><span></span><span></span></div>
          <div class="search-line">Find overlapping subscriptions</div>
          <div class="result-card active"><b>Keep one</b><span>The seat that does this week&apos;s job</span><em>Free audit</em></div>
          <div class="result-card"><b>Cut overlap</b><span>Same job, second subscription</span><em>Cancel before renewal</em></div>
          <div class="result-card"><b>Optional pack</b><span>Keep/cut notes + 48-hour reply</span><em>Premium</em></div>
        </div>
      </div>
    </section>'''


def homepage_header_html() -> str:
    """Slim homepage header. Inner pages keep their own nav."""
    return (
        '<header class="global-nav" aria-label="Primary navigation" data-nav="slim">'
        '<a class="brand" href="/" aria-label="AIToolsEssentials home"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a>'
        '<nav class="nav-links">'
        '<a href="/stack-audit.html">Stack Audit</a>'
        '<a href="/premium/">Premium</a>'
        '<a href="/subscribe/">Subscribe</a>'
        '<a href="/tools/index.html">Tools</a>'
        "</nav>"
        f'<a class="nav-cta" href="/stack-audit.html">{FREE_AUDIT_LABEL}</a>'
        "</header>"
    )


def homepage_footer_html() -> str:
    """Short homepage utility footer. Inner pages keep their own footers."""
    return (
        '<footer class="footer" data-footer="slim">'
        "<span>© 2026 AIToolsEssentials</span>"
        '<a href="/tools/index.html">Tools</a>'
        '<a href="/pricing-watch/">Pricing Watch</a>'
        '<a href="/legal/about.html">About</a>'
        f'<a href="mailto:{EMAIL}">Contact</a>'
        '<a href="/legal/privacy.html">Privacy</a>'
        '<a href="/legal/terms.html">Terms</a>'
        "</footer>"
    )


def homepage_band_html(whop: dict[str, Any]) -> str:
    """One short Premium line — not a second sales page."""
    price = int(whop["price_usd_month"])
    trial = int(whop["trial_period_days"])
    return f"""<!-- AIT HOMEPAGE PREMIUM BAND START -->
<section class="scene scene-light home-premium-band">
<div>
<p class="kicker light">Optional Premium</p>
<p>Need a keep/cut pack and a 48-hour written reply before renewals? ${price}/month — cheaper than one overlapping seat, not another AI subscription.</p>
<p><a class="button button-blue" href="/premium/">{BUY_PAGE_LABEL}</a>
<a class="checkout-plain-link" href="{esc(primary_checkout_url(whop))}" rel="external noopener">{esc(join_label(price, trial_days=trial, promo=whop["promo_code"]))}</a></p>
</div>
</section>
<!-- AIT HOMEPAGE PREMIUM BAND END -->
"""
