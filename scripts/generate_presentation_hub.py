#!/usr/bin/env python3
"""Presentation and deck cost calculator. Decks do not pick a credit tier."""
from __future__ import annotations

import html
import json
from pathlib import Path

from ledger_offers import receipt_footer_html
from site_chrome import CANONICAL_HEADER

DOMAIN = "https://aitoolsessentials.com"
PATH = "/compare/ai-presentation-cost/"
TITLE = "AI Presentation & Deck Cost Calculator"
DESCRIPTION = (
    "Compare Gamma, Canva AI, HTMLSlides, and Microsoft 365 Copilot from the "
    "checked pricing summaries. A deck count does not convert into credits, "
    "and a month-to-month sticker that was not published stays blank."
)

FAQS = [
    (
        "Why doesn't the deck count change the price?",
        "Gamma meters credits and slides per prompt, not a price per finished deck. Canva meters an AI-use allowance. HTMLSlides sells a seat and separate credit packs, and the checked page does not say how many credits one deck uses. Microsoft 365 Copilot does not meter decks. This calculator shows the seat the checked page actually prices.",
    ),
    (
        "Why is a month-to-month Gamma or Canva seat blank?",
        "Gamma's 1 Oct 2026 check prints a per-seat monthly equivalent and an annual bill, and it advertises saving up to 28%. Canva's annual view prints US$0, US$144, and US$250 per year and advertises saving from 16%. Neither page's month-to-month sticker is the figure used here, and this page does not reverse a savings claim into a monthly price.",
    ),
    (
        "Where is Beautiful.ai?",
        "Beautiful.ai is mentioned in Gamma's help material and as a partner-program example. It is not a directory row on this site, and no checked price for it is published here. This calculator does not invent one and does not open a Beautiful.ai hop.",
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
<p class="kicker light">Pricing check · Oct 2026</p>
<h1>{_esc(TITLE)}</h1>
<p class="subhead">Four tools with a checked price. Beautiful.ai is not one of them. A finished deck is not a credit, and a savings percentage is not a monthly sticker.</p>
<p><a class="button button-blue" href="#calculator">Price the seat</a> <a class="button button-ledger" href="/pricing-watch/credit-traps/">Credit traps</a></p>
</div>
</section>
<section class="scene scene-light">
<div class="article-shell wide">
<p class="affiliate-inline">The Gamma button is a partner link. Canva AI, HTMLSlides, and Microsoft 365 Copilot buttons go to the official site with our campaign tag. <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</p>
<p>Beautiful.ai has no checked directory price on this site, so it is not in the ledger and it has no hop here.</p>
<form id="calculator" class="ledger-sheet">
<h2>The seat</h2>
<div class="ledger-seats">
<label>Seats <input id="deck-seats" type="range" min="1" max="25" value="1"> <output id="deck-seats-out">1</output></label>
<label>Decks / month <input id="deck-count" type="number" min="0" max="400" value="4"></label>
<label><input id="deck-brand" type="checkbox"> Custom brand kit</label>
<label><input id="deck-watermark" type="checkbox"> Export without watermark</label>
<label><input id="deck-annual" type="checkbox" checked> Annual billing</label>
</div>
</form>
<div id="deck-result" class="ledger-sheet" aria-live="polite"></div>
<p class="ledger-cta"><a class="button button-blue" href="/go/gamma/" rel="sponsored nofollow noopener">Gamma</a> <a class="button button-blue" href="/go/canva-ai/" rel="external noopener">Canva AI</a> <a class="button button-blue" href="/go/htmlslides/" rel="external noopener">HTMLSlides</a> <a class="button button-blue" href="/go/microsoft-copilot/" rel="external noopener">Microsoft 365 Copilot</a></p>
<h2>Questions</h2>
<div class="faq-list">{faqs}</div>
<p>Reviews: <a href="/tools/gamma/">Gamma</a>, <a href="/tools/canva-ai/">Canva AI</a>, <a href="/tools/htmlslides/">HTMLSlides</a>, <a href="/tools/microsoft-copilot/">Microsoft 365 Copilot</a>. Sources: <a href="https://gamma.app/pricing" rel="external noopener">Gamma pricing</a>, <a href="https://www.canva.com/pricing/" rel="external noopener">Canva pricing</a>, <a href="https://www.htmlslides.ai/pricing" rel="external noopener">HTMLSlides pricing</a>, <a href="https://www.microsoft.com/en-us/microsoft-365-copilot/pricing" rel="external noopener">Microsoft 365 Copilot pricing</a>.</p>
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
<a href="/newsletter/">Newsletter</a>
<a href="/newsletter/">Keep, Test, Cut</a>
<a href="mailto:contact@aitoolsessentials.com">Contact</a>
</footer>
<script src="/js/presentation-calculator.js"></script>
<script>
(function () {{
  var calc = window.PresentationCalc;
  function render() {{
    var seats = document.getElementById("deck-seats");
    document.getElementById("deck-seats-out").textContent = seats.value;
    var result = calc.priceDeck({{
      seats: seats.value,
      decks: document.getElementById("deck-count").value,
      brand: document.getElementById("deck-brand").checked,
      watermark: document.getElementById("deck-watermark").checked,
      annual: document.getElementById("deck-annual").checked
    }});
    var rows = result.rows.map(function (row) {{
      var monthly = row.monthlyCents == null ? "Not on the checked page" : calc.money(row.monthlyCents) + "/mo";
      var annual = row.annualCents == null ? "—" : calc.money(row.annualCents) + "/yr";
      var tone = row.verdict === "Keep" ? "keep" : row.verdict === "Cut" ? "cut" : "test";
      return "<tr><th>" + row.name + "</th><td>" + row.tier + "</td><td>" + monthly + "</td><td>" + annual + "</td><td>" + row.meter + "</td><td><span class=\\"ledger-stamp ledger-" + tone + "\\">" + row.verdict + "</span></td><td><a class=\\"button button-blue\\" href=\\"" + row.href + "\\" rel=\\"" + row.rel + "\\">Open " + row.name + "</a><p>" + row.note + "</p></td></tr>";
    }}).join("");
    var gap = result.savingsAnnualCents > 0
      ? "<p>Annual gap between the cheapest and dearest covering seat: " + calc.money(result.savingsAnnualCents) + ". Unconfirmed rows stay out of that gap.</p>"
      : "<p>No dollar gap. A row stays out until the checked page covers the toggles with a published USD price.</p>";
    document.getElementById("deck-result").innerHTML = "<p class=\\"ledger-kicker\\">" + result.seats + " seats · " + result.decks + " decks. The deck count does not change a price.</p>" + gap + "<div class=\\"table-wrap\\"><table class=\\"ledger-table\\"><thead><tr><th>Tool</th><th>Plan</th><th>Monthly</th><th>Annual</th><th>Rule</th><th>Call</th><th></th></tr></thead><tbody>" + rows + "</tbody></table></div>";
  }}
  document.getElementById("calculator").addEventListener("input", render);
  document.getElementById("calculator").addEventListener("change", render);
  render();
}})();
</script>
<script src="/js/site.js" defer></script>
</body>
</html>
"""
    dest = root / "compare" / "ai-presentation-cost" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")
    return dest


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parents[1]))
