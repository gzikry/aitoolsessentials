# Weekly Traffic Report — AIToolsEssentials

**Week of:** 2026-09-01 → 2026-09-07  
**Report date:** 2026-09-07  
**Site:** https://aitoolsessentials.com  
**Analytics:** Plausible (plausible.io, domain: aitoolsessentials.com)  

---

## 1. Traffic Sources

### Plausible Access

Plausible is installed via `js/analytics.js` (loads `plausible.io/js/script.js` with `data-domain=aitoolsessentials.com`). The stats dashboard at `plausible.io/aitoolsessentials.com` and the public API endpoints are **not publicly accessible** — they require authentication or an API key, which is not configured in this environment. The last known Plausible snapshot (from memory, 2026-09-04) was **~39 visitors / 112 pageviews over trailing 30 days** (ending Sep 2). This report uses that as the baseline and supplements with activity-based estimation.

### Estimated Traffic (trailing 7 days: Sep 1–7)

| Source | Est. Visitors | Notes |
|---|---|---|
| **Organic search** | 10–15 | GSC sitemap submitted on property-owner account; impressions not expected immediately. Site:search confirms Google has indexed homepage, workflows, deals, weekly, categories, legal, badges, articles hub, evidence ledger, alternatives hub. No GSC impression data available yet. |
| **Directories** | 0–3 | SaaSHub listing live but "Pending approval" (verified via web extract — page exists at saashub.com/aitoolsessentials, 0 reviews). The Next AI submission approved Sep 3 but no evidence of a live tool page found via search. AIAI.Tools confirmation shown but not yet indexed by Google. |
| **Email outreach** | 0 | 10 pitch emails sent Sep 3 (TLDR AI, The Rundown AI, Ben's Bites, The Neuron, ToolChase, ToolRadar, Last Week in AI, Changelog, infoDOCKET, AIToolsRecap). **Zero responses received** as of Sep 7. |
| **Social (X/LinkedIn)** | 0–2 | 5 social post templates drafted (marketing/social-posts-2026-08.md). No evidence of active posting this week. |
| **Direct/referral** | 2–5 | Stack Audit launched Sep 3 (/stack-audit.html); homepage redesign shipped Sep 4–6 (PRs #16–#24). Possible direct visits from Whop forum, GitHub PRs, and George's network. |
| **Estimated total** | **12–25** | Low but consistent with pre-GSC-impressions phase. The 30d baseline of ~39 visitors/112 PV suggests ~7–10 visitors/week organically; new content + Stack Audit launch may add a small bump. |

### Traffic Trend Context

- **30d baseline (ending Sep 2):** ~39 visitors, 112 pageviews (from memory note, 2026-09-04)
- **Previous 30d (ending Sep 1):** 36 visitors, 105 pageviews (from memory note, 2026-09-02)
- **Trajectory:** Flat to slight upward. Site is in the pre-indexation phase — GSC sitemap submitted but impressions haven't materialized. Traffic is expected to remain low until Google begins surfacing pages in search results.

---

## 2. Top Performing Pages

Plausible page-level data is not accessible without API auth. Based on site structure, search visibility, and content launch sequence, the likely top pages are:

| Page | URL | Why it likely performs |
|---|---|---|
| Homepage | `/` | Primary landing; redesigned 3× this week (PRs #16, #19, #20, #22, #24). Stack Audit CTA is now primary. |
| Stack Audit | `/stack-audit.html` | New interactive tool launched Sep 3 (PR #11→#16). Primary conversion funnel entry per Path A. |
| Pricing Watch | `/pricing-watch/` | Core linkable asset; referenced in all outreach emails. |
| Tools directory | `/tools/index.html` | 75 tool review pages; hub for organic discovery. |
| Articles hub | `/articles` | 173 articles; high topical coverage for long-tail SEO. |
| Premium | `/premium/` | Redesigned Sep 3–4 (PRs #12–#16). $12/mo Whop membership. |
| Newsletter | `/newsletter/` | Keep/Cut Weekly; Issue 1 live at `/newsletter/2026-w35.html`. 0 Beehiiv subscribers. |
| Alternatives hub | `/alternatives/index.html` | 20+ alternative pages; strong SEO structure for "X alternatives" queries. |

### Site Volume (as of Sep 7)

| Content type | Count |
|---|---|
| Sitemap URLs | 715 |
| Tool review pages | 75 |
| Articles | 173 |
| Comparisons | 192 |
| How-to guides | 10 |
| Hardware compatibility | 6 |
| Premium library pages | 8 |
| **New HTML pages this week** | **43** |

---

## 3. New Backlinks Earned This Week

| Source | URL | Status | Type |
|---|---|---|---|
| SaaSHub | saashub.com/aitoolsessentials | **Live but pending approval** — page exists, 0 reviews, "Pending approval" banner shown. Listed in Finance > Subscriptions > Subscription Tracking (wrong category — should be AI Tools). | Directory listing (potential dofollow) |
| The Next AI | thenextai.com/ai-tools/aitoolsessentials/ | **Submitted & approved Sep 3** — but web extract returned HTTP error; live page not confirmed via search. May be indexed but not yet appearing in results. | Directory listing (dofollow claimed) |
| AIAI.Tools | aiai.tools | **Confirmation shown Sep 3** ("Thanks for contribution") — not yet visible in search results. | Directory listing |

**No editorial backlinks, newsletter mentions, or organic citations found this week.** All 10 outreach emails went unanswered.

### Backlink Audit Notes

- The SaaSHub listing is categorized under "Finance > Subscriptions > Subscription Tracking" rather than "AI Tools" — this may limit referral relevance. The submission used categories AI, AI Tools, Software Directory, but SaaSHub appears to have placed it in Finance.
- No third-party sites found linking to aitoolsessentials.com via search (query: `"aitoolsessentials" -site:aitoolsessentials.com` returned no external mentions).
- The `/badges/` page exists to encourage vendor backlinks (reviewed tools can embed badges linking back to their review pages). No badge adoptions observed.

---

## 4. Directory Submissions Status

| Directory | Status | Date | Notes |
|---|---|---|---|
| **SaaSHub** | Live, pending approval | Aug 31 | Page exists at saashub.com/aitoolsessentials. 0 reviews. "Pending approval" banner. Up to 32-day approval window. |
| **The Next AI** | Approved | Sep 3 | Free, no account. Dofollow claimed. Live page not confirmed via search yet. 120k monthly visitors claimed. |
| **AIAI.Tools** | Confirmation received | Sep 3 | Free, no account. Tally form. Not yet indexed by Google. |
| **AlternativeTo** | Blocked — needs George's account | Sep 3 | Form requires signed-in user. George hasn't created account yet. |
| **Uneed** | Blocked — needs George's account | Sep 3 | Preview works without account; saving requires signup. |
| **ToolScout** | Blocked — needs account | Sep 3 | Requires sign-in. |
| **AIToolsDirectory.com** | Incomplete — Paperform issue | Sep 3 | YES/NO ad-space question uses SPAN elements, not buttons. Needs manual completion or George's approval of upsell. |
| **PoweredByAI** | Blocked — React Select issue | Sep 3 | Category/subcategory are React Select components; automation approach needed. |
| **Dofollow.Tools** | Incomplete — AI auto-fill failed | Sep 3 | Multi-step form; AI button silently failed. |
| **Futuretools.io** | Blocked — 404 | Sep 3 | Submit page returns 404. |
| **Toolify** | Paid only ($99) | Aug 31 | No free tier. Skip unless George approves spend. |
| **TopAI.tools** | Paid only ($47) | Aug 31 | Fast Track only. Skip unless George approves. |
| **AIXploria** | Paid only ($79–$279) | Aug 31 | No free tier on live form. |
| **TAAFT** | Paid ($49+) | Aug 31 | Held. |
| **Futurepedia** | Paid ($247+) | Aug 31 | Hold until ~5K monthly visits. |

**Summary:** 3 submitted (1 live-pending, 2 confirmed but not indexed), 3 blocked on George's accounts, 4 blocked on form automation issues, 5 paid-only (skip).

---

## 5. Email Outreach Responses

### Outreach Sent (Sep 3)

| Outlet | Type | Contact | Response |
|---|---|---|---|
| TLDR AI | Newsletter | dan@tldr.tech | **No response** |
| The Rundown AI | Newsletter | support@therundown.ai | **No response** |
| Ben's Bites | Newsletter | team@bensbites.com | **No response** |
| The Neuron | Newsletter | team@theneurondaily.com | **No response** |
| ToolChase | Blog | hello@toolchase.com | **No response** |
| ToolRadar | Blog | contact@aitoolradar.io | **No response** |
| Last Week in AI | Podcast | contact@lastweekinai.com | **No response** |
| Changelog / Practical AI | Podcast | editors@changelog.com | **No response** |
| infoDOCKET | Blog | gprice@gmail.com | **No response** |
| AIToolsRecap | Blog | editor@aitoolsrecap.com | **No response** |

**Response rate: 0/10 (0%)**. All pitches offered AIToolsEssentials as a resource (Pricing Watch, verified pricing snapshots) with a "no strings" framing. No bounces reported, but no replies either. Typical cold outreach response rates are 5–10% after follow-ups; a single send without follow-up is expected to underperform.

### HARO / Journalist Source Queries

Daily HARO digests run Sep 4–6. **Zero relevant journalist queries found** across all checked platforms (HARO, Connectively/Featured.com, Qwoted, Source of Sources, JournoFinder, Medialyst, X #journorequest, general web search). All major source-request platforms now require login/registration to view queries. HARO is email-digest-only. No pitches sent via HARO this week.

### Prior Outreach (from memory)

Emails also sent Aug 31 to: dan@tldr.tech, support@therundown.ai, cndls@georgetown.edu, asklib@duke.edu. No responses from those either.

---

## 6. Recommendations for Next Week

### Immediate (Sep 8–14)

1. **Send follow-up emails to the 10 newsletter/blog/podcast contacts.** Cold outreach without a follow-up gets ~1–3% response. A single polite follow-up ("bumping this in case it got buried") can lift response rates to 5–8%. Prioritize TLDR AI, The Rundown AI, and Ben's Bites (highest audience overlap).

2. **Fix the SaaSHub category.** The listing is in Finance > Subscriptions > Subscription Tracking. It should be in AI Tools / Software Directory. Check if SaaSHub allows category editing without an account, or if George needs to claim the listing first.

3. **Verify The Next AI and AIAI.Tools live pages.** Web extract returned errors/empty for both. Use browser to confirm the tool pages are actually live and indexable. If The Next AI page exists, check for dofollow backlink attribute.

4. **George-only: create accounts on AlternativeTo, Uneed, and ToolScout.** These are the highest-DA free directories that require signup. Once George confirms accounts, the agent can complete submissions immediately. AlternativeTo (DA ~90) is the highest-value free directory remaining.

5. **Post the 5 social content templates to X and LinkedIn.** The templates in `marketing/social-posts-2026-08.md` are ready. They target commercial-intent pages (cursor-vs-copilot, meeting notes, stack audit, newsletter, subscription overlap). No social posting has happened this week.

### Content & SEO

6. **Monitor GSC impressions.** The sitemap (715 URLs) was submitted on the property-owner account. Once impressions begin appearing, identify which pages/queries Google is testing and double down on those topics. Until then, do not add more pages — the instruction from memory is "no more pages until GSC impressions."

7. **Build the Stack Audit conversion funnel.** Path A is locked (Stack Audit front door → optional Whop paid outcome). The kill metrics are 200 audits / 10 trials / 3 paid. Start tracking Stack Audit completions via Plausible custom events (the analytics.js already fires `stack_audit` conversion events). Need Plausible API access to read these.

8. **Pitch the coding-assistant quiz as a linkable asset.** `marketing/linkable-assets/coding-assistant-quiz.html` exists but hasn't been promoted. Pitch it to developer-focused newsletters (Bytes, JavaScript Weekly, TLDR Web Dev) as a free interactive tool.

### Directory automation fixes

9. **Solve the React Select problem for PoweredByAI.** The pattern (type into search input → wait for menu portal → click option by text) is documented in the outreach file. Apply it to complete the PoweredByAI submission.

10. **Re-attempt AIToolsDirectory.com with click_at_xy on Paperform SPAN elements.** The workaround is documented; it just needs execution. George may need to approve the ad-space upsell answer (answer NO).

### Infrastructure

11. **Get Plausible API access.** Weekly traffic reports are currently estimated. Configure a Plausible API token in `.env` (George-owned credential) so future reports can pull actual visitor/pageview/top-pages/bounce-rate data programmatically.

---

## Summary Metrics

| Metric | Value |
|---|---|
| Estimated weekly visitors | 12–25 |
| 30d baseline visitors (ending Sep 2) | ~39 |
| 30d baseline pageviews (ending Sep 2) | ~112 |
| Sitemap URLs | 715 |
| New pages this week | 43 |
| PRs merged this week | 10 |
| Directory submissions live | 1 (SaaSHub, pending) |
| Directory submissions confirmed | 2 (The Next AI, AIAI.Tools) |
| Backlinks earned this week | 0 confirmed (3 pending) |
| Outreach emails sent | 10 |
| Outreach responses | 0 |
| HARO queries found | 0 |
| Beehiiv subscribers | 0 |
| Social posts published | 0 |

---

*Report generated by Hermes Agent (aitools profile) via cron job. Plausible data not accessible — estimates based on prior snapshots, site activity, and outreach logs. Next report: 2026-09-14.*