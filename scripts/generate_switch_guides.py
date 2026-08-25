#!/usr/bin/env python3
"""Generate switch-from migration guides (e.g., "Switching from ChatGPT to Claude").

High-intent SEO surface competitors don't cover: people who already pay for one tool
and are considering moving. Each guide covers what carries over, what doesn't, cost
math, and a first-week test plan — ending in our decision-brief/review CTAs.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

DOMAIN = "https://aitoolsessentials.com"

GUIDES = [
    {
        "slug": "switch-from-chatgpt-to-claude",
        "from_slug": "chatgpt", "to_slug": "claude",
        "title": "Switching from ChatGPT to Claude: the honest migration guide",
        "why": "Long-document analysis, careful tone, and coding review are Claude's strengths. If your work is long-form writing, contract/document review, or careful analysis, the switch often pays for itself.",
        "carries": ["Conversation habits (clear prompts work everywhere)", "Custom instructions map to Claude's Project instructions/styles", "File uploads work in both"],
        "doesnt": ["GPTs/custom GPT builds do not transfer", "DALL·E image generation has no Claude equivalent", "ChatGPT memory does not carry to Claude"],
        "cost_note": "Claude Pro is $17/mo billed annually ($20 monthly). ChatGPT Plus pricing varies by plan — check both official pages before cancelling anything.",
        "test_plan": ["Move ONE real weekly task (not everything) for 5 days.", "Compare editing burden and hallucination rate on the same source material.", "Check export/retention settings before uploading anything sensitive."],
    },
    {
        "slug": "switch-from-jasper-to-copy-ai",
        "from_slug": "jasper", "to_slug": "copy-ai",
        "title": "Switching from Jasper to Copy.ai: pricing-first migration guide",
        "why": "Copy.ai's chat/workflow model can cost less for teams that need volume generation rather than brand-voice depth. The tradeoff is less fine-grained brand voice control.",
        "carries": ["Campaign briefs and prompt libraries re-create quickly", "Team seats work similarly", "Both integrate with common marketing stacks"],
        "doesnt": ["Jasper Brand Voice training does not transfer — budget re-training time", "Campaign history exports may be partial"],
        "cost_note": "Copy.ai Chat starts ~$29/mo (billed annually options lower it); Growth tier is sales-assisted. Compare against your current Jasper tier at official pricing pages.",
        "test_plan": ["Recreate your top 3 content templates in Copy.ai.", "Run the same brief through both; score editing time honestly.", "Only cancel Jasper after two weeks of equal-or-better output."],
    },
    {
        "slug": "switch-from-zapier-to-make",
        "from_slug": "zapier-ai", "to_slug": "make",
        "title": "Switching from Zapier to Make: when the math actually works",
        "why": "Make charges per operation inside visual scenarios; multi-step workflows that burn Zapier tasks often run dramatically cheaper on Make.",
        "carries": ["App connections/auth re-authorize fresh", "Trigger/action logic maps to Make modules", "Webhooks supported on both"],
        "doesnt": ["Zaps do not import — you rebuild scenarios visually", "Filter/path logic differs and needs re-testing", "Task history does not transfer"],
        "cost_note": "Make Core runs roughly $12/mo at the 10k-operations tier. Model YOUR volume: count current Zapier tasks × steps before comparing sticker prices.",
        "test_plan": ["Pick your highest-volume Zap and rebuild it in Make.", "Track operations consumed for a week vs tasks burned on Zapier.", "Migrate the rest only if the math holds on real usage."],
    },
    {
        "slug": "switch-from-perplexity-to-you-com",
        "from_slug": "perplexity", "to_slug": "you-com",
        "title": "Switching from Perplexity to You.com: research workflow guide",
        "why": "You.com emphasizes customizable AI models and apps-style research. Worth testing if you want more control over which model answers your research queries.",
        "carries": ["Search-and-cite habits translate directly", "Browser/mobile workflows similar", "Prompt libraries carry over"],
        "doesnt": ["Perplexity Collections do not transfer", "Source-quality differences mean re-verifying citations initially"],
        "cost_note": "You.com offers free use with paid tiers for advanced models. Perplexity Pro pricing is on their official page — verify both before switching.",
        "test_plan": ["Run 10 real research questions through both in one week.", "Grade citation quality and follow-up depth.", "Keep whichever reduces verification time — not whichever is newer."],
    },
]


def esc(s: Any) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    if tools is None:
        tools = json.loads((root / "data/tools.json").read_text())
    today = today or datetime.today().strftime("%Y-%m-%d")
    by_slug = {t["slug"]: t for t in tools}

    out = root / "guides" / "switch-guides"
    out.mkdir(parents=True, exist_ok=True)

    cards = ""
    pages = []
    for g in GUIDES:
        frm, to = by_slug.get(g["from_slug"], {}), by_slug.get(g["to_slug"], {})
        url = f"{DOMAIN}/guides/switch-guides/{g['slug']}.html"
        cards += (f'<article class="content-hub-card"><span>Migration guide</span>'
                  f'<h3>{esc(frm.get("name", g["from_slug"]))} → {esc(to.get("name", g["to_slug"]))}</h3>'
                  f'<p>{esc(g["why"][:150])}…</p>'
                  f'<p><a href="/guides/switch-guides/{g["slug"]}.html">Read the switch guide →</a></p></article>')
        li = lambda items: "".join(f"<li>{esc(x)}</li>" for x in items)
        html = f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(g['title'])} — what transfers, what doesn't, cost math, and a first-week test plan.">
<title>{esc(g["title"])} — AIToolsEssentials</title>
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(g["title"])}"><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/css/styles.css"><link rel="stylesheet" href="/css/share.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":{json.dumps(g["title"])},"datePublished":"2026-08-24","author":{{"@type":"Organization","name":"AIToolsEssentials"}},"publisher":{{"@type":"Organization","name":"AIToolsEssentials"}}}}</script>
<script type="application/ld+json">__FAQ_SCHEMA__</script>

</head><body>
<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/alternatives/">Alternatives</a><a href="/decision-brief.html">Decision brief</a><a href="/resources/">Resources</a></nav><a class="nav-cta" href="/pricing/">Premium</a></header>
<main>
<section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:88px 28px 64px;text-align:center">
<p class="kicker">Migration guide · Updated {today}</p>
<h1>Switching from {esc(frm.get("name", g["from_slug"]))} to {esc(to.get("name", g["to_slug"]))}.</h1>
<p class="subhead">{esc(g["why"])}</p>
<p><a class="button button-blue" href="/tools/{esc(to.get('slug', g['to_slug']))}/">{esc(to.get("name", g["to_slug"]))} review</a><a class="button button-ghost-dark" href="/decision-brief.html?vs={g["from_slug"]},{g["to_slug"]}" style="margin-left:8px">Get a decision brief</a></p>
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide">

<div class="content-hub-grid">
<article class="content-hub-card"><h3>✓ What carries over</h3><ul style="padding-left:18px;margin:0">{li(g["carries"])}</ul></article>
<article class="content-hub-card"><h3>✗ What doesn't transfer</h3><ul style="padding-left:18px;margin:0">{li(g["doesnt"])}</ul></article>
</div>

<section class="score-card" style="margin-top:26px"><span>Cost reality</span><h3>Do the math before cancelling anything</h3><p>{esc(g["cost_note"])}</p></section>

<section class="score-card" style="margin-top:26px;border-left:4px solid #16a34a"><span>First-week test plan</span><h3>Migrate one task, not your whole workflow</h3><ol style="padding-left:20px;margin:0">{"".join(f"<li>{esc(x)}</li>" for x in g["test_plan"])}</ol></section>

<div class="table-wrap" style="margin-top:30px"><table>
<thead><tr><th></th><th>{esc(frm.get("name", g["from_slug"]))}</th><th>{esc(to.get("name", g["to_slug"]))}</th></tr></thead><tbody>
<tr><td><strong>Editorial score</strong></td><td>{esc(frm.get("rating", "—"))}/5</td><td>{esc(to.get("rating", "—"))}/5</td></tr>
<tr><td><strong>Pricing model</strong></td><td>{esc(frm.get("price") or frm.get("pricing") or "See review")}</td><td>{esc(to.get("price") or to.get("pricing") or "See review")}</td></tr>
<tr><td><strong>Best fit</strong></td><td>{esc(frm.get("best_for", ""))}</td><td>{esc(to.get("best_for", ""))}</td></tr>
<tr><td><strong>Full review</strong></td><td><a href="/tools/{g["from_slug"]}/">Read →</a></td><td><a href="/tools/{g["to_slug"]}/">Read →</a></td></tr>
</tbody></table></div>

<p class="affiliate-inline" style="margin-top:18px">Pricing changes often — every figure traces to the official vendor page dated on each linked review. Editorial scores are ours, not benchmarks.</p>
<p style="margin-top:14px;text-align:center"><a class="button button-ghost-dark" href="/alternatives/">Browse all alternatives guides →</a></p>
</div></section>
</main>
<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a><a href="/legal/corrections.html">Corrections</a><a href="mailto:contact@aitoolsessentials.com">Contact</a></footer>
<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>
</body></html>'''
        p = out / f"{g['slug']}.html"
        p.write_text(html)
        pages.append(p)

    # Hub page
    hub = f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Already paying for an AI tool and thinking of moving? Honest switch guides: what transfers, what doesn't, cost math, and a first-week test plan.">
<title>AI Tool Switch Guides — AIToolsEssentials</title>
<link rel="canonical" href="{DOMAIN}/guides/switch-guides/">
<link rel="stylesheet" href="/css/styles.css"><link rel="stylesheet" href="/css/share.css">
</head><body>
<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/alternatives/">Alternatives</a><a href="/resources/">Resources</a></nav><a class="nav-cta" href="/pricing/">Premium</a></header>
<main>
<section class="scene scene-dark"><div style="max-width:900px;margin:0 auto;padding:88px 28px 64px;text-align:center">
<p class="kicker">Switch guides</p><h1>Already paying? Switch smart, not fast.</h1>
<p class="subhead">Most migration articles are ads for the new tool. Ours tell you what breaks, what the math actually looks like, and how to test before you cancel anything.</p>
</div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{cards}</div></div></section>
</main>
<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a><a href="mailto:contact@aitoolsessentials.com">Contact</a></footer>
<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>
</body></html>'''
    (out / "index.html").write_text(hub)
    return len(pages) + 1


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    print(generate(root))
