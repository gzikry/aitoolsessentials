# Weekly traffic report — 2026-11-23

## Headline: the failure mode changed — the Plausible key is now rejected outright

**Every Plausible metric is blank. Blank is not zero — the data is unavailable.**
No figure below is estimated, ranged, or carried forward as current.

Both wrapper runs failed against the Plausible **v2** API (`/api/v2/query` only):

```
python3 scripts/plausible_report.py --period 30d   → exit 3
python3 scripts/plausible_report.py --period 7d    → exit 3

Plausible API returned an error — no metrics can be reported.
Reason: Invalid API key or site ID. Please make sure you're using a valid API key
with access to the site you've requested.
Do NOT record this as zero traffic; the data is unavailable.
```

### What is new versus last week

For seven consecutive weeks (2026-09-28 → 2026-11-16) the same wrapper failed with a
**site-level subscription lock**:

> *"This Plausible site is locked due to missing active subscription…"*

That message only appears *after* a key authenticates. This week the API instead returns
**HTTP 401 "Invalid API key or site ID"** — the unauthenticated response. The failure has
moved from the billing side to the credential side.

### Credential diagnosis (v2 only; the token value was never printed)

| Probe | HTTP | Response |
|---|---|---|
| Wrapper, `--period 30d` | 401 | `Invalid API key or site ID…` |
| Wrapper, `--period 7d` | 401 | `Invalid API key or site ID…` |
| Raw v2, `site_id=aitoolsessentials.com` | 401 | `Invalid API key or site ID…` |
| Raw v2, `site_id=www.aitoolsessentials.com` | 401 | `Invalid API key or site ID…` |
| Raw v2, **deliberately garbage key** | 401 | `Invalid API key or site ID…` *(identical)* |
| Raw v2, **no Authorization header** | 401 | `Missing API key…` *(different — header is being sent correctly)* |

Two facts follow, and no more than two:

1. The wrapper is sending the credential. With no header the API explicitly says
   *"Missing API key"*; with any key (ours or a garbage string) it says *"Invalid API key
   or site ID."* So the request is well-formed and the key is genuinely being **rejected**.
2. A revoked/rotated key and a wrong key are **indistinguishable** from outside — both
   return the exact same 401. I cannot tell *why* it is rejected, only *that* it is.

Token file is present and unchanged: `~/.hermes/profiles/aitools/plausible_token`, mode
`600`, 65 bytes, mtime **2026-08-25 13:40** (same as every prior report). The file did not
change — the site's acceptance of it did.

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

## Site state (independently verifiable, checked this run)

| | 2026-11-16 | 2026-11-23 | Δ |
|---|---|---|---|
| Tracked HTML pages | 1416 | **1829** | +413 |
| Sitemap URLs | 1187 | **1580** | +393 |
| Comparison pages | 600 | **1034** | +434 |
| Google verification meta tag | live | **live** | unchanged |

Live checks (2026-11-23): `/` **200** · `/stack-audit.html` **200** · `/sitemap.xml` **200** ·
`/js/analytics.js` **200**. The `google-site-verification` meta tag is still served in
production (`content="OzzGs2QF4v6zSBd9uO95NGgSPH5B598E6DPtcjRNn_4"`).

Publishing accelerated: **+413 pages in seven days** (vs +150 the week before), of which
**+434 are comparison pages** — the site is now majority comparison content (1034 of 1829
HTML pages).

## Actionable observations

1. **Re-issue the Plausible key — this is now a one-line fix, not a billing decision.**
   Through last week the block was a missing subscription (George's call). This week the
   API rejects the key itself with a 401, which is what you get from a **rotated or revoked
   API key**. If the subscription was cancelled or the workspace changed, the key was
   invalidated as a side effect. Action: in Plausible, confirm the site still exists under
   the account, then issue a fresh API key and drop it in
   `~/.hermes/profiles/aitools/plausible_token`. Until that happens no Plausible number can
   exist, and this report stays blank by design.
2. **The zero-cost path is still one empty string away** — and it is now the only path that
   does not depend on Plausible at all. `js/analytics.js:63` still reads
   `var CF_WA = { token: '', version: '2024.11.0' };`. An empty token disables the beacon by
   design. Meanwhile the Plausible loader on line 11 still fires from every one of the
   **1829** tracked pages into an account that no longer accepts our key — one third-party
   request per visitor that stores nothing anywhere. Either paste a Cloudflare Web Analytics
   token into line 63 or state plainly that the site is not being measured.
3. **Volume is still the only lever being pulled, and the measurement floor is now zero.**
   Your own rule: after ~600 pages, run distribution instead of adding more volume until
   data picks winners. The site went from 600 → **1034** comparison pages in the last two
   weeks alone, with **zero** working analytics. The last window that ever produced a
   number (week ending 2026-09-21) had ~12 organic visitors/month. Adding 400+ pages a week
   to an unmeasured site is not a growth strategy; it is intake throughput. Search Console
   remains the one free source that does not touch Plausible — the verification tag has
   been live since 2026-08-22, so only the **export/login** is outstanding (George-only).

## Standing (historical, NOT current)

Week ending 2026-09-21: 18 visitors / 36 pageviews, 83% bounce, avg visit 74s.
30d to 2026-09-21: 95 visitors / 283 pageviews, 62% bounce, avg visit 124s.
~93 of those 95 were Direct/bot traffic; ~12 were organic search. Do not read these as this
week: the site has grown from 740 to 1829 tracked HTML pages since that window closed, so a
trend line across the gap would be measuring a different site.
