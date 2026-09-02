#!/usr/bin/env python3
"""Public monthly keep/cut digest pages from data/monthly_digests.json."""
from __future__ import annotations

import json
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
HEADER = '<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/change-radar/">Change radar</a><a href="/pricing-watch/">Pricing Watch</a><a href="/articles/index.html">Guides</a><a href="/premium/">Premium</a></nav><a class="nav-cta" href="/premium/">Premium</a></header>'
FOOTER = f'<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a></footer>'


def esc(s: object) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def source_item(url: str) -> str:
    href = esc(url)
    if url.startswith("http://") or url.startswith("https://"):
        return f'<li><a href="{href}" rel="external nofollow" target="_blank">{href}</a></li>'
    return f'<li><a href="{href}">{href}</a></li>'


def listing_item(x: dict) -> str:
    name = esc(x.get("name"))
    note = esc(x.get("note"))
    slug = x.get("slug")
    source = x.get("source_url") or ""
    checked = x.get("checked_at") or ""
    if slug:
        link = f'<a href="/tools/{esc(slug)}/">{name}</a>'
    elif source:
        rel = ' rel="external nofollow" target="_blank"' if source.startswith("http") else ""
        link = f'<a href="{esc(source)}"{rel}>{name}</a>'
    else:
        link = name
    extra = f' Source checked {esc(checked)}.' if checked else ""
    return f"<li>{link} — {note}{extra}</li>"


def generate(root: Path) -> int:
    data = json.loads((root / "data/monthly_digests.json").read_text())
    out = root / "updates"
    out.mkdir(exist_ok=True)
    cards = []
    for d in data:
        slug = d["slug"]
        listings = "".join(listing_item(x) for x in d.get("new_listings", []))
        launches = "".join(listing_item(x) for x in d.get("vendor_launches", []))
        watch = "".join(listing_item(x) for x in d.get("watch_list", []))
        sources = "".join(source_item(s) for s in d.get("sources", []))
        desc = d.get("summary", "")
        launches_block = (
            f"<h2>Vendor launches (not directory listings)</h2><ul>{launches}</ul>"
            if launches else ""
        )
        sources_block = (
            f"<h2>Sources</h2><ul>{sources}</ul>"
            if sources else ""
        )
        page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(desc)}"><title>{esc(d["title"])} | AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/updates/{esc(slug)}.html"><link rel="stylesheet" href="/css/styles.css"><link rel="stylesheet" href="/css/share.css"></head><body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Keep/cut digest · checked {esc(d.get("checked_at"))}</p><h1>{esc(d["title"])}</h1><p class="subhead">{esc(desc)}</p><p><a class="button button-blue" href="/subscribe/">Get the digest</a><a class="button button-blue" href="/change-radar/" style="margin-left:8px">Open Change Radar</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
<div class="score-card"><span>Rule</span><h2>Keep one tool per weekly job.</h2><p>{esc(d.get("keep_cut_rule"))}</p></div>
<h2>New listings this month</h2><ul>{listings or "<li>None recorded.</li>"}</ul>
{launches_block}
<h2>Re-check before you renew</h2><ul>{watch or "<li>None recorded.</li>"}</ul>
{sources_block}
<p>These notes are from recorded directory checks, not a live vendor API. Confirm prices and model names on official pages. Public digest is the headline list. <a href="/premium/">Premium</a> members get the curated alert feed, stack-audit template, and 7-day free trial (code LAUNCH50 for 50% off the first paid month, new users).</p>
<p>Related: <a href="/pricing-watch/">Pricing Watch</a> · <a href="/model-lineups/">Model lineups</a> · <a href="/articles/how-to-cut-ai-tool-subscriptions.html">Cut overlapping subscriptions</a></p>
</div></section>
</main>{FOOTER}<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script></body></html>'''
        (out / f"{slug}.html").write_text(page)
        cards.append(
            f'<article class="content-hub-card"><span>{esc(d["month_label"])}</span><h3><a href="/updates/{esc(slug)}.html">{esc(d["title"])}</a></h3><p>{esc(desc)}</p><a class="button button-blue small" href="/updates/{esc(slug)}.html">Read digest</a></article>'
        )
    hub_desc = "Dated public keep/cut digests of recorded AI tool listing, pricing, and model-lineup checks."
    hub = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(hub_desc)}"><title>AI tool change digests | AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/updates/"><link rel="stylesheet" href="/css/styles.css"></head><body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Repeat-visit library</p><h1>What changed. What to keep. What to cut.</h1><p class="subhead">{esc(hub_desc)}</p><p><a class="button button-blue" href="/subscribe/">Subscribe free</a><a class="button button-blue" href="/change-radar/" style="margin-left:8px">Live radar</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{"".join(cards)}</div></div></section>
</main>{FOOTER}<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script></body></html>'''
    (out / "index.html").write_text(hub)
    return len(data) + 1


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parent.parent))
