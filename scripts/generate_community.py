#!/usr/bin/env python3
"""Generate an honest community page without fabricated traffic or vote counts."""
import json
from pathlib import Path


def generate(root: Path, tools: list, today: str) -> Path:
    top = sorted(tools, key=lambda t: (-float(t.get('rating', 0)), t['name']))[:10]
    cards = ''
    for i, tool in enumerate(top, 1):
        cards += f'''<article class="directory-card">
<div><span class="category-pill">Editorial #{i} · {tool.get('rating')}/5</span><h3><a href="tools/{tool['slug']}/">{tool['name']}</a></h3><p>{tool.get('best_for','')}</p></div>
<div class="card-actions"><a class="text-link" href="tools/{tool['slug']}/">Read review</a><a class="button button-blue small" href="tools/{tool['slug']}/">See evidence</a></div>
</article>'''
    html = f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="AIToolsEssentials community submissions and the current evidence-based editorial shortlist. No fabricated vote or traffic counts.">
<title>Community Picks &amp; Editorial Shortlist — AIToolsEssentials</title>
<link rel="canonical" href="https://aitoolsessentials.com/leaderboard.html">
<link rel="stylesheet" href="css/styles.css"><link rel="stylesheet" href="css/share.css"></head><body>
<header class="global-nav"><a class="brand" href="index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="tools/index.html">Tools</a><a href="comparisons/best-ai-tools.html">Best AI tools</a><a href="categories/index.html">Categories</a><a href="articles/index.html">Guides</a><a href="benchmarks/">Benchmarks</a></nav><a class="nav-cta" href="legal/affiliate-disclosure.html">Disclosure</a></header>
<section class="review-hero scene scene-light"><p class="kicker light">Community</p><h1>Community picks—without fake popularity numbers.</h1><p>Voting will open after we have enough verified submissions to make the result meaningful. Until then, this page shows the current editorial shortlist and labels it clearly.</p><p class="last-updated">Editorial shortlist updated {today} · Community vote count: not yet published</p><div class="actions"><a class="button button-blue" href="submit-tool.html">Submit a tool</a><a class="button button-dark" href="legal/editorial-methodology.html">How rankings work</a></div></section>
<section class="directory-section scene scene-light"><div class="section-title"><p class="kicker light">Current shortlist</p><h2>Highest editorial scores</h2><p>These positions come from AIToolsEssentials editorial ratings—not votes, traffic, sponsorships, or affiliate relationships.</p></div><div class="directory-grid">{cards}</div></section>
<section class="benchmark-policy"><div><h2>When community voting opens</h2><p>We will publish the verified submission count, eligibility rules, anti-spam controls, reset schedule, and actual vote totals. Until that system has real data, we will not simulate engagement.</p></div></section>
<footer class="footer"><span>© {today[:4]} AIToolsEssentials</span><a href="advertise/index.html" rel="nofollow">Advertise</a><a href="submit-tool.html" rel="nofollow">Submit a tool</a><a href="legal/editorial-methodology.html">Methodology</a><a href="mailto:contact@aitoolsessentials.com">Contact</a></footer><section class="directory-section scene scene-light" id="community-report-queue"><div class="section-title"><p class="kicker light">Report queue</p><h2>Verified community results will publish here</h2><p>When community test reports arrive via the <a href="community/test-report.html">report form</a>, each one is checked against our testing protocol, then listed below with the reporter's role, tool version, and dated result. Nothing is published unverified.</p></div><div class="content-hub-grid"><article class="content-hub-card"><h3>Queue status</h3><p>0 reports pending verification · 0 published. First verified reports get featured on this page and credited.</p></article><article class="content-hub-card"><h3>How to get featured</h3><p>Submit a structured result: tool + plan, your task, time spent, what worked/failed. Vague "it's great" notes don't clear verification.</p></article></div></section><script src="js/site.js" defer></script><script src="js/analytics.js" defer></script></body></html>'''
    out = root / 'leaderboard.html'; out.write_text(html); return out


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    tools = json.loads((root/'data/tools.json').read_text())
    from datetime import date
    generate(root, tools, date.today().isoformat())
