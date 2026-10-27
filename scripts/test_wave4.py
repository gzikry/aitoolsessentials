#!/usr/bin/env python3
"""Wave 4: deck-cost calculator, credit-trap ledger, newsletter archive links."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NODE = r"""
const calc = require("./js/presentation-calculator.js");
const errors = [];
const check = (label, cond) => { if (!cond) errors.push(label); };
const by = (result, slug) => result.rows.find((row) => row.slug === slug);

const base = calc.priceDeck({ seats: 1, decks: 4, brand: false, watermark: false, annual: true });
const other = calc.priceDeck({ seats: 1, decks: 40, brand: false, watermark: false, annual: true });
["gamma", "canva-ai", "htmlslides", "microsoft-copilot"].forEach((slug) => {
  check(slug + " ignores decks", by(base, slug).monthlyCents === by(other, slug).monthlyCents);
});
check("default gamma free", by(base, "gamma").monthlyCents === 0 && by(base, "gamma").verdict === "Keep");
check("default gamma sponsored", by(base, "gamma").rel === "sponsored nofollow noopener");
check("default canva free keep", by(base, "canva-ai").monthlyCents === 0 && by(base, "canva-ai").verdict === "Keep");
check("default slides free keep", by(base, "htmlslides").monthlyCents === 0 && by(base, "htmlslides").verdict === "Keep");
check("default microsoft cut", by(base, "microsoft-copilot").monthlyCents === 2100 && by(base, "microsoft-copilot").verdict === "Cut");
check("microsoft external", by(base, "microsoft-copilot").rel === "external noopener");
check("canva external", by(base, "canva-ai").rel === "external noopener");
check("no beautiful row", !base.rows.some((row) => /beautiful/i.test(row.slug + row.name)));
check("default gap", base.savingsAnnualCents === 2100 * 12);

const seats = calc.priceDeck({ seats: 5, decks: 8, brand: false, watermark: false, annual: true });
check("five gamma plus", by(seats, "gamma").tier === "Plus" && by(seats, "gamma").monthlyCents === 4500 && by(seats, "gamma").annualCents === 54000);
check("five gamma keep", by(seats, "gamma").verdict === "Keep");
check("five canva business", by(seats, "canva-ai").annualCents === 125000 && by(seats, "canva-ai").monthlyCents === Math.round(125000 / 12));
check("five canva test", by(seats, "canva-ai").verdict === "Test" && by(seats, "canva-ai").covers);
check("five slides unpriced", by(seats, "htmlslides").monthlyCents === null && by(seats, "htmlslides").verdict === "Test");
check("five microsoft test", by(seats, "microsoft-copilot").monthlyCents === 10500 && by(seats, "microsoft-copilot").verdict === "Test");

const brand = calc.priceDeck({ seats: 1, decks: 2, brand: true, watermark: false, annual: true });
check("brand forces pro", by(brand, "gamma").tier === "Pro" && by(brand, "gamma").monthlyCents === 1800 && by(brand, "gamma").verdict === "Keep");
check("brand canva uncovered", by(brand, "canva-ai").covers === false && by(brand, "canva-ai").monthlyCents === null);
check("brand slides uncovered", by(brand, "htmlslides").covers === false && by(brand, "htmlslides").monthlyCents === 990);
check("brand microsoft uncovered", by(brand, "microsoft-copilot").covers === false && by(brand, "microsoft-copilot").monthlyCents === 2100);
check("brand gap excludes uncovered", brand.savingsAnnualCents === 0);

const monthly = calc.priceDeck({ seats: 5, decks: 3, brand: false, watermark: false, annual: false });
["gamma", "canva-ai", "microsoft-copilot"].forEach((slug) => {
  check(slug + " monthly paid blank", by(monthly, slug).monthlyCents === null && by(monthly, slug).covers === false);
});
const monthlyFree = calc.priceDeck({ seats: 1, decks: 3, brand: false, watermark: false, annual: false });
check("monthly free gamma", by(monthlyFree, "gamma").monthlyCents === 0 && by(monthlyFree, "gamma").covers);
check("monthly microsoft blank", by(monthlyFree, "microsoft-copilot").monthlyCents === null);

const mark = calc.priceDeck({ seats: 1, decks: 1, brand: false, watermark: true, annual: true });
check("watermark is plus", by(mark, "gamma").tier === "Plus" && by(mark, "gamma").monthlyCents === 900);

if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}
console.log("presentation calc ok");
"""


def _need(html: str, needle: str, errors: list[str], label: str) -> None:
    if needle not in html:
        errors.append(f"{label} missing {needle}")


def main() -> None:
    errors: list[str] = []
    proc = subprocess.run(["node", "-e", NODE], cwd=ROOT, capture_output=True, text=True)
    if proc.returncode:
        errors.append(proc.stdout + proc.stderr)

    cfg = json.loads((ROOT / "data" / "newsletter.json").read_text(encoding="utf-8"))
    if cfg.get("send_enabled") is not False:
        errors.append("send_enabled must stay false")

    deck = ROOT / "compare" / "ai-presentation-cost" / "index.html"
    traps = ROOT / "pricing-watch" / "credit-traps" / "index.html"
    archive = ROOT / "newsletter" / "index.html"
    subscribe = ROOT / "subscribe" / "index.html"
    home = ROOT / "index.html"
    for path in (deck, traps, archive, subscribe, home):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        raise SystemExit("\n".join(errors))

    deck_html = deck.read_text(encoding="utf-8")
    _need(deck_html, 'href="/go/gamma/" rel="sponsored nofollow noopener"', errors, "deck")
    _need(deck_html, 'href="/go/canva-ai/" rel="external noopener"', errors, "deck")
    _need(deck_html, 'href="/go/htmlslides/" rel="external noopener"', errors, "deck")
    _need(deck_html, 'href="/go/microsoft-copilot/" rel="external noopener"', errors, "deck")
    _need(deck_html, "Beautiful.ai", errors, "deck")
    if "/go/beautiful" in deck_html or "beautiful.ai/" in deck_html.casefold():
        errors.append("deck page invented a Beautiful.ai hop")
    if 'id="site-nav"' not in deck_html or 'href="/newsletter/">Newsletter</a>' not in deck_html:
        errors.append("deck page missing the Newsletter nav link")

    trap_html = traps.read_text(encoding="utf-8")
    for needle in (
        "Monthly credits expire after 65 days.",
        "Monthly plan credits expire two months after issue.",
        "Credits normally expire at the end of the subscription term.",
        "The checked pricing summary does not state a credit rollover or reset rule.",
        "data-pill=\"expiry90\"",
        "data-pill=\"lock\"",
        "data-pill=\"reset\"",
        "data-pill=\"annual\"",
        "Check if my tools have credit traps",
        'name="company_website"',
        "aitools-newsletter-subscribe.aitoolsessentials.workers.dev",
        'href="/compare/ai-presentation-cost/"',
        'href="/go/gamma/" rel="sponsored nofollow noopener"',
        'href="/go/heygen/" rel="external noopener"',
    ):
        _need(trap_html, needle, errors, "traps")
    if "HeyGen credits do not roll" in trap_html or "Zapier tasks reset" in trap_html:
        errors.append("traps page invented a rollover rule")

    archive_html = archive.read_text(encoding="utf-8")
    for slug in ("2026-w44.html", "2026-w43.html", "2026-w42.html", "2026-w38.html", "2026-w35.html"):
        _need(archive_html, f"/newsletter/{slug}", errors, "archive")
    _need(archive_html, "Issues 2 and 3 were not published.", errors, "archive")
    _need(archive_html, 'name="company_website"', errors, "archive")
    _need(archive_html, 'href="/subscribe/"', errors, "archive")
    _need(archive_html, "call-pill-keep", errors, "archive")
    if "2026-w36" in archive_html or "2026-w37" in archive_html or "Issue 2" in archive_html or "Issue 3" in archive_html:
        if "were not published" not in archive_html:
            errors.append("archive invented issue 2 or 3")
    for slug in ("2026-w36.html", "2026-w37.html", "2026-w39.html", "2026-w40.html", "2026-w41.html"):
        if (ROOT / "newsletter" / slug).is_file():
            errors.append(f"unexpected issue file {slug}")

    issue = (ROOT / "newsletter" / "2026-w44.html").read_text(encoding="utf-8")
    _need(issue, 'href="/newsletter/">← All past issues', errors, "issue 7")
    _need(issue, "Previous · Issue 6 ·", errors, "issue 7")
    if "newsletter-pager-next" in issue:
        errors.append("issue 7 invented a next issue")

    sub_html = subscribe.read_text(encoding="utf-8")
    _need(sub_html, "ledger-mast", errors, "subscribe")
    _need(sub_html, "Recent issues", errors, "subscribe")
    _need(sub_html, "/newsletter/2026-w44.html", errors, "subscribe")
    _need(sub_html, "aitools-newsletter-subscribe.aitoolsessentials.workers.dev", errors, "subscribe")
    _need(sub_html, "1090 West Foothill, Claremont, CA 91711", errors, "subscribe")
    if "aitools-bot-logo" in sub_html or "scene-dark\"" in sub_html and "ledger-mast" not in sub_html:
        errors.append("subscribe page kept the bot-logo scene")
    if "beehiiv" in sub_html.casefold() or "formsubmit" in sub_html.casefold():
        errors.append("subscribe page points at an old form host")

    home_html = home.read_text(encoding="utf-8")
    _need(home_html, 'href="/newsletter/">Browse all past issues →', errors, "home")
    _need(home_html, 'href="/newsletter/2026-w44.html"', errors, "home")
    _need(home_html, 'href="/compare/ai-presentation-cost/"', errors, "home")
    _need(home_html, 'href="/pricing-watch/credit-traps/"', errors, "home")
    _need(home_html, 'href="/newsletter/">Newsletter</a>', errors, "home")

    if errors:
        raise SystemExit("\n".join(errors))
    print("wave 4 ok")


if __name__ == "__main__":
    main()
