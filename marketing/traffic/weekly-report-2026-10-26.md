# Weekly traffic report — 2026-10-26

## Headline: fifth consecutive week with no measurable traffic — but the one free lever is now verified closed

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
`~/.hermes/profiles/aitools/plausible_token` (never printed; mode 600, mtime unchanged
at 2026-08-25 13:40).

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

**1. The 404 lever is closed and verified live.** PR #38 (`cf0689c1c`, 2026-10-17) added
redirect stubs for the 59 public URLs that had gone 404 plus the 3 sitemap-only paths.
This week I tested all **63** mappings against production, source and destination:

- 63/63 redirect sources return **HTTP 200**
- 63/63 destinations return **HTTP 200**
- 10 of the paths contain spaces or `&` (`Audio Production`, `Music & Audio`, `Video & 3D`);
  all resolve when percent-encoded, so the earlier "000" results were my test not encoding
  the URL, not a site fault
- **0** redirect stubs appear in `sitemap.xml`

Mechanism, stated precisely: these are 200-status meta-refresh stubs with a self-targeting
canonical to the keeper and `robots: noindex,follow`. GitHub Pages cannot serve a real 301
for an arbitrary path, so a soft redirect is the ceiling here. That is enough to stop the
404s scoring against the site, but it is not a 301 and I am not claiming the indexed-page
count will jump back.

**2. Publishing did not stop while measurement did.** The site grew again:

| | 2026-10-19 | 2026-10-26 |
|---|---|---|
| HTML files referencing `/js/analytics.js` | 834 | **990** |
| Sitemap URLs | 747 (10-17) | **908** |
| Public HTML files on disk | — | 1006 |
| Meta-refresh stubs (excluded from sitemap) | — | 87 |

That is 156 more tracked pages and 161 more sitemap URLs in one week, with collection off.
Each one is being published into a blind spot.

**3. Live-site sanity checks** (2026-10-26): `/` 200, `/js/analytics.js` 200,
`/stack-audit.html` 200. The loader still targets `https://plausible.io/js/script.js`, so
the tag is correctly installed and will resume counting the moment the plan is active.

## Actionable observations

1. **The analytics decision is now five weeks old and is the only thing standing between
   this report and a real number.** It is a payment or an account creation, both of which
   are yours. Two viable paths: Plausible Starter ≈ $9/mo (no code change, this wrapper
   starts returning data again the same day), or GA4 at $0 (needs a property and a snippet
   swap, then the wrapper is replaced). The third option — stay dark — is what the last
   five reports have been.
2. **Read the next Search Console coverage report before drawing any conclusion from the
   redirects.** The redirects landed 2026-10-17; Google needs a recrawl cycle to retire the
   208 "Not found" rows. I cannot see GSC from here, so this is unverified on my side and I
   am not going to imply otherwise.
3. **When numbers return, treat that week as a new baseline, not a continuation.** The last
   reportable datum is the week ending 2026-09-21, and the site has added roughly 250 pages
   since. A trend line drawn across the gap would be measuring a different site.

## Standing (historical, NOT current)

Week ending 2026-09-21: 18 visitors / 36 pageviews, 83% bounce, avg visit 74s.
30d to 2026-09-21: 95 visitors / 283 pageviews, 62% bounce, avg visit 124s.
~93 of those 95 were Direct/bot traffic; ~12 were organic search. Do not read these as this week.
