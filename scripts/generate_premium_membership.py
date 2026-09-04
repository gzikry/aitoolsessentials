#!/usr/bin/env python3
"""Generate public premium pages and Whop-ready member content assets."""
from __future__ import annotations

import csv
import json
import re
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

from premium_copy import (
    BUY_PAGE_LABEL,
    DEFAULT_HUB_URL,
    PREVIEW_LABEL,
    WELCOME_PATH,
    path_a_pitch,
    billing_fine_print,
    buy_story_cards_html,
    checkout_buttons,
    deliverable_cards_html,
    homepage_band_html,
    homepage_footer_html,
    homepage_header_html,
    homepage_hero_actions_html,
    homepage_hero_html,
    hub_url,
    join_label,
    lanes_note,
    not_included_phrase,
    plain_checkout_link,
    premium_nav_header,
    primary_checkout_url,
    this_week_items,
    upsell_module_html,
    what_you_buy_items,
)

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
# Existing Whop Premium checkout only — do not invent new plan IDs or URLs.
WHOP_CHECKOUT = "https://whop.com/checkout/ch_DKm5yxA1OBXoDru/"
WHOP_CHECKOUT_PROMO = "https://whop.com/checkout/ch_DKm5yxA1OBXoDru/?promo=LAUNCH50"
WHOP_PRODUCT_URL = "https://whop.com/aitoolsessentials/aitoolsessentials-premium/"
WHOP_HUB = DEFAULT_HUB_URL
WHOP_PLAN_ID = "plan_FNXWs3suBFwDN"
WHOP_PROMO_CODE = "LAUNCH50"
WHOP_TRIAL_DAYS = 7
WHOP_PRICE = 12
JOIN_PREMIUM_LABEL = join_label(WHOP_PRICE, trial_days=WHOP_TRIAL_DAYS, promo=WHOP_PROMO_CODE)
HEADER = premium_nav_header()
FOOTER = f'<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/advertise/index.html" rel="nofollow">Advertise</a><a href="/submit-tool.html" rel="nofollow">Submit a tool</a><a href="/community/test-report.html" rel="nofollow">Report your results</a><a href="/badges/">Badges</a><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a></footer>'


def load_whop_from_integrations(root: Path) -> None:
    """Keep module constants aligned with data/integrations.json. Never invent new IDs."""
    global WHOP_CHECKOUT, WHOP_CHECKOUT_PROMO, WHOP_PRODUCT_URL, WHOP_HUB, WHOP_PLAN_ID, WHOP_PROMO_CODE, WHOP_TRIAL_DAYS, WHOP_PRICE, JOIN_PREMIUM_LABEL
    path = root / "data" / "integrations.json"
    if not path.exists():
        return
    cfg = json.loads(path.read_text()).get("whop") or {}
    if cfg.get("checkout_url"):
        WHOP_CHECKOUT = cfg["checkout_url"]
    if cfg.get("checkout_promo_url"):
        WHOP_CHECKOUT_PROMO = cfg["checkout_promo_url"]
    if cfg.get("product_url"):
        WHOP_PRODUCT_URL = cfg["product_url"]
    if cfg.get("hub_url"):
        WHOP_HUB = cfg["hub_url"]
    if cfg.get("plan_id"):
        WHOP_PLAN_ID = cfg["plan_id"]
    if cfg.get("promo_code"):
        WHOP_PROMO_CODE = cfg["promo_code"]
    if cfg.get("trial_period_days"):
        WHOP_TRIAL_DAYS = int(cfg["trial_period_days"])
    if cfg.get("price_usd_month"):
        WHOP_PRICE = int(cfg["price_usd_month"])
    JOIN_PREMIUM_LABEL = join_label(WHOP_PRICE, trial_days=WHOP_TRIAL_DAYS, promo=WHOP_PROMO_CODE)


def esc(s: Any) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def homepage_voice_meta(root: Path | None = None) -> tuple[str, str]:
    """Homepage title/description from data/voice_rewrites.json (second-person voice)."""
    root = root or Path(__file__).resolve().parent.parent
    title_tail = "Stop paying for tools you do not use"
    desc = "See which subscriptions you should keep, which you can cancel, and what to test this week."
    path = root / "data" / "voice_rewrites.json"
    if path.exists():
        data = json.loads(path.read_text())
        by_phrase = {item["phrase"]: item["rewrite"] for item in data.get("rewrites", [])}
        title_tail = by_phrase.get("The essential AI tools directory", title_tail)
        desc = by_phrase.get("operationalize the best AI tools", desc)
    return f"AIToolsEssentials — {title_tail}", desc


def apply_homepage_voice_meta(html: str, title: str | None = None, desc: str | None = None, root: Path | None = None) -> str:
    """Always SET homepage title/description/OG/Twitter/JSON-LD. Do not depend on leftover phrases."""
    if title is None or desc is None:
        title, desc = homepage_voice_meta(root)
    title_e = esc(title)
    desc_e = esc(desc)
    html = re.sub(r"(<title>)(.*?)(</title>)", rf"\1{title_e}\3", html, count=1, flags=re.S | re.I)
    html = re.sub(
        r'(<meta\b[^>]*\bname=["\']description["\'][^>]*\bcontent=")[^"]*(")',
        rf"\1{desc_e}\2",
        html,
        count=1,
        flags=re.I,
    )
    for attr, value in (
        ('property="og:title"', title_e),
        ('property="og:description"', desc_e),
        ('name="twitter:title"', title_e),
        ('name="twitter:description"', desc_e),
    ):
        html = re.sub(
            rf'(<meta\b[^>]*\b{re.escape(attr)}[^>]*\bcontent=")[^"]*(")',
            rf"\1{value}\2",
            html,
            flags=re.I,
        )
        html = re.sub(
            rf'(<meta\b[^>]*\bcontent=")[^"]*("[^>]*\b{re.escape(attr)})',
            rf"\1{value}\2",
            html,
            flags=re.I,
        )

    def rewrite_seo_block(match: re.Match[str]) -> str:
        block = match.group(0)

        def rewrite_script(sm: re.Match[str]) -> str:
            raw = sm.group(1)
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                return sm.group(0)
            if isinstance(data, dict) and data.get("@type") == "WebPage":
                data["name"] = title
                data["description"] = desc
                return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'
            return sm.group(0)

        return re.sub(
            r'<script type="application/ld\+json">(.*?)</script>',
            rewrite_script,
            block,
            flags=re.S,
        )

    return re.sub(
        r"<!-- AIT SEO START -->.*?<!-- AIT SEO END -->",
        rewrite_seo_block,
        html,
        count=1,
        flags=re.S,
    )


def head(title: str, desc: str, canonical: str, noindex: bool = False) -> str:
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{robots}<meta name="description" content="{esc(desc)}"><title>{esc(title)}</title><link rel="canonical" href="{canonical}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/css/styles.css"><link rel="stylesheet" href="/css/share.css"></head>'


def scripts() -> str:
    return '<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>'


def jsonld(data: dict[str, Any]) -> str:
    return '<script type="application/ld+json">' + json.dumps(data, separators=(",", ":")) + '</script>'


def category_top_tools(tools: list[dict[str, Any]], category: str, limit: int = 5) -> list[dict[str, Any]]:
    return sorted([t for t in tools if category.lower() in str(t.get("category", "")).lower()], key=lambda t: float(t.get("rating", 0) or 0), reverse=True)[:limit]


def _whop_dict() -> dict[str, Any]:
    return {
        "checkout_url": WHOP_CHECKOUT,
        "checkout_promo_url": WHOP_CHECKOUT_PROMO,
        "product_url": WHOP_PRODUCT_URL,
        "plan_id": WHOP_PLAN_ID,
        "promo_code": WHOP_PROMO_CODE,
        "trial_period_days": WHOP_TRIAL_DAYS,
        "price_usd_month": WHOP_PRICE,
        "hub_url": WHOP_HUB,
    }


def generate_public_pages(root: Path, tools: list[dict[str, Any]], today: str) -> None:
    out = root / "premium"
    out.mkdir(exist_ok=True)
    n_tools = len(tools)
    whop = _whop_dict()
    buy_list = "".join(f"<li>{esc(x)}</li>" for x in what_you_buy_items(n_tools))
    week_list = "".join(f"<li>{esc(x)}</li>" for x in this_week_items())
    kicker, pitch_h1, pitch_sub = path_a_pitch(WHOP_PRICE)
    desc = (
        f"The free Stack Audit finds the waste. Premium is optional: a dated keep/cut pack and a "
        f"48-hour written reply in Whop for ${WHOP_PRICE}/month — cheaper than one overlapping seat, "
        "not another AI subscription. Directory, Keep/Cut Weekly, and instant Stack Audit stay free."
    )
    page = f'''<!doctype html><html lang="en">{head("Premium — optional keep/cut pack after the free audit", desc, DOMAIN+"/premium/")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">{kicker}</p><h1>{pitch_h1}</h1><p class="subhead">{pitch_sub}</p><p>{checkout_buttons(whop, preview=True, free_audit=True)}</p>{billing_fine_print(whop)}{lanes_note()}</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
<h2>The purchase, in four boxes</h2>
{buy_story_cards_html(n_tools)}
<div class="score-card"><span>Delivered in Whop</span><h2>What $12/month is, without the jargon.</h2><ul>{buy_list}</ul><p>This week: </p><ul>{week_list}</ul><p><a class="button button-blue" href="{WHOP_CHECKOUT_PROMO}" rel="external noopener">{JOIN_PREMIUM_LABEL}</a><a class="button button-ghost-dark" href="/premium/library/" style="margin-left:8px">{PREVIEW_LABEL}</a><a class="button button-ghost-dark" href="/premium/faq.html" style="margin-left:8px">Premium FAQ</a><a class="button button-ghost-dark" href="/premium/roadmap.html" style="margin-left:8px">What shows up each month</a></p><p class="muted-small">Then ${WHOP_PRICE}/mo · {plain_checkout_link(whop)}</p></div>
<h2>Inside the Whop pack</h2>
<div class="content-hub-grid">{deliverable_cards_html(n_tools)}</div>
<section class="score-card"><span>What is not included</span><h2>Premium does not buy setup, logins, or rankings.</h2><p>You are buying dated research and a written keep/cut reply. Premium does not include {not_included_phrase()}. It does not change public editorial rankings, sponsor labels, affiliate disclosures, or review scores. The pages at <a href="/premium/library/">/premium/library/</a> are a public preview of the format. They are not gated.</p></section>
</div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "index.html").write_text(page)

    sample_tools = category_top_tools(tools, "General AI Assistant", 5) or tools[:5]
    rows = "".join(f'<tr><td><a href="/tools/{esc(t["slug"])}/">{esc(t["name"])}</a></td><td>{esc(t.get("price"))}</td><td>{esc(t.get("best_for"))}</td><td>{esc(t.get("summary"))}</td></tr>' for t in sample_tools)
    sample_desc = "Sample AIToolsEssentials Premium report showing the structure of monthly member briefings, decision matrices, and source-led recommendations."
    sample = f'''<!doctype html><html lang="en">{head("Sample Premium AI Tool Report", sample_desc, DOMAIN+"/premium/sample-report.html")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Public sample · keep/cut brief</p><h1>General AI assistant decision brief.</h1><p class="subhead">This public sample shows the format. If you join Premium for ${WHOP_PRICE}/month, you get the monthly pack, CSV files, stack-audit template, weekly checklist, tool-change alerts, and priority research slots in Whop.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT_PROMO}" rel="external noopener">{JOIN_PREMIUM_LABEL}</a><a class="button button-ghost-dark" href="/pricing/" style="margin-left:8px">Compare free vs paid</a><a class="button button-ghost-dark" href="/premium/library/" style="margin-left:8px">{PREVIEW_LABEL}</a></p><p class="muted-small">Then ${WHOP_PRICE}/mo · {plain_checkout_link(whop)}</p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Sample recommendation</span><h2>Pick by workflow, not by brand.</h2><p>For general AI assistants, the member report separates everyday drafting, source-backed research, long-context document work, coding help, and organization controls. The public sample is intentionally partial; members get the full source-dated matrix and CSV.</p></div><div class="table-wrap"><table><thead><tr><th>Tool</th><th>Pricing model</th><th>Best fit</th><th>Sample note</th></tr></thead><tbody>{rows}</tbody></table></div><h2>What full members receive</h2><div class="content-hub-grid"><article class="content-hub-card"><h3>Full matrix</h3><p>All {len(tools)} tracked tools scored across workflow fit, pricing pressure, data controls, and trial priority — refreshed monthly.</p></article><article class="content-hub-card"><h3>Stack audit + ROI tools</h3><p>Fillable audit template, weekly checklist, and ROI calculator so members cut overlap with a defensible process.</p></article><article class="content-hub-card"><h3>Hands-on protocols</h3><p>Identical-task comparison sheets for assistants, plus tool-change alerts before public pages catch up.</p></article><article class="content-hub-card"><h3>Priority research</h3><p>First 5 member requests each month become the next CSV + brief drop.</p></article></div></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "sample-report.html").write_text(sample)

    roadmap_desc = "AIToolsEssentials Premium monthly research roadmap and member deliverable calendar."
    roadmap_items = [
        ("September", "Cut AI subscription sprawl", "Decision matrix, general assistant shortlist, automation pricing decoder, vendor security questions."),
        ("October", "Visual and meeting stacks", "Refreshed decision matrix, visual AI shortlist, meeting-notes decision sheet, and pricing-watch handoff."),
        ("November", "Audit template, checklist, and alerts", "Stack-audit template, weekly checklist, tool-change alerts, ROI worksheet, and priority research slots."),
        ("December", "Content production stack", "ChatGPT, Claude, Jasper, Copy.ai, Canva AI, Descript, and distribution workflow playbook."),
        ("Ongoing", "Member-driven deep dives", "First 5 member requests each month become the next CSV + brief. Weekly checklist and alert feed refresh every month."),
    ]
    roadmap_cards = "".join(f'<article class="content-hub-card"><span>{esc(month)}</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>' for month, title, text in roadmap_items)
    roadmap = f'''<!doctype html><html lang="en">{head("Premium Research Roadmap", roadmap_desc, DOMAIN+"/premium/roadmap.html")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Premium roadmap</p><h1>What shows up in Whop each month.</h1><p class="subhead">Premium is not one PDF. Each month you get dated keep/cut notes, a refreshed decision matrix CSV, the weekly checklist, and tool-change alerts — delivered in Whop.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT_PROMO}" rel="external noopener">{JOIN_PREMIUM_LABEL}</a><a class="button button-ghost-dark" href="/premium/" style="margin-left:8px">{BUY_PAGE_LABEL}</a><a class="button button-ghost-dark" href="/premium/library/" style="margin-left:8px">{PREVIEW_LABEL}</a></p><p class="muted-small">Then ${WHOP_PRICE}/mo · {plain_checkout_link(whop)}</p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><h2>Research calendar</h2><div class="content-hub-grid">{roadmap_cards}</div><section class="score-card"><span>Member-driven</span><h2>Requests shape the calendar.</h2><p>Whop members can request workflows to compare. Good requests include your role, current stack, weekly task, budget, data constraints, and tools you are deciding between.</p></section></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "roadmap.html").write_text(roadmap)

    archive_desc = "AIToolsEssentials Premium archive preview for monthly AI tool research drops."
    archive_rows = "".join([
        '<tr><td>2026-09</td><td>AI stack cost-cutting brief</td><td>Decision matrix CSV, assistant shortlist, automation decoder, vendor questions</td><td>Live in Whop archive</td></tr>',
        '<tr><td>2026-10</td><td>Visual and meeting stacks</td><td>Refreshed matrix, visual shortlist, meeting-notes decision sheet</td><td>Live in Whop archive</td></tr>',
        '<tr><td>2026-11</td><td>Premium content engine</td><td>Stack audit, weekly checklist, alert feed, hands-on protocol, ROI calculator, 30-day calendar, value matrix, priority slots</td><td>Live in Whop (pinned welcome)</td></tr>',
        '<tr><td>2026-12</td><td>Content production stack</td><td>Writing/design/video workflow playbook and CSV archive</td><td>Planned</td></tr>',
    ])
    archive = f'''<!doctype html><html lang="en">{head("Premium Research Archive Preview", archive_desc, DOMAIN+"/premium/archive.html")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Premium archive</p><h1>Monthly drops, delivered in Whop.</h1><p class="subhead">A public preview of the monthly pack list. The files, posts, and request threads live inside Whop.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT_PROMO}" rel="external noopener">{JOIN_PREMIUM_LABEL}</a><a class="button button-ghost-dark" href="/premium/library/" style="margin-left:8px">{PREVIEW_LABEL}</a><a class="button button-ghost-dark" href="/premium/sample-audit.html" style="margin-left:8px">See sample audit</a></p><p class="muted-small">Then ${WHOP_PRICE}/mo · {plain_checkout_link(whop)}</p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="table-wrap"><table><thead><tr><th>Month</th><th>Drop</th><th>Member files</th><th>Status</th></tr></thead><tbody>{archive_rows}</tbody></table></div><section class="score-card"><span>Public preview</span><h2>This table is a preview. The files live in Whop.</h2><p>Billing and the monthly pack live in Whop. The pages at <a href="/premium/library/">/premium/library/</a> show the format. They are not gated. This static site cannot hide HTML.</p></section></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "archive.html").write_text(archive)

    faq_desc = "Premium membership FAQ for AIToolsEssentials Whop subscribers."
    faqs = [
        ("What do I buy for $12/month?", "Premium is delivered in Whop. You get dated keep/cut research, a monthly decision matrix CSV, a weekly checklist, tool-change alerts, a stack-audit template with a strategy-only written reply within 48 hours, an ROI worksheet, and priority research slots (first 5 complete requests each month)."),
        ("What do I get this week?", "After checkout, open /premium/welcome/. This page cannot verify a charge. If Whop shows the trial or payment succeeded, open the AIToolsEssentials Premium hub, download this week's keep/cut notes and the decision matrix CSV, run the 15-minute checklist, and fill the stack-audit template if you want a written keep/cut reply."),
        ("What stays free?", "The public directory, Keep/Cut Weekly (the Beehiiv email), and the instant Stack Audit at /stack-audit.html. Do not use the Whop checkout for those."),
        ("What is not included?", "Implementation, setup, integrations, account access, credentials, or ongoing technical support. Premium does not change public rankings, sponsor labels, or review scores. The /premium/library/ pages on this site are a public preview of the format. They are not gated."),
        ("Is Premium a course, community, or consulting service?", "No. You are buying dated research and a written keep/cut reply. Personalized stack recommendations from the audit template are strategy-only written replies — not hands-on implementation."),
        ("Can vendors pay to change rankings?", "No. Premium does not change public editorial rankings, sponsor labels, affiliate disclosures, or review scores."),
        ("How does billing and cancellation work?", "Billing, login, member access, and cancellation are handled by Whop. New members get a 7-day free trial, then $12/month. Use code LAUNCH50 for 50% off the first paid month (new users only). Cancel anytime from your Whop account."),
        ("Are refunds offered?", "No. All sales are final and there are no refunds. Use the 7-day free trial, the public preview, and the terms before you join."),
        ("How do member requests work?", "Post the workflow you want compared next. Include your role, current tools, weekly task, candidate tools, budget, and data constraints. The first 5 complete requests each month become priority research slots delivered as a CSV + brief in the next drop."),
        ("Is Premium worth $12/month?", "Only you can decide. It is useful if you already pay for multiple AI tools, have overlap, or have a renewal coming up, and you will use the checklist in week one. It is not useful if you only use one free assistant occasionally. Use the 7-day trial: if you have not made a keep/cut decision by day 7, cancel. We do not invent savings figures."),
    ]
    faq_items = "".join(f'<article class="content-hub-card"><h3>{esc(q)}</h3><p>{esc(a)}</p></article>' for q, a in faqs)
    faq_schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    product_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "AIToolsEssentials Premium",
        "description": "Paid $12/month Whop membership. Dated keep/cut research, monthly decision matrix CSV, weekly checklist, tool-change alerts, stack-audit template with a strategy-only written reply, ROI worksheet, and priority research slots. Delivered in Whop. Directory, Keep/Cut Weekly, and instant Stack Audit stay free.",
        "brand": {"@type": "Brand", "name": "AIToolsEssentials"},
        "image": DOMAIN + "/assets/og-ai-tools.jpg",
        "category": "Digital membership",
        "offers": {
            "@type": "Offer",
            "price": "12",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "url": WHOP_CHECKOUT,
            "category": "https://schema.org/DigitalDocument",
            "hasMerchantReturnPolicy": {
                "@type": "MerchantReturnPolicy",
                "applicableCountry": "US",
                "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                "merchantReturnDays": 7,
                "returnFees": "https://schema.org/FreeReturn",
                "refundType": "https://schema.org/FullRefund",
                "merchantReturnLink": DOMAIN + "/premium/faq.html",
            },
            "shippingDetails": {
                "@type": "OfferShippingDetails",
                "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "USD"},
                "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "US"},
                "deliveryTime": {
                    "@type": "ShippingDeliveryTime",
                    "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 0, "unitCode": "DAY"},
                    "transitTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 0, "unitCode": "DAY"},
                },
            },
        },
    }
    faq = f'''<!doctype html><html lang="en">{head("Premium Membership FAQ", faq_desc, DOMAIN+"/premium/faq.html")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Premium FAQ</p><h1>What you buy, what stays free, what is not included.</h1><p class="subhead">Plain answers on the $12/month Whop membership before anyone pays.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT_PROMO}" rel="external noopener">{JOIN_PREMIUM_LABEL}</a><a class="button button-ghost-dark" href="/premium/" style="margin-left:8px">{BUY_PAGE_LABEL}</a><a class="button button-ghost-dark" href="/stack-audit.html" style="margin-left:8px">Free Stack Audit</a></p><p class="muted-small">Then ${WHOP_PRICE}/mo · {plain_checkout_link(whop)}</p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{faq_items}</div><section class="score-card"><span>Access</span><h2>Premium is delivered in Whop. These pages are a public preview.</h2><p>Join through the existing AIToolsEssentials Premium checkout. After checkout, Whop returns you to <a href="{WELCOME_PATH}">{WELCOME_PATH}</a>. This site cannot verify a charge. If Whop shows the trial or payment succeeded, open the <a href="{WHOP_HUB}" rel="external noopener">AIToolsEssentials Premium hub</a> with that email for the pack, alerts, written reply, and request thread. The pages at <a href="/premium/library/">/premium/library/</a> show the format. They are not gated. This static site cannot hide HTML.</p></section></div></section>
</main>{FOOTER}{jsonld(faq_schema)}{jsonld(product_schema)}{scripts()}</body></html>'''
    (out / "faq.html").write_text(faq)

    welcome_dir = out / "welcome"
    welcome_dir.mkdir(exist_ok=True)
    welcome_desc = "Welcome to AIToolsEssentials Premium. Open your Whop member hub — that is where Premium is delivered."
    welcome = f'''<!doctype html><html lang="en">{head("Welcome to Premium", welcome_desc, DOMAIN+"/premium/welcome/")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Welcome</p><h1>If Whop shows you are in, open the Premium hub.</h1><p class="subhead">This page cannot verify a charge. If Whop shows the trial or payment succeeded, your Premium membership is on that email. Premium is delivered in Whop. The pages on this site are a public preview of the format.</p><p><a class="button button-blue" href="{WHOP_HUB}" rel="external noopener">Open AIToolsEssentials Premium hub</a><a class="button button-ghost-dark" href="/premium/onboarding/" style="margin-left:8px">7-day onboarding</a><a class="button button-ghost-dark" href="/premium/library/" style="margin-left:8px">{PREVIEW_LABEL}</a></p><p class="affiliate-inline">Billing, login, cancellation, and member access are handled by Whop. Research and strategy only — no {not_included_phrase()}.</p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Start here</span><h2>What to do in the first 15 minutes</h2><ol><li>Open the <a href="{WHOP_HUB}" rel="external noopener">AIToolsEssentials Premium hub</a>. That is where Premium is delivered.</li><li>Download this week's keep/cut notes and the decision matrix CSV.</li><li>Run the free instant <a href="/stack-audit.html">Stack Audit</a>, then fill the stack-audit template if you want a written keep/cut reply.</li><li>Reply in the request thread if you want a priority research slot this month.</li></ol></div></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (welcome_dir / "index.html").write_text(welcome)
    write_onboarding_page(root, whop)


def write_onboarding_page(root: Path, whop: dict[str, Any]) -> None:
    out = root / "premium" / "onboarding"
    out.mkdir(parents=True, exist_ok=True)
    hub = hub_url(whop)
    desc = "AIToolsEssentials Premium 7-day onboarding checklist: what to do each day during your free trial to get the most from the membership."
    page = f'''<!doctype html><html lang="en">{head("Premium 7-Day Onboarding Checklist — AIToolsEssentials", desc, DOMAIN+"/premium/onboarding/")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:880px;margin:0 auto;padding:88px 28px 40px;text-align:center"><p class="kicker light">Premium onboarding</p><h1>Make your first week count.</h1><p class="subhead">A 7-day rhythm for the Premium trial. This page cannot verify a charge. If Whop shows the trial or payment succeeded, start in the Premium hub.</p><p><a class="button button-blue" href="{esc(hub)}" rel="external noopener">Open AIToolsEssentials Premium hub</a><a class="button button-ghost-dark" href="{WELCOME_PATH}" style="margin-left:8px">Welcome / first 15 minutes</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
<div class="score-card"><span>Day 0</span><h2>Open the hub and grab your first file</h2><ul style="line-height:1.75;padding-left:18px"><li><a href="{esc(hub)}" rel="external noopener">Open your AIToolsEssentials Premium hub</a> with the email you used at checkout.</li><li>Download <strong>premium-tool-decision-matrix-2026-09.csv</strong> and open it in a spreadsheet.</li><li>Read the September cost-cutting brief in Whop.</li></ul></div>
<div class="score-card"><span>Day 1</span><h2>Tag every tool you pay for</h2><ul style="line-height:1.75;padding-left:18px"><li>Run the <a href="/stack-audit.html">free Stack Audit</a> first — it takes 3 minutes.</li><li>Transfer each paid tool into the Premium decision matrix CSV.</li><li>Tag each as <strong>Keep</strong> (weekly, clear owner, saves measurable time), <strong>Trial</strong> (needs a real-task test), or <strong>Cut/Defer</strong> (no owner, no recent use).</li></ul></div>
<div class="score-card"><span>Day 2</span><h2>Run one real-task test on every "Trial" tool</h2><ul style="line-height:1.75;padding-left:18px"><li>Pick one weekly task you do for real work (writing a client email, summarizing a meeting, generating an image, etc.).</li><li>Run the exact same task in each tool tagged "Trial."</li><li>Record editing burden — which tool reduces review time without increasing verification risk?</li></ul></div>
<div class="score-card"><span>Day 3</span><h2>Fill the stack-audit template if you want a written reply</h2><ul style="line-height:1.75;padding-left:18px"><li>Open the <a href="/premium/library/stack-audit-template.html">Premium stack-audit template</a> (public preview).</li><li>Fill the fields: every paid tool, cost, weekly usage, overlap, and a priority workflow you want tested.</li><li>Reply with your completed audit in the Whop member area. You get a strategy-only keep/cut/trial reply within 48 hours.</li></ul></div>
<div class="score-card"><span>Day 4</span><h2>Set one calendar reminder for every "Cut/Defer" tool</h2><ul style="line-height:1.75;padding-left:18px"><li>Check each cut/defer tool's renewal date on its official billing page.</li><li>Set a calendar reminder 48 hours before renewal.</li><li>Export your data from any tool you're about to cancel — don't wait until the last minute.</li></ul></div>
<div class="score-card"><span>Day 5</span><h2>Run the weekly checklist for the first time</h2><ul style="line-height:1.75;padding-left:18px"><li>Download the <strong>weekly-ai-stack-checklist.csv</strong> from Whop.</li><li>Follow the 15-minute rhythm: check alerts, test one tool, log one friction point, make one keep/cut decision.</li><li>This is the operating system that keeps the stack lean month after month.</li></ul></div>
<div class="score-card"><span>Day 6</span><h2>Decide: does Premium earn its $12?</h2><ul style="line-height:1.75;padding-left:18px"><li>Check your <strong>cancel-savings tracker</strong> — have you cut or deferred more than $12 in monthly AI spend?</li><li>If yes, keep going. If no, put a note to cancel in Whop before Day 7 so the trial doesn't convert.</li><li>Either way, reply in the Whop request thread with the workflow you want tested next.</li></ul></div>
<div class="score-card"><span>Day 7</span><h2>Keep or cancel — no regret either way</h2><ul style="line-height:1.75;padding-left:18px"><li>If Premium saved you time or money, let the trial convert. The next month's pack drops in Whop.</li><li>If it didn't, <a href="{esc(hub)}" rel="external noopener">cancel from your Whop account</a>. Access continues to the end of the paid period. All sales are final — no refunds.</li></ul></div>
<div class="score-card"><span>Scope</span><h2>Premium is research and strategy, not implementation</h2><p>Premium does not include setup, integrations, account access, credentials, or ongoing technical support. The stack-audit template gets you a written keep/cut/trial recommendation — not hands-on implementation.</p></div>
</div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "index.html").write_text(page)


def write_csv(path: Path, headers: list[str], rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(headers)
        w.writerows(rows)


def generate_whop_pack(root: Path, tools: list[dict[str, Any]], today: str) -> None:
    admin = root / "admin" / "whop-premium"
    admin.mkdir(parents=True, exist_ok=True)
    download_dir = admin / "files"
    download_dir.mkdir(exist_ok=True)

    sorted_tools = sorted(tools, key=lambda t: (str(t.get("category", "")), str(t.get("name", ""))))
    matrix_rows = []
    for t in sorted_tools:
        price = str(t.get("price", ""))
        pressure = "free-first" if "free" in price.lower() else "paid-only" if "paid" in price.lower() else "verify"
        matrix_rows.append([t.get("name"), t.get("slug"), t.get("category"), price, t.get("rating"), pressure, t.get("best_for"), t.get("summary")])
    write_csv(download_dir / "premium-tool-decision-matrix-2026-09.csv", ["name", "slug", "category", "pricing", "editorial_score", "pricing_pressure", "best_for", "summary"], matrix_rows)

    automation = [t for t in tools if "automation" in str(t.get("category", "")).lower() or t.get("slug") in {"zapier-ai", "make", "n8n"}]
    write_csv(download_dir / "automation-pricing-model-decoder-2026-09.csv", ["tool", "slug", "pricing", "best_for", "trial_test"], [[t.get("name"), t.get("slug"), t.get("price"), t.get("best_for"), "Map one real workflow; count task/operation/execution volume before annual billing."] for t in automation])

    assistant = [t for t in tools if "assistant" in str(t.get("category", "")).lower() or t.get("slug") in {"chatgpt", "claude", "gemini", "perplexity", "you-com", "mistral-le-chat", "deepseek"}]
    write_csv(download_dir / "general-ai-assistant-shortlist-2026-09.csv", ["tool", "slug", "pricing", "best_for", "member_note"], [[t.get("name"), t.get("slug"), t.get("price"), t.get("best_for"), "Run the same real task in each shortlisted assistant; compare editing burden and verification effort."] for t in assistant])

    # ---- October member pack (next month's drop, prepared ahead) ----
    write_csv(download_dir / "premium-tool-decision-matrix-2026-10.csv", ["name", "slug", "category", "pricing", "editorial_score", "pricing_pressure", "best_for", "summary"], matrix_rows)

    video = [t for t in tools if any(k in str(t.get("category", "")).lower() for k in ("video", "image")) or t.get("slug") in {"heygen", "synthesia", "midjourney", "leonardo-ai", "gamma"}]
    write_csv(download_dir / "visual-ai-tool-shortlist-2026-10.csv", ["tool", "slug", "pricing", "best_for", "member_note"], [[t.get("name"), t.get("slug"), t.get("price"), t.get("best_for"), "Test with one real brand-styled asset before committing; compare output acceptance rate, not just samples."] for t in video])

    meeting = [t for t in tools if t.get("slug") in {"fireflies", "otter-ai"} or "meeting" in str(t.get("category", "")).lower() or "transcript" in str(t.get("summary", "")).lower()]
    if meeting:
        write_csv(download_dir / "meeting-notes-decision-sheet-2026-10.csv", ["tool", "slug", "pricing", "best_for", "decision_question"], [[t.get("name"), t.get("slug"), t.get("price"), t.get("best_for"), "Does it handle your industry vocabulary and accents? Grade on real meetings only."] for t in meeting])

    oct_posts = "# AIToolsEssentials Premium - Whop Upload Pack - OCTOBER (" + today + ")\n\nPrepared ahead so the next monthly drop is upload-ready. Create these as Whop posts when October begins; attach CSVs from admin/whop-premium/files/.\n\n---\n\n## POST O1 - October drop: what changed since September\n\nWelcome to month two. This month focuses on visual/meeting tool decisions and the new public pricing tracker.\n\n**New files this month:**\n1. premium-tool-decision-matrix-2026-10.csv - refreshed decision matrix (" + str(len(tools)) + " tools).\n2. visual-ai-tool-shortlist-2026-10.csv - image/video generation shortlist.\n3. meeting-notes-decision-sheet-2026-10.csv - Fireflies vs Otter style decision sheet.\n\n**Also new on the public site:** AI Pricing Watch (https://aitoolsessentials.com/pricing-watch/) tracks verified price changes across all " + str(len(tools)) + " tools. Members get flagged summaries here first.\n\n---\n\n## POST O2 - October playbook: pick ONE visual AI and stop paying for three\n\nMost teams overlap Midjourney/Leonardo/HeyGen/Synthesia subscriptions. Use the visual shortlist CSV:\n1. List every visual AI you currently pay for.\n2. Score each against your actual monthly output volume.\n3. Cancel down to the single best fit; keep a free tier of a second only if genuinely used.\n\nReply with your current visual stack for a specific recommendation.\n\n---\n\n## POST O3 - October request thread\n\nPost the workflow you want researched next: role, current tools, weekly task volume, budget ceiling. October research slots fill in order of request.\n"
    (admin / "whop-posts-2026-10.md").write_text(oct_posts)

    # ---- November member pack: Premium content engine ----
    write_csv(download_dir / "premium-tool-decision-matrix-2026-11.csv", ["name", "slug", "category", "pricing", "editorial_score", "pricing_pressure", "best_for", "summary"], matrix_rows)

    write_csv(download_dir / "ai-stack-audit-template.csv", ["Field", "Your Answer", "Guidance"], [
        ["Your role/team size", "", "e.g. Solo consultant, 5-person agency, 20-person sales team"],
        ["Monthly AI spend (all tools)", "", "Sum all AI subscription costs"],
        ["Tool 1: Name", "", "e.g. ChatGPT Plus"],
        ["Tool 1: Monthly cost", "", "$/month"],
        ["Tool 1: Weekly use hours", "", "Estimate"],
        ["Tool 1: What it does for you", "", "One sentence"],
        ["Tool 1: Could it be replaced?", "", "By what? Or 'no'"],
        ["Tool 2: Name", "", ""],
        ["Tool 2: Monthly cost", "", ""],
        ["Tool 2: Weekly use hours", "", ""],
        ["Tool 2: What it does for you", "", ""],
        ["Tool 2: Could it be replaced?", "", ""],
        ["Tool 3: Name", "", ""],
        ["Tool 3: Monthly cost", "", ""],
        ["Tool 3: Weekly use hours", "", ""],
        ["Tool 3: What it does for you", "", ""],
        ["Tool 3: Could it be replaced?", "", ""],
        ["Tool 4: Name", "", ""],
        ["Tool 4: Monthly cost", "", ""],
        ["Tool 4: Weekly use hours", "", ""],
        ["Tool 4: What it does for you", "", ""],
        ["Tool 4: Could it be replaced?", "", ""],
        ["Tool 5: Name", "", ""],
        ["Tool 5: Monthly cost", "", ""],
        ["Tool 5: Weekly use hours", "", ""],
        ["Tool 5: What it does for you", "", ""],
        ["Tool 5: Could it be replaced?", "", ""],
        ["Biggest overlap (which tools do the same job?)", "", ""],
        ["Most expensive tool you rarely use", "", ""],
        ["One workflow you wish AI handled better", "", "Describe the task"],
        ["Privacy/data constraints", "", "Client data, HIPAA, NDA, etc."],
        ["Budget ceiling for AI tools", "", "$/month total you're willing to spend"],
        ["Cancellation risk (annual prepay?)", "", "Which tools lock you in annually?"],
    ])

    write_csv(download_dir / "weekly-ai-stack-checklist.csv", ["Day", "Task", "Why", "Done?"], [
        ["Mon", "Check tool-change alerts (pricing, plans, models)", "Catch changes before they affect your billing or workflow", ""],
        ["Mon", "Review any new tool submissions from AIToolsEssentials", "Stay aware of new options without spending hours researching", ""],
        ["Tue", "Run one real task in your primary AI assistant", "Keep muscle memory; notice if quality/limits shifted", ""],
        ["Wed", "Review your tool overlap matrix", "Is anything overlapping or unused this week?", ""],
        ["Thu", "Test one tool you're considering switching to", "One real task, not a demo", ""],
        ["Fri", "Check AIToolsEssentials change-radar for pricing/model updates", "Get the week's recorded changes in one scan", ""],
        ["Fri", "Log any limit-hits or friction from the week", "Data for next month's cancel/upgrade decisions", ""],
        ["Sun", "Decide: any cancellations or trials to start next week?", "Act on data, not impulse", ""],
    ])

    write_csv(download_dir / "tool-change-alert-feed-2026-11.csv", ["Date", "Tool", "Change Type", "Summary", "Action for Members", "Source"], [
        ["2026-11-01", "Cursor", "Model lineup", "Cursor Composer 2.5 now default on Pro; Grok 4.6 available as alternative model", "Test if Composer 2.5 changes your coding workflow; no action needed if current setup works", "Cursor changelog"],
        ["2026-11-01", "Grok", "Model lineup", "Grok 4.6 shipping; Grok Build and Grok Bot features expanded", "Evaluate if real-time X/web data adds value to your workflow vs existing assistants", "X/Grok official"],
        ["2026-11-01", "HtmlSlides", "New tool", "Interactive HTML presentation maker added to directory (vendor submission)", "Test as alternative to Gamma for browser-playable decks", "AIToolsEssentials review"],
        ["2026-11-01", "Whop CLI", "New tool", "Business CLI launched — programmatically manage products, pricing, ads, payouts", "If you sell on Whop, install and test the CLI for automated business management", "Whop blog"],
        ["2026-11-01", "All tools", "Pricing watch", f"Monthly pricing snapshot refreshed across {len(tools)} tools", "Review premium-tool-decision-matrix-2026-11.csv for any changes affecting your stack", "AIToolsEssentials pricing-watch"],
    ])

    write_csv(download_dir / "assistant-hands-on-comparison-2026-11.csv", ["Criterion", "ChatGPT", "Claude", "Grok", "Gemini"], [
        ["Plan checked", "Free/Plus/Pro (verify current)", "Free/Pro/Max (verify current)", "Free/Paid via X (verify current)", "Free/AI Pro/Ultra (verify current)"],
        ["Best for", "Breadth: images, files, voice, browsing in one place", "Long documents, careful prose, instruction adherence", "Real-time X/web data, always-on agents, image gen", "Google Workspace integration, multimodal"],
        ["File upload", "Yes — images, PDFs, spreadsheets", "Yes — documents, PDFs, code", "Limited (check official)", "Yes — docs, images, sheets"],
        ["Web access", "Yes (Plus+)", "Limited", "Yes — real-time X + web", "Yes — Google search integration"],
        ["Image generation", "Yes (native / DALL-E lineage)", "No or limited (check current)", "Yes (Imagine)", "Yes (Imagen)"],
        ["Code execution", "Yes (advanced data analysis)", "Yes (artifacts)", "Yes (Grok Build)", "Yes (code execution)"],
        ["Data training opt-out", "Available on Business/Enterprise", "Available on Team/Enterprise", "Check X/Grok privacy", "Available on paid tiers"],
        ["Offline mode", "No", "No", "No", "No"],
        ["Member test result (drafting)", "TBD — run identical prompt", "TBD — run identical prompt", "TBD — run identical prompt", "TBD — run identical prompt"],
        ["Member test result (research)", "TBD — run identical query", "TBD — run identical query", "TBD — run identical query", "TBD — run identical query"],
        ["Member test result (coding)", "TBD — run identical task", "TBD — run identical task", "TBD — run identical task", "TBD — run identical task"],
        ["Verdict per workflow", "Fill after testing", "Fill after testing", "Fill after testing", "Fill after testing"],
    ])

    write_csv(download_dir / "ai-roi-calculator-template.csv", ["Metric", "Formula", "Your Value", "Notes"], [
        ["Monthly AI spend", "", "", "Sum of all subscriptions"],
        ["Hours saved per week (estimated)", "", "", "Be honest — compare to pre-AI baseline"],
        ["Your hourly rate", "", "", "What your time is worth"],
        ["Monthly time value saved", "Hours saved/week x 4.3 x hourly rate", "", "Auto-calculate"],
        ["Net ROI", "Monthly time value saved - monthly AI spend", "", "Positive = worth keeping"],
        ["ROI %", "(Net ROI / Monthly AI spend) x 100", "", ">100% means tools pay for themselves multiple times over"],
        ["Most expensive unused tool", "", "", "Candidate for cancellation"],
        ["Most used tool", "", "", "Core of your stack"],
        ["Overlap cost (duplicate tools)", "", "", "Sum of tools that do the same job"],
        ["Recommended action", "", "", "Cut, keep, or trial"],
    ])

    write_csv(download_dir / "vendor-security-questions-pack.csv", ["Question", "Why it matters", "What good looks like", "Red flag", "Your notes"], [
        ["Is customer data used for model training by default?", "Training defaults decide whether client text becomes model fuel.", "Clear opt-out or never-train on business/enterprise tiers.", "Vague blog language, no admin control.", ""],
        ["Can admins disable retention/training or set workspace controls?", "You need org-level control, not per-user hope.", "Admin toggles + audit log + role permissions.", "Only individual chat settings.", ""],
        ["Is there a DPA, subprocessors list, security page, or SOC report?", "Procurement and client contracts often require this.", "Public security page + DPA request path.", "No security page; sales-only answers.", ""],
        ["Can exports, sharing, and user access be revoked?", "Offboarding depends on this.", "Admin can revoke seats and export first.", "No export or revoke path documented.", ""],
        ["What happens when a seat leaves the company?", "Licenses and data must not travel with departed users.", "Seat transfer + content reassignment documented.", "Silent retention of ex-user workspaces.", ""],
        ["Which plan includes the controls you actually need?", "Controls often sit behind Team/Business tiers.", "Named plan with the exact control you need.", "Marketing implies controls the free tier lacks.", ""],
        ["Is there an exit plan (export formats)?", "Switching cost is a hidden lock-in tax.", "Standard exports (CSV/MD/JSON/PDF).", "Proprietary-only export or none.", ""],
    ])
    write_csv(download_dir / "30-day-renewal-cancel-calendar.csv", ["Day", "Action", "Owner", "Done?", "Notes"], [
        ["Day 0 (join)", "Download stack audit + weekly checklist; list every paid AI tool", "Member", "", ""],
        ["Day 1", "Fill stack audit; note monthly cost and weekly hours", "Member", "", ""],
        ["Day 2", "Mark keep/trial/replace/cancel for each tool", "Member", "", ""],
        ["Day 3", "Run one real task in primary assistant; log friction", "Member", "", ""],
        ["Day 7 (trial decision)", "Keep Premium only if audit/matrix saved a decision; else cancel trial", "Member", "", ""],
        ["Day 10", "Cancel or pause any tool tagged cancel before next charge", "Member", "", ""],
        ["Day 14", "Reply in request thread if you need a priority research slot", "Member", "", ""],
        ["Day 30", "File one cancel/keep decision with dollar amount saved or kept", "Member", "", ""],
    ])
    write_csv(download_dir / "free-vs-premium-value-matrix.csv", ["Capability", "Free site", "Premium members", "Why it matters"], [
        ["Tool reviews + comparisons", "Yes", "Yes + full decision matrix CSV", "Public is enough for browsing"],
        ["Scorecards / cost calculator / decision brief", "Yes", "Yes", "Free utilities stay free"],
        ["Keep/Cut Weekly email", "Yes (Beehiiv)", "Yes", "Free newsletter stays free"],
        ["Instant Stack Audit scorecard", "Yes — /stack-audit.html", "Yes, plus the deeper template + written reply", "Free tool stays free"],
        ["Full decision matrix CSV", "No", "Yes, refreshed from official labels", "Monthly stack decisions"],
        ["AI Stack Audit Template + 48h strategy reply", "No", "Yes", "Turns inventory into keep/cut"],
        ["Weekly checklist + 30-day calendar", "No", "Yes", "Habit beats one-off cleanup"],
        ["Hands-on protocol + ROI worksheet", "Partial", "Yes — your numbers only", "Identical-task testing"],
        ["Priority research slots", "No", "First 5 complete requests/month", "Member research queue"],
        ["Implementation / account access", "Never", "Never", "Scope boundary on purpose"],
    ])
    write_csv(download_dir / "member-first-15-minutes.csv", ["Step", "Minutes", "Action", "Done?"], [
        ["1", "2", "Open pinned Welcome post; bookmark Whop hub", ""],
        ["2", "3", "Download stack audit + weekly checklist", ""],
        ["3", "5", "List every paid AI tool (name, cost, last use)", ""],
        ["4", "3", "Read free-vs-premium-value-matrix.csv", ""],
        ["5", "2", "Skim tool-change alert feed for tools you pay for", ""],
    ])
    write_csv(download_dir / "cancel-savings-tracker.csv", ["Tool cancelled or downgraded", "Monthly $ saved", "Annual $ saved", "Date", "Replaced by", "Notes"], [
        ["(example) unused image tool", "10", "120", "", "Free-tier visual tool", "Was under 1 hr/week"],
        ["TOTAL", "", "", "", "", "Premium pays for itself if monthly saves exceed $12"],
    ])
    write_csv(download_dir / "sample-filled-stack-audit-example.csv", ["Field", "Example Answer", "Editor note"], [
        ["Role/team size", "Solo consultant, 1 person", "Be specific"],
        ["Monthly AI spend", "$97", "Sum everything"],
        ["Biggest overlap", "ChatGPT + Claude both used for drafting", "Pick one primary"],
        ["Most expensive rarely used", "Image generator at 0.5 hrs/week", "Cancel candidate"],
        ["Strategy reply example", "Keep one research tool; pick ONE primary assistant after 3 identical tasks; cancel unused image seat. Est. save $30-50/mo.", "Premium audit reply style - strategy only"],
    ])
    coding = [t for t in tools if t.get("slug") in {"cursor", "github-copilot", "replit-ai", "bolt-new", "lovable", "v0", "claude", "chatgpt", "grok", "windsurf"} or "code" in str(t.get("category", "")).lower() or "coding" in str(t.get("best_for", "")).lower()]
    seen_c: set[str] = set()
    coding_rows = []
    for t in coding:
        slug = str(t.get("slug") or "")
        if not slug or slug in seen_c:
            continue
        seen_c.add(slug)
        coding_rows.append([t.get("name"), slug, t.get("price"), t.get("best_for"), "Run the same real coding task. Compare first-output acceptance rate, not demos."])
    write_csv(download_dir / "coding-assistant-shortlist-2026-11.csv", ["tool", "slug", "pricing", "best_for", "member_test"], coding_rows)

    nov_posts = f"""# AIToolsEssentials Premium — Whop Upload Pack — NOVEMBER ({today})

This is the November member drop. Upload each section as a Whop post and attach the matching CSV from `admin/whop-premium/files/`.

---

## POST N1 — Pinned: Welcome to Premium (updated for November)

Welcome to AIToolsEssentials Premium. This is the $12/month membership for deciding which subscriptions you keep — not another folder of unused tools.

**New this month (November):**
1. **AI Stack Audit Template** — fill it out and reply with your answers for a personalized stack recommendation within 48 hours.
2. **Weekly AI Stack Checklist** — a 7-day rhythm for keeping your stack lean.
3. **Tool-Change Alert Feed** — curated pricing, model, and feature changes across all {len(tools)} tracked tools.
4. **Assistant Hands-On Comparison** — ChatGPT vs Claude vs Grok vs Gemini test protocol with fillable results.
5. **AI ROI Calculator** — measure whether your AI spend is actually paying for itself.
6. **Refreshed decision matrix** — `premium-tool-decision-matrix-2026-11.csv`.

**What Premium includes (all months):**
- Monthly decision matrix CSV
- One workflow deep-dive or playbook each month
- Weekly AI stack checklist
- Tool-change alert feed (pricing, models, features)
- AI stack audit template with personalized strategy-only response
- Assistant hands-on comparison protocol with fillable CSV
- AI ROI calculator template
- Source-dated pricing/policy notes when available
- Member request thread for upcoming research
- Priority research slots for the first 5 complete requests each month
- Strategy-only recommendations — no account access, implementation, integrations, or ongoing support

**Billing:** 7-day free trial, then $12/month via Whop. Use code LAUNCH50 for 50% off your first paid month (new users only). Cancel anytime from your Whop account. All sales final — no refunds.

---

## POST N2 — November brief: Stop paying for AI tools you don't use

Most teams and solo users are paying for 3-5 AI tools and actively using 1-2. The rest are overlap, inertia, or "just in case" subscriptions.

**This month's decision framework:**

1. **Download the AI Stack Audit Template** (`ai-stack-audit-template.csv`)
2. **Fill it out honestly** — list every AI tool you pay for, monthly cost, weekly hours, what it does, and whether something else could do it
3. **Reply with your completed audit** — within 48 hours you'll get a personalized strategy-only recommendation: keep, cut, trial, or switch
4. **Use the AI ROI Calculator** (`ai-roi-calculator-template.csv`) to see if your total AI spend is actually paying for itself

**The rule:** if a tool doesn't save you measurable time on a weekly workflow, it's a candidate for cancellation. "Just in case" is not a workflow.

Attach: `ai-stack-audit-template.csv`, `ai-roi-calculator-template.csv`, `premium-tool-decision-matrix-2026-11.csv`

---

## POST N3 — Weekly AI Stack Checklist: your 7-day rhythm

Stop doing ad-hoc tool reviews. Run this checklist every week — it takes 15 minutes total.

| Day | Task | Why |
|-----|------|-----|
| Mon | Check tool-change alerts | Catch pricing/model changes before they affect you |
| Tue | Run one real task in your primary assistant | Notice quality/limit shifts early |
| Wed | Review overlap matrix | Is anything overlapping or unused? |
| Thu | Test one tool you're considering switching to | One real task, not a demo |
| Fri | Check change-radar for the week's updates | One scan, all recorded changes |
| Fri | Log any limit-hits or friction | Data for next month's decisions |
| Sun | Decide: cancellations or trials to start? | Act on data, not impulse |

Attach: `weekly-ai-stack-checklist.csv`

---

## POST N4 — November alert feed: what changed across tracked tools

Curated changes for members. Public change-radar catches up later; members get the curated feed here first.

**Highlights:**
- **Cursor:** Composer 2.5 now default on Pro; Grok 4.6 available as alternative model
- **Grok:** Grok 4.6 shipping; Grok Build and Grok Bot features expanded
- **HtmlSlides:** New tool added (vendor submission) — interactive HTML presentation maker
- **Whop CLI:** Business CLI launched — programmatically manage products, pricing, ads, payouts
- **All tools:** Monthly pricing snapshot refreshed across {len(tools)} tracked tools

**Action:** Review the full alert feed CSV. If any change affects a tool in your stack, note it in your weekly checklist.

Attach: `tool-change-alert-feed-2026-11.csv`

---

## POST N5 — Hands-on comparison: ChatGPT vs Claude vs Grok vs Gemini

Stop reading reviews. Run the test yourself.

**Protocol:**
1. Download the comparison CSV (`assistant-hands-on-comparison-2026-11.csv`)
2. Write one brief for each of three workflows: drafting, research, coding
3. Run the identical brief in all four assistants
4. Fill in the "Member test result" rows with your findings
5. The verdict row: which assistant won each workflow for *your* work?

**Why this matters:** benchmarks don't match your actual tasks. This protocol takes about 30 minutes and gives you a defensible answer for which assistant to keep paying for.

Attach: `assistant-hands-on-comparison-2026-11.csv`

---

## POST N6 — November request thread + priority research slots

Reply with the workflow you want researched next. Good requests include:

- Your role/team
- Current tool stack
- The task you do weekly
- Tools you're deciding between
- Budget, privacy, or export constraints

**November research slots (first 5 complete requests):**
1. Open
2. Open
3. Open
4. Open
5. Open

Research is delivered as a new CSV + brief in the next monthly drop. Replies are strategy-only — no implementation, setup, account access, or ongoing support.
"""
    (admin / "whop-posts-2026-11.md").write_text(nov_posts)


    posts = f'''# AIToolsEssentials Premium — Whop Upload Pack ({today})

Use this file to populate the Whop member area. Create each section below as a Whop post, then attach the CSV files from `admin/whop-premium/files/`.

---

## POST 1 — Pinned start here: Welcome to Premium

Welcome to AIToolsEssentials Premium. This is the $12/month membership for deciding which subscriptions you keep — not another folder of unused tools.

**Start here:**
1. Download `premium-tool-decision-matrix-2026-09.csv`.
2. Read the September cost-cutting brief below.
3. Pick one workflow you want tested next and reply in the request thread.

**What Premium includes:**
- Monthly decision matrix CSV (all tracked tools).
- AI Stack Audit Template + strategy-only personalized reply.
- Weekly AI Stack Checklist and Tool-Change Alert Feed.
- Hands-On Comparison Protocol and AI ROI Calculator.
- One workflow deep-dive or playbook each month.
- Priority research slots (first 5 member requests).
- Source-dated pricing/policy notes when available.
- Strategy-only recommendations — no account access, implementation, integrations, or ongoing support.

**Billing:** 7-day free trial, then $12/month via Whop. Use code LAUNCH50 for 50% off your first paid month (new users only). Auto-renews until cancelled from the Whop account. All sales final — no refunds.

---

## POST 2 — September brief: cut AI subscription sprawl

Most teams do not have an AI tool problem. They have an overlap problem.

**This month's decision rule:** keep the smallest stack that covers the weekly workflow with the least upgrade pressure.

**Use the CSV matrix to tag every tool as:**
- Keep: used weekly, has a clear owner, and saves measurable time.
- Trial: promising, but needs a real task test.
- Replace: overlaps with another paid tool.
- Cancel/defer: no workflow owner or no recent use.

**Recommended 30-minute review:**
1. List every AI subscription and owner.
2. Sort the matrix by category.
3. Identify duplicate writing, meeting, automation, and creative tools.
4. Run one real task in each contender.
5. Cancel or defer anything without a weekly workflow.

Attach: `premium-tool-decision-matrix-2026-09.csv`

---

## POST 3 — General AI assistant shortlist

The common mistake is comparing assistants as if they all solve one job. They do not.

**Test separately for:**
- Everyday drafting and rewriting.
- Source-backed research.
- Long-context document analysis.
- Coding/debugging assistance.
- Team controls and data policy.

**Member action:** choose 2–3 assistants from the CSV, run the same real prompt in each, and record editing burden. The winner is the one that reduces review time without increasing verification risk.

Attach: `general-ai-assistant-shortlist-2026-09.csv`

---

## POST 4 — Automation pricing model decoder

Zapier, Make, and n8n do not bill the same unit.

**Decision shortcut:**
- Simple app-to-app workflows: compare Zapier task volume.
- Visual branching scenarios: test Make operation/credit usage.
- Complex multi-step workflows: test n8n executions, especially if technical/self-hosting is acceptable.

**Before upgrading:** map one real workflow and estimate monthly volume. Do not compare sticker price until you know whether you are paying by task, operation, credit, or execution.

Attach: `automation-pricing-model-decoder-2026-09.csv`

---

## POST 5 — Vendor/security questions pack

Before connecting sensitive company, client, student, or customer data, answer these questions:

1. Is customer data used for model training by default?
2. Can admins disable retention/training or configure workspace controls?
3. Is there a DPA, subprocessors list, security page, SOC report, or enterprise docs page?
4. Can exports, sharing, and user access be revoked?
5. What happens when a seat leaves the company?
6. Which plan includes the controls you actually need?

If the vendor does not make the answer easy to find, treat that as a procurement risk — not an automatic rejection, but a reason to delay annual billing.

---

## POST 6 — Member request thread

Reply with the workflow you want tested next. Good requests include:

- Your role/team.
- The current tool stack.
- The task you do weekly.
- The tools you are deciding between.
- Any budget, privacy, or export constraint.

Examples:
- Meeting notes stack for a sales team: Fireflies vs Otter vs Fathom.
- AI writing pipeline for a solo consultant: ChatGPT vs Claude vs Jasper vs Copy.ai.
- App prototyping stack: Cursor vs Replit AI vs Bolt.new vs Lovable vs v0.
- Video course workflow: Descript vs HeyGen vs Synthesia vs Runway.
'''
    (admin / "whop-posts-2026-09.md").write_text(posts)

    checklist = f'''# Whop Premium Setup Checklist

Use this before turning on promotion for the $12/month Premium membership.

## Required in Whop
- [x] Create or update the Premium product/community (AIToolsEssentials Premium).
- [x] Set plan title to Premium Monthly and price to $12/month.
- [x] Enable 7-day free trial on plan_FNXWs3suBFwDN.
- [x] Create branded checkout configuration: {WHOP_CHECKOUT}
- [x] Create promo code LAUNCH50 (50% off first paid month, new users only).
- [ ] Confirm cancellation is handled by Whop account settings.
- [ ] Upload September files + posts from `whop-posts-2026-09.md`.
- [ ] Upload October files + posts from `whop-posts-2026-10.md`.
- [ ] Upload November content-engine pack from `whop-posts-2026-11.md`:
  - `premium-tool-decision-matrix-2026-11.csv`
  - `ai-stack-audit-template.csv`
  - `weekly-ai-stack-checklist.csv`
  - `tool-change-alert-feed-2026-11.csv`
  - `assistant-hands-on-comparison-2026-11.csv`
  - `ai-roi-calculator-template.csv`
- [ ] Pin the November welcome post as the start-here post.
- [ ] Confirm live checkout still matches: {WHOP_CHECKOUT}
- [ ] Confirm promo checkout path works: {WHOP_CHECKOUT_PROMO}
- [ ] Run George's Whop test transaction (trial path) before public launch.

## Scope reminder
Premium is research and strategy only. Do not promise implementation, setup, integrations, account access, credential handling, or ongoing technical support. Stack-audit replies are strategy-only written recommendations.
'''
    (admin / "whop-setup-checklist.md").write_text(checklist)

    readiness = {
        "updated_at": today,
        "site_ready": True,
        "whop_commerce_ready": {
            "plan_id": "plan_FNXWs3suBFwDN",
            "checkout": WHOP_CHECKOUT,
            "checkout_promo": WHOP_CHECKOUT_PROMO,
            "trial_days": WHOP_TRIAL_DAYS,
            "promo_code": WHOP_PROMO_CODE,
            "price_usd_month": 12,
        },
        "public_pages": ["/premium/", "/premium/library/", "/premium/welcome/", "/premium/sample-report.html", "/premium/roadmap.html", "/premium/archive.html", "/premium/faq.html", "/pricing/", "/checkout/complete/"],
        "whop_assets_ready": [
            "whop-posts-2026-09.md",
            "whop-posts-2026-10.md",
            "whop-posts-2026-11.md",
            "files/premium-tool-decision-matrix-2026-09.csv",
            "files/premium-tool-decision-matrix-2026-10.csv",
            "files/premium-tool-decision-matrix-2026-11.csv",
            "files/general-ai-assistant-shortlist-2026-09.csv",
            "files/automation-pricing-model-decoder-2026-09.csv",
            "files/visual-ai-tool-shortlist-2026-10.csv",
            "files/meeting-notes-decision-sheet-2026-10.csv",
            "files/ai-stack-audit-template.csv",
            "files/weekly-ai-stack-checklist.csv",
            "files/tool-change-alert-feed-2026-11.csv",
            "files/assistant-hands-on-comparison-2026-11.csv",
            "files/ai-roi-calculator-template.csv",
        ],
        "george_still_needs_to_do": [
            "Run a Whop test transaction through the 7-day trial path",
            "Confirm LAUNCH50 applies 50% off the first paid month",
        ],
        "scope_boundary": "Research and strategy only; no implementation, setup, integrations, account access, credentials, or ongoing support. Stack-audit replies are strategy-only written recommendations."
    }
    (admin / "whop-launch-readiness.json").write_text(json.dumps(readiness, indent=2))

    readiness_md = "# Whop Launch Readiness\n\n" + "## Site-ready public pages\n" + "\n".join(f"- [x] {x}" for x in readiness["public_pages"]) + "\n\n## Whop assets ready\n" + "\n".join(f"- [x] {x}" for x in readiness["whop_assets_ready"]) + "\n\n## George still needs to do in Whop\n" + "\n".join(f"- [ ] {x}" for x in readiness["george_still_needs_to_do"]) + "\n\n## Scope boundary\n" + readiness["scope_boundary"] + "\n"
    (admin / "whop-launch-readiness.md").write_text(readiness_md)

    # Deterministic upload bundle for Whop: fixed timestamps keep repeated builds stable.
    bundle_path = admin / "aitools-premium-whop-upload-pack.zip"
    bundle_members = [
        (admin / "whop-posts-2026-09.md", "whop-posts-2026-09.md"),
        (admin / "whop-posts-2026-10.md", "whop-posts-2026-10.md"),
        (admin / "whop-posts-2026-11.md", "whop-posts-2026-11.md"),
        (admin / "whop-setup-checklist.md", "whop-setup-checklist.md"),
        (admin / "whop-launch-readiness.md", "whop-launch-readiness.md"),
        (admin / "whop-launch-readiness.json", "whop-launch-readiness.json"),
        (download_dir / "premium-tool-decision-matrix-2026-09.csv", "files/premium-tool-decision-matrix-2026-09.csv"),
        (download_dir / "premium-tool-decision-matrix-2026-10.csv", "files/premium-tool-decision-matrix-2026-10.csv"),
        (download_dir / "premium-tool-decision-matrix-2026-11.csv", "files/premium-tool-decision-matrix-2026-11.csv"),
        (download_dir / "general-ai-assistant-shortlist-2026-09.csv", "files/general-ai-assistant-shortlist-2026-09.csv"),
        (download_dir / "automation-pricing-model-decoder-2026-09.csv", "files/automation-pricing-model-decoder-2026-09.csv"),
        (download_dir / "visual-ai-tool-shortlist-2026-10.csv", "files/visual-ai-tool-shortlist-2026-10.csv"),
        (download_dir / "meeting-notes-decision-sheet-2026-10.csv", "files/meeting-notes-decision-sheet-2026-10.csv"),
        (download_dir / "ai-stack-audit-template.csv", "files/ai-stack-audit-template.csv"),
        (download_dir / "weekly-ai-stack-checklist.csv", "files/weekly-ai-stack-checklist.csv"),
        (download_dir / "tool-change-alert-feed-2026-11.csv", "files/tool-change-alert-feed-2026-11.csv"),
        (download_dir / "assistant-hands-on-comparison-2026-11.csv", "files/assistant-hands-on-comparison-2026-11.csv"),
        (download_dir / "ai-roi-calculator-template.csv", "files/ai-roi-calculator-template.csv"),
        (download_dir / "vendor-security-questions-pack.csv", "files/vendor-security-questions-pack.csv"),
        (download_dir / "30-day-renewal-cancel-calendar.csv", "files/30-day-renewal-cancel-calendar.csv"),
        (download_dir / "free-vs-premium-value-matrix.csv", "files/free-vs-premium-value-matrix.csv"),
        (download_dir / "member-first-15-minutes.csv", "files/member-first-15-minutes.csv"),
        (download_dir / "cancel-savings-tracker.csv", "files/cancel-savings-tracker.csv"),
        (download_dir / "sample-filled-stack-audit-example.csv", "files/sample-filled-stack-audit-example.csv"),
        (download_dir / "coding-assistant-shortlist-2026-11.csv", "files/coding-assistant-shortlist-2026-11.csv"),
    ]
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for src, arc in bundle_members:
            info = zipfile.ZipInfo(arc, date_time=(2026, 11, 1, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, src.read_bytes())
    (admin / "whop-upload-pack-manifest.json").write_text(json.dumps({
        "bundle": bundle_path.name,
        "files": [arc for _, arc in bundle_members],
        "note": "Upload the Markdown posts/checklists as Whop posts and attach the CSV files to the member area.",
    }, indent=2))


def update_checkout(root: Path) -> None:
    p = root / "checkout" / "complete" / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="0; url={WELCOME_PATH}">
  <meta name="robots" content="noindex">
  <meta name="description" content="This page cannot verify a charge. Continue to the Premium welcome page.">
  <title>Continue to Premium welcome</title>
  <link rel="canonical" href="{DOMAIN}{WELCOME_PATH}">
  <link rel="stylesheet" href="/css/styles.css">
</head>
<body>
  <main>
    <section class="scene scene-dark">
      <div style="max-width:720px;margin:0 auto;padding:92px 28px;text-align:center">
        <p class="kicker light">Checkout return</p>
        <h1>This page cannot verify a charge.</h1>
        <p class="subhead">If Whop shows payment succeeded, continue to the Premium welcome page. Whop is the source of truth — not this URL.</p>
        <p><a class="button button-blue" href="{WELCOME_PATH}">Continue to /premium/welcome/</a></p>
      </div>
    </section>
  </main>
</body>
</html>
'''
    )
    # Homepage chrome is owned by enhance_homepage. Do not re-inflate it here.


def rewrite_homepage_hero_actions(html: str) -> str:
    """Hero: Stack Audit first. Premium keep/cut pack is secondary."""
    actions = homepage_hero_actions_html(_whop_dict())
    pattern = re.compile(
        r'(<section class="hero(?: home-hero)? scene scene-dark">.*?<div class="hero-copy">.*?)(<div class="actions">.*?</div>)(?:\s*<p class="affiliate-inline">.*?</p>)?(?:\s*<p class="hero-secondary-links">.*?</p>)?',
        flags=re.S,
    )
    match = pattern.search(html)
    if not match:
        return html
    return html[: match.start(2)] + actions + html[match.end():]


def homepage_newsletter_panel(root: Path) -> str:
    """One Subscribe CTA to the on-site embed. Beehiiv lives on /subscribe/ only."""
    cfg = {}
    cfg_path = root / "data/newsletter.json"
    if cfg_path.exists():
        cfg = json.loads(cfg_path.read_text())
    kicker = esc(cfg.get("homepage_kicker") or "Keep/Cut Weekly · free email")
    headline = esc(cfg.get("homepage_headline") or "Get the free weekly keep/cut email.")
    body = esc(cfg.get("homepage_body") or "One email a week on Beehiiv. Premium is a separate paid membership — not this list.")
    return f'''<!-- AIT HOMEPAGE NEWSLETTER START -->
<section id="subscribe" class="newsletter-panel home-newsletter">
<div>
<span>{kicker}</span>
<h2>{headline}</h2>
<p>{body}</p>
</div>
<div class="newsletter-actions">
<a class="button button-secondary" href="/subscribe/">Subscribe free</a>
</div>
</section>
<!-- AIT HOMEPAGE NEWSLETTER END -->'''


def _homepage_scripts(_html: str) -> str:
    """Stable script block so a second enhance_homepage pass is a no-diff."""
    return (
        '<script src="js/site.js" defer></script>'
        '<script src="/js/cookie-consent.js" defer></script>'
        '<script src="js/analytics.js" defer></script>'
    )


def slim_homepage_html(html: str, root: Path) -> str:
    """Rebuild homepage body to hero + one Premium band + subscribe + slim chrome."""
    load_whop_from_integrations(root)
    html = apply_homepage_voice_meta(html, root=root)
    head_end = html.find("</head>")
    if head_end == -1:
        return html
    head = html[: head_end + len("</head>")]
    scripts = _homepage_scripts(html)
    body = (
        '\n<body data-page="home">\n  '
        + homepage_header_html()
        + "\n\n  <main>\n"
        + homepage_hero_html(_whop_dict())
        + "\n"
        + homepage_band_html(_whop_dict()).rstrip()
        + "\n"
        + homepage_newsletter_panel(root)
        + "\n</main>\n\n"
        + '  <div id="share-row" hidden></div>\n  '
        + homepage_footer_html()
        + "\n"
        + scripts
        + "\n</body>\n</html>\n"
    )
    return head + body


def enhance_homepage(root: Path) -> None:
    """Own the homepage. Daily generators must not restore the fat page."""
    load_whop_from_integrations(root)
    home = root / "index.html"
    if not home.exists():
        return
    html = slim_homepage_html(home.read_text(), root)
    if not html.endswith("\n"):
        html += "\n"
    home.write_text(html)


def premium_upsell_module() -> str:
    return upsell_module_html(_whop_dict())


def inject_before_main_end(html: str, module: str) -> str:
    import re
    html = re.sub(r'\n?<!-- AIT PREMIUM MODULE START -->.*?<!-- AIT PREMIUM MODULE END -->\n?', '\n', html, flags=re.S)
    html = re.sub(
        r'\n?<section class="newsletter-panel premium-conversion-panel">.*?</section>\n?',
        '\n',
        html,
        flags=re.S,
    )
    if '</main>' not in html:
        return html
    return html.replace('</main>', module + '\n</main>', 1)


def postprocess(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    load_whop_from_integrations(root)
    base_targets = [
        'stack-builder.html',
        'cost-calculator.html',
        'compare-shortlist.html',
        'tool-finder.html',
        'deals/index.html',
        'resources/index.html',
        'pricing-index/index.html',
        'weekly/index.html',
        'start-here/index.html',
    ]
    dynamic_targets = []
    dynamic_targets.extend(str(p.relative_to(root)) for p in sorted((root / 'tools').glob('*/index.html')))
    dynamic_targets.extend(str(p.relative_to(root)) for p in sorted((root / 'comparisons').glob('*.html')))
    # Keep admin/noindex/checkout/legal pages out of the conversion injection path.
    targets = list(dict.fromkeys(base_targets + dynamic_targets))
    module = premium_upsell_module()
    changed = 0
    for rel in targets:
        p = root / rel
        if not p.exists():
            continue
        old = p.read_text()
        if 'name="robots" content="noindex' in old:
            continue
        new = inject_before_main_end(old, module)
        if new != old:
            p.write_text(new)
            changed += 1
    enhance_homepage(root)
    return changed

def update_pricing_page(root: Path, tools: list[dict[str, Any]]) -> None:
    import re
    path = root / "pricing" / "index.html"
    if not path.exists():
        return
    html = path.read_text()
    n = len(tools)
    meta = (
        f'content="You are paying for overlapping AI tools. The directory, Keep/Cut Weekly, '
        f'and instant Stack Audit stay free. Premium is ${WHOP_PRICE}/month on Whop: dated '
        f'keep/cut research, monthly CSV, weekly checklist, alerts, and a written keep/cut reply."'
    )
    html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" {meta}>', html, count=1)
    hero = (
        f'<p class="kicker light">Pricing</p>'
        f'<h1>You are paying for overlapping AI tools. Here is what is free, and what ${WHOP_PRICE}/month buys.</h1>'
        f'<p>The directory, <a href="/newsletter/">Keep/Cut Weekly</a>, and the '
        f'<a href="/stack-audit.html">instant Stack Audit</a> stay free. Premium is ${WHOP_PRICE}/month on Whop: '
        f'dated keep/cut research, a monthly decision matrix CSV, a weekly checklist, tool-change alerts, '
        f'a stack-audit template with a written keep/cut reply within 48 hours, an ROI worksheet, and '
        f'priority research slots — delivered in Whop. The written reply is included — not a second product.</p>'
        f'<p class="last-updated">{WHOP_TRIAL_DAYS}-day free trial · then ${WHOP_PRICE}/month · code {WHOP_PROMO_CODE} '
        f'for 50% off first paid month · Cancel in Whop · All sales final — no refunds</p>'
    )
    html = re.sub(
        r'(<section class="review-hero scene scene-light">).*?(</section>)',
        r'\1' + hero + r'\2',
        html,
        count=1,
        flags=re.S,
    )
    new_grid = (
        f'<div class="pricing-grid">'
        f'<article class="pricing-card"><p class="eyebrow">Free</p><h3>Directory + Keep/Cut Weekly</h3>'
        f'<p class="pricing-price">$0<span>/forever</span></p><ul class="pricing-features">'
        f'<li>Tool reviews, comparisons, and dated evidence</li>'
        f'<li>Free Beehiiv email — not a Whop charge</li>'
        f'<li>Buyer guides, benchmarks, and scorecards</li>'
        f'<li>This is not Premium</li></ul>'
        f'<a class="button button-blue" href="../tools/index.html">Browse free</a>'
        f'<a class="button button-dark" href="/subscribe/" style="margin-left:8px">Subscribe free</a></article>'
        f'<article class="pricing-card"><p class="eyebrow">Free</p><h3>Instant Stack Audit</h3>'
        f'<p class="pricing-price">$0<span>/no login</span></p><ul class="pricing-features">'
        f'<li>Keep / cut / overlap scorecard on your device</li>'
        f'<li>All {n} directory tools selectable</li>'
        f'<li>Share and export locally — nothing is posted to us</li>'
        f'<li>Not a Whop product and not a second paid product</li></ul>'
        f'<a class="button button-blue" href="/stack-audit.html">Run free Stack Audit</a></article>'
        f'<article class="pricing-card featured"><p class="pricing-flag">Paid · Whop</p>'
        f'<p class="eyebrow">Premium</p><h3>Keep/cut research on Whop</h3>'
        f'<p class="pricing-price">${WHOP_PRICE}<span>/month</span></p><ul class="pricing-features">'
        f'<li>{WHOP_TRIAL_DAYS}-day free trial, then ${WHOP_PRICE}/month — code {WHOP_PROMO_CODE} for 50% off the first paid month (new users)</li>'
        f'<li>Dated keep/cut research, monthly {n}-tool decision matrix CSV, weekly checklist</li>'
        f'<li>Tool-change alerts, ROI worksheet, priority research slots</li>'
        f'<li>Stack-audit template + strategy-only written reply within 48 hours — not a second product</li>'
        f'<li>Delivered in Whop. Public /premium/library/ pages are a preview of the format</li></ul>'
        f'<a class="button button-blue" href="{WHOP_CHECKOUT_PROMO}" rel="external noopener" data-whop-checkout="{WHOP_PLAN_ID}">{JOIN_PREMIUM_LABEL}</a>'
        f'<a class="button button-ghost-dark" href="/premium/" style="margin-left:8px">{BUY_PAGE_LABEL}</a>'
        f'<p class="muted-small">Then ${WHOP_PRICE}/mo · {plain_checkout_link(_whop_dict())}</p>'
        f'<p class="affiliate-inline">{WHOP_TRIAL_DAYS}-day free trial · then ${WHOP_PRICE}/month · {WHOP_PROMO_CODE} = 50% off first paid month (new users) · cancel in Whop. All sales final — no refunds. Research and strategy only. Affiliate status never changes recommendations.</p></article>'
        f'</div>'
    )
    html = re.sub(
        r'<div class="pricing-grid[^"]*">.*?</div>(?=\s*</section>)',
        new_grid,
        html,
        count=1,
        flags=re.S,
    )
    # Consume whitespace before Scope so a second generate does not keep
    # inserting the trailing space (site-qa idempotency).
    html = re.sub(
        r"<strong>Delivery:</strong>.*?(?=<strong>Scope:)",
        "<strong>Delivery:</strong> Premium is delivered in Whop. The <a href=\"/premium/library/\">/premium/library/</a> pages on this site are a public preview of the format and are not gated. Free Keep/Cut Weekly and free Stack Audit are not this membership. ",
        html,
        count=1,
        flags=re.S,
    )
    if 'href="/stack-audit.html"' not in html:
        html = html.replace(
            '<article class="content-hub-card"><span>Free utility</span><h3><a href="/decision-brief.html">Decision Brief</a></h3>',
            '<article class="content-hub-card"><span>Free utility</span><h3><a href="/stack-audit.html">Instant Stack Audit</a></h3><p>No-login keep/cut scorecard. Stays on your device.</p></article><article class="content-hub-card"><span>Free utility</span><h3><a href="/decision-brief.html">Decision Brief</a></h3>',
        )
    path.write_text(html)


def update_services_audit_page(root: Path) -> None:
    path = root / "services" / "ai-stack-audit.html"
    if not path.exists():
        return
    html = path.read_text()
    html = html.replace(
        'content="AI Stack Audit: included with Premium membership ($12/mo). A personalized strategy report, decision brief, and 30-day adoption roadmap — no implementation, no logins required."',
        'content="Two Stack Audits: the free instant scorecard at /stack-audit.html, and the deeper Premium strategy reply included with the $12/mo Whop membership. Not a second paid product."',
    )
    html = html.replace(
        '<p class="kicker">Strategy report · included with Premium</p><h1>Get a clear AI stack recommendation without wasting weeks testing tools.</h1><p class="subhead">The AI Stack Audit is now a Premium member deliverable. $12/month, 7-day free trial. You fill out an intake questionnaire, and we send a personalized strategy report: keep / cut / trial per tool, a printable decision one-pager, and a 30-day adoption roadmap. No software setup, integrations, or account access required.</p><div class="actions"><a class="button button-blue" href="../premium/">Join Premium and get the audit</a><a class="button button-ghost-dark" href="intake-questionnaire.html">Member intake form</a></div>',
        f'<p class="kicker">Free scorecard · paid Premium reply</p><h1>Start free. Pay only for the deeper strategy reply.</h1><p class="subhead">The <a href="/stack-audit.html">instant Stack Audit</a> is free, no login, and stays on your device. Paid Premium ($12/mo via Whop) adds the inventory template and a strategy-only written keep/cut/trial reply. It is not a second checkout product.</p><div class="actions"><a class="button button-blue" href="/stack-audit.html">Run the free instant audit</a><a class="button button-ghost-dark" href="{WHOP_CHECKOUT_PROMO}" rel="external noopener">{JOIN_PREMIUM_LABEL}</a></div>',
    )
    html = html.replace(
        "<h2>AI Stack Audit — included with Premium</h2>\n<p>Premium members get a personalized AI Stack Audit built from their intake.",
        "<h2>Free instant scorecard vs paid Premium reply</h2>\n<p>Use <a href=\"/stack-audit.html\">/stack-audit.html</a> for an immediate keep/cut score. Premium members can also send a completed inventory for a personalized written reply.",
    )
    html = html.replace(
        "<li><a href=\"../premium/\">Subscribe to Premium</a> (7-day free trial).</li>\n<li>Fill out the <a href=\"intake-questionnaire.html\">intake questionnaire</a>.</li>",
        "<li>Run the free <a href=\"/stack-audit.html\">instant Stack Audit</a> first.</li>\n<li>If you want a written strategy reply, <a href=\"" + WHOP_CHECKOUT_PROMO + f"\" rel=\"external noopener\">{JOIN_PREMIUM_LABEL}</a>.</li>\n<li>Fill out the <a href=\"intake-questionnaire.html\">member intake</a> or the <a href=\"/premium/library/stack-audit-template.html\">Premium template</a>.</li>",
    )
    html = html.replace(
        '<p><a class="button button-blue" href="../premium/">Join Premium (7-day trial)</a> <a class="button button-dark" href="mailto:contact@aitoolsessentials.com?subject=AI%20Stack%20Audit%20question">Email a question about the audit</a></p>',
        f'<p><a class="button button-blue" href="/stack-audit.html">Free instant audit</a> <a class="button button-blue" href="{WHOP_CHECKOUT_PROMO}" rel="external noopener">{JOIN_PREMIUM_LABEL}</a> <a class="button button-dark" href="mailto:contact@aitoolsessentials.com?subject=AI%20Stack%20Audit%20question">Email a question</a></p>',
    )
    html = html.replace(
        '<div class="score-card"><span>Premium deliverable</span><strong>$12/mo</strong><p>7-day free trial. Cancel anytime. Strategy only — no implementation, no account access, no ongoing support.</p><a class="button button-blue" href="../premium/">Subscribe</a></div>',
        f'<div class="score-card"><span>Paid Premium includes the written audit</span><strong>${WHOP_PRICE}/mo</strong><p>Not a second product. Free scorecard stays free. Strategy only — no implementation, no account access, no ongoing support.</p><a class="button button-blue" href="{WHOP_CHECKOUT_PROMO}" rel="external noopener">{JOIN_PREMIUM_LABEL}</a></div>',
    )
    path.write_text(html)


def update_sample_audit_page(root: Path) -> None:
    path = root / "premium" / "sample-audit.html"
    if not path.exists():
        return
    html = path.read_text()
    html = html.replace(
        '<a class="button button-blue" href="../services/intake-questionnaire.html">Get your audit — start intake</a>\n<a class="button button-ghost-dark" href="../premium/">Premium pricing &amp; trial</a>',
        f'<a class="button button-blue" href="{WHOP_CHECKOUT_PROMO}" rel="external noopener">{JOIN_PREMIUM_LABEL}</a>\n<a class="button button-ghost-dark" href="/stack-audit.html">Free instant Stack Audit</a>\n<a class="button button-ghost-dark" href="/premium/">{BUY_PAGE_LABEL}</a>',
    )
    html = html.replace(
        '<p><a class="button button-blue" href="../services/intake-questionnaire.html">Submit intake (Premium member)</a> <a class="button button-dark" href="../premium/">Subscribe on Whop</a></p>',
        f'<p><a class="button button-blue" href="{WHOP_CHECKOUT_PROMO}" rel="external noopener">{JOIN_PREMIUM_LABEL}</a> <a class="button button-dark" href="/premium/library/stack-audit-template.html">Open the Premium template</a> <a class="button button-dark" href="/stack-audit.html">Free instant audit</a></p>',
    )
    html = html.replace(
        '<p class="subhead">This is the headline Premium deliverable. Below is the structure and tone of a real audit. Names and client details have been changed.</p>',
        '<p class="subhead">This is the paid Premium written-audit format — deeper than the free instant scorecard. Structure and tone only. No invented client savings. Names in the sample are illustrative, not a case study.</p>',
    )
    html = html.replace(
        '<a class="button button-ghost-dark" href="/premium/library/">Member library</a>',
        f'<a class="button button-ghost-dark" href="/premium/">{BUY_PAGE_LABEL}</a>',
    )
    html = html.replace("the headline Premium deliverable", "the written keep/cut reply included with Premium")
    path.write_text(html)


def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    load_whop_from_integrations(root)
    tools_list = tools if tools is not None else json.loads((root / "data/tools.json").read_text())
    today = today or datetime.today().strftime("%Y-%m-%d")
    generate_public_pages(root, tools_list, today)
    generate_whop_pack(root, tools_list, today)
    from generate_premium_library import generate as generate_library
    from generate_site_discovery import generate_human_sitemap, generate_start_here
    generate_library(root, tools_list, today)
    update_checkout(root)
    update_pricing_page(root, tools_list)
    update_services_audit_page(root)
    update_sample_audit_page(root)
    generate_human_sitemap(root, tools_list)
    generate_start_here(root)
    enhance_homepage(root)
    return 12


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    tools = json.loads((root / "data/tools.json").read_text())
    print(generate(root, tools))
