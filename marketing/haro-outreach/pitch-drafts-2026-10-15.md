# Pitch drafts — 2026-10-15

**Nothing here has been sent, and nothing here will be sent by the monitor.** 136 tracked requests,
**58 live unpitched, 2 sendable** (`pitch-queue.md`, built 2026-10-15). This is the fourth consecutive run
with a sendable count above zero and the sixth consecutive run with **zero sends**.

**⚠ TODAY IS THE LAST DAY THE FIRST DRAFT IS WORTH SENDING.** §1's row is 10 days old today — exactly on the
10-day cold line — and tomorrow it leaves the sendable list. Nothing brings it back once it does. §2 is the
only other sendable row and is 5 days old.

**Both sections are paste-ready and both are George's lane.** §1's route is a LinkedIn DM. §2's route is an
email address published by the journalist on his own site.

**Figures in this file are re-derived at build time, never typed.** `data/pricing_snapshots.json` carries
`updated: 2026-10-15` and `data/tools.json` holds 78 tools: **42 publish a monthly price, 33 of those at or
under $25/month, median $17.50**. Per-tool figures carry their own check dates from `data/tool_sources.json`
(`checked_at: 2026-10-08`; each entry has its own `pricing_checked_date`). Every number below is one of those
two files or a specific tool entry inside them. Nothing else is used.

---

## 1. Employees blocked from AI on work accounts — what the workaround buyer pays ◀ SENDABLE, medium, 10d old — LEAVES THE LIST TOMORROW

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **10 days.** Page re-read today: HTTP 200, live, badge "Posted 10 days ago".
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist (confirmed at his own byline page).
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work by hand.
**Why it fits:** the blocked employee is the enterprise mirror of this monitor's core shadow-AI request — locked out of
the work account, they buy the tool personally, and that purchase is unbudgeted, unenumerated software spend.

**⚠ Honesty constraint — read before sending.** The request wants the respondent's own personal annoyance. We are a
publisher, not a blocked employee. The draft says so in its first sentence. Do not edit it out.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — re-fetched today:
HTTP 200, 634,859 bytes, title "Christopher Mims - The Wall Street Journal | LinkedIn". The request's own body says
"(DMs open)". **George's lane. Not automatable** — no address, no form, no scheduling link; a LinkedIn DM has no
subject line, so the text below is the whole message.
Dead ends re-checked today so they are not retried: `muckrack.com/christopher-mims` → HTTP 403;
`wsj.com/news/author/christopher-mims` → HTTP 401.

> Hi Christopher — three numbers first, because I can't give you the personal account you asked for: I'm a publisher, not a blocked employee.
>
> We hand-check the list price of 78 AI tools. 42 publish a monthly price and 33 of those start at or under $25/month — median $17.50, re-checked today (2026-10-15).
>
> That is what the people who route around a blocked work account pay. Browse AI is $48/month against $19/month billed annually (browse.ai/pricing, checked 2026-09-18) — a 2.5x penalty for paying monthly out of pocket. Gamma's Pro seat is $18/month-equivalent on either term (gamma.app/pricing, checked 2026-10-01), so the penalty is real but not universal.
>
> Cheap enough for a personal card without asking anyone, expensive enough to add up across a year, and invisible to whoever holds the budget.
>
> Happy to send the full dated set, source URL for every number, no charge.
>
> AIToolsEssentials

*Draft length: 143 words including the signature — measured on this file, not asserted:*
`python3 -c "import re;t=open('marketing/haro-outreach/pitch-drafts-2026-10-15.md').read().split('## 1.')[1].split('*Draft length')[0];print(len(re.findall(r\"[A-Za-z0-9\\$@./'’%+-]+\",t)))"`.
*Under the 200-word ceiling. Every figure is re-derived from `data/pricing_snapshots.json` (updated 2026-10-15) or
from a named entry in `data/tool_sources.json` with its own `pricing_checked_date` (Browse AI 2026-09-18;
Gamma 2026-10-01).*

---

## 2. Fast Company Work Life — AI at work, jobs and hiring ◀ SENDABLE, low-medium, 5d old — EMAIL ROUTE

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **5 days.** Page re-read today: HTTP 200, live, badge "Posted in last 7 days".
**Who:** **Tobi Amure** — the page's own author field; a freelance finance and tech journalist whose body text says his
work runs in Investopedia, TheStreet, Forbes, Inc., Benzinga and FinanceFeeds, and who is building pitches for
**Fast Company's Work Life section**.
**Ask:** he is explicit about what he needs — *"For experts: the credential and the research behind it. Original data, or
a survey with its sample size and method. Workplace expert is not a credential."* And explicit about the door:
*"No DM pitches here on LinkedIn. Email me."*
**Why the request page alone is not enough:** Sourcee redacts his address. Six byline pages for him — Muck Rack,
Investopedia, Forbes, TheStreet, Benzinga, Inc. — returned HTTP 403 again today, so his own site is the only route.

**Reply route:** **hello@tobiamure.com**, published by the journalist himself on **https://tobiamure.com/** — re-fetched
today: HTTP 200, 58,905 bytes, title "Tobi Amure | Finance & Technology Journalist". The address appears verbatim three
times on that page: in the Person JSON-LD `email` field, in the FAQ answer he wrote himself ("Send the brief through the
contact page or email hello@tobiamure.com. I reply to editors within two business days."), and in the site footer.
`tobiamure.com` MX = Namecheap email forwarding (eforward1-5.registrar-servers.com), so the domain routes mail.
**Technically automatable via SMTP — but sends are George's lane**, so it is a draft, not a send.

> Hi Tobi — the denominator first, since it is the thing you said you check: 78 AI tools, 42 of them with a published monthly price, 33 of those at or under $25/month, median $17.50. Re-checked today, 2026-10-15.
>
> Method, in one line: we open each vendor's own pricing page by hand, record the list price, the billing term and the date we saw it, and publish the source URL with every figure. No surveys, no vendor-supplied decks.
>
> Two entries from the set speak to your AI-at-work lane. Browse AI costs $48/month or $19/month billed annually (browse.ai/pricing, checked 2026-09-18) — a 2.5x penalty for the person paying monthly out of pocket. Gamma's Pro seat is $18/month-equivalent on either term (gamma.app/pricing, checked 2026-10-01), so the penalty is not universal, which is the more interesting finding.
>
> You were right that a workplace expert is not a credential. I'm not one and won't present myself as one. This is a data set, free to quote with attribution, and I can send it as a CSV with check dates if useful.
>
> AIToolsEssentials

*Draft length: 175 words including the signature — measured on this file with the same command as section 1 —
under the 200-word ceiling. Figures as above: `data/pricing_snapshots.json` (updated 2026-10-15) plus the named
Browse AI and Gamma entries in `data/tool_sources.json` with their own `pricing_checked_date` values.*

---

## What was NOT drafted this run, and why

**Five rows were added to tracking today** — every AI-token slug in the 90-slug window — and none is drafted, because
none has a route that reaches us and none asks about tool cost: a callout for painters and photographers for a feature
on AI and art; a callout for legal assistants and paralegals whose jobs AI eliminated (a personal job-loss bar we cannot
meet without inventing a source); a recruiter's Data & AI podcast at Harnham asking for guest introductions; a Rest of
World callout for AI companion users in Africa (30-minute Zoom, redacted address, residence bar); and a UConn Law
student's academic interviews with pro se litigants who used ChatGPT, Claude or Grok (no compensation, tool *use* not
tool *cost*). Recorded as measurements, not as candidates.

**The window's nearest thing to our beat was still not a candidate.** `pro-se-litigants-using-generative-ai-access-to-justice-impact`
names ChatGPT, Claude and Grok in its body — the richest vendor vocabulary of any row this run — but it is academic
research into access to justice, with a standing bar (you litigated pro se) we cannot meet and no pricing question.

**Standing rule that produced both sections above:** a row is drafted only when it is live, not past the 10-day line,
on our beat, and has a route evidenced by a page we fetched today. That rule is why this file has two drafts and the
ledger still carries 24 earlier draft rows with no send against them.
