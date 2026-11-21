# Pitch drafts — 2026-11-21

**One live pitch + two late sends. Zero sent yet. Each one needs George's click or paste.**

365 tracked requests, **89 live unpitched, 1 sendable** (`pitch-queue.md`, rebuilt this run), 42 dead on
the platform, **0 newly expired**, **0 crossed cold since the last run except the one named in §3**. §1 is
Business Insider / Thibault Spirlet at **5 days** — the only sendable row in the queue and the freshest
on-beat row alive. §2 is the Forbes late send that closes two already-cold rows with one email. §3 is
InformationWeek / Kelsey Ziser, which **crossed the 10-day line today** (11d) — still live, still
routable, now a late send rather than a candidate.

**Figures today:** `data/tools.json` holds **131 tools**; `data/pricing_snapshots.json`
(`updated: 2026-11-21`) yields **51 with a published monthly per-seat price, 42 at or under $25/month,
median $15.00**. Monthly vs annual is unchanged: **1.11x to 2.53x, median 1.25x over 19 tiers**
(`data/monthly_annual_pairs.json`, re-asserted 2026-10-16). Every route below was re-probed today
(`route-checks-2026-11-21.json`).

---

## 1. Business Insider — US-to-Mistral switchers and the seat arithmetic ◀ 5d, EMAIL, SEND FIRST

**Source:** https://www.sourcee.app/journo-request/former-software-engineers-left-tech-after-ai-coding-tools
**Posted:** 2026-11-16 12:19 UTC — **5 days.** Page read today: HTTP 200, body served,
`datePublished 2026-11-16T12:19:09.818+00:00`, badge *"Posted in last 7 days"*, no expiry notice.
**Who:** **Thibault Spirlet**, Business Insider — the page's JSON-LD author field names him.
**Ask, his words:** *"Employees, customers, and investors who have switched from US AI firms to Mistral,
or are seriously considering doing so."* (Three of his four asks are first-hand testimony we cannot give;
this one is a pricing question we can.)

**Reply route:** **tspirlet@businessinsider.com** — **automatable? No.** Published as a `mailto:` link on
his byline page `businessinsider.com/author/thibault-spirlet` (re-probed today: `route-checks-2026-11-21.json`,
HTTP 200, 321,249 bytes, address present in the markup). The request page redacts the address. The send is George's.

**Subject:** `The per-seat arithmetic in your Mistral switchers call`

> Hi Thibault —
>
> You're looking for people who moved from a US provider to Mistral. I'm not one, so I won't answer as one. What I can give you is the seat arithmetic behind that decision.
>
> Mistral Vibe (Le Chat) Pro is $14.99/month and Team is $24.99 per user per month. Against that: ChatGPT Plus is $20/month, and Claude Pro is $20 month-to-month or $17 on a $200 annual prepay — all three read off the vendors' own pricing pages, snapshot dated 2026-11-14.
>
> At the individual tier that is a 25% cut. At team level it depends which US plan the buyer left; OpenAI's Business tier is sales-assisted, so no published per-seat price exists to compare against.
>
> The other half is billing term: across the 19 same-tier pairs in our census, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (pair set re-asserted 2026-10-16). That premium is often what a switcher is reacting to, not the sticker.
>
> We track 131 AI tools, each tier read off the vendor's own pricing page with its check date, so every number above is citable. Free to use, with or without attribution.
>
> AIToolsEssentials

**Stageable:** yes — `scripts/stage_pitch_drafts.py`; sending is George's.

---

## 2. Forbes — Alison Coleman's two founder calls, one email ◀ 25d, EMAIL, LATE SEND (past the line)

**Sources (one email closes both):**
https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact
**Posted:** 2026-10-27 12:57 and 12:50 UTC — **25 days each.** Both pages read today: HTTP 200,
badge *"Posted 25 days ago"*, no expiry notice. Live, but well past the queue's cold line: send it
knowing it is late, or record it skipped and stop carrying it.
**Who:** **Alison Coleman**, Forbes senior contributor.

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** Published in visible body text on
`alisoncoleman.co.uk/contact-me/` (re-probed today: `route-checks-2026-11-21.json`, HTTP 200, 28,116 bytes).
`forbes.com/sites/alisoncoleman/` answers 403 to this monitor and is a dead end, not a route. The send is George's.

**Subject:** `One price dataset behind both of your founder calls`

> Hi Alison —
>
> You posted two founder calls on 27 October — solopreneurs whose first hire was delayed or eliminated by AI, and founders who bootstrapped rather than raise. I can't give you a first-hand founder story; I can give you the numbers those decisions sit on.
>
> Of the 131 AI tools we track, 51 publish a monthly per-seat price; 42 of those are at or under $25, and the median cheapest paid seat is $15.00 — $180 a year (snapshot 2026-11-21, each tier read off the vendor's own pricing page with its check date). The cheapest paid seat we record is $4, Khanmigo's learner plan, checked 2026-09-18.
>
> A stack of four paid tools at that median is $720 a year. That is the arithmetic behind "we didn't make the hire yet": the routine work a first hire used to absorb now has a published price, and it is small.
>
> If either piece needs a figure checked against a vendor page, send it and I'll confirm or correct it the same day.
>
> AIToolsEssentials

**Stageable:** yes; sending is George's.

---

## 3. InformationWeek — CIOs on the SaaSpocalypse and temporary AI ◀ 11d, EMAIL, LATE SEND (crossed today)

**Source:** https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai
**Posted:** 2026-11-09 20:11 UTC — **11 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-11-09T20:11:11.759Z`, badge *"Posted 11 days ago"*, no expiry notice. It sat ON the
10-day line last run and crossed today, so it is now a late send: live and routable, no longer a candidate.
**Who:** **Kelsey Ziser**, Senior Editor, InformationWeek (named in the page's author field).
**Ask, her words:** *"thoughts on the SaaSpocalypse? - are there any use cases where you deploy a
temporary AI tool?"*

**Reply route:** **kelsey.ziser@informationweek.com** — **automatable? No.** Published in a `mailto:` link
on her author page `informationweek.com/author/kelsey-ziser` (re-probed today: `route-checks-2026-11-21.json`,
HTTP 200, 585,222 bytes, address present in the `mailto:` link). The request page publishes no address.

**Subject:** `The seat-price numbers behind the SaaSpocalypse question`

> Hi Kelsey —
>
> You asked CIOs about the SaaSpocalypse and temporary AI deployments. I'm not a CIO, so I won't answer as one. What I can give you is the seat-price floor beneath that question.
>
> Of the 131 AI tools we track, 51 publish a monthly per-seat price; 42 of those sit at or under $25, and the median cheapest paid seat is $15.00 (snapshot 2026-11-21, every tier read off the vendor's own pricing page with its check date). The cheapest paid seat we record is $4 (Khanmigo's learner plan, checked 2026-09-18) and the dearest $299 (Instrumentl, checked 2026-09-18), so "AI" is not one price point to a CFO.
>
> The billing split speaks directly to a temporary deployment: across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (pair set re-asserted 2026-10-16). That premium is exactly what a buyer pays for the right to switch a tool off.
>
> Every figure carries its vendor URL and check date. Free to use, with or without attribution. If you need a CIO voice rather than a price census, I'm the wrong source and I'll say so.
>
> AIToolsEssentials

**Stageable:** yes; sending is George's.

---

## What is not in this file, and why

The 2026-11-21 window carried 65 slugs, 3 AI-token and 0 AI+spend at slug level; all 65 window bodies
were fetched and read, lifting the candidate set to 6 (3 of them body-level AI hits whose slugs carry no
AI token). Every one asks for first-hand testimony, institutional standing or a named guest, and every
one publishes no route of its own — they are added to tracking and assessed in the digest, not drafted.
The window's 3 spend-token hits are consumer money (flight/hotel price alerts, paid-off debt, paid
content-creator narratives), none an AI tool-price question this census answers. No new draft is written
from this window; the sendable set is carried, and the work that matters is sending it.

Every route above answered HTTP 200 today (`route-checks-2026-11-21.json`). Nothing in this file has been
sent, and nothing will be sent by the monitor: each route is a journalist's mailbox, which is George's lane.
