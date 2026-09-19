#!/usr/bin/env python3
"""Assemble digest-2026-09-19.json (metadata + opportunities from _digest_0919.py)."""
import json
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
ops = json.load(open("/tmp/ops_0919.json"))
ver = json.load(open(D / "verified-requests.json"))

digest = {
    "date": "2026-09-19",
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": "2026-09-19T09:00:00-07:00",
    "search_scope": "AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support value, tool consolidation, procurement budget",
    "age_policy": ("Ages are read off each request page (JSON-LD datePublished plus the rendered "
                   "'Posted ... ago' badge), never off the digest text. All 29 tracked URLs were "
                   "re-fetched this run: HTTP 200 and the request body still served, none returns an "
                   "expiry notice."),
    "platforms_checked": [
        {"platform": "Sourcee (sourcee.app)", "status": "accessible",
         "notes": ("Sitemap pulled fresh from the index child /sitemap-journo-requests.xml "
                   "(9,927,746 bytes, 41,286 loc/lastmod pairs, 40,435 unique slugs, newest lastmod "
                   "2026-09-19T02:27:03Z). 578 slugs carry a lastmod inside the 2026-09-11+ window; "
                   "63 carry any AI token; 1 carries a strict pricing/cost token alongside an AI "
                   "token and 3 carry a third-tier spend token alongside one. 32 candidate bodies "
                   "were fetched and read this run. No new core-beat request.")},
        {"platform": "Sourcee AI topic feed — /topics/ai/journo-requests", "status": "recency_window_not_persistence",
         "notes": ("Re-measured for the third run. The page carries 30 slugs today; all 30 have a "
                   "lastmod inside a single 15.4-hour window (2026-09-18T11:01:23Z to "
                   "2026-09-19T02:27:03Z) and it shares 0 of its slugs with the 2026-09-17 capture, "
                   "which itself shared 0 with 2026-09-16. It is a rolling recency window over the "
                   "newest ~30-42 indexed requests, not a feed a request persists on, so absence from "
                   "it is NOT a cold signal and build_pitch_queue.py does not use it as one. This run "
                   "also established the reason it can never be one: 53 slugs across the entire "
                   "40,435-slug sitemap are newer than the window's oldest member, i.e. the window is "
                   "the newest ~30 of everything, with no topic curation at all.")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed. / returns HTTP 429 (33,954 bytes) titled 'Vercel Security Checkpoint'. "
                   "Eighth consecutive identical result. Queries are distributed only by a 3x-daily "
                   "email digest requiring a subscribed inbox.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": ("Re-probed. / HTTP 429 (33,944 bytes) and /queries HTTP 429 (33,945 bytes), both "
                   "'Vercel Security Checkpoint'. No public query feed.")},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,650 bytes, 'Page Not Found - Source "
                   "of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,265 bytes) — the path is "
                   "wrong, not gated. The feed needs an authenticated app session.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. Apex HTTP 200 (11,345 bytes, 'MentionMatch - Connect B2B Writers with "
                   "Expert Sources') with no feed. Eighth consecutive run confirming a pre-launch shell.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 73-byte {\"error\":\"invalid_token\"}. Free read-only feed "
                   "covering Connectively, HARO, X, LinkedIn, MentionMatch and Substack. Needs an "
                   "interactive OAuth handshake that cannot be completed from a scheduled run. "
                   "`hermes mcp list` in this profile still reports no MCP servers configured.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on eight consecutive runs; "
                   "the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (148,264 bytes, 'ResponseSource - Connecting the media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free "
                   "source-facing feed.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        ("TWO RESOLVED EMAIL ROUTES, the first in this monitor's history beyond a hand-found contact "
         "form. Sourcee redacts the requester's address inside the request body — verified this run that "
         "the redaction is real, not display-only: no address survives anywhere in the page payload for "
         "five sampled requests. But the *publication's* own site publishes the reporter, and two are "
         "reachable: (a) Raconteur's byline pages carry the writer's address as an obfuscated "
         "data-part1/2/3 triple that the site's own scripts-last.min.js assembles at runtime "
         "(part1+'@'+part2+'.'+part3); reconstructed and cross-checked on two authors, giving "
         "simon.chandler@raconteur.net for the shadow-AI request's author, on Google Workspace MX. "
         "(b) Speciality Food magazine's /contact page lists named editorial addresses, including "
         "holly.shackleton@artichokehq.com for that request's author, on Microsoft 365 MX. Raconteur's "
         "own contact page explicitly asks PRs to approach the relevant writer directly."),
        ("NEW HIGH-RELEVANCE REQUEST, the first in six runs: 'Full-Time Employees - Shadow AI Use & "
         "Paying Out-of-Pocket' (Raconteur, Simon Chandler, 2 days old). Employees buying AI without "
         "employer approval and paying personally is unbudgeted, unenumerated software spend — our "
         "actual beat. It has been on Sourcee since 2026-09-17 and was missed because the previous run's "
         "sitemap scan read /sitemap.xml, which now returns only an index of 8 children; the scan "
         "silently produced 0 pairs. This run read /sitemap-journo-requests.xml directly."),
        ("RENEWAL SIGNAL TESTED AND FOUND ABSENT. The queue's cold label said 'never refreshed', which "
         "asserts an edit event. Sourcee's sitemap lastmod is byte-identical to the page's datePublished "
         "on all 300 most recently indexed slugs (300/300) and all 30 live-feed slugs (30/30), so lastmod "
         "carries no renewal information. build_pitch_queue.py no longer makes the claim."),
        ("RELEVANCE-RANKING DEFECT FIXED in build_pitch_queue.py._norm_rel. The digests use free-text "
         "labels ('high on topic, low on currency', 'medium (adjacent, not core AI-spend)'); only "
         "parentheticals were stripped, so 'high on topic, low on currency' reached RELEVANCE_RANK as an "
         "unknown key and took the default 9 — ranking it below every 'low' request. Both occurrences "
         "normalise to 'medium' now."),
        ("THE 2026-09-18 DIGEST WAS NEVER WRITTEN. That run produced its scratch artifacts "
         "(_scan_0918.json, _bodies_0918.json, _bodies_0918b.json — all committed) but no "
         "digest-2026-09-18.json, so build_pitch_queue.py's newest-digest membership test had been "
         "pointing at 2026-09-17 and reading 'not carried by the 2026-09-17 digest' on rows the "
         "2026-09-18 run had in fact seen. Confirmed by git: no digest-2026-09-18.json exists in the "
         "working tree or anywhere in history. This run's digest carries all 29 tracked requests so the "
         "membership test has a complete newest digest to read."),
        ("SUPPLY: 578 slugs newly indexed in the 2026-09-11+ window, 63 carrying any AI token, of which "
         "9 AI-token slugs had never been body-read by any prior run and all 9 were read this run "
         "(travel/cruise, narrative-medicine podcast, UK 80+ book interview, Cornell academic-integrity, "
         "Morocco sports hosting, parents teaching kids AI, two Medicare-agent requests). None is "
         "core-beat. 32 bodies read in total this run, 1 new core-beat-adjacent request (Raconteur)."),
        ("TWO REQUESTS CROSSED INTO COLD UNPITCHED TODAY. FinOps/agentic AI cost overruns (12 days) was "
         "the queue's #1 on 2026-09-17 at 10 days and its draft was written and never sent; it is now "
         "past the 10-day line with its route still a LinkedIn DM. UK managers/Gen Z AI overuse (12 "
         "days) also crossed."),
    ],
    "expired_this_run": [
        ("Tech Policy Experts - California AI audit bills (Industry Dive, Paige Gross): the request's own "
         "stated turnaround was 'speak with a source today' and it was posted 2026-09-10; now 9 days. "
         "Page live, no expiry notice. Do-not-pitch."),
        ("UK Managers - Gen Z AI overuse (MaryLou Costa): internal deadline ('by this Wednesday September 9') "
         "passed 10 days ago; now also past the 10-day line. Cold."),
        ("No request page fetched this run returned a removal notice: all 29 tracked URLs still serve their "
         "request body at HTTP 200."),
    ],
    "summary": ("29 tracked requests, 12 live and unpitched, 17 at or past the cold line. One new "
                "high-relevance request (Raconteur shadow AI, 2 days) — the first core-beat find in six "
                "runs — and, for the first time, two resolved publication-side email routes rather than "
                "DM-only. Two requests that had drafts written for them crossed into cold unpitched. Two "
                "monitor defects fixed: a missing 2026-09-18 digest that corrupted the newest-digest "
                "membership test, and a relevance normaliser that ranked the two highest-scoring requests "
                "below every low one."),
    "recommended_actions": [
        ("Send Draft 1 to simon.chandler@raconteur.net (Raconteur, shadow AI spend, 2 days, high). The "
         "strongest request this monitor has held: on-beat, fresh, and with a resolved email route to the "
         "named author. Keep the no-personal-account disclosure."),
        ("Send Draft 2 to hliwrites.99 on Signal (Anthropic subscription value, 7 days, medium-high). "
         "Handle re-read off the live page this run; it is the direct channel and the request is ageing."),
        ("Send Draft 3 to holly.shackleton@artichokehq.com (Speciality Food, 1 day, low-medium) only if a "
         "budget benchmark is welcome from a non-retailer; the draft says so in its first line."),
        ("Decide on FinOps (12 days, cold): send the existing 2026-09-17 draft 1 as a LinkedIn DM or drop "
         "it. It is now the longest-standing high-relevance request we have never answered."),
        ("Resolve the Medialyst MCP OAuth handshake: the single step that adds six platforms' feeds "
         "(Connectively, HARO, X, LinkedIn, MentionMatch, Substack) to this monitor. Endpoint confirmed "
         "live (401 invalid_token); no MCP servers are configured in this profile."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 1,
        "consecutive_runs_without_new_core_beat": 0,
        "tracked_urls": 29,
        "live_unpitched": 12,
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 2,
    },
}

out = D / "digest-2026-09-19.json"
out.write_text(json.dumps(digest, indent=2) + "\n")
print("wrote", out.name, len(json.dumps(digest)), "bytes")
print("opportunities:", len(ops))
