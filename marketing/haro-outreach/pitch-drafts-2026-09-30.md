# Pitch drafts — 2026-09-30

**Nothing here has been sent.** Today's queue holds **0 sendable** requests (54 tracked, 22 live
unpitched, 28 cold — `pitch-queue.md`). The queue's `_sendable()` count and the digest's both read 0,
and today they read 0 for the right reason: **every live row is either relevance `low` with no usable
route, or comment-only.** No row is live *and* ranked above the tangential band *and* carries a
resolved reply route.

**So the two drafts below are the same two rows as yesterday, re-derived and still unsent.** Both
crossed the cold line on 2026-09-28. Neither is void: both pages returned HTTP 200 today and both
reply routes were re-resolved against the live pages this run (below). A late send is still possible
on either — what was lost is the ideal window, not the pitch.

**Figures re-derived today** against `data/pricing_snapshots.json` as it stands (`updated: 2026-09-30`,
76 snapshots) and `data/monthly_annual_pairs.json` (`built: 2026-09-30`, re-asserted clean by
`scripts/extract_monthly_annual_pairs.py`, exit 0, no needle failures). Neither figure has moved since
2026-09-22 — eighth consecutive day of a clean assertion.

**Unchanged standing constraint:** no draft here claims a personal account or a customer story we do
not have. Both say what we are in the first line.

---

## 1. Shadow AI spend — employees paying out of pocket ◀ 13d, crossed cold 2026-09-28, unsent through thirteen runs

**Source:** https://www.sourcee.app/journo-request/fulltime-employees-shadow-ai-use-and-paying-outofpocket
**Posted:** 2026-09-17 11:40 UTC — **13 days**. Badge re-read off the live page today: "Posted 13 days
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

**Reply route:** `simon.chandler@raconteur.net` — **re-resolved today.** The live page
**https://www.raconteur.net/contributors/simon-chandler** returns HTTP 200 (154,857 bytes today) and
still carries `data-part1="simon.chandler" data-part2="raconteur" data-part3="net"`, which the site's
JS assembles at runtime. Control on the same run: `/contributors/tom-dennis` (HTTP 200, 154,062 bytes)
carries `tom.dennis` `raconteur` `net`. The byline URL cited on 2026-09-19 (`/author/simon-chandler/`)
still returns **HTTP 404** (re-checked today) — it is dead and must not be cited.
**George's lane. Not automatable — it is a plain email send, but the address is a reconstructed byline
address rather than one published in the request body, so it is sent by hand.**

> Subject: Shadow AI spend — what the out-of-pocket tiers actually cost
>
> Hi Simon,
>
> Straight up front: I can't give you a personal account of paying for AI behind my employer's back.
> What I can give you is what those out-of-pocket buyers are actually paying.
>
> We track dated pricing for 76 AI tools. 40 publish a monthly price; 31 of those start at or under
> $25/month — median $16.50, lowest $4 (Khanmigo, checked 2026-09-18).
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
> https://aitoolsessentials.com
>
> --
> We publish dated pricing evidence for AI tools and write about overlapping subscriptions and AI
> budget visibility. Reply "stop" and I won't follow up again.

**Figures:** 76 tools (`data/tools.json` 76 records and `data/pricing_snapshots.json` 76 snapshot
records — both re-counted today). 40 with a non-zero monthly price, 31 of those ≤$25, median $16.50,
minimum $4 Khanmigo (checked 2026-09-18) — recomputed today from `data/pricing_snapshots.json`
(`updated: 2026-09-30`). **19 same-tier monthly-vs-annual pairs across 14 tools, 1.11x–2.53x, median
1.25x** from `data/monthly_annual_pairs.json`, re-derived today; Browse AI Personal $48 vs $19 is the
widest, replit-ai Core $20 vs $18 (and Pro $100 vs $90) the narrowest. Pair snapshot dates 2026-09-18
and 2026-09-21. The 1.21x and 1.16x floors are both superseded and must not be sent.

---

## 2. Speciality Food — a £10k tech budget ◀ 12d, crossed cold 2026-09-28, October window closed — send or skip

**Source:** https://www.sourcee.app/journo-request/speciality-food-retailers-and-producers-how-theyd-spend-10k-on-tech
**Posted:** 2026-09-17 16:05 UTC — **12 days**. Badge re-read off the live page today: "Posted 12 days
ago". **Crossed the cold line on 2026-09-28, and its October issue window has closed.**
**Who:** **Holly Shackleton**, Content Editor, Speciality Food magazine.
**Ask:** for the October issue — a speciality food/drink business given £10k for EPOS, shelf labels,
ecommerce, stock and loyalty systems: how would you spend it?

**⚠ Standing constraint — read before sending.** She wants food and drink businesses. We are not one,
and our price set covers AI tools, not retail hardware. The draft's first line says so and offers the
pricing method as a benchmark. **The issue window is the reason to reconsider this one: if the October
issue is laid out, the honest move is to record a skip in `pitch-ledger.json` rather than send a late
benchmark into a closed issue.** Send only if she still has room. This is the fourth run this draft has
been carried; a fifth carry is the thing to avoid.

**Reply route:** `holly.shackleton@artichokehq.com` — re-read today off
`specialityfoodmagazine.com/contact` (HTTP 200, 59,500 bytes, byte-count identical to yesterday), listed
"Content Editor Holly Shackleton" alongside five other named staff addresses (`charlotte.smith-jarvis@`,
`jessica.brett@`, `louise.barnes@`, `sam.reubin@`, `subscriptions@`, all re-read today), so it is a
published masthead rather than a guessed pattern. **George's lane. Not automatable.**

> Subject: A £10k benchmark from dated prices, if a non-retailer's data is useful
>
> Hi Holly,
>
> I'm not a speciality food business, so I can't tell you how a retailer would spend £10k. I can offer
> you one thing retailers rarely put side by side: of the 76 software tools we track, 40 publish a
> monthly price, 31 of those start at or under $25/month, and the median cheapest paid tier is $16.50
> (checked 2026-09-18).
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
> https://aitoolsessentials.com
>
> --
> We publish dated pricing evidence for software tools and write about overlapping subscriptions and
> budget visibility. Reply "stop" and I won't follow up again.

**Figures:** 76 tools, 40 of them with a non-zero monthly price, 31 of those ≤$25, median $16.50, 19
tiers at 1.11x–2.53x — all recomputed today from `data/pricing_snapshots.json`
(`updated: 2026-09-30`) and `data/monthly_annual_pairs.json`. Deliberately **no** £/$ conversion: our
figures are USD and the request is in sterling, so the numbers are offered as published.

---

## The third sendable thing on this page is not a pitch

**A correction is owed to Jan Suski, and it is now twelve days outstanding.** He replied to our
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
| **The three NEW AI-token finds added to tracking today** | All three are recorded in `digest-2026-09-30.json` as tracked opportunities, none is drafted: **Cybersecurity Expert — AI Nexus & Security Risks** (0d) wants a named cybersecurity practitioner available for a next-day written piece, which we are not; **US Emergency Physicians & Paramedics — AI Answering 911 Calls** (1d) wants a US doctor and the address is redacted by Sourcee with no alternative route; **Job Seekers & Recruiters — AI Recruitment** (1d) is a 2SM Super Radio Network programme rundown whose segment is already booked with Randstad Australia's Madeline Hill and which invites call-ins, not pitches. |
| **Nothing new core-beat this window** | 113 slugs in the window, 3 AI-token, 0 AI+spend (eighth consecutive run with none), 10 spend-token. All 13 candidates fetched and read in full. |
| **The 10 spend-token slugs** | All consumer cost-of-living, sport or personal-finance calls: London Colts/Commanders ticket price drop, women small-business tax burden, manufacturing procurement/carbon, small-business budgeting, Irish carbon tax, UK energy price cap, home-energy benefit schemes, a paid assault-account call, FMCG licensing podcast, Sydney/Melbourne inheritance spending. They matched on 'price drop', 'cost', 'budget', 'tax', 'procurement'. |
| **Forbes — Founders Cutting AI Use (11d, crossed cold TODAY)** | The row the queue wrongly counted as sendable for two runs before the 2026-09-29 chrome-filter fix. Its body: *"Please only answer as a comment on this post. Do not email or DM me because they won't be used."* It wants a named founder's first-person rationale for cutting AI. Crossing today cost nothing — nothing sendable was ever behind it. |
| **AI Alignment Researchers — human/AI mutual understanding (11d, crossed cold TODAY)** | Low relevance, no email or handle published on the page. No route was ever resolved, so the crossing costs nothing. |
| **Anthropic — customer service (18d, cold)** | Crossed the line 2026-09-23. Draft finished and unsent since 2026-09-19 at `pitch-drafts-2026-09-22.md` §2, route Signal `hliwrites.99` (still verbatim on the live page). Send late or mark skipped. |
| **FinOps — agentic AI cost overruns (23d, high, cold)** | The highest-relevance request we have never answered. Draft since `pitch-drafts-2026-09-17.md` §1, route LinkedIn DM to `linkedin.com/in/niloy-ghosh`. Send it late or drop it — do not redraft. |
| **Business & Technology Leaders — tech budget priorities (71d) / AI SaaS users in production (131d) / SMEs — AI ops case study (204d) / MSP experts (197d)** | The four oldest rows still marked `high`/`medium` and never pitched. Recorded so the loss stays visible: these are on-beat calls the monitor found and never acted on. |
| **All other live rows (22 live minus the two drafted)** | Off-beat calls — podcast guesting, ML methods, alignment philosophy, AI-hardware makers, PDF workflows, hospital billing, insurance agents (comment-only). All listed in `pitch-queue.md` under "Live but not sendable". |

---

## Reply status — checked this run

**Mailbox checked 2026-09-30** (`himalaya`). **No reply to any tracked pitch.** The newest inbound is
still **msg 84, Lilach Bullock (2026-09-29 18:09+03:00)** — **not** a tracked-pitch reply: a reply to
the subscription-creep resource pitch offering a **$300 paid product placement** and a
15,000-subscriber newsletter partnership at 50% off, already **answered and declined the same day**
under editorial independence (Sent msg **189**, 2026-09-29, in-thread, signed AIToolsEssentials, no
personal name).

The most recent human message on a **tracked** pitch remains **Jan Suski's 2026-09-18 20:39Z reply**.
**No reply to the 2026-09-15 Enterprise AI Leaders send (fifteen days) or the 2026-09-18 Sherwood
News send (twelve days).** Sent Mail's top is still msg 189 — **no send has gone out since
2026-09-29.**

**Pitches sent today: 0.**

---

## The one thing blocking a send that is not George's

The **Medialyst MCP** feed needs an interactive OAuth handshake that cannot be completed from a
scheduled run. It is a free read-only feed covering Connectively, HARO, X, LinkedIn, MentionMatch and
Substack — six platforms in one step, and the only path to widening a monitor whose single accessible
source has now produced **no real AI+spend slug on eight consecutive runs**. Endpoint re-confirmed
live this run (HTTP 401, 74 bytes — answers and refuses without credentials).

**The structural consequence, stated plainly:** the queue's `_sendable()` count is 0, and today it is 0
for the correct reason — every live row is off-beat or comment-only, none carries a resolved route.
No new on-beat supply is arriving from Sourcee. Until either the handshake is done or one of the two
crossed drafts is sent late, the next run of this monitor will produce the same zero.
