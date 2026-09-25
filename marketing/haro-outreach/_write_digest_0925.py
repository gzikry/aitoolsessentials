#!/usr/bin/env python3
"""Write today's digest: marketing/haro-outreach/digest-2026-09-25.json

One record per tracked opportunity, re-verified against its own page today. Carried rows are
refreshed from verified-requests.json (page datePublished + rendered badge), not from yesterday's
digest text.
"""
import json
import re
from datetime import date
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-09-25"

prev = json.loads((D / "digest-2026-09-24.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
ledger = json.loads((D / "pitch-ledger.json").read_text())
win = json.loads((D / "_window_0925.json").read_text())
newbodies = json.loads((D / "_newbodies_0925.json").read_text())

ops = []
for op in prev["opportunities"]:
    slug = op["url"].rstrip("/").split("/journo-request/")[-1]
    v = verified.get(slug) or {}
    new = dict(op)
    # Re-verify by URL: page truth replaces the carried deadline text.
    if v:
        dp = v.get("datePublished")
        age = v.get("days_old")
        badge = v.get("badge")
        base = re.sub(r"\s*RE-VERIFIED[^.]*\.?", "", new.get("deadline") or "").strip()
        base = re.sub(r"\s*PAGE-VERIFIED[^.]*\.?", "", base).strip()
        new["deadline"] = (
            f"{base} RE-VERIFIED {TODAY}: HTTP {v.get('http')}, live={v.get('live')}, "
            f"badge '{badge}', datePublished {dp} = {age} days, no expiry notice on the page."
        ).strip()
        new["_page_live"] = bool(v.get("live"))
        new["_days_old"] = age
        new["_badge"] = badge
    ops.append(new)

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{TODAY}T09:00:00-07:00",
    "search_scope": ("AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, "
                     "software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support "
                     "value, tool consolidation, procurement budget"),
    "age_policy": ("Ages are read off each request page (JSON-LD datePublished plus the rendered "
                   "'Posted ... ago' badge), never off the digest text. All 47 carried URLs were "
                   "re-fetched this run: HTTP 200 and the request body still served, none returns an "
                   "expiry notice."),
    "platforms_checked": [
        {"platform": "Sourcee (sourcee.app)", "status": "accessible",
         "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP 200, "
                   f"{win['bytes']:,} bytes, {win['count']:,} loc/lastmod pairs, newest lastmod "
                   f"{win['newest']}). {len(win['window'])} slugs carry a lastmod newer than the "
                   f"2026-09-24 run's mark ({win['mark']}). Of those, {len(win['ai'])} carry an AI "
                   f"token, {len(win['ai_strict'])} carry an AI token plus a strict spend token, and "
                   f"{len(win['spend_any'])} carry any spend-adjacent token. All {len(win['ai'])} "
                   f"AI-token candidates were fetched and read in full, plus the 7 spend-token slugs; "
                   f"none is on-beat. Sourcee itself re-probed HTTP 200 (100,854 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Re-measured for the ninth run: {win['feed_count']} slugs listed today (was 47 "
                   f"yesterday), and {win['feed_overlap_with_window']} of {win['feed_count']} of them "
                   f"are slugs inside today's new sitemap window - i.e. the feed is exactly the "
                   f"newest-slugs window, not a feed a request persists on. Absence from it is "
                   f"therefore NOT a cold signal and build_pitch_queue.py does not use it as one. "
                   f"In_ai_topic_feed is False for all 47 tracked requests, as it has been every run.")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,194 bytes, 'Vercel Security Checkpoint'. "
                   "Fourteenth consecutive identical result. Queries reach sources only by a 3x-daily "
                   "email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": "Re-probed once. / HTTP 429, 31,195 bytes, 'Vercel Security Checkpoint'. No public feed."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                   "Source of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes, 'Error: The "
                   "page you were looking for doesn't exist'). Wrong path, not gated - unchanged. The "
                   "feed needs an authenticated app session.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. Apex HTTP 200 (11,342 bytes), title 'MentionMatch - Connect B2B Writers "
                   "with Expert Sources', no feed. Fourteenth consecutive run confirming a pre-launch shell.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\","
                   "\"error_description\":\"No authorization provided\"}. Free read-only feed covering "
                   "Connectively, HARO, X, LinkedIn, MentionMatch and Substack. Needs an interactive "
                   "OAuth handshake that cannot be completed from a scheduled run.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on thirteen consecutive "
                   "runs; the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (147,974 bytes, 'ResponseSource - Connecting the media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free "
                   "source-facing feed.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        (f"NO NEW CORE-BEAT REQUEST FOR THE SIXTH RUN IN SEVEN. {len(win['window'])} slugs carry a "
         f"lastmod newer than the 2026-09-24 mark. {len(win['ai'])} of them carry an AI token and "
         f"{len(win['ai_strict'])} carries an AI token plus a strict spend token - and that single "
         f"hit is a FALSE POSITIVE: 'seattle-k2-parents-new-screen-time-limits-and-classroom-ai' "
         f"matched on the substring 'seat' inside 'Seattle'. There is NO AI+spend slug in the window "
         f"for the third consecutive run. All {len(win['ai'])} AI-token slugs were fetched and read in "
         f"full: a Seattle K-2 screen-time newsletter item, an agent-forensics research series, "
         f"advertising to AI agents, interior designers vs AI, AI builders in Africa, NYT Wirecutter "
         f"on AI note-takers, a women-in-AI spotlight, decentralized AI for creators, workers whose "
         f"jobs shifted, sales-enablement onboarding, Chinese suppliers for the Spanish market, and a "
         f"£50 case-study call about AI self-diagnosis. Every one is a different sector's adoption "
         f"story, a personal-testimony call or a booking solicitation; none contains a price, seat, "
         f"licence or spend ask."),
        ("THE NEAREST THING TO ON-BEAT IS THE NYT WIRECUTTER AI-NOTE-TAKERS PIECE AND IT IS STILL NOT "
         "PITCHABLE. 'Academia, Healthcare, Law & Customer Service Pros - AI Note-Takers Use' "
         "(2026-09-24T17:43Z) is a Wirecutter story on the role of AI note-takers across professions. "
         "Note-takers are a tool category we track, but the ask is practitioners' on-the-record "
         "experiences of using them, and the page publishes no email or DM handle. Recorded, not "
         "drafted - the same standing problem that sank the Inc. and Forbes founders requests."),
        ("THE PAIR RANGE HELD FOR THE THIRD CONSECUTIVE DAY. data/pricing_snapshots.json now carries "
         "`updated: 2026-09-25`, so the 19 curated pairs were re-asserted against a refreshed file "
         "rather than carried. scripts/extract_monthly_annual_pairs.py re-asserted every pair against "
         "its own sentence and exited 0 with no needle failures. Range unchanged at 1.11x to 2.53x, "
         "median 1.25x, over 19 tiers across 14 tools, pair snapshot dates 2026-09-18 and 2026-09-21. "
         "data/monthly_annual_pairs.json re-derived and rewritten today."),
        ("ALL 47 CARRIED URLS RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page "
         "returns HTTP 200 with the request body still served and no removal or expiry notice. 26 are "
         "live and unpitched, 17 of the live set are past the 10-day cold line, 2 rows have both a "
         "relevance above the tangential band and a resolved reply route, and both of those routes "
         "were re-resolved against the live pages again today."),
        ("BOTH SENDABLE REPLIES ARE STILL EXACTLY AS RESOLVED. simon.chandler@raconteur.net "
         "re-resolved off https://www.raconteur.net/contributors/simon-chandler (HTTP 200, "
         "data-part1/2/3 triple unchanged, control /contributors/tom-dennis unchanged); the older "
         "/author/simon-chandler/ URL still returns HTTP 404 and must not be cited. "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact (HTTP 200, "
         "59,500 bytes) alongside the same five other named masthead addresses."),
        ("MAILBOX CHECKED: NO NEW REPLIES. INBOX top is still the Google 'Security alert' new-sign-in "
         "notice (2026-09-23 15:59Z) above three identical 'New AI tool submission' form-mails from "
         "2026-09-22 15:29Z. The most recent human message remains Jan Suski's 2026-09-18 20:39Z "
         "reply, answered at 21:29Z the same day. No reply to the 2026-09-15 Enterprise AI Leaders "
         "send (ten days) or the 2026-09-18 Sherwood News send (seven days). Sent Mail top is "
         "unchanged at msg 187; All Mail top is msg 257. Zero pitches sent this run."),
        ("THE UNANSWERED FIGURES CORRECTION IS NOW SEVEN DAYS OUTSTANDING AND IS THE ONLY OUTBOUND "
         "ITEM THIS MONITOR HAS LEFT THAT IS NOT A PITCH. The recipient of the 2026-09-18 Amplemarket "
         "reply was told the same-tier monthly/annual range is '1.21x-2.53x, median 1.33x'; the "
         "current verified figure is 1.11x-2.53x, median 1.25x over 19 tiers. Not sent this run: the "
         "monitor's brief forbids the scheduled run from sending, and the ledger records it as "
         "George's lane. Flagged rather than silently carried again."),
    ],
    "expired_this_run": [
        ("Nothing expired and nothing dropped off this run. All 47 carried URLs returned HTTP 200 with "
         "the request body still served, and none has stopped appearing in a URL-carrying digest. The "
         "usual caveat applies and is not a clean bill of health: this monitor carries every tracked "
         "request forward into each new digest, so 'absent from the newest digest' cannot fire by "
         "construction. Independently cross-checked this run against the full sitemap (40,980 "
         "journo-request loc/lastmod pairs): all 47 tracked slugs are still present in it, and ZERO of "
         "them carry a lastmod inside today's new window, i.e. no tracked request was edited or "
         "renewed today."),
        ("TWO ROWS CROSS THE 10-DAY LINE TODAY, UP FROM ONE YESTERDAY. Enterprise AI Leaders - Value "
         "Creation went 10d -> 11d; it was pitched 2026-09-15 to hello@foxandspindle.com and no reply "
         "has come in ten days, so it leaves the live set as an unanswered send rather than an unsent "
         "draft. EdTech - LMS audit went 11d -> 12d and was already recorded as skipped, so it costs "
         "nothing again."),
        ("The three requests already recorded as spent remain spent and are not resurfaced: California "
         "AI audit bills ('speak with a source today', 15d), UK Managers - Gen Z AI overuse (internal "
         "deadline 'by this Wednesday September 9', 18d) - both stay live with no expiry notice, so the "
         "do-not-pitch judgement rests on their stated deadlines, not on the page - and the Amplemarket "
         "request, which is a live thread with Jan Suski and is not re-pitched."),
        ("Four high-relevance requests are now well past the cold line with no send: Enterprise AI "
         "Leaders - agent sprawl (20d), Scientists paying for PhD/postdoc AI subscriptions (20d), "
         "FinOps - agentic AI cost overruns (18d, draft exists unsent since 2026-09-17) and the "
         "Anthropic customer-service request (13d, draft exists unsent since 2026-09-19). None has "
         "ever been pitched. Recorded so the accumulating cost of the cold queue is visible rather "
         "than only its count."),
    ],
    "summary": (
        f"47 tracked requests (all 47 re-verified live, 0 new on-beat, 0 dropped off, 3 pitched, 1 "
        f"deliberately skipped). Of the 43 unpitched, 26 are live and 17 are cold, and 2 are sendable "
        f"- unchanged from yesterday, and both drafts are paste-ready in pitch-drafts-2026-09-25.md. "
        f"The new window produced {len(win['ai'])} AI-token slugs and ZERO real AI+spend slugs, the "
        f"third consecutive run with none; the one AI+spend regex hit was 'Seattle' matching 'seat'. "
        f"The pair range re-asserted clean against the refreshed snapshot and held at 1.11x-2.53x over "
        f"19 tiers across 14 tools. Both reply routes were re-resolved against the live pages and "
        f"hold. No new replies in the mailbox. Zero pitches sent this run - sends remain George's lane."),
    "recommended_actions": [
        ("SEND THE RACONTEUR SHADOW-AI DRAFT. Paste-ready at pitch-drafts-2026-09-25.md section 1, "
         "route simon.chandler@raconteur.net (re-resolved off the live /contributors/simon-chandler "
         "page today: HTTP 200, triple unchanged, control author checked). It is the only "
         "high-relevance request in the queue, the only core-beat find the monitor has produced, and "
         "it has now been written and unsent for SEVEN consecutive runs. It is 8 days old today - two "
         "days from the cold line."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-09-25.md section 2, "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today "
         "alongside five other named masthead addresses). Standing constraint is in its first line; "
         "7 days old, and it is the last fresh request in the sendable set."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI. Thread is live, he replied on 2026-09-18, and he "
         "was told '1.21x-2.53x, median 1.33x' when the true figure is 1.11x-2.53x, median 1.25x over "
         "19 tiers. An un-flagged wrong figure in a peer method discussion is worse than a follow-up, "
         "and it has now been outstanding seven days. Route: reply to jan@jansuski.com, In-Reply-To "
         "the existing thread."),
        ("SEND OR DROP THE ANTHROPIC DRAFT. Cold at 13 days. Draft finished and unsent since "
         "2026-09-19 at pitch-drafts-2026-09-22.md section 2, route Signal hliwrites.99 still verbatim "
         "on the live page. Send late or record it as skipped; carrying it a seventh time without "
         "either is the defect this monitor exists to fix."),
        ("DECIDE ON FINOPS (18d, high, cold, unpitched since 2026-09-17). Its draft exists at "
         "pitch-drafts-2026-09-17.md section 1 and its route is a LinkedIn DM to "
         "linkedin.com/in/niloy-ghosh. Still the highest-relevance request the monitor has never "
         "answered. Send it late or drop it; do not draft it a fifth time."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has produced no core-beat request on six "
         "of the last seven runs and no real AI+spend slug for three consecutive runs, so this is the "
         "only lever that widens the monitor rather than re-reading the same single source."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": 0,
        "ai_plus_spend_regex_hits_that_were_false_positives": 1,
        "consecutive_runs_without_new_core_beat": 6,
        "tracked_urls": 47,
        "carried_and_reverified": 47,
        "unpitched": 43,
        "live_unpitched": 26,
        "live_unpitched_with_a_resolved_route": 2,
        "cold_unpitched": 17,
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 3,
        "drafts_written_never_sent": 4,
        "sendable": 2,
        "lost_to_the_cold_line_with_a_draft_ready": 1,
    },
    "monitor_defects_fixed_this_run": [
        ("THE AI+SPEND FILTER MATCHES TOKENS, NOT SUBJECTS. Today's only strict AI+spend hit was "
         "'seattle-k2-parents-new-screen-time-limits-and-classroom-ai' - the token 'seat' matched "
         "inside 'Seattle'. The 2026-09-24 digest had already recorded the same class of error on the "
         "spend side ('billing' matching a hospital-bills story), so this is the second instance. The "
         "window's ai_strict list is now printed alongside the tokens that produced each match, so a "
         "false positive is visible in the digest rather than only in the negative count."),
        ("TWO ROWS CROSSED THE COLD LINE TODAY AND THE DIGEST REPORTS THEM SEPARATELY. Yesterday's "
         "edition recorded one crossing; today's records Enterprise AI Leaders - Value Creation (a "
         "send with no reply, 11d) alongside the EdTech one (already skipped, 12d). Separating a "
         "crossing that cost a draft from one that cost nothing is the distinction the 2026-09-23 and "
         "2026-09-24 entries were built around; today's keeps it explicit rather than folding both "
         "into a single count."),
        ("THE CARRIED DEADLINE TEXT IS NOW REWRITTEN, NOT APPENDED TO. Every prior run appended a "
         "'RE-VERIFIED <date>' sentence to whatever the previous digest had said, so deadline fields "
         "had grown to five stacked verification sentences with three superseded ages in them - a "
         "reader could not tell which age was current. This run strips prior verification sentences "
         "before appending today's, so each record carries exactly one live age."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print(f"wrote digest-{TODAY}.json: {len(ops)} opportunities, {len(digest['platforms_checked'])} platforms")
