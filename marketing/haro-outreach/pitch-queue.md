# Pitch queue — clear this in one pass

Built 2026-10-23 from 179 unique requests across the digest history. **0 sendable**, 58 live, 114 cold (> 10 days and unpitched).

*"Sendable" is the number that matters and the one the headline used to hide: a live page is not a candidate. A row counts as sendable only when it is live, not cold, not dropped off, not already pitched, ranked above the tangential band, and has a resolved reply route (a published email, a named handle, a booking link). The other live rows are off-beat calls this queue already documents as excluded.*

**Ages are read off each request page** (`datePublished`), not off the digest text — see `marketing/haro-outreach/verified-requests.json`, refreshed by `scripts/verify_journo_requests.py`. An earlier build fell back to the digest's first-seen date and showed a 190-day-old request as 8 days old.

**No renewal signal exists on this source.** Sourcee publishes no renewal signal: on the 300 most recently indexed slugs and all 30 slugs of the live AI topic feed (checked 2026-09-19) the sitemap lastmod is byte-identical to datePublished, so 'never refreshed' is not observable and is not claimed here. Cold means old and unpitched, not provably abandoned.

**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, Qwoted and Medialyst need authenticated sessions, and Sourcee redacts the requester's own address in the request body. That is why 43 flagged opportunities produced zero pitches. Reply routes are named per row — including addresses resolved off the *publication's* own site (a byline page or an editorial contact page), which is now the strongest route class in this queue.

## Drafts that exist and were never sent

Read this before clearing the queue: 36 draft files exist on disk. **3 of the pitches drafted here have now been sent** — listed at the bottom, not as work. The rest are still unsent; a written draft is not progress — the send is.

**THE QUEUE IS AT ZERO SENDABLE, AND TODAY THAT IS THE TRUE NUMBER RATHER THAN A CODE ARTEFACT.** Repeated builds have each had to be corrected for the same defect class — a field that records something adjacent to a reply route being read as one. On 2026-09-29 the refresh script had dropped Sourcee's two own social links from its chrome filter, so a page's own chrome landed in one row's `published_links`. On 2026-10-01 the first build read the employees-conflicted-about-AI-use row as sendable because its body embeds a docs.google.com casting form, which `_sendable()` accepted as a link route. Both are fixed: a `published_links` entry now counts as a route only when it is a booking/contact link. Today the live unpitched set is 58 rows (measured at build time from the merged digests, not typed), and none has both a relevance above the tangential band and a usable route.

**Today's draft file is `pitch-drafts-2026-10-23.md` (derived from disk, not typed).** The headline figures are re-derived every run: 44 of 91 tools publish a monthly price, 35 of those at or under $25/month, median $17.50 (snapshots `updated: 2026-10-23`). Superseded sets still sitting in older dated drafts (40/31/$16.50 and earlier) must not be reused.

**The pair range is `1.11x to 2.53x, median 1.25x` over 19 tiers, and it held today.** History, because every superseded value is still sitting in dated draft files and must not be reused: the range was first published as `1.21x to 2.53x, median 1.33x` (2026-09-18, sent to a real correspondent — wrong because the pair population was regex-dependent and undefined); corrected to `1.16x to 2.53x, median 1.25x` over 18 curated pairs (2026-09-21); then re-derived to `1.11x to 2.53x` when the replit-ai snapshot was refreshed (2026-09-22). See `data/monthly_annual_pairs.json` and `scripts/extract_monthly_annual_pairs.py`, which refuses to write the file at all unless every curated pair re-asserts against the live snapshot.

- anthropic-users-and-business-owners-customer-service-experiences — **Crossed cold 2026-09-23; now 41d old — no longer counted as sendable.** Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal hliwrites.99 (re-read verbatim off the live page 2026-09-30). Send late or record as skipped in `pitch-ledger.json`; the crossing is logged in `cold_without_a_send`.
- employees-blocked-from-ai-on-work-accounts-automating-tedious-ta — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — §2 in `pitch-drafts-2026-10-23.md`. Now 18d old.** Route: LinkedIn DM to linkedin.com/in/christopher-mims-club/ (LinkedIn byline page — route-checks probe 2026-10-22: HTTP 200, 623,445 bytes, title 'Christopher Mims - The Wall Street Journal | LinkedIn'; the request's own body says '(DMs open)'; muckrack.com/christopher-mims 403 and wsj.com/news/author/christopher-mims 401 are dead ends, not routes — both re-checked in the same 2026-10-22 probe). It has left the sendable count: the row is now past the 10-day line and this queue no longer ranks it as actionable. The route is not dead and the draft named above is still paste-ready — George's call is to send it late or record it skipped in `pitch-ledger.json`. Silence is the one option that leaves it drifting.
- finops-professionals-agentic-ai-cost-overruns — **Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1. Now 46d old.** Route: LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 and still unsent — the longest-standing high-relevance request this monitor has never answered. Send it late or drop it, do not draft it a fifth time.
- tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — §1 in `pitch-drafts-2026-10-23.md`. Now 13d old, carried in 11 draft files.** Route: hello@tobiamure.com, the address the journalist publishes himself on his own site — tobiamure.com homepage — route-checks probe 2026-10-22: HTTP 200, 62,628 bytes, title 'Tobi Amure, CFEI® | Finance &amp; Technology Journalist', with the contact form on tobiamure.com/contact — route-checks probe 2026-10-22: HTTP 200, 17,762 bytes, title 'Contact Tobi Amure | Finance &amp; Technology Journalist' as the fallback if mail bounces. Deliverability is NOT SMTP-verified: the domain's MX answers 554 Relay access denied for a real address, a fake control and postmaster@ alike, so that probe discriminates nothing. He asks for 'original data, or a survey with its sample size and method' and refuses DM pitches, which is why the draft leads with the one measured series we hold. Past the 10-day line the send is still possible — a late send or a ledger entry closes it; silence leaves it drifting exactly as the WSJ row did on 2026-10-16.

### Already sent — do NOT re-send

- fulltime-employees-shadow-ai-use-and-paying-outofpocket — **SENT BUT BOUNCED — the address is dead, do not retry it; a fresh route is needed before this row can be sent at all.** `pitch-ledger.json`: 2026-10-10 (SENT BUT BOUNCED - see log)
- google-and-claude-enterprise-users-seats-and-token-costs — SENT. `pitch-ledger.json`: 2026-10-10
- speciality-food-retailers-and-producers-how-theyd-spend-10k-on-t — SENT. `pitch-ledger.json`: 2026-10-10

## Send these now (2) — late, not dead

Each row below has a finished, paste-ready pitch in `pitch-drafts-2026-10-23.md` and a page that served the request today. They sit past the 10-day line, which is this monitor's own heuristic and not the platform's: no page on this source has ever carried an expiry. A send, or a `skipped` entry in `pitch-ledger.json`, closes each one. A fourth rewrite of the same draft does not.

- **§2 in `pitch-drafts-2026-10-23.md`** — https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks — 18d old, page live today, route `https://www.linkedin.com/in/christopher-mims-club`
- **§1 in `pitch-drafts-2026-10-23.md`** — https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring — 13d old, page live today, route `hello@tobiamure.com`

## Sendable — pitch these (0)

Live, not cold, ranked above the tangential band, and with a reply route a human can actually use. This is the whole actionable queue.

**There is nothing to send from this queue today.** Every row that had both a relevance above the tangential band and a resolved route has now crossed the 10-day line unpitched; the live rows below are off-beat calls with no usable route. The rows that carried a finished draft are named in the section above as crossed-but-still-sendable — a late send is the only action left on them.

## Live but not sendable (58)

These pages resolve and the requests are unexpired, so they are recorded — but none has both a relevance above the tangential band and a usable route. They are listed for completeness, not as candidates: pitching any of them would mean claiming standing we do not have (see the exclusions in the newest `pitch-drafts-*.md`).

### [low-medium] AI / Anthropic Governance / Value Distribution (adjacent)
- **URL:** https://www.sourcee.app/journo-request/claude-users-anthropic-public-benefit-fund-trust-and-job-impact
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-23, last 2026-10-23 (1x)
- **Publication:** Ryan Moeller (the page's own author field). No outlet named; the body reads as a LinkedIn community post.
- **Reply route:** No route of any kind: the body names no channel, the page publishes no address or booking link, and it is not even an email-wall request. The two social URLs that appear in the raw payload are Sourcee's own footer chrome rather than the poster's profile - both were found on three unrelated request pages today (boston-soccer-parents, couples-letting-ai, rig-hse-officers), which is why they sit in the shared CHROME filter. They are NOT a route to this journalist, and are deliberately not written out here because a bare handle string in this field is what has twice made a route-less row read as sendable. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, and the ask is opinion, not data. NOT DRAFTED.

### [low-medium] AI / B2B Buying Process / Vendor Research
- **URL:** https://www.sourcee.app/journo-request/b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-13, last 2026-10-23 (11x)
- **Publication:** Lyza G (the page's own author field). No outlet named on the request.
- **Reply route:** The body says 'Email [email redacted]' — Sourcee redacts the address, and the page publishes no handle and no link (published_links = Sourcee's own author chrome only, which the verifier excludes). NOT RESOLVED as a route.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing.

### [low] AI / NSFW Creator Economy / Platform Labour
- **URL:** https://www.sourcee.app/journo-request/fanvue-chatters-nsfw-ai-model-experiences
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-23, last 2026-10-23 (1x)
- **Publication:** Dazed magazine (domain field dazeddigital.com); the page's author field is the handle 'Dazedjourno', so no individual byline. · domain dazeddigital.com
- **Reply route:** The body says 'please DM me'; no address, handle or link is published on the page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route published, and no standing to claim. NOT DRAFTED.

### [low] AI / Consumer Behaviour / Relationships (tabloid)
- **URL:** https://www.sourcee.app/journo-request/couples-letting-ai-dictate-relationship-emotions-and-intimacy
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-23, last 2026-10-23 (1x)
- **Publication:** Luke Chafer, The Sun (domain field thesun.co.uk; the body signs 'The Sun'). · domain thesun.co.uk
- **Reply route:** The body says 'I am available here or at [email redacted]' - Sourcee redacts the address and the page publishes no other handle or link. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route, and the ask is first-person experience we cannot supply. NOT DRAFTED.

### [low] Fashion / Halloween (NOT AI - false positive)
- **URL:** https://www.sourcee.app/journo-request/people-recreating-iconic-runway-looks-halloween-costume-story
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-23, last 2026-10-23 (1x)
- **Publication:** Alexandra Hildreth (the page's own author field). No outlet named.
- **Reply route:** The body asks 'Would love to chat for a story' and publishes no address, handle or link. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Not an AI request at all. NOT DRAFTED.

### [low] AI / Faith Communities / Design Tools
- **URL:** https://www.sourcee.app/journo-request/parish-event-organizers-aigenerated-flyers-scourge-or-timesaver
- **Posted:** 0d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-23, last 2026-10-23 (1x)
- **Publication:** Zoey Maraist (the page's own author field). No outlet named; the body says 'an article I'm writing'.
- **Reply route:** The page publishes no address, handle or link, and the body names no channel at all. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Search & Discovery / Corporate Communications
- **URL:** https://www.sourcee.app/journo-request/nontech-inhouse-corporate-comms-lead-ai-search-and-discovery-strategy
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-23 (2x)
- **Publication:** Andrew Birmingham (the page's own author field). No outlet named in the body; he describes the request as 'for a project I'm running' and addresses it to 'my PR and Comms mates'.
- **Reply route:** The body says only 'If that sounds like you drop me a line' — no address, handle or link to the poster. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, and no standing to claim. NOT DRAFTED.

### [low] AI / Training Data / Labour (broadcast)
- **URL:** https://www.sourcee.app/journo-request/anthropic-project-panama-employees-book-digitization-and-ai-training
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-23 (2x)
- **Publication:** TF1, the French TV network (domain field tf1.fr; the body signs 'TF1'). Reporter not named on the page. · domain tf1.fr
- **Reply route:** The body says 'Feel free to comment below or reach out to me directly' — the page publishes no address and no handle. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, and the ask is insider testimony we do not hold. NOT DRAFTED.

### [low] Geopolitics / AI security (adjacent)
- **URL:** https://www.sourcee.app/journo-request/geopolitical-analysts-and-ai-security-experts-global-hotspots
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-23 (2x)
- **Publication:** Abdurakhmonov NormuhammadAli, sourcing for the Geosiyosat project (no outlet site named).
- **Reply route:** The body asks readers to 'let me know' or name someone who might be interested; no address, handle or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Off-beat and route-less. NOT DRAFTED.

### [low] AI / Workplace Policy / HR
- **URL:** https://www.sourcee.app/journo-request/omaha-hr-representatives-offices-with-written-ai-policies
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-23 (2x)
- **Publication:** Tim Trudell (the page's own author field). Outlet not named in the body; the request is local to the Omaha area.
- **Reply route:** The body says 'please DM me or have them message me' — no address, handle or link to the poster is printed. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Standing impossible (Omaha HR representative). NOT DRAFTED.

### [low] AI / Creative Work / Social Platforms
- **URL:** https://www.sourcee.app/journo-request/digital-artists-aigenerated-posters-flooding-social-feeds
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-23 (2x)
- **Publication:** Chloe O'Keeffe (the page's own author field). No outlet named; the body carries '#mediarequest #journorequests'.
- **Reply route:** The body closes 'DMs open' — no address, handle or link to the poster is printed, and the page publishes no route of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, no standing. NOT DRAFTED.

### [low] AI / Podcast Guest Call / Healthcare & Fintech
- **URL:** https://www.sourcee.app/journo-request/founders-and-ctos-production-ai-tradeoffs-in-healthcare-and-fintech
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-23, last 2026-10-23 (1x)
- **Publication:** Bryan Dennstedt, 'AI with Bry' podcast (domain field bry.net). · domain bry.net
- **Reply route:** The page publishes no address, handle or link; the body says 'I'd love to hear from you' with no channel named. Sourcee redacted the address in the body. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route, and we are not the guest profile. NOT DRAFTED.

### [low] AI / Human Focus / Interview Call
- **URL:** https://www.sourcee.app/journo-request/students-and-professionals-balancing-ai-use-and-human-focus
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-23, last 2026-10-23 (1x)
- **Publication:** KimberMarie Faircloth, The Limitation Game (no domain field set; the body signs the project name).
- **Reply route:** The body says 'Comment below or DM me - please!'; no address, handle or link published on the page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, and the ask is personal testimony. NOT DRAFTED.

### [low] AI / Industrial HSE / Computer Vision
- **URL:** https://www.sourcee.app/journo-request/rig-hse-officers-aienabled-camera-trial-outcomes
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-23, last 2026-10-23 (1x)
- **Publication:** Roxana Shirkhorshidi (the page's own author field). No outlet named.
- **Reply route:** The body says 'Share your thoughts in the comments - or, if you'd prefer to talk, send me a message'; no address, handle or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Marketing / Customer Insight
- **URL:** https://www.sourcee.app/journo-request/brand-managers-ai-to-deepen-customer-insight-and-preserve-humanity
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-21, last 2026-10-23 (3x)
- **Publication:** Daniel Burstein, for MarketingSherpa - the handle and the publication are both named in the body ('Looking for examples from your experience for @MarketingSherpa article'). The page's author field carries his name and domain marketingsherpa.com. · domain marketingsherpa.com
- **Reply route:** The body asks for 'examples from your experience' and publishes one link, a t.co to a previous MarketingSherpa article he wrote as a model of what he publishes. No address, no handle of his own, no scheduling link. NOT RESOLVED. Links published on the page: https://t.co/8JPO9sSjJy.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/8JPO9sSjJy
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Education Surveillance / Data Practices
- **URL:** https://www.sourcee.app/journo-request/nj-parents-and-teachers-ai-school-surveillance-and-data-practices
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-23 (2x)
- **Publication:** Nicole Rosenthal, investigative reporter at NJ.com (named in the page's author field; the body signs 'NJ.com'). · domain nj.com
- **Reply route:** The body says 'DM me or email [email redacted]' — Sourcee redacts the address. No handle and no link to the reporter is published on the request page. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Standing impossible (NJ parent/teacher) and the address is redacted. NOT DRAFTED.

### [low] Podcast booking / Bengaluru founders
- **URL:** https://www.sourcee.app/journo-request/bengaluru-founders-deep-tech-healthcare-biology-housing-and-ai
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-23 (2x)
- **Publication:** Sikandar (page author field), booking guests for the @dostcast podcast.
- **Reply route:** The body says 'Let me know please' — no address, handle or link published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Off-beat, no route. NOT DRAFTED.

### [low] AI / Fintech / Sponsored feature (likely paid placement)
- **URL:** https://www.sourcee.app/journo-request/fintech-product-managers-nextgen-aipowered-personal-finance-apps
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-22, last 2026-10-23 (2x)
- **Publication:** Paul Dus Navis (the page's own author field). Outlet not named; the body is a single line advertising an 'editorial feature'.
- **Reply route:** The only published route is a LinkedIn short link, https://lnkd.in/gh2gpgwg, which is the feature's own advert link — not a route to a journalist sourcing sources. Links published on the page: https://lnkd.in/gh2gPgwg.  ·  _no — published booking link https://lnkd.in/gh2gPgwg (George)_
- **Links published on the page:** https://lnkd.in/gh2gPgwg
- **Angle:** None. Paid-placement advert, not a source request. DO NOT PITCH.

### [low] AI / Student Life / Dating
- **URL:** https://www.sourcee.app/journo-request/carleton-students-ai-impact-on-dating-experiences
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-20, last 2026-10-23 (4x)
- **Publication:** The Charlatan (charlatan.ca), Carleton University's student paper - named in the body's closing line. The page's author field is a Reddit-style handle, 'Individual_Hawk_5754', with no byline name. · domain charlatan.ca
- **Reply route:** The body's only ask is 'send me a DM and we can arrange a time'. No address, handle or link of the poster's own is published; the page's two links belong to the Sourcee account that republished it. The page publishes no address, handle or link of its own.  ·  _no — platform reply (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Music / Local Business
- **URL:** https://www.sourcee.app/journo-request/new-yorkers-ai-music-playing-in-cabs-and-local-businesses
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-20, last 2026-10-23 (4x)
- **Publication:** WNYC / Gothamist - both named in the body. The page's author field is the handle 'catgone8'; no byline name is published. · domain gothamist.com
- **Reply route:** The body says 'DM me if interested!'. No address, handle or scheduling link of the reporter's own is published on the page. The page publishes no address, handle or link of its own.  ·  _no — platform reply (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / HR / Organisational Decision-Making
- **URL:** https://www.sourcee.app/journo-request/hr-leaders-and-organizational-design-practitioners-decision-fatigue
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-20, last 2026-10-23 (4x)
- **Publication:** Molly Woudenberg, for McLean & Company - a HR research and advisory firm running its own research study, not a newsroom. The body names the team and the firm.
- **Reply route:** The body says 'Comment below or send me a direct message' and offers 'a 30-45 minute virtual research interview'. No address, scheduling link or handle is published. NOT RESOLVED. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Vendor research call, no route, no standing. NOT DRAFTED.

### [low] AI / Enterprise IT / Conference Reporting
- **URL:** https://www.sourcee.app/journo-request/cios-at-gartner-it-symposium-orlando-balancing-ai-risk-and-value
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-21, last 2026-10-23 (3x)
- **Publication:** Paige Gross - the page's author field. No outlet is named in the body or the domain field; she is reporting from the Gartner IT Symposium/Xpo in Orlando this week.
- **Reply route:** The body says 'If you're at the conference and want to connect, drop me a line!' and publishes an lnkd.in short link. No address or personal handle is published; the route is a LinkedIn connection through a short link that cannot be resolved without following it. NOT RESOLVED. Links published on the page: https://lnkd.in/gQ9HXqrU.  ·  _no — published booking link https://lnkd.in/gQ9HXqrU (George)_
- **Links published on the page:** https://lnkd.in/gQ9HXqrU
- **Angle:** None. Standing requires being at the conference. NOT DRAFTED.

### [low] Property / Consumer Law / Disclosure
- **URL:** https://www.sourcee.app/journo-request/estate-agents-and-property-lawyers-disclosure-rules-haunted-homes
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-21, last 2026-10-23 (3x)
- **Publication:** Natasha Christou - the page's author field. No publication is named in the body or the domain field.
- **Reply route:** The body reads 'Please get in touch with me via DM or email at: [email redacted]' - the address is redacted by Sourcee and no handle or link of hers is published. The two links on the page belong to the Sourcee account that republished the request. NOT RESOLVED. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route, no standing, and the AI token is a slug false positive. NOT DRAFTED.

### [low] AI / Product Management / Team Practice
- **URL:** https://www.sourcee.app/journo-request/product-managers-on-512-engineer-teams-engineers-using-ai
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-21, last 2026-10-23 (3x)
- **Publication:** Steve Tauber - the page's author field. No publication, domain or outlet is named anywhere in the body.
- **Reply route:** The body's whole ask is 'Please get in touch!' with no address, handle, link or platform named; the page publishes nothing of the poster's own. NOT RESOLVED. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Podcast / Developer Ecosystem
- **URL:** https://www.sourcee.app/journo-request/bay-area-agentic-ai-builders-agntcon-and-mcpcon-stories
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-21, last 2026-10-23 (3x)
- **Publication:** Luca Berton, whose podcast Udienza (udienza.com, named in the body and in the page's domain field) is a media partner of AGNTCon + MCPCon North America in San Jose, 22-23 October. · domain udienza.com
- **Reply route:** The body says 'If you are in the Bay Area, message me: I want to hear your story' and publishes https://www.udienza.com/. No address or personal handle; the link is the podcast's own site, not a route to the poster. NOT RESOLVED. Links published on the page: https://www.udienza.com/.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://www.udienza.com/
- **Angle:** None. Conference-standing podcast booking with no route. NOT DRAFTED.

### [low] AI / Consumer Marketplace / Resale Pricing
- **URL:** https://www.sourcee.app/journo-request/fb-marketplace-sellers-and-buyers-ai-impact-on-pricing-and-listings
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-19, last 2026-10-23 (5x)
- **Publication:** No author field resolvable off the page, and no outlet named: the body opens 'A fun reporting request' and closes 'Hoping to chat with people for a story and can protect privacy!' The only self-identifying line is 'Half the stuff in my home came from Marketplace. I love it; that's why I'm so curious about this.'
- **Reply route:** The body ends '[email redacted] or message me!' - the address is redacted by Sourcee and no handle is published. The page carries no address, link or reply instruction of its own. NOT RESOLVED. The route would be a DM on the poster's own platform. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Workplace Automation / Customer Service
- **URL:** https://www.sourcee.app/journo-request/uk-customer-service-workers-daytoday-now-ai-automation-vs-human
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-19, last 2026-10-23 (5x)
- **Publication:** No author field on the page. Domain field: cnbc.com, and the body is headed 'For CNBC' with the hashtags #journorequest #journorequests and the outlet name 'CNBC' as its last line. · domain cnbc.com
- **Reply route:** The body reads 'Email: [email redacted]' - redacted by Sourcee - and the only other instruction is the edit line 'Only looking for UK-based sources at this time!'. The page carries no address, handle or link of its own. NOT RESOLVED. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Student Project / AI Companions
- **URL:** https://www.sourcee.app/journo-request/western-students-using-ai-companions-psychological-effects
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-20, last 2026-10-23 (4x)
- **Publication:** No outlet at all: the poster ('Toad') is a student in English 110 at Western building a class podcast, and asks for interviews with Western students. The page's domain field is empty.
- **Reply route:** The body says 'Please DM me or comment below'. Nothing is published to reply to off-platform. The page publishes no address, handle or link of its own.  ·  _no — platform reply (George)_
- **Angle:** None. A class project with no publication, no route and no standing. NOT DRAFTED.

### [low] AI / Consumer Finance / Advice
- **URL:** https://www.sourcee.app/journo-request/consumers-using-ai-for-financial-advice-experience-and-factchecking
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-20, last 2026-10-23 (4x)
- **Publication:** Emily Braeger, for The i Paper - the outlet is named in the body and the author field carries her name. · domain theipaper.com
- **Reply route:** The body reads 'Please email me at [email redacted] if this is you or you can help' - the address is redacted by Sourcee, and the page publishes no link or handle of hers. NOT RESOLVED. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Data Centre Infrastructure / Energy & Tax Policy
- **URL:** https://www.sourcee.app/journo-request/ai-energy-and-tax-experts-project-jupiter-documentary-new-mexico
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-20, last 2026-10-23 (4x)
- **Publication:** Amelia K., sourcing experts for a documentary film on Project Jupiter in New Mexico. No outlet is named; the body offers an lnkd.in short link and interviewing starts mid-November.
- **Reply route:** The body says 'Please reach out if you would like to be interviewed' and publishes an lnkd.in short link plus the Sourcee account's links. No address and no personal handle; the route would be a LinkedIn message through the short link, which cannot be resolved without following it. Links published on the page: https://lnkd.in/g4-_xKt3.  ·  _no — published booking link https://lnkd.in/g4-_xKt3 (George)_
- **Links published on the page:** https://lnkd.in/g4-_xKt3
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / SaaS / Vendor Case Studies
- **URL:** https://www.sourcee.app/journo-request/ai-saas-vendors-targeting-journalists-prs-and-marketers-case-studies
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-17, last 2026-10-23 (7x)
- **Publication:** Vartika (the page's own author field). No outlet named on the request or in the body; the body is tagged #JournoRequest.
- **Reply route:** The body ends 'Pitch me :)' and publishes no address, handle or link of its own. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED. The route would in any case be a reply on the poster's own platform.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Real Estate / Operations
- **URL:** https://www.sourcee.app/journo-request/real-estate-operators-ai-adoption-and-org-restructuring
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-17, last 2026-10-23 (7x)
- **Publication:** Jake (the page's own author field). No outlet named on the request or in the body.
- **Reply route:** The body says 'DMs are open!!!' and publishes no address, handle or link. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED. The route would be a DM on the poster's own platform - not automatable and not a route this monitor can use.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Data-Centre Infrastructure / Local Impact
- **URL:** https://www.sourcee.app/journo-request/memphis-and-southaven-residents-and-env-advocates-xai-colossus-impact
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-18, last 2026-10-23 (6x)
- **Publication:** Augustina Boateng (the page's own author field). Domain field: scalawagmag.org - a piece for Scalawag. · domain scalawagmag.org
- **Reply route:** The body says 'DMs are open' and publishes no address, handle or link of its own. The only links on the page are Sourcee's own author chrome, which the verifier excludes. NOT RESOLVED. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Health / Consumer Chatbot Use
- **URL:** https://www.sourcee.app/journo-request/black-women-in-canada-ai-chatbots-and-healthcare-experiences
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-18, last 2026-10-23 (6x)
- **Publication:** Maryam Parkar (the page's own author field). No outlet named on the request or in the body; the body is tagged as a STORY CALLOUT.
- **Reply route:** The body ends 'Please DM me' and publishes no address, handle or link of its own. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED. The route would be a DM on the poster's own platform. The page publishes no address, handle or link of its own.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Engineering Management / Workplace
- **URL:** https://www.sourcee.app/journo-request/engineering-leaders-leading-people-through-ai-changes
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-18, last 2026-10-23 (6x)
- **Publication:** Gabe Dunlop (the page's own author field). No outlet named on the request or in the body.
- **Reply route:** The body ends 'Who should I talk to?' and publishes no address, handle or link. The only links on the page are Sourcee's own author chrome, which the verifier excludes. NOT RESOLVED. The route would be a reply or referral on the poster's own platform. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Higher Education / Chemistry
- **URL:** https://www.sourcee.app/journo-request/chemistry-undergrads-and-phd-students-ai-use-in-coursework-and-research
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-17, last 2026-10-23 (7x)
- **Publication:** Mason Wakley (the page's own author field). Domain field: chemistryworld.com - a story for Chemistry World. · domain chemistryworld.com
- **Reply route:** The body says 'please feel free to get in touch' and publishes no address, handle or link of its own. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED. The route would be a reply on the poster's own platform.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / SaaS Founders / Podcast Promotion
- **URL:** https://www.sourcee.app/journo-request/ai-app-and-saas-founders-1k-mrr-youtube-feature-growth-tactics
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-17, last 2026-10-23 (7x)
- **Publication:** Ayush Gupta (the page's own author field). No outlet named; the body describes his own YouTube channel.
- **Reply route:** The body says 'You can reach out to me with your website and trustmrr link' and publishes no address, handle or link. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED. The route would be a reply on the poster's own platform.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Data Centres / Infrastructure
- **URL:** https://www.sourcee.app/journo-request/ai-infrastructure-engineers-in-berlin-data-centers-and-bottlenecks
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-17, last 2026-10-23 (7x)
- **Publication:** Kai Nicol-Schwarz (the page's own author field). No outlet named on the request or in the body; the author field matches a reporter who covers AI infrastructure.
- **Reply route:** The body says 'Drop me a line if you're around' and publishes no address, handle or link. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED. The route would be arranged in person at Nvidia's GTC, which is not a route this monitor can use.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Data Centres / Infrastructure & Policy
- **URL:** https://www.sourcee.app/journo-request/residents-near-mumbai-ai-data-centres-power-and-water-strain
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-17, last 2026-10-23 (7x)
- **Publication:** Kapil Saini (the page's own author field). Domain field: businessworld.in - BusinessWorld. · domain businessworld.in
- **Reply route:** The body says 'please feel free to DM me. Email: [email redacted]' - Sourcee redacts the address, and the page publishes no handle and no link. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED. The route would be a DM on the poster's own platform.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Cybersecurity / Family Offices
- **URL:** https://www.sourcee.app/journo-request/single-family-office-cybersecurity-experts-ai-risks-and-opportunities
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-17, last 2026-10-23 (7x)
- **Publication:** Naama Saar (the page's own author field). No outlet named on the request or in the body; the body names the piece 'INFORMED NOT INVOLVED'.
- **Reply route:** The body says 'please DM me' and publishes no address, handle or link. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED. The route would be a DM on the poster's own platform.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Visual Art / Feature Story
- **URL:** https://www.sourcee.app/journo-request/painters-and-photographers-ai-impact-on-art
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-15, last 2026-10-23 (9x)
- **Publication:** Reddit throwaway-style handle Beautiful_Annual9811 (the page's own author field). No outlet and no journalist named on the request or in the body.
- **Reply route:** The body says 'Any recommendations please let me know, I'd be happy to reach out' - it asks the reader to volunteer other people, and publishes no address, handle or link of its own. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Legal Sector / Job Displacement
- **URL:** https://www.sourcee.app/journo-request/legal-assistants-paralegals-and-lawfirm-staff-jobs-eliminated-by-ai
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-15, last 2026-10-23 (9x)
- **Publication:** Reddit-style throwaway handle YardOptimal9329 (the page's own author field). The body says 'I'm a journalist looking to speak with...' but names no outlet and no byline.
- **Reply route:** The body says 'please DM me' - a route on the poster's own platform, with no handle, address or link printed on the request. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Enterprise Infrastructure / Day-2 Ops & Costs
- **URL:** https://www.sourcee.app/journo-request/cios-and-ai-leaders-ai-infrastructure-day2-ops-and-costs
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-16, last 2026-10-23 (8x)
- **Publication:** Punam Singh (the page's own author field) - CIO&Leader / ET Edge (indiatimes.com, domain field). The body calls it an ET Edge cover story on 'Infrastructure for AI'. · domain indiatimes.com
- **Reply route:** The body says 'Please reach out to [email redacted]' - Sourcee redacts the address, and the page publishes no handle and no link. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED. AND THE ROW IS CLOSED TO US BY ITS OWN WORDING, whether or not a route is ever resolved: 'As this story focuses on end-user experience, we will not be taking vendor quotes, and we thank you for your understanding.' AIToolsEssentials is a publisher of dated vendor pricing - a vendor-adjacent source by that rule, not an end-user enterprise.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Training Data / Corporate Data Sales
- **URL:** https://www.sourcee.app/journo-request/companies-and-data-buyers-selling-corporate-data-to-train-ai
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-16, last 2026-10-23 (8x)
- **Publication:** Sam Blum (the page's own author field). No outlet named on the request or in the body; the author field matches a staff reporter who writes on technology and labour.
- **Reply route:** The body says 'DM me for my Signal information if you'd like to speak anonymously' and publishes no address, handle or link. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED - and the ask is a DM that becomes a Signal conversation, which is not a route this monitor can use.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Politics / Disinformation
- **URL:** https://www.sourcee.app/journo-request/uk-political-analysts-disinformation-and-ai-manipulation-in-politics
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-16, last 2026-10-23 (8x)
- **Publication:** Flaminia (the page's own author field). No outlet named on the request; the body carries a #journorequest tag and the subject is UK politics.
- **Reply route:** The body is a bare #journorequest asking to speak to someone, and publishes no address, handle or link of its own. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED. The route would in any case be a reply on the poster's own platform.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Content Creation / Labour & Ethics
- **URL:** https://www.sourcee.app/journo-request/content-creators-using-ai-job-losses-and-ethics
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-16, last 2026-10-23 (8x)
- **Publication:** Saumya Rastogi (the page's own author field). No outlet named on the request or in the body.
- **Reply route:** The body says 'please DM me or drop a comment below' - a route on the poster's own platform, with no handle, address or link printed on the request. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Education Policy / Nonprofit Adoption
- **URL:** https://www.sourcee.app/journo-request/school-leaders-and-ngo-staff-ai-adoption-challenges-across-sectors
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-23 (10x)
- **Publication:** Anurita Srivastava (the page's own author field). No outlet named on the request.
- **Reply route:** The body says 'I'd love to hear what you're seeing' with no address, handle or link published (published_links = Sourcee's own author chrome only, which the verifier excludes). NOT RESOLVED.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Elections / Consumer Use
- **URL:** https://www.sourcee.app/journo-request/minnesotans-using-chatgpt-and-ai-tools-experiences-with-election-info
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-23 (10x)
- **Publication:** Sofia Barnett (named in the body) - Minnesota Star Tribune (startribune.com, domain field). · domain startribune.com
- **Reply route:** The body says 'email me at [email redacted]' - Sourcee redacts the address, and the page publishes no handle and no link (published_links = Sourcee's own author chrome only). NOT RESOLVED.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Regulation / Broadcast
- **URL:** https://www.sourcee.app/journo-request/ai-policy-advisor-newsom-administration-ai-regulation
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-23 (10x)
- **Publication:** Jenny Jiin Huh (the page's own author field) - ABC10 Sacramento (abc10.com, domain field). · domain abc10.com
- **Reply route:** The request opens '@goldman' - it is addressed to one named person, not an open call, and publishes no address, handle or link of its own. NOT RESOLVED, and not open to us by its own wording.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Data Platforms / Podcast Guests
- **URL:** https://www.sourcee.app/journo-request/uk-and-us-heads-of-data-and-ai-from-idea-to-production
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-15, last 2026-10-23 (9x)
- **Publication:** Lloyd Black (the page's own author field) - Harnham / Rockborne (harnham.com, domain field), the recruiter behind the Data & AI podcast named in the body. · domain harnham.com
- **Reply route:** The body asks for 'an introduction' to other people and publishes no address, handle or link of its own. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED - and the ask is to nominate a guest, not to answer a reporter's question.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Consumer Companionship / Global South
- **URL:** https://www.sourcee.app/journo-request/ai-companion-users-in-africa-friendship-and-emotional-impact
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-15, last 2026-10-23 (9x)
- **Publication:** Danai (named in the body) - Rest of World (restofworld.org, domain field), 'a New York based publication covering emerging technology in the Global South'. · domain restofworld.org
- **Reply route:** The body says 'please message me privately or email me: [email redacted]' - Sourcee redacts the address, and the page publishes no handle and no link. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Legal Access / Academic Research
- **URL:** https://www.sourcee.app/journo-request/pro-se-litigants-using-generative-ai-access-to-justice-impact
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-15, last 2026-10-23 (9x)
- **Publication:** Reddit throwaway handle ProSe-Throwaway (the page's own author field); the body says 'I'm a UConn Law student writing an article'. No outlet, no byline, no editor named.
- **Reply route:** The body says 'please feel free to send me a private message' - a platform DM with no handle, address or link published on the request. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Global Development Sector / Practitioner Tools
- **URL:** https://www.sourcee.app/journo-request/global-development-professionals-using-ai-across-programs-and-policy
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-13, last 2026-10-23 (11x)
- **Publication:** Emma Smith (the page's own author field) — Devex (devex.com, domain field). · domain devex.com
- **Reply route:** The body says 'Get in touch' with no address, handle or link published on the request (published_links = Sourcee's own author chrome only). NOT RESOLVED as a route.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing.

### [low] AI / Startups / Founder Stories
- **URL:** https://www.sourcee.app/journo-request/african-founders-building-ai-companies-pitch-deck-realities
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-23 (10x)
- **Publication:** MarketBrain OS (the page's own author field). No outlet named on the request.
- **Reply route:** The body says 'Reply or DM' - a route on the poster's own platform, not on the request, and no handle or link is printed here. NOT RESOLVED from this end.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Higher Education / Workplace
- **URL:** https://www.sourcee.app/journo-request/higher-ed-nonfaculty-staff-ai-use-at-work
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-23 (10x)
- **Publication:** Adrienne Lu (the page's own author field). No outlet named on the request and none in the body.
- **Reply route:** The body is two lines with no address, handle or link published on the request (published_links = Sourcee's own author chrome only). NOT RESOLVED.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Channel & Partner Ecosystem / Podcast
- **URL:** https://www.sourcee.app/journo-request/podcast-guests-ai-channel-and-partner-ecosystem
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-23 (10x)
- **Publication:** Dinara B. (the page's own author field). No outlet named on the request; 'Channel Insights - AI Talk' is named in the body.
- **Reply route:** The body carries one real published link, https://lnkd.in/e-bXaf-B (a LinkedIn short link to her own show) and says 'Get in touch' - but the ask is to come on as a guest, and the link is her programme rather than a reply route to a journalist. NOT RESOLVED as a route for us.  ·  _no — published booking link https://lnkd.in/e-bXaf-B (George)_
- **Links published on the page:** https://lnkd.in/e-bXaf-B
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Data Centres / Infrastructure
- **URL:** https://www.sourcee.app/journo-request/ai-infrastructure-professionals-in-london-capacity-europe-attendees
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-23 (10x)
- **Publication:** Kai Nicol-Schwarz (the page's own author field). No outlet named on the request.
- **Reply route:** The body says 'drop me a line' with no address, handle or link published (published_links = Sourcee's own author chrome only). NOT RESOLVED, and the ask is attendance-bound.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / B2B Sales / Content Marketing
- **URL:** https://www.sourcee.app/journo-request/b2b-vendors-buyers-pasting-proposals-into-ai-tools
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-23 (10x)
- **Publication:** Lyza G (the page's own author field) - Flipbooker (flipbooker.com, domain field). · domain flipbooker.com
- **Reply route:** The body says 'Email [email redacted]' - Sourcee redacts the address, and the page publishes no handle and no link (published_links = Sourcee's own author chrome only). NOT RESOLVED.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

## Cold — only if you have a reason

Older than the 10-day line and never pitched. Not provably abandoned — no renewal signal exists on this source — but every one of these has already passed an ideal send window.

- [high] 46d old — https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
- [high] 48d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-ai-governance-and-agent-sprawl
- [high] 48d old — https://www.sourcee.app/journo-request/scientists-phd-students-and-postdocs-paying-for-ai-subscriptions
- [high] 94d old — https://www.sourcee.app/journo-request/business-and-technology-leaders-tech-budget-priorities-amid-volatility
- [high] 154d old — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [high] 173d old — https://www.sourcee.app/journo-request/anthropic-api-users-costs-and-token-burn-increase-since-january
- [medium-high] 41d old — https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
- [medium-high] 46d old — https://www.sourcee.app/journo-request/uk-managers-cracked-down-on-gen-z-ai-overuse
- [medium-high] 220d old — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium] 18d old — https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
- [medium] 42d old — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [medium] 46d old — https://www.sourcee.app/journo-request/ai-agents-making-money-2026-sales-and-leadgen-workflow-ops
- [medium] 46d old — https://www.sourcee.app/journo-request/ai-startups-workplace-fraud-detection-expenses-time-theft
- [medium] 46d old — https://www.sourcee.app/journo-request/marketing-and-content-leaders-aiassisted-work-review-process
- [medium] 50d old — https://www.sourcee.app/journo-request/ceos-ai-impact-on-ops-culture-and-commercial-strategy
- [medium] 60d old — https://www.sourcee.app/journo-request/uk-finance-risk-and-regulatory-leaders-ai-explainability-risks
- [medium] 227d old — https://www.sourcee.app/journo-request/sme-owners-operational-challenges-for-ai-solutions-case-study
- [low-medium] 13d old — https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
- [low-medium] 17d old — https://www.sourcee.app/journo-request/uk-companies-implementing-ai-how-automation-transforms-workdays
- [low-medium] 21d old — https://www.sourcee.app/journo-request/law-firm-lawyers-concrete-ai-implementations-and-billing-impact
- [low-medium] 22d old — https://www.sourcee.app/journo-request/employees-conflicted-about-ai-use-generative-ai-workplace-impact
- [low-medium] 24d old — https://www.sourcee.app/journo-request/insurance-agents-ai-use-in-personal-lines
- [medium-low] 34d old — https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business
- [low-medium] 37d old — https://www.sourcee.app/journo-request/us-founders-calls-to-slow-ai-development-impact-on-companies
- [medium-low] 43d old — https://www.sourcee.app/journo-request/tech-policy-experts-california-ai-audit-bills-impact-cios
- [low-medium] 62d old — https://www.sourcee.app/journo-request/ai-project-builders-youtube-finance-and-lifestyle-channel-feature
- [low-medium] 107d old — https://www.sourcee.app/journo-request/prompt-engineers-tokenmaxxing-anecdotes
- [low] 11d old — https://www.sourcee.app/journo-request/caine-prize-winners-gen-ai-accusations-targeting-black-writers
- [low] 11d old — https://www.sourcee.app/journo-request/software-engineers-who-left-tech-jobs-lost-to-ai-coding-tools
- [low] 11d old — https://www.sourcee.app/journo-request/manufacturers-and-ai-safety-experts-ai-risks-in-chemical-food-defense
- [low] 11d old — https://www.sourcee.app/journo-request/uk-baby-boomers-misinformation-sharing-and-ai-influence-online
- [low] 12d old — https://www.sourcee.app/journo-request/hedera-builders-shipping-defi-nfts-rwas-ai-games-and-memes
- [low] 12d old — https://www.sourcee.app/journo-request/production-designers-ai-impact-on-future-of-filmmaking
- [low] 12d old — https://www.sourcee.app/journo-request/ai-researchers-and-policy-experts-5-years-us-race-to-superintelligence
- [low] 13d old — https://www.sourcee.app/journo-request/ai-cybersecurity-iot-and-web3-founders-and-operators-news-submissions
- [low] 13d old — https://www.sourcee.app/journo-request/employees-pay-transparency-good-or-bad
- [low] 14d old — https://www.sourcee.app/journo-request/sales-reps-who-cold-call-and-email-how-ai-changed-outreach
- [low] 14d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-and-builders-realworld-deployment-and-strategy
- [low] 14d old — https://www.sourcee.app/journo-request/voters-who-used-ai-to-navigate-ballot-voting-experience
- [low] 14d old — https://www.sourcee.app/journo-request/anthropic-gtm-leaders-scaling-300k-b2b-clients
- [low] 15d old — https://www.sourcee.app/journo-request/patent-attorneys-and-agents-startup-ip-starter-pack
- [low] 15d old — https://www.sourcee.app/journo-request/hotel-and-fandb-supervisors-and-managers-customer-expectations-vs-ai
- [low] 15d old — https://www.sourcee.app/journo-request/researchers-founders-and-funders-ai-transforming-scientific-research
- [low] 15d old — https://www.sourcee.app/journo-request/facebook-marketplace-sellers-ai-listing-photos-and-selling-experience
- [low] 16d old — https://www.sourcee.app/journo-request/aps-hr-leaders-ai-skills-training-and-workforce-planning
- [low] 16d old — https://www.sourcee.app/journo-request/scrum-masters-daytoday-and-career-pivots-and-ai-impact
- [low] 16d old — https://www.sourcee.app/journo-request/real-estate-agents-replacing-pdf-property-brochure
- [low] 16d old — https://www.sourcee.app/journo-request/anz-marketers-ai-and-martech-innovation-spotlight
- [low] 16d old — https://www.sourcee.app/journo-request/solicitors-and-barristers-ai-to-expand-pro-bono-capacity
- [low] 16d old — https://www.sourcee.app/journo-request/uk-ai-data-trainers-daytoday-work
- [low] 16d old — https://www.sourcee.app/journo-request/apac-reporters-and-editors-ai-accountability-coverage
- [low] 16d old — https://www.sourcee.app/journo-request/early-to-midcareer-information-architects-products-featuring-ai
- [low] 16d old — https://www.sourcee.app/journo-request/martech-buyers-ai-impact-on-build-vs-buy-decisions
- [low] 17d old — https://www.sourcee.app/journo-request/ai-infrastructure-experts-china-vs-us-datacenter-capacity
- [low] 17d old — https://www.sourcee.app/journo-request/plaintiffs-attorneys-and-legal-scholars-ai-deepfake-liability
- [low] 17d old — https://www.sourcee.app/journo-request/emergency-managers-ai-tools-for-funding-and-staffing-shortfalls
- [low] 17d old — https://www.sourcee.app/journo-request/coweta-county-artists-and-creatives-data-centers-and-ai-infrastructure
- [low] 17d old — https://www.sourcee.app/journo-request/swiss-ai-companion-users-emotional-bonds-and-daily-life
- [low] 17d old — https://www.sourcee.app/journo-request/ai-data-labelers-in-germany-positive-and-negative-experiences
- [low] 17d old — https://www.sourcee.app/journo-request/ai-data-annotators-and-labellers-experience-with-ai-training-data
- [low] 17d old — https://www.sourcee.app/journo-request/ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories
- [low] 17d old — https://www.sourcee.app/journo-request/academics-social-media-and-ai-impact-on-womens-identity-and-selfesteem
- [low] 18d old — https://www.sourcee.app/journo-request/ai-liability-insurers-and-legal-experts-procurement-and-implementation
- [low] 18d old — https://www.sourcee.app/journo-request/uk-cybersecurity-hiring-managers-state-of-hiring-2026-and-ai-impact
- [low] 18d old — https://www.sourcee.app/journo-request/ai-emotional-support-users-chatbot-therapy-and-journaling
- [low] 18d old — https://www.sourcee.app/journo-request/mortgage-adviser-using-ai-efficiency-and-client-outcomes-video-series
- [low] 18d old — https://www.sourcee.app/journo-request/founders-and-cxos-in-automotive-ai-evs-autonomy-thought-leadership
- [low] 19d old — https://www.sourcee.app/journo-request/video-game-developer-falsely-accused-of-using-generative-ai
- [low] 20d old — https://www.sourcee.app/journo-request/lawyers-and-tech-ethics-experts-ai-wearables-and-legal-journeys
- [low] 20d old — https://www.sourcee.app/journo-request/mls-executives-risks-when-agents-grant-mls-access-to-llms
- [low] 20d old — https://www.sourcee.app/journo-request/real-estate-agents-and-brokers-switched-from-pdf-brochures
- [low] 21d old — https://www.sourcee.app/journo-request/storytellers-and-brand-founders-marys-big-30-ai-story-project
- [low] 21d old — https://www.sourcee.app/journo-request/newsletter-editors-using-ai-agents-news-aggregation-practices
- [low] 21d old — https://www.sourcee.app/journo-request/scottish-teachers-ai-tools-implementation-in-education
- [low] 21d old — https://www.sourcee.app/journo-request/advertising-tech-and-media-pros-in-miami-ai-audience-discovery
- [low] 21d old — https://www.sourcee.app/journo-request/hr-leaders-company-ai-strategies-and-cognitive-offloading-risk
- [low] 22d old — https://www.sourcee.app/journo-request/fea-engineers-using-agentic-ai-practitioner-case-study
- [low] 22d old — https://www.sourcee.app/journo-request/parents-ai-acting-as-pseudoparent-in-kid-questions
- [low] 22d old — https://www.sourcee.app/journo-request/fb-marketplace-sellers-ai-photos-and-description-prompts
- [low] 22d old — https://www.sourcee.app/journo-request/k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact
- [low] 22d old — https://www.sourcee.app/journo-request/ai-summit-barcelona-attendees-controversy-and-experiences
- [low] 22d old — https://www.sourcee.app/journo-request/ai-glasses-owners-users-and-developers-in-india-product-experience
- [low] 23d old — https://www.sourcee.app/journo-request/cybersecurity-expert-ai-nexus-and-security-risks
- [low] 23d old — https://www.sourcee.app/journo-request/chatbot-users-experiences-talking-to-ai
- [low] 23d old — https://www.sourcee.app/journo-request/us-ai-security-experts-rogue-ai-agents-hitting-government-sites
- [low] 23d old — https://www.sourcee.app/journo-request/real-estate-agents-pdf-brochures-vs-alternatives-agent-workflow
- [low] 24d old — https://www.sourcee.app/journo-request/us-emergency-physicians-and-paramedics-impact-of-ai-answering-911-calls
- [low] 24d old — https://www.sourcee.app/journo-request/job-seekers-and-recruiters-ai-recruitment-experiences
- [low] 25d old — https://www.sourcee.app/journo-request/data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity
- [low] 25d old — https://www.sourcee.app/journo-request/b2b-marketing-leaders-hyperspecialization-to-outcompete-ai
- [low] 25d old — https://www.sourcee.app/journo-request/ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes
- [low] 31d old — https://www.sourcee.app/journo-request/saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup
- [low] 31d old — https://www.sourcee.app/journo-request/engineering-managers-measuring-engineers-when-using-ai
- [low] 31d old — https://www.sourcee.app/journo-request/ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai
- [low] 32d old — https://www.sourcee.app/journo-request/sales-enablement-saas-tools-proposal-and-deck-engagement-tracking
- [low] 32d old — https://www.sourcee.app/journo-request/founders-and-leaders-mindsets-and-milestones
- [low] 32d old — https://www.sourcee.app/journo-request/london-businesses-stopped-using-ai-hiring-tools
- [low] 32d old — https://www.sourcee.app/journo-request/creative-industry-professionals-podcast-on-ai-impact
- [low] 32d old — https://www.sourcee.app/journo-request/former-ai-skeptics-changed-views-on-ai-impact
- [low] 33d old — https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- [low] 33d old — https://www.sourcee.app/journo-request/employers-and-recruiters-over-50s-adapting-to-ai
- [low] 33d old — https://www.sourcee.app/journo-request/data-center-professionals-podcast-guest-ai-and-hyperscale-trends
- [low] 33d old — https://www.sourcee.app/journo-request/patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges
- [low] 33d old — https://www.sourcee.app/journo-request/ml-researchers-continuous-learning-fast-weights-and-adapters
- [low] 33d old — https://www.sourcee.app/journo-request/founders-55-latelife-entrepreneurship-series-1
- [low] 33d old — https://www.sourcee.app/journo-request/founders-and-entrepreneurs-and-musicians-podcast-guests
- [low] 34d old — https://www.sourcee.app/journo-request/ai-alignment-researchers-humanai-mutual-understanding
- [low] 35d old — https://www.sourcee.app/journo-request/companies-that-stopped-emailing-pdfs-new-tools-and-transition
- [low] 36d old — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 36d old — https://www.sourcee.app/journo-request/gen-z-ai-data-annotators-work-experience-and-income-impact
- [low] 36d old — https://www.sourcee.app/journo-request/ai-automation-experts-speakers-on-marketing-sales-operations-gains
- [low] 36d old — https://www.sourcee.app/journo-request/ecommerce-marketers-transparency-in-ai-recommendations-and-conversion
- [low] 37d old — https://www.sourcee.app/journo-request/cybersecurity-companies-and-experts-ai-scams-and-consumer-safety
- [low] 105d old — https://www.sourcee.app/journo-request/investigative-reporters-openai-training-predatory-dynamic-pricing

---

## Clearing the queue

After sending, record it so the row does not reappear:

```json
{"pitched": {"<url>": "2026-09-15"}, "skipped": {"<url>": "reason"}}
```

Ledger: `marketing/haro-outreach/pitch-ledger.json`
