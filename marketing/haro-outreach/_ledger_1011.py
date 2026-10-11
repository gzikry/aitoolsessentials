#!/usr/bin/env python3
"""Patch pitch-ledger.json for the 2026-10-11 run.

Records the monitor run, the corrected send count, the mailbox check and the crossings. Touches no
`pitched` entry: nothing was sent this run, and a pitch that was not sent is not progress.
"""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
LED = D / "pitch-ledger.json"
led = json.loads(LED.read_text())

led["notes"] += (
    " || 2026-10-11 run: 114 tracked, 56 live unpitched, 58 cold unpitched, 1 sendable. THE SEND COUNT IN "
    "THE FIRST LINE OF THIS FIELD ('Pitches sent to date: 3') IS SUPERSEDED: the pitched map holds 6 URLs - "
    "5 delivered (enterprise-ai-leaders 2026-09-15; amplemarket 2026-09-18; individual-contributors 2026-09-18; "
    "google-and-claude-enterprise-users-seats-and-token-costs 2026-10-10; speciality-food-retailers 2026-10-10) "
    "and 1 bounced (fulltime-employees-shadow-ai-use-and-paying-outofpocket, 550 NoSuchUser). The 2026-10-10 "
    "21:20 UTC send was the first in 22 days and the largest single send this monitor has recorded. The "
    "Amplemarket thread is closed (vendor acknowledged the figures correction 2026-10-11 06:57 UTC) and must "
    "not be bumped. The only sendable row carried into today is the WSJ blocked-work-accounts request, now 6 "
    "days old, drafted at pitch-drafts-2026-10-11.md section 1, route LinkedIn DM to "
    "linkedin.com/in/christopher-mims-club/ - George's lane, still unsent through two runs. "
    "DEFECT FIXED THIS RUN: the per-run AI regex listed product classes and no vendor names, so "
    "anthropic-gtm-leaders-scaling-300k-b2b-clients was fetched inside the 2026-10-10 window and then dropped "
    "without being tracked; the token set now lives in scripts/sourcee_terms.py with vendor and product names "
    "and the per-run window script imports it. Measured against today's full 40,299-slug sitemap the fix "
    "recovers 63 slugs the old filter missed, 3 of them AI+spend, including "
    "anthropic-api-users-costs-and-token-burn-increase-since-january (Ed Zitron, 162 days, still live, never "
    "tracked until today). Two candidate tokens were rejected after measuring them ('make' and bare 'token'), "
    "which is the difference between 85 and 63 new slugs. MAILBOX CHECKED 2026-10-11: All Mail top is msg 305, "
    "the vendor's courtesy acknowledgment on the Amplemarket thread; nothing newer, no reply to either of the "
    "two pitches delivered on 2026-10-10 21:20 UTC (19 hours old), and no reply to the two September sends."
)

led["reply_status_checked"] = "2026-10-11"

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": "2026-10-11",
    "url": ("https://www.sourcee.app/journo-request/chatbot-users-experiences-talking-to-ai, "
            "https://www.sourcee.app/journo-request/cybersecurity-expert-ai-nexus-and-security-risks, "
            "https://www.sourcee.app/journo-request/real-estate-agents-pdf-brochures-vs-alternatives-agent-workflow, "
            "https://www.sourcee.app/journo-request/us-ai-security-experts-rogue-ai-agents-hitting-government-sites"),
    "action": "crossed the 10-day line today at 11 days, all four unpitched, none ever drafted",
    "note": ("All four are relevance 'low' and none was ever inside the sendable count, so the crossing cost "
             "nothing. Three of the four name a reply route in the form 'DM the poster' or 'reply to the "
             "original post' - a route on the poster's own platform, not on Sourcee - so none of them was "
             "actionable from here on any day of the ten. Seven more rows sit at exactly 10 days and cross "
             "tomorrow, all of them also 'low' or 'low-medium' and route-less; they are named in "
             "digest-2026-10-11.json so the next quiet count change is not mistaken for a quiet week."),
})

led.setdefault("log", []).append({
    "date": "2026-10-11",
    "event": ("monitor run - 36-slug window, 2 AI-token, 1 spend-only, 0 AI+spend; 7 rows added including 3 "
              "recovered by the vendor-token fix; 4 rows crossed cold; 1 sendable; no sends"),
    "detail": ("114 tracked (107 carried, all 107 re-verified HTTP 200/live with every deadline field rebuilt "
               "from the page's own badge and datePublished; 7 added), 56 live unpitched, 58 cold unpitched, "
               "1 sendable. New window: 36 slugs (up from 66), 2 AI-token, 0 AI+spend, 1 spend-only "
               "(employees-pay-transparency-good-or-bad - payroll, not purchasing). All four AI/spend-relevant "
               "window bodies were fetched and read. FEED MEASUREMENT: the AI topic page is a rolling 50-slot "
               "window (35 of 50 carried over from 2026-10-10, 15 turned over) and ZERO of the 114 tracked rows "
               "appear in it on either day, so feed membership is recorded on every row and used in no ranking. "
               "Mailbox: All Mail top is msg 305 (vendor acknowledgment, 2026-10-11 06:57 UTC); no new reply to "
               "any pitch, and none to either of the two deliveries from 2026-10-10 21:20 UTC. 0 pitches sent "
               "this run - sends remain George's lane. Figures re-derived against data/pricing_snapshots.json "
               "updated 2026-10-11: 42 of 77 tools publish a monthly price, 33 at or under $25/month, median "
               "$17.50; pairs 1.11x-2.53x, median 1.25x over 19 tiers (built 2026-10-08, re-read not rebuilt)."),
})

LED.write_text(json.dumps(led, indent=1))
print("ledger updated: notes extended, reply_status_checked =", led["reply_status_checked"])
print("pitched entries (unchanged):", len(led["pitched"]))
print("log entries:", len(led["log"]), "| cold_without_a_send entries:", len(led["cold_without_a_send"]))
