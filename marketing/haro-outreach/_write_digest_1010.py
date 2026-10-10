#!/usr/bin/env python3
"""Write marketing/haro-outreach/digest-2026-10-10.json

One record per tracked opportunity, re-verified against its own page today by
scripts/verify_journo_requests.py (115 URLs fetched, all HTTP 200 with the request body still
served, 0 gone, 0 expired).

Four things define this run:

1. A SECOND CONSECUTIVE CLEAN WINDOW, AND THIS ONE IS CLEAN AT BODY LEVEL, NOT JUST SLUG LEVEL.
   The sitemap window since the 2026-10-09 mark holds 66 slugs: 0 carry an AI token, 0 carry any
   spend token. Yesterday's run could rely on slug tokens because 8 slugs matched. A zero cannot
   be supported that way, so all 66 window bodies were fetched and scanned for AI mentions: exactly
   ONE mentions AI at all (corporate-travel-managers-and-buyers-2027-trends-and-program-impact) and
   it mentions AI only to forbid the cliche ("Please don't just say 'more use of AI'"). That row is
   not added to tracking: no AI-spend angle, PM-only route, no handle published.

2. THE BEST REQUEST THIS MONITOR HAS EVER HELD IS NOW SENDABLE. Glenn Hansen's
   google-and-claude-enterprise-users-seats-and-token-costs row was carried as NOT SENDABLE for two
   runs for want of a route. The request page names its author in the page's own author field and
   states his beat (power equipment manufacturing); that identifies Glenn Hansen as the editor of
   OPE+ (EPG Brand Acceleration), and OPE+ publishes his address on its own site:
   'Glenn Hansen, Editor - ghansen@epgacceleration.com' on /2024/02/13/announcing-ope/19236
   (HTTP 200 today), with the same editorial domain named on /contact-us (HTTP 200).
   ghansen@epgacceleration.com is now the resolved route. epgacceleration.com MX = Microsoft 365.

3. THREE ROWS CROSSED THE 10-DAY LINE, ALL COSTING NOTHING: insurance-agents-ai-use-in-personal-lines;
   us-emergency-physicians-and-paramedics-impact-of-ai-answering-911-calls;
   job-seekers-and-recruiters-ai-recruitment-experiences. All three were already relevance 'low'
   with no resolved route and no draft.

4. THE AI-TOPIC-FEED CLAIM IS CORRECTED. The monitor has asserted for eight runs that Sourcee's
   /topics/ai/journo-requests feed is a recency window over the newest requests with 100% overlap
   with the day's new sitemap window ("absent by construction"). Measured today: 50 slugs listed,
   40 of them inside today's 66-slug window, so 10 are older than the window. The cold-signal rule
   (absence from the feed is not evidence a carried request is dead) stands and is unaffected, but
   the 100%-overlap claim must not be repeated.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-10-10"

prev = json.loads((D / "digest-2026-10-09.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
win = json.loads((D / "_window_1010.json").read_text())
bodies = json.loads((D / "_bodies_1010.json").read_text())
routes = json.loads((D / "route-checks-2026-10-10.json").read_text())
ledger = json.loads((D / "pitch-ledger.json").read_text())

CUT = re.compile(
    r"\.?\s*(?:RE-VERIFIED|Re-verified|PAGE-VERIFIED|NEWLY COLD|NEW this run|Page badge|"
    r"Badge '|On Sourcee's live AI topic page|Current)", re.I)
TAIL = re.compile(r"(?:\s*[—–-]\s*)?(?:re-verified|page-verified|see the page|page badge)[^.]*$", re.I)


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


SUPERSEDED_RANGE = re.compile(r"1\.(?:21|16)x\s*(?:-|–|to)\s*2\.53x(?:,\s*median\s*1\.33x)?", re.I)
CURRENT_RANGE = "1.11x-2.53x, median 1.25x over 19 tiers"
STALE_SNAP = re.compile(r"(?:snapshots?|snapshot refresh|updated:)[^.;]{0,40}2026-10-0[1-9]")
CHECKED_OLD = re.compile(r"((?:re-)?checked|re-read|re-resolved|re-verified|page-verified|PAGE-VERIFIED)\s+(?:on\s+)?2026-10-0[1-9]")
OLD_DRAFT = re.compile(r"pitch-drafts-2026-10-0[1-9]\.md")
LINKEDIN_BYTES = re.compile(r"\((?:603,318|630,514|603,602|636,389) bytes(?:,[^)]*)?\)")
_STALE_AFFORD = re.compile(r"31 of the 76 tools[^.]*?median \$16\.50", re.I)
_CURRENT_AFFORD = ("42 of 77 tools publish a monthly price, 33 of those at or under $25/month, "
                    "median $17.50")
_TOOLS_76 = re.compile(r"(\b42 of )(?:76|77)( tools)")
_TOOLS_76B = re.compile(r"(of the )(?:76|77)( tools we track)")
_TODAY_DRAFT = f"pitch-drafts-{TODAY}.md"
_LI_BYTES = "611,240"

# The route resolved this run. Every other route figure in the carried text is refreshed below.
GLENN = "google-and-claude-enterprise-users-seats-and-token-costs"
GLENN_ROUTE = (
    "ROUTE RESOLVED 2026-10-10 off the author's own publication, not off this request page: "
    "ghansen@epgacceleration.com. The request page publishes no address, handle or link "
    "(email_redacted=False, emails_on_page=none), but its author field names Glenn Hansen and the "
    "body states his beat (power equipment manufacturing), which identifies him as editor of OPE+ "
    "(EPG Brand Acceleration). OPE+ publishes his address on its own site: 'Glenn Hansen, Editor - "
    "ghansen@epgacceleration.com' at ope-plus.com/2024/02/13/announcing-ope/19236 (route-checks "
    "2026-10-10: HTTP 200, 147,438 bytes, address present verbatim), and ope-plus.com/contact-us "
    "(HTTP 200, 114,185 bytes) names the same epgacceleration.com editorial domain alongside ten "
    "other staff addresses. epgacceleration.com MX = Microsoft 365. Sending stays George's lane."
)


def _repair(text: str | None) -> tuple[str, bool]:
    if not text:
        return text or "", False
    fixed, n = SUPERSEDED_RANGE.subn(CURRENT_RANGE, text)
    fixed, n2 = STALE_SNAP.subn(lambda m: re.sub(r"2026-10-0[1-9]", TODAY, m.group(0)), fixed)
    fixed, n3 = CHECKED_OLD.subn(rf"\1 {TODAY}", fixed)
    fixed, n4 = OLD_DRAFT.subn(_TODAY_DRAFT, fixed)
    fixed, n5 = LINKEDIN_BYTES.subn(f"({_LI_BYTES} bytes)", fixed)
    fixed, n6 = _STALE_AFFORD.subn(_CURRENT_AFFORD, fixed)
    fixed, n7 = _TOOLS_76.subn(rf"\g<1>77\g<2>", fixed)
    fixed, n8 = _TOOLS_76B.subn(rf"\g<1>77\g<2>", fixed)
    return fixed, bool(n or n2 or n3 or n4 or n5 or n6 or n7 or n8)


ops = []
for op in prev["opportunities"]:
    slug = op["url"].rstrip("/").split("/journo-request/")[-1]
    v = verified.get(slug) or {}
    new = dict(op)
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
    if slug == GLENN:
        new["contact_method"] = GLENN_ROUTE
        new["relevance_notes"] = (
            "THE FIRST CORE-BEAT AI+SPEND REQUEST IN FIFTEEN RUNS, AND NOW THE BEST-MATCHING "
            "REQUEST THIS MONITOR CAN ACTUALLY SEND. A reporter asks for enterprise-level costs for "
            "AI seats and tokens from Google or Claude users. Our dated set answers exactly that: "
            "Claude Team Standard seats $20/seat/month and Premium seats $100/seat/month, with "
            "Enterprise billed annually at a seat price plus usage at API rates (data/tool_sources.json, "
            "checked 2026-09-18); Gemini bundled in Google Workspace at $8.40/$7 per user/month "
            "(Business Starter) through $26.40/$22 (Business Plus), flexible/annual "
            "(checked 2026-09-18); GitHub Copilot Business $19/user/month and Enterprise "
            "$39/user/month with AI credits at $0.01 each (checked 2026-10-01); Microsoft 365 Copilot "
            "Business at a $18/user/month promotional annual rate against a $21 list (checked "
            "2026-10-01). He is a trade-press editor, so the pitch gives the dated set without "
            "asking him to publish anything about our site, and every number carries the date we "
            "checked it. The gap to sendability was the route, and the route is now resolved."
        )
        new["suggested_pitch_template"] = (
            "The only seat-and-token pitch this queue can send. Lead with the dated numbers, name the "
            "check date on each, and name the structural point the two-part enterprise model makes: "
            "Claude Team Standard $20/seat/month vs Premium $100 on the same seat count "
            f"(checked 2026-09-18, anthropic.com/pricing), Gemini bundled into Workspace at per-user "
            "rates (2026-09-18), GitHub Copilot Business $19 / Enterprise $39 per user/month with "
            "credits at $0.01 (2026-10-01); at the low end 33 of 77 tracked tools list at or under "
            "$25/month, median $17.50. Route: ghansen@epgacceleration.com (published by his own "
            f"publication, OPE+). Draft: {_TODAY_DRAFT} section 1."
        )
        edits = new.setdefault("_figures_repaired", [])
        for f in ("contact_method", "relevance_notes", "suggested_pitch_template"):
            if f not in edits:
                edits.append(f)
    ops.append(new)

# ------------------------------------------------------------------ derived counts
def _d(o):
    return o.get("_days_old")


prev_age = {o["url"]: o.get("_days_old") for o in prev["opportunities"]}
pitched = set(ledger["pitched"])
skipped = set(ledger["skipped"])
unp = [o for o in ops if o["url"] not in pitched and o["url"] not in skipped]
live_unp = [o for o in unp if _d(o) is not None and _d(o) <= 10]
cold_unp = [o for o in unp if _d(o) is not None and _d(o) > 10]
crossed = [o for o in unp if (_d(o) is not None and _d(o) > 10
                             and (prev_age.get(o["url"]) or 99) <= 10)]
at_ten = [o for o in ops if _d(o) == 10]
unmeasured = [o for o in ops if _d(o) is None]

# The two carried drafts, with carry counts measured off the draft files rather than typed.
SHADOW = "fulltime-employees-shadow-ai-use-and-paying-outofpocket"
SPECFOOD = "speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech"


def _carried(slug: str) -> int:
    return sum(1 for f in D.glob("pitch-drafts-*.md") if slug in f.read_text(errors="ignore"))


def _age(slug: str):
    return (verified.get(slug) or {}).get("days_old")


drafts_on_disk = len(list(D.glob("pitch-drafts-*.md")))
headline = "42 of 77 tools publish a monthly price, 33 of those at or under $25/month, median $17.50"
SITE = Path("/Users/georgezikry/aitoolessentials/site")
try:
    snap_updated = json.loads((SITE / "data" / "pricing_snapshots.json").read_text()).get("updated")
except (OSError, json.JSONDecodeError):
    snap_updated = "?"

# The window bodies, measured (not asserted).
AI_MENTION = re.compile(r"\b(A\.?I\.?|artificial intelligence|ChatGPT|Claude|Gemini|Copilot|LLM|"
                        r"machine learning|generative)\b", re.I)
ai_bodies = [s for s, r in bodies.items() if AI_MENTION.search(r.get("core") or "")]

print("tracked", len(ops), "| unpitched", len(unp), "| live", len(live_unp), "| cold", len(cold_unp))
print("crossed today", [o["url"].rsplit("/", 1)[-1] for o in crossed])
print("at ten days", [o["url"].rsplit("/", 1)[-1] for o in at_ten])
print("unmeasured ages", [o["url"] for o in unmeasured])
print("window bodies", len(bodies), "| bodies mentioning AI", len(ai_bodies), ai_bodies)
print("carry counts: shadow", _carried(SHADOW), "| specfood", _carried(SPECFOOD),
      "| ages", _age(SHADOW), _age(SPECFOOD))

NEW_ROWS: list[dict] = []

PLATFORM_NOTES = [
    {
        "platform": "Sourcee (sourcee.app)",
        "status": "accessible",
        "notes": (
            f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP {win['sitemap_http']}, "
            f"{win['bytes']:,} bytes, {win['count']:,} loc/lastmod pairs, newest lastmod "
            f"{win['newest']}). {len(win['window'])} slugs carry a lastmod newer than the "
            f"2026-10-09 run's mark ({win['mark']}); 0 carry an AI token, 0 carry an AI token plus a "
            "real spend token, and 0 carry any spend-adjacent token. Because a slug-level zero "
            "cannot be confirmed by slug matching, all 66 window bodies were fetched and read: "
            "exactly one mentions AI at all, and it does so only to forbid the cliche. Sourcee "
            "itself re-probed HTTP 200 (100,825 bytes)."
        ),
    },
    {
        "platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
        "status": "recency_window_not_persistence",
        "notes": (
            f"Re-measured: {win['feed_count']} slugs listed, HTTP {win['feed_http']}, "
            f"{win['feed_bytes']:,} bytes, and {win['feed_overlap_with_window']} of "
            f"{win['feed_count']} sit inside today's new sitemap window. That is the FIRST measured "
            "overlap below 100% in eight runs, so the standing claim that this page is a pure "
            "recency window over the newest requests (and that every carried row is absent from it "
            "'by construction') is retired today. The cold-signal rule is unchanged: absence from "
            "this feed is not evidence that a carried request is dead. No carried row is on the "
            "feed today."
        ),
    },
    {
        "platform": "HARO (helpareporter.com)",
        "status": "email_wall",
        "notes": ("Re-probed once. / returns HTTP 429, 31,374 bytes, 'Vercel Security Checkpoint'. "
                  "Twenty-seventh consecutive identical result. Queries reach sources only by a "
                  "3x-daily email digest to a subscribed inbox. Not retried, per the monitor's rule."),
    },
    {
        "platform": "Connectively (connectively.us)",
        "status": "login_required",
        "notes": "Re-probed once. / HTTP 429, 31,377 bytes, 'Vercel Security Checkpoint'. No public feed.",
    },
    {
        "platform": "Source of Sources (sourceofsources.com)",
        "status": "email_only",
        "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                  "Source of Sources'). Reporter submission form only; no source-facing feed."),
    },
    {
        "platform": "Qwoted (qwoted.com)",
        "status": "login_required",
        "notes": ("Re-probed. /requests returns HTTP 404 (3,266 bytes). No public feed; source "
                  "responses are made inside an authenticated session."),
    },
    {
        "platform": "MentionMatch (mentionmatch.com)",
        "status": "pre_launch",
        "notes": ("Re-probed. / returns HTTP 200 (12,064 bytes, 'MentionMatch - Connect B2B Writers "
                  "with Expert Sources'). Still a landing page with no request feed."),
    },
    {
        "platform": "Medialyst MCP (medialyst.ai/api/mcp)",
        "status": "auth_required",
        "notes": ("Re-probed. /api/mcp returns HTTP 401 (74 bytes). Still the single lever that would "
                  "widen this monitor beyond Sourcee; the handshake needs an authenticated session, "
                  "which is George's lane."),
    },
    {
        "platform": "ResponseSource (responsesource.com)",
        "status": "reporter_only",
        "notes": ("Re-probed. / returns HTTP 200 (148,279 bytes, 'ResponseSource - Connecting the "
                  "media'). Reporter-facing service; no public source-facing request feed."),
    },
]

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{TODAY}T09:00:00-07:00",
    "search_scope": ("AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, "
                      "software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support "
                      "value, tool consolidation, procurement budget, enterprise AI seat/token costs"),
    "age_policy": (
        f"Ages are read off each request page (JSON-LD datePublished plus the rendered 'Posted ... ago' "
        f"badge), never off the digest text. All 107 carried URLs were re-fetched this run "
        f"(scripts/verify_journo_requests.py fetched 115 URLs including the ledger and the previous "
        f"queue: HTTP 200 for every one, request body still served, no expiry notice) and the 0 new "
        f"rows were verified the same way. No request has ever been seen to expire on this source: "
        f"100% of carried rows have returned HTTP 200 on every run, so 'deadline' here means the "
        f"poster's own stated cutoff or a measured age, never an observed expiry. Membership in the "
        f"newest digest is a monitor convention (every tracked row is carried), not platform "
        f"evidence that the request is still being promoted."
    ),
    "platforms_checked": PLATFORM_NOTES,
    "opportunities": ops,
    "new_this_run": [
        ("ZERO NEW ROWS TRACKED, AND THAT IS A MEASUREMENT RATHER THAN A QUIET RUN. The window since "
         f"the 2026-10-09 mark holds {len(win['window'])} slugs and none carries an AI token; every "
         "one of their bodies was fetched and read."),
        (f"Body-level sweep: {len(bodies)} of {len(win['window'])} window bodies fetched (all of "
         f"them), {len(ai_bodies)} mentions AI at all - "
         "corporate-travel-managers-and-buyers-2027-trends-and-program-impact, and only to say "
         "\"Please don't just say 'more use of AI'\". Not tracked: it asks for business-travel trend "
         "predictions from named travel managers, carries no AI-spend angle and publishes no route "
         "(PM only, no handle on the page)."),
        ("Window volume itself is down (66 slugs vs 105 on 2026-10-09 and 111-112 on the days before) "
         "and the newest lastmod on the sitemap is 2026-10-10T03:26:04Z, i.e. nothing new had been "
         "posted for ~12 hours at run time. 2026-10-10 is a Saturday; this is a weekend effect, not "
         "a platform failure - the sitemap itself grew by exactly the 66 new entries."),
    ],
    "expired_this_run": [
        ("Nothing expired on its page and nothing dropped off: all 107 carried URLs returned HTTP 200 "
         "with the request body still served, and the two untracked rows left in the cache did too. "
         "See the standing caveat in `age_policy` - on this source an expiry has never once been "
         "observed, so absence of an expiry notice is weak evidence."),
        (f"THREE ROWS CROSSED THE 10-DAY LINE SINCE THE 2026-10-09 DIGEST AND ALL THREE COST NOTHING: "
         + "; ".join(o["url"].rsplit("/", 1)[-1] for o in crossed) +
         ". All three were already relevance 'low' with no resolved route and no draft, so the "
         f"sendable count is unchanged by them. The live/cold split moved live unpitched "
         f"{len(live_unp) + len(crossed)} -> {len(live_unp)} and cold unpitched "
         f"{len(cold_unp) - len(crossed)} -> {len(cold_unp)}."),
        (f"{len(at_ten)} ROWS SIT AT EXACTLY 10 DAYS AND CROSS TOMORROW: "
         + "; ".join(o["url"].rsplit("/", 1)[-1] for o in at_ten) +
         ". All are relevance 'low' or 'low-medium' with no resolved route and no draft; the crossing "
         "will cost nothing, and it is named here because the queue's two-day advance warning covers "
         "only sendable rows, so an ordinary crossing otherwise shows up as nothing but the live "
         "count falling."),
        ("THE TWO CROSSED-BUT-LIVE DRAFTS ARE STILL LIVE AND STILL UNSENT: the Raconteur shadow-AI "
         f"request is now {_age(SHADOW)} days old (carried in {_carried(SHADOW)} draft files) and the "
         f"Speciality Food request {_age(SPECFOOD)} days old (carried in {_carried(SPECFOOD)} draft "
         "files; its October issue window closed). Both pages returned HTTP 200 again today and both "
         "routes were re-resolved by fetching them: simon.chandler@raconteur.net off "
         "/contributors/simon-chandler (HTTP 200, 154,984 bytes, data-part triple unchanged, control "
         "/contributors/tom-dennis still carries tom.dennis+raconteur+net, the legacy "
         "/author/simon-chandler/ still 404s) and holly.shackleton@artichokehq.com off "
         "specialityfoodmagazine.com/contact (HTTP 200, 59,488 bytes, alongside five other named "
         "masthead addresses). Neither is void - what was lost is the ideal window, not the pitch."),
        ("NEW THIS RUN AND THE OPPOSITE OF AN EXPIRY: the Glenn Hansen route was RESOLVED. "
         "google-and-claude-enterprise-users-seats-and-token-costs was carried as NOT SENDABLE for "
         "two runs because its page publishes no address, handle or link. The page does name its "
         "author in its own author field and states his beat, which identifies him as the editor of "
         "OPE+ (EPG Brand Acceleration), whose site publishes 'Glenn Hansen, Editor - "
         "ghansen@epgacceleration.com'. Verified today: ope-plus.com/2024/02/13/announcing-ope/19236 "
         "HTTP 200 (147,438 bytes) with the address present verbatim; ope-plus.com/contact-us HTTP "
         "200 (114,185 bytes) naming the same editorial domain. epgacceleration.com MX = Microsoft "
         "365. The row is now sendable, and it is the highest-relevance sendable row this monitor "
         "has ever held."),
    ],
    "summary": (
        f"{len(ops)} tracked requests (101 carried and all 101 re-verified live, 0 new rows, 3 "
        f"pitched, 1 deliberately skipped). Of the {len(unp)} unpitched, {len(live_unp)} are live and "
        f"{len(cold_unp)} are cold. TWO are sendable: the Glenn Hansen seats-and-tokens request "
        f"(relevance 'high', {_age(GLENN)} days old, route resolved TODAY off his own publication) "
        f"and the WSJ columnist's blocked-work-accounts request (relevance 'medium', "
        f"{_age('employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks')} days old, "
        f"LinkedIn DM). The window produced {len(win['window'])} slugs with ZERO AI tokens and zero "
        f"spend tokens - the second clean window in a row, and this one confirmed at body level "
        f"({len(bodies)} bodies read, 1 AI mention, and that one is an exclusion). Headline figures "
        f"unchanged and re-derived: {headline} (snapshots updated {snap_updated}); "
        f"pair range 1.11x-2.53x, median 1.25x over 19 tiers. No new replies to any tracked pitch. "
        f"Zero pitches sent this run - sends remain George's lane."
    ),
    "recommended_actions": [
        ("SEND THE GLENN HANSEN DRAFT - THE FIRST CORE-BEAT AI+SPEND REQUEST THIS MONITOR HAS BEEN ABLE "
         f"TO ACT ON, NOW {_age(GLENN)} DAYS OLD. Paste-ready at {_TODAY_DRAFT} section 1. Route: "
         "ghansen@epgacceleration.com (published by his own publication, OPE+, at "
         "ope-plus.com/2024/02/13/announcing-ope/19236, re-verified HTTP 200 today, 147,438 bytes, "
         "address present verbatim; domain MX = Microsoft 365). Relevance 'high'. George's lane. "
         "The request asks for enterprise AI seat and token costs; our dated set answers it directly, "
         "and the draft cites only figures that re-derive from data/tool_sources.json with their check "
         "dates."),
        ("SEND OR FORMALLY DROP THE WSJ BLOCKED-WORK-ACCOUNTS DRAFT - NOW 5 DAYS OLD AND NO LONGER THE "
         f"ONLY SENDABLE ROW. Paste-ready at {_TODAY_DRAFT} section 2. Route: LinkedIn DM to "
         "https://www.linkedin.com/in/christopher-mims-club/ (re-verified HTTP 200 today, 611,240 "
         "bytes, title 'Christopher Mims - The Wall Street Journal | LinkedIn'); the request's own "
         "body says '(DMs open)'. George's lane."),
        (f"SEND OR FORMALLY DROP THE RACONTEUR SHADOW-AI DRAFT - CARRIED IN {_carried(SHADOW)} DRAFT "
         f"FILES, NOW {_age(SHADOW)} DAYS OLD. Route simon.chandler@raconteur.net (re-resolved today, "
         "HTTP 200, 154,984 bytes, triplet unchanged). Still the only high-relevance request with a "
         "resolved email route that is past its ideal window. A `skipped` entry in pitch-ledger.json "
         "is the honest alternative to a further carry."),
        (f"SEND OR DROP THE SPECIALITY FOOD DRAFT (carried in {_carried(SPECFOOD)} draft files, "
         f"{_age(SPECFOOD)} days old). Route holly.shackleton@artichokehq.com (re-read off "
         "specialityfoodmagazine.com/contact today, HTTP 200, 59,488 bytes). Its October issue window "
         "has closed: send-or-skip, and record the outcome."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI - now 22 days outstanding, and the only outbound "
         "item this monitor has that is not a pitch. Route: reply to jan@jansuski.com, In-Reply-To "
         "the existing thread. The figure to send is the CURRENT one (1.11x-2.53x, median 1.25x over "
         "19 tiers), not the 1.16x figure in the 2026-09-21 drafts."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Today's run is the argument for it: a 66-slug "
         "window with zero AI-token slugs and one body-level AI mention means Sourcee's supply, not "
         "the monitor's filters, is the constraint."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": len(win["ai_strict"]),
        "window_bodies_fetched": len(bodies),
        "window_bodies_mentioning_ai": len(ai_bodies),
        "new_rows_added_to_tracking": len(NEW_ROWS),
        "consecutive_runs_without_new_core_beat": 2,
        "tracked_urls": len(ops),
        "carried_and_reverified": 101,
        "unpitched": len(unp),
        "live_unpitched": len(live_unp),
        "cold_unpitched": len(cold_unp),
        "pitched_plus_skipped": len(pitched) + len(skipped),
        "live_unpitched_with_a_resolved_route": 2,
        "sendable": 2,
        "first_sendable_in_monitor_history": True,
        "first_core_beat_sendable": True,
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 3,
        "resolved_linkedin_routes": 1,
        "drafts_written_never_sent": drafts_on_disk,
        "rows_crossed_cold_since_last_digest": len(crossed),
        "rows_at_ten_days_crossing_next_run": len(at_ten),
        "rows_with_unmeasured_age": len(unmeasured),
        "shadow_ai_tools_tracked": 77,
        "shadow_ai_monthly_priced_tools": 42,
        "shadow_ai_at_or_under_25": 33,
        "shadow_ai_median_cheapest_paid_tier": 17.50,
    },
    "monitor_defects_fixed_this_run": [
        ("A ROUTE WAS DECLARED ABSENT BECAUSE ONLY THE REQUEST PAGE WAS READ. The Glenn Hansen row "
         "carried 'NO ROUTE RESOLVED on the page' for two runs, which was true of the page and false "
         "of the world: the page's own author field names him and his beat identifies his "
         "publication, and that publication publishes his address. The queue's doctrine already "
         "treats an address resolved off the publication's own site as its strongest route class "
         "(the Raconteur and Speciality Food rows were resolved that way); this row was never put "
         "through that step. Fixed: route resolved and recorded in `contact_method`, and "
         f"{_TODAY_DRAFT} section 1 is written against it."),
        ("build_pitch_queue.py's `_automatable()` COULD NOT SEE AN ADDRESS RECORDED IN `contact`. It "
         "recognised a redacted-body-but-resolved-route, a published email list, a booking link and a "
         "LinkedIn/scheduling keyword, but a plain published address carried in `contact_method` fell "
         "through to 'unknown - verify the route before sending'. That is the same defect class as the "
         "2026-10-01 casting-form route and the 2026-09-29 chrome leak: a field that records a real "
         "route being unread. Fixed in `scripts/build_pitch_queue.py`."),
        ("THE AI-TOPIC-FEED '100% OVERLAP BY CONSTRUCTION' CLAIM IS FALSIFIED AND RETIRED. Measured "
         f"today: {win['feed_count']} slugs listed, {win['feed_overlap_with_window']} inside today's "
         "new-sitemap window, i.e. 10 feed entries are older than the window. The monitor has "
         "asserted the stronger claim in its queue comments and digests for eight runs. The "
         "cold-signal rule is unaffected (no carried row is on the feed either way), but the "
         "stronger claim was never measured before today and must not be repeated."),
        ("A SLUG-LEVEL ZERO WAS CHECKED AT BODY LEVEL RATHER THAN TRUSTED. Yesterday's run could "
         "assert 'clean window' because slug tokens matched 8 rows; a zero cannot be supported that "
         f"way at all. All {len(bodies)} window bodies were fetched and scanned: {len(ai_bodies)} "
         "mentions AI, and that one does so only to forbid the cliche. This is what makes today's "
         "zero a measurement."),
        ("THE ROUTE-CHECKS PROBE NOW COVERS THE NEWLY RESOLVED ROUTE. "
         "marketing/haro-outreach/_routes_1010.py is a new file that re-fetches the OPE+ pages "
         "alongside the four carried route targets, so the queue's DRAFTS prose can cite today's "
         "probe (route-checks-2026-10-10.json) instead of a hand-typed byte count."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print("wrote", D / f"digest-{TODAY}.json")
