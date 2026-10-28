#!/usr/bin/env python3
"""Voice, avatar, Runway, and Midjourney calculator.

Minutes price Descript and Midjourney Fast GPU time. A separate seconds
box prices Runway at the published Gen-4.5 rate of 12 credits per second.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

from ledger_offers import receipt_footer_html
from site_chrome import CANONICAL_HEADER

DOMAIN = "https://aitoolsessentials.com"
PATH = "/compare/ai-video-avatar-cost/"
TITLE = "Voice, Avatar, Runway, and Midjourney Credit Ledger"
DESCRIPTION = (
    "Price ElevenLabs, Descript, HeyGen, Synthesia, Runway, and Midjourney "
    "from the checked summaries. Minutes pick a Descript media-hour plan and "
    "a Midjourney Fast GPU plan. Gen-4 seconds pick a Runway credit seat at "
    "12 credits per second. ElevenLabs, HeyGen, and Synthesia stay unconverted."
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
        "ElevenLabs, Descript, and HeyGen do not publish a separate clone fee on the checked pages, so the toggle does not add one. Synthesia's checked pricing text puts unlimited Personal Avatars on Enterprise, which is custom, so the toggle moves that row off the $29 Starter seat. The same toggle is Midjourney Stealth Mode: Basic ($10, 3.3 Fast hours) and Standard ($30, 15 Fast hours plus unlimited Relax) leave images public, so Stealth moves the row to Pro at $60 for 30 Fast hours, or Mega at $120 for 60.",
    ),
    (
        "How does Runway turn a clip into a monthly seat?",
        "The 18 Sep 2026 pricing page says Gen-4.5 costs 12 credits per generated second. Standard is $15 for 625 credits, about 52 seconds. Pro is $35 for 2,250 credits. Max is $95 for 9,500 credits, with up to one month of rollover. Retakes multiply the seconds first, which is how a 10-second clip at 5x still fits Standard (600 credits) and a 40-second clip at 5x moves to Max (2,400 credits). The page does not publish a Turbo credits-per-second rate, so Turbo is not priced. Max is not a relaxed unlimited plan.",
    ),
    (
        "How do Midjourney Fast hours use the minutes box?",
        "One finished minute is one Fast GPU minute. Basic covers 3.3 hours (198 minutes) at $10. Standard covers 15 hours at $30 and adds unlimited Relax image generations, which this sheet does not convert into Fast time. Pro covers 30 hours at $60. Mega covers 60 hours at $120. Unused Fast time does not roll over. Annual billing is 20% lower and is not the figure used here.",
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
<p class="subhead">Voice minutes, avatar credits, Runway Gen-4.5 seconds, and Midjourney Fast GPU hours sit on one sheet. A credit balance without a published per-minute rate stays unconverted.</p>
<p><a class="button button-blue" href="#calculator">Price the minutes</a> <a class="button button-ledger" href="/price-changes/">Price changes</a></p>
</div>
</section>
<section class="scene scene-light">
<div class="article-shell wide">
<p class="affiliate-inline">ElevenLabs, Descript, and Synthesia buttons are partner links. HeyGen, Runway, and Midjourney buttons go to the official site with our campaign tag. <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</p>
<p><a href="/embed/ai-video-avatar-cost/">Embed this calculator</a> · <a href="/embeds/">All embeds and badges</a></p>
<form id="calculator" class="ledger-sheet voice-calc">
<h2>Finished minutes and Gen-4 seconds</h2>
<div class="ledger-seats">
<label>Minutes / month <input id="voice-minutes" type="number" min="0" max="6000" value="60"></label>
<label>Gen-4 seconds <input id="voice-seconds" type="number" min="0" max="3600" value="10"></label>
<label>Retakes <select id="voice-retake"><option value="1">1x</option><option value="2">2x</option><option value="3">3x</option><option value="4">4x</option><option value="5">5x</option></select></label>
<label><input id="voice-clone" type="checkbox"> Private mode: studio avatar or Midjourney Stealth</label>
</div>
<p class="score-note">Minutes price Descript media time and Midjourney Fast GPU time. Seconds price Runway at 12 Gen-4.5 credits each. B-roll retakes are often 3x–5x.</p>
</form>
<div id="voice-result" class="ledger-sheet" aria-live="polite"></div>
<p class="ledger-cta"><a class="button button-blue" href="/go/elevenlabs/" rel="sponsored nofollow noopener">ElevenLabs</a> <a class="button button-blue" href="/go/descript/" rel="sponsored nofollow noopener">Descript</a> <a class="button button-blue" href="/go/heygen/" rel="external noopener">HeyGen</a> <a class="button button-blue" href="/go/synthesia/" rel="sponsored nofollow noopener">Synthesia</a> <a class="button button-blue" href="/go/runway/" rel="external noopener">Runway</a> <a class="button button-blue" href="/go/midjourney/" rel="external noopener">Midjourney</a></p>
<h2>Questions</h2>
<div class="faq-list">{faqs}</div>
<p>Reviews: <a href="/tools/elevenlabs/">ElevenLabs</a>, <a href="/tools/descript/">Descript</a>, <a href="/tools/heygen/">HeyGen</a>, <a href="/tools/synthesia/">Synthesia</a>, <a href="/tools/runway/">Runway</a>, <a href="/tools/midjourney/">Midjourney</a>. Sources: <a href="https://elevenlabs.io/pricing" rel="external noopener">ElevenLabs pricing</a>, <a href="https://descript.com/pricing" rel="external noopener">Descript pricing</a>, <a href="https://www.heygen.com/pricing" rel="external noopener">HeyGen pricing</a>, <a href="https://www.synthesia.io/pricing" rel="external noopener">Synthesia pricing</a>, <a href="https://runwayml.com/pricing" rel="external noopener">Runway pricing</a>, <a href="https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans" rel="external noopener">Midjourney plans</a>.</p>
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
      seconds: document.getElementById("voice-seconds").value,
      retake: document.getElementById("voice-retake").value,
      clone: document.getElementById("voice-clone").checked
    }});
    var rows = result.rows.map(function (row) {{
      var price = row.monthlyCents == null ? (row.unpriced || "Not priced from minutes") : calc.money(row.monthlyCents) + "/mo";
      var tone = row.verdict === "Keep" ? "keep" : (row.verdict === "Switch" || row.verdict === "Cut") ? "cut" : "test";
      return "<tr><th>" + row.name + "</th><td>" + row.tier + "</td><td>" + price + "</td><td>" + row.meter + "</td><td>" + row.expiry + "</td><td><span class=\\"ledger-stamp ledger-" + tone + "\\">" + row.verdict + "</span></td><td><a class=\\"button button-blue\\" href=\\"" + row.href + "\\" rel=\\"" + row.rel + "\\">Open " + row.name + "</a><p>" + row.note + "</p></td></tr>";
    }}).join("");
    document.getElementById("voice-result").innerHTML = "<p class=\\"ledger-kicker\\">" + result.demandedMinutes + " media or Fast minutes · " + result.generatedSeconds + " Gen-4.5 seconds after " + result.retake + "x</p><div class=\\"table-wrap\\"><table class=\\"ledger-table\\"><thead><tr><th>Tool</th><th>Plan</th><th>Monthly</th><th>Meter</th><th>Rollover</th><th>Call</th><th></th></tr></thead><tbody>" + rows + "</tbody></table></div>";
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
