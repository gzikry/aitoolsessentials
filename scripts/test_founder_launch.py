#!/usr/bin/env python3
"""The founder launch desk sells time and labeled space, never a verdict.

- Only live buy.stripe.com links render as checkout buttons.
- A product without a link renders as an email request.
- Launch cards are labeled Sponsored and expire after 7 days.
- The homepage line points at /founders/ when nothing is booked.
"""
from __future__ import annotations

import copy
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_founder_launch as founder

ROOT = Path(__file__).resolve().parents[1]
DAY = dt.date(2026, 11, 24)


def _fail(msg: str) -> None:
    raise SystemExit(msg)


def _data() -> dict:
    return json.loads((ROOT / "data" / "founder_products.json").read_text(encoding="utf-8"))


def test_committed_data_loads() -> None:
    data = founder.load(ROOT)
    prices = {p["key"]: p["price"] for p in data["products"]}
    if prices != {"verified": "$79", "launch_feature": "$49", "roundup_line": "$29", "launch_pack": "$99"}:
        _fail(f"unexpected prices {prices}")


def test_live_links_render_as_checkouts() -> None:
    html = founder.page_html(_data(), DAY)
    for url in (
        "buy.stripe.com/7sY6oG3Ed2SF7JZ3eD0x205",
        "buy.stripe.com/6oU28q1w59h3e8nbL90x207",
        "buy.stripe.com/8x25kCeiR50N7JZ6qP0x208",
        "buy.stripe.com/6oU6oGeiRbpb4xNbL90x209",
    ):
        if url not in html:
            _fail(f"committed product link {url} should render as a checkout")
    if "mailto:contact@aitoolsessentials.com?subject=Launch-day%20feature" in html:
        _fail("launch feature has a live link and should not be an email request")


def test_empty_link_is_an_email_request() -> None:
    data = copy.deepcopy(_data())
    for product in data["products"]:
        if product["key"] == "launch_feature":
            product["payment_url"] = ""
    html = founder.page_html(data, DAY)
    if "mailto:contact@aitoolsessentials.com?subject=Launch-day%20feature" not in html:
        _fail("launch feature should be an email request until a Stripe link exists")
    if "buy.stripe.com/7sY6oG3Ed2SF7JZ3eD0x205" not in html:
        _fail("verified fast lane should use the live $79 link")
    if "never buys" not in html and "never buy" not in html.lower():
        _fail("page must say money never buys a score")


def test_test_mode_link_is_refused() -> None:
    data = _data()
    data["products"][1]["payment_url"] = "https://buy.stripe.com/test_abc123"
    path = ROOT / "data" / "founder_products.json"
    try:
        tmp = copy.deepcopy(data)
        founder_load = founder.load
        original = path.read_text(encoding="utf-8")
        path.write_text(json.dumps(tmp), encoding="utf-8")
        try:
            founder_load(ROOT)
        except ValueError:
            return
        _fail("a Stripe test link must be refused")
    finally:
        path.write_text(original, encoding="utf-8")


def test_launch_cards_are_labeled_and_expire() -> None:
    data = _data()
    data["launches"] = [{
        "name": "Example Tool",
        "url": "https://example.com/",
        "line": "Turns meeting notes into tasks",
        "start": "2026-11-20",
    }]
    html = founder.page_html(data, DAY)
    if "Sponsored" not in html or 'rel="sponsored noopener nofollow"' not in html:
        _fail("launch card must be labeled and rel=sponsored")
    if founder.active_launches(data, dt.date(2026, 11, 27)) != []:
        _fail("launch card must expire after 7 days")
    line = founder.home_line(data, DAY)
    if "Sponsored launch" not in line:
        _fail("homepage line must be labeled")


def test_home_line_defaults_to_founders_link() -> None:
    line = founder.home_line(_data(), DAY)
    if 'href="/founders/"' not in line or "Sponsored" in line:
        _fail("empty week should link the desk without a sponsored label")
    page = "<main><p>x</p></main>"
    once = founder.inject_home(page, line)
    twice = founder.inject_home(once, line)
    if once != twice or once.count("AIT FOUNDER LAUNCH LINE START") != 1:
        _fail("homepage injection must be idempotent")


def main() -> None:
    test_committed_data_loads()
    test_live_links_render_as_checkouts()
    test_empty_link_is_an_email_request()
    test_test_mode_link_is_refused()
    test_launch_cards_are_labeled_and_expire()
    test_home_line_defaults_to_founders_link()
    print("founder launch desk checks passed")


if __name__ == "__main__":
    main()
