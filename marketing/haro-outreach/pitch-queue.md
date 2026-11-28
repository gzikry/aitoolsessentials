# Pitch queue — clear this in one pass

Built 2026-11-28 from 407 unique requests across the digest history. **2 sendable**, 77 live, 321 cold (> 10 days and unpitched), 42 expired on the platform.

**2 finished drafts are ready to send now — 'Send these now' below names each route; 2 of them are inside the 10-day line.**

*"Sendable" is the number that matters and the one the headline used to hide: a live page is not a candidate. A row counts as sendable only when it is live, not cold, not dropped off, not already pitched, ranked above the tangential band, and has a resolved reply route (a published email, a named handle, a booking link). The other live rows are off-beat calls this queue already documents as excluded.*

**Ages are read off each request page** (`datePublished`), not off the digest text — see `marketing/haro-outreach/verified-requests.json`, refreshed by `scripts/verify_journo_requests.py`. An earlier build fell back to the digest's first-seen date and showed a 190-day-old request as 8 days old.

**No renewal signal exists on this source.** Sourcee publishes no renewal signal: on the 300 most recently indexed slugs and all 30 slugs of the live AI topic feed (checked 2026-09-19) the sitemap lastmod is byte-identical to datePublished, so 'never refreshed' is not observable and is not claimed here. Cold means old and unpitched, not provably abandoned.

**No NEW expiry in the 2026-11-28 run — but 44 carried requests are already dead.** Each answered HTTP 404 again and remains absent from the sitemap; the 2026-11-28 digest did not record a fresh wave. The rule stands: a row can disappear between two runs a day apart, so a live row is worth sending today.

**Every pitch here needs a human send.** HARO and Connectively sit behind an email wall, Qwoted and Medialyst need authenticated sessions, and Sourcee redacts the requester's own address in the request body. That is the friction that produced zero sends from the first 43 flagged opportunities. Reply routes are named per row — including addresses resolved off the *publication's* own site (a byline page or an editorial contact page), which is now the strongest route class in this queue.

## Drafts that exist and were never sent

Read this before clearing the queue: 67 draft files exist on disk. **3 of the pitches drafted here have now been sent** — listed at the bottom, not as work. The rest are still unsent; a written draft is not progress — the send is.

**THE QUEUE HOLDS 2 SENDABLE ROW(S).** A row is declared sendable on two facts evidenced separately rather than trusted from a digest field: a relevance above the tangential band, and a reply route verified by fetching a page today. Both are named in the row. The previous run reported 2; the last run before it with a non-zero count was 2026-11-27, with 0 consecutive zero run(s) in between. The live unpitched set is 77 rows.

**Today's draft file is `pitch-drafts-2026-11-28.md` (derived from disk, not typed).** The headline figures are re-derived every run: 56 of 141 tools publish a monthly price, 45 of those at or under $25/month, median $15.00 (snapshots `updated: 2026-11-28`). Superseded sets still sitting in older dated drafts (40/31/$16.50 and earlier) must not be reused.

**The pair range is `1.11x to 2.53x, median 1.25x` over 19 tiers, and it held today.** History, because every superseded value is still sitting in dated draft files and must not be reused: the range was first published as `1.21x to 2.53x, median 1.33x` (2026-09-18, sent to a real correspondent — wrong because the pair population was regex-dependent and undefined); corrected to `1.16x to 2.53x, median 1.25x` over 18 curated pairs (2026-09-21); then re-derived to `1.11x to 2.53x` when the replit-ai snapshot was refreshed (2026-09-22). See `data/monthly_annual_pairs.json` and `scripts/extract_monthly_annual_pairs.py`, which refuses to write the file at all unless every curated pair re-asserts against the live snapshot.

- anthropic-users-and-business-owners-customer-service-experiences — **Crossed cold 2026-09-23; now 78d old — no longer counted as sendable.** Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal hliwrites.99 (re-read verbatim off the live page 2026-09-30). Send late or record as skipped in `pitch-ledger.json`; the crossing is logged in `cold_without_a_send`.
- employees-blocked-from-ai-on-work-accounts-automating-tedious-ta — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — §3 in `pitch-drafts-2026-10-27.md`. Now 54d old.** Route: LinkedIn DM to linkedin.com/in/christopher-mims-club/ (LinkedIn byline page — route-checks probe 2026-11-28: HTTP 200, 666,151 bytes, title 'Christopher Mims - The Wall Street Journal | LinkedIn'; the request's own body says '(DMs open)'; muckrack.com/christopher-mims 403 and wsj.com/news/author/christopher-mims 401 are dead ends, not routes — both re-checked in the same 2026-11-28 probe). It has left the sendable count: the row is now past the 10-day line and this queue no longer ranks it as actionable. The route is not dead and the draft named above is still paste-ready — George's call is to send it late or record it skipped in `pitch-ledger.json`. Silence is the one option that leaves it drifting.
- finops-professionals-agentic-ai-cost-overruns — **Draft ready and UNSENT since 2026-09-17: `pitch-drafts-2026-09-17.md` §1. Now 82d old.** Route: LinkedIn DM to linkedin.com/in/niloy-ghosh. Cold since 2026-09-19 and still unsent — the longest-standing high-relevance request this monitor has never answered. Send it late or drop it, do not draft it a fifth time.
- tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring — **ROUTE LIVE, ROW NOW COLD — no longer in the sendable count — draft ready and UNSENT — §3 in `pitch-drafts-2026-10-28.md`. Now 49d old, carried in 27 draft files.** Route: hello@tobiamure.com, the address the journalist publishes himself on his own site — tobiamure.com homepage — route-checks probe 2026-11-28: HTTP 200, 63,449 bytes, title 'Tobi Amure, CFEI® | Finance &amp; Technology Journalist', with the contact form on tobiamure.com/contact — route-checks probe 2026-11-28: HTTP 200, 19,626 bytes, title 'Contact Tobi Amure | Finance &amp; Technology Journalist' as the fallback if mail bounces. Deliverability is NOT SMTP-verified: the domain's MX answers 554 Relay access denied for a real address, a fake control and postmaster@ alike, so that probe discriminates nothing. He asks for 'original data, or a survey with its sample size and method' and refuses DM pitches, which is why the draft leads with the one measured series we hold. Past the 10-day line the send is still possible — a late send or a ledger entry closes it; silence leaves it drifting exactly as the WSJ row did on 2026-10-16.

### Already sent — do NOT re-send

- fulltime-employees-shadow-ai-use-and-paying-outofpocket — **SENT BUT BOUNCED — the address is dead, do not retry it; a fresh route is needed before this row can be sent at all.** `pitch-ledger.json`: 2026-10-10 (SENT BUT BOUNCED - see log)
- google-and-claude-enterprise-users-seats-and-token-costs — SENT. `pitch-ledger.json`: 2026-10-10
- speciality-food-retailers-and-producers-how-theyd-spend-10k-on-t — SENT. `pitch-ledger.json`: 2026-10-10

## Send these now (2) — a finished draft and a live route

Each row below has a finished, paste-ready pitch in `pitch-drafts-2026-11-28.md` and a page that served the request today. All 2 are inside the 10-day line. A send, or a `skipped` entry in `pitch-ledger.json`, closes each one. A rewrite of the same draft does not.

- **§2 in `pitch-drafts-2026-11-28.md`** — https://www.sourcee.app/journo-request/brits-using-ai-subscription-spend-vs-annual-savings-and-earnings — 4d old, page live today, route `katiestrickwrites@gmail.com`
- **§1 in `pitch-drafts-2026-11-28.md`** — https://www.sourcee.app/journo-request/hr-professionals-ai-hiring-economics-and-workforce-planning — 5d old, page live today, route `jo.faragher@personneltoday.com`

## Sendable — pitch these (2)

Live, not cold, ranked above the tangential band, and with a reply route a human can actually use. This is the whole actionable queue.

### [high] AI / Token & Seat Cost vs Employment Economics
- **URL:** https://www.sourcee.app/journo-request/hr-professionals-ai-hiring-economics-and-workforce-planning
- **Posted:** 5d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Jo Faragher (contributing editor), Personnel Today (personneltoday.com) - byline on the page and named on the publication's own contact page. · domain personneltoday.com
- **Reply route:** ROUTE RESOLVED OFF THE PUBLICATION'S OWN SITE, not the request page: personneltoday.com/contact-us/ publishes 'Jo Faragher, contributing editor jo.faragher@personneltoday.com' in its own contact listing (re-probed 2026-11-25: HTTP 200, 243,136 bytes, address present in the page text; route-checks-2026-11-28.json). The request page itself publishes no address, handle or link. personneltoday.com MX = Google Workspace; deliverability not SMTP-verified. The send is George's.  ·  _no — email resolved off the publication's own site: jo.faragher@personneltoday.com (George sends)_
- **Angle:** Lead with the measured seat/token series and the per-seat arithmetic, offer the dated price census as the number, and answer the 'cost of AI vs cost of people' framing with our cheapest-paid-tier median and the seat annualisation. Full paste-ready draft in pitch-drafts-2026-11-24.md §1.

### [medium] AI / Consumer AI Subscription Spend
- **URL:** https://www.sourcee.app/journo-request/brits-using-ai-subscription-spend-vs-annual-savings-and-earnings
- **Posted:** 4d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-25, last 2026-11-28 (4x)
- **Publication:** Katie Strick, for Telegraph Money (telegraph.co.uk) - outlet named in the body and on the page's domain field; author on the page. · domain telegraph.co.uk
- **Reply route:** ON-BEAT AND ROUTABLE. The body's address is redacted by Sourcee, but the reporter's own site publishes katiestrickwrites@gmail.com in visible text - katiestrick.co.uk (HTTP 200, 212,116 bytes, address present) and katiestrick.co.uk/contact/ (HTTP 200, 99,121 bytes) both carry it, and the homepage lists Telegraph among her outlets (route-checked 2026-11-25). The request page publishes no address. The send is George's. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee; route resolved off the publication's own site: katiestrickwrites@gmail.com (George sends)_
- **Angle:** Lead with the measured subscription spend - how many priced tools sit at or under $25/month at the median, annualised per seat, and the monthly-vs-annual premium as the 'what you actually save' number. Full paste-ready draft in pitch-drafts-2026-11-25.md section 1.

## Live but not sendable (75)

These pages resolve and the requests are unexpired, so they are recorded — but none has both a relevance above the tangential band and a usable route. They are listed for completeness, not as candidates: pitching any of them would mean claiming standing we do not have (see the exclusions in the newest `pitch-drafts-*.md`).

### [low] AI / Healthcare / Nursing
- **URL:** https://www.sourcee.app/journo-request/nurses-where-ai-is-showing-up-and-what-needs-plain-explanation
- **Posted:** 0d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-28, last 2026-11-28 (1x)
- **Publication:** Steven Payne — Charted: AI in Healthcare (page author and body)
- **Reply route:** Comments on the original LinkedIn post; newsletter signup https://lnkd.in/ecYRNN_x is not a pitch route. Links published on the page: https://lnkd.in/ecYRNN_x.  ·  _no — published booking link https://lnkd.in/ecYRNN_x (George)_
- **Links published on the page:** https://lnkd.in/ecYRNN_x
- **Angle:** None; do not impersonate a nurse.

### [low] AI / ChatGPT Business Hub / Company metrics
- **URL:** https://www.sourcee.app/journo-request/companies-with-chatgpt-business-hub-profile-28day-mentions-and-clicks
- **Posted:** 1d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-28, last 2026-11-28 (1x)
- **Publication:** Matthew Proctor — newsletter (page author; publication not named)
- **Reply route:** Comment or message the author on the original platform; no direct handle or address is published by Sourcee. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None; no approved profile analytics to report.

### [low] AI / Accounting / Automation
- **URL:** https://www.sourcee.app/journo-request/accountants-and-students-automation-impact-on-client-advice
- **Posted:** 1d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-28, last 2026-11-28 (1x)
- **Publication:** Stéphanie KPAKPO — AUREON Insight (page author and body)
- **Reply route:** Original-platform reply; no direct handle or address published on Sourcee. Links published on the page: https://lnkd.in/eG_-nWKx.  ·  _no — published booking link https://lnkd.in/eG_-nWKx (George)_
- **Links published on the page:** https://lnkd.in/eG_-nWKx
- **Angle:** None; no accounting practitioner evidence.

### [low] AI / EU policy / Lisbon founders
- **URL:** https://www.sourcee.app/journo-request/lisbon-founders-and-ai-developers-eu-rules-impact-on-scaling
- **Posted:** 1d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-28, last 2026-11-28 (1x)
- **Publication:** Masha Moisseyeva — European research initiative (publication not specified)
- **Reply route:** Get in touch on original platform; registration links said to be in comments, not available on Sourcee. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None; no qualifying Lisbon founder experience.

### [low] AI / Higher education / Campus
- **URL:** https://www.sourcee.app/journo-request/warwick-university-students-and-faculty-ai-research-and-campus-impact
- **Posted:** 1d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-28, last 2026-11-28 (1x)
- **Publication:** Orlando Crowcroft — publication not named (page author)
- **Reply route:** DM author on original platform; no direct handle published on Sourcee. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None; no Warwick affiliation.

### [low] AI / Accountancy / Data privacy
- **URL:** https://www.sourcee.app/journo-request/accountants-and-finance-professionals-ai-data-privacy-hurdles
- **Posted:** 2d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: yes
- **Seen:** first 2026-11-27, last 2026-11-28 (2x)
- **Publication:** Pitch & Shout repost; journalist and publication not named on Sourcee.
- **Reply route:** Original post links to https://t.co/U6uparVncd as 'Pitch here'; destination not verified as an accessible reply route. Sourcee page does not expose a contact address. Links published on the page: https://t.co/U6uparVncd.  ·  _unknown — verify the route before sending_
- **Links published on the page:** https://t.co/U6uparVncd
- **Angle:** None. No qualified privacy/accountancy source; do not draft.

### [low-medium] AI / False AI-Use Accusations
- **URL:** https://www.sourcee.app/journo-request/freelance-illustrators-false-aiuse-accusations-economic-impact
- **Posted:** 5d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Suzanne Bearne - the page's own author field; no outlet named.
- **Reply route:** The body says 'Please share' but publishes no address, handle or link of its own; the request page carries no reply route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] Marketing / Automation / Management
- **URL:** https://www.sourcee.app/journo-request/marketing-automation-managers-5-ways-to-improve-team-efficiency
- **Posted:** 1d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-28, last 2026-11-28 (1x)
- **Publication:** Publication and journalist to be confirmed on original post
- **Reply route:** Original-platform reply; no verified direct route in Sourcee page. Links published on the page: https://t.co/U6uparUPmF.  ·  _unknown — verify the route before sending_
- **Links published on the page:** https://t.co/U6uparUPmF
- **Angle:** None; not an operational manager source.

### [low] AI / Human-AI Relationships
- **URL:** https://www.sourcee.app/journo-request/people-bringing-ai-partners-to-couples-therapy-relationship-impact
- **Posted:** 2d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-26, last 2026-11-28 (3x)
- **Publication:** Not named on the page - no author field, no outlet. The post is a first-person casting call.
- **Reply route:** The body says 'Please reach out if you have done this'; it publishes no address, handle or link of its own and the request page carries no reply route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **⚠ Dropped off:** left the newest Sourcee AI topic feed; page still live, but colder than age suggests — colder than its age suggests
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Customer service / Consumer testimony
- **URL:** https://www.sourcee.app/journo-request/food-delivery-and-grocery-app-users-ai-chatbot-customer-care-issues
- **Posted:** 2d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-27, last 2026-11-28 (2x)
- **Publication:** Anushka Vats — News18.com (named in request). · domain news18.com
- **Reply route:** Request asks for DM or email with subject 'Story Request – AI Chatbot & Customer Care Issues'; Sourcee redacts the email and exposes no author handle. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **⚠ Dropped off:** left the newest Sourcee AI topic feed; page still live, but colder than age suggests — colder than its age suggests
- **Angle:** None. Not a first-hand consumer source; do not draft.

### [low] AI / Data centres / UK economy and environment
- **URL:** https://www.sourcee.app/journo-request/uk-ai-and-data-centre-experts-economic-and-environmental-impact
- **Posted:** 2d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-27, last 2026-11-28 (2x)
- **Publication:** Matthew Graham (named on page); publication not supplied.
- **Reply route:** Original platform reply; no address, handle, or submission link published on Sourcee. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **⚠ Dropped off:** left the newest Sourcee AI topic feed; page still live, but colder than age suggests — colder than its age suggests
- **Angle:** None. No qualified data-centre source; do not draft.

### [low] AI / Travel technology / Hospitality
- **URL:** https://www.sourcee.app/journo-request/traveltech-companies-agentic-ai-systems-in-hospitality-and-booking
- **Posted:** 2d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-27, last 2026-11-28 (2x)
- **Publication:** Chandreyi Bandyopadhyay (named on page); print outlet not stated.
- **Reply route:** Email invitation in source request is redacted by Sourcee; no published direct address. Original platform reply requires human access. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **⚠ Dropped off:** left the newest Sourcee AI topic feed; page still live, but colder than age suggests — colder than its age suggests
- **Angle:** None. No qualifying travel-tech product; do not draft.

### [low] AI / Podcast Guest Call
- **URL:** https://www.sourcee.app/journo-request/professionals-using-ai-at-work-realworld-stories
- **Posted:** 3d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-25, last 2026-11-28 (4x)
- **Publication:** chetan K. - the page's own author field; the post is a podcast (Kicckutalks) guest call; no outlet named.
- **Reply route:** The body asks people to 'drop your industry and your experience in the comments'; it publishes no address, handle or link of its own and the request page carries no reply route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Compute & Data-Centre Economics
- **URL:** https://www.sourcee.app/journo-request/data-center-economists-ai-compute-economics
- **Posted:** 3d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-25, last 2026-11-28 (4x)
- **Publication:** Waqas - the page's own author field; no outlet named.
- **Reply route:** The body says 'Does anyone know any expert on data centers and economics of ai? I need to talk to someone for a story.' It publishes no address, handle or link of its own and the request page carries no reply route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Game-Theory Framing Critique
- **URL:** https://www.sourcee.app/journo-request/game-theorists-working-on-ai-risks-of-game-theory-framing
- **Posted:** 3d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-25, last 2026-11-28 (4x)
- **Publication:** Adam Tohn - the page's own author field; no outlet named.
- **Reply route:** Carries one short link (https://lnkd.in/eV6EKDDc) as a 'reach out' call; it publishes no address or handle of its own. Links published on the page: https://lnkd.in/eV6EKDDc.  ·  _no — published booking link https://lnkd.in/eV6EKDDc (George)_
- **Links published on the page:** https://lnkd.in/eV6EKDDc
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Cybersecurity Breach Follow-up
- **URL:** https://www.sourcee.app/journo-request/eu-academy-learners-6-months-ago-how-you-learned-of-breach
- **Posted:** 3d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-25, last 2026-11-28 (4x)
- **Publication:** Eddie Valentine, High Point Investigation Desk / High Point Editorial Services - a research-desk post, not a newsroom byline.
- **Reply route:** Carries a redirect link (https://lnkd.in/gCYCf9HX); it publishes no address or handle of its own. Links published on the page: https://lnkd.in/gCYCf9HX.  ·  _no — published booking link https://lnkd.in/gCYCf9HX (George)_
- **Links published on the page:** https://lnkd.in/gCYCf9HX
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Agentic Automation Critique
- **URL:** https://www.sourcee.app/journo-request/ai-engineers-and-tech-leaders-agentic-automation-critique
- **Posted:** 3d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-26, last 2026-11-28 (3x)
- **Publication:** The page's own author field; no outlet named.
- **Reply route:** The body asks AI engineers/tech leaders to comment; it publishes no address or handle of its own and the page carries a 'Comment' hint only, not a route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Sports Technology
- **URL:** https://www.sourcee.app/journo-request/sports-tech-experts-ai-and-sport
- **Posted:** 3d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-26, last 2026-11-28 (3x)
- **Publication:** The page's own author field; no outlet named.
- **Reply route:** A 'source callout' with 'DMs are open'; it publishes no address, handle or link of its own and the page carries no reply route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Career & Industry Testimony
- **URL:** https://www.sourcee.app/journo-request/ai-and-ml-engineers-data-scientists-career-paths-and-ai-impact
- **Posted:** 3d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-26, last 2026-11-28 (3x)
- **Publication:** Business Insider (businessinsider.com on the page's domain field); author not named. · domain businessinsider.com
- **Reply route:** Sourcee redacts the body's address; the page publishes only a redirect link (https://lnkd.in/erSx6dTf), not a route. The request body's address is redacted by Sourcee. Links published on the page: https://lnkd.in/erSx6dTf.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Links published on the page:** https://lnkd.in/erSx6dTf
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Labour & Workforce Testimony
- **URL:** https://www.sourcee.app/journo-request/us-workers-who-used-ai-challenging-layoffs-and-pay-delays
- **Posted:** 3d old (page datePublished unparseable (cached age)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-26, last 2026-11-28 (3x)
- **Publication:** Business Insider (businessinsider.com on the page's domain field); author not named. · domain businessinsider.com
- **Reply route:** The body says 'DM me'/'email me' but publishes no handle; the request page carries no reply route and the address is redacted. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Special-Education Data
- **URL:** https://www.sourcee.app/journo-request/k12-deaf-and-hard-of-hearing-students-missing-iep-services
- **Posted:** 3d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-26, last 2026-11-28 (3x)
- **Publication:** Not named on the page - no author field, no outlet.
- **Reply route:** The body references the National Deaf Education Data Index (NDEDI); it publishes no address, handle or link of its own and the page carries no reply route. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Property & Consumer
- **URL:** https://www.sourcee.app/journo-request/property-viewers-who-saw-aigenerated-listing-images-reactions
- **Posted:** 3d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-26, last 2026-11-28 (3x)
- **Publication:** The i Paper (theipaper.com on the page's domain field); author not named. · domain theipaper.com
- **Reply route:** Sourcee redacts the body's address ('[email redacted]'); the request page publishes no address, handle or link of its own. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Corporate Governance Reaction
- **URL:** https://www.sourcee.app/journo-request/current-and-former-nvidia-employees-jensen-huang-reinstated-as-ceo
- **Posted:** 4d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Daniel Howley - the page's own author field; no outlet named on the page.
- **Reply route:** The body says 'My DMs are open' but publishes no handle or address of its own; the request page carries no reply route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Breaking-News Market Comment
- **URL:** https://www.sourcee.app/journo-request/ai-industry-analysts-jensen-huang-return-to-nvda-implications
- **Posted:** 4d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Jon Swartz, TechStrong Group (techstronggroup.com) - domain on the page. · domain techstronggroup.com
- **Reply route:** The body's address is redacted by Sourcee ('DM or [email redacted]'); the request page publishes no address, handle or link of its own. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Opinion Pieces
- **URL:** https://www.sourcee.app/journo-request/it-analysts-and-security-experts-nvidia-ceo-reinstatement-impact
- **Posted:** 4d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Sarah A. - the page's own author field; no outlet named.
- **Reply route:** The body asks to 'drop me a line' but publishes no address or handle; the request page carries no reply route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Insurance Response to Outages
- **URL:** https://www.sourcee.app/journo-request/brokers-and-claims-pros-m365-and-us-atc-ground-stop-insurer-response
- **Posted:** 4d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Bryony Garlick, Insurance Business UK (insurancebusinessmag.com) - domain on the page. · domain insurancebusinessmag.com
- **Reply route:** The body's address is redacted by Sourcee ('Comment below, DM me or email [email redacted]'); the request page publishes no address, handle or link of its own. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Consumer AI Mishaps
- **URL:** https://www.sourcee.app/journo-request/uk-residents-ai-horror-stories-embarrassing-costly-mistakes
- **Posted:** 4d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-25, last 2026-11-28 (4x)
- **Publication:** Katie Strick - the page's own author field; 'a UK newspaper' is named in the body, not on the page.
- **Reply route:** Sourcee redacts the body's address ('[email redacted]'); the request page publishes no address, handle or link of its own. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Agent Failure Anecdotes
- **URL:** https://www.sourcee.app/journo-request/employees-using-ai-agents-tasks-reclaimed-over-tone-and-date-errors
- **Posted:** 4d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-25, last 2026-11-28 (4x)
- **Publication:** Dhruv Jain - the page's own author field; no outlet named.
- **Reply route:** Asks people to post examples ('here is my question for anyone who has used AI agents at work'); it publishes no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Tech Layoffs Testimony
- **URL:** https://www.sourcee.app/journo-request/tech-employees-in-india-conversations-and-preparation-amid-layoffs
- **Posted:** 4d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-25, last 2026-11-28 (4x)
- **Publication:** Devansh Mittal, The Indian Express (indianexpress.com) - domain on the page and named in the body. · domain indianexpress.com
- **Reply route:** The body says 'If you want to talk, please DM me' but publishes no handle; the request page carries no reply route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Employee Reaction
- **URL:** https://www.sourcee.app/journo-request/nvidia-employees-and-openai-staff-at-altman-exit-and-return-reactions
- **Posted:** 5d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Manseen Logan, MFA, Business Insider (businessinsider.com) - domain on the page. · domain businessinsider.com
- **Reply route:** The body's address is redacted by Sourcee ('reach out on LinkedIn or to my inbox: [email redacted]'); the page publishes no address or handle of its own. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / PR Agency Listing
- **URL:** https://www.sourcee.app/journo-request/uk-healthcare-expert-ai-impact-on-nhs-staffing-and-care
- **Posted:** 5d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Pitch & Shout - an agency's own request-listing post; no journalist or outlet named.
- **Reply route:** The post carries one outbound link, an application form at https://t.co/U6uparUPmF ('Join here to apply for this'); there is no address or handle. Links published on the page: https://t.co/U6uparUPmF.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/U6uparUPmF
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Leadership Interview
- **URL:** https://www.sourcee.app/journo-request/hr-professional-leadership-and-ai-available-next-48-hours
- **Posted:** 5d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Dr. Cheryl Robinson - the page's own author field; no outlet named.
- **Reply route:** Asks to be recommended someone available for a brief interview; publishes no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Healthcare Operations
- **URL:** https://www.sourcee.app/journo-request/uk-healthcare-experts-ai-scheduling-and-staffing-admin-impact
- **Posted:** 5d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Lindsay Dodgson - the page's own author field; no outlet named.
- **Reply route:** The body's address is redacted by Sourcee; the request page publishes no address, handle or link of its own. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Real-Estate Listing Images
- **URL:** https://www.sourcee.app/journo-request/estate-agents-using-ai-photos-reluctant-due-to-competition
- **Posted:** 5d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Emily Braeger, The i Paper (theipaper.com) - domain on the page. · domain theipaper.com
- **Reply route:** The body's address is redacted by Sourcee ('Pls email me at [email redacted]'); the request page publishes no address or handle of its own. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Accountancy Automation
- **URL:** https://www.sourcee.app/journo-request/accountancy-automation-consultant-professional-body-publication
- **Posted:** 5d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Caroline Roberts - the page's own author field; no outlet named ('professional body publication').
- **Reply route:** The page publishes no address, handle or link of its own; the body carries only a deadline ('Deadline Thurs 26th'). The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Accountancy Firms RPA
- **URL:** https://www.sourcee.app/journo-request/icaew-sme-accountancy-firms-ai-and-robotics-process-automation
- **Posted:** 5d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Caroline Roberts - same author as the row above; no outlet named.
- **Reply route:** The page publishes no address, handle or link of its own; deadline 'Thurs 26th'. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Podcast Booking
- **URL:** https://www.sourcee.app/journo-request/classic-car-owners-restoration-and-firstcar-stories
- **Posted:** 5d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Doug K., carsloved.com - the poster's own podcast site, linked from the page. · domain carsloved.com
- **Reply route:** The body links the poster's own site (https://carsloved.com) as a listen/join call; no address or handle published for a reply. Links published on the page: https://carsloved.com.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://carsloved.com
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Newsletter Case Studies
- **URL:** https://www.sourcee.app/journo-request/executives-and-founders-career-reinvention-case-studies
- **Posted:** 5d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-24, last 2026-11-28 (5x)
- **Publication:** Mo GAD - the page's own author field; the post is a LinkedIn newsletter promo.
- **Reply route:** The body's address is redacted by Sourcee; the page publishes no address or handle of its own. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Security Review
- **URL:** https://www.sourcee.app/journo-request/cybersecurity-experts-review-ai-weaponization-investigation-desk
- **Posted:** 6d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-23, last 2026-11-28 (6x)
- **Publication:** High Point Editorial Services - the banner/byline on the page; a Substack publisher, no news outlet named.
- **Reply route:** No address, handle or reply link published on the request page; the only outbound link is the poster's own Substack (lnkd.in/gXPpRwvh). Links published on the page: https://lnkd.in/gXPpRwvh,.  ·  _no — published booking link https://lnkd.in/gXPpRwvh, (George)_
- **Links published on the page:** https://lnkd.in/gXPpRwvh,
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] AI / Language Use Testimony
- **URL:** https://www.sourcee.app/journo-request/nontech-users-and-ai-teams-in-india-ai-use-in-complex-indian-languages
- **Posted:** 6d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-23, last 2026-11-28 (6x)
- **Publication:** LiveMint (livemint.com) - domain on the page; no named byline. · domain livemint.com
- **Reply route:** The body says 'DMs open' but publishes no handle or address of its own; the request page carries no reply route. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None. No route and no standing. NOT DRAFTED.

### [low] Legal Tech / AI Explanation
- **URL:** https://www.sourcee.app/journo-request/generative-and-agentic-ai-builders-and-users-agentic-vs-generative-ai
- **Posted:** 7d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-21, last 2026-11-28 (8x)
- **Publication:** Mark Schwartz - Lawyers Weekly (lawyersweekly.com.au); the domain field on the page names the outlet. · domain lawyersweekly.com.au
- **Reply route:** Body says 'Comment below or send me a message, and introductions are welcome too'; the page publishes no address or handle of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off our standing (wants an AI builder/practitioner) and no route published.

### [low] Higher Ed / Corporate AI Partnerships
- **URL:** https://www.sourcee.app/journo-request/higher-ed-advancement-leaders-and-board-members-ai-partnerships
- **Posted:** 7d old (page datePublished (page probed 2026-11-28)) · badge: Posted in last 7 days · AI-topic feed: no
- **Seen:** first 2026-11-21, last 2026-11-28 (8x)
- **Publication:** Kristin Hanson - page names no publication domain; body is tagged 'SOURCE REQUEST!'.
- **Reply route:** Body says 'Please DM or email me to chat ASAP'; the page publishes no address or handle of the poster's own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Institutional-partnership testimony we do not hold and no route.

### [low] Consumer AI / Retail
- **URL:** https://www.sourcee.app/journo-request/consumers-using-agentic-shopping-christmas-purchase-insights
- **Posted:** 8d old (page datePublished (page probed 2026-11-28)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-20, last 2026-11-28 (9x)
- **Publication:** Jeremy Lott - page names no publication (byline reads 'Jeremy Lott has a children's book for you')
- **Reply route:** Body says 'Drop me a line'; the page publishes no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Consumer agentic-shopping testimony; no pricing question we hold evidence on and no route.

### [low] AI and Education
- **URL:** https://www.sourcee.app/journo-request/parents-of-current-students-ai-impact-on-kids-and-how-they-help
- **Posted:** 8d old (page datePublished (page probed 2026-11-28)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-20, last 2026-11-28 (9x)
- **Publication:** Unlocked: Living With AI - podcast (page names no publication domain; body tags #Unlocked_LivingWithAI)
- **Reply route:** Page publishes no address, handle or link of its own; the body routes via hashtags to 'Beyond the Screen: Whose Voices'. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Parental AI-in-schools testimony; no pricing question and no route.

### [low] Customer Experience / Webinar Booking
- **URL:** https://www.sourcee.app/journo-request/customer-experience-experts-b2c-experience-trends-and-challenges
- **Posted:** 8d old (page datePublished (page probed 2026-11-28)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-20, last 2026-11-28 (9x)
- **Publication:** Claire Cunningham - The Customer Connexion (webinar series; page names no publication domain)
- **Reply route:** Body books an 'industry expert guest' for the Experience Gap webinar series; no address or handle of the poster's own is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. CX webinar guest booking; no pricing question and no route.

### [low] AI Infrastructure / Community Impact
- **URL:** https://www.sourcee.app/journo-request/residents-near-data-centers-jobs-and-investment-promises
- **Posted:** 8d old (page datePublished unparseable (cached age)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-20, last 2026-11-28 (9x)
- **Publication:** Adam Mahoney - Capital B (capitalbnews.org), Pulitzer Center AI Accountability Network series · domain capitalbnews.org
- **Reply route:** Body routes to a story-sharing form (https://lnkd.in/gvxbu9vx); the page publishes no address or handle of the reporter's own. Links published on the page: https://lnkd.in/gA8YUM4W, https://lnkd.in/gvxbu9vx).  ·  _no — published booking link https://lnkd.in/gA8YUM4W (George)_
- **Links published on the page:** https://lnkd.in/gA8YUM4W, https://lnkd.in/gvxbu9vx)
- **Angle:** None - excluded. Resident data-centre testimony; first-hand experience we do not hold and only a form as a route.

### [low] AI and Work / HR Technology Pay
- **URL:** https://www.sourcee.app/journo-request/payroll-and-hris-analysts-combined-role-challenges-and-pay-gaps
- **Posted:** 8d old (page datePublished (page probed 2026-11-28)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-20, last 2026-11-28 (9x)
- **Publication:** Katrina Flowers, MSOP - page names no publication (a first-person data post)
- **Reply route:** Page publishes no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. HRIS role/pay commentary; salary spend, not tool pricing, and no route.

### [low] AI and Work / Graduate Hiring
- **URL:** https://www.sourcee.app/journo-request/hiring-managers-and-hr-leaders-ai-impact-on-graduate-hiring
- **Posted:** 8d old (page datePublished (page probed 2026-11-28)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-21, last 2026-11-28 (8x)
- **Publication:** Pitch & Shout - a PR/press-feature platform (the page's author field), relaying a journalist co-writing for an unnamed 'leading business magazine'.
- **Reply route:** Body says 'Join Pitch & Shout using the link in bio and apply directly'; no address or handle of the journalist's own is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Employer hiring-experience solicitation via a PR platform; no standing and no route.

### [low] Business Travel / Behavioural Science
- **URL:** https://www.sourcee.app/journo-request/psychologist-and-behavioural-scientist-value-of-business-travel
- **Posted:** 8d old (page datePublished (page probed 2026-11-28)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-21, last 2026-11-28 (8x)
- **Publication:** Becky Tanner-Rolf - page names no publication domain; the piece is an 'editorial report' for an unnamed client.
- **Reply route:** Body says 'drop a note in the comments or send me a message'; the page publishes no address or handle of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat expert call, no pricing question and no route.

### [low] Healthcare IT / 2027 Regulation
- **URL:** https://www.sourcee.app/journo-request/hospital-cios-and-cisos-preparing-for-2027-it-regulations
- **Posted:** 8d old (page datePublished (page probed 2026-11-28)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-21, last 2026-11-28 (8x)
- **Publication:** Brian Eastwood - HealthTech Magazine (healthtechmagazine.net); the domain field names the outlet. · domain healthtechmagazine.net
- **Reply route:** Body says 'Hit me up with suggestions'; the page publishes no address or handle of the reporter's own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Wants a hospital/health-system IT leader's own response; no standing and no route.

### [low] Crypto / Podcast Booking
- **URL:** https://www.sourcee.app/journo-request/crypto-hack-victims-hacked-podcast-personal-stories
- **Posted:** 8d old (page datePublished (page probed 2026-11-28)) · badge: Posted 8 days ago · AI-topic feed: no
- **Seen:** first 2026-11-21, last 2026-11-28 (8x)
- **Publication:** James McFadden ('Six8Jay') - 'HACKED: The Podcast'; page names no publication domain.
- **Reply route:** Body invites victims to tell their story; the page publishes only a t.co book link, no address or handle as a reply channel. Links published on the page: https://t.co/LTFOJ4gbVG, https://t.co/LTFOJ4gbVG,.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/LTFOJ4gbVG, https://t.co/LTFOJ4gbVG,
- **Angle:** None - excluded. Podcast victim-story booking; off the pricing beat and no route.

### [low] AI Infrastructure / Data Centres and Compute Cost
- **URL:** https://www.sourcee.app/journo-request/data-centre-operators-and-enterprise-cios-in-india-ai-capacity-and-costs
- **Posted:** 9d old (page datePublished (page probed 2026-11-28)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Shrikanth Govindarajan - Dataquest (dataquest.in), print cover story · domain dataquest.in
- **Reply route:** Body asks for perspective and the page's address is platform-redacted; no handle, link or byline route is published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Off-beat: Indian data-centre capex and power costs; no pricing question we hold evidence on and no route.

### [low] Startups / Culture
- **URL:** https://www.sourcee.app/journo-request/startup-founders-time-off-for-gta-release-and-anthropic-ipo-coincidence
- **Posted:** 9d old (page datePublished (page probed 2026-11-28)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Amanda Silberling - TechCrunch (techcrunch.com) · domain techcrunch.com
- **Reply route:** Body says 'emailed quotes OK [email redacted]'; the address is platform-redacted and no handle is published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Off-beat joke call about GTA and the Anthropic IPO; no pricing question and no route.

### [low] AI and Work / Creative Industries
- **URL:** https://www.sourcee.app/journo-request/young-nigerian-creatives-ai-impact-on-work-and-income
- **Posted:** 9d old (page datePublished (page probed 2026-11-28)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-20, last 2026-11-28 (9x)
- **Publication:** Ihuoma Ukeje - ClickNaija (page names no publication domain; body tags #ClickNaija)
- **Reply route:** Body routes to a survey: https://lnkd.in/ecTwGXJr. No email or handle of the poster's own is published. Links published on the page: https://lnkd.in/ecTwGXJr.  ·  _no — published booking link https://lnkd.in/ecTwGXJr (George)_
- **Links published on the page:** https://lnkd.in/ecTwGXJr
- **Angle:** None - excluded. Nigerian-creative income survey; first-hand experience we do not hold and the only route is a form.

### [low] AI / Benchmarks and Evaluation
- **URL:** https://www.sourcee.app/journo-request/ai-benchmark-experts-commentary-on-arena-and-datacurve
- **Posted:** 9d old (page datePublished (page probed 2026-11-28)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-20, last 2026-11-28 (9x)
- **Publication:** Scott Tolinski - page names no publication (the tagged @arena and @datacurve are product accounts, not outlets)
- **Reply route:** Body asks 'who should i talk to?' - a referral ask, not an open call; the page publishes no address or handle. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Benchmark-expert referral; off our pricing beat and no route.

### [low] Supply Chain / Retail AI
- **URL:** https://www.sourcee.app/journo-request/uk-and-europe-sports-retail-supply-chain-pros-retail-ai-at-scale
- **Posted:** 9d old (page datePublished (page probed 2026-11-28)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-20, last 2026-11-28 (9x)
- **Publication:** Katie Howard - SupplyChainTalk (podcast/webinar series; page names no publication domain)
- **Reply route:** Body books speakers for two 2027 episodes (13 January 2027 and a second slot); the page publishes no address or handle. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Supply-chain podcast booking; no pricing question and no route.

### [low] AI and Work / Talent
- **URL:** https://www.sourcee.app/journo-request/hr-leaders-and-talent-execs-skills-gap-ai-and-graduate-employability
- **Posted:** 9d old (page datePublished (page probed 2026-11-28)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-20, last 2026-11-28 (9x)
- **Publication:** George Chilton - HBR (Deusto edition) article (page names no publication domain)
- **Reply route:** Body says 'If you answer below, I may include your quote or reach out for an interview'; the page publishes no address or handle. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. HR talent-strategy quotes; standing we do not have and no route.

### [low] AI Security / Podcast Booking
- **URL:** https://www.sourcee.app/journo-request/security-researchers-antiforensics-iot-ai-security
- **Posted:** 9d old (page datePublished (page probed 2026-11-28)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-20, last 2026-11-28 (9x)
- **Publication:** Enleak - DE&TH DIARIES podcast (page names no publication domain)
- **Reply route:** Page publishes one shortened link (https://t.co/TOTtQF2Xl8); no address or handle of the poster's own. Links published on the page: https://t.co/TOTtQF2Xl8!.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/TOTtQF2Xl8!
- **Angle:** None - excluded. Security-research podcast booking; off the pricing beat and no route.

### [low] Fashion / Media Commentary
- **URL:** https://www.sourcee.app/journo-request/fashion-analysts-industry-trends-and-commentary
- **Posted:** 9d old (page datePublished (page probed 2026-11-28)) · badge: Posted 9 days ago · AI-topic feed: no
- **Seen:** first 2026-11-20, last 2026-11-28 (9x)
- **Publication:** Trishla Ostwal - ADWEEK (page names no publication domain)
- **Reply route:** Body says 'my DMs and emails are open'; the page publishes no address or handle of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Fashion-analyst commentary; the poster says it is not an AI story this week and no route is published.

### [low] AI Markets / IPO and Valuation
- **URL:** https://www.sourcee.app/journo-request/investment-bankers-and-vcs-and-valuation-experts-ai-ipo-race-drivers
- **Posted:** 10d old (page datePublished unparseable (cached age)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-18, last 2026-11-28 (11x)
- **Publication:** Not named on the page - Times Group (timesgroup.com) request · domain timesgroup.com
- **Reply route:** Body says 'please feel free to DM me' and 'reach out to me here: [email redacted]'; Sourcee redacts the address and the page publishes no handle, link or byline of the poster's own. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Off-beat: capital-markets and valuation commentary on the AI IPO race; no pricing question we can answer and no route published.

### [low] B2B Marketing / AI Visibility and AEO
- **URL:** https://www.sourcee.app/journo-request/b2b-creators-and-agencies-impact-on-ai-visibility-and-aeo
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-18, last 2026-11-28 (11x)
- **Publication:** Not named on the page - an unnamed report author
- **Reply route:** Body names three wanted profiles and asks for no channel at all; the page publishes no address, handle or link of its own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat: B2B creator/AEO practitioner research with no pricing question and no route published.

### [low] AI Policy / Agent-Centric Web
- **URL:** https://www.sourcee.app/journo-request/ai-agent-builders-and-researchers-agentcentric-web-policy-input
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-18, last 2026-11-28 (11x)
- **Publication:** Not named on the page - input sought for the UNESCO IFAP Information Literacy Working Group (ILWG)
- **Reply route:** Body says 'If you build, deploy or research...' and the page publishes one shortened link (https://lnkd.in/gPvrfnae) plus a 'Signal' hint; no address or handle is published. Links published on the page: https://lnkd.in/gPvrfnae.  ·  _no — published booking link https://lnkd.in/gPvrfnae (George)_
- **Links published on the page:** https://lnkd.in/gPvrfnae
- **Angle:** None - excluded. Off-beat: UNESCO policy consultation for AI agent builders and researchers; standing we do not have.

### [low] Visual Arts / AI and Culture
- **URL:** https://www.sourcee.app/journo-request/flemish-visual-artists-against-ai-college-magazine-article
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-18, last 2026-11-28 (11x)
- **Publication:** Not named on the page - college magazine
- **Reply route:** Body says 'Contact me!' but the page publishes no address, handle or link. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Off-beat: Flemish artist testimony; no pricing question and no route.

### [low] AI and Work / Agentic Customer Service
- **URL:** https://www.sourcee.app/journo-request/call-center-and-customer-service-reps-ai-agent-phone-calls-impact
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Issie Lapowsky - columnist (page names no publication; body says 'an upcoming column on AI and work')
- **Reply route:** Body says 'Reach out at [email redacted] or issielapowsky.08 on Signal'. The Signal handle is the only published route and is a reporter's own handle, not an address on the request page. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. First-hand call-centre testimony only; we hold no such experience.

### [low] Freelance Work / AI Productivity
- **URL:** https://www.sourcee.app/journo-request/freelancers-using-ai-tools-rising-income-and-more-work
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Ellen Sheng - CNBC (cnbc.com) · domain cnbc.com
- **Reply route:** Body says 'email me at [email redacted]'; the address is platform-redacted and the page publishes no handle or link. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Freelancer income testimony; no pricing question we can answer as a publisher and no route.

### [low] Corporate Governance
- **URL:** https://www.sourcee.app/journo-request/board-directors-and-governance-advisers-nvidia-ceo-crisis-prevention
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Matt Kelly - no publication named on the page
- **Reply route:** Body says 'Reach out if interested'; no address, handle or link is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Board governance commentary with no pricing question and no route.

### [low] Logistics / GIS
- **URL:** https://www.sourcee.app/journo-request/truck-drivers-nomap-mishaps-and-gis-ai-future
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** The Open Road w/ KC Phillips - podcast (no publication domain)
- **Reply route:** Page publishes one shortened link (https://t.co/yrokZsDvOF); no address or handle of the poster's own. Links published on the page: https://t.co/yrokZsDvOF.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Links published on the page:** https://t.co/yrokZsDvOF
- **Angle:** None - excluded. Trucking podcast booking; no pricing question and no route.

### [low] AI Markets / IPO
- **URL:** https://www.sourcee.app/journo-request/anthropic-investors-bull-and-bear-case-ahead-of-ipo
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Jennifer Sor - Business Insider (businessinsider.com) · domain businessinsider.com
- **Reply route:** Body says 'email [email redacted]'; the address is platform-redacted and the page publishes no handle. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Investor testimony requiring receipts; we are not an Anthropic investor and no route is published.

### [low] Banking Risk / AI Governance
- **URL:** https://www.sourcee.app/journo-request/apac-banking-risk-officers-ai-agents-accelerating-bank-runs
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Vince Dioquino - page names no publication
- **Reply route:** Body says 'Please message me or leave a comment so I can reach out'; no address or handle is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. APAC banking-risk commentary; no pricing question and only a platform comment as a route.

### [low] Consumer AI / Property
- **URL:** https://www.sourcee.app/journo-request/estate-agents-and-buyers-affected-by-housefishing-ai-listing-photos
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Emily Braeger - The i Paper (theipaper.com) · domain theipaper.com
- **Reply route:** Body says 'Pls email me at [email redacted]'; the address is platform-redacted and no handle is published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. First-hand housefishing testimony; address redacted and no route.

### [low] AI Markets / IPO
- **URL:** https://www.sourcee.app/journo-request/uk-retail-investors-who-bought-anthropic-preipo-anthropic-ipo
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Maisie Grice - City A.M. (cityam.com) · domain cityam.com
- **Reply route:** Body says 'Please email [email redacted]'; redacted, no handle published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. UK retail investor testimony, same-day deadline implied; no route and no pricing question.

### [low] AI Markets / IPO
- **URL:** https://www.sourcee.app/journo-request/british-private-investors-anthropic-ipo-plans
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Callum Martin - The Times (thetimes.co.uk) · domain thetimes.co.uk
- **Reply route:** Body says 'please reach out at [email redacted]'; redacted, no handle published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Private-investor testimony; no route and no pricing question.

### [low] AI in Emerging Markets
- **URL:** https://www.sourcee.app/journo-request/nigerian-ai-founders-realworld-ai-solving-local-problems
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Dr Chioma Ezenwafor - page names no publication
- **Reply route:** Body says 'DM me with a one-line description'; no address, handle or link is published. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Nigerian founder profile call; standing we do not have and no route.

### [low] AI / Podcast Booking
- **URL:** https://www.sourcee.app/journo-request/ai-experts-and-industry-leaders-use-cases-jobs-ethics
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Chetan K. - Kicckutalks podcast (no publication domain)
- **Reply route:** Body says 'Send me a DM or comment AI EXPERT below'; no address or handle of the poster's own. The page publishes no address, handle or link of its own.  ·  _no — no route published on the page or the publication's site (George: original platform)_
- **Angle:** None - excluded. Podcast guest booking; no pricing question and no route.

### [low] Consumer Finance
- **URL:** https://www.sourcee.app/journo-request/consumers-panic-buying-and-hoarding-cash-outages-and-market-fears
- **Posted:** 10d old (page datePublished (page probed 2026-11-28)) · badge: Posted 10 days ago · AI-topic feed: no
- **Seen:** first 2026-11-19, last 2026-11-28 (10x)
- **Publication:** Genna - MarketWatch (marketwatch.com) · domain marketwatch.com
- **Reply route:** Body says 'Email me if interested [email redacted]'; redacted, no handle published. The request body's address is redacted by Sourcee.  ·  _no — body address redacted by Sourcee, no route resolved for this request (George: original platform)_
- **Angle:** None - excluded. Consumer panic-buying testimony; AI is incidental, address redacted, no route.

## Cold — only if you have a reason

Older than the 10-day line and never pitched. Not provably abandoned — no renewal signal exists on this source — but every one of these has already passed an ideal send window.

- [high] 79d old — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [high] 82d old — https://www.sourcee.app/journo-request/finops-professionals-agentic-ai-cost-overruns
- [high] 84d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-ai-governance-and-agent-sprawl
- [high] 85d old — https://www.sourcee.app/journo-request/scientists-phd-students-and-postdocs-paying-for-ai-subscriptions
- [high] 130d old — https://www.sourcee.app/journo-request/business-and-technology-leaders-tech-budget-priorities-amid-volatility
- [high] 210d old — https://www.sourcee.app/journo-request/anthropic-api-users-costs-and-token-burn-increase-since-january
- [medium-high] 78d old — https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
- [medium-high] 79d old — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium-high] 82d old — https://www.sourcee.app/journo-request/uk-managers-cracked-down-on-gen-z-ai-overuse
- [medium] 12d old — https://www.sourcee.app/journo-request/former-software-engineers-left-tech-after-ai-coding-tools
- [medium] 16d old — https://www.sourcee.app/journo-request/companies-switched-from-token-ai-pricing-outcomebased-contracts
- [medium] 31d old — https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
- [medium] 32d old — https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
- [medium] 32d old — https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact
- [medium] 54d old — https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
- [medium] 78d old — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [medium] 82d old — https://www.sourcee.app/journo-request/ai-agents-making-money-2026-sales-and-leadgen-workflow-ops
- [medium] 82d old — https://www.sourcee.app/journo-request/ai-startups-workplace-fraud-detection-expenses-time-theft
- [medium] 82d old — https://www.sourcee.app/journo-request/marketing-and-content-leaders-aiassisted-work-review-process
- [medium] 86d old — https://www.sourcee.app/journo-request/ceos-ai-impact-on-ops-culture-and-commercial-strategy
- [medium] 96d old — https://www.sourcee.app/journo-request/uk-finance-risk-and-regulatory-leaders-ai-explainability-risks
- [medium] 263d old — https://www.sourcee.app/journo-request/sme-owners-operational-challenges-for-ai-solutions-case-study
- [low-medium] 18d old — https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai
- [low-medium] 18d old — https://www.sourcee.app/journo-request/labor-economists-unintended-consequences-of-automation
- [low-medium] 21d old — https://www.sourcee.app/journo-request/business-owners-and-leaders-team-resistance-to-ai-adoption
- [low-medium] 36d old — https://www.sourcee.app/journo-request/claude-users-anthropic-public-benefit-fund-trust-and-job-impact
- [low-medium] 46d old — https://www.sourcee.app/journo-request/b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research
- [low-medium] 49d old — https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
- [low-medium] 53d old — https://www.sourcee.app/journo-request/uk-companies-implementing-ai-how-automation-transforms-workdays
- [low-medium] 57d old — https://www.sourcee.app/journo-request/law-firm-lawyers-concrete-ai-implementations-and-billing-impact
- [low-medium] 58d old — https://www.sourcee.app/journo-request/employees-conflicted-about-ai-use-generative-ai-workplace-impact
- [low-medium] 60d old — https://www.sourcee.app/journo-request/insurance-agents-ai-use-in-personal-lines
- [medium-low] 70d old — https://www.sourcee.app/journo-request/founders-cutting-ai-use-eliminating-or-reducing-ai-in-business
- [low-medium] 73d old — https://www.sourcee.app/journo-request/us-founders-calls-to-slow-ai-development-impact-on-companies
- [medium-low] 79d old — https://www.sourcee.app/journo-request/tech-policy-experts-california-ai-audit-bills-impact-cios
- [low-medium] 98d old — https://www.sourcee.app/journo-request/ai-project-builders-youtube-finance-and-lifestyle-channel-feature
- [low-medium] 143d old — https://www.sourcee.app/journo-request/prompt-engineers-tokenmaxxing-anecdotes
- [low] 11d old — https://www.sourcee.app/journo-request/lab-researchers-and-ai-preppers-ai-doom-prep-land-metals-weapons
- [low] 11d old — https://www.sourcee.app/journo-request/ai-experts-bot-syntax-and-prompt-structure
- [low] 11d old — https://www.sourcee.app/journo-request/divorcing-adults-who-used-ai-personal-stories-about-impact
- [low] 11d old — https://www.sourcee.app/journo-request/parents-using-ai-tools-invisible-labor-in-relationships
- [low] 11d old — https://www.sourcee.app/journo-request/cpas-choosing-best-accounting-software-forbes-advisor
- [low] 11d old — https://www.sourcee.app/journo-request/ai-faculty-fellows-and-supervisors-role-between-policy-tech-curriculum
- [low] 11d old — https://www.sourcee.app/journo-request/publishers-creators-and-media-brands-state-of-newsletter-report-2027
- [low] 11d old — https://www.sourcee.app/journo-request/home-hunters-and-renters-misleading-aigenerated-listing-photos
- [low] 12d old — https://www.sourcee.app/journo-request/comic-book-writer-greg-pak-ai-consent-and-digital-comics
- [low] 12d old — https://www.sourcee.app/journo-request/bay-area-tech-workers-laid-off-last-6-months-roles-changed-by-ai
- [low] 12d old — https://www.sourcee.app/journo-request/basementborn-entrepreneurs-built-businesses-despite-doubters
- [low] 12d old — https://www.sourcee.app/journo-request/software-developers-ai-impact-on-development-practices
- [low] 12d old — https://www.sourcee.app/journo-request/cios-ctos-and-senior-tech-leaders-working-with-ai-cio-summit-nyc-feb
- [low] 12d old — https://www.sourcee.app/journo-request/chatgpt-users-use-ai-to-run-their-lives-and-been-called-meat-proxy
- [low] 12d old — https://www.sourcee.app/journo-request/uk-tech-leaders-nvidia-role-in-infrastructure-finance-and-geopolitics
- [low] 12d old — https://www.sourcee.app/journo-request/uk-developers-ai-impact-on-job-satisfaction-and-careers
- [low] 12d old — https://www.sourcee.app/journo-request/cfpa-members-and-fluid-power-experts-spring-2027-articles
- [low] 13d old — https://www.sourcee.app/journo-request/women-writers-in-global-south-climate-care-and-environmental-justice
- [low] 13d old — https://www.sourcee.app/journo-request/ai-economist-tokenomics-and-market-winners-selfhosting-viability
- [low] 13d old — https://www.sourcee.app/journo-request/ai-safety-leaders-physical-ai-safety-and-zerotrust-infrastructure
- [low] 13d old — https://www.sourcee.app/journo-request/employees-at-anduril-and-9-ai100-firms-build-hire-and-sell
- [low] 15d old — https://www.sourcee.app/journo-request/job-seekers-postai-interviews-and-recruiters-ai-interview-impact
- [low] 15d old — https://www.sourcee.app/journo-request/midsize-manufacturing-it-leaders-ai-impact-on-tasks-teams-governance
- [low] 15d old — https://www.sourcee.app/journo-request/employees-using-ai-avatars-training-and-support-zdnet
- [low] 15d old — https://www.sourcee.app/journo-request/us-retail-executives-agentic-ai-shopping-in-ecommerce
- [low] 15d old — https://www.sourcee.app/journo-request/ev-industry-employees-insider-stories-and-source-protection
- [low] 15d old — https://www.sourcee.app/journo-request/microsoft-365-users-email-outage-impact-on-workflows
- [low] 15d old — https://www.sourcee.app/journo-request/individuals-accused-of-using-ai-misattribution-experiences
- [low] 15d old — https://www.sourcee.app/journo-request/servicenow-customers-and-partners-podcast-guests-ai-and-career-stories
- [low] 15d old — https://www.sourcee.app/journo-request/israeli-software-developers-ai-impact-on-jobs
- [low] 15d old — https://www.sourcee.app/journo-request/local-model-operators-10-prod-inference-and-7-figure-biz
- [low] 16d old — https://www.sourcee.app/journo-request/ramp-crews-and-gate-agents-hardest-and-best-job-moments
- [low] 16d old — https://www.sourcee.app/journo-request/innovators-and-changemakers-neuroscience-ai-future-of-work
- [low] 16d old — https://www.sourcee.app/journo-request/teachers-and-school-leaders-ai-in-school-devices-student-wellbeing
- [low] 16d old — https://www.sourcee.app/journo-request/accountants-and-bookkeepers-who-dont-use-ai-why-they-opt-out
- [low] 16d old — https://www.sourcee.app/journo-request/small-businesses-aidriven-cyber-risks-and-affordable-protections
- [low] 16d old — https://www.sourcee.app/journo-request/frontier-ai-industry-insiders-huang-resignation-impact-and-next-steps
- [low] 16d old — https://www.sourcee.app/journo-request/ai-leader-jensen-huang-resignation-ai-policy-and-china
- [low] 16d old — https://www.sourcee.app/journo-request/midterm-voters-on-ai-data-center-measure-why-they-voted
- [low] 16d old — https://www.sourcee.app/journo-request/ai-startup-founders-jensen-huang-resignation-impact-and-opensource
- [low] 16d old — https://www.sourcee.app/journo-request/msp-owners-resellers-and-integrators-ai-ops-security-and-supply-chain
- [low] 16d old — https://www.sourcee.app/journo-request/berlin-london-and-sf-ai-founders-and-tech-execs-podcast-tech-landscape
- [low] 16d old — https://www.sourcee.app/journo-request/individuals-and-small-businesses-accused-of-using-ai-false-allegations
- [low] 16d old — https://www.sourcee.app/journo-request/parents-of-students-with-loans-managing-cost-and-sacrifices-ipaper
- [low] 16d old — https://www.sourcee.app/journo-request/software-engineers-and-leaders-one-practical-engineering-question
- [low] 17d old — https://www.sourcee.app/journo-request/women-founders-deeptech-startups-biotech-space-ai-robotics
- [low] 17d old — https://www.sourcee.app/journo-request/facebook-marketplace-users-ai-impact-on-buying-and-selling
- [low] 17d old — https://www.sourcee.app/journo-request/telecom-policy-experts-international-telecom-sovereignty-research
- [low] 17d old — https://www.sourcee.app/journo-request/business-schools-ai-applications-in-teaching-and-operations-jan-2027
- [low] 17d old — https://www.sourcee.app/journo-request/job-candidates-interviewed-by-ai-interview-experience
- [low] 17d old — https://www.sourcee.app/journo-request/nova-scotia-residents-near-ai-data-centre-community-impact
- [low] 17d old — https://www.sourcee.app/journo-request/indian-cios-founders-investors-and-policymakers-sovereign-ai-challenges
- [low] 18d old — https://www.sourcee.app/journo-request/uk-ai-founders-compute-datacentre-and-grid-constraints
- [low] 18d old — https://www.sourcee.app/journo-request/ai-griefbot-creators-mimicking-deceased-loved-ones-doubletake
- [low] 18d old — https://www.sourcee.app/journo-request/uk-recruitment-expert-advice-on-losing-jobs-to-ai
- [low] 18d old — https://www.sourcee.app/journo-request/facebook-marketplace-users-ai-agents-impact-on-feed-spam-and-privacy
- [low] 18d old — https://www.sourcee.app/journo-request/jobseekers-in-ireland-resenting-ai-in-hiring-on-principle
- [low] 18d old — https://www.sourcee.app/journo-request/sales-leaders-and-ai-sales-tool-builders-ai-during-sales-calls
- [low] 18d old — https://www.sourcee.app/journo-request/designled-ai-practitioners-where-ai-transformations-stall
- [low] 18d old — https://www.sourcee.app/journo-request/cybersecurity-founder-and-ciso-ai-infra-ceo-scandal-risk-and-governance
- [low] 20d old — https://www.sourcee.app/journo-request/podcasters-and-linkedin-live-creators-tech-and-ai-and-career-topics
- [low] 21d old — https://www.sourcee.app/journo-request/human-behind-ai-crypto-agent-agentwritten-crypto-blogs
- [low] 22d old — https://www.sourcee.app/journo-request/people-with-friends-and-coworkers-who-disagree-on-ai-managing-tension
- [low] 22d old — https://www.sourcee.app/journo-request/woman-replaced-by-ai-and-recruitment-expert-ai-job-loss-case-study
- [low] 22d old — https://www.sourcee.app/journo-request/ai-founders-and-investors-in-barcelona-podcast-and-company-visit-guests
- [low] 22d old — https://www.sourcee.app/journo-request/prs-and-agents-celebrities-national-titles-interview-slots
- [low] 22d old — https://www.sourcee.app/journo-request/ai-users-and-relationship-therapists-dating-conflicts-breakups
- [low] 22d old — https://www.sourcee.app/journo-request/b2b-tech-and-software-sales-reps-and-leaders-real-customer-deal-lessons
- [low] 23d old — https://www.sourcee.app/journo-request/uk-job-hunters-12-months-job-market-climate-and-ai
- [low] 23d old — https://www.sourcee.app/journo-request/designers-and-creators-balancing-bills-family-and-meaningful-work
- [low] 23d old — https://www.sourcee.app/journo-request/early-career-workers-future-of-work-and-ai
- [low] 23d old — https://www.sourcee.app/journo-request/ai-and-virtual-influencer-creators-index-submission
- [low] 23d old — https://www.sourcee.app/journo-request/nar-nxt-safety-and-cybersecurity-experts-gen-ai-cybersecurity
- [low] 23d old — https://www.sourcee.app/journo-request/ai-policy-expert-possible-pause-on-ai-in-us
- [low] 23d old — https://www.sourcee.app/journo-request/data-center-workers-and-ai-execs-ban-ai-expansion-until-safety-rules
- [low] 23d old — https://www.sourcee.app/journo-request/doctoral-candidates-and-phd-holders-dissertation-writing-strategies
- [low] 23d old — https://www.sourcee.app/journo-request/postcolonial-scholars-and-former-coloniser-officials-citizenship-debate
- [low] 23d old — https://www.sourcee.app/journo-request/business-leaders-and-educators-headtohead-handwriting-in-business
- [low] 23d old — https://www.sourcee.app/journo-request/cisos-and-senior-cybersecurity-leaders-protecting-developers
- [low] 24d old — https://www.sourcee.app/journo-request/ai-data-center-operators-midterm-vote-backlash-impact
- [low] 24d old — https://www.sourcee.app/journo-request/canadian-real-estate-agents-foreign-buyer-ban-ending-jan-1-2027
- [low] 24d old — https://www.sourcee.app/journo-request/freelancers-small-businesses-and-employees-falsely-accused-of-ai-use
- [low] 24d old — https://www.sourcee.app/journo-request/anthropic-employees-company-decisionmaking-and-workplace-impact
- [low] 24d old — https://www.sourcee.app/journo-request/ai-policy-experts-tech-influence-on-midterms-tonight
- [low] 24d old — https://www.sourcee.app/journo-request/retail-workers-and-managers-instore-ai-impact-holiday-season
- [low] 24d old — https://www.sourcee.app/journo-request/generative-ai-documentation-experts-business-document-fraud-risk
- [low] 25d old — https://www.sourcee.app/journo-request/freelance-journalists-automation-feature-pitches
- [low] 25d old — https://www.sourcee.app/journo-request/former-muse-users-gave-up-on-ai-agents
- [low] 25d old — https://www.sourcee.app/journo-request/designers-on-large-teams-evolving-design-systems-dive-radio
- [low] 25d old — https://www.sourcee.app/journo-request/world-model-researchers-applications-in-robotics
- [low] 25d old — https://www.sourcee.app/journo-request/founders-selling-to-nurses-nurse-adoption-and-clinical-ai
- [low] 25d old — https://www.sourcee.app/journo-request/dallas-insurance-executives-private-capital-ai-rbc-reforms
- [low] 25d old — https://www.sourcee.app/journo-request/retail-executives-nrf-nyc-retail-media-supply-chain-and-ai
- [low] 25d old — https://www.sourcee.app/journo-request/regulators-and-compliance-experts-consumer-ai-mental-wellbeing
- [low] 25d old — https://www.sourcee.app/journo-request/newsletter-publishers-and-creators-state-of-newsletters-report-2027
- [low] 25d old — https://www.sourcee.app/journo-request/job-seekers-in-ireland-aiautomated-job-applications-experience
- [low] 25d old — https://www.sourcee.app/journo-request/biometrics-and-computer-vision-experts-proving-humanity-in-digital-age
- [low] 25d old — https://www.sourcee.app/journo-request/carleton-students-ai-use-in-dating-advice
- [low] 25d old — https://www.sourcee.app/journo-request/aussie-travellers-1861-hotel-tech-abandoned-bookings-and-ai-concerns
- [low] 25d old — https://www.sourcee.app/journo-request/young-adults-1835-ai-impact-on-comingofage
- [low] 25d old — https://www.sourcee.app/journo-request/people-with-ai-psychosis-firsthand-accounts
- [low] 25d old — https://www.sourcee.app/journo-request/new-authors-ai-market-dilution-and-fair-use-impact-on-writing
- [low] 25d old — https://www.sourcee.app/journo-request/marketers-and-creators-using-ai-agents-timesaving-wins
- [low] 25d old — https://www.sourcee.app/journo-request/ut-austin-students-ai-trump-crypto-ads-on-game-livestreams
- [low] 26d old — https://www.sourcee.app/journo-request/uk-recruiters-ai-impact-on-billing-and-candidate-matching
- [low] 26d old — https://www.sourcee.app/journo-request/global-and-european-marketing-leaders-investment-and-ops-challenges
- [low] 29d old — https://www.sourcee.app/journo-request/startup-founders-deciding-first-marketing-tests-on-tight-runway
- [low] 29d old — https://www.sourcee.app/journo-request/multifamily-professionals-ai-adoption-and-employee-chatbot-use
- [low] 29d old — https://www.sourcee.app/journo-request/canadian-ai-and-tech-companies-government-picking-winners-and-losers
- [low] 29d old — https://www.sourcee.app/journo-request/bank-and-brokerage-users-ai-tools-managing-personal-finances
- [low] 29d old — https://www.sourcee.app/journo-request/midlife-professionals-career-regret
- [low] 30d old — https://www.sourcee.app/journo-request/rig-hse-staff-aienabled-cameras-trial-outcomes
- [low] 30d old — https://www.sourcee.app/journo-request/current-ucla-students-and-faculty-ai-impact-on-majors
- [low] 30d old — https://www.sourcee.app/journo-request/founders-and-inclusion-leads-future-of-work-and-ai-impact
- [low] 30d old — https://www.sourcee.app/journo-request/uk-law-experts-and-ai-safety-researchers-chatbotaided-crime
- [low] 30d old — https://www.sourcee.app/journo-request/buyers-and-sellers-without-agents-diy-property-sale-experience
- [low] 30d old — https://www.sourcee.app/journo-request/editors-creatives-and-graphic-designers-ai-impact-documentary
- [low] 30d old — https://www.sourcee.app/journo-request/character-ai-users-emotional-attachment-and-loneliness
- [low] 31d old — https://www.sourcee.app/journo-request/users-who-linked-bank-and-brokerage-accounts-to-llms-ai-finance
- [low] 31d old — https://www.sourcee.app/journo-request/musicians-artists-writers-and-creators-ai-impact-on-creativity
- [low] 31d old — https://www.sourcee.app/journo-request/literary-writers-thoughts-on-lit-mags-funny-deep-frustrated
- [low] 31d old — https://www.sourcee.app/journo-request/ai-researchers-founders-and-tech-ceos-retirement-plans-amid-ai-risk
- [low] 31d old — https://www.sourcee.app/journo-request/canadian-skilled-trades-workers-ai-impact-on-manufacturing
- [low] 31d old — https://www.sourcee.app/journo-request/gcc-founders-and-entrepreneurs-ai-collaboration-and-data-sovereignty
- [low] 31d old — https://www.sourcee.app/journo-request/dairy-companies-and-startups-aipowered-livestock-health-and-nutrition
- [low] 32d old — https://www.sourcee.app/journo-request/excorporate-privacy-lead-built-privacy-and-ai-consultancy
- [low] 32d old — https://www.sourcee.app/journo-request/canadian-health-innovators-voices-of-innovation-canada-nov-16
- [low] 32d old — https://www.sourcee.app/journo-request/ai-startup-founders-and-marketers-b2b-marketing-as-show-business
- [low] 32d old — https://www.sourcee.app/journo-request/students-whose-professors-allow-ai-ai-use-in-coursework
- [low] 32d old — https://www.sourcee.app/journo-request/carleton-students-ai-dating-advice-impact-on-dating-experience
- [low] 32d old — https://www.sourcee.app/journo-request/former-software-engineers-turned-traders-pivot-after-layoff-or-ai
- [low] 32d old — https://www.sourcee.app/journo-request/members-club-and-hospitality-pros-in-hong-kong-postcovid-trends
- [low] 33d old — https://www.sourcee.app/journo-request/people-using-llms-as-companions-emotional-support-stories
- [low] 33d old — https://www.sourcee.app/journo-request/admissions-leaders-and-researchers-measuring-judgment-amid-ai
- [low] 33d old — https://www.sourcee.app/journo-request/celebrity-agents-how-i-manage-my-money-series
- [low] 33d old — https://www.sourcee.app/journo-request/ai-companies-in-utilities-and-construction-frontline-safety-and-workload
- [low] 33d old — https://www.sourcee.app/journo-request/sound-artists-and-field-recordists-run-radio-aarhus-open-call
- [low] 35d old — https://www.sourcee.app/journo-request/people-using-ai-for-social-advice-communication-and-connection-impact
- [low] 35d old — https://www.sourcee.app/journo-request/video-teams-using-claude-and-remotion-agentic-video-editing
- [low] 36d old — https://www.sourcee.app/journo-request/couples-letting-ai-dictate-relationship-emotions-and-intimacy
- [low] 36d old — https://www.sourcee.app/journo-request/people-recreating-iconic-runway-looks-halloween-costume-story
- [low] 36d old — https://www.sourcee.app/journo-request/parish-event-organizers-aigenerated-flyers-scourge-or-timesaver
- [low] 36d old — https://www.sourcee.app/journo-request/uk-and-eu-sports-retail-supply-chain-leaders-retail-ai-at-scale
- [low] 36d old — https://www.sourcee.app/journo-request/founders-and-cofounders-fortnightly-founder-qanda
- [low] 36d old — https://www.sourcee.app/journo-request/fanvue-chatters-nsfw-ai-model-experiences
- [low] 37d old — https://www.sourcee.app/journo-request/nontech-inhouse-corporate-comms-lead-ai-search-and-discovery-strategy
- [low] 37d old — https://www.sourcee.app/journo-request/geopolitical-analysts-and-ai-security-experts-global-hotspots
- [low] 37d old — https://www.sourcee.app/journo-request/digital-artists-aigenerated-posters-flooding-social-feeds
- [low] 37d old — https://www.sourcee.app/journo-request/founders-and-ctos-production-ai-tradeoffs-in-healthcare-and-fintech
- [low] 37d old — https://www.sourcee.app/journo-request/students-and-professionals-balancing-ai-use-and-human-focus
- [low] 37d old — https://www.sourcee.app/journo-request/rig-hse-officers-aienabled-camera-trial-outcomes
- [low] 37d old — https://www.sourcee.app/journo-request/anthropic-project-panama-employees-book-digitization-and-ai-training
- [low] 37d old — https://www.sourcee.app/journo-request/nj-parents-and-teachers-ai-school-surveillance-and-data-practices
- [low] 38d old — https://www.sourcee.app/journo-request/brand-managers-ai-to-deepen-customer-insight-and-preserve-humanity
- [low] 38d old — https://www.sourcee.app/journo-request/omaha-hr-representatives-offices-with-written-ai-policies
- [low] 38d old — https://www.sourcee.app/journo-request/bengaluru-founders-deep-tech-healthcare-biology-housing-and-ai
- [low] 38d old — https://www.sourcee.app/journo-request/fintech-product-managers-nextgen-aipowered-personal-finance-apps
- [low] 39d old — https://www.sourcee.app/journo-request/hr-leaders-and-organizational-design-practitioners-decision-fatigue
- [low] 39d old — https://www.sourcee.app/journo-request/cios-at-gartner-it-symposium-orlando-balancing-ai-risk-and-value
- [low] 39d old — https://www.sourcee.app/journo-request/estate-agents-and-property-lawyers-disclosure-rules-haunted-homes
- [low] 39d old — https://www.sourcee.app/journo-request/product-managers-on-512-engineer-teams-engineers-using-ai
- [low] 39d old — https://www.sourcee.app/journo-request/bay-area-agentic-ai-builders-agntcon-and-mcpcon-stories
- [low] 39d old — https://www.sourcee.app/journo-request/carleton-students-ai-impact-on-dating-experiences
- [low] 39d old — https://www.sourcee.app/journo-request/new-yorkers-ai-music-playing-in-cabs-and-local-businesses
- [low] 39d old — https://www.sourcee.app/journo-request/western-students-using-ai-companions-psychological-effects
- [low] 40d old — https://www.sourcee.app/journo-request/fb-marketplace-sellers-and-buyers-ai-impact-on-pricing-and-listings
- [low] 40d old — https://www.sourcee.app/journo-request/consumers-using-ai-for-financial-advice-experience-and-factchecking
- [low] 40d old — https://www.sourcee.app/journo-request/ai-energy-and-tax-experts-project-jupiter-documentary-new-mexico
- [low] 41d old — https://www.sourcee.app/journo-request/uk-customer-service-workers-daytoday-now-ai-automation-vs-human
- [low] 42d old — https://www.sourcee.app/journo-request/ai-saas-vendors-targeting-journalists-prs-and-marketers-case-studies
- [low] 42d old — https://www.sourcee.app/journo-request/real-estate-operators-ai-adoption-and-org-restructuring
- [low] 42d old — https://www.sourcee.app/journo-request/memphis-and-southaven-residents-and-env-advocates-xai-colossus-impact
- [low] 42d old — https://www.sourcee.app/journo-request/black-women-in-canada-ai-chatbots-and-healthcare-experiences
- [low] 42d old — https://www.sourcee.app/journo-request/engineering-leaders-leading-people-through-ai-changes
- [low] 42d old — https://www.sourcee.app/journo-request/ai-app-and-saas-founders-1k-mrr-youtube-feature-growth-tactics
- [low] 43d old — https://www.sourcee.app/journo-request/chemistry-undergrads-and-phd-students-ai-use-in-coursework-and-research
- [low] 43d old — https://www.sourcee.app/journo-request/ai-infrastructure-engineers-in-berlin-data-centers-and-bottlenecks
- [low] 43d old — https://www.sourcee.app/journo-request/residents-near-mumbai-ai-data-centres-power-and-water-strain
- [low] 43d old — https://www.sourcee.app/journo-request/single-family-office-cybersecurity-experts-ai-risks-and-opportunities
- [low] 44d old — https://www.sourcee.app/journo-request/cios-and-ai-leaders-ai-infrastructure-day2-ops-and-costs
- [low] 44d old — https://www.sourcee.app/journo-request/companies-and-data-buyers-selling-corporate-data-to-train-ai
- [low] 44d old — https://www.sourcee.app/journo-request/uk-political-analysts-disinformation-and-ai-manipulation-in-politics
- [low] 44d old — https://www.sourcee.app/journo-request/content-creators-using-ai-job-losses-and-ethics
- [low] 44d old — https://www.sourcee.app/journo-request/painters-and-photographers-ai-impact-on-art
- [low] 44d old — https://www.sourcee.app/journo-request/legal-assistants-paralegals-and-lawfirm-staff-jobs-eliminated-by-ai
- [low] 44d old — https://www.sourcee.app/journo-request/ai-companion-users-in-africa-friendship-and-emotional-impact
- [low] 44d old — https://www.sourcee.app/journo-request/pro-se-litigants-using-generative-ai-access-to-justice-impact
- [low] 45d old — https://www.sourcee.app/journo-request/school-leaders-and-ngo-staff-ai-adoption-challenges-across-sectors
- [low] 45d old — https://www.sourcee.app/journo-request/ai-policy-advisor-newsom-administration-ai-regulation
- [low] 45d old — https://www.sourcee.app/journo-request/uk-and-us-heads-of-data-and-ai-from-idea-to-production
- [low] 45d old — https://www.sourcee.app/journo-request/minnesotans-using-chatgpt-and-ai-tools-experiences-with-election-info
- [low] 46d old — https://www.sourcee.app/journo-request/global-development-professionals-using-ai-across-programs-and-policy
- [low] 46d old — https://www.sourcee.app/journo-request/african-founders-building-ai-companies-pitch-deck-realities
- [low] 46d old — https://www.sourcee.app/journo-request/higher-ed-nonfaculty-staff-ai-use-at-work
- [low] 46d old — https://www.sourcee.app/journo-request/podcast-guests-ai-channel-and-partner-ecosystem
- [low] 46d old — https://www.sourcee.app/journo-request/ai-infrastructure-professionals-in-london-capacity-europe-attendees
- [low] 46d old — https://www.sourcee.app/journo-request/b2b-vendors-buyers-pasting-proposals-into-ai-tools
- [low] 47d old — https://www.sourcee.app/journo-request/caine-prize-winners-gen-ai-accusations-targeting-black-writers
- [low] 47d old — https://www.sourcee.app/journo-request/software-engineers-who-left-tech-jobs-lost-to-ai-coding-tools
- [low] 47d old — https://www.sourcee.app/journo-request/manufacturers-and-ai-safety-experts-ai-risks-in-chemical-food-defense
- [low] 47d old — https://www.sourcee.app/journo-request/uk-baby-boomers-misinformation-sharing-and-ai-influence-online
- [low] 48d old — https://www.sourcee.app/journo-request/hedera-builders-shipping-defi-nfts-rwas-ai-games-and-memes
- [low] 48d old — https://www.sourcee.app/journo-request/production-designers-ai-impact-on-future-of-filmmaking
- [low] 48d old — https://www.sourcee.app/journo-request/ai-researchers-and-policy-experts-5-years-us-race-to-superintelligence
- [low] 49d old — https://www.sourcee.app/journo-request/ai-cybersecurity-iot-and-web3-founders-and-operators-news-submissions
- [low] 49d old — https://www.sourcee.app/journo-request/employees-pay-transparency-good-or-bad
- [low] 50d old — https://www.sourcee.app/journo-request/sales-reps-who-cold-call-and-email-how-ai-changed-outreach
- [low] 50d old — https://www.sourcee.app/journo-request/enterprise-ai-leaders-and-builders-realworld-deployment-and-strategy
- [low] 50d old — https://www.sourcee.app/journo-request/anthropic-gtm-leaders-scaling-300k-b2b-clients
- [low] 51d old — https://www.sourcee.app/journo-request/voters-who-used-ai-to-navigate-ballot-voting-experience
- [low] 51d old — https://www.sourcee.app/journo-request/hotel-and-fandb-supervisors-and-managers-customer-expectations-vs-ai
- [low] 51d old — https://www.sourcee.app/journo-request/researchers-founders-and-funders-ai-transforming-scientific-research
- [low] 51d old — https://www.sourcee.app/journo-request/facebook-marketplace-sellers-ai-listing-photos-and-selling-experience
- [low] 51d old — https://www.sourcee.app/journo-request/uk-ai-data-trainers-daytoday-work
- [low] 51d old — https://www.sourcee.app/journo-request/patent-attorneys-and-agents-startup-ip-starter-pack
- [low] 52d old — https://www.sourcee.app/journo-request/aps-hr-leaders-ai-skills-training-and-workforce-planning
- [low] 52d old — https://www.sourcee.app/journo-request/scrum-masters-daytoday-and-career-pivots-and-ai-impact
- [low] 52d old — https://www.sourcee.app/journo-request/real-estate-agents-replacing-pdf-property-brochure
- [low] 52d old — https://www.sourcee.app/journo-request/anz-marketers-ai-and-martech-innovation-spotlight
- [low] 52d old — https://www.sourcee.app/journo-request/solicitors-and-barristers-ai-to-expand-pro-bono-capacity
- [low] 52d old — https://www.sourcee.app/journo-request/apac-reporters-and-editors-ai-accountability-coverage
- [low] 52d old — https://www.sourcee.app/journo-request/early-to-midcareer-information-architects-products-featuring-ai
- [low] 52d old — https://www.sourcee.app/journo-request/martech-buyers-ai-impact-on-build-vs-buy-decisions
- [low] 52d old — https://www.sourcee.app/journo-request/swiss-ai-companion-users-emotional-bonds-and-daily-life
- [low] 52d old — https://www.sourcee.app/journo-request/ai-data-labelers-in-germany-positive-and-negative-experiences
- [low] 52d old — https://www.sourcee.app/journo-request/ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories
- [low] 53d old — https://www.sourcee.app/journo-request/ai-infrastructure-experts-china-vs-us-datacenter-capacity
- [low] 53d old — https://www.sourcee.app/journo-request/plaintiffs-attorneys-and-legal-scholars-ai-deepfake-liability
- [low] 53d old — https://www.sourcee.app/journo-request/coweta-county-artists-and-creatives-data-centers-and-ai-infrastructure
- [low] 53d old — https://www.sourcee.app/journo-request/ai-data-annotators-and-labellers-experience-with-ai-training-data
- [low] 53d old — https://www.sourcee.app/journo-request/academics-social-media-and-ai-impact-on-womens-identity-and-selfesteem
- [low] 53d old — https://www.sourcee.app/journo-request/emergency-managers-ai-tools-for-funding-and-staffing-shortfalls
- [low] 54d old — https://www.sourcee.app/journo-request/ai-liability-insurers-and-legal-experts-procurement-and-implementation
- [low] 54d old — https://www.sourcee.app/journo-request/uk-cybersecurity-hiring-managers-state-of-hiring-2026-and-ai-impact
- [low] 54d old — https://www.sourcee.app/journo-request/ai-emotional-support-users-chatbot-therapy-and-journaling
- [low] 54d old — https://www.sourcee.app/journo-request/mortgage-adviser-using-ai-efficiency-and-client-outcomes-video-series
- [low] 54d old — https://www.sourcee.app/journo-request/founders-and-cxos-in-automotive-ai-evs-autonomy-thought-leadership
- [low] 55d old — https://www.sourcee.app/journo-request/video-game-developer-falsely-accused-of-using-generative-ai
- [low] 56d old — https://www.sourcee.app/journo-request/lawyers-and-tech-ethics-experts-ai-wearables-and-legal-journeys
- [low] 57d old — https://www.sourcee.app/journo-request/storytellers-and-brand-founders-marys-big-30-ai-story-project
- [low] 57d old — https://www.sourcee.app/journo-request/newsletter-editors-using-ai-agents-news-aggregation-practices
- [low] 57d old — https://www.sourcee.app/journo-request/scottish-teachers-ai-tools-implementation-in-education
- [low] 57d old — https://www.sourcee.app/journo-request/mls-executives-risks-when-agents-grant-mls-access-to-llms
- [low] 57d old — https://www.sourcee.app/journo-request/real-estate-agents-and-brokers-switched-from-pdf-brochures
- [low] 57d old — https://www.sourcee.app/journo-request/advertising-tech-and-media-pros-in-miami-ai-audience-discovery
- [low] 57d old — https://www.sourcee.app/journo-request/hr-leaders-company-ai-strategies-and-cognitive-offloading-risk
- [low] 57d old — https://www.sourcee.app/journo-request/k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact
- [low] 58d old — https://www.sourcee.app/journo-request/fea-engineers-using-agentic-ai-practitioner-case-study
- [low] 58d old — https://www.sourcee.app/journo-request/fb-marketplace-sellers-ai-photos-and-description-prompts
- [low] 58d old — https://www.sourcee.app/journo-request/ai-summit-barcelona-attendees-controversy-and-experiences
- [low] 58d old — https://www.sourcee.app/journo-request/ai-glasses-owners-users-and-developers-in-india-product-experience
- [low] 58d old — https://www.sourcee.app/journo-request/parents-ai-acting-as-pseudoparent-in-kid-questions
- [low] 59d old — https://www.sourcee.app/journo-request/chatbot-users-experiences-talking-to-ai
- [low] 59d old — https://www.sourcee.app/journo-request/us-ai-security-experts-rogue-ai-agents-hitting-government-sites
- [low] 59d old — https://www.sourcee.app/journo-request/real-estate-agents-pdf-brochures-vs-alternatives-agent-workflow
- [low] 60d old — https://www.sourcee.app/journo-request/cybersecurity-expert-ai-nexus-and-security-risks
- [low] 60d old — https://www.sourcee.app/journo-request/us-emergency-physicians-and-paramedics-impact-of-ai-answering-911-calls
- [low] 60d old — https://www.sourcee.app/journo-request/job-seekers-and-recruiters-ai-recruitment-experiences
- [low] 61d old — https://www.sourcee.app/journo-request/data-center-operators-and-cloud-buyers-proof-of-deployable-ai-capacity
- [low] 61d old — https://www.sourcee.app/journo-request/b2b-marketing-leaders-hyperspecialization-to-outcompete-ai
- [low] 61d old — https://www.sourcee.app/journo-request/ai-practitioners-and-team-leads-real-ai-deployments-failures-and-fixes
- [low] 67d old — https://www.sourcee.app/journo-request/saas-tools-for-gated-content-lead-gen-and-doc-tracking-q4-roundup
- [low] 67d old — https://www.sourcee.app/journo-request/ai-hardware-makers-3d-printing-smart-devices-mini-robots-local-ai
- [low] 68d old — https://www.sourcee.app/journo-request/sales-enablement-saas-tools-proposal-and-deck-engagement-tracking
- [low] 68d old — https://www.sourcee.app/journo-request/london-businesses-stopped-using-ai-hiring-tools
- [low] 68d old — https://www.sourcee.app/journo-request/engineering-managers-measuring-engineers-when-using-ai
- [low] 68d old — https://www.sourcee.app/journo-request/creative-industry-professionals-podcast-on-ai-impact
- [low] 68d old — https://www.sourcee.app/journo-request/former-ai-skeptics-changed-views-on-ai-impact
- [low] 69d old — https://www.sourcee.app/journo-request/employers-and-recruiters-over-50s-adapting-to-ai
- [low] 69d old — https://www.sourcee.app/journo-request/data-center-professionals-podcast-guest-ai-and-hyperscale-trends
- [low] 69d old — https://www.sourcee.app/journo-request/patients-with-exorbitant-hospital-bills-billing-errors-and-overcharges
- [low] 69d old — https://www.sourcee.app/journo-request/founders-and-leaders-mindsets-and-milestones
- [low] 69d old — https://www.sourcee.app/journo-request/ml-researchers-continuous-learning-fast-weights-and-adapters
- [low] 69d old — https://www.sourcee.app/journo-request/founders-55-latelife-entrepreneurship-series-1
- [low] 69d old — https://www.sourcee.app/journo-request/founders-and-entrepreneurs-and-musicians-podcast-guests
- [low] 69d old — https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- [low] 70d old — https://www.sourcee.app/journo-request/ai-alignment-researchers-humanai-mutual-understanding
- [low] 71d old — https://www.sourcee.app/journo-request/companies-that-stopped-emailing-pdfs-new-tools-and-transition
- [low] 72d old — https://www.sourcee.app/journo-request/gen-z-ai-data-annotators-work-experience-and-income-impact
- [low] 72d old — https://www.sourcee.app/journo-request/ecommerce-marketers-transparency-in-ai-recommendations-and-conversion
- [low] 72d old — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 73d old — https://www.sourcee.app/journo-request/cybersecurity-companies-and-experts-ai-scams-and-consumer-safety
- [low] 73d old — https://www.sourcee.app/journo-request/ai-automation-experts-speakers-on-marketing-sales-operations-gains
- [low] 141d old — https://www.sourcee.app/journo-request/investigative-reporters-openai-training-predatory-dynamic-pricing

## Dropped off the feed

Still fetching, but absent from the newest digest — colder than the age says.

- [high] 79d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-saas-users-in-production-integrations-and-autonomous-workflows
- [medium-high] 79d old — page no longer serves the request — https://www.sourcee.app/journo-request/msp-experts-and-case-studies-ai-ops-and-pricing-and-backup-trends
- [medium] 78d old — page no longer serves the request — https://www.sourcee.app/journo-request/earlystage-founders-building-saas-and-ai-tools-built-from-scratch
- [low] 72d old — page no longer serves the request — https://www.sourcee.app/journo-request/ediscovery-lawyers-aiassisted-review-impact-on-practice
- [low] 69d old — page no longer serves the request — https://www.sourcee.app/journo-request/survivors-of-ai-and-autonomous-weapons-civilian-impact-testimonies
- [low-medium] 60d old — page no longer serves the request — https://www.sourcee.app/journo-request/insurance-agents-ai-use-in-personal-lines
- [low] 58d old — page no longer serves the request — https://www.sourcee.app/journo-request/parents-ai-acting-as-pseudoparent-in-kid-questions
- [low-medium] 58d old — page no longer serves the request — https://www.sourcee.app/journo-request/employees-conflicted-about-ai-use-generative-ai-workplace-impact
- [low] 57d old — page no longer serves the request — https://www.sourcee.app/journo-request/k8-and-hs-teachers-using-studentfacing-ai-moratorium-impact
- [low] 53d old — page no longer serves the request — https://www.sourcee.app/journo-request/emergency-managers-ai-tools-for-funding-and-staffing-shortfalls
- [low] 52d old — page no longer serves the request — https://www.sourcee.app/journo-request/swiss-ai-companion-users-emotional-bonds-and-daily-life
- [low] 52d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-data-labelers-in-germany-positive-and-negative-experiences
- [low] 52d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-chatbot-users-and-therapists-selfdiagnosing-mental-health-stories
- [low] 51d old — page no longer serves the request — https://www.sourcee.app/journo-request/uk-ai-data-trainers-daytoday-work
- [low] 51d old — page no longer serves the request — https://www.sourcee.app/journo-request/patent-attorneys-and-agents-startup-ip-starter-pack
- [low] 45d old — page no longer serves the request — https://www.sourcee.app/journo-request/minnesotans-using-chatgpt-and-ai-tools-experiences-with-election-info
- [low] 44d old — page no longer serves the request — https://www.sourcee.app/journo-request/painters-and-photographers-ai-impact-on-art
- [low] 44d old — page no longer serves the request — https://www.sourcee.app/journo-request/legal-assistants-paralegals-and-lawfirm-staff-jobs-eliminated-by-ai
- [low] 44d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-companion-users-in-africa-friendship-and-emotional-impact
- [low] 44d old — page no longer serves the request — https://www.sourcee.app/journo-request/pro-se-litigants-using-generative-ai-access-to-justice-impact
- [low] 42d old — page no longer serves the request — https://www.sourcee.app/journo-request/ai-app-and-saas-founders-1k-mrr-youtube-feature-growth-tactics
- [low] 39d old — page no longer serves the request — https://www.sourcee.app/journo-request/carleton-students-ai-impact-on-dating-experiences
- [low] 39d old — page no longer serves the request — https://www.sourcee.app/journo-request/new-yorkers-ai-music-playing-in-cabs-and-local-businesses
- [low] 39d old — page no longer serves the request — https://www.sourcee.app/journo-request/western-students-using-ai-companions-psychological-effects
- [low] 37d old — page no longer serves the request — https://www.sourcee.app/journo-request/anthropic-project-panama-employees-book-digitization-and-ai-training
- [low] 37d old — page no longer serves the request — https://www.sourcee.app/journo-request/nj-parents-and-teachers-ai-school-surveillance-and-data-practices
- [low] 36d old — page no longer serves the request — https://www.sourcee.app/journo-request/fanvue-chatters-nsfw-ai-model-experiences
- [low] 33d old — page no longer serves the request — https://www.sourcee.app/journo-request/sound-artists-and-field-recordists-run-radio-aarhus-open-call
- [low] 32d old — page no longer serves the request — https://www.sourcee.app/journo-request/students-whose-professors-allow-ai-ai-use-in-coursework
- [low] 32d old — page no longer serves the request — https://www.sourcee.app/journo-request/carleton-students-ai-dating-advice-impact-on-dating-experience
- [low] 32d old — page no longer serves the request — https://www.sourcee.app/journo-request/former-software-engineers-turned-traders-pivot-after-layoff-or-ai
- [low] 32d old — page no longer serves the request — https://www.sourcee.app/journo-request/members-club-and-hospitality-pros-in-hong-kong-postcovid-trends
- [low] 30d old — page no longer serves the request — https://www.sourcee.app/journo-request/buyers-and-sellers-without-agents-diy-property-sale-experience
- [low] 30d old — page no longer serves the request — https://www.sourcee.app/journo-request/editors-creatives-and-graphic-designers-ai-impact-documentary
- [low] 30d old — page no longer serves the request — https://www.sourcee.app/journo-request/character-ai-users-emotional-attachment-and-loneliness
- [low] 25d old — page no longer serves the request — https://www.sourcee.app/journo-request/carleton-students-ai-use-in-dating-advice
- [low] 25d old — page no longer serves the request — https://www.sourcee.app/journo-request/aussie-travellers-1861-hotel-tech-abandoned-bookings-and-ai-concerns
- [low] 25d old — page no longer serves the request — https://www.sourcee.app/journo-request/young-adults-1835-ai-impact-on-comingofage
- [low] 25d old — page no longer serves the request — https://www.sourcee.app/journo-request/people-with-ai-psychosis-firsthand-accounts
- [low] 25d old — page no longer serves the request — https://www.sourcee.app/journo-request/new-authors-ai-market-dilution-and-fair-use-impact-on-writing
- [low] 25d old — page no longer serves the request — https://www.sourcee.app/journo-request/marketers-and-creators-using-ai-agents-timesaving-wins
- [low] 25d old — page no longer serves the request — https://www.sourcee.app/journo-request/ut-austin-students-ai-trump-crypto-ads-on-game-livestreams
- [low] 2d old — left the newest Sourcee AI topic feed; page still live, but colder than age suggests — https://www.sourcee.app/journo-request/people-bringing-ai-partners-to-couples-therapy-relationship-impact
- [low] 2d old — left the newest Sourcee AI topic feed; page still live, but colder than age suggests — https://www.sourcee.app/journo-request/food-delivery-and-grocery-app-users-ai-chatbot-customer-care-issues
- [low] 2d old — left the newest Sourcee AI topic feed; page still live, but colder than age suggests — https://www.sourcee.app/journo-request/uk-ai-and-data-centre-experts-economic-and-environmental-impact
- [low] 2d old — left the newest Sourcee AI topic feed; page still live, but colder than age suggests — https://www.sourcee.app/journo-request/traveltech-companies-agentic-ai-systems-in-hospitality-and-booking

---

## Clearing the queue

After sending, record it so the row does not reappear:

```json
{"pitched": {"<url>": "2026-09-15"}, "skipped": {"<url>": "reason"}}
```

Ledger: `marketing/haro-outreach/pitch-ledger.json`
