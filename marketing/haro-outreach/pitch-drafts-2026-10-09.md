# Pitch drafts — 2026-10-09

**Nothing here has been sent.** 107 tracked requests, **57 live unpitched, 1 sendable**
(`pitch-queue.md`).

**§1 is the sendable row** — the WSJ blocked-work-accounts request, now **4 days old**, still the only
row in the queue that is both above the tangential band and route-resolved. Its route was re-fetched
today (HTTP 200, 636,389 bytes, exact title match) rather than trusted from the digest.

**§2 is the best-matching request this monitor has ever held** — Google & Claude enterprise seat and
token costs, relevance **high**, 1 day old. It has **no reply route** (the page publishes no address
or handle), so it is not sendable until George resolves one. The data is ready; only the route is
missing. Second run carrying it.

**§3 carries the Raconteur shadow-AI draft** — 22 days old, unsent through **twenty** consecutive runs.
A twenty-first carry is the thing to avoid: send it late or record a `skipped` entry.

**§4 is the Speciality Food send-or-skip call** (21 days, October window closed) — republished with
freshly re-derived figures so a late send cannot go out with a superseded denominator; the alternative
is a `skipped` entry in `pitch-ledger.json`.

**Drafts deliberately NOT written this run:** nothing new was worth drafting. The 2026-10-09 sitemap
window produced 8 AI-token slugs and **zero** AI+spend slugs — the first clean window in four runs —
and all six added rows are low-relevance, route-less calls (sales-reps' personal stories with an
explicit anti-pitch instruction, a studio booking promo, voter experience, hospitality interviews, a
science-landscape study sign-up, FB Marketplace sellers). See `digest-2026-10-09.json` `new_this_run`.

**Figures re-derived today.** `data/pricing_snapshots.json` carries `updated: 2026-10-09` (77 snapshots,
up from 76); the set is **42 of 77 tools publishing a monthly price, 33 of those at or under $25/month,
median $17.50**, lowest $4.00 (Khanmigo, checked 2026-09-18). Re-derived by
`marketing/haro-outreach/_figures_1009.py` and asserted against the drafts by
`marketing/haro-outreach/_verify_drafts_1009.py`. The **denominator moved 76 → 77** and every draft
sentence reading "42 of 76" is superseded. The pair file was **not** rebuilt this run (its inputs were
rebuilt yesterday); range held: **1.11x to 2.53x, median 1.25x over 19 tiers**
(`data/monthly_annual_pairs.json`, built 2026-10-08).

---

## 1. Employees blocked from AI on work accounts — the workaround spend ◀ SENDABLE, 4d old, only sendable row

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **4 days.** Page re-read today: HTTP 200, live, badge "Posted in last 7 days".
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist (his own byline page confirms the title).
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work by hand.

**Why it fits:** the blocked employee is the enterprise mirror of this monitor's core shadow-AI request — locked out of the work account, they buy the tool personally, and that purchase is unbudgeted, unenumerated software spend. That is the quantity our dated price set exists to make visible.

**⚠ Honesty constraint — read before sending.** The request wants the respondent's own personal annoyance. We are a publisher, not a blocked employee. The draft says so in its opening line. Do not edit it out.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — verified today:
HTTP 200, 636,389 bytes, title "Christopher Mims - The Wall Street Journal | LinkedIn". The request's own
body says "(DMs open)". **George's lane. Not automatable.**
Dead ends recorded so they are not retried: muckrack.com/christopher-mims → HTTP 403; wsj.com/news/author/christopher-mims → HTTP 401.

> Subject: The blocked-work-account workaround, in dated prices
>
> Hi Christopher,
>
> Up front: I can't give you a personal account of being locked out of AI on a work account. What I can give you is what the people who route around that block pay.
>
> We track dated list prices for 77 AI tools. 42 publish a monthly price; 33 of those start at or under $25/month — median $17.50, lowest $4 (Khanmigo). Every figure carries the date we checked it.
>
> The workaround buyer almost always pays the worst rate. Across the 19 tiers where we hold both billing terms, paying monthly instead of annually costs 1.11x to 2.53x more — median 1.25x. Browse AI is $48/month against $19/month billed annually. One seat expensed personally sits at the top of that range with nobody to negotiate for it.
>
> Cheap enough to pay alone, expensive enough to add up over a year, invisible to whoever holds the budget.
>
> Happy to hand over the full dated set and name the source for every number.
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --

---

## 2. Google & Claude enterprise seats and token costs ◀ HIGH relevance, 1d old — BEST MATCH, NO ROUTE

**Source:** https://www.sourcee.app/journo-request/google-and-claude-enterprise-users-seats-and-token-costs
**Posted:** 2026-10-07 19:16 UTC — **1 day.** Page re-read today: HTTP 200, live, badge "Posted in last 7 days".
**Who:** **Glenn Hansen** — the page's own author field; the body says he reports on power-equipment manufacturing (lawnmowers, chainsaws). Outlet not named.
**Ask:** "enterprise-level costs for AI seats and tokens. Google or Claude users care to enlighten me?"

**Why it matters:** this is the exact quantity our dated price set measures, and the only core-beat AI+spend request this monitor has produced in fifteen runs. The three facts below are all in `data/tool_sources.json` with their own check dates.

**⚠ Standing constraint.** We are a publisher, not an enterprise buyer running Google/Claude seats at scale. The draft claims only what our dated records show.

**⚠ Route unresolved — do not send blind.** The page publishes **no address, handle or link** and gives no reply instruction (verified today: `email_redacted=False` but `emails_on_page=none`, published links = Sourcee chrome only). A web search cannot confirm WHICH Glenn Hansen this is — a same-name LinkedIn profile ("In Power", Stillwater MN) is a different person, so **no handle may be invented**. Route must be resolved before send. **George's lane. Not automatable.**

> Subject: Enterprise AI seats — the list prices, with check dates
>
> Hi Glenn,
>
> You asked for enterprise-level costs on AI seats and tokens. Here is what the public list prices actually say, each with the date we checked it.
>
> Claude Team lists Standard seats at $20 per seat/month and Premium at $100 per seat/month, capped at 2–150 users (checked 2026-09-18). Google sells no standalone enterprise AI seat — Gemini is bundled into Workspace at $8.40/$7 per user/month for Business Starter, rising to $26.40/$22 for Business Plus on flexible against annual terms (checked 2026-09-18). GitHub Copilot Business is $19/user/month and Enterprise $39/user/month, each with a metered AI-credit allowance (checked 2026-10-01).
>
> Two things the list prices hide: the biggest tiers — ChatGPT Enterprise, Gemini Enterprise — publish no seat price at all and are sales-assisted, so the figure people quote is not the one being paid; and the annual term is where the real discount sits.
>
> Happy to hand over the full dated set, with a source and check date for every number.
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --

---

## 3. Shadow AI spend — employees paying out of pocket ◀ 22d, crossed cold 2026-09-28, unsent through TWENTY runs

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **22 days.** Page re-read today: HTTP 200, badge "Posted 22 days ago".
**Who:** **Simon Chandler** — the page's own author field; covers enterprise tech for Raconteur.
**Ask:** quotes from full-time employees who use AI without their employer's knowledge and pay personally.

**Why it is still worth sending late:** identical ground to §1 — employees buying AI unapproved and paying personally is unbudgeted software spend. Raconteur's contact page asks for "pitches with exclusive business data", which is what we hold. It remains the only **high**-relevance request this monitor has ever produced with a resolved route.

**⚠ Honesty constraint — read before sending.** The same one as §1: the request wants employees' personal accounts and we are a publisher with none. Do not edit that line out.

**Reply route:** `simon.chandler@raconteur.net` — re-resolved today off the live
`raconteur.net/contributors/simon-chandler` (HTTP 200, 154,984 bytes; data-part1/2/3 = simon.chandler + raconteur + net; control `/contributors/tom-dennis` HTTP 200 carries tom.dennis + raconteur + net). The older `/author/simon-chandler/` still 404s and must not be cited. **George's lane. Not automatable** — the address is assembled from the byline page's JS triplet, not published in the request body.

> Subject: Shadow AI spend — what the out-of-pocket tiers actually cost
>
> Hi Simon,
>
> Straight up front: I can't give you a personal account of paying for AI behind my employer's back. What I can give you is what those out-of-pocket buyers are actually paying.
>
> We track dated pricing for 77 AI tools. 42 publish a monthly price; 33 of those start at or under $25/month — median $17.50, lowest $4 (Khanmigo). Every number carries its check date.
>
> Nearly all charge more if you pay monthly instead of annually. Across the 19 tiers where we hold both terms, the gap runs 1.11x to 2.53x, median 1.25x. Browse AI is $48/month against $19/month billed annually. The buyer with no company card pays the top of that range.
>
> That's the shape of shadow spend: small enough to expense personally, expensive enough to matter over a year, and invisible to whoever holds the budget.
>
> Happy to hand over the full dated set, and to name my source for every number.
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --

---

## Carried items NOT drafted again

| Request | Status |
|---|---|
| **Speciality Food — a £10k tech budget (21d, cold, October window closed)** | Republished at §4 above with freshly re-derived figures; route `holly.shackleton@artichokehq.com` (re-read today off `specialityfoodmagazine.com/contact`, HTTP 200, 59,488 bytes). **Send-or-skip call:** send late or record the skip in `pitch-ledger.json`. |
| **The Jan Suski figures correction (21 days outstanding)** | Reply to `jan@jansuski.com`, In-Reply-To the existing thread. The 2026-09-18 reply told him the range was "1.21x-2.53x, median 1.33x"; the current verified figure is **1.11x-2.53x, median 1.25x over 19 tiers**. Draft text at `pitch-drafts-2026-10-05.md` §3 — do not redraft, send. |
| **Google & Claude enterprise seats and tokens — Glenn Hansen (1d, high, NO ROUTE)** | Draft at §2 above; blocked on route resolution. |
| **Anthropic customer service (33d, cold)** | Crossed 2026-09-23. Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal `hliwrites.99`. Send late or mark skipped. |
| **FinOps — agentic AI cost overruns (32d, high, cold)** | The highest-relevance request we have never answered. Draft since `pitch-drafts-2026-09-17.md` §1, route LinkedIn DM to `linkedin.com/in/niloy-ghosh`. Send late or drop; do not redraft. |
| **The six new low-relevance rows added today** | Recorded in `digest-2026-10-09.json`; none drafted. No spend angle, no usable route. The sales-reps row is the only one where replying would break the journalist's own stated rule ("you will be placed on the naughty list"). |

---

## 4. Speciality Food — a £10k tech budget ◀ 21d, cold, October window closed — SEND OR SKIP

**Source:** https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
**Posted:** 2026-09-17 16:05 UTC — **21 days.** Page re-read today: HTTP 200, badge "Posted 21 days ago".
**Who:** **Holly Shackleton**, Content Editor, Speciality Food magazine.
**Ask:** for the October issue — a speciality food/drink business given £10k for EPOS, shelf labels, ecommerce, stock and loyalty systems: how would you spend it?

**⚠ Standing constraint.** She wants food and drink businesses. We are not one, and our price set covers AI tools, not retail hardware. The draft's first line says so. **The October issue is the reason to decide rather than carry again: if it is laid out, the honest move is a `skipped` entry in `pitch-ledger.json` rather than a late benchmark into a closed issue.** This body has now been carried in seventeen draft files; the figures below are re-derived so a late send would not go out with a superseded denominator.

**Reply route:** `holly.shackleton@artichokehq.com` — re-read today off `specialityfoodmagazine.com/contact` (HTTP 200, 59,488 bytes, alongside five other named masthead addresses). **George's lane. Not automatable.**

> Subject: A £10k benchmark from dated prices, if a non-retailer's data is useful
>
> Hi Holly,
>
> I'm not a speciality food business, so I can't tell you how a retailer would spend £10k. I can offer you one thing retailers rarely put side by side: of the 77 software tools we track, 42 publish a monthly price, 33 of those start at or under $25/month, and the median cheapest paid tier is $17.50 (checked 2026-10-09).
>
> A per-seat tool is recurring, not one-off — so the £10k is a decision about the next 24 months, not one purchase.
>
> The second number bears directly on it: where a vendor publishes both terms, paying monthly instead of annually costs more for the same tier — from 1.11x up to 2.53x across the 19 tiers we hold both terms for. On stock management or loyalty software, the billing term moves the number more than the vendor choice does.
>
> Full dated set available if useful, every figure traceable to its own page.
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --

**Figures:** 77 tools, 42 with a non-zero monthly price, 33 of those ≤$25, median $17.50, 19 tiers at 1.11x–2.53x — recomputed today from `data/pricing_snapshots.json` (`updated: 2026-10-09`) and `data/monthly_annual_pairs.json`. Deliberately **no** £/$ conversion: our figures are USD and the request is in sterling, so the numbers are offered as published.

---

## Reply status — checked this run

**Mailbox checked 2026-10-09** (`himalaya`). **No reply to any tracked pitch.** A search of All Mail
for the four tracked-pitch recipients (`jansuski`, `foxandspindle`, `sherwood`,
`marketintelligencetools`) returns exactly **one** inbound message ever: Jan Suski's 2026-09-18 20:39Z
reply (msg 234). **No reply to the 2026-09-15 Enterprise AI Leaders send (twenty-four days) or the
2026-09-18 Sherwood News send (twenty-one days).** INBOX top is msg 104 (Anike Tobechukwu,
2026-10-08, on the separate AIDetector.cx affiliate thread); next is msg 102 (a ToolChase reply to the
Sep-3 guest-pitch batch — not this monitor).

**Pitches sent today: 0.**

---

## The one thing blocking a send that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake that cannot be completed from a
scheduled run. It is a free read-only feed covering Connectively, HARO, X, LinkedIn, MentionMatch and
Substack — six platforms in one step, and the only path to widening a monitor whose single accessible
source produced **zero core-beat finds and zero AI+spend slugs** in today's 105-slug window. Endpoint
re-confirmed today (HTTP 401, 74 bytes — answers and refuses without credentials).

**The structural consequence, stated plainly:** `_sendable()` is 1, and that 1 has now been carried by
eight consecutive runs without a send. Every other live row is off-beat or comment-only, and none
carries a resolved route. No new on-beat supply is arriving from Sourcee. Until the handshake is done
or one of the crossed drafts is sent late, the next run of this monitor produces the same result.
