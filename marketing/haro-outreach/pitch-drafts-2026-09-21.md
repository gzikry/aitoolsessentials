# Pitch drafts — 2026-09-21

**Nothing here has been sent.** These are the three sendable requests in today's queue (see
`pitch-queue.md`) — the same three as the last three runs, re-verified against today's pages and
today's data rather than carried on trust. Each has now been written and unsent for 2–3 consecutive
runs. A draft is not progress; only the send is.

**What changed today — one figure was wrong and is corrected.**

Every draft written since 2026-09-18 cites the same-tier monthly-vs-annual range as
**1.21x to 2.53x, median 1.33x**. That range came from a regex-dependent pair set and **the floor is
wrong**. Re-deriving it four different ways over the same `data/pricing_snapshots.json` returned 2, 7,
9 and 18 pairs — the "range" was a property of the pattern, not of the data. Four same-tier per-month
pairs sit *below* 1.21x and were never in the set:

- instrumentl Pre-Award — **$579** monthly vs **$499**/month billed annually = **1.16x**
- instrumentl Discover — **$349** monthly vs **$299**/month annually = **1.17x**
- airtable-ai Team — **$24** monthly vs **$20**/seat/month billed annually = **1.20x**
- slack-ai Business+ — **$18** monthly vs **$15**/user/month annually = **1.20x**

**Correct figures, now locked:** 18 curated pairs, range **1.16x to 2.53x, median 1.25x**. Written to
`data/monthly_annual_pairs.json` and re-asserted sentence-by-sentence on every run by
`scripts/extract_monthly_annual_pairs.py`, so it cannot drift silently again. **The drafts below use
1.16x–2.53x.** The wrong floor was sent to Jan Suski on 2026-09-18; it is disclosed in the ledger
rather than left standing.

**Why these three.** They are the only rows in the queue that are live, not cold, ranked above the
tangential band, *and* have a resolved reply route a human can act on. The other 22 live rows are
off-beat calls (hospital billing, podcast guesting, a founders' profile slot) that the queue
documents as excluded. The queue now heads with this number instead of the old "16 live".

---

## 1. Shadow AI spend — employees paying out of pocket ◀ SEND THIS FIRST, day 4 unsent

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **4 days** (page badge today: "Posted in last 7 days")
**Who:** **Simon Chandler** — in the page's own author field. Covers enterprise tech for Raconteur and
TechRepublic; writes TechRepublic's Tech Insider Europe newsletter; ten years on technology with
bylines at Wired, Forbes, Digital Trends, Business Insider, Decrypt.
**Ask:** quotes from full-time employees who use AI without their employer's knowledge and pay for it
personally; anonymity offered.

**Why it is the best live request:** employees buying AI without approval and paying personally is
unbudgeted, unenumerated software spend — the quantity our dated price set exists to make visible.
Raconteur's own contact page asks for "pitches with exclusive business data", which is what we hold.
It is the only high-relevance request in the queue and the only core-beat find in eight runs.

**⚠ Honesty constraint — read before sending.** The request wants employees' personal accounts. We are
a publisher with no such account. The draft says so in its first line and offers price evidence
instead. Do not let anyone edit that line out.

**Reply route:** `simon.chandler@raconteur.net` — **re-resolved today.** The live page
**https://www.raconteur.net/contributors/simon-chandler** returns HTTP 200 (154,932 bytes) and still
carries `data-part1="simon.chandler" data-part2="raconteur" data-part3="net"`, which the site's JS
assembles at runtime. Control on the same run: `/contributors/tom-dennis` (HTTP 200) carries
`tom.dennis` `raconteur` `net`. `raconteur.net` MX re-checked today = Google Workspace
(`aspmx.l.google.com`). The byline URL cited on 2026-09-19 (`/author/simon-chandler/`) still 404s —
it is dead and must not be cited.
**George's lane. Not automatable.**

> Subject: Shadow AI spend — what the out-of-pocket tiers actually cost
>
> Hi Simon,
>
> Straight up front: I can't give you a personal account of paying for AI behind my employer's back.
> I run AIToolsEssentials, where we track verified pricing for 76 AI tools, and that's the half of
> this story I can quantify.
>
> What the out-of-pocket buyer is choosing between, from the vendors' own pricing pages:
>
> - 31 of the 76 tools have a cheapest paid tier at or under $25/month. Median $16.50. Lowest is
>   Khanmigo at $4/month (checked 2026-09-18).
> - Nearly all of them charge more if you pay monthly instead of annually. Across the 18 tiers we
>   hold both terms for, the gap runs 1.16x to 2.53x — Browse AI is $48/month against $19/month
>   billed annually (checked 2026-09-18). The buyer with no company card pays the top of that range.
>
> That's the shape of shadow spend: small enough to expense personally, expensive enough to matter
> over a year, and invisible to whoever holds the budget.
>
> Happy to hand over the full dated set if it's useful, and to name my source for every number.
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --
> We publish dated pricing evidence for AI tools and write about overlapping subscriptions and AI
> budget visibility. Reply "stop" and I won't follow up again.

**Figures:** 76 tools (`data/tools.json`, 76 records). 31 with a cheapest paid monthly tier ≤$25,
median $16.50, minimum $4 Khanmigo (2026-09-18) — computed from the `digest` text of
`data/pricing_snapshots.json`, each value carrying its own snapshot `date`. **18 same-tier
monthly-vs-annual pairs, 1.16x–2.53x** from `data/monthly_annual_pairs.json` (curated, sentence-asserted);
HeyGen $29 vs $24 is among the narrowest, Browse AI $48 vs $19 the widest. All pair dates 2026-09-18
and 2026-08-21. The old "1.21x floor / 1.33x median" is superseded.

---

## 2. Anthropic subscription value — price vs support ◀ day 9, ONE DAY FROM COLD

**Source:** https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
**Posted:** 2026-09-11 16:58 UTC — **9 days** (page badge today: "Posted 9 days ago")
**Who:** **Helen Li** — independent journalist, in the page's own author field.
**Ask:** users and business owners with Anthropic customer-service experiences; DMs, email or Signal.

**Fit:** on-beat as a subscription-value story, not a grievance. We hold dated official Anthropic
pricing and no complaint of our own, so the draft leads on price and claims no support failure.

**Reply route:** **Signal `hliwrites.99`** — re-read verbatim off the live request page today (page
body: "I'd love to chat via DMs, email, or Signal hliwrites.99"). Still the only concrete handle
published on any request page in the queue. DMs and email are also invited; the address is redacted on
Sourcee. **George's lane. Not automatable.**

**If this is not going out this run, record it as skipped in `pitch-ledger.json`.** At 9 days it is
one day short of the cold line, and it has been the queue's #2 for four consecutive runs.

> Signal/DM —
>
> Your story is a value story, not a service one, and there's a number under it. Anthropic's own
> published tiers run from $17/month for Pro (with a $200 annual prepayment, or $20 month-to-month)
> to $100/month for Max, and Team lists Standard seats at $20/seat/month up to Premium at
> $100/seat/month (checked 2026-09-18 against anthropic.com/pricing).
>
> At the top of that range a buyer is paying five figures a year per seat, and the support channel
> doesn't change between the $20 seat and the $100 one.
>
> I don't have a support failure to give you — I'd be inventing standing I don't have. What I can
> give you is the pricing side, dated and sourced to Anthropic's own page, plus the same map for
> the other assistants if it helps you draw the comparison.
>
> The question your readers ask last is the useful one: what exactly does the premium tier buy, if
> the way to reach support is the same at both prices?
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --
> We publish dated pricing evidence for AI tools and write about overlapping subscriptions and AI
> budget visibility. Reply "stop" and I won't follow up again.

**Figures:** Claude Pro $17/month with a $200 annual prepayment or $20 month-to-month; Max from
$100/month; Team Standard $20/seat/month and Premium $100/seat/month. All five from
`data/tool_sources.json` slug `claude` (`pricing_checked_date` 2026-09-18) — which carries the full
sentence. `data/pricing_snapshots.json` key `claude` truncates its 200-character `digest` mid-sentence
after "Standard seats at $20 per seat per month", so the verifier checks the Premium seat against
`tool_sources.json` rather than assuming the two files agree. "Five figures a year per seat" is
arithmetic on $100/seat/month — not a published number.

---

## 3. Speciality Food — a £10k tech budget ◀ fresh, reachable, weaker standing

**Source:** https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
**Posted:** 2026-09-17 16:05 UTC — **3 days** (page badge today: "Posted in last 7 days")
**Who:** **Holly Shackleton**, Content Editor, Speciality Food magazine.
**Ask:** for the October issue — a speciality food/drink business given £10k for EPOS, shelf labels,
ecommerce, stock and loyalty systems: how would you spend it?

**⚠ Standing constraint — read before sending.** She wants food and drink businesses. We are not one,
and our price set covers AI tools, not retail hardware. The draft's first line says so and offers the
pricing method as a benchmark. If a non-retailer benchmark is not useful to her, drop this rather than
rework it.

**Reply route:** `holly.shackleton@artichokehq.com` — re-read today off
`specialityfoodmagazine.com/contact` (HTTP 200, 59,500 bytes), listed "Content Editor Holly Shackleton"
alongside five other named staff addresses (`charlotte.smith-jarvis@`, `jessica.brett@`,
`louise.barnes@`, `sam.reubin@`, `subscriptions@`), so it is a published masthead rather than a
guessed pattern. `artichokehq.com` MX re-checked today = Microsoft 365
(`artichokehq-com.mail.protection.outlook.com`). **George's lane. Not automatable.**

> Subject: A £10k benchmark from dated prices, if a non-retailer's data is useful
>
> Hi Holly,
>
> I'm not a speciality food business, so I can't tell you how a retailer would spend £10k. What I
> can offer is a benchmark from the other side of the budget line: what a fixed sum actually buys at
> published prices, checked vendor by vendor.
>
> We track verified pricing for 76 software tools. Two numbers from it that bear on a £10k decision:
>
> - 40 of the 76 publish a non-zero monthly price, and 31 of those start at or under $25/month. The
>   median cheapest paid tier is $16.50 (checked 2026-09-18). A per-seat tool is a recurring cost, not
>   a one-off — the £10k is really a decision about the next 24 months.
> - Where vendors publish both terms, paying monthly instead of annually costs more for the same
>   tier — from 1.16x up to 2.53x across the 18 tiers we hold both terms for (checked 2026-09-18). On
>   stock management or loyalty software, the billing term moves the number more than the vendor
>   choice does.
>
> Full dated set available if useful, every figure traceable to its own page.
>
> AIToolsEssentials
> https://aitoolsessentials.com
>
> --
> We publish dated pricing evidence for software tools and write about overlapping subscriptions and
> budget visibility. Reply "stop" and I won't follow up again.

**Figures:** 40 of 76 with a non-zero monthly price, 31 of those ≤$25, median $16.50 — from
`data/pricing_snapshots.json`; 18 pairs, 1.16x–2.53x from `data/monthly_annual_pairs.json`.
Deliberately **no** £/$ conversion: our figures are USD and the request is in sterling, so the numbers
are offered as published.

---

## Requests deliberately NOT drafted

| Request | Why not |
|---|---|
| **FinOps — agentic AI cost overruns (14d, high, COLD)** | The highest-relevance request we have never answered, cold since two runs. A finished draft has existed since `pitch-drafts-2026-09-17.md` §1, route LinkedIn DM to `linkedin.com/in/niloy-ghosh`. Send it late or drop it — re-drafting a fifth time would be the fifth time we did nothing with it. |
| Founders cutting AI use (Forbes, 2d, medium-low) | The body is explicit: "Please only answer as a comment on this post. Do not email or DM me because they won't be used." It wants a named founder's own rationale on the record. We publish anonymously-signed and have no founder to put forward. |
| Early-stage founders — Built From Scratch (10d, medium) | Crosses the cold line today. A founder-profile slot with a public-comment route: earns standing, not a citation. |
| AI automation experts — speaking slots (4d) | A speaking-slot solicitation, not a journalist request. |
| Podcast guest calls (3 today: data-centre podcast, founders' Rational Exchange, an AI-bot guest prompt) | Booking solicitations, not reporter calls. The third is literally a public prompt to an AI connector bot. |
| Sales-enablement SaaS sourcing / PDF-workflow (2d, new) | #PROpportunity PR posts from the same account. They want a tool name and a founder quote in a category we do not cover. |
| ML researchers — continuous learning (new, 2d) | A researcher-to-researcher methods call. Nothing to do with spend. |
| Founders 55+ series (new, 2d) | Off-beat. |
| US hospital billing errors (new, 1d) | Matched our spend filter on the word "billing" but the subject is medical charges, not software. |
| The Lever — autonomous weapons survivors (1d) | Wants survivor testimony. Off-beat. |
| Over-50s adapting to AI (1d) | Workplace-culture piece, no cost angle. |
| AI alignment framework (2d) | Self-published framework discussion. |
| E-Discovery AI-assisted review (4d) | Wants practising e-discovery lawyers. Wrong standing. |
| Gen Z AI data annotators (Fortune, 4d) | Wants annotators describing their own work and pay. No standing. |
| Ecommerce marketers — AI recommendation transparency (4d) | Wants AEO case studies we do not have. |
| Cybersecurity companies & AI scams (5d) | A PR firm building a spokesperson roster. Off-beat and off-standing. |
| U.S. Founders — calls to slow AI development (Inc., 5d) | Wants founders' firsthand safety-guardrail accounts; address redacted with no route resolved. Wrong standing and unreachable. |
| EdTech LMS audit (8d, medium) | Genuinely adjacent ("follow the invoice") but the writer sources people inside EdTech; skipped 2026-09-15 on that basis and the judgement stands. |
| California AI audit bills → CIOs (11d) | Its own stated deadline — "speak with a source today" — passed 2026-09-12. |
| UK managers / Gen Z AI overuse (14d) | Internal deadline "by this Wednesday September 9" passed; cold. |
| Individual contributors managing AI agents (11d) | Pitched 2026-09-18 to Rani@Sherwood.news. No reply. |
| Amplemarket Growth/Elite (14d, high) | Pitched 2026-09-18; Jan Suski replied 2026-09-18 20:39Z and we answered 21:29Z. Live thread — do not re-pitch. |
| Enterprise AI Leaders — value creation (7d) | Pitched 2026-09-15 to hello@foxandspindle.com. No reply in six days. |

---

## Send log — what "sent" actually means here

Three pitches have ever gone out from this monitor: 2026-09-15 (Enterprise AI Leaders → Fox & Spindle),
2026-09-18 (Amplemarket → Market Intelligence Tools), 2026-09-18 (Sherwood News → Rani Molla). One
reply, answered the same day. **Pitches sent today: 0.** The three drafts above are all still unsent.

**Mailbox checked 2026-09-21:** no new replies. INBOX top is still Jan Suski's 2026-09-18 20:39Z
message, which we answered at 21:29Z. No reply to the 2026-09-15 send (six days) or the 2026-09-18
Sherwood send (three days). Spam holds three items, all delivery-failure bounces and directory
form-mail. Sent Mail top is unchanged at msg 178.
**A reply to the Amplemarket pitch is the only one this monitor has ever received.**

## The one thing blocking sends that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake (`hermes mcp add --auth oauth`) that
cannot be completed from a scheduled run. It is a free read-only feed covering Connectively, HARO, X,
LinkedIn, MentionMatch and Substack — six platforms in one step, and the only path to widening a
monitor whose sole accessible source produced **zero new AI-token requests** today (first time on
record). Endpoint re-confirmed live this run (HTTP 401, `invalid_token`), and `hermes mcp list` in this
profile still reports "No MCP servers configured."
