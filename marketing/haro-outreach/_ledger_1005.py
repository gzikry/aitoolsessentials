#!/usr/bin/env python3
"""Update marketing/haro-outreach/pitch-ledger.json for the 2026-10-05 run.

Only fields the run actually measured are touched: the mailbox was checked (no new tracked-pitch
reply), nothing was sent, and the figures were re-derived. Nothing is added to `pitched` because
nothing was sent.
"""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-10-05"
p = D / "pitch-ledger.json"
led = json.loads(p.read_text())

led["reply_status_checked"] = TODAY

led["notes"] = (
    "URL -> date or reason. Written by George or the agent when a pitch is sent or deliberately "
    "dropped, so build_pitch_queue.py stops resurfacing it. Pitches sent to date: 3. Replies "
    "received: 1. Zero sent on 2026-09-29 through 2026-10-05. The queue is at ZERO SENDABLE, and on "
    "2026-10-05 that is the true count: 74 tracked, 27 live unpitched, none with both a relevance "
    "above the tangential band and a usable route. The two rows that do carry a resolved route "
    "(Raconteur, Speciality Food) are the two crossed drafts, both past the 10-day line and still "
    "sendable late (routes re-resolved live this run). Mailbox checked 2026-10-05: no reply to any "
    "tracked pitch; the newest inbound is a tool submission (msg 91), not a pitch reply. Separately: "
    "a paid-placement offer (Lilach Bullock, $300) arrived on a different outreach thread and was "
    "declined same-day under editorial independence - that is not a pitch from this monitor and is "
    "not recorded as one."
)

led["figures_disclosure"]["date"] = TODAY
led["figures_disclosure"]["status"] = (
    "STILL UNSENT - Day 17. The recipient of the 2026-09-18 Amplemarket reply was told the same-tier "
    "monthly/annual range is '1.21x-2.53x, median 1.33x'. The current verified figure is "
    "1.11x-2.53x, median 1.25x over 19 tiers across 14 tools. 2026-10-05: the 19-pair set "
    "RE-ASSERTED CLEAN against the refreshed snapshot (data/pricing_snapshots.json updated "
    "2026-10-05, extract_monthly_annual_pairs.py exit 0 printing all 19 pairs, no needle failures). "
    "SEPARATELY, the shadow-AI headline figures re-derived UNCHANGED today: 42 of 76 tools quote a "
    "non-zero monthly price, 33 at or under $25/month, median $17.50 (same set as 2026-10-02; the "
    "40/31/$16.50 set that moved on 2026-10-02 stayed moved and is superseded). Drafts written "
    "before 2026-10-02 that cite 40/31/$16.50 must not be sent. The 1.16x floor and the 138/136 word "
    "counts claimed in older drafts are also superseded. Day 17 unsent."
)

led["reply_status"]["https://www.sourcee.app/journo-request/enterprise-ai-leaders-value-creation-ownership-and-governance"] = (
    "no reply. Pitched 2026-09-15 to hello@foxandspindle.com (msg 171/172). Twenty days of silence. "
    "This send crossed the 10-day cold line on 2026-09-25 and the request page is 21 days old today."
)
led["reply_status"]["https://www.sourcee.app/journo-request/individual-contributors-managing-ai-agents-without-title-or-pay"] = (
    "no reply. Pitched 2026-09-18 to Rani@Sherwood.news (msg 175/176). Seventeen days of silence. "
    "Request is now 25 days old and well past the cold line."
)

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": TODAY,
    "url": ("https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket, "
            "https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech"),
    "action": ("both sent-ready drafts carried and republished again, still unsent (sixteenth run; ninth run). "
               "Figures re-derived unchanged (42/33/$17.50) against a snapshot refreshed today."),
    "note": ("Neither is void. Both pages returned HTTP 200 again today with the request body still served, and "
             "both routes were re-resolved against the live pages this run: simon.chandler@raconteur.net off "
             "/contributors/simon-chandler (HTTP 200, 154,819 bytes, data-part1/2/3 unchanged at simon.chandler "
             "+ raconteur + net; control /contributors/tom-dennis HTTP 200 carries tom.dennis/raconteur/net; the "
             "older /author/simon-chandler/ still 404s), and holly.shackleton@artichokehq.com off "
             "specialityfoodmagazine.com/contact (HTTP 200, 59,488 bytes, alongside five other named masthead "
             "addresses). The shadow-AI draft is now unsent through SIXTEEN consecutive runs; the Speciality "
             "Food draft has been carried for a ninth time and its October window has closed. What was lost is "
             "the ideal window, not the pitch."),
})

led.setdefault("cold_without_a_send", []).insert(1, {
    "date": TODAY,
    "url": ("ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai, "
            "engineering-managers-measuring-engineers-when-using-ai, "
            "saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup"),
    "action": "all three crossed the 10-day line since the 2026-10-02 digest at 13 days, unpitched, none with a resolved route",
    "note": ("All three were already relevance 'low' and none was ever sendable, so the crossing cost nothing. "
             "Two of the three were sitting at exactly 10 days in the 2026-10-02 digest's advance warning. Named "
             "individually because build_pitch_queue.py's two-day advance warning covers only sendable rows, so "
             "an ordinary crossing otherwise shows up as nothing but the live count falling."),
})

p.write_text(json.dumps(led, indent=1))
print("updated", p.name)
print("reply_status_checked:", led["reply_status_checked"])
print("pitched entries:", len(led["pitched"]), "| cold_without_a_send:", len(led["cold_without_a_send"]))
