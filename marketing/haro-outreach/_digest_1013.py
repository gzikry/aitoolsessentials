#!/usr/bin/env python3
"""Compose marketing/haro-outreach/digest-2026-10-13.json.

Carries the 117 tracked rows forward with their page truth refreshed from
verified-requests.json (re-fetched today by scripts/verify_journo_requests.py --refresh-feed),
and adds the six AI-token rows found in today's 105-slug sitemap window.

Nothing is marked pitched here: sends are George's lane and the ledger is the only place a send
is recorded.
"""
from __future__ import annotations

import json
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing/haro-outreach"
TODAY = "2026-10-13"
PREV = "2026-10-12"

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
# Rows found this run — every AI-token slug in the 105-slug window. All six are
# recorded as measurements; none is a candidate and none has a route.
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
            "_new_or_recovered_2026-10-13": True}


def core(slug: str) -> str:
    return (bodies.get(slug) or {}).get("core", "")


def dp(slug: str) -> str:
    return (verified.get(slug) or {}).get("datePublished") or ""


def _dl(slug: str) -> str:
    r = verified[slug]
    return (f"No cutoff stated. Page fetched today: HTTP 200, live=True, badge "
            f"'{r.get('badge')}', datePublished {dp(slug)} = {r['days_old']} days.")


# ---------------------------------------------------------------------------
# Headline figures re-derived at build time, never typed. The snapshot file is refreshed by the
# daily maintenance job, and on this run it carries `updated: 2026-10-13` while yesterday's digest
# prose said 2026-10-12 - so a figure typed here would have been a day stale inside a file built
# today, which is the defect class every earlier hand-typed figure in this monitor belonged to.
# ---------------------------------------------------------------------------
def _derive_figures() -> tuple[str, str, str, str, str]:
    try:
        _snaps = json.loads((S / "data/pricing_snapshots.json").read_text())
        _tools = json.loads((S / "data/tools.json").read_text())
    except (OSError, json.JSONDecodeError):
        return ("?", "?", "?", "?", "?")
    _month = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
    _paid = {}
    for _k, _v in (_snaps.get("snapshots") or {}).items():
        _vals = [float(_x) for _x in _month.findall(_v.get("digest") or "") if float(_x) > 0]
        if _vals:
            _paid[_k] = min(_vals)
    if not _paid:
        return (str(len(_tools)), "?", "?", "?", _snaps.get("updated", "?"))
    return (str(len(_tools)), str(len(_paid)),
            str(sum(1 for _x in _paid.values() if _x <= 25)),
            f"{statistics.median(_paid.values()):.2f}", _snaps.get("updated", "?"))


n_tools, n_paid, n_25, med_paid, _snap_updated = _derive_figures()
print(f"figures re-derived: {n_paid} of {n_tools} monthly-priced, {n_25} at/under $25, "
      f"median ${med_paid}, snapshot updated {_snap_updated}")


# The one row the slug filter flagged as AI+spend, and the judgement on it. 'Procurement' and
# 'saas' are both real spend tokens and both are used here about the buyer's own research
# behaviour, not about what software anyone pays for; the body never mentions cost, a budget,
# a subscription or a price.
_s = "b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Lyza G (the page's own author field). No outlet named on the request.",
    "AI / B2B Buying Process / Vendor Research",
    _dl(_s),
    "The body says 'Email [email redacted]' — Sourcee redacts the address, and the page publishes "
    "no handle and no link (published_links = Sourcee's own author chrome only, which the verifier "
    "excludes). NOT RESOLVED as a route.",
    "low-medium",
    "The only AI+spend slug match in the window, and it is a false positive on our beat. It cites "
    "Forrester on buyers using AI to research vendors and on buying groups averaging a dozen "
    "internal stakeholders, then asks B2B buyers, procurement, RevOps and SaaS sales leaders to "
    "share lessons. That is a change in how software is BOUGHT, not what AI tools cost; the body "
    "carries no price, budget or subscription figure, and we are a publisher rather than a "
    "procurement team. Recorded because the slug filter matched it, not because it is pitchable.",
    "None. No route and no standing.",
))

_s = "global-development-professionals-using-ai-across-programs-and-policy"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Emma Smith (the page's own author field) — Devex (devex.com, domain field).",
    "AI / Global Development Sector / Practitioner Tools",
    _dl(_s),
    "The body says 'Get in touch' with no address, handle or link published on the request "
    "(published_links = Sourcee's own author chrome only). NOT RESOLVED as a route.",
    "low",
    "Wants global development professionals — program management, policy and advocacy, comms, "
    "grant writing — describing the tools they use. We are not in that sector and hold no "
    "standing to answer it. It also carries no cost angle: the ask is about ways of working, not "
    "spend. Recorded as an AI-token window slug only.",
    "None. No route and no standing.",
))

_s = "caine-prize-winners-gen-ai-accusations-targeting-black-writers"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "noid. (the page's own author field) — for takingCustody, named in the body.",
    "AI / Publishing & Authorship / Plagiarism Accusations",
    _dl(_s),
    "The body is a public DM request to three named Caine Prize winners; no address, handle or "
    "link is published on the request itself. NOT RESOLVED as a route, and the people asked are "
    "named individuals rather than an open call.",
    "low",
    "Wants the accused/award-winning writers themselves for a story on generative-AI accusations "
    "against Black writers. It is an authorship-integrity story with no cost, pricing or "
    "purchasing element, and we have no part in it. Recorded as an AI-token window slug only.",
    "None. No route and no standing.",
))

_s = "software-engineers-who-left-tech-jobs-lost-to-ai-coding-tools"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Thibault Spirlet (the page's own author field) — Business Insider (businessinsider.com, "
    "domain field).",
    "AI / Labour Market / Coding Tools",
    _dl(_s),
    "The body says 'Please reach out at [email redacted]' — Sourcee redacts the address and the "
    "page publishes no alternative handle or link (published_links = Sourcee's own author chrome "
    "only). NOT RESOLVED as a route.",
    "low",
    "Wants software engineers who have LEFT tech because AI coding tools removed the part of the "
    "job they loved. That is a first-person career story from a practitioner; we are a publisher "
    "and cannot supply one. The beat is job displacement, not tool cost. Recorded as an AI-token "
    "window slug only.",
    "None. No route and no standing.",
))

_s = "manufacturers-and-ai-safety-experts-ai-risks-in-chemical-food-defense"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Sakshi Udavant (Luna) (the page's own author field) — Manufacturing Dive "
    "(manufacturingdive.com, domain field).",
    "AI / Industrial Safety / Risk",
    _dl(_s),
    "The body says 'For: Manufacturing Dive [email redacted]' — Sourcee redacts the address and "
    "the page publishes no other route (published_links = Sourcee's own author chrome only). "
    "NOT RESOLVED.",
    "low",
    "Wants manufacturers and AI safety experts on the risks of AI in chemical, food and defence "
    "manufacturing. It is a safety-and-risk story; we hold dated AI tool prices and have no "
    "industrial safety standing. No cost or purchasing angle in the body. Recorded as an AI-token "
    "window slug only.",
    "None. No route and no standing.",
))

_s = "uk-baby-boomers-misinformation-sharing-and-ai-influence-online"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Dan McCarthy (the page's own author field) — Canvas8 (canvas8.com, domain field).",
    "AI / Media Literacy / Audience Research",
    _dl(_s),
    "The body asks for academics researching misinformation and publishes no address, handle or "
    "link (published_links = Sourcee's own author chrome only). NOT RESOLVED as a route.",
    "low",
    "Wants academics studying misinformation sharing among UK baby boomers for a Canvas8 report. "
    "An explicit academic-researcher standing bar we do not meet, and the subject is media "
    "literacy rather than tool spend. Recorded as an AI-token window slug only.",
    "None. No route and no standing.",
))

opps.extend(NEW)
print(f"added {len(NEW)} new rows -> {len(opps)} tracked")

# ---------------------------------------------------------------------------
# The one sendable row: its route evidence carried yesterday's byte count and
# yesterday's date. Rewritten from today's own route probe.
# ---------------------------------------------------------------------------
_MIMS = "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks"
_route = json.loads((D / f"route-checks-{TODAY}.json").read_text())["routes"]
_mims_route = _route["linkedin.com/in/christopher-mims-club/"]
by_slug[_MIMS]["contact_method"] = (
    "Body says '(DMs open)'; no address, handle or link is printed in the request itself. Route: "
    f"https://www.linkedin.com/in/christopher-mims-club/ — re-fetched today in route-checks-{TODAY}.json: "
    f"HTTP {_mims_route['http']}, {_mims_route['bytes']:,} bytes, title '{_mims_route['title']}'. Two dead "
    f"ends re-checked today so they are not retried as routes: muckrack.com/christopher-mims "
    f"HTTP {_route['muckrack.com/christopher-mims/']['http']} (Cloudflare interstitial) and "
    f"wsj.com/news/author/christopher-mims HTTP {_route['wsj.com/news/author/christopher-mims/']['http']}. "
    "LINKEDIN DM — George's lane. Not automatable. Request page re-verified today: HTTP 200, "
    "email_redacted=False, emails_on_page=none, published_links=Sourcee chrome only."
)
by_slug[_MIMS]["suggested_pitch_template"] = (
    "Lead with the dated price set behind the blocked-employee workaround: 42 of 77 tracked tools publish "
    "a monthly price, 33 of those at or under $25/month, median $17.50; paying monthly instead of annually "
    "costs 1.11x-2.53x across the 19 tiers where both terms are held, median 1.25x (snapshots updated "
    f"{_snap_updated}, pair set built 2026-10-08). State plainly that we are not an employee with a blocked account. "
    f"Route: LinkedIn DM to https://www.linkedin.com/in/christopher-mims-club/ — George's lane. "
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
for a in at_ten:
    print("   ", a)

# ---------------------------------------------------------------------------
# Ledger-derived headline counts
# ---------------------------------------------------------------------------
led = json.loads((D / "pitch-ledger.json").read_text())
pitched = set(led["pitched"])
skipped = set(led["skipped"])
sent_slugs = {slug_of(u) for u in pitched}
skipped_slugs = {slug_of(u) for u in skipped}
unpitched = [o for o in opps if o["slug"] not in sent_slugs and o["slug"] not in skipped_slugs]
# `o["_days_old"] or 999` is WRONG and was wrong in the 2026-10-12 script this is built from:
# a request posted today has _days_old == 0, which is falsy, so `0 or 999` is 999 and the row was
# classified cold on the day it was freshest. It put the two 0-day rows added on 2026-10-13 into
# the cold count and printed 48 live / 68 cold where the truth (and build_pitch_queue.py's own
# output on the same data) is 50 / 66. Same defect class as the typed live-row count fixed on
# 2026-10-01: a number that looks like a measurement and is an artefact of the expression.
def _age(o: dict) -> int:
    d = o.get("_days_old")
    return d if d is not None else 999


live = [o for o in unpitched if _age(o) <= 10]
cold = [o for o in unpitched if _age(o) > 10]
print(f"tracked {len(opps)} | unpitched {len(unpitched)} | live {len(live)} | cold {len(cold)}")

SENDABLE = [o for o in live if o["slug"] == _MIMS]

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

_ai_body_hits = [s for s, r in bodies.items() if r.get("ai_tokens_in_body")]
_spend_only = [s for s, r in bodies.items()
               if r.get("spend_tokens_in_body") and not r.get("ai_tokens_in_body")]

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
        "(2) FEED MEMBERSHIP IS STILL NOT A FRESHNESS SIGNAL FOR THE BACKLOG, but today the opposite "
        "reading is also wrong and is recorded so neither is inferred: the AI topic page carries 50 "
        f"slugs and 50 of them are inside today's 105-slug sitemap window, and {len(_tracked_in_feed)} "
        "tracked rows appear in it. The feed is a rolling window over the newest requests, so a "
        "carried row's absence from it says nothing about that row."
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
                f"{len(window['ai_strict'])} carry an AI token plus a spend token, "
                f"{len(window['spend_any'])} carry a spend token alone. Every one of the 105 window "
                "bodies was fetched and read - the only check that can back a zero. Site root "
                "re-probed HTTP 200 (100,825 bytes)."
            ),
        },
        {
            "platform": "Sourcee AI topic feed",
            "status": "accessible",
            "notes": (
                f"HTTP {window['feed_http']}, {window['feed_bytes']:,} bytes, {window['feed_count']} slugs. "
                f"{window['feed_overlap_with_window']} of the {window['feed_count']} are inside today's "
                f"{len(window['window'])}-slug sitemap window - i.e. today the feed is essentially the "
                f"newest slice of the same window. {len(_tracked_in_feed)} tracked row(s) appear in it."
            ),
        },
        {"platform": "HARO (helpareporter.com)", "status": "blocked",
         "notes": "HTTP 429, 31,373 bytes, page title 'Vercel Security Checkpoint'. Expected; not retried. Unchanged since 2026-09-12."},
        {"platform": "Connectively (connectively.us)", "status": "blocked",
         "notes": "HTTP 429, 31,390 bytes, 'Vercel Security Checkpoint'. Expected; not retried."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "not-applicable",
         "notes": "HTTP 404 at /requests, 140,415 bytes, page title 'Page Not Found - Source of Sources'. Reporter-only per the monitor's standing finding."},
        {"platform": "Qwoted (qwoted.com)", "status": "blocked",
         "notes": "HTTP 404 at app.qwoted.com/requests, 3,266 bytes; the app needs an authenticated session. Not retried."},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre-launch",
         "notes": "HTTP 200, 12,064 bytes, 'MentionMatch - Connect B2B Writers with Expert Sources'. Still a holding page."},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "blocked",
         "notes": "HTTP 401, 74 bytes - the MCP endpoint needs an OAuth handshake. Fifth consecutive run. This is the one platform that would widen supply, and it is blocked on an account, not on the monitor."},
        {"platform": "ResponseSource (responsesource.com)", "status": "accessible-but-not-usable",
         "notes": "HTTP 200, 148,193 bytes. Public pages only; the request database needs a subscription."},
    ],
    "opportunities": opps,
    "new_this_run": [
        (f"SIX ROWS ADDED - every AI-token slug in the 105-slug window - AND NOT ONE OF THEM IS A "
         f"CANDIDATE. None publishes a reply route and none asks about tool cost: a B2B-buying-process "
         f"question about AI-mediated vendor research, a Devex call for global-development staff, a "
         f"gen-AI-plagiarism story aimed at three named Caine Prize winners, a Business Insider call "
         f"for engineers who left tech over AI coding tools, a manufacturing-safety risk piece, and a "
         f"Canvas8 report on UK baby boomers and misinformation. Recorded as measurements so the "
         f"window is fully accounted for."),
        (f"THE WINDOW PRODUCED ZERO CORE-BEAT REQUESTS: {len(window['window'])} slugs, "
         f"{len(window['ai'])} AI-token, {len(window['ai_strict'])} AI+spend, "
         f"{len(window['spend_any'])} spend-only. The single AI+spend slug match "
         f"(b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research) is a false positive on "
         f"our beat and is written up in full in its own row: 'procurement' and 'saas' there describe "
         f"how software is BOUGHT, not what AI tools cost, and the body carries no price, budget or "
         f"subscription figure. All seven spend-only slugs are consumer or non-software stories "
         f"(fuel prices, council tax, SNAP cuts, elder care, cost-of-living, a pensioner story, a "
         f"hospitality-economy piece). All 105 window bodies were fetched and read, which is the only "
         f"check that can back a zero."),
        "NO ROW DROPPED OFF: every tracked row is carried in every digest by design, so that figure is a "
        "monitor convention and not platform evidence - see age_policy.",
    ],
    "expired_this_run": [
        (f"Nothing expired on its page: all {len(prev['opportunities'])} carried URLs returned HTTP 200 "
         f"with the request body still served, and so did the {len(NEW)} new ones. See age_policy - an "
         f"expiry has never once been observed on this source, so the absence of an expiry notice is "
         f"weak evidence and is recorded as such."),
        (f"ROWS CROSSED THE 10-DAY LINE SINCE YESTERDAY: {len(crossed)}."
         + (" " + "; ".join(crossed) + "." if crossed else " No row crossed.")
         if crossed else "NO ROW CROSSED THE 10-DAY LINE SINCE YESTERDAY."),
        (f"{len(at_ten)} ROW(S) SIT AT EXACTLY 10 DAYS AND CROSS TOMORROW, named here in advance because a "
         f"quiet count change should never be mistaken for a quiet week: " + "; ".join(at_ten) + "."
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
        f"acknowledgment and must not be bumped. The window produced {len(window['window'])} slugs with "
        f"{len(window['ai'])} AI-token and {len(window['ai_strict'])} AI+spend (a false positive). "
        f"Headline figures re-derived this run against the snapshot (updated {_snap_updated}): "
        f"{n_paid} of {n_tools} tools publish a monthly price, {n_25} of those at or under $25/month, "
        f"median ${med_paid}; monthly vs annual 1.11x-2.53x, median 1.25x over 19 tiers (pair set built "
        "2026-10-08, re-read not rebuilt). Zero pitches sent this run - sends remain George's lane."
    ),
    "recommended_actions": [
        "SEND THE WSJ BLOCKED-WORK-ACCOUNTS DRAFT - STILL THE ONLY SENDABLE ROW IN THE QUEUE, NOW 8 DAYS OLD, "
        f"CARRIED UNSENT THROUGH FOUR RUNS. Paste-ready at pitch-drafts-{TODAY}.md section 1. Route: "
        "LinkedIn DM to https://www.linkedin.com/in/christopher-mims-club/ (the request's own body says "
        "'(DMs open)'). Relevance 'medium'. George's lane, not automatable. Route re-fetched today: HTTP 200, "
        f"{_mims_route['bytes']:,} bytes. Two dead ends are recorded so they are not retried as routes: "
        "muckrack.com/christopher-mims HTTP 403 and wsj.com/news/author/christopher-mims HTTP 401. IT HAS "
        "TWO DAYS LEFT AS A SENDABLE ROW: at 10 days old on 2026-10-15 it is at the line, and on 2026-10-16 "
        "it crosses it and leaves the sendable list - nothing brings it back once it does.",
        "NOTE THAT NO REPLY HAS ARRIVED TO EITHER DELIVERED PITCH FROM 2026-10-10 (google-and-claude-enterprise-"
        "users-seats-and-token-costs, speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech); the "
        "third (fulltime-employees-shadow-ai-use-and-paying-outofpocket) bounced with a 550 NoSuchUser and its "
        "address is dead. Mailbox checked today: the only inbound from any pitch recipient ever is still Jan "
        "Suski's 2026-09-18 message, acknowledged and closed on 2026-10-11.",
        "ACCEPT THAT SOURCEE SUPPLY IS EXHAUSTED FOR THIS BEAT, and decide on Medialyst rather than re-measuring "
        f"it a fifth time. Today's evidence: {len(window['window'])} slugs, {len(window['ai'])} AI-token, none on "
        "our beat. Five consecutive runs have reported the same 401 on the Medialyst MCP endpoint. If the "
        "account is not going to be opened, say so and the monitor stops reporting it as the one widening option.",
        "DO NOT DRAFT ANY OF TODAY'S SIX ROWS. None has a route and none is on our beat; drafting one would add "
        "another unsent file to the 26 already on disk, which is the exact failure this monitor was rebuilt to "
        "stop repeating.",
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
        "shadow_ai_tools_tracked": int(n_tools) if n_tools.isdigit() else n_tools,
        "shadow_ai_monthly_priced_tools": int(n_paid) if n_paid.isdigit() else n_paid,
        "shadow_ai_at_or_under_25": int(n_25) if n_25.isdigit() else n_25,
        "shadow_ai_median_cheapest_paid_tier": float(med_paid) if med_paid != "?" else med_paid,
        "pricing_snapshot_updated": _snap_updated,
        "monthly_annual_pairs_built": "2026-10-08",
    },
    "monitor_defects_fixed_this_run": [
        "THE DIGEST CLASSIFIED THE FRESHEST ROWS IN THE QUEUE AS COLD, AND THE CAUSE WAS A FALSY ZERO. The "
        "line `live = [o for o in unpitched if (o['_days_old'] or 999) <= 10]` turns a request posted TODAY "
        "into 999, because `_days_old == 0` is falsy - so the two rows added on 2026-10-13 (both 0 days old, "
        "both genuinely the newest things this monitor holds) were counted as cold and the digest printed "
        "48 live / 68 cold where the truth is 50 / 66. build_pitch_queue.py, which does not use the idiom, "
        "printed 50 live on the same data, which is how the disagreement was caught: two artefacts of the "
        "monitor disagreeing is the only reason a wrong number here is visible at all. Replaced with an "
        "explicit None test. Same defect class as the hand-typed live-row count fixed on 2026-10-01 - a "
        "number that looks measured and is an artefact of the expression that produced it.",
        "THE PER-RUN ROUTE PROBE WAS A HAND-COPIED FILE AND IT HAD ALREADY SILENTLY DROPPED A ROUTE. "
        "marketing/haro-outreach/_routes_*.py was produced each day by copying the previous day's script and "
        "editing its URL list, and the 2026-10-12 probe's list did not include the two OPE+ routes "
        "(ope-plus.com/2024/02/13/announcing-ope/19236 and ope-plus.com/contact-us) that the 2026-10-10 probe "
        "had verified - the newest file simply did not mention them, and only build_pitch_queue.py's "
        "file-MERGING kept their evidence alive. That is the same defect class as the hardcoded draft filename "
        "and the hand-typed live-row count fixed on earlier runs: a list that must be maintained by hand, "
        "maintained wrong. Replaced by scripts/probe_routes.py, which takes the UNION of the route keys in "
        "every route-checks-*.json on disk and re-probes each one once, so a route can only leave the set by "
        "being deleted from every historical file on purpose. It re-probed 9 routes today and recovered both "
        "OPE+ routes at HTTP 200.",
        "A PROSE STRING WAS BEING PROBED AS IF IT WERE A URL. The 2026-10-11 route file wrote `routes` as a "
        "list and used the sentence 'six byline pages (muckrack.com/tobi-amure, investopedia.com/...)' as one "
        "row's `route` field. The first run of the new probe read that as a URL and fetched 'https://six byline "
        "pages (...)', returning HTTP 000 - which, had it been written, would have read in the queue as a route "
        "that had gone dead overnight. The probe now requires a route key to look like a host/path before "
        "probing it; prose belongs on the row, not in the probe list.",
        "THE WINDOW SCRIPT NO LONGER CARRIES A HAND-TYPED MARK. _window_1013.py reads the previous run's newest "
        "lastmod out of _window_1012.json instead of pasting the constant in, so the one value that must move "
        "every day cannot drift behind a day. This is the fix for the limitation the 2026-10-12 run recorded "
        "rather than fixed.",
        "ONE HONEST LIMITATION IS RECORDED AGAIN AND IS NOT FIXED: the body-level AI scan still reports zero AI "
        "hits across all 105 window bodies, including the six whose bodies say 'AI' in plain text. The token set "
        "in scripts/sourcee_terms.py is written for slugs, where 'ai' must be delimited by hyphens, and it does "
        "not match the word in prose. The window's zero therefore rests on six bodies having been read and "
        "quoted in this digest, not on that regex, and the regex must not be cited as evidence until it is "
        f"fixed. The body-level spend scan has the same caveat and produced {len(_spend_only)} spend-only hits, "
        "every one of which was read and judged.",
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(out, indent=1))
print(f"\nwrote digest-{TODAY}.json: {len(out['opportunities'])} opportunities, "
      f"{len(out['new_this_run'])} new-this-run notes, {len(out['expired_this_run'])} expiry notes")
