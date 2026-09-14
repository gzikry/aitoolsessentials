# Weekly Traffic Report — AIToolsEssentials

**Week of:** 2026-09-08 → 2026-09-14
**Report date:** 2026-09-14
**Site:** https://aitoolsessentials.com
**Analytics:** Plausible — **real API data this week** (token at `~/.hermes/profiles/aitools/plausible_token`)

> **Correction to prior reports.** The 2026-09-07 report stated Plausible was inaccessible and estimated traffic at 12–25 visitors. That was wrong: a Plausible API token has existed in the profile since 2026-08-25. Actual traffic for the week reported then was **24 visitors / 90 pageviews** — the estimate happened to land in range, but it was a guess and should not have been. This report contains no estimates; every number is from the Plausible Stats API or from git/mail evidence.

---

## 1. Traffic Sources

### Headline

| Metric | This week (Sep 8–14) | Last week (Sep 1–7) | Change |
|---|---|---|---|
| Visitors | **26** | 24 | **+8.3%** |
| Pageviews | **69** | 90 | **−23.3%** |
| Pages / visitor | 2.65 | 3.75 | **−29%** |
| Bounce rate (7d) | 68% | — | — |
| Avg. visit duration | 147 s (2m27s) | — | — |
| 30-day visitors | **77** | — | — |
| 30-day pageviews | **247** | — | — |

Visitors rose slightly while pageviews fell by a quarter. That is a real signal, not noise at these volumes: last week's 90 pageviews came from 24 visitors at 3.75 pages each, this week's 69 from 26 at 2.65. The extra pages last week were the homepage redesign and Stack Audit launch drawing repeat internal navigation from a handful of sessions. This week the same number of people read fewer pages each.

### Sources (7 days)

| Source | Visitors | Pageviews | Share of visitors |
|---|---|---|---|
| Direct / None | 19 | 63 | **68%** |
| Google | 8 | 17 | 29% |
| Perplexity | 1 | 1 | 4% |

### Sources (30 days)

| Source | Visitors | Pageviews |
|---|---|---|
| Direct / None | 63 | 223 |
| Google | 10 | 20 |
| 247team.ai.studio | 1 | 1 |
| ChatGPT | 1 | 1 |
| Perplexity | 1 | 1 |
| impactcommunityservices.sharepoint.com | 1 | 1 |

### Reading the sources honestly

**"Direct" is not a traffic source — at this size it is mostly us.** 11 of the 19 direct visitors are US, 7 are Nigeria. Nigeria is the Sonaopus vendor's own follow-up traffic: the Sonaopus review drew 4 visitors as an entry page and 9 pageviews this week, the second-highest page on the site, and NG sessions hit `/tools/sonaopus/`, `/tools/index.html`, and `/`, which is what checking your own listing looks like. Two visitors arrived on Yandex Browser from RU. Strip the vendor-check and crawler-adjacent traffic and the genuinely new-audience figure for the week is closer to **9 visitors** (Google 8 + Perplexity 1).

**Google's entire 30-day contribution arrived this week.** 8 of the 10 Google visitors in the 30-day window came in the last 7 days. Google sent 8 visitors and 17 pageviews this week versus essentially none in the trailing three weeks. That is the most important number in this report — it is the first week search produced a measurable audience rather than impressions alone.

**Zero traffic from any directory, email, or social channel.** No directory referral, no UTM campaign, no newsletter click. The 30-day UTM breakdown contains exactly one tagged visit (`utm_source=chatgpt.com`, 1 visitor). Directories have not sent a single visitor despite three submissions; nine days of outreach has not sent one either.

### Engagement detail

- Devices: Desktop 14 / Mobile 14 — a genuinely even split, so mobile layout matters as much as desktop.
- Browsers: Chrome 22, Opera 2, Yandex 2, Edge 1, Safari 1. Only one Safari visitor; Chrome dominance with Yandex/Opera present is consistent with a technical/bot-adjacent audience rather than consumer readers.
- Countries: US 15, NG 8, RU 2, BR 1, MU 1, MY 1.

---

## 2. Top Performing Pages

### This week (Sep 8–14)

| Page | Visitors | Pageviews |
|---|---|---|
| `/` | 9 | 18 |
| `/tools/sonaopus/` | 4 | 9 |
| `/tools/index.html` | 5 | 6 |
| `/stack-audit.html` | 5 | 5 |
| `/legal/privacy.html` | 3 | 4 |
| `/submit-tool.html` | 3 | 13 |
| `/comparisons/best-ai-tools.html` | 2 | 2 |
| `/legal/terms.html` | 2 | 2 |
| `/pricing-watch/` | 2 | 2 |
| `/guides/switch-guides/` | 1 | 2 |

### Last week (Sep 1–7), for comparison

| Page | Visitors | Pageviews |
|---|---|---|
| `/` | 15 | 33 |
| `/submit-tool.html` | 3 | 8 |
| `/subscribe/` | 3 | 3 |
| `/premium/` | 3 | 3 |
| `/stack-audit.html` | 5 | 5 |
| `/newsletter/` | 2 | 5 |

### What the page data says

**The homepage and the Sonaopus review are the only pages with real pull.** The homepage halved week-over-week (15 → 9 visitors, 33 → 18 pageviews) — expected after the redesign-driven repeat visits settled. Sonaopus, published Sep 12, took 4 visitors and 9 pageviews within two days, all of it vendor-side. That is not a readership signal, but it does confirm the review is live and reachable.

**`/submit-tool.html` is the most pageview-dense page on the site (13 pageviews from 3 visitors)** and appears in both weeks. That is a form being filled in repeatedly, not read — consistent with the eight FormSubmit submissions in the mailbox this week.

**Google's entry pages are the useful part.** The 8 Google visitors landed on `/pricing-watch/` (2), then one each on `/`, `/alternatives/`, `/comparisons/best-ai-tools.html`, `/faq.html`, `/guides/switch-guides/`, `/stack-audit.html`, `/submit-tool.html`, `/tools/index.html`, `/use-cases/best-ai-tools-for-teachers.html`. Pricing Watch, the switch guides, and the alternatives hub are earning search entry on their own — these are the pages worth deepening.

**Conversion events — 7 days:** `stack_audit_started` 1, `conversion_stack_audit_entry` 1, `conversion_stack_builder_html` 1.

**Conversion events — 30 days:** `conversion_subscribe` 5 (4 visitors), `conversion_premium` 3 (3), `conversion_newsletter` 2, `conversion_pricing` 2, `stack_audit_started` 2, `stack_audit_completed` 1, `stack_audit_cta` 1, plus single events for compare-shortlist, cost-calculator, stack-builder.

**The funnel moved backwards.** Last week produced 4 subscribe events, 2 premium, 1 newsletter, 1 pricing, and a completed audit. This week produced **one** stack-audit entry and one start — no subscribe, no premium, no newsletter click. Nine conversion events dropped to three. Either the funnel pages are not being seen (homepage traffic halved) or the CTAs are not working at these volumes; at 26 visitors the sample is too small to distinguish, but the drop is real and worth watching for a second week before intervening.

**No 404 events recorded** in 30 days, and no outbound-link click events — the outbound tracking appears not to be firing, worth confirming.

### Site volume

| Content type | Count |
|---|---|
| Sitemap URLs | 724 |
| HTML pages | 736 |
| Tools tracked / reviewed | 76 |
| New HTML pages this week | 13 |
| Commits this week | 63 |
| Files changed this week | 850 |

**New pages this week (13):** `articles/ai-email-triage-setup.html`, `articles/company-ai-usage-policy-checklist.html`, `quiz/coding-assistant-keep-cut.html`, `tools/sonaopus/index.html`, and nine comparisons all pairing Sonaopus against incumbent tools (`airtable-ai`, `gamma`, `grammarly`, `htmlslides`, `microsoft-copilot`, `notion-ai`, `rows`, `shortwave`, `slack-ai`). That is a deliberate cluster: one vendor reviewed, nine head-to-head entry points built around it.

---

## 3. New Backlinks Earned This Week

**Editorial backlinks earned: 0.**

| Source | URL | Status | Type |
|---|---|---|---|
| SaaSHub | saashub.com/aitoolsessentials | **Live, still "Pending approval"** — verified this week | Directory |
| The Next AI | thenextai.com/ai-tools/aitoolsessentials/ | **Not found — URL returns 404** | None |
| AIAI.Tools | aiai.tools | Homepage 200; site search returns a title match for "aitoolsessentials" but the listing URL 404s | Unconfirmed |

**SaaSHub — verified in full this week.** The listing is live and now correctly categorized under **AI Tools → Software Directory** (the wrong Finance → Subscriptions placement is fixed). It carries the real logo, the approved description, pricing (Freemium, free trial, $12/month Premium), and six answered product Q&A prompts. The "Pending approval…" banner and "0 reviews" remain. The field-completion work done on Sep 13 landed — everything is present and correct; SaaSHub simply has not re-reviewed.

**The Next AI — the backlink is gone.** The Sep 7 report recorded this as "submitted & approved, live page not confirmed." It is confirmed now, and the answer is not there: `thenextai.com/ai-tools/aitoolsessentials/` and the `/tool/` variant both return **404**. The directory's featured-tools list contains no AIToolsEssentials entry. Either the listing was never published, or it was removed. This needs a resubmission, not a wait — and it means the prior report's "2 confirmed" count was one too high.

**AIAI.Tools** — homepage returns 200 and a site-search title match exists, but the listing path returns an HTTP error on extraction. Treated as unconfirmed rather than counted.

**No external mentions found** via web search. No badge adoptions. No third-party site was observed citing or linking to the site this week.

---

## 4. Directory Submissions Status

| Directory | Status | Notes |
|---|---|---|
| **SaaSHub** | **Live — pending re-review** | All fields completed and verified Sep 13; correct category, logo, pricing, Q&A. "Pending approval" banner persists. |
| **The Next AI** | **LOST — 404** | Approved Sep 3 but no live page exists now. Needs resubmission. |
| **AIAI.Tools** | Unconfirmed | Confirmation received Sep 3; listing URL not resolving. |
| **AlternativeTo** | Blocked — George's account | Highest-value free directory remaining (DA ~90). |
| **Uneed** | Blocked — George's account | Submission cannot save without signup; support only auto-acked. |
| **ToolScout** | Blocked — paid placement only | Replied asking what we would pay. Closed — no budget for placement. |
| **AIToolsDirectory.com** | Blocked — form automation | Paperform SPAN elements; needs `click_at_xy`. |
| **PoweredByAI** | Blocked — form automation | React Select components. |
| **Dofollow.Tools** | Blocked — form automation | Multi-step form; AI auto-fill silently failed. |
| **Futuretools.io** | Blocked — 404 | Submit page still returns 404. |
| Paid-only (Toolify, TopAI, AIXploria, TAAFT, Futurepedia) | Skipped | $47–$497. No spend approved. |

**Summary: 1 live-pending (SaaSHub), 1 lost (The Next AI), 1 unconfirmed (AIAI.Tools), 2 George-blocked, 3 automation-blocked, 5 paid-only.**

**Directories sent zero visitors this week.** Three submissions, one confirmed live, and not a single referral in Plausible. Directory listings are a backlink play at this stage, not a traffic play — the report should stop implying otherwise.

---

## 5. Email Outreach Responses

### Sent volume

**61 outbound sends across 58 distinct domains** on Sep 9 (the "free keep/cut companion for X readers" batch), plus follow-ups. September total: **78 sends / 68 distinct domains**.

### Replies received (Sep 9–14)

| Date | Target | Response | Outcome |
|---|---|---|---|
| Sep 11 | memeburn.com — Carl Davis | Offered paid press releases, partner articles, banners: $600–$1,200 (MemeBurn), $400–$900 (NFT Plazas) | **Declined — paid only** |
| Sep 11 | toolscout.ai | Asked what AIToolsEssentials would pay for placement; sent twice | **Declined — paid only** |
| Sep 11 | techsy.io | $170 roundup / $86 review / $238 both; then proposed a **link exchange** and asked for our DR + monthly traffic | **Declined both** — early site, and we do not trade undisclosed dofollow links |
| Sep 10 | zplatform.ai — Alston Antony | $95 per article "or link insertion", 700-word min | **Declined — paid only** |
| Sep 9 | uneed.best | Support auto-ack only ("9:00–18:00 UTC+1 weekdays") | Open — no human reply |
| Sep 9 | stack-match.io, hello@ | Replied twice | Closed |
| Sep 11 | stackaible.com — info@ | **Hard bounce 550 no such user** | Closed — unreachable |
| Sep 11 | videoupscaler.video — support@ | **Hard bounce 550 5.1.1** | Blocked — vendor contact broken |
| Sep 12 | aitoolswise.com, llmversus.com, aigearbase.com | Final DSNs `Action: failed` / `4.4.1` after Gmail's ~3-day retry cycle | **Closed — unreachable** |

### The honest read

**Six human replies from 61 sends (9.8%) — and every single one was a sales pitch.** Not one was an editorial yes. Four asked for money ($86–$1,200), one was a support auto-acknowledgement, one was a follow-up thread already closed. The effective editorial-placement rate of this campaign is **0%**.

That is a clear enough pattern to stop and name: **the directory/blog outreach list is being answered by link sellers, not editors.** The addresses that reply are monetized placement desks. Continuing to send this class of email at volume will keep producing the same result — paid offers to decline.

**Five domains are confirmed dead ends** — three with no MX at all (aitoolswise.com, aigearbase.com, llmversus.com), one with a broken published address (videoupscaler.video), one with no published address anywhere (stackaible.com). All are now closed; no retries.

### HARO / journalist requests

Daily digests ran Sep 8–13. The Sep 11 and Sep 12 digests flagged live on-beat opportunities — notably a **FinOps agentic-AI-cost-overrun request** (described as "the core AIToolsEssentials problem", live across four consecutive runs) and a **Science Magazine** request for individual scientists paying out of pocket for AI subscriptions. The Sep 13 digest found nothing new, and concluded the AI-spend beat on Sourcee is genuinely thin: of 882 requests posted since Sep 2, only three co-occur with both an AI and a spend token.

**No pitch emails were sent from any of these leads.** I searched Sent Mail, Trash, and All Mail for every HARO/pitch variant and found zero sends. The FinOps request — the single best-matched opportunity of the month, flagged as live on four separate runs — went unpitched, and its window has likely closed.

### Newsletter

Beehiiv publication (Keep/Cut Weekly) remains live with **0 subscribers**. No issue was sent this week. There was **1 newsletter conversion event** in the 30-day window (a click on Issue 1, `2026-w35.html`), against 5 subscribe-intent events — so the funnel is: people click toward the newsletter, and the signup does not complete or is not recorded. Beehiiv's subscriber count could not be independently verified (the public API returns 403 without a key, and the MCP requires interactive OAuth).

### Social

**Nothing published.** No X posts, no LinkedIn. `xurl` has no apps registered, so no posting was possible even if attempted. The five templates in `marketing/social-posts-2026-08.md` have now sat unused for two weeks.

---

## 6. Recommendations for Next Week

Ordered by expected return.

### 1. Pitch the FinOps/cost-overrun beat immediately — and set up a daily pitch step, not just monitoring

The daily HARO monitor identifies good opportunities and then nothing happens with them. That is the single clearest process failure this month: a request that is literally "the core AIToolsEssentials problem" surfaced four times and was never pitched. Add pitch execution to the monitor run — when a digest flags a high-relevance item with a live deadline, draft and send the pitch in the same run, don't file it.

Also: stop reporting "0 opportunities found" as a neutral outcome. The Sep 13 digest's own analysis (3 matching slugs out of 882 requests) is the useful finding — the beat is thin, so the monitor should widen to adjacent beats (AI procurement, SaaS sprawl, subscription audits) rather than keep re-scanning one narrow term.

### 2. Resubmit to The Next AI

The approved listing is gone — 404 on both URL patterns. Resubmit and then **verify the live page exists and returns 200 before counting it as a backlink.** The prior report counted it as confirmed on the strength of an approval email; there was no page. Only a fetched 200 with the link visible should count.

### 3. Deepen the three pages Google actually sends people to

Google's 8 visitors entered through `/pricing-watch/`, the switch guides, and `/alternatives/` / `/comparisons/best-ai-tools.html`. These earned search entry on their own, with no promotion. Pricing Watch in particular is the site's stated linkable asset and now has proof it ranks. Add depth there before building anything new.

### 4. Change the outreach list, not the volume

61 sends produced 6 replies, all of them sellers. Sending more of the same to the same class of target will not produce an editorial link. Shift to targets where an editorial mention is the actual business model: journalists (HARO beats, per #1), niche practitioners who cite resources, and vendor-side "featured on" badge programs. Stop emailing monetized directory placement desks.

### 5. Chase the badge program as the systematic backlink route

`/badges/` exists to give reviewed vendors an embeddable badge linking back to their review. **Zero adoptions.** There are now 76 reviewed tools — a one-time email to each reviewed vendor offering the badge is a concrete, non-spammy, zero-cost backlink program with a real conversion path, and it is the closest thing to a repeatable link engine the site has.

### 6. Fix the conversion funnel before traffic grows

Subscription/premium/newsletter events fell from 9 to 3 week-over-week while visitors rose. The funnel pages are getting fewer visits (homepage halved) and the CTAs are not converting the visits they get. At 26 visitors this is not yet diagnosable, but set a threshold: if next week also shows ≤3 conversion events on comparable traffic, instrument the funnel steps individually to find where it breaks — before spending effort on traffic that will not convert.

### 7. Verify outbound-link tracking

No `Outbound Link: Click` events in 30 days on a site whose entire model is sending people to vendor sites. Either the event is not firing or nobody is clicking out. Both matter; confirm which.

### 8. George-only: AlternativeTo and Uneed accounts

These remain the highest-value free directories and both are blocked purely on signup. AlternativeTo is DA ~90. Nothing on the agent side can move these.

### 9. Get the Beehiiv API key, or accept the manual count

Newsletter subscriber state cannot be verified programmatically without a key, and "0 subscribers" has been carried forward unverified for weeks. Either a key goes in `.env` or the report should state the count as unverified rather than 0.

---

## Summary Metrics

| Metric | Value |
|---|---|
| Visitors (Sep 8–14) | **26** |
| Pageviews (Sep 8–14) | **69** |
| Visitors week-over-week | **+8.3%** |
| Pageviews week-over-week | **−23.3%** |
| 30-day visitors / pageviews | 77 / 247 |
| Genuinely new-audience visitors (Google + Perplexity) | **9** |
| Google visitors 30d vs this week | 10 total, 8 this week |
| Bounce rate (7d) / visit duration | 68% / 2m27s |
| Top page | `/` (9 visitors, 18 pageviews) |
| Conversion events (7d) | **3** (down from 9) |
| Stack audits completed (30d) | 1 |
| Sitemap URLs / HTML pages | 724 / 736 |
| New HTML pages this week | 13 |
| Commits this week | 63 |
| Directory listings live | **1** (SaaSHub, pending re-review) |
| Directory listings lost | **1** (The Next AI — 404) |
| Editorial backlinks earned | **0** |
| Directory referrals | **0** |
| Outreach emails sent (Sep 9 batch) | 61 across 58 domains |
| Outreach human replies | 6 (9.8%) — all paid placement offers |
| Editorial placements won | **0** |
| HARO opportunities pitched | **0** (of several flagged live) |
| Dead-end domains closed | 5 |
| Beehiiv subscribers | 0 (unverified — no API key) |
| Social posts published | 0 |

---

## Data Sources

- Plausible Stats API v1 (aggregate, timeseries, breakdown) — real data, token at `~/.hermes/profiles/aitools/plausible_token`
- GSC export 2026-08-22 → 2026-09-10 (see `marketing/gsc-diagnosis-2026-09-12.md`): 4,665 impressions, 6 clicks, avg position 44.3 (improving from 62)
- Git history for page/commit counts
- Himalaya over the `aitools` IMAP account: INBOX, Sent Mail, Trash, All Mail, Spam
- `admin/held-submissions.md`, `marketing/backlink-outreach-2026-09.md`, `admin/affiliate-applications-ready.md`
- HARO digests `marketing/haro-outreach/digest-2026-09-1{0,1,2,3}.json`
- Live HTTP checks (SaaSHub, The Next AI, AIAI.Tools)

---

*Report generated by Hermes Agent (aitools profile) via cron job. All traffic figures are real Plausible API data. Next report: 2026-09-21.*
