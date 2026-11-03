# Pitch queue — clear this in one pass

Built 2026-11-03 from 232 unique requests across the digest history. **4 sendable**, 50 live, 175 cold (> 10 days and unpitched).

*"Sendable" is the number that matters and the one the headline used to hide: a live page is not a candidate. A row counts as sendable only when it is live, not cold, not dropped off, not already pitched, ranked above the tangential band, and has a resolved reply route (a published email, a named handle, a booking link). The other live rows are off-beat calls this queue already documents as excluded.*

**Ages are read off each request page** (`datePublished`), not off the digest text — see `marketing/haro-outreach/verified-requests.json`, refreshed by `scripts/verify_journo_requests.py`. An earlier build fell back to the digest's first-seen date and showed a 190-day-old request as 8 days old.

**No renewal signal exists on this source.** Sourcee publishes no renewal signal: on the 300 most recently indexed slugs and all 30 slugs of the live AI topic feed (checked 2026-09-19) the sitemap lastmod is byte-identical to datePublished, so 'never refreshed' is not observable and is not claimed here. Cold means old and unpitched, not provably abandoned.

**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, Qwoted and Medialyst need authenticated sessions, and Sourcee redacts the requester's own address in the request body. That is why 43 flagged opportunities produced zero pitches. Reply routes are named per row — including addresses resolved off the *publication's* own site (a byline page or an editorial contact page), which is now the strongest route class in this queue.

## Drafts that exist and were never sent

Read this before clearing the queue: 43 draft files exist on disk. **3 of the pitches drafted here have now been sent** — listed at the bottom, not as work. The rest are still unsent; a written draft is not progress — the send is.

**THE QUEUE HOLDS 4 SENDABLE ROW(S).** A row is declared sendable on two facts evidenced separately rather than trusted from a digest field: a relevance above the tangential band, and a reply route verified by fetching a page today. Both are named in the row. The previous run reported 4; the last run before it with a non-zero count was 2026-10-29, with 0 consecutive zero run(s) in between. The live unpitched set is 50 rows.

**Today's draft file is `pitch-drafts-2026-11-03.md` (derived from disk, not typed).** The headline figures are re-derived every run: 44 of 105 tools publish a monthly price, 35 of those at or under $25/month, median $16.50 (snapshots `updated: 2026-11-03`). Superseded sets still sitting in older dated drafts (40/31/$16.50 and earlier) must not be reused.

**The pair range is `1.11x to 2.53x, median 1.25x` over 19 tiers, and it held today.** History, because every superseded value is still sitting in dated draft files and must not be reused: the range was first published as `1.21x to 2.53x, median 1.33x` (2026-09-18, sent to a real correspondent — wrong because the pair population was regex-dependent and undefined); corrected to `1.16x to 2.53x, median 1.25x` over 18 curated pairs (2026-09-21); then re-derived to `1.11x to 2.53x` when the replit-ai snapshot was refreshed (2026-09-22). See `data/monthly_annual_pairs.json` and `scripts/extract_monthly_annual_pairs.py`, which refuses to write the file at all unless every curated pair re-asserts against the live snapshot.

- anthropic-users-and-business-owners-customer-service-experiences — **Crossed cold 2026-09-23; now 53d old — no longer counted as sendable.** Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal hliwrites.99 (re-read verbatim off the live page 2026-09-30). Send late or record as skipped in `pitch-ledger.json`; the crossing is logged in `cold_without_a_send`.
- employees-blocked-from-ai-on-work-accounts-automating-tedious-ta — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — in an earlier dated draft file (not named in the newest one). Now 29d old.** Route: LinkedIn DM to linkedin.com/in/christopher-mims-club/ (LinkedIn byline page — route-checks probe 2026-11-03: HTTP 200, 553,522 bytes, title 'Christopher Mims - The Wall Street Journal | LinkedIn'; the request's own body says '(DMs open)'; muckrack.com/christopher-mims 403 and wsj.com/news/author/christopher-mims 401 are dead ends, not routes — both re-checked in the same 2026-11-03 probe). It has left the sendable count: the row is now past the 10-day line and this queue no longer ranks it as actionable. The route is not dead and the draft named above is still paste-ready — George's call is to send it late or record it skipped in `pitch-ledger.json`. Silence is the one option that leaves it drifting.
- finops-professionals-agentic-ai-cost-overruns — **Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1. Now 57d old.** Route: LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 and still unsent — the longest-standing high-relevance request this monitor has never answered. Send it late or drop it, do not draft it a fifth time.
- tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — pitch-drafts-2026-10-17.md (not named in the newest file). Now 24d old, carried in 17 draft files.** Route: hello@tobiamure.com, the address the journalist publishes himself on his own site — tobiamure.com homepage — route-checks probe 2026-11-03: HTTP 200, 63,370 bytes, title 'Tobi Amure, CFEI® | Finance &amp; Technology Journalist', with the contact form on tobiamure.com/contact — route-checks probe 2026-11-03: HTTP 200, 18,505 bytes, title 'Contact Tobi Amure | Finance &amp; Technology Journalist' as the fallback if mail bounces. Deliverability is NOT SMTP-verified: the domain's MX answers 554 Relay access denied for a real address, a fake control and postmaster@ alike, so that probe discriminates nothing. He asks for 'original data, or a survey with its sample size and method' and refuses DM pitches, which is why the draft leads with the one measured series we hold. Past the 10-day line the send is still possible — a late send or a ledger entry closes it; silence leaves it drifting exactly as the WSJ row did on 2026-10-16.

### Already sent — do NOT re-send

- fulltime-employees-shadow-ai-use-and-paying-outofpocket — **SENT BUT BOUNCED — the address is dead, do not retry it; a fresh route is needed before this row can be sent at all.** `pitch-ledger.json`: 2026-10-10 (SENT BUT BOUNCED - see log)
- google-and-claude-enterprise-users-seats-and-token-costs — SENT. `pitch-ledger.json`: 2026-10-10
- speciality-food-retailers-and-producers-how-theyd-spend-10k-on-t — SENT. `pitch-ledger.json`: 2026-10-10

## Send these now (3) — a finished draft and a live route

Each row below has a finished, paste-ready pitch in `pitch-drafts-2026-11-03.md` and a page that served the request today. All 3 are inside the 10-day line. A send, or a `skipped` entry in `pitch-ledger.json`, closes each one. A rewrite of the same draft does not.

- **§2 in `pitch-drafts-2026-11-03.md`** — https://www.sourcee.app/journo-request/cios-and-cisos-steps-to-address-ai-orphans — 0d old, page live today, route `Kelsey.ziser@informationweek.com`
- **§3 in `pitch-drafts-2026-11-03.md`** — https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training — 6d old, page live today, route named in the draft
- **§1 in `pitch-drafts-2026-11-03.md`** — https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes — 7d old, page live today, route `alison@alisoncoleman.co.uk`

## Sendable — pitch these (4)

Live, not cold, ranked above the tangential band, and with a reply route a human can actually use. This is the whole actionable queue.

### [medium] AI / Enterprise Governance / Agent Sprawl
- **URL:** https://www.sourcee.app/journo-request/cios-and-cisos-steps-to-address-ai-orphans
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** Kelsey Ziser, Senior Editor at InformationWeek (page domain informationweek.com; the body signs 'InformationWeek'). Her author page https://www.informationweek.com/author/kelsey-ziser returns HTTP 200, 587,272 bytes, title 'Kelsey Ziser | Senior Editor, InformationWeek'. · domain informationweek.com
- **Reply route:** Body redacts the address ('Email: [email redacted]'). Route resolved OFF HER PUBLICATION'S OWN AUTHOR PAGE, not guessed: informationweek.com/author/kelsey-ziser HTTP 200 today, 587,272 bytes, publishing Kelsey.ziser@informationweek.com (both casings, twice in the markup) - route-checks-2026-11-03.json. HARD DEADLINE: 'Deadline for interviews is Wednesday EOD' = 2026-11-04, i.e. tomorrow. The only other link on the page is lnkd.in/eECBX7_D, a LinkedIn post about the earlier piece (login-walled, not a reply route). The request body's address is redacted by Sourcee. Links published on the page: https://lnkd.in/eECBX7_D.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: Kelsey.ziser@informationweek.com (George sends)_
- **Links published on the page:** https://lnkd.in/eECBX7_D
- **Angle:** Data-led: 44 of 105 tracked AI tools publish a monthly per-seat price, 35 of those at or under $25, median $16.50 (checked 2026-11-03) - cheap enough per seat to be bought without an owner, which is where orphans start. Signed AIToolsEssentials, under 200 words. See pitch-drafts-2026-11-03.md section 2.

### [medium] AI / Workplace Adoption / Training & Skills
- **URL:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-29, last 2026-11-03 (2x)
- **Publication:** Vidhya Das, Business Today (India Today group) - the page's own domain field is businesstoday.in and the body signs 'Business Today'; her author page businesstoday.in/author/vidhya-das returns HTTP 200 (662,049 bytes) with the title 'Trainee Sub Editor'. · domain businesstoday.in
- **Reply route:** Address redacted ('You can also email me at [email redacted]'). Published routes: comment on the LinkedIn post, or DM her - handle resolved as in.linkedin.com/in/vidya-das through search on 2026-10-29 (profile title 'Trainee Sub Editor | Business Today | India Today group'), NOT off the request page; LinkedIn answers HTTP 999 to this monitor's probe, so the handle is search-resolved rather than page-verified. Her Business Today author page publishes no email. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; LinkedIn DM route named in the row: in.linkedin.com/in/vidya-das (George sends)_
- **Angle:** Data-led: median cheapest paid tier $17.50/seat/month across the 44 of 99 tracked tools that publish a monthly price, 35 of those at or under $25 - i.e. per-seat cost is low enough that adoption outruns training. Signed AIToolsEssentials, under 200 words. See pitch-drafts-2026-10-29.md section 3.

### [medium] AI / Small Business / First-Hire Substitution
- **URL:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-28, last 2026-11-03 (3x)
- **Publication:** Alison Coleman, Forbes senior contributor (page author field 'Alison Coleman', domain forbes.com; her Forbes bio, read through search 2026-10-28, says she is a freelance journalist and founder of Coleman Media Ltd. covering entrepreneurs and their startups). · domain forbes.com
- **Reply route:** The body's address is platform-redacted ('email: [email redacted]'), and the page publishes no link or handle. ROUTE RESOLVED OFF HER OWN SITE, not guessed: https://www.alisoncoleman.co.uk/contact-me/ returns HTTP 200, 28,082 bytes, title 'Contact me : Alison Coleman', and prints in visible body text 'Email: alison@alisoncoleman.co.uk', 'Twitter: @alisonbcoleman', 'Skype: alisonbcoleman', beside a Contact Form 7 form (action /contact-me/#wpcf7-f52-p21-o1) as the fallback; her homepage https://www.alisoncoleman.co.uk/ returns HTTP 200, 21,396 bytes, title 'Alison Coleman'. Both recorded in route-checks-2026-11-03.json. alisoncoleman.co.uk MX = Google Workspace (aspmx.l.google.com first). Forbes' own byline page https://www.forbes.com/sites/alisoncoleman/ answers HTTP 403 (770 bytes) to us, so her own site is the only readable route. Email to a published address - a human send, George's lane. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: alison@alisoncoleman.co.uk (George sends)_
- **Angle:** Lead with the measured substitute cost, not a description of the site: 'Of the 99 AI tools we price, 44 publish a monthly per-seat price; 35 of those sit at or under $25, median $16.50 (checked 2026-10-28).' Then state plainly what we cannot give her (first-person testimony from a switching business) and offer the price set as background with check dates and vendor URLs on every figure. […] (full angle in the digest entry for this row)

### [medium] AI / Founders / Bootstrapping & Capital Substitution
- **URL:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-28, last 2026-11-03 (3x)
- **Publication:** Alison Coleman, Forbes (page author field; domain field is empty, and the two requests were posted seven minutes apart so they are one commissioning pass - the sibling request carries forbes.com).
- **Reply route:** Address platform-redacted ('[email redacted]'); no link or handle on the page. Same reporter as the solopreneur request above, so the route is the same one already resolved and re-probed today: alison@alisoncoleman.co.uk published in visible text on https://www.alisoncoleman.co.uk/contact-me/ (HTTP 200, 28,082 bytes, route-checks-2026-11-03.json), with the site's contact form as fallback. George's lane. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: alison@alisoncoleman.co.uk (George sends)_
- **Angle:** None of its own - covered by pitch-drafts-2026-10-28.md section 1, which names both of Alison Coleman's open requests in one email.

## Live but not sendable (46)

These pages resolve and the requests are unexpired, so they are recorded — but none has both a relevance above the tangential band and a usable route. They are listed for completeness, not as candidates: pitching any of them would mean claiming standing we do not have (see the exclusions in the newest `pitch-drafts-*.md`).

### [low] AI / Student Life / Testimony
- **URL:** https://www.sourcee.app/journo-request/carleton-students-ai-use-in-dating-advice
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** A reporter for The Charlatan, Carleton University's independent student newspaper (page domain charlatan.ca). · domain charlatan.ca
- **Reply route:** DM only ('send me a DM and we can arrange a time'); no address, handle or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Student testimony, no route. NOT DRAFTED.

### [low] PR Subcontracting / Travel Tech (not a source request)
- **URL:** https://www.sourcee.app/journo-request/aussie-travellers-1861-hotel-tech-abandoned-bookings-and-ai-concerns
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** A freelance copywriter (page author field 'sezen711') sourcing interviewees 'for a few media pitches for a leading hotel commerce platform'.
- **Reply route:** Comment or DM on the original post; no address, handle or link published. The buyer is an unnamed hotel platform, not a publication. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Vendor case-study recruitment, not a request. NOT DRAFTED.

### [low] Commissioning Call (not a source request)
- **URL:** https://www.sourcee.app/journo-request/freelance-journalists-automation-feature-pitches
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** Rachel Courtland, MIT Technology Review (page domain technologyreview.com; the body is a call from the magazine). · domain technologyreview.com
- **Reply route:** Pitch guide and print-pitch address behind https://lnkd.in/ghW8vbiT; pitches due Friday 2026-11-13. Links published on the page: https://lnkd.in/ghW8vbiT)..  ·  _no — published booking link https://lnkd.in/ghW8vbiT). (George)_
- **Links published on the page:** https://lnkd.in/ghW8vbiT).
- **Angle:** None. Commissioning call, not a source request. NOT DRAFTED.

### [low] AI Agents / Churn & Abandonment
- **URL:** https://www.sourcee.app/journo-request/former-muse-users-gave-up-on-ai-agents
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** Katie Notopoulos (page author field; no publication named anywhere in the body).
- **Reply route:** No address, handle or link on the page; the body ends 'I want to hear from you.....' with nothing to reply to. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Testimony request with no route. NOT DRAFTED.

### [low] AI / Design Systems / Live Stream
- **URL:** https://www.sourcee.app/journo-request/designers-on-large-teams-evolving-design-systems-dive-radio
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** A designer-host (page author field 'Michael Riddering' is named in the body as co-host), sourcing for the Dive Radio live stream; no publication named.
- **Reply route:** DM only ('DM me what you're actually doing and seeing for Thursday's Dive Radio'); no handle, address or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Wrong standing, no route. NOT DRAFTED.

### [low] AI / Robotics Research
- **URL:** https://www.sourcee.app/journo-request/world-model-researchers-applications-in-robotics
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** Matthew S. Smith, writing for the Association for Advancing Automation (named in the body); no domain on the page.
- **Reply route:** 'Let's connect' - no address, handle or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Research standing, no route. NOT DRAFTED.

### [low] AI / Culture / First-Person Essay
- **URL:** https://www.sourcee.app/journo-request/young-adults-1835-ai-impact-on-comingofage
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** A Reddit user (page author field 'coolskeleton96_'), self-described writer, no publication named.
- **Reply route:** Reply on the originating thread; no address, handle or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Testimony request, no route. NOT DRAFTED.

### [low] AI / Recruitment Industry / Billing
- **URL:** https://www.sourcee.app/journo-request/uk-recruiters-ai-impact-on-billing-and-candidate-matching
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** Lindsay Dodgson, CNBC (page domain cnbc.com; the body signs '#journorequest #journorequests CNBC'). · domain cnbc.com
- **Reply route:** Address redacted in the body ('Get in touch if that's you [email redacted]'); the page publishes no other address, handle or link. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No UK recruiter standing and no route. NOT DRAFTED.

### [low] Networking / Web Summit (not a source request)
- **URL:** https://www.sourcee.app/journo-request/global-and-european-marketing-leaders-investment-and-ops-challenges
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** An unnamed attendee (no author field, no publication), posting a Web Summit Lisbon meeting list.
- **Reply route:** No route published: it is a list of people the poster wants to meet at a conference. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Not a request. NOT DRAFTED.

### [low] AI / Mental Health / Sensitive Testimony
- **URL:** https://www.sourcee.app/journo-request/people-with-ai-psychosis-firsthand-accounts
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** An anonymous Reddit account (page author field 'helloiamareporter'), self-described reporter, no publication named.
- **Reply route:** DMs only ('please reach out to me in the DMs'); no handle, address or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Sensitive testimony, no route. NOT DRAFTED.

### [low] Startups / Marketing Spend
- **URL:** https://www.sourcee.app/journo-request/startup-founders-deciding-first-marketing-tests-on-tight-runway
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** MarketBrain OS (page author field); no publication named, and the account reads as a vendor's content operation rather than a newsroom.
- **Reply route:** No route published: the post asks founders to 'tell us how you're deciding' and provides no address, handle or link. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Off-beat and route-less. NOT DRAFTED.

### [low] AI / Copyright / Academic
- **URL:** https://www.sourcee.app/journo-request/new-authors-ai-market-dilution-and-fair-use-impact-on-writing
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** Sarosha (named in the body), a law student writing a note for her school's law review; page author field 'Matcha_Vintage10'.
- **Reply route:** DM only through the originating thread; no address or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Academic research request, no route. NOT DRAFTED.

### [low] AI / Property Management Adoption
- **URL:** https://www.sourcee.app/journo-request/multifamily-professionals-ai-adoption-and-employee-chatbot-use
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** Daniel Paulino (page author field); no publication named - the audience is the multifamily property industry.
- **Reply route:** DM only ('please message me privately'); no address, handle or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Wrong standing, no route. NOT DRAFTED.

### [low] AI Agents / Creator Workflows
- **URL:** https://www.sourcee.app/journo-request/marketers-and-creators-using-ai-agents-timesaving-wins
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** A Reddit user (page author field 'Fun_Grapefruit7182'), collecting stories for 'a podcast I'm working on at my company'; no publication named.
- **Reply route:** Reply to the originating post only ('If you're interested, let me know and I'll send you a DM request'); no handle, address or link beyond the thread. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Podcast guest call on a Reddit thread, no route. NOT DRAFTED.

### [low] AI / Policy / Canada
- **URL:** https://www.sourcee.app/journo-request/canadian-ai-and-tech-companies-government-picking-winners-and-losers
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** Terry Newman (page author field); no publication named.
- **Reply route:** 'My DMs are open' - but no handle, address or link is published, so there is nothing to open. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Off-beat, no route. NOT DRAFTED.

### [low] AI / Student Media / Ad Fraud
- **URL:** https://www.sourcee.app/journo-request/ut-austin-students-ai-trump-crypto-ads-on-game-livestreams
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** A Daily Texan reporter (page domain dailytexanonline.com). · domain dailytexanonline.com
- **Reply route:** Reply on the originating thread; no address, handle or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Student testimony, no route. NOT DRAFTED.

### [low] AI / Consumer Finance Tools / Testimony
- **URL:** https://www.sourcee.app/journo-request/bank-and-brokerage-users-ai-tools-managing-personal-finances
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** genna, writing for MarketWatch (page domain marketwatch.com; the body says 'for a @MarketWatch story'). · domain marketwatch.com
- **Reply route:** Address redacted ('Email me at [email redacted]'); nothing else published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Consumer testimony, no route. NOT DRAFTED.

### [low] AI-Adjacent / Personal Career Testimony
- **URL:** https://www.sourcee.app/journo-request/midlife-professionals-career-regret
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** Suzanne Reilley, sourcing for Business Insider (page domain businessinsider.com; the body says 'Would you like to be featured in Business Insider?'). · domain businessinsider.com
- **Reply route:** The body publishes an UNREDACTED address in plain text: 'suzanne [dot] reilley @ gmail [dot] com' - the only request in this window that states a usable address itself. It asks for 'a concise 1-2 paragraph pitch with specific details about your story'. The page publishes no address, handle or link of its own.  ·  _no — email resolved off the publication's own site (George sends)_
- **Angle:** None. Personal testimony we do not have. NOT DRAFTED.

### [low] Consumer / Property / DIY Sale (not AI)
- **URL:** https://www.sourcee.app/journo-request/buyers-and-sellers-without-agents-diy-property-sale-experience
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-29, last 2026-11-03 (2x)
- **Publication:** Anna (page author field 'Anna_the_journo'), a producer on the SBS TV show 'Insight' (sbs.com.au, named in the body). · domain sbs.com.au
- **Reply route:** Platform reply only: the body says 'Feel free to comment or DM' on the Reddit thread Sourcee ingested; the handle in the author field is the only identifier. No address, no link. The page publishes no address, handle or link of its own.  ·  _no — platform reply (George)_
- **Angle:** None. Off-beat and route-less. NOT DRAFTED.

### [low] Media / Creative Work / Unpaid Documentary Recruitment
- **URL:** https://www.sourcee.app/journo-request/editors-creatives-and-graphic-designers-ai-impact-documentary
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-29, last 2026-11-03 (2x)
- **Publication:** An unnamed studio (page author field 'your_pro_Designer'); no publication, no masthead, no company named in the body.
- **Reply route:** Comment on the originating post only - the page publishes no address, handle or link, and the body asks people to 'show us your day, a clip of you telling us about your story'. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Unpaid crew call, wrong side of the camera, no route. NOT DRAFTED.

### [low] AI / Oil & Gas / HSE Computer Vision
- **URL:** https://www.sourcee.app/journo-request/rig-hse-staff-aienabled-cameras-trial-outcomes
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-29, last 2026-11-03 (2x)
- **Publication:** Roxana Shirkhorshidi (page author field); no publication named.
- **Reply route:** Comment on the post or send a message: 'Share your thoughts in the comments - or, if you'd prefer to talk, send me a message'. No address or handle published. The page publishes no address, handle or link of its own.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. Right shape, wrong standing, no route. NOT DRAFTED.

### [low] AI / Higher Education / Campus Research
- **URL:** https://www.sourcee.app/journo-request/current-ucla-students-and-faculty-ai-impact-on-majors
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** Thoun Thant Nandi with Max Benedetti, working with Prof. Daniel Schwalbe-Koda at UCLA; no publication named.
- **Reply route:** 'Comment "Coffee" below or send me a DM'; explicitly 'Open to current UCLA students and faculty only'. No address or link. The page publishes no address, handle or link of its own.  ·  _no — platform reply (George)_
- **Angle:** None. Explicitly campus-only, no route. NOT DRAFTED.

### [low] Future of Work / Guest Booking (not a source request)
- **URL:** https://www.sourcee.app/journo-request/founders-and-inclusion-leads-future-of-work-and-ai-impact
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** Sheryl Miller (page author field), booking guests for her LinkedIn Live 'Friday Morning Live' diary for 2027.
- **Reply route:** 'Please tag them in the comments' - a comment route on the original post; no address or handle published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Guest booking, not a request. NOT DRAFTED.

### [low] AI / Law / Podcast
- **URL:** https://www.sourcee.app/journo-request/uk-law-experts-and-ai-safety-researchers-chatbotaided-crime
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-03, last 2026-11-03 (1x)
- **Publication:** Deborah Boyle, a Social Change Initiative journalism fellow (named in the body); no publication.
- **Reply route:** No address, handle or link published; the body asks to 'speak with any law experts and AI safety researchers in the UK'. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Wrong standing, no route. NOT DRAFTED.

### [low] AI / Consumer Finance / Linked Accounts Testimony
- **URL:** https://www.sourcee.app/journo-request/users-who-linked-bank-and-brokerage-accounts-to-llms-ai-finance
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-28, last 2026-11-03 (3x)
- **Publication:** Genna Contino, MarketWatch (page author field; domain marketwatch.com). · domain marketwatch.com
- **Reply route:** The body's address is platform-redacted ('Email me at [email redacted]'). The page publishes no link, handle or form. No route resolved this run; marketwatch.com was not probed for a byline address because the ask is not one we can answer. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Consumer testimony only; address redacted; no route. NOT DRAFTED.

### [low] AI / Creative Work / Testimony
- **URL:** https://www.sourcee.app/journo-request/musicians-artists-writers-and-creators-ai-impact-on-creativity
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-28, last 2026-11-03 (3x)
- **Publication:** Chloe Bishop (page author field). No publication on the page - the domain field is empty, and the body says 'for a feature I am pitching'.
- **Reply route:** The page publishes no address, handle, link or form at all. A platform reply on Sourcee itself, which is not a route we hold credentials for. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Opinion testimony; no publication; no route. NOT DRAFTED.

### [low] Publishing / Literary Magazines / Body-level AI hit only
- **URL:** https://www.sourcee.app/journo-request/literary-writers-thoughts-on-lit-mags-funny-deep-frustrated
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-28, last 2026-11-03 (3x)
- **Publication:** Becky Tuch (page author field), writing for her Thursday column at Lit Mag News.
- **Reply route:** No address, link, handle or form published on the page. Platform reply only. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. The AI token is a joke in the copy; no ask, no route. NOT DRAFTED.

### [low] AI / Personal Finance / Existential-Risk Testimony
- **URL:** https://www.sourcee.app/journo-request/ai-researchers-founders-and-tech-ceos-retirement-plans-amid-ai-risk
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-29, last 2026-11-03 (2x)
- **Publication:** Thibault Spirlet, tech reporter in Business Insider's London office (domain field businessinsider.com; the body is signed as a Business Insider call for sources). · domain businessinsider.com
- **Reply route:** Address redacted in the body ('email me at [email redacted] before Friday'). The same reporter's byline route is already resolved and re-probed today: businessinsider.com/author/thibault-spirlet (HTTP 200, 328,800 bytes, tspirlet@businessinsider.com published in a mailto link) - route-checks-2026-11-03.json. The request body's address is redacted by Sourcee. Links published on the page: https://lnkd.in/e5E_f8RM.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: tspirlet@businessinsider.com (George sends)_
- **Links published on the page:** https://lnkd.in/e5E_f8RM
- **Angle:** None. Requires holding an existential-risk position we do not hold. NOT DRAFTED - but the reporter is live, see the Business Insider row.

### [low] AI / Manufacturing / Skilled Trades
- **URL:** https://www.sourcee.app/journo-request/canadian-skilled-trades-workers-ai-impact-on-manufacturing
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-29, last 2026-11-03 (2x)
- **Publication:** Andrea Wahbe (page author field); no publication named anywhere in the body.
- **Reply route:** DM only: 'Please DM me if interested.' No address, no link, no handle published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No publication, no route, wrong standing. NOT DRAFTED.

### [low] AI / Consumer Chatbots / First-Person Testimony
- **URL:** https://www.sourcee.app/journo-request/character-ai-users-emotional-attachment-and-loneliness
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-29, last 2026-11-03 (2x)
- **Publication:** A Reddit user (page author field 'Melodic-Phrase-3303'), self-described journalist, no publication named.
- **Reply route:** Reply on the originating thread; no address or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Testimony request, no route. NOT DRAFTED.

### [low] AI / Founder Feature Promotion (not a request)
- **URL:** https://www.sourcee.app/journo-request/gcc-founders-and-entrepreneurs-ai-collaboration-and-data-sovereignty
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-29, last 2026-11-03 (2x)
- **Publication:** Ornella Nett (page author field); the body is a promotional write-up of a feature on Lenks.ai and Rawan Almogbil, with a LinkedIn link (lnkd.in/dD9PhQZj).
- **Reply route:** DM the author on LinkedIn; the only link on the page is the article itself. Links published on the page: https://lnkd.in/dD9PhQZj.  ·  _no — published booking link https://lnkd.in/dD9PhQZj (George)_
- **Links published on the page:** https://lnkd.in/dD9PhQZj
- **Angle:** None. Not a request. NOT DRAFTED.

### [low] AI / Agritech / Dairy Livestock
- **URL:** https://www.sourcee.app/journo-request/dairy-companies-and-startups-aipowered-livestock-health-and-nutrition
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-29, last 2026-11-03 (2x)
- **Publication:** Ankit Saproo (page author field); no publication named.
- **Reply route:** Reach out via the post - the body says 'Kindly reach out'; no address, link or handle published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Off-beat and route-less. NOT DRAFTED.

### [low] AI / Privacy Governance / NOT A REQUEST (founder milestone post)
- **URL:** https://www.sourcee.app/journo-request/excorporate-privacy-lead-built-privacy-and-ai-consultancy
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-11-03 (4x)
- **Publication:** Aakash Suri (the page's author field). No publication on the page - the domain field is empty.
- **Reply route:** The page publishes no address, handle, link or form. The body is a first-person anniversary post about leaving corporate employment, not a call for sources. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Not a request - no ask and no route. NOT DRAFTED.

### [low] Hospitality / Video Sourcing (body-level AI hit, slug has no AI token)
- **URL:** https://www.sourcee.app/journo-request/members-club-and-hospitality-pros-in-hong-kong-postcovid-trends
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-11-03 (4x)
- **Publication:** Reddit-style handle 'Hihellohi' (the page's author field). No publication named.
- **Reply route:** No address, link or handle published. The body asks for on-camera or voice-note interviews; platform reply only. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Wants on-camera hospitality testimony; no route. NOT DRAFTED.

### [low] Healthcare / Book Contribution Call (body-level AI hit)
- **URL:** https://www.sourcee.app/journo-request/canadian-health-innovators-voices-of-innovation-canada-nov-16
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-11-03 (4x)
- **Publication:** Glenn Lanteigne (author field). A book series ('Voices of Innovation', Canadian edition), no publication domain.
- **Reply route:** No address, link or handle published on the page; the call is to participate in a book, with a stated deadline of 2026-11-16. Links published on the page: https://lnkd.in/g2f3pGmu, https://lnkd.in/g8ugVuWR.  ·  _no — published booking link https://lnkd.in/g2f3pGmu (George)_
- **Links published on the page:** https://lnkd.in/g2f3pGmu, https://lnkd.in/g8ugVuWR
- **Angle:** None. Book contribution call for clinicians; no route. NOT DRAFTED.

### [low] AI / B2B Marketing / Startup Branding
- **URL:** https://www.sourcee.app/journo-request/ai-startup-founders-and-marketers-b2b-marketing-as-show-business
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-28, last 2026-11-03 (3x)
- **Publication:** Shalaka Kulkarni, LiveMint (page author field and body '@livemint'; domain livemint.com). · domain livemint.com
- **Reply route:** No address, handle, link or form is published on the page; the body names the publication and nothing else. No route resolved. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Marketing-practice testimony; no route. NOT DRAFTED.

### [low] AI / Companion Chatbots / Personal Testimony (podcast sourcing)
- **URL:** https://www.sourcee.app/journo-request/people-using-llms-as-companions-emotional-support-stories
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-26, last 2026-11-03 (5x)
- **Publication:** Rose Guingrich, PhD (the page's author field). The body names the two people actually collecting: Kim Shirin Cupal, a journalist and audio producer, working with Hilke Schellmann on a mini-podcast series for Jennifer Strong's SHIFT podcast, funded by the Pulitzer Center. No publication domain on the page.
- **Reply route:** The body publishes two live channels and redacts the third: Reddit u/KimCupal and Discord kimcupal are printed verbatim in the request body, while the email is platform-redacted ('Email: [email redacted]'). The page itself publishes no link, and the raw payload carries no address. ROUTE CLASS THAT IS NEW FOR THIS MONITOR: a named Reddit handle read straight off the request body - usable without any signup, unlike the LinkedIn DMs which need George's session. NOT VERIFIED: no page was fetched to confirm the handle exists or is still active; a Reddit profile probe was not run this pass, so treat the handle as published-but-unconfirmed. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. The ask is first-person experience and we would have to invent it. NOT DRAFTED.

### [low] AI / Higher Education / Student Testimony
- **URL:** https://www.sourcee.app/journo-request/students-whose-professors-allow-ai-ai-use-in-coursework
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-11-03 (4x)
- **Publication:** Reddit handle 'LegitimateOil90' (the page's author field). Says they are a journalism student. No publication named.
- **Reply route:** The page publishes no address, handle beyond the author field, or link. The body asks respondents to 'send me a message or comment' - a platform reply on Sourcee itself, which is not a route we hold credentials for. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Wants student testimony; no route. NOT DRAFTED.

### [low] AI / Higher Education Admissions / Judgment Assessment
- **URL:** https://www.sourcee.app/journo-request/admissions-leaders-and-researchers-measuring-judgment-amid-ai
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-11-03 (4x)
- **Publication:** Dr. Aviva Legatt, contributing to Forbes (the page's domain field is forbes.com). · domain forbes.com
- **Reply route:** The body says 'please reply to me directly' and the page publishes no address, handle or link. Platform reply only; no route resolved. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Wants admissions leaders and assessment researchers; no route. NOT DRAFTED.

### [low] AI / Consumer Behaviour / Student Testimony
- **URL:** https://www.sourcee.app/journo-request/carleton-students-ai-dating-advice-impact-on-dating-experience
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-11-03 (4x)
- **Publication:** Reddit handle 'Individual_Hawk_5754' (author field), a reporter for The Charlatan, Carleton University's independent newspaper (domain field charlatan.ca). · domain charlatan.ca
- **Reply route:** No address, handle or link published. The body asks for a DM: 'send me a DM and we can arrange a time'. Platform reply only. The page publishes no address, handle or link of its own.  ·  _no — platform reply (George)_
- **Angle:** None. Student testimony only; no route. NOT DRAFTED.

### [low] Personal Finance / Celebrity Agents / Interview Series
- **URL:** https://www.sourcee.app/journo-request/celebrity-agents-how-i-manage-my-money-series
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-11-03 (4x)
- **Publication:** Emily Braeger, The i Paper (the page's author field and domain theipaper.com). · domain theipaper.com
- **Reply route:** The body's address is platform-redacted ('Please email me at [email redacted]'). The page publishes no link or handle. No route resolved; the i Paper's own contact page was not probed for a byline address this run. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Wants celebrity agents; address redacted; no route. NOT DRAFTED.

### [low] AI / Careers / Software Engineers Turned Traders
- **URL:** https://www.sourcee.app/journo-request/former-software-engineers-turned-traders-pivot-after-layoff-or-ai
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-11-03 (4x)
- **Publication:** Thibault Spirlet, tech reporter, Business Insider London (page author field 'Thibault_SpirletBI', domain businessinsider.com). THE SAME REPORTER as this queue's one sendable row. · domain businessinsider.com
- **Reply route:** The body's address is platform-redacted ('please email me at [email redacted]'), but this reporter's address is already resolved off his own byline page and RE-PROBED TODAY: businessinsider.com/author/thibault-spirlet HTTP 200, 326,570 bytes, tspirlet@businessinsider.com published in a mailto link and 5 times in the markup (route-checks-2026-11-03.json). Automatable? No - George's lane. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: tspirlet@businessinsider.com (George sends)_
- **Angle:** None for this row's ask (wants trader testimony we do not have). Its byline route is reused by the Mistral draft, pitch-drafts-2026-10-27.md section 1.

### [low] AI / Blue-Collar AI Adoption / Utilities & Construction
- **URL:** https://www.sourcee.app/journo-request/ai-companies-in-utilities-and-construction-frontline-safety-and-workload
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-27, last 2026-11-03 (4x)
- **Publication:** Lindsay Dodgson, CNBC (page author field, domain cnbc.com). · domain cnbc.com
- **Reply route:** The body's address is platform-redacted. No link, handle or form published; no route resolved. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Wants AI vendors; address redacted; no route. NOT DRAFTED.

### [low] Arts / Open Call (false positive - not AI)
- **URL:** https://www.sourcee.app/journo-request/sound-artists-and-field-recordists-run-radio-aarhus-open-call
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-26, last 2026-11-03 (5x)
- **Publication:** Run_Radio (author field) - RUN RADIO, a music radio station and sound archive in Aarhus, Denmark, run with the Institute for X.
- **Reply route:** Email is platform-redacted ([email redacted]) and the page publishes no link or handle. The body asks for a downloadable transfer link by email. NOT RESOLVED and not worth resolving: the call is for field recordings, DJ mixes and sound art. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Not an AI request and no route. NOT DRAFTED.

### [low] AI / Consumer Behaviour / Social Connection
- **URL:** https://www.sourcee.app/journo-request/people-using-ai-for-social-advice-communication-and-connection-impact
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-25, last 2026-11-03 (6x)
- **Publication:** Trisha Mahajan, for TOI Digital (The Times of India) - the outlet is named in the body ('I'm working on a story for TOI DIGITAL', closing line 'The Times of India') and the author field carries her name; the page's domain field is indiatimes.com. · domain indiatimes.com
- **Reply route:** The body says 'Please reply to this post, DM me or email me ([email redacted])'. Sourcee redacts the address, the page publishes no link or handle of hers, and no address appears anywhere on the page. NOT RESOLVED. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Video Production / Agentic Tooling
- **URL:** https://www.sourcee.app/journo-request/video-teams-using-claude-and-remotion-agentic-video-editing
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-25, last 2026-11-03 (6x)
- **Publication:** Enrico Tartarotti (page author field). No outlet, no domain: the domain field is empty and the body names no publication - this is an individual sourcing for his own project.
- **Reply route:** The body publishes one link, a t.co shortener (https://t.co/4ZzXXpfAC4) with the instruction '(please add a few lines about who you are)'. The page publishes no address and no personal handle; the destination behind the shortener was not resolved, so the route is the post itself. NOT RESOLVED. Links published on the page: https://t.co/4ZzXXpfAC4.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/4ZzXXpfAC4
- **Angle:** None. No route and no standing. NOT DRAFTED.

## Cold — only if you have a reason

Older than the 10-day line and never pitched. Not provably abandoned — no renewal signal exists on this source — but every one of these has already passed an ideal send window.

- [high] 57d old — https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
- [high] 59d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-ai-governance-and-agent-sprawl
- [high] 60d old — https://www.sourcee.app/journo-request/scientists-phd-students-and-postdocs-paying-for-ai-subscriptions
- [high] 105d old — https://www.sourcee.app/journo-request/business-and-technology-leaders-tech-budget-priorities-amid-volatility
- [high] 165d old — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [high] 185d old — https://www.sourcee.app/journo-request/anthropic-api-users-costs-and-token-burn-increase-since-january
- [medium-high] 53d old — https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
- [medium-high] 57d old — https://www.sourcee.app/journo-request/uk-managers-cracked-down-on-gen-z-ai-overuse
- [medium-high] 231d old — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium] 11d old — https://www.sourcee.app/journo-request/employees-at-european-orgs-switch-from-us-ai-provider-to-mistral
- [medium] 29d old — https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
- [medium] 53d old — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [medium] 57d old — https://www.sourcee.app/journo-request/ai-agents-making-money-2026-sales-and-leadgen-workflow-ops
- [medium] 57d old — https://www.sourcee.app/journo-request/ai-startups-workplace-fraud-detection-expenses-time-theft
- [medium] 57d old — https://www.sourcee.app/journo-request/marketing-and-content-leaders-aiassisted-work-review-process
- [medium] 61d old — https://www.sourcee.app/journo-request/ceos-ai-impact-on-ops-culture-and-commercial-strategy
- [medium] 71d old — https://www.sourcee.app/journo-request/uk-finance-risk-and-regulatory-leaders-ai-explainability-risks
- [medium] 238d old — https://www.sourcee.app/journo-request/sme-owners-operational-challenges-for-ai-solutions-case-study
- [low-medium] 11d old — https://www.sourcee.app/journo-request/claude-users-anthropic-public-benefit-fund-trust-and-job-impact
- [low-medium] 21d old — https://www.sourcee.app/journo-request/b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research
- [low-medium] 24d old — https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
- [low-medium] 28d old — https://www.sourcee.app/journo-request/uk-companies-implementing-ai-how-automation-transforms-workdays
- [low-medium] 32d old — https://www.sourcee.app/journo-request/law-firm-lawyers-concrete-ai-implementations-and-billing-impact
- [low-medium] 34d old — https://www.sourcee.app/journo-request/employees-conflicted-about-ai-use-generative-ai-workplace-impact
- [low-medium] 35d old — https://www.sourcee.app/journo-request/insurance-agents-ai-use-in-personal-lines
- [medium-low] 45d old — https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business
- [low-medium] 48d old — https://www.sourcee.app/journo-request/us-founders-calls-to-slow-ai-development-impact-on-companies
- [medium-low] 54d old — https://www.sourcee.app/journo-request/tech-policy-experts-california-ai-audit-bills-impact-cios
- [low-medium] 73d old — https://www.sourcee.app/journo-request/ai-project-builders-youtube-finance-and-lifestyle-channel-feature
- [low-medium] 118d old — https://www.sourcee.app/journo-request/prompt-engineers-tokenmaxxing-anecdotes
- [low] 11d old — https://www.sourcee.app/journo-request/fanvue-chatters-nsfw-ai-model-experiences
- [low] 11d old — https://www.sourcee.app/journo-request/couples-letting-ai-dictate-relationship-emotions-and-intimacy
- [low] 11d old — https://www.sourcee.app/journo-request/people-recreating-iconic-runway-looks-halloween-costume-story
- [low] 11d old — https://www.sourcee.app/journo-request/parish-event-organizers-aigenerated-flyers-scourge-or-timesaver
- [low] 11d old — https://www.sourcee.app/journo-request/uk-and-eu-sports-retail-supply-chain-leaders-retail-ai-at-scale
- [low] 11d old — https://www.sourcee.app/journo-request/founders-and-cofounders-fortnightly-founder-qanda
- [low] 12d old — https://www.sourcee.app/journo-request/nontech-inhouse-corporate-comms-lead-ai-search-and-discovery-strategy
- [low] 12d old — https://www.sourcee.app/journo-request/anthropic-project-panama-employees-book-digitization-and-ai-training
- [low] 12d old — https://www.sourcee.app/journo-request/geopolitical-analysts-and-ai-security-experts-global-hotspots
- [low] 12d old — https://www.sourcee.app/journo-request/digital-artists-aigenerated-posters-flooding-social-feeds
- [low] 12d old — https://www.sourcee.app/journo-request/founders-and-ctos-production-ai-tradeoffs-in-healthcare-and-fintech
- [low] 12d old — https://www.sourcee.app/journo-request/students-and-professionals-balancing-ai-use-and-human-focus
- [low] 12d old — https://www.sourcee.app/journo-request/rig-hse-officers-aienabled-camera-trial-outcomes
- [low] 13d old — https://www.sourcee.app/journo-request/brand-managers-ai-to-deepen-customer-insight-and-preserve-humanity
- [low] 13d old — https://www.sourcee.app/journo-request/omaha-hr-representatives-offices-with-written-ai-policies
- [low] 13d old — https://www.sourcee.app/journo-request/nj-parents-and-teachers-ai-school-surveillance-and-data-practices
- [low] 13d old — https://www.sourcee.app/journo-request/bengaluru-founders-deep-tech-healthcare-biology-housing-and-ai
- [low] 13d old — https://www.sourcee.app/journo-request/fintech-product-managers-nextgen-aipowered-personal-finance-apps
- [low] 14d old — https://www.sourcee.app/journo-request/carleton-students-ai-impact-on-dating-experiences
- [low] 14d old — https://www.sourcee.app/journo-request/hr-leaders-and-organizational-design-practitioners-decision-fatigue
- [low] 14d old — https://www.sourcee.app/journo-request/cios-at-gartner-it-symposium-orlando-balancing-ai-risk-and-value
- [low] 14d old — https://www.sourcee.app/journo-request/estate-agents-and-property-lawyers-disclosure-rules-haunted-homes
- [low] 14d old — https://www.sourcee.app/journo-request/product-managers-on-512-engineer-teams-engineers-using-ai
- [low] 14d old — https://www.sourcee.app/journo-request/bay-area-agentic-ai-builders-agntcon-and-mcpcon-stories
- [low] 15d old — https://www.sourcee.app/journo-request/fb-marketplace-sellers-and-buyers-ai-impact-on-pricing-and-listings
- [low] 15d old — https://www.sourcee.app/journo-request/new-yorkers-ai-music-playing-in-cabs-and-local-businesses
- [low] 15d old — https://www.sourcee.app/journo-request/western-students-using-ai-companions-psychological-effects
- [low] 15d old — https://www.sourcee.app/journo-request/consumers-using-ai-for-financial-advice-experience-and-factchecking
- [low] 15d old — https://www.sourcee.app/journo-request/ai-energy-and-tax-experts-project-jupiter-documentary-new-mexico
- [low] 16d old — https://www.sourcee.app/journo-request/uk-customer-service-workers-daytoday-now-ai-automation-vs-human
- [low] 17d old — https://www.sourcee.app/journo-request/ai-saas-vendors-targeting-journalists-prs-and-marketers-case-studies
- [low] 17d old — https://www.sourcee.app/journo-request/real-estate-operators-ai-adoption-and-org-restructuring
- [low] 17d old — https://www.sourcee.app/journo-request/memphis-and-southaven-residents-and-env-advocates-xai-colossus-impact
- [low] 17d old — https://www.sourcee.app/journo-request/black-women-in-canada-ai-chatbots-and-healthcare-experiences
- [low] 17d old — https://www.sourcee.app/journo-request/engineering-leaders-leading-people-through-ai-changes
- [low] 18d old — https://www.sourcee.app/journo-request/chemistry-undergrads-and-phd-students-ai-use-in-coursework-and-research
- [low] 18d old — https://www.sourcee.app/journo-request/ai-app-and-saas-founders-1k-mrr-youtube-feature-growth-tactics
- [low] 18d old — https://www.sourcee.app/journo-request/ai-infrastructure-engineers-in-berlin-data-centers-and-bottlenecks
- [low] 18d old — https://www.sourcee.app/journo-request/residents-near-mumbai-ai-data-centres-power-and-water-strain
- [low] 18d old — https://www.sourcee.app/journo-request/single-family-office-cybersecurity-experts-ai-risks-and-opportunities
- [low] 19d old — https://www.sourcee.app/journo-request/painters-and-photographers-ai-impact-on-art
- [low] 19d old — https://www.sourcee.app/journo-request/legal-assistants-paralegals-and-lawfirm-staff-jobs-eliminated-by-ai
- [low] 19d old — https://www.sourcee.app/journo-request/cios-and-ai-leaders-ai-infrastructure-day2-ops-and-costs
- [low] 19d old — https://www.sourcee.app/journo-request/companies-and-data-buyers-selling-corporate-data-to-train-ai
- [low] 19d old — https://www.sourcee.app/journo-request/uk-political-analysts-disinformation-and-ai-manipulation-in-politics
- [low] 19d old — https://www.sourcee.app/journo-request/content-creators-using-ai-job-losses-and-ethics
- [low] 20d old — https://www.sourcee.app/journo-request/school-leaders-and-ngo-staff-ai-adoption-challenges-across-sectors
- [low] 20d old — https://www.sourcee.app/journo-request/minnesotans-using-chatgpt-and-ai-tools-experiences-with-election-info
- [low] 20d old — https://www.sourcee.app/journo-request/ai-policy-advisor-newsom-administration-ai-regulation
- [low] 20d old — https://www.sourcee.app/journo-request/uk-and-us-heads-of-data-and-ai-from-idea-to-production
- [low] 20d old — https://www.sourcee.app/journo-request/ai-companion-users-in-africa-friendship-and-emotional-impact
- [low] 20d old — https://www.sourcee.app/journo-request/pro-se-litigants-using-generative-ai-access-to-justice-impact
- [low] 21d old — https://www.sourcee.app/journo-request/global-development-professionals-using-ai-across-programs-and-policy
- [low] 21d old — https://www.sourcee.app/journo-request/african-founders-building-ai-companies-pitch-deck-realities
- [low] 21d old — https://www.sourcee.app/journo-request/higher-ed-nonfaculty-staff-ai-use-at-work
- [low] 21d old — https://www.sourcee.app/journo-request/podcast-guests-ai-channel-and-partner-ecosystem
- [low] 21d old — https://www.sourcee.app/journo-request/ai-infrastructure-professionals-in-london-capacity-europe-attendees
- [low] 21d old — https://www.sourcee.app/journo-request/b2b-vendors-buyers-pasting-proposals-into-ai-tools
- [low] 22d old — https://www.sourcee.app/journo-request/caine-prize-winners-gen-ai-accusations-targeting-black-writers
- [low] 22d old — https://www.sourcee.app/journo-request/software-engineers-who-left-tech-jobs-lost-to-ai-coding-tools
- [low] 22d old — https://www.sourcee.app/journo-request/manufacturers-and-ai-safety-experts-ai-risks-in-chemical-food-defense
- [low] 22d old — https://www.sourcee.app/journo-request/uk-baby-boomers-misinformation-sharing-and-ai-influence-online
- [low] 23d old — https://www.sourcee.app/journo-request/hedera-builders-shipping-defi-nfts-rwas-ai-games-and-memes
- [low] 23d old — https://www.sourcee.app/journo-request/production-designers-ai-impact-on-future-of-filmmaking
- [low] 23d old — https://www.sourcee.app/journo-request/ai-researchers-and-policy-experts-5-years-us-race-to-superintelligence
- [low] 24d old — https://www.sourcee.app/journo-request/ai-cybersecurity-iot-and-web3-founders-and-operators-news-submissions
- [low] 24d old — https://www.sourcee.app/journo-request/employees-pay-transparency-good-or-bad
- [low] 25d old — https://www.sourcee.app/journo-request/sales-reps-who-cold-call-and-email-how-ai-changed-outreach
- [low] 25d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-and-builders-realworld-deployment-and-strategy
- [low] 25d old — https://www.sourcee.app/journo-request/anthropic-gtm-leaders-scaling-300k-b2b-clients
- [low] 26d old — https://www.sourcee.app/journo-request/patent-attorneys-and-agents-startup-ip-starter-pack
- [low] 26d old — https://www.sourcee.app/journo-request/voters-who-used-ai-to-navigate-ballot-voting-experience
- [low] 26d old — https://www.sourcee.app/journo-request/hotel-and-fandb-supervisors-and-managers-customer-expectations-vs-ai
- [low] 26d old — https://www.sourcee.app/journo-request/researchers-founders-and-funders-ai-transforming-scientific-research
- [low] 26d old — https://www.sourcee.app/journo-request/facebook-marketplace-sellers-ai-listing-photos-and-selling-experience
- [low] 27d old — https://www.sourcee.app/journo-request/aps-hr-leaders-ai-skills-training-and-workforce-planning
- [low] 27d old — https://www.sourcee.app/journo-request/scrum-masters-daytoday-and-career-pivots-and-ai-impact
- [low] 27d old — https://www.sourcee.app/journo-request/real-estate-agents-replacing-pdf-property-brochure
- [low] 27d old — https://www.sourcee.app/journo-request/anz-marketers-ai-and-martech-innovation-spotlight
- [low] 27d old — https://www.sourcee.app/journo-request/solicitors-and-barristers-ai-to-expand-pro-bono-capacity
- [low] 27d old — https://www.sourcee.app/journo-request/uk-ai-data-trainers-daytoday-work
- [low] 27d old — https://www.sourcee.app/journo-request/apac-reporters-and-editors-ai-accountability-coverage
- [low] 27d old — https://www.sourcee.app/journo-request/early-to-midcareer-information-architects-products-featuring-ai
- [low] 27d old — https://www.sourcee.app/journo-request/martech-buyers-ai-impact-on-build-vs-buy-decisions
- [low] 28d old — https://www.sourcee.app/journo-request/ai-infrastructure-experts-china-vs-us-datacenter-capacity
- [low] 28d old — https://www.sourcee.app/journo-request/plaintiffs-attorneys-and-legal-scholars-ai-deepfake-liability
- [low] 28d old — https://www.sourcee.app/journo-request/emergency-managers-ai-tools-for-funding-and-staffing-shortfalls
- [low] 28d old — https://www.sourcee.app/journo-request/coweta-county-artists-and-creatives-data-centers-and-ai-infrastructure
- [low] 28d old — https://www.sourcee.app/journo-request/swiss-ai-companion-users-emotional-bonds-and-daily-life
- [low] 28d old — https://www.sourcee.app/journo-request/ai-data-labelers-in-germany-positive-and-negative-experiences
- [low] 28d old — https://www.sourcee.app/journo-request/ai-data-annotators-and-labellers-experience-with-ai-training-data
- [low] 28d old — https://www.sourcee.app/journo-request/ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories
- [low] 28d old — https://www.sourcee.app/journo-request/academics-social-media-and-ai-impact-on-womens-identity-and-selfesteem
- [low] 29d old — https://www.sourcee.app/journo-request/ai-liability-insurers-and-legal-experts-procurement-and-implementation
- [low] 29d old — https://www.sourcee.app/journo-request/uk-cybersecurity-hiring-managers-state-of-hiring-2026-and-ai-impact
- [low] 29d old — https://www.sourcee.app/journo-request/ai-emotional-support-users-chatbot-therapy-and-journaling
- [low] 29d old — https://www.sourcee.app/journo-request/mortgage-adviser-using-ai-efficiency-and-client-outcomes-video-series
- [low] 29d old — https://www.sourcee.app/journo-request/founders-and-cxos-in-automotive-ai-evs-autonomy-thought-leadership
- [low] 30d old — https://www.sourcee.app/journo-request/video-game-developer-falsely-accused-of-using-generative-ai
- [low] 31d old — https://www.sourcee.app/journo-request/lawyers-and-tech-ethics-experts-ai-wearables-and-legal-journeys
- [low] 32d old — https://www.sourcee.app/journo-request/storytellers-and-brand-founders-marys-big-30-ai-story-project
- [low] 32d old — https://www.sourcee.app/journo-request/newsletter-editors-using-ai-agents-news-aggregation-practices
- [low] 32d old — https://www.sourcee.app/journo-request/scottish-teachers-ai-tools-implementation-in-education
- [low] 32d old — https://www.sourcee.app/journo-request/mls-executives-risks-when-agents-grant-mls-access-to-llms
- [low] 32d old — https://www.sourcee.app/journo-request/real-estate-agents-and-brokers-switched-from-pdf-brochures
- [low] 32d old — https://www.sourcee.app/journo-request/advertising-tech-and-media-pros-in-miami-ai-audience-discovery
- [low] 32d old — https://www.sourcee.app/journo-request/hr-leaders-company-ai-strategies-and-cognitive-offloading-risk
- [low] 33d old — https://www.sourcee.app/journo-request/fea-engineers-using-agentic-ai-practitioner-case-study
- [low] 33d old — https://www.sourcee.app/journo-request/parents-ai-acting-as-pseudoparent-in-kid-questions
- [low] 33d old — https://www.sourcee.app/journo-request/fb-marketplace-sellers-ai-photos-and-description-prompts
- [low] 33d old — https://www.sourcee.app/journo-request/k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact
- [low] 33d old — https://www.sourcee.app/journo-request/ai-summit-barcelona-attendees-controversy-and-experiences
- [low] 33d old — https://www.sourcee.app/journo-request/ai-glasses-owners-users-and-developers-in-india-product-experience
- [low] 34d old — https://www.sourcee.app/journo-request/chatbot-users-experiences-talking-to-ai
- [low] 34d old — https://www.sourcee.app/journo-request/us-ai-security-experts-rogue-ai-agents-hitting-government-sites
- [low] 34d old — https://www.sourcee.app/journo-request/real-estate-agents-pdf-brochures-vs-alternatives-agent-workflow
- [low] 35d old — https://www.sourcee.app/journo-request/cybersecurity-expert-ai-nexus-and-security-risks
- [low] 35d old — https://www.sourcee.app/journo-request/us-emergency-physicians-and-paramedics-impact-of-ai-answering-911-calls
- [low] 35d old — https://www.sourcee.app/journo-request/job-seekers-and-recruiters-ai-recruitment-experiences
- [low] 36d old — https://www.sourcee.app/journo-request/data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity
- [low] 36d old — https://www.sourcee.app/journo-request/b2b-marketing-leaders-hyperspecialization-to-outcompete-ai
- [low] 36d old — https://www.sourcee.app/journo-request/ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes
- [low] 42d old — https://www.sourcee.app/journo-request/saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup
- [low] 42d old — https://www.sourcee.app/journo-request/ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai
- [low] 43d old — https://www.sourcee.app/journo-request/sales-enablement-saas-tools-proposal-and-deck-engagement-tracking
- [low] 43d old — https://www.sourcee.app/journo-request/london-businesses-stopped-using-ai-hiring-tools
- [low] 43d old — https://www.sourcee.app/journo-request/engineering-managers-measuring-engineers-when-using-ai
- [low] 43d old — https://www.sourcee.app/journo-request/creative-industry-professionals-podcast-on-ai-impact
- [low] 43d old — https://www.sourcee.app/journo-request/former-ai-skeptics-changed-views-on-ai-impact
- [low] 44d old — https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- [low] 44d old — https://www.sourcee.app/journo-request/employers-and-recruiters-over-50s-adapting-to-ai
- [low] 44d old — https://www.sourcee.app/journo-request/data-center-professionals-podcast-guest-ai-and-hyperscale-trends
- [low] 44d old — https://www.sourcee.app/journo-request/patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges
- [low] 44d old — https://www.sourcee.app/journo-request/founders-and-leaders-mindsets-and-milestones
- [low] 44d old — https://www.sourcee.app/journo-request/ml-researchers-continuous-learning-fast-weights-and-adapters
- [low] 44d old — https://www.sourcee.app/journo-request/founders-55-latelife-entrepreneurship-series-1
- [low] 44d old — https://www.sourcee.app/journo-request/founders-and-entrepreneurs-and-musicians-podcast-guests
- [low] 45d old — https://www.sourcee.app/journo-request/ai-alignment-researchers-humanai-mutual-understanding
- [low] 46d old — https://www.sourcee.app/journo-request/companies-that-stopped-emailing-pdfs-new-tools-and-transition
- [low] 47d old — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 47d old — https://www.sourcee.app/journo-request/gen-z-ai-data-annotators-work-experience-and-income-impact
- [low] 47d old — https://www.sourcee.app/journo-request/ecommerce-marketers-transparency-in-ai-recommendations-and-conversion
- [low] 48d old — https://www.sourcee.app/journo-request/cybersecurity-companies-and-experts-ai-scams-and-consumer-safety
- [low] 48d old — https://www.sourcee.app/journo-request/ai-automation-experts-speakers-on-marketing-sales-operations-gains
- [low] 116d old — https://www.sourcee.app/journo-request/investigative-reporters-openai-training-predatory-dynamic-pricing

---

## Clearing the queue

After sending, record it so the row does not reappear:

```json
{"pitched": {"<url>": "2026-09-15"}, "skipped": {"<url>": "reason"}}
```

Ledger: `marketing/haro-outreach/pitch-ledger.json`
