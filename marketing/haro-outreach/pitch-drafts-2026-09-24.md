# Pitch drafts — 2026-09-24

**Nothing here has been sent.** Today's queue holds **2 sendable** requests (47 tracked, 26 live, 2
sendable — `pitch-queue.md`). Both are drafted below, paste-ready, figures re-derived against
`data/pricing_snapshots.json` as it stands today (`updated: 2026-09-24`).

**What is the same and what changed since yesterday:**

1. **The live set is unchanged.** All 47 carried URLs re-verified live today (HTTP 200, request body
   served, no expiry notice). 26 live unpitched, 17 cold unpitched, 2 sendable — the same two rows as
   yesterday, and both reply routes were re-resolved off the live pages again today.
2. **The pair range held for the second consecutive day.** `scripts/extract_monthly_annual_pairs.py`
   re-asserted all 19 curated pairs against today's refreshed snapshot file and passed clean (exit 0).
   **1.11x to 2.53x, median 1.25x, over 19 tiers across 14 tools.** `data/monthly_annual_pairs.json`
   re-derived and rewritten today. The 1.21x and 1.16x floors remain superseded and must not be sent.
3. **The new window produced nothing.** 108 slugs since yesterday's mark, 8 carrying an AI token,
   **zero carrying an AI token plus a spend token** — the second consecutive run with none. All 8 were
   fetched and read in full; none contains a price, seat, licence or spend ask.
4. **One row crossed the cold line and it cost nothing.** EdTech — LMS audit went 10d → 11d. It was
   recorded as skipped on 2026-09-15, so it was never sendable and no draft was lost.

**Unchanged standing constraint:** no draft here claims a personal account we do not have. Both say
what we are in the first line.

---

## 1. Shadow AI spend — employees paying out of pocket ◀ SEND THIS FIRST, day 7 unsent

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **7 days** (page badge today: "Posted in last 7 days")
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
still returns **HTTP 404** (re-checked today) — it is dead and must not be cited.
**George's lane. Not automatable.**

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

**Figures:** 76 tools (`data/pricing_snapshots.json`, 76 snapshot records and `data/tools.json` 76
records — both re-counted today). 31 with a cheapest paid monthly tier ≤$25, median $16.50, minimum $4
Khanmigo (2026-09-18) — recomputed today from the `digest` text of `data/pricing_snapshots.json`
(`updated: 2026-09-24`); 40 tools publish a non-zero monthly price, so the 31 is measured against that
population. **19 same-tier monthly-vs-annual pairs across 14 tools, 1.11x–2.53x, median 1.25x** from
`data/monthly_annual_pairs.json`, re-derived today (built 2026-09-24); Browse AI $48 vs $19 is the
widest, replit-ai Core $20 vs $18 the narrowest. Pair dates 2026-09-18 and 2026-09-21. The 1.21x and
1.16x floors are both superseded. **Draft word count: measured below, not asserted.**

---

## 2. Speciality Food — a £10k tech budget ◀ fresh, reachable, weaker standing

**Source:** https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
**Posted:** 2026-09-17 16:05 UTC — **6 days** (page badge today: "Posted in last 7 days")
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
`louise.barnes@`, `sam.reubin@`, `subscriptions@`, all re-read today), so it is a published masthead
rather than a guessed pattern. `artichokehq.com` MX re-checked today = Microsoft 365
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
recomputed today from `data/pricing_snapshots.json` (`updated: 2026-09-24`); 19 tiers, 1.11x–2.53x from
`data/monthly_annual_pairs.json`, re-derived today. Deliberately **no** £/$ conversion: our figures are
USD and the request is in sterling, so the numbers are offered as published.

---

## Requests deliberately NOT drafted

| Request | Why not |
|---|---|
| **Anthropic — customer service (12d, medium-high, COLD)** | Crossed the >10-day line on 2026-09-23. Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal `hliwrites.99` (still verbatim on the live page, re-checked today). Send late or mark skipped — five runs unsent already. |
| **FinOps — agentic AI cost overruns (17d, high, COLD)** | The highest-relevance request we have never answered. Draft since `pitch-drafts-2026-09-17.md` §1, route LinkedIn DM to `linkedin.com/in/niloy-ghosh`. Send it late or drop it — do not redraft. |
| New this window: 8 AI-token slugs (Web3/AI/FinTech podcast guests, online-school AI grading, Newsweek restaurants, CNN relationships, HR hidden labour, Rails developers, Business Insider Instinct AI couples, Produck Podcast guests) | All eight were fetched and read in full. Every one is a different sector's adoption story, a personal-testimony call or a booking solicitation; **none contains a price, seat, licence or spend ask.** No AI+spend slug appeared in the window at all — the second run running. |
| **HR Leaders — hidden labour fixing AI output (1d)** | The closest near-miss in the window: it explicitly reasons about the cost of validating AI output ("producing a first draft costs almost nothing… knowing whether it's right costs what it always did"). But the ask is how HR leaders map workflows to see those hours — no price, seat or subscription question — and the page publishes **no route at all** (no email, no DM handle, no form). Recorded, not drafted. |
| UK conservative-commentary Substack launch (1d) | The only other new slug carrying any spend token; the token matched the word "substack", not a spend subject. |
| BBC — London businesses that dropped AI hiring tools (3d) | Wants a London employer's own decision; no cost angle in the body; address redacted with no route resolved. |
| Forbes — founders cutting AI use (5d, medium-low) | Body is explicit: "Please only answer as a comment on this post. Do not email or DM me." Wants a named founder's own rationale on the record. |
| Enterprise AI Leaders — agent sprawl (19d, high) / Scientists paying for AI (19d, high) | Both genuinely on-beat, both well past the cold line and unpitched. The cost of the cold queue, recorded so the loss is visible. |
| EdTech LMS audit (11d, crossed cold today) | Already recorded as skipped on 2026-09-15 — never sendable, so the crossing cost nothing. |
| Early-stage founders Built From Scratch (13d) | Founder-profile slot with a public-comment route. Cold. |
| Individual contributors managing agents (14d) | Pitched 2026-09-18 to Rani@Sherwood.news. No reply. |
| Amplemarket Growth/Elite (17d, high) | Pitched 2026-09-18; Jan Suski replied 2026-09-18 20:39Z, answered 21:29Z. Live thread — do not re-pitch. **A correction is still owed on the wrong 1.21x floor — see the ledger's `figures_disclosure`.** |
| Enterprise AI Leaders — value creation (10d) | Pitched 2026-09-15 to hello@foxandspindle.com. No reply in nine days. |
| Remaining live rows (26 live less the 2 above) | Off-beat calls — hospital billing, podcast guesting, PR solicitation, ML methods, alignment philosophy. All listed in `pitch-queue.md` under "Live but not sendable". |

---

## Send log — what "sent" actually means here

Three pitches have ever gone out from this monitor: 2026-09-15 (Enterprise AI Leaders → Fox & Spindle),
2026-09-18 (Amplemarket → Market Intelligence Tools), 2026-09-18 (Sherwood News → Rani Molla). One
reply, answered same day. **Pitches sent today: 0.**

**Mailbox checked 2026-09-24** (`himalaya`): **no reply to any pitch.** INBOX top is still a Google
"Security alert" (new-sign-in notice, 2026-09-23 15:59Z) above three identical "New AI tool submission"
form-mails from 2026-09-22 15:29Z. The most recent human message is still Jan Suski's 2026-09-18 20:39Z
reply, which we answered at 21:29Z. Sent Mail top unchanged at msg 187; All Mail top is msg 257. Spam
holds three items, all delivery-failure bounces and directory form-mail. **No reply to the 2026-09-15
send (nine days) or the 2026-09-18 Sherwood send (six days).**

## The one thing blocking sends that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake (`hermes mcp add --auth oauth`) that
cannot be completed from a scheduled run. It is a free read-only feed covering Connectively, HARO, X,
LinkedIn, MentionMatch and Substack — six platforms in one step, and the only path to widening a monitor
whose single accessible source has now produced **no core-beat request on five of the last six runs and
no AI+spend slug for two consecutive runs**. Endpoint re-confirmed live this run (HTTP 401,
`{"error":"invalid_token","error_description":"No authorization provided"}`), and `hermes mcp list` in
this profile still reports "No MCP servers configured."
