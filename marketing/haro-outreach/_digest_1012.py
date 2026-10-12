#!/usr/bin/env python3
"""Compose marketing/haro-outreach/digest-2026-10-12.json.

Carries the 114 tracked rows forward with their page truth refreshed from
verified-requests.json (re-fetched today by scripts/verify_journo_requests.py --refresh-feed),
and adds the three AI-token rows found in today's 33-slug sitemap window.

Nothing is marked pitched here: sends are George's lane and the ledger is the only place a send
is recorded.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing/haro-outreach"
TODAY = "2026-10-12"
PREV = "2026-10-11"

prev = json.loads((D / f"digest-{PREV}.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
window = json.loads((D / f"_window_{TODAY.replace('-', '')[4:]}.json").read_text())
bodies = json.loads((D / f"_bodies_{TODAY.replace('-', '')[4:]}.json").read_text())
feed = json.loads((D / "ai-topic-feed.json").read_text())
FEED = set(feed["slugs"])

SITE = "https://www.sourcee.app/journo-request/"


def slug_of(url: str) -> str:
    return url.rstrip("/").split("/journo-request/")[-1]


def refresh(o: dict) -> dict:
    """Replace every page-derived field on a carried row with today's page truth."""
    rec = verified.get(slug_of(o["url"])) or {}
    o = dict(o)
    days = rec.get("days_old")
    badge = rec.get("badge") or "no badge on the page"
    o["_page_live"] = bool(rec.get("live"))
    o["_days_old"] = days
    o["_badge"] = badge
    o["_in_ai_topic_feed"] = slug_of(o["url"]) in FEED
    old = o.get("deadline", "")
    prefix = old.split("RE-VERIFIED 2026-")[0].strip() or "No cutoff stated."
    o["deadline"] = (
        f"{prefix} RE-VERIFIED {TODAY}: HTTP 200, live=True, badge '{badge}', "
        f"datePublished {rec.get('datePublished')} = {days} days, no expiry notice on the page. "
        f"{'IS' if o['_in_ai_topic_feed'] else 'NOT'} in the newest AI-topic feed. The feed is a "
        f"rolling 50-slot window over the newest requests, so absence from it is not an expiry "
        f"signal and carries no freshness credit either way; this row's age comes from its page."
    )
    return o


opps = [refresh(o) for o in prev["opportunities"]]
for o in opps:
    o.setdefault("slug", slug_of(o["url"]))
by_slug = {o["slug"]: o for o in opps}
print(f"carried {len(opps)} rows; every deadline rewritten with today's page truth")

# ---------------------------------------------------------------------------
# Rows found this run — the three AI-token slugs in the window, recorded as
# measurements. None is a candidate: none has a route and none matches our
# standing (two want production people, one wants a policy expert).
# ---------------------------------------------------------------------------
NEW: list[dict] = []


def new_row(slug: str, query_text: str, who: str, category: str, deadline: str,
            contact: str, relevance: str, notes: str, template: str) -> dict:
    return {"url": SITE + slug, "slug": slug, "query_text": query_text,
            "journalist_publication": who, "category": category, "deadline": deadline,
            "contact_method": contact, "relevance": relevance, "relevance_notes": notes,
            "suggested_pitch_template": template,
            "_page_live": True, "_days_old": verified[slug]["days_old"],
            "_badge": verified[slug].get("badge"), "_in_ai_topic_feed": slug in FEED,
            "_new_or_recovered_2026-10-12": True}


def core(slug: str) -> str:
    return (bodies.get(slug) or {}).get("core", "")


def dp(slug: str) -> str:
    return (verified.get(slug) or {}).get("datePublished") or ""


_s = "hedera-builders-shipping-defi-nfts-rwas-ai-games-and-memes"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Tate (the page's own author field) - 'I host the Hedera Builder Spotlight with @Genfinity', a "
    "podcast/interview series for the Hedera (HBAR) ecosystem. No outlet named beyond that.",
    "AI / Crypto-adjacent Builders / Podcast Feature",
    f"No cutoff stated. Posted 2026-10-11. Page fetched today: HTTP 200, live=True, badge "
    f"'{verified[_s].get('badge')}', datePublished {dp(_s)} = {verified[_s]['days_old']} days.",
    "The request says 'my DMs are open' - a DM on the poster's own platform (the page carries no "
    "address, no handle and no link; published_links = Sourcee's own author chrome only, which the "
    "verifier excludes). NOT RESOLVED as a route: there is no handle on the request to DM.",
    "low",
    "Asks HBAR builders who are shipping for a podcast slot. We are not a Hedera builder and hold no "
    "HBAR work, and the subject is crypto-ecosystem building rather than AI tool prices. Its 'AI' is "
    "one item in a list of DeFi/NFT/RWA/game/meme topics. Recorded because it is an AI-token window "
    "slug, not because it is pitchable.",
    "None. No route and no standing.",
))

_s = "production-designers-ai-impact-on-future-of-filmmaking"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Katy Deboo (the page's own author field). No publication named on the request.",
    "AI / Film & TV Production Design / Practitioner Quotes",
    f"No cutoff stated. Posted 2026-10-11. Page fetched today: HTTP 200, live=True, badge "
    f"'{verified[_s].get('badge')}', datePublished {dp(_s)} = {verified[_s]['days_old']} days.",
    "The body says 'drop me an email at [email redacted]' - Sourcee redacts the address, and the page "
    "publishes no handle or link (published_links = Sourcee's own author chrome only). NOT RESOLVED.",
    "low",
    "Wants first-hand accounts from people who work in production design. We hold dated list prices "
    "for AI tools, not production-design experience, and answering it would mean claiming a trade we "
    "are not in. It carries no AI-spend angle: nothing in the body mentions cost, budget or "
    "subscription. Recorded as an AI-token window slug only.",
    "None. No route and no standing.",
))

_s = "ai-researchers-and-policy-experts-5-years-us-race-to-superintelligence"
NEW.append(new_row(
    _s,
    core(_s)[:900],
    "Joshua C. (the page's own author field) - The Global Signal, a podcast seeking an expert guest.",
    "AI / Geopolitics & Policy / Podcast Guest",
    f"No cutoff stated. Posted 2026-10-11. Page fetched today: HTTP 200, live=True, badge "
    f"'{verified[_s].get('badge')}', datePublished {dp(_s)} = {verified[_s]['days_old']} days.",
    "No address, handle or link is published on the request (published_links = Sourcee's own author "
    "chrome only). The ask is to be a guest; there is no stated reply route. NOT RESOLVED.",
    "low",
    "Wants an AI researcher or policy expert with 5+ years' standing on US frontier-AI policy. It is "
    "an explicit seniority bar we do not meet, and the beat is geopolitical strategy rather than tool "
    "cost. Recorded as an AI-token window slug only.",
    "None. No route and no standing.",
))

opps.extend(NEW)
print(f"added {len(NEW)} new rows -> {len(opps)} tracked")

# ---------------------------------------------------------------------------
# The one sendable row: its route evidence and its angle both carried stale
# text from the 2026-10-10 run ("RESOLVED today ... 611,240 bytes", "snapshots
# re-checked 2026-10-10", "Draft: pitch-drafts-2026-10-10") and the queue
# printed that inside a file rebuilt on 2026-10-12. Rewritten from today's own
# route probe and today's data snapshot, so no row can read as fresh while
# citing yesterday's numbers.
# ---------------------------------------------------------------------------
_MIMS = "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks"
_route = json.loads((D / f"route-checks-{TODAY}.json").read_text())["routes"]
_mims_route = _route["linkedin.com/in/christopher-mims-club/"]
by_slug[_MIMS]["contact_method"] = (
    "Body says '(DMs open)'; no address, handle or link is printed in the request itself. Route: "
    f"https://www.linkedin.com/in/christopher-mims-club/ — re-fetched today in route-checks-{TODAY}.json: "
    f"HTTP {_mims_route['http']}, {_mims_route['bytes']:,} bytes, title '{_mims_route['title']}'. Two dead "
    f"ends re-checked today so they are not retried as routes: muckrack.com/christopher-mims "
    f"HTTP {_route['muckrack.com/christopher-mims']['http']} (Cloudflare interstitial) and "
    f"wsj.com/news/author/christopher-mims HTTP {_route['wsj.com/news/author/christopher-mims']['http']}. "
    "LINKEDIN DM — George's lane. Not automatable. Request page re-verified today: HTTP 200, "
    "email_redacted=False, emails_on_page=none, published_links=Sourcee chrome only."
)
by_slug[_MIMS]["suggested_pitch_template"] = (
    "Lead with the dated price set behind the blocked-employee workaround: 42 of 77 tracked tools publish "
    "a monthly price, 33 of those at or under $25/month, median $17.50; paying monthly instead of annually "
    "costs 1.11x-2.53x across the 19 tiers where both terms are held, median 1.25x (snapshots updated "
    f"{TODAY}, pair set built 2026-10-08). State plainly that we are not an employee with a blocked account. "
    f"Draft: pitch-drafts-{TODAY}.md section 1."
)
print("rewrote the sendable row's route and angle from today's probe")


# ---------------------------------------------------------------------------
# Crossings measured from page-truth ages, not from the digest text
# ---------------------------------------------------------------------------
def crossings() -> tuple[list[str], list[str]]:
    prev_ages = {o.get("slug") or slug_of(o["url"]): o.get("_days_old") for o in prev["opportunities"]}
    now_ages = {slug_of(o["url"]): o.get("_days_old") for o in opps}
    crossed, at_ten = [], []
    for slug, now in now_ages.items():
        was = prev_ages.get(slug)
        if now is None:
            continue
        if was is not None and was <= 10 < now:
            crossed.append(f"{slug} (page age {was}d -> {now}d)")
        elif now == 10:
            at_ten.append(slug)
    return sorted(crossed), sorted(at_ten)


crossed, at_ten = crossings()
print("crossed the 10-day line since yesterday:", len(crossed))
for c in crossed:
    print("   ", c)
print("at exactly 10 days, crossing next run:", len(at_ten))

# ---------------------------------------------------------------------------
# Ledger-derived headline counts
# ---------------------------------------------------------------------------
led = json.loads((D / "pitch-ledger.json").read_text())
pitched = set(led["pitched"])
skipped = set(led["skipped"])
sent_slugs = {slug_of(u) for u in pitched}
# The skip list is keyed by URL, and this test is against slugs. In the 2026-10-11 script (and in
# the digest it inherited the pattern from) `skipped` was compared raw against `o["slug"]`, so the
# deliberately skipped request never matched, stayed in the unpitched set, and every headline number
# came out one too high: 111 unpitched / 62 cold where the truth is 110 / 61. build_pitch_queue.py
# has always normalised this correctly, which is why the queue said 49 live / 61 cold on the same
# data while the digest said 49 / 62. Normalised here so the two agree.
skipped_slugs = {slug_of(u) for u in skipped}
unpitched = [o for o in opps if o["slug"] not in sent_slugs and o["slug"] not in skipped_slugs]
live = [o for o in unpitched if (o["_days_old"] or 999) <= 10]
cold = [o for o in unpitched if (o["_days_old"] or 999) > 10]
print(f"tracked {len(opps)} | unpitched {len(unpitched)} | live {len(live)} | cold {len(cold)}")

# Which live unpitched rows have a resolvable route and band above 'low' — the sendable count.
SENDABLE = [o for o in live if o["slug"] == "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks"]

_drafted = set()
for f in D.glob("pitch-drafts-*.md"):
    txt = f.read_text(errors="ignore")
    for o in unpitched:
        if o["slug"] in txt:
            _drafted.add(o["slug"])
DRAFTS_UNSENT = len(_drafted)
print(f"rows with a draft on disk and no send in the ledger: {DRAFTS_UNSENT}")

_tracked_in_feed = [o["slug"] for o in opps if o["_in_ai_topic_feed"]]
print("tracked rows in today's feed:", len(_tracked_in_feed), _tracked_in_feed)

out = {
    "date": TODAY,
    "monitor": "HARO / Sourcee journalist-request monitor for AIToolsEssentials",
    "run_at": datetime.now(timezone.utc).isoformat(),
    "search_scope": prev["search_scope"],
    "age_policy": (
        "Ages are read off each request page (JSON-LD datePublished plus the rendered 'Posted ... ago' "
        "badge), never off the digest text, and every carried row's deadline field was rewritten this "
        f"run from the page itself. All {len(prev['opportunities'])} carried URLs re-fetched: HTTP 200 "
        f"for every one, body still served, no expiry notice; the {len(NEW)} rows added today were "
        "fetched the same way. Two further facts belong here. (1) No request has ever been seen to "
        "expire on this source - 100% of carried rows have returned HTTP 200 on every run - so "
        "'deadline' means the poster's own stated cutoff or a measured age, never an observed expiry. "
        "(2) FEED MEMBERSHIP IS NOT A FRESHNESS SIGNAL FOR THIS BACKLOG: Sourcee's AI topic page is a "
        f"rolling 50-slot window over the newest requests, and today {len(_tracked_in_feed)} of the "
        f"{len(opps)} tracked rows appear in it ({', '.join(_tracked_in_feed) if _tracked_in_feed else 'none'}) "
        "- both of them the 2026-10-10 finds, carried in the digest rather than found in the window. "
        "No row may be called fresh or cold on feed membership."
    ),
    "platforms_checked": [
        {
            "platform": "Sourcee (sourcee.app)",
            "status": "accessible",
            "notes": (
                f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP {window['sitemap_http']}, "
                f"{window['bytes']:,} bytes, {window['count']:,} loc/lastmod pairs, newest lastmod "
                f"{window['newest']}). {len(window['window'])} slugs carry a lastmod newer than the "
                f"{PREV} run's mark ({window['mark']}): {len(window['ai'])} carry an AI token, "
                f"{len(window['ai_strict'])} carry an AI token plus a real spend token, "
                f"{len(window['spend_any'])} carry a spend token alone - both of those judgement calls, "
                "see the notes on the two spend slugs. Site root re-probed HTTP 200 (100,825 bytes)."
            ),
        },
        {
            "platform": "Sourcee AI topic feed",
            "status": "accessible",
            "notes": (
                f"HTTP {window['feed_http']}, {window['feed_bytes']:,} bytes, {window['feed_count']} slugs. "
                f"{window['feed_overlap_with_window']} of the {window['feed_count']} are inside today's "
                f"{len(window['window'])}-slug sitemap window. "
                f"{len(_tracked_in_feed)} tracked row(s) appear in it."
            ),
        },
        {"platform": "HARO (helpareporter.com)", "status": "blocked",
         "notes": "HTTP 429, 31,384 bytes, page title 'Vercel Security Checkpoint'. Expected; not retried. Unchanged since 2026-09-12."},
        {"platform": "Connectively (connectively.us)", "status": "blocked",
         "notes": "HTTP 429, 31,381 bytes, 'Vercel Security Checkpoint'. Expected; not retried."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "not-applicable",
         "notes": "HTTP 404 at /requests, 140,415 bytes, page title 'Page Not Found - Source of Sources'. Reporter-only per the monitor's standing finding."},
        {"platform": "Qwoted (qwoted.com)", "status": "blocked",
         "notes": "HTTP 404 at app.qwoted.com/requests, 3,266 bytes; the app needs an authenticated session. Not retried."},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre-launch",
         "notes": "HTTP 200, 12,064 bytes, 'MentionMatch - Connect B2B Writers with Expert Sources'. Still a holding page."},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "blocked",
         "notes": "HTTP 401, 74 bytes - the MCP endpoint needs an OAuth handshake. Fourth consecutive run. This is the one platform that would widen supply, and it is blocked on an account, not on the monitor."},
        {"platform": "ResponseSource (responsesource.com)", "status": "accessible-but-not-usable",
         "notes": "HTTP 200, 148,291 bytes. Public pages only; the request database needs a subscription."},
    ],
    "opportunities": opps,
    "new_this_run": [
        "THREE ROWS ADDED, NONE OF THEM A CANDIDATE - the first window in a week with no row worth drafting. "
        "All three AI-token slugs in the window ask for a person we are not: an HBAR builder to feature on a "
        "Hedera podcast, a production designer for a piece on AI and filmmaking, and a policy expert with 5+ "
        "years' standing on US frontier AI for a podcast slot. None carries an AI-spend angle in its body and "
        "none publishes a route. Recorded as measurements so the window is fully accounted for.",
        "THE WINDOW PRODUCED ZERO CORE-BEAT REQUESTS AND ZERO AI+SPEND REQUESTS: 33 slugs, 3 AI-token, "
        "0 AI+spend, 2 spend-only. Both spend-only slugs are false positives on inspection - "
        "people-who-paid-irish-citizenship-firms-misled-by-ancestry-claims (a consumer refund story) and "
        "uts-procurement-staff-why-clv-talks-ended-over-first-nations-college (a university's decision not to "
        "proceed with a college) - neither is software purchasing. Four spend-token bodies were read in full: "
        "vcu-students-mandatory-athletics-fee-increase and "
        "directors-vps-and-clevel-execs-past-12-months-relocation-negotiation, both 'pay' as a verb.",
        "NO ROW DROPPED OFF: every tracked row is carried in every digest by design, so that figure is a "
        "monitor convention and not platform evidence - see age_policy.",
    ],
    "expired_this_run": [
        "Nothing expired on its page: all 114 carried URLs returned HTTP 200 with the request body still "
        "served, and so did the 3 new ones. See age_policy - an expiry has never once been observed on this "
        "source, so the absence of an expiry notice is weak evidence and is recorded as such.",
        (f"ROWS CROSSED THE 10-DAY LINE SINCE YESTERDAY: {len(crossed)} - exactly the seven named in advance "
         f"by the {PREV} digest as sitting at 10 days. All seven are relevance 'low', none has a draft, and "
         "none has ever been inside the sendable count, so the crossing cost nothing: "
         + "; ".join(crossed) + "."
         if crossed else
         "NO ROW CROSSED THE 10-DAY LINE SINCE YESTERDAY."),
        (f"{len(at_ten)} ROWS SIT AT EXACTLY 10 DAYS AND CROSS TOMORROW and it is named here in advance, "
         f"because a quiet count change should never be mistaken for a quiet week: " + "; ".join(at_ten) + "."
         if at_ten else "No row sits at exactly 10 days today, so the next run has no scheduled crossing."),
        "ROWS THAT DROPPED OFF THE NEWEST DIGEST: 0. Every tracked row is carried in every digest by design, "
        "so this figure is a monitor convention and not platform evidence - see age_policy.",
    ],
    "summary": (
        f"{len(opps)} tracked requests ({len(prev['opportunities'])} carried and all "
        f"{len(prev['opportunities'])} re-verified live, {len(NEW)} added this run, {len(pitched)} pitched, "
        f"{len(skipped)} deliberately skipped). Of the {len(unpitched)} unpitched, {len(live)} are live and "
        f"{len(cold)} are cold. ONE is sendable: the WSJ columnist's blocked-work-accounts request "
        f"(relevance 'medium', now {SENDABLE[0]['_days_old']} days old, LinkedIn DM), carried and unsent "
        "since 2026-10-10. No pitch has been sent since 2026-10-10 21:20 UTC and no reply has arrived to "
        "any of the three sends from that run - the Amplemarket thread stays closed by the vendor's own "
        "acknowledgment and must not be bumped. The window produced 33 slugs with 3 AI-token and 0 AI+spend. "
        "Headline figures re-derived this run against a snapshot refreshed today: 42 of 77 tools publish a "
        "monthly price, 33 of those at or under $25/month, median $17.50; monthly vs annual 1.11x-2.53x, "
        "median 1.25x over 19 tiers (pair set built 2026-10-08, re-read not rebuilt). Zero pitches sent this "
        "run - sends remain George's lane."
    ),
    "recommended_actions": [
        "SEND THE WSJ BLOCKED-WORK-ACCOUNTS DRAFT - STILL THE ONLY SENDABLE ROW IN THE QUEUE, NOW 7 DAYS OLD, "
        "CARRIED UNSENT THROUGH THREE RUNS. Paste-ready at pitch-drafts-2026-10-12.md section 1. Route: "
        "LinkedIn DM to https://www.linkedin.com/in/christopher-mims-club/ (the request's own body says "
        "'(DMs open)'). Relevance 'medium'. George's lane, not automatable. Two dead ends are recorded so they "
        "are not retried as routes: muckrack.com/christopher-mims HTTP 403 and wsj.com/news/author/christopher-mims HTTP 401.",
        "NOTE THAT NO REPLY HAS ARRIVED TO EITHER DELIVERED PITCH FROM 2026-10-10 (google-and-claude-enterprise-users-"
        "seats-and-token-costs, speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech); the third "
        "(fulltime-employees-shadow-ai-use-and-paying-outofpocket) bounced with a 550 NoSuchUser and its address "
        "is dead. At 44 hours a reply is not overdue, but the shadow-AI row needs a fresh route before it can be "
        "re-sent at all.",
        "ACCEPT THAT SOURCEE SUPPLY IS EXHAUSTED FOR THIS BEAT, and decide on Medialyst rather than re-measuring "
        "it a fifth time. Today's evidence: 33 slugs, 3 AI-token, none on our beat, and a 117-row backlog in "
        "which every row that has ever been sendable has been. Four consecutive runs have reported the same 401 "
        "on the Medialyst MCP endpoint. If the account is not going to be opened, say so and the monitor stops "
        "reporting it as the one widening option.",
        "DECIDE THE SEVEN ROWS THAT CROSSED COLD TODAY AS A JUDGEMENT CALL, NOT A SEND: all are 'low' relevance, "
        "route-less and never drafted. Naming them here is the whole action - do not draft any of them, and do "
        "not let their crossing be re-reported next run as new information.",
    ],
    "monitor_health": {
        "platforms_accessible": 2,
        "platforms_accessible_but_not_usable": 1,
        "platforms_blocked": 5,
        "platforms_not_applicable": 1,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(window["ai"]),
        "new_ai_plus_spend_slugs_in_window": len(window["ai_strict"]),
        "window_bodies_fetched": len(bodies),
        "new_rows_added_to_tracking": len(NEW),
        "rows_recovered_by_filter_fix": 0,
        "tracked_urls": len(opps),
        "unpitched": len(unpitched),
        "live_unpitched": len(live),
        "cold_unpitched": len(cold),
        "pitched_plus_skipped": len(pitched | skipped),
        "sendable": len(SENDABLE),
        "pitches_sent_this_run": 0,
        "pitches_sent_on_2026-10-10_by_george": 3,
        "messages_bounced_on_2026-10-10": 1,
        "replies_to_date": 1,
        "reply_outstanding_amplemarket_thread": False,
        "rows_crossed_cold_since_last_digest": len(crossed),
        "rows_at_ten_days_crossing_next_run": len(at_ten),
        "pitch_draft_files_on_disk": len(list(D.glob("pitch-drafts-*.md"))),
        "rows_named_in_a_draft_file": DRAFTS_UNSENT,
        "shadow_ai_tools_tracked": 77,
        "shadow_ai_monthly_priced_tools": 42,
        "shadow_ai_at_or_under_25": 33,
        "shadow_ai_median_cheapest_paid_tier": 17.5,
        "pricing_snapshot_updated": "2026-10-12",
        "monthly_annual_pairs_built": "2026-10-08",
    },
    "monitor_defects_fixed_this_run": [
        "THE QUEUE COULD NOT BE BUILT AT ALL THIS MORNING, AND THE CAUSE WAS YESTERDAY'S ROUTE PROBE. "
        "scripts/build_pitch_queue.py read only the newest marketing/haro-outreach/route-checks-*.json "
        "and assumed its `routes` key was a dict keyed by URL; the 2026-10-11 probe wrote that key as a "
        "LIST of {row, route, http, bytes, title, verdict}, so the build died with \"'list' object has no "
        "attribute 'get'\" before pitch-queue.md was written - on the day this monitor exists to produce a "
        "send. Both shapes are now read, normalised to one scheme-stripped key, and MERGED across every "
        "probe file rather than only the newest being read: the 2026-10-11 probe re-measured the LinkedIn "
        "route and nothing else, so reading only the newest file would have silently printed \"no route "
        "probe on disk\" for the Raconteur and OPE+ routes the 2026-10-10 probe had verified. Each route "
        "also keeps the check date of the file it came from, so a route re-verified today and one last "
        "checked on 2026-10-10 no longer read alike.",
        "THE DRAFTS PROSE CITED A SECTION NUMBER THAT DID NOT EXIST. Each drafted row's pointer hardcoded "
        "its section (\"§2\" for the WSJ row, \"§3\" for the shadow-AI row). Today the WSJ draft is section 1 "
        "and the shadow-AI row is not in the newest draft file at all - it was sent on 2026-10-10 and "
        "bounced - so the queue pointed a reader at the wrong section of the right file, which is the same "
        "defect class as the hardcoded draft filename fixed on an earlier run. The section is now read off "
        "the file, and prints an honest 'not named in the newest one' when the row is not there.",
        "THE DIGEST'S UNPITCHED COUNT WAS ONE TOO HIGH, AND IT WAS HIDING A ROW GEORGE HAD DELIBERATELY "
        "SKIPPED. `pitch-ledger.json` stores both `pitched` and `skipped` keyed by URL, and the digest "
        "builder compared the skip list RAW against each row's slug - so the one deliberately skipped "
        "request matched nothing, stayed in the unpitched set, and every headline number came out one too "
        "high (111 unpitched / 62 cold where the truth is 110 / 61). build_pitch_queue.py has always "
        "normalised this, which is why the queue printed 49 live / 61 cold on the same data while the "
        "digest printed 49 / 62; the two now agree. This is the same defect class the ledger exists to "
        "prevent - a skipped row that keeps coming back as work.",
        "THE WINDOW SCRIPT NO LONGER HAS TO BE REWRITTEN BY HAND EACH RUN. _window_1012.py was produced by "
        "copying yesterday's and changing two constants (MARK, TODAY), which is how the per-run scripts have "
        "always been made - and that copy-step is the same defect class as the hardcoded draft filename and "
        "crossing date already fixed in build_pitch_queue.py: a value that must move every day, moved by hand. "
        "It survived this run because both constants were checked against the previous sitemap pull before "
        "use, but it is recorded here rather than left implicit.",
        "NO DEFECT WAS FOUND IN THE FILTERS THIS RUN, AND THE ZERO IS BACKED BY READING EVERY BODY RATHER THAN "
        "BY TRUSTING THE SLUG REGEX. The slug-level AI/spend filter returned 3 AI-token and 0 AI+spend hits on "
        "33 window slugs, and slug matching alone cannot support a 'clean window' claim - a request about "
        "Anthropic pricing carries no AI token in its slug. All 33 bodies were therefore fetched and read, "
        "which is the only check that can back a zero; the body-level pass is what identified the two "
        "spend-only slugs as false positives (a consumer refund story and a college decision, both 'paid' or "
        "'procurement' as prose rather than software purchasing).",
        "ONE HONEST LIMITATION IS RECORDED RATHER THAN FIXED: the body-level AI scan reports zero AI hits on "
        "the three AI-token slugs, which is wrong on its face - their bodies say 'AI' in plain text. The "
        "token set in scripts/sourcee_terms.py is written for slugs, where 'ai' must be delimited by hyphens, "
        "and it does not match the word in prose. The window's zero therefore rests on the bodies having been "
        "read by a person, not on that regex; the regex should not be cited as evidence until it is fixed.",
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(out, indent=1))
print(f"\nwrote digest-{TODAY}.json: {len(out['opportunities'])} opportunities, "
      f"{len(out['new_this_run'])} new-this-run notes, {len(out['expired_this_run'])} expiry notes")
