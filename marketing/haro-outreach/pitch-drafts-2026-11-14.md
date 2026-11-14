# Pitch drafts — 2026-11-14

**Three drafts, three sends, all George's lane. Nothing below has been sent.**

308 tracked requests, **64 live unpitched, 1 sendable** (`pitch-queue.md`, built today), 43 dead on
the platform, **0 newly expired**. The one sendable row is **InformationWeek / Kelsey Ziser, 4 days
old** — the only request inside the 10-day line with both an on-beat angle and a resolved direct
address. The other two are live and late (18 and 17 days) against this monitor's own cold line, not
against any deadline either reporter stated.

**Send in this order: §1 (4d, one click in Gmail Drafts), then §2 (one email closes two Forbes
rows), then §3 (a LinkedIn DM, which cannot be staged).**

**Today's 80-slug window produced nothing sendable and nothing on-beat.** 5 AI-token slugs, 0 AI+spend,
4 body-level AI hits, all 80 bodies read. Three of the five are first-person testimony asks (an
Israeli developer whose job AI changed, people wrongly accused of using AI, Microsoft 365 users hit by
yesterday's outage), one is a ServiceNow vendor podcast guest call, and one wants someone running 10%+
of production inference on local models inside a seven-figure business. None publishes an address,
handle or link. Full accounting in `digest-2026-11-14.json`.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **111 tools**;
`data/pricing_snapshots.json` (`updated: 2026-11-14`) yields **45 with a published monthly per-seat
price, 36 of those at or under $25/month, median $16.00**. Monthly vs annual: **1.11x to 2.53x, median
1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, re-asserted 2026-10-16). Superseded, do not
reuse: every 110-tool draft (2026-11-13 — including Gmail drafts 64 and 65), every 109-tool draft
(2026-11-12), every 105-tool / $16.50 draft (2026-11-09 and earlier) and every 99-tool / $17.50 draft
before 2026-11-03.

**Mailbox: zero replies**, measured today with `jansuski.com` as a positive control that returned its
two known messages (234, 305). No reply to any pitch since 2026-10-11; nothing sent since 2026-10-10.
Sent folder's newest items are vendor submission notes (2026-11-14 13:57Z), not pitches.

---

## 1. InformationWeek — CIOs on the SaaSpocalypse and temporary AI ◀ 4d, EMAIL, FRESH, SEND FIRST

**Source:** https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai
**Posted:** 2026-11-09 20:11 UTC — **4 days.** Page read today: HTTP 200, body served,
`datePublished 2026-11-09T20:11:11.759Z`, badge *"Posted in last 7 days"*, no expiry notice.
**Who:** **Kelsey Ziser**, Senior Editor, InformationWeek. The page's author field names her; her
author page is `informationweek.com/author/kelsey-ziser` (HTTP 200, 582,084 bytes today).
**Ask, her words:** *"looking for CIOs to discuss... thoughts on the SaaSpocalypse? - are there any
use cases where you deploy a temporary AI tool?"* — five topics, two of them pricing questions.

**Reply route:** **kelsey.ziser@informationweek.com** — **automatable? No.** Published as a
`mailto:` link on her InformationWeek author page; the request page itself publishes no address.
The send is George's.
- Route probe today (`route-checks-2026-11-14.json`): HTTP 200, 582,084 bytes, title *"Kelsey Ziser |
  Senior Editor, InformationWeek"*, address present once as `Kelsey.ziser@` and once as
  `kelsey.ziser@` in the markup.
- She asks for CIOs. We are a price census, not a CIO, and the draft says so in the first paragraph.

**Subject:** `The seat-price numbers behind the SaaSpocalypse question`

> Hi Kelsey —
>
> You asked CIOs about the SaaSpocalypse and temporary AI deployments. I'm not a CIO, so I won't answer as one. What I can give you is the seat-price floor beneath that question.
>
> Of the 111 AI tools we track, 45 publish a monthly per-seat price; 36 of those sit at or under $25, and the median cheapest paid seat is $16.00 (snapshot updated 2026-11-14, every tier read off the vendor's own pricing page with its check date).
>
> The billing split is the part that speaks to a temporary deployment: across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (pair set re-asserted 2026-10-16). That premium is what a buyer pays for the right to switch a tool off, which is the trade-off your temp-AI question implies.
>
> Every figure carries its vendor URL and check date. Use the dataset free for the SaaSpocalypse or temporary-AI piece, with or without attribution. If you need a CIO voice rather than a price census, I'm the wrong source and I'll say so.
>
> AIToolsEssentials

*Word count: 177 words including the signature — measured on this file; subject line excluded.*

**Stageable:** yes — `scripts/stage_pitch_drafts.py` writes this to `[Gmail]/Drafts`; sending is George's.

---

## 2. Forbes — US solopreneurs, and bootstrapped founders who can quantify what AI removed ◀ 18d, EMAIL, LATE

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **18 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-27T12:57:38Z`, badge *"Posted 18 days ago"*, no expiry notice.
**Who:** **Alison Coleman**, Forbes senior contributor covering entrepreneurs and their startups.
**Ask, her words:** *"Looking for US #solopreneurs, genuinely one-person business that have used AI to
eliminate the need to hire, or simply change when and why the first hire happens."*

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** A published email; the send is
George's.
- Re-probed today: https://www.alisoncoleman.co.uk/contact-me/ **HTTP 200, 28,082 bytes**, address
  `alison@alisoncoleman.co.uk` present in the visible body text beside a Contact Form 7 form;
  `forbes.com/sites/alisoncoleman/` remains outside our reach (HTTP 403 in earlier probes — dead
  end, do not retry).
- One send closes both Forbes rows. Deliverability is not SMTP-verified; only a bounce proves anything.

**Subject:** `What the AI stack costs when it stands in for a first hire`

> Hi Alison —
>
> $16.00 is the median cheapest paid seat among the 111 AI tools we track, 45 of which publish a monthly per-seat price (snapshot updated 2026-11-14). Five seats is $80 a month, $960 a year — the number a US solo founder weighs against a first salary, which is the comparison your solopreneurs call asks for.
>
> I can't answer from inside a one-person business, so I won't pretend to. What I do is a dated price census: every tier read off the vendor's own pricing page, check date attached. Across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16), so the annual figure is the honest one to quote.
>
> Your bootstrapped-founders call, posted seven minutes earlier, is the same arithmetic on the capital side, so one dataset answers both. I saw the UK compute call you posted since; I have nothing on data centres, so this stays on the two US ones.
>
> Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 169 words including the signature — measured on this file; subject line excluded.*

**Stageable:** yes — re-staged in `[Gmail]/Drafts` from this file today; the 110-tool copy from
2026-11-13 (uid 65) is deleted so only one version exists.

---

## 3. Business Today — workplace AI adoption and the skills to use the tools ◀ 17d, LINKEDIN DM, LATE

**Source:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
**Posted:** 2026-10-28 11:24 UTC — **17 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-28T11:24:30Z`, badge *"Posted 17 days ago"*, no expiry notice.
**Who:** **Vidhya Das**, Business Today (India Today group); author page
`businesstoday.in/author/vidhya-das`.
**Ask, her words:** *"how employees are adapting to the growing use of artificial intelligence (AI) in
the workplace, and what it takes to use these tools effectively"* — she wants *"independent AI experts,
enterprise AI trainers, researchers and technology professionals"*.

**Reply route:** **LinkedIn DM to linkedin.com/in/vidya-das** — **automatable? No.**
- The body redacts her email and offers *"comment below or DM me on LinkedIn"*. The handle was
  search-resolved 2026-10-29 and re-confirmed at snippet level 2026-11-12 (profile title *"Trainee Sub
  Editor | Business Today | India Today group"*); a direct fetch still returns HTTP 999 (LinkedIn
  blocks this probe), so the DM is the one route no script can stage or check. Confirm the profile
  matches her masthead before sending.
- No deadline stated on the page. The 10-day figure is this monitor's own line.

**First line does the work (a DM has no subject):**

> Hi Vidhya — $16.00 is the median cheapest paid seat among the 111 AI tools we track, 45 of which publish a monthly price (snapshot updated 2026-11-14). Five seats is about $960 a year. That number sits underneath your adoption story: the spend is small enough that an employee can adopt a tool without asking anyone, so training lags adoption rather than causing it.
>
> I'm not a trainer, so I'm not pitching that angle. I run a dated price census — every tier read off the vendor's own pricing page, each with its check date — and I can give you the seat and billing numbers behind the skills question. Across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16).
>
> Every figure carries its vendor URL and check date. Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 144 words including the signature — measured on this file.*

**Cannot be staged:** a LinkedIn DM has no mailbox artefact. Paste it yourself.

---

## Why there is no fourth draft

The 5 rows added today were read and excluded, not silently dropped: Microsoft 365 users on yesterday's
outage (testimony, and the AI token is the product name, not an ask), people wrongly accused of using
AI (testimony, no route), a ServiceNow vendor podcast guest call, an Israeli developer whose job AI
changed (testimony with a geographic and occupational screen), and someone running 10%+ of production
inference on local models inside a seven-figure business — the closest row to our beat, but the only
honest answer is that we price vendor list tiers and have never operated a local inference deployment.
Full read on each in `digest-2026-11-14.json`.

## Still open past the line — send late or record skipped

- **WSJ / Christopher Mims** — `employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`,
  **40 days**, page live (HTTP 200 today). Route `linkedin.com/in/christopher-mims-club/` (HTTP 200,
  618,897 bytes today). Draft in `pitch-drafts-2026-10-27.md` §3.
- **Tobi Amure** — `tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring`, **35 days**, page live.
  Route `hello@tobiamure.com` (contact form as fallback; tobiamure.com HTTP 200, 63,314 bytes today).
  Draft in `pitch-drafts-2026-10-28.md` §3.
- **Anthropic / customer service** — `anthropic-users-and-business-owners-customer-service-experiences`,
  **64 days**, page live. Route Signal `hliwrites.99`. Draft in `pitch-drafts-2026-09-22.md` §2.
- **FinOps / Niloy Ghosh** — `finops-professionals-agentic-ai-cost-overruns`, **68 days**, page live,
  the longest-standing high-relevance request this monitor has never answered. Route: LinkedIn DM to
  `linkedin.com/in/niloy-ghosh`. Draft in `pitch-drafts-2026-09-17.md` §1. Do not draft it a fifth time.
- **Business Insider / Thibault Spirlet** — `employees-at-european-orgs-switch-from-us-ai-provider-to-mistral`,
  now **404: deleted from the platform**. It crossed the 10-day line on 2026-11-03 with a finished
  draft behind it, and no send is possible any more. Recorded `skipped` in `pitch-ledger.json` today
  with that reason, so the queue stops carrying it as a late send.
