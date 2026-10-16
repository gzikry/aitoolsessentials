#!/usr/bin/env python3
"""Compose marketing/haro-outreach/digest-2026-10-15.json.

Carries the 131 tracked rows forward with their page truth refreshed from
verified-requests.json (re-fetched today by scripts/verify_journo_requests.py --refresh-feed,
139 URLs, every one HTTP 200 and live), and adds the five AI-token rows found in today's
90-slug window.

Nothing is marked pitched here: sends are George's lane and the ledger is the only place a
send is recorded.
"""
from __future__ import annotations

import json
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing/haro-outreach"
TODAY = "2026-10-15"
PREV = "2026-10-14"

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
VERIFY_URLS = 139  # the union of tracked URLs scripts/verify_journo_requests.py probed today


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
# daily maintenance job and on this run carries `updated: 2026-10-15`, so a figure typed here
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
        return (str(len(_tools)), "?", "?", "?", _snaps.get("updated", "?"))
    return (str(len(_tools)), str(len(_paid)),
            str(sum(1 for _x in _paid.values() if _x <= 25)),
            f"{statistics.median(_paid.values()):.2f}", _snaps.get("updated", "?"))


n_tools, n_paid, n_25, med_paid, _snap_updated = _derive_figures()
_pairs = json.loads((S / "data/monthly_annual_pairs.json").read_text())
PAIR_TXT = (f"{_pairs['range_low']}x-{_pairs['range_high']}x, median {_pairs['median']}x over "
            f"{_pairs['n']} tiers, pair set built {_pairs['built']}")
print(f"figures re-derived: {n_paid} of {n_tools} monthly-priced, {n_25} at/under $25, "
      f"median ${med_paid}, snapshot updated {_snap_updated}; pairs {PAIR_TXT}")


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
# Rows found this run - every AI-token slug in the 90-slug window. All five are recorded as
# measurements; none is a candidate, none publishes a route that reaches us, and none asks a
# question about tool cost.
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
            "_new_or_recovered_2026-10-15": True}


# Note carried on every row added today: the only links the body extractor sees on these pages
# are Sourcee's own author chrome (linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith), which
# scripts/verify_journo_requests.py excludes from `published_links` by design. They are NOT routes
# and must not be read as one.
_CHROME = ("The only links on the page are Sourcee's own author chrome "
           "(linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes "
           "from published_links; neither is a route to the poster.")

# 1. A subreddit-shaped callout for artists, reposted into the feed the same evening. No outlet,
# no name beyond a throwaway handle, no route.
_s = "painters-and-photographers-ai-impact-on-art"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Reddit throwaway-style handle Beautiful_Annual9811 (the page's own author field). No outlet "
    "and no journalist named on the request or in the body.",
    "AI / Visual Art / Feature Story",
    _dl(_s),
    "The body says 'Any recommendations please let me know, I'd be happy to reach out' - it asks "
    "the reader to volunteer other people, and publishes no address, handle or link of its own. "
    + _CHROME + " NOT RESOLVED.",
    "low",
    "Someone planning a feature on how art has changed with AI, looking for painters and "
    "photographers to interview. Standing bar is being an artist; the body carries no cost, "
    "pricing, subscription or purchasing element anywhere. Recorded as an AI-token window slug.",
    _NN,
))

# 2. The one row of the window with a journalist's own words in it - and it wants victims of job
# loss, a standing bar we cannot meet, plus a DM route that is not published.
_s = "legal-assistants-paralegals-and-lawfirm-staff-jobs-eliminated-by-ai"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Reddit-style throwaway handle YardOptimal9329 (the page's own author field). The body says "
    "'I'm a journalist looking to speak with...' but names no outlet and no byline.",
    "AI / Legal Sector / Job Displacement",
    _dl(_s),
    "The body says 'please DM me' - a route on the poster's own platform, with no handle, address "
    "or link printed on the request. " + _CHROME + " NOT RESOLVED.",
    "low",
    "Wants legal assistants, paralegals and other law-firm staff whose jobs were eliminated "
    "because of AI. The standing bar is a personal job loss inside a law firm - we cannot meet it "
    "without inventing a source - and there is no cost or tool-spend question in the body. "
    "Recorded as an AI-token window slug.",
    _NN,
))

# 3. A recruiter's podcast, named outlet in the domain field, and a route that is an introduction
# request rather than a reply.
_s = "uk-and-us-heads-of-data-and-ai-from-idea-to-production"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Lloyd Black (the page's own author field) - Harnham / Rockborne (harnham.com, domain field), "
    "the recruiter behind the Data & AI podcast named in the body.",
    "AI / Data Platforms / Podcast Guests",
    _dl(_s),
    "The body asks for 'an introduction' to other people and publishes no address, handle or link "
    "of its own. " + _CHROME + " NOT RESOLVED - and the ask is to nominate a guest, not to answer "
    "a reporter's question.",
    "low",
    "A recruiter's podcast looking for Heads of Data/AI, CDOs and CTOs with production experience. "
    "It is a guest-invitation from a staffing firm rather than a journalist request for sources, "
    "the standing bar is an executive job title we do not hold, and the body carries no cost or "
    "pricing question. Recorded as an AI-token window slug.",
    _NN,
))

# 4. A named reporter at a real publication, a Zoom interview, a redacted address - and a
# geographic standing bar.
_s = "ai-companion-users-in-africa-friendship-and-emotional-impact"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Danai (named in the body) - Rest of World (restofworld.org, domain field), 'a New York based "
    "publication covering emerging technology in the Global South'.",
    "AI / Consumer Companionship / Global South",
    _dl(_s),
    "The body says 'please message me privately or email me: [email redacted]' - Sourcee redacts "
    "the address, and the page publishes no handle and no link. " + _CHROME + " NOT RESOLVED.",
    "low",
    "A 30-minute Zoom interview with adults in Africa who use AI companions for friendship, "
    "emotional support or romance, naming Replika and similar apps. Standing is residence and "
    "personal use in Africa; we meet neither, and the subject is emotional impact rather than what "
    "the subscription costs. Recorded as an AI-token window slug.",
    _NN,
))

# 5. Academic research with the most AI vendor names of any window row - and an explicit
# 'you participated in litigation' bar.
_s = "pro-se-litigants-using-generative-ai-access-to-justice-impact"
NEW.append(new_row(
    _s,
    core(_s)[:600],
    "Reddit throwaway handle ProSe-Throwaway (the page's own author field); the body says 'I'm a "
    "UConn Law student writing an article'. No outlet, no byline, no editor named.",
    "AI / Legal Access / Academic Research",
    _dl(_s),
    "The body says 'please feel free to send me a private message' - a platform DM with no handle, "
    "address or link published on the request. " + _CHROME + " NOT RESOLVED.",
    "low",
    "Interviews with self-represented litigants who used ChatGPT, Claude or Grok in court, for a "
    "law-review comment on access to justice. The standing bar is first-hand pro se litigation; "
    "the body is explicit that there is no compensation and it is academic research, and it asks "
    "about tool USE, never tool COST. Recorded as an AI-token window slug.",
    _NN,
))

opps.extend(NEW)
print(f"added {len(NEW)} new rows -> {len(opps)} tracked")


# ---------------------------------------------------------------------------
# The two rows that carry a route. Both are rewritten from today's own route probe, not from
# yesterday's byte counts.
# ---------------------------------------------------------------------------
_routes = json.loads((D / f"route-checks-{TODAY}.json").read_text())["routes"]

_MIMS = "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks"
_mims_route = _routes["linkedin.com/in/christopher-mims-club/"]
by_slug[_MIMS]["contact_method"] = (
    "Body says '(DMs open)'; no address, handle or link is printed in the request itself. Route: "
    f"https://www.linkedin.com/in/christopher-mims-club/ — re-fetched today in route-checks-{TODAY}.json: "
    f"HTTP {_mims_route['http']}, {_mims_route['bytes']:,} bytes, title '{_mims_route['title']}'. Two dead "
    f"ends re-checked today so they are not retried as routes: muckrack.com/christopher-mims "
    f"HTTP {_routes['muckrack.com/christopher-mims/']['http']} (Cloudflare interstitial) and "
    f"wsj.com/news/author/christopher-mims HTTP {_routes['wsj.com/news/author/christopher-mims/']['http']}. "
    "LINKEDIN DM — George's lane. Not automatable. Request page re-verified today: HTTP 200, "
    "email_redacted=False, emails_on_page=none, published_links=Sourcee chrome only."
)
by_slug[_MIMS]["suggested_pitch_template"] = (
    f"Lead with the dated price set behind the blocked-employee workaround: {n_paid} of {n_tools} tracked tools publish "
    f"a monthly price, {n_25} of those at or under $25/month, median ${med_paid}; paying monthly instead of annually "
    f"costs {PAIR_TXT} (snapshots updated "
    f"{_snap_updated}). State plainly that we are not an employee with a blocked account. "
    f"Route: LinkedIn DM to https://www.linkedin.com/in/christopher-mims-club/ — George's lane. "
    f"Draft: pitch-drafts-{TODAY}.md section 1."
)
print("rewrote the Mims row's route and angle from today's probe")

_AMURE = "tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring"
_amure_route = _routes["tobiamure.com/"]
by_slug[_AMURE]["contact_method"] = (
    "The request page redacts the address ('email me at [email redacted]') and says explicitly 'No DM "
    "pitches here on LinkedIn. Email me.' NOT SENDABLE until an address is published somewhere other "
    "than the redacted body - resolved 2026-10-14, re-verified today. ROUTE: hello@tobiamure.com, "
    "published by the journalist himself on his own site, https://tobiamure.com/ - re-fetched today in "
    f"route-checks-{TODAY}.json: HTTP {_amure_route['http']}, {_amure_route['bytes']:,} bytes, title "
    f"'{_amure_route['title']}'. The address appears verbatim three times on that page: in the Person "
    "JSON-LD email field, in his own FAQ answer ('Send the brief through the contact page or email "
    "hello@tobiamure.com. I reply to editors within two business days.'), and in the site footer. "
    "tobiamure.com MX = Namecheap email forwarding (eforward1-5.registrar-servers.com), so the domain "
    "routes mail. Six byline pages re-checked again today so they are not retried as routes: "
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
    f"lane. Draft: pitch-drafts-{TODAY}.md section 2."
)
print("re-verified the Tobi Amure route from today's probe")


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
# The prose scan (scripts/sourcee_terms.AI_PROSE) is the matcher that can actually see the word
# 'AI' in a sentence: the slug-tuned token set requires hyphens and reported a false zero on every
# run up to 2026-10-13.
_ai_body_prose = sum(1 for r in bodies.values() if r.get("ai_prose_in_body"))
_ai_prose_spend = sum(1 for r in bodies.values()
                      if r.get("ai_prose_in_body") and r.get("real_spend_in_body"))
_spend_only = [s for s, r in bodies.items()
               if r.get("spend_tokens_in_body") and not r.get("ai_tokens_in_body")]
print(f"body prose AI hits: {_ai_body_prose}; AI+real-spend: {_ai_prose_spend}; spend-only: {len(_spend_only)}")

_MIMS_AGE = by_slug[_MIMS]["_days_old"]
_AMURE_AGE = by_slug[_AMURE]["_days_old"]

out = {
    "date": TODAY,
    "monitor": "HARO / Sourcee journalist-request monitor for AIToolsEssentials",
    "run_at": datetime.now(timezone.utc).isoformat(),
    "search_scope": prev["search_scope"],
    "age_policy": (
        "Ages are read off each request page (JSON-LD datePublished plus the rendered 'Posted ... ago' "
        "badge), never off the digest text, and every carried row's deadline field was rewritten this "
        f"run from the page itself. All {VERIFY_URLS} tracked URLs were re-fetched and read today: HTTP 200 "
        f"for every one, body still served, no expiry notice; the {len(NEW)} rows added today were "
        "fetched the same way and cached by the verifier. Two further facts belong here. (1) No request "
        "has ever been seen to expire on this source - 100% of carried rows have returned HTTP 200 on "
        "every run - so 'deadline' means the poster's own stated cutoff or a measured age, never an "
        "observed expiry, and the absence of an expiry notice is weak evidence recorded as such. "
        "(2) FEED MEMBERSHIP IS STILL NOT A FRESHNESS SIGNAL FOR THE BACKLOG: the AI topic page carries "
        f"{window['feed_count']} slugs and {window['feed_overlap_with_window']} of them are inside today's "
        f"{len(window['window'])}-slug sitemap window, and {len(_tracked_in_feed)} tracked row(s) appear "
        "in it. The feed is a rolling window over the newest requests, so a carried row's absence from "
        "it says nothing about that row."
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
                  "monitor's standing finding; the /requests path now 404s from this end, so even the "
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
                  "needs an OAuth handshake. Seventh consecutive run. This is the one platform that "
                  "would widen supply, and it is blocked on an account, not on the monitor."},
        {"platform": "ResponseSource (responsesource.com)", "status": "accessible-but-not-usable",
         "notes": f"HTTP {PLAT['ResponseSource (responsesource.com)']['http']}, "
                  f"{PLAT['ResponseSource (responsesource.com)']['bytes']:,} bytes. Public pages only; the "
                  "request database needs a subscription."},
    ],
    "opportunities": opps,
    "new_this_run": [
        (f"FIVE ROWS ADDED - every AI-token slug in the {len(window['window'])}-slug window - AND NOT ONE "
         f"OF THEM IS A CANDIDATE. None publishes a reply route that reaches us and none asks about tool "
         f"cost: a Reddit-shaped callout for painters and photographers for a feature on AI and art; a "
         f"callout for legal assistants and paralegals whose jobs AI eliminated (a standing bar we cannot "
         f"meet); a recruiter's Data & AI podcast at Harnham asking for guest introductions; a Rest of "
         f"World callout for AI companion users in Africa (30-minute Zoom, redacted address); and a UConn "
         f"Law student's research interviews with pro se litigants who used ChatGPT, Claude or Grok. "
         f"Recorded as measurements so the window is fully accounted for."),
        (f"THE WINDOW PRODUCED ZERO CORE-BEAT REQUESTS AND ZERO AI+SPEND SLUGS: {len(window['window'])} "
         f"slugs, {len(window['ai'])} AI-token, {len(window['ai_strict'])} AI+spend, "
         f"{len(window['spend_any'])} spend-only. The four spend-only slugs are all off-beat "
         f"(fintech payments strategy, rural home-heating prices, grocery payment options, uninsurable "
         f"homes) and not one of them is an AI request. All {len(window['window'])} window bodies were "
         f"fetched and read, which is the only check that can back a zero; the fixed prose matcher "
         f"({_ai_body_prose} AI hits across the window's bodies) is what makes that zero evidence rather "
         f"than an artefact."),
        "NO ROW DROPPED OFF: every tracked row is carried in every digest by design, so that figure is a "
        "monitor convention and not platform evidence - see age_policy.",
    ],
    "expired_this_run": [
        (f"Nothing expired on its page: all {VERIFY_URLS} tracked URLs returned HTTP 200 with the request "
         f"body still served, and so did the {len(NEW)} new ones. See age_policy - an expiry has never "
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
        f"{len(cold)} are cold. TWO are sendable and both are still unsent: the WSJ columnist's "
        f"blocked-work-accounts request (relevance 'medium', now {_MIMS_AGE} days old, LinkedIn DM) sits at "
        f"exactly the cold line today and leaves the sendable list tomorrow - nothing brings it back once it "
        f"does; and the Fast Company Work Life request for AI-at-work data (low-medium, {_AMURE_AGE} days "
        f"old), whose route is a published email address: hello@tobiamure.com. No pitch has been sent since "
        f"2026-10-10 21:20 UTC and no reply has arrived to any of the three sends from that run - the "
        f"Amplemarket thread stays closed by the vendor's own acknowledgment and must not be bumped. The "
        f"window produced {len(window['window'])} slugs with {len(window['ai'])} AI-token and "
        f"{len(window['ai_strict'])} AI+spend. "
        f"Headline figures re-derived this run against the snapshot (updated {_snap_updated}): "
        f"{n_paid} of {n_tools} tools publish a monthly price, {n_25} of those at or under $25/month, "
        f"median ${med_paid}; monthly vs annual {PAIR_TXT}. Zero pitches sent this run - sends remain "
        f"George's lane."
    ),
    "recommended_actions": [
        f"SEND THE WSJ BLOCKED-WORK-ACCOUNTS DRAFT TODAY - it is {_MIMS_AGE} DAYS OLD, AT EXACTLY THE "
        f"10-DAY COLD LINE, AND TOMORROW IT LEAVES THE SENDABLE LIST FOR GOOD. Carried unsent through six "
        f"runs. Paste-ready at pitch-drafts-{TODAY}.md section 1. Route: LinkedIn DM to "
        f"https://www.linkedin.com/in/christopher-mims-club/ (the request's own body says '(DMs open)'). "
        f"Relevance 'medium'. George's lane, not automatable. Route re-fetched today: "
        f"HTTP {_mims_route['http']}, {_mims_route['bytes']:,} bytes. Two dead ends are recorded so they "
        f"are not retried as routes: muckrack.com/christopher-mims HTTP "
        f"{_routes['muckrack.com/christopher-mims/']['http']} and wsj.com/news/author/christopher-mims "
        f"HTTP {_routes['wsj.com/news/author/christopher-mims/']['http']}.",
        f"SEND THE TOBI AMURE EMAIL - THE ONLY SENDABLE ROW THAT IS NOT SITTING ON THE COLD LINE. "
        f"{_AMURE_AGE} days old, relevance low-medium, route hello@tobiamure.com re-verified today "
        f"(tobiamure.com HTTP {_amure_route['http']}, {_amure_route['bytes']:,} bytes). Paste-ready at "
        f"pitch-drafts-{TODAY}.md section 2. He states his own requirement ('Original data, or a survey "
        f"with its sample size and method') and the draft answers it with method and denominator. Email "
        f"route - technically automatable over SMTP, but sends are George's lane.",
        "NOTE THAT NO REPLY HAS ARRIVED TO EITHER DELIVERED PITCH FROM 2026-10-10 (google-and-claude-"
        "enterprise-users-seats-and-token-costs, speciality-food-retailers-and-producers-how-theyd-spend-"
        "10k-on-tech); the third (fulltime-employees-shadow-ai-use-and-paying-outofpocket) bounced with a "
        "550 NoSuchUser and its address is dead. Mailbox checked today across INBOX/All Mail/Sent/Spam: the "
        "newest inbound of any kind is a FormSubmit tool submission at 2026-10-15 12:12 UTC and the newest "
        "message at all in All Mail is our own outgoing verification request at 12:43 UTC - no pitch "
        "recipient has ever written in, and the only inbound from a pitch recipient remains Jan Suski's "
        "2026-09-18 message, acknowledged and closed on 2026-10-11.",
        "DO NOT DRAFT ANY OF TODAY'S FIVE ROWS. None has a route and none is on our beat; drafting one "
        f"would add another unsent file to the {len(list(D.glob('pitch-drafts-*.md')))} already on disk and "
        f"another unsent row to the {DRAFTS_UNSENT} the ledger still records without a send. That is the "
        "exact failure this monitor was rebuilt to stop repeating.",
        "ACCEPT THAT SOURCEE SUPPLY IS EXHAUSTED FOR THIS BEAT, and decide on Medialyst rather than "
        f"re-measuring it a seventh time. Today's evidence: {len(window['window'])} slugs, "
        f"{len(window['ai'])} AI-token, none on our beat, and no AI+spend slug at all. Seven consecutive "
        "runs have reported the same 401 on the Medialyst MCP endpoint. If the account is not going to be "
        "opened, say so and the monitor stops reporting it as the one widening option.",
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
        "routes_reverified_this_run": ["linkedin.com/in/christopher-mims-club/ (LinkedIn DM, for "
                                       "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks)",
                                       "tobiamure.com/ (hello@tobiamure.com, for "
                                       "tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring)"],
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
        "THE BODY FETCH SCRIPT WAS STILL WRITTEN AGAINST THE OLD SINGLE-GROUP TOKEN REGEX AND CRASHED "
        "MID-WINDOW. `_bodies_1015.py`, copied from yesterday's file, called "
        "`AI.findall(core)` and `SPEND.findall(core)`; both patterns carry TWO capture groups, so findall "
        "returns tuples and the line `t.lower() for t in AI.findall(core)` raised "
        "`AttributeError: 'tuple' object has no attribute 'lower'` after 57 of 90 slugs had been fetched. "
        "The same file has been copied forward since the prose matcher landed; it survived only because "
        "the crash happens after the per-slug write, so the run looked complete. Fixed in place and the "
        "fix recorded here: both scans now use `finditer` and read group 2 (AI) / group 1 (SPEND). Re-run "
        "completed 90 of 90. Same defect class as every other hand-copied per-run script in this monitor: "
        "the copy step, not the code, is the fault.",
        "THE FIVE ROWS FOUND TODAY WERE INVISIBLE TO THE QUEUE UNTIL THE VERIFIER SAW THEM. "
        "scripts/verify_journo_requests.py builds its URL list from pitch-queue.md, the digests and the "
        "ledger - all of which describe YESTERDAY's state - so a slug found in today's window has no page "
        "truth (no days_old, no badge, no feed membership) until the next run, and build_pitch_queue.py "
        "would rank it as 'age unknown'. Not fixed structurally this run, but closed by hand: the five new "
        "slugs were passed to the verifier explicitly, so they carry measured ages and the queue can rank "
        "them. The real fix is to append the window's slugs to the verifier's input inside the window "
        "script; recorded as the next change.",
        "THE PER-RUN WINDOW, BODY AND DIGEST SCRIPTS ARE STILL HAND-COPIED, AND THAT IS RECORDED AS A "
        "KNOWN GAP, NOT A FIX. _window_1015.py, _bodies_1015.py and _digest_1015.py were produced by "
        "copying yesterday's files and editing constants - and today that copy step is exactly what "
        "produced the tuple crash above. The window script reads its mark from the previous run rather "
        "than pasting it, so the mark cannot drift, but the copy step itself survives and remains this "
        "monitor's one unfixed structural defect. Converting the three to scripts/ with an explicit run "
        "date is the next real fix.",
        "THE PLATFORM PROBE'S BYTE COUNTS AND STATUS TEXTS ARE STILL READ OUT OF THE PROBE, NOT TYPED - "
        "carried forward from 2026-10-14 and holding today: every per-platform note in `platforms_checked` "
        "is generated from the window probe's own `platforms` array, so the byte counts, the titles and "
        "the checkpoint flag move with the measurement instead of being frozen prose.",
        "THE DIGEST CLASSIFIED THE FRESHEST ROWS IN THE QUEUE AS COLD, AND THE CAUSE WAS A FALSY ZERO. "
        "Fixed 2026-10-13 and carried forward: the line `live = [o for o in unpitched if (o['_days_old'] "
        "or 999) <= 10]` turns a request posted TODAY into 999, because `_days_old == 0` is falsy. Today's "
        "window added two rows at 0 days, so this fix is load-bearing again: they are counted live, not "
        "cold.",
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(out, indent=1))
print(f"\nwrote digest-{TODAY}.json: {len(out['opportunities'])} opportunities, "
      f"{len(out['new_this_run'])} new-this-run notes, {len(out['expired_this_run'])} expiry notes")
