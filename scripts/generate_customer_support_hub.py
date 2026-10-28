#!/usr/bin/env python3
"""Resolution-fee versus seat calculator for AI customer support."""
from __future__ import annotations

import html
import json
from pathlib import Path

from ledger_offers import receipt_footer_html
from site_chrome import CANONICAL_HEADER

DOMAIN = "https://aitoolsessentials.com"
PATH = "/compare/ai-customer-support-cost/"
TITLE = "AI customer support resolution-fee calculator"
DESCRIPTION = (
    "Compare Intercom Fin, Zendesk automated resolutions, Tidio Lyro packs, "
    "and CustomGPT.ai's flat subscription. Ada and Sierra stay unpriced because "
    "they do not publish a per-resolution rate."
)

FAQS = [
    (
        "Does Intercom charge again if the customer replies?",
        "Intercom's outcome article says a return to the same conversation is deducted and not charged. This calculator does not add a second Fin outcome when the retry toggle is on. Standalone Fin still has a 50-outcome monthly minimum.",
    ),
    (
        "Why is Tidio's free 50 not subtracted every month?",
        "Tidio's help center says the 50 free Lyro conversations are one-time and do not reset. A new thread after inactivity counts as another conversation. The monthly bill is the smallest published pack that covers the conversations, and volume above 1,000 is left unpriced.",
    ),
    (
        "Is CustomGPT.ai a per-resolution product?",
        "No. Standard is $99 per month with 1,000 queries and Premium is $499 per month with 5,000, checked 2026-10-27. Extra queries are $375 per month for 2,500. There is no per-resolution fee. The visit button is a partner link.",
    ),
]


def _esc(value: str) -> str:
    return html.escape(value, quote=True)


def _pricing(root: Path) -> dict:
    return json.loads((root / "data" / "customer_support_pricing.json").read_text(encoding="utf-8"))


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


def _form(compact: bool) -> str:
    advanced = ""
    if not compact:
        advanced = """
<details>
<summary>Plan options</summary>
<label>Fin <select name="fin-mode"><option value="desk">With Intercom Essential seats</option><option value="standalone">Standalone Fin</option></select></label>
<label>Zendesk <select name="zd-plan"><option value="team">Suite Team</option><option value="pro">Suite Professional</option></select></label>
<label>Zendesk billing <select name="zd-billing"><option value="annual">Annual</option><option value="monthly">Monthly</option></select></label>
<label>Extra resolutions <select name="zd-resolution"><option value="payg">Pay as you go $2</option><option value="committed">Committed $1.50</option></select></label>
<label><input name="copilot" type="checkbox"> Zendesk Copilot</label>
</details>
"""
    else:
        advanced = """
<input type="hidden" name="fin-mode" value="desk">
<input type="hidden" name="zd-plan" value="team">
<input type="hidden" name="zd-billing" value="annual">
<input type="hidden" name="zd-resolution" value="payg">
"""
    return f"""
<form id="support-calc" class="ledger-sheet">
<div class="ledger-seats">
<label>Tickets / month <input name="tickets" type="number" min="100" max="25000" value="800"></label>
<label>AI resolution % <input name="rate" type="number" min="20" max="80" value="45"></label>
<label>Human seats <input name="seats" type="number" min="1" max="50" value="2"></label>
<label><input name="reopen" type="checkbox"> Retry / re-open inflation</label>
</div>
<p>
<button type="button" data-support-preset="solo">Solo SaaS</button>
<button type="button" data-support-preset="ecom">Growing E-Com</button>
<button type="button" data-support-preset="scale">Scale-Up Support Desk</button>
</p>
{advanced}
</form>
<div id="support-result" aria-live="polite"></div>
"""


def _boot() -> str:
    return r"""
<script>
(function () {
  var node = document.getElementById("support-pricing");
  if (!node || !window.SupportCalc) return;
  var pricing = JSON.parse(node.textContent);
  var form = document.getElementById("support-calc");
  var out = document.getElementById("support-result");
  if (location.search) SupportCalc.fillForm(form, new URLSearchParams(location.search));
  function paint() {
    out.innerHTML = SupportCalc.render(SupportCalc.priceSupport(SupportCalc.readForm(form), pricing));
  }
  form.addEventListener("input", paint);
  form.addEventListener("change", paint);
  document.querySelectorAll("[data-support-preset]").forEach(function (button) {
    button.addEventListener("click", function () {
      SupportCalc.applyPreset(form, button.getAttribute("data-support-preset"));
      paint();
    });
  });
  var copy = document.getElementById("support-share");
  if (copy) copy.addEventListener("click", function () {
    var url = location.origin + location.pathname + "?" + SupportCalc.queryFrom(SupportCalc.readForm(form));
    var done = function () { copy.textContent = "Copied"; };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done);
    else done();
  });
  paint();
})();
</script>
"""


def embed_page(root: Path) -> str:
    pricing = json.dumps(_pricing(root), ensure_ascii=False)
    count = len(json.loads((root / "data" / "tools.json").read_text(encoding="utf-8")))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{_esc(DESCRIPTION)}">
<title>{_esc(TITLE)} embed | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/embed/customer-support-cost.html">
<style>
html,body{{margin:0;background:#FAF8F5;color:#111315}}
body{{font:15px/1.4 Newsreader,Georgia,serif;padding:12px 14px 48px}}
h1{{font-size:22px;margin:0 0 8px}}
label,button{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:12px}}
.ledger-seats{{display:grid;grid-template-columns:1fr 1fr;gap:6px}}
input,select{{border:1px solid #111315;background:#fff;color:#111315;font:inherit}}
.embed-bar{{position:sticky;bottom:0;margin:8px -14px 0;padding:8px 14px;background:#111315;color:#FAF8F5;font:11px/1.35 "IBM Plex Mono",ui-monospace,monospace}}
.embed-bar a{{color:#FAF8F5}}
</style>
</head>
<body>
<main>
<h1>{_esc(TITLE)}</h1>
<script type="application/json" id="support-pricing">{pricing}</script>
{_form(True)}
<footer class="embed-bar">Source: AI Tools Essentials Audited Price Ledger → <a href="{PATH}">Full {count}-tool breakdown</a> · <a href="/newsletter/">Newsletter</a> · <a href="/embeds/">Embeds</a></footer>
</main>
<script src="/js/customer-support-calculator.js"></script>
{_boot()}
</body>
</html>
"""


def generate(root: Path) -> Path:
    pricing = json.dumps(_pricing(root), ensure_ascii=False)
    faqs = "".join(
        f"<details><summary>{_esc(q)}</summary><p>{_esc(a)}</p></details>" for q, a in FAQS
    )
    iframe = (
        f'<iframe src="{DOMAIN}/embed/customer-support-cost.html" '
        f'title="{_esc(TITLE)}" width="100%" height="480" '
        f'style="border:1px solid #111315;background:#FAF8F5"></iframe>'
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
<p class="subhead">Seat floors, per-resolution fees, and one flat subscription. A vendor without a public rate is left blank.</p>
<p><a class="button button-blue" href="#support-calc">Price the tickets</a> <a class="button button-ledger" href="/embeds/">Embeds</a></p>
</div>
</section>
<section class="scene scene-light">
<div class="article-shell wide">
<p class="affiliate-inline">The CustomGPT.ai button is a partner link. Intercom, Zendesk, Tidio, Ada, and Sierra buttons go to the official site. <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a>.</p>
<p><a class="button button-blue" href="/go/customgpt/" rel="sponsored nofollow noopener" data-partner-slug="customgpt">Partner link · CustomGPT.ai →</a> <a href="/tools/customgpt/">Read the CustomGPT.ai audit</a></p>
<script type="application/json" id="support-pricing">{pricing}</script>
{_form(False)}
<p><button type="button" id="support-share">Copy shareable receipt link</button></p>
<details class="cite-drawer">
<summary>Embed this calculator</summary>
<textarea readonly>{_esc(iframe)}</textarea>
</details>
<h2>Questions</h2>
<div class="faq-list">{faqs}</div>
<p>Catalog review: <a href="/tools/customgpt/">CustomGPT.ai</a>. Official pricing: <a href="https://www.intercom.com/pricing" rel="external noopener">Intercom</a>, <a href="https://www.zendesk.com/pricing/" rel="external noopener">Zendesk</a>, <a href="https://www.tidio.com/pricing/" rel="external noopener">Tidio</a>, <a href="https://www.ada.cx/" rel="external noopener">Ada</a>, <a href="https://sierra.ai/" rel="external noopener">Sierra</a>.</p>
{receipt_footer_html()}
</div>
</section>
</main>
<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/newsletter/">Newsletter</a><a href="/embeds/">Embeds</a></footer>
<script src="/js/customer-support-calculator.js"></script>
{_boot()}
</body>
</html>
"""
    dest = root / "compare" / "ai-customer-support-cost" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")
    return dest
