#!/usr/bin/env python3
"""Update pitch-ledger.json for 2026-09-29: reply status, the figures correction, and the paid-
placement exchange on the separate subscription-creep thread. Nothing is marked pitched."""
import json, re
from datetime import date
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
led = json.loads((D / "pitch-ledger.json").read_text())
TODAY = "2026-09-29"

led["reply_status_checked"] = TODAY
led["reply_status"] = {
    "https://www.sourcee.app/journo-request/enterprise-ai-leaders-value-creation-ownership-and-governance":
        "no reply. Pitched 2026-09-15 to hello@foxandspindle.com (msg 171/172). Fourteen days of "
        "silence. This send crossed the 10-day cold line on 2026-09-25 and is 15 days old today.",
    "https://www.sourcee.app/journo-request/amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot":
        "REPLIED 2026-09-18 20:39Z from jan@jansuski.com; answered the same day 21:29Z (msg 178). "
        "Thread live, no further message from either side as of 2026-09-29. The reply told him a "
        "monthly/annual range that has since been proven wrong twice. See figures_disclosure - the "
        "correction is now ELEVEN days outstanding.",
    "https://www.sourcee.app/journo-request/individual-contributors-managing-ai-agents-without-title-or-pay":
        "no reply. Pitched 2026-09-18 to Rani@Sherwood.news (msg 175/176). Eleven days of silence. "
        "Request is now 19 days old and well past the cold line.",
}

led["figures_disclosure"] = {
    "date": TODAY,
    "status": ("STILL UNSENT - Day 11. The recipient of the 2026-09-18 Amplemarket reply was told the "
               "same-tier monthly/annual range is '1.21x-2.53x, median 1.33x'. The current verified "
               "figure is 1.11x-2.53x, median 1.25x over 19 tiers across 14 tools. 2026-09-23 through "
               "2026-09-29: the 19-pair set RE-ASSERTED CLEAN against the refreshed snapshot on SEVEN "
               "consecutive days (data/pricing_snapshots.json updated 2026-09-29, "
               "extract_monthly_annual_pairs.py exit 0, no needle failures) - the longest stretch the "
               "figure has held since the assertion gate was added. The 1.16x floor in the 2026-09-21 "
               "drafts, and the 138/136 word counts claimed in the 2026-09-23 drafts, are superseded "
               "and must not be sent. Day 11 unsent."),
    "action_required": ("Send Jan Suski a short correction. The thread is live and he replied to us on "
                        "2026-09-18, so an un-flagged wrong figure in a peer method discussion is worse "
                        "than a follow-up. Send the CURRENT figure (1.11x-2.53x, median 1.25x over 19 "
                        "tiers), not the 1.16x one from the 2026-09-21 drafts. Route: reply to "
                        "jan@jansuski.com (In-Reply-To the existing thread). George's lane."),
    "source_of_truth": ("data/monthly_annual_pairs.json, re-asserted by "
                        "scripts/extract_monthly_annual_pairs.py, which refuses to write the file "
                        "unless all 19 curated pairs re-assert against the live snapshot"),
    "superseded_word_counts_note": ("The 2026-09-23 drafts claimed 138 and 136 words for the shadow-AI "
                                    "and Speciality Food bodies. As republished in the 2026-09-29 "
                                    "drafts they measure 194 and 197 words including the subject line "
                                    "and signature (the verifier measures them rather than asserting "
                                    "them)."),
    "carried_record_repair": ("2026-09-29: build_pitch_queue.py's DRAFTS and DRAFT_INDEX blocks were "
                              "hand-written prose for six consecutive runs and had drifted to a "
                              "crossing date that was already a day old. They are now derived at build "
                              "time from verified-requests.json, so an age in the queue is always a "
                              "figure that run measured."),
}

led["notes"] = (
    "URL -> date or reason. Written by George or the agent when a pitch is sent or deliberately "
    "dropped, so build_pitch_queue.py stops resurfacing it. Pitches sent to date: 3. Replies "
    "received: 1. Zero sent on 2026-09-29. The queue is at ZERO SENDABLE, and on 2026-09-29 it took a "
    "code fix to establish that: the run's own refresh script had dropped Sourcee's two own social "
    "links from its chrome filter, so a page's own chrome landed in published_links and _sendable() "
    "read it as a reply route, reporting 1 sendable (a comment-only Forbes request). Filter restored, "
    "queue re-built, true count 0. Separately: a paid-placement offer (Lilach Bullock, $300) arrived "
    "on a different outreach thread and was declined same-day under editorial independence - that is "
    "not a pitch from this monitor and is not recorded as one."
)

led["declined_paid_placements"] = {
    "2026-09-29": {
        "from": "Lilach Bullock <lilachbullock@gmail.com>",
        "offer": ("$300 paid product placement in a relevant existing article, plus wider partnership "
                  "options incl. newsletter features; newsletter reaches ~15,000; 50% September "
                  "discount."),
        "outcome": ("Declined the same day in-thread (Sent msg 189, 2026-09-29 15:52-07:00), signed "
                    "AIToolsEssentials, no personal name; offered the free tool for editorial mention "
                    "at her discretion."),
        "reason": "budget and editorial-independence position; consistent with the prior declines",
        "thread": "subscription-creep resource pitch (not a HARO/Sourcee pitch)",
    }
}

(D / "pitch-ledger.json").write_text(json.dumps(led, indent=2))
print("updated pitch-ledger.json")
print("pitched:", len(led["pitched"]), "skipped:", len(led["skipped"]))
print("reply_status_checked:", led["reply_status_checked"])
