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
    {
        "slug": "switch-from-elevenlabs-to-descript",
        "from_slug": "elevenlabs", "to_slug": "descript",
        "title": "Switching from ElevenLabs to Descript: voice and video workflow guide",
        "why": "If your work is podcast/video editing with occasional voiceover, Descript bundles transcription, editing, and overdub in one subscription. If you need the most natural standalone TTS at scale, ElevenLabs usually stays the better pick.",
        "carries": ["Scripts and transcripts import cleanly", "Both handle multitrack audio", "Team collaboration exists on both paid tiers"],
        "doesnt": ["Custom cloned voices do not transfer between platforms", "ElevenLabs' fine voice controls (stability/similarity) have no Descript equivalent", "API-based TTS pipelines must be rebuilt"],
        "cost_note": "Descript's creator tier covers editing plus limited overdub; ElevenLabs charges by character credits. Price YOUR monthly character/minute volume against both official pricing pages.",
        "test_plan": ["Clone nothing yet — test stock voices on one real episode/project.", "Compare output quality of the same 60-second script side by side.", "Only clone and migrate if quality holds; otherwise keep ElevenLabs for TTS and use Descript only for editing."],
    },
    {
        "slug": "switch-from-notion-ai-to-microsoft-copilot",
        "from_slug": "notion-ai", "to_slug": "microsoft-copilot",
        "title": "Switching from Notion AI to Microsoft Copilot: office-stack migration guide",
        "why": "If your organization already pays for Microsoft 365, Copilot rides on licenses you may already own — Word/Excel/Outlook integration beats a separate AI add-on for Office-centric teams.",
        "carries": ["Writing/editing assistance habits transfer directly", "Summarization workflows are similar", "Meeting-notes patterns map to Teams/Outlook equivalents"],
        "doesnt": ["Notion databases and pages stay in Notion — this is an add-on switch, not a data migration", "Notion Q&A across your workspace has no direct Copilot equivalent outside M365 files"],
        "cost_note": "Copilot requires Microsoft 365 seats plus its add-on price per user; Notion AI is a per-member add-on. Compare per-seat totals against what you already pay Microsoft.",
        "test_plan": ["Pilot with 2–3 power users for two weeks.", "Score where each assistant actually saves time: docs vs spreadsheets vs email vs wiki.", "Decide per-team, not company-wide — many orgs legitimately run both."],
    },
    {
        "slug": "switch-from-midjourney-to-leonardo-ai",
        "from_slug": "midjourney", "to_slug": "leonardo-ai",
        "title": "Switching from Midjourney to Leonardo AI: cost-control migration guide",
        "why": "Leonardo offers a free daily credit tier and API access that Midjourney lacks, making it attractive for product-shot pipelines and budget-conscious teams. The tradeoff is generally lower peak aesthetic quality.",
        "carries": ["Prompt-writing skills transfer almost fully", "Style references re-create with some tuning", "Upscaling workflows are similar"],
        "doesnt": ["Midjourney style codes (--sref) don't translate — rebuild reference sets", "Private generation defaults differ by plan", "Discord-native workflow habits don't apply"],
        "cost_note": "Leonardo's free tier gives daily credits; paid tiers undercut Midjourney's base plan for light users. Heavy aesthetic-driven creators often find Midjourney worth the premium — model your monthly image count first.",
        "test_plan": ["Recreate your 10 most-used prompts on identical settings.", "Blind-compare outputs before judging — brand aesthetics matter more than specs.", "Move production only if quality is acceptable to your audience, not just cheaper."],
    },
    {
        "slug": "switch-from-fireflies-to-otter-ai",
        "from_slug": "fireflies", "to_slug": "otter-ai",
        "title": "Switching from Fireflies.ai to Otter.ai: meeting-notes migration guide",
        "why": "Otter undercuts Fireflies on entry pricing and is strong for individual note-takers; Fireflies stays ahead for sales teams needing CRM sync and conversation intelligence. Switch only if your usage profile matches Otter's strengths.",
        "carries": ["Meeting platforms supported overlap heavily (Zoom/Meet/Teams)", "Transcript search habits carry over", "Highlight/comment workflows are similar"],
        "doesnt": ["Historical transcripts do not export wholesale between platforms", "Fireflies' CRM integrations (HubSpot/Salesforce) have no Otter equivalent", "Soundbites/clips metadata stays behind"],
        "cost_note": "Otter Pro runs well below Fireflies' business tiers for individuals. Teams relying on revenue-intelligence features should price the cost of losing them, not just the subscription delta.",
        "test_plan": ["Run Otter alongside Fireflies on one week of real meetings — never switch blind.", "Grade transcript accuracy on your industry vocabulary and accents specifically.", "Export anything you must keep from Fireflies before cancelling."],
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
        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": "What transfers when switching?", "acceptedAnswer": {"@type": "Answer", "text": ". ".join(g["carries"])}},
                {"@type": "Question", "name": "What does not transfer?", "acceptedAnswer": {"@type": "Answer", "text": ". ".join(g["doesnt"])}},
            ],
        }
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
        html = html.replace("__FAQ_SCHEMA__", json.dumps(faq_schema, separators=(",", ":")))
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


def postprocess(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    """Re-inject switch-guide modules into review pages + alternatives hub after regeneration."""
    import re as _re
    if tools is None:
        tools = json.loads((root / "data/tools.json").read_text())
    pairs = {
        "chatgpt": ("claude", "Switching from ChatGPT to Claude?", "Read our honest migration guide — what transfers, cost math, first-week test plan.", "/guides/switch-guides/switch-from-chatgpt-to-claude.html"),
        "claude": ("chatgpt", "Thinking of switching from ChatGPT?", "See what carries over, what breaks, and how to test before cancelling anything.", "/guides/switch-guides/switch-from-chatgpt-to-claude.html"),
        "jasper": ("copy-ai", "Considering Copy.ai instead?", "Our Jasper → Copy.ai switch guide covers pricing math and a two-week test plan.", "/guides/switch-guides/switch-from-jasper-to-copy-ai.html"),
        "copy-ai": ("jasper", "Coming from Jasper?", "See what re-creates easily and what (Brand Voice) needs rebuilding in our switch guide.", "/guides/switch-guides/switch-from-jasper-to-copy-ai.html"),
        "zapier-ai": ("make", "Considering Make instead?", "Our Zapier → Make guide shows when the operations math actually favors switching.", "/guides/switch-guides/switch-from-zapier-to-make.html"),
        "make": ("zapier-ai", "Migrating from Zapier?", "What imports, what you rebuild, and a one-Zap-first test plan in our switch guide.", "/guides/switch-guides/switch-from-zapier-to-make.html"),
        "elevenlabs": ("descript", "Evaluating Descript for editing?", "Voice stays ours; editing may belong elsewhere — see the ElevenLabs → Descript switch guide.", "/guides/switch-guides/switch-from-elevenlabs-to-descript.html"),
        "fireflies": ("otter-ai", "Considering Otter.ai?", "Cheaper for individuals, weaker for sales teams — read the Fireflies → Otter switch guide first.", "/guides/switch-guides/switch-from-fireflies-to-otter-ai.html"),
    }
    n = 0
    for slug, (other, h, txt, url) in pairs.items():
        rp = root / f"tools/{slug}/index.html"
        if not rp.exists():
            continue
        s = rp.read_text()
        block = ('<!-- AIT SWITCH GUIDE START --><section class="score-card" style="margin:26px auto 0;max-width:880px">'
                 f'<span>Migration guide</span><h3>{esc(h)}</h3><p>{esc(txt)}</p>'
                 f'<p><a href="{url}">Read the switch guide →</a></p></section><!-- AIT SWITCH GUIDE END -->')
        if "<!-- AIT SWITCH GUIDE START -->" in s:
            s = _re.sub(r"<!-- AIT SWITCH GUIDE START -->.*?<!-- AIT SWITCH GUIDE END -->", lambda _m: block, s, flags=_re.S)
        else:
            idx = s.rfind("</main>")
            s = s[:idx] + block + "\n" + s[idx:]
        rp.write_text(s)
        n += 1
    ah = root / "alternatives/index.html"
    if ah.exists():
        s = ah.read_text()
        if "/guides/switch-guides/" not in s:
            mod = ('<section class="score-card" style="margin:26px auto 0;max-width:880px"><span>Already subscribed?</span>'
                   '<h3>Switch guides</h3><p>Moving between tools? See what transfers, real cost math, and test plans.</p>'
                   '<p><a href="/guides/switch-guides/">Browse all switch guides →</a></p></section>')
            i = s.rfind("</main>")
            ah.write_text(s[:i] + mod + "\n" + s[i:])
    return n


if __name__ == "__main__":
    root0 = Path(__file__).resolve().parent.parent
    print(generate(root0))
    print("postprocess:", postprocess(root0))
