#!/usr/bin/env python3
"""Embeds hub, calculator iframes, audited badges, and the cite drawer."""
from __future__ import annotations

import html
import json
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
