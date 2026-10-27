#!/usr/bin/env python3
"""Voice and avatar minute calculator. Minutes price a plan only for Descript."""
from __future__ import annotations

import html
import json
from pathlib import Path

from ledger_offers import receipt_footer_html
from site_chrome import CANONICAL_HEADER

DOMAIN = "https://aitoolsessentials.com"
PATH = "/compare/ai-video-avatar-cost/"
TITLE = "AI Voice & Video Minute / Credit Overage Calculator"
DESCRIPTION = (
    "Compare ElevenLabs, Descript, HeyGen, and Synthesia from the checked "
    "pricing summaries. Finished minutes pick a Descript media-hour plan. "
    "Credit tools stay unconverted, because no credit-per-minute rate is published."
)

FAQS = [
    (
        "How many Descript media hours does a retake burn?",
        "The checked Descript page meters media hours, not retakes. This calculator treats each retake as another full finished minute: 30 finished minutes at 2x is 60 media minutes, which still fits the Free plan's 1 media hour. Hobbyist is $24/month for 10 media hours, Creator is $35 for 30, and Business is $65 for 40. Annual prices on that page are lower and are not the figure used here.",
    ),
    (
        "Why doesn't the ElevenLabs row turn minutes into credits?",
        "The 18 Sep 2026 pricing summary lists Free at 10,000 credits, Starter at $6 for 30,000, Creator at $22 for 121,000, and Pro at $99 for 600,000. It also says paid-plan credits can roll over up to two months. It does not say how many credits one finished minute uses, so this page does not invent that rate and does not add overage.",
    ),
    (
        "Does a custom voice or studio avatar change the price?",
        "ElevenLabs, Descript, and HeyGen do not publish a separate clone fee on the checked pages, so the toggle does not add one. Synthesia's checked pricing text puts unlimited Personal Avatars on Enterprise, which is custom, so the toggle moves that row off the $29 Starter seat.",
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
<p class="kicker light">Pricing check · Sep 2026</p>
<h1>{_esc(TITLE)}</h1>
<p class="subhead">Finished minutes pick a plan only where the vendor meters media hours. A credit balance is not a minute, and this page does not invent the conversion.</p>
<p><a class="button button-blue" href="#calculator">Price the minutes</a> <a class="button button-ledger" href="/price-changes/">Price changes</a></p>
</div>
</section>
<section class="scene scene-light">
<div class="article-shell wide">
<p class="affiliate-inline">ElevenLabs and Descript buttons are partner links. HeyGen and Synthesia buttons go to the official site with our campaign tag. <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</p>
<form id="calculator" class="ledger-sheet voice-calc">
<h2>Finished minutes</h2>
<div class="ledger-seats">
<label>Minutes / month <input id="voice-minutes" type="number" min="0" max="6000" value="60"></label>
<label>Retakes <select id="voice-retake"><option value="1">1x</option><option value="2">2x</option><option value="3">3x</option></select></label>
<label><input id="voice-clone" type="checkbox"> Custom voice clone / studio avatar</label>
</div>
</form>
<div id="voice-result" class="ledger-sheet" aria-live="polite"></div>
<p class="ledger-cta"><a class="button button-blue" href="/go/elevenlabs/" rel="sponsored nofollow noopener">ElevenLabs</a> <a class="button button-blue" href="/go/descript/" rel="sponsored nofollow noopener">Descript</a> <a class="button button-blue" href="/go/heygen/" rel="external noopener">HeyGen</a> <a class="button button-blue" href="/go/synthesia/" rel="external noopener">Synthesia</a></p>
<h2>Questions</h2>
<div class="faq-list">{faqs}</div>
<p>Reviews: <a href="/tools/elevenlabs/">ElevenLabs</a>, <a href="/tools/descript/">Descript</a>, <a href="/tools/heygen/">HeyGen</a>, <a href="/tools/synthesia/">Synthesia</a>. Sources: <a href="https://elevenlabs.io/pricing" rel="external noopener">ElevenLabs pricing</a>, <a href="https://descript.com/pricing" rel="external noopener">Descript pricing</a>, <a href="https://www.heygen.com/pricing" rel="external noopener">HeyGen pricing</a>, <a href="https://www.synthesia.io/pricing" rel="external noopener">Synthesia pricing</a>.</p>
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
<script src="/js/voice-video-calculator.js"></script>
<script>
(function () {{
  var calc = window.VoiceVideoCalc;
  function render() {{
    var result = calc.priceVoice({{
      minutes: document.getElementById("voice-minutes").value,
      retake: document.getElementById("voice-retake").value,
      clone: document.getElementById("voice-clone").checked
    }});
    var rows = result.rows.map(function (row) {{
      var price = row.monthlyCents == null ? "Not priced from minutes" : calc.money(row.monthlyCents) + "/mo";
      var tone = row.verdict === "Keep" ? "keep" : row.verdict === "Switch" ? "cut" : "test";
      return "<tr><th>" + row.name + "</th><td>" + row.tier + "</td><td>" + price + "</td><td>" + row.meter + "</td><td>" + row.expiry + "</td><td><span class=\\"ledger-stamp ledger-" + tone + "\\">" + row.verdict + "</span></td><td><a class=\\"button button-blue\\" href=\\"" + row.href + "\\" rel=\\"" + row.rel + "\\">Open " + row.name + "</a><p>" + row.note + "</p></td></tr>";
    }}).join("");
    document.getElementById("voice-result").innerHTML = "<p class=\\"ledger-kicker\\">" + result.demandedMinutes + " media minutes after " + result.retake + "x</p><div class=\\"table-wrap\\"><table class=\\"ledger-table\\"><thead><tr><th>Tool</th><th>Plan</th><th>Monthly</th><th>Meter</th><th>Rollover</th><th>Call</th><th></th></tr></thead><tbody>" + rows + "</tbody></table></div>";
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
    dest = root / "compare" / "ai-video-avatar-cost" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")
    return dest


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parents[1]))
