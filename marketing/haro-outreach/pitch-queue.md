# Pitch queue — clear this in one pass

Built 2026-11-14 from 308 unique requests across the digest history. **1 sendable**, 64 live, 235 cold (> 10 days and unpitched), 42 expired on the platform.

**3 finished drafts are ready to send now — 'Send these now' below names each route; 1 of them is inside the 10-day line.**

*"Sendable" is the number that matters and the one the headline used to hide: a live page is not a candidate. A row counts as sendable only when it is live, not cold, not dropped off, not already pitched, ranked above the tangential band, and has a resolved reply route (a published email, a named handle, a booking link). The other live rows are off-beat calls this queue already documents as excluded.*

**Ages are read off each request page** (`datePublished`), not off the digest text — see `marketing/haro-outreach/verified-requests.json`, refreshed by `scripts/verify_journo_requests.py`. An earlier build fell back to the digest's first-seen date and showed a 190-day-old request as 8 days old.

**No renewal signal exists on this source.** Sourcee publishes no renewal signal: on the 300 most recently indexed slugs and all 30 slugs of the live AI topic feed (checked 2026-09-19) the sitemap lastmod is byte-identical to datePublished, so 'never refreshed' is not observable and is not claimed here. Cold means old and unpitched, not provably abandoned.

**No NEW expiry in the 2026-11-14 run — but 44 carried requests are already dead.** Each answered HTTP 404 again and remains absent from the sitemap; the 2026-11-14 digest did not record a fresh wave. The rule stands: a row can disappear between two runs a day apart, so a live row is worth sending today.

**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, Qwoted and Medialyst need authenticated sessions, and Sourcee redacts the requester's own address in the request body. That is the friction that produced zero sends from the first 43 flagged opportunities. Reply routes are named per row — including addresses resolved off the *publication's* own site (a byline page or an editorial contact page), which is now the strongest route class in this queue.

## Drafts that exist and were never sent

Read this before clearing the queue: 53 draft files exist on disk. **3 of the pitches drafted here have now been sent** — listed at the bottom, not as work. The rest are still unsent; a written draft is not progress — the send is.

**THE QUEUE HOLDS 1 SENDABLE ROW(S).** A row is declared sendable on two facts evidenced separately rather than trusted from a digest field: a relevance above the tangential band, and a reply route verified by fetching a page today. Both are named in the row. The previous run reported 1; the last run before it with a non-zero count was 2026-11-13, with 0 consecutive zero run(s) in between. The live unpitched set is 64 rows.

**Today's draft file is `pitch-drafts-2026-11-14.md` (derived from disk, not typed).** The headline figures are re-derived every run: 45 of 111 tools publish a monthly price, 36 of those at or under $25/month, median $16.00 (snapshots `updated: 2026-11-14`). Superseded sets still sitting in older dated drafts (40/31/$16.50 and earlier) must not be reused.

**The pair range is `1.11x to 2.53x, median 1.25x` over 19 tiers, and it held today.** History, because every superseded value is still sitting in dated draft files and must not be reused: the range was first published as `1.21x to 2.53x, median 1.33x` (2026-09-18, sent to a real correspondent — wrong because the pair population was regex-dependent and undefined); corrected to `1.16x to 2.53x, median 1.25x` over 18 curated pairs (2026-09-21); then re-derived to `1.11x to 2.53x` when the replit-ai snapshot was refreshed (2026-09-22). See `data/monthly_annual_pairs.json` and `scripts/extract_monthly_annual_pairs.py`, which refuses to write the file at all unless every curated pair re-asserts against the live snapshot.

- anthropic-users-and-business-owners-customer-service-experiences — **Crossed cold 2026-09-23; now 64d old — no longer counted as sendable.** Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal hliwrites.99 (re-read verbatim off the live page 2026-09-30). Send late or record as skipped in `pitch-ledger.json`; the crossing is logged in `cold_without_a_send`.
- employees-blocked-from-ai-on-work-accounts-automating-tedious-ta — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — §3 in `pitch-drafts-2026-10-27.md`. Now 40d old.** Route: LinkedIn DM to linkedin.com/in/christopher-mims-club/ (LinkedIn byline page — route-checks probe 2026-11-14: HTTP 200, 618,897 bytes, title 'Christopher Mims - The Wall Street Journal | LinkedIn'; the request's own body says '(DMs open)'; muckrack.com/christopher-mims 403 and wsj.com/news/author/christopher-mims 401 are dead ends, not routes — both re-checked in the same 2026-11-14 probe). It has left the sendable count: the row is now past the 10-day line and this queue no longer ranks it as actionable. The route is not dead and the draft named above is still paste-ready — George's call is to send it late or record it skipped in `pitch-ledger.json`. Silence is the one option that leaves it drifting.
- finops-professionals-agentic-ai-cost-overruns — **Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1. Now 68d old.** Route: LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 and still unsent — the longest-standing high-relevance request this monitor has never answered. Send it late or drop it, do not draft it a fifth time.
- tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — §3 in `pitch-drafts-2026-10-28.md`. Now 35d old, carried in 27 draft files.** Route: hello@tobiamure.com, the address the journalist publishes himself on his own site — tobiamure.com homepage — route-checks probe 2026-11-14: HTTP 200, 63,314 bytes, title 'Tobi Amure, CFEI® | Finance &amp; Technology Journalist', with the contact form on tobiamure.com/contact — route-checks probe 2026-11-14: HTTP 200, 18,449 bytes, title 'Contact Tobi Amure | Finance &amp; Technology Journalist' as the fallback if mail bounces. Deliverability is NOT SMTP-verified: the domain's MX answers 554 Relay access denied for a real address, a fake control and postmaster@ alike, so that probe discriminates nothing. He asks for 'original data, or a survey with its sample size and method' and refuses DM pitches, which is why the draft leads with the one measured series we hold. Past the 10-day line the send is still possible — a late send or a ledger entry closes it; silence leaves it drifting exactly as the WSJ row did on 2026-10-16.

### Already sent — do NOT re-send

- fulltime-employees-shadow-ai-use-and-paying-outofpocket — **SENT BUT BOUNCED — the address is dead, do not retry it; a fresh route is needed before this row can be sent at all.** `pitch-ledger.json`: 2026-10-10 (SENT BUT BOUNCED - see log)
- google-and-claude-enterprise-users-seats-and-token-costs — SENT. `pitch-ledger.json`: 2026-10-10
- speciality-food-retailers-and-producers-how-theyd-spend-10k-on-t — SENT. `pitch-ledger.json`: 2026-10-10

## Send these now (3) — a finished draft and a live route

Each row below has a finished, paste-ready pitch in `pitch-drafts-2026-11-14.md` and a page that served the request today. 1 is inside the 10-day line and 2 sit past it. The line is this monitor's own heuristic, not the platform's: no page on this source has ever carried an expiry, so a past-line row is late, not dead. A send, or a `skipped` entry in `pitch-ledger.json`, closes each one. A rewrite of the same draft does not.

- **§1 in `pitch-drafts-2026-11-14.md`** — https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai — 4d old, page live today, route `kelsey.ziser@informationweek.com`
- **§3 in `pitch-drafts-2026-11-14.md`** — https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training — 17d old, page live today, route `linkedin.com/in/vidya-das`
- **§2 in `pitch-drafts-2026-11-14.md`** — https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes — 18d old, page live today, route `alison@alisoncoleman.co.uk`

## Sendable — pitch these (1)

Live, not cold, ranked above the tangential band, and with a reply route a human can actually use. This is the whole actionable queue.

### [low-medium] AI / Enterprise Spend / SaaS Pricing Pressure
- **URL:** https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai
- **Posted:** 4d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-10, last 2026-11-14 (5x)
- **Publication:** InformationWeek (informationweek.com) - Kelsey Ziser, Senior Editor, named in the page's author field. · domain informationweek.com
- **Reply route:** Route resolved OFF the request page, not guessed: kelsey.ziser@informationweek.com, published as a mailto link on her InformationWeek author page https://www.informationweek.com/author/kelsey-ziser (route-checks-2026-11-14.json: HTTP 200, 582,084 bytes, title 'Kelsey Ziser | Senior Editor, InformationWeek', address present once as 'Kelsey.ziser@' and once as 'kelsey.ziser@' in the markup). The request page itself publishes no address and no link. The send is George's: no plain mailbox on a request page has ever been ours to write to unattended. Deliverability is not SMTP-verified - only a bounce proves anything.  ·  _no — email resolved off the publication's own site: kelsey.ziser@informationweek.com (George sends)_
- **Angle:** Email to kelsey.ziser@informationweek.com. Subject: 'The seat-price numbers behind the SaaSpocalypse question'. Open with one measured number from the 2026-11-14 snapshot (45 of 111 tracked AI tools publish a monthly price, median cheapest paid seat $16.00), give the monthly-vs-annual premium (1.11x-2.53x, median 1.25x over 19 tiers, asserted 2026-10-16), state plainly that we are a price census […] (full angle in the digest entry for this row)

## Live but not sendable (63)

These pages resolve and the requests are unexpired, so they are recorded — but none has both a relevance above the tangential band and a usable route. They are listed for completeness, not as candidates: pitching any of them would mean claiming standing we do not have (see the exclusions in the newest `pitch-drafts-*.md`).

### [medium] AI / Pricing Models
- **URL:** https://www.sourcee.app/journo-request/companies-switched-from-token-ai-pricing-outcomebased-contracts
- **Posted:** 2d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Agam Shah, named in the page's author field; no publication stated on the page.
- **Reply route:** The page publishes no address, handle or link of its own, and the body names no contact route. Sourcee's redaction is not the reason: there is simply no route on the page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route, and the ask excludes us by its own terms. NOT DRAFTED.

### [low-medium] AI / Labour Economics
- **URL:** https://www.sourcee.app/journo-request/labor-economists-unintended-consequences-of-automation
- **Posted:** 4d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-14 (4x)
- **Publication:** Gavin Clarke, named in the page's author field; no publication stated.
- **Reply route:** The page publishes no address, handle or link of its own; the body says 'drop me a line' and gives nothing to drop it to. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route resolved. If a route is found, the angle is the annual-billing premium as an unrecognised adoption cost - 1.11x to 2.53x, median 1.25x over 19 same-tier pairs, asserted 2026-10-16 - offered as data, not as labour-economics expertise.

### [low-medium] AI / SMB Adoption
- **URL:** https://www.sourcee.app/journo-request/business-owners-and-leaders-team-resistance-to-ai-adoption
- **Posted:** 7d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-07, last 2026-11-14 (8x)
- **Publication:** Not named on the page; the body advertises 'National media coverage opp!' with no outlet or byline
- **Reply route:** The body says 'Hit me up!' and publishes no address, handle or link. NOT a reply route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Hiring Testimony
- **URL:** https://www.sourcee.app/journo-request/job-seekers-postai-interviews-and-recruiters-ai-interview-impact
- **Posted:** 1d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Jordan Friedman, named in the page's author field; no publication stated.
- **Reply route:** The body says 'comment or DM'; the page publishes no handle or link to either. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Podcast Guest Call
- **URL:** https://www.sourcee.app/journo-request/us-retail-executives-agentic-ai-shopping-in-ecommerce
- **Posted:** 1d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Russell Goldsmith, named in the page's author field; no publication stated (the body describes 'our own channel, the c-suite podcast').
- **Reply route:** The page publishes no address, handle or link; the body invites guest pitches without a route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Not our standing, no route. NOT DRAFTED.

### [low] EV / Whistleblower Call
- **URL:** https://www.sourcee.app/journo-request/ev-industry-employees-insider-stories-and-source-protection
- **Posted:** 1d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Suvrat Kothari, named in the page's author field; domain insideevs.com. · domain insideevs.com
- **Reply route:** The body's email is redacted by Sourcee. A Signal handle is published: @suvratk.13. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site (George sends)_
- **Angle:** None. Not an AI request, no standing. NOT DRAFTED.

### [low] Tech / Outage Testimony
- **URL:** https://www.sourcee.app/journo-request/microsoft-365-users-email-outage-impact-on-workflows
- **Posted:** 1d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-14, last 2026-11-14 (1x)
- **Publication:** Ricky Boleto, BBC News (page author field; domain bbc.co.uk). · domain bbc.co.uk
- **Reply route:** The page publishes no address and no handle. One shortlink is embedded in the body: https://t.co/Wm8BPSYAzN, which is a BBC News link, not a reply route. Links published on the page: https://t.co/Wm8BPSYAzN.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/Wm8BPSYAzN
- **Angle:** None. Not an AI request and no route. NOT DRAFTED.

### [low] AI / Consumer Testimony
- **URL:** https://www.sourcee.app/journo-request/individuals-accused-of-using-ai-misattribution-experiences
- **Posted:** 1d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-14, last 2026-11-14 (1x)
- **Publication:** Suzanne Bearne, freelance journalist writing for national titles (no publication named on the page).
- **Reply route:** The body lists three separate asks and says 'PRs and agents, email me' for the celebrity slots only; no address, handle or link is published anywhere on the page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Podcast Guest Call
- **URL:** https://www.sourcee.app/journo-request/servicenow-customers-and-partners-podcast-guests-ai-and-career-stories
- **Posted:** 1d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-14, last 2026-11-14 (1x)
- **Publication:** Brogan Howie, ServiceNow (domain servicenow.com). · domain servicenow.com
- **Reply route:** No address or handle published. One shortlink in the body: https://lnkd.in/eDkSrN6T, which points at the ServiceNow podcast series, not at a reply route. Links published on the page: https://lnkd.in/eDkSrN6T.  ·  _no — published booking link https://lnkd.in/eDkSrN6T (George)_
- **Links published on the page:** https://lnkd.in/eDkSrN6T
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Workplace Testimony
- **URL:** https://www.sourcee.app/journo-request/israeli-software-developers-ai-impact-on-jobs
- **Posted:** 1d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-14, last 2026-11-14 (1x)
- **Publication:** Daniela Fubini (page author field); the request itself is from Gianluca Pacchiani. No publication named on the page.
- **Reply route:** The page publishes no address, handle or link; the body says 'Tag your friends' on LinkedIn and gives nothing to send to. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Local Inference
- **URL:** https://www.sourcee.app/journo-request/local-model-operators-10-prod-inference-and-7-figure-biz
- **Posted:** 1d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-14, last 2026-11-14 (1x)
- **Publication:** Brad, no surname and no publication named on the page.
- **Reply route:** The page publishes no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Enterprise IT Testimony
- **URL:** https://www.sourcee.app/journo-request/midsize-manufacturing-it-leaders-ai-impact-on-tasks-teams-governance
- **Posted:** 1d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Dan Tynan, named in the page's author field; domain freshworks.com. · domain freshworks.com
- **Reply route:** One shortlink published on the page: https://lnkd.in/gjjANXqs (not resolved; the page states no address). Links published on the page: https://lnkd.in/gjjANXqs.  ·  _no — published booking link https://lnkd.in/gjjANXqs (George)_
- **Links published on the page:** https://lnkd.in/gjjANXqs
- **Angle:** None. Standing explicitly excluded. NOT DRAFTED.

### [low] AI / Workplace Adoption
- **URL:** https://www.sourcee.app/journo-request/employees-using-ai-avatars-training-and-support-zdnet
- **Posted:** 1d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Radhika Rajkumar, named in the page's author field; domain zdnet.com. · domain zdnet.com
- **Reply route:** The body asks readers to reply 'in the comments'; the page publishes no address or handle. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Adoption Testimony
- **URL:** https://www.sourcee.app/journo-request/accountants-and-bookkeepers-who-dont-use-ai-why-they-opt-out
- **Posted:** 2d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-14 (3x)
- **Publication:** Debra Kilsheimer - the byline on the page; no publication named.
- **Reply route:** The body invites a comment or a private message on the platform the post came from; no address published on the request page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] Consumer Finance / Case Study
- **URL:** https://www.sourcee.app/journo-request/parents-of-students-with-loans-managing-cost-and-sacrifices-ipaper
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Maria Shahid, named in the page's author field; domain inews.co.uk. · domain inews.co.uk
- **Reply route:** The body's email is redacted by Sourcee; the body also says 'message me here' (a platform reply). The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Off-beat on both items. NOT DRAFTED.

### [low] AI / Industry News Reaction
- **URL:** https://www.sourcee.app/journo-request/frontier-ai-industry-insiders-huang-resignation-impact-and-next-steps
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Greta Reich, named in the page's author field; domain usatoday.com. · domain usatoday.com
- **Reply route:** The body's email is redacted by Sourcee. A Signal handle is published in the body: gretareich.19. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Routable but off-beat. NOT DRAFTED.

### [low] AI / Policy News Reaction
- **URL:** https://www.sourcee.app/journo-request/ai-leader-jensen-huang-resignation-ai-policy-and-china
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Emilia David, named in the page's author field; domain ismg.io (Information Security Media Group). · domain ismg.io
- **Reply route:** The body's email is redacted by Sourcee; the page publishes no other route. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Voter Testimony
- **URL:** https://www.sourcee.app/journo-request/midterm-voters-on-ai-data-center-measure-why-they-voted
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Ginny Hogan, named in the page's author field; no publication stated.
- **Reply route:** The body's email is redacted by Sourcee; no other route published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Industry News Reaction
- **URL:** https://www.sourcee.app/journo-request/ai-startup-founders-jensen-huang-resignation-impact-and-opensource
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Aaron Mok, named in the page's author field; domain inc.com. · domain inc.com
- **Reply route:** The body's email is redacted by Sourcee; no other route published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Channel Partner Testimony
- **URL:** https://www.sourcee.app/journo-request/msp-owners-resellers-and-integrators-ai-ops-security-and-supply-chain
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Victoria Durgin, named in the page's author field; domain channelinsider.com. · domain channelinsider.com
- **Reply route:** The body's email is redacted by Sourcee. It also offers 'message me here', which is a platform reply on Sourcee itself, and an in-person meeting at an Ingram event. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Wrong standing, no draft.

### [low] AI / Podcast Guest Call
- **URL:** https://www.sourcee.app/journo-request/software-engineers-and-leaders-one-practical-engineering-question
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** John Crickett, named in the page's author field; no publication stated (Coding Chats podcast).
- **Reply route:** The page publishes no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Podcast Guest Call
- **URL:** https://www.sourcee.app/journo-request/berlin-london-and-sf-ai-founders-and-tech-execs-podcast-tech-landscape
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Sowmya Guru, named in the page's author field; no publication stated.
- **Reply route:** The body asks for 'comments' and mentions people in them; no address, handle or link is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Consumer Testimony
- **URL:** https://www.sourcee.app/journo-request/individuals-and-small-businesses-accused-of-using-ai-false-allegations
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-13, last 2026-11-14 (2x)
- **Publication:** Suzanne Bearne, named in the page's author field; no publication stated (the body says 'a national').
- **Reply route:** The body says 'DM me'; no handle or link is published on the page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Labour Testimony
- **URL:** https://www.sourcee.app/journo-request/ramp-crews-and-gate-agents-hardest-and-best-job-moments
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-14 (3x)
- **Publication:** Plan0gram (plan0gram.com/bs) - the byline on the page; no publication named.
- **Reply route:** No address, handle or link published on the request page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Podcast Promo
- **URL:** https://www.sourcee.app/journo-request/innovators-and-changemakers-neuroscience-ai-future-of-work
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-14 (3x)
- **Publication:** Pamela Cowan, Build Resilience International - the byline on the page; no publication named.
- **Reply route:** No address, handle or link published on the request page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Promo post, no route. NOT DRAFTED.

### [low] AI / Education Testimony
- **URL:** https://www.sourcee.app/journo-request/teachers-and-school-leaders-ai-in-school-devices-student-wellbeing
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-14 (3x)
- **Publication:** Wired (wired.com) - domain field on the page; the author field carries a display name, not a byline. · domain wired.com
- **Reply route:** The request body's address is redacted by Sourcee ('Hit me up at [email redacted]'). The page publishes no link or handle of its own. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Small Business Risk
- **URL:** https://www.sourcee.app/journo-request/small-businesses-aidriven-cyber-risks-and-affordable-protections
- **Posted:** 2d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-14 (3x)
- **Publication:** Samantha J. Subin, CNBC (cnbc.com) - domain and byline on the page. · domain cnbc.com
- **Reply route:** The request body's address is redacted by Sourcee, but the page publishes a Signal handle: ssubin.51. No email and no LinkedIn link on the page. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. Route exists (Signal ssubin.51) but no standing and no on-beat data. NOT DRAFTED.

### [low] AI / Higher Education
- **URL:** https://www.sourcee.app/journo-request/business-schools-ai-applications-in-teaching-and-operations-jan-2027
- **Posted:** 3d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-14 (3x)
- **Publication:** Kevin Anselmo, writing for the American Association of Colleges and Universities (aacu.org) report 'A Framework for Artificial Intelligence in Business Education', led by Tawnya Means. · domain aacu.org
- **Reply route:** Two lnkd.in links on the page: the submission route (lnkd.in/eb-r8aBc) and the current report (lnkd.in/eDD2p8ek). No email address. Links published on the page: https://lnkd.in/eDD2p8ek, https://lnkd.in/eb-r8aBc.  ·  _no — published booking link https://lnkd.in/eDD2p8ek (George)_
- **Links published on the page:** https://lnkd.in/eDD2p8ek, https://lnkd.in/eb-r8aBc
- **Angle:** None. Institutional call, not our standing. NOT DRAFTED.

### [low] AI / Hiring Testimony
- **URL:** https://www.sourcee.app/journo-request/job-candidates-interviewed-by-ai-interview-experience
- **Posted:** 3d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-14 (3x)
- **Publication:** Not named on the page - the author field is a single display name, no publication stated.
- **Reply route:** No address, handle or link published on the request page. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Documentary Sourcing
- **URL:** https://www.sourcee.app/journo-request/nova-scotia-residents-near-ai-data-centre-community-impact
- **Posted:** 3d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-14 (3x)
- **Publication:** Joshua Saunders and Justin White, A Venturesome Production - a documentary team, byline on the page; no publication.
- **Reply route:** The request body's address is redacted by Sourcee ('Please reach out directly or email: [email redacted]'). The page publishes four lnkd.in links, all to the film's own trailer and social accounts - promotion, not a reply route. The request body's address is redacted by Sourcee. Links published on the page: https://lnkd.in/gAMUxgqr, https://lnkd.in/gX86GKjH, https://lnkd.in/ggn7PVx3.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Links published on the page:** https://lnkd.in/gAMUxgqr, https://lnkd.in/gX86GKjH, https://lnkd.in/ggn7PVx3, https://lnkd.in/gnPyZVSB, https://lnkd.in/guChj6UZ
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Enterprise Policy
- **URL:** https://www.sourcee.app/journo-request/indian-cios-founders-investors-and-policymakers-sovereign-ai-challenges
- **Posted:** 3d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-12, last 2026-11-14 (3x)
- **Publication:** Ankit Anand, Express Computer (expresscomputer.in) - domain on the page; the body also signs Srikanth RP, Nivedan Prakash and Sayantan Mondal. · domain expresscomputer.in
- **Reply route:** The body says 'reach out via LinkedIn DM or at [email redacted]'; the address is platform-redacted and no handle of his own is published on the page. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Startup Sourcing
- **URL:** https://www.sourcee.app/journo-request/women-founders-deeptech-startups-biotech-space-ai-robotics
- **Posted:** 3d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-14 (4x)
- **Publication:** YourStory (yourstory.com) - Rekha Balakrishnan, named in the page's author field. · domain yourstory.com
- **Reply route:** The request body's address is redacted by Sourcee. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Consumer
- **URL:** https://www.sourcee.app/journo-request/facebook-marketplace-users-ai-impact-on-buying-and-selling
- **Posted:** 3d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-14 (4x)
- **Publication:** Rainesford Stauffer, freelance journalist, named in the page's author field; no publication stated.
- **Reply route:** The page publishes no address and no link; the body opens with a Bluesky handle (@obicynkenobi.bsky.social), which is a source she was already writing to, not a reply route for us. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Telecom Policy
- **URL:** https://www.sourcee.app/journo-request/telecom-policy-experts-international-telecom-sovereignty-research
- **Posted:** 3d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-14 (4x)
- **Publication:** Dean Bubley, telecom analyst (Disruptive Analysis), named in the page's author field; published as a guest blog for techUK's Cloud and Infrastructure Week. · domain techuk.org
- **Reply route:** One link published on the page: https://lnkd.in/egE8qFYa, a LinkedIn short link to his own article. The page publishes no address. Links published on the page: https://lnkd.in/egE8qFYa.  ·  _no — published booking link https://lnkd.in/egE8qFYa (George)_
- **Links published on the page:** https://lnkd.in/egE8qFYa
- **Angle:** None. No route to the author and no standing on telecom sovereignty. NOT DRAFTED.

### [low] AI / Infrastructure Sourcing
- **URL:** https://www.sourcee.app/journo-request/uk-ai-founders-compute-datacentre-and-grid-constraints
- **Posted:** 4d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-14 (4x)
- **Publication:** Alison Coleman, Forbes senior contributor (entrepreneurs and startups) - named in the page's author field. The page names no publication; the attribution comes from her Forbes byline, which is the same reporter behind the two carried Forbes rows.
- **Reply route:** The request body's address is redacted by Sourcee. Her address is already resolved off her own site for the two carried Forbes calls - alison@alisoncoleman.co.uk, published on alisoncoleman.co.uk/contact-me/ (route-checks-2026-11-14.json: HTTP 200, 28,112 bytes) - and that resolution is NOT used for this row. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: alison@alisoncoleman.co.uk (George sends)_
- **Angle:** None. Deliberately not drafted: no data, no standing, and one pitch per reporter. The two Forbes rows it sits beside are drafted at pitch-drafts-2026-11-11.md section 2.

### [low] AI / Podcast Sourcing
- **URL:** https://www.sourcee.app/journo-request/ai-griefbot-creators-mimicking-deceased-loved-ones-doubletake
- **Posted:** 4d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-14 (4x)
- **Publication:** WORLD (world.wng.org) - 'Doubletake' podcast, host Les Sillars, named in the body.
- **Reply route:** The request body's address is redacted by Sourcee. The page publishes no link. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / PR Request
- **URL:** https://www.sourcee.app/journo-request/uk-recruitment-expert-advice-on-losing-jobs-to-ai
- **Posted:** 4d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-14 (4x)
- **Publication:** Pitch & Shout, a PR request account; no publication named on the page.
- **Reply route:** One link published on the page: https://t.co/U6uparVncd, which the body describes as the pitch route ('Pitch here'). Links published on the page: https://t.co/U6uparVncd.  ·  _unknown — verify the route before sending_
- **Links published on the page:** https://t.co/U6uparVncd
- **Angle:** None. No standing. NOT DRAFTED.

### [low] AI / Consumer
- **URL:** https://www.sourcee.app/journo-request/facebook-marketplace-users-ai-agents-impact-on-feed-spam-and-privacy
- **Posted:** 4d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-14 (4x)
- **Publication:** Rainesford Stauffer, freelance journalist, named in the page's author field; no publication stated.
- **Reply route:** The page publishes no address and no link; 'DMs open' with no handle given. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Labour
- **URL:** https://www.sourcee.app/journo-request/jobseekers-in-ireland-resenting-ai-in-hiring-on-principle
- **Posted:** 4d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-14 (4x)
- **Publication:** Alex Meehan, named in the page's author field; no publication stated.
- **Reply route:** The page publishes no address and no link; 'drop me a message' with no handle given. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Sales Tools
- **URL:** https://www.sourcee.app/journo-request/sales-leaders-and-ai-sales-tool-builders-ai-during-sales-calls
- **Posted:** 4d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-14 (4x)
- **Publication:** Peter O., writing for The Growth Signal, named in the body.
- **Reply route:** The page publishes no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Transformation
- **URL:** https://www.sourcee.app/journo-request/designled-ai-practitioners-where-ai-transformations-stall
- **Posted:** 4d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-14 (4x)
- **Publication:** Sebastian Nause-Blüml, writing a public fieldnotes guide; named in the post.
- **Reply route:** The page publishes no address and no link; asks people to tag or message him. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Security Governance
- **URL:** https://www.sourcee.app/journo-request/cybersecurity-founder-and-ciso-ai-infra-ceo-scandal-risk-and-governance
- **Posted:** 4d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-11, last 2026-11-14 (4x)
- **Publication:** Times Internet (timesinternet.in) - Vaishnavi D., named in the page's author field. · domain timesinternet.in
- **Reply route:** The request body's address is redacted by Sourcee; the page publishes no link. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Podcast booking
- **URL:** https://www.sourcee.app/journo-request/podcasters-and-linkedin-live-creators-tech-and-ai-and-career-topics
- **Posted:** 6d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-09, last 2026-11-14 (6x)
- **Publication:** Nashpunk Forge (nashpunkforge.com) - no reporter named; the call is a booking sheet for podcast and LinkedIn Live guests. · domain nashpunkforge.com
- **Reply route:** Page says 'DM me or reach out in the comments'; email is platform-redacted ([email redacted]) and no LinkedIn handle or profile URL is published. No resolvable route. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing as a podcast guest. NOT DRAFTED.

### [low] AI / Content Submission (not a press request)
- **URL:** https://www.sourcee.app/journo-request/human-behind-ai-crypto-agent-agentwritten-crypto-blogs
- **Posted:** 7d old (page datePublished (page probed 2026-11-14)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-07, last 2026-11-14 (8x)
- **Publication:** CryptoBloggers - a crypto blog network soliciting agent-written posts; no reporter or outlet masthead named
- **Reply route:** The body publishes only a t.co shortlink (https://t.co/KZyXLXRgYP) and no address or handle. NOT a reply route for us. Links published on the page: https://t.co/KZyXLXRgYP.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/KZyXLXRgYP
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Social and Workplace Tension
- **URL:** https://www.sourcee.app/journo-request/people-with-friends-and-coworkers-who-disagree-on-ai-managing-tension
- **Posted:** 8d old (page datePublished unparseable (cached age)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-06, last 2026-11-14 (9x)
- **Publication:** CNBC Make It - reporter not named on the page; page domain cnbc.com · domain cnbc.com
- **Reply route:** The body asks for a DM or an email and redacts the address ('please DM or email me ([email redacted])'). No handle, address or link is published on the page and none was resolved off cnbc.com. NOT RESOLVED as a route. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No standing and no route. NOT DRAFTED.

### [low] AI / Jobs and Displacement
- **URL:** https://www.sourcee.app/journo-request/woman-replaced-by-ai-and-recruitment-expert-ai-job-loss-case-study
- **Posted:** 8d old (page datePublished (page probed 2026-11-14)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-07, last 2026-11-14 (8x)
- **Publication:** A weekly magazine - reporter, title and publication not named on the page; page domain not exposed
- **Reply route:** The body says 'Please email me on [email redacted]' - Sourcee redacts it, and the page publishes no handle, link or publication site to resolve it from. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Podcast Guest Booking
- **URL:** https://www.sourcee.app/journo-request/ai-founders-and-investors-in-barcelona-podcast-and-company-visit-guests
- **Posted:** 8d old (page datePublished (page probed 2026-11-14)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-07, last 2026-11-14 (8x)
- **Publication:** AI & Business Club at EADA Business School, Barcelona - podcast and company-visit programming; no reporter named
- **Reply route:** The body asks readers to 'DM me' or comment; no handle is published and Sourcee redacts nothing because there is no address in the body. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] B2B Sales / Deal Stories
- **URL:** https://www.sourcee.app/journo-request/b2b-tech-and-software-sales-reps-and-leaders-real-customer-deal-lessons
- **Posted:** 8d old (page datePublished (page probed 2026-11-14)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-07, last 2026-11-14 (8x)
- **Publication:** The Follow Up - a newsletter for B2B sales professionals (40,000+ subscribers per the body); writer not named
- **Reply route:** The body says 'send me a DM or comment below'; no address, handle or newsletter URL is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] Not a source request - celebrity booking
- **URL:** https://www.sourcee.app/journo-request/prs-and-agents-celebrities-national-titles-interview-slots
- **Posted:** 8d old (page datePublished (page probed 2026-11-14)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-07, last 2026-11-14 (8x)
- **Publication:** Not named on the page - a #journorequest for celebrity interviews across national titles
- **Reply route:** The body says 'DM me'; no handle, address or outlet is published. NOT a reply route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Consumer Behaviour
- **URL:** https://www.sourcee.app/journo-request/ai-users-and-relationship-therapists-dating-conflicts-breakups
- **Posted:** 8d old (page datePublished (page probed 2026-11-14)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-07, last 2026-11-14 (8x)
- **Publication:** Not named on the page; a feature on AI in romantic relationships, no outlet or byline
- **Reply route:** The body asks for a 'DM me'; no address, handle or link is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] Academia / Writing Process
- **URL:** https://www.sourcee.app/journo-request/doctoral-candidates-and-phd-holders-dissertation-writing-strategies
- **Posted:** 9d old (page datePublished (page probed 2026-11-14)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-06, last 2026-11-14 (9x)
- **Publication:** A doctoral mentor and dissertation editor (individual call, not a publication); no outlet named
- **Reply route:** The page publishes no address, handle or link of its own, and says 'invite' without a route. NOT RESOLVED as a route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No standing and no route. NOT DRAFTED.

### [low] Future of Work / Early-Career Research
- **URL:** https://www.sourcee.app/journo-request/early-career-workers-future-of-work-and-ai
- **Posted:** 9d old (page datePublished (page probed 2026-11-14)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-06, last 2026-11-14 (9x)
- **Publication:** The Future Collective, with Henley Business School - research report; no named reporter
- **Reply route:** Asks early-career workers to volunteer for a one-hour interview; no address, handle or form is published on the page. NOT RESOLVED as a route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No standing and no route. NOT DRAFTED.

### [low] Not a source request - directory submission
- **URL:** https://www.sourcee.app/journo-request/ai-and-virtual-influencer-creators-index-submission
- **Posted:** 9d old (page datePublished (page probed 2026-11-14)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-06, last 2026-11-14 (9x)
- **Publication:** An AI/virtual-influencer index; no publication or reporter named
- **Reply route:** A t.co shortlink is the only route; the page publishes no address or handle. NOT a reply route for a pitch. Links published on the page: https://t.co/xpRPRwr5RU.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/xpRPRwr5RU
- **Angle:** None. Not a source request. NOT DRAFTED.

### [low] PropTech / Real-Estate Cybersecurity
- **URL:** https://www.sourcee.app/journo-request/nar-nxt-safety-and-cybersecurity-experts-gen-ai-cybersecurity
- **Posted:** 9d old (page datePublished (page probed 2026-11-14)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-06, last 2026-11-14 (9x)
- **Publication:** Tracey 'the Safety Lady' Hawkins for REALTOR Magazine (magazine.realtor); covering NAR NXT in New Orleans · domain magazine.realtor
- **Reply route:** The body says 'Comment below, send me a message, or email [email redacted]' - the address is redacted and no handle or link is published on the page. NOT RESOLVED as a route. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No standing, no route, and the event window is now. NOT DRAFTED.

### [low] AI Policy / Regulation
- **URL:** https://www.sourcee.app/journo-request/ai-policy-expert-possible-pause-on-ai-in-us
- **Posted:** 9d old (page datePublished (page probed 2026-11-14)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-06, last 2026-11-14 (9x)
- **Publication:** Daily Mail (dailymail.co.uk) - reporter not named on the page · domain dailymail.co.uk
- **Reply route:** The body says 'DM me or email me: [email redacted]'. No handle or address is published on the page and none was resolved off dailymail.co.uk. NOT RESOLVED as a route. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No standing and no route. NOT DRAFTED.

### [low] Not AI - citizenship debate
- **URL:** https://www.sourcee.app/journo-request/postcolonial-scholars-and-former-coloniser-officials-citizenship-debate
- **Posted:** 9d old (page datePublished (page probed 2026-11-14)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-06, last 2026-11-14 (9x)
- **Publication:** Business Spotlight / ZEIT SPRACHEN - Head-to-Head debate feature
- **Reply route:** A lnkd.in shortlink is published; no address or handle. NOT a route to a pitch we could send. Links published on the page: https://lnkd.in/eNwsNMwi.  ·  _no — published booking link https://lnkd.in/eNwsNMwi (George)_
- **Links published on the page:** https://lnkd.in/eNwsNMwi
- **Angle:** None. Off-beat. NOT DRAFTED.

### [low] Not AI - handwriting in business
- **URL:** https://www.sourcee.app/journo-request/business-leaders-and-educators-headtohead-handwriting-in-business
- **Posted:** 9d old (page datePublished (page probed 2026-11-14)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-06, last 2026-11-14 (9x)
- **Publication:** Business Spotlight / ZEIT SPRACHEN - Head-to-Head debate feature
- **Reply route:** A lnkd.in shortlink is published; no address or handle. NOT a route to a pitch we could send. Links published on the page: https://lnkd.in/eBz-gM_d.  ·  _no — published booking link https://lnkd.in/eBz-gM_d (George)_
- **Links published on the page:** https://lnkd.in/eBz-gM_d
- **Angle:** None. Off-beat. NOT DRAFTED.

### [low] AI Infrastructure / Regulation Debate
- **URL:** https://www.sourcee.app/journo-request/data-center-workers-and-ai-execs-ban-ai-expansion-until-safety-rules
- **Posted:** 9d old (page datePublished (page probed 2026-11-14)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-06, last 2026-11-14 (9x)
- **Publication:** Business Spotlight / ZEIT SPRACHEN - Head-to-Head debate feature; no reporter named
- **Reply route:** The page publishes a lnkd.in shortlink to the poster's Qwoted profile plus 'drop me a DM'. No address or handle is readable from this end. NOT RESOLVED as a route. Links published on the page: https://lnkd.in/eCYXvMnw.  ·  _no — published booking link https://lnkd.in/eCYXvMnw (George)_
- **Links published on the page:** https://lnkd.in/eCYXvMnw
- **Angle:** None. No standing and no usable route. NOT DRAFTED.

### [low] AI / Developer Security and Supply Chain
- **URL:** https://www.sourcee.app/journo-request/cisos-and-senior-cybersecurity-leaders-protecting-developers
- **Posted:** 9d old (page datePublished (page probed 2026-11-14)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-06, last 2026-11-14 (9x)
- **Publication:** The Stack (thestack.co) - security title; reporter not named on the page · domain thestack.co
- **Reply route:** The body asks security leaders how they protect developers, and publishes no address, handle or link of its own. NOT RESOLVED as a route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. Off-ask and routeless. NOT DRAFTED.

### [low] AI / Design / Podcast
- **URL:** https://www.sourcee.app/journo-request/designers-and-creators-balancing-bills-family-and-meaningful-work
- **Posted:** 9d old (page datePublished (page probed 2026-11-14)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-05, last 2026-11-14 (10x)
- **Publication:** Tommy Geoco (no publication domain on the page); recording a podcast episode with @ridd_design.
- **Reply route:** No address, handle or link on the page; asks listeners to reply to the post. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. NOT DRAFTED.

### [low] AI / UK Labour Market
- **URL:** https://www.sourcee.app/journo-request/uk-job-hunters-12-months-job-market-climate-and-ai
- **Posted:** 9d old (page datePublished (page probed 2026-11-14)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-05, last 2026-11-14 (10x)
- **Publication:** Fatima O (no publication domain on the page).
- **Reply route:** No address, handle or link; hashtag-only post. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. NOT DRAFTED.

### [low] AI / False Accusations / Testimony
- **URL:** https://www.sourcee.app/journo-request/freelancers-small-businesses-and-employees-falsely-accused-of-ai-use
- **Posted:** 10d old (page datePublished unparseable (cached age)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-05, last 2026-11-14 (10x)
- **Publication:** Suzanne Bearne, freelance journalist writing from Berlin (no publication domain on the page; she is a regular byline in UK national titles).
- **Reply route:** No address or link; 'DMs are open' on the platform, which is the only route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. NOT DRAFTED.

### [low] AI / Retail Work / Businessweek Column
- **URL:** https://www.sourcee.app/journo-request/retail-workers-and-managers-instore-ai-impact-holiday-season
- **Posted:** 10d old (page datePublished unparseable (cached age)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-05, last 2026-11-14 (10x)
- **Publication:** Issie Lapowsky, Bloomberg Businessweek columnist (page domain bloomberg.com). · domain bloomberg.com
- **Reply route:** Body redacts the email ('[email redacted]') and gives Signal 'issielapowsky.08'. The page publishes no address. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. The ask excludes us by its own words. NOT DRAFTED.

## Cold — only if you have a reason

Older than the 10-day line and never pitched. Not provably abandoned — no renewal signal exists on this source — but every one of these has already passed an ideal send window.

- [high] 65d old — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [high] 68d old — https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
- [high] 70d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-ai-governance-and-agent-sprawl
- [high] 71d old — https://www.sourcee.app/journo-request/scientists-phd-students-and-postdocs-paying-for-ai-subscriptions
- [high] 116d old — https://www.sourcee.app/journo-request/business-and-technology-leaders-tech-budget-priorities-amid-volatility
- [high] 196d old — https://www.sourcee.app/journo-request/anthropic-api-users-costs-and-token-burn-increase-since-january
- [medium-high] 64d old — https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
- [medium-high] 65d old — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium-high] 68d old — https://www.sourcee.app/journo-request/uk-managers-cracked-down-on-gen-z-ai-overuse
- [medium] 17d old — https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
- [medium] 18d old — https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
- [medium] 18d old — https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact
- [medium] 40d old — https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
- [medium] 64d old — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [medium] 68d old — https://www.sourcee.app/journo-request/ai-startups-workplace-fraud-detection-expenses-time-theft
- [medium] 68d old — https://www.sourcee.app/journo-request/ai-agents-making-money-2026-sales-and-leadgen-workflow-ops
- [medium] 68d old — https://www.sourcee.app/journo-request/marketing-and-content-leaders-aiassisted-work-review-process
- [medium] 72d old — https://www.sourcee.app/journo-request/ceos-ai-impact-on-ops-culture-and-commercial-strategy
- [medium] 82d old — https://www.sourcee.app/journo-request/uk-finance-risk-and-regulatory-leaders-ai-explainability-risks
- [medium] 249d old — https://www.sourcee.app/journo-request/sme-owners-operational-challenges-for-ai-solutions-case-study
- [low-medium] 22d old — https://www.sourcee.app/journo-request/claude-users-anthropic-public-benefit-fund-trust-and-job-impact
- [low-medium] 32d old — https://www.sourcee.app/journo-request/b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research
- [low-medium] 35d old — https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
- [low-medium] 39d old — https://www.sourcee.app/journo-request/uk-companies-implementing-ai-how-automation-transforms-workdays
- [low-medium] 43d old — https://www.sourcee.app/journo-request/law-firm-lawyers-concrete-ai-implementations-and-billing-impact
- [low-medium] 44d old — https://www.sourcee.app/journo-request/employees-conflicted-about-ai-use-generative-ai-workplace-impact
- [low-medium] 46d old — https://www.sourcee.app/journo-request/insurance-agents-ai-use-in-personal-lines
- [medium-low] 56d old — https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business
- [low-medium] 59d old — https://www.sourcee.app/journo-request/us-founders-calls-to-slow-ai-development-impact-on-companies
- [medium-low] 65d old — https://www.sourcee.app/journo-request/tech-policy-experts-california-ai-audit-bills-impact-cios
- [low-medium] 84d old — https://www.sourcee.app/journo-request/ai-project-builders-youtube-finance-and-lifestyle-channel-feature
- [low-medium] 129d old — https://www.sourcee.app/journo-request/prompt-engineers-tokenmaxxing-anecdotes
- [low] 10d old — https://www.sourcee.app/journo-request/ai-data-center-operators-midterm-vote-backlash-impact
- [low] 10d old — https://www.sourcee.app/journo-request/canadian-real-estate-agents-foreign-buyer-ban-ending-jan-1-2027
- [low] 10d old — https://www.sourcee.app/journo-request/anthropic-employees-company-decisionmaking-and-workplace-impact
- [low] 10d old — https://www.sourcee.app/journo-request/ai-policy-experts-tech-influence-on-midterms-tonight
- [low] 10d old — https://www.sourcee.app/journo-request/generative-ai-documentation-experts-business-document-fraud-risk
- [low] 11d old — https://www.sourcee.app/journo-request/founders-selling-to-nurses-nurse-adoption-and-clinical-ai
- [low] 11d old — https://www.sourcee.app/journo-request/newsletter-publishers-and-creators-state-of-newsletters-report-2027
- [low] 11d old — https://www.sourcee.app/journo-request/dallas-insurance-executives-private-capital-ai-rbc-reforms
- [low] 11d old — https://www.sourcee.app/journo-request/job-seekers-in-ireland-aiautomated-job-applications-experience
- [low] 11d old — https://www.sourcee.app/journo-request/biometrics-and-computer-vision-experts-proving-humanity-in-digital-age
- [low] 11d old — https://www.sourcee.app/journo-request/retail-executives-nrf-nyc-retail-media-supply-chain-and-ai
- [low] 11d old — https://www.sourcee.app/journo-request/regulators-and-compliance-experts-consumer-ai-mental-wellbeing
- [low] 11d old — https://www.sourcee.app/journo-request/carleton-students-ai-use-in-dating-advice
- [low] 11d old — https://www.sourcee.app/journo-request/aussie-travellers-1861-hotel-tech-abandoned-bookings-and-ai-concerns
- [low] 11d old — https://www.sourcee.app/journo-request/young-adults-1835-ai-impact-on-comingofage
- [low] 11d old — https://www.sourcee.app/journo-request/people-with-ai-psychosis-firsthand-accounts
- [low] 11d old — https://www.sourcee.app/journo-request/new-authors-ai-market-dilution-and-fair-use-impact-on-writing
- [low] 11d old — https://www.sourcee.app/journo-request/marketers-and-creators-using-ai-agents-timesaving-wins
- [low] 11d old — https://www.sourcee.app/journo-request/ut-austin-students-ai-trump-crypto-ads-on-game-livestreams
- [low] 11d old — https://www.sourcee.app/journo-request/freelance-journalists-automation-feature-pitches
- [low] 11d old — https://www.sourcee.app/journo-request/designers-on-large-teams-evolving-design-systems-dive-radio
- [low] 11d old — https://www.sourcee.app/journo-request/former-muse-users-gave-up-on-ai-agents
- [low] 11d old — https://www.sourcee.app/journo-request/world-model-researchers-applications-in-robotics
- [low] 12d old — https://www.sourcee.app/journo-request/global-and-european-marketing-leaders-investment-and-ops-challenges
- [low] 12d old — https://www.sourcee.app/journo-request/uk-recruiters-ai-impact-on-billing-and-candidate-matching
- [low] 15d old — https://www.sourcee.app/journo-request/startup-founders-deciding-first-marketing-tests-on-tight-runway
- [low] 15d old — https://www.sourcee.app/journo-request/multifamily-professionals-ai-adoption-and-employee-chatbot-use
- [low] 15d old — https://www.sourcee.app/journo-request/canadian-ai-and-tech-companies-government-picking-winners-and-losers
- [low] 15d old — https://www.sourcee.app/journo-request/midlife-professionals-career-regret
- [low] 15d old — https://www.sourcee.app/journo-request/bank-and-brokerage-users-ai-tools-managing-personal-finances
- [low] 16d old — https://www.sourcee.app/journo-request/rig-hse-staff-aienabled-cameras-trial-outcomes
- [low] 16d old — https://www.sourcee.app/journo-request/current-ucla-students-and-faculty-ai-impact-on-majors
- [low] 16d old — https://www.sourcee.app/journo-request/founders-and-inclusion-leads-future-of-work-and-ai-impact
- [low] 16d old — https://www.sourcee.app/journo-request/uk-law-experts-and-ai-safety-researchers-chatbotaided-crime
- [low] 16d old — https://www.sourcee.app/journo-request/buyers-and-sellers-without-agents-diy-property-sale-experience
- [low] 16d old — https://www.sourcee.app/journo-request/editors-creatives-and-graphic-designers-ai-impact-documentary
- [low] 16d old — https://www.sourcee.app/journo-request/character-ai-users-emotional-attachment-and-loneliness
- [low] 17d old — https://www.sourcee.app/journo-request/ai-researchers-founders-and-tech-ceos-retirement-plans-amid-ai-risk
- [low] 17d old — https://www.sourcee.app/journo-request/canadian-skilled-trades-workers-ai-impact-on-manufacturing
- [low] 17d old — https://www.sourcee.app/journo-request/gcc-founders-and-entrepreneurs-ai-collaboration-and-data-sovereignty
- [low] 17d old — https://www.sourcee.app/journo-request/dairy-companies-and-startups-aipowered-livestock-health-and-nutrition
- [low] 17d old — https://www.sourcee.app/journo-request/users-who-linked-bank-and-brokerage-accounts-to-llms-ai-finance
- [low] 17d old — https://www.sourcee.app/journo-request/literary-writers-thoughts-on-lit-mags-funny-deep-frustrated
- [low] 17d old — https://www.sourcee.app/journo-request/musicians-artists-writers-and-creators-ai-impact-on-creativity
- [low] 18d old — https://www.sourcee.app/journo-request/ai-startup-founders-and-marketers-b2b-marketing-as-show-business
- [low] 18d old — https://www.sourcee.app/journo-request/students-whose-professors-allow-ai-ai-use-in-coursework
- [low] 18d old — https://www.sourcee.app/journo-request/carleton-students-ai-dating-advice-impact-on-dating-experience
- [low] 18d old — https://www.sourcee.app/journo-request/former-software-engineers-turned-traders-pivot-after-layoff-or-ai
- [low] 18d old — https://www.sourcee.app/journo-request/members-club-and-hospitality-pros-in-hong-kong-postcovid-trends
- [low] 18d old — https://www.sourcee.app/journo-request/canadian-health-innovators-voices-of-innovation-canada-nov-16
- [low] 18d old — https://www.sourcee.app/journo-request/excorporate-privacy-lead-built-privacy-and-ai-consultancy
- [low] 19d old — https://www.sourcee.app/journo-request/admissions-leaders-and-researchers-measuring-judgment-amid-ai
- [low] 19d old — https://www.sourcee.app/journo-request/celebrity-agents-how-i-manage-my-money-series
- [low] 19d old — https://www.sourcee.app/journo-request/ai-companies-in-utilities-and-construction-frontline-safety-and-workload
- [low] 19d old — https://www.sourcee.app/journo-request/people-using-llms-as-companions-emotional-support-stories
- [low] 19d old — https://www.sourcee.app/journo-request/sound-artists-and-field-recordists-run-radio-aarhus-open-call
- [low] 21d old — https://www.sourcee.app/journo-request/people-using-ai-for-social-advice-communication-and-connection-impact
- [low] 21d old — https://www.sourcee.app/journo-request/video-teams-using-claude-and-remotion-agentic-video-editing
- [low] 22d old — https://www.sourcee.app/journo-request/uk-and-eu-sports-retail-supply-chain-leaders-retail-ai-at-scale
- [low] 22d old — https://www.sourcee.app/journo-request/founders-and-cofounders-fortnightly-founder-qanda
- [low] 22d old — https://www.sourcee.app/journo-request/fanvue-chatters-nsfw-ai-model-experiences
- [low] 22d old — https://www.sourcee.app/journo-request/couples-letting-ai-dictate-relationship-emotions-and-intimacy
- [low] 22d old — https://www.sourcee.app/journo-request/parish-event-organizers-aigenerated-flyers-scourge-or-timesaver
- [low] 22d old — https://www.sourcee.app/journo-request/people-recreating-iconic-runway-looks-halloween-costume-story
- [low] 23d old — https://www.sourcee.app/journo-request/nontech-inhouse-corporate-comms-lead-ai-search-and-discovery-strategy
- [low] 23d old — https://www.sourcee.app/journo-request/founders-and-ctos-production-ai-tradeoffs-in-healthcare-and-fintech
- [low] 23d old — https://www.sourcee.app/journo-request/students-and-professionals-balancing-ai-use-and-human-focus
- [low] 23d old — https://www.sourcee.app/journo-request/rig-hse-officers-aienabled-camera-trial-outcomes
- [low] 23d old — https://www.sourcee.app/journo-request/anthropic-project-panama-employees-book-digitization-and-ai-training
- [low] 23d old — https://www.sourcee.app/journo-request/nj-parents-and-teachers-ai-school-surveillance-and-data-practices
- [low] 23d old — https://www.sourcee.app/journo-request/digital-artists-aigenerated-posters-flooding-social-feeds
- [low] 23d old — https://www.sourcee.app/journo-request/geopolitical-analysts-and-ai-security-experts-global-hotspots
- [low] 24d old — https://www.sourcee.app/journo-request/omaha-hr-representatives-offices-with-written-ai-policies
- [low] 24d old — https://www.sourcee.app/journo-request/bengaluru-founders-deep-tech-healthcare-biology-housing-and-ai
- [low] 24d old — https://www.sourcee.app/journo-request/fintech-product-managers-nextgen-aipowered-personal-finance-apps
- [low] 24d old — https://www.sourcee.app/journo-request/brand-managers-ai-to-deepen-customer-insight-and-preserve-humanity
- [low] 25d old — https://www.sourcee.app/journo-request/cios-at-gartner-it-symposium-orlando-balancing-ai-risk-and-value
- [low] 25d old — https://www.sourcee.app/journo-request/estate-agents-and-property-lawyers-disclosure-rules-haunted-homes
- [low] 25d old — https://www.sourcee.app/journo-request/product-managers-on-512-engineer-teams-engineers-using-ai
- [low] 25d old — https://www.sourcee.app/journo-request/bay-area-agentic-ai-builders-agntcon-and-mcpcon-stories
- [low] 25d old — https://www.sourcee.app/journo-request/carleton-students-ai-impact-on-dating-experiences
- [low] 25d old — https://www.sourcee.app/journo-request/new-yorkers-ai-music-playing-in-cabs-and-local-businesses
- [low] 25d old — https://www.sourcee.app/journo-request/western-students-using-ai-companions-psychological-effects
- [low] 25d old — https://www.sourcee.app/journo-request/hr-leaders-and-organizational-design-practitioners-decision-fatigue
- [low] 26d old — https://www.sourcee.app/journo-request/consumers-using-ai-for-financial-advice-experience-and-factchecking
- [low] 26d old — https://www.sourcee.app/journo-request/ai-energy-and-tax-experts-project-jupiter-documentary-new-mexico
- [low] 26d old — https://www.sourcee.app/journo-request/fb-marketplace-sellers-and-buyers-ai-impact-on-pricing-and-listings
- [low] 27d old — https://www.sourcee.app/journo-request/uk-customer-service-workers-daytoday-now-ai-automation-vs-human
- [low] 28d old — https://www.sourcee.app/journo-request/memphis-and-southaven-residents-and-env-advocates-xai-colossus-impact
- [low] 28d old — https://www.sourcee.app/journo-request/black-women-in-canada-ai-chatbots-and-healthcare-experiences
- [low] 28d old — https://www.sourcee.app/journo-request/engineering-leaders-leading-people-through-ai-changes
- [low] 28d old — https://www.sourcee.app/journo-request/ai-app-and-saas-founders-1k-mrr-youtube-feature-growth-tactics
- [low] 28d old — https://www.sourcee.app/journo-request/ai-saas-vendors-targeting-journalists-prs-and-marketers-case-studies
- [low] 28d old — https://www.sourcee.app/journo-request/real-estate-operators-ai-adoption-and-org-restructuring
- [low] 29d old — https://www.sourcee.app/journo-request/chemistry-undergrads-and-phd-students-ai-use-in-coursework-and-research
- [low] 29d old — https://www.sourcee.app/journo-request/ai-infrastructure-engineers-in-berlin-data-centers-and-bottlenecks
- [low] 29d old — https://www.sourcee.app/journo-request/residents-near-mumbai-ai-data-centres-power-and-water-strain
- [low] 29d old — https://www.sourcee.app/journo-request/single-family-office-cybersecurity-experts-ai-risks-and-opportunities
- [low] 30d old — https://www.sourcee.app/journo-request/companies-and-data-buyers-selling-corporate-data-to-train-ai
- [low] 30d old — https://www.sourcee.app/journo-request/uk-political-analysts-disinformation-and-ai-manipulation-in-politics
- [low] 30d old — https://www.sourcee.app/journo-request/cios-and-ai-leaders-ai-infrastructure-day2-ops-and-costs
- [low] 30d old — https://www.sourcee.app/journo-request/content-creators-using-ai-job-losses-and-ethics
- [low] 30d old — https://www.sourcee.app/journo-request/painters-and-photographers-ai-impact-on-art
- [low] 30d old — https://www.sourcee.app/journo-request/legal-assistants-paralegals-and-lawfirm-staff-jobs-eliminated-by-ai
- [low] 30d old — https://www.sourcee.app/journo-request/ai-companion-users-in-africa-friendship-and-emotional-impact
- [low] 30d old — https://www.sourcee.app/journo-request/pro-se-litigants-using-generative-ai-access-to-justice-impact
- [low] 31d old — https://www.sourcee.app/journo-request/uk-and-us-heads-of-data-and-ai-from-idea-to-production
- [low] 31d old — https://www.sourcee.app/journo-request/minnesotans-using-chatgpt-and-ai-tools-experiences-with-election-info
- [low] 31d old — https://www.sourcee.app/journo-request/school-leaders-and-ngo-staff-ai-adoption-challenges-across-sectors
- [low] 31d old — https://www.sourcee.app/journo-request/ai-policy-advisor-newsom-administration-ai-regulation
- [low] 32d old — https://www.sourcee.app/journo-request/podcast-guests-ai-channel-and-partner-ecosystem
- [low] 32d old — https://www.sourcee.app/journo-request/african-founders-building-ai-companies-pitch-deck-realities
- [low] 32d old — https://www.sourcee.app/journo-request/higher-ed-nonfaculty-staff-ai-use-at-work
- [low] 32d old — https://www.sourcee.app/journo-request/ai-infrastructure-professionals-in-london-capacity-europe-attendees
- [low] 32d old — https://www.sourcee.app/journo-request/b2b-vendors-buyers-pasting-proposals-into-ai-tools
- [low] 32d old — https://www.sourcee.app/journo-request/global-development-professionals-using-ai-across-programs-and-policy
- [low] 33d old — https://www.sourcee.app/journo-request/caine-prize-winners-gen-ai-accusations-targeting-black-writers
- [low] 33d old — https://www.sourcee.app/journo-request/software-engineers-who-left-tech-jobs-lost-to-ai-coding-tools
- [low] 33d old — https://www.sourcee.app/journo-request/manufacturers-and-ai-safety-experts-ai-risks-in-chemical-food-defense
- [low] 33d old — https://www.sourcee.app/journo-request/uk-baby-boomers-misinformation-sharing-and-ai-influence-online
- [low] 34d old — https://www.sourcee.app/journo-request/hedera-builders-shipping-defi-nfts-rwas-ai-games-and-memes
- [low] 34d old — https://www.sourcee.app/journo-request/production-designers-ai-impact-on-future-of-filmmaking
- [low] 34d old — https://www.sourcee.app/journo-request/ai-researchers-and-policy-experts-5-years-us-race-to-superintelligence
- [low] 35d old — https://www.sourcee.app/journo-request/employees-pay-transparency-good-or-bad
- [low] 35d old — https://www.sourcee.app/journo-request/ai-cybersecurity-iot-and-web3-founders-and-operators-news-submissions
- [low] 36d old — https://www.sourcee.app/journo-request/anthropic-gtm-leaders-scaling-300k-b2b-clients
- [low] 36d old — https://www.sourcee.app/journo-request/sales-reps-who-cold-call-and-email-how-ai-changed-outreach
- [low] 36d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-and-builders-realworld-deployment-and-strategy
- [low] 37d old — https://www.sourcee.app/journo-request/voters-who-used-ai-to-navigate-ballot-voting-experience
- [low] 37d old — https://www.sourcee.app/journo-request/hotel-and-fandb-supervisors-and-managers-customer-expectations-vs-ai
- [low] 37d old — https://www.sourcee.app/journo-request/researchers-founders-and-funders-ai-transforming-scientific-research
- [low] 37d old — https://www.sourcee.app/journo-request/facebook-marketplace-sellers-ai-listing-photos-and-selling-experience
- [low] 37d old — https://www.sourcee.app/journo-request/uk-ai-data-trainers-daytoday-work
- [low] 37d old — https://www.sourcee.app/journo-request/patent-attorneys-and-agents-startup-ip-starter-pack
- [low] 38d old — https://www.sourcee.app/journo-request/apac-reporters-and-editors-ai-accountability-coverage
- [low] 38d old — https://www.sourcee.app/journo-request/early-to-midcareer-information-architects-products-featuring-ai
- [low] 38d old — https://www.sourcee.app/journo-request/solicitors-and-barristers-ai-to-expand-pro-bono-capacity
- [low] 38d old — https://www.sourcee.app/journo-request/martech-buyers-ai-impact-on-build-vs-buy-decisions
- [low] 38d old — https://www.sourcee.app/journo-request/aps-hr-leaders-ai-skills-training-and-workforce-planning
- [low] 38d old — https://www.sourcee.app/journo-request/scrum-masters-daytoday-and-career-pivots-and-ai-impact
- [low] 38d old — https://www.sourcee.app/journo-request/swiss-ai-companion-users-emotional-bonds-and-daily-life
- [low] 38d old — https://www.sourcee.app/journo-request/ai-data-labelers-in-germany-positive-and-negative-experiences
- [low] 38d old — https://www.sourcee.app/journo-request/ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories
- [low] 38d old — https://www.sourcee.app/journo-request/real-estate-agents-replacing-pdf-property-brochure
- [low] 38d old — https://www.sourcee.app/journo-request/anz-marketers-ai-and-martech-innovation-spotlight
- [low] 39d old — https://www.sourcee.app/journo-request/ai-data-annotators-and-labellers-experience-with-ai-training-data
- [low] 39d old — https://www.sourcee.app/journo-request/academics-social-media-and-ai-impact-on-womens-identity-and-selfesteem
- [low] 39d old — https://www.sourcee.app/journo-request/emergency-managers-ai-tools-for-funding-and-staffing-shortfalls
- [low] 39d old — https://www.sourcee.app/journo-request/plaintiffs-attorneys-and-legal-scholars-ai-deepfake-liability
- [low] 39d old — https://www.sourcee.app/journo-request/ai-infrastructure-experts-china-vs-us-datacenter-capacity
- [low] 39d old — https://www.sourcee.app/journo-request/coweta-county-artists-and-creatives-data-centers-and-ai-infrastructure
- [low] 40d old — https://www.sourcee.app/journo-request/ai-liability-insurers-and-legal-experts-procurement-and-implementation
- [low] 40d old — https://www.sourcee.app/journo-request/uk-cybersecurity-hiring-managers-state-of-hiring-2026-and-ai-impact
- [low] 40d old — https://www.sourcee.app/journo-request/ai-emotional-support-users-chatbot-therapy-and-journaling
- [low] 40d old — https://www.sourcee.app/journo-request/mortgage-adviser-using-ai-efficiency-and-client-outcomes-video-series
- [low] 40d old — https://www.sourcee.app/journo-request/founders-and-cxos-in-automotive-ai-evs-autonomy-thought-leadership
- [low] 41d old — https://www.sourcee.app/journo-request/video-game-developer-falsely-accused-of-using-generative-ai
- [low] 42d old — https://www.sourcee.app/journo-request/lawyers-and-tech-ethics-experts-ai-wearables-and-legal-journeys
- [low] 43d old — https://www.sourcee.app/journo-request/mls-executives-risks-when-agents-grant-mls-access-to-llms
- [low] 43d old — https://www.sourcee.app/journo-request/real-estate-agents-and-brokers-switched-from-pdf-brochures
- [low] 43d old — https://www.sourcee.app/journo-request/advertising-tech-and-media-pros-in-miami-ai-audience-discovery
- [low] 43d old — https://www.sourcee.app/journo-request/hr-leaders-company-ai-strategies-and-cognitive-offloading-risk
- [low] 43d old — https://www.sourcee.app/journo-request/k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact
- [low] 43d old — https://www.sourcee.app/journo-request/storytellers-and-brand-founders-marys-big-30-ai-story-project
- [low] 43d old — https://www.sourcee.app/journo-request/newsletter-editors-using-ai-agents-news-aggregation-practices
- [low] 43d old — https://www.sourcee.app/journo-request/scottish-teachers-ai-tools-implementation-in-education
- [low] 44d old — https://www.sourcee.app/journo-request/ai-summit-barcelona-attendees-controversy-and-experiences
- [low] 44d old — https://www.sourcee.app/journo-request/fb-marketplace-sellers-ai-photos-and-description-prompts
- [low] 44d old — https://www.sourcee.app/journo-request/ai-glasses-owners-users-and-developers-in-india-product-experience
- [low] 44d old — https://www.sourcee.app/journo-request/fea-engineers-using-agentic-ai-practitioner-case-study
- [low] 44d old — https://www.sourcee.app/journo-request/parents-ai-acting-as-pseudoparent-in-kid-questions
- [low] 45d old — https://www.sourcee.app/journo-request/chatbot-users-experiences-talking-to-ai
- [low] 45d old — https://www.sourcee.app/journo-request/us-ai-security-experts-rogue-ai-agents-hitting-government-sites
- [low] 45d old — https://www.sourcee.app/journo-request/real-estate-agents-pdf-brochures-vs-alternatives-agent-workflow
- [low] 46d old — https://www.sourcee.app/journo-request/cybersecurity-expert-ai-nexus-and-security-risks
- [low] 46d old — https://www.sourcee.app/journo-request/us-emergency-physicians-and-paramedics-impact-of-ai-answering-911-calls
- [low] 46d old — https://www.sourcee.app/journo-request/job-seekers-and-recruiters-ai-recruitment-experiences
- [low] 47d old — https://www.sourcee.app/journo-request/data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity
- [low] 47d old — https://www.sourcee.app/journo-request/b2b-marketing-leaders-hyperspecialization-to-outcompete-ai
- [low] 47d old — https://www.sourcee.app/journo-request/ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes
- [low] 53d old — https://www.sourcee.app/journo-request/ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai
- [low] 53d old — https://www.sourcee.app/journo-request/saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup
- [low] 54d old — https://www.sourcee.app/journo-request/engineering-managers-measuring-engineers-when-using-ai
- [low] 54d old — https://www.sourcee.app/journo-request/london-businesses-stopped-using-ai-hiring-tools
- [low] 54d old — https://www.sourcee.app/journo-request/creative-industry-professionals-podcast-on-ai-impact
- [low] 54d old — https://www.sourcee.app/journo-request/former-ai-skeptics-changed-views-on-ai-impact
- [low] 54d old — https://www.sourcee.app/journo-request/sales-enablement-saas-tools-proposal-and-deck-engagement-tracking
- [low] 55d old — https://www.sourcee.app/journo-request/founders-and-leaders-mindsets-and-milestones
- [low] 55d old — https://www.sourcee.app/journo-request/founders-55-latelife-entrepreneurship-series-1
- [low] 55d old — https://www.sourcee.app/journo-request/founders-and-entrepreneurs-and-musicians-podcast-guests
- [low] 55d old — https://www.sourcee.app/journo-request/ml-researchers-continuous-learning-fast-weights-and-adapters
- [low] 55d old — https://www.sourcee.app/journo-request/patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges
- [low] 55d old — https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- [low] 55d old — https://www.sourcee.app/journo-request/employers-and-recruiters-over-50s-adapting-to-ai
- [low] 55d old — https://www.sourcee.app/journo-request/data-center-professionals-podcast-guest-ai-and-hyperscale-trends
- [low] 56d old — https://www.sourcee.app/journo-request/ai-alignment-researchers-humanai-mutual-understanding
- [low] 57d old — https://www.sourcee.app/journo-request/companies-that-stopped-emailing-pdfs-new-tools-and-transition
- [low] 58d old — https://www.sourcee.app/journo-request/gen-z-ai-data-annotators-work-experience-and-income-impact
- [low] 58d old — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 58d old — https://www.sourcee.app/journo-request/ecommerce-marketers-transparency-in-ai-recommendations-and-conversion
- [low] 59d old — https://www.sourcee.app/journo-request/ai-automation-experts-speakers-on-marketing-sales-operations-gains
- [low] 59d old — https://www.sourcee.app/journo-request/cybersecurity-companies-and-experts-ai-scams-and-consumer-safety
- [low] 127d old — https://www.sourcee.app/journo-request/investigative-reporters-openai-training-predatory-dynamic-pricing

## Dropped off the feed

Still fetching, but absent from the newest digest — colder than the age says.

- [high] 65d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [medium-high] 65d old — page no longer serves the request — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium] 64d old — page no longer serves the request — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [low] 58d old — page no longer serves the request — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 55d old — page no longer serves the request — https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- [low-medium] 46d old — page no longer serves the request — https://www.sourcee.app/journo-request/insurance-agents-ai-use-in-personal-lines
- [low] 44d old — page no longer serves the request — https://www.sourcee.app/journo-request/parents-ai-acting-as-pseudoparent-in-kid-questions
- [low-medium] 44d old — page no longer serves the request — https://www.sourcee.app/journo-request/employees-conflicted-about-ai-use-generative-ai-workplace-impact
- [low] 43d old — page no longer serves the request — https://www.sourcee.app/journo-request/k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact
- [low] 39d old — page no longer serves the request — https://www.sourcee.app/journo-request/emergency-managers-ai-tools-for-funding-and-staffing-shortfalls
- [low] 38d old — page no longer serves the request — https://www.sourcee.app/journo-request/swiss-ai-companion-users-emotional-bonds-and-daily-life
- [low] 38d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-data-labelers-in-germany-positive-and-negative-experiences
- [low] 38d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories
- [low] 37d old — page no longer serves the request — https://www.sourcee.app/journo-request/uk-ai-data-trainers-daytoday-work
- [low] 37d old — page no longer serves the request — https://www.sourcee.app/journo-request/patent-attorneys-and-agents-startup-ip-starter-pack
- [low] 31d old — page no longer serves the request — https://www.sourcee.app/journo-request/minnesotans-using-chatgpt-and-ai-tools-experiences-with-election-info
- [low] 30d old — page no longer serves the request — https://www.sourcee.app/journo-request/painters-and-photographers-ai-impact-on-art
- [low] 30d old — page no longer serves the request — https://www.sourcee.app/journo-request/legal-assistants-paralegals-and-lawfirm-staff-jobs-eliminated-by-ai
- [low] 30d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-companion-users-in-africa-friendship-and-emotional-impact
- [low] 30d old — page no longer serves the request — https://www.sourcee.app/journo-request/pro-se-litigants-using-generative-ai-access-to-justice-impact
- [low] 28d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-app-and-saas-founders-1k-mrr-youtube-feature-growth-tactics
- [low] 25d old — page no longer serves the request — https://www.sourcee.app/journo-request/carleton-students-ai-impact-on-dating-experiences
- [low] 25d old — page no longer serves the request — https://www.sourcee.app/journo-request/new-yorkers-ai-music-playing-in-cabs-and-local-businesses
- [low] 25d old — page no longer serves the request — https://www.sourcee.app/journo-request/western-students-using-ai-companions-psychological-effects
- [low] 23d old — page no longer serves the request — https://www.sourcee.app/journo-request/anthropic-project-panama-employees-book-digitization-and-ai-training
- [low] 23d old — page no longer serves the request — https://www.sourcee.app/journo-request/nj-parents-and-teachers-ai-school-surveillance-and-data-practices
- [low] 22d old — page no longer serves the request — https://www.sourcee.app/journo-request/fanvue-chatters-nsfw-ai-model-experiences
- [low] 19d old — page no longer serves the request — https://www.sourcee.app/journo-request/sound-artists-and-field-recordists-run-radio-aarhus-open-call
- [low] 18d old — page no longer serves the request — https://www.sourcee.app/journo-request/students-whose-professors-allow-ai-ai-use-in-coursework
- [low] 18d old — page no longer serves the request — https://www.sourcee.app/journo-request/carleton-students-ai-dating-advice-impact-on-dating-experience
- [low] 18d old — page no longer serves the request — https://www.sourcee.app/journo-request/former-software-engineers-turned-traders-pivot-after-layoff-or-ai
- [low] 18d old — page no longer serves the request — https://www.sourcee.app/journo-request/members-club-and-hospitality-pros-in-hong-kong-postcovid-trends
- [low] 16d old — page no longer serves the request — https://www.sourcee.app/journo-request/buyers-and-sellers-without-agents-diy-property-sale-experience
- [low] 16d old — page no longer serves the request — https://www.sourcee.app/journo-request/editors-creatives-and-graphic-designers-ai-impact-documentary
- [low] 16d old — page no longer serves the request — https://www.sourcee.app/journo-request/character-ai-users-emotional-attachment-and-loneliness
- [low] 11d old — page no longer serves the request — https://www.sourcee.app/journo-request/carleton-students-ai-use-in-dating-advice
- [low] 11d old — page no longer serves the request — https://www.sourcee.app/journo-request/aussie-travellers-1861-hotel-tech-abandoned-bookings-and-ai-concerns
- [low] 11d old — page no longer serves the request — https://www.sourcee.app/journo-request/young-adults-1835-ai-impact-on-comingofage
- [low] 11d old — page no longer serves the request — https://www.sourcee.app/journo-request/people-with-ai-psychosis-firsthand-accounts
- [low] 11d old — page no longer serves the request — https://www.sourcee.app/journo-request/new-authors-ai-market-dilution-and-fair-use-impact-on-writing
- [low] 11d old — page no longer serves the request — https://www.sourcee.app/journo-request/marketers-and-creators-using-ai-agents-timesaving-wins
- [low] 11d old — page no longer serves the request — https://www.sourcee.app/journo-request/ut-austin-students-ai-trump-crypto-ads-on-game-livestreams

---

## Clearing the queue

After sending, record it so the row does not reappear:

```json
{"pitched": {"<url>": "2026-09-15"}, "skipped": {"<url>": "reason"}}
```

Ledger: `marketing/haro-outreach/pitch-ledger.json`
