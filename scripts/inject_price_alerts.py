#!/usr/bin/env python3
"""Add a price-and-credit alert signup on tool, comparison, and price-hub pages.

The form posts to the existing workers.dev subscribe endpoint. Extra hidden
fields are ignored by that worker. Newsletter issues stay send_enabled false.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

from newsletter_hold import compliance_footer, subscribe_endpoint

START = "<!-- AIT PRICE ALERT START -->"
END = "<!-- AIT PRICE ALERT END -->"
BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
DIV_TOKEN = re.compile(r"<div\b|</div>", re.I)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S | re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")


def _endpoint(root: Path) -> str:
    data = json.loads((root / "data" / "newsletter.json").read_text(encoding="utf-8"))
    return subscribe_endpoint(data.get("subscribe_endpoint", ""))


def _name(text: str, fallback: str, path: Path) -> str:
    match = H1_RE.search(text) or TITLE_RE.search(text)
    raw = TAG_RE.sub("", match.group(1) if match else fallback)
    raw = re.sub(r"\s+", " ", raw).strip()
    raw = re.sub(r"\s+[—–|-]\s+AIToolsEssentials$", "", raw)
    if "tools" in path.parts and raw.lower().endswith(" review"):
        raw = raw[: -len(" review")].strip()
    return raw or fallback


def _end_of_div(text: str, start: int) -> int | None:
    depth = 0
    for match in DIV_TOKEN.finditer(text, start):
        if match.group(0).lower().startswith("</"):
            depth -= 1
            if depth == 0:
                return match.end()
        else:
            depth += 1
    return None


def _insert_at(text: str) -> int | None:
    card = text.find('<div class="official-source-card"')
    if card != -1:
        end = _end_of_div(text, card)
        if end:
            return end
    main = text.find("<main")
    if main == -1:
        return None
    main_end = text.find("</main>", main)
    if main_end == -1:
        return None
    table_end = text.find("</table>", main, main_end)
    if table_end != -1:
        return table_end + len("</table>")
    return main_end


# Price and decision hubs: one alert box for every tool on the page.
_HUBS = {
    "pricing-watch/index.html": "pricing-watch",
    "pricing-watch/credit-traps/index.html": "credit-traps",
    "change-radar/index.html": "change-radar",
    "price-changes/index.html": "price-changes",
    "pricing-index/index.html": "pricing-index",
}


def _sentence(name: str, hub: bool) -> str:
    if hub:
        return (
            "Get an email when a tool you pay for changes its price, credits, or free plan. "
            "Each change is tied to the vendor's own pricing page with the date we checked it."
        )
    safe = html.escape(name, quote=True)
    return (
        f"Track {safe} price &amp; credit-rule changes — get an email when {safe} "
        "changes tier pricing, credit rollover, or free-plan limits."
    )


def _block(
    name: str,
    tool_id: str,
    source: str,
    endpoint: str,
    hub: bool = False,
    *,
    watch_tool: bool = True,
) -> str:
    sentence = _sentence(name, hub)
    tool_input = ""
    if watch_tool:
        tool_input = f'<input type="hidden" name="tool" value="{html.escape(tool_id, quote=True)}">'
    hidden = (
        tool_input
        + f'<input type="hidden" name="source_page" value="{html.escape(source, quote=True)}">'
    )
    fields = (
        hidden
        + '<p><label>Email <input type="email" name="email" autocomplete="email" required></label></p>'
        + '<p class="subscribe-honeypot"><label>Company website '
        + '<input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></p>'
        + '<p><button class="button button-blue" type="submit">Get the free email</button></p>'
        + "<p>One email a week. We send a confirm link first.</p>"
        + f"<p>{compliance_footer()}</p>"
    )
    if endpoint:
        form = (
            f'<form class="price-alert-form" method="post" action="{html.escape(endpoint, quote=True)}">'
            + fields
            + "</form>"
        )
    else:
        form = '<p><a href="/subscribe/">Get the free email</a></p>' + f"<p>{compliance_footer()}</p>"
    anchor = ' id="price-alert"' if hub else ""
    aside = f'<aside class="price-alert ledger-sheet"{anchor}><p>{sentence}</p>{form}</aside>'
    return START + aside + END


def signup_block(root: Path, *, source: str, hub: bool = False, tool_id: str = "", name: str = "") -> str:
    """The same signup box tool and comparison pages already use.

    A tool page passes its slug so the subscribe worker can store it on
    price_watch. A page that is not one tool omits that field.
    """
    return _block(name, tool_id, source, _endpoint(root), hub=hub, watch_tool=bool(tool_id))


def _tool_id(path: Path) -> str:
    if path.parent.name != "tools" and path.name == "index.html":
        return path.parent.name
    return path.stem


def _targets(root: Path) -> list[Path]:
    pages = list((root / "tools").glob("*/index.html"))
    pages.extend((root / "comparisons").glob("*.html"))
    pages.extend(root / rel for rel in _HUBS if (root / rel).is_file())
    return sorted(set(pages))


def inject(root: Path) -> int:
    endpoint = _endpoint(root)
    changed = 0
    for path in _targets(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if 'http-equiv="refresh"' in text or "<main" not in text:
            continue
        rel = path.relative_to(root).as_posix()
        hub = rel in _HUBS
        tool_id = _HUBS.get(rel) or _tool_id(path)
        block = _block(_name(text, path.stem, path), tool_id, rel, endpoint, hub=hub)
        if START in text:
            updated = BLOCK_RE.sub(block, text, count=1)
        else:
            at = _insert_at(text)
            if at is None:
                continue
            updated = text[:at] + "\n" + block + "\n" + text[at:]
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


if __name__ == "__main__":
    print(inject(Path(__file__).resolve().parents[1]))
