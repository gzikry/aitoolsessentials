# Pitch drafts — 2026-11-18

**Three paste-ready pitches. Zero sent. Each one needs George's click or paste.**

334 tracked requests, **69 live unpitched, 2 sendable** (`pitch-queue.md`, built today), 42 dead on the
platform, **0 newly expired**. §1 is Business Insider / Thibault Spirlet at **2 days** — the freshest
on-beat row in the queue. §2 is InformationWeek / Kelsey Ziser at **8 days**, which crosses the 10-day
line on **2026-11-20**. §3 is the Forbes late send that closes two rows with one email.

**Figures today:** `data/tools.json` holds **117 tools**; `data/pricing_snapshots.json`
(`updated: 2026-11-18`) yields **50 with a published monthly per-seat price, 41 at or under $25/month,
median $15.50**. Monthly vs annual is unchanged: **1.11x to 2.53x, median 1.25x over 19 tiers**
(`data/monthly_annual_pairs.json`, re-asserted 2026-10-16). The tool count moved 115 → 117 since
yesterday, so the three Gmail drafts staged 2026-11-17 (uids 72-74) were deleted and re-staged from this
file rather than left carrying a stale count behind a send button.

---

## 1. Business Insider — US-to-Mistral switchers and the seat arithmetic ◀ 2d, EMAIL, SEND FIRST

**Source:** https://www.sourcee.app/journo-request/former-software-engineers-left-tech-after-ai-coding-tools
**Posted:** 2026-11-16 12:19 UTC — **2 days.** Page read today: HTTP 200, body served,
`datePublished 2026-11-16T12:19:09.818+00:00`, badge *"Posted in last 7 days"*, no expiry notice.
**Who:** **Thibault Spirlet**, Business Insider — the page's JSON-LD author field names him.
**Ask, his words:** *"Employees, customers, and investors who have switched from US AI firms to
Mistral, or are seriously considering doing so."* (Three of his four asks are first-hand testimony we
cannot give; this one is a pricing question we can.)

**Reply route:** **tspirlet@businessinsider.com** — **automatable? No.** Published as a `mailto:` link
on his byline page `businessinsider.com/author/thibault-spirlet` (probed today:
`route-checks-2026-11-18.json`, HTTP 200, 322,839 bytes, address 5 times in the markup). The request
page redacts the address. The send is George's.

**Subject:** `The per-seat arithmetic in your Mistral switchers call`

> Hi Thibault —
>
> You're looking for people who moved from a US provider to Mistral. I'm not one, so I won't answer as one. What I can give you is the seat arithmetic behind that decision: Mistral Vibe (Le Chat) Pro is $14.99/month and Team is $24.99 per user per month, against ChatGPT Plus at $20/month and Claude Pro at $20 month-to-month or $17 on a $200 annual prepay — all four read off the vendors' own pricing pages on 2026-11-14.
>
> At the individual tier the switch is a 25% cut. At team level it depends which US plan the buyer came from, and OpenAI's Business tier is sales-assisted, so there is no published seat price to compare against.
>
> The other half is billing term: across 19 same-tier pairs in our census, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (pairs re-asserted 2026-10-16). That premium is usually what a switcher is reacting to, not the sticker.
>
> I run a dated price census of 117 AI tools — every tier read off the vendor's own pricing page with its check date — so each number above is citable. Free to use, with or without attribution.
>
> AIToolsEssentials

**Stageable:** yes — `scripts/stage_pitch_drafts.py`; sending is George's.

---

## 2. InformationWeek — CIOs on the SaaSpocalypse and temporary AI ◀ 8d, EMAIL, CROSSES COLD 2026-11-20

**Source:** https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai
**Posted:** 2026-11-09 20:11 UTC — **8 days.** Page read today: HTTP 200, body served,
`datePublished 2026-11-09T20:11:11.759Z`, badge *"Posted 8 days ago"*, no expiry notice.
**Who:** **Kelsey Ziser**, Senior Editor, InformationWeek (named in the page's author field).
**Ask, her words:** *"thoughts on the SaaSpocalypse? - are there any use cases where you deploy a
temporary AI tool?"*

**Reply route:** **kelsey.ziser@informationweek.com** — **automatable? No.** Published in a `mailto:`
link on her author page `informationweek.com/author/kelsey-ziser` (re-probed today:
`route-checks-2026-11-18.json`, HTTP 200, 587,341 bytes, address present twice in the markup). The
request page publishes no address. The send is George's.

**Subject:** `The seat-price numbers behind the SaaSpocalypse question`

> Hi Kelsey —
>
> You asked CIOs about the SaaSpocalypse and temporary AI deployments. I'm not a CIO, so I won't answer as one. What I can give you is the seat-price floor beneath that question.
>
> Of the 117 AI tools we track, 50 publish a monthly per-seat price; 41 of those sit at or under $25, and the median cheapest paid seat is $15.50 (snapshot 2026-11-18, every tier read off the vendor's own pricing page with its check date). The cheapest paid seat we record is $4 (Khanmigo's teacher plan, 2026-09-18) and the dearest $299 (Instrumentl, 2026-09-18), so "AI" is not one price point to a CFO.
>
> The billing split is the part that speaks to a temporary deployment: across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (pair set re-asserted 2026-10-16). That premium is exactly what a buyer pays for the right to switch a tool off.
>
> Every figure carries its vendor URL and check date. Free to use for the SaaSpocalypse or temporary-AI piece, with or without attribution. If you need a CIO voice rather than a price census, I'm the wrong source and I'll say so.
>
> AIToolsEssentials

**Stageable:** yes — same staging path; sending is George's.

---

## 3. Forbes — US solopreneurs, and bootstrapped founders who can quantify what AI removed ◀ 22d, EMAIL, LATE

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **22 days.** Page read today: HTTP 200, badge *"Posted 22 days ago"*, no expiry notice.
**Who:** **Alison Coleman**, Forbes senior contributor covering entrepreneurs.
**Ask, her words:** *"Looking for US #solopreneurs, genuinely one-person business that have used AI to
eliminate the need to hire, or simply change when and why the first hire happens."*

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** Re-probed today:
`alisoncoleman.co.uk/contact-me/` HTTP 200, 28,113 bytes, address printed in visible body text
(`route-checks-2026-11-18.json`). `forbes.com/sites/alisoncoleman/` returns 403 — dead end, do not
retry. One send closes both Forbes rows.

**Subject:** `What the AI stack costs when it stands in for a first hire`

> Hi Alison —
>
> $930 a year. That is five seats at $15.50, the median cheapest paid seat across the 117 AI tools we track, 50 of which publish a monthly per-seat price (snapshot 2026-11-18). It is the number a US solo founder weighs against a first salary, which is the comparison your solopreneurs call asks for.
>
> I can't answer from inside a one-person business, so I won't pretend to. What I do is a dated price census: every tier read off the vendor's own pricing page, check date attached. Across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16), so the annual figure is the honest one to quote.
>
> Your bootstrapped-founders call, posted seven minutes earlier, is the same arithmetic on the capital side, so one dataset answers both.
>
> Free to use, with or without attribution.
>
> AIToolsEssentials

**Stageable:** yes — same staging path; sending is George's.

---

## Why these three, and what was excluded

- **§1 is the only on-beat sendable row in the queue and the freshest.** It is the same Business
  Insider reporter whose two September calls we drafted and never sent; that earlier page is now 404,
  so this is a fresh request and a first contact, not a re-send.
- **§2 is 8 days old and crosses the 10-day line on 2026-11-20.** Two more runs and it leaves the
  sendable count for good — the route stays live, but the queue stops ranking it.
- **§3 is a late send at 22 days.** The page is live, the route answers, and one email closes two
  rows. Send it or record it skipped — do not leave it undecided.
- **Today's window produced nothing draftable.** 92 slugs, 5 AI-token, 0 AI+spend; all 92 bodies were
  fetched and read. The two body-only AI hits were the beehiiv State of Newsletter survey (we would be
  overstating our standing as a media brand, and no route) and The Sun's AI listing-photo call
  (consumer testimony, address redacted). The other five ask for bankers, B2B creator agencies, UNESCO
  agent-policy input, Flemish artists or faculty fellows — none is a pricing question and none
  publishes a route to a named person.
