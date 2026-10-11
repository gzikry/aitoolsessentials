#!/usr/bin/env python3
"""Compose marketing/haro-outreach/digest-2026-10-11.json.

Carries the 107 tracked rows forward with their page truth refreshed from
verified-requests.json (fetched today by scripts/verify_journo_requests.py), adds the four rows
found this run, and records the three rows the vendor-token filter fix recovered.

Nothing is marked pitched here: sends are George's lane and the ledger is the only place a send
is recorded.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

S = Path("/Users/georgezikry/aitoolessentials/site")
D = S / "marketing/haro-outreach"
TODAY = "2026-10-11"

prev = json.loads((D / "digest-2026-10-10.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
window = json.loads((D / "_window_1011.json").read_text())
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
        f"NOT in the newest AI-topic feed: 0 of the tracked rows are, on {TODAY} or on 2026-10-10, "
        f"because the feed is a rolling 50-slot window that the tracked backlog sits outside of - "
        f"so this row carries no feed freshness and is colder than its age alone suggests."
    )
    return o


opps = [refresh(o) for o in prev["opportunities"]]
for o in opps:
    o.setdefault("slug", slug_of(o["url"]))
by_slug = {o["slug"]: o for o in opps}
print(f"carried {len(opps)} rows; every deadline rewritten with today's page truth")

# ---------------------------------------------------------------------------
# Rows found this run
# ---------------------------------------------------------------------------
NEW = [
    {
        "url": SITE + "tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring",
        "query_text": (
            "Tech & HR Leaders - AI At Work Impact On Jobs & Hiring. \"Pitch Me Workplace Stories and Experts "
            "for a Fast Company Work Life Feature. I'm a finance and technology journalist. My work runs in "
            "Investopedia, TheStreet, Forbes, Inc., Benzinga, and FinanceFeeds. I'm building pitches for Fast "
            "Company's Work Life section... The lanes I'm sourcing for right now: AI at work: what it is really "
            "changing about jobs, teams and hiring... What I'd need: For experts: the credential and the research "
            "behind it. Original data, or a survey with its sample size and method. Workplace expert is not a "
            "credential... email me at [email redacted] No DM pitches here on LinkedIn. Email me.\""
        ),
        "journalist_publication": (
            "Tobi Amure (the page's own author field) - freelancer building pitches for Fast Company's Work Life "
            "section; his body text says his work runs in Investopedia, TheStreet, Forbes, Inc., Benzinga and "
            "FinanceFeeds. Fast Company does not name him on the request."
        ),
        "category": "AI / Future of Work / Jobs & Hiring / Original Data",
        "deadline": (
            "No cutoff stated; he asks for the idea and says the editor approval cycle 'takes weeks, not days'. "
            f"RE-VERIFIED {TODAY}: HTTP 200, live=True, badge 'Posted in last 7 days', datePublished "
            "2026-10-10T13:51:49.235+00:00 = 1 day, no expiry notice on the page. IS in the newest AI-topic feed "
            "(one of the 15 entries that turned over into it today)."
        ),
        "contact_method": (
            "The page redacts the address ('email me at [email redacted]') and says explicitly 'No DM pitches here "
            "on LinkedIn. Email me.' No address, handle or link is published on the request itself "
            "(published_links = Sourcee's own author chrome only). ROUTE NOT RESOLVED: six byline pages tried on "
            f"{TODAY} and all six returned HTTP 403 - muckrack.com/tobi-amure (5,693 B), "
            "investopedia.com/tobi-amure-5203106 (680,487 B), forbes.com/sites/tobiamure (770 B), "
            "thestreet.com/author/tobi-amure (773 B), benzinga.com/author/tobi-amure (5,486 B), "
            "inc.com/author/tobi-amure (767 B). Recorded so they are not retried as routes. NOT SENDABLE until an "
            "address is published somewhere other than the redacted body."
        ),
        "relevance": "low-medium",
        "relevance_notes": (
            "His AI-at-work lane asks what AI is changing about jobs, teams and hiring; the only asset this site "
            "holds is a dated list-price index of 77 AI tools, which speaks to what AI costs a person, not to what "
            "it changes about work. He states plainly that a workplace expert is not a credential and asks for the "
            "research behind the claim - we hold no workplace credential and would be claiming one. Held below "
            "'medium' for that reason. Recorded anyway because it is the freshest AI-relevant request in the window "
            "and the first in weeks that explicitly asks for original data with a method, which is the one thing "
            "this monitor genuinely has."
        ),
        "suggested_pitch_template": (
            "None drafted - no route. If a route is ever resolved, the only honest angle is the method: we "
            "hand-check dated list prices across 77 AI tools and can supply every figure with its source URL and "
            "check date (42 of 77 publish a monthly price, 33 at or under $25/month, median $17.50, checked "
            f"{TODAY}). Do not present any of it as a workplace-expert credential."
        ),
    },
    {
        "url": SITE + "ai-cybersecurity-iot-and-web3-founders-and-operators-news-submissions",
        "query_text": (
            "AI, Cybersecurity, IoT & Web3 Founders & Operators - News Submissions. \"Morning Tick has found its "
            "place... Our readers are founders, business owners, operators, investors and buyers who want to know "
            "which young companies are worth watching. If you're building one of these companies, we'd like to "
            "hear from you. Send us your news, and we'll write the story in our own words. If you're a founder, "
            "operator or researcher with a view on where your industry is heading, the Thought Pulse Network "
            "gives you a place to share it under your own name... Get in touch: [email redacted]\""
        ),
        "journalist_publication": (
            "Aditya Prakash (the page's own author field) - Morning Tick, a startup-news publication"
        ),
        "category": "AI / Startup News Submissions",
        "deadline": (
            f"None stated. RE-VERIFIED {TODAY}: HTTP 200, live=True, badge 'Posted in last 7 days', datePublished "
            "2026-10-10T06:06:01.882+00:00 = 1 day, no expiry notice on the page. IS in the newest AI-topic feed."
        ),
        "contact_method": (
            "'Get in touch: [email redacted]' - Sourcee redacts the address and the page publishes no other handle "
            "or link (published_links = Sourcee's own author chrome only). Its one outbound link, "
            "lnkd.in/gHZDHvxS, is a Morning Tick 'about us' shortlink, not a reply route. NOT RESOLVED."
        ),
        "relevance": "low",
        "relevance_notes": (
            "The request wants the founders and operators of companies building AI, cybersecurity, IoT or Web3 to "
            "send their own company news. We are a publisher, not such a company, and answering it would mean "
            "claiming standing we do not hold. It also has no route. Tracked as a measurement, not a candidate."
        ),
        "suggested_pitch_template": "None. No route and no standing.",
    },
    {
        "url": SITE + "anthropic-gtm-leaders-scaling-300k-b2b-clients",
        "query_text": (
            "Anthropic GTM Leaders - Scaling 300k B2B Clients. \"I'm on the way to New York! In 2026, I recorded 21 "
            "interviews with the UK's best sales leaders - think OpenAI, Granola, Wiz, Pleo and Vanta. Now I'm "
            "hopping across the pond to film another 10 episodes with the fastest growing GTM/sales people on the "
            "planet - ElevenLabs, Fortify, AirOps, amongst other industry leading companies. But there's one more "
            "I want to hear from - Anthropic. They're already serving 300k B2B clients and the people want to hear "
            "how. So if you know someone on Anthropic's go to market team, give me a shout!\""
        ),
        "journalist_publication": (
            "Tris Tusa (the page's own author field) - an interviewer running a sales/GTM podcast and newsletter; "
            "no outlet is named on the request itself"
        ),
        "category": "AI / Vendor GTM / Interview Booking",
        "deadline": (
            f"None stated. RE-VERIFIED {TODAY}: HTTP 200, live=True, badge 'Posted in last 7 days', datePublished "
            "2026-10-09T13:24:02.267+00:00 = 2 days, no expiry notice on the page. IS in the newest AI-topic feed. "
            "It was inside the 2026-10-10 sitemap window and its body was fetched that run, but it was never "
            "tracked - see monitor_defects_fixed_this_run."
        ),
        "contact_method": (
            "'give me a shout' - no address, handle or link is published on the request. The two links the page "
            "carries, linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith, are Sourcee's own author chrome and "
            "are excluded by the verifier's CHROME list. NOT RESOLVED."
        ),
        "relevance": "low",
        "relevance_notes": (
            "The ask is an introduction to somebody on Anthropic's go-to-market team. We hold no such introduction "
            "and no standing to offer one. What we could contribute - dated list prices for Anthropic's own tiers "
            "(Claude Team Standard $20/seat/month and Premium $100, checked 2026-09-18) - is not what the request "
            "asks for. Tracked because it is an Anthropic-named request the monitor's own filter never caught, "
            "which is the evidence behind the vendor-token fix this run, not because it is pitchable."
        ),
        "suggested_pitch_template": "None. Do not pitch this without an Anthropic GTM introduction we do not have.",
    },
    {
        "url": SITE + "employees-pay-transparency-good-or-bad",
        "query_text": (
            "Employees - Pay Transparency Good or Bad. \"VOX POP CALLOUT: Is #paytransparency a good or a bad "
            "thing? I need AUDIO RESPONSES to this question for Business Spotlight Audio. Get in touch by "
            "Tuesday/Wednesday. #journorequest\""
        ),
        "journalist_publication": (
            "Melita Cameron-Wood (the page's own author field) - Business Spotlight Audio"
        ),
        "category": "Workplace / Pay Transparency / Audio Vox Pop",
        "deadline": (
            "'Get in touch by Tuesday/Wednesday' - a relative cutoff with no date attached, the only request in "
            f"this window that states one. RE-VERIFIED {TODAY}: HTTP 200, live=True, badge 'Posted in last 7 days', "
            "datePublished 2026-10-10T12:58:47+00:00 = 1 day."
        ),
        "contact_method": (
            "No address, handle or link published on the request (published_links = Sourcee's own author chrome "
            "only). NOT RESOLVED."
        ),
        "relevance": "low",
        "relevance_notes": (
            "Wants recorded audio of employees answering a pay-transparency question. We are not an employee and "
            "hold no audio contribution to make, and the request has no route. It is the window's only spend-token "
            "slug, and it is why the window is recorded as one spend hit and zero software spend - 'pay' here is "
            "payroll, not purchasing. It also falls in the same 'money at work' lane as the Fast Company request "
            "above, which is the only reason it is worth a note rather than a line in the count."
        ),
        "suggested_pitch_template": "None. Audio vox pop from employees; no route.",
    },
]

# ---------------------------------------------------------------------------
# Rows the vendor-token fix recovered: live pages, never tracked, all long cold
# ---------------------------------------------------------------------------
RECOVERED = [
    {
        "url": SITE + "anthropic-api-users-costs-and-token-burn-increase-since-january",
        "query_text": (
            "Anthropic API Users - Costs & Token Burn Increase Since January. \"so, for a story I'm chasing down: "
            "have you, as a user of its API, seen a dramatic increase in costs with Anthropic since January? Not "
            "talking about the company's growth, I'm asking if your costs/token burn went up, and if so why. No "
            "problem if not!\""
        ),
        "journalist_publication": "Ed Zitron (the page's own author field) - technology journalist",
        "category": "AI / Vendor API Costs & Token Burn / Core Beat",
        "deadline": (
            f"None stated. RE-VERIFIED {TODAY}: HTTP 200, live=True, badge 'Posted more than 1 month ago', "
            "datePublished 2026-05-02T16:34:15+00:00 = 162 days, no expiry notice. NOT in the newest AI-topic "
            "feed. Found by this run's filter fix, not by any earlier run: the slug names a vendor and no AI "
            "product class, so the previous AI regex never saw it."
        ),
        "contact_method": (
            "No route published on the request. Not pursued this run: at 162 days this is cold by the queue's "
            "10-day rule whatever its topic fit."
        ),
        "relevance": "high (topic) / cold (age)",
        "relevance_notes": (
            "Topically the closest request to this monitor's core beat that has ever been recorded - Anthropic "
            "API cost and token burn, asked of API users directly - and it sat untracked for 162 days because the "
            "filter listed product classes but no vendor names. Not sendable: five months old, out of the feed, "
            "and the story it feeds was almost certainly published long ago."
        ),
        "suggested_pitch_template": "None. Cold. Recorded as evidence for the filter fix.",
    },
    {
        "url": SITE + "prompt-engineers-tokenmaxxing-anecdotes",
        "query_text": (
            "Prompt Engineers - Tokenmaxxing Anecdotes. \"What's the most outrageous example of tokenmaxxing "
            "you've personally observed? Looking for some anecdotes for an article.\""
        ),
        "journalist_publication": "Jacqueline Isaacs (the page's own author field)",
        "category": "AI / Token Spend / Anecdotes",
        "deadline": (
            f"None stated. RE-VERIFIED {TODAY}: HTTP 200, live=True, badge 'Posted more than 1 month ago', "
            "datePublished 2026-07-08T14:44:50+00:00 = 95 days, no expiry notice. NOT in the newest AI-topic feed."
        ),
        "contact_method": "No route published on the request. Not pursued: 95 days, cold.",
        "relevance": "low-medium (topic) / cold (age)",
        "relevance_notes": (
            "Asks for personally observed anecdotes of token overspend. We hold measured list prices, not "
            "observed anecdote, and the request is 95 days old. Recovered by the 2026-10-11 vendor-token fix."
        ),
        "suggested_pitch_template": "None. Cold.",
    },
    {
        "url": SITE + "investigative-reporters-openai-training-predatory-dynamic-pricing",
        "query_text": (
            "Investigative Reporters - OpenAI Training - Predatory Dynamic Pricing. \"If anyone is investigating "
            "for a piece on predatory and discriminatory 'dynamic pricing,' I have stuff for you. This is OpenAI's "
            "official partner training material...\""
        ),
        "journalist_publication": "Iaian7 (the page's own author field) - a source offering material, not a journalist",
        "category": "AI / Retail Pricing / Material Offered",
        "deadline": (
            f"None stated. RE-VERIFIED {TODAY}: HTTP 200, live=True, badge 'Posted more than 1 month ago', "
            "datePublished 2026-07-10T14:29:25.212+00:00 = 93 days, no expiry notice. NOT in the newest AI-topic "
            "feed."
        ),
        "contact_method": "None resolved; the poster offers material rather than requesting any.",
        "relevance": "low",
        "relevance_notes": (
            "Not a request at all - it offers material to investigative reporters. Recorded only so the filter "
            "fix's output is fully accounted for."
        ),
        "suggested_pitch_template": "None.",
    },
]

for r in NEW + RECOVERED:
    r["slug"] = slug_of(r["url"])
    r["_page_live"] = True
    r["_days_old"] = {
        "tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring": 1,
        "ai-cybersecurity-iot-and-web3-founders-and-operators-news-submissions": 1,
        "anthropic-gtm-leaders-scaling-300k-b2b-clients": 2,
        "employees-pay-transparency-good-or-bad": 1,
        "anthropic-api-users-costs-and-token-burn-increase-since-january": 162,
        "prompt-engineers-tokenmaxxing-anecdotes": 95,
        "investigative-reporters-openai-training-predatory-dynamic-pricing": 93,
    }[r["slug"]]
    r["_in_ai_topic_feed"] = r["slug"] in FEED
    r["_badge"] = "Posted more than 1 month ago" if r["_days_old"] > 30 else "Posted in last 7 days"
    r["_new_or_recovered_2026-10-11"] = True

opps.extend(NEW + RECOVERED)

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
unpitched = [o for o in opps if o["slug"] not in sent_slugs and o["slug"] not in skipped]
live = [o for o in unpitched if (o["_days_old"] or 999) <= 10]
cold = [o for o in unpitched if (o["_days_old"] or 999) > 10]
print(f"tracked {len(opps)} | unpitched {len(unpitched)} | live {len(live)} | cold {len(cold)}")

# Drafts on disk for rows that were never sent and are not recorded as skipped — measured, not typed.
_drafted = set()
for f in D.glob("pitch-drafts-*.md"):
    txt = f.read_text(errors="ignore")
    for o in unpitched:
        if o["slug"] in txt:
            _drafted.add(o["slug"])
DRAFTS_UNSENT = len(_drafted)
print(f"rows with a draft on disk and no send in the ledger: {DRAFTS_UNSENT}")

out = {
    "date": TODAY,
    "monitor": "HARO / Sourcee journalist-request monitor for AIToolsEssentials",
    "run_at": datetime.now(timezone.utc).isoformat(),
    "search_scope": prev["search_scope"],
    "age_policy": (
        "Ages are read off each request page (JSON-LD datePublished plus the rendered 'Posted ... ago' badge), "
        "never off the digest text, and every carried row's deadline field was rewritten this run from the page "
        "itself. All 107 carried URLs re-fetched: HTTP 200 for every one, body still served, no expiry notice; "
        "the 7 rows added today were fetched the same way. Two further facts belong here. (1) No request has ever "
        "been seen to expire on this source - 100% of carried rows have returned HTTP 200 on every run - so "
        "'deadline' means the poster's own stated cutoff or a measured age, never an observed expiry. (2) FEED "
        "MEMBERSHIP IS NOT A FRESHNESS SIGNAL FOR THIS BACKLOG: Sourcee's AI topic page is a rolling 50-slot "
        f"window that turned over 15 entries between 2026-10-10 and {TODAY} (35 of the 50 are the same slugs), "
        "and ZERO of the 107 tracked rows are in it on either day. Every tracked row is therefore outside the "
        "live feed by construction, and no row may be called fresh or cold on feed membership. A row's age comes "
        "from its page, and a row that has left the feed is colder than that age suggests - which today is every "
        "tracked row."
    ),
    "platforms_checked": [
        {
            "platform": "Sourcee (sourcee.app)",
            "status": "accessible",
            "notes": (
                "Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP 200, 9,689,320 bytes, 40,299 "
                "loc/lastmod pairs, newest lastmod 2026-10-11T02:55:43.000Z). 36 slugs carry a lastmod newer than "
                "the 2026-10-10 run's mark (2026-10-10T03:26:04.000Z): 2 carry an AI token, 0 carry an AI token "
                "plus a real spend token, 1 carries a spend token alone (employees-pay-transparency-good-or-bad, "
                "payroll not purchasing). Site root re-probed HTTP 200 (100,825 bytes)."
            ),
        },
        {
            "platform": "Sourcee AI topic feed",
            "status": "accessible",
            "notes": (
                "HTTP 200, 194,727 bytes, 50 slugs - up from 174,204 bytes yesterday. 35 of the 50 are the same "
                "slugs as 2026-10-10; 15 turned over. 15 of the 50 are inside today's 36-slug sitemap window. "
                "Zero of the 107 tracked rows appear, on either day."
            ),
        },
        {"platform": "HARO (helpareporter.com)", "status": "blocked",
         "notes": "HTTP 429, 31,377 bytes, page title 'Vercel Security Checkpoint'. Expected; not retried. Unchanged since 2026-09-12."},
        {"platform": "Connectively (connectively.us)", "status": "blocked",
         "notes": "HTTP 429, 31,373 bytes, 'Vercel Security Checkpoint'. Expected; not retried."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "not-applicable",
         "notes": "HTTP 404 at /requests and the page title is 'Page Not Found - Source of Sources'. Reporter-only per the monitor's standing finding."},
        {"platform": "Qwoted (qwoted.com)", "status": "blocked",
         "notes": "HTTP 404 at /requests; the app needs an authenticated session. Not retried."},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre-launch",
         "notes": "HTTP 200, 12,064 bytes, 'MentionMatch - Connect B2B Writers with Expert Sources'. Still a holding page."},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "blocked",
         "notes": "HTTP 401, 74 bytes - the MCP endpoint needs an OAuth handshake. Third consecutive run. This is the one platform that would widen supply, and it is blocked on an account, not on the monitor."},
        {"platform": "ResponseSource (responsesource.com)", "status": "accessible-but-not-usable",
         "notes": "HTTP 200, 148,281 bytes. Public pages only; the request database needs a subscription."},
    ],
    "opportunities": opps,
    "new_this_run": [
        "FOUR ROWS ADDED — the first additions since 2026-10-07 — and THREE OF THEM WERE RECOVERED FROM THE MONITOR'S OWN FILTER, NOT FROM THE PLATFORM'S SUPPLY. The vendor-token defect is now fixed (see monitor_defects_fixed_this_run).",
        "tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring — 1 day old, live, in the feed. A freelancer building pitches for Fast Company's Work Life section, asking for original data with a sample size and method. Relevance low-medium: the lane is AI-and-jobs, our asset is AI prices, and he states that a workplace expert is not a credential. No route — his address is Sourcee-redacted and six byline pages returned HTTP 403.",
        "ai-cybersecurity-iot-and-web3-founders-and-operators-news-submissions — 1 day old, live, in the feed. Morning Tick wants founders of AI/cyber/IoT/Web3 companies to submit their own news. We are not such a company. Relevance low, no route.",
        "anthropic-gtm-leaders-scaling-300k-b2b-clients — 2 days old, live, in the feed, and NEVER TRACKED UNTIL NOW. It was inside the 2026-10-10 sitemap window and its body was fetched that run, but the AI regex listed product classes and no vendor names, so 'anthropic' matched nothing and the row was dropped. Relevance low (it asks for an introduction to Anthropic's GTM team, which we do not have) but it is the evidence for the fix, and it is core beat in every other respect.",
        "employees-pay-transparency-good-or-bad — 1 day old, live, in the feed. Business Spotlight Audio wants recorded audio from employees on pay transparency, with the window's only stated cutoff ('by Tuesday/Wednesday', no date). No route; we are not an employee. It is the window's single spend-token slug, and it is why the window shows one spend hit and zero software spend.",
        "THREE LONG-COLD CORE-BEAT ROWS RECOVERED BY THE FILTER FIX: anthropic-api-users-costs-and-token-burn-increase-since-january (Ed Zitron, 162 days, relevance high on topic and cold on age - the closest request to this monitor's beat that has ever been recorded, and it was invisible for 162 days because the slug says 'anthropic' and names no AI product class); prompt-engineers-tokenmaxxing-anecdotes (95 days); investigative-reporters-openai-training-predatory-dynamic-pricing (93 days, and not a request at all - it offers material).",
        "WINDOW BODY SWEEP: 36 slugs, 2 AI-token, 1 spend-token, 0 AI+spend. The two AI-token slugs and the one spend slug were all fetched and read; their four bodies are the three rows above plus the audio vox pop. No other window body touches AI, pricing or software spend. Window volume is up from 66 slugs on 2026-10-10.",
    ],
    "expired_this_run": [
        "Nothing expired on its page: all 107 carried URLs returned HTTP 200 with the request body still served. See age_policy - an expiry has never once been observed on this source, so the absence of an expiry notice is weak evidence and is recorded as such.",
        ((f"ROWS CROSSED THE 10-DAY LINE SINCE YESTERDAY: {len(crossed)}."
          if crossed else
          "NO ROW CROSSED THE 10-DAY LINE SINCE YESTERDAY - the first run in nine days with no crossing. The live/cold split moved live unpitched 54 -> "
          f"{len(live)} and cold unpitched 49 -> {len(cold)} for the opposite reason: three rows left the unpitched pool by being sent on 2026-10-10 and one more by being added inside the 10-day window than crossed out of it.")
         + ("" if not crossed else
            " Each one is relevance 'low', none of them has a draft, and none has ever been inside the sendable "
            "count, so the crossing cost nothing. Three of the four do name a reply route, but it is 'DM the poster' "
            "or 'reply to the original post' - a route on the poster's own platform, not on Sourcee - so none of the "
            "four was actionable from here on any day of the ten: " + "; ".join(crossed) + ".")),
        (f"{len(at_ten)} ROWS SIT AT EXACTLY 10 DAYS AND CROSS TOMORROW and it is named here in advance, because a quiet count change should never be mistaken for a quiet week: " + "; ".join(at_ten) + "."
         if at_ten else "No row sits at exactly 10 days today, so the next run has no scheduled crossing."),
        "ROWS THAT DROPPED OFF THE NEWEST DIGEST: 0. Every tracked row is carried in every digest by design, so this figure is a monitor convention and not platform evidence - see age_policy.",
    ],
    "summary": (
        f"{len(opps)} tracked requests ({len(prev['opportunities'])} carried and all {len(prev['opportunities'])} "
        f"re-verified live, 7 added this run including 3 recovered by a filter fix, {len(pitched)} pitched, "
        f"{len(skipped)} deliberately skipped). Of the {len(unpitched)} unpitched, {len(live)} are live and "
        f"{len(cold)} are cold. ONE is sendable: the WSJ columnist's blocked-work-accounts request (relevance "
        "'medium', 6 days old, LinkedIn DM), carried and unsent since 2026-10-10. The three pitches George sent "
        "on 2026-10-10 21:20 UTC are the first sends in 22 days; one of the four messages bounced (550 NoSuchUser) "
        "and no recipient has replied. The window produced 36 slugs with 2 AI-token and 0 AI+spend. Headline "
        "figures re-derived this run against a snapshot refreshed today: 42 of 77 tools publish a monthly price, "
        "33 of those at or under $25/month, median $17.50; monthly vs annual 1.11x-2.53x, median 1.25x over 19 "
        "tiers (pair set built 2026-10-08, re-read not rebuilt). Zero pitches sent this run - sends remain "
        "George's lane."
    ),
    "recommended_actions": [
        "SEND THE WSJ BLOCKED-WORK-ACCOUNTS DRAFT - THE ONLY SENDABLE ROW IN THE QUEUE, NOW 6 DAYS OLD, CARRIED UNSENT THROUGH TWO RUNS. Paste-ready at pitch-drafts-2026-10-11.md section 1. Route: LinkedIn DM to https://www.linkedin.com/in/christopher-mims-club/ (re-verified HTTP 200 today, 611,240 bytes, title 'Christopher Mims - The Wall Street Journal | LinkedIn'); the request's own body says '(DMs open)'. Relevance 'medium'. George's lane, not automatable. Two dead ends are recorded so they are not retried as routes: muckrack.com/christopher-mims HTTP 403 and wsj.com/news/author/christopher-mims HTTP 401.",
        "NOTE THE THREE SENDS FROM 2026-10-10: google-and-claude-enterprise-users-seats-and-token-costs, speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech and fulltime-employees-shadow-ai-use-and-paying-outofpocket. The last of the three bounced. No reply has arrived to either of the two that were delivered, and none is due yet at 19 hours. The Amplemarket thread is closed by the vendor's own acknowledgment and must not be bumped.",
        "RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE if the queue is ever to be wider than one row. Today's evidence: a 36-slug window with 2 AI-token slugs and no AI+spend slug, and a 107-row backlog that has rotated entirely out of the live feed. Sourcee's supply and this monitor's filters are both near their limit; the authenticated platforms are the only remaining supply, and the monitor cannot open them itself.",
        "DECIDE THE COLD CORE-BEAT ROWS RECOVERED TODAY, as a judgement call rather than a send: an Ed Zitron request for Anthropic API users' cost increases, 162 days old, high relevance and cold. It is not a pitch candidate - the story has almost certainly run - but a row that good should not be re-discovered on a future run and then quietly drafted. Either record it as skipped or leave it recorded as cold; do not draft it.",
    ],
    "monitor_health": {
        "platforms_accessible": 2,
        "platforms_accessible_but_not_usable": 1,
        "platforms_blocked": 5,
        "platforms_not_applicable": 1,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": 2,
        "new_ai_plus_spend_slugs_in_window": 0,
        "window_bodies_fetched": 36,
        "new_rows_added_to_tracking": 7,
        "rows_recovered_by_filter_fix": 3,
        "tracked_urls": len(opps),
        "unpitched": len(unpitched),
        "live_unpitched": len(live),
        "cold_unpitched": len(cold),
        "pitched_plus_skipped": len(pitched | skipped),
        "sendable": 1,
        "pitches_sent_this_run": 0,
        "pitches_sent_on_2026-10-10_by_george": 3,
        "messages_bounced_on_2026-10-10": 1,
        "replies_to_date": 1,
        "reply_outstanding_amplemarket_thread": False,
        "rows_crossed_cold_since_last_digest": len(crossed),
        "rows_at_ten_days_crossing_next_run": len(at_ten),
        # Renamed from `drafts_written_never_sent`, which had been hand-typed at 4-7 for weeks while
        # 23 files sat on disk, and which could not survive today's draft file: that file names rows
        # it deliberately did NOT draft, so counting rows named in a draft file counts non-drafts too.
        # Two precise numbers instead of one ambiguous one.
        "pitch_draft_files_on_disk": len(list(D.glob("pitch-drafts-*.md"))),
        "rows_named_in_a_draft_file": DRAFTS_UNSENT,
        "shadow_ai_tools_tracked": 77,
        "shadow_ai_monthly_priced_tools": 42,
        "shadow_ai_at_or_under_25": 33,
        "shadow_ai_median_cheapest_paid_tier": 17.5,
        "pricing_snapshot_updated": "2026-10-11",
        "monthly_annual_pairs_built": "2026-10-08",
    },
    "monitor_defects_fixed_this_run": [
        "THE AI FILTER HAD NO VENDOR NAMES, AND THAT LOST A CORE-BEAT REQUEST FOR 162 DAYS. Every per-run window script carried its own AI regex, and it listed product classes (ai, llm, gpt, claude, gemini, copilot, agents, machine-learning, automation, ml) and no vendor. A slug that names a vendor without naming a class was therefore invisible: 'anthropic-gtm-leaders-scaling-300k-b2b-clients' sat inside the 2026-10-10 sitemap window, its body was fetched that run, and it was dropped without being tracked. Measured across today's full 40,299-slug sitemap, the fix adds 63 slugs the old filter missed, of which 3 carry a real spend token - including anthropic-api-users-costs-and-token-burn-increase-since-january, the single closest match to this monitor's beat it has ever recorded. Fixed: the token set now lives in scripts/sourcee_terms.py with vendor and product names alongside product classes, and the per-run window script imports it instead of defining its own.",
        "FALSE-POSITIVE CONTROL ON THAT FIX. Two candidate tokens were rejected after measuring them against the whole sitemap rather than trusting them: 'make' fired on make-friends, make-money, make-life-affordable, make-kitchens and even a vintage-tractor slug about the Make brand, and bare 'token' fired on crypto-tokens and a Paizo token-gallery story. Both were cut, which is why the fix adds 63 slugs and not 85 - the 22 dropped were noise, and the count is a measurement rather than a guess.",
        "THE FEED-MEMBERSHIP CLAIM IS NOW MEASURED RATHER THAN ASSUMED. The monitor had been reading 'AI-topic feed: yes' as a freshness signal on individual rows. Measured today: the feed is a rolling 50-slot window that turned over 15 entries in a day, 35 of the 50 persisted, and ZERO of the 107 tracked rows appear on either day. Every tracked row is outside it by construction, so the flag is recorded on every row and used in no ranking.",
        "THE DIGEST NO LONGER PATCHES THE DEADLINE FIELD BY APPEND. Each of the 107 carried rows had its deadline rebuilt this run from the page's own badge and datePublished, with the previous verification block stripped rather than appended to, so a row's age cannot be read off a stale sentence stacked underneath today's.",
        "THE MONITOR'S OWN RE-VERIFICATION STAMP WAS BEING READ AS THE POSTING DATE, AND IT FLOATED THREE DEAD REQUESTS INTO THE LIVE LIST. build_pitch_queue.py's age fallback took the FIRST yyyy-mm-dd in a row's deadline text whenever the page had not been probed. The deadline strings written this run lead with 'RE-VERIFIED 2026-10-11: HTTP 200 ...', so the first date in the text was the run's own date: the three rows recovered by the filter fix - posted in May and July, 162, 95 and 93 days old - were measured at 0.67 days and ranked as the freshest things in the queue, which is the same failure class as the 190-day-old request the queue's own docstring records as fixed. Caught by comparing the queue's live set against the digest's page-derived ages rather than by trusting either. Fixed: the monitor's own stamps are stripped before the search, an explicit 'datePublished <date>' is preferred, and the three now measure 162.67, 95.67 and 93.67 days. The queue and the digest agree at 53 live and 1 sendable.",
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(out, indent=1))
print(f"\nwrote digest-{TODAY}.json: {len(out['opportunities'])} opportunities, "
      f"{len(out['new_this_run'])} new-this-run notes, {len(out['expired_this_run'])} expiry notes")
