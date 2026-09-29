#!/usr/bin/env python3
"""Prepend today's cold_without_a_send entries (the ledger lists newest first)."""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
led = json.loads((D / "pitch-ledger.json").read_text())
TODAY = "2026-09-29"

led["cold_without_a_send"] = [
    {
        "date": TODAY,
        "url": "https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business",
        "action": "LAST LIVE DAY - crosses TOMORROW at 11 days, and the crossing costs nothing",
        "note": ("10 days old today and it has been counted as sendable for two consecutive runs, "
                 "wrongly both times. Its body is explicit: \"Please only answer as a comment on this "
                 "post. Do not email or DM me because they won't be used.\" The queue's own angle "
                 "field already said the reply route requires a named founder's firsthand account of "
                 "cutting AI, which we do not have. It looked sendable only because this run's refresh "
                 "script dropped Sourcee's two own social links from its chrome filter, so a page's own "
                 "chrome landed in published_links and _sendable() read that as a usable route. With "
                 "the filter restored the row is correctly not sendable, so tomorrow's crossing "
                 "removes nothing. Logged on the day it still looks live, so the advance warning is "
                 "not misread as a lost draft."),
    },
    {
        "date": TODAY,
        "url": "https://www.sourcee.app/journo-request/companies-that-stopped-emailing-pdfs-new-tools-and-transition",
        "action": "crossed the 10-day line today at 11 days, unpitched, no draft ever existed",
        "note": ("Low relevance, never had a draft and never had a resolved route, so nothing sendable "
                 "was lost. Named because build_pitch_queue.py's two-day advance warning covers only "
                 "sendable rows, so an ordinary crossing otherwise shows up as nothing but the live "
                 "count falling 18 to 17."),
    },
    {
        "date": TODAY,
        "url": ("https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket, "
                "https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech"),
        "action": "both were sent-ready drafts that had already crossed on 2026-09-28 - re-derived and republished today, still unsent",
        "note": ("Neither is void. Both pages returned HTTP 200 again today with the request body still "
                 "served, and both routes were re-resolved against the live pages this run: "
                 "simon.chandler@raconteur.net off /contributors/simon-chandler (HTTP 200, 154,759 "
                 "bytes, data-part1/2/3 unchanged, control author /contributors/tom-dennis carries "
                 "tom.dennis/raconteur/net; the older /author/simon-chandler/ still 404s), and "
                 "holly.shackleton@artichokehq.com off specialityfoodmagazine.com/contact (HTTP 200, "
                 "59,500 bytes, byte-count unchanged, alongside five other named masthead addresses). "
                 "The shadow-AI draft is now unsent through twelve consecutive runs, and the "
                 "Speciality Food draft has been carried four times. What was lost is the ideal "
                 "window, not the pitch."),
    },
] + led["cold_without_a_send"]

(D / "pitch-ledger.json").write_text(json.dumps(led, indent=2))
print("cold_without_a_send entries now:", len(led["cold_without_a_send"]))
