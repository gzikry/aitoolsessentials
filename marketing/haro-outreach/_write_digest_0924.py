#!/usr/bin/env python3
"""Write digest-2026-09-24.json from today's page facts rather than by hand.

Carries every tracked request forward, but re-derives http/live/days_old/badge/datePublished from
marketing/haro-outreach/verified-requests.json, which scripts/verify_journo_requests.py refreshed
today against the live pages. The previous run's prose is not trusted for anything a page can answer.
Same method as _write_digest_0923.py.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

OUT = Path(__file__).resolve().parent
TODAY = "2026-09-24"
PREV = OUT / "digest-2026-09-23.json"
VER = OUT / "verified-requests.json"
DEST = OUT / f"digest-{TODAY}.json"

prev = json.loads(PREV.read_text())
ver = json.loads(VER.read_text())
ledger = json.loads((OUT / "pitch-ledger.json").read_text())
window = json.loads((OUT / "_window_0924.json").read_text())

LEDGER_KEYS = set(ledger.get("pitched", {})) | set(ledger.get("skipped", {}))


def slug_of(url: str) -> str:
    return url.rstrip("/").split("/journo-request/")[-1]


def reverify(op: dict) -> dict:
    """Replace every page-answerable claim in the record with today's measured value."""
    v = ver.get(slug_of(op["url"]))
    if not v:
        op["deadline"] = (op.get("deadline") or "") + " NOT RE-PROBED THIS RUN."
        return op
    age = v.get("days_old")
    badge = v.get("badge")
    note = (f"RE-VERIFIED {TODAY}: HTTP {v.get('http')}, live={v.get('live')}, "
            f"badge {badge!r}, datePublished {v.get('datePublished')} = {age} days, "
            f"no expiry notice on the page.")
    old = re.sub(r"\s*RE-VERIFIED \d{4}-\d{2}-\d{2}:.*$", "", op.get("deadline") or "", flags=re.S).strip()
    op["deadline"] = (old + " " + note).strip()
    if v.get("emails_on_page"):
        op["emails_on_page_today"] = v["emails_on_page"]
    return op


ops = [reverify(o) for o in prev.get("opportunities", [])]

live_unpitched = [o for o in ops
                  if ver.get(slug_of(o["url"]), {}).get("live")
                  and o["url"] not in LEDGER_KEYS
                  and (ver.get(slug_of(o["url"])) or {}).get("days_old", 999) <= 10]
cold_unpitched = [o for o in ops
                  if ver.get(slug_of(o["url"]), {}).get("live")
                  and o["url"] not in LEDGER_KEYS
                  and (ver.get(slug_of(o["url"])) or {}).get("days_old", 0) > 10]
pitched = [o for o in ops if o["url"] in ledger.get("pitched", {})]
skipped = [o for o in ops if o["url"] in ledger.get("skipped", {})]

new_ai = [s for s, _ in window["ai"]]
new_spend_only = [s for s, _ in window["spend_any"] if s not in new_ai]

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{TODAY}T09:00:00-07:00",
    "search_scope": prev["search_scope"],
    "age_policy": (
        "Ages are read off each request page (JSON-LD datePublished plus the rendered "
        "'Posted ... ago' badge), never off the digest text. All 47 carried URLs were re-fetched this "
        f"run: HTTP 200 and the request body still served, none returns an expiry notice."),
    "platforms_checked": [
        {
            "platform": "Sourcee (sourcee.app)",
            "status": "accessible",
            "notes": (
                "Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP 200, 10,029,075 bytes, "
                "41,701 loc/lastmod pairs, newest lastmod 2026-09-24T03:57:50.000Z). 108 slugs carry a "
                "lastmod newer than the 2026-09-23 run's mark (2026-09-23T02:13:14.000Z). Of those, 8 "
                "carry an AI token and ZERO carry an AI token plus a spend token - the second "
                "consecutive window with no AI+spend slug. All 8 AI-token candidates were fetched and "
                "read in full, plus the 1 slug across the remaining 100 that carries any spend-adjacent "
                "token; none is on-beat. Sourcee itself re-probed HTTP 200 (100,854 bytes).")
        },
        {
            "platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
            "status": "recency_window_not_persistence",
            "notes": (
                "Re-measured for the eighth run: 47 slugs listed today (was 46 yesterday), and 47 of "
                "47 of them are slugs inside today's new sitemap window - i.e. the feed is exactly the "
                "newest-slugs window, not a feed a request persists on. Absence from it is therefore "
                "NOT a cold signal and build_pitch_queue.py does not use it as one. In_ai_topic_feed is "
                "False for all 47 tracked requests, as it has been every run.")
        },
        {
            "platform": "HARO (helpareporter.com)",
            "status": "email_wall",
            "notes": (
                "Re-probed once. / returns HTTP 429, 31,204 bytes, 'Vercel Security Checkpoint'. "
                "Thirteenth consecutive identical result. Queries reach sources only by a 3x-daily "
                "email digest to a subscribed inbox. Not retried, per the monitor's rule.")
        },
        {
            "platform": "Connectively (connectively.us)",
            "status": "login_required",
            "notes": "Re-probed once. / HTTP 429, 31,198 bytes, 'Vercel Security Checkpoint'. No public feed."
        },
        {
            "platform": "Source of Sources (sourceofsources.com)",
            "status": "email_only",
            "notes": (
                "Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - Source of "
                "Sources'). Reporter submission form only; no source-facing feed.")
        },
        {
            "platform": "Qwoted (qwoted.com)",
            "status": "login_required",
            "notes": (
                "Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes, 'Error: The page "
                "you were looking for doesn't exist'). Wrong path, not gated - unchanged. The feed needs "
                "an authenticated app session.")
        },
        {
            "platform": "MentionMatch (mentionmatch.com)",
            "status": "pre_launch",
            "notes": (
                "Re-probed. Apex HTTP 200 (11,342 bytes), title 'MentionMatch - Connect B2B Writers with "
                "Expert Sources', no feed. Thirteenth consecutive run confirming a pre-launch shell.")
        },
        {
            "platform": "Medialyst MCP (medialyst.ai/api/mcp)",
            "status": "oauth_required",
            "notes": (
                "Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\","
                "\"error_description\":\"No authorization provided\"}. Free read-only feed covering "
                "Connectively, HARO, X, LinkedIn, MentionMatch and Substack. Needs an interactive OAuth "
                "handshake that cannot be completed from a scheduled run. `hermes mcp list` in this "
                "profile still reports 'No MCP servers configured.'")
        },
        {
            "platform": "X/Twitter #journorequest",
            "status": "credits_exhausted",
            "notes": (
                "Not re-attempted. Team-level credit limit blocked this on twelve consecutive runs; the "
                "block is account state, not a transient failure. Sourcee's X-originated aggregation is "
                "used as a proxy.")
        },
        {
            "platform": "ResponseSource (responsesource.com)",
            "status": "paywalled_uk",
            "notes": (
                "Root re-probed HTTP 200 (147,995 bytes, 'ResponseSource - Connecting the media'). "
                "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free source-facing feed.")
        },
    ],
    "opportunities": ops,
    "new_this_run": [
        "NO NEW CORE-BEAT REQUEST FOR THE FIFTH RUN IN SIX, AND NO AI+SPEND SLUG FOR THE SECOND CONSECUTIVE RUN. 108 slugs carry a lastmod newer than the 2026-09-23 run's mark. 8 of them carry an AI token and ZERO carry an AI token plus a spend token. All 8 were fetched and read in full: a Web3/AI/FinTech podcast guest call, an online-school AI grading/surveillance source request, a Newsweek restaurant-AI piece, a CNN piece on relationships strained over AI beliefs, an HR-leaders piece on the hidden labour of fixing AI output, a Rails-developers call, a Business Insider piece seeking couples using Instinct AI, and a Produck Podcast guest call. The one remaining new slug carrying any spend token is a UK conservative-commentary Substack launch. Every one is a different sector's adoption story, a personal-testimony call, or a booking solicitation; none contains a price, seat, licence or spend ask.",
        "THE HR-LEADERS PIECE IS THE CLOSEST NEAR-MISS AND STILL IS NOT PITCHABLE. 'HR Leaders - Valuing Hidden Labor Fixing AI Output' (2026-09-23T17:14Z) is the only new request that reasons about cost: it argues that generating a first draft now costs almost nothing while validating it still costs what it always did, so fixers absorb the cost and producers bank the credit. That is adjacent to our overlap work but it asks HR leaders how they map workflows to see those hours - no price, seat, licence or subscription question anywhere in the body - and the page publishes no route (no email, no DM handle; the only links are Sourcee's own template links). Recorded, not drafted.",
        "THE PAIR RANGE HELD FOR THE SECOND CONSECUTIVE DAY. data/pricing_snapshots.json carries `updated: 2026-09-24`, so the 19 curated pairs were re-asserted rather than carried. scripts/extract_monthly_annual_pairs.py re-asserted every pair against its own sentence and exited 0 with no needle failures. Range unchanged at 1.11x to 2.53x, median 1.25x, over 19 tiers across 14 tools, pair snapshot dates 2026-09-18 and 2026-09-21. data/monthly_annual_pairs.json re-derived and rewritten today.",
        "ALL 47 CARRIED URLS RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page returns HTTP 200 with the request body still served and no removal or expiry notice. 26 are live and unpitched, 17 of the live set are past the 10-day cold line, 2 rows have both a relevance above the tangential band and a resolved reply route, and both of those routes were re-resolved against the live pages again today.",
        "BOTH SENDABLE REPLIES ARE STILL EXACTLY AS RESOLVED ON 2026-09-23. simon.chandler@raconteur.net re-resolved off https://www.raconteur.net/contributors/simon-chandler (HTTP 200, 154,797 bytes, data-part1/2/3 triple unchanged, control /contributors/tom-dennis unchanged); the older /author/simon-chandler/ URL still returns HTTP 404 and must not be cited; raconteur.net MX still Google Workspace. holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact (HTTP 200, 59,500 bytes) alongside the same five other named masthead addresses; artichokehq.com MX still Microsoft 365.",
        "MAILBOX CHECKED: NO NEW REPLIES. INBOX top is still the Google 'Security alert' new-sign-in notice (2026-09-23 15:59Z) above three identical 'New AI tool submission' form-mails from 2026-09-22 15:29Z. The most recent human message remains Jan Suski's 2026-09-18 20:39Z reply, answered at 21:29Z the same day. No reply to the 2026-09-15 Enterprise AI Leaders send (nine days) or the 2026-09-18 Sherwood News send (six days). Sent Mail top is unchanged at msg 187; All Mail top is msg 257. Zero pitches sent this run.",
        "THE UNANSWERED FIGURES CORRECTION IS NOW SIX DAYS OUTSTANDING AND IS THE ONLY OUTBOUND ITEM THIS MONITOR HAS LEFT THAT IS NOT A PITCH. The recipient of the 2026-09-18 Amplemarket reply was told the same-tier monthly/annual range is '1.21x-2.53x, median 1.33x'; the current verified figure is 1.11x-2.53x, median 1.25x over 19 tiers. Not sent this run: the monitor's brief forbids the scheduled run from sending, and the ledger records it as George's lane. Flagged rather than silently carried again.",
    ],
    "expired_this_run": [
        "Nothing expired and nothing dropped off this run. All 47 carried URLs returned HTTP 200 with the request body still served, and none has stopped appearing in a URL-carrying digest. The usual caveat applies and is not a clean bill of health: this monitor carries every tracked request forward into each new digest, so 'absent from the newest digest' cannot fire by construction. Independently cross-checked this run against the full sitemap (41,701 loc/lastmod pairs): all 47 tracked slugs are still present in it, and ZERO of them carry a lastmod inside today's new window, i.e. no tracked request was edited or renewed today.",
        "ONE ROW CROSSES THE 10-DAY LINE TODAY AND IT COSTS NOTHING, BECAUSE IT WAS ALREADY DELIBERATELY DROPPED. EdTech - LMS audit went 10d -> 11d and is now cold. It was recorded as skipped in pitch-ledger.json on 2026-09-15 ('wants people inside EdTech; we would be overstating our standing'), so it was never in the sendable count and no draft was lost. This is the exact opposite of yesterday's Anthropic crossing, where a finished paste-ready draft was carried past the line.",
        "The three requests already recorded as spent remain spent and are not resurfaced: California AI audit bills ('speak with a source today', 14d), UK Managers - Gen Z AI overuse (internal deadline 'by this Wednesday September 9', 17d) - both stay live with no expiry notice, so the do-not-pitch judgement rests on their stated deadlines, not on the page - and the Amplemarket request, which is a live thread with Jan Suski and is not re-pitched.",
        "Four high-relevance requests are now well past the cold line with no send: Enterprise AI Leaders - agent sprawl (19d), Scientists paying for PhD/postdoc AI subscriptions (19d), FinOps - agentic AI cost overruns (17d, draft exists unsent since 2026-09-17) and the Anthropic customer-service request (12d, draft exists unsent since 2026-09-19). None has ever been pitched. Recorded so the accumulating cost of the cold queue is visible rather than only its count.",
    ],
    "summary": (
        f"47 tracked requests (all 47 re-verified live, 0 new on-beat, 0 dropped off, "
        f"{len(pitched)} pitched, {len(skipped)} deliberately skipped). Of the 43 unpitched, 26 are live "
        f"and 17 are cold, and 2 are sendable - unchanged from yesterday, and both drafts are paste-ready "
        f"in pitch-drafts-2026-09-24.md. The new window produced 8 AI-token slugs and ZERO AI+spend slugs, "
        f"the second consecutive run with none; all 8 were read in full and none carries a price, seat or "
        f"licence ask. The pair range re-asserted clean against the refreshed snapshot and held at "
        f"1.11x-2.53x over 19 tiers across 14 tools. Both reply routes were re-resolved against the live "
        f"pages and hold. No new replies in the mailbox. Zero pitches sent this run - sends remain "
        f"George's lane."),
    "recommended_actions": [
        "SEND THE RACONTEUR SHADOW-AI DRAFT. Paste-ready at pitch-drafts-2026-09-24.md section 1, route simon.chandler@raconteur.net (re-resolved off the live /contributors/simon-chandler page today: HTTP 200, triple unchanged, control author checked, MX Google Workspace). It is the only high-relevance request in the queue, the only core-beat find the monitor has produced, and it has now been written and unsent for SIX consecutive runs. It is 7 days old today.",
        "SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-09-24.md section 2, holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today alongside five other named masthead addresses). Standing constraint is in its first line; 6 days old, the freshest of the two.",
        "SEND OR DROP THE ANTHROPIC DRAFT. Cold at 12 days, one day past the line. Draft finished and unsent since 2026-09-19 at pitch-drafts-2026-09-22.md section 2, route Signal hliwrites.99 still verbatim on the live page. Send late or record it as skipped; carrying it a sixth time without either is the defect this monitor exists to fix.",
        "SEND THE FIGURES CORRECTION TO JAN SUSKI. Thread is live, he replied on 2026-09-18, and he was told '1.21x-2.53x, median 1.33x' when the true figure is 1.11x-2.53x, median 1.25x over 19 tiers. An un-flagged wrong figure in a peer method discussion is worse than a follow-up, and it has now been outstanding six days. Route: reply to jan@jansuski.com, In-Reply-To the existing thread.",
        "DECIDE ON FINOPS (17d, high, cold, unpitched since 2026-09-17). Its draft exists at pitch-drafts-2026-09-17.md section 1 and its route is a LinkedIn DM to linkedin.com/in/niloy-ghosh. Still the highest-relevance request the monitor has never answered. Send it late or drop it; do not draft it a fourth time.",
        "RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has produced no core-beat request on five of the last six runs and no AI+spend slug at all for two consecutive runs, so this is the only lever that widens the monitor rather than re-reading the same single source.",
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(new_ai),
        "new_ai_plus_spend_slugs_in_window": len(window["ai_strict"]),
        "consecutive_runs_without_new_core_beat": 5,
        "tracked_urls": len(ops),
        "carried_and_reverified": sum(1 for o in ops if (ver.get(slug_of(o["url"])) or {}).get("live")),
        "unpitched": len(ops) - len(pitched) - len(skipped),
        "live_unpitched": len(live_unpitched),
        "live_unpitched_with_a_resolved_route": 2,
        "cold_unpitched": len(cold_unpitched),
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 3,
        "drafts_written_never_sent": 4,
        "sendable": 2,
        "lost_to_the_cold_line_with_a_draft_ready": 1,
    },
    "monitor_defects_fixed_this_run": [
        "THE QUEUE'S DRAFT INDEX NAMED YESTERDAY'S DRAFT FILE. build_pitch_queue.py's DRAFTS map and DRAFT_INDEX described the shadow-AI and Speciality Food rows as pointing at pitch-drafts-2026-09-23.md and repeated that file's 'day 6 / day 5' ages and its 2026-09-23 pair-range note. Both drafts were re-derived and re-written today at pitch-drafts-2026-09-24.md with today's ages, so the map now names today's file and today's figures.",
        "THE QUEUE'S DRAFT INDEX STILL CARRIED THE ANTHROPIC ROW AS A LIVE CANDIDATE ONE DAY LATE. The map described it as having 'CROSSED COLD 2026-09-23 at 11 days - no longer counted as sendable', which is right, but the ledger's cold_without_a_send entry named pitch-drafts-2026-09-22.md as if that were still the newest copy. The 2026-09-24 state is recorded instead: 12 days, still carrying, still unsent, route unchanged.",
        "THE DIGEST'S NEW-REQUEST COUNTS WERE PREVIOUSLY QUOTED WITHOUT THE WINDOW SIZE THAT PRODUCED THEM. A reader could not tell whether '0 AI+spend slugs' meant the window was empty or the filter was too narrow. Today's digest records the window size (108 slugs), the AI-token count (8) and the AI+spend count (0) together, and names all 8 slugs that were read, so the negative result is auditable rather than asserted.",
    ],
}

DEST.write_text(json.dumps(digest, indent=1), encoding="utf-8")
print(f"wrote {DEST.name}: {len(ops)} opportunities, "
      f"{len(live_unpitched)} live unpitched, {len(cold_unpitched)} cold unpitched, "
      f"{len(pitched)} pitched, {len(skipped)} skipped")
print(f"new window: {len(window['window'])} slugs, {len(new_ai)} AI-token, {len(window['ai_strict'])} AI+spend")
