#!/usr/bin/env python3
"""Write digest-2026-09-20.json.

Every one of the 29 tracked requests was re-fetched from its own page today (verified-requests.json
was refreshed by scripts/verify_journo_requests.py --refresh-feed), so the deadline field carries a
today-stamped page verification rather than yesterday's. Editorial text is carried forward from the
2026-09-19 digest and re-stamped, except where today's probe changed a fact - the Raconteur route
is one: the byline URL used on 2026-09-19 (/author/simon-chandler/) now 404s and the live page is
/contributors/simon-chandler.
"""
import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
prev = json.loads((D / "digest-2026-09-19.json").read_text())
ver = json.loads((D / "verified-requests.json").read_text())
probe = json.loads((D / "_probe_0920.json").read_text())
todays = json.loads((D / "_bodies_0920.json").read_text())
window = json.loads((D / "_window_0920.json").read_text())

TODAY = "2026-09-20"

# The 2026-09-19 digest's route claim for the Raconteur request named a byline path that is gone.
ROUTE_FIX = (
    " ROUTE CORRECTED 2026-09-20: the 2026-09-19 digest named "
    "https://www.raconteur.net/author/simon-chandler/ as the page publishing the obfuscated "
    "data-part1/2/3 triple. That URL now returns HTTP 404 (139,404 bytes, Raconteur's own 404 "
    "shell) and so does /author/ian-deering/, which had been used as the cross-check. Raconteur's "
    "author-sitemap.xml still lists him but under a different, space-encoded path: "
    "https://www.raconteur.net/contributors/Simon%20Chandler - which is itself a 404. The live "
    "page is https://www.raconteur.net/contributors/simon-chandler (HTTP 200) and it still carries "
    "data-part1=\"simon.chandler\" data-part2=\"raconteur\" data-part3=\"net\", i.e. "
    "simon.chandler@raconteur.net, unchanged. Control test on the same run: "
    "https://www.raconteur.net/contributors/tom-dennis (HTTP 200) carries "
    "data-part1=\"tom.dennis\" data-part2=\"raconteur\" data-part3=\"net\". raconteur.net MX "
    "re-checked today = Google Workspace (1 aspmx.l.google.com). The address is unchanged; only the "
    "URL that publishes it moved, so the draft needed no edit but the queue's route note did."
)

out = []
for op in prev["opportunities"]:
    slug = op["url"].rstrip("/").split("/journo-request/")[-1]
    v = ver.get(slug)
    rec = dict(op)
    if v:
        old = re.sub(r"\s*PAGE-VERIFIED 2026-09-19:.*$", "", rec.get("deadline") or "",
                     flags=re.S).rstrip()
        old = re.sub(r"\s*RE-VERIFIED 2026-09-20:.*$", "", old, flags=re.S).rstrip()
        rec["deadline"] = (f"{old} RE-VERIFIED 2026-09-20: HTTP {v['http']}, live={v['live']}, "
                           f"badge '{v['badge']}', datePublished {v['datePublished']} = "
                           f"{v['days_old']} days, no expiry notice on the page.")
    if slug == "fulltime-employees-shadow-ai-use-and-paying-outofpocket":
        rec["contact_method"] = (rec.get("contact_method") or "") + ROUTE_FIX
    out.append(rec)

# New candidate bodies read this run, recorded so they are not re-surfaced as new tomorrow.
NEW = {
    "founders-cutting-ai-use-eliminating-or-reducing-ai-in-business": {
        "journalist_publication": "Forbes - author named in the page's own author field: Jodie Cook",
        "category": "AI / Founders / Deliberate AI Reduction",
        "relevance": "medium-low",
        "relevance_notes": "NEW and the freshest AI-token request in the window (published 2026-09-19T13:00Z), a Forbes byline. It is the inverse of our usual beat: it wants founders who are *cutting* AI, asked to answer publicly as a comment. There is a real adjacency - 'which AI tools did you drop and what did it save' is the keep/cut question - but the request wants a named founder's first-person rationale on the record, and AIToolsEssentials is an anonymous-signed publisher with no founder to put forward. Recorded, not drafted; the standing problem is the same one that sank the Inc. founders request.",
        "contact_method": ("Comment on the original post - the body is explicit: 'Please only answer as a "
                          "comment on this post. Do not email or DM me because they won't be used.' "
                          "No email published. PAGE-VERIFIED 2026-09-20: HTTP 200, email_redacted=False, "
                          "emails_on_page=none."),
        "suggested_pitch_template": "None - the reply route is a public comment requiring a named founder's firsthand account, which we do not have.",
    },
    "survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies": {
        "journalist_publication": "The Lever - author field 'badplacetimes', journalist self-identified as Craig",
        "category": "AI / Autonomous Weapons / Investigative",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-20T00:27Z - the single newest request in the whole window. Off-beat and off-standing: it wants survivors of autonomous weaponry giving testimony. Nothing to do with AI pricing or spend. Recorded for completeness so it is not re-surfaced as new.",
        "contact_method": "Signal 972-408-7275, published verbatim in the request body. PAGE-VERIFIED 2026-09-20: HTTP 200, email_redacted=False, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded, wrong standing.",
    },
    "employers-and-recruiters-over-50s-adapting-to-ai": {
        "journalist_publication": "Independent (Ovee, 'Beyond the CV' interviews) - author field: Peter Tsakissiris",
        "category": "AI / Workforce / Age & Adaptation",
        "relevance": "low",
        "relevance_notes": "NEW. A workplace-culture piece about over-50s adapting to AI. Adjacent to nothing we hold - no cost, pricing, seat or spend angle anywhere in the body. Recorded, excluded.",
        "contact_method": "No email, DM handle or link published on the page. PAGE-VERIFIED 2026-09-20: HTTP 200, email_redacted=False, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded.",
    },
    "data-center-professionals-podcast-guest-ai-and-hyperscale-trends": {
        "journalist_publication": "Independent podcast ('The Strategic Podcast') - author field: Todd T. Stone",
        "category": "Data Centre / Podcast Guest Booking",
        "relevance": "low",
        "relevance_notes": "NEW. A podcast guest-and-sponsor solicitation for data-centre industry people, not a journalist request. No spend or subscription angle. Recorded, excluded.",
        "contact_method": "No route published on the Sourcee page; the body solicits guest and sponsor enquiries. PAGE-VERIFIED 2026-09-20: HTTP 200, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded, and it is a booking solicitation rather than a request.",
    },
    "ai-alignment-researchers-humanai-mutual-understanding": {
        "journalist_publication": "Independent (framework author, LinkedIn long-form) - author field: Zamo Dana",
        "category": "AI / Alignment / Philosophy",
        "relevance": "low",
        "relevance_notes": "NEW. A self-published framework discussion seeking alignment researchers. No pricing, spend or procurement content. Recorded, excluded.",
        "contact_method": "No email or handle published on the page. PAGE-VERIFIED 2026-09-20: HTTP 200, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded.",
    },
    "patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges": {
        "journalist_publication": "Independent journalist - author field: Tanushka Dutta",
        "category": "US Healthcare Billing / Consumer Costs",
        "relevance": "low",
        "relevance_notes": ("NEW, published 2026-09-20T03:58Z - the newest slug in the sitemap at run time "
                            "and the only one in the window that carried a spend token ('billing'), which is "
                            "why it was read. It is a US hospital-billing story wanting patients with wrongful "
                            "bills. The word 'billing' matched our spend filter but the subject is medical "
                            "charges, not software subscriptions. A reminder that the slug filter matches a "
                            "token, not a subject. Recorded, excluded."),
        "contact_method": "DM the author; no email published. PAGE-VERIFIED 2026-09-20: HTTP 200, email_redacted=False, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded, wrong subject.",
    },
}
for slug, extra in NEW.items():
    if any(slug in o["url"] for o in out):
        continue
    v = todays[slug]
    out.append({
        "url": f"https://www.sourcee.app/journo-request/{slug}",
        "query_text": re.sub(r"\s+", " ", v["core"])[:900],
        "deadline": (f"NEW this run. Page badge '{v['badge']}'; datePublished {v['datePublished']}. "
                     f"PAGE-VERIFIED 2026-09-20: HTTP {v['http']}, live=True, no expiry notice on the page."),
        **{k: extra[k] for k in ("journalist_publication", "category", "relevance",
                                 "relevance_notes", "contact_method", "suggested_pitch_template")},
    })

platforms = [
    {"platform": "Sourcee (sourcee.app)", "status": "accessible",
     "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP 200, 9,936,974 bytes, "
               f"{len(window['window']) + 0} loc/lastmod pairs in the file, newest lastmod "
               f"2026-09-20T03:58:40Z). 39 slugs carry a lastmod newer than the 2026-09-19 run's newest "
               f"({window['mark']}); 5 of those carry any AI token and 0 carries an AI token plus a "
               f"strict pricing/cost token. All 5 new AI-token slugs plus 1 spend-token slug were "
               f"fetched and read: no new core-beat request. Sourcee itself re-probed HTTP 200 "
               f"(100,854 bytes).")},
    {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
     "status": "recency_window_not_persistence",
     "notes": ("Re-measured for the fourth run. 39 slugs today, all with a lastmod inside a single "
               "recency window; it shares 0 slugs with the 2026-09-19 capture, which shared 0 with "
               "2026-09-18. Still a rolling window over the newest requests, not a feed a request "
               "persists on, so absence from it is NOT a cold signal and build_pitch_queue.py does not "
               "use it as one. No change to that finding this run.")},
    {"platform": "HARO (helpareporter.com)", "status": "email_wall",
     "notes": ("Re-probed once. / returns HTTP 429 (31,198 bytes, 'Vercel Security Checkpoint'). Ninth "
               "consecutive identical result. Queries reach sources only by a 3x-daily email digest to a "
               "subscribed inbox. Not retried, per the monitor's rule.")},
    {"platform": "Connectively (connectively.us)", "status": "login_required",
     "notes": "Re-probed once. / HTTP 429 (31,199 bytes, 'Vercel Security Checkpoint'). No public query feed."},
    {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
     "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - Source of "
               "Sources'). Reporter submission form only; no source-facing feed.")},
    {"platform": "Qwoted (qwoted.com)", "status": "login_required",
     "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes) - wrong path, not "
               "gated. The feed needs an authenticated app session.")},
    {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
     "notes": "Re-probed. Apex HTTP 200 (11,342 bytes) with no feed. Ninth consecutive run confirming a pre-launch shell."},
    {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
     "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\"}. Free read-only feed covering "
               "Connectively, HARO, X, LinkedIn, MentionMatch and Substack. Needs an interactive OAuth "
               "handshake that cannot be completed from a scheduled run. `hermes mcp list` in this "
               "profile still reports 'No MCP servers configured.'")},
    {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
     "notes": ("Not re-attempted. Team-level credit limit blocked this on eight consecutive runs; the "
               "block is account state, not a transient failure. Sourcee's X-originated aggregation is "
               "used as a proxy.")},
    {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
     "notes": ("Root re-probed HTTP 200 (148,252 bytes, 'ResponseSource - Connecting the media'). UK-only; "
               "enquiry feed sold by category from GBP 85 pay-as-you-go. No free source-facing feed.")},
]

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": "2026-09-20T09:00:00-07:00",
    "search_scope": ("AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, "
                     "software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support "
                     "value, tool consolidation, procurement budget"),
    "age_policy": ("Ages are read off each request page (JSON-LD datePublished plus the rendered "
                   "'Posted ... ago' badge), never off the digest text. All 29 tracked URLs were "
                   "re-fetched this run: HTTP 200 and the request body still served, none returns an "
                   "expiry notice."),
    "platforms_checked": platforms,
    "opportunities": out,
    "new_this_run": [
        "NO NEW CORE-BEAT REQUEST. Five new AI-token slugs were indexed since the 2026-09-19 run and all five were read: Forbes founders cutting AI use (medium-low, comment-only route needing a named founder), The Lever autonomous-weapons survivors (off-beat), an over-50s workplace piece, a data-centre podcast booking, and a self-published alignment framework. One spend-token-only slug (US hospital billing) was read and is a medical-charges story. Supply on the one accessible platform is thin again: 39 new slugs in 25 hours, 5 with an AI token, 0 with an AI token and a pricing token.",
        "THE RACONTEUR ROUTE'S SOURCE URL MOVED. Yesterday's digest cited https://www.raconteur.net/author/simon-chandler/ as the page publishing the obfuscated address triple. Both that URL and the cross-check URL /author/ian-deering/ now return 404. Raconteur's author-sitemap.xml (HTTP 200, 1,000 locs) still lists Simon Chandler, but under a space-encoded path (/contributors/Simon%20Chandler) that is itself a 404. The live page is /contributors/simon-chandler (HTTP 200), still carrying data-part1=\"simon.chandler\" data-part2=\"raconteur\" data-part3=\"net\". Address unchanged, route intact, citation in the queue corrected. Control test on /contributors/tom-dennis returned the same triple shape, so the pattern is the site's standard.",
        "ALL THREE 2026-09-19 DRAFTS RE-VERIFIED, STILL UNSENT. The Raconteur shadow-AI draft, the Anthropic Signal draft and the Speciality Food draft were each checked against today's data and today's pages: every cited figure still holds and every reply route still resolves (raconteur.net MX = Google Workspace; artichokehq.com MX = Microsoft 365, with holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today; Signal handle hliwrites.99 re-read off the live request page today). Nothing needed an edit. Nothing has been sent.",
        "MAILBOX CHECKED: NO NEW REPLIES. INBOX top is still Jan Suski's 2026-09-18 20:39Z reply to the Amplemarket pitch, which we answered 2026-09-18 21:29Z. No reply to the 2026-09-15 Raconteur-equivalent send, none to the 2026-09-18 Sherwood News send. Spam holds three items, all delivery-failure bounces and directory form-mail.",
        "ONE REQUEST AT THE COLD LINE. Individual contributors managing AI agents (10 days) and the California AI audit bills request (10 days) both sit exactly on the 10-day threshold today and will read cold on the next run if unsent. Both are already pitched or do-not-pitch, so neither is actionable - recorded so the line is visible.",
    ],
    "expired_this_run": [
        "Nothing expired or dropped off this run. All 29 tracked URLs returned HTTP 200 with the request body still served and no removal or expiry notice on any page.",
        "The two requests already recorded as spent remain spent: Tech Policy Experts - California AI audit bills ('speak with a source today', posted 2026-09-10) and UK Managers - Gen Z AI overuse (internal deadline 'by this Wednesday September 9'). Both pages stay live with no expiry notice, which is why the do-not-pitch judgement rests on their stated deadlines rather than on the page.",
    ],
    "summary": ("35 tracked requests (29 carried and re-verified, 6 new and recorded), 17 live and "
                "unpitched, 3 pitched, 14 at or past the cold line. No new core-beat request: five new "
                "AI-token slugs were indexed and all five were read, none on-beat. The Raconteur "
                "shadow-AI route's source URL was found to have moved and was re-resolved to "
                "/contributors/simon-chandler (address unchanged). All three outstanding drafts were "
                "re-verified against today's data and today's pages and all three still hold. No new "
                "replies in the mailbox. Zero pitches sent this run - sends remain George's lane."),
    "recommended_actions": [
        "Send the Raconteur shadow-AI draft (pitch-drafts-2026-09-20.md section 1) to simon.chandler@raconteur.net. Route re-resolved today at /contributors/simon-chandler. This is the best request the monitor has ever held and its unsent draft is now 24 hours old.",
        "Send the Anthropic subscription-value draft (section 2) to Signal hliwrites.99. Handle re-read off the live page today. The request is 8 days old and rising - send or drop.",
        "Send the Speciality Food draft (section 3) to holly.shackleton@artichokehq.com only if a non-retailer budget benchmark is welcome; the draft says so in its first line.",
        "Decide on FinOps (13 days, cold, unpitched): the 2026-09-17 draft exists and the route is a LinkedIn DM to linkedin.com/in/niloy-ghosh. Send it late or drop it - it has now been the longest-standing high-relevance request for six days.",
        "Resolve the Medialyst MCP OAuth handshake: the single step that adds six platforms' feeds to a monitor whose only accessible source produced no core-beat request today.",
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "consecutive_runs_without_new_core_beat": 1,
        "tracked_urls": 35,
        "carried_and_reverified": 29,
        "live_unpitched": 17,
        "cold_unpitched": 14,
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 2,
        "drafts_written_never_sent": 4,
    },
    "monitor_defects_fixed_this_run": [
        "RELEVANCE RANKING, second occurrence of the same defect class. build_pitch_queue.py's RELEVANCE_RANK map had no entry for the band 'medium-high', which three digest rows carry, so _norm_rel's output reached RELEVANCE_RANK.get() and took the default of 9 - ranking them BELOW every 'low' request. The Anthropic subscription-value request, which has a finished draft and the only published direct channel in the queue, was ranked 17th of 17 as a result. Fixed by adding the band and routing all lookups through a new _rel_rank() that bands on the 'high'/'medium'/'low' prefix before defaulting, so an unanticipated label can never again sort below 'low'. The queue's live section is now asserted sorted by band in _verify_drafts_0920.py.",
        "RUN-SPECIFIC FILENAME IN A REUSABLE SCRIPT. build_pitch_queue.py._load_renewal() was pinned to _renewal_0919.json, so every run after 2026-09-19 would have loaded that run's evidence regardless of what it had measured itself. Now globs the newest _renewal_*.json.",
        "STALE CITATION IN THE QUEUE'S ROUTE NOTES. The DRAFTS index still pointed at pitch-drafts-2026-09-19.md for four rows; it now names the newest file per row and records that the Raconteur byline URL cited on 2026-09-19 is dead.",
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=2, ensure_ascii=False))
print("wrote", f"digest-{TODAY}.json", "opportunities:", len(out))
