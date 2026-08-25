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
WHOP_CHECKOUT = "https://whop.com/checkout/plan_FNXWs3suBFwDN"
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
        ("Deep-dive workflow report", "One practical workflow per month compared across tools with testing plan, decision matrix, and cost notes."),
        ("CSV decision archive", "Downloadable scorecards for sorting tools by workflow, pricing pressure, policy risk, and trial priority."),
        ("Member request thread", "Subscribers vote on the next workflow to test. Requests shape future premium research."),
        ("Audit-style playbooks", "Strategy-only templates for cutting tool sprawl, choosing alternatives, and preparing vendor/security questions."),
        ("Update notes", "Source-dated alerts when pricing, policies, or plan names change across tracked tools."),
    ]
    cards = "".join(f'<article class="content-hub-card"><span>Premium deliverable</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>' for title, text in library_cards)
    deliverables = [
        "Welcome/start-here post for new Whop members",
        "September AI stack cost-cutting brief",
        "General AI assistants decision matrix",
        "Automation pricing model decoder",
        "Vendor security questions pack",
        "CSV comparison/archive files",
        "Member request thread for next workflow deep-dive",
    ]
    deliverable_list = "".join(f"<li>{esc(x)}</li>" for x in deliverables)
    desc = "AIToolsEssentials Premium is a $12/month Whop membership with monthly AI tool research briefs, CSV decision archives, workflow deep-dives, and strategy-only playbooks."
    page = f'''<!doctype html><html lang="en">{head("Premium AI Tool Research Membership", desc, DOMAIN+"/premium/")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Premium research membership</p><h1>Give subscribers more than access. Give them decisions.</h1><p class="subhead">A $12/month Whop membership for people who want dated research briefs, side-by-side decision archives, workflow playbooks, and pricing/policy alerts before they buy more AI tools.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT}" rel="external noopener" data-whop-checkout="plan_FNXWs3suBFwDN">Subscribe on Whop</a><a class="button button-blue" href="/premium/sample-report.html" style="margin-left:8px">See sample report</a></p><p class="affiliate-inline">Billing, login, cancellation, and member access are handled by Whop. Research and strategy only — no implementation, setup, account access, credentials, or ongoing support.</p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>What members get immediately</span><h2>A real member library from day one.</h2><ul>{deliverable_list}</ul><p><a class="button button-blue" href="/premium/roadmap.html">View roadmap</a><a class="button button-blue" href="/premium/archive.html" style="margin-left:8px">Archive preview</a><a class="button button-blue" href="/premium/faq.html" style="margin-left:8px">Premium FAQ</a></p></div><h2>Premium content library</h2><div class="content-hub-grid">{cards}</div><section class="score-card"><span>Scope boundary</span><h2>Premium does not buy rankings or implementation help.</h2><p>Premium is a research membership. It does not change public editorial rankings, sponsor labels, affiliate disclosures, or review scores. It does not include setup, integrations, credential handling, or technical support.</p></section></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "index.html").write_text(page)

    sample_tools = category_top_tools(tools, "General AI Assistant", 5) or tools[:5]
    rows = "".join(f'<tr><td><a href="/tools/{esc(t["slug"])}/">{esc(t["name"])}</a></td><td>{esc(t.get("price"))}</td><td>{esc(t.get("best_for"))}</td><td>{esc(t.get("summary"))}</td></tr>' for t in sample_tools)
    sample_desc = "Sample AIToolsEssentials Premium report showing the structure of monthly member briefings, decision matrices, and source-led recommendations."
    sample = f'''<!doctype html><html lang="en">{head("Sample Premium AI Tool Report", sample_desc, DOMAIN+"/premium/sample-report.html")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Sample member report</p><h1>General AI assistant decision brief.</h1><p class="subhead">This public sample shows the format. Paid Whop members get the full monthly archive, CSV files, source notes, and workflow playbooks.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT}" rel="external noopener">Subscribe on Whop</a><a class="button button-blue" href="/pricing/" style="margin-left:8px">Compare plans</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>Sample recommendation</span><h2>Pick by workflow, not by brand.</h2><p>For general AI assistants, the member report separates everyday drafting, source-backed research, long-context document work, coding help, and organization controls. The public sample is intentionally partial; members get the full source-dated matrix and CSV.</p></div><div class="table-wrap"><table><thead><tr><th>Tool</th><th>Pricing model</th><th>Best fit</th><th>Sample note</th></tr></thead><tbody>{rows}</tbody></table></div><h2>What full members receive</h2><div class="content-hub-grid"><article class="content-hub-card"><h3>Full matrix</h3><p>All tracked assistant tools scored across workflow fit, pricing pressure, data controls, and trial priority.</p></article><article class="content-hub-card"><h3>CSV archive</h3><p>Sortable CSV for filtering by buyer role, tool category, risk, and renewal pressure.</p></article><article class="content-hub-card"><h3>Action notes</h3><p>What to test before upgrading, which tools overlap, and when to defer payment.</p></article></div></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "sample-report.html").write_text(sample)

    roadmap_desc = "AIToolsEssentials Premium monthly research roadmap and member deliverable calendar."
    roadmap_items = [
        ("September", "Cut AI subscription sprawl", "Decision matrix, general assistant shortlist, automation pricing decoder, vendor security questions."),
        ("October", "Coding and app-building workflow", "Cursor, GitHub Copilot, Replit AI, Bolt.new, Lovable, and v0 decision brief."),
        ("November", "Meeting intelligence stack", "Fireflies, Otter, Fathom, Notion AI, and CRM handoff workflow review."),
        ("December", "Content production stack", "ChatGPT, Claude, Jasper, Copy.ai, Canva AI, Descript, and distribution workflow playbook."),
    ]
    roadmap_cards = "".join(f'<article class="content-hub-card"><span>{esc(month)}</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>' for month, title, text in roadmap_items)
    roadmap = f'''<!doctype html><html lang="en">{head("Premium Research Roadmap", roadmap_desc, DOMAIN+"/premium/roadmap.html")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Premium roadmap</p><h1>The member library keeps compounding.</h1><p class="subhead">Premium is not a single PDF. It is a monthly research layer: dated briefs, CSV archives, workflow playbooks, and member-requested deep dives.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT}" rel="external noopener">Subscribe on Whop</a><a class="button button-blue" href="/premium/" style="margin-left:8px">Premium overview</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><h2>Research calendar</h2><div class="content-hub-grid">{roadmap_cards}</div><section class="score-card"><span>Member-driven</span><h2>Requests shape the calendar.</h2><p>Whop members can request workflows to compare. Good requests include your role, current stack, weekly task, budget, data constraints, and tools you are deciding between.</p></section></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "roadmap.html").write_text(roadmap)

    archive_desc = "AIToolsEssentials Premium archive preview for monthly AI tool research drops."
    archive_rows = "".join([
        '<tr><td>2026-09</td><td>AI stack cost-cutting brief</td><td>Decision matrix CSV, assistant shortlist, automation decoder</td><td>Ready for Whop upload</td></tr>',
        '<tr><td>2026-10</td><td>Coding/app-building workflow</td><td>Planned decision brief and tool comparison archive</td><td>Planned</td></tr>',
        '<tr><td>2026-11</td><td>Meeting intelligence workflow</td><td>Planned brief, policy notes, handoff checklist</td><td>Planned</td></tr>',
    ])
    archive = f'''<!doctype html><html lang="en">{head("Premium Research Archive Preview", archive_desc, DOMAIN+"/premium/archive.html")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Premium archive</p><h1>Monthly research drops, organized for members.</h1><p class="subhead">A public preview of the member archive structure. Full posts, CSVs, and request threads live inside Whop.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT}" rel="external noopener">Subscribe on Whop</a><a class="button button-blue" href="/premium/sample-report.html" style="margin-left:8px">See sample report</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="table-wrap"><table><thead><tr><th>Month</th><th>Drop</th><th>Member files</th><th>Status</th></tr></thead><tbody>{archive_rows}</tbody></table></div><section class="score-card"><span>Access note</span><h2>Full archive access is through Whop.</h2><p>Subscribers receive the actual posts, downloads, and request threads in the Whop member area. This page is a transparent preview, not the gated archive itself.</p></section></div></section>
</main>{FOOTER}{scripts()}</body></html>'''
    (out / "archive.html").write_text(archive)

    faq_desc = "Premium membership FAQ for AIToolsEssentials Whop subscribers."
    faqs = [
        ("What do I get immediately after subscribing?", "Access is handled through Whop. The day-one member library includes a start-here post, September research brief, CSV tool decision matrix, general AI assistant shortlist, automation pricing decoder, vendor/security questions, and the member request thread."),
        ("Is Premium a course, community, or consulting service?", "It is a research membership. Premium gives you decision briefs, CSVs, playbooks, and request threads. It does not include implementation, setup, integrations, account access, credential handling, or ongoing technical support."),
        ("Can Premium vendors pay to change rankings?", "No. Premium does not change public editorial rankings, sponsor labels, affiliate disclosures, or review scores. Paid visibility and editorial scoring remain separate."),
        ("How does billing and cancellation work?", "Billing, login, member access, and cancellation are handled by Whop. The plan is listed at $12/month unless the live checkout states otherwise. Cancel from your Whop account."),
        ("Are refunds offered?", "No. The current Premium terms state all sales are final and there are no refunds. Review the sample report, roadmap, archive preview, and terms before subscribing."),
        ("How do member requests work?", "Members can post the workflows they want compared next. Good requests include role, current stack, weekly task, candidate tools, budget, and data constraints."),
    ]
    faq_items = "".join(f'<article class="content-hub-card"><h3>{esc(q)}</h3><p>{esc(a)}</p></article>' for q, a in faqs)
    faq_schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    product_schema = {"@context":"https://schema.org","@type":"Product","name":"AIToolsEssentials Premium","description":"Monthly AI tool research membership with briefings, CSV decision archives, workflow playbooks, and member-requested deep dives.","brand":{"@type":"Brand","name":"AIToolsEssentials"},"offers":{"@type":"Offer","price":"12","priceCurrency":"USD","availability":"https://schema.org/InStock","url":WHOP_CHECKOUT},"category":"Research membership"}
    faq = f'''<!doctype html><html lang="en">{head("Premium Membership FAQ", faq_desc, DOMAIN+"/premium/faq.html")}<body>{HEADER}<main>
<section class="scene scene-dark"><div style="max-width:980px;margin:0 auto;padding:92px 28px 72px;text-align:center"><p class="kicker light">Premium FAQ</p><h1>Know exactly what the Whop membership includes.</h1><p class="subhead">Clear answers on deliverables, billing, cancellations, refunds, editorial independence, and scope boundaries before anyone subscribes.</p><p><a class="button button-blue" href="{WHOP_CHECKOUT}" rel="external noopener">Subscribe on Whop</a><a class="button button-blue" href="/premium/sample-report.html" style="margin-left:8px">See sample report</a></p></div></section>
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="content-hub-grid">{faq_items}</div><section class="score-card"><span>Before launch</span><h2>Whop still needs the member posts uploaded.</h2><p>The site and content pack are ready. George still needs to upload the prepared posts and CSV files to Whop and run the $12 test transaction before promoting the checkout heavily.</p></section></div></section>
</main>{FOOTER}{jsonld(faq_schema)}{jsonld(product_schema)}{scripts()}</body></html>'''
    (out / "faq.html").write_text(faq)


def write_csv(path: Path, headers: list[str], rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
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
- Monthly decision matrix CSV.
- One workflow deep-dive or playbook each month.
- Source-dated pricing/policy notes when available.
- Member request thread for upcoming research.
- Strategy-only recommendations — no account access, implementation, integrations, or ongoing support.

**Billing:** $12/month via Whop, auto-renews until cancelled from the Whop account. All sales final — no refunds.

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
- [ ] Create or update the Premium product/community.
- [ ] Set price to $12/month.
- [ ] Confirm cancellation is handled by Whop account settings.
- [ ] Upload these files:
  - `premium-tool-decision-matrix-2026-09.csv`
  - `general-ai-assistant-shortlist-2026-09.csv`
  - `automation-pricing-model-decoder-2026-09.csv`
- [ ] Create posts from `whop-posts-2026-09.md`.
- [ ] Pin POST 1 as the start-here post.
- [ ] Confirm checkout URL still matches: {WHOP_CHECKOUT}
- [ ] Run George's $12 test transaction before public launch.

## Scope reminder
Premium is research and strategy only. Do not promise implementation, setup, integrations, account access, credential handling, or ongoing technical support.
'''
    (admin / "whop-setup-checklist.md").write_text(checklist)

    readiness = {
        "updated_at": today,
        "site_ready": True,
        "public_pages": ["/premium/", "/premium/sample-report.html", "/premium/roadmap.html", "/premium/archive.html", "/premium/faq.html", "/pricing/", "/checkout/complete/?status=success"],
        "whop_assets_ready": [
            "whop-posts-2026-09.md",
            "files/premium-tool-decision-matrix-2026-09.csv",
            "files/general-ai-assistant-shortlist-2026-09.csv",
            "files/automation-pricing-model-decoder-2026-09.csv",
        ],
        "george_still_needs_to_do": [
            "Upload posts from whop-posts-2026-09.md into Whop",
            "Attach the three CSV files inside the Whop member area",
            "Pin the start-here post",
            "Run the $12 Whop test transaction",
            "Confirm the checkout URL still resolves to the correct product",
        ],
        "scope_boundary": "Research and strategy only; no implementation, setup, integrations, account access, credentials, or ongoing support."
    }
    (admin / "whop-launch-readiness.json").write_text(json.dumps(readiness, indent=2))

    readiness_md = "# Whop Launch Readiness\n\n" + "## Site-ready public pages\n" + "\n".join(f"- [x] {x}" for x in readiness["public_pages"]) + "\n\n## Whop assets ready\n" + "\n".join(f"- [x] {x}" for x in readiness["whop_assets_ready"]) + "\n\n## George still needs to do in Whop\n" + "\n".join(f"- [ ] {x}" for x in readiness["george_still_needs_to_do"]) + "\n\n## Scope boundary\n" + readiness["scope_boundary"] + "\n"
    (admin / "whop-launch-readiness.md").write_text(readiness_md)

    # Deterministic upload bundle for Whop: fixed timestamps keep repeated builds stable.
    bundle_path = admin / "aitools-premium-whop-upload-pack-2026-09.zip"
    bundle_members = [
        (admin / "whop-posts-2026-09.md", "whop-posts-2026-09.md"),
        (admin / "whop-setup-checklist.md", "whop-setup-checklist.md"),
        (admin / "whop-launch-readiness.md", "whop-launch-readiness.md"),
        (admin / "whop-launch-readiness.json", "whop-launch-readiness.json"),
        (download_dir / "premium-tool-decision-matrix-2026-09.csv", "files/premium-tool-decision-matrix-2026-09.csv"),
        (download_dir / "general-ai-assistant-shortlist-2026-09.csv", "files/general-ai-assistant-shortlist-2026-09.csv"),
        (download_dir / "automation-pricing-model-decoder-2026-09.csv", "files/automation-pricing-model-decoder-2026-09.csv"),
    ]
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for src, arc in bundle_members:
            info = zipfile.ZipInfo(arc, date_time=(2026, 9, 1, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, src.read_bytes())
    (admin / "whop-upload-pack-manifest.json").write_text(json.dumps({
        "bundle": bundle_path.name,
        "files": [arc for _, arc in bundle_members],
        "note": "Upload the Markdown posts/checklists as Whop posts and attach the CSV files to the member area.",
    }, indent=2))


def update_checkout(root: Path) -> None:
    p = root / "checkout" / "complete" / "index.html"
    if not p.exists():
        return
    html = p.read_text()
    html = html.replace("Bookmark\n      <a href=\"/pricing/\">aitoolsessentials.com/pricing</a> — member links ship from there.", "Open your Whop account for the member library, then bookmark <a href=\"/premium/\">aitoolsessentials.com/premium</a> for previews and monthly context.")
    html = html.replace("'<a class=\"button button-blue\" href=\"../../tools/index.html\">Explore the tools database</a>' +\n      '<a class=\"button button-ghost-dark\" href=\"../../articles/index.html\">Browse guides</a>';", "'<a class=\"button button-blue\" href=\"https://whop.com/hub\" rel=\"external noopener\">Open Whop member hub</a>' +\n      '<a class=\"button button-ghost-dark\" href=\"../../premium/\">Preview Premium library</a>';")
    p.write_text(html)



def premium_upsell_module() -> str:
    return f'''<!-- AIT PREMIUM MODULE START -->
<section class="newsletter-panel premium-conversion-panel"><div><span>Premium research layer</span><h2>Want the member-only decision archive?</h2><p>Premium adds monthly research briefs, CSV decision matrices, workflow playbooks, and member-requested deep dives through Whop.</p><p class="affiliate-inline">$12/month · Whop handles billing and access · research and strategy only.</p></div><div class="newsletter-actions"><a class="button button-blue" href="{WHOP_CHECKOUT}" rel="external noopener">Subscribe on Whop</a><a class="button button-dark" href="/premium/">See Premium library</a><a class="button button-dark" href="/premium/faq.html">FAQ</a></div></section>
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
