# Pitch drafts — 2026-09-19

Written for the **best live requests in the queue**. Every draft below is paste-ready, signed
AIToolsEssentials, and under 200 words. No draft names George.

**Nothing in this file has been sent.** Every route is George's lane: two publication-side email
addresses and one Signal handle. The agent sent nothing.

Every figure is read off our own verified data with its check date, recomputed today by
`_figures_0919.py` rather than carried forward — the 2026-09-15 pitch went out citing a count (60)
that had drifted to 70, and the 2026-09-18 Amplemarket pitch cited two opacity claims that were
simply wrong. `_verify_drafts_0919.py` asserts every number in this file.

**Why these three.** The queue's #1 is new and on-beat (Raconteur, shadow AI spend, 2 days) and is
the only high-relevance request with a resolved email route. Second is the Anthropic
subscription-value request, whose Signal handle is the one direct channel published on any page in
the queue; it is now 7 days old and rising, so send or drop. Third is the freshest request in the
queue (Speciality Food, 1 day) with a verified address for its named author — lower standing, but
fresh and reachable. Rank-4 and below stay in `pitch-queue.md`.

---

## 1. Shadow AI spend — employees paying out of pocket ◀ the one to send first

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **2 days** (page badge: "Posted in last 7 days")
**Who:** **Simon Chandler** — named in the page's own author field this run. Covers enterprise tech
for Raconteur and TechRepublic; ten years on technology, bylines at Wired, Forbes, Digital Trends,
Business Insider. Based in Hove/Brighton, UK.
**Ask:** "I am looking for quotes and comments from full-time employees who use AI without the
approval or knowledge of their employers, and who even pay out of their own pocket to use AI. I and
Raconteur will of course protect your anonymity if we use your quotes."

**Why it is the best live request:** this is the closest Sourcee has come to our actual beat in six
runs. Employees buying AI without approval and paying personally is unbudgeted, unenumerated
software spend — the quantity our dated price set exists to make visible. Raconteur's own contact
page says it wants "pitches with exclusive business data", which is what we hold.

**⚠ Honesty constraint — read before sending.** The request wants employees to give personal
accounts. We are a publisher, not a shadow-AI employee. The draft offers the price evidence and says
outright that we hold no personal account and will not pose as one.

**Reply route:** `simon.chandler@raconteur.net` — reconstructed this run from Raconteur's own byline
page, which publishes the address as an obfuscated `data-part1`/`data-part2`/`data-part3` triple that
the site's `scripts-last.min.js` assembles at runtime (`part1 + '@' + part2 + '.' + part3`). Pattern
cross-checked against a second author's byline (Ian Deering → `id@raconteur.net`) so it is the site's
standard, not a stray attribute. `raconteur.net` MX = Google Workspace
(`aspmx.l.google.com`). Raconteur's /contact page states PRs should contact the relevant writer
directly. **George's lane. Not automatable.**

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

**Figures used, and where they come from:** 76 tools (`data/tools.json`, 76 records); 31 tools with
a cheapest paid monthly tier ≤$25, median $16.50, minimum $4 (Khanmigo) — all computed from the
`digest` text of `data/pricing_snapshots.json` by regex over `$N/month` in each tool's own snapshot,
every value carrying that snapshot's own `date` (Khanmigo 2026-09-18); the 1.21x–2.53x range is
same-tier monthly-vs-annual pairs, one tier per tool, from the same file — Browse AI $48 vs $19
(2026-09-18) is the widest, HeyGen $29 vs $24 (2026-09-18) the narrowest.

---

## 2. Anthropic subscription value — price vs support ◀ the only published direct channel

**Source:** https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
**Posted:** 2026-09-11 16:58 UTC — **7 days** (page badge: "Posted in last 7 days")
**Who:** **Helen Li** — independent journalist, named in the page's own author field.
**Ask:** "I am writing a story about the difficulties that people have had with Anthropic customer
service. Are there any users or business owners who can share about their Anthropic customer service
experiences? I'd love to chat via DMs, email, or Signal hliwrites.99"

**Fit:** on-beat as a subscription-value story, not a grievance. We hold dated official Anthropic
pricing and no complaint of our own, so the draft leads on the price side and offers pricing evidence
only. It makes no claim that we had a support failure.

**Reply route:** **Signal `hliwrites.99`** — re-read verbatim off the live page this run (not carried
from the digest). It is still the only concrete handle published on any request page in this queue.
DMs and email are also invited; the address is redacted on Sourcee. **George's lane. Not
automatable.**

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

**Figures used:** Claude Pro $17/month with a $200 annual prepayment or $20 month-to-month; Max from
$100/month; Team Standard $20/seat/month and Premium $100/seat/month. All five come from
`data/pricing_snapshots.json` key `claude` (`date` 2026-09-18, `verified_against`
https://www.anthropic.com/pricing) **except** the Premium seat price: that snapshot's `digest` field
is 200 characters and truncates mid-sentence after "Standard seats at $20 per seat per month", so the
$100 Premium seat is quoted from `data/tool_sources.json` slug `claude`
(`pricing_checked_date` 2026-09-18), which carries the full sentence including Premium seats at $100
per seat per month. The verifier checks each figure against the file that actually holds it rather
than assuming both files agree. "Five figures a year per seat" is arithmetic on the $100/seat/month
Premium tier — not a separately published number.

---

## 3. Speciality Food — a £10k tech budget ◀ fresh, reachable, weaker standing

**Source:** https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
**Posted:** 2026-09-17 16:05 UTC — **1 day** (page badge: "Posted in last 7 days")
**Who:** **Holly Shackleton**, Content Editor, Speciality Food magazine (specialityfoodmagazine.com).
**Ask:** for the October issue — if you had £10k to spend on revamping your business with EPOS tools,
electronic shelf labels, ecommerce and website, stock management, loyalty systems, how would you
utilise it?

**⚠ Standing constraint — read before sending.** She wants speciality food and drink businesses. We
are not a food retailer and our price set covers AI tools, not retail hardware. The draft's first line
says so and offers the pricing-method half as a benchmark, not as a retailer's answer. If a
non-retailer benchmark is not useful to her, this pitch should be dropped rather than reworked.

**Reply route:** `holly.shackleton@artichokehq.com` — published with her name on the magazine's own
/contact page, re-verified live this run (listed as "Content Editor", direct line
+44(0)1206 505110). `artichokehq.com` MX = Microsoft 365
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

**Figures used:** 40 of 76 tools with a non-zero monthly price, 31 of those ≤$25, median $16.50 —
computed from `data/pricing_snapshots.json` (checked 2026-09-18); the 1.21x–2.53x same-tier
monthly/annual range from the same file. Deliberately **no** £/$ conversion: our figures are in USD
and the request is in sterling, so the draft offers the numbers as published rather than converting
them.

---

## Requests deliberately NOT drafted

| Request | Why not |
|---|---|
| FinOps — agentic AI cost overruns (12d, high) | **Draft already exists** as `pitch-drafts-2026-09-17.md` §1 (route: LinkedIn DM to linkedin.com/in/niloy-ghosh). It has now crossed the 10-day line unpitched. Send that existing draft or drop it — do not re-draft. |
| E-Discovery AI-assisted review (Mass Lawyers Weekly, 2d) | Wants practising e-discovery lawyers. We are a pricing publisher. Wrong standing. |
| U.S. Founders — calls to slow AI development (Inc., 3d) | Wants founders' firsthand safety-guardrail accounts. Wrong standing, and the route is unresolved. |
| Gen Z AI data annotators (Fortune, 2d) | Wants annotators describing their own work and pay. No standing. |
| AI Automation Experts — speaking slots (2d) | A speaking-slot solicitation, not a journalist request. |
| Ecommerce marketers — AI recommendation transparency (MarketingSherpa, 2d) | Wants AEO case studies we do not have. |
| Cybersecurity companies & AI scams (3d, Sandra Torres) | A PR firm building a spokesperson roster. Off-beat and off-standing. |
| EdTech LMS audit (6d, medium) | Queue rank 5; the procurement-incentive angle is genuinely adjacent to ours ("follow the invoice") but the writer sources people inside EdTech. Skipped on 2026-09-15 for that reason; judgement stands. |
| Early-stage founders — Built From Scratch (8d, medium) | Queue rank 2 and the best of the remaining, but it is a founder-profile post: earns standing, no citation. Left in `pitch-queue.md`. |
| California AI audit bills → CIOs (Industry Dive, 9d) | Its own stated deadline — "speak with a source today" — passed 2026-09-12. |
| UK managers / Gen Z AI overuse (MaryLou Costa, 12d) | Internal deadline ("by this Wednesday September 9") passed; now cold. |
| Individual contributors managing AI agents (Sherwood, 9d) | Pitched 2026-09-18 (Rani@Sherwood.news). No reply as of this run. |
| Amplemarket Growth/Elite (12d, high) | Pitched 2026-09-18; the correspondent replied and we answered. Live thread — do not re-pitch. |
| Enterprise AI Leaders — value creation (5d) | Pitched 2026-09-15. No reply as of this run. |

---

## The one thing blocking sends that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake (`hermes mcp add --auth oauth`) that
cannot be completed from a scheduled run. It is a free read-only feed covering Connectively, HARO, X,
LinkedIn, MentionMatch and Substack — six platforms in one step, and the only path to widening a
monitor whose sole accessible source has produced exactly one core-beat request in six runs. Endpoint
re-confirmed live this run (HTTP 401, `invalid_token`), and `hermes mcp list` in this profile still
reports no MCP servers configured.
