#!/usr/bin/env python3
"""Record the 2026-10-12 monitor run in marketing/haro-outreach/pitch-ledger.json.

No send is recorded here — sends are George's lane and this run sent nothing. This writes only what
the run measured: the mailbox re-check (no new reply), the seven rows that crossed the 10-day cold
line unpitched, and the run's own log line.
"""
from __future__ import annotations

import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
LED = D / "pitch-ledger.json"
led = json.loads(LED.read_text())

led["reply_status_checked"] = "2026-10-12"
led.setdefault("reply_status", {})

# Re-runnable: drop anything this script wrote on an earlier attempt today, so a second run
# corrects the record instead of stacking a duplicate on top of it.
led["log"] = [e for e in led.get("log", []) if e.get("date") != "2026-10-12"]
led["cold_without_a_send"] = [e for e in led.get("cold_without_a_send", []) if e.get("date") != "2026-10-12"]

CROSSED = [
    "ai-glasses-owners-users-and-developers-in-india-product-experience",
    "ai-summit-barcelona-attendees-controversy-and-experiences",
    "employees-conflicted-about-ai-use-generative-ai-workplace-impact",
    "fb-marketplace-sellers-ai-photos-and-description-prompts",
    "fea-engineers-using-agentic-ai-practitioner-case-study",
    "k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact",
    "parents-ai-acting-as-pseudoparent-in-kid-questions",
]

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": "2026-10-12",
    "url": ", ".join(f"https://www.sourcee.app/journo-request/{s}" for s in CROSSED),
    "action": "crossed the 10-day line today at 11 days, all seven unpitched, none ever drafted",
    "note": (
        "All seven were named in advance by the 2026-10-11 digest as sitting at 10 days, so this is a "
        "scheduled crossing and not new information. All seven are relevance 'low', none has a draft, and "
        "none has ever been inside the sendable count, so the crossing cost nothing. Five more rows sit at "
        "exactly 10 days and cross tomorrow: storytellers-and-brand-founders-marys-big-30-ai-story-project, "
        "newsletter-editors-using-ai-agents-news-aggregation-practices, "
        "scottish-teachers-ai-tools-implementation-in-education, "
        "law-firm-lawyers-concrete-ai-implementations-and-billing-impact, "
        "hr-leaders-company-ai-strategies-and-cognitive-offloading-risk - all 'low' or 'low-medium' and "
        "route-less, named so the next quiet count change is not mistaken for a quiet week."
    ),
})

led.setdefault("log", []).append({
    "date": "2026-10-12",
    "event": ("monitor run - 33-slug window, 3 AI-token, 0 AI+spend; 3 rows added; 7 rows crossed cold; "
              "1 sendable; no sends; queue build was broken by yesterday's route-checks shape and fixed"),
    "detail": (
        "117 tracked (114 carried, all 114 re-verified HTTP 200/live with every deadline field rebuilt from "
        "the page's own badge and datePublished; 3 added - every AI-token slug in the window, none a candidate), "
        "49 live unpitched, 61 cold unpitched, 1 sendable. New window: 33 slugs, 3 AI-token, 0 AI+spend, "
        "2 spend-only and both false positives (a consumer refund story and a college decision). All 33 window "
        "bodies fetched and read in full, which is the only check that can back a zero. Mailbox: INBOX top is "
        "msg 111 (a FormSubmit tool submission, 2026-10-12 10:21 UTC) and All Mail top is msg 314 (our own "
        "vendor-verification request); no reply has arrived to either of the two deliveries from 2026-10-10 "
        "21:20 UTC, and the Amplemarket thread stays closed by the vendor's own acknowledgment. 0 pitches sent "
        "this run - sends remain George's lane. CODE FIX: scripts/build_pitch_queue.py read only the newest "
        "route-checks-*.json and assumed its `routes` was a dict; the 2026-10-11 probe wrote it as a list, so "
        "the queue build died with \"'list' object has no attribute 'get'\" and pitch-queue.md was not written "
        "at all. Both shapes are now read, normalised to one scheme-stripped key and MERGED across files so a "
        "route the newest probe did not re-measure keeps its last verified evidence. Figures re-derived against "
        "data/pricing_snapshots.json updated 2026-10-12: 42 of 77 tools publish a monthly price, 33 at or under "
        "$25/month, median $17.50; pairs 1.11x-2.53x, median 1.25x over 19 tiers (built 2026-10-08, re-read "
        "not rebuilt)."
    ),
})

LED.write_text(json.dumps(led, indent=1))
print("ledger updated:", LED)
print("reply_status_checked =", led["reply_status_checked"])
print("cold_without_a_send entries:", len(led["cold_without_a_send"]), "| log entries:", len(led["log"]))
