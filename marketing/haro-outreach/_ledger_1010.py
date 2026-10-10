#!/usr/bin/env python3
"""Patch pitch-ledger.json for the 2026-10-10 run (notes, reply_status_checked, figures_disclosure,
cold_without_a_send entries, log entry). Loads, updates, writes - no hand-editing."""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
LED = D / "pitch-ledger.json"
led = json.loads(LED.read_text())

SHADOW = "fulltime-employees-shadow-ai-use-and-paying-outofpocket"
SPECFOOD = "speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech"


def _carried(slug: str) -> int:
    """Draft files that name this slug — measured on disk, not typed."""
    return sum(1 for f in D.glob("pitch-drafts-*.md") if slug in f.read_text(errors="ignore"))


led["notes"] = (
    "URL -> date or reason. Written by George or the agent when a pitch is sent or deliberately "
    "dropped, so build_pitch_queue.py stops resurfacing it. Pitches sent to date: 3. Replies "
    "received: 1. Zero pitches sent on 2026-09-29 through 2026-10-10 (twelve consecutive runs). "
    "2026-10-10 run: 107 tracked, 54 live unpitched, 49 cold unpitched, 2 sendable - the second "
    "sendable row is the one that matters: google-and-claude-enterprise-users-seats-and-token-costs "
    "(Glenn Hansen, editor of OPE+ / EPG Brand Acceleration) was carried as NOT SENDABLE for two runs "
    "for want of a route; the route was resolved this run off his own publication "
    "(ghansen@epgacceleration.com, published at ope-plus.com/2024/02/13/announcing-ope/19236, "
    "re-verified HTTP 200, 147,438 bytes, address present verbatim; epgacceleration.com MX = Microsoft "
    "365). It is the first core-beat AI+spend request this monitor has ever been able to send. The "
    "window produced 66 slugs, ZERO AI-token and zero spend-token; all 66 bodies were fetched and "
    "scanned, and exactly one mentions AI at all - to forbid the cliche 'more use of AI' - so the zero "
    "is a body-level measurement. Mailbox checked 2026-10-10: All Mail carries no message after "
    "2026-10-08 and exactly one inbound from any pitch recipient ever, Jan Suski's 2026-09-18 reply "
    "(msg 234); no reply to the Enterprise AI Leaders or Sherwood News sends, and nothing from "
    "raconteur.net, artichokehq.com or foxandspindle.com. INBOX top is still msg 104 (Anike "
    "Tobechukwu, on the separate AIDetector.cx affiliate thread); Sent top is msg 221 (2026-10-08), so "
    "no pitch-monitor mail has gone out since the 2026-09-18 Sherwood send. Separately: a "
    "paid-placement offer (Lilach Bullock, $300) arrived on a different outreach thread on 2026-09-29 "
    "and was declined same-day under editorial independence - that is not a pitch from this monitor "
    "and is not recorded as one."
)
led["reply_status_checked"] = "2026-10-10"

fd = led.get("figures_disclosure", {})
fd["date"] = "2026-10-10"
fd["status"] = (
    "STILL UNSENT - Day 22. The recipient of the 2026-09-18 Amplemarket reply was told the "
    "same-tier monthly/annual range is '1.21x-2.53x, median 1.33x'. The current verified figure is "
    "1.11x-2.53x, median 1.25x over 19 tiers. 2026-10-10: the 19-pair set was RE-READ, NOT REBUILT - "
    "data/monthly_annual_pairs.json stands on its 2026-10-08 build and the 19 curated pairs are "
    "unchanged; scripts/extract_monthly_annual_pairs.py has not been re-run against a 2026-10-10 "
    "snapshot this run, so the pair sentence stands on the 2026-10-08 build and says so. SEPARATELY, "
    "the shadow-AI headline figures were re-derived against today's refreshed snapshot "
    "(data/pricing_snapshots.json `updated: 2026-10-10`, 77 snapshots) and are unchanged: 42 of 77 "
    "tools quote a non-zero monthly price, 33 at or under $25/month, median $17.50. The numerator set "
    "is unchanged since 2026-10-02, so any sentence reading '42 of 76 tools' is superseded. Drafts "
    "written before 2026-10-02 that cite 40/31/$16.50 must not be sent. Day 22 unsent."
)
fd["action_required"] = (
    "Send Jan Suski a short correction. The thread is live and he replied to us on 2026-09-18, so an "
    "un-flagged wrong figure in a peer method discussion is worse than a follow-up. Send the CURRENT "
    "figure (1.11x-2.53x, median 1.25x over 19 tiers), not the 1.16x one from the 2026-09-21 drafts. "
    "Route: reply to jan@jansuski.com (In-Reply-To the existing thread). George's lane. Confirmed "
    "unsent again today: the only message ever sent to jansuski.com is msg 178, the 2026-09-18 reply."
)
fd["sendable_route_resolved_2026_10_10"] = (
    "A sendable row now exists that is not a late carry: google-and-claude-enterprise-users-seats-and-"
    "token-costs was carried for two runs as 'NO ROUTE RESOLVED', which was true of the request page "
    "and false of the world. The page's own author field names Glenn Hansen and the body states his "
    "beat (power equipment manufacturing), which identifies him as editor of OPE+ (EPG Brand "
    "Acceleration); OPE+ publishes 'Glenn Hansen, Editor - ghansen@epgacceleration.com' on its own "
    "site. Route-checks 2026-10-10: ope-plus.com/2024/02/13/announcing-ope/19236 HTTP 200, 147,438 "
    "bytes, address present verbatim; ope-plus.com/contact-us HTTP 200, 114,185 bytes, same editorial "
    "domain. MX = Microsoft 365. This is the class of defect the ledger exists to catch: a route "
    "declared absent because only the request page was read."
)
led["figures_disclosure"] = fd

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": "2026-10-10",
    "url": "https://www.sourcee.app/journo-request/google-and-claude-enterprise-users-seats-and-token-costs",
    "action": ("NEW AND SENDABLE - the route was RESOLVED today, two runs after this row was first "
               "carried as unsendable. Not a crossing: the opposite."),
    "note": ("The request page publishes no address, handle or link (email_redacted=False, "
             "emails_on_page=none) and the monitor recorded that as 'no route'. The page does name its "
             "author in its own author field and states his beat, which identifies him as Glenn "
             "Hansen, editor of OPE+ (EPG Brand Acceleration). OPE+ publishes his address on its own "
             "site: 'Glenn Hansen, Editor - ghansen@epgacceleration.com' at ope-plus.com/2024/02/13/"
             "announcing-ope/19236 (HTTP 200 today, 147,438 bytes, address present verbatim), with the "
             "same epgacceleration.com editorial domain named on ope-plus.com/contact-us (HTTP 200, "
             "114,185 bytes, ten other staff addresses). epgacceleration.com MX = Microsoft 365. "
             "Relevance 'high' and the best-matching request this monitor has held: the reporter asks "
             "for enterprise-level costs for AI seats and tokens, which data/tool_sources.json answers "
             "with dated figures (Claude Team $20/$100 per seat/month checked 2026-09-18; Gemini in "
             "Workspace from $8.40/$7 to $26.40/$22 per user/month checked 2026-09-18; GitHub Copilot "
             "Business $19 / Enterprise $39 per user/month with credits at $0.01 checked 2026-10-01; "
             "Microsoft 365 Copilot Business $18 promotional annual vs $21 list checked 2026-10-01). "
             "Draft: pitch-drafts-2026-10-10.md section 1. Not sent - sends are George's lane.")
})

led.setdefault("cold_without_a_send", []).insert(1, {
    "date": "2026-10-10",
    "url": ("https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-"
            "outofpocket, https://www.sourcee.app/journo-request/speciality-food-retailers-and-"
            "producers-how-theyd-spend-10k-on-tech"),
    "action": (f"both sent-ready drafts carried and republished again, still unsent — the shadow-AI "
               f"one now sits in {_carried(SHADOW)} draft files and the Speciality Food one in "
               f"{_carried(SPECFOOD)}. Figures re-derived against a snapshot refreshed to 2026-10-10 "
               "(77 tools, 42/33/$17.50); the pair file was RE-READ, not rebuilt, because its inputs "
               "were last rebuilt on 2026-10-08."),
    "note": ("Neither is void. Both pages returned HTTP 200 again today with the request body still "
             "served. The shadow-AI route was re-resolved against the live /contributors/"
             "simon-chandler page this run (HTTP 200, 154,984 bytes, data-part triple unchanged at "
             "simon.chandler+raconteur+net; control /contributors/tom-dennis HTTP 200 carries "
             "tom.dennis+raconteur+net; the older /author/simon-chandler/ still 404s), and the "
             "Speciality Food route was re-read off specialityfoodmagazine.com/contact (HTTP 200, "
             "59,488 bytes, alongside five other named masthead addresses). The Speciality Food "
             "October issue window has closed. What was lost is the ideal window, not the pitch.")
})

led.setdefault("cold_without_a_send", []).insert(2, {
    "date": "2026-10-10",
    "url": ("insurance-agents-ai-use-in-personal-lines, us-emergency-physicians-and-paramedics-impact-"
            "of-ai-answering-911-calls, job-seekers-and-recruiters-ai-recruitment-experiences"),
    "action": ("all three crossed the 10-day line today at 11 days, unpitched, none with a resolved "
               "route, none with a draft"),
    "note": ("All three were already relevance 'low', so the crossing cost nothing sendable - the "
             "sendable count is unchanged by them (it rose today, but for a different reason: the "
             "Glenn Hansen route was resolved). Named individually because build_pitch_queue.py's "
             "two-day advance warning covers only sendable rows, so an ordinary crossing otherwise "
             "shows up as nothing but the live count falling 57 -> 54. Four further rows sit at "
             "exactly 10 days and cross on the next run (cybersecurity-expert-ai-nexus-and-security-"
             "risks; chatbot-users-experiences-talking-to-ai; us-ai-security-experts-rogue-ai-agents-"
             "hitting-government-sites; real-estate-agents-pdf-brochures-vs-alternatives-agent-"
             "workflow) - all low or low-medium, none sendable."),
})

led.setdefault("log", []).insert(0, {
    "date": "2026-10-10",
    "event": ("monitor run - 0 new rows tracked (66-slug window, ZERO AI-token and zero spend-token, "
              "all 66 bodies read), 3 rows crossed cold, 1 route RESOLVED (first core-beat sendable "
              "row in monitor history), 2 sendable, no sends"),
    "url": "(no pitch)",
    "action": "none sent - 2 sendable rows carried (Glenn Hansen seats/tokens, 3 days old, email route; WSJ blocked-work-accounts, 5 days old, LinkedIn DM)",
    "to": None,
    "route": None,
    "sent_message_id": None,
    "note": ("107 tracked (101 carried and all 101 re-verified HTTP 200/live, 0 new rows, 3 pitched, 1 "
             "skipped), 54 live unpitched, 49 cold unpitched, 2 sendable. New window: 66 slugs, 0 "
             "AI-token, 0 spend-token. Because a slug-level zero cannot be confirmed by slug matching, "
             "all 66 window bodies were fetched and scanned for AI mentions: exactly one mentions AI "
             "(corporate-travel-managers-and-buyers-2027-trends-and-program-impact) and only to forbid "
             "the cliche. Window volume is down ~40% (66 vs 105) and the newest lastmod is "
             "2026-10-10T03:26:04Z, ~12 hours before the run: 2026-10-10 is a Saturday, so this is a "
             "weekend effect. THE FIND: the Glenn Hansen route was resolved off his own publication "
             "(ghansen@epgacceleration.com, ope-plus.com/2024/02/13/announcing-ope/19236, HTTP 200, "
             "147,438 bytes, address verbatim; epgacceleration.com MX = Microsoft 365). Headline "
             "figures re-derived and unchanged: 42 of 77 tools publish a monthly price, 33 at or under "
             "$25, median $17.50; pair range re-read at 1.11x-2.53x over 19 tiers. Mailbox: no reply to "
             "any tracked pitch; All Mail holds no message after 2026-10-08 and exactly one inbound "
             "from a pitch recipient ever (Jan Suski, 2026-09-18). 0 pitches sent this run - sends "
             "remain George's lane. Defects fixed: (1) a route declared absent because only the "
             "request page was read; (2) build_pitch_queue.py's _automatable() could not see an "
             "address recorded in `contact_method`; (3) the AI-topic-feed '100% overlap by "
             "construction' claim measured at 40/50 today and retired; (4) a slug-level zero confirmed "
             "at body level."),
})

LED.write_text(json.dumps(led, indent=1))
print("updated", LED)
print("log entries:", len(led["log"]), "| cold entries:", len(led["cold_without_a_send"]))
