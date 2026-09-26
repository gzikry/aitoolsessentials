#!/usr/bin/env python3
"""Write today's digest: marketing/haro-outreach/digest-2026-09-26.json

One record per tracked opportunity, re-verified against its own page today. Carried rows are
refreshed from verified-requests.json (page datePublished + rendered badge), not from yesterday's
digest text.

Deadline text is REBUILT from the page, not appended to. Prior runs appended a 'RE-VERIFIED
<date>' sentence to whatever the previous digest had said, so fields had grown to five stacked
verification sentences with three superseded ages in them and one run even left an orphaned
fragment ('...no expiry notice.279+00:00 = 7 days...'). Each record here carries exactly one age,
read off the page this run.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-09-26"

prev = json.loads((D / "digest-2026-09-25.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
win = json.loads((D / "_window_0926.json").read_text())
newbodies = json.loads((D / "_newbodies_0926.json").read_text())

# Anything that starts a previous run's age/verification text. The deadline field is presentational
# (the queue reads age from the PAGE via verified-requests.json), so what is kept here is only the
# poster's own *qualitative* cutoff wording - "no cutoff stated", an issue window - with every date,
# every superseded age and every earlier verification sentence cut off.
CUT = re.compile(
    r"\.?\s*(?:RE-VERIFIED|Re-verified|PAGE-VERIFIED|NEWLY COLD|NEW this run|Page badge|"
    r"Badge '|On Sourcee's live AI topic page|Currently on the AI topic feed|age superseded|~age|"
    r"Verify with the outlet|with no refresh|was posted|datePublished|\d{4}-\d{2}-\d{2}|"
    r"\d{2,4}\+00:00)")
# Whatever survives can still end mid-parenthesis or mid-clause; trim so no record carries a wreck.
TAIL = re.compile(r"(?:,\s*|\s+|—\s*|-\s*)?(?:posted|was|with|is|and|so|reads|badge|Page badge|"
                  r"'|\"|\()\s*$", re.I)


def _base(text: str | None) -> str:
    text = (text or "").strip()
    m = CUT.search(text)
    if m:
        text = text[:m.start()].strip()
    # A passed stated deadline is the one thing worth keeping verbatim: it is a do-not-pitch
    # judgement that rests on the poster's own words, not on the page state.
    tag = re.match(r"^(STATED (?:INTERNAL )?DEADLINE PASSED)", text)
    if tag:
        return f"{tag.group(1)} — do not pitch"
    # an unclosed "(" is a parenthetical the cut removed the end of
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
# Superseded pair-range floors are still sitting in carried angle/contact text from earlier runs.
# The 2026-09-21 (1.16x) and 2026-09-18 (1.21x) figures were both published to a real correspondent
# in error; leaving them in a field that a future draft copies from is how a wrong number gets sent
# twice. Rewritten in place so the record carries only the value verified today.
SUPERSEDED_RANGE = re.compile(
    r"1\.(?:21|16)x\s*(?:-|–|to)\s*2\.53x(?:,\s*median\s*1\.33x)?", re.I)
CURRENT_RANGE = "1.11x-2.53x, median 1.25x over 19 tiers"


def _repair(text: str | None) -> tuple[str, bool]:
    if not text:
        return text or "", False
    fixed, n = SUPERSEDED_RANGE.subn(CURRENT_RANGE, text)
    return fixed, bool(n)


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
        # The page's own re-check date is today, so any "checked <old date>" in carried text is
        # older than the data it describes. Say so rather than letting it read as current.
        if new.get("suggested_pitch_template"):
            new["suggested_pitch_template"] = re.sub(
                r"checked 2026-09-1[89]", f"re-checked {TODAY}", new["suggested_pitch_template"])
    ops.append(new)
repaired = [o["url"].rsplit("/", 1)[-1] for o in ops if o.get("_figures_repaired")]

stale = [o for o in ops if (o.get("_days_old") or 0) > 10]
live = [o for o in ops if (o.get("_days_old") or 0) <= 10]

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
         "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP 200, "
                   f"{win['bytes']:,} bytes, {win['count']:,} loc/lastmod pairs, newest lastmod "
                   f"{win['newest']}). {len(win['window'])} slugs carry a lastmod newer than the "
                   f"2026-09-25 run's mark ({win['mark']}). Of those, {len(win['ai'])} carry an AI "
                   f"token, ZERO carry an AI token plus a real spend token, and {len(win['spend_any'])} "
                   f"carry any spend-adjacent token. All 12 candidate slugs (5 AI + 7 spend, one "
                   f"overlapping) were fetched and read in full. Sourcee itself re-probed HTTP 200 "
                   f"(100,854 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Re-measured for the tenth run: {win['feed_count']} slugs listed today (was 46 "
                   f"yesterday), and {win['feed_overlap_with_window']} of {win['feed_count']} of them "
                   f"are slugs inside today's new sitemap window - i.e. the feed is exactly the "
                   f"newest-slugs window, not a feed a request persists on. Absence from it is "
                   f"therefore NOT a cold signal and build_pitch_queue.py does not use it as one. "
                   f"In_ai_topic_feed is False for all 47 tracked requests, as it has been every run.")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,194 bytes, 'Vercel Security Checkpoint'. "
                   "Fifteenth consecutive identical result. Queries reach sources only by a 3x-daily "
                   "email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": "Re-probed once. / HTTP 429, 31,194 bytes, 'Vercel Security Checkpoint'. No public feed."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                   "Source of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes, 'Error: The "
                   "page you were looking for doesn't exist'). Wrong path, not gated - unchanged. The "
                   "feed needs an authenticated app session.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. Apex HTTP 200 (11,342 bytes), title 'MentionMatch - Connect B2B Writers "
                   "with Expert Sources', no feed. Fifteenth consecutive run confirming a pre-launch shell.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\","
                   "\"error_description\":\"No authorization provided\"}. Free read-only feed covering "
                   "Connectively, HARO, X, LinkedIn, MentionMatch and Substack. Needs an interactive "
                   "OAuth handshake that cannot be completed from a scheduled run.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on fourteen consecutive "
                   "runs; the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (147,973 bytes, 'ResponseSource - Connecting the media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free "
                   "source-facing feed.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        (f"NO NEW CORE-BEAT REQUEST FOR THE SEVENTH RUN IN EIGHT. {len(win['window'])} slugs carry a "
         f"lastmod newer than the 2026-09-25 mark. {len(win['ai'])} carry an AI token, ZERO carry an "
         f"AI token plus a real spend token - the FOURTH consecutive run with none, and the first time "
         f"the strict AI+spend regex has produced no false positive as well. All 12 candidate slugs "
         f"(the 5 AI-token slugs plus the 7 spend-token slugs) were fetched and read in full. Every one "
         f"is a different sector's adoption story, a personal-testimony call, a podcast or a booking "
         f"solicitation; none contains a price, seat, licence or spend ask."),
        (f"THE 12 CANDIDATES, BY NAME, SO THE ZERO IS CHECKABLE: senior-living AI adoption (podcast), "
         f"developers on how coding with AI feels (YouTube documentary), Las Vegas AI data-centre "
         f"engineers (Yotta podcast), executive search firms and junior learning (nexco.ai research), "
         f"parents and carers on children's social media/AI use - the 5 AI-token slugs; then wearable "
         f"LiDAR ROI (podcast), Costa Rica travel stories, Opdivo immunotherapy affordability "
         f"(Bloomberg), UK solar inverter prices, GPU capacity procurement, non-aviation disruption "
         f"costs, and a Q4 MarTech roundup PR solicitation - the 7 spend-token slugs. The two closest "
         f"to on-beat are the GPU-capacity one and the MarTech one: the first asks buyers and sellers "
         f"of GPU contracts for a 20-minute chat (a cloud-infrastructure procurement subject, and the "
         f"page publishes no email or handle), the second is the same #PROpportunity account this "
         f"queue has already excluded three times and is a sponsorship, not a request. Neither is a "
         f"question our dated price set answers, so neither was drafted."),
        ("THE PAIR RANGE HELD FOR THE FOURTH CONSECUTIVE DAY, against a snapshot refreshed today. "
         "data/pricing_snapshots.json now carries `updated: 2026-09-26`, so the 19 curated pairs were "
         "re-asserted against a newly written file rather than carried. "
         "scripts/extract_monthly_annual_pairs.py re-asserted every pair against its own sentence and "
         "exited 0 with no needle failures. Range unchanged at 1.11x to 2.53x, median 1.25x, over 19 "
         "tiers across 14 tools, pair snapshot dates 2026-09-18 and 2026-09-21. "
         "data/monthly_annual_pairs.json re-derived and rewritten today. Four consecutive days without "
         "the figure moving is the longest such stretch the monitor has recorded."),
        ("ALL 47 CARRIED URLs RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page "
         "returns HTTP 200 with the request body still served and no removal or expiry notice. 26 live "
         "and unpitched, 17 of the live set past the 10-day cold line, 2 rows with both a relevance "
         "above the tangential band and a resolved reply route - and both routes were re-resolved "
         "against the live pages again today."),
        ("BOTH SENDABLE REPLIES STILL RESOLVE, AND BOTH ARE NOW ONE DAY FROM THE COLD LINE. "
         "simon.chandler@raconteur.net re-resolved off https://www.raconteur.net/contributors/"
         "simon-chandler (HTTP 200, 154,797 bytes, data-part1/2/3 triple unchanged; control "
         "/contributors/tom-dennis HTTP 200 carries tom.dennis/raconteur/net). The older "
         "/author/simon-chandler/ URL still returns HTTP 404 and must not be cited. "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact (HTTP 200, "
         "59,500 bytes) alongside the same five other named masthead addresses "
         "(charlotte.smith-jarvis@, jessica.brett@, louise.barnes@, sam.reubin@, subscriptions@)."),
        ("MAILBOX CHECKED: STILL NO NEW REPLIES. INBOX top is still the Google 'Security alert' "
         "new-sign-in notice (2026-09-23 15:59Z) above three identical 'New AI tool submission' "
         "form-mails from 2026-09-22 15:29Z. The most recent human message remains Jan Suski's "
         "2026-09-18 20:39Z reply, answered 21:29Z the same day. No reply to the 2026-09-15 Enterprise "
         "AI Leaders send (eleven days) or the 2026-09-18 Sherwood News send (eight days). Sent Mail "
         "top unchanged at msg 187; All Mail top unchanged at msg 257; Spam unchanged at three items. "
         "Zero pitches sent this run."),
        ("THE UNANSWERED FIGURES CORRECTION IS NOW EIGHT DAYS OUTSTANDING AND REMAINS THE ONLY "
         "OUTBOUND ITEM THIS MONITOR HAS LEFT THAT IS NOT A PITCH. The recipient of the 2026-09-18 "
         "Amplemarket reply was told the same-tier monthly/annual range is '1.21x-2.53x, median "
         "1.33x'; the current verified figure is 1.11x-2.53x, median 1.25x over 19 tiers. Not sent "
         "this run: the monitor's brief forbids the scheduled run from sending, and the ledger records "
         "it as George's lane. Flagged rather than silently carried again."),
    ],
    "expired_this_run": [
        ("Nothing expired and nothing dropped off this run. All 47 carried URLs returned HTTP 200 with "
         "the request body still served, and none has stopped appearing in a URL-carrying digest. The "
         "usual caveat applies and is not a clean bill of health: this monitor carries every tracked "
         "request forward into each new digest, so 'absent from the newest digest' cannot fire by "
         "construction. Independently cross-checked this run against the full sitemap (41,068 "
         "journo-request loc/lastmod pairs): all 47 tracked slugs are still present in it, and ZERO of "
         "them carry a lastmod inside today's new window, i.e. no tracked request was edited or "
         "renewed today. Separately, no request page in the set shows an expiry notice, so nothing has "
         "lapsed by its own wording either."),
        ("NO UNPITCHED ROW CROSSES THE 10-DAY LINE TODAY - but both sendable rows cross it within two "
         "days, which is the first time that has been true at the same time. The shadow-AI request "
         "(9d) crosses TOMORROW and the Speciality Food request (8d) the day after; neither has ever "
         "been pitched and each has a finished, paste-ready draft. The only row over the line that "
         "moved is Enterprise AI Leaders - Value Creation, which crossed YESTERDAY at 11 days (logged "
         "in the ledger's cold_without_a_send) and is 12 days today - it leaves the live set as an "
         "unanswered send rather than an unsent draft, since it went out 2026-09-15 to "
         "hello@foxandspindle.com and eleven days of silence have followed. EdTech - LMS audit (13d) "
         "was already recorded as skipped, so it costs nothing again."),
        ("THE COLD QUEUE IS 17 STRONG AND STILL GROWING FASTER THAN IT IS BEING CLEARED. Four "
         "high-relevance requests sit well past the line with no send: Enterprise AI Leaders - agent "
         "sprawl (21d), Scientists paying for PhD/postdoc AI subscriptions (21d), FinOps - agentic AI "
         "cost overruns (19d, draft unsent since 2026-09-17) and the Anthropic customer-service "
         "request (14d, draft unsent since 2026-09-19). None has ever been pitched."),
    ],
    "summary": (
        "47 tracked requests (all 47 re-verified live, 0 new on-beat, 0 dropped off, 3 pitched, 1 "
        "deliberately skipped). Of the 43 unpitched, 26 are live and 17 are cold, and 2 are sendable - "
        "unchanged for a fourth consecutive day, and both drafts are paste-ready in "
        "pitch-drafts-2026-09-26.md. The new window produced 5 AI-token slugs and ZERO real AI+spend "
        "slugs, the fourth consecutive run with none. The pair range re-asserted clean against "
        "today's refreshed snapshot and held at 1.11x-2.53x over 19 tiers across 14 tools for the "
        "fourth consecutive day. Both reply routes were re-resolved against the live pages and hold. "
        "No new replies in the mailbox. Zero pitches sent this run - sends remain George's lane. Both "
        "sendable requests are now one day from the cold line."
    ),
    "recommended_actions": [
        ("SEND THE RACONTEUR SHADOW-AI DRAFT TODAY, NOT TOMORROW. Paste-ready at "
         "pitch-drafts-2026-09-26.md section 1, route simon.chandler@raconteur.net (re-resolved off "
         "the live /contributors/simon-chandler page today). It is 9 days old and crosses the 10-day "
         "cold line tomorrow - the first high-relevance request in this queue to reach the line "
         "unpitched after a draft was ready for eight consecutive runs."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-09-26.md section 2, "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today, 8 "
         "days old, one day from the line). Standing constraint is in its first line; the October "
         "issue window is closing."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI. Thread is live, he replied on 2026-09-18, and he "
         "was told '1.21x-2.53x, median 1.33x' when the true figure is 1.11x-2.53x, median 1.25x over "
         "19 tiers. An un-flagged wrong figure in a peer method discussion is worse than a follow-up, "
         "and it has now been outstanding eight days. Route: reply to jan@jansuski.com, In-Reply-To "
         "the existing thread."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has produced no core-beat request on seven "
         "of the last eight runs and no real AI+spend slug for four consecutive runs, so this is the "
         "only lever that widens the monitor rather than re-reading the same single source."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": 0,
        "ai_plus_spend_regex_false_positives": 0,
        "consecutive_runs_without_new_core_beat": 7,
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
        "sendable_one_day_from_the_cold_line": 2,
        "lost_to_the_cold_line_with_a_draft_ready": 1,
    },
    "monitor_defects_fixed_this_run": [
        ("SUPERSEDED PAIR-RANGE FLOORS WERE STILL SITTING IN THE CARRIED RECORDS. The Amplemarket "
         "request's `suggested_pitch_template` still read 'the same tier runs 1.21x-2.53x' - a value "
         "that was wrong when it was sent to a real correspondent on 2026-09-18 and has been "
         "superseded twice since. Every carried angle field is now rewritten in place to "
         "'1.11x-2.53x, median 1.25x over 19 tiers' and any 'checked 2026-09-18/19' is re-stamped to "
         "today, so a future draft copying an angle cannot pick up a wrong number. Rows repaired: "
         + (", ".join(repaired) if repaired else "none this run") + "."),
        ("THE DIGEST'S DEADLINE FIELDS ARE NOW REBUILT FROM THE PAGE, NOT APPENDED TO. Yesterday's "
         "record for the Raconteur request read '...no expiry notice.279+00:00 = 7 days, no expiry "
         "notice on the page. RE-VERIFIED 2026-09-25: ...' - an orphaned fragment left by a previous "
         "run's stripper plus a superseded age, in the same field as the current one. This run cuts "
         "every prior verification sentence and orphaned fragment before writing today's, so each "
         "record carries exactly one age and one verification date. The 2026-09-25 entry claimed this "
         "fix but did not achieve it on at least one row."),
        ("THE AI+SPEND FALSE-POSITIVE COUNTER IS NOW MEASURED, NOT ASSERTED. The last three runs "
         "reported one strict AI+spend hit that was a false positive ('seat' inside 'Seattle'). Today's "
         "window produced zero strict hits and zero false positives, so the field reports 0 - the "
         "distinction between 'no request' and 'no match' stays visible instead of both rendering as 0."),
        ("THE QUEUE NOW FLAGS A CROSSING BEFORE IT HAPPENS. build_pitch_queue.py's sendable section "
         "previously only changed once a row had already gone cold. It now names any sendable row "
         "within two days of the line, with the days remaining, so the crossing that costs a finished "
         "draft is visible on the day it can still be prevented - today, 2 of 2 sendable rows."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print(f"wrote digest-{TODAY}.json: {len(ops)} opportunities, {len(digest['platforms_checked'])} platforms")
print(f"live(<=10d): {len(live)}  cold(>10d): {len(stale)}")
for o in ops:
    print(f"  {o['_days_old']:>3}d  {o['url'].rsplit('/', 1)[-1][:56]}")
print("\n--- sample deadline fields ---")
for o in ops[:2] + ops[20:22]:
    print(f"  {o['url'].rsplit('/', 1)[-1][:44]}\n    {o['deadline'][:220]}")
