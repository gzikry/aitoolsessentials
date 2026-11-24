#!/usr/bin/env python3
"""Write /founders/, the founder launch desk, and its homepage launch line.

Founders already send tools every day. This page sells them what they can
point to: a faster written decision, a labeled launch card, and a labeled
newsletter line. Payment never changes a score, a rank, or a verdict.

Products live in data/founder_products.json. A product with no payment_url
renders as an email request. Only a live https://buy.stripe.com/ link renders
as a checkout button, so nothing can be bought before a Stripe product exists.
"""
from __future__ import annotations

import datetime as _dt
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

_DEST = Path("founders") / "index.html"
_DATA = Path("data") / "founder_products.json"
_HOME_S = "<!-- AIT FOUNDER LAUNCH LINE START -->"
_HOME_E = "<!-- AIT FOUNDER LAUNCH LINE END -->"
_HOME_RE = re.compile(re.escape(_HOME_S) + r".*?" + re.escape(_HOME_E), re.S)
_STRIPE = re.compile(r"^https://buy\.stripe\.com/[A-Za-z0-9]+$")
_TEST_LINK = re.compile(r"buy\.stripe\.com/test_", re.I)
_EXTERNAL_REL = "external noopener nofollow"
_TITLE = "Founder launch desk — AIToolsEssentials"
_DESC = (
    "Launching an AI tool? Skip the free queue with a $79 written decision in one working day, "
    "or book a labeled launch card. Payment never changes a score."
)
_KEYS = ("verified", "launch_feature", "roundup_line", "launch_pack")
_LINE_LIMIT = 80


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def load(root: Path) -> dict:
    data = json.loads((root / _DATA).read_text(encoding="utf-8"))
    keys = tuple(p.get("key") for p in data.get("products", []))
    if keys != _KEYS:
        raise ValueError(f"founder products must be {_KEYS}, got {keys}")
    for product in data["products"]:
        url = (product.get("payment_url") or "").strip()
        if url and (not _STRIPE.match(url) or _TEST_LINK.search(url)):
            raise ValueError(f"{product['key']}: payment_url must be a live buy.stripe.com link")
    return data


def active_launches(data: dict, today: _dt.date) -> list[dict]:
    rows = []
    for launch in data.get("launches") or []:
        start = _dt.date.fromisoformat(launch["start"])
        end = start + _dt.timedelta(days=6)
        url = str(launch.get("url") or "")
        line = str(launch.get("line") or "").strip()
        if not url.startswith("https://") or not line or len(line) > _LINE_LIMIT:
            raise ValueError(f"bad launch row: {launch.get('name')}")
        if start <= today <= end:
            rows.append(launch)
    return rows


def _button(product: dict, contact: str) -> str:
    url = (product.get("payment_url") or "").strip()
    if url:
        return (
            f'<a class="button button-blue" href="{_esc(url)}" target="_blank" rel="{_EXTERNAL_REL}">'
            f"Pay {_esc(product['price'])} for the {_esc(product['name'].lower())}</a>"
        )
    subject = quote(f"{product['name']} ({product['price']})")
    return (
        f'<a class="button button-blue" href="mailto:{_esc(contact)}?subject={subject}">'
        f"Email to book the {_esc(product['name'].lower())}</a>"
        " <span class=\"ledger-note\">Checkout opens soon. We reply with a payment link.</span>"
    )


def _product_card(product: dict, contact: str) -> str:
    items = "".join(f"<li>{_esc(item)}</li>" for item in product.get("includes", []))
    return (
        f'<article class="submit-lane founder-product" id="{_esc(product["key"])}">'
        f"<h2>{_esc(product['name'])}. {_esc(product['price'])} {_esc(product['price_note'])}.</h2>"
        f"<p>{_esc(product['summary'])}</p><ul>{items}</ul>"
        f"<p>{_button(product, contact)}</p></article>"
    )


def _launch_list(rows: list[dict]) -> str:
    if not rows:
        return "<p>No paid launches are booked this week.</p>"
    items = "".join(
        f'<li><span class="ledger-stamp">Sponsored</span> '
        f'<a href="{_esc(r["url"])}" rel="sponsored noopener nofollow">{_esc(r["name"])}</a> '
        f"— {_esc(r['line'])}</li>"
        for r in rows
    )
    return f"<ul>{items}</ul>"


def page_html(data: dict, today: _dt.date) -> str:
    from site_chrome import canonical_header

    contact = data.get("contact") or "contact@aitoolsessentials.com"
    cards = "".join(_product_card(p, contact) for p in data["products"])
    body = (
        "<h1>Founder launch desk</h1>"
        "<p>Launching an AI tool? The free submission form still works. It joins a queue that "
        "currently runs 3 to 4 weeks, and declined tools get no written feedback. If you need a "
        "date, these are the paid options.</p>"
        "<p><strong>What money never buys:</strong> a score, a rank, a verdict, or a review "
        "date for the free queue. Paid placements are labeled Sponsored. If we would not list "
        "the tool for free, we do not take the money.</p>"
        + cards
        + "<h2>Launching this week</h2>"
        + _launch_list(active_launches(data, today))
        + "<h2>Questions founders ask</h2>"
        "<h3>Does the Verified fast lane change my score?</h3>"
        "<p>No. It changes when you hear back, and you get the reasons in writing. "
        "The score uses the same <a href=\"/methodology/\">methodology</a> as every listing.</p>"
        "<h3>What traffic do you get?</h3>"
        "<p>This site is early. We do not publish traffic or list numbers we cannot stand behind, "
        "so the launch products are priced as small, one-time tests.</p>"
        "<h3>What do you check before taking money?</h3>"
        "<p>A named operator, working legal pages, and a product that does what its page says. "
        "Tools that fail those checks are declined and refunded.</p>"
        f'<p><a href="/submit/">Free submission form</a> · <a href="/sponsor/">Sponsor the site</a> · '
        f'<a href="/badges/">Badge rules</a> · <a href="mailto:{_esc(contact)}">Email us</a></p>'
        "<p>— AIToolsEssentials</p>"
    )
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{_TITLE}</title>\n"
        f'<meta name="description" content="{_esc(_DESC)}">\n'
        '<link rel="canonical" href="https://aitoolsessentials.com/founders/">\n'
        '<link rel="stylesheet" href="/css/styles.css">\n'
        "</head>\n<body>\n"
        + canonical_header(contained=True)
        + '\n<main class="sponsor-offer founder-desk">\n<section class="scene scene-light content-hub">'
        '<div class="article-shell wide">\n'
        + body
        + "\n</div></section>\n</main>\n"
        '<footer class="footer"><span>\u00a9 2026 AIToolsEssentials</span>'
        '<a href="/advertise/" rel="nofollow">Advertise</a>'
        '<a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>'
        '<a href="mailto:contact@aitoolsessentials.com">Contact</a>'
        '<a href="/legal/about.html">About</a>'
        '<a href="/legal/privacy.html">Privacy</a>'
        '<a href="/legal/terms.html">Terms</a></footer>'
        "\n</body>\n</html>\n"
    )


def home_line(data: dict, today: _dt.date) -> str:
    rows = active_launches(data, today)
    if rows:
        r = rows[0]
        inner = (
            f'<span class="ledger-stamp">Sponsored launch</span> '
            f'<a href="{_esc(r["url"])}" rel="sponsored noopener nofollow">{_esc(r["name"])}</a> '
            f"— {_esc(r['line'])} · <a href=\"/founders/\">Book a launch</a>"
        )
    else:
        inner = (
            'Launching an AI tool? <a href="/founders/">Get a written decision in one working day</a>'
            ' or <a href="/submit/">join the free queue</a>.'
        )
    return f'{_HOME_S}<p class="home-founder-line">{inner}</p>{_HOME_E}'


def inject_home(text: str, line: str) -> str:
    if _HOME_S in text:
        return _HOME_RE.sub(lambda _m: line, text, count=1)
    marker = "</main>"
    if marker not in text:
        return text
    return text.replace(marker, line + "\n" + marker, 1)


def generate(root: Path, today: _dt.date | None = None) -> Path:
    from asset_rev import stamp_html

    today = today or _dt.date.today()
    data = load(root)
    dest = root / _DEST
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(stamp_html(page_html(data, today), dest, root), encoding="utf-8")
    home = root / "index.html"
    if home.is_file():
        text = home.read_text(encoding="utf-8")
        updated = inject_home(text, home_line(data, today))
        if updated != text:
            home.write_text(updated, encoding="utf-8")
    return dest


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    print("Wrote", generate(Path(__file__).resolve().parents[1]))
