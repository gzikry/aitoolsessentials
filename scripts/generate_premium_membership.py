#!/usr/bin/env python3
"""Generate public premium pages and Whop-ready member content assets."""
from __future__ import annotations

import csv
import json
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
<section class="scene scene-light content-hub"><div class="article-shell wide"><div class="score-card"><span>What members get immediately</span><h2>A real member library from day one.</h2><ul>{deliverable_list}</ul></div><h2>Premium content library</h2><div class="content-hub-grid">{cards}</div><section class="score-card"><span>Scope boundary</span><h2>Premium does not buy rankings or implementation help.</h2><p>Premium is a research membership. It does not change public editorial rankings, sponsor labels, affiliate disclosures, or review scores. It does not include setup, integrations, credential handling, or technical support.</p></section></div></section>
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


def update_checkout(root: Path) -> None:
    p = root / "checkout" / "complete" / "index.html"
    if not p.exists():
        return
    html = p.read_text()
    html = html.replace("Bookmark\n      <a href=\"/pricing/\">aitoolsessentials.com/pricing</a> — member links ship from there.", "Open your Whop account for the member library, then bookmark <a href=\"/premium/\">aitoolsessentials.com/premium</a> for previews and monthly context.")
    html = html.replace("'<a class=\"button button-blue\" href=\"../../tools/index.html\">Explore the tools database</a>' +\n      '<a class=\"button button-ghost-dark\" href=\"../../articles/index.html\">Browse guides</a>';", "'<a class=\"button button-blue\" href=\"https://whop.com/hub\" rel=\"external noopener\">Open Whop member hub</a>' +\n      '<a class=\"button button-ghost-dark\" href=\"../../premium/\">Preview Premium library</a>';")
    p.write_text(html)


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
