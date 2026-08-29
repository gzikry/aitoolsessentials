#!/usr/bin/env python3
"""Generate an explainable automation billing-unit calculator and cross-links."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

DOMAIN = "https://aitoolsessentials.com"
MARKER_START = "<!-- AIT AUTOMATION DECODER START -->"
MARKER_END = "<!-- AIT AUTOMATION DECODER END -->"


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> Path:
    tools_list: list[dict[str, Any]] = tools if tools is not None else json.loads((root / "data" / "tools.json").read_text())
    pricing = json.loads((root / "data" / "pricing_snapshots.json").read_text()).get("snapshots", {})
    by_slug = {tool["slug"]: tool for tool in tools_list}
    slugs = ("zapier-ai", "make", "n8n")
    missing = [slug for slug in slugs if slug not in by_slug or slug not in pricing]
    if missing:
        raise ValueError(f"Automation decoder missing tool or pricing records: {missing}")

    source_cards = "".join(
        f'''<article class="content-hub-card"><span>Checked {esc(pricing[slug].get("date"))}</span><h3><a href="/tools/{slug}/">{esc(by_slug[slug].get("name"))}</a></h3><p>{esc(pricing[slug].get("digest"))}</p></article>'''
        for slug in slugs
    )
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Automation Cost Decoder",
        "url": f"{DOMAIN}/automation-cost-decoder/",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Any",
        "description": "Compare estimated Zapier tasks, Make credits, and n8n workflow executions for the same automation shape.",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    }, separators=(",", ":"))

    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Estimate the billing units behind one automation: Zapier tasks, Make credits, and n8n executions, with current official-pricing context."><title>Zapier vs Make vs n8n Cost Calculator — Automation Billing Decoder</title><link rel="canonical" href="{DOMAIN}/automation-cost-decoder/"><link rel="stylesheet" href="../css/styles.css"><link rel="stylesheet" href="../css/share.css"><script type="application/ld+json">{schema}</script></head><body>
<header class="global-nav"><a class="brand" href="/"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/zapier-ai/">Zapier</a><a href="/tools/make/">Make</a><a href="/tools/n8n/">n8n</a><a href="/comparisons/zapier-vs-make-vs-n8n.html">Full comparison</a><a href="/pricing-watch/">Pricing Watch</a></nav><a class="nav-cta" href="/newsletter/">Keep/Cut Weekly</a></header>
<main><section class="scene scene-dark"><div style="max-width:900px;margin:0 auto;padding:86px 28px 68px;text-align:center"><p class="kicker light">Free automation cost decoder</p><h1>Translate one workflow into tasks, credits, and executions.</h1><p class="subhead">Zapier, Make, and n8n meter automation differently. Enter your workflow shape to compare billing units before comparing plan prices.</p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card viral-control"><span>Your workflow</span><div class="viral-controls"><label>Workflow runs per month<input id="automationRuns" type="number" min="1" max="10000000" value="1000"></label><label>Billable actions per run<input id="automationSteps" type="number" min="1" max="1000" value="5"></label><label>AI multiplier<input id="automationAiMultiplier" type="number" min="1" max="5" step="1" value="1"></label></div><p class="muted-small">Use the AI multiplier only when a platform's selected AI action consumes more than one base unit. Check the builder and plan terms before purchase.</p><p><button class="button button-blue" id="decodeAutomation">Decode billing units</button></p></div>
<div id="automationResult" class="viral-result-card" aria-live="polite"><span>Monthly planning estimate</span><h2>5,000 action units · 1,000 workflow executions</h2><div class="content-hub-grid"><article class="content-hub-card"><h3>Zapier</h3><p><strong>~5,000 tasks</strong></p><p>Planning assumption: each successful billable action uses one task; selected AI actions and tool calls can use more.</p></article><article class="content-hub-card"><h3>Make</h3><p><strong>~5,000 credits</strong></p><p>Planning assumption: most module actions use one credit; AI and other modules can consume more.</p></article><article class="content-hub-card"><h3>n8n</h3><p><strong>~1,000 executions</strong></p><p>Cloud plans meter complete workflow executions with unlimited steps; AI-credit allowances are separate.</p></article></div></div>
<section class="score-card"><span>Read this correctly</span><h2>This compares meters—not final invoices.</h2><p>A five-step workflow run 1,000 times can resemble 5,000 action-based units but only 1,000 execution-based units. That does not automatically make one platform cheaper: retries, premium apps, AI calls, polling, data transfer, self-hosting labor, and annual billing change the result.</p><p><a class="button button-blue" href="/comparisons/zapier-vs-make-vs-n8n.html">Read the full comparison</a><a class="button button-dark" href="/workflows/client-onboarding-automation.html" style="margin-left:8px">Test a real workflow</a></p></section>
<h2>Current official-pricing context</h2><div class="content-hub-grid">{source_cards}</div>
<h2>How to choose with this estimate</h2><ol><li>Map one real workflow from trigger to final action.</li><li>Count the actions that would consume a task or credit on every run.</li><li>Include retries, branches, polling, and AI-call multipliers.</li><li>Run the same workflow on free or trial access.</li><li>Compare the resulting unit count with the current official plan limits—not an old review screenshot.</li></ol>
<section class="newsletter-panel"><div><span>Keep/Cut Weekly</span><h2>Get one overlap or pricing decision each week.</h2><p>Verified pricing changes, one workflow to test, and a clear keep/cut question before renewal.</p></div><div class="newsletter-actions"><a class="button button-blue" href="/newsletter/">Read the newsletter</a><a class="button button-dark" href="/pricing-watch/">Open Pricing Watch</a></div></section></div></section></main>
<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/comparisons/zapier-vs-make-vs-n8n.html">Full comparison</a><a href="/evidence/">Evidence</a><a href="/legal/editorial-methodology.html">Methodology</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a></footer>
<script>(()=>{{const nf=new Intl.NumberFormat();function render(){{const runs=Math.max(1,Number(document.getElementById('automationRuns').value||1));const steps=Math.max(1,Number(document.getElementById('automationSteps').value||1));const mult=Math.max(1,Number(document.getElementById('automationAiMultiplier').value||1));const action=Math.round(runs*steps*mult);document.getElementById('automationResult').innerHTML=`<span>Monthly planning estimate</span><h2>${{nf.format(action)}} action units · ${{nf.format(runs)}} workflow executions</h2><div class="content-hub-grid"><article class="content-hub-card"><h3>Zapier</h3><p><strong>~${{nf.format(action)}} tasks</strong></p><p>Base planning estimate; selected AI actions and tool calls can consume more.</p></article><article class="content-hub-card"><h3>Make</h3><p><strong>~${{nf.format(action)}} credits</strong></p><p>Base planning estimate; AI and other modules can consume more.</p></article><article class="content-hub-card"><h3>n8n</h3><p><strong>~${{nf.format(runs)}} executions</strong></p><p>Complete workflow runs; cloud AI-credit allowances are separate.</p></article></div>`;}}document.getElementById('decodeAutomation').addEventListener('click',render);}})();</script><script src="../js/site.js" defer></script><script src="../js/analytics.js" defer></script></body></html>'''
    out = root / "automation-cost-decoder" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    postprocess(root)
    return out


def postprocess(root: Path) -> int:
    targets = [
        root / "tools" / "zapier-ai" / "index.html",
        root / "tools" / "make" / "index.html",
        root / "tools" / "n8n" / "index.html",
        root / "comparisons" / "zapier-vs-make-vs-n8n.html",
        root / "categories" / "Automation" / "index.html",
        root / "articles" / "make-vs-zapier-which-to-pay-for.html",
        root / "workflows" / "client-onboarding-automation.html",
    ]
    block = f'''\n{MARKER_START}\n<section class="score-card"><span>Automation billing decoder</span><h2>Translate this workflow into billing units.</h2><p>Estimate Zapier tasks, Make credits, and n8n executions for the same monthly run volume before comparing plan prices.</p><p><a class="button button-blue" href="/automation-cost-decoder/">Open the free decoder</a></p></section>\n{MARKER_END}\n'''
    changed = 0
    for path in targets:
        if not path.exists():
            continue
        old = path.read_text()
        new = re.sub(rf"\s*{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\s*", "\n", old, flags=re.S)
        if "</main>" in new:
            new = new.replace("</main>", block + "</main>", 1)
        if new != old:
            path.write_text(new)
            changed += 1
    return changed


if __name__ == "__main__":
    project = Path(__file__).resolve().parents[1]
    print(generate(project))
