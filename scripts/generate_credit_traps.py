#!/usr/bin/env python3
"""Filterable ledger of verified credit-expiry, lock, reset, and annual traps."""
from __future__ import annotations

import html
import json
from pathlib import Path

from newsletter_hold import compliance_footer, subscribe_endpoint
from site_chrome import CANONICAL_HEADER

DOMAIN = "https://aitoolsessentials.com"
PATH = "/pricing-watch/credit-traps/"
TITLE = "The AI Credit Expiry, Rollover & Downgrade-Lock Tracker"
DESCRIPTION = (
    "Verified credit-expiry windows, rollover rules, cancellation locks, and "
    "annual-only prices from the checked tool pages. Slide monthly utilization "
    "from 25% to 100% to see the effective cost of a seat you do not finish. "
    "A rule the page does not state is labeled as unstated."
)

# kind: expiry90, lock, reset, annual, rollover, unstated, other
# Quotes are sentences already on the checked page or the dated price-change note.
TRAPS = [
    {
        "slug": "v0",
        "name": "v0",
        "checked": "2026-10-25",
        "kind": "expiry90",
        "rule": "Monthly credits expire after 65 days.",
    },
    {
        "slug": "v0",
        "name": "v0",
        "checked": "2026-10-25",
        "kind": "lock",
        "rule": "Purchased credits expire after one year and lock if the paid plan lapses.",
    },
    {
        "slug": "v0",
        "name": "v0",
        "checked": "2026-10-25",
        "kind": "annual",
        "rule": "Legacy Premium is $20/month and is closed to new signups.",
    },
    {
        "slug": "lovable",
        "name": "Lovable",
        "checked": "2026-10-25",
        "kind": "expiry90",
        "rule": "Monthly plan credits expire two months after issue.",
    },
    {
        "slug": "lovable",
        "name": "Lovable",
        "checked": "2026-10-25",
        "kind": "reset",
        "rule": "Daily grants do not roll over.",
    },
    {
        "slug": "elevenlabs",
        "name": "ElevenLabs",
        "checked": "2026-09-18",
        "kind": "rollover",
        "rule": "Paid-plan credits can roll over up to two months' worth while the subscription remains active.",
    },
    {
        "slug": "heygen",
        "name": "HeyGen",
        "checked": "2026-09-18",
        "kind": "unstated",
        "rule": "The checked pricing summary does not state a credit rollover or reset rule.",
    },
    {
        "slug": "synthesia",
        "name": "Synthesia",
        "checked": "2026-09-18",
        "kind": "unstated",
        "rule": "The checked pricing summary does not state a credit rollover or reset rule.",
    },
    {
        "slug": "descript",
        "name": "Descript",
        "checked": "2026-09-18",
        "kind": "unstated",
        "rule": "The checked pricing summary does not state a credit rollover or reset rule.",
    },
    {
        "slug": "zapier-ai",
        "name": "Zapier",
        "checked": "2026-09-18",
        "kind": "unstated",
        "rule": "The checked pricing summary does not state that tasks reset monthly or roll over.",
    },
    {
        "slug": "make",
        "name": "Make",
        "checked": "2026-10-01",
        "kind": "reset",
        "rule": "Credits normally expire at the end of the subscription term.",
    },
    {
        "slug": "n8n",
        "name": "n8n",
        "checked": "2026-10-01",
        "kind": "reset",
        "rule": "Assistant-credit balances refresh monthly and unused credits do not roll over.",
    },
    {
        "slug": "n8n",
        "name": "n8n",
        "checked": "2026-10-01",
        "kind": "other",
        "rule": "Free trials include 800 Assistant credits plus 100 AI credits that expire when the trial ends.",
    },
    {
        "slug": "n8n",
        "name": "n8n",
        "checked": "2026-10-01",
        "kind": "annual",
        "rule": "Starter, Pro, and Business prices in the checked summary are billed annually. The page advertises saving 17% on annual billing and does not print a month-to-month sticker. This row does not convert euros.",
    },
    {
        "slug": "canva-ai",
        "name": "Canva AI",
        "checked": "2026-10-01",
        "kind": "reset",
        "rule": "Allowances reset monthly.",
    },
    {
        "slug": "gamma",
        "name": "Gamma",
        "checked": "2026-10-01",
        "kind": "reset",
        "rule": "400 one-time signup credits that do not refill.",
    },
    {
        "slug": "runway",
        "name": "Runway",
        "checked": "2026-09-18",
        "kind": "reset",
        "also": ["longroll"],
        "rule": "Standard and Pro subscription credits do not roll over; purchased credits do not expire.",
    },
    {
        "slug": "runway",
        "name": "Runway",
        "checked": "2026-09-18",
        "kind": "rollover",
        "rule": "Max includes up to one month of credit rollover.",
    },
    {
        "slug": "midjourney",
        "name": "Midjourney",
        "checked": "2026-10-01",
        "kind": "reset",
        "rule": "Unused subscription Fast time does not roll over.",
    },
    {
        "slug": "udio",
        "name": "Udio",
        "checked": "2026-10-01",
        "kind": "reset",
        "rule": "Free includes 100 monthly credits and a 10-credit daily limit, with no rollovers.",
    },
    {
        "slug": "browse-ai",
        "name": "Browse.ai",
        "checked": "2026-09-18",
        "kind": "reset",
        "rule": "Unused credits reset at billing cycle end.",
    },
    {
        "slug": "imagesv2",
        "name": "ImagesV2",
        "checked": "2026-10-22",
        "kind": "reset",
        "also": ["longroll"],
        "rule": "Monthly subscription credits expire at the end of each cycle; yearly credits arrive as twelve 30-day blocks; pack credits never expire.",
    },
    {
        "slug": "words-into-music",
        "name": "Words Into Music",
        "checked": "2026-10-21",
        "kind": "reset",
        "also": ["longroll"],
        "rule": "Unused subscription credits expire at the next allowance boundary and do not roll over, while purchased pack credits do not expire.",
    },
    {
        "slug": "rapvideo-ai",
        "name": "RapVideo AI",
        "checked": "2026-10-27",
        "kind": "reset",
        "rule": "Monthly plans (credits reset monthly, unused expire).",
    },
    {
        "slug": "tarotai-chat",
        "name": "TAROTAI.CHAT",
        "checked": "2026-10-21",
        "kind": "reset",
        "rule": "Monthly subscriptions: $3.99 for 800 credits, $9.90 for 3,000 (no rollover, cancel anytime).",
    },
    {
        "slug": "htmlslides",
        "name": "HTMLSlides",
        "checked": "2026-09-18",
        "kind": "other",
        "rule": "Credits non-refundable, may expire. The checked page does not give a day window.",
    },
    {
        "slug": "retouchia",
        "name": "Retouchia",
        "checked": "2026-10-22",
        "kind": "other",
        "also": ["longroll"],
        "rule": "Paid credits are valid 365 days from purchase.",
    },
    {
        "slug": "leonardo-ai",
        "name": "Leonardo AI",
        "checked": "2026-08-25",
        "kind": "rollover",
        "rule": "Essential, Premium, and Ultimate each list a rollover-bank cap on Fast Tokens.",
    },
    {
        "slug": "bolt-new",
        "name": "Bolt.new",
        "checked": "2026-10-25",
        "kind": "rollover",
        "rule": "Pro includes 10 million tokens/month with rollover. The checked page does not publish a day-count.",
    },
    {
        "slug": "genjutsu-ai",
        "name": "Genjutsu AI",
        "checked": "2026-10-26",
        "kind": "reset",
        "also": ["longroll"],
        "rule": "One-time credits never expire while subscription credits expire each period.",
    },
    {
        "slug": "microsoft-copilot",
        "name": "Microsoft 365 Copilot",
        "checked": "2026-10-01",
        "kind": "annual",
        "rule": "Prices are USD, annual subscriptions that auto-renew. Copilot Business is a promotional $18/user/month, paid yearly, versus a $21 list price.",
    },
    {
        "slug": "cursor",
        "name": "Cursor",
        "checked": "2026-10-13",
        "kind": "annual",
        "rule": "The standalone Pro, Pro Plus and Teams tiers no longer appear on the page.",
    },
    {
        "slug": "windsurf",
        "name": "Windsurf",
        "checked": "2026-10-26",
        "kind": "annual",
        "rule": "March 2026 replaced prompt credits with a daily and weekly quota. An existing Pro subscriber at $15/mo keeps that price.",
    },
    {
        "slug": "replit-ai",
        "name": "Replit",
        "checked": "2026-10-25",
        "kind": "annual",
        "rule": "The free Starter tier from the 21 Aug check is off the public table.",
    },
    {
        "slug": "suno",
        "name": "Suno",
        "checked": "2026-10-01",
        "kind": "reset",
        "rule": "The review says unused credits expire each cycle. The cost score says subscription credits do not roll over and monthly downloads are capped.",
    },
    {
        "slug": "ideogram",
        "name": "Ideogram",
        "checked": "2026-10-01",
        "kind": "reset",
        "rule": "Unused subscription credits expire; only paid top-ups carry over. Priority credits do not roll over between billing cycles. Plus is $15/month billed annually.",
    },
    {
        "slug": "synthesia",
        "name": "Synthesia",
        "checked": "2026-09-18",
        "kind": "other",
        "rule": "Starter lists 1,200 credits/month, or 14,500 credits/year when billed yearly. Creator lists 3,600 credits/month, or 44,000 credits/year. These are credits, not video minutes. The checked summary does not state a rollover rule.",
    },
    {
        "slug": "customgpt",
        "name": "CustomGPT.ai",
        "checked": "2026-10-27",
        "kind": "meter",
        "rule": "Standard is $99 per month with 1,000 queries. Premium is $499 per month with 5,000 queries. Queries are counted on attempted inbound tickets, including ones that escalate. There is no per-resolution fee.",
    },
    {
        "slug": "intercom-fin",
        "name": "Intercom Fin",
        "checked": "2026-10-28",
        "kind": "meter",
        "meter": True,
        "tool_href": "/compare/ai-customer-support-cost/",
        "rule": "Fin outcomes are $0.99. A return to the same conversation is not charged. Standalone Fin has no seat fee and a 50-outcome monthly minimum.",
    },
    {
        "slug": "zendesk-ai",
        "name": "Zendesk AI",
        "checked": "2026-10-28",
        "kind": "meter",
        "meter": True,
        "tool_href": "/compare/ai-customer-support-cost/",
        "rule": "Extra resolutions are $1.50 committed or $2.00 pay-as-you-go. Suite Team is $55 per agent per month billed annually or $69 monthly.",
    },
    {
        "slug": "umevo",
        "name": "UMEVO",
        "checked": "2026-10-27",
        "kind": "unstated",
        "rule": "Pay-as-you-go minute packs are published. Unused free minutes do not carry over. The checked pages do not state a 2-year pack validity window.",
    },
]

CALCS = {
    "v0": "/compare/ai-app-builders/",
    "bolt-new": "/compare/ai-app-builders/",
    "lovable": "/compare/ai-app-builders/",
    "replit-ai": "/compare/ai-app-builders/",
    "cursor": "/compare/ai-coding-assistants/",
    "windsurf": "/compare/ai-coding-assistants/",
    "elevenlabs": "/compare/ai-video-avatar-cost/",
    "descript": "/compare/ai-video-avatar-cost/",
    "heygen": "/compare/ai-video-avatar-cost/",
    "synthesia": "/compare/ai-video-avatar-cost/",
    "make": "/compare/automation-task-calculator/",
    "zapier-ai": "/compare/automation-task-calculator/",
    "n8n": "/compare/automation-task-calculator/",
    "gamma": "/compare/ai-presentation-cost/",
    "canva-ai": "/compare/ai-presentation-cost/",
    "htmlslides": "/compare/ai-presentation-cost/",
    "microsoft-copilot": "/compare/ai-presentation-cost/",
    "customgpt": "/compare/ai-customer-support-cost/",
    "intercom-fin": "/compare/ai-customer-support-cost/",
    "zendesk-ai": "/compare/ai-customer-support-cost/",
}

# Published sticker used only for the utilization math. Keyed by slug and kind
# so a second row about the same product does not inherit the wrong seat.
SEAT_CENTS = {
    ("v0", "expiry90"): 3000,
    ("lovable", "expiry90"): 2500,
    ("elevenlabs", "rollover"): 2200,
    ("runway", "reset"): 1500,
    ("runway", "rollover"): 9500,
    ("heygen", "unstated"): 2900,
    ("descript", "unstated"): 2400,
    ("midjourney", "reset"): 1000,
    ("suno", "reset"): 800,
    ("ideogram", "reset"): 1500,
    ("synthesia", "other"): 2900,
    ("customgpt", "meter"): 9900,
}

SEAT_NOTE = {
    ("v0", "expiry90"): "Plus list $30/user/mo",
    ("lovable", "expiry90"): "Pro list $25/mo",
    ("elevenlabs", "rollover"): "Creator list $22/mo",
    ("runway", "reset"): "Standard list $15/mo",
    ("runway", "rollover"): "Max list $95/mo",
    ("heygen", "unstated"): "Creator list $29/mo",
    ("descript", "unstated"): "Hobbyist list $24/mo",
    ("midjourney", "reset"): "Basic list $10/mo",
    ("suno", "reset"): "Pro list $8/mo",
    ("ideogram", "reset"): "Plus $15/mo billed annually",
    ("synthesia", "other"): "Starter list $29/mo",
    ("customgpt", "meter"): "Standard list $99/mo",
}

KIND_LABEL = {
    "expiry90": "60–65 Day Expiry",
    "lock": "Downgrade / Cancel Credit Wipe",
    "reset": "Monthly Reset / No Rollover",
    "annual": "Annual-only / tier sunset",
    "rollover": "Rollover stated",
    "unstated": "Not stated",
    "other": "Stated, no day window",
    "meter": "Attempted vs. Resolved Meter",
    "longroll": "2-Year / Long Rollover",
}


def _esc(value: str) -> str:
    return html.escape(value, quote=True)


def _links(root: Path) -> dict:
    path = root / "data" / "affiliate_links.json"
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("links") or {}


def _rel(entry: dict | None) -> str:
    if entry and entry.get("partner"):
        return "sponsored nofollow noopener"
    return "external noopener"


def _signup(root: Path) -> str:
    cfg_path = root / "data" / "newsletter.json"
    endpoint = ""
    if cfg_path.is_file():
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        endpoint = subscribe_endpoint(cfg.get("subscribe_endpoint"))
    footer = "<p>" + compliance_footer() + "</p>"
    if not endpoint:
        return '<p><a href="/subscribe/">Get the free email</a></p>' + footer
    return (
        f'<form class="price-alert-form" method="post" action="{_esc(endpoint)}">'
        '<input type="hidden" name="tool" value="credit-traps">'
        '<input type="hidden" name="source_page" value="pricing-watch/credit-traps/index.html">'
        '<p><label>Email <input type="email" name="email" autocomplete="email" required></label></p>'
        '<p class="subscribe-honeypot"><label>Company website '
        '<input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></p>'
        '<p><button class="button button-blue" type="submit">Get the free email</button></p>'
        "<p>One email a week. We send a confirm link first. The list stays empty until you click it.</p>"
        "</form>"
        + footer
    )


def _rows(root: Path, keys: set[tuple[str, str]] | None = None, compact: bool = False) -> str:
    links = _links(root)
    rendered = []
    for trap in TRAPS:
        slug = trap["slug"]
        kind = trap["kind"]
        if keys is not None and (slug, kind) not in keys:
            continue
        entry = links.get(slug) or {}
        href = entry.get("public_href") or ""
        tool = trap.get("tool_href") or f"/tools/{slug}/"
        if not trap.get("tool_href") and (slug == "windsurf" or not (root / "tools" / slug / "index.html").is_file()):
            tool = href or "/pricing-watch/"
        calc = CALCS.get(slug, "")
        calc_cell = f'<a href="{_esc(calc)}">Calculator</a>' if calc else "—"
        go_cell = "—"
        if href:
            go_cell = f'<a href="{_esc(href)}" rel="{_esc(_rel(entry))}">Open</a>'
        kinds = [kind] + list(trap.get("also") or [])
        labels = " ".join(KIND_LABEL[item] for item in kinds)
        search = " ".join((trap["name"], slug, trap["rule"], labels)).casefold()
        cents = trap.get("monthly_cents", SEAT_CENTS.get((slug, kind)))
        note = trap.get("price_note") or SEAT_NOTE.get((slug, kind)) or ""
        attrs = (
            f' data-slug="{_esc(slug)}"'
            f' data-kinds="{_esc(" ".join(kinds))}"'
            f' data-search="{_esc(search)}"'
        )
        if cents:
            attrs += f' data-monthly-cents="{int(cents)}"'
        if trap.get("meter") or kind == "meter":
            attrs += ' data-meter="1"'
        if note:
            attrs += f' data-price-note="{_esc(note)}"'
        pills = "".join(
            f'<span class="trap-pill trap-pill-{_esc(item)}">{_esc(KIND_LABEL[item])}</span>'
            for item in kinds
        )
        row_html = (
            "<tr"
            f"{attrs}>"
            f'<th><a href="{_esc(tool)}">{_esc(trap["name"])}</a></th>'
            f'<td>{_esc(trap["checked"])}</td>'
            f"<td>{pills}</td>"
            f'<td>{_esc(trap["rule"])}</td>'
            f'<td class="trap-effective">—</td>'
        )
        if not compact:
            row_html += f"<td>{calc_cell}</td>"
        row_html += f"<td>{go_cell}</td></tr>"
        rendered.append(row_html)
    return "".join(rendered)


TRAP_SCRIPT = r"""
(function () {
  var pills = document.querySelectorAll("[data-pill]");
  var rows = Array.prototype.slice.call(document.querySelectorAll("#trap-rows tr"));
  var empty = document.getElementById("trap-empty");
  var util = document.getElementById("trap-util");
  var utilOut = document.getElementById("trap-util-out");
  var active = "all";
  function money(cents) {
    return "$" + (cents / 100).toFixed(2);
  }
  function paintCost() {
    var pct = util ? Math.max(25, Math.min(100, parseInt(util.value, 10) || 100)) : 100;
    if (utilOut) utilOut.textContent = pct + "%";
    rows.forEach(function (row) {
      var cell = row.querySelector(".trap-effective");
      if (!cell) return;
      var raw = row.getAttribute("data-monthly-cents");
      var note = row.getAttribute("data-price-note") || "";
      if (!raw) {
        cell.textContent = row.getAttribute("data-meter") === "1" ? "Metered · not divided" : "No flat seat on this row";
        return;
      }
      var monthly = parseInt(raw, 10);
      var effective = Math.round(monthly * 100 / pct);
      var waste = monthly - Math.round(monthly * pct / 100);
      cell.textContent = money(effective) + " / used seat · waste " + money(waste) + "/mo";
      if (note) cell.setAttribute("title", note);
    });
  }
  function apply() {
    var qEl = document.getElementById("trap-q");
    var q = qEl ? qEl.value.trim().toLowerCase() : "";
    var picked = Array.prototype.map.call(
      document.querySelectorAll("#trap-tools input:checked"),
      function (box) { return box.value; }
    );
    var shown = 0;
    rows.forEach(function (row) {
      var kinds = row.getAttribute("data-kinds") || "";
      var blob = row.getAttribute("data-search") || "";
      var slug = row.getAttribute("data-slug") || "";
      var pillOk = active === "all" || kinds.split(" ").indexOf(active) !== -1;
      var textOk = !q || blob.indexOf(q) !== -1;
      var pickOk = !picked.length || picked.indexOf(slug) !== -1;
      var show = pillOk && textOk && pickOk;
      row.hidden = !show;
      row.classList.toggle("trap-hit", !!(show && (q || picked.length)));
      if (show) shown += 1;
    });
    if (empty) empty.hidden = shown !== 0;
    paintCost();
  }
  pills.forEach(function (pill) {
    pill.addEventListener("click", function () {
      active = pill.getAttribute("data-pill");
      pills.forEach(function (other) { other.classList.toggle("is-on", other === pill); });
      apply();
    });
  });
  var form = document.getElementById("trap-check");
  if (form) {
    form.addEventListener("input", apply);
    form.addEventListener("change", apply);
  }
  if (util) {
    util.addEventListener("input", paintCost);
    util.addEventListener("change", paintCost);
  }
  apply();
})();
"""


EMBED_KEYS = {
    ("v0", "expiry90"),
    ("v0", "lock"),
    ("lovable", "expiry90"),
    ("elevenlabs", "rollover"),
    ("suno", "reset"),
    ("ideogram", "reset"),
    ("runway", "reset"),
    ("heygen", "unstated"),
    ("synthesia", "other"),
    ("customgpt", "meter"),
    ("intercom-fin", "meter"),
    ("zendesk-ai", "meter"),
    ("umevo", "unstated"),
    ("retouchia", "other"),
}


def _picker() -> str:
    seen = []
    boxes = []
    for trap in TRAPS:
        if trap["slug"] in seen:
            continue
        seen.append(trap["slug"])
        boxes.append(
            "<label>"
            f'<input type="checkbox" value="{_esc(trap["slug"])}"> {_esc(trap["name"])}'
            "</label>"
        )
    return "".join(boxes)


def generate(root: Path) -> Path:
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
</head>
<body>
{CANONICAL_HEADER}
<main>
<section class="scene scene-dark ledger-mast">
<div style="max-width:880px;margin:0 auto;padding:72px 28px 36px">
<p class="kicker light">Pricing watch · checked pages only</p>
<h1>{_esc(TITLE)}</h1>
<p class="subhead">Expiry windows, locks, resets, and annual-only prices that the checked page actually states. A positive rollover, or a page that is silent, stays out of the trap filters. The long-rollover filter is the counter-example: validity the checked page actually states.</p>
<p><a class="button button-ledger" href="/pricing-watch/">Pricing Watch</a> <a class="button button-ledger" href="/compare/ai-presentation-cost/">Deck cost</a> <a class="button button-ledger" href="/compare/ai-customer-support-cost/">Support fees</a> <a class="button button-ledger" href="/embed/credit-traps.html">Embed</a></p>
</div>
</section>
<section class="scene scene-light">
<div class="article-shell wide">
<div class="trap-filters" role="group" aria-label="Trap filters">
<button type="button" class="is-on" data-pill="all">All</button>
<button type="button" data-pill="reset">Monthly Reset / No Rollover</button>
<button type="button" data-pill="expiry90">60–65 Day Expiry</button>
<button type="button" data-pill="lock">Downgrade / Cancel Credit Wipe</button>
<button type="button" data-pill="meter">Attempted vs. Resolved Meter</button>
<button type="button" data-pill="longroll">2-Year / Long Rollover</button>
<button type="button" data-pill="annual">Annual-only / tier sunset</button>
</div>
<form id="waste-calc" class="ledger-sheet" data-testid="waste-calc">
<h2>Effective cost after waste</h2>
<p><label>Monthly utilization
<input id="trap-util" type="range" min="25" max="100" value="50" step="5">
</label> <output id="trap-util-out" for="trap-util">50%</output></p>
<p>Effective real cost per used seat equals the published sticker divided by utilization. At 25% you still pay the sticker, so each used seat-equivalent costs four times list. A per-resolution meter with no flat seat is not divided.</p>
</form>
<form id="trap-check" class="ledger-sheet">
<h2>Check if my tools have credit traps</h2>
<p><label>Search <input id="trap-q" type="search" placeholder="v0, rollover, 65 days"></label></p>
<div id="trap-tools" class="trap-tools">{_picker()}</div>
</form>
<div class="table-wrap">
<table class="ledger-table">
<thead><tr><th>Tool</th><th>Checked</th><th>Kind</th><th>What the page says</th><th>Effective cost</th><th>Calculator</th><th>Hop</th></tr></thead>
<tbody id="trap-rows">{_rows(root)}</tbody>
</table>
</div>
<p id="trap-empty" hidden>No row matches that filter.</p>
<aside class="price-alert ledger-sheet">
<p>Track price and credit-rule changes. One email when a checked rule on this list moves.</p>
{_signup(root)}
<p><a href="/subscribe/">Subscribe page</a></p>
</aside>
<p>Make’s checked line is the end of the subscription term, not a monthly reset. Zapier, HeyGen, Synthesia, and Descript do not state a rollover rule on the checked page, so this ledger does not invent one. n8n prices stay in euros. ElevenLabs states rollover only while the subscription remains active. Lovable states that monthly credits expire two months after issue. A one-month annual window and a cancel wipe are not on that page. UMEVO publishes pay-as-you-go packs and says unused free minutes do not carry over. It does not state a 2-year validity window, so it stays out of the long-rollover filter. Synthesia’s 1,200 and 3,600 figures are monthly credits. CustomGPT Premium on the checked pricing file is $499 per month.</p>
</div>
</section>
</main>
<footer class="footer">
<span>© 2026 AIToolsEssentials</span>
<a href="/pricing-watch/">Pricing Watch</a>
<a href="/newsletter/">Newsletter</a>
<a href="/legal/privacy.html">Privacy</a>
<a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
</footer>
<script>
{TRAP_SCRIPT}
</script>
<script src="/js/site.js" defer></script>
</body>
</html>
"""
    dest = root / "pricing-watch" / "credit-traps" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")
    return dest


def embed_page(root: Path) -> str:
    count = len(json.loads((root / "data" / "tools.json").read_text(encoding="utf-8")))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{_esc(DESCRIPTION)}">
<title>{_esc(TITLE)} embed | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/embed/credit-traps.html">
<style>
html,body{{margin:0;background:#FAF8F5;color:#111315}}
body{{font:15px/1.45 Newsreader,Georgia,serif;padding:12px 14px 56px}}
h1{{font-size:22px;line-height:1.15;margin:0 0 8px}}
p,td,th{{font-size:13px}}
button,label,output,.trap-effective{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:12px}}
.trap-filters{{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}}
.trap-filters button{{color:#111315;background:#fff;border:1px solid #111315;border-radius:999px;padding:4px 8px;cursor:pointer}}
.trap-filters button.is-on{{color:#FAF8F5;background:#111315}}
input[type=range]{{width:140px}}
table{{width:100%;border-collapse:collapse}}
th,td{{border-top:1px solid #D8D2C5;padding:6px 4px;text-align:left;vertical-align:top}}
a{{color:#111315}}
.trap-pill{{display:inline-block;margin:0 4px 4px 0;padding:1px 6px;border:1px solid #D8D2C5;border-radius:999px}}
.embed-bar{{position:sticky;bottom:0;margin:8px -14px 0;padding:8px 14px;background:#111315;color:#FAF8F5;font:11px/1.35 "IBM Plex Mono",ui-monospace,monospace}}
.embed-bar a{{color:#FAF8F5}}
</style>
</head>
<body>
<main>
<h1>{_esc(TITLE)}</h1>
<div class="trap-filters" role="group" aria-label="Trap filters">
<button type="button" class="is-on" data-pill="all">All</button>
<button type="button" data-pill="reset">Monthly Reset / No Rollover</button>
<button type="button" data-pill="expiry90">60–65 Day Expiry</button>
<button type="button" data-pill="lock">Downgrade / Cancel Credit Wipe</button>
<button type="button" data-pill="meter">Attempted vs. Resolved Meter</button>
<button type="button" data-pill="longroll">2-Year / Long Rollover</button>
</div>
<form id="waste-calc">
<p><label>Monthly utilization <input id="trap-util" type="range" min="25" max="100" value="50" step="5"></label> <output id="trap-util-out" for="trap-util">50%</output></p>
</form>
<div class="table-wrap">
<table>
<thead><tr><th>Tool</th><th>Checked</th><th>Kind</th><th>What the page says</th><th>Effective cost</th><th>Hop</th></tr></thead>
<tbody id="trap-rows">{_rows(root, EMBED_KEYS, compact=True)}</tbody>
</table>
</div>
<p id="trap-empty" hidden>No row matches that filter.</p>
<footer class="embed-bar">Source: AI Tools Essentials Audited Price Ledger → <a href="{PATH}">Full {count}-tool breakdown</a> · <a href="{PATH}">Credit traps</a> · <a href="/newsletter/">Newsletter</a> · <a href="/embeds/">Embeds</a></footer>
</main>
<script>
{TRAP_SCRIPT}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parents[1]))
