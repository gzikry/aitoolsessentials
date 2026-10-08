# Pitch queue — clear this in one pass

Built 2026-10-08 from 101 unique requests across the digest history. **1 sendable**, 54 live, 43 cold (> 10 days and unpitched).

*"Sendable" is the number that matters and the one the headline used to hide: a live page is not a candidate. A row counts as sendable only when it is live, not cold, not dropped off, not already pitched, ranked above the tangential band, and has a resolved reply route (a published email, a named handle, a booking link). The other live rows are off-beat calls this queue already documents as excluded.*

**Ages are read off each request page** (`datePublished`), not off the digest text — see `marketing/haro-outreach/verified-requests.json`, refreshed by `scripts/verify_journo_requests.py`. An earlier build fell back to the digest's first-seen date and showed a 190-day-old request as 8 days old.

**No renewal signal exists on this source.** Sourcee publishes no renewal signal: on the 300 most recently indexed slugs and all 30 slugs of the live AI topic feed (checked 2026-09-19) the sitemap lastmod is byte-identical to datePublished, so 'never refreshed' is not observable and is not claimed here. Cold means old and unpitched, not provably abandoned.

**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, Qwoted and Medialyst need authenticated sessions, and Sourcee redacts the requester's own address in the request body. That is why 43 flagged opportunities produced zero pitches. Reply routes are named per row — including addresses resolved off the *publication's* own site (a byline page or an editorial contact page), which is now the strongest route class in this queue.

## Drafts that exist and were never sent

Read this before clearing the queue: 21 draft files exist on disk and not one of the pitches in them has been sent. A written draft is not progress — the send is.

**THE QUEUE IS AT 1 SENDABLE — THE FIRST TIME THIS MONITOR HAS EVER PRODUCED ONE.** Every prior build reported 0, and twice that 0 was a genuine measurement after a defect had been fixed (the 2026-09-29 chrome leak into `published_links`, the 2026-10-01 Google Form read as a link route). The row is declared sendable on two facts evidenced separately: a relevance above the tangential band, and a reply route verified by fetching a page today rather than by trusting a digest field. Both are named in the row. The live unpitched set is 54 rows.

**Today's draft file is `pitch-drafts-2026-10-08.md` (derived from disk, not typed).** The headline figures are re-derived every run: 42 of 76 tools publish a monthly price, 33 of those at or under $25/month, median $17.50 (snapshots `updated: 2026-10-08`). Superseded sets still sitting in older dated drafts (40/31/$16.50 and earlier) must not be reused.

**The pair range is `1.11x to 2.53x, median 1.25x` over 19 tiers, and it held today.** History, because every superseded value is still sitting in dated draft files and must not be reused: the range was first published as `1.21x to 2.53x, median 1.33x` (2026-09-18, sent to a real correspondent — wrong because the pair population was regex-dependent and undefined); corrected to `1.16x to 2.53x, median 1.25x` over 18 curated pairs (2026-09-21); then re-derived to `1.11x to 2.53x` when the replit-ai snapshot was refreshed (2026-09-22). See `data/monthly_annual_pairs.json` and `scripts/extract_monthly_annual_pairs.py`, which refuses to write the file at all unless every curated pair re-asserts against the live snapshot.

- anthropic-users-and-business-owners-customer-service-experiences — **Crossed cold 2026-09-23; now 26d old — no longer counted as sendable.** Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal hliwrites.99 (re-read verbatim off the live page 2026-09-30). Send late or record as skipped in `pitch-ledger.json`; the crossing is logged in `cold_without_a_send`.
- employees-blocked-from-ai-on-work-accounts-automating-tedious-ta — **SENDABLE — draft ready and UNSENT — `pitch-drafts-2026-10-08.md` §1. Now 3d old.** Route: LinkedIn DM to linkedin.com/in/christopher-mims-club/ (LinkedIn byline page — route-checks probe 2026-10-08: HTTP 200, 603,602 bytes, title 'Christopher Mims - The Wall Street Journal | LinkedIn'; the request's own body says '(DMs open)'; muckrack.com/christopher-mims 403 and wsj.com/news/author/christopher-mims 401 are dead ends, not routes). This is the ONLY row in this queue that is both above the tangential band and route-resolved. George's lane.
- finops-professionals-agentic-ai-cost-overruns — **Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1. Now 31d old.** Route: LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 and still unsent — the longest-standing high-relevance request this monitor has never answered. Send it late or drop it, do not draft it a fifth time.
- fulltime-employees-shadow-ai-use-and-paying-outofpocket — **Draft ready and UNSENT — `pitch-drafts-2026-10-08.md` §2. Now 21d old, and it crossed the 10-day line on 2026-09-28 unpitched. Carried in 18 draft files.** Route: simon.chandler@raconteur.net, re-resolved off the live /contributors/simon-chandler page — route-checks probe 2026-10-08: HTTP 200, 154,819 bytes, data-part triple simon.chandler + raconteur + net, title 'Simon Chandler, Author at Raconteur' (control /contributors/tom-dennis — route-checks probe 2026-10-08: HTTP 200, 154,030 bytes, data-part triple tom.dennis + raconteur + net, title 'Tom Dennis, Author at Raconteur'); the older /author/simon-chandler/ URL still 404s and must not be cited. Figures re-derived at build time (76 tools, 42 publishing a monthly price, 33 of those at or under $25/month, median $17.50 (snapshots `updated: 2026-10-08`); and the pair range 1.11x-2.53x, median 1.25x over 19 tiers (built 2026-10-08)). It is the only high-relevance request this monitor has ever produced with a resolved route; the page is still HTTP 200 and the address still resolves, so a late send is still possible — what was lost is the ideal window, not the pitch.
- google-and-claude-enterprise-users-seats-and-token-costs — **DRAFT READY, ROUTE UNRESOLVED — NOT SENDABLE YET — `pitch-drafts-2026-10-08.md` §2. Now 0d old, relevance 'high'.** This is the first core-beat AI+spend request in fourteen runs and the best-matching request this queue has ever held: the reporter (Glenn Hansen) asks directly for 'enterprise-level costs for AI seats and tokens' from Google or Claude users, and our dated set answers it (Claude Team $20/$100 per seat/month checked 2026-09-18; Gemini in Workspace $8.40/$7 to $26.40/$22 per user/month, 2026-09-18; Copilot Business $19 / Enterprise $39 per user/month, 2026-10-01). NO ROUTE: the page publishes no address, handle or link (verified email_redacted=False, emails_on_page=none), and a web search cannot confirm WHICH Glenn Hansen this is — a same-name LinkedIn profile is a different person — so no handle may be invented. George's lane to resolve the route; the draft is otherwise ready.
- speciality-food-retailers-and-producers-how-theyd-spend-10k-on-t — **Draft ready and UNSENT — `pitch-drafts-2026-10-08.md` §3. Now 20d old, crossed the 10-day line on 2026-09-28 unpitched. Carried in 17 draft files.** Route: holly.shackleton@artichokehq.com (re-read off specialityfoodmagazine.com/contact — route-checks probe 2026-10-08: HTTP 200, 59,488 bytes, title 'Contact Us | Speciality Food Magazine', alongside five other named staff addresses). Standing constraint is stated in the draft's first line: we are not a food retailer. Its October issue window has closed, so treat this as a send-or-skip call and record the outcome in `pitch-ledger.json` rather than carrying it a 18th day.

## Sendable — pitch these (1)

Live, not cold, ranked above the tangential band, and with a reply route a human can actually use. This is the whole actionable queue.

### [medium] AI / Workplace Policy / Shadow & Unapproved AI Use
- **URL:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-08 (3x)
- **Publication:** Christopher Mims (author field) — Wall Street Journal columnist (outlet not named in the body; confirmed at his own byline page)
- **Reply route:** Body says '(DMs open)'; no address, handle or link is printed in the request itself. Route RESOLVED today off his own byline page, not off the request: https://www.linkedin.com/in/christopher-mims-club/ returns HTTP 200 (603,602 bytes), title 'Christopher Mims - The Wall Street Journal | LinkedIn'. Two dead ends recorded so they are not retried as routes: muckrack.com/christopher-mims HTTP 403 (Cloudflare interstitial) and wsj.com/news/author/christopher-mims HTTP 401. LINKEDIN DM — George's lane. Not automatable. PAGE-VERIFIED 2026-10-08 on the request: HTTP 200, email_redacted=False, emails_on_page=none, published_links=Sourcee chrome only.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** Template: lead with the dated price set behind the blocked-employee workaround (42 of 76 tools quote a monthly price, 33 of those at or under $25/month, median $17.50; monthly vs annual 1.11x-2.53x, median 1.25x over 19 tiers; snapshots re-checked 2026-10-08), state plainly that we are not an employee with a blocked account, and offer the full dated set with sources. Draft: pitch-drafts-2026-10-08

## Live but not sendable (53)

These pages resolve and the requests are unexpired, so they are recorded — but none has both a relevance above the tangential band and a usable route. They are listed for completeness, not as candidates: pitching any of them would mean claiming standing we do not have (see the exclusions in the newest `pitch-drafts-*.md`).

### [high] AI / Enterprise Procurement / Seats & Token Costs
- **URL:** https://www.sourcee.app/journo-request/google-and-claude-enterprise-users-seats-and-token-costs
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-08, last 2026-10-08 (1x)
- **Publication:** Glenn Hansen (author field) — outlet not named in the body (he states he reports on power-equipment manufacturing)
- **Reply route:** The body publishes NO address, handle or link and gives no reply instruction beyond 'Google or Claude users care to enlighten me?'; the page's only published links are Sourcee chrome. email_redacted=False but emails_on_page=none. NO ROUTE RESOLVED on the page. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, feed=n.  ·  _unknown — verify the route before sending_
- **Angle:** Lead with the dated seat prices, name the checked date on each, and note that enterprise tiers are sales-assisted (so the list price is the only public anchor). No route is resolved, so this cannot be sent yet - do NOT invent a LinkedIn handle for a common name.

### [low-medium] AI / Enterprise Adoption / CNBC Series
- **URL:** https://www.sourcee.app/journo-request/uk-companies-implementing-ai-how-automation-transforms-workdays
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-08 (2x)
- **Publication:** Lindsay Dodgson (author field) — CNBC (cnbc.com, domain field) · domain cnbc.com
- **Reply route:** Body: 'you know where to find me [email redacted]'. Address Sourcee-redacted; no handle or link published. NO ROUTE RESOLVED as-is. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, email_redacted=True, feed=Y.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** If a route is ever resolved, the only defensible angle is the dated-price half of 'fresh data': 42 of 76 tools quote a monthly price, 33 at or under $25/month, median $17.50; monthly vs annual 1.11x-2.53x, median 1.25x over 19 tiers (snapshots re-checked 2026-10-08). Do NOT claim to be a UK company implementing AI. Excluded this run for want of a route.

### [low-medium] AI / Legal Sector / Billing & Billable Hour
- **URL:** https://www.sourcee.app/journo-request/law-firm-lawyers-concrete-ai-implementations-and-billing-impact
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-05, last 2026-10-08 (4x)
- **Publication:** Lindsay Dodgson (author field) — CNBC (cnbc.com, domain field) · domain cnbc.com
- **Reply route:** The body says 'If you'd like to chat: [email redacted]' — Sourcee redacts the address. No author page exists at cnbc.com (/lindsay-dodgson/ and /author/lindsay-dodgson/ both HTTP 404) and the page publishes no alternative route. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=True, emails_on_page=none.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None — excluded: wants a practising lawyer's own firm evidence. A price-dataset contribution would be claiming standing we do not have, and the body address is redacted with no alternative route on cnbc.com.

### [low-medium] AI / Workplace Culture / Shadow AI Use
- **URL:** https://www.sourcee.app/journo-request/employees-conflicted-about-ai-use-generative-ai-workplace-impact
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-01, last 2026-10-08 (6x)
- **Publication:** Independent artist/filmmaker (video project; outlet not named)
- **Reply route:** A Google Form published in the body (docs.google.com/forms/d/e/1FAIpQLSdWsFQ0q\_Mngmu7kGKnLwt4Z-Z4\_Exh5H41eqJ0rjk0t1i1Jg/viewform) or a direct message. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, published_links=['https://docs.google.com/forms/d/e/1FAIpQLSdWsFQ0q'].  ·  _unknown — verify the route before sending_
- **Links published on the page:** https://docs.google.com/forms/d/e/1FAIpQLSdWsFQ0q
- **Angle:** Template 2 (cost optimization), only if a data contribution is welcome: offer the dated price set behind unmanaged adoption rather than a personal account. Do not claim to be a conflicted employee.

### [low-medium] Insurance / AI Adoption
- **URL:** https://www.sourcee.app/journo-request/insurance-agents-ai-use-in-personal-lines
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-09-29, last 2026-10-08 (8x)
- **Publication:** P&C Specialist (Financial Times) — reporter not named in the body · domain ft.com
- **Reply route:** 'Comment below or DM me' — no address published and none redacted. PAGE-VERIFIED 2026-10-08: email_redacted=False, emails_on_page=none, reply_hints=['Comment', 'DM me']. Route is the original X/LinkedIn post; we hold no handle for this reporter.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None — excluded: wants a working insurance agent's own AI usage; we have no standing and the only route is a public comment on a post we cannot identify.

### [low] Legal / IP / Practitioner Guide
- **URL:** https://www.sourcee.app/journo-request/patent-attorneys-and-agents-startup-ip-starter-pack
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-08, last 2026-10-08 (1x)
- **Publication:** Ptoleme (author field) — no domain named
- **Reply route:** Body: 'Feel free to comment or message me' with an acknowledgement offer, but no address, handle or link printed. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, feed=n.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants patent practitioners; no spend angle, no route.

### [low] AI / Public-Sector Workforce / Skills & Training
- **URL:** https://www.sourcee.app/journo-request/aps-hr-leaders-ai-skills-training-and-workforce-planning
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-08 (2x)
- **Publication:** Joshua Gliddon (author field) — The Mandarin (themandarin.com.au, domain field) · domain themandarin.com.au
- **Reply route:** Body: 'please drop me a line' with no address, handle or link published; the page's only published links are Sourcee chrome. email_redacted=False but emails_on_page=none. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, feed=Y.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants public-sector HR interviewees; no spend angle and no route.

### [low] AI / Agile Careers / Podcast Guest Booking
- **URL:** https://www.sourcee.app/journo-request/scrum-masters-daytoday-and-career-pivots-and-ai-impact
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-08 (2x)
- **Publication:** Dr. Yvette Jett (author field) — The Dr. Vett Jett Show (vettjett.com, domain field) · domain vettjett.com
- **Reply route:** Body: 'Send me a message right here on LinkedIn or email me at [email redacted]'. The address is Sourcee-redacted and no handle is printed; no route resolved. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, email_redacted=True, emails_on_page=none.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: wants practising Scrum Masters as guests; we hold no such standing.

### [low] AI / PropTech / Vendor Blog Content Call
- **URL:** https://www.sourcee.app/journo-request/real-estate-agents-replacing-pdf-property-brochure
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-08 (2x)
- **Publication:** Lyza G (author field) — Flipbooker blog (flipbooker.com, domain field) · domain flipbooker.com
- **Reply route:** Body: 'Email [email redacted]'. Address Sourcee-redacted; no handle or link. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, email_redacted=True.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: vendor blog promo wanting a real-estate agent voice.

### [low] AI / Marketing Technology / Self-Promo Spotlight
- **URL:** https://www.sourcee.app/journo-request/anz-marketers-ai-and-martech-innovation-spotlight
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-08 (2x)
- **Publication:** RAHUL B. (author field) — KARV Tech Insider (domain not named in the page's domain field)
- **Reply route:** Body: 'DM me. Let's connect and explore how we can amplify your story.' No handle, address or link published; the page's only published links are Sourcee chrome. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, feed=Y.  ·  _no — platform reply (George)_
- **Angle:** None — excluded: self-promo spotlight, no editorial data ask and no route.

### [low] AI / Legal Sector / Access to Justice
- **URL:** https://www.sourcee.app/journo-request/solicitors-and-barristers-ai-to-expand-pro-bono-capacity
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-08, last 2026-10-08 (1x)
- **Publication:** Catherine Baksi (author field) — publication not named
- **Reply route:** Body: 'please drop me an email at: [email redacted] by the end of this week'. Address Sourcee-redacted; no handle or link. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, email_redacted=True, emails_on_page=none.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: wants law firms' own pro-bono AI projects; no spend angle, no route.

### [low] AI / Labour / Data Training
- **URL:** https://www.sourcee.app/journo-request/uk-ai-data-trainers-daytoday-work
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-08, last 2026-10-08 (1x)
- **Publication:** momitola (author handle) — The Times (thetimes.co.uk, domain field) · domain thetimes.co.uk
- **Reply route:** Body: 'Ping me a message if you're interested'. No handle, address or link printed. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, feed=n.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants UK data trainers' first-person accounts.

### [low] AI / Press & Media / Accountability
- **URL:** https://www.sourcee.app/journo-request/apac-reporters-and-editors-ai-accountability-coverage
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-08, last 2026-10-08 (1x)
- **Publication:** Sen Nguyen (author field) — BBC News (bbc.co.uk, domain field) · domain bbc.co.uk
- **Reply route:** Body: 'Hit me up here or at [email redacted]'. Address Sourcee-redacted; no handle or link. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, email_redacted=True.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: wants APAC reporters/editors; no spend angle.

### [low] AI / UX & IA / Practitioner Interviews
- **URL:** https://www.sourcee.app/journo-request/early-to-midcareer-information-architects-products-featuring-ai
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-08, last 2026-10-08 (1x)
- **Publication:** World Information Architecture Association (author field) — no domain named
- **Reply route:** No address, handle or link published; the body gives no reply instruction. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, feed=n.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants IA practitioners' own product stories.

### [low] AI / Martech / Vendor Blog Content Call
- **URL:** https://www.sourcee.app/journo-request/martech-buyers-ai-impact-on-build-vs-buy-decisions
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-08, last 2026-10-08 (1x)
- **Publication:** Lyza G (author field) — Flipbooker blog (flipbooker.com, domain field) · domain flipbooker.com
- **Reply route:** Body: 'Email [email redacted]'. Address Sourcee-redacted; no handle or link. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, email_redacted=True.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: vendor blog promo wanting martech-buyer quotes.

### [low] AI / Infrastructure / Data-Centre Capacity
- **URL:** https://www.sourcee.app/journo-request/ai-infrastructure-experts-china-vs-us-datacenter-capacity
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-08 (3x)
- **Publication:** Harriet Weber (author field) — outlet not named in the body
- **Reply route:** The body publishes a Signal username, 'hew.04', plus an address Sourcee redacts. Signal is a resolved route; the request still asks for expertise we do not hold. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=True, emails_on_page=none, published_links=Sourcee chrome only.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: no data-centre-capacity expertise. Route (Signal hew.04) recorded so the exclusion can be audited.

### [low] AI / Legal / Deepfake Liability
- **URL:** https://www.sourcee.app/journo-request/plaintiffs-attorneys-and-legal-scholars-ai-deepfake-liability
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-08 (3x)
- **Publication:** Mitchell Price (author field) — outlet not named (student podcast)
- **Reply route:** The body asks respondents to 'comment on this post'; no address, handle or link is published. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, reply_hints=none, published_links=Sourcee chrome only. No route we can use.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None — excluded: wants practising attorneys or legal scholars for a student podcast; no spend angle and no route.

### [low] AI / Emergency Management / Public-Sector Adoption
- **URL:** https://www.sourcee.app/journo-request/emergency-managers-ai-tools-for-funding-and-staffing-shortfalls
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-08 (3x)
- **Publication:** Jake Bittle (named in the body) — Grist (grist.org, domain field) · domain grist.org
- **Reply route:** The body prints a phone number (8134664712) and an address Sourcee redacts. Grist's staff page grist.org/staff/jake-bittle/ returns HTTP 404, so no email route resolved. A phone is a voice route, not a written pitch route. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=True, emails_on_page=none, published_links=Sourcee chrome only.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: wants an emergency manager's own departmental experience.

### [low] AI / Arts & Community / Data-Centre Siting
- **URL:** https://www.sourcee.app/journo-request/coweta-county-artists-and-creatives-data-centers-and-ai-infrastructure
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-08 (3x)
- **Publication:** Artist Rights Watch (author field) — outlet not named in the body
- **Reply route:** An X post tagging named panellists for an in-person symposium panel; the body carries a t.co link and no address or handle for us. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, published_links=['https://t.co/8l6CGKC9yq', ...Sourcee chrome]. No route we can use.  ·  _unknown — verify the route before sending_
- **Links published on the page:** https://t.co/8l6CGKC9yq
- **Angle:** None — excluded: local panel invitation, not a source request.

### [low] AI / Human-AI Relationships / Documentary
- **URL:** https://www.sourcee.app/journo-request/swiss-ai-companion-users-emotional-bonds-and-daily-life
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-08 (2x)
- **Publication:** Leila (author handle) — SRF 'rec.' (srf.ch, domain field) · domain srf.ch
- **Reply route:** Body: 'You're welcome to send me a private message'. No address, handle or link printed. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, feed=Y.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants Swiss AI-companion users' personal accounts.

### [low] AI / Labour / Data Annotation
- **URL:** https://www.sourcee.app/journo-request/ai-data-labelers-in-germany-positive-and-negative-experiences
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-08 (2x)
- **Publication:** freelance journalist (author handle JulDagg) — FLUTER (fluter.de, domain field) · domain fluter.de
- **Reply route:** No address, handle or link published in the body; interviews offered anonymously. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, feed=Y.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants German data annotators' first-person accounts.

### [low] AI / Labour / Data Annotation
- **URL:** https://www.sourcee.app/journo-request/ai-data-annotators-and-labellers-experience-with-ai-training-data
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-08 (2x)
- **Publication:** Modupe (author field) — The Times (thetimes.co.uk, domain field) · domain thetimes.co.uk
- **Reply route:** Body: 'My email is [email redacted]'. Address Sourcee-redacted; no handle or link. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, email_redacted=True.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: wants annotators' first-person accounts, no spend angle.

### [low] AI / Mental Health / Self-Diagnosis
- **URL:** https://www.sourcee.app/journo-request/ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-08 (2x)
- **Publication:** student journalist (author handle yaegrrr) — publication not named
- **Reply route:** Body: 'feel free to send me a PM or comment below'. No address, handle or link published. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, feed=n.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants users'/therapists' personal accounts.

### [low] AI / Academia / Media & Identity
- **URL:** https://www.sourcee.app/journo-request/academics-social-media-and-ai-impact-on-womens-identity-and-selfesteem
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-08 (2x)
- **Publication:** Lucy Abbersteen (author field) — publication not named
- **Reply route:** Body: 'please comment below!' No address, handle or link published; the only way in is a public comment. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-08: HTTP 200, live=True, feed=n.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants academic researchers; no route beyond a public comment.

### [low] AI / Legal & Insurance / Procurement
- **URL:** https://www.sourcee.app/journo-request/ai-liability-insurers-and-legal-experts-procurement-and-implementation
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-08 (3x)
- **Publication:** Ritoban Mukherjee (author field) — ZDNET (zdnet.com, domain field) · domain zdnet.com
- **Reply route:** The body publishes a Qwoted link, https://lnkd.in/dVu9JK4C (HTTP 200, 5,322 bytes, resolves to LinkedIn), with 'refer to my Qwoted post to pitch any insights'. That is a usable route in principle, but Qwoted's feed needs an authenticated session we do not hold. No address on the page. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _no — published booking link https://lnkd.in/dVu9JK4C (George)_
- **Links published on the page:** https://lnkd.in/dVu9JK4C
- **Angle:** None — excluded: wants AI liability-insurance practitioners; the 'procurement' token is insurance procurement, not software spend.

### [low] AI / Hiring / Cybersecurity Sector Research
- **URL:** https://www.sourcee.app/journo-request/uk-cybersecurity-hiring-managers-state-of-hiring-2026-and-ai-impact
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-08 (3x)
- **Publication:** Mike Carthy (author field) — CyberHire (outlet not named in body)
- **Reply route:** The body publishes a survey form, https://tally.so/r/A7VLXe; no address or handle. A survey form collects the sender's data - it is not a reply route for us. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Links published on the page:** https://tally.so/r/A7VLXe
- **Angle:** None — excluded: wants UK security hiring managers' survey responses.

### [low] AI / Consumer Behaviour / Emotional Use
- **URL:** https://www.sourcee.app/journo-request/ai-emotional-support-users-chatbot-therapy-and-journaling
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-08 (3x)
- **Publication:** Louise Gill (author field) — outlet not named in the body
- **Reply route:** Body says 'DM or email me' but prints neither: email_redacted=False and no address, handle or link appears on the page beyond Sourcee chrome. PAGE-VERIFIED 2026-10-08: HTTP 200, emails_on_page=none. No route we can use.  ·  _no — platform reply (George)_
- **Angle:** None — excluded: wants personal emotional-use accounts; no spend angle, no route.

### [low] AI / Financial Services / Video Series
- **URL:** https://www.sourcee.app/journo-request/mortgage-adviser-using-ai-efficiency-and-client-outcomes-video-series
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-08 (3x)
- **Publication:** Amy Hannah Loddington (author field) — outlet not named in body
- **Reply route:** Body: 'drop me an email on [email redacted]' — Sourcee redacts the address and no alternative route is published. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=True, emails_on_page=none, published_links=Sourcee chrome only.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None — excluded: wants a mortgage adviser's own workflow; address redacted, no route.

### [low] AI / Automotive / Thought-Leadership Placement
- **URL:** https://www.sourcee.app/journo-request/founders-and-cxos-in-automotive-ai-evs-autonomy-thought-leadership
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-08 (3x)
- **Publication:** Poonam Mahajan (author field) — The Autonaut Media (theautonautmedia.com, domain field) · domain theautonautmedia.com
- **Reply route:** Body: 'Reach out to [email redacted] or [email redacted]' — both addresses are redacted and no alternative is published. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=True, emails_on_page=none, published_links=Sourcee chrome only.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None — excluded: contributed-content invitation, not a source request.

### [low] AI / Games Industry / Attribution Disputes
- **URL:** https://www.sourcee.app/journo-request/video-game-developer-falsely-accused-of-using-generative-ai
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-05, last 2026-10-08 (4x)
- **Publication:** Chris Kerr (author field) — outlet not named in the body
- **Reply route:** Body publishes a Signal handle (kerrblimey.43) plus 'Email in bio. DMs open.' PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, reply_hints=['email me'/'DM'], published_links=['https://www.linkedin.com/in/andrewsmith313/', 'https://x.com/andy_cb_smith'] (both Sourcee chrome).  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None — excluded: wants a game developer's own accusation experience; no spend angle.

### [low] AI / Wearables / Legal Industry / Podcast Guest
- **URL:** https://www.sourcee.app/journo-request/lawyers-and-tech-ethics-experts-ai-wearables-and-legal-journeys
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-05, last 2026-10-08 (4x)
- **Publication:** Alexandra Zandamela — Lex & Lace Podcast (podcast guest call)
- **Reply route:** Published booking link (https://lnkd.in/dcKHYkDR) for the podcast; no email on the page. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, published_links=['https://lnkd.in/dcKHYkDR', ...].  ·  _no — published booking link https://lnkd.in/dcKHYkDR (George)_
- **Links published on the page:** https://lnkd.in/dcKHYkDR
- **Angle:** None — excluded: podcast guest call, not a report request; no spend angle.

### [low] Real Estate / MLS Data Access / LLM Permissions Risk
- **URL:** https://www.sourcee.app/journo-request/mls-executives-risks-when-agents-grant-mls-access-to-llms
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-05, last 2026-10-08 (4x)
- **Publication:** Craig Rowe (author field) — outlet not named in the body
- **Reply route:** DMs on the original post; no email, handle or link published on the page. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, published_links=Sourcee chrome only, reply_hints=['DM me']. No route we can use.  ·  _no — platform reply (George)_
- **Angle:** None — excluded: wants an MLS executive's firsthand permissions account.

### [low] Real Estate / Marketing Tools / Document Workflow
- **URL:** https://www.sourcee.app/journo-request/real-estate-agents-and-brokers-switched-from-pdf-brochures
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-05, last 2026-10-08 (4x)
- **Publication:** Lyza G (author field) — outlet not named in the body
- **Reply route:** The body says 'DM me or email [email redacted]' — Sourcee redacts the address and the page publishes no alternative route. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=True, emails_on_page=none, reply_hints=['DM me'/'email me'].  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None — excluded: wants a real estate agent's own switching experience.

### [low] Advertising / AI Audience Discovery / Event Interview
- **URL:** https://www.sourcee.app/journo-request/advertising-tech-and-media-pros-in-miami-ai-audience-discovery
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-05, last 2026-10-08 (4x)
- **Publication:** Kendra Barnett (author field) — outlet not named in the body
- **Reply route:** Drop a line / DM on the original post; no email, handle or link published on the page beyond a t.co. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, published_links=['https://t.co/AEgLhRuQL7', ...]. No route we can use.  ·  _no — platform reply (George)_
- **Links published on the page:** https://t.co/AEgLhRuQL7
- **Angle:** None — excluded: wants Miami conference attendees, not a data contribution.

### [low] AI / Storytelling / Sponsor Solicitation
- **URL:** https://www.sourcee.app/journo-request/storytellers-and-brand-founders-marys-big-30-ai-story-project
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-02, last 2026-10-08 (5x)
- **Publication:** Independent creator (author field: Mary's Big 30 project)
- **Reply route:** Comment or DM on the original post; no email or handle published on the page. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, published_links=none, reply_hints=['Comment'].  ·  _no — platform reply (George)_
- **Angle:** None — excluded: creator project soliciting stories and sponsors.

### [low] AI Agents / Publishing Workflow
- **URL:** https://www.sourcee.app/journo-request/newsletter-editors-using-ai-agents-news-aggregation-practices
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-02, last 2026-10-08 (5x)
- **Publication:** Independent journalist (outlet not named in the body)
- **Reply route:** No email, handle or link published on the page. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, published_links=none, reply_hints=none. No route we can use.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: workflow practice call with no spend angle and no route.

### [low] Education / AI Tools Implementation
- **URL:** https://www.sourcee.app/journo-request/scottish-teachers-ai-tools-implementation-in-education
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-02, last 2026-10-08 (5x)
- **Publication:** Independent journalist (outlet not named in the body)
- **Reply route:** The body says 'DM or email [email redacted]' — Sourcee redacts the address and the page publishes no alternative route. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=True, emails_on_page=none, reply_hints=['DM or email'].  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None — excluded: wrong standing (we are not a Scottish teacher).

### [low] AI / HR Practice / Cognitive Offloading Policy
- **URL:** https://www.sourcee.app/journo-request/hr-leaders-company-ai-strategies-and-cognitive-offloading-risk
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-05, last 2026-10-08 (4x)
- **Publication:** Katie Jacobs (author field) — CIPD (cipd.co.uk, domain field) · domain cipd.co.uk
- **Reply route:** No address or handle on the page; the body says 'Hit me up'. No people page exists at cipd.org (/uk/about/people/katie-jacobs/ and the contact page both HTTP 404). PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, reply_hints=none. No route we can use.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants an HR leader's own policy example; no spend angle, no route.

### [low] Engineering Simulation / Agentic AI / Webinar Guest
- **URL:** https://www.sourcee.app/journo-request/fea-engineers-using-agentic-ai-practitioner-case-study
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-01, last 2026-10-08 (6x)
- **Publication:** Independent / Synera webinar series (author not a journalist byline)
- **Reply route:** No email, handle or link published on the page; the body invites a comment. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, published_links=none, reply_hints=['Comment']. No route we can use.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: webinar guest call wanting an engineer's own deployment story.

### [low] AI / Family / Consumer Behaviour
- **URL:** https://www.sourcee.app/journo-request/parents-ai-acting-as-pseudoparent-in-kid-questions
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-01, last 2026-10-08 (6x)
- **Publication:** Independent writer/journalist (outlet not named in the body)
- **Reply route:** No email, handle or link published on the page; the body says 'would love to chat'. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, published_links=none, reply_hints=none.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: personal testimony call with no spend angle.

### [low] Consumer Platforms / AI Features
- **URL:** https://www.sourcee.app/journo-request/fb-marketplace-sellers-ai-photos-and-description-prompts
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-02, last 2026-10-08 (5x)
- **Publication:** Independent journalist (outlet not named in the body)
- **Reply route:** DM the poster, or an address Sourcee redacts; the page publishes no alternative route. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=True, emails_on_page=none, reply_hints=none.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None — excluded: wrong standing and no spend angle.

### [low] Education / AI Policy / Teacher Testimony
- **URL:** https://www.sourcee.app/journo-request/k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-02, last 2026-10-08 (5x)
- **Publication:** Columbia Journalism School reporting fellow (outlet not named)
- **Reply route:** DMs on the original post; no email, handle or link published on the page. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, published_links=none, reply_hints=none. No route we can use.  ·  _no — platform reply (George)_
- **Angle:** None — excluded: wants a teacher's firsthand moratorium experience.

### [low] AI Industry Events / Conference Controversy
- **URL:** https://www.sourcee.app/journo-request/ai-summit-barcelona-attendees-controversy-and-experiences
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-02, last 2026-10-08 (5x)
- **Publication:** Independent journalist (outlet not named in the body)
- **Reply route:** Tag or DM on the original post; no email, handle or link published on the page. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, published_links=none, reply_hints=['DM me']. No route we can use.  ·  _no — platform reply (George)_
- **Angle:** None — excluded: attendee testimony call with no spend angle.

### [low] AI Hardware / Consumer Product Review
- **URL:** https://www.sourcee.app/journo-request/ai-glasses-owners-users-and-developers-in-india-product-experience
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-02, last 2026-10-08 (5x)
- **Publication:** The StyleList (thestylelist.in) — domain named in the body
- **Reply route:** The body says 'please email us at [email redacted]' — Sourcee redacts the address and the page publishes no alternative route. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=True, emails_on_page=none, published_links=none.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None — excluded: wrong standing (we are not an AI-glasses owner/developer).

### [low] Cybersecurity / AI Risk / Expert Availability
- **URL:** https://www.sourcee.app/journo-request/cybersecurity-expert-ai-nexus-and-security-risks
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-09-30, last 2026-10-08 (7x)
- **Publication:** Unnamed outlet (posted via #journorequest on X/social); no publication named in the request
- **Reply route:** Recommendations/DMs via the original #journorequest post. No email published and none redacted on the Sourcee page; no route we can use.  ·  _no — platform reply (George)_
- **Angle:** None. Off-beat: we do not hold the standing the request asks for (a cybersecurity practitioner; a US emergency physician; a booked radio segment). Do not draft.

### [low] AI / Consumer Experience
- **URL:** https://www.sourcee.app/journo-request/chatbot-users-experiences-talking-to-ai
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-01, last 2026-10-08 (6x)
- **Publication:** Independent journalist (outlet not named in the body)
- **Reply route:** DM or reply to the original post; no email published and none redacted. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, reply_hints=['DM me']. The route is the original post, which we cannot identify.  ·  _no — platform reply (George)_
- **Angle:** None — excluded: no spend angle, no resolvable route.

### [low] AI Security / Governance / Agent Accountability
- **URL:** https://www.sourcee.app/journo-request/us-ai-security-experts-rogue-ai-agents-hitting-government-sites
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-01, last 2026-10-08 (6x)
- **Publication:** Category A publication via a PR/media-query desk (outlet not named)
- **Reply route:** DM the poster; no email or handle published on the Sourcee page. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=False, emails_on_page=none, published_links=none, reply_hints=['Comment'].  ·  _no — platform reply (George)_
- **Angle:** None — excluded: paid placement and wrong standing.

### [low] Real Estate / Document Workflow / Tools
- **URL:** https://www.sourcee.app/journo-request/real-estate-agents-pdf-brochures-vs-alternatives-agent-workflow
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-01, last 2026-10-08 (6x)
- **Publication:** Independent journalist (outlet not named in the body)
- **Reply route:** DM the poster, or an address Sourcee redacts; the page publishes no alternative route. PAGE-VERIFIED 2026-10-08: HTTP 200, email_redacted=True, emails_on_page=none, reply_hints=['DM me'].  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None — excluded: wrong standing (we are not a real-estate agent).

### [low] AI in Public Services / Emergency Response / Health
- **URL:** https://www.sourcee.app/journo-request/us-emergency-physicians-and-paramedics-impact-of-ai-answering-911-calls
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-09-30, last 2026-10-08 (7x)
- **Publication:** Unnamed US national outlet (no masthead named in the request)
- **Reply route:** The body says 'Please email [email redacted]' - Sourcee redacts the address and the page carries no alternative route. Not reachable from this monitor.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Off-beat: we do not hold the standing the request asks for (a cybersecurity practitioner; a US emergency physician; a booked radio segment). Do not draft.

### [low] AI in Hiring / Radio Feature / Audience Call-Out
- **URL:** https://www.sourcee.app/journo-request/job-seekers-and-recruiters-ai-recruitment-experiences
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-09-30, last 2026-10-08 (7x)
- **Publication:** 2SM Super Radio Network / 2HD Newcastle (2sm.com.au) - the Nightline programme · domain 2sm.com.au
- **Reply route:** Call-in audience format (live radio). No email, handle or link published on the page; no route we can use.  ·  _unknown — verify the route before sending_
- **Angle:** None. Off-beat: we do not hold the standing the request asks for (a cybersecurity practitioner; a US emergency physician; a booked radio segment). Do not draft.

### [low] Data Center / AI Infrastructure
- **URL:** https://www.sourcee.app/journo-request/data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-09-29, last 2026-10-08 (8x)
- **Publication:** Connectbase (vendor-authored request, not a journalist byline)
- **Reply route:** No route published on the page: no email, no handle, no link, and no reply hint. PAGE-VERIFIED 2026-10-08: email_redacted=False, emails_on_page=none, published_links=none.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: vendor-authored promotion with no reply route.

### [low] B2B Marketing / Positioning
- **URL:** https://www.sourcee.app/journo-request/b2b-marketing-leaders-hyperspecialization-to-outcompete-ai
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-09-29, last 2026-10-08 (8x)
- **Publication:** MarketingSherpa · domain marketingsherpa.com
- **Reply route:** Original X post (the page carries a t.co link to the article example); no address published. PAGE-VERIFIED 2026-10-08: email_redacted=False, emails_on_page=none, published_links=['https://t.co/Wk0GLLXXen'].  ·  _unknown — verify the route before sending_
- **Links published on the page:** https://t.co/Wk0GLLXXen
- **Angle:** None — excluded: wants a B2B company's own positioning anecdote; we are a publisher, and the request asks for nothing our price data supports.

### [low] AI Adoption / Podcast Guesting
- **URL:** https://www.sourcee.app/journo-request/ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-09-29, last 2026-10-08 (8x)
- **Publication:** AI Everywhere® Leaders podcast (host not named in the body)
- **Reply route:** 'Comment "guest" or send me a DM'; no address published and none redacted. PAGE-VERIFIED 2026-10-08: email_redacted=False, emails_on_page=none, reply_hints=['Comment']. Route is the original LinkedIn post, which we cannot identify from the page.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None — excluded: podcast guest call wanting an operator's own deployment story; no route resolvable off the page.

## Cold — only if you have a reason

Older than the 10-day line and never pitched. Not provably abandoned — no renewal signal exists on this source — but every one of these has already passed an ideal send window.

- [high] 21d old — https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
- [high] 31d old — https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
- [high] 33d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-ai-governance-and-agent-sprawl
- [high] 33d old — https://www.sourcee.app/journo-request/scientists-phd-students-and-postdocs-paying-for-ai-subscriptions
- [high] 79d old — https://www.sourcee.app/journo-request/business-and-technology-leaders-tech-budget-priorities-amid-volatility
- [high] 139d old — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [medium-high] 26d old — https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
- [medium-high] 31d old — https://www.sourcee.app/journo-request/uk-managers-cracked-down-on-gen-z-ai-overuse
- [medium-high] 205d old — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium] 27d old — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [medium] 31d old — https://www.sourcee.app/journo-request/ai-agents-making-money-2026-sales-and-leadgen-workflow-ops
- [medium] 31d old — https://www.sourcee.app/journo-request/ai-startups-workplace-fraud-detection-expenses-time-theft
- [medium] 31d old — https://www.sourcee.app/journo-request/marketing-and-content-leaders-aiassisted-work-review-process
- [medium] 35d old — https://www.sourcee.app/journo-request/ceos-ai-impact-on-ops-culture-and-commercial-strategy
- [medium] 45d old — https://www.sourcee.app/journo-request/uk-finance-risk-and-regulatory-leaders-ai-explainability-risks
- [medium] 212d old — https://www.sourcee.app/journo-request/sme-owners-operational-challenges-for-ai-solutions-case-study
- [medium-low] 19d old — https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business
- [low-medium] 20d old — https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
- [low-medium] 22d old — https://www.sourcee.app/journo-request/us-founders-calls-to-slow-ai-development-impact-on-companies
- [medium-low] 28d old — https://www.sourcee.app/journo-request/tech-policy-experts-california-ai-audit-bills-impact-cios
- [low-medium] 47d old — https://www.sourcee.app/journo-request/ai-project-builders-youtube-finance-and-lifestyle-channel-feature
- [low] 16d old — https://www.sourcee.app/journo-request/saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup
- [low] 16d old — https://www.sourcee.app/journo-request/engineering-managers-measuring-engineers-when-using-ai
- [low] 16d old — https://www.sourcee.app/journo-request/ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai
- [low] 17d old — https://www.sourcee.app/journo-request/sales-enablement-saas-tools-proposal-and-deck-engagement-tracking
- [low] 17d old — https://www.sourcee.app/journo-request/founders-and-leaders-mindsets-and-milestones
- [low] 17d old — https://www.sourcee.app/journo-request/london-businesses-stopped-using-ai-hiring-tools
- [low] 17d old — https://www.sourcee.app/journo-request/creative-industry-professionals-podcast-on-ai-impact
- [low] 17d old — https://www.sourcee.app/journo-request/former-ai-skeptics-changed-views-on-ai-impact
- [low] 18d old — https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- [low] 18d old — https://www.sourcee.app/journo-request/employers-and-recruiters-over-50s-adapting-to-ai
- [low] 18d old — https://www.sourcee.app/journo-request/data-center-professionals-podcast-guest-ai-and-hyperscale-trends
- [low] 18d old — https://www.sourcee.app/journo-request/patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges
- [low] 18d old — https://www.sourcee.app/journo-request/ml-researchers-continuous-learning-fast-weights-and-adapters
- [low] 18d old — https://www.sourcee.app/journo-request/founders-55-latelife-entrepreneurship-series-1
- [low] 18d old — https://www.sourcee.app/journo-request/founders-and-entrepreneurs-and-musicians-podcast-guests
- [low] 19d old — https://www.sourcee.app/journo-request/ai-alignment-researchers-humanai-mutual-understanding
- [low] 20d old — https://www.sourcee.app/journo-request/companies-that-stopped-emailing-pdfs-new-tools-and-transition
- [low] 21d old — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 21d old — https://www.sourcee.app/journo-request/gen-z-ai-data-annotators-work-experience-and-income-impact
- [low] 21d old — https://www.sourcee.app/journo-request/ai-automation-experts-speakers-on-marketing-sales-operations-gains
- [low] 21d old — https://www.sourcee.app/journo-request/ecommerce-marketers-transparency-in-ai-recommendations-and-conversion
- [low] 22d old — https://www.sourcee.app/journo-request/cybersecurity-companies-and-experts-ai-scams-and-consumer-safety

---

## Clearing the queue

After sending, record it so the row does not reappear:

```json
{"pitched": {"<url>": "2026-09-15"}, "skipped": {"<url>": "reason"}}
```

Ledger: `marketing/haro-outreach/pitch-ledger.json`
