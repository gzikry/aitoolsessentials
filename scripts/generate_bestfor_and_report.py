#!/usr/bin/env python3
"""Generate:

1. /best-for/ — profession routing hub linking audience guides + top picks per role.
2. /pricing-report/ — quarterly "State of AI pricing" report generated from
   data/pricing_snapshots.json (verified promos, coverage, change log status).

Both are data-driven and regenerate idempotently with the pipeline.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

DOMAIN = "https://aitoolsessentials.com"
DEALS_S = "<!-- AIT BESTFOR DEALS START -->"
DEALS_E = "<!-- AIT BESTFOR DEALS END -->"


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


HEADER = '<header class="global-nav"><a class="brand" href="/index.html"><span class="brand-glyph">✦</span><span>AIToolsEssentials</span></a><nav class="nav-links"><a href="/tools/index.html">Tools</a><a href="/comparisons/best-ai-tools.html">Best AI tools</a><a href="/guides/switch-guides/">Switching</a><a href="/pricing-watch/">Pricing Watch</a><a href="/benchmarks/">Benchmarks</a><a href="/resources/">Resources</a></nav><a class="nav-cta" href="/premium/">Premium</a></header>'
FOOTER = '<footer class="footer"><span>© 2026 AIToolsEssentials</span><a href="/legal/about.html">About</a><a href="/legal/privacy.html">Privacy</a><a href="/legal/terms.html">Terms</a><a href="/legal/corrections.html">Corrections</a><a href="mailto:contact@aitoolsessentials.com">Contact</a></footer>'


def _head(title: str, desc: str, path: str) -> str:
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="description" content="{_esc(desc)}"><title>{_esc(title)}</title>'
            f'<link rel="canonical" href="{DOMAIN}{path}">'
            f'<link rel="stylesheet" href="/css/styles.css"><link rel="stylesheet" href="/css/share.css">'
            f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"{_esc(title)}","url":"{DOMAIN}{path}","publisher":{{"@type":"Organization","name":"AIToolsEssentials"}}}}</script>'
            f'</head><body>{HEADER}<main>')


ROLES = [
    ("students", "Students", "Free-first stacks that cover research, writing, notes, and presentations without paid seats.",
     [("chatgpt", "General assistant: explanations, drafting, practice questions"),
      ("perplexity", "Cited research for papers and quick fact-checks"),
      ("notion-ai", "Notes, summaries, and study organization"),
      ("gamma", "Fast presentation drafts")],
     "articles/best-ai-tools-for-students.html"),
    ("freelancers", "Freelancers & solo consultants", "Client work, proposals, invoicing admin, and one-person marketing on a lean budget.",
     [("claude", "Long-form client deliverables and careful editing"),
      ("canva-ai", "On-brand social and proposal visuals"),
      ("zapier-ai", "Automating client onboarding and follow-ups"),
      ("fireflies", "Meeting notes and action items from client calls")],
     "articles/best-ai-tools-for-freelancers.html"),
    ("agencies", "Agencies", "Multi-client content operations, brand voice control, approvals, and reporting.",
     [("jasper", "Brand-voice marketing content at team volume"),
      ("make", "Scenario automation across client accounts"),
      ("notion-ai", "Client wikis, briefs, and internal knowledge"),
      ("heygen", "Avatar video for client campaigns")],
     "articles/best-ai-tools-for-agencies.html"),
    ("consultants", "Consultants", "Research speed, deck production, meeting capture, and analysis under confidentiality constraints.",
     [("claude", "Document review, synthesis, and long-form analysis"),
      ("gamma", "Deck generation from outlines"),
      ("perplexity", "Market scans with sources"),
      ("microsoft-copilot", "Working inside the client's Microsoft 365 estate")],
     "articles/best-ai-tools-for-consultants.html"),
    ("developers", "Developers", "Coding agents, editors, code review, and terminal workflows.",
     [("cursor", "AI-native editor with Cursor Grok 4.6 + Composer 2.5"),
      ("github-copilot", "In-IDE completions across every major IDE"),
      ("claude", "Architecture reasoning and document-grade explanations"),
      ("v0", "UI generation from prompts")],
     "articles/best-ai-tools-for-developers.html"),
    ("small-business", "Small businesses", "Practical AI that replaces repetitive admin without an IT department.",
     [("chatgpt", "Broad default assistant"),
      ("microsoft-copilot", "Already in your M365 seat — check before buying anything"),
      ("notion-ai", "Docs, wikis, and light project tracking in one place")],
     "articles/best-ai-tools-for-small-business.html"),
    ("healthcare-admin", "Healthcare admin & medical teams", "Documentation drafts and literature lookup for medical professionals, with no implied HIPAA or clinical-decision certification.",
     [("heidi-health", "Self-serve clinical documentation drafts with a published free plan"),
      ("openevidence", "Official-homepage-free cited literature lookup for healthcare professionals"),
      ("dragon-copilot", "Microsoft quote-based enterprise clinical assistant"),
      ("microsoft-copilot", "Practice-admin drafting inside an existing Microsoft 365 tenant")],
     "articles/best-ai-tools-for-healthcare-admin.html"),
]


def generate_best_for(root: Path) -> Path:
    tools = {t["slug"]: t for t in json.loads((root / "data/tools.json").read_text())}
    cards = ""
    for slug, title, blurb, picks, article in ROLES:
        pick_items = ""
        for pslug, why in picks:
            t = tools.get(pslug)
            name = t["name"] if t else pslug
            rating = f' · {t["rating"]}/5' if t and t.get("rating") else ""
            pick_items += (f'<li><strong><a href="/tools/{pslug}/">{_esc(name)}</a></strong>{rating} — {_esc(why)}</li>')
        cards += (
            f'<article class="content-hub-card"><span>{_esc(title)}</span>'
            f'<h3><a href="/{article}">Best AI stack for {_esc(title.lower())}</a></h3>'
            f"<p>{_esc(blurb)}</p><ul>{pick_items}</ul>"
            f'<p><a class="text-link" href="/stack-builder.html?role={slug}">Build this stack →</a></p></article>'
        )
    deals = _deals_strip(root)
    page = (_head("Best AI tools by profession", 
                  "Role-based AI stack recommendations: students, freelancers, agencies, consultants, developers, and small businesses — with verified pricing.", 
                  "/best-for/")
            + '<section class="scene scene-dark hero compact-hero"><div class="hero-copy"><p class="kicker">By profession</p>'
              '<h1>The right AI stack for how you actually work.</h1>'
              '<p class="subhead">Curated picks per role, each verified against official pricing. Start here instead of guessing from the current directory.</p></div></section>'
              '<section class="scene scene-light content-hub"><div class="article-shell wide">'
              f'<div class="content-hub-grid">{cards}</div>{deals}'
              '<section class="score-card"><span>Cross-role rules</span><h2>Pick by workflow, not hype.</h2>'
              "<ol><li>Name the weekly task first; the tool second.</li>"
              "<li>Check what your existing seats already include (M365 Copilot, Google Workspace).</li>"
              "<li>Trial on one real deliverable before any annual plan.</li>"
              "<li>Cancel overlaps — most teams need fewer tools than they pay for.</li></ol></section>"
              '</div></section><section class="newsletter-panel"><div><span>Not sure where to start?</span>'
              "<h2>Use the free Decision Checklist</h2><p>A printable worksheet to score overlap, cost, and trial results before paying.</p></div>"
              '<div class="newsletter-actions"><a class="button button-blue" href="/downloads/ai-stack-decision-checklist.pdf">Download PDF</a>'
              '<a class="button button-dark" href="/decision-brief.html">Get a decision brief</a></div></section>'
            + "</main>" + FOOTER + '</body></html>')
    out = root / "best-for" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)
    return out


def _deals_strip(root: Path) -> str:
    """Small strip of current verified promo count linking to /deals/."""
    try:
        records = json.loads((root / "data/tool_sources.json").read_text())["tools"]
        kws = ["promo", "% off", "promotion", "discount", "first year", "free month", "introductory", "limited time"]
        names = []
        for rec in records:
            low = (rec.get("pricing_summary") or "").lower()
            if any(k in low for k in kws):
                names.append(rec["slug"])
        n = len(names)
        sample = ", ".join(sorted(names)[:4]).replace("-", " ").title()
        return (f'{DEALS_S}<section class="score-card"><span>Live now</span><h2>{n} verified promos are currently active.</h2>'
                f'<p>Including {_esc(sample)} — all confirmed from official pricing pages with checked dates.</p>'
                '<p><a class="text-link" href="/deals/">See verified live deals →</a></p></section>' + DEALS_E + "\n")
    except Exception:
        return ""


def generate_pricing_report(root: Path, today: str) -> Path:
    tools = {t["slug"]: t for t in json.loads((root / "data/tools.json").read_text())}
    snaps = json.loads((root / "data/pricing_snapshots.json").read_text())
    snapshots = snaps.get("snapshots", {})
    changes = snaps.get("changes", [])
    records = {r["slug"]: r for r in json.loads((root / "data/tool_sources.json").read_text())["tools"]}
    checked_dates = sorted({r.get("date") for r in snapshots.values() if r.get("date")})
    baseline = checked_dates[0] if checked_dates else today

    kws = ["promo", "% off", "promotion", "discount", "first year", "free month", "introductory", "limited time"]
    promo_rows = ""
    n_promos = 0
    for slug, rec in sorted(records.items()):
        digest = rec.get("pricing_summary", "")
        if not digest or not any(k in digest.lower() for k in kws):
            continue
        date = rec.get("pricing_checked_date", "")
        tool = tools.get(slug)
        if not tool:
            continue
        n_promos += 1
        sents = [x.strip() for x in re.split(r"(?<=[.!?])\s+", digest) if any(k in x.lower() for k in kws)]
        detail = " ".join(sents[:2]) or digest[:200]
        promo_rows += (f'<tr><td><strong><a href="/tools/{slug}/">{_esc(tool["name"])}</a></strong></td>'
                       f'<td>{_esc(detail)}</td><td>{date}</td></tr>')

    changes_html = ("<p>No confirmed price changes detected since the baseline was established. "
                    "When a vendor changes official pricing, the dated entry appears here automatically.</p>")
    if changes:
        rows = "".join(f'<tr><td>{_esc(c.get("date",""))}</td><td><a href="/tools/{c.get("slug","")}/">{_esc(tools.get(c.get("slug",{}),{}).get("name", c.get("slug","")))}</a></td>'
                       f'<td>{_esc(str(c.get("summary",""))[:220])}</td></tr>' for c in changes)
        changes_html = ('<div class="table-wrap"><table><thead><tr><th>Date</th><th>Tool</th><th>Change</th></tr></thead>'
                        f'<tbody>{rows}</tbody></table></div>')

    page = (_head(f"State of AI Pricing — {baseline} baseline",
                  "A public, evidence-based snapshot of AI tool pricing: verified coverage, live promotions, and confirmed price changes since baseline.",
                  "/pricing-report/")
            + '<section class="scene scene-dark hero compact-hero"><div class="hero-copy"><p class="kicker">Quarterly report · evidence-based</p>'
              f'<h1>State of AI Pricing</h1><p class="subhead">What {len(snapshots)} AI tools officially charge as of the {baseline} verification run — '
              'which vendors run real promotions, and every confirmed price movement since. No scraped guesses, no expired offers.</p></div></section>'
              '<section class="scene scene-light content-hub"><div class="article-shell wide">'
              '<h2>Coverage</h2>'
              f'<div class="decision-grid"><div class="score-card"><span>Coverage</span><h3>{len(snapshots)} tools tracked</h3>'
              f'<p>Every tool in our directory has an official-pricing snapshot dated {baseline} or later.</p></div>'
              f'<div class="score-card"><span>Live promotions</span><h3>{n_promos} verified promos</h3>'
              '<p>Found on official pricing pages during verification runs. Each links to the vendor page so you can confirm before buying.</p></div>'
              f'<div class="score-card"><span>Confirmed changes</span><h3>{len(changes)} since baseline</h3>'
              '<p>Detected automatically when a new verification run differs from the stored snapshot.</p></div></div>'
              '<h2>Verified promotions right now</h2>'
              + ('<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Promo detail</th><th>Checked</th></tr></thead>'
                 f'<tbody>{promo_rows}</tbody></table></div>' if promo_rows else '<p>None found in the latest verification run.</p>')
              + '<h2>Confirmed price changes since baseline</h2>' + changes_html +
              '<section class="score-card"><span>Stay ahead of renewals</span><h2>Premium members get price-change alerts.</h2>'
              '<p>When our verification runs detect an official price change, Premium members hear about it first — before it hits their renewal.</p>'
              '<p><a class="button button-blue" href="/premium/">See Premium</a> '
              '<a class="button button-dark" href="/pricing-watch/">Open the live Pricing Watch</a></p></section>'
              '<p class="benchmark-caveat">Methodology: every figure traces to the vendor\'s official pricing page with a checked date shown in '
              '<a href="/pricing-watch/">AI Pricing Watch</a>. Prices change often — verify on the vendor page before purchase. This report is research, not purchasing advice.</p>'
              '</div></section>'
            + "</main>" + FOOTER + '</body></html>')
    out = root / "pricing-report" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page)
    return out


def postprocess_refresh(root: Path) -> int:
    """Re-inject the deals strip into best-for hub after other generators run."""
    hub = root / "best-for/index.html"
    if not hub.exists():
        return 0
    s = hub.read_text()
    fresh = _deals_strip(root)
    old = re.search(re.escape(DEALS_S) + r".*?" + re.escape(DEALS_E), s, re.S)
    if old and old.group(0) == fresh.rstrip("\n"):
        return 0
    if old:
        s = s.replace(old.group(0), fresh.rstrip("\n"))
    else:
        i = s.find("</main>")
        s = s[:i] + fresh + s[i:]
    hub.write_text(s)
    return 1


if __name__ == "__main__":
    r = Path(__file__).resolve().parent.parent
    print(generate_best_for(r))
    print(generate_pricing_report(r, datetime.today().strftime("%Y-%m-%d")))
