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
import statistics
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
                # For the "longest text" fields, `>` kept the OLDER digest's value whenever two
                # digests carried equal-length text — so a row's `angle` could point at a superseded
                # draft filename even though the newest digest had already corrected it. Digests are
                # iterated oldest→newest, so `>=` lets the newest win on a tie while a genuinely
                # longer older value still wins.
                if v and (longest is False or len(v) >= len(rec[dst])):
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
            #
            # 2026-10-10 CORRECTION: the "by construction" half of that reasoning was never
            # measured and is now falsified. Re-measured today: the AI topic page listed 50 slugs
            # and only 40 of them sat inside that day's new-sitemap window, so the page is NOT a
            # pure recency window over the newest requests. The RULE above is unchanged and does
            # not depend on the retracted half: absence from that page is still not evidence that
            # a carried request is dead, which is the only thing this branch needs.
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
    # A plain published address carried in `contact_method` — the class of route this queue calls
    # its strongest (resolved off the publication's own site, not off the request page). Until
    # 2026-10-10 this fell through every branch below to "unknown — verify the route before
    # sending", because only a redacted body, an `emails_on_page` list, a booking link or a
    # LinkedIn/scheduling keyword was recognised. That is the same defect class as the 2026-10-01
    # casting-form route and the 2026-09-29 chrome leak: a field that records a real route being
    # unread, and the reason the Glenn Hansen row printed as route-less on the build that first
    # had its route.
    if "@" in c:
        return "no — email resolved off the publication's own site (George sends)"
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
#
# These entries are rewritten on every run against that run's verified-requests.json. They carried
# hand-written prose for six runs in a row, including a "TODAY IS ITS LAST LIVE DAY" claim for a row
# that had already crossed - so the ages and the crossing dates here are now read from the cache, not
# typed out. `scripts/build_pitch_queue.py` refuses to print an age it has not just measured.
_VERIFIED_CACHE = _load_verified()


def _age_of(slug: str) -> int | None:
    return (_VERIFIED_CACHE.get(slug) or {}).get("days_old")


def _sent_word(n: int | None) -> str:
    return f"{n}d" if n is not None else "age unmeasured"


def _newest_drafts() -> str:
    """The newest `pitch-drafts-*.md`, derived rather than typed.

    This block carried a hardcoded filename for six consecutive runs and drifted a day behind the
    drafts that actually existed, so a reader following the queue opened the wrong file. Deriving it
    means the pointer cannot be older than the newest draft on disk.
    """
    files = sorted(OUT.glob("pitch-drafts-*.md"))
    return files[-1].name if files else "pitch-drafts-<none>.md"


def _carried_runs(slug: str) -> int:
    """How many draft files have carried this request — measured, not asserted.

    The old prose said "unsent through twelve consecutive runs" as typed text; the number moved
    every day and was maintained by hand. Counting the files that actually name the slug makes the
    claim checkable.
    """
    return sum(1 for f in OUT.glob("pitch-drafts-*.md") if slug in f.read_text(errors="ignore"))


def _live_row_count() -> int:
    """Rows the queue itself counts as live, measured at build time.

    `DRAFT_INDEX` used to assert "Today the live set is 21 rows" as typed text. That number moved
    every day and, on the 2026-10-02 run, was already three days stale inside a file dated today —
    the same defect class as the hardcoded draft filename and the hardcoded crossing date fixed on
    earlier runs. Derived from the same verified-requests cache the ages come from, so it cannot
    drift from the headline.
    """
    return sum(1 for r in _VERIFIED_CACHE.values()
               if r.get("days_old") is not None and r["days_old"] <= STALE_DAYS)


def _headline_figures() -> str:
    """The figures a carried draft may stand behind today, re-derived from our own data files.

    The two DRAFTS entries below used to carry hand-typed copies of these ("40 publishing a monthly
    price, ... median $16.50", "updated: 2026-09-30"). On 2026-10-02 the snapshot refresh moved them
    (to 42 / 33 / $17.50) while the typed prose stayed put — a stale figure inside a file rebuilt
    today, which is the same defect class as the hardcoded live-row count. Derived instead, and
    falls back to a pointer rather than inventing a number if the data is unreadable.
    """
    try:
        snaps = json.loads((SITE_ROOT / "data" / "pricing_snapshots.json").read_text())
        tools = json.loads((SITE_ROOT / "data" / "tools.json").read_text())
        pairs = json.loads((SITE_ROOT / "data" / "monthly_annual_pairs.json").read_text())
    except (OSError, json.JSONDecodeError):
        return "(figures not re-derived this run — see the newest `pitch-drafts-*.md`)"
    month = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
    paid = {}
    for k, v in (snaps.get("snapshots") or {}).items():
        vals = [float(x) for x in month.findall(v.get("digest") or "") if float(x) > 0]
        if vals:
            paid[k] = min(vals)
    if not paid:
        return "(figures not re-derived this run — see the newest `pitch-drafts-*.md`)"
    med = statistics.median(paid.values())
    return (f"{len(tools)} tools, {len(paid)} publishing a monthly price, "
            f"{sum(1 for x in paid.values() if x <= 25)} of those at or under $25/month, "
            f"median ${med:.2f} (snapshots `updated: {snaps.get('updated')}`); and the pair range "
            f"{pairs.get('range_low')}x-{pairs.get('range_high')}x, median {pairs.get('median')}x "
            f"over {pairs.get('n')} tiers (built {pairs.get('built')})")


def _latest_route_checks() -> dict:
    """The newest marketing/haro-outreach/route-checks-*.json, read for route byte counts and titles.

    The DRAFTS prose used to carry hand-typed route evidence from the 2026-10-06 run ("HTTP 200,
    154,819 bytes", "verified HTTP 200 on 2026-10-06") inside a file rebuilt on a later day — the
    same defect class as the hardcoded draft filename and figures. The file is written by the run's
    `_routes_<MMDD>.py` probe and named by date, so the pointer cannot be older than the newest
    probe on disk. Returns {} rather than inventing a value when no probe exists.
    """
    files = sorted(OUT.glob("route-checks-*.json"))
    if not files:
        return {}
    try:
        return json.loads(files[-1].read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def _route_evidence(key: str, label: str) -> str:
    """One route's verified evidence, phrased for the DRAFTS prose, from the newest probe file."""
    checks = _latest_route_checks()
    r = (checks.get("routes") or {}).get(key) or {}
    if not r:
        return f"{label} (no route probe on disk this run — verify before citing)"
    when = checks.get("checked", "?")
    bits = f"HTTP {r.get('http')}, {r.get('bytes'):,} bytes" if isinstance(r.get("bytes"), int) \
        else f"HTTP {r.get('http')}"
    out = f"{label} — route-checks probe {when}: {bits}"
    if r.get("triple"):
        out += f", data-part triple {r['triple']}"
    if r.get("title"):
        out += f", title '{r['title']}'"
    return out


def _route_checked_date() -> str:
    return (_latest_route_checks().get("checked") or "?")


DRAFTS = {
    "employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks":
        f"**SENDABLE — draft ready and UNSENT — `{_newest_drafts()}` §2. Now "
        f"{_sent_word(_age_of('employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks'))} old.** "
        "Route: LinkedIn DM to linkedin.com/in/christopher-mims-club/ ("
        f"{_route_evidence('linkedin.com/in/christopher-mims-club/', 'LinkedIn byline page')}; "
        "the request's own body says '(DMs open)'; muckrack.com/christopher-mims 403 and "
        "wsj.com/news/author/christopher-mims 401 are dead ends, not routes). One of two rows in "
        "this queue that are both above the tangential band and route-resolved — the other is the "
        "Glenn Hansen seats-and-tokens request, which is newer and higher-relevance. George's lane.",
    "fulltime-employees-shadow-ai-use-and-paying-outofpocket":
        f"**Draft ready and UNSENT — `{_newest_drafts()}` §3. Now {_sent_word(_age_of('fulltime-employees-shadow-ai-use-and-paying-outofpocket'))} "
        f"old, and it crossed the 10-day line on 2026-09-28 unpitched. Carried in "
        f"{_carried_runs('fulltime-employees-shadow-ai-use-and-paying-outofpocket')} draft files.** Route: simon.chandler@raconteur.net, "
        f"re-resolved off the live {_route_evidence('raconteur.net/contributors/simon-chandler', '/contributors/simon-chandler page')} "
        f"(control {_route_evidence('raconteur.net/contributors/tom-dennis', '/contributors/tom-dennis')}); the older "
        "/author/simon-chandler/ URL still 404s and must not be cited. Figures re-derived at build "
        f"time ({_headline_figures()}). It is "
        "the only high-relevance request this monitor has ever produced with a resolved route; the "
        "page is still HTTP 200 and the address still resolves, so a late send is still possible — "
        "what was lost is the ideal window, not the pitch.",
    "speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech":
        f"**Draft ready and UNSENT — `{_newest_drafts()}` §4. Now {_sent_word(_age_of('speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech'))} "
        f"old, crossed the 10-day line on 2026-09-28 unpitched. Carried in "
        f"{_carried_runs('speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech')} draft files.** Route: holly.shackleton@artichokehq.com "
        f"({_route_evidence('specialityfoodmagazine.com/contact', 're-read off specialityfoodmagazine.com/contact')}, "
        "alongside five other named staff addresses). Standing constraint is stated in the "
        "draft's first line: we are not a food retailer. Its October issue window has closed, so treat "
        "this as a send-or-skip call and record the outcome in `pitch-ledger.json` rather than "
        f"carrying it a {_carried_runs('speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech') + 1}th day.",
    "anthropic-users-and-business-owners-customer-service-experiences":
        f"**Crossed cold 2026-09-23; now {_sent_word(_age_of('anthropic-users-and-business-owners-customer-service-experiences'))} old — no longer counted as sendable.** "
        "Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal "
        "hliwrites.99 (re-read verbatim off the live page 2026-09-30). Send late or record as skipped "
        "in `pitch-ledger.json`; the crossing is logged in `cold_without_a_send`.",
    "finops-professionals-agentic-ai-cost-overruns":
        f"**Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1. Now {_sent_word(_age_of('finops-professionals-agentic-ai-cost-overruns'))} old.** "
        "Route: LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 and still unsent — "
        "the longest-standing high-relevance request this monitor has never answered. Send it late or "
        "drop it, do not draft it a fifth time.",
    # The find of the 2026-10-08 run and the best-matching request this monitor has ever held: a
    # reporter asking directly for enterprise AI seat and token costs, which our dated price set
    # answers. It was out of the sendable list for two runs ONLY for want of a route; the route was
    # resolved on 2026-10-10 off the author's own publication, and the row is now sendable. Named
    # here as well because it is the row whose route resolution matters most.
    "google-and-claude-enterprise-users-seats-and-token-costs":
        f"**SENDABLE — THE FIRST CORE-BEAT AI+SPEND ROW THIS MONITOR CAN ACT ON — draft at "
        f"`{_newest_drafts()}` §1. Now {_sent_word(_age_of('google-and-claude-enterprise-users-seats-and-token-costs'))} "
        "old, relevance 'high'.** This is the only core-beat AI+spend request the monitor has produced "
        "in fifteen runs — the first it ever produced, arriving on the 2026-10-08 run after fourteen "
        "without one — and the best-matching request this queue has ever held: the reporter (Glenn "
        "Hansen, editor of OPE+) asks directly for 'enterprise-level costs for AI seats and tokens' "
        "from Google or Claude users, and our dated set answers it (Claude Team $20/$100 per "
        "seat/month checked 2026-09-18; Gemini in Workspace $8.40/$7 to $26.40/$22 per user/month, "
        "2026-09-18; GitHub Copilot Business $19 / Enterprise $39 per user/month with credits at "
        "$0.01, 2026-10-01; Microsoft 365 Copilot Business $18 promotional annual vs $21 list, "
        "2026-10-01). THE ROUTE WAS RESOLVED ON THE 2026-10-10 RUN, off his own publication rather "
        "than the request page: the page's author field names him and the body states his beat, and "
        "OPE+ publishes 'Glenn Hansen, Editor — ghansen@epgacceleration.com' at "
        "ope-plus.com/2024/02/13/announcing-ope/19236 "
        f"({_route_evidence('ope-plus.com/2024/02/13/announcing-ope/19236', 'OPE+ editor announcement page')}), "
        "with the same editorial domain on ope-plus.com/contact-us "
        f"({_route_evidence('ope-plus.com/contact-us', 'contact page')}); epgacceleration.com MX = "
        "Microsoft 365. Two runs were spent calling this row unsendable because only the request page "
        "was read. George's lane to send.",
}

def _pairs_now() -> tuple[str, str, str, str]:
    """(range_low, range_high, median, n) read from data/monthly_annual_pairs.json, never typed."""
    try:
        d = json.loads((SITE_ROOT / "data" / "monthly_annual_pairs.json").read_text())
    except (OSError, json.JSONDecodeError):
        return ("?", "?", "?", "?")
    return (d.get("range_low"), d.get("range_high"), d.get("median"), d.get("n"))


def _figures_now() -> tuple[str, str, str, str]:
    """(n_tools, n_monthly_priced, n_at_or_under_25, median) re-derived the same way as
    _headline_figures(). Returns '?'s rather than inventing a number if the data is unreadable."""
    try:
        snaps = json.loads((SITE_ROOT / "data" / "pricing_snapshots.json").read_text())
        tools = json.loads((SITE_ROOT / "data" / "tools.json").read_text())
    except (OSError, json.JSONDecodeError):
        return ("?", "?", "?", "?")
    month = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
    paid = {}
    for k, v in (snaps.get("snapshots") or {}).items():
        vals = [float(x) for x in month.findall(v.get("digest") or "") if float(x) > 0]
        if vals:
            paid[k] = min(vals)
    if not paid:
        return (str(len(tools)), "?", "?", "?")
    return (str(len(tools)), str(len(paid)),
            str(sum(1 for x in paid.values() if x <= 25)),
            f"{statistics.median(paid.values()):.2f}")


def _unsent_draft_files() -> int:
    """How many draft files exist on disk, measured — not asserted.

    The prose said "four drafts are already written and none has been sent" as typed text. On
    2026-10-06 there were 17 draft files on disk and the count moved every day, so it was wrong
    by an order of magnitude inside a file rebuilt that morning. Same defect class as the
    hardcoded draft filename, live-row count and figures fixed on earlier runs.
    """
    return len(list(OUT.glob("pitch-drafts-*.md")))


def _draft_index(live_count: int, sendable_count: int) -> str:
    """The carried-drafts block, with every date-sensitive claim re-derived at build time.

    Four consecutive runs have now been bitten by typed prose inside a file rebuilt today: a
    hardcoded draft filename (fixed 2026-09-29), a hardcoded crossing date and live-row count
    (fixed 2026-09-30/2026-10-01), a hardcoded "the figures moved today" block plus byte-count
    route notes (2026-10-05), and — this run — a hardcoded "ZERO SENDABLE" paragraph that flatly
    contradicted the 1 sendable row the same build had just measured. The block is now a function
    of the run's own numbers: the sendable and live counts come from the queue render, the draft
    file count and section pointers from the files on disk, and the figures from our data files.
    Anything that cannot be re-derived prints '?' rather than a number nobody measured.
    """
    n_tools, n_paid, n_25, med = _figures_now()
    lo, hi, mid, n = _pairs_now()
    snap_updated = "?"
    try:
        snap_updated = json.loads(
            (SITE_ROOT / "data" / "pricing_snapshots.json").read_text()).get("updated", "?")
    except (OSError, json.JSONDecodeError):
        pass
    if sendable_count:
        # A non-zero sendable count is the state this monitor spent eleven runs failing to reach.
        # It must never be reported through prose that says otherwise, so the two states carry
        # different text rather than one paragraph with a number spliced in.
        state = (
            f"**THE QUEUE IS AT {sendable_count} SENDABLE.** Every build before the 2026-10-06 run "
            f"reported 0, and twice that 0 was a genuine measurement after a defect had been fixed "
            f"(the 2026-09-29 chrome leak into `published_links`, the 2026-10-01 Google Form read as "
            f"a link route). A row is declared sendable on two facts evidenced separately rather "
            f"than trusted from a digest field: a relevance above the tangential band, and a reply "
            f"route verified by fetching a page today. Both are named in the row. Holding more than "
            f"one at a time is itself new — the 2026-10-10 build is the first to do it, and it "
            f"happened because a route was resolved rather than because a find arrived. The live "
            f"unpitched set is {live_count} rows."
        )
    else:
        state = (
            f"**THE QUEUE IS AT ZERO SENDABLE, AND TODAY THAT IS THE TRUE NUMBER RATHER THAN A "
            f"CODE ARTEFACT.** Repeated builds have each had to be corrected for the same defect "
            f"class — a field that records something adjacent to a reply route being read as one. "
            f"On 2026-09-29 the refresh script had dropped Sourcee's two own social links from its "
            f"chrome filter, so a page's own chrome landed in one row's `published_links`. On "
            f"2026-10-01 the first build read the employees-conflicted-about-AI-use row as "
            f"sendable because its body embeds a docs.google.com casting form, which `_sendable()` "
            f"accepted as a link route. Both are fixed: a `published_links` entry now counts as a "
            f"route only when it is a booking/contact link. Today the live unpitched set is "
            f"{live_count} rows (measured at build time from the merged digests, not typed), and "
            f"none has both a relevance above the tangential band and a usable route."
        )
    return (
        "## Drafts that exist and were never sent\n\n"
        f"Read this before clearing the queue: {_unsent_draft_files()} draft files exist on disk "
        "and not one of the pitches in them has been sent. A written draft is not progress — the "
        "send is.\n\n"
        + state + "\n\n"
        f"**Today's draft file is `{_newest_drafts()}` (derived from disk, not typed).** The "
        f"headline figures are re-derived every run: {n_paid} of {n_tools} tools publish a monthly "
        f"price, {n_25} of those at or under $25/month, median ${med} (snapshots `updated: "
        f"{snap_updated}`). Superseded sets still sitting in older dated drafts "
        "(40/31/$16.50 and earlier) must not be reused.\n\n"
        f"**The pair range is `{lo}x to {hi}x, median {mid}x` over {n} tiers, and it held today.** "
        "History, because every superseded value is still sitting in dated draft files and must not "
        "be reused: the range was first published as `1.21x to 2.53x, median 1.33x` (2026-09-18, sent "
        "to a real correspondent — wrong because the pair population was regex-dependent and "
        "undefined); corrected to `1.16x to 2.53x, median 1.25x` over 18 curated pairs (2026-09-21); "
        "then re-derived to `1.11x to 2.53x` when the replit-ai snapshot was refreshed (2026-09-22). "
        "See `data/monthly_annual_pairs.json` and `scripts/extract_monthly_annual_pairs.py`, which "
        "refuses to write the file at all unless every curated pair re-asserts against the live "
        "snapshot.\n\n"
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
    # `published_links` is the list of non-chrome URLs found anywhere in the page payload, and a
    # request body routinely embeds ones that are NOT a reply route for us: a Google Form casting
    # call, a bit.ly to the poster's own newsletter, a t.co to the article being written. On
    # 2026-10-01 the employees-conflicted-about-AI-use row was counted sendable for exactly that
    # reason — its only "route" was a docs.google.com casting form — which is the same defect class
    # as the 2026-09-29 chrome-filter bug, reached through a different field. A link now counts as a
    # route only when it is a booking/contact route of the kind _automatable() already recognises.
    booking = [u for u in (q.get("published_links") or [])
               if any(k in u.lower() for k in ("calendly", "lnkd.in", "hubspot", "/contact", "mailto:"))]
    has_route = bool(q.get("emails_on_page")) or "@" in route or "linkedin.com/in/" in route \
        or "signal" in route or bool(booking)
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
        # 2026-10-10 CORRECTION: the overlap was measured for the first time today and is 40 of
        # 50, not 50 of 50 — the page is not a pure recency window over the newest requests, so
        # "by construction" is retired. The decision above stands on its own argument: no carried
        # row is on that page either way, so it cannot be used as a membership test.
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
        _draft_index(len(fresh), len(sendable)),
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
        if not sendable:
            # A zero here is the same class of defect as a draft nobody sends, so it is stated
            # rather than left as an empty section a reader can skim past.
            lines += [
                "**There is nothing to send from this queue today.** Every row that had both a "
                "relevance above the tangential band and a resolved route has now crossed the "
                f"{STALE_DAYS}-day line unpitched; the live rows below are off-beat calls with no "
                "usable route. The rows that carried a finished draft are named in the section above "
                "as crossed-but-still-sendable — a late send is the only action left on them.", ""]
        if sendable:
            soon = [q for q in sendable if q["days_old"] is not None and q["days_old"] >= STALE_DAYS - 2]
            if soon:
                lines += [
                    f"**{len(soon)} of these cross the {STALE_DAYS}-day cold line within two days. "
                    f"Past it, they leave this section and nothing brings them back:**", ""]
                for q in soon:
                    left = STALE_DAYS - int(q["days_old"])
                    lines.append(f"- {q['url']} — {int(q['days_old'])}d old, "
                                 f"{'crosses the line TOMORROW' if left == 1 else f'{left} days left'}")
                lines += [""]
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
