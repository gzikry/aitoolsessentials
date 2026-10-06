#!/usr/bin/env python3
"""Update marketing/haro-outreach/pitch-ledger.json for the 2026-10-06 run.

Only fields the run actually measured are touched: the mailbox was checked (no new tracked-pitch
reply), nothing was sent, and the figures were re-derived. Nothing is added to `pitched` because
nothing was sent.
"""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-10-06"
p = D / "pitch-ledger.json"
led = json.loads(p.read_text())

led["reply_status_checked"] = TODAY

led["notes"] = (
    "URL -> date or reason. Written by George or the agent when a pitch is sent or deliberately "
    "dropped, so build_pitch_queue.py stops resurfacing it. Pitches sent to date: 3. Replies "
    "received: 1. Zero sent on 2026-09-29 through 2026-10-06. On 2026-10-06 the queue reached 1 "
    "SENDABLE for the first time in twelve runs: employees-blocked-from-ai-on-work-accounts-"
    "automating-tedious-tasks (Christopher Mims, WSJ columnist) - 1 day old, relevance 'medium', "
    "reply route resolved off his own byline page (linkedin.com/in/christopher-mims-club/, HTTP 200 "
    "with a matching title) rather than off the request. 84 tracked, 37 live unpitched, 43 cold. "
    "The other two route-resolved rows (Raconteur, Speciality Food) remain the crossed drafts and "
    "are still sendable late. Mailbox checked 2026-10-06: no reply to any tracked pitch; the newest "
    "inbound is a tool submission (msg 91), not a pitch reply. Separately: a paid-placement offer "
    "(Lilach Bullock, $300) arrived on a different outreach thread on 2026-09-29 and was declined "
    "same-day under editorial independence - that is not a pitch from this monitor and is not "
    "recorded as one."
)

led["figures_disclosure"]["date"] = TODAY
led["figures_disclosure"]["status"] = (
    "STILL UNSENT - Day 18. The recipient of the 2026-09-18 Amplemarket reply was told the same-tier "
    "monthly/annual range is '1.21x-2.53x, median 1.33x'. The current verified figure is "
    "1.11x-2.53x, median 1.25x over 19 tiers across 14 tools. 2026-10-06: the 19-pair set was "
    "RE-ASSERTED AND THE FILE REBUILT against the refreshed snapshot (data/pricing_snapshots.json "
    "updated 2026-10-06, extract_monthly_annual_pairs.py exit 0, all 19 pairs printed, no needle "
    "failures, data/monthly_annual_pairs.json rewritten with built: 2026-10-06). SEPARATELY, the "
    "shadow-AI headline figures re-derived UNCHANGED: 42 of 76 tools quote a non-zero monthly price, "
    "33 at or under $25/month, median $17.50 (same set as 2026-10-02/2026-10-05; the 40/31/$16.50 "
    "set that moved on 2026-10-02 stayed moved and is superseded). Drafts written before 2026-10-02 "
    "that cite 40/31/$16.50 must not be sent. The 1.16x floor and the 138/136 word counts claimed in "
    "older drafts are also superseded. Day 18 unsent."
)

led["reply_status"]["https://www.sourcee.app/journo-request/enterprise-ai-leaders-value-creation-ownership-and-governance"] = (
    "no reply. Pitched 2026-09-15 to hello@foxandspindle.com (msg 171/172). Twenty-one days of "
    "silence. This send crossed the 10-day cold line on 2026-09-25 and the request page is 22 days "
    "old today."
)
led["reply_status"]["https://www.sourcee.app/journo-request/individual-contributors-managing-ai-agents-without-title-or-pay"] = (
    "no reply. Pitched 2026-09-18 to Rani@Sherwood.news (msg 175/176). Eighteen days of silence. "
    "Request is now 26 days old and well past the cold line."
)

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": TODAY,
    "url": ("https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket, "
            "https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech"),
    "action": ("both sent-ready drafts carried and republished again, still unsent (seventeenth run; "
               "eleventh run). Figures re-derived unchanged (42/33/$17.50) against a snapshot "
               "refreshed today, and the pair file was rebuilt rather than re-read."),
    "note": ("Neither is void. Both pages returned HTTP 200 again today with the request body still "
             "served, and both routes were re-resolved against the live pages this run: "
             "simon.chandler@raconteur.net off /contributors/simon-chandler (HTTP 200, 154,819 bytes, "
             "data-part1/2/3 unchanged at simon.chandler + raconteur + net; control "
             "/contributors/tom-dennis HTTP 200 carries tom.dennis/raconteur/net; the older "
             "/author/simon-chandler/ still 404s), and holly.shackleton@artichokehq.com off "
             "specialityfoodmagazine.com/contact (HTTP 200, 59,488 bytes, alongside five other named "
             "masthead addresses). The shadow-AI draft is now unsent through SEVENTEEN consecutive "
             "runs; the Speciality Food draft has been carried an eleventh time and its October "
             "window has closed. What was lost is the ideal window, not the pitch."),
})

led.setdefault("cold_without_a_send", []).insert(1, {
    "date": TODAY,
    "url": "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks",
    "action": ("NEW AND NOT YET COLD - logged here so the first sendable row in this monitor's "
               "history does not go unrecorded. 1 day old, relevance 'medium', route resolved."),
    "note": ("The counterweight to the two rows above: this is the first request in twelve runs that "
             "is both above the tangential band and route-resolved, and it arrived the day after the "
             "monitor went twelve runs without a core-beat find. Written into the ledger rather than "
             "left in the digest because the ledger is what the next run reads before deciding what "
             "to resurface. Draft: pitch-drafts-2026-10-06.md section 1. Route: LinkedIn DM to "
             "linkedin.com/in/christopher-mims-club/ (HTTP 200 today, title 'Christopher Mims - The "
             "Wall Street Journal | LinkedIn'); the request's own body says '(DMs open)'. Dead ends "
             "recorded so they are not retried as routes: muckrack.com/christopher-mims HTTP 403, "
             "wsj.com/news/author/christopher-mims HTTP 401. Not sent - sends are George's lane."),
})

p.write_text(json.dumps(led, indent=1))
print("updated", p.name)
print("reply_status_checked:", led["reply_status_checked"])
print("pitched entries:", len(led["pitched"]), "| cold_without_a_send:", len(led["cold_without_a_send"]))
