# Pitch drafts — 2026-11-16

**Three paste-ready pitches. Zero sent. Every one needs George's click or paste.**

315 tracked requests, **58 live unpitched, 1 sendable** (`pitch-queue.md`, built today), 44 dead on the
platform, **0 newly expired**. The sendable row is **InformationWeek / Kelsey Ziser at 6 days** — the
only request inside the 10-day line with both an on-beat angle and a resolved direct address.

**Send in this order: §1 (6d, email) → §2 (one email closes two Forbes rows, 20d) → §3 (LinkedIn DM, 19d).**

**Figures moved again today.** `data/tools.json` now holds **114 tools** (was 113, RapVideoGo added);
`data/pricing_snapshots.json` (`updated: 2026-11-16`) yields **50 with a published monthly per-seat
price, 41 of those at or under $25/month, median $15.50**. Monthly vs annual is unchanged: **1.11x to
2.53x, median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, re-asserted 2026-10-16).
The two Gmail drafts staged yesterday (uids 68, 69) carry the 113-tool figure and were replaced today.

**What changed in the queue:** the InformationWeek row **left the AI-topic feed today** (it was in the
50-slot feed through 2026-11-15). Its page still answers HTTP 200 and still reads *"Posted in last 7
days"*, so it is live — but a row that has stopped being promoted is colder than its age suggests, and
that is the reason to send it today rather than tomorrow.

**Today's window produced nothing draftable.** 30 slugs, 4 AI-token, 0 AI+spend; all 30 bodies read.
One body-level AI+spend hit (Revue des Mines, tokenomics) is the closest thing to our beat in weeks and
still cannot be answered from our data — see the exclusion at the bottom. Digest: `digest-2026-11-16.json`.

---

## 1. InformationWeek — CIOs on the SaaSpocalypse and temporary AI ◀ 6d, EMAIL, SEND FIRST

**Source:** https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai
**Posted:** 2026-11-09 20:11 UTC — **6 days.** Page read today: HTTP 200, body served,
`datePublished 2026-11-09T20:11:11.759Z`, badge *"Posted in last 7 days"*, no expiry notice.
Left the AI-topic feed today; page live and unexpired.
**Who:** **Kelsey Ziser**, Senior Editor, InformationWeek (named in the page's author field).
**Ask, her words:** *"looking for CIOs to discuss... thoughts on the SaaSpocalypse? - are there any
use cases where you deploy a temporary AI tool?"*

**Reply route:** **kelsey.ziser@informationweek.com** — **automatable? No.** Published as a
`mailto:` link on her author page `informationweek.com/author/kelsey-ziser` (re-probed today:
`route-checks-2026-11-16.json`, HTTP 200, 582,686 bytes, address present twice in the markup).
The request page publishes no address. The send is George's.

**Subject:** `The seat-price numbers behind the SaaSpocalypse question`

> Hi Kelsey —
>
> You asked CIOs about the SaaSpocalypse and temporary AI deployments. I'm not a CIO, so I won't answer as one. What I can give you is the seat-price floor beneath that question.
>
> Of the 114 AI tools we track, 50 publish a monthly per-seat price; 41 of those sit at or under $25, and the median cheapest paid seat is $15.50 (snapshot 2026-11-16, every tier read off the vendor's own pricing page with its check date). The cheapest paid seat we record is $4 a month and the dearest $299, so "AI" is not one price point to a CFO.
>
> The billing split is the part that speaks to a temporary deployment: across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (pair set re-asserted 2026-10-16). That premium is what a buyer pays for the right to switch a tool off.
>
> Every figure carries its vendor URL and check date. Free to use for the SaaSpocalypse or temporary-AI piece, with or without attribution. If you need a CIO voice rather than a price census, I'm the wrong source and I'll say so.
>
> AIToolsEssentials

**Stageable:** yes — `scripts/stage_pitch_drafts.py` stages it into `[Gmail]/Drafts`; sending is George's.

---

## 2. Forbes — US solopreneurs, and bootstrapped founders who can quantify what AI removed ◀ 20d, EMAIL, LATE

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **20 days.** Page read today: HTTP 200, `datePublished 2026-10-27T12:57:38Z`, badge *"Posted 20 days ago"*, no expiry notice.
**Who:** **Alison Coleman**, Forbes senior contributor covering entrepreneurs.
**Ask, her words:** *"Looking for US #solopreneurs, genuinely one-person business that have used AI to
eliminate the need to hire, or simply change when and why the first hire happens."*

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** Re-probed today:
`alisoncoleman.co.uk/contact-me/` HTTP 200, 28,116 bytes, address printed in visible body text
(`route-checks-2026-11-16.json`). `forbes.com/sites/alisoncoleman/` returns 403 — dead end, do not
retry. One send closes both Forbes rows.

**Subject:** `What the AI stack costs when it stands in for a first hire`

> Hi Alison —
>
> $15.50 is the median cheapest paid seat among the 114 AI tools we track, 50 of which publish a monthly per-seat price (snapshot 2026-11-16). Five seats is $77.50 a month, $930 a year — the number a US solo founder weighs against a first salary, which is the comparison your solopreneurs call asks for.
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

## 3. Business Today — workplace AI adoption and the skills to use the tools ◀ 19d, LINKEDIN DM, LATE

**Source:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
**Posted:** 2026-10-28 11:24 UTC — **19 days.** Page read today: HTTP 200, `datePublished 2026-10-28T11:24:30Z`, badge *"Posted 19 days ago"*, no expiry notice.
**Who:** **Vidhya Das**, Business Today (India Today group); author page `businesstoday.in/author/vidhya-das` (HTTP 200, title *"Trainee Sub Editor"*).
**Ask, her words:** *"how employees are adapting to the growing use of artificial intelligence (AI) in
the workplace, and what it takes to use these tools effectively"* — she wants *"independent AI experts,
enterprise AI trainers, researchers and technology professionals"*.

**Reply route:** **LinkedIn DM to linkedin.com/in/vidya-das** — **automatable? No.** The body redacts her
email and offers *"comment below or DM me on LinkedIn"*. The handle was confirmed 2026-11-12 at snippet
level; a direct fetch returns HTTP 999. Confirm the profile matches her masthead before sending.

**First line does the work (a DM has no subject):**

> Hi Vidhya — $15.50 is the median cheapest paid seat among the 114 AI tools we track, 50 of which publish a monthly price (snapshot 2026-11-16). Five seats is about $930 a year. That number sits underneath your adoption story: the spend is small enough that an employee can adopt a tool without asking anyone, so training lags adoption rather than causing it.
>
> I'm not a trainer, so I'm not pitching that angle. I run a dated price census — every tier read off the vendor's own pricing page, each with its check date — and I can give you the seat and billing numbers behind the skills question. Across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16).
>
> Every figure carries its vendor URL and check date. Free to use, with or without attribution.
>
> AIToolsEssentials

**Cannot be staged:** a LinkedIn DM has no mailbox artefact. Paste it yourself.

---

## Excluded today, and why

- **Revue des Mines — AI Economist / tokenomics** (1d, `ai-economist-tokenomics-and-market-winners-selfhosting-viability`).
  The window's only body-level AI+spend hit and the nearest to our beat: it asks whether there is an AI
  bubble, whether token prices rise or fall, who wins, and whether companies will self-host. Our census
  measures published **subscription seat prices**, not token or API prices, and holds nothing on
  self-hosting economics — the three questions it poses are exactly the ones we cannot evidence. The ask
  is authorship of a French-language print article, and the address is platform-redacted with no handle
  published. Not drafted: a pitch would have to claim tokenomics standing we do not have.
- The other five window rows (a contact route for one comic writer, a podcast guest call that excludes
  consultants, laid-off-worker testimony, employees of ten named AI firms, an AI-safety interview
  round-up) ask for testimony or standing we do not hold, and four publish no route at all.

## Still open past the line — send late or record skipped

- **WSJ / Christopher Mims** — 42 days, page live, route `linkedin.com/in/christopher-mims-club/`.
  Draft in `pitch-drafts-2026-10-27.md` §3.
- **Tobi Amure** — 37 days, page live, route `hello@tobiamure.com`. Draft in `pitch-drafts-2026-10-28.md` §3.
- **Anthropic / customer service** — 66 days, page live, route Signal `hliwrites.99`. Draft in `pitch-drafts-2026-09-22.md` §2.
- **FinOps / Niloy Ghosh** — 70 days, page live, route `linkedin.com/in/niloy-ghosh`. Draft in
  `pitch-drafts-2026-09-17.md` §1. Do not draft it a fifth time.
