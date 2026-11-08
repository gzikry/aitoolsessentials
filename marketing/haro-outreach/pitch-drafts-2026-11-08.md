# Pitch drafts — 2026-11-08

**Two drafts, two sends, both George's lane. Nothing below has been sent.** 265 tracked requests,
**48 live unpitched, 0 sendable** (`pitch-queue.md`, built 2026-11-08), 43 expired on the platform.

**Zero new supply, fifth window running.** The 23-slug sitemap window
(2026-11-06T23:31Z → 2026-11-08T00:14Z) carried **0 AI-token slugs, 0 AI+spend slugs**, and every one
of the 23 bodies was fetched and read: **0 mention AI at body level** — so this is not a keyword miss,
there is nothing in the window. The only spend-token slug asks homeowners about holiday spending.
That is why there is no new draft today: the two sends below are carried, and they are the whole
actionable set.

**Both carried rows are now past the 10-day line and both pages and routes answered today.**
Forbes is 12 days old (page HTTP 200, `alison@alisoncoleman.co.uk` re-probed HTTP 200 on
alisoncoleman.co.uk/contact-me/, 28,113 bytes); Business Today is 11 days old (page HTTP 200).
One email closes two Forbes rows; one LinkedIn DM closes the third.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **105 tools**;
`data/pricing_snapshots.json` (`updated: 2026-11-08`) yields **44 with a published monthly per-seat
price, 35 of those at or under $25/month, median $16.50**. Monthly vs annual: **1.11x to 2.53x,
median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, re-asserted 2026-10-16). Superseded,
do not reuse: every 99-tool / $17.50 draft written before 2026-11-03, and the `1.21x–2.53x` pair
claim sent to Jan Suski on 2026-09-18.

**Mailbox: zero replies**, measured today with `jansuski.com` as a positive control that returned
its two known messages (234, 305) before the sweep. No reply to any pitch since 2026-10-11.

---

## 1. Forbes — US solopreneurs, and bootstrapped founders who can quantify what AI removed ◀ 12d, EMAIL, LATE SEND

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted 2026-10-27 12:50Z, seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **12 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-27T12:57:38Z`, badge *"Posted 12 days ago"*, no expiry notice.
**Who:** **Alison Coleman**, Forbes senior contributor covering entrepreneurs and their startups;
page domain `forbes.com`.
**Ask, her words:** *"US #solopreneurs, genuinely one-person business that have used AI to eliminate
the need to hire, or simply change when and why the first hire happens."* The sibling call asks
founders who can *"quantify how AI has reduced the capital/headcount needed to build their company."*

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** A published email; the send is
still George's.
- Re-probed today: https://www.alisoncoleman.co.uk/contact-me/ **HTTP 200, 28,113 bytes**, address in
  visible body text beside a Contact Form 7 form (`route-checks-2026-11-08.json`); homepage
  `alisoncoleman.co.uk/` **HTTP 200, 21,366 bytes**.
- Dead end, do not retry: `forbes.com/sites/alisoncoleman/` answers **HTTP 403**.
- `alisoncoleman.co.uk` MX = Google Workspace. Deliverability is **not SMTP-verified** — a Google MX
  accepts at RCPT whatever the mailbox, so only a bounce proves anything.

**Subject:** `What the AI stack costs when it stands in for a first hire`

> Hi Alison —
>
> You asked US one-person businesses how AI changed when the first hire happens, and founders who
> can quantify what AI took out of the build. I can't answer from inside either, so I won't pretend
> to.
>
> I run a price census: what AI tools list at, read off each vendor's own pricing page, with the date
> of every check.
>
> As of 2026-11-08: of the 105 AI tools we track, 44 publish a monthly per-seat price; 35 of those
> sit at or under $25, and the median cheapest paid tier is $16.50. Five seats on that median cost
> $82.50 a month, about $990 a year — the figure a solo founder weighs against a salary. Billing is
> the other half: across 19 same-tier monthly/annual pairs, paying monthly costs 1.11x to 2.53x the
> annual rate, median 1.25x (pair set re-asserted 2026-10-16).
>
> Your bootstrapped-founders call, posted seven minutes earlier, is the same arithmetic from the
> capital side. One dataset answers both, and every figure carries its vendor URL and check date.
> Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 179 including the signature — measured on this file, subject line excluded.*

**Staged for this send:** Gmail draft in `[Gmail]/Drafts` holds the body above, re-staged today from
this file by `scripts/stage_pitch_drafts.py` (which refuses to stage a body whose tool count or median
disagrees with today's dataset). The superseded 2026-11-07 draft (uid 55) is deleted so only one
version exists. Sending is George's: hit send in Gmail, or
`himalaya message send -f "[Gmail]/Drafts" <uid>` from the mailbox.

---

## 2. Business Today — workplace AI adoption and the skills to use the tools ◀ 11d, LINKEDIN DM

**Source:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
**Posted:** 2026-10-28 11:24 UTC — **11 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-28T11:24:30Z`, badge *"Posted 11 days ago"*, no expiry notice.
**Who:** **Vidhya Das**, Business Today (India Today group); page domain `businesstoday.in`; her
author page `businesstoday.in/author/vidhya-das` HTTP 200, title *"Trainee Sub Editor"*.
**Ask, her words:** *"how employees are adapting to the growing use of artificial intelligence (AI)
in the workplace, and what it takes to use these tools effectively"* — she wants *"independent AI
experts, enterprise AI trainers, researchers and technology professionals"*.

**Reply route:** **LinkedIn DM to `linkedin.com/in/vidya-das`** — **automatable? No.**
- The body redacts the email (*"You can also email me at [email redacted]"*) and offers *"comment
  below or DM me on LinkedIn"*. The handle is search-resolved (2026-10-29), not page-published, and
  **LinkedIn answers HTTP 999 to this monitor's probe** — confirm the profile matches her face and
  masthead before sending. Her Business Today author page publishes no address.
- Deadline: none stated on the page. The 10-day figure is this monitor's own line, and this row is
  one day past it.

**First line does the work (a DM has no subject):**

> Hi Vidhya — I can't answer as a trainer, so I won't pitch myself as one. I run a dated price census
> of AI tools, and it covers the part of your story that sits under the training question: what a
> seat costs, and therefore why adoption outruns it.
>
> As of 2026-11-08: of the 105 AI tools we track, 44 publish a monthly per-seat price. 35 of those
> start at or under $25, and the median cheapest paid tier is $16.50 — cheap enough that an employee
> can adopt a tool without asking anyone. Annual billing barely helps: across 19 same-tier pairs,
> monthly costs 1.11x to 2.53x the annual rate, median 1.25x (re-asserted 2026-10-16).
>
> If your story is the skills gap, that is the number underneath it: the spend is small enough to
> stay invisible to whoever owns the training budget.
>
> Every figure carries its vendor URL and check date. Free to use, with or without attribution.
>
> AIToolsEssentials

*Word count: 158 including the signature — measured on this file; a DM has no subject line.*

---

## Why there is no third draft today

The window carried nothing to draft: 23 slugs, **0 AI-token, 0 AI+spend, 0 body-level AI mentions** —
all 23 bodies were read. The five spend-token-adjacent or AI-adjacent rows that exist in the live set
are all below the relevance bar or route-less:

- **Deadline already closed, recorded skipped:** `cios-and-cisos-steps-to-address-ai-orphans`
  (5d, medium, route resolving at `Kelsey.ziser@informationweek.com`) — her body states *"Deadline for
  interviews is Wednesday EOD"*; posted 2026-11-02, so Wednesday was 2026-11-04. Drafted on
  2026-11-03 and never sent; the ledger records it `skipped` since 2026-11-05. Page live, deadline dead.
- **No standing:** `anthropic-employees-company-decisionmaking-and-workplace-impact` (4d) is addressed
  to Anthropic staff, with a Signal handle (`cweinberg.91`) that leads to the NYT reporter's tips line,
  not a price story.
- **No route and no standing:** `business-owners-and-leaders-team-resistance-to-ai-adoption` (2d,
  low-medium) has the only budget sentence of the week (*"maybe the budget isn't there"*) but asks for
  an operator losing an internal adoption fight; the page publishes no address, handle or link.

## Still open past the line — send late or record skipped

Four beyond the two above; each has a finished draft, a page that answered HTTP 200 today, and a
route. None is in the sendable count; each needs one decision.

- **WSJ / Christopher Mims** — `employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`,
  **34 days**, page HTTP 200. Route `linkedin.com/in/christopher-mims-club/` re-probed today (HTTP 200,
  609,152 bytes); `wsj.com` author page 401 and `muckrack.com` 403 are dead ends. Draft in
  `pitch-drafts-2026-10-27.md` §3.
- **Fast Company / Tobi Amure** — `tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring`, **29
  days**, page HTTP 200. Route `hello@tobiamure.com` (tobiamure.com HTTP 200, 63,370 bytes; /contact/
  18,505 bytes), contact form as fallback. Draft in `pitch-drafts-2026-10-28.md` §3.
- **Anthropic / customer service** — `anthropic-users-and-business-owners-customer-service-experiences`,
  **58 days**. Route Signal `hliwrites.99`, re-read verbatim off the live page 2026-09-30. Draft in
  `pitch-drafts-2026-09-22.md` §2.
- **FinOps / Niloy Ghosh** — `finops-professionals-agentic-ai-cost-overruns`, **62 days**, the
  longest-standing high-relevance request this monitor has never answered. Route: LinkedIn DM to
  `linkedin.com/in/niloy-ghosh`. Draft in `pitch-drafts-2026-09-17.md` §1. Do not draft it a fifth time.
