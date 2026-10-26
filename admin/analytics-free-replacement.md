# Free replacement for Plausible (site analytics)

Written 2026-10-21. Plausible has been unusable since its API began returning **HTTP 402 — "locked
due to missing active subscription"**. The tracking script is still on **996 pages**, so every visit
currently fires a request to an account that cannot read the result. That is roughly three weeks of
traffic lost, on a site whose whole editorial argument is that dated, verifiable evidence beats
vibes.

Plausible has no free tier (30-day trial only), so it is not a candidate for a zero-cost fix.

## Verified options

Every figure below was read from the vendor's own page on 2026-10-21, not from memory. Free tiers
change often; re-check before relying on one.

| Service | Free tier | Cookies | Needs an account | Notes |
|---|---|---|---|---|
| **Cloudflare Web Analytics** | Unlimited, free forever ("For free") | None | Yes (free Cloudflare account) | Works **without** moving DNS — see below |
| **Umami Cloud (Hobby)** | $0/mo — 100K events/mo, 1 website, **6-month retention** | None | Yes | Open source, self-hostable if we ever want to own it |
| **Counter.dev** | Free, "for everyone" | None | Yes | Small independent project; thin docs, no SLA |
| **GoatCounter** | Free for non-commercial; paid for commercial use | None | Yes | **Commercial use is not free** — this site is commercial |
| **Google Analytics 4** | Free | Yes — needs a consent banner | Yes | Rejected: a consent banner and a Google tag contradict our published standard |
| **Matomo** | Free only if self-hosted | None | Yes (+ a server) | Needs a host we do not have; GitHub Pages cannot run it |
| **Plausible CE** | Free self-hosted | None | Yes (+ a server) | Same hosting problem |

## Recommendation: Cloudflare Web Analytics

It is the only option that is unlimited, free forever, cookieless, and installable on this exact
stack. The important detail, which had to be verified rather than assumed, is **whether it works
without proxying the domain through Cloudflare** — our DNS is on Porkbun and the site is on GitHub
Pages, so moving DNS is not a one-line change.

It does work. The beacon script posts to:

```
https://cloudflareinsights.com/cdn-cgi/rum
```

That is an absolutely addressed Cloudflare host — **not** `/cdn-cgi/rum` on our own domain, which is
what would only exist behind their proxy. Confirmed by reading the served `beacon.min.js` (31,853
bytes, HTTP 200) and extracting the endpoint from it. Cloudflare's own get-started flow is "Add a
site → set up hostname → copy the JS snippet", and their FAQ covers adding it to a DNS-only
(non-proxied) domain.

What it gives up versus Plausible: **no custom conversion events**. Cloudflare's free tier reports
page views, referrers, top paths, countries, and device class. It will not replace our
`conversion_pricing` / `conversion_premium` goals. That is why the Plausible loader is left in place
rather than deleted — if the subscription is ever paid for, the goal tracking starts working again
with no code change.

## What is already done (code side)

`js/analytics.js` now carries a Cloudflare Web Analytics loader:

```js
var CF_WA = { token: '', version: '2024.11.0' };
```

**An empty token means disabled — no script tag, no third-party request, nothing to disclose.** The
live site behaves exactly as it does today until the token is filled in. It is gated on the
production hostname like everything else, so localhost and previews never report.

`legal/privacy.html` has been updated in the same pass so the analytics section is already accurate
when it switches on: it names both providers, describes the conversion goals, and states plainly
that no advertising, remarketing or session-replay script runs here. Adding a tracker while
criticising vendors for unnamed beacons would be indefensible, so the disclosure ships first.

## Activating it — three minutes, and it needs the operator

Only the account holder can do this; it is a third-party signup.

1. Create a free account at `dash.cloudflare.com`. **No DNS change and no card required.**
2. **Web Analytics → Add a site.** Enter hostname `aitoolsessentials.com`.
3. Cloudflare shows the JS snippet. Copy **only the `token` value** from it — the 32-character hex
   string inside `data-cf-beacon`.
4. Paste it into `CF_WA.token` in `js/analytics.js`, replacing the empty `''`.
5. Run the pipeline, validate, push. Within a minute or two the dashboard shows live page views.

Sanity check after activation: load the site, open devtools, and confirm one request to
`static.cloudflareinsights.com/beacon.min.js` and one POST to `cloudflareinsights.com/cdn-cgi/rum`.
If both appear and the dashboard stays empty, check the token — a wrong token fails silently.

## If the token never arrives

Nothing breaks — the site simply keeps reporting nothing, as it does today. Worth knowing for the
traffic reports: the current zero is **unavailable data, not zero traffic**, and no report should
present it as a measured decline. That distinction is already recorded in
`references/plausible-analytics-and-deploy-reads.md`.

## Second free signal already available, needs no code

**Google Search Console** reports impressions, clicks, CTR, average position and the queries driving
them, at no cost and with no script. It is the only free source for what people search before they
arrive. It does not measure on-site behaviour, so it complements a page-view tool rather than
replacing one — and if verification was never completed, that is the single highest-value free
data source still unused.
