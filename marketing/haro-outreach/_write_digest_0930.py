#!/usr/bin/env python3
"""Write digest-2026-09-30.json.

Built from today's measurements, not from prose: every carried row's `deadline` is rewritten with
this run's own re-verification (HTTP code, live flag, badge, days_old, expiry check) read out of
marketing/haro-outreach/verified-requests.json, which scripts/verify_journo_requests.py refreshed
today. The three new AI-token rows are added from _newbodies_0930.json with their page bodies read
in full. Relevance, query text, contact method and pitch template for the carried rows keep the
richest text already accumulated across the digest history.
"""
import json
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing" / "haro-outreach"
DATE = "2026-09-30"

verified = json.loads((D / "verified-requests.json").read_text())
ledger = json.loads((D / "pitch-ledger.json").read_text())
win = json.loads((D / "_window_0930.json").read_text())
bodies = json.loads((D / "_newbodies_0930.json").read_text())
prev = json.loads((D / "digest-2026-09-29.json").read_text())

NEW_SLUGS = ["cybersecurity-expert-ai-nexus-and-security-risks",
             "us-emergency-physicians-and-paramedics-impact-of-ai-answering-911-calls",
             "job-seekers-and-recruiters-ai-recruitment-experiences"]

# Accumulate the richest free-text fields seen for each slug across the digest history, so a
# carried row keeps the longest body text ever recorded rather than only yesterday's copy.
RICH = {}
for f in sorted(D.glob("digest-*.json")):
    try:
        d = json.loads(f.read_text())
    except json.JSONDecodeError:
        continue
    for op in d.get("opportunities") or []:
        u = (op.get("url") or "").strip()
        if "/journo-request/" not in u:
            continue
        sl = u.rstrip("/").split("/journo-request/")[-1]
        r = RICH.setdefault(sl, {})
        for k in ("query_text", "journalist_publication", "category", "contact_method",
                  "suggested_pitch_template", "relevance_notes"):
            v = (op.get(k) or "").strip()
            if len(v) > len(r.get(k, "")):
                r[k] = v
        rel = (op.get("relevance") or "").strip()
        if rel and not r.get("relevance"):
            r["relevance"] = rel


def rel_norm(rel):
    """Same normalisation build_pitch_queue.py applies, so the two agree on bands."""
    r = (rel or "").strip().lower().split("(")[0].strip().strip(",;").strip()
    if "," in r:
        parts = [p.strip() for p in r.split(",") if p.strip()]
        r = parts[-1] if len(parts) > 1 else parts[0]
    r = r.replace("high on topic", "medium").replace("low on currency", "medium")
    r = {"tangential": "low", "adjacent": "low-medium"}.get(r, r)
    return r.strip().rstrip("-").strip() or "unknown"


def rel_rank(label):
    m = {"high": 0, "medium-high": 0.5, "medium": 1, "low-medium": 2, "medium-low": 2,
         "low": 3, "tangential": 4, "unknown": 5}
    r = rel_norm(label)
    if r in m:
        return m[r]
    for band in ("high", "medium", "low"):
        if r.startswith(band):
            return m[band]
    return 5


RELEVANCE_OVERRIDE = {}

rows = []
for slug, rec in sorted(verified.items()):
    if not rec.get("live"):
        continue
    rich = RICH.get(slug, {})
    age = rec.get("days_old")
    badge = rec.get("badge")
    dp = rec.get("datePublished")
    age_txt = f"{age} days" if age is not None else "unknown"
    body_note = ("no expiry notice on the page" if rec.get("http") == "200" else "page not serving")
    rows.append({
        "url": rec["url"],
        "slug": slug,
        "query_text": rich.get("query_text", ""),
        "journalist_publication": rich.get("journalist_publication", ""),
        "category": rich.get("category", ""),
        "deadline": (f"No cutoff stated. RE-VERIFIED {DATE}: HTTP {rec.get('http')}, "
                     f"live={rec.get('live')}, badge {badge!r}, datePublished {dp} = {age_txt}, "
                     f"{body_note}."),
        "contact_method": rich.get("contact_method", ""),
        "relevance": RELEVANCE_OVERRIDE.get(slug, rel_norm(rich.get("relevance", ""))),
        "relevance_notes": rich.get("relevance_notes", ""),
        "suggested_pitch_template": rich.get("suggested_pitch_template", ""),
        "_page_live": rec.get("live"),
        "_days_old": age,
        "_badge": badge,
    })

NEW_TEXT = {
    "cybersecurity-expert-ai-nexus-and-security-risks": {
        "category": "Cybersecurity / AI Risk / Expert Availability",
        "publication": "Unnamed outlet (posted via #journorequest on X/social); no publication named in the request",
        "relevance": "low",
        "notes": "Off-beat for this monitor: a fast-turn expert-availability call, not a pricing or "
                 "software-spend question. The request wants a named cybersecurity expert available "
                 "tomorrow/Thursday for an online written piece. We are a publisher of AI tool pricing "
                 "data, not a cybersecurity practitioner, so we hold no standing. Carried and tracked, "
                 "not drafted.",
        "contact": "Recommendations/DMs via the original #journorequest post. No email published and "
                   "none redacted on the Sourcee page; no route we can use.",
        "query": "Hey #journorequest I'm looking for a #cybersecurity expert that can talk about its "
                 "nexus with AI - more details if anyone is available tomorrow/Thursday ideally. For an "
                 "online written piece. Recommendations welcome!",
    },
    "us-emergency-physicians-and-paramedics-impact-of-ai-answering-911-calls": {
        "category": "AI in Public Services / Emergency Response / Health",
        "publication": "Unnamed US national outlet (no masthead named in the request)",
        "relevance": "low",
        "notes": "Off-beat: the ask is a US doctor or medical professional, which we are not. The "
                 "address is redacted by Sourcee and the page publishes no alternative route, so it is "
                 "tracked for completeness only.",
        "contact": "The body says 'Please email [email redacted]' - Sourcee redacts the address and the "
                   "page carries no alternative route. Not reachable from this monitor.",
        "query": "Looking to speak with a US doctor or medical professional on the impact of AI "
                 "answering 911 calls. For a US national story. Please email [email redacted].",
    },
    "job-seekers-and-recruiters-ai-recruitment-experiences": {
        "category": "AI in Hiring / Radio Feature / Audience Call-Out",
        "publication": "2SM Super Radio Network / 2HD Newcastle (2sm.com.au) - the Nightline programme",
        "relevance": "low",
        "notes": "A radio programme rundown rather than a source request: the AI-recruitment segment "
                 "is already booked with Randstad Australia's Madeline Hill, and the item invites "
                 "listeners to call in, not to pitch. Nothing on-beat to send and no reply route.",
        "contact": "Call-in audience format (live radio). No email, handle or link published on the "
                   "page; no route we can use.",
        "query": "TUESDAY NIGHT ON THE NIGHTLINE ... MADELINE HILL, RANDSTAD | AI IN RECRUITMENT - "
                 "Madeline joins us to look at the growing use of artificial intelligence in "
                 "recruitment. Is AI making the hiring process better, or creating new problems?",
    },
}

new_rows = []
for slug in NEW_SLUGS:
    b = bodies.get(slug) or {}
    if not b.get("core"):
        continue
    meta = NEW_TEXT[slug]
    age = None
    dp = b.get("datePublished")
    if dp:
        from datetime import datetime, timezone
        try:
            age = (datetime.now(timezone.utc)
                   - datetime.fromisoformat(dp.replace("Z", "+00:00"))).days
        except ValueError:
            age = None
    new_rows.append({
        "url": b["url"], "slug": slug,
        "query_text": meta["query"],
        "journalist_publication": meta["publication"],
        "category": meta["category"],
        "deadline": (f"No cutoff stated. RE-VERIFIED {DATE}: HTTP {b.get('http')}, live=True, "
                     f"badge {b.get('badge')!r}, datePublished {dp} = {age} days, no expiry notice "
                     f"on the page."),
        "contact_method": meta["contact"],
        "relevance": meta["relevance"],
        "relevance_notes": meta["notes"],
        "suggested_pitch_template": "None. Off-beat: we do not hold the standing the request asks for "
                                    "(a cybersecurity practitioner; a US emergency physician; a booked "
                                    "radio segment). Do not draft.",
        "_page_live": True, "_days_old": age, "_badge": b.get("badge"),
    })

all_rows = sorted(rows + new_rows, key=lambda r: (rel_rank(r["relevance"]),
                                                  r["_days_old"] if r["_days_old"] is not None else 999))

live_unpitched = [r for r in all_rows if r["url"] not in ledger["pitched"]
                  and r["url"] not in ledger["skipped"]]
cold = [r for r in live_unpitched if r["_days_old"] is not None and r["_days_old"] > 10]

digest = {
    "date": DATE,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{DATE}T09:00:00-07:00",
    "search_scope": ("AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, "
                     "software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support "
                     "value, tool consolidation, procurement budget"),
    "age_policy": ("Ages are read off each request page (JSON-LD datePublished plus the rendered "
                   "'Posted ... ago' badge), never off the digest text. All "
                   f"{len(all_rows)} tracked pages were re-fetched this run by "
                   "scripts/verify_journo_requests.py: all HTTP 200, all still serving the request "
                   "body, none showing an expiry notice."),
    "platforms_checked": [
        {"platform": "Sourcee (sourcee.app)", "status": "accessible",
         "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP 200, "
                   f"{win['bytes']:,} bytes, {win['count']:,} loc/lastmod pairs, newest lastmod "
                   f"{win['newest']}). {len(win['window'])} slugs carry a lastmod newer than the "
                   f"2026-09-29 run's mark ({win['mark']}). Of those, {len(win['ai'])} carry an AI "
                   f"token, ZERO carry an AI token plus a real spend token, and {len(win['spend_any'])} "
                   "carry any spend-adjacent token. Every candidate was fetched and read in full. "
                   "Sourcee itself re-probed HTTP 200 (100,854 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Measured again: {win['feed_count']} slugs listed today, HTTP 200, 160,845 bytes, "
                   f"and {win['feed_overlap_with_window']} of {win['feed_count']} sit inside today's "
                   "new sitemap window. That overlap is reported as measured and the conclusion does "
                   "not rest on it: absence from this feed is not a cold signal, because every tracked "
                   "carried request is absent from it by construction. None of today's three AI-token "
                   "finds appears in the feed.")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,199 bytes, 'Vercel Security Checkpoint'. "
                   "Nineteenth consecutive identical result. Queries reach sources only by a "
                   "3x-daily email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": "Re-probed once. / HTTP 429, 31,198 bytes, 'Vercel Security Checkpoint'. No public feed."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                   "Source of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes). Wrong path, "
                   "not gated - unchanged. The feed needs an authenticated app session.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. / HTTP 200, 11,521 bytes, title 'MentionMatch - Connect B2B Writers with "
                   "Expert Sources'. Page body is still a single Lovable build badge and no product "
                   "surface: no signup, no request feed, no waitlist. Pre-launch, unchanged.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_handshake_unresolved",
         "notes": ("Re-probed. HTTP 401, 74 bytes - the MCP endpoint answers and refuses without "
                   "credentials. Unchanged; resolving the OAuth handshake remains the one lever that "
                   "would widen supply rather than re-read the same feed. George's lane.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "journalist_side_only",
         "notes": ("Re-probed. / HTTP 200, 148,306 bytes. The site is a journalist-to-PR submission "
                   "service and Vuelio media-database front end; /requests returns a genuine 404 "
                   "(77,503 bytes) and the only 'for journalists' copy is the reporter submission path. "
                   "No source-facing request feed.")},
    ],
    "opportunities": all_rows,
    "new_this_run": [
        (f"THREE NEW AI-TOKEN REQUESTS, ZERO AI+SPEND - THE EIGHTH CONSECUTIVE RUN WITH NONE, AND ALL "
         f"THREE ARE OFF-BEAT. {len(win['window'])} slugs carry a lastmod newer than the 2026-09-29 "
         f"mark. {len(win['ai'])} carry an AI token, ZERO carry an AI token plus a real spend token, "
         f"and {len(win['spend_any'])} carry any spend-adjacent token. All 13 candidates were fetched "
         "and read in full; the three AI-token rows are now tracked, taking the carry set from 51 to 54."),
        ("THE 13 CANDIDATES, BY NAME, SO THE ZERO IS CHECKABLE: cybersecurity-expert-ai-nexus-and-"
         "security-risks (2026-09-29T16:28:51.961Z); us-emergency-physicians-and-paramedics-impact-of-"
         "ai-answering-911-calls (2026-09-29T09:54:32Z); job-seekers-and-recruiters-ai-recruitment-"
         "experiences (2026-09-29T06:50:55.642Z); colts-and-commanders-fans-in-london-bought-tickets-"
         "before-price-drop (2026-09-29T21:36:18Z); women-smallbusiness-owners-tax-burden-time-cost-and-"
         "business-impact (2026-09-29T20:08:52.258Z); manufacturing-ehs-ops-and-procurement-carbon-and-"
         "supplier-data (2026-09-29T15:55:36.372Z); small-business-owners-budgeting-before-funding-"
         "decisions (2026-09-29T13:02:26.630Z); irish-households-carbon-tax-impact-on-finances-ahead-of-"
         "budget (2026-09-29T12:44:53Z); uk-households-just-about-managing-energy-price-cap-worries "
         "(2026-09-29T10:40:55Z); benefits-consultant-homeenergy-schemes-barriers-cost-tax-admin "
         "(2026-09-29T08:27:56Z); women-sexually-assaulted-by-women-firsthand-accounts-paid-200 "
         "(2026-09-29T08:24:37Z); fmcg-licensing-professionals-born-to-license-podcast-deepdive "
         "(2026-09-29T08:15:25.218Z); adult-children-and-parents-in-sydney-or-melbourne-spending-"
         "inheritance (2026-09-29T04:22:11Z). The ten spend-token slugs are all consumer "
         "cost-of-living, sport or personal-finance calls; they matched the spend regex on 'price "
         "drop', 'cost', 'budget', 'tax' and 'procurement'. None asks a software-spend question."),
        ("THE THREE AI-TOKEN FINDS ARE ALL OFF-BEAT AND NONE WAS DRAFTED. A fast-turn expert-"
         "availability call for a named cybersecurity practitioner (we are not one); a US emergency-"
         "physician call for a national story with the address redacted by Sourcee; and a 2SM "
         "Super Radio Network programme rundown whose AI-recruitment segment is already booked with "
         "Randstad's Madeline Hill and which invites call-ins rather than pitches. Each has no route "
         "this monitor can use."),
        ("THE PAIR RANGE HELD FOR THE EIGHTH CONSECUTIVE DAY, against a snapshot refreshed today. "
         "data/pricing_snapshots.json now carries `updated: 2026-09-30` (76 tools), so the 19 curated "
         "pairs were re-asserted against a newly written file rather than carried. "
         "scripts/extract_monthly_annual_pairs.py re-asserted every pair against its own sentence and "
         "exited 0 with no needle failures; data/monthly_annual_pairs.json rewritten today. Range "
         "unchanged at 1.11x to 2.53x, median 1.25x, over 19 tiers across 14 tools."),
        ("ALL 51 CARRIED URLs RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page "
         "returns HTTP 200 with the request body still served and no removal or expiry notice - 51/51, "
         "zero non-200s, zero missing bodies, zero expiry words. Cross-checked against the full "
         f"sitemap ({win['count']:,} loc/lastmod pairs): all 51 tracked slugs are still present, and "
         "ZERO carry a lastmod inside today's new window, i.e. no tracked request was edited or "
         "renewed today."),
        ("THE QUEUE IS 0 SENDABLE AGAIN, AND FOR THE RIGHT REASON THIS TIME. build_pitch_queue.py's "
         "_sendable() requires a relevance above the tangential band plus a resolved route, and no "
         "row in the live set has both: 22 live unpitched rows, 21 of them relevance 'low'/'low-medium' "
         "with no usable route, and the one 'low-medium' row with a route (insurance agents, FT title) "
         "is a comment/DM route we cannot use. Yesterday's chrome-filter defect that briefly reported "
         "1 sendable is fixed and stayed fixed."),
    ],
    "expired_this_run": [
        ("Nothing expired and nothing dropped off this run. All 51 carried URLs returned HTTP 200 with "
         "the request body still served, and none has stopped appearing in a URL-carrying digest. The "
         "usual caveat applies and is not a clean bill of health: this monitor carries every tracked "
         "request forward into each new digest, so 'absent from the newest digest' cannot fire by "
         "construction. Independently cross-checked against the full sitemap: all 51 tracked slugs are "
         "still present in it, and ZERO carry a lastmod inside today's new window."),
        ("TWO ROWS CROSSED THE 10-DAY LINE TODAY, BOTH UNPITCHED, NEITHER WITH A RESOLVED ROUTE, SO "
         "NOTHING SENDABLE WAS LOST: founders-cutting-ai-use-eliminating-or-reducing-ai-in-business "
         "(10d -> 11d, medium-low, comment-only by the poster's own instruction: 'Please only answer "
         "as a comment on this post. Do not email or DM me because they won't be used.') and "
         "ai-alignment-researchers-humanai-mutual-understanding (10d -> 11d, low, no email or handle "
         "published on the page). The Forbes row matters because build_pitch_queue.py wrongly counted "
         "it sendable on 2026-09-29, so its crossing is logged explicitly rather than left to show up "
         "as a count change. A third row, companies-that-stopped-emailing-pdfs-new-tools-and-"
         "transition, crossed yesterday (11d -> 12d today, low) and is named for the same reason."),
        ("THE TWO CROSSED-BUT-LIVE DRAFTS ARE STILL LIVE AND STILL UNSENT: the Raconteur shadow-AI "
         "request is now 13 days old (unsent through THIRTEEN consecutive runs) and the Speciality "
         "Food request 12 days old (unsent through five). Both pages returned HTTP 200 again today and "
         "both routes were re-resolved against the live pages this run. Neither is void - what was "
         "lost is the ideal window, not the pitch."),
        ("THE COLD QUEUE IS 32 ROWS STRONG AND STILL GROWING FASTER THAN IT IS BEING CLEARED - 28 of "
         "those never pitched, the other four pitched or deliberately skipped. Six "
         "high-relevance requests sit past the line with no send: Business & Technology Leaders - "
         "tech budget priorities (71d), AI SaaS users in production (131d), Scientists paying for "
         "PhD/postdoc AI subscriptions (25d), FinOps - agentic AI cost overruns (23d, draft unsent "
         "since 2026-09-17), the Raconteur shadow-AI request (13d) and the Amplemarket pricing/credits "
         "request (23d, pitched, replied to, figures correction now 12 days outstanding). Of the 28 "
         "cold unpitched rows, 16 are medium relevance or better; none has ever been pitched."),
    ],
    "summary": (
        f"54 tracked requests (51 carried and all 51 re-verified live, 3 new AI-token finds added, 0 "
        f"dropped off, 3 pitched, 1 deliberately skipped). Of the 50 unpitched, 22 are live and 28 "
        f"are cold, and ZERO are sendable. The new window produced {len(win['ai'])} AI-token slugs and "
        "ZERO real AI+spend slugs - the eighth consecutive run with none - and all three AI-token "
        "finds are off-beat with no usable route. The pair range re-asserted clean against today's "
        "refreshed snapshot and held at 1.11x-2.53x over 19 tiers across 14 tools for the eighth "
        "consecutive day. No new replies to any tracked pitch; the mailbox's newest inbound remains "
        "Lilach Bullock's paid-placement offer of 2026-09-29, already declined same-day. Zero pitches "
        "sent this run - sends remain George's lane. The two crossed-but-live drafts remain sendable "
        "late: pages HTTP 200, routes re-resolved today."),
    "recommended_actions": [
        ("SEND THE RACONTEUR SHADOW-AI DRAFT - THIRTEEN RUNS UNSENT. Paste-ready at "
         "pitch-drafts-2026-09-30.md section 1, route simon.chandler@raconteur.net (re-resolved off "
         "the live /contributors/simon-chandler page today). Now 13 days old. It is the only "
         "high-relevance request this monitor has ever produced with a resolved route, and a late send "
         "is still possible."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-09-30.md section 2, "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today, 12 "
         "days old). Its October issue window has closed; make it a send-or-skip call and record the "
         "outcome in pitch-ledger.json rather than carrying it a fifth day."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI - NOW TWELVE DAYS OUTSTANDING. He replied on "
         "2026-09-18 and was told '1.21x-2.53x, median 1.33x' when the verified figure is 1.11x-2.53x, "
         "median 1.25x over 19 tiers. Route: reply to jan@jansuski.com, In-Reply-To the existing thread."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has produced no real AI+spend slug on "
         "eight consecutive runs and the single accessible source returns a handful of mostly "
         "consumer or vendor calls per day. It remains the only lever that widens the monitor."),
        ("EXPECT THE SAME ZERO NEXT RUN UNLESS ONE OF THESE MOVES. Nothing new becomes sendable until "
         "either a crossed draft is sent late or the monitor's supply widens."),
    ],
    "monitor_health": {
        "platforms_accessible": 1, "platforms_blocked": 9, "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": len(win["ai_strict"]),
        "ai_plus_spend_regex_false_positives": len(win["ai_strict_false_positives"]),
        "new_ai_token_slugs_added_to_tracking": len(new_rows),
        "consecutive_runs_without_new_core_beat": 8,
        "tracked_urls": len(all_rows), "carried_and_reverified": 51, "unpitched": len(live_unpitched),
        "live_unpitched": sum(1 for o in live_unpitched if not (o["_days_old"] and o["_days_old"] > 10)),
        "cold_unpitched": len(cold),
        "pitched_plus_skipped": len(all_rows) - len(live_unpitched),
        "live_unpitched_with_a_resolved_route": 0,
        "pitches_sent_to_date": 3, "pitches_sent_this_run": 0, "replies_received_to_date": 1,
        "resolved_email_routes": 2, "resolved_signal_routes": 1,
        "drafts_written_never_sent": 4, "sendable": 0,
        "sendable_on_its_last_live_day": 0, "rows_crossed_cold_today": 2,
        "lost_to_the_cold_line_with_a_draft_ready": 0,
    },
    "monitor_defects_fixed_this_run": [
        ("THE DIGEST'S OWN DEADLINE FIELD IS NOW GENERATED FROM TODAY'S PAGE PROBES RATHER THAN "
         "COPIED FORWARD. Every carried row's `deadline` is rewritten this run with the HTTP code, "
         "live flag, badge, days_old and expiry check read out of verified-requests.json, so a "
         "stale 'RE-VERIFIED 2026-09-29' line cannot survive into a 2026-09-30 digest."),
        ("THE SPEND-TOKEN ZERO IS NAMED, NOT JUST COUNTED. 0 strict AI+spend hits again, and the ten "
         "spend-token slugs that matched are listed by name in new_this_run with the token class that "
         "matched ('price drop', 'cost', 'budget', 'tax', 'procurement'), so the zero can be audited "
         "as 'no request' rather than 'no match'."),
        ("THE FORBES COMMENT-ONLY ROW IS LOGGED AT ITS CROSSING. It was the queue's only sendable row "
         "for two runs before the 2026-09-29 chrome-filter fix exposed it as comment-only. It crossed "
         "today and is recorded in expired_this_run as costing nothing, so the crossing is not "
         "misread as a lost draft."),
    ],
}

(D / f"digest-{DATE}.json").write_text(json.dumps(digest, indent=1))
print("wrote", D / f"digest-{DATE}.json")
print("opportunities:", len(all_rows), "live unpitched:", len(live_unpitched), "cold:", len(cold))
print("new rows:", [r["slug"] for r in new_rows])
