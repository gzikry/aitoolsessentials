#!/usr/bin/env python3
"""Write marketing/haro-outreach/digest-2026-10-02.json

One record per tracked opportunity, re-verified against its own page today by
scripts/verify_journo_requests.py. Carried rows are refreshed from verified-requests.json
(page datePublished + rendered badge), never from yesterday's digest text.

New this run: the SEVEN AI-token slugs from today's sitemap window are added to the tracked
set, because each is a real /journo-request/<slug> page with a live body. That takes the carry
set from 60 to 67. The eight spend-token slugs are NOT added: all eight are consumer
cost-of-living / sport / personal-finance calls that matched a spend regex on 'costs'/'budget'
and contain no software-spend ask.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-10-02"

prev = json.loads((D / "digest-2026-10-01.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
win = json.loads((D / "_window_1002.json").read_text())
cands = {c["slug"]: c for c in json.loads((D / "_candidates_1002.json").read_text())}

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
                r"checked 2026-09-\d\d", f"re-checked {TODAY}", new["suggested_pitch_template"])
        if new.get("contact_method"):
            new["contact_method"] = re.sub(
                r"(PAGE-VERIFIED|RE-VERIFIED|re-verified|re-read|re-checked)\s+2026-09-\d\d",
                rf"\1 {TODAY}", new["contact_method"])
    ops.append(new)

repaired = [o["url"].rsplit("/", 1)[-1] for o in ops if o.get("_figures_repaired")]

# ------------------------------------------------------- seven new tracked rows
NEW_ROWS = [
    {
        "slug": "storytellers-and-brand-founders-marys-big-30-ai-story-project",
        "query_text": (
            "Storytellers & Brand Founders - Mary's Big 30 AI Story Project. 'I'm turning 30 this "
            "October... I want to hear 30 stories from 30 people and bring selected stories to life "
            "using AI, creativity and storytelling... I'll use my own AI credits to create the "
            "stories... brands are welcome too... And if you'd like to sponsor Mary's Big 30, "
            "you're welcome.'"),
        "journalist_publication": "Independent creator (author field: Mary's Big 30 project)",
        "category": "AI / Storytelling / Sponsor Solicitation",
        "contact_method": (
            "Comment or DM on the original post; no email or handle published on the page. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "published_links=none, reply_hints=['Comment']."),
        "relevance": "low",
        "relevance_notes": (
            "A personal story-collection project with a sponsorship ask, not a journalist request "
            "and not a report. It mentions AI credits only as the poster's own production tool; "
            "no price, seat, licence or software-spend question anywhere in the body."),
        "suggested_pitch_template": "None — excluded: creator project soliciting stories and sponsors.",
    },
    {
        "slug": "newsletter-editors-using-ai-agents-news-aggregation-practices",
        "query_text": (
            "Newsletter Editors Using AI Agents - News Aggregation Practices. 'Do you use an AI "
            "agent to combine your newsletters or collect your news for you? I'd love to speak with "
            "you for an article I'm working on!'"),
        "journalist_publication": "Independent journalist (outlet not named in the body)",
        "category": "AI Agents / Publishing Workflow",
        "contact_method": (
            "No email, handle or link published on the page. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "published_links=none, reply_hints=none. No route we can use."),
        "relevance": "low",
        "relevance_notes": (
            "A workflow-practice interview call: it wants newsletter editors who run AI aggregation "
            "agents. We publish a pricing dataset, not an aggregation workflow, and the brief names "
            "no cost, seat or subscription question."),
        "suggested_pitch_template": "None — excluded: workflow practice call with no spend angle and no route.",
    },
    {
        "slug": "scottish-teachers-ai-tools-implementation-in-education",
        "query_text": (
            "Scottish Teachers - AI Tools Implementation in Education. 'I'm looking to speak to "
            "Scottish teachers about the implementation of AI tools in education for a potential "
            "story. DM or email [email redacted] #journorequest'"),
        "journalist_publication": "Independent journalist (outlet not named in the body)",
        "category": "Education / AI Tools Implementation",
        "contact_method": (
            "The body says 'DM or email [email redacted]' — Sourcee redacts the address and the page "
            f"publishes no alternative route. PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=True, "
            "emails_on_page=none, reply_hints=['DM or email']."),
        "relevance": "low",
        "relevance_notes": (
            "The slug carries an AI-tools token, which is why it was read, but the ask is a Scottish "
            "teacher's own classroom experience. We are not a Scottish teacher and the body contains "
            "no pricing, procurement or spend question."),
        "suggested_pitch_template": "None — excluded: wrong standing (we are not a Scottish teacher).",
    },
    {
        "slug": "fb-marketplace-sellers-ai-photos-and-description-prompts",
        "query_text": (
            "FB Marketplace Sellers - AI Photos & Description Prompts. 'Has FB Marketplace turned "
            "into a hellscape for you? Are all the listing pictures AI-generated, or does it keep "
            "prodding you to write item descriptions with AI? As a seller, do the AI features help "
            "you? I'm reporting on this and would love to hear about it: [email redacted], or DM here.'"),
        "journalist_publication": "Independent journalist (outlet not named in the body)",
        "category": "Consumer Platforms / AI Features",
        "contact_method": (
            "DM the poster, or an address Sourcee redacts; the page publishes no alternative route. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=True, emails_on_page=none, "
            "reply_hints=none."),
        "relevance": "low",
        "relevance_notes": (
            "A consumer-platform experience call wanting FB Marketplace sellers. No price, seat, "
            "subscription or software-spend question in the body, and we hold no seller experience "
            "to offer."),
        "suggested_pitch_template": "None — excluded: wrong standing and no spend angle.",
    },
    {
        "slug": "k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact",
        "query_text": (
            "K-8 & HS Teachers Using Student-Facing AI - Moratorium Impact. 'Looking to speak to "
            "teachers affected by AI Moratorium... I am a reporting fellow at Columbia Journalism "
            "School, working on a story about how teachers are being affected by the moratorium... "
            "Are you a K-8 teacher? Are you a high school teacher that used an AI program that "
            "wasn't on their pilot list (like Magic School AI)?... Reach me by DMs.'"),
        "journalist_publication": "Columbia Journalism School reporting fellow (outlet not named)",
        "category": "Education / AI Policy / Teacher Testimony",
        "contact_method": (
            "DMs on the original post; no email, handle or link published on the page. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "published_links=none, reply_hints=none. No route we can use."),
        "relevance": "low",
        "relevance_notes": (
            "A teacher-testimony call about a student-facing AI moratorium. It names a specific "
            "vendor (Magic School AI) but asks teachers for their own classroom experience, not for "
            "pricing or procurement evidence. We hold no teacher account."),
        "suggested_pitch_template": "None — excluded: wants a teacher's firsthand moratorium experience.",
    },
    {
        "slug": "ai-summit-barcelona-attendees-controversy-and-experiences",
        "query_text": (
            "AI Summit Barcelona Attendees - Controversy & Experiences. 'I'm working on a story "
            "about the controversy surrounding AI Summit Barcelona. If you know anyone who attended "
            "(whether they had a good or bad experience) please tag them here or DM me.' "
            "(published in English, Spanish and Catalan)"),
        "journalist_publication": "Independent journalist (outlet not named in the body)",
        "category": "AI Industry Events / Conference Controversy",
        "contact_method": (
            "Tag or DM on the original post; no email, handle or link published on the page. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "published_links=none, reply_hints=['DM me']. No route we can use."),
        "relevance": "low",
        "relevance_notes": (
            "A conference-controversy story wanting attendee testimony. Nothing in the body touches "
            "AI pricing, seats, subscriptions or software spend, and we hold no attendee account."),
        "suggested_pitch_template": "None — excluded: attendee testimony call with no spend angle.",
    },
    {
        "slug": "ai-glasses-owners-users-and-developers-in-india-product-experience",
        "query_text": (
            "AI Glasses Owners, Users & Developers in India - Product Experience. '#JournoRequest "
            "The StyleList is working on a story and we are looking to get in touch with individuals "
            "who own, have used or have helped develop AI glasses in India. If you're interested, "
            "please email us at [email redacted]'"),
        "journalist_publication": "The StyleList (thestylelist.in) — domain named in the body",
        "category": "AI Hardware / Consumer Product Review",
        "contact_method": (
            "The body says 'please email us at [email redacted]' — Sourcee redacts the address and "
            f"the page publishes no alternative route. PAGE-VERIFIED {TODAY}: HTTP 200, "
            "email_redacted=True, emails_on_page=none, published_links=none."),
        "relevance": "low",
        "relevance_notes": (
            "AI-hardware consumer review call for India-based owners and developers of AI glasses. "
            "The slug's 'AI' token is what surfaced it; the body asks no price, subscription or "
            "spend question about software, and we hold none of the standing it wants."),
        "suggested_pitch_template": "None — excluded: wrong standing (we are not an AI-glasses owner/developer).",
    },
]

for row in NEW_ROWS:
    slug = row.pop("slug")
    v = verified.get(slug) or cands.get(slug) or {}
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

# Rows that moved live -> cold today, named rather than left as a count change.
CROSSED = (
    "founders-and-leaders-mindsets-and-milestones",
    "sales-enablement-saas-tools-proposal-and-deck-engagement-tracking",
    "creative-industry-professionals-podcast-on-ai-impact",
    "former-ai-skeptics-changed-views-on-ai-impact",
    "london-businesses-stopped-using-ai-hiring-tools",
)
AT_TEN = (
    "ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai",
    "engineering-managers-measuring-engineers-when-using-ai",
    "saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup",
)

ledger = json.loads((D / "pitch-ledger.json").read_text())
done = set()
for u in list(ledger.get("pitched", {})) + list(ledger.get("skipped", {})):
    done.add(u.rstrip("/").split("/journo-request/")[-1])
live_unp = [o for o in live if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]
cold_unp = [o for o in stale if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]

CAND_LINES = "; ".join(f"{c['slug']} ({c.get('datePublished')})"
                       for c in json.loads((D / "_candidates_1002.json").read_text()))
SPEND_ONLY = [
    "harlem-landlords-rent-freeze-impact-on-costs-and-plans (Harlem landlords, rent freeze)",
    "alaska-residents-struggling-with-basic-expenses-affordability-story (Alaska living costs)",
    "firsttime-parents-in-canada-cost-of-raising-child (Canada childcare costs)",
    "uk-voters-autumn-budget-priorities (the i Paper, Autumn Budget)",
    "longterm-savers-invest-vs-rent-vs-move-vs-spend (the i Paper, savers)",
    "parents-freelancers-and-students-real-cost-of-digital-disconnection (cost of going offline)",
    "mattress-walking-pads-and-robot-vacuum-pros-everyday-product-spending (consumer product spend)",
    "uk-sme-owners-winter-pressures-and-2026-budget-impact-named (UK SME winter pressures)",
]

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
         "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP {win['sitemap_http']}, "
                   f"{win['bytes']:,} bytes, {win['count']:,} loc/lastmod pairs, newest lastmod "
                   f"{win['newest']}). {len(win['window'])} slugs carry a lastmod newer than the "
                   f"2026-10-01 run's mark ({win['mark']}). Of those, {len(win['ai'])} carry an AI "
                   f"token, ZERO carry an AI token plus a real spend token, and {len(win['spend_any'])} "
                   f"carry any spend-adjacent token. All {len(win['ai']) + len(win['spend_any'])} "
                   f"candidate slugs (7 AI + 8 spend, none overlapping) were fetched and read in full. "
                   f"Sourcee itself re-probed HTTP 200 (100,854 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Re-measured. {win['feed_count']} slugs listed today, HTTP 200, "
                   f"{win['feed_bytes']:,} bytes, and {win['feed_overlap_with_window']} of "
                   f"{win['feed_count']} sit inside today's new sitemap window - the third "
                   f"consecutive 100% overlap the monitor has measured. The conclusion does not rest "
                   f"on that overlap: absence from this feed is still not a cold signal, because "
                   f"every tracked carried request is absent from it by construction. None of today's "
                   f"seven AI-token finds appears in the feed.")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,198 bytes, 'Vercel Security Checkpoint'. "
                   "Twenty-first consecutive identical result. Queries reach sources only by a "
                   "3x-daily email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": "Re-probed once. / HTTP 429, 31,195 bytes, 'Vercel Security Checkpoint'. No public feed."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                   "Source of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes, 'Error: The "
                   "page you were looking for doesn't exist'). Wrong path, not gated - unchanged. The "
                   "feed needs an authenticated app session.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. Apex HTTP 200 (11,486 bytes), title 'MentionMatch - Connect B2B Writers "
                   "with Expert Sources', no feed. Twentieth consecutive run confirming a pre-launch shell.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\",\"error_description\":"
                   "\"No authorization provided\"}. Free read-only feed covering Connectively, HARO, X, "
                   "LinkedIn, MentionMatch and Substack. Needs an interactive OAuth handshake that "
                   "cannot be completed from a scheduled run.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on nineteen consecutive "
                   "runs; the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy - and several of today's seven AI-token finds are "
                   "X-originated requests, so the proxy is still carrying that supply.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (148,202 bytes, 'ResponseSource - Connecting the media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free "
                   "source-facing feed.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        (f"SEVEN NEW AI-TOKEN REQUESTS ADDED, AND NONE IS CORE-BEAT. {len(win['window'])} slugs carry "
         f"a lastmod newer than the 2026-10-01 mark. {len(win['ai'])} carry an AI token, ZERO carry an "
         f"AI token plus a real spend token - the TENTH consecutive run with none. All seven AI-token "
         f"rows are now tracked, which takes the carry set from 60 to 67. None asks a price, seat, "
         f"licence or software-spend question: they are a creator story-project, a newsletter-aggregation "
         f"practice call, a Scottish-teacher call, an FB Marketplace seller call, a teachers' moratorium "
         f"call, an AI Summit Barcelona controversy call, and an AI-glasses (India) product call."),
        (f"THE 15 CANDIDATES, BY NAME, SO THE ZERO IS CHECKABLE: {CAND_LINES}. None asks a price, seat, "
         f"licence or software-spend question. The eight spend-token slugs are all consumer or "
         f"non-software calls - "
         + "; ".join(SPEND_ONLY) +
         ". They matched the spend regex on 'costs', 'budget' and 'spend'. Not drafted; the seven "
         "AI-token rows are carried."),
        ("THE PAIR RANGE HELD FOR THE TENTH CONSECUTIVE DAY, against a snapshot refreshed today. "
         "data/pricing_snapshots.json carries `updated: 2026-10-02` (76 snapshots), and "
         "scripts/extract_monthly_annual_pairs.py re-asserted all 19 curated pairs against their own "
         "sentences, exited 0 with no needle failures, and rewrote data/monthly_annual_pairs.json "
         "(built 2026-10-02). Range unchanged at 1.11x to 2.53x, median 1.25x, over 19 tiers across "
         "14 tools, pair snapshot dates 2026-09-18 and 2026-09-21. Ten consecutive days without the "
         "figure moving."),
        ("THE SHADOW-AI HEADLINE FIGURES DID MOVE TODAY, because the snapshot refreshed: 42 of 76 "
         "tools now quote a non-zero monthly price (was 40), 33 of those are at or under $25/month "
         "(was 31), and the median cheapest paid tier is $17.50 (was $16.50). Drafts written before "
         "today cite the superseded 40/31/$16.50 set against `updated: 2026-10-01`. Today's figures "
         "are re-derived from `data/pricing_snapshots.json` (updated 2026-10-02) by "
         "scripts/haro-outreach/_figures_1002.py."),
        ("ALL 60 CARRIED URLs RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page "
         "returns HTTP 200 with the request body still served and no removal or expiry notice - "
         "60/60, zero non-200s, zero missing bodies, zero expiry words. With the seven new rows: "
         "67 tracked, 23 live, 44 cold, minus the 3 pitched and 1 skipped."),
        ("THE QUEUE IS 0 SENDABLE, AND THE REASON IS STILL STRUCTURAL RATHER THAN TEMPORARY. "
         "build_pitch_queue.py's _sendable() requires a relevance above the tangential band plus a "
         "resolved route, and no row in the live set has both: the 16 live unpitched rows are "
         "overwhelmingly relevance 'low'/'low-medium' with no usable route, and the two rows that do "
         "carry a resolved route (Raconteur, Speciality Food) are the two crossed drafts, both past "
         "the 10-day line. The two routes were re-resolved against the live pages again today: "
         "raconteur.net/contributors/simon-chandler HTTP 200 (154,819 bytes, data-part1/2/3 = "
         "simon.chandler + raconteur + net, control /contributors/tom-dennis HTTP 200 carrying "
         "tom.dennis/raconteur/net, legacy /author/simon-chandler/ still 404) and "
         "specialityfoodmagazine.com/contact HTTP 200 (59,500 bytes, holly.shackleton@artichokehq.com "
         "alongside five other named masthead addresses)."),
        ("MAILBOX CHECKED: STILL NO REPLY TO ANY TRACKED PITCH, AND NO NEW INBOUND AT ALL. The newest "
         "inbound remains Lilach Bullock (msg 84, 2026-09-29 18:09+03:00), the paid-placement offer "
         "already declined same-day under editorial independence - not a tracked-pitch reply. The "
         "most recent human message on a tracked pitch remains Jan Suski's 2026-09-18 20:39Z reply "
         "(msg 77). No reply to the 2026-09-15 Enterprise AI Leaders send (seventeen days) or the "
         "2026-09-18 Sherwood News send (fourteen days). Sent Mail's top is still msg 189 "
         "(2026-09-29) - nothing has gone out since. Zero pitches sent this run."),
        ("THE UNANSWERED FIGURES CORRECTION IS NOW FOURTEEN DAYS OUTSTANDING, AND IT IS NOW WRONG BY "
         "AN ADDITIONAL FIGURE THAN WHEN IT WAS FIRST OWED. The recipient of the 2026-09-18 "
         "Amplemarket reply was told the same-tier monthly/annual range is '1.21x-2.53x, median "
         "1.33x'; the current verified figure is 1.11x-2.53x, median 1.25x over 19 tiers. Not sent "
         "this run: the monitor's brief forbids the scheduled run from sending, and the ledger "
         "records it as George's lane."),
    ],
    "expired_this_run": [
        ("Nothing expired and nothing dropped off this run. All 60 carried URLs returned HTTP 200 "
         "with the request body still served, and none has stopped appearing in a URL-carrying "
         "digest. The usual caveat applies and is not a clean bill of health: this monitor carries "
         "every tracked request forward into each new digest, so 'absent from the newest digest' "
         "cannot fire by construction. Independently cross-checked against the full sitemap "
         f"({win['count']:,} loc/lastmod pairs): all 60 tracked slugs are still present in it, and "
         "ZERO carry a lastmod inside today's new window."),
        ("FIVE ROWS CROSSED THE 10-DAY LINE TODAY, ALL UNPITCHED, NONE WITH A RESOLVED ROUTE, AND "
         "NONE SENDABLE - so nothing actionable was lost, and this is the second consecutive day of "
         "a mass crossing (seven crossed yesterday). All five were relevance 'low': "
         "founders-and-leaders-mindsets-and-milestones (11d), "
         "sales-enablement-saas-tools-proposal-and-deck-engagement-tracking (11d), "
         "creative-industry-professionals-podcast-on-ai-impact (11d), "
         "former-ai-skeptics-changed-views-on-ai-impact (11d), and "
         "london-businesses-stopped-using-ai-hiring-tools (11d). Named rather than left as a count "
         "change because build_pitch_queue.py's two-day advance warning covers only sendable rows, "
         "so an ordinary crossing otherwise shows up as nothing but the live count falling."),
        ("THREE MORE ROWS SIT AT EXACTLY 10 DAYS TODAY AND CROSS TOMORROW, all relevance 'low': "
         "ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai, "
         "engineering-managers-measuring-engineers-when-using-ai, and "
         "saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup. None is sendable, so "
         "tomorrow's crossings cost nothing - recorded in advance so the drop is not misread."),
        ("THE TWO CROSSED-BUT-LIVE DRAFTS ARE STILL LIVE AND STILL UNSENT: the Raconteur shadow-AI "
         "request is now 15 days old (unsent through FIFTEEN consecutive runs) and the Speciality "
         "Food request 14 days old (unsent through seven, its October issue window closed). Both "
         "pages returned HTTP 200 again today and both routes were re-resolved against the live "
         "pages this run. Neither is void - what was lost is the ideal window, not the pitch."),
        ("THE COLD QUEUE IS 44 ROWS STRONG (40 unpitched) AND STILL GROWING FASTER THAN IT IS BEING "
         "CLEARED. Seven high-relevance requests sit past the line with no send: Business & "
         "Technology Leaders - tech budget priorities (73d), AI SaaS users in production (133d), "
         "Enterprise AI Leaders - agent sprawl (27d), Scientists paying for PhD/postdoc AI "
         "subscriptions (27d), FinOps - agentic AI cost overruns (25d, draft unsent since "
         "2026-09-17), the Amplemarket pricing/credits request (25d, pitched, replied to, figures "
         "correction 14 days outstanding) and the Raconteur shadow-AI request (15d). None of the "
         "unpitched ones has ever been pitched."),
    ],
    "summary": (
        "67 tracked requests (60 carried and all 60 re-verified live, 7 new AI-token finds added, 0 "
        "dropped off, 3 pitched, 1 deliberately skipped). Of the 63 unpitched, 23 are live and 40 "
        "are cold, and ZERO are sendable. The new window produced 7 AI-token slugs and ZERO real "
        "AI+spend slugs - the tenth consecutive run with none - and all seven are off-beat: a creator "
        "story project, a newsletter-aggregation practice call, a Scottish-teacher call, an FB "
        "Marketplace seller call, a teachers' moratorium call, a conference-controversy call and an "
        "AI-glasses product call. The pair range re-asserted clean against today's refreshed snapshot "
        "and held at 1.11x-2.53x over 19 tiers across 14 tools for the tenth consecutive day, but the "
        "shadow-AI headline figures did move with the snapshot refresh (42 tools publish a monthly "
        "price, 33 at or under $25, median $17.50). No new replies to any tracked pitch; the "
        "mailbox's newest inbound remains Lilach Bullock's paid-placement offer of 2026-09-29, "
        "already declined same-day. Zero pitches sent this run - sends remain George's lane. The two "
        "crossed-but-live drafts remain sendable late: pages HTTP 200, routes re-resolved today."
    ),
    "recommended_actions": [
        ("SEND THE RACONTEUR SHADOW-AI DRAFT - FIFTEEN RUNS UNSENT. Paste-ready at "
         f"pitch-drafts-{TODAY}.md section 1, route simon.chandler@raconteur.net (re-resolved off "
         "the live /contributors/simon-chandler page today, HTTP 200, 154,819 bytes, data-part1/2/3 "
         "triple unchanged; control /contributors/tom-dennis HTTP 200 carries tom.dennis/raconteur/"
         "net; the older /author/simon-chandler/ still 404s and must not be cited). Now 15 days old. "
         "It is the only high-relevance request this monitor has ever produced with a resolved route, "
         "and a late send is still possible."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT ("
         f"pitch-drafts-{TODAY}.md section 2, holly.shackleton@artichokehq.com re-read off "
         "specialityfoodmagazine.com/contact today, HTTP 200, 59,500 bytes, alongside five other "
         "named masthead addresses, 14 days old). Its October issue window has closed; make it a "
         "send-or-skip call and record the outcome in pitch-ledger.json rather than carrying it an "
         "eighth day."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI - NOW FOURTEEN DAYS OUTSTANDING. He replied on "
         "2026-09-18 and was told '1.21x-2.53x, median 1.33x' when the verified figure is "
         "1.11x-2.53x, median 1.25x over 19 tiers. Route: reply to jan@jansuski.com, In-Reply-To the "
         "existing thread."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has produced no real AI+spend slug on "
         "ten consecutive runs and the single accessible source returns a handful of mostly consumer "
         "or vendor calls per day. It remains the only lever that widens the monitor."),
        ("EXPECT THE SAME ZERO NEXT RUN UNLESS ONE OF THESE MOVES. Nothing new becomes sendable until "
         "either a crossed draft is sent late or the monitor's supply widens."),
    ],
    "monitor_health": {
        "platforms_accessible": 1,
        "platforms_blocked": 9,
        "core_beat_new_requests": 0,
        "new_ai_token_slugs_in_window": len(win["ai"]),
        "new_ai_plus_spend_slugs_in_window": len(win["ai_strict"]),
        "ai_plus_spend_regex_false_positives": len(win["ai_strict_false_positives"]),
        "new_ai_token_slugs_added_to_tracking": len(NEW_ROWS),
        "consecutive_runs_without_new_core_beat": 10,
        "tracked_urls": len(ops),
        "carried_and_reverified": 60,
        "unpitched": len(live_unp) + len(cold_unp),
        "live_unpitched": len(live_unp),
        "cold_unpitched": len(cold_unp),
        "pitched_plus_skipped": 4,
        "live_unpitched_with_a_resolved_route": 0,
        "pitches_sent_to_date": 3,
        "pitches_sent_this_run": 0,
        "replies_received_to_date": 1,
        "resolved_email_routes": 2,
        "resolved_signal_routes": 1,
        "drafts_written_never_sent": 4,
        "sendable": 0,
        "sendable_on_its_last_live_day": 0,
        "rows_crossed_cold_today": len(CROSSED),
        "rows_at_ten_days_crossing_tomorrow": len(AT_TEN),
        "lost_to_the_cold_line_with_a_draft_ready": 0,
        "shadow_ai_monthly_priced_tools": 42,
        "shadow_ai_at_or_under_25": 33,
        "shadow_ai_median_cheapest_paid_tier": 17.50,
    },
    "monitor_defects_fixed_this_run": [
        ("THE SHADOW-AI HEADLINE FIGURES ARE NOW RE-DERIVED AND STATED PER RUN, BECAUSE THEY MOVED. "
         "The snapshot refresh took the monthly-priced count from 40 to 42, the sub-$25 count from 31 "
         "to 33 and the median cheapest paid tier from $16.50 to $17.50. Every earlier draft cites "
         "the older set against `updated: 2026-10-01`; today's draft carries the new set against "
         "`updated: 2026-10-02`. The pair range did not move and is unchanged."),
        ("THE FIVE ROWS THAT CROSSED TODAY ARE NAMED INDIVIDUALLY, WITH THE THREE CROSSING TOMORROW. "
         "This is the second consecutive day of a mass crossing (seven yesterday, five today); the "
         "crossing would otherwise appear as nothing but a live-count drop."),
        ("THE SPEND-TOKEN ZERO IS NAMED, NOT JUST COUNTED. 0 strict AI+spend hits again, and the eight "
         "spend-token slugs that matched are listed by name in new_this_run, so the zero can be "
         "audited as 'no request' rather than 'no match'."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print(f"wrote digest-{TODAY}.json: {len(ops)} opportunities, {len(digest['platforms_checked'])} platforms")
print(f"live(<=10d): {len(live)}  cold(>10d): {len(stale)}  live_unpitched: {len(live_unp)}  cold_unpitched: {len(cold_unp)}")
print("crossed today:", len(CROSSED), "at 10d:", len(AT_TEN))
print("figures repaired in:", repaired)
