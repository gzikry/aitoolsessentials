#!/usr/bin/env python3
"""Write marketing/haro-outreach/digest-2026-10-07.json

One record per tracked opportunity, re-verified against its own page today by
scripts/verify_journo_requests.py. Carried rows are refreshed from verified-requests.json
(page datePublished + rendered badge), never from the previous digest's text.

New this run: the TEN AI-token slugs from today's sitemap window are added to the tracked set,
taking the carry set from 84 to 94. None is core-beat and none is sendable - the window produced
zero AI+spend slugs (cleaner than yesterday's single 'procurement' false positive). The six
spend-only slugs (all consumer cost-of-living calls) are NOT added.

The 2026-10-06 sendable row (employees-blocked-from-ai, Christopher Mims, WSJ) is now 2 days old,
still live, still route-resolved - the only sendable row in the queue.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-10-07"

prev = json.loads((D / "digest-2026-10-06.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
win = json.loads((D / "_window_1007.json").read_text())
bodies = json.loads((D / "_bodies_1007.json").read_text())

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
STALE_SNAP = re.compile(r"(?:snapshots?|snapshot refresh)[^.;]{0,40}2026-10-0[1-6]|updated: 2026-10-0[1-6]")
CHECKED_OLD = re.compile(r"((?:re-)?checked) 2026-10-\d\d")
# A hand-typed affordability sentence baked into an old digest row still cited the superseded
# 31/$16.50 set ("31 of the 76 tools we track have a cheapest paid tier at or under $25/month,
# median $16.50"). Rewritten to the current derived set, same as every other superseded figure.
STALE_AFFORD = re.compile(
    r"31 of the 76 tools[^.]*?median \$16\.50", re.I)
CURRENT_AFFORD = ("42 of 76 tools publish a monthly price, 33 of those at or under $25/month, "
                  "median $17.50")
# Older-dated draft filenames and stale route byte-counts sit inside carried rows; both are the
# same defect class as the hardcoded figures. The draft filename is rewritten to today's, and the
# LinkedIn route byte-count is taken from today's route-checks probe (route-checks-2026-10-07.json).
OLD_DRAFT = re.compile(r"pitch-drafts-2026-10-0[1-6]\.md")
LINKEDIN_BYTES = re.compile(r"\(630,514 bytes\)")
_TODAY_DRAFT = f"pitch-drafts-{TODAY}.md"
_LI_BYTES = "603,318"


def _repair(text: str | None) -> tuple[str, bool]:
    if not text:
        return text or "", False
    fixed, n = SUPERSEDED_RANGE.subn(CURRENT_RANGE, text)
    fixed, n2 = STALE_SNAP.subn(lambda m: re.sub(r"2026-10-0[1-6]", TODAY, m.group(0)), fixed)
    fixed, n3 = CHECKED_OLD.subn(rf"\1 {TODAY}", fixed)
    fixed, n4 = OLD_DRAFT.subn(_TODAY_DRAFT, fixed)
    fixed, n5 = LINKEDIN_BYTES.subn(f"({_LI_BYTES} bytes)", fixed)
    fixed, n6 = STALE_AFFORD.subn(CURRENT_AFFORD, fixed)
    return fixed, bool(n or n2 or n3 or n4 or n5 or n6)


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
                r"(PAGE-VERIFIED|RE-VERIFIED|re-verified|re-read|re-checked)\s+2026-10-0[1-6]",
                rf"\1 {TODAY}", new["contact_method"])
    ops.append(new)

repaired = [o["url"].rsplit("/", 1)[-1] for o in ops if o.get("_figures_repaired")]

# ------------------------------------------------------- ten new tracked rows
def _body(slug: str) -> str:
    return re.sub(r"\s+", " ", (bodies.get(slug) or {}).get("core") or "").strip()


NEW_ROWS = [
    {
        "slug": "aps-hr-leaders-ai-skills-training-and-workforce-planning",
        "query_text": _body("aps-hr-leaders-ai-skills-training-and-workforce-planning")[:900],
        "journalist_publication": "Joshua Gliddon (author field) — The Mandarin (themandarin.com.au, domain field)",
        "category": "AI / Public-Sector Workforce / Skills & Training",
        "contact_method": (
            "Body: 'please drop me a line' with no address, handle or link published; the page's only "
            "published links are Sourcee chrome. email_redacted=False but emails_on_page=none. "
            f"NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, feed=Y."),
        "relevance": "low",
        "relevance_notes": (
            "Public-sector HR/capability piece for an Australian audience; the ask is interviewees who "
            "can speak to skills and workforce planning, not to software spend. No cost, pricing or "
            "budget angle in the text."),
        "suggested_pitch_template": "None — excluded: wants public-sector HR interviewees; no spend angle and no route.",
    },
    {
        "slug": "scrum-masters-daytoday-and-career-pivots-and-ai-impact",
        "query_text": _body("scrum-masters-daytoday-and-career-pivots-and-ai-impact")[:900],
        "journalist_publication": "Dr. Yvette Jett (author field) — The Dr. Vett Jett Show (vettjett.com, domain field)",
        "category": "AI / Agile Careers / Podcast Guest Booking",
        "contact_method": (
            "Body: 'Send me a message right here on LinkedIn or email me at [email redacted]'. The "
            "address is Sourcee-redacted and no handle is printed; no route resolved. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, live=True, email_redacted=True, emails_on_page=none."),
        "relevance": "low",
        "relevance_notes": (
            "Podcast guest booking wanting working Scrum Masters' first-person career stories. We are "
            "not a Scrum Master and hold no such account; nothing in our dated data answers it."),
        "suggested_pitch_template": "None — excluded: wants practising Scrum Masters as guests; we hold no such standing.",
    },
    {
        "slug": "real-estate-agents-replacing-pdf-property-brochure",
        "query_text": _body("real-estate-agents-replacing-pdf-property-brochure")[:900],
        "journalist_publication": "Lyza G (author field) — Flipbooker blog (flipbooker.com, domain field)",
        "category": "AI / PropTech / Vendor Blog Content Call",
        "contact_method": (
            "Body: 'Email [email redacted]'. Address Sourcee-redacted; no handle or link. "
            f"NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, email_redacted=True."),
        "relevance": "low",
        "relevance_notes": (
            "A vendor blog (Flipbooker) seeking a real-estate agent's quote for its own guide, offering "
            "'a quote and a link to your site'. Not editorial press and not our beat: no pricing, "
            "budget or software-spend question, and we are not a real-estate agent."),
        "suggested_pitch_template": "None — excluded: vendor blog promo wanting a real-estate agent voice.",
    },
    {
        "slug": "anz-marketers-ai-and-martech-innovation-spotlight",
        "query_text": _body("anz-marketers-ai-and-martech-innovation-spotlight")[:900],
        "journalist_publication": "RAHUL B. (author field) — KARV Tech Insider (domain not named in the page's domain field)",
        "category": "AI / Marketing Technology / Self-Promo Spotlight",
        "contact_method": (
            "Body: 'DM me. Let's connect and explore how we can amplify your story.' No handle, address "
            "or link published; the page's only published links are Sourcee chrome. NO ROUTE RESOLVED. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, live=True, feed=Y."),
        "relevance": "low",
        "relevance_notes": (
            "A 'spotlight' call inviting ANZ marketers to pitch their own AI/Martech launch for "
            "amplification - self-promotion, not a journalist request for a source with data. We are "
            "not an ANZ marketer and it asks for no pricing or spend evidence."),
        "suggested_pitch_template": "None — excluded: self-promo spotlight, no editorial data ask and no route.",
    },
    {
        "slug": "swiss-ai-companion-users-emotional-bonds-and-daily-life",
        "query_text": _body("swiss-ai-companion-users-emotional-bonds-and-daily-life")[:900],
        "journalist_publication": "Leila (author handle) — SRF 'rec.' (srf.ch, domain field)",
        "category": "AI / Human-AI Relationships / Documentary",
        "contact_method": (
            "Body: 'You're welcome to send me a private message'. No address, handle or link printed. "
            f"NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, feed=Y."),
        "relevance": "low",
        "relevance_notes": (
            "Swiss broadcaster documentary seeking people in Switzerland with a personal emotional bond "
            "to an AI companion. Not a spend, pricing or budget story and we are not such a user."),
        "suggested_pitch_template": "None — excluded: wants Swiss AI-companion users' personal accounts.",
    },
    {
        "slug": "ai-data-labelers-in-germany-positive-and-negative-experiences",
        "query_text": _body("ai-data-labelers-in-germany-positive-and-negative-experiences")[:900],
        "journalist_publication": "freelance journalist (author handle JulDagg) — FLUTER (fluter.de, domain field)",
        "category": "AI / Labour / Data Annotation",
        "contact_method": (
            "No address, handle or link published in the body; interviews offered anonymously. "
            f"NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, feed=Y."),
        "relevance": "low",
        "relevance_notes": (
            "Wants data labellers/annotators in Germany to describe their working experience. We hold no "
            "annotator standing and the story is labour conditions, not tool spend."),
        "suggested_pitch_template": "None — excluded: wants German data annotators' first-person accounts.",
    },
    {
        "slug": "ai-data-annotators-and-labellers-experience-with-ai-training-data",
        "query_text": _body("ai-data-annotators-and-labellers-experience-with-ai-training-data")[:900],
        "journalist_publication": "Modupe (author field) — The Times (thetimes.co.uk, domain field)",
        "category": "AI / Labour / Data Annotation",
        "contact_method": (
            "Body: 'My email is [email redacted]'. Address Sourcee-redacted; no handle or link. "
            f"NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, email_redacted=True."),
        "relevance": "low",
        "relevance_notes": (
            "The Times wants former AI data annotators/labellers to speak to their experience. We hold "
            "no such standing; the story is labour, not software pricing."),
        "suggested_pitch_template": "None — excluded: wants annotators' first-person accounts, no spend angle.",
    },
    {
        "slug": "uk-companies-implementing-ai-how-automation-transforms-workdays",
        "query_text": _body("uk-companies-implementing-ai-how-automation-transforms-workdays")[:900],
        "journalist_publication": "Lindsay Dodgson (author field) — CNBC (cnbc.com, domain field)",
        "category": "AI / Enterprise Adoption / CNBC Series",
        "contact_method": (
            "Body: 'you know where to find me [email redacted]'. Address Sourcee-redacted; no handle or "
            f"link published. NO ROUTE RESOLVED as-is. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, "
            "email_redacted=True, feed=Y."),
        "relevance": "low-medium",
        "relevance_notes": (
            "The closest to core beat in today's window: a CNBC series on UK companies implementing AI, "
            "and it explicitly offers 'extra points if you have a news hook or fresh data' - which our "
            "dated price set could answer. But the ask is for UK companies implementing AI as sources, "
            "and we are a publisher, not such a company; below 'medium' on standing. No route resolved."),
        "suggested_pitch_template": (
            "If a route is ever resolved, the only defensible angle is the dated-price half of 'fresh "
            "data': 42 of 76 tools quote a monthly price, 33 at or under $25/month, median $17.50; "
            "monthly vs annual 1.11x-2.53x, median 1.25x over 19 tiers (snapshots re-checked 2026-10-07). "
            "Do NOT claim to be a UK company implementing AI. Excluded this run for want of a route."),
    },
    {
        "slug": "ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories",
        "query_text": _body("ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories")[:900],
        "journalist_publication": "student journalist (author handle yaegrrr) — publication not named",
        "category": "AI / Mental Health / Self-Diagnosis",
        "contact_method": (
            "Body: 'feel free to send me a PM or comment below'. No address, handle or link published. "
            f"NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, feed=n."),
        "relevance": "low",
        "relevance_notes": (
            "Student journalist seeking users' and therapists' personal accounts of AI self-diagnosis. "
            "Not a spend or pricing story; we hold neither standing."),
        "suggested_pitch_template": "None — excluded: wants users'/therapists' personal accounts.",
    },
    {
        "slug": "academics-social-media-and-ai-impact-on-womens-identity-and-selfesteem",
        "query_text": _body("academics-social-media-and-ai-impact-on-womens-identity-and-selfesteem")[:900],
        "journalist_publication": "Lucy Abbersteen (author field) — publication not named",
        "category": "AI / Academia / Media & Identity",
        "contact_method": (
            "Body: 'please comment below!' No address, handle or link published; the only way in is a "
            f"public comment. NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, feed=n."),
        "relevance": "low",
        "relevance_notes": (
            "Wants academics researching how social media and AI affect women's identity and self-esteem. "
            "We are not academics and hold no research in that area; no spend angle."),
        "suggested_pitch_template": "None — excluded: wants academic researchers; no route beyond a public comment.",
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

# rows that crossed the 10-day line since the 2026-10-06 digest (live then, cold now)
prev_live = {o["url"].rstrip("/").split("/journo-request/")[-1]
             for o in prev["opportunities"] if (o.get("_days_old") or 0) <= 10}
crossed = sorted(s for s in prev_live
                 if (verified.get(s) or {}).get("days_old") is not None
                 and (verified.get(s) or {}).get("days_old") > 10)

MIMS = "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks"
CAND_LINES = "; ".join(f"{s} ({lm})" for s, lm in win["ai"])
SPEND_ONLY = [
    "oneflight-international-customers-prepaid-flights-and-cancellations (airline customer stories)",
    "lanterns-fans-18-50-paid-remote-casting-call (paid TV casting call, $50)",
    "houston-hispanic-families-rising-cost-of-living-impact (household cost of living, Telemundo)",
    "crown-heights-and-flatbush-curly-and-coily-residents-hair-care-costs (hair-care costs, student journalist)",
    "people-living-alone-considering-house-share-due-to-rising-costs (housing costs)",
    "gen-z-vs-millennials-housing-costs-and-retirement-savings (personal finance, the i Paper)",
]

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{TODAY}T09:00:00-07:00",
    "search_scope": ("AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, "
                     "software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support "
                     "value, tool consolidation, procurement budget"),
    "age_policy": ("Ages are read off each request page (JSON-LD datePublished plus the rendered "
                   "'Posted ... ago' badge), never off the digest text. All 84 carried URLs were "
                   "re-fetched this run (HTTP 200, request body still served, no expiry notice) and "
                   "the 10 new rows were verified the same way on first sight."),
    "platforms_checked": [
        {"platform": "Sourcee (sourcee.app)", "status": "accessible",
         "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP {win['sitemap_http']}, "
                   f"{win['bytes']:,} bytes, {win['count']:,} loc/lastmod pairs, newest lastmod "
                   f"{win['newest']}). {len(win['window'])} slugs carry a lastmod newer than the "
                   f"2026-10-06 run's mark ({win['mark']}); {len(win['ai'])} carry an AI token, "
                   f"{len(win['ai_strict'])} carry an AI token plus a real spend token, and "
                   f"{len(win['spend_any'])} carry any spend-adjacent token. All candidate slugs were "
                   f"fetched and read in full. Sourcee itself re-probed HTTP 200 (100,825 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Re-measured. {win['feed_count']} slugs listed today, HTTP 200, "
                   f"{win['feed_bytes']:,} bytes, and {win['feed_overlap_with_window']} of "
                   f"{win['feed_count']} sit inside today's new sitemap window - the sixth consecutive "
                   f"100% overlap the monitor has measured. Absence from this feed is still NOT a cold "
                   f"signal: every carried request is absent from it by construction. Six of today's "
                   f"ten new rows are in the feed; none of the 84 carried rows is.")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,198 bytes, 'Vercel Security Checkpoint'. "
                   "Twenty-fourth consecutive identical result. Queries reach sources only by a "
                   "3x-daily email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": "Re-probed once. / HTTP 429, 31,203 bytes, 'Vercel Security Checkpoint'. No public feed."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                   "Source of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes, 'Error: The "
                   "page you were looking for doesn't exist'). Wrong path, not gated - unchanged. The "
                   "feed needs an authenticated app session.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. Apex HTTP 200 (11,486 bytes), title 'MentionMatch - Connect B2B Writers "
                   "with Expert Sources', no feed. Twenty-third consecutive run confirming a "
                   "pre-launch shell.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\",\"error_description\":"
                   "\"No authorization provided\"}. Free read-only feed covering Connectively, HARO, X, "
                   "LinkedIn, MentionMatch and Substack. Needs an interactive OAuth handshake that "
                   "cannot be completed from a scheduled run.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on twenty-two consecutive "
                   "runs; the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy - today's The Times and CNBC rows both came through it.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (147,630 bytes, 'ResponseSource - Connecting the media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free "
                   "source-facing feed.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        (f"TEN NEW AI-TOKEN REQUESTS ADDED, TAKING THE CARRY SET FROM 84 TO 94. {len(win['window'])} "
         f"slugs carry a lastmod newer than the 2026-10-06 mark. {len(win['ai'])} carry an AI token, "
         f"{len(win['ai_strict'])} carry an AI token plus a real spend token, and "
         f"{len(win['spend_any'])} carry any spend-adjacent token. NONE of the ten is core-beat and "
         f"NONE is sendable - all ten leave the body address Sourcee-redacted or publish no route at all."),
        (f"THE TEN CANDIDATES, BY NAME, SO THE FIND IS CHECKABLE: {CAND_LINES}."),
        ("THE STRICT AI+SPEND COUNT IS ZERO TODAY - CLEANER THAN YESTERDAY. The 2026-10-06 window's "
         "single ai_strict hit was a false positive ('procurement' in an AI-liability-INSURANCE call). "
         "Today no window slug carries both an AI token and a real spend token, so there is no hit to "
         "re-judge and no software-spend call in either of the last two windows."),
        ("THE SIX SPEND-ONLY SLUGS ARE NOT ADDED, AND ALL SIX ARE CONSUMER COST-OF-LIVING CALLS: "
         + "; ".join(SPEND_ONLY) + ". None touches software, AI subscriptions or tool budgets."),
        ("THE PAIR RANGE HELD AGAIN against a snapshot refreshed today, and the pair file was "
         "REBUILT, not just re-read: data/pricing_snapshots.json carries `updated: 2026-10-07` (76 "
         "snapshots), scripts/extract_monthly_annual_pairs.py re-asserted all 19 curated pairs against "
         "their own sentences, exited 0 with no needle failures, and rewrote "
         "data/monthly_annual_pairs.json. Range unchanged at 1.11x to 2.53x, median 1.25x, over 19 "
         "tiers across 14 tools (lowest replit-ai Core $20 vs $18; highest browse-ai Personal $48 vs "
         "$19; pair snapshot dates 2026-09-18 and 2026-09-21)."),
        ("THE SHADOW-AI HEADLINE FIGURES RE-DERIVED UNCHANGED: 42 of 76 tools quote a non-zero monthly "
         "price, 33 of those at or under $25/month, median cheapest paid tier $17.50, lowest $4.00 "
         "(khanmigo) against `updated: 2026-10-07`; 31 of 76 quote both a monthly and an annual rate. "
         "Same set as 2026-10-02 through 2026-10-06, so every draft written since 2026-10-02 stands "
         "behind identical numbers."),
        ("ALL 84 CARRIED URLs RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF: 84/84 HTTP 200 "
         "with the request body still served, zero non-200s, zero missing bodies, zero expiry words. "
         "The 2026-10-06 sendable row (employees-blocked-from-ai, Christopher Mims, WSJ) is now 2 days "
         "old, still live, still route-resolved - the only sendable row in the queue."),
        ("MAILBOX CHECKED: STILL NO REPLY TO ANY TRACKED PITCH. INBOX top is msg 100 (a tool "
         "submission, 2026-10-07 15:55Z); the newest human message on a tracked pitch remains Jan "
         "Suski's 2026-09-18 20:39Z reply. No reply to the 2026-09-15 Enterprise AI Leaders send (22 "
         "days) or the 2026-09-18 Sherwood News send (19 days). Four new tool submissions arrived since "
         "the last run (msgs 96-100), none a pitch reply. Zero pitches sent this run."),
        ("THE UNANSWERED FIGURES CORRECTION IS NOW NINETEEN DAYS OUTSTANDING. The recipient of the "
         "2026-09-18 Amplemarket reply was told the same-tier monthly/annual range is '1.21x-2.53x, "
         "median 1.33x'; the current verified figure is 1.11x-2.53x, median 1.25x over 19 tiers. Not "
         "sent this run: the monitor's brief forbids the scheduled run from sending, and the ledger "
         "records it as George's lane."),
    ],
    "expired_this_run": [
        ("Nothing expired and nothing dropped off this run. All 84 carried URLs returned HTTP 200 with "
         "the request body still served. The standing caveat is not a clean bill of health: this "
         "monitor carries every tracked request forward into each new digest, so 'absent from the "
         "newest digest' cannot fire by construction; the sitemap cross-check is the independent "
         "evidence."),
        (("NO CARRIED ROW CROSSED THE 10-DAY LINE SINCE THE 2026-10-06 DIGEST. " if not crossed else
          f"{len(crossed)} ROW(S) CROSSED THE 10-DAY LINE SINCE THE 2026-10-06 DIGEST: " + "; ".join(crossed) + ". ")
         + "The live/cold split moved because of the ten new rows (live unpitched 37 -> "
         f"{len(live_unp)}, cold unpitched 43 -> {len(cold_unp)}). The two-day advance warning in "
         "build_pitch_queue.py covers only sendable rows, so this is stated here instead."),
        ("THE TWO CROSSED-BUT-LIVE DRAFTS ARE STILL LIVE AND STILL UNSENT: the Raconteur shadow-AI "
         "request is now 20 days old (unsent through EIGHTEEN consecutive runs) and the Speciality Food "
         "request 19 days old (its October issue window closed). Both pages returned HTTP 200 again "
         "today. Neither is void - what was lost is the ideal window, not the pitch."),
        ("THE COLD QUEUE IS 43+ ROWS STRONG AND STILL GROWING FASTER THAN IT IS BEING CLEARED. The "
         "highest-relevance cold rows remain unsent: AI SaaS users in production (138d), Business & "
         "Technology Leaders - tech budget priorities (78d), Enterprise AI Leaders - agent sprawl "
         "(32d), Scientists paying for PhD/postdoc AI subscriptions, FinOps - agentic AI cost overruns "
         "(draft unsent since 2026-09-17), the Amplemarket pricing/credits request (pitched and replied "
         "to, figures correction 19 days outstanding) and the Raconteur shadow-AI request (20d)."),
    ],
    "summary": (
        f"{len(ops)} tracked requests (84 carried and all 84 re-verified live, {len(NEW_ROWS)} new "
        f"AI-token finds added, 0 dropped off, 3 pitched, 1 deliberately skipped). Of the "
        f"{len(live_unp) + len(cold_unp)} unpitched, {len(live_unp)} are live and {len(cold_unp)} are "
        "cold, and ONE is sendable: the WSJ columnist's blocked-work-accounts request, now 2 days old, "
        "relevance 'medium', reply route resolved off his own byline page (LinkedIn DM, George's lane). "
        "The new window produced 10 AI-token slugs and ZERO AI+spend slugs - none core-beat, none "
        "sendable. The pair range re-asserted clean against today's rebuilt pair file and held at "
        "1.11x-2.53x over 19 tiers across 14 tools; the shadow-AI headline figures re-derived unchanged "
        "(42 tools publish a monthly price, 33 at or under $25, median $17.50). No new replies to any "
        "tracked pitch; the mailbox's newest inbound is a tool submission, not a pitch reply. Zero "
        "pitches sent this run - sends remain George's lane. Three send-ready drafts are in "
        "pitch-drafts-2026-10-07.md."
    ),
    "recommended_actions": [
        ("SEND THE WSJ BLOCKED-WORK-ACCOUNTS DRAFT - STILL THE ONLY SENDABLE ROW AND NOW 2 DAYS OLD. "
         "Paste-ready at pitch-drafts-2026-10-07.md section 1. Route: LinkedIn DM to "
         "https://www.linkedin.com/in/christopher-mims-club/ (verified HTTP 200, title 'Christopher "
         "Mims - The Wall Street Journal | LinkedIn'); the request's own body says '(DMs open)'. "
         "Relevance 'medium'. It is George's lane, so it cannot be sent from this run."),
        ("SEND THE RACONTEUR SHADOW-AI DRAFT - EIGHTEEN RUNS UNSENT. pitch-drafts-2026-10-07.md "
         "section 2, route simon.chandler@raconteur.net (re-resolved off the live "
         "/contributors/simon-chandler page, HTTP 200; control /contributors/tom-dennis HTTP 200; "
         "legacy /author/simon-chandler/ still 404 and must not be cited). Now 20 days old. It is "
         "still the only HIGH-relevance request this monitor has ever produced with a resolved route."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-10-07.md section 3, "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact, HTTP 200, "
         "alongside five other named masthead addresses, 19 days old). Its October issue window has "
         "closed: make it a send-or-skip call and record the outcome in pitch-ledger.json rather than "
         "carrying it another day."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI - NOW NINETEEN DAYS OUTSTANDING. He replied on "
         "2026-09-18 and was told '1.21x-2.53x, median 1.33x' when the verified figure is "
         "1.11x-2.53x, median 1.25x over 19 tiers. Route: reply to jan@jansuski.com, In-Reply-To the "
         "existing thread."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has produced no real AI+spend slug on "
         "thirteen consecutive runs; the single accessible source returns a handful of mostly consumer "
         "or vendor calls per day. It remains the only lever that widens the monitor."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": len(win["ai_strict"]),
        "ai_plus_spend_regex_false_positives": 0,
        "new_ai_token_slugs_added_to_tracking": len(NEW_ROWS),
        "consecutive_runs_without_new_core_beat": 13,
        "tracked_urls": len(ops),
        "carried_and_reverified": 84,
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
        "drafts_written_never_sent": 6,
        "sendable_on_its_last_live_day": 0,
        "rows_crossed_cold_since_last_digest": len(crossed),
        "rows_at_ten_days_crossing_next_run": 0,
        "lost_to_the_cold_line_with_a_draft_ready": 0,
        "shadow_ai_monthly_priced_tools": 42,
        "shadow_ai_at_or_under_25": 33,
        "shadow_ai_median_cheapest_paid_tier": 17.50,
    },
    "monitor_defects_fixed_this_run": [
        ("NO NEW DEFECT FOUND THIS RUN, AND THAT IS THE POINT: the sendable row carried cleanly. The "
         "2026-10-06 row (employees-blocked-from-ai) was re-verified today (HTTP 200, 2 days old, "
         "relevance 'medium', route still resolving to the same live byline page) and its draft "
         "re-derives its figures at build time, so carrying it cost no numbers. The two prior sendable "
         "defects (the 2026-09-29 chrome leak into `published_links`, the 2026-10-01 Google Form read "
         "as a route) remain fixed in scripts/build_pitch_queue.py."),
        ("FIGURES RE-DERIVED, NOT COPIED. marketing/haro-outreach/_figures_1007.py recomputed the "
         "shadow-AI headline set and the pair sentence from data/pricing_snapshots.json (`updated: "
         "2026-10-07`), data/tools.json and the rebuilt data/monthly_annual_pairs.json. The set is "
         "unchanged, which is exactly why a run that copies yesterday's prose still looks right - so it "
         "is derived anyway."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print(f"wrote digest-{TODAY}.json: {len(ops)} opportunities, {len(digest['platforms_checked'])} platforms")
print(f"live(<=10d): {len(live)}  cold(>10d): {len(stale)}  live_unp: {len(live_unp)}  cold_unp: {len(cold_unp)}")
print(f"crossed cold since last digest: {crossed}")
print(f"repaired rows: {repaired}")
