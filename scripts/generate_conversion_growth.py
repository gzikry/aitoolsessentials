#!/usr/bin/env python3
"""Generate distribution, conversion, and trust growth surfaces."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
HEADER = '<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/stack-builder.html">Stack builder</a><a href="/tool-finder.html">Tool finder</a><a href="/free-ai-tools.html">Free AI tools</a><a href="/alternatives/">Alternatives</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/articles/index.html">Guides</a><a href="/deals/">Deals</a></nav><a class="nav-cta" href="/pricing/">Premium</a></header>'
FOOTER = f'<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/advertise/index.html" rel="nofollow">Advertise</a><a href="/submit-tool.html" rel="nofollow">Submit a tool</a><a href="/community/test-report.html" rel="nofollow">Report your results</a><a href="/badges/">Badges</a><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a></footer>'

ALT_DEFS = {
    "chatgpt": ["claude", "gemini", "perplexity", "deepseek", "mistral-le-chat"],
    "claude": ["chatgpt", "gemini", "perplexity", "mistral-le-chat", "deepseek"],
    "gemini": ["chatgpt", "claude", "perplexity", "microsoft-copilot"],
    "jasper": ["copy-ai", "chatgpt", "claude", "grammarly", "canva-ai"],
    "zapier-ai": ["make", "n8n", "airtable-ai", "slack-ai"],
    "make": ["zapier-ai", "n8n", "airtable-ai", "slack-ai"],
    "midjourney": ["leonardo-ai", "adobe-firefly", "canva-ai"],
    "canva-ai": ["adobe-firefly", "leonardo-ai", "midjourney"],
    "perplexity": ["you-com", "claude", "chatgpt", "gemini"],
    "notion-ai": ["airtable-ai", "slack-ai", "microsoft-copilot", "chatgpt"],
    "elevenlabs": ["descript", "heygen", "synthesia", "allvideoai"],
    "descript": ["elevenlabs", "allvideoai", "heygen", "synthesia"],
    "github-copilot": ["cursor", "replit-ai", "v0", "bolt-new", "lovable"],
    "replit-ai": ["cursor", "github-copilot", "bolt-new", "v0"],
    "grammarly": ["chatgpt", "claude", "jasper", "copy-ai"],
    "runway": ["allvideoai", "heygen", "synthesia", "descript"],
    "synthesia": ["heygen", "allvideoai", "descript", "elevenlabs"],
    "cursor": ["github-copilot", "replit-ai", "v0", "bolt-new", "lovable"],
    "n8n": ["zapier-ai", "make", "airtable-ai"],
    "adobe-firefly": ["midjourney", "leonardo-ai", "canva-ai"],
    "leonardo-ai": ["midjourney", "adobe-firefly", "canva-ai"],
    "bolt-new": ["lovable", "v0", "replit-ai", "cursor"],
    "lovable": ["bolt-new", "v0", "replit-ai", "cursor"],
    "v0": ["bolt-new", "lovable", "cursor", "github-copilot"],
    "deepseek": ["chatgpt", "claude", "gemini", "grok"],
    "grok": ["chatgpt", "claude", "gemini", "deepseek"],
    "meta-ai": ["chatgpt", "grok", "gemini", "claude"],
    "mistral-le-chat": ["chatgpt", "claude", "deepseek", "gemini"],
    "copy-ai": ["jasper", "chatgpt", "claude", "grammarly"],
    "fathom": ["fireflies", "otter-ai", "notion-ai"],
    "fireflies": ["otter-ai", "fathom", "notion-ai"],
    "otter-ai": ["fireflies", "fathom", "notion-ai"],
    "poe": ["chatgpt", "perplexity", "claude", "gemini"],
    "gamma": ["canva-ai", "notion-ai", "chatgpt"],
    "airtable-ai": ["notion-ai", "make", "zapier-ai"],
    "microsoft-copilot": ["chatgpt", "gemini", "claude", "notion-ai"],
    "slack-ai": ["notion-ai", "microsoft-copilot", "fathom"],
    "you-com": ["perplexity", "chatgpt", "poe", "claude"],
    "heygen": ["synthesia", "runway", "allvideoai"],
    "allvideoai": ["runway", "descript", "synthesia", "heygen"],
}


def esc(s: Any) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def head(title: str, desc: str, canonical: str) -> str:
    return f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{esc(desc)}"><title>{esc(title)}</title><link rel="canonical" href="{canonical}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/css/styles.css"></head>'


def scripts(extra: str = "") -> str:
    return extra + '<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>'


def by_slug(tools: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {t["slug"]: t for t in tools}


def tool_card(t: dict[str, Any], note: str = "") -> str:
    note_html = f'<p><strong>Why compare:</strong> {esc(note)}</p>' if note else ""
    return f'<article class="content-hub-card"><span>{esc(t.get("category"))} · {esc(t.get("price"))}</span><h3><a href="/tools/{t["slug"]}/">{esc(t["name"])}</a></h3><p>{esc(t.get("summary", ""))}</p>{note_html}<p><strong>Best for:</strong> {esc(t.get("best_for", ""))}</p><a class="button button-blue small" href="/tools/{t["slug"]}/">Read review</a></article>'


def generate_alternative_pages(root: Path, tools: list[dict[str, Any]]) -> None:
    tools_by_slug = by_slug(tools)
    out = root / "alternatives"
    out.mkdir(exist_ok=True)
    index_links = []
    for primary_slug, alt_slugs in ALT_DEFS.items():
        if primary_slug not in tools_by_slug:
            continue
        primary = tools_by_slug[primary_slug]
        alts = [tools_by_slug[s] for s in alt_slugs if s in tools_by_slug]
        title = f"Best {primary['name']} alternatives"
        desc = f"Compare {primary['name']} alternatives by workflow fit, pricing model, best use case, and review evidence before switching tools."
        cards = "".join(tool_card(t, f"Consider this when {primary['name']} is too expensive, too broad, or not the right workflow fit.") for t in alts)
        page = f'<!doctype html><html lang="en">{head(title+" | AIToolsEssentials", desc, DOMAIN+"/alternatives/"+primary_slug+"-alternatives.html")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Alternatives guide</p><h1>{esc(title)}</h1><p class="subhead">{esc(desc)}</p><p><a class="button button-blue" href="/tools/{primary_slug}/">Read {esc(primary["name"])} review</a><a class="button button-blue" href="/compare-shortlist.html" style="margin-left:8px">Compare shortlist</a></p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Quick verdict</span><p>If {esc(primary["name"])} is not the right fit, start by comparing cost, data policy, workflow depth, and whether you need a specialist tool or a general assistant.</p></div><div class="content-hub-grid">{cards}</div><h2>How to choose</h2><div class="content-hub-grid"><article class="content-hub-card"><h3>Choose by workflow</h3><p>Pick the tool that matches the job you do weekly, not the tool with the longest feature list.</p></article><article class="content-hub-card"><h3>Compare upgrade pressure</h3><p>Free tiers are useful for testing, but team features, limits, and exports often determine the real cost.</p></article></div></div></section></main>{FOOTER}{scripts()}</body></html>'
        (out / f"{primary_slug}-alternatives.html").write_text(page)
        index_links.append(f'<article class="content-hub-card"><span>Alternatives</span><h3><a href="/alternatives/{primary_slug}-alternatives.html">{esc(title)}</a></h3><p>{esc(desc)}</p><a class="button button-blue small" href="/alternatives/{primary_slug}-alternatives.html">Compare alternatives</a></article>')
    # Add an index section to the existing alternatives hub without replacing the generated hub.
    hub = out / "index.html"
    if hub.exists() and "AIT INDIVIDUAL ALTERNATIVES START" not in hub.read_text():
        html = hub.read_text()
        block = f'\n<!-- AIT INDIVIDUAL ALTERNATIVES START -->\n<section style="margin:54px 0"><h2>Individual alternatives guides</h2><div class="content-hub-grid">{"".join(index_links)}</div></section>\n<!-- AIT INDIVIDUAL ALTERNATIVES END -->\n'
        html = html.replace("</main>", block + "</main>", 1)
        hub.write_text(html)


def generate_get_reviewed(root: Path) -> None:
    page = f'<!doctype html><html lang="en">{head("Get Reviewed on AIToolsEssentials", "Submit an AI tool for editorial review consideration, badge eligibility, and sponsorship discussion without affecting editorial scores.", DOMAIN+"/get-reviewed/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Vendor review funnel</p><h1>Get reviewed without buying the verdict.</h1><p class="subhead">Vendors can submit tools, corrections, and sponsorship inquiries. Editorial scores stay separate from paid visibility.</p><p><a class="button button-blue" href="/submit-tool.html">Submit a tool</a><a class="button button-blue" href="/advertise/" style="margin-left:8px">See sponsor options</a></p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid"><article class="content-hub-card"><h3>What helps review</h3><p>Official pricing, docs, trial access information, security/privacy pages, and clear buyer use cases.</p></article><article class="content-hub-card"><h3>What does not affect score</h3><p>Paid sponsorship, affiliate relationships, vendor pressure, or badge usage never changes editorial scoring.</p></article><article class="content-hub-card"><h3>After review</h3><p>Reviewed tools may link to their page using transparent badges. Sponsored placements are separately labeled.</p></article></div><div class="score-card"><span>Vendor checklist</span><ul><li>Submit the official URL and category.</li><li>Include pricing and documentation links.</li><li>Tell us the ideal buyer and main limitation.</li><li>Use the badges page only after a review is published.</li></ul><p><a class="button button-blue" href="/badges/">View badge rules</a></p></div></div></section></main>{FOOTER}{scripts()}</body></html>'
    out = root / "get-reviewed" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)


def generate_changelog(root: Path, tools: list[dict[str, Any]], today: str) -> None:
    page = f'<!doctype html><html lang="en">{head("AIToolsEssentials Editorial Changelog", "Track major AIToolsEssentials updates: new tools, stack pages, growth utilities, pricing assets, review modules, and trust improvements.", DOMAIN+"/changelog/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Editorial changelog</p><h1>What changed on AIToolsEssentials.</h1><p class="subhead">A transparent log of major site, review, monetization, and utility updates.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell"><div class="timeline"><article class="score-card"><span>{today}</span><h2>Viral utility expansion</h2><p>Added downloadable stack cards, individual stack pages, shortlist comparison, deals/free-trials hub, and review-page stack modules.</p></article><article class="score-card"><span>{today}</span><h2>Directory coverage</h2><p>{len(tools)} AI tools tracked with generated reviews, category pages, structured data, and sitemap coverage.</p></article><article class="score-card"><span>Ongoing</span><h2>Correction policy</h2><p>Readers and vendors can submit pricing, feature, and policy corrections. Submissions are verified before pages change.</p></article></div></div></section></main>{FOOTER}{scripts()}</body></html>'
    out = root / "changelog" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)


USE_CASE_DEFS = [
    ("best-ai-tools-for-content-creators", "Best AI tools for content creators", ["Creative", "Audio", "Video", "Marketing"], "Plan, create, edit, voice, and repurpose content with a practical AI creator stack."),
    ("best-ai-tools-for-research", "Best AI tools for research", ["Research", "General AI Assistant"], "Find source-backed AI tools for research, synthesis, citations, and document analysis."),
    ("best-ai-tools-for-meetings", "Best AI tools for meetings", ["Meetings", "Audio"], "Compare AI meeting tools for transcription, summaries, action items, and follow-up."),
    ("best-ai-tools-for-automation", "Best AI tools for automation", ["Automation"], "Build workflows, lead routing, internal operations, and AI-assisted automations."),
    ("best-ai-tools-for-coding", "Best AI tools for coding", ["Development"], "Compare AI coding assistants, app builders, IDE copilots, and prototyping tools."),
    ("best-ai-tools-for-students", "Best AI tools for students", ["General AI Assistant", "Research", "Creative"], "Free-first AI tools for studying, research, presentations, notes, and responsible drafting."),
    ("best-ai-tools-for-marketers", "Best AI tools for marketers", ["Creative", "Marketing", "Writing", "Automation"], "AI tools for campaigns, copy, creative assets, research, and workflow automation."),
    ("best-ai-tools-for-sales-teams", "Best AI tools for sales teams", ["Automation", "Meetings", "Productivity"], "AI tools for call notes, lead follow-up, CRM workflows, and sales enablement."),
]

PROMOTION_TARGETS = [
    ("Product Hunt", "Launch as a free AI stack builder and AI tools directory."),
    ("Indie Hackers", "Share the build story and revenue-site angle."),
    ("r/artificial", "Soft-share the stack builder; avoid spammy affiliate framing."),
    ("r/Entrepreneur", "Position as a free AI stack/cost calculator for small businesses."),
    ("r/freelance", "Share the free AI stack for freelancers page."),
    ("LinkedIn", "Founder/operator post about reducing AI subscription sprawl."),
    ("X/Twitter", "Thread: the practical free-first AI stack by role."),
    ("AI newsletters", "Pitch the Stack Builder + cost calculator as a free utility."),
]

def generate_use_case_pages(root: Path, tools: list[dict[str, Any]]) -> None:
    out = root / "use-cases"
    out.mkdir(exist_ok=True)
    index_cards = []
    for slug, title, needles, desc in USE_CASE_DEFS:
        selected = []
        for t in tools:
            hay = (t.get("category", "") + " " + t.get("best_for", "") + " " + t.get("summary", "")).lower()
            if any(n.lower() in hay for n in needles):
                selected.append(t)
        selected = sorted(selected, key=lambda t: float(t.get("rating", 0) or 0), reverse=True)[:10]
        cards = "".join(tool_card(t) for t in selected)
        page = f'<!doctype html><html lang="en">{head(title+" | AIToolsEssentials", desc, DOMAIN+"/use-cases/"+slug+".html")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Use-case guide</p><h1>{esc(title)}</h1><p class="subhead">{esc(desc)}</p><p><a class="button button-blue" href="/stack-builder.html">Generate a stack</a><a class="button button-blue" href="/cost-calculator.html" style="margin-left:8px">Estimate cost</a></p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Decision framework</span><p>Start with a workflow you do every week, then compare cost, privacy posture, collaboration needs, and export limits before paying annually.</p></div><div class="content-hub-grid">{cards}</div><h2>Next steps</h2><div class="content-hub-grid"><article class="content-hub-card"><h3>Build a full stack</h3><p>Use the Stack Builder to combine tools across categories.</p><a class="button button-blue small" href="/stack-builder.html">Open Stack Builder</a></article><article class="content-hub-card"><h3>Compare cost</h3><p>Estimate the monthly cost before your tool stack sprawls.</p><a class="button button-blue small" href="/cost-calculator.html">Open calculator</a></article></div></div></section></main>{FOOTER}{scripts()}</body></html>'
        (out / f"{slug}.html").write_text(page)
        index_cards.append(f'<article class="content-hub-card"><span>Use case</span><h3><a href="/use-cases/{slug}.html">{esc(title)}</a></h3><p>{esc(desc)}</p><a class="button button-blue small" href="/use-cases/{slug}.html">Open guide</a></article>')
    index = f'<!doctype html><html lang="en">{head("AI Tool Use-Case Guides", "Browse AI tools by job to be done: content, research, meetings, automation, coding, students, marketing, and sales.", DOMAIN+"/use-cases/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Use cases</p><h1>Find AI tools by job, not hype.</h1><p class="subhead">Role and workflow-specific guides that route you to reviews, stacks, and cost checks.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{"".join(index_cards)}</div></div></section></main>{FOOTER}{scripts()}</body></html>'
    (out / "index.html").write_text(index)

def generate_launch_kit(root: Path) -> None:
    posts = {
        "Product Hunt tagline": "Find your practical AI stack by role, budget, and workflow.",
        "Product Hunt short description": "AIToolsEssentials helps people compare AI tools, generate shareable AI stacks, estimate subscription cost, and avoid paying for the wrong tools.",
        "Maker comment": "I built AIToolsEssentials because AI tool discovery is noisy. The site now includes reviewed tools, alternatives guides, a free-first stack builder, cost calculator, shortlist comparison, and transparent editorial policies.",
        "X thread opener": "Most people do not need more AI tools. They need the right stack for their actual workflow. I built a free AI Stack Builder to help with that:",
        "LinkedIn post": "AI subscription sprawl is real. AIToolsEssentials now lets you generate a role-specific AI stack, download a share card, estimate monthly cost, and compare alternatives before paying.",
        "Reddit post": "I made a free AI stack generator that suggests tools by role, budget, and workflow style. Would love feedback on what you would swap in the stacks.",
        "HN title": "Show HN: A free AI stack builder and cost calculator for choosing AI tools",
        "Pricing Watch — X post": "AI tools change prices quietly. We built a public tracker: every price tied to its official source with a checked date, changes logged as they happen. 40 tools, zero guesses. https://aitoolsessentials.com/pricing-watch/",
        "Pricing Watch — LinkedIn post": "Most teams discover AI price increases at renewal. AIToolsEssentials now publishes verified pricing snapshots for 40 AI tools, each traced to the vendor's official page with a checked date, plus a public change log when prices move. Free: https://aitoolsessentials.com/pricing-watch/",
        "Switch Guides — X post": "Thinking of switching from ChatGPT to Claude? Don't cancel anything yet. Our migration guides cover what transfers, what breaks, and a first-week test plan. 12 tool pairs: https://aitoolsessentials.com/guides/switch-guides/",
        "Switch Guides — Reddit post": "I wrote migration guides for switching between AI tools (ChatGPT→Claude, Zapier→Make, Midjourney→Leonardo, etc.) — what transfers vs what breaks, real cost math, and structured first-week test plans. Feedback welcome: https://aitoolsessentials.com/guides/switch-guides/",
    }
    cards = "".join(f'<article class="content-hub-card"><span>Launch copy</span><h3>{esc(k)}</h3><textarea readonly>{esc(v)}</textarea></article>' for k,v in posts.items())
    targets = "".join(f'<article class="content-hub-card"><h3>{esc(name)}</h3><p>{esc(note)}</p></article>' for name,note in PROMOTION_TARGETS)
    page = f'<!doctype html><html lang="en">{head("AIToolsEssentials Launch Kit", "Ready-to-use launch copy, channel positioning, and promotion targets for AIToolsEssentials.", DOMAIN+"/launch-kit/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Launch kit</p><h1>Promote the Stack Builder without starting from blank copy.</h1><p class="subhead">Ready-to-use Product Hunt, X, LinkedIn, Reddit, and newsletter copy for distribution.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><h2>Copy-ready launch assets</h2><div class="content-hub-grid">{cards}</div><h2>Promotion targets</h2><div class="content-hub-grid">{targets}</div><div class="score-card"><span>Recommended launch route</span><ol><li>Post the Stack Builder and free freelancer stack first.</li><li>Ask for swaps/feedback, not clicks.</li><li>Use traffic data to expand the winning stack/use-case pages.</li></ol></div></div></section></main>{FOOTER}{scripts()}</body></html>'
    out = root / "launch-kit" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)

def generate_feeds(root: Path, tools: list[dict[str, Any]], today: str) -> None:
    items = [
        ("AI Stack Builder", "/stack-builder.html", "Generate a shareable AI stack by role, budget, and workflow."),
        ("AI Tool Cost Calculator", "/cost-calculator.html", "Estimate monthly AI stack cost and find lower-cost swaps."),
        ("AI tools worth testing this week", "/weekly/", "Weekly public shortlist of tools worth testing."),
        ("Editorial changelog", "/changelog/", "Transparent update log for site and review improvements."),
        ("Get reviewed", "/get-reviewed/", "Vendor submission and editorial-boundary guide."),
        ("AI Pricing Watch", "/pricing-watch/", "Public tracker of verified AI pricing snapshots for 40 tools, with an automatic change log."),
        ("Switch Guides hub", "/guides/switch-guides/", "12 honest migration guides for switching between AI tools — what transfers, what breaks, cost math, test plans."),
        ("Switching from ChatGPT to Claude", "/guides/switch-guides/switch-from-chatgpt-to-claude.html", "Migration guide: what carries over, what breaks, and a first-week test plan."),
        ("Switching from Zapier to Make", "/guides/switch-guides/switch-from-zapier-to-make.html", "Task-based vs operation-based pricing, migration steps, and when the switch pays off."),
        ("ChatGPT vs Grok comparison", "/comparisons/chatgpt-vs-grok.html", "Head-to-head with current model lineups: GPT-5.4 family vs Grok 4.6/4.5/4.3/Build 0.1."),
        ("Claude vs Cursor comparison", "/comparisons/claude-vs-cursor.html", "Frontier assistant vs AI-native editor with Cursor Grok 4.6 and Composer 2.5."),
        ("Decision Brief generator", "/decision-brief.html", "Pick 2–3 tools and generate a shareable decision brief with overlap warnings and trial script."),
        ("Verified live deals", "/deals/", "Deals auto-verified from official vendor pricing pages with checked dates."),
        ("Free AI Stack Decision Checklist (PDF)", "/downloads/ai-stack-decision-checklist.html", "Printable worksheet for scoring overlap, cost, trial results, and cancellation risk before buying."),
        ("Grok review", "/tools/grok/", "Full review covering Grok 4.6, Grok Bot always-on agents, Grok Build, Imagine, Voice, and verified pricing."),
        ("Cursor review", "/tools/cursor/", "Review of Cursor's own model stack (Cursor Grok 4.6, Composer 2.5), agent modes, cloud agents, and Bugbot."),
        ("Premium research membership", "/premium/", "$12/mo decision briefs, CSV matrices, playbooks, and price-change alerts via Whop."),
        ("Benchmarks evidence hub", "/benchmarks/", "Versioned external benchmark snapshots with exact models, configurations, and dates."),
        ("Tool Finder", "/tool-finder.html", "Find AI tools by category, use case, budget, and free-tier availability."),
        ("Best AI tools hub", "/comparisons/best-ai-tools.html", "Editorial shortlist across categories with verified pricing."),
    ]
    def feed(title, link, desc, feed_items):
        rows = []
        for name, path, summary in feed_items:
            rows.append(f'<item><title>{esc(name)}</title><link>{DOMAIN}{path}</link><guid>{DOMAIN}{path}</guid><pubDate>{today} 12:00:00 -0700</pubDate><description>{esc(summary)}</description></item>')
        return f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{esc(title)}</title><link>{DOMAIN}{link}</link><description>{esc(desc)}</description>{"".join(rows)}</channel></rss>\n'
    (root / "feed.xml").write_text(feed("AIToolsEssentials updates", "/", "AI tools directory updates, stack utilities, and buyer guides.", items))
    (root / "weekly" / "feed.xml").write_text(feed("AIToolsEssentials weekly shortlist", "/weekly/", "Weekly AI tools worth testing.", [items[2]]))
    (root / "changelog" / "feed.xml").write_text(feed("AIToolsEssentials changelog", "/changelog/", "Editorial and product update log.", [items[3]]))

def postprocess_related_next_steps(root: Path) -> None:
    marker = "<!-- AIT RELATED NEXT STEPS START -->"
    targets = (list((root / "alternatives").glob("*-alternatives.html"))
               + list((root / "use-cases").glob("*.html"))
               + list((root / "stacks").glob("*.html"))
               + list((root / "comparisons").glob("*.html"))
               + [p for p in (root / "categories").glob("*/index.html")])
    for p in targets:
        if p == root / "categories" / "index.html":
            continue
        html = p.read_text()
        if marker in html:
            continue
        block = f'\n{marker}\n<section class="score-card related-next-steps"><span>Related next steps</span><h2>Turn this page into a decision.</h2><p><a class="button button-blue" href="/stack-builder.html">Generate stack</a><a class="button button-blue" href="/cost-calculator.html" style="margin-left:8px">Estimate cost</a><a class="button button-blue" href="/compare-shortlist.html" style="margin-left:8px">Compare shortlist</a></p></section>\n<!-- AIT RELATED NEXT STEPS END -->\n'
        html = html.replace("</main>", block + "</main>", 1)
        p.write_text(html)

def generate_js(root: Path) -> None:
    js = r'''
(function(){
function copy(text,btn){navigator.clipboard?.writeText(text).then(()=>{if(btn){btn.textContent='Copied ✓'; setTimeout(()=>btn.textContent=btn.dataset.label||'Copy',1600)}})}
function stackNames(){return [...document.querySelectorAll('#stackShareCard li')].map(li=>li.textContent.trim()).filter(Boolean)}
function stackTitle(){return document.querySelector('#stackShareCard h2')?.textContent.trim()||'My AI stack'}
function shareText(kind){const names=stackNames().join(' + '); const url=location.href; const title=stackTitle(); if(kind==='linkedin') return `I generated ${title}: ${names}. Built with AIToolsEssentials: ${url}`; if(kind==='reddit') return `I tried this AI stack generator and got: ${names}. What would you swap? ${url}`; if(kind==='email') return `Subject: AI stack idea\n\nI generated this AI stack: ${names}\n\nYou can customize it here: ${url}`; return `My AI stack: ${names}\nGenerate yours: ${url}`}
function scoreStack(){const card=document.getElementById('stackShareCard'); const host=document.getElementById('stackResult'); if(!card||!host||document.getElementById('stackScore'))return; const names=stackNames(); const cats=[...document.querySelectorAll('#stackResult .content-hub-card > span')].map(x=>x.textContent.split('·')[0].trim()); const unique=new Set(cats); const free=[...document.querySelectorAll('#stackResult .content-hub-card > span')].filter(x=>/free/i.test(x.textContent)).length; const score=Math.min(96,60+unique.size*7+free*3); const gaps=['Research','Automation','Creative','Meetings','Development'].filter(g=>![...unique].some(c=>c.toLowerCase().includes(g.toLowerCase()))); const html=`<div class="stack-score" id="stackScore"><span>AI Stack Score</span><strong>${score}/100</strong><p>Coverage: ${unique.size} categories · Free-first tools: ${free}/${names.length}</p><p>${gaps.length?'Possible gaps: '+gaps.join(', '):'Strong coverage across common workflows.'}</p></div>`; card.insertAdjacentHTML('afterend',html)}
function addShareCopyButtons(){const host=document.getElementById('stackResult'); if(!host||document.getElementById('shareCopyPanel'))return; const panel=document.createElement('div'); panel.className='share-copy-panel'; panel.id='shareCopyPanel'; panel.innerHTML='<span>Copy launch-ready share text</span><button class="button button-blue small" data-kind="x" data-label="Copy X post">Copy X post</button><button class="button button-blue small" data-kind="linkedin" data-label="Copy LinkedIn post">Copy LinkedIn post</button><button class="button button-blue small" data-kind="reddit" data-label="Copy Reddit post">Copy Reddit post</button><button class="button button-blue small" data-kind="email" data-label="Copy email">Copy email</button>'; host.appendChild(panel); panel.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>copy(shareText(b.dataset.kind),b)))}
function addFreeAlternatives(){if(!window.COST_TOOLS||!document.getElementById('costSummary')||document.getElementById('freeAltPanel'))return; const free=COST_TOOLS.filter(t=>/free/i.test(t.price||'')).slice(0,6); const panel=document.createElement('div'); panel.className='score-card free-alt-panel'; panel.id='freeAltPanel'; panel.innerHTML=`<span>Lower-cost swaps</span><h2>Try free tiers before paid stack sprawl.</h2><p>These tools have free or self-hosted starting points and can reduce early subscription risk.</p><div class="content-hub-grid">${free.map(t=>`<article class="content-hub-card"><span>${t.category} · ${t.price||''}</span><h3><a href="/tools/${t.slug}/">${t.name}</a></h3><p>${t.summary||''}</p><a class="button button-blue small" href="/tools/${t.slug}/">Read review</a></article>`).join('')}</div>`; document.getElementById('costSummary').after(panel)}
document.addEventListener('DOMContentLoaded',()=>{setTimeout(()=>{scoreStack();addShareCopyButtons();addFreeAlternatives()},50)});
})();
'''
    (root / "js" / "conversion.js").write_text(js)


def generate_css(root: Path) -> None:
    p = root / "css" / "styles.css"
    css = p.read_text()
    if "/* Conversion growth surfaces */" not in css:
        css += """

/* Conversion growth surfaces */
.stack-score { margin:18px 0; border:1px solid rgba(94,106,210,.22); border-radius:20px; padding:18px; background:linear-gradient(180deg,#fff,#eef0ff); box-shadow:0 18px 48px rgba(94,106,210,.12); }
.stack-score span, .share-copy-panel > span { display:block; color:#4f5cc8; text-transform:uppercase; letter-spacing:.12em; font-size:12px; font-weight:900; margin-bottom:8px; }
.stack-score strong { font-size:42px; color:#111827; }
.share-copy-panel { margin-top:22px; padding:18px; border-radius:18px; border:1px solid rgba(94,106,210,.18); background:#f7f8ff; display:flex; gap:10px; flex-wrap:wrap; align-items:center; }
.free-alt-panel { margin:26px 0; }
.conversion-verdict-bar { margin:24px 0; padding:18px; border-radius:18px; border:1px solid rgba(94,106,210,.18); background:linear-gradient(135deg,#eef0ff,#fff); display:grid; grid-template-columns:repeat(3,minmax(160px,1fr)); gap:12px; }
.conversion-verdict-bar strong { display:block; color:#111827; }
.correction-module { margin:34px auto; max-width:980px; }
@media (max-width: 800px) { .conversion-verdict-bar { grid-template-columns:1fr; } .share-copy-panel { display:grid; } }
"""
        p.write_text(css)


def inject_script(html: str) -> str:
    if "/js/conversion.js" in html:
        return html
    return html.replace("</body>", '<script src="/js/conversion.js" defer></script></body>', 1)


def postprocess(root: Path, tools: list[dict[str, Any]]) -> None:
    # Stack/cost pages: social copy, score, and free alternative JS.
    stack_page = root / "stack-builder.html"
    if stack_page.exists():
        stack_page.write_text(inject_script(stack_page.read_text()))

    cost_page = root / "cost-calculator.html"
    if cost_page.exists():
        html = inject_script(cost_page.read_text())
        if "AIT FREE ALT PANEL START" not in html:
            free = [t for t in tools if "free" in t.get("price", "").lower()][:6]
            cards = "".join(tool_card(t) for t in free)
            panel = f'\n<!-- AIT FREE ALT PANEL START -->\n<section class="score-card free-alt-panel"><span>Lower-cost swaps</span><h2>Try free tiers before paid stack sprawl.</h2><p>These tools have free or self-hosted starting points and can reduce early subscription risk.</p><div class="content-hub-grid">{cards}</div></section>\n<!-- AIT FREE ALT PANEL END -->\n'
            html = html.replace('<div id="costToolList"', panel + '<div id="costToolList"', 1)
        cost_page.write_text(html)

    for p in (root / "stacks").glob("*.html"):
        p.write_text(inject_script(p.read_text()))

    # Comparison verdict bars.
    marker = "<!-- AIT VERDICT BAR START -->"
    for p in (root / "comparisons").glob("*.html"):
        html = p.read_text()
        if marker in html:
            continue
        title = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        title_text = re.sub(r"<.*?>", "", title.group(1)).strip() if title else "this comparison"
        bar = f'\n{marker}\n<section class="conversion-verdict-bar"><div><span>Best first step</span><strong>Read the verdict</strong><p>Use this page to shortlist, then verify pricing.</p></div><div><span>Cost check</span><strong>Estimate stack cost</strong><p><a href="/cost-calculator.html">Open calculator</a></p></div><div><span>Decision loop</span><strong>Save contenders</strong><p><a href="/compare-shortlist.html">Compare shortlist</a></p></div></section>\n<!-- AIT VERDICT BAR END -->\n'
        html = html.replace("<main>", "<main>" + bar, 1) if "<main>" in html else html.replace("<body>", "<body>" + bar, 1)
        p.write_text(html)

    # Review correction/trust modules.
    corr_start = "<!-- AIT CORRECTION MODULE START -->"
    for t in tools:
        p = root / "tools" / t["slug"] / "index.html"
        if not p.exists():
            continue
        html = p.read_text()
        html = re.sub(r"\s*<!-- AIT CORRECTION MODULE START -->.*?<!-- AIT CORRECTION MODULE END -->\s*", "\n", html, flags=re.S)
        block = f'\n{corr_start}\n<section class="score-card correction-module"><span>Help keep this review accurate</span><h2>Pricing, features, or policy changed?</h2><p>Tell us what changed for {esc(t["name"])}. We verify corrections against official sources before updating reviews.</p><p><a class="button button-blue" href="/community/test-report.html">Submit user result</a><a class="button button-blue" href="/get-reviewed/" style="margin-left:8px">Vendor correction path</a></p></section>\n<!-- AIT CORRECTION MODULE END -->\n'
        html = html.replace("</main>", block + "</main>", 1)
        p.write_text(html)


    postprocess_related_next_steps(root)

def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    tools = tools or json.loads((root / "data/tools.json").read_text())
    today = today or datetime.today().strftime("%Y-%m-%d")
    generate_alternative_pages(root, tools)
    generate_use_case_pages(root, tools)
    generate_launch_kit(root)
    generate_get_reviewed(root)
    generate_changelog(root, tools, today)
    generate_feeds(root, tools, today)
    generate_js(root)
    generate_css(root)
    return 30


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    tools = json.loads((root / "data/tools.json").read_text())
    print(generate(root, tools))
    postprocess(root, tools)
