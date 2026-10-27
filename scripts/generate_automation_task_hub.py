#!/usr/bin/env python3
"""Zapier vs Make vs n8n task, credit, and execution calculator."""
from __future__ import annotations

import html
import json
from pathlib import Path

from ledger_offers import receipt_footer_html
from site_chrome import CANONICAL_HEADER

DOMAIN = "https://aitoolsessentials.com"
PATH = "/compare/automation-task-calculator/"
TITLE = "Zapier vs Make vs n8n Monthly Task & Operation Burn Calculator"
DESCRIPTION = (
    "Turn workflows, steps, and daily runs into Zapier tasks, Make credits, "
    "and n8n executions. Prices come from the checked plan pages. Euros are "
    "not converted, and an unpublished task pack is not treated as a quote."
)

FAQS = [
    (
        "How is a Zapier task different from a Make operation?",
        "The directory records a Zapier task as one action execution. Filters that stop a Zap are not priced here. Make's checked page says most module actions use 1 credit, and AI modules can use more, which this calculator does not estimate. The same step count is therefore tasks on Zapier and credits on Make.",
    ),
    (
        "Why can n8n stay cheaper when a workflow has many steps?",
        "n8n's checked cloud plans meter complete workflow executions and say steps are unlimited. Ten steps in one run are still one execution. Starter is €20/month billed annually for 2,500 executions, Pro is €50 for 10,000, and Business is €667 for 40,000. Those euros are not converted to dollars.",
    ),
    (
        "What does the polling mix change?",
        "Webhook workflows use the runs-per-day you enter, over a 30-day month. The share you mark as polling is planned at 24 checks a day. None of the three pricing pages publish a price for an empty poll, so that 24 is an assumption. Set the mix to 100% webhooks and it drops out.",
    ),
]


def _esc(value: str) -> str:
    return html.escape(value, quote=True)


def _schema() -> str:
    graph = {
        "@context": "https://schema.org",
        "@graph": [
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
                "@type": "WebApplication",
                "name": TITLE,
                "applicationCategory": "BusinessApplication",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                "url": f"{DOMAIN}{PATH}",
                "description": DESCRIPTION,
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False)


def generate(root: Path) -> Path:
    faqs = "".join(
        f"<details><summary>{_esc(q)}</summary><p>{_esc(a)}</p></details>" for q, a in FAQS
    )
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
<meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<link rel="stylesheet" href="/css/styles.css">
<script type="application/ld+json">{_schema()}</script>
</head>
<body>
{CANONICAL_HEADER}
<main>
<section class="scene scene-dark ledger-mast">
<div style="max-width:880px;margin:0 auto;padding:72px 28px 36px">
<p class="kicker light">Pricing check · Sep–Oct 2026</p>
<h1>{_esc(TITLE)}</h1>
<p class="subhead">Zapier bills the step. Make bills the module. n8n bills the whole run. The annual gap is exact only when both USD plans publish an allowance that covers the volume.</p>
<p><a class="button button-blue" href="#calculator">Price the runs</a> <a class="button button-ledger" href="/compare/ai-video-avatar-cost/">Voice and video minutes</a></p>
</div>
</section>
<section class="scene scene-light">
<div class="article-shell wide">
<p class="affiliate-inline">The Make button is a partner link. Zapier and n8n buttons go to the official site with our campaign tag. <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</p>
<form id="calculator" class="ledger-sheet">
<h2>Workflow shape</h2>
<div class="ledger-seats">
<label>Active workflows <input id="auto-workflows" type="number" min="1" max="500" value="3"></label>
<label>Steps per workflow <input id="auto-steps" type="number" min="1" max="100" value="5"></label>
<label>Runs per day <input id="auto-runs" type="number" min="0" max="10000" value="4"></label>
<label>Webhook share <input id="auto-webhook" type="number" min="0" max="100" value="100"> %</label>
</div>
</form>
<div id="auto-result" class="ledger-sheet" aria-live="polite"></div>
<p class="ledger-cta"><a class="button button-blue" href="/go/make/" rel="sponsored nofollow noopener">Make</a> <a class="button button-blue" href="/go/n8n/" rel="external noopener">n8n</a> <a class="button button-blue" href="/go/zapier/" rel="external noopener">Zapier</a></p>
<h2>Questions</h2>
<div class="faq-list">{faqs}</div>
<p>Reviews: <a href="/tools/zapier-ai/">Zapier</a>, <a href="/tools/make/">Make</a>, <a href="/tools/n8n/">n8n</a>. Sources: <a href="https://zapier.com/pricing" rel="external noopener">Zapier pricing</a>, <a href="https://www.make.com/en/pricing" rel="external noopener">Make pricing</a>, <a href="https://n8n.io/pricing/" rel="external noopener">n8n pricing</a>.</p>
{receipt_footer_html()}
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
<script src="/js/automation-task-calculator.js"></script>
<script>
(function () {{
  var calc = window.AutomationTaskCalc;
  function render() {{
    var result = calc.priceAutomation({{
      workflows: document.getElementById("auto-workflows").value,
      steps: document.getElementById("auto-steps").value,
      runsPerDay: document.getElementById("auto-runs").value,
      webhookPercent: document.getElementById("auto-webhook").value
    }});
    var rows = result.rows.map(function (row) {{
      var price = row.monthlyCents == null ? "No published covering price" : calc.money(row.monthlyCents, row.currency) + "/mo";
      var year = row.annualCents == null ? "—" : calc.money(row.annualCents, row.currency) + "/yr";
      var tone = row.verdict === "Keep" ? "keep" : row.verdict === "Switch" ? "cut" : "test";
      return "<tr><th>" + row.name + "</th><td>" + row.units.toLocaleString("en-US") + " " + row.unitLabel + "</td><td>" + row.tier + "</td><td>" + price + "</td><td>" + year + "</td><td>" + row.expiry + "</td><td><span class=\\"ledger-stamp ledger-" + tone + "\\">" + row.verdict + "</span></td><td><a class=\\"button button-blue\\" href=\\"" + row.href + "\\" rel=\\"" + row.rel + "\\">Open " + row.name + "</a><p>" + row.meter + " " + row.note + "</p></td></tr>";
    }}).join("");
    var save = result.savingsAnnualCents ? calc.money(result.savingsAnnualCents, "USD") + "/yr" : "not exact";
    document.getElementById("auto-result").innerHTML = "<p class=\\"ledger-kicker\\">" + result.runs.toLocaleString("en-US") + " runs / 30 days · switch saving " + save + "</p><p>" + result.assumption + " " + result.savingsNote + "</p><div class=\\"table-wrap\\"><table class=\\"ledger-table\\"><thead><tr><th>Tool</th><th>Units</th><th>Plan</th><th>Monthly</th><th>Annual</th><th>Expiry</th><th>Call</th><th></th></tr></thead><tbody>" + rows + "</tbody></table></div>";
  }}
  document.getElementById("calculator").addEventListener("input", render);
  render();
}})();
</script>
<script src="/js/site.js" defer></script>
</body>
</html>
"""
    dest = root / "compare" / "automation-task-calculator" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")
    return dest


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parents[1]))
