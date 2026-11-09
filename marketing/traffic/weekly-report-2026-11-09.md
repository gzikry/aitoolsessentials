# Weekly traffic report — 2026-11-09

## Headline: sixth consecutive week with no measurement — and the monitor itself missed a week

**Every Plausible metric is blank. Blank is not zero — the data is unavailable.**
No figure below is estimated, ranged, or carried forward as current.

The API did not return empty results. It returned a site-level lock:

```
python3 scripts/plausible_report.py --period 30d   → exit 3
python3 scripts/plausible_report.py --period 7d    → exit 3

Plausible API returned an error — no metrics can be reported.
Reason: This Plausible site is locked due to missing active subscription. In order to
access it, the site owner should subscribe to a suitable plan
Do NOT record this as zero traffic; the data is unavailable.
```

This is a subscription lock, not a credential problem: the token at
`~/.hermes/profiles/aitools/plausible_token` is present, mode 600, 65 bytes, mtime
**2026-08-25 13:40** — unchanged since it was issued. v2 `/api/v2/query` only.

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

## What is new this week

**1. There is no 2026-11-02 report because the run failed, not because there was nothing to say.**
Job `4bd2baf551f4` ("AIToolsEssentials weekly traffic report", `0 9 * * 1`, enabled) records
`last_status: error` with:

```
RuntimeError: HTTP 429: you (georgezikry) have reached your session usage limit
```

So the ledger is 09-07 → 10-26 with a hole at 11-02. That hole is a model-quota failure on the
runner, not a site fault and not a lost measurement — there has been nothing to measure since 09-21.

**2. Publishing did not slow down while measurement stayed dark.** Like-for-like counts at the
last report commit (`e91c067ce`, 2026-10-26) versus today:

| | 2026-10-26 | 2026-11-09 | Δ |
|---|---|---|---|
| Tracked HTML pages | 1014 | **1266** | +252 |
| Pages loading the analytics loader | 996 | **1136** | +140 |
| Sitemap URLs | 908 | **1046** | +138 |

That is two weekly slots (one unmonitored) and 252 new pages, none of which can be measured.

**3. The `.html` → trailing-slash tool-page migration is clean, and it is bigger than it looks.**
I found 194 files carrying a meta refresh and did not report that as a doubling of redirects —
109 of them are `/go/` affiliate hop pages (live, robots-disallowed, working as intended). The
real redirect surface is:

- **85** internal-destination soft redirects, **73** unique destinations
- **73/73 destinations return HTTP 200** in production (checked individually, URL-encoded)
- **0** of them appear in `sitemap.xml`
- Internal linking is essentially migrated: **5098** hrefs to `/tools/x/` shape, **3** to flat
  `/tools/x.html` — and all three are in `admin/`, which `robots.txt` disallows

Mechanically these are still meta-refresh stubs with a self-targeting canonical and
`noindex,follow`: GitHub Pages cannot serve a real 301 for an arbitrary path. Adequate to stop
scoring 404s, not equivalent to a redirect, and I am not claiming the indexed count recovers.

**4. Live-site checks (2026-11-09):** `/` 200, `/js/analytics.js` 200, `/stack-audit.html` 200,
`/sitemap.xml` 200 (1046 URLs, all `lastmod` 2026-11-09). `robots.txt` allows crawling, disallows
`/admin/ /checkout/ /go/`, and declares both sitemaps.

**5. The free replacement is still one string away.** `js/analytics.js` line 63, as served in
production, reads `var CF_WA = { token: '', version: '2024.11.0' };`. Empty token = disabled by
design, so nothing is sent. Meanwhile the Plausible loader on line 11 still points at
`https://plausible.io/js/script.js` and fires from all **1136** pages at an account returning 402.

## Actionable observations

1. **The cheapest unblock is not the $9/mo Plausible plan — it is the free Cloudflare beacon that
   is already in production code.** The gap is one 32-character hex token pasted at line 63 of
   `js/analytics.js`: a free Cloudflare account, no card, no DNS change (the beacon posts to an
   absolutely addressed `cloudflareinsights.com/cdn-cgi/rum`, verified 2026-10-21). What you give
   up versus Plausible is custom conversion events: Cloudflare gives pageviews, referrers, paths,
   countries, device class — not `conversion_premium` / `conversion_pricing`. So the real choice is
   **$0 for views-only** or **$9/mo for views plus goals**. Both beat a seventh blank report.
2. **Decide the fate of the dead Plausible loader on 1136 pages.** It currently sends every visitor
   to a 402 endpoint: no data, one extra third-party request, disclosed in `legal/privacy.html` but
   serving nothing. The only argument for keeping it is that goal tracking resumes with zero code
   change if the plan is ever paid. Six weeks is long enough that "keep it just in case" is itself
   the decision — state it or reverse it.
3. **Expect index churn from the migration and do not read it as decline.** 85 soft redirects and
   140 new tracked pages entered the crawl queue since the last report, with Google needing a
   recrawl cycle to retire the old `.html` URLs. Without GSC or pageview data there is no way to
   distinguish "recrawl in progress" from "traffic fell" — and the next report will not be able to
   either if the token is still empty.
4. **GSC remains the single unused free signal.** No verification file is on disk and it is not
   reachable from here; if verification was never completed, it is a George-only step and it is the
   only free source for impressions, queries and CTR — the exact data that would tell us whether
   the migration cost anything.

## Standing (historical, NOT current)

Week ending 2026-09-21: 18 visitors / 36 pageviews, 83% bounce, avg visit 74s.
30d to 2026-09-21: 95 visitors / 283 pageviews, 62% bounce, avg visit 124s.
~93 of those 95 were Direct/bot traffic; ~12 were organic search. Do not read these as this week:
the site has gone from 740 to 1266 tracked HTML pages (+526) since that window closed, so a trend
line across the gap would be measuring a different site.
