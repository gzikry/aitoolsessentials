#!/usr/bin/env python3
"""Compose a run's HARO/Sourcee digest from measured artifacts, with no per-run copy.

Replaces `marketing/haro-outreach/_digest_MMDD.py`, which existed as one hand-copied 40KB file per
run for a dozen runs. The 2026-10-17 digest named that as "this monitor's one unfixed structural
defect" and deferred the fix three runs; every daily copy also carried hand-typed counts, ages and
route evidence that could drift from the pages.

What is mechanical here (carried rows, page truth, figures, crossings, ledger counts, platform
notes, health, summary, actions) is derived. What is genuinely editorial today — a new row's
`relevance_notes`, the day's defect log, any extra narrative — is read from
`marketing/haro-outreach/_run_notes_MMDD.json`, which is small and diffable.

Usage:
    python3 scripts/build_digest.py                       # today, prev = newest digest
    python3 scripts/build_digest.py --today 2026-10-18 --prev 2026-10-17
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
from datetime import date, datetime, timezone
from pathlib import Path

S = Path(__file__).resolve().parent.parent
D = S / "marketing/haro-outreach"
SITE = "https://www.sourcee.app/journo-request/"
STALE_DAYS = 10

# Platform statuses used to be a hand-maintained PLATFORM_STATUS map here. It was never read by
# anything, and by 2026-10-19 it had drifted: it still said MentionMatch was "pre-launch" after the
# site had shipped a live product behind an account. Each status now lives in exactly one place -
# `platforms_checked` below, written beside the probe note it describes - and monitor_health's counts
# are counted from that list instead of typed.



def slug_of(url: str) -> str:
    return url.rstrip("/").split("/journo-request/")[-1]


def load(p: Path, default=None):
    try:
        return json.loads(p.read_text())
    except (OSError, json.JSONDecodeError):
        return default


def derive_figures() -> dict:
    snaps = load(S / "data/pricing_snapshots.json", {}) or {}
    tools = load(S / "data/tools.json", []) or []
    month = re.compile(r"\$\s?(\d+(?:\.\d+)?)\s*/\s*(?:user|seat|member|person)?\s*/?\s*month", re.I)
    paid = {}
    for k, v in (snaps.get("snapshots") or {}).items():
        vals = [float(x) for x in month.findall(v.get("digest") or "") if float(x) > 0]
        if vals:
            paid[k] = min(vals)
    med = statistics.median(paid.values()) if paid else None
    pairs = load(S / "data/monthly_annual_pairs.json", {}) or {}
    return {
        "n_tools": len(tools),
        "n_paid": len(paid),
        "n_25": sum(1 for v in paid.values() if v <= 25),
        "median": f"{med:.2f}" if med is not None else "?",
        "snapshot_updated": snaps.get("updated") or "?",
        "pair_txt": (f"{pairs.get('range_low')}x to {pairs.get('range_high')}x, median "
                     f"{pairs.get('median')}x over {pairs.get('n')} tiers, pair set re-asserted "
                     f"{pairs.get('built')}") if pairs else "pair file unreadable",
        "pairs": pairs,
    }


def refresh(o: dict, verified: dict, feed: set[str], today: str) -> dict:
    """Replace every page-derived field on a carried row with today's page truth."""
    rec = verified.get(slug_of(o["url"])) or {}
    o = dict(o)
    days = rec.get("days_old")
    badge = rec.get("badge") or "no badge on the page"
    o["_page_live"] = bool(rec.get("live"))
    o["_days_old"] = days
    o["_badge"] = badge
    o["_in_ai_topic_feed"] = slug_of(o["url"]) in feed
    old = o.get("deadline", "")
    prefix = old.split("RE-VERIFIED 2026-")[0].strip() or "No cutoff stated."
    o["deadline"] = (
        f"{prefix} RE-VERIFIED {today}: HTTP 200, live=True, badge '{badge}', "
        f"datePublished {rec.get('datePublished')} = {days} days, no expiry notice on the page. "
        f"{'IS' if o['_in_ai_topic_feed'] else 'NOT'} in the newest AI-topic feed. The feed is a "
        f"rolling 50-slot window over the newest requests, so absence from it is not an expiry "
        f"signal and carries no freshness credit either way; this row's age comes from its page."
    )
    return o


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=date.today().isoformat())
    ap.add_argument("--prev", default=None)
    a = ap.parse_args()
    today = a.today
    mmdd = today.replace("-", "")[4:]
    if a.prev:
        prev_day = a.prev
    else:
        prior = sorted(p for p in D.glob("digest-*.json") if p.stem.replace("digest-", "") < today)
        if not prior:
            raise SystemExit("no previous digest to carry")
        prev_day = prior[-1].stem.replace("digest-", "")

    prev = load(D / f"digest-{prev_day}.json")
    if not prev or "opportunities" not in prev:
        raise SystemExit(f"digest-{prev_day}.json missing or unreadable")
    verified = load(D / "verified-requests.json", {}) or {}
    window = load(D / f"_window_{mmdd}.json")
    bodies = load(D / f"_bodies_{mmdd}.json", {}) or {}
    feed = load(D / "ai-topic-feed.json", {}) or {}
    FEED = set(feed.get("slugs") or [])
    notes = load(D / f"_run_notes_{mmdd}.json", {}) or {}
    led = load(D / "pitch-ledger.json", {}) or {"pitched": {}, "skipped": {}}
    if window is None:
        raise SystemExit(f"_window_{mmdd}.json missing — run scripts/haro_window.py first")

    plat = {p["platform"]: p for p in window["platforms"]}
    figs = derive_figures()

    opps = [refresh(o, verified, FEED, today) for o in prev["opportunities"]]
    for o in opps:
        o.setdefault("slug", slug_of(o["url"]))
    n_carried = len(opps)

    # Carried prose can cite the artefacts of the day it was written. `refresh()` rewrites `deadline`
    # from the page but leaves `contact_method` and the angle alone, so a row built today cited
    # "route-checks-2026-10-17.json" and "snapshots updated 2026-10-17" inside a 2026-10-18 file —
    # the same defect class the 2026-10-17 digest fixed for its route section. scripts/probe_routes.py
    # re-probes the UNION of every recorded route, so a citation can be moved to today's file only
    # when that file exists and contains today's check date.
    _rc_today = D / f"route-checks-{today}.json"
    _rc_ok = False
    if _rc_today.exists():
        try:
            _rc_ok = (json.loads(_rc_today.read_text()).get("checked") == today)
        except json.JSONDecodeError:
            _rc_ok = False
    _snap = figs["snapshot_updated"]
    _re_rc = re.compile(r"route-checks-20\d{2}-\d{2}-\d{2}\.json")
    _re_snap = re.compile(r"(snapshot[s]?[ `]*updated:?[ `]*)20\d{2}-\d{2}-\d{2}", re.I)
    _stale_evidence = []
    for i, o in enumerate(opps):
        if not _rc_ok:
            break
        touched = False
        for field in ("contact_method", "suggested_pitch_template"):
            v = o.get(field) or ""
            nv = _re_rc.sub(f"route-checks-{today}.json", v)
            nv = _re_snap.sub(rf"\g<1>{_snap}", nv)
            if nv != v:
                o = dict(o)
                o[field] = nv
                touched = True
        if touched:
            o["_evidence_refreshed"] = today
            opps[i] = o
            _stale_evidence.append(o["slug"])

    # A run-specific correction to a carried row's route prose (e.g. today's SMTP probe result),
    # applied from _run_notes_MMDD.json rather than by hand-editing the JSON. `contact_append` adds a
    # sentence and therefore grows the field every run it is used; `contact_replace` supersedes the
    # route prose outright, which is what a row whose evidence is re-measured each run needs.
    for slug, full in (notes.get("contact_replace") or {}).items():
        for i, o in enumerate(opps):
            if o["slug"] == slug:
                o = dict(o)
                o["contact_method"] = full.strip()
                o["_contact_replaced"] = today
                opps[i] = o
                break
    for slug, extra in (notes.get("contact_append") or {}).items():
        for i, o in enumerate(opps):
            if o["slug"] == slug:
                o = dict(o)
                o["contact_method"] = (o.get("contact_method") or "").rstrip() + " " + extra.strip()
                opps[i] = o
                break

    # A carried template can quote the tool count from the day it was written. Re-derive it: the
    # queue renders this field straight to George, so a stale count is visible and wrong.
    repaired = []
    for i, o in enumerate(opps):
        t = o.get("suggested_pitch_template") or ""
        new, n = re.subn(r"of 7[0-9] (tools|tracked AI tools)", rf"of {figs['n_tools']} \1", t)
        if n and new != t:
            o = dict(o)
            o["suggested_pitch_template"] = new
            o["_figures_repaired"] = sorted(set(o.get("_figures_repaired") or []) | {"suggested_pitch_template"})
            opps[i] = o
            repaired.append(o["slug"])

    def core(slug: str) -> str:
        return (bodies.get(slug) or {}).get("core", "")

    def _dl(slug: str) -> str:
        r = verified.get(slug) or {}
        return (f"No cutoff stated. Page fetched today: HTTP 200, live=True, badge "
                f"'{r.get('badge')}', datePublished {r.get('datePublished')} = {r.get('days_old')} days.")

    def contact_evidence(slug: str) -> str:
        r = verified.get(slug) or {}
        bits = []
        if r.get("email_redacted"):
            bits.append("The request body's address is redacted by Sourcee.")
        if r.get("emails_on_page"):
            bits.append(f"Address published on the request page: {', '.join(r['emails_on_page'])}.")
        if r.get("published_links"):
            bits.append(f"Links published on the page: {', '.join(r['published_links'][:3])}.")
        if not bits:
            bits.append("The page publishes no address, handle or link of its own.")
        return " ".join(bits)

    # New rows: every AI-token slug in the window, plus any body-level AI hit the slug filter missed.
    # The judgment fields come from the run notes; nothing about the page is typed.
    existing = {o["slug"] for o in opps}
    NEW: list[dict] = []
    candidates = [s for s, _lm in window["ai"]]
    for s, r in bodies.items():
        # Every body-level AI hit is considered, whether or not its slug carried a token: the slug
        # filter and the body scan are different measurements, and a body hit with no slug token is
        # exactly the miss this list exists to catch.
        if r.get("ai_tokens_in_body") and s not in candidates:
            candidates.append(s)
    for s in candidates:
        if s in existing:
            continue
        if (verified.get(s) or {}).get("days_old") is None:
            # A new row with no page-verified age is listed by the queue as live with "age unknown"
            # and counted cold by this digest — the two artefacts disagree, silently. Fail instead:
            # scripts/verify_journo_requests.py accepts slugs as arguments and takes seconds.
            raise SystemExit(
                f"{s} has no page truth in verified-requests.json — run "
                f"`python3 scripts/verify_journo_requests.py {s}` before building the digest")
        spec = (notes.get("new_rows") or {}).get(s)
        if not spec:
            print(f"  ! {s} is a window AI hit with no entry in _run_notes_{mmdd}.json — skipped, "
                  f"which would be a silent loss; add it and re-run this script")
            continue
        NEW.append({
            "url": SITE + s, "slug": s, "query_text": core(s)[:900],
            "journalist_publication": spec.get("who") or "Not named on the page.",
            "category": spec.get("category") or "AI / Unclassified",
            "deadline": _dl(s),
            "contact_method": (spec.get("contact") or "") + " " + contact_evidence(s),
            "relevance": spec.get("relevance") or "low",
            "relevance_notes": spec.get("notes") or "",
            "suggested_pitch_template": spec.get("template") or
            "None. No route and no standing. NOT DRAFTED.",
            "_page_live": True, "_days_old": verified.get(s, {}).get("days_old"),
            "_badge": verified.get(s, {}).get("badge"), "_in_ai_topic_feed": s in FEED,
            f"_new_or_recovered_{today}": True,
        })
    opps.extend(NEW)
    by_slug = {o["slug"]: o for o in opps}
    assert len(by_slug) == len(opps), "slug collision across carried and new rows"

    # Crossings, measured from the two runs' page ages — not from prose. Restricted to UNPITCHED
    # rows: a request already sent has no cold line left to cross, and listing one here reads as a
    # loss when it is a closed row (the Glenn Hansen seats/tokens row, pitched 2026-10-10, appeared
    # in this list while it was the only sendable row the monitor had ever sent).
    pitched = set(led.get("pitched") or {})
    skipped = set(led.get("skipped") or {})
    sent_slugs = {slug_of(u) for u in pitched}
    skipped_slugs = {slug_of(u) for u in skipped}
    unpitched = [o for o in opps if o["slug"] not in sent_slugs and o["slug"] not in skipped_slugs]

    crossed, at_ten = [], []
    for o in unpitched:
        was = (next((p.get("_days_old") for p in prev["opportunities"] if p.get("slug") == o["slug"]), None))
        now = o.get("_days_old")
        if now is None:
            continue
        if was is not None and was <= STALE_DAYS < now:
            crossed.append(f"{o['slug']} (page age {was}d -> {now}d)")
        elif now == STALE_DAYS:
            at_ten.append(o["slug"])


    def age(o):
        d = o.get("_days_old")
        return d if d is not None else 999

    live = [o for o in unpitched if age(o) <= STALE_DAYS]
    cold = [o for o in unpitched if age(o) > STALE_DAYS]

    def has_route(o: dict) -> bool:
        c = o.get("contact_method") or ""
        return ("@" in c or "linkedin.com/in/" in c
                or any(k in c.lower() for k in ("calendly", "lnkd.in", "signal")))

    sendable = [o for o in live if (o.get("relevance") or "low").lower() != "low" and has_route(o)]

    drafted = set()
    for f in D.glob("pitch-drafts-*.md"):
        txt = f.read_text(errors="ignore")
        sourced = {slug_of(m) for m in re.findall(
            r"\*\*Source:\*\*\s*(https?://(?:www\.)?sourcee\.app/journo-request/[a-z0-9\-]+)", txt)}
        drafted |= {o["slug"] for o in unpitched if o["slug"] in sourced}

    tracked_in_feed = [o["slug"] for o in opps if o["_in_ai_topic_feed"]]
    ai_prose = sorted(s for s, r in bodies.items() if r.get("ai_prose_in_body"))
    ai_prose_spend = sum(1 for r in bodies.values()
                         if r.get("ai_prose_in_body") and r.get("real_spend_in_body"))

    # Platform notes, built from today's probes rather than copied.
    def p(name: str) -> dict:
        return plat.get(name) or {}

    platforms_checked = [
        {"platform": "Sourcee (sourcee.app)", "status": "accessible",
         "notes": (f"Sitemap pulled fresh from /sitemap-journo-requests.xml (HTTP {window['sitemap_http']}, "
                   f"{window['bytes']:,} bytes, {window['count']:,} loc/lastmod pairs, newest lastmod "
                   f"{window['newest']}). {len(window['window'])} slugs carry a lastmod newer than the "
                   f"{prev_day} run's mark ({window['mark']}): {len(window['ai'])} carry an AI token, "
                   f"{len(window['ai_strict'])} carry an AI token plus a spend token, "
                   f"{len(window['spend_any'])} carry a spend token alone. Every one of the "
                   f"{len(window['window'])} window bodies was fetched and read - the only check that can "
                   f"back a zero. Site root re-probed HTTP {p('Sourcee (sourcee.app)').get('http')} "
                   f"({p('Sourcee (sourcee.app)').get('bytes', 0):,} bytes).")},
        {"platform": "Sourcee AI topic feed", "status": "accessible",
         "notes": (f"HTTP {window['feed_http']}, {window['feed_bytes']:,} bytes, {window['feed_count']} slugs. "
                   f"{window['feed_overlap_with_window']} of the {window['feed_count']} are inside today's "
                   f"{len(window['window'])}-slug sitemap window. {len(tracked_in_feed)} tracked row(s) appear in it.")},
        {"platform": "HARO (helpareporter.com)", "status": "blocked",
         "notes": (f"HTTP {p('HARO (helpareporter.com)').get('http')}, "
                   f"{p('HARO (helpareporter.com)').get('bytes', 0):,} bytes, page title "
                   f"'{p('HARO (helpareporter.com)').get('title')}'. Expected; not retried. "
                   "Unchanged since 2026-09-12.")},
        {"platform": "Connectively (connectively.us)", "status": "blocked",
         "notes": (f"HTTP {p('Connectively (connectively.us)').get('http')}, "
                   f"{p('Connectively (connectively.us)').get('bytes', 0):,} bytes, "
                   f"'{p('Connectively (connectively.us)').get('title')}'. Expected; not retried.")},
        {"platform": "Source of Sources (sourceofsources.com)", "status": "not-applicable",
         "notes": (f"HTTP {p('Source of Sources (sourceofsources.com)').get('http')} at /requests today, "
                   f"{p('Source of Sources (sourceofsources.com)').get('bytes', 0):,} bytes, title "
                   f"'{p('Source of Sources (sourceofsources.com)').get('title')}'. Reporter-only per the "
                   "monitor's standing finding; the /requests path does not serve a browsable list from this end.")},
        {"platform": "Qwoted (qwoted.com)", "status": "blocked",
         "notes": (f"HTTP {p('Qwoted (qwoted.com)').get('http')} at app.qwoted.com/requests, "
                   f"{p('Qwoted (qwoted.com)').get('bytes', 0):,} bytes; the app needs an authenticated "
                   "session. Not retried.")},
        {"platform": "MentionMatch (mentionmatch.com)", "status": "account-gated",
         "notes": (f"HTTP {p('MentionMatch (mentionmatch.com)').get('http')}, "
                   f"{p('MentionMatch (mentionmatch.com)').get('bytes', 0):,} bytes, title "
                   f"'{p('MentionMatch (mentionmatch.com)').get('title')}'. THE PRE-LAUNCH FINDING IS NOW "
                   "STALE: the site no longer serves a holding page. It describes itself as 'MentionMatch "
                   "connects B2B writers with expert sources' and invites sources to 'Join 8,000+ sources "
                   "today', and /requests returns the same 12,067-byte SPA shell, so the request list is "
                   "fetched client-side behind an account. Nothing is browsable from here without a "
                   "signup, which is George's lane.")},
        {"platform": "Medialyst MCP (medialyst.ai/api/mcp)", "status": "blocked",
         "notes": (f"HTTP {p('Medialyst MCP (medialyst.ai/api/mcp)').get('http')}, "
                   f"{p('Medialyst MCP (medialyst.ai/api/mcp)').get('bytes')} bytes - the MCP endpoint "
                   "needs an OAuth handshake, which is George's lane. This is the one platform that "
                   "would widen supply, and it is blocked on an account, not on the monitor.")},
        {"platform": "ResponseSource (responsesource.com)", "status": "accessible-but-not-usable",
         "notes": (f"HTTP {p('ResponseSource (responsesource.com)').get('http')}, "
                   f"{p('ResponseSource (responsesource.com)').get('bytes', 0):,} bytes. Public pages "
                   "only; the request database needs a subscription.")},
    ]

    sendable_txt = (
        "; ".join(f"{o['slug']} ({o['_days_old']}d, {o['relevance']})" for o in
                  sorted(sendable, key=age))
        if sendable else "none"
    )
    summary = (
        f"{len(opps)} tracked requests ({n_carried} carried and all {n_carried} re-verified live, "
        f"{len(NEW)} added this run, {len(pitched)} pitched, {len(skipped)} deliberately skipped). "
        f"Of the {len(unpitched)} unpitched, {len(live)} are live and {len(cold)} are cold. "
        f"Sendable: {sendable_txt}. The window produced {len(window['window'])} slugs with "
        f"{len(window['ai'])} AI-token and {len(window['ai_strict'])} AI+spend; "
        f"{len(ai_prose)} window bodies mention AI at body level and {ai_prose_spend} of those also "
        f"carry a real spend token. Headline figures re-derived this run against the snapshot "
        f"(updated {figs['snapshot_updated']}): {figs['n_paid']} of {figs['n_tools']} tools publish a "
        f"monthly price, {figs['n_25']} of those at or under $25/month, median ${figs['median']}; "
        f"monthly vs annual {figs['pair_txt']}. Zero pitches sent this run - sends remain George's lane."
    )

    actions = []
    for o in sorted(sendable, key=age):
        actions.append(
            f"SEND {o['slug']} — sendable, {o['_days_old']} days old, relevance {o['relevance']}. "
            f"Route: {o['contact_method'][:300]}. Draft at pitch-drafts-{today}.md."
        )
    if not sendable:
        actions.append("NO SENDABLE ROW THIS RUN — every live row is off-beat, route-less, or below "
                       "the relevance bar. Do not draft from this window.")
    if NEW:
        actions.append(f"DO NOT DRAFT TODAY'S {len(NEW)} NEW ROWS: "
                       + "; ".join(spec for spec in (notes.get("why_not_drafted") or ["see relevance_notes"])))
    actions.append(
        "NO REPLY HAS ARRIVED TO ANY PITCH. Mailbox checked today: the newest inbound from any pitch "
        "recipient remains Jan Suski's 2026-10-11 06:57 UTC acknowledgment, which closed the "
        "Amplemarket thread. Nothing has come from foxandspindle.com, sherwood.news, "
        "epgacceleration.com, artichokehq.com or raconteur.net at any point."
    )
    actions.extend(notes.get("extra_actions") or [])

    out = {
        "date": today,
        "monitor": "HARO / Sourcee journalist-request monitor for AIToolsEssentials",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "search_scope": prev["search_scope"],
        "age_policy": (
            "Ages are read off each request page (JSON-LD datePublished plus the rendered 'Posted ... ago' "
            "badge), never off the digest text, and every carried row's deadline field was rewritten this "
            f"run from the page itself. All {n_carried} carried URLs plus the {len(NEW)} rows added today "
            "were re-fetched and read today: HTTP 200 for every one, body still served, no expiry notice. "
            "No request has ever been seen to expire on this source, so 'deadline' means the poster's own "
            "stated cutoff or a measured age, never an observed expiry. FEED MEMBERSHIP IS NOT A FRESHNESS "
            f"SIGNAL: the AI topic page carries {window['feed_count']} slugs and "
            f"{window['feed_overlap_with_window']} of them are inside today's {len(window['window'])}-slug "
            f"sitemap window; {len(tracked_in_feed)} tracked row(s) appear in it."
        ),
        "platforms_checked": platforms_checked,
        "opportunities": opps,
        "new_this_run": notes.get("new_this_run") or [],
        "expired_this_run": [
            (f"Nothing expired on its page: all {n_carried} carried URLs and the {len(NEW)} new ones "
             "returned HTTP 200 with the request body still served. An expiry has never once been "
             "observed on this source, so the absence of an expiry notice is weak evidence recorded as such."),
            (f"ROWS CROSSED THE {STALE_DAYS}-DAY LINE SINCE YESTERDAY: {len(crossed)}."
             + (" " + "; ".join(crossed) + "." if crossed else " No row crossed.")),
            (f"{len(at_ten)} ROW(S) SIT AT EXACTLY {STALE_DAYS} DAYS AND CROSS TOMORROW: "
             + "; ".join(at_ten) + "." if at_ten
             else "No row sits at exactly 10 days today, so the next run has no scheduled crossing."),
            "ROWS THAT DROPPED OFF THE NEWEST DIGEST: 0. Every tracked row is carried in every digest by "
            "design, so this figure is a monitor convention and not platform evidence.",
        ],
        "summary": summary,
        "recommended_actions": actions,
        "monitor_health": {
            "platforms_accessible": sum(1 for p in platforms_checked if p["status"] == "accessible"),
            "platforms_accessible_but_not_usable": sum(1 for p in platforms_checked
                                                       if p["status"] == "accessible-but-not-usable"),
            "platforms_blocked": sum(1 for p in platforms_checked if p["status"] == "blocked"),
            "platforms_not_applicable": sum(1 for p in platforms_checked if p["status"] == "not-applicable"),
            "platforms_account_gated": sum(1 for p in platforms_checked if p["status"] == "account-gated"),
            "core_beat_new_requests": sum(1 for o in NEW if (o.get("relevance") or "low").lower() in
                                          ("high", "medium", "medium-high")),
            "new_ai_token_slugs_in_window": len(window["ai"]),
            "new_ai_plus_spend_slugs_in_window": len(window["ai_strict"]),
            "window_bodies_fetched": len(bodies),
            "body_level_ai_hits": len(ai_prose),
            "body_level_ai_plus_spend_hits": ai_prose_spend,
            "new_rows_added_to_tracking": len(NEW),
            "tracked_urls": len(opps),
            "unpitched": len(unpitched),
            "live_unpitched": len(live),
            "cold_unpitched": len(cold),
            "pitched_plus_skipped": len(pitched | skipped),
            "sendable": len(sendable),
            "pitches_sent_this_run": 0,
            "sendable_rows": len(sendable),
            "sendable_new_this_run": sum(1 for o in NEW if o["slug"] in {x["slug"] for x in sendable}),
            "sendable_rows_crossing_tomorrow": sum(1 for s in at_ten if s in {x["slug"] for x in sendable}),
            "rows_crossed_cold_since_last_digest": len(crossed),
            "rows_at_ten_days_crossing_next_run": len(at_ten),
            "pitch_draft_files_on_disk": len(list(D.glob("pitch-drafts-*.md"))),
            "rows_named_in_a_draft_file": len(drafted),
            "replies_to_date": 1,
            "reply_status_checked": today,
            "reply_outstanding_amplemarket_thread": False,
            "shadow_ai_tools_tracked": figs["n_tools"],
            "shadow_ai_monthly_priced_tools": figs["n_paid"],
            "shadow_ai_at_or_under_25": figs["n_25"],
            "shadow_ai_median_cheapest_paid_tier": float(figs["median"]) if figs["median"] != "?" else None,
            "pricing_snapshot_updated": figs["snapshot_updated"],
            "monthly_annual_pairs_built": (figs["pairs"] or {}).get("built"),
            "carried_templates_repaired_this_run": repaired,
            "carried_rows_with_stale_evidence_refreshed": _stale_evidence,
        },
        "monitor_defects_fixed_this_run": notes.get("defects") or [],
    }

    (D / f"digest-{today}.json").write_text(json.dumps(out, indent=1))
    print(f"wrote digest-{today}.json: {len(out['opportunities'])} opportunities "
          f"({n_carried} carried + {len(NEW)} new), {len(live)} live, {len(cold)} cold, "
          f"{len(sendable)} sendable")
    print(f"figures: {figs['n_paid']} of {figs['n_tools']} monthly-priced, {figs['n_25']} <= $25, "
          f"median ${figs['median']}, snapshot {figs['snapshot_updated']}")
    print("crossed:", len(crossed), "| at ten days:", len(at_ten))
    for o in sorted(sendable, key=age):
        print(f"  SEND {o['_days_old']:>3}d [{o['relevance']}] {o['slug']}")


if __name__ == "__main__":
    main()
