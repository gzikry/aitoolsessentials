# Weekly traffic report — 2026-10-19

## Headline: fourth consecutive week with no measurable traffic

**Every Plausible metric below is blank. Blank is not zero — the data is unavailable.**
No figure in this report is estimated, ranged, or carried forward as current.

The API did not return an empty result. It returned a site-level lock:

```
python3 scripts/plausible_report.py --period 30d   → exit 3
python3 scripts/plausible_report.py --period 7d    → exit 3

Plausible API returned an error — no metrics can be reported.
Reason: This Plausible site is locked due to missing active subscription. In order to
access it, the site owner should subscribe to a suitable plan
Do NOT record this as zero traffic; the data is unavailable.
```

v2 `/api/v2/query` only; token read by the script from
`~/.hermes/profiles/aitools/plausible_token` (never printed).

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

## What was re-checked this week (blocker is still not on our side)

- **Site is up:** `https://aitoolsessentials.com/` 200, `/js/analytics.js` 200,
  `/stack-audit.html` 200 (live check, 2026-10-19).
- **Tag still installed:** loader targets `https://plausible.io/js/script.js`; **834** HTML files
  reference `/js/analytics.js` (was 754 on 2026-10-12 — the site grew while measurement is off).
- **Token untouched:** `plausible_token`, mode 600, mtime 2026-08-25 13:40.
- **No fallback analytics:** no GA4/gtag, GoatCounter, Umami, Matomo, or Cloudflare snippet on
  disk. Plausible is the only source, so there is no second number to cross-check against.
- **Only change since last report:** the gap got a week longer. Last reportable datum is the week
  ending **2026-09-21**; trial expiry ≈ 2026-09-22; that is **27 days** of unrecorded traffic as of
  today, and Plausible's docs say trial-expiry stops collection and later deletes stats.

## The measurement that *is* still working

Google Search Console is unaffected by the Plausible lock. From `docs/gsc-drop-2026-10-17.md`
(checked 2026-10-17, not a traffic metric and not a substitute for one):

- Impressions fell from ~250–480/day to **~0 from 2026-09-16**.
- Indexed pages fell **640 → 405** (drops dated 2026-09-21 and 2026-10-04).
- Not indexed: 656 total — 208 Not found (404), 107 canonical alternates, 248 crawled–not indexed,
  88 discovered–not indexed.
- 59 previously published URLs are now live 404s with no redirect; 23 are noindex refresh stubs.

## Actionable observations

1. **The impressions cliff is the real problem, not the missing visitor count.** If Google has
   shown the site ~0 impressions for a month, a restored visitor number would read near zero
   anyway. Restoring redirects for the 59 dead URLs is free and is the only lever here that does
   not need an account or a payment.
2. **Each week of delay weakens the next comparison.** The site is now 834 pages versus 754 when
   measurement stopped. When analytics returns, the "before" baseline (week ending 2026-09-21:
   18 visitors / 36 pageviews; 30d 95 / 283, of which ~12 were organic) will describe a smaller,
   different site — plan to treat the return as a new baseline rather than a trend continuation.
3. **Decide the analytics vendor once, not weekly.** Plausible Starter ≈ $9/mo for ~12 real
   humans/month is poor value at this size; GA4 is $0 and Search Console is $0 and already the
   better signal. Either path needs your account action (subscribe, or create the GA4 property) —
   I can't pay for or create accounts.

## Standing (historical, NOT current)

Week ending 2026-09-21: 18 visitors / 36 pageviews, 83% bounce, avg visit 74s.
30d to 2026-09-21: 95 visitors / 283 pageviews, 62% bounce, avg visit 124s.
~93 of those 95 were Direct/bot traffic; ~12 were organic search. Do not read these as this week.
