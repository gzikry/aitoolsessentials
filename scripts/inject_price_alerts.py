#!/usr/bin/env python3
"""Add a price-and-credit alert signup beside pricing on tool and comparison pages.

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


def _block(name: str, tool_id: str, source: str, endpoint: str) -> str:
    safe = html.escape(name, quote=True)
    sentence = (
        f"Track {safe} price &amp; credit-rule changes — get an email when {safe} "
        "changes tier pricing, credit rollover, or free-plan limits."
    )
    hidden = (
        f'<input type="hidden" name="tool" value="{html.escape(tool_id, quote=True)}">'
        f'<input type="hidden" name="source_page" value="{html.escape(source, quote=True)}">'
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
    aside = f'<aside class="price-alert ledger-sheet"><p>{sentence}</p>{form}</aside>'
    return START + aside + END


def _tool_id(path: Path) -> str:
    if path.parent.name != "tools" and path.name == "index.html":
        return path.parent.name
    return path.stem


def _targets(root: Path) -> list[Path]:
    pages = list((root / "tools").glob("*/index.html"))
    pages.extend((root / "comparisons").glob("*.html"))
    return sorted(pages)


def inject(root: Path) -> int:
    endpoint = _endpoint(root)
    changed = 0
    for path in _targets(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if 'http-equiv="refresh"' in text or "<main" not in text:
            continue
        rel = path.relative_to(root).as_posix()
        block = _block(_name(text, path.stem, path), _tool_id(path), rel, endpoint)
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
