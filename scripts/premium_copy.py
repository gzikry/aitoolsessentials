#!/usr/bin/env python3
"""Shared Premium purchase-story copy.

Path A: the free Stack Audit finds the waste. Premium is optional —
dated keep/cut pack + a 48-hour written reply in Whop when you want
help deciding before renewals. $12/month, cheaper than one overlapping
seat — not another AI subscription.

Public /premium/library/ pages are a preview of the format, not a gated
member area. Checkout is Stripe. LAUNCH50 is typed at checkout.
Payment links cannot prefill it. Do not invent plans, prices, trial
days, or member counts.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from newsletter_hold import public_colophon_html

EMAIL = "contact@aitoolsessentials.com"
PREVIEW_LABEL = "See a public preview"
BUY_PAGE_LABEL = "See Premium keep/cut pack"
FREE_AUDIT_LABEL = "Free Stack Audit"
FREE_EMAIL_LABEL = "Free Keep, Test, Cut"
ACCESS_EMAIL = "aitoolsessentials@gmail.com"
STRIPE_PREMIUM_URL = "https://buy.stripe.com/bJe4gya2Bctf1lB02r0x203"
STRIPE_AUDIT_URL = "https://buy.stripe.com/cNi00ideNbpb8O32az0x204"
CANCEL_COPY = "Cancel anytime from the link in your Stripe receipt email"
ACCESS_COPY = (
    "Access is delivered by email from aitoolsessentials@gmail.com within 24 hours"
)
DEFAULT_HUB_URL = "mailto:" + ACCESS_EMAIL
DEFAULT_CHECKOUT = STRIPE_PREMIUM_URL
DEFAULT_CHECKOUT_PROMO = STRIPE_PREMIUM_URL
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
    return f"Join Premium — {int(trial_days)}-day trial · use code {promo} at checkout"


def hub_url(whop: dict[str, Any] | None = None) -> str:
    _ = whop
    return DEFAULT_HUB_URL


def primary_checkout_url(whop: dict[str, Any] | None = None) -> str:
    _ = whop
    return STRIPE_PREMIUM_URL


def plain_checkout_url(whop: dict[str, Any] | None = None) -> str:
    _ = whop
    return STRIPE_PREMIUM_URL


def plain_checkout_link(whop: dict[str, Any] | None = None) -> str:
    promo = esc(str((whop or {}).get("promo_code") or "LAUNCH50"))
    return (
        f'<a class="checkout-plain-link" href="{esc(plain_checkout_url(whop))}" '
        f'rel="external noopener">use code {promo} at checkout</a>'
    )


def audit_buy_html() -> str:
    return (
        f'<a class="button button-blue" href="{STRIPE_AUDIT_URL}" target="_blank" '
        'rel="external noopener nofollow">Buy the written audit — $497</a>'
    )


def lanes_note() -> str:
    return (
        '<p class="affiliate-inline">'
        "The <strong>instant Stack Audit</strong> is free — that is how you find the waste. "
        "<strong>Keep, Test, Cut</strong> is the free weekly email. "
        "<strong>Premium</strong> is optional: $12/month, secure checkout by Stripe, for the dated keep/cut pack "
        "and a 48-hour written reply when you want help before renewals. "
        "Cheaper than one overlapping seat. Not another AI subscription."
        "</p>"
    )


def path_a_pitch(price: int = 12) -> tuple[str, str, str]:
    """Premium page kicker, h1, subhead. Not “pay $12 to stop paying.”"""
    return (
        f"Optional Premium · ${int(price)}/month, secure checkout by Stripe",
        "The free audit finds the waste. Premium is optional help before you renew.",
        "Run the instant Stack Audit first — no login. If you want a dated keep/cut pack "
        f"and a written reply within 48 hours, Premium is ${int(price)}/month, secure checkout by Stripe. "
        "That is cheaper than one overlapping seat. It is not another AI subscription. "
        'The <a href="/stack-audit.html">instant Stack Audit</a>, the directory, and '
        '<a href="/newsletter/">Keep, Test, Cut</a> stay free.',
    )


def post_audit_upgrade_html(whop: dict[str, Any] | None = None) -> str:
    """Two paid lanes after the free audit, stated as a real choice. No invented savings figures."""
    price = int((whop or {}).get("price_usd_month") or 12)
    trial = int((whop or {}).get("trial_period_days") or 7)
    promo = str((whop or {}).get("promo_code") or "LAUNCH50")
    href = esc(primary_checkout_url(whop or {"checkout_promo_url": DEFAULT_CHECKOUT_PROMO}))
    return (
        '<section class="score-card sa-premium-upsell">'
        "<span>Optional next step</span>"
        "<h3>Want a keep/cut pack and a written reply before you renew?</h3>"
        "<p>The scorecard above stays free. Premium is optional: dated keep/cut notes and a "
        "48-hour written reply by email when you want someone to decide with you. "
        f"${price}/month — cheaper than one overlapping seat, not another AI subscription.</p>"
        f'<p><a class="button button-blue" data-sa-cta href="{href}" rel="external noopener">'
        f"{esc(join_label(price, trial_days=trial, promo=promo))}</a></p>"
        f'<p class="sa-note">{trial}-day free trial, then ${price}/month. Code <strong>{esc(promo)}</strong> '
        "for 50% off the first paid month. We do not invent how much you will save. "
        "Use your own numbers from this audit.</p>"
        "</section>"
        # The written audit belongs here and nowhere more naturally: the reader has just
        # inventoried the stack and seen the overlap, which is exactly the input a $497 audit
        # needs. Offering only the $12 lane at this moment hid the higher-value service from
        # the warmest leads on the site.
        '<section class="score-card sa-paid-audit">'
        "<span>If a scorecard is not enough</span>"
        "<h3>Written AI Stack Audit — $497, one-time.</h3>"
        "<p>This scorecard tells you where the overlap is. It cannot tell you what the "
        "overlap costs, because it cannot see your invoices or renewal dates. The written "
        "audit is built from completed discovery plus public vendor documentation, priced "
        "against what you actually pay.</p>"
        "<p>What it includes: a direct answer to every workflow you named, a keep/cut/defer "
        "table with money attached, a deep pass on the one bottleneck you ranked, a Monday "
        "action per finding, and a 30-day sequence.</p>"
        '<p><a class="button button-ghost-dark" data-sa-cta href="/services/paid-audit.html">'
        "What the written audit adds</a> "
        f"{audit_buy_html()}"
        '<a class="text-link" data-sa-cta href="/services/audit-intake.html" '
        'style="margin-left:8px">Start the intake</a></p>'
        '<p class="sa-note">Strategy and written recommendations only. No implementation, no '
        "account access, no credentials or API keys. Discovery is required first — we say so "
        "before you pay rather than shipping a document full of gaps.</p>"
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
        "Open this week's keep/cut notes and the decision matrix CSV from the access email",
        "Run the 15-minute checklist on the tools you already pay for",
        "Fill the stack-audit template if you want a written keep/cut reply",
        "Reply in the request thread if you want a priority research slot",
    ]


def stays_free_items() -> list[str]:
    return [
        'The public directory of tool reviews and comparisons',
        'Keep, Test, Cut — the free weekly email at <a href="/subscribe/">/subscribe/</a>',
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
        "<h2>Preview = format only. Paid access is the dated pack.</h2>"
        "<p><strong>Preview</strong> on this site is the format: sample brief, matrix, "
        "checklist, alerts, and worksheets. Pages are not gated. This static site cannot hide HTML.</p>"
        "<p><strong>Paid access</strong> is the dated pack, tool-change alerts, a written keep/cut reply, "
        "and priority research slots. After checkout, Stripe returns you to "
        f'<a href="{WELCOME_PATH}">{WELCOME_PATH}</a>. {ACCESS_COPY}. {CANCEL_COPY}.</p>'
        "</section>"
    )


def preview_access_note(whop: dict[str, Any]) -> str:
    price = int(whop["price_usd_month"])
    trial = int(whop["trial_period_days"])
    promo = esc(whop["promo_code"])
    return (
        '<section class="score-card"><span>Public Premium preview</span>'
        "<h2>These pages are not gated. Premium is delivered by email.</h2>"
        "<p>You can read this preview without paying. This site is static, so it cannot hide HTML. "
        f"What you buy for ${price}/month arrives by email from {esc(ACCESS_EMAIL)}: dated keep/cut research, the monthly "
        "decision matrix CSV, the weekly checklist, tool-change alerts, a stack-audit template "
        "with a strategy-only reply within 48 hours, an ROI worksheet, and priority research slots.</p>"
        f"<p>{trial}-day free trial, then ${price}/month. Code <strong>{promo}</strong> is 50% off "
        "the first paid month for new users. Use code {promo} at checkout. After checkout, open "
        f'<a href="{WELCOME_PATH}">{WELCOME_PATH}</a>. {ACCESS_COPY}. {CANCEL_COPY}. '
        "The directory, Keep, Test, Cut, and instant Stack Audit "
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
        ("Dated keep/cut research", "A dated brief on price, plan, and overlap changes for tools you already pay for. Delivered by email."),
        ("Monthly decision matrix CSV", f"One spreadsheet covering {n_tools} tracked tools: official price labels, category, and what each tool is for."),
        ("Weekly checklist", "Fifteen minutes. Check the tools on your bill. Make one keep, cut, or trial decision."),
        ("Tool-change alerts", "When a price, plan name, or model changes on a tool you pay for, the alert arrives by email."),
        ("Stack-audit template + written reply", "Fill the inventory. Send it. You get a strategy-only keep/cut/trial reply within 48 hours. No one logs into your accounts."),
        ("ROI worksheet", "You type your invoices and hours. The page does not invent savings."),
        ("Priority research slots", "The first 5 complete member requests each month become the next brief and CSV."),
    ]
    return "".join(
        f'<article class="content-hub-card"><span>Delivered by email</span>'
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
        f'<a class="button button-blue" href="{esc(primary_checkout_url(whop))}" rel="external noopener">{esc(join_label(price, trial_days=trial, promo=promo))}</a>',
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
        f'<p class="affiliate-inline">{trial}-day free trial, then ${price}/month, secure checkout by Stripe. '
        f"Code <strong>{promo}</strong> is 50% off the first "
        f"paid month for new users. Use code {promo} at checkout. {CANCEL_COPY}. All sales are final — no refunds. "
        f"{ACCESS_COPY}. Research and strategy only — no {not_included_phrase()}. "
        "Affiliate or sponsor status never changes recommendations.</p>"
    )


def premium_nav_header() -> str:
    return (
        '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">ATE</span>'
        "<span>AIToolsEssentials</span></a><nav class=\"nav-links\">"
        '<a href="/tools/index.html">Tools</a>'
        '<a href="/stack-audit.html">Free Stack Audit</a>'
        '<a href="/newsletter/">Keep, Test, Cut</a>'
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
        f"<span>Optional Premium · ${price}/mo, secure checkout by Stripe</span>"
        "<h2>Want someone to decide with you before a renewal?</h2>"
        f"<p>The free Stack Audit finds the waste. Premium is optional: a dated keep/cut pack, "
        f"alerts, and a 48-hour written reply by email — ${price}/month, cheaper than one overlapping "
        "seat, not another AI subscription. The directory, Keep, Test, Cut, and the instant Stack "
        "Audit stay free.</p>"
        f'<p class="affiliate-inline">{trial}-day free trial · then ${price}/month · code {promo} '
        "for 50% off first paid month · use code LAUNCH50 at checkout · delivered by email · research and strategy only · "
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
        '<div class="actions home-appear" data-appear="5">'
        f'<a class="button home-cta-primary" href="/stack-audit.html">{FREE_AUDIT_LABEL}</a>'
        '<a class="button home-cta-ghost" href="/tools/index.html">Browse tools</a>'
        "</div>"
    )


def homepage_dateline_html() -> str:
    """Issue bar. Counts come from the catalog so the masthead cannot drift from the directory."""
    root = Path(__file__).resolve().parents[1]
    tools = json.loads((root / "data" / "tools.json").read_text(encoding="utf-8"))
    ledgers = sum(
        1
        for path in (root / "comparisons").glob("*.html")
        if "-vs-" in path.name
    )
    return (
        '<p class="home-dateline">INDEPENDENT AI SPEND &amp; TEARDOWN DESK'
        " · UPDATED OCT 26, 2026"
        f" · {len(tools)} TOOLS AUDITED"
        f" · {ledgers} HEAD-TO-HEAD LEDGERS"
        " · ZERO PAID RANKINGS</p>"
    )


def homepage_hero_html(whop: dict[str, Any]) -> str:
    """Copy-first homepage hero. Choose/learn with dated evidence first. No decorative device card."""
    actions = homepage_hero_actions_html(whop)
    return f'''    <section class="hero home-hero scene scene-dark">
      <div class="hero-copy">
        {homepage_dateline_html()}
        <p class="home-kicker home-appear" data-appear="2">Dated reviews, comparisons, and a free stack check</p>
        <h1><span class="home-line home-appear" data-appear="3">Stop paying for overlapping AI seats.</span> <span class="home-line home-deck home-appear" data-appear="4">Pick the seat that fits the job, not the <em>hype</em>.</span></h1>
        <p class="subhead home-appear" data-appear="4">You get dated evidence on the price, the credit clock, and the overlap. Check the date before you renew.</p>
        {actions}
        <p class="hero-secondary-links"><a href="#bill-slasher">30-second bill</a><a href="/compare/ai-coding-assistants/">Coding seats</a><a href="/compare/ai-app-builders/">App builders</a><a href="/compare/ai-video-avatar-cost/">Voice &amp; video</a><a href="/compare/automation-task-calculator/">Automation burn</a><a href="/compare/ai-presentation-cost/">Deck cost</a><a href="/compare/ai-customer-support-cost/">Support fees</a><a href="/pricing-watch/credit-traps/">Credit traps</a><a href="/price-changes/">Price changes</a></p>
      </div>
    </section>'''


def homepage_header_html() -> str:
    """Homepage nav from main: Tools, Search, Stack Audit, Premium, Subscribe."""
    from site_chrome import homepage_header

    return homepage_header()


def homepage_footer_html() -> str:
    """Short homepage utility footer. Inner pages keep their own footers."""
    return (
        '<footer class="footer" data-footer="slim">'
        "<span>© 2026 AIToolsEssentials</span>"
        '<a href="/tools/index.html">Tools</a>'
        '<a href="/newsletter/">Newsletter</a>'
        '<a href="/newsletter/">Keep, Test, Cut</a>'
        '<a href="/pricing-watch/">Pricing Watch</a>'
        '<a href="/legal/about.html">About</a>'
        f'<a href="mailto:{EMAIL}">Contact</a>'
        '<a href="/legal/privacy.html">Privacy</a>'
        '<a href="/legal/terms.html">Terms</a>'
        + public_colophon_html()
        + "</footer>"
    )


def homepage_learn_html() -> str:
    """Compact choose/learn strip. Real existing URLs only. No Premium CTA."""
    cards = (
        (
            "/pricing-watch/credit-traps/",
            "Credit expiry ledger",
            "65-day clocks, cancel locks, and what a half-used seat actually costs.",
            "Open the tracker",
            "home-learn-card home-learn-card-wide",
        ),
        (
            "/articles/chatgpt-vs-claude-which-is-better.html",
            "ChatGPT vs Claude",
            "Which assistant fits the week's work, not the brand.",
            "Read the comparison",
        ),
        (
            "/articles/cursor-vs-github-copilot-deep-comparison.html",
            "Cursor vs GitHub Copilot",
            "An IDE agent or inline completions. Pick one paid seat.",
            "Read the comparison",
        ),
        (
            "/comparisons/best-ai-tools.html",
            "Best AI tools",
            "A practical shortlist by job, not a ranked trophy list.",
            "See the shortlist",
        ),
    )
    card_html = "".join(
        f'<a class="{esc(card[4] if len(card) > 4 else "home-learn-card")}" href="{esc(card[0])}">'
        f"<h3>{esc(card[1])}</h3>"
        f"<p>{esc(card[2])}</p>"
        f'<span class="home-learn-card-link">{esc(card[3])}</span>'
        "</a>"
        for card in cards
    )
    return f"""<!-- AIT HOMEPAGE LEARN START -->
<section class="scene scene-dark home-learn" aria-labelledby="home-learn-heading">
<div class="home-learn-inner">
<p class="home-learn-kicker">Learn</p>
<h2 id="home-learn-heading">Choose with <em>dated evidence</em>, then keep or cut the overlap.</h2>
<div class="home-learn-cards">
{card_html}
</div>
<p class="home-learn-more">
<a href="/pricing-watch/">Pricing Watch</a>
<a href="/price-changes/">Price changes</a>
<a href="/compare/ai-coding-assistants/">Coding assistant cost</a>
<a href="/compare/ai-video-avatar-cost/">Voice and video minutes</a>
<a href="/compare/automation-task-calculator/">Automation burn</a>
<a href="/compare/ai-presentation-cost/">Deck cost</a>
<a href="/compare/ai-customer-support-cost/">Support fees</a>
<a href="/pricing-watch/credit-traps/">Credit traps</a>
<a href="/articles/">Articles</a>
<a href="/alternatives/">Alternatives</a>
</p>
</div>
</section>
<!-- AIT HOMEPAGE LEARN END -->
"""


def homepage_band_html(whop: dict[str, Any]) -> str:
    """One short Premium line — second opinion, not a cancel-only pitch."""
    price = int(whop["price_usd_month"])
    trial = int(whop["trial_period_days"])
    return f"""<!-- AIT HOMEPAGE PREMIUM BAND START -->
<section class="scene scene-dark home-premium-band">
<div>
<p class="kicker light">Want a second opinion before you renew?</p>
<p>Two ways to get one. Premium is the ${price}/month keep/cut pack. You get dated notes and a written reply in 48 hours, usually cheaper than one forgotten seat. If your stack is bigger than a pack can cover, the <a href="/services/paid-audit.html">written AI Stack Audit</a> is $497 one-time.</p>
<p class="home-premium-actions"><a class="button home-cta-primary" href="/premium/">{BUY_PAGE_LABEL}</a>
<a href="/services/paid-audit.html">Or see the $497 written audit</a>
{audit_buy_html()}
<a class="checkout-plain-link" href="{esc(primary_checkout_url(whop))}" rel="external noopener">{esc(join_label(price, trial_days=trial, promo=whop["promo_code"]))}</a></p>
</div>
</section>
<!-- AIT HOMEPAGE PREMIUM BAND END -->
"""
