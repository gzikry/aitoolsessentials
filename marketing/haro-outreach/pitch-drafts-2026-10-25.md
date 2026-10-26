# Pitch drafts — 2026-10-25

**Nothing here has been sent. This run sent nothing.** 184 tracked requests, **50 live unpitched, 1
sendable** (`pitch-queue.md`, built 2026-10-25). The ledger still records six `pitched` entries: five
delivered, one bounced (`simon.chandler@raconteur.net`, 550 NoSuchUser — dead mailbox, do not retry).

**Three drafts, all paste-ready, each behind a page that answered HTTP 200 today and a route re-probed
today.** Draft 1 is the queue's one sendable row: 2 days old and still inside the newest AI-topic feed.
Drafts 2 and 3 are the standing late sends, carried because their routes and pages are live and their
drafts exist — they are past the 10-day line, so sending them is a decision, not a queue action. All
three carry figures re-derived today so they can go out from this one document.

**Figures re-derived at build time, not typed.** `data/tools.json` holds **94 tools**;
`data/pricing_snapshots.json` (`updated: 2026-10-25`) yields **44 with a published monthly price, 35
of those at or under $25/month, median $17.50**. Monthly vs annual: **1.11x to 2.53x, median 1.25x
over 19 tiers** (`data/monthly_annual_pairs.json`, built 2026-10-16).
**Superseded — do not reuse:** the 95-tool / 40-of-31 / $16.50 sets in drafts before 2026-10-22, and
the `1.21x–2.53x, median 1.33x` pair claim sent to Jan Suski on 2026-09-18 and corrected on 2026-10-10.

---

## 1. Business Insider — European orgs moving from a US AI provider to Mistral ◀ 2d, EMAIL, paste-ready

**Source:** https://www.sourcee.app/journo-request/employees-at-european-orgs-switch-from-us-ai-provider-to-mistral
**Posted:** 2026-10-23 08:46 UTC — **2 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-23T08:46:17Z`, badge "Posted in last 7 days", no expiry notice. **In the newest
AI-topic feed**, so it is as fresh as this source can show.
**Who:** **Thibault Spirlet**, tech reporter, Business Insider London. The page's domain field is
`businessinsider.com`; the body signs *"Thibault Spirlet, Business Insider"*.
**Ask, his words:** employees at European organisations that *"have moved from, or are considering
moving from, a US AI provider like OpenAI or Anthropic, to Mistral"*, especially where data
sovereignty, procurement rules or customer contracts drove it. His fourth question is *"what trade-offs
did the switch create in model quality, cost, or developer experience?"* He offers to talk off the record.

**What we can and cannot answer.** We cannot answer the testimony part — we are not an employee of a
switching organisation, and the draft says so in its first line rather than implying standing. Cost is
one of his four questions, and it is the one we measure with dated source URLs.

**Reply route:** **tspirlet@businessinsider.com** — **automatable? No** (sends are George's lane), but
it is a plain email address, not a DM or a form.
- Resolved off his own byline page, not guessed: https://www.businessinsider.com/author/thibault-spirlet
  **HTTP 200, 326,719 bytes**, title *"Thibault Spirlet - Business Insider"*, re-probed today and
  recorded in `route-checks-2026-10-25.json`; the page publishes a `mailto:` link and the address
  appears **5 times** in the page markup.
- Fallbacks published on the same page: `linkedin.com/in/thibault-spirlet/`, `x.com/ThibaultSpirlet`.
- Deliverability not SMTP-verified — no probe was run against the BI mailbox, and one would not
  discriminate anyway.

**Subject:** `Mistral vs US providers: the per-seat numbers, dated`

> Hi Thibault —
>
> I can't give you the employee side of this: I run a price dataset, not an organisation that switched.
> I can give you the cost trade-off on your list, measured rather than estimated.
>
> As of today, 2026-10-25: Mistral's Pro tier lists at $14.99/month excluding taxes (checked
> 2026-09-18, mistral.ai/pricing). The comparable US individual tiers both list at $20/month — Claude
> Pro at $20 month-to-month or $17 on annual prepay (checked 2026-09-18, anthropic.com/pricing), ChatGPT
> Plus at $20/month (checked 2026-10-01). So at list price the Mistral seat is $5.01/month cheaper than
> either, $60.12 per seat per year, or $2.01/month cheaper against Claude Pro prepaid annually. That is
> the whole of the list-price saving — small enough that it is worth stating plainly, because the
> sovereignty case has to carry the rest. Mistral's enterprise tier is a custom quote, so the number
> your sources feel is a negotiation, not a list price.
>
> Same method, wider: of the 94 AI tools we track, 44 publish a monthly per-seat price; 35 of those
> start at or under $25/month, median $17.50.
>
> Every figure carries its check date and the vendor URL behind it. Free to use, no attribution needed.
>
> AIToolsEssentials

*Word count: 196 words including the signature — measured by `scripts/verify_drafts.py` on this file (subject line excluded).*

---

## 2. Fast Company Work Life — AI at work, jobs and hiring ◀ 15d, LATE SEND — EMAIL, paste-ready

**Source:** https://www.sourcee.app/journo-request/tech-and-hr-leaders-ai-at-work-impact-on-jobs-and-hiring
**Posted:** 2026-10-10 13:51 UTC — **15 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-10T13:51:49Z`, no expiry notice. **Not in the newest AI-topic feed** (a 50-slot
recency window), which is why it reads colder than its age.
**Who:** **Tobi Amure** — the page's own author field; sourcing for **Fast Company's Work Life** section.
**Ask, his words:** *"For experts: the credential and the research behind it. Original data, or a survey
with its sample size and method. Workplace expert is not a credential."* He is *"not placing bylined
guest posts"* — so this offers a dataset, never a post. **The door:** *"No DM pitches here on LinkedIn.
Email me."*

**Reply route:** **hello@tobiamure.com** — self-published on his own site. Re-probed today:
https://tobiamure.com/ **HTTP 200, 62,818 bytes**, title *"Tobi Amure, CFEI® | Finance & Technology
Journalist"*, address present **6 times**; fallback https://tobiamure.com/contact/ **HTTP 200, 17,905
bytes**, address 5 times, beside a contact form. **Automatable? No** — George's lane.
**Deliverability is not SMTP-verified.** `tobiamure.com` MX is Namecheap forwarding and answers
554 5.7.1 Relay access denied for `hello@`, a fake control and `postmaster@` alike, so the probe
discriminates nothing. Self-publication on his live site is the evidence; a bounce is itself the answer.

**Subject:** `The $17.50 median: method and denominator first`

> Hi Tobi —
>
> Method first, since that is the bar you set. This is not a survey: it is a census of published list
> prices. We hand-check the pricing page of 94 AI tools and store the date of every check.
>
> As of today, 2026-10-25, 44 of those 94 publish a monthly per-seat price. 35 of the 44 start at or
> under $25/month, and the median cheapest paid tier is $17.50.
>
> The same set answers the annual-discount question. Paying monthly instead of yearly costs between
> 1.11x and 2.53x, median 1.25x across 19 tiers, pair set re-asserted 2026-10-16. Two rows with their
> check dates: Browse AI Personal is $48/month or $19/month billed annually, 2.53x
> (browse.ai/pricing, checked 2026-09-18); Otter.ai Pro is $16.99/month or $8.33/month billed
> annually, 2.04x (otter.ai/pricing, checked 2026-09-18).
>
> For your AI-at-work lane that is the personal-economics half: what a seat costs the individual, and
> how often it comes out of their own pocket.
>
> You asked for the credential too. I do not have one to offer; I have a dated dataset, its method, and
> the source URL behind every number, free to use.
>
> AIToolsEssentials

*Word count: 184 words including the signature — measured by `scripts/verify_drafts.py` on this file (subject line excluded).*

---

## 3. WSJ blocked work accounts — what the workaround buyer pays ◀ 20d, LATE SEND — LINKEDIN DM

**Source:** https://www.sourcee.app/journo-request/employees-blocked-from-ai-on-work-accounts-automating-tedious-tasks
**Posted:** 2026-10-05 15:15 UTC — **20 days.** Page re-read today: HTTP 200, body served,
`datePublished 2026-10-05T15:15:11Z`, no expiry notice.
**Who:** **Christopher Mims** — the page's own author field; WSJ technology columnist.
**Ask:** quotes from people whose employer blocks AI on work accounts, forcing them to do tedious work
by hand.

**Honesty constraint — do not edit out.** The request wants the respondent's own annoyance. We are a
publisher, not a blocked employee. The draft says so in its first sentence.

**Reply route:** LinkedIn DM to **https://www.linkedin.com/in/christopher-mims-club/** — re-probed
today: **HTTP 200, 563,095 bytes**, title *"Christopher Mims - The Wall Street Journal | LinkedIn"*.
The request's own body says *"(DMs open)"*. **Automatable? No** — no address, no form, no booking link;
the text below is the whole message and must go from George's own LinkedIn.
Dead ends recorded so they are not retried: `muckrack.com/christopher-mims` HTTP 403,
`wsj.com/news/author/christopher-mims` HTTP 401.

**Subject:** none (DM)

> Hi Christopher — three numbers first, because I can't give you the personal account you asked for: I'm a publisher, not a blocked employee.
>
> We hand-check the list price of 94 AI tools. 44 publish a monthly price and 35 of those start at or under $25/month — median $17.50, checked today (2026-10-25).
>
> That is what the people who route around a blocked work account pay. Browse AI Personal is $48/month against $19/month billed annually (2.53x, checked 2026-09-18); Otter.ai Pro is $16.99 against $8.33 (2.04x, same date). Cheap enough for a personal card without asking anyone, expensive enough to add up across a year, and invisible to whoever holds the budget.
>
> Happy to send the full dated set, source URL for every number, no charge.
>
> AIToolsEssentials

*Word count: 126 words including the signature — measured by `scripts/verify_drafts.py` on this file (subject line excluded).*

---

## Not redrafted deliberately

- **This run's two new rows are not drafts.** `people-using-ai-for-social-advice-communication-and-connection-impact`
  (TOI Digital / Trisha Mahajan): the ask is personal testimony about using AI for social advice, the
  address is redacted, and the page publishes no handle or link. `video-teams-using-claude-and-remotion-agentic-video-editing`
  (Enrico Tartarotti, no outlet): wants teams doing collaborative agentic video editing; its only
  published channel is a `t.co` shortener and it asks no cost question. Neither has a route.
- **The 49 other live rows** are relevance `low` (a handful `low-medium`) with no resolved route, so
  drafting one would mean claiming standing we do not have. The exclusions are documented per row in
  `digest-2026-10-25.json`.
