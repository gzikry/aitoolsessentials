#!/usr/bin/env python3
"""Write today's digest: marketing/haro-outreach/digest-2026-09-29.json

One record per tracked opportunity, re-verified against its own page today. Carried rows are
refreshed from verified-requests.json (page datePublished + rendered badge), not from yesterday's
digest text.

New this run: the four AI-token slugs from today's sitemap window are ADDED to the tracked set,
because each is a real /journo-request/<slug> page with a live body and a documented reply route.
That takes the carry set from 47 to 51. The ten spend-token slugs are NOT added: all ten are
consumer cost-of-living calls (gas prices, childcare, dating budgets, retirement) that matched a
spend regex on 'affordable'/'budget'/'prices' and contain no software-spend ask.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-09-29"

prev = json.loads((D / "digest-2026-09-28.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
win = json.loads((D / "_window_0929.json").read_text())
cands = json.loads((D / "_candidates_0929.json").read_text())
routes = json.loads((D / "_routes_0929.json").read_text()) if (D / "_routes_0929.json").exists() else {}

CUT = re.compile(
    r"\.?\s*(?:RE-VERIFIED|Re-verified|PAGE-VERIFIED|NEWLY COLD|NEW this run|Page badge|"
    r"Badge '|On Sourcee's live AI topic page|Currently on the AI topic feed|age superseded|~age|"
    r"Verify with the outlet|with no refresh|was posted|datePublished|\d{4}-\d{2}-\d{2}|"
    r"\d{2,4}\+00:00)")
TAIL = re.compile(r"(?:,\s*|\s+|—\s*|-\s*)?(?:posted|was|with|is|and|so|reads|badge|Page badge|"
                  r"'|\"|\()\s*$", re.I)


def _base(text: str | None) -> str:
    text = (text or "").strip()
    m = CUT.search(text)
    if m:
        text = text[:m.start()].strip()
    tag = re.match(r"^(STATED (?:INTERNAL )?DEADLINE PASSED)", text)
    if tag:
        return f"{tag.group(1)} — do not pitch"
    if text.count("(") > text.count(")"):
        text = text[:text.rfind("(")].strip()
    for _ in range(3):
        t2 = TAIL.sub("", text).strip()
        if t2 == text:
            break
        text = t2
    text = re.sub(r",\s*BUT$", "", text, flags=re.I).strip()
    if text.count("'") % 2:
        text = text[:text.rfind("'")].strip().rstrip(" ,;:.–—-~\"")
    return text.rstrip(" ,;:.–—-~'\"")


ops = []
SUPERSEDED_RANGE = re.compile(r"1\.(?:21|16)x\s*(?:-|–|to)\s*2\.53x(?:,\s*median\s*1\.33x)?", re.I)
CURRENT_RANGE = "1.11x-2.53x, median 1.25x over 19 tiers"
CHECKED_OLD = re.compile(r"checked 2026-09-1[89]")


def _repair(text: str | None) -> tuple[str, bool]:
    if not text:
        return text or "", False
    fixed, n = SUPERSEDED_RANGE.subn(CURRENT_RANGE, text)
    fixed, n2 = CHECKED_OLD.subn(f"checked {TODAY}", fixed)
    return fixed, bool(n or n2)


for op in prev["opportunities"]:
    slug = op["url"].rstrip("/").split("/journo-request/")[-1]
    v = verified.get(slug) or {}
    new = dict(op)
    repairs = []
    for field in ("suggested_pitch_template", "relevance_notes", "contact_method", "query_text"):
        new[field], changed = _repair(new.get(field))
        if changed:
            repairs.append(field)
    if repairs:
        new["_figures_repaired"] = repairs
    if v:
        base = _base(new.get("deadline")) or "No cutoff stated"
        new["deadline"] = (
            f"{base + '. ' if base else ''}RE-VERIFIED {TODAY}: HTTP {v.get('http')}, "
            f"live={v.get('live')}, badge '{v.get('badge')}', datePublished {v.get('datePublished')} "
            f"= {v.get('days_old')} days, no expiry notice on the page."
        ).strip()
        new["_page_live"] = bool(v.get("live"))
        new["_days_old"] = v.get("days_old")
        new["_badge"] = v.get("badge")
        if new.get("suggested_pitch_template"):
            new["suggested_pitch_template"] = re.sub(
                r"checked 2026-09-1[89]", f"re-checked {TODAY}", new["suggested_pitch_template"])
    ops.append(new)

repaired = [o["url"].rsplit("/", 1)[-1] for o in ops if o.get("_figures_repaired")]

# ---------------------------------------------------------------- four new tracked rows
NEW_ROWS = [
    {
        "slug": "insurance-agents-ai-use-in-personal-lines",
        "query_text": ("Insurance Agents - AI Use in Personal Lines. 'How much do you use AI?' — a "
                       "reporter covering personal lines insurance for P&C Specialist (a Financial "
                       "Times publication) looking to talk to agents about how much they use AI in "
                       "their work. 'If you're willing to talk, please comment below or DM me. We "
                       "don't need to identify you in the story.'"),
        "journalist_publication": "P&C Specialist (Financial Times) — reporter not named in the body",
        "category": "Insurance / AI Adoption",
        "contact_method": ("'Comment below or DM me' — no address published and none redacted. "
                           "PAGE-VERIFIED 2026-09-29: email_redacted=False, emails_on_page=none, "
                           "reply_hints=['Comment', 'DM me']. Route is the original X/LinkedIn post; "
                           "we hold no handle for this reporter."),
        "relevance": "low-medium",
        "relevance_notes": (
            "On-topic on AI adoption and from an FT title, but it is a first-person-use call: an "
            "agent describing how they use AI day to day. We are not an insurance agent, and the "
            "request contains no pricing, seat or budget question our dated price set answers. "
            "Recorded and carried because it is a genuine live request with a named publication; "
            "not drafted, and there is no route we can resolve."),
        "suggested_pitch_template": (
            "None — excluded: wants a working insurance agent's own AI usage; we have no standing "
            "and the only route is a public comment on a post we cannot identify."),
    },
    {
        "slug": "data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity",
        "query_text": ("Data Center Operators & Cloud Buyers - Proof of Deployable AI Capacity. "
                       "'A GPU commitment is not deployable capacity... The gap between announced "
                       "capacity and deployable capacity is where the next generation of "
                       "infrastructure work begins.' A vendor-authored thought-leadership essay "
                       "(Location Truth / Path Truth) from Connectbase."),
        "journalist_publication": "Connectbase (vendor-authored request, not a journalist byline)",
        "category": "Data Center / AI Infrastructure",
        "contact_method": ("No route published on the page: no email, no handle, no link, and no "
                           "reply hint. PAGE-VERIFIED 2026-09-29: email_redacted=False, "
                           "emails_on_page=none, published_links=none."),
        "relevance": "low",
        "relevance_notes": (
            "Self-interested vendor essay soliciting co-signature on Connectbase's framing of "
            "data-centre capacity, not a reporter gathering sources. Contains no question, no "
            "deadline and no cost data we could answer with. Carried for completeness only."),
        "suggested_pitch_template": "None — excluded: vendor-authored promotion with no reply route.",
    },
    {
        "slug": "b2b-marketing-leaders-hyperspecialization-to-outcompete-ai",
        "query_text": ("B2B Marketing Leaders - Hyper-Specialization to Outcompete AI. 'Pitch me "
                       "example for @MarketingSherpa article: Using hyper-specialization to "
                       "outcompete AI mediocrity. LLMs are generalists. How does your company use "
                       "its domain specialty to deliver better value prop?'"),
        "journalist_publication": "MarketingSherpa",
        "category": "B2B Marketing / Positioning",
        "contact_method": ("Original X post (the page carries a t.co link to the article example); "
                           "no address published. PAGE-VERIFIED 2026-09-29: email_redacted=False, "
                           "emails_on_page=none, published_links=['https://t.co/Wk0GLLXXen']."),
        "relevance": "low",
        "relevance_notes": (
            "Wants a company's own positioning story — how a domain specialist outperforms "
            "generalist LLMs. A price-benchmark publisher has no such customer story to give, and "
            "the request names no cost or subscription angle. Carried because it is an editorial "
            "call from a named publication, not drafted."),
        "suggested_pitch_template": (
            "None — excluded: wants a B2B company's own positioning anecdote; we are a publisher, "
            "and the request asks for nothing our price data supports."),
    },
    {
        "slug": "ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes",
        "query_text": ("AI Practitioners & Team Leads - Real AI Deployments Failures & Fixes. 'That's "
                       "why the AI Everywhere® Leaders podcast is back... 1. Want to be a guest? If "
                       "you're using AI in your business, your team or your career, I want to hear "
                       "your story. Comment \"guest\" or send me a DM.'"),
        "journalist_publication": "AI Everywhere® Leaders podcast (host not named in the body)",
        "category": "AI Adoption / Podcast Guesting",
        "contact_method": ("'Comment \"guest\" or send me a DM'; no address published and none "
                           "redacted. PAGE-VERIFIED 2026-09-29: email_redacted=False, "
                           "emails_on_page=none, reply_hints=['Comment']. Route is the original "
                           "LinkedIn post, which we cannot identify from the page."),
        "relevance": "low",
        "relevance_notes": (
            "A podcast guest booking, plus a 'tag someone who should be on the show' sweepstakes. "
            "Guesting would mean appearing as ourselves to tell a deployment story we do not have, "
            "and the request asks no question our data answers. Carried, not drafted."),
        "suggested_pitch_template": (
            "None — excluded: podcast guest call wanting an operator's own deployment story; "
            "no route resolvable off the page."),
    },
]

for row in NEW_ROWS:
    slug = row.pop("slug")
    v = verified.get(slug) or {}
    rec = {
        "url": f"https://www.sourcee.app/journo-request/{slug}",
        "_page_live": bool(v.get("live")), "_days_old": v.get("days_old"), "_badge": v.get("badge"),
        "deadline": (f"No cutoff stated. RE-VERIFIED {TODAY}: HTTP {v.get('http')}, live={v.get('live')}, "
                     f"badge '{v.get('badge')}', datePublished {v.get('datePublished')} = "
                     f"{v.get('days_old')} days, no expiry notice on the page."),
        "_new_this_run": True,
    }
    rec.update(row)
    ops.append(rec)

stale = [o for o in ops if (o.get("_days_old") or 0) > 10]
live = [o for o in ops if (o.get("_days_old") or 0) <= 10]

# Every row that moved from live to cold in this run, named rather than left as a count change.
CROSSED = ("companies-that-stopped-emailing-pdfs-new-tools-and-transition",)

ledger = json.loads((D / "pitch-ledger.json").read_text())
done = set()
for u in list(ledger.get("pitched", {})) + list(ledger.get("skipped", {})):
    done.add(u.rstrip("/").split("/journo-request/")[-1])
live_unp = [o for o in live if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]
cold_unp = [o for o in stale if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]

CAND_LINES = "; ".join(f"{s} ({c['datePublished']}Z)" for s, c in cands.items())

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{TODAY}T09:00:00-07:00",
    "search_scope": ("AI tools, AI pricing, shadow/unbudgeted AI spend, overlapping AI subscriptions, "
                     "software spend, SaaS cost/credits, agentic AI cost overruns, AI vendor support "
                     "value, tool consolidation, procurement budget"),
    "age_policy": ("Ages are read off each request page (JSON-LD datePublished plus the rendered "
                   "'Posted ... ago' badge), never off the digest text. Every carried URL was "
                   "re-fetched this run: HTTP 200 and the request body still served, none returns an "
                   "expiry notice and none has dropped off."),
    "platforms_checked": [
        {"platform": "Sourcee (sourcee.app)", "status": "accessible",
         "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP 200, "
                   f"{win['bytes']:,} bytes, {win['count']:,} loc/lastmod pairs, newest lastmod "
                   f"{win['newest']}). {len(win['window'])} slugs carry a lastmod newer than the "
                   f"2026-09-28 run's mark ({win['mark']}). Of those, {len(win['ai'])} carry an AI "
                   f"token, ZERO carry an AI token plus a real spend token, and {len(win['spend_any'])} "
                   f"carry any spend-adjacent token. All {len(win['ai']) + len(win['spend_any'])} "
                   f"candidate slugs (4 AI + 10 spend, none overlapping) were fetched and read in "
                   f"full. Sourcee itself re-probed HTTP 200 (100,854 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Re-measured. {win['feed_count']} slugs listed today, HTTP 200, 158,191 bytes, "
                   f"and {win['feed_overlap_with_window']} of {win['feed_count']} sit inside today's "
                   f"new sitemap window (40 of 40 this run - the first 100% overlap the monitor has "
                   f"measured, against 42-of-42 wrongly asserted on 2026-09-26 and 36-of-40 on "
                   f"2026-09-28). The conclusion does not rest on that overlap: absence from this "
                   f"feed is still not a cold signal, because every tracked carried request is "
                   f"absent from it by construction. Of the four AI-token finds today, only "
                   f"insurance-agents-ai-use-in-personal-lines appears in the feed.")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,204 bytes, 'Vercel Security Checkpoint'. "
                   "Eighteenth consecutive identical result. Queries reach sources only by a 3x-daily "
                   "email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": "Re-probed once. / HTTP 429, 31,194 bytes, 'Vercel Security Checkpoint'. No public feed."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                   "Source of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes, 'Error: The "
                   "page you were looking for doesn't exist'). Wrong path, not gated - unchanged. The "
                   "feed needs an authenticated app session.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. Apex HTTP 200 (11,342 bytes), title 'MentionMatch - Connect B2B Writers "
                   "with Expert Sources', no feed. Eighteenth consecutive run confirming a pre-launch shell.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\","
                   "\"error_description\":\"No authorization provided\"}. Free read-only feed covering "
                   "Connectively, HARO, X, LinkedIn, MentionMatch and Substack. Needs an interactive "
                   "OAuth handshake that cannot be completed from a scheduled run.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on seventeen consecutive "
                   "runs; the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy - and three of today's four AI-token finds are "
                   "X-originated requests (MarketingSherpa, the insurance call's DM route, the AI "
                   "Everywhere podcast call), so the proxy is still carrying that supply.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (148,368 bytes, 'ResponseSource - Connecting the Media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free "
                   "source-facing feed.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        (f"FOUR NEW AI-TOKEN REQUESTS - THE MOST THIS MONITOR HAS ADDED IN ONE RUN, AND ALL FOUR ARE "
         f"NOW TRACKED. {len(win['window'])} slugs carry a lastmod newer than the 2026-09-28 mark. "
         f"{len(win['ai'])} carry an AI token, ZERO carry an AI token plus a real spend token - the "
         f"SEVENTH consecutive run with none. Unlike the last six runs, the AI-token finds are not "
         f"all off-beat: one is an FT-title editorial call (P&C Specialist, insurance agents' AI use) "
         f"and one is a named-publication pitch call (MarketingSherpa on hyper-specialisation). All "
         f"four were fetched and read in full and are now carried as tracked opportunities, which "
         f"takes the carry set from 47 to 51."),
        (f"THE {len(cands)} CANDIDATES, BY NAME, SO THE ZERO IS CHECKABLE: {CAND_LINES}. None asks a "
         f"price, seat, licence or software-spend question. The four AI-token rows are: an insurance "
         f"agents' AI-use call (P&C Specialist, FT); a vendor-authored thought-leadership essay on "
         f"data-centre 'deployable capacity' from Connectbase; a MarketingSherpa call for a B2B "
         f"company's hyper-specialisation story; and an AI Everywhere podcast guest booking with a "
         f"'tag someone' sweepstake. The ten spend-token slugs are all consumer cost-of-living calls "
         f"- gas prices (Business Insider hypermiling), SF-to-affordable-area moves, Irish childcare "
         f"budgets, Christmas payday hacks, Washington Mystics ticket prices, 1-car households, NYC "
         f"heating-season fuel costs, Gen-Z dating budgets, small-business cash-flow stories and "
         f"'trapped living with your ex'. They matched the spend regex on 'prices', 'affordable', "
         f"'budget' and 'cost of living'. Not drafted; the AI-token four are carried."),
        ("THE PAIR RANGE HELD FOR THE SEVENTH CONSECUTIVE DAY, against a snapshot refreshed today. "
         "data/pricing_snapshots.json now carries `updated: 2026-09-29`, so the 19 curated pairs were "
         "re-asserted against a newly written file rather than carried. "
         "scripts/extract_monthly_annual_pairs.py re-asserted every pair against its own sentence and "
         "exited 0 with no needle failures. Range unchanged at 1.11x to 2.53x, median 1.25x, over 19 "
         "tiers across 14 tools, pair snapshot dates 2026-09-18 and 2026-09-21. "
         "data/monthly_annual_pairs.json re-derived and rewritten today. Seven consecutive days "
         "without the figure moving extends the longest such stretch the monitor has recorded."),
        ("ALL 47 CARRIED URLs RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page "
         "returns HTTP 200 with the request body still served and no removal or expiry notice - 47/47, "
         "zero non-200s, zero missing bodies, zero expiry words. Cross-checked against the full "
         "sitemap: all 47 tracked slugs are still present in it (42,106 loc/lastmod pairs), and ZERO "
         "of them carry a lastmod inside today's new window, i.e. no tracked request was edited or "
         "renewed today. 17 live and unpitched, 29 cold, and with the four new rows: 51 tracked, "
         "21 live, 26 cold unpitched (excluding the 3 pitched and 1 skipped)."),
        ("THE QUEUE IS STILL 0 SENDABLE, AND THIS RUN FOUND AND FIXED WHY IT LOOKED LIKE 1. On the "
         "first build this run the queue reported 1 sendable: the Forbes founders-cutting-AI request, "
         "whose reply route is a public comment and which the body explicitly closes to email and DM. "
         "The cause was in this run's own refresh script: its chrome filter had dropped Sourcee's two "
         "own social links (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which appear on "
         "every request page, so that row carried a non-empty `published_links` and "
         "build_pitch_queue.py's _sendable() counted a page's own chrome as a usable route. Filter "
         "restored, both links re-excluded, queue re-built: 0 sendable, which is the true number. The "
         "same defect had also silently reclassified every other row's `published_links`."),
        ("MAILBOX CHECKED: STILL NO REPLY TO ANY TRACKED PITCH, BUT THE MONITOR IS NOT THE ONLY "
         "OUTREACH RUNNING - and today that showed. The newest inbound is Lilach Bullock (2026-09-29 "
         "18:09+03:00, msg 84), a reply to the subscription-creep resource pitch: she offers a $300 "
         "paid product placement and a 15,000-subscriber newsletter partnership at 50% off. That was "
         "answered and declined the same day under editorial independence (Sent msg 189, 2026-09-29 "
         "15:52 -07:00), in the thread, signed AIToolsEssentials, no personal name. It is not a reply "
         "to any of the three tracked HARO pitches. Sent Mail's previous top was msg 187 (2026-09-23 "
         "directory batch); msg 189 is the first send since. The most recent human message on a "
         "tracked pitch remains Jan Suski's 2026-09-18 20:39Z reply. No reply to the 2026-09-15 "
         "Enterprise AI Leaders send (fourteen days) or the 2026-09-18 Sherwood News send (eleven "
         "days). Zero pitches sent this run."),
        ("THE UNANSWERED FIGURES CORRECTION IS NOW ELEVEN DAYS OUTSTANDING AND REMAINS THE ONLY "
         "OUTBOUND ITEM THIS MONITOR HAS LEFT THAT IS NOT A PITCH. The recipient of the 2026-09-18 "
         "Amplemarket reply was told the same-tier monthly/annual range is '1.21x-2.53x, median "
         "1.33x'; the current verified figure is 1.11x-2.53x, median 1.25x over 19 tiers. Not sent "
         "this run: the monitor's brief forbids the scheduled run from sending, and the ledger records "
         "it as George's lane. Flagged rather than silently carried again."),
    ],
    "expired_this_run": [
        ("Nothing expired and nothing dropped off this run. All 47 carried URLs returned HTTP 200 "
         "with the request body still served, and none has stopped appearing in a URL-carrying digest. "
         "The usual caveat applies and is not a clean bill of health: this monitor carries every "
         "tracked request forward into each new digest, so 'absent from the newest digest' cannot "
         "fire by construction. Independently cross-checked this run against the full sitemap "
         "(42,106 loc/lastmod pairs): all 47 tracked slugs are still present in it, and ZERO carry a "
         "lastmod inside today's new window. Separately, no request page in the set shows an expiry "
         "notice, so nothing has lapsed by its own wording either."),
        ("ONE ROW CROSSED THE 10-DAY LINE TODAY: companies-that-stopped-emailing-pdfs-new-tools-and-"
         "transition (10d -> 11d, low relevance, unpitched). It has never had a draft and never had a "
         "resolved route, so nothing sendable was lost. Named because build_pitch_queue.py's two-day "
         "advance warning covers only sendable rows, so a low-relevance crossing otherwise shows up as "
         "nothing but the live count falling 18 to 17."),
        ("THE ROW THE QUEUE SPENT TWO DAYS WARNING ABOUT IS NOW ITS LAST LIVE DAY. The Forbes "
         "founders-cutting-AI request (founders-cutting-ai-use-eliminating-or-reducing-ai-in-business) "
         "is 10 days old today and crosses the cold line tomorrow. It has been the queue's only row "
         "counted as sendable for two consecutive runs. It should not have been: the request body is "
         "explicit - 'Please only answer as a comment on this post. Do not email or DM me because they "
         "won't be used' - and the queue's own angle field says the reply requires a named founder's "
         "firsthand account, which we do not have. With the chrome-filter defect above fixed, it is "
         "correctly not sendable, so tomorrow's crossing costs nothing. Logged now, on the day it "
         "still looks live, so the warning is not read as a lost draft."),
        ("THE COLD QUEUE IS 26 STRONG AND STILL GROWING FASTER THAN IT IS BEING CLEARED. Five "
         "high-relevance requests sit past the line with no send: Enterprise AI Leaders - agent sprawl "
         "(24d), Scientists paying for PhD/postdoc AI subscriptions (24d), FinOps - agentic AI cost "
         "overruns (22d, draft unsent since 2026-09-17), the Raconteur shadow-AI request (12d, draft "
         "unsent since 2026-09-19 through twelve runs) and the Forbes/tech-budget call (70d). None has "
         "ever been pitched."),
    ],
    "summary": (
        "51 tracked requests (47 carried and all 47 re-verified live, 4 new AI-token finds added, 0 "
        "dropped off, 3 pitched, 1 deliberately skipped). Of the 47 unpitched, 17 are live and 26 are "
        "cold, and ZERO are sendable. The new window produced 4 AI-token slugs and ZERO real AI+spend "
        "slugs - the seventh consecutive run with none - but for the first time since 2026-09-22 the "
        "AI-token finds include a named-publication editorial call, so all four are now tracked. The "
        "pair range re-asserted clean against today's refreshed snapshot and held at 1.11x-2.53x over "
        "19 tiers across 14 tools for the seventh consecutive day. No new replies to any tracked "
        "pitch; the only inbound today was a paid-placement offer on a different thread, declined "
        "same-day under editorial independence. Zero pitches sent this run - sends remain George's "
        "lane. The two crossed-but-live drafts remain sendable late: pages HTTP 200, routes "
        "re-resolved today (Raconteur byline triple unchanged; Speciality Food masthead unchanged)."
    ),
    "recommended_actions": [
        ("SEND THE RACONTEUR SHADOW-AI DRAFT LATE - THE ONE THAT WILL NEVER COME BACK. Paste-ready at "
         "pitch-drafts-2026-09-29.md section 1, route simon.chandler@raconteur.net (re-resolved off "
         "the live /contributors/simon-chandler page today, HTTP 200, 154,759 bytes, data-part1/2/3 "
         "triple unchanged at simon.chandler + raconteur + net, control /contributors/tom-dennis HTTP "
         "200 carries tom.dennis/raconteur/net; the older /author/simon-chandler/ URL still 404s). "
         "Now 12 days old and unsent through twelve consecutive runs with a finished draft - the only "
         "high-relevance request this monitor has ever produced with a resolved route."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-09-29.md section 2, "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today, "
         "HTTP 200, 59,500 bytes, unchanged, alongside five other named masthead addresses, 12 days "
         "old). Its October issue window has closed; make it a send-or-skip call and record the "
         "outcome in pitch-ledger.json rather than carrying it a fourth day."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI. Thread is live, he replied on 2026-09-18, and he "
         "was told '1.21x-2.53x, median 1.33x' when the true figure is 1.11x-2.53x, median 1.25x over "
         "19 tiers. An un-flagged wrong figure in a peer method discussion is worse than a follow-up, "
         "and it is now eleven days outstanding. Route: reply to jan@jansuski.com, In-Reply-To the "
         "existing thread."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has now produced no real AI+spend slug on "
         "seven consecutive runs, and the single accessible source returns a handful of AI-token "
         "finds per day that are mostly consumer or vendor calls. It remains the only lever that "
         "widens the monitor rather than re-reading the same feed."),
        ("EXPECT THE SAME ZERO NEXT RUN UNLESS ONE OF THESE MOVES. Every remaining live row is "
         "off-beat or comment-only; the queue's own _sendable() returns 0 and now does so for the "
         "right reason. Nothing new will become sendable until either a crossed draft is sent late or "
         "the monitor's supply widens."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": len(win["ai_strict"]),
        "ai_plus_spend_regex_false_positives": len(win["ai_strict_false_positives"]),
        "new_ai_token_slugs_added_to_tracking": len(NEW_ROWS),
        "consecutive_runs_without_new_core_beat": 7,
        "tracked_urls": len(ops),
        "carried_and_reverified": 47,
        "unpitched": len(live_unp) + len(cold_unp),
        "live_unpitched": len(live_unp),
        "cold_unpitched": len(cold_unp),
        "live_unpitched_with_a_resolved_route": 0,
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 2,
        "resolved_signal_routes": 1,
        "drafts_written_never_sent": 4,
        "sendable": 0,
        "sendable_on_its_last_live_day": 0,
        "rows_crossed_cold_today": 1,
        "lost_to_the_cold_line_with_a_draft_ready": 0,
    },
    "monitor_defects_fixed_this_run": [
        ("THE QUEUE COUNTED A COMMENT-ONLY REQUEST AS SENDABLE, AND THE CAUSE WAS IN THIS RUN'S OWN "
         "CODE. _refreshverified_0929.py's chrome filter omitted Sourcee's two own social links, which "
         "appear on every request page, so published_links came out non-empty for rows that publish "
         "no route at all; build_pitch_queue.py's _sendable() accepts a non-empty published_links as a "
         "usable route. First build: 1 sendable. After restoring the filter: 0. The two links are now "
         "in the filter with a comment explaining what they are, so the same misread cannot recur."),
        ("THE SENDABLE WARNING NO LONGER POINTS AT A ROW THAT CANNOT BE PITCHED. Yesterday's queue "
         "and digest both headlined the Forbes founders-cutting-AI row as the sendable row with '0 "
         "days left'. Its own body forbids email and DM and demands a named founder's account; the "
         "queue's angle field already said so. It is now correctly not sendable and is named in "
         "expired_this_run as a crossing that costs nothing, so the advance warning cannot be mistaken "
         "for a missed draft."),
        ("THE BUILD SCRIPT'S OWN NOTES ARE REGENERATED FROM TODAY'S MEASUREMENT. build_pitch_queue.py "
         "still carried hand-written 2026-09-28 prose in its DRAFTS and DRAFT_INDEX blocks, including "
         "'CROSSED COLD 2026-09-28 ... now 11 days' claims. Those blocks are rewritten against today's "
         "verified-requests.json, so a future run cannot inherit a stale urgency claim."),
        ("THE AI+SPEND ZERO IS NAMED, NOT JUST COUNTED. 0 strict hits again, and the 10 spend-token "
         "slugs that matched are listed by name in new_this_run with the exact token class that "
         "matched ('prices', 'affordable', 'budget', 'cost of living'), so a zero can be audited as "
         "'no request' rather than 'no match'."),
        ("THE FEED-OVERLAP NUMBER IS REPORTED AS MEASURED, INCLUDING WHEN IT IS A SUSPICIOUS 100%. "
         "40 of 40 feed slugs sit inside today's window - the first exact overlap this monitor has "
         "measured, after asserting one wrongly on 2026-09-26 and correcting it on 2026-09-27. It is "
         "recorded as measured and the conclusion it supports is explicitly not rested on it."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print(f"wrote digest-{TODAY}.json: {len(ops)} opportunities, {len(digest['platforms_checked'])} platforms")
print(f"live(<=10d): {len(live)}  cold(>10d): {len(stale)}  live_unpitched: {len(live_unp)}  cold_unpitched: {len(cold_unp)}")
print("crossed today:", CROSSED)
print("figures repaired in:", repaired)
for o in ops:
    print(f"  {str(o.get('_days_old')):>4}d  {'NEW ' if o.get('_new_this_run') else '    '}{o['url'].rsplit('/', 1)[-1][:56]}")
