#!/usr/bin/env python3
"""Generate evergreen resource library pages for AI tool buyers."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
HEADER = '<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/stack-builder.html">Stack builder</a><a href="/tool-finder.html">Tool finder</a><a href="/free-ai-tools.html">Free AI tools</a><a href="/alternatives/">Alternatives</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/articles/index.html">Guides</a><a href="/deals/">Deals</a></nav><a class="nav-cta" href="/pricing/">Premium</a></header>'
FOOTER = f'<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/advertise/index.html" rel="nofollow">Advertise</a><a href="/submit-tool.html" rel="nofollow">Submit a tool</a><a href="/community/test-report.html" rel="nofollow">Report your results</a><a href="/badges/">Badges</a><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a></footer>'

RESOURCES = [
    {
        "slug": "ai-tool-evaluation-checklist",
        "title": "AI Tool Evaluation Checklist",
        "kicker": "Buyer checklist",
        "description": "A practical checklist for testing an AI tool before you connect data, invite a team, or pay annually.",
        "sections": [
            ("Workflow fit", ["What weekly task does this tool replace or improve?", "Who owns the workflow internally?", "What output quality would make the tool worth keeping?", "Which current tool or process does it overlap with?"]),
            ("Trial test", ["Run one real task, not a demo prompt.", "Save the input, output, time spent, and failure cases.", "Check export options before creating important work inside the tool.", "Document what a human still must review."]),
            ("Buying decision", ["Confirm free-tier limits and paid upgrade triggers.", "Check cancellation and seat-management terms.", "Compare at least two alternatives before annual billing.", "Estimate total monthly stack cost, not one subscription in isolation."]),
        ],
    },
    {
        "slug": "ai-tool-security-questions",
        "title": "AI Tool Security Questions",
        "kicker": "Trust checklist",
        "description": "Questions to ask before putting company, client, student, or customer data into an AI tool.",
        "sections": [
            ("Data handling", ["What data is uploaded or synced?", "Is data used for model training by default?", "Can admins disable training or retention?", "Where is the data stored and processed?"]),
            ("Access controls", ["Does the plan support SSO, SCIM, or admin controls?", "Can you remove users and revoke sessions quickly?", "Are workspace roles granular enough?", "Can exports and sharing be restricted?"]),
            ("Vendor evidence", ["Is there a security page, DPA, subprocessors list, or SOC 2 report?", "Are incident/contact policies public?", "Does the vendor document enterprise controls separately from consumer plans?", "Are limitations explained clearly?"]),
        ],
    },
    {
        "slug": "ai-pricing-audit-worksheet",
        "title": "AI Pricing Audit Worksheet",
        "kicker": "Cost worksheet",
        "description": "A lightweight worksheet for reducing AI subscription sprawl across a team or solo business.",
        "sections": [
            ("Inventory", ["List every AI tool with plan, owner, monthly cost, and renewal date.", "Mark free, freemium, paid-only, annual, and unused seats.", "Note which tools store business/client data.", "Identify duplicate categories like writing, meeting notes, and automation."]),
            ("Usage proof", ["For each paid tool, name the weekly workflow it supports.", "Estimate hours saved or revenue/risk improved.", "Mark tools that have not been used in 30 days.", "Cancel or downgrade tools without a clear owner."]),
            ("Optimization", ["Move experiments to free tiers when possible.", "Bundle overlapping workflows into one stack.", "Avoid annual upgrades until the workflow is proven.", "Recheck pricing and limits quarterly."]),
        ],
    },
    {
        "slug": "ai-stack-planning-template",
        "title": "AI Stack Planning Template",
        "kicker": "Stack template",
        "description": "A template for designing a small AI stack by role, budget, risk, and weekly workflow.",
        "sections": [
            ("Define the stack", ["Role or team:", "Top three weekly workflows:", "Current tools used:", "Budget cap per month:", "Data sensitivity level:"]),
            ("Choose categories", ["General assistant or research tool", "Creation/editing tool", "Automation tool", "Meeting/transcription tool", "Specialist domain tool"]),
            ("Decision rule", ["Start with the free or lowest-friction option.", "Test with real work for seven days.", "Upgrade only when limits block a valuable workflow.", "Revisit the stack monthly until stable."]),
        ],
    },
    {
        "slug": "ai-tool-comparison-scorecard",
        "title": "AI Tool Comparison Scorecard",
        "kicker": "Comparison template",
        "description": "A scorecard for comparing two or three AI tools before choosing one.",
        "sections": [
            ("Score each tool", ["Workflow fit: /10", "Output quality: /10", "Data controls: /10", "Collaboration: /10", "Price pressure: /10", "Export/portability: /10"]),
            ("Evidence to capture", ["Screenshot of pricing page", "Official docs for data/training policy", "One real output sample", "Notes on failure cases", "Cancellation/renewal terms"]),
            ("Final call", ["Best for solo testing:", "Best for teams:", "Best free option:", "Risks before purchase:", "Review date:"]),
        ],
    },
    {
        "slug": "prompt-template-tool-testing",
        "title": "Prompt Template for Testing AI Tools",
        "kicker": "Prompt template",
        "description": "A reusable prompt for stress-testing an AI assistant, writing tool, research tool, or workflow tool.",
        "sections": [
            ("Copy/paste prompt", ["You are helping me evaluate this AI tool for [workflow]. My success criteria are [criteria]. Use the following real input: [input]. Produce [output format]. Then list assumptions, missing context, risks, and what a human should verify before using the result."]),
            ("How to judge output", ["Did it follow the requested format?", "Did it make unsupported claims?", "Did it ask for missing context when needed?", "Did it reduce work compared with the current process?"]),
            ("Next test", ["Run the same prompt in two alternatives.", "Compare time saved, correctness, and editing burden.", "Save the best output and failure cases."]),
        ],
    },
    {
        "slug": "prompt-template-ai-research",
        "title": "Prompt Template for AI Research",
        "kicker": "Prompt template",
        "description": "A cautious research prompt that asks an AI tool for sources, uncertainty, and verification steps.",
        "sections": [
            ("Copy/paste prompt", ["Research [topic] for [decision]. Prioritize recent, primary, and official sources. Separate verified facts from assumptions. Include source links, date sensitivity, contradictions, and what I should verify manually before acting."]),
            ("Source checks", ["Prefer official docs, pricing pages, filings, benchmarks, or primary announcements.", "Do not trust uncited claims.", "Check dates and whether pricing/features changed."]),
            ("Decision output", ["Summarize in five bullets.", "List three risks.", "Recommend the next verification step."]),
        ],
    },
    {
        "slug": "prompt-template-automation-workflow",
        "title": "Prompt Template for AI Automation Workflows",
        "kicker": "Prompt template",
        "description": "A planning prompt for turning a repetitive business process into a safe AI-assisted automation.",
        "sections": [
            ("Copy/paste prompt", ["Map this workflow into triggers, inputs, AI steps, human review points, app actions, failure modes, and logs: [workflow]. Keep customer-facing, financial, legal, and credential steps behind human approval."]),
            ("Safety checks", ["What happens if the AI output is wrong?", "Where is the human approval gate?", "What data is passed between apps?", "How are errors logged and reversed?"]),
            ("Implementation caution", ["Prototype with dummy data first.", "Avoid secrets in prompts.", "Keep audit logs for customer-impacting automations."]),
        ],
    },
]


def esc(s: Any) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def head(title: str, desc: str, canonical: str) -> str:
    return f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{esc(desc)}"><title>{esc(title)}</title><link rel="canonical" href="{canonical}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/css/styles.css"></head>'


def scripts() -> str:
    return '<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>'


def render_resource(res: dict[str, Any]) -> str:
    section_html = []
    for title, items in res["sections"]:
        lis = "".join(f'<li><label><input type="checkbox"> {esc(item)}</label></li>' for item in items)
        section_html.append(f'<article class="content-hub-card resource-checklist"><h2>{esc(title)}</h2><ul>{lis}</ul></article>')
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f"Who should use {res['title']}?", "acceptedAnswer": {"@type": "Answer", "text": res["description"]}},
            {"@type": "Question", "name": "What should I do after filling it out?", "acceptedAnswer": {"@type": "Answer", "text": "Use the answers to shortlist tools, estimate stack cost, compare alternatives, and verify pricing/security details against official sources."}},
        ],
    }
    return f'<!doctype html><html lang="en">{head(res["title"]+" | AIToolsEssentials", res["description"], DOMAIN+"/resources/"+res["slug"]+".html")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">{esc(res["kicker"])}</p><h1>{esc(res["title"])}</h1><p class="subhead">{esc(res["description"])}</p><p><button class="button button-blue" onclick="window.print()">Print / save PDF</button><a class="button button-blue" href="/stack-builder.html" style="margin-left:8px">Build related stack</a></p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>How to use this resource</span><p>Use this as a working checklist. Print it, save it as PDF, or copy the prompts into the tool you are testing. Verify pricing, policy, and security details against official vendor pages before buying.</p></div><div class="content-hub-grid">{"".join(section_html)}</div><section class="score-card related-next-steps"><span>Decision loop</span><h2>Turn the answers into a shortlist.</h2><p><a class="button button-blue" href="/tool-finder.html">Find tools</a><a class="button button-blue" href="/cost-calculator.html" style="margin-left:8px">Estimate cost</a><a class="button button-blue" href="/compare-shortlist.html" style="margin-left:8px">Compare shortlist</a></p></section></div></section><script type="application/ld+json">{json.dumps(faq)}</script></main>{FOOTER}{scripts()}</body></html>'


def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    out = root / "resources"
    out.mkdir(exist_ok=True)
    cards = []
    for res in RESOURCES:
        (out / f"{res['slug']}.html").write_text(render_resource(res))
        cards.append(f'<article class="content-hub-card"><span>{esc(res["kicker"])}</span><h3><a href="/resources/{res["slug"]}.html">{esc(res["title"])}</a></h3><p>{esc(res["description"])}</p><a class="button button-blue small" href="/resources/{res["slug"]}.html">Open resource</a></article>')
    desc = "Free AI tool buyer checklists, security questions, pricing worksheets, scorecards, and prompt templates for evaluating tools before paying."
    index = f'<!doctype html><html lang="en">{head("AI Tool Buyer Resource Library", desc, DOMAIN+"/resources/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Resource library</p><h1>Checklists and prompts for choosing AI tools.</h1><p class="subhead">Use practical worksheets, scorecards, and prompt templates before connecting data, inviting a team, or paying annually.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{"".join(cards)}</div></div></section></main>{FOOTER}{scripts()}</body></html>'
    (out / "index.html").write_text(index)
    return len(RESOURCES) + 1


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    print(generate(root))
