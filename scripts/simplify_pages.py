#!/usr/bin/env python3
"""House style pass, Nov 2026 cleanup (P2). Runs after every generator.

1. Retired bands. Every block listed in RETIRED_BLOCKS is removed wherever an
   older run or another generator left it. The generators that only existed to
   add these bands are no longer called from daily_content_update.py.
2. Scores. No page shows an x/5 score until a tool has a published hands-on
   result (George, Nov 24 2026). No tool has one yet, so the score markup goes.
   JSON-LD only carries a rating for hands-on results already
   (enhance_structured_data.is_hands_on_published).

Redirect stubs are left alone. The pass is idempotent.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_scope import is_public_rel

RETIRED_BLOCKS = (
    "CALCULATOR CALLOUT",
    "CORRECTION MODULE",
    "EVIDENCE LINK",
    "EXIT PLAN",
    "FREE STACK AUDIT CTA",
    "LEAD MAGNET",
    "PREMIUM MODULE",
    "QUIZ LINK",
    "RELATED NEXT STEPS",
    "SOURCE CITE",
    "STACK MODULE",
    "SWITCH GUIDE",
    "TEST PROTOCOL",
    "VERDICT BAR",
)
_BLOCK_RE = re.compile(
    r"\s*<!-- AIT (" + "|".join(re.escape(n) for n in RETIRED_BLOCKS) + r") START -->.*?<!-- AIT \1 END -->\s*",
    re.S,
)

# Bands without markers.
_LOOSE = (
    # Tool pages: the "Choose with evidence, not hype." newsletter band.
    re.compile(r'\s*<section class="newsletter-cta">.*?</section>\s*', re.S),
    # Comparison pages: the scorecard panel.
    re.compile(r'\s*<section class="newsletter-panel"><div><span>AI Tool Evaluation Scorecard</span>.*?</section>\s*', re.S),
    # Decision-brief buttons under tools and comparisons.
    re.compile(r'\s*<p[^>]*>\s*<a [^>]*href="/decision-brief\.html\?vs=[^"]*"[^>]*>[^<]*</a>\s*</p>\s*', re.S),
    # Comparison "On this page" index above the hero.
    re.compile(r'\s*<nav class="page-toc"[^>]*>.*?</nav>\s*', re.S),
    # A loose related-next-steps module some generators write without markers.
    re.compile(r'\s*<section class="score-card related-next-steps">.*?</section>\s*', re.S),
)

# Score markup.
_SCORES = (
    (re.compile(r'<span>AIToolsEssentials editorial score</span>\s*<strong>[^<]*<small[^>]*>/5</small></strong>\s*'
                r'<div class="score-meter"[^>]*>.*?</div>\s*<span>Evidence:[^<]*</span>\s*', re.S), ""),
    (re.compile(r'<span>AIToolsEssentials editorial score</span>\s*<strong>Not yet scored</strong>\s*<span>[^<]*</span>\s*', re.S), ""),
    (re.compile(r'<tr><th>AIToolsEssentials editorial score</th>.*?</tr>', re.S), ""),
    (re.compile(r'<p class="score-note">(?:Scores|Ratings) are editorial.*?</p>', re.S), ""),
    (re.compile(r'<span class="pick-score">[^<]*/5 editorial</span>'), ""),
    (re.compile(r' has an AIToolsEssentials editorial score of [0-9.]+/5\. '), ". "),
    (re.compile(r'\s*<span class="category-pill">#\d+ · (?:[0-9.]+/5(?: editorial)?|Editorial score in review)</span>'), ""),
    (re.compile(r'\s*<span style="color:#f5a623;letter-spacing:2px">★*</span>'), ""),
    (re.compile(r'<dt>Rating \(editorial\)</dt><dd>[^<]*</dd>'), ""),
    (re.compile(r' · [0-9](?:\.[0-9])?/5(?: editorial)?(?=</span>)'), ""),
    (re.compile(r' · Editorial score in review(?=</span>)'), ""),
    (re.compile(r' \(editorial [0-9.]+/5\)'), ""),
    (re.compile(r' · [0-9.]+/5 editorial — '), " — "),
    (re.compile(r'Published at [0-9.]+/5 - job fit [0-9.]+, transparency [0-9.]+ - below every other tool in the catalog because '),
     "Treated with caution because "),
)

_TABLE_RE = re.compile(r"<table\b.*?</table>", re.S)
_ROW_RE = re.compile(r"<tr\b[^>]*>.*?</tr>", re.S)
_CELL_RE = re.compile(r"<t([hd])\b[^>]*>.*?</t\1>", re.S)


def _drop_score_column(table: str) -> str:
    """Remove a Score or Rating column from a ranked table."""
    rows = _ROW_RE.findall(table)
    if not rows:
        return table
    head = [m.group(0) for m in _CELL_RE.finditer(rows[0])]
    idx = next((i for i, c in enumerate(head)
                if re.fullmatch(r"<th\b[^>]*>\s*(?:Score|Rating|Editorial score)\s*</th>", c)), None)
    if idx is None:
        return table

    def fix(row_match: re.Match) -> str:
        row = row_match.group(0)
        cells = list(_CELL_RE.finditer(row))
        if len(cells) <= idx:
            return row
        c = cells[idx]
        return row[:c.start()] + row[c.end():]

    return _ROW_RE.sub(fix, table)


CALC_LABELS = {
    "coding": "AI coding assistant cost calculator",
    "apps": "App builder cost calculator",
    "voice": "Voice and video cost calculator",
    "auto": "Automation cost calculator",
    "deck": "Presentation tool cost calculator",
    "support": "Customer support cost calculator",
}
_ASIDE_ANCHOR = '</div>\n<div class="score-card">\n<span>Related tools</span>'


def add_calculator_link(html: str, href: str, label: str) -> str:
    """One plain link to the matching cost calculator, in the tool page sidebar."""
    if 'class="aside-calc"' in html or _ASIDE_ANCHOR not in html:
        return html
    link = f'<p class="aside-calc"><a href="{href}">{label}</a></p>\n'
    return html.replace(_ASIDE_ANCHOR, link + _ASIDE_ANCHOR, 1)


def _hands_on_slugs(root: Path) -> set[str]:
    from enhance_structured_data import is_hands_on_published

    data = json.loads((root / "data" / "tools.json").read_text(encoding="utf-8"))
    tools = data if isinstance(data, list) else data.get("tools", [])
    return {t["slug"] for t in tools if is_hands_on_published(t)}


_RAW_RE = re.compile(r"(<(pre|textarea|script|style)\b.*?</\2>)", re.S | re.I)
_BLANK_RE = re.compile(r"\n(?:[ \t]*\n)+")


def _collapse_blank_lines(html: str) -> str:
    """Blank lines left by removed bands vary run to run; fold them so output is stable."""
    parts = _RAW_RE.split(html)
    out = []
    i = 0
    while i < len(parts):
        out.append(_BLANK_RE.sub("\n", parts[i]))
        if i + 1 < len(parts):
            out.append(parts[i + 1])
        i += 3
    return "".join(out)


def simplify(html: str, *, keep_scores: bool = False) -> str:
    html = _BLOCK_RE.sub("\n", html)
    for pattern in _LOOSE:
        html = pattern.sub("\n", html)
    if not keep_scores:
        for pattern, repl in _SCORES:
            html = pattern.sub(repl, html)
        html = _TABLE_RE.sub(lambda m: _drop_score_column(m.group(0)), html)
    return _collapse_blank_lines(html)


def apply(root: Path) -> int:
    from inject_ledger_pages import HUBS, _catalog, _hub_key

    hands_on = _hands_on_slugs(root)
    by_slug = _catalog(root)
    changed = 0
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if not is_public_rel(rel):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if 'http-equiv="refresh"' in text:
            continue
        keep = len(rel.parts) == 3 and rel.parts[0] == "tools" and rel.parts[1] in hands_on
        updated = simplify(text, keep_scores=keep)
        if len(rel.parts) == 3 and rel.parts[0] == "tools" and rel.parts[2] == "index.html":
            key = _hub_key(rel.parts[1], by_slug)
            if key:
                updated = add_calculator_link(updated, HUBS[key][0], CALC_LABELS[key])
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


if __name__ == "__main__":
    print(apply(Path(__file__).resolve().parents[1]))
