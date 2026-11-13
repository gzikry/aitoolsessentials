# Pitch drafts — 2026-11-13

**Three drafts, three sends, all George's lane. Nothing below has been sent.**

303 tracked requests, **64 live unpitched, 1 sendable** (`pitch-queue.md`, built 2026-11-13),
43 dead on the platform, **0 newly expired today**. The one sendable row is **InformationWeek /
Kelsey Ziser, 3 days old** — the only request inside the 10-day line with both an on-beat angle and
a resolved direct address. The other two are live and late (17 and 16 days) against this monitor's
own cold line, not against any deadline the reporters stated.

**Send in this order: §1 (3d, one click in Gmail Drafts), then §2 (one email closes two Forbes rows),
then §3 (a LinkedIn DM, which cannot be staged).**

**Today's 93-slug window produced nothing sendable and nothing on-beat.** 12 AI-token slugs, 1 AI+spend
at slug level, 15 body-level AI hits, all 93 bodies read. Four of the twelve are the same story —
Jensen Huang's resignation — from USA Today, ISMG, Inc. and a frontier-AI panel; the rest are
testimony asks from inside a job, podcast guest calls, and one pricing-models ask (Agam Shah,
token → outcome-based contracts) that excludes us by its own terms: *"Only those who have made
switches, no SMEs."* Full accounting in `digest-2026-11-13.json`.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **110 tools**;
`data/pricing_snapshots.json` (`updated: 2026-11-13`) yields **45 with a published monthly
per-seat price, 36 of those at or under $25/month, median $16.00**. Monthly vs annual:
**1.11x to 2.53x, median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, re-asserted
2026-10-16). Superseded, do not reuse: every 109-tool draft (2026-11-12 — including drafts 62/63
that sat unsent in Gmail), every 105-tool / $16.50 draft (2026-11-09 and before) and every
99-tool / $17.50 draft before 2026-11-03.

**Mailbox: zero replies**, measured today with `jansuski.com` as a positive control that returned
its two known messages (234, 305). No reply to any pitch since 2026-10-11; nothing sent since
2026-10-10.

---

## 1. InformationWeek — CIOs on the SaaSpocalypse and temporary AI ◀ 3d, EMAIL, FRESH, SEND FIRST

**Source:** https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai
**Posted:** 2026-11-09 20:11 UTC — **3 days.** Page read today: HTTP 200, body served,
`datePublished 2026-11-09T20:11:11.759Z`, badge *"Posted in last 7 days"*, no expiry notice.
**Who:** **Kelsey Ziser**, Senior Editor, InformationWeek. The page's author field names her; her
author page is `informationweek.com/author/kelsey-ziser` (HTTP 200, 579,285 bytes today).
**Ask, her words:** *"looking for CIOs to discuss... thoughts on the SaaSpocalypse? - are there any
use cases where you deploy a temporary AI tool?"* — five topics, two of them pricing questions.

**Reply route:** **kelsey.ziser@informationweek.com** — **automatable? No.** Published as a
`mailto:` link on her InformationWeek author page; the request page itself publishes no address.
The send is George's.
- Route probe today: HTTP 200, 579,285 bytes, title *"Kelsey Ziser | Senior Editor, InformationWeek"*.
- She asks for CIOs. We are a price census, not a CIO, and the draft says so in the first paragraph.

**Subject:** `The seat-price numbers behind the SaaSpocalypse question`

> Hi Kelsey —
>
> You asked CIOs about the SaaSpocalypse and temporary AI deployments. I'm not a CIO, so I won't answer as one. What I can give you is the seat-price floor beneath that question.
>
> Of the 110 AI tools we track, 45 publish a monthly per-seat price; 36 of those sit at or under $25, and the median cheapest paid seat is $16.00 (snapshot 2026-11-13, every tier read off the vendor's own pricing page with its check date).
>
> The billing split is the part that speaks to a temporary deployment: across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16). That premium is what a buyer pays for the right to switch a tool off, which is the trade-off your temp-AI question implies.
>
> Every figure carries its vendor URL and check date. Use the dataset free for the SaaSpocalypse or temporary-AI piece, with or without attribution. If you need a CIO voice rather than a price census, I'm the wrong source and I'll say so.
>
> AIToolsEssentials

*Word count: 174 including the signature — measured on this file; subject line excluded.*

**Stageable:** yes — `scripts/stage_pitch_drafts.py` writes this to `[Gmail]/Drafts`; sending is George's.

---

## 2. Forbes — US solopreneurs, and bootstrapped founders who can quantify what AI removed ◀ 17d, EMAIL, LATE

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **17 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-27T12:57:38Z`, badge *"Posted 17 days ago"*, no expiry notice.
**Who:** **Alison Coleman**, Forbes senior contributor covering entrepreneurs and their startups.
**Ask, her words:** *"Looking for US #solopreneurs, genuinely one-person business that have used AI to
eliminate the need to hire, or simply change when and why the first hire happens."*

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** A published email; the send is
George's.
- Re-probed today: https://www.alisoncoleman.co.uk/contact-me/ **HTTP 200, 28,112 bytes**, address in
  visible body text beside a Contact Form 7 form; `forbes.com/sites/alisoncoleman/` remains outside
  our reach (HTTP 403 in earlier probes — dead end, do not retry).
- One send closes both Forbes rows. Deliverability is not SMTP-verified; only a bounce proves
  anything.

**Subject:** `What the AI stack costs when it stands in for a first hire`

> Hi Alison —
>
> $16.00 is the median cheapest paid seat among the AI tools we track, 45 of 110 publishing a monthly per-seat price (snapshot 2026-11-13). Five seats is $80 a month, $960 a year — the number a US solo founder weighs against a first salary, which is the comparison your solopreneurs call asks for.
>
> I can't answer from inside a one-person business, so I won't pretend to. What I do is a dated price census: every tier read off the vendor's own pricing page, check date attached. Across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16), so the annual figure is the honest one to quote.
>
> Your bootstrapped-founders call, posted seven minutes earlier, is the same arithmetic on the capital side, so one dataset answers both. I saw the UK compute call you posted since; I have nothing on data centres, so this stays on the two US ones.
>
> Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 167 including the signature — measured on this file; subject line excluded.*

**Stageable:** yes — staged in `[Gmail]/Drafts` from this file today; yesterday's 109-tool copy is
deleted so only one version exists.

---

## 3. Business Today — workplace AI adoption and the skills to use the tools ◀ 16d, LINKEDIN DM, LATE

**Source:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
**Posted:** 2026-10-28 11:24 UTC — **16 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-28T11:24:30Z`, badge *"Posted 16 days ago"*, no expiry notice.
**Who:** **Vidhya Das**, Business Today (India Today group); author page
`businesstoday.in/author/vidhya-das`.
**Ask, her words:** *"how employees are adapting to the growing use of artificial intelligence (AI) in
the workplace, and what it takes to use these tools effectively"* — she wants *"independent AI experts,
enterprise AI trainers, researchers and technology professionals"*.

**Reply route:** **LinkedIn DM to linkedin.com/in/vidya-das** — **automatable? No.**
- The body redacts her email and offers *"comment below or DM me on LinkedIn"*. The handle was
  search-resolved on 2026-10-29 and re-confirmed 2026-11-12 at snippet level; a direct fetch of the
  profile still returns HTTP 999 (LinkedIn blocks it), so the DM is the one route no script can
  stage or check.
- No deadline stated on the page. The 10-day figure is this monitor's own line.

**First line does the work (a DM has no subject):**

> Hi Vidhya — $16.00 is the median cheapest paid seat among the AI tools we track, 45 of 110 publishing a monthly price (snapshot 2026-11-13). Five seats is about $960 a year. That number sits underneath your adoption story: the spend is small enough that an employee can adopt a tool without asking anyone, so training lags adoption rather than causing it.
>
> I'm not a trainer, so I'm not pitching that angle. I run a dated price census — every tier read off the vendor's own pricing page, each with its check date — and I can give you the seat and billing numbers behind the skills question. Across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16).
>
> Every figure carries its vendor URL and check date. Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 142 including the signature — measured on this file.*

**Cannot be staged:** a LinkedIn DM has no mailbox artefact. Paste it yourself.

---

## Why there is no fourth draft

The 15 rows added today were read and excluded, not silently dropped: a token-to-outcome pricing
call that bars anyone who has not switched contracts (no route published either), four separate
Huang-resignation reaction calls, AI-interview candidates and recruiters, Freshworks' manufacturing-IT
series (practitioners only, closing end of next week), ZDNET's AI-avatar workplaces, a US retail-exec
podcast booking, midterm voters on a data-centre ballot measure, Inc.'s startup founders, Channel
Insider's MSP/partner call, a Berlin/London/SF founder podcast, a false-AI-accusation testimony call,
an EV-industry whistleblower call and a Coding Chats guest call (both of the last two carry no AI
question at all — they are body-level hits on a passing AI mention), and an iPaper student-loans
case-study call. Full read on each in `digest-2026-11-13.json`.

## Still open past the line — send late or record skipped

- **WSJ / Christopher Mims** — `employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`,
  **39 days**. Route `linkedin.com/in/christopher-mims-club/` (HTTP 200 today). Draft in
  `pitch-drafts-2026-10-27.md` §3.
- **Tobi Amure** — `tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring`, **34 days**.
  Route `hello@tobiamure.com` (contact form as fallback). Draft in `pitch-drafts-2026-10-28.md` §3.
- **Anthropic / customer service** — `anthropic-users-and-business-owners-customer-service-experiences`,
  **63 days**. Route Signal `hliwrites.99`. Draft in `pitch-drafts-2026-09-22.md` §2.
- **FinOps / Niloy Ghosh** — `finops-professionals-agentic-ai-cost-overruns`, **67 days**, the
  longest-standing high-relevance request this monitor has never answered. Route: LinkedIn DM to
  `linkedin.com/in/niloy-ghosh`. Draft in `pitch-drafts-2026-09-17.md` §1. Do not draft it a fifth time.
