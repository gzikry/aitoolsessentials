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

RELEVANCE_RANK = {"high": 0, "medium": 1, "low-medium": 2, "medium-low": 2, "low": 3}


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
    r = (rel or "").strip().lower()
    r = r.split("(")[0].split("—")[0].split("-")[0 and 0 or 0] if False else r.split("(")[0]
    r = r.strip().rstrip("-").strip()
    return r or "unknown"


def collect() -> list[dict]:
    """Merge every digest into one record per URL, keeping the richest fields."""
    seen: dict[str, dict] = {}
    verified = _load_verified()
    digest_sizes: dict[str, int] = {}
    digests = sorted(OUT.glob("digest-*.json"))
    for f in digests:
        day = f.stem.replace("digest-", "")
        try:
            d = json.loads(f.read_text())
        except json.JSONDecodeError:
            continue
        digest_sizes[day] = len(d.get("opportunities") or [])
        for op in d.get("opportunities") or []:
            url = (op.get("url") or "").strip()
            if not url:
                continue
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
            if RELEVANCE_RANK.get(rel, 9) < RELEVANCE_RANK.get(rec["relevance"], 9):
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
        elif not rec["in_latest"] and not rec["in_ai_topic_feed"]:
            # Absent from both the newest digest and Sourcee's live AI topic page. Absence from
            # a single thin digest is not evidence on its own — the 2026-09-15 digest carried
            # only two opportunities — so this needs both signals to fire.
            rec["dropped_off"] = (f"absent from both the {latest} digest "
                                  f"({digest_sizes.get(latest, '?')} items) and the AI topic page")
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
        return "no — contact redacted on Sourcee (George: original platform)"
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


def render(queue: list[dict], ledger: dict) -> str:
    live = [q for q in queue if q["url"] not in ledger.get("pitched", {})]
    live = [q for q in live if q["url"] not in ledger.get("skipped", {})]
    fresh = [q for q in live if not q["stale"]]
    stale = [q for q in live if q["stale"]]

    def key(q):
        # Specified ranking: still-live-in-the-feed first, then relevance, then age. Feed
        # membership comes from two independent checks — appearing in the newest digest, and
        # appearing on Sourcee's own /topics/ai/journo-requests page — so a request that the
        # digest stopped carrying but the topic page still lists is not wrongly demoted.
        live_in_feed = q["in_latest"] or q["in_ai_topic_feed"]
        return (0 if live_in_feed else 1,
                RELEVANCE_RANK.get(q["relevance"], 9),
                q["days_old"] if q["days_old"] is not None else 999)

    fresh.sort(key=key)
    stale.sort(key=key)

    lines = [
        "# Pitch queue — clear this in one pass",
        "",
        f"Built {date.today().isoformat()} from {len(queue)} unique requests across the digest "
        f"history. {len(fresh)} live, {len(stale)} cold (> {STALE_DAYS} days, never refreshed).",
        "",
        "**Ages are read off each request page** (`datePublished`), not off the digest text — see "
        "`marketing/haro-outreach/verified-requests.json`, refreshed by "
        "`scripts/verify_journo_requests.py`. An earlier build fell back to the digest's "
        "first-seen date and showed a 190-day-old request as 8 days old.",
        "",
        "**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, "
        "Qwoted and Medialyst need authenticated sessions, and Sourcee's requests ask for a "
        "LinkedIn DM. That is why 43 flagged opportunities produced zero pitches. Reply routes "
        "are named per row, including any email the request page itself publishes.",
        "",
    ]

    if fresh:
        lines += ["## Live — pitch these", ""]
        for q in fresh:
            age = f"{q['days_old']:.0f}d old" if q["days_old"] is not None else "age unknown"
            lines += [
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
                lines.append(f"- **Email published on the page:** {', '.join(q['emails_on_page'])}")
            if q["published_links"]:
                lines.append(f"- **Links published on the page:** {', '.join(q['published_links'])}")
            if q["dropped_off"]:
                lines.append(f"- **⚠ Dropped off:** {q['dropped_off']} — colder than its age suggests")
            if q["angle"]:
                lines.append(f"- **Angle:** {q['angle'][:400]}")
            lines.append("")
    else:
        lines += ["## Live — none", ""]

    if stale:
        lines += ["## Cold — only if you have a reason", ""]
        for q in stale:
            age = f"{q['days_old']:.0f}d old" if q["days_old"] is not None else "age unknown"
            lines.append(f"- [{q['relevance']}] {age}, never refreshed — {q['url']}")
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
    print(f"unique requests: {len(queue)}")
    print(f"live (not stale, not pitched): {len(live)}")
    print(f"of those, dropped off the newest digest: {sum(1 for q in live if q['dropped_off'])}")
    print(f"wrote {QUEUE_MD.relative_to(SITE_ROOT)}")
    for q in sorted(live, key=lambda x: x["days_old"] if x["days_old"] is not None else 999)[:5]:
        age = f"{q['days_old']:.0f}d" if q["days_old"] is not None else "?"
        print(f"  {age:>5} [{q['relevance']:<9}] {q['url'][:72]}")


if __name__ == "__main__":
    main()
