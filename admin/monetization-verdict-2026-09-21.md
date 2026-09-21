# Can AIToolsEssentials ever make money — or should it be pivoted?

Written 2026-09-21 from the Search Console export (2026-08-22 → 2026-09-19),
Plausible (30d), the affiliate registry, and the repo itself. No projections
without a stated source.

## The honest headline

**No, not as a generalist "best AI tools" directory. Yes, as a narrow
pricing/monitoring product — and the pivot is a narrowing, not a restart.**

The domain is one month old (registered 2026-08-21, first GSC impression
2026-08-23). Everything below has to be read against that. But two facts are
already decisive and will not change much with age:

1. The site has **740 pages for ~3,300 impressions/month** of visible query
   demand — 4.4 impressions per page per month, 0.15/day. At a generous 0.5%
   CTR that is one click per ~330 days per page.
2. **No affiliate click has ever been recorded** (Plausible, all time), and only
   **2.6% of visits land on a page carrying a monetised link.**

## Why the generalist directory is the wrong shape

For our single best near-miss query — "best ai tools for agencies", 260
impressions at position 29.61 — every result on page one is a single-topic
specialist domain (aipedia.wiki, agencypro.app, cartabyte.com, storyflow.so).
Same for "best ai assistant". A 76-tool generalist with a one-month-old domain
does not rank for either, regardless of on-page depth.

Confirmed internally: controlling for page type (only `/articles/` buyer
guides, n=91), the correlation between word count and position is **+0.089** —
none. Bucketed by depth, the *deepest* pages have the *worst* median position:

| words | n | median position |
|---|---|---|
| <600 | 66 | 54.5 |
| 600–1200 | 16 | 53.0 |
| 1200+ | 9 | 55.9 |

Every page deepened in earlier passes sits at position 34–56. Depth is not the
lever. (Those blocks landed 09-12..09-19 against an export ending 09-19, so read
this as "no positive signal", not "disproven".)

## The one thing the data says works

Split the pages by whether they carry **data we generate and maintain** versus
**commodity listicles any competitor can write**:

| class | pages | impressions | CTR | median position |
|---|---|---|---|---|
| proprietary (pricing/change data) | 9 | 165 | **0.61%** | **10.1** |
| generic (listicles, comparisons) | 203 | 4,452 | 0.07% | 24.1 |

The proprietary pages rank more than twice as well and convert at roughly
**9x the CTR**. `/pricing-watch/` sits at position 6.13; `/change-radar/` at
10.10 with a 2.08% CTR — the best on the site.

This is the defensible asset. A vendor cannot publish "here is how my price
changed and when we checked it" about itself — the *checked date* is the
artifact. It is also the only content type that does not compete head-on with
established specialist domains.

## What the numbers say about scale (be blunt)

Affiliate economics at our verified rates (ElevenLabs 22%, Make 35%, Gamma 25%,
Sonaopus one-time, Nous $15) blend to roughly **$3–14 per referral**, mostly
small recurring:

| visitors/mo | affiliate clicks (2%) | signups (8.4%) | monthly |
|---|---|---|---|
| 66 (today) | 1 | 0.1 | ~$0.33 |
| 6,600 | 132 | 11 | ~$33 |
| 66,000 | 1,320 | 111 | ~$333 |

To reach **$100/month** needs roughly 24,000 visitors/month — **~360x today**.
At one month old with 189 impressions/day, that is not a matter of effort; it is
a matter of years, and only if the content shape is right.

Also note the affiliate surface itself is thin: of 76 tracked tools, **9 have a
known program and only 4 are approved and wired**. ChatGPT, Claude, Gemini,
Zapier, Notion, Canva and Perplexity — the tools people actually search for —
have no publisher program at all.

## Recommendation: narrow, do not restart

The site has real assets that a fresh project would have to rebuild: 76 reviewed
tools, verified pricing snapshots with checked dates, a change log, 740
validated pages, generation that is idempotent in CI, and live affiliate
relationships (Gamma, ElevenLabs, Make, Sonaopus, Nous).

Recommendation, in order:

1. **Stop producing new generic listicles.** 740 pages is far past the point
   where more volume helps. This is the single biggest change.
2. **Reposition the site around verified pricing and price-change tracking** —
   the one class with evidence of ranking. Deepen `/pricing-watch/`,
   `/change-radar/`, per-tool pricing pages.
3. **Fix the monetisation density.** Only 10 of 740 pages carry an affiliate
   link. The high-traffic guides naming an approved tool should carry one.
4. **Do not add AdSense, and do not push Premium.** At 66 visitors both are
   noise; Premium at $12/mo needs volume that does not exist yet.
5. **Keep building the moat that is hard to copy** — checked dates, change
   history, and the discipline of never re-dating unverified data.

A pivot to a *new* site would throw away the only thing that is working. A
narrowing to the pricing/product-data thesis is a real, evidence-backed move.

## Caveats to keep attached to this

- 29 days of history. Nothing here is a settled trend.
- `best ai tools for agencies` (260 impressions) alone is 8% of all visible
  demand; conclusions resting on it are fragile.
- 44% of our position-≤10 impressions come from operator/scraper queries
  (`-site:`, `intitle:` strings), not buyers.
- 24 of 76 pricing snapshots are client-rendered and unreadable by CLI, so
  price freshness coverage is partial.

## What changed on the site as a result (2026-09-21)

- Consolidated 8 duplicate-intent pairs → **0 duplicate titles** sitewide
  (was 7). Stubs canonical to the `/articles/` guide, `noindex`, out of sitemap.
- Fixed **12 affiliate links across 6 pages** mislabeled
  `rel="external nofollow"` instead of `rel="sponsored"` — an FTC/Google
  misdeclaration on the site's highest-traffic buyer guides.
- Closed the validator escape hatch that let those links pass: the outbound-CTA
  rule skipped anything containing `external`, so commission links were exempt
  from the exact check written to catch them. Proven to fail before, pass after.
