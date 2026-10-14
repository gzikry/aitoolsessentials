# Pitch drafts — 2026-10-14

**Nothing here has been sent.** 131 tracked requests, **54 live unpitched, 2 sendable** (`pitch-queue.md`,
built 2026-10-14). This is the first run in which the sendable count is 2 rather than 1.

**Both sections are paste-ready and both are George's lane.** §1's route is a LinkedIn DM. §2's route is an
email address — resolved today, after six byline pages had dead-ended on three separate runs.

**Figures in this file are re-derived at build time, never typed.** `data/pricing_snapshots.json` carries
`updated: 2026-10-14` (77 snapshots) and `data/tools.json` holds 77 tools: **42 publish a monthly price,
33 of those at or under $25/month, median $17.50**. Per-tool figures carry their own check dates from
`data/tool_sources.json` (`checked_at: 2026-10-08`; each entry has its own `pricing_checked_date`). Every
number below is one of those two files or a specific tool entry inside them. Nothing else is used.

---

## 1. Employees blocked from AI on work accounts — what the workaround buyer pays ◀ SENDABLE, medium, 9d old — SEND TODAY

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **9 days.** Page re-read today: HTTP 200, live, badge "Posted 9 days ago".
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist (confirmed at his own byline page).
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work by hand.
**Why it fits:** the blocked employee is the enterprise mirror of this monitor's core shadow-AI request — locked out of the work account, they buy the tool personally, and that purchase is unbudgeted, unenumerated software spend.

**⚠ Honesty constraint — read before sending.** The request wants the respondent's own personal annoyance. We
are a publisher, not a blocked employee. The draft says so in its second sentence. Do not edit it out.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — re-fetched and
re-verified today: HTTP 200, 629,204 bytes, title "Christopher Mims - The Wall Street Journal | LinkedIn".
The request's own body says "(DMs open)". **George's lane. Not automatable** — no address, no form, no
scheduling link; a LinkedIn DM has no subject line, so the text below is the whole message.
Dead ends re-checked today so they are not retried: `muckrack.com/christopher-mims` → HTTP 403;
`wsj.com/news/author/christopher-mims` → HTTP 401.

> Hi Christopher — three numbers first, because I can't give you the personal account you asked for: I'm a publisher, not a blocked employee.
>
> We hand-check the list price of 77 AI tools. 42 publish a monthly price and 33 of those start at or under $25/month — median $17.50, re-checked today (2026-10-14).
>
> That is what the people who route around a blocked work account pay. Browse AI is $48/month against $19/month billed annually (browse.ai/pricing, checked 2026-09-18) — a 2.5x penalty for paying monthly out of pocket. Gamma's Pro seat is $18/month-equivalent on either term (gamma.app/pricing, checked 2026-10-01), so the penalty is real but not universal.
>
> Cheap enough for a personal card without asking anyone, expensive enough to add up across a year, and invisible to whoever holds the budget.
>
> Happy to send the full dated set, source URL for every number, no charge.
>
> AIToolsEssentials

*Draft length: 143 words including the signature (measured on this file with `[A-Za-z0-9$@./'’%+-]+`
tokenisation, not asserted) — under the 200-word ceiling. Every figure is re-derived from
`data/pricing_snapshots.json` (updated 2026-10-14) or from a named entry in `data/tool_sources.json` with its
own `pricing_checked_date` (Browse AI 2026-09-18; Gamma 2026-10-01).*

---

## 2. Fast Company Work Life — AI at work, jobs and hiring ◀ SENDABLE, low-medium, 4d old — ROUTE RESOLVED TODAY

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **4 days.** Page re-read today: HTTP 200, live, badge "Posted in last 7 days".
**Who:** **Tobi Amure** — the page's own author field; a freelance finance and tech journalist whose body text
says his work runs in Investopedia, TheStreet, Forbes, Inc., Benzinga and FinanceFeeds, and who is building
pitches for **Fast Company's Work Life section**.
**Ask:** he is explicit about what he needs — *"For experts: the credential and the research behind it. Original
data, or a survey with its sample size and method. Workplace expert is not a credential."* And explicit about
the door: *"No DM pitches here on LinkedIn. Email me."*
**Why it was unsendable until today:** the request page redacts the address. The 2026-10-11 run tried six byline
pages for him — muckrack, Investopedia, Forbes, TheStreet, Benzinga, Inc. — and **all six returned HTTP 403**.

**Reply route — resolved this run:** **hello@tobiamure.com**, published by the journalist himself on his own
site **https://tobiamure.com/** — re-fetched today: HTTP 200, 58,905 bytes, title "Tobi Amure | Finance &
Technology Journalist". The address appears verbatim three times on that page: in the Person JSON-LD `email`
field, in the FAQ answer he wrote himself ("Send the brief through the contact page or email
hello@tobiamure.com. I reply to editors within two business days."), and in the site footer. `tobiamure.com`
MX = Namecheap email forwarding (eforward1-5.registrar-servers.com), so the domain routes mail.
**Technically automatable via SMTP — but sends are George's lane**, so it is a draft, not a send.

> Hi Tobi — the denominator first, since it is the thing you said you check: 77 AI tools, 42 of them with a published monthly price, 33 of those at or under $25/month, median $17.50. Re-checked today, 2026-10-14.
>
> Method, in one line: we open each vendor's own pricing page by hand, record the list price, the billing term and the date we saw it, and publish the source URL with every figure. No surveys, no vendor-supplied decks.
>
> Two entries from the set speak to your AI-at-work lane. Browse AI costs $48/month or $19/month billed annually (browse.ai/pricing, checked 2026-09-18) — a 2.5x penalty for the person paying monthly out of pocket. Gamma's Pro seat is $18/month-equivalent on either term (gamma.app/pricing, checked 2026-10-01), so the penalty is not universal, which is the more interesting finding.
>
> You were right that a workplace expert is not a credential. I'm not one and won't present myself as one. This is a data set, free to quote with attribution, and I can send it as a CSV with check dates if useful.
>
> AIToolsEssentials

*Draft length: 175 words including the signature (measured on this file with the same tokenisation as
section 1) — under the 200-word ceiling. Figures as above: `data/pricing_snapshots.json` (updated 2026-10-14)
plus the named Browse AI and Gamma entries in `data/tool_sources.json` with their own `pricing_checked_date`
values.*

---

## What was NOT drafted this run, and why

**Eight rows were added to tracking today** — every AI-token slug in the 111-slug window — and none is drafted,
because none has a route that reaches us and none asks about tool cost: an education-policy post on school and
NGO AI adoption (the one Anthropic-adjacent row), a Star Tribune callout for Minnesotans who asked an AI about
candidates, a same-day ABC10 interview request addressed to one named adviser, a founder-story collection for
African AI founders, a two-line call for higher-ed non-faculty staff, a podcast guest invitation, a
conference-attendance ask for AI data-centre people in London, and a Flipbooker content request about buyers
pasting proposals into AI tools. Recorded as measurements, not as candidates.

**One row came close and is named so the decision is visible.** `uk-companies-implementing-ai-how-automation-
transforms-workdays` (Lindsay Dodgson, CNBC, 8d, low-medium) is on our beat's edge and says "you know where to
find me" — but the address is Sourcee-redacted, her CNBC author page 404s (`cnbc.com/lindsay-dodgson/`), and no
address of hers is published on a page we can cite. Not drafted: no verified route, and guessing an address is
not a route.

**Standing rule that produced both sections above:** a row is drafted only when it is live, not past the
10-day line, on our beat, and has a route evidenced by a page we fetched today. That rule is why this file has
two drafts and 24 earlier draft rows still sit unsent in `pitch-ledger.json`.
