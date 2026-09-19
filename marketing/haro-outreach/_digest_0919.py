#!/usr/bin/env python3
"""Build digest-2026-09-19.json from what this run actually verified.

Every record's age/badge/liveness comes from verified-requests.json, which scripts/verify_journo_requests.py
re-read off each request page today. Query text, publication and category are carried from the digest
where the request first appeared; the two requests new to this monitor are written by hand from their
own page bodies. Nothing here is carried on trust: each of the 29 tracked URLs returned HTTP 200 today.
"""
import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
ver = json.load(open(D / "verified-requests.json"))

# richest record per slug from digest history
hist = {}
for f in sorted(D.glob("digest-*.json")):
    for op in (json.loads(f.read_text()).get("opportunities") or []):
        u = (op.get("url") or "").strip()
        if "/journo-request/" not in u:
            continue
        s = u.split("/journo-request/")[-1].strip("/")
        rec = hist.get(s)
        if not rec or len(op.get("query_text") or "") > len(rec.get("query_text") or ""):
            hist[s] = op

bodies = {}
for f in ("_bodies_0919.json", "_bodies_0919b.json", "_bodies_0918.json", "_bodies_0918b.json"):
    p = D / f
    if p.exists():
        for k, v in json.loads(p.read_text()).items():
            if (v or {}).get("core"):
                bodies[k] = v


def core(slug):
    return " ".join((bodies.get(slug, {}).get("core") or "").replace("&amp;", "&").replace("&#x27;", "'").split())


def body_after_headline(slug):
    """The request body with Sourcee's own 'Posted ... ago <Headline>' prefix stripped."""
    c = core(slug)
    c = re.sub(r"^Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago)\s*", "", c)
    hl = (bodies.get(slug, {}).get("headline") or "").strip()
    if hl and c.startswith(hl):
        c = c[len(hl):].strip()
    return c


def age_line(slug, extra="No cutoff stated."):
    v = ver[slug]
    dp = (v.get("datePublished") or "")[:19]
    return (f"{extra} Page badge reads '{v.get('badge')}'; datePublished {dp}Z "
            f"({v.get('days_old')} days at this run). Re-verified live this run: HTTP {v.get('http')}, "
            f"page still serves the request body, no expiry notice.")


NEW = {
    "fulltime-employees-shadow-ai-use-and-paying-outofpocket": {
        "query_text": body_after_headline("fulltime-employees-shadow-ai-use-and-paying-outofpocket"),
        "journalist_publication": "Raconteur (raconteur.net) — author named in the page's own author field: Simon Chandler",
        "category": "AI / Shadow AI Spend / Out-of-Pocket Subscriptions / Enterprise Tech",
        "deadline": age_line("fulltime-employees-shadow-ai-use-and-paying-outofpocket"),
        "contact_method": "The page redacts the address ('Please email me at [email redacted]'), but Raconteur's own byline pages publish the writer's address as an obfuscated data-part1/2/3 triple that the site's JS assembles at runtime (scripts-last.min.js: part1 + '@' + part2 + '.' + part3). Reconstructed and cross-checked against a second author this run: simon.chandler@raconteur.net. raconteur.net MX = Google Workspace (aspmx.l.google.com). Raconteur's /contact page states PRs should contact the relevant writer directly.",
        "relevance": "high",
        "relevance_notes": "The closest thing to our core beat that Sourcee has produced in six runs: employees buying AI tools without approval and paying for them personally is unbudgeted, unenumerated software spend — the exact quantity our dated price set exists to make visible. Raconteur's own contact page says it wants 'pitches with exclusive business data', which is what we hold. Honesty constraint: the request asks for employees to give personal quotes and we are a publisher, not a shadow-AI employee, so the pitch must offer the price evidence and say outright that we hold no personal account. Its title says Raconteur; the byline that published the request is on raconteur.net, and the article is anonymous-source-based.",
        "suggested_pitch_template": "Template 2 (Overlapping Subscriptions / Cost Optimization), shadow-spend framing — lead with the affordability threshold computed from data/pricing_snapshots.json today: 31 of the 76 tools we track have a cheapest paid tier at or under $25/month, median $16.50, lowest $4 (Khanmigo, checked 2026-09-18); and the same tier billed monthly instead of annually runs up to 2.53x (Browse AI $48/month vs $19/month billed annually, checked 2026-09-18). Offer the dated set; state plainly that we have no personal shadow-AI account to quote.",
    },
    "speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech": {
        "query_text": body_after_headline("speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech"),
        "journalist_publication": "Speciality Food magazine (specialityfoodmagazine.com) — author named in the page's own author field: Holly Shackleton, Content Editor",
        "category": "Retail Tech Budget / £10k Procurement / Speciality Food",
        "deadline": age_line("speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech",
                             "For the October issue, so the window is roughly two weeks."),
        "contact_method": "The page redacts the address, but the magazine's /contact page publishes named editorial addresses: holly.shackleton@artichokehq.com (Content Editor), verified live this run. artichokehq.com MX = Outlook/Microsoft 365 (artichokehq-com.mail.protection.outlook.com).",
        "relevance": "low-medium",
        "relevance_notes": "Fresh (1 day) and with a verified email route to the named author, but a standing mismatch: the request asks speciality food and drink businesses how they would spend £10k on EPOS, shelf labels, ecommerce and stock systems. We are not a food retailer and our price set covers AI tools, not retail hardware. The only honest contribution is the pricing-method half — what a fixed budget buys at dated prices, and how billing term changes it — offered as a benchmark rather than as a retailer's own answer.",
        "suggested_pitch_template": "Template 2 (cost optimization), budget-benchmark framing — lead with a verified figure and no currency conversion: 40 of the 76 AI tools we track publish a non-zero monthly price, 31 of them at or under $25/month, and of those that quote both terms the same tier runs 1.21x-2.53x depending on whether it is billed monthly or annually (checked 2026-09-18). Offer the dated set as a benchmark against their £10k and say we are not a food retailer.",
    },
}

# Requests this run re-verified but that carry a passed deadline, an unverifiable route, or no
# standing: recorded, ranked low, and marked do-not-pitch in the deadline field itself.
OVERRIDE = {
    "tech-policy-experts-california-ai-audit-bills-impact-cios": dict(
        deadline="STATED DEADLINE PASSED — 'looking to speak with a source today' was posted 2026-09-10 (badge 'Posted 9 days ago'; datePublished 2026-09-10T15:11:11Z). Page is live with no expiry notice but the ask is spent. Do not pitch."),
    "uk-managers-cracked-down-on-gen-z-ai-overuse": dict(
        deadline="STATED INTERNAL DEADLINE PASSED ('by this Wednesday September 9'). Page live, no expiry notice; badge 'Posted 12 days ago'; datePublished 2026-09-07T09:57:18Z. Cold: crossed the 10-day line this run."),
    "finops-professionals-agentic-ai-cost-overruns": dict(
        deadline="No cutoff stated. Page badge now reads 'Posted 12 days ago'; datePublished 2026-09-07T14:19:46Z. NEWLY COLD this run: it was the queue's #1 on 2026-09-17 at 10 days and has crossed the 10-day line unpitched. Its route is a LinkedIn DM to a named author (linkedin.com/in/niloy-ghosh)."),
    "anthropic-users-and-business-owners-customer-service-experiences": dict(
        deadline="No cutoff stated. Page badge reads 'Posted in last 7 days'; datePublished 2026-09-11T16:58:59Z (7 days at this run, up from 5 on 2026-09-17). Re-verified live: HTTP 200, body unchanged, Signal handle still published. The request has NOT been renewed or edited since posting — see the lastmod finding below.",
        contact_method="Signal handle 'hliwrites.99' published verbatim in the request (re-read off the live page this run); DMs or email also invited, address redacted on Sourcee.",
        relevance_notes="On-beat as a subscription-value story rather than a grievance: we hold dated official Anthropic pricing and no customer-service complaint of our own, so the honest contribution is the price side only. The route is the strongest thing about it — a Signal handle, published in the request, is a direct channel. Its age is now 7 days and rising, so send or drop."),
}

ORDER = [
    # live and unpitched, strongest first
    "fulltime-employees-shadow-ai-use-and-paying-outofpocket",
    "anthropic-users-and-business-owners-customer-service-experiences",
    "earlystage-founders-building-saas-and-ai-tools-built-from-scratch",
    "speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech",
    "us-founders-calls-to-slow-ai-development-impact-on-companies",
    "ediscovery-lawyers-aiassisted-review-impact-on-practice",
    "gen-z-ai-data-annotators-work-experience-and-income-impact",
    "ai-automation-experts-speakers-on-marketing-sales-operations-gains",
    "ecommerce-marketers-transparency-in-ai-recommendations-and-conversion",
    "cybersecurity-companies-and-experts-ai-scams-and-consumer-safety",
    "edtech-product-managers-lms-audit-does-product-manage-learning",
    "tech-policy-experts-california-ai-audit-bills-impact-cios",
    "fulltime-placeholder-removed",
    # newly cold
    "finops-professionals-agentic-ai-cost-overruns",
    "uk-managers-cracked-down-on-gen-z-ai-overuse",
    "ai-startups-workplace-fraud-detection-expenses-time-theft",
    "marketing-and-content-leaders-aiassisted-work-review-process",
    "ai-agents-making-money-2026-sales-and-leadgen-workflow-ops",
    # pitched / skipped — carried so the queue can exclude them by URL
    "enterprise-ai-leaders-value-creation-ownership-and-governance",
    "amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot",
    "individual-contributors-managing-ai-agents-without-title-or-pay",
    # cold archive, page-verified today
    "enterprise-ai-leaders-ai-governance-and-agent-sprawl",
    "scientists-phd-students-and-postdocs-paying-for-ai-subscriptions",
    "ceos-ai-impact-on-ops-culture-and-commercial-strategy",
    "business-and-technology-leaders-tech-budget-priorities-amid-volatility",
    "ai-saas-users-in-production-integrations-and-autonomous-workflows",
    "uk-finance-risk-and-regulatory-leaders-ai-explainability-risks",
    "ai-project-builders-youtube-finance-and-lifestyle-channel-feature",
    "msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends",
    "sme-owners-operational-challenges-for-ai-solutions-case-study",
]

ops = []
for slug in ORDER:
    if slug not in ver:
        print("SKIP (not verified):", slug)
        continue
    h = hist.get(slug, {})
    o = {
        "url": f"https://www.sourcee.app/journo-request/{slug}",
        "query_text": (h.get("query_text") or core(slug))[:1200],
        "journalist_publication": h.get("journalist_publication") or "(publication not captured; page author field holds the byline)",
        "category": h.get("category") or "(uncategorised)",
        "deadline": h.get("deadline") or age_line(slug),
        "contact_method": h.get("contact_method") or "(route recorded from the request page)",
        "relevance": h.get("relevance") or "medium",
        "relevance_notes": h.get("relevance_notes") or "",
        "suggested_pitch_template": h.get("suggested_pitch_template") or "",
    }
    if slug in NEW:
        o.update(NEW[slug])
    if slug in OVERRIDE:
        o.update(OVERRIDE[slug])
    if o["relevance"] in ("high on topic, low on currency", "medium (adjacent, not core AI-spend)",
                          "low-medium (adjacent; no cost or spend angle in the text)"):
        o["relevance"] = {"high on topic, low on currency": "medium",
                          "medium (adjacent, not core AI-spend)": "medium",
                          "low-medium (adjacent; no cost or spend angle in the text)": "low-medium"}[o["relevance"]]
    # Carried deadline/contact prose was written on the day it was written and states ages that are
    # now wrong ("0 days", "less than 24 hours old", "1 day"), and Sourcee has since reworded some
    # bodies. Age, liveness and route are re-stated from today's page read; the carried prose is
    # kept only for its own stated-deadline facts, with its stale age claims scrubbed.
    v = ver[slug]
    carried = re.sub(r"\((?:\d+|zero|one) days?\)", "(age superseded)", o["deadline"])
    carried = re.sub(r"(?:is |now )?\d+ days? old", "age superseded", carried)
    carried = re.sub(r"(posted )?less than 24 hours old at run time", "posted, age superseded", carried)
    carried = re.sub(r"\(\d+ days\)\.?$", "", carried).strip()
    verified_line = (f"PAGE-VERIFIED 2026-09-19: HTTP {v.get('http')}, live={v.get('live')}, badge "
                     f"'{v.get('badge')}', datePublished {(v.get('datePublished') or '')[:19]}Z = "
                     f"{v.get('days_old')} days, no expiry notice on the page.")
    o["deadline"] = f"{carried} {verified_line}".strip()
    if slug not in NEW and slug not in OVERRIDE:
        o["contact_method"] = (f"{o['contact_method']} | PAGE-VERIFIED 2026-09-19: "
                               f"email_redacted={v.get('email_redacted')}, "
                               f"emails_on_page={v.get('emails_on_page') or 'none'}, "
                               f"reply_hints={v.get('reply_hints') or 'none'}.")
    ops.append(o)

print("opportunities written:", len(ops))
json.dump(ops, open("/tmp/ops_0919.json", "w"), indent=1)
for o in ops:
    s = o["url"].split("/journo-request/")[-1]
    print(f"  {ver[s]['days_old']:>4}d [{o['relevance']:<11}] {s}")
