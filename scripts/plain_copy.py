#!/usr/bin/env python3
"""Plain-copy pass, Nov 2026 cleanup (P3). Runs after simplify_pages.py.

Visible body text only. Tags, attributes, <head>, scripts, styles, <pre>,
<code> and <textarea> are left alone, so links, schema and embed snippets do
not change.

* Em dashes become commas (or hyphens in number ranges).
* " — AIToolsEssentials" suffixes on link labels go.
* A short list of house jargon and slogans is replaced (PHRASES).

scripts/test_plain_copy.py keeps BANNED out of every public page.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_scope import is_public_rel

PHRASES = (
    ("Interactive ledger", "Cost calculator"),
    ("Run the numbers in the interactive calculator →", "Open the cost calculator"),
    ("Choose with evidence, not hype.", "Compare before you pay."),
    ("Turn this page into a decision.", ""),
    (", not hype", ""),
    ("credit clock", "credit expiry rules"),
    ("Credit clock", "Credit expiry rules"),
    ("cut sheet", "subscription summary"),
    ("Cut sheet", "Subscription summary"),
    ("Chatgpt", "ChatGPT"),
    ("Github Copilot", "GitHub Copilot"),
)
# Must not appear in any public page's visible text once this pass has run.
BANNED = (
    "—",
    "not hype",
    "Turn this page into a decision",
    "credit clock",
    "cut sheet",
    "Interactive ledger",
    "Chatgpt",
    "Github Copilot",
    " Vs ",
)

_SKIP_RE = re.compile(r"<(script|style|pre|code|textarea)\b.*?</\1\s*>", re.S | re.I)
_TAG_RE = re.compile(r"(<[^>]*>)")
_SUFFIX_RE = re.compile(r"\s+[—|]\s+AIToolsEssentials\s*$")


def plain_text(text: str) -> str:
    if not text.strip():
        return text
    text = _SUFFIX_RE.sub("", text)
    for old, new in PHRASES:
        text = text.replace(old, new)
    text = re.sub(r"(\d)\s*—\s*(\d)", r"\1-\2", text)
    text = re.sub(r"\s+—\s+", ", ", text)
    text = re.sub(r"\s*—\s*", ", ", text) if text.strip() != "—" else text.replace("—", "-")
    text = text.replace(" Vs ", " vs ")
    text = text.replace(", not hype", "")
    # A comma right before other punctuation reads badly: "word, ." or ", ,".
    text = re.sub(r",\s*([,.;:)])", r"\1", text)
    return text


def _plain_segment(segment: str) -> str:
    parts = _TAG_RE.split(segment)
    return "".join(p if i % 2 else plain_text(p) for i, p in enumerate(parts))


def _body_start(html: str) -> int:
    """Where visible copy starts. A few hand-written pages have no <body> or </head>."""
    for marker in ("<body", "</head>", "<header", "<main"):
        start = html.find(marker)
        if start != -1:
            return start
    return -1


def plain_body(html: str) -> str:
    start = _body_start(html)
    if start == -1:
        return html
    head, body = html[:start], html[start:]
    out, pos = [], 0
    for m in _SKIP_RE.finditer(body):
        out.append(_plain_segment(body[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(_plain_segment(body[pos:]))
    return head + "".join(out)


def visible_text(html: str) -> str:
    start = _body_start(html)
    body = html[start:] if start != -1 else html
    body = _SKIP_RE.sub(" ", body)
    return " ".join(p for i, p in enumerate(_TAG_RE.split(body)) if not i % 2)


def apply(root: Path) -> int:
    changed = 0
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if not is_public_rel(rel):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if 'http-equiv="refresh"' in text:
            continue
        updated = plain_body(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


if __name__ == "__main__":
    print(apply(Path(__file__).resolve().parents[1]))
