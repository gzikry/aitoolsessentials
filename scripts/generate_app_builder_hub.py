#!/usr/bin/env python3
"""AI app-builder pricing and credit-burn comparison hub.

Prices are the 25 Oct 2026 official-page check recorded in Keep, Test, Cut
Issue 7. The calculator logic lives in js/app-builder-calculator.js.
"""
from __future__ import annotations

import json
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"
PATH = "/compare/ai-app-builders/"
TITLE = "v0 vs Bolt.new vs Lovable vs Replit"
DESCRIPTION = (
    "Compare v0, Bolt.new, Lovable, and Replit prices checked 25 Oct 2026. "
    "Calculate duplicate-seat waste, the 65-day v0 credit window, the 2-month "
    "Lovable credit window, and the Keep, Test First, or Cut call."
)

FAQS = [
    (
        "Is v0's $20 Premium tier still available to new signups?",
        "No. Checked 25 Oct 2026, legacy Premium at $20/mo is closed to new signups. "
        "New accounts start on Free at $0 with a one-time $5 signup credit and a 7-message daily limit. "
        "Existing Free accounts keep a recurring $5 monthly credit. The next paid rung is Plus at $30 per user a month.",
    ),
    (
        "Does Replit still have a free Starter tier?",
        "No. The 25 Oct 2026 public table lists Core at $20/mo ($18 billed annually), Pro at $100/mo ($90 billed annually), and Enterprise. "
        "The free Starter tier from the 21 Aug check is off the page.",
    ),
    (
        "How long do v0 and Lovable credits last?",
        "v0 monthly credits and top-ups expire after 65 days, and v0 locks purchased credits if the paid plan lapses. "
        "Lovable monthly credits expire after 2 months. Lovable daily grants do not roll over.",
    ),
    (
        "Should I pay for two AI app builders at once?",
        "No. Keep at most one paid builder for the prototype you are shipping this month. "
        "If you already hold legacy v0 Premium at $20, keep that seat, because you cannot buy it back. "
        "Cut a second paid seat. If you only spin up a UI once a quarter, test Bolt.new Free or Lovable Free instead.",
    ),
    (
        "What does v0 Business add over Plus?",
        "Business is $100 per user a month and Plus is $30 per user a month. "
        "Both include a $30 monthly credit allowance. The extra $70 buys training-data opt-out and team controls, not more generation capacity.",
    ),
]

APPS = [
    {
        "name": "v0",
        "url": f"{DOMAIN}/tools/v0/",
        "sameAs": "https://v0.app/docs/pricing",
        "low": "0",
        "high": "100",
        "description": "Free $0 with a one-time $5 signup credit. Legacy Premium $20/mo closed to new signups. Plus $30/user/mo. Business $100/user/mo with a $30 monthly credit allowance. Checked 2026-10-25.",
    },
    {
        "name": "Replit",
        "url": f"{DOMAIN}/tools/replit-ai/",
        "sameAs": "https://replit.com/pricing",
        "low": "20",
        "high": "100",
        "description": "Core $20/mo or $18/mo billed annually. Pro $100/mo or $90/mo billed annually. Enterprise custom. No free Starter tier on the public page. Checked 2026-10-25.",
    },
    {
        "name": "Bolt.new",
        "url": f"{DOMAIN}/tools/bolt-new/",
        "sameAs": "https://bolt.new/pricing",
        "low": "0",
        "high": "30",
        "description": "Free $0 with 1 million tokens a month. Pro $25/mo ($18/mo billed annually, $216/year) for 10 million tokens. Teams $30/mo ($27 annual). Checked 2026-10-25.",
    },
    {
        "name": "Lovable",
        "url": f"{DOMAIN}/tools/lovable/",
        "sameAs": "https://lovable.dev/pricing",
        "low": "0",
        "high": "50",
        "description": "Free $0 with 5 daily credits capped at 30 a month. Pro $25/mo ($21 annual) with 100 monthly credits plus 5 daily credits. Business $50/mo ($42 annual). Checked 2026-10-25.",
    },
]


def _schema() -> str:
    graph = [
        {
            "@type": "Article",
            "headline": TITLE,
            "description": DESCRIPTION,
            "datePublished": "2026-10-27",
            "dateModified": "2026-10-26",
            "author": {"@type": "Organization", "name": "AIToolsEssentials"},
            "publisher": {
                "@type": "Organization",
                "name": "AIToolsEssentials",
                "url": f"{DOMAIN}/",
            },
            "mainEntityOfPage": f"{DOMAIN}{PATH}",
            "image": f"{DOMAIN}/assets/og-ai-tools.jpg",
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {"@type": "Answer", "text": answer},
                }
                for question, answer in FAQS
            ],
        },
    ]
    for app in APPS:
        graph.append(
            {
                "@type": "SoftwareApplication",
                "name": app["name"],
                "applicationCategory": "DeveloperApplication",
                "operatingSystem": "Web",
                "url": app["url"],
                "sameAs": app["sameAs"],
                "offers": {
                    "@type": "AggregateOffer",
                    "lowPrice": app["low"],
                    "highPrice": app["high"],
                    "priceCurrency": "USD",
                    "description": app["description"],
                },
            }
        )
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def _faq_html() -> str:
    items = []
    for question, answer in FAQS:
        items.append(f"<details><summary>{question}</summary><p>{answer}</p></details>")
    return "".join(items)


def generate(root: Path) -> Path:
    dest = root / "compare" / "ai-app-builders" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    page = f'''<!doctype html>
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
<meta property="og:type" content="article">
<meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE} | AIToolsEssentials">
<meta name="twitter:description" content="{DESCRIPTION}">
<meta name="twitter:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<link rel="stylesheet" href="/css/styles.css">
<script type="application/ld+json">{_schema()}</script>
<style>
.app-builder-calc fieldset {{ border: 0; margin: 0; padding: 0; }}
.app-builder-calc legend {{ font-weight: 700; margin-bottom: 8px; }}
.app-builder-calc label {{ display: flex; gap: 10px; align-items: flex-start; margin: 8px 0; }}
.app-builder-seats, .app-builder-cadence {{ margin-bottom: 16px; }}
.app-builder-waste {{ display: flex; justify-content: space-between; gap: 12px; align-items: baseline; }}
.app-builder-waste strong {{ font-size: 2rem; line-height: 1; }}
#app-builder-result h3 {{ margin: 16px 0 6px; }}
</style>
</head>
<body>
<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a></header>
<main>
<section class="scene scene-dark">
<div style="max-width:880px;margin:0 auto;padding:86px 28px 68px">
<p class="kicker light">Pricing check · 25 Oct 2026</p>
<h1>{TITLE}</h1>
<p class="subhead">Vercel’s $20 individual rung is closing and Replit’s free Starter tier is off the page. Don’t pay for two prompt-to-app builders at once.</p>
<p><a class="button button-blue" href="#calculator">Price your seats</a> <a class="button button-ghost-dark" href="/newsletter/2026-w44.html">Read Issue 7</a></p>
</div>
</section>
<section class="scene scene-light content-hub">
<div class="article-shell wide">
<p class="affiliate-inline">Prices come from official vendor pages checked 25 Oct 2026. This page is a planning calculator, not a bill. <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</p>

<h2>Verified pricing</h2>
<div class="table-wrap"><table>
<thead><tr><th>Tool</th><th>Check</th><th>Verified pricing</th></tr></thead>
<tbody>
<tr><td><a href="/tools/v0/">v0</a></td><td>25 Oct 2026 · Tier sunset</td><td>Free $0 ($5 once for new users) · Premium $20/mo closed to new signups · Plus $30/user/mo · Business $100/user/mo</td></tr>
<tr><td><a href="/tools/replit-ai/">Replit</a></td><td>25 Oct 2026 · Starter off page</td><td>Core $20/mo ($18 annual) · Pro $100/mo ($90 annual) · Enterprise custom</td></tr>
<tr><td><a href="/tools/bolt-new/">Bolt.new</a></td><td>25 Oct 2026 · Verified</td><td>Free $0 (1M tokens/mo) · Pro $25/mo ($18 annual, $216/yr) · Teams $30/mo ($27 annual)</td></tr>
<tr><td><a href="/tools/lovable/">Lovable</a></td><td>25 Oct 2026 · Verified</td><td>Free $0 (5 daily credits, 30/mo cap) · Pro $25/mo ($21 annual) · Business $50/mo ($42 annual)</td></tr>
</tbody>
</table></div>
<p>v0 monthly credits expire after 65 days. Lovable monthly credits expire after 2 months. Business on v0 costs $100 per user a month and includes the same $30 monthly credit allowance as Plus. Full tracker: <a href="/pricing-watch/">Pricing Watch</a>.</p>

<h2 id="calculator">App-builder seat and credit-burn calculator</h2>
<p>Check the seats you pay for now and how often you actually prototype. The waste figure is the annual cost of every selected seat except the one this call says to keep. It stays in this browser.</p>
<div class="score-card">
<form id="app-builder-calc" class="app-builder-calc">
<fieldset class="app-builder-seats">
<legend>Seats you currently pay for</legend>
<label><input type="checkbox" name="seat" value="legacy-v0"> Legacy v0 $20</label>
<label><input type="checkbox" name="seat" value="v0-plus"> v0 Plus $30</label>
<label><input type="checkbox" name="seat" value="replit-core"> Replit Core $20</label>
<label><input type="checkbox" name="seat" value="bolt-pro"> Bolt.new Pro $25</label>
<label><input type="checkbox" name="seat" value="lovable-pro"> Lovable Pro $25</label>
</fieldset>
<fieldset class="app-builder-cadence">
<legend>Monthly prototype cadence</legend>
<label><input type="radio" name="cadence" value="shipping" checked> Shipping a prototype this month</label>
<label><input type="radio" name="cadence" value="quarterly"> Once a quarter</label>
<label><input type="radio" name="cadence" value="idle"> Idle — no commit in 30 days</label>
</fieldset>
<p id="app-builder-active-wrap" hidden><label>Which paid seat is shipping this month? <select id="app-builder-active"></select></label></p>
</form>
<div id="app-builder-result" aria-live="polite">
<p class="app-builder-waste"><span>Annual duplicate-seat waste</span><strong data-waste="0">$0</strong></p>
<p>Select the seats you pay for. The Keep, Test First, and Cut call updates on this page.</p>
</div>
</div>
<noscript>
<p><strong>Keep</strong> legacy v0 Premium at $20/mo if you already hold it, or one active builder. <strong>Test First</strong> Bolt.new Free (1M tokens/mo) or Lovable Free (5 daily credits). <strong>Cut</strong> a second paid app-builder seat. v0 credits expire after 65 days. Lovable monthly credits expire after 2 months.</p>
</noscript>

<h2>How the call is made</h2>
<ul>
<li><strong>Keep</strong> legacy v0 Premium ($20/mo) if you already hold it. Cancelling that tier means you cannot buy it back. Otherwise keep one paid builder for the prototype shipping this month.</li>
<li><strong>Test First</strong> Bolt.new Free (1 million tokens a month, 300,000 daily limit) or Lovable Free (5 daily credits, up to 30 a month).</li>
<li><strong>Cut</strong> every other paid app-builder seat, and cut all of them when the builder has not shipped a commit in 30 days — except a legacy v0 seat you already hold.</li>
</ul>

<h2>Questions</h2>
<div class="faq-list">{_faq_html()}</div>

<p>Issue 7 of Keep, Test, Cut, 27 Oct 2026, walks through the same check. <a href="/newsletter/2026-w44.html">Read the letter</a>. Then run the <a href="/stack-audit.html">Stack Audit</a> for the rest of the card.</p>
</div>
</section>
</main>
<footer class="footer">
<span>© 2026 AIToolsEssentials</span>
<a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
<a href="/pricing-watch/">Pricing Watch</a>
<a href="/newsletter/">Keep, Test, Cut</a>
<a href="/legal/privacy.html">Privacy</a>
</footer>
<script src="/js/app-builder-calculator.js" defer></script>
<script src="/js/site.js" defer></script>
<script src="/js/analytics.js" defer></script>
</body>
</html>
'''
    dest.write_text(page, encoding="utf-8")
    return dest


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parents[1]))
