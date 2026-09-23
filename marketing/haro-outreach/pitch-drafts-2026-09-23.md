# Pitch drafts — 2026-09-23

**Nothing here has been sent.** Today's queue holds **2 sendable** requests (47 tracked, 26 live, 2
sendable — `pitch-queue.md`). Both are drafted below, paste-ready, figures re-derived against
`data/pricing_snapshots.json` as it stands today (`updated: 2026-09-23`).

**Two things changed since yesterday:**

1. **The Anthropic draft dropped out of the sendable set.** It is 11 days old today, so it crossed the
   >10-day cold line and the queue no longer counts it as live. The draft is unchanged and still valid
   at `pitch-drafts-2026-09-22.md` §2, route Signal `hliwrites.99`. **Send it late today or record it
   as skipped in `pitch-ledger.json`** — it has now been written and unsent for four consecutive runs.
   It is not re-drafted here, because drafting it a fifth time is the exact defect this monitor exists
   to fix.
2. **The pair range held.** `scripts/extract_monthly_annual_pairs.py` re-asserted all 19 curated pairs
   against today's snapshot file and passed clean (exit 0) — the first run since the gate was added
   where it did not fail loudly. **1.11x to 2.53x, median 1.25x, over 19 tiers across 14 tools.**
   `data/monthly_annual_pairs.json` re-derived and rewritten today. The 1.21x and 1.16x floors remain
   superseded and must not be sent.

**Unchanged standing constraint:** no draft here claims a personal account we do not have. Both say
what we are in the first line.

---

## 1. Shadow AI spend — employees paying out of pocket ◀ SEND THIS FIRST, day 6 unsent

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **6 days** (page badge today: "Posted in last 7 days")
**Who:** **Simon Chandler** — named in the page's own author field; covers enterprise tech for Raconteur.
**Ask:** quotes from full-time employees who use AI without their employer's knowledge and pay for it
personally. Anonymity offered.

**Why it is the best live request:** employees buying AI without approval and paying personally is
unbudgeted, unenumerated software spend — the quantity our dated price set exists to make visible.
Raconteur's own contact page asks for "pitches with exclusive business data", which is what we hold. It
is the only high-relevance request in the queue and the only core-beat find the monitor has produced.

**⚠ Honesty constraint — read before sending.** The request wants employees' personal accounts. We are
a publisher with no such account. The draft says so in its opening line. Do not edit that line out.

**Reply route:** `simon.chandler@raconteur.net` — **re-resolved today.** The live page
**https://www.raconteur.net/contributors/simon-chandler** returns HTTP 200 (154,797 bytes) and still
carries `data-part1="simon.chandler" data-part2="raconteur" data-part3="net"`, which the site's JS
assembles at runtime. Control on the same run: `/contributors/tom-dennis` (HTTP 200) carries
`tom.dennis` `raconteur` `net`. `raconteur.net` MX re-checked today = Google Workspace
(`aspmx.l.google.com`, priority 1). The byline URL cited on 2026-09-19 (`/author/simon-chandler/`)
still returns **HTTP 404** — it is dead and must not be cited. **George's lane. Not automatable.**

> Subject: Shadow AI spend — what the out-of-pocket tiers actually cost
>
> Hi Simon,
>
> Straight up front: I can't give you a personal account of paying for AI behind my employer's back.
> What I can give you is what those out-of-pocket buyers are actually paying.
>
> We track dated pricing for 76 AI tools. 31 of them have a cheapest paid tier at or under $25/month
> — median $16.50, lowest $4 (Khanmigo, checked 2026-09-18).
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

**Figures:** 76 tools (`data/tools.json`, 76 records — re-counted today). 31 with a cheapest paid
monthly tier ≤$25, median $16.50, minimum $4 Khanmigo (2026-09-18) — recomputed today from the `digest`
text of `data/pricing_snapshots.json` (`updated: 2026-09-23`); 40 tools publish a non-zero monthly
price, so the 31 is measured against that population. **19 same-tier monthly-vs-annual pairs across 14
tools, 1.11x–2.53x, median 1.25x** from `data/monthly_annual_pairs.json`, re-derived today; Browse AI
$48 vs $19 is the widest, replit-ai Core $20 vs $18 the narrowest. Pair dates 2026-09-18 and 2026-09-21.
The 1.21x and 1.16x floors are both superseded. **Draft word count: 154 (body, excl.
subject/signature — measured today).**

---

## 2. Speciality Food — a £10k tech budget ◀ fresh, reachable, weaker standing

**Source:** https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
**Posted:** 2026-09-17 16:05 UTC — **5 days** (page badge today: "Posted in last 7 days")
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
`louise.barnes@`, `sam.reubin@`, `subscriptions@`), so it is a published masthead rather than a guessed
pattern. `artichokehq.com` MX re-checked today = Microsoft 365
(`artichokehq-com.mail.protection.outlook.com`). **George's lane. Not automatable.**

> Subject: A £10k benchmark from dated prices, if a non-retailer's data is useful
>
> Hi Holly,
>
> I'm not a speciality food business, so I can't tell you how a retailer would spend £10k. I can offer
> you one thing retailers rarely put side by side: of the 76 software tools we track, 40 publish a
> non-zero monthly price, 31 of those start at or under $25/month, and the median cheapest paid tier is
> $16.50 (checked 2026-09-18).
>
> A per-seat tool is a recurring cost, not a one-off — so the £10k is really a decision about the next
> 24 months, not one purchase.
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

**Figures:** 76 tools, 40 of them with a non-zero monthly price, 31 of those ≤$25, median $16.50 — all
recomputed today from `data/pricing_snapshots.json` (`updated: 2026-09-23`); 19 tiers, 1.11x–2.53x from
`data/monthly_annual_pairs.json`, re-derived today. Deliberately **no** £/$ conversion: our figures are
USD and the request is in sterling, so the numbers are offered as published. **Draft word count: 164
(body, excl. subject/signature — measured today).**

---

## Requests deliberately NOT drafted

| Request | Why not |
|---|---|
| **Anthropic — customer service (11d, medium-high, CROSSED COLD TODAY)** | Crossed the >10-day line this run. Draft is finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal `hliwrites.99` (still verbatim on the live page). Send today or mark skipped — four runs unsent already. |
| **FinOps — agentic AI cost overruns (16d, high, COLD)** | The highest-relevance request we have never answered. Draft since `pitch-drafts-2026-09-17.md` §1, route LinkedIn DM to `linkedin.com/in/niloy-ghosh`. Send it late or drop it — do not redraft. |
| New this window: 8 AI-token slugs (med-lab AI adoption, PR-review capacity, research agents, fractional executives, tech-leader podcast, physics tech, humanist essay, Ifa/Yoruba AI) | All eight were fetched and read. Every one is either a different sector's adoption story or a booking/philosophy call; **none contains a price, seat, licence or spend ask.** No AI+spend slug appeared in the window at all — the first time in five runs. |
| Procurement/tariff, affordable-housing cost, health tools, Ontario privacy, protein-beverage buying (4d–1d) | The only other spend-adjacent slugs in the window; the tokens matched words, not subjects (tariffs, construction cost, wellness, privacy, consumer goods). None is software spend. |
| BBC — London businesses that dropped AI hiring tools (2d) | Wants a London employer's own decision; no cost angle in the body; address redacted with no route resolved. |
| Forbes — founders cutting AI use (4d, medium-low) | Body is explicit: "Please only answer as a comment on this post. Do not email or DM me." Wants a named founder's own rationale on the record. |
| Enterprise AI Leaders — agent sprawl (18d, high) / Scientists paying for AI (18d, high) | Both genuinely on-beat, both well past the cold line and unpitched. Not drafted this run; they are the cost of the cold queue, recorded so the loss is visible. |
| EdTech LMS audit (10d) / Early-stage founders Built From Scratch (12d) | Standing / founder-profile slot with a public-comment route. Both cold. |
| Individual contributors managing agents (13d) | Pitched 2026-09-18 to Rani@Sherwood.news. No reply. |
| Amplemarket Growth/Elite (16d, high) | Pitched 2026-09-18; Jan Suski replied 2026-09-18 20:39Z, answered 21:29Z. Live thread — do not re-pitch. **A correction is still owed on the wrong 1.21x floor — see the ledger's `figures_disclosure`.** |
| Enterprise AI Leaders — value creation (9d) | Pitched 2026-09-15 to hello@foxandspindle.com. No reply in eight days. |
| Remaining live rows (26 live less the 2 above) | Off-beat calls — hospital billing, podcast guesting, PR solicitation, ML methods, hospital-bill testimony, alignment philosophy. All listed in `pitch-queue.md` under "Live but not sendable". |

---

## Send log — what "sent" actually means here

Three pitches have ever gone out from this monitor: 2026-09-15 (Enterprise AI Leaders → Fox & Spindle),
2026-09-18 (Amplemarket → Market Intelligence Tools), 2026-09-18 (Sherwood News → Rani Molla). One
reply, answered same day. **Pitches sent today: 0.**

**Mailbox checked 2026-09-23** (`himalaya`): **no reply to any pitch.** INBOX top is a Google "Security
alert" (new-sign-in notice, 2026-09-23 15:59Z) above three identical "New AI tool submission" form-mails
from 2026-09-22 15:29Z. The most recent human message is still Jan Suski's 2026-09-18 20:39Z reply,
which we answered at 21:29Z. Sent Mail top unchanged at msg 178; All Mail top is msg 239 (the Google
alert). Spam holds three items, all delivery-failure bounces and directory form-mail. **No reply to the
2026-09-15 send (eight days) or the 2026-09-18 Sherwood send (five days).**

## The one thing blocking sends that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake (`hermes mcp add --auth oauth`) that
cannot be completed from a scheduled run. It is a free read-only feed covering Connectively, HARO, X,
LinkedIn, MentionMatch and Substack — six platforms in one step, and the only path to widening a monitor
whose single accessible source has now produced **no core-beat request on two of the last four runs**.
Endpoint re-confirmed live this run (HTTP 401, `{"error":"invalid_token","error_description":"No
authorization provided"}`), and `hermes mcp list` in this profile still reports "No MCP servers
configured."
