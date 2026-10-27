#!/usr/bin/env python3
"""AI coding-assistant pricing calculator.

List prices were checked on 2026-10-26. The calculator logic lives in
js/coding-assistant-calculator.js. Prompt counts select a published plan.
They are not converted into tokens or credits.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

from site_chrome import CANONICAL_HEADER

DOMAIN = "https://aitoolsessentials.com"
PATH = "/compare/ai-coding-assistants/"
TITLE = "AI Coding Assistants Pricing & Token ROI Calculator"
DESCRIPTION = (
    "Compare Cursor, Claude Code, GitHub Copilot, and Windsurf list prices "
    "checked 26 Oct 2026. Price a team of 1 to 50 and see the Keep, Test, or "
    "Cut call. Overage is added only when a vendor publishes a per-prompt price."
)

FAQS = [
    (
        "Is Cursor Pro $20 enough or do I need Ultra $200?",
        "Pro at $20 is not on cursor.com/pricing as of 26 Oct 2026. The page lists Free at $0, Plus at $8/month, Premium at $30/month, Super at $100/month, and Ultra at $200/month. Ultra is the power-user pool, published as 50× Plus. Premium, at $30, is the plan Cursor describes for new AI users, with a pool of 4× Plus. Super, at $100, is described for daily agent users and is 15× Plus. Third-party frontier models are not included in those prices. They bill at API list price. A legacy Cursor plan can continue: xAI's subscription docs, checked for this site on 13 Oct 2026, say existing Cursor plans continue and switching is optional. This calculator prices the plans a new buyer can select.",
    ),
    (
        "How much does Claude Code cost per month on Max vs API?",
        "Claude Code is included with paid Claude plans and draws from the same usage pool as chat. Pro is $20/month, or $200/year ($17/month equivalent on Anthropic's pricing card). Max 5x is $100/month and Max 20x is $200/month. Max is monthly only. Anthropic's help center describes Max 5x as 5× Pro usage per 5-hour session and Max 20x as 20×. There is no fixed message count. After a limit, paid plans can continue on usage credits at standard API rates. The pricing page lists Sonnet 5.5 at $2 per million input tokens and $10 per million output tokens, and Opus 5.5 at $4 and $20. Max also includes monthly API credits ($100 on 5x, $200 on 20x) that Anthropic says do not apply to Claude Code. This calculator does not turn a prompt into tokens, so the API path is not added as a dollar overage.",
    ),
    (
        "What counts as a Premium Request in GitHub Copilot Pro vs Pro+?",
        "GitHub's plans page checked 26 Oct 2026 meters GitHub AI Credits, not a unit called a premium request. Copilot Pro is $10/month with 1,500 total monthly AI credits (1,000 base plus 500 flex). Copilot Pro+ is $39/month with 7,000 (3,900 base plus 3,100 flex). Copilot Max is $100/month with 20,000. Copilot Free includes 2,000 completions a month and an AI-credit allowance the plans page does not number. Business is $19/user/month with 1,900 credits, and Enterprise is $39/user/month with 3,900. Usage past the pool is $0.01 per AI credit. Code completions stay unlimited on paid plans. The page does not say how many credits one agent prompt uses, so this calculator does not convert prompts into credits.",
    ),
    (
        "Windsurf Pro $15 vs Cursor Pro $20: how do prompt credits compare?",
        "They are not the same unit, and neither sticker is the current public list price for a new buyer. windsurf.com/pricing, checked 26 Oct 2026, lists Pro at $20/month and Max at $200/month. Devin's quota docs say an existing Pro subscriber at $15/month keeps that price, and that March 2026 replaced prompt credits with a daily and weekly quota. Add-on prompt credits were converted at $0.04 per credit. Cursor's $20 Pro tier is not on cursor.com/pricing. The current individual rungs are Plus $8, Premium $30, Super $100, and Ultra $200. Windsurf Pro includes frontier models inside the quota. Cursor's included pool does not include third-party frontier models. Neither vendor publishes a prompt-credit balance you can line up one for one.",
    ),
    (
        "Which AI coding stack is cheapest for a 5-person engineering team?",
        "At 20 prompts a day per developer, balanced models, and monthly billing, the published subscriptions are GitHub Copilot Pro at $50, Claude Pro at $100, Cursor Premium at $150, and Windsurf Teams at $200. Copilot Pro is the lowest published subscription, so the calculator marks it Keep, Claude Test, and Cursor and Windsurf Cut for that profile. That is the subscription, not a measured token bill. Copilot Business at $19/user ($95 for five) has a larger credit pool than Pro, and it is the org plan if you need centralized policy. Move the sliders for a different workload. Five heavy frontier seats are a different total.",
    ),
]


def _esc(value: str) -> str:
    return html.escape(value, quote=True)


def _schema() -> str:
    graph = [
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
        {
            "@type": "Dataset",
            "name": "AI coding assistant list prices checked 2026-10-26",
            "description": DESCRIPTION,
            "url": f"{DOMAIN}{PATH}",
            "dateModified": "2026-10-26",
            "creator": {"@type": "Organization", "name": "AIToolsEssentials", "url": f"{DOMAIN}/"},
            "variableMeasured": [
                {"@type": "PropertyValue", "name": "Cursor Free", "value": 0, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "Cursor Plus", "value": 8, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "Cursor Premium", "value": 30, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "Cursor Super", "value": 100, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "Cursor Ultra", "value": 200, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "Claude Pro monthly", "value": 20, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "Claude Pro annual", "value": 200, "unitText": "USD per year"},
                {"@type": "PropertyValue", "name": "Claude Max 5x", "value": 100, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "Claude Max 20x", "value": 200, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "GitHub Copilot Pro", "value": 10, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "GitHub Copilot Pro+", "value": 39, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "GitHub Copilot Max", "value": 100, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "GitHub Copilot Business", "value": 19, "unitText": "USD per user per month"},
                {"@type": "PropertyValue", "name": "GitHub Copilot Enterprise", "value": 39, "unitText": "USD per user per month"},
                {"@type": "PropertyValue", "name": "GitHub Copilot extra AI credit", "value": 0.01, "unitText": "USD per AI credit"},
                {"@type": "PropertyValue", "name": "Windsurf Pro", "value": 20, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "Windsurf Max", "value": 200, "unitText": "USD per month"},
                {"@type": "PropertyValue", "name": "Windsurf Teams full seat", "value": 40, "unitText": "USD per full seat per month"},
                {"@type": "PropertyValue", "name": "Windsurf Teams minimum", "value": 80, "unitText": "USD per month"},
            ],
        },
    ]
    apps = [
        (
            "Cursor",
            f"{DOMAIN}/tools/cursor/",
            "https://cursor.com/pricing",
            "0",
            "200",
            "Free $0, Plus $8/mo, Premium $30/mo, Super $100/mo, Ultra $200/mo. Teams from $30/user/mo. Checked 2026-10-26.",
        ),
        (
            "Claude Code",
            f"{DOMAIN}/tools/claude/",
            "https://www.anthropic.com/pricing",
            "0",
            "200",
            "Pro $20/mo or $200/year. Max 5x $100/mo. Max 20x $200/mo. Claude Code is included on paid plans. Checked 2026-10-26.",
        ),
        (
            "GitHub Copilot",
            f"{DOMAIN}/tools/github-copilot/",
            "https://docs.github.com/en/copilot/get-started/plans",
            "0",
            "100",
            "Free $0. Pro $10/mo. Pro+ $39/mo. Max $100/mo. Business $19/user/mo. Enterprise $39/user/mo. Extra usage $0.01 per AI credit. Checked 2026-10-26.",
        ),
        (
            "Windsurf",
            "https://windsurf.com/pricing",
            "https://windsurf.com/pricing",
            "0",
            "200",
            "Free $0. Pro $20/mo. Max $200/mo. Teams $40 per full seat per month with an $80 minimum. Enterprise is sales-assisted. Checked 2026-10-26.",
        ),
    ]
    for name, url, same_as, low, high, description in apps:
        graph.append(
            {
                "@type": "SoftwareApplication",
                "name": name,
                "applicationCategory": "DeveloperApplication",
                "operatingSystem": "Web",
                "url": url,
                "sameAs": same_as,
                "offers": {
                    "@type": "AggregateOffer",
                    "lowPrice": low,
                    "highPrice": high,
                    "priceCurrency": "USD",
                    "description": description,
                },
            }
        )
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def _faq_html() -> str:
    items = []
    for question, answer in FAQS:
        items.append(f"<details><summary>{_esc(question)}</summary><p>{_esc(answer)}</p></details>")
    return "".join(items)


STYLE = """
<style>
.coding-calc fieldset { border: 0; margin: 0 0 18px; padding: 0; }
.coding-calc legend { font-weight: 700; margin-bottom: 8px; }
.coding-range { display: grid; grid-template-columns: 1fr 96px; gap: 12px; align-items: center; }
.coding-range input[type="number"] { width: 100%; padding: 8px 10px; border: 1px solid #c7c7cc; border-radius: 10px; font: inherit; }
.coding-seg { display: flex; flex-wrap: wrap; gap: 8px; }
.coding-seg label { display: flex; gap: 8px; align-items: center; border: 1px solid #D8D4CC; border-radius: 3px; padding: 8px 14px; }
.coding-card-top { margin-bottom: 8px; }
.coding-verdict { display: inline-block; font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 12px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; border-radius: 3px; border: 1px solid currentColor; padding: 2px 6px; }
.coding-verdict-keep { color: #156E3F; }
.coding-verdict-test { color: #B45309; }
.coding-verdict-cut { color: #B91C1C; }
</style>
"""


def generate(root: Path) -> Path:
    dest = root / "compare" / "ai-coding-assistants" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{_esc(DESCRIPTION)}">
<title>{_esc(TITLE)} | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}{PATH}">
<meta property="og:title" content="{_esc(TITLE)} | AIToolsEssentials">
<meta property="og:description" content="{_esc(DESCRIPTION)}">
<meta property="og:url" content="{DOMAIN}{PATH}">
<meta property="og:type" content="article">
<meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{_esc(TITLE)} | AIToolsEssentials">
<meta name="twitter:description" content="{_esc(DESCRIPTION)}">
<meta name="twitter:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<link rel="stylesheet" href="/css/styles.css">
<link rel="icon" href="/assets/aitools-bot-mark.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/aitools-bot-logo-256.png">
<script type="application/ld+json">{_schema()}</script>
{STYLE}
</head>
<body>
{CANONICAL_HEADER}
<main>
<section class="scene scene-dark ledger-mast">
<div style="max-width:880px;margin:0 auto;padding:86px 28px 68px">
<p class="kicker light">Pricing check · 26 Oct 2026</p>
<h1>{_esc(TITLE)}</h1>
<p class="subhead">Four coding seats, one workload. The total is the published subscription. A prompt is not a token, and this page does not invent one.</p>
<p><a class="button button-blue" href="#calculator">Price the seats</a> <a class="button button-ghost-dark" href="/pricing-watch/">Pricing Watch</a></p>
</div>
</section>
<section class="scene scene-light content-hub">
<div class="article-shell wide">
<p class="affiliate-inline">Prices come from official vendor pages checked 26 Oct 2026. This is a planning calculator, not an invoice. <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</p>

<h2>Verified pricing</h2>
<div class="table-wrap"><table>
<thead><tr><th>Tool</th><th>Checked</th><th>List price</th><th>What the meter is</th></tr></thead>
<tbody>
<tr><td><a href="/tools/cursor/">Cursor</a></td><td>26 Oct 2026</td><td>Free $0 · Plus $8 · Premium $30 · Super $100 · Ultra $200 · Teams from $30/user</td><td>Weekly shared pool: Premium 4× Plus, Super 15× Plus, Ultra 50× Plus. Third-party models are extra at API list price. No annual discount on the page.</td></tr>
<tr><td><a href="/tools/claude/">Claude Code</a></td><td>26 Oct 2026</td><td>Pro $20/mo or $200/year · Max 5x $100/mo · Max 20x $200/mo</td><td>Claude Code is included on paid plans and shares the chat pool. No fixed message count. Max is monthly only.</td></tr>
<tr><td><a href="/tools/github-copilot/">GitHub Copilot</a></td><td>26 Oct 2026</td><td>Free $0 · Pro $10 · Pro+ $39 · Max $100 · Business $19/user · Enterprise $39/user</td><td>AI credits: Pro 1,500, Pro+ 7,000, Max 20,000, Business 1,900, Enterprise 3,900. Extra credits are $0.01. Free includes 2,000 completions a month.</td></tr>
<tr><td>Windsurf</td><td>26 Oct 2026</td><td>Free $0 · Pro $20 · Max $200 · Teams $40/full seat ($80 minimum) · Enterprise custom</td><td>Daily and weekly quota. Prompt credits were retired in March 2026. Extra usage is API list price. Existing Pro subscribers can keep $15.</td></tr>
</tbody>
</table></div>
<p>Sources: <a href="https://cursor.com/pricing" rel="external noopener">Cursor pricing</a>, <a href="https://www.anthropic.com/pricing" rel="external noopener">Anthropic pricing</a>, <a href="https://support.claude.com/en/articles/11049762-choose-a-claude-plan" rel="external noopener">Claude plan guide</a>, <a href="https://docs.github.com/en/copilot/get-started/plans" rel="external noopener">GitHub Copilot plans</a>, <a href="https://windsurf.com/pricing" rel="external noopener">Windsurf pricing</a>, <a href="https://docs.devin.ai/admin/billing/self-serve" rel="external noopener">Devin self-serve plans</a>, <a href="https://docs.devin.ai/desktop/accounts/quota" rel="external noopener">Devin quota migration</a>. Windsurf's pricing page is titled as Devin plans.</p>

<h2 id="calculator">Team and solo cost calculator</h2>
<p>Set the seats and the heavy prompts each developer runs in a day. The band is a planning label, not a measured burn rate: 5–25 is light, 26–60 is steady, and 61–100 is heavy. Frontier steps the published pool up where the vendor says harder models draw more of it. Overage stays at $0 unless the vendor publishes a price per prompt. None of these four do.</p>
<div class="score-card">
<form id="coding-calc" class="coding-calc">
<fieldset>
<legend>Team size</legend>
<div class="coding-range">
<input id="coding-seats-range" type="range" min="1" max="50" value="5" aria-label="Team size slider">
<input id="coding-seats" type="number" min="1" max="50" value="5" aria-label="Developers, from 1 to 50">
</div>
</fieldset>
<fieldset>
<legend>Daily agentic prompts per developer</legend>
<div class="coding-range">
<input id="coding-prompts-range" type="range" min="5" max="100" value="20" aria-label="Daily prompts slider">
<input id="coding-prompts" type="number" min="5" max="100" value="20" aria-label="Heavy prompts per developer per day, from 5 to 100">
</div>
</fieldset>
<fieldset>
<legend>Model tier</legend>
<div class="coding-seg">
<label><input type="radio" name="coding-tier" value="balanced" checked> Balanced (Sonnet / GPT-5 / Fast)</label>
<label><input type="radio" name="coding-tier" value="frontier"> Frontier Heavy (Opus / Deep Reasoning / Background Agents)</label>
</div>
</fieldset>
<fieldset>
<legend>Billing cadence</legend>
<div class="coding-seg">
<label><input id="coding-cadence-monthly" type="radio" name="coding-cadence" value="monthly" checked> Monthly</label>
<label><input id="coding-cadence-annual" type="radio" name="coding-cadence" value="annual"> Annual</label>
</div>
</fieldset>
</form>
<div id="coding-result" aria-live="polite">
<p>The subscription totals load in this browser.</p>
</div>
</div>
<noscript>
<p><strong>Keep</strong> GitHub Copilot Pro at $50/month for five developers at 20 balanced prompts a day. <strong>Test</strong> Claude Pro at $100. <strong>Cut</strong> Cursor Premium at $150 and Windsurf Teams at $200 for that same profile. Overage is not estimated.</p>
</noscript>

<h2>How the call is made</h2>
<ul>
<li><strong>Keep</strong> is the lowest published subscription whose plan actually includes the model class you selected.</li>
<li><strong>Test</strong> is another seat at or under 2.5× that price. It is worth a trial if the editor or the terminal is the job, not because the quota is proven to last.</li>
<li><strong>Cut</strong> means do not also pay for that seat at this workload. It is overlap, or the published price is the wrong size.</li>
<li>Cursor's included pool is the X Subscription allowance. Frontier models from other labs are not in that price, so Cursor is not the Keep seat when Frontier Heavy is selected.</li>
<li>Annual billing changes Claude Pro only, from $20/month to $200/year. Max, Copilot, Cursor, and Windsurf have no lower annual list price on the pages checked.</li>
</ul>

<h2>Questions</h2>
<div class="faq-list">{_faq_html()}</div>

<p>Read the lane split in <a href="/articles/claude-code-vs-cursor-vs-copilot.html">Claude Code vs Cursor vs Copilot</a>, then run the <a href="/stack-audit.html">Stack Audit</a> if these seats are already on the card. Credit clocks are on <a href="/price-changes/">Price changes</a>.</p>
<p>Switch links: <a href="/go/cursor/">Cursor</a>, <a href="/go/claude/">Claude</a>, <a href="/go/github-copilot/">GitHub Copilot</a>, <a href="/go/windsurf/">Windsurf</a>.</p>
{__import__('ledger_offers').receipt_footer_html()}
</div>
</section>
</main>
<footer class="footer">
<span>© 2026 AIToolsEssentials</span>
<a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
<a href="/legal/about.html">About</a>
<a href="/legal/privacy.html">Privacy</a>
<a href="/legal/terms.html">Terms</a>
<a href="/legal/corrections.html">Corrections</a>
<a href="/pricing-watch/">Pricing Watch</a>
<a href="/newsletter/">Keep, Test, Cut</a>
<a href="mailto:contact@aitoolsessentials.com">Contact</a>
</footer>
<script src="/js/coding-assistant-calculator.js" defer></script>
<script src="/js/site.js" defer></script>
<script src="/js/analytics.js" defer></script>
<script src="/js/cookie-consent.js" defer></script>
</body>
</html>
"""
    dest.write_text(page, encoding="utf-8")
    return dest


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parents[1]))
