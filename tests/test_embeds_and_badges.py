#!/usr/bin/env python3
"""Embeds hub, calculator iframes, audited badges, and the cite drawer."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMBEDS = (
    "ai-bill-slasher",
    "ai-coding-assistants",
    "ai-video-avatar-cost",
    "automation-task-calculator",
)


def test_embed_pages() -> None:
    tools = json.loads((ROOT / "data" / "tools.json").read_text(encoding="utf-8"))
    count = str(len(tools))
    hub = (ROOT / "embeds" / "index.html").read_text(encoding="utf-8")
    if "Free embeddable AI cost calculators and audited badges" not in hub:
        raise AssertionError("embeds hub title")
    if f"Full {count}-tool breakdown" not in hub and f'height="480"' not in hub:
        raise AssertionError("embeds hub missing iframe height")
    for slug in EMBEDS:
        if f'src="/embed/{slug}/"' not in hub:
            raise AssertionError(f"hub missing iframe {slug}")
        page = (ROOT / "embed" / slug / "index.html").read_text(encoding="utf-8")
        if 'background:#FAF8F5' not in page or "color:#111315" not in page:
            raise AssertionError(f"{slug} missing newsprint colors")
        if f"Full {count}-tool breakdown" not in page:
            raise AssertionError(f"{slug} missing attribution")
        if 'class="embed-bar"' not in page:
            raise AssertionError(f"{slug} missing attribution bar")
        if "<h1>" not in page:
            raise AssertionError(f"{slug} missing h1")
    voice = (ROOT / "embed" / "ai-video-avatar-cost" / "index.html").read_text(encoding="utf-8")
    if 'rel="' + "sponsored nofollow noopener" + '"' not in voice and "row.rel" not in voice:
        raise AssertionError("voice embed must keep the calculator rel")
    coding = (ROOT / "embed" / "ai-coding-assistants" / "index.html").read_text(encoding="utf-8")
    if "external noopener" not in coding or "sponsored" in coding:
        raise AssertionError("coding embed must not mark non-partners sponsored")
    auto = (ROOT / "embed" / "automation-task-calculator" / "index.html").read_text(encoding="utf-8")
    if "money(row.monthlyCents, row.currency)" not in auto:
        raise AssertionError("automation embed must pass row.currency into money()")
    if ' " EUR"' in auto or " EUR" in auto:
        raise AssertionError("automation embed must not suffix a second EUR label")
    if 'prev.tagName === "TEXTAREA"' not in hub or 'prev.querySelector("textarea")' not in hub:
        raise AssertionError("embeds hub copy handler must read a textarea or a label wrapping one")


def test_badges() -> None:
    tools = json.loads((ROOT / "data" / "tools.json").read_text(encoding="utf-8"))
    stamp = (ROOT / "badges" / "audited.svg").read_text(encoding="utf-8")
    if "AUDITED BY AI TOOLS ESSENTIALS" not in stamp:
        raise AssertionError("generic stamp")
    if "#FAF8F5" not in stamp or "#111315" not in stamp:
        raise AssertionError("stamp colors")
    for tool in tools:
        path = ROOT / "badges" / f"{tool['slug']}.svg"
        if not path.exists():
            raise AssertionError(f"missing badge {tool['slug']}")
        svg = path.read_text(encoding="utf-8")
        if "AUDITED BY AI TOOLS ESSENTIALS" not in svg:
            raise AssertionError(f"{tool['slug']} stamp")
        if html.escape(tool["name"], quote=True) not in svg and tool["name"] not in svg:
            raise AssertionError(f"{tool['slug']} name")
        if "#FAF8F5" not in svg:
            raise AssertionError(f"{tool['slug']} paper")
        if 'x="342" y="20" text-anchor="end"' not in svg:
            raise AssertionError(f"{tool['slug']} month is not on the header row")
        if 'y="86" text-anchor="end"' in svg:
            raise AssertionError(f"{tool['slug']} month still sits on the trap line")
        price = html.unescape(re.search(r'y="66"[^>]*>([^<]*)<', svg).group(1))
        trap = html.unescape(re.search(r'y="86"[^>]*>([^<]*)<', svg).group(1))
        if len(price) > 46:
            raise AssertionError(f"{tool['slug']} price is {len(price)} characters")
        if len(trap) > 50:
            raise AssertionError(f"{tool['slug']} trap is {len(trap)} characters")


def test_cite_drawer() -> None:
    tools = json.loads((ROOT / "data" / "tools.json").read_text(encoding="utf-8"))
    for tool in tools:
        page = ROOT / "tools" / tool["slug"] / "index.html"
        html = page.read_text(encoding="utf-8")
        if "Cite or embed this audit" not in html:
            raise AssertionError(f"{tool['slug']} drawer")
        if f"utm_source=badge_embed" not in html:
            raise AssertionError(f"{tool['slug']} utm")
        if f"/badges/{tool['slug']}.svg" not in html:
            raise AssertionError(f"{tool['slug']} badge url")
        if "@misc{" not in html:
            raise AssertionError(f"{tool['slug']} bibtex")
        if "[![" not in html:
            raise AssertionError(f"{tool['slug']} markdown")


if __name__ == "__main__":
    test_embed_pages()
    test_badges()
    test_cite_drawer()
    print("embeds and badges ok")
