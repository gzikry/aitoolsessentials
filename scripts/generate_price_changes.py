#!/usr/bin/env python3
"""Verified 2026 price-change and credit-expiry notes. No invented burn rates."""
from __future__ import annotations

import json
from pathlib import Path

from site_chrome import CANONICAL_HEADER

DOMAIN = "https://aitoolsessentials.com"
PATH = "/price-changes/"
TITLE = "AI price hikes and credit traps"
DESCRIPTION = (
    "What changed in the public price lists checked in October 2026: "
    "expired credits, closed tiers, and pools that are not the same unit."
)

ROWS = [
    (
        "v0",
        "/tools/v0/",
        "25 Oct 2026",
        "Legacy Premium at $20/mo is closed to new signups. New accounts start on Free. Plus is $30/user/mo and Business is $100/user/mo. Both paid rungs include a $30 monthly credit allowance. The extra $70 on Business is team controls, not more generation.",
        "Monthly credits and top-ups expire after 65 days. Purchased credits lock if the paid plan lapses. A one-year purchased balance is not a reason to keep a seat you are not shipping on.",
    ),
    (
        "Bolt.new",
        "/tools/bolt-new/",
        "25 Oct 2026",
        "Free is $0 with 1 million tokens a month and a 300,000 daily limit. Pro is $25/mo, or $18/mo billed annually ($216/year), for 10 million tokens. Teams is $30/mo.",
        "The 25 Oct check says the Pro token allowance rolls over. It does not publish a day-count the way v0 does. Do not treat a weekend prototype as a reason to keep the seat until renewal.",
    ),
    (
        "Lovable",
        "/tools/lovable/",
        "25 Oct 2026",
        "Free is 5 daily credits, capped at 30 a month. Pro is $25/mo ($21 billed annually) with 100 monthly credits plus 5 daily credits. Business is $50/mo.",
        "Monthly credits expire after 2 months. Daily grants do not roll over.",
    ),
    (
        "Replit",
        "/tools/replit-ai/",
        "25 Oct 2026",
        "The free Starter tier from the 21 Aug check is off the public table. Core is $20/mo ($18 billed annually). Pro is $100/mo ($90 billed annually).",
        "The public pricing table checked that day does not publish an effort-checkpoint price. Price the seat you can see, not a meter the page does not name.",
    ),
    (
        "Cursor",
        "/tools/cursor/",
        "26 Oct 2026",
        "Pro at $20 is not on cursor.com/pricing. The rungs a new buyer can select are Free $0, Plus $8, Premium $30, Super $100, and Ultra $200. Ultra is published as 50× Plus. Teams starts at $30/user. There is no annual discount on that page.",
        "Third-party frontier models are not inside the subscription. They bill at API list price. A legacy seat can continue. This note prices the plans on the page.",
    ),
    (
        "Claude Code",
        "/tools/claude/",
        "26 Oct 2026",
        "Claude Code is included on paid Claude plans. Pro is $20/mo or $200/year. Max 5x is $100/mo. Max 20x is $200/mo. Max is monthly only.",
        "Max 5x is 5× Pro usage per 5-hour session. Max 20x is 20×. There is no fixed message count. The $100 and $200 Max API credits do not apply to Claude Code.",
    ),
    (
        "GitHub Copilot",
        "/tools/github-copilot/",
        "26 Oct 2026",
        "The meter on the plans page is GitHub AI Credits, not a unit called a premium request. Pro is $10/mo with 1,500 credits. Pro+ is $39 with 7,000. Max is $100 with 20,000. Extra usage is $0.01 per credit.",
        "The page does not say how many credits one agent prompt uses. Do not convert a prompt into a dollar overage from this table.",
    ),
    (
        "Windsurf",
        "/price-changes/",
        "26 Oct 2026",
        "New Pro is $20/mo. Max is $200/mo and cannot be shared. Teams is $40 per full seat with an $80 minimum. Enterprise is custom, not a $60 list price.",
        "March 2026 replaced prompt credits with a daily and weekly quota. An existing Pro subscriber at $15/mo keeps that price. Add-on credits converted at $0.04 were not a new public meter.",
    ),
]


def _schema() -> str:
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Dataset",
                "name": "AI price changes and credit expirations checked October 2026",
                "description": DESCRIPTION,
                "url": DOMAIN + PATH,
                "dateModified": "2026-10-26",
                "creator": {"@type": "Organization", "name": "AIToolsEssentials", "url": DOMAIN + "/"},
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": row[0] + " hidden cost or credit expiration",
                        "acceptedAnswer": {"@type": "Answer", "text": row[3] + " " + row[4]},
                    }
                    for row in ROWS
                ],
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False)


def generate(root: Path) -> Path:
    body = []
    for name, href, checked, price, trap in ROWS:
        body.append(
            "<tr>"
            f'<th><a href="{href}">{name}</a></th>'
            f"<td>{checked}</td>"
            f"<td>{price}</td>"
            f"<td>{trap}</td>"
            "</tr>"
        )
    faqs = []
    for name, _href, _checked, price, trap in ROWS[:5]:
        faqs.append(f"<details><summary>{name}: what expires or changed?</summary><p>{price} {trap}</p></details>")
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{DESCRIPTION}">
<title>{TITLE} | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}{PATH}">
<meta property="og:title" content="{TITLE} | AIToolsEssentials">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:url" content="{DOMAIN}{PATH}">
<meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<link rel="stylesheet" href="/css/styles.css">
<script type="application/ld+json">{_schema()}</script>
</head>
<body>
{CANONICAL_HEADER}
<main>
<section class="scene scene-dark ledger-mast">
<div style="max-width:880px;margin:0 auto;padding:86px 28px 48px">
<p class="kicker light">Checked October 2026</p>
<h1>The credit expires. The seat keeps billing.</h1>
<p class="subhead">These are the public list changes and expiry rules from the vendor pages. A prompt count is not a dollar.</p>
</div>
</section>
<section class="scene scene-light">
<div class="article-shell wide">
<div class="table-wrap"><table class="ledger-table">
<thead><tr><th>Tool</th><th>Checked</th><th>What the list says now</th><th>Credit trap</th></tr></thead>
<tbody>
{''.join(body)}
</tbody>
</table></div>
<h2>Questions</h2>
<div class="faq-list">{''.join(faqs)}</div>
<p>Price a live workload in the <a href="/compare/ai-coding-assistants/">coding assistant calculator</a>, the <a href="/compare/ai-app-builders/">app-builder calculator</a>, the <a href="/compare/ai-video-avatar-cost/">voice and video minute calculator</a>, the <a href="/compare/automation-task-calculator/">automation task calculator</a>, or the <a href="/compare/ai-presentation-cost/">deck cost calculator</a>. <a href="/pricing-watch/credit-traps/">Credit traps</a> lists expiry windows and locks. The full dated log is <a href="/pricing-watch/">Pricing Watch</a>.</p>
</div>
</section>
</main>
<footer class="footer">
<span>© 2026 AIToolsEssentials</span>
<a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
<a href="/pricing-watch/">Pricing Watch</a>
<a href="/legal/corrections.html">Corrections</a>
</footer>
<script src="/js/site.js" defer></script>
<script src="/js/analytics.js" defer></script>
</body>
</html>
"""
    dest = root / "price-changes" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")
    return dest


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parents[1]))
