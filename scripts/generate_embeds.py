#!/usr/bin/env python3
"""Iframe calculators and the public embeds hub.

The widgets call the same client-side pricing functions as the full
calculators. Partner buttons keep the hop rel values those functions already
publish. The page count in the attribution line is the live catalog size.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"

EMBEDS = (
    {
        "slug": "ai-bill-slasher",
        "title": "30-second AI bill",
        "canonical_calc": "/",
        "calc_label": "Homepage bill",
        "script": "/js/homepage-bill-slasher.js",
    },
    {
        "slug": "ai-coding-assistants",
        "title": "Coding seat price",
        "canonical_calc": "/compare/ai-coding-assistants/",
        "calc_label": "Coding calculator",
        "script": "/js/coding-assistant-calculator.js",
    },
    {
        "slug": "ai-video-avatar-cost",
        "title": "Voice and video minutes",
        "canonical_calc": "/compare/ai-video-avatar-cost/",
        "calc_label": "Voice and video calculator",
        "script": "/js/voice-video-calculator.js",
    },
    {
        "slug": "automation-task-calculator",
        "title": "Automation task cost",
        "canonical_calc": "/compare/automation-task-calculator/",
        "calc_label": "Automation calculator",
        "script": "/js/automation-task-calculator.js",
    },
    {
        "slug": "customer-support-cost",
        "title": "Support resolution fee",
        "canonical_calc": "/compare/ai-customer-support-cost/",
        "calc_label": "Support calculator",
        "script": "/js/customer-support-calculator.js",
        "href": "/embed/customer-support-cost.html",
    },
    {
        "slug": "credit-traps",
        "title": "Credit expiry ledger",
        "canonical_calc": "/pricing-watch/credit-traps/",
        "calc_label": "Credit traps",
        "href": "/embed/credit-traps.html",
    },
)

STYLE = """
<style>
html,body{margin:0;background:#FAF8F5;color:#111315}
body{font:15px/1.4 Newsreader,Georgia,serif;padding:12px 14px 0}
h1{font-size:22px;line-height:1.15;margin:0 0 8px}
form,label{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:12px}
.seats{display:grid;grid-template-columns:1fr 1fr;gap:4px 12px;margin:0 0 8px}
label{display:flex;gap:6px;align-items:center}
input,select{font:inherit;border:1px solid #111315;background:#fff;color:#111315}
#result{border-top:1px solid #D8D2C5;padding-top:8px;min-height:120px}
#result p{margin:4px 0}
#result a{color:#111315}
.embed-bar{position:sticky;bottom:0;margin:8px -14px 0;padding:8px 14px;background:#111315;color:#FAF8F5;font:11px/1.35 "IBM Plex Mono",ui-monospace,monospace}
.embed-bar a{color:#FAF8F5}
</style>
"""

BILL_SEATS = (
    ("chatgpt", "ChatGPT Plus $20"),
    ("claude", "Claude Pro $20"),
    ("cursor", "Cursor Pro $20"),
    ("copilot", "GitHub Copilot $10"),
    ("windsurf", "Windsurf $15"),
    ("elevenlabs", "ElevenLabs $22"),
    ("descript", "Descript $24"),
    ("midjourney", "Midjourney $10"),
)


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def _bar(count: int, calc_href: str, calc_label: str, partners: str) -> str:
    return (
        f'<footer class="embed-bar">Source: AI Tools Essentials Audited Price Ledger → '
        f'<a href="{esc(calc_href)}">Full {count}-tool breakdown</a>'
        f' · <a href="{esc(calc_href)}">{esc(calc_label)}</a>'
        f'{partners}'
        f' · <a href="/newsletter/">Newsletter</a>'
        f' · <a href="/embeds/">Embeds</a></footer>'
    )


def _page(title: str, slug: str, body: str, script: str, extra: str) -> str:
    path = f"/embed/{slug}/"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{esc(title)} embed from the AI Tools Essentials audited price ledger.">
<title>{esc(title)} embed | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}{path}">
{STYLE}
</head>
<body>
<main>
<h1>{esc(title)}</h1>
{body}
</main>
<script src="{esc(script)}"></script>
<script>
{extra}
</script>
</body>
</html>
'''


def _bill(count: int) -> str:
    boxes = "".join(
        f'<label><input type="checkbox" name="seat" value="{esc(value)}"> {esc(label)}</label>'
        for value, label in BILL_SEATS
    )
    body = f'''<form id="embed-bill"><div class="seats">{boxes}</div></form>
<div id="result" aria-live="polite"></div>
{_bar(count, "/", "Homepage bill", "")}'''
    extra = r'''
var form = document.getElementById("embed-bill");
var out = document.getElementById("result");
function paint() {
  var ids = [];
  form.querySelectorAll("input:checked").forEach(function (box) { ids.push(box.value); });
  var result = window.BillSlasher.quote(ids);
  var keep = result.keep.map(function (seat) {
    var rel = seat.partner ? "sponsored nofollow noopener" : "external noopener";
    return "<p>Keep " + seat.name + " · $" + seat.price + "/mo · <a href=\"/go/" + seat.slug + "/\" rel=\"" + rel + "\">Open</a></p>";
  }).join("");
  var cut = result.cut.map(function (seat) {
    return "<p>Cut " + seat.name + " · overlap $" + (seat.price * 12) + "/yr</p>";
  }).join("");
  out.innerHTML = "<p><strong>$" + result.monthly + "/mo</strong> · overlap waste $" + result.waste + "/yr</p>" + keep + cut;
}
form.addEventListener("change", paint);
paint();
'''
    return _page("30-second AI bill", "ai-bill-slasher", body, "/js/homepage-bill-slasher.js", extra)


def _coding(count: int) -> str:
    body = f'''<form id="embed-coding" class="seats">
<label>Seats <input id="seats" type="number" min="1" max="50" value="5"></label>
<label>Prompts / day <input id="prompts" type="number" min="1" max="200" value="20"></label>
<label><input id="frontier" type="checkbox"> Frontier models</label>
<label><input id="annual" type="checkbox"> Annual where published</label>
</form>
<div id="result" aria-live="polite"></div>
{_bar(count, "/compare/ai-coding-assistants/", "Coding calculator", "")}'''
    extra = r'''
var form = document.getElementById("embed-coding");
var out = document.getElementById("result");
var hops = { cursor: "cursor", claude: "claude", copilot: "github-copilot", windsurf: "windsurf" };
function paint() {
  var result = window.CodingAssistantCalc.quote({
    seats: document.getElementById("seats").value,
    prompts: document.getElementById("prompts").value,
    frontier: document.getElementById("frontier").checked,
    annual: document.getElementById("annual").checked
  });
  out.innerHTML = result.tools.map(function (tool) {
    return "<p>" + tool.verdict + " · " + tool.name + " " + tool.tier + " · " +
      window.CodingAssistantCalc.money(tool.totalMonthlyCents) + "/mo · " +
      "<a href=\"/go/" + hops[tool.id] + "/\" rel=\"external noopener\">Open</a></p>";
  }).join("");
}
form.addEventListener("input", paint);
form.addEventListener("change", paint);
paint();
'''
    return _page("Coding seat price", "ai-coding-assistants", body, "/js/coding-assistant-calculator.js", extra)


def _voice(count: int) -> str:
    body = f'''<form id="embed-voice" class="seats">
<label>Minutes <input id="minutes" type="number" min="0" max="6000" value="60"></label>
<label>Gen-4 seconds <input id="seconds" type="number" min="0" max="3600" value="10"></label>
<label>Retakes <input id="retake" type="number" min="1" max="5" value="1"></label>
<label><input id="clone" type="checkbox"> Private mode</label>
</form>
<div id="result" aria-live="polite"></div>
{_bar(count, "/compare/ai-video-avatar-cost/", "Voice and video calculator", "")}'''
    extra = r'''
var form = document.getElementById("embed-voice");
var out = document.getElementById("result");
function paint() {
  var result = window.VoiceVideoCalc.priceVoice({
    minutes: document.getElementById("minutes").value,
    seconds: document.getElementById("seconds").value,
    retake: document.getElementById("retake").value,
    clone: document.getElementById("clone").checked
  });
  out.innerHTML = result.rows.map(function (row) {
    var dollars = row.monthlyCents == null ? "unconverted" : window.VoiceVideoCalc.money(row.monthlyCents) + "/mo";
    return "<p>" + row.verdict + " · " + row.name + " " + row.tier + " · " + dollars +
      " · <a href=\"" + row.href + "\" rel=\"" + row.rel + "\">Open</a></p>";
  }).join("");
}
form.addEventListener("input", paint);
form.addEventListener("change", paint);
paint();
'''
    return _page("Voice and video minutes", "ai-video-avatar-cost", body, "/js/voice-video-calculator.js", extra)


def _auto(count: int) -> str:
    body = f'''<form id="embed-auto" class="seats">
<label>Workflows <input id="workflows" type="number" min="1" max="500" value="3"></label>
<label>Steps <input id="steps" type="number" min="1" max="100" value="5"></label>
<label>Runs / day <input id="runs" type="number" min="0" max="10000" value="4"></label>
<label>Webhook % <input id="webhook" type="number" min="0" max="100" value="100"></label>
</form>
<div id="result" aria-live="polite"></div>
{_bar(count, "/compare/automation-task-calculator/", "Automation calculator", "")}'''
    extra = r'''
var form = document.getElementById("embed-auto");
var out = document.getElementById("result");
function paint() {
  var result = window.AutomationTaskCalc.priceAutomation({
    workflows: document.getElementById("workflows").value,
    steps: document.getElementById("steps").value,
    runsPerDay: document.getElementById("runs").value,
    webhookPercent: document.getElementById("webhook").value
  });
  out.innerHTML = result.rows.map(function (row) {
    var dollars = window.AutomationTaskCalc.money(row.monthlyCents, row.currency);
    return "<p>" + row.verdict + " · " + row.name + " " + row.tier + " · " + dollars +
      " · <a href=\"" + row.href + "\" rel=\"" + row.rel + "\">Open</a></p>";
  }).join("");
}
form.addEventListener("input", paint);
form.addEventListener("change", paint);
paint();
'''
    return _page("Automation task cost", "automation-task-calculator", body, "/js/automation-task-calculator.js", extra)


def _hub(root: Path, tools: list[dict], count: int) -> str:
    previews = []
    snippets = []
    for item in EMBEDS:
        src = item.get("href") or f"/embed/{item['slug']}/"
        iframe = f'<iframe src="{DOMAIN}{src}" title="{item["title"]}" width="100%" height="480" style="border:1px solid #111315;background:#FAF8F5"></iframe>'
        previews.append(
            f'<article class="content-hub-card"><h2>{esc(item["title"])}</h2>'
            f'<iframe src="{src}" title="{esc(item["title"])}" width="100%" height="480" style="border:1px solid #111315;background:#FAF8F5"></iframe>'
            f'<textarea readonly data-cite-box>{esc(iframe)}</textarea>'
            f'<button type="button" data-cite-copy>Copy iframe</button></article>'
        )
        snippets.append(iframe)
    options = "".join(
        f'<option value="{esc(tool["slug"])}">{esc(tool.get("name") or tool["slug"])}</option>'
        for tool in sorted(tools, key=lambda row: str(row.get("name") or "").lower())
    )
    copy_script = r'''
<script>
function fillBadge() {
  var slug = document.getElementById("badge-tool").value;
  var name = document.getElementById("badge-tool").selectedOptions[0].textContent;
  var page = "https://aitoolsessentials.com/tools/" + slug + "/?utm_source=badge_embed";
  var src = "https://aitoolsessentials.com/badges/" + slug + ".svg";
  var alt = "AUDITED BY AI TOOLS ESSENTIALS — " + name;
  document.getElementById("badge-preview").src = "/badges/" + slug + ".svg";
  document.getElementById("badge-preview").alt = alt;
  document.getElementById("badge-html").value = '<a href="' + page + '"><img alt="' + alt + '" src="' + src + '" width="360" height="108"></a>';
  document.getElementById("badge-md").value = "[![" + alt + "](" + src + ")](" + page + ")";
}
document.getElementById("badge-tool").addEventListener("change", fillBadge);
fillBadge();
document.querySelectorAll("[data-cite-copy]").forEach(function (button) {
  button.addEventListener("click", function () {
    var prev = button.previousElementSibling;
    var box = prev && prev.tagName === "TEXTAREA" ? prev : (prev ? prev.querySelector("textarea") : null);
    if (!box) return;
    var done = function () { button.textContent = "Copied"; };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(box.value).then(done);
    else { box.select(); document.execCommand("copy"); done(); }
  });
});
</script>
'''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Free embeddable AI cost calculators and audited pricing badges from AI Tools Essentials.">
<title>Free embeddable AI cost calculators and audited badges | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/embeds/">
<link rel="stylesheet" href="/css/styles.css">
</head>
<body>
<main>
<section class="scene scene-light">
<div class="article-shell wide">
<p class="kicker">Embeds</p>
<h1>Free embeddable AI cost calculators and audited badges</h1>
<p>{len(EMBEDS)} calculators and {count} tool badges. Each iframe is 480 pixels tall. The badge links back to the review. Partner buttons inside a widget use the same hop as the full calculator.</p>
<h2>Calculators</h2>
<div class="content-hub-grid">{''.join(previews)}</div>
<h2>Audited badges</h2>
<label>Tool <select id="badge-tool">{options}</select></label>
<p><img id="badge-preview" alt="" src="/badges/audited.svg" width="360" height="108"></p>
<label>HTML <textarea id="badge-html" readonly data-cite-box></textarea></label>
<button type="button" data-cite-copy>Copy HTML</button>
<label>Markdown <textarea id="badge-md" readonly data-cite-box></textarea></label>
<button type="button" data-cite-copy>Copy Markdown</button>
<p><a href="/badges/">Badge rules</a> · <a href="/legal/affiliate-disclosure.html">Affiliate disclosure</a></p>
</div>
</section>
</main>
<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/newsletter/">Newsletter</a><a href="/embeds/">Embeds</a><a href="/badges/">Badges</a></footer>
{copy_script}
</body>
</html>
'''


def generate(root: Path, tools: list[dict] | None = None) -> int:
    tools = tools or json.loads((root / "data" / "tools.json").read_text(encoding="utf-8"))
    count = len(tools)
    pages = {
        "ai-bill-slasher": _bill(count),
        "ai-coding-assistants": _coding(count),
        "ai-video-avatar-cost": _voice(count),
        "automation-task-calculator": _auto(count),
    }
    for slug, html_page in pages.items():
        dest = root / "embed" / slug / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html_page, encoding="utf-8")
    from generate_customer_support_hub import embed_page
    support = root / "embed" / "customer-support-cost.html"
    support.write_text(embed_page(root), encoding="utf-8")
    from generate_credit_traps import embed_page as credit_embed_page
    credit = root / "embed" / "credit-traps.html"
    credit.write_text(credit_embed_page(root), encoding="utf-8")
    hub = root / "embeds" / "index.html"
    hub.parent.mkdir(parents=True, exist_ok=True)
    hub.write_text(_hub(root, tools, count), encoding="utf-8")
    return len(pages) + 3
