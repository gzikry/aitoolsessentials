# Weekly traffic report — 2026-10-05

## Headline: no traffic figures are available this week (site still locked)

**The Plausible site is locked, so every metric below is blank. There are no estimates in
this report and no fabricated ranges.** Nothing here should be read as "traffic fell to
zero" — the numbers are *unavailable*, which is a different thing from zero. Prior figures
are not carried forward and are not restated as current.

This is the **second consecutive week** with no measurable data (2026-09-28 was the first).

## What was actually run

```
python3 scripts/plausible_report.py --period 30d
python3 scripts/plausible_report.py --period 7d
```

Both exited **3** with this on stderr and no numbers printed:

```
Plausible API returned an error — no metrics can be reported.
Reason: This Plausible site is locked due to missing active subscription. In order to
access it, the site owner should subscribe to a suitable plan
Do NOT record this as zero traffic; the data is unavailable.
```

Re-verified as deterministic across every window — `day`, `7d`, `30d`, `month`, `6mo`,
`12mo`, `all` — all returned the identical error object. This is a site-level lock, not a
narrow query failure.

## Cross-checks: the problem is Plausible's, not ours

Checked before attributing this to the account, all re-run this week:

1. **The API is reachable and healthy.** An unauthenticated control request to
   `/api/v2/query` returns `HTTP 401 {"error":"Missing API key..."}` — the endpoint answers
   correctly. With our bearer token the same endpoint returns the *site lock*, not an auth
   error. So this is neither a network failure nor a bad token; it is the site's
   subscription state.
2. **The token is valid and unchanged.** The error is a *site* lock ("the site owner should
   subscribe"), not a 401. `~/.hermes/profiles/aitools/plausible_token` is unchanged since
   2026-08-25 (mode 600). The token value was not printed at any point.
3. **Tracking is still installed and live.** `js/analytics.js` is referenced by **741 of
   757** HTML pages on disk; the live homepage serves it (`/js/analytics.js` → HTTP 200),
   the loader still points at `https://plausible.io/js/script.js` (HTTP 200) for
   `aitoolsessentials.com`, and the locked front door `/stack-audit.html` → HTTP 200. The
   site is not the blocker.

## Metrics

| Metric | 7d | 30d |
|---|---|---|
| Visitors | *(unavailable)* | *(unavailable)* |
| Pageviews | *(unavailable)* | *(unavailable)* |
| Bounce rate | *(unavailable)* | *(unavailable)* |
| Avg visit duration | *(unavailable)* | *(unavailable)* |
| Top pages | *(unavailable)* | *(unavailable)* |
| Sources | *(unavailable)* | *(unavailable)* |
| Conversion goals | *(unavailable)* | *(unavailable)* |
| Stack Audit funnel | *(unavailable)* | *(unavailable)* |

## Last verified figures on record (2026-09-21 — historical, not current)

Carried here for continuity only. These are the final numbers that were actually read from
the v2 API, describing the week ending **2026-09-21**. They are **not** this week's traffic
and no trend should be inferred across the gap.

- Week (7d): **18 visitors / 36 pageviews**, 83% bounce, avg visit 74s
- 30d: **95 visitors / 283 pageviews**, 62% bounce, avg visit 124s
- All-time: 96 visitors / 284 pageviews (recording began 2026-08-23)
- Prior standing finding: of ~95 visitors, only ~12 were organic search — roughly 93 of 95
  were Direct/bot traffic
- AdSense remains gated by traffic (~7 PV/day from search vs. the ~500 PV/day where ads are
  worth running)

## The action that unblocks this

**George-only lane.** Restoring Plausible requires a payment decision in the Plausible
account, which I do not make and cannot do.

- **Option A — subscribe to Plausible** (Starter ≈ $9/month). Restores the API immediately
  and keeps the existing history continuous and directly comparable to prior reports.
  Plausible offers a student discount if that applies.
- **Option B — switch to Google Analytics 4 (free).** Worth weighing honestly at this
  traffic level: paying ~$9/month to measure ~12 real organic visitors is poor value, and
  GA4 is free. The tradeoff is losing continuous comparability with the Plausible history
  and Plausible's cleaner bot filtering.

**Google Search Console is unaffected by this lock** and remains the better signal source at
this stage. The 2026-09-12 diagnosis (4,665 impressions over 20 days, 6 clicks, CTR 0.129%,
average position 51.6) still stands as the last on-disk GSC export — no fresh export exists,
so it is not restated as current.

## Risk if this stays locked

A locked Plausible site may not be ingesting events. If that is the case, traffic during the
lock window is being **lost rather than hidden**, and subscribing later will not recover it.
The gap is now **~2 weeks**. I cannot verify the ingest state from the API — this is a risk
to confirm on the Plausible side, not a claim. If ingest is stopped, every week of delay
permanently reduces the baseline the next report can compare against.

## Note on the reporting tooling

`scripts/plausible_report.py` is v2-only by design and raises on an API `error` response,
writing the reason to stderr and exiting non-zero rather than emitting a misleading empty
header (a silent-fallback bug fixed on 2026-09-28). No figure in this report was produced by
a fallback, a v1 endpoint, or an estimate.
