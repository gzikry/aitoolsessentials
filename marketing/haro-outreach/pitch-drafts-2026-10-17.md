# Pitch drafts — 2026-10-17

**Nothing here has been sent, and nothing here will be sent by the monitor.** 147 tracked requests,
**53 live unpitched, 1 sendable** (`pitch-queue.md`, built 2026-10-17). This is the eighth consecutive
run with **zero sends**.

**§1 is the whole actionable queue.** One row is live, not cold, on our beat and has a reply route
re-verified today: the Fast Company Work Life request, whose route is an email address the journalist
published himself. **§2 is included for a decision, not as a candidate** — its route is still live but
the row is 12 days old and has been past the 10-day cold line since yesterday.

**There is no third section, and that is deliberate.** Today's window added seven rows and none of them
is drafted (see the closing section). A draft with no route is not progress; it is a file.

**Figures in this file are re-derived at build time, never typed.** `data/pricing_snapshots.json` carries
`updated: 2026-10-17` and `data/tools.json` holds 79 tools: **42 publish a monthly price, 33 of those at
or under $25/month, median $17.50**. Monthly-versus-annual was re-asserted against the live snapshots:
**1.11x to 2.53x, median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, rebuilt 2026-10-16).
Per-tool figures carry their own check dates from `data/tool_sources.json` (Browse AI 2026-09-18; Gamma
2026-10-01). Every number below is one of those files or a named tool entry inside them. Nothing else is
used.

---

## 1. Fast Company Work Life — AI at work, jobs and hiring ◀ SENDABLE, low-medium, 7d old — EMAIL ROUTE

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **7 days.** Page re-read today: HTTP 200, live, badge "Posted in last 7 days".
**Who:** **Tobi Amure** — the page's own author field; a freelance finance and technology journalist whose
body text says his work runs in Investopedia, TheStreet, Forbes, Inc., Benzinga and FinanceFeeds, and who
is building pitches for **Fast Company's Work Life section**.
**Ask:** he states his own requirement in his own words — *"For experts: the credential and the research
behind it. Original data, or a survey with its sample size and method. Workplace expert is not a
credential."* And he states the door: *"No DM pitches here on LinkedIn. Email me."*

**Reply route:** **hello@tobiamure.com**, published by the journalist himself on **https://tobiamure.com/** —
re-probed today: HTTP 200, 58,905 bytes, title "Tobi Amure | Finance &amp; Technology Journalist", the
address counted **6 times** on that page. His contact page **https://tobiamure.com/contact/** re-probed
today: HTTP 200, 16,213 bytes, title "Hire a Finance &amp; Crypto Writer | Tobi Amure", address counted 5
times. `tobiamure.com` MX = Namecheap email forwarding (eforward1-5.registrar-servers.com), so the domain
routes mail. Six byline pages remain recorded dead ends so they are not retried as routes (last re-checked
2026-10-15): muckrack.com/tobi-amure, investopedia.com/tobi-amure-5203106, forbes.com/sites/tobiamure,
thestreet.com/author/tobi-amure, benzinga.com/author/tobi-amure, inc.com/author/tobi-amure — all HTTP 403.
**Technically automatable via SMTP — but sends are George's lane**, so it is a draft, not a send.

> Hi Tobi — the denominator first, since it is the thing you said you check: 88 AI tools tracked, 42 of them with a published monthly price, 33 of those at or under $25/month, median $17.50. Re-checked today, 2026-10-17.
>
> Method, in one line: we open each vendor's own pricing page by hand, record the list price, the billing term and the date we saw it, and publish the source URL with every figure. No surveys, no vendor-supplied decks.
>
> Two entries from the set speak to your AI-at-work lane. Browse AI costs $48/month or $19/month billed annually (browse.ai/pricing, checked 2026-09-18) — a 2.53x penalty for the person paying monthly out of pocket. Gamma's Pro seat is $18/month-equivalent on either term (gamma.app/pricing, checked 2026-10-01), so the penalty is not universal, which is the more interesting finding.
>
> You were right that a workplace expert is not a credential. I'm not one and won't present myself as one. This is a data set, free to quote with attribution, and I can send it as a CSV with check dates if useful.
>
> AIToolsEssentials

*Draft length: 176 words including the signature — measured on this file, not asserted (see the command
recorded in `_verify_drafts_1017.py`). Under the 200-word ceiling. Figures as above: `data/pricing_snapshots.json`
(updated 2026-10-17) plus the named Browse AI and Gamma entries in `data/tool_sources.json` with their own
`pricing_checked_date` values.*

---

## 2. WSJ blocked work accounts — what the workaround buyer pays ◀ ROUTE LIVE, ROW COLD (12d) — DECISION, NOT A CANDIDATE

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **12 days.** It crossed the 10-day cold line on 2026-10-16 and has left
the sendable list after being carried unsent through eight runs. Its route is still live; the row is not.
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist.
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work by hand.

**Honesty constraint — read before sending.** The request wants the respondent's own personal annoyance. We
are a publisher, not a blocked employee. The draft says so in its first sentence. Do not edit it out.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — re-probed today:
HTTP 200, 626,630 bytes, title "Christopher Mims - The Wall Street Journal | LinkedIn". The request's own
body says "(DMs open)".
**George's lane. Not automatable** — no address, no form, no scheduling link, so the text below is the whole
message. Dead ends recorded so they are not retried (re-probed today): `muckrack.com/christopher-mims` → HTTP
403; `wsj.com/news/author/christopher-mims` → HTTP 401.

> Hi Christopher — three numbers first, because I can't give you the personal account you asked for: I'm a publisher, not a blocked employee.
>
> We hand-check the list price of 79 AI tools. 42 publish a monthly price and 33 of those start at or under $25/month — median $17.50, re-checked today (2026-10-17).
>
> That is what the people who route around a blocked work account pay. Browse AI is $48/month against $19/month billed annually (browse.ai/pricing, checked 2026-09-18) — a 2.53x penalty for paying monthly out of pocket. Gamma's Pro seat is $18/month-equivalent on either term (gamma.app/pricing, checked 2026-10-01), so the penalty is real but not universal.
>
> Cheap enough for a personal card without asking anyone, expensive enough to add up across a year, and invisible to whoever holds the budget.
>
> Happy to send the full dated set, source URL for every number, no charge.
>
> AIToolsEssentials

*Draft length: 143 words including the signature — measured on this file, not asserted. Under the 200-word ceiling.*

---

## What was NOT drafted this run, and why

**Seven rows were added to tracking today** — every AI-token slug in the 74-slug window — and none is drafted.

- **`ai-saas-vendors-targeting-journalists-prs-and-marketers-case-studies`** is the one that scored AI+spend
  (on the bare token `saas`) and the closest to looking like a fit. It is not one. She wants CASE STUDIES
  from **brands that sell AI tools** — "HOW does your AI brand solve issues faced by these professionals?"
  We are a publisher that prices and reviews those tools, not the vendor she is asking for, and the body asks
  nothing about cost. No route either — "Pitch me :)" with no address, handle or link on the page.
- **`ai-app-and-saas-founders-1k-mrr-youtube-feature-growth-tactics`** is a promotion request wearing a
  journalist-request tag: a founder wants AI app / SaaS builders at $1K MRR featured on his YouTube channel
  ("only 100 subs right now"). Standing bar is a founder with a TrustMRR profile. Not us.
- **`real-estate-operators-ai-adoption-and-org-restructuring`** wants real-estate operators' own AI journeys,
  "DMs are open!!!". The standing bar is an operator, and the body never touches tool cost.
- **`chemistry-undergrads-and-phd-students-ai-use-in-coursework-and-research`** is a Chemistry World story on
  how chemistry students use AI. Every source it asks for is a student; it is a usage-behaviour story with no
  cost question and no printed route.
- **`ai-infrastructure-engineers-in-berlin-data-centers-and-bottlenecks`** is a reporter going to Nvidia's GTC
  to talk data-centre capacity, chips and permits. Physical infrastructure, not tool pricing.
- **`residents-near-mumbai-ai-data-centres-power-and-water-strain`** (BusinessWorld) wants residents near
  Mumbai data-centre projects and local experts. Email redacted, DM route.
- **`single-family-office-cybersecurity-experts-ai-risks-and-opportunities`** wants cybersecurity practitioners
  serving family offices, on threats and capabilities "beyond the technical aspects". Not a pricing source.

All seven are recorded in `digest-2026-10-17.json` as measurements, not as candidates.

**Standing rule that produced both sections above:** a row is drafted only when it is live, not past the
10-day line, on our beat, and has a route evidenced by a page we fetched today. That rule is why this file
has one sendable draft and the ledger still carries earlier draft rows with no send against them.

**The blocker is not supply.** 147 requests are tracked, 21 draft files are on disk, and the sendable queue
is one row. Nothing in this file can be cleared by the monitor: §1 is an email George sends, §2 is a LinkedIn
DM George sends. That is the whole gap between this monitor's finds and its sends.
