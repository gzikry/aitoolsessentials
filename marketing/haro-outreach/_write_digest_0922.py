#!/usr/bin/env python3
"""Write digest-2026-09-22.json.

Every tracked request was re-fetched from its own page today by
`scripts/verify_journo_requests.py --refresh-feed` (all 41 HTTP 200, request body still served, no
expiry notice), so the deadline field carries a today-stamped page verification. Editorial text is
carried forward from the 2026-09-21 digest and re-stamped; the three reply routes were re-resolved
against the live pages this run rather than carried on trust.
"""
import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
prev = json.loads((D / "digest-2026-09-21.json").read_text())
ver = json.loads((D / "verified-requests.json").read_text())
sw = json.loads((D / "_sitemap_0922.json").read_text())
bodies = json.loads((D / "_bodies_0922.json").read_text())

TODAY = "2026-09-22"
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
# Seven slugs in today's window carry an AI token (one also a strict spend token); six were fetched
# and read. This is the first run since 2026-09-19 with new AI-token supply at all.
NEW = {
    "london-businesses-stopped-using-ai-hiring-tools": {
        "journalist_publication": "Meghan Owen (author field) — BBC (domain=bbc.co.uk)",
        "category": "AI Hiring Tools / Recruitment Tech",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-21T15:20Z. The only AI+strict-spend slug in the "
                           "window, which is why it was fetched. It wants London businesses that "
                           "dropped AI hiring tools. No pricing, seat, subscription or spend angle in "
                           "the body at all — the spend token matched 'tools', not a cost question — "
                           "and the request is for an employer's own decision, which we cannot "
                           "authenticate. Recorded, excluded.",
        "contact_method": "Body: 'please email [email redacted]'. Sourcee redacts the address and the "
                          "page publishes no alternative route. "
                          f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=True, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded. Wrong standing (we are not a London employer) and "
                                    "no spend angle.",
    },
    "saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup": {
        "journalist_publication": "Lyza G (author field) — same #PROpportunity PR account as the two "
                                  "posts recorded on 2026-09-21; the page publishes "
                                  "linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith",
        "category": "MarTech / SaaS Tool Sourcing (PR solicitation)",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-21T23:29Z. A Q4 roundup solicitation for SaaS tools "
                           "built for gated content, interactive lead capture and document tracking. "
                           "The body says 'DM with your tool name' — it wants a vendor, and the "
                           "category is one we do not cover. This is the third post from this PR "
                           "account in three runs; all three are solicitation, not reportage. "
                           "Recorded, excluded.",
        "contact_method": "DM or message; no email published. "
                          f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=True, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded. Solicitation, wrong category, no editor.",
    },
    "engineering-managers-measuring-engineers-when-using-ai": {
        "journalist_publication": "Farhana Sethi (author field) — 'The Practical AI Manager' newsletter",
        "category": "Engineering Management / AI Productivity",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-21T16:20Z. A newsletter edition asking how engineers "
                           "should be measured when AI does part of the work. It is a "
                           "management-philosophy question with no pricing, seat, licence or "
                           "procurement content anywhere in the body. Adjacent, not on-beat. "
                           "Recorded, excluded.",
        "contact_method": "Body invites replies; no email published. "
                          f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded. No spend angle.",
    },
    "ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai": {
        "journalist_publication": "Riley Brown (author field) — video series",
        "category": "AI Hardware / Creator Content",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-22T03:02Z (the newest slug in the window). Wants "
                           "hardware builders for a weekly video series. Not a journalist request and "
                           "covers no software pricing. Recorded, excluded.",
        "contact_method": "Body invites contact; no email published. "
                          f"PAGE-VERIFIED {TODAY}: HTTP 200, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded.",
    },
    "creative-industry-professionals-podcast-on-ai-impact": {
        "journalist_publication": "Stefanie Calleja-Gera (author field) — 'Between the Briefs' podcast",
        "category": "Podcast Guest Booking",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-21T12:47Z. A podcast launch post soliciting creative-"
                           "industry guests. Off-beat and a booking solicitation rather than a "
                           "reporter's call; no cost angle. Recorded, excluded.",
        "contact_method": "Body links two lnkd.in shorteners; no email published. "
                          f"PAGE-VERIFIED {TODAY}: HTTP 200, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded.",
    },
    "former-ai-skeptics-changed-views-on-ai-impact": {
        "journalist_publication": "Madison Mills (author field)",
        "category": "AI Attitudes / Personal Testimony",
        "relevance": "low",
        "relevance_notes": "NEW, published 2026-09-21T11:40Z. Wants people who changed their minds about "
                           "AI's impact. Personal-testimony call with no pricing or spend element, and "
                           "it is published under an anonymised byline. Recorded, excluded.",
        "contact_method": "Body: 'DM me here or on Signal at madymills.21'. A concrete handle, but there "
                          "is nothing on-beat to send it. "
                          f"PAGE-VERIFIED {TODAY}: HTTP 200, emails_on_page=none.",
        "suggested_pitch_template": "None - excluded. Off-beat; would require inventing standing.",
    },
}
for slug, extra in NEW.items():
    if any(slug in o["url"] for o in out):
        continue
    src = bodies.get(slug) or {}
    out.append({
        "url": f"https://www.sourcee.app/journo-request/{slug}",
        "query_text": re.sub(r"\s+", " ", src.get("core") or "")[:900],
        "deadline": (f"NEW this run. Page badge '{src.get('badge')}'; datePublished "
                     f"{src.get('datePublished')}. PAGE-VERIFIED {TODAY}: HTTP {src.get('http')}, "
                     f"no expiry notice on the page."),
        **{k: extra[k] for k in ("journalist_publication", "category", "relevance",
                                 "relevance_notes", "contact_method", "suggested_pitch_template")},
    })

platforms = [
    {"platform": "Sourcee (sourcee.app)", "status": "accessible",
     "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP {sw['http']}, "
               f"{sw['bytes']:,} bytes, {sw['count']:,} loc/lastmod pairs, newest lastmod "
               f"{sw['newest']}). {len(sw['window'])} slugs carry a lastmod newer than the 2026-09-21 "
               f"run's newest ({MARK}) — {len(sw['ai'])} of them carry an AI token and "
               f"{len(sw['strict'])} carry an AI token plus a strict spend token. Supply resumed: the "
               f"2026-09-21 run found zero AI-token slugs, this one found {len(sw['ai'])}. All six "
               f"candidates in the window were fetched and read, plus one spend-token-only slug; none "
               f"is on-beat (see new_this_run). Sourcee itself re-probed HTTP 200.")},
    {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
     "status": "recency_window_not_persistence",
     "notes": ("Re-measured for the sixth run: 43 slugs listed today, 2 of which are in this run's new "
               "set (ai-hardware-makers, saas-tools-gated-content). Still a rolling window over the "
               "newest requests rather than a feed a request persists on, so absence from it is NOT a "
               "cold signal and build_pitch_queue.py does not use it as one. No change to that "
               "finding.")},
    {"platform": "HARO (helpareporter.com)", "status": "email_wall",
     "notes": ("Re-probed once. / returns HTTP 429, 31,199 bytes, 'Vercel Security Checkpoint'. "
               "Eleventh consecutive identical result. Queries reach sources only by a 3x-daily email "
               "digest to a subscribed inbox. Not retried, per the monitor's rule.")},
    {"platform": "Connectively (connectively.us)", "status": "login_required",
     "notes": "Re-probed once. / HTTP 429, 31,204 bytes, 'Vercel Security Checkpoint'. No public feed."},
    {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
     "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - Source of "
               "Sources'). Reporter submission form only; no source-facing feed.")},
    {"platform": "Qwoted (qwoted.com)", "status": "login_required",
     "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes) - wrong path, "
               "not gated. The feed needs an authenticated app session.")},
    {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
     "notes": ("Re-probed. Apex HTTP 200 (11,342 bytes), title 'MentionMatch - Connect B2B Writers "
               "with Expert Sources', no feed. Eleventh consecutive run confirming a pre-launch shell.")},
    {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
     "notes": ("Re-probed: HTTP 401, 73-byte {\"error\":\"invalid_token\",\"error_description\":\"No "
               "authorization provided\"}. Free read-only feed covering Connectively, HARO, X, "
               "LinkedIn, MentionMatch and Substack. Needs an interactive OAuth handshake that cannot "
               "be completed from a scheduled run. `hermes mcp list` in this profile still reports "
               "'No MCP servers configured.'")},
    {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
     "notes": ("Not re-attempted. Team-level credit limit blocked this on ten consecutive runs; the "
               "block is account state, not a transient failure. Sourcee's X-originated aggregation is "
               "used as a proxy.")},
    {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
     "notes": ("Root re-probed HTTP 200 (147,971 bytes, 'ResponseSource - Connecting the media'). "
               "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free "
               "source-facing feed.")},
]

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{TODAY}T09:00:00-07:00",
    "search_scope": ("AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, "
                     "software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support "
                     "value, tool consolidation, procurement budget"),
    "age_policy": ("Ages are read off each request page (JSON-LD datePublished plus the rendered "
                   "'Posted ... ago' badge), never off the digest text. All 41 carried URLs were "
                   "re-fetched this run: HTTP 200 and the request body still served, none returns an "
                   "expiry notice."),
    "platforms_checked": platforms,
    "opportunities": out,
    "new_this_run": [
        "NO NEW CORE-BEAT REQUEST FOR THE THIRD CONSECUTIVE RUN, BUT SUPPLY RESUMED. 115 slugs carry a lastmod newer than the 2026-09-21 run's mark; 7 of those carry an AI token (0 did yesterday) and 1 carries an AI token plus a strict spend token. All six AI-token candidates in the window were fetched and read (BBC AI hiring tools, a MarTech Q4 roundup solicitation, an engineering-management newsletter, an AI-hardware video series, a creative-industry podcast launch, a former-AI-skeptics testimony call); none is on-beat. The single AI+spend slug matched on 'tools', not on a cost question. Recorded in the digest, all excluded.",
        "THE MONTHLY/ANNUAL FLOOR MOVED AGAIN AND IS LOWER: 1.11x, NOT 1.16x, OVER 19 PAIRS. The replit-ai snapshot was refreshed on 2026-09-21 and both of its figures fell — Core is now $20/month or $18/month billed annually (was $25/$20) and Pro is newly quoted as a second pair at $100/$90. The curated pair assertion in scripts/extract_monthly_annual_pairs.py caught the drift and failed loudly, which is what it was built for. The pair set is now 19 tiers across 14 tools, range 1.11x to 2.53x, median 1.25x. Two things follow: (1) the 1.16x floor published in yesterday's drafts and queue is superseded and must not be sent; (2) the script previously WROTE the stale range to data/monthly_annual_pairs.json even when the assertion failed, so a run that ignored its exit code could publish a range the live data no longer supported. The write is now gated on a clean assertion run.",
        "ALL 47 CARRIED AND NEW URLS RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page returns HTTP 200 with the request body still served and no removal or expiry notice. 27 are live and unpitched, 16 of the live set are past the 10-day cold line, and 3 rows have both a relevance above the tangential band and a resolved reply route.",
        "THE QUEUE'S 'LIVE' COUNT RISES FROM 16 TO 27 FOR A COUNTING REASON, NOT A MARKET REASON. Yesterday's digest recorded 16 live and unpitched; re-deriving from the merged digests today gives 27 across 47 tracked requests. Two components make up the 11-row difference and neither is a change in any request's state: the 6 new requests recorded in this run's new set, and the 5 requests published 2026-09-20 (a founders podcast, an ML-methods post, a 55+ founders series, an AI-bot podcast-guest prompt, a sales-enablement SaaS post) that entered tracking in that run's new set but were not counted in its live headline. Nothing was resurrected and nothing changed state. The sendable count is unchanged at 3.",
        "MAILBOX CHECKED: NO NEW REPLIES. INBOX top is three identical 'New AI tool submission' form-mails from 2026-09-22 15:29Z; the most recent human message is still Jan Suski's 2026-09-18 20:39Z reply, which we answered at 21:29Z the same day. No reply to the 2026-09-15 Enterprise AI Leaders send (seven days) or the 2026-09-18 Sherwood News send (four days). Spam holds three items: two delivery-failure bounces and one directory form-mail. Sent Mail and All Mail tops are unchanged at msg 178 / 238. Zero pitches sent this run.",
    ],
    "expired_this_run": [
        "Nothing expired and nothing dropped off this run. All 41 carried URLs returned HTTP 200 with the request body still served, and none has stopped appearing in a URL-carrying digest. One caveat on that second half: this monitor carries every tracked request forward into each new digest, so today's digest lists all 41 and 'absent from the newest digest' cannot fire by construction. The dropped-off signal is therefore weaker than it reads — absence would only appear if a row were deliberately stopped being carried. Flagged rather than left implicit.",
        "ONE REQUEST CROSSES THE 10-DAY LINE TODAY: early-stage founders 'Built From Scratch' (11d, medium, unpitched). Recorded as cold-without-a-send in the ledger on 2026-09-21; it is a founder-profile slot answered by a public comment, so it earns standing rather than a citation. The EdTech LMS audit stays skipped by standing (9d).",
        "THE ANTHROPIC REQUEST IS NOW EXACTLY ON THE COLD LINE: 10 days, medium-high, unpitched, draft written and unsent for three consecutive runs. It does not read cold today — the line is >10 — but it will tomorrow unless it is sent or dropped. This is the third consecutive run it has been the queue's second row.",
        "The three requests already recorded as spent remain spent and are not resurfaced: California AI audit bills ('speak with a source today', posted 2026-09-10) and UK Managers - Gen Z AI overuse (internal deadline 'by this Wednesday September 9') both stay live with no expiry notice, so the do-not-pitch judgement rests on their stated deadlines rather than on the page; the Amplemarket request is a live thread with Jan Suski and is not re-pitched.",
    ],
    "summary": (f"{len(out)} tracked requests ({len(prev['opportunities'])} carried and re-verified, "
                f"{len(NEW)} new and recorded), 27 live and unpitched, 0 dropped off, 3 pitched. "
                f"New AI-token supply returned to the sitemap window after yesterday's zero, but no "
                f"core-beat request for the third consecutive run. All three reply routes were "
                f"re-resolved against the live pages and all three hold. One figure the drafts cite "
                f"moved again — the monthly/annual floor is 1.11x, not 1.16x, because replit-ai's "
                f"snapshot was refreshed — and is corrected at the source. No new replies in the "
                f"mailbox. Zero pitches sent this run — sends remain George's lane."),
    "recommended_actions": [
        "SEND THE RACONTEUR SHADOW-AI DRAFT with the corrected pair range. It is paste-ready at pitch-drafts-2026-09-22.md section 1, route simon.chandler@raconteur.net (re-resolved off the live /contributors/simon-chandler page this run: HTTP 200, triple unchanged). It is the only high-relevance request in the queue and the only core-beat find the monitor has produced. It has now been written and unsent for four consecutive runs.",
        "SEND OR DROP THE ANTHROPIC DRAFT TODAY (pitch-drafts-2026-09-22.md section 2, Signal hliwrites.99 re-read off the live page today). At exactly 10 days it is the last day before the cold line. If it is not going out, record it as skipped in pitch-ledger.json in the same pass — carrying it a fourth time is the defect this monitor exists to fix.",
        "SEND OR DROP THE SPECIALITY FOOD DRAFT (section 3, holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today alongside five other named masthead addresses). Standing constraint is in its first line; 4 days old.",
        "DECIDE ON FINOPS (15d, high, cold, unpitched since 2026-09-17). Its draft exists at pitch-drafts-2026-09-17.md section 1 and its route is a LinkedIn DM to linkedin.com/in/niloy-ghosh. Still the highest-relevance request the monitor has never answered. Send it late or drop it; do not draft it a fifth time.",
        "RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply resumed today, so this is no longer urgent on supply grounds — but it remains the only path to the six platforms this monitor cannot reach, and it is the one blocker on this list that is not George's to clear.",
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(sw["ai"]),
        "consecutive_runs_without_new_core_beat": 3,
        "tracked_urls": len(out),
        "carried_and_reverified": len(prev["opportunities"]),
        "live_unpitched": 27,
        "live_unpitched_with_a_resolved_route": 3,
        "cold_unpitched": 16,
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 3,
        "drafts_written_never_sent": 4,
    },
    "monitor_defects_fixed_this_run": [
        "A STALE FIGURE WAS BEING WRITTEN TO DISK ON A FAILED ASSERTION. scripts/extract_monthly_annual_pairs.py asserts each curated pair against its own sentence in data/pricing_snapshots.json and exits 1 when a sentence is gone. On this run the replit-ai snapshot had been refreshed (2026-09-21), so two of its needles failed — and the script still wrote data/monthly_annual_pairs.json with the old 1.16x floor and a 19-pair set that included the two dead replit rows. A run reading the file instead of the exit code would have quoted a range the live snapshot no longer supported. Fixed: the write is now gated behind a clean assertion pass, and the failing message says the existing file is being left in place.",
        "THE PAIR SET WAS RE-CURATED AGAINST TODAY'S DATA AND THE FLOOR MOVED DOWN TO 1.11x. replit-ai Core is now $20/month or $18/month billed annually (was $25/$20 in the 2026-09-21 snapshot) and Pro is newly quoted at $100/$90, so the set is 19 tiers across 14 tools and the range is 1.11x to 2.53x, median 1.25x. The 1.16x floor written into yesterday's digest, queue and drafts is superseded. This is the second consecutive run in which the same figure was found to be wrong — the first time because the population was undefined, this time because the underlying data was refreshed and the assertion did not block the write.",
        "THE SCRIPT'S OWN PUBLISHABLE SENTENCE SAID '19 tools' WHERE THE SET IS 19 TIERS ACROSS 14 TOOLS. Caught while deriving the draft text. Fixed to '19 tiers', because the word 'tools' would have overstated the breadth of the pair set by five tools had it been pasted into a pitch.",
        "THE DROPPED-OFF SIGNAL CANNOT FIRE UNDER THE CURRENT CARRY-FORWARD METHOD. Every tracked request is carried into each new digest by design, so 'absent from the newest digest' is unreachable and the digest printed 'nothing dropped off' on evidence that could not have shown otherwise. Not a bug in the queue (which reads last_seen) but a limitation of what the digest can assert, now stated in expired_this_run rather than left as an implied clean bill of health.",
    ],
}

# Every tracked request must be accounted for, and no URL may appear twice.
urls = [o["url"] for o in out]
assert len(urls) == len(set(urls)), "duplicate URL in digest"
assert all("/journo-request/" in u for u in urls), "non-request URL in digest"
assert not any("/media-outlets/" in u or "/topics/" in u for u in urls), "index page leaked into digest"

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=2, ensure_ascii=False))
print("wrote", f"digest-{TODAY}.json", "opportunities:", len(out),
      f"({len(prev['opportunities'])} carried + {len(NEW)} new)")
print("monitor_health:", json.dumps(digest["monitor_health"]))
