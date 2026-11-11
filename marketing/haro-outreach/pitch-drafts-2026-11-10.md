# Pitch drafts — 2026-11-10

**Three drafts, three sends, all George's lane. Nothing below has been sent.**

267 tracked requests, **41 live unpitched, 1 sendable** (`pitch-queue.md`, built 2026-11-10),
44 expired on the platform. The sendable row is **fresh**: InformationWeek posted 2026-11-09 20:11 UTC.
The other two are carried, still live, and late — 14 and 13 days old against this monitor's own
10-day line, not against any deadline the reporters stated.

**A 116-slug window produced one usable row.** 12 bodies carried an AI token; 2 carried an AI+spend
token and both are false positives on reading (a Microsoft-partner podcast that says "chair", a
UK fashion-scam story about return postage). The InformationWeek call is the only one with a
tool-pricing question in it, and the first in seven windows whose route resolves.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **108 tools**;
`data/pricing_snapshots.json` (`updated: 2026-11-10`) yields **45 with a published monthly
per-seat price, 36 of those at or under $25/month, median $16.00**. Monthly vs annual:
**1.11x to 2.53x, median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, re-asserted
2026-10-16). Superseded, do not reuse: every 105-tool / $16.50 draft written on 2026-11-09 and
every 99-tool / $17.50 draft before 2026-11-03.

**Mailbox: zero replies**, measured today with `jansuski.com` as a positive control that returned
its two known messages (234, 305). No reply to any pitch since 2026-10-11; nothing has been sent
since 2026-10-10.

---

## 1. InformationWeek — CIOs on the SaaSpocalypse and temporary AI ◀ 0d, EMAIL, FRESH, SEND FIRST

**Source:** https://www.sourcee.app/journo-request/cios-2027-goals-ram-shortage-saaspocalypse-temp-ai-physical-ai
**Posted:** 2026-11-09 20:11 UTC — **0 days.** Page read today: HTTP 200, body served,
`datePublished 2026-11-09T20:11:11.759Z`, badge *"Posted in last 7 days"*, no expiry notice.
**Who:** **Kelsey Ziser**, Senior Editor, InformationWeek. The page's author field names her; her
author page is `informationweek.com/author/kelsey-ziser` (HTTP 200, 578,961 bytes).
**Ask, her words:** *"looking for CIOs to discuss... thoughts on the SaaSpocalypse? - are there any
use cases where you deploy a temporary AI tool?"* — five topics, two of them pricing questions.

**Reply route:** **kelsey.ziser@informationweek.com** — **automatable? No.** Published as a `mailto:`
link on her InformationWeek author page; the request page itself publishes no address. Send is George's.
- Route probe today: HTTP 200, 578,961 bytes, title *"Kelsey Ziser | Senior Editor, InformationWeek"*.
- She asks for CIOs. We are a price census, not a CIO, and the draft says so in the first paragraph.
  The offer is the dated seat-price evidence behind the SaaSpocalypse and temporary-deployment questions.

**Subject:** `The seat-price numbers behind the SaaSpocalypse question`

> Hi Kelsey —
>
> You asked CIOs about the SaaSpocalypse and temporary AI deployments. I'm not a CIO, so I won't answer as one. What I can give you is the seat-price floor beneath that question: of the 108 AI tools we track, 45 publish a monthly per-seat price, 36 at or under $25, median $16.00 (snapshot 2026-11-10, every tier read off the vendor's own page).
>
> The billing split is the part that matters for temporary deployments. Across 19 same-tier pairs, paying monthly costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16). That is the premium a CIO pays for a tool they may switch off — the trade-off your temp-AI question implies.
>
> Every figure carries its vendor URL and check date. Use the dataset free for the SaaSpocalypse or temporary-AI piece, with or without attribution. If you need a CIO voice rather than a price census, I'm the wrong source and will say so.
>
> AIToolsEssentials

*Word count: 157 including the signature — measured on this file; subject line excluded.*

**Stageable:** yes — `scripts/stage_pitch_drafts.py` writes this to `[Gmail]/Drafts`; sending is George's.

---

## 2. Forbes — US solopreneurs, and bootstrapped founders who can quantify what AI removed ◀ 14d, EMAIL, LATE

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **14 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-27T12:57:38Z`, badge *"Posted 14 days ago"*, no expiry notice.
**Who:** **Alison Coleman**, Forbes senior contributor covering entrepreneurs and their startups.
**Ask, her words:** *"Looking for US #solopreneurs, genuinely one-person business that have used AI to
eliminate the need to hire, or simply change when and why the first hire happens."*

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** A published email; the send is George's.
- Re-probed today: https://www.alisoncoleman.co.uk/contact-me/ **HTTP 200, 28,112 bytes**, address in
  visible body text beside a Contact Form 7 form; `forbes.com/sites/alisoncoleman/` remains **HTTP 403**
  (dead end, do not retry).
- One send closes both Forbes rows. `alisoncoleman.co.uk` MX = Google Workspace; deliverability is not
  SMTP-verified, so only a bounce proves anything.

**Subject:** `What the AI stack costs when it stands in for a first hire`

> Hi Alison —
>
> $16.00 is the median cheapest paid seat among the 108 AI tools we track that publish a monthly price (108 tracked, snapshot 2026-11-10). Five seats is $80 a month, $960 a year — the number a US solo founder weighs against a first salary, which is what you asked about.
>
> I can't answer from inside a one-person business, so I won't pretend to. What I do is a dated price census: every tier read off the vendor's own pricing page, with the check date attached. Across 19 same-tier pairs, paying monthly costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16), so the annual figure is the honest one.
>
> Your bootstrapped-founders call, posted seven minutes earlier, is the same arithmetic on the capital side. One dataset answers both, free to use with or without attribution.
>
> AIToolsEssentials

*Word count: 140 including the signature — measured on this file; subject line excluded.*

**Stageable:** yes — staged in `[Gmail]/Drafts` today from this file; the previous 2026-11-09 draft is
deleted so only one version exists.

---

## 3. Business Today — workplace AI adoption and the skills to use the tools ◀ 13d, LINKEDIN DM, LATE

**Source:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
**Posted:** 2026-10-28 11:24 UTC — **13 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-28T11:24:30Z`, badge *"Posted 13 days ago"*, no expiry notice.
**Who:** **Vidhya Das**, Business Today (India Today group); her author page
`businesstoday.in/author/vidhya-das` is HTTP 200, title *"Trainee Sub Editor"*.
**Ask, her words:** *"how employees are adapting to the growing use of artificial intelligence (AI) in
the workplace, and what it takes to use these tools effectively"* — she wants *"independent AI experts,
enterprise AI trainers, researchers and technology professionals"*.

**Reply route:** **LinkedIn DM to linkedin.com/in/vidya-das** — **automatable? No.**
- The body redacts her email and offers *"comment below or DM me on LinkedIn"*. The handle is
  **search-resolved (2026-10-29), not page-published**, and LinkedIn answers **HTTP 999** to this
  monitor's probe — **confirm the profile matches her masthead before sending.**
- No deadline stated on the page. The 10-day figure is this monitor's own line.

**First line does the work (a DM has no subject):**

> Hi Vidhya — $16.00 is the median cheapest paid seat among the 108 AI tools we track that publish a monthly price (108 tracked, snapshot 2026-11-10). Five seats is about $960 a year. That is the number underneath your adoption story: the spend is small enough that an employee can adopt a tool without asking anyone, so training lags adoption rather than causing it.
>
> I'm not a trainer, so I'm not pitching that angle. I run a dated price census — every tier read off the vendor's own pricing page, each with its check date — and I can give you the seat and billing numbers behind the skills question. Across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16).
>
> Every figure carries its vendor URL and check date. Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 144 including the signature — measured on this file.*

**Cannot be staged:** a LinkedIn DM has no mailbox artefact. Paste it yourself.

---

## Why there is no fourth draft

The other 11 AI-token rows in the window were read and excluded: two podcast bookings, an ABC
Australia request for Jensen Huang himself, a TribLive job-seeker call, an AEC data-licensing call,
a founders' profile request, a non-tech AI-impact call aimed at AI companies, a UK fashion-scam
consumer story, a cybersecurity/reverse-engineering call, a consultants' role-change call and an
agent-feedback experiment. None asks about tool pricing or subscription spend, and most publish no
route. The full window accounting is in `digest-2026-11-10.json`.

## Still open past the line — send late or record skipped

- **WSJ / Christopher Mims** — `employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`,
  **36 days**. Route `linkedin.com/in/christopher-mims-club/` (HTTP 200 today). Draft in
  `pitch-drafts-2026-10-27.md` §3.
- **Fast Company / Tobi Amure** — `tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring`,
  **31 days**. Route `hello@tobiamure.com` (contact form as fallback). Draft in
  `pitch-drafts-2026-10-28.md` §3.
- **Anthropic / customer service** — `anthropic-users-and-business-owners-customer-service-experiences`,
  **60 days**. Route Signal `hliwrites.99`. Draft in `pitch-drafts-2026-09-22.md` §2.
- **FinOps / Niloy Ghosh** — `finops-professionals-agentic-ai-cost-overruns`, **65 days**, the
  longest-standing high-relevance request this monitor has never answered. Route: LinkedIn DM to
  `linkedin.com/in/niloy-ghosh`. Draft in `pitch-drafts-2026-09-17.md` §1. Do not draft it a fifth time.
