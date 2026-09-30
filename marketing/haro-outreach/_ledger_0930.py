#!/usr/bin/env python3
"""Update pitch-ledger.json for the 2026-09-30 run: reply status, figures disclosure age, and the
day's cold-line crossings. Writes measured values only.
"""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
p = D / "pitch-ledger.json"
led = json.loads(p.read_text())

led["reply_status_checked"] = "2026-09-30"

led["reply_status"] = {
    "https://www.sourcee.app/journo-request/enterprise-ai-leaders-value-creation-ownership-and-governance":
        "no reply. Pitched 2026-09-15 to hello@foxandspindle.com (msg 171/172). Fifteen days of "
        "silence. This send crossed the 10-day cold line on 2026-09-25 and is 16 days old today.",
    "https://www.sourcee.app/journo-request/amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot":
        "REPLIED 2026-09-18 20:39Z from jan@jansuski.com; answered the same day 21:29Z (msg 178). "
        "Thread live, no further message from either side as of 2026-09-30. The reply told him a "
        "monthly/annual range that has since been proven wrong twice. See figures_disclosure - the "
        "correction is now TWELVE days outstanding.",
    "https://www.sourcee.app/journo-request/individual-contributors-managing-ai-agents-without-title-or-pay":
        "no reply. Pitched 2026-09-18 to Rani@Sherwood.news (msg 175/176). Twelve days of silence. "
        "Request is now 20 days old and well past the cold line.",
}

led["figures_disclosure"]["date"] = "2026-09-30"
led["figures_disclosure"]["status"] = (
    "STILL UNSENT - Day 12. The recipient of the 2026-09-18 Amplemarket reply was told the same-tier "
    "monthly/annual range is '1.21x-2.53x, median 1.33x'. The current verified figure is 1.11x-2.53x, "
    "median 1.25x over 19 tiers across 14 tools. 2026-09-23 through 2026-09-30: the 19-pair set "
    "RE-ASSERTED CLEAN against the refreshed snapshot on EIGHT consecutive days "
    "(data/pricing_snapshots.json updated 2026-09-30, extract_monthly_annual_pairs.py exit 0, no "
    "needle failures, data/monthly_annual_pairs.json rebuilt with built: 2026-09-30) - the longest "
    "stretch the figure has held since the assertion gate was added. The 1.16x floor in the "
    "2026-09-21 drafts, and the 138/136 word counts claimed in the 2026-09-23 drafts, are superseded "
    "and must not be sent. Day 12 unsent."
)
led["figures_disclosure"]["action_required"] = (
    "Send Jan Suski a short correction. The thread is live and he replied to us on 2026-09-18, so an "
    "un-flagged wrong figure in a peer method discussion is worse than a follow-up. Send the CURRENT "
    "figure (1.11x-2.53x, median 1.25x over 19 tiers), not the 1.16x one from the 2026-09-21 drafts. "
    "Route: reply to jan@jansuski.com (In-Reply-To the existing thread). George's lane."
)

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": "2026-09-30",
    "url": "https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business, "
           "https://www.sourcee.app/journo-request/ai-alignment-researchers-humanai-mutual-understanding",
    "action": "both crossed the 10-day line today at 11 days, unpitched, neither with a resolved route",
    "note": "The Forbes founders-cutting-AI row is the important one: build_pitch_queue.py counted it "
            "sendable for two consecutive runs (2026-09-28 and 2026-09-29) before the 2026-09-29 "
            "chrome-filter fix exposed that its only 'route' was Sourcee's own page chrome. Its body "
            "is explicit - 'Please only answer as a comment on this post. Do not email or DM me because "
            "they won't be used.' - and it wants a named founder's first-person account of cutting AI, "
            "which we do not have. So the crossing cost nothing sendable; it is logged here because the "
            "advance warning was pointed at it for two days and would otherwise read as a lost draft. "
            "The alignment-researchers row is low relevance with no email or handle on the page. Named "
            "because build_pitch_queue.py's two-day advance warning covers only sendable rows, so an "
            "ordinary crossing otherwise shows up as nothing but the live count falling 22 to 21.",
})
led.setdefault("cold_without_a_send", []).insert(0, {
    "date": "2026-09-30",
    "url": "https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket, "
           "https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech",
    "action": "both sent-ready drafts carried and republished again, still unsent (thirteenth run; fifth run)",
    "note": "Neither is void. Both pages returned HTTP 200 again today with the request body still "
            "served, and both routes were re-resolved against the live pages this run: "
            "simon.chandler@raconteur.net off /contributors/simon-chandler (HTTP 200, 154,857 bytes, "
            "data-part1/2/3 unchanged at simon.chandler + raconteur + net; control /contributors/"
            "tom-dennis HTTP 200, 154,062 bytes, carries tom.dennis/raconteur/net; the older "
            "/author/simon-chandler/ still 404s), and holly.shackleton@artichokehq.com off "
            "specialityfoodmagazine.com/contact (HTTP 200, 59,500 bytes, byte-count unchanged, "
            "alongside five other named masthead addresses). The shadow-AI draft is now unsent through "
            "THIRTEEN consecutive runs; the Speciality Food draft has been carried five times and its "
            "October window has closed. What was lost is the ideal window, not the pitch.",
})

led.setdefault("log", []).append({
    "date": "2026-09-30",
    "event": "monitor run - 0 sendable, 3 new AI-token tracked, 0 AI+spend (8th consecutive), no sends",
    "detail": "54 tracked (51 carried and all 51 re-verified HTTP 200/live, 3 new AI-token finds), 22 "
              "live unpitched, 28 cold unpitched, 0 sendable. New window: 113 slugs, 3 AI-token, 0 "
              "AI+spend, 10 spend-token (all consumer cost-of-living / sport / personal finance). All "
              "13 candidates fetched and read in full. Pair range held at 1.11x-2.53x over 19 tiers "
              "for the eighth consecutive day against a snapshot refreshed today. Mailbox: no reply to "
              "any tracked pitch; sent mail top is still msg 189 (2026-09-29), so nothing has gone out "
              "since. 0 pitches sent this run - sends remain George's lane.",
})

p.write_text(json.dumps(led, indent=2) + "\n")
print("updated", p)
print("reply_status_checked:", led["reply_status_checked"])
print("cold_without_a_send entries:", len(led["cold_without_a_send"]))
print("log entries:", len(led.get("log", [])))
print("pitched:", len(led["pitched"]), "skipped:", len(led["skipped"]))
