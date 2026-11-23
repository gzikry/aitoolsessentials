# Pitch drafts — 2026-11-23

**One sendable row, one late send, one cold cleanup. Zero sent since 2026-10-10. Each needs George's click.**

365 carried requests + 2 new = 367 tracked, **69 live unpitched, 1 sendable** (`pitch-queue.md`, rebuilt this run
from page truth: 373 URLs probed, 327 serving, 46 gone on the platform; 44 carried rows dead and unchanged since
2026-11-05), **0 newly expired**, 15 rows crossed the 10-day line overnight. §1 is Business Insider / Thibault
Spirlet at **7 days** — the only sendable row in the queue and the freshest on-beat row alive. §2 is
InformationWeek / Kelsey Ziser at **13 days**, a late send that is still live and routable. §3 is the Forbes
cleanup that closes two rows at **27 days** each with one email.

**Figures today:** `data/tools.json` holds **133 tools**; `data/pricing_snapshots.json` (`updated: 2026-11-23`)
yields **52 with a published monthly per-seat price, 42 at or under $25/month, median $15.50**. Monthly vs annual:
**1.11x to 2.53x, median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, built 2026-10-16). Prices quoted
below carry the per-tool check date from `data/tool_sources.json`; every route below was re-probed today
(`route-checks-2026-11-23.json`).

---

## 1. Business Insider — US-to-Mistral switchers and the seat arithmetic ◀ 7d, EMAIL, SEND FIRST

**Source:** https://www.sourcee.app/journo-request/former-software-engineers-left-tech-after-ai-coding-tools
**Posted:** 2026-11-16 12:19 UTC — **7 days.** Page read today: HTTP 200, body served, badge *"Posted in last
7 days"*, no expiry notice. Absent from the 50-slot AI topic feed all week — found through the sitemap window,
so feed absence here means "not a topic-page listing", not "dropped".
**Who:** **Thibault Spirlet**, Business Insider (JSON-LD author field).
**Ask, his words:** *"Employees, customers, and investors who have switched from US AI firms to Mistral, or are
seriously considering doing so."* The other three parts are first-hand engineer testimony we cannot give.

**Reply route:** **tspirlet@businessinsider.com** — **automatable? No.** Published in a `mailto:` link on
`businessinsider.com/author/thibault-spirlet` (re-probed today: HTTP 200, 321,331 bytes, address present 5 times in
the markup). The request page redacts the address. The send is George's.

**Subject:** `The per-seat arithmetic in your Mistral switchers call`

> Hi Thibault —
>
> You're looking for people who moved from a US provider to Mistral. I'm not one, so I won't answer as one. What I can give you is the seat arithmetic behind that decision.
>
> Mistral Vibe (Le Chat) Pro is $14.99/month and Team is $24.99 per user per month. Against that: ChatGPT Plus is $20/month, and Claude Pro is $20 month-to-month or $17 on a $200 annual prepay — all three read off the vendors' own pricing pages, checked 2026-11-14.
>
> At the individual tier that is a 25% cut. At team level it depends which US plan the buyer left; OpenAI's Business tier is sales-assisted, so no published per-seat price exists to compare against.
>
> The other half is billing term: across the 19 same-tier pairs in our census, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (pair set re-asserted 2026-10-16). That premium is often what a switcher is reacting to, not the sticker.
>
> We track 133 AI tools, each tier read off the vendor's own pricing page with its check date, so every number above is citable. Free to use, with or without attribution.
>
> AIToolsEssentials

**Stageable:** yes — `scripts/stage_pitch_drafts.py`; sending is George's.

---

## 2. InformationWeek — CIOs on the SaaSpocalypse and temporary AI ◀ 13d, EMAIL, LATE SEND

**Source:** https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai
**Posted:** 2026-11-09 20:11 UTC — **13 days.** Page read today: HTTP 200, body served, badge *"Posted 13 days
ago"*, no expiry notice. Past the monitor's 10-day line: late, not dead.
**Who:** **Kelsey Ziser**, Senior Editor, InformationWeek (page author field).
**Ask, her words:** *"thoughts on the SaaSpocalypse? - are there any use cases where you deploy a temporary
AI tool?"*

**Reply route:** **kelsey.ziser@informationweek.com** — **automatable? No.** Published in a `mailto:` link on her
author page `informationweek.com/author/kelsey-ziser` (re-probed today: HTTP 200, 584,932 bytes, address in the
`mailto:`). The request page publishes no address. The send is George's.

**Subject:** `The seat-price numbers behind the SaaSpocalypse question`

> Hi Kelsey —
>
> You asked CIOs about the SaaSpocalypse and temporary AI deployments. I'm not a CIO, so I won't answer as one. What I can give you is the seat-price floor beneath that question.
>
> Of the 133 AI tools we track, 52 publish a monthly per-seat price; 42 of those sit at or under $25, and the median cheapest paid seat is $15.50 (snapshot 2026-11-23, every tier read off the vendor's own pricing page with its check date). The cheapest paid seat we record is $4 (Khanmigo's learner plan, checked 2026-09-18) and the dearest $299 (Instrumentl, checked 2026-09-18), so "AI" is not one price point to a CFO.
>
> The billing split speaks directly to a temporary deployment: across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (pair set re-asserted 2026-10-16). That premium is exactly what a buyer pays for the right to switch a tool off.
>
> Every figure carries its vendor URL and check date. Free to use, with or without attribution. If you need a CIO voice rather than a price census, I'm the wrong source and I'll say so.
>
> AIToolsEssentials

**Stageable:** yes; sending is George's.

---

## 3. Forbes — Alison Coleman's two founder calls, one email ◀ 27d each, EMAIL, LATE SEND (cold)

**Sources (one email closes both):**
https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact
**Posted:** 2026-10-27 12:57 and 12:50 UTC — **27 days each.** Both pages read today: HTTP 200, badge *"Posted 27
days ago"*, no expiry notice. Cold by age; send late or record skipped in `pitch-ledger.json` and stop carrying it.
**Who:** **Alison Coleman**, Forbes senior contributor.

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** Published in visible body text on
`alisoncoleman.co.uk/contact-me/` (re-probed today: HTTP 200, 28,116 bytes). `forbes.com/sites/alisoncoleman/`
answers 403 to this monitor and is a dead end, not a route.

**Subject:** `One price dataset behind both of your founder calls`

> Hi Alison —
>
> You posted two founder calls on 27 October — solopreneurs whose first hire was delayed or eliminated by AI, and founders who bootstrapped rather than raise. I can't give you a first-hand founder story; I can give you the numbers those decisions sit on.
>
> Of the 133 AI tools we track, 52 publish a monthly per-seat price; 42 of those are at or under $25, and the median cheapest paid seat is $15.50 — $186 a year (snapshot 2026-11-23, each tier read off the vendor's own pricing page with its check date). The cheapest paid seat we record is $4, Khanmigo's learner plan, checked 2026-09-18.
>
> A stack of four paid tools at that median is $744 a year. That is the arithmetic behind "we didn't make the hire yet": the routine work a first hire used to absorb now has a published price, and it is small.
>
> If either piece needs a figure checked against a vendor page, send it and I'll confirm or correct it the same day.
>
> AIToolsEssentials

**Stageable:** yes, but it is cold — George's call whether to send or skip.

---

## What is not in this file, and why

The 2026-11-23 sitemap window carried 25 slugs, 2 with an AI token and 0 with an AI+spend token; all 25 window
bodies were fetched (25/25 HTTP 200) and read. Both AI rows ask for testimony or peer review, not pricing data,
and neither publishes a route: High Point Editorial Services wants cybersecurity experts to review its own
AI-weaponization desk, and LiveMint wants first-hand testimony on everyday AI use in complex Indian languages.
Both are recorded in the digest, neither is drafted. No figure is typed here that is not in `data/` with its
check date.