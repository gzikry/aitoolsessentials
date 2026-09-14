# Weekly Traffic Report — AIToolsEssentials

**Week of:** 2026-09-08 → 2026-09-14
**Report date:** 2026-09-14
**Site:** https://aitoolsessentials.com
**Analytics:** Plausible **v2** API — real data (token at `~/.hermes/profiles/aitools/plausible_token`)

> **Two corrections to the prior reports.**
>
> **1. Plausible was never inaccessible.** The 2026-09-07 report stated the dashboard "and the public API endpoints are not publicly accessible — ... no API key is configured" and estimated traffic at 12–25 visitors. That was wrong: a Plausible API token has been sitting at `~/.hermes/profiles/aitools/plausible_token` since 2026-08-25, and `scripts/plausible_report.py` already wraps the whole query set. Actual traffic for the week that report covered was **24 visitors / 90 pageviews** — the guess landed in range by luck, but it was a guess and should not have been. This report contains no estimates.
>
> **2. v1 and v2 disagree; v2 is authoritative.** My first pass this week used the v1 stats endpoints. Cross-checking against v2 produced *different numbers on the same dimensions* — sources (Google 8 vs 6 visitors), homepage visitors (9 vs 8), conversion events (3 vs 2), countries (US 15 vs 14, plus a phantom MU), and browsers (a phantom Safari). v1 returns stale/zero-filled data for this site. **Every figure below is from `/api/v2/query`**, and where a number moved I used the v2 value. Any future report must use v2 only.

---

## 1. Traffic Sources

### Headline

| Metric | This week (Sep 8–14) | Last week (Sep 1–7) | Change |
|---|---|---|---|
| Visitors | **26** | 24 | **+8.3%** |
| Pageviews | **69** | 90 | **−23.3%** |
| Pages / visitor | 2.65 | 3.75 | **−29%** |
| Bounce rate | 68% (trailing 7d) | — | — |
| Avg. visit duration | 147 s (2m27s) | — | — |
| 30-day visitors | **77** | — | — |
| 30-day pageviews | **247** | — | — |
| 30-day bounce / duration | 58% / 133 s | — | — |

Visitors rose slightly while pageviews fell by a quarter. That is a real move, not noise at these volumes: last week's 90 pageviews came from 24 visitors at 3.75 pages each, this week's 69 from 26 at 2.65. The extra depth last week came from the homepage redesign and Stack Audit launch drawing repeat internal navigation from a handful of sessions. This week the same number of people read fewer pages each.

### Sources (Sep 8–14)

| Source | Visitors | Pageviews | Share of visitors |
|---|---|---|---|
| Direct / None | **19** | 53 | **73%** |
| Google | **6** | 15 | 23% |
| Perplexity | 1 | 1 | 4% |

### Sources (30 days)

| Source | Visitors | Pageviews |
|---|---|---|
| Direct / None | 63 | 223 |
| Google | 10 | 20 |
| ChatGPT | 1 | 1 |
| Perplexity | 1 | 1 |
| 247team.ai.studio | 1 | 1 |
| impactcommunityservices.sharepoint.com | 1 | 1 |

### Reading the sources honestly

**"Direct" is not a traffic source at this size — it is mostly us.** 14 of the 26 visitors are US, 8 are Nigeria, 2 Russia. Nigeria is the Sonaopus vendor checking their own listing: `/tools/sonaopus/` drew 4 visitors and 9 pageviews this week, was an *entry* page for 4 sessions, and the NG sessions cluster on `/`, `/tools/index.html`, and `/tools/sonaopus/` — which is what reviewing your own listing looks like. Two visitors arrived on Yandex Browser from RU.

Strip the vendor-check and crawler-adjacent traffic and the **genuinely new audience for the week is 7 visitors** — Google 6 plus Perplexity 1. That is the number that matters, and it is small.

**Google's measurable traffic is essentially all from this week.** 6 of the 10 Google visitors in the entire 30-day window arrived in these 7 days. Google sent 6 visitors and 15 pageviews this week against 4 visitors across the preceding three weeks. This is the first week search produced a measurable audience rather than impressions alone — the single most important number here.

**Zero traffic from any directory, email, or social channel.** No directory referral. No UTM campaign. The only tagged visit in 30 days is a single `utm_source=chatgpt.com`. Directories have sent nothing despite three submissions; nine days of outreach has sent nothing either.

The two one-off referrers (`247team.ai.studio`, `impactcommunityservices.sharepoint.com`) are single sessions, most likely someone opening a link from a doc or dashboard. Not links, not traffic.

### Engagement detail

- Devices: Mobile 13 / Desktop 13 — a genuinely even split, so mobile layout carries as much weight as desktop.
- Browsers: Chrome 21, Opera 2, Yandex 2, Edge 1. **No Safari at all.** Chrome dominance with Yandex/Opera present reads as a technical and bot-adjacent audience, not consumer readers.
- Countries: US 14, NG 8, RU 2, MY 1, BR 1.

---

## 2. Top Performing Pages

### This week (Sep 8–14)

| Page | Visitors | Pageviews |
|---|---|---|
| `/` | 8 | 17 |
| `/tools/index.html` | 5 | 6 |
| `/tools/sonaopus/` | 4 | 9 |
| `/stack-audit.html` | 4 | 4 |
| `/submit-tool.html` | 3 | 7 |
| `/legal/privacy.html` | 2 | 3 |
| `/legal/terms.html` | 2 | 2 |
| `/pricing-watch/` | 2 | 2 |
| `/guides/switch-guides/` | 1 | 2 |
| then 15 pages with 1 visitor each | 1 | 1 |

### Last week (Sep 1–7), for comparison

| Page | Visitors | Pageviews |
|---|---|---|
| `/` | 15 | 33 |
| `/stack-audit.html` | 5 | 5 |
| `/submit-tool.html` | 3 | 8 |
| `/subscribe/` | 3 | 6 |
| `/premium/` | 3 | 3 |
| `/newsletter/` | 2 | 5 |
| `/newsletter/2026-w35.html` | 1 | **9** |

### What the page data says

**The homepage halved and nothing replaced it.** 15 → 8 visitors, 33 → 17 pageviews. The prior week's numbers were inflated by redesign-driven repeat visits; this week is closer to the real baseline. No other page took up the slack.

**Sonaopus, published Sep 12, is already the second-most-viewed page (4 visitors, 9 pageviews, 4 entry sessions) — and all of it is vendor traffic from Nigeria.** Not a readership signal, but it does confirm the review is live, indexed, and reachable. Its nine comparison pages drew a combined 5 visitors, so the cluster is not yet pulling anyone in from search.

**`/submit-tool.html` remains the most pageview-dense page (7 pageviews from 3 visitors)** and appears in both weeks. That is a form being filled repeatedly, not read — consistent with the eight FormSubmit submissions in the mailbox this week.

**Google's entry pages are the useful part.** Six Google visitors entered on six different pages, one each: `/`, `/pricing-watch/`, `/stack-audit.html`, `/submit-tool.html`, `/tools/sonaopus/`, and `/guides/switch-guides/switch-from-gemini-to-claude.html`. **Pricing Watch and the switch guides are earning search entry unprompted** — these are the two content surfaces with proven pull, and the ones worth deepening.

**Direct entry pages** tell the same story from the other side: `/` (6), `/tools/sonaopus/` (3), `/stack-audit.html` (2), `/submit-tool.html` (2), then `/premium/`, `/tools/jasper/`, `/tools/gamma/`, `/tools/cursor/`, `/tools/index.html`, and three `leonardo-ai` comparisons at 1 each.

### Conversion events — the funnel went backwards

| Event | Sep 1–7 | Sep 8–14 |
|---|---|---|
| `conversion_subscribe` | **4** | **0** |
| `conversion_premium` | 2 | **0** |
| `conversion_newsletter` | 1 | **0** |
| `conversion_newsletter_2026_w35_html` | 1 | **0** |
| `conversion_pricing` | 1 | **0** |
| `conversion_stack_builder_html` | 1 | **0** |
| `stack_audit_cta` | 1 | **0** |
| `stack_audit_started` | 1 | 1 |
| `conversion_stack_audit_entry` | 0 | 1 |
| `stack_audit_completed` | 1 | **0** |
| **Total non-pageview events** | **9** | **2** |

**Nine conversion events dropped to two — a −78% collapse — while visitors rose 8%.** Last week produced four subscribe intents, two premium intents, a newsletter click, a pricing click, and a completed audit. This week produced one audit entry and one audit start, and nothing else. No subscribe, no premium, no newsletter, no pricing, no completed audit.

At 26 visitors the sample is far too small to call a broken CTA — but the direction is unambiguous and it is the second consecutive structural problem in these numbers (the first being that the audience is us). Two readings, and they need one more week to separate:

1. **Exposure:** homepage traffic halved, and the homepage is where the Premium/subscribe CTAs live. Fewer people saw the funnel at all.
2. **The audience changed character:** last week's visitors were more likely internal/returning (higher pages-per-visit); this week's are cold one-page arrivals from search, who do not convert on first touch. That would be a more hopeful reading — cold search traffic not converting yet is normal.

Do not act on either this week. Set the trip-wire explicitly: **if next week shows ≤3 non-pageview events on comparable traffic, instrument each funnel step individually** before spending any further effort on traffic acquisition, because traffic that cannot convert is not the bottleneck.

**30-day event totals** (for context): `conversion_subscribe` 4 visitors / 5 events, `conversion_premium` 3, `conversion_pricing` 2, `conversion_newsletter` 2, `stack_audit_started` 2, `stack_audit_completed` 1, and one each for `conversion_compare_shortlist`, `conversion_cost_calculator`, `conversion_stack_builder`, `conversion_stack_audit_entry`, `stack_audit_cta`.

**No 404 events in 30 days** (confirmed against the full window, not a narrow one). **Outbound-link events are also absent** — on a site whose entire model is sending readers to vendor pages, that is worth confirming rather than assuming; either the event is not firing or nobody clicks out.

### Site volume

| Content type | Count |
|---|---|
| Sitemap URLs | 724 |
| HTML pages | 736 |
| Tools tracked / reviewed | 76 |
| New HTML pages this week | 13 |
| Commits this week | 63 |
| Files changed this week | 850 |

**New pages this week (13):** `articles/ai-email-triage-setup.html`, `articles/company-ai-usage-policy-checklist.html`, `quiz/coding-assistant-keep-cut.html`, `tools/sonaopus/index.html`, and nine comparisons pairing Sonaopus against incumbents (`airtable-ai`, `gamma`, `grammarly`, `htmlslides`, `microsoft-copilot`, `notion-ai`, `rows`, `shortwave`, `slack-ai`). A deliberate cluster: one vendor reviewed, nine head-to-head entry points built around it.

---

## 3. New Backlinks Earned This Week

**Editorial backlinks earned: 0.**

| Source | URL | Status | Type |
|---|---|---|---|
| SaaSHub | saashub.com/aitoolsessentials | **Live, still "Pending approval"** — verified this week | Directory |
| The Next AI | thenextai.com/ai-tools/aitoolsessentials/ | **Not found — 404** | None |
| AIAI.Tools | aiai.tools/aitoolsessentials/ | **Not found — listing URL errors** | Unconfirmed |

**SaaSHub — verified in full this week.** The listing is live and now correctly categorized under **AI Tools → Software Directory**; the wrong Finance → Subscriptions placement is fixed. It carries the real logo, the approved description, pricing (Freemium, free trial, $12/month Premium), and six answered product Q&A prompts. The "Pending approval…" banner and "0 reviews" remain, and the alternatives page still says "the primary details have not been verified within the last quarter." The field-completion work of Sep 13 landed completely — SaaSHub simply has not re-reviewed.

**The Next AI — the backlink is gone.** The Sep 7 report recorded this as "submitted & approved Sep 3, live page not confirmed." It is confirmed now and the answer is negative: `thenextai.com/ai-tools/aitoolsessentials/` and the `/tool/` variant both return **404**, and the directory's featured-tools list carries no AIToolsEssentials entry. Either it was never published or it was removed. This needs a **resubmission**, not a wait — and it means the prior report's "2 confirmed" directory count was one too high.

**AIAI.Tools** — homepage returns 200 and a site-search title match exists, but the listing path errors on extraction. Counted as unconfirmed, not as a backlink.

**No external mentions found** via web search this week. No badge adoptions. No third-party site observed citing or linking to the site.

---

## 4. Directory Submissions Status

| Directory | Status | Notes |
|---|---|---|
| **SaaSHub** | **Live — pending re-review** | All fields completed and verified Sep 13: correct category, logo, pricing, six Q&A answers. Banner persists. |
| **The Next AI** | **LOST — 404** | Approved Sep 3, no live page exists now. Needs resubmission. |
| **AIAI.Tools** | Unconfirmed | Confirmation received Sep 3; listing URL not resolving. |
| **AlternativeTo** | Blocked — George's account | Highest-value free directory remaining (DA ~90). |
| **Uneed** | Blocked — George's account | Cannot save without signup; support only auto-acked. |
| **ToolScout** | Closed — paid placement only | Replied asking what we would pay. No budget for placement. |
| **AIToolsDirectory.com** | Blocked — form automation | Paperform SPAN elements; needs `click_at_xy`. |
| **PoweredByAI** | Blocked — form automation | React Select components. |
| **Dofollow.Tools** | Blocked — form automation | Multi-step form; AI auto-fill silently failed. |
| **Futuretools.io** | Blocked — 404 | Submit page still returns 404. |
| Paid-only (Toolify, TopAI, AIXploria, TAAFT, Futurepedia) | Skipped | $47–$497. No spend approved. |

**Summary: 1 live-pending (SaaSHub), 1 lost (The Next AI), 1 unconfirmed (AIAI.Tools), 2 George-blocked, 3 automation-blocked, 5 paid-only.**

**Directories sent zero visitors this week** — zero in 30 days, in fact. Three submissions, one confirmed live, and not one referral in Plausible. **Directory listings are a backlink play at this stage, not a traffic play**, and the reports should stop implying otherwise.

---

## 5. Email Outreach Responses

### Sent volume

**61 outbound sends across 58 distinct domains** on Sep 9 (the "free keep/cut companion for X readers" batch), plus follow-ups. September total: **78 sends / 68 distinct domains**.

### Replies received (Sep 9–14)

| Date | Target | Response | Outcome |
|---|---|---|---|
| Sep 11 | memeburn.com — Carl Davis | Offered paid press releases, partner articles, banners: $600–$1,200 (MemeBurn), $400–$900 (NFT Plazas) | **Declined — paid only** |
| Sep 11 | toolscout.ai | Asked what AIToolsEssentials would pay for placement; pitched twice | **Declined — paid only** |
| Sep 11 | techsy.io | $170 roundup / $86 review / $238 both; then proposed a **link exchange** and asked for our DR + monthly traffic | **Declined both** — early site, and we do not trade undisclosed dofollow links |
| Sep 10 | zplatform.ai — Alston Antony | $95 per article "or link insertion", 700-word minimum | **Declined — paid only** |
| Sep 9 | uneed.best | Support auto-ack only ("9:00–18:00 UTC+1 weekdays") | Open — no human reply |
| Sep 9 | stack-match.io | Replied twice | Closed |
| Sep 11 | stackaible.com — info@ | **Hard bounce 550 no such user** | Closed — unreachable |
| Sep 11 | videoupscaler.video — support@ | **Hard bounce 550 5.1.1** | Blocked — vendor's published contact is broken |
| Sep 12 | aitoolswise.com, llmversus.com, aigearbase.com | Final DSNs `Action: failed` / `4.4.1` after Gmail's ~3-day retry cycle | **Closed — unreachable** |

### The honest read

**Six human replies from 61 sends (9.8%) — and every single one was a sales pitch.** Not one was an editorial yes. Four asked for money ($86–$1,200); one was a support auto-acknowledgement; one was a thread already closed. The editorial-placement rate of this campaign is **0%**.

That is a clear enough pattern to stop and name: **the outreach list is being answered by link sellers, not editors.** The addresses that reply are monetized placement desks. Sending more of this email class at volume will keep producing the same result — paid offers to decline. More volume is the wrong fix.

**Five domains are confirmed dead ends** — three with no MX at all (aitoolswise.com, aigearbase.com, llmversus.com), one with a broken published address (videoupscaler.video), one with no published address anywhere (stackaible.com). All closed; no retries.

### HARO / journalist requests

Daily digests ran Sep 8–14. The Sep 11 and Sep 12 digests flagged live on-beat opportunities — notably a **FinOps agentic-AI-cost-overrun request** ("the core AIToolsEssentials problem", live across four consecutive runs) and a **Science Magazine** request for individual scientists paying out of pocket for AI subscriptions. The Sep 13 and Sep 14 digests both came back thin, and the Sep 14 run verified it at the body level rather than by slug: of 63 AI-token candidate bodies since Sep 2, only 6 carry a strong spend signal, five of which were already in or retired from the queue — **exactly one new adjacent body surfaced**, an EdTech writer's "whoever signs the invoice controls the roadmap" call. The beat is genuinely thin, not under-searched. **Six opportunities expired in today's run, including the FinOps request still sitting unpitched.**

**No pitch emails were sent from any of these leads.** I searched Sent Mail, Trash, and All Mail for every HARO/pitch variant and found zero sends. The FinOps request — the best-matched opportunity of the month, flagged live on four separate runs and then allowed to expire — went unpitched. Its window has closed.

**This is the clearest process failure of the month, and it is a process failure, not a targeting failure.** The monitor is doing its job: it found the right request, correctly identified it as core to the site's thesis, and recorded that the window was narrowing. Nothing then acted on it. Monitoring without a send step produces reports, not links.

### Newsletter

Beehiiv publication (Keep/Cut Weekly) remains live with **0 subscribers** and no issue sent this week. There was **1 newsletter conversion event** in the 30-day window (a click on Issue 1, `2026-w35.html`, which drew 1 visitor / 9 pageviews last week) against 5 subscribe-intent events — people move toward the newsletter and the signup does not complete or is not recorded. Beehiiv's subscriber count remains **unverified**: the public API returns 403 without a key and the MCP requires interactive OAuth. It has been reported as "0" for weeks on assumption; treat it as unknown.

### Social

**Nothing published.** No X posts, no LinkedIn. `xurl` has no apps registered, so posting was not possible even if attempted. The five templates in `marketing/social-posts-2026-08.md` have now sat unused for two weeks.

---

## 6. Recommendations for Next Week

Ordered by expected return.

### 1. Pitch in the same run that finds the opportunity

The daily HARO monitor identifies good requests and nothing is sent. Add pitch execution to the monitor: when a digest flags a high-relevance item with a live deadline, draft **and send** the pitch in that run. Also stop treating "0 opportunities" as neutral — the Sep 13 digest's own analysis (3 matching slugs out of 882) is the finding, so widen to adjacent beats (AI procurement, SaaS sprawl, subscription audits) instead of re-scanning one narrow term.

### 2. Resubmit to The Next AI — and verify the page before counting it

The approved listing 404s. Resubmit, then fetch the live URL and confirm a 200 with the link visible **before** recording it as a backlink. The prior report counted it as confirmed on the strength of an approval email alone; there was no page. Only a successful fetch counts.

### 3. Deepen the two pages with proven search entry

Pricing Watch and the Gemini→Claude switch guide each pulled a Google visitor on their own, unprompted, in the site's first week of real search traffic. They have demonstrated demand. Add depth there before building anything new — this is the same conclusion the GSC diagnosis reached about `best-ai-tools-for-agencies` (259 impressions, position 29.6, 425 words).

### 4. Change the outreach list, not the volume

61 sends produced 6 replies, all sellers. Shift to targets where an editorial mention *is* the business model: journalists (via #1), niche practitioners who cite resources, and vendor-side badge programs. Stop emailing monetized directory placement desks.

### 5. Work the badge program as the systematic backlink route

`/badges/` exists to give reviewed vendors an embeddable badge linking back to their review. **Zero adoptions.** There are now 76 reviewed tools — a single outreach to each reviewed vendor offering the badge is a concrete, non-spammy, zero-cost backlink program with a real conversion path, and it is the closest thing to a repeatable link engine the site has.

### 6. Set the funnel trip-wire

Conversion events fell from 9 to 2 (−78%) while visitors rose. Too small to diagnose, too large to ignore. **If next week shows ≤3 non-pageview events on comparable traffic, instrument each funnel step individually** before doing any further acquisition work.

### 7. Verify outbound-link tracking

No outbound-click events in 30 days on a site built to send readers to vendors. Confirm whether the event fires at all.

### 8. George-only: AlternativeTo and Uneed accounts

The two highest-value free directories, both blocked purely on signup. AlternativeTo is DA ~90. Nothing on the agent side can move these.

### 9. Get the Beehiiv key, or report the count as unknown

Subscriber state cannot be verified programmatically without a key, and "0 subscribers" has been carried forward unverified for weeks. Either a key goes in `.env`, or the report states the figure as unverified.

### 10. Always use the Plausible v2 API

`scripts/plausible_report.py` already wraps v2 correctly. Do not hand-roll v1 stats calls — they disagree with v2 on sources, pages, events, countries, and browsers.

---

## Summary Metrics

| Metric | Value |
|---|---|
| Visitors (Sep 8–14) | **26** |
| Pageviews (Sep 8–14) | **69** |
| Visitors week-over-week | **+8.3%** |
| Pageviews week-over-week | **−23.3%** |
| 30-day visitors / pageviews | 77 / 247 |
| Genuinely new-audience visitors (Google + Perplexity) | **7** |
| Google visitors: 30d total vs this week | **10 total, 6 this week** |
| Bounce rate (7d / 30d) | 68% / 58% |
| Avg. visit duration (7d / 30d) | 147 s / 133 s |
| Top page | `/` (8 visitors, 17 pageviews) |
| Conversion events (7d) | **2** (down from 9, −78%) |
| Stack audits completed (30d) | 1 |
| Sitemap URLs / HTML pages | 724 / 736 |
| New HTML pages this week | 13 |
| Commits this week | 63 |
| Directory listings live | **1** (SaaSHub, pending re-review) |
| Directory listings lost | **1** (The Next AI — 404) |
| Directory referrals | **0** |
| Editorial backlinks earned | **0** |
| Outreach emails sent (Sep 9 batch) | 61 across 58 domains |
| Outreach human replies | 6 (9.8%) — all paid placement offers |
| Editorial placements won | **0** |
| HARO opportunities pitched | **0** (of several flagged live) |
| Dead-end domains closed | 5 |
| Beehiiv subscribers | unknown (reported as 0 for weeks; unverified) |
| Social posts published | 0 |

---

## Data Sources

- **Plausible `/api/v2/query`** — aggregate, breakdown by `visit:source`, `event:page`, `visit:entry_page`, `visit:country`, `visit:device`, `visit:browser`, `event:name`, with explicit `date_range` arrays for the two comparison weeks. Token at `~/.hermes/profiles/aitools/plausible_token`; wrapper at `scripts/plausible_report.py`.
- GSC export 2026-08-22 → 2026-09-10 (see `marketing/gsc-diagnosis-2026-09-12.md`): 4,665 impressions, 6 clicks, average position 44.3, improving from 62.
- Git history for page, commit, and file counts.
- Himalaya over the `aitools` IMAP account: INBOX, Sent Mail, Trash, All Mail, Spam.
- `admin/held-submissions.md`, `marketing/backlink-outreach-2026-09.md`, `admin/affiliate-applications-ready.md`, `marketing/haro-outreach/digest-2026-09-{10,11,12,13,14}.json`.
- Live HTTP checks: SaaSHub (listing + alternatives page), The Next AI, AIAI.Tools.

---

## 4. Analytics coverage gap — 53 pages could not be counted (fixed 2026-09-14)

Every figure above is a **floor, not a total**. A third of the site had no analytics
loader, so its visitors were never counted by Plausible at all.

53 live, sitemap-listed pages served no `js/analytics.js`:

- the legacy article/`.html` comparison template — `articles/*-vs-*.html` (20 pages:
  jasper-vs-copy-ai, elevenlabs-vs-playht, make-vs-n8n, gamma-vs-beautiful-ai, …) and
  `comparisons/gemini-vs-claude.html`
- the how-to hub and its 9 guides (`how-to/*.html`, including install-hermes-agent)
- `guides/official/*` (index + cohere, qwen, apple-intelligence, deepseek)
- `best-for/`, `change-radar/`, `pricing-report/`, `local-ai-planner/`
- `hardware/` + 5 hardware pages, `use-cases/best-ai-tools-for-teachers.html`,
  `workflows/classroom-lesson-planning.html`, `services/ai-stack-consulting.html`,
  `downloads/ai-stack-decision-checklist.html`, `checkout/complete/`,
  `xai-bot-guides/designing-grok-bot-with-grok-bot/`

Two consequences that matter more than the missing rows:

1. **The teachers page is a hole in the data.** It is tied to the single largest GSC
   opportunity theme (51 queries / 343 impressions) and it was one of the uncounted
   pages. Any decision about deepening it was made blind.
2. **Affiliate-eligible pages were among the invisible ones.** `articles/make-vs-n8n.html`,
   `articles/zapier-vs-make.html`, `articles/elevenlabs-vs-playht.html`,
   `articles/gamma-vs-beautiful-ai.html`, `how-to/install-hermes-agent.html` and
   `best-for/` all carry links to approved programs (Make 35%, ElevenLabs 22%, Gamma,
   Nous) and none of their traffic was measurable, so affiliate intent could not be
   attributed.

**Fix shipped:** `scripts/cleanup_html.py` now injects the loader on every public page
(and keeps it across regeneration), and `scripts/validate_site.py` fails the build with
`Public pages missing analytics loader` if any public page lacks it. `admin/` paste packs
and `go/` redirect stubs stay excluded. Commit `60dfa418`; deploy verified live on
cache-busted URLs across all affected page types.

**Read next week's figures with this in mind:** visitors and pageviews will rise for a
reason that is not growth. Pages that were never counted are now counted, so a step up in
`articles/*-vs-*.html`, `how-to/*`, `guides/official/*`, `best-for/`, `change-radar/`,
`pricing-report/` and the teachers guide is instrumentation, not audience. The honest
comparison baseline resets on 2026-09-14.

---

*Report generated by Hermes Agent (aitools profile) via cron job. All traffic figures are real Plausible v2 API data — no estimates. Next report: 2026-09-21.*
