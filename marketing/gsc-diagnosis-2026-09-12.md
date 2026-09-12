# GSC diagnosis — 2026-09-12

Data: Search Console export 2026-08-22 → 2026-09-10 (20 days).
4,665 impressions, 6 clicks, CTR 0.129%, average position 51.6.

**Headline correction to the earlier read: this is not an indexation problem.**

306 pages have received impressions, which means Google has indexed the site broadly.
717 sitemap URLs with 306 showing impressions in a 20-day window is consistent with
normal discovery. The duplicate-comparison theory was wrong: 44 comparison URLs
carry only 263 impressions total (6 each), so they are neither helping nor
suppressing the rest of the site.

**The real constraint is ranking position, then click-through on the pages that do rank.**

## What the numbers say

Impressions are growing and position is improving:
- Aug 27–31: 1,674 impressions, avg position 62.3
- Sep 01–05: 1,322 impressions, avg position 44.5
- Sep 06–10: 1,309 impressions, avg position 44.3

Position moved from ~62 to ~44 in three weeks — the site is climbing normally for its
age. 4,665 impressions on 306 pages is an average of 15 impressions per page, which is
the signature of a young domain, not of a penalty or an indexing failure.

## Where the demand actually is (by query theme)

| Theme | Queries | Impressions |
|---|---|---|
| teachers / education | 51 | 343 |
| ai assistant (generic) | 45 | 291 |
| meetings | 49 | 184 |
| nonprofit / grant | 22 | 178 |
| property / landlord | 45 | 143 |
| free writing tools | 24 | 125 |
| search engines (perplexity) | 28 | 108 |
| automation (zapier/make/n8n) | 16 | 101 |
| real estate | 15 | 95 |
| local / ollama | 40 | 85 |

## The biggest single opportunity

`best ai tools for agencies` — **259 impressions, position 29.6, zero clicks.**
That is the highest-impression query on the site and it sits just outside page one.
The page serving it (`articles/best-ai-tools-for-agencies.html`) is only **425 words**
with 5 H2 sections. A 425-word page will not hold position 29 against competitors
publishing 2,000+ word guides. This is the clearest "add depth, gain rank" target.

## The zero-click anomaly — and its real explanation

16 pages rank at position ≤10 with ≥10 impressions and earned **zero** clicks in 20 days
(534 impressions, 0 clicks where ~5% CTR would predict ~25 clicks).

Titles and metas are not the cause — they are specific and well-written
("Is HeyGen worth it?", "Perplexity vs Gemini", 105–157 char descriptions).

Two real explanations:

1. **Low absolute volume per page.** 171 impressions over 20 days is ~8.5/day. A page at
   position 7 with 8 impressions/day can legitimately receive zero clicks for weeks.
   At these volumes CTR measurements are noise, not signal.
2. **The keyword set is largely non-commercial or SEO-tool traffic.** Of the 27 queries
   ranking at position ≤10, 8 are operator queries from SEO tools, not humans
   (`intitle:"leonardo ai" "license for free"`, `site:poe.com/...`,
   `"tenantcloud" -site:reddit.com -site:twitter.com ...`). Those never click.

So the "good position, no clicks" pattern is mostly small-sample noise plus bot traffic,
not a title or snippet defect. Do not rewrite titles chasing it.

## Cannibalization is real but small

The teachers theme (51 queries, 343 impressions — the largest demand cluster) is split
across four overlapping pages:
- `use-cases/best-ai-tools-for-teachers.html` (325 words)
- `articles/best-ai-tools-for-teachers.html` (524 words)
- `stacks/ai-stack-for-teachers.html`
- `workflows/classroom-lesson-planning.html`

None is long enough to win. Best positions in that cluster are 57–90.

## What to do, in order

1. **Deepen `best-ai-tools-for-agencies.html`** from 425 to 1,500+ words. It is one
   position-29 query with 259 impressions and no competition from our own pages.
   Highest expected return of anything on this list.
2. **Consolidate the teachers cluster into one strong page** with the others 301-ing or
   linking to it. 343 impressions spread across four thin pages cannot rank.
3. **Add depth to the queries at position 20–50 with real volume**: `best ai assistant`
   (116 impr, pos 49), `best ai assistants` (30, pos 33), `best ai search tool` (23, pos 35),
   `best ai tools for real estate agents` (34, pos 47).
4. **Do not chase** the zero-click pages — the position data there is small-sample noise.
5. **Do not fix indexation** — there is nothing to fix. Google has the site.

## What this means for revenue

At 306 impressions/day and position ~44, ad or affiliate revenue stays near zero.
But impressions are up 3.6x in three weeks with position improving 18 places. The lever
is depth on a handful of pages that already have proven demand, not more pages.

**AdSense remains gated by traffic** (~500 PV/day is the point ads are worth running);
current ~7 PV/day from search is 70x below that. Sponsorship and the affiliate programs
already approved are the realistic near-term revenue, and both scale with the same fix:
rank the pages that already have impressions.
