#!/usr/bin/env python3
"""Generate long-tail AI workflow pages for organic visitor growth.

These are not generic blog stubs: each page is sourced from data/workflows.json
and existing tool records, then routes readers into reviews, Fit Interview,
Stack Builder, Pricing Watch, Evidence Ledger, and Decision Brief.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
HEADER = '<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/use-cases/">Use cases</a><a href="/workflows/">Workflows</a><a href="/fit-interview/">Fit interview</a><a href="/pricing-watch/">Pricing Watch</a><a href="/evidence/">Evidence</a></nav><a class="nav-cta" href="/premium/">Premium</a></header>'
FOOTER = f'<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/advertise/index.html" rel="nofollow">Advertise</a><a href="/submit-tool.html" rel="nofollow">Submit a tool</a><a href="/community/test-report.html" rel="nofollow">Report your results</a><a href="/badges/">Badges</a><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a></footer>'


def esc(v: Any) -> str:
    return escape(str(v or ""), quote=True)


def jsonld(data: dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":")).replace("</", "<\\/")


def head(title: str, desc: str, canonical: str, schema: dict[str, Any] | None = None) -> str:
    schema_html = f'<script type="application/ld+json">{jsonld(schema)}</script>' if schema else ""
    return f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(desc)}"><title>{esc(title)}</title><link rel="canonical" href="{esc(canonical)}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/css/styles.css">{schema_html}</head>'


def tool_card(tool: dict[str, Any], position: int) -> str:
    slug = tool["slug"]
    return f'''<article class="content-hub-card">
<span>#{position} · {esc(tool.get("category"))} · {esc(tool.get("price"))}</span>
<h3><a href="/tools/{esc(slug)}/">{esc(tool.get("name", slug))}</a></h3>
<p>{esc(tool.get("summary") or tool.get("best_for"))}</p>
<ul><li><strong>Best for:</strong> {esc(tool.get("best_for"))}</li><li><strong>Trial test:</strong> use one real workflow before upgrading.</li></ul>
<p><a class="button button-blue small" href="/tools/{esc(slug)}/">Read review</a><a class="button button-blue small" href="/pricing-watch/" style="margin-left:8px">Check price</a></p>
</article>'''


def generate(root: Path) -> int:
    workflows = json.loads((root / "data/workflows.json").read_text())
    tools = {t["slug"]: t for t in json.loads((root / "data/tools.json").read_text())}
    today = datetime.now().strftime("%Y-%m-%d")
    out = root / "workflows"
    out.mkdir(exist_ok=True)
    index_cards: list[str] = []

    seen = set()
    for wf in workflows:
        slug = wf.get("slug")
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in seen:
            raise ValueError(f"Invalid or duplicate workflow slug: {slug!r}")
        seen.add(slug)
        primary = wf.get("primary_tools", [])
        if not isinstance(primary, list) or not primary:
            raise ValueError(f"Workflow {slug} has no primary_tools list")
        missing = [s for s in primary if s not in tools]
        if missing:
            raise ValueError(f"Workflow {slug} references unknown tools: {missing}")

        selected = [tools[s] for s in primary]
        title = wf["title"]
        desc = wf["description"]
        audience = wf.get("audience", "")
        query_list = wf.get("search_queries", [])
        steps = wf.get("decision_steps", [])
        guardrails = wf.get("guardrails", [])
        if guardrails is not None and not isinstance(guardrails, list):
            raise ValueError(f"Workflow {slug} guardrails must be a list")
        cards = "".join(tool_card(t, i) for i, t in enumerate(selected, 1))
        step_items = "".join(f"<li>{esc(step)}</li>" for step in steps)
        guardrail_block = ""
        if guardrails:
            guardrail_items = "".join(f"<li>{esc(item)}</li>" for item in guardrails)
            guardrail_block = f'<h2>Safety and compliance guardrails</h2><div class="score-card"><ul>{guardrail_items}</ul></div>'
        query_items = "".join(f"<li>{esc(q)}</li>" for q in query_list)
        schema = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": title,
            "description": desc,
            "url": f"{DOMAIN}/workflows/{slug}.html",
            "dateModified": today,
            "itemListElement": [
                {"@type": "ListItem", "position": i, "url": f"{DOMAIN}/tools/{t['slug']}/", "name": t.get("name", t["slug"])}
                for i, t in enumerate(selected, 1)
            ],
        }
        page = f'''<!doctype html><html lang="en">{head(title + " | AIToolsEssentials", desc, DOMAIN + "/workflows/" + slug + ".html", schema)}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:960px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Workflow guide · updated {esc(today)}</p><h1>{esc(title)}</h1><p class="subhead">{esc(desc)}</p><p><a class="button button-blue" href="/fit-interview/">Find your fit</a><a class="button button-blue" href="/stack-builder.html" style="margin-left:8px">Build a stack</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Who this helps</span><h2>{esc(audience)}</h2><p>This page is built for searchers who already know the workflow they need to improve. It does not claim a universal winner; it routes you to evidence, pricing checks, and a repeatable trial.</p></div><h2>Recommended tools for this workflow</h2><div class="content-hub-grid">{cards}</div><h2>How to test before paying</h2><div class="score-card"><ol>{step_items}</ol></div>{guardrail_block}<h2>Search intents this page covers</h2><div class="score-card"><ul>{query_items}</ul><p class="benchmark-caveat">These are editorial targeting notes, not traffic or ranking claims.</p></div><div class="content-hub-grid"><article class="content-hub-card"><h3>Compare finalists</h3><p>Put 2–3 tools into a shortlist and compare cost, overlap, and trial criteria.</p><a class="button button-blue small" href="/compare-shortlist.html">Compare shortlist</a></article><article class="content-hub-card"><h3>Inspect evidence</h3><p>Open source links, pricing dates, unresolved claims, and methodology before buying.</p><a class="button button-blue small" href="/evidence/">Open Evidence Ledger</a></article><article class="content-hub-card"><h3>Save the decision</h3><p>Generate a decision brief you can share with a client, manager, or team.</p><a class="button button-blue small" href="/decision-brief.html">Create brief</a></article></div></div></section>
</main>{FOOTER}<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script></body></html>'''
        (out / f"{slug}.html").write_text(page)
        index_cards.append(f'<article class="content-hub-card"><span>{esc(audience)}</span><h3><a href="/workflows/{esc(slug)}.html">{esc(title)}</a></h3><p>{esc(desc)}</p><a class="button button-blue small" href="/workflows/{esc(slug)}.html">Open workflow</a></article>')

    index_schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "AI Workflow Guides", "url": f"{DOMAIN}/workflows/", "description": "Long-tail AI workflow guides that map jobs to tools, trials, pricing checks, and evidence.", "dateModified": today}
    index_desc = "Browse AI workflow guides for property manager operations, rental listing copy, podcast editing, nonprofit grant writing, classroom lesson planning, consultant admin, knowledge bases, transcript newsletters, coding-assistant security reviews, and commercial image rights."
    index = f'''<!doctype html><html lang="en">{head("AI Workflow Guides — Find Tools by Job", index_desc, DOMAIN+"/workflows/", index_schema)}<body>{HEADER}<main><section class="scene scene-dark"><div style="max-width:960px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Organic growth library · updated {esc(today)}</p><h1>Find AI tools by the workflow you need to fix.</h1><p class="subhead">Search-friendly workflow pages that connect real jobs to reviewed tools, trial checklists, pricing checks, and evidence.</p><p><a class="button button-blue" href="/tool-finder.html">Use Tool Finder</a><a class="button button-blue" href="/use-cases/" style="margin-left:8px">Browse use cases</a></p></div></section><section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{"".join(index_cards)}</div></div></section></main>{FOOTER}<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script></body></html>'''
    (out / "index.html").write_text(index)

    home = root / "index.html"
    if home.exists():
        html = home.read_text()
        block = f'''\n<!-- AIT WORKFLOW LIBRARY PROMO START -->\n<section class="scene scene-light guide-strip"><div><p class="kicker light">Workflow search guides</p><h2>New: AI tools by job-to-be-done.</h2><p>Built for visitors searching for concrete workflows — property manager operations, rental listings, podcast editing, nonprofit grants, consultant admin, and more.</p><div class="guide-pill-grid"><a class="guide-pill" href="workflows/">Browse workflow guides</a><a class="guide-pill" href="articles/best-ai-tools-for-property-managers.html">AI tools for property managers</a><a class="guide-pill" href="workflows/property-manager-operations.html">Property manager operations</a><a class="guide-pill" href="workflows/rental-listing-copy.html">Rental listing copy</a><a class="guide-pill" href="articles/best-ai-tools-for-podcast-shows.html">AI tools for podcasters</a><a class="guide-pill" href="articles/best-ai-tools-for-nonprofits.html">AI tools for nonprofits</a></div></div></section>\n<!-- AIT WORKFLOW LIBRARY PROMO END -->\n'''
        html = re.sub(r"\s*<!-- AIT WORKFLOW LIBRARY PROMO START -->.*?<!-- AIT WORKFLOW LIBRARY PROMO END -->\s*", "\n", html, flags=re.S)
        anchor = '<!-- AIT LEAD MAGNET START -->'
        if anchor in html:
            html = html.replace(anchor, block + anchor, 1)
        else:
            html = html.replace("</main>", block + "</main>", 1)
        home.write_text(html)

    return len(workflows) + 1


def main() -> None:
    import sys
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    print(generate(root))


if __name__ == "__main__":
    main()
