# Pitch drafts — 2026-11-24

**Two sendable rows, both emails, both George's click. Zero sent since 2026-10-10.**

382 tracked requests (367 carried + 15 new this run), **74 live unpitched, 2 sendable** (`pitch-queue.md`,
rebuilt this run from page truth: 375 URLs probed, all carried rows re-fetched today; 44 carried rows dead and
unchanged since 2026-11-05), **0 newly expired**, 10 rows crossed the 10-day line overnight. §1 is Personnel
Today / Jo Faragher at **1 day** — a direct *AI-token-cost-vs-employment-cost* question, the freshest on-beat
row alive and route-resolved off the publication's own contact page. §2 is Business Insider / Thibault Spirlet
at **8 days**, still inside the line and routable.

**Figures today:** `data/tools.json` holds **134 tools**; `data/pricing_snapshots.json` (`updated: 2026-11-24`)
yields **52 with a published monthly per-seat price, 42 at or under $25/month, median $15.50**. Monthly vs annual:
**1.11x to 2.53x, median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, built 2026-10-16). Every price
below carries the per-tool check date from `data/tool_sources.json`; both routes were re-probed today
(`route-checks-2026-11-24.json`).

---

## 1. Personnel Today — the cost of AI seats vs the cost of a hire ◀ 1d, EMAIL, SEND FIRST

**Source:** https://www.sourcee.app/journo-request/hr-professionals-ai-hiring-economics-and-workforce-planning
**Posted:** 2026-11-23 10:49 UTC — **1 day.** Page read today: HTTP 200, body served, badge *"Posted in last
7 days"*. Absent from the 50-slot AI topic feed — found through the sitemap window, so feed absence here means
"not a topic-page listing", not "dropped".
**Who:** **Jo Faragher**, contributing editor, Personnel Today (JSON-LD author field; also named on the
publication's own contact page).
**Ask, her words:** *"With news that some companies are capping the use of tokens, how do companies calculate the
cost of AI against the cost of employing people, and what does this mean for the future structure of the
workforce?"* She wants HR practitioners **or** an AI expert on the trends — the second invitation is ours.

**Reply route:** **jo.faragher@personneltoday.com** — **automatable? No.** Published in the editorial contact
listing on `personneltoday.com/contact-us/` (re-probed today: HTTP 200, 243,494 bytes, *"Jo Faragher, contributing
editor"*). The request page publishes no address. `personneltoday.com` MX = Google Workspace. The send is George's.

**Subject:** `The per-seat numbers behind "AI cost vs hire cost"`

> Hi Jo —
>
> You asked how companies price AI seats against the cost of people, and mentioned token caps. I run a dated price census of AI tools, so I can give you the seat half of that arithmetic.
>
> Of the 134 AI tools we track, 52 publish a monthly per-seat price; 42 of those sit at or under $25, and the median cheapest paid seat is $15.50/month — about $186 a year (snapshot 2026-11-24, each tier read off the vendor's own pricing page with its check date). Ten seats at that median is $1,860/year, which is where the "cheaper than a hire" claim comes from and also its ceiling.
>
> The token caps are visible in the same data: Bolt's free tier meters to a 300,000-token daily limit (2026-10-25); GitHub Copilot Pro is $10/month for 1,500 monthly AI credits, Pro+ $39 for 7,000 (2026-11-14); Leonardo's $12 tier caps at 8,500 fast tokens/month (2026-08-25). Copilot Business lists at $18/user/month promotional versus $21 list (2026-11-14).
>
> Every figure carries its vendor URL and check date. Free to use, with or without attribution.
>
> AIToolsEssentials

**Stageable:** yes — `scripts/stage_pitch_drafts.py`; sending is George's.

---

## 2. Business Insider — US-to-Mistral switchers and the seat arithmetic ◀ 8d, EMAIL, SEND

**Source:** https://www.sourcee.app/journo-request/former-software-engineers-left-tech-after-ai-coding-tools
**Posted:** 2026-11-16 12:19 UTC — **8 days.** Page read today: HTTP 200, body served, badge *"Posted in last
7 days"*, no expiry notice. Still inside the 10-day line.
**Who:** **Thibault Spirlet**, Business Insider (JSON-LD author field).
**Ask, his words:** *"Employees, customers, and investors who have switched from US AI firms to Mistral, or are
seriously considering doing so."* The other three parts are first-hand engineer testimony we cannot give.

**Reply route:** **tspirlet@businessinsider.com** — **automatable? No.** Published in a `mailto:` link on
`businessinsider.com/author/thibault-spirlet` (re-probed today: HTTP 200, 328,089 bytes, address present 5 times
in the markup). The request page redacts the address. The send is George's.

**Subject:** `The per-seat arithmetic in your Mistral switchers call`

> Hi Thibault —
>
> You're looking for people who moved from a US provider to Mistral. I'm not one, so I won't answer as one. What I can give you is the seat arithmetic behind that decision.
>
> Mistral Vibe (Le Chat) Pro is $14.99/month and Team is $24.99 per user per month. Against that: ChatGPT Plus is $20/month, and Claude Pro is $20 month-to-month or $17 on a $200 annual prepay — all read off the vendors' own pricing pages, checked 2026-11-14.
>
> At the individual tier that is roughly a 25% cut. At team level it depends which US plan the buyer left; OpenAI's Business tier is sales-assisted, so no published per-seat price exists to compare against.
>
> The other half is billing term: across the 19 same-tier pairs in our census, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (pair set re-asserted 2026-10-16). That premium is often what a switcher is reacting to, not the sticker.
>
> We track 134 AI tools, each tier read off the vendor's own pricing page with its check date, so every number above is citable. Free to use, with or without attribution.
>
> AIToolsEssentials

**Stageable:** yes — `scripts/stage_pitch_drafts.py`; sending is George's.

---

## What is not in this file, and why

The 2026-11-24 sitemap window carried 87 slugs, 12 with an AI slug token and 0 with an AI+spend token; all 87
window bodies were fetched and read, and the body scan found 14 AI-token bodies of which 2 also carry a real
spend token. One is drafted (§1). The other thirteen AI rows ask for reactive testimony or sector expertise, not
pricing data, and none publishes a route: Nvidia/OpenAI leadership reaction (Daniel Howley; Jon Swartz /
TechStrong; Sarah A.; Manseen Logan / Business Insider), insurance-outage testimony (Insurance Business UK),
NHS and healthcare AI (a Pitch & Shout agency application form; Lindsay Dodgson; Dr. Cheryl Robinson),
estate-agent AI listing photos (The i Paper), accountancy-automation consultants (two Caroline Roberts calls
needing ICAEW/consulting standing we do not hold), a classic-car podcast booking, and a careers-newsletter
promo. The second body-level spend hit — Suzanne Bearne's false-AI-use-accusation request — wants
accusation-prevalence research we do not hold and publishes no route. All are recorded in the digest; none is
drafted. No figure is typed here that is not in `data/` with its check date.
