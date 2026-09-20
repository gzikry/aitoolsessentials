# Pitch queue — clear this in one pass

Built 2026-09-20 from 35 unique requests across the digest history. 17 live, 14 cold (> 10 days and unpitched).

**Ages are read off each request page** (`datePublished`), not off the digest text — see `marketing/haro-outreach/verified-requests.json`, refreshed by `scripts/verify_journo_requests.py`. An earlier build fell back to the digest's first-seen date and showed a 190-day-old request as 8 days old.

**No renewal signal exists on this source.** Sourcee publishes no renewal signal: on the 300 most recently indexed slugs and all 30 slugs of the live AI topic feed (checked 2026-09-19) the sitemap lastmod is byte-identical to datePublished, so 'never refreshed' is not observable and is not claimed here. Cold means old and unpitched, not provably abandoned.

**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, Qwoted and Medialyst need authenticated sessions, and Sourcee redacts the requester's own address in the request body. That is why 43 flagged opportunities produced zero pitches. Reply routes are named per row — including addresses resolved off the *publication's* own site (a byline page or an editorial contact page), which is now the strongest route class in this queue.

## Drafts that exist and were never sent

Read this before clearing the queue: four drafts are already written and none has been sent. A written draft is not progress — the send is.

- anthropic-users-and-business-owners-customer-service-experiences — **Draft ready and UNSENT since 2026-09-19, re-verified unchanged 2026-09-20: `pitch-drafts-2026-09-20.md` §2.** Route: Signal hliwrites.99 (re-read off the live page 2026-09-20). Now 8 days old — send or drop.
- finops-professionals-agentic-ai-cost-overruns — **Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1.** Route: LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 and still unsent — the longest-standing high-relevance request this monitor has never answered. Send it late or drop it, do not draft it a fourth time.
- fulltime-employees-shadow-ai-use-and-paying-outofpocket — **Draft ready and UNSENT since 2026-09-19, re-verified unchanged 2026-09-20: `pitch-drafts-2026-09-20.md` §1.** Route: simon.chandler@raconteur.net. ROUTE NOTE: the 2026-09-19 digest cited raconteur.net/author/simon-chandler/ for the obfuscated address triple; that URL 404s as of 2026-09-20 and the live page is /contributors/simon-chandler (HTTP 200, same triple, same address). Send this row.
- speciality-food-retailers-and-producers-how-theyd-spend-10k-on-t — **Draft ready and UNSENT since 2026-09-19, re-verified unchanged 2026-09-20: `pitch-drafts-2026-09-20.md` §3.** Route: holly.shackleton@artichokehq.com (re-read off specialityfoodmagazine.com/contact 2026-09-20).

## Live — pitch these

### [high] AI / Shadow AI Spend / Out-of-Pocket Subscriptions / Enterprise Tech
- **URL:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-19, last 2026-09-20 (2x)
- **Publication:** Raconteur (raconteur.net) — author named in the page's own author field: Simon Chandler · domain raconteur.net
- **Reply route:** The page redacts the address ('Please email me at [email redacted]'), but Raconteur's own byline pages publish the writer's address as an obfuscated data-part1/2/3 triple that the site's JS assembles at runtime (scripts-last.min.js: part1 + '@' + part2 + '.' + part3). Reconstructed and cross-checked against a second author this run: simon.chandler@raconteur.net. raconteur.net MX = Google Workspace (aspmx.l.google.com). Raconteur's /contact page states PRs should contact the relevant writer directly. ROUTE CORRECTED 2026-09-20: the 2026-09-19 digest named https://www.raconteur.net/author/simon-chandler/ as the page publishing the obfuscated data-part1/2/3 triple. That URL now returns HTTP 404 (139,404 bytes, Raconteur's own 404 shell) and so does /author/ian-deering/, which had been used as the cross-check. Raconteur's author-sitemap.xml still lists him but under a different, space-encoded path: https://www.raconteur.net/contributors/Simon%20Chandler - which is itself a 404. The live page is https://www.raconteur.net/contributors/simon-chandler (HTTP 200) and it still carries data-part1="simon.chandler" data-part2="raconteur" data-part3="net", i.e. simon.chandler@raconteur.net, unchanged. Control test on the same run: https://www.raconteur.net/contributors/tom-dennis (HTTP 200) carries data-part1="tom.dennis" data-part2="raconteur" data-part3="net". raconteur.net MX re-checked today = Google Workspace (1 aspmx.l.google.com). The address is unchanged; only the URL that publishes it moved, so the draft needed no edit but the queue's route note did.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** Template 2 (Overlapping Subscriptions / Cost Optimization), shadow-spend framing — lead with the affordability threshold computed from data/pricing_snapshots.json today: 31 of the 76 tools we track have a cheapest paid tier at or under $25/month, median $16.50, lowest $4 (Khanmigo, checked 2026-09-18); and the same tier billed monthly instead of annually runs up to 2.53x (Browse AI $48/month vs $1

### [medium-high] AI / Vendor Support Quality / Subscription Value
- **URL:** https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-09-12, last 2026-09-20 (6x)
- **Publication:** Independent journalist (dedicated story on Anthropic customer service)
- **Reply route:** Signal handle 'hliwrites.99' published verbatim in the request (re-read off the live page this run); DMs or email also invited, address redacted on Sourcee.  ·  _no — platform reply (George)_
- **Angle:** Template 1 (AI Tool Pricing Changes, reactive) — adapted: pitch the price-to-support ratio, not a grievance. Frame: Anthropic's paid tiers run from $20/month (Pro, $17 annual) to $100-$200/month (Max); at the top tiers buyers pay enterprise money for consumer-grade support channels, which is what makes a support gap a value problem rather than an annoyance. Offer verified Anthropic pricing snapsho

### [medium] Founders / SaaS / AI Tools / Startup Profile
- **URL:** https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-09-11, last 2026-09-20 (5x)
- **Publication:** Independent (bi-weekly founder series, 'Built From Scratch')
- **Reply route:** Comment on the original post with a short description of the business | PAGE-VERIFIED 2026-09-19: email_redacted=False, emails_on_page=none, reply_hints=none.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** Template 3 (AI Tool Directory / Comparison, general) — adapted: pitch AIToolsEssentials as a bootstrapped independent tool directory that grew out of the overlap problem. Angle: 'what's completely not working' is honest material — the directory earns nothing from rankings, so the keep/cut verdicts are the product. Mention the free Stack Audit as the current traction experiment. Medium priority — b

### [medium-low] AI / Founders / Deliberate AI Reduction
- **URL:** https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business
- **Posted:** 2d old (digest (page not probed)) · badge: — · AI-topic feed: no
- **Seen:** first 2026-09-20, last 2026-09-20 (1x)
- **Publication:** Forbes - author named in the page's own author field: Jodie Cook
- **Reply route:** Comment on the original post - the body is explicit: 'Please only answer as a comment on this post. Do not email or DM me because they won't be used.' No email published. PAGE-VERIFIED 2026-09-20: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None - the reply route is a public comment requiring a named founder's firsthand account, which we do not have.

### [low-medium] Retail Tech Budget / £10k Procurement / Speciality Food
- **URL:** https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-19, last 2026-09-20 (2x)
- **Publication:** Speciality Food magazine (specialityfoodmagazine.com) — author named in the page's own author field: Holly Shackleton, Content Editor · domain specialityfoodmagazine.com
- **Reply route:** The page redacts the address, but the magazine's /contact page publishes named editorial addresses: holly.shackleton@artichokehq.com (Content Editor), verified live this run. artichokehq.com MX = Outlook/Microsoft 365 (artichokehq-com.mail.protection.outlook.com).  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** Template 2 (cost optimization), budget-benchmark framing — lead with a verified figure and no currency conversion: 40 of the 76 AI tools we track publish a non-zero monthly price, 31 of them at or under $25/month, and of those that quote both terms the same tier runs 1.21x-2.53x depending on whether it is billed monthly or annually (checked 2026-09-18). Offer the dated set as a benchmark against t

### [low-medium] AI / Founders / Policy Impact
- **URL:** https://www.sourcee.app/journo-request/us-founders-calls-to-slow-ai-development-impact-on-companies
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-16, last 2026-09-20 (4x)
- **Publication:** Inc. (domain inc.com) · domain inc.com
- **Reply route:** Email the reporter — redacted on Sourcee. No reachable route from the page. | PAGE-VERIFIED 2026-09-19: email_redacted=True, emails_on_page=none, reply_hints=['email me'].  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** Template 3 (AI Tool Directory / Comparison, general) — only if a data contribution is welcome: the commercial-AI-spend picture small teams are actually acting on is consolidation, not guardrails, and we hold dated pricing evidence for how that looks.

### [medium-low] AI Policy / Regulation / CIO Impact
- **URL:** https://www.sourcee.app/journo-request/tech-policy-experts-california-ai-audit-bills-impact-cios
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-09-12, last 2026-09-20 (5x)
- **Publication:** Independent journalist (tech policy beat) · domain industrydive.com
- **Reply route:** Email (redacted on Sourcee) or DM — reply to the original post  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** Template 3 (AI Tool Directory / Comparison, general) — adapted if pursuing: the compliance-driven inventory angle. Frame: third-party AI audit requirements force organisations to enumerate which AI systems they run and what those systems cost — most cannot, and the subscription inventory is the prerequisite nobody scopes. Do not pitch: the stated deadline has passed.

### [low] AI / Autonomous Weapons / Investigative
- **URL:** https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- **Posted:** 1d old (digest (page not probed)) · badge: — · AI-topic feed: no
- **Seen:** first 2026-09-20, last 2026-09-20 (1x)
- **Publication:** The Lever - author field 'badplacetimes', journalist self-identified as Craig
- **Reply route:** Signal 972-408-7275, published verbatim in the request body. PAGE-VERIFIED 2026-09-20: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded, wrong standing.

### [low] US Healthcare Billing / Consumer Costs
- **URL:** https://www.sourcee.app/journo-request/patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges
- **Posted:** 1d old (digest (page not probed)) · badge: — · AI-topic feed: no
- **Seen:** first 2026-09-20, last 2026-09-20 (1x)
- **Publication:** Independent journalist - author field: Tanushka Dutta
- **Reply route:** DM the author; no email published. PAGE-VERIFIED 2026-09-20: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None - excluded, wrong subject.

### [low] AI / Workforce / Age & Adaptation
- **URL:** https://www.sourcee.app/journo-request/employers-and-recruiters-over-50s-adapting-to-ai
- **Posted:** 2d old (digest (page not probed)) · badge: — · AI-topic feed: no
- **Seen:** first 2026-09-20, last 2026-09-20 (1x)
- **Publication:** Independent (Ovee, 'Beyond the CV' interviews) - author field: Peter Tsakissiris
- **Reply route:** No email, DM handle or link published on the page. PAGE-VERIFIED 2026-09-20: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _no — platform reply (George)_
- **Angle:** None - excluded.

### [low] Data Centre / Podcast Guest Booking
- **URL:** https://www.sourcee.app/journo-request/data-center-professionals-podcast-guest-ai-and-hyperscale-trends
- **Posted:** 2d old (digest (page not probed)) · badge: — · AI-topic feed: no
- **Seen:** first 2026-09-20, last 2026-09-20 (1x)
- **Publication:** Independent podcast ('The Strategic Podcast') - author field: Todd T. Stone
- **Reply route:** No route published on the Sourcee page; the body solicits guest and sponsor enquiries. PAGE-VERIFIED 2026-09-20: HTTP 200, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded, and it is a booking solicitation rather than a request.

### [low] AI / Alignment / Philosophy
- **URL:** https://www.sourcee.app/journo-request/ai-alignment-researchers-humanai-mutual-understanding
- **Posted:** 2d old (digest (page not probed)) · badge: — · AI-topic feed: no
- **Seen:** first 2026-09-20, last 2026-09-20 (1x)
- **Publication:** Independent (framework author, LinkedIn long-form) - author field: Zamo Dana
- **Reply route:** No email or handle published on the page. PAGE-VERIFIED 2026-09-20: HTTP 200, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None - excluded.

### [low] Legal / AI Vendor Claims / Practice Impact
- **URL:** https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-17, last 2026-09-20 (3x)
- **Publication:** Massachusetts Lawyers Weekly (masslawyersweekly.com) — published across state Lawyers Weekly titles · domain masslawyersweekly.com
- **Reply route:** DM the author (page author field: misterschwartz33). No email published; on-record or on-background offered. | PAGE-VERIFIED 2026-09-19: email_redacted=False, emails_on_page=none, reply_hints=['DM me'].  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None this run — wrong standing. If pursued, the only honest line is that vendor-published performance claims are self-reported, the same pattern we document on pricing pages.

### [low] AI Labour / Data Annotation / Income
- **URL:** https://www.sourcee.app/journo-request/gen-z-ai-data-annotators-work-experience-and-income-impact
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-17, last 2026-09-20 (3x)
- **Publication:** Fortune (freelance reporter) · domain fortune.com
- **Reply route:** DM or email — redacted on Sourcee. | PAGE-VERIFIED 2026-09-19: email_redacted=True, emails_on_page=none, reply_hints=['DM me', 'email me'].  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None — excluded.

### [low] AI / Automation / Speaking
- **URL:** https://www.sourcee.app/journo-request/ai-automation-experts-speakers-on-marketing-sales-operations-gains
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-17, last 2026-09-20 (3x)
- **Publication:** Independent platform (AI TED-talk format)
- **Reply route:** Comment on the original post (body instructs commenting a keyword for tickets). No email published. | PAGE-VERIFIED 2026-09-19: email_redacted=False, emails_on_page=none, reply_hints=['Comment'].  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None — excluded.

### [low] Ecommerce / AI Recommendations / Conversion
- **URL:** https://www.sourcee.app/journo-request/ecommerce-marketers-transparency-in-ai-recommendations-and-conversion
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-17, last 2026-09-20 (3x)
- **Publication:** MarketingSherpa (marketingsherpa.com) · domain marketingsherpa.com
- **Reply route:** Reply to the original X/LinkedIn post (body links a recent article). No email published. | PAGE-VERIFIED 2026-09-19: email_redacted=False, emails_on_page=none, reply_hints=none.  ·  _no — LinkedIn DM / comment (George)_
- **Links published on the page:** https://t.co/1pVlbDpTfQ
- **Angle:** None — excluded.

### [low] Cybersecurity / Media Placement / AI Scams
- **URL:** https://www.sourcee.app/journo-request/cybersecurity-companies-and-experts-ai-scams-and-consumer-safety
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-09-16, last 2026-09-20 (4x)
- **Publication:** Independent PR/comms practitioner sourcing cybersecurity spokespeople
- **Reply route:** Not stated on the Sourcee page — the body asks companies to identify themselves; no email, DM handle or form published. | PAGE-VERIFIED 2026-09-19: email_redacted=False, emails_on_page=none, reply_hints=none.  ·  _no — platform reply (George)_
- **Angle:** None — off-beat and off-standing.

## Cold — only if you have a reason

Older than the 10-day line and never pitched. Not provably abandoned — no renewal signal exists on this source — but every one of these has already passed an ideal send window.

- [high] 13d old — https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
- [high] 15d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-ai-governance-and-agent-sprawl
- [high] 15d old — https://www.sourcee.app/journo-request/scientists-phd-students-and-postdocs-paying-for-ai-subscriptions
- [high] 61d old — https://www.sourcee.app/journo-request/business-and-technology-leaders-tech-budget-priorities-amid-volatility
- [high] 121d old — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [medium-high] 13d old — https://www.sourcee.app/journo-request/uk-managers-cracked-down-on-gen-z-ai-overuse
- [medium-high] 187d old — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium] 13d old — https://www.sourcee.app/journo-request/ai-agents-making-money-2026-sales-and-leadgen-workflow-ops
- [medium] 13d old — https://www.sourcee.app/journo-request/ai-startups-workplace-fraud-detection-expenses-time-theft
- [medium] 13d old — https://www.sourcee.app/journo-request/marketing-and-content-leaders-aiassisted-work-review-process
- [medium] 17d old — https://www.sourcee.app/journo-request/ceos-ai-impact-on-ops-culture-and-commercial-strategy
- [medium] 27d old — https://www.sourcee.app/journo-request/uk-finance-risk-and-regulatory-leaders-ai-explainability-risks
- [medium] 194d old — https://www.sourcee.app/journo-request/sme-owners-operational-challenges-for-ai-solutions-case-study
- [low-medium] 29d old — https://www.sourcee.app/journo-request/ai-project-builders-youtube-finance-and-lifestyle-channel-feature

---

## Clearing the queue

After sending, record it so the row does not reappear:

```json
{"pitched": {"<url>": "2026-09-15"}, "skipped": {"<url>": "reason"}}
```

Ledger: `marketing/haro-outreach/pitch-ledger.json`
