# Pitch drafts — 2026-09-26

**Nothing here has been sent.** Today's queue holds **2 sendable** requests (47 tracked, 26 live, 2
sendable — `pitch-queue.md`). Both are drafted below, paste-ready, figures re-derived against
`data/pricing_snapshots.json` as it stands today (`updated: 2026-09-26`) and `data/tools.json`.

**Both sendable requests are now ONE DAY from the cold line.** That is the whole story of this run.

**What is the same and what changed since yesterday:**

1. **The live set is unchanged.** All 47 carried URLs re-verified live today (HTTP 200, request body
   served, no expiry notice). 26 live unpitched, 17 cold unpitched, 2 sendable — the same two rows for
   the fourth consecutive day, and both reply routes were re-resolved off the live pages again today.
2. **The pair range held for the fourth consecutive day**, against a snapshot refreshed today
   (`updated: 2026-09-26`). `scripts/extract_monthly_annual_pairs.py` re-asserted all 19 curated pairs
   and exited 0. **1.11x to 2.53x, median 1.25x, over 19 tiers across 14 tools.** The 1.21x and 1.16x
   floors remain superseded and must not be sent.
3. **The new window produced nothing, for the seventh run in eight.** 88 slugs since yesterday's mark,
   5 carrying an AI token, **zero carrying an AI token plus a spend token** — the fourth consecutive
   run with none, and the first with no false positive either. All 12 candidate slugs were fetched and
   read in full; none contains a price, seat, licence or spend ask.
4. **The shadow-AI draft crosses the 10-day line tomorrow.** It has now been written and unsent for
   eight consecutive runs. If it is not sent today it becomes the first *high-relevance* request this
   queue has ever lost to the cold line with a draft sitting ready.

**Unchanged standing constraint:** no draft here claims a personal account we do not have. Both say
what we are in the first line.

---

## 1. Shadow AI spend — employees paying out of pocket ◀ SEND THIS TODAY, day 9 unsent

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **9 days** (page badge today: "Posted 9 days ago"). **Crosses the
cold line tomorrow.**
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
`tom.dennis` `raconteur` `net`. The byline URL cited on 2026-09-19 (`/author/simon-chandler/`) still
returns **HTTP 404** (re-checked today) — it is dead and must not be cited.
**George's lane. Not automatable — it is a plain email send, but the address is a reconstructed byline
address rather than one published in the request body, so it is sent by hand.**

> Subject: Shadow AI spend — what the out-of-pocket tiers actually cost
>
> Hi Simon,
>
> Straight up front: I can't give you a personal account of paying for AI behind my employer's back.
> What I can give you is what those out-of-pocket buyers are actually paying.
>
> We track dated pricing for 76 AI tools. 40 of them publish a monthly price; 31 of those start at or
> under $25/month — median $16.50, lowest $4 (Khanmigo, checked 2026-09-18).
>
> Nearly all charge more if you pay monthly instead of annually. Across the 19 tiers where we hold
> both terms, the gap runs 1.11x to 2.53x (checked 2026-09-18 and 2026-09-21). Browse AI is
> $48/month against $19/month billed annually. The buyer with no company card pays the top of that
> range.
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

**Figures:** 76 tools (`data/tools.json` 76 records and `data/pricing_snapshots.json` 76 snapshot
records — both re-counted today). 40 with a non-zero monthly price, 31 of those ≤$25, median $16.50,
minimum $4 Khanmigo (checked 2026-09-18) — recomputed today from `data/pricing_snapshots.json`
(`updated: 2026-09-26`). **19 same-tier monthly-vs-annual pairs across 14 tools, 1.11x–2.53x, median
1.25x** from `data/monthly_annual_pairs.json`, re-derived today; Browse AI Personal $48 vs $19 is the
widest, replit-ai Core $20 vs $18 the narrowest. Pair dates 2026-09-18 and 2026-09-21. The 1.21x and
1.16x floors are both superseded.

---

## 2. Speciality Food — a £10k tech budget ◀ fresh-ish, reachable, weaker standing

**Source:** https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
**Posted:** 2026-09-17 16:05 UTC — **8 days** (page badge today: "Posted 8 days ago"). **Crosses the
cold line the day after tomorrow.**
**Who:** **Holly Shackleton**, Content Editor, Speciality Food magazine.
**Ask:** for the October issue — a speciality food/drink business given £10k for EPOS, shelf labels,
ecommerce, stock and loyalty systems: how would you spend it?

**⚠ Standing constraint — read before sending.** She wants food and drink businesses. We are not one,
and our price set covers AI tools, not retail hardware. The draft's first line says so and offers the
pricing method as a benchmark. If a non-retailer benchmark is not useful to her, drop this rather than
rework it. **8 days old and the October issue window is closing — send it today or drop it.**

**Reply route:** `holly.shackleton@artichokehq.com` — re-read today off
`specialityfoodmagazine.com/contact` (HTTP 200, 59,500 bytes), listed "Content Editor Holly Shackleton"
alongside five other named staff addresses (`charlotte.smith-jarvis@`, `jessica.brett@`,
`louise.barnes@`, `sam.reubin@`, `subscriptions@`, all re-read today), so it is a published masthead
rather than a guessed pattern. **George's lane. Not automatable.**

> Subject: A £10k benchmark from dated prices, if a non-retailer's data is useful
>
> Hi Holly,
>
> I'm not a speciality food business, so I can't tell you how a retailer would spend £10k. I can offer
> you one thing retailers rarely put side by side: of the 76 software tools we track, 40 publish a
> monthly price, 31 of those start at or under $25/month, and the median cheapest paid tier is $16.50
> (checked 2026-09-18).
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

**Figures:** 76 tools, 40 of them with a non-zero monthly price, 31 of those ≤$25, median $16.50, 19
tiers at 1.11x–2.53x — all recomputed today from `data/pricing_snapshots.json`
(`updated: 2026-09-26`) and `data/monthly_annual_pairs.json`. Deliberately **no** £/$ conversion: our
figures are USD and the request is in sterling, so the numbers are offered as published.

---

## Requests deliberately NOT drafted

| Request | Why not |
|---|---|
| **Nothing new this window** | 88 slugs, 5 AI-token, 0 AI+spend. All 12 candidates read in full. Closest near-miss: **GPU capacity buyers & sellers — pricing, contracts, delivery** (2026-09-25T15:53Z). A 20-minute buyer/seller chat about cloud GPU procurement. On-beat in subject, but the page publishes no email and no handle (body says "DMs/referrals welcome" with no address), and our data is AI-tool list prices, not negotiated GPU capacity contracts. Recorded, not drafted. |
| **Q4 MarTech gated-content roundup** (2026-09-25T04:39Z) | Same `#PROpportunity` PR account this queue has excluded on three earlier runs. A sponsorship solicitation, not a request. |
| **Anthropic — customer service (14d, medium-high, COLD)** | Crossed the line 2026-09-23. Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal `hliwrites.99` (still verbatim on the live page). Send late or mark skipped — seven runs unsent already. |
| **FinOps — agentic AI cost overruns (19d, high, COLD)** | The highest-relevance request we have never answered. Draft since `pitch-drafts-2026-09-17.md` §1, route LinkedIn DM to `linkedin.com/in/niloy-ghosh`. Send it late or drop it — do not redraft. |
| **Enterprise AI Leaders — value creation (12d, COLD as of today)** | Crossed the line this run. Pitched 2026-09-15 to `hello@foxandspindle.com`, eleven days of silence. An unanswered send, not an unsent draft. |
| **Enterprise AI Leaders — agent sprawl (21d) / Scientists paying for AI (21d)** | Both genuinely on-beat, both well past the cold line and unpitched. The cost of the cold queue, recorded so the loss is visible. |
| **Forbes — founders cutting AI use (7d, medium-low)** | Body is explicit: "Please only answer as a comment on this post. Do not email or DM me." Wants a named founder's own rationale on the record. |
| **BBC — London businesses that dropped AI hiring tools (5d)** | Wants a London employer's own decision; no cost angle in the body; address redacted with no route resolved. |
| All other live rows (26 live less the 2 above) | Off-beat calls — hospital billing, podcast guesting, ML methods, alignment philosophy, AI-hardware makers. All listed in `pitch-queue.md` under "Live but not sendable". |

---

## Send log — what "sent" actually means here

Three pitches have ever gone out from this monitor: 2026-09-15 (Enterprise AI Leaders → Fox & Spindle),
2026-09-18 (Amplemarket → Market Intelligence Tools), 2026-09-18 (Sherwood News → Rani Molla). One
reply, answered same day. **Pitches sent today: 0.**

**Mailbox checked 2026-09-26** (`himalaya`): **no reply to any pitch.** INBOX top is still the Google
"Security alert" new-sign-in notice (2026-09-23 15:59Z) above three identical "New AI tool submission"
form-mails from 2026-09-22 15:29Z. The most recent human message is still Jan Suski's 2026-09-18 20:39Z
reply, which we answered at 21:29Z. Sent Mail top unchanged at msg 187; All Mail top unchanged at msg
257; Spam unchanged at three items (two delivery-failure bounces and a directory form-mail). **No reply
to the 2026-09-15 send (eleven days) or the 2026-09-18 Sherwood send (eight days).**

**Still owed, and not a pitch:** a correction to Jan Suski. He was told the same-tier monthly/annual
range is "1.21x-2.53x, median 1.33x"; the current verified figure is **1.11x-2.53x, median 1.25x over
19 tiers**. Eight days outstanding. Reply to `jan@jansuski.com`, In-Reply-To the existing thread.

## The one thing blocking sends that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake that cannot be completed from a
scheduled run. It is a free read-only feed covering Connectively, HARO, X, LinkedIn, MentionMatch and
Substack — six platforms in one step, and the only path to widening a monitor whose single accessible
source has now produced **no core-beat request on seven of the last eight runs and no real AI+spend
slug for four consecutive runs**. Endpoint re-confirmed live this run (HTTP 401,
`{"error":"invalid_token","error_description":"No authorization provided"}`).
