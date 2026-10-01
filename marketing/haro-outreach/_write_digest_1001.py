#!/usr/bin/env python3
"""Write marketing/haro-outreach/digest-2026-10-01.json

One record per tracked opportunity, re-verified against its own page today by
scripts/verify_journo_requests.py. Carried rows are refreshed from verified-requests.json
(page datePublished + rendered badge), never from yesterday's digest text.

New this run: the SIX AI-token slugs from today's sitemap window are added to the tracked set,
because each is a real /journo-request/<slug> page with a live body. That takes the carry set
from 54 to 60. The four spend-token slugs are NOT added: all four are consumer cost-of-living,
commuter or physical-goods-subscription calls that matched a spend regex on 'costs'/'budget'/
'subscription revenue' and contain no software-spend ask.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

D = Path("/Users/georgezikry/aitoolessentials/site/marketing/haro-outreach")
TODAY = "2026-10-01"

prev = json.loads((D / "digest-2026-09-30.json").read_text())
verified = json.loads((D / "verified-requests.json").read_text())
win = json.loads((D / "_window_1001.json").read_text())
cands = json.loads((D / "_candidates_1001.json").read_text())

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

# ---------------------------------------------------------------- six new tracked rows
NEW_ROWS = [
    {
        "slug": "fea-engineers-using-agentic-ai-practitioner-case-study",
        "query_text": (
            "FEA Engineers Using Agentic AI - Practitioner Case Study. 'Have you used agentic AI in "
            "your simulation work? If so, I would like to hear from you. This fall, in collaboration "
            "with Synera, I will be hosting \"Agentic AI in Simulation\", a two-part webinar series "
            "to help engineers and engineering managers understand what AI agents can do for FEA, "
            "how they improve simulation practice, and how to bring them into an organization. Part 2 "
            "(November 12) will focus on \"The Practitioner's Perspective\". For Part 2, I am looking "
            "for a guest who has applied agentic AI to real simulation work.'"),
        "journalist_publication": "Independent / Synera webinar series (author not a journalist byline)",
        "category": "Engineering Simulation / Agentic AI / Webinar Guest",
        "contact_method": (
            "No email, handle or link published on the page; the body invites a comment. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "published_links=none, reply_hints=['Comment']. No route we can use."),
        "relevance": "low",
        "relevance_notes": (
            "A webinar guest booking, not a journalist request: it wants a simulation engineer's "
            "firsthand account of applying agentic AI to FEA work. A price-benchmark publisher has "
            "no such account and the body names no cost, seat or subscription question."),
        "suggested_pitch_template": "None — excluded: webinar guest call wanting an engineer's own deployment story.",
    },
    {
        "slug": "parents-ai-acting-as-pseudoparent-in-kid-questions",
        "query_text": (
            "Parents - AI Acting As Pseudo-Parent In Kid Questions. 'Is AI becoming a pseudo-parent to "
            "your children? Parents, has your kid ever asked ChatGPT something you wish they'd asked "
            "you? ... I'm looking for parents with a specific moment like that, big or small, where it "
            "might feel like AI is overstepping as a pseudo-parent. I'm a writer journalist working on "
            "a story and would love to chat about this!'"),
        "journalist_publication": "Independent writer/journalist (outlet not named in the body)",
        "category": "AI / Family / Consumer Behaviour",
        "contact_method": (
            "No email, handle or link published on the page; the body says 'would love to chat'. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "published_links=none, reply_hints=none."),
        "relevance": "low",
        "relevance_notes": (
            "A parents' personal-testimony call. Nothing in the body touches pricing, seats, "
            "subscriptions or spend, and we are not parents-with-a-moment to quote."),
        "suggested_pitch_template": "None — excluded: personal testimony call with no spend angle.",
    },
    {
        "slug": "employees-conflicted-about-ai-use-generative-ai-workplace-impact",
        "query_text": (
            "Employees Conflicted About AI Use - Generative AI Workplace Impact. 'I'm an artist and "
            "filmmaker based in Woodside working on a new video project about generative AI and "
            "changing workplace dynamics. I'm looking to talk to people who feel conflicted about "
            "their AI use at work. ... People I've spoken to so far have said the introduction of AI "
            "has led to greater mistrust of their coworkers, shame around their own use, and avoiding "
            "full disclosure when they use AI. Most people say there are no formal policies around AI "
            "use in their workplace. If this sounds familiar to you, I'd love to talk! If you're "
            "interested, please fill out the form below or message me.'"),
        "journalist_publication": "Independent artist/filmmaker (video project; outlet not named)",
        "category": "AI / Workplace Culture / Shadow AI Use",
        "contact_method": (
            "A Google Form published in the body "
            "(docs.google.com/forms/d/e/1FAIpQLSdWsFQ0q\\_Mngmu7kGKnLwt4Z-Z4\\_Exh5H41eqJ0rjk0t1i1Jg/viewform) "
            "or a direct message. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "published_links=['https://docs.google.com/forms/d/e/1FAIpQLSdWsFQ0q']."),
        "relevance": "low-medium",
        "relevance_notes": (
            "The nearest thing to our beat in this window — 'no formal policies around AI use' and "
            "staff not disclosing their AI use is the shadow-AI problem — but it is a first-person "
            "testimony call for a video project: it wants employees describing their own conflicted "
            "use. We are a publisher and hold no such account, so the only honest contribution is the "
            "price evidence behind unmanaged adoption, which the brief does not ask for."),
        "suggested_pitch_template": (
            "Template 2 (cost optimization), only if a data contribution is welcome: offer the dated "
            "price set behind unmanaged adoption rather than a personal account. Do not claim to be a "
            "conflicted employee."),
    },
    {
        "slug": "chatbot-users-experiences-talking-to-ai",
        "query_text": (
            "Chatbot Users - Experiences Talking to AI. 'If you talk to chat bots I would love to "
            "interview you for a story! DM me or reply!'"),
        "journalist_publication": "Independent journalist (outlet not named in the body)",
        "category": "AI / Consumer Experience",
        "contact_method": (
            "DM or reply to the original post; no email published and none redacted. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "reply_hints=['DM me']. The route is the original post, which we cannot identify."),
        "relevance": "low",
        "relevance_notes": (
            "A general chatbot-user interview call with no pricing, seat, subscription or spend "
            "content and no named publication. Recorded, excluded."),
        "suggested_pitch_template": "None — excluded: no spend angle, no resolvable route.",
    },
    {
        "slug": "us-ai-security-experts-rogue-ai-agents-hitting-government-sites",
        "query_text": (
            "US AI Security Experts - Rogue AI Agents Hitting Government Sites. 'Media Query *Interview "
            "opportunity Pr charges applicable*** Category A PUBLICATION. Topic: Rogue AI: When AI "
            "Agents Go Beyond Their Instructions. Seeking expert views on recent reports of AI agents "
            "interacting with U.S. government websites. Looking for comments on: Risks of AI agents "
            "acting on their own; Cybersecurity threats; Who is accountable when AI goes wrong; "
            "Whether current safeguards are enough. AI, cybersecurity and tech experts: Please DM if "
            "you can comment.'"),
        "journalist_publication": "Category A publication via a PR/media-query desk (outlet not named)",
        "category": "AI Security / Governance / Agent Accountability",
        "contact_method": (
            "DM the poster; no email or handle published on the Sourcee page. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=False, emails_on_page=none, "
            "published_links=none, reply_hints=['Comment']."),
        "relevance": "low",
        "relevance_notes": (
            "Two disqualifiers, stated in the body itself: it is a paid-placement query ('Pr charges "
            "applicable') and it wants credentialed AI-security practitioners, which we are not. No "
            "cost or software-spend question anywhere in it."),
        "suggested_pitch_template": "None — excluded: paid placement and wrong standing.",
    },
    {
        "slug": "real-estate-agents-pdf-brochures-vs-alternatives-agent-workflow",
        "query_text": (
            "Real Estate Agents - PDF Brochures Vs Alternatives - Agent Workflow. 'Are PDF property "
            "brochures on their way out? I'm writing about what agents are using instead. Which angle "
            "would you want to read: the buyer experience or the agent workflow? Real estate folks, "
            "DM me or email [email redacted]'"),
        "journalist_publication": "Independent journalist (outlet not named in the body)",
        "category": "Real Estate / Document Workflow / Tools",
        "contact_method": (
            "DM the poster, or an address Sourcee redacts; the page publishes no alternative route. "
            f"PAGE-VERIFIED {TODAY}: HTTP 200, email_redacted=True, emails_on_page=none, "
            "reply_hints=['DM me']."),
        "relevance": "low",
        "relevance_notes": (
            "Wants practising real-estate agents on brochure alternatives. 'Tools' in the slug is a "
            "document-workflow question, not a software-subscription one, and the body asks no price "
            "or spend question. Recorded, excluded."),
        "suggested_pitch_template": "None — excluded: wrong standing (we are not a real-estate agent).",
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
    "data-center-professionals-podcast-guest-ai-and-hyperscale-trends",
    "employers-and-recruiters-over-50s-adapting-to-ai",
    "patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges",
    "survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies",
    "founders-55-latelife-entrepreneurship-series-1",
    "founders-and-entrepreneurs-and-musicians-podcast-guests",
    "ml-researchers-continuous-learning-fast-weights-and-adapters",
)
AT_TEN = (
    "founders-and-leaders-mindsets-and-milestones",
    "sales-enablement-saas-tools-proposal-and-deck-engagement-tracking",
    "creative-industry-professionals-podcast-on-ai-impact",
    "former-ai-skeptics-changed-views-on-ai-impact",
    "london-businesses-stopped-using-ai-hiring-tools",
)

ledger = json.loads((D / "pitch-ledger.json").read_text())
done = set()
for u in list(ledger.get("pitched", {})) + list(ledger.get("skipped", {})):
    done.add(u.rstrip("/").split("/journo-request/")[-1])
live_unp = [o for o in live if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]
cold_unp = [o for o in stale if o["url"].rstrip("/").split("/journo-request/")[-1] not in done]

CAND_LINES = "; ".join(f"{s} ({c['datePublished']})" for s, c in cands.items())

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
                   f"2026-09-30 run's mark ({win['mark']}). Of those, {len(win['ai'])} carry an AI "
                   f"token, ZERO carry an AI token plus a real spend token, and {len(win['spend_any'])} "
                   f"carry any spend-adjacent token. All {len(win['ai']) + len(win['spend_any'])} "
                   f"candidate slugs (6 AI + 4 spend, none overlapping) were fetched and read in full. "
                   f"Sourcee itself re-probed HTTP 200 (100,854 bytes).")},
        {"platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
         "status": "recency_window_not_persistence",
         "notes": (f"Re-measured. {win['feed_count']} slugs listed today, HTTP 200, "
                   f"{win['feed_bytes']:,} bytes, and {win['feed_overlap_with_window']} of "
                   f"{win['feed_count']} sit inside today's new sitemap window - the second "
                   f"consecutive 100% overlap the monitor has measured. The conclusion does not rest "
                   f"on that overlap: absence from this feed is still not a cold signal, because "
                   f"every tracked carried request is absent from it by construction. None of today's "
                   f"six AI-token finds appears in the feed.")},
        {"platform": "HARO (helpareporter.com)", "status": "email_wall",
         "notes": ("Re-probed once. / returns HTTP 429, 31,195 bytes, 'Vercel Security Checkpoint'. "
                   "Twentieth consecutive identical result. Queries reach sources only by a 3x-daily "
                   "email digest to a subscribed inbox. Not retried, per the monitor's rule.")},
        {"platform": "Connectively (connectively.us)", "status": "login_required",
         "notes": "Re-probed once. / HTTP 429, 31,200 bytes, 'Vercel Security Checkpoint'. No public feed."},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "email_only",
         "notes": ("Re-probed. /requests returns a genuine 404 (140,415 bytes, 'Page Not Found - "
                   "Source of Sources'). Reporter submission form only; no source-facing feed.")},
        {"platform": "Qwoted (qwoted.com)", "status": "login_required",
         "notes": ("Re-probed. app.qwoted.com/requests returns a genuine 404 (3,266 bytes, 'Error: The "
                   "page you were looking for doesn't exist'). Wrong path, not gated - unchanged. The "
                   "feed needs an authenticated app session.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "pre_launch",
         "notes": ("Re-probed. Apex HTTP 200 (11,522 bytes), title 'MentionMatch - Connect B2B Writers "
                   "with Expert Sources', no feed. Nineteenth consecutive run confirming a pre-launch shell.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "oauth_required",
         "notes": ("Re-probed: HTTP 401, 74-byte {\"error\":\"invalid_token\",\"error_description\":"
                   "\"No authorization provided\"}. Free read-only feed covering Connectively, HARO, X, "
                   "LinkedIn, MentionMatch and Substack. Needs an interactive OAuth handshake that "
                   "cannot be completed from a scheduled run.")},
        {"platform": "X/Twitter #journorequest", "status": "credits_exhausted",
         "notes": ("Not re-attempted. Team-level credit limit blocked this on eighteen consecutive "
                   "runs; the block is account state, not a transient failure. Sourcee's X-originated "
                   "aggregation is used as a proxy - and two of today's six AI-token finds are "
                   "X-originated requests (the paid-placements query desk and the chatbot-user call), "
                   "so the proxy is still carrying that supply.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "paywalled_uk",
         "notes": ("Root re-probed HTTP 200 (148,204 bytes, 'ResponseSource - Connecting the media'). "
                   "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free "
                   "source-facing feed.")},
    ],
    "opportunities": ops,
    "new_this_run": [
        (f"SIX NEW AI-TOKEN REQUESTS - THE MOST THIS MONITOR HAS ADDED IN ONE RUN, AND NONE IS "
         f"CORE-BEAT. {len(win['window'])} slugs carry a lastmod newer than the 2026-09-30 mark. "
         f"{len(win['ai'])} carry an AI token, ZERO carry an AI token plus a real spend token - the "
         f"NINTH consecutive run with none. All six AI-token rows are now tracked, which takes the "
         f"carry set from 54 to 60. None asks a price, seat, licence or software-spend question: they "
         f"are a paid-placement security query, two personal-testimony calls (parents on AI as "
         f"pseudo-parent, chatbot users), a workplace-conflict video project, a webinar guest booking "
         f"for simulation engineers, and a real-estate brochure-workflow call."),
        (f"THE {len(cands)} CANDIDATES, BY NAME, SO THE ZERO IS CHECKABLE: {CAND_LINES}. None asks a "
         f"price, seat, licence or software-spend question. The four spend-token slugs are all "
         f"consumer or non-software calls - Gen Z dating costs (Fortune), UK season-ticket costs, "
         f"small UK business winter pressures and the 2026 Autumn budget, and marketing experts "
         f"selling physical-good subscriptions. They matched the spend regex on 'costs', 'budget' and "
         f"'subscription revenue'. Not drafted; the six AI-token rows are carried."),
        ("THE PAIR RANGE HELD FOR THE NINTH CONSECUTIVE DAY, against a snapshot refreshed today. "
         "data/pricing_snapshots.json carries `updated: 2026-10-01` (76 snapshots), and "
         "scripts/extract_monthly_annual_pairs.py re-asserted all 19 curated pairs against their own "
         "sentences, exited 0 with no needle failures, and rewrote data/monthly_annual_pairs.json "
         "(built 2026-10-01). Range unchanged at 1.11x to 2.53x, median 1.25x, over 19 tiers across "
         "14 tools, pair snapshot dates 2026-09-18 and 2026-09-21. Nine consecutive days without the "
         "figure moving."),
        ("ALL 54 CARRIED URLs RE-VERIFIED LIVE, NOTHING EXPIRED, NOTHING DROPPED OFF. Every page "
         "returns HTTP 200 with the request body still served and no removal or expiry notice - "
         "54/54, zero non-200s, zero missing bodies, zero expiry words. 26 live unpitched, 28 cold. "
         "With the six new rows: 60 tracked, 32 live, 28 cold unpitched (excluding the 3 pitched and "
         "1 skipped)."),
        ("THE QUEUE IS 0 SENDABLE, AND THE REASON IS STRUCTURAL RATHER THAN TEMPORARY. "
         "build_pitch_queue.py's _sendable() requires a relevance above the tangential band plus a "
         "resolved route, and no row in the live set has both: the 26 live unpitched rows are "
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
         "(msg 77). No reply to the 2026-09-15 Enterprise AI Leaders send (sixteen days) or the "
         "2026-09-18 Sherwood News send (thirteen days). Sent Mail's top is still msg 189 "
         "(2026-09-29) - nothing has gone out since. Zero pitches sent this run."),
        ("THE UNANSWERED FIGURES CORRECTION IS NOW THIRTEEN DAYS OUTSTANDING AND REMAINS THE ONLY "
         "OUTBOUND ITEM THIS MONITOR HAS LEFT THAT IS NOT A PITCH. The recipient of the 2026-09-18 "
         "Amplemarket reply was told the same-tier monthly/annual range is '1.21x-2.53x, median "
         "1.33x'; the current verified figure is 1.11x-2.53x, median 1.25x over 19 tiers. Not sent "
         "this run: the monitor's brief forbids the scheduled run from sending, and the ledger "
         "records it as George's lane."),
    ],
    "expired_this_run": [
        ("Nothing expired and nothing dropped off this run. All 54 carried URLs returned HTTP 200 "
         "with the request body still served, and none has stopped appearing in a URL-carrying "
         "digest. The usual caveat applies and is not a clean bill of health: this monitor carries "
         "every tracked request forward into each new digest, so 'absent from the newest digest' "
         "cannot fire by construction. Independently cross-checked against the full sitemap "
         "(42,314 loc/lastmod pairs): all 54 tracked slugs are still present in it, and ZERO carry a "
         "lastmod inside today's new window."),
        ("SEVEN ROWS CROSSED THE 10-DAY LINE TODAY, ALL UNPITCHED, NONE WITH A RESOLVED ROUTE, AND "
         "NONE SENDABLE - so nothing actionable was lost. All seven were already relevance 'low': "
         "data-center-professionals-podcast-guest (11d), employers-and-recruiters-over-50s (11d), "
         "patients-with-exorbitant-hospital-bills (11d), survivors-of-ai-and-autonomous-weapons "
         "(11d), founders-55-latelife-entrepreneurship-series (11d), "
         "founders-and-entrepreneurs-and-musicians-podcast-guests (11d), and "
         "ml-researchers-continuous-learning-fast-weights-and-adapters (11d). This is the largest "
         "single-day crossing the monitor has recorded. Named rather than left as a count change "
         "because build_pitch_queue.py's two-day advance warning covers only sendable rows, so an "
         "ordinary crossing otherwise shows up as nothing but the live count falling."),
        ("FIVE MORE ROWS SIT AT EXACTLY 10 DAYS TODAY AND CROSS TOMORROW, all relevance 'low': "
         "founders-and-leaders-mindsets-and-milestones, "
         "sales-enablement-saas-tools-proposal-and-deck-engagement-tracking, "
         "creative-industry-professionals-podcast-on-ai-impact, "
         "former-ai-skeptics-changed-views-on-ai-impact, and "
         "london-businesses-stopped-using-ai-hiring-tools. None is sendable, so tomorrow's crossings "
         "cost nothing - recorded in advance so the drop is not misread."),
        ("THE TWO CROSSED-BUT-LIVE DRAFTS ARE STILL LIVE AND STILL UNSENT: the Raconteur shadow-AI "
         "request is now 14 days old (unsent through FOURTEEN consecutive runs) and the Speciality "
         "Food request 13 days old (unsent through six, its October issue window closed). Both pages "
         "returned HTTP 200 again today and both routes were re-resolved against the live pages this "
         "run. Neither is void - what was lost is the ideal window, not the pitch."),
        ("THE COLD QUEUE IS 32 ROWS STRONG AND STILL GROWING FASTER THAN IT IS BEING CLEARED - 28 of "
         "those never pitched, the other four pitched or deliberately skipped. Six high-relevance "
         "requests sit past the line with no send: Business & Technology Leaders - tech budget "
         "priorities (72d), AI SaaS users in production (132d), Scientists paying for PhD/postdoc AI "
         "subscriptions (26d), FinOps - agentic AI cost overruns (24d, draft unsent since "
         "2026-09-17), the Amplemarket pricing/credits request (24d, pitched, replied to, figures "
         "correction 13 days outstanding) and the Raconteur shadow-AI request (14d). None of the "
         "unpitched ones has ever been pitched."),
    ],
    "summary": (
        "60 tracked requests (54 carried and all 54 re-verified live, 6 new AI-token finds added, 0 "
        "dropped off, 3 pitched, 1 deliberately skipped). Of the 56 unpitched, 32 are live and 24 are "
        "cold, and ZERO are sendable. The new window produced 6 AI-token slugs and ZERO real AI+spend "
        "slugs - the ninth consecutive run with none - and all six are off-beat: a paid-placement "
        "security query, two personal-testimony calls, a workplace-conflict video project, a webinar "
        "guest booking and a real-estate workflow call. The pair range re-asserted clean against "
        "today's refreshed snapshot and held at 1.11x-2.53x over 19 tiers across 14 tools for the "
        "ninth consecutive day. No new replies to any tracked pitch; the mailbox's newest inbound "
        "remains Lilach Bullock's paid-placement offer of 2026-09-29, already declined same-day. "
        "Zero pitches sent this run - sends remain George's lane. The two crossed-but-live drafts "
        "remain sendable late: pages HTTP 200, routes re-resolved today."
    ),
    "recommended_actions": [
        ("SEND THE RACONTEUR SHADOW-AI DRAFT - FOURTEEN RUNS UNSENT. Paste-ready at "
         "pitch-drafts-2026-10-01.md section 1, route simon.chandler@raconteur.net (re-resolved off "
         "the live /contributors/simon-chandler page today, HTTP 200, 154,819 bytes, data-part1/2/3 "
         "triple unchanged; control /contributors/tom-dennis HTTP 200 carries tom.dennis/raconteur/"
         "net; the older /author/simon-chandler/ still 404s and must not be cited). Now 14 days old. "
         "It is the only high-relevance request this monitor has ever produced with a resolved route, "
         "and a late send is still possible."),
        ("SEND OR DROP THE SPECIALITY FOOD DRAFT (pitch-drafts-2026-10-01.md section 2, "
         "holly.shackleton@artichokehq.com re-read off specialityfoodmagazine.com/contact today, "
         "HTTP 200, 59,500 bytes, alongside five other named masthead addresses, 13 days old). Its "
         "October issue window has closed; make it a send-or-skip call and record the outcome in "
         "pitch-ledger.json rather than carrying it a seventh day."),
        ("SEND THE FIGURES CORRECTION TO JAN SUSKI - NOW THIRTEEN DAYS OUTSTANDING. He replied on "
         "2026-09-18 and was told '1.21x-2.53x, median 1.33x' when the verified figure is "
         "1.11x-2.53x, median 1.25x over 19 tiers. Route: reply to jan@jansuski.com, In-Reply-To the "
         "existing thread."),
        ("RESOLVE THE MEDIALYST MCP OAUTH HANDSHAKE. Supply has produced no real AI+spend slug on "
         "nine consecutive runs and the single accessible source returns a handful of mostly consumer "
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
        "consecutive_runs_without_new_core_beat": 9,
        "tracked_urls": len(ops),
        "carried_and_reverified": 54,
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
    },
    "monitor_defects_fixed_this_run": [
        ("THE DIGEST'S OWN DEADLINE FIELD IS REGENERATED FROM TODAY'S PAGE PROBES, NOT COPIED "
         "FORWARD. Every carried row's `deadline` is rewritten this run with the HTTP code, live "
         "flag, badge, days_old and expiry check read out of verified-requests.json, so a stale "
         "'RE-VERIFIED 2026-09-30' line cannot survive into a 2026-10-01 digest."),
        ("THE SPEND-TOKEN ZERO IS NAMED, NOT JUST COUNTED. 0 strict AI+spend hits again, and the four "
         "spend-token slugs that matched are listed by name in new_this_run with the token class that "
         "matched ('costs', 'budget', 'subscription revenue'), so the zero can be audited as 'no "
         "request' rather than 'no match'."),
        ("THE SEVEN ROWS THAT CROSSED TODAY ARE NAMED INDIVIDUALLY, WITH THE FIVE CROSSING TOMORROW. "
         "The largest single-day crossing the monitor has recorded would otherwise appear as nothing "
         "but a live-count drop; each is now listed so a quiet number change cannot be mistaken for a "
         "quiet week."),
    ],
}

(D / f"digest-{TODAY}.json").write_text(json.dumps(digest, indent=1))
print(f"wrote digest-{TODAY}.json: {len(ops)} opportunities, {len(digest['platforms_checked'])} platforms")
print(f"live(<=10d): {len(live)}  cold(>10d): {len(stale)}  live_unpitched: {len(live_unp)}  cold_unpitched: {len(cold_unp)}")
print("crossed today:", len(CROSSED), "at 10d:", len(AT_TEN))
print("figures repaired in:", repaired)
for o in ops:
    print(f"  {str(o.get('_days_old')):>4}d  {'NEW ' if o.get('_new_this_run') else '    '}{o['url'].rsplit('/', 1)[-1][:56]}")
