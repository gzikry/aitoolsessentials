# Pitch queue — clear this in one pass

Built 2026-10-29 from 210 unique requests across the digest history. **4 sendable**, 60 live, 143 cold (> 10 days and unpitched).

*"Sendable" is the number that matters and the one the headline used to hide: a live page is not a candidate. A row counts as sendable only when it is live, not cold, not dropped off, not already pitched, ranked above the tangential band, and has a resolved reply route (a published email, a named handle, a booking link). The other live rows are off-beat calls this queue already documents as excluded.*

**Ages are read off each request page** (`datePublished`), not off the digest text — see `marketing/haro-outreach/verified-requests.json`, refreshed by `scripts/verify_journo_requests.py`. An earlier build fell back to the digest's first-seen date and showed a 190-day-old request as 8 days old.

**No renewal signal exists on this source.** Sourcee publishes no renewal signal: on the 300 most recently indexed slugs and all 30 slugs of the live AI topic feed (checked 2026-09-19) the sitemap lastmod is byte-identical to datePublished, so 'never refreshed' is not observable and is not claimed here. Cold means old and unpitched, not provably abandoned.

**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, Qwoted and Medialyst need authenticated sessions, and Sourcee redacts the requester's own address in the request body. That is why 43 flagged opportunities produced zero pitches. Reply routes are named per row — including addresses resolved off the *publication's* own site (a byline page or an editorial contact page), which is now the strongest route class in this queue.

## Drafts that exist and were never sent

Read this before clearing the queue: 42 draft files exist on disk. **3 of the pitches drafted here have now been sent** — listed at the bottom, not as work. The rest are still unsent; a written draft is not progress — the send is.

**THE QUEUE HOLDS 4 SENDABLE ROW(S).** A row is declared sendable on two facts evidenced separately rather than trusted from a digest field: a relevance above the tangential band, and a reply route verified by fetching a page today. Both are named in the row. The previous run reported 4; the last run before it with a non-zero count was 2026-10-28, with 0 consecutive zero run(s) in between. The live unpitched set is 60 rows.

**Today's draft file is `pitch-drafts-2026-10-29.md` (derived from disk, not typed).** The headline figures are re-derived every run: 44 of 99 tools publish a monthly price, 35 of those at or under $25/month, median $17.50 (snapshots `updated: 2026-10-29`). Superseded sets still sitting in older dated drafts (40/31/$16.50 and earlier) must not be reused.

**The pair range is `1.11x to 2.53x, median 1.25x` over 19 tiers, and it held today.** History, because every superseded value is still sitting in dated draft files and must not be reused: the range was first published as `1.21x to 2.53x, median 1.33x` (2026-09-18, sent to a real correspondent — wrong because the pair population was regex-dependent and undefined); corrected to `1.16x to 2.53x, median 1.25x` over 18 curated pairs (2026-09-21); then re-derived to `1.11x to 2.53x` when the replit-ai snapshot was refreshed (2026-09-22). See `data/monthly_annual_pairs.json` and `scripts/extract_monthly_annual_pairs.py`, which refuses to write the file at all unless every curated pair re-asserts against the live snapshot.

- anthropic-users-and-business-owners-customer-service-experiences — **Crossed cold 2026-09-23; now 47d old — no longer counted as sendable.** Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal hliwrites.99 (re-read verbatim off the live page 2026-09-30). Send late or record as skipped in `pitch-ledger.json`; the crossing is logged in `cold_without_a_send`.
- employees-blocked-from-ai-on-work-accounts-automating-tedious-ta — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — §3 in `pitch-drafts-2026-10-29.md`. Now 24d old.** Route: LinkedIn DM to linkedin.com/in/christopher-mims-club/ (LinkedIn byline page — route-checks probe 2026-10-29: HTTP 200, 609,107 bytes, title 'Christopher Mims - The Wall Street Journal | LinkedIn'; the request's own body says '(DMs open)'; muckrack.com/christopher-mims 403 and wsj.com/news/author/christopher-mims 401 are dead ends, not routes — both re-checked in the same 2026-10-29 probe). It has left the sendable count: the row is now past the 10-day line and this queue no longer ranks it as actionable. The route is not dead and the draft named above is still paste-ready — George's call is to send it late or record it skipped in `pitch-ledger.json`. Silence is the one option that leaves it drifting.
- finops-professionals-agentic-ai-cost-overruns — **Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1. Now 52d old.** Route: LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 and still unsent — the longest-standing high-relevance request this monitor has never answered. Send it late or drop it, do not draft it a fifth time.
- tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — §3 in `pitch-drafts-2026-10-29.md`. Now 19d old, carried in 17 draft files.** Route: hello@tobiamure.com, the address the journalist publishes himself on his own site — tobiamure.com homepage — route-checks probe 2026-10-29: HTTP 200, 63,200 bytes, title 'Tobi Amure, CFEI® | Finance &amp; Technology Journalist', with the contact form on tobiamure.com/contact — route-checks probe 2026-10-29: HTTP 200, 18,379 bytes, title 'Contact Tobi Amure | Finance &amp; Technology Journalist' as the fallback if mail bounces. Deliverability is NOT SMTP-verified: the domain's MX answers 554 Relay access denied for a real address, a fake control and postmaster@ alike, so that probe discriminates nothing. He asks for 'original data, or a survey with its sample size and method' and refuses DM pitches, which is why the draft leads with the one measured series we hold. Past the 10-day line the send is still possible — a late send or a ledger entry closes it; silence leaves it drifting exactly as the WSJ row did on 2026-10-16.

### Already sent — do NOT re-send

- fulltime-employees-shadow-ai-use-and-paying-outofpocket — **SENT BUT BOUNCED — the address is dead, do not retry it; a fresh route is needed before this row can be sent at all.** `pitch-ledger.json`: 2026-10-10 (SENT BUT BOUNCED - see log)
- google-and-claude-enterprise-users-seats-and-token-costs — SENT. `pitch-ledger.json`: 2026-10-10
- speciality-food-retailers-and-producers-how-theyd-spend-10k-on-t — SENT. `pitch-ledger.json`: 2026-10-10

## Send these now (3) — a finished draft and a live route

Each row below has a finished, paste-ready pitch in `pitch-drafts-2026-10-29.md` and a page that served the request today. All 3 are inside the 10-day line. A send, or a `skipped` entry in `pitch-ledger.json`, closes each one. A rewrite of the same draft does not.

- **§3 in `pitch-drafts-2026-10-29.md`** — https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training — 1d old, page live today, route named in the draft
- **§1 in `pitch-drafts-2026-10-29.md`** — https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes — 2d old, page live today, route `alison@alisoncoleman.co.uk`
- **§2 in `pitch-drafts-2026-10-29.md`** — https://www.sourcee.app/journo-request/employees-at-european-orgs-switch-from-us-ai-provider-to-mistral — 6d old, page live today, route `tspirlet@businessinsider.com`

## Sendable — pitch these (4)

Live, not cold, ranked above the tangential band, and with a reply route a human can actually use. This is the whole actionable queue.

### [medium] AI / Workplace Adoption / Training & Skills
- **URL:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-29, last 2026-10-29 (1x)
- **Publication:** Vidhya Das, Business Today (India Today group) - the page's own domain field is businesstoday.in and the body signs 'Business Today'; her author page businesstoday.in/author/vidhya-das returns HTTP 200 (662,049 bytes) with the title 'Trainee Sub Editor'. · domain businesstoday.in
- **Reply route:** Address redacted ('You can also email me at [email redacted]'). Published routes: comment on the LinkedIn post, or DM her - handle resolved as in.linkedin.com/in/vidya-das through search on 2026-10-29 (profile title 'Trainee Sub Editor | Business Today | India Today group'), NOT off the request page; LinkedIn answers HTTP 999 to this monitor's probe, so the handle is search-resolved rather than page-verified. Her Business Today author page publishes no email. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; LinkedIn DM route named in the row: in.linkedin.com/in/vidya-das (George sends)_
- **Angle:** Data-led: median cheapest paid tier $17.50/seat/month across the 44 of 99 tracked tools that publish a monthly price, 35 of those at or under $25 - i.e. per-seat cost is low enough that adoption outruns training. Signed AIToolsEssentials, under 200 words. See pitch-drafts-2026-10-29.md section 3.

### [medium] AI / Small Business / First-Hire Substitution
- **URL:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-28, last 2026-10-29 (2x)
- **Publication:** Alison Coleman, Forbes senior contributor (page author field 'Alison Coleman', domain forbes.com; her Forbes bio, read through search 2026-10-28, says she is a freelance journalist and founder of Coleman Media Ltd. covering entrepreneurs and their startups). · domain forbes.com
- **Reply route:** The body's address is platform-redacted ('email: [email redacted]'), and the page publishes no link or handle. ROUTE RESOLVED OFF HER OWN SITE, not guessed: https://www.alisoncoleman.co.uk/contact-me/ returns HTTP 200, 28,082 bytes, title 'Contact me : Alison Coleman', and prints in visible body text 'Email: alison@alisoncoleman.co.uk', 'Twitter: @alisonbcoleman', 'Skype: alisonbcoleman', beside a Contact Form 7 form (action /contact-me/#wpcf7-f52-p21-o1) as the fallback; her homepage https://www.alisoncoleman.co.uk/ returns HTTP 200, 21,396 bytes, title 'Alison Coleman'. Both recorded in route-checks-2026-10-29.json. alisoncoleman.co.uk MX = Google Workspace (aspmx.l.google.com first). Forbes' own byline page https://www.forbes.com/sites/alisoncoleman/ answers HTTP 403 (770 bytes) to us, so her own site is the only readable route. Email to a published address - a human send, George's lane. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: alison@alisoncoleman.co.uk (George sends)_
- **Angle:** Lead with the measured substitute cost, not a description of the site: 'Of the 99 AI tools we price, 44 publish a monthly per-seat price; 35 of those sit at or under $25, median $17.50 (checked 2026-10-28).' Then state plainly what we cannot give her (first-person testimony from a switching business) and offer the price set as background with check dates and vendor URLs on every figure. […] (full angle in the digest entry for this row)

### [medium] AI / Founders / Bootstrapping & Capital Substitution
- **URL:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-28, last 2026-10-29 (2x)
- **Publication:** Alison Coleman, Forbes (page author field; domain field is empty, and the two requests were posted seven minutes apart so they are one commissioning pass - the sibling request carries forbes.com).
- **Reply route:** Address platform-redacted ('[email redacted]'); no link or handle on the page. Same reporter as the solopreneur request above, so the route is the same one already resolved and re-probed today: alison@alisoncoleman.co.uk published in visible text on https://www.alisoncoleman.co.uk/contact-me/ (HTTP 200, 28,082 bytes, route-checks-2026-10-29.json), with the site's contact form as fallback. George's lane. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: alison@alisoncoleman.co.uk (George sends)_
- **Angle:** None of its own - covered by pitch-drafts-2026-10-28.md section 1, which names both of Alison Coleman's open requests in one email.

### [medium] AI / Vendor Switching / Procurement, Sovereignty & Cost Trade-offs
- **URL:** https://www.sourcee.app/journo-request/employees-at-european-orgs-switch-from-us-ai-provider-to-mistral
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-24, last 2026-10-29 (6x)
- **Publication:** Thibault Spirlet, tech reporter in Business Insider's London office (the page's domain field is businessinsider.com; the body signs 'Thibault Spirlet, Business Insider'). · domain businessinsider.com
- **Reply route:** The request body's address is redacted by Sourcee ('please email me at [email redacted]'), and the page publishes no link of its own. ROUTE FOUND: the reporter's own Business Insider byline page publishes the address as a mailto link — businessinsider.com/author/thibault-spirlet (HTTP 200, title 'Thibault Spirlet - Business Insider', measured and recorded in route-checks-2026-10-29.json; the probe finds tspirlet@businessinsider.com 5 times in the page markup, alongside group-subscriptions@ and support@). Address published: tspirlet@businessinsider.com. Fallbacks published on the same page: linkedin.com/in/thibault-spirlet/ and x.com/ThibaultSpirlet. The page also states his beat is 'AI's impact on the workplace, job and cognitive skills', which is narrower than the switch story he is sourcing here. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: tspirlet@businessinsider.com (George sends)_
- **Angle:** Offer the measured cost side of the switch, not testimony: state in the first sentence that we are a publisher with a dated price set and not an employee of a switching org. Then the per-seat comparison […] (full angle in the digest entry for this row)

## Live but not sendable (56)

These pages resolve and the requests are unexpired, so they are recorded — but none has both a relevance above the tangential band and a usable route. They are listed for completeness, not as candidates: pitching any of them would mean claiming standing we do not have (see the exclusions in the newest `pitch-drafts-*.md`).

### [low-medium] AI / Anthropic Governance / Value Distribution (adjacent)
- **URL:** https://www.sourcee.app/journo-request/claude-users-anthropic-public-benefit-fund-trust-and-job-impact
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-23, last 2026-10-29 (7x)
- **Publication:** Ryan Moeller (the page's own author field). No outlet named; the body reads as a LinkedIn community post.
- **Reply route:** No route of any kind: the body names no channel, the page publishes no address or booking link, and it is not even an email-wall request. The two social URLs that appear in the raw payload are Sourcee's own footer chrome rather than the poster's profile - both were found on three unrelated request pages today (boston-soccer-parents, couples-letting-ai, rig-hse-officers), which is why they sit in the shared CHROME filter. They are NOT a route to this journalist, and are deliberately not written out here because a bare handle string in this field is what has twice made a route-less row read as sendable. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, and the ask is opinion, not data. NOT DRAFTED.

### [low] Consumer / Property / DIY Sale (not AI)
- **URL:** https://www.sourcee.app/journo-request/buyers-and-sellers-without-agents-diy-property-sale-experience
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-29, last 2026-10-29 (1x)
- **Publication:** Anna (page author field 'Anna_the_journo'), a producer on the SBS TV show 'Insight' (sbs.com.au, named in the body). · domain sbs.com.au
- **Reply route:** Platform reply only: the body says 'Feel free to comment or DM' on the Reddit thread Sourcee ingested; the handle in the author field is the only identifier. No address, no link. The page publishes no address, handle or link of its own.  ·  _no — platform reply (George)_
- **Angle:** None. Off-beat and route-less. NOT DRAFTED.

### [low] Media / Creative Work / Unpaid Documentary Recruitment
- **URL:** https://www.sourcee.app/journo-request/editors-creatives-and-graphic-designers-ai-impact-documentary
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-29, last 2026-10-29 (1x)
- **Publication:** An unnamed studio (page author field 'your_pro_Designer'); no publication, no masthead, no company named in the body.
- **Reply route:** Comment on the originating post only - the page publishes no address, handle or link, and the body asks people to 'show us your day, a clip of you telling us about your story'. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Unpaid crew call, wrong side of the camera, no route. NOT DRAFTED.

### [low] AI / Personal Finance / Existential-Risk Testimony
- **URL:** https://www.sourcee.app/journo-request/ai-researchers-founders-and-tech-ceos-retirement-plans-amid-ai-risk
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-29, last 2026-10-29 (1x)
- **Publication:** Thibault Spirlet, tech reporter in Business Insider's London office (domain field businessinsider.com; the body is signed as a Business Insider call for sources). · domain businessinsider.com
- **Reply route:** Address redacted in the body ('email me at [email redacted] before Friday'). The same reporter's byline route is already resolved and re-probed today: businessinsider.com/author/thibault-spirlet (HTTP 200, 328,800 bytes, tspirlet@businessinsider.com published in a mailto link) - route-checks-2026-10-29.json. The request body's address is redacted by Sourcee. Links published on the page: https://lnkd.in/e5E_f8RM.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: tspirlet@businessinsider.com (George sends)_
- **Links published on the page:** https://lnkd.in/e5E_f8RM
- **Angle:** None. Requires holding an existential-risk position we do not hold. NOT DRAFTED - but the reporter is live, see the Business Insider row.

### [low] AI / Oil & Gas / HSE Computer Vision
- **URL:** https://www.sourcee.app/journo-request/rig-hse-staff-aienabled-cameras-trial-outcomes
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-29, last 2026-10-29 (1x)
- **Publication:** Roxana Shirkhorshidi (page author field); no publication named.
- **Reply route:** Comment on the post or send a message: 'Share your thoughts in the comments - or, if you'd prefer to talk, send me a message'. No address or handle published. The page publishes no address, handle or link of its own.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. Right shape, wrong standing, no route. NOT DRAFTED.

### [low] AI / Consumer Finance / Linked Accounts Testimony
- **URL:** https://www.sourcee.app/journo-request/users-who-linked-bank-and-brokerage-accounts-to-llms-ai-finance
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-28, last 2026-10-29 (2x)
- **Publication:** Genna Contino, MarketWatch (page author field; domain marketwatch.com). · domain marketwatch.com
- **Reply route:** The body's address is platform-redacted ('Email me at [email redacted]'). The page publishes no link, handle or form. No route resolved this run; marketwatch.com was not probed for a byline address because the ask is not one we can answer. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Consumer testimony only; address redacted; no route. NOT DRAFTED.

### [low] AI / Creative Work / Testimony
- **URL:** https://www.sourcee.app/journo-request/musicians-artists-writers-and-creators-ai-impact-on-creativity
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-28, last 2026-10-29 (2x)
- **Publication:** Chloe Bishop (page author field). No publication on the page - the domain field is empty, and the body says 'for a feature I am pitching'.
- **Reply route:** The page publishes no address, handle, link or form at all. A platform reply on Sourcee itself, which is not a route we hold credentials for. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Opinion testimony; no publication; no route. NOT DRAFTED.

### [low] Publishing / Literary Magazines / Body-level AI hit only
- **URL:** https://www.sourcee.app/journo-request/literary-writers-thoughts-on-lit-mags-funny-deep-frustrated
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-28, last 2026-10-29 (2x)
- **Publication:** Becky Tuch (page author field), writing for her Thursday column at Lit Mag News.
- **Reply route:** No address, link, handle or form published on the page. Platform reply only. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. The AI token is a joke in the copy; no ask, no route. NOT DRAFTED.

### [low] AI / Manufacturing / Skilled Trades
- **URL:** https://www.sourcee.app/journo-request/canadian-skilled-trades-workers-ai-impact-on-manufacturing
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-29, last 2026-10-29 (1x)
- **Publication:** Andrea Wahbe (page author field); no publication named anywhere in the body.
- **Reply route:** DM only: 'Please DM me if interested.' No address, no link, no handle published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No publication, no route, wrong standing. NOT DRAFTED.

### [low] AI / Consumer Chatbots / First-Person Testimony
- **URL:** https://www.sourcee.app/journo-request/character-ai-users-emotional-attachment-and-loneliness
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-29, last 2026-10-29 (1x)
- **Publication:** A Reddit user (page author field 'Melodic-Phrase-3303'), self-described journalist, no publication named.
- **Reply route:** Reply on the originating thread; no address or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Testimony request, no route. NOT DRAFTED.

### [low] AI / Founder Feature Promotion (not a request)
- **URL:** https://www.sourcee.app/journo-request/gcc-founders-and-entrepreneurs-ai-collaboration-and-data-sovereignty
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-29, last 2026-10-29 (1x)
- **Publication:** Ornella Nett (page author field); the body is a promotional write-up of a feature on Lenks.ai and Rawan Almogbil, with a LinkedIn link (lnkd.in/dD9PhQZj).
- **Reply route:** DM the author on LinkedIn; the only link on the page is the article itself. Links published on the page: https://lnkd.in/dD9PhQZj.  ·  _no — published booking link https://lnkd.in/dD9PhQZj (George)_
- **Links published on the page:** https://lnkd.in/dD9PhQZj
- **Angle:** None. Not a request. NOT DRAFTED.

### [low] AI / Agritech / Dairy Livestock
- **URL:** https://www.sourcee.app/journo-request/dairy-companies-and-startups-aipowered-livestock-health-and-nutrition
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-29, last 2026-10-29 (1x)
- **Publication:** Ankit Saproo (page author field); no publication named.
- **Reply route:** Reach out via the post - the body says 'Kindly reach out'; no address, link or handle published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Off-beat and route-less. NOT DRAFTED.

### [low] AI / Privacy Governance / NOT A REQUEST (founder milestone post)
- **URL:** https://www.sourcee.app/journo-request/excorporate-privacy-lead-built-privacy-and-ai-consultancy
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-10-29 (3x)
- **Publication:** Aakash Suri (the page's author field). No publication on the page - the domain field is empty.
- **Reply route:** The page publishes no address, handle, link or form. The body is a first-person anniversary post about leaving corporate employment, not a call for sources. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Not a request - no ask and no route. NOT DRAFTED.

### [low] AI / Higher Education / Student Testimony
- **URL:** https://www.sourcee.app/journo-request/students-whose-professors-allow-ai-ai-use-in-coursework
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-10-29 (3x)
- **Publication:** Reddit handle 'LegitimateOil90' (the page's author field). Says they are a journalism student. No publication named.
- **Reply route:** The page publishes no address, handle beyond the author field, or link. The body asks respondents to 'send me a message or comment' - a platform reply on Sourcee itself, which is not a route we hold credentials for. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Wants student testimony; no route. NOT DRAFTED.

### [low] Hospitality / Video Sourcing (body-level AI hit, slug has no AI token)
- **URL:** https://www.sourcee.app/journo-request/members-club-and-hospitality-pros-in-hong-kong-postcovid-trends
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-10-29 (3x)
- **Publication:** Reddit-style handle 'Hihellohi' (the page's author field). No publication named.
- **Reply route:** No address, link or handle published. The body asks for on-camera or voice-note interviews; platform reply only. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Wants on-camera hospitality testimony; no route. NOT DRAFTED.

### [low] Healthcare / Book Contribution Call (body-level AI hit)
- **URL:** https://www.sourcee.app/journo-request/canadian-health-innovators-voices-of-innovation-canada-nov-16
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-10-29 (3x)
- **Publication:** Glenn Lanteigne (author field). A book series ('Voices of Innovation', Canadian edition), no publication domain.
- **Reply route:** No address, link or handle published on the page; the call is to participate in a book, with a stated deadline of 2026-11-16. Links published on the page: https://lnkd.in/g2f3pGmu, https://lnkd.in/g8ugVuWR.  ·  _no — published booking link https://lnkd.in/g2f3pGmu (George)_
- **Links published on the page:** https://lnkd.in/g2f3pGmu, https://lnkd.in/g8ugVuWR
- **Angle:** None. Book contribution call for clinicians; no route. NOT DRAFTED.

### [low] AI / B2B Marketing / Startup Branding
- **URL:** https://www.sourcee.app/journo-request/ai-startup-founders-and-marketers-b2b-marketing-as-show-business
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-28, last 2026-10-29 (2x)
- **Publication:** Shalaka Kulkarni, LiveMint (page author field and body '@livemint'; domain livemint.com). · domain livemint.com
- **Reply route:** No address, handle, link or form is published on the page; the body names the publication and nothing else. No route resolved. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Marketing-practice testimony; no route. NOT DRAFTED.

### [low] AI / Companion Chatbots / Personal Testimony (podcast sourcing)
- **URL:** https://www.sourcee.app/journo-request/people-using-llms-as-companions-emotional-support-stories
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-26, last 2026-10-29 (4x)
- **Publication:** Rose Guingrich, PhD (the page's author field). The body names the two people actually collecting: Kim Shirin Cupal, a journalist and audio producer, working with Hilke Schellmann on a mini-podcast series for Jennifer Strong's SHIFT podcast, funded by the Pulitzer Center. No publication domain on the page.
- **Reply route:** The body publishes two live channels and redacts the third: Reddit u/KimCupal and Discord kimcupal are printed verbatim in the request body, while the email is platform-redacted ('Email: [email redacted]'). The page itself publishes no link, and the raw payload carries no address. ROUTE CLASS THAT IS NEW FOR THIS MONITOR: a named Reddit handle read straight off the request body - usable without any signup, unlike the LinkedIn DMs which need George's session. NOT VERIFIED: no page was fetched to confirm the handle exists or is still active; a Reddit profile probe was not run this pass, so treat the handle as published-but-unconfirmed. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. The ask is first-person experience and we would have to invent it. NOT DRAFTED.

### [low] AI / Higher Education Admissions / Judgment Assessment
- **URL:** https://www.sourcee.app/journo-request/admissions-leaders-and-researchers-measuring-judgment-amid-ai
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-10-29 (3x)
- **Publication:** Dr. Aviva Legatt, contributing to Forbes (the page's domain field is forbes.com). · domain forbes.com
- **Reply route:** The body says 'please reply to me directly' and the page publishes no address, handle or link. Platform reply only; no route resolved. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Wants admissions leaders and assessment researchers; no route. NOT DRAFTED.

### [low] AI / Consumer Behaviour / Student Testimony
- **URL:** https://www.sourcee.app/journo-request/carleton-students-ai-dating-advice-impact-on-dating-experience
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-10-29 (3x)
- **Publication:** Reddit handle 'Individual_Hawk_5754' (author field), a reporter for The Charlatan, Carleton University's independent newspaper (domain field charlatan.ca). · domain charlatan.ca
- **Reply route:** No address, handle or link published. The body asks for a DM: 'send me a DM and we can arrange a time'. Platform reply only. The page publishes no address, handle or link of its own.  ·  _no — platform reply (George)_
- **Angle:** None. Student testimony only; no route. NOT DRAFTED.

### [low] Personal Finance / Celebrity Agents / Interview Series
- **URL:** https://www.sourcee.app/journo-request/celebrity-agents-how-i-manage-my-money-series
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-10-29 (3x)
- **Publication:** Emily Braeger, The i Paper (the page's author field and domain theipaper.com). · domain theipaper.com
- **Reply route:** The body's address is platform-redacted ('Please email me at [email redacted]'). The page publishes no link or handle. No route resolved; the i Paper's own contact page was not probed for a byline address this run. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Wants celebrity agents; address redacted; no route. NOT DRAFTED.

### [low] AI / Careers / Software Engineers Turned Traders
- **URL:** https://www.sourcee.app/journo-request/former-software-engineers-turned-traders-pivot-after-layoff-or-ai
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-10-29 (3x)
- **Publication:** Thibault Spirlet, tech reporter, Business Insider London (page author field 'Thibault_SpirletBI', domain businessinsider.com). THE SAME REPORTER as this queue's one sendable row. · domain businessinsider.com
- **Reply route:** The body's address is platform-redacted ('please email me at [email redacted]'), but this reporter's address is already resolved off his own byline page and RE-PROBED TODAY: businessinsider.com/author/thibault-spirlet HTTP 200, 326,570 bytes, tspirlet@businessinsider.com published in a mailto link and 5 times in the markup (route-checks-2026-10-29.json). Automatable? No - George's lane. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: tspirlet@businessinsider.com (George sends)_
- **Angle:** None for this row's ask (wants trader testimony we do not have). Its byline route is reused by the Mistral draft, pitch-drafts-2026-10-27.md section 1.

### [low] AI / Blue-Collar AI Adoption / Utilities & Construction
- **URL:** https://www.sourcee.app/journo-request/ai-companies-in-utilities-and-construction-frontline-safety-and-workload
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-10-29 (3x)
- **Publication:** Lindsay Dodgson, CNBC (page author field, domain cnbc.com). · domain cnbc.com
- **Reply route:** The body's address is platform-redacted. No link, handle or form published; no route resolved. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Wants AI vendors; address redacted; no route. NOT DRAFTED.

### [low] Arts / Open Call (false positive - not AI)
- **URL:** https://www.sourcee.app/journo-request/sound-artists-and-field-recordists-run-radio-aarhus-open-call
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-26, last 2026-10-29 (4x)
- **Publication:** Run_Radio (author field) - RUN RADIO, a music radio station and sound archive in Aarhus, Denmark, run with the Institute for X.
- **Reply route:** Email is platform-redacted ([email redacted]) and the page publishes no link or handle. The body asks for a downloadable transfer link by email. NOT RESOLVED and not worth resolving: the call is for field recordings, DJ mixes and sound art. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Not an AI request and no route. NOT DRAFTED.

### [low] AI / Consumer Behaviour / Social Connection
- **URL:** https://www.sourcee.app/journo-request/people-using-ai-for-social-advice-communication-and-connection-impact
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-25, last 2026-10-29 (5x)
- **Publication:** Trisha Mahajan, for TOI Digital (The Times of India) - the outlet is named in the body ('I'm working on a story for TOI DIGITAL', closing line 'The Times of India') and the author field carries her name; the page's domain field is indiatimes.com. · domain indiatimes.com
- **Reply route:** The body says 'Please reply to this post, DM me or email me ([email redacted])'. Sourcee redacts the address, the page publishes no link or handle of hers, and no address appears anywhere on the page. NOT RESOLVED. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Video Production / Agentic Tooling
- **URL:** https://www.sourcee.app/journo-request/video-teams-using-claude-and-remotion-agentic-video-editing
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-25, last 2026-10-29 (5x)
- **Publication:** Enrico Tartarotti (page author field). No outlet, no domain: the domain field is empty and the body names no publication - this is an individual sourcing for his own project.
- **Reply route:** The body publishes one link, a t.co shortener (https://t.co/4ZzXXpfAC4) with the instruction '(please add a few lines about who you are)'. The page publishes no address and no personal handle; the destination behind the shortener was not resolved, so the route is the post itself. NOT RESOLVED. Links published on the page: https://t.co/4ZzXXpfAC4.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/4ZzXXpfAC4
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / NSFW Creator Economy / Platform Labour
- **URL:** https://www.sourcee.app/journo-request/fanvue-chatters-nsfw-ai-model-experiences
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-23, last 2026-10-29 (7x)
- **Publication:** Dazed magazine (domain field dazeddigital.com); the page's author field is the handle 'Dazedjourno', so no individual byline. · domain dazeddigital.com
- **Reply route:** The body says 'please DM me'; no address, handle or link is published on the page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route published, and no standing to claim. NOT DRAFTED.

### [low] AI / Consumer Behaviour / Relationships (tabloid)
- **URL:** https://www.sourcee.app/journo-request/couples-letting-ai-dictate-relationship-emotions-and-intimacy
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-23, last 2026-10-29 (7x)
- **Publication:** Luke Chafer, The Sun (domain field thesun.co.uk; the body signs 'The Sun'). · domain thesun.co.uk
- **Reply route:** The body says 'I am available here or at [email redacted]' - Sourcee redacts the address and the page publishes no other handle or link. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route, and the ask is first-person experience we cannot supply. NOT DRAFTED.

### [low] Fashion / Halloween (NOT AI - false positive)
- **URL:** https://www.sourcee.app/journo-request/people-recreating-iconic-runway-looks-halloween-costume-story
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-23, last 2026-10-29 (7x)
- **Publication:** Alexandra Hildreth (the page's own author field). No outlet named.
- **Reply route:** The body asks 'Would love to chat for a story' and publishes no address, handle or link. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Not an AI request at all. NOT DRAFTED.

### [low] AI / Faith Communities / Design Tools
- **URL:** https://www.sourcee.app/journo-request/parish-event-organizers-aigenerated-flyers-scourge-or-timesaver
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-23, last 2026-10-29 (7x)
- **Publication:** Zoey Maraist (the page's own author field). No outlet named; the body says 'an article I'm writing'.
- **Reply route:** The page publishes no address, handle or link, and the body names no channel at all. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Supply-Chain Operations / Podcast Panel Booking
- **URL:** https://www.sourcee.app/journo-request/uk-and-eu-sports-retail-supply-chain-leaders-retail-ai-at-scale
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-24, last 2026-10-29 (6x)
- **Publication:** Katie Howard (the page's own author field) sourcing panellists for SupplyChainTalk, the podcast she runs; no outlet domain field is set on the page.
- **Reply route:** No route published: the body says 'I'd love to hear from you' and 'tag them in the comments or drop me a message', but the page carries no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route published and we are not the panellist profile. NOT DRAFTED.

### [low] Founders / Community Q&A (AI mention incidental)
- **URL:** https://www.sourcee.app/journo-request/founders-and-cofounders-fortnightly-founder-qanda
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-24, last 2026-10-29 (6x)
- **Publication:** Lauren Hargreaves, Remobi (named in the body; no outlet domain field on the page).
- **Reply route:** No route published: the body says 'answer in writing, or we jump on a call' and 'Tag a...', but the page carries no address, handle or link. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, and the ask is a founder story we cannot supply. NOT DRAFTED.

### [low] AI / Search & Discovery / Corporate Communications
- **URL:** https://www.sourcee.app/journo-request/nontech-inhouse-corporate-comms-lead-ai-search-and-discovery-strategy
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-29 (8x)
- **Publication:** Andrew Birmingham (the page's own author field). No outlet named in the body; he describes the request as 'for a project I'm running' and addresses it to 'my PR and Comms mates'.
- **Reply route:** The body says only 'If that sounds like you drop me a line' — no address, handle or link to the poster. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, and no standing to claim. NOT DRAFTED.

### [low] AI / Training Data / Labour (broadcast)
- **URL:** https://www.sourcee.app/journo-request/anthropic-project-panama-employees-book-digitization-and-ai-training
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-29 (8x)
- **Publication:** TF1, the French TV network (domain field tf1.fr; the body signs 'TF1'). Reporter not named on the page. · domain tf1.fr
- **Reply route:** The body says 'Feel free to comment below or reach out to me directly' — the page publishes no address and no handle. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, and the ask is insider testimony we do not hold. NOT DRAFTED.

### [low] Geopolitics / AI security (adjacent)
- **URL:** https://www.sourcee.app/journo-request/geopolitical-analysts-and-ai-security-experts-global-hotspots
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-29 (8x)
- **Publication:** Abdurakhmonov NormuhammadAli, sourcing for the Geosiyosat project (no outlet site named).
- **Reply route:** The body asks readers to 'let me know' or name someone who might be interested; no address, handle or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Off-beat and route-less. NOT DRAFTED.

### [low] AI / Workplace Policy / HR
- **URL:** https://www.sourcee.app/journo-request/omaha-hr-representatives-offices-with-written-ai-policies
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-29 (8x)
- **Publication:** Tim Trudell (the page's own author field). Outlet not named in the body; the request is local to the Omaha area.
- **Reply route:** The body says 'please DM me or have them message me' — no address, handle or link to the poster is printed. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Standing impossible (Omaha HR representative). NOT DRAFTED.

### [low] AI / Creative Work / Social Platforms
- **URL:** https://www.sourcee.app/journo-request/digital-artists-aigenerated-posters-flooding-social-feeds
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-29 (8x)
- **Publication:** Chloe O'Keeffe (the page's own author field). No outlet named; the body carries '#mediarequest #journorequests'.
- **Reply route:** The body closes 'DMs open' — no address, handle or link to the poster is printed, and the page publishes no route of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, no standing. NOT DRAFTED.

### [low] AI / Podcast Guest Call / Healthcare & Fintech
- **URL:** https://www.sourcee.app/journo-request/founders-and-ctos-production-ai-tradeoffs-in-healthcare-and-fintech
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-23, last 2026-10-29 (7x)
- **Publication:** Bryan Dennstedt, 'AI with Bry' podcast (domain field bry.net). · domain bry.net
- **Reply route:** The page publishes no address, handle or link; the body says 'I'd love to hear from you' with no channel named. Sourcee redacted the address in the body. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route, and we are not the guest profile. NOT DRAFTED.

### [low] AI / Human Focus / Interview Call
- **URL:** https://www.sourcee.app/journo-request/students-and-professionals-balancing-ai-use-and-human-focus
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-23, last 2026-10-29 (7x)
- **Publication:** KimberMarie Faircloth, The Limitation Game (no domain field set; the body signs the project name).
- **Reply route:** The body says 'Comment below or DM me - please!'; no address, handle or link published on the page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, and the ask is personal testimony. NOT DRAFTED.

### [low] AI / Industrial HSE / Computer Vision
- **URL:** https://www.sourcee.app/journo-request/rig-hse-officers-aienabled-camera-trial-outcomes
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-23, last 2026-10-29 (7x)
- **Publication:** Roxana Shirkhorshidi (the page's own author field). No outlet named.
- **Reply route:** The body says 'Share your thoughts in the comments - or, if you'd prefer to talk, send me a message'; no address, handle or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Marketing / Customer Insight
- **URL:** https://www.sourcee.app/journo-request/brand-managers-ai-to-deepen-customer-insight-and-preserve-humanity
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-21, last 2026-10-29 (9x)
- **Publication:** Daniel Burstein, for MarketingSherpa - the handle and the publication are both named in the body ('Looking for examples from your experience for @MarketingSherpa article'). The page's author field carries his name and domain marketingsherpa.com. · domain marketingsherpa.com
- **Reply route:** The body asks for 'examples from your experience' and publishes one link, a t.co to a previous MarketingSherpa article he wrote as a model of what he publishes. No address, no handle of his own, no scheduling link. NOT RESOLVED. Links published on the page: https://t.co/8JPO9sSjJy.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/8JPO9sSjJy
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Education Surveillance / Data Practices
- **URL:** https://www.sourcee.app/journo-request/nj-parents-and-teachers-ai-school-surveillance-and-data-practices
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-29 (8x)
- **Publication:** Nicole Rosenthal, investigative reporter at NJ.com (named in the page's author field; the body signs 'NJ.com'). · domain nj.com
- **Reply route:** The body says 'DM me or email [email redacted]' — Sourcee redacts the address. No handle and no link to the reporter is published on the request page. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Standing impossible (NJ parent/teacher) and the address is redacted. NOT DRAFTED.

### [low] Podcast booking / Bengaluru founders
- **URL:** https://www.sourcee.app/journo-request/bengaluru-founders-deep-tech-healthcare-biology-housing-and-ai
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-29 (8x)
- **Publication:** Sikandar (page author field), booking guests for the @dostcast podcast.
- **Reply route:** The body says 'Let me know please' — no address, handle or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Off-beat, no route. NOT DRAFTED.

### [low] AI / Fintech / Sponsored feature (likely paid placement)
- **URL:** https://www.sourcee.app/journo-request/fintech-product-managers-nextgen-aipowered-personal-finance-apps
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-29 (8x)
- **Publication:** Paul Dus Navis (the page's own author field). Outlet not named; the body is a single line advertising an 'editorial feature'.
- **Reply route:** The only published route is a LinkedIn short link, https://lnkd.in/gh2gpgwg, which is the feature's own advert link — not a route to a journalist sourcing sources. Links published on the page: https://lnkd.in/gh2gPgwg.  ·  _no — published booking link https://lnkd.in/gh2gPgwg (George)_
- **Links published on the page:** https://lnkd.in/gh2gPgwg
- **Angle:** None. Paid-placement advert, not a source request. DO NOT PITCH.

### [low] AI / Student Life / Dating
- **URL:** https://www.sourcee.app/journo-request/carleton-students-ai-impact-on-dating-experiences
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-20, last 2026-10-29 (10x)
- **Publication:** The Charlatan (charlatan.ca), Carleton University's student paper - named in the body's closing line. The page's author field is a Reddit-style handle, 'Individual_Hawk_5754', with no byline name. · domain charlatan.ca
- **Reply route:** The body's only ask is 'send me a DM and we can arrange a time'. No address, handle or link of the poster's own is published; the page's two links belong to the Sourcee account that republished it. The page publishes no address, handle or link of its own.  ·  _no — platform reply (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Music / Local Business
- **URL:** https://www.sourcee.app/journo-request/new-yorkers-ai-music-playing-in-cabs-and-local-businesses
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-20, last 2026-10-29 (10x)
- **Publication:** WNYC / Gothamist - both named in the body. The page's author field is the handle 'catgone8'; no byline name is published. · domain gothamist.com
- **Reply route:** The body says 'DM me if interested!'. No address, handle or scheduling link of the reporter's own is published on the page. The page publishes no address, handle or link of its own.  ·  _no — platform reply (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / HR / Organisational Decision-Making
- **URL:** https://www.sourcee.app/journo-request/hr-leaders-and-organizational-design-practitioners-decision-fatigue
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-20, last 2026-10-29 (10x)
- **Publication:** Molly Woudenberg, for McLean & Company - a HR research and advisory firm running its own research study, not a newsroom. The body names the team and the firm.
- **Reply route:** The body says 'Comment below or send me a direct message' and offers 'a 30-45 minute virtual research interview'. No address, scheduling link or handle is published. NOT RESOLVED. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Vendor research call, no route, no standing. NOT DRAFTED.

### [low] AI / Enterprise IT / Conference Reporting
- **URL:** https://www.sourcee.app/journo-request/cios-at-gartner-it-symposium-orlando-balancing-ai-risk-and-value
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-21, last 2026-10-29 (9x)
- **Publication:** Paige Gross - the page's author field. No outlet is named in the body or the domain field; she is reporting from the Gartner IT Symposium/Xpo in Orlando this week.
- **Reply route:** The body says 'If you're at the conference and want to connect, drop me a line!' and publishes an lnkd.in short link. No address or personal handle is published; the route is a LinkedIn connection through a short link that cannot be resolved without following it. NOT RESOLVED. Links published on the page: https://lnkd.in/gQ9HXqrU.  ·  _no — published booking link https://lnkd.in/gQ9HXqrU (George)_
- **Links published on the page:** https://lnkd.in/gQ9HXqrU
- **Angle:** None. Standing requires being at the conference. NOT DRAFTED.

### [low] Property / Consumer Law / Disclosure
- **URL:** https://www.sourcee.app/journo-request/estate-agents-and-property-lawyers-disclosure-rules-haunted-homes
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-21, last 2026-10-29 (9x)
- **Publication:** Natasha Christou - the page's author field. No publication is named in the body or the domain field.
- **Reply route:** The body reads 'Please get in touch with me via DM or email at: [email redacted]' - the address is redacted by Sourcee and no handle or link of hers is published. The two links on the page belong to the Sourcee account that republished the request. NOT RESOLVED. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route, no standing, and the AI token is a slug false positive. NOT DRAFTED.

### [low] AI / Product Management / Team Practice
- **URL:** https://www.sourcee.app/journo-request/product-managers-on-512-engineer-teams-engineers-using-ai
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-21, last 2026-10-29 (9x)
- **Publication:** Steve Tauber - the page's author field. No publication, domain or outlet is named anywhere in the body.
- **Reply route:** The body's whole ask is 'Please get in touch!' with no address, handle, link or platform named; the page publishes nothing of the poster's own. NOT RESOLVED. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Podcast / Developer Ecosystem
- **URL:** https://www.sourcee.app/journo-request/bay-area-agentic-ai-builders-agntcon-and-mcpcon-stories
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-21, last 2026-10-29 (9x)
- **Publication:** Luca Berton, whose podcast Udienza (udienza.com, named in the body and in the page's domain field) is a media partner of AGNTCon + MCPCon North America in San Jose, 22-23 October. · domain udienza.com
- **Reply route:** The body says 'If you are in the Bay Area, message me: I want to hear your story' and publishes https://www.udienza.com/. No address or personal handle; the link is the podcast's own site, not a route to the poster. NOT RESOLVED. Links published on the page: https://www.udienza.com/.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://www.udienza.com/
- **Angle:** None. Conference-standing podcast booking with no route. NOT DRAFTED.

### [low] AI / Consumer Marketplace / Resale Pricing
- **URL:** https://www.sourcee.app/journo-request/fb-marketplace-sellers-and-buyers-ai-impact-on-pricing-and-listings
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-19, last 2026-10-29 (11x)
- **Publication:** No author field resolvable off the page, and no outlet named: the body opens 'A fun reporting request' and closes 'Hoping to chat with people for a story and can protect privacy!' The only self-identifying line is 'Half the stuff in my home came from Marketplace. I love it; that's why I'm so curious about this.'
- **Reply route:** The body ends '[email redacted] or message me!' - the address is redacted by Sourcee and no handle is published. The page carries no address, link or reply instruction of its own. NOT RESOLVED. The route would be a DM on the poster's own platform. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Workplace Automation / Customer Service
- **URL:** https://www.sourcee.app/journo-request/uk-customer-service-workers-daytoday-now-ai-automation-vs-human
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-19, last 2026-10-29 (11x)
- **Publication:** No author field on the page. Domain field: cnbc.com, and the body is headed 'For CNBC' with the hashtags #journorequest #journorequests and the outlet name 'CNBC' as its last line. · domain cnbc.com
- **Reply route:** The body reads 'Email: [email redacted]' - redacted by Sourcee - and the only other instruction is the edit line 'Only looking for UK-based sources at this time!'. The page carries no address, handle or link of its own. NOT RESOLVED. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Student Project / AI Companions
- **URL:** https://www.sourcee.app/journo-request/western-students-using-ai-companions-psychological-effects
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-20, last 2026-10-29 (10x)
- **Publication:** No outlet at all: the poster ('Toad') is a student in English 110 at Western building a class podcast, and asks for interviews with Western students. The page's domain field is empty.
- **Reply route:** The body says 'Please DM me or comment below'. Nothing is published to reply to off-platform. The page publishes no address, handle or link of its own.  ·  _no — platform reply (George)_
- **Angle:** None. A class project with no publication, no route and no standing. NOT DRAFTED.

### [low] AI / Consumer Finance / Advice
- **URL:** https://www.sourcee.app/journo-request/consumers-using-ai-for-financial-advice-experience-and-factchecking
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-20, last 2026-10-29 (10x)
- **Publication:** Emily Braeger, for The i Paper - the outlet is named in the body and the author field carries her name. · domain theipaper.com
- **Reply route:** The body reads 'Please email me at [email redacted] if this is you or you can help' - the address is redacted by Sourcee, and the page publishes no link or handle of hers. NOT RESOLVED. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Data Centre Infrastructure / Energy & Tax Policy
- **URL:** https://www.sourcee.app/journo-request/ai-energy-and-tax-experts-project-jupiter-documentary-new-mexico
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-20, last 2026-10-29 (10x)
- **Publication:** Amelia K., sourcing experts for a documentary film on Project Jupiter in New Mexico. No outlet is named; the body offers an lnkd.in short link and interviewing starts mid-November.
- **Reply route:** The body says 'Please reach out if you would like to be interviewed' and publishes an lnkd.in short link plus the Sourcee account's links. No address and no personal handle; the route would be a LinkedIn message through the short link, which cannot be resolved without following it. Links published on the page: https://lnkd.in/g4-_xKt3.  ·  _no — published booking link https://lnkd.in/g4-_xKt3 (George)_
- **Links published on the page:** https://lnkd.in/g4-_xKt3
- **Angle:** None. No route and no standing. NOT DRAFTED.

## Cold — only if you have a reason

Older than the 10-day line and never pitched. Not provably abandoned — no renewal signal exists on this source — but every one of these has already passed an ideal send window.

- [high] 52d old — https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
- [high] 54d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-ai-governance-and-agent-sprawl
- [high] 54d old — https://www.sourcee.app/journo-request/scientists-phd-students-and-postdocs-paying-for-ai-subscriptions
- [high] 100d old — https://www.sourcee.app/journo-request/business-and-technology-leaders-tech-budget-priorities-amid-volatility
- [high] 160d old — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [high] 179d old — https://www.sourcee.app/journo-request/anthropic-api-users-costs-and-token-burn-increase-since-january
- [medium-high] 47d old — https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
- [medium-high] 52d old — https://www.sourcee.app/journo-request/uk-managers-cracked-down-on-gen-z-ai-overuse
- [medium-high] 226d old — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium] 24d old — https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
- [medium] 48d old — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [medium] 52d old — https://www.sourcee.app/journo-request/ai-agents-making-money-2026-sales-and-leadgen-workflow-ops
- [medium] 52d old — https://www.sourcee.app/journo-request/ai-startups-workplace-fraud-detection-expenses-time-theft
- [medium] 52d old — https://www.sourcee.app/journo-request/marketing-and-content-leaders-aiassisted-work-review-process
- [medium] 56d old — https://www.sourcee.app/journo-request/ceos-ai-impact-on-ops-culture-and-commercial-strategy
- [medium] 66d old — https://www.sourcee.app/journo-request/uk-finance-risk-and-regulatory-leaders-ai-explainability-risks
- [medium] 233d old — https://www.sourcee.app/journo-request/sme-owners-operational-challenges-for-ai-solutions-case-study
- [low-medium] 16d old — https://www.sourcee.app/journo-request/b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research
- [low-medium] 19d old — https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
- [low-medium] 23d old — https://www.sourcee.app/journo-request/uk-companies-implementing-ai-how-automation-transforms-workdays
- [low-medium] 27d old — https://www.sourcee.app/journo-request/law-firm-lawyers-concrete-ai-implementations-and-billing-impact
- [low-medium] 28d old — https://www.sourcee.app/journo-request/employees-conflicted-about-ai-use-generative-ai-workplace-impact
- [low-medium] 30d old — https://www.sourcee.app/journo-request/insurance-agents-ai-use-in-personal-lines
- [medium-low] 40d old — https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business
- [low-medium] 43d old — https://www.sourcee.app/journo-request/us-founders-calls-to-slow-ai-development-impact-on-companies
- [medium-low] 49d old — https://www.sourcee.app/journo-request/tech-policy-experts-california-ai-audit-bills-impact-cios
- [low-medium] 68d old — https://www.sourcee.app/journo-request/ai-project-builders-youtube-finance-and-lifestyle-channel-feature
- [low-medium] 113d old — https://www.sourcee.app/journo-request/prompt-engineers-tokenmaxxing-anecdotes
- [low] 12d old — https://www.sourcee.app/journo-request/ai-saas-vendors-targeting-journalists-prs-and-marketers-case-studies
- [low] 12d old — https://www.sourcee.app/journo-request/real-estate-operators-ai-adoption-and-org-restructuring
- [low] 12d old — https://www.sourcee.app/journo-request/memphis-and-southaven-residents-and-env-advocates-xai-colossus-impact
- [low] 12d old — https://www.sourcee.app/journo-request/black-women-in-canada-ai-chatbots-and-healthcare-experiences
- [low] 12d old — https://www.sourcee.app/journo-request/engineering-leaders-leading-people-through-ai-changes
- [low] 13d old — https://www.sourcee.app/journo-request/chemistry-undergrads-and-phd-students-ai-use-in-coursework-and-research
- [low] 13d old — https://www.sourcee.app/journo-request/ai-app-and-saas-founders-1k-mrr-youtube-feature-growth-tactics
- [low] 13d old — https://www.sourcee.app/journo-request/ai-infrastructure-engineers-in-berlin-data-centers-and-bottlenecks
- [low] 13d old — https://www.sourcee.app/journo-request/residents-near-mumbai-ai-data-centres-power-and-water-strain
- [low] 13d old — https://www.sourcee.app/journo-request/single-family-office-cybersecurity-experts-ai-risks-and-opportunities
- [low] 14d old — https://www.sourcee.app/journo-request/painters-and-photographers-ai-impact-on-art
- [low] 14d old — https://www.sourcee.app/journo-request/legal-assistants-paralegals-and-lawfirm-staff-jobs-eliminated-by-ai
- [low] 14d old — https://www.sourcee.app/journo-request/cios-and-ai-leaders-ai-infrastructure-day2-ops-and-costs
- [low] 14d old — https://www.sourcee.app/journo-request/companies-and-data-buyers-selling-corporate-data-to-train-ai
- [low] 14d old — https://www.sourcee.app/journo-request/uk-political-analysts-disinformation-and-ai-manipulation-in-politics
- [low] 14d old — https://www.sourcee.app/journo-request/content-creators-using-ai-job-losses-and-ethics
- [low] 15d old — https://www.sourcee.app/journo-request/school-leaders-and-ngo-staff-ai-adoption-challenges-across-sectors
- [low] 15d old — https://www.sourcee.app/journo-request/minnesotans-using-chatgpt-and-ai-tools-experiences-with-election-info
- [low] 15d old — https://www.sourcee.app/journo-request/ai-policy-advisor-newsom-administration-ai-regulation
- [low] 15d old — https://www.sourcee.app/journo-request/uk-and-us-heads-of-data-and-ai-from-idea-to-production
- [low] 15d old — https://www.sourcee.app/journo-request/ai-companion-users-in-africa-friendship-and-emotional-impact
- [low] 15d old — https://www.sourcee.app/journo-request/pro-se-litigants-using-generative-ai-access-to-justice-impact
- [low] 16d old — https://www.sourcee.app/journo-request/global-development-professionals-using-ai-across-programs-and-policy
- [low] 16d old — https://www.sourcee.app/journo-request/african-founders-building-ai-companies-pitch-deck-realities
- [low] 16d old — https://www.sourcee.app/journo-request/higher-ed-nonfaculty-staff-ai-use-at-work
- [low] 16d old — https://www.sourcee.app/journo-request/podcast-guests-ai-channel-and-partner-ecosystem
- [low] 16d old — https://www.sourcee.app/journo-request/ai-infrastructure-professionals-in-london-capacity-europe-attendees
- [low] 16d old — https://www.sourcee.app/journo-request/b2b-vendors-buyers-pasting-proposals-into-ai-tools
- [low] 17d old — https://www.sourcee.app/journo-request/caine-prize-winners-gen-ai-accusations-targeting-black-writers
- [low] 17d old — https://www.sourcee.app/journo-request/software-engineers-who-left-tech-jobs-lost-to-ai-coding-tools
- [low] 17d old — https://www.sourcee.app/journo-request/manufacturers-and-ai-safety-experts-ai-risks-in-chemical-food-defense
- [low] 17d old — https://www.sourcee.app/journo-request/uk-baby-boomers-misinformation-sharing-and-ai-influence-online
- [low] 18d old — https://www.sourcee.app/journo-request/hedera-builders-shipping-defi-nfts-rwas-ai-games-and-memes
- [low] 18d old — https://www.sourcee.app/journo-request/production-designers-ai-impact-on-future-of-filmmaking
- [low] 18d old — https://www.sourcee.app/journo-request/ai-researchers-and-policy-experts-5-years-us-race-to-superintelligence
- [low] 19d old — https://www.sourcee.app/journo-request/ai-cybersecurity-iot-and-web3-founders-and-operators-news-submissions
- [low] 19d old — https://www.sourcee.app/journo-request/employees-pay-transparency-good-or-bad
- [low] 20d old — https://www.sourcee.app/journo-request/sales-reps-who-cold-call-and-email-how-ai-changed-outreach
- [low] 20d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-and-builders-realworld-deployment-and-strategy
- [low] 20d old — https://www.sourcee.app/journo-request/voters-who-used-ai-to-navigate-ballot-voting-experience
- [low] 20d old — https://www.sourcee.app/journo-request/anthropic-gtm-leaders-scaling-300k-b2b-clients
- [low] 21d old — https://www.sourcee.app/journo-request/patent-attorneys-and-agents-startup-ip-starter-pack
- [low] 21d old — https://www.sourcee.app/journo-request/hotel-and-fandb-supervisors-and-managers-customer-expectations-vs-ai
- [low] 21d old — https://www.sourcee.app/journo-request/researchers-founders-and-funders-ai-transforming-scientific-research
- [low] 21d old — https://www.sourcee.app/journo-request/facebook-marketplace-sellers-ai-listing-photos-and-selling-experience
- [low] 22d old — https://www.sourcee.app/journo-request/aps-hr-leaders-ai-skills-training-and-workforce-planning
- [low] 22d old — https://www.sourcee.app/journo-request/scrum-masters-daytoday-and-career-pivots-and-ai-impact
- [low] 22d old — https://www.sourcee.app/journo-request/real-estate-agents-replacing-pdf-property-brochure
- [low] 22d old — https://www.sourcee.app/journo-request/anz-marketers-ai-and-martech-innovation-spotlight
- [low] 22d old — https://www.sourcee.app/journo-request/solicitors-and-barristers-ai-to-expand-pro-bono-capacity
- [low] 22d old — https://www.sourcee.app/journo-request/uk-ai-data-trainers-daytoday-work
- [low] 22d old — https://www.sourcee.app/journo-request/apac-reporters-and-editors-ai-accountability-coverage
- [low] 22d old — https://www.sourcee.app/journo-request/early-to-midcareer-information-architects-products-featuring-ai
- [low] 22d old — https://www.sourcee.app/journo-request/martech-buyers-ai-impact-on-build-vs-buy-decisions
- [low] 23d old — https://www.sourcee.app/journo-request/ai-infrastructure-experts-china-vs-us-datacenter-capacity
- [low] 23d old — https://www.sourcee.app/journo-request/plaintiffs-attorneys-and-legal-scholars-ai-deepfake-liability
- [low] 23d old — https://www.sourcee.app/journo-request/emergency-managers-ai-tools-for-funding-and-staffing-shortfalls
- [low] 23d old — https://www.sourcee.app/journo-request/coweta-county-artists-and-creatives-data-centers-and-ai-infrastructure
- [low] 23d old — https://www.sourcee.app/journo-request/swiss-ai-companion-users-emotional-bonds-and-daily-life
- [low] 23d old — https://www.sourcee.app/journo-request/ai-data-labelers-in-germany-positive-and-negative-experiences
- [low] 23d old — https://www.sourcee.app/journo-request/ai-data-annotators-and-labellers-experience-with-ai-training-data
- [low] 23d old — https://www.sourcee.app/journo-request/ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories
- [low] 23d old — https://www.sourcee.app/journo-request/academics-social-media-and-ai-impact-on-womens-identity-and-selfesteem
- [low] 24d old — https://www.sourcee.app/journo-request/ai-liability-insurers-and-legal-experts-procurement-and-implementation
- [low] 24d old — https://www.sourcee.app/journo-request/uk-cybersecurity-hiring-managers-state-of-hiring-2026-and-ai-impact
- [low] 24d old — https://www.sourcee.app/journo-request/ai-emotional-support-users-chatbot-therapy-and-journaling
- [low] 24d old — https://www.sourcee.app/journo-request/mortgage-adviser-using-ai-efficiency-and-client-outcomes-video-series
- [low] 24d old — https://www.sourcee.app/journo-request/founders-and-cxos-in-automotive-ai-evs-autonomy-thought-leadership
- [low] 25d old — https://www.sourcee.app/journo-request/video-game-developer-falsely-accused-of-using-generative-ai
- [low] 26d old — https://www.sourcee.app/journo-request/lawyers-and-tech-ethics-experts-ai-wearables-and-legal-journeys
- [low] 26d old — https://www.sourcee.app/journo-request/mls-executives-risks-when-agents-grant-mls-access-to-llms
- [low] 26d old — https://www.sourcee.app/journo-request/real-estate-agents-and-brokers-switched-from-pdf-brochures
- [low] 27d old — https://www.sourcee.app/journo-request/storytellers-and-brand-founders-marys-big-30-ai-story-project
- [low] 27d old — https://www.sourcee.app/journo-request/newsletter-editors-using-ai-agents-news-aggregation-practices
- [low] 27d old — https://www.sourcee.app/journo-request/scottish-teachers-ai-tools-implementation-in-education
- [low] 27d old — https://www.sourcee.app/journo-request/advertising-tech-and-media-pros-in-miami-ai-audience-discovery
- [low] 27d old — https://www.sourcee.app/journo-request/hr-leaders-company-ai-strategies-and-cognitive-offloading-risk
- [low] 28d old — https://www.sourcee.app/journo-request/fea-engineers-using-agentic-ai-practitioner-case-study
- [low] 28d old — https://www.sourcee.app/journo-request/parents-ai-acting-as-pseudoparent-in-kid-questions
- [low] 28d old — https://www.sourcee.app/journo-request/fb-marketplace-sellers-ai-photos-and-description-prompts
- [low] 28d old — https://www.sourcee.app/journo-request/k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact
- [low] 28d old — https://www.sourcee.app/journo-request/ai-summit-barcelona-attendees-controversy-and-experiences
- [low] 28d old — https://www.sourcee.app/journo-request/ai-glasses-owners-users-and-developers-in-india-product-experience
- [low] 29d old — https://www.sourcee.app/journo-request/cybersecurity-expert-ai-nexus-and-security-risks
- [low] 29d old — https://www.sourcee.app/journo-request/chatbot-users-experiences-talking-to-ai
- [low] 29d old — https://www.sourcee.app/journo-request/us-ai-security-experts-rogue-ai-agents-hitting-government-sites
- [low] 29d old — https://www.sourcee.app/journo-request/real-estate-agents-pdf-brochures-vs-alternatives-agent-workflow
- [low] 30d old — https://www.sourcee.app/journo-request/us-emergency-physicians-and-paramedics-impact-of-ai-answering-911-calls
- [low] 30d old — https://www.sourcee.app/journo-request/job-seekers-and-recruiters-ai-recruitment-experiences
- [low] 31d old — https://www.sourcee.app/journo-request/data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity
- [low] 31d old — https://www.sourcee.app/journo-request/b2b-marketing-leaders-hyperspecialization-to-outcompete-ai
- [low] 31d old — https://www.sourcee.app/journo-request/ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes
- [low] 37d old — https://www.sourcee.app/journo-request/saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup
- [low] 37d old — https://www.sourcee.app/journo-request/engineering-managers-measuring-engineers-when-using-ai
- [low] 37d old — https://www.sourcee.app/journo-request/ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai
- [low] 38d old — https://www.sourcee.app/journo-request/sales-enablement-saas-tools-proposal-and-deck-engagement-tracking
- [low] 38d old — https://www.sourcee.app/journo-request/founders-and-leaders-mindsets-and-milestones
- [low] 38d old — https://www.sourcee.app/journo-request/london-businesses-stopped-using-ai-hiring-tools
- [low] 38d old — https://www.sourcee.app/journo-request/creative-industry-professionals-podcast-on-ai-impact
- [low] 38d old — https://www.sourcee.app/journo-request/former-ai-skeptics-changed-views-on-ai-impact
- [low] 39d old — https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- [low] 39d old — https://www.sourcee.app/journo-request/employers-and-recruiters-over-50s-adapting-to-ai
- [low] 39d old — https://www.sourcee.app/journo-request/data-center-professionals-podcast-guest-ai-and-hyperscale-trends
- [low] 39d old — https://www.sourcee.app/journo-request/patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges
- [low] 39d old — https://www.sourcee.app/journo-request/ml-researchers-continuous-learning-fast-weights-and-adapters
- [low] 39d old — https://www.sourcee.app/journo-request/founders-55-latelife-entrepreneurship-series-1
- [low] 39d old — https://www.sourcee.app/journo-request/founders-and-entrepreneurs-and-musicians-podcast-guests
- [low] 40d old — https://www.sourcee.app/journo-request/ai-alignment-researchers-humanai-mutual-understanding
- [low] 41d old — https://www.sourcee.app/journo-request/companies-that-stopped-emailing-pdfs-new-tools-and-transition
- [low] 42d old — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 42d old — https://www.sourcee.app/journo-request/gen-z-ai-data-annotators-work-experience-and-income-impact
- [low] 42d old — https://www.sourcee.app/journo-request/ai-automation-experts-speakers-on-marketing-sales-operations-gains
- [low] 42d old — https://www.sourcee.app/journo-request/ecommerce-marketers-transparency-in-ai-recommendations-and-conversion
- [low] 43d old — https://www.sourcee.app/journo-request/cybersecurity-companies-and-experts-ai-scams-and-consumer-safety
- [low] 111d old — https://www.sourcee.app/journo-request/investigative-reporters-openai-training-predatory-dynamic-pricing

---

## Clearing the queue

After sending, record it so the row does not reappear:

```json
{"pitched": {"<url>": "2026-09-15"}, "skipped": {"<url>": "reason"}}
```

Ledger: `marketing/haro-outreach/pitch-ledger.json`
