# Pitch queue — clear this in one pass

Built 2026-11-19 from 348 unique requests across the digest history. **2 sendable**, 82 live, 257 cold (> 10 days and unpitched), 42 expired on the platform.

**2 finished drafts are ready to send now — 'Send these now' below names each route; 2 of them are inside the 10-day line.**

*"Sendable" is the number that matters and the one the headline used to hide: a live page is not a candidate. A row counts as sendable only when it is live, not cold, not dropped off, not already pitched, ranked above the tangential band, and has a resolved reply route (a published email, a named handle, a booking link). The other live rows are off-beat calls this queue already documents as excluded.*

**Ages are read off each request page** (`datePublished`), not off the digest text — see `marketing/haro-outreach/verified-requests.json`, refreshed by `scripts/verify_journo_requests.py`. An earlier build fell back to the digest's first-seen date and showed a 190-day-old request as 8 days old.

**No renewal signal exists on this source.** Sourcee publishes no renewal signal: on the 300 most recently indexed slugs and all 30 slugs of the live AI topic feed (checked 2026-09-19) the sitemap lastmod is byte-identical to datePublished, so 'never refreshed' is not observable and is not claimed here. Cold means old and unpitched, not provably abandoned.

**No NEW expiry in the 2026-11-19 run — but 44 carried requests are already dead.** Each answered HTTP 404 again and remains absent from the sitemap; the 2026-11-19 digest did not record a fresh wave. The rule stands: a row can disappear between two runs a day apart, so a live row is worth sending today.

**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, Qwoted and Medialyst need authenticated sessions, and Sourcee redacts the requester's own address in the request body. That is the friction that produced zero sends from the first 43 flagged opportunities. Reply routes are named per row — including addresses resolved off the *publication's* own site (a byline page or an editorial contact page), which is now the strongest route class in this queue.

## Drafts that exist and were never sent

Read this before clearing the queue: 58 draft files exist on disk. **3 of the pitches drafted here have now been sent** — listed at the bottom, not as work. The rest are still unsent; a written draft is not progress — the send is.

**THE QUEUE HOLDS 2 SENDABLE ROW(S).** A row is declared sendable on two facts evidenced separately rather than trusted from a digest field: a relevance above the tangential band, and a reply route verified by fetching a page today. Both are named in the row. The previous run reported 2; the last run before it with a non-zero count was 2026-11-18, with 0 consecutive zero run(s) in between. The live unpitched set is 82 rows.

**Today's draft file is `pitch-drafts-2026-11-19.md` (derived from disk, not typed).** The headline figures are re-derived every run: 51 of 124 tools publish a monthly price, 42 of those at or under $25/month, median $15.00 (snapshots `updated: 2026-11-19`). Superseded sets still sitting in older dated drafts (40/31/$16.50 and earlier) must not be reused.

**The pair range is `1.11x to 2.53x, median 1.25x` over 19 tiers, and it held today.** History, because every superseded value is still sitting in dated draft files and must not be reused: the range was first published as `1.21x to 2.53x, median 1.33x` (2026-09-18, sent to a real correspondent — wrong because the pair population was regex-dependent and undefined); corrected to `1.16x to 2.53x, median 1.25x` over 18 curated pairs (2026-09-21); then re-derived to `1.11x to 2.53x` when the replit-ai snapshot was refreshed (2026-09-22). See `data/monthly_annual_pairs.json` and `scripts/extract_monthly_annual_pairs.py`, which refuses to write the file at all unless every curated pair re-asserts against the live snapshot.

- anthropic-users-and-business-owners-customer-service-experiences — **Crossed cold 2026-09-23; now 69d old — no longer counted as sendable.** Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal hliwrites.99 (re-read verbatim off the live page 2026-09-30). Send late or record as skipped in `pitch-ledger.json`; the crossing is logged in `cold_without_a_send`.
- employees-blocked-from-ai-on-work-accounts-automating-tedious-ta — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — §3 in `pitch-drafts-2026-10-27.md`. Now 45d old.** Route: LinkedIn DM to linkedin.com/in/christopher-mims-club/ (LinkedIn byline page — route-checks probe 2026-11-19: HTTP 200, 571,926 bytes, title 'Christopher Mims - The Wall Street Journal | LinkedIn'; the request's own body says '(DMs open)'; muckrack.com/christopher-mims 403 and wsj.com/news/author/christopher-mims 401 are dead ends, not routes — both re-checked in the same 2026-11-19 probe). It has left the sendable count: the row is now past the 10-day line and this queue no longer ranks it as actionable. The route is not dead and the draft named above is still paste-ready — George's call is to send it late or record it skipped in `pitch-ledger.json`. Silence is the one option that leaves it drifting.
- finops-professionals-agentic-ai-cost-overruns — **Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1. Now 73d old.** Route: LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 and still unsent — the longest-standing high-relevance request this monitor has never answered. Send it late or drop it, do not draft it a fifth time.
- tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — §3 in `pitch-drafts-2026-10-28.md`. Now 40d old, carried in 27 draft files.** Route: hello@tobiamure.com, the address the journalist publishes himself on his own site — tobiamure.com homepage — route-checks probe 2026-11-19: HTTP 200, 63,335 bytes, title 'Tobi Amure, CFEI® | Finance &amp; Technology Journalist', with the contact form on tobiamure.com/contact — route-checks probe 2026-11-19: HTTP 200, 18,470 bytes, title 'Contact Tobi Amure | Finance &amp; Technology Journalist' as the fallback if mail bounces. Deliverability is NOT SMTP-verified: the domain's MX answers 554 Relay access denied for a real address, a fake control and postmaster@ alike, so that probe discriminates nothing. He asks for 'original data, or a survey with its sample size and method' and refuses DM pitches, which is why the draft leads with the one measured series we hold. Past the 10-day line the send is still possible — a late send or a ledger entry closes it; silence leaves it drifting exactly as the WSJ row did on 2026-10-16.

### Already sent — do NOT re-send

- fulltime-employees-shadow-ai-use-and-paying-outofpocket — **SENT BUT BOUNCED — the address is dead, do not retry it; a fresh route is needed before this row can be sent at all.** `pitch-ledger.json`: 2026-10-10 (SENT BUT BOUNCED - see log)
- google-and-claude-enterprise-users-seats-and-token-costs — SENT. `pitch-ledger.json`: 2026-10-10
- speciality-food-retailers-and-producers-how-theyd-spend-10k-on-t — SENT. `pitch-ledger.json`: 2026-10-10

## Send these now (2) — a finished draft and a live route

Each row below has a finished, paste-ready pitch in `pitch-drafts-2026-11-19.md` and a page that served the request today. All 2 are inside the 10-day line. A send, or a `skipped` entry in `pitch-ledger.json`, closes each one. A rewrite of the same draft does not.

- **§1 in `pitch-drafts-2026-11-19.md`** — https://www.sourcee.app/journo-request/former-software-engineers-left-tech-after-ai-coding-tools — 3d old, page live today, route `tspirlet@businessinsider.com`
- **§2 in `pitch-drafts-2026-11-19.md`** — https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai — 9d old, page live today, route `kelsey.ziser@informationweek.com`

## Sendable — pitch these (2)

Live, not cold, ranked above the tangential band, and with a reply route a human can actually use. This is the whole actionable queue.

**1 of these cross the 10-day cold line within two days. Past it, they leave this section and nothing brings them back:**

- https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai — 9d old, crosses the line TOMORROW

### [medium] AI Coding Tools / Vendor Switching / Software Careers
- **URL:** https://www.sourcee.app/journo-request/former-software-engineers-left-tech-after-ai-coding-tools
- **Posted:** 3d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-17, last 2026-11-19 (3x)
- **Publication:** Thibault Spirlet - Business Insider (author field in the page's JSON-LD reads 'Thibault Spirlet') · domain businessinsider.com
- **Reply route:** Body says 'please DM me or email me at [email redacted]' - Sourcee redacts the address and the page publishes no handle of the poster's own. His byline page businessinsider.com/author/thibault-spirlet publishes tspirlet@businessinsider.com in a mailto link (re-probed today, HTTP 200, 319,992 bytes, address 5 times in the markup), which is the route used in the draft. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: tspirlet@businessinsider.com (George sends)_
- **Angle:** Email to tspirlet@businessinsider.com (route resolved off his Business Insider byline page, re-probed 2026-11-18: HTTP 200). Subject: 'The per-seat arithmetic in your Mistral switchers call'. Open with the dated switching comparison: Mistral Vibe (Le Chat) Pro $14.99/month and Team $24.99 per user/month against ChatGPT Plus $20/month and Claude Pro $20 month-to-month or $17 on a $200 annual […] (full angle in the digest entry for this row)

### [low-medium] AI / Enterprise Spend / SaaS Pricing Pressure
- **URL:** https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai
- **Posted:** 9d old (page datePublished (page probed 2026-11-19)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-10, last 2026-11-19 (10x)
- **Publication:** InformationWeek (informationweek.com) - Kelsey Ziser, Senior Editor, named in the page's author field. · domain informationweek.com
- **Reply route:** Route resolved OFF the request page, not guessed: kelsey.ziser@informationweek.com, published as a mailto link on her InformationWeek author page https://www.informationweek.com/author/kelsey-ziser (route-checks-2026-11-19.json: HTTP 200, 584,322 bytes  ·  _no — email resolved off the publication's own site: kelsey.ziser@informationweek.com (George sends)_
- **Angle:** Email to kelsey.ziser@informationweek.com (mailto on her InformationWeek author page, re-probed 2026-11-18: HTTP 200). Subject: 'The seat-price numbers behind the SaaSpocalypse question'. Open with one measured number from the 2026-11-19 snapshot: 51 of 124 tracked AI tools publish a monthly per-seat price, 42 of those at or under $25, median cheapest paid seat $15.00, with the cheapest paid seat […] (full angle in the digest entry for this row)

## Live but not sendable (80)

These pages resolve and the requests are unexpired, so they are recorded — but none has both a relevance above the tangential band and a usable route. They are listed for completeness, not as candidates: pitching any of them would mean claiming standing we do not have (see the exclusions in the newest `pitch-drafts-*.md`).

### [medium] AI / Pricing Models
- **URL:** https://www.sourcee.app/journo-request/companies-switched-from-token-ai-pricing-outcomebased-contracts
- **Posted:** 7d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Agam Shah, named in the page's author field; no publication stated on the page.
- **Reply route:** The page publishes no address, handle or link of its own, and the body names no contact route. Sourcee's redaction is not the reason: there is simply no route on the page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, and the ask excludes us by its own terms. NOT DRAFTED.

### [low-medium] AI / Labour Economics
- **URL:** https://www.sourcee.app/journo-request/labor-economists-unintended-consequences-of-automation
- **Posted:** 9d old (page datePublished (page probed 2026-11-19)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-19 (9x)
- **Publication:** Gavin Clarke, named in the page's author field; no publication stated.
- **Reply route:** The page publishes no address, handle or link of its own; the body says 'drop me a line' and gives nothing to drop it to. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route resolved. If a route is found, the angle is the annual-billing premium as an unrecognised adoption cost - 1.11x to 2.53x, median 1.25x over 19 same-tier pairs, asserted 2026-10-16 - offered as data, not as labour-economics expertise.

### [low] AI Infrastructure / Data Centres and Compute Cost
- **URL:** https://www.sourcee.app/journo-request/data-centre-operators-and-enterprise-cios-in-india-ai-capacity-and-costs
- **Posted:** 0d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Shrikanth Govindarajan - Dataquest (dataquest.in), print cover story · domain dataquest.in
- **Reply route:** Body asks for perspective and the page's address is platform-redacted; no handle, link or byline route is published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Off-beat: Indian data-centre capex and power costs; no pricing question we hold evidence on and no route.

### [low] Startups / Culture
- **URL:** https://www.sourcee.app/journo-request/startup-founders-time-off-for-gta-release-and-anthropic-ipo-coincidence
- **Posted:** 0d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Amanda Silberling - TechCrunch (techcrunch.com) · domain techcrunch.com
- **Reply route:** Body says 'emailed quotes OK [email redacted]'; the address is platform-redacted and no handle is published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Off-beat joke call about GTA and the Anthropic IPO; no pricing question and no route.

### [low] AI Markets / IPO and Valuation
- **URL:** https://www.sourcee.app/journo-request/investment-bankers-and-vcs-and-valuation-experts-ai-ipo-race-drivers
- **Posted:** 1d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-18, last 2026-11-19 (2x)
- **Publication:** Not named on the page - Times Group (timesgroup.com) request · domain timesgroup.com
- **Reply route:** Body says 'please feel free to DM me' and 'reach out to me here: [email redacted]'; Sourcee redacts the address and the page publishes no handle, link or byline of the poster's own. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Off-beat: capital-markets and valuation commentary on the AI IPO race; no pricing question we can answer and no route published.

### [low] B2B Marketing / AI Visibility and AEO
- **URL:** https://www.sourcee.app/journo-request/b2b-creators-and-agencies-impact-on-ai-visibility-and-aeo
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-18, last 2026-11-19 (2x)
- **Publication:** Not named on the page - an unnamed report author
- **Reply route:** Body names three wanted profiles and asks for no channel at all; the page publishes no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat: B2B creator/AEO practitioner research with no pricing question and no route published.

### [low] AI Policy / Agent-Centric Web
- **URL:** https://www.sourcee.app/journo-request/ai-agent-builders-and-researchers-agentcentric-web-policy-input
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-18, last 2026-11-19 (2x)
- **Publication:** Not named on the page - input sought for the UNESCO IFAP Information Literacy Working Group (ILWG)
- **Reply route:** Body says 'If you build, deploy or research...' and the page publishes one shortened link (https://lnkd.in/gPvrfnae) plus a 'Signal' hint; no address or handle is published. Links published on the page: https://lnkd.in/gPvrfnae.  ·  _no — published booking link https://lnkd.in/gPvrfnae (George)_
- **Links published on the page:** https://lnkd.in/gPvrfnae
- **Angle:** None - excluded. Off-beat: UNESCO policy consultation for AI agent builders and researchers; standing we do not have.

### [low] AI and Work / Agentic Customer Service
- **URL:** https://www.sourcee.app/journo-request/call-center-and-customer-service-reps-ai-agent-phone-calls-impact
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Issie Lapowsky - columnist (page names no publication; body says 'an upcoming column on AI and work')
- **Reply route:** Body says 'Reach out at [email redacted] or issielapowsky.08 on Signal'. The Signal handle is the only published route and is a reporter's own handle, not an address on the request page. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. First-hand call-centre testimony only; we hold no such experience.

### [low] Freelance Work / AI Productivity
- **URL:** https://www.sourcee.app/journo-request/freelancers-using-ai-tools-rising-income-and-more-work
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Ellen Sheng - CNBC (cnbc.com) · domain cnbc.com
- **Reply route:** Body says 'email me at [email redacted]'; the address is platform-redacted and the page publishes no handle or link. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Freelancer income testimony; no pricing question we can answer as a publisher and no route.

### [low] Corporate Governance
- **URL:** https://www.sourcee.app/journo-request/board-directors-and-governance-advisers-nvidia-ceo-crisis-prevention
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Matt Kelly - no publication named on the page
- **Reply route:** Body says 'Reach out if interested'; no address, handle or link is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Board governance commentary with no pricing question and no route.

### [low] Logistics / GIS
- **URL:** https://www.sourcee.app/journo-request/truck-drivers-nomap-mishaps-and-gis-ai-future
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** The Open Road w/ KC Phillips - podcast (no publication domain)
- **Reply route:** Page publishes one shortened link (https://t.co/yrokZsDvOF); no address or handle of the poster's own. Links published on the page: https://t.co/yrokZsDvOF.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/yrokZsDvOF
- **Angle:** None - excluded. Trucking podcast booking; no pricing question and no route.

### [low] AI Markets / IPO
- **URL:** https://www.sourcee.app/journo-request/anthropic-investors-bull-and-bear-case-ahead-of-ipo
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Jennifer Sor - Business Insider (businessinsider.com) · domain businessinsider.com
- **Reply route:** Body says 'email [email redacted]'; the address is platform-redacted and the page publishes no handle. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Investor testimony requiring receipts; we are not an Anthropic investor and no route is published.

### [low] Banking Risk / AI Governance
- **URL:** https://www.sourcee.app/journo-request/apac-banking-risk-officers-ai-agents-accelerating-bank-runs
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Vince Dioquino - page names no publication
- **Reply route:** Body says 'Please message me or leave a comment so I can reach out'; no address or handle is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. APAC banking-risk commentary; no pricing question and only a platform comment as a route.

### [low] Consumer AI / Property
- **URL:** https://www.sourcee.app/journo-request/estate-agents-and-buyers-affected-by-housefishing-ai-listing-photos
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Emily Braeger - The i Paper (theipaper.com) · domain theipaper.com
- **Reply route:** Body says 'Pls email me at [email redacted]'; the address is platform-redacted and no handle is published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. First-hand housefishing testimony; address redacted and no route.

### [low] AI Markets / IPO
- **URL:** https://www.sourcee.app/journo-request/uk-retail-investors-who-bought-anthropic-preipo-anthropic-ipo
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Maisie Grice - City A.M. (cityam.com) · domain cityam.com
- **Reply route:** Body says 'Please email [email redacted]'; redacted, no handle published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. UK retail investor testimony, same-day deadline implied; no route and no pricing question.

### [low] AI Markets / IPO
- **URL:** https://www.sourcee.app/journo-request/british-private-investors-anthropic-ipo-plans
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Callum Martin - The Times (thetimes.co.uk) · domain thetimes.co.uk
- **Reply route:** Body says 'please reach out at [email redacted]'; redacted, no handle published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Private-investor testimony; no route and no pricing question.

### [low] AI in Emerging Markets
- **URL:** https://www.sourcee.app/journo-request/nigerian-ai-founders-realworld-ai-solving-local-problems
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Dr Chioma Ezenwafor - page names no publication
- **Reply route:** Body says 'DM me with a one-line description'; no address, handle or link is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Nigerian founder profile call; standing we do not have and no route.

### [low] AI / Podcast Booking
- **URL:** https://www.sourcee.app/journo-request/ai-experts-and-industry-leaders-use-cases-jobs-ethics
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Chetan K. - Kicckutalks podcast (no publication domain)
- **Reply route:** Body says 'Send me a DM or comment AI EXPERT below'; no address or handle of the poster's own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Podcast guest booking; no pricing question and no route.

### [low] Consumer Finance
- **URL:** https://www.sourcee.app/journo-request/consumers-panic-buying-and-hoarding-cash-outages-and-market-fears
- **Posted:** 1d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-19, last 2026-11-19 (1x)
- **Publication:** Genna - MarketWatch (marketwatch.com) · domain marketwatch.com
- **Reply route:** Body says 'Email me if interested [email redacted]'; redacted, no handle published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Consumer panic-buying testimony; AI is incidental, address redacted, no route.

### [low] AI Risk / Preparedness
- **URL:** https://www.sourcee.app/journo-request/lab-researchers-and-ai-preppers-ai-doom-prep-land-metals-weapons
- **Posted:** 2d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-17, last 2026-11-19 (3x)
- **Publication:** Not named on the page
- **Reply route:** Body says 'shoot me a DM'; no address, handle or link is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat: AI-doom preparedness testimony; no pricing question and no route.

### [low] Prompt Engineering / Bot Syntax
- **URL:** https://www.sourcee.app/journo-request/ai-experts-bot-syntax-and-prompt-structure
- **Posted:** 2d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-17, last 2026-11-19 (3x)
- **Publication:** Not named on the page
- **Reply route:** Body says 'ping me by chat'; the page publishes no address, handle or link. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat: prompt-syntax expertise with no pricing question and no route.

### [low] Consumer AI / Divorce and Co-parenting
- **URL:** https://www.sourcee.app/journo-request/divorcing-adults-who-used-ai-personal-stories-about-impact
- **Posted:** 2d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-17, last 2026-11-19 (3x)
- **Publication:** Not named on the page - Insider · domain insider.com
- **Reply route:** Body says 'Email me at [email redacted]'; the address is platform-redacted and no handle is published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Off-beat: personal divorce testimony; address redacted, no route.

### [low] Consumer AI / Family Labour
- **URL:** https://www.sourcee.app/journo-request/parents-using-ai-tools-invisible-labor-in-relationships
- **Posted:** 2d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-17, last 2026-11-19 (3x)
- **Publication:** Not named on the page - The Washington Post · domain washingtonpost.com
- **Reply route:** Body says 'Let me know your experience by emailing me: [email redacted]'; the address is platform-redacted and no handle is published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Off-beat: household testimony about AI and invisible labour; address redacted, no route.

### [low] Accounting Software / Expert Quote
- **URL:** https://www.sourcee.app/journo-request/cpas-choosing-best-accounting-software-forbes-advisor
- **Posted:** 2d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-17, last 2026-11-19 (3x)
- **Publication:** Forbes Advisor source request - poster's name not given on the page · domain forbes.com
- **Reply route:** Body says 'comment for more info or send me a message'; no address, handle or link is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat (CPA quote for Forbes Advisor); 'AI' appears only in the instruction that the quote be original, and no route is published.

### [low] Visual Arts / AI and Culture
- **URL:** https://www.sourcee.app/journo-request/flemish-visual-artists-against-ai-college-magazine-article
- **Posted:** 2d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-18, last 2026-11-19 (2x)
- **Publication:** Not named on the page - college magazine
- **Reply route:** Body says 'Contact me!' but the page publishes no address, handle or link. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat: Flemish artist testimony; no pricing question and no route.

### [low] Higher Education / AI Faculty Roles
- **URL:** https://www.sourcee.app/journo-request/ai-faculty-fellows-and-supervisors-role-between-policy-tech-curriculum
- **Posted:** 2d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-18, last 2026-11-19 (2x)
- **Publication:** Not named on the page - the poster says she started in an AI faculty fellow role this fall
- **Reply route:** Body shares a survey link (https://lnkd.in/gch_xGQk) and asks people to comment or tag colleagues; no address or handle of the poster's own is published. Links published on the page: https://lnkd.in/gch_xGQk.  ·  _no — published booking link https://lnkd.in/gch_xGQk (George)_
- **Links published on the page:** https://lnkd.in/gch_xGQk
- **Angle:** None - excluded. Off-beat: survey of AI faculty fellows; standing we do not have.

### [low] Newsletter Industry / Media Business
- **URL:** https://www.sourcee.app/journo-request/publishers-creators-and-media-brands-state-of-newsletter-report-2027
- **Posted:** 2d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-18, last 2026-11-19 (2x)
- **Publication:** Not named on the page - beehiiv's annual State of Newsletter report · domain beehiiv.com
- **Reply route:** Body points at a Tally survey (https://tally.so/r/rDDdP2) and asks for comments; no address or handle is published. Links published on the page: https://tally.so/r/rDDdP2.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://tally.so/r/rDDdP2
- **Angle:** None - excluded. Off-beat: newsletter-industry survey where we would be overstating our standing; no route.

### [low] Consumer AI / Property
- **URL:** https://www.sourcee.app/journo-request/home-hunters-and-renters-misleading-aigenerated-listing-photos
- **Posted:** 2d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-18, last 2026-11-19 (2x)
- **Publication:** Not named on the page - The Sun · domain thesun.co.uk
- **Reply route:** Body says 'Email me: [email redacted]'; the address is platform-redacted and no handle is published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Off-beat: consumer testimony about AI listing photos; address redacted, no route.

### [low] Comics / AI Consent / Creator Rights
- **URL:** https://www.sourcee.app/journo-request/comic-book-writer-greg-pak-ai-consent-and-digital-comics
- **Posted:** 3d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-16, last 2026-11-19 (4x)
- **Publication:** Weird City Media - poster's name not given on the page (author field reads 'Weird City Media'); the request is addressed to the comic writer Greg Pak (@gregpak.net)
- **Reply route:** The request body is a single line asking @gregpak.net for 'the best way to get in touch with you for a story on AI consent and digital comics'. The page publishes no address, handle or link of its own, so there is no route to the poster at all. The page publishes no address, handle or link of its own.  ·  _no — email resolved off the publication's own site (George sends)_
- **Angle:** None - excluded. Off-beat: a contact-route request aimed at one named comic writer, with no pricing question and no route to the poster.

### [low] Tech Layoffs / Future of Work
- **URL:** https://www.sourcee.app/journo-request/bay-area-tech-workers-laid-off-last-6-months-roles-changed-by-ai
- **Posted:** 3d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-16, last 2026-11-19 (4x)
- **Publication:** Basem Istanbouli - (un)PTO, a Bay Area layoff community of ~2,000 people
- **Reply route:** Body says 'DM me a short blurb about your story'. No address, no handle and no link is published on the page. The page publishes no address, handle or link of its own.  ·  _no — platform reply (George)_
- **Angle:** None - excluded. Off-beat: first-hand layoff testimony from named workers; no pricing question and no route.

### [low] Podcast Guest Booking / Entrepreneurship
- **URL:** https://www.sourcee.app/journo-request/basementborn-entrepreneurs-built-businesses-despite-doubters
- **Posted:** 3d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-16, last 2026-11-19 (4x)
- **Publication:** Jen Josey - Comfort to Courage Podcast (guest booking)
- **Reply route:** No address and no link published on the page; the call says to pitch a personal founding story. Sourcee's redaction is not the reason there is no route - the body simply publishes none. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat: personal founding-story booking that names consultants and advisors as excluded, with one incidental AI mention.

### [low] Software Engineering / AI Coding Tools
- **URL:** https://www.sourcee.app/journo-request/software-developers-ai-impact-on-development-practices
- **Posted:** 3d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-17, last 2026-11-19 (3x)
- **Publication:** Not named on the page - the call is addressed to software developers
- **Reply route:** Body says 'DM or comment below'; the page publishes no address, handle or link. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat: practitioner testimony from working developers; no pricing question and no route.

### [low] Enterprise AI / Funding, Ownership and ROI / Conference Sourcing
- **URL:** https://www.sourcee.app/journo-request/cios-ctos-and-senior-tech-leaders-working-with-ai-cio-summit-nyc-feb
- **Posted:** 3d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-17, last 2026-11-19 (3x)
- **Publication:** GDS Group CIO Summit portfolio - poster's name not given on the page; the call is addressed to CIOs, CTOs and senior technology leaders attending the New York edition in February
- **Reply route:** Body says 'please do comment below or drop me a message if you have thoughts'; the page publishes no address, no handle and no link of its own, so there is no route to the poster at all. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Asks CIOs/CTOs for funding, ownership and ROI experience we do not hold; the page publishes no route.

### [low] Consumer AI / Daily Life
- **URL:** https://www.sourcee.app/journo-request/chatgpt-users-use-ai-to-run-their-lives-and-been-called-meat-proxy
- **Posted:** 3d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-17, last 2026-11-19 (3x)
- **Publication:** Not named on the page
- **Reply route:** Body says 'my DMs are open' but publishes no handle, address or link. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat: consumer ChatGPT testimony with no route.

### [low] UK Tech / Nvidia / Infrastructure and Geopolitics
- **URL:** https://www.sourcee.app/journo-request/uk-tech-leaders-nvidia-role-in-infrastructure-finance-and-geopolitics
- **Posted:** 3d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-17, last 2026-11-19 (3x)
- **Publication:** Not named on the page
- **Reply route:** Body says 'please DM me in confidence'; no handle, address or link is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat: UK tech-leader commentary on Nvidia; standing we do not have and no route.

### [low] UK Tech Labour / AI Coding Tools
- **URL:** https://www.sourcee.app/journo-request/uk-developers-ai-impact-on-job-satisfaction-and-careers
- **Posted:** 3d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-17, last 2026-11-19 (3x)
- **Publication:** Not named on the page - the call is addressed to UK-based software engineers and developers
- **Reply route:** Body says 'DM / email: [email redacted]'; Sourcee redacts the address and no handle is published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Off-beat: UK developer testimony on job satisfaction; address redacted, no route.

### [low] Trade Magazine / Fluid Power / Byline Contribution
- **URL:** https://www.sourcee.app/journo-request/cfpa-members-and-fluid-power-experts-spring-2027-articles
- **Posted:** 3d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-17, last 2026-11-19 (3x)
- **Publication:** Richard Cowan - 'Your World in Motion', published for the Canadian Fluid Power Association (CFPA)
- **Reply route:** Body says to send an abstract to Richard Cowan at [email redacted]; the address is platform-redacted and no handle is published. The request body's address is redacted by Sourcee. Links published on the page: https://lnkd.in/g4G8c6Eq.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Links published on the page:** https://lnkd.in/g4G8c6Eq
- **Angle:** None - excluded. Off-beat (fluid-power trade bylines, abstracts due 2027-01-04); 'AI' is a contributor's job title, and the address is platform-redacted.

### [low] Literature / Climate & Environmental Justice / Submissions Call
- **URL:** https://www.sourcee.app/journo-request/women-writers-in-global-south-climate-care-and-environmental-justice
- **Posted:** 4d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-15, last 2026-11-19 (5x)
- **Publication:** Poetry Wales / MODRON magazine — editorial call from the publication itself (no journalist named; page author field is blank) · domain poetrywales.co.uk
- **Reply route:** Pitch by following the two lnkd.in short links published in the body (one to MODRON's pitch call, one to the UN Women fact sheet). No address and no handle of the author's own is published; Sourcee's redaction is not the reason. Links published on the page: https://lnkd.in/e_EwSdD6, https://lnkd.in/eu9mQYZK.  ·  _no — published booking link https://lnkd.in/e_EwSdD6 (George)_
- **Links published on the page:** https://lnkd.in/e_EwSdD6, https://lnkd.in/eu9mQYZK
- **Angle:** None — excluded. Off-beat: a literary submissions call whose only AI mention is a data-centre electricity aside; no spend angle, no route of the author's own, and no standing for us.

### [low] AI Economics / Tokenomics / Byline Contribution
- **URL:** https://www.sourcee.app/journo-request/ai-economist-tokenomics-and-market-winners-selfhosting-viability
- **Posted:** 4d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-16, last 2026-11-19 (4x)
- **Publication:** Theophile Cantelobre - Revue des Mines (revue-mines.org), a community-run magazine for the Mines engineering alumni and academic network · domain revue-mines.org
- **Reply route:** Body says 'DM me or write to [email redacted]'; the page publishes no address, handle or link of its own and Sourcee has redacted the one address the poster offered. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded despite being on-beat-adjacent. Asks for tokenomics expertise and an authored French print article; we hold seat/subscription prices only, the address is platform-redacted and no DM handle is published.

### [low] AI Safety / Governance / Interview Sourcing
- **URL:** https://www.sourcee.app/journo-request/ai-safety-leaders-physical-ai-safety-and-zerotrust-infrastructure
- **Posted:** 4d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-16, last 2026-11-19 (4x)
- **Publication:** Luiza Jarovsky, PhD - AI governance newsletter (103,000+ subscribers), recapping her GTC Berlin interviews
- **Reply route:** Body says 'write to me' but publishes no address, handle or link; the only link offered is to her newsletter and the 15-minute interview. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat: AI-safety interview sourcing in a newsletter recap; no pricing question, no standing, no published route.

### [low] Physical AI / Podcast Interviews
- **URL:** https://www.sourcee.app/journo-request/employees-at-anduril-and-9-ai100-firms-build-hire-and-sell
- **Posted:** 4d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-16, last 2026-11-19 (4x)
- **Publication:** Michael Finocchiaro - ThreadMoat / 'AI Across the Product Lifecycle' podcast
- **Reply route:** Publishes one lnkd.in short link to the podcast; no address and no handle of the poster's own. The call is for employees of ten named companies or people who can introduce them. Links published on the page: https://lnkd.in/eezQ6K5U),.  ·  _no — published booking link https://lnkd.in/eezQ6K5U), (George)_
- **Links published on the page:** https://lnkd.in/eezQ6K5U),
- **Angle:** None - excluded. Off-beat: named-employer podcast sourcing; standing we do not have and no route of the poster's own.

### [low] AI / Hiring Testimony
- **URL:** https://www.sourcee.app/journo-request/job-seekers-postai-interviews-and-recruiters-ai-interview-impact
- **Posted:** 6d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Jordan Friedman, named in the page's author field; no publication stated.
- **Reply route:** The body says 'comment or DM'; the page publishes no handle or link to either. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Enterprise IT Testimony
- **URL:** https://www.sourcee.app/journo-request/midsize-manufacturing-it-leaders-ai-impact-on-tasks-teams-governance
- **Posted:** 6d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Dan Tynan, named in the page's author field; domain freshworks.com. · domain freshworks.com
- **Reply route:** One shortlink published on the page: https://lnkd.in/gjjANXqs (not resolved; the page states no address). Links published on the page: https://lnkd.in/gjjANXqs.  ·  _no — published booking link https://lnkd.in/gjjANXqs (George)_
- **Links published on the page:** https://lnkd.in/gjjANXqs
- **Angle:** None. Standing explicitly excluded. NOT DRAFTED.

### [low] AI / Workplace Adoption
- **URL:** https://www.sourcee.app/journo-request/employees-using-ai-avatars-training-and-support-zdnet
- **Posted:** 6d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Radhika Rajkumar, named in the page's author field; domain zdnet.com. · domain zdnet.com
- **Reply route:** The body asks readers to reply 'in the comments'; the page publishes no address or handle. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Podcast Guest Call
- **URL:** https://www.sourcee.app/journo-request/us-retail-executives-agentic-ai-shopping-in-ecommerce
- **Posted:** 6d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Russell Goldsmith, named in the page's author field; no publication stated (the body describes 'our own channel, the c-suite podcast').
- **Reply route:** The page publishes no address, handle or link; the body invites guest pitches without a route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Not our standing, no route. NOT DRAFTED.

### [low] EV / Whistleblower Call
- **URL:** https://www.sourcee.app/journo-request/ev-industry-employees-insider-stories-and-source-protection
- **Posted:** 6d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Suvrat Kothari, named in the page's author field; domain insideevs.com. · domain insideevs.com
- **Reply route:** The body's email is redacted by Sourcee. A Signal handle is published: @suvratk.13. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None. Not an AI request, no standing. NOT DRAFTED.

### [low] Tech / Outage Testimony
- **URL:** https://www.sourcee.app/journo-request/microsoft-365-users-email-outage-impact-on-workflows
- **Posted:** 6d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-14, last 2026-11-19 (6x)
- **Publication:** Ricky Boleto, BBC News (page author field; domain bbc.co.uk). · domain bbc.co.uk
- **Reply route:** The page publishes no address and no handle. One shortlink is embedded in the body: https://t.co/Wm8BPSYAzN, which is a BBC News link, not a reply route. Links published on the page: https://t.co/Wm8BPSYAzN.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/Wm8BPSYAzN
- **Angle:** None. Not an AI request and no route. NOT DRAFTED.

### [low] AI / Consumer Testimony
- **URL:** https://www.sourcee.app/journo-request/individuals-accused-of-using-ai-misattribution-experiences
- **Posted:** 6d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-14, last 2026-11-19 (6x)
- **Publication:** Suzanne Bearne, freelance journalist writing for national titles (no publication named on the page).
- **Reply route:** The body lists three separate asks and says 'PRs and agents, email me' for the celebrity slots only; no address, handle or link is published anywhere on the page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Podcast Guest Call
- **URL:** https://www.sourcee.app/journo-request/servicenow-customers-and-partners-podcast-guests-ai-and-career-stories
- **Posted:** 6d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-14, last 2026-11-19 (6x)
- **Publication:** Brogan Howie, ServiceNow (domain servicenow.com). · domain servicenow.com
- **Reply route:** No address or handle published. One shortlink in the body: https://lnkd.in/eDkSrN6T, which points at the ServiceNow podcast series, not at a reply route. Links published on the page: https://lnkd.in/eDkSrN6T.  ·  _no — published booking link https://lnkd.in/eDkSrN6T (George)_
- **Links published on the page:** https://lnkd.in/eDkSrN6T
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Workplace Testimony
- **URL:** https://www.sourcee.app/journo-request/israeli-software-developers-ai-impact-on-jobs
- **Posted:** 6d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-14, last 2026-11-19 (6x)
- **Publication:** Daniela Fubini (page author field); the request itself is from Gianluca Pacchiani. No publication named on the page.
- **Reply route:** The page publishes no address, handle or link; the body says 'Tag your friends' on LinkedIn and gives nothing to send to. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Local Inference
- **URL:** https://www.sourcee.app/journo-request/local-model-operators-10-prod-inference-and-7-figure-biz
- **Posted:** 6d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-14, last 2026-11-19 (6x)
- **Publication:** Brad, no surname and no publication named on the page.
- **Reply route:** The page publishes no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Labour Testimony
- **URL:** https://www.sourcee.app/journo-request/ramp-crews-and-gate-agents-hardest-and-best-job-moments
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-19 (8x)
- **Publication:** Plan0gram (plan0gram.com/bs) - the byline on the page; no publication named.
- **Reply route:** No address, handle or link published on the request page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Podcast Promo
- **URL:** https://www.sourcee.app/journo-request/innovators-and-changemakers-neuroscience-ai-future-of-work
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-19 (8x)
- **Publication:** Pamela Cowan, Build Resilience International - the byline on the page; no publication named.
- **Reply route:** No address, handle or link published on the request page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Promo post, no route. NOT DRAFTED.

### [low] AI / Education Testimony
- **URL:** https://www.sourcee.app/journo-request/teachers-and-school-leaders-ai-in-school-devices-student-wellbeing
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-19 (8x)
- **Publication:** Wired (wired.com) - domain field on the page; the author field carries a display name, not a byline. · domain wired.com
- **Reply route:** The request body's address is redacted by Sourcee ('Hit me up at [email redacted]'). The page publishes no link or handle of its own. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Adoption Testimony
- **URL:** https://www.sourcee.app/journo-request/accountants-and-bookkeepers-who-dont-use-ai-why-they-opt-out
- **Posted:** 7d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-19 (8x)
- **Publication:** Debra Kilsheimer - the byline on the page; no publication named.
- **Reply route:** The body invites a comment or a private message on the platform the post came from; no address published on the request page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Small Business Risk
- **URL:** https://www.sourcee.app/journo-request/small-businesses-aidriven-cyber-risks-and-affordable-protections
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-19 (8x)
- **Publication:** Samantha J. Subin, CNBC (cnbc.com) - domain and byline on the page. · domain cnbc.com
- **Reply route:** The request body's address is redacted by Sourcee, but the page publishes a Signal handle: ssubin.51. No email and no LinkedIn link on the page. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Route exists (Signal ssubin.51) but no standing and no on-beat data. NOT DRAFTED.

### [low] AI / Industry News Reaction
- **URL:** https://www.sourcee.app/journo-request/frontier-ai-industry-insiders-huang-resignation-impact-and-next-steps
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Greta Reich, named in the page's author field; domain usatoday.com. · domain usatoday.com
- **Reply route:** The body's email is redacted by Sourcee. A Signal handle is published in the body: gretareich.19. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Routable but off-beat. NOT DRAFTED.

### [low] AI / Policy News Reaction
- **URL:** https://www.sourcee.app/journo-request/ai-leader-jensen-huang-resignation-ai-policy-and-china
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Emilia David, named in the page's author field; domain ismg.io (Information Security Media Group). · domain ismg.io
- **Reply route:** The body's email is redacted by Sourcee; the page publishes no other route. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Voter Testimony
- **URL:** https://www.sourcee.app/journo-request/midterm-voters-on-ai-data-center-measure-why-they-voted
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Ginny Hogan, named in the page's author field; no publication stated.
- **Reply route:** The body's email is redacted by Sourcee; no other route published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Industry News Reaction
- **URL:** https://www.sourcee.app/journo-request/ai-startup-founders-jensen-huang-resignation-impact-and-opensource
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Aaron Mok, named in the page's author field; domain inc.com. · domain inc.com
- **Reply route:** The body's email is redacted by Sourcee; no other route published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Channel Partner Testimony
- **URL:** https://www.sourcee.app/journo-request/msp-owners-resellers-and-integrators-ai-ops-security-and-supply-chain
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Victoria Durgin, named in the page's author field; domain channelinsider.com. · domain channelinsider.com
- **Reply route:** The body's email is redacted by Sourcee. It also offers 'message me here', which is a platform reply on Sourcee itself, and an in-person meeting at an Ingram event. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Wrong standing, no draft.

### [low] AI / Podcast Guest Call
- **URL:** https://www.sourcee.app/journo-request/berlin-london-and-sf-ai-founders-and-tech-execs-podcast-tech-landscape
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Sowmya Guru, named in the page's author field; no publication stated.
- **Reply route:** The body asks for 'comments' and mentions people in them; no address, handle or link is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Consumer Testimony
- **URL:** https://www.sourcee.app/journo-request/individuals-and-small-businesses-accused-of-using-ai-false-allegations
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Suzanne Bearne, named in the page's author field; no publication stated (the body says 'a national').
- **Reply route:** The body says 'DM me'; no handle or link is published on the page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] Consumer Finance / Case Study
- **URL:** https://www.sourcee.app/journo-request/parents-of-students-with-loans-managing-cost-and-sacrifices-ipaper
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** Maria Shahid, named in the page's author field; domain inews.co.uk. · domain inews.co.uk
- **Reply route:** The body's email is redacted by Sourcee; the body also says 'message me here' (a platform reply). The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Off-beat on both items. NOT DRAFTED.

### [low] AI / Podcast Guest Call
- **URL:** https://www.sourcee.app/journo-request/software-engineers-and-leaders-one-practical-engineering-question
- **Posted:** 7d old (page datePublished (page probed 2026-11-19)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-19 (7x)
- **Publication:** John Crickett, named in the page's author field; no publication stated (Coding Chats podcast).
- **Reply route:** The page publishes no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Startup Sourcing
- **URL:** https://www.sourcee.app/journo-request/women-founders-deeptech-startups-biotech-space-ai-robotics
- **Posted:** 8d old (page datePublished (page probed 2026-11-19)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-19 (9x)
- **Publication:** YourStory (yourstory.com) - Rekha Balakrishnan, named in the page's author field. · domain yourstory.com
- **Reply route:** The request body's address is redacted by Sourcee. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Consumer
- **URL:** https://www.sourcee.app/journo-request/facebook-marketplace-users-ai-impact-on-buying-and-selling
- **Posted:** 8d old (page datePublished (page probed 2026-11-19)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-19 (9x)
- **Publication:** Rainesford Stauffer, freelance journalist, named in the page's author field; no publication stated.
- **Reply route:** The page publishes no address and no link; the body opens with a Bluesky handle (@obicynkenobi.bsky.social), which is a source she was already writing to, not a reply route for us. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Telecom Policy
- **URL:** https://www.sourcee.app/journo-request/telecom-policy-experts-international-telecom-sovereignty-research
- **Posted:** 8d old (page datePublished (page probed 2026-11-19)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-19 (9x)
- **Publication:** Dean Bubley, telecom analyst (Disruptive Analysis), named in the page's author field; published as a guest blog for techUK's Cloud and Infrastructure Week. · domain techuk.org
- **Reply route:** One link published on the page: https://lnkd.in/egE8qFYa, a LinkedIn short link to his own article. The page publishes no address. Links published on the page: https://lnkd.in/egE8qFYa.  ·  _no — published booking link https://lnkd.in/egE8qFYa (George)_
- **Links published on the page:** https://lnkd.in/egE8qFYa
- **Angle:** None. No route to the author and no standing on telecom sovereignty. NOT DRAFTED.

### [low] AI / Higher Education
- **URL:** https://www.sourcee.app/journo-request/business-schools-ai-applications-in-teaching-and-operations-jan-2027
- **Posted:** 8d old (page datePublished (page probed 2026-11-19)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-19 (8x)
- **Publication:** Kevin Anselmo, writing for the American Association of Colleges and Universities (aacu.org) report 'A Framework for Artificial Intelligence in Business Education', led by Tawnya Means. · domain aacu.org
- **Reply route:** Two lnkd.in links on the page: the submission route (lnkd.in/eb-r8aBc) and the current report (lnkd.in/eDD2p8ek). No email address. Links published on the page: https://lnkd.in/eDD2p8ek, https://lnkd.in/eb-r8aBc.  ·  _no — published booking link https://lnkd.in/eDD2p8ek (George)_
- **Links published on the page:** https://lnkd.in/eDD2p8ek, https://lnkd.in/eb-r8aBc
- **Angle:** None. Institutional call, not our standing. NOT DRAFTED.

### [low] AI / Hiring Testimony
- **URL:** https://www.sourcee.app/journo-request/job-candidates-interviewed-by-ai-interview-experience
- **Posted:** 8d old (page datePublished (page probed 2026-11-19)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-19 (8x)
- **Publication:** Not named on the page - the author field is a single display name, no publication stated.
- **Reply route:** No address, handle or link published on the request page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Documentary Sourcing
- **URL:** https://www.sourcee.app/journo-request/nova-scotia-residents-near-ai-data-centre-community-impact
- **Posted:** 8d old (page datePublished (page probed 2026-11-19)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-19 (8x)
- **Publication:** Joshua Saunders and Justin White, A Venturesome Production - a documentary team, byline on the page; no publication.
- **Reply route:** The request body's address is redacted by Sourcee ('Please reach out directly or email: [email redacted]'). The page publishes four lnkd.in links, all to the film's own trailer and social accounts - promotion, not a reply route. The request body's address is redacted by Sourcee. Links published on the page: https://lnkd.in/gAMUxgqr, https://lnkd.in/gX86GKjH, https://lnkd.in/ggn7PVx3.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Links published on the page:** https://lnkd.in/gAMUxgqr, https://lnkd.in/gX86GKjH, https://lnkd.in/ggn7PVx3, https://lnkd.in/gnPyZVSB, https://lnkd.in/guChj6UZ
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Enterprise Policy
- **URL:** https://www.sourcee.app/journo-request/indian-cios-founders-investors-and-policymakers-sovereign-ai-challenges
- **Posted:** 8d old (page datePublished (page probed 2026-11-19)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-19 (8x)
- **Publication:** Ankit Anand, Express Computer (expresscomputer.in) - domain on the page; the body also signs Srikanth RP, Nivedan Prakash and Sayantan Mondal. · domain expresscomputer.in
- **Reply route:** The body says 'reach out via LinkedIn DM or at [email redacted]'; the address is platform-redacted and no handle of his own is published on the page. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Infrastructure Sourcing
- **URL:** https://www.sourcee.app/journo-request/uk-ai-founders-compute-datacentre-and-grid-constraints
- **Posted:** 9d old (page datePublished (page probed 2026-11-19)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-19 (9x)
- **Publication:** Alison Coleman, Forbes senior contributor (entrepreneurs and startups) - named in the page's author field. The page names no publication; the attribution comes from her Forbes byline, which is the same reporter behind the two carried Forbes rows.
- **Reply route:** The request body's address is redacted by Sourcee. Her address is already resolved off her own site for the two carried Forbes calls - alison@alisoncoleman.co.uk, published on alisoncoleman.co.uk/contact-me/ (route-checks-2026-11-19.json: HTTP 200, 21,366 bytes  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: alison@alisoncoleman.co.uk (George sends)_
- **Angle:** None. Deliberately not drafted: no data, no standing, and one pitch per reporter. The two Forbes rows it sits beside are drafted at pitch-drafts-2026-11-11.md section 2.

### [low] AI / Podcast Sourcing
- **URL:** https://www.sourcee.app/journo-request/ai-griefbot-creators-mimicking-deceased-loved-ones-doubletake
- **Posted:** 9d old (page datePublished (page probed 2026-11-19)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-19 (9x)
- **Publication:** WORLD (world.wng.org) - 'Doubletake' podcast, host Les Sillars, named in the body.
- **Reply route:** The request body's address is redacted by Sourcee. The page publishes no link. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / PR Request
- **URL:** https://www.sourcee.app/journo-request/uk-recruitment-expert-advice-on-losing-jobs-to-ai
- **Posted:** 9d old (page datePublished (page probed 2026-11-19)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-19 (9x)
- **Publication:** Pitch & Shout, a PR request account; no publication named on the page.
- **Reply route:** One link published on the page: https://t.co/U6uparVncd, which the body describes as the pitch route ('Pitch here'). Links published on the page: https://t.co/U6uparVncd.  ·  _unknown — verify the route before sending_
- **Links published on the page:** https://t.co/U6uparVncd
- **Angle:** None. No standing. NOT DRAFTED.

### [low] AI / Consumer
- **URL:** https://www.sourcee.app/journo-request/facebook-marketplace-users-ai-agents-impact-on-feed-spam-and-privacy
- **Posted:** 9d old (page datePublished (page probed 2026-11-19)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-19 (9x)
- **Publication:** Rainesford Stauffer, freelance journalist, named in the page's author field; no publication stated.
- **Reply route:** The page publishes no address and no link; 'DMs open' with no handle given. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Labour
- **URL:** https://www.sourcee.app/journo-request/jobseekers-in-ireland-resenting-ai-in-hiring-on-principle
- **Posted:** 9d old (page datePublished (page probed 2026-11-19)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-19 (9x)
- **Publication:** Alex Meehan, named in the page's author field; no publication stated.
- **Reply route:** The page publishes no address and no link; 'drop me a message' with no handle given. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Sales Tools
- **URL:** https://www.sourcee.app/journo-request/sales-leaders-and-ai-sales-tool-builders-ai-during-sales-calls
- **Posted:** 9d old (page datePublished (page probed 2026-11-19)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-19 (9x)
- **Publication:** Peter O., writing for The Growth Signal, named in the body.
- **Reply route:** The page publishes no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Transformation
- **URL:** https://www.sourcee.app/journo-request/designled-ai-practitioners-where-ai-transformations-stall
- **Posted:** 9d old (page datePublished (page probed 2026-11-19)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-19 (9x)
- **Publication:** Sebastian Nause-Blüml, writing a public fieldnotes guide; named in the post.
- **Reply route:** The page publishes no address and no link; asks people to tag or message him. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Security Governance
- **URL:** https://www.sourcee.app/journo-request/cybersecurity-founder-and-ciso-ai-infra-ceo-scandal-risk-and-governance
- **Posted:** 9d old (page datePublished (page probed 2026-11-19)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-19 (9x)
- **Publication:** Times Internet (timesinternet.in) - Vaishnavi D., named in the page's author field. · domain timesinternet.in
- **Reply route:** The request body's address is redacted by Sourcee; the page publishes no link. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

## Cold — only if you have a reason

Older than the 10-day line and never pitched. Not provably abandoned — no renewal signal exists on this source — but every one of these has already passed an ideal send window.

- [high] 70d old — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [high] 73d old — https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
- [high] 75d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-ai-governance-and-agent-sprawl
- [high] 76d old — https://www.sourcee.app/journo-request/scientists-phd-students-and-postdocs-paying-for-ai-subscriptions
- [high] 121d old — https://www.sourcee.app/journo-request/business-and-technology-leaders-tech-budget-priorities-amid-volatility
- [high] 201d old — https://www.sourcee.app/journo-request/anthropic-api-users-costs-and-token-burn-increase-since-january
- [medium-high] 69d old — https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
- [medium-high] 70d old — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium-high] 73d old — https://www.sourcee.app/journo-request/uk-managers-cracked-down-on-gen-z-ai-overuse
- [medium] 22d old — https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
- [medium] 23d old — https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
- [medium] 23d old — https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact
- [medium] 45d old — https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
- [medium] 69d old — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [medium] 73d old — https://www.sourcee.app/journo-request/ai-agents-making-money-2026-sales-and-leadgen-workflow-ops
- [medium] 73d old — https://www.sourcee.app/journo-request/ai-startups-workplace-fraud-detection-expenses-time-theft
- [medium] 73d old — https://www.sourcee.app/journo-request/marketing-and-content-leaders-aiassisted-work-review-process
- [medium] 77d old — https://www.sourcee.app/journo-request/ceos-ai-impact-on-ops-culture-and-commercial-strategy
- [medium] 87d old — https://www.sourcee.app/journo-request/uk-finance-risk-and-regulatory-leaders-ai-explainability-risks
- [medium] 254d old — https://www.sourcee.app/journo-request/sme-owners-operational-challenges-for-ai-solutions-case-study
- [low-medium] 12d old — https://www.sourcee.app/journo-request/business-owners-and-leaders-team-resistance-to-ai-adoption
- [low-medium] 27d old — https://www.sourcee.app/journo-request/claude-users-anthropic-public-benefit-fund-trust-and-job-impact
- [low-medium] 37d old — https://www.sourcee.app/journo-request/b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research
- [low-medium] 40d old — https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
- [low-medium] 44d old — https://www.sourcee.app/journo-request/uk-companies-implementing-ai-how-automation-transforms-workdays
- [low-medium] 48d old — https://www.sourcee.app/journo-request/law-firm-lawyers-concrete-ai-implementations-and-billing-impact
- [low-medium] 49d old — https://www.sourcee.app/journo-request/employees-conflicted-about-ai-use-generative-ai-workplace-impact
- [low-medium] 51d old — https://www.sourcee.app/journo-request/insurance-agents-ai-use-in-personal-lines
- [medium-low] 61d old — https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business
- [low-medium] 64d old — https://www.sourcee.app/journo-request/us-founders-calls-to-slow-ai-development-impact-on-companies
- [medium-low] 70d old — https://www.sourcee.app/journo-request/tech-policy-experts-california-ai-audit-bills-impact-cios
- [low-medium] 89d old — https://www.sourcee.app/journo-request/ai-project-builders-youtube-finance-and-lifestyle-channel-feature
- [low-medium] 134d old — https://www.sourcee.app/journo-request/prompt-engineers-tokenmaxxing-anecdotes
- [low] 11d old — https://www.sourcee.app/journo-request/podcasters-and-linkedin-live-creators-tech-and-ai-and-career-topics
- [low] 12d old — https://www.sourcee.app/journo-request/human-behind-ai-crypto-agent-agentwritten-crypto-blogs
- [low] 13d old — https://www.sourcee.app/journo-request/people-with-friends-and-coworkers-who-disagree-on-ai-managing-tension
- [low] 13d old — https://www.sourcee.app/journo-request/woman-replaced-by-ai-and-recruitment-expert-ai-job-loss-case-study
- [low] 13d old — https://www.sourcee.app/journo-request/ai-founders-and-investors-in-barcelona-podcast-and-company-visit-guests
- [low] 13d old — https://www.sourcee.app/journo-request/prs-and-agents-celebrities-national-titles-interview-slots
- [low] 13d old — https://www.sourcee.app/journo-request/ai-users-and-relationship-therapists-dating-conflicts-breakups
- [low] 13d old — https://www.sourcee.app/journo-request/b2b-tech-and-software-sales-reps-and-leaders-real-customer-deal-lessons
- [low] 14d old — https://www.sourcee.app/journo-request/uk-job-hunters-12-months-job-market-climate-and-ai
- [low] 14d old — https://www.sourcee.app/journo-request/designers-and-creators-balancing-bills-family-and-meaningful-work
- [low] 14d old — https://www.sourcee.app/journo-request/early-career-workers-future-of-work-and-ai
- [low] 14d old — https://www.sourcee.app/journo-request/ai-and-virtual-influencer-creators-index-submission
- [low] 14d old — https://www.sourcee.app/journo-request/nar-nxt-safety-and-cybersecurity-experts-gen-ai-cybersecurity
- [low] 14d old — https://www.sourcee.app/journo-request/ai-policy-expert-possible-pause-on-ai-in-us
- [low] 14d old — https://www.sourcee.app/journo-request/data-center-workers-and-ai-execs-ban-ai-expansion-until-safety-rules
- [low] 14d old — https://www.sourcee.app/journo-request/doctoral-candidates-and-phd-holders-dissertation-writing-strategies
- [low] 14d old — https://www.sourcee.app/journo-request/postcolonial-scholars-and-former-coloniser-officials-citizenship-debate
- [low] 14d old — https://www.sourcee.app/journo-request/business-leaders-and-educators-headtohead-handwriting-in-business
- [low] 14d old — https://www.sourcee.app/journo-request/cisos-and-senior-cybersecurity-leaders-protecting-developers
- [low] 15d old — https://www.sourcee.app/journo-request/ai-data-center-operators-midterm-vote-backlash-impact
- [low] 15d old — https://www.sourcee.app/journo-request/canadian-real-estate-agents-foreign-buyer-ban-ending-jan-1-2027
- [low] 15d old — https://www.sourcee.app/journo-request/freelancers-small-businesses-and-employees-falsely-accused-of-ai-use
- [low] 15d old — https://www.sourcee.app/journo-request/anthropic-employees-company-decisionmaking-and-workplace-impact
- [low] 15d old — https://www.sourcee.app/journo-request/ai-policy-experts-tech-influence-on-midterms-tonight
- [low] 15d old — https://www.sourcee.app/journo-request/retail-workers-and-managers-instore-ai-impact-holiday-season
- [low] 15d old — https://www.sourcee.app/journo-request/generative-ai-documentation-experts-business-document-fraud-risk
- [low] 16d old — https://www.sourcee.app/journo-request/freelance-journalists-automation-feature-pitches
- [low] 16d old — https://www.sourcee.app/journo-request/former-muse-users-gave-up-on-ai-agents
- [low] 16d old — https://www.sourcee.app/journo-request/designers-on-large-teams-evolving-design-systems-dive-radio
- [low] 16d old — https://www.sourcee.app/journo-request/world-model-researchers-applications-in-robotics
- [low] 16d old — https://www.sourcee.app/journo-request/founders-selling-to-nurses-nurse-adoption-and-clinical-ai
- [low] 16d old — https://www.sourcee.app/journo-request/dallas-insurance-executives-private-capital-ai-rbc-reforms
- [low] 16d old — https://www.sourcee.app/journo-request/retail-executives-nrf-nyc-retail-media-supply-chain-and-ai
- [low] 16d old — https://www.sourcee.app/journo-request/regulators-and-compliance-experts-consumer-ai-mental-wellbeing
- [low] 16d old — https://www.sourcee.app/journo-request/newsletter-publishers-and-creators-state-of-newsletters-report-2027
- [low] 16d old — https://www.sourcee.app/journo-request/job-seekers-in-ireland-aiautomated-job-applications-experience
- [low] 16d old — https://www.sourcee.app/journo-request/biometrics-and-computer-vision-experts-proving-humanity-in-digital-age
- [low] 16d old — https://www.sourcee.app/journo-request/carleton-students-ai-use-in-dating-advice
- [low] 16d old — https://www.sourcee.app/journo-request/aussie-travellers-1861-hotel-tech-abandoned-bookings-and-ai-concerns
- [low] 16d old — https://www.sourcee.app/journo-request/young-adults-1835-ai-impact-on-comingofage
- [low] 16d old — https://www.sourcee.app/journo-request/people-with-ai-psychosis-firsthand-accounts
- [low] 16d old — https://www.sourcee.app/journo-request/new-authors-ai-market-dilution-and-fair-use-impact-on-writing
- [low] 16d old — https://www.sourcee.app/journo-request/marketers-and-creators-using-ai-agents-timesaving-wins
- [low] 16d old — https://www.sourcee.app/journo-request/ut-austin-students-ai-trump-crypto-ads-on-game-livestreams
- [low] 17d old — https://www.sourcee.app/journo-request/uk-recruiters-ai-impact-on-billing-and-candidate-matching
- [low] 17d old — https://www.sourcee.app/journo-request/global-and-european-marketing-leaders-investment-and-ops-challenges
- [low] 20d old — https://www.sourcee.app/journo-request/startup-founders-deciding-first-marketing-tests-on-tight-runway
- [low] 20d old — https://www.sourcee.app/journo-request/multifamily-professionals-ai-adoption-and-employee-chatbot-use
- [low] 20d old — https://www.sourcee.app/journo-request/canadian-ai-and-tech-companies-government-picking-winners-and-losers
- [low] 20d old — https://www.sourcee.app/journo-request/bank-and-brokerage-users-ai-tools-managing-personal-finances
- [low] 20d old — https://www.sourcee.app/journo-request/midlife-professionals-career-regret
- [low] 21d old — https://www.sourcee.app/journo-request/rig-hse-staff-aienabled-cameras-trial-outcomes
- [low] 21d old — https://www.sourcee.app/journo-request/current-ucla-students-and-faculty-ai-impact-on-majors
- [low] 21d old — https://www.sourcee.app/journo-request/founders-and-inclusion-leads-future-of-work-and-ai-impact
- [low] 21d old — https://www.sourcee.app/journo-request/uk-law-experts-and-ai-safety-researchers-chatbotaided-crime
- [low] 21d old — https://www.sourcee.app/journo-request/buyers-and-sellers-without-agents-diy-property-sale-experience
- [low] 21d old — https://www.sourcee.app/journo-request/editors-creatives-and-graphic-designers-ai-impact-documentary
- [low] 21d old — https://www.sourcee.app/journo-request/character-ai-users-emotional-attachment-and-loneliness
- [low] 22d old — https://www.sourcee.app/journo-request/users-who-linked-bank-and-brokerage-accounts-to-llms-ai-finance
- [low] 22d old — https://www.sourcee.app/journo-request/musicians-artists-writers-and-creators-ai-impact-on-creativity
- [low] 22d old — https://www.sourcee.app/journo-request/literary-writers-thoughts-on-lit-mags-funny-deep-frustrated
- [low] 22d old — https://www.sourcee.app/journo-request/ai-researchers-founders-and-tech-ceos-retirement-plans-amid-ai-risk
- [low] 22d old — https://www.sourcee.app/journo-request/canadian-skilled-trades-workers-ai-impact-on-manufacturing
- [low] 22d old — https://www.sourcee.app/journo-request/gcc-founders-and-entrepreneurs-ai-collaboration-and-data-sovereignty
- [low] 22d old — https://www.sourcee.app/journo-request/dairy-companies-and-startups-aipowered-livestock-health-and-nutrition
- [low] 23d old — https://www.sourcee.app/journo-request/excorporate-privacy-lead-built-privacy-and-ai-consultancy
- [low] 23d old — https://www.sourcee.app/journo-request/canadian-health-innovators-voices-of-innovation-canada-nov-16
- [low] 23d old — https://www.sourcee.app/journo-request/ai-startup-founders-and-marketers-b2b-marketing-as-show-business
- [low] 23d old — https://www.sourcee.app/journo-request/students-whose-professors-allow-ai-ai-use-in-coursework
- [low] 23d old — https://www.sourcee.app/journo-request/carleton-students-ai-dating-advice-impact-on-dating-experience
- [low] 23d old — https://www.sourcee.app/journo-request/former-software-engineers-turned-traders-pivot-after-layoff-or-ai
- [low] 23d old — https://www.sourcee.app/journo-request/members-club-and-hospitality-pros-in-hong-kong-postcovid-trends
- [low] 24d old — https://www.sourcee.app/journo-request/people-using-llms-as-companions-emotional-support-stories
- [low] 24d old — https://www.sourcee.app/journo-request/admissions-leaders-and-researchers-measuring-judgment-amid-ai
- [low] 24d old — https://www.sourcee.app/journo-request/celebrity-agents-how-i-manage-my-money-series
- [low] 24d old — https://www.sourcee.app/journo-request/ai-companies-in-utilities-and-construction-frontline-safety-and-workload
- [low] 24d old — https://www.sourcee.app/journo-request/sound-artists-and-field-recordists-run-radio-aarhus-open-call
- [low] 26d old — https://www.sourcee.app/journo-request/people-using-ai-for-social-advice-communication-and-connection-impact
- [low] 26d old — https://www.sourcee.app/journo-request/video-teams-using-claude-and-remotion-agentic-video-editing
- [low] 27d old — https://www.sourcee.app/journo-request/couples-letting-ai-dictate-relationship-emotions-and-intimacy
- [low] 27d old — https://www.sourcee.app/journo-request/people-recreating-iconic-runway-looks-halloween-costume-story
- [low] 27d old — https://www.sourcee.app/journo-request/parish-event-organizers-aigenerated-flyers-scourge-or-timesaver
- [low] 27d old — https://www.sourcee.app/journo-request/uk-and-eu-sports-retail-supply-chain-leaders-retail-ai-at-scale
- [low] 27d old — https://www.sourcee.app/journo-request/founders-and-cofounders-fortnightly-founder-qanda
- [low] 27d old — https://www.sourcee.app/journo-request/fanvue-chatters-nsfw-ai-model-experiences
- [low] 28d old — https://www.sourcee.app/journo-request/nontech-inhouse-corporate-comms-lead-ai-search-and-discovery-strategy
- [low] 28d old — https://www.sourcee.app/journo-request/geopolitical-analysts-and-ai-security-experts-global-hotspots
- [low] 28d old — https://www.sourcee.app/journo-request/digital-artists-aigenerated-posters-flooding-social-feeds
- [low] 28d old — https://www.sourcee.app/journo-request/founders-and-ctos-production-ai-tradeoffs-in-healthcare-and-fintech
- [low] 28d old — https://www.sourcee.app/journo-request/students-and-professionals-balancing-ai-use-and-human-focus
- [low] 28d old — https://www.sourcee.app/journo-request/rig-hse-officers-aienabled-camera-trial-outcomes
- [low] 28d old — https://www.sourcee.app/journo-request/anthropic-project-panama-employees-book-digitization-and-ai-training
- [low] 28d old — https://www.sourcee.app/journo-request/nj-parents-and-teachers-ai-school-surveillance-and-data-practices
- [low] 29d old — https://www.sourcee.app/journo-request/brand-managers-ai-to-deepen-customer-insight-and-preserve-humanity
- [low] 29d old — https://www.sourcee.app/journo-request/omaha-hr-representatives-offices-with-written-ai-policies
- [low] 29d old — https://www.sourcee.app/journo-request/bengaluru-founders-deep-tech-healthcare-biology-housing-and-ai
- [low] 29d old — https://www.sourcee.app/journo-request/fintech-product-managers-nextgen-aipowered-personal-finance-apps
- [low] 30d old — https://www.sourcee.app/journo-request/hr-leaders-and-organizational-design-practitioners-decision-fatigue
- [low] 30d old — https://www.sourcee.app/journo-request/cios-at-gartner-it-symposium-orlando-balancing-ai-risk-and-value
- [low] 30d old — https://www.sourcee.app/journo-request/estate-agents-and-property-lawyers-disclosure-rules-haunted-homes
- [low] 30d old — https://www.sourcee.app/journo-request/product-managers-on-512-engineer-teams-engineers-using-ai
- [low] 30d old — https://www.sourcee.app/journo-request/bay-area-agentic-ai-builders-agntcon-and-mcpcon-stories
- [low] 30d old — https://www.sourcee.app/journo-request/carleton-students-ai-impact-on-dating-experiences
- [low] 30d old — https://www.sourcee.app/journo-request/new-yorkers-ai-music-playing-in-cabs-and-local-businesses
- [low] 30d old — https://www.sourcee.app/journo-request/western-students-using-ai-companions-psychological-effects
- [low] 31d old — https://www.sourcee.app/journo-request/fb-marketplace-sellers-and-buyers-ai-impact-on-pricing-and-listings
- [low] 31d old — https://www.sourcee.app/journo-request/consumers-using-ai-for-financial-advice-experience-and-factchecking
- [low] 31d old — https://www.sourcee.app/journo-request/ai-energy-and-tax-experts-project-jupiter-documentary-new-mexico
- [low] 32d old — https://www.sourcee.app/journo-request/uk-customer-service-workers-daytoday-now-ai-automation-vs-human
- [low] 33d old — https://www.sourcee.app/journo-request/ai-saas-vendors-targeting-journalists-prs-and-marketers-case-studies
- [low] 33d old — https://www.sourcee.app/journo-request/real-estate-operators-ai-adoption-and-org-restructuring
- [low] 33d old — https://www.sourcee.app/journo-request/memphis-and-southaven-residents-and-env-advocates-xai-colossus-impact
- [low] 33d old — https://www.sourcee.app/journo-request/black-women-in-canada-ai-chatbots-and-healthcare-experiences
- [low] 33d old — https://www.sourcee.app/journo-request/engineering-leaders-leading-people-through-ai-changes
- [low] 33d old — https://www.sourcee.app/journo-request/ai-app-and-saas-founders-1k-mrr-youtube-feature-growth-tactics
- [low] 34d old — https://www.sourcee.app/journo-request/chemistry-undergrads-and-phd-students-ai-use-in-coursework-and-research
- [low] 34d old — https://www.sourcee.app/journo-request/ai-infrastructure-engineers-in-berlin-data-centers-and-bottlenecks
- [low] 34d old — https://www.sourcee.app/journo-request/residents-near-mumbai-ai-data-centres-power-and-water-strain
- [low] 34d old — https://www.sourcee.app/journo-request/single-family-office-cybersecurity-experts-ai-risks-and-opportunities
- [low] 35d old — https://www.sourcee.app/journo-request/cios-and-ai-leaders-ai-infrastructure-day2-ops-and-costs
- [low] 35d old — https://www.sourcee.app/journo-request/companies-and-data-buyers-selling-corporate-data-to-train-ai
- [low] 35d old — https://www.sourcee.app/journo-request/uk-political-analysts-disinformation-and-ai-manipulation-in-politics
- [low] 35d old — https://www.sourcee.app/journo-request/content-creators-using-ai-job-losses-and-ethics
- [low] 35d old — https://www.sourcee.app/journo-request/painters-and-photographers-ai-impact-on-art
- [low] 35d old — https://www.sourcee.app/journo-request/legal-assistants-paralegals-and-lawfirm-staff-jobs-eliminated-by-ai
- [low] 35d old — https://www.sourcee.app/journo-request/ai-companion-users-in-africa-friendship-and-emotional-impact
- [low] 35d old — https://www.sourcee.app/journo-request/pro-se-litigants-using-generative-ai-access-to-justice-impact
- [low] 36d old — https://www.sourcee.app/journo-request/school-leaders-and-ngo-staff-ai-adoption-challenges-across-sectors
- [low] 36d old — https://www.sourcee.app/journo-request/ai-policy-advisor-newsom-administration-ai-regulation
- [low] 36d old — https://www.sourcee.app/journo-request/uk-and-us-heads-of-data-and-ai-from-idea-to-production
- [low] 36d old — https://www.sourcee.app/journo-request/minnesotans-using-chatgpt-and-ai-tools-experiences-with-election-info
- [low] 37d old — https://www.sourcee.app/journo-request/global-development-professionals-using-ai-across-programs-and-policy
- [low] 37d old — https://www.sourcee.app/journo-request/african-founders-building-ai-companies-pitch-deck-realities
- [low] 37d old — https://www.sourcee.app/journo-request/higher-ed-nonfaculty-staff-ai-use-at-work
- [low] 37d old — https://www.sourcee.app/journo-request/podcast-guests-ai-channel-and-partner-ecosystem
- [low] 37d old — https://www.sourcee.app/journo-request/ai-infrastructure-professionals-in-london-capacity-europe-attendees
- [low] 37d old — https://www.sourcee.app/journo-request/b2b-vendors-buyers-pasting-proposals-into-ai-tools
- [low] 38d old — https://www.sourcee.app/journo-request/caine-prize-winners-gen-ai-accusations-targeting-black-writers
- [low] 38d old — https://www.sourcee.app/journo-request/software-engineers-who-left-tech-jobs-lost-to-ai-coding-tools
- [low] 38d old — https://www.sourcee.app/journo-request/manufacturers-and-ai-safety-experts-ai-risks-in-chemical-food-defense
- [low] 38d old — https://www.sourcee.app/journo-request/uk-baby-boomers-misinformation-sharing-and-ai-influence-online
- [low] 39d old — https://www.sourcee.app/journo-request/hedera-builders-shipping-defi-nfts-rwas-ai-games-and-memes
- [low] 39d old — https://www.sourcee.app/journo-request/production-designers-ai-impact-on-future-of-filmmaking
- [low] 39d old — https://www.sourcee.app/journo-request/ai-researchers-and-policy-experts-5-years-us-race-to-superintelligence
- [low] 40d old — https://www.sourcee.app/journo-request/ai-cybersecurity-iot-and-web3-founders-and-operators-news-submissions
- [low] 40d old — https://www.sourcee.app/journo-request/employees-pay-transparency-good-or-bad
- [low] 41d old — https://www.sourcee.app/journo-request/sales-reps-who-cold-call-and-email-how-ai-changed-outreach
- [low] 41d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-and-builders-realworld-deployment-and-strategy
- [low] 41d old — https://www.sourcee.app/journo-request/anthropic-gtm-leaders-scaling-300k-b2b-clients
- [low] 42d old — https://www.sourcee.app/journo-request/voters-who-used-ai-to-navigate-ballot-voting-experience
- [low] 42d old — https://www.sourcee.app/journo-request/hotel-and-fandb-supervisors-and-managers-customer-expectations-vs-ai
- [low] 42d old — https://www.sourcee.app/journo-request/researchers-founders-and-funders-ai-transforming-scientific-research
- [low] 42d old — https://www.sourcee.app/journo-request/facebook-marketplace-sellers-ai-listing-photos-and-selling-experience
- [low] 42d old — https://www.sourcee.app/journo-request/uk-ai-data-trainers-daytoday-work
- [low] 42d old — https://www.sourcee.app/journo-request/patent-attorneys-and-agents-startup-ip-starter-pack
- [low] 43d old — https://www.sourcee.app/journo-request/aps-hr-leaders-ai-skills-training-and-workforce-planning
- [low] 43d old — https://www.sourcee.app/journo-request/scrum-masters-daytoday-and-career-pivots-and-ai-impact
- [low] 43d old — https://www.sourcee.app/journo-request/real-estate-agents-replacing-pdf-property-brochure
- [low] 43d old — https://www.sourcee.app/journo-request/anz-marketers-ai-and-martech-innovation-spotlight
- [low] 43d old — https://www.sourcee.app/journo-request/solicitors-and-barristers-ai-to-expand-pro-bono-capacity
- [low] 43d old — https://www.sourcee.app/journo-request/apac-reporters-and-editors-ai-accountability-coverage
- [low] 43d old — https://www.sourcee.app/journo-request/early-to-midcareer-information-architects-products-featuring-ai
- [low] 43d old — https://www.sourcee.app/journo-request/martech-buyers-ai-impact-on-build-vs-buy-decisions
- [low] 43d old — https://www.sourcee.app/journo-request/swiss-ai-companion-users-emotional-bonds-and-daily-life
- [low] 43d old — https://www.sourcee.app/journo-request/ai-data-labelers-in-germany-positive-and-negative-experiences
- [low] 43d old — https://www.sourcee.app/journo-request/ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories
- [low] 44d old — https://www.sourcee.app/journo-request/ai-infrastructure-experts-china-vs-us-datacenter-capacity
- [low] 44d old — https://www.sourcee.app/journo-request/plaintiffs-attorneys-and-legal-scholars-ai-deepfake-liability
- [low] 44d old — https://www.sourcee.app/journo-request/coweta-county-artists-and-creatives-data-centers-and-ai-infrastructure
- [low] 44d old — https://www.sourcee.app/journo-request/ai-data-annotators-and-labellers-experience-with-ai-training-data
- [low] 44d old — https://www.sourcee.app/journo-request/academics-social-media-and-ai-impact-on-womens-identity-and-selfesteem
- [low] 44d old — https://www.sourcee.app/journo-request/emergency-managers-ai-tools-for-funding-and-staffing-shortfalls
- [low] 45d old — https://www.sourcee.app/journo-request/ai-liability-insurers-and-legal-experts-procurement-and-implementation
- [low] 45d old — https://www.sourcee.app/journo-request/uk-cybersecurity-hiring-managers-state-of-hiring-2026-and-ai-impact
- [low] 45d old — https://www.sourcee.app/journo-request/ai-emotional-support-users-chatbot-therapy-and-journaling
- [low] 45d old — https://www.sourcee.app/journo-request/mortgage-adviser-using-ai-efficiency-and-client-outcomes-video-series
- [low] 45d old — https://www.sourcee.app/journo-request/founders-and-cxos-in-automotive-ai-evs-autonomy-thought-leadership
- [low] 46d old — https://www.sourcee.app/journo-request/video-game-developer-falsely-accused-of-using-generative-ai
- [low] 47d old — https://www.sourcee.app/journo-request/lawyers-and-tech-ethics-experts-ai-wearables-and-legal-journeys
- [low] 48d old — https://www.sourcee.app/journo-request/storytellers-and-brand-founders-marys-big-30-ai-story-project
- [low] 48d old — https://www.sourcee.app/journo-request/newsletter-editors-using-ai-agents-news-aggregation-practices
- [low] 48d old — https://www.sourcee.app/journo-request/scottish-teachers-ai-tools-implementation-in-education
- [low] 48d old — https://www.sourcee.app/journo-request/mls-executives-risks-when-agents-grant-mls-access-to-llms
- [low] 48d old — https://www.sourcee.app/journo-request/real-estate-agents-and-brokers-switched-from-pdf-brochures
- [low] 48d old — https://www.sourcee.app/journo-request/advertising-tech-and-media-pros-in-miami-ai-audience-discovery
- [low] 48d old — https://www.sourcee.app/journo-request/hr-leaders-company-ai-strategies-and-cognitive-offloading-risk
- [low] 48d old — https://www.sourcee.app/journo-request/k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact
- [low] 49d old — https://www.sourcee.app/journo-request/fea-engineers-using-agentic-ai-practitioner-case-study
- [low] 49d old — https://www.sourcee.app/journo-request/fb-marketplace-sellers-ai-photos-and-description-prompts
- [low] 49d old — https://www.sourcee.app/journo-request/ai-summit-barcelona-attendees-controversy-and-experiences
- [low] 49d old — https://www.sourcee.app/journo-request/ai-glasses-owners-users-and-developers-in-india-product-experience
- [low] 49d old — https://www.sourcee.app/journo-request/parents-ai-acting-as-pseudoparent-in-kid-questions
- [low] 50d old — https://www.sourcee.app/journo-request/chatbot-users-experiences-talking-to-ai
- [low] 50d old — https://www.sourcee.app/journo-request/us-ai-security-experts-rogue-ai-agents-hitting-government-sites
- [low] 50d old — https://www.sourcee.app/journo-request/real-estate-agents-pdf-brochures-vs-alternatives-agent-workflow
- [low] 51d old — https://www.sourcee.app/journo-request/cybersecurity-expert-ai-nexus-and-security-risks
- [low] 51d old — https://www.sourcee.app/journo-request/us-emergency-physicians-and-paramedics-impact-of-ai-answering-911-calls
- [low] 51d old — https://www.sourcee.app/journo-request/job-seekers-and-recruiters-ai-recruitment-experiences
- [low] 52d old — https://www.sourcee.app/journo-request/data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity
- [low] 52d old — https://www.sourcee.app/journo-request/b2b-marketing-leaders-hyperspecialization-to-outcompete-ai
- [low] 52d old — https://www.sourcee.app/journo-request/ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes
- [low] 58d old — https://www.sourcee.app/journo-request/saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup
- [low] 58d old — https://www.sourcee.app/journo-request/ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai
- [low] 59d old — https://www.sourcee.app/journo-request/sales-enablement-saas-tools-proposal-and-deck-engagement-tracking
- [low] 59d old — https://www.sourcee.app/journo-request/london-businesses-stopped-using-ai-hiring-tools
- [low] 59d old — https://www.sourcee.app/journo-request/engineering-managers-measuring-engineers-when-using-ai
- [low] 59d old — https://www.sourcee.app/journo-request/creative-industry-professionals-podcast-on-ai-impact
- [low] 59d old — https://www.sourcee.app/journo-request/former-ai-skeptics-changed-views-on-ai-impact
- [low] 60d old — https://www.sourcee.app/journo-request/employers-and-recruiters-over-50s-adapting-to-ai
- [low] 60d old — https://www.sourcee.app/journo-request/data-center-professionals-podcast-guest-ai-and-hyperscale-trends
- [low] 60d old — https://www.sourcee.app/journo-request/patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges
- [low] 60d old — https://www.sourcee.app/journo-request/founders-and-leaders-mindsets-and-milestones
- [low] 60d old — https://www.sourcee.app/journo-request/ml-researchers-continuous-learning-fast-weights-and-adapters
- [low] 60d old — https://www.sourcee.app/journo-request/founders-55-latelife-entrepreneurship-series-1
- [low] 60d old — https://www.sourcee.app/journo-request/founders-and-entrepreneurs-and-musicians-podcast-guests
- [low] 60d old — https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- [low] 61d old — https://www.sourcee.app/journo-request/ai-alignment-researchers-humanai-mutual-understanding
- [low] 62d old — https://www.sourcee.app/journo-request/companies-that-stopped-emailing-pdfs-new-tools-and-transition
- [low] 63d old — https://www.sourcee.app/journo-request/gen-z-ai-data-annotators-work-experience-and-income-impact
- [low] 63d old — https://www.sourcee.app/journo-request/ecommerce-marketers-transparency-in-ai-recommendations-and-conversion
- [low] 63d old — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 64d old — https://www.sourcee.app/journo-request/cybersecurity-companies-and-experts-ai-scams-and-consumer-safety
- [low] 64d old — https://www.sourcee.app/journo-request/ai-automation-experts-speakers-on-marketing-sales-operations-gains
- [low] 132d old — https://www.sourcee.app/journo-request/investigative-reporters-openai-training-predatory-dynamic-pricing

## Dropped off the feed

Still fetching, but absent from the newest digest — colder than the age says.

- [high] 70d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [medium-high] 70d old — page no longer serves the request — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium] 69d old — page no longer serves the request — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [low] 63d old — page no longer serves the request — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 60d old — page no longer serves the request — https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- [low-medium] 51d old — page no longer serves the request — https://www.sourcee.app/journo-request/insurance-agents-ai-use-in-personal-lines
- [low] 49d old — page no longer serves the request — https://www.sourcee.app/journo-request/parents-ai-acting-as-pseudoparent-in-kid-questions
- [low-medium] 49d old — page no longer serves the request — https://www.sourcee.app/journo-request/employees-conflicted-about-ai-use-generative-ai-workplace-impact
- [low] 48d old — page no longer serves the request — https://www.sourcee.app/journo-request/k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact
- [low] 44d old — page no longer serves the request — https://www.sourcee.app/journo-request/emergency-managers-ai-tools-for-funding-and-staffing-shortfalls
- [low] 43d old — page no longer serves the request — https://www.sourcee.app/journo-request/swiss-ai-companion-users-emotional-bonds-and-daily-life
- [low] 43d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-data-labelers-in-germany-positive-and-negative-experiences
- [low] 43d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories
- [low] 42d old — page no longer serves the request — https://www.sourcee.app/journo-request/uk-ai-data-trainers-daytoday-work
- [low] 42d old — page no longer serves the request — https://www.sourcee.app/journo-request/patent-attorneys-and-agents-startup-ip-starter-pack
- [low] 36d old — page no longer serves the request — https://www.sourcee.app/journo-request/minnesotans-using-chatgpt-and-ai-tools-experiences-with-election-info
- [low] 35d old — page no longer serves the request — https://www.sourcee.app/journo-request/painters-and-photographers-ai-impact-on-art
- [low] 35d old — page no longer serves the request — https://www.sourcee.app/journo-request/legal-assistants-paralegals-and-lawfirm-staff-jobs-eliminated-by-ai
- [low] 35d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-companion-users-in-africa-friendship-and-emotional-impact
- [low] 35d old — page no longer serves the request — https://www.sourcee.app/journo-request/pro-se-litigants-using-generative-ai-access-to-justice-impact
- [low] 33d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-app-and-saas-founders-1k-mrr-youtube-feature-growth-tactics
- [low] 30d old — page no longer serves the request — https://www.sourcee.app/journo-request/carleton-students-ai-impact-on-dating-experiences
- [low] 30d old — page no longer serves the request — https://www.sourcee.app/journo-request/new-yorkers-ai-music-playing-in-cabs-and-local-businesses
- [low] 30d old — page no longer serves the request — https://www.sourcee.app/journo-request/western-students-using-ai-companions-psychological-effects
- [low] 28d old — page no longer serves the request — https://www.sourcee.app/journo-request/anthropic-project-panama-employees-book-digitization-and-ai-training
- [low] 28d old — page no longer serves the request — https://www.sourcee.app/journo-request/nj-parents-and-teachers-ai-school-surveillance-and-data-practices
- [low] 27d old — page no longer serves the request — https://www.sourcee.app/journo-request/fanvue-chatters-nsfw-ai-model-experiences
- [low] 24d old — page no longer serves the request — https://www.sourcee.app/journo-request/sound-artists-and-field-recordists-run-radio-aarhus-open-call
- [low] 23d old — page no longer serves the request — https://www.sourcee.app/journo-request/students-whose-professors-allow-ai-ai-use-in-coursework
- [low] 23d old — page no longer serves the request — https://www.sourcee.app/journo-request/carleton-students-ai-dating-advice-impact-on-dating-experience
- [low] 23d old — page no longer serves the request — https://www.sourcee.app/journo-request/former-software-engineers-turned-traders-pivot-after-layoff-or-ai
- [low] 23d old — page no longer serves the request — https://www.sourcee.app/journo-request/members-club-and-hospitality-pros-in-hong-kong-postcovid-trends
- [low] 21d old — page no longer serves the request — https://www.sourcee.app/journo-request/buyers-and-sellers-without-agents-diy-property-sale-experience
- [low] 21d old — page no longer serves the request — https://www.sourcee.app/journo-request/editors-creatives-and-graphic-designers-ai-impact-documentary
- [low] 21d old — page no longer serves the request — https://www.sourcee.app/journo-request/character-ai-users-emotional-attachment-and-loneliness
- [low] 16d old — page no longer serves the request — https://www.sourcee.app/journo-request/carleton-students-ai-use-in-dating-advice
- [low] 16d old — page no longer serves the request — https://www.sourcee.app/journo-request/aussie-travellers-1861-hotel-tech-abandoned-bookings-and-ai-concerns
- [low] 16d old — page no longer serves the request — https://www.sourcee.app/journo-request/young-adults-1835-ai-impact-on-comingofage
- [low] 16d old — page no longer serves the request — https://www.sourcee.app/journo-request/people-with-ai-psychosis-firsthand-accounts
- [low] 16d old — page no longer serves the request — https://www.sourcee.app/journo-request/new-authors-ai-market-dilution-and-fair-use-impact-on-writing
- [low] 16d old — page no longer serves the request — https://www.sourcee.app/journo-request/marketers-and-creators-using-ai-agents-timesaving-wins
- [low] 16d old — page no longer serves the request — https://www.sourcee.app/journo-request/ut-austin-students-ai-trump-crypto-ads-on-game-livestreams

---

## Clearing the queue

After sending, record it so the row does not reappear:

```json
{"pitched": {"<url>": "2026-09-15"}, "skipped": {"<url>": "reason"}}
```

Ledger: `marketing/haro-outreach/pitch-ledger.json`
