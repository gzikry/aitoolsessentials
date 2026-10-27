# Pitch drafts — 2026-10-27

**Nothing here has been sent. This run sent nothing.** 195 tracked requests, **50 live unpitched, 1
sendable** (`pitch-queue.md`, built 2026-10-27). The ledger still records six `pitched` entries: five
delivered, one bounced (`simon.chandler@raconteur.net`, 550 NoSuchUser — dead mailbox, do not retry).

**Today's window produced 102 slugs and no candidate**: 7 AI tokens, 0 AI+spend, 8 body-level AI
hits, and every one of the 9 new rows asks for first-person testimony or institutional standing we
do not have (students, celebrity agents, admissions leaders, ex-engineers now trading, AI vendors,
hospitality staff, clinicians). Four redact the address; five publish nothing at all.

**The one thing that changed today, and the reason to send now.** The single sendable row —
Business Insider / Thibault Spirlet, 4 days old — is still live, still unexpired, and **left the
AI-topic feed for the second day running** (rule: colder than its age suggests). But the same
reporter **posted a new request yesterday, 2026-10-26 11:46 UTC, and it is in today's feed**. He is
commissioning two pieces this week and reading his inbox. A cost pitch that has sat unsent for four
days is not arriving late into a dead mailbox; it is arriving while he is actively working. That is
the strongest send case this queue has produced since 2026-09-15.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **97 tools**;
`data/pricing_snapshots.json` (`updated: 2026-10-27`) yields **44 with a published monthly price, 35
of those at or under $25/month, median $17.50**. Monthly vs annual: **1.11x to 2.53x, median 1.25x
over 19 tiers** (`data/monthly_annual_pairs.json`, built 2026-10-16).
**Superseded — do not reuse:** the 95-tool set in the 2026-10-26 draft, the 94-tool set in the
2026-10-25 draft, the 40/31/$16.50 sets in drafts before 2026-10-22, and the `1.21x–2.53x, median
1.33x` pair claim sent to Jan Suski on 2026-09-18 and corrected on 2026-10-10.

---

## 1. Business Insider — European orgs moving from a US AI provider to Mistral ◀ 4d, EMAIL, SEND THIS ONE

**Source:** https://www.sourcee.app/journo-request/employees-at-european-orgs-switch-from-us-ai-provider-to-mistral
**Posted:** 2026-10-23 08:46 UTC — **4 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-23T08:46:17Z`, badge "Posted in last 7 days", no expiry notice. **Not in
today's AI-topic feed** (second consecutive day out). Live, unexpired, no longer promoted.
**Who:** **Thibault Spirlet**, tech reporter, Business Insider London. Page domain
`businessinsider.com`; the body signs *"Thibault Spirlet, Business Insider"*.
**Ask, his words:** employees at European organisations that *"have moved from, or are considering
moving from, a US AI provider like OpenAI or Anthropic, to Mistral"*, especially where data
sovereignty, procurement rules or customer contracts drove it. Fourth question: *"what trade-offs did
the switch create in model quality, cost, or developer experience?"* He offers to talk off the record.

**What we can and cannot answer.** Not the testimony — we are not an employee of a switching
organisation, and the draft says so in its first line rather than implying standing. Cost is one of
his four questions and the one we measure with dated source URLs.

**Reply route:** **tspirlet@businessinsider.com** — **automatable? No** (sends are George's lane),
but it is a plain email address, not a DM and not a form.
- Resolved off his own byline page, not guessed: https://www.businessinsider.com/author/thibault-spirlet
  **HTTP 200, 326,570 bytes**, title *"Thibault Spirlet - Business Insider"*, re-probed today and
  recorded in `route-checks-2026-10-27.json`; the page publishes a `mailto:` link and the address
  appears **5 times** in the markup.
- Fallbacks on the same page: `linkedin.com/in/thibault-spirlet/`, `x.com/ThibaultSpirlet`.
- Deliverability: SMTP RCPT TO probe run today against all three of BI's Google Workspace MX
  (`aspmx.l.google.com`, `alt1`, `alt2`) answered **250 2.1.5 OK** for `tspirlet@`, for a fabricated
  control address and for `postmaster@` alike — so it rules out a domain-level rejection and nothing
  more. Google accepts at RCPT and rejects later, so this is not evidence the mailbox exists; a bounce
  is the only real evidence, and the byline `mailto:` is the evidence that it is his published address.
- **Shortest path to a sent pitch in the entire queue: one email, no form, no login.**

**Subject:** `Mistral vs US providers: the per-seat numbers, dated`

> Hi Thibault —
>
> I saw you're sourcing again this week, so: on the Mistral switch I can't give you the employee
> side. I run a price dataset, not an organisation that switched. I can give you the cost trade-off
> on your list, measured rather than estimated.
>
> As of today, 2026-10-27: Mistral's Pro tier lists at $14.99/month excluding taxes
> (mistral.ai/pricing, checked 2026-09-18). The comparable US individual tiers both list at $20 —
> ChatGPT Plus (openai.com/chatgpt/pricing, checked 2026-10-01) and Claude Pro month-to-month
> (anthropic.com/pricing, checked 2026-09-18). So the list-price saving is $5.01 per seat per month,
> $60.12 a year; against Claude Pro prepaid annually at $17 it is $2.01 a month, $24.12 a year.
>
> That is all of it — small enough that the sovereignty case has to carry the rest, which is worth
> saying plainly. Mistral's enterprise tier is a custom quote, so what your sources feel is a
> negotiation, not a list price.
>
> Same method, wider: of the 97 AI tools we track, 44 publish a monthly per-seat price, 35 of those
> at or under $25, median $17.50.
>
> Every figure carries its check date and vendor URL. Free to use, no attribution needed.
>
> AIToolsEssentials

*Word count: 193 words including the signature — measured on this file, subject line excluded.*

---

## 2. Fast Company Work Life — AI at work, jobs and hiring ◀ 17d, LATE SEND — EMAIL

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **17 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-10T13:51:49Z`, no expiry notice. **Not in today's AI-topic feed.**
**Who:** **Tobi Amure** — the page's own author field; sourcing for **Fast Company's Work Life**
section.
**Ask, his words:** *"For experts: the credential and the research behind it. Original data, or a
survey with its sample size and method. Workplace expert is not a credential."* He is *"not placing
bylined guest posts"* — so this offers a dataset, never a post. **The door:** *"No DM pitches here on
LinkedIn. Email me."*

**Reply route:** **hello@tobiamure.com** — self-published on his own site. Re-probed today:
https://tobiamure.com/ **HTTP 200, 63,292 bytes**, title *"Tobi Amure, CFEI® | Finance & Technology
Journalist"*, address present **6 times**; fallback https://tobiamure.com/contact/ **HTTP 200, 18,379
bytes**, address 5 times, beside a contact form. **Automatable? No** — George's lane.
**Deliverability is not SMTP-verified.** `tobiamure.com` MX is Namecheap forwarding and answers
554 5.7.1 Relay access denied for `hello@`, a fake control and `postmaster@` alike, so the probe
discriminates nothing. Self-publication on his live site is the evidence; a bounce is itself the answer.
**A draft for this row has been sitting in Gmail Drafts (uid 29) since 2026-10-23 with the
2026-10-23 figures in it — sending that one unedited would send aged numbers. Use this text instead.**

**Subject:** `The $17.50 median: method and denominator first`

> Hi Tobi —
>
> Method first, since that is the bar you set. This is not a survey: it is a census of published list
> prices. We hand-check the pricing page of 97 AI tools and store the date of every check.
>
> As of today, 2026-10-27, 44 of those 97 publish a monthly per-seat price. 35 of the 44 start at or
> under $25/month, and the median cheapest paid tier is $17.50.
>
> The same set answers the annual-discount question. Paying monthly instead of yearly costs between
> 1.11x and 2.53x, median 1.25x across 19 tiers, pair set re-asserted 2026-10-16. Two rows with
> their check dates: Browse AI Personal is $48/month or $19/month billed annually, 2.53x
> (browse.ai/pricing, checked 2026-09-18); Otter.ai Pro is $16.99/month or $8.33/month billed
> annually, 2.04x (otter.ai/pricing, checked 2026-09-18).
>
> For your AI-at-work lane that is the personal-economics half: what a seat costs the individual, and
> how often it comes out of their own pocket.
>
> You asked for the credential too. I do not have one to offer; I have a dated dataset, its method,
> and the source URL behind every number, free to use.
>
> AIToolsEssentials

*Word count: 184 words including the signature — measured on this file, subject line excluded.*

---

## 3. WSJ blocked work accounts — what the workaround buyer pays ◀ 22d, LATE SEND — LINKEDIN DM

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **22 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-05T15:15:11Z`, no expiry notice.
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist.
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work
by hand.

**Honesty constraint — do not edit out.** The request wants the respondent's own annoyance. We are a
publisher, not a blocked employee. The draft says so in its first sentence.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — re-probed
today: **HTTP 200, 620,486 bytes**, title *"Christopher Mims - The Wall Street Journal | LinkedIn"*.
The request's own body says *"(DMs open)"*. **Automatable? No** — no address, no form, no booking
link; the text below is the whole message and must go from George's own LinkedIn.
Dead ends recorded so they are not retried: `muckrack.com/christopher-mims` HTTP 403,
`wsj.com/news/author/christopher-mims` HTTP 401.

**Subject:** none (DM)

> Hi Christopher — three numbers first, because I can't give you the personal account you asked for: I'm a publisher, not a blocked employee.
>
> We hand-check the list price of 97 AI tools. 44 publish a monthly price and 35 of those start at or under $25/month — median $17.50, checked today (2026-10-27).
>
> That is what the people who route around a blocked work account pay. Browse AI Personal is $48/month against $19/month billed annually (2.53x, checked 2026-09-18); Otter.ai Pro is $16.99 against $8.33 (2.04x, same date). Cheap enough for a personal card without asking anyone, expensive enough to add up across a year, and invisible to whoever holds the budget.
>
> Happy to send the full dated set, source URL for every number, no charge.
>
> AIToolsEssentials

*Word count: 126 words including the signature — measured on this file, subject line excluded.*

---

## Not redrafted deliberately

- **All 9 new rows from today's window are excluded.** Each asks for testimony or standing we do not
  have: `students-whose-professors-allow-ai-ai-use-in-coursework` (students), `celebrity-agents-how-i-manage-my-money-series`
  (celebrity agents, address redacted), `admissions-leaders-and-researchers-measuring-judgment-amid-ai`
  (Forbes; admissions leaders and assessment researchers), `carleton-students-ai-dating-advice-impact-on-dating-experience`
  (Carleton students), `ai-companies-in-utilities-and-construction-frontline-safety-and-workload`
  (CNBC; AI vendors), `members-club-and-hospitality-pros-in-hong-kong-postcovid-trends` (on-camera
  hotel staff), `canadian-health-innovators-voices-of-innovation-canada-nov-16` (clinicians, book
  chapters), `excorporate-privacy-lead-built-privacy-and-ai-consultancy` (**not a request at all** — a
  founder milestone post Sourcee ingested), and
  `former-software-engineers-turned-traders-pivot-after-layoff-or-ai` (former engineers now trading;
  its author is Thibault Spirlet, whose byline route draft 1 uses).
- **The 49 other live rows** are relevance `low` (a handful `low-medium`) with no resolved route, so
  drafting one would mean claiming standing we do not have. Exclusions are documented per row in
  `digest-2026-10-27.json`. The three `high` rows that are not BI — finops (50d, LinkedIn DM),
  Science Magazine (52d, thread reply), Forbes (98d) — are all far past the line and have been
  drafted or excluded before; re-drafting them a fifth time is the failure mode this file exists to
  stop.
