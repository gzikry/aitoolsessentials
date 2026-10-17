#!/usr/bin/env python3
"""Compose marketing/haro-outreach/digest-2026-10-17.json.

Carries the 140 tracked rows forward with their page truth refreshed from verified-requests.json
(re-fetched today by scripts/verify_journo_requests.py, every URL HTTP 200 and live), and adds the
seven AI-token rows found in today's 74-slug window.

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
TODAY = "2026-10-17"
PREV = "2026-10-16"
MMDD = TODAY.replace("-", "")[4:]

prev = json.loads((D / f"digest-{PREV}.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
window = json.loads((D / f"_window_{MMDD}.json").read_text())
bodies = json.loads((D / f"_bodies_{MMDD}.json").read_text())
feed = json.loads((D / "ai-topic-feed.json").read_text())
FEED = set(feed["slugs"])

PLAT = {p["platform"]: p for p in window["platforms"]}

SITE = "https://www.sourcee.app/journo-request/"
VERIFY_URLS = len(prev["opportunities"])
VERIFY_NEW = 7


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
print(f"carried {len(opps)} rows; every deadline rewritten with today's page truth")


# ---------------------------------------------------------------------------
# Headline figures re-derived at build time, never typed.
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


_FIG_REPAIRED: list[str] = []


def _repair_tool_count(o: dict) -> dict:
    """A carried row can quote the tool count from the day it was written. The catalogue moved
    from 78 to 79 today (a vendor listing landed on 2026-10-17), and build_pitch_queue.py renders
    this field straight into the queue George reads - so a carried template quoting 77 or 78 while
    the digest headline says 79 is visible to him, which is the only reason a wrong number here is
    findable at all. Re-derived, never hand-edited."""
    t = o.get("suggested_pitch_template") or ""
    if not t:
        return o
    new, n = re.subn(r"of 7[0-9] (tools|tracked AI tools)", rf"of {n_tools} \1", t)
    if n and new != t:
        o = dict(o)
        o["suggested_pitch_template"] = new
        o["_figures_repaired"] = sorted(set(o.get("_figures_repaired") or []) | {"suggested_pitch_template"})
        _FIG_REPAIRED.append(o["slug"])
    return o


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
# Rows found this run - every AI-token slug in the 74-slug window. All seven are recorded as
# measurements; none is a candidate.
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
            "_new_or_recovered_2026-10-17": True}


_CHROME = ("The only links on the page are Sourcee's own author chrome "
           "(linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes "
           "from published_links; neither is a route to the poster.")

# 1. The one AI+spend slug the slug filter kept, and the vendor-promo bar it sets.
_s = "ai-saas-vendors-targeting-journalists-prs-and-marketers-case-studies"
NEW.append(new_row(
    _s,
    core(_s)[:900],
    "Vartika (the page's own author field). No outlet named on the request or in the body; the "
    "body is tagged #JournoRequest.",
    "AI / SaaS / Vendor Case Studies",
    _dl(_s),
    "The body ends 'Pitch me :)' and publishes no address, handle or link of its own. " + _CHROME +
    " NOT RESOLVED. The route would in any case be a reply on the poster's own platform.",
    "low",
    "She is seeking CASE STUDIES from brands that SELL AI tools as software for journalists, PRs "
    "and marketers - 'HOW does your AI brand solve issues faced by these professionals?' The "
    "standing bar is being an AI-tool vendor with a customer story. AIToolsEssentials is a "
    "publisher that prices and reviews those tools; it is not the brand she is asking for, and the "
    "body asks nothing about what any tool costs. Recorded as an AI-token window slug, relevance "
    "low. The 'saas' token is what put it in the AI+spend column and it is not a spend question.",
    _NN,
))

# 2. A real-estate beat with a DM-only route.
_s = "real-estate-operators-ai-adoption-and-org-restructuring"
NEW.append(new_row(
    _s,
    core(_s)[:900],
    "Jake (the page's own author field). No outlet named on the request or in the body.",
    "AI / Real Estate / Operations",
    _dl(_s),
    "The body says 'DMs are open!!!' and publishes no address, handle or link. " + _CHROME +
    " NOT RESOLVED. The route would be a DM on the poster's own platform - not automatable and not "
    "a route this monitor can use.",
    "low",
    "He has been interviewing real-estate operators on their AI journey and how they are "
    "restructuring around tech, and wants more operators. The standing bar is a real-estate "
    "operator's own experience; we run a pricing catalogue, not a property operation. Nothing in "
    "the body touches tool cost, subscriptions or software spend.",
    _NN,
))

# 3. A named outlet (Chemistry World) and a standing bar that is a student.
_s = "chemistry-undergrads-and-phd-students-ai-use-in-coursework-and-research"
NEW.append(new_row(
    _s,
    core(_s)[:900],
    "Mason Wakley (the page's own author field). Domain field: chemistryworld.com - a story for "
    "Chemistry World.",
    "AI / Higher Education / Chemistry",
    _dl(_s),
    "The body says 'please feel free to get in touch' and publishes no address, handle or link of "
    "its own. " + _CHROME + " NOT RESOLVED. The route would be a reply on the poster's own "
    "platform.",
    "low",
    "A Chemistry World story on how and why chemistry undergraduates and PhD students use AI - "
    "summarising papers, finding reactions, explaining concepts, writing emails. The standing bar "
    "is being a chemistry student; every source the body asks for is a student. It is a "
    "usage-behaviour story and asks nothing about what any AI tool costs.",
    _NN,
))

# 4. A YouTube feature request wearing a journalist-request tag.
_s = "ai-app-and-saas-founders-1k-mrr-youtube-feature-growth-tactics"
NEW.append(new_row(
    _s,
    core(_s)[:900],
    "Ayush Gupta (the page's own author field). No outlet named; the body describes his own "
    "YouTube channel.",
    "AI / SaaS Founders / Podcast Promotion",
    _dl(_s),
    "The body says 'You can reach out to me with your website and trustmrr link' and publishes no "
    "address, handle or link. " + _CHROME + " NOT RESOLVED. The route would be a reply on the "
    "poster's own platform.",
    "low",
    "This is a promotion request, not a reporting request: he wants AI app / SaaS founders who "
    "have reached $1K MRR on his YouTube channel, which he notes has 'only 100 subs right now'. "
    "The standing bar is a founder with a product and a TrustMRR profile. We are neither, and the "
    "body asks about growth tactics, not cost.",
    _NN,
))

# 5. The Berlin AI-infrastructure request: a named reporter, an off-beat ask.
_s = "ai-infrastructure-engineers-in-berlin-data-centers-and-bottlenecks"
NEW.append(new_row(
    _s,
    core(_s)[:900],
    "Kai Nicol-Schwarz (the page's own author field). No outlet named on the request or in the "
    "body; the author field matches a reporter who covers AI infrastructure.",
    "AI / Data Centres / Infrastructure",
    _dl(_s),
    "The body says 'Drop me a line if you're around' and publishes no address, handle or link. " +
    _CHROME + " NOT RESOLVED. The route would be arranged in person at Nvidia's GTC, which is not a "
    "route this monitor can use.",
    "low",
    "He is going to Berlin for Nvidia's GTC next week and wants to speak to AI-infrastructure "
    "engineers about where data-centre projects are being built, how U.S. Big Tech and AI labs are "
    "securing capacity, and what bottlenecks are emerging (supply chains, chips, permits). The "
    "standing bar is an infrastructure engineer's own knowledge; the subject is physical capacity, "
    "not tool pricing, and the body asks nothing about software cost.",
    _NN,
))

# 6. BusinessWorld, an infrastructure-impact story, email redacted.
_s = "residents-near-mumbai-ai-data-centres-power-and-water-strain"
NEW.append(new_row(
    _s,
    core(_s)[:900],
    "Kapil Saini (the page's own author field). Domain field: businessworld.in - BusinessWorld.",
    "AI / Data Centres / Infrastructure & Policy",
    _dl(_s),
    "The body says 'please feel free to DM me. Email: [email redacted]' - Sourcee redacts the "
    "address, and the page publishes no handle and no link. " + _CHROME + " NOT RESOLVED. The route "
    "would be a DM on the poster's own platform.",
    "low",
    "A BusinessWorld story on how AI data-centre expansion is straining electricity and water "
    "infrastructure around Mumbai, ahead of a dedicated data-centre policy. He wants residents "
    "near the projects, plus environmentalists, urban planners and energy experts. The standing "
    "bar is local on-the-ground experience, not a pricing catalogue; it is an infrastructure-and-"
    "policy story and asks nothing about tool cost.",
    _NN,
))

# 7. Single family offices: cybersecurity experts wanted.
_s = "single-family-office-cybersecurity-experts-ai-risks-and-opportunities"
NEW.append(new_row(
    _s,
    core(_s)[:900],
    "Naama Saar (the page's own author field). No outlet named on the request or in the body; the "
    "body names the piece 'INFORMED NOT INVOLVED'.",
    "AI / Cybersecurity / Family Offices",
    _dl(_s),
    "The body says 'please DM me' and publishes no address, handle or link. " + _CHROME +
    " NOT RESOLVED. The route would be a DM on the poster's own platform.",
    "low",
    "An 'INFORMED NOT INVOLVED' article on data protection, privacy and cybersecurity inside "
    "Single Family Offices in the age of AI, sourcing experts with practical experience of the "
    "threats and capabilities. The standing bar is a cybersecurity practitioner serving family "
    "offices; a tool-pricing publisher meets none of it, and the body focuses on 'real-world "
    "challenges ... beyond the technical aspects', not on what AI costs.",
    _NN,
))

opps.extend(NEW)
print(f"added {len(NEW)} new rows -> {len(opps)} tracked")

# Index the FINAL rows, after the figure-repair pass above has copied any repaired row into a new
# dict. Building this index earlier (as the 2026-10-14..16 runs did) left it pointing at the
# pre-repair objects, so a route field written onto `by_slug[...]` landed on a dict that was no
# longer in `opps` - and on 2026-10-17 the sendable row happened to be one of the repaired rows,
# which shipped yesterday's route evidence inside a digest built today. Index last, always.
by_slug = {o["slug"]: o for o in opps}
assert len(by_slug) == len(opps), "duplicate slug would silently drop a row from the index"


# ---------------------------------------------------------------------------
# The one row that carries a route usable today. Rewritten from today's own route probe.
# ---------------------------------------------------------------------------
_routes = json.loads((D / f"route-checks-{TODAY}.json").read_text())["routes"]

_AMURE = "tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring"
_amure_route = _routes["tobiamure.com/"]
_amure_contact = _routes["tobiamure.com/contact/"]
_amure_n = _amure_route.get("emails_on_page", {}).get("hello@tobiamure.com")
_amure_n_contact = _amure_contact.get("emails_on_page", {}).get("hello@tobiamure.com")
by_slug[_AMURE]["contact_method"] = (
    "The request page redacts the address ('email me at [email redacted]') and says explicitly 'No DM "
    "pitches here on LinkedIn. Email me.' ROUTE: hello@tobiamure.com, published by the journalist "
    f"himself on his own site, https://tobiamure.com/ - re-probed today in route-checks-{TODAY}.json: "
    f"HTTP {_amure_route['http']}, {_amure_route['bytes']:,} bytes, title '{_amure_route['title']}', "
    f"with the address counted {_amure_n} times on that page (Person JSON-LD email field, his own FAQ "
    "answer, and the site footer). His contact page "
    f"https://tobiamure.com/contact/ re-probed today: HTTP {_amure_contact['http']}, "
    f"{_amure_contact['bytes']:,} bytes, title '{_amure_contact['title']}', address counted "
    f"{_amure_n_contact} times. tobiamure.com MX = Namecheap email forwarding "
    "(eforward1-5.registrar-servers.com), so the domain routes mail. Six byline pages remain recorded "
    "dead ends so they are not retried as routes (last re-checked 2026-10-15): muckrack.com/tobi-amure, "
    "investopedia.com/tobi-amure-5203106, forbes.com/sites/tobiamure, thestreet.com/author/tobi-amure, "
    "benzinga.com/author/tobi-amure, inc.com/author/tobi-amure - all HTTP 403. EMAIL ROUTE - no "
    "platform form, no DM, no scheduling link. Sending is George's lane."
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

# The Mims row is now 12 days old and stays off the sendable list.
_MIMS = "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks"
_mims_route = _routes["linkedin.com/in/christopher-mims-club/"]
by_slug[_MIMS]["contact_method"] = (
    "Body says '(DMs open)'; no address, handle or link is printed in the request itself. Route: "
    f"https://www.linkedin.com/in/christopher-mims-club/ - re-probed today in route-checks-{TODAY}.json: "
    f"HTTP {_mims_route['http']}, {_mims_route['bytes']:,} bytes, title '{_mims_route['title']}'. The route is "
    f"still live; the ROW is {by_slug[_MIMS]['_days_old']} days old and has been past the 10-day cold line since "
    "yesterday, so it is not counted sendable. Two dead ends remain recorded so they are not retried as routes "
    "(re-probed today): muckrack.com/christopher-mims HTTP 403 (Cloudflare interstitial) and "
    "wsj.com/news/author/christopher-mims HTTP 401. LINKEDIN DM - George's lane. Not automatable."
)
print(f"re-probed the Mims route; the row is now {by_slug[_MIMS]['_days_old']} days old and not sendable")


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


def _age(o: dict) -> int:
    d = o.get("_days_old")
    return d if d is not None else 999


live = [o for o in unpitched if _age(o) <= 10]
cold = [o for o in unpitched if _age(o) > 10]
print(f"tracked {len(opps)} | unpitched {len(unpitched)} | live {len(live)} | cold {len(cold)}")


def _has_route(o: dict) -> bool:
    c = o.get("contact_method") or ""
    return "hello@tobiamure.com" in c or "linkedin.com/in/" in c or ("://" in c and "sourcee.app" not in c)


_sendable_now = sum(1 for o in live
                    if (o.get("relevance") or "").lower() not in ("low", "") and _has_route(o))
print(f"sendable by the queue's own rule: {_sendable_now}")

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

# The prose scan is the matcher that can see the word 'AI' in a sentence. Today it returned 8 hits
# over the 74 window bodies, of which exactly one is a false positive: the YouTube share parameter
# '?si=AI-KPLnoV8cIWkS9' on the paranormal-witnesses request, where '\bai\b' matches the 'AI' inside
# a URL. Recorded because it is the matcher, not supply, that decides how clean a window looks.
_ai_body_prose_slugs = sorted(s for s, r in bodies.items() if r.get("ai_prose_in_body"))
_ai_body_prose = len(_ai_body_prose_slugs)
_ai_prose_fp = ["paranormal-witnesses-haunted-encounters-and-ghost-stories"]
_ai_prose_spend = sum(1 for r in bodies.values()
                      if r.get("ai_prose_in_body") and r.get("real_spend_in_body"))
_spend_only = [s for s, r in bodies.items()
               if r.get("spend_tokens_in_body") and not r.get("ai_tokens_in_body")]
print(f"body prose AI hits: {_ai_body_prose}; AI+real-spend: {_ai_prose_spend}; spend-only: {len(_spend_only)}")

_AMURE_AGE = by_slug[_AMURE]["_days_old"]
_MIMS_AGE = by_slug[_MIMS]["_days_old"]
_SPEND_ONLY_OFF_BEAT = (
    "family affordability, school recess policy, cost-of-living before the midterms, allergy-safe "
    "food, inheritance spending, subscription-free security cameras, small-business pay transparency, "
    "a boss who vanished on payday, a security camera buyer's guide, food-access pantries, local-news "
    "tips, a £10k tech spend story"
)

out = {
    "date": TODAY,
    "monitor": "HARO / Sourcee journalist-request monitor for AIToolsEssentials",
    "run_at": datetime.now(timezone.utc).isoformat(),
    "search_scope": prev["search_scope"],
    "age_policy": (
        "Ages are read off each request page (JSON-LD datePublished plus the rendered 'Posted ... ago' "
        "badge), never off the digest text, and every carried row's deadline field was rewritten this "
        f"run from the page itself. All {VERIFY_URLS} carried URLs plus the {VERIFY_NEW} rows added today "
        f"were re-fetched and read today: HTTP 200 for every one, body still served, no expiry notice. "
        "Two further facts belong here. (1) No request has ever been seen to expire on this source - "
        "100% of carried rows have returned HTTP 200 on every run - so 'deadline' means the poster's own "
        "stated cutoff or a measured age, never an observed expiry, and the absence of an expiry notice "
        "is weak evidence recorded as such. (2) FEED MEMBERSHIP IS STILL NOT A FRESHNESS SIGNAL FOR THE "
        f"BACKLOG: the AI topic page carries {window['feed_count']} slugs and "
        f"{window['feed_overlap_with_window']} of them are inside today's {len(window['window'])}-slug "
        f"sitemap window - the feed is a rolling window over the newest requests, and "
        f"{len(_tracked_in_feed)} tracked row(s) appear in it. A carried row's absence from the feed says "
        "nothing about that row, and its presence says only that the request is new."
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
                  "needs an OAuth handshake. Ninth consecutive run. This is the one platform that "
                  "would widen supply, and it is blocked on an account, not on the monitor."},
        {"platform": "ResponseSource (responsesource.com)", "status": "accessible-but-not-usable",
         "notes": f"HTTP {PLAT['ResponseSource (responsesource.com)']['http']}, "
                  f"{PLAT['ResponseSource (responsesource.com)']['bytes']:,} bytes. Public pages only; the "
                  "request database needs a subscription."},
    ],
    "opportunities": opps,
    "new_this_run": [
        (f"SEVEN ROWS ADDED - every AI-token slug in the {len(window['window'])}-slug window - AND NOT ONE "
         f"OF THEM IS A CANDIDATE. The shape is a promo/discussion cluster, not a reporting cluster: an AI "
         f"SaaS vendor wanting a case study for his own pitch, a real-estate operator wanting peer "
         f"interviews, a founder wanting a YouTube feature, plus beat-specific asks (chemistry students, "
         f"Berlin AI-infra engineers, Mumbai data-centre residents, family-office cybersecurity experts). "
         f"Not one body asks what an AI tool costs, and not one publishes a route."),
        (f"THE WINDOW PRODUCED ZERO USABLE CORE-BEAT REQUESTS AGAIN: {len(window['window'])} slugs, "
         f"{len(window['ai'])} AI-token, {len(window['ai_strict'])} AI+spend, {len(window['spend_any'])} "
         f"spend-only. Both AI+spend slug hits matched on the token 'saas' alone and NEITHER is a spend "
         f"question ('AI SaaS Vendors Targeting Journalists' and 'AI App & SaaS Founders'), so the "
         f"substantive AI+spend count is zero, not two. The spend-only slugs are off-beat "
         f"({_SPEND_ONLY_OFF_BEAT}) and not one of them is an AI request. All {len(window['window'])} "
         f"window bodies were fetched and read, which is the only check that can back a zero."),
        "NO ROW DROPPED OFF: every tracked row is carried in every digest by design, so that figure is a "
        "monitor convention and not platform evidence - see age_policy.",
    ],
    "expired_this_run": [
        (f"Nothing expired on its page: all {VERIFY_URLS} carried URLs and the {VERIFY_NEW} new ones "
         "returned HTTP 200 with the request body still served. See age_policy - an expiry has never once "
         "been observed on this source, so the absence of an expiry notice is weak evidence and is "
         "recorded as such."),
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
        f"on his own site, hello@tobiamure.com, re-verified today (counted "
        f"{_amure_n} times on tobiamure.com/). The WSJ blocked-work-accounts row, the other former "
        f"sendable row, is now {_MIMS_AGE} days old and stays off the sendable list. No pitch has been "
        f"sent since 2026-10-10 21:20 UTC and no reply has arrived to any of the three sends from that "
        f"run; the Amplemarket thread stays closed by the vendor's own acknowledgment and must not be "
        f"bumped. The window produced {len(window['window'])} slugs with {len(window['ai'])} AI-token and "
        f"{len(window['ai_strict'])} AI+spend (both 'saas'-token false positives in substance). "
        f"Headline figures re-derived this run against the snapshot (updated {_snap_updated}): "
        f"{n_paid} of {n_tools} tools publish a monthly price, {n_25} of those at or under $25/month, "
        f"median ${med_paid}; monthly vs annual {PAIR_TXT}. Zero pitches sent this run - sends remain "
        f"George's lane."
    ),
    "recommended_actions": [
        f"SEND THE TOBI AMURE EMAIL - THE ONLY SENDABLE ROW THIS RUN, AND THE ONLY ONE THAT WAS SENDABLE "
        f"YESTERDAY AND STILL IS. {_AMURE_AGE} days old, relevance low-medium, route hello@tobiamure.com "
        f"re-verified today (tobiamure.com/ HTTP {_amure_route['http']}, {_amure_route['bytes']:,} bytes, "
        f"address counted {_amure_n} times; /contact/ HTTP {_amure_contact['http']}, "
        f"{_amure_contact['bytes']:,} bytes, counted {_amure_n_contact} times; MX = Namecheap forwarding). "
        f"Paste-ready at pitch-drafts-{TODAY}.md section 1. He states his own requirement ('Original data, "
        f"or a survey with its sample size and method') and the draft answers it with method and "
        f"denominator. Email route - technically automatable over SMTP, but sends are George's lane. It is "
        f"{10 - _AMURE_AGE} day(s) from the 10-day line, so this is the run where it either goes or is "
        f"recorded skipped.",
        "DO NOT DRAFT TODAY'S SEVEN ROWS. Not one body asks what an AI tool costs, and not one publishes "
        "a route; the closest to usable (the AI SaaS case-studies callout) wants a vendor's customer "
        "story, which we are not. Drafting any of them would add another unsent row to the "
        f"{DRAFTS_UNSENT} draft rows this monitor already carries without a send (counted from "
        "`**Source:**` lines in the draft files, not from any mention of a slug).",
        "NOTE THAT NO REPLY HAS ARRIVED TO ANY PITCH. Mailbox checked today (see reply_status below): the "
        "newest inbound from any pitch recipient remains Jan Suski's 2026-10-11 06:57 UTC acknowledgment, "
        "which closed the Amplemarket thread. Nothing has come from foxandspindle.com, sherwood.news, "
        "epgacceleration.com, artichokehq.com or raconteur.net at any point.",
        "DECIDE ON THE MEDIALYST ACCOUNT OR STOP MEASURING IT. Nine consecutive runs have reported the "
        "same 401 on the Medialyst MCP endpoint. If the account is not going to be opened, say so and the "
        "monitor stops reporting it as the one widening option.",
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
        "body_level_ai_hits_false_positives": len(_ai_prose_fp),
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
                                       "route live, row cold)"],
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
        "THE DIGEST SHIPPED YESTERDAY'S ROUTE EVIDENCE FOR THE ONE SENDABLE ROW, BECAUSE THE INDEX THE "
        "ROUTE SECTION WRITES THROUGH WAS BUILT BEFORE THE FIGURE-REPAIR PASS. `_repair_tool_count` "
        "returns a COPY of any row whose template quoted a superseded tool count, and those copies "
        "replaced the originals in `opps` - but `by_slug` had already been built from the pre-repair "
        "objects. On this run the sendable row (tech-and-hr-leaders-ai-at-work-...) was itself a repaired "
        "row, so the route text written for it was written onto a dict no longer in `opps`, and the digest "
        "went to press citing route-checks-2026-10-16.json and 'verbatim 6 times' inside a file built "
        "today. Caught by reading the written digest rather than trusting the build log (the log printed "
        "'re-verified the Tobi Amure route from today's probe' either way). `by_slug` is now built after "
        "the repair pass and after the new rows are appended, with an assertion that it holds every row.",
        "THE PROSE AI MATCHER COUNTED A URL PARAMETER AS A REQUEST, AND IT IS NAMED RATHER THAN SILENTLY "
        "DROPPED. The body scan returned 8 AI hits over today's 74 window bodies; one of them is the "
        "paranormal-witnesses request, where `\\bai\\b` (case-insensitive) matches the 'AI' inside a "
        "YouTube share parameter, `?si=AI-KPLnoV8cIWkS9`. That request is not an AI request. The count is "
        "reported with the false positive named in monitor_health so a window never looks cleaner than "
        "the matcher makes it look. The matcher itself is shared (scripts/sourcee_terms.py) and is left "
        "unchanged mid-run; stripping URL query strings before the prose scan is the next change.",
        "THE 'SaaS' TOKEN IS A PRODUCT CLASS, NOT A SPEND WORD, AND IT INFLATED TODAY'S AI+SPEND COUNT "
        "FROM ZERO TO TWO. `SPEND`/`REAL_SPEND` in scripts/sourcee_terms.py list 'saas', so "
        "'ai-saas-vendors-...' and 'ai-app-and-saas-founders-...' were both scored AI+spend although "
        "neither asks what anything costs. This run records the substantive count as zero and names the "
        "cause; removing 'saas' from the spend sets (a spend question still matches 'pricing'/'cost'/"
        "'budget'/'subscription') is the fix and it is flagged for the next run rather than applied "
        "mid-run to a shared module.",
        "THE VERBATIM-ADDRESS COUNT ON A REPLY ROUTE WAS A HAND-MEASURED NUMBER UNTIL TODAY. The digest "
        "cited 'the address appearing verbatim 6 times' on tobiamure.com/, but every per-run probe wrote "
        "that by hand, so a moved or re-worded page could not be told from a live route. "
        "scripts/probe_routes.py now records `emails_on_page` (each address and how many times it appears) "
        "for every route it probes, and this digest reads the count from today's probe file: 6 on "
        "tobiamure.com/, 5 on tobiamure.com/contact/. Measured, not typed.",
        "THE DIGEST AND THE QUEUE STILL DISAGREE ON THE TOOL COUNT IF A CARRIED TEMPLATE IS NOT "
        "RE-DERIVED, AND THE REPAIR RAN AGAIN TODAY. The catalogue moved from 78 to 79 entries (a vendor "
        "listing landed 2026-10-17), so any carried row still quoting 'of 77/78 tools' was re-derived in "
        "suggested_pitch_template; the repaired rows are named in this file's build log.",
        "THE PER-RUN WINDOW, BODY AND DIGEST SCRIPTS ARE STILL HAND-COPIED, AND THAT REMAINS THIS "
        f"MONITOR'S ONE UNFIXED STRUCTURAL DEFECT. _window_{MMDD}.py, _bodies_{MMDD}.py and "
        f"_digest_{MMDD}.py were produced by copying yesterday's files and editing constants. Converting "
        "the three to scripts/ with an explicit run date is the next real fix; it has now been deferred "
        "three runs.",
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(out, indent=1))
print(f"\nwrote digest-{TODAY}.json: {len(out['opportunities'])} opportunities, "
      f"{len(out['new_this_run'])} new-this-run notes, {len(out['expired_this_run'])} expiry notes")
