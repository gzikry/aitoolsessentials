# Pitch queue — clear this in one pass

Built 2026-10-01 from 60 unique requests across the digest history. **0 sendable**, 21 live, 35 cold (> 10 days and unpitched).

*"Sendable" is the number that matters and the one the headline used to hide: a live page is not a candidate. A row counts as sendable only when it is live, not cold, not dropped off, not already pitched, ranked above the tangential band, and has a resolved reply route (a published email, a named handle, a booking link). The other live rows are off-beat calls this queue already documents as excluded.*

**Ages are read off each request page** (`datePublished`), not off the digest text — see `marketing/haro-outreach/verified-requests.json`, refreshed by `scripts/verify_journo_requests.py`. An earlier build fell back to the digest's first-seen date and showed a 190-day-old request as 8 days old.

**No renewal signal exists on this source.** Sourcee publishes no renewal signal: on the 300 most recently indexed slugs and all 30 slugs of the live AI topic feed (checked 2026-09-19) the sitemap lastmod is byte-identical to datePublished, so 'never refreshed' is not observable and is not claimed here. Cold means old and unpitched, not provably abandoned.

**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, Qwoted and Medialyst need authenticated sessions, and Sourcee redacts the requester's own address in the request body. That is why 43 flagged opportunities produced zero pitches. Reply routes are named per row — including addresses resolved off the *publication's* own site (a byline page or an editorial contact page), which is now the strongest route class in this queue.

## Drafts that exist and were never sent

Read this before clearing the queue: four drafts are already written and none has been sent. A written draft is not progress — the send is.

**THE QUEUE IS AT ZERO SENDABLE, AND TODAY THAT IS THE TRUE NUMBER RATHER THAN A CODE ARTEFACT.** Two consecutive builds have now had to be corrected for the same defect class — a field that records something adjacent to a reply route being read as one. On 2026-09-29 the refresh script had dropped Sourcee's two own social links from its chrome filter, so a page's own chrome landed in one row's `published_links`. On 2026-10-01 the first build read the employees-conflicted-about-AI-use row as sendable because its body embeds a docs.google.com casting form, which `_sendable()` accepted as a link route. Both are fixed: a `published_links` entry now counts as a route only when it is a booking/contact link. Today the live set is 21 rows, 20 of them relevance `low`/`low-medium` with no usable route and the remaining one a comment-only DM call, so there is genuinely nothing a person can send from the live queue. Nothing was sent this run either.

**Today's drafts are `pitch-drafts-2026-10-01.md` (§1 Raconteur shadow AI, §2 Speciality Food, both paste-ready, both crossed-but-still-sendable).** The pair range re-asserted clean for the ninth consecutive day against a freshly refreshed snapshot (`updated: 2026-10-01`), so today's drafts cite the same figures as yesterday's.

**The pair range is `1.11x to 2.53x, median 1.25x` over 19 tiers across 14 tools, and it held today.** History, because every superseded value is still sitting in dated draft files and must not be reused: the range was first published as `1.21x to 2.53x, median 1.33x` (2026-09-18, sent to a real correspondent — wrong because the pair population was regex-dependent and undefined); corrected to `1.16x to 2.53x, median 1.25x` over 18 curated pairs (2026-09-21); then re-derived to **1.11x to 2.53x** when the replit-ai snapshot was refreshed (2026-09-22). From 2026-09-23 through 2026-10-01 the 19-pair set re-asserted clean against the refreshed snapshot (exit 0, no needle failures) — nine consecutive days without the figure moving, the longest such stretch since the assertion gate was added. See `data/monthly_annual_pairs.json` and `scripts/extract_monthly_annual_pairs.py`, which refuses to write the file at all unless every curated pair re-asserts against the live snapshot.

- anthropic-users-and-business-owners-customer-service-experiences — **Crossed cold 2026-09-23; now 19d old — no longer counted as sendable.** Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal hliwrites.99 (re-read verbatim off the live page 2026-09-30). Send late or record as skipped in `pitch-ledger.json`; the crossing is logged in `cold_without_a_send`.
- finops-professionals-agentic-ai-cost-overruns — **Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1. Now 24d old.** Route: LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 and still unsent — the longest-standing high-relevance request this monitor has never answered. Send it late or drop it, do not draft it a fifth time.
- fulltime-employees-shadow-ai-use-and-paying-outofpocket — **Draft ready and UNSENT — `pitch-drafts-2026-10-01.md` §1. Now 14d old, and it crossed the 10-day line on 2026-09-28 unpitched. Carried in 13 draft files.** Route: simon.chandler@raconteur.net, re-resolved off the live /contributors/simon-chandler page (HTTP 200, 154,857 bytes, data-part1/2/3 triple unchanged at simon.chandler + raconteur + net, control author /contributors/tom-dennis carries tom.dennis/raconteur/net) on 2026-09-30; the older /author/simon-chandler/ URL still 404s and must not be cited. Figures re-derived today against data/pricing_snapshots.json (`updated: 2026-09-30`): 76 tools, 40 publishing a monthly price, 31 of those at or under $25/month, median $16.50, and the pair range holding at 1.11x-2.53x over 19 tiers across 14 tools. It is the only high-relevance request this monitor has ever produced with a resolved route; the page is still HTTP 200 and the address still resolves, so a late send is still possible — what was lost is the ideal window, not the pitch.
- speciality-food-retailers-and-producers-how-theyd-spend-10k-on-t — **Draft ready and UNSENT — `pitch-drafts-2026-10-01.md` §2. Now 14d old, crossed the 10-day line on 2026-09-28 unpitched. Carried in 13 draft files.** Route: holly.shackleton@artichokehq.com (re-read off specialityfoodmagazine.com/contact 2026-09-30, HTTP 200, 59,500 bytes, byte-count unchanged, alongside five other named staff addresses). Standing constraint is stated in the draft's first line: we are not a food retailer. Its October issue window has closed, so treat this as a send-or-skip call and record the outcome in `pitch-ledger.json` rather than carrying it a fifth day.

## Sendable — pitch these (0)

Live, not cold, ranked above the tangential band, and with a reply route a human can actually use. This is the whole actionable queue.

**There is nothing to send from this queue today.** Every row that had both a relevance above the tangential band and a resolved route has now crossed the 10-day line unpitched; the live rows below are off-beat calls with no usable route. The rows that carried a finished draft are named in the section above as crossed-but-still-sendable — a late send is the only action left on them.

## Live but not sendable (21)

These pages resolve and the requests are unexpired, so they are recorded — but none has both a relevance above the tangential band and a usable route. They are listed for completeness, not as candidates: pitching any of them would mean claiming standing we do not have (see the exclusions in the newest `pitch-drafts-*.md`).

### [low-medium] AI / Workplace Culture / Shadow AI Use
- **URL:** https://www.sourcee.app/journo-request/employees-conflicted-about-ai-use-generative-ai-workplace-impact
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-01, last 2026-10-01 (1x)
- **Publication:** Independent artist/filmmaker (video project; outlet not named)
- **Reply route:** A Google Form published in the body (docs.google.com/forms/d/e/1FAIpQLSdWsFQ0q\_Mngmu7kGKnLwt4Z-Z4\_Exh5H41eqJ0rjk0t1i1Jg/viewform) or a direct message. PAGE-VERIFIED 2026-10-01: HTTP 200, email_redacted=False, emails_on_page=none, published_links=['https://docs.google.com/forms/d/e/1FAIpQLSdWsFQ0q'].  ·  _unknown — verify the route before sending_
- **Links published on the page:** https://docs.google.com/forms/d/e/1FAIpQLSdWsFQ0q
- **Angle:** Template 2 (cost optimization), only if a data contribution is welcome: offer the dated price set behind unmanaged adoption rather than a personal account. Do not claim to be a conflicted employee.

### [low-medium] Insurance / AI Adoption
- **URL:** https://www.sourcee.app/journo-request/insurance-agents-ai-use-in-personal-lines
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-29, last 2026-10-01 (3x)
- **Publication:** P&C Specialist (Financial Times) — reporter not named in the body · domain ft.com
- **Reply route:** 'Comment below or DM me' — no address published and none redacted. PAGE-VERIFIED 2026-10-01: email_redacted=False, emails_on_page=none, reply_hints=['Comment', 'DM me']. Route is the original X/LinkedIn post; we hold no handle for this reporter.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None — excluded: wants a working insurance agent's own AI usage; we have no standing and the only route is a public comment on a post we cannot identify.

### [low] Engineering Simulation / Agentic AI / Webinar Guest
- **URL:** https://www.sourcee.app/journo-request/fea-engineers-using-agentic-ai-practitioner-case-study
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-01, last 2026-10-01 (1x)
- **Publication:** Independent / Synera webinar series (author not a journalist byline)
- **Reply route:** No email, handle or link published on the page; the body invites a comment. PAGE-VERIFIED 2026-10-01: HTTP 200, email_redacted=False, emails_on_page=none, published_links=none, reply_hints=['Comment']. No route we can use.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: webinar guest call wanting an engineer's own deployment story.

### [low] AI / Family / Consumer Behaviour
- **URL:** https://www.sourcee.app/journo-request/parents-ai-acting-as-pseudoparent-in-kid-questions
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-01, last 2026-10-01 (1x)
- **Publication:** Independent writer/journalist (outlet not named in the body)
- **Reply route:** No email, handle or link published on the page; the body says 'would love to chat'. PAGE-VERIFIED 2026-10-01: HTTP 200, email_redacted=False, emails_on_page=none, published_links=none, reply_hints=none.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: personal testimony call with no spend angle.

### [low] Cybersecurity / AI Risk / Expert Availability
- **URL:** https://www.sourcee.app/journo-request/cybersecurity-expert-ai-nexus-and-security-risks
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-30, last 2026-10-01 (2x)
- **Publication:** Unnamed outlet (posted via #journorequest on X/social); no publication named in the request
- **Reply route:** Recommendations/DMs via the original #journorequest post. No email published and none redacted on the Sourcee page; no route we can use.  ·  _no — platform reply (George)_
- **Angle:** None. Off-beat: we do not hold the standing the request asks for (a cybersecurity practitioner; a US emergency physician; a booked radio segment). Do not draft.

### [low] AI / Consumer Experience
- **URL:** https://www.sourcee.app/journo-request/chatbot-users-experiences-talking-to-ai
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-01, last 2026-10-01 (1x)
- **Publication:** Independent journalist (outlet not named in the body)
- **Reply route:** DM or reply to the original post; no email published and none redacted. PAGE-VERIFIED 2026-10-01: HTTP 200, email_redacted=False, emails_on_page=none, reply_hints=['DM me']. The route is the original post, which we cannot identify.  ·  _no — platform reply (George)_
- **Angle:** None — excluded: no spend angle, no resolvable route.

### [low] AI Security / Governance / Agent Accountability
- **URL:** https://www.sourcee.app/journo-request/us-ai-security-experts-rogue-ai-agents-hitting-government-sites
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-01, last 2026-10-01 (1x)
- **Publication:** Category A publication via a PR/media-query desk (outlet not named)
- **Reply route:** DM the poster; no email or handle published on the Sourcee page. PAGE-VERIFIED 2026-10-01: HTTP 200, email_redacted=False, emails_on_page=none, published_links=none, reply_hints=['Comment'].  ·  _no — platform reply (George)_
- **Angle:** None — excluded: paid placement and wrong standing.

### [low] Real Estate / Document Workflow / Tools
- **URL:** https://www.sourcee.app/journo-request/real-estate-agents-pdf-brochures-vs-alternatives-agent-workflow
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-01, last 2026-10-01 (1x)
- **Publication:** Independent journalist (outlet not named in the body)
- **Reply route:** DM the poster, or an address Sourcee redacts; the page publishes no alternative route. PAGE-VERIFIED 2026-10-01: HTTP 200, email_redacted=True, emails_on_page=none, reply_hints=['DM me'].  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None — excluded: wrong standing (we are not a real-estate agent).

### [low] AI in Public Services / Emergency Response / Health
- **URL:** https://www.sourcee.app/journo-request/us-emergency-physicians-and-paramedics-impact-of-ai-answering-911-calls
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-30, last 2026-10-01 (2x)
- **Publication:** Unnamed US national outlet (no masthead named in the request)
- **Reply route:** The body says 'Please email [email redacted]' - Sourcee redacts the address and the page carries no alternative route. Not reachable from this monitor.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Off-beat: we do not hold the standing the request asks for (a cybersecurity practitioner; a US emergency physician; a booked radio segment). Do not draft.

### [low] AI in Hiring / Radio Feature / Audience Call-Out
- **URL:** https://www.sourcee.app/journo-request/job-seekers-and-recruiters-ai-recruitment-experiences
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-30, last 2026-10-01 (2x)
- **Publication:** 2SM Super Radio Network / 2HD Newcastle (2sm.com.au) - the Nightline programme · domain 2sm.com.au
- **Reply route:** Call-in audience format (live radio). No email, handle or link published on the page; no route we can use.  ·  _unknown — verify the route before sending_
- **Angle:** None. Off-beat: we do not hold the standing the request asks for (a cybersecurity practitioner; a US emergency physician; a booked radio segment). Do not draft.

### [low] Data Center / AI Infrastructure
- **URL:** https://www.sourcee.app/journo-request/data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-29, last 2026-10-01 (3x)
- **Publication:** Connectbase (vendor-authored request, not a journalist byline)
- **Reply route:** No route published on the page: no email, no handle, no link, and no reply hint. PAGE-VERIFIED 2026-10-01: email_redacted=False, emails_on_page=none, published_links=none.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: vendor-authored promotion with no reply route.

### [low] B2B Marketing / Positioning
- **URL:** https://www.sourcee.app/journo-request/b2b-marketing-leaders-hyperspecialization-to-outcompete-ai
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-29, last 2026-10-01 (3x)
- **Publication:** MarketingSherpa · domain marketingsherpa.com
- **Reply route:** Original X post (the page carries a t.co link to the article example); no address published. PAGE-VERIFIED 2026-10-01: email_redacted=False, emails_on_page=none, published_links=['https://t.co/Wk0GLLXXen'].  ·  _unknown — verify the route before sending_
- **Links published on the page:** https://t.co/Wk0GLLXXen
- **Angle:** None — excluded: wants a B2B company's own positioning anecdote; we are a publisher, and the request asks for nothing our price data supports.

### [low] AI Adoption / Podcast Guesting
- **URL:** https://www.sourcee.app/journo-request/ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-29, last 2026-10-01 (3x)
- **Publication:** AI Everywhere® Leaders podcast (host not named in the body)
- **Reply route:** 'Comment "guest" or send me a DM'; no address published and none redacted. PAGE-VERIFIED 2026-10-01: email_redacted=False, emails_on_page=none, reply_hints=['Comment']. Route is the original LinkedIn post, which we cannot identify from the page.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None — excluded: podcast guest call wanting an operator's own deployment story; no route resolvable off the page.

### [low] MarTech / SaaS Tool Sourcing (PR solicitation)
- **URL:** https://www.sourcee.app/journo-request/saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-09-22, last 2026-10-01 (10x)
- **Publication:** Lyza G (author field) — same #PROpportunity PR account as the two posts recorded on 2026-09-21; the page publishes linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith
- **Reply route:** DM or message; no email published. PAGE-VERIFIED 2026-10-01: HTTP 200, email_redacted=True, emails_on_page=none.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Solicitation, wrong category, no editor.

### [low] Engineering Management / AI Productivity
- **URL:** https://www.sourcee.app/journo-request/engineering-managers-measuring-engineers-when-using-ai
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-09-22, last 2026-10-01 (10x)
- **Publication:** Farhana Sethi (author field) — 'The Practical AI Manager' newsletter
- **Reply route:** Body invites replies; no email published. PAGE-VERIFIED 2026-10-01: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded. No spend angle.

### [low] AI Hardware / Creator Content
- **URL:** https://www.sourcee.app/journo-request/ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-09-22, last 2026-10-01 (10x)
- **Publication:** Riley Brown (author field) — video series
- **Reply route:** Body invites contact; no email published. PAGE-VERIFIED 2026-10-01: HTTP 200, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded.

### [low] Sales Tech / SaaS Tool Sourcing (PR solicitation)
- **URL:** https://www.sourcee.app/journo-request/sales-enablement-saas-tools-proposal-and-deck-engagement-tracking
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-09-21, last 2026-10-01 (11x)
- **Publication:** Lyza G (author field) — a #PROpportunity post; the page publishes linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith as the reply handles
- **Reply route:** Reply/DM — the body says 'Drop your tool name … below or in DMs'; the page publishes linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith. No email. PAGE-VERIFIED 2026-10-01: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None - excluded. Wrong tool category, wrong standing, and it is a solicitation rather than a journalist request.

### [low] Founders / Podcast Interviews
- **URL:** https://www.sourcee.app/journo-request/founders-and-leaders-mindsets-and-milestones
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-09-21, last 2026-10-01 (11x)
- **Publication:** Conor Burchall (author field) — 'Rational Exchange' podcast
- **Reply route:** No route published on the page. PAGE-VERIFIED 2026-10-01: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded.

### [low] AI Hiring Tools / Recruitment Tech
- **URL:** https://www.sourcee.app/journo-request/london-businesses-stopped-using-ai-hiring-tools
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-09-22, last 2026-10-01 (10x)
- **Publication:** Meghan Owen (author field) — BBC (domain=bbc.co.uk) · domain bbc.co.uk
- **Reply route:** Body: 'please email [email redacted]'. Sourcee redacts the address and the page publishes no alternative route. PAGE-VERIFIED 2026-10-01: HTTP 200, email_redacted=True, emails_on_page=none.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Wrong standing (we are not a London employer) and no spend angle.

### [low] Podcast Guest Booking
- **URL:** https://www.sourcee.app/journo-request/creative-industry-professionals-podcast-on-ai-impact
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-09-22, last 2026-10-01 (10x)
- **Publication:** Stefanie Calleja-Gera (author field) — 'Between the Briefs' podcast
- **Reply route:** Body links two lnkd.in shorteners; no email published. PAGE-VERIFIED 2026-10-01: HTTP 200, emails_on_page=none.  ·  _no — published booking link https://lnkd.in/e-ChShR4 (George)_
- **Links published on the page:** https://lnkd.in/e-ChShR4, https://lnkd.in/erVuW5q5
- **Angle:** None - excluded.

### [low] AI Attitudes / Personal Testimony
- **URL:** https://www.sourcee.app/journo-request/former-ai-skeptics-changed-views-on-ai-impact
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-09-22, last 2026-10-01 (10x)
- **Publication:** Madison Mills (author field)
- **Reply route:** Body: 'DM me here or on Signal at madymills.21'. A concrete handle, but there is nothing on-beat to send it. PAGE-VERIFIED 2026-10-01: HTTP 200, emails_on_page=none.  ·  _no — platform reply (George)_
- **Angle:** None - excluded. Off-beat; would require inventing standing.

## Cold — only if you have a reason

Older than the 10-day line and never pitched. Not provably abandoned — no renewal signal exists on this source — but every one of these has already passed an ideal send window.

- [high] 14d old — https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
- [high] 24d old — https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
- [high] 26d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-ai-governance-and-agent-sprawl
- [high] 26d old — https://www.sourcee.app/journo-request/scientists-phd-students-and-postdocs-paying-for-ai-subscriptions
- [high] 72d old — https://www.sourcee.app/journo-request/business-and-technology-leaders-tech-budget-priorities-amid-volatility
- [high] 132d old — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [medium-high] 19d old — https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
- [medium-high] 24d old — https://www.sourcee.app/journo-request/uk-managers-cracked-down-on-gen-z-ai-overuse
- [medium-high] 198d old — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium] 20d old — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [medium] 24d old — https://www.sourcee.app/journo-request/ai-agents-making-money-2026-sales-and-leadgen-workflow-ops
- [medium] 24d old — https://www.sourcee.app/journo-request/ai-startups-workplace-fraud-detection-expenses-time-theft
- [medium] 24d old — https://www.sourcee.app/journo-request/marketing-and-content-leaders-aiassisted-work-review-process
- [medium] 28d old — https://www.sourcee.app/journo-request/ceos-ai-impact-on-ops-culture-and-commercial-strategy
- [medium] 38d old — https://www.sourcee.app/journo-request/uk-finance-risk-and-regulatory-leaders-ai-explainability-risks
- [medium] 205d old — https://www.sourcee.app/journo-request/sme-owners-operational-challenges-for-ai-solutions-case-study
- [medium-low] 12d old — https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business
- [low-medium] 14d old — https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
- [low-medium] 15d old — https://www.sourcee.app/journo-request/us-founders-calls-to-slow-ai-development-impact-on-companies
- [medium-low] 21d old — https://www.sourcee.app/journo-request/tech-policy-experts-california-ai-audit-bills-impact-cios
- [low-medium] 40d old — https://www.sourcee.app/journo-request/ai-project-builders-youtube-finance-and-lifestyle-channel-feature
- [low] 11d old — https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- [low] 11d old — https://www.sourcee.app/journo-request/employers-and-recruiters-over-50s-adapting-to-ai
- [low] 11d old — https://www.sourcee.app/journo-request/data-center-professionals-podcast-guest-ai-and-hyperscale-trends
- [low] 11d old — https://www.sourcee.app/journo-request/patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges
- [low] 11d old — https://www.sourcee.app/journo-request/ml-researchers-continuous-learning-fast-weights-and-adapters
- [low] 11d old — https://www.sourcee.app/journo-request/founders-55-latelife-entrepreneurship-series-1
- [low] 11d old — https://www.sourcee.app/journo-request/founders-and-entrepreneurs-and-musicians-podcast-guests
- [low] 12d old — https://www.sourcee.app/journo-request/ai-alignment-researchers-humanai-mutual-understanding
- [low] 13d old — https://www.sourcee.app/journo-request/companies-that-stopped-emailing-pdfs-new-tools-and-transition
- [low] 14d old — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 14d old — https://www.sourcee.app/journo-request/gen-z-ai-data-annotators-work-experience-and-income-impact
- [low] 14d old — https://www.sourcee.app/journo-request/ai-automation-experts-speakers-on-marketing-sales-operations-gains
- [low] 14d old — https://www.sourcee.app/journo-request/ecommerce-marketers-transparency-in-ai-recommendations-and-conversion
- [low] 15d old — https://www.sourcee.app/journo-request/cybersecurity-companies-and-experts-ai-scams-and-consumer-safety

---

## Clearing the queue

After sending, record it so the row does not reappear:

```json
{"pitched": {"<url>": "2026-09-15"}, "skipped": {"<url>": "reason"}}
```

Ledger: `marketing/haro-outreach/pitch-ledger.json`
