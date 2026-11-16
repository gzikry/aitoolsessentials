# Weekly traffic report — 2026-11-16

## Headline: seventh consecutive week with no measurement — and a correction: GSC was never blocked

**Every Plausible metric is blank. Blank is not zero — the data is unavailable.**
No figure below is estimated, ranged, or carried forward as current.

Both wrapper runs failed against the Plausible v2 API with an explicit site-level lock:

```
python3 scripts/plausible_report.py --period 30d   → exit 3
python3 scripts/plausible_report.py --period 7d    → exit 3

Plausible API returned an error — no metrics can be reported.
Reason: This Plausible site is locked due to missing active subscription. In order to
access it, the site owner should subscribe to a suitable plan
Do NOT record this as zero traffic; the data is unavailable.
```

This is a subscription lock, not a credential problem. The token at
`~/.hermes/profiles/aitools/plausible_token` is present, mode 600, 65 bytes, mtime
**2026-08-25 13:40** — unchanged since issue. The wrapper authenticates with it (the API
answered with a site-level error, not `Invalid API key`), which is how we know the lock is
billing-side. v2 `/api/v2/query` only, as required.

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

**1. Publishing ran at full speed with zero measurement: +150 pages in seven days.**

| | 2026-11-09 report | 2026-11-16 | Δ |
|---|---|---|---|
| Tracked HTML pages | 1266 | **1416** | +150 |
| Pages loading the analytics loader | 1136 | **1277** | +141 |
| Sitemap URLs | 1046 | **1187** | +141 |
| Comparison pages | — | **600** | (130 added this week) |

The 150 new files decompose exactly: **9 new tool pages** (01Router, Accuratescribe,
AgentMsgr, AI Image To Prompt, Dreammmer, Edit Pic Text, MakifyAI, Random Topic Generator,
RapVideoGo), **9 `/go/` affiliate hop pages**, **130 comparison pages**, and 2 articles.
Coverage is not the problem: **every HTML page in `sitemap.xml` loads `js/analytics.js`
(0 missing)** — the instrument is wired into all 1187 indexable pages and pointed at a dead
account.

**2. Correction to last week's report: Search Console verification has existed since August.**
Last report said "no verification file is on disk… if verification was never completed, it is
a George-only step." That was wrong in a consequential way. `index.html` has carried
`<meta name="google-site-verification" content="OzzGs2QF4v6zSBd9uO95NGgSPH5B598E6DPtcjRNn_4">`
since commit `c69e020bf` (2026-08-22), and it is served live in production (checked this run).
So the tag is not the blocker; only the Search Console login/export is. That matters because
GSC is the one free source of impressions, queries and CTR that does not depend on the
Plausible subscription.

**3. The zero-cost analytics path is unchanged and still one string away.**
`js/analytics.js` line 63 still reads `var CF_WA = { token: '', version: '2024.11.0' };`.
Empty token = disabled by design. The Cloudflare Web Analytics beacon posts to
`cloudflareinsights.com/cdn-cgi/rum` with no card and no DNS change; only custom conversion
events are lost versus Plausible. Meanwhile the Plausible loader on line 11 still fires from
**1277 pages** into a locked account — one third-party request per visitor that stores nothing.

**4. Live checks (2026-11-16):** `/` 200 · `/stack-audit.html` 200 · `/sitemap.xml` 200 (1187
URLs) · `/js/analytics.js` 200 · `/categories/AI%20Agents/` 200 · `/categories/Local%20AI/` 200.
`robots.txt` allows crawling, disallows `/admin/ /checkout/ /go/`, declares both sitemaps.
The 5 percent-encoded category URLs in the sitemap resolve 200 in production — not a defect.

**5. Checked and NOT reported as a problem: the 130 new comparison pages are not near-duplicates.**
130 templated pages in one week is exactly the shape of a thin-content problem, so I tested it
rather than assuming. Unrelated pairs (e.g. `jasper-vs-makifyai` vs `copy-ai-vs-dreammmer`)
share 8-gram Jaccard **0.17**, and the shared text is boilerplate CTA/nav inside `<main>`. Pairs
sharing one tool score 0.5–0.65, which is expected when half the subject is identical. Median
main-text length 11,900 chars. No duplicate-content finding to report.

## Actionable observations

1. **Pull the free signal this week: Search Console, not Plausible.** The verification meta tag
   has been live for ~12 weeks. A 28-day Search Console export gives impressions, queries and
   CTR for a 1187-URL site — the exact data needed to decide whether 600 comparison pages earn
   anything. This is a George-only step (the login/export); nothing on the site blocks it.
2. **Either paste the Cloudflare token at `js/analytics.js:63` or state that you are not
   measuring.** One 32-hex string buys pageviews, referrers, paths, countries and device class
   for $0. Seven blank weeks against 1416 published pages is long past "temporary".
3. **Volume has now outrun the bottleneck you already named.** Your own rule was: after ~600
   pages, run distribution instead of adding volume until data picks winners. The site is at
   **1416 pages / 600 comparisons**, and the last measured window (week ending 2026-09-21) had
   **~12 organic visitors/month** — with 130 new comparison pages added this week alone, driven
   by 9 new tool submissions (≈14 comparison pages each). Vendor intake is now a
   page-count multiplier; without a measurement floor, intake volume is the only lever being
   pulled.

## Standing (historical, NOT current)

Week ending 2026-09-21: 18 visitors / 36 pageviews, 83% bounce, avg visit 74s.
30d to 2026-09-21: 95 visitors / 283 pageviews, 62% bounce, avg visit 124s.
~93 of those 95 were Direct/bot traffic; ~12 were organic search. Do not read these as this
week: the site has gone from 740 to 1416 tracked HTML pages (+676) since that window closed,
so a trend line across the gap would be measuring a different site.
