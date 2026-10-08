# Pitch drafts — 2026-10-08

**Nothing here has been sent.** 101 tracked requests, **54 live unpitched, 1 sendable** (`pitch-queue.md`).

**§1 is the sendable row** — the WSJ blocked-work-accounts request, now **3 days old**, still the only
row in the queue that is both above the tangential band and route-resolved. Its route was re-fetched
today (HTTP 200 with a matching title) rather than trusted from the digest.

**§2 is the find of the run** — the first core-beat AI+spend request in fourteen runs, and the
best-matching request this monitor has ever held: Google & Claude enterprise seat and token costs.
It is relevance **high** but **has no reply route** (the page publishes no address or handle), so it
is not sendable until George resolves one. The data is ready; only the route is missing.

**§3 carries the Raconteur shadow-AI draft** — 21 days old, unsent through nineteen runs.
The Speciality Food draft (20 days, October window closed) is now a **send-or-skip** call: send it
late or record it in `pitch-ledger.json`.

**Figures re-derived today.** `data/pricing_snapshots.json` carries `updated: 2026-10-08` (76
snapshots); the set is **42 of 76 tools publishing a monthly price, 33 of those at or under
$25/month, median $17.50**, lowest $4.00 (khanmigo). Re-derived by
`marketing/haro-outreach/_figures_1008.py`. The pair file was **rebuilt, not re-read**:
`scripts/extract_monthly_annual_pairs.py` re-asserted all 19 curated pairs against the refreshed
snapshot, exited 0 and rewrote `data/monthly_annual_pairs.json` — **1.11x to 2.53x, median 1.25x over
19 tiers**. Superseded 40/31/$16.50 and floors of 1.16x/1.21x sit in older dated drafts and must not
be reused.

---

## 1. Employees blocked from AI on work accounts — the workaround spend ◀ SENDABLE, 3d old, only sendable row

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **3 days.** Page re-read today: HTTP 200, live, badge "Posted in last 7 days".
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist (his own byline page confirms the title).
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work by hand.

**Why it fits:** the blocked employee is the enterprise mirror of this monitor's core shadow-AI request — locked out of the work account, they buy the tool personally, and that purchase is unbudgeted, unenumerated software spend. That is the quantity our dated price set exists to make visible.

**⚠ Honesty constraint — read before sending.** The request wants the respondent's own personal annoyance. We are a publisher, not a blocked employee. The draft says so in its opening line. Do not edit it out.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — verified today:
HTTP 200, 603,602 bytes, title "Christopher Mims - The Wall Street Journal | LinkedIn". The request's own
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
> https://aitoolessentials.com
>
> --

---

## 2. Google & Claude enterprise seats and token costs ◀ HIGH relevance, 0d old — BEST MATCH IN 14 RUNS, but NO ROUTE

**Source:** https://www.sourcee.app/journo-request/google-and-claude-enterprise-users-seats-and-token-costs
**Posted:** 2026-10-07 19:16 UTC — **0 days (posted yesterday).** Page re-read today: HTTP 200, live, badge "Posted in last 7 days".
**Who:** **Glenn Hansen** — the page's own author field; the body says he reports on power-equipment manufacturing (lawnmowers, chainsaws). Outlet not named.
**Ask:** "enterprise-level costs for AI seats and tokens. Google or Claude users care to enlighten me?"

**Why it is the run's find:** this is the exact quantity our dated price set measures, and it is the first core-beat AI+spend request in **fourteen** runs. The three facts below are all in `data/tool_sources.json` with check dates.

**⚠ Standing constraint.** We are a publisher, not an enterprise buyer running Google/Claude seats at scale. The draft claims only what our dated records show and says so.

**⚠ Route unresolved — do not send blind.** The page publishes **no address, handle or link** and gives no reply instruction (verified today: `email_redacted=False` but `emails_on_page=none`, published links = Sourcee chrome only). A web search cannot confirm WHICH Glenn Hansen this is — a same-name LinkedIn profile ("In Power", Stillwater MN) is a different person, so **no handle may be invented**. Route must be resolved before send. **George's lane.**

> Subject: Enterprise AI seats — the list prices, with check dates
>
> Hi Glenn,
>
> You asked for enterprise-level costs on AI seats and tokens. Here is what the public list prices
> actually say, each with the date we checked it.
>
> Claude Team lists Standard seats at $20 per seat/month and Premium at $100 per seat/month, capped at
> 2–150 users (checked 2026-09-18). Google sells no standalone enterprise AI seat — Gemini is bundled
> into Workspace at $8.40/$7 per user/month for Business Starter, rising to $26.40/$22 for Business
> Plus on flexible against annual terms (checked 2026-09-18). GitHub Copilot Business is $19/user/month
> and Enterprise $39/user/month, each with a metered AI-credit allowance (checked 2026-10-01).
>
> Two things the list prices hide: the biggest tiers — ChatGPT Enterprise, Gemini Enterprise — publish
> no seat price at all and are sales-assisted, so the figure people quote is not the one being paid;
> and the annual term is where the real discount hides.
>
> Happy to hand over the full dated set, with a source and check date for every number.
>
> AIToolsEssentials
> https://aitoolessentials.com
>
> --

---

## 3. Shadow AI spend — employees paying out of pocket ◀ 21d, crossed cold 2026-09-28, unsent through NINETEEN runs

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **21 days.** Page re-read today: HTTP 200, badge "Posted 21 days ago".
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
> https://aitoolessentials.com
>
> --
