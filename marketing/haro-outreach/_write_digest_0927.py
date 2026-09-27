#!/usr/bin/env python3
"""Write today's digest: marketing/haro-outreach/digest-2026-09-27.json

One record per tracked opportunity, re-verified against its own page today. Carried rows are
refreshed from verified-requests.json (page datePublished + rendered badge), not from yesterday's
digest text.

Deadline text is REBUILT from the page, not appended to. Each record carries exactly one age,
read off the page this run.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-09-27"

prev = json.loads((D / "digest-2026-09-26.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
win = json.loads((D / "_window_0927.json").read_text())
newbodies = json.loads((D / "_newbodies_0927.json").read_text())

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
        if new.get("suggested_pitch_template"):
            new["suggested_pitch_template"] = re.sub(
                r"checked 2026-09-1[89]", f"re-checked {TODAY}", new["suggested_pitch_template"])
    ops.append(new)
repaired = [o["url"].rsplit("/", 1)[-1] for o in ops if o.get("_figures_repaired")]

stale = [o for o in ops if (o.get("_days_old") or 0) > 10]
live = [o for o in ops if (o.get("_days_old") or 0) <= 10]

# Every row that moved from live to cold in this run, named rather than left as a count change.
CROSSED = ("cybersecurity-companies-and-experts-ai-scams-and-consumer-safety",
           "us-founders-calls-to-slow-ai-development-impact-on-companies")

ledger = json.loads((D / "pitch-ledger.json").read_text())
done = set()
for u in list(ledger.get("pitched", {})) + list(ledger.get("skipped", {})):
    done.add(u.rstrip("/").split("/journo-request/")[-1])
live_unp = [o for o in live if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]
cold_unp = [o for o in stale if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]

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
                   f"2026-09-26 run's mark ({win['mark']}). Of those, {len(win['ai'])} carry an AI "
                   f"token, ZERO carry an AI token plus a real spend token, and {len(win['spend_any'])} "
                   f"carry any spend-adjacent token. All 4 candidate slugs (2 AI + 2 spend, none "
                   f"overlapping) were fetched and read in full. Sourcee itself re-probed HTTP 200 "
                   f"(100,854 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Re-measured for the eleventh run, and yesterday's sharper claim is CORRECTED "
                   f"here: {win['feed_count']} slugs listed today, and only "
                   f"{win['feed_overlap_with_window']} of {win['feed_count']} sit inside today's new "
                   f"sitemap window. The other 7 carry lastmods from 2026-09-25 (one from "
                   f"2026-09-26T01:22Z, six from 2026-09-25 evening) - so the feed is a recency "
                   f"window over roughly the newest two days, NOT byte-exactly today's window as the "
                   f"2026-09-26 digest asserted ('42 of 42'). The conclusion it was used to support is "
                   f"unchanged and now rests on the correct measurement: absence from this feed is "
                   f"still not a cold signal, because all 47 tracked requests are absent from it by "
                   f"construction (in_ai_topic_feed is False for all 47 again this run).")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,199 bytes, 'Vercel Security Checkpoint'. "
                   "Sixteenth consecutive identical result. Queries reach sources only by a 3x-daily "
                   "email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
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
         "notes": ("Re-probed. Apex HTTP 200 (11,342 bytes), title 'MentionMatch - Connect B2B Writers "
                   "with Expert Sources', no feed. Sixteenth consecutive run confirming a pre-launch shell.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\","
                   "\"error_description\":\"No authorization provided\"}. Free read-only feed covering "
                   "Connectively, HARO, X, LinkedIn, MentionMatch and Substack. Needs an interactive "
                   "OAuth handshake that cannot be completed from a scheduled run.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on fifteen consecutive "
                   "runs; the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (147,975 bytes, 'ResponseSource - Connecting the media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free "
                   "source-facing feed.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        (f"NO NEW CORE-BEAT REQUEST FOR THE EIGHTH RUN IN NINE. {len(win['window'])} slugs carry a "
         f"lastmod newer than the 2026-09-26 mark. {len(win['ai'])} carry an AI token, ZERO carry an "
         f"AI token plus a real spend token - the FIFTH consecutive run with none. The window is "
         f"smaller than usual (46 vs 88 yesterday), and so is the candidate set: all 4 candidates "
         f"(the 2 AI-token slugs plus the 2 spend-token slugs) were fetched and read in full. Every "
         f"one is a different sector's adoption story or a personal-testimony call; none contains a "
         f"price, seat, licence or spend ask."),
        (f"THE 4 CANDIDATES, BY NAME, SO THE ZERO IS CHECKABLE: TMU Creative School first- and "
         f"second-years on CSE100 AI use (a student newspaper asking its own classmates - "
         f"theeyeopener.com, 'reply to this post or send me a PM', and it is a 10-15 minute call "
         f"scheduled before Wednesday Sept 30th); a business school career expert on employers' view "
         f"of human skills as AI spreads (journalist Alyshia Hull, two questions, 'By Monday', "
         f"address redacted) - the 2 AI-token slugs; then nurses/physicians/EMTs on the human cost of "
         f"healthcare (a nonfiction-book questionnaire) and freelancers in Amsterdam on going solo, "
         f"boundaries and invoices (a newsletter) - the 2 spend-token slugs. The business-school one "
         f"is on AI at work but asks for a career-services professional's view, which we are not; the "
         f"Amsterdam one carries 'invoices' as its only spend token and is off-beat. Neither is a "
         f"question our dated price set answers, so neither was drafted."),
        ("THE PAIR RANGE HELD FOR THE FIFTH CONSECUTIVE DAY, against a snapshot refreshed today. "
         "data/pricing_snapshots.json now carries `updated: 2026-09-27`, so the 19 curated pairs were "
         "re-asserted against a newly written file rather than carried. "
         "scripts/extract_monthly_annual_pairs.py re-asserted every pair against its own sentence and "
         "exited 0 with no needle failures. Range unchanged at 1.11x to 2.53x, median 1.25x, over 19 "
         "tiers across 14 tools, pair snapshot dates 2026-09-18 and 2026-09-21. "
         "data/monthly_annual_pairs.json re-derived and rewritten today ('built: 2026-09-27'). Five "
         "consecutive days without the figure moving is the longest such stretch the monitor has "
         "recorded."),
        ("ALL 47 CARRIED URLs RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page "
         "returns HTTP 200 with the request body still served and no removal or expiry notice. 24 "
         "live and unpitched (down from 26 - two rows crossed the 10-day line today), 19 cold, and 2 "
         "rows with both a relevance above the tangential band and a resolved reply route - and both "
         "routes were re-resolved against the live pages again today."),
        ("BOTH SENDABLE REPLIES STILL RESOLVE, AND ONE OF THEM IS ON ITS LAST DAY. "
         "simon.chandler@raconteur.net re-resolved off https://www.raconteur.net/contributors/"
         "simon-chandler (HTTP 200, 154,797 bytes, data-part1/2/3 triple unchanged at "
         "simon.chandler + raconteur + net; control /contributors/tom-dennis HTTP 200 carries "
         "tom.dennis/raconteur/net). The older /author/simon-chandler/ URL still returns HTTP 404 and "
         "must not be cited. holly.shackleton@artichokehq.com re-read off "
         "specialityfoodmagazine.com/contact (HTTP 200, 59,500 bytes) alongside the same five other "
         "named masthead addresses (charlotte.smith-jarvis@, jessica.brett@, louise.barnes@, "
         "sam.reubin@, subscriptions@)."),
        ("MAILBOX CHECKED: STILL NO NEW REPLIES TO ANY PITCH. One new message since yesterday and it "
         "is not a pitch reply: SaaSHub Stan (2026-09-27 13:17Z, msg 82/258) reporting "
         "AIToolsEssentials is #1,321 in the SaaSHub approval queue, with a Priority+ upsell. The most "
         "recent human message remains Jan Suski's 2026-09-18 20:39Z reply, answered 21:29Z the same "
         "day. No reply to the 2026-09-15 Enterprise AI Leaders send (twelve days) or the 2026-09-18 "
         "Sherwood News send (nine days). Sent Mail top unchanged at msg 187; All Mail top now msg "
         "258; Spam unchanged at three items. Zero pitches sent this run."),
        ("THE UNANSWERED FIGURES CORRECTION IS NOW NINE DAYS OUTSTANDING AND REMAINS THE ONLY "
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
         "construction. Independently cross-checked this run against the full sitemap (41,114 "
         "journo-request loc/lastmod pairs): all 47 tracked slugs are still present in it, and ZERO of "
         "them carry a lastmod inside today's new window, i.e. no tracked request was edited or "
         "renewed today. Separately, no request page in the set shows an expiry notice, so nothing has "
         "lapsed by its own wording either."),
        ("TWO ROWS CROSSED THE 10-DAY LINE TODAY, BOTH LOW RELEVANCE AND BOTH UNPITCHED - neither is "
         "a lost draft, and neither was flagged in advance: cybersecurity-companies-and-experts-ai-"
         "scams-and-consumer-safety (10d to 11d) and us-founders-calls-to-slow-ai-development-impact-"
         "on-companies (10d to 11d). No draft existed for either and neither has ever had a resolved "
         "route, so nothing sendable was lost. They are named here because build_pitch_queue.py's "
         "advance warning only covers sendable rows, so a low-relevance crossing otherwise shows up "
         "as nothing but a live-count change."),
        ("THE SHADOW-AI REQUEST IS AT 10 DAYS AND THIS IS ITS LAST LIVE DAY. It crosses the cold line "
         "tomorrow. It is the only high-relevance request that has ever sat in this queue with a "
         "finished draft, and the draft has now been written and unsent for NINE consecutive runs "
         "(`pitch-drafts-2026-09-26.md` section 1, route simon.chandler@raconteur.net, re-resolved "
         "today). If it crosses unpitched it becomes the first high-relevance request this queue has "
         "lost to the line with a paste-ready draft sitting ready. The Speciality Food request (9d) "
         "crosses the day after, and its October issue window is closing."),
        ("THE COLD QUEUE IS 19 STRONG AND STILL GROWING FASTER THAN IT IS BEING CLEARED. Four "
         "high-relevance requests sit well past the line with no send: Enterprise AI Leaders - agent "
         "sprawl (22d), Scientists paying for PhD/postdoc AI subscriptions (22d), FinOps - agentic AI "
         "cost overruns (20d, draft unsent since 2026-09-17) and the Anthropic customer-service "
         "request (15d, draft unsent since 2026-09-19). None has ever been pitched."),
    ],
    "summary": (
        "47 tracked requests (all 47 re-verified live, 0 new on-beat, 0 dropped off, 3 pitched, 1 "
        "deliberately skipped). Of the 43 unpitched, 24 are live and 19 are cold, and 2 are sendable "
        "- both drafts paste-ready in pitch-drafts-2026-09-26.md (unchanged figures, re-verified "
        "today). The new window produced 2 AI-token slugs and ZERO real AI+spend slugs, the fifth "
        "consecutive run with none. The pair range re-asserted clean against today's refreshed "
        "snapshot and held at 1.11x-2.53x over 19 tiers across 14 tools for the fifth consecutive "
        "day. Both reply routes were re-resolved against the live pages and hold. No new replies in "
        "the mailbox (the one new message is a SaaSHub queue notice). Zero pitches sent this run - "
        "sends remain George's lane. The shadow-AI request is on its last live day."
    ),
    "recommended_actions": [
        ("SEND THE RACONTEUR SHADOW-AI DRAFT TODAY - THIS IS THE LAST DAY IT IS LIVE. Paste-ready at "
         "pitch-drafts-2026-09-26.md section 1, route simon.chandler@raconteur.net (re-resolved off "
         "the live /contributors/simon-chandler page today). It is 10 days old and crosses the 10-day "
         "cold line tomorrow, after nine consecutive runs unsent. This is the one row where a single "
         "send converts the whole monitor's output into an actual pitch."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-09-26.md section 2, "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today, 9 "
         "days old, crosses the line tomorrow). Standing constraint is in its first line; the October "
         "issue window is closing."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI. Thread is live, he replied on 2026-09-18, and he "
         "was told '1.21x-2.53x, median 1.33x' when the true figure is 1.11x-2.53x, median 1.25x over "
         "19 tiers. An un-flagged wrong figure in a peer method discussion is worse than a follow-up, "
         "and it has now been outstanding nine days. Route: reply to jan@jansuski.com, In-Reply-To "
         "the existing thread."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has produced no core-beat request on eight "
         "of the last nine runs and no real AI+spend slug for five consecutive runs, so this is the "
         "only lever that widens the monitor rather than re-reading the same single source."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": len(win["ai_strict"]),
        "ai_plus_spend_regex_false_positives": len(win["ai_strict_false_positives"]),
        "consecutive_runs_without_new_core_beat": 8,
        "tracked_urls": 47,
        "carried_and_reverified": 47,
        "unpitched": 43,
        "live_unpitched": len(live_unp),
        "cold_unpitched": len(cold_unp),
        "live_unpitched_with_a_resolved_route": 2,
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 3,
        "drafts_written_never_sent": 4,
        "sendable": 2,
        "sendable_on_its_last_live_day": 1,
        "rows_crossed_cold_today": 2,
        "lost_to_the_cold_line_with_a_draft_ready": 1,
    },
    "monitor_defects_fixed_this_run": [
        ("THE FEED-OVERLAP CLAIM WAS OVERSTATED AND IS CORRECTED. The 2026-09-26 digest recorded "
         "'42 of 42 of them are slugs inside today's new sitemap window - i.e. the feed is exactly the "
         "newest-slugs window'. Measured properly today: 40 slugs listed, 33 inside today's window, "
         "and 7 carrying lastmods from the previous one-to-two days (one at 2026-09-26T01:22Z, six "
         "from 2026-09-25 evening). The feed is a recency window over roughly the newest two days, not "
         "a byte-exact copy of today's window. The claim only ever existed to support 'absence from "
         "the feed is not a cold signal', and that conclusion survives on the correct measurement - "
         "but a monitor that asserts an exact overlap it does not have is one bad day from using "
         "absence as evidence."),
        ("THE AI+SPEND FALSE-POSITIVE COUNTER NOW NAMES ITS HITS RATHER THAN ONLY COUNTING THEM. It "
         "reported 0 real hits and 0 false positives today, and this time the strict-hit list itself "
         "is written into _window_0927.json, so a future zero cannot be the arithmetic accident the "
         "last three runs had to be audited for."),
        ("THE CANDIDATE SET IS SMALLER AND THE DIGEST SAYS SO. 4 candidates were fetched today against "
         "12 yesterday, because the window shrank to 46 slugs from 88. The digest names all 4 rather "
         "than leaving '0 new on-beat' as an unverifiable number."),
        ("CROSSINGS THAT THE ADVANCE WARNING CANNOT SEE ARE NOW NAMED IN expired_this_run. "
         "build_pitch_queue.py warns two days ahead only for sendable rows, so the two low-relevance "
         "rows that went cold today would otherwise have appeared only as the live count falling from "
         "26 to 24."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print(f"wrote digest-{TODAY}.json: {len(ops)} opportunities, {len(digest['platforms_checked'])} platforms")
print(f"live(<=10d): {len(live)}  cold(>10d): {len(stale)}")
for o in ops:
    print(f"  {o['_days_old']:>3}d  {o['url'].rsplit('/', 1)[-1][:56]}")
print("\n--- sample deadline fields ---")
for o in ops[:2]:
    print(f"  {o['url'].rsplit('/', 1)[-1][:44]}\n    {o['deadline'][:220]}")
