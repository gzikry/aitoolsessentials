# Pitch drafts — 2026-11-07

**Two drafts, two sends, both George's lane. Nothing below has been sent.** 265 tracked requests,
**56 live unpitched, 1 sendable** (`pitch-queue.md`, built 2026-11-07), 43 expired on the platform.

**Today's number is 1, and it falls to 0 tomorrow whether or not anyone writes another draft.**
The Business Today row is 10 days old today and crosses this monitor's 10-day line tonight. The two
Forbes rows crossed it overnight at 11 days — both pages still answer HTTP 200 and
`alison@alisoncoleman.co.uk` re-probed live this morning, so they stay here as a late send, not as
dead work. One email to Alison Coleman closes two rows; one LinkedIn DM closes the third.

**Supply was the fourth consecutive zero window.** The 60-slug sitemap window
(2026-11-06T02:09Z → 2026-11-06T23:31Z) produced 6 AI-token slugs, **0 AI+spend**, and 7 new rows
once the body scan added one AI hit the slug filter cannot see. All 7 were read in full; not one
asks what an AI tool, seat or subscription costs, and **none publishes an email address** — one
redacts it, one publishes only a `t.co` shortlink, five publish nothing at all. The body scan reports
two AI+spend hits and both are word-level false positives ("budget isn't there" in an adoption call,
"SaaS" in a sales-rep deal call), so the real count is zero for the fourth window running. The closest
is a call for business owners whose team resists AI adoption ("maybe the budget isn't there"), which
fails on standing: we are a price census, not an operator with a resistant team.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **105 tools**;
`data/pricing_snapshots.json` (`updated: 2026-11-07`) yields **44 with a published monthly per-seat
price, 35 of those at or under $25/month, median $16.50**. Monthly vs annual: **1.11x to 2.53x,
median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, re-asserted 2026-10-16). Superseded,
do not reuse: every 99-tool / $17.50 draft written before 2026-11-03, and the `1.21x–2.53x` pair
claim sent to Jan Suski on 2026-09-18.

**Mailbox: zero replies**, measured today with `jansuski.com` as a positive control that returned
its two known messages (234, 305) before the sweep. No reply to any pitch since 2026-10-11.

---

## 1. Business Today — workplace AI adoption and the skills to use the tools ◀ 10d, LINKEDIN DM, LAST DAY INSIDE THE LINE

**Source:** https://www.sourcee.app/journo-request/ai-trainers-and-researchers-workplace-ai-adoption-and-training
**Posted:** 2026-10-28 11:24 UTC — **10 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-28T11:24:30Z`, badge *"Posted 10 days ago"*, no expiry notice, not in today's
AI-topic feed.
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
- Deadline: none stated on the page. The 10-day figure is this monitor's own line, and today is the
  last day inside it.

**First line does the work (a DM has no subject):**

> Hi Vidhya — I can't answer as a trainer, so I won't pitch myself as one. I run a dated price census
> of AI tools, and it covers the part of your story that sits under the training question: what a
> seat costs, and therefore why adoption outruns it.
>
> As of 2026-11-07: of the 105 AI tools we track, 44 publish a monthly per-seat price. 35 of those
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

## 2. Forbes — US solopreneurs, and bootstrapped founders who can quantify what AI removed ◀ 11d, EMAIL, LATE SEND

**Source:** https://www.sourcee.app/journo-request/us-solopreneurs-ai-eliminated-or-delayed-first-hire-forbes
**Also closes:** https://www.sourcee.app/journo-request/us-founders-bootstrapped-despite-vc-revenue-growth-and-ai-impact (same reporter, posted 2026-10-27 12:50Z, seven minutes earlier)
**Posted:** 2026-10-27 12:57 UTC — **11 days.** Page read today: HTTP 200, body served,
`datePublished 2026-10-27T12:57:38Z`, badge *"Posted 11 days ago"*, no expiry notice.
**Who:** **Alison Coleman**, Forbes senior contributor covering entrepreneurs and their startups;
page domain `forbes.com`.
**Ask, her words:** *"US #solopreneurs, genuinely one-person business that have used AI to eliminate
the need to hire, or simply change when and why the first hire happens."* The sibling call asks
founders who can *"quantify how AI has reduced the capital/headcount needed to build their company."*

**Reply route:** **alison@alisoncoleman.co.uk** — **automatable? No.** A published email; the send is
still George's.
- Re-probed today: https://www.alisoncoleman.co.uk/contact-me/ **HTTP 200, 28,082 bytes**, address
  in visible body text beside a Contact Form 7 form (`route-checks-2026-11-07.json`); homepage
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
> As of 2026-11-07: of the 105 AI tools we track, 44 publish a monthly per-seat price; 35 of those
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

**Staged for this send:** Gmail draft **uid 55** in `[Gmail]/Drafts` now holds the body above (saved
and re-read 2026-11-07, `As of 2026-11-07`), with the subject set and the recipient
`alison@alisoncoleman.co.uk`. The superseded 2026-11-06 draft (uid 54) was deleted so there is only
one version to send. Sending is George's: `himalaya message send -f "[Gmail]/Drafts" 55` from the
mailbox, or hit send in Gmail.

---

## Why there is no third draft today

Seven new rows, none drafted. Not one asks what an AI tool costs, and none carries an email address:

- **Only budget sentence, wrong standing:** `business-owners-and-leaders-team-resistance-to-ai-adoption`
  (1d) wants a business owner losing an internal adoption fight — "maybe the budget isn't there". We
  can price the tools; we are not an operator with a resistant team, and the page publishes no route
  at all (no address, handle or link).
- **Persona we are not:** `woman-replaced-by-ai-and-recruitment-expert-ai-job-loss-case-study` (1d,
  email redacted, no publication to resolve it from); `ai-founders-and-investors-in-barcelona-podcast-and-company-visit-guests`
  (1d, business-school podcast guests, "DM me" with no handle); `ai-users-and-relationship-therapists-dating-conflicts-breakups`
  (1d, wants people who used AI for relationship advice and the therapists who treat them).
- **Not a source request:** `human-behind-ai-crypto-agent-agentwritten-crypto-blogs` (0d) is a call
  for agent-written crypto blogs, route is a `t.co` shortlink; `prs-and-agents-celebrities-national-titles-interview-slots`
  (1d) is a celebrity-booking call addressed to PRs and agents.
- **Body-scan catch, still off-beat:** `b2b-tech-and-software-sales-reps-and-leaders-real-customer-deal-lessons`
  (1d) — The Follow Up newsletter wants a B2B sales rep's war story. "SaaS" in the body tripped the
  spend token; the ask has no cost angle.

## Still open past the line — send late or record skipped

All five have a finished draft, a page that answered HTTP 200 today, and a route. None is in the
sendable count; each needs one decision — send late, or record `skipped` in `pitch-ledger.json`.

- **FinOps / Niloy Ghosh** — `finops-professionals-agentic-ai-cost-overruns`, **61 days**, the
  longest-standing high-relevance request this monitor has never answered. Route: LinkedIn DM to
  `linkedin.com/in/niloy-ghosh`. Draft in `pitch-drafts-2026-09-17.md` §1. Do not draft it a fifth time.
- **Anthropic / customer service** — `anthropic-users-and-business-owners-customer-service-experiences`,
  **57 days**. Route: Signal `hliwrites.99`, re-read verbatim off the live page 2026-09-30. Draft in
  `pitch-drafts-2026-09-22.md` §2.
- **WSJ / Christopher Mims** — `employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`,
  **33 days**, page HTTP 200. Route `linkedin.com/in/christopher-mims-club/` re-probed today (HTTP
  200, 654,042 bytes); `wsj.com` author page 401 and `muckrack.com` 403 are dead ends. Draft in
  `pitch-drafts-2026-10-27.md` §3.
- **Fast Company / Tobi Amure** — `tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring`, **28
  days**, page HTTP 200. Route `hello@tobiamure.com` (tobiamure.com HTTP 200, 63,370 bytes; /contact/
  18,505 bytes), contact form as fallback. Draft in `pitch-drafts-2026-10-28.md` §3.
- **Raconteur / Simon Chandler** — `fulltime-employees-shadow-ai-use-and-paying-outofpocket`, **51
  days**, and its ledger entry is **SENT BUT BOUNCED** (550 NoSuchUser). Do not retry that address;
  a fresh route is needed before it can go anywhere.
