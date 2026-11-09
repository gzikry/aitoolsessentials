# Pitch drafts — 2026-11-09

**Two drafts, two sends, both George's lane. Nothing below has been sent.**

266 tracked requests, **40 live unpitched, 0 sendable** (`pitch-queue.md`, built 2026-11-09),
43 expired on the platform. **Sixth consecutive window with nothing on-beat:** 27 slugs,
1 AI-token, 0 AI+spend, every one of the 27 bodies read; the only AI row is a podcast booking
call that publishes no address (recorded in the digest, not drafted).

The two below are the whole actionable set: both pages answered HTTP 200 today with their own
badges (*"Posted 13 days ago"*, *"Posted 12 days ago"*), both routes were re-probed today, and
both are **late sends** — 2-3 days past this monitor's own 10-day line, which is a heuristic and
not a platform deadline. No page on this source carries an expiry; a send or a `skipped` entry
closes each one.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **105 tools**;
`data/pricing_snapshots.json` (`updated: 2026-11-09`) yields **44 with a published monthly
per-seat price, 35 of those at or under $25/month, median $16.50**. Monthly vs annual:
**1.11x to 2.53x, median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, re-asserted
2026-10-16). Superseded, do not reuse: every 99-tool / $17.50 draft written before 2026-11-03.

**Mailbox: zero replies**, measured today with `jansuski.com` as a positive control that returned
its two known messages (234, 305). No reply to any pitch since 2026-10-11.

---

## 1. Forbes — US solopreneurs, and bootstrapped founders who can quantify what AI removed ◀ 13d, EMAIL, LATE SEND

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **13 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-27T12:57:38Z`, badge *"Posted 13 days ago"*, no expiry notice.
**Who:** **Alison Coleman**, Forbes senior contributor covering entrepreneurs and their startups.
**Ask, her words:** *"US #solopreneurs, genuinely one-person business that have used AI to eliminate
the need to hire, or simply change when and why the first hire happens."* The sibling call asks
founders who can *"quantify how AI has reduced the capital/headcount needed to build their company."*

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** A published email; the send is
still George's.
- Re-probed today: https://www.alisoncoleman.co.uk/contact-me/ **HTTP 200, 28,123 bytes**, address in
  visible body text beside a Contact Form 7 form; `forbes.com/sites/alisoncoleman/` remains **HTTP 403**
  (dead end, do not retry).
- `alisoncoleman.co.uk` MX = Google Workspace. Deliverability is **not SMTP-verified** — Google
  accepts at RCPT whatever the mailbox, so only a bounce proves anything.

**Subject:** `What the AI stack costs when it stands in for a first hire`

> Hi Alison —
>
> $16.50 a seat is the median cheapest paid tier among the 44 AI tools we track that publish a monthly price (105 tracked, snapshot 2026-11-09). Five seats is $82.50 a month, about $990 a year — the number a US solo founder weighs against a first salary, which is what you asked about.
>
> I can't answer from inside a one-person business, so I won't pretend to. What I do is a dated price census: every tier read off the vendor's own pricing page, with the check date attached. Across 19 same-tier pairs, paying monthly costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16), so the annual figure is the honest one.
>
> Your bootstrapped-founders call, posted seven minutes earlier, is the same arithmetic on the capital side. One dataset answers both, free to use with or without attribution.
>
> AIToolsEssentials

*Word count: 143 including the signature — measured on this file, subject line excluded.*

**Staged for this send:** rewritten into `[Gmail]/Drafts` today from this file by
`scripts/stage_pitch_drafts.py`, which refuses to stage a body whose tool count or median disagrees
with today's dataset. Sending is George's: hit send in Gmail, or
`himalaya message send -f "[Gmail]/Drafts" <uid>` from the mailbox.

---

## 2. Business Today — workplace AI adoption and the skills to use the tools ◀ 12d, LINKEDIN DM

**Source:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
**Posted:** 2026-10-28 11:24 UTC — **12 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-28T11:24:30Z`, badge *"Posted 12 days ago"*, no expiry notice.
**Who:** **Vidhya Das**, Business Today (India Today group); her author page
`businesstoday.in/author/vidhya-das` HTTP 200, title *"Trainee Sub Editor"*.
**Ask, her words:** *"how employees are adapting to the growing use of artificial intelligence (AI)
in the workplace, and what it takes to use these tools effectively"* — she wants *"independent AI
experts, enterprise AI trainers, researchers and technology professionals"*.

**Reply route:** **LinkedIn DM to `linkedin.com/in/vidya-das`** — **automatable? No.**
- The body redacts her email and offers *"comment below or DM me on LinkedIn"*. The handle is
  **search-resolved (2026-10-29), not page-published**, and LinkedIn answered **HTTP 999** to today's
  probe — confirm the profile matches her face and masthead before sending. Her author page publishes
  no address.
- No deadline stated on the page. The 10-day figure is this monitor's own line.

**First line does the work (a DM has no subject):**

> Hi Vidhya — $16.50 is the median cheapest paid seat among the 44 AI tools we track that publish a monthly price (105 tracked, snapshot 2026-11-09). Five seats is about $990 a year. That is the number underneath your adoption story: the spend is small enough that an employee can adopt a tool without asking anyone, so training lags adoption rather than causing it.
>
> I'm not a trainer, so I'm not pitching that angle. I run a dated price census — every tier read off the vendor's own pricing page, each with its check date — and I can give you the seat and billing numbers behind the skills question. Across 19 same-tier pairs, monthly billing costs 1.11x to 2.53x the annual rate, median 1.25x (asserted 2026-10-16).
>
> Every figure carries its vendor URL and check date. Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 144 including the signature — measured on this file; a DM has no subject line.*

**Cannot be staged:** a LinkedIn DM has no mailbox artefact. Paste it into the DM yourself; the
route check is the only pre-send validation available.

---

## Why there is no third draft today

The window carried nothing to draft: 27 slugs, **1 AI-token, 0 AI+spend**, all 27 bodies read.
The single AI row is a podcast-booking call (`podcasters-and-linkedin-live-creators-tech-and-ai-and-career-topics`,
1d) that asks for hosts and publishes a redacted address — no route, no standing.

The nearest third candidate is `midlife-professionals-career-regret` (10d, Business Insider,
published email) but its relevance is **low**: a career-regret feature is not a software-cost story
and a price dataset would be padding inside it. Drafting it would produce a pitch we cannot defend
on the merits.

## Still open past the line — send late or record skipped

Each has a finished draft, a page that answered HTTP 200 today, and a route. None is in the
sendable count.

- **WSJ / Christopher Mims** — `employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`,
  **35 days**. Route `linkedin.com/in/christopher-mims-club/`. Draft in `pitch-drafts-2026-10-27.md` §3.
- **Fast Company / Tobi Amure** — `tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring`,
  **30 days**. Route `hello@tobiamure.com` (contact form as fallback). Draft in
  `pitch-drafts-2026-10-28.md` §3.
- **Anthropic / customer service** — `anthropic-users-and-business-owners-customer-service-experiences`,
  **59 days**. Route Signal `hliwrites.99`. Draft in `pitch-drafts-2026-09-22.md` §2.
- **FinOps / Niloy Ghosh** — `finops-professionals-agentic-ai-cost-overruns`, **63 days**, the
  longest-standing high-relevance request this monitor has never answered. Route: LinkedIn DM to
  `linkedin.com/in/niloy-ghosh`. Draft in `pitch-drafts-2026-09-17.md` §1. Do not draft it a fifth time.
