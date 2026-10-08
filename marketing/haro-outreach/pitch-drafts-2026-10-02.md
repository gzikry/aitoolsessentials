# Pitch drafts — 2026-10-02

**Nothing here has been sent.** 67 tracked requests, **23 live unpitched, 0 sendable**
(`pitch-queue.md`). A row is sendable only with a relevance above the tangential band **and** a
resolved reply route; no row in the live set has both today. The live rows are off-beat calls with
no usable route (podcast bookings, teacher/seller testimony, a paid-placement query, an FB
Marketplace call). The two rows that do carry a resolved route are the two crossed drafts below.

**⚠ THE HEADLINE FIGURES MOVED TODAY.** The snapshot refresh (`data/pricing_snapshots.json`,
`updated: 2026-10-02`) took the monthly-priced count from 40 to **42**, the sub-$25 count from 31 to
**33**, and the median cheapest paid tier from $16.50 to **$17.50**. Every draft dated before today
cites the superseded 40/31/$16.50 set against `updated: 2026-10-01` and must not be reused.
Re-derived today by `scripts/haro-outreach/_figures_1002.py`. The 77-tool count and the 19-pair range
are unchanged.

**Reply routes re-resolved today, both live:** `simon.chandler@raconteur.net` off
`raconteur.net/contributors/simon-chandler` (HTTP 200, 154,819 bytes, `data-part1/2/3` =
simon.chandler + raconteur + net; control `/contributors/tom-dennis` HTTP 200 carries
tom.dennis/raconteur/net; legacy `/author/simon-chandler/` still **404** and must not be cited), and
`holly.shackleton@artichokehq.com` off `specialityfoodmagazine.com/contact` (HTTP 200, 59,500 bytes,
alongside five other named masthead addresses).

---

## 1. Shadow AI spend — employees paying out of pocket ◀ 15d, crossed cold 2026-09-28, unsent through FIFTEEN runs

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **15 days**. Badge re-read off the live page today: "Posted 15 days
ago". **Crossed the cold line on 2026-09-28.**
**Who:** **Simon Chandler** — named in the page's own author field; covers enterprise tech for Raconteur.
**Ask:** quotes from full-time employees who use AI without their employer's knowledge and pay for it
personally. Anonymity offered.

**Why it is still worth sending late:** employees buying AI without approval and paying personally is
unbudgeted, unenumerated software spend — the quantity our dated price set exists to make visible.
Raconteur's own contact page asks for "pitches with exclusive business data", which is what we hold.
It remains the only high-relevance request this monitor has ever produced with a resolved route.

**⚠ Honesty constraint — read before sending.** The request wants employees' personal accounts. We are
a publisher with no such account. The draft says so in its opening line. Do not edit that line out.

**Reply route:** `simon.chandler@raconteur.net` — re-resolved today (see header).
**George's lane. Not automatable** — the address is reconstructed from the byline page's JS triplet,
not published in the request body, so it is sent by hand.

> Subject: Shadow AI spend — what the out-of-pocket tiers actually cost
>
> Hi Simon,
>
> Straight up front: I can't give you a personal account of paying for AI behind my employer's back.
> What I can give you is what those out-of-pocket buyers are actually paying.
>
> We track dated pricing for 76 AI tools. 42 publish a monthly price; 33 of those start at or under
> $25/month — median $17.50, lowest $4 (Khanmigo, checked 2026-09-18).
>
> Nearly all charge more if you pay monthly instead of annually. Across the 19 tiers where we hold
> both terms, the gap runs 1.11x to 2.53x (checked 2026-09-18 and 2026-09-21). Browse AI is $48/month
> against $19/month billed annually. The buyer with no company card pays the top of that range.
>
> That's the shape of shadow spend: small enough to expense personally, expensive enough to matter
> over a year, and invisible to whoever holds the budget.
>
> Happy to hand over the full dated set, and to name my source for every number.
>
> AIToolsEssentials
> https://aitoolessentials.com
>
> --
> We publish dated pricing evidence for AI tools and write about overlapping subscriptions and AI
> budget visibility. Reply "stop" and I won't follow up again.

**Figures (all re-derived today):** 76 tools (`data/tools.json` and `data/pricing_snapshots.json`,
both 76 records). 42 with a non-zero monthly price, 33 of those ≤$25, median **$17.50**, minimum $4
Khanmigo (checked 2026-09-18) — from `data/pricing_snapshots.json` `updated: 2026-10-02`. **19
same-tier monthly-vs-annual pairs across 14 tools, 1.11x–2.53x, median 1.25x** from
`data/monthly_annual_pairs.json` (`built: 2026-10-02`, re-asserted clean by
`scripts/extract_monthly_annual_pairs.py`, exit 0). The 1.21x and 1.16x floors are superseded.

---

## 2. Speciality Food — a £10k tech budget ◀ 14d, crossed cold 2026-09-28 — **send or skip**

**Source:** https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
**Posted:** 2026-09-17 16:05 UTC — **14 days**. Badge re-read off the live page today: "Posted 14 days
ago". **Crossed the cold line on 2026-09-28, and its October issue window has closed.**
**Who:** **Holly Shackleton**, Content Editor, Speciality Food magazine.
**Ask:** for the October issue — a speciality food/drink business given £10k for EPOS, shelf labels,
ecommerce, stock and loyalty systems: how would you spend it?

**⚠ Standing constraint.** She wants food and drink businesses. We are not one, and our price set
covers AI tools, not retail hardware. The draft's first line says so. **The October issue is the
reason to reconsider: if it is laid out, the honest move is to record a skip in `pitch-ledger.json`
rather than send a late benchmark into a closed issue.** This is the eighth run this draft has been
carried; a ninth is the thing to avoid.

**Reply route:** `holly.shackleton@artichokehq.com` — re-read today off the masthead contact page (see
header). **George's lane. Not automatable.**

> Subject: A £10k benchmark from dated prices, if a non-retailer's data is useful
>
> Hi Holly,
>
> I'm not a speciality food business, so I can't tell you how a retailer would spend £10k. I can offer
> you one thing retailers rarely put side by side: of the 76 software tools we track, 42 publish a
> monthly price, 33 of those start at or under $25/month, and the median cheapest paid tier is $17.50
> (checked 2026-10-02).
>
> A per-seat tool is recurring, not one-off — so the £10k is a decision about the next 24 months, not
> one purchase.
>
> The second number bears directly on it: where a vendor publishes both terms, paying monthly instead
> of annually costs more for the same tier — from 1.11x up to 2.53x across the 19 tiers we hold both
> terms for (checked 2026-09-18 and 2026-09-21). On stock management or loyalty software, the billing
> term moves the number more than the vendor choice does.
>
> Full dated set available if useful, every figure traceable to its own page.
>
> AIToolsEssentials
> https://aitoolessentials.com
>
> --
> We publish dated pricing evidence for software tools and write about overlapping subscriptions and
> budget visibility. Reply "stop" and I won't follow up again.

**Figures:** 76 tools, 42 with a non-zero monthly price, 33 of those ≤$25, median $17.50, 19 tiers at
1.11x–2.53x — recomputed today from `data/pricing_snapshots.json` (`updated: 2026-10-02`) and
`data/monthly_annual_pairs.json`. Deliberately **no** £/$ conversion: our figures are USD and the
request is in sterling, so the numbers are offered as published.

---

## 3. The other sendable item on this page is not a pitch

**A correction is owed to Jan Suski, now fourteen days outstanding.** He replied to our 2026-09-18
Amplemarket pitch on 2026-09-18 20:39Z; our reply the same day told him the same-tier monthly/annual
range is "1.21x-2.53x, median 1.33x". That figure was wrong when sent and has been superseded twice
since. **The current verified figure is 1.11x–2.53x, median 1.25x over 19 tiers.** An un-flagged wrong
number in a live peer method discussion is worse than a follow-up.

> Subject: Re: The Amplemarket list-vs-real gap, with dated numbers
>
> Jan — one correction I owe you, on a number I sent you on 18 September.
>
> I told you the same-tier monthly/annual range was 1.21x-2.53x, median 1.33x. That was wrong, and it
> was my error, not a change in the data. The pair population behind it was defined by a regex rather
> than curated, so it mixed tiers. Re-derived from a hand-checked set:
>
> — 19 tiers across 14 tools where the same tier quotes both a monthly price and an annual-billed
> monthly price:
> — range 1.11x to 2.53x, median 1.25x (checked 2026-09-18 and 2026-09-21).
>
> The direction is unchanged and the point stands — the monthly payer always pays more — but the floor
> is 1.11x, not 1.21x, and I'd rather you had the right figure than the one that flattered the claim.
> The set is the same one I offered you, and every pair traces to its own vendor page with its own
> checked date.
>
> AIToolsEssentials
> https://aitoolessentials.com

**Route:** reply to `jan@jansuski.com`, In-Reply-To the existing thread (msg 77 in the mailbox).
**George's lane. Not automatable.**

---

## Requests deliberately NOT drafted

| Request | Why not |
|---|---|
| **The seven NEW AI-token finds added to tracking today** | All seven recorded in `digest-2026-10-02.json`, none drafted. Creator story-project (solicits stories + sponsors), newsletter-aggregation practice call, Scottish-teacher call, FB Marketplace seller call, teachers' moratorium call, AI Summit Barcelona controversy call, AI-glasses (India) product call. None asks a price, seat, licence or software-spend question. |
| **Nothing new core-beat this window** | 91 slugs in the window, 7 AI-token, 0 AI+spend (tenth consecutive run with none), 8 spend-token. All 15 candidates fetched and read in full. |
| **The 8 spend-token slugs** | Harlem landlords / rent freeze, Alaska residents' living costs, Canada childcare costs, the i Paper Autumn Budget, the i Paper savers, cost of digital disconnection, consumer product spending (mattress/walking-pad/robot vacuum), UK SME winter pressures. They matched on 'costs', 'budget', 'spend'. |
| **Employees Conflicted About AI Use (1d, low-medium)** | Nearest thing to our beat in the live set: "no formal policies around AI use" is the shadow-AI problem. But it wants employees' own conflicted testimony for a video project, and its only published link is a `docs.google.com` casting form — **not** a reply route. Drafting it would claim standing we do not have. |
| **The 5 rows that crossed cold today** | All `low`, none ever sendable, none with a route: founders-and-leaders-mindsets-and-milestones, sales-enablement-saas-tools (PR solicitation), creative-industry-professionals-podcast, former-ai-skeptics-changed-views, london-businesses-stopped-using-ai-hiring-tools. Second consecutive day of a mass crossing. |
| **The 3 rows at exactly 10d, crossing tomorrow** | ai-hardware-makers, engineering-managers-measuring-engineers, saas-tools-for-gated-content Q4 roundup. All `low`, none sendable. |
| **Anthropic — customer service (20d, cold)** | Crossed 2026-09-23. Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal `hliwrites.99` (still verbatim on the live page). Send late or mark skipped. |
| **FinOps — agentic AI cost overruns (25d, high, cold)** | The highest-relevance request we have never answered. Draft since `pitch-drafts-2026-09-17.md` §1, route LinkedIn DM to `linkedin.com/in/niloy-ghosh`. Send it late or drop it — do not redraft. |
| **Business & Technology Leaders (73d) / AI SaaS users in production (133d) / Enterprise AI Leaders agent sprawl (27d) / Scientists paying for AI subscriptions (27d) / MSP experts (199d) / SMEs AI ops (206d)** | The oldest rows still marked `high`/`medium` and never pitched. Recorded so the loss stays visible. |
| **All other live rows (23 live minus the two drafted)** | Off-beat calls — podcast guesting, teacher/seller testimony, ML methods, alignment philosophy, AI-hardware makers, hospital billing, insurance agents (comment-only), and today's seven. Listed in `pitch-queue.md` under "Live but not sendable". |

---

## Reply status — checked this run

**Mailbox checked 2026-10-02** (`himalaya`). **No reply to any tracked pitch, and no new inbound at
all.** The newest inbound is still **msg 84, Lilach Bullock (2026-09-29 18:09+03:00)** — **not** a
tracked-pitch reply: a reply to the subscription-creep resource pitch offering a **$300 paid product
placement**, already **answered and declined the same day** under editorial independence (Sent msg
**189**, 2026-09-29, in-thread, signed AIToolsEssentials, no personal name).

The most recent human message on a **tracked** pitch remains **Jan Suski's 2026-09-18 20:39Z reply**.
**No reply to the 2026-09-15 Enterprise AI Leaders send (seventeen days) or the 2026-09-18 Sherwood
News send (fourteen days).** Sent Mail's top is still msg 189 — **no send has gone out since
2026-09-29.**

**Pitches sent today: 0.**

---

## The one thing blocking a send that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake that cannot be completed from a
scheduled run. It is a free read-only feed covering Connectively, HARO, X, LinkedIn, MentionMatch and
Substack — six platforms in one step, and the only path to widening a monitor whose single accessible
source has now produced **no real AI+spend slug on ten consecutive runs**. Endpoint re-confirmed
today (HTTP 401, 74 bytes — answers and refuses without credentials).

**The structural consequence, stated plainly:** `_sendable()` is 0, and today it is 0 for the correct
reason — every live row is off-beat or comment-only and none carries a resolved route. No new on-beat
supply is arriving from Sourcee. Until the handshake is done or one of the two crossed drafts is sent
late, the next run of this monitor produces the same zero.
