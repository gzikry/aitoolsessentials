# Weekly Traffic Report — AIToolsEssentials

**Week of:** 2026-09-14 → 2026-09-20 (Mon–Sun, complete)
**Report date:** 2026-09-21
**Site:** https://aitoolsessentials.com
**Analytics:** Plausible **v2** API only (`/api/v2/query`) via `scripts/plausible_report.py`, token at `~/.hermes/profiles/aitools/plausible_token`. No v1 calls, no estimates, no hand-rolled queries.

> **Two structural facts to read everything below against.**
>
> **1. "30d" is this site's entire measurable history.** The 30-day window reads **95 visitors / 283 pageviews**, and all-time reads **96 / 284**. Plausible recording for this domain begins **2026-08-23** (confirmed: 2026-08-22 returns 0, 2026-08-23 returns 3). There is no pre-analytics baseline to compare a 30-day trend against, and 30-day figures are not a smoothed view — they are the whole dataset.
>
> **2. This is the first week measured with complete page coverage.** The 2026-09-14 report documented that 53 public pages served no analytics loader and shipped the fix (commit `60dfa418`). Verified this week two ways: `validate_site.py` passes with 732 public HTML pages and 0 missing loaders, and a tree-level check of the 2026-09-19 and 2026-09-20 commits found **0 of 732 public HTML files** lacking `js/analytics.js`. The step-up the prior report warned about **did not happen** — see §5.

---

## 1. Headline

| Metric | This week (Sep 14–20) | Prior week (Sep 7–13) | Change |
|---|---|---|---|
| Visitors | **18** | 28 | **−36%** |
| Pageviews | **36** | 81 | **−56%** |
| Visits (sessions) | 18 | 34 | −47% |
| Pages / visit | 2.00 | 2.38 | −16% |
| Bounce rate | **83%** | 68% | +15 pts |
| Avg. visit duration | **74 s** | 147 s | −50% |
| Non-pageview events | 9 (1 excluding one session — §4) | 3 | — |
| 30-day visitors / pageviews | **95 / 283** | 81 / 252 (08-15→09-14) | +17% / +12% |

Script output, trailing 7d: **18 visitors, 36 pageviews, 83% bounce, avg visit 74s.**
Script output, 30d: **95 visitors, 283 pageviews, 62% bounce, avg visit 124s.**

Full script output for both periods is reproduced verbatim in §8.

### The three-week series (complete Mon–Sun weeks)

| Week | Visitors | Pageviews | Visits | Bounce | Avg duration |
|---|---|---|---|---|---|
| W36 · Aug 31 – Sep 6 | 26 | 85 | 36 | 50% | 101 s |
| W37 · Sep 7 – 13 | 28 | 81 | 34 | 68% | 147 s |
| **W38 · Sep 14 – 20** | **18** | **36** | **18** | **83%** | **74 s** |

Volume, depth, and duration all fell in the same week. Bounce at 83% with a 74-second average is not a marginal move: 15 of 18 sessions this week viewed exactly one page and triggered no event.

Per the metrics definitions, Plausible counts a session as a bounce unless the visitor views a second page **or** triggers a custom event. So the bounce rate and the event count are two views of the same fact — this week very little of anything happened after the first pageview. Duration corroborates it (74s, down from 147s); the two readings agree, so this is a real depth loss, not a bounce-rate artifact.

### Reconciliation with last week's report

The 2026-09-14 report reported **26 visitors / 69 pageviews** for Sep 8–14. Re-queried today, that same window reads **29 / 73**. The difference is exactly **3 visitors and 4 pageviews**, and Sep 14 itself totalled 4 visitors / 5 pageviews — consistent with that report's query having run while Sep 14 was still in progress, counting 1 of its 4 visitors. The last day of any report generated mid-day is provisional; use complete Mon–Sun weeks for comparison, which is what the table above does.

---

## 2. Sources

### This week (Sep 14–20)

| Source | Visitors | Pageviews | Bounce | Avg duration |
|---|---|---|---|---|
| Direct / None | **10** | 11 | 90% | 1 s |
| Perplexity | **4** | 9 | 75% | 295 s |
| ChatGPT | 2 | 2 | 100% | 0 s |
| Google | 2 | 14 | 50% | 66 s |

### Prior week (Sep 7–13)

| Source | Visitors | Pageviews |
|---|---|---|
| Direct / None | 19 | 63 |
| Google | 8 | 17 |
| Perplexity | 1 | 1 |

### Last 30 days (Aug 22 – Sep 20)

| Source | Visitors | Pageviews |
|---|---|---|
| Direct / None | **73** | 234 |
| Google | 12 | 34 |
| Perplexity | 5 | 13 |
| ChatGPT | 3 | 3 |
| 247team.ai.studio | 1 | 1 |
| impactcommunityservices.sharepoint.com | 1 | 1 |

Channel view, same numbers grouped: Direct 73v/234pv · Organic Search 12v/34pv · **AI Assistants 8v/13pv** · Referral 2v/2pv.

### Reading the sources honestly

**Google did not "arrive" last week — it was a spike that did not repeat.** Last week's report called Google's 6 visitors "the single most important number here". This week Google sent **2 visitors, and one of those two is the 13-pageview session in §4 from Pakistan**. Google's real contribution this week is **1 visitor / 1 pageview**. Across the whole 30-day window Google has sent 12 visitors, and its best days were Sep 7–9 and Sep 12–13. Google's per-day entries are single visitors trickling into `articles/`, `guides/switch-guides/`, `pricing-watch/` and `submit-tool.html` — no page is accumulating search entry.

**AI assistants are now the more reliable non-direct source.** Perplexity + ChatGPT sent **6 visitors this week against Google's 2** (and against 1 combined last week). All 8 AI-assistant visitors in the 30-day window arrived on either a tool review page or a comparison page, and 6 of the 8 arrived this week:

| Date | Entry page | Source |
|---|---|---|
| Sep 1 | `/articles/best-ai-productivity-tools.html` | ChatGPT |
| Sep 10 | `/tools/leonardo-ai/` | ChatGPT |
| Sep 14 | `/tools/perplexity/` | Perplexity |
| Sep 15 | `/tools/fireflies/` | Perplexity |
| Sep 16 | `/tools/perplexity/` | Perplexity |
| Sep 16 | `/articles/notion-ai-vs-microsoft-copilot-deep-comparison.html` | ChatGPT |
| Sep 17 | `/tools/perplexity/` | Perplexity |
| Sep 18 | `/tools/catch-ai/` | ChatGPT |

That is a coherent pattern, not noise: **single-tool review pages are what AI assistants cite and send people to.** `/tools/perplexity/` is the clearest case — 3 entry visitors this week, 67% bounce, **394-second average visit duration**, and it is the only page on the site where a single session reached 1,181 seconds (Sep 17). Nothing else on the site engages at that level.

**Direct / None is still the top "source" and is still not a source.** It remains suspicious by the standard set last week: 73 of 95 visitors, on a domain with no brand recognition. What changed is its character. Last week Direct produced 63 pageviews from 19 visitors (3.3 pages each) — the signature of internal browsing. This week it produced **11 pageviews from 10 visitors (1.1 pages each)** with 90% bounce. Direct is no longer "us clicking around the site".

Where this week's Direct sessions landed is the tell: eight entries, one visitor each, and most of them on deep comparison pages that no one navigates to as a home page —

`/comparisons/canva-ai-vs-leonardo-ai.html` (2), `/stack-builder.html`, `/comparisons/notion-ai-vs-slack-ai.html`, `/xai-bot-guides/designing-grok-bot-with-grok-bot/`, `/guides/switch-guides/switch-from-jasper-to-copy-ai.html`, `/comparisons/ideogram-vs-leonardo-ai.html`, `/comparisons/grammarly-vs-microsoft-copilot.html`, `/` (2).

Deep comparison pages + no referrer + single pageview is what a click from an AI answer or a pasted link looks like once the referrer is stripped (two of these arrived on Yandex Browser). **Treat Direct / None as a mixed bucket — some of it is almost certainly AI-assistant referral that Plausible could not attribute — and do not count it as an acquisition win.** It fell 9 visitors and 52 pageviews week-over-week, and the 30-day figure is not growth.

**Zero traffic from a directory, an email campaign, or social.** Every visitor in the 30-day window has `utm_campaign = (not set)`; only three tagged visits exist at all (`utm_source=chatgpt.com` 3, `utm_source=perplexity` 3). No directory referral has ever appeared in the data.

---

## 3. Top pages

### This week (Sep 14–20)

| Page | Visitors | Pageviews |
|---|---|---|
| `/` | 4 | 7 |
| `/tools/perplexity/` | 3 | 3 |
| `/premium/` | 2 | 4 |
| `/comparisons/canva-ai-vs-leonardo-ai.html` | 2 | 2 |
| `/newsletter/` | 1 | 1 |
| `/tools/catch-ai/` | 1 | 1 |
| `/stack-audit.html` | 1 | 2 |
| `/tools/fireflies/` | 1 | 1 |
| `/tools/landlord-studio/` | 1 | 1 |
| `/premium/library/` | 1 | 1 |

### Last 30 days (Aug 22 – Sep 20)

| Page | Visitors | Pageviews | Visits | Bounce | Avg duration |
|---|---|---|---|---|---|
| `/` | **47** | 79 | 52 | 47% | 128 s |
| `/premium/` | 10 | 13 | 10 | 100% | 0 s |
| `/stack-audit.html` | 10 | 11 | 10 | 60% | 35 s |
| `/tools/index.html` | 8 | 9 | 8 | 50% | 54 s |
| `/submit-tool.html` | 7 | 19 | 9 | 50% | 167 s |
| `/pricing/` | 6 | 9 | 7 | 100% | 0 s |
| `/stack-builder.html` | 6 | 8 | 6 | 100% | 0 s |
| `/tools/sonaopus/` | 4 | 9 | 5 | 80% | 460 s |
| `/index.html` | 4 | 8 | 5 | 0% | 0 s |
| `/services/intake-questionnaire.html` | 3 | 5 | 4 | 0% | 750 s |
| `/legal/privacy.html` | 3 | 4 | 3 | 0% | 0 s |
| `/pricing-watch/` | 3 | 3 | 3 | 0% | 96 s |

**Note on the bounce/duration columns.** In a Top Pages breakdown those are *session* metrics, attributed to where a session started, not to the page itself. `/premium/`, `/pricing/` and `/stack-builder.html` all read 100% / 0 s for the same structural reason: 9 of `/premium/`'s 10 visitors arrived by internal navigation, so the session's real engagement belongs to the entry page. Read page quality off `visit:entry_page` instead:

| Entry page (30d) | Visitors | Bounce | Avg duration |
|---|---|---|---|
| `/` | 42 | 47% | 128 s |
| `/submit-tool.html` | 6 | 50% | 167 s |
| `/stack-audit.html` | 5 | 60% | 35 s |
| `/tools/sonaopus/` | 4 | 80% | **460 s** |
| `/tools/perplexity/` | 3 | 67% | **394 s** |

**Two homepage paths, one page.** `/` (47v/79pv) and `/index.html` (4v/8pv) both serve the homepage and both carry `canonical → https://aitoolsessentials.com/`. Plausible logs the literal path, so the homepage's true 30-day figure is **51 of 95 visitors** — more than half the site's entire audience — not 47. Read them as one row.

**`/submit-tool.html` is a form being worked, not read.** 7 visitors produced 19 pageviews (2.7 each) with a 167-second average entry duration — the second-longest on the site. One submission was re-verified this week (Short.now, commit `44d405a1`, five items still live) and no new tool was published. 76 tools tracked.

**`/tools/sonaopus/` (460 s average) is vendor self-review traffic, not readership.** All four of its visitors were Nigerian and it drew 8 of the prior week's Nigerian visitors. See §4.

---

## 4. Conversion goals

### This week (Sep 14–20)

| Event | Events | Visitors |
|---|---|---|
| `conversion_premium` | **5** | 2 |
| `stack_audit_started` | 2 | 1 |
| `conversion_newsletter` | 1 | 1 |
| `conversion_stack_audit_entry` | 1 | 1 |
| **Total non-pageview** | **9** | |

### Prior week (Sep 7–13)

| Event | Events |
|---|---|
| `stack_audit_started` | 1 |
| `conversion_stack_builder_html` | 1 |
| `conversion_stack_audit_entry` | 1 |
| **Total non-pageview** | **3** |

### Last 30 days

`conversion_premium` 8 · `conversion_subscribe` 5 · `stack_audit_started` 4 · `conversion_newsletter` 3 · `conversion_pricing` 2 · `conversion_stack_audit_entry` 2 · then 1 each: `conversion_newsletter_2026_w35_html`, `conversion_compare_shortlist`, `stack_audit_cta`, `conversion_stack_builder_html`, `conversion_stack_builder`, `conversion_cost_calculator`, `stack_audit_completed`. **31 non-pageview events in 30 days.**

### Do not read 9 events as recovery — one session produced 8 of them

The week-over-week events table looks like the funnel tripled (3 → 9). It did not. Grouping the week's events by country:

| Country | Non-pageview events |
|---|---|
| **PK** | **8** |
| US | 1 |
| FR, GB, RU, IN, KR, IT | 0 |

A **single session on Sep 17 from Pakistan** — one visitor, **13 pageviews across 8 distinct pages**, 0% bounce, 131 s, Chrome on desktop, entering on `/stack-audit.html` from Google — fired **4 `conversion_premium`**, **2 `stack_audit_started`**, **1 `conversion_newsletter`** and **1 `conversion_stack_audit_entry`**. That is 8 of the week's 9 events, and 13 of its 36 pageviews: **36% of the week's pageviews and 89% of its conversion events from one session.**

Clicking a Premium link four times across four page loads, starting the audit twice, and clicking through to the newsletter in one 131-second visit is not how a reader behaves. These fields cannot prove it was automated, and I am not asserting that it was — but it is unattributed traffic that should not be counted as audience or as funnel improvement. **Excluding it, this week produced exactly one conversion event: a single `conversion_premium` from a US Direct visitor on `/`.**

So the honest week-over-week comparison is **1 real event vs 3 last week**, on 36% less traffic. Last week's report set an explicit trip-wire: *"if next week shows ≤3 non-pageview events on comparable traffic, instrument each funnel step individually."* Traffic is not comparable (down 36%), so the trigger is not met literally. But the substance of it is: **two consecutive weeks at ≤3 events on real traffic, and this week at 1.** The recommendation stands unchanged — see §6.

### The Stack Audit funnel

Script output, 30d: **10 visitors to `/stack-audit.html` → 4 started (40%) → 1 completed (10%).**
Script output, 7d: 1 visitor to the page, 2 started, 0 completed — the printed 200% start rate is an artifact worth naming, because it will recur: `started` is an event count (two page loads by the same visitor, `state.started` guards once per load) while "visitors to page" is visitor-deduplicated. **At n=1 a funnel rate can exceed 100% and means nothing.**

The real finding: **`stack_audit_completed` has fired once in 30 days, on 2026-09-04 — 17 days ago.** `stack_audit_started` fired on Sep 4, Sep 13, and Sep 17 (the PK session, twice). Ten visitors reached the page in 30 days and the audit has been completed once.

### The rest of the funnel has stopped converting entirely

| Event | Last fired | Gap |
|---|---|---|
| `conversion_subscribe` | **2026-09-04** | 17 days |
| `conversion_pricing` | **2026-09-03** | 18 days |
| `stack_audit_cta` | 2026-09-04 | 17 days |
| `conversion_cost_calculator` | 2026-09-04 | 17 days |
| `conversion_stack_builder` | 2026-09-03 | 18 days |
| `stack_audit_completed` | 2026-09-04 | 17 days |

`conversion_subscribe` has 5 events in the 30-day window and **none since Sep 4**, despite `/subscribe/` drawing 3 visitors and 4 pageviews in that window and `/newsletter/` drawing 3. People reach the newsletter pages and the subscribe link and the intent never records. That is either a broken path, an unattractive offer, or both — and it is the cheapest thing on this list to diagnose.

### Instrumentation gap, verified: outbound and affiliate clicks are not tracked at all

Last week's report asked whether outbound-link tracking works. **It does not exist.** Established by reading the code, not by inferring from the missing events:

- `js/analytics.js` loads `plausible.io/js/script.js` **without** the `outbound-links` extension, and its click handler explicitly returns `null` for any anchor carrying `data-outbound` (`isInternal()` line 31) — so vendor links can never produce an event.
- `js/tracking.js` (on 46 pages) does listen for `a[data-outbound="true"]` clicks, but it only increments a counter in the visitor's own `localStorage` and never calls `plausible()`. Nothing leaves the browser.

There are **31 pages carrying outbound anchors** and **327 links to the Whop checkout** across the site, plus live affiliate destinations (ElevenLabs, Make, Nous). None of those clicks is measurable. On a site whose entire revenue model is sending readers to vendor and checkout pages, the conversion that matters most is invisible. There are also no 404 events and no other custom events in the 30-day window.

(Incidental, same code path: `js/cookie-consent.js` renders an Accept/Decline banner whose copy says "essential cookies … and anonymous analytics (Plausible)", but the Decline button only writes a `localStorage` key — the analytics loader is injected on `load` regardless of the choice. Plausible sets no cookies, so this is not a tracking-law violation, but the banner implies a control it does not implement.)

---

## 5. What changed on the site, and why the numbers moved

**The coverage fix worked but added almost nothing.** The prior report predicted visitors and pageviews would rise for a reason that was not growth, because 53 previously uncounted pages became countable on 2026-09-14. Measured against the exact set of those 53 files (commit `60dfa418`): **they drew 2 visitors and 2 pageviews in the entire 30-day window — and only 1 visitor / 1 pageview this week** (`/xai-bot-guides/designing-grok-bot-with-grok-bot/`, a Direct entry with no referrer, one pageview, bounced). The step-up did not materialise because those pages get almost no traffic — which is itself the finding. The instrumentation was right to ship and the gap was real, but it was not hiding an audience.

**One correction to the prior report's framing of that gap.** Not all 53 URLs had "no analytics loader"; at least some **lost** it. The teachers guide — the page the prior report called "a hole in the data" on the strength of its 343 GSC impressions — carried the loader from 2026-08-26, lost it in a 2026-09-12 rewrite (`cba0d127`, which also dropped a duplicate page), and regained it on 2026-09-14. Its measured contribution over 30 days is **1 visitor / 1 pageview**, which is the honest size of the hole. The practical lesson is that a regeneration pass can silently strip instrumentation a page already had, so the `validate_site.py` guard added alongside the fix is the part that matters more than the backfill.

**Volume fell because the two largest contributors above were one-offs, both gone.**

| Driver | W37 (Sep 7–13) | W38 (Sep 14–20) | Change |
|---|---|---|---|
| Nigeria (`/tools/sonaopus/` vendor cluster) | 8 v / 35 pv | **0 v / 0 pv** | −8 v |
| United States | 15 v / 41 pv | 7 v / 8 pv | −8 v |
| Perplexity | 1 v / 1 pv | 4 v / 9 pv | +3 v |
| ChatGPT | 0 | 2 v / 2 pv | +2 v |
| Google | 8 v / 17 pv | 2 v / 14 pv | −6 v |
| Pakistan | 0 | 1 v / 13 pv | +1 v |

Nigeria's collapse accounts for 8 of the 10 lost visitors. The Sonaopus vendor cluster (4 visitors, 9 pageviews, 9 comparison pages built around it) reviewed its own listing and left; the 35 Nigerian pageviews went with it. **The prior week's traffic was never as large as it read.** And the US fall from 41 pageviews to 8 is the other half: last week's US visitors browsed the site, this week's view one page and leave.

**Content volume this week:** 726 sitemap URLs · 740 HTML pages (732 public) · 76 tools tracked · 33 commits · 528 files changed · **2 new public pages** (`articles/ai-assisted-job-search-workflow.html`, `articles/monthly-ai-cost-review.html`).

---

## 6. Recommendations

Ordered by expected return against numbers in this report.

### 1. Instrument outbound and checkout clicks — the revenue event is currently unmeasurable

Verified in §4: no outbound event exists anywhere in the stack. Add `outbound-links` to the Plausible script URL (one-line change in `js/analytics.js`) and fire an explicit `plausible('checkout_whop')` on `a[data-whop-checkout]` clicks (present on `/premium/`, `/pricing/`, `/premium/library/`). Without it, every future report continues to describe traffic at a site whose only revenue action is invisible, and the 30-day `conversion_premium` count (8 events, 5 of them on internal links) is being mistaken for checkout intent.

### 2. Diagnose the subscribe path before touching acquisition again

`conversion_subscribe` last fired **2026-09-04**, 17 days ago, despite `/subscribe/` and `/newsletter/` drawing traffic in the same window. This is a bounded, cheap investigation: verify the subscribe CTA on `/newsletter/`, `/newsletter/2026-w35.html` and `/subscribe/` actually produces a recorded event, and check whether the goal name still matches what fires. Nothing else on this list is as cheap to fix or as costly to leave broken.

### 3. Write more single-tool reviews — that is where the AI assistants send people

Perplexity + ChatGPT sent 6 visitors this week against Google's 2, and **all 8 AI-assistant visitors in the 30-day window entered on a tool review or comparison page**. `/tools/perplexity/` is the best-engaging entry page on the site (394 s average, 67% bounce, one 1,181-second session). This is the most concrete demand signal in the dataset and it points at a content type the site already has 76 of. Prioritise reviews of tools that AI assistants are actually asked about, and keep the per-page pricing/checked-date structure that makes them citable.

### 4. Stop treating the homepage's share as healthy

`/` + `/index.html` = **51 of 95 visitors (54%)** in 30 days, at 47% bounce and 128 s. The site has 732 public pages and half its audience enters on one page whose exit leads to a 100%-bounce `/premium/`. The comparison and tool pages do the engaging; the homepage does the arriving. Route more of the homepage's traffic into the two surfaces that hold attention.

### 5. Refresh the GSC export — the search picture is 11 days stale

`marketing/gsc-diagnosis-2026-09-12.md` covers 2026-08-22 → 2026-09-10 (4,665 impressions, 6 clicks, average position 44.3). Everything it concluded about ranking progress predates the Google fall in this report (8 → 2 visitors, 1 excluding the PK session). **George's lane** — a fresh export is needed to tell whether Google's decline is a ranking change or ordinary small-sample variance, and no Plausible query can answer that.

### 6. Keep reporting on complete Mon–Sun weeks only

This report's reconciliation in §1 shows why: the 2026-09-14 report read 26/69 for Sep 8–14 because its query ran before that day finished; the window reads 29/73 today. Use `2026-09-DD` → `2026-09-DD` arrays for whole weeks and reserve `7d`/`30d` for the headline figures.

### 7. Keep using v2, and keep the wrapper

`scripts/plausible_report.py` is v2-only (`/api/v2/query`) and correct. Do not hand-roll v1 calls: v1 disagrees with v2 on sources, pages, events, countries and browsers on identical dimensions, and has previously returned a phantom Safari browser, a phantom MU country, and Google 8 vs 6 visitors.

---

## 7. Summary metrics

| Metric | Value |
|---|---|
| Visitors (Sep 14–20) | **18** |
| Pageviews (Sep 14–20) | **36** |
| Visitors week-over-week | **−36%** |
| Pageviews week-over-week | **−56%** |
| Bounce rate (7d / 30d) | **83%** / 62% |
| Avg. visit duration (7d / 30d) | **74 s** / 124 s |
| 30-day visitors / pageviews | 95 / 283 |
| All-time visitors / pageviews | 96 / 284 |
| Recording began | 2026-08-23 |
| Real (non-direct) audience this week | 8 visitors (Perplexity 4, ChatGPT 2, Google 2) |
| AI-assistant visitors, 30d | 8 (6 of them this week) |
| Google visitors this week | 2 — **1 excluding the PK session** |
| Top page (30d) | `/` 47v/79pv · homepage total with `/index.html` **51v** |
| Non-pageview events this week | 9 — **1 excluding one Sep 17 session** |
| Stack audits started / completed (30d) | 4 / **1** (last completed 2026-09-04) |
| `conversion_subscribe` last fired | **2026-09-04** |
| Outbound / checkout click tracking | **does not exist** |
| Directory referrals, email, social | **0** |
| Pages missing analytics loader | **0** of 732 public pages |
| Traffic to the 53 newly-instrumented pages (30d) | **2 visitors / 2 pageviews** |
| Sitemap URLs / HTML pages | 726 / 740 |
| Tools tracked | 76 |
| New public pages this week | 2 |
| Commits this week | 33 |
| Beehiiv subscribers | **unknown** — unverifiable without a key; not carried forward as 0 |

---

## 8. Raw script output (verbatim)

### `python3 scripts/plausible_report.py --period 30d`

```
## Traffic (30d)

- Visitors: **95**
- Pageviews: **283**
- Bounce rate: 62% · avg visit 124s

### Top pages

- 47v / 79pv — `/`
- 10v / 13pv — `/premium/`
- 10v / 11pv — `/stack-audit.html`
- 8v / 9pv — `/tools/index.html`
- 7v / 19pv — `/submit-tool.html`
- 6v / 9pv — `/pricing/`
- 6v / 8pv — `/stack-builder.html`
- 4v / 9pv — `/tools/sonaopus/`
- 4v / 8pv — `/index.html`
- 3v / 5pv — `/services/intake-questionnaire.html`

### Sources

- 73v — Direct / None
- 12v — Google
- 5v — Perplexity
- 3v — ChatGPT
- 1v — 247team.ai.studio
- 1v — impactcommunityservices.sharepoint.com

### Conversion goals

- 8 — `conversion_premium`
- 5 — `conversion_subscribe`
- 4 — `stack_audit_started`
- 3 — `conversion_newsletter`
- 2 — `conversion_pricing`
- 2 — `conversion_stack_audit_entry`
- 1 — `conversion_newsletter_2026_w35_html`
- 1 — `conversion_compare_shortlist`
- 1 — `stack_audit_cta`
- 1 — `conversion_stack_builder_html`
- 1 — `conversion_stack_builder`
- 1 — `conversion_cost_calculator`
- 1 — `stack_audit_completed`

### Stack Audit funnel

- Visitors to page: 10
- Started: 4
- Completed: 1
- Start rate: 40% · completion rate: 10%
```

### `python3 scripts/plausible_report.py --period 7d`

```
## Traffic (7d)

- Visitors: **18**
- Pageviews: **36**
- Bounce rate: 83% · avg visit 74s

### Top pages

- 4v / 7pv — `/`
- 3v / 3pv — `/tools/perplexity/`
- 2v / 4pv — `/premium/`
- 2v / 2pv — `/comparisons/canva-ai-vs-leonardo-ai.html`
- 1v / 1pv — `/newsletter/`
- 1v / 1pv — `/tools/catch-ai/`
- 1v / 2pv — `/stack-audit.html`
- 1v / 1pv — `/tools/fireflies/`
- 1v / 1pv — `/tools/landlord-studio/`
- 1v / 1pv — `/premium/library/`

### Sources

- 10v — Direct / None
- 4v — Perplexity
- 2v — ChatGPT
- 2v — Google

### Conversion goals

- 5 — `conversion_premium`
- 2 — `stack_audit_started`
- 1 — `conversion_newsletter`
- 1 — `conversion_stack_audit_entry`

### Stack Audit funnel

- Visitors to page: 1
- Started: 2
- Completed: 0
- Start rate: 200% · completion rate: 0%
```

---

## 9. Data sources

- **Plausible `/api/v2/query`** via `scripts/plausible_report.py` (both periods, plus cross-checks broken down by `visit:source`, `visit:channel`, `visit:country`, `visit:device`, `visit:browser`, `visit:entry_page`, `event:page`, `event:name`, `time:day`, `visit:utm_source`, `visit:utm_campaign`, and compound breakdowns). Explicit `date_range` arrays used for the three complete Mon–Sun weeks. Token at `~/.hermes/profiles/aitools/plausible_token`; never printed.
- Code inspection for the instrumentation findings: `js/analytics.js`, `js/stack-audit.js`, `js/tracking.js`, `js/cookie-consent.js`.
- `scripts/validate_site.py` (passes: 732 public pages, 76 tools), `sitemap.xml`, git history for commit/file/page counts, and a per-file `git show` sweep of the 2026-09-19 and 2026-09-20 trees confirming 0 of 732 public HTML files lack the analytics loader.
- Live fetches of `https://aitoolsessentials.com/` for the loader, `/js/analytics.js` (HTTP 200), `/premium/` checkout links, and canonical tags.
- `marketing/gsc-diagnosis-2026-09-12.md` (GSC export 2026-08-22 → 2026-09-10 — **stale, refresh pending**), `admin/held-submissions.md`, `marketing/backlink-outreach-2026-09.md`.

---

*Report generated by Hermes Agent (aitools profile) via cron job. Every traffic figure above comes from Plausible v2 output — no estimates, no v1 calls, no ranges. Next report: 2026-09-28.*
