#!/usr/bin/env python3
"""Patch pitch-ledger.json for the 2026-10-07 run (notes, reply_status_checked, figures_disclosure,
cold_without_a_send entry, log entry). Loads, updates, writes — no hand-editing."""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
LED = D / "pitch-ledger.json"
led = json.loads(LED.read_text())

led["notes"] = (
    "URL -> date or reason. Written by George or the agent when a pitch is sent or deliberately "
    "dropped, so build_pitch_queue.py stops resurfacing it. Pitches sent to date: 3. Replies "
    "received: 1. Zero sent on 2026-09-29 through 2026-10-07 (nine consecutive runs). The queue's "
    "first and so far ONLY sendable row (employees-blocked-from-ai-on-work-accounts-automating-"
    "tedious-tasks; Christopher Mims, WSJ) is now 2 days old and still route-resolved. 2026-10-07 "
    "run: 94 tracked, 47 live unpitched, 43 cold unpitched, 1 sendable. The new window produced 10 "
    "AI-token slugs and ZERO AI+spend slugs - none core-beat, none sendable (cleaner than 2026-10-06, "
    "whose single ai_strict hit was a 'procurement' false positive in an AI-insurance call). Mailbox "
    "checked 2026-10-07: no reply to any tracked pitch; four new inbound tool submissions (msgs "
    "96-100), the newest msg 100 at 2026-10-07 15:55Z, none a pitch reply. Separately: a "
    "paid-placement offer (Lilach Bullock, $300) arrived on a different outreach thread on "
    "2026-09-29 and was declined same-day under editorial independence - that is not a pitch from "
    "this monitor and is not recorded as one."
)
led["reply_status_checked"] = "2026-10-07"

fd = led.get("figures_disclosure", {})
fd["date"] = "2026-10-07"
fd["status"] = (
    "STILL UNSENT - Day 19. The recipient of the 2026-09-18 Amplemarket reply was told the "
    "same-tier monthly/annual range is '1.21x-2.53x, median 1.33x'. The current verified figure is "
    "1.11x-2.53x, median 1.25x over 19 tiers across 14 tools. 2026-10-07: the 19-pair set was "
    "RE-ASSERTED AND THE FILE REBUILT against the refreshed snapshot (data/pricing_snapshots.json "
    "updated 2026-10-07, extract_monthly_annual_pairs.py exit 0, all 19 pairs printed, no needle "
    "failures, data/monthly_annual_pairs.json rewritten with built: 2026-10-07). SEPARATELY, the "
    "shadow-AI headline figures re-derived UNCHANGED: 42 of 76 tools quote a non-zero monthly price, "
    "33 at or under $25/month, median $17.50 (same set as 2026-10-02 through 2026-10-06). Drafts "
    "written before 2026-10-02 that cite 40/31/$16.50 must not be sent. The 1.16x floor and the "
    "138/136 word counts claimed in older drafts are also superseded. Day 19 unsent."
)
fd["action_required"] = (
    "Send Jan Suski a short correction. The thread is live and he replied to us on 2026-09-18, so an "
    "un-flagged wrong figure in a peer method discussion is worse than a follow-up. Send the CURRENT "
    "figure (1.11x-2.53x, median 1.25x over 19 tiers), not the 1.16x one from the 2026-09-21 drafts. "
    "Route: reply to jan@jansuski.com (In-Reply-To the existing thread). George's lane."
)
led["figures_disclosure"] = fd

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": "2026-10-07",
    "url": ("https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-"
            "outofpocket, https://www.sourcee.app/journo-request/speciality-food-retailers-and-"
            "producers-how-theyd-spend-10k-on-tech"),
    "action": ("both sent-ready drafts carried and republished again, still unsent (EIGHTEENTH run; "
               "twelfth run). Figures re-derived unchanged (42/33/$17.50) against a snapshot "
               "refreshed to 2026-10-07, and the pair file was rebuilt rather than re-read."),
    "note": ("Neither is void. Both pages returned HTTP 200 again today with the request body still "
             "served. The shadow-AI route was re-resolved against the live "
             "/contributors/simon-chandler page this run (HTTP 200, 154,819 bytes, data-part1/2/3 "
             "unchanged at simon.chandler + raconteur + net; control /contributors/tom-dennis HTTP "
             "200 carries tom.dennis/raconteur/net; the older /author/simon-chandler/ still 404s), "
             "and the Speciality Food route was re-read off specialityfoodmagazine.com/contact "
             "(HTTP 200, 59,488 bytes, alongside five other named masthead addresses). The shadow-AI "
             "draft is now unsent through EIGHTEEN consecutive runs; the Speciality Food draft has "
             "been carried a twelfth time and its October window has closed. What was lost is the "
             "ideal window, not the pitch.")
})

led.setdefault("log", []).insert(0, {
    "date": "2026-10-07",
    "event": ("monitor run - 10 new AI-token tracked, 0 AI+spend (first clean window in three runs), "
              "0 rows crossed cold, 1 sendable, no sends"),
    "url": "(no pitch)",
    "action": "none sent - 1 sendable row carried (WSJ blocked-work-accounts, now 2 days old)",
    "to": None, "route": None, "sent_message_id": None,
    "note": ("94 tracked (84 carried and all 84 re-verified HTTP 200/live, 10 new AI-token finds), "
             "47 live unpitched, 43 cold unpitched, 1 sendable. New window: 109 slugs, 10 AI-token, "
             "0 AI+spend, 6 spend-token (all consumer cost-of-living: airline customers, a paid TV "
             "casting call, Houston household costs, Brooklyn hair-care costs, house-sharing, Gen Z "
             "personal finance). All 16 candidates fetched and read in full. None of the ten new "
             "rows is core-beat and none is sendable - all leave the body address Sourcee-redacted "
             "or publish no route. The pair range held at 1.11x-2.53x over 19 tiers for the "
             "eleventh consecutive day against a snapshot refreshed to `updated: 2026-10-07` and a "
             "pair file rebuilt today. The 2026-10-06 sendable row (Christopher Mims, WSJ) "
             "re-verified live at 2 days and its route re-fetched (LinkedIn, HTTP 200, 603,318 "
             "bytes, matching title). Mailbox: no reply to any tracked pitch; four new tool "
             "submissions (msgs 96-100), none a pitch reply. 0 pitches sent this run - sends remain "
             "George's lane. Figures correction to Jan Suski now 19 days outstanding.")
})

LED.write_text(json.dumps(led, indent=1))
print("ledger updated:", LED)
print("notes len:", len(led["notes"]))
print("cold entries:", len(led["cold_without_a_send"]), "log entries:", len(led["log"]))
