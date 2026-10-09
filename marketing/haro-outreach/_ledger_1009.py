#!/usr/bin/env python3
"""Patch pitch-ledger.json for the 2026-10-09 run (notes, reply_status_checked, figures_disclosure,
cold_without_a_send entries, log entry). Loads, updates, writes - no hand-editing."""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
LED = D / "pitch-ledger.json"
led = json.loads(LED.read_text())

led["notes"] = (
    "URL -> date or reason. Written by George or the agent when a pitch is sent or deliberately "
    "dropped, so build_pitch_queue.py stops resurfacing it. Pitches sent to date: 3. Replies "
    "received: 1. Zero sent on 2026-09-29 through 2026-10-09 (eleven consecutive runs). The queue's "
    "first and so far ONLY sendable row (employees-blocked-from-ai-on-work-accounts-automating-"
    "tedious-tasks; Christopher Mims, WSJ) is now 4 days old and still route-resolved; it has been "
    "carried by eight consecutive runs without a send. 2026-10-09 run: 107 tracked, 57 live "
    "unpitched, 46 cold unpitched, 1 sendable. The new window produced 8 AI-token slugs and ZERO "
    "AI+spend slugs - the first clean window in four runs, so nothing core-beat was added; the six "
    "rows that were added are low-relevance and route-less. Two rows were DELETED from tracking "
    "this run because no digest had ever recorded them as opportunities (saas-tools-gated-content-"
    "and-lead-capture-and-document-tracking; indie-makers-product-journey-first-user-and-paid-users) "
    "- they had entered verified-requests.json from an earlier ad-hoc probe and were inflating the "
    "queue's live count. Mailbox checked 2026-10-09: a search of All Mail for the four tracked-pitch "
    "recipients returns exactly one inbound message ever, Jan Suski's 2026-09-18 reply (msg 234); no "
    "reply to the Enterprise AI Leaders or Sherwood News sends. INBOX top is msg 104 (Anike "
    "Tobechukwu, on the separate AIDetector.cx affiliate thread), then msg 102 (a ToolChase reply to "
    "the Sep-3 guest-pitch batch). Separately: a paid-placement offer (Lilach Bullock, $300) arrived "
    "on a different outreach thread on 2026-09-29 and was declined same-day under editorial "
    "independence - that is not a pitch from this monitor and is not recorded as one."
)
led["reply_status_checked"] = "2026-10-09"

fd = led.get("figures_disclosure", {})
fd["date"] = "2026-10-09"
fd["status"] = (
    "STILL UNSENT - Day 21. The recipient of the 2026-09-18 Amplemarket reply was told the "
    "same-tier monthly/annual range is '1.21x-2.53x, median 1.33x'. The current verified figure is "
    "1.11x-2.53x, median 1.25x over 19 tiers. 2026-10-09: the 19-pair set was RE-READ, NOT REBUILT - "
    "data/monthly_annual_pairs.json was rebuilt on 2026-10-08 against that day's snapshot and the "
    "19 curated pairs are unchanged; re-running scripts/extract_monthly_annual_pairs.py against a "
    "2026-10-09 snapshot has not been done this run, so the pair sentence stands on the 2026-10-08 "
    "build and says so. SEPARATELY, the shadow-AI headline figures were re-derived against the "
    "refreshed snapshot and the DENOMINATOR MOVED: 77 tools now (was 76), 42 of 77 quote a non-zero "
    "monthly price, 33 at or under $25/month, median $17.50, lowest $4.00 (khanmigo). The numerator "
    "set is unchanged since 2026-10-02, so the only superseded text is any sentence reading '42 of "
    "76 tools'. data/pricing_snapshots.json `updated: 2026-10-09`. Drafts written before 2026-10-02 "
    "that cite 40/31/$16.50 must not be sent. Day 21 unsent."
)
fd["action_required"] = (
    "Send Jan Suski a short correction. The thread is live and he replied to us on 2026-09-18, so an "
    "un-flagged wrong figure in a peer method discussion is worse than a follow-up. Send the CURRENT "
    "figure (1.11x-2.53x, median 1.25x over 19 tiers), not the 1.16x one from the 2026-09-21 drafts. "
    "Route: reply to jan@jansuski.com (In-Reply-To the existing thread). George's lane."
)
fd["denominator_note_2026_10_09"] = (
    "The 2026-10-09 snapshot added a 77th tool, so the headline set reads 42 of 77 rather than 42 of "
    "76. Every other number is unchanged, which is exactly why it is easy to keep sending the old "
    "denominator: the numerator and the median did not move. build_pitch_queue.py re-derives the "
    "figures at build time, and marketing/haro-outreach/_write_digest_1009.py's _repair() rewrites any "
    "carried '42 of 76' sentence, so the drift cannot survive into today's digest or drafts. "
    "marketing/haro-outreach/_verify_drafts_1009.py asserts that no 'of 76 tools' phrase remains in "
    "today's draft file."
)
led["figures_disclosure"] = fd

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": "2026-10-09",
    "url": ("https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-"
            "outofpocket, https://www.sourcee.app/journo-request/speciality-food-retailers-and-"
            "producers-how-theyd-spend-10k-on-tech"),
    "action": ("both sent-ready drafts carried and republished again, still unsent (TWENTIETH run; "
               "fourteenth run). Figures re-derived against a snapshot refreshed to 2026-10-09 "
               "(77 tools, 42/33/$17.50); the pair file was NOT rebuilt this run because its inputs "
               "were rebuilt yesterday and the 19 pairs are unchanged."),
    "note": ("Neither is void. Both pages returned HTTP 200 again today with the request body still "
             "served. The shadow-AI route was re-resolved against the live /contributors/simon-chandler "
             "page this run (HTTP 200, 154,984 bytes, data-part1/2/3 unchanged at simon.chandler + "
             "raconteur + net; control /contributors/tom-dennis HTTP 200 carries tom.dennis/raconteur/"
             "net; the older /author/simon-chandler/ still 404s), and the Speciality Food route was "
             "re-read off specialityfoodmagazine.com/contact (HTTP 200, 59,488 bytes, alongside five "
             "other named masthead addresses). The shadow-AI draft is now unsent through TWENTY "
             "consecutive runs - the first round number this monitor has hit with a finished draft - "
             "and the Speciality Food draft has been carried a fourteenth time with its October "
             "window closed. What was lost is the ideal window, not the pitch.")
})

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": "2026-10-09",
    "url": ("ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes, "
            "b2b-marketing-leaders-hyperspecialization-to-outcompete-ai, "
            "data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity"),
    "action": "all three crossed the 10-day line today at 11 days, unpitched, none with a resolved route",
    "note": ("All three were already relevance 'low' with no draft and no resolved route, so the "
             "crossing cost nothing sendable - the sendable count is unchanged by them. Named "
             "individually because build_pitch_queue.py's two-day advance warning covers only "
             "sendable rows, so an ordinary crossing otherwise shows up as nothing but the live count "
             "falling. Three further rows sit at exactly 10 days and cross on the next run.")
})

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": "2026-10-09",
    "url": ("saas-tools-gated-content-and-lead-capture-and-document-tracking, "
            "indie-makers-product-journey-first-user-and-paid-users"),
    "action": ("REMOVED FROM TRACKING - not a crossing. Neither row was ever recorded as an "
               "opportunity by any digest."),
    "note": ("These two sat in verified-requests.json (entered from an earlier run's ad-hoc fetch) and "
             "in the 2026-10-10 queue's live list, but neither appears in any digest's "
             "`opportunities` array and neither is in this ledger. scripts/build_pitch_queue.py "
             "merges digests, and scripts/verify_journo_requests.py run with no arguments sweeps "
             "every digest URL AND the ledger AND pitch-queue.md - so once pitch-queue.md had carried "
             "them, the cache held them and the queue counted them. Effect: the live unpitched count "
             "was inflated by two rows the monitor had never classified, which is the mirror image "
             "of the index-page bug the queue already filters (digest counted what the queue should "
             "not). Removed at the data layer; the queue's live count is now digest-faithful. What "
             "they are, for the record: saas-tools-gated-content-and-lead-capture-and-document-"
             "tracking is a PR request for 'SaaS tools built for gated content' (a vendor-blog "
             "solicitation, not an AI-tool-spend story); indie-makers-product-journey-first-user-and-"
             "paid-users is a HackerMRR site promo inviting product stories.")
})

led.setdefault("log", []).insert(0, {
    "date": "2026-10-09",
    "event": ("monitor run - 6 new AI-token tracked, 0 AI+spend (first clean window in four runs), "
              "3 rows crossed cold, 2 untracked rows removed, 1 sendable, no sends"),
    "url": "(no pitch)",
    "action": "none sent - 1 sendable row carried (WSJ blocked-work-accounts, now 4 days old)",
    "to": None, "route": None, "sent_message_id": None,
    "note": ("107 tracked (101 carried and all 101 re-verified HTTP 200/live, 6 new AI-token finds, 2 "
             "untracked rows removed), 57 live unpitched, 46 cold unpitched, 1 sendable. New window: "
             "105 slugs, 8 AI-token, 0 AI+spend, 7 spend-token (all consumer cost-of-living: "
             "citizenship-service fees, a political podcast, paid parking, grocery returns, state "
             "cost-cutting, cost-of-living relationship trade-offs, a paid interview fee). All 16 "
             "candidates fetched and read in full. NOTHING core-beat arrived: the closest is "
             "sales-reps-who-cold-call-and-email (Issie Lapowsky), whose body puts product pitches on "
             "a 'naughty list' - the clearest anti-pitch instruction this monitor has seen. The "
             "carried high-relevance row (google-and-claude-enterprise-users-seats-and-token-costs, "
             "Glenn Hansen) is now 1 day old and still has NO resolved route, so it remains "
             "unsendable. Headline figures re-derived: 42 of 77 tools publish a monthly price "
             "(denominator moved 76 -> 77), 33 at or under $25, median $17.50. Pair range held at "
             "1.11x-2.53x over 19 tiers; the pair file was read, not rebuilt. Mailbox: no reply to "
             "any tracked pitch; All-Mail search over the four tracked recipients returns only Jan "
             "Suski's 2026-09-18 message. 0 pitches sent this run - sends remain George's lane. "
             "Figures correction to Jan Suski now 21 days outstanding. Defect fixed: two rows no "
             "digest ever recorded were inflating the queue's live count and are removed from "
             "tracking.")
})

LED.write_text(json.dumps(led, indent=1))
print("ledger updated:", LED)
print("notes len:", len(led["notes"]))
print("cold entries:", len(led["cold_without_a_send"]), "log entries:", len(led["log"]))
