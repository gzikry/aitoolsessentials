#!/usr/bin/env python3
"""Sitewide SEO/monetization sweep:

1. FAQPage schema on content pages missing it — derived from the page's real
   question-style H3s where present, otherwise a generic evidence-based FAQ.
   Only applies to articles/use-cases/guides/comparisons content pages (not hubs).
2. Affiliate coverage: inject approved ElevenLabs + Make links into the deals hub
   and top buyer guides via a dedicated module (FTC-compliant, sponsored attrs
   handled by wire_affiliate_links.py which runs later in the pipeline).
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from affiliate_util import inject_nous_referral_module

DOMAIN = "https://aitoolsessentials.com"
MARK_START = "<!-- AIT SWEEP FAQ START -->"
MARK_END = "<!-- AIT SWEEP FAQ END -->"


def _questions_from_page(s: str) -> list[tuple[str, str]]:
    """Extract real Q&A pairs: H3 phrased as a question + following paragraph."""
    qa: list[tuple[str, str]] = []
    for m in re.finditer(r"<h3>([^<]{8,140}\?)</h3>\s*<p>(.{40,600}?)</p>", s, re.S):
        q = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        a = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if q.endswith("?") and not any(x in a.lower() for x in ("<a", "http")):
            qa.append((q, a[:400]))
        if len(qa) >= 4:
            break
    return qa


FAQ_SCHEMA_RE = re.compile(
    r'<!-- AIT SWEEP FAQ START -->.*?<!-- AIT SWEEP FAQ END -->\n?', re.S
)


def postprocess(root: Path, tools: list[dict[str, Any]] | None = None, today: str | None = None) -> dict[str, int]:
    tools_list: list[dict[str, Any]] = tools if tools is not None else json.loads((root / "data/tools.json").read_text())
    today = today or datetime.today().strftime("%Y-%m-%d")
    stats = {"faq_added": 0, "affiliate_modules": 0}

    content_dirs = ["articles", "use-cases", "comparisons", "guides"]
    for d in content_dirs:
        dd = root / d
        if not dd.exists():
            continue
        for p in dd.rglob("*.html"):
            s = p.read_text()
            # Skip hubs/index pages. If this sweep previously added FAQ schema,
            # strip the old block and re-add it so the pass is idempotent.
            if p.name == "index.html":
                continue
            had_sweep_block = MARK_START in s
            if had_sweep_block:
                s = FAQ_SCHEMA_RE.sub("", s)
            # If another generator already provides FAQPage schema, leave it alone.
            if "FAQPage" in s:
                if had_sweep_block:
                    p.write_text(s)
                continue
            qa = _questions_from_page(s)
            generic = [
                ("How were these recommendations verified?",
                 "Pricing and claims trace to each vendor's official page with a checked date; editorial scores are independent of sponsorships and affiliate relationships."),
                ("Are the affiliate links on this page paid placements?",
                 "Some outbound tool links are affiliate links. They never change rankings or scores, and every page carries an FTC-compliant disclosure."),
            ]
            use = qa if len(qa) >= 2 else generic
            faq_schema = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in use
                ],
            }
            block = (
                f"{MARK_START}<script type=\"application/ld+json\">"
                f"{json.dumps(faq_schema, separators=(',', ':'))}</script>{MARK_END}\n</head>"
            )
            if "</head>" in s:
                s = FAQ_SCHEMA_RE.sub("", s)  # remove stale first
                s = s.replace("</head>", block, 1)
                p.write_text(s)
                stats["faq_added"] += 1

    # ---- affiliate coverage module on deals hub + top buyer guides ----
    targets = [
        root / "deals/index.html",
        root / "articles/best-ai-writing-tools.html",
        root / "articles/best-free-ai-writing-tools.html",
        root / "articles/best-ai-productivity-tools.html",
        root / "articles/transcript-to-newsletter-pipeline.html",
        root / "articles/jasper-alternatives.html",
    ]
    A_MARK_S = "<!-- AIT AFFILIATE MODULE START -->"
    A_MARK_E = "<!-- AIT AFFILIATE MODULE END -->"
    A_RE = re.compile(re.escape(A_MARK_S) + r".*?" + re.escape(A_MARK_E) + r"\n?", re.S)
    module = (
        f"{A_MARK_S}<section class=\"score-card\" style=\"margin:26px auto 0;max-width:880px\">"
        "<span>Verified picks</span><h3>Tools we recommend with confidence</h3>"
        "<p>Two of our highest-scored tools have partner programs we're enrolled in. "
        "Links below are affiliate links — they never influence our rankings.</p>"
        '<p><a href="https://try.elevenlabs.io/xs6witq7izqe" target="_blank" rel="sponsored nofollow noopener">Try ElevenLabs (editorial 4.6/5) →</a>'
        ' &nbsp;·&nbsp; <a href="https://www.make.com/en/register?pc=aitoolsessentials" target="_blank" rel="sponsored nofollow noopener">Try Make.com (automation pick) →</a></p>'
        f"</section>{A_MARK_E}"
    )
    for t in targets:
        if not t.exists():
            continue
        s = t.read_text()
        if A_MARK_S in s:
            new_s = A_RE.sub(lambda _m: module, s)
        else:
            i = s.rfind("</main>")
            if i == -1:
                continue
            new_s = s[:i] + module + "\n" + s[i:]
        if new_s != s:
            t.write_text(new_s)
            stats["affiliate_modules"] += 1

    nous_targets = [
        root / "categories" / "AI Agents" / "index.html",
        root / "start-here" / "index.html",
    ]
    for t in nous_targets:
        if not t.exists():
            continue
        s = t.read_text()
        new_s = inject_nous_referral_module(s)
        if new_s != s:
            t.write_text(new_s)
            stats["affiliate_modules"] += 1


    # ---- lead magnet module on homepage + high-intent utilities ----
    L_MARK_S = "<!-- AIT LEAD MAGNET START -->"
    L_MARK_E = "<!-- AIT LEAD MAGNET END -->"
    L_RE = re.compile(re.escape(L_MARK_S) + r".*?" + re.escape(L_MARK_E) + r"\n?", re.S)
    lead_module = (
        f"{L_MARK_S}<section class=\"newsletter-panel\"><div><span>Free buyer checklist</span>"
        "<h2>Download the AI Stack Decision Checklist</h2>"
        "<p>Print this one-page worksheet before buying another AI subscription. It helps you score overlap, cost, trial results, and cancellation risk.</p>"
        "<p class=\"affiliate-inline\">No signup wall yet — use it now, then come back to Premium for monthly decision matrices and price alerts.</p></div>"
        "<div class=\"newsletter-actions\"><a class=\"button button-blue\" href=\"/downloads/ai-stack-decision-checklist.pdf\">Download PDF</a>"
        "<a class=\"button button-dark\" href=\"/downloads/ai-stack-decision-checklist.html\">Open HTML</a></div></section>"
        f"{L_MARK_E}"
    )
    lead_targets = [root / "index.html", root / "tool-finder.html", root / "stack-builder.html", root / "cost-calculator.html"]
    for t in lead_targets:
        if not t.exists():
            continue
        s = t.read_text()
        if L_MARK_S in s:
            new_s = L_RE.sub(lambda _m: lead_module, s)
        else:
            i = s.rfind("</main>")
            if i == -1:
                continue
            new_s = s[:i] + lead_module + "\n" + s[i:]
        if new_s != s:
            t.write_text(new_s)
            stats.setdefault("lead_modules", 0)
            stats["lead_modules"] += 1



    # ---- pricing page explore module (top entry page cross-links) ----
    PE_S = "<!-- AIT PRICING EXPLORE START -->"
    PE_E = "<!-- AIT PRICING EXPLORE END -->"
    PE_RE = re.compile(re.escape(PE_S) + r".*?" + re.escape(PE_E) + r"\n?", re.S)
    pe_module = (
        f"{PE_S}<section class=\"scene scene-light content-hub\"><div class=\"article-shell wide\">"
        "<h2>Try the free research tools first</h2>"
        "<p>Not ready to subscribe? These public utilities use the same verification data our members get:</p>"
        '<div class="content-hub-grid">'
        '<article class="content-hub-card"><span>Free tracker</span><h3><a href="/pricing-watch/">AI Pricing Watch</a></h3>'
        "<p>Verified official-pricing snapshots for all 40 tracked tools, each with a checked date.</p></article>"
        '<article class="content-hub-card"><span>Free report</span><h3><a href="/pricing-report/">State of AI Pricing</a></h3>'
        "<p>The quarterly evidence-based summary: coverage stats, live promotions, confirmed changes.</p></article>"
        '<article class="content-hub-card"><span>Free utility</span><h3><a href="/stack-audit.html">Instant Stack Audit</a></h3>'
        "<p>No-login keep/cut scorecard. Stays on your device. Not a Whop charge.</p></article>"
        '<article class="content-hub-card"><span>Free utility</span><h3><a href="/decision-brief.html">Decision Brief</a></h3>'
        "<p>Pick 2–3 tools and generate a shareable decision brief with overlap warnings.</p></article>"
        '<article class="content-hub-card"><span>Free download</span><h3><a href="/downloads/ai-stack-decision-checklist.html">Decision Checklist</a></h3>'
        "<p>Printable worksheet to score overlap, cost, and trial results before paying for anything.</p></article>"
        "</div></div></section>" + PE_E
    )
    pricing_page = root / "pricing" / "index.html"
    if pricing_page.exists():
        s2 = pricing_page.read_text()
        if PE_S in s2:
            new = PE_RE.sub(lambda _m: pe_module, s2)
        else:
            i = s2.rfind("</main>")
            new = s2[:i] + pe_module + "\n" + s2[i:] if i != -1 else s2
        if new != s2:
            pricing_page.write_text(new)
            stats.setdefault("pricing_explore", 0)
            stats["pricing_explore"] += 1

    return stats


if __name__ == "__main__":
    root0 = Path(__file__).resolve().parent.parent
    print(postprocess(root0))
