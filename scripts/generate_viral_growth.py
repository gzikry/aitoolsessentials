#!/usr/bin/env python3
"""Generate viral/shareable growth utilities for AIToolsEssentials."""
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

STACK_PAGE_DEFS = [
    ("free-ai-stack-for-freelancers", "Free AI stack for freelancers", "freelancer", "free", "low-friction", "A practical free-first AI stack for solo freelancers and consultants who need research, drafting, design, automation, and meeting notes without subscription sprawl."),
    ("ai-stack-for-teachers", "AI stack for teachers", "teacher", "free", "low-friction", "A classroom-friendly AI stack for lesson planning, slides, research, visuals, and notes with free-tier tools first."),
    ("ai-stack-for-youtube-creators", "AI stack for YouTube creators", "creator", "balanced", "creative", "A creator stack for scripts, voice, editing, visuals, and repurposing video content into shareable assets."),
    ("ai-stack-for-small-business", "AI stack for small business", "small-business", "balanced", "low-friction", "A low-friction AI stack for small-business operations, intake, automation, internal docs, and client follow-up."),
    ("ai-stack-for-developers", "AI stack for developers", "developer", "balanced", "technical", "A builder-focused AI stack for coding, app scaffolding, UI generation, pair programming, and workflow automation."),
    ("ai-stack-for-researchers", "AI stack for researchers", "researcher", "free", "technical", "A source-first AI stack for research, synthesis, note capture, and writing support."),
    ("ai-stack-for-students", "AI stack for students", "teacher", "free", "low-friction", "A free-first student AI stack for studying, research, notes, presentations, and responsible drafting."),
    ("ai-stack-for-real-estate-agents", "AI stack for real estate agents", "small-business", "balanced", "low-friction", "A practical AI stack for listing copy, lead routing, follow-up reminders, visuals, and client communications."),

    ("ai-stack-for-marketers", "AI stack for marketers", "agency", "balanced", "creative", "A practical AI stack for campaign research, content production, creative assets, and marketing automation."),
    ("ai-stack-for-sales-teams", "AI stack for sales teams", "small-business", "balanced", "low-friction", "A sales-team AI stack for meeting notes, lead follow-up, prospect research, and lightweight automation."),
    ("ai-stack-for-recruiters", "AI stack for recruiters", "small-business", "balanced", "low-friction", "An AI stack for recruiters handling research, candidate notes, outreach drafts, scheduling summaries, and internal workflows."),
    ("ai-stack-for-lawyers", "AI stack for lawyers", "researcher", "balanced", "technical", "A careful AI stack for legal research support, document review, notes, and drafting workflows with human verification."),
    ("ai-stack-for-accountants", "AI stack for accountants", "small-business", "balanced", "technical", "An AI stack for accountants working with client notes, spreadsheet analysis, document drafting, and operations automation."),
    ("ai-stack-for-coaches", "AI stack for coaches", "freelancer", "balanced", "low-friction", "A coach-friendly AI stack for session notes, content, client follow-up, presentations, and lightweight automation."),
    ("ai-stack-for-podcasters", "AI stack for podcasters", "creator", "balanced", "creative", "An AI stack for podcasters handling recording notes, transcript editing, voice assets, clips, and repurposed content."),
    ("ai-stack-for-ecommerce-stores", "AI stack for ecommerce stores", "small-business", "balanced", "low-friction", "An ecommerce AI stack for product copy, support workflows, marketing assets, and operational automation."),
    ("ai-stack-for-startup-founders", "AI stack for startup founders", "small-business", "balanced", "technical", "A founder AI stack for research, prototypes, pitch assets, operations, and customer follow-up."),
    ("ai-stack-for-nonprofits", "AI stack for nonprofits", "freelancer", "free", "low-friction", "A free-first AI stack for nonprofits handling grant drafts, outreach, design, research, and meeting summaries."),
]


def esc(s: Any) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def head(title: str, desc: str, canonical: str) -> str:
    return f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{esc(desc)}"><title>{esc(title)}</title><link rel="canonical" href="{canonical}"><link rel="stylesheet" href="/css/styles.css"></head>'


def scripts(extra: str = "") -> str:
    return extra + '<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>'


def compact_tool(t: dict[str, Any]) -> dict[str, Any]:
    return {k: t.get(k) for k in ["slug", "name", "category", "best_for", "price", "rating", "summary"]}


def tool_card(t: dict[str, Any]) -> str:
    return f'<article class="content-hub-card"><span>{esc(t["category"])} · {esc(t.get("price", ""))}</span><h3><a href="/tools/{t["slug"]}/">{esc(t["name"])}</a></h3><p>{esc(t.get("summary", ""))}</p><p><strong>Best for:</strong> {esc(t.get("best_for", ""))}</p><a class="button button-blue small" href="/tools/{t["slug"]}/">Read review</a></article>'


def pick_stack(tools: list[dict[str, Any]], role: str, budget: str, vibe: str) -> list[dict[str, Any]]:
    by = {t["slug"]: t for t in tools}
    stacks = {
        "freelancer": ["chatgpt", "perplexity", "make", "canva-ai", "otter-ai"],
        "agency": ["jasper", "copy-ai", "canva-ai", "make", "descript"],
        "developer": ["cursor", "github-copilot", "claude", "replit-ai", "v0"],
        "teacher": ["chatgpt", "gamma", "canva-ai", "perplexity", "otter-ai"],
        "creator": ["descript", "elevenlabs", "canva-ai", "midjourney", "allvideoai"],
        "small-business": ["chatgpt", "make", "zapier-ai", "airtable-ai", "microsoft-copilot"],
        "researcher": ["perplexity", "claude", "you-com", "gemini", "notion-ai"],
    }
    slugs = list(stacks.get(role, stacks["freelancer"]))
    if budget == "free":
        slugs = [s for s in slugs if s in by and "free" in by[s].get("price", "").lower()] + [s for s in ["chatgpt", "claude", "gemini", "perplexity", "canva-ai", "n8n"] if s in by]
    if vibe == "technical":
        slugs = ["n8n", "cursor", "github-copilot", "claude", "airtable-ai"] + slugs
    if vibe == "low-friction":
        slugs = ["chatgpt", "canva-ai", "zapier-ai", "perplexity", "otter-ai"] + slugs
    seen: list[str] = []
    for slug in slugs:
        if slug in by and slug not in seen:
            seen.append(slug)
    return [by[s] for s in seen[:5]]


def stack_visual_card(title: str, role: str, budget: str, vibe: str, items: list[dict[str, Any]]) -> str:
    names = "".join(f'<li>{esc(t["name"])}</li>' for t in items)
    return f'<div class="stack-share-card" id="stackShareCard"><span>My AI Stack</span><h2>{esc(title)}</h2><p>{esc(role)} · {esc(budget)} · {esc(vibe)}</p><ol>{names}</ol><small>Generated by AIToolsEssentials</small></div>'


def generate_stack_builder(root: Path, tools: list[dict[str, Any]]) -> None:
    payload = json.dumps([compact_tool(t) for t in tools], separators=(",", ":"))
    default_stack = pick_stack(tools, "freelancer", "free", "low-friction")
    default_cards = "".join(tool_card(t) for t in default_stack)
    default_share = stack_visual_card("Freelancer free-first stack", "freelancer", "free", "low-friction", default_stack)
    default_result = f'<span>Your shareable stack</span><h2>freelancer · free · low-friction</h2>{default_share}<p class="actions"><button class="button button-blue" id="downloadStackCard">Download card</button><button class="button button-blue" id="shareNative">Share stack</button><a class="button button-blue" href="/cost-calculator.html">Estimate cost</a></p><div class="content-hub-grid">{default_cards}</div>'
    extra_js = '<script>const TOOLS='+payload+';</script><script src="/js/viral.js" defer></script>'
    page = f'<!doctype html><html lang="en">{head("AI Stack Builder — Generate Your Shareable AI Stack | AIToolsEssentials", "Generate a personalized AI tools stack for your role, budget, and workflow. Share your stack with a link and downloadable card.", DOMAIN+"/stack-builder.html")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:900px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Shareable AI stack generator</p><h1>Generate the AI stack you would actually use.</h1><p class="subhead">Pick your role, budget, and workflow style. Get a clean stack you can copy, save, download, or share.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card viral-control"><span>Build your stack</span><div class="viral-controls"><label>Role<select id="role"><option value="freelancer">Freelancer / consultant</option><option value="agency">Agency / marketer</option><option value="developer">Developer / builder</option><option value="teacher">Teacher / educator</option><option value="creator">Creator / YouTuber</option><option value="small-business">Small business / ops</option><option value="researcher">Researcher / analyst</option></select></label><label>Budget<select id="budget"><option value="free">Free-first</option><option value="balanced">Balanced</option><option value="premium">Premium OK</option></select></label><label>Style<select id="vibe"><option value="low-friction">Low-friction</option><option value="technical">Technical/control</option><option value="creative">Creative-heavy</option></select></label></div><div class="actions" style="margin-top:18px"><button class="button button-blue" id="generateStack">Generate stack</button><button class="button button-blue" id="copyStack">Copy share link</button></div></div><div id="stackResult" class="viral-result-card">{default_result}</div></div></section></main>{FOOTER}{scripts(extra_js)}</body></html>'
    (root / "stack-builder.html").write_text(page)


def generate_stack_pages(root: Path, tools: list[dict[str, Any]]) -> str:
    outdir = root / "stacks"
    outdir.mkdir(exist_ok=True)
    index_cards: list[str] = []
    for slug, title, role, budget, vibe, desc in STACK_PAGE_DEFS:
        items = pick_stack(tools, role, budget, vibe)
        cards = "".join(tool_card(t) for t in items)
        share = stack_visual_card(title, role, budget, vibe, items)
        viral_js = '<script src="/js/viral.js" defer></script>'
        page = f'<!doctype html><html lang="en">{head(title+" | AIToolsEssentials", desc, DOMAIN+"/stacks/"+slug+".html")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Shareable AI stack</p><h1>{esc(title)}</h1><p class="subhead">{esc(desc)}</p><p><a class="button button-blue" href="/stack-builder.html">Customize this stack</a><a class="button button-blue" href="/cost-calculator.html" style="margin-left:8px">Estimate cost</a></p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="stack-layout"><div>{share}<p class="actions"><button class="button button-blue" data-download-stack>Download stack card</button><button class="button button-blue" data-copy-stack>Copy link</button></p></div><div><h2>Recommended tools</h2><div class="content-hub-grid">{cards}</div></div></div><div class="score-card"><span>How to use this stack</span><p>Start with the free or lowest-friction tool in each category, then upgrade only when a bottleneck is proven. Read each review before connecting business data or paying annually.</p></div></div></section></main>{FOOTER}{scripts(viral_js)}</body></html>'
        (outdir / f"{slug}.html").write_text(page)
        index_cards.append(f'<article class="content-hub-card"><span>{esc(role)} · {esc(budget)}</span><h3><a href="/stacks/{slug}.html">{esc(title)}</a></h3><p>{esc(desc)}</p><a class="button button-blue small" href="/stacks/{slug}.html">Open stack</a></article>')
    return "".join(index_cards)


def generate_stack_gallery(root: Path, tools: list[dict[str, Any]]) -> None:
    seed = [
        ("Solo consultant admin stack", "freelancer", "Free-first tools for drafting, research, automation, visuals, and meeting notes."),
        ("Teacher free-tier classroom stack", "teacher", "A practical stack for lesson planning, slides, research, visuals, and meeting notes."),
        ("Creator repurposing stack", "creator", "Voice, video, short clips, visuals, and script support for creators."),
        ("Developer shipping stack", "developer", "Coding assistant, app builder, pair-programming, and UI generation stack."),
        ("Small business operations stack", "small-business", "Lightweight tools for admin, CRM, automation, internal docs, and client workflows."),
        ("Research analyst stack", "researcher", "Source-backed search, long-document synthesis, notes, and writing support."),
    ]
    seo_cards = generate_stack_pages(root, tools)
    sections = ""
    for title, role, desc in seed:
        items = pick_stack(tools, role, "free" if "free" in title.lower() else "balanced", "low-friction")
        sections += f'<section class="stack-gallery-block"><div><h2>{esc(title)}</h2><p>{esc(desc)}</p><p><a class="button button-blue small" href="/stack-builder.html">Build a similar stack</a></p></div><div class="content-hub-grid">{"".join(tool_card(t) for t in items[:3])}</div></section>'
    page = f'<!doctype html><html lang="en">{head("AI Stack Gallery — Copy Practical AI Tool Stacks | AIToolsEssentials", "Browse practical AI stacks for consultants, teachers, creators, developers, small businesses, and researchers.", DOMAIN+"/stacks/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:880px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">AI stack gallery</p><h1>Copy a stack. Then make it yours.</h1><p class="subhead">Seed stacks for common roles — designed to be shared, debated, and improved.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Community loop</span><p>Have a better real-world stack? Submit it through the community report form and we can publish verified examples as buyer evidence.</p><p><a class="button button-blue" href="/community/test-report.html">Submit real results</a></p></div><h2>Shareable stack pages</h2><div class="content-hub-grid">{seo_cards}</div>{sections}</div></section></main>{FOOTER}{scripts()}</body></html>'
    (root / "stacks" / "index.html").write_text(page)


def generate_badges(root: Path, tools: list[dict[str, Any]]) -> None:
    # Emit an embeddable SVG badge for every listed tool so vendors can link back.
    badge_dir = root / "badges"
    badge_dir.mkdir(exist_ok=True)
    accent = "#0071E3"
    for t in tools:
        slug = t["slug"]
        rating = t.get("rating", "")
        label = esc(t["name"])
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="54" role="img" aria-label="Reviewed on AIToolsEssentials">
  <rect width="200" height="54" rx="8" fill="#ffffff"/>
  <rect width="200" height="54" rx="8" fill="none" stroke="{accent}" stroke-width="1.5"/>
  <rect width="6" height="54" fill="{accent}"/>
  <text x="16" y="22" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" font-size="11" font-weight="600" fill="#111111">Reviewed on</text>
  <text x="16" y="37" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" font-size="13" font-weight="700" fill="{accent}">AIToolsEssentials</text>
  <text x="184" y="37" text-anchor="end" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" font-size="11" fill="#555555">{esc(rating)}/5</text>
  <title>{label} review on AIToolsEssentials</title>
</svg>'''
        (badge_dir / f"{slug}.svg").write_text(svg)
    top = sorted(tools, key=lambda t: float(t.get("rating", 0) or 0), reverse=True)[:12]
    badges = "".join(f'<article class="content-hub-card"><span>{esc(t["category"])}</span><h3>{esc(t["name"])}</h3><div class="vendor-badge-preview"><strong>Reviewed on AIToolsEssentials</strong><small>{esc(t.get("rating"))}/5 editorial score</small></div><textarea readonly>&lt;a href="{DOMAIN}/tools/{t["slug"]}/" rel="noopener"&gt;&lt;img alt="Reviewed on AIToolsEssentials" src="{DOMAIN}/badges/{t["slug"]}.svg"&gt;&lt;/a&gt;</textarea><a class="button button-blue small" href="/tools/{t["slug"]}/">Review page</a></article>' for t in top)
    all_note = '<p class="muted-small">Every listed tool has a badge. Ask us for yours if it is not shown: <a href="mailto:' + EMAIL + '">' + EMAIL + '</a></p>'
    page = f'<!doctype html><html lang="en">{head("AIToolsEssentials Vendor Badges — Reviewed AI Tool Badges", "Vendors can link to their AIToolsEssentials review with transparent, editorially-labeled badges.", DOMAIN+"/badges/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:880px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Vendor badges</p><h1>Give reviewed tools a reason to link back.</h1><p class="subhead">Transparent badges for vendors who want to point buyers to independent review pages. No paid ranking implied.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Editorial rules</span><p>Badges link to review pages and may not imply endorsement beyond the exact text shown. Sponsored placements remain separately labeled.</p></div>{all_note}<div class="content-hub-grid">{badges}</div></div></section></main>{FOOTER}{scripts()}</body></html>'
    out = root / "badges" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)


def generate_cost_calculator(root: Path, tools: list[dict[str, Any]]) -> None:
    payload = json.dumps([compact_tool(t) for t in tools], separators=(",", ":"))
    cost_cards = "".join(f'<article class="content-hub-card"><span>{esc(t["category"])} · {esc(t.get("price", ""))}</span><h3>{esc(t["name"])}</h3><p>{esc(t.get("summary", ""))}</p><label><input type="checkbox" data-cost value="{t["slug"]}"> Add to estimate</label></article>' for t in tools)
    default_summary = '<span>Estimated monthly stack cost</span><h2>$0/mo</h2><p>Select tools below to estimate your monthly stack. Verify current vendor pricing before paying.</p>'
    extra_js = '<script>const COST_TOOLS='+payload+';</script><script src="/js/viral.js" defer></script>'
    page = f'<!doctype html><html lang="en">{head("AI Tool Cost Calculator — Estimate Your Stack Cost | AIToolsEssentials", "Estimate your AI stack cost by choosing tools and team size. Compare free-first and paid-plan risk before subscribing.", DOMAIN+"/cost-calculator.html")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:880px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">AI tool cost calculator</p><h1>Know the monthly cost before the stack sprawls.</h1><p class="subhead">Select tools, set team size, and see rough monthly budget risk. Official pricing changes often — use this as a planning estimate.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Estimate</span><label>Team size <input id="teamSize" type="number" min="1" value="1"></label><p class="muted-small">Planning assumptions: free/self-hosted = $0, free+paid = $20/user/mo, paid = $35/user/mo unless official pages say otherwise. Use reviews for current pricing.</p></div><div id="costSummary" class="viral-result-card">{default_summary}</div><div id="costToolList" class="content-hub-grid">{cost_cards}</div></div></section></main>{FOOTER}{scripts(extra_js)}</body></html>'
    (root / "cost-calculator.html").write_text(page)


def generate_deals(root: Path, tools: list[dict[str, Any]]) -> None:
    free = [t for t in tools if "free" in t.get("price", "").lower()]
    paid = [t for t in tools if "free" not in t.get("price", "").lower()]
    page = f'<!doctype html><html lang="en">{head("AI Tool Deals, Free Trials & Free Plans | AIToolsEssentials", "Find AI tools with free plans, free trials, and budget-friendly starting points before committing to paid AI subscriptions.", DOMAIN+"/deals/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Deals and free trials</p><h1>Try the stack before the subscriptions pile up.</h1><p class="subhead">Free plans, free-first picks, and paid tools to evaluate carefully. Affiliate or sponsored offers are labeled when active.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Budget rule</span><p>Use free tiers for workflow validation. Upgrade only when the tool saves time every week or replaces a paid seat elsewhere.</p><p><a class="button button-blue" href="/cost-calculator.html">Estimate stack cost</a><a class="button button-blue" href="/free-ai-tools.html" style="margin-left:8px">Browse free AI tools</a></p></div><h2>Free-plan tools to test first</h2><div class="content-hub-grid">{"".join(tool_card(t) for t in free[:18])}</div><h2>Paid tools worth comparing before you subscribe</h2><div class="content-hub-grid">{"".join(tool_card(t) for t in paid[:8])}</div></div></section></main>{FOOTER}{scripts()}</body></html>'
    out = root / "deals" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)


def generate_shortlist_compare(root: Path, tools: list[dict[str, Any]]) -> None:
    payload = json.dumps([compact_tool(t) for t in tools], separators=(",", ":"))
    extra_js = '<script>const COMPARE_TOOLS='+payload+';</script><script src="/js/viral.js" defer></script>'
    page = f'<!doctype html><html lang="en">{head("Compare My AI Tool Shortlist | AIToolsEssentials", "Compare your saved AI tools by category coverage, rough monthly cost, and workflow gaps before choosing a stack.", DOMAIN+"/compare-shortlist.html")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Shortlist comparison</p><h1>Turn saved tools into a decision.</h1><p class="subhead">See rough cost, overlapping categories, and missing stack coverage from your no-login shortlist.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div id="shortlistCompare" class="viral-result-card"><span>Compare shortlist</span><h2>No saved tools yet</h2><p>Add tools to your shortlist, then come back to compare cost and coverage.</p><p><a class="button button-blue" href="/tool-finder.html">Find tools</a></p></div></div></section></main>{FOOTER}{scripts(extra_js)}</body></html>'
    (root / "compare-shortlist.html").write_text(page)


def generate_weekly(root: Path, tools: list[dict[str, Any]], today: str) -> None:
    top = sorted(tools, key=lambda t: float(t.get("rating", 0) or 0), reverse=True)[:5]
    free = [t for t in tools if "free" in t.get("price", "").lower()][:5]
    auto = [t for t in tools if "automation" in t.get("category", "").lower() or "workflow" in t.get("best_for", "").lower()][:4]
    page = f'<!doctype html><html lang="en">{head("AI Tools Worth Testing This Week | AIToolsEssentials", "A weekly public shortlist of AI tools worth testing, pricing notes, workflow ideas, and tools to compare before paying.", DOMAIN+"/weekly/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:880px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Weekly shortlist · Updated {today}</p><h1>AI tools worth testing this week.</h1><p class="subhead">A repeat-visit page for practical tools, free-tier picks, and workflow stacks worth trying.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card newsletter-card"><span>Weekly note</span><h2>Get the 5-tool weekly shortlist.</h2><p>Until a full email platform is connected, send yourself here each week or contact us to be added manually.</p><form action="https://formsubmit.co/{EMAIL}" method="POST"><input type="hidden" name="_subject" value="Weekly AI tools signup"><label>Email <input type="email" name="email" placeholder="you@example.com" required></label><button class="button button-blue" type="submit">Request weekly list</button></form></div><h2>Five tools worth testing</h2><div class="content-hub-grid">{"".join(tool_card(t) for t in top)}</div><h2>Free-tier picks to try before paying</h2><div class="content-hub-grid">{"".join(tool_card(t) for t in free)}</div><h2>Workflow stack of the week</h2><p>Automate lead intake, first response, and follow-up reminders with a free-first operations stack.</p><div class="content-hub-grid">{"".join(tool_card(t) for t in auto)}</div><p><a class="button button-blue" href="/stack-builder.html">Generate your stack</a><a class="button button-blue" href="/cost-calculator.html" style="margin-left:8px">Estimate cost</a></p></div></section></main>{FOOTER}{scripts()}</body></html>'
    out = root / "weekly" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)


def inject_review_stack_modules(root: Path, tools: list[dict[str, Any]]) -> None:
    role_map = {
        "automation": ("small-business", "AI stack for small-business automation"),
        "audio": ("creator", "Creator audio/video stack"),
        "video": ("creator", "Creator video stack"),
        "creative": ("creator", "Creator content stack"),
        "development": ("developer", "Developer shipping stack"),
        "research": ("researcher", "Research analyst stack"),
        "writing": ("agency", "Agency writing stack"),
        "meeting": ("freelancer", "Consultant meeting stack"),
    }
    for t in tools:
        path = root / "tools" / t["slug"] / "index.html"
        if not path.exists():
            continue
        html = path.read_text()
        html = re.sub(r"\s*<!-- AIT STACK MODULE START -->.*?<!-- AIT STACK MODULE END -->\s*", "\n", html, flags=re.S)
        hay = (t.get("category", "") + " " + t.get("best_for", "")).lower()
        role, title = "freelancer", "Practical AI stack including " + t["name"]
        for needle, value in role_map.items():
            if needle in hay:
                role, title = value
                break
        block = f'\n<!-- AIT STACK MODULE START -->\n<section class="score-card stack-entry-module"><span>Build around {esc(t["name"])}</span><h2>{esc(title)}</h2><p>Use {esc(t["name"])} as one part of a complete AI workflow, then compare cost and overlap before paying for the whole stack.</p><p><a class="button button-blue" href="/stack-builder.html">Generate related stack</a><a class="button button-blue" href="/compare-shortlist.html" style="margin-left:8px">Compare shortlist</a></p></section>\n<!-- AIT STACK MODULE END -->\n'
        if "</main>" in html:
            html = html.replace("</main>", block + "</main>", 1)
            path.write_text(html)


def generate_js(root: Path) -> None:
    js = r'''
(function(){
function params(){return new URLSearchParams(location.search)}
function find(slug){return (window.TOOLS||[]).find(t=>t.slug===slug)}
function stacks(role,budget,vibe){const base={freelancer:['chatgpt','perplexity','make','canva-ai','otter-ai'],agency:['jasper','copy-ai','canva-ai','make','descript'],developer:['cursor','github-copilot','claude','replit-ai','v0'],teacher:['chatgpt','gamma','canva-ai','perplexity','otter-ai'],creator:['descript','elevenlabs','canva-ai','midjourney','allvideoai'],'small-business':['chatgpt','make','zapier-ai','airtable-ai','microsoft-copilot'],researcher:['perplexity','claude','you-com','gemini','notion-ai']};let slugs=(base[role]||base.freelancer).slice();if(budget==='free') slugs=slugs.filter(s=>{let t=find(s);return t&&/free/i.test(t.price||'')}).concat(['chatgpt','claude','gemini','perplexity','canva-ai','n8n']);if(vibe==='technical') slugs=['n8n','cursor','github-copilot','claude','airtable-ai'].concat(slugs);if(vibe==='low-friction') slugs=['chatgpt','canva-ai','zapier-ai','perplexity','otter-ai'].concat(slugs);const seen=[];return slugs.filter(s=>find(s)&&!seen.includes(s)&&seen.push(s)).slice(0,5).map(find)}
function card(t){return `<article class="content-hub-card"><span>${t.category} · ${t.price||''}</span><h3><a href="/tools/${t.slug}/">${t.name}</a></h3><p>${t.summary||''}</p><p><strong>Best for:</strong> ${t.best_for||''}</p><a class="button button-blue small" href="/tools/${t.slug}/">Read review</a></article>`}
function visual(title,role,budget,vibe,items){return `<div class="stack-share-card" id="stackShareCard"><span>My AI Stack</span><h2>${title}</h2><p>${role} · ${budget} · ${vibe}</p><ol>${items.map(t=>`<li>${t.name}</li>`).join('')}</ol><small>Generated by AIToolsEssentials</small></div>`}
function downloadCard(){const el=document.getElementById('stackShareCard'); if(!el)return; const text=[...el.querySelectorAll('h2,p,li,small')].map(x=>x.textContent).join('\n'); const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630"><rect width="1200" height="630" fill="#08090a"/><circle cx="950" cy="100" r="280" fill="#5e6ad2" opacity=".35"/><text x="80" y="100" fill="#aeb7ff" font-size="28" font-family="Inter,Arial">My AI Stack</text><text x="80" y="175" fill="white" font-size="54" font-weight="700" font-family="Inter,Arial">${(el.querySelector('h2')?.textContent||'AI Stack').replace(/&/g,'&amp;')}</text>${[...el.querySelectorAll('li')].map((li,i)=>`<text x="110" y="${260+i*58}" fill="white" font-size="36" font-family="Inter,Arial">${i+1}. ${li.textContent.replace(/&/g,'&amp;')}</text>`).join('')}<text x="80" y="575" fill="#aeb7ff" font-size="28" font-family="Inter,Arial">aitoolsessentials.com</text></svg>`; const blob=new Blob([svg],{type:'image/svg+xml'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='ai-stack-card.svg'; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),1000)}
function copyLink(btn){navigator.clipboard?.writeText(location.href).then(()=>{if(btn)btn.textContent='Copied ✓'})}
function renderStack(){if(!window.TOOLS||!document.getElementById('stackResult'))return;const p=params();['role','budget','vibe'].forEach(id=>{if(p.get(id)&&document.getElementById(id))document.getElementById(id).value=p.get(id)});const role=document.getElementById('role').value,budget=document.getElementById('budget').value,vibe=document.getElementById('vibe').value;const result=stacks(role,budget,vibe);const url=new URL(location.href);url.search=`?role=${role}&budget=${budget}&vibe=${vibe}`;history.replaceState(null,'',url);document.getElementById('stackResult').innerHTML=`<span>Your shareable stack</span><h2>${role.replace('-',' ')} · ${budget} · ${vibe}</h2>${visual(role.replace('-',' ')+' stack',role,budget,vibe,result)}<p class="actions"><button class="button button-blue" id="downloadStackCard">Download card</button><button class="button button-blue" id="shareNative">Share stack</button><a class="button button-blue" href="/cost-calculator.html">Estimate cost</a></p><div class="content-hub-grid">${result.map(card).join('')}</div>`;document.getElementById('downloadStackCard')?.addEventListener('click',downloadCard);const share=document.getElementById('shareNative'); if(share)share.onclick=()=>{navigator.share?navigator.share({title:document.title,url:location.href}):copyLink(share)}}
function renderCost(){if(!window.COST_TOOLS||!document.getElementById('costToolList'))return;const list=document.getElementById('costToolList'),summary=document.getElementById('costSummary'),team=document.getElementById('teamSize');function est(t){let p=(t.price||'').toLowerCase();if(p.includes('free self-hosted'))return 0;if(p.includes('free'))return 20;return 35}function update(){let selected=[...document.querySelectorAll('[data-cost]:checked')].map(i=>COST_TOOLS.find(t=>t.slug===i.value)).filter(Boolean);let seats=Math.max(1,Number(team.value||1));let monthly=selected.reduce((a,t)=>a+est(t)*seats,0);summary.innerHTML=`<span>Estimated monthly stack cost</span><h2>$${monthly}/mo</h2><p>${selected.length} tools · ${seats} seat${seats===1?'':'s'} · rough planning estimate. Verify current vendor pricing before paying.</p>`}list.addEventListener('change',update);team?.addEventListener('input',update);update()}
function renderShortlistCompare(){if(!window.COMPARE_TOOLS||!document.getElementById('shortlistCompare'))return;const saved=JSON.parse(localStorage.getItem('aitoolsessentials.shortlist.v1')||'[]');const tools=saved.map(s=>COMPARE_TOOLS.find(t=>t.slug===s)).filter(Boolean);const el=document.getElementById('shortlistCompare');if(!tools.length)return;const cats=[...new Set(tools.map(t=>t.category))];const monthly=tools.reduce((a,t)=>a+(/free self-hosted/i.test(t.price||'')?0:/free/i.test(t.price||'')?20:35),0);const gaps=['Research','Automation','Creative','Development','Meetings','Writing'].filter(c=>!cats.some(x=>x.toLowerCase().includes(c.toLowerCase())));el.innerHTML=`<span>Compare shortlist</span><h2>${tools.length} saved tools · ~$${monthly}/mo planning estimate</h2><p><strong>Categories covered:</strong> ${cats.join(', ')}</p><p><strong>Possible gaps:</strong> ${gaps.length?gaps.join(', '):'Good coverage across common workflows.'}</p><div class="content-hub-grid">${tools.map(card).join('')}</div><p><a class="button button-blue" href="/cost-calculator.html">Estimate full stack cost</a><a class="button button-blue" href="/stack-builder.html" style="margin-left:8px">Generate a stack</a></p>`}
document.addEventListener('DOMContentLoaded',function(){document.getElementById('generateStack')?.addEventListener('click',renderStack);document.getElementById('copyStack')?.addEventListener('click',e=>copyLink(e.target));document.getElementById('downloadStackCard')?.addEventListener('click',downloadCard);document.querySelectorAll('[data-download-stack]').forEach(b=>b.addEventListener('click',downloadCard));document.querySelectorAll('[data-copy-stack]').forEach(b=>b.addEventListener('click',()=>copyLink(b)));renderStack();renderCost();renderShortlistCompare();});
})();
'''
    (root / "js" / "viral.js").write_text(js)


def generate_css(root: Path) -> None:
    p = root / "css" / "styles.css"
    css = p.read_text()
    if "/* Viral/share utility surfaces */" not in css:
        css += """

/* Viral/share utility surfaces */
.viral-controls { display:grid; grid-template-columns:repeat(3,minmax(180px,1fr)); gap:14px; margin-top:14px; }
.viral-controls label, .viral-control label { display:flex; flex-direction:column; gap:7px; font-size:13px; font-weight:700; color:rgba(0,0,0,.62); }
.viral-controls select, .viral-control input { border:1px solid rgba(94,106,210,.22); border-radius:10px; padding:12px; font:inherit; background:#fff; }
.viral-result-card { margin-top:28px; padding:28px; border-radius:22px; border:1px solid rgba(94,106,210,.18); background:linear-gradient(180deg,#fff,rgba(94,106,210,.06)); box-shadow:0 24px 70px rgba(8,9,10,.08); }
.viral-result-card > span, .stack-gallery-block > div > p:first-child { text-transform:uppercase; letter-spacing:.12em; font-size:12px; font-weight:800; color:#5e6ad2; }
.stack-gallery-block { display:grid; grid-template-columns:minmax(240px,.55fr) 1fr; gap:28px; align-items:start; margin:58px 0; }
.vendor-badge-preview { display:inline-flex; flex-direction:column; gap:2px; border:1px solid rgba(94,106,210,.28); border-radius:14px; padding:12px 14px; background:linear-gradient(135deg,#08090a,#151626); color:#fff; box-shadow:0 18px 42px rgba(94,106,210,.18); }
.vendor-badge-preview small { color:rgba(255,255,255,.72); }
.content-hub-card textarea { width:100%; min-height:84px; border:1px solid rgba(0,0,0,.12); border-radius:10px; padding:10px; font-size:12px; background:#f8f8fb; }
@media (max-width: 800px) { .viral-controls, .stack-gallery-block { grid-template-columns:1fr; } }
"""
    if "/* Stack share cards and conversion surfaces */" not in css:
        css += """

/* Stack share cards and conversion surfaces */
.stack-layout { display:grid; grid-template-columns:minmax(280px,.42fr) 1fr; gap:30px; align-items:start; }
.stack-share-card { border-radius:28px; padding:28px; color:#fff; background:radial-gradient(circle at 80% 12%, rgba(94,106,210,.55), transparent 34%), linear-gradient(135deg,#08090a,#17182b 62%,#32266f); box-shadow:0 28px 80px rgba(8,9,10,.22); border:1px solid rgba(255,255,255,.14); }
.stack-share-card span { color:#aeb7ff; text-transform:uppercase; letter-spacing:.14em; font-size:12px; font-weight:900; }
.stack-share-card h2 { color:#fff; font-size:34px; line-height:1.04; margin:12px 0; }
.stack-share-card p, .stack-share-card small { color:rgba(255,255,255,.75); }
.stack-share-card ol { margin:18px 0 20px; padding-left:24px; }
.stack-share-card li { margin:9px 0; font-size:20px; font-weight:800; }
.stack-entry-module { margin:34px auto; max-width:980px; }
.newsletter-card form { display:flex; gap:12px; flex-wrap:wrap; align-items:end; }
.newsletter-card input { border:1px solid rgba(94,106,210,.22); border-radius:10px; padding:12px; min-width:260px; }
button.shortlist-btn, .card-actions button.shortlist-btn { color:#1e2a8a !important; border-color:#5e6ad2 !important; background:#e1e6ff !important; box-shadow:0 8px 18px rgba(94,106,210,.13) !important; opacity:1 !important; }
@media (max-width: 900px) { .stack-layout { grid-template-columns:1fr; } }
"""
    p.write_text(css)


def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    tools = tools or json.loads((root / "data/tools.json").read_text())
    today = today or datetime.today().strftime("%Y-%m-%d")
    generate_stack_builder(root, tools)
    generate_stack_gallery(root, tools)
    generate_badges(root, tools)
    generate_cost_calculator(root, tools)
    generate_deals(root, tools)
    generate_shortlist_compare(root, tools)
    generate_weekly(root, tools, today)
    inject_review_stack_modules(root, tools)
    generate_js(root)
    generate_css(root)
    return 16


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    print(generate(root))
