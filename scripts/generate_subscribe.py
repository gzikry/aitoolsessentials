#!/usr/bin/env python3
"""Subscribe page: Beehiiv embed or iframe. Never FormSubmit."""
from __future__ import annotations

import json
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
HEADER = '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/newsletter/">Keep/Cut Weekly</a><a href="/subscribe/">Free email</a><a href="/premium/">Paid Premium</a></nav><a class="nav-cta" href="/subscribe/">Get the free email</a></header>'
FOOTER = f'<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="/legal/privacy.html">Privacy</a></footer>'


def esc(s: object) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def beehiiv_block(cfg: dict) -> str:
    """On-domain Beehiiv capture. Never FormSubmit — that is for intake only."""
    embed = (cfg.get("embed_html") or "").strip()
    signup = (cfg.get("signup_url") or "").strip() or "https://aitoolsessentials.beehiiv.com/subscribe"
    if embed:
        return f'<div class="score-card"><span>Keep/Cut Weekly</span><h2>Get the free digest.</h2>{embed}</div>'
    src = esc(signup)
    logo = esc(cfg.get("logo_url") or "/assets/aitools-bot-logo-256.png")
    return f'''<div class="score-card"><span>Keep/Cut Weekly</span>
<p style="text-align:center"><img src="{logo}" alt="AIToolsEssentials" width="72" height="72" style="border-radius:18px"></p>
<h2>One email. One week. One cut, if you are lucky.</h2>
<p>One email a week. What changed, what to keep, and what to cancel before renewal. Weekly only. Hosted on Beehiiv — not FormSubmit.</p>
<p><a class="button button-blue" href="{src}" rel="noopener sponsored nofollow">Get the free email</a></p>
<iframe src="{src}" title="Keep/Cut Weekly signup" loading="lazy" referrerpolicy="no-referrer-when-downgrade" style="width:100%;min-height:520px;border:0;border-radius:12px;background:#fff;margin-top:16px"></iframe>
<p class="affiliate-inline">If the form does not load, use the button. Publication: aitoolsessentials.beehiiv.com.</p>
</div>'''


def latest_issue(root: Path) -> dict:
    issues = json.loads((root / "data/weekly_issues.json").read_text())
    return issues[0] if issues else {}


def generate(root: Path) -> int:
    cfg = json.loads((root / "data/newsletter.json").read_text())
    desc = cfg.get("description") or "Free keep/cut digest for AI tool pricing and model changes."
    block = beehiiv_block(cfg)
    issue = latest_issue(root)
    issue_slug = esc(issue.get("slug") or "2026-w35")
    issue_title = esc(issue.get("subject") or "Issue 1")
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(desc)}"><title>Subscribe — Keep/Cut Weekly | AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/subscribe/"><link rel="stylesheet" href="/css/styles.css"></head><body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><img src="{esc(cfg.get("logo_url") or "/assets/aitools-bot-logo-256.png")}" alt="AIToolsEssentials" width="72" height="72" style="border-radius:18px"><p class="kicker light">Free weekly email · Beehiiv</p><h1>Keep/Cut Weekly.</h1><p class="subhead">{esc(desc)}</p></div></section>
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
