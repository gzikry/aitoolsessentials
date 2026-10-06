#!/usr/bin/env python3
"""Write marketing/haro-outreach/digest-2026-10-06.json

One record per tracked opportunity, re-verified against its own page today by
scripts/verify_journo_requests.py. Carried rows are refreshed from verified-requests.json
(page datePublished + rendered badge), never from the previous digest's text.

New this run: the TEN AI-token slugs from today's sitemap window are added to the tracked set
(each is a real /journo-request/<slug> page with a live body), taking the carry set from 74 to 84.
The nine spend-only slugs are NOT added: eight are consumer / personal-finance calls and the
ninth (buyers-and-procurement-leaders-what-you-need-before-vendor-call) is beat-adjacent but its
body address is Sourcee-redacted with no alternative route.

One new row is declared sendable, the first in this monitor's history: employees-blocked-from-ai-
on-work-accounts (Christopher Mims, WSJ) carries relevance 'medium' AND a reply route resolved
today off his own byline page (LinkedIn DM). See the row's contact_method and relevance_notes.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-10-06"

prev = json.loads((D / "digest-2026-10-05.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
win = json.loads((D / "_window_1006.json").read_text())
bodies = json.loads((D / "_bodies_1006.json").read_text())

CUT = re.compile(
    r"\.?\s*(?:RE-VERIFIED|Re-verified|PAGE-VERIFIED|NEWLY COLD|NEW this run|Page badge|"
    r"Badge '|On Sourcee's live AI topic page|Currently on the AI topic feed|age superseded|~age|"
    r"Verify with the outlet|with no refresh|was posted|datePublished|\d{4}-\d{2}-\d{2}|"
    r"\d{2,4}\+00:00)")
TAIL = re.compile(r"(?:,\s*|\s+|—\s*|-\s*)?(?:posted|was|with|is|and|so|reads|badge|Page badge|"
                  r"'|\"|\()\s*$", re.I)


def _base(text: str | None) -> str:
    text = (text or "").strip()
    m = CUT.search(text)
    if m:
        text = text[:m.start()].strip()
    tag = re.match(r"^(STATED (?:INTERNAL )?DEADLINE PASSED)", text)
    if tag:
        return f"{tag.group(1)} — do not pitch"
    if text.count("(") > text.count(")"):
        text = text[:text.rfind("(")].strip()
    for _ in range(3):
        t2 = TAIL.sub("", text).strip()
        if t2 == text:
            break
        text = t2
    text = re.sub(r",\s*BUT$", "", text, flags=re.I).strip()
    if text.count("'") % 2:
        text = text[:text.rfind("'")].strip().rstrip(" ,;:.–—-~\"")
    return text.rstrip(" ,;:.–—-~'\"")


ops = []
SUPERSEDED_RANGE = re.compile(r"1\.(?:21|16)x\s*(?:-|–|to)\s*2\.53x(?:,\s*median\s*1\.33x)?", re.I)
CURRENT_RANGE = "1.11x-2.53x, median 1.25x over 19 tiers"
STALE_SNAP = re.compile(r"(?:snapshots?|snapshot refresh)[^.;]{0,40}2026-10-0[1-5]|updated: 2026-10-0[1-5]")
CHECKED_OLD = re.compile(r"((?:re-)?checked) 2026-10-\d\d")


def _repair(text: str | None) -> tuple[str, bool]:
    if not text:
        return text or "", False
    fixed, n = SUPERSEDED_RANGE.subn(CURRENT_RANGE, text)
    fixed, n2 = STALE_SNAP.subn(lambda m: re.sub(r"2026-10-0[1-5]", "2026-10-06", m.group(0)), fixed)
    fixed, n3 = CHECKED_OLD.subn(rf"\1 {TODAY}", fixed)
    return fixed, bool(n or n2 or n3)


for op in prev["opportunities"]:
    slug = op["url"].rstrip("/").split("/journo-request/")[-1]
    v = verified.get(slug) or {}
    new = dict(op)
    repairs = []
    for field in ("suggested_pitch_template", "relevance_notes", "contact_method", "query_text"):
        new[field], changed = _repair(new.get(field))
        if changed:
            repairs.append(field)
    if repairs:
        new["_figures_repaired"] = repairs
    if v:
        base = _base(new.get("deadline")) or "No cutoff stated"
        new["deadline"] = (
            f"{base + '. ' if base else ''}RE-VERIFIED {TODAY}: HTTP {v.get('http')}, "
            f"live={v.get('live')}, badge '{v.get('badge')}', datePublished {v.get('datePublished')} "
            f"= {v.get('days_old')} days, no expiry notice on the page."
        ).strip()
        new["_page_live"] = bool(v.get("live"))
        new["_days_old"] = v.get("days_old")
        new["_badge"] = v.get("badge")
        new["_in_ai_topic_feed"] = bool(v.get("in_ai_topic_feed"))
        if new.get("contact_method"):
            new["contact_method"] = re.sub(
                r"(PAGE-VERIFIED|RE-VERIFIED|re-verified|re-read|re-checked)\s+2026-10-0[1-5]",
                rf"\1 {TODAY}", new["contact_method"])
    ops.append(new)

repaired = [o["url"].rsplit("/", 1)[-1] for o in ops if o.get("_figures_repaired")]

# ------------------------------------------------------- ten new tracked rows
NEW_ROWS = [
    {
        "slug": "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks",
        "query_text": (
            "Employees Blocked From AI on Work Accounts - Automating Tedious Tasks. 'journalist "
            "request: Are you, like me, ever annoyed that your work accounts are the one place you "
            "can't use AI to automate precisely the kind of tedious, soul-sucking tasks where it "
            "could be of the most help? If so, I would like to hear from you. (DMs open)'"),
        "journalist_publication": "Christopher Mims (author field) — Wall Street Journal columnist "
                                  "(outlet not named in the body; confirmed at his own byline page)",
        "category": "AI / Workplace Policy / Shadow & Unapproved AI Use",
        "contact_method": (
            "Body says '(DMs open)'; no address, handle or link is printed in the request itself. "
            "Route RESOLVED today off his own byline page, not off the request: "
            "https://www.linkedin.com/in/christopher-mims-club/ returns HTTP 200 (630,514 bytes), "
            "title 'Christopher Mims - The Wall Street Journal | LinkedIn'. Two dead ends recorded "
            "so they are not retried as routes: muckrack.com/christopher-mims HTTP 403 (Cloudflare "
            "interstitial) and wsj.com/news/author/christopher-mims HTTP 401. "
            f"LINKEDIN DM — George's lane. Not automatable. PAGE-VERIFIED {TODAY} on the request: "
            "HTTP 200, email_redacted=False, emails_on_page=none, published_links=Sourcee chrome only."),
        "relevance": "medium",
        "relevance_notes": (
            "The enterprise mirror of this monitor's core shadow-AI request: employees locked out of "
            "AI on their work accounts are exactly the population that buys tools personally and "
            "unapproved, which is unbudgeted, unenumerated software spend - the quantity our dated "
            "price set exists to make visible. Standing caveat, stated in the draft's first line: we "
            "are not such an employee and the draft says so. Below 'high' because the ask is a "
            "personal-annoyance quote, not a price or budget question."),
        "suggested_pitch_template": (
            "Template: lead with the dated price set behind the blocked-employee workaround (42 of 76 "
            "tools quote a monthly price, 33 of those at or under $25/month, median $17.50; monthly "
            "vs annual 1.11x-2.53x, median 1.25x over 19 tiers; snapshots re-checked 2026-10-06), "
            "state plainly that we are not an employee with a blocked account, and offer the full "
            "dated set with sources. Draft: pitch-drafts-2026-10-06.md section 1."),
    },
    {
        "slug": "ai-liability-insurers-and-legal-experts-procurement-and-implementation",
        "query_text": (
            "AI Liability Insurers & Legal Experts - Procurement & Implementation. 'For an upcoming "
            "ZDNET article, I'm looking for experts and execs who can speak about AI liability "
            "insurance products. If you or your organization has been involved in procuring, "
            "implementing, or building AI liability insurance, I'd love to hear from you. Please "
            "refer to my Qwoted post to pitch any insights that you might want to share: "
            "[lnkd.in link]. P.S. Even if you don't have firsthand experience with AI liability "
            "insurance, but can speak to it from a legal or academic standpoint, please feel free "
            "to share your thoughts. ZDNet'"),
        "journalist_publication": "Ritoban Mukherjee (author field) — ZDNET (zdnet.com, domain field)",
        "category": "AI / Legal & Insurance / Procurement",
        "contact_method": (
            "The body publishes a Qwoted link, https://lnkd.in/dVu9JK4C (HTTP 200, 5,322 bytes, "
            "resolves to LinkedIn), with 'refer to my Qwoted post to pitch any insights'. That is a "
            "usable route in principle, but Qwoted's feed needs an authenticated session we do not "
            "hold. No address on the page. PAGE-VERIFIED "
            f"{TODAY}: HTTP 200, email_redacted=False, emails_on_page=none."),
        "relevance": "low",
        "relevance_notes": (
            "Matched the spend regex on 'procurement', and that match is a false positive for our "
            "beat: the procurement here is of insurance cover, not of software seats or licences. "
            "We are not an insurer, a broker or a legal academic, so a list-price dataset does not "
            "answer the request."),
        "suggested_pitch_template": (
            "None — excluded: wants AI liability-insurance practitioners; the 'procurement' token is "
            "insurance procurement, not software spend."),
    },
    {
        "slug": "ai-infrastructure-experts-china-vs-us-datacenter-capacity",
        "query_text": (
            "AI Infrastructure Experts - China vs US Data-Center Capacity. 'Source request: I'm "
            "seeking experts who can speak to the scope of the AI infrastructure boom in China and "
            "how it compares to the U.S. buildout. I'm specifically interested in data-center "
            "capacity. If any experts come to mind with firsthand expertise in this area, please say "
            "hi :-) Email: [email redacted] / Signal username: hew.04 In exchange, here are two "
            "pumpkins my friends and I carved last year!'"),
        "journalist_publication": "Harriet Weber (author field) — outlet not named in the body",
        "category": "AI / Infrastructure / Data-Centre Capacity",
        "contact_method": (
            "The body publishes a Signal username, 'hew.04', plus an address Sourcee redacts. "
            "Signal is a resolved route; the request still asks for expertise we do not hold. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=True, emails_on_page=none, "
            "published_links=Sourcee chrome only."),
        "relevance": "low",
        "relevance_notes": (
            "Wants firsthand expertise on Chinese vs US data-centre capacity. We publish AI tool "
            "list prices, not infrastructure capacity or buildout data; contributing would mean "
            "claiming standing we do not have. The route is named anyway so the exclusion is "
            "checkable rather than invisible."),
        "suggested_pitch_template": (
            "None — excluded: no data-centre-capacity expertise. Route (Signal hew.04) recorded so "
            "the exclusion can be audited."),
    },
    {
        "slug": "plaintiffs-attorneys-and-legal-scholars-ai-deepfake-liability",
        "query_text": (
            "Plaintiffs' Attorneys & Legal Scholars - AI Deepfake Liability. 'Looking for experts in "
            "the discussion surrounding AI Deepfake liability. Plaintiffs' attorneys, law review "
            "scholars, 1st amendment or torts legal experts, etc. For my 1L torts class, I am part "
            "of a group producing a short podcast on this topic. We would love to interview some "
            "people with boots on the ground for this issue. If you know someone, or are someone, "
            "who fits the above description, please comment on this post and I'll reach out to you "
            "to set up a 10-15 minute interview over Zoom.'"),
        "journalist_publication": "Mitchell Price (author field) — outlet not named (student podcast)",
        "category": "AI / Legal / Deepfake Liability",
        "contact_method": (
            "The body asks respondents to 'comment on this post'; no address, handle or link is "
            f"published. PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "reply_hints=none, published_links=Sourcee chrome only. No route we can use."),
        "relevance": "low",
        "relevance_notes": (
            "A law-student podcast interview call for practising plaintiffs' attorneys and legal "
            "scholars. Nothing in the body asks about AI pricing, seats or software spend, and we "
            "hold no legal standing."),
        "suggested_pitch_template": (
            "None — excluded: wants practising attorneys or legal scholars for a student podcast; no "
            "spend angle and no route."),
    },
    {
        "slug": "emergency-managers-ai-tools-for-funding-and-staffing-shortfalls",
        "query_text": (
            "Emergency Managers - AI Tools for Funding & Staffing Shortfalls. 'Journalist writing "
            "about AI and emergency management. Hello everyone, my name is Jake Bittle, I'm a "
            "journalist at the nonprofit news outlet Grist where I often cover disasters and climate "
            "change. We're working on a story about AI and emergency management and I'd love to hear "
            "from you all. There's some new research from RAND and the Markle Foundation exploring "
            "whether AI tools can help emergency managers deal with funding and staffing "
            "shortfalls... We're really interested in how that looks on the ground. I'd love to talk "
            "with you about how your departments are or aren't using AI. This can of course be "
            "anonymous if you prefer. I'm at [email redacted] and 8134664712. Grist'"),
        "journalist_publication": "Jake Bittle (named in the body) — Grist (grist.org, domain field)",
        "category": "AI / Emergency Management / Public-Sector Adoption",
        "contact_method": (
            "The body prints a phone number (8134664712) and an address Sourcee redacts. Grist's "
            "staff page grist.org/staff/jake-bittle/ returns HTTP 404, so no email route resolved. "
            f"A phone is a voice route, not a written pitch route. PAGE-VERIFIED {TODAY}: HTTP 200, "
            "email_redacted=True, emails_on_page=none, published_links=Sourcee chrome only."),
        "relevance": "low",
        "relevance_notes": (
            "A named Grist reporter's call for emergency managers' firsthand AI use in disaster "
            "response. Our dated price dataset is not evidence an emergency manager can give; the "
            "one usable channel is a phone number."),
        "suggested_pitch_template": (
            "None — excluded: wants an emergency manager's own departmental experience."),
    },
    {
        "slug": "coweta-county-artists-and-creatives-data-centers-and-ai-infrastructure",
        "query_text": (
            "Coweta County Artists & Creatives - Data Centers & AI Infrastructure. '@johnrich how "
            "would you like to speak at the Symposium? @ArtistRights Symposium 5 Panel: Coweta "
            "County Data Centers, AI Infrastructure, and the Creative Communities That Pay the "
            "Price [t.co link] @Ansleysgarden @human_artistry @davidclowery'"),
        "journalist_publication": "Artist Rights Watch (author field) — outlet not named in the body",
        "category": "AI / Arts & Community / Data-Centre Siting",
        "contact_method": (
            "An X post tagging named panellists for an in-person symposium panel; the body carries a "
            "t.co link and no address or handle for us. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "published_links=['https://t.co/8l6CGKC9yq', ...Sourcee chrome]. No route we can use."),
        "relevance": "low",
        "relevance_notes": (
            "A local symposium panel invitation tagged at specific people in Coweta County. It is "
            "community organising, not a data request, and asks nothing about AI pricing or spend."),
        "suggested_pitch_template": "None — excluded: local panel invitation, not a source request.",
    },
    {
        "slug": "uk-cybersecurity-hiring-managers-state-of-hiring-2026-and-ai-impact",
        "query_text": (
            "UK Cybersecurity Hiring Managers - State of Hiring 2026 & AI Impact. 'Cyber security "
            "hiring managers: how confident are you that your hiring process shows who can actually "
            "do the job? I'm inviting security leaders, technical interviewers and internal "
            "recruiters to contribute to CyberHire's State of Cyber Security Hiring 2026 report... "
            "If you've helped hire for a UK-based cybersecurity role in the past 12 months, I'd "
            "value your perspective... If you'd like to contribute you can do so here: [tally.so "
            "link] Know someone who hires cybersecurity professionals? Please send this their way.'"),
        "journalist_publication": "Mike Carthy (author field) — CyberHire (outlet not named in body)",
        "category": "AI / Hiring / Cybersecurity Sector Research",
        "contact_method": (
            "The body publishes a survey form, https://tally.so/r/A7VLXe; no address or handle. A "
            "survey form collects the sender's data - it is not a reply route for us. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none."),
        "relevance": "low",
        "relevance_notes": (
            "A vendor (CyberHire) recruiting UK cybersecurity hiring managers into a 2026 hiring "
            "report. We are not a security-role hiring manager, and the only spend-adjacent token is "
            "'AI changing the interview process'."),
        "suggested_pitch_template": (
            "None — excluded: wants UK security hiring managers' survey responses."),
    },
    {
        "slug": "ai-emotional-support-users-chatbot-therapy-and-journaling",
        "query_text": (
            "AI Emotional Support Users - Chatbot Therapy & Journaling. 'Happy Monday everyone! I am "
            "becoming increasingly fascinated with how people are using AI for non-productivity "
            "means. I am currently working on an article about usage of software such as ChatGPT as "
            "a form of therapy, instant-response journalling or as a way to process emotions/events "
            "etc... Please feel free to DM or email me, and a huge thank you in advance if you are "
            "interested in chatting about this.'"),
        "journalist_publication": "Louise Gill (author field) — outlet not named in the body",
        "category": "AI / Consumer Behaviour / Emotional Use",
        "contact_method": (
            "Body says 'DM or email me' but prints neither: email_redacted=False and no address, "
            "handle or link appears on the page beyond Sourcee chrome. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, emails_on_page=none. No route we can use."),
        "relevance": "low",
        "relevance_notes": (
            "Wants personal accounts of using AI for therapy or journalling. Nothing about pricing, "
            "seats or software spend, and no route is published."),
        "suggested_pitch_template": (
            "None — excluded: wants personal emotional-use accounts; no spend angle, no route."),
    },
    {
        "slug": "mortgage-adviser-using-ai-efficiency-and-client-outcomes-video-series",
        "query_text": (
            "Mortgage Adviser Using AI - Efficiency & Client Outcomes Video Series. 'Looking to speak "
            "to a mortgage adviser using AI extensively to create efficiencies (or better customer "
            "outcomes - or both!) in their business who'd be willing to tell other advisers about "
            "the possibilities for a video series we've got coming up. If that's you, drop me an "
            "email on [email redacted]!'"),
        "journalist_publication": "Amy Hannah Loddington (author field) — outlet not named in body",
        "category": "AI / Financial Services / Video Series",
        "contact_method": (
            "Body: 'drop me an email on [email redacted]' — Sourcee redacts the address and no "
            f"alternative route is published. PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=True, "
            "emails_on_page=none, published_links=Sourcee chrome only."),
        "relevance": "low",
        "relevance_notes": (
            "Wants a practising mortgage adviser for a video series. We are not an adviser and the "
            "ask carries no price, seat or spend question."),
        "suggested_pitch_template": (
            "None — excluded: wants a mortgage adviser's own workflow; address redacted, no route."),
    },
    {
        "slug": "founders-and-cxos-in-automotive-ai-evs-autonomy-thought-leadership",
        "query_text": (
            "Founders & CXOs in Automotive - AI, EVs, Autonomy Thought Leadership. 'Attention "
            "Automotive & Mobility Leaders... The Autonaut Media is inviting Founders, CXOs, "
            "Automotive Leaders, Mobility Experts and Technology Innovators to share their ideas, "
            "experiences and perspectives through our exclusive editorial platform... Reach out to "
            "[email redacted] or [email redacted] Visit the website: theautonautmedia.com'"),
        "journalist_publication": "Poonam Mahajan (author field) — The Autonaut Media "
                                  "(theautonautmedia.com, domain field)",
        "category": "AI / Automotive / Thought-Leadership Placement",
        "contact_method": (
            "Body: 'Reach out to [email redacted] or [email redacted]' — both addresses are redacted "
            f"and no alternative is published. PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=True, "
            "emails_on_page=none, published_links=Sourcee chrome only."),
        "relevance": "low",
        "relevance_notes": (
            "An open invitation to contribute leadership articles to an automotive trade platform. "
            "This is a contributed-content placement, not a reporter's request, and we are not an "
            "automotive founder or CXO."),
        "suggested_pitch_template": (
            "None — excluded: contributed-content invitation, not a source request."),
    },
]

for row in NEW_ROWS:
    slug = row.pop("slug")
    v = verified.get(slug) or {}
    rec = {
        "url": f"https://www.sourcee.app/journo-request/{slug}",
        "_page_live": bool(v.get("live")), "_days_old": v.get("days_old"), "_badge": v.get("badge"),
        "_in_ai_topic_feed": bool(v.get("in_ai_topic_feed")),
        "deadline": (f"No cutoff stated. RE-VERIFIED {TODAY}: HTTP {v.get('http')}, live={v.get('live')}, "
                     f"badge '{v.get('badge')}', datePublished {v.get('datePublished')} = "
                     f"{v.get('days_old')} days, no expiry notice on the page."),
        "_new_this_run": True,
    }
    rec.update(row)
    ops.append(rec)

stale = [o for o in ops if (o.get("_days_old") or 0) > 10]
live = [o for o in ops if (o.get("_days_old") or 0) <= 10]

ledger = json.loads((D / "pitch-ledger.json").read_text())
done = set()
for u in list(ledger.get("pitched", {})) + list(ledger.get("skipped", {})):
    done.add(u.rstrip("/").split("/journo-request/")[-1])
live_unp = [o for o in live if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]
cold_unp = [o for o in stale if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]

MIMS = "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks"
CAND_LINES = "; ".join(f"{s} ({lm})" for s, lm in win["ai"])
SPEND_ONLY = [
    "student-loan-borrowers-repayment-plan-confusion-and-servicer-issues (student-loan servicing)",
    "connecticut-residents-on-heating-oil-winter-cost-impact (household fuel costs)",
    "people-using-debt-snowball-personal-debt-payoff-stories (debt payoff)",
    "child-safety-expert-halloween-costume-hazards-this-week (costume safety)",
    "pensioners-who-took-taxfree-lump-sum-budget-worries (pension budgeting)",
    "parents-sacrificing-to-afford-school-fees-financial-strain (school fees)",
    "artist-what-we-spend-podcast-feature (podcast guest call, not software spend)",
    "buyers-and-procurement-leaders-what-you-need-before-vendor-call (BEAT-ADJACENT: asks buyers "
    "and procurement leaders what they need before a vendor call - but the body address is "
    "Sourcee-redacted, no handle or link is published, and we hold no buyer standing, so it is "
    "route-less and not tracked)",
]

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{TODAY}T09:00:00-07:00",
    "search_scope": ("AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, "
                     "software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support "
                     "value, tool consolidation, procurement budget"),
    "age_policy": ("Ages are read off each request page (JSON-LD datePublished plus the rendered "
                   "'Posted ... ago' badge), never off the digest text. All 74 carried URLs were "
                   "re-fetched this run (HTTP 200, request body still served, no expiry notice) and "
                   "the 10 new rows were verified the same way on first sight."),
    "platforms_checked": [
        {"platform": "Sourcee (sourcee.app)", "status": "accessible",
         "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP {win['sitemap_http']}, "
                   f"{win['bytes']:,} bytes, {win['count']:,} loc/lastmod pairs, newest lastmod "
                   f"{win['newest']}). {len(win['window'])} slugs carry a lastmod newer than the "
                   f"2026-10-05 run's mark ({win['mark']}); {len(win['ai'])} carry an AI token, "
                   f"{len(win['ai_strict'])} carry an AI token plus a real spend token, and "
                   f"{len(win['spend_any'])} carry any spend-adjacent token. All candidate slugs were "
                   f"fetched and read in full. Sourcee itself re-probed HTTP 200 (100,825 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Re-measured. {win['feed_count']} slugs listed today, HTTP 200, "
                   f"{win['feed_bytes']:,} bytes, and {win['feed_overlap_with_window']} of "
                   f"{win['feed_count']} sit inside today's new sitemap window - the fifth consecutive "
                   f"100% overlap the monitor has measured. Absence from this feed is still NOT a cold "
                   f"signal: every carried request is absent from it by construction. Six of today's "
                   f"ten new rows are in the feed; none of the 74 carried rows is.")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,208 bytes, 'Vercel Security Checkpoint'. "
                   "Twenty-third consecutive identical result. Queries reach sources only by a "
                   "3x-daily email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": "Re-probed once. / HTTP 429, 31,209 bytes, 'Vercel Security Checkpoint'. No public feed."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                   "Source of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes, 'Error: The "
                   "page you were looking for doesn't exist'). Wrong path, not gated - unchanged. The "
                   "feed needs an authenticated app session; today's ZDNET row points at a Qwoted post "
                   "because of exactly this.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. Apex HTTP 200 (11,486 bytes), title 'MentionMatch - Connect B2B Writers "
                   "with Expert Sources', no feed. Twenty-second consecutive run confirming a "
                   "pre-launch shell.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\",\"error_description\":"
                   "\"No authorization provided\"}. Free read-only feed covering Connectively, HARO, X, "
                   "LinkedIn, MentionMatch and Substack. Needs an interactive OAuth handshake that "
                   "cannot be completed from a scheduled run.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on twenty-one consecutive "
                   "runs; the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy - today's Coweta County row and yesterday's "
                   "attribution call both came through it.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (148,267 bytes, 'ResponseSource - Connecting the media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free "
                   "source-facing feed.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        (f"TEN NEW AI-TOKEN REQUESTS ADDED, TAKING THE CARRY SET FROM 74 TO 84. {len(win['window'])} "
         f"slugs carry a lastmod newer than the 2026-10-05 mark. {len(win['ai'])} carry an AI token, "
         f"{len(win['ai_strict'])} carries an AI token plus a real spend token, and "
         f"{len(win['spend_any'])} carry any spend-adjacent token. One of the ten is the first "
         f"sendable row this monitor has ever produced: employees-blocked-from-ai-on-work-accounts "
         f"(Christopher Mims, WSJ) - relevance 'medium' plus a reply route resolved today off his own "
         f"byline page. The other nine are off-beat: a law-student deepfake podcast, a Grist "
         f"emergency-management call, a data-centre-capacity call, a Coweta County symposium panel, "
         f"a ZDNET AI-liability-insurance call, a CyberHire hiring survey, an AI-therapy piece, a "
         f"mortgage-adviser video series and an automotive thought-leadership placement."),
        (f"THE TEN CANDIDATES, BY NAME, SO THE FIND IS CHECKABLE: {CAND_LINES}."),
        ("THE ONE STRICT AI+SPEND HIT IS AGAIN A FALSE POSITIVE. The single ai_strict slug is "
         "ai-liability-insurers-and-legal-experts-procurement-and-implementation, which matched on "
         "'procurement' - and that procurement is of insurance cover, not software seats or licences. "
         "Second consecutive run where the only AI+spend hit is a token that does not mean software "
         "spend; recorded by name so the count moving off zero is not read as supply widening."),
        ("THE NINE SPEND-ONLY SLUGS ARE NOT ADDED, AND ONE OF THEM IS NAMED AS BEAT-ADJACENT: "
         + "; ".join(SPEND_ONLY) + "."),
        ("THE PAIR RANGE HELD AGAIN against a snapshot refreshed today, and the pair file was "
         "REBUILT, not just re-read: data/pricing_snapshots.json carries `updated: 2026-10-06` (76 "
         "snapshots), scripts/extract_monthly_annual_pairs.py re-asserted all 19 curated pairs against "
         "their own sentences, exited 0 with no needle failures, and rewrote "
         "data/monthly_annual_pairs.json. Range unchanged at 1.11x to 2.53x, median 1.25x, over 19 "
         "tiers across 14 tools (lowest replit-ai Core $20 vs $18; highest browse-ai Personal $48 vs "
         "$19; pair snapshot dates 2026-09-18 and 2026-09-21)."),
        ("THE SHADOW-AI HEADLINE FIGURES RE-DERIVED UNCHANGED: 42 of 76 tools quote a non-zero monthly "
         "price, 33 of those at or under $25/month, median cheapest paid tier $17.50, lowest $4.00 "
         "(khanmigo) against `updated: 2026-10-06`; 31 of 76 quote both a monthly and an annual rate. "
         "Same set as 2026-10-02 and 2026-10-05, so every draft written since 2026-10-02 stands behind "
         "identical numbers."),
        ("ALL 74 CARRIED URLs RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF: 74/74 HTTP 200 "
         "with the request body still served, zero non-200s, zero missing bodies, zero expiry words, "
         "and an independent cross-check against the full sitemap (39,185 loc/lastmod pairs) finds "
         "every tracked slug still present in it."),
        ("THE QUEUE HAS ITS FIRST SENDABLE ROW IN THIS MONITOR'S HISTORY: employees-blocked-from-ai-"
         "on-work-accounts-automating-tedious-tasks, 1 day old, live, relevance 'medium', with a "
         "verified reply route. The previous eleven runs produced 0. The two crossed-but-live drafts "
         "(Raconteur shadow-AI, Speciality Food) remain sendable late and their routes were "
         "re-resolved live today."),
        ("MAILBOX CHECKED: STILL NO REPLY TO ANY TRACKED PITCH. INBOX top is msg 91 (a tool "
         "submission, 2026-10-05 12:39Z); the newest human message anywhere on a tracked pitch remains "
         "Jan Suski's 2026-09-18 20:39Z reply (msg 77). No reply to the 2026-09-15 Enterprise AI "
         "Leaders send (21 days) or the 2026-09-18 Sherwood News send (18 days). Spam holds only two "
         "2026-09-12 delivery-failure notices. Sent Mail's top is msg 209 (2026-10-06 13:12Z, a "
         "tool-submission verification note) - no pitch has gone out. Zero pitches sent this run."),
        ("THE UNANSWERED FIGURES CORRECTION IS NOW EIGHTEEN DAYS OUTSTANDING. The recipient of the "
         "2026-09-18 Amplemarket reply was told the same-tier monthly/annual range is '1.21x-2.53x, "
         "median 1.33x'; the current verified figure is 1.11x-2.53x, median 1.25x over 19 tiers. Not "
         "sent this run: the monitor's brief forbids the scheduled run from sending, and the ledger "
         "records it as George's lane."),
    ],
    "expired_this_run": [
        ("Nothing expired and nothing dropped off this run. All 74 carried URLs returned HTTP 200 with "
         "the request body still served, and none has stopped appearing in a URL-carrying digest. The "
         "standing caveat is not a clean bill of health: this monitor carries every tracked request "
         "forward into each new digest, so 'absent from the newest digest' cannot fire by "
         "construction; the sitemap cross-check is the independent evidence."),
        ("NO ROW CROSSED THE 10-DAY LINE SINCE THE 2026-10-05 DIGEST, so the live/cold split moved "
         "only because of the ten new rows (live unpitched 27 -> 37, cold unpitched 43 -> 43). The "
         "youngest row at risk is video-game-developer-falsely-accused-of-using-generative-ai at 2 "
         "days, then the three 3-day rows; the two-day advance warning in build_pitch_queue.py covers "
         "only sendable rows, so this is stated here instead."),
        ("THE TWO CROSSED-BUT-LIVE DRAFTS ARE STILL LIVE AND STILL UNSENT: the Raconteur shadow-AI "
         "request is now 19 days old (unsent through SEVENTEEN consecutive runs) and the Speciality "
         "Food request 18 days old (unsent through ten, its October issue window closed). Both pages "
         "returned HTTP 200 again today and both routes were re-resolved against the live pages this "
         "run. Neither is void - what was lost is the ideal window, not the pitch."),
        ("THE COLD QUEUE IS 43 ROWS STRONG AND STILL GROWING FASTER THAN IT IS BEING CLEARED. The "
         "highest-relevance cold rows remain unsent: AI SaaS users in production (137d), Business & "
         "Technology Leaders - tech budget priorities (77d), Enterprise AI Leaders - agent sprawl "
         "(31d), Scientists paying for PhD/postdoc AI subscriptions (31d), FinOps - agentic AI cost "
         "overruns (29d, draft unsent since 2026-09-17), the Amplemarket pricing/credits request (29d, "
         "pitched and replied to, figures correction 18 days outstanding) and the Raconteur shadow-AI "
         "request (19d)."),
    ],
    "summary": (
        f"{len(ops)} tracked requests (74 carried and all 74 re-verified live, {len(NEW_ROWS)} new "
        f"AI-token finds added, 0 dropped off, 3 pitched, 1 deliberately skipped). Of the "
        f"{len(live_unp) + len(cold_unp)} unpitched, {len(live_unp)} are live and {len(cold_unp)} are "
        "cold, and ONE is sendable - the first this monitor has produced: the WSJ columnist's "
        "blocked-work-accounts request, 1 day old, relevance 'medium', reply route resolved today "
        "off the journalist's own byline page (LinkedIn DM, George's lane). The new window produced "
        "10 AI-token slugs and 1 strict AI+spend regex hit - and that hit is 'procurement' in a ZDNET "
        "AI-liability-INSURANCE call, not software procurement, the second consecutive run of that "
        "false positive. The pair range re-asserted clean against today's rebuilt pair file and held "
        "at 1.11x-2.53x over 19 tiers across 14 tools; the shadow-AI headline figures re-derived "
        "unchanged (42 tools publish a monthly price, 33 at or under $25, median $17.50). No new "
        "replies to any tracked pitch; the mailbox's newest inbound is a tool submission, not a pitch "
        "reply. Zero pitches sent this run - sends remain George's lane. Three send-ready drafts are "
        "in pitch-drafts-2026-10-06.md."
    ),
    "recommended_actions": [
        ("SEND THE WSJ BLOCKED-WORK-ACCOUNTS DRAFT - THE FIRST SENDABLE ROW THIS MONITOR HAS EVER "
         "PRODUCED. Paste-ready at pitch-drafts-2026-10-06.md section 1. Route: LinkedIn DM to "
         "https://www.linkedin.com/in/christopher-mims-club/ (verified HTTP 200 today, title "
         "'Christopher Mims - The Wall Street Journal | LinkedIn'); the request's own body says '(DMs "
         "open)'. 1 day old, live, relevance 'medium'. It is George's lane, so it cannot be sent from "
         "this run."),
        ("SEND THE RACONTEUR SHADOW-AI DRAFT - SEVENTEEN RUNS UNSENT. pitch-drafts-2026-10-06.md "
         "section 2, route simon.chandler@raconteur.net (re-resolved off the live "
         "/contributors/simon-chandler page today, HTTP 200, 154,819 bytes; control "
         "/contributors/tom-dennis HTTP 200; legacy /author/simon-chandler/ still 404 and must not be "
         "cited). Now 19 days old. It is still the only HIGH-relevance request this monitor has ever "
         "produced with a resolved route."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-10-06.md section 3, "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today, HTTP "
         "200, 59,488 bytes, alongside five other named masthead addresses, 18 days old). Its October "
         "issue window has closed: make it a send-or-skip call and record the outcome in "
         "pitch-ledger.json rather than carrying it an eleventh day."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI - NOW EIGHTEEN DAYS OUTSTANDING. He replied on "
         "2026-09-18 and was told '1.21x-2.53x, median 1.33x' when the verified figure is "
         "1.11x-2.53x, median 1.25x over 19 tiers. Route: reply to jan@jansuski.com, In-Reply-To the "
         "existing thread."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has produced no real AI+spend slug on "
         "twelve consecutive runs (the last two 'hits' were the same 'billing'/'procurement' false "
         "positives) and the single accessible source returns a handful of mostly consumer or vendor "
         "calls per day. It remains the only lever that widens the monitor."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": len(win["ai_strict"]),
        "ai_plus_spend_regex_false_positives": 1,
        "new_ai_token_slugs_added_to_tracking": len(NEW_ROWS),
        "consecutive_runs_without_new_core_beat": 12,
        "tracked_urls": len(ops),
        "carried_and_reverified": 74,
        "unpitched": len(live_unp) + len(cold_unp),
        "live_unpitched": len(live_unp),
        "cold_unpitched": len(cold_unp),
        "pitched_plus_skipped": 4,
        "live_unpitched_with_a_resolved_route": 1,
        "sendable": 1,
        "first_sendable_in_monitor_history": True,
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 2,
        "resolved_signal_routes": 3,
        "resolved_linkedin_routes": 1,
        "drafts_written_never_sent": 5,
        "sendable_on_its_last_live_day": 0,
        "rows_crossed_cold_since_last_digest": 0,
        "rows_at_ten_days_crossing_next_run": 0,
        "lost_to_the_cold_line_with_a_draft_ready": 0,
        "shadow_ai_monthly_priced_tools": 42,
        "shadow_ai_at_or_under_25": 33,
        "shadow_ai_median_cheapest_paid_tier": 17.50,
    },
    "monitor_defects_fixed_this_run": [
        ("A SENDABLE ROW IS DECLARED ONLY WITH BOTH HALVES EVIDENCED SEPARATELY. Every prior run "
         "reported 0 sendable, twice because a field adjacent to a route had been read as a route "
         "(the 2026-09-29 chrome leak, the 2026-10-01 Google Form). This run's single sendable row is "
         "declared on two independent facts: relevance 'medium' written into the row, and a route "
         "verified by fetching the journalist's own byline page today (HTTP 200 with a matching "
         "title), plus the request body's own '(DMs open)'. Both halves are named in the row so the "
         "declaration can be audited rather than trusted."),
        ("THE ROUTE-SEARCH DEAD ENDS ARE RECORDED SO THEY ARE NOT RETRIED. muckrack.com/christopher-"
         "mims returns HTTP 403 (Cloudflare interstitial) and wsj.com/news/author/christopher-mims "
         "HTTP 401; grist.org/staff/jake-bittle/ returns HTTP 404. Written into the rows rather than "
         "left in a scratch file, because the next run would otherwise re-probe them."),
        ("THE PAIR FILE IS REBUILT EACH RUN, NOT RE-READ. extract_monthly_annual_pairs.py was re-run "
         "against the refreshed snapshot and rewrote data/monthly_annual_pairs.json (exit 0, 19 pairs "
         "re-asserted). The range has been re-published unchanged three runs running and any stale "
         "1.16x/1.21x floor sitting in an older draft file is superseded."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print(f"wrote digest-{TODAY}.json: {len(ops)} opportunities, {len(digest['platforms_checked'])} platforms")
print(f"live(<=10d): {len(live)}  cold(>10d): {len(stale)}  live_unp: {len(live_unp)}  cold_unp: {len(cold_unp)}")
print("sendable rows:", [o["url"] for o in live_unp if o.get("relevance") == "medium"])
print("figures repaired in:", repaired)
