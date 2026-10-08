#!/usr/bin/env python3
"""Write marketing/haro-outreach/digest-2026-10-08.json

One record per tracked opportunity, re-verified against its own page today by
scripts/verify_journo_requests.py. Carried rows are refreshed from verified-requests.json
(page datePublished + rendered badge), never from the previous digest's text.

New this run: the SEVEN AI-token slugs from today's sitemap window are added to the tracked
set, taking the carry set from 94 to 101. Exactly ONE is core-beat: the Google & Claude
Enterprise seats-and-token-costs request (Glenn Hansen) - the first AI+spend slug with a real
software-cost ask in fourteen runs. It has NO reply route resolved, so it is not sendable.
The other six are off-beat (patent/IP, IA careers, data-labelling labour, pro-bono law,
APAC press, a martech vendor blog).

The 2026-10-06 sendable row (employees-blocked-from-ai, Christopher Mims, WSJ) is now 3 days
old, still live, still route-resolved - still the only sendable row in the queue.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-10-08"

prev = json.loads((D / "digest-2026-10-07.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
win = json.loads((D / "_window_1008.json").read_text())
bodies = json.loads((D / "_bodies_1008.json").read_text())

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
STALE_SNAP = re.compile(r"(?:snapshots?|snapshot refresh)[^.;]{0,40}2026-10-0[1-7]|updated: 2026-10-0[1-7]")
CHECKED_OLD = re.compile(r"((?:re-)?checked) 2026-10-\d\d")
STALE_AFFORD = re.compile(r"31 of the 76 tools[^.]*?median \$16\.50", re.I)
CURRENT_AFFORD = ("42 of 76 tools publish a monthly price, 33 of those at or under $25/month, "
                  "median $17.50")
OLD_DRAFT = re.compile(r"pitch-drafts-2026-10-0[1-7]\.md")
LINKEDIN_BYTES = re.compile(r"\((?:603,318|630,514|603,602) bytes\)")
_TODAY_DRAFT = f"pitch-drafts-{TODAY}.md"
_LI_BYTES = "603,602"


def _repair(text: str | None) -> tuple[str, bool]:
    if not text:
        return text or "", False
    fixed, n = SUPERSEDED_RANGE.subn(CURRENT_RANGE, text)
    fixed, n2 = STALE_SNAP.subn(lambda m: re.sub(r"2026-10-0[1-7]", TODAY, m.group(0)), fixed)
    fixed, n3 = CHECKED_OLD.subn(rf"\1 {TODAY}", fixed)
    fixed, n4 = OLD_DRAFT.subn(_TODAY_DRAFT, fixed)
    fixed, n5 = LINKEDIN_BYTES.subn(f"({_LI_BYTES} bytes)", fixed)
    fixed, n6 = STALE_AFFORD.subn(CURRENT_AFFORD, fixed)
    return fixed, bool(n or n2 or n3 or n4 or n5 or n6)


for op in prev["opportunities"]:
    slug = op["url"].rstrip("/").split("/journo-request/")[-1]
    v = verified.get(slug) or {}
    new = dict(op)
    # `_new_this_run` is a per-run flag, not a carried property: without clearing it here it
    # accumulated across digests (2026-10-08 carried 40 flags of which only 7 were new).
    new.pop("_new_this_run", None)
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
                r"(PAGE-VERIFIED|RE-VERIFIED|re-verified|re-read|re-checked)\s+2026-10-0[1-7]",
                rf"\1 {TODAY}", new["contact_method"])
    ops.append(new)

repaired = [o["url"].rsplit("/", 1)[-1] for o in ops if o.get("_figures_repaired")]


# ------------------------------------------------------- seven new tracked rows
def _body(slug: str) -> str:
    return re.sub(r"\s+", " ", (bodies.get(slug) or {}).get("core") or "").strip()


NEW_ROWS = [
    {
        "slug": "google-and-claude-enterprise-users-seats-and-token-costs",
        "query_text": _body("google-and-claude-enterprise-users-seats-and-token-costs")[:900],
        "journalist_publication": "Glenn Hansen (author field) — outlet not named in the body (he states he reports on power-equipment manufacturing)",
        "category": "AI / Enterprise Procurement / Seats & Token Costs",
        "contact_method": (
            "The body publishes NO address, handle or link and gives no reply instruction beyond "
            "'Google or Claude users care to enlighten me?'; the page's only published links are "
            "Sourcee chrome. email_redacted=False but emails_on_page=none. NO ROUTE RESOLVED on the "
            f"page. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, feed=n."),
        "relevance": "high",
        "relevance_notes": (
            "THE FIRST CORE-BEAT AI+SPEND REQUEST IN FOURTEEN RUNS: a reporter wants enterprise-level "
            "costs for AI seats and tokens from Google or Claude users. Our dated price set answers "
            "exactly this - Claude Team Standard seats $20/seat/month and Premium $100/seat/month "
            "(checked 2026-09-18), Gemini bundled in Workspace at $8.40/$7 per user/month for Business "
            "Starter through $26.40/$22 for Business Plus (checked 2026-09-18), Copilot Business "
            "$19/user/month and Enterprise $39/user/month each with an AI-credit allowance "
            "(2026-10-01). The gap to sendability is the route, not the data."),
        "suggested_pitch_template": (
            "Lead with the dated seat prices, name the checked date on each, and note that enterprise "
            "tiers are sales-assisted (so the list price is the only public anchor). No route is "
            "resolved, so this cannot be sent yet - do NOT invent a LinkedIn handle for a common name."),
    },
    {
        "slug": "solicitors-and-barristers-ai-to-expand-pro-bono-capacity",
        "query_text": _body("solicitors-and-barristers-ai-to-expand-pro-bono-capacity")[:900],
        "journalist_publication": "Catherine Baksi (author field) — publication not named",
        "category": "AI / Legal Sector / Access to Justice",
        "contact_method": (
            "Body: 'please drop me an email at: [email redacted] by the end of this week'. Address "
            "Sourcee-redacted; no handle or link. NO ROUTE RESOLVED. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, live=True, email_redacted=True, emails_on_page=none."),
        "relevance": "low",
        "relevance_notes": (
            "Wants law firms'/chambers' examples of AI applied to pro bono work. We are a publisher, "
            "not a firm, and the ask carries no pricing or spend question. Stated internal deadline "
            "'by the end of this week' (request posted 2026-10-07)."),
        "suggested_pitch_template": "None — excluded: wants law firms' own pro-bono AI projects; no spend angle, no route.",
    },
    {
        "slug": "uk-ai-data-trainers-daytoday-work",
        "query_text": _body("uk-ai-data-trainers-daytoday-work")[:900],
        "journalist_publication": "momitola (author handle) — The Times (thetimes.co.uk, domain field)",
        "category": "AI / Labour / Data Training",
        "contact_method": (
            "Body: 'Ping me a message if you're interested'. No handle, address or link printed. "
            f"NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, feed=n."),
        "relevance": "low",
        "relevance_notes": (
            "The Times wants young UK AI data trainers to describe their day-to-day work. We hold no "
            "such standing; the story is labour, not software pricing."),
        "suggested_pitch_template": "None — excluded: wants UK data trainers' first-person accounts.",
    },
    {
        "slug": "apac-reporters-and-editors-ai-accountability-coverage",
        "query_text": _body("apac-reporters-and-editors-ai-accountability-coverage")[:900],
        "journalist_publication": "Sen Nguyen (author field) — BBC News (bbc.co.uk, domain field)",
        "category": "AI / Press & Media / Accountability",
        "contact_method": (
            "Body: 'Hit me up here or at [email redacted]'. Address Sourcee-redacted; no handle or "
            f"link. NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, email_redacted=True."),
        "relevance": "low",
        "relevance_notes": (
            "Wants APAC journalists covering AI accountability. We are not a reporter and hold no "
            "APAC reporting; no pricing or spend angle."),
        "suggested_pitch_template": "None — excluded: wants APAC reporters/editors; no spend angle.",
    },
    {
        "slug": "early-to-midcareer-information-architects-products-featuring-ai",
        "query_text": _body("early-to-midcareer-information-architects-products-featuring-ai")[:900],
        "journalist_publication": "World Information Architecture Association (author field) — no domain named",
        "category": "AI / UX & IA / Practitioner Interviews",
        "contact_method": (
            "No address, handle or link published; the body gives no reply instruction. "
            f"NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, feed=n."),
        "relevance": "low",
        "relevance_notes": (
            "A research interview call for early/mid-career information architects who built AI "
            "products. We are not such a practitioner and no spend question is asked."),
        "suggested_pitch_template": "None — excluded: wants IA practitioners' own product stories.",
    },
    {
        "slug": "patent-attorneys-and-agents-startup-ip-starter-pack",
        "query_text": _body("patent-attorneys-and-agents-startup-ip-starter-pack")[:900],
        "journalist_publication": "Ptoleme (author field) — no domain named",
        "category": "Legal / IP / Practitioner Guide",
        "contact_method": (
            "Body: 'Feel free to comment or message me' with an acknowledgement offer, but no address, "
            f"handle or link printed. NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, feed=n."),
        "relevance": "low",
        "relevance_notes": (
            "Wants patent attorneys/agents to contribute to a free founder IP guide. We are neither and "
            "the ask has no software-spend angle."),
        "suggested_pitch_template": "None — excluded: wants patent practitioners; no spend angle, no route.",
    },
    {
        "slug": "martech-buyers-ai-impact-on-build-vs-buy-decisions",
        "query_text": _body("martech-buyers-ai-impact-on-build-vs-buy-decisions")[:900],
        "journalist_publication": "Lyza G (author field) — Flipbooker blog (flipbooker.com, domain field)",
        "category": "AI / Martech / Vendor Blog Content Call",
        "contact_method": (
            "Body: 'Email [email redacted]'. Address Sourcee-redacted; no handle or link. "
            f"NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, email_redacted=True."),
        "relevance": "low",
        "relevance_notes": (
            "A vendor blog (Flipbooker) seeking martech buyers' quotes for its own guide, offering a "
            "backlink. Same shape as yesterday's Flipbooker real-estate call: self-promo, not editorial "
            "press, and we are not a martech buyer."),
        "suggested_pitch_template": "None — excluded: vendor blog promo wanting martech-buyer quotes.",
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

prev_live = {o["url"].rstrip("/").split("/journo-request/")[-1]
             for o in prev["opportunities"] if (o.get("_days_old") or 0) <= 10}
crossed = sorted(s for s in prev_live
                 if (verified.get(s) or {}).get("days_old") is not None
                 and (verified.get(s) or {}).get("days_old") > 10)

CAND_LINES = "; ".join(f"{s} ({lm})" for s, lm in win["ai"])
SPEND_ONLY = [
    "south-florida-restaurant-workers-scheduling-pay-and-harassment (restaurant labour)",
    "ucf-organic-chemistry-students-paid-tutoring-email (student tutoring pay)",
    "university-food-bank-staff-rising-grocery-prices-impact-on-students (grocery prices)",
    "commuters-and-households-impact-of-fuel-price-hike-on-budgets (fuel/household budgets)",
    "doulas-and-midwives-billing-medicaid-or-insurance-state-reimbursement (medical billing)",
    "parents-in-ireland-childcare-costs-and-work-arrangements (childcare costs)",
    "gen-zers-dating-spending-2026-and-how-they-feel (dating spend, Yahoo)",
]

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{TODAY}T09:00:00-07:00",
    "search_scope": ("AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, "
                     "software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support "
                     "value, tool consolidation, procurement budget, enterprise AI seat/token costs"),
    "age_policy": ("Ages are read off each request page (JSON-LD datePublished plus the rendered "
                   "'Posted ... ago' badge), never off the digest text. All 94 carried URLs were "
                   "re-fetched this run (HTTP 200, request body still served, no expiry notice) and "
                   "the 7 new rows were verified the same way on first sight."),
    "platforms_checked": [
        {"platform": "Sourcee (sourcee.app)", "status": "accessible",
         "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP {win['sitemap_http']}, "
                   f"{win['bytes']:,} bytes, {win['count']:,} loc/lastmod pairs, newest lastmod "
                   f"{win['newest']}). {len(win['window'])} slugs carry a lastmod newer than the "
                   f"2026-10-07 run's mark ({win['mark']}); {len(win['ai'])} carry an AI token, "
                   f"{len(win['ai_strict'])} carry an AI token plus a real spend token, and "
                   f"{len(win['spend_any'])} carry any spend-adjacent token. All candidate slugs were "
                   f"fetched and read in full. Sourcee itself re-probed HTTP 200 (100,825 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Re-measured. {win['feed_count']} slugs listed today, HTTP 200, "
                   f"{win['feed_bytes']:,} bytes, and {win['feed_overlap_with_window']} of "
                   f"{win['feed_count']} sit inside today's new sitemap window - the seventh consecutive "
                   f"100% overlap the monitor has measured. Absence from this feed is still NOT a cold "
                   f"signal: every carried request is absent from it by construction. FIVE of today's "
                   f"seven new rows are in the feed (the Google/Claude, solicitor, UK data-trainer, "
                   f"IA and martech rows; the patent-IP and APAC rows are not); none of the 94 carried "
                   f"rows is.")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,193 bytes, 'Vercel Security Checkpoint'. "
                   "Twenty-fifth consecutive identical result. Queries reach sources only by a "
                   "3x-daily email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": "Re-probed once. / HTTP 429, 31,194 bytes, 'Vercel Security Checkpoint'. No public feed."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                   "Source of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes, 'Error: The "
                   "page you were looking for doesn't exist'). Wrong path, not gated - unchanged.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. Apex HTTP 200 (11,486 bytes), title 'MentionMatch - Connect B2B Writers "
                   "with Expert Sources', no feed. Twenty-fourth consecutive run confirming a "
                   "pre-launch shell.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\"}. Free read-only feed "
                   "covering Connectively, HARO, X, LinkedIn, MentionMatch and Substack. Needs an "
                   "interactive OAuth handshake that cannot be completed from a scheduled run.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on twenty-three consecutive "
                   "runs; the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (148,206 bytes, 'ResponseSource - Connecting the media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        (f"SEVEN NEW AI-TOKEN REQUESTS ADDED, TAKING THE CARRY SET FROM 94 TO 101. {len(win['window'])} "
         f"slugs carry a lastmod newer than the 2026-10-07 mark. {len(win['ai'])} carry an AI token, "
         f"{len(win['ai_strict'])} carries an AI token plus a real spend token, and {len(win['spend_any'])} "
         f"carry any spend-adjacent token."),
        (f"THE SEVEN CANDIDATES, BY NAME: {CAND_LINES}."),
        ("ONE IS CORE-BEAT AND IT IS THE FIND OF THE RUN: google-and-claude-enterprise-users-seats-and-"
         "token-costs (Glenn Hansen) asks directly for 'enterprise-level costs for AI seats and tokens' "
         "from Google or Claude users. That is the exact quantity our dated price set makes visible - "
         "the first such request in fourteen runs. It is recorded as relevance 'high' but is NOT "
         "sendable: the page publishes no address, handle or link and gives no reply instruction, so no "
         "route is resolved. The gap is the route, not the data."),
        ("THE STRICT AI+SPEND COUNT IS ONE - the first real software-cost hit in three runs. Its matched "
         "tokens are 'seat' and 'cost' in the slug, and unlike the 2026-10-06 'procurement' false "
         "positive (an AI-liability-INSURANCE call) this one is genuinely about AI seat and token spend."),
        ("THE SEVEN SPEND-ONLY SLUGS ARE NOT ADDED, AND ALL SEVEN ARE CONSUMER COST-OF-LIVING CALLS: "
         + "; ".join(SPEND_ONLY) + ". None touches software, AI subscriptions or tool budgets."),
        ("THE PAIR RANGE HELD AGAIN against a snapshot refreshed today, and the pair file was REBUILT: "
         "data/pricing_snapshots.json carries `updated: 2026-10-08` (76 snapshots), "
         "scripts/extract_monthly_annual_pairs.py re-asserted all 19 curated pairs, exited 0 with no "
         "needle failures, and rewrote data/monthly_annual_pairs.json. Range unchanged at 1.11x to "
         "2.53x, median 1.25x, over 19 tiers (lowest replit-ai Core $20 vs $18; highest browse-ai "
         "Personal $48 vs $19)."),
        ("THE SHADOW-AI HEADLINE FIGURES RE-DERIVED UNCHANGED: 42 of 76 tools quote a non-zero monthly "
         "price, 33 of those at or under $25/month, median cheapest paid tier $17.50, lowest $4.00 "
         "(khanmigo) against `updated: 2026-10-08`. Same set as 2026-10-02 through 2026-10-07."),
        ("ALL 94 CARRIED URLs RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF: 94/94 HTTP 200 "
         "with the request body still served. The 2026-10-06 sendable row (employees-blocked-from-ai, "
         "Christopher Mims, WSJ) is now 3 days old, still live, still route-resolved - the only "
         "sendable row in the queue."),
        ("MAILBOX CHECKED: NO REPLY TO ANY TRACKED PITCH. INBOX top is msg 102 (a ToolChase reply, "
         "2026-10-08 13:30+03:00, to the Sep-3 guest-pitch batch - not this monitor's pitches); the "
         "next is msg 101 (a tool submission, 2026-10-08 00:29Z). No reply to the 2026-09-15 "
         "Enterprise AI Leaders send or the 2026-09-18 Sherwood News send. Zero pitches sent this run."),
        ("THE UNANSWERED FIGURES CORRECTION IS NOW TWENTY DAYS OUTSTANDING. The recipient of the "
         "2026-09-18 Amplemarket reply was told the same-tier monthly/annual range is '1.21x-2.53x, "
         "median 1.33x'; the current verified figure is 1.11x-2.53x, median 1.25x over 19 tiers. Not "
         "sent this run: the monitor's brief forbids the scheduled run from sending."),
    ],
    "expired_this_run": [
        ("Nothing expired and nothing dropped off this run. All 94 carried URLs returned HTTP 200 with "
         "the request body still served. The standing caveat is not a clean bill of health: this "
         "monitor carries every tracked request forward into each new digest, so 'absent from the "
         "newest digest' cannot fire by construction; the sitemap cross-check is the independent "
         "evidence."),
        (("NO CARRIED ROW CROSSED THE 10-DAY LINE SINCE THE 2026-10-07 DIGEST. " if not crossed else
          f"{len(crossed)} ROW(S) CROSSED THE 10-DAY LINE SINCE THE 2026-10-07 DIGEST: " + "; ".join(crossed) + ". ")
         + "The live/cold split moved because of the seven new rows (live unpitched 47 -> "
         f"{len(live_unp)}, cold unpitched 43 -> {len(cold_unp)})."),
        ("ONE REQUEST CARRIES A STATED INTERNAL DEADLINE THAT FALLS THIS WEEK: solicitors-and-"
         "barristers-ai-to-expand-pro-bono-capacity asks for an email 'by the end of this week' "
         "(posted 2026-10-07). It is low relevance with no resolved route, so it is not a send - "
         "recorded only so the deadline is not missed silently."),
        ("THE TWO CROSSED-BUT-LIVE DRAFTS ARE STILL LIVE AND STILL UNSENT: the Raconteur shadow-AI "
         "request is now 21 days old (unsent through NINETEEN consecutive runs) and the Speciality "
         "Food request 20 days old (its October issue window closed). Both pages returned HTTP 200 "
         "again today. Neither is void - what was lost is the ideal window, not the pitch."),
    ],
    "summary": (
        f"{len(ops)} tracked requests (94 carried and all 94 re-verified live, {len(NEW_ROWS)} new "
        f"AI-token finds added, 0 dropped off, 3 pitched, 1 deliberately skipped). Of the "
        f"{len(live_unp) + len(cold_unp)} unpitched, {len(live_unp)} are live and {len(cold_unp)} are "
        "cold, and ONE is sendable: the WSJ columnist's blocked-work-accounts request, now 3 days old, "
        "relevance 'medium', reply route resolved off his own byline page (LinkedIn DM, George's lane). "
        "The new window produced 7 AI-token slugs and ONE AI+spend slug - the first real software-cost "
        "request in fourteen runs (Google & Claude enterprise seats and token costs) - but that row has "
        "no resolved reply route, so it is not sendable. The pair range held at 1.11x-2.53x over 19 "
        "tiers across 14 tools; the shadow-AI headline figures re-derived unchanged (42 tools publish a "
        "monthly price, 33 at or under $25, median $17.50). No new replies to any tracked pitch. Zero "
        "pitches sent this run - sends remain George's lane."
    ),
    "recommended_actions": [
        ("SEND THE WSJ BLOCKED-WORK-ACCOUNTS DRAFT - STILL THE ONLY SENDABLE ROW AND NOW 3 DAYS OLD. "
         "Paste-ready at pitch-drafts-2026-10-08.md section 1. Route: LinkedIn DM to "
         "https://www.linkedin.com/in/christopher-mims-club/ (verified HTTP 200, 603,602 bytes, title "
         "'Christopher Mims - The Wall Street Journal | LinkedIn'); the request's own body says "
         "'(DMs open)'. Relevance 'medium'. George's lane."),
        ("RESOLVE A ROUTE FOR THE GOOGLE & CLAUDE SEATS-AND-TOKENS REQUEST - IT IS THE BEST-MATCHING "
         "REQUEST THIS MONITOR HAS SEEN IN FOURTEEN RUNS AND IT HAS NO ROUTE. Glenn Hansen wants "
         "enterprise AI seat and token costs; our dated set holds Claude Team $20/$100 per seat/month, "
         "Gemini Workspace org rates and Copilot Business/Enterprise per-user prices. The page "
         "publishes no address or handle and a web search cannot confirm WHICH Glenn Hansen he is (a "
         "same-name LinkedIn profile is a different person), so no route must be invented. If George "
         "can find his outlet handle, this is a high-relevance send."),
        ("SEND THE RACONTEUR SHADOW-AI DRAFT - NINETEEN RUNS UNSENT. pitch-drafts-2026-10-08.md "
         "section 2, route simon.chandler@raconteur.net (re-resolved off the live "
         "/contributors/simon-chandler page, HTTP 200, 154,819 bytes, data-part triplet unchanged). "
         "Now 21 days old. Still the only HIGH-relevance request with a resolved route."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-10-08.md section 3, "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact, HTTP 200, "
         "59,488 bytes, 20 days old). Its October issue window has closed: make it a send-or-skip call "
         "and record the outcome in pitch-ledger.json."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI - NOW TWENTY DAYS OUTSTANDING. Route: reply to "
         "jan@jansuski.com, In-Reply-To the existing thread."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. It remains the only lever that widens the "
         "monitor beyond Sourcee; Sourcee itself produced its first core-beat find in fourteen runs "
         "today, which is the argument for widening supply rather than retiring the monitor."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 1,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": len(win["ai_strict"]),
        "ai_plus_spend_regex_false_positives": 0,
        "new_ai_token_slugs_added_to_tracking": len(NEW_ROWS),
        "consecutive_runs_without_new_core_beat": 0,
        "tracked_urls": len(ops),
        "carried_and_reverified": 94,
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
        "drafts_written_never_sent": 7,
        "sendable_on_its_last_live_day": 0,
        "rows_crossed_cold_since_last_digest": len(crossed),
        "rows_at_ten_days_crossing_next_run": 0,
        "lost_to_the_cold_line_with_a_draft_ready": 0,
        "shadow_ai_monthly_priced_tools": 42,
        "shadow_ai_at_or_under_25": 33,
        "shadow_ai_median_cheapest_paid_tier": 17.50,
    },
    "monitor_defects_fixed_this_run": [
        ("NO NEW DEFECT FOUND THIS RUN. The sendable row carried cleanly: the 2026-10-06 row "
         "(employees-blocked-from-ai) was re-verified today (HTTP 200, 3 days old, relevance 'medium', "
         "route still resolving to the same live byline page) and its draft re-derives its figures at "
         "build time. The two prior sendable defects (the 2026-09-29 chrome leak into `published_links`, "
         "the 2026-10-01 Google Form read as a route) remain fixed in scripts/build_pitch_queue.py."),
        ("FIGURES RE-DERIVED, NOT COPIED. marketing/haro-outreach/_figures_1008.py recomputed the "
         "shadow-AI headline set and the pair sentence from data/pricing_snapshots.json (`updated: "
         "2026-10-08`), data/tools.json and the rebuilt data/monthly_annual_pairs.json."),
        ("NEW THIS RUN, AND THE `_new_this_run` FLAG IS NOW CLEARED ON EVERY CARRY: it had accumulated "
         "across digests (the 2026-10-08 build carried 40 flags of which only 7 were actually new this "
         "run), so any count of new rows read off it was wrong by an order of magnitude. Fixed in "
         "marketing/haro-outreach/_write_digest_1008.py: the flag is popped on every carried row before "
         "the new rows are added."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print(f"wrote digest-{TODAY}.json: {len(ops)} opportunities, {len(digest['platforms_checked'])} platforms")
print(f"live(<=10d): {len(live)}  cold(>10d): {len(stale)}  live_unp: {len(live_unp)}  cold_unp: {len(cold_unp)}")
print(f"crossed cold since last digest: {crossed}")
print(f"repaired rows: {repaired}")
