# Pitch drafts — 2026-10-19

**Nothing here has been sent. Nothing here will be sent by the monitor.** 152 tracked requests,
**45 live unpitched, 1 sendable** (`pitch-queue.md`, built 2026-10-19). This is the tenth consecutive
run with **zero sends**.

**§1 is the entire actionable queue, and today is its last day in the queue.** The Fast Company Work
Life row is 9 days old and crosses the 10-day cold line tomorrow. It is the only request in 152 that
is live, on our beat, and has a reply route a human can use. There is no §2 draft, and that is a
measurement rather than an omission: of the other 44 live unpitched rows, every one is either
off-beat (a patient's story, a UK call-centre worker's day, a resident beside a data centre, a
podcast guest slot) or publishes no route at all — both of today's new rows carry a Sourcee-redacted
address and nothing else.

**Figures are re-derived at build time, never typed.** `data/pricing_snapshots.json` carries
`updated: 2026-10-19` and `data/tools.json` holds 79 tools: **42 publish a monthly price, 33 of those
at or under $25/month, median $17.50**. Monthly-versus-annual: **1.11x to 2.53x, median 1.25x over 19
tiers** (`data/monthly_annual_pairs.json`, built 2026-10-16). Per-tool figures carry their own check
dates from `data/tool_sources.json` — Browse AI 2026-09-18, Gamma 2026-10-01. Every number below is
from one of those three files.

---

## 1. Fast Company Work Life — AI at work, jobs and hiring ◀ SENDABLE, low-medium, 9d old — EMAIL

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **9 days.** Page re-read today: HTTP 200, live, badge "Posted 9 days ago".
**Who:** **Tobi Amure** — the page's own author field; a freelance finance and technology journalist
whose body says his work runs in Investopedia, TheStreet, Forbes, Inc., Benzinga and FinanceFeeds, and
who is building pitches for **Fast Company's Work Life section**.
**Ask, in his words:** *"For experts: the credential and the research behind it. Original data, or a
survey with its sample size and method. Workplace expert is not a credential."* And the door:
*"No DM pitches here on LinkedIn. Email me."*

**Reply route — his own address, not the platform's:**
**hello@tobiamure.com**, published by the journalist himself. `scripts/probe_routes.py`, run today
(`route-checks-2026-10-19.json`): **https://tobiamure.com/** HTTP 200, 60,159 bytes, title "Tobi Amure
| Finance & Technology Journalist", the address counted **6 times**; **https://tobiamure.com/contact/**
HTTP 200, 16,636 bytes, the address counted **5 times** beside a `mailto:` link and a contact form.
Fallback if the address bounces: **the form on /contact/**.
**Deliverability is not SMTP-verified and the earlier probe must not be read as a yes:**
`tobiamure.com` MX is Namecheap forwarding (eforward1-5.registrar-servers.com) and answers **554 5.7.1
Relay access denied** for `hello@`, for a deliberately fake control address and for `postmaster@` —
it refuses every recipient from an outside probe, so that result discriminates nothing. The evidence
is self-publication on his own live site.

**Automatable?** Technically yes — it is one plain email — **and no.** Sends are George's lane; the
monitor has never sent one and is not doing so today.

> Hi Tobi — the number first, since the denominator is what you said you check: 79 AI tools priced by hand, 42 with a published monthly price, 33 of those at or under $25/month, median $17.50. Re-checked today, 2026-10-19.
>
> Method, in one line: we open each vendor's own pricing page, record the list price, the billing term and the date we saw it, and publish the source URL with every figure. No surveys, no vendor decks.
>
> Why that touches your AI-at-work lane: at $17.50 a month a tool fits inside someone's own discretionary spend, so it can reach a team without a procurement decision — one reason AI shows up in workflows before it shows up in a budget line. The monthly penalty is real: across 19 same-tier pairs, paying monthly instead of annually costs 1.11x to 2.53x, median 1.25x (Browse AI: $48 vs $19, checked 2026-09-18).
>
> You're right that a workplace expert is not a credential — I'm not one. This is a dated data set, free to quote with attribution, CSV on request.
>
> AIToolsEssentials

**Subject:** `The $17.50 median: what AI actually costs the person using it at work`
**Length:** 176 words including the signature — measured on this file by `scripts/verify_drafts.py`.

---

## Cold rows with live routes — send late or record skipped, do not re-draft

These are past the 10-day line, so they cost nothing to leave, but each has a paste-ready draft and a
route that was re-probed today. Silence keeps them drifting; a ledger entry closes them.

- **`employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks`** (Christopher Mims, WSJ) —
  **14d.** Route LinkedIn DM `linkedin.com/in/christopher-mims-club/`, probed today HTTP 200, 549,248
  bytes. Draft: `pitch-drafts-2026-10-17.md` §2.
- **`finops-professionals-agentic-ai-cost-overruns`** — **42d**, the oldest high-relevance row this
  monitor has never answered. Route LinkedIn DM `linkedin.com/in/niloy-ghosh`. Draft:
  `pitch-drafts-2026-09-17.md` §1.
- **`anthropic-users-and-business-owners-customer-service-experiences`** — **37d.** Route Signal
  `hliwrites.99`. Draft: `pitch-drafts-2026-09-22.md` §2.

## What was not drafted this run, and why

Both of today's new rows want a first-person account from someone inside the situation and neither
publishes a route: **`fb-marketplace-sellers-and-buyers-ai-impact-on-pricing-and-listings`** (a
Marketplace seller or buyer on AI and resale pricing — its "pricing" token is what made it the
window's only AI+spend hit, and it is a false positive on our beat) and
**`uk-customer-service-workers-daytoday-now-ai-automation-vs-human`** (CNBC, UK customer-service
workers only). A draft with no route and false standing is a file, not a pitch.
