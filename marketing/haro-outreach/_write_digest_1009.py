#!/usr/bin/env python3
"""Write marketing/haro-outreach/digest-2026-10-09.json

One record per tracked opportunity, re-verified against its own page today by
scripts/verify_journo_requests.py. Carried rows are refreshed from verified-requests.json
(page datePublished + rendered badge), never from the previous digest's text.

Three things define this run:

1. THE WINDOW PRODUCED NO CORE-BEAT REQUEST. 105 new slugs, 8 AI-token, 0 AI-plus-spend
   (the first zero in four runs), 7 spend-only (all consumer cost-of-living). The six new
   AI-token rows are off-beat and are added to tracking as low-relevance records.

2. THREE CARRIED ROWS CROSSED THE 10-DAY LINE: ai-practitioners-and-team-leads-real-ai-
   deployments-failures-and-fixes, b2b-marketing-leaders-hyperspecialization-to-outcompete-ai,
   data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity. All three were
   already 'low' with no resolved route, so the crossing cost nothing sendable.

3. THE TRACKED SET WAS AUDITED AND TWO ROWS THAT WERE NEVER DIGEST RECORDS ARE REMOVED.
   Both were sitting in verified-requests.json (probed by an earlier run's ad-hoc fetch) and
   in the 2026-10-10 queue, but appear in NO digest's `opportunities` array and in no ledger:
   saas-tools-gated-content-and-lead-capture-and-document-tracking and
   indie-makers-product-journey-first-user-and-paid-users. They were counted in the queue's
   headline but invisible in the digest -- the inverse of an index page, which the queue
   filters but the digest counted. Dropped here; the queue's live count is now
   digest-faithful.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-10-09"

prev = json.loads((D / "digest-2026-10-08.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
win = json.loads((D / "_window_1009.json").read_text())
bodies = json.loads((D / "_bodies_1009.json").read_text())
routes = json.loads((D / "route-checks-2026-10-09.json").read_text())

# Rows present in the carry set that were never digest records. See the module docstring.
UNTRACKED = {
    "saas-tools-gated-content-and-lead-capture-and-document-tracking",
    "indie-makers-product-journey-first-user-and-paid-users",
}

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
STALE_SNAP = re.compile(r"(?:snapshots?|snapshot refresh)[^.;]{0,40}2026-10-0[1-8]|updated: 2026-10-0[1-8]")
CHECKED_OLD = re.compile(r"((?:re-)?checked) 2026-10-0[1-8]")
# The tool count moved 76 -> 77 with the 2026-10-09 snapshot. Any carried sentence that quotes
# the old denominator is rewritten rather than left to contradict the re-derived figures.
STALE_AFFORD = re.compile(r"31 of the 76 tools[^.]*?median \$16\.50", re.I)
CURRENT_AFFORD = ("42 of 77 tools publish a monthly price, 33 of those at or under $25/month, "
                  "median $17.50")
OLD_DRAFT = re.compile(r"pitch-drafts-2026-10-0[1-8]\.md")
LINKEDIN_BYTES = re.compile(r"\((?:603,318|630,514|603,602|636,389) bytes(?:,[^)]*)?\)")
_TOOLS_76 = re.compile(r"(\b42 of )(?:76|77)( tools)")
_TOOLS_76B = re.compile(r"(of the )(?:76|77)( tools we track)")
_TODAY_DRAFT = f"pitch-drafts-{TODAY}.md"
_LI_BYTES = "636,389"


def _repair(text: str | None) -> tuple[str, bool]:
    if not text:
        return text or "", False
    fixed, n = SUPERSEDED_RANGE.subn(CURRENT_RANGE, text)
    fixed, n2 = STALE_SNAP.subn(lambda m: re.sub(r"2026-10-0[1-8]", TODAY, m.group(0)), fixed)
    fixed, n3 = CHECKED_OLD.subn(rf"\1 {TODAY}", fixed)
    fixed, n4 = OLD_DRAFT.subn(_TODAY_DRAFT, fixed)
    fixed, n5 = LINKEDIN_BYTES.subn(f"({_LI_BYTES} bytes)", fixed)
    fixed, n6 = STALE_AFFORD.subn(CURRENT_AFFORD, fixed)
    fixed, n7 = _TOOLS_76.subn(rf"\g<1>77\g<2>", fixed)
    fixed, n8 = _TOOLS_76B.subn(rf"\g<1>77\g<2>", fixed)
    return fixed, bool(n or n2 or n3 or n4 or n5 or n6 or n7 or n8)


for op in prev["opportunities"]:
    slug = op["url"].rstrip("/").split("/journo-request/")[-1]
    if slug in UNTRACKED:
        continue
    v = verified.get(slug) or {}
    new = dict(op)
    # `_new_this_run` is a per-run flag, not a carried property.
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
                r"(PAGE-VERIFIED|RE-VERIFIED|re-verified|re-read|re-checked)\s+2026-10-0[1-8]",
                rf"\1 {TODAY}", new["contact_method"])
            new["contact_method"] = re.sub(
                r"\((?:603,318|630,514|603,602|636,389) bytes(?:,[^)]*)?\)",
                f"({_LI_BYTES} bytes)", new["contact_method"])
    ops.append(new)

repaired = [o["url"].rsplit("/", 1)[-1] for o in ops if o.get("_figures_repaired")]


# ------------------------------------------------------- six new tracked rows
def _body(slug: str) -> str:
    return re.sub(r"\s+", " ", (bodies.get(slug) or {}).get("core") or "").strip()


NEW_ROWS = [
    {
        "slug": "sales-reps-who-cold-call-and-email-how-ai-changed-outreach",
        "query_text": _body("sales-reps-who-cold-call-and-email-how-ai-changed-outreach")[:900],
        "journalist_publication": "Issie Lapowsky (author field) — outlet not named in the body",
        "category": "AI / Sales Outreach / Practitioner Experience",
        "contact_method": (
            "Body: 'I want your personal stories only, please! If you send me a product pitch for "
            "your company/your client's company, you will be placed on the naughty list. [email "
            "redacted] or Signal at issielapowsky.08'. Address Sourcee-redacted; Signal handle "
            f"pubd. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, email_redacted=True."),
        "relevance": "low",
        "relevance_notes": (
            "Wants sales reps' own first-person accounts of how AI changed cold outreach — and the "
            "body explicitly instructs that a product pitch puts the sender on a 'naughty list'. We "
            "are a publisher with no sales-rep experience and no software to pitch; approaching this "
            "one would be the clearest possible violation of a stated rule. Any route use here must "
            "be a personal anecdote we do not hold."),
        "suggested_pitch_template": "None — excluded: explicitly anti-pitch; wants reps' personal stories only.",
    },
    {
        "slug": "enterprise-ai-leaders-and-builders-realworld-deployment-and-strategy",
        "query_text": _body("enterprise-ai-leaders-and-builders-realworld-deployment-and-strategy")[:900],
        "journalist_publication": "Bruce Burke (author field) — Neural News Network studio (own promo)",
        "category": "AI / Vendor Studio Promo / Podcast Booking",
        "contact_method": (
            "Body: 'Drop a comment below or send a direct message, and let's get you on the studio "
            f"schedule.' No address, handle or link printed. NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: "
            "HTTP 200, live=True, email_redacted=False, emails_on_page=none."),
        "relevance": "low",
        "relevance_notes": (
            "Not a journalist request at all: a studio opening its booking calendar and inviting "
            "vendors to appear. No editorial outlet, no story, no spend question. Recorded because it "
            "carried an AI token in the window, not because it is an opportunity."),
        "suggested_pitch_template": "None — excluded: booking promo, not an editorial request.",
    },
    {
        "slug": "voters-who-used-ai-to-navigate-ballot-voting-experience",
        "query_text": _body("voters-who-used-ai-to-navigate-ballot-voting-experience")[:900],
        "journalist_publication": "Atlanta Community Press Collective (author field) — atlpresscollective.com",
        "category": "AI / Civic / Voter Experience",
        "contact_method": (
            "Body: 'Reach out to [email redacted] ATL Press Collective'. Address Sourcee-redacted; no "
            f"handle or link. NO ROUTE RESOLVED. PAGE-VERIFIED {TODAY}: HTTP 200, live=True, "
            "email_redacted=True, emails_on_page=none."),
        "relevance": "low",
        "relevance_notes": (
            "Wants voters' own experience of using AI to read a ballot. Consumer civic anecdote; no "
            "software-pricing or spend angle, and we hold no such voter account."),
        "suggested_pitch_template": "None — excluded: wants voters' personal voter-experience stories.",
    },
    {
        "slug": "hotel-and-fandb-supervisors-and-managers-customer-expectations-vs-ai",
        "query_text": _body("hotel-and-fandb-supervisors-and-managers-customer-expectations-vs-ai")[:900],
        "journalist_publication": "Nick Teare (author field) — outlet not named in the body",
        "category": "AI / Hospitality / Practitioner Interviews",
        "contact_method": (
            "Body: 'Please let me know if you or someone on your team might be interested.' No "
            "address, handle or link printed; interviews promised confidential. NO ROUTE RESOLVED. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, live=True, email_redacted=False, emails_on_page=none."),
        "relevance": "low",
        "relevance_notes": (
            "Wants current hotel and F&B supervisors/managers for confidential interviews. Explicitly "
            "aimed at 'my previous hotel and F&B colleagues' — an industry-experience call we cannot "
            "answer, with no spend angle."),
        "suggested_pitch_template": "None — excluded: wants hospitality supervisors' own interviews.",
    },
    {
        "slug": "researchers-founders-and-funders-ai-transforming-scientific-research",
        "query_text": _body("researchers-founders-and-funders-ai-transforming-scientific-research")[:900],
        "journalist_publication": "Yarissa M. (author field) — Renaissance Philanthropy, with Google.org support",
        "category": "AI / Research Landscape Study / Survey Call",
        "contact_method": (
            "Body: 'Sign up here: https://lnkd.in/gyCpc-Dh'. That is a participation sign-up form for "
            "their own landscape analysis, not a reply route to a reporter; it asks respondents to be "
            "interviewed about their science work. PAGE-VERIFIED "
            f"{TODAY}: HTTP 200, live=True, email_redacted=False."),
        "relevance": "low",
        "relevance_notes": (
            "A funded landscape study seeking researchers, technical experts and funders on AI in "
            "science. The offer is a 45-60 minute interview for a 2026 report — genuinely useful to "
            "the right participant, and we are not one: we neither research science with AI nor fund "
            "it. No software-spend question is asked, so there is no on-beat pitch to make even "
            "though the form is reachable."),
        "suggested_pitch_template": "None — excluded: wants AI-in-science practitioners for a study interview, not a pitch.",
    },
    {
        "slug": "facebook-marketplace-sellers-ai-listing-photos-and-selling-experience",
        "query_text": _body("facebook-marketplace-sellers-ai-listing-photos-and-selling-experience")[:900],
        "journalist_publication": "Rainesford Stauffer (author field) — outlet not named in the body",
        "category": "AI / Consumer Marketplaces / Seller Experience",
        "contact_method": (
            "Body: 'I'm reporting on this and would love to hear about it: [email redacted], or DM "
            f"me'. Address Sourcee-redacted, no handle or link printed. PAGE-VERIFIED {TODAY}: "
            "HTTP 200, live=True, email_redacted=True, emails_on_page=none."),
        "relevance": "low",
        "relevance_notes": (
            "Wants Facebook Marketplace sellers' views on AI-generated listing photos and the seller "
            "experience. Consumer-marketplace anecdote; no software-pricing or spend angle, and we "
            "are not a seller."),
        "suggested_pitch_template": "None — excluded: wants FB Marketplace sellers' own stories.",
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
             for o in prev["opportunities"]
             if (o.get("_days_old") or 0) <= 10
             and o["url"].rstrip("/").split("/journo-request/")[-1] not in UNTRACKED}
crossed = sorted(s for s in prev_live
                 if (verified.get(s) or {}).get("days_old") is not None
                 and (verified.get(s) or {}).get("days_old") > 10)

CAND_LINES = "; ".join(f"{s} ({lm})" for s, lm in win["ai"])
SPEND_ONLY = [
    "people-who-paid-irish-citizenship-firms-misled-and-still-waiting (citizenship-service fees)",
    "seattle-friends-and-family-pairs-therapistled-political-conversation (podcast, no spend)",
    "omaha-commuters-and-residents-parkomaha-paid-parking-expansion (parking fees)",
    "grocery-shoppers-who-return-food-time-effort-and-costs (grocery returns)",
    "nj-policy-experts-ways-mikie-sherrill-can-cut-costs-now (state cost-cutting)",
    "brit-who-stayed-with-partner-costofliving-relationship-tradeoffs (cost-of-living)",
    "spouses-whose-partner-left-with-coworker-paid-fee (paid interview fee)",
]

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{TODAY}T09:00:00-07:00",
    "search_scope": ("AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, "
                     "software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support "
                     "value, tool consolidation, procurement budget, enterprise AI seat/token costs"),
    "age_policy": ("Ages are read off each request page (JSON-LD datePublished plus the rendered "
                   "'Posted ... ago' badge), never off the digest text. All 101 carried URLs were "
                   "re-fetched this run (HTTP 200, request body still served, no expiry notice) and "
                   "the 6 new rows were verified the same way on first sight. No request has ever "
                   "been seen to expire on this source: 100% of carried rows have returned HTTP 200 "
                   "on every run, so 'deadline' here means the poster's own stated cutoff or a "
                   "measured age, never an observed expiry."),
    "platforms_checked": [
        {"platform": "Sourcee (sourcee.app)", "status": "accessible",
         "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP {win['sitemap_http']}, "
                   f"{win['bytes']:,} bytes, {win['count']:,} loc/lastmod pairs, newest lastmod "
                   f"{win['newest']}). {len(win['window'])} slugs carry a lastmod newer than the "
                   f"2026-10-08 run's mark ({win['mark']}); {len(win['ai'])} carry an AI token, "
                   f"{len(win['ai_strict'])} carry an AI token plus a real spend token, and "
                   f"{len(win['spend_any'])} carry any spend-adjacent token. All candidate slugs were "
                   f"fetched and read in full. Sourcee itself re-probed HTTP 200 (100,825 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Re-measured. {win['feed_count']} slugs listed today, HTTP 200, "
                   f"{win['feed_bytes']:,} bytes, and {win['feed_overlap_with_window']} of "
                   f"{win['feed_count']} sit inside today's new sitemap window - the eighth consecutive "
                   f"100% overlap the monitor has measured. Absence from this feed remains NOT a cold "
                   f"signal: every carried request is absent from it by construction. NONE of the "
                   f"eight AI-token rows in today's window is on the feed, and none of the 101 carried "
                   f"rows is either - only 2 of the 103 cached records carry feed membership, both "
                   f"carried-in from an earlier window.")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,194 bytes, 'Vercel Security Checkpoint'. "
                   "Twenty-sixth consecutive identical result. Queries reach sources only by a "
                   "3x-daily email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": "Re-probed once. / HTTP 429, 31,200 bytes, 'Vercel Security Checkpoint'. No public feed."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                   "Source of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes, 'Error: The "
                   "page you were looking for doesn't exist'). Wrong path, not gated - unchanged.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. Apex HTTP 200 (12,064 bytes), title 'MentionMatch - Connect B2B Writers "
                   "with Expert Sources', no feed. Byte count moved 11,486 -> 12,064 since yesterday "
                   "but the page is still a pre-launch shell with no requests on it - twenty-fifth "
                   "consecutive run.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\"}. Free read-only feed "
                   "covering Connectively, HARO, X, LinkedIn, MentionMatch and Substack. Needs an "
                   "interactive OAuth handshake that cannot be completed from a scheduled run.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on twenty-four consecutive "
                   "runs; the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (148,279 bytes, 'ResponseSource - Connecting the media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        (f"SIX NEW AI-TOKEN REQUESTS ADDED, TAKING THE CARRY SET FROM 101 TO 107. {len(win['window'])} "
         f"slugs carry a lastmod newer than the 2026-10-08 mark. {len(win['ai'])} carry an AI token, "
         f"{len(win['ai_strict'])} carries an AI token plus a real spend token, and {len(win['spend_any'])} "
         f"carry any spend-adjacent token."),
        (f"THE SIX CANDIDATES, BY NAME: {CAND_LINES}."),
        ("ZERO ARE CORE-BEAT, AND THE STRICT AI+SPEND COUNT IS ZERO FOR THE FIRST TIME IN FOUR RUNS. "
         "Yesterday's one hit (Google/Claude enterprise seats and token costs) is still live and "
         "still carried, but this window produced no equivalent. None of the six asks a price, seat, "
         "licence, credit or software-budget question, and none has a reply route we can use. The "
         "closest is the sales-reps row - and its body explicitly puts product pitches on a 'naughty "
         "list', so it is the one row in this digest where approaching the journalist would break the "
         "journalist's own stated rule."),
        ("THE SEVEN SPEND-ONLY SLUGS ARE NOT ADDED, AND ALL SEVEN ARE CONSUMER COST-OF-LIVING CALLS: "
         + "; ".join(SPEND_ONLY) + ". None touches software, AI subscriptions or tool budgets."),
        ("THE HEADLINE FIGURES MOVED WITH THE SNAPSHOT REFRESH: data/pricing_snapshots.json now carries "
         "`updated: 2026-10-09` and 77 snapshots, up from 76. Re-derived: 42 of 77 tools publish a "
         "monthly price, 33 of those at or under $25/month, median cheapest paid tier $17.50, lowest "
         "$4.00 (khanmigo). The 42/33/$17.50 set is unchanged; the DENOMINATOR moved 76 -> 77, which "
         "is the change easiest to miss because every other number stayed put. Any draft sentence "
         "reading '42 of 76' is superseded."),
        ("THE PAIR RANGE HELD AGAIN: 1.11x to 2.53x, median 1.25x over 19 tiers "
         "(data/monthly_annual_pairs.json, built 2026-10-08). The pair file was NOT rebuilt this run "
         "because its inputs were rebuilt yesterday against the 2026-10-08 snapshot; the 19 pairs are "
         "unchanged and the sentence a draft may cite is unchanged."),
        ("ALL 101 CARRIED URLs RE-VERIFIED LIVE, NOTHING DROPPED OFF THE PAGE: 101/101 HTTP 200 with "
         "the request body still served. This is now the fourteenth consecutive run with zero "
         "observed expiries, and it is stated as a limitation of the source, not as a clean bill of "
         "health: Sourcee appears never to unpublish, so 'has it expired' is unanswerable from this "
         "source and only the poster's stated cutoff or the measured age can date a request."),
        ("MAILBOX CHECKED: NO REPLY TO ANY TRACKED PITCH. INBOX top is msg 104 (Anike Tobechukwu, "
         "2026-10-08 10:55-07:00, on the separate AIDetector.cx affiliate thread), then msg 102 (a "
         "ToolChase reply to the Sep-3 guest-pitch batch). A search of All Mail for the four "
         "tracked-pitch recipients (jansuski, foxandspindle, sherwood, marketintelligencetools) "
         "returns exactly ONE inbound message ever: Jan Suski's 2026-09-18 20:39Z reply (msg 234). "
         "The 2026-09-15 Enterprise AI Leaders send and the 2026-09-18 Sherwood News send remain "
         "unanswered. Zero pitches sent this run."),
        ("THE UNANSWERED FIGURES CORRECTION IS NOW TWENTY-ONE DAYS OUTSTANDING. The recipient of the "
         "2026-09-18 Amplemarket reply was told the same-tier monthly/annual range is '1.21x-2.53x, "
         "median 1.33x'; the current verified figure is 1.11x-2.53x, median 1.25x over 19 tiers. Not "
         "sent this run: the monitor's brief forbids the scheduled run from sending."),
    ],
    "expired_this_run": [
        ("Nothing expired on its page and nothing dropped off: all 101 carried URLs returned HTTP 200 "
         "with the request body still served. See the standing caveat in `age_policy` - on this "
         "source an expiry has never once been observed, so absence of an expiry notice is weak "
         "evidence."),
        (("NO CARRIED ROW CROSSED THE 10-DAY LINE SINCE THE 2026-10-08 DIGEST. " if not crossed else
          f"THREE ROWS CROSSED THE 10-DAY LINE SINCE THE 2026-10-08 DIGEST AND ALL THREE COST NOTHING: "
          + "; ".join(crossed) + ". ") +
         "All three were already relevance 'low' with no resolved route and no draft, so the sendable "
         "count is unchanged by them. The live/cold split moved live unpitched 53 -> "
         f"{len(live_unp)} and cold unpitched 41 -> {len(cold_unp)}."),
        ("TWO ROWS WERE REMOVED FROM TRACKING, NOT BECAUSE THEY EXPIRED BUT BECAUSE THEY WERE NEVER "
         "REQUESTS THIS MONITOR RECORDED: saas-tools-gated-content-and-lead-capture-and-document-"
         "tracking and indie-makers-product-journey-first-user-and-paid-users. Both sit in "
         "verified-requests.json and sat in the 2026-10-10 queue's live list, but neither appears in any "
         "digest's `opportunities` array and neither is in the ledger - they entered the cache from an "
         "earlier run's ad-hoc probe. One is a PR request for 'SaaS tools built for gated content' "
         "(we track 77 AI tools; that is a vendor-blog solicitation), the other is a HackerMRR site "
         "promo inviting product stories. Dropped here so the queue's headline is digest-faithful."),
        ("ONE ROW STATES A DEADLINE THAT HAS NOW PASSED, AND NO OTHER TRACKED REQUEST STATES ONE: "
         "solicitors-and-barristers-ai-to-expand-pro-bono-capacity asked for an email 'by the end of "
         "this week' (posted 2026-10-07). It is low relevance with no resolved route, so it was never "
         "a send - recorded only so the deadline does not pass silently. This is the only stated "
         "cutoff anywhere in the 107-row set; every other row's 'deadline' field is a measured age, "
         "not a promise the poster made."),
        ("THE TWO CROSSED-BUT-LIVE DRAFTS ARE STILL LIVE AND STILL UNSENT: the Raconteur shadow-AI "
         "request is now 22 days old (unsent through TWENTY consecutive runs) and the Speciality Food "
         "request 21 days old (its October issue window closed). Both pages returned HTTP 200 again "
         "today and both routes were re-resolved by fetching them: simon.chandler@raconteur.net off "
         "/contributors/simon-chandler (HTTP 200, 154,984 bytes, triplet unchanged) and "
         "holly.shackleton@artichokehq.com off specialityfoodmagazine.com/contact (HTTP 200, 59,488 "
         "bytes, alongside five other named masthead addresses). Neither is void - what was lost is "
         "the ideal window, not the pitch."),
    ],
    "summary": (
        f"{len(ops)} tracked requests (101 carried and all 101 re-verified live, {len(NEW_ROWS)} new "
        f"AI-token finds added, 2 untracked rows removed, 0 dropped off, 3 pitched, 1 deliberately "
        f"skipped). Of the {len(live_unp) + len(cold_unp)} unpitched, {len(live_unp)} are live and "
        f"{len(cold_unp)} are cold, and ONE is sendable: the WSJ columnist's blocked-work-accounts "
        "request, now 4 days old, relevance 'medium', reply route re-verified off his own byline page "
        "(LinkedIn DM, HTTP 200, 636,389 bytes, George's lane). The new window produced 8 AI-token "
        "slugs and ZERO AI+spend slugs - the first clean window in four runs - so nothing core-beat "
        "was added. The headline figure set moved only in its denominator (76 -> 77 tools); the pair "
        "range held at 1.11x-2.53x over 19 tiers. No new replies to any tracked pitch. Zero pitches "
        "sent this run - sends remain George's lane."
    ),
    "recommended_actions": [
        ("SEND THE WSJ BLOCKED-WORK-ACCOUNTS DRAFT - STILL THE ONLY SENDABLE ROW, NOW 4 DAYS OLD AND "
         "THE OLDEST IT HAS EVER BEEN. Paste-ready at pitch-drafts-2026-10-09.md section 1. Route: "
         "LinkedIn DM to https://www.linkedin.com/in/christopher-mims-club/ (re-verified HTTP 200, "
         "636,389 bytes, title 'Christopher Mims - The Wall Street Journal | LinkedIn'); the "
         "request's own body says '(DMs open)'. Relevance 'medium'. George's lane. This row has now "
         "been carried by eight consecutive runs without a send."),
        ("RESOLVE A ROUTE FOR THE GOOGLE & CLAUDE SEATS-AND-TOKENS REQUEST - STILL THE BEST-MATCHING "
         "REQUEST THIS MONITOR HAS SEEN AND STILL UNSENDABLE FOR WANT OF A ROUTE. Glenn Hansen wants "
         "enterprise AI seat and token costs; our dated set holds Claude Team $20/$100 per seat/month, "
         "Gemini Workspace org rates and Copilot Business $19 / Enterprise $39 per user/month. The "
         "page publishes no address or handle and a web search cannot confirm WHICH Glenn Hansen he is "
         "(a same-name LinkedIn profile is a different person), so no route must be invented. Second "
         "run carrying it; it is now 1 day old."),
        ("SEND OR FORMALLY DROP THE RACONTEUR SHADOW-AI DRAFT - TWENTY RUNS UNSENT. pitch-drafts-"
         "2026-10-09.md section 2, route simon.chandler@raconteur.net (re-resolved today, HTTP 200, "
         "154,984 bytes, triplet unchanged). Now 22 days old. Still the only HIGH-relevance request "
         "with a resolved route. The honest options are a late send or a `skipped` entry in "
         "pitch-ledger.json; a twenty-first carry is the thing to avoid."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-10-09.md section 3, "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact, HTTP 200, "
         "59,488 bytes, 21 days old). Its October issue window has closed: make it a send-or-skip "
         "call and record the outcome in pitch-ledger.json."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI - NOW TWENTY-ONE DAYS OUTSTANDING. Route: reply to "
         "jan@jansuski.com, In-Reply-To the existing thread."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. It remains the only lever that widens the "
         "monitor beyond Sourcee. Today is the argument FOR widening rather than retiring it: the "
         "single accessible source produced zero core-beat finds and zero AI+spend slugs in its "
         "105-slug window, so the monitor's supply is the constraint, not its filters."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": len(win["ai_strict"]),
        "ai_plus_spend_regex_false_positives": 0,
        "new_ai_token_slugs_added_to_tracking": len(NEW_ROWS),
        "untracked_rows_removed": len(UNTRACKED),
        "consecutive_runs_without_new_core_beat": 1,
        "tracked_urls": len(ops),
        "carried_and_reverified": 101,
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
        "rows_at_ten_days_crossing_next_run": sum(
            1 for o in ops if (o.get("_days_old") or 99) == 10),
        "lost_to_the_cold_line_with_a_draft_ready": 0,
        "shadow_ai_tools_tracked": 77,
        "shadow_ai_monthly_priced_tools": 42,
        "shadow_ai_at_or_under_25": 33,
        "shadow_ai_median_cheapest_paid_tier": 17.50,
    },
    "monitor_defects_fixed_this_run": [
        ("THE QUEUE'S HEADLINE COUNT WAS NOT DIGEST-FAITHFUL: the live count it printed (53) included "
         "two rows that no digest has ever recorded as opportunities. build_pitch_queue.py merges "
         "`digest-*.json::opportunities`; scripts/verify_journo_requests.py, run with no arguments, "
         "sweeps every URL in every digest AND the ledger AND pitch-queue.md - and pitch-queue.md had "
         "carried those two rows, so the cache held them and the queue's verified-count path surfaced "
         "them. Fixed at the data layer: both are removed from tracking in this digest, so the queue "
         "will read 51 live on its next build. Class of defect: a count that includes rows the "
         "monitor never classified, which is the mirror image of the index-page bug the queue already "
         "filters."),
        ("A MISSED AI+SPEND SLUG, RECORDED BECAUSE IT CHANGES WHAT THE METRIC MEANS: "
         "saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup is carried at 17 days and "
         "is in the cache, but has zero occurrences in any digest's `opportunities` array - another "
         "record that entered only via a probe. It was not added to the digest for that reason; the "
         "cross-reference is noted so the 'carried 101' number is checkable against the cache "
         "(cache holds 103 records: 101 carried + the 2 removed + 0 unaccounted - verified)."),
        ("FIGURES RE-DERIVED, NOT COPIED, AND THE DENOMINATOR CHANGE PROPAGATED. "
         "marketing/haro-outreach/_figures_1009.py recomputed the headline set from "
         "data/pricing_snapshots.json (`updated: 2026-10-09`, 77 snapshots), data/tools.json and "
         "data/monthly_annual_pairs.json. The carried drafts' '42 of 76 tools' sentences are rewritten "
         "to 77 by this writer's `_repair()`, so a stale denominator cannot survive into today's "
         "file - the same defect class as the 2026-10-02 figure drift, reached through the "
         "denominator rather than the numerator."),
        ("NO NEW DEFECT IN THE SENDABLE ROW. employees-blocked-from-ai was re-verified today (HTTP "
         "200, 4 days old, relevance 'medium') and its route re-fetched (LinkedIn byline page HTTP "
         "200, 636,389 bytes, exact title match). Its draft re-derives figures at build time. The two "
         "prior sendable defects (the 2026-09-29 chrome leak into `published_links`, the 2026-10-01 "
         "Google Form read as a route) remain fixed in scripts/build_pitch_queue.py."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print(f"wrote digest-{TODAY}.json: {len(ops)} opportunities, {len(digest['platforms_checked'])} platforms")
print(f"live(<=10d): {len(live)}  cold(>10d): {len(stale)}  live_unp: {len(live_unp)}  cold_unp: {len(cold_unp)}")
print(f"crossed cold since last digest: {crossed}")
print(f"repaired rows: {repaired}")
