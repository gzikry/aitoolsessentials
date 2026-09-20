# Pitch drafts — 2026-09-20

**Nothing here has been sent.** These are the same three requests as `pitch-drafts-2026-09-19.md`,
re-verified against today's pages and today's data rather than carried on trust. Two of the three
have now had a finished draft sitting unsent for 24 hours and one for 72. A draft is not progress.

**What changed today:** nothing in the drafts needed an edit — every route still resolves and every
figure still computes. What *did* change is the citation for the Raconteur route: the byline URL the
2026-09-19 digest named (`/author/simon-chandler/`) now 404s, and the live page is
`/contributors/simon-chandler`. Same address, different URL. Detail in draft 1.

**Why these three.** Ranked by the queue (`pitch-queue.md`, rebuilt today): draft 1 is the only
high-relevance request in the queue and the only core-beat find in seven runs. Draft 2 is
medium-high with the only direct channel published on any request page. Draft 3 is the freshest
request in the queue (2 days) with a verified named-author address. Nothing ranked below them has
both a resolved route and standing.

**Figures** were recomputed today by `_figures_0919.py` against `data/tools.json`,
`data/pricing_snapshots.json` and `data/tool_sources.json` as they stand at the 2026-09-20 build
(`pricing_snapshots.json` `updated` = 2026-09-20; the file's data rows are unchanged since 2026-09-18,
only a version note and the `updated` field moved). `_verify_drafts_0920.py` asserts every number
against the file that actually holds it. The 2026-09-15 pitch went out citing a count that had
drifted; the 2026-09-18 one cited two claims that were simply wrong. Neither error is repeated.

---

## 1. Shadow AI spend — employees paying out of pocket ◀ send this first, day 3 unsent

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **3 days** (page badge today: "Posted in last 7 days")
**Who:** **Simon Chandler** — in the page's own author field. Covers enterprise tech for Raconteur and
TechRepublic; writes TechRepublic's Tech Insider Europe newsletter; ten years on technology with
bylines at Wired, Forbes, Digital Trends, Business Insider, Decrypt.
**Ask:** quotes from full-time employees who use AI without their employer's knowledge and pay for it
personally; anonymity offered.

**Why it is the best live request:** employees buying AI without approval and paying personally is
unbudgeted, unenumerated software spend — the quantity our dated price set exists to make visible.
Raconteur's own contact page asks for "pitches with exclusive business data", which is what we hold.

**⚠ Honesty constraint — read before sending.** The request wants employees' personal accounts. We are
a publisher with no such account. The draft says so in its first line and offers price evidence
instead. Do not let anyone edit that line out.

**Reply route:** `simon.chandler@raconteur.net` — **re-resolved today.** The 2026-09-19 digest cited
`https://www.raconteur.net/author/simon-chandler/`, which now returns HTTP 404 (139,404 bytes,
Raconteur's own 404 shell); `/author/ian-deering/`, the cross-check URL, also 404s. Raconteur's
`author-sitemap.xml` (HTTP 200, 1,000 locs) still lists him at
`/contributors/Simon%20Chandler` — also a 404, because the sitemap URL-encodes a space. The live page
is **https://www.raconteur.net/contributors/simon-chandler** (HTTP 200) and it still carries
`data-part1="simon.chandler" data-part2="raconteur" data-part3="net"`. Control: `/contributors/tom-dennis`
(HTTP 200) carries `tom.dennis` `raconteur` `net`, so the triple is the site's standard, not a stray
attribute. `raconteur.net` MX re-checked today = Google Workspace (`aspmx.l.google.com`).
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
> - Nearly all of them charge more if you pay monthly instead of annually. Across the same tiers we
>   hold both terms for, the gap runs 1.21x to 2.53x — Browse AI is $48/month against $19/month
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
`data/pricing_snapshots.json`, each value carrying its own snapshot `date`. 1.21x–2.53x is the
same-tier monthly-vs-annual pair range from the same file; HeyGen $29 vs $24 is the narrowest,
Browse AI $48 vs $19 the widest (both 2026-09-18).

---

## 2. Anthropic subscription value — price vs support ◀ day 8, send or drop

**Source:** https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
**Posted:** 2026-09-11 16:58 UTC — **8 days** (page badge today: "Posted 8 days ago")
**Who:** **Helen Li** — independent journalist, in the page's own author field.
**Ask:** users and business owners with Anthropic customer-service experiences; DMs, email or Signal.

**Fit:** on-beat as a subscription-value story, not a grievance. We hold dated official Anthropic
pricing and no complaint of our own, so the draft leads on price and claims no support failure.

**Reply route:** **Signal `hliwrites.99`** — re-read verbatim off the live request page today (not
carried from the digest). Still the only concrete handle published on any request page in the queue.
DMs and email are also invited; the address is redacted on Sourcee. **George's lane. Not automatable.**

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
**Posted:** 2026-09-17 16:05 UTC — **2 days** (page badge today: "Posted in last 7 days")
**Who:** **Holly Shackleton**, Content Editor, Speciality Food magazine.
**Ask:** for the October issue — a speciality food/drink business given £10k for EPOS, shelf labels,
ecommerce, stock and loyalty systems: how would you spend it?

**⚠ Standing constraint — read before sending.** She wants food and drink businesses. We are not one,
and our price set covers AI tools, not retail hardware. The draft's first line says so and offers the
pricing method as a benchmark. If a non-retailer benchmark is not useful to her, drop this rather than
rework it.

**Reply route:** `holly.shackleton@artichokehq.com` — re-read today off
`specialityfoodmagazine.com/contact` (HTTP 200, 59,500 bytes), listed "Content Editor Holly Shackleton
… +44(0)1206 505110" alongside five other named staff addresses, so it is a published masthead rather
than a guessed pattern. `artichokehq.com` MX re-checked today = Microsoft 365
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
>   tier — from 1.21x up to 2.53x (checked 2026-09-18). On stock management or loyalty software, the
>   billing term moves the number more than the vendor choice does.
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
`data/pricing_snapshots.json`; 1.21x–2.53x same-tier monthly/annual from the same file. Deliberately
**no** £/$ conversion: our figures are USD and the request is in sterling, so the numbers are offered
as published.

---

## Requests deliberately NOT drafted

| Request | Why not |
|---|---|
| **FinOps — agentic AI cost overruns (13d, high, COLD)** | The highest-relevance request we have never answered and it has now been cold for two days. A finished draft has existed since `pitch-drafts-2026-09-17.md` §1, route LinkedIn DM to `linkedin.com/in/niloy-ghosh`. Send it late or drop it — re-drafting a fourth time would be the fourth time we did nothing with it. |
| Forbes — founders cutting AI use (1d, medium-low) | **New today** and a Forbes byline, but the body is explicit: "Please only answer as a comment on this post. Do not email or DM me because they won't be used." It wants a named founder's own rationale on the record. We publish anonymously-signed and have no founder to put forward. |
| The Lever — autonomous weapons survivors (1d) | New today, newest request in the window. Off-beat, and it wants survivor testimony. |
| US hospital billing errors (newest slug) | New today. Matched our spend filter on the word "billing" but the subject is medical charges, not software. |
| Over-50s adapting to AI / data-centre podcast booking / alignment framework | New today. No cost, pricing or spend content in any of them. |
| U.S. Founders — calls to slow AI development (Inc., 4d) | Wants founders' firsthand safety-guardrail accounts, and the address is redacted with no route resolved. Wrong standing and unreachable. |
| E-Discovery AI-assisted review (3d) | Wants practising e-discovery lawyers. Wrong standing. |
| Gen Z AI data annotators (Fortune, 3d) | Wants annotators describing their own work and pay. No standing. |
| AI Automation Experts — speaking slots (3d) | A speaking-slot solicitation, not a journalist request. |
| Ecommerce marketers — AI recommendation transparency (3d) | Wants AEO case studies we do not have. |
| Cybersecurity companies & AI scams (4d) | A PR firm building a spokesperson roster. Off-beat and off-standing. |
| EdTech LMS audit (7d, medium) | Queue rank 2 on relevance. Genuinely adjacent ("follow the invoice") but the writer sources people inside EdTech; skipped 2026-09-15 on that basis and the judgement stands. |
| Early-stage founders — Built From Scratch (9d, medium) | Best remaining unpitched request, a founder-profile slot. Earns standing, not a citation, and the route is a public comment. Left in `pitch-queue.md`. |
| California AI audit bills → CIOs (10d) | Its own stated deadline — "speak with a source today" — passed 2026-09-12. |
| UK managers / Gen Z AI overuse (13d) | Internal deadline "by this Wednesday September 9" passed; cold. |
| Individual contributors managing AI agents (10d) | Pitched 2026-09-18 to Rani@Sherwood.news. No reply. |
| Amplemarket Growth/Elite (13d, high) | Pitched 2026-09-18; Jan Suski replied 2026-09-18 20:39Z and we answered 21:29Z. Live thread — do not re-pitch. |
| Enterprise AI Leaders — value creation (6d) | Pitched 2026-09-15 to hello@foxandspindle.com. No reply in five days. |

---

## Send log — what "sent" actually means here

Three pitches have ever gone out from this monitor: 2026-09-15 (Enterprise AI Leaders → Fox & Spindle),
2026-09-18 (Amplemarket → Market Intelligence Tools), 2026-09-18 (Sherwood News → Rani Molla). One
reply, answered the same day. **Pitches sent today: 0.** The three drafts above are all still unsent,
which is the whole reason this queue exists.

## The one thing blocking sends that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake (`hermes mcp add --auth oauth`) that
cannot be completed from a scheduled run. It is a free read-only feed covering Connectively, HARO, X,
LinkedIn, MentionMatch and Substack — six platforms in one step, and the only path to widening a
monitor whose sole accessible source produced **zero** core-beat requests today. Endpoint re-confirmed
live this run (HTTP 401, `invalid_token`), and `hermes mcp list` in this profile still reports
"No MCP servers configured."
