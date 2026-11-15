# Pitch drafts — 2026-11-15

**Three drafts, three sends, all George's lane. Nothing below has been sent.**

309 tracked requests, **52 live unpitched, 1 sendable** (`pitch-queue.md`, built today), 44 dead on
the platform, **0 newly expired**. The one sendable row is **InformationWeek / Kelsey Ziser, 5 days
old** — the only request inside the 10-day line with both an on-beat angle and a resolved direct
address. The other two are live and late (19 and 18 days) against this monitor's own cold line, not
against any deadline either reporter stated.

**Send in this order: §1 (5d, email), then §2 (one email closes two Forbes rows), then §3 (a LinkedIn
DM, which cannot be staged).**

**The figures moved since yesterday's drafts, so yesterday's copies are now wrong.** `data/tools.json`
holds **113 tools** (was 111); `data/pricing_snapshots.json` (`updated: 2026-11-15`) yields **50 with
a published monthly per-seat price, 41 of those at or under $25/month, median $15.50** (yesterday:
45 / 36 / $16.00). Gmail drafts 66 and 67 still carry the 111-tool, $16.00 figures and should be
deleted once these are staged. Monthly vs annual is unchanged: **1.11x to 2.53x, median 1.25x over 19
tiers** (`data/monthly_annual_pairs.json`, re-asserted 2026-10-16).

**Today's 24-slug window produced nothing.** 0 AI-token slugs, 0 AI+spend, 1 spend-only, 1 body-level
AI mention across all 24 bodies read — a Poetry Wales submissions call that mentions data-centre
electricity in passing. Full accounting in `digest-2026-11-15.json`.

---

## 1. InformationWeek — CIOs on the SaaSpocalypse and temporary AI ◀ 5d, EMAIL, FRESH, SEND FIRST

**Source:** https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai
**Posted:** 2026-11-09 20:11 UTC — **5 days.** Page read today: HTTP 200, body served,
`datePublished 2026-11-09T20:11:11.759Z`, badge *"Posted in last 7 days"*, no expiry notice.
**Who:** **Kelsey Ziser**, Senior Editor, InformationWeek. The page's author field names her; her
author page is `informationweek.com/author/kelsey-ziser` (HTTP 200, 582,084 bytes, probed 2026-11-14).
**Ask, her words:** *"looking for CIOs to discuss... thoughts on the SaaSpocalypse? - are there any
use cases where you deploy a temporary AI tool?"* — five topics, two of them pricing questions.

**Reply route:** **kelsey.ziser@informationweek.com** — **automatable? No.** Published as a
`mailto:` link on her InformationWeek author page; the request page itself publishes no address.
The send is George's.

**Subject:** `The seat-price numbers behind the SaaSpocalypse question`

> Hi Kelsey —
>
> You asked CIOs about the SaaSpocalypse and temporary AI deployments. I'm not a CIO, so I won't answer as one. What I can give you is the seat-price floor beneath that question.
>
> Of the 113 AI tools we track, 50 publish a monthly per-seat price; 41 of those sit at or under $25, and the median cheapest paid seat is $15.50 (snapshot updated 2026-11-15, every tier read off the vendor's own pricing page with its check date).
>
> The billing split is the part that speaks to a temporary deployment: across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (pair set re-asserted 2026-10-16). That premium is what a buyer pays for the right to switch a tool off, which is the trade-off your temp-AI question implies.
>
> Every figure carries its vendor URL and check date. Use the dataset free for the SaaSpocalypse or temporary-AI piece, with or without attribution. If you need a CIO voice rather than a price census, I'm the wrong source and I'll say so.
>
> AIToolsEssentials

*Word count: 177 words including the signature — counted on this file; subject line excluded.*

**Stageable:** yes — `scripts/stage_pitch_drafts.py` writes it to `[Gmail]/Drafts`; sending is George's.

---

## 2. Forbes — US solopreneurs, and bootstrapped founders who can quantify what AI removed ◀ 19d, EMAIL, LATE

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **19 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-27T12:57:38Z`, badge *"Posted 19 days ago"*, no expiry notice.
**Who:** **Alison Coleman**, Forbes senior contributor covering entrepreneurs and their startups.
**Ask, her words:** *"Looking for US #solopreneurs, genuinely one-person business that have used AI to
eliminate the need to hire, or simply change when and why the first hire happens."*

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** A published email; the send is
George's. Re-probed 2026-11-14: `alisoncoleman.co.uk/contact-me/` HTTP 200, 28,082 bytes, the address
printed in visible body text beside a Contact Form 7 form. `forbes.com/sites/alisoncoleman/` returns
403 to us — dead end, do not retry. One send closes both Forbes rows.

**Subject:** `What the AI stack costs when it stands in for a first hire`

> Hi Alison —
>
> $15.50 is the median cheapest paid seat among the 113 AI tools we track, 50 of which publish a monthly per-seat price (snapshot updated 2026-11-15). Five seats is $77.50 a month, $930 a year — the number a US solo founder weighs against a first salary, which is the comparison your solopreneurs call asks for.
>
> I can't answer from inside a one-person business, so I won't pretend to. What I do is a dated price census: every tier read off the vendor's own pricing page, check date attached. Across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16), so the annual figure is the honest one to quote.
>
> Your bootstrapped-founders call, posted seven minutes earlier, is the same arithmetic on the capital side, so one dataset answers both.
>
> Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 146 words including the signature — counted on this file; subject line excluded.*

**Stageable:** yes — stage from this file, then delete Gmail draft uid 67 (it carries the superseded
111-tool, $16.00 figures).

---

## 3. Business Today — workplace AI adoption and the skills to use the tools ◀ 18d, LINKEDIN DM, LATE

**Source:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
**Posted:** 2026-10-28 11:24 UTC — **18 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-28T11:24:30Z`, badge *"Posted 18 days ago"*, no expiry notice.
**Who:** **Vidhya Das**, Business Today (India Today group); author page
`businesstoday.in/author/vidhya-das` (HTTP 200, title *"Trainee Sub Editor"*).
**Ask, her words:** *"how employees are adapting to the growing use of artificial intelligence (AI) in
the workplace, and what it takes to use these tools effectively"* — she wants *"independent AI experts,
enterprise AI trainers, researchers and technology professionals"*.

**Reply route:** **LinkedIn DM to linkedin.com/in/vidya-das** — **automatable? No.**
The body redacts her email and offers *"comment below or DM me on LinkedIn"*. The handle was
confirmed 2026-11-12 at snippet level (profile title *"Trainee Sub Editor | Business Today | India
Today group"*); a direct fetch still returns HTTP 999, so the DM is the one route no script can stage
or check. Confirm the profile matches her masthead before sending.

**First line does the work (a DM has no subject):**

> Hi Vidhya — $15.50 is the median cheapest paid seat among the 113 AI tools we track, 50 of which publish a monthly price (snapshot updated 2026-11-15). Five seats is about $930 a year. That number sits underneath your adoption story: the spend is small enough that an employee can adopt a tool without asking anyone, so training lags adoption rather than causing it.
>
> I'm not a trainer, so I'm not pitching that angle. I run a dated price census — every tier read off the vendor's own pricing page, each with its check date — and I can give you the seat and billing numbers behind the skills question. Across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16).
>
> Every figure carries its vendor URL and check date. Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 143 words including the signature — counted on this file.*

**Cannot be staged:** a LinkedIn DM has no mailbox artefact. Paste it yourself.

---

## Why there is only one new row today, and no fourth draft

The 24-slug window produced one body-level AI mention: a Poetry Wales / MODRON call for women writers
from the Global South, where AI appears once as a data-centre electricity aside inside a climate-justice
pitch call. It carries no pricing, seat or procurement question, publishes no address of its own, and the
outlet states it cannot pay contributors. Recorded as `low` and excluded, not silently dropped. Full read
in `digest-2026-11-15.json`.

## Still open past the line — send late or record skipped

- **WSJ / Christopher Mims** — 41 days, page live, route `linkedin.com/in/christopher-mims-club/`.
  Draft in `pitch-drafts-2026-10-27.md` §3.
- **Tobi Amure** — 36 days, page live, route `hello@tobiamure.com`. Draft in `pitch-drafts-2026-10-28.md` §3.
- **Anthropic / customer service** — 65 days, page live, route Signal `hliwrites.99`. Draft in `pitch-drafts-2026-09-22.md` §2.
- **FinOps / Niloy Ghosh** — 69 days, page live, route `linkedin.com/in/niloy-ghosh`. Draft in
  `pitch-drafts-2026-09-17.md` §1. Do not draft it a fifth time.
