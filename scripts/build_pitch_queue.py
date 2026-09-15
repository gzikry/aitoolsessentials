#!/usr/bin/env python3
"""Build a ranked, actionable pitch queue from the HARO/Sourcee digests.

The monitor's problem was never supply: it flagged 43 opportunities across 29 unique URLs in
12 days while nothing was ever pitched. The bottleneck is the send step, so this turns the
accumulated digests into one queue George can clear in a single pass.

Design notes:
  * Dedupe by URL, not by digest date. The same request recurs for days (the FinOps one
    appeared in six consecutive digests) and listing it six times buries the queue.
  * Rank by relevance, then by freshness. A high-relevance request that is 8 days old and
    never refreshed is colder than a medium one posted yesterday.
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

# A request older than this, never refreshed, is cold in practice even if the page is live.
STALE_DAYS = 10

RELEVANCE_RANK = {"high": 0, "medium": 1, "low-medium": 2, "medium-low": 2, "low": 3}


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
    digests = sorted(OUT.glob("digest-*.json"))
    for f in digests:
        day = f.stem.replace("digest-", "")
        try:
            d = json.loads(f.read_text())
        except json.JSONDecodeError:
            continue
        for op in d.get("opportunities") or []:
            url = (op.get("url") or "").strip()
            if not url:
                continue
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
    for rec in seen.values():
        rec["days_old"] = _days_old(rec["deadline"], rec["first_seen"])
        rec["stale"] = rec["days_old"] is not None and rec["days_old"] > STALE_DAYS
        rec["automatable"] = _automatable(rec["contact"])
    # A request that appears in the newest digest was re-verified live by that run; one that
    # stopped appearing has dropped off the feed, which is a stronger cold signal than age.
    latest = max((r["last_seen"] for r in seen.values()), default="")
    for rec in seen.values():
        rec["in_latest"] = rec["last_seen"] == latest
    return list(seen.values())


def _automatable(contact: str) -> str:
    c = (contact or "").lower()
    if "linkedin" in c or "dm the author" in c or "comment on" in c:
        return "no — LinkedIn DM / comment (George)"
    if "schedule" in c or "scheduling link" in c:
        return "no — scheduling link (George)"
    if "reply to the original" in c or "reddit" in c:
        return "no — platform reply (George)"
    if "@" in c:
        return "email — could be automated"
    return "unknown"


def render(queue: list[dict], ledger: dict) -> str:
    live = [q for q in queue if q["url"] not in ledger.get("pitched", {})]
    live = [q for q in live if q["url"] not in ledger.get("skipped", {})]
    fresh = [q for q in live if not q["stale"]]
    stale = [q for q in live if q["stale"]]

    def key(q):
        # Still in the newest digest (re-verified live) beats older; then relevance; then age.
        return (0 if q["in_latest"] else 1,
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
        "**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, "
        "Qwoted and Medialyst need authenticated sessions, and Sourcee's requests ask for a "
        "LinkedIn DM. That is why 43 flagged opportunities produced zero pitches. Reply routes "
        "are named per row.",
        "",
    ]

    if fresh:
        lines += ["## Live — pitch these", ""]
        for q in fresh:
            age = f"{q['days_old']:.0f}d old" if q["days_old"] is not None else "age unknown"
            lines += [
                f"### [{q['relevance']}] {q['category'] or '(uncategorised)'}",
                f"- **URL:** {q['url']}",
                f"- **Seen:** first {q['first_seen']}, last {q['last_seen']} "
                f"({q['appearances']}x) · **{age}**",
                f"- **Publication:** {q['publication'] or '—'}",
                f"- **Reply route:** {q['contact'] or '—'}  ·  _{q['automatable']}_",
            ]
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
    print(f"unique requests: {len(queue)}")
    print(f"live (not stale, not pitched): {len(live)}")
    print(f"wrote {QUEUE_MD.relative_to(SITE_ROOT)}")
    for q in sorted(live, key=lambda x: RELEVANCE_RANK.get(x["relevance"], 9))[:5]:
        age = f"{q['days_old']:.0f}d" if q["days_old"] is not None else "?"
        print(f"  [{q['relevance']:<9}] {age:>4}  {q['url'][:78]}")


if __name__ == "__main__":
    main()
