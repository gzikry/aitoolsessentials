#!/usr/bin/env python3
"""Build a ranked, actionable pitch queue from the HARO/Sourcee digests.

The monitor's problem was never supply: it flagged 43 opportunities across 29 unique URLs in
12 days while nothing was ever pitched. The bottleneck is the send step, so this turns the
accumulated digests into one queue George can clear in a single pass.

Design notes:
  * Dedupe by URL, not by digest date. The same request recurs for days (the FinOps one
    appeared in six consecutive digests) and listing it six times buries the queue.
  * Age comes from the PAGE, not from the digest. `verified-requests.json` (written by
    scripts/verify_journo_requests.py) holds `datePublished` read off each request page. This
    replaces an earlier fallback that used the digest's first-seen date whenever the deadline
    text carried no date - a digest saying "Open (posted >1 month ago)" made a 190-day-old
    request look 8 days old, which floated two dead requests to the top of the live list.
  * Rank by freshness first (a request posted yesterday outranks a stale one whatever its
    keyword score), then by relevance. Anything older than STALE_DAYS and never refreshed is
    cold, and anything the last digest stopped carrying is shown as dropped off.
  * Name the reply route explicitly and say whether it is automatable. Every platform here
    except Sourcee is closed, and Sourcee's own requests ask for a LinkedIn DM - that is why
    zero pitches have ever gone out. Surfacing it per row makes the blocker visible.
  * Never re-list anything already in the ledger.
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
OUT = SITE_ROOT / "marketing" / "haro-outreach"
LEDGER = OUT / "pitch-ledger.json"
QUEUE_MD = OUT / "pitch-queue.md"
# Page-verified facts, keyed by slug. Written by scripts/verify_journo_requests.py.
VERIFIED = OUT / "verified-requests.json"

# A request older than this, never refreshed, is cold in practice even if the page is live.
STALE_DAYS = 10

# Band order, best first. "medium-high" was missing from this map, so the three requests carrying
# that label — including the Anthropic subscription-value request that has a finished draft and the
# only published direct channel in the whole queue — fell through RELEVANCE_RANK.get()'s default of
# 9 and were ranked BELOW every "low" request. That is the same defect class the previous run fixed
# for "high on topic, low on currency", reached through a different label: the digests use free text,
# so the map has to be defensive about every variant rather than the handful that were noticed.
RELEVANCE_RANK = {"high": 0, "medium-high": 0.5, "medium": 1, "low-medium": 2, "medium-low": 2,
                  "low": 3, "tangential": 4, "unknown": 5}


def _rel_rank(label: str) -> float:
    """Rank a (possibly messy) relevance label, never silently dropping it below 'low'."""
    r = (label or "").strip().lower()
    if r in RELEVANCE_RANK:
        return RELEVANCE_RANK[r]
    # "high" / "medium" / "low" as a prefix or with a trailing qualifier still bands correctly.
    for band in ("high", "medium", "low"):
        if r.startswith(band):
            return RELEVANCE_RANK[band]
    return RELEVANCE_RANK["unknown"]


def _load_verified() -> dict:
    if VERIFIED.exists():
        try:
            return json.loads(VERIFIED.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def _verified_for(url: str, verified: dict) -> dict:
    slug = url.rstrip("/").split("/journo-request/")[-1]
    return verified.get(slug) or {}


def _canon(url: str) -> str:
    """Dedupe key: the same request appears with and without the www. host in the digests."""
    return re.sub(r"^https?://(?:www\.)?sourcee\.app/", "https://www.sourcee.app/", url.strip())


def _load_ledger() -> dict:
    if LEDGER.exists():
        try:
            return json.loads(LEDGER.read_text())
        except json.JSONDecodeError:
            pass
    return {"pitched": {}, "skipped": {}, "notes": "URL -> date/status. Written by hand or by the agent."}


def _days_old(text: str, first_seen: str | None) -> float | None:
    """Prefer a datePublished/date in the digest's deadline text, else the first sighting."""
    stamps = re.findall(r"(20\d{2}-\d{2}-\d{2})", text or "")
    for s in stamps:
        try:
            d = datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - d).total_seconds() / 86400
        except ValueError:
            continue
    if first_seen:
        try:
            d = datetime.strptime(first_seen, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - d).total_seconds() / 86400
        except ValueError:
            return None
    return None


def _norm_rel(rel: str) -> str:
    """Normalise a digest's relevance label.

    The digests are written by hand and use free text: "medium (adjacent, not core AI-spend)",
    "high on topic, low on currency", "low-medium (adjacent; no cost or spend angle in the text)",
    "tangential". Stripping only at "(" left "high on topic, low on currency" unmapped, and
    RELEVANCE_RANK.get() then returned the default 9 — so the two highest-scoring requests in the
    queue were ranked below every "low" one. Parentheticals are dropped and the leading qualifier
    is mapped onto a known band.
    """
    r = (rel or "").strip().lower()
    r = r.split("(")[0].strip().strip(",;").strip()
    # "high on topic, low on currency" -> the qualifier is the operative half
    if "," in r:
        parts = [p.strip() for p in r.split(",") if p.strip()]
        r = parts[-1] if len(parts) > 1 else parts[0]
    r = r.replace("high on topic", "medium").replace("low on currency", "medium")
    r = {"tangential": "low", "adjacent": "low-medium"}.get(r, r)
    r = r.strip().rstrip("-").strip()
    return r or "unknown"


def collect() -> list[dict]:
    """Merge every digest into one record per URL, keeping the richest fields."""
    seen: dict[str, dict] = {}
    verified = _load_verified()
    digest_sizes: dict[str, int] = {}
    digest_urls: dict[str, int] = {}
    digests = sorted(OUT.glob("digest-*.json"))
    for f in digests:
        day = f.stem.replace("digest-", "")
        try:
            d = json.loads(f.read_text())
        except json.JSONDecodeError:
            continue
        ops = d.get("opportunities") or []
        digest_sizes[day] = len(ops)
        with_url = 0
        for op in ops:
            url = (op.get("url") or "").strip()
            if not url:
                continue
            with_url += 1
            url = _canon(url)
            # Index/browse pages are not requests: they carry no deadline, no journalist and
            # no reply route, yet they scored as "high relevance" and outranked real requests.
            # Two shapes seen: /media-outlets/<name>/journo-requests and
            # /topics/<topic>/journo-requests. A real request always lives at /journo-request/<slug>.
            if "/media-outlets/" in url or "/topics/" in url:
                continue
            if "/journo-request/" not in url:
                continue
            rel = _norm_rel(op.get("relevance", ""))
            rec = seen.setdefault(url, {
                "url": url,
                "first_seen": day,
                "last_seen": day,
                "appearances": 0,
                "relevance": rel,
                "deadline": "",
                "contact": "",
                "category": "",
                "publication": "",
                "query_text": "",
                "angle": "",
            })
            rec["last_seen"] = max(rec["last_seen"], day)
            rec["appearances"] += 1
            # keep the strongest relevance and the longest text we have
            if _rel_rank(rel) < _rel_rank(rec["relevance"]):
                rec["relevance"] = rel
            for src, dst, longest in (
                ("deadline", "deadline", False),
                ("contact_method", "contact", False),
                ("category", "category", False),
                ("journalist_publication", "publication", False),
                ("query_text", "query_text", True),
                ("suggested_pitch_template", "angle", True),
            ):
                v = (op.get(src) or "").strip()
                if v and (longest is False or len(v) > len(rec[dst])):
                    rec[dst] = v
        digest_urls[day] = with_url
    # A digest carrying zero URLs holds no membership information — the 2026-09-16 digest
    # recorded nine opportunities by prose with no `url` field at all (they have since been
    # re-keyed, and scripts/haro_monitor.py's undefined `run()` call that produced them is
    # fixed). Treating such a digest as "did not carry this request" flagged every row in the
    # queue as dropped off at once, which is a data defect masquerading as a cold signal.
    members = [day for day, n in digest_urls.items() if n > 0]
    latest = max((r["last_seen"] for r in seen.values()), default="")
    for rec in seen.values():
        v = _verified_for(rec["url"], verified)
        # Age: the page's own datePublished beats anything the digest text claimed. The digest
        # fallback is only used when the page has not been probed at all.
        if v.get("days_old") is not None:
            rec["days_old"] = float(v["days_old"])
            rec["age_source"] = "page datePublished"
        else:
            rec["days_old"] = _days_old(rec["deadline"], rec["first_seen"])
            rec["age_source"] = "digest (page not probed)"
        rec["page_live"] = bool(v.get("live")) if v else None
        rec["badge"] = v.get("badge")
        rec["domain"] = v.get("domain")
        rec["in_ai_topic_feed"] = bool(v.get("in_ai_topic_feed"))
        rec["email_redacted"] = bool(v.get("email_redacted"))
        rec["emails_on_page"] = v.get("emails_on_page") or []
        rec["published_links"] = v.get("published_links") or []
        rec["stale"] = rec["days_old"] is not None and rec["days_old"] > STALE_DAYS
        rec["automatable"] = _automatable(rec["contact"], rec)
        # A request that appears in the newest digest was re-verified live by that run; one that
        # stopped appearing has dropped off the feed, which is a stronger cold signal than age.
        rec["in_latest"] = rec["last_seen"] == latest
        if rec["page_live"] is False:
            rec["dropped_off"] = "page no longer serves the request"
        elif not rec["in_latest"] and members:
            # Absent from the newest URL-carrying digest. Note what is deliberately NOT used as
            # evidence here: Sourcee's /topics/ai/journo-requests page. Measured on 2026-09-17,
            # all 42 of its slugs have a lastmod inside a single 15.7-hour window (2026-09-16
            # 12:14Z to 2026-09-17 03:59Z) and it shares 0 of 36 slugs with the previous day's
            # capture. It is a recency window over the newest ~42 requests, so any carried
            # request is absent from it by construction. Treating that absence as a cold signal
            # flagged requests as "dropped off" for the sole reason that they were posted more
            # than a day ago.
            rec["dropped_off"] = (f"not carried by the {latest} digest "
                                  f"({digest_sizes.get(latest, '?')} items)")
        else:
            rec["dropped_off"] = ""
    return list(seen.values())


def _automatable(contact: str, rec: dict | None = None) -> str:
    """How the reply has to be sent. Page-verified facts win over the digest's guess.

    Deliberately never returns "automatable". No request page in this monitor has published a
    plain mailbox that we are free to write to unattended: Sourcee redacts the journalist's
    address and asks for a DM, and the two routes we have resolved by hand (a scheduling link
    and a site contact form) are both George's lane. Claiming otherwise is what produced the
    "email — could be automated" line that made the queue look clearable by machine.
    """
    rec = rec or {}
    if rec.get("email_redacted"):
        # The request body's address is redacted by Sourcee — verified 2026-09-19 that the redaction
        # is real, not display-only: no address survives anywhere in the payload for five sampled
        # requests. A route may still exist on the *publication's* own site (Raconteur assembles the
        # byline address from data-part1/2/3 in its own JS; Speciality Food's /contact page lists
        # named editorial addresses), but only some rows have had that resolved. Say which, because
        # claiming a resolved route on a row that has none is the same class of error as the old
        # "email — could be automated" line.
        c = (contact or "").lower()
        if "@" in c or "resolved" in c:
            return "no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)"
        return "no — body address redacted by Sourcee, no route resolved for this request (George: original platform)"
    emails = rec.get("emails_on_page") or []
    if emails:
        return f"no — email {emails[0]} published (George sends)"
    if rec.get("published_links"):
        link = rec["published_links"][0]
        if "calendly" in link or "lnkd.in" in link:
            return f"no — published booking link {link} (George)"
    c = (contact or "").lower()
    if "linkedin" in c or "dm the author" in c or "comment on" in c:
        return "no — LinkedIn DM / comment (George)"
    if "schedule" in c or "scheduling link" in c:
        return "no — scheduling link (George)"
    if "reply to the original" in c or "reddit" in c or "x/twitter" in c or "dm" in c:
        return "no — platform reply (George)"
    return "unknown — verify the route before sending"


def _load_renewal() -> dict:
    """Per-slug page-edit evidence, written by whichever run's sitemap cross-check produced it.

    The filename used to be pinned to _renewal_0919.json, so every later run loaded the 2026-09-19
    file regardless of what it had measured. Globs the newest available instead.
    """
    candidates = sorted(OUT.glob("_renewal_*.json"))
    if not candidates:
        return {}
    p = candidates[-1]
    try:
        d = json.loads(p.read_text())
        d["_source_file"] = p.name
        return d
    except json.JSONDecodeError:
        return {}


# Measured 2026-09-19 and deliberately recorded, because it removes a claim the queue used to make:
# Sourcee's sitemap <lastmod> for a journo-request is byte-identical to that page's datePublished.
# Verified on all 300 most recently indexed slugs (300/300) and on all 30 slugs of the live AI
# topic feed (30/30). So lastmod carries NO renewal information, and any wording of the form
# "never refreshed" asserts knowledge of an edit event that cannot be observed from this source.
# The cold label therefore rests on age + the poster's own stated deadline, nothing else.
RENEWAL_CAVEAT = ("Sourcee publishes no renewal signal: on the 300 most recently indexed slugs and all 30 "
                  "slugs of the live AI topic feed (checked 2026-09-19) the sitemap lastmod is "
                  "byte-identical to datePublished, so 'never refreshed' is not observable and is not "
                  "claimed here. Cold means old and unpitched, not provably abandoned.")


# A request can sit in the queue for days while a draft for it already exists: the FinOps request
# was the queue's #1 on 2026-09-17 with a finished draft in pitch-drafts-2026-09-17.md and was never
# sent, and it crossed into cold on 2026-09-19. Naming which rows are already written is the one
# thing that turns "3 live requests" into an actual send decision.
DRAFTS = {
    "fulltime-employees-shadow-ai-use-and-paying-outofpocket":
        "**Draft ready and UNSENT since 2026-09-19, re-verified and re-drafted 2026-09-23: "
        "`pitch-drafts-2026-09-23.md` §1 (154-word body).** Route: simon.chandler@raconteur.net, "
        "re-resolved off the live /contributors/simon-chandler page (HTTP 200, triple unchanged, "
        "control author checked) on 2026-09-23; the older /author/simon-chandler/ URL still 404s and "
        "must not be cited. Figures re-derived today against data/pricing_snapshots.json "
        "(`updated: 2026-09-23`): 76 tools, 31 of 40 priced tools at or under $25/month, median "
        "$16.50, and the pair range holding at 1.11x-2.53x over 19 tiers across 14 tools. "
        "Written and unsent for five consecutive runs. The only high-relevance request in the queue.",
    "speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech":
        "**Draft ready and UNSENT since 2026-09-19, re-drafted 2026-09-23: "
        "`pitch-drafts-2026-09-23.md` §2 (164-word body).** Route: holly.shackleton@artichokehq.com "
        "(re-read off specialityfoodmagazine.com/contact 2026-09-23, HTTP 200, alongside five other "
        "named staff addresses). Standing constraint is stated in the draft's first line: we are not a "
        "food retailer. 5 days old.",
    "anthropic-users-and-business-owners-customer-service-experiences":
        "**CROSSED COLD 2026-09-23 at 11 days — no longer counted as sendable.** Draft finished and "
        "unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal hliwrites.99 "
        "(re-read verbatim off the live page 2026-09-22). It was the queue's #2 and sendable on four "
        "consecutive runs. Send late or record as skipped in pitch-ledger.json; the crossing is logged "
        "in `cold_without_a_send`.",
    "finops-professionals-agentic-ai-cost-overruns":
        "**Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1.** Route: "
        "LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 and still unsent — the "
        "longest-standing high-relevance request this monitor has never answered. Send it late or "
        "drop it, do not draft it a fifth time.",
}

DRAFT_INDEX = (
    "## Drafts that exist and were never sent\n\n"
    "Read this before clearing the queue: four drafts are already written and none has been sent. "
    "A written draft is not progress — the send is.\n\n"
    "**Today's drafts are `pitch-drafts-2026-09-23.md` (§1 shadow AI, §2 Speciality Food, both "
    "paste-ready).** One of the four rows below crossed the cold line today: the Anthropic draft is "
    "not in today's file and is not sendable any more.\n\n"
    "**The pair range is `1.11x to 2.53x, median 1.25x` over 19 tiers across 14 tools, and it held "
    "today.** History, because every superseded value is still sitting in dated draft files and must "
    "not be reused: the range was first published as `1.21x to 2.53x, median 1.33x` (2026-09-18, sent "
    "to a real correspondent — wrong because the pair population was regex-dependent and undefined); "
    "corrected to `1.16x to 2.53x, median 1.25x` over 18 curated pairs (2026-09-21); then re-derived "
    "to **1.11x to 2.53x** when the replit-ai snapshot was refreshed (2026-09-22). On 2026-09-23 the "
    "19-pair set re-asserted clean against the refreshed snapshot (exit 0, no needle failures) — the "
    "first day since the assertion gate was added that the figure did NOT move. See "
    "`data/monthly_annual_pairs.json` and `scripts/extract_monthly_annual_pairs.py`, which refuses to "
    "write the file at all unless every curated pair re-asserts against the live snapshot.\n\n"
    + "\n".join(f"- {u.rsplit('/', 1)[-1][:64]} — {v}" for u, v in sorted(DRAFTS.items()))
)


def _sendable(q: dict) -> bool:
    """Is this row something a person could actually send, or just a live page?

    The queue's headline used to read "16 live" and a reader scanning it concluded there were 16
    candidates. Only 3 of those 16 had both a relevance above the tangential band and a resolved
    reply route; the remaining 13 are off-beat calls (hospital billing, podcast bookings, a founders'
    profile slot) that the queue's own draft file documents as excluded. A count nobody can act on is
    the same defect as a draft nobody sends, so the sendable number is now named separately.
    """
    if q["stale"] or q["dropped_off"]:
        return False
    if _rel_rank(q["relevance"]) >= RELEVANCE_RANK["low"]:
        return False
    route = (q.get("contact") or "").lower()
    has_route = bool(q.get("emails_on_page")) or "@" in route or "linkedin.com/in/" in route \
        or "signal" in route or bool(q.get("published_links"))
    return has_route


def render(queue: list[dict], ledger: dict) -> str:
    live = [q for q in queue if q["url"] not in ledger.get("pitched", {})]
    live = [q for q in live if q["url"] not in ledger.get("skipped", {})]
    fresh = [q for q in live if not q["stale"]]
    stale = [q for q in live if q["stale"]]

    def key(q):
        # Specified ranking: still-live-in-the-feed first, then relevance, then age. Feed
        # membership comes from the newest URL-carrying digest. Sourcee's AI topic page is
        # deliberately NOT used here: it is a recency window over the newest ~42 requests
        # (all 42 slugs dated inside one 15.7-hour window on 2026-09-17, 0 of 36 shared with
        # the previous capture), so every carried request is absent from it by construction
        # and using it as a membership test would demote the whole queue.
        #
        # 2026-09-21: all 41 tracked requests now carry last_seen == the newest digest day, so
        # `in_latest` is True for every row and the first key component no longer discriminates.
        # That is a property of carrying every request forward in each digest, not a ranking error,
        # and relevance + age still order the list correctly. Left in place because the moment a
        # digest stops carrying a row it becomes the strongest cold signal available.
        live_in_feed = q["in_latest"]
        return (0 if live_in_feed else 1,
                _rel_rank(q["relevance"]),
                q["days_old"] if q["days_old"] is not None else 999)

    fresh.sort(key=key)
    stale.sort(key=key)
    # Built AFTER the sort, not before. Building it first (as this did) froze the sendable list in
    # pre-sort order, so the section headed "pitch these" listed the 9-day medium-high row above the
    # 4-day high row — the same class of defect as the relevance-band bug, reached by mutating a
    # filtered copy before ordering the list it derives from.
    sendable = sorted([q for q in fresh if _sendable(q)], key=key)

    lines = [
        "# Pitch queue — clear this in one pass",
        "",
        f"Built {date.today().isoformat()} from {len(queue)} unique requests across the digest "
        f"history. **{len(sendable)} sendable**, {len(fresh)} live, {len(stale)} cold "
        f"(> {STALE_DAYS} days and unpitched).",
        "",
        "*\"Sendable\" is the number that matters and the one the headline used to hide: a live page "
        "is not a candidate. A row counts as sendable only when it is live, not cold, not dropped "
        "off, not already pitched, ranked above the tangential band, and has a resolved reply route "
        "(a published email, a named handle, a booking link). The other live rows are off-beat calls "
        "this queue already documents as excluded.*",
        "",
        "**Ages are read off each request page** (`datePublished`), not off the digest text — see "
        "`marketing/haro-outreach/verified-requests.json`, refreshed by "
        "`scripts/verify_journo_requests.py`. An earlier build fell back to the digest's "
        "first-seen date and showed a 190-day-old request as 8 days old.",
        "",
        f"**No renewal signal exists on this source.** {RENEWAL_CAVEAT}",
        "",
        "**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, "
        "Qwoted and Medialyst need authenticated sessions, and Sourcee redacts the requester's own "
        "address in the request body. That is why 43 flagged opportunities produced zero pitches. "
        "Reply routes are named per row — including addresses resolved off the *publication's* own "
        "site (a byline page or an editorial contact page), which is now the strongest route class "
        "in this queue.",
        "",
        DRAFT_INDEX,
        "",
    ]

    def _row(q: dict) -> list[str]:
        age = f"{q['days_old']:.0f}d old" if q["days_old"] is not None else "age unknown"
        out = [
            f"### [{q['relevance']}] {q['category'] or '(uncategorised)'}",
            f"- **URL:** {q['url']}",
            f"- **Posted:** {age} ({q['age_source']}) · badge: {q['badge'] or '—'} · "
            f"AI-topic feed: {'yes' if q['in_ai_topic_feed'] else 'no'}",
            f"- **Seen:** first {q['first_seen']}, last {q['last_seen']} ({q['appearances']}x)",
            f"- **Publication:** {q['publication'] or '—'}"
            + (f" · domain {q['domain']}" if q["domain"] else ""),
            f"- **Reply route:** {q['contact'] or '—'}  ·  _{q['automatable']}_",
        ]
        if q["emails_on_page"]:
            out.append(f"- **Email published on the page:** {', '.join(q['emails_on_page'])}")
        if q["published_links"]:
            out.append(f"- **Links published on the page:** {', '.join(q['published_links'])}")
        if q["dropped_off"]:
            out.append(f"- **⚠ Dropped off:** {q['dropped_off']} — colder than its age suggests")
        if q["angle"]:
            out.append(f"- **Angle:** {q['angle'][:400]}")
        out.append("")
        return out

    if fresh:
        # Splitting this section matters: the heading used to say "pitch these" over every live row,
        # which is where "16 live" came from. 19 of these 22 rows are off-beat calls with no route
        # and no standing; the 3 that are not are the ones worth a person's time, so they get the
        # heading that implies action and the rest get one that says what they are.
        lines += [f"## Sendable — pitch these ({len(sendable)})", "",
                  "Live, not cold, ranked above the tangential band, and with a reply route a human "
                  "can actually use. This is the whole actionable queue.", ""]
        for q in sendable:
            lines += _row(q)
        rest = [q for q in fresh if q not in sendable]
        if rest:
            lines += [f"## Live but not sendable ({len(rest)})", "",
                      "These pages resolve and the requests are unexpired, so they are recorded — but "
                      "none has both a relevance above the tangential band and a usable route. They are "
                      "listed for completeness, not as candidates: pitching any of them would mean "
                      "claiming standing we do not have (see the exclusions in the newest "
                      "`pitch-drafts-*.md`).", ""]
            for q in rest:
                lines += _row(q)
    else:
        lines += ["## Sendable — none", ""]

    if stale:
        lines += ["## Cold — only if you have a reason", "",
                  "Older than the 10-day line and never pitched. Not provably abandoned — no renewal "
                  "signal exists on this source — but every one of these has already passed an ideal "
                  "send window.", ""]
        for q in stale:
            age = f"{q['days_old']:.0f}d old" if q["days_old"] is not None else "age unknown"
            lines.append(f"- [{q['relevance']}] {age} — {q['url']}")
        lines.append("")

    dropped = [q for q in live if q["dropped_off"]]
    if dropped:
        lines += ["## Dropped off the feed", "",
                  "Still fetching, but absent from the newest digest — colder than the age says.", ""]
        for q in dropped:
            age = f"{q['days_old']:.0f}d old" if q["days_old"] is not None else "age unknown"
            lines.append(f"- [{q['relevance']}] {age} — {q['dropped_off']} — {q['url']}")
        lines.append("")

    lines += [
        "---",
        "",
        "## Clearing the queue",
        "",
        "After sending, record it so the row does not reappear:",
        "",
        "```json",
        '{"pitched": {"<url>": "2026-09-15"}, "skipped": {"<url>": "reason"}}',
        "```",
        "",
        f"Ledger: `{LEDGER.relative_to(SITE_ROOT)}`",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    queue = collect()
    ledger = _load_ledger()
    QUEUE_MD.write_text(render(queue, ledger))
    live = [q for q in queue if not q["stale"] and q["url"] not in ledger.get("pitched", {})]
    live = [q for q in live if q["url"] not in ledger.get("skipped", {})]
    sendable = [q for q in live if _sendable(q)]
    print(f"unique requests: {len(queue)}")
    print(f"live (not stale, not pitched): {len(live)}")
    print(f"SENDABLE (live + route + relevance above low): {len(sendable)}")
    print(f"of those, dropped off the newest digest: {sum(1 for q in sendable if q['dropped_off'])}")
    print(f"wrote {QUEUE_MD.relative_to(SITE_ROOT)}")
    for q in sorted(sendable, key=lambda x: (0 if x["in_latest"] else 1, _rel_rank(x["relevance"]),
                                             x["days_old"] if x["days_old"] is not None else 999)):
        age = f"{q['days_old']:.0f}d" if q["days_old"] is not None else "?"
        print(f"  SEND {age:>5} [{q['relevance']:<9}] {q['url'][:66]}")
    for q in sorted(live, key=lambda x: x["days_old"] if x["days_old"] is not None else 999):
        if q in sendable:
            continue
        age = f"{q['days_old']:.0f}d" if q["days_old"] is not None else "?"
        print(f"  (not sendable) {age:>5} [{q['relevance']:<9}] {q['url'][:58]}")


if __name__ == "__main__":
    main()
