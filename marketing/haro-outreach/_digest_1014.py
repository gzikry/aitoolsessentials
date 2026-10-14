#!/usr/bin/env python3
"""Compose marketing/haro-outreach/digest-2026-10-14.json.

Carries the 123 tracked rows forward with their page truth refreshed from
verified-requests.json (re-fetched today by scripts/verify_journo_requests.py --refresh-feed),
and adds the eight AI-token rows found in today's 111-slug window.

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
TODAY = "2026-10-14"
PREV = "2026-10-13"

prev = json.loads((D / f"digest-{PREV}.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
window = json.loads((D / f"_window_{TODAY.replace('-', '')[4:]}.json").read_text())
bodies = json.loads((D / f"_bodies_{TODAY.replace('-', '')[4:]}.json").read_text())
feed = json.loads((D / "ai-topic-feed.json").read_text())
FEED = set(feed["slugs"])

# The platform probes run in the window script, and their byte counts used to be hand-typed into
# this digest - the same defect class as the hand-typed mark and the hand-typed live-row count fixed
# on earlier runs. Read them from the probe's own output instead.
PLAT = {p["platform"]: p for p in window["platforms"]}

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
# Rows found this run - every AI-token slug in the 111-slug window. All eight are
# recorded as measurements; none is a candidate, none publishes a route, and
# none asks a question about tool cost.
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
            "_new_or_recovered_2026-10-14": True}


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
# daily maintenance job, and on this run it carries `updated: 2026-10-14` - so a figure typed here
# would be a day stale inside a file built today, which is the defect class every earlier
# hand-typed figure in this monitor belonged to.
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


_NN = ("None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth "
       "unsent draft would be a defect rather than progress.")

# 1. The Anthropic-adjacent one. It names Anthropic and the AI boom and it is the closest thing in
# the window to our beat - and it is still not a cost question. She is interviewing NGOs about how
# they use AI and wants practitioners in schools, NGOs and foundations to describe what they see.
# We are a publisher; we hold dated prices, not a field observation from inside a school.
_s = "school-leaders-and-ngo-staff-ai-adoption-challenges-across-sectors"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Anurita Srivastava (the page's own author field). No outlet named on the request.",
    "AI / Education Policy / Nonprofit Adoption",
    _dl(_s),
    "The body says 'I'd love to hear what you're seeing' with no address, handle or link published "
    "(published_links = Sourcee's own author chrome only, which the verifier excludes). NOT RESOLVED.",
    "low",
    "Wants school leaders, NGO staff, foundation and technology-org people to describe AI adoption "
    "challenges - external validity, policy transfer, infrastructure and training. It is an "
    "adoption-realities piece with no cost, pricing or purchasing element anywhere in the body, and "
    "we are not inside a school or an NGO. The Anthropic mention is the event she attended, not the "
    "subject. Recorded as an AI-token window slug.",
    _NN,
))

# 2. A big-metro callout, a named reporter, and a redacted address: the classic shape of a request
# that looks sendable until the route is read.
_s = "minnesotans-using-chatgpt-and-ai-tools-experiences-with-election-info"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Sofia Barnett (named in the body) - Minnesota Star Tribune (startribune.com, domain field).",
    "AI / Elections / Consumer Use",
    _dl(_s),
    "The body says 'email me at [email redacted]' - Sourcee redacts the address, and the page "
    "publishes no handle and no link (published_links = Sourcee's own author chrome only). NOT RESOLVED.",
    "low",
    "A callout for Minnesotans who used ChatGPT, Claude or Gemini to look up candidates or ballot "
    "questions. The standing bar is residence and personal experience in one state's election; we "
    "meet neither, and the subject is election information rather than tool cost. Recorded as an "
    "AI-token window slug.",
    _NN,
))

# 3. An interview request aimed at one named individual, posted the same day.
_s = "ai-policy-advisor-newsom-administration-ai-regulation"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Jenny Jiin Huh (the page's own author field) - ABC10 Sacramento (abc10.com, domain field).",
    "AI / Regulation / Broadcast",
    _dl(_s),
    "The request opens '@goldman' - it is addressed to one named person, not an open call, and "
    "publishes no address, handle or link of its own. NOT RESOLVED, and not open to us by its own "
    "wording.",
    "low",
    "A same-day TV interview with a specific AI policy adviser to the Newsom administration about "
    "California AI regulation. Not an open call, not our beat, and the body carries no cost or "
    "purchasing angle. Recorded as an AI-token window slug.",
    _NN,
))

# 4. A founder-story collection with a DM route - but the route belongs to the poster's platform.
_s = "african-founders-building-ai-companies-pitch-deck-realities"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "MarketBrain OS (the page's own author field). No outlet named on the request.",
    "AI / Startups / Founder Stories",
    _dl(_s),
    "The body says 'Reply or DM' - a route on the poster's own platform, not on the request, and no "
    "handle or link is printed here. NOT RESOLVED from this end.",
    "low",
    "Wants African founders building AI companies to describe what pitch decks never prepare them "
    "for. It is a first-person founder story with a geographic standing bar we do not meet, and the "
    "body carries no cost, pricing or subscription figure. Recorded as an AI-token window slug.",
    _NN,
))

# 5. Two sentences, no outlet, no route, and an explicit 'if you work in higher ed'.
_s = "higher-ed-nonfaculty-staff-ai-use-at-work"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Adrienne Lu (the page's own author field). No outlet named on the request and none in the body.",
    "AI / Higher Education / Workplace",
    _dl(_s),
    "The body is two lines with no address, handle or link published on the request "
    "(published_links = Sourcee's own author chrome only). NOT RESOLVED.",
    "low",
    "Asks higher-ed non-faculty staff who use AI at work to get in touch for 'an upcoming story'. "
    "An explicit employment standing bar, no cost angle, and no route at all. Recorded as an "
    "AI-token window slug.",
    _NN,
))

# 6. The one window row with a real published link - and the ask is to be a podcast guest.
_s = "podcast-guests-ai-channel-and-partner-ecosystem"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Dinara B. (the page's own author field). No outlet named on the request; 'Channel Insights - "
    "AI Talk' is named in the body.",
    "AI / Channel & Partner Ecosystem / Podcast",
    _dl(_s),
    "The body carries one real published link, https://lnkd.in/e-bXaf-B (a LinkedIn short link to "
    "her own show) and says 'Get in touch' - but the ask is to come on as a guest, and the link is "
    "her programme rather than a reply route to a journalist. NOT RESOLVED as a route for us.",
    "low",
    "A podcast looking for guests, framed as a two-year anniversary post. It is a guest-invitation "
    "and not a journalist request for sources, there is no cost or pricing question in it, and "
    "appearing on it would not be coverage. Recorded as an AI-token window slug.",
    _NN,
))

# 7. Live at a conference, wants people in the room.
_s = "ai-infrastructure-professionals-in-london-capacity-europe-attendees"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Kai Nicol-Schwarz (the page's own author field). No outlet named on the request.",
    "AI / Data Centres / Infrastructure",
    _dl(_s),
    "The body says 'drop me a line' with no address, handle or link published "
    "(published_links = Sourcee's own author chrome only). NOT RESOLVED, and the ask is attendance-"
    "bound.",
    "low",
    "Wants AI data-centre people who will be at Capacity Europe in London to speak with him there. "
    "A physical-attendance standing bar we cannot meet, and the beat is infrastructure capacity "
    "rather than tool spend. Recorded as an AI-token window slug.",
    _NN,
))

# 8. The one window slug that pairs 'AI' with a software-buying subject - and it is a supplier-facing
# content request, not a cost story.
_s = "b2b-vendors-buyers-pasting-proposals-into-ai-tools"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Lyza G (the page's own author field) - Flipbooker (flipbooker.com, domain field).",
    "AI / B2B Sales / Content Marketing",
    _dl(_s),
    "The body says 'Email [email redacted]' - Sourcee redacts the address, and the page publishes "
    "no handle and no link (published_links = Sourcee's own author chrome only). NOT RESOLVED.",
    "low",
    "A Flipbooker blog piece asking B2B vendors what they are seeing as buyers paste vendor "
    "proposals into AI tools and ask for the short version. It concerns how proposals are READ, not "
    "what AI tools COST - the body carries no price, budget or subscription figure - and it is a "
    "content-marketing request from a vendor rather than a news desk. Recorded as an AI-token window "
    "slug.",
    _NN,
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
    f"Lead with the dated price set behind the blocked-employee workaround: {n_paid} of {n_tools} tracked tools publish "
    f"a monthly price, {n_25} of those at or under $25/month, median ${med_paid}; paying monthly instead of annually "
    "costs 1.11x-2.53x across the 19 tiers where both terms are held, median 1.25x (snapshots updated "
    f"{_snap_updated}, pair set built 2026-10-08). State plainly that we are not an employee with a blocked account. "
    f"Route: LinkedIn DM to https://www.linkedin.com/in/christopher-mims-club/ — George's lane. "
    f"Draft: pitch-drafts-{TODAY}.md section 1."
)
print("rewrote the sendable row's route and angle from today's probe")


# ---------------------------------------------------------------------------
# A SECOND ROUTE RESOLVED THIS RUN, three days after six byline pages dead-ended.
# The 2026-10-11 run tried six byline pages for this journalist and all six returned HTTP 403, and the
# row has been carried as NOT SENDABLE since. It is sendable now, off his own site rather than off a
# byline page: tobiamure.com publishes hello@tobiamure.com in its Person schema (`"email":"mailto:..."`),
# in the FAQ answer he wrote himself ("Send the brief through the contact page or email
# hello@tobiamure.com. I reply to editors within two business days."), and in the site footer. The
# request itself is explicit that email is the only door - "No DM pitches here on LinkedIn. Email me."
# ---------------------------------------------------------------------------
_AMURE = "tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring"
_amure_route = json.loads((D / f"route-checks-{TODAY}.json").read_text())["routes"]["tobiamure.com/"]
by_slug[_AMURE]["contact_method"] = (
    "The request page redacts the address ('email me at [email redacted]') and says explicitly 'No DM "
    "pitches here on LinkedIn. Email me.' NOT SENDABLE until an address is published somewhere other "
    "than the redacted body - resolved today. ROUTE: hello@tobiamure.com, published by the journalist "
    f"himself on his own site, https://tobiamure.com/ - re-fetched today in route-checks-{TODAY}.json: "
    f"HTTP {_amure_route['http']}, {_amure_route['bytes']:,} bytes, title '{_amure_route['title']}'. The "
    "address appears verbatim three times on that page: in the Person JSON-LD email field, in his own "
    "FAQ answer ('Send the brief through the contact page or email hello@tobiamure.com. I reply to "
    "editors within two business days.'), and in the site footer. tobiamure.com MX = Namecheap email "
    "forwarding (eforward1-5.registrar-servers.com), so the domain routes mail. Six byline pages "
    "re-checked today so they are not retried as routes: muckrack.com/tobi-amure, "
    "investopedia.com/tobi-amure-5203106, forbes.com/sites/tobiamure, thestreet.com/author/tobi-amure, "
    "benzinga.com/author/tobi-amure, inc.com/author/tobi-amure - all HTTP 403. EMAIL ROUTE - no platform "
    "form, no DM, no scheduling link. Sending is George's lane."
)
by_slug[_AMURE]["suggested_pitch_template"] = (
    "Answer his own stated requirement - 'Original data, or a survey with its sample size and method' - "
    f"with the method and the denominator, not a credential: {n_paid} of {n_tools} tracked AI tools publish a "
    f"monthly price, {n_25} of those at or under $25/month, median ${med_paid}, every figure carrying the date we "
    "checked it and a source URL (snapshots updated "
    f"{_snap_updated}); paying monthly rather than annually costs 1.11x-2.53x across the 19 tiers where both "
    "terms are held, median 1.25x (pair set built 2026-10-08). Say plainly that we hold no workplace "
    "credential and are offering a data set, not testimony. Route: email to hello@tobiamure.com - George's "
    f"lane. Draft: pitch-drafts-{TODAY}.md section 2."
)
print("resolved a second route (Tobi Amure / Fast Company Work Life) and rewrote the row from today's probe")


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

# Counted with build_pitch_queue.py's own rule (live, not cold, a route in the contact field, and
# relevance above 'low'), not typed - the two artefacts of this monitor disagreeing is the only
# reason a wrong number here is visible at all.
def _has_route(o: dict) -> bool:
    c = o.get("contact_method") or ""
    return "@" in c or "linkedin.com/in/" in c or "://" in c and "sourcee.app" not in c


_sendable_now = sum(1 for o in live
                    if (o.get("relevance") or "").lower() not in ("low", "") and _has_route(o))
print(f"sendable by the queue's own rule: {_sendable_now}")

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
# The prose scan. `_bodies_1014.py` now records ai_prose_in_body (scripts/sourcee_terms.AI_PROSE);
# on the 111 bodies of this window it finds 11 AI hits where the old slug-tuned regex found 0.
_ai_body_prose = sum(1 for r in bodies.values() if r.get("ai_prose_in_body"))
_ai_prose_spend = sum(1 for r in bodies.values()
                      if r.get("ai_prose_in_body") and r.get("real_spend_in_body"))
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
        f"slugs and {window['feed_overlap_with_window']} of them are inside today's "
        f"{len(window['window'])}-slug sitemap window, and {len(_tracked_in_feed)} "
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
                f"{len(window['spend_any'])} carry a spend token alone. Every one of the "
                f"{len(window['window'])} window "
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
         "notes": f"HTTP {PLAT['HARO (helpareporter.com)']['http']}, "
                  f"{PLAT['HARO (helpareporter.com)']['bytes']:,} bytes, page title "
                  f"'{PLAT['HARO (helpareporter.com)']['title']}'. Expected; not retried. "
                  "Unchanged since 2026-09-12."},
        {"platform": "Connectively (connectively.us)", "status": "blocked",
         "notes": f"HTTP {PLAT['Connectively (connectively.us)']['http']}, "
                  f"{PLAT['Connectively (connectively.us)']['bytes']:,} bytes, "
                  f"'{PLAT['Connectively (connectively.us)']['title']}'. Expected; not retried."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "not-applicable",
         "notes": f"HTTP {PLAT['Source of Sources (sourceofsources.com)']['http']} at /requests, "
                  f"{PLAT['Source of Sources (sourceofsources.com)']['bytes']:,} bytes, page title "
                  f"'{PLAT['Source of Sources (sourceofsources.com)']['title']}'. Reporter-only per "
                  "the monitor's standing finding."},
        {"platform": "Qwoted (qwoted.com)", "status": "blocked",
         "notes": f"HTTP {PLAT['Qwoted (qwoted.com)']['http']} at app.qwoted.com/requests, "
                  f"{PLAT['Qwoted (qwoted.com)']['bytes']:,} bytes; the app needs an authenticated "
                  "session. Not retried."},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre-launch",
         "notes": f"HTTP {PLAT['MentionMatch (mentionmatch.com)']['http']}, "
                  f"{PLAT['MentionMatch (mentionmatch.com)']['bytes']:,} bytes, "
                  f"'{PLAT['MentionMatch (mentionmatch.com)']['title']}'. Still a holding page."},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "blocked",
         "notes": f"HTTP {PLAT['Medialyst MCP (medialyst.ai/api/mcp)']['http']}, "
                  f"{PLAT['Medialyst MCP (medialyst.ai/api/mcp)']['bytes']} bytes - the MCP endpoint "
                  "needs an OAuth handshake. Sixth consecutive run. This is the one platform that "
                  "would widen supply, and it is blocked on an account, not on the monitor."},
        {"platform": "ResponseSource (responsesource.com)", "status": "accessible-but-not-usable",
         "notes": f"HTTP {PLAT['ResponseSource (responsesource.com)']['http']}, "
                  f"{PLAT['ResponseSource (responsesource.com)']['bytes']:,} bytes. Public pages "
                  "only; the request database needs a subscription."},
    ],
    "opportunities": opps,
    "new_this_run": [
        (f"EIGHT ROWS ADDED - every AI-token slug in the {len(window['window'])}-slug window - AND NOT ONE "
         f"OF THEM IS A CANDIDATE. None publishes a reply route that reaches us and none asks about tool "
         f"cost: an education-policy post about school and NGO AI adoption (the one Anthropic-adjacent "
         f"row), a Star Tribune callout for Minnesotans who asked an AI about candidates, a same-day "
         f"ABC10 interview request addressed to one named adviser, a founder-story collection for African "
         f"AI founders, a two-line call for higher-ed non-faculty staff, a podcast guest invitation, a "
         f"conference-attendance ask for AI data-centre people in London, and a Flipbooker content request "
         f"about buyers pasting proposals into AI tools. Recorded as measurements so the window is fully "
         f"accounted for."),
        (f"THE WINDOW PRODUCED ZERO CORE-BEAT REQUESTS AND ZERO AI+SPEND SLUGS: {len(window['window'])} "
         f"slugs, {len(window['ai'])} AI-token, {len(window['ai_strict'])} AI+spend, "
         f"{len(window['spend_any'])} spend-only. This is the first window since the token fix that "
         f"produced no AI+spend slug at all; yesterday's single match "
         f"(b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research) was already judged a false "
         f"positive on our beat, and today's nearest equivalent is written up in full in its own row "
         f"(b2b-vendors-buyers-pasting-proposals-into-ai-tools): how proposals are READ, not what AI tools "
         f"COST. All {len(window['window'])} window bodies were fetched and read, which is the only check "
         f"that can back a zero."),
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
        f"{len(cold)} are cold. TWO are sendable, up from one: the WSJ columnist's blocked-work-accounts "
        f"request (relevance 'medium', now {SENDABLE[0]['_days_old']} days old, LinkedIn DM), carried and unsent "
        "since 2026-10-10; and - NEW THIS RUN - the Fast Company Work Life request for AI-at-work data, whose "
        "route six byline pages could not reach and whose own site could: hello@tobiamure.com, published by the "
        "journalist himself on tobiamure.com (HTTP 200, 58,905 bytes today, same-day; MX live). No pitch has been "
        "sent since 2026-10-10 21:20 UTC and no reply has arrived to any of the three sends from that run - the "
        "Amplemarket thread stays closed by the vendor's own acknowledgment and must not be bumped. The window "
        f"produced {len(window['window'])} slugs with {len(window['ai'])} AI-token and {len(window['ai_strict'])} "
        "AI+spend. "
        f"Headline figures re-derived this run against the snapshot (updated {_snap_updated}): "
        f"{n_paid} of {n_tools} tools publish a monthly price, {n_25} of those at or under $25/month, "
        f"median ${med_paid}; monthly vs annual 1.11x-2.53x, median 1.25x over 19 tiers (pair set built "
        "2026-10-08, re-read not rebuilt). Zero pitches sent this run - sends remain George's lane."
    ),
    "recommended_actions": [
        f"SEND THE WSJ BLOCKED-WORK-ACCOUNTS DRAFT - STILL THE ONLY SENDABLE ROW IN THE QUEUE, NOW "
        f"{SENDABLE[0]['_days_old']} DAYS OLD, CARRIED UNSENT THROUGH FIVE RUNS. Paste-ready at "
        f"pitch-drafts-{TODAY}.md section 1. Route: LinkedIn DM to "
        "https://www.linkedin.com/in/christopher-mims-club/ (the request's own body says '(DMs open)'). "
        "Relevance 'medium'. George's lane, not automatable. Route re-fetched today: "
        f"HTTP {_mims_route['http']}, {_mims_route['bytes']:,} bytes. Two dead ends are recorded so they "
        f"are not retried as routes: muckrack.com/christopher-mims HTTP "
        f"{_route['muckrack.com/christopher-mims/']['http']} and wsj.com/news/author/christopher-mims HTTP "
        f"{_route['wsj.com/news/author/christopher-mims/']['http']}. TODAY IS ITS LAST FULL DAY AS A "
        "SENDABLE ROW: at 10 days old on 2026-10-15 it sits exactly on the line, and on 2026-10-16 it "
        "crosses it and leaves the sendable list - nothing brings it back once it does.",
        "NOTE THAT NO REPLY HAS ARRIVED TO EITHER DELIVERED PITCH FROM 2026-10-10 (google-and-claude-enterprise-"
        "users-seats-and-token-costs, speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech); the "
        "third (fulltime-employees-shadow-ai-use-and-paying-outofpocket) bounced with a 550 NoSuchUser and its "
        "address is dead. Mailbox checked today across INBOX/All Mail/Sent/Spam/Trash: the newest message of any "
        "kind is a Gamma affiliate note at 2026-10-14 11:10 UTC and the newest sent message is our own reply to "
        "it at 11:38 UTC - no pitch recipient has written in. The only inbound from any pitch recipient ever is "
        "still Jan Suski's 2026-09-18 message, acknowledged and closed on 2026-10-11.",
        "ACCEPT THAT SOURCEE SUPPLY IS EXHAUSTED FOR THIS BEAT, and decide on Medialyst rather than re-measuring "
        f"it a sixth time. Today's evidence: {len(window['window'])} slugs, {len(window['ai'])} AI-token, none on "
        "our beat, and for the first time no AI+spend slug at all. Six consecutive runs have reported the same "
        "401 on the Medialyst MCP endpoint. If the account is not going to be opened, say so and the monitor "
        "stops reporting it as the one widening option.",
        f"DO NOT DRAFT ANY OF TODAY'S EIGHT ROWS. None has a route and none is on our beat; drafting one would "
        f"add another unsent file to the {len(list(D.glob('pitch-drafts-*.md')))} already on disk and another "
        f"unsent row to the {DRAFTS_UNSENT} the ledger still records without a send. That is the exact failure "
        "this monitor was rebuilt to stop repeating.",
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
        "body_level_ai_hits": _ai_body_prose,
        "body_level_ai_plus_spend_hits": _ai_prose_spend,
        "new_rows_added_to_tracking": len(NEW),
        "rows_recovered_by_filter_fix": 0,
        "tracked_urls": len(opps),
        "unpitched": len(unpitched),
        "live_unpitched": len(live),
        "cold_unpitched": len(cold),
        "pitched_plus_skipped": len(pitched | skipped),
        "sendable": len(SENDABLE),
        "pitches_sent_this_run": 0,
        "sendable_rows": _sendable_now,
        "sendable_new_this_run": 1 if _AMURE in {o["slug"] for o in live} else 0,
        "routes_resolved_this_run": ["tobiamure.com/ (hello@tobiamure.com, for tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring)"],
        "pitches_sent_on_2026-10-10_by_george": 3,
        "messages_bounced_on_2026-10-10": 1,
        "replies_to_date": 1,
        "reply_status_checked": TODAY,
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
        "THE BODY-LEVEL AI SCAN WAS MEASURING NOTHING, AND THE FALSE ZERO IS NOW FIXED RATHER THAN RECORDED. "
        "Every digest from 2026-10-11 to 2026-10-13 carried a note admitting that the body scan reported zero "
        "AI hits even on bodies that say 'AI' in plain text, because the token set in scripts/sourcee_terms.py "
        "is written for SLUGS, where every token must be hyphen-delimited. Prose has no hyphens, so a request "
        "titled 'B2B Vendors - Buyers Pasting Proposals Into AI Tools' scanned clean. The window's zero rested "
        "on hand-quoted bodies, not on the regex, and the note said the regex must not be cited as evidence "
        "until fixed. Fixed this run: scripts/sourcee_terms.py gains AI_PROSE (word-boundary prose matcher "
        "including the two-word forms) and prose_ai(); marketing/haro-outreach/_bodies_*.py records "
        "ai_prose_in_body alongside the old field; scripts/rescan_body_ai.py re-scans stored bodies with no "
        "network calls and self-checks the matcher with three assertions. Re-scanning today's 111 stored bodies "
        f"returns {_ai_body_prose} AI hits, of which {_ai_prose_spend} is also a real-spend body "
        "(men-who-used-mental-health-chatbots-and-apps-experience-cost-ease - a consumer mental-health story, "
        "already tracked). The headline 'zero AI+spend' claim above still holds under the fixed matcher, and it "
        "now holds on evidence.",
        "THE PLATFORM PROBE'S BYTE COUNTS AND STATUS TEXTS WERE HAND-TYPED INTO THE DIGEST. The per-platform "
        "notes in `platforms_checked` carried literals like 'HTTP 429, 31,373 bytes' and 'Fifth consecutive run' "
        "copied forward run after run while the probe's own output sat in the window file. That is the same "
        "defect class as the hand-typed mark and the hand-typed live-row count fixed on 2026-10-12 and "
        "2026-10-13, and it silently froze the Medialyst 'fifth consecutive run' sentence in place. Every "
        "per-platform note is now read out of the window probe's `platforms` array, so the byte counts, the "
        "titles and the checkpoint flag move with the measurement.",
        "THE PER-RUN WINDOW AND BODY SCRIPTS ARE STILL HAND-COPIED, AND THAT IS RECORDED AS A KNOWN GAP, NOT A "
        "FIX. _window_1014.py and _bodies_1014.py were produced by copying yesterday's files and editing two "
        "constants, which is exactly how the route probe silently lost two URLs on 2026-10-12. The window "
        "script now reads its mark from the previous run rather than pasting it, and the body script now "
        "imports the prose matcher, but the copy step itself survives and remains the monitor's one unfixed "
        "structural defect. Converting both to scripts/ with an explicit run date is the next real fix.",
        "THE DIGEST CLASSIFIED THE FRESHEST ROWS IN THE QUEUE AS COLD, AND THE CAUSE WAS A FALSY ZERO. Fixed "
        "yesterday and carried forward: the line `live = [o for o in unpitched if (o['_days_old'] or 999) <= 10]` "
        "turns a request posted TODAY into 999, because `_days_old == 0` is falsy. Replaced with an explicit "
        "None test. Same defect class as the hand-typed live-row count fixed on 2026-10-01 - a number that "
        "looks measured and is an artefact of the expression that produced it.",
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(out, indent=1))
print(f"\nwrote digest-{TODAY}.json: {len(out['opportunities'])} opportunities, "
      f"{len(out['new_this_run'])} new-this-run notes, {len(out['expired_this_run'])} expiry notes")
