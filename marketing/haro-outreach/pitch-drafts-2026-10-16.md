# Pitch drafts — 2026-10-16

**Nothing here has been sent, and nothing here will be sent by the monitor.** 140 tracked requests,
**56 live unpitched, 1 sendable** (`pitch-queue.md`, built 2026-10-16). This is the seventh consecutive run
with **zero sends**.

**§1 is the whole actionable queue.** One row is live, not cold, on our beat and has a reply route
re-verified today: the Fast Company Work Life request, whose route is an email address the journalist
published himself. **§2 is included for a decision, not as a candidate** — its route is still live but the
row crossed the 10-day cold line today and has left the sendable list.

**There is no third section, and that is deliberate.** Today's window added four rows and none of them is
drafted (see the closing section). A draft with no route is not progress; it is a file.

**Figures in this file are re-derived at build time, never typed.** `data/pricing_snapshots.json` carries
`updated: 2026-10-16` and `data/tools.json` holds 78 tools: **42 publish a monthly price, 33 of those at or
under $25/month, median $17.50**. Monthly-versus-annual was re-asserted against the live snapshots today:
**1.11x to 2.53x, median 1.25x over 19 tiers** (`data/monthly_annual_pairs.json`, rebuilt 2026-10-16). Per-tool
figures carry their own check dates from `data/tool_sources.json` (Browse AI 2026-09-18; Gamma 2026-10-01).
Every number below is one of those files or a named tool entry inside them. Nothing else is used.

---

## 1. Fast Company Work Life — AI at work, jobs and hiring ◀ SENDABLE, low-medium, 6d old — EMAIL ROUTE

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **6 days.** Page re-read today: HTTP 200, live, badge "Posted in last 7 days".
**Who:** **Tobi Amure** — the page's own author field; a freelance finance and technology journalist whose body text
says his work runs in Investopedia, TheStreet, Forbes, Inc., Benzinga and FinanceFeeds, and who is building pitches
for **Fast Company's Work Life section**.
**Ask:** he states his own requirement in his own words — *"For experts: the credential and the research behind it.
Original data, or a survey with its sample size and method. Workplace expert is not a credential."* And he states the
door: *"No DM pitches here on LinkedIn. Email me."*

**Reply route:** **hello@tobiamure.com**, published by the journalist himself on **https://tobiamure.com/** —
re-fetched today: HTTP 200, 58,905 bytes, title "Tobi Amure | Finance & Technology Journalist", the address appearing
verbatim **6 times** on that page. His contact page **https://tobiamure.com/contact/** re-fetched today: HTTP 200,
16,213 bytes, title "Hire a Finance & Crypto Writer | Tobi Amure", address verbatim 5 times.
`tobiamure.com` MX = Namecheap email forwarding (eforward1-5.registrar-servers.com), so the domain routes mail.
Six byline pages remain recorded dead ends so they are not retried as routes (last re-checked 2026-10-15):
muckrack.com/tobi-amure, investopedia.com/tobi-amure-5203106, forbes.com/sites/tobiamure, thestreet.com/author/tobi-amure,
benzinga.com/author/tobi-amure, inc.com/author/tobi-amure — all HTTP 403.
**Technically automatable via SMTP — but sends are George's lane**, so it is a draft, not a send.

> Hi Tobi — the denominator first, since it is the thing you said you check: 78 AI tools, 42 of them with a published monthly price, 33 of those at or under $25/month, median $17.50. Re-checked today, 2026-10-16.
>
> Method, in one line: we open each vendor's own pricing page by hand, record the list price, the billing term and the date we saw it, and publish the source URL with every figure. No surveys, no vendor-supplied decks.
>
> Two entries from the set speak to your AI-at-work lane. Browse AI costs $48/month or $19/month billed annually (browse.ai/pricing, checked 2026-09-18) — a 2.5x penalty for the person paying monthly out of pocket. Gamma's Pro seat is $18/month-equivalent on either term (gamma.app/pricing, checked 2026-10-01), so the penalty is not universal, which is the more interesting finding.
>
> You were right that a workplace expert is not a credential. I'm not one and won't present myself as one. This is a data set, free to quote with attribution, and I can send it as a CSV with check dates if useful.
>
> AIToolsEssentials

*Draft length: 175 words including the signature — measured on this file, not asserted (see the command recorded in
`_verify_drafts_1016.py`). Under the 200-word ceiling. Figures as above: `data/pricing_snapshots.json` (updated
2026-10-16) plus the named Browse AI and Gamma entries in `data/tool_sources.json` with their own
`pricing_checked_date` values.*

---

## 2. WSJ blocked work accounts — what the workaround buyer pays ◀ ROUTE LIVE, ROW NOW COLD (11d) — DECISION, NOT A CANDIDATE

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **11 days. It crossed the 10-day cold line today** and has left the sendable list
after being carried unsent through seven runs. Its route is still live; the row is not.
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist.
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work by hand.

**Honesty constraint — read before sending.** The request wants the respondent's own personal annoyance. We are a
publisher, not a blocked employee. The draft says so in its first sentence. Do not edit it out.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — re-fetched today: HTTP 200,
658,713 bytes, title "Christopher Mims - The Wall Street Journal | LinkedIn". The request's own body says "(DMs open)".
**George's lane. Not automatable** — no address, no form, no scheduling link, so the text below is the whole message.
Dead ends recorded so they are not retried (last re-checked 2026-10-15): `muckrack.com/christopher-mims` → HTTP 403;
`wsj.com/news/author/christopher-mims` → HTTP 401.

> Hi Christopher — three numbers first, because I can't give you the personal account you asked for: I'm a publisher, not a blocked employee.
>
> We hand-check the list price of 78 AI tools. 42 publish a monthly price and 33 of those start at or under $25/month — median $17.50, re-checked today (2026-10-16).
>
> That is what the people who route around a blocked work account pay. Browse AI is $48/month against $19/month billed annually (browse.ai/pricing, checked 2026-09-18) — a 2.5x penalty for paying monthly out of pocket. Gamma's Pro seat is $18/month-equivalent on either term (gamma.app/pricing, checked 2026-10-01), so the penalty is real but not universal.
>
> Cheap enough for a personal card without asking anyone, expensive enough to add up across a year, and invisible to whoever holds the budget.
>
> Happy to send the full dated set, source URL for every number, no charge.
>
> AIToolsEssentials

*Draft length: 143 words including the signature — measured on this file, not asserted. Under the 200-word ceiling.*

---

## What was NOT drafted this run, and why

**Four rows were added to tracking today** — every AI-token slug in the 94-slug window — and none is drafted.

- **`cios-and-ai-leaders-ai-infrastructure-day2-ops-and-costs`** is the one that had to be read twice. It is the
  window's only AI+spend slug, and the first since 2026-10-08: a CIO&Leader / ET Edge cover story that asks what AI
  "really costs" once it is running in production on a budget. It then closes the door in writing — *"As this story
  focuses on end-user experience, we will not be taking vendor quotes"* — and lists the sources it wants: end-user
  businesses in regulated BFSI, manufacturing, IT services and GCCs, pharma, retail, and mid-market CIOs, CTOs, CISOs
  and CFOs. We are a publisher of dated vendor pricing. That sentence excludes us whatever the address does.
- **`companies-and-data-buyers-selling-corporate-data-to-train-ai`** (Sam Blum) wants companies that have sold
  corporate data to an AI lab, or that buy it. Our dated set describes what AI tools cost to buy — a different
  quantity from what company data fetches. Standing bar not met; route is a DM that becomes a Signal conversation.
- **`uk-political-analysts-disinformation-and-ai-manipulation-in-politics`** is one line of text asking for UK
  political analysts. Standing bar is a practising UK political analyst; no cost question anywhere in the body.
- **`content-creators-using-ai-job-losses-and-ethics`** (Saumya Rastogi) is the closest of the four to a usable angle
  — the "insights into the ethical questions" half would take a publisher's view — but the main ask is a creator's own
  experience, the body asks nothing about what AI tools cost, and there is no route to send it to.

All four are recorded in `digest-2026-10-16.json` as measurements, not as candidates.

**Standing rule that produced both sections above:** a row is drafted only when it is live, not past the 10-day line,
on our beat, and has a route evidenced by a page we fetched today. That rule is why this file has one sendable draft
and the ledger still carries earlier draft rows with no send against them.

**The blocker is not supply.** 140 requests are tracked, 20 draft files are on disk, and the sendable queue is one
row. Nothing in this file can be cleared by the monitor: §1 is an email George sends, §2 is a LinkedIn DM George
sends. That is the whole gap between this monitor's finds and its sends.
