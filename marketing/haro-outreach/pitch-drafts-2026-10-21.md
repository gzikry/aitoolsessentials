# Pitch drafts — 2026-10-21

**Nothing here has been sent. Nothing here will be sent by the monitor.** 163 tracked requests,
**49 live unpitched, 0 sendable** (`pitch-queue.md`, built 2026-10-21). This is the twelfth
consecutive run with **zero sends**.

**Zero sendable is not zero to do.** The row this file drafts crossed the 10-day line **today**, at
11 days, with a live route and a finished draft — the second row this monitor has lost to the line
with a paste-ready pitch behind it (the WSJ blocked-work-accounts row crossed the same way on
2026-10-16). A late send is still possible on it. It is the only row in the queue with all three of:
a route verified today, a relevance above the tangential band, and a written pitch.

**Why there is no §2.** Of the 49 live unpitched rows, 21 carry a route string and **every one of
them is relevance `low`** and off our standing — a brand manager's AI case study, a CIO who has to be
in Orlando this week, a property-disclosure piece about haunted houses, a PM interview call with no
outlet named, a podcast booking at a San Jose conference. Exactly one live row is above `low`
(`b2b-buyers-procurement-revops-and-saas-leaders-ai-vendor-research`, 8 days, low-medium) and it
publishes no address, no handle and no link. A draft with no route is a file, not a pitch.

**Figures are re-derived at build time, never typed.** `data/tools.json` holds 84 tools;
`data/pricing_snapshots.json` (`updated: 2026-10-21`) yields **43 with a published monthly price, 34 of
those at or under $25/month, median $18.00**. Monthly-versus-annual: **1.11x to 2.53x, median 1.25x
over 19 tiers** (`data/monthly_annual_pairs.json`, built 2026-10-16). Per-tool figures carry their own
check dates from `data/tool_sources.json` — Browse AI 2026-09-18. **The headline set moved with today's
snapshot refresh** (from 42/33/$17.50 on 2026-10-20), so any draft in an older dated file that quotes
$17.50 or 80 tools is stale and must not be reused.

---

## 1. Fast Company Work Life — AI at work, jobs and hiring ◀ ROW CROSSED COLD TODAY, late send, low-medium, 11d — EMAIL

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **11 days.** Page re-read today: HTTP 200, body still served,
`datePublished 2026-10-10T13:51:49Z`, badge **"Posted 11 days ago"**, no expiry notice.
**Who:** **Tobi Amure** — the page's own author field. He is sourcing for **Fast Company's Work Life
section**, with an "AI at work: what it is really changing about jobs, teams and hiring" lane open.
**Ask, in his words:** *"For experts: the credential and the research behind it. Original data, or a
survey with its sample size and method. Workplace expert is not a credential."* He also wants *"about
30 minutes on a recorded Zoom call"*, rejects *"survey data with no methodology"*, and is **"not
placing bylined guest posts"** — so this offers data and a call, never a post.
**The door:** *"No DM pitches here on LinkedIn. Email me."*

**Reply route — his own address, not the platform's:** **hello@tobiamure.com**, self-published.
Re-probed today (`route-checks-2026-10-21.json`, `scripts/probe_routes.py`):
**https://tobiamure.com/** HTTP 200, 62,030 bytes, title "Tobi Amure | Finance & Technology
Journalist", the address counted **6 times**; **https://tobiamure.com/contact/** HTTP 200, 16,636
bytes, the address counted **5 times** beside a `mailto:` link and a `<form class="contact-form">` —
two routes, and the form is the fallback if mail bounces.
**Deliverability is not SMTP-verified.** `tobiamure.com` MX is Namecheap forwarding
(eforward1-5.registrar-servers.com) and answers **554 5.7.1 Relay access denied** for `hello@`, for a
deliberately fake control address and for `postmaster@` — it refuses every recipient from an outside
probe, so that result discriminates nothing. The evidence is self-publication on his live site.

**Automatable?** It is one plain email, so technically yes — **and no.** Sends are George's lane; the
monitor has never sent one and is not sending today.

**Subject:** `The $18 median: what AI actually costs the person using it at work`

> Hi Tobi — the number first, since you check the denominator: we price-check 84 AI tools by hand, 43 publish a monthly per-seat price, 34 of those sit at or under $25/month, and the median cheapest paid tier is $18.00. Snapshot re-read today, 2026-10-21.
>
> Method, in one line: we open each vendor's own pricing page, record the published list price, the billing term and the date we saw it, and publish the source URL with every figure. No surveys, no vendor decks, no estimates.
>
> Why it touches your lane without overclaiming: at $18/month a tool fits inside one person's discretionary spend, so it can reach a team before it reaches a procurement line. The annual-versus-monthly penalty is measurable across 19 same-tier pairs: 1.11x to 2.53x, median 1.25x (pairs re-asserted 2026-10-16; Browse AI Personal is $48 monthly vs $19/month billed annually, checked 2026-09-18).
>
> You're right that a workplace expert is not a credential — I'm not one and won't pitch as one. What I have is a dated price set, free to quote with attribution, CSV on request. Happy to do the 30-minute recorded call if the data is useful.
>
> AIToolsEssentials

**Length:** 190 words including the signature — measured on this file by `scripts/verify_drafts.py`.

---

## Cold rows with live routes — send late or record skipped, do not re-draft

Past the 10-day line, so they cost nothing to leave, but each has a paste-ready draft and a route that
is still live. Silence keeps them drifting; a ledger entry closes them.

- **`tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring`** (Fast Company Work Life / Tobi
  Amure) — **11d, crossed today.** Draft: §1 above. Route: `hello@tobiamure.com` plus
  `tobiamure.com/contact/`, both HTTP 200 today.
- **`employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`** (Christopher Mims, WSJ) —
  **16d.** Route LinkedIn DM `linkedin.com/in/christopher-mims-club/`, probed today HTTP 200, 535,677
  bytes. Draft: `pitch-drafts-2026-10-20.md` §1.
- **`finops-professionals-agentic-ai-cost-overruns`** — **44d**, the oldest high-relevance row this
  monitor has never answered. Route LinkedIn DM `linkedin.com/in/niloy-ghosh`. Draft:
  `pitch-drafts-2026-09-17.md` §1.
- **`anthropic-users-and-business-owners-customer-service-experiences`** — **39d.** Route Signal
  `hliwrites.99`. Draft: `pitch-drafts-2026-09-22.md` §2.

## What was not drafted this run, and why

The five rows added today are all standing misses with no published route: a MarketingSherpa
case-study call wanting brand managers; a reporter at Gartner IT Symposium/Xpo in Orlando wanting CIOs
who are physically there this week; an estate-agent and property-lawyer request about disclosing a
home's history (the window's one AI-token slug whose body never mentions AI); a product-manager
interview call with no outlet named; and a podcast booking for builders at AGNTCon/MCPCon in San Jose.
Every one asks for a first-person or professional standing we do not hold, and none asks what an AI
tool or seat costs. Full text and reasoning in `digest-2026-10-21.json`.
