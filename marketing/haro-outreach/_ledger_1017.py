#!/usr/bin/env python3
"""Record the 2026-10-17 monitor run in marketing/haro-outreach/pitch-ledger.json.

No send is recorded here — sends are George's lane and this run sent nothing. This writes only what
the run measured: the mailbox re-check (no new reply), the ten rows that crossed the 10-day cold line
unpitched, and the run's own log line.
"""
from __future__ import annotations

import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
LED = D / "pitch-ledger.json"
led = json.loads(LED.read_text())

led["reply_status_checked"] = "2026-10-17"
led.setdefault("reply_status", {})

# Re-runnable: drop anything this script wrote on an earlier attempt today.
led["log"] = [e for e in led.get("log", []) if e.get("date") != "2026-10-17"]
led["cold_without_a_send"] = [e for e in led.get("cold_without_a_send", []) if e.get("date") != "2026-10-17"]

CROSSED = [
    "academics-social-media-and-ai-impact-on-womens-identity-and-selfesteem",
    "ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories",
    "ai-data-annotators-and-labellers-experience-with-ai-training-data",
    "ai-data-labelers-in-germany-positive-and-negative-experiences",
    "ai-infrastructure-experts-china-vs-us-datacenter-capacity",
    "coweta-county-artists-and-creatives-data-centers-and-ai-infrastructure",
    "emergency-managers-ai-tools-for-funding-and-staffing-shortfalls",
    "plaintiffs-attorneys-and-legal-scholars-ai-deepfake-liability",
    "swiss-ai-companion-users-emotional-bonds-and-daily-life",
    "uk-companies-implementing-ai-how-automation-transforms-workdays",
]

AT_TEN = [
    "anz-marketers-ai-and-martech-innovation-spotlight",
    "apac-reporters-and-editors-ai-accountability-coverage",
    "aps-hr-leaders-ai-skills-training-and-workforce-planning",
    "early-to-midcareer-information-architects-products-featuring-ai",
    "martech-buyers-ai-impact-on-build-vs-buy-decisions",
    "real-estate-agents-replacing-pdf-property-brochure",
    "scrum-masters-daytoday-and-career-pivots-and-ai-impact",
    "solicitors-and-barristers-ai-to-expand-pro-bono-capacity",
    "uk-ai-data-trainers-daytoday-work",
]

led.setdefault("cold_without_a_send", []).insert(0, {
    "date": "2026-10-17",
    "url": ", ".join(f"https://www.sourcee.app/journo-request/{s}" for s in CROSSED),
    "action": "crossed the 10-day line today at 11 days, all ten unpitched, none ever drafted",
    "note": (
        "All ten were named in advance by the 2026-10-16 digest as sitting at exactly 10 days, so this "
        "is a scheduled crossing and not new information. All ten are relevance 'low', none has a draft, "
        "and none has ever been inside the sendable count, so the crossing cost nothing. Nine more rows "
        "sit at exactly 10 days and cross tomorrow: " + ", ".join(AT_TEN) + " - all 'low' and route-less, "
        "named so the next quiet count change is not mistaken for a quiet week."
    ),
})

led.setdefault("log", []).append({
    "date": "2026-10-17",
    "event": ("monitor run - 74-slug window, 7 AI-token, 2 AI+spend (both the bare 'saas' token, neither a "
              "spend question); 7 rows added; 10 rows crossed cold; 1 sendable; no sends"),
    "detail": (
        "147 tracked (140 carried, all 140 re-verified HTTP 200/live with every deadline field rebuilt from "
        "the page's own badge and datePublished; 7 added - every AI-token slug in the window, none a "
        "candidate), 53 live unpitched, 87 cold unpitched, 1 sendable (the Fast Company Work Life / Tobi "
        "Amure row, now 7 days old, route hello@tobiamure.com re-probed today with the address counted 6 "
        "times on tobiamure.com/ and 5 times on /contact/). New window: 74 slugs, 7 AI-token, 2 AI+spend, 4 "
        "spend-only; all 74 window bodies fetched and read in full, which is the only check that can back a "
        "zero. The 7 are a promo/discussion cluster (an AI SaaS vendor wanting a case study for his own "
        "pitch, a real-estate operator wanting peer interviews, a founder wanting a YouTube feature, plus "
        "beat-specific asks: chemistry students, Berlin AI-infra engineers, Mumbai data-centre residents, "
        "family-office cybersecurity experts) - not one body asks what a tool costs and not one publishes a "
        "route. Mailbox: INBOX newest is a Keep/Cut Weekly confirmation (2026-10-17 05:20 UTC) and All Mail "
        "page 1 still carries Jan Suski's 2026-10-11 06:57 UTC acknowledgment as the newest inbound from any "
        "pitch recipient; nothing has come from foxandspindle.com, epgacceleration.com, artichokehq.com or "
        "raconteur.net at any point. Sent Mail shows nothing sent since 2026-10-10 21:20 UTC. 0 pitches sent "
        "this run - sends remain George's lane. CODE CHANGES: (1) scripts/probe_routes.py now records "
        "`emails_on_page` (each address and how many times it appears) for every route it probes, so the "
        "'verbatim N times' evidence for a reply route is measured rather than hand-typed; (2) the digest's "
        "route section had indexed its rows BEFORE the tool-count repair pass copied repaired rows into new "
        "dicts, so the sendable row's route text was written onto a dict no longer in the digest - caught by "
        "reading the written digest, and the index is now built last. Figures re-derived against "
        "data/pricing_snapshots.json updated 2026-10-17: 42 of 79 tools publish a monthly price, 33 at or "
        "under $25/month, median $17.50; pairs 1.11x-2.53x, median 1.25x over 19 tiers (built 2026-10-16)."
    ),
})

LED.write_text(json.dumps(led, indent=1))
print("ledger updated:", LED)
print("reply_status_checked =", led["reply_status_checked"])
print("cold_without_a_send entries:", len(led["cold_without_a_send"]), "| log entries:", len(led["log"]))
