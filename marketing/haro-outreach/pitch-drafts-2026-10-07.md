# Pitch drafts — 2026-10-07

**Nothing here has been sent.** 94 tracked requests, **47 live unpitched, 1 sendable** (`pitch-queue.md`).

**§1 is the sendable row** — the WSJ blocked-work-accounts request, now **2 days old**, still the only
row in the queue that is both above the tangential band and route-resolved. Its route was re-fetched
today (HTTP 200 with a matching title) rather than trusted from the digest. Everything else the
window produced today was off-beat: ten AI-token finds, none core-beat, none with a usable route.

**Figures re-derived today.** `data/pricing_snapshots.json` carries `updated: 2026-10-07` (76
snapshots); the set is **42 of 76 tools publishing a monthly price, 33 of those at or under
$25/month, median $17.50**, lowest $4.00 (khanmigo). Re-derived by
`marketing/haro-outreach/_figures_1007.py`. The pair file was **rebuilt, not re-read**:
`scripts/extract_monthly_annual_pairs.py` re-asserted all 19 curated pairs against the refreshed
snapshot, exited 0 and rewrote `data/monthly_annual_pairs.json` — **1.11x to 2.53x, median 1.25x over
19 tiers across 14 tools**. Superseded 40/31/$16.50 and floors of 1.16x/1.21x sit in older dated
drafts and must not be reused.

---

## 1. Employees blocked from AI on work accounts — the workaround spend ◀ SENDABLE, 2d old, only sendable row

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **2 days.** Page re-read today: HTTP 200, live, badge "Posted in last 7 days".
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist (his own byline page confirms the title).
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work by hand.

**Why it fits:** the blocked employee is the enterprise mirror of this monitor's core shadow-AI request — locked out of the work account, they buy the tool personally, and that purchase is unbudgeted, unenumerated software spend. That is the quantity our dated price set exists to make visible.

**⚠ Honesty constraint — read before sending.** The request wants the respondent's own personal annoyance. We are a publisher, not a blocked employee. The draft says so in its opening line. Do not edit it out.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — verified today:
HTTP 200, 603,318 bytes, title "Christopher Mims - The Wall Street Journal | LinkedIn". The request's own
body says "(DMs open)". **George's lane. Not automatable.**
Dead ends recorded so they are not retried: muckrack.com/christopher-mims → HTTP 403; wsj.com/news/author/christopher-mims → HTTP 401.

> Subject: The blocked-work-account workaround, in dated prices
>
> Hi Christopher,
>
> Straight up front: I can't give you a personal account of being locked out of AI on a work account. What
> I can give you is what the people who go around that block are paying.
>
> We track dated list prices for 76 AI tools. 42 publish a monthly price; 33 of those start at or under
> $25/month, median $17.50, lowest $4 (Khanmigo). Every figure carries the date we checked it.
>
> The workaround buyer almost always pays the worst rate. Across the 19 tiers where we hold both terms,
> paying monthly instead of annually costs 1.11x to 2.53x more — median 1.25x. Browse AI is $48/month
> against $19/month billed annually. Someone quietly expense-ing one seat personally sits at the top of
> that range with no one to negotiate for them.
>
> That is the shape of it: cheap enough to pay alone, expensive enough to add up over a year, and
> invisible to whoever holds the budget.
>
> Happy to hand over the full dated set and name the source for every number.
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --

---

## 2. Shadow AI spend — employees paying out of pocket ◀ 20d, crossed cold 2026-09-28, unsent through EIGHTEEN runs

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **20 days.** Page re-read today: HTTP 200, badge "Posted 20 days ago".
**Who:** **Simon Chandler** — the page's own author field; covers enterprise tech for Raconteur.
**Ask:** quotes from full-time employees who use AI without their employer's knowledge and pay personally.

**Why it is still worth sending late:** identical to §1's ground — employees buying AI unapproved and paying personally is unbudgeted software spend. Raconteur's contact page asks for "pitches with exclusive business data", which is what we hold. It remains the only **high**-relevance request this monitor has ever produced with a resolved route.

**⚠ Honesty constraint — read before sending.** The same one as §1: the request wants employees' personal accounts and we are a publisher with none. Do not edit that line out.

**Reply route:** `simon.chandler@raconteur.net` — re-resolved today off the live
`raconteur.net/contributors/simon-chandler` (HTTP 200, 154,819 bytes; data-part1/2/3 = simon.chandler + raconteur + net; control `/contributors/tom-dennis` HTTP 200 carries tom.dennis + raconteur + net). The older `/author/simon-chandler/` still 404s and must not be cited. **George's lane. Not automatable** — the address is assembled from the byline page's JS triplet, not published in the request body.

> Subject: Shadow AI spend — what the out-of-pocket tiers actually cost
>
> Hi Simon,
>
> Straight up front: I can't give you a personal account of paying for AI behind my employer's back. What I
> can give you is what those out-of-pocket buyers are actually paying.
>
> We track dated pricing for 76 AI tools. 42 publish a monthly price; 33 of those start at or under
> $25/month — median $17.50, lowest $4 (Khanmigo).
>
> Nearly all charge more if you pay monthly instead of annually. Across the 19 tiers where we hold both
> terms, the gap runs 1.11x to 2.53x, median 1.25x. Browse AI is $48/month against $19/month billed
> annually. The buyer with no company card pays the top of that range.
>
> That's the shape of shadow spend: small enough to expense personally, expensive enough to matter over a
> year, and invisible to whoever holds the budget.
>
> Happy to hand over the full dated set, and to name my source for every number.
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --

---

## 3. Speciality food retailers spending £10k on tech ◀ 19d, crossed cold 2026-09-28 — send or skip

**Source:** https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
**Posted:** 2026-09-18 — **19 days.** **Crossed the cold line on 2026-09-28.** Its October issue window
has closed, so this is now a send-or-skip call: send it late or record it as skipped in `pitch-ledger.json`.

**⚠ Standing constraint — read before sending.** We are not a speciality food retailer. The draft says so
in its first line and offers only the tool-spend half of the £10k question.

**Reply route:** `holly.shackleton@artichokehq.com` — re-read today off
`specialityfoodmagazine.com/contact` (HTTP 200, 59,488 bytes, alongside five other named masthead
addresses). **George's lane. Not automatable** (address published on the publication's contact page, sent by hand).

> Subject: The £10k tech question — the software half, in dated numbers
>
> Hi Holly,
>
> Up front: we're not a speciality food retailer, so I can't give you a shop's own £10k breakdown. I can
> give you the part most of those budgets get spent inside — recurring AI and software pricing.
>
> We track dated list prices for 76 AI tools. 42 publish a monthly price; 33 of those start at or under
> $25/month, median $17.50 (snapshots re-checked 2026-10-07). At that level ten small subscriptions is a
> four-figure annual line item before anything bespoke.
>
> The trap is the billing term. Across the 19 tiers where we hold both a monthly and an annual-billed
> monthly price, paying monthly costs 1.11x to 2.53x more — median 1.25x. A retailer paying month to month
> on five tools is buying roughly a quarter more than they need to.
>
> If it's useful, I'll send the dated set with a source for every figure.
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --
