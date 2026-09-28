# Weekly traffic report — 2026-09-28

## Headline: no traffic figures are available this week

**The Plausible site is locked, so every metric in this report is blank. There are no
estimates here and no fabricated ranges.** Nothing below should be read as "traffic fell
to zero" — the numbers are *unavailable*, which is a different thing from zero. The
previous report's figures cannot be carried forward and are not restated as current.

## What was actually run

```
python3 scripts/plausible_report.py --period 30d
python3 scripts/plausible_report.py --period 7d
```

Both exited 0 and printed a header with no numbers under it. Investigating at the API
level rather than trusting that output, `/api/v2/query` returned this for **every**
combination of window and dimension:

```
This Plausible site is locked due to missing active subscription.
In order to access it, the site owner should subscribe to a suitable plan
```

Re-verified as deterministic — 3 identical calls, same error. Windows tried: `day`, `7d`,
`30d`, `month`, `year`, `all`. Dimensions tried: `event:page`, `visit:source`,
`event:name`, `visit:country`, `visit:browser`. All returned the same error object. This is
a site-level lock, not a narrow query failure.

## Why: the 30-day free trial expired

This is an inference, but a well-supported one — the error text names a subscription, and
the dates line up exactly:

- Plausible recording for this domain began **2026-08-23** (established in the 09-21 report:
  08-22 returns 0, 08-23 returns 3).
- A 30-day trial starting 08-23 ends **2026-09-22**.
- The **09-21** report pulled real data successfully. The **09-28** report is the first
  failure.

Last working run: 09-21. Trial expiry: 09-22. First failed run: 09-28. The lock begins
precisely at the trial boundary, and the error says "missing active subscription" — i.e.
subscription was never started, rather than lapsed after purchase. I cannot see Plausible's
billing state from here, so treat the trial-expiry link as a strong hypothesis, not a
confirmed fact.

## Cross-checks: the problem is Plausible's, not ours

Three things were checked before attributing this to the account:

1. **The token is valid.** The error is a *site* lock ("the site owner should subscribe"),
   not an auth rejection. A bad or expired token returns a 401-class auth error instead.
   The token file is unchanged since 2026-08-25.
2. **Tracking is still installed.** `js/analytics.js` (the Plausible loader) is referenced
   by **739 of 750** HTML pages, and the loader itself still points at
   `https://plausible.io/js/script.js` for `aitoolsessentials.com`. The site is not the
   blocker.
3. **The API is reachable and responding** — with an application-level error, not a
   network failure or timeout.

The `***` seen when reading `scripts/plausible_report.py` is a display mask; the script
does send the real bearer token. The token value was not printed at any point.

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
the v2 API and they describe the week ending **2026-09-21**. They are **not** this week's
traffic and no trend should be inferred across the gap.

- Week (7d): **18 visitors / 36 pageviews**, 83% bounce, avg visit 74s
- 30d: **95 visitors / 283 pageviews**, 62% bounce, avg visit 124s
- All-time: 96 visitors / 284 pageviews (recording began 2026-08-23)
- Prior standing finding: of ~95 visitors, only ~12 were organic search — roughly 93 of 95
  were Direct/bot traffic
- AdSense remains gated by traffic (~7 PV/day from search vs. the ~500 PV/day where ads
  are worth running)

## The one action that unblocks this — and a cheaper alternative

**George-only lane.** Restoring Plausible requires a payment decision in the Plausible
account, which I do not make and cannot do for you.

- **Option A — subscribe to Plausible** (Starter is roughly $9/month). Restores the API
  immediately and keeps the existing history continuous and directly comparable to the
  prior reports. Plausible offers a student discount if that applies.
- **Option B — switch to Google Analytics 4 (free).** Worth weighing honestly at this
  traffic level: paying ~$9/month to measure ~12 real organic visitors is poor value, and
  GA4 is free. The tradeoff is losing continuous comparability with the Plausible history
  and Plausible's cleaner bot filtering.

Either way, **Google Search Console is unaffected by this lock** and is currently the better
signal source at this stage of the site's life. The 09-12 diagnosis (4,665 impressions over
20 days on 306 pages, avg position ~44, `best ai tools for agencies` at 259 impressions and
position 29.6 with zero clicks) still stands — but no fresh GSC export is on disk, so it
is not restated as current either.

## Risk if this stays locked

A locked Plausible site may not be ingesting events. If that is the case, the traffic
during the lock window is being lost rather than merely hidden, and subscribing later will
not recover it. I have not been able to verify the ingest state from the API, so this is a
risk to confirm on the Plausible side, not a claim.

## Note on the reporting tooling

`scripts/plausible_report.py` printed a valid-looking empty report (exit 0, no numbers)
when the API returned an error object, which on 09-28 looked exactly like genuine zero
traffic. It has been fixed in the same commit as this report: the wrapper now raises on an
API `error` response, writes the reason to stderr, and exits non-zero instead of emitting
a misleading empty header. Reported figures must never come from a silent fallback.
