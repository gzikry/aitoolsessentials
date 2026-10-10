# Pitch drafts — 2026-09-28

**Nothing here has been sent.** Today's queue holds **0 sendable** requests (47 tracked, 18 live,
29 cold — `pitch-queue.md`). **Both of last run's sendable rows crossed the 10-day cold line today,
unpitched.** That is the news this page has to carry, so it leads:

- **The Raconteur shadow-AI request** (11d, high relevance) had a finished draft for **ten
  consecutive runs** and crossed unpitched this run. It is the first high-relevance request this
  queue has ever lost to the line with a paste-ready draft sitting ready.
- **The Speciality Food request** (11d) crossed the same day.

**Neither draft is void.** Both pages are still HTTP 200 and both reply routes were re-resolved
against the live pages today (below). A late send is still possible on either — what was lost is the
ideal window, not the pitch. **Both are republished below, paste-ready, with every figure re-derived
against today's data**, because the alternative is a fourth day of carrying yesterday's file.

**Figures re-derived today** against `data/pricing_snapshots.json` as it stands
(`updated: 2026-09-28`) and `data/monthly_annual_pairs.json` (`built: 2026-09-28`, re-asserted
clean by `scripts/extract_monthly_annual_pairs.py`, exit 0, no needle failures).

**Unchanged standing constraint:** no draft here claims a personal account we do not have. Both say
what we are in the first line.

---

## 1. Shadow AI spend — employees paying out of pocket ◀ CROSSED COLD TODAY at 11d — send it late, 10 runs unsent

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **11 days**. Badge re-read off the live page today: "Posted 11 days
ago". **Crossed the cold line in this run.**
**Who:** **Simon Chandler** — named in the page's own author field; covers enterprise tech for Raconteur.
**Ask:** quotes from full-time employees who use AI without their employer's knowledge and pay for it
personally. Anonymity offered.

**Why it is still worth sending late:** employees buying AI without approval and paying personally is
unbudgeted, unenumerated software spend — the quantity our dated price set exists to make visible.
Raconteur's own contact page asks for "pitches with exclusive business data", which is what we hold.
It remains the only high-relevance request this monitor has ever produced with a resolved route.

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
> https://aitoolsessentials.com
>
> --
> We publish dated pricing evidence for AI tools and write about overlapping subscriptions and AI
> budget visibility. Reply "stop" and I won't follow up again.

**Figures:** 76 tools (`data/tools.json` 76 records and `data/pricing_snapshots.json` 76 snapshot
records — both re-counted today). 40 with a non-zero monthly price, 31 of those ≤$25, median $16.50,
minimum $4 Khanmigo (checked 2026-09-18) — recomputed today from `data/pricing_snapshots.json`
(`updated: 2026-09-28`). **19 same-tier monthly-vs-annual pairs across 14 tools, 1.11x–2.53x, median
1.25x** from `data/monthly_annual_pairs.json`, re-derived today; Browse AI Personal $48 vs $19 is the
widest, replit-ai Core $20 vs $18 the narrowest. Pair dates 2026-09-18 and 2026-09-21. The 1.21x and
1.16x floors are both superseded and must not be sent.

---

## 2. Speciality Food — a £10k tech budget ◀ CROSSED COLD TODAY at 11d — send or skip

**Source:** https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
**Posted:** 2026-09-17 16:05 UTC — **11 days**. Badge re-read off the live page today: "Posted 11 days
ago". **Crossed the cold line in this run, and its October issue window has almost certainly closed.**
**Who:** **Holly Shackleton**, Content Editor, Speciality Food magazine.
**Ask:** for the October issue — a speciality food/drink business given £10k for EPOS, shelf labels,
ecommerce, stock and loyalty systems: how would you spend it?

**⚠ Standing constraint — read before sending.** She wants food and drink businesses. We are not one,
and our price set covers AI tools, not retail hardware. The draft's first line says so and offers the
pricing method as a benchmark. **The issue window is the reason to reconsider this one: if the October
issue is already laid out, the honest move is to record a skip in `pitch-ledger.json` rather than
send a late benchmark into a closed issue.** Send only if she still has room.

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
> https://aitoolsessentials.com
>
> --
> We publish dated pricing evidence for software tools and write about overlapping subscriptions and
> budget visibility. Reply "stop" and I won't follow up again.

**Figures:** 76 tools, 40 of them with a non-zero monthly price, 31 of those ≤$25, median $16.50, 19
tiers at 1.11x–2.53x — all recomputed today from `data/pricing_snapshots.json`
(`updated: 2026-09-28`) and `data/monthly_annual_pairs.json`. Deliberately **no** £/$ conversion: our
figures are USD and the request is in sterling, so the numbers are offered as published.

---

## The third sendable thing on this page is not a pitch

**A correction is owed to Jan Suski, and it is now ten days outstanding.** He replied to our
2026-09-18 Amplemarket pitch on 2026-09-18 20:39Z; our reply the same day told him the same-tier
monthly/annual range is "1.21x-2.53x, median 1.33x". That figure was wrong when it was sent and has
been superseded twice since. **The current verified figure is 1.11x–2.53x, median 1.25x over 19
tiers.** An un-flagged wrong number in a live peer method discussion is worse than a follow-up.

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
> https://aitoolsessentials.com

**Route:** reply to `jan@jansuski.com`, In-Reply-To the existing thread (msg 77 in the mailbox).
**George's lane. Not automatable.**

---

## Requests deliberately NOT drafted

| Request | Why not |
|---|---|
| **Nothing new this window** | 38 slugs, 2 AI-token, 0 AI+spend. All 5 candidates read in full. Closest near-miss: **a firm-level "training playbook" essay** on replacing apprenticeship work with AI (2026-09-27T09:00Z) — it proposes four practices and asks no question our dated price set answers. |
| **Instinct / AI companies user-growth analysis** (2026-09-27T13:55Z) | A growth practitioner writing up one AI company a week. Carries "AI" as its only token; it is a public writing series, not a request for pricing evidence. |
| **Homeowners squeezed by a rate hike** (2026-09-27T23:41Z) | SBS World News TV news call. Matched our spend regex on "repayment". Consumer cost-of-living, not software spend, and it wants on-camera homeowners. |
| **Ottawa low-cost community resources** (2026-09-27T20:53Z) | A student reporter asking users of tool libraries and free stores. Matched on "lowcost". Wrong subject and wrong standing. |
| **Retirees 55+ — cheapest places to retire** (2026-09-27T14:30Z) | Matched on "affordable". A US relocation listicle, no software content. |
| **Anthropic — customer service (16d, medium-high, COLD)** | Crossed the line 2026-09-23. Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal `hliwrites.99` (still verbatim on the live page). Send late or mark skipped — nine runs unsent already. |
| **FinOps — agentic AI cost overruns (21d, high, COLD)** | The highest-relevance request we have never answered. Draft since `pitch-drafts-2026-09-17.md` §1, route LinkedIn DM to `linkedin.com/in/niloy-ghosh`. Send it late or drop it — do not redraft. |
| **ediscovery lawyers + Gen-Z data annotators (both crossed cold today)** | Named so the crossings are visible: both were 10d → 11d today, both low relevance, neither has ever had a draft or a resolved route. No sendable row was lost. |
| **Enterprise AI Leaders — agent sprawl (23d) / Scientists paying for AI (23d)** | Both genuinely on-beat, both never pitched, both well past the cold line. Recorded so the loss stays visible. |
| All other live rows (18 live minus the crossed pairs) | Off-beat calls — podcast guesting, ML methods, alignment philosophy, AI-hardware makers, PDF workflows. All listed in `pitch-queue.md` under "Live but not sendable". |

---

## Send log — what "sent" actually means here

Three pitches have ever gone out from this monitor: 2026-09-15 (Enterprise AI Leaders → Fox & Spindle),
2026-09-18 (Amplemarket → Market Intelligence Tools), 2026-09-18 (Sherwood News → Rani Molla). One
reply, answered same day. **Pitches sent today: 0.**

**Mailbox checked 2026-09-28** (`himalaya`): **no new replies to any pitch — and no new message at
all.** The newest message is unchanged from yesterday: SaaSHub Stan (2026-09-27 13:17Z, msg 82)
reporting AIToolsEssentials is **#1,321 in the SaaSHub approval queue**, with a Priority+ upsell. Sent
Mail top unchanged at msg 187, so nothing has been sent since the 2026-09-23 directory batch. The most
recent human message remains Jan Suski's 2026-09-18 20:39Z reply. **No reply to the 2026-09-15 send
(thirteen days) or the 2026-09-18 Sherwood send (ten days).** Spam unchanged at three items.

---

## The one thing blocking sends that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake that cannot be completed from a
scheduled run. It is a free read-only feed covering Connectively, HARO, X, LinkedIn, MentionMatch and
Substack — six platforms in one step, and the only path to widening a monitor whose single accessible
source has now produced **no core-beat request on nine of the last ten runs and no real AI+spend slug
for six consecutive runs**. Endpoint re-confirmed live this run (HTTP 401,
`{"error":"invalid_token","error_description":"No authorization provided"}`).

**The structural consequence, stated plainly:** with both drafted rows crossed, the queue is now at
**zero sendable** and no new on-beat supply. Until either the handshake is done or one of the two
crossed drafts is sent late, the next run of this monitor will produce the same zero.
