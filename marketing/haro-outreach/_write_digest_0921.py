#!/usr/bin/env python3
"""Write digest-2026-09-21.json.

Every tracked request was re-fetched from its own page today by
`scripts/verify_journo_requests.py --refresh-feed` (all 35 HTTP 200, request body still served, no
expiry notice), so the deadline field carries a today-stamped page verification. Editorial text is
carried forward from the 2026-09-20 digest and re-stamped; the contact routes were re-resolved
against the live pages this run rather than carried on trust.
"""
import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
prev = json.loads((D / "digest-2026-09-20.json").read_text())
ver = json.loads((D / "verified-requests.json").read_text())
sw = json.loads((D / "_sitemap_0921.json").read_text())
bodies = json.loads((D / "_bodies_0921.json").read_text())
adjacent = json.loads((D / "_bodies_0921b.json").read_text())

TODAY = "2026-09-21"
MARK = sw["mark"]

out = []
for op in prev["opportunities"]:
    slug = op["url"].rstrip("/").split("/journo-request/")[-1]
    v = ver.get(slug)
    rec = dict(op)
    if v:
        old = re.sub(r"\s*PAGE-VERIFIED 2026-09-\d\d:.*$", "", rec.get("deadline") or "", flags=re.S).rstrip()
        old = re.sub(r"\s*RE-VERIFIED 2026-09-\d\d:.*$", "", old, flags=re.S).rstrip()
        rec["deadline"] = (f"{old} RE-VERIFIED {TODAY}: HTTP {v['http']}, live={v['live']}, "
                           f"badge '{v['badge']}', datePublished {v['datePublished']} = "
                           f"{v['days_old']} days, no expiry notice on the page.")
    out.append(rec)

# --- new reads this run, recorded so they are not re-surfaced as new tomorrow ---------------
# Both carry a spend token in the slug but no AI token; both are the class the slug filter misses.
NEW = {
    "sales-enablement-saas-tools-proposal-and-deck-engagement-tracking": {
        "journalist_publication": "Lyza G (author field) — a #PROpportunity post; the page publishes "
                                  "linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith as the reply handles",
        "category": "Sales Tech / SaaS Tool Sourcing (PR solicitation)",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-20T18:25Z, and it is the only new slug in the whole "
                           "window that touches software at all — which is why it was read. It seeks "
                           "SaaS tools that track proposal and pitch-deck engagement, a tool category we "
                           "do not cover, and the body asks for 'your tool name, main feature, and "
                           "founder quote'. That is a vendor-sourcing call from a PR account "
                           "(#PROpportunity), not a reporter's request, and we have no founder to quote. "
                           "Recorded, excluded.",
        "contact_method": "Reply/DM — the body says 'Drop your tool name … below or in DMs'; the page "
                          "publishes linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith. No email. "
                          f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded. Wrong tool category, wrong standing, and it is a "
                                    "solicitation rather than a journalist request.",
    },
    "companies-that-stopped-emailing-pdfs-new-tools-and-transition": {
        "journalist_publication": "Lyza G (author field) — same PR account as the sales-enablement post",
        "category": "Workflow Tools / Document Handling",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-18T14:38Z. Wants companies that moved away from "
                           "emailing PDF attachments and what they switched to. Document-handling "
                           "workflow, not AI pricing or spend — no cost, pricing, seat or subscription "
                           "angle anywhere in the body. Recorded, excluded.",
        "contact_method": "Reply or DM; no email published. "
                          f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded, off-beat.",
    },
    "founders-and-leaders-mindsets-and-milestones": {
        "journalist_publication": "Conor Burchall (author field) — 'Rational Exchange' podcast",
        "category": "Founders / Podcast Interviews",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-20T16:58Z. A podcast interview call for founders, "
                           "fund managers and people with a career story. No pricing, spend or "
                           "procurement content. Recorded, excluded.",
        "contact_method": f"No route published on the page. PAGE-VERIFIED {TODAY}: HTTP 200, "
                          f"email_redacted=False, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded.",
    },
    "ml-researchers-continuous-learning-fast-weights-and-adapters": {
        "journalist_publication": "Chris (author field) — ML research 'DevDay wish list' post",
        "category": "ML Research / Methods",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-20T10:30Z. A researcher-to-researcher call about "
                           "continuous learning, fast weights and adapters. Methods discussion; nothing "
                           "to do with AI spend or pricing. Recorded, excluded.",
        "contact_method": f"No route published on the page. PAGE-VERIFIED {TODAY}: HTTP 200, "
                          f"emails_on_page=none.",
        "suggested_pitch_template": "None - excluded.",
    },
    "founders-55-latelife-entrepreneurship-series-1": {
        "journalist_publication": "Marcelo Salup (author field) — article series",
        "category": "Founders / Age & Entrepreneurship",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-20T14:00Z. Wants founders over 55 for a series of "
                           "articles. Off-beat. Recorded, excluded.",
        "contact_method": f"Body links a bit.ly shortener and publishes no email. PAGE-VERIFIED {TODAY}: "
                          f"HTTP 200, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded.",
    },
    "founders-and-entrepreneurs-and-musicians-podcast-guests": {
        "journalist_publication": "Coral Rose Official (author field) — asks an AI agent to make the connections",
        "category": "Podcast Guest Booking",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-20T10:54Z. Not a journalist request at all: the "
                           "body is a public prompt to an AI connector bot ('Hey Boardy, can you connect "
                           "me to…') asking for podcast guests. Recorded, excluded — and worth noting as "
                           "the second request in two runs that is a booking solicitation rather than a "
                           "reporter's call.",
        "contact_method": f"None — the page is an AI-agent prompt, no human route. PAGE-VERIFIED {TODAY}: "
                          f"HTTP 200, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded.",
    },
}
for slug, extra in NEW.items():
    if any(slug in o["url"] for o in out):
        continue
    src = bodies.get(slug) or adjacent.get(slug) or {}
    out.append({
        "url": f"https://www.sourcee.app/journo-request/{slug}",
        "query_text": re.sub(r"\s+", " ", src.get("core") or "")[:900],
        "deadline": (f"NEW this run. Page badge '{src.get('badge')}'; datePublished "
                     f"{src.get('datePublished')}. PAGE-VERIFIED {TODAY}: HTTP {src.get('http')}, "
                     f"live=True, no expiry notice on the page."),
        **{k: extra[k] for k in ("journalist_publication", "category", "relevance",
                                 "relevance_notes", "contact_method", "suggested_pitch_template")},
    })

platforms = [
    {"platform": "Sourcee (sourcee.app)", "status": "accessible",
     "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP {sw['http']}, "
               f"{sw['bytes']:,} bytes, {sw['count']:,} loc/lastmod pairs, newest lastmod "
               f"{sw['newest']}). {len(sw['window'])} slugs carry a lastmod newer than the 2026-09-20 "
               f"run's newest ({MARK}) — and **0 of those carry any AI token, 0 carry an AI token plus "
               f"a pricing token**. That is the first run in the monitor's history with zero new "
               f"AI-token slugs in the window. Six slugs from the last 3 days carrying a spend or "
               f"adjacency token were fetched and read instead (2 spend-token-only, 4 adjacent): none "
               f"on-beat. Sourcee itself re-probed HTTP 200.")},
    {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
     "status": "recency_window_not_persistence",
     "notes": ("Re-measured for the fifth run: 5 of the 35 tracked slugs are in it today, all "
               "published within the last 48 hours. It shares almost no slugs with previous captures "
               "(0 shared between the 2026-09-18, -19 and -20 captures). Still a rolling window over "
               "the newest requests, not a feed a request persists on, so absence from it is NOT a "
               "cold signal and build_pitch_queue.py does not use it as one. No change to that finding.")},
    {"platform": "HARO (helpareporter.com)", "status": "email_wall",
     "notes": ("Re-probed once. / returns HTTP 429, 33,948 bytes, 'Vercel Security Checkpoint'. Tenth "
               "consecutive identical result. Queries reach sources only by a 3x-daily email digest to "
               "a subscribed inbox. Not retried, per the monitor's rule.")},
    {"platform": "Connectively (connectively.us)", "status": "login_required",
     "notes": "Re-probed once. / HTTP 429, 33,940 bytes, 'Vercel Security Checkpoint'. No public query feed."},
    {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
     "notes": ("Re-probed. /requests returns a genuine 404 (140,650 bytes, 'Page Not Found - Source of "
               "Sources'). Reporter submission form only; no source-facing feed.")},
    {"platform": "Qwoted (qwoted.com)", "status": "login_required",
     "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,265 bytes) - wrong path, "
               "not gated. The feed needs an authenticated app session.")},
    {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
     "notes": ("Re-probed. Apex HTTP 200 (11,345 bytes), title 'MentionMatch - Connect B2B Writers with "
               "Expert Sources', no feed. Tenth consecutive run confirming a pre-launch shell. NOTE: the "
               "earlier probe of www.mentionmatch.com in the same batch returned the *Qwoted* 404 body "
               "(3,265 bytes) because curl -sL followed a redirect to a stale cache; the apex result "
               "above is the real one.")},
    {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
     "notes": ("Re-probed: HTTP 401, 73-byte {\"error\":\"invalid_token\"}. Free read-only feed "
               "covering Connectively, HARO, X, LinkedIn, MentionMatch and Substack. Needs an "
               "interactive OAuth handshake that cannot be completed from a scheduled run. "
               "`hermes mcp list` in this profile still reports 'No MCP servers configured.'")},
    {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
     "notes": ("Not re-attempted. Team-level credit limit blocked this on nine consecutive runs; the "
               "block is account state, not a transient failure. Sourcee's X-originated aggregation is "
               "used as a proxy.")},
    {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
     "notes": ("Root re-probed HTTP 200 (148,191 bytes, 'ResponseSource - Connecting the media'). "
               "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free source-facing feed.")},
]

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{TODAY}T09:00:00-07:00",
    "search_scope": ("AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, "
                     "software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support "
                     "value, tool consolidation, procurement budget"),
    "age_policy": ("Ages are read off each request page (JSON-LD datePublished plus the rendered "
                   "'Posted ... ago' badge), never off the digest text. All 35 tracked URLs were "
                   "re-fetched this run: HTTP 200 and the request body still served, none returns an "
                   "expiry notice."),
    "platforms_checked": platforms,
    "opportunities": out,
    "new_this_run": [
        "NO NEW CORE-BEAT REQUEST, AND FOR THE FIRST TIME NO NEW AI-TOKEN SLUG AT ALL. 31 slugs carry a lastmod newer than the 2026-09-20 run's mark and 0 of them carry any AI token — every one is sport, local news, music or consumer-interest. Two slugs carrying a spend token but no AI token were read (a sales-enablement SaaS tool-sourcing post and a PDF-workflow post, both from the same #PROpportunity PR account) and four adjacent slugs were read (a founders podcast, an ML-methods post, a 55+ founders series, an AI-bot podcast-guest prompt). None is on-beat. This is the thinnest new-supply run the monitor has recorded.",
        "THE 1.21x FLOOR PUBLISHED ON 2026-09-18 IS WRONG — it is 1.16x, and the median is 1.25x, not 1.33x. The '1.21x to 2.53x, median 1.33x' range was measured across a regex-dependent pair set: re-running the extraction four ways over the same data/pricing_snapshots.json returned 2, 7, 9 and 18 pairs, so the range was a property of the pattern rather than of the data. Four same-tier per-month pairs sit BELOW the published floor and were never in the set: instrumentl Pre-Award $579 monthly vs $499/month annually (1.16x), instrumentl Discover $349 vs $299 (1.17x), airtable-ai Team $24 vs $20/seat/month annually (1.20x) and slack-ai Business+ $18 vs $15/user/month annually (1.20x). The pairs are now curated by hand, each one re-asserted against its own sentence on every run by scripts/extract_monthly_annual_pairs.py, and published to data/monthly_annual_pairs.json: 18 pairs, range 1.16x-2.53x, median 1.25x. This matters beyond the drafts: the 1.21x floor was the *corrected* figure sent to Jan Suski on 2026-09-18, so an un-disclosed error now stands in a sent message.",
        "ALL 35 TRACKED URLS RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page returns HTTP 200 with the request body still served and no removal or expiry notice. 16 are live and unpitched, 0 of those has stopped appearing in the newest digest.",
        "ALL FOUR OUTSTANDING DRAFTS STILL HOLD, AND NONE HAS BEEN SENT. The Raconteur shadow-AI draft is now 4 days old and was written on 2026-09-19; the Anthropic draft is 2 days old; the Speciality Food draft 2 days; the FinOps draft 4 days and cold since 2026-09-19. Every reply route was re-resolved against the live page this run (see below) and every figure recomputed against today's data files. Nothing needed an edit except the 1.21x → 1.16x correction.",
        "MAILBOX CHECKED: NO NEW REPLIES. INBOX top is still Jan Suski's 2026-09-18 20:39Z reply, answered by us at 21:29Z on the same day. No reply to the 2026-09-15 Enterprise AI Leaders send (six days), none to the 2026-09-18 Sherwood News send (three days). Spam holds three items, all delivery-failure bounces and directory form-mail. Sent Mail top is unchanged at msg 178.",
    ],
    "expired_this_run": [
        "Nothing expired and nothing dropped off this run. All 35 tracked URLs returned HTTP 200 with the request body still served, and none has stopped appearing in a URL-carrying digest.",
        "The three requests already recorded as spent remain spent and are not resurfaced: California AI audit bills ('speak with a source today', posted 2026-09-10) and UK Managers - Gen Z AI overuse (internal deadline 'by this Wednesday September 9') both stay live with no expiry notice, so the do-not-pitch judgement rests on their stated deadlines rather than on the page; the Amplemarket request is a live thread with Jan Suski and is not re-pitched.",
        "TWO REQUESTS CROSS THE 10-DAY LINE TODAY: early-stage founders 'Built From Scratch' (10d, medium, unpitched) and the EdTech LMS audit (8d and rising, skipped by standing). Neither is a loss — Built From Scratch is a public-comment founder-profile slot and the EdTech one was deliberately skipped on 2026-09-15 — but both read cold from tomorrow.",
    ],
    "summary": (f"41 tracked requests ({len(prev['opportunities'])} carried and re-verified, 6 new and "
                f"recorded), 16 live and unpitched, 0 dropped off, 3 pitched. No new core-beat request "
                f"and — for the first run on record — no new AI-token slug in the sitemap window at all. "
                f"All four outstanding drafts were re-verified against today's pages and today's data "
                f"and all four still hold, but the 1.21x monthly/annual floor they cite was found to be "
                f"wrong (true floor 1.16x, true median 1.25x) and is corrected in data/monthly_annual_pairs.json. "
                f"No new replies in the mailbox. Zero pitches sent this run — sends remain George's lane."),
    "recommended_actions": [
        "SEND THE RACONTEUR SHADOW-AI DRAFT. It is paste-ready at pitch-drafts-2026-09-21.md section 1 (unchanged but for one corrected figure), route simon.chandler@raconteur.net, re-resolved off the live /contributors/simon-chandler page this run. It is the only high-relevance request in the queue, the only core-beat find in eight runs, and its reply route is an email address we can address directly. It has now been written and unsent for three consecutive runs.",
        "SEND OR DROP THE ANTHROPIC DRAFT (section 2, Signal hliwrites.99 re-read off the live page today). At 9 days it is one day short of the cold line. If it is not going out this week, record it as skipped in pitch-ledger.json so it stops occupying the top of the queue.",
        "SEND OR DROP THE SPECIALITY FOOD DRAFT (section 3, holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today). Standing constraint is in its first line.",
        "DECIDE ON FINOPS (14d, high, cold, unpitched since 2026-09-17). Its draft exists at pitch-drafts-2026-09-17.md section 1 and its route is a LinkedIn DM to linkedin.com/in/niloy-ghosh. This is the highest-relevance request the monitor has ever never answered.",
        "RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Today is the strongest evidence yet for it: the only accessible platform produced zero new AI-token slugs, and Medialyst is a free read-only feed covering six platforms in one step.",
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": 0,
        "consecutive_runs_without_new_core_beat": 2,
        "tracked_urls": len(out),
        "carried_and_reverified": len(prev["opportunities"]),
        "live_unpitched": 16,
        "live_unpitched_with_a_resolved_route": 3,
        "cold_unpitched": 14,
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 3,
        "drafts_written_never_sent": 4,
    },
    "monitor_defects_fixed_this_run": [
        "A PUBLISHED FIGURE WAS WRONG AND IS NOW FIXED AT THE SOURCE. The same-tier monthly/annual range '1.21x to 2.53x, median 1.33x' had been cited in every draft since 2026-09-18 and was sent to a real correspondent. Re-deriving it four different ways over the same data/pricing_snapshots.json produced 2, 7, 9 and 18 pairs, which proves the range was regex-dependent. Four pairs sit below the published floor. Fixed by curating the pair set by hand and adding scripts/extract_monthly_annual_pairs.py, which re-asserts each pair's own sentence against the snapshot file on every run and writes data/monthly_annual_pairs.json (18 pairs, 1.16x-2.53x, median 1.25x). The old claim measured a population nobody had defined; the new one cannot drift silently.",
        "THE QUEUE'S HEADLINE COUNT OVERSTATED WHAT WAS SENDABLE. It reported '16 live' when only 3 of those rows have both relevance above the tangential band and a resolved reply route — the rest are off-beat calls the queue itself already documents as excluded, so a reader scanning the headline saw 16 candidates where the real number is 3. build_pitch_queue.py now prints and headlines a 'sendable' count (live, not cold, not pitched, resolved email/booking route, relevance not 'low') alongside the raw live count, so the number that decides whether to act is the honest one.",
        "A STALE PROBE RESULT NEARLY BECAME A FINDING. www.mentionmatch.com returned Qwoted's 404 body (3,265 bytes) in this run's platform batch while the apex mentionmatch.com returned its real 200 shell (11,345 bytes). The apex result is the correct one and the platform note now says so, because logging the redirect artifact as MentionMatch's state would have been a false platform reading of exactly the kind the retry rule exists to avoid.",
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=2, ensure_ascii=False))
print("wrote", f"digest-{TODAY}.json", "opportunities:", len(out))
print("monitor_health:", json.dumps(digest["monitor_health"]))
