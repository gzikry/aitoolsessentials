# Pitch drafts — 2026-09-22

**Nothing here has been sent.** These are the three sendable requests in today's queue (see
`pitch-queue.md` — 47 tracked, 27 live, **3 sendable**) — the same three as the last four runs,
re-verified against today's pages and today's data rather than carried on trust. Each has now been
written and unsent for 3–4 consecutive runs. **A draft is not progress; only the send is.**

## What changed today — the pair range moved a second time

The same-tier monthly-vs-annual range has now been wrong twice, in opposite directions, for two
different reasons. The current figures are **1.11x to 2.53x, median 1.25x, over 19 tiers across 14
tools**.

- **1.21x–2.53x, median 1.33x** — published 2026-09-18 and sent to a real correspondent. Wrong
  because the pair population was regex-dependent and nobody had defined it: four extractions over
  the same file returned 2, 7, 9 and 18 pairs.
- **1.16x–2.53x, median 1.25x, 18 pairs** — the 2026-09-21 correction. Right about the population,
  but it went stale within a day: the **replit-ai** snapshot was refreshed on 2026-09-21 and both of
  that tool's figures moved — Core is now **$20/month or $18/month billed annually** (was $25/$20)
  and Pro is newly quoted as a second pair at **$100/$90**.
- **1.11x–2.53x, median 1.25x, 19 tiers** — today's figures, from `data/monthly_annual_pairs.json`.

`scripts/extract_monthly_annual_pairs.py` asserts each curated pair against its own sentence in the
snapshot file and **failed loudly** this run — which is how the drift was caught. But it then wrote
the stale 1.16x set to disk anyway, so a run reading the file rather than the exit code would have
quoted a range the live snapshot no longer supported. The write is now gated behind a clean
assertion pass; on failure it leaves the last good file in place and exits 1.

**Consequence for the drafts below:** every draft before today cites a superseded floor, including
the 1.16x one in `pitch-drafts-2026-09-21.md`. Use **1.11x–2.53x, 19 tiers** or drop the sentence.
The wrong 1.21x floor is still standing in the 2026-09-18 message to Jan Suski; it is disclosed in
`pitch-ledger.json` (`figures_disclosure`) and the correction is still unsent.

**Why these three.** They are the only rows in the queue that are live, not cold, ranked above the
tangential band, *and* have a resolved reply route a human can act on. The other 24 live rows are
off-beat calls (hospital billing, podcast guesting, PR solicitation, founders' profile slots) that
the queue documents as excluded.

---

## 1. Shadow AI spend — employees paying out of pocket ◀ SEND THIS FIRST, day 5 unsent

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **5 days** (page badge today: "Posted in last 7 days")
**Who:** **Simon Chandler** — in the page's own author field. Covers enterprise tech for Raconteur and
TechRepublic; writes TechRepublic's Tech Insider Europe newsletter; ten years on technology with
bylines at Wired, Forbes, Digital Trends, Business Insider, Decrypt.
**Ask:** quotes from full-time employees who use AI without their employer's knowledge and pay for it
personally; anonymity offered.

**Why it is the best live request:** employees buying AI without approval and paying personally is
unbudgeted, unenumerated software spend — the quantity our dated price set exists to make visible.
Raconteur's own contact page asks for "pitches with exclusive business data", which is what we hold.
It is the only high-relevance request in the queue and the only core-beat find in nine runs.

**⚠ Honesty constraint — read before sending.** The request wants employees' personal accounts. We
are a publisher with no such account. The draft says so in its first line and offers price evidence
instead. Do not let anyone edit that line out.

**Reply route:** `simon.chandler@raconteur.net` — **re-resolved today.** The live page
**https://www.raconteur.net/contributors/simon-chandler** returns HTTP 200 (154,895 bytes) and still
carries `data-part1="simon.chandler" data-part2="raconteur" data-part3="net"`, which the site's JS
assembles at runtime. Control on the same run: `/contributors/tom-dennis` (HTTP 200) carries
`tom.dennis` `raconteur` `net`. `raconteur.net` MX re-checked today = Google Workspace
(`aspmx.l.google.com`). The byline URL cited on 2026-09-19 (`/author/simon-chandler/`) still 404s —
it is dead and must not be cited. **George's lane. Not automatable.**

> Subject: Shadow AI spend — what the out-of-pocket tiers actually cost
>
> Hi Simon,
>
> Straight up front: I can't give you a personal account of paying for AI behind my employer's back.
> What I can give you is what those out-of-pocket buyers are actually paying. We track dated pricing
> for 76 AI tools, and 31 of them have a cheapest paid tier at or under $25/month — median $16.50,
> lowest $4 (Khanmigo, checked 2026-09-18).
>
> Nearly all of them charge more if you pay monthly instead of annually. Across the 19 tiers we hold
> both terms for, the gap runs 1.11x to 2.53x — Browse AI is $48/month against $19/month billed
> annually (checked 2026-09-18). The buyer with no company card pays the top of that range.
>
> That's the shape of shadow spend: small enough to expense personally, expensive enough to matter
> over a year, and invisible to whoever holds the budget.
>
> Happy to hand over the full dated set if it's useful, and to name my source for every number.
>
> AIToolsEssentials
> https://aitoolessentials.com
>
> --
> We publish dated pricing evidence for AI tools and write about overlapping subscriptions and AI
> budget visibility. Reply "stop" and I won't follow up again.

**Figures:** 76 tools (`data/tools.json`, 76 records). 31 with a cheapest paid monthly tier ≤$25,
median $16.50, minimum $4 Khanmigo (2026-09-18) — computed from the `digest` text of
`data/pricing_snapshots.json`, each value carrying its own snapshot `date`. **19 same-tier
monthly-vs-annual pairs across 14 tools, 1.11x–2.53x, median 1.25x** from
`data/monthly_annual_pairs.json` (curated, sentence-asserted); Browse AI $48 vs $19 is the widest,
replit-ai Core $20 vs $18 the narrowest. Pair dates 2026-09-18 and 2026-09-21. The 1.21x and 1.16x
floors are both superseded.

---

## 2. Anthropic subscription value — price vs support ◀ day 10, LAST DAY BEFORE COLD

**Source:** https://www.sourcee.app/journo-request/anthropic-users-and-business-owners-customer-service-experiences
**Posted:** 2026-09-11 16:58 UTC — **10 days** (page badge today: "Posted 10 days ago")
**Who:** **Helen Li** — independent journalist, in the page's own author field.
**Ask:** users and business owners with Anthropic customer-service experiences; DMs, email or Signal.

**Fit:** on-beat as a subscription-value story, not a grievance. We hold dated official Anthropic
pricing and no complaint of our own, so the draft leads on price and claims no support failure.

**Reply route:** **Signal `hliwrites.99`** — re-read verbatim off the live request page today (page
body: "I'd love to chat via DMs, email, or Signal hliwrites.99"). Still the only concrete handle
published on any request page in the queue. DMs and email are also invited; the address is redacted
on Sourcee. **George's lane. Not automatable.**

**This is the fourth consecutive run it has been the queue's #2.** At exactly 10 days it is on the
cold line — tomorrow it reads cold. **Send it today or record it as skipped in
`pitch-ledger.json` in the same pass.** Carrying it a fifth time is precisely the defect this
monitor exists to fix.

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
> https://aitoolessentials.com
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
**Posted:** 2026-09-17 16:05 UTC — **4 days** (page badge today: "Posted in last 7 days")
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
> I'm not a speciality food business, so I can't tell you how a retailer would spend £10k. I can
> offer you one thing retailers rarely put side by side: 40 of the 76 software tools we track publish
> a non-zero monthly price, 31 of those start at or under $25/month, and the median cheapest paid tier
> is $16.50 (checked 2026-09-18). A per-seat tool is a recurring cost, not a one-off — the £10k is
> really a decision about the next 24 months.
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

**Figures:** 40 of 76 with a non-zero monthly price, 31 of those ≤$25, median $16.50 — from
`data/pricing_snapshots.json`; 19 tiers, 1.11x–2.53x from `data/monthly_annual_pairs.json`.
Deliberately **no** £/$ conversion: our figures are USD and the request is in sterling, so the numbers
are offered as published.

---

## Requests deliberately NOT drafted

| Request | Why not |
|---|---|
| **FinOps — agentic AI cost overruns (15d, high, COLD)** | The highest-relevance request we have never answered, cold since four runs. A finished draft has existed since `pitch-drafts-2026-09-17.md` §1, route LinkedIn DM to `linkedin.com/in/niloy-ghosh`. Send it late or drop it — re-drafting a fifth time would be the fifth time we did nothing with it. |
| BBC — London businesses that dropped AI hiring tools (2d, new) | The only AI+spend slug in today's window, but the spend token matched the word "tools". Wants a London employer's own decision; no cost angle in the body and we cannot authenticate standing. |
| SaaS tools for gated content — Q4 roundup (2d, new) | Third post in three runs from the same #PROpportunity PR account. Wants a tool name and a founder quote in a category we do not cover. Solicitation, not reportage. |
| Engineering managers measuring AI use (2d, new) | Management-philosophy newsletter. No pricing, seat, licence or procurement content. |
| Former AI skeptics — changed views (2d, new) | Personal-testimony call; publishes a Signal handle (`madymills.21`) but there is nothing on-beat to send it. |
| AI hardware makers / creative-industry podcast / founders podcast (3 today) | Creator and booking solicitation. Not reporter calls. |
| Founders cutting AI use (Forbes, 3d, medium-low) | The body is explicit: "Please only answer as a comment on this post. Do not email or DM me because they won't be used." Wants a named founder's own rationale on the record. |
| Early-stage founders — Built From Scratch (11d, medium) | Crossed the cold line. A founder-profile slot with a public-comment route: earns standing, not a citation. |
| ML researchers — continuous learning (2d) | A researcher-to-researcher methods call. Nothing to do with spend. |
| Sales-enablement SaaS sourcing / PDF-workflow (2d) | #PROpportunity PR posts from the same account. Wrong category. |
| Founders 55+ series (2d) | Off-beat. |
| US hospital billing errors (2d) | Matched our spend filter on the word "billing" but the subject is medical charges, not software. |
| The Lever — autonomous weapons survivors (2d) | Wants survivor testimony. Off-beat. |
| Over-50s adapting to AI (2d) | Workplace-culture piece, no cost angle. |
| AI alignment framework (3d) | Self-published framework discussion. |
| E-Discovery AI-assisted review (5d) | Wants practising e-discovery lawyers. Wrong standing. |
| Gen Z AI data annotators (Fortune, 5d) | Wants annotators describing their own work and pay. No standing. |
| Ecommerce marketers — AI recommendation transparency (5d) | Wants AEO case studies we do not have. |
| AI automation experts — speaking slots (5d) | A speaking-slot solicitation, not a journalist request. |
| Cybersecurity companies & AI scams (6d) | A PR firm building a spokesperson roster. Off-beat and off-standing. |
| U.S. Founders — calls to slow AI development (6d) | Wants founders' firsthand safety-guardrail accounts; address redacted with no route resolved. Wrong standing and unreachable. |
| EdTech LMS audit (9d, medium) | Genuinely adjacent ("follow the invoice") but the writer sources people inside EdTech; skipped 2026-09-15 on that basis and the judgement stands. |
| California AI audit bills → CIOs (12d) | Its own stated deadline — "speak with a source today" — passed 2026-09-12. |
| UK managers / Gen Z AI overuse (15d) | Internal deadline "by this Wednesday September 9" passed; cold. |
| Individual contributors managing AI agents (12d) | Pitched 2026-09-18 to Rani@Sherwood.news. No reply. |
| Amplemarket Growth/Elite (15d, high) | Pitched 2026-09-18; Jan Suski replied 2026-09-18 20:39Z and we answered 21:29Z. Live thread — do not re-pitch. |
| Enterprise AI Leaders — value creation (8d) | Pitched 2026-09-15 to hello@foxandspindle.com. No reply in seven days. |

---

## Send log — what "sent" actually means here

Three pitches have ever gone out from this monitor: 2026-09-15 (Enterprise AI Leaders → Fox & Spindle),
2026-09-18 (Amplemarket → Market Intelligence Tools), 2026-09-18 (Sherwood News → Rani Molla). One
reply, answered the same day. **Pitches sent today: 0.** The three drafts above are all still unsent.

**Mailbox checked 2026-09-22:** no new replies. INBOX top is three identical "New AI tool submission"
form-mails at 15:29Z; the most recent human message is still Jan Suski's 2026-09-18 20:39Z reply, which
we answered at 21:29Z. No reply to the 2026-09-15 send (seven days) or the 2026-09-18 Sherwood send
(four days). Spam holds three items, all delivery-failure bounces and directory form-mail. Sent Mail
top is unchanged at msg 178. **A reply to the Amplemarket pitch is the only one this monitor has ever
received.**

## The one thing blocking sends that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake (`hermes mcp add --auth oauth`) that
cannot be completed from a scheduled run. It is a free read-only feed covering Connectively, HARO, X,
LinkedIn, MentionMatch and Substack — six platforms in one step, and the only path to widening a
monitor whose sole accessible source produced zero new core-beat requests for the third consecutive
run. Endpoint re-confirmed live this run (HTTP 401, `{"error":"invalid_token","error_description":"No
authorization provided"}`), and `hermes mcp list` in this profile still reports "No MCP servers
configured."
