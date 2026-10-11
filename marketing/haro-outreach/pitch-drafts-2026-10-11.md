# Pitch drafts — 2026-10-11

**Nothing here has been sent.** 114 tracked requests, **56 live unpitched, 1 sendable** (`pitch-queue.md`).

**§1 is the whole queue.** The WSJ blocked-work-accounts request — relevance **medium**, **6 days old**,
carried unsent through two runs now. It is the only row that is live, above the tangential band and
route-resolved at the same time. **Route: LinkedIn DM to `https://www.linkedin.com/in/christopher-mims-club/`**
(re-fetched and re-verified today: HTTP 200, 611,175 bytes, title "Christopher Mims - The Wall Street
Journal | LinkedIn"; the request's own body says "(DMs open)"). **George's lane. Not automatable.**

**§2 records what was NOT drafted this run, and why** — three new rows and three recovered rows, none of
which is sendable. They are recorded rather than drafted on purpose: drafting a row with no route is how
this monitor accumulated 24 unsent drafts in the first place.

**Figures re-derived today.** `data/pricing_snapshots.json` carries `updated: 2026-10-11` (77 snapshots):
**42 of 77 tools publish a monthly price, 33 of those at or under $25/month, median $17.50**, lowest $4
(Khanmigo, checked 2026-09-18). Per-tool figures below come from `data/tool_sources.json` with their own
check dates: Claude Team Standard $20 and Premium $100 per seat/month (checked 2026-09-18). The pair range
was **re-read, not rebuilt**: **1.11x to 2.53x, median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`,
built 2026-10-08). Browse AI $48/month vs $19/month billed annually and Khanmigo $4 are both from
`data/pricing_snapshots.json`, checked **2026-09-18** against `browse.ai/pricing` and `khanmigo.ai/pricing`.
No sentence in this file may go out with an older denominator than the 2026-10-11 refresh.

---

## 1. Employees blocked from AI on work accounts — the workaround spend ◀ SENDABLE, medium, 6d old — SEND THIS

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **6 days.** Page re-read today: HTTP 200, live, badge "Posted in last 7 days".
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist (confirmed at his own byline page).
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work by hand.
**Why it fits:** the blocked employee is the enterprise mirror of this monitor's core shadow-AI request — locked out of the work account, they buy the tool personally, and that purchase is unbudgeted, unenumerated software spend.

**⚠ Honesty constraint — read before sending.** The request wants the respondent's own personal annoyance. We are a publisher, not a blocked employee. The draft says so in its opening line. Do not edit it out.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — re-fetched and
re-verified today: HTTP 200, 611,175 bytes, title "Christopher Mims - The Wall Street Journal | LinkedIn".
The request's own body says "(DMs open)". **George's lane. Not automatable.**
Dead ends recorded so they are not retried: muckrack.com/christopher-mims → HTTP 403; wsj.com/news/author/christopher-mims → HTTP 401.

> Subject: The blocked-work-account workaround, in dated prices
>
> Hi Christopher,
>
> Up front: I can't give you a personal account of being locked out of AI on a work account. What I can give you is what the people who route around that block pay.
>
> We track dated list prices for 77 AI tools. 42 publish a monthly price; 33 of those start at or under $25/month — median $17.50, lowest $4 (Khanmigo). Every figure carries the date we checked it, and the set was refreshed today.
>
> The workaround buyer almost always pays the worst rate. Across the 19 tiers where we hold both billing terms, paying monthly instead of annually costs 1.11x to 2.53x more — median 1.25x. Browse AI is $48/month against $19/month billed annually. One seat expensed personally sits at the top of that range with nobody to negotiate for it.
>
> Cheap enough to pay alone, expensive enough to add up over a year, invisible to whoever holds the budget.
>
> Happy to hand over the full dated set and name the source for every number.
>
> AIToolsEssentials
> https://aitoolsessentials.com

---

## 2. What was NOT drafted this run

Six rows were added to tracking today. None is drafted, and each one is recorded here with the reason, so
that "no new drafts" is a decision and not an omission.

**New rows (all live, all in the AI-topic feed, none sendable):**

- **tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring** — 1 day old. Tobi Amure, freelancing for
  Fast Company's Work Life section, asking for original data with a sample size and method. The closest
  thing this monitor has to a fit in weeks, and still not drafted: his address is Sourcee-redacted, he says
  "No DM pitches here on LinkedIn. Email me", and all six of his byline pages returned HTTP 403 today
  (muckrack, Investopedia, Forbes, TheStreet, Benzinga, Inc). A draft with no route is a 25th unsent draft.
  If a route appears, the honest angle is the method — dated hand-checked list prices, every figure with a
  source URL — and never a workplace-expert credential.
- **ai-cybersecurity-iot-and-web3-founders-and-operators-news-submissions** — 1 day old. Morning Tick wants
  founders of AI/cyber/IoT/Web3 companies to send their own news. We are not such a company. No route.
- **anthropic-gtm-leaders-scaling-300k-b2b-clients** — 2 days old, and tracked for the first time today
  after the vendor-token fix: it sat in the 2026-10-10 window, its body was fetched, and it was dropped
  because "anthropic" was not in the AI token list. The ask is an introduction to Anthropic's GTM team.
  We have none. Not drafted.
- **employees-pay-transparency-good-or-bad** — 1 day old. Business Spotlight Audio wants recorded audio
  from employees on pay transparency, cutoff "by Tuesday/Wednesday". We are not an employee, and it wants
  audio. Not drafted.

**Recovered by the filter fix (all live pages, all long cold, none drafted):**

- **anthropic-api-users-costs-and-token-burn-increase-since-january** — Ed Zitron, 162 days, badge
  "Posted more than 1 month ago". Topically the closest request to this monitor's beat that has ever been
  recorded, and it was invisible for 162 days. Cold, five months old, story long published. Do not draft it;
  decide `skipped` or leave it recorded as cold.
- **prompt-engineers-tokenmaxxing-anecdotes** — 95 days. Cold.
- **investigative-reporters-openai-training-predatory-dynamic-pricing** — 93 days, and not a request at all:
  it offers material to reporters. Cold.

**Drafts still open from earlier runs** (listed so they are not drafted again):

- `pitch-drafts-2026-09-17.md` §1 — finops-professionals-agentic-ai-cost-overruns, 34 days, cold. Route:
  LinkedIn DM to linkedin.com/in/niloy-ghosh. Send late or record `skipped`; do not draft a fifth time.
