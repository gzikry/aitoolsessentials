#!/usr/bin/env python3
"""Subscribe page: in-house form, held until sending is enabled."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from newsletter_hold import subscribe_form

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
HEADER = '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/newsletter/">Keep/Cut Weekly</a><a href="/subscribe/">Free email</a><a href="/premium/">Paid Premium</a></nav><a class="nav-cta" href="/subscribe/">Get the free email</a></header>'
FOOTER = f'<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="/legal/privacy.html">Privacy</a></footer>'


def esc(s: object) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def signup_block(cfg: dict) -> str:
    logo = esc(cfg.get("logo_url") or "/assets/aitools-bot-logo-256.png")
    return f'''<div class="score-card"><span>Keep/Cut Weekly</span>
<p style="text-align:center"><img src="{logo}" alt="AIToolsEssentials" width="72" height="72" style="border-radius:18px"></p>
<h2>One email. One week. One cut, if you are lucky.</h2>
<p>One email a week. What changed, what to keep, and what to cancel before renewal. Weekly only.</p>
{subscribe_form(str(cfg.get("subscribe_endpoint") or ""))}
</div>'''


def latest_issue(root: Path) -> dict:
    issues = json.loads((root / "data/weekly_issues.json").read_text())
    return issues[0] if issues else {}


def generate(root: Path) -> int:
    cfg = json.loads((root / "data/newsletter.json").read_text())
    desc = cfg.get("description") or "Free keep/cut digest for AI tool pricing and model changes."
    block = signup_block(cfg)
    issue = latest_issue(root)
    issue_slug = esc(issue.get("slug") or "2026-w35")
    issue_title = esc(issue.get("subject") or "Issue 1")
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(desc)}"><title>Subscribe — Keep/Cut Weekly | AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/subscribe/"><link rel="stylesheet" href="/css/styles.css"></head><body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><img src="{esc(cfg.get("logo_url") or "/assets/aitools-bot-logo-256.png")}" alt="AIToolsEssentials" width="72" height="72" style="border-radius:18px"><p class="kicker light">Free weekly email</p><h1>Keep/Cut Weekly.</h1><p class="subhead">{esc(desc)}</p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">{block}
<p>Issue 1 is live on the site: <a href="/newsletter/{issue_slug}.html">{issue_title}</a>. This form is the free email. Paid <a href="/premium/">Premium</a> is a separate $12/month Whop membership — do not use checkout for this list. FormSubmit is only for tool submissions and intake.</p>
</div></section>
</main>{FOOTER}<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script></body></html>'''
    out = root / "subscribe"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page)
    return 1


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parent.parent))
