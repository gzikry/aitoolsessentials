# Pitch queue — clear this in one pass

Built 2026-10-16 from 140 unique requests across the digest history. **1 sendable**, 56 live, 77 cold (> 10 days and unpitched).

*"Sendable" is the number that matters and the one the headline used to hide: a live page is not a candidate. A row counts as sendable only when it is live, not cold, not dropped off, not already pitched, ranked above the tangential band, and has a resolved reply route (a published email, a named handle, a booking link). The other live rows are off-beat calls this queue already documents as excluded.*

**Ages are read off each request page** (`datePublished`), not off the digest text — see `marketing/haro-outreach/verified-requests.json`, refreshed by `scripts/verify_journo_requests.py`. An earlier build fell back to the digest's first-seen date and showed a 190-day-old request as 8 days old.

**No renewal signal exists on this source.** Sourcee publishes no renewal signal: on the 300 most recently indexed slugs and all 30 slugs of the live AI topic feed (checked 2026-09-19) the sitemap lastmod is byte-identical to datePublished, so 'never refreshed' is not observable and is not claimed here. Cold means old and unpitched, not provably abandoned.

**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, Qwoted and Medialyst need authenticated sessions, and Sourcee redacts the requester's own address in the request body. That is why 43 flagged opportunities produced zero pitches. Reply routes are named per row — including addresses resolved off the *publication's* own site (a byline page or an editorial contact page), which is now the strongest route class in this queue.

## Drafts that exist and were never sent

Read this before clearing the queue: 29 draft files exist on disk. **3 of the pitches drafted here have now been sent** — listed at the bottom, not as work. The rest are still unsent; a written draft is not progress — the send is.

**THE QUEUE IS AT 1 SENDABLE.** Every build before the 2026-10-06 run reported 0, and twice that 0 was a genuine measurement after a defect had been fixed (the 2026-09-29 chrome leak into `published_links`, the 2026-10-01 Google Form read as a link route). A row is declared sendable on two facts evidenced separately rather than trusted from a digest field: a relevance above the tangential band, and a reply route verified by fetching a page today. Both are named in the row. A build holding more than one sendable row used to be rare — the 2026-10-10 build was the first to hold two, and it did so because a route was resolved off a publication's own site rather than because a new find arrived. This build holds 1. The live unpitched set is 56 rows.

**Today's draft file is `pitch-drafts-2026-10-16.md` (derived from disk, not typed).** The headline figures are re-derived every run: 42 of 78 tools publish a monthly price, 33 of those at or under $25/month, median $17.50 (snapshots `updated: 2026-10-16`). Superseded sets still sitting in older dated drafts (40/31/$16.50 and earlier) must not be reused.

**The pair range is `1.11x to 2.53x, median 1.25x` over 19 tiers, and it held today.** History, because every superseded value is still sitting in dated draft files and must not be reused: the range was first published as `1.21x to 2.53x, median 1.33x` (2026-09-18, sent to a real correspondent — wrong because the pair population was regex-dependent and undefined); corrected to `1.16x to 2.53x, median 1.25x` over 18 curated pairs (2026-09-21); then re-derived to `1.11x to 2.53x` when the replit-ai snapshot was refreshed (2026-09-22). See `data/monthly_annual_pairs.json` and `scripts/extract_monthly_annual_pairs.py`, which refuses to write the file at all unless every curated pair re-asserts against the live snapshot.

- anthropic-users-and-business-owners-customer-service-experiences — **Crossed cold 2026-09-23; now 34d old — no longer counted as sendable.** Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal hliwrites.99 (re-read verbatim off the live page 2026-09-30). Send late or record as skipped in `pitch-ledger.json`; the crossing is logged in `cold_without_a_send`.
- employees-blocked-from-ai-on-work-accounts-automating-tedious-ta — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — §2 in `pitch-drafts-2026-10-16.md`. Now 11d old.** Route: LinkedIn DM to linkedin.com/in/christopher-mims-club/ (LinkedIn byline page — route-checks probe 2026-10-16: HTTP 200, 658,713 bytes, title 'Christopher Mims - The Wall Street Journal | LinkedIn'; the request's own body says '(DMs open)'; muckrack.com/christopher-mims 403 and wsj.com/news/author/christopher-mims 401 are dead ends, not routes — both last re-checked 2026-10-15, the day before this build). It has left the sendable count: the row is now past the 10-day line and this queue no longer ranks it as actionable. The route is not dead and the draft named above is still paste-ready — George's call is to send it late or record it skipped in `pitch-ledger.json`. Silence is the one option that leaves it drifting.
- finops-professionals-agentic-ai-cost-overruns — **Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1. Now 39d old.** Route: LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 and still unsent — the longest-standing high-relevance request this monitor has never answered. Send it late or drop it, do not draft it a fifth time.

### Already sent — do NOT re-send

- fulltime-employees-shadow-ai-use-and-paying-outofpocket — **SENT BUT BOUNCED — the address is dead, do not retry it; a fresh route is needed before this row can be sent at all.** `pitch-ledger.json`: 2026-10-10 (SENT BUT BOUNCED - see log)
- google-and-claude-enterprise-users-seats-and-token-costs — SENT. `pitch-ledger.json`: 2026-10-10
- speciality-food-retailers-and-producers-how-theyd-spend-10k-on-t — SENT. `pitch-ledger.json`: 2026-10-10

## Sendable — pitch these (1)

Live, not cold, ranked above the tangential band, and with a reply route a human can actually use. This is the whole actionable queue.

### [low-medium] AI / Future of Work / Jobs & Hiring / Original Data
- **URL:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-11, last 2026-10-16 (6x)
- **Publication:** Tobi Amure (the page's own author field) - freelancer building pitches for Fast Company's Work Life section; his body text says his work runs in Investopedia, TheStreet, Forbes, Inc., Benzinga and FinanceFeeds. Fast Company does not name him on the request. · domain fastcompany.com
- **Reply route:** The request page redacts the address ('email me at [email redacted]') and says explicitly 'No DM pitches here on LinkedIn. Email me.' ROUTE: hello@tobiamure.com, published by the journalist himself on his own site, https://tobiamure.com/ - re-fetched today in route-checks-2026-10-16.json: HTTP 200, 58,905 bytes, title 'Tobi Amure | Finance &amp; Technology Journalist', with the address appearing verbatim 6 times on that page (Person JSON-LD email field, his own FAQ answer, and the site footer). His contact page https://tobiamure.com/contact/ re-fetched today: HTTP 200, 16,213 bytes, title 'Hire a Finance &amp; Crypto Writer | Tobi Amure', address verbatim 5 times. tobiamure.com MX = Namecheap email forwarding (eforward1-5.registrar-servers.com), so the domain routes mail. Six byline pages remain recorded dead ends so they are not retried as routes (last re-checked 2026-10-15): muckrack.com/tobi-amure, investopedia.com/tobi-amure-5203106, forbes.com/sites/tobiamure, thestreet.com/author/tobi-amure, benzinga.com/author/tobi-amure, inc.com/author/tobi-amure - all HTTP 403. EMAIL ROUTE - no platform form, no DM, no scheduling link. Sending is George's lane.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** Answer his own stated requirement - 'Original data, or a survey with its sample size and method' - with the method and the denominator, not a credential: 42 of 78 tracked AI tools publish a monthly price, 33 of those at or under $25/month, median $17.50, every figure carrying the date we checked it and a source URL (snapshots updated 2026-10-16); […] (full angle in the digest entry for this row)

## Live but not sendable (55)

These pages resolve and the requests are unexpired, so they are recorded — but none has both a relevance above the tangential band and a usable route. They are listed for completeness, not as candidates: pitching any of them would mean claiming standing we do not have (see the exclusions in the newest `pitch-drafts-*.md`).

### [low-medium] AI / B2B Buying Process / Vendor Research
- **URL:** https://www.sourcee.app/journo-request/b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-13, last 2026-10-16 (4x)
- **Publication:** Lyza G (the page's own author field). No outlet named on the request.
- **Reply route:** The body says 'Email [email redacted]' — Sourcee redacts the address, and the page publishes no handle and no link (published_links = Sourcee's own author chrome only, which the verifier excludes). NOT RESOLVED as a route.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None. No route and no standing.

### [low-medium] AI / Enterprise Adoption / CNBC Series
- **URL:** https://www.sourcee.app/journo-request/uk-companies-implementing-ai-how-automation-transforms-workdays
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-16 (10x)
- **Publication:** Lindsay Dodgson (author field) — CNBC (cnbc.com, domain field) · domain cnbc.com
- **Reply route:** Body: 'you know where to find me [email redacted]'. Address Sourcee-redacted; no handle or link published. NO ROUTE RESOLVED as-is. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=True, feed=Y.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** If a route is ever resolved, the only defensible angle is the dated-price half of 'fresh data': 42 of 78 tools quote a monthly price, 33 at or under $25/month, median $17.50; monthly vs annual 1.11x-2.53x, median 1.25x over 19 tiers (snapshots re-checked 2026-10-10). Do NOT claim to be a UK company implementing AI. Excluded this run for want of a route.

### [low] AI / Visual Art / Feature Story
- **URL:** https://www.sourcee.app/journo-request/painters-and-photographers-ai-impact-on-art
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-15, last 2026-10-16 (2x)
- **Publication:** Reddit throwaway-style handle Beautiful_Annual9811 (the page's own author field). No outlet and no journalist named on the request or in the body.
- **Reply route:** The body says 'Any recommendations please let me know, I'd be happy to reach out' - it asks the reader to volunteer other people, and publishes no address, handle or link of its own. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Legal Sector / Job Displacement
- **URL:** https://www.sourcee.app/journo-request/legal-assistants-paralegals-and-lawfirm-staff-jobs-eliminated-by-ai
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-15, last 2026-10-16 (2x)
- **Publication:** Reddit-style throwaway handle YardOptimal9329 (the page's own author field). The body says 'I'm a journalist looking to speak with...' but names no outlet and no byline.
- **Reply route:** The body says 'please DM me' - a route on the poster's own platform, with no handle, address or link printed on the request. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Enterprise Infrastructure / Day-2 Ops & Costs
- **URL:** https://www.sourcee.app/journo-request/cios-and-ai-leaders-ai-infrastructure-day2-ops-and-costs
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-16, last 2026-10-16 (1x)
- **Publication:** Punam Singh (the page's own author field) - CIO&Leader / ET Edge (indiatimes.com, domain field). The body calls it an ET Edge cover story on 'Infrastructure for AI'. · domain indiatimes.com
- **Reply route:** The body says 'Please reach out to [email redacted]' - Sourcee redacts the address, and the page publishes no handle and no link. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED. AND THE ROW IS CLOSED TO US BY ITS OWN WORDING, whether or not a route is ever resolved: 'As this story focuses on end-user experience, we will not be taking vendor quotes, and we thank you for your understanding.' AIToolsEssentials is a publisher of dated vendor pricing - a vendor-adjacent source by that rule, not an end-user enterprise.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Training Data / Corporate Data Sales
- **URL:** https://www.sourcee.app/journo-request/companies-and-data-buyers-selling-corporate-data-to-train-ai
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-16, last 2026-10-16 (1x)
- **Publication:** Sam Blum (the page's own author field). No outlet named on the request or in the body; the author field matches a staff reporter who writes on technology and labour.
- **Reply route:** The body says 'DM me for my Signal information if you'd like to speak anonymously' and publishes no address, handle or link. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED - and the ask is a DM that becomes a Signal conversation, which is not a route this monitor can use.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Politics / Disinformation
- **URL:** https://www.sourcee.app/journo-request/uk-political-analysts-disinformation-and-ai-manipulation-in-politics
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-10-16, last 2026-10-16 (1x)
- **Publication:** Flaminia (the page's own author field). No outlet named on the request; the body carries a #journorequest tag and the subject is UK politics.
- **Reply route:** The body is a bare #journorequest asking to speak to someone, and publishes no address, handle or link of its own. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED. The route would in any case be a reply on the poster's own platform.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Content Creation / Labour & Ethics
- **URL:** https://www.sourcee.app/journo-request/content-creators-using-ai-job-losses-and-ethics
- **Posted:** 1d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-16, last 2026-10-16 (1x)
- **Publication:** Saumya Rastogi (the page's own author field). No outlet named on the request or in the body.
- **Reply route:** The body says 'please DM me or drop a comment below' - a route on the poster's own platform, with no handle, address or link printed on the request. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Education Policy / Nonprofit Adoption
- **URL:** https://www.sourcee.app/journo-request/school-leaders-and-ngo-staff-ai-adoption-challenges-across-sectors
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-16 (3x)
- **Publication:** Anurita Srivastava (the page's own author field). No outlet named on the request.
- **Reply route:** The body says 'I'd love to hear what you're seeing' with no address, handle or link published (published_links = Sourcee's own author chrome only, which the verifier excludes). NOT RESOLVED.  ·  _unknown — verify the route before sending_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Elections / Consumer Use
- **URL:** https://www.sourcee.app/journo-request/minnesotans-using-chatgpt-and-ai-tools-experiences-with-election-info
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-16 (3x)
- **Publication:** Sofia Barnett (named in the body) - Minnesota Star Tribune (startribune.com, domain field). · domain startribune.com
- **Reply route:** The body says 'email me at [email redacted]' - Sourcee redacts the address, and the page publishes no handle and no link (published_links = Sourcee's own author chrome only). NOT RESOLVED.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Regulation / Broadcast
- **URL:** https://www.sourcee.app/journo-request/ai-policy-advisor-newsom-administration-ai-regulation
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-16 (3x)
- **Publication:** Jenny Jiin Huh (the page's own author field) - ABC10 Sacramento (abc10.com, domain field). · domain abc10.com
- **Reply route:** The request opens '@goldman' - it is addressed to one named person, not an open call, and publishes no address, handle or link of its own. NOT RESOLVED, and not open to us by its own wording.  ·  _no — email resolved off the publication's own site (George sends)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Data Platforms / Podcast Guests
- **URL:** https://www.sourcee.app/journo-request/uk-and-us-heads-of-data-and-ai-from-idea-to-production
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-15, last 2026-10-16 (2x)
- **Publication:** Lloyd Black (the page's own author field) - Harnham / Rockborne (harnham.com, domain field), the recruiter behind the Data & AI podcast named in the body. · domain harnham.com
- **Reply route:** The body asks for 'an introduction' to other people and publishes no address, handle or link of its own. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED - and the ask is to nominate a guest, not to answer a reporter's question.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Consumer Companionship / Global South
- **URL:** https://www.sourcee.app/journo-request/ai-companion-users-in-africa-friendship-and-emotional-impact
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-15, last 2026-10-16 (2x)
- **Publication:** Danai (named in the body) - Rest of World (restofworld.org, domain field), 'a New York based publication covering emerging technology in the Global South'. · domain restofworld.org
- **Reply route:** The body says 'please message me privately or email me: [email redacted]' - Sourcee redacts the address, and the page publishes no handle and no link. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Legal Access / Academic Research
- **URL:** https://www.sourcee.app/journo-request/pro-se-litigants-using-generative-ai-access-to-justice-impact
- **Posted:** 2d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-15, last 2026-10-16 (2x)
- **Publication:** Reddit throwaway handle ProSe-Throwaway (the page's own author field); the body says 'I'm a UConn Law student writing an article'. No outlet, no byline, no editor named.
- **Reply route:** The body says 'please feel free to send me a private message' - a platform DM with no handle, address or link published on the request. The only links on the page are Sourcee's own author chrome (linkedin.com/in/andrewsmith313, x.com/andy_cb_smith), which the verifier excludes from published_links; neither is a route to the poster. NOT RESOLVED.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why another unsent draft would be a defect rather than progress.

### [low] AI / Global Development Sector / Practitioner Tools
- **URL:** https://www.sourcee.app/journo-request/global-development-professionals-using-ai-across-programs-and-policy
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-13, last 2026-10-16 (4x)
- **Publication:** Emma Smith (the page's own author field) — Devex (devex.com, domain field). · domain devex.com
- **Reply route:** The body says 'Get in touch' with no address, handle or link published on the request (published_links = Sourcee's own author chrome only). NOT RESOLVED as a route.  ·  _unknown — verify the route before sending_
- **Angle:** None. No route and no standing.

### [low] AI / Startups / Founder Stories
- **URL:** https://www.sourcee.app/journo-request/african-founders-building-ai-companies-pitch-deck-realities
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-16 (3x)
- **Publication:** MarketBrain OS (the page's own author field). No outlet named on the request.
- **Reply route:** The body says 'Reply or DM' - a route on the poster's own platform, not on the request, and no handle or link is printed here. NOT RESOLVED from this end.  ·  _no — platform reply (George)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Higher Education / Workplace
- **URL:** https://www.sourcee.app/journo-request/higher-ed-nonfaculty-staff-ai-use-at-work
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-16 (3x)
- **Publication:** Adrienne Lu (the page's own author field). No outlet named on the request and none in the body.
- **Reply route:** The body is two lines with no address, handle or link published on the request (published_links = Sourcee's own author chrome only). NOT RESOLVED.  ·  _unknown — verify the route before sending_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Channel & Partner Ecosystem / Podcast
- **URL:** https://www.sourcee.app/journo-request/podcast-guests-ai-channel-and-partner-ecosystem
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-16 (3x)
- **Publication:** Dinara B. (the page's own author field). No outlet named on the request; 'Channel Insights - AI Talk' is named in the body.
- **Reply route:** The body carries one real published link, https://lnkd.in/e-bXaf-B (a LinkedIn short link to her own show) and says 'Get in touch' - but the ask is to come on as a guest, and the link is her programme rather than a reply route to a journalist. NOT RESOLVED as a route for us.  ·  _no — published booking link https://lnkd.in/e-bXaf-B (George)_
- **Links published on the page:** https://lnkd.in/e-bXaf-B
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Data Centres / Infrastructure
- **URL:** https://www.sourcee.app/journo-request/ai-infrastructure-professionals-in-london-capacity-europe-attendees
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-16 (3x)
- **Publication:** Kai Nicol-Schwarz (the page's own author field). No outlet named on the request.
- **Reply route:** The body says 'drop me a line' with no address, handle or link published (published_links = Sourcee's own author chrome only). NOT RESOLVED, and the ask is attendance-bound.  ·  _unknown — verify the route before sending_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / B2B Sales / Content Marketing
- **URL:** https://www.sourcee.app/journo-request/b2b-vendors-buyers-pasting-proposals-into-ai-tools
- **Posted:** 3d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-14, last 2026-10-16 (3x)
- **Publication:** Lyza G (the page's own author field) - Flipbooker (flipbooker.com, domain field). · domain flipbooker.com
- **Reply route:** The body says 'Email [email redacted]' - Sourcee redacts the address, and the page publishes no handle and no link (published_links = Sourcee's own author chrome only). NOT RESOLVED.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None. No route and no standing. NOT DRAFTED - see the run's own note on why an eighth unsent draft would be a defect rather than progress.

### [low] AI / Publishing & Authorship / Plagiarism Accusations
- **URL:** https://www.sourcee.app/journo-request/caine-prize-winners-gen-ai-accusations-targeting-black-writers
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-13, last 2026-10-16 (4x)
- **Publication:** noid. (the page's own author field) — for takingCustody, named in the body.
- **Reply route:** The body is a public DM request to three named Caine Prize winners; no address, handle or link is published on the request itself. NOT RESOLVED as a route, and the people asked are named individuals rather than an open call.  ·  _no — platform reply (George)_
- **Angle:** None. No route and no standing.

### [low] AI / Labour Market / Coding Tools
- **URL:** https://www.sourcee.app/journo-request/software-engineers-who-left-tech-jobs-lost-to-ai-coding-tools
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-13, last 2026-10-16 (4x)
- **Publication:** Thibault Spirlet (the page's own author field) — Business Insider (businessinsider.com, domain field). · domain businessinsider.com
- **Reply route:** The body says 'Please reach out at [email redacted]' — Sourcee redacts the address and the page publishes no alternative handle or link (published_links = Sourcee's own author chrome only). NOT RESOLVED as a route.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None. No route and no standing.

### [low] AI / Industrial Safety / Risk
- **URL:** https://www.sourcee.app/journo-request/manufacturers-and-ai-safety-experts-ai-risks-in-chemical-food-defense
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-13, last 2026-10-16 (4x)
- **Publication:** Sakshi Udavant (Luna) (the page's own author field) — Manufacturing Dive (manufacturingdive.com, domain field). · domain manufacturingdive.com
- **Reply route:** The body says 'For: Manufacturing Dive [email redacted]' — Sourcee redacts the address and the page publishes no other route (published_links = Sourcee's own author chrome only). NOT RESOLVED.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None. No route and no standing.

### [low] AI / Media Literacy / Audience Research
- **URL:** https://www.sourcee.app/journo-request/uk-baby-boomers-misinformation-sharing-and-ai-influence-online
- **Posted:** 4d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-13, last 2026-10-16 (4x)
- **Publication:** Dan McCarthy (the page's own author field) — Canvas8 (canvas8.com, domain field). · domain canvas8.com
- **Reply route:** The body asks for academics researching misinformation and publishes no address, handle or link (published_links = Sourcee's own author chrome only). NOT RESOLVED as a route.  ·  _unknown — verify the route before sending_
- **Angle:** None. No route and no standing.

### [low] AI / Crypto-adjacent Builders / Podcast Feature
- **URL:** https://www.sourcee.app/journo-request/hedera-builders-shipping-defi-nfts-rwas-ai-games-and-memes
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-12, last 2026-10-16 (5x)
- **Publication:** Tate (the page's own author field) - 'I host the Hedera Builder Spotlight with @Genfinity', a podcast/interview series for the Hedera (HBAR) ecosystem. No outlet named beyond that.
- **Reply route:** The request says 'my DMs are open' - a DM on the poster's own platform (the page carries no address, no handle and no link; published_links = Sourcee's own author chrome only, which the verifier excludes). NOT RESOLVED as a route: there is no handle on the request to DM.  ·  _no — platform reply (George)_
- **Angle:** None. No route and no standing.

### [low] AI / Film & TV Production Design / Practitioner Quotes
- **URL:** https://www.sourcee.app/journo-request/production-designers-ai-impact-on-future-of-filmmaking
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-12, last 2026-10-16 (5x)
- **Publication:** Katy Deboo (the page's own author field). No publication named on the request.
- **Reply route:** The body says 'drop me an email at [email redacted]' - Sourcee redacts the address, and the page publishes no handle or link (published_links = Sourcee's own author chrome only). NOT RESOLVED.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None. No route and no standing.

### [low] AI / Geopolitics & Policy / Podcast Guest
- **URL:** https://www.sourcee.app/journo-request/ai-researchers-and-policy-experts-5-years-us-race-to-superintelligence
- **Posted:** 5d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-12, last 2026-10-16 (5x)
- **Publication:** Joshua C. (the page's own author field) - The Global Signal, a podcast seeking an expert guest.
- **Reply route:** No address, handle or link is published on the request (published_links = Sourcee's own author chrome only). The ask is to be a guest; there is no stated reply route. NOT RESOLVED.  ·  _unknown — verify the route before sending_
- **Angle:** None. No route and no standing.

### [low] AI / Startup News Submissions
- **URL:** https://www.sourcee.app/journo-request/ai-cybersecurity-iot-and-web3-founders-and-operators-news-submissions
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-11, last 2026-10-16 (6x)
- **Publication:** Aditya Prakash (the page's own author field) - Morning Tick, a startup-news publication · domain morningtick.com
- **Reply route:** 'Get in touch: [email redacted]' - Sourcee redacts the address and the page publishes no other handle or link (published_links = Sourcee's own author chrome only). Its one outbound link, lnkd.in/gHZDHvxS, is a Morning Tick 'about us' shortlink, not a reply route. NOT RESOLVED.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Links published on the page:** https://lnkd.in/gHZDHvxS
- **Angle:** None. No route and no standing.

### [low] Workplace / Pay Transparency / Audio Vox Pop
- **URL:** https://www.sourcee.app/journo-request/employees-pay-transparency-good-or-bad
- **Posted:** 6d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-11, last 2026-10-16 (6x)
- **Publication:** Melita Cameron-Wood (the page's own author field) - Business Spotlight Audio
- **Reply route:** No address, handle or link published on the request (published_links = Sourcee's own author chrome only). NOT RESOLVED.  ·  _unknown — verify the route before sending_
- **Angle:** None. Audio vox pop from employees; no route.

### [low] AI / Sales Outreach / Practitioner Experience
- **URL:** https://www.sourcee.app/journo-request/sales-reps-who-cold-call-and-email-how-ai-changed-outreach
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-09, last 2026-10-16 (8x)
- **Publication:** Issie Lapowsky (author field) — outlet not named in the body
- **Reply route:** Body: 'I want your personal stories only, please! If you send me a product pitch for your company/your client's company, you will be placed on the naughty list. [email redacted] or Signal at issielapowsky.08'. Address Sourcee-redacted; Signal handle pubd. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=True.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None — excluded: explicitly anti-pitch; wants reps' personal stories only.

### [low] AI / Vendor Studio Promo / Podcast Booking
- **URL:** https://www.sourcee.app/journo-request/enterprise-ai-leaders-and-builders-realworld-deployment-and-strategy
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-09, last 2026-10-16 (8x)
- **Publication:** Bruce Burke (author field) — Neural News Network studio (own promo)
- **Reply route:** Body: 'Drop a comment below or send a direct message, and let's get you on the studio schedule.' No address, handle or link printed. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=False, emails_on_page=none.  ·  _no — scheduling link (George)_
- **Angle:** None — excluded: booking promo, not an editorial request.

### [low] AI / Civic / Voter Experience
- **URL:** https://www.sourcee.app/journo-request/voters-who-used-ai-to-navigate-ballot-voting-experience
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-09, last 2026-10-16 (8x)
- **Publication:** Atlanta Community Press Collective (author field) — atlpresscollective.com · domain atlpresscollective.com
- **Reply route:** Body: 'Reach out to [email redacted] ATL Press Collective'. Address Sourcee-redacted; no handle or link. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=True, emails_on_page=none.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: wants voters' personal voter-experience stories.

### [low] AI / Vendor GTM / Interview Booking
- **URL:** https://www.sourcee.app/journo-request/anthropic-gtm-leaders-scaling-300k-b2b-clients
- **Posted:** 7d old (page datePublished) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-10-11, last 2026-10-16 (6x)
- **Publication:** Tris Tusa (the page's own author field) - an interviewer running a sales/GTM podcast and newsletter; no outlet is named on the request itself
- **Reply route:** 'give me a shout' - no address, handle or link is published on the request. The two links the page carries, linkedin.com/in/andrewsmith313 and x.com/andy_cb_smith, are Sourcee's own author chrome and are excluded by the verifier's CHROME list. NOT RESOLVED.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None. Do not pitch this without an Anthropic GTM introduction we do not have.

### [low] Legal / IP / Practitioner Guide
- **URL:** https://www.sourcee.app/journo-request/patent-attorneys-and-agents-startup-ip-starter-pack
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-08, last 2026-10-16 (9x)
- **Publication:** Ptoleme (author field) — no domain named
- **Reply route:** Body: 'Feel free to comment or message me' with an acknowledgement offer, but no address, handle or link printed. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, feed=n.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants patent practitioners; no spend angle, no route.

### [low] AI / Hospitality / Practitioner Interviews
- **URL:** https://www.sourcee.app/journo-request/hotel-and-fandb-supervisors-and-managers-customer-expectations-vs-ai
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-09, last 2026-10-16 (8x)
- **Publication:** Nick Teare (author field) — outlet not named in the body
- **Reply route:** Body: 'Please let me know if you or someone on your team might be interested.' No address, handle or link printed; interviews promised confidential. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=False, emails_on_page=none.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants hospitality supervisors' own interviews.

### [low] AI / Research Landscape Study / Survey Call
- **URL:** https://www.sourcee.app/journo-request/researchers-founders-and-funders-ai-transforming-scientific-research
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-09, last 2026-10-16 (8x)
- **Publication:** Yarissa M. (author field) — Renaissance Philanthropy, with Google.org support
- **Reply route:** Body: 'Sign up here: https://lnkd.in/gyCpc-Dh'. That is a participation sign-up form for their own landscape analysis, not a reply route to a reporter; it asks respondents to be interviewed about their science work. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=False.  ·  _no — published booking link https://lnkd.in/gyCpc-Dh (George)_
- **Links published on the page:** https://lnkd.in/gyCpc-Dh
- **Angle:** None — excluded: wants AI-in-science practitioners for a study interview, not a pitch.

### [low] AI / Consumer Marketplaces / Seller Experience
- **URL:** https://www.sourcee.app/journo-request/facebook-marketplace-sellers-ai-listing-photos-and-selling-experience
- **Posted:** 8d old (page datePublished) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-10-09, last 2026-10-16 (8x)
- **Publication:** Rainesford Stauffer (author field) — outlet not named in the body
- **Reply route:** Body: 'I'm reporting on this and would love to hear about it: [email redacted], or DM me'. Address Sourcee-redacted, no handle or link printed. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=True, emails_on_page=none.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None — excluded: wants FB Marketplace sellers' own stories.

### [low] AI / Public-Sector Workforce / Skills & Training
- **URL:** https://www.sourcee.app/journo-request/aps-hr-leaders-ai-skills-training-and-workforce-planning
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-16 (10x)
- **Publication:** Joshua Gliddon (author field) — The Mandarin (themandarin.com.au, domain field) · domain themandarin.com.au
- **Reply route:** Body: 'please drop me a line' with no address, handle or link published; the page's only published links are Sourcee chrome. email_redacted=False but emails_on_page=none. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, feed=Y.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants public-sector HR interviewees; no spend angle and no route.

### [low] AI / Agile Careers / Podcast Guest Booking
- **URL:** https://www.sourcee.app/journo-request/scrum-masters-daytoday-and-career-pivots-and-ai-impact
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-16 (10x)
- **Publication:** Dr. Yvette Jett (author field) — The Dr. Vett Jett Show (vettjett.com, domain field) · domain vettjett.com
- **Reply route:** Body: 'Send me a message right here on LinkedIn or email me at [email redacted]'. The address is Sourcee-redacted and no handle is printed; no route resolved. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=True, emails_on_page=none.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: wants practising Scrum Masters as guests; we hold no such standing.

### [low] AI / PropTech / Vendor Blog Content Call
- **URL:** https://www.sourcee.app/journo-request/real-estate-agents-replacing-pdf-property-brochure
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-16 (10x)
- **Publication:** Lyza G (author field) — Flipbooker blog (flipbooker.com, domain field) · domain flipbooker.com
- **Reply route:** Body: 'Email [email redacted]'. Address Sourcee-redacted; no handle or link. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=True.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: vendor blog promo wanting a real-estate agent voice.

### [low] AI / Marketing Technology / Self-Promo Spotlight
- **URL:** https://www.sourcee.app/journo-request/anz-marketers-ai-and-martech-innovation-spotlight
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-16 (10x)
- **Publication:** RAHUL B. (author field) — KARV Tech Insider (domain not named in the page's domain field)
- **Reply route:** Body: 'DM me. Let's connect and explore how we can amplify your story.' No handle, address or link published; the page's only published links are Sourcee chrome. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, feed=Y.  ·  _no — platform reply (George)_
- **Angle:** None — excluded: self-promo spotlight, no editorial data ask and no route.

### [low] AI / Legal Sector / Access to Justice
- **URL:** https://www.sourcee.app/journo-request/solicitors-and-barristers-ai-to-expand-pro-bono-capacity
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-08, last 2026-10-16 (9x)
- **Publication:** Catherine Baksi (author field) — publication not named
- **Reply route:** Body: 'please drop me an email at: [email redacted] by the end of this week'. Address Sourcee-redacted; no handle or link. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=True, emails_on_page=none.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: wants law firms' own pro-bono AI projects; no spend angle, no route.

### [low] AI / Labour / Data Training
- **URL:** https://www.sourcee.app/journo-request/uk-ai-data-trainers-daytoday-work
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-08, last 2026-10-16 (9x)
- **Publication:** momitola (author handle) — The Times (thetimes.co.uk, domain field) · domain thetimes.co.uk
- **Reply route:** Body: 'Ping me a message if you're interested'. No handle, address or link printed. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, feed=n.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants UK data trainers' first-person accounts.

### [low] AI / Press & Media / Accountability
- **URL:** https://www.sourcee.app/journo-request/apac-reporters-and-editors-ai-accountability-coverage
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-08, last 2026-10-16 (9x)
- **Publication:** Sen Nguyen (author field) — BBC News (bbc.co.uk, domain field) · domain bbc.co.uk
- **Reply route:** Body: 'Hit me up here or at [email redacted]'. Address Sourcee-redacted; no handle or link. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=True.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: wants APAC reporters/editors; no spend angle.

### [low] AI / UX & IA / Practitioner Interviews
- **URL:** https://www.sourcee.app/journo-request/early-to-midcareer-information-architects-products-featuring-ai
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-08, last 2026-10-16 (9x)
- **Publication:** World Information Architecture Association (author field) — no domain named
- **Reply route:** No address, handle or link published; the body gives no reply instruction. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, feed=n.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants IA practitioners' own product stories.

### [low] AI / Martech / Vendor Blog Content Call
- **URL:** https://www.sourcee.app/journo-request/martech-buyers-ai-impact-on-build-vs-buy-decisions
- **Posted:** 9d old (page datePublished) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-10-08, last 2026-10-16 (9x)
- **Publication:** Lyza G (author field) — Flipbooker blog (flipbooker.com, domain field) · domain flipbooker.com
- **Reply route:** Body: 'Email [email redacted]'. Address Sourcee-redacted; no handle or link. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=True.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: vendor blog promo wanting martech-buyer quotes.

### [low] AI / Infrastructure / Data-Centre Capacity
- **URL:** https://www.sourcee.app/journo-request/ai-infrastructure-experts-china-vs-us-datacenter-capacity
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-16 (11x)
- **Publication:** Harriet Weber (author field) — outlet not named in the body
- **Reply route:** The body publishes a Signal username, 'hew.04', plus an address Sourcee redacts. Signal is a resolved route; the request still asks for expertise we do not hold. PAGE-VERIFIED 2026-10-10: HTTP 200, email_redacted=True, emails_on_page=none, published_links=Sourcee chrome only.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: no data-centre-capacity expertise. Route (Signal hew.04) recorded so the exclusion can be audited.

### [low] AI / Legal / Deepfake Liability
- **URL:** https://www.sourcee.app/journo-request/plaintiffs-attorneys-and-legal-scholars-ai-deepfake-liability
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-16 (11x)
- **Publication:** Mitchell Price (author field) — outlet not named (student podcast)
- **Reply route:** The body asks respondents to 'comment on this post'; no address, handle or link is published. PAGE-VERIFIED 2026-10-10: HTTP 200, email_redacted=False, emails_on_page=none, reply_hints=none, published_links=Sourcee chrome only. No route we can use.  ·  _no — LinkedIn DM / comment (George)_
- **Angle:** None — excluded: wants practising attorneys or legal scholars for a student podcast; no spend angle and no route.

### [low] AI / Emergency Management / Public-Sector Adoption
- **URL:** https://www.sourcee.app/journo-request/emergency-managers-ai-tools-for-funding-and-staffing-shortfalls
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-16 (11x)
- **Publication:** Jake Bittle (named in the body) — Grist (grist.org, domain field) · domain grist.org
- **Reply route:** The body prints a phone number (8134664712) and an address Sourcee redacts. Grist's staff page grist.org/staff/jake-bittle/ returns HTTP 404, so no email route resolved. A phone is a voice route, not a written pitch route. PAGE-VERIFIED 2026-10-10: HTTP 200, email_redacted=True, emails_on_page=none, published_links=Sourcee chrome only.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: wants an emergency manager's own departmental experience.

### [low] AI / Arts & Community / Data-Centre Siting
- **URL:** https://www.sourcee.app/journo-request/coweta-county-artists-and-creatives-data-centers-and-ai-infrastructure
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-06, last 2026-10-16 (11x)
- **Publication:** Artist Rights Watch (author field) — outlet not named in the body
- **Reply route:** An X post tagging named panellists for an in-person symposium panel; the body carries a t.co link and no address or handle for us. PAGE-VERIFIED 2026-10-10: HTTP 200, email_redacted=False, emails_on_page=none, published_links=['https://t.co/8l6CGKC9yq', ...Sourcee chrome]. No route we can use.  ·  _unknown — verify the route before sending_
- **Links published on the page:** https://t.co/8l6CGKC9yq
- **Angle:** None — excluded: local panel invitation, not a source request.

### [low] AI / Human-AI Relationships / Documentary
- **URL:** https://www.sourcee.app/journo-request/swiss-ai-companion-users-emotional-bonds-and-daily-life
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-16 (10x)
- **Publication:** Leila (author handle) — SRF 'rec.' (srf.ch, domain field) · domain srf.ch
- **Reply route:** Body: 'You're welcome to send me a private message'. No address, handle or link printed. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, feed=Y.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants Swiss AI-companion users' personal accounts.

### [low] AI / Labour / Data Annotation
- **URL:** https://www.sourcee.app/journo-request/ai-data-labelers-in-germany-positive-and-negative-experiences
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-16 (10x)
- **Publication:** freelance journalist (author handle JulDagg) — FLUTER (fluter.de, domain field) · domain fluter.de
- **Reply route:** No address, handle or link published in the body; interviews offered anonymously. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, feed=Y.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants German data annotators' first-person accounts.

### [low] AI / Labour / Data Annotation
- **URL:** https://www.sourcee.app/journo-request/ai-data-annotators-and-labellers-experience-with-ai-training-data
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-16 (10x)
- **Publication:** Modupe (author field) — The Times (thetimes.co.uk, domain field) · domain thetimes.co.uk
- **Reply route:** Body: 'My email is [email redacted]'. Address Sourcee-redacted; no handle or link. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, email_redacted=True.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None — excluded: wants annotators' first-person accounts, no spend angle.

### [low] AI / Mental Health / Self-Diagnosis
- **URL:** https://www.sourcee.app/journo-request/ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-16 (10x)
- **Publication:** student journalist (author handle yaegrrr) — publication not named
- **Reply route:** Body: 'feel free to send me a PM or comment below'. No address, handle or link published. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, feed=n.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants users'/therapists' personal accounts.

### [low] AI / Academia / Media & Identity
- **URL:** https://www.sourcee.app/journo-request/academics-social-media-and-ai-impact-on-womens-identity-and-selfesteem
- **Posted:** 10d old (page datePublished) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-10-07, last 2026-10-16 (10x)
- **Publication:** Lucy Abbersteen (author field) — publication not named
- **Reply route:** Body: 'please comment below!' No address, handle or link published; the only way in is a public comment. NO ROUTE RESOLVED. PAGE-VERIFIED 2026-10-10: HTTP 200, live=True, feed=n.  ·  _unknown — verify the route before sending_
- **Angle:** None — excluded: wants academic researchers; no route beyond a public comment.

## Cold — only if you have a reason

Older than the 10-day line and never pitched. Not provably abandoned — no renewal signal exists on this source — but every one of these has already passed an ideal send window.

- [high] 39d old — https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
- [high] 41d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-ai-governance-and-agent-sprawl
- [high] 41d old — https://www.sourcee.app/journo-request/scientists-phd-students-and-postdocs-paying-for-ai-subscriptions
- [high] 87d old — https://www.sourcee.app/journo-request/business-and-technology-leaders-tech-budget-priorities-amid-volatility
- [high] 147d old — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [high] 166d old — https://www.sourcee.app/journo-request/anthropic-api-users-costs-and-token-burn-increase-since-january
- [medium-high] 34d old — https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
- [medium-high] 39d old — https://www.sourcee.app/journo-request/uk-managers-cracked-down-on-gen-z-ai-overuse
- [medium-high] 213d old — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium] 11d old — https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
- [medium] 35d old — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [medium] 39d old — https://www.sourcee.app/journo-request/ai-agents-making-money-2026-sales-and-leadgen-workflow-ops
- [medium] 39d old — https://www.sourcee.app/journo-request/ai-startups-workplace-fraud-detection-expenses-time-theft
- [medium] 39d old — https://www.sourcee.app/journo-request/marketing-and-content-leaders-aiassisted-work-review-process
- [medium] 43d old — https://www.sourcee.app/journo-request/ceos-ai-impact-on-ops-culture-and-commercial-strategy
- [medium] 53d old — https://www.sourcee.app/journo-request/uk-finance-risk-and-regulatory-leaders-ai-explainability-risks
- [medium] 220d old — https://www.sourcee.app/journo-request/sme-owners-operational-challenges-for-ai-solutions-case-study
- [low-medium] 14d old — https://www.sourcee.app/journo-request/law-firm-lawyers-concrete-ai-implementations-and-billing-impact
- [low-medium] 15d old — https://www.sourcee.app/journo-request/employees-conflicted-about-ai-use-generative-ai-workplace-impact
- [low-medium] 17d old — https://www.sourcee.app/journo-request/insurance-agents-ai-use-in-personal-lines
- [medium-low] 27d old — https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business
- [low-medium] 30d old — https://www.sourcee.app/journo-request/us-founders-calls-to-slow-ai-development-impact-on-companies
- [medium-low] 36d old — https://www.sourcee.app/journo-request/tech-policy-experts-california-ai-audit-bills-impact-cios
- [low-medium] 55d old — https://www.sourcee.app/journo-request/ai-project-builders-youtube-finance-and-lifestyle-channel-feature
- [low-medium] 100d old — https://www.sourcee.app/journo-request/prompt-engineers-tokenmaxxing-anecdotes
- [low] 11d old — https://www.sourcee.app/journo-request/ai-liability-insurers-and-legal-experts-procurement-and-implementation
- [low] 11d old — https://www.sourcee.app/journo-request/uk-cybersecurity-hiring-managers-state-of-hiring-2026-and-ai-impact
- [low] 11d old — https://www.sourcee.app/journo-request/ai-emotional-support-users-chatbot-therapy-and-journaling
- [low] 11d old — https://www.sourcee.app/journo-request/mortgage-adviser-using-ai-efficiency-and-client-outcomes-video-series
- [low] 11d old — https://www.sourcee.app/journo-request/founders-and-cxos-in-automotive-ai-evs-autonomy-thought-leadership
- [low] 12d old — https://www.sourcee.app/journo-request/video-game-developer-falsely-accused-of-using-generative-ai
- [low] 13d old — https://www.sourcee.app/journo-request/lawyers-and-tech-ethics-experts-ai-wearables-and-legal-journeys
- [low] 13d old — https://www.sourcee.app/journo-request/mls-executives-risks-when-agents-grant-mls-access-to-llms
- [low] 13d old — https://www.sourcee.app/journo-request/real-estate-agents-and-brokers-switched-from-pdf-brochures
- [low] 14d old — https://www.sourcee.app/journo-request/storytellers-and-brand-founders-marys-big-30-ai-story-project
- [low] 14d old — https://www.sourcee.app/journo-request/newsletter-editors-using-ai-agents-news-aggregation-practices
- [low] 14d old — https://www.sourcee.app/journo-request/scottish-teachers-ai-tools-implementation-in-education
- [low] 14d old — https://www.sourcee.app/journo-request/advertising-tech-and-media-pros-in-miami-ai-audience-discovery
- [low] 14d old — https://www.sourcee.app/journo-request/hr-leaders-company-ai-strategies-and-cognitive-offloading-risk
- [low] 15d old — https://www.sourcee.app/journo-request/fea-engineers-using-agentic-ai-practitioner-case-study
- [low] 15d old — https://www.sourcee.app/journo-request/parents-ai-acting-as-pseudoparent-in-kid-questions
- [low] 15d old — https://www.sourcee.app/journo-request/fb-marketplace-sellers-ai-photos-and-description-prompts
- [low] 15d old — https://www.sourcee.app/journo-request/k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact
- [low] 15d old — https://www.sourcee.app/journo-request/ai-summit-barcelona-attendees-controversy-and-experiences
- [low] 15d old — https://www.sourcee.app/journo-request/ai-glasses-owners-users-and-developers-in-india-product-experience
- [low] 16d old — https://www.sourcee.app/journo-request/cybersecurity-expert-ai-nexus-and-security-risks
- [low] 16d old — https://www.sourcee.app/journo-request/chatbot-users-experiences-talking-to-ai
- [low] 16d old — https://www.sourcee.app/journo-request/us-ai-security-experts-rogue-ai-agents-hitting-government-sites
- [low] 16d old — https://www.sourcee.app/journo-request/real-estate-agents-pdf-brochures-vs-alternatives-agent-workflow
- [low] 17d old — https://www.sourcee.app/journo-request/us-emergency-physicians-and-paramedics-impact-of-ai-answering-911-calls
- [low] 17d old — https://www.sourcee.app/journo-request/job-seekers-and-recruiters-ai-recruitment-experiences
- [low] 18d old — https://www.sourcee.app/journo-request/data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity
- [low] 18d old — https://www.sourcee.app/journo-request/b2b-marketing-leaders-hyperspecialization-to-outcompete-ai
- [low] 18d old — https://www.sourcee.app/journo-request/ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes
- [low] 24d old — https://www.sourcee.app/journo-request/saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup
- [low] 24d old — https://www.sourcee.app/journo-request/engineering-managers-measuring-engineers-when-using-ai
- [low] 24d old — https://www.sourcee.app/journo-request/ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai
- [low] 25d old — https://www.sourcee.app/journo-request/sales-enablement-saas-tools-proposal-and-deck-engagement-tracking
- [low] 25d old — https://www.sourcee.app/journo-request/founders-and-leaders-mindsets-and-milestones
- [low] 25d old — https://www.sourcee.app/journo-request/london-businesses-stopped-using-ai-hiring-tools
- [low] 25d old — https://www.sourcee.app/journo-request/creative-industry-professionals-podcast-on-ai-impact
- [low] 25d old — https://www.sourcee.app/journo-request/former-ai-skeptics-changed-views-on-ai-impact
- [low] 26d old — https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- [low] 26d old — https://www.sourcee.app/journo-request/employers-and-recruiters-over-50s-adapting-to-ai
- [low] 26d old — https://www.sourcee.app/journo-request/data-center-professionals-podcast-guest-ai-and-hyperscale-trends
- [low] 26d old — https://www.sourcee.app/journo-request/patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges
- [low] 26d old — https://www.sourcee.app/journo-request/ml-researchers-continuous-learning-fast-weights-and-adapters
- [low] 26d old — https://www.sourcee.app/journo-request/founders-55-latelife-entrepreneurship-series-1
- [low] 26d old — https://www.sourcee.app/journo-request/founders-and-entrepreneurs-and-musicians-podcast-guests
- [low] 27d old — https://www.sourcee.app/journo-request/ai-alignment-researchers-humanai-mutual-understanding
- [low] 28d old — https://www.sourcee.app/journo-request/companies-that-stopped-emailing-pdfs-new-tools-and-transition
- [low] 29d old — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 29d old — https://www.sourcee.app/journo-request/gen-z-ai-data-annotators-work-experience-and-income-impact
- [low] 29d old — https://www.sourcee.app/journo-request/ai-automation-experts-speakers-on-marketing-sales-operations-gains
- [low] 29d old — https://www.sourcee.app/journo-request/ecommerce-marketers-transparency-in-ai-recommendations-and-conversion
- [low] 30d old — https://www.sourcee.app/journo-request/cybersecurity-companies-and-experts-ai-scams-and-consumer-safety
- [low] 98d old — https://www.sourcee.app/journo-request/investigative-reporters-openai-training-predatory-dynamic-pricing

---

## Clearing the queue

After sending, record it so the row does not reappear:

```json
{"pitched": {"<url>": "2026-09-15"}, "skipped": {"<url>": "reason"}}
```

Ledger: `marketing/haro-outreach/pitch-ledger.json`
