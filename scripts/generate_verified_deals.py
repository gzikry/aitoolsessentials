#!/usr/bin/env python3
"""Regenerate the Deals hub from verified pricing evidence.

Every tool whose official-pricing digest contains a live promo/discount gets a
deal card with its checked date, the promo detail, and links to review + official
pricing. Non-promo sections (free tiers, trials) are preserved as static content
already on the page; this generator owns the "Verified deals" section.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

MARK_S = "<!-- AIT VERIFIED DEALS START -->"
MARK_E = "<!-- AIT VERIFIED DEALS END -->"
DEALS_RE = re.compile(re.escape(MARK_S) + r".*?" + re.escape(MARK_E) + r"\n?", re.S)

PROMO_KEYWORDS = ["promo", "% off", "promotion", "discount", "first year", "free month", "introductory", "limited time"]

# Slugs with approved affiliate links get an affiliate CTA; all others link to review only.
AFFILIATE = {
    "elevenlabs": ("https://try.elevenlabs.io/xs6witq7izqe", "sponsored nofollow noopener"),
    "make": ("https://www.make.com/en/register?pc=aitoolsessentials", "sponsored nofollow noopener"),
}


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def generate(root: Path) -> int:
    tools = {t["slug"]: t for t in json.loads((root / "data/tools.json").read_text())}
    records = json.loads((root / "data/tool_sources.json").read_text())["tools"]
    checked = {r["slug"]: r for r in records}

    deals = []
    for slug, rec in checked.items():
        summary = rec.get("pricing_summary", "")
        low = summary.lower()
        if not any(k in low for k in PROMO_KEYWORDS):
            continue
        tool = tools.get(slug)
        if not tool:
            continue
        # Extract the most deal-relevant sentence(s)
        sents = [x.strip() for x in re.split(r"(?<=[.!?])\s+", summary) if any(k in x.lower() for k in PROMO_KEYWORDS)]
        detail = " ".join(sents[:2]) or summary[:220]
        date = rec.get("pricing_checked_date", "")
        affiliate = AFFILIATE.get(slug)
        if affiliate:
            cta = f'<a class="button button-blue small" href="{affiliate[0]}" target="_blank" rel="{affiliate[1]}">Claim at {tool["name"]} →</a>'
        else:
            cta = f'<a class="button button-dark small" href="/tools/{slug}/">Read review</a>'
        deals.append(
            f'<article class="directory-card"><div><span class="pill pill-promo">Promo live</span> '
            f'<h3><a href="/tools/{slug}/">{_esc(tool["name"])}</a></h3>'
            f'<p>{_esc(detail)}</p>'
            f'<p class="last-updated">Verified from official pricing page · checked {date}</p></div>'
            f'<div class="card-actions">{cta} <a class="text-link" href="/tools/{slug}/">Review</a></div></article>'
        )

    section = (
        f"{MARK_S}<section class=\"scene scene-light\"><div class=\"section-title\">"
        "<p class=\"kicker light\">Evidence-based</p><h2>Verified live deals</h2>"
        "<p>Auto-generated from our pricing verification runs — every deal below was found on the vendor's "
        "official pricing page with a checked date. Nothing scraped, nothing expired-on-purpose.</p></div>"
        f"<div class=\"directory-grid\">{''.join(deals)}</div>"
        '<p><a class="text-link" href="/pricing-watch/">See the full AI Pricing Watch →</a></p></section>'
        f"{MARK_E}\n"
    )

    path = root / "deals/index.html"
    html = path.read_text()
    original = html
    if MARK_S in html:
        html = DEALS_RE.sub(lambda _m: section, html)
    else:
        idx = html.find("</main>")
        if idx == -1:
            return 0
        html = html[:idx] + section + html[idx:]
    if html != original:
        path.write_text(html)
        print(f"Verified deals: {len(deals)} promos surfaced")
        return 1
    print(f"Verified deals: {len(deals)} promos surfaced (unchanged)")
    return 1


if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent)
