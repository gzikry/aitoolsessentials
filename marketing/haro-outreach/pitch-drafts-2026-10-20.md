# Pitch drafts — 2026-10-20

**Nothing here has been sent. Nothing here will be sent by the monitor.** 158 tracked requests,
**47 live unpitched, 1 sendable** (`pitch-queue.md`, built 2026-10-20). This is the eleventh
consecutive run with **zero sends**.

**§1 is the whole actionable queue, and today is its last day in it.** The Fast Company Work Life row
turns 10 days old today; tomorrow the queue marks it cold. It has had a finished draft since
2026-10-17 and has been carried unsent through four runs. It does not need another draft — it needs a
send or a ledger entry, and only one of those two is a decision the monitor can't make.

**Why there is no §2.** Of the 47 live unpitched rows, 18 others carry a route string, and every one
of those is relevance `low` and off our standing: a class podcast, a Mumbai resident beside a data
centre, a Berlin infrastructure engineer, a UK political analyst, a painter whose art AI imitates.
The single other on-beat live row — `b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research`,
7 days, low-medium — publishes no address, no handle and no link, and its requester is a content
marketer at a sales-enablement vendor, not a newsroom. A draft with no route is a file, not a pitch.

**Figures are re-derived at build time, never typed.** `data/tools.json` holds 80 tools;
`data/pricing_snapshots.json` (`updated: 2026-10-20`) yields **42 with a published monthly price, 33 of
those at or under $25/month, median $17.50**. Monthly-versus-annual: **1.11x to 2.53x, median 1.25x
over 19 tiers** (`data/monthly_annual_pairs.json`, built 2026-10-16). Per-tool figures carry their own
check dates from `data/tool_sources.json` — Browse AI 2026-09-18.

---

## 1. Fast Company Work Life — AI at work, jobs and hiring ◀ SENDABLE, low-medium, 10d old — EMAIL

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **10 days.** Page re-read today: HTTP 200, 70,288 bytes,
`datePublished 2026-10-10T13:51:49Z`, badge **"Posted 10 days ago"**, request body still served.
**Who:** **Tobi Amure, CFEI®, B Pharm** — the page's own author field. He is sourcing for **Fast
Company's Work Life section** (his body: "Work Life covers how people actually work"), with an "AI at
work: what it is really changing about jobs, teams and hiring" lane open.
**Ask, in his words:** *"For experts: the credential and the research behind it. Original data, or a
survey with its sample size and method. Workplace expert is not a credential."* He also wants *"about
30 minutes on a recorded Zoom call"*, rejects *"survey data with no methodology"*, and is **"not
placing bylined guest posts"** — so the draft offers data and a call, never a post.
**The door:** *"No DM pitches here on LinkedIn. Email me."*

**Reply route — his own address, not the platform's:** **hello@tobiamure.com**, self-published.
Re-probed today (`route-checks-2026-10-20.json`, `scripts/probe_routes.py`):
**https://tobiamure.com/** HTTP 200, 60,159 bytes, title "Tobi Amure | Finance & Technology
Journalist", the address counted **6 times**; **https://tobiamure.com/contact/** HTTP 200, 16,636
bytes, the address once beside a `mailto:` link and a `<form class="contact-form">` — two routes, and
the form is the fallback if mail bounces.
**Deliverability is not SMTP-verified.** `tobiamure.com` MX is Namecheap forwarding
(eforward1-5.registrar-servers.com) and answers **554 5.7.1 Relay access denied** for `hello@`, for a
deliberately fake control address and for `postmaster@` — it refuses every recipient from an outside
probe, so that result discriminates nothing. The evidence is self-publication on his live site.

**Automatable?** It is one plain email, so technically yes — **and no.** Sends are George's lane; the
monitor has never sent one and is not sending today.

**Subject:** `The $17.50 median: what AI actually costs the person using it at work`

> Hi Tobi — the number first, since you check the denominator: 80 AI tools priced by hand, 42 with a published monthly price, 33 of those at or under $25/month, median $17.50. Snapshot re-checked today, 2026-10-20.
>
> Method, in one line: we open each vendor's own pricing page, record the list price, the billing term and the date we saw it, and publish the source URL with every figure. No surveys, no vendor decks, no estimates.
>
> Why it fits your AI-at-work lane: at $17.50 a month a tool fits inside someone's own discretionary spend, so it can reach a team without a procurement decision — one reason AI arrives in the workflow before it arrives in a budget line. The monthly penalty is measurable: across 19 same-tier pairs, paying monthly instead of annually costs 1.11x to 2.53x, median 1.25x (pairs built 2026-10-16; Browse AI $48 monthly vs $19/month billed annually, checked 2026-09-18).
>
> You're right that a workplace expert is not a credential — I'm not one. What I have is a dated data set, free to quote with attribution, CSV on request. Happy to do the 30-minute recorded call.
>
> AIToolsEssentials

**Length:** 189 words including the signature — measured on this file by `scripts/verify_drafts.py`.

---

## Cold rows with live routes — send late or record skipped, do not re-draft

Past the 10-day line, so they cost nothing to leave, but each has a paste-ready draft and a route that
is still live. Silence keeps them drifting; a ledger entry closes them.

- **`employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`** (Christopher Mims, WSJ) —
  **15d.** Route LinkedIn DM `linkedin.com/in/christopher-mims-club/`, probed today HTTP 200, 570,300
  bytes. Draft: `pitch-drafts-2026-10-17.md` §2.
- **`finops-professionals-agentic-ai-cost-overruns`** — **43d**, the oldest high-relevance row this
  monitor has never answered. Route LinkedIn DM `linkedin.com/in/niloy-ghosh`. Draft:
  `pitch-drafts-2026-09-17.md` §1.
- **`anthropic-users-and-business-owners-customer-service-experiences`** — **38d.** Route Signal
  `hliwrites.99`. Draft: `pitch-drafts-2026-09-22.md` §2.

## What was not drafted this run, and why

The six rows added today are all standing misses with no published route: a Carleton student paper
wanting Carleton students on AI and dating; WNYC wanting New Yorkers who hear AI music in cabs; a
Western English-110 class podcast; The i Paper wanting a consumer who took AI financial advice; a New
Mexico documentary wanting energy and tax experts (the window's only spend-token body hit — "taxpayer
implications" is policy, not software spend); and a McLean & Company vendor research study wanting HR
leaders. Every one asks for a first-person or professional standing we do not hold, and none asks what
an AI tool or seat costs. Full text and reasoning in digest-2026-10-20.json.
