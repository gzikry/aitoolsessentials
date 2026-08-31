#!/usr/bin/env python3
"""Journalist / editor press page — cite-us landing, not a traffic boast."""
from __future__ import annotations

import json
from pathlib import Path

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
HEADER = '<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/comparisons/">Comparisons</a><a href="/articles/">Guides</a><a href="/pricing-watch/">Pricing Watch</a><a href="/methodology/">Methodology</a></nav><a class="nav-cta" href="/premium/">Premium</a></header>'
FOOTER = f'<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/methodology/">Methodology</a><a href="/evidence/">Evidence</a><a href="/badges/">Badges</a><a href="/legal/about.html">About</a><a href="/legal/affiliate-disclosure.html" rel="nofollow">Disclosure</a><a href="mailto:{EMAIL}">Contact</a></footer>'


def generate(root: Path) -> int:
    tools = json.loads((root / "data/tools.json").read_text())
    n = len(tools)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Press and citation page for AIToolsEssentials: independently verified AI tool pricing, keep/cut guidance, and editorial rules. No pay-to-rank."><title>Press — cite AIToolsEssentials</title><link rel="canonical" href="{DOMAIN}/press/"><meta property="og:title" content="Press — AIToolsEssentials"><meta property="og:description" content="Cite independently verified AI tool pricing and keep/cut guidance. Editorial scores cannot be bought."><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg"><link rel="stylesheet" href="/css/styles.css"><link rel="stylesheet" href="/css/share.css"><script type="application/ld+json">{{"@context":"https://schema.org","@type":"AboutPage","name":"AIToolsEssentials Press","url":"{DOMAIN}/press/","publisher":{{"@type":"Organization","name":"AIToolsEssentials","url":"{DOMAIN}","email":"{EMAIL}"}}}}</script></head><body>{HEADER}<main>
<section class="scene scene-dark"><div class="methodology-hero"><p class="kicker">Press &amp; citations</p><h1>Cite the pricing, not the hype.</h1><p class="subhead">AIToolsEssentials is an independent directory of {n} AI tools. We publish checked dates on pricing, keep/cut guidance for overlapping subscriptions, and honest “not worth it” sections. Rankings cannot be bought.</p><p><a class="button button-blue" href="/pricing-watch/">Pricing Watch</a><a class="button button-dark" href="/methodology/">Editorial rules</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">
<section class="methodology-block"><span class="kicker light">Boilerplate</span><h2>One paragraph you can paste.</h2><p>AIToolsEssentials (aitoolsessentials.com) independently reviews AI tools with pricing verified from official vendor pages and dated on every snapshot. Coverage includes head-to-head comparisons, “is it worth it” guides, and keep/cut advice for overlapping subscriptions. Affiliate and sponsored relationships are labeled and do not change editorial scores.</p></section>
<section class="methodology-block"><span class="kicker light">Cite these pages</span><h2>Use the source pages, not a homepage screenshot.</h2><ul>
<li><a href="/pricing-watch/">Pricing Watch</a> — dated snapshots and the change log</li>
<li><a href="/methodology/">Editorial methodology</a> — how scores, sources, and freshness work</li>
<li><a href="/evidence/">Evidence ledger</a> — official pricing, docs, privacy, and rights links per tool</li>
<li><a href="/comparisons/">Comparisons</a> — head-to-head matchups</li>
<li><a href="/articles/">Guides</a> — worth-it and keep/cut articles</li>
<li><a href="/badges/">Vendor badges</a> — embeddable “Reviewed on AIToolsEssentials” SVGs</li>
</ul></section>
<section class="methodology-block"><span class="kicker light">What we will not claim</span><h2>No invented traffic, rankings, or lab tests.</h2><p>We do not publish fabricated visitor counts, search rankings, or hands-on scores we did not run. Community reports stay labeled as individual experience. If a price or model version is not on an official page with a checked date, we mark it unresolved.</p></section>
<section class="score-card methodology-next"><span>Contact</span><h2>Corrections, citations, and interviews</h2><p>Editorial corrections, citation questions, and interview requests: <a href="mailto:{EMAIL}">{EMAIL}</a>. Tool submissions go through <a href="/submit-tool.html">Submit a tool</a>. Sponsorships are labeled and never buy a ranking — see <a href="/advertise/">Advertise</a>.</p></section>
</div></section>
</main>{FOOTER}<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script></body></html>'''
    out = root / "press" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    return 1


if __name__ == "__main__":
    print(generate(Path(__file__).resolve().parent.parent))
