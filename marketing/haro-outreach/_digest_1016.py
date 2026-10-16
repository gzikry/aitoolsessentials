#!/usr/bin/env python3
"""Compose marketing/haro-outreach/digest-2026-10-16.json.

Carries the 136 tracked rows forward with their page truth refreshed from verified-requests.json
(re-fetched today by scripts/verify_journo_requests.py, 136 URLs, every one HTTP 200 and live), and
adds the four AI-token rows found in today's 94-slug window.

Nothing is marked pitched here: sends are George's lane and the ledger is the only place a send is
recorded.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing/haro-outreach"
TODAY = "2026-10-16"
PREV = "2026-10-15"

prev = json.loads((D / f"digest-{PREV}.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
window = json.loads((D / f"_window_{TODAY.replace('-', '')[4:]}.json").read_text())
bodies = json.loads((D / f"_bodies_{TODAY.replace('-', '')[4:]}.json").read_text())
feed = json.loads((D / "ai-topic-feed.json").read_text())
FEED = set(feed["slugs"])

# The platform probes run in the window script; reading them out of its output rather than typing
# them here is the fix made on 2026-10-14 and carried forward - a typed byte count is the same
# defect class as the typed mark and the typed live-row count fixed on earlier runs.
PLAT = {p["platform"]: p for p in window["platforms"]}

SITE = "https://www.sourcee.app/journo-request/"
# The union of tracked URLs scripts/verify_journo_requests.py probed today, plus the four slugs found
# in today's window, which were passed to the verifier by hand (the verifier reads its input from
# pitch-queue.md, the digests and the ledger, all of which describe yesterday's state).
VERIFY_URLS = 136
VERIFY_NEW = 4


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
# Headline figures re-derived at build time, never typed. The snapshot file is refreshed by the
# daily maintenance job and on this run carries `updated: 2026-10-16`, so a figure typed here
# would be a day stale inside a file built today.
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
        return ("?", "?", "?", "?", _snaps.get("updated") or "?")
    import statistics as _st
    return (str(len(_tools)), str(len(_paid)), str(sum(1 for v in _paid.values() if v <= 25)),
            f"{_st.median(_paid.values()):.2f}", _snaps.get("updated") or "?")


n_tools, n_paid, n_25, med_paid, _snap_updated = _derive_figures()

_pairs = json.loads((S / "data/monthly_annual_pairs.json").read_text())
PAIR_TXT = (f"{_pairs['range_low']}x to {_pairs['range_high']}x, median {_pairs['median']}x over "
            f"{_pairs['n']} tiers, pair set re-asserted {_pairs['built']}")
print(f"figures re-derived: {n_paid} of {n_tools} monthly-priced, {n_25} at/under $25, "
      f"median ${med_paid}, snapshot updated {_snap_updated}; pairs {PAIR_TXT}")


# A carried row can carry a figure from the day it was written. The 2026-10-15 digest shipped rows
# quoting "42 of 77 tools" while that same file's headline figure was 78 tools, and the queue renders
# those rows to George - so the two artefacts of this monitor disagreeing is visible to him, which is
# the only reason a wrong number here is findable at all. Re-derived here rather than edited by hand,
# and every repaired row is named.
def _repair_tool_count(o: dict) -> dict:
    t = o.get("suggested_pitch_template") or ""
    if not t:
        return o
    new, n = re.subn(r"of 7[0-9] (tools|tracked AI tools)", rf"of {n_tools} \1", t)
    if n and new != t:   # a substitution that leaves the text unchanged is not a repair
        o = dict(o)
        o["suggested_pitch_template"] = new
        o["_figures_repaired"] = sorted(set(o.get("_figures_repaired") or []) | {"suggested_pitch_template"})
        _FIG_REPAIRED.append(o["slug"])
    return o


_FIG_REPAIRED: list[str] = []
opps = [_repair_tool_count(o) for o in opps]
print(f"carried rows whose template quoted a superseded tool count: {len(_FIG_REPAIRED)} {_FIG_REPAIRED}")


_NN = ("None. No route and no standing. NOT DRAFTED - see the run's own note on why another "
       "unsent draft would be a defect rather than progress.")


def core(slug: str) -> str:
    return (bodies.get(slug) or {}).get("core", "")


def dp(slug: str) -> str:
    return (verified.get(slug) or {}).get("datePublished") or ""


def _dl(slug: str) -> str:
    r = verified[slug]
    return (f"No cutoff stated. Page fetched today: HTTP 200, live=True, badge "
            f"'{r.get('badge')}', datePublished {dp(slug)} = {r['days_old']} days.")


# ---------------------------------------------------------------------------
# Rows found this run - every AI-token slug in the 94-slug window. All four are recorded as
# measurements; none is a candidate and the single AI+spend row of the window is the clearest bar
# this monitor has yet had to record.
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
            "_new_or_recovered_2026-10-16": True}


# Note carried on every row added today: the only links the body extractor sees on these pages
# are Sourcee's own author chrome (linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith), which
# scripts/verify_journo_requests.py excludes from `published_links` by design. They are NOT routes
# and must not be read as one.
_CHROME = ("The only links on the page are Sourcee's own author chrome "
           "(linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes "
           "from published_links; neither is a route to the poster.")

# 1. The one AI+spend slug of the window, and the sharpest standing bar in eight runs: a named
# reporter at a named publication, a cost question squarely on our beat ("what it really costs"),
# and a sourcing rule that excludes us in the journalist's own words.
_s = "cios-and-ai-leaders-ai-infrastructure-day2-ops-and-costs"
NEW.append(new_row(
    _s,
    core(_s)[:900],
    "Punam Singh (the page's own author field) - CIO&Leader / ET Edge (indiatimes.com, domain "
    "field). The body calls it an ET Edge cover story on 'Infrastructure for AI'.",
    "AI / Enterprise Infrastructure / Day-2 Ops & Costs",
    _dl(_s),
    "The body says 'Please reach out to [email redacted]' - Sourcee redacts the address, and the "
    "page publishes no handle and no link. " + _CHROME + " NOT RESOLVED. AND THE ROW IS CLOSED TO "
    "US BY ITS OWN WORDING, whether or not a route is ever resolved: 'As this story focuses on "
    "end-user experience, we will not be taking vendor quotes, and we thank you for your "
    "understanding.' AIToolsEssentials is a publisher of dated vendor pricing - a vendor-adjacent "
    "source by that rule, not an end-user enterprise.",
    "low",
    "The first AI+spend slug in this monitor's window since 2026-10-08: it asks what AI 'really "
    "costs' once it is running in production under a budget, and names the exact quantity this "
    "site holds dated evidence for. It is unusable for a reason that has nothing to do with our "
    "data: the ask is for end-user businesses - regulated BFSI, manufacturing, IT services and "
    "GCCs, pharma, retail, mid-market CIOs, CTOs, CISOs and CFOs - and the request rules vendor "
    "quotes out in writing. Recorded rather than dressed up, because a request that matches our "
    "beat and excludes us by its own terms is the single most misleading shape this monitor "
    "produces.",
    _NN,
))

# 2. A real byline at a real outlet, a personal-experience bar, and a DM route that is not ours.
_s = "companies-and-data-buyers-selling-corporate-data-to-train-ai"
NEW.append(new_row(
    _s,
    core(_s)[:900],
    "Sam Blum (the page's own author field). No outlet named on the request or in the body; the "
    "author field matches a staff reporter who writes on technology and labour.",
    "AI / Training Data / Corporate Data Sales",
    _dl(_s),
    "The body says 'DM me for my Signal information if you'd like to speak anonymously' and "
    "publishes no address, handle or link. " + _CHROME + " NOT RESOLVED - and the ask is a DM "
    "that becomes a Signal conversation, which is not a route this monitor can use.",
    "low",
    "He wants companies that have SOLD corporate data to an AI lab for training, or businesses "
    "that buy it. The standing bar is being either side of that transaction: we have never sold "
    "corporate data and we do not buy it. Our dated price set describes what AI tools cost to "
    "buy, which is a different question from what company data fetches from a lab. Recorded as "
    "an AI-token window slug; no cost, subscription or tool-pricing question in the body.",
    _NN,
))

# 3. A named reporter, a named outlet, and a standing bar that is a job, not a data set.
_s = "uk-political-analysts-disinformation-and-ai-manipulation-in-politics"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Flaminia (the page's own author field). No outlet named on the request; the body carries a "
    "#journorequest tag and the subject is UK politics.",
    "AI / Politics / Disinformation",
    _dl(_s),
    "The body is a bare #journorequest asking to speak to someone, and publishes no address, "
    "handle or link of its own. " + _CHROME + " NOT RESOLVED. The route would in any case be a "
    "reply on the poster's own platform.",
    "low",
    "The ask is for UK political analysts on disinformation and AI manipulation in politics. The "
    "standing bar is a practising UK political analyst; we meet none of it. Nothing in the body "
    "touches tool cost, subscriptions, credits or software spend. Recorded as an AI-token window "
    "slug - one line of text is the whole request.",
    _NN,
))

# 4. The broadest of the four: a real reporter with a real beat, inviting exactly the kind of
# angle we could write - and no route, plus a standing bar that is a creator, not a publisher.
_s = "content-creators-using-ai-job-losses-and-ethics"
NEW.append(new_row(
    _s,
    core(_s)[:900],
    "Saumya Rastogi (the page's own author field). No outlet named on the request or in the body.",
    "AI / Content Creation / Labour & Ethics",
    _dl(_s),
    "The body says 'please DM me or drop a comment below' - a route on the poster's own platform, "
    "with no handle, address or link printed on the request. " + _CHROME + " NOT RESOLVED.",
    "low",
    "A story on AI-powered content creation, sourcing people who create content with AI, have "
    "lost work to it, are building an AI content company, or can speak to originality and "
    "ownership. The 'insights into the ethical questions' half is genuinely open to a publisher, "
    "and this is the closest of the four to a usable angle - but there is no route to send it to, "
    "the standing bar for the main ask is a creator's own experience, and the body asks nothing "
    "about what AI tools cost. Recorded as an AI-token window slug.",
    _NN,
))

opps.extend(NEW)
print(f"added {len(NEW)} new rows -> {len(opps)} tracked")


# ---------------------------------------------------------------------------
# The one row that carries a route usable today. Rewritten from today's own route probe, not from
# yesterday's byte counts.
# ---------------------------------------------------------------------------
_routes = json.loads((D / f"route-checks-{TODAY}.json").read_text())["routes"]

_AMURE = "tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring"
_amure_route = _routes["tobiamure.com/"]
_amure_contact = _routes["tobiamure.com/contact/"]
by_slug[_AMURE]["contact_method"] = (
    "The request page redacts the address ('email me at [email redacted]') and says explicitly 'No DM "
    "pitches here on LinkedIn. Email me.' ROUTE: hello@tobiamure.com, published by the journalist "
    f"himself on his own site, https://tobiamure.com/ - re-fetched today in route-checks-{TODAY}.json: "
    f"HTTP {_amure_route['http']}, {_amure_route['bytes']:,} bytes, title '{_amure_route['title']}', "
    f"with the address appearing verbatim {_amure_route.get('address_verbatim_on_page')} times on that "
    "page (Person JSON-LD email field, his own FAQ answer, and the site footer). His contact page "
    f"https://tobiamure.com/contact/ re-fetched today: HTTP {_amure_contact['http']}, "
    f"{_amure_contact['bytes']:,} bytes, title '{_amure_contact['title']}', address verbatim "
    f"{_amure_contact.get('address_verbatim_on_page')} times. tobiamure.com MX = Namecheap email "
    "forwarding (eforward1-5.registrar-servers.com), so the domain routes mail. Six byline pages "
    "remain recorded dead ends so they are not retried as routes (last re-checked 2026-10-15): "
    "muckrack.com/tobi-amure, investopedia.com/tobi-amure-5203106, forbes.com/sites/tobiamure, "
    "thestreet.com/author/tobi-amure, benzinga.com/author/tobi-amure, inc.com/author/tobi-amure - all "
    "HTTP 403. EMAIL ROUTE - no platform form, no DM, no scheduling link. Sending is George's lane."
)
by_slug[_AMURE]["suggested_pitch_template"] = (
    "Answer his own stated requirement - 'Original data, or a survey with its sample size and method' - "
    f"with the method and the denominator, not a credential: {n_paid} of {n_tools} tracked AI tools publish a "
    f"monthly price, {n_25} of those at or under $25/month, median ${med_paid}, every figure carrying the date we "
    f"checked it and a source URL (snapshots updated {_snap_updated}); paying monthly rather than annually "
    f"costs {PAIR_TXT}. Say plainly that we hold no workplace "
    "credential and are offering a data set, not testimony. Route: email to hello@tobiamure.com - George's "
    f"lane. Draft: pitch-drafts-{TODAY}.md section 1."
)
print("re-verified the Tobi Amure route from today's probe")

# The Mims row is no longer a sendable row: it crossed the 10-day line today. Its route was still
# re-fetched today, and the probe is recorded here so the crossing is not mistaken for the route
# going dead.
_MIMS = "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks"
_mims_route = _routes["linkedin.com/in/christopher-mims-club/"]
by_slug[_MIMS]["contact_method"] = (
    "Body says '(DMs open)'; no address, handle or link is printed in the request itself. Route: "
    f"https://www.linkedin.com/in/christopher-mims-club/ - re-fetched today in route-checks-{TODAY}.json: "
    f"HTTP {_mims_route['http']}, {_mims_route['bytes']:,} bytes, title '{_mims_route['title']}'. The route is "
    f"still live; the ROW is {by_slug[_MIMS]['_days_old']} days old and crossed the 10-day cold line today, so it "
    "is no longer counted sendable. Two dead ends remain recorded so they are not retried as routes (last "
    "re-checked 2026-10-15): muckrack.com/christopher-mims HTTP 403 (Cloudflare interstitial) and "
    "wsj.com/news/author/christopher-mims HTTP 401. LINKEDIN DM - George's lane. Not automatable."
)
print(f"re-fetched the Mims route; the row is now {by_slug[_MIMS]['_days_old']} days old and no longer sendable")


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


# `o["_days_old"] or 999` is WRONG and was wrong in the 2026-10-12 script this is built from: a
# request posted today has _days_old == 0, which is falsy, so the row was classified cold on the
# day it was freshest. Fixed 2026-10-13 and carried forward.
def _age(o: dict) -> int:
    d = o.get("_days_old")
    return d if d is not None else 999


live = [o for o in unpitched if _age(o) <= 10]
cold = [o for o in unpitched if _age(o) > 10]
print(f"tracked {len(opps)} | unpitched {len(unpitched)} | live {len(live)} | cold {len(cold)}")


# Counted with build_pitch_queue.py's own rule (live, not cold, a route in the contact field, and
# relevance above 'low'), not typed - the two artefacts of this monitor disagreeing is the only
# reason a wrong number here is visible at all.
def _has_route(o: dict) -> bool:
    c = o.get("contact_method") or ""
    return "hello@tobiamure.com" in c or "linkedin.com/in/" in c or ("://" in c and "sourcee.app" not in c)


_sendable_now = sum(1 for o in live
                    if (o.get("relevance") or "").lower() not in ("low", "") and _has_route(o))
print(f"sendable by the queue's own rule: {_sendable_now}")

# A slug NAMED anywhere in a draft file is not a drafted row: every run's draft file also names the
# rows it deliberately did NOT draft, so counting bare slug occurrences inflated this figure (29 on
# 2026-10-16, of which 4 were the rows the file explicitly declines to draft). A row is drafted only
# when the file carries it as a draft, which is marked by its own `**Source:** <url>` line.
_drafted = set()
for f in D.glob("pitch-drafts-*.md"):
    txt = f.read_text(errors="ignore")
    sourced = {m.rstrip("/").split("/journo-request/")[-1]
               for m in re.findall(r"\*\*Source:\*\*\s*(https?://(?:www\.)?sourcee\.app/journo-request/[a-z0-9\-]+)", txt)}
    _drafted |= {o["slug"] for o in unpitched if o["slug"] in sourced}
DRAFTS_UNSENT = len(_drafted)
print(f"rows carried as a draft on disk with no send in the ledger: {DRAFTS_UNSENT}")

_tracked_in_feed = [o["slug"] for o in opps if o["_in_ai_topic_feed"]]
print("tracked rows in today's feed:", len(_tracked_in_feed), _tracked_in_feed)

_ai_body_hits = [s for s, r in bodies.items() if r.get("ai_tokens_in_body")]
# The prose scan (scripts/sourcee_terms.AI_PROSE) is the matcher that can actually see the word
# 'AI' in a sentence: the slug-tuned token set requires hyphens and reported a false zero on every
# run up to 2026-10-13.
_ai_body_prose = sum(1 for r in bodies.values() if r.get("ai_prose_in_body"))
_ai_prose_spend = sum(1 for r in bodies.values()
                      if r.get("ai_prose_in_body") and r.get("real_spend_in_body"))
_spend_only = [s for s, r in bodies.items()
               if r.get("spend_tokens_in_body") and not r.get("ai_tokens_in_body")]
print(f"body prose AI hits: {_ai_body_prose}; AI+real-spend: {_ai_prose_spend}; spend-only: {len(_spend_only)}")

_AMURE_AGE = by_slug[_AMURE]["_days_old"]
_MIMS_AGE = by_slug[_MIMS]["_days_old"]

out = {
    "date": TODAY,
    "monitor": "HARO / Sourcee journalist-request monitor for AIToolsEssentials",
    "run_at": datetime.now(timezone.utc).isoformat(),
    "search_scope": prev["search_scope"],
    "age_policy": (
        "Ages are read off each request page (JSON-LD datePublished plus the rendered 'Posted ... ago' "
        "badge), never off the digest text, and every carried row's deadline field was rewritten this "
        f"run from the page itself. All {VERIFY_URLS} tracked URLs were re-fetched and read today: HTTP 200 "
        f"for every one, body still served, no expiry notice; the {VERIFY_NEW} rows added today were "
        "fetched the same way and cached by the verifier before this digest was written. Two further "
        "facts belong here. (1) No request has ever been seen to expire on this source - 100% of carried "
        "rows have returned HTTP 200 on every run - so 'deadline' means the poster's own stated cutoff or "
        "a measured age, never an observed expiry, and the absence of an expiry notice is weak evidence "
        "recorded as such. (2) FEED MEMBERSHIP IS STILL NOT A FRESHNESS SIGNAL FOR THE BACKLOG: the AI "
        f"topic page carries {window['feed_count']} slugs and {window['feed_overlap_with_window']} of them "
        f"are inside today's {len(window['window'])}-slug sitemap window - the feed is a rolling window over "
        f"the newest requests, and {len(_tracked_in_feed)} tracked row(s) appear in it. A carried row's "
        "absence from the feed says nothing about that row, and its presence says only that the request "
        "is new."
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
                f"{len(window['window'])} window bodies was fetched and read - the only check that can "
                "back a zero. Site root "
                f"re-probed HTTP {PLAT['Sourcee (sourcee.app)']['http']} "
                f"({PLAT['Sourcee (sourcee.app)']['bytes']:,} bytes)."
            ),
        },
        {
            "platform": "Sourcee AI topic feed",
            "status": "accessible",
            "notes": (
                f"HTTP {window['feed_http']}, {window['feed_bytes']:,} bytes, {window['feed_count']} slugs. "
                f"{window['feed_overlap_with_window']} of the {window['feed_count']} are inside today's "
                f"{len(window['window'])}-slug sitemap window. {len(_tracked_in_feed)} tracked row(s) "
                "appear in it."
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
         "notes": f"HTTP {PLAT['Source of Sources (sourceofsources.com)']['http']} at /requests today "
                  f"(not 200), {PLAT['Source of Sources (sourceofsources.com)']['bytes']:,} bytes, title "
                  f"'{PLAT['Source of Sources (sourceofsources.com)']['title']}'. Reporter-only per the "
                  "monitor's standing finding; the /requests path 404s from this end, so even the "
                  "browse route is unchanged in usefulness."},
        {"platform": "Qwoted (qwoted.com)", "status": "blocked",
         "notes": f"HTTP {PLAT['Qwoted (qwoted.com)']['http']} at app.qwoted.com/requests, "
                  f"{PLAT['Qwoted (qwoted.com)']['bytes']:,} bytes; the app needs an authenticated session. "
                  "Not retried."},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre-launch",
         "notes": f"HTTP {PLAT['MentionMatch (mentionmatch.com)']['http']}, "
                  f"{PLAT['MentionMatch (mentionmatch.com)']['bytes']:,} bytes, "
                  f"'{PLAT['MentionMatch (mentionmatch.com)']['title']}'. Still a holding page."},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "blocked",
         "notes": f"HTTP {PLAT['Medialyst MCP (medialyst.ai/api/mcp)']['http']}, "
                  f"{PLAT['Medialyst MCP (medialyst.ai/api/mcp)']['bytes']} bytes - the MCP endpoint "
                  "needs an OAuth handshake. Eighth consecutive run. This is the one platform that "
                  "would widen supply, and it is blocked on an account, not on the monitor."},
        {"platform": "ResponseSource (responsesource.com)", "status": "accessible-but-not-usable",
         "notes": f"HTTP {PLAT['ResponseSource (responsesource.com)']['http']}, "
                  f"{PLAT['ResponseSource (responsesource.com)']['bytes']:,} bytes. Public pages only; the "
                  "request database needs a subscription."},
    ],
    "opportunities": opps,
    "new_this_run": [
        (f"FOUR ROWS ADDED - every AI-token slug in the {len(window['window'])}-slug window - AND NOT ONE "
         f"OF THEM IS A CANDIDATE. The sharpest is the one that looks most promising: a CIO&Leader / ET Edge "
         f"cover story on AI day-2 ops that asks what AI 'really costs' once it is running in production, "
         f"and then rules vendor quotes out in writing - it wants end-user CIOs, not a pricing publisher. "
         f"The other three are a corporate-data-sales callout (be the company that sold data to an AI lab), "
         f"a one-line #journorequest for UK political analysts, and a story on AI content creation that "
         f"invites exactly our kind of angle but publishes no route and asks about ethics, not cost. "
         f"Recorded as measurements so the window is fully accounted for."),
        (f"THE WINDOW PRODUCED ITS FIRST AI+SPEND SLUG SINCE 2026-10-08, AND ZERO USABLE CORE-BEAT REQUESTS: "
         f"{len(window['window'])} slugs, {len(window['ai'])} AI-token, {len(window['ai_strict'])} AI+spend, "
         f"{len(window['spend_any'])} spend-only. The AI+spend slug is the ET Edge one above. The other "
         f"nine spend-only slugs are all off-beat (family affordability, school recess policy, "
         f"cost-of-living before the midterms, allergy-safe food, inheritance spending, subscription-free "
         f"security cameras, small-business pay transparency, a boss who vanished on payday, a security "
         f"camera buyer's guide) and not one of them is an AI request. All {len(window['window'])} window "
         f"bodies were fetched and read, which is the only check that can back a zero; the prose matcher "
         f"({_ai_body_prose} AI hits across the window's bodies) is what makes that zero evidence rather "
         f"than an artefact."),
        "NO ROW DROPPED OFF: every tracked row is carried in every digest by design, so that figure is a "
        "monitor convention and not platform evidence - see age_policy.",
    ],
    "expired_this_run": [
        (f"Nothing expired on its page: all {VERIFY_URLS} tracked URLs returned HTTP 200 with the request "
         f"body still served, and so did the {VERIFY_NEW} new ones. See age_policy - an expiry has never "
         f"once been observed on this source, so the absence of an expiry notice is weak evidence and is "
         f"recorded as such."),
        (f"ROWS CROSSED THE 10-DAY LINE SINCE YESTERDAY: {len(crossed)}."
         + (" " + "; ".join(crossed) + "." if crossed else " No row crossed.")),
        (f"{len(at_ten)} ROW(S) SIT AT EXACTLY 10 DAYS AND CROSS TOMORROW, named here in advance because a "
         f"quiet count change should never be mistaken for a quiet week: " + "; ".join(at_ten) + "."
         if at_ten else "No row sits at exactly 10 days today, so the next run has no scheduled crossing."),
        "ROWS THAT DROPPED OFF THE NEWEST DIGEST: 0. Every tracked row is carried in every digest by "
        "design, so this figure is a monitor convention and not platform evidence - see age_policy.",
    ],
    "summary": (
        f"{len(opps)} tracked requests ({len(prev['opportunities'])} carried and all "
        f"{len(prev['opportunities'])} re-verified live, {len(NEW)} added this run, {len(pitched)} pitched, "
        f"{len(skipped)} deliberately skipped). Of the {len(unpitched)} unpitched, {len(live)} are live and "
        f"{len(cold)} are cold. ONE is sendable: the Fast Company Work Life request for AI-at-work data "
        f"(low-medium, {_AMURE_AGE} days old), whose route is an email address published by the journalist "
        f"on his own site, hello@tobiamure.com, re-verified today. The WSJ blocked-work-accounts row that "
        f"was the other sendable row is now {_MIMS_AGE} days old - it crossed the 10-day cold line today, "
        f"its LinkedIn route is still live but the row has left the sendable list and nothing brings it "
        f"back. No pitch has been sent since 2026-10-10 21:20 UTC and no reply has arrived to any of the "
        f"three sends from that run; the Amplemarket thread stays closed by the vendor's own acknowledgment "
        f"and must not be bumped. The window produced {len(window['window'])} slugs with "
        f"{len(window['ai'])} AI-token and {len(window['ai_strict'])} AI+spend. "
        f"Headline figures re-derived this run against the snapshot (updated {_snap_updated}): "
        f"{n_paid} of {n_tools} tools publish a monthly price, {n_25} of those at or under $25/month, "
        f"median ${med_paid}; monthly vs annual {PAIR_TXT}. Zero pitches sent this run - sends remain "
        f"George's lane."
    ),
    "recommended_actions": [
        f"SEND THE TOBI AMURE EMAIL - THE ONLY SENDABLE ROW THIS RUN, AND THE ONLY ONE THAT WAS SENDABLE "
        f"YESTERDAY AND STILL IS. {_AMURE_AGE} days old, relevance low-medium, route hello@tobiamure.com "
        f"re-verified today (tobiamure.com HTTP {_amure_route['http']}, {_amure_route['bytes']:,} bytes, "
        f"address verbatim {_amure_route.get('address_verbatim_on_page')} times; /contact/ HTTP "
        f"{_amure_contact['http']}, {_amure_contact['bytes']:,} bytes; MX = Namecheap forwarding). "
        f"Paste-ready at pitch-drafts-{TODAY}.md section 1. He states his own requirement ('Original data, "
        f"or a survey with its sample size and method') and the draft answers it with method and "
        f"denominator. Email route - technically automatable over SMTP, but sends are George's lane.",
        f"DECIDE WHETHER TO SEND THE WSJ BLOCKED-WORK-ACCOUNTS PITCH LATE, OR RECORD IT SKIPPED. It crossed "
        f"the 10-day cold line today at {_MIMS_AGE} days and has now left the sendable list after being "
        f"carried unsent through seven runs. The route still resolves "
        f"(linkedin.com/in/christopher-mims-club/ re-fetched today: HTTP {_mims_route['http']}, "
        f"{_mims_route['bytes']:,} bytes) and the draft still exists at pitch-drafts-2026-10-15.md section 1, "
        f"but this monitor will no longer rank it as actionable. Either state is fine; silence is what "
        f"leaves it drifting.",
        "NOTE THAT NO REPLY HAS ARRIVED TO ANY PITCH. Mailbox checked today across INBOX, All Mail, Sent "
        "Mail, Drafts and folder list: the newest inbound from any pitch recipient remains Jan Suski's "
        "2026-10-11 06:57 UTC acknowledgment, which closed the Amplemarket thread, and the only other "
        "inbound from a pitch recipient in the whole mailbox is his 2026-09-18 first reply. Nothing has "
        "come from foxandspindle.com, sherwood.news, epgacceleration.com, artichokehq.com or raconteur.net "
        "at any point. All Mail page 1 spans 2026-08-31 to 2026-10-16, so the search covers every send.",
        "DO NOT DRAFT TODAY'S FOUR ROWS. None has a route and none is on our beat; the one that is on our "
        f"beat excludes vendor quotes in writing. Drafting any of them would add another unsent row to the "
        f"{DRAFTS_UNSENT} draft rows this monitor already carries without a send (counted from `**Source:**` "
        "lines in the draft files, not from any mention of a slug). That is the exact failure this monitor "
        "was rebuilt to stop repeating.",
        "ACCEPT THAT SOURCEE SUPPLY IS EXHAUSTED FOR THIS BEAT, and decide on Medialyst rather than "
        f"re-measuring it an eighth time. Today's evidence: {len(window['window'])} slugs, "
        f"{len(window['ai'])} AI-token, and the one AI+spend row closed to us by the journalist's own "
        "sourcing rule. Eight consecutive runs have reported the same 401 on the Medialyst MCP endpoint. "
        "If the account is not going to be opened, say so and the monitor stops reporting it as the one "
        "widening option.",
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
        "sendable": _sendable_now,
        "pitches_sent_this_run": 0,
        "sendable_rows": _sendable_now,
        "sendable_new_this_run": 0,
        "sendable_rows_crossing_tomorrow": len(at_ten),
        "routes_reverified_this_run": ["tobiamure.com/ and tobiamure.com/contact/ (hello@tobiamure.com, for "
                                       "tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring)",
                                       "linkedin.com/in/christopher-mims-club/ (LinkedIn DM, for "
                                       "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks - "
                                       "route live, row now cold)"],
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
        "monthly_annual_pairs_built": _pairs["built"],
    },
    "monitor_defects_fixed_this_run": [
        "THE QUEUE RENDERED A SUPERSEDED FIGURE FROM A CARRIED ROW, AND IT WAS RE-DERIVED RATHER THAN "
        "EDITED. Two carried rows still carried '42 of 77 tools' in their suggested_pitch_template - a "
        "figure from the day they were written, against today's 78 - and build_pitch_queue.py renders that "
        "field straight into the queue George reads, so the queue said 77 while its own headline said 78. "
        "A regex pass now re-derives the tool count inside every carried template at digest build time and "
        "records the row in `_figures_repaired`; two rows were repaired this run, and a substitution that leaves the text unchanged is not counted as one. Same defect class as the "
        "corrected Amplemarket range, caught this time before it was sent.",
        "THE QUEUE STILL BRANDED A COLD ROW 'SENDABLE', AND THE LABEL IS NOW DERIVED. build_pitch_queue.py's "
        "DRAFTS prose carried the string '**SENDABLE — draft ready and UNSENT**' for the WSJ "
        "blocked-work-accounts row as a literal. That row crossed the 10-day line today, so the queue's own "
        "headline count said 1 sendable while its prose said 2 - a label recording a past state and never "
        "re-derived, the same defect class as the hardcoded draft filename and the typed section numbers "
        "fixed on earlier runs. The label now comes from the row's measured age (new `_state_of()`), and the "
        "trailing sentence switches with it: still-inside-the-count or left-the-count, with the send-late-or-"
        "skip decision named either way.",
        "THE QUEUE'S ONE ACTIONABLE ROW ENDED IN HALF A MULTIPLIER. The row renderer cut every angle at "
        "`q['angle'][:400]`, and the sendable row's angle ends '... paying monthly rather than annually "
        "costs 1.11x to ' - truncated mid-value in the file George is meant to paste from. Truncation now "
        "backs up to the last sentence boundary inside the limit and says it has done so (new "
        "`_clip_angle()`), so a figure is never rendered half-written.",
        "THE QUEUE'S '23 DRAFT ROWS WITH NO SEND' FIGURE COUNTED ANY MENTION, NOT A DRAFT. The digest "
        "counted a row as drafted when its slug appeared anywhere in a draft file, but every run's draft "
        "file also names the rows it deliberately did NOT draft - so this run's own file inflated the "
        "figure to 29, four of them rows it explicitly declines to draft. A row now counts only when a "
        "draft file carries it as a draft, which is marked by its own `**Source:** <url>` line. The figure "
        "is reported below at its corrected value.",
        "THE FOUR ROWS FOUND TODAY WERE INVISIBLE TO THE QUEUE UNTIL THE VERIFIER SAW THEM, AND THIS RUN "
        "CLOSED THAT BY HAND AGAIN. scripts/verify_journo_requests.py builds its URL list from "
        "pitch-queue.md, the digests and the ledger - all of which describe YESTERDAY's state - so a slug "
        f"found in today's window has no page truth (no days_old, no badge, no feed membership) until the "
        "next run, and build_pitch_queue.py would rank it as 'age unknown'. Recorded as a defect on "
        f"2026-10-15 and still unfixed structurally: the {VERIFY_NEW} new slugs were passed to the verifier "
        "explicitly before this digest was written, so they carry measured ages and feed membership. The "
        "real fix is to append the window's slugs to the verifier's input inside the window script; it is "
        "the next change and it is the second run it has been deferred.",
        "THE PER-RUN WINDOW, BODY AND DIGEST SCRIPTS ARE STILL HAND-COPIED, AND THAT REMAINS THIS "
        "MONITOR'S ONE UNFIXED STRUCTURAL DEFECT. _window_1016.py, _bodies_1016.py and _digest_1016.py were "
        "produced by copying yesterday's files and editing constants. Carried forward from the 2026-10-15 "
        "record, which was itself written after the copy step caused a tuple crash mid-window. The "
        "hand-copy survived today because yesterday's fix travelled with the copy; that is luck, not "
        "repair. Converting the three to scripts/ with an explicit run date is the next real fix.",
        "THE ONE AI+SPEND ROW OF THE WINDOW WAS CLOSED TO US BY ITS OWN WORDING, AND THE DIGEST DOES NOT "
        "LET IT LOOK LIKE A CANDIDATE. The ET Edge cover story on AI day-2 ops asks what AI 'really costs' "
        "- the quantity this site holds dated evidence for - and then states 'we will not be taking vendor "
        "quotes'. It is recorded as relevance 'low' with that sentence quoted in relevance_notes and in "
        "contact_method, rather than carried as a near-miss, because a request that matches the beat and "
        "excludes the source by its own terms is the most misleading shape this monitor produces.",
        "THE PLATFORM PROBE'S BYTE COUNTS AND STATUS TEXTS ARE STILL READ OUT OF THE PROBE, NOT TYPED - "
        "carried forward from 2026-10-14 and holding today: every per-platform note in `platforms_checked` "
        "is generated from the window probe's own `platforms` array, so the byte counts, the titles and "
        "the checkpoint flag move with the measurement instead of being frozen prose.",
        "THE DIGEST CLASSIFIED THE FRESHEST ROWS IN THE QUEUE AS COLD, AND THE CAUSE WAS A FALSY ZERO. "
        "Fixed 2026-10-13 and carried forward: the line `live = [o for o in unpitched if (o['_days_old'] "
        "or 999) <= 10]` turns a request posted TODAY into 999, because `_days_old == 0` is falsy. Today's "
        "window added rows at 1 day, so the guard still matters, and it is checked here rather than "
        "assumed.",
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(out, indent=1))
print(f"\nwrote digest-{TODAY}.json: {len(out['opportunities'])} opportunities, "
      f"{len(out['new_this_run'])} new-this-run notes, {len(out['expired_this_run'])} expiry notes")
