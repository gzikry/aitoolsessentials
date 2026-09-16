#!/usr/bin/env python3
"""Verify journo-request URLs against the pages themselves, and cache the facts.

Why this exists: build_pitch_queue.py derived a request's age from the digest's `deadline`
text. When that text carried no date it fell back to the digest's first-seen date, so a
request posted 2026-03-10 that a digest described as "Open (posted >1 month ago)" was shown
in the queue as 8 days old. Three rows were overstated by 100-182 days, which pushed two
genuinely dead requests to the top of the "live — pitch these" list and buried the fresh ones.

This script reads the truth off the page: the `datePublished` field in the RSC payload, the
rendered "Posted ... ago" badge, membership in the /topics/ai/journo-requests feed, the
publishing domain, whether the contact email is platform-redacted, and any published
scheduling/DM link. Results accumulate in verified-requests.json keyed by URL, so each run
only pays for the URLs it has not checked today.

Usage:
    python3 scripts/verify_journo_requests.py                # verify everything in the queue
    python3 scripts/verify_journo_requests.py <url|slug> ...  # verify specific requests
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
OUT = SITE_ROOT / "marketing" / "haro-outreach"
CACHE = OUT / "verified-requests.json"
FEED_CACHE = OUT / "ai-topic-feed.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
FEED_URL = "https://www.sourcee.app/topics/ai/journo-requests"

# Sourcee's own chrome appears on every page; none of it is a reply route.
CHROME = ("sourcee.app", "vercel", "sentry", "nextjs.org", "schema.org", "w3.org", "gstatic",
          "google.com/s2", "supabase.co", "redditstatic", "preview.redd.it",
          "linkedin.com/in/andrewsmith313", "x.com/andy_cb_smith")


def curl(url: str, timeout: int = 30) -> tuple[str, str]:
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA,
                        "-w", "\n__HTTP__%{http_code}__", url], capture_output=True, text=True)
    raw = r.stdout
    m = re.search(r"__HTTP__(\d+)__\s*$", raw)
    code = m.group(1) if m else "000"
    return code, (raw[:raw.rfind("__HTTP__")] if m else raw)


def _field(raw: str, key: str) -> str | None:
    m = (re.search(r'\\"' + key + r'\\":\\"((?:[^"\\]|\\.)*?)\\"', raw)
         or re.search(r'"' + key + r'":"((?:[^"\\]|\\.)*?)"', raw))
    if not m:
        return None
    return (m.group(1).replace("\\n", " ").replace("\\u0026", "&").replace("\\/", "/").strip())


def visible(raw: str) -> str:
    """The rendered request body, with Sourcee's chrome stripped off both ends."""
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", body)
    txt = re.sub(r"\s+", " ", txt).strip()
    m = re.search(r"Start free trial (.*?)Brought to you by Sourcee", txt, re.S)
    return (m.group(1).strip() if m else "")


def fetch_ai_feed(refresh: bool = False) -> set[str]:
    """Slugs currently listed on Sourcee's AI topic page — the live-feed membership set."""
    if not refresh and FEED_CACHE.exists():
        try:
            d = json.loads(FEED_CACHE.read_text())
            if d.get("captured") == date.today().isoformat():
                return set(d.get("slugs") or [])
        except json.JSONDecodeError:
            pass
    code, raw = curl(FEED_URL, 40)
    slugs: list[str] = []
    for s in re.findall(r"/journo-request/([a-z0-9\-]{5,160})", raw):
        if s not in slugs:
            slugs.append(s)
    FEED_CACHE.write_text(json.dumps({"captured": date.today().isoformat(), "http": code,
                                      "count": len(slugs), "slugs": slugs}, indent=1))
    return set(slugs)


def probe(url: str, feed: set[str]) -> dict:
    code, raw = curl(url)
    core = visible(raw)
    dp = _field(raw, "datePublished")
    age = None
    if dp:
        try:
            age = (datetime.now(timezone.utc) - datetime.fromisoformat(dp.replace("Z", "+00:00"))).days
        except ValueError:
            age = None
    badge = re.search(r"(Posted (?:in last 7 days|today|\d+ (?:days?|hours?) ago))", core)
    slug = url.rstrip("/").split("/journo-request/")[-1]
    links = [u for u in sorted(set(re.findall(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]{8,160}", raw)))
             if not any(c in u for c in CHROME)]
    emails = sorted(set(e for e in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", core)
                        if "sourcee" not in e.lower()))
    return {
        "url": url, "slug": slug, "http": code,
        "live": code == "200" and bool(core),
        "headline": _field(raw, "headline"),
        "datePublished": dp, "days_old": age,
        "badge": badge.group(1) if badge else None,
        "domain": _field(raw, "domain"),
        "in_ai_topic_feed": slug in feed,
        "email_redacted": bool(re.search(r"email redacted", core, re.I)),
        "emails_on_page": emails,
        "published_links": links[:6],
        "reply_hints": sorted({h for h in ("DM me", "DM or email", "reply to this thread", "Comment",
                                           "schedule time", "email me", "shoot me a DM", "Signal")
                               if h.lower() in core.lower()}),
        "checked": date.today().isoformat(),
    }


def main() -> None:
    cache: dict[str, dict] = {}
    if CACHE.exists():
        try:
            cache = json.loads(CACHE.read_text())
        except json.JSONDecodeError:
            cache = {}

    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if args:
        urls = [a if a.startswith("http") else f"https://www.sourcee.app/journo-request/{a}" for a in args]
    else:
        urls = set()
        for f in (OUT / "pitch-queue.md", *(OUT.glob("digest-*.json")), OUT / "pitch-ledger.json"):
            if not f.exists():
                continue
            for m in re.findall(r"https?://(?:www\.)?sourcee\.app/journo-request/[a-z0-9\-]+", f.read_text()):
                urls.add(m)
        urls = sorted(urls)

    print(f"verifying {len(urls)} URL(s)")
    feed = fetch_ai_feed(refresh="--refresh-feed" in sys.argv)
    print(f"AI topic feed: {len(feed)} slugs")

    for url in urls:
        rec = probe(url, feed)
        cache[rec["slug"] or url] = rec
        print(f"{'LIVE' if rec['live'] else 'GONE':<4} {rec['http']} "
              f"{str(rec['days_old']):>5}d feed={'Y' if rec['in_ai_topic_feed'] else 'n'} "
              f"{str(rec['badge']):<22} {str(rec['headline'])[:52]}", flush=True)
        time.sleep(1)

    CACHE.write_text(json.dumps(cache, indent=1))
    fresh = [r for r in cache.values()
             if r.get("live") and (r.get("days_old") is not None and r["days_old"] <= 10)]
    print(f"\ncached {len(cache)} records in {CACHE.relative_to(SITE_ROOT)}")
    print(f"live and <=10 days old: {len(fresh)}")
    for r in sorted(fresh, key=lambda x: x["days_old"]):
        print(f"  {r['days_old']:>3}d feed={'Y' if r['in_ai_topic_feed'] else 'n'} {r['headline']}")


if __name__ == "__main__":
    main()
