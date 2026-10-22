# Pitch drafts — 2026-10-22

**Nothing here has been sent. Nothing here will be sent by the monitor.** 171 tracked requests,
**54 live unpitched, 0 sendable** (`pitch-queue.md`, built 2026-10-22). No pitch has gone out since the
four George authorised on 2026-10-10; the ledger records six `pitched` entries in total, five delivered
and one bounced.

**Zero sendable is not zero to send.** Today's window produced 96 slugs, 6 with an AI token, **0 with
an AI token plus a spend token**, all 96 bodies read: nothing new on the cost beat. The 8 rows added
this run are the 6 AI-token slugs plus the 2 body-level AI hits the slug filter cannot see — seven are
standing-only calls with no published route (in-house comms leader, an Anthropic insider, a geopolitical
analyst, an Omaha HR rep, an NJ parent/teacher, a Bengaluru podcast founder, an AI-art request) and the
eighth is a paid-placement advert recorded as DO NOT PITCH. Full reasoning in
`digest-2026-10-22.json`; none is drafted.

**What is drafted is the two rows that already had paste-ready pitches and live routes and were never
sent.** Both are past the 10-day cold line. The line is this monitor's own heuristic, not the
platform's: neither page carries an expiry, both routes answer HTTP 200 today. A late send or a
ledger `skipped` entry closes each one. Silence leaves them drifting — which is exactly how the
monitor reached 43 finds and zero sends.

**Figures are re-derived at build time, never typed.** `data/tools.json` holds **88 tools**;
`data/pricing_snapshots.json` (`updated: 2026-10-22`) yields **44 with a published monthly price, 35 of
those at or under $25/month, median $17.50**. Monthly-versus-annual: **1.11x to 2.53x, median 1.25x
over 19 tiers** (`data/monthly_annual_pairs.json`, built 2026-10-16). Per-tool figures carry their own
check dates from `data/tool_sources.json` — Browse AI 2026-09-18, Gamma 2026-10-01.
**The headline set moved with today's snapshot refresh** (from 84/43/34/$18.00 quoted in the 2026-10-21
file), so any older draft quoting 84 tools, 43 priced or $18.00 is stale and must not be sent.

---

## 1. Fast Company Work Life — AI at work, jobs and hiring ◀ 12d, LATE SEND — EMAIL

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **12 days.** Page re-read today: HTTP 200, body still served,
`datePublished 2026-10-10T13:51:49Z`, no expiry notice.
**Who:** **Tobi Amure** — the page's own author field. He is sourcing for **Fast Company's Work Life
section**, with an "AI at work: what it is really changing about jobs, teams and hiring" lane open.
**Ask, in his words:** *"For experts: the credential and the research behind it. Original data, or a
survey with its sample size and method. Workplace expert is not a credential."* He is **"not placing
bylined guest posts"**, so this offers a dataset and a call, never a post.
**The door:** *"No DM pitches here on LinkedIn. Email me."*

**Reply route:** **hello@tobiamure.com** — self-published on his own site, not the platform's.
Re-probed today (`route-checks-2026-10-22.json`): **https://tobiamure.com/** HTTP 200, 62,628 bytes,
title "Tobi Amure, CFEI® | Finance & Technology Journalist", address present; fallback
**https://tobiamure.com/contact/** HTTP 200, 17,762 bytes, address plus a contact form.
**Deliverability is not SMTP-verified.** `tobiamure.com` MX is Namecheap forwarding and answers
554 5.7.1 Relay access denied for `hello@`, a fake control and `postmaster@` alike — it refuses every
recipient from an outside probe, so that test discriminates nothing. The evidence is self-publication
on his live site, and a bounce is itself the answer.
**Automatable? No.** It is one plain email, but sends are George's lane and the monitor has never sent
one.

**Subject:** `The $17.50 median: method and denominator first`

> Hi Tobi —
>
> Method first, since that is the bar you set: we hand-check official vendor pricing pages for 88 AI tools and store the date of each check. As of today, 2026-10-22, 44 of them publish a monthly per-seat price, 35 of those start at or under $25/month, and the median cheapest paid tier is $17.50.
>
> The same set answers the annual-discount question: paying monthly rather than yearly costs between 1.11x and 2.53x, median 1.25x across 19 tiers, pair set re-asserted 2026-10-16. Two rows with their check dates: Browse AI Personal is $48/month or $19/month billed annually (browse.ai/pricing, checked 2026-09-18); Gamma Pro is $18/seat/month-equivalent on either term (gamma.app/pricing, checked 2026-10-01).
>
> For your AI-at-work lane that is the personal-economics half — what a seat costs the person using it, and how often they pay it out of pocket.
>
> You asked for the credential too. I do not have one to offer; I have a dated dataset, its method and the source URL behind every number, free to use.
>
> AIToolsEssentials

*Draft length: 169 words including the signature — measured on this file with a word count, not
asserted. Under the 200-word ceiling.*

---

## 2. WSJ blocked work accounts — what the workaround buyer pays ◀ 17d, LATE SEND — LINKEDIN DM

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **17 days.** Page re-read today: HTTP 200, body still served, no
expiry notice. It crossed the 10-day cold line on 2026-10-16 and has been carried unsent since.
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist.
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work
by hand.

**Honesty constraint — read before sending.** The request wants the respondent's own personal
annoyance. We are a publisher, not a blocked employee. The draft says so in its first sentence. Do not
edit it out.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — re-probed
today: HTTP 200, 623,445 bytes, title "Christopher Mims - The Wall Street Journal | LinkedIn". The
request's own body says "(DMs open)".
**Automatable? No.** No address, no form, no scheduling link — the text below is the whole message, and
it has to be sent from George's own LinkedIn.
Dead ends recorded so they are not retried as routes (re-probed today): `muckrack.com/christopher-mims`
→ HTTP 403; `wsj.com/news/author/christopher-mims` → HTTP 401.

> Hi Christopher — three numbers first, because I can't give you the personal account you asked for: I'm a publisher, not a blocked employee.
>
> We hand-check the list price of 88 AI tools. 44 publish a monthly price and 35 of those start at or under $25/month — median $17.50, re-checked today (2026-10-22).
>
> That is what the people who route around a blocked work account pay. Browse AI is $48/month against $19/month billed annually (browse.ai/pricing, checked 2026-09-18) — a 2.53x penalty for paying monthly out of pocket. Gamma's Pro seat is $18/month-equivalent on either term (gamma.app/pricing, checked 2026-10-01), so the penalty is real but not universal.
>
> Cheap enough for a personal card without asking anyone, expensive enough to add up across a year, and invisible to whoever holds the budget.
>
> Happy to send the full dated set, source URL for every number, no charge.
>
> AIToolsEssentials

*Draft length: 145 words including the signature — measured on this file with a word count, not
asserted. Under the 200-word ceiling.*

---

## 3. No third draft, and why

The other live rows all fail on one of two facts, and both are recorded per row in
`digest-2026-10-22.json`:

- **No route.** The request body's address is redacted by Sourcee and the page publishes no handle,
  form or booking link. That is true of the window's most credible row,
  `nj-parents-and-teachers-ai-school-surveillance-and-data-practices` (Nicole Rosenthal, NJ.com) — and
  that row also wants a New Jersey parent or teacher, which we are not.
- **No standing.** `cios-and-ai-leaders-ai-infrastructure-day2-ops-and-costs` (7 days) is the freshest
  request that actually asks "what it really costs" — and it states in its own body *"As this story
  focuses on end-user experience, we will not be taking vendor quotes."* We are a vendor of nothing but
  data; pitching it would be the exact misrepresentation this queue exists to prevent.

A draft with no route and false standing is a file, not a pitch. Two paste-ready sends with live
routes beat three where one is theatre.
