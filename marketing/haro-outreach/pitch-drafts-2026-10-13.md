# Pitch drafts — 2026-10-13

**Nothing here has been sent.** 123 tracked requests, **50 live unpitched, 1 sendable** (`pitch-queue.md`,
built 2026-10-13).

**§1 is the whole queue.** The WSJ blocked-work-accounts request — relevance **medium**, **8 days old**,
carried unsent through four runs now. It is the only row that is live, above the tangential band and
route-resolved at the same time. **Route: LinkedIn DM to `https://www.linkedin.com/in/christopher-mims-club/`**
(re-fetched today in `route-checks-2026-10-13.json`: HTTP 200, 609,627 bytes, title "Christopher Mims - The
Wall Street Journal | LinkedIn"; the request's own body says "(DMs open)"). **George's lane. Not automatable.**
Dead ends re-checked today so they are not retried as routes: `muckrack.com/christopher-mims` HTTP 403,
`wsj.com/news/author/christopher-mims` HTTP 401.

**It has two days left as a sendable row.** At 10 days old on 2026-10-15 it sits at the cold line; on
2026-10-16 it crosses it and leaves the sendable list. Nothing brings it back after that.

**§2 records what was NOT drafted this run, and why** — six new rows, none sendable, none on our beat.
They are recorded rather than drafted on purpose: drafting a row with no route is how this monitor
accumulated two dozen unsent drafts (26 draft files sit on disk, 18 of them naming rows the ledger still
records as unsent).

**Figures re-derived today.** `data/pricing_snapshots.json` carries `updated: 2026-10-13` (77 snapshots):
**42 of 77 tools publish a monthly price, 33 of those at or under $25/month, median $17.50**. Per-tool
figures carry their own check dates from `data/pricing_snapshots.json`: Browse AI $48/month vs $19/month
billed annually, verified against `browse.ai/pricing`, **checked 2026-09-18**; Khanmigo $4/month against
`khanmigo.ai/pricing`, checked 2026-09-18 (`tool_sources.json`). The pair range was **re-read, not
rebuilt**: **1.11x to 2.53x, median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, built
2026-10-08). No sentence in this file may go out with an older denominator than the 2026-10-13 refresh.

---

## 1. Employees blocked from AI on work accounts — what the workaround buyer pays ◀ SENDABLE, medium, 8d old — SEND THIS

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **8 days.** Page re-read today: HTTP 200, live, badge "Posted 8 days ago".
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist (confirmed at his own byline page).
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work by hand.
**Why it fits:** the blocked employee is the enterprise mirror of this monitor's core shadow-AI request — locked out of the work account, they buy the tool personally, and that purchase is unbudgeted, unenumerated software spend.

**⚠ Honesty constraint — read before sending.** The request wants the respondent's own personal annoyance. We are a publisher, not a blocked employee. The draft says so in its opening line. Do not edit it out.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — re-fetched and
re-verified today: HTTP 200, 609,627 bytes, title "Christopher Mims - The Wall Street Journal | LinkedIn".
The request's own body says "(DMs open)". **George's lane. Not automatable.** A LinkedIn DM has no subject
line; the text below is the whole message.
Dead ends re-checked today so they are not retried: `muckrack.com/christopher-mims` → HTTP 403; `wsj.com/news/author/christopher-mims` → HTTP 401.

> Hi Christopher — up front: I can't give you a personal account of being locked out of AI on a work account. What I can give you is what the people who route around that block pay.
>
> We hand-check the list price of 77 AI tools. 42 publish a monthly price and 33 of those start at or under $25/month — median $17.50. Every figure carries the date we checked it; the set was refreshed today.
>
> The workaround buyer almost always pays the worst rate. Across the 19 tiers where we hold both billing terms, paying monthly instead of annually costs 1.11x to 2.53x more — median 1.25x. Browse AI is $48/month against $19/month billed annually (checked 2026-09-18).
>
> That combination is the story: cheap enough to put on a personal card without asking anyone, expensive enough to add up across a year, and invisible to whoever holds the budget.
>
> Happy to send the full dated set with a source URL for every number, no charge.
>
> AIToolsEssentials

*Draft length: 164 words including the signature (measured on this file, not asserted) — under the
200-word ceiling, and it carries no subject line because the route is a DM. Every figure in it is
re-derived from our own data files today and carries its check date: 42/33/$17.50 from
`data/pricing_snapshots.json` (updated 2026-10-13); the pair range from `data/monthly_annual_pairs.json`
(built 2026-10-08); Browse AI's two terms from the same snapshot set, checked 2026-09-18 against
`browse.ai/pricing`.*

---

## 2. What was NOT drafted this run

Six rows were added to tracking today — every AI-token slug in the 105-slug window. None is drafted, and
each is recorded here with its reason, so that "no new drafts" is a decision and not an omission.

**New rows (all live, 1–2 days old, none with a route, none on our beat):**

- **b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research** — the window's only AI+spend slug
  match, and a false positive. It cites Forrester on buyers using AI to research vendors and asks B2B
  buyers, procurement, RevOps and SaaS sales leaders for lessons. "Procurement" and "SaaS" there describe
  how software is *bought*, not what AI tools *cost*; the body names no price, budget or subscription, and
  we are a publisher rather than a procurement team. Address Sourcee-redacted, no other route.
- **software-engineers-who-left-tech-jobs-lost-to-ai-coding-tools** — Business Insider (Thibault Spirlet)
  wants engineers who have *left* tech because AI coding tools removed the part of the job they loved. A
  first-person career story we cannot supply. Address Sourcee-redacted, no other route.
- **manufacturers-and-ai-safety-experts-ai-risks-in-chemical-food-defense** — Manufacturing Dive wants
  manufacturers and AI safety experts on AI risk in chemical, food and defence manufacturing. No cost angle.
  Address Sourcee-redacted, no other route.
- **uk-baby-boomers-misinformation-sharing-and-ai-influence-online** — Canvas8 wants academics researching
  misinformation among UK baby boomers. An explicit academic-researcher standing bar. No route published.
- **global-development-professionals-using-ai-across-programs-and-policy** — Devex wants global-development
  staff describing the tools they use. Not our sector, no cost angle, no route published.
- **caine-prize-winners-gen-ai-accusations-targeting-black-writers** — a public DM request to three named
  Caine Prize winners about gen-AI plagiarism accusations. Authorship integrity, no purchasing element, and
  the people asked are named individuals. No route published.

**The window itself, stated plainly:** 105 slugs, 6 AI-token, **1 AI+spend (a false positive), 0 core-beat**.
All seven spend-only slugs are consumer or non-software stories (fuel prices, council tax, SNAP cuts, elder
care, cost-of-living, a pensioner story, a hospitality-economy piece). All 105 window bodies were fetched and
read, which is the only check that can back a zero.

**Drafts still open from earlier runs** (listed so they are not drafted again):

- `pitch-drafts-2026-09-17.md` §1 — finops-professionals-agentic-ai-cost-overruns, 36 days, cold. Route:
  LinkedIn DM to linkedin.com/in/niloy-ghosh. Send late or record `skipped`; do not draft a fifth time.
- `pitch-drafts-2026-09-22.md` §2 — anthropic-users-and-business-owners-customer-service-experiences, 31 days,
  cold. Route: Signal hliwrites.99. Send late or record `skipped`.
- `pitch-drafts-2026-10-12.md` §1 — the same WSJ request as §1 above; superseded by this file, do not send both.
