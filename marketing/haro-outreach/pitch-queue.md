# Pitch queue — clear this in one pass

Built 2026-09-28 from 47 unique requests across the digest history. **0 sendable**, 18 live, 25 cold (> 10 days and unpitched).

*"Sendable" is the number that matters and the one the headline used to hide: a live page is not a candidate. A row counts as sendable only when it is live, not cold, not dropped off, not already pitched, ranked above the tangential band, and has a resolved reply route (a published email, a named handle, a booking link). The other live rows are off-beat calls this queue already documents as excluded.*

**Ages are read off each request page** (`datePublished`), not off the digest text — see `marketing/haro-outreach/verified-requests.json`, refreshed by `scripts/verify_journo_requests.py`. An earlier build fell back to the digest's first-seen date and showed a 190-day-old request as 8 days old.

**No renewal signal exists on this source.** Sourcee publishes no renewal signal: on the 300 most recently indexed slugs and all 30 slugs of the live AI topic feed (checked 2026-09-19) the sitemap lastmod is byte-identical to datePublished, so 'never refreshed' is not observable and is not claimed here. Cold means old and unpitched, not provably abandoned.

**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, Qwoted and Medialyst need authenticated sessions, and Sourcee redacts the requester's own address in the request body. That is why 43 flagged opportunities produced zero pitches. Reply routes are named per row — including addresses resolved off the *publication's* own site (a byline page or an editorial contact page), which is now the strongest route class in this queue.

## Drafts that exist and were never sent

Read this before clearing the queue: four drafts are already written and none has been sent. A written draft is not progress — the send is.

**THE QUEUE IS AT ZERO SENDABLE, AND IT GOT THERE BY LOSING BOTH ITS DRAFTS.** Both rows that carried a finished draft and a resolved route crossed the 10-day line on 2026-09-28, unpitched: the Raconteur shadow-AI request (11d, high relevance, draft unsent for TEN consecutive runs) and the Speciality Food request (11d, draft unsent since 2026-09-19). The live count fell 24 to 18 and the sendable count fell 2 to 0. Neither draft is void — both pages are still HTTP 200 and both routes were re-resolved against the live pages again today, so a late send is still possible. What was lost is the ideal window, not the pitch.

**Today's drafts are `pitch-drafts-2026-09-28.md` (§1 shadow AI, §2 Speciality Food, both paste-ready and both marked crossed-but-still-sendable).** The pair range re-asserted clean for the sixth consecutive day against a freshly refreshed snapshot (`updated: 2026-09-28`), so today's drafts cite the same figures as yesterday's.

**The pair range is `1.11x to 2.53x, median 1.25x` over 19 tiers across 14 tools, and it held today.** History, because every superseded value is still sitting in dated draft files and must not be reused: the range was first published as `1.21x to 2.53x, median 1.33x` (2026-09-18, sent to a real correspondent — wrong because the pair population was regex-dependent and undefined); corrected to `1.16x to 2.53x, median 1.25x` over 18 curated pairs (2026-09-21); then re-derived to **1.11x to 2.53x** when the replit-ai snapshot was refreshed (2026-09-22). From 2026-09-23 through 2026-09-28 the 19-pair set re-asserted clean against the refreshed snapshot (exit 0, no needle failures) — six consecutive days without the figure moving, the longest such stretch since the assertion gate was added. See `data/monthly_annual_pairs.json` and `scripts/extract_monthly_annual_pairs.py`, which refuses to write the file at all unless every curated pair re-asserts against the live snapshot.

- anthropic-users-and-business-owners-customer-service-experiences — **CROSSED COLD 2026-09-23 at 11 days, now 16 — no longer counted as sendable.** Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal hliwrites.99 (re-read verbatim off the live page, still published 2026-09-28). It was the queue's #2 and sendable on four consecutive runs. Send late or record as skipped in pitch-ledger.json; the crossing is logged in `cold_without_a_send`.
- finops-professionals-agentic-ai-cost-overruns — **Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1.** Route: LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 (now 21 days) and still unsent — the longest-standing high-relevance request this monitor has never answered. Send it late or drop it, do not draft it a fifth time.
- fulltime-employees-shadow-ai-use-and-paying-outofpocket — **CROSSED COLD 2026-09-28 at 11 days, draft ready and UNSENT — send it late: `pitch-drafts-2026-09-28.md` §1.** Route: simon.chandler@raconteur.net, re-resolved off the live /contributors/simon-chandler page (HTTP 200, 154,797 bytes, triple unchanged, control author checked) on 2026-09-28; the older /author/simon-chandler/ URL still 404s and must not be cited. Figures re-derived today against data/pricing_snapshots.json (`updated: 2026-09-28`): 76 tools, 40 publishing a monthly price, 31 of those at or under $25/month, median $16.50, and the pair range holding at 1.11x-2.53x over 19 tiers across 14 tools. Written and unsent for TEN consecutive runs, and it crossed unpitched on 2026-09-28 — the first high-relevance request this queue has lost to the cold line with a paste-ready draft sitting ready. The page is still HTTP 200 and the address still resolves, so a late send is still possible; what was lost is the ideal window, not the pitch.
- speciality-food-retailers-and-producers-how-theyd-spend-10k-on-t — **CROSSED COLD 2026-09-28 at 11 days, draft ready and UNSENT — send or skip: `pitch-drafts-2026-09-28.md` §2.** Route: holly.shackleton@artichokehq.com (re-read off specialityfoodmagazine.com/contact 2026-09-28, HTTP 200, 59,500 bytes, alongside five other named staff addresses). Standing constraint is stated in the draft's first line: we are not a food retailer. 11 days old and cold as of today; its October issue window has almost certainly closed, so treat this as a send-or-skip call and record the outcome in pitch-ledger.json.

## Sendable — pitch these (0)

Live, not cold, ranked above the tangential band, and with a reply route a human can actually use. This is the whole actionable queue.

**There is nothing to send from this queue today.** Every row that had both a relevance above the tangential band and a resolved route has now crossed the 10-day line unpitched; the live rows below are off-beat calls with no usable route. The rows that carried a finished draft are named in the section above as crossed-but-still-sendable — a late send is the only action left on them.

## Live but not sendable (18)

These pages resolve and the requests are unexpired, so they are recorded — but none has both a relevance above the tangential band and a usable route. They are listed for completeness, not as candidates: pitching any of them would mean claiming standing we do not have (see the exclusions in the newest `pitch-drafts-*.md`).

### [medium-low] AI / Founders / Deliberate AI Reduction
- **URL:** https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-09-20, last 2026-09-28 (9x)
- **Publication:** Forbes - author named in the page's own author field: Jodie Cook · domain forbes.com
- **Reply route:** Comment on the original post - the body is explicit: 'Please only answer as a comment on this post. Do not email or DM me because they won't be used.' No email published. PAGE-VERIFIED 2026-09-20: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None - the reply route is a public comment requiring a named founder's firsthand account, which we do not have.

### [low] MarTech / SaaS Tool Sourcing (PR solicitation)
- **URL:** https://www.sourcee.app/journo-request/saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-22, last 2026-09-28 (7x)
- **Publication:** Lyza G (author field) — same #PROpportunity PR account as the two posts recorded on 2026-09-21; the page publishes linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith
- **Reply route:** DM or message; no email published. PAGE-VERIFIED 2026-09-22: HTTP 200, email_redacted=True, emails_on_page=none.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Solicitation, wrong category, no editor.

### [low] Engineering Management / AI Productivity
- **URL:** https://www.sourcee.app/journo-request/engineering-managers-measuring-engineers-when-using-ai
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-22, last 2026-09-28 (7x)
- **Publication:** Farhana Sethi (author field) — 'The Practical AI Manager' newsletter
- **Reply route:** Body invites replies; no email published. PAGE-VERIFIED 2026-09-22: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded. No spend angle.

### [low] AI Hardware / Creator Content
- **URL:** https://www.sourcee.app/journo-request/ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-22, last 2026-09-28 (7x)
- **Publication:** Riley Brown (author field) — video series
- **Reply route:** Body invites contact; no email published. PAGE-VERIFIED 2026-09-22: HTTP 200, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded.

### [low] Sales Tech / SaaS Tool Sourcing (PR solicitation)
- **URL:** https://www.sourcee.app/journo-request/sales-enablement-saas-tools-proposal-and-deck-engagement-tracking
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-21, last 2026-09-28 (8x)
- **Publication:** Lyza G (author field) — a #PROpportunity post; the page publishes linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith as the reply handles
- **Reply route:** Reply/DM — the body says 'Drop your tool name … below or in DMs'; the page publishes linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith. No email. PAGE-VERIFIED 2026-09-21: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None - excluded. Wrong tool category, wrong standing, and it is a solicitation rather than a journalist request.

### [low] Founders / Podcast Interviews
- **URL:** https://www.sourcee.app/journo-request/founders-and-leaders-mindsets-and-milestones
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-21, last 2026-09-28 (8x)
- **Publication:** Conor Burchall (author field) — 'Rational Exchange' podcast
- **Reply route:** No route published on the page. PAGE-VERIFIED 2026-09-21: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded.

### [low] AI Hiring Tools / Recruitment Tech
- **URL:** https://www.sourcee.app/journo-request/london-businesses-stopped-using-ai-hiring-tools
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-22, last 2026-09-28 (7x)
- **Publication:** Meghan Owen (author field) — BBC (domain=bbc.co.uk) · domain bbc.co.uk
- **Reply route:** Body: 'please email [email redacted]'. Sourcee redacts the address and the page publishes no alternative route. PAGE-VERIFIED 2026-09-22: HTTP 200, email_redacted=True, emails_on_page=none.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Wrong standing (we are not a London employer) and no spend angle.

### [low] Podcast Guest Booking
- **URL:** https://www.sourcee.app/journo-request/creative-industry-professionals-podcast-on-ai-impact
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-22, last 2026-09-28 (7x)
- **Publication:** Stefanie Calleja-Gera (author field) — 'Between the Briefs' podcast
- **Reply route:** Body links two lnkd.in shorteners; no email published. PAGE-VERIFIED 2026-09-22: HTTP 200, emails_on_page=none.  ·  _no — published booking link https://lnkd.in/e-ChShR4 (George)_
- **Links published on the page:** https://lnkd.in/e-ChShR4, https://lnkd.in/erVuW5q5
- **Angle:** None - excluded.

### [low] AI Attitudes / Personal Testimony
- **URL:** https://www.sourcee.app/journo-request/former-ai-skeptics-changed-views-on-ai-impact
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-22, last 2026-09-28 (7x)
- **Publication:** Madison Mills (author field)
- **Reply route:** Body: 'DM me here or on Signal at madymills.21'. A concrete handle, but there is nothing on-beat to send it. PAGE-VERIFIED 2026-09-22: HTTP 200, emails_on_page=none.  ·  _no — platform reply (George)_
- **Angle:** None - excluded. Off-beat; would require inventing standing.

### [low] AI / Autonomous Weapons / Investigative
- **URL:** https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-09-20, last 2026-09-28 (9x)
- **Publication:** The Lever - author field 'badplacetimes', journalist self-identified as Craig · domain thelever.co
- **Reply route:** Signal 972-408-7275, published verbatim in the request body. PAGE-VERIFIED 2026-09-20: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded, wrong standing.

### [low] AI / Workforce / Age & Adaptation
- **URL:** https://www.sourcee.app/journo-request/employers-and-recruiters-over-50s-adapting-to-ai
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-09-20, last 2026-09-28 (9x)
- **Publication:** Independent (Ovee, 'Beyond the CV' interviews) - author field: Peter Tsakissiris
- **Reply route:** No email, DM handle or link published on the page. PAGE-VERIFIED 2026-09-20: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _no — platform reply (George)_
- **Angle:** None - excluded.

### [low] Data Centre / Podcast Guest Booking
- **URL:** https://www.sourcee.app/journo-request/data-center-professionals-podcast-guest-ai-and-hyperscale-trends
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-09-20, last 2026-09-28 (9x)
- **Publication:** Independent podcast ('The Strategic Podcast') - author field: Todd T. Stone
- **Reply route:** No route published on the Sourcee page; the body solicits guest and sponsor enquiries. PAGE-VERIFIED 2026-09-20: HTTP 200, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded, and it is a booking solicitation rather than a request.

### [low] US Healthcare Billing / Consumer Costs
- **URL:** https://www.sourcee.app/journo-request/patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-09-20, last 2026-09-28 (9x)
- **Publication:** Independent journalist - author field: Tanushka Dutta
- **Reply route:** DM the author; no email published. PAGE-VERIFIED 2026-09-20: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None - excluded, wrong subject.

### [low] ML Research / Methods
- **URL:** https://www.sourcee.app/journo-request/ml-researchers-continuous-learning-fast-weights-and-adapters
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-09-21, last 2026-09-28 (8x)
- **Publication:** Chris (author field) — ML research 'DevDay wish list' post
- **Reply route:** No route published on the page. PAGE-VERIFIED 2026-09-21: HTTP 200, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded.

### [low] Founders / Age & Entrepreneurship
- **URL:** https://www.sourcee.app/journo-request/founders-55-latelife-entrepreneurship-series-1
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-09-21, last 2026-09-28 (8x)
- **Publication:** Marcelo Salup (author field) — article series
- **Reply route:** Body links a bit.ly shortener and publishes no email. PAGE-VERIFIED 2026-09-21: HTTP 200, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Links published on the page:** https://bit.ly/3YhUyvk
- **Angle:** None - excluded.

### [low] Podcast Guest Booking
- **URL:** https://www.sourcee.app/journo-request/founders-and-entrepreneurs-and-musicians-podcast-guests
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-09-21, last 2026-09-28 (8x)
- **Publication:** Coral Rose Official (author field) — asks an AI agent to make the connections
- **Reply route:** None — the page is an AI-agent prompt, no human route. PAGE-VERIFIED 2026-09-21: HTTP 200, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded.

### [low] AI / Alignment / Philosophy
- **URL:** https://www.sourcee.app/journo-request/ai-alignment-researchers-humanai-mutual-understanding
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-09-20, last 2026-09-28 (9x)
- **Publication:** Independent (framework author, LinkedIn long-form) - author field: Zamo Dana
- **Reply route:** No email or handle published on the page. PAGE-VERIFIED 2026-09-20: HTTP 200, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded.

### [low] Workflow Tools / Document Handling
- **URL:** https://www.sourcee.app/journo-request/companies-that-stopped-emailing-pdfs-new-tools-and-transition
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-09-21, last 2026-09-28 (8x)
- **Publication:** Lyza G (author field) — same PR account as the sales-enablement post
- **Reply route:** Reply or DM; no email published. PAGE-VERIFIED 2026-09-21: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _no — platform reply (George)_
- **Angle:** None - excluded, off-beat.

## Cold — only if you have a reason

Older than the 10-day line and never pitched. Not provably abandoned — no renewal signal exists on this source — but every one of these has already passed an ideal send window.

- [high] 11d old — https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
- [high] 21d old — https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
- [high] 23d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-ai-governance-and-agent-sprawl
- [high] 23d old — https://www.sourcee.app/journo-request/scientists-phd-students-and-postdocs-paying-for-ai-subscriptions
- [high] 69d old — https://www.sourcee.app/journo-request/business-and-technology-leaders-tech-budget-priorities-amid-volatility
- [high] 129d old — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [medium-high] 16d old — https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
- [medium-high] 21d old — https://www.sourcee.app/journo-request/uk-managers-cracked-down-on-gen-z-ai-overuse
- [medium-high] 195d old — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium] 17d old — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [medium] 21d old — https://www.sourcee.app/journo-request/ai-agents-making-money-2026-sales-and-leadgen-workflow-ops
- [medium] 21d old — https://www.sourcee.app/journo-request/ai-startups-workplace-fraud-detection-expenses-time-theft
- [medium] 21d old — https://www.sourcee.app/journo-request/marketing-and-content-leaders-aiassisted-work-review-process
- [medium] 25d old — https://www.sourcee.app/journo-request/ceos-ai-impact-on-ops-culture-and-commercial-strategy
- [medium] 35d old — https://www.sourcee.app/journo-request/uk-finance-risk-and-regulatory-leaders-ai-explainability-risks
- [medium] 202d old — https://www.sourcee.app/journo-request/sme-owners-operational-challenges-for-ai-solutions-case-study
- [low-medium] 11d old — https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
- [low-medium] 12d old — https://www.sourcee.app/journo-request/us-founders-calls-to-slow-ai-development-impact-on-companies
- [medium-low] 18d old — https://www.sourcee.app/journo-request/tech-policy-experts-california-ai-audit-bills-impact-cios
- [low-medium] 37d old — https://www.sourcee.app/journo-request/ai-project-builders-youtube-finance-and-lifestyle-channel-feature
- [low] 11d old — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 11d old — https://www.sourcee.app/journo-request/gen-z-ai-data-annotators-work-experience-and-income-impact
- [low] 11d old — https://www.sourcee.app/journo-request/ai-automation-experts-speakers-on-marketing-sales-operations-gains
- [low] 11d old — https://www.sourcee.app/journo-request/ecommerce-marketers-transparency-in-ai-recommendations-and-conversion
- [low] 12d old — https://www.sourcee.app/journo-request/cybersecurity-companies-and-experts-ai-scams-and-consumer-safety

---

## Clearing the queue

After sending, record it so the row does not reappear:

```json
{"pitched": {"<url>": "2026-09-15"}, "skipped": {"<url>": "reason"}}
```

Ledger: `marketing/haro-outreach/pitch-ledger.json`
