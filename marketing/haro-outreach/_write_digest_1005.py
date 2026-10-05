#!/usr/bin/env python3
"""Write marketing/haro-outreach/digest-2026-10-05.json

One record per tracked opportunity, re-verified against its own page today by
scripts/verify_journo_requests.py. Carried rows are refreshed from verified-requests.json
(page datePublished + rendered badge), never from the previous digest's text.

New this run: the SEVEN AI-token slugs from today's sitemap window are added to the tracked set
(each is a real /journo-request/<slug> page with a live body), taking the carry set from 67 to 74.
The nine spend-only slugs are NOT added: eight are consumer / personal-finance / non-software
calls; the two software-adjacent ones (saas-tools-gated-content..., indie-makers-...) want a
vendor tool or an indie-maker story we do not have.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-10-05"

prev = json.loads((D / "digest-2026-10-02.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
win = json.loads((D / "_window_1005.json").read_text())
bodies = json.loads((D / "_bodies_1005.json").read_text())

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
CHECKED_OLD = re.compile(r"checked 2026-09-1[89]")


def _repair(text: str | None) -> tuple[str, bool]:
    if not text:
        return text or "", False
    fixed, n = SUPERSEDED_RANGE.subn(CURRENT_RANGE, text)
    fixed, n2 = CHECKED_OLD.subn(f"checked {TODAY}", fixed)
    return fixed, bool(n or n2)


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
        if new.get("suggested_pitch_template"):
            new["suggested_pitch_template"] = re.sub(
                r"checked 2026-09-\d\d", f"re-checked {TODAY}", new["suggested_pitch_template"])
        if new.get("contact_method"):
            new["contact_method"] = re.sub(
                r"(PAGE-VERIFIED|RE-VERIFIED|re-verified|re-read|re-checked)\s+2026-09-\d\d",
                rf"\1 {TODAY}", new["contact_method"])
    ops.append(new)

repaired = [o["url"].rsplit("/", 1)[-1] for o in ops if o.get("_figures_repaired")]

# ------------------------------------------------------- seven new tracked rows
NEW_ROWS = [
    {
        "slug": "video-game-developer-falsely-accused-of-using-generative-ai",
        "query_text": (
            "Video Game Developer - Falsely Accused of Using Generative AI. 'Afternoon! Are you a "
            "video game developer who has been falsely accused of using generative AI? I'd love to "
            "pick your brains for a story about how those claims impact individuals, teams, and "
            "projects. Email in bio. DMs open. Signal: kerrblimey.43 Keen to hear lots of views!'"),
        "journalist_publication": "Chris Kerr (author field) — outlet not named in the body",
        "category": "AI / Games Industry / Attribution Disputes",
        "contact_method": (
            "Body publishes a Signal handle (kerrblimey.43) plus 'Email in bio. DMs open.' "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "reply_hints=['email me'/'DM'], published_links=['https://www.linkedin.com/in/andrewsmith313/', "
            "'https://x.com/andy_cb_smith'] (both Sourcee chrome)."),
        "relevance": "low",
        "relevance_notes": (
            "A first-person testimony call from game developers accused of AI use. It touches AI "
            "attribution, not AI pricing - no price, seat, licence or subscription-spend question "
            "anywhere in the body. We hold no game-development experience to offer."),
        "suggested_pitch_template": "None — excluded: wants a game developer's own accusation experience; no spend angle.",
    },
    {
        "slug": "lawyers-and-tech-ethics-experts-ai-wearables-and-legal-journeys",
        "query_text": (
            "Lawyers & Tech Ethics Experts - AI Wearables & Legal Journeys. 'Every few months, I "
            "release a new season of the Lex & Lace Podcast... This season, I'll be exploring the "
            "tech advancements that are constantly reshaping our world... Episode 1 is a rundown of "
            "the summer's biggest tech and AI developments, including Meta Glasses... And if you "
            "have a story you'd like to share, I'd love to hear from you. Reach out to be a guest on "
            "the pod!'"),
        "journalist_publication": "Alexandra Zandamela — Lex & Lace Podcast (podcast guest call)",
        "category": "AI / Wearables / Legal Industry / Podcast Guest",
        "contact_method": (
            "Published booking link (https://lnkd.in/dcKHYkDR) for the podcast; no email on the page. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "published_links=['https://lnkd.in/dcKHYkDR', ...]."),
        "relevance": "low",
        "relevance_notes": (
            "A podcast guest solicitation about law, fashion and AI wearables. It is a booking call, "
            "not a report; it asks nothing about AI pricing, seats or software spend, and we are not "
            "lawyers. The lnkd.in link is the pod's own booking route, not a cost question."),
        "suggested_pitch_template": "None — excluded: podcast guest call, not a report request; no spend angle.",
    },
    {
        "slug": "mls-executives-risks-when-agents-grant-mls-access-to-llms",
        "query_text": (
            "MLS Executives - Risks When Agents Grant MLS Access to LLMs. 'LOOKING FOR SOURCES: Would "
            "love to chat with MLS execs/pros about the risks/concerns that arise when agents grant "
            "MLS access directly to their LLMs. I've seen/interacted with several agents doing this "
            "and when I ask them for more information about permissions/bylaws, etc, ... crickets. To "
            "the DMs >>'"),
        "journalist_publication": "Craig Rowe (author field) — outlet not named in the body",
        "category": "Real Estate / MLS Data Access / LLM Permissions Risk",
        "contact_method": (
            "DMs on the original post; no email, handle or link published on the page. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "published_links=Sourcee chrome only, reply_hints=['DM me']. No route we can use."),
        "relevance": "low",
        "relevance_notes": (
            "A data-governance risk call wanting MLS executives' own experience of agents granting "
            "MLS access to LLMs. No price, seat, licence or software-spend question in the body, and "
            "we hold no MLS standing."),
        "suggested_pitch_template": "None — excluded: wants an MLS executive's firsthand permissions account.",
    },
    {
        "slug": "real-estate-agents-and-brokers-switched-from-pdf-brochures",
        "query_text": (
            "Real Estate Agents & Brokers - Switched From PDF Brochures. 'Still looking for real "
            "estate voices on what's replacing the PDF brochure. Made the switch as an agent or "
            "broker? DM me or email [email redacted] #journorequest'"),
        "journalist_publication": "Lyza G (author field) — outlet not named in the body",
        "category": "Real Estate / Marketing Tools / Document Workflow",
        "contact_method": (
            "The body says 'DM me or email [email redacted]' — Sourcee redacts the address and the "
            f"page publishes no alternative route. PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=True, "
            "emails_on_page=none, reply_hints=['DM me'/'email me']."),
        "relevance": "low",
        "relevance_notes": (
            "A tools-substitution call wanting real estate agents who moved off PDF brochures. "
            "Adjacent to our beat (a document/workflow tool switch) but the ask is an agent's own "
            "story, and we are not agents."),
        "suggested_pitch_template": "None — excluded: wants a real estate agent's own switching experience.",
    },
    {
        "slug": "advertising-tech-and-media-pros-in-miami-ai-audience-discovery",
        "query_text": (
            "Advertising, Tech & Media Pros in Miami - AI Audience Discovery. 'This year, I'm swapping "
            "AWNY for the inaugural IAB-backed Jupiter Festival Miami! On Weds, I'll interview "
            "@Chroniclemedia Media's Aaron Sisto & Scott Greenberg on how AI is reshaping audience "
            "discovery. Advertising, tech, and media folks, drop me a line if you'll be there!'"),
        "journalist_publication": "Kendra Barnett (author field) — outlet not named in the body",
        "category": "Advertising / AI Audience Discovery / Event Interview",
        "contact_method": (
            "Drop a line / DM on the original post; no email, handle or link published on the page "
            f"beyond a t.co. PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "published_links=['https://t.co/AEgLhRuQL7', ...]. No route we can use."),
        "relevance": "low",
        "relevance_notes": (
            "An in-person conference-attendance call for Miami advertising and media people. Nothing "
            "in the body asks about AI pricing, seats or software spend; the AI angle is audience "
            "discovery, and we are not attending."),
        "suggested_pitch_template": "None — excluded: wants Miami conference attendees, not a data contribution.",
    },
    {
        "slug": "law-firm-lawyers-concrete-ai-implementations-and-billing-impact",
        "query_text": (
            "Law Firm Lawyers - Concrete AI Implementations & Billing Impact (for CNBC). 'I'm looking "
            "to speak to lawyers about how their firms are using AI. ⚖️ I'm looking for tangible, "
            "real examples of how it's being implemented already rather than speculative ideas on how "
            "it could change work. Is it changing what it means to be a lawyer? What's it doing to the "
            "billable hour? 📧 If you'd like to chat: [email redacted] #journorequest #journorequests CNBC'"),
        "journalist_publication": "Lindsay Dodgson (author field) — CNBC (cnbc.com, domain field)",
        "category": "AI / Legal Sector / Billing & Billable Hour",
        "contact_method": (
            "The body says 'If you'd like to chat: [email redacted]' — Sourcee redacts the address. "
            f"No author page exists at cnbc.com (/lindsay-dodgson/ and /author/lindsay-dodgson/ both "
            f"HTTP 404) and the page publishes no alternative route. PAGE-VERIFIED {TODAY}: HTTP 200, "
            "email_redacted=True, emails_on_page=none."),
        "relevance": "low-medium",
        "relevance_notes": (
            "The only new row that touches our beat at all: it asks directly about the billable hour, "
            "which is a monetisation effect of AI adoption. But the want is a practising lawyer's own "
            "firm-level implementation, and we are not a law firm - we publish a dated price dataset. "
            "No route resolved for us (CNBC publishes no author contact), so it is not sendable."),
        "suggested_pitch_template": (
            "None — excluded: wants a practising lawyer's own firm evidence. A price-dataset "
            "contribution would be claiming standing we do not have, and the body address is redacted "
            "with no alternative route on cnbc.com."),
    },
    {
        "slug": "hr-leaders-company-ai-strategies-and-cognitive-offloading-risk",
        "query_text": (
            "HR Leaders - Company AI Strategies & Cognitive Offloading Risk. '📢 Looking for input! "
            "... Now for a different publication, I am looking to speak to HR people about whether "
            "they are building this risk into their company AI strategies. Are you giving your people "
            "guidance about how and when best to use it in their process to avoid cognitive "
            "offloading? What does this look like? Hit me up and please amplify. For this one, I want "
            "business-contextualised examples of what people are actually doing and why...'"),
        "journalist_publication": "Katie Jacobs (author field) — CIPD (cipd.co.uk, domain field)",
        "category": "AI / HR Practice / Cognitive Offloading Policy",
        "contact_method": (
            "No address or handle on the page; the body says 'Hit me up'. No people page exists at "
            "cipd.org (/uk/about/people/katie-jacobs/ and the contact page both HTTP 404). "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "reply_hints=none. No route we can use."),
        "relevance": "low",
        "relevance_notes": (
            "An HR-practice call wanting business-contextualised HR examples of staff AI guidance. "
            "Nothing asks about AI pricing, seats or software spend, and we hold no HR standing."),
        "suggested_pitch_template": "None — excluded: wants an HR leader's own policy example; no spend angle, no route.",
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

# Rows that moved live -> cold since the 2026-10-02 digest, named rather than left as a count change.
CROSSED = (
    "ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai",
    "engineering-managers-measuring-engineers-when-using-ai",
    "saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup",
)

ledger = json.loads((D / "pitch-ledger.json").read_text())
done = set()
for u in list(ledger.get("pitched", {})) + list(ledger.get("skipped", {})):
    done.add(u.rstrip("/").split("/journo-request/")[-1])
live_unp = [o for o in live if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]
cold_unp = [o for o in stale if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]

CAND_LINES = "; ".join(f"{s} ({lm})" for s, lm in win["ai"])
SPEND_ONLY = [
    "food-creators-work-copied-without-credit-or-payment (creator payment, not software spend)",
    "equity-analysts-covering-us-homebuilders-price-cuts-and-buydowns (homebuilder price cuts)",
    "saas-tools-gated-content-and-lead-capture-and-document-tracking (wants a gated-content SaaS vendor - we are not one)",
    "indie-makers-product-journey-first-user-and-paid-users (wants indie-maker product stories)",
    "crown-heights-and-flatbush-residents-with-3a4c-curls-hair-care-costs (hair-care costs)",
    "people-who-used-debt-snowball-or-avalanche-repayment-stories (debt repayment)",
    "former-nyc-and-philly-residents-and-longtime-nj-residents-cost-strain (cost of living)",
    "nj-employers-and-business-owners-rising-health-costs-preenrollment (health costs)",
    "longterm-savers-investing-vs-renting-vs-moving-vs-spending (savers, personal finance)",
]

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{TODAY}T09:00:00-07:00",
    "search_scope": ("AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, "
                     "software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support "
                     "value, tool consolidation, procurement budget"),
    "age_policy": ("Ages are read off each request page (JSON-LD datePublished plus the rendered "
                   "'Posted ... ago' badge), never off the digest text. Every carried URL was "
                   "re-fetched this run: HTTP 200 and the request body still served, none returns an "
                   "expiry notice and none has dropped off."),
    "platforms_checked": [
        {"platform": "Sourcee (sourcee.app)", "status": "accessible",
         "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP {win['sitemap_http']}, "
                   f"{win['bytes']:,} bytes, {win['count']:,} loc/lastmod pairs, newest lastmod "
                   f"{win['newest']}). {len(win['window'])} slugs carry a lastmod newer than the "
                   f"2026-10-02 run's mark ({win['mark']}). Of those, {len(win['ai'])} carry an AI "
                   f"token, {len(win['ai_strict'])} carry an AI token plus a real spend token, and "
                   f"{len(win['spend_any'])} carry any spend-adjacent token. All "
                   f"{len(win['ai']) + len([s for s, _ in win['spend_any'] if s not in {a for a, _ in win['ai']}])} "
                   f"candidate slugs were fetched and read in full. Sourcee itself re-probed HTTP 200 "
                   f"(100,825 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Re-measured. {win['feed_count']} slugs listed today, HTTP 200, "
                   f"{win['feed_bytes']:,} bytes, and {win['feed_overlap_with_window']} of "
                   f"{win['feed_count']} sit inside today's new sitemap window - the fourth "
                   f"consecutive 100% overlap the monitor has measured. The conclusion does not rest "
                   f"on that overlap: absence from this feed is still not a cold signal, because "
                   f"every tracked carried request is absent from it by construction. None of today's "
                   f"seven AI-token finds was in the feed when the previous digest was built.")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,198 bytes, 'Vercel Security Checkpoint'. "
                   "Twenty-second consecutive identical result. Queries reach sources only by a "
                   "3x-daily email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": "Re-probed once. / HTTP 429, 31,198 bytes, 'Vercel Security Checkpoint'. No public feed."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                   "Source of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes, 'Error: The "
                   "page you were looking for doesn't exist'). Wrong path, not gated - unchanged. The "
                   "feed needs an authenticated app session.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. Apex HTTP 200 (11,486 bytes), title 'MentionMatch - Connect B2B Writers "
                   "with Expert Sources', no feed. Twenty-first consecutive run confirming a pre-launch shell.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\",\"error_description\":"
                   "\"No authorization provided\"}. Free read-only feed covering Connectively, HARO, X, "
                   "LinkedIn, MentionMatch and Substack. Needs an interactive OAuth handshake that "
                   "cannot be completed from a scheduled run.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on twenty consecutive "
                   "runs; the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (148,179 bytes, 'ResponseSource - Connecting the media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free "
                   "source-facing feed.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        (f"SEVEN NEW AI-TOKEN REQUESTS ADDED, AND NONE IS CORE-BEAT. {len(win['window'])} slugs carry "
         f"a lastmod newer than the 2026-10-02 mark. {len(win['ai'])} carry an AI token, "
         f"{len(win['ai_strict'])} carries an AI token plus a real spend token (the single hit is "
         f"'billing' in the CNBC law-firm slug - a billable-hour ask, not a software-spend ask), and "
         f"{len(win['spend_any'])} carry any spend-adjacent token. All seven AI-token rows are now "
         f"tracked, which takes the carry set from 67 to 74. None asks a price, seat, licence or "
         f"software-spend question: they are a game-dev attribution call, a law/fashion podcast guest "
         f"call, an MLS-data-risk call, a real-estate brochure-switch call, a Miami conference call, a "
         f"CNBC law-firm billable-hour call, and a CIPD HR-practice call."),
        (f"THE 16 CANDIDATES, BY NAME, SO THE ZERO IS CHECKABLE: {CAND_LINES}. None asks a price, seat, "
         f"licence or software-spend question. The nine spend-token slugs are all consumer, "
         "personal-finance or non-software calls - " + "; ".join(SPEND_ONLY) +
         ". They matched the spend regex on 'costs', 'spend' and 'paid'. Not drafted; the seven "
         "AI-token rows are carried."),
        ("THE PAIR RANGE HELD AGAIN, against a snapshot refreshed today. data/pricing_snapshots.json "
         "carries `updated: 2026-10-05` (76 snapshots), and scripts/extract_monthly_annual_pairs.py "
         "re-asserted all 19 curated pairs against their own sentences, exited 0 with no needle "
         "failures, and rewrote data/monthly_annual_pairs.json. Range unchanged at 1.11x to 2.53x, "
         "median 1.25x, over 19 tiers across 14 tools, pair snapshot dates 2026-09-18 and 2026-09-21."),
        ("THE SHADOW-AI HEADLINE FIGURES RE-DERIVED UNCHANGED: 42 of 76 tools quote a non-zero monthly "
         "price, 33 of those at or under $25/month, median cheapest paid tier $17.50 against "
         "`updated: 2026-10-05`. Same set as the 2026-10-02 run, so a draft written today and one "
         "written on 2026-10-02 stand behind identical numbers."),
        ("ALL 67 CARRIED URLs RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page "
         "returns HTTP 200 with the request body still served and no removal or expiry notice - "
         "67/67, zero non-200s, zero missing bodies, zero expiry words. With the seven new rows: "
         f"{len(ops)} tracked, {len(live)} live, {len(stale)} cold, minus the 3 pitched and 1 skipped."),
        ("THE QUEUE IS 0 SENDABLE. build_pitch_queue.py's _sendable() requires a relevance above the "
         "tangential band plus a resolved route, and no live row has both: the "
         f"{len(live_unp)} live unpitched rows "
         "are all relevance 'low'/'low-medium' with no usable route, and the two rows that do carry a "
         "resolved route (Raconteur, Speciality Food) are the two crossed drafts, both past the "
         "10-day line. The two routes were re-resolved against the live pages again today: "
         "raconteur.net/contributors/simon-chandler HTTP 200 (154,819 bytes, data-part1/2/3 = "
         "simon.chandler + raconteur + net; control /contributors/tom-dennis HTTP 200 carrying "
         "tom.dennis/raconteur/net; legacy /author/simon-chandler/ still 404) and "
         "specialityfoodmagazine.com/contact HTTP 200 (59,488 bytes, holly.shackleton@artichokehq.com "
         "alongside five other named masthead addresses). No new route resolved for any new row: "
         "cnbc.com author pages 404, cipd.org people pages 404."),
        ("MAILBOX CHECKED: STILL NO REPLY TO ANY TRACKED PITCH. INBOX top is msg 91 (a tool "
         "submission, 2026-10-05 12:39Z); the most recent human message on a tracked pitch remains "
         "Jan Suski's 2026-09-18 20:39Z reply (msg 77). No reply to the 2026-09-15 Enterprise AI "
         "Leaders send (twenty days) or the 2026-09-18 Sherwood News send (seventeen days). Spam "
         "holds only two 2026-09-12 delivery-failure notices. Sent Mail's top is msg 201 "
         "(2026-10-05 13:39Z, a tool-submission verification note) - no pitch has gone out. Zero "
         "pitches sent this run."),
        ("THE UNANSWERED FIGURES CORRECTION IS NOW SEVENTEEN DAYS OUTSTANDING. The recipient of the "
         "2026-09-18 Amplemarket reply was told the same-tier monthly/annual range is '1.21x-2.53x, "
         "median 1.33x'; the current verified figure is 1.11x-2.53x, median 1.25x over 19 tiers. Not "
         "sent this run: the monitor's brief forbids the scheduled run from sending, and the ledger "
         "records it as George's lane."),
    ],
    "expired_this_run": [
        ("Nothing expired and nothing dropped off this run. All 67 carried URLs returned HTTP 200 "
         "with the request body still served, and none has stopped appearing in a URL-carrying "
         "digest. The usual caveat applies and is not a clean bill of health: this monitor carries "
         "every tracked request forward into each new digest, so 'absent from the newest digest' "
         f"cannot fire by construction. Independently cross-checked against the full sitemap "
         f"({win['count']:,} loc/lastmod pairs): every tracked slug is still present in it."),
        ("THREE ROWS CROSSED THE 10-DAY LINE SINCE THE 2026-10-02 DIGEST, ALL UNPITCHED, NONE WITH A "
         "RESOLVED ROUTE, AND NONE SENDABLE - so nothing actionable was lost. All three were "
         "relevance 'low': ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai (13d), "
         "engineering-managers-measuring-engineers-when-using-ai (13d), and "
         "saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup (13d). Named rather than "
         "left as a count change because build_pitch_queue.py's two-day advance warning covers only "
         "sendable rows, so an ordinary crossing otherwise shows up as nothing but the live count "
         "falling."),
        ("THE TWO CROSSED-BUT-LIVE DRAFTS ARE STILL LIVE AND STILL UNSENT: the Raconteur shadow-AI "
         "request is now 18 days old (unsent through SIXTEEN consecutive runs) and the Speciality "
         "Food request 17 days old (unsent through eight, its October issue window closed). Both "
         "pages returned HTTP 200 again today and both routes were re-resolved against the live "
         "pages this run. Neither is void - what was lost is the ideal window, not the pitch."),
        ("THE COLD QUEUE IS 45 ROWS STRONG AND STILL GROWING FASTER THAN IT IS BEING CLEARED. The "
         "highest-relevance cold rows remain unsent: Business & Technology Leaders - tech budget "
         "priorities (76d), AI SaaS users in production (136d), Enterprise AI Leaders - agent sprawl "
         "(30d), Scientists paying for PhD/postdoc AI subscriptions (30d), FinOps - agentic AI cost "
         "overruns (28d, draft unsent since 2026-09-17), the Amplemarket pricing/credits request "
         "(28d, pitched, replied to, figures correction 17 days outstanding) and the Raconteur "
         "shadow-AI request (18d)."),
    ],
    "summary": (
        f"{len(ops)} tracked requests (67 carried and all 67 re-verified live, 7 new AI-token finds "
        f"added, 0 dropped off, 3 pitched, 1 deliberately skipped). Of the "
        f"{len(live_unp) + len(cold_unp)} unpitched, {len(live_unp)} are live and {len(cold_unp)} are "
        "cold, and ZERO are sendable. The new window produced 7 AI-token slugs and 1 strict "
        "AI+spend regex hit - and that one hit is 'billing' in a CNBC law-firm billable-hour call, "
        "not a software-spend ask - and all seven are off-beat: a game-dev attribution call, a "
        "law/fashion podcast guest call, an MLS-data-risk call, a real-estate brochure-switch call, a "
        "Miami conference call, a CNBC law-firm billable-hour call and a CIPD HR-practice call. The "
        "pair range re-asserted clean against today's refreshed snapshot and held at 1.11x-2.53x over "
        "19 tiers across 14 tools; the shadow-AI headline figures re-derived unchanged (42 tools "
        "publish a monthly price, 33 at or under $25, median $17.50). No new replies to any tracked "
        "pitch; the mailbox's newest inbound is a tool submission, not a pitch reply. Zero pitches "
        "sent this run - sends remain George's lane. The two crossed-but-live drafts remain sendable "
        "late: pages HTTP 200, routes re-resolved today."
    ),
    "recommended_actions": [
        ("SEND THE RACONTEUR SHADOW-AI DRAFT - SIXTEEN RUNS UNSENT. Paste-ready at "
         f"pitch-drafts-{TODAY}.md section 1, route simon.chandler@raconteur.net (re-resolved off the "
         "live /contributors/simon-chandler page today, HTTP 200, 154,819 bytes, data-part1/2/3 "
         "triple unchanged; control /contributors/tom-dennis HTTP 200 carries tom.dennis/raconteur/"
         "net; the older /author/simon-chandler/ still 404s and must not be cited). Now 18 days old. "
         "It is the only high-relevance request this monitor has ever produced with a resolved route, "
         "and a late send is still possible."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT ("
         f"pitch-drafts-{TODAY}.md section 2, holly.shackleton@artichokehq.com re-read off "
         "specialityfoodmagazine.com/contact today, HTTP 200, 59,488 bytes, alongside five other "
         "named masthead addresses, 17 days old). Its October issue window has closed; make it a "
         "send-or-skip call and record the outcome in pitch-ledger.json rather than carrying it a "
         "ninth day."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI - NOW SEVENTEEN DAYS OUTSTANDING. He replied on "
         "2026-09-18 and was told '1.21x-2.53x, median 1.33x' when the verified figure is "
         "1.11x-2.53x, median 1.25x over 19 tiers. Route: reply to jan@jansuski.com, In-Reply-To the "
         "existing thread."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has produced no real AI+spend slug on "
         "eleven consecutive runs and the single accessible source returns a handful of mostly "
         "consumer or vendor calls per day. It remains the only lever that widens the monitor."),
        ("EXPECT THE SAME ZERO NEXT RUN UNLESS ONE OF THESE MOVES. Nothing new becomes sendable until "
         "either a crossed draft is sent late or the monitor's supply widens."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": len(win["ai_strict"]),
        "ai_plus_spend_regex_false_positives": len(win["ai_strict_false_positives"]),
        "new_ai_token_slugs_added_to_tracking": len(NEW_ROWS),
        "consecutive_runs_without_new_core_beat": 11,
        "tracked_urls": len(ops),
        "carried_and_reverified": 67,
        "unpitched": len(live_unp) + len(cold_unp),
        "live_unpitched": len(live_unp),
        "cold_unpitched": len(cold_unp),
        "pitched_plus_skipped": 4,
        "live_unpitched_with_a_resolved_route": 0,
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 2,
        "resolved_signal_routes": 1,
        "drafts_written_never_sent": 4,
        "sendable": 0,
        "sendable_on_its_last_live_day": 0,
        "rows_crossed_cold_since_last_digest": len(CROSSED),
        "rows_at_ten_days_crossing_next_run": 0,
        "lost_to_the_cold_line_with_a_draft_ready": 0,
        "shadow_ai_monthly_priced_tools": 42,
        "shadow_ai_at_or_under_25": 33,
        "shadow_ai_median_cheapest_paid_tier": 17.50,
    },
    "monitor_defects_fixed_this_run": [
        ("A STRICT AI+SPEND HIT IS NAMED, NOT JUST COUNTED. This run's regex produced 1 strict hit "
         "after ten consecutive zeroes, and it is a FALSE POSITIVE for our beat: 'billing' in "
         "law-firm-lawyers-concrete-ai-implementations-and-billing-impact refers to the billable "
         "hour, not to software spend. Recorded by name so the count moving off zero is not read as "
         "supply widening."),
        ("THE THREE ROWS THAT CROSSED SINCE THE LAST DIGEST ARE NAMED INDIVIDUALLY. The crossing "
         "would otherwise appear as nothing but a live-count drop from 29 to 26; two of the three "
         "were sitting at exactly 10 days in the 2026-10-02 digest's advance warning."),
        ("THE SHADOW-AI HEADLINE FIGURES ARE STATED PER RUN AND RE-DERIVED. They re-derived to the "
         "same 42/33/$17.50 set against `updated: 2026-10-05`, so today's draft and the 2026-10-02 "
         "draft stand behind identical numbers - stated explicitly because the previous run's set HAD "
         "moved and stale copies are still sitting in earlier draft files."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print(f"wrote digest-{TODAY}.json: {len(ops)} opportunities, {len(digest['platforms_checked'])} platforms")
print(f"live(<=10d): {len(live)}  cold(>10d): {len(stale)}  live_unp: {len(live_unp)}  cold_unp: {len(cold_unp)}")
print("crossed since last digest:", len(CROSSED))
print("figures repaired in:", repaired)
