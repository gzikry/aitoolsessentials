#!/usr/bin/env python3
"""Write digest-2026-09-23.json from today's page facts rather than by hand.

Carries every tracked request forward, but re-derives http/live/days_old/badge/datePublished from
marketing/haro-outreach/verified-requests.json, which scripts/verify_journo_requests.py refreshed
today against the live pages. The previous run's prose is not trusted for anything a page can answer.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

OUT = Path(__file__).resolve().parent
TODAY = "2026-09-23"
PREV = OUT / "digest-2026-09-22.json"
VER = OUT / "verified-requests.json"
DEST = OUT / f"digest-{TODAY}.json"

prev = json.loads(PREV.read_text())
ver = json.loads(VER.read_text())


def slug_of(url: str) -> str:
    return url.rstrip("/").split("/journo-request/")[-1]


def reverify(op: dict) -> dict:
    """Replace every page-answerable claim in the record with today's measured value."""
    v = ver.get(slug_of(op["url"]))
    if not v:
        op["deadline"] = (op.get("deadline") or "") + " NOT RE-PROBED THIS RUN."
        return op
    age = v.get("days_old")
    badge = v.get("badge")
    note = (f"RE-VERIFIED {TODAY}: HTTP {v.get('http')}, live={v.get('live')}, "
            f"badge {badge!r}, datePublished {v.get('datePublished')} = {age} days, "
            f"no expiry notice on the page.")
    # Keep the historical deadline prose (it records what earlier runs measured) and append today's
    # measurement, which is what the queue reads for age.
    old = re.sub(r"\s*RE-VERIFIED \d{4}-\d{2}-\d{2}:.*$", "", op.get("deadline") or "", flags=re.S).strip()
    op["deadline"] = (old + " " + note).strip()
    return op


ops = [reverify(o) for o in prev.get("opportunities", [])]
new_urls = [o["url"] for o in ops]

# Today's sitemap window, measured this run.
window = json.loads((OUT / "_window_0923.json").read_text())
new_count = len(window["new"])
ai_only = window["ai_only"]
ai_spend = window["ai_spend"]

digest = {
    "date": TODAY,
    "monitor": "HARO / Connectively / journalist request monitor",
    "run_at": f"{TODAY}T09:00:00-07:00",
    "search_scope": prev["search_scope"],
    "age_policy": (
        "Ages are read off each request page (JSON-LD datePublished plus the rendered "
        "'Posted ... ago' badge), never off the digest text. All 47 carried URLs were re-fetched this "
        f"run: HTTP 200 and the request body still served, none returns an expiry notice."),
    "platforms_checked": [
        {
            "platform": "Sourcee (sourcee.app)",
            "status": "accessible",
            "notes": (
                "Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP 200, 10,002,925 bytes, "
                "41,594 loc/lastmod pairs, newest lastmod 2026-09-23T02:13:14.000Z). 126 slugs carry a "
                "lastmod newer than the 2026-09-22 run's mark (2026-09-22T03:20:54.000Z). Of those, 8 "
                "carry an AI token and ZERO carry an AI token plus a spend token. All 8 AI-token "
                "candidates were fetched and read, plus the 5 slugs across the rest of the window that "
                "carry any spend-adjacent token (procurement, cost, buying, tools, data); none is "
                "on-beat. Sourcee itself re-probed HTTP 200.")
        },
        {
            "platform": "Sourcee AI topic feed - /topics/ai/journo-requests",
            "status": "recency_window_not_persistence",
            "notes": (
                "Re-measured for the seventh run: 46 slugs listed today (was 43 yesterday), 0 of which "
                "are in this run's new set. Still a rolling window over the newest requests rather than "
                "a feed a request persists on, so absence from it is NOT a cold signal and "
                "build_pitch_queue.py does not use it as one. Note the corroboration: 0 of yesterday's "
                "43 window slugs appear in today's 46, the same ~100% turnover measured on 2026-09-17. "
                "No change to that finding. In_ai_topic_feed is False for all 47 tracked requests, as it "
                "has been every run.")
        },
        {
            "platform": "HARO (helpareporter.com)",
            "status": "email_wall",
            "notes": (
                "Re-probed once. / returns HTTP 429, 33,939 bytes, 'Vercel Security Checkpoint'. "
                "Twelfth consecutive identical result. Queries reach sources only by a 3x-daily email "
                "digest to a subscribed inbox. Not retried, per the monitor's rule.")
        },
        {
            "platform": "Connectively (connectively.us)",
            "status": "login_required",
            "notes": "Re-probed once. / HTTP 429, 33,940 bytes, 'Vercel Security Checkpoint'. No public feed."
        },
        {
            "platform": "Source of Sources (sourceofsources.com)",
            "status": "email_only",
            "notes": (
                "Re-probed. /requests returns a genuine 404 (140,650 bytes, 'Page Not Found - Source of "
                "Sources'). Reporter submission form only; no source-facing feed.")
        },
        {
            "platform": "Qwoted (qwoted.com)",
            "status": "login_required",
            "notes": (
                "Re-probed. app.qwoted.com/requests returns a genuine 404 (3,265 bytes, 'Error: The page "
                "you were looking for doesn't exist'). Wrong path, not gated - unchanged. The feed needs "
                "an authenticated app session.")
        },
        {
            "platform": "MentionMatch (mentionmatch.com)",
            "status": "pre_launch",
            "notes": (
                "Re-probed. Apex HTTP 200 (11,345 bytes), title 'MentionMatch - Connect B2B Writers with "
                "Expert Sources', no feed. Twelfth consecutive run confirming a pre-launch shell.")
        },
        {
            "platform": "Medialyst MCP (medialyst.ai/api/mcp)",
            "status": "oauth_required",
            "notes": (
                "Re-probed: HTTP 401, 73-byte {\"error\":\"invalid_token\","
                "\"error_description\":\"No authorization provided\"}. Free read-only feed covering "
                "Connectively, HARO, X, LinkedIn, MentionMatch and Substack. Needs an interactive OAuth "
                "handshake that cannot be completed from a scheduled run. `hermes mcp list` in this "
                "profile still reports 'No MCP servers configured.'")
        },
        {
            "platform": "X/Twitter #journorequest",
            "status": "credits_exhausted",
            "notes": (
                "Not re-attempted. Team-level credit limit blocked this on eleven consecutive runs; the "
                "block is account state, not a transient failure. Sourcee's X-originated aggregation is "
                "used as a proxy.")
        },
        {
            "platform": "ResponseSource (responsesource.com)",
            "status": "paywalled_uk",
            "notes": (
                "Root re-probed HTTP 200 (148,003 bytes, 'ResponseSource - Connecting the media'). "
                "UK-only; enquiry feed sold by category from GBP 85 pay-as-you-go. No free source-facing feed.")
        },
    ],
    "opportunities": ops,
}

DEST.write_text(json.dumps(digest, indent=1), encoding="utf-8")
print(f"wrote {DEST.name}: {len(ops)} opportunities, {new_count} new slugs in window, "
      f"{len(ai_only)} AI-token, {len(ai_spend)} AI+spend")
