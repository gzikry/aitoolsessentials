# Pitch drafts — 2026-11-20

**Two live pitches + one late send. Zero sent yet. Each one needs George's click or paste.**

359 tracked requests, **93 live unpitched, 2 sendable** (`pitch-queue.md`, rebuilt this run), 42 dead on
the platform, **0 newly expired**, **0 crossed cold** since yesterday. §1 is Business Insider / Thibault
Spirlet at **4 days** — the freshest on-beat row in the queue. §2 is InformationWeek / Kelsey Ziser, whose
page badge reads **"Posted 10 days ago"**: it sits ON the 10-day line today and crosses cold at 11 days,
so **today is its last sendable day**. §3 is the Forbes late send that closes two already-cold rows with
one email.

**Figures today:** `data/tools.json` holds **127 tools**; `data/pricing_snapshots.json`
(`updated: 2026-11-20`) yields **51 with a published monthly per-seat price, 42 at or under $25/month,
median $15.00**. Monthly vs annual is unchanged: **1.11x to 2.53x, median 1.25x over 19 tiers**
(`data/monthly_annual_pairs.json`, re-asserted 2026-10-16). Every route below was re-probed today
(`route-checks-2026-11-20.json`).

---

## 1. Business Insider — US-to-Mistral switchers and the seat arithmetic ◀ 4d, EMAIL, SEND FIRST

**Source:** https://www.sourcee.app/journo-request/former-software-engineers-left-tech-after-ai-coding-tools
**Posted:** 2026-11-16 12:19 UTC — **4 days.** Page read today: HTTP 200, body served,
`datePublished 2026-11-16T12:19:09.818+00:00`, badge *"Posted in last 7 days"*, no expiry notice.
**Who:** **Thibault Spirlet**, Business Insider — the page's JSON-LD author field names him.
**Ask, his words:** *"Employees, customers, and investors who have switched from US AI firms to Mistral,
or are seriously considering doing so."* (Three of his four asks are first-hand testimony we cannot give;
this one is a pricing question we can.)

**Reply route:** **tspirlet@businessinsider.com** — **automatable? No.** Published as a `mailto:` link on
his byline page `businessinsider.com/author/thibault-spirlet` (re-probed today: `route-checks-2026-11-20.json`,
HTTP 200, 323,884 bytes, address present in the markup). The request page redacts the address. The send is George's.

**Subject:** `The per-seat arithmetic in your Mistral switchers call`

> Hi Thibault —
>
> You're looking for people who moved from a US provider to Mistral. I'm not one, so I won't answer as one. What I can give you is the seat arithmetic behind that decision: Mistral Vibe (Le Chat) Pro is $14.99/month and Team is $24.99 per user per month, against ChatGPT Plus at $20/month and Claude Pro at $20 month-to-month or $17 on a $200 annual prepay — all four read off the vendors' own pricing pages, snapshot dated 2026-11-14.
>
> At the individual tier the switch is a 25% cut. At team level it depends which US plan the buyer came from; OpenAI's Business tier is sales-assisted, so no published seat price exists to compare against.
>
> The other half is billing term: across 19 same-tier pairs in our census, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (pairs re-asserted 2026-10-16). That premium is usually what a switcher is reacting to, not the sticker.
>
> I keep a dated census of the 127 AI tools we track, each tier read off the vendor's own pricing page with its check date, so every number above is citable. Free to use, with or without attribution.
>
> AIToolsEssentials

**Stageable:** yes — `scripts/stage_pitch_drafts.py`; sending is George's.

---

## 2. InformationWeek — CIOs on the SaaSpocalypse and temporary AI ◀ 10d, EMAIL, LAST SENDABLE DAY

**Source:** https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai
**Posted:** 2026-11-09 20:11 UTC — **10 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-11-09T20:11:11.759Z`, badge *"Posted 10 days ago"*, no expiry notice. At 11 days it
leaves the sendable count — tomorrow this row is cold.
**Who:** **Kelsey Ziser**, Senior Editor, InformationWeek (named in the page's author field).
**Ask, her words:** *"thoughts on the SaaSpocalypse? - are there any use cases where you deploy a
temporary AI tool?"*

**Reply route:** **kelsey.ziser@informationweek.com** — **automatable? No.** Published in a `mailto:` link
on her author page `informationweek.com/author/kelsey-ziser` (re-probed today: `route-checks-2026-11-20.json`,
HTTP 200, 583,970 bytes, address present in the `mailto:` link). The request page publishes no address.
The send is George's. **This is the row that leaves the queue first** — not by a stated deadline, but by
the queue's own 10-day line: it sits on the line today and crosses tomorrow.

**Subject:** `The seat-price numbers behind the SaaSpocalypse question`

> Hi Kelsey —
>
> You asked CIOs about the SaaSpocalypse and temporary AI deployments. I'm not a CIO, so I won't answer as one. What I can give you is the seat-price floor beneath that question.
>
> Of the 127 AI tools we track, 51 publish a monthly per-seat price; 42 of those sit at or under $25, and the median cheapest paid seat is $15.00 (snapshot 2026-11-20, every tier read off the vendor's own pricing page with its check date). The cheapest paid seat we record is $4 (Khanmigo's learner plan, checked 2026-09-18) and the dearest $299 (Instrumentl, checked 2026-09-18), so "AI" is not one price point to a CFO.
>
> The billing split is the part that speaks to a temporary deployment: across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (pair set re-asserted 2026-10-16). That premium is exactly what a buyer pays for the right to switch a tool off.
>
> Every figure carries its vendor URL and check date. Free to use for the SaaSpocalypse or temporary-AI piece, with or without attribution. If you need a CIO voice rather than a price census, I'm the wrong source and I'll say so.
>
> AIToolsEssentials

**Stageable:** yes — same staging path; sending is George's.

---

## 3. Forbes — Alison Coleman's two founder calls, one email ◀ 24d, EMAIL, LATE SEND (past the line)

**Sources (one email closes both):**
https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact
**Posted:** 2026-10-27 12:57 and 12:50 UTC — **24 days each.** Both pages read today: HTTP 200,
badge *"Posted 24 days ago"*, no expiry notice. Live, but well past the queue's cold line: send it
knowing it is late, or record it skipped and stop carrying it.
**Who:** **Alison Coleman**, Forbes senior contributor.

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** Published in visible body text on
`alisoncoleman.co.uk/contact-me/` (re-probed today: `route-checks-2026-11-20.json`, HTTP 200, 28,113 bytes).
`forbes.com/sites/alisoncoleman/` answers 403 to this monitor and is a dead end, not a route. The send is George's.

**Subject:** `One price dataset behind both of your founder calls`

> Hi Alison —
>
> You posted two founder calls on 27 October — solopreneurs whose first hire was delayed or eliminated by AI, and founders who bootstrapped rather than raise. I can't give you a first-hand founder story. I can give you the numbers those decisions sit on.
>
> Of the 127 AI tools we track, 51 publish a monthly per-seat price; 42 of those are at or under $25, and the median cheapest paid seat is $15.00 — $180 a year (snapshot 2026-11-20, each tier read off the vendor's own pricing page with its check date). The cheapest paid seat we record is $4, for Khanmigo's learner plan, checked 2026-09-18.
>
> A stack of four paid tools at that median is $720 a year. That is the arithmetic behind "we didn't make the hire yet": the routine work a first hire used to absorb now has a published price, and it is small.
>
> If either piece needs a figure checked against a vendor page, send it and I'll confirm or correct it the same day.
>
> AIToolsEssentials

**Stageable:** yes; sending is George's.

---

## What is not in this file, and why

The 2026-11-20 window carried 7 AI-token slugs and 0 AI+spend slugs at slug level; all 92 window bodies
were fetched and read, lifting the candidate set to 11. Every one of the 11 asks for first-hand testimony,
standing or a named guest, or is a referral, and every one publishes no route of its own — they are added
to tracking and assessed in the digest, not drafted. The window's spend-token hits are salary (payroll/HRIS
pay gap) and procurement (sports-retail supply chain), neither of which a seat-price census can answer. No
new draft is written from this window; the sendable set is carried, and the work that matters is sending it.

Every route above answered HTTP 200 today (`route-checks-2026-11-20.json`). Nothing in this file has been
sent, and nothing will be sent by the monitor: each route is a journalist's mailbox, which is George's lane.
