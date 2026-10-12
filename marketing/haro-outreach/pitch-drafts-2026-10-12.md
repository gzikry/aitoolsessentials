# Pitch drafts — 2026-10-12

**Nothing here has been sent.** 117 tracked requests, **49 live unpitched, 1 sendable** (`pitch-queue.md`).

**§1 is the whole queue.** The WSJ blocked-work-accounts request — relevance **medium**, **7 days old**,
carried unsent through three runs now. It is the only row that is live, above the tangential band and
route-resolved at the same time. **Route: LinkedIn DM to `https://www.linkedin.com/in/christopher-mims-club/`**
(re-fetched today in `route-checks-2026-10-12.json`: HTTP 200, 643,775 bytes, title "Christopher Mims - The
Wall Street Journal | LinkedIn"; the request's own body says "(DMs open)"). **George's lane. Not automatable.**
Dead ends re-checked today so they are not retried as routes: `muckrack.com/christopher-mims` HTTP 403,
`wsj.com/news/author/christopher-mims` HTTP 401.

**§2 records what was NOT drafted this run, and why** — three new rows, none sendable. They are recorded rather
than drafted on purpose: drafting a row with no route is how this monitor accumulated two dozen unsent drafts
(25 draft files sit on disk, 18 of them naming rows the ledger still records as unsent).

**Figures re-derived today.** `data/pricing_snapshots.json` carries `updated: 2026-10-12` (77 snapshots):
**42 of 77 tools publish a monthly price, 33 of those at or under $25/month, median $17.50**. Per-tool figures
carry their own check dates from `data/pricing_snapshots.json`: Browse AI $48/month vs $19/month billed
annually, verified against `browse.ai/pricing`, **checked 2026-09-18**; Khanmigo $4/month against
`khanmigo.ai/pricing`, checked 2026-09-18. The pair range was **re-read, not rebuilt**: **1.11x to 2.53x,
median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, built 2026-10-08). No sentence in this file may
go out with an older denominator than the 2026-10-12 refresh.

---

## 1. Employees blocked from AI on work accounts — the workaround spend ◀ SENDABLE, medium, 7d old — SEND THIS

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **7 days.** Page re-read today: HTTP 200, live, badge "Posted in last 7 days".
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist (confirmed at his own byline page).
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work by hand.
**Why it fits:** the blocked employee is the enterprise mirror of this monitor's core shadow-AI request — locked out of the work account, they buy the tool personally, and that purchase is unbudgeted, unenumerated software spend.

**⚠ Honesty constraint — read before sending.** The request wants the respondent's own personal annoyance. We are a publisher, not a blocked employee. The draft says so in its opening line. Do not edit it out.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — re-fetched and
re-verified today: HTTP 200, 643,775 bytes, title "Christopher Mims - The Wall Street Journal | LinkedIn".
The request's own body says "(DMs open)". **George's lane. Not automatable.**
Dead ends re-checked today so they are not retried: `muckrack.com/christopher-mims` → HTTP 403; `wsj.com/news/author/christopher-mims` → HTTP 401.

> Subject: The blocked-work-account workaround, in dated prices
>
> Hi Christopher,
>
> Up front: I can't give you a personal account of being locked out of AI on a work account. What I can give you is what the people who route around that block pay.
>
> We track dated list prices for 77 AI tools. 42 publish a monthly price; 33 of those start at or under $25/month — median $17.50. Every figure carries the date we checked it, and the set was refreshed today.
>
> The workaround buyer almost always pays the worst rate. Across the 19 tiers where we hold both billing terms, paying monthly instead of annually costs 1.11x to 2.53x more — median 1.25x. Browse AI is $48/month against $19/month billed annually, verified against browse.ai/pricing and checked 2026-09-18. One seat expensed personally sits at the top of that range, with nobody to negotiate for it.
>
> Cheap enough to pay alone, expensive enough to add up over a year, invisible to whoever holds the budget.
>
> Happy to hand over the full dated set with a source URL for every number.
>
> AIToolsEssentials
> https://aitoolsessentials.com

*Draft length: 172 words including the signature, 179 with the subject line — under the 200-word ceiling
(measured on this file, not asserted). Every figure in it is
re-derived from our own data files today and carries its check date: 42/33/$17.50 and the pair range from
`data/pricing_snapshots.json` (updated 2026-10-12) and `data/monthly_annual_pairs.json` (built 2026-10-08);
Browse AI's two terms from the same snapshot set, checked 2026-09-18 against `browse.ai/pricing`.*

---

## 2. What was NOT drafted this run

Three rows were added to tracking today — every AI-token slug in the 33-slug window. None is drafted, and each
is recorded here with its reason, so that "no new drafts" is a decision and not an omission.

**New rows (all live, all in the AI-topic feed, all 1 day old, none sendable):**

- **hedera-builders-shipping-defi-nfts-rwas-ai-games-and-memes** — a podcast host looking for Hedera (HBAR)
  builders who are shipping, for the Hedera Builder Spotlight. We are not an HBAR builder, the subject is
  crypto-ecosystem building, and "AI" is one item in a list of DeFi/NFT/RWA/game/meme topics. It says "my DMs
  are open" but publishes no handle to DM, so there is no route either.
- **production-designers-ai-impact-on-future-of-filmmaking** — Katy Deboo wants first-hand accounts from people
  who work in production design, on whether AI will affect their role. We hold dated AI tool prices, not
  production-design experience, and its body carries no cost, budget or subscription angle. Address Sourcee-redacted,
  no other route published.
- **ai-researchers-and-policy-experts-5-years-us-race-to-superintelligence** — The Global Signal wants an expert
  podcast guest with 5+ years on US frontier-AI policy. That is an explicit seniority bar we do not meet, and the
  beat is geopolitical strategy, not tool cost. No route published.

**The window itself, stated plainly:** 33 slugs, 3 AI-token, **0 AI+spend**. Both spend-only slugs are false
positives on inspection — `people-who-paid-irish-citizenship-firms-misled-by-ancestry-claims` (a consumer refund
story) and `uts-procurement-staff-why-clv-talks-ended-over-first-nations-college` (a university's decision not to
proceed with a college). Neither is software purchasing. All 33 bodies were fetched and read, which is the only
check that can back a zero.

**Drafts still open from earlier runs** (listed so they are not drafted again):

- `pitch-drafts-2026-09-17.md` §1 — finops-professionals-agentic-ai-cost-overruns, 35 days, cold. Route:
  LinkedIn DM to linkedin.com/in/niloy-ghosh. Send late or record `skipped`; do not draft a fifth time.
- `pitch-drafts-2026-09-22.md` §2 — anthropic-users-and-business-owners-customer-service-experiences, 30 days,
  cold. Route: Signal hliwrites.99. Send late or record `skipped`.
- `pitch-drafts-2026-10-11.md` §1 — the same WSJ request as §1 above; superseded by this file, do not send both.
