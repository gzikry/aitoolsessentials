#!/usr/bin/env python3
"""Subscribe page: newsprint ledger, in-house form, recent published issues."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from newsletter_archive import load_letters
from newsletter_hold import subscribe_form
from site_chrome import CANONICAL_HEADER

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"


def esc(value: object) -> str:
    return (
        str(value or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def recent_issues(root: Path) -> str:
    letters = load_letters(root)
    if not letters:
        return "<p>No public issues are on the archive yet. <a href=\"/newsletter/\">Past issues</a>.</p>"
    rows = []
    for letter in letters:
        rows.append(
            "<tr>"
            f"<th>Issue {letter.issue}</th>"
            f"<td>{esc(letter.when)}</td>"
            f'<td><a href="/newsletter/{esc(letter.slug)}.html">{esc(letter.title)}</a></td>'
            "</tr>"
        )
    return (
        '<div class="table-wrap"><table class="ledger-table">'
        "<thead><tr><th>Issue</th><th>Date</th><th>Letter</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div>"
        '<p><a href="/newsletter/">Browse all past issues →</a></p>'
    )


def generate(root: Path) -> int:
    cfg = json.loads((root / "data/newsletter.json").read_text(encoding="utf-8"))
    desc = cfg.get("description") or "Free keep/cut digest for AI tool pricing and model changes."
    form = subscribe_form(str(cfg.get("subscribe_endpoint") or ""))
    issues = recent_issues(root)
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{esc(desc)}">
<title>Subscribe — Keep, Test, Cut | AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/subscribe/">
<meta property="og:title" content="Subscribe — Keep, Test, Cut | AIToolsEssentials">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{DOMAIN}/subscribe/">
<meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<link rel="stylesheet" href="/css/styles.css">
</head>
<body>
{CANONICAL_HEADER}
<main>
<section class="scene scene-dark ledger-mast">
<div style="max-width:880px;margin:0 auto;padding:72px 28px 36px">
<p class="kicker light">Free weekly email</p>
<h1>Keep, Test, Cut.</h1>
<p class="subhead">{esc(desc)}</p>
</div>
</section>
<section class="scene scene-light">
<div class="article-shell wide">
<div class="ledger-sheet">
<h2>One email a week</h2>
<p>What changed, what to keep, and what to cancel before renewal. This form is the free email. Paid <a href="/premium/">Premium</a> is a separate $12/month membership. Do not use that checkout for this list.</p>
{form}
</div>
<h2>Recent issues</h2>
{issues}
<p>Earlier letters stay on the <a href="/newsletter/">archive</a>.</p>
</div>
</section>
</main>
<footer class="footer">
<span>© 2026 AIToolsEssentials</span>
<a href="/newsletter/">Newsletter</a>
<a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a>
<a href="mailto:{EMAIL}">Contact</a>
<a href="/legal/privacy.html">Privacy</a>
</footer>
<script src="/js/site.js" defer></script>
<script src="/js/analytics.js" defer></script>
</body>
</html>
'''
    out = root / "subscribe"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    return 1


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parent.parent))
