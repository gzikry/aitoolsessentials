# Pitch drafts — 2026-10-05

**Nothing here has been sent.** 74 tracked requests, **27 live unpitched, 0 sendable**
(`pitch-queue.md`). A row is sendable only with a relevance above the tangential band **and** a
resolved reply route; no row in the live set has both today. Every live row is an off-beat call with
no usable route for us — a game-dev attribution call, a law/fashion podcast booking, an MLS-data-risk
call, a real-estate brochure-switch call, a Miami conference call, a CNBC billable-hour call, a CIPD
HR-practice call, plus the carried set of teacher/seller/testimony calls. The two rows that do carry a
resolved route are the two crossed drafts below, both still live (HTTP 200) and still sendable late.

**Figures re-derived today and unchanged from 2026-10-02.** The snapshot refresh
(`data/pricing_snapshots.json`, `updated: 2026-10-05`) leaves the set at **42 of 76 tools publishing a
monthly price, 33 of those at or under $25/month, median $17.50**. The July 40/31/$16.50 set is
superseded; the 1.16x and 1.21x floors are superseded. Re-derived by
`scripts/haro-outreach/_figures_1005.py`; the 19-pair range re-asserted clean by
`scripts/extract_monthly_annual_pairs.py` (exit 0, no needle failures).

**Reply routes re-resolved today, both live:** `simon.chandler@raconteur.net` off
`raconteur.net/contributors/simon-chandler` (HTTP 200, 154,819 bytes, `data-part1/2/3` =
simon.chandler + raconteur + net; control `/contributors/tom-dennis` HTTP 200 carries
tom.dennis/raconteur/net; legacy `/author/simon-chandler/` still **404** and must not be cited), and
`holly.shackleton@artichokehq.com` off `specialityfoodmagazine.com/contact` (HTTP 200, 59,488 bytes,
alongside five other named masthead addresses).

---

## 1. Shadow AI spend — employees paying out of pocket ◀ 18d, crossed cold 2026-09-28, unsent through SIXTEEN runs (carried in 15 draft files, measured)

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **18 days**. Badge re-read off the live page today: "Posted 18 days
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
Khanmigo (checked 2026-09-18) — from `data/pricing_snapshots.json` `updated: 2026-10-05`. **19
same-tier monthly-vs-annual pairs across 14 tools, 1.11x–2.53x, median 1.25x** from
`data/monthly_annual_pairs.json` (`built: 2026-10-02`, re-asserted clean today by
`scripts/extract_monthly_annual_pairs.py`, exit 0).

---

## 2. Speciality Food — a £10k tech budget ◀ 17d, crossed cold 2026-09-28 — **send or skip** (carried in 15 draft files, measured)

**Source:** https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
**Posted:** 2026-09-17 16:05 UTC — **17 days**. Badge re-read off the live page today: "Posted 17 days
ago". **Crossed the cold line on 2026-09-28, and its October issue window has closed.**
**Who:** **Holly Shackleton**, Content Editor, Speciality Food magazine.
**Ask:** for the October issue — a speciality food/drink business given £10k for EPOS, shelf labels,
ecommerce, stock and loyalty systems: how would you spend it?

**⚠ Standing constraint.** She wants food and drink businesses. We are not one, and our price set
covers AI tools, not retail hardware. The draft's first line says so. **The October issue is the
reason to reconsider: if it is laid out, the honest move is to record a skip in `pitch-ledger.json`
rather than send a late benchmark into a closed issue.** This is the ninth run this draft has been
carried; a tenth is the thing to avoid.

**Reply route:** `holly.shackleton@artichokehq.com` — re-read today off the masthead contact page (see
header). **George's lane. Not automatable.**

> Subject: A £10k benchmark from dated prices, if a non-retailer's data is useful
>
> Hi Holly,
>
> I'm not a speciality food business, so I can't tell you how a retailer would spend £10k. I can offer
> you one thing retailers rarely put side by side: of the 76 software tools we track, 42 publish a
> monthly price, 33 of those start at or under $25/month, and the median cheapest paid tier is $17.50
> (checked 2026-10-05).
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
1.11x–2.53x — recomputed today from `data/pricing_snapshots.json` (`updated: 2026-10-05`) and
`data/monthly_annual_pairs.json`. Deliberately **no** £/$ conversion: our figures are USD and the
request is in sterling, so the numbers are offered as published.

---

## 3. The other sendable item on this page is not a pitch

**A correction is owed to Jan Suski, now SEVENTEEN days outstanding.** He replied to our 2026-09-18
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
| **The seven NEW AI-token finds added to tracking today** | All seven recorded in `digest-2026-10-05.json`, none drafted. Game-dev attribution call, law/fashion podcast booking, MLS-data-risk call, real-estate brochure-switch call, Miami conference call, CNBC law-firm billable-hour call, CIPD HR-practice call. None asks a price, seat, licence or software-spend question, and none has a route we can use. |
| **CNBC — law firm lawyers, billable hour (3d, low-medium)** | The closest new row to our beat: it asks what AI is doing to the billable hour. But it wants a practising lawyer's own firm-level implementation — we are not a law firm — and the body address is Sourcee-redacted with no alternative: `cnbc.com/lindsay-dodgson/` and `/author/lindsay-dodgson/` both return **HTTP 404**. Drafting it would claim standing we do not have. |
| **Nothing new core-beat this window** | 157 slugs in the window, 7 AI-token, **1** strict AI+spend regex hit, 10 spend-token. The single strict hit is `billing` in the CNBC law-firm slug — a billable-hour ask, **not** a software-spend ask. All 16 candidates fetched and read in full. |
| **The nine spend-token slugs** | Food creators (creator payment), homebuilder price cuts, gated-content SaaS vendor (we are not a vendor), indie-maker product stories, curls hair-care costs, debt repayment, NJ cost strain, NJ health costs, savers renting-vs-buying. They matched on 'costs', 'spend', 'paid'. |
| **CIPD — HR leaders, cognitive offloading (3d, low)** | Asks HR leaders for business-contextualised examples of staff AI guidance. No spend angle, no route: `cipd.org/uk/about/people/katie-jacobs/` and the contact page both return **HTTP 404**. |
| **Video Game Developer — falsely accused (1d, low)** | The freshest live row, and it does publish a Signal handle (`kerrblimey.43`) — but it wants a game developer's own accusation experience, and we hold no such standing. No spend angle. |
| **The 3 rows that crossed cold since 2026-10-02** | All `low`, none ever sendable, none with a route: ai-hardware-makers-3d-printing, engineering-managers-measuring-engineers, saas-tools-for-gated-content Q4 roundup. |
| **Anthropic — customer service (23d, cold)** | Crossed 2026-09-23. Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal `hliwrites.99` (still verbatim on the live page). Send late or mark skipped. |
| **FinOps — agentic AI cost overruns (28d, high, cold)** | The highest-relevance request we have never answered. Draft since `pitch-drafts-2026-09-17.md` §1, route LinkedIn DM to `linkedin.com/in/niloy-ghosh`. Send it late or drop it — do not redraft. |
| **Business & Technology Leaders (76d) / AI SaaS users in production (136d) / Enterprise AI Leaders agent sprawl (30d) / Scientists paying for AI subscriptions (30d) / MSP experts (202d) / SMEs AI ops (209d)** | The oldest rows still marked `high`/`medium` and never pitched. Recorded so the loss stays visible. |
| **All other live rows (27 live minus the two drafted)** | Off-beat calls — podcast guesting, teacher/seller testimony, ML methods, alignment philosophy, AI-hardware makers, hospital billing, insurance agents (comment-only), and today's seven. Listed in `pitch-queue.md` under "Live but not sendable". |

---

## Reply status — checked this run

**Mailbox checked 2026-10-05** (`himalaya`). **No reply to any tracked pitch.** INBOX top is msg 91
(a tool submission, 2026-10-05 12:39Z). The most recent human message on a **tracked** pitch remains
**Jan Suski's 2026-09-18 20:39Z reply**. **No reply to the 2026-09-15 Enterprise AI Leaders send
(twenty days) or the 2026-09-18 Sherwood News send (seventeen days).** Spam holds only two 2026-09-12
delivery-failure notices. Sent Mail's top is msg 201 (2026-10-05 13:39Z, a tool-submission
verification note) — **no pitch has gone out.**

**Pitches sent today: 0.**

---

## The one thing blocking a send that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake that cannot be completed from a
scheduled run. It is a free read-only feed covering Connectively, HARO, X, LinkedIn, MentionMatch and
Substack — six platforms in one step, and the only path to widening a monitor whose single accessible
source has now produced **no real AI+spend slug on eleven consecutive runs**. Endpoint re-confirmed
today (HTTP 401, 74 bytes — answers and refuses without credentials).

**The structural consequence, stated plainly:** `_sendable()` is 0, and today it is 0 for the correct
reason — every live row is off-beat or comment-only and none carries a resolved route. No new on-beat
supply is arriving from Sourcee. Until the handshake is done or one of the two crossed drafts is sent
late, the next run of this monitor produces the same zero.
