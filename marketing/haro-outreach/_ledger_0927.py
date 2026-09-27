#!/usr/bin/env python3
"""Update the ledger for the 2026-09-27 run, keeping the JSON valid.

Three things the ledger has to carry forward:
  * the mail/reply check date and what it found today;
  * the figures-disclosure clock on the Jan Suski correction (now nine days);
  * the crossings that happened today, including the shadow-AI row that is about to cross
    unpitched with a paste-ready draft.
"""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
p = D / "pitch-ledger.json"
led = json.loads(p.read_text())
TODAY = "2026-09-27"

led["reply_status_checked"] = TODAY

led["figures_disclosure"]["date"] = TODAY
led["figures_disclosure"]["status"] = (
    "STILL UNSENT - Day 9. The recipient of the 2026-09-18 Amplemarket reply was told the same-tier "
    "monthly/annual range is '1.21x-2.53x, median 1.33x'. The current verified figure is 1.11x-2.53x, "
    "median 1.25x over 19 tiers across 14 tools. 2026-09-23 through 2026-09-27: the 19-pair set "
    "RE-ASSERTED CLEAN against the refreshed snapshot on FIVE consecutive days (data/pricing_snapshots.json "
    "updated 2026-09-27, extract_monthly_annual_pairs.py exit 0, no needle failures) - the longest "
    "stretch the figure has held since the assertion gate was added. The 1.16x floor in the 2026-09-21 "
    "drafts, and the 138/136 word counts claimed in the 2026-09-23 drafts, are superseded and must not "
    "be sent. Day 9 unsent."
)
led["figures_disclosure"]["action_required"] = (
    "Send Jan Suski a short correction. The thread is live and he replied to us on 2026-09-18, so an "
    "un-flagged wrong figure in a peer method discussion is worse than a follow-up. Send the CURRENT "
    "figure (1.11x-2.53x, median 1.25x over 19 tiers), not the 1.16x one from the 2026-09-21 drafts. "
    "Route: reply to jan@jansuski.com (In-Reply-To the existing thread). George's lane."
)

led["reply_status"]["https://www.sourcee.app/journo-request/enterprise-ai-leaders-value-creation-ownership-and-governance"] = (
    "no reply. Pitched 2026-09-15 to hello@foxandspindle.com (msg 171/172). INBOX, All Mail, Sent Mail, "
    "Spam and Trash all re-checked 2026-09-27. Twelve days of silence. This send crossed the 10-day "
    "cold line on 2026-09-25 and is 13 days old today."
)
led["reply_status"]["https://www.sourcee.app/journo-request/amplemarket-growth-and-elite-customers-pricing-credits-and-duo-copilot"] = (
    "REPLIED 2026-09-18 20:39Z from jan@jansuski.com; answered the same day 21:29Z (msg 178). Thread "
    "live, no further message from either side as of 2026-09-27. The correspondence asked whether a "
    "dynamically re-checked pricing database would make sense; the reply answered it as a peer method "
    "discussion - and then repeated a monthly/annual range that has since been proven wrong twice. See "
    "figures_disclosure. The correction is now NINE days outstanding."
)
led["reply_status"]["https://www.sourcee.app/journo-request/individual-contributors-managing-ai-agents-without-title-or-pay"] = (
    "no reply. Pitched 2026-09-18 to Rani@Sherwood.news (msg 175/176). Nine days of silence. Request "
    "is now 17 days old and well past the cold line."
)

# Newest crossings first: the ledger's list is read newest-to-oldest.
led["cold_without_a_send"] = [
    {
        "date": TODAY,
        "url": "https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket",
        "action": "LAST LIVE DAY - crosses TOMORROW, unpitched, with a paste-ready draft",
        "note": (
            "10 days old today and sendable; it crosses the 10-day line tomorrow. This is the row the "
            "monitor has been watching for a week, and today is the last day it counts as sendable. The "
            "draft has been written and unsent for NINE consecutive runs (pitch-drafts-2026-09-27.md "
            "section 1, figures re-derived today against a snapshot refreshed today). Route "
            "simon.chandler@raconteur.net re-resolved off the live /contributors/simon-chandler page "
            "today (HTTP 200, 154,797 bytes, data-part1/2/3 triple unchanged). It is the only "
            "high-relevance request this queue has ever held with a finished draft, so if it crosses "
            "unpitched it is the first high-relevance loss of that kind. Logged on the day it can still "
            "be prevented, not after the fact."
        ),
    },
    {
        "date": TODAY,
        "url": "https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech",
        "action": "one day from the line - crosses TOMORROW, unpitched, with a paste-ready draft",
        "note": (
            "9 days old and sendable; crosses the day after the shadow-AI row and its October issue "
            "window is closing. Draft re-verified today at pitch-drafts-2026-09-27.md section 2, route "
            "holly.shackleton@artichokehq.com re-read today off specialityfoodmagazine.com/contact "
            "(HTTP 200, 59,500 bytes, alongside five other named masthead addresses). Standing "
            "constraint stated in the draft's first line: we are not a food retailer."
        ),
    },
    {
        "date": TODAY,
        "url": ("https://www.sourcee.app/journo-request/cybersecurity-companies-and-experts-ai-scams-and-consumer-safety, "
                "https://www.sourcee.app/journo-request/us-founders-calls-to-slow-ai-development-impact-on-companies"),
        "action": "crossed the 10-day line today at 11 days, both unpitched, neither ever had a draft",
        "note": (
            "Both low/low-medium relevance and neither has ever had a resolved reply route, so nothing "
            "sendable was lost. Named because build_pitch_queue.py's two-day advance warning covers only "
            "sendable rows, so an ordinary crossing otherwise shows up as nothing but the live count "
            "falling from 26 to 24. Logged so that a quiet count change is never mistaken for a quiet "
            "week."
        ),
    },
] + led["cold_without_a_send"]

led["notes"] = (
    "URL -> date or reason. Written by George or the agent when a pitch is sent or deliberately "
    "dropped, so build_pitch_queue.py stops resurfacing it. Pitches sent to date: 3. Replies received: "
    "1. Zero sent on 2026-09-27."
)

p.write_text(json.dumps(led, indent=2))
print("ledger updated:", p)
print("cold_without_a_send entries:", len(led["cold_without_a_send"]))
print("reply_status_checked:", led["reply_status_checked"])
json.loads(p.read_text())
print("re-parsed OK")
