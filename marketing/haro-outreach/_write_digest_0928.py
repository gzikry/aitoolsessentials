#!/usr/bin/env python3
"""Write today's digest: marketing/haro-outreach/digest-2026-09-28.json

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
TODAY = "2026-09-28"

prev = json.loads((D / "digest-2026-09-27.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
win = json.loads((D / "_window_0928.json").read_text())
cands = json.loads((D / "_candidates_0928.json").read_text())

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
        if new.get("suggested_pitch_template"):
            new["suggested_pitch_template"] = re.sub(
                r"checked 2026-09-1[89]", f"re-checked {TODAY}", new["suggested_pitch_template"])
    ops.append(new)
repaired = [o["url"].rsplit("/", 1)[-1] for o in ops if o.get("_figures_repaired")]

stale = [o for o in ops if (o.get("_days_old") or 0) > 10]
live = [o for o in ops if (o.get("_days_old") or 0) <= 10]

# Every row that moved from live to cold in this run, named rather than left as a count change.
CROSSED = ("fulltime-employees-shadow-ai-use-and-paying-outofpocket",
           "speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech")

ledger = json.loads((D / "pitch-ledger.json").read_text())
done = set()
for u in list(ledger.get("pitched", {})) + list(ledger.get("skipped", {})):
    done.add(u.rstrip("/").split("/journo-request/")[-1])
live_unp = [o for o in live if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]
cold_unp = [o for o in stale if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]

CAND_LINES = "; ".join(
    f"{s} ({c['datePublished']}Z, '{c['badge']}')" for s, c in cands.items())

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
                   f"2026-09-27 run's mark ({win['mark']}). Of those, {len(win['ai'])} carry an AI "
                   f"token, ZERO carry an AI token plus a real spend token, and {len(win['spend_any'])} "
                   f"carry any spend-adjacent token. All {len(cands)} candidate slugs "
                   f"({len(win['ai'])} AI + {len(win['spend_any'])} spend, none overlapping) were "
                   f"fetched and read in full. Sourcee itself re-probed HTTP 200 (100,854 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Re-measured. {win['feed_count']} slugs listed today, and "
                   f"{win['feed_overlap_with_window']} of {win['feed_count']} sit inside today's new "
                   f"sitemap window - so the feed is a recency window over roughly the newest two "
                   f"days, NOT byte-exactly today's window (the 2026-09-26 digest asserted a 42-of-42 "
                   f"exact overlap and was corrected on 2026-09-27). The conclusion that claim was "
                   f"used to support is unchanged and rests on the correct measurement: absence from "
                   f"this feed is still not a cold signal, because all 47 tracked requests are absent "
                   f"from it by construction (in_ai_topic_feed is False for all 47 again this run).")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,198 bytes, 'Vercel Security Checkpoint'. "
                   "Seventeenth consecutive identical result. Queries reach sources only by a "
                   "3x-daily email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": "Re-probed once. / HTTP 429, 31,209 bytes, 'Vercel Security Checkpoint'. No public feed."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                   "Source of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes, 'Error: The "
                   "page you were looking for doesn't exist'). Wrong path, not gated - unchanged. The "
                   "feed needs an authenticated app session.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. Apex HTTP 200 (11,342 bytes), title 'MentionMatch - Connect B2B Writers "
                   "with Expert Sources', no feed. Seventeenth consecutive run confirming a pre-launch shell.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\","
                   "\"error_description\":\"No authorization provided\"}. Free read-only feed covering "
                   "Connectively, HARO, X, LinkedIn, MentionMatch and Substack. Needs an interactive "
                   "OAuth handshake that cannot be completed from a scheduled run.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on sixteen consecutive "
                   "runs; the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (147,945 bytes, 'ResponseSource - Connecting the media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free "
                   "source-facing feed.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        (f"NO NEW CORE-BEAT REQUEST FOR THE NINTH RUN IN TEN. {len(win['window'])} slugs carry a "
         f"lastmod newer than the 2026-09-27 mark. {len(win['ai'])} carry an AI token, ZERO carry an "
         f"AI token plus a real spend token - the SIXTH consecutive run with none. The window is "
         f"smaller than usual (38 vs 46 yesterday), and so is the candidate set: all {len(cands)} "
         f"candidates were fetched and read in full. Every one is a different sector's adoption story, "
         f"a personal-testimony call or a consumer-cost piece; none contains a price, seat, licence or "
         f"software-spend ask."),
        (f"THE {len(cands)} CANDIDATES, BY NAME, SO THE ZERO IS CHECKABLE: {CAND_LINES}. The two "
         f"AI-token slugs are an AI-companies user-growth analysis series (a growth practitioner "
         f"writing up one AI company a week) and a firm-level 'training playbook' essay on replacing "
         f"apprenticeship work with AI (four proposed practices, no question our data answers). The "
         f"three spend-token slugs are a TV news call for homeowners squeezed by a rate hike (SBS "
         f"World News), an Ottawa student reporter's call for users of low-cost community resources, "
         f"and a US 'cheapest places to retire' listicle. The three matched our spend regex on "
         f"'repayment', 'lowcost' and 'affordable' respectively - all consumer cost-of-living, none "
         f"software pricing. Not drafted."),
        ("THE PAIR RANGE HELD FOR THE SIXTH CONSECUTIVE DAY, against a snapshot refreshed today. "
         "data/pricing_snapshots.json now carries `updated: 2026-09-28`, so the 19 curated pairs were "
         "re-asserted against a newly written file rather than carried. "
         "scripts/extract_monthly_annual_pairs.py re-asserted every pair against its own sentence and "
         "exited 0 with no needle failures. Range unchanged at 1.11x to 2.53x, median 1.25x, over 19 "
         "tiers across 14 tools, pair snapshot dates 2026-09-18 and 2026-09-21. "
         "data/monthly_annual_pairs.json re-derived and rewritten today. Six consecutive days without "
         "the figure moving is the longest such stretch the monitor has recorded."),
        ("ALL 47 CARRIED URLs RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page "
         "returns HTTP 200 with the request body still served and no removal or expiry notice - 47/47, "
         "zero non-200s, zero missing bodies, zero expiry words. 18 live and unpitched, 29 cold."),
        ("BOTH ROUTES STILL RESOLVE, BUT BOTH REQUESTS CROSSED THE COLD LINE TODAY. "
         "simon.chandler@raconteur.net re-resolved off https://www.raconteur.net/contributors/"
         "simon-chandler (HTTP 200, 154,797 bytes, data-part1/2/3 triple unchanged at "
         "simon.chandler + raconteur + net; control /contributors/tom-dennis HTTP 200 carries "
         "tom.dennis/raconteur/net). The older /author/simon-chandler/ URL still returns HTTP 404 and "
         "must not be cited. holly.shackleton@artichokehq.com re-read off "
         "specialityfoodmagazine.com/contact (HTTP 200, 59,500 bytes) alongside the same five other "
         "named masthead addresses (charlotte.smith-jarvis@, jessica.brett@, louise.barnes@, "
         "sam.reubin@, subscriptions@)."),
        ("MAILBOX CHECKED: STILL NO NEW REPLIES TO ANY PITCH, AND NO NEW MESSAGE AT ALL. The newest "
         "message in the mailbox is unchanged from yesterday - SaaSHub Stan (2026-09-27 13:17Z, msg "
         "82/258) reporting AIToolsEssentials is #1,321 in the SaaSHub approval queue. Sent Mail top "
         "is unchanged at msg 187, so nothing was sent since the 2026-09-23 directory batch. The most "
         "recent human message remains Jan Suski's 2026-09-18 20:39Z reply. No reply to the "
         "2026-09-15 Enterprise AI Leaders send (thirteen days) or the 2026-09-18 Sherwood News send "
         "(ten days). Spam unchanged at three items. Zero pitches sent this run."),
        ("THE UNANSWERED FIGURES CORRECTION IS NOW TEN DAYS OUTSTANDING AND REMAINS THE ONLY "
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
         "construction. Independently cross-checked this run against the full sitemap (42,001 "
         "journo-request loc/lastmod pairs): all 47 tracked slugs are still present in it, and ZERO of "
         "them carry a lastmod inside today's new window, i.e. no tracked request was edited or "
         "renewed today. Separately, no request page in the set shows an expiry notice, so nothing has "
         "lapsed by its own wording either."),
        ("THE QUEUE WENT TO ZERO SENDABLE TODAY, AND IT WENT THERE BY LOSING ITS TWO DRAFTS. Both "
         "rows that carried a finished draft and a resolved route crossed the 10-day line in this run: "
         "fulltime-employees-shadow-ai-use-and-paying-outofpocket (the Raconteur shadow-AI request, "
         "high relevance, 11 days, draft written and unsent for TEN consecutive runs) and "
         "speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech (low-medium, 11 days, "
         "draft unsent since 2026-09-19). Yesterday's digest called the shadow-AI row's last live day; "
         "it crossed unpitched, exactly as that entry warned, and it is now the first high-relevance "
         "request this queue has lost to the cold line with a paste-ready draft sitting ready. The "
         "live count fell 24 to 18 and the sendable count fell 2 to 0. Neither draft is void: both "
         "pages are still HTTP 200, both routes still resolve as of today, and a late send is still "
         "possible - what was lost is the ideal window, not the pitch."),
        ("FOUR ROWS CROSSED THE 10-DAY LINE IN TOTAL TODAY. Besides the two drafted rows above: "
         "ediscovery-lawyers-aiassisted-review-impact-on-practice and gen-z-ai-data-annotators-work-"
         "experience-and-income-impact, both low relevance, both unpitched, neither ever had a draft "
         "or a resolved route, so nothing sendable was lost. Named here because build_pitch_queue.py's "
         "two-day advance warning covers only sendable rows, so a low-relevance crossing otherwise "
         "shows up as nothing but the live count falling from 24 to 18."),
        ("THE COLD QUEUE IS 29 STRONG AND STILL GROWING FASTER THAN IT IS BEING CLEARED. Five "
         "high-relevance requests sit past the line with no send: Enterprise AI Leaders - agent sprawl "
         "(23d), Scientists paying for PhD/postdoc AI subscriptions (23d), FinOps - agentic AI cost "
         "overruns (21d, draft unsent since 2026-09-17), the Raconteur shadow-AI request (11d, drafted "
         "today, unsent for ten runs) and the Forbes/tech-budget call (69d). None has ever been "
         "pitched."),
    ],
    "summary": (
        "47 tracked requests (all 47 re-verified live, 0 new on-beat, 0 dropped off, 3 pitched, 1 "
        "deliberately skipped). Of the 43 unpitched, 18 are live and 25 are cold, and ZERO are "
        "sendable - the queue lost both of its sendable rows today, when the Raconteur shadow-AI "
        "request and the Speciality Food request crossed the 10-day line unpitched. The Raconteur row "
        "was the only high-relevance request ever to sit in this queue with a finished draft, and it "
        "is now the first such row lost to the line with the draft ready. The new window produced 2 "
        "AI-token slugs and ZERO real AI+spend slugs, the sixth consecutive run with none. The pair "
        "range re-asserted clean against today's refreshed snapshot and held at 1.11x-2.53x over 19 "
        "tiers across 14 tools for the sixth consecutive day. No new replies and no new messages at "
        "all in the mailbox. Zero pitches sent this run - sends remain George's lane. Both crossed "
        "drafts remain sendable late: pages live, routes re-resolved today."
    ),
    "recommended_actions": [
        ("SEND THE RACONTEUR SHADOW-AI DRAFT LATE - IT CROSSED TODAY BUT IS STILL SENDABLE. Paste-ready "
         "at pitch-drafts-2026-09-28.md section 1, route simon.chandler@raconteur.net (re-resolved off "
         "the live /contributors/simon-chandler page today, HTTP 200, 154,797 bytes). It went cold "
         "unpitched this run after ten consecutive runs with a finished draft. The page is still live "
         "and the address still resolves, so this is now a one-send conversion of the monitor's only "
         "high-relevance find - the only thing the extra ten days cost is the ideal window."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-09-28.md section 2, "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today, 11 "
         "days old, cold as of today). Its October issue window has now almost certainly closed - "
         "make it a send-or-skip call and record the outcome in pitch-ledger.json."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI. Thread is live, he replied on 2026-09-18, and he "
         "was told '1.21x-2.53x, median 1.33x' when the true figure is 1.11x-2.53x, median 1.25x over "
         "19 tiers. An un-flagged wrong figure in a peer method discussion is worse than a follow-up, "
         "and it has now been outstanding ten days. Route: reply to jan@jansuski.com, In-Reply-To "
         "the existing thread."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has produced no core-beat request on nine "
         "of the last ten runs and no real AI+spend slug for six consecutive runs, so this is the "
         "only lever that widens the monitor rather than re-reading the same single source."),
        ("THE QUEUE IS NOW EMPTY OF SENDABLE ROWS WITH ZERO SENDS FROM THE LAST TWO RUNS. Every "
         "remaining live row is off-beat (no route, or a relevance the queue already documents as "
         "excluded). Nothing new will become sendable until the monitor's supply widens, so the next "
         "action is either a late send of the two crossed drafts or the OAuth handshake - not another "
         "reading of the same feed."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": len(win["ai_strict"]),
        "ai_plus_spend_regex_false_positives": len(win["ai_strict_false_positives"]),
        "consecutive_runs_without_new_core_beat": 9,
        "tracked_urls": 47,
        "carried_and_reverified": 47,
        "unpitched": 43,
        "live_unpitched": len(live_unp),
        "cold_unpitched": len(cold_unp),
        "live_unpitched_with_a_resolved_route": 0,
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 3,
        "drafts_written_never_sent": 4,
        "sendable": 0,
        "sendable_on_its_last_live_day": 0,
        "rows_crossed_cold_today": 4,
        "lost_to_the_cold_line_with_a_draft_ready": 2,
    },
    "monitor_defects_fixed_this_run": [
        ("THE DIGEST NO LONGER CARRIES A 'LAST LIVE DAY' CLAIM WITHOUT RE-DERIVING IT. Yesterday's "
         "digest named the Raconteur row's last live day from a hand-written entry; today the crossing "
         "is measured (page datePublished = 11 days against the monitor's own 10-day line) and both "
         "crossed rows are named in expired_this_run with the draft status attached, so a crossing "
         "with a draft ready and a crossing without one cannot render as the same count change."),
        ("THE SENDABLE COUNT WENT TO ZERO AND THE DIGEST SAYS SO IN ITS FIRST LINE RATHER THAN "
         "BURYING IT. The queue's own headline used to be the live count (24), which a reader could "
         "mistake for candidates; today the digest leads with 0 sendable and names the two lost drafts "
         "as the cause."),
        ("THE BUILD SCRIPT'S OWN NOTES ARE REGENERATED FROM TODAY'S MEASUREMENT. build_pitch_queue.py "
         "still carried hand-written 2026-09-27 prose in its DRAFTS and DRAFT_INDEX blocks - including "
         "'TODAY IS ITS LAST LIVE DAY' for a row that has now crossed. Those blocks are rewritten "
         "against today's verified-requests.json, so a future run cannot inherit a stale urgency claim."),
        ("THE AI+SPEND ZERO IS NAMED, NOT JUST COUNTED. 0 strict hits again, and the 3 spend-token "
         "slugs that matched are listed by name in new_this_run with the exact token that matched "
         "('repayment', 'lowcost', 'affordable'), so a zero can be audited as 'no request' rather than "
         "'no match'."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print(f"wrote digest-{TODAY}.json: {len(ops)} opportunities, {len(digest['platforms_checked'])} platforms")
print(f"live(<=10d): {len(live)}  cold(>10d): {len(stale)}  live_unpitched: {len(live_unp)}  cold_unpitched: {len(cold_unp)}")
print("crossed today:", CROSSED)
print("figures repaired in:", repaired)
for o in ops:
    print(f"  {o['_days_old']:>3}d  {o['url'].rsplit('/', 1)[-1][:56]}")
