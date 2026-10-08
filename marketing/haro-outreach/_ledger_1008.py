#!/usr/bin/env python3
"""Patch pitch-ledger.json for the 2026-10-08 run (notes, reply_status_checked, figures_disclosure,
cold_without_a_send entry, log entry). Loads, updates, writes — no hand-editing."""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
LED = D / "pitch-ledger.json"
led = json.loads(LED.read_text())

led["notes"] = (
    "URL -> date or reason. Written by George or the agent when a pitch is sent or deliberately "
    "dropped, so build_pitch_queue.py stops resurfacing it. Pitches sent to date: 3. Replies "
    "received: 1. Zero sent on 2026-09-29 through 2026-10-08 (ten consecutive runs). The queue's "
    "first and so far ONLY sendable row (employees-blocked-from-ai-on-work-accounts-automating-"
    "tedious-tasks; Christopher Mims, WSJ) is now 3 days old and still route-resolved. 2026-10-08 "
    "run: 101 tracked, 54 live unpitched, 43 cold unpitched, 1 sendable. The new window produced 7 "
    "AI-token slugs and ONE AI+spend slug - the first real software-cost request in fourteen runs "
    "(google-and-claude-enterprise-users-seats-and-token-costs, Glenn Hansen), relevance 'high' but "
    "with NO resolved route, so not sendable. Mailbox checked 2026-10-08: no reply to any tracked "
    "pitch; INBOX top is msg 102 (a ToolChase reply to the separate Sep-3 guest-pitch batch, not "
    "this monitor), then msg 101 (a tool submission, 2026-10-08 00:29Z). Separately: a paid-"
    "placement offer (Lilach Bullock, $300) arrived on a different outreach thread on 2026-09-29 "
    "and was declined same-day under editorial independence - that is not a pitch from this monitor "
    "and is not recorded as one."
)
led["reply_status_checked"] = "2026-10-08"

fd = led.get("figures_disclosure", {})
fd["date"] = "2026-10-08"
fd["status"] = (
    "STILL UNSENT - Day 20. The recipient of the 2026-09-18 Amplemarket reply was told the "
    "same-tier monthly/annual range is '1.21x-2.53x, median 1.33x'. The current verified figure is "
    "1.11x-2.53x, median 1.25x over 19 tiers across 14 tools. 2026-10-08: the 19-pair set was "
    "RE-ASSERTED AND THE FILE REBUILT against the refreshed snapshot (data/pricing_snapshots.json "
    "updated 2026-10-08, extract_monthly_annual_pairs.py exit 0, all 19 pairs printed, no needle "
    "failures, data/monthly_annual_pairs.json rewritten). SEPARATELY, the shadow-AI headline figures "
    "re-derived UNCHANGED: 42 of 76 tools quote a non-zero monthly price, 33 at or under $25/month, "
    "median $17.50 (same set as 2026-10-02 through 2026-10-07). Drafts written before 2026-10-02 "
    "that cite 40/31/$16.50 must not be sent. The 1.16x floor and the 138/136 word counts claimed in "
    "older drafts are also superseded. Day 20 unsent."
)
fd["action_required"] = (
    "Send Jan Suski a short correction. The thread is live and he replied to us on 2026-09-18, so an "
    "un-flagged wrong figure in a peer method discussion is worse than a follow-up. Send the CURRENT "
    "figure (1.11x-2.53x, median 1.25x over 19 tiers), not the 1.16x one from the 2026-09-21 drafts. "
    "Route: reply to jan@jansuski.com (In-Reply-To the existing thread). George's lane."
)
led["figures_disclosure"] = fd

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": "2026-10-08",
    "url": ("https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-"
            "outofpocket, https://www.sourcee.app/journo-request/speciality-food-retailers-and-"
            "producers-how-theyd-spend-10k-on-tech"),
    "action": ("both sent-ready drafts carried and republished again, still unsent (NINETEENTH run; "
               "thirteenth run). Figures re-derived unchanged (42/33/$17.50) against a snapshot "
               "refreshed to 2026-10-08, and the pair file was rebuilt rather than re-read."),
    "note": ("Neither is void. Both pages returned HTTP 200 again today with the request body still "
             "served. The shadow-AI route was re-resolved against the live /contributors/simon-chandler "
             "page this run (HTTP 200, 154,819 bytes, data-part1/2/3 unchanged at simon.chandler + "
             "raconteur + net; control /contributors/tom-dennis HTTP 200 carries tom.dennis/raconteur/"
             "net; the older /author/simon-chandler/ still 404s), and the Speciality Food route was "
             "re-read off specialityfoodmagazine.com/contact (HTTP 200, 59,488 bytes, alongside five "
             "other named masthead addresses). The shadow-AI draft is now unsent through NINETEEN "
             "consecutive runs; the Speciality Food draft has been carried a thirteenth time and its "
             "October window has closed. What was lost is the ideal window, not the pitch.")
})

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": "2026-10-08",
    "url": "https://www.sourcee.app/journo-request/google-and-claude-enterprise-users-seats-and-token-costs",
    "action": ("NEW - the FIRST core-beat AI+spend request in fourteen runs, and the best-matching "
               "request this monitor has ever held. Logged here because it is high relevance and "
               "would otherwise be lost in the 'not sendable' tail purely for want of a route."),
    "note": ("relevance 'high': the reporter Glenn Hansen asks directly for 'enterprise-level costs "
             "for AI seats and tokens' from Google or Claude users - the exact quantity our dated "
             "price set measures. Our data holds Claude Team seats $20/$100 per seat/month (checked "
             "2026-09-18), Gemini bundled into Workspace at $8.40/$7 up to $26.40/$22 per user/month "
             "(2026-09-18), and Copilot Business $19 / Enterprise $39 per user/month (2026-10-01). "
             "NOT SENDABLE: the page publishes no address, handle or link and gives no reply "
             "instruction (email_redacted=False but emails_on_page=none). A web search cannot confirm "
             "WHICH Glenn Hansen this is - a same-name LinkedIn profile ('In Power', Stillwater MN) "
             "is a different person - so NO handle may be invented. Route must be resolved before "
             "send. Draft ready at pitch-drafts-2026-10-08.md section 2.")
})

led.setdefault("log", []).insert(0, {
    "date": "2026-10-08",
    "event": ("monitor run - 7 new AI-token tracked, 1 AI+spend (first real software-cost hit in three "
              "runs), 0 rows crossed cold, 1 sendable, no sends"),
    "url": "(no pitch)",
    "action": "none sent - 1 sendable row carried (WSJ blocked-work-accounts, now 3 days old)",
    "to": None, "route": None, "sent_message_id": None,
    "note": ("101 tracked (94 carried and all 94 re-verified HTTP 200/live, 7 new AI-token finds), "
             "54 live unpitched, 43 cold unpitched, 1 sendable. New window: 111 slugs, 7 AI-token, "
             "1 AI+spend, 8 spend-token (all consumer cost-of-living: restaurant labour, student "
             "tutoring pay, grocery prices, fuel/household budgets, medical billing, childcare, "
             "dating spend). All 14 candidates fetched and read in full. THE FIND: google-and-claude-"
             "enterprise-users-seats-and-token-costs (Glenn Hansen) is the first core-beat AI+spend "
             "request in fourteen runs - relevance 'high', our data answers it - but it has NO "
             "resolved route, so it is not sendable. The other six new rows are off-beat (patent/IP, "
             "IA careers, data-labelling labour, pro-bono law, APAC press, a martech vendor blog). "
             "The pair range held at 1.11x-2.53x over 19 tiers for the twelfth consecutive day "
             "against a snapshot refreshed to `updated: 2026-10-08` and a pair file rebuilt today. "
             "Mailbox: no reply to any tracked pitch; INBOX top is a ToolChase reply to the separate "
             "Sep-3 guest-pitch batch (msg 102), not this monitor. 0 pitches sent this run - sends "
             "remain George's lane. Figures correction to Jan Suski now 20 days outstanding. Defect "
             "fixed: the digest writer's `_new_this_run` flag was accumulating across carries (40 "
             "flags on a 7-new run) and is now popped on every carried row.")
})

LED.write_text(json.dumps(led, indent=1))
print("ledger updated:", LED)
print("notes len:", len(led["notes"]))
print("cold entries:", len(led["cold_without_a_send"]), "log entries:", len(led["log"]))
