#!/usr/bin/env python3
"""Generate glossary/pricing knowledge pages and sitewide knowledge schema."""
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

GLOSSARY = [
    ("ai-agent", "AI agent", "An AI system that can plan steps, use tools, and complete a task with less step-by-step prompting than a basic chatbot.", "Use agents for repeatable workflows with clear guardrails, logs, and human review."),
    ("ai-copilot", "AI copilot", "An assistant embedded inside an app, editor, or workflow that suggests, drafts, summarizes, or automates next actions.", "Best when you already know the workflow and want faster execution, not a replacement for judgment."),
    ("ai-stack", "AI stack", "A collection of AI tools used together for a role or workflow, such as research, content, meetings, automation, and design.", "Keep the stack small and prove each paid tool removes a real bottleneck."),
    ("context-window", "Context window", "The amount of text, code, documents, or conversation a model can consider at one time.", "Large context helps with long documents, but retrieval quality and instruction discipline still matter."),
    ("fine-tuning", "Fine-tuning", "Training a model further on examples so it better matches a style, format, domain, or task pattern.", "Use fine-tuning after prompts and retrieval are not enough, and when you have high-quality examples."),
    ("freemium-ai-tool", "Freemium AI tool", "A tool with a free tier plus paid upgrades for higher limits, team features, exports, integrations, or commercial usage.", "Test the free tier, but check upgrade pressure before building business workflows around it."),
    ("hallucination", "AI hallucination", "A confident but false or unsupported answer produced by an AI system.", "For decisions, require sources, official docs, screenshots, logs, or human verification."),
    ("model-routing", "Model routing", "Choosing different AI models for different tasks based on cost, speed, reasoning quality, or modality.", "Useful when a workflow mixes cheap drafts with expensive high-stakes reasoning."),
    ("prompt-engineering", "Prompt engineering", "Writing instructions, examples, constraints, and context so an AI tool produces a more useful output.", "Good prompts define role, input, output format, constraints, and evaluation criteria."),
    ("rag", "RAG", "Retrieval-augmented generation: searching trusted documents or data first, then asking a model to answer using that context.", "Use RAG when answers must be grounded in your own docs or current source material."),
    ("shortlist", "AI tool shortlist", "A small set of candidate tools selected for testing before purchase.", "Shortlists prevent buying tools that overlap or solve the wrong workflow problem."),
    ("workflow-automation", "AI workflow automation", "Connecting apps, triggers, actions, and AI steps to reduce manual operational work.", "Start with low-risk tasks and keep audit trails for anything customer-facing or financial."),
]


def esc(s: Any) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def head(title: str, desc: str, canonical: str) -> str:
    return f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{esc(desc)}"><title>{esc(title)}</title><link rel="canonical" href="{canonical}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/css/styles.css"></head>'


def scripts() -> str:
    return '<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>'


def tool_card(t: dict[str, Any]) -> str:
    return f'<article class="content-hub-card"><span>{esc(t.get("category"))} · {esc(t.get("price"))}</span><h3><a href="/tools/{esc(t["slug"])}/">{esc(t["name"])}</a></h3><p>{esc(t.get("summary", ""))}</p><p><strong>Best for:</strong> {esc(t.get("best_for", ""))}</p><a class="button button-blue small" href="/tools/{esc(t["slug"])}/">Read review</a></article>'


TERM_MATCH_HINTS = {
    "RAG": ["Research", "General AI Assistant", "AI Search"],
    "AI hallucination": ["Research", "General AI Assistant", "AI Search"],
    "Context window": ["General AI Assistant", "Research", "Development"],
    "AI workflow automation": ["Automation"],
    "AI copilot": ["Development", "Productivity", "General AI Assistant"],
    "AI agent": ["Automation", "Development", "General AI Assistant"],
    "Prompt engineering": ["General AI Assistant", "Writing", "Marketing"],
    "AI stack": ["Automation", "Productivity", "General AI Assistant"],
    "AI tool shortlist": ["Productivity", "Research", "General AI Assistant"],
    "Freemium AI tool": ["Automation", "Creative", "Development"],
    "Fine-tuning": ["Development", "General AI Assistant"],
    "Model routing": ["Development", "General AI Assistant"],
}


def related_tools(term: str, tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    q = term.lower().replace("ai ", "")
    hints = [h.lower() for h in TERM_MATCH_HINTS.get(term, [])]
    scored: list[tuple[int, dict[str, Any]]] = []
    for t in tools:
        hay = " ".join(str(t.get(k, "")) for k in ["name", "category", "summary", "best_for", "price"]).lower()
        score = 0
        if q in hay:
            score += 4
        for hint in hints:
            if hint and hint in hay:
                score += 3
        for token in re.findall(r"[a-z]+", q):
            if len(token) > 2 and token in hay:
                score += 1
        if score:
            scored.append((score, t))
    return [t for _, t in sorted(scored, key=lambda x: (-x[0], x[1].get("name", "")))[:6]] or tools[:6]


def generate_glossary(root: Path, tools: list[dict[str, Any]]) -> None:
    out = root / "glossary"
    out.mkdir(exist_ok=True)
    cards = []
    for slug, term, definition, advice in GLOSSARY:
        rel_tools = related_tools(term, tools)
        tool_cards = "".join(tool_card(t) for t in rel_tools[:4])
        desc = f"Plain-English definition of {term}, when it matters, and how to evaluate related AI tools before paying."
        faq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f"What is {term}?", "acceptedAnswer": {"@type": "Answer", "text": definition}},
                {"@type": "Question", "name": f"How should I evaluate {term} tools?", "acceptedAnswer": {"@type": "Answer", "text": advice}},
            ],
        }
        page = f'<!doctype html><html lang="en">{head(term+" definition | AIToolsEssentials", desc, DOMAIN+"/glossary/"+slug+".html")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">AI tools glossary</p><h1>{esc(term)}</h1><p class="subhead">{esc(definition)}</p><p><a class="button button-blue" href="/tool-finder.html">Find related tools</a><a class="button button-blue" href="/stack-builder.html" style="margin-left:8px">Build a stack</a></p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Practical evaluation note</span><p>{esc(advice)}</p></div><h2>Related AI tools to compare</h2><div class="content-hub-grid">{tool_cards}</div><h2>Next steps</h2><div class="content-hub-grid"><article class="content-hub-card"><h3>Estimate cost</h3><p>Check whether related tools are free, freemium, or likely to create subscription sprawl.</p><a class="button button-blue small" href="/cost-calculator.html">Open calculator</a></article><article class="content-hub-card"><h3>Compare alternatives</h3><p>Use alternatives pages before replacing a tool in your stack.</p><a class="button button-blue small" href="/alternatives/">Open alternatives</a></article></div></div></section><script type="application/ld+json">{json.dumps(faq)}</script></main>{FOOTER}{scripts()}</body></html>'
        (out / f"{slug}.html").write_text(page)
        cards.append(f'<article class="content-hub-card"><span>Glossary</span><h3><a href="/glossary/{slug}.html">{esc(term)}</a></h3><p>{esc(definition)}</p><a class="button button-blue small" href="/glossary/{slug}.html">Read definition</a></article>')
    index_desc = "Plain-English AI tool definitions for buyers comparing agents, copilots, RAG, context windows, automations, shortlists, and pricing models."
    index = f'<!doctype html><html lang="en">{head("AI Tools Glossary", index_desc, DOMAIN+"/glossary/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Glossary</p><h1>AI tool terms without vendor fog.</h1><p class="subhead">Use these definitions to evaluate tools, compare pricing pressure, and avoid buying terminology instead of workflow value.</p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{"".join(cards)}</div></div></section></main>{FOOTER}{scripts()}</body></html>'
    (out / "index.html").write_text(index)


def generate_pricing_index(root: Path, tools: list[dict[str, Any]]) -> None:
    groups = {
        "Free or free-tier AI tools": [t for t in tools if "free" in t.get("price", "").lower()],
        "Paid-only AI tools": [t for t in tools if "paid" in t.get("price", "").lower() and "free" not in t.get("price", "").lower()],
        "Open/self-hostable or low-control-risk tools": [t for t in tools if any(x in " ".join(t.get("summary", "") if isinstance(t.get("summary", ""), str) else t.get("summary", [])).lower() + " " + " ".join(t.get("best_for", "") if isinstance(t.get("best_for", ""), str) else t.get("best_for", [])).lower() + " " + t.get("price", "").lower() for x in ["self-host", "open", "technical"])],
    }
    sections = []
    for name, items in groups.items():
        cards = "".join(tool_card(t) for t in items[:12]) or '<p>No matching tools yet.</p>'
        sections.append(f'<section style="margin:48px 0"><h2>{esc(name)}</h2><p>Use this group to plan trials, compare upgrade pressure, and avoid overlapping subscriptions.</p><div class="content-hub-grid">{cards}</div></section>')
    desc = "Browse AI tools by pricing model: free, freemium, paid-only, self-hostable, and low-control-risk options before committing to subscriptions."
    page = f'<!doctype html><html lang="en">{head("AI Tool Pricing Index", desc, DOMAIN+"/pricing-index/")}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:920px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Pricing index</p><h1>Compare AI tools by pricing pressure.</h1><p class="subhead">Find free-tier tools, paid-only tools, and lower-control-risk options before your AI subscriptions sprawl.</p><p><a class="button button-blue" href="/cost-calculator.html">Estimate stack cost</a><a class="button button-blue" href="/free-ai-tools.html" style="margin-left:8px">Browse free tools</a></p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Planning rule</span><p>Do not optimize for the cheapest tool in isolation. Optimize for the smallest stack that solves a weekly workflow and keeps data, export, and collaboration requirements clear.</p></div>{"".join(sections)}</div></section></main>{FOOTER}{scripts()}</body></html>'
    out = root / "pricing-index" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)


def generate_ai_index(root: Path, tools: list[dict[str, Any]], today: str) -> None:
    pages = [
        {"title": "Stack Builder", "url": f"{DOMAIN}/stack-builder.html", "type": "utility", "summary": "Generate a shareable AI stack."},
        {"title": "Cost Calculator", "url": f"{DOMAIN}/cost-calculator.html", "type": "utility", "summary": "Estimate monthly AI tool stack cost."},
        {"title": "Tool Finder", "url": f"{DOMAIN}/tool-finder.html", "type": "utility", "summary": "Filter tools by workflow, budget, and buyer."},
        {"title": "Glossary", "url": f"{DOMAIN}/glossary/", "type": "knowledge", "summary": "Plain-English AI tool definitions."},
        {"title": "Pricing Index", "url": f"{DOMAIN}/pricing-index/", "type": "knowledge", "summary": "Browse tools by pricing pressure."},
    ]
    data = {
        "site": "AIToolsEssentials",
        "domain": DOMAIN,
        "generated": today,
        "tools_count": len(tools),
        "core_pages": pages,
        "tool_reviews": [{"name": t["name"], "slug": t["slug"], "category": t.get("category"), "price": t.get("price"), "url": f"{DOMAIN}/tools/{t['slug']}/"} for t in tools],
        "editorial_note": "AIToolsEssentials separates editorial scoring from affiliate and sponsor relationships.",
    }
    (root / "ai-index.json").write_text(json.dumps(data, indent=2) + "\n")


def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    tools_list: list[dict[str, Any]] = tools if tools is not None else json.loads((root / "data/tools.json").read_text())
    today = today or datetime.today().strftime("%Y-%m-%d")
    generate_glossary(root, tools_list)
    generate_pricing_index(root, tools_list)
    generate_ai_index(root, tools_list, today)
    return len(GLOSSARY) + 3


def inject_site_schema(root: Path, tools: list[dict[str, Any]] | None = None) -> None:
    marker_start = "<!-- AIT KNOWLEDGE SCHEMA START -->"
    marker_end = "<!-- AIT KNOWLEDGE SCHEMA END -->"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": f"{DOMAIN}/#organization", "name": "AIToolsEssentials", "url": DOMAIN, "email": EMAIL, "logo": f"{DOMAIN}/assets/aitools-bot-mark.svg"},
            {"@type": "WebSite", "@id": f"{DOMAIN}/#website", "url": DOMAIN, "name": "AIToolsEssentials", "publisher": {"@id": f"{DOMAIN}/#organization"}, "potentialAction": {"@type": "SearchAction", "target": f"{DOMAIN}/tools/index.html?q={{search_term_string}}", "query-input": "required name=search_term_string"}},
        ],
    }
    block = f'\n{marker_start}\n<script type="application/ld+json">{json.dumps(schema, separators=(",", ":"))}</script>\n{marker_end}\n'
    for p in root.rglob("*.html"):
        if any(part.startswith(".") for part in p.relative_to(root).parts):
            continue
        html = p.read_text()
        html = re.sub(r"\s*<!-- AIT KNOWLEDGE SCHEMA START -->.*?<!-- AIT KNOWLEDGE SCHEMA END -->\s*", "\n", html, flags=re.S)
        if "</head>" in html:
            html = html.replace("</head>", block + "</head>", 1)
            p.write_text(html)


def postprocess(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> None:
    inject_site_schema(root, tools)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    tools = json.loads((root / "data/tools.json").read_text())
    print(generate(root, tools))
    postprocess(root, tools)
