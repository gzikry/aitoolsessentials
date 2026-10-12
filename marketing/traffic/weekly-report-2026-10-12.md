# Weekly traffic report — 2026-10-12

## Headline: third consecutive week with no measurable traffic — and this week I can now
## tell you what the lock actually does to the data

**Every metric below is blank. There are no estimates and no fabricated ranges in this report.**
Blank is not zero: the numbers are *unavailable*.

New this week: last week's report called the risk of data loss *unverified*. It is now verified
from Plausible's own documentation, and the news is worse than "the dashboard is hidden" — see
**What the lock actually does**, below.

## What was actually run

```
python3 scripts/plausible_report.py --period 30d
python3 scripts/plausible_report.py --period 7d
```

Both exited **3**, printing no numbers and this on stderr (v2 API, token read from
`~/.hermes/profiles/aitools/plausible_token`; token value never printed):

```
Plausible API returned an error — no metrics can be reported.
Reason: This Plausible site is locked due to missing active subscription. In order to
access it, the site owner should subscribe to a suitable plan
Do NOT record this as zero traffic; the data is unavailable.
```

Re-confirmed as a site-level lock, not a query failure — `day`, `7d`, `30d`, `month`, `6mo`,
`12mo`, `all` all returned the identical error object.

## What the lock actually does (verified this week, with sources)

Last week this was flagged as an unverified risk. It is documented:

1. **New stats stop being collected.** Plausible, /docs/trial (linked from the docs as "see what
   happens when your trial ends"): *"If you don't subscribe, we'll stop collecting new stats and
   eventually delete your dashboards and all their stats permanently."*
2. **Deletion is permanent, with an email warning first.** Same page: *"We'll email you before
   deletion so you have time to subscribe or export your stats… Deleted stats cannot be
   recovered."*
3. **This is the trial-expiry path, not the over-quota path.** The over-limit lock behaves
   differently — /docs/billing says stats *"continue to be collected in the background"* while
   over-limit dashboards are locked. Our error is *"missing active subscription"*, i.e. the
   trial-expiry path, where collection **stops**. So the last three weeks are being **lost, not
   hidden**.
4. **The trial never auto-charges.** /docs/trial: no credit card, *"Your trial never converts
   into a paid subscription automatically."* There is nothing to cancel.

## The timeline, reconstructed from on-disk reports

- Recording began **2026-08-23** (Plausible trial is 30 days) → trial would have ended **~2026-09-22**.
- The **2026-09-21** report still read real data from the v2 API; the **2026-09-28** report is the
  first with no data. That brackets the lock to the ~Sep 22 trial expiry.
- So this is roughly **20 days** (Sep 22 → Oct 12) of traffic that was never recorded.
- Every additional week the decision slips permanently reduces the baseline the next report can
  compare against. There is no documented deletion date — "eventually" is the only wording.

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

## Cross-checks re-run this week (the blocker is not on our side)

- **API endpoint healthy:** unauthenticated control POST to `/api/v2/query` → `HTTP 401
  {"error":"Missing API key…"}`. With our bearer token the same endpoint returns the *site lock*,
  not an auth error — so not a network failure and not a bad token.
- **Token unchanged:** `~/.hermes/profiles/aitools/plausible_token`, mode 600, mtime
  **2026-08-25 13:40** — untouched.
- **Tracking still installed and live:** live `https://aitoolsessentials.com/` → 200,
  `/js/analytics.js` → 200, `/stack-audit.html` → 200; the loader still targets
  `https://plausible.io/js/script.js` for `aitoolsessentials.com`. **754** HTML files on disk
  reference `/js/analytics.js`. The site is not the blocker — and if the tag has been firing into
  a stopped collector, that is exactly the loss described above.
- **Plausible is the only analytics installed.** No GA4/gtag, GoatCounter, Umami, Matomo or
  Cloudflare Insights snippet exists anywhere on disk. There is no second source to fall back on.

## Last verified figures on record (2026-09-21 — historical, NOT current)

Carried for continuity only; they describe the week ending 2026-09-21 and no trend should be
inferred across the gap:

- Week (7d): **18 visitors / 36 pageviews**, 83% bounce, avg visit 74s
- 30d: **95 visitors / 283 pageviews**, 62% bounce, avg visit 124s
- All-time: 96 visitors / 284 pageviews
- Standing finding: of ~95 visitors, only **~12 were organic search** — ~93 of 95 were
  Direct/bot traffic, so read that 95 as ~12 real humans
- AdSense is still gated by traffic (~7 search PV/day vs. the ~500 PV/day where ads pay)

## Actionable observations (tied to the real numbers above)

1. **Export the history before it can be deleted — this is the only irreversible loss on the
   table.** ~96 all-time visitors is small, but it is the entire measurement baseline and
   Plausible's docs explicitly offer export "before deletion." If you subscribe, nothing resets
   (docs: *"Nothing is reset when you upgrade"*).
2. **Paying ~$9/month to measure ~12 organic visitors is poor value — say so plainly.** The
   honest comparison, at the last verified figures: Plausible Starter ≈ $9/mo to count ~12 real
   humans/month, versus **Google Analytics 4 at $0**, versus **Google Search Console at $0 —
   already the better signal source** at this stage (last export 2026-09-12: 4,665 impressions,
   6 clicks, CTR 0.129%, avg position 51.6 — no newer export exists, so it is not restated as
   current).
3. **GSC is unaffected by this lock and is the measurement that should carry the next report.**
   A fresh GSC export is the cheapest way to restore week-over-week numbers without paying
   anything. Both GSC access and any GA4 property creation are your lane (account work), not mine.

## The decision (George-only lane)

I cannot pay for, subscribe to, or create an analytics account. Two viable paths:

- **Option A — subscribe** (Starter ≈ $9/mo, student discount available): restores the API
  immediately, keeps the history continuous and directly comparable to the earlier reports, and
  resumes collection.
- **Option B — don't pay:** export the existing stats now to preserve history, then let GSC +
  GA4 (both free) carry measurement. GA4 needs a property under your Google account; GSC only
  needs a fresh export.

Either way, **export first.** That step is free and it is the difference between a
three-week gap and a permanent loss of the whole record.

## Note on the tooling

`scripts/plausible_report.py` is v2-only by design and raises on an API `error` response
(stderr + non-zero exit) rather than emitting a misleading empty report. No figure in this
report came from a fallback, a v1 endpoint, or an estimate.
