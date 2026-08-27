#!/usr/bin/env python3
"""Generate public premium pages and Whop-ready member content assets."""
from __future__ import annotations

import csv
import json
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

DOMAIN = "https://aitoolsessentials.com"
EMAIL = "contact@aitoolsessentials.com"
WHOP_CHECKOUT = "https://whop.com/checkout/ch_DKm5yxA1OBXoDru/"
WHOP_CHECKOUT_PROMO = "https://whop.com/checkout/ch_DKm5yxA1OBXoDru/?promo=LAUNCH50"
WHOP_PROMO_CODE = "LAUNCH50"
WHOP_TRIAL_DAYS = 7
HEADER = '<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/stack-builder.html">Stack builder</a><a href="/tool-finder.html">Tool finder</a><a href="/free-ai-tools.html">Free AI tools</a><a href="/alternatives/">Alternatives</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/resources/">Resources</a><a href="/premium/">Premium</a></nav><a class="nav-cta" href="/pricing/">Subscribe</a></header>'
FOOTER = f'<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/advertise/index.html" rel="nofollow">Advertise</a><a href="/submit-tool.html" rel="nofollow">Submit a tool</a><a href="/community/test-report.html" rel="nofollow">Report your results</a><a href="/badges/">Badges</a><a href="/legal/affiliate-disclosure.html" rel="nofollow">Affiliate disclosure</a><a href="mailto:{EMAIL}">Contact</a><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a></footer>'


def esc(s: Any) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def head(title: str, desc: str, canonical: str, noindex: bool = False) -> str:
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return f'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{robots}<meta name="description" content="{esc(desc)}"><title>{esc(title)}</title><link rel="canonical" href="{canonical}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{DOMAIN}/assets/og-ai-tools.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/css/styles.css"><link rel="stylesheet" href="/css/share.css"></head>'


def scripts() -> str:
    return '<script src="/js/site.js" defer></script><script src="/js/analytics.js" defer></script>'


def jsonld(data: dict[str, Any]) -> str:
    return '<script type="application/ld+json">' + json.dumps(data, separators=(",", ":")) + '</script>'


def category_top_tools(tools: list[dict[str, Any]], category: str, limit: int = 5) -> list[dict[str, Any]]:
    return sorted([t for t in tools if category.lower() in str(t.get("category", "")).lower()], key=lambda t: float(t.get("rating", 0) or 0), reverse=True)[:limit]


def generate_public_pages(root: Path, tools: list[dict[str, Any]], today: str) -> None:
    out = root / "premium"
    out.mkdir(exist_ok=True)
    library_cards = [
        ("Monthly research briefing", "A dated, source-led briefing on tool changes, pricing shifts, and what to watch before renewing subscriptions."),
        ("Monthly decision matrix", "Downloadable CSV comparing all 61 tracked AI tools by category, pricing, use cases, and trial priority. Refreshed monthly."),
        ("Deep-dive workflow report", "One practical workflow per month compared across tools with testing plan, decision matrix, and cost notes."),
        ("CSV decision archive", "Downloadable scorecards for sorting tools by workflow, pricing pressure, policy risk, and trial priority."),
        ("Member request thread", "Subscribers vote on the next workflow to test. Requests shape future premium research."),
        ("Audit-style playbooks", "Strategy-only templates for cutting tool sprawl, choosing alternatives, and preparing vendor/security questions."),
        ("Update notes", "Source-dated alerts when pricing, policies, or plan names change across tracked tools."),
        ("AI Stack Audit Template", "Fillable CSV that maps every tool you pay for, weekly usage, overlap, and cancellation risk. Reply with your audit for a personalized stack recommendation within 48 hours."),
        ("Weekly AI Stack Checklist", "A 7-day rhythm for keeping your stack lean: check alerts, test tools, log friction, and make data-driven cut/keep decisions in 15 minutes per week."),
        ("Tool-Change Alert Feed", "Curated monthly feed of pricing, model, and feature changes across all 61 tracked tools — delivered to members before the public change-radar page."),
        ("Hands-On Comparison Protocol", "Fillable comparison CSV for running identical tasks across ChatGPT, Claude, Grok, and Gemini. Stop reading reviews — test the tools yourself in 30 minutes."),
        ("AI ROI Calculator", "Template that measures whether your AI spend is actually paying for itself: time saved x hourly rate minus monthly tool costs."),
        ("Priority research slots", "First 5 members each month get their specific workflow researched and delivered as a CSV + brief in the next monthly drop."),
        ("30-day renewal/cancel calendar", "Day-by-day operating system for the trial week and first month so Premium is used, not collected."),
        ("Free vs Premium value matrix", "Honest table of what stays free vs what $12 buys, so members can judge payback in one page."),
        ("Cancel-savings tracker", "Log cancelled or downgraded seats. If monthly saves exceed $12, Premium has paid for itself."),
        ("Vendor/security questions pack", "Structured procurement questions before client data touches a new tool."),
        ("Coding assistant shortlist", "Force a single primary coding tool instead of paying for Cursor plus Copilot plus chat coding seats."),
    ]
    cards = "".join(f'<article class="content-hub-card"><span>Premium deliverable</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>' for title, text in library_cards)
    deliverables = [
        "Welcome/start-here post with 7-day free trial and LAUNCH50 first-month discount",
        "Full 61-tool decision matrix CSV (refreshed monthly)",
        "AI Stack Audit Template + personalized 48-hour stack recommendation",
        "Weekly AI Stack Checklist (15-minute lean-stack rhythm)",
        "Tool-Change Alert Feed (pricing, models, features — members first)",
        "Hands-On Comparison Protocol (ChatGPT vs Claude vs Grok vs Gemini)",
        "AI ROI Calculator template",
        "Priority research slots (first 5 member requests each month)",
        "September–November archive: cost-cutting, visual/meeting stacks, assistant protocols",
        "Vendor/security questions pack and automation pricing decoder",
        "30-day renewal/cancel calendar + first-15-minutes onboarding sheet",
        "Free vs Premium value matrix and cancel-savings tracker",
        "Coding assistant shortlist and sample filled stack-audit example",
    ]
    deliverable_list = "".join(f"<li>{esc(x)}</li>" for x in deliverables)
    desc = "AIToolsEssentials Premium is a $12/month Whop membership with a 7-day free trial, monthly AI tool research briefs, stack-audit templates, weekly checklists, tool-change alerts, hands-on comparison protocols, ROI calculators, and priority research slots."
    page = f'''<!doctype html><html lang="en">{head("Premium AI Tool Research Membership", desc, DOMAIN+"/premium/")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Premium research membership</p><h1>Give subscribers more than access. Give them decisions.</h1><p class="subhead">A $12/month Whop membership for people who want dated research briefs, side-by-side decision archives, workflow playbooks, and pricing/policy alerts before they buy more AI tools. <strong>7-day free trial.</strong></p><p><a class="button button-blue" href="{WHOP_CHECKOUT}" rel="external noopener" data-whop-checkout="plan_FNXWs3suBFwDN">Start 7-day free trial</a><a class="button button-blue" href="{WHOP_CHECKOUT_PROMO}" rel="external noopener" style="margin-left:8px">Use code LAUNCH50 — 50% off</a><a class="button button-blue" href="/premium/sample-report.html" style="margin-left:8px">See sample report</a></p><p class="affiliate-inline">7-day free trial, then $12/month. Use code <strong>LAUNCH50</strong> for 50% off your first paid month. Cancel anytime. Billing, login, cancellation, and member access are handled by Whop. Research and strategy only — no implementation, setup, account access, credentials, or ongoing support.</p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>What members get immediately</span><h2>A real member library from day one.</h2><ul>{deliverable_list}</ul><p><a class="button button-blue" href="/premium/roadmap.html">View roadmap</a><a class="button button-blue" href="/premium/archive.html" style="margin-left:8px">Archive preview</a><a class="button button-blue" href="/premium/faq.html" style="margin-left:8px">Premium FAQ</a></p></div><h2>Premium content library</h2><div class="content-hub-grid">{cards}</div><section class="score-card"><span>Scope boundary</span><h2>Premium does not buy rankings or implementation help.</h2><p>Premium is a research membership. It does not change public editorial rankings, sponsor labels, affiliate disclosures, or review scores. It does not include setup, integrations, credential handling, or technical support.</p></section></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "index.html").write_text(page)

    sample_tools = category_top_tools(tools, "General AI Assistant", 5) or tools[:5]
    rows = "".join(f'<tr><td><a href="/tools/{esc(t["slug"])}/">{esc(t["name"])}</a></td><td>{esc(t.get("price"))}</td><td>{esc(t.get("best_for"))}</td><td>{esc(t.get("summary"))}</td></tr>' for t in sample_tools)
    sample_desc = "Sample AIToolsEssentials Premium report showing the structure of monthly member briefings, decision matrices, and source-led recommendations."
    sample = f'''<!doctype html><html lang="en">{head("Sample Premium AI Tool Report", sample_desc, DOMAIN+"/premium/sample-report.html")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Sample member report</p><h1>General AI assistant decision brief.</h1><p class="subhead">This public sample shows the format. Paid Whop members get the full monthly archive, CSV files, stack-audit templates, weekly checklists, tool-change alerts, hands-on protocols, and priority research slots.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT}" rel="external noopener">Subscribe on Whop</a><a class="button button-blue" href="/pricing/" style="margin-left:8px">Compare plans</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Sample recommendation</span><h2>Pick by workflow, not by brand.</h2><p>For general AI assistants, the member report separates everyday drafting, source-backed research, long-context document work, coding help, and organization controls. The public sample is intentionally partial; members get the full source-dated matrix and CSV.</p></div><div class="table-wrap"><table><thead><tr><th>Tool</th><th>Pricing model</th><th>Best fit</th><th>Sample note</th></tr></thead><tbody>{rows}</tbody></table></div><h2>What full members receive</h2><div class="content-hub-grid"><article class="content-hub-card"><h3>Full matrix</h3><p>All 61 tracked tools scored across workflow fit, pricing pressure, data controls, and trial priority — refreshed monthly.</p></article><article class="content-hub-card"><h3>Stack audit + ROI tools</h3><p>Fillable audit template, weekly checklist, and ROI calculator so members cut overlap with a defensible process.</p></article><article class="content-hub-card"><h3>Hands-on protocols</h3><p>Identical-task comparison sheets for assistants, plus tool-change alerts before public pages catch up.</p></article><article class="content-hub-card"><h3>Priority research</h3><p>First 5 member requests each month become the next CSV + brief drop.</p></article></div></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "sample-report.html").write_text(sample)

    roadmap_desc = "AIToolsEssentials Premium monthly research roadmap and member deliverable calendar."
    roadmap_items = [
        ("September", "Cut AI subscription sprawl", "Decision matrix, general assistant shortlist, automation pricing decoder, vendor security questions."),
        ("October", "Visual and meeting stacks", "Refreshed decision matrix, visual AI shortlist, meeting-notes decision sheet, and pricing-watch handoff."),
        ("November", "Premium content engine", "Stack audit template, weekly checklist, tool-change alert feed, hands-on assistant protocol, ROI calculator, and priority research slots."),
        ("December", "Content production stack", "ChatGPT, Claude, Jasper, Copy.ai, Canva AI, Descript, and distribution workflow playbook."),
        ("Ongoing", "Member-driven deep dives", "First 5 member requests each month become the next CSV + brief. Weekly checklist and alert feed refresh every month."),
    ]
    roadmap_cards = "".join(f'<article class="content-hub-card"><span>{esc(month)}</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>' for month, title, text in roadmap_items)
    roadmap = f'''<!doctype html><html lang="en">{head("Premium Research Roadmap", roadmap_desc, DOMAIN+"/premium/roadmap.html")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Premium roadmap</p><h1>The member library keeps compounding.</h1><p class="subhead">Premium is not a single PDF. It is a compounding research engine: dated briefs, CSV archives, stack audits, weekly checklists, tool-change alerts, hands-on protocols, and member-requested deep dives.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT}" rel="external noopener">Subscribe on Whop</a><a class="button button-blue" href="/premium/" style="margin-left:8px">Premium overview</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><h2>Research calendar</h2><div class="content-hub-grid">{roadmap_cards}</div><section class="score-card"><span>Member-driven</span><h2>Requests shape the calendar.</h2><p>Whop members can request workflows to compare. Good requests include your role, current stack, weekly task, budget, data constraints, and tools you are deciding between.</p></section></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "roadmap.html").write_text(roadmap)

    archive_desc = "AIToolsEssentials Premium archive preview for monthly AI tool research drops."
    archive_rows = "".join([
        '<tr><td>2026-09</td><td>AI stack cost-cutting brief</td><td>Decision matrix CSV, assistant shortlist, automation decoder, vendor questions</td><td>Live in Whop archive</td></tr>',
        '<tr><td>2026-10</td><td>Visual and meeting stacks</td><td>Refreshed matrix, visual shortlist, meeting-notes decision sheet</td><td>Live in Whop archive</td></tr>',
        '<tr><td>2026-11</td><td>Premium content engine</td><td>Stack audit, weekly checklist, alert feed, hands-on protocol, ROI calculator, 30-day calendar, value matrix, priority slots</td><td>Live in Whop (pinned welcome)</td></tr>',
        '<tr><td>2026-12</td><td>Content production stack</td><td>Writing/design/video workflow playbook and CSV archive</td><td>Planned</td></tr>',
    ])
    archive = f'''<!doctype html><html lang="en">{head("Premium Research Archive Preview", archive_desc, DOMAIN+"/premium/archive.html")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Premium archive</p><h1>Monthly research drops, organized for members.</h1><p class="subhead">A public preview of the member archive structure. Full posts, CSVs, and request threads live inside Whop.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT}" rel="external noopener">Subscribe on Whop</a><a class="button button-blue" href="/premium/sample-report.html" style="margin-left:8px">See sample report</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="table-wrap"><table><thead><tr><th>Month</th><th>Drop</th><th>Member files</th><th>Status</th></tr></thead><tbody>{archive_rows}</tbody></table></div><section class="score-card"><span>Access note</span><h2>Full archive access is through Whop.</h2><p>Subscribers receive the actual posts, downloads, and request threads in the Whop member area. This page is a transparent preview, not the gated archive itself.</p></section></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "archive.html").write_text(archive)

    faq_desc = "Premium membership FAQ for AIToolsEssentials Whop subscribers."
    faqs = [
        ("What do I get immediately after subscribing?", "Access is handled through Whop. Day one includes the start-here post, full 61-tool decision matrix, AI Stack Audit Template, Weekly AI Stack Checklist, Tool-Change Alert Feed, Hands-On Comparison Protocol, AI ROI Calculator, September–November archive packs, vendor/security questions, and the member request thread with priority research slots."),
        ("Is Premium a course, community, or consulting service?", "It is a research membership. Premium gives you decision briefs, CSVs, stack-audit templates, weekly checklists, hands-on protocols, playbooks, and request threads. It does not include implementation, setup, integrations, account access, credential handling, or ongoing technical support. Personalized stack recommendations from the audit template are strategy-only written replies — not hands-on implementation."),
        ("Can Premium vendors pay to change rankings?", "No. Premium does not change public editorial rankings, sponsor labels, affiliate disclosures, or review scores. Paid visibility and editorial scoring remain separate."),
        ("How does billing and cancellation work?", "Billing, login, member access, and cancellation are handled by Whop. New members get a 7-day free trial, then $12/month. Use code LAUNCH50 for 50% off the first paid month (new users only). Cancel anytime from your Whop account."),
        ("Are refunds offered?", "No. The current Premium terms state all sales are final and there are no refunds. Use the 7-day free trial, sample report, roadmap, archive preview, and terms before subscribing."),
        ("How do member requests work?", "Members can post the workflows they want compared next. Good requests include role, current stack, weekly task, candidate tools, budget, and data constraints. The first 5 complete requests each month become priority research slots delivered as a CSV + brief in the next drop."),
        ("What is the AI Stack Audit?", "Download the fillable CSV, list every AI tool you pay for with cost and weekly usage, then reply with your completed audit. Within 48 hours you get a strategy-only keep/cut/trial/switch recommendation. No account access required."),
        ("Is Premium worth $12/month?", "Yes if you already spend on multiple AI tools, have overlap, or have a renewal coming up, and you will use the audit and checklist in week one. No if you only use one free assistant occasionally. One cancelled unused seat usually covers months of Premium. Use the 7-day trial: if you have not made a keep/cut decision by day 7, cancel."),
        ("What should I do in the first 15 minutes?", "Open the pinned welcome post, download the stack audit and weekly checklist, list every paid AI tool, and put days 0-7 from the renewal/cancel calendar on your calendar. Premium is a research operating system - it only pays off if you use it."),
    ]
    faq_items = "".join(f'<article class="content-hub-card"><h3>{esc(q)}</h3><p>{esc(a)}</p></article>' for q, a in faqs)
    faq_schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    product_schema = {"@context":"https://schema.org","@type":"Product","name":"AIToolsEssentials Premium","description":"Monthly AI tool research membership with briefings, CSV decision archives, stack audits, weekly checklists, tool-change alerts, hands-on protocols, ROI calculators, and member-requested deep dives.","brand":{"@type":"Brand","name":"AIToolsEssentials"},"offers":{"@type":"Offer","price":"12","priceCurrency":"USD","availability":"https://schema.org/InStock","url":WHOP_CHECKOUT},"category":"Research membership"}
    faq = f'''<!doctype html><html lang="en">{head("Premium Membership FAQ", faq_desc, DOMAIN+"/premium/faq.html")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Premium FAQ</p><h1>Know exactly what the Whop membership includes.</h1><p class="subhead">Clear answers on deliverables, billing, cancellations, refunds, editorial independence, and scope boundaries before anyone subscribes.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT}" rel="external noopener">Subscribe on Whop</a><a class="button button-blue" href="/premium/sample-report.html" style="margin-left:8px">See sample report</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{faq_items}</div><section class="score-card"><span>Before launch</span><h2>Whop still needs the member posts uploaded.</h2><p>The site and November content engine pack are ready. George still needs to upload the prepared posts and CSV files to Whop (including the November pack) and run a Whop test transaction before promoting the checkout heavily.</p></section></div></section>
</main>{FOOTER}{jsonld(faq_schema)}{jsonld(product_schema)}{scripts()}</body></html>'''
    (out / "faq.html").write_text(faq)

    welcome_dir = out / "welcome"
    welcome_dir.mkdir(exist_ok=True)
    welcome_desc = "Welcome to AIToolsEssentials Premium. Open your Whop member hub for the full research library."
    welcome = f'''<!doctype html><html lang="en">{head("Welcome to Premium", welcome_desc, DOMAIN+"/premium/welcome/")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Welcome</p><h1>You're in. Open the member library.</h1><p class="subhead">Checkout completed. Your Premium research membership lives in Whop — decision matrices, stack-audit templates, weekly checklists, tool-change alerts, hands-on protocols, and priority research slots.</p><p><a class="button button-blue" href="https://whop.com/hub" rel="external noopener">Open Whop member hub</a><a class="button button-blue" href="/premium/" style="margin-left:8px">Premium overview</a><a class="button button-blue" href="/premium/sample-report.html" style="margin-left:8px">Sample report</a></p><p class="affiliate-inline">Billing, login, cancellation, and member access are handled by Whop. Research and strategy only — no implementation, setup, account access, credentials, or ongoing support.</p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Start here</span><h2>What to do in the first 15 minutes</h2><ol><li>Open the Whop member hub and pin the November welcome post.</li><li>Download the AI Stack Audit Template and list every AI tool you currently pay for.</li><li>Grab the Weekly AI Stack Checklist so next week's review is automatic.</li><li>Reply in the request thread if you want a priority research slot this month.</li></ol></div></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (welcome_dir / "index.html").write_text(welcome)


def write_csv(path: Path, headers: list[str], rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(headers)
        w.writerows(rows)


def generate_whop_pack(root: Path, tools: list[dict[str, Any]], today: str) -> None:
    admin = root / "admin" / "whop-premium"
    admin.mkdir(parents=True, exist_ok=True)
    download_dir = admin / "files"
    download_dir.mkdir(exist_ok=True)

    sorted_tools = sorted(tools, key=lambda t: (str(t.get("category", "")), str(t.get("name", ""))))
    matrix_rows = []
    for t in sorted_tools:
        price = str(t.get("price", ""))
        pressure = "free-first" if "free" in price.lower() else "paid-only" if "paid" in price.lower() else "verify"
        matrix_rows.append([t.get("name"), t.get("slug"), t.get("category"), price, t.get("rating"), pressure, t.get("best_for"), t.get("summary")])
    write_csv(download_dir / "premium-tool-decision-matrix-2026-09.csv", ["name", "slug", "category", "pricing", "editorial_score", "pricing_pressure", "best_for", "summary"], matrix_rows)

    automation = [t for t in tools if "automation" in str(t.get("category", "")).lower() or t.get("slug") in {"zapier-ai", "make", "n8n"}]
    write_csv(download_dir / "automation-pricing-model-decoder-2026-09.csv", ["tool", "slug", "pricing", "best_for", "trial_test"], [[t.get("name"), t.get("slug"), t.get("price"), t.get("best_for"), "Map one real workflow; count task/operation/execution volume before annual billing."] for t in automation])

    assistant = [t for t in tools if "assistant" in str(t.get("category", "")).lower() or t.get("slug") in {"chatgpt", "claude", "gemini", "perplexity", "you-com", "mistral-le-chat", "deepseek"}]
    write_csv(download_dir / "general-ai-assistant-shortlist-2026-09.csv", ["tool", "slug", "pricing", "best_for", "member_note"], [[t.get("name"), t.get("slug"), t.get("price"), t.get("best_for"), "Run the same real task in each shortlisted assistant; compare editing burden and verification effort."] for t in assistant])

    # ---- October member pack (next month's drop, prepared ahead) ----
    write_csv(download_dir / "premium-tool-decision-matrix-2026-10.csv", ["name", "slug", "category", "pricing", "editorial_score", "pricing_pressure", "best_for", "summary"], matrix_rows)

    video = [t for t in tools if any(k in str(t.get("category", "")).lower() for k in ("video", "image")) or t.get("slug") in {"heygen", "synthesia", "midjourney", "leonardo-ai", "gamma"}]
    write_csv(download_dir / "visual-ai-tool-shortlist-2026-10.csv", ["tool", "slug", "pricing", "best_for", "member_note"], [[t.get("name"), t.get("slug"), t.get("price"), t.get("best_for"), "Test with one real brand-styled asset before committing; compare output acceptance rate, not just samples."] for t in video])

    meeting = [t for t in tools if t.get("slug") in {"fireflies", "otter-ai"} or "meeting" in str(t.get("category", "")).lower() or "transcript" in str(t.get("summary", "")).lower()]
    if meeting:
        write_csv(download_dir / "meeting-notes-decision-sheet-2026-10.csv", ["tool", "slug", "pricing", "best_for", "decision_question"], [[t.get("name"), t.get("slug"), t.get("price"), t.get("best_for"), "Does it handle your industry vocabulary and accents? Grade on real meetings only."] for t in meeting])

    oct_posts = "# AIToolsEssentials Premium - Whop Upload Pack - OCTOBER (" + today + ")\n\nPrepared ahead so the next monthly drop is upload-ready. Create these as Whop posts when October begins; attach CSVs from admin/whop-premium/files/.\n\n---\n\n## POST O1 - October drop: what changed since September\n\nWelcome to month two. This month focuses on visual/meeting tool decisions and the new public pricing tracker.\n\n**New files this month:**\n1. premium-tool-decision-matrix-2026-10.csv - refreshed decision matrix (40 tools).\n2. visual-ai-tool-shortlist-2026-10.csv - image/video generation shortlist.\n3. meeting-notes-decision-sheet-2026-10.csv - Fireflies vs Otter style decision sheet.\n\n**Also new on the public site:** AI Pricing Watch (https://aitoolsessentials.com/pricing-watch/) tracks verified price changes across all 40 tools. Members get flagged summaries here first.\n\n---\n\n## POST O2 - October playbook: pick ONE visual AI and stop paying for three\n\nMost teams overlap Midjourney/Leonardo/HeyGen/Synthesia subscriptions. Use the visual shortlist CSV:\n1. List every visual AI you currently pay for.\n2. Score each against your actual monthly output volume.\n3. Cancel down to the single best fit; keep a free tier of a second only if genuinely used.\n\nReply with your current visual stack for a specific recommendation.\n\n---\n\n## POST O3 - October request thread\n\nPost the workflow you want researched next: role, current tools, weekly task volume, budget ceiling. October research slots fill in order of request.\n"
    (admin / "whop-posts-2026-10.md").write_text(oct_posts)

    # ---- November member pack: Premium content engine ----
    write_csv(download_dir / "premium-tool-decision-matrix-2026-11.csv", ["name", "slug", "category", "pricing", "editorial_score", "pricing_pressure", "best_for", "summary"], matrix_rows)

    write_csv(download_dir / "ai-stack-audit-template.csv", ["Field", "Your Answer", "Guidance"], [
        ["Your role/team size", "", "e.g. Solo consultant, 5-person agency, 20-person sales team"],
        ["Monthly AI spend (all tools)", "", "Sum all AI subscription costs"],
        ["Tool 1: Name", "", "e.g. ChatGPT Plus"],
        ["Tool 1: Monthly cost", "", "$/month"],
        ["Tool 1: Weekly use hours", "", "Estimate"],
        ["Tool 1: What it does for you", "", "One sentence"],
        ["Tool 1: Could it be replaced?", "", "By what? Or 'no'"],
        ["Tool 2: Name", "", ""],
        ["Tool 2: Monthly cost", "", ""],
        ["Tool 2: Weekly use hours", "", ""],
        ["Tool 2: What it does for you", "", ""],
        ["Tool 2: Could it be replaced?", "", ""],
        ["Tool 3: Name", "", ""],
        ["Tool 3: Monthly cost", "", ""],
        ["Tool 3: Weekly use hours", "", ""],
        ["Tool 3: What it does for you", "", ""],
        ["Tool 3: Could it be replaced?", "", ""],
        ["Tool 4: Name", "", ""],
        ["Tool 4: Monthly cost", "", ""],
        ["Tool 4: Weekly use hours", "", ""],
        ["Tool 4: What it does for you", "", ""],
        ["Tool 4: Could it be replaced?", "", ""],
        ["Tool 5: Name", "", ""],
        ["Tool 5: Monthly cost", "", ""],
        ["Tool 5: Weekly use hours", "", ""],
        ["Tool 5: What it does for you", "", ""],
        ["Tool 5: Could it be replaced?", "", ""],
        ["Biggest overlap (which tools do the same job?)", "", ""],
        ["Most expensive tool you rarely use", "", ""],
        ["One workflow you wish AI handled better", "", "Describe the task"],
        ["Privacy/data constraints", "", "Client data, HIPAA, NDA, etc."],
        ["Budget ceiling for AI tools", "", "$/month total you're willing to spend"],
        ["Cancellation risk (annual prepay?)", "", "Which tools lock you in annually?"],
    ])

    write_csv(download_dir / "weekly-ai-stack-checklist.csv", ["Day", "Task", "Why", "Done?"], [
        ["Mon", "Check tool-change alerts (pricing, plans, models)", "Catch changes before they affect your billing or workflow", ""],
        ["Mon", "Review any new tool submissions from AIToolsEssentials", "Stay aware of new options without spending hours researching", ""],
        ["Tue", "Run one real task in your primary AI assistant", "Keep muscle memory; notice if quality/limits shifted", ""],
        ["Wed", "Review your tool overlap matrix", "Is anything overlapping or unused this week?", ""],
        ["Thu", "Test one tool you're considering switching to", "One real task, not a demo", ""],
        ["Fri", "Check AIToolsEssentials change-radar for pricing/model updates", "Get the week's recorded changes in one scan", ""],
        ["Fri", "Log any limit-hits or friction from the week", "Data for next month's cancel/upgrade decisions", ""],
        ["Sun", "Decide: any cancellations or trials to start next week?", "Act on data, not impulse", ""],
    ])

    write_csv(download_dir / "tool-change-alert-feed-2026-11.csv", ["Date", "Tool", "Change Type", "Summary", "Action for Members", "Source"], [
        ["2026-11-01", "Cursor", "Model lineup", "Cursor Composer 2.5 now default on Pro; Grok 4.6 available as alternative model", "Test if Composer 2.5 changes your coding workflow; no action needed if current setup works", "Cursor changelog"],
        ["2026-11-01", "Grok", "Model lineup", "Grok 4.6 shipping; Grok Build and Grok Bot features expanded", "Evaluate if real-time X/web data adds value to your workflow vs existing assistants", "X/Grok official"],
        ["2026-11-01", "HtmlSlides", "New tool", "Interactive HTML presentation maker added to directory (vendor submission)", "Test as alternative to Gamma for browser-playable decks", "AIToolsEssentials review"],
        ["2026-11-01", "Whop CLI", "New tool", "Business CLI launched — programmatically manage products, pricing, ads, payouts", "If you sell on Whop, install and test the CLI for automated business management", "Whop blog"],
        ["2026-11-01", "All tools", "Pricing watch", f"Monthly pricing snapshot refreshed across {len(tools)} tools", "Review premium-tool-decision-matrix-2026-11.csv for any changes affecting your stack", "AIToolsEssentials pricing-watch"],
    ])

    write_csv(download_dir / "assistant-hands-on-comparison-2026-11.csv", ["Criterion", "ChatGPT", "Claude", "Grok", "Gemini"], [
        ["Plan checked", "Free/Plus/Pro (verify current)", "Free/Pro/Max (verify current)", "Free/Paid via X (verify current)", "Free/AI Pro/Ultra (verify current)"],
        ["Best for", "Breadth: images, files, voice, browsing in one place", "Long documents, careful prose, instruction adherence", "Real-time X/web data, always-on agents, image gen", "Google Workspace integration, multimodal"],
        ["File upload", "Yes — images, PDFs, spreadsheets", "Yes — documents, PDFs, code", "Limited (check official)", "Yes — docs, images, sheets"],
        ["Web access", "Yes (Plus+)", "Limited", "Yes — real-time X + web", "Yes — Google search integration"],
        ["Image generation", "Yes (native / DALL-E lineage)", "No or limited (check current)", "Yes (Imagine)", "Yes (Imagen)"],
        ["Code execution", "Yes (advanced data analysis)", "Yes (artifacts)", "Yes (Grok Build)", "Yes (code execution)"],
        ["Data training opt-out", "Available on Business/Enterprise", "Available on Team/Enterprise", "Check X/Grok privacy", "Available on paid tiers"],
        ["Offline mode", "No", "No", "No", "No"],
        ["Member test result (drafting)", "TBD — run identical prompt", "TBD — run identical prompt", "TBD — run identical prompt", "TBD — run identical prompt"],
        ["Member test result (research)", "TBD — run identical query", "TBD — run identical query", "TBD — run identical query", "TBD — run identical query"],
        ["Member test result (coding)", "TBD — run identical task", "TBD — run identical task", "TBD — run identical task", "TBD — run identical task"],
        ["Verdict per workflow", "Fill after testing", "Fill after testing", "Fill after testing", "Fill after testing"],
    ])

    write_csv(download_dir / "ai-roi-calculator-template.csv", ["Metric", "Formula", "Your Value", "Notes"], [
        ["Monthly AI spend", "", "", "Sum of all subscriptions"],
        ["Hours saved per week (estimated)", "", "", "Be honest — compare to pre-AI baseline"],
        ["Your hourly rate", "", "", "What your time is worth"],
        ["Monthly time value saved", "Hours saved/week x 4.3 x hourly rate", "", "Auto-calculate"],
        ["Net ROI", "Monthly time value saved - monthly AI spend", "", "Positive = worth keeping"],
        ["ROI %", "(Net ROI / Monthly AI spend) x 100", "", ">100% means tools pay for themselves multiple times over"],
        ["Most expensive unused tool", "", "", "Candidate for cancellation"],
        ["Most used tool", "", "", "Core of your stack"],
        ["Overlap cost (duplicate tools)", "", "", "Sum of tools that do the same job"],
        ["Recommended action", "", "", "Cut, keep, or trial"],
    ])

    write_csv(download_dir / "vendor-security-questions-pack.csv", ["Question", "Why it matters", "What good looks like", "Red flag", "Your notes"], [
        ["Is customer data used for model training by default?", "Training defaults decide whether client text becomes model fuel.", "Clear opt-out or never-train on business/enterprise tiers.", "Vague blog language, no admin control.", ""],
        ["Can admins disable retention/training or set workspace controls?", "You need org-level control, not per-user hope.", "Admin toggles + audit log + role permissions.", "Only individual chat settings.", ""],
        ["Is there a DPA, subprocessors list, security page, or SOC report?", "Procurement and client contracts often require this.", "Public security page + DPA request path.", "No security page; sales-only answers.", ""],
        ["Can exports, sharing, and user access be revoked?", "Offboarding depends on this.", "Admin can revoke seats and export first.", "No export or revoke path documented.", ""],
        ["What happens when a seat leaves the company?", "Licenses and data must not travel with departed users.", "Seat transfer + content reassignment documented.", "Silent retention of ex-user workspaces.", ""],
        ["Which plan includes the controls you actually need?", "Controls often sit behind Team/Business tiers.", "Named plan with the exact control you need.", "Marketing implies controls the free tier lacks.", ""],
        ["Is there an exit plan (export formats)?", "Switching cost is a hidden lock-in tax.", "Standard exports (CSV/MD/JSON/PDF).", "Proprietary-only export or none.", ""],
    ])
    write_csv(download_dir / "30-day-renewal-cancel-calendar.csv", ["Day", "Action", "Owner", "Done?", "Notes"], [
        ["Day 0 (join)", "Download stack audit + weekly checklist; list every paid AI tool", "Member", "", ""],
        ["Day 1", "Fill stack audit; note monthly cost and weekly hours", "Member", "", ""],
        ["Day 2", "Mark keep/trial/replace/cancel for each tool", "Member", "", ""],
        ["Day 3", "Run one real task in primary assistant; log friction", "Member", "", ""],
        ["Day 7 (trial decision)", "Keep Premium only if audit/matrix saved a decision; else cancel trial", "Member", "", ""],
        ["Day 10", "Cancel or pause any tool tagged cancel before next charge", "Member", "", ""],
        ["Day 14", "Reply in request thread if you need a priority research slot", "Member", "", ""],
        ["Day 30", "File one cancel/keep decision with dollar amount saved or kept", "Member", "", ""],
    ])
    write_csv(download_dir / "free-vs-premium-value-matrix.csv", ["Capability", "Free site", "Premium members", "Why it matters"], [
        ["Tool reviews + comparisons", "Yes", "Yes + full decision matrix CSV", "Public is enough for browsing"],
        ["Scorecards / cost calculator / decision brief", "Yes", "Yes", "Free utilities stay free"],
        ["Full 61-tool decision matrix CSV", "No", "Yes, refreshed monthly", "Monthly stack decisions"],
        ["AI Stack Audit Template + 48h strategy reply", "No", "Yes", "Turns inventory into keep/cut"],
        ["Weekly checklist + 30-day calendar", "No", "Yes", "Habit beats one-off cleanup"],
        ["Hands-on protocol + ROI calculator", "Partial", "Yes", "Identical-task testing"],
        ["Priority research slots", "No", "First 5 complete requests/month", "Without a $497 audit"],
        ["Implementation / account access", "Never", "Never", "Scope boundary on purpose"],
    ])
    write_csv(download_dir / "member-first-15-minutes.csv", ["Step", "Minutes", "Action", "Done?"], [
        ["1", "2", "Open pinned Welcome post; bookmark Whop hub", ""],
        ["2", "3", "Download stack audit + weekly checklist", ""],
        ["3", "5", "List every paid AI tool (name, cost, last use)", ""],
        ["4", "3", "Read free-vs-premium-value-matrix.csv", ""],
        ["5", "2", "Skim tool-change alert feed for tools you pay for", ""],
    ])
    write_csv(download_dir / "cancel-savings-tracker.csv", ["Tool cancelled or downgraded", "Monthly $ saved", "Annual $ saved", "Date", "Replaced by", "Notes"], [
        ["(example) unused image tool", "10", "120", "", "Free-tier visual tool", "Was under 1 hr/week"],
        ["TOTAL", "", "", "", "", "Premium pays for itself if monthly saves exceed $12"],
    ])
    write_csv(download_dir / "sample-filled-stack-audit-example.csv", ["Field", "Example Answer", "Editor note"], [
        ["Role/team size", "Solo consultant, 1 person", "Be specific"],
        ["Monthly AI spend", "$97", "Sum everything"],
        ["Biggest overlap", "ChatGPT + Claude both used for drafting", "Pick one primary"],
        ["Most expensive rarely used", "Image generator at 0.5 hrs/week", "Cancel candidate"],
        ["Strategy reply example", "Keep one research tool; pick ONE primary assistant after 3 identical tasks; cancel unused image seat. Est. save $30-50/mo.", "Premium audit reply style - strategy only"],
    ])
    coding = [t for t in tools if t.get("slug") in {"cursor", "github-copilot", "replit-ai", "bolt-new", "lovable", "v0", "claude", "chatgpt", "grok", "windsurf"} or "code" in str(t.get("category", "")).lower() or "coding" in str(t.get("best_for", "")).lower()]
    seen_c: set[str] = set()
    coding_rows = []
    for t in coding:
        slug = str(t.get("slug") or "")
        if not slug or slug in seen_c:
            continue
        seen_c.add(slug)
        coding_rows.append([t.get("name"), slug, t.get("price"), t.get("best_for"), "Run the same real coding task. Compare first-output acceptance rate, not demos."])
    write_csv(download_dir / "coding-assistant-shortlist-2026-11.csv", ["tool", "slug", "pricing", "best_for", "member_test"], coding_rows)

    nov_posts = f"""# AIToolsEssentials Premium — Whop Upload Pack — NOVEMBER ({today})

This is the November member drop. Upload each section as a Whop post and attach the matching CSV from `admin/whop-premium/files/`.

---

## POST N1 — Pinned: Welcome to Premium (updated for November)

Welcome to AIToolsEssentials Premium. This is a research membership for choosing better AI tools without paying for overlapping subscriptions.

**New this month (November):**
1. **AI Stack Audit Template** — fill it out and reply with your answers for a personalized stack recommendation within 48 hours.
2. **Weekly AI Stack Checklist** — a 7-day rhythm for keeping your stack lean.
3. **Tool-Change Alert Feed** — curated pricing, model, and feature changes across all {len(tools)} tracked tools.
4. **Assistant Hands-On Comparison** — ChatGPT vs Claude vs Grok vs Gemini test protocol with fillable results.
5. **AI ROI Calculator** — measure whether your AI spend is actually paying for itself.
6. **Refreshed decision matrix** — `premium-tool-decision-matrix-2026-11.csv`.

**What Premium includes (all months):**
- Monthly decision matrix CSV
- One workflow deep-dive or playbook each month
- Weekly AI stack checklist
- Tool-change alert feed (pricing, models, features)
- AI stack audit template with personalized strategy-only response
- Assistant hands-on comparison protocol with fillable CSV
- AI ROI calculator template
- Source-dated pricing/policy notes when available
- Member request thread for upcoming research
- Priority research slots for the first 5 complete requests each month
- Strategy-only recommendations — no account access, implementation, integrations, or ongoing support

**Billing:** 7-day free trial, then $12/month via Whop. Use code LAUNCH50 for 50% off your first paid month (new users only). Cancel anytime from your Whop account. All sales final — no refunds.

---

## POST N2 — November brief: Stop paying for AI tools you don't use

Most teams and solo users are paying for 3-5 AI tools and actively using 1-2. The rest are overlap, inertia, or "just in case" subscriptions.

**This month's decision framework:**

1. **Download the AI Stack Audit Template** (`ai-stack-audit-template.csv`)
2. **Fill it out honestly** — list every AI tool you pay for, monthly cost, weekly hours, what it does, and whether something else could do it
3. **Reply with your completed audit** — within 48 hours you'll get a personalized strategy-only recommendation: keep, cut, trial, or switch
4. **Use the AI ROI Calculator** (`ai-roi-calculator-template.csv`) to see if your total AI spend is actually paying for itself

**The rule:** if a tool doesn't save you measurable time on a weekly workflow, it's a candidate for cancellation. "Just in case" is not a workflow.

Attach: `ai-stack-audit-template.csv`, `ai-roi-calculator-template.csv`, `premium-tool-decision-matrix-2026-11.csv`

---

## POST N3 — Weekly AI Stack Checklist: your 7-day rhythm

Stop doing ad-hoc tool reviews. Run this checklist every week — it takes 15 minutes total.

| Day | Task | Why |
|-----|------|-----|
| Mon | Check tool-change alerts | Catch pricing/model changes before they affect you |
| Tue | Run one real task in your primary assistant | Notice quality/limit shifts early |
| Wed | Review overlap matrix | Is anything overlapping or unused? |
| Thu | Test one tool you're considering switching to | One real task, not a demo |
| Fri | Check change-radar for the week's updates | One scan, all recorded changes |
| Fri | Log any limit-hits or friction | Data for next month's decisions |
| Sun | Decide: cancellations or trials to start? | Act on data, not impulse |

Attach: `weekly-ai-stack-checklist.csv`

---

## POST N4 — November alert feed: what changed across tracked tools

Curated changes for members. Public change-radar catches up later; members get the curated feed here first.

**Highlights:**
- **Cursor:** Composer 2.5 now default on Pro; Grok 4.6 available as alternative model
- **Grok:** Grok 4.6 shipping; Grok Build and Grok Bot features expanded
- **HtmlSlides:** New tool added (vendor submission) — interactive HTML presentation maker
- **Whop CLI:** Business CLI launched — programmatically manage products, pricing, ads, payouts
- **All tools:** Monthly pricing snapshot refreshed across {len(tools)} tracked tools

**Action:** Review the full alert feed CSV. If any change affects a tool in your stack, note it in your weekly checklist.

Attach: `tool-change-alert-feed-2026-11.csv`

---

## POST N5 — Hands-on comparison: ChatGPT vs Claude vs Grok vs Gemini

Stop reading reviews. Run the test yourself.

**Protocol:**
1. Download the comparison CSV (`assistant-hands-on-comparison-2026-11.csv`)
2. Write one brief for each of three workflows: drafting, research, coding
3. Run the identical brief in all four assistants
4. Fill in the "Member test result" rows with your findings
5. The verdict row: which assistant won each workflow for *your* work?

**Why this matters:** benchmarks don't match your actual tasks. This protocol takes about 30 minutes and gives you a defensible answer for which assistant to keep paying for.

Attach: `assistant-hands-on-comparison-2026-11.csv`

---

## POST N6 — November request thread + priority research slots

Reply with the workflow you want researched next. Good requests include:

- Your role/team
- Current tool stack
- The task you do weekly
- Tools you're deciding between
- Budget, privacy, or export constraints

**November research slots (first 5 complete requests):**
1. Open
2. Open
3. Open
4. Open
5. Open

Research is delivered as a new CSV + brief in the next monthly drop. Replies are strategy-only — no implementation, setup, account access, or ongoing support.
"""
    (admin / "whop-posts-2026-11.md").write_text(nov_posts)


    posts = f'''# AIToolsEssentials Premium — Whop Upload Pack ({today})

Use this file to populate the Whop member area. Create each section below as a Whop post, then attach the CSV files from `admin/whop-premium/files/`.

---

## POST 1 — Pinned start here: Welcome to Premium

Welcome to AIToolsEssentials Premium. This is a research membership for choosing better AI tools without paying for overlapping subscriptions.

**Start here:**
1. Download `premium-tool-decision-matrix-2026-09.csv`.
2. Read the September cost-cutting brief below.
3. Pick one workflow you want tested next and reply in the request thread.

**What Premium includes:**
- Monthly decision matrix CSV (all tracked tools).
- AI Stack Audit Template + strategy-only personalized reply.
- Weekly AI Stack Checklist and Tool-Change Alert Feed.
- Hands-On Comparison Protocol and AI ROI Calculator.
- One workflow deep-dive or playbook each month.
- Priority research slots (first 5 member requests).
- Source-dated pricing/policy notes when available.
- Strategy-only recommendations — no account access, implementation, integrations, or ongoing support.

**Billing:** 7-day free trial, then $12/month via Whop. Use code LAUNCH50 for 50% off your first paid month (new users only). Auto-renews until cancelled from the Whop account. All sales final — no refunds.

---

## POST 2 — September brief: cut AI subscription sprawl

Most teams do not have an AI tool problem. They have an overlap problem.

**This month's decision rule:** keep the smallest stack that covers the weekly workflow with the least upgrade pressure.

**Use the CSV matrix to tag every tool as:**
- Keep: used weekly, has a clear owner, and saves measurable time.
- Trial: promising, but needs a real task test.
- Replace: overlaps with another paid tool.
- Cancel/defer: no workflow owner or no recent use.

**Recommended 30-minute review:**
1. List every AI subscription and owner.
2. Sort the matrix by category.
3. Identify duplicate writing, meeting, automation, and creative tools.
4. Run one real task in each contender.
5. Cancel or defer anything without a weekly workflow.

Attach: `premium-tool-decision-matrix-2026-09.csv`

---

## POST 3 — General AI assistant shortlist

The common mistake is comparing assistants as if they all solve one job. They do not.

**Test separately for:**
- Everyday drafting and rewriting.
- Source-backed research.
- Long-context document analysis.
- Coding/debugging assistance.
- Team controls and data policy.

**Member action:** choose 2–3 assistants from the CSV, run the same real prompt in each, and record editing burden. The winner is the one that reduces review time without increasing verification risk.

Attach: `general-ai-assistant-shortlist-2026-09.csv`

---

## POST 4 — Automation pricing model decoder

Zapier, Make, and n8n do not bill the same unit.

**Decision shortcut:**
- Simple app-to-app workflows: compare Zapier task volume.
- Visual branching scenarios: test Make operation/credit usage.
- Complex multi-step workflows: test n8n executions, especially if technical/self-hosting is acceptable.

**Before upgrading:** map one real workflow and estimate monthly volume. Do not compare sticker price until you know whether you are paying by task, operation, credit, or execution.

Attach: `automation-pricing-model-decoder-2026-09.csv`

---

## POST 5 — Vendor/security questions pack

Before connecting sensitive company, client, student, or customer data, answer these questions:

1. Is customer data used for model training by default?
2. Can admins disable retention/training or configure workspace controls?
3. Is there a DPA, subprocessors list, security page, SOC report, or enterprise docs page?
4. Can exports, sharing, and user access be revoked?
5. What happens when a seat leaves the company?
6. Which plan includes the controls you actually need?

If the vendor does not make the answer easy to find, treat that as a procurement risk — not an automatic rejection, but a reason to delay annual billing.

---

## POST 6 — Member request thread

Reply with the workflow you want tested next. Good requests include:

- Your role/team.
- The current tool stack.
- The task you do weekly.
- The tools you are deciding between.
- Any budget, privacy, or export constraint.

Examples:
- Meeting notes stack for a sales team: Fireflies vs Otter vs Fathom.
- AI writing pipeline for a solo consultant: ChatGPT vs Claude vs Jasper vs Copy.ai.
- App prototyping stack: Cursor vs Replit AI vs Bolt.new vs Lovable vs v0.
- Video course workflow: Descript vs HeyGen vs Synthesia vs Runway.
'''
    (admin / "whop-posts-2026-09.md").write_text(posts)

    checklist = f'''# Whop Premium Setup Checklist

Use this before turning on promotion for the $12/month Premium membership.

## Required in Whop
- [x] Create or update the Premium product/community (AIToolsEssentials Premium).
- [x] Set plan title to Premium Monthly and price to $12/month.
- [x] Enable 7-day free trial on plan_FNXWs3suBFwDN.
- [x] Create branded checkout configuration: {WHOP_CHECKOUT}
- [x] Create promo code LAUNCH50 (50% off first paid month, new users only).
- [ ] Confirm cancellation is handled by Whop account settings.
- [ ] Upload September files + posts from `whop-posts-2026-09.md`.
- [ ] Upload October files + posts from `whop-posts-2026-10.md`.
- [ ] Upload November content-engine pack from `whop-posts-2026-11.md`:
  - `premium-tool-decision-matrix-2026-11.csv`
  - `ai-stack-audit-template.csv`
  - `weekly-ai-stack-checklist.csv`
  - `tool-change-alert-feed-2026-11.csv`
  - `assistant-hands-on-comparison-2026-11.csv`
  - `ai-roi-calculator-template.csv`
- [ ] Pin the November welcome post as the start-here post.
- [ ] Confirm live checkout still matches: {WHOP_CHECKOUT}
- [ ] Confirm promo checkout path works: {WHOP_CHECKOUT_PROMO}
- [ ] Run George's Whop test transaction (trial path) before public launch.

## Scope reminder
Premium is research and strategy only. Do not promise implementation, setup, integrations, account access, credential handling, or ongoing technical support. Stack-audit replies are strategy-only written recommendations.
'''
    (admin / "whop-setup-checklist.md").write_text(checklist)

    readiness = {
        "updated_at": today,
        "site_ready": True,
        "whop_commerce_ready": {
            "plan_id": "plan_FNXWs3suBFwDN",
            "checkout": WHOP_CHECKOUT,
            "checkout_promo": WHOP_CHECKOUT_PROMO,
            "trial_days": WHOP_TRIAL_DAYS,
            "promo_code": WHOP_PROMO_CODE,
            "price_usd_month": 12,
        },
        "public_pages": ["/premium/", "/premium/welcome/", "/premium/sample-report.html", "/premium/roadmap.html", "/premium/archive.html", "/premium/faq.html", "/pricing/", "/checkout/complete/?status=success"],
        "whop_assets_ready": [
            "whop-posts-2026-09.md",
            "whop-posts-2026-10.md",
            "whop-posts-2026-11.md",
            "files/premium-tool-decision-matrix-2026-09.csv",
            "files/premium-tool-decision-matrix-2026-10.csv",
            "files/premium-tool-decision-matrix-2026-11.csv",
            "files/general-ai-assistant-shortlist-2026-09.csv",
            "files/automation-pricing-model-decoder-2026-09.csv",
            "files/visual-ai-tool-shortlist-2026-10.csv",
            "files/meeting-notes-decision-sheet-2026-10.csv",
            "files/ai-stack-audit-template.csv",
            "files/weekly-ai-stack-checklist.csv",
            "files/tool-change-alert-feed-2026-11.csv",
            "files/assistant-hands-on-comparison-2026-11.csv",
            "files/ai-roi-calculator-template.csv",
        ],
        "george_still_needs_to_do": [
            "Run a Whop test transaction through the 7-day trial path",
            "Confirm LAUNCH50 applies 50% off the first paid month",
        ],
        "scope_boundary": "Research and strategy only; no implementation, setup, integrations, account access, credentials, or ongoing support. Stack-audit replies are strategy-only written recommendations."
    }
    (admin / "whop-launch-readiness.json").write_text(json.dumps(readiness, indent=2))

    readiness_md = "# Whop Launch Readiness\n\n" + "## Site-ready public pages\n" + "\n".join(f"- [x] {x}" for x in readiness["public_pages"]) + "\n\n## Whop assets ready\n" + "\n".join(f"- [x] {x}" for x in readiness["whop_assets_ready"]) + "\n\n## George still needs to do in Whop\n" + "\n".join(f"- [ ] {x}" for x in readiness["george_still_needs_to_do"]) + "\n\n## Scope boundary\n" + readiness["scope_boundary"] + "\n"
    (admin / "whop-launch-readiness.md").write_text(readiness_md)

    # Deterministic upload bundle for Whop: fixed timestamps keep repeated builds stable.
    bundle_path = admin / "aitools-premium-whop-upload-pack.zip"
    bundle_members = [
        (admin / "whop-posts-2026-09.md", "whop-posts-2026-09.md"),
        (admin / "whop-posts-2026-10.md", "whop-posts-2026-10.md"),
        (admin / "whop-posts-2026-11.md", "whop-posts-2026-11.md"),
        (admin / "whop-setup-checklist.md", "whop-setup-checklist.md"),
        (admin / "whop-launch-readiness.md", "whop-launch-readiness.md"),
        (admin / "whop-launch-readiness.json", "whop-launch-readiness.json"),
        (download_dir / "premium-tool-decision-matrix-2026-09.csv", "files/premium-tool-decision-matrix-2026-09.csv"),
        (download_dir / "premium-tool-decision-matrix-2026-10.csv", "files/premium-tool-decision-matrix-2026-10.csv"),
        (download_dir / "premium-tool-decision-matrix-2026-11.csv", "files/premium-tool-decision-matrix-2026-11.csv"),
        (download_dir / "general-ai-assistant-shortlist-2026-09.csv", "files/general-ai-assistant-shortlist-2026-09.csv"),
        (download_dir / "automation-pricing-model-decoder-2026-09.csv", "files/automation-pricing-model-decoder-2026-09.csv"),
        (download_dir / "visual-ai-tool-shortlist-2026-10.csv", "files/visual-ai-tool-shortlist-2026-10.csv"),
        (download_dir / "meeting-notes-decision-sheet-2026-10.csv", "files/meeting-notes-decision-sheet-2026-10.csv"),
        (download_dir / "ai-stack-audit-template.csv", "files/ai-stack-audit-template.csv"),
        (download_dir / "weekly-ai-stack-checklist.csv", "files/weekly-ai-stack-checklist.csv"),
        (download_dir / "tool-change-alert-feed-2026-11.csv", "files/tool-change-alert-feed-2026-11.csv"),
        (download_dir / "assistant-hands-on-comparison-2026-11.csv", "files/assistant-hands-on-comparison-2026-11.csv"),
        (download_dir / "ai-roi-calculator-template.csv", "files/ai-roi-calculator-template.csv"),
        (download_dir / "vendor-security-questions-pack.csv", "files/vendor-security-questions-pack.csv"),
        (download_dir / "30-day-renewal-cancel-calendar.csv", "files/30-day-renewal-cancel-calendar.csv"),
        (download_dir / "free-vs-premium-value-matrix.csv", "files/free-vs-premium-value-matrix.csv"),
        (download_dir / "member-first-15-minutes.csv", "files/member-first-15-minutes.csv"),
        (download_dir / "cancel-savings-tracker.csv", "files/cancel-savings-tracker.csv"),
        (download_dir / "sample-filled-stack-audit-example.csv", "files/sample-filled-stack-audit-example.csv"),
        (download_dir / "coding-assistant-shortlist-2026-11.csv", "files/coding-assistant-shortlist-2026-11.csv"),
    ]
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for src, arc in bundle_members:
            info = zipfile.ZipInfo(arc, date_time=(2026, 11, 1, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, src.read_bytes())
    (admin / "whop-upload-pack-manifest.json").write_text(json.dumps({
        "bundle": bundle_path.name,
        "files": [arc for _, arc in bundle_members],
        "note": "Upload the Markdown posts/checklists as Whop posts and attach the CSV files to the member area.",
    }, indent=2))


def update_checkout(root: Path) -> None:
    p = root / "checkout" / "complete" / "index.html"
    if p.exists():
        html = p.read_text()
        html = html.replace("Bookmark\n      <a href=\"/pricing/\">aitoolsessentials.com/pricing</a> — member links ship from there.", "Open your Whop account for the member library, then bookmark <a href=\"/premium/\">aitoolsessentials.com/premium</a> for previews and monthly context.")
        html = html.replace("'<a class=\"button button-blue\" href=\"../../tools/index.html\">Explore the tools database</a>' +\n      '<a class=\"button button-ghost-dark\" href=\"../../articles/index.html\">Browse guides</a>';", "'<a class=\"button button-blue\" href=\"https://whop.com/hub\" rel=\"external noopener\">Open Whop member hub</a>' +\n      '<a class=\"button button-ghost-dark\" href=\"../../premium/\">Preview Premium library</a>';")
        p.write_text(html)
    home = root / "index.html"
    if home.exists():
        html = home.read_text()
        html = html.replace(
            "<p>Premium membership is being prepared and checkout is not active yet. The public directory stays free; the $497 AI Stack Audit is available as a strategy-only report.</p>",
            "<p>Premium is live: 7-day free trial, then $12/month. Use code <strong>LAUNCH50</strong> for 50% off the first paid month (new users). The public directory stays free. Research and strategy only.</p>",
        )
        html = html.replace("See planned Premium", "Start 7-day free trial")
        html = html.replace('href="pricing/index.html"', f'href="{WHOP_CHECKOUT}" rel="external noopener"')
        html = html.replace(
            "<p>Monthly comparison archives, workflow deep-dives, and CSV exports — $12/month via Whop, cancel anytime.</p><div class=\"guide-pill-grid\"><a class=\"guide-pill\" href=\"pricing/\">See pricing</a></div>",
            "<p>Stack audits, weekly checklists, tool-change alerts, hands-on protocols, and a 61-tool decision matrix. 7-day free trial, then $12/month. Code LAUNCH50 for 50% off the first paid month.</p><div class=\"guide-pill-grid\"><a class=\"guide-pill\" href=\"premium/\">Premium library</a><a class=\"guide-pill\" href=\"pricing/\">Pricing</a><a class=\"guide-pill\" href=\"" + WHOP_CHECKOUT + "\" rel=\"external noopener\">Start free trial</a></div>",
        )
        home.write_text(html)



def premium_upsell_module() -> str:
    return f'''<!-- AIT PREMIUM MODULE START -->
<section class="newsletter-panel premium-conversion-panel"><div><span>Premium research layer</span><h2>Want the member-only decision archive?</h2><p>Premium adds monthly research briefs, stack-audit templates, weekly checklists, tool-change alerts, hands-on protocols, ROI calculators, and member-requested deep dives through Whop.</p><p class="affiliate-inline">7-day free trial · then $12/month · code LAUNCH50 for 50% off first paid month · Whop handles billing and access · research and strategy only.</p></div><div class="newsletter-actions"><a class="button button-blue" href="{WHOP_CHECKOUT}" rel="external noopener">Subscribe on Whop</a><a class="button button-dark" href="/premium/">See Premium library</a><a class="button button-dark" href="/premium/faq.html">FAQ</a></div></section>
<!-- AIT PREMIUM MODULE END -->'''


def inject_before_main_end(html: str, module: str) -> str:
    import re
    html = re.sub(r'\n?<!-- AIT PREMIUM MODULE START -->.*?<!-- AIT PREMIUM MODULE END -->\n?', '\n', html, flags=re.S)
    if '</main>' not in html:
        return html
    return html.replace('</main>', module + '\n</main>', 1)


def postprocess(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    base_targets = [
        'stack-builder.html',
        'cost-calculator.html',
        'compare-shortlist.html',
        'tool-finder.html',
        'deals/index.html',
        'resources/index.html',
        'pricing-index/index.html',
        'weekly/index.html',
        'start-here/index.html',
        'index.html',
    ]
    dynamic_targets = []
    dynamic_targets.extend(str(p.relative_to(root)) for p in sorted((root / 'tools').glob('*/index.html')))
    dynamic_targets.extend(str(p.relative_to(root)) for p in sorted((root / 'comparisons').glob('*.html')))
    # Keep admin/noindex/checkout/legal pages out of the conversion injection path.
    targets = list(dict.fromkeys(base_targets + dynamic_targets))
    module = premium_upsell_module()
    changed = 0
    for rel in targets:
        p = root / rel
        if not p.exists():
            continue
        old = p.read_text()
        if 'name="robots" content="noindex' in old:
            continue
        new = inject_before_main_end(old, module)
        if new != old:
            p.write_text(new)
            changed += 1
    return changed

def generate(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> int:
    tools_list = tools if tools is not None else json.loads((root / "data/tools.json").read_text())
    today = today or datetime.today().strftime("%Y-%m-%d")
    generate_public_pages(root, tools_list, today)
    generate_whop_pack(root, tools_list, today)
    update_checkout(root)
    return 9


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    tools = json.loads((root / "data/tools.json").read_text())
    print(generate(root, tools))
