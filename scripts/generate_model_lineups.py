#!/usr/bin/env python3
"""Inject "current model lineup" panels into head-to-head comparison pages.

Data-driven from data/model_lineups.json so updates stay durable through the
pipeline. Panels render above the verdict sections on each comparison page.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

MARK_S = "<!-- AIT LINEUP START -->"
MARK_E = "<!-- AIT LINEUP END -->"
LINEUP_RE = re.compile(re.escape(MARK_S) + r".*?" + re.escape(MARK_E) + r"\n?", re.S)

COMPARISONS = {
    'chatgpt-vs-claude.html': ['chatgpt', 'claude'],
    'chatgpt-vs-grok.html': ['chatgpt', 'grok'],
    'claude-vs-grok.html': ['claude', 'grok'],
    'cursor-vs-github-copilot.html': ['cursor', 'github-copilot'],
    'perplexity-vs-chatgpt.html': ['perplexity', 'chatgpt'],
    'chatgpt-vs-perplexity.html': ['chatgpt', 'perplexity'],
    'claude-vs-cursor.html': ['claude', 'cursor'],
    'midjourney-vs-canva-ai.html': ['midjourney', 'canva-ai'],
    'zapier-vs-make-vs-n8n.html': ['zapier-ai', 'make', 'n8n'],
}


def generate(root: Path) -> int:
    lineups = json.loads((root / 'data/model_lineups.json').read_text())
    tools = {x['slug']: x for x in json.loads((root / 'data/tools.json').read_text())}
    changed = 0
    for filename, slugs in COMPARISONS.items():
        path = root / 'comparisons' / filename
        if not path.exists():
            continue
        html = path.read_text()
        original = html
        cards = ''
        used = False
        for slug in slugs:
            lu = lineups.get(slug)
            if not lu:
                continue
            used = True
            rows = ''.join(
                f'<tr><td><strong>{m["model"]}</strong></td><td>{m["role"]}</td>'
                f'<td>{m.get("context", "-")}</td><td>{m.get("pricing", "-")}</td></tr>'
                for m in lu['models']
            )
            notes = ''.join(f'<li>{n}</li>' for n in lu.get('notes', []))
            cards += (
                f'<div><strong>{tools[slug]["name"]} — current lineup ({lu["as_of"]})</strong>'
                f'<div class="table-wrap"><table><thead><tr><th>Model</th><th>Role</th>'
                f'<th>Context</th><th>Pricing</th></tr></thead><tbody>{rows}</tbody></table></div>'
                f'<ul class="lineup-notes">{notes}</ul></div>'
            )
        if not used:
            continue
        panel = (
            f'{MARK_S}<section class="comparison-evidence"><h2>Current model lineup</h2>'
            f'<p>Version names and prices move fast. This panel tracks what each product '
            f'actually ships today, with checked dates — so the comparison stays about '
            f'real models, not marketing names.</p><div class="decision-grid">{cards}</div>'
            f'<p class="benchmark-caveat">Lineups verified from official vendor pages; confirm before purchase.</p>'
            f'</section>{MARK_E}\n'
        )
        # Replace existing block or insert before the "When ... is the better fit" section
        if MARK_S in html:
            html = LINEUP_RE.sub(lambda _m: panel, html)
        else:
            marker = '<h2>When '
            idx = html.find(marker)
            if idx >= 0:
                html = html[:idx] + panel + html[idx:]
            else:
                # Fall back to inserting before "How to decide", then "Quick recommendation"
                for marker in ('<h2>How to decide</h2>', '<h2>Quick recommendation</h2>'):
                    idx = html.find(marker)
                    if idx >= 0:
                        html = html[:idx] + panel + html[idx:]
                        break
                else:
                    continue
        if html != original:
            path.write_text(html)
            changed += 1
    print(f'Model lineup panels on {changed} comparison pages')
    return changed


if __name__ == '__main__':
    generate(Path(__file__).resolve().parent.parent)
